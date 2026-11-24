sudo -n python3 - <<'PY'
import json,urllib.request,base64
env={}
for l in open('/etc/flashticket-rca/grafana.env'):
    k,_,v=l.strip().partition('='); env[k]=v.strip().strip('"').strip("'")
auth='Basic '+base64.b64encode((env.get('GF_SECURITY_ADMIN_USER','admin')+':'+env['GF_SECURITY_ADMIN_PASSWORD']).encode()).decode()
def req(p,m='GET'):
    with urllib.request.urlopen(urllib.request.Request('http://10.0.0.215:3000'+p,method=m,headers={'Authorization':auth}),timeout=20) as r: return r.status, json.load(r)
rules=req('/api/v1/provisioning/alert-rules')[1]
for uid in ['cg51evuk4md4wb','ag51evv3jtxxcf']:
    nl=sum(1 for r in rules if r['folderUID']==uid); nd=len(req('/api/search?folderUIDs='+uid)[1])
    if nl==0 and nd==0: print(uid, req('/api/folders/'+uid,'DELETE'))
    else: print('GIU',uid,nl,nd)
print([(f['uid'],f['title']) for f in req('/api/folders')[1]])
print('so luat', len(req('/api/v1/provisioning/alert-rules')[1]), 'dashboard', len(req('/api/search?type=dash-db')[1]))
PY
