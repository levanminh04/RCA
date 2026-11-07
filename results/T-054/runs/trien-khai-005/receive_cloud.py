from inventory import *
from cloud_dev import TARGET,MAIN
import sys,shlex,tarfile,io,hashlib
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(ROOT/'results/T-054/runs/trien-khai-003')]
from bien_nhan import *
from cham import snapshot_from_status,verify_snapshot
from dieu_phoi import verify_attempt
from pilot import reference,comparable
from doi_chieu_pilot import differences

code="""import pathlib,json,sys,tarfile,io,hashlib
r=pathlib.Path(TARGET);sys.path.insert(0,str(r/'results/T-054/scripts'))
from dieu_phoi import status
from bien_nhan import fingerprint
from cham import snapshot_from_status
p=json.loads((r/'results/T-054/cloud-plan.json').read_bytes());s=status(r/'results/T-054/queue')
assert s['controller']is None and all(v['state']=='VERIFIED'for v in s['jobs'].values())
snap=snapshot_from_status(p,s)
files=[x for x in (r/'results/T-054').rglob('*')if x.is_file()]+[r/'dev-metadata.json',r/'package-files.json']
manifest={x.relative_to(r).as_posix():{'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()}for x in files}
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|gz')as t:
 for x in files:t.add(x,arcname=x.relative_to(r).as_posix(),recursive=False)
 for name,obj in [('transfer-manifest.json',manifest),('snapshot.json',snap)]:
  b=json.dumps(obj).encode();m=tarfile.TarInfo(name);m.size=len(b);t.addfile(m,io.BytesIO(b))
""".replace('TARGET',repr(TARGET))
r=subprocess.run(ssh_args(HOSTS[1])+['python3 -c '+shlex.quote(code)],capture_output=True,timeout=30)
assert r.returncode==0,r.stderr
(RUN/'received-cloud-001.tar.gz').write_bytes(r.stdout)
dest=RUN/'received-cloud-001';dest.mkdir(exist_ok=False)
with tarfile.open(fileobj=io.BytesIO(r.stdout))as t:
 for m in t.getmembers():assert m.isfile()and not m.name.startswith('/')and'..'not in Path(m.name).parts
 t.extractall(dest,filter='data')
manifest=json.loads((dest/'transfer-manifest.json').read_bytes())
for rel,pin in manifest.items():
 p=dest/rel;assert p.stat().st_size==pin['bytes']and digest(p)==pin['sha256']
receive_paths({TARGET:str(dest)})
plan=read_pin(ref(dest/'results/T-054/cloud-plan.json'));snapshot=read_pin(ref(dest/'snapshot.json'))
verified=verify_snapshot(snapshot,plan['jobs']);record,=next(iter(verified.values()));assert record['status']=='OK'
meta=json.loads((dest/'dev-metadata.json').read_bytes());native=reference(meta['reference']['native_record'],'K-E1+E2+E5')
left,right=comparable(native),comparable(record);diff=differences(left,right)
attempt=next((dest/'results/T-054/queue').glob('*/attempt-001'))
cost=read_pin(ref(attempt/'cost.json'));monitors=events(attempt/'monitor.jsonl')
summary={'transfer_files_verified':len(manifest),'received_archive':ref(RUN/'received-cloud-001.tar.gz'),
 'status':record['status'],'exact_native_same_EC2':left==right,'differences':diff,
 'native':meta['reference'],'elapsed_s':cost['wall_s'],'peak_tree_rss':max(x['peak_tree_rss']for x in monitors),
 'max_monitor_gap_s':max(x['max_monitor_gap_s']for x in monitors),'ssh_detached_completed':True,
 'labels_read':False,'test_opened':False,'main_started':False}
atomic(RUN/'cloud-dev-summary.json',summary)
print(json.dumps(summary,ensure_ascii=False))
