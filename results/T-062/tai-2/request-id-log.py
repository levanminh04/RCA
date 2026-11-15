import json,subprocess
r=subprocess.run(['sudo','-n','docker','logs','--since','2026-11-12T22:43:53Z','--until','2026-11-12T22:43:55Z',
    'flash-ticket-api-gateway-api-gateway-1'],capture_output=True,text=True)
ids={'48494c7f-28cb-406f-9126-b41a42132f96','1120cf25-5d66-43b7-9105-a6a1cac69e9f',
    '0521e5b0-28f5-4515-9fcf-5f08c87f2696','57566e77-369e-4579-9e89-c7e93f7da961',
    'cf6121de-3455-48b6-82cb-d8759c1d38d1','a040167e-c348-4ede-9642-87923cd1fe88'}
for line in (r.stdout+'\n'+r.stderr).splitlines():
    try:v=json.loads(line)
    except ValueError:continue
    if v.get('requestId') in ids:
        print(json.dumps({k:v.get(k) for k in ['timestamp','traceId','requestId','routeId','httpStatus']}))
