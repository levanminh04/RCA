"""Export completed EC2 chain, recheck V1 and preserve every primary run."""
import hashlib
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path

B=Path.home()/'rca/T-029'
DATA=Path.home()/'rca/T-031/repo'
SOURCE=Path.home()/'rca/T-025/repo'
E=B/'export-complete-002'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def put(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''): h.update(block)
    return h.hexdigest()
def status(s):
    with (B/'trang-thai.txt').open('a',encoding='utf-8') as f:
        f.write(datetime.now(timezone.utc).isoformat()+' EXPORT002 '+s+'\n')

assert read(B/'runs/chuoi-002/ket-thuc.json')['status']=='PASS'
assert read(B/'runs/chuoi-002/v4-check.json')['status']=='PASS'
E.mkdir(exist_ok=False)
checks=[]
for case in read(B/'inputs/allowlist-dev.json')['cases']:
    for name,meta in case['files'].items():
        if meta is None: continue
        path=(DATA/meta['path']).resolve(); assert DATA in path.parents
        checks.append({'opaque_id':case['opaque_id'],'file':name,'sha256':sha(path),'expected':meta['sha256']})
before=read(B/'runs/chuoi-002/guard.json')['remote_src_p3']['tep']
after={'src/'+p.relative_to(SOURCE/'src').as_posix():sha(p) for p in sorted((SOURCE/'src/p3').rglob('*.py'))}
passed=all(x['sha256']==x['expected'] for x in checks) and after==before and len(checks)==89
put(E/'final-v1.json',{'status':'PASS' if passed else 'FAIL','file_count':len(checks),'data_checks':checks,
                      'src_p3_final':after,'src_p3_matches_start':after==before})
if not passed:
    status('DUNG V1 final mismatch; no archive')
    raise RuntimeError('V1 final mismatch')
status('V1 FINAL PASS 30ca 89tep; export BAT_DAU')
files=sorted(p for name in ('inputs','scripts','runs') for p in (B/name).rglob('*') if p.is_file())
files += [p for p in sorted(B.glob('STOP*')) if p.is_file()]
files += [B/'trang-thai.txt',E/'final-v1.json']
for p in files: assert not p.is_symlink() and B in p.resolve().parents
manifest={'task':'T-029','status':'COMPLETED_CHAIN_002','time':datetime.now(timezone.utc).isoformat(),
          'files':{p.relative_to(B).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in files},
          'file_count':len(files),'excluded':['tmp','cache','tmux socket','previous export copies; primary runs retained']}
mp=E/'transfer-manifest.json'; put(mp,manifest)
archive=E/'artifacts.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for p in files: tar.add(p,arcname=p.relative_to(B).as_posix(),recursive=False)
    tar.add(mp,arcname='transfer-manifest.json',recursive=False)
result={'file_count':len(files),'archive_members':len(files)+1,'archive_sha256':sha(archive),
        'manifest_sha256':sha(mp),'archive_bytes':archive.stat().st_size}
put(E/'export-check.json',result)
print(json.dumps(result))
# No append to trang-thai after hashing it: exported snapshot must remain immutable.
