import collections,datetime as dt,json,subprocess
counts=collections.Counter();errors=[];gateway=[]
for service in ['payment-service','booking-service','api-gateway']:
    name=f'flash-ticket-{service}-{service}-1'
    result=subprocess.run(['sudo','-n','docker','logs','--since','2026-11-13T02:56:00Z','--until','2026-11-13T03:00:00Z',name],text=True,capture_output=True)
    chosen=[]
    for line in (result.stdout+'\n'+result.stderr).splitlines():
        try:v=json.loads(line)
        except ValueError:continue
        counts[(service,v.get('eventName'),v.get('severity'))]+=1
        if v.get('severity') in ['WARN','ERROR'] or v.get('httpStatus',0)>=500:
            if len(chosen)<12:
                safe={k:v.get(k) for k in ['timestamp','serviceName','eventName','severity','traceId','requestId','routeId','httpStatus','reasonCode','errorCode','errorType','operation','outcome','durationMs','message']}
                safe['stackFirstLines']=v.get('stackTrace','').splitlines()[:18]
                chosen.append(safe)
    errors.append({'service':service,'records':chosen})
    inspected=json.loads(subprocess.check_output(['sudo','-n','docker','inspect',name],text=True))[0]
    print(json.dumps({'container':name,'state':inspected['State'],'restartCount':inspected['RestartCount']}))
print(json.dumps({'eventCounts':{'|'.join(str(x) for x in k):v for k,v in counts.items()},'samples':errors}))
