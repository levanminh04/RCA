python3 - <<'PY'
import json,urllib.request,time,datetime as dt
d=json.load(open('/etc/flashticket-rca/load-secret/l1-tokens.json'))
def cau_truc(x,depth=0):
    if isinstance(x,dict): return {k:cau_truc(v,depth+1) for k,v in list(x.items())[:6]} if depth<2 else '{..}'
    if isinstance(x,list): return [cau_truc(x[0],depth+1)] if x else []
    return type(x).__name__
print('cau truc:',json.dumps(cau_truc(d))[:400])
def tim_token(x):
    if isinstance(x,dict):
        for k in ('accessToken','access_token','token'):
            if isinstance(x.get(k),str) and x[k].count('.')==2: return x[k]
        for v in x.values():
            t=tim_token(v)
            if t: return t
    if isinstance(x,list):
        for v in x:
            t=tim_token(v)
            if t: return t
tok=tim_token(d)
print('co token:',bool(tok))
for i in range(3):
    t0=dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%SZ')
    rq=urllib.request.Request('http://129.221.208.47:8081/api/v1/me',headers={'Authorization':'Bearer '+tok})
    try:
        with urllib.request.urlopen(rq,timeout=10) as r: print(t0,'GET /api/v1/me',r.status,len(r.read()),'byte')
    except Exception as e: print(t0,'LOI',repr(e)[:150])
    time.sleep(3)
PY
