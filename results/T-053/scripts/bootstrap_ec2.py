
import gzip,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT/n) for n in ('src','results/T-047/scripts','results/T-045/scripts')]
import pha2_t047 as old
from m1_danh_gia.pha2 import giai_ma_json,ma_hoa_json
folder=ROOT/'results/T-053/runs/bootstrap-ec2-001'
data=giai_ma_json(json.loads((folder/'input.json').read_bytes()))
start=time.monotonic()
with (folder/'progress.jsonl').open('x',encoding='utf-8') as progress, gzip.open(folder/'samples.jsonl.gz','xt',encoding='utf-8',compresslevel=3) as samples:
 def event(**value):
  progress.write(json.dumps(dict(value,elapsed=time.monotonic()-start))+chr(10));progress.flush()
 def sample(value):
  samples.write(json.dumps(ma_hoa_json(value),ensure_ascii=False)+chr(10));samples.flush()
 result=old.bootstrap(data['kq'],data['ce'],{k:set(v) for k,v in data['E_X'].items()},event,sample)
for key,value in result['mau_goc'].items():
 assert value==data['main'][key],key
result['remote_seconds']=time.monotonic()-start
with (folder/'do-ben.json').open('x',encoding='utf-8') as f:json.dump(ma_hoa_json(result),f,ensure_ascii=False)
hashes={}
for p in folder.iterdir():
 if p.is_file():
  hashes[p.name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
with (folder/'closed.json').open('x',encoding='utf-8') as f:json.dump({'files':hashes,'complete':True,'n':1000},f,indent=2)
print('BOOTSTRAP PASS',result['remote_seconds'],flush=True)
