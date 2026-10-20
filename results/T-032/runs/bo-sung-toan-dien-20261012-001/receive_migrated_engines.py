"""Receive completed assigned T33 outputs from T32; immutable files only, no remote writes."""
from pathlib import Path
import datetime, hashlib, io, json, subprocess, sys, tarfile

P=Path(__file__).resolve().parent
D=P/'t32/t33-migration-001'
manifest=D/'migration-inputs-001/manifest.json'
cases=json.loads(manifest.read_text(encoding='utf-8'))['cases']
assert len(cases)==30
branches=['prior_df4','prior_kappa4','prior_precision4','causal_fixed','causal_expanding','compressed_row','compressed_calendar']
names=[]
for item in cases[14:]:
    oid=item['opaque_id']
    names += [(oid+'--full-sham-thread1.json','native')]
    names += [(oid+'--'+branch+'.json',branch) for branch in branches]
remote='/home/ubuntu/rca/T-032/runs/bo-sung-toan-dien-20261012-001/t32/t33-migration-001'
program='''import pathlib,json,hashlib,io,tarfile,sys,datetime
p=pathlib.Path(BASE); blobs={}; received={}; pending=[]; failed=[]
for name,branch in NAMES:
 f=p/name
 if not f.exists():pending.append(name);continue
 b=f.read_bytes()
 try:d=json.loads(b)
 except Exception as e:failed.append({'file':name,'reason':repr(e)});continue
 good=d.get('native_full_sham_exact') is True if branch=='native' else d.get('status')=='PASS'
 if not good:failed.append({'file':name,'reason':d.get('status','INVALID_GATE')});continue
 blobs[name]=b;received[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
r={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':received,'pending':pending,'failed':failed,'expected':128}
blobs['transfer-receipt.json']=json.dumps(r,indent=2).encode()
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|gz') as tar:
 for name,b in blobs.items():
  info=tarfile.TarInfo(name);info.size=len(b);tar.addfile(info,io.BytesIO(b))
'''.replace('BASE',repr(remote)).replace('NAMES',repr(names))
token=sys.argv[1]
archive=P/(token+'.tar.gz'); receipt_path=P/(token+'-receipt.json')
assert not archive.exists() and not receipt_path.exists()
r=subprocess.run(['ssh','-i','D:/RCA-ext/keys/key2.pem','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=20','ubuntu@3.26.62.217','python3 -B -'],input=program.encode(),capture_output=True)
with (P/(token+'-stderr.txt')).open('xb') as f:f.write(r.stderr)
if r.returncode:raise RuntimeError('Transfer failed; stderr retained, no output extracted')
with archive.open('xb') as f:f.write(r.stdout)
with tarfile.open(fileobj=io.BytesIO(r.stdout),mode='r:gz') as tar:
    members=tar.getmembers()
    assert all(m.isfile() and Path(m.name).name==m.name for m in members)
    assert len({m.name for m in members})==len(members)
    blobs={m.name:tar.extractfile(m).read() for m in members}
receipt=json.loads(blobs.pop('transfer-receipt.json'))
assert set(blobs)==set(receipt['files'])
assert set(blobs).issubset({n for n,_ in names})
for name,b in blobs.items():
    meta=receipt['files'][name]
    assert len(b)==meta['bytes'] and hashlib.sha256(b).hexdigest()==meta['sha256'],name
    target=D/name
    if target.exists():assert target.read_bytes()==b,'Existing local file differs: '+name
for name,b in blobs.items():
    target=D/name
    if not target.exists():
        with target.open('xb') as f:f.write(b)
receipt.update(archive_sha256=hashlib.sha256(r.stdout).hexdigest(),source_case_manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),local_verified=True)
with receipt_path.open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps({'files':len(blobs),'expected':128,'pending':len(receipt['pending']),'failed':receipt['failed'],'received_bytes':sum(len(b) for b in blobs.values()),'local_verified':True}))
