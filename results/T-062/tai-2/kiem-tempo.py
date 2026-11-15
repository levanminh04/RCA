import urllib.request,json,collections,base64
ids=['3c948dea77c249cd9165b3b12f9aca99','01a40fbceeff4ab2a3d8b4d6382fe225',
     '7ca3dcbae6bc41178554fa76281e994f','2fb98b05a0842b81daf282eb14d7f7bb',
     'b659ab1b00b5f810206e1f24ecd62bde','de8e3fd47b38025d87bf987ef568e70a',
     'c6c075e2468997703e9be083609c1a78','4cf0e56227debf23e7e44ab856165f54']
def walk(v):
    if isinstance(v,dict):
        if 'spans' in v:
            for s in v['spans']:
                yield s
        for k,x in v.items():
            if k!='spans': yield from walk(x)
    elif isinstance(v,list):
        for x in v: yield from walk(x)
for tid in ids:
    try:
        with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:3200/api/traces/'+tid,headers={'Accept':'application/json'}),timeout=20) as r:
            v=json.load(r)
        spans=list(walk(v)); kinds=collections.Counter(str(s.get('kind')) for s in spans)
        safe=[{k:s.get(k) for k in ['name','kind','traceId','spanId','parentSpanId','startTimeUnixNano','endTimeUnixNano','status']} for s in spans]
        print(json.dumps({'traceId':tid,'count':len(spans),'kinds':dict(kinds),'spans':safe}))
    except Exception as ex:
        print(json.dumps({'traceId':tid,'errorType':type(ex).__name__}))
