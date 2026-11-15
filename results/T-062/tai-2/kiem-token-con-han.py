import base64,datetime as dt,json,time
from pathlib import Path
p=Path('/opt/rca-tai/secret/l1-tokens.json')
if not p.exists():
    print(json.dumps({'count':0,'minAccessRemaining':0,'minRefreshRemaining':0}));raise SystemExit()
values=json.loads(p.read_text())['tokens'];now=int(time.time())
def claims(token):return json.loads(base64.urlsafe_b64decode(token.split('.')[1]+'=='))
access=[claims(v['access_token']) for v in values]
refresh=[claims(v['refresh_token']) for v in values]
print(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'count':len(values),
    'minAccessRemaining':min(c['exp']-now for c in access),
    'minRefreshRemaining':min(c['exp']-now for c in refresh),
    'allBuyer':all('BUYER' in c.get('realm_access',{}).get('roles',[]) for c in access),
    'permissionsOctal':oct(p.stat().st_mode&0o777)}))
