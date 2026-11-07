"""Một lượt M1 dev trên EC2_2; tái dùng code/env, không test/nhãn."""
from inventory import *
import sys,tarfile,shlex,copy
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(ROOT/'src')]
from bien_nhan import ref,read_pin,fingerprint,canonical
from nguon import original_dev_sources
from pilot import reference
TARGET='/home/ubuntu/rca-p7/T-054/cloud-dev-001'
MAIN='/home/ubuntu/rca/T-025/envs/main/bin/python'

def stage(h):
    tarpath=RUN/'cloud-dev-001.tar.gz';sha=hashlib.sha256(tarpath.read_bytes()).hexdigest()
    program="""import pathlib,sys,tarfile,hashlib,json
r=pathlib.Path(TARGET);r.mkdir(parents=True,exist_ok=False)
p=r/'package.tar.gz';p.write_bytes(sys.stdin.buffer.read());assert hashlib.sha256(p.read_bytes()).hexdigest()==SHA
with tarfile.open(p)as t:
 for m in t.getmembers():
  assert m.isfile() and not m.name.startswith('/') and '..'not in pathlib.PurePosixPath(m.name).parts
 t.extractall(r,filter='data')
items=json.loads((r/'package-files.json').read_bytes())
for relative,pin in items.items():
 p=r/relative;assert p.stat().st_size==pin['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==pin['sha256']
print(json.dumps({'verified_files':len(items),'root':str(r)}))
""".replace('TARGET',repr(TARGET)).replace('SHA',repr(sha))
    tick=time.monotonic();r=subprocess.run(ssh_args(h)+['python3 -c '+shlex.quote(program)],input=tarpath.read_bytes(),capture_output=True,timeout=90)
    result={'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'elapsed_s':time.monotonic()-tick,'bytes':tarpath.stat().st_size}
    (RUN/(h['name']+'-stage.json')).write_text(json.dumps(result),encoding='utf-8');assert r.returncode==0,result

def build():
    old=read_pin(ref(ROOT/'results/T-054/runs/trien-khai-003/pilot-local-007/plan.json'))
    job=copy.deepcopy(next(j for j in old['jobs']if j['slot']['dataset']=='RE2-TT'and j['slot']['arm']=='M1'))
    oid='dev-a915aa2424'
    candidate=next(c for c in read_pin(ref(ROOT/'results/T-054/pilot-plan.json'))['candidates']if c['opaque_id']==oid and c['window']=='that')
    desc=read_pin(job['independent_source_ref']);desc.update(selected_ids=[oid],command_refs={oid:candidate['native_command_pin']})
    authoritative=original_dev_sources(desc);row=next(iter(authoritative['cases_by_member'].values()))
    job.update(source=row,t=row['t'],data_root=TARGET,pythonpath=[],code_pins={},a4=False)
    job['slot'].update(opaque_id=oid,member_sha256=row['member_sha256'],source_sha256=fingerprint(row),window={'t':row['t'],'half_width_s':300})
    keys=set(read_pin(ref(ROOT/'results/T-054/runs/freeze-cong-cu-006/files.json'))['files'])
    keys.update(row['files'][name]['path']for name in row['files'])
    files={rel:ref(ROOT/rel)for rel in keys}
    metadata={'job':job,'source':authoritative,'reference':candidate,'scope':'selected DEV only; no labels/test; compare same EC2 native'}
    (RUN/'dev-metadata.json').write_bytes(canonical(metadata))
    with tarfile.open(RUN/'cloud-dev-001.tar.gz','w:gz')as t:
        for rel in sorted(keys):t.add(ROOT/rel,arcname=rel,recursive=False)
        for name,value in [('dev-metadata.json',metadata),('package-files.json',files)]:
            import io
            b=canonical(value);m=tarfile.TarInfo(name);m.size=len(b);t.addfile(m,io.BytesIO(b))
    print('archive', (RUN/'cloud-dev-001.tar.gz').stat().st_size,flush=True)

def launch_dev(host=HOSTS[1]):
    code="""import sys,pathlib,json,os,subprocess
r=pathlib.Path(TARGET);sys.path[:0]=[str(r/'results/T-054/scripts'),str(r/'src')]
for k in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[k]='1'
os.environ['PYTHONHASHSEED']='0';os.environ['PYTHONDONTWRITEBYTECODE']='1'
from bien_nhan import *
from lap_ho_so import stable_environment
meta=json.loads((r/'dev-metadata.json').read_bytes());j=meta['job'];environment=stable_environment()
atomic(r/'results/T-054/cloud-environment.json',environment)
j['slot']['environment_sha256']=fingerprint(environment);j['executable']=sys.executable
j['code_pins']={k:v['sha256'] for k,v in json.loads((r/'package-files.json').read_bytes()).items()if k.endswith('.py')}
runtime={'dataset':'RE2-TT','g1_revision':j['g1_revision'],'inventory':j['inventory'],'cases':{j['slot']['opaque_id']:j['source']}}
j['runtime_ref']=atomic(r/'results/T-054/dev-runtime.json',runtime)
j['independent_source_ref']=atomic(r/'results/T-054/dev-original-source.json',meta['source'])
for key in ['m1_contract','static_snapshot']:
 old=pathlib.PureWindowsPath(j[key]['path']).as_posix();suffix=old.split('/RCA-flashticket/',1)[1] if '/RCA-flashticket/'in old else old
 j[key]=ref(r/suffix)
p={'schema':'T054-PLAN-1','mode':'dev','host_role':HOST_ROLE,'workers':1,'directory':str(r/'results/T-054/queue'),
 'jobs':[j],'monitor':{'poll_s':.2,'max_monitor_gap_s':5,'score_phases':[]},'budget':{'wall_s':1200,'method_dataset_s':{'RE2-TT|M1':900}},'open_before_run':[]}
plan=atomic(r/'results/T-054/cloud-plan.json',p)
source=r/'results/T-054/cloud-authorization-source.txt';source.write_text('Minh authorizes SSH and one short targeted DEV cloud route; stop before main, 2026-11-05')
auth=atomic(r/'results/T-054/cloud-authority.json',{'pilot_grant':True,'source':ref(source),'plan_sha256':fingerprint(p),'g3':False,'test_grant':False})
result=subprocess.run([sys.executable,'-B',str(r/'results/T-054/scripts/p7.py'),'run','--plan',plan['path'],'--sha256',plan['sha256'],'--authority',auth['path'],'--authority-sha256',auth['sha256']],capture_output=True,text=True)
print(json.dumps({'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr}));assert result.returncode==0
""".replace('TARGET',repr(TARGET)).replace('HOST_ROLE',repr(host['name']))
    r=subprocess.run(ssh_args(host)+[MAIN+' -B -c '+shlex.quote(code)],capture_output=True,text=True,timeout=30)
    (RUN/(host['name']+'-cloud-launch.json')).write_text(json.dumps({'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}),encoding='utf-8')
    print(r.stdout,r.stderr);assert r.returncode==0
if __name__=='__main__':
    build()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as p:list(p.map(stage,HOSTS))
    launch_dev()
