import base64,datetime,hashlib,json,pathlib,subprocess,urllib.request
B=pathlib.Path('/opt/flash-ticket-obs/pinned')
C='flash-ticket-obs-grafana'
T=[{"name":"t065-l8b-rca.json","path":"/opt/flash-ticket-obs/pinned/provisioning/dashboards/RCA FlashTicket/1 · Kết quả hiện hành/t065-l8b-rca.json","uid":"t065-l8b-rca","expected":{"sha256":"e0145eafbdbd9ada8386dc91e5abe97ce761c7b33197e9a180231e8fcb078d93","bytes":36292}},{"name":"t065-l8b-phat-lai.json","path":"/opt/flash-ticket-obs/pinned/provisioning/dashboards/RCA FlashTicket/1 · Kết quả hiện hành/t065-l8b-phat-lai.json","uid":"t065-l8b-phat-lai","expected":{"sha256":"a73be77effc35356706e77177b44285d6ea923ccaafcb801ef95d7e51f9aada7","bytes":16069}}]
def digest(b): return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
stop=pathlib.Path('/home/ubuntu/rca-dieu-phoi/STOP')
assert not stop.exists(),'STOP remote'
ins=json.loads(subprocess.check_output(['docker','inspect',C]))[0]
env=dict(s.split('=',1) for s in ins['Config']['Env'] if '=' in s)
auth=base64.b64encode((env.get('GF_SECURITY_ADMIN_USER','admin')+':'+env['GF_SECURITY_ADMIN_PASSWORD']).encode()).decode()
def api(uid):
 req=urllib.request.Request('http://10.0.0.215:3000/api/dashboards/uid/'+uid,headers={'Authorization':'Basic '+auth})
 with urllib.request.urlopen(req,timeout=20) as res: return {'http':res.status,'data':json.load(res)}
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stop':False,'files':{},'targets':{},'machine':{'started_at':ins['State']['StartedAt'],'restart_count':ins['RestartCount'],'status':ins['State']['Status']}}
for p in [B/'compose.json',*sorted((B/'provisioning').rglob('*'))]:
 if p.is_file(): result['files'][str(p)]=digest(p.read_bytes())
for t in T:
 p=pathlib.Path(t['path'])
 assert p.is_relative_to(B/'provisioning/dashboards') and not p.is_symlink()
 b=p.read_bytes()
 assert digest(b)==t['expected'],('L11b pin',t['name'])
 d=json.loads(b); a=api(t['uid'])
 fields=['uid','title','panels','templating','time','links','tags']
 for k in fields: assert a['data']['dashboard'].get(k)==d.get(k),('GET/file',t['name'],k)
 projection={k:a['data']['dashboard'].get(k) for k in fields}
 result['targets'][t['name']]={'path':str(p),**digest(b),'before_base64':base64.b64encode(b).decode(),'api':a,'get_source_projection':digest(json.dumps(projection,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),'get_compared_fields':fields,'get_matches_file':True}
print(json.dumps(result,ensure_ascii=False))
