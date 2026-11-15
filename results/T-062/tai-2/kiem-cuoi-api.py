# Read-only probes, to run BETWEEN the two measurement windows.
abandoned=api('GET','/api/v1/orders/375499e4-64d7-4800-b114-e905d07fc2ba','BUYER')
available=api('GET','/api/v1/events/3e7c1df9-ada4-4081-94a1-548b80a5da86/availability')
print(json.dumps({'abandoned':abandoned,'availability':available,'requests':evidence}))
service_token=internal_token()
for oid in ['ee1d0aa3-e45c-4100-9a69-bb9f56979210','b16ae2e8-3893-466d-94eb-08ace3a9ace2','e8117cb3-609e-4ddd-a0c3-a179dcf17462','2f6c01b2-ab05-49d5-affc-3c0bbafb67a2']:
    trace=uuid.uuid4().hex
    req=urllib.request.Request('http://127.0.0.1:8084/internal/v1/orders/'+oid+'/issuance',
        headers={'Authorization':'Bearer '+service_token,'traceparent':'00-'+trace+'-'+uuid.uuid4().hex[:16]+'-01'})
    try:r=urllib.request.urlopen(req,timeout=15)
    except urllib.error.HTTPError as error:r=error
    value=json.load(r)
    print(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'orderId':oid,'probeStatus':r.code,
        'traceId':trace,'data':{k:v for k,v in value.items() if k in ['state','orderId','issuanceId','code','message']}}))
