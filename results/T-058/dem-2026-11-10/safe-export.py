"""Operator export checks. No plaintext credential is printed or exported."""
import datetime,hashlib,json,os,re,sys,tarfile
from pathlib import Path
ROOT=Path('/home/ubuntu/t058')

def app_secrets():
 values=set()
 paths=list(Path('/opt/flash-ticket-app/env').glob('*.env'))+[Path('/opt/flash-ticket-src/.env'),Path('/opt/flash-ticket-app/collector/collector.env')]
 for path in paths:
  for line in path.read_text().splitlines():
   if '=' not in line: continue
   k,v=line.split('=',1)
   if any(word in k for word in ['PASSWORD','SECRET','TOKEN','API_KEY']) and not k.endswith(('_URI','_URL')) and len(v)>=16: values.add(v)
 for name in ['test-users.json','client-secrets.json']:
  obj=json.loads((Path('/opt/flash-ticket-app/env')/name).read_text())
  values.update(u['password'] for u in obj) if isinstance(obj,list) else values.update(obj.values())
 values.update(json.loads(Path('/opt/flash-ticket-app/secrets/ticket-qr/key-ring.json').read_text())['keys'].values())
 return values

def strings(value):
 if isinstance(value,str): yield value
 elif isinstance(value,dict):
  for k,v in value.items(): yield str(k); yield from strings(v)
 elif isinstance(value,list):
  for v in value: yield from strings(v)

mode=sys.argv[1]
if mode=='catalog':
 secrets=app_secrets()
 catalog={}
 for v in secrets: catalog.setdefault(str(len(v)),[]).append(hashlib.sha256(v.encode()).hexdigest())
 path=ROOT/'credential-hash-catalog.json'
 path.write_text(json.dumps(catalog)+'\n'); path.chmod(0o600)
 print('Wrote hash-only catalog; no credential values exported; entries',len(secrets))
elif mode in ['app-config','obs-config']:
 role=mode.split('-')[0]
 if role=='app':
  base=Path('/opt/flash-ticket-app')
  paths=sorted((base/'compose').glob('*.yml'))+sorted((base/'compose-exp').glob('*.yml'))+[base/'collector/config.json',base/'collector/compose.json']
  secrets=app_secrets()
 else:
  base=Path('/opt/flash-ticket-obs/pinned')
  paths=sorted(base.glob('*.json'))+sorted((base/'provisioning').rglob('*.yaml'))
  secrets={line.split('=',1)[1] for line in Path('/opt/flash-ticket-obs/grafana.env').read_text().splitlines() if line.startswith('GF_SECURITY_ADMIN_PASSWORD=')}
 for path in paths:
  body=path.read_text()
  if any(v and v in body for v in secrets): raise SystemExit('Credential match in selected config; export refused: '+str(path))
 archive=ROOT/('public-'+role+'-config.tgz')
 with tarfile.open(archive,'w:gz') as stream:
  for path in paths: stream.add(path,arcname=role+'/'+str(path.relative_to(base)))
 archive.chmod(0o644)
 report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Explicit public config allowlist; exact provisioned credential scan',
         'files':[str(p) for p in paths],'credential_matches':0,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
 target=ROOT/('public-'+role+'-config-audit.json');target.write_text(json.dumps(report,indent=2)+'\n');target.chmod(0o644)
 print('Public config allowlist exported; files',len(paths),'credential matches 0')
elif mode=='case':
 opaque=sys.argv[2]
 if not opaque.isalnum(): raise SystemExit('Bad case ID')
 base=Path('/opt/flash-ticket-rca')
 if not (base/'cases'/opaque/'manifest.json').is_file() or not (base/'outputs'/opaque/'summary.json').is_file():
  raise SystemExit('Both frozen input manifest and completed output summary are required')
 catalog=json.loads((ROOT/'credential-hash-catalog.json').read_text())
 catalog={int(k):set(v) for k,v in catalog.items()}
 pattern=re.compile(r'[A-Za-z0-9+/=_-]{'+str(min(catalog))+r',}')
 jwt=re.compile(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+')
 paths=sorted((base/'cases'/opaque).glob('*.json*'))+sorted((base/'outputs'/opaque).glob('*.json'))
 hits=[]; checked=0
 for path in paths:
  with path.open() as stream:
   documents=(json.loads(line) for line in stream if line.endswith('\n')) if path.suffix=='.jsonl' else [json.load(stream)]
   for doc in documents:
    for value in strings(doc):
     checked+=1
     if jwt.search(value): hits.append({'file':str(path),'kind':'JWT-shaped value'}); break
     found=False
     for match in pattern.finditer(value):
      token=match[0]
      for length,hashes in catalog.items():
       for offset in range(len(token)-length+1):
        if hashlib.sha256(token[offset:offset+length].encode()).hexdigest() in hashes:
         found=True; break
       if found: break
      if found: break
     if found: hits.append({'file':str(path),'kind':'provisioned credential hash match'}); break
 report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'opaque_id':opaque,'files_checked':len(paths),'strings_checked':checked,
         'matches':hits,'passed':not hits,'scope':'Exact provisioned-credential candidate hash scan and JWT pattern; not a generic secret detector'}
 target=ROOT/('export-audit-'+opaque+'.json');target.write_text(json.dumps(report,indent=2)+'\n');target.chmod(0o644)
 print(json.dumps(report,indent=2))
 if hits: raise SystemExit('Case export refused')
else: raise SystemExit('Unknown mode')
