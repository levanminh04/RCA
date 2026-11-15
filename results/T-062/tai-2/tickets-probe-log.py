import json,subprocess
ids={'0e7d0afe05fa42bd981364b9b0a98350','4d91e246e65c4ec491c8b58d18c0b084','18dee2002a4f41d3855c7593f1b9ed42'}
r=subprocess.run(['sudo','-n','docker','logs','--since','2026-11-12T22:41:48Z','--until','2026-11-12T22:41:50Z','flash-ticket-ticket-service-ticket-service-1'],capture_output=True,text=True)
for l in (r.stdout+'\n'+r.stderr).splitlines():
    try:v=json.loads(l)
    except ValueError:continue
    if v.get('traceId') in ids:
        safe={k:v.get(k) for k in ['timestamp','traceId','eventName','httpStatus','errorCode','errorType']}
        safe['stackFirstLines']=v.get('stackTrace','').splitlines()[:12]
        print(json.dumps(safe))
