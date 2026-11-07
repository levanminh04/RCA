"""Kiểm điều phối sau sửa cuối; pipeline dùng worker giả, không telemetry."""
import copy
import sys
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(RUN)]
from bien_nhan import *
import dieu_phoi as d
from kiem_van_hanh import plan,verified,denied

checks=[]
p=plan('final2-two-workers',2,1);d.supervise(p,p['directory']);verified(p)
assert all('host_available_ram' in r for r in events(Path(p['directory'])/'resources.jsonl'))
assert d.status(p['directory'])['counts']=={'VERIFIED':2}
checks.append('two_workers_and_host_resource_fields')
p=plan('final2-same-group',2,.5);p['jobs'][1]['slot']['arm']='M1'
d.supervise(p,p['directory']);verified(p)
starts=[];ends=[]
for a in Path(p['directory']).glob('*/attempt-*'):
    t=read_pin(ref(a/'launch.json'))['started_epoch'];starts.append(t);ends.append(t+read_pin(ref(a/'cost.json'))['wall_s'])
assert max(starts)>=min(ends)
checks.append('same_method_dataset_serialized')
p=plan('final2-error-stops-dispatch',3,1);p['workers']=1;p['jobs'][0]['scenario']='source_error'
d.supervise(p,p['directory']);st=d.status(p['directory'])
assert len(st['jobs'])==1 and next(iter(st['jobs'].values()))['state']=='BLOCKED' and st['wait']['state']=='WAIT_ERROR'
checks.append('operational_error_stops_new_jobs_unrun_not_TIMEOUT')

fake=RUN/'pipeline-transport-only-002';(fake/'scripts').mkdir(parents=True)
worker='''import sys,time
from pathlib import Path
sys.path.insert(0, REPLACE_REAL_SCRIPT_PATH)
from bien_nhan import *
j=read_pin(ref(sys.argv[1]));a=Path(sys.argv[2]);token=sys.argv[3];s=j['slot']
if j['fixture_route']=='torai_prep':
 p=a/'fake.csv';p.write_text('x\\n1\\n',encoding='utf-8')
 atomic(a/'prepared.json',dict(schema='T054-PREP-1',token=token,slot_sha256=fingerprint(s),tables={'fake':ref(p)}))
else:
 inv=dict(schema='T054-INVOKE-1',slot_sha256=fingerprint(s),token=token,normalized_input_sha256='e'*64,
          **{k:s[k]for k in ['config_sha256','source_sha256','environment_sha256','window','seed']},prepared_ref=j['prepared'])
 atomic(a/'invocation.json',inv)
 append(a/'phases.jsonl',dict(token=token,pid=__import__('os').getpid(),phase='method',state='start',invocation_sha256=fingerprint(inv)))
 time.sleep(10)
'''.replace('REPLACE_REAL_SCRIPT_PATH',repr(str(ROOT/'results/T-054/scripts')))
(fake/'scripts/worker.py').write_text(worker,encoding='utf-8')
p=plan('final2-pipeline-method-timeout',1);p['jobs'][0].update(pipeline_fixture=True,prep_executable=sys.executable,
 method_executable=sys.executable,timeout_s=2,failure_policy_ref=ref(RUN/'failure-policy-dev.json'))
p['jobs'][0]['slot'].update(arm='torai_B',dataset='RE2-TT',seed=0)
with patch.object(d,'OUT',fake):d.supervise(p,p['directory'])
verified(p)
a=Path(next(iter(d.status(p['directory'])['jobs'].values()))['attempt'])
assert read_pin(ref(a/'result.json'))['records'][0]['status']=='TIMEOUT'
assert read_pin(ref(a/'verified.json'))['method_failure']==ref(a/'method-failure.json')
checks.append('pipeline_method_timeout_keeps_prep_and_scoring_receipt')
atomic(RUN/'final2-branch-checks.json',{'PASS':True,'checks':checks,'pipeline_scope':'transport-only fake stage processes; not real TORAI method',
 'test_opened':False})
print('final branch checks PASS',len(checks))
