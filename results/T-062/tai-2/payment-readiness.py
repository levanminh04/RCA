import subprocess,json,urllib.request
d=json.loads(subprocess.check_output(['sudo','-n','docker','inspect','flash-ticket-payment-service-payment-service-1'],text=True))[0]
e=dict(l.split('=',1) for l in d['Config']['Env'] if '=' in l)
print(json.dumps({k:v for k,v in e.items() if k in ['SERVER_ADDRESS','PAYMENT_SERVICE_PORT','EUREKA_SERVER_URL','BOOKING_SERVICE_URL','PAYMENT_DOCKER_BOOKING_URL','VNPAY_API_URL']}))
for url in ['http://127.0.0.1:8761/eureka/apps/PAYMENT-SERVICE','http://127.0.0.1:8083/actuator/health','http://10.0.0.158:8083/actuator/health']:
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'Accept':'application/json'}),timeout=5) as r:
   v=json.load(r)
   if 'application' in v:
    print(json.dumps({'url':url,'instances':[{'host':i.get('hostName'),'ip':i.get('ipAddr'),'status':i.get('status'),'port':i.get('port')} for i in v['application']['instance']]}))
   else: print(json.dumps({'url':url,'status':r.code,'body':v}))
 except Exception as ex:
  print(json.dumps({'url':url,'errorType':type(ex).__name__}))
