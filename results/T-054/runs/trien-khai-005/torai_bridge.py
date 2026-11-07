"""Dùng CSV DEV đã có để kiểm parser/API py38 Linux, không chạy lại TORAI."""
from inventory import *
import sys,io,tarfile,shlex
sys.path.insert(0,str(ROOT/'results/T-054/scripts'))
from bien_nhan import *
from dieu_phoi import status
p=read_pin(ref(ROOT/'results/T-054/runs/trien-khai-003/pilot-local-007/plan.json'))
j=next(j for j in p['jobs']if j['slot']['arm']=='torai_B'and j['slot']['dataset']=='RE2-TT'and j['slot']['seed']==0)
st=status(ROOT/'results/T-054/runs/trien-khai-003/pilot-local-007/queue');a=Path(st['jobs'][fingerprint(j['slot'])]['attempt'])
inv=read_pin(ref(a/'invocation.json'));prep=read_pin(inv['prepared_ref'])
buf=io.BytesIO()
with tarfile.open(fileobj=buf,mode='w:gz')as t:
 for name,pin in prep['tables'].items():
  path=Path(pin['path']);assert digest(path)==pin['sha256'];t.add(path,arcname=name+'.csv',recursive=False)
target='/home/ubuntu/rca-p7/T-054/transport-final-005/torai-parser-bridge'
def go(h):
 code="""import pathlib,tarfile,io,sys,json,subprocess,os
r=pathlib.Path(TARGET);r.mkdir(exist_ok=False)
with tarfile.open(fileobj=io.BytesIO(sys.stdin.buffer.read()))as t:
 for m in t.getmembers():assert m.isfile()and m.name in ['metric.csv','logts.csv','tracets_err.csv','tracets_lat.csv']
 t.extractall(r,filter='data')
code=INNER
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONHASHSEED='0',PYTHONDONTWRITEBYTECODE='1')
p=subprocess.run(['/home/ubuntu/rca/T-025/envs/py38/bin/python','-B','-c',code],capture_output=True,text=True,env=env)
print(json.dumps({'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}));assert p.returncode==0
"""
 inner="import sys,json,pandas as pd;from pathlib import Path;sys.path.insert(0,'/home/ubuntu/rca-p7/T-054/transport-final-005/results/T-054/scripts');from bien_nhan import normalized_digest;r=Path("+repr(target)+");args=[pd.read_csv(r/(k+'.csv'))for k in ['metric','logts','tracets_err','tracets_lat']]+["+repr(j['t'])+",0];actual=normalized_digest(args);print(json.dumps({'normalized_input_exact':actual=="+repr(inv['normalized_input_sha256'])+",'actual':actual,'method_rerun':False}));assert actual=="+repr(inv['normalized_input_sha256'])
 code=code.replace('TARGET',repr(target)).replace('INNER',repr(inner))
 q=subprocess.run(ssh_args(h)+['python3 -c '+shlex.quote(code)],input=buf.getvalue(),capture_output=True,timeout=25)
 (RUN/(h['name']+'-torai-bridge.json')).write_text(json.dumps({'exit':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode(),'reference':ref(a/'invocation.json')}),encoding='utf-8')
 print(h['name'],q.returncode,q.stdout.decode(),q.stderr.decode())
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:list(pool.map(go,HOSTS))
