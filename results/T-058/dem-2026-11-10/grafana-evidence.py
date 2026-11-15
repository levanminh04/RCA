import base64
import datetime
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

e=dict(line.split('=',1) for line in Path('/opt/flash-ticket-obs/grafana.env').read_text().splitlines() if '=' in line)
basic='Basic '+base64.b64encode((e['GF_SECURITY_ADMIN_USER']+':'+e['GF_SECURITY_ADMIN_PASSWORD']).encode()).decode()
base='http://10.0.0.215:3000'
def get(url,auth=False,data=None):
    headers={'Authorization':basic} if auth else {}
    if data is not None: headers['Content-Type']='application/json'
    with urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(data).encode() if data is not None else None,headers=headers),timeout=30) as r:
        return json.load(r)

smoke=json.loads(Path('/home/ubuntu/t058/smoke-api-agent.json').read_text())
trace=next(x['trace_id'] for x in smoke['checks'] if 'availability' in x['path'])
queries={
 'redis':'{ span.db.system = "redis" || span.db.system.name = "redis" }',
 'rabbitmq':'{ span.messaging.system = "rabbitmq" }',
 'producer_consumer':'{ kind = producer || kind = consumer }',
 'postgresql':'{ span.db.system = "postgresql" || span.db.system.name = "postgresql" }',
}
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'traceql':{},'grafana_proxies':{}}
for name,q in queries.items():
    params={'q':q,'start':int(time.time())-3600,'end':int(time.time()),'limit':1000}
    body=get('http://127.0.0.1:3200/api/search?'+urllib.parse.urlencode(params))
    result['traceql'][name]={'query':q,'returned_traces':len(body.get('traces',[])),'limit':1000,'trace_ids':[x.get('traceID') for x in body.get('traces',[])[:8]]}
query='count by(service_name) (http_server_request_duration_seconds_count)'
body=get(base+'/api/datasources/proxy/uid/prometheus/api/v1/query?'+urllib.parse.urlencode({'query':query}),True)
result['grafana_proxies']['metrics']={'query':query,'status':body['status'],'series':body['data']['result']}
body=get(base+'/api/datasources/proxy/uid/loki/loki/api/v1/query_range?'+urllib.parse.urlencode({'query':'{service_name="booking-service"}','limit':10}),True)
result['grafana_proxies']['logs']={'status':body['status'],'streams':len(body['data']['result']),'rows':sum(len(x['values']) for x in body['data']['result'])}
body=get(base+'/api/datasources/proxy/uid/tempo/api/traces/'+trace,True)
batches=body.get('batches',body.get('resourceSpans',[]))
count=sum(len(g.get('spans',[])) for b in batches for g in b.get('scopeSpans',b.get('instrumentationLibrarySpans',[])))
result['grafana_proxies']['traces']={'trace_id':trace,'span_count':count,'top_level_keys':list(body)}
panels=[
 {'id':1,'type':'timeseries','title':'HTTP requests / second','gridPos':{'x':0,'y':0,'w':12,'h':8},'datasource':{'type':'prometheus','uid':'prometheus'},'targets':[{'refId':'A','expr':'sum by(service_name) (rate(http_server_request_duration_seconds_count[2m]))','legendFormat':'{{service_name}}'}]},
 {'id':2,'type':'timeseries','title':'JVM memory used','gridPos':{'x':12,'y':0,'w':12,'h':8},'datasource':{'type':'prometheus','uid':'prometheus'},'targets':[{'refId':'A','expr':'sum by(service_name) (jvm_memory_used_bytes)','legendFormat':'{{service_name}}'}],'fieldConfig':{'defaults':{'unit':'bytes'},'overrides':[]}},
 {'id':3,'type':'logs','title':'Application logs','gridPos':{'x':0,'y':8,'w':24,'h':10},'datasource':{'type':'loki','uid':'loki'},'targets':[{'refId':'A','expr':'{service_name=~"api-gateway|booking-service|event-service|payment-service|ticket-service|user-service|keycloak|discovery-server"}','queryType':'range'}]},
 {'id':4,'type':'traces','title':'Gateway to booking: availability trace','gridPos':{'x':0,'y':18,'w':24,'h':12},'datasource':{'type':'tempo','uid':'tempo'},'targets':[{'refId':'A','queryType':'traceId','query':trace}]},
]
dashboard={'uid':'t058-flashticket','title':'FlashTicket T-058','schemaVersion':41,'version':0,'refresh':'30s','time':{'from':'now-30m','to':'now'},'panels':panels,'tags':['FlashTicket']}
created=get(base+'/api/dashboards/db',True,{'dashboard':dashboard,'overwrite':True,'message':'Initial telemetry verification dashboard'})
result['dashboard']={k:created.get(k) for k in ['uid','url','status','version']}
Path('/home/ubuntu/t058/grafana-evidence.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
