"""Read-only checks of prepared artifacts. Writes only its receipt in this run."""
from pathlib import Path
import difflib
import importlib.util
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(ROOT/'src')]
from bien_nhan import digest,Blocked
from p7 import load_plan
from nguon import authorize
from dieu_phoi import memory_request

def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
checks=[]
manifest=load(ROOT/'results/T-054/manifest-cai-re3-h2-010.json')
for rel,pin in manifest['outputs'].items():
    path=ROOT/rel;assert path.stat().st_size==pin['bytes']and digest(path)==pin['sha256'],rel
checks.append({'name':'immutable010_reuse','PASS':True,'files':len(manifest['outputs'])})
changed=[]
for rel,pin in manifest['mutable_current'].items():
    if digest(ROOT/rel)!=pin['sha256']:changed.append(rel)
allowed={'src/p3/re3.py','results/T-054/scripts/worker.py','tasks/T-054-khoa-g3-chay-p7-a/SPEC.md',
         'docs/WHY.md','docs/DECISIONS.md','tasks/T-054-khoa-g3-chay-p7-a/LOG.md','docs/STATE.md'}
assert set(changed)<=allowed,changed
checks.append({'name':'010_mutable_change_scope','PASS':True,'changed':changed})
pins=load(RUN/'current-code-pins.json')['files']
for rel,pin in pins.items():assert digest(ROOT/rel)==pin['sha256'],rel
checks.append({'name':'current_code_pins','PASS':True,'files':len(pins)})
for host in ['ec2_1','ec2_2','local']:
    path=RUN/'prepared'/(host+'-plan.json');p=load_plan(str(path),digest(path))
    auth=load(RUN/'prepared'/(host+'-authority.json'))
    try:authorize(p,auth,'run')
    except Blocked as exc:assert str(exc)=='WAIT_G3'
    else:raise AssertionError('unexpected run grant')
    if host=='local':assert not Path(p['directory']).exists(),'main queue unexpectedly exists'
checks.append({'name':'three_plan_validation_and_run_denial','PASS':True,'denied':'WAIT_G3'})
spec=importlib.util.spec_from_file_location('activate011',RUN/'activate_after_g3.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
for grant in [{},{'g3':True},{'g3':True,'test_grant':True,'main_dispatch':True,'torai_A_source_grant':False}]:
    try:mod.require_grant(grant)
    except Blocked:pass
    else:raise AssertionError('incomplete grant accepted')
assert not (RUN/'activated-001').exists()
checks.append({'name':'activation_requires_real_grants','PASS':True,'negative_checks':3,
               'positive_activation':'NOT_RUN_NO_REAL_GRANT'})
program="import sys,json;from pathlib import Path;sys.path.insert(0,'src');from p3.re3 import validate_profile,validate_torai_status;p=json.loads(Path(sys.argv[1]).read_text(encoding='utf8'));validate_profile(p);validate_torai_status([0,2,13,16],p);print('PASS')"
cp=subprocess.run(['D:/RCA-ext/envs/py38-rcdlock/Scripts/python.exe','-X','utf8','-B','-c',program,
                   str(RUN/'grpc-check-001/profile-GENERATED.json')],capture_output=True,text=True)
assert cp.returncode==0,cp.stderr
checks.append({'name':'grpc_profile_actual_py38','PASS':True,'stdout':cp.stdout.strip()})
resources=load(RUN/'local-resource-final.json');plan=load(RUN/'prepared/local-plan.json')
requests=[memory_request(plan,j)for j in plan['jobs']]
resources.update(largest_slot_RAM_request_bytes=max(requests),reserve_bytes=plan['resources']['reserve_bytes'],
    RAM_status='WAIT_RESOURCE'if resources['available_RAM_bytes']<max(requests)+plan['resources']['reserve_bytes']else'SNAPSHOT_FITS_ONE_LARGEST_SLOT',
    storage_planning_bytes=load(RUN/'storage-copy-accounting.json')['corrected_planning_bytes'])
resources['storage_status']='SCENARIO_FITS_D'if resources['D_free_bytes']>=resources['storage_planning_bytes']else'WAIT_DISK'
assert resources['C_proposal_path_exists']is False
checks.append({'name':'resources','observation':resources,'bound_proven':False})
diff=[]
for rel in ['src/p3/re3.py','results/T-054/scripts/worker.py','tasks/T-054-khoa-g3-chay-p7-a/SPEC.md','docs/WHY.md','docs/DECISIONS.md']:
    before=(RUN/'before'/rel).read_text(encoding='utf-8-sig').splitlines(True)
    after=(ROOT/rel).read_text(encoding='utf-8-sig').splitlines(True)
    diff.extend(difflib.unified_diff(before,after,fromfile='before/'+rel,tofile=rel))
(RUN/'approved-core-doc.diff').write_text(''.join(diff),encoding='utf-8')
with (RUN/'local-checks.json').open('x',encoding='utf-8')as f:json.dump({'PASS':True,'checks':checks,'no_main':True,'no_cloud':True},f,ensure_ascii=False,separators=(',',':'))
print(json.dumps({'PASS':True,'checks':len(checks),'RAM_status':resources['RAM_status'],'storage_status':resources['storage_status']}),flush=True)
