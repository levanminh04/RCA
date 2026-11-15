import json,base64,pathlib,collections,datetime as dt
p=pathlib.Path('/opt/rca-tai/secret/l1-tokens.json')
pool=json.loads(p.read_text())['tokens']
claims=[json.loads(base64.urlsafe_b64decode(t['access_token'].split('.')[1]+'==')) for t in pool]
print(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'sessions':len(pool),
    'distinctSubjects':len({c['sub'] for c in claims}),
    'allBuyer':all('BUYER' in c.get('realm_access',{}).get('roles',[]) for c in claims),
    'tokenLifetimeSeconds':dict(collections.Counter(c['exp']-c['iat'] for c in claims)),
    'permissionsOctal':oct(p.stat().st_mode&0o777)}))
