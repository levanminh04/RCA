import os,hashlib
kc=env('keycloak.env')
issuer=env()['KEYCLOAK_ISSUER_URI']
base=issuer.split('/realms/')[0]
admin_data=urllib.parse.urlencode({'grant_type':'password','client_id':'admin-cli',
    'username':kc['KC_BOOTSTRAP_ADMIN_USERNAME'],'password':kc['KC_BOOTSTRAP_ADMIN_PASSWORD']}).encode()
try:
    with urllib.request.urlopen(base+'/realms/master/protocol/openid-connect/token',data=admin_data,timeout=20) as r:
        admin=json.load(r)['access_token']
except Exception:
    raise SystemExit('Admin authentication failed; secrets omitted')
def call(method,path,body=None):
    req=urllib.request.Request(base+'/admin/realms/flash-ticket'+path,
        data=None if body is None else json.dumps(body).encode(),method=method,
        headers={'Authorization':'Bearer '+admin,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            b=r.read(); return json.loads(b) if b else None
    except urllib.error.HTTPError as ex:
        raise RuntimeError('Admin API '+method+' '+path.split('?')[0]+': '+str(ex.code)) from None
path=ROOT/'env/l1-buyers.json'
os.umask(0o077)
pool=json.loads(path.read_text()) if path.exists() else []
before=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
role=call('GET','/roles/BUYER')
for i in range(1,21):
    name=f'load-buyer-{i:02d}@example.invalid'
    if any(u['username']==name for u in pool):
        continue
    if call('GET','/users?username='+urllib.parse.quote(name)+'&exact=true'):
        raise SystemExit('Name exists outside retained pool; stopped')
    password=secrets.token_urlsafe(30)
    call('POST','/users',{'username':name,'email':name,'emailVerified':True,'enabled':True,
        'firstName':'Load','lastName':f'Buyer {i:02d}',
        'credentials':[{'type':'password','value':password,'temporary':False}]})
    users=call('GET','/users?username='+urllib.parse.quote(name)+'&exact=true')
    if len(users)!=1:
        raise SystemExit('Created user lookup not unique')
    user=users[0]
    call('POST','/users/'+user['id']+'/role-mappings/realm',[role])
    pool.append({'id':user['id'],'username':name,'password':password,'realmRoles':['BUYER']})
    path.write_text(json.dumps(pool)); os.chmod(path,0o600)
print(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'count':len(pool),
    'secretFile':str(path),'sha256Before':before,'sha256After':hashlib.sha256(path.read_bytes()).hexdigest(),
    'users':[{'id':u['id'],'username':u['username']} for u in pool],
    'rollback':'Delete only these users via Keycloak admin API; retain secret file as rollback evidence, mode 0600.'}))
