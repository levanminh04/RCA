
import sys,pathlib,json,hashlib,os,shutil,collections
root=pathlib.Path('/home/ubuntu/rca-p7/T-054/ec2_2/main-005/code');sys.path[:0]=[str(root/'results/T-054/scripts'),str(root/'src'),str(root/'results/T-052/scripts')]
from bien_nhan import *
from nguon import compare_sources,placement_key,authorize
from p7 import load_plan
from lap_ho_so import stable_environment
from dieu_phoi import memory_request
import p7_entry_v2
planpin={'bytes': 5323834, 'path': 'results/T-054/runs/chuan-bi-main-006/prepared/ec2_2-plan.json', 'sha256': 'fb9bd7a907c0a5a9ab01916173f9600819a61df9296f751e62b5ca4dd8252ec1'};plan=load_plan(str(root/planpin['path']),planpin['sha256']);authority=read_pin({'bytes': 649, 'path': 'results/T-054/runs/chuan-bi-main-006/prepared/ec2_2-authority.json', 'sha256': '1e263b42649f82eda81d0a2e6ccf3635fa8daa194fe6f947d36c22e5a9e1e136'})
assert plan['preparation_only']and not authority['g3']and not authority['main_dispatch']
protocol=read_pin(plan['protocol_ref']);contract=read_pin(protocol['dispatch_contract_ref']);hc=dict(contract,**contract['hosts']['ec2_2'])
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
 expected=read_pin(contract['partition_ref'])['hosts']['ec2_2']
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
print(json.dumps({'PASS':True,'host':'ec2_2','jobs':len(plan['jobs']),'Ce_insufficient':len(plan['ce_support']),'positions':len(got),'unique_cases_source_checked':len(source_cases),
 'source_mode':'opaque hashes/schema metadata only, no method','actual_main_environment_match':True,'code_pins':len(hc['code_pins']),
 'main_guard_denial':denial,'free_bytes':shutil.disk_usage(root).free,'available_RAM_bytes':available,'max_reserved_slot_bytes':need,
 'two_slots_memory_heuristic_fit':available>=2*need+reserve,'main_started':False}))
