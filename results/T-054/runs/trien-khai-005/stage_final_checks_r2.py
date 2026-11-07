from inventory import *
import sys,tarfile,shlex
sys.path.insert(0,str(ROOT/'results/T-054/scripts'))
from bien_nhan import ref,read_pin,canonical
keys=set(read_pin(ref(ROOT/'results/T-054/runs/freeze-cong-cu-006/files.json'))['files'])
keys.add('results/T-054/runs/trien-khai-005/cloud_checks.py')
archive=RUN/'final-cloud-code-r2.tar.gz'
with tarfile.open(archive,'w:gz')as t:
 for rel in sorted(keys):t.add(ROOT/rel,arcname=rel,recursive=False)
pins={rel:ref(ROOT/rel)for rel in keys};(RUN/'final-cloud-code-files-r2.json').write_bytes(canonical(pins))
target='/home/ubuntu/rca-p7/T-054/transport-final-005-r2'
def check(h):
 code="""import pathlib,tarfile,sys,hashlib,subprocess,json,os
r=pathlib.Path(TARGET);r.mkdir(parents=True,exist_ok=False)
p=r/'code.tar.gz';p.write_bytes(sys.stdin.buffer.read());assert hashlib.sha256(p.read_bytes()).hexdigest()==SHA
with tarfile.open(p)as t:
 for m in t.getmembers():assert m.isfile()and not m.name.startswith('/')and'..'not in pathlib.PurePosixPath(m.name).parts
 t.extractall(r,filter='data')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONHASHSEED='0')
q=subprocess.run(['/home/ubuntu/rca/T-025/envs/main/bin/python','-B',str(r/'results/T-054/runs/trien-khai-005/cloud_checks.py')],capture_output=True,text=True,env=env,timeout=60)
summary=r/'results/T-054/runs/cloud-checks-005/summary.json'
print(json.dumps({'exit':q.returncode,'out':q.stdout,'err':q.stderr,'summary':json.loads(summary.read_bytes())if summary.exists()else None}));assert q.returncode==0
""".replace('TARGET',repr(target)).replace('SHA',repr(hashlib.sha256(archive.read_bytes()).hexdigest()))
 q=subprocess.run(ssh_args(h)+['python3 -c '+shlex.quote(code)],input=archive.read_bytes(),capture_output=True,timeout=90)
 result={'exit':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()}
 (RUN/(h['name']+'-final-checks-r2.json')).write_text(json.dumps(result),encoding='utf-8')
 print(h['name'],result,flush=True);assert q.returncode==0
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:list(pool.map(check,HOSTS))
