"""Chỉ hai slot: C-e còn thiếu và một M1 OB làm đối chiếu concurrency."""
import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(ROOT/'results/T-054/runs/trien-khai-003')]
from bien_nhan import atomic,ref,read_pin,fingerprint
from nguon import original_dev_sources,compare_sources
from chuan_bi_pilot import environment, MAIN, ENV

old=read_pin(ref(ROOT/'results/T-054/runs/trien-khai-003/pilot-local-007/plan.json'))
dest=RUN/'pilot-2-worker-001';dest.mkdir(exist_ok=False)
private=Path('D:/RCA-ext/private/T-054/pilot-2-worker-001');private.mkdir(exist_ok=False)
candidates=read_pin(ref(ROOT/'results/T-054/pilot-plan.json'))['candidates']
ce=next(c for c in candidates if c['opaque_id']=='dev-a5cabe5fa7' and c['window']=='ce')
env=environment(MAIN);atomic(dest/'environment.json',env)
code=read_pin(ref(ROOT/'results/T-054/source-manifest.json'))
code_pins=dict(old['jobs'][0]['code_pins'])
for p in (ROOT/'results/T-054/scripts').glob('*.py'):code_pins[p.relative_to(ROOT).as_posix()]=ref(p)['sha256']
snap=dest/'code';snap.mkdir()
for p in (ROOT/'results/T-054/scripts').glob('*.py'):(snap/p.name).write_bytes(p.read_bytes())
jobs=[];metadata=[]
for ds,oid,view in [('RE2-TT','dev-a5cabe5fa7','ce'),('Nezha-OB','dev-607751ac0a','main')]:
    job=copy.deepcopy(next(j for j in old['jobs'] if j['slot']['dataset']==ds and j['slot']['arm']=='M1'))
    descriptor=read_pin(job['independent_source_ref'])
    if view=='ce':descriptor['ce_evidence']={oid:{'command':ce['native_command_pin'],'record':ce['native_record'],'config_id':'K-E1+E2+E5'}}
    rows=original_dev_sources(descriptor)
    row=next(iter(rows['cases_by_member'].values()))
    runtime=read_pin(job['runtime_ref']);runtime['cases']={oid:row}
    compare_sources(runtime,descriptor,ds,job['g1_revision'])
    job['runtime_ref']=atomic(private/(ds+'-runtime.json'),runtime)
    job['independent_source_ref']=atomic(private/(ds+'-originals.json'),descriptor)
    job['source']=row;job['code_pins']=code_pins;job['a4']=False
    job['t']=row.get('t',row.get('t_ns',0)//10**9)-(300 if view=='ce' else 0)
    job['slot'].update(view=view,window={'t':job['t'],'half_width_s':300},source_sha256=fingerprint(row),environment_sha256=fingerprint(env))
    job['failure_policy_ref']=ref(RUN/'failure-policy-dev.json')
    jobs.append(job);metadata.append({'dataset':ds,'opaque_id':oid,'view':view,'reference':ce if view=='ce' else 'pilot-local-007'})
plan=dict(schema='T054-PLAN-1',mode='dev',host_role='local',workers=2,directory=str(dest/'queue'),
          jobs=jobs,inventories=old['inventories'],open_before_run=[],monitor=read_pin(ref(RUN/'failure-policy-dev.json'))['monitor'],
          budget={'mode':'UNTIL_COHORT_COMPLETE','wall_s':None,'method_dataset_s':{},'decision_ref':ref(RUN/'quyet-dinh-minh.json')},
          purpose='one missing C-e route + specific two-worker operational parity; no broad baseline rerun',
          sensitivity_decision_ref=ref(RUN/'quyet-dinh-minh.json'))
pin=atomic(dest/'plan.json',plan)
auth=dict(schema='T054-AUTHORITY-1',source=ref(RUN/'quyen-minh.txt'),pilot_grant=True,materialize_private=True,
          plan_sha256=fingerprint(plan),torai_A_source_grant=False,g3=False,test_grant=False,ssh_grant=False)
authority=atomic(dest/'authority.json',auth)
atomic(dest/'metadata.json',{'plan':pin,'authority':authority,'slots':metadata,'no_test':True})
result=subprocess.run([MAIN,'-B',str(ROOT/'results/T-054/scripts/p7.py'),'run','--plan',pin['path'],
                        '--sha256',pin['sha256'],'--authority',authority['path'],'--authority-sha256',authority['sha256']],
                       env=ENV,capture_output=True)
atomic(dest/'launch.json',{'exit_code':result.returncode,'stdout':result.stdout.decode('utf-8'),'stderr':result.stderr.decode('utf-8')})
print(result.stdout.decode('utf-8'));print(result.stderr.decode('utf-8'));result.check_returncode()
