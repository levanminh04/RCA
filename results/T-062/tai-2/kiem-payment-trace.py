import collections,datetime as dt,json,urllib.request
ids=['b3d9fc69c85d9e3b2bc7bd449f6407a5','7ac27fe8ee682ae8a03897a39b90fba1']
allowed={'http.route','http.response.status_code','http.request.method','server.address','server.port',
    'error.type','exception.type','db.system','db.system.name','db.query.summary','messaging.destination.name',
    'thread.name','rpc.method','rpc.service','network.peer.address'}
def walk(v,service=None):
    if isinstance(v,dict):
        if 'resource' in v:
            for a in v['resource'].get('attributes',[]):
                if a['key']=='service.name':service=a['value'].get('stringValue')
        for s in v.get('spans',[]):yield service,s
        for k,x in v.items():
            if k!='spans':yield from walk(x,service)
    elif isinstance(v,list):
        for x in v:yield from walk(x,service)
for tid in ids:
    try:
        with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:3200/api/traces/'+tid,headers={'Accept':'application/json'}),timeout=20) as r:v=json.load(r)
        spans=[]
        for service,s in walk(v):
            attrs={a['key']:a['value'] for a in s.get('attributes',[]) if a['key'] in allowed}
            events=[{'name':e.get('name'),'attributes':{a['key']:a['value'] for a in e.get('attributes',[]) if a['key'] in allowed}} for e in s.get('events',[])]
            spans.append({'service':service,'name':s.get('name'),'kind':s.get('kind'),'spanId':s.get('spanId'),
                'parentSpanId':s.get('parentSpanId'),'durationMs':(int(s['endTimeUnixNano'])-int(s['startTimeUnixNano']))/1e6,
                'status':s.get('status'),'attributes':attrs,'events':events})
        print(json.dumps({'traceId':tid,'count':len(spans),'slowest':sorted(spans,key=lambda x:x['durationMs'],reverse=True)[:20]}))
    except Exception as ex:print(json.dumps({'traceId':tid,'errorType':type(ex).__name__}))
