set -eu
python3 - <<'PY'
import subprocess,json,pathlib,hashlib
root=pathlib.Path('/opt/flash-ticket-app')
names=subprocess.check_output(['sudo','-n','docker','ps','--format','{{.Names}}'],text=True).splitlines()
for n in names:
 if any(x in n for x in ['payment-service','keycloak','api-gateway']):
  d=json.loads(subprocess.check_output(['sudo','-n','docker','inspect',n],text=True))[0]
  e=dict(x.split('=',1) for x in d['Config']['Env'] if '=' in x)
  safe={k:v for k,v in e.items() if k in ['SERVER_PORT','VNPAY_URL','VNPAY_API_URL','VNPAY_RETURN_URL','VNPAY_IPN_URL','KC_HOSTNAME','KEYCLOAK_ISSUER_URI']}
  print(json.dumps({'container':n,'image':d['Config']['Image'],'safeEnv':safe,'vnpayKeys':[k for k in e if k.startswith('VNPAY_')],'labels':d['Config']['Labels'],'networks':list(d['NetworkSettings']['Networks'])}))
for p in [root/'env/test-users.json',root/'env/keycloak.env',root/'env-t062/payment-service.env',root/'compose-t062/payment-service.yml']:
 if p.exists():
  b=p.read_bytes(); print(json.dumps({'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}))
  if p.name=='test-users.json':
   print(json.dumps({'testUsers':[{'username':u['username'],'roles':u.get('realmRoles',[])} for u in json.loads(b)]}))
  elif p.suffix=='.yml': print(p.read_text())
  else: print(json.dumps({'envKeys':[l.split('=',1)[0] for l in b.decode().splitlines() if l and not l.startswith('#')]}))
PY
