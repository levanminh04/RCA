# Run after both measurement windows; no synthetic traceparent and no auth data.
import datetime as dt,json,subprocess,time,urllib.request,urllib.error
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args):return None
began=dt.datetime.now(dt.timezone.utc).isoformat()
records=[]
for route in ['ipn','return']:
    req=urllib.request.Request('http://10.0.0.158:8081/api/v1/payments/vnpay/'+route)
    try:r=urllib.request.build_opener(NoRedirect()).open(req,timeout=15)
    except urllib.error.HTTPError as error:r=error
    body=r.read()
    try:value=json.loads(body) if body else {}
    except ValueError:value={}
    records.append({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'method':'GET',
        'path':'/api/v1/payments/vnpay/'+route,'status':r.code,
        'requestId':r.headers.get('X-Request-Id'),'correlationId':r.headers.get('X-Correlation-Id'),
        'safeBody':{k:value[k] for k in ['RspCode','Message','code','message'] if k in value},
        'parameters':'none; negative signature probe'})
time.sleep(0.2)
logs=subprocess.run(['sudo','-n','docker','logs','--since',began,'flash-ticket-api-gateway-api-gateway-1'],capture_output=True,text=True)
for line in (logs.stdout+'\n'+logs.stderr).splitlines():
    try:entry=json.loads(line)
    except ValueError:continue
    for record in records:
        if entry.get('requestId')==record['requestId'] and entry.get('operation')=='http.proxy':
            record['traceId']=entry.get('traceId')
print(json.dumps({'requests':records}))
