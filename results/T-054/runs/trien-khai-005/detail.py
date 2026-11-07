from inventory import *
SCRIPT=r'''
import json,subprocess,os
from pathlib import Path
out={}
for path in ['/home/ubuntu/rca/envs','/home/ubuntu/rca/data','/home/ubuntu/rca/T-032','/home/ubuntu/rca/T-033','/home/ubuntu/rca-t048']:
 if Path(path).exists():
  r=subprocess.run(['du','-x','-B1','--max-depth=2',path],capture_output=True,text=True,timeout=60);out[path]=r.stdout
out['source_examples']={}
for base in ['/home/ubuntu/rca/data','/home/ubuntu/rca/T-032','/home/ubuntu/rca-t053']:
 if Path(base).exists():
  out['source_examples'][base]=[str(p)for p in Path(base).rglob('metrics.parquet')][:100]
exe='/home/ubuntu/rca/T-025/envs/main/bin/python'
code="import sys,json,importlib.metadata as m; print(json.dumps({'python':sys.version,'exe':sys.executable,'packages':{n:m.version(n) for n in ['numpy','pandas','scipy','networkx','scikit-learn','psutil','pyarrow','drain3','causal-learn']}}))"
r=subprocess.run([exe,'-B','-c',code],capture_output=True,text=True);out['main_environment']={'exit':r.returncode,'out':r.stdout,'err':r.stderr}
out['reuse_wrappers']={}
for base in ['/home/ubuntu/rca/T-032','/home/ubuntu/rca-t053']:
 if Path(base).exists():out['reuse_wrappers'][base]=[str(p) for p in Path(base).rglob('*.py') if any(w in p.name for w in ['controller','receive','pilot','resume'])][:50]
print(json.dumps(out))
'''
def detail(h):
 r=subprocess.run(ssh_args(h)+['python3 -'],input=SCRIPT,text=True,encoding='utf-8',capture_output=True,timeout=110)
 (RUN/(h['name']+'-detail.json')).write_text(json.dumps({'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr},indent=2),encoding='utf-8')
 print(h['name'],r.returncode,flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as p:list(p.map(detail,HOSTS))
