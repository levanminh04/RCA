#!/usr/bin/env python3
import datetime
import json
from pathlib import Path
import secrets
import sys
import time
import urllib.error
import urllib.request
import uuid
from auth import buyer_token

root=Path('/home/ubuntu/t058')
fixture=json.loads((root/'seed-fixture.json').read_text())
token=buyer_token()
results={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':[]}
def call(method,path,body=None,key=None):
    traceid=secrets.token_hex(16)
    headers={'Authorization':'Bearer '+token,'traceparent':'00-'+traceid+'-'+secrets.token_hex(8)+'-01'}
    if body is not None: headers['Content-Type']='application/json'
    if key: headers['Idempotency-Key']=key
    req=urllib.request.Request('http://10.0.0.158:8081'+path,data=json.dumps(body).encode() if body is not None else None,headers=headers,method=method)
    t=time.monotonic()
    try:
        with urllib.request.urlopen(req,timeout=40) as r:
            status=r.status; result=json.load(r)
    except urllib.error.HTTPError as r:
        status=r.code
        try: result=json.load(r)
        except ValueError: result={}
    rec={'method':method,'path':path,'status':status,'latency_ms':round((time.monotonic()-t)*1000,2),'trace_id':traceid}
    if isinstance(result,dict):
        rec['keys']=list(result)
        for k in ['code','message','orderId','state','status','totalAmount','total','expiresAt']:
            if k in result: rec[k if k!='status' else 'business_status']=result[k]
        if isinstance(result.get('data'),dict):
            rec['data_keys']=list(result['data'])
            rec['payment_url_present']=bool(result['data'].get('paymentUrl'))
    results['checks'].append(rec)
    return status,result

call('GET','/api/v1/events')
call('GET','/api/v1/events/'+fixture['event_id'])
call('GET','/api/v1/events/'+fixture['event_id']+'/availability')
if '--read-only' not in sys.argv:
    body={'eventId':fixture['event_id'],'customerEmail':'buyer@example.invalid',
          'selection':{'mode':'QUANTITY','items':[{'ticketTypeId':fixture['ticket_type_id'],'quantity':1}]}}
    key=str(uuid.uuid4())
    status,order=call('POST','/api/v1/orders',body,key)
    if status==201 and order.get('orderId'):
        orderid=order['orderId']
        _,replay=call('POST','/api/v1/orders',body,key)
        results['idempotency_same_order']=replay.get('orderId')==orderid
        call('GET','/api/v1/orders/'+orderid)
        if '--payment' in sys.argv:
            call('POST','/api/v1/payments',{'orderId':orderid},str(uuid.uuid4()))
        # Release this disposable hold, preserving its audit trail.
        call('POST','/api/v1/orders/'+orderid+'/cancel',{})
output=root/('smoke-api-agent.json' if '--agent' in sys.argv else 'smoke-api-baseline.json')
for arg in sys.argv:
    if arg.startswith('--output='):
        output=root/(arg.split('=',1)[1]+'.json')
if output.exists():
    output.rename(output.with_stem(output.stem+'-'+datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S')))
output.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
