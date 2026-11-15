import json,subprocess
r=subprocess.run(['sudo','-n','docker','logs','--since',SINCE,'--until',UNTIL,
    'flash-ticket-api-gateway-api-gateway-1'],capture_output=True,text=True)
if r.returncode:raise SystemExit('Gateway logs failed')
for line in (r.stdout+'\n'+r.stderr).splitlines():
    try:v=json.loads(line)
    except ValueError:continue
    if v.get('eventName') in ['gateway.request.completed','gateway.request.failed','gateway.request.rejected','gateway.request.cancelled']:
        print(json.dumps({k:v.get(k) for k in ['timestamp','traceId','routeId','httpMethod','httpStatus','reasonCode','durationMs','requestId','correlationId']}))
