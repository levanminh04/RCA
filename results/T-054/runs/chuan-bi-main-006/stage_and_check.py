"""Đặt code/plan candidate và kiểm metadata/nguồn/env, không phát supervisor/method."""
from pathlib import Path
import sys,json,subprocess,shlex,concurrent.futures,tarfile,io,time,hashlib,os
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;OUT=ROOT/'results/T-054'
sys.path[:0]=[str(OUT/'scripts'),str(OUT/'runs/trien-khai-005')]
from bien_nhan import *
from inventory import HOSTS,ssh_args
CHECK=r'''
import sys,pathlib,json,hashlib,os,shutil,collections
root=pathlib.Path(CODE_ROOT);sys.path[:0]=[str(root/'results/T-054/scripts'),str(root/'src'),str(root/'results/T-052/scripts')]
from bien_nhan import *
from nguon import compare_sources,placement_key,authorize
from p7 import load_plan
from lap_ho_so import stable_environment
from dieu_phoi import memory_request
import p7_entry_v2
planpin=PLAN_PIN;plan=load_plan(str(root/planpin['path']),planpin['sha256']);authority=read_pin(AUTH_PIN)
assert plan['preparation_only']and not authority['g3']and not authority['main_dispatch']
protocol=read_pin(plan['protocol_ref']);contract=read_pin(protocol['dispatch_contract_ref']);hc=dict(contract,**contract['hosts'][HOST])
assert str(root).replace('\\','/').lower()==hc['code_root'].lower()
assert protocol['status']=='CANDIDATE_NOT_LOCKED'
assert fingerprint(stable_environment())==hc['environment_sha256']['main'],'actual main env differs'
for rel,sha in hc['code_pins'].items():assert digest(root/rel)==sha,rel
data=pathlib.Path(hc['data_root']);source_cases=set();temps=[]
for j in plan['jobs']:
 s=j['slot'];ds=s['dataset'];oid=s['opaque_id'];rt=read_pin(j['runtime_ref']);ind=read_pin(j['independent_source_ref'])
 if (ds,oid)not in source_cases:
  compare_sources(rt,ind,ds,j['g1_revision'])
  # selector kiểm locator/byte/hash, không mở telemetry thành bảng.
  p7_entry_v2.source_selection(rt,oid,repo=data)
  source_cases.add((ds,oid))
 assert j['source']==rt['cases'][oid]and s['source_sha256']==fingerprint(j['source'])
 expected_t=j['source'].get('t',j['source'].get('t_ns',0)//10**9)-(300 if s['view']=='ce'else 0)
 assert j['t']==expected_t and s['window']=={'t':expected_t,'half_width_s':300}
 assert j['data_root']==hc['data_root']and j['code_pins']==hc['code_pins']
 assert j['protocol_ref']==plan['protocol_ref']
 for field in ['pythonpath','executable','prep_executable','method_executable']:assert j[field]==hc[field],field
 if s['arm']in protocol['configurations']:assert s['config_sha256']==protocol['configurations'][s['arm']]['sha256']and j['m1_contract']==protocol['m1_contract_ref']
 elif s['arm']=='C-d3':assert s['config_sha256']==fingerprint({'cd3':'same sealed M1'})
 else:assert s['config_sha256']==hc['baseline_config_sha256'][s['arm']]
 assert fingerprint(j['config'])==s['config_sha256']
 assert s['environment_sha256']==hc['environment_sha256']['py38'if j['kind']=='torai_pipeline'else'main']
 assert j['timeout_s']==hc['timeout_s']['C-d3'if j['kind']=='cd3'else'main_slot']
 policy=read_pin(j['failure_policy_ref']);candidate=read_pin(hc['failure_policy_candidate_ref']);assert policy==candidate
 for pin in policy['code_evidence']:read_pin(pin)if pin['path'].endswith('.json')else None
 got=[placement_key(j['slot'])for j in plan['jobs']]+[placement_key(dict(x,arm='M1',view='ce',seed=None))for x in plan['ce_support']]
 expected=read_pin(contract['partition_ref'])['hosts'][HOST]
 assert len(got)==len(set(got))and set(got)==set(expected)
 assert plan['budget']==hc['budget']and plan['monitor']==hc['monitor']and plan['resources']==hc['resources']and plan['workers']==hc['workers']
 temps.append(memory_request(plan,j))
try:authorize(plan,authority,'run')
except Blocked as e:denial=str(e);assert denial=='WAIT_G3'
else:raise AssertionError('candidate preparation unexpectedly dispatchable')
import psutil
available=psutil.virtual_memory().available;reserve=plan['resources']['reserve_bytes'];need=max(temps)
assert available>=need+reserve,'not enough RAM for even one maximum expected slot'
assert shutil.disk_usage(root).free>=2*1024**3,'less than 2GiB operational headroom'
assert not pathlib.Path(plan['directory']).exists(),'main queue exists unexpectedly'
print(json.dumps({'PASS':True,'host':HOST,'jobs':len(plan['jobs']),'Ce_insufficient':len(plan['ce_support']),'positions':len(got),'unique_cases_source_checked':len(source_cases),
 'source_mode':'opaque hashes/schema metadata only, no method','actual_main_environment_match':True,'code_pins':len(hc['code_pins']),
 'main_guard_denial':denial,'free_bytes':shutil.disk_usage(root).free,'available_RAM_bytes':available,'max_reserved_slot_bytes':need,
 'two_slots_memory_heuristic_fit':available>=2*need+reserve,'main_started':False}))
'''
def stage(host,metadata):
    name=host['name'];p=read_pin(metadata['plan_refs'][name]);protocol=read_pin(p['protocol_ref']);contract=read_pin(protocol['dispatch_contract_ref']);root=contract['hosts'][name]['code_root']
    freeze=OUT/'runs/freeze-cong-cu-007';pins=read_pin(ref(freeze/'files.json'))['files'];files={rel:freeze/'code'/rel for rel in pins}
    extras=[RUN/'prepared'/ (name+'-plan.json'),RUN/'prepared'/(name+'-authority.json'),RUN/'preparation-grant.json',RUN/'quyen-minh.txt']+list((RUN/'runtime-TT').glob('*.json'))
    for path in extras:files[path.relative_to(ROOT).as_posix()]=path
    planpin=metadata['plan_refs'][name];authpin=metadata['authority_refs'][name]
    checkcode=CHECK.replace('CODE_ROOT',repr(root)).replace('PLAN_PIN',repr(planpin)).replace('AUTH_PIN',repr(authpin)).replace('HOST',repr(name))
    checkrel='results/T-054/runs/chuan-bi-main-006/check_prepared.py';checkpath=RUN/(name+'-check-prepared.py');checkpath.write_text(checkcode,encoding='utf-8');files[checkrel]=checkpath
    buf=io.BytesIO()
    with tarfile.open(fileobj=buf,mode='w:gz')as t:
        for rel,path in sorted(files.items()):t.add(path,arcname=rel,recursive=False)
    archive=RUN/(name+'-code-and-prepared.tar.gz');archive.write_bytes(buf.getvalue());manifest={rel:{'bytes':path.stat().st_size,'sha256':digest(path)}for rel,path in files.items()};atomic(RUN/(name+'-staged-files.json'),manifest)
    code=r'''import sys,pathlib,tarfile,io,hashlib,json,subprocess,os
root=pathlib.Path(TARGET);stage=root.with_name('code.partial-006');assert not root.exists()and not stage.exists()
assert root.is_relative_to(pathlib.Path('/home/ubuntu/rca-p7/T-054'));stage.mkdir(parents=True,exist_ok=False)
b=sys.stdin.buffer.read();assert hashlib.sha256(b).hexdigest()==SHA
(stage.parent/'code-prepare-006.tar.gz').write_bytes(b)
with tarfile.open(fileobj=io.BytesIO(b))as t:
 for m in t.getmembers():assert m.isfile()and not m.name.startswith('/')and'..'not in pathlib.PurePosixPath(m.name).parts
 t.extractall(stage,filter='data')
manifest=MANIFEST
for rel,pin in manifest.items():
 p=stage/rel;assert p.stat().st_size==pin['bytes']and hashlib.sha256(p.read_bytes()).hexdigest()==pin['sha256']
stage.rename(root)
env=dict(os.environ,PYTHONHASHSEED='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
q=subprocess.run(['/home/ubuntu/rca/T-025/envs/main/bin/python','-B',str(root/'results/T-054/runs/chuan-bi-main-006/check_prepared.py')],env=env,capture_output=True,text=True,cwd=root,timeout=180)
print(json.dumps({'files':len(manifest),'exit':q.returncode,'stdout':q.stdout,'stderr':q.stderr}));assert q.returncode==0
'''.replace('TARGET',repr(root)).replace('SHA',repr(digest(archive))).replace('MANIFEST',repr(manifest))
    start=time.monotonic();q=subprocess.run(ssh_args(host)+['python3 -c '+shlex.quote(code)],input=buf.getvalue(),capture_output=True,timeout=240)
    result={'host':name,'exit':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode(),'elapsed_s':time.monotonic()-start};atomic(RUN/(name+'-preflight.json'),result)
    assert q.returncode==0,result
    print(json.dumps({'host':name,'result':json.loads(result['stdout'])}),flush=True)
    return result
if __name__=='__main__':
    meta=read_pin(ref(RUN/'checkpoint-01-plans.json'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:results=list(pool.map(lambda h:stage(h,meta),HOSTS))
    atomic(RUN/'checkpoint-03-cloud-preflight.json',{'PASS':True,'hosts':[r['host']for r in results],'main_started':False,'test_methods_executed':0})
