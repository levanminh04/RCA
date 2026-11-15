# Read-only validation of response request IDs. No synthetic traceparent.
bearer=role_token('BUYER')
for path in ['/api/v1/events','/api/v1/events/3e7c1df9-ada4-4081-94a1-548b80a5da86',
    '/api/v1/events/3e7c1df9-ada4-4081-94a1-548b80a5da86/availability',
    '/api/v1/orders/2f6c01b2-ab05-49d5-affc-3c0bbafb67a2',
    '/api/v1/orders/2f6c01b2-ab05-49d5-affc-3c0bbafb67a2/payment',
    '/api/v1/orders/2f6c01b2-ab05-49d5-affc-3c0bbafb67a2/tickets']:
    req=urllib.request.Request('http://10.0.0.158:8081'+path,headers={'Authorization':'Bearer '+bearer})
    with urllib.request.urlopen(req,timeout=15) as r:
        r.read();print(json.dumps({'path':path,'status':r.code,'requestId':r.headers.get('X-Request-Id'),'correlationId':r.headers.get('X-Correlation-Id'),'utc':dt.datetime.now(dt.timezone.utc).isoformat()}))
