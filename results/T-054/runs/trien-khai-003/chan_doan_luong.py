"""Một ca DEV đã được Minh cấp riêng; kiểm giả thuyết luồng, không đổi cấu hình chính."""
import copy
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-003'
sys.path[:0] = [str(OUT / 'scripts'), str(RUN)]
from bien_nhan import atomic, append, fingerprint, read_pin, ref
from dieu_phoi import identity, _monitor, verify_attempt
from nguon import authorize
from chuan_bi_pilot import MAIN, ENV, PATHS

grant = {'source': 'Minh trả lời trong chat 05/11/2026', 'answer': 'Cho chạy chẩn đoán đúng ca này',
         'scope': 'dev-607751ac0a MicroRank, một lượt kiểm thiết lập luồng; không đổi cấu hình chính/dung sai',
         'correction': 'Hồ sơ ghi current OpenBLAS 16 tại lần kiểm kê; source thread lịch sử OPEN. Không coi current16 là bằng chứng lịch sử.',
         'test': False, 'main_config_changed': False}
grant_ref = atomic(RUN / 'grant-diagnostic-thread.json', grant)
with (ROOT / 'tasks/T-054-khoa-g3-chay-p7-a/LOG.md').open('ab') as f:
    f.write(('\n\n### Quyết định Minh trong phiên 4 — chẩn đoán số luồng\n\nMinh trả lời “Cho chạy chẩn đoán đúng ca này” cho một lượt MicroRank dev-607751ac0a để kiểm giả thuyết sai khác số cuối do cấu hình luồng, giữ cả kết quả, chưa đổi cấu hình chính/dung sai. Nguồn: grant-diagnostic-thread.json. Đính chính ngay trong chat: hồ sơ WHY ghi current16 lúc kiểm kê, source thread lịch sử còn OPEN; câu hỏi đã diễn đạt quá mạnh “nguồn cũ16”, không dùng câu ấy làm sự thật. Quyền thao tác một lượt vẫn đúng phạm vi đã hỏi; không suy kết quả từ tiền đề chưa xác minh.\n').encode('utf-8'))
dest = RUN / 'diagnostic-thread-001'; dest.mkdir(exist_ok=False)
base_plan = read_pin(ref(RUN / 'pilot-local-007/plan.json'))
job = copy.deepcopy(next(j for j in base_plan['jobs'] if j['slot']['dataset'] == 'Nezha-OB' and j['slot']['arm'] == 'microrank'))
env = dict(ENV)
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    env.pop(name, None)
# Kiểm kê đúng thứ tự nhập của worker; đo số luồng thực tế của thư viện đã nhập.
probe = ('import sys,json;sys.path.insert(0,' + repr(str(OUT/'scripts')) + ');sys.path.insert(0,' + repr(str(ROOT/'src')) +
         ');sys.path.extend(' + repr(PATHS) + ');import numpy,scipy.linalg;from lap_ho_so import stable_environment;'
         'from threadpoolctl import threadpool_info;print(json.dumps({"environment":stable_environment(),"threadpools":threadpool_info()}))')
r = subprocess.run([MAIN, '-B', '-c', probe], env=env, capture_output=True, check=True)
observed_env = json.loads(r.stdout)
atomic(dest/'environment.json', observed_env)
job['slot']['environment_sha256'] = fingerprint(observed_env['environment'])
job['code_pins'].update({p.relative_to(ROOT).as_posix():ref(p)['sha256'] for p in (OUT/'scripts').glob('*.py')})
job['diagnostic_only'] = 'thread settings comparison; no main configuration decision'
plan = {'schema':'T054-PLAN-1','mode':'dev','host_role':'local','jobs':[job],
        'directory':str(dest),'budget':{'wall_s':120,'method_dataset_s':{'Nezha-OB|microrank':120}},
        'monitor':{'poll_s':.1,'max_monitor_gap_s':5,'score_phases':[]}}
p = atomic(dest/'plan.json',plan)
authority = {'source':grant_ref,'pilot_grant':True,'plan_sha256':fingerprint(plan)}
atomic(dest/'authority.json',authority); authorize(plan,authority,'run')
attempt=dest/'attempt-001'; attempt.mkdir(); jp=atomic(attempt/'job.json',job);token=uuid.uuid4().hex
start=time.monotonic()
append(dest/'events.jsonl',{'state':'RUNNING','token':token,'plan':p})
options={}
if os.name=='nt':options['creationflags']=subprocess.CREATE_NEW_PROCESS_GROUP|subprocess.CREATE_NO_WINDOW
with (attempt/'stdout.txt').open('ab') as stdout,(attempt/'stderr.txt').open('ab') as stderr:
    process=subprocess.Popen([MAIN,'-B',str(OUT/'scripts/worker.py'),jp['path'],str(attempt),token],
                             env=env,cwd=ROOT,stdout=stdout,stderr=stderr,**options)
ident=identity(process.pid,token);atomic(attempt/'identity.json',ident)
timed,sample=_monitor(attempt,token,ident,time.time()+120,plan['monitor'])
assert not timed,'diagnostic timeout; preserved, no retry'
records=verify_attempt(attempt,job,token)
actual=records[0]
old_ref=next(x['source_ref'] for x in read_pin(ref(OUT/'runs/trien-khai-002/pilot-proposal.json'))['baseline_jobs']
             if x['dataset']=='Nezha-OB' and x['arm']=='microrank')
expected=read_pin(old_ref)
one_job=next(j for j in base_plan['jobs'] if j['slot']['dataset']=='Nezha-OB' and j['slot']['arm']=='microrank')
from dieu_phoi import status
one_state=status(RUN/'pilot-local-007/queue')['jobs'][fingerprint(one_job['slot'])]
one_inv=read_pin(ref(Path(one_state['attempt'])/'invocation.json'))
one=read_pin(ref(Path(one_state['attempt'])/'result.json'))['records'][0]
inv=read_pin(ref(attempt/'invocation.json'))
same_input=one_inv['normalized_input_sha256']==inv['normalized_input_sha256']
fields=('blocks','entity_ranking','ranking_native','status','error','diagnostics','observed_entities')
old_exact=all(actual.get(k)==expected.get(k) for k in fields)
one_exact=all(actual.get(k)==one.get(k) for k in fields)
result={'status':'DIAGNOSTIC_ONLY_NOT_MAIN_DECISION','wall_s':time.monotonic()-start,
 'same_normalized_input_as_one_thread':same_input,'exact_scientific_fields_vs_old':old_exact,
 'exact_scientific_fields_vs_one_thread':one_exact,
 'threadpools_observed':observed_env['threadpools'],
 'old_reference':old_ref,'one_thread_attempt':one_state['attempt'],'new_result':ref(attempt/'result.json'),
 'ranking_order_unchanged': [r['entity'] for r in actual['entity_ranking']]==[r['entity'] for r in one['entity_ranking']],
 'historical_source_thread':'OPEN; current diagnostic cannot establish old run settings',
 'interpretation':('This diagnostic distinguishes the observed current thread regimes on the same normalized input; it does not alone explain historical output or authorize a tolerance.'),
 'main_config_changed':False,'test_opened':False}
atomic(dest/'summary.json',result)
append(dest/'events.jsonl',{'state':'COMPLETE','summary':ref(dest/'summary.json')})
print(json.dumps(result,ensure_ascii=False))
