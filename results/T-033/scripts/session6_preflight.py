"""Read-only EC2 process/source/hash check; stdout retained by laptop controller."""
import pathlib,json,hashlib,subprocess,os,platform,sys,time,shutil
import numpy,pandas,scipy,psutil
H=pathlib.Path('/home/ubuntu/rca/T-033'); t=time.perf_counter()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(p.read_text())
source_sha='3071381a24edcfe82c1df19ffe4b816b2356a3afad1117fdae260f6c04f9079c'
assert sha(H/'inputs/source.json')==source_sha
S=read(H/'inputs/source.json'); I=read(H/'runs/preflight-002/inventory.json')
ps=subprocess.check_output(['ps','-eo','pid,args'],text=True).splitlines()
workers=[s for s in ps if str(H) in s and any(x in s for x in ['delay.py','context.py','factorial.py','frozen.py','_job','session6_job','accounted_worker'])]
assert not workers,workers
assert not (H/'STOP').exists()
raw=[]
for item in S['cases']:
 row=next(r for r in I['cases'] if r['opaque_id']==item['opaque_id'])
 for n,m in item['files'].items():
  p=pathlib.Path(row['files'][n]); assert str(p)==str(pathlib.Path(S['source_roots_remote'][0])/m['path'])
  assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256']
  raw.append({'path':str(p),'sha256':m['sha256'],'bytes':m['bytes']})
native={}
for n,v in S['native_hash'].items():
 p=pathlib.Path('/home/ubuntu/rca/T-025/src/baro/baro')/n; assert sha(p)==v
 native[n]={'sha256':v,'bytes':p.stat().st_size}
p=pathlib.Path('/home/ubuntu/rca/T-025/repo/src/p3/adapters/phat_hien.py');assert sha(p)==S['adapter_sha256']
native[p.name]={'sha256':sha(p),'bytes':p.stat().st_size}
assert (numpy.__version__,pandas.__version__,scipy.__version__,psutil.__version__)==('1.26.4','2.2.3','1.14.1','6.1.1')
assert sys.version.startswith('3.12.3') and platform.machine()=='x86_64'
print(json.dumps({'status':'PASS','source_sha256':source_sha,'worker_candidates':workers,'archive_exists':(H/'runs/checkpoint-handoff-001/artifacts.tar').exists(),'raw':raw,'native':native,'environment':{'python':sys.version,'platform':platform.platform(),'numpy':numpy.__version__,'pandas':pandas.__version__,'scipy':scipy.__version__,'psutil':psutil.__version__},'logical_bytes':sum(p.stat().st_size for p in H.rglob('*') if p.is_file()),'disk_free_bytes':shutil.disk_usage(H).free,'ram_available_bytes':psutil.virtual_memory().available,'tmux':subprocess.run(['tmux','-S',str(H/'tmux.sock'),'list-sessions'],capture_output=True,text=True).stdout,'tail':(H/'trang-thai.txt').read_text().splitlines()[-20:],'body_wall_s':time.perf_counter()-t},indent=2))
