#!/usr/bin/env python3
import base64
import datetime
import json
from pathlib import Path
import secrets
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from auth import role_token

root=Path('/home/ubuntu/t058')
e=dict(x.split('=',1) for x in Path('/opt/flash-ticket-infra/.env').read_text().splitlines() if x and not x.startswith('#'))
basic='Basic '+base64.b64encode((e['RABBITMQ_ADMIN_USERNAME']+':'+e['RABBITMQ_ADMIN_PASSWORD']).encode()).decode()
def rabbit(path):
    req=urllib.request.Request('http://127.0.0.1:15672'+path,headers={'Authorization':basic})
    with urllib.request.urlopen(req,timeout=10) as response: return json.load(response)
def snapshot():
    overview=rabbit('/api/overview')
    queues=rabbit('/api/queues')
    output=subprocess.check_output(['docker','exec','flash-ticket-infra-redis-1','sh','-c','REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli INFO commandstats'],text=True)
    stats={}
    for line in output.splitlines():
        if line.startswith(('cmdstat_get:','cmdstat_set:','cmdstat_del:')):
            key,rest=line.split(':',1)
            stats[key]={k:float(v) for k,v in (part.split('=') for part in rest.split(','))}
    return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'redis_commandstats':stats,
            'rabbit_message_stats':{k:v for k,v in overview.get('message_stats',{}).items() if isinstance(v,(int,float))},
            'rabbit_queue_totals':overview.get('queue_totals',{}),
            'rabbit_queues':[{'name':q['name'],'messages':q.get('messages'),
                              'message_stats':{k:v for k,v in q.get('message_stats',{}).items() if isinstance(v,(int,float))}} for q in queues]}
result={'before':snapshot()}
subprocess.run(['python3',str(root/'smoke-api.py'),'--agent','--payment','--output=traffic-probe-order-flow'],check=True,stdout=subprocess.DEVNULL)
time.sleep(7)
result['after_order_flow']=snapshot()
# An independent, disposable synthetic event exercises the real event outbox
# and the three cancellation consumers without changing the load fixture.
original=json.loads((root/'seed-fixture.json').read_text())
ids={k:str(uuid.uuid4()) for k in ['category_id','venue_id','event_id','ticket_type_id','second_ticket_type_id']}
sql=(root/'seed-minimal.sql').read_text().replace('Evening concert','Afternoon concert')
for key,val in ids.items(): sql=sql.replace(original[key],val)
(root/'seed-second-event.sql').write_text(sql)
p=subprocess.run(['docker','exec','-i','flash-ticket-infra-postgres-1','psql','-X','-v','ON_ERROR_STOP=1','-U','postgres','-d','postgres'],input=sql,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
if p.returncode:
    raise SystemExit('Disposable event seed failed')
token=role_token('ADMIN')
traceid=secrets.token_hex(16)
path='/api/v1/admin/events/'+ids['event_id']+'/cancel'
req=urllib.request.Request('http://10.0.0.158:8081'+path,data=b'{"rowVersion":"0"}',method='POST',
                           headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','traceparent':'00-'+traceid+'-'+secrets.token_hex(8)+'-01'})
try:
    with urllib.request.urlopen(req,timeout=30) as r:
        body=json.load(r); status=r.status
except urllib.error.HTTPError as r:
    status=r.code
    try:body=json.load(r)
    except ValueError:body={}
result['cancellation_api']={'path':path,'status':status,'trace_id':traceid,'event_status':body.get('status'),'code':body.get('code')}
time.sleep(10)
result['after_cancellation_flow']=snapshot()
result['synthetic_second_event_id']=ids['event_id']
(root/'traffic-probe.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:({'utc':v['utc'],'redis_commandstats':v['redis_commandstats'],'rabbit_message_stats':v['rabbit_message_stats']} if k in ['before','after_order_flow','after_cancellation_flow'] else v) for k,v in result.items()},indent=2))
