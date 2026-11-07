from pathlib import Path
import sys,copy,json
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'results/T-054/scripts'))
from bien_nhan import *
import dieu_phoi as d
from cham import merge_partitions
from nguon import authorize
target=OUT/'runs/cloud-checks-005';target.mkdir(parents=True,exist_ok=False)
checks=[]
def denied(fn):
 try:fn()
 except Blocked:return
 raise AssertionError('invalid case accepted')
class P:
 def create_time(self):return 1
 def cmdline(self):
  self.calls+=1;return ['parent']if self.calls==1 else ['worker','token']
 calls=0
proc=P()
with patch('psutil.Process',return_value=proc):
 ident=d.launched_identity(1,'token');assert ident['command_sha256']==fingerprint(['worker','token'])and proc.calls>=3
checks.append('preexec_parent_argv_not_pinned_as_worker')
jobs=[]
for i in range(3):
 s=dict(dataset='SYNTHETIC',opaque_id='fixture-'+str(i),member_sha256='a'*64,arm='M1'if i==0 else 'bo-E'+str(i),view='main',seed=None,
  window={'t':1000,'half_width_s':300},source_sha256='b'*64,config_sha256='c'*64,environment_sha256='d'*64)
 jobs.append(dict(slot=s,kind='synthetic',executable=sys.executable,timeout_s=10,scenario='slow_ok',sleep_s=.05,synthetic_records=[{'status':'NO_EVIDENCE','blocks':[]}]))
p=dict(schema='T054-PLAN-1',mode='synthetic',host_role='fixture',workers=2,jobs=jobs,monitor={'poll_s':.03,'max_monitor_gap_s':5,'score_phases':[]})
d.supervise(p,target/'queue');assert d.status(target/'queue')['counts']=={'VERIFIED':3}
checks.append('real_subprocess_handshake_two_workers')
bad=copy.deepcopy(p);bad['resources']={'reserve_bytes':1024,'factor':1.25,'expected_peak_bytes':{d.budget_group(j):10**15 for j in jobs}}
d.supervise(bad,target/'resource-blocked');assert d.status(target/'resource-blocked')['wait']['state']=='WAIT_RESOURCE_OR_DEPENDENCY'
assert not list((target/'resource-blocked').glob('*/attempt-*'));checks.append('insufficient_RAM_does_not_launch_or_score_TIMEOUT')
parts=[];full={'jobs':jobs[:2]}
for i,j in enumerate(jobs[:2]):
 pl={'jobs':[j],'host_role':'fixture'+str(i)};key=fingerprint(j['slot']);token='token'+str(i)
 inv=dict(schema='T054-INVOKE-1',token=token,slot_sha256=key,normalized_input_sha256='e'*64,
 **{k:j['slot'][k]for k in ['source_sha256','config_sha256','environment_sha256','window','seed']})
 env=dict(schema='T054-RESULT-1',token=token,slot_sha256=key,invocation_sha256=fingerprint(inv),records=j['synthetic_records'],record_sha256=fingerprint(j['synthetic_records']))
 receipt=atomic(target/f'r{i}.json',{'job_sha256':fingerprint(j),'result':atomic(target/f'e{i}.json',env),'invocation':atomic(target/f'i{i}.json',inv)})
 snap={'schema':'T054-SNAPSHOT-1','plan_sha256':fingerprint(pl),'slots':{key:{'state':'VERIFIED','receipt':receipt,'token':token}}}
 parts.append({'plan':atomic(target/f'p{i}.json',pl),'snapshot':atomic(target/f's{i}.json',snap)})
assert len(merge_partitions(full,parts)['slots'])==2
denied(lambda:merge_partitions(full,parts[:1]));denied(lambda:merge_partitions(full,parts+[parts[0]]))
checks+=['merge_complete_without_labels','merge_missing_blocked','merge_duplicate_host_blocked']
local=atomic(target/'mapping.json',{'proof':1});receive_paths({'/remote/output':str(target)})
assert read_pin(dict(local,path='/remote/output/mapping.json'))=={'proof':1}
denied(lambda:read_pin(dict(local,path='/remote/output/mapping.json',sha256='0'*64)))
receive_paths({});checks+=['received_original_ref_hash_verified','received_wrong_hash_blocked']
denied(lambda:authorize({'mode':'test','host_role':'ec2_1'},{'g3':False},'run'));checks.append('EC2_not_automatic_G3_permission')
atomic(target/'summary.json',{'PASS':True,'checks':checks,'count':len(checks),'synthetic_only':True,'test_opened':False})
print(json.dumps({'PASS':True,'checks':len(checks)}))
