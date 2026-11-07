"""Chuyển allowlist TT opaque hai máy song song; không gọi method/đọc parquet."""
from pathlib import Path
import sys,json,tarfile,subprocess,shlex,concurrent.futures,time,io
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;OUT=ROOT/'results/T-054'
sys.path[:0]=[str(OUT/'scripts'),str(OUT/'runs/trien-khai-005')]
from bien_nhan import *
from inventory import HOSTS,ssh_args
REMOTE=r'''
import sys,tarfile,pathlib,json,hashlib,os,time,shutil
root=pathlib.Path(TARGET);stage=root.with_name('data-root.partial-006')
assert not root.exists() and not stage.exists(),'destination exists; do not overwrite'
assert root.is_absolute()and root.is_relative_to(pathlib.Path('/home/ubuntu/rca-p7/T-054'))
stage.mkdir(parents=True,exist_ok=False)
start=time.monotonic();manifest=None;actual={}
with tarfile.open(fileobj=sys.stdin.buffer,mode='r|')as t:
 for m in t:
  assert m.isfile()and not m.name.startswith('/')and'..'not in pathlib.PurePosixPath(m.name).parts
  if m.name=='transfer-manifest.json':
   assert manifest is None;manifest=json.load(t.extractfile(m));continue
  assert manifest is not None and m.name in manifest and m.name not in actual
  pin=manifest[m.name];assert m.size==pin['bytes']
  p=stage/m.name;assert p.resolve().is_relative_to(stage.resolve());p.parent.mkdir(parents=True,exist_ok=True)
  h=hashlib.sha256();size=0
  with t.extractfile(m)as f,p.open('xb')as out:
   while True:
    b=f.read(1024*1024)
    if not b:break
    out.write(b);h.update(b);size+=len(b)
   out.flush();os.fsync(out.fileno())
  assert size==pin['bytes']and h.hexdigest()==pin['sha256'],m.name
  actual[m.name]={'bytes':size,'sha256':h.hexdigest()}
assert set(actual)==set(manifest)and len(actual)==90
# Verify from disk again before making complete directory visible.
for rel,pin in actual.items():
 h=hashlib.sha256()
 with (stage/rel).open('rb')as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 assert h.hexdigest()==pin['sha256']
(stage/'transfer-manifest.json').write_text(json.dumps(actual))
stage.rename(root)
print(json.dumps({'PASS':True,'files':len(actual),'bytes':sum(p['bytes']for p in actual.values()),'destination':str(root),'elapsed_s':time.monotonic()-start,'free_bytes':shutil.disk_usage(root).free,'opaque_hash_only':True,'method_started':False,'files_verified':actual}))
'''
def run(host,rows):
    target=str(Path(rows[0]['destination']).as_posix()).split('/data/locked/')[0]
    man={r['path']:{k:r[k]for k in ['bytes','sha256']}for r in rows}
    for rel,pin in man.items():assert digest(ROOT/rel)==pin['sha256']and (ROOT/rel).stat().st_size==pin['bytes']
    code=REMOTE.replace('TARGET',repr(target));start=time.monotonic()
    p=subprocess.Popen(ssh_args(host)+['python3 -c '+shlex.quote(code)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        with tarfile.open(fileobj=p.stdin,mode='w|')as t:
            b=canonical(man);m=tarfile.TarInfo('transfer-manifest.json');m.size=len(b);t.addfile(m,io.BytesIO(b))
            for rel in sorted(man):t.add(ROOT/rel,arcname=rel,recursive=False)
        p.stdin.close();out=p.stdout.read();err=p.stderr.read();p.wait(timeout=90)
        result={'host':host['name'],'exit':p.returncode,'stdout':out.decode(),'stderr':err.decode(),'elapsed_s':time.monotonic()-start}
        pin=atomic(RUN/(host['name']+'-TT-transfer.json'),result)
        assert p.returncode==0,result['stderr']
        parsed=json.loads(result['stdout']);assert parsed['PASS']and parsed['files_verified']==man
        print(json.dumps({'host':host['name'],'files':parsed['files'],'bytes':parsed['bytes'],'elapsed_s':result['elapsed_s'],'receipt':pin}),flush=True)
        return pin
    except BaseException as e:
        if p.poll()is None:p.terminate()
        atomic(RUN/(host['name']+'-TT-transfer-failure.json'),{'type':type(e).__name__,'error':str(e),'elapsed_s':time.monotonic()-start});raise
if __name__=='__main__':
    plan=read_pin(ref(OUT/'runs/trien-khai-005/transfer-plan-005.json'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:receipts=list(pool.map(lambda h:run(h,plan['hosts'][h['name']]),HOSTS))
    atomic(RUN/'checkpoint-02-transfer.json',dict(PASS=True,host_receipts=receipts,files=180,bytes=1309388082,main_started=False,labels_transferred=False))
    with (ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md').open('ab')as f:f.write('\nCheckpoint phần2: hai EC2 nhận đủ90tệp TT/máy, tổng180tệp/1.309.388.082byte. Hash trước gửi, trong stream và đọc đĩa đích đều khớp; vùng partial chỉ rename sau đủ. Bản gốc giữ laptop, không labels/method. Nguồn: runs/chuan-bi-main-006/checkpoint-02-transfer.json và hai receipt.\n'.encode())
