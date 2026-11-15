#!/usr/bin/env python3
import base64
import datetime
import json
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse

root=Path('/opt/flash-ticket-app')
def env(name):
    return dict(x.split('=',1) for x in (root/'env'/name).read_text().splitlines() if x and not x.startswith('#'))
settings=env('booking-service.env')
issuer=settings['KEYCLOAK_ISSUER_URI']
def request(url, data=None, token=None):
    headers={}
    if token:
        headers['Authorization']='Bearer '+token
    if data is not None:
        headers['Content-Type']='application/x-www-form-urlencoded'
        data=urllib.parse.urlencode(data).encode()
    req=urllib.request.Request(url,data=data,headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=15) as response:
            return response.status,json.load(response)
    except urllib.error.HTTPError as e:
        try: result=json.load(e)
        except ValueError: result={}
        return e.code,result
token_status,result=request(issuer+'/protocol/openid-connect/token',{'grant_type':'client_credentials','client_id':'internal-service','client_secret':settings['INTERNAL_SERVICE_CLIENT_SECRET']})
token=result.get('access_token')
output={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'token_http_status':token_status,'issuer':issuer,'checks':[]}
if token:
    claims=json.loads(base64.urlsafe_b64decode(token.split('.')[1]+'=='))
    output['token_claims']={k:claims.get(k) for k in ['iss','aud','azp','realm_access']}
    output['issuer_matches']=claims.get('iss')==issuer
    for name,port in [('discovery-server',8761),('api-gateway',8081),('user-service',8085),('event-service',8086),('ticket-service',8084),('booking-service',8082),('payment-service',8083)]:
        try:
            host='10.0.0.158' if name=='api-gateway' else '127.0.0.1'
            status,body=request(f'http://{host}:{port}/actuator/health',token=token)
            output['checks'].append({'service':name,'http_status':status,'health':body.get('status')})
        except Exception as e:
            output['checks'].append({'service':name,'error':type(e).__name__})
    for path in ['/api/v1/events','/api/v1/events?page=0&size=5']:
        try:
            status,body=request('http://10.0.0.158:8081'+path,token=token)
            output['checks'].append({'gateway_api':path,'http_status':status,'response_keys':list(body) if isinstance(body,dict) else 'list'})
            if status==200:
                break
        except Exception as e:
            output['checks'].append({'gateway_api':path,'error':type(e).__name__})
from auth import buyer_token
buyer=buyer_token()
output['buyer_token_http_status']=200
if buyer:
    claims=json.loads(base64.urlsafe_b64decode(buyer.split('.')[1]+'=='))
    output['buyer_claims']={k:claims.get(k) for k in ['iss','aud','azp','realm_access']}
try:
    req=urllib.request.Request('http://127.0.0.1:8761/eureka/apps',headers={'Accept':'application/json'})
    with urllib.request.urlopen(req) as response:
        apps=json.load(response)['applications'].get('application',[])
    output['eureka']=[{'name':a['name'],'instances':[{'status':i['status'],'port':i['port']['$']} for i in (a['instance'] if isinstance(a['instance'],list) else [a['instance']])]} for a in apps]
except Exception as e:
    output['eureka_error']=type(e).__name__
Path('/home/ubuntu/t058/verify-app.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
