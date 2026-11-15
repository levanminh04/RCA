import json,urllib.request
traces={'v1_synthetic_parent':'206402e5dba5c8219b11fb79cdbdcfb0',
    'without_traceparent':'b10d3b381a35edf1eba152ead094705e'}
def walk(v):
    if isinstance(v,dict):
        for s in v.get('spans',[]):yield s
        for k,x in v.items():
            if k!='spans':yield from walk(x)
    elif isinstance(v,list):
        for x in v:yield from walk(x)
for label,tid in traces.items():
    with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:3200/api/traces/'+tid,headers={'Accept':'application/json'}),timeout=20) as r:
        spans=list(walk(json.load(r)))
    ids={s['spanId'] for s in spans}
    missing=[{k:s.get(k) for k in ['name','kind','spanId','parentSpanId']} for s in spans if s.get('parentSpanId') and s['parentSpanId'] not in ids]
    roots=[{k:s.get(k) for k in ['name','kind','spanId','parentSpanId']} for s in spans if not s.get('parentSpanId')]
    print(json.dumps({'label':label,'traceId':tid,'spans':len(spans),'missingParents':missing,'roots':roots}))
