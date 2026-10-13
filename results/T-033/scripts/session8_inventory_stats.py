"""Read-only inventory for streaming verified extraction, without archive."""
import pathlib,json,hashlib,subprocess
H=pathlib.Path('/home/ubuntu/rca/T-033')
ps=subprocess.check_output(['ps','-eo','pid,args'],text=True).splitlines()
workers=[s for s in ps if str(H) in s and any(v in s for v in ['accounted_worker.py','/job.sh','extract_v2.py'])]
assert not workers,workers
files={}
for n in ['session8-stats-001']:
 for p in (H/'runs'/n).iterdir():
  assert p.is_file();h=hashlib.sha256()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1<<20),b''):h.update(b)
  files[p.relative_to(H).as_posix()]={'sha256':h.hexdigest(),'bytes':p.stat().st_size}
print(json.dumps({'status':'PASS','files':files,'worker_candidates':workers,'logical_bytes':sum(p.stat().st_size for p in H.rglob('*') if p.is_file())}))
