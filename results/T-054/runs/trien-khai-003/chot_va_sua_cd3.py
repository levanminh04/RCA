"""Sau pilot: audit hai lỗi dev, sửa tuyến C-d3 và chỉ chạy lại C-d3; giữ mọi bản gốc."""
import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-003'
sys.path[:0] = [str(OUT / 'scripts'), str(RUN), str(ROOT / 'src')]
from bien_nhan import atomic, append, fingerprint, read_pin, ref
from dieu_phoi import status
from chuan_bi_pilot import ENV, MAIN

old = RUN / 'pilot-local-005'
state = status(old / 'queue')
assert state['controller'] is None and len(state['jobs']) == 32, 'Pilot chưa dừng/đủ32slot'
assert all(v['state'] in ('VERIFIED', 'BLOCKED') for v in state['jobs'].values())
subprocess.run([MAIN, '-B', str(RUN / 'hoan_thien_code_sau_pilot.py')], env=ENV, check=True)
# Nhập module mới trong tiến trình khác để không dùng cache hàm trước sửa.
if __name__ == '__main__':
    code = r'''
import copy,json,sys
from pathlib import Path
ROOT=Path.cwd(); OUT=ROOT/'results/T-054';RUN=OUT/'runs/trien-khai-003'
sys.path[:0]=[str(OUT/'scripts'),str(RUN),str(ROOT/'src')]
from bien_nhan import atomic,append,fingerprint,read_pin,ref,verify_envelope
from dieu_phoi import status,verify_attempt
from nguon import source_row
from chuan_bi_pilot import ENV,MAIN
import subprocess
old=RUN/'pilot-local-005';meta=read_pin(ref(old/'metadata.json'));plan=read_pin(meta['plan']);state=status(old/'queue')
jobs={fingerprint(j['slot']):j for j in plan['jobs']}
# Đọc lại đúng trace TT đã cấp để kiểm cơ chế lỗi, sau khi lô đo đã dừng.
j=next(j for j in plan['jobs'] if j['slot']['dataset']=='RE2-TT' and j['slot']['arm']=='microrank')
paths=source_row(j['source'],j['data_root'])
import pyarrow.parquet as pq
from p3.cua_so import cat_span
frame=pq.read_table(paths['traces.parquet']).to_pandas()
frame=cat_span(frame,j['t'])
frame['methodName']=frame['methodName'].fillna(frame['operationName'])
operations=frame['serviceName']+'_'+frame['methodName']
end=frame['startTime']+frame['duration'];t_us=j['t']*1000000
operation='ts-order-other-service_getMore ts.orders'
count_n=int(((operations==operation)&(end<t_us)).sum())
count_a=int(((operations==operation)&(end>=t_us)).sum())
assert count_n==0 and count_a>0
audit=atomic(RUN/'operation-error-audit.json',{'t':j['t'],'trace_sha256':j['source']['files']['traces.parquet']['sha256'],
 'operation':operation,'normal_count':{'microrank':count_n,'tracerca':count_n},
 'anomalous_count':{'microrank':count_a,'tracerca':count_a},'window':j['slot']['window'],
 'mechanism':'Both code paths split by span end; operation appears only in A. MicroRank raises at newops, TraceRCA dictionary lookup lacks baseline. This is method implementation assumption, not a malformed source/adapter claim.',
 'original_run_method_status_preserved':True})
source=read_pin(ref(OUT/'runs/trien-khai-002/pilot-proposal.json'))['baseline_jobs']
for key,row in state['jobs'].items():
 job=jobs[key];slot=job['slot']
 if row['state']!='BLOCKED' or slot['arm']=='C-d3':continue
 assert slot['dataset']=='RE2-TT' and slot['arm'] in ('microrank','tracerca'),(slot,row)
 attempt=Path(row['attempt']); envelope=read_pin(ref(attempt/'result.json'));inv=read_pin(ref(attempt/'invocation.json'))
 old_ref=next(x['source_ref'] for x in source if all(x[k]==slot[k] for k in ('dataset','opaque_id','arm','seed')))
 core=ROOT/'src/microrank/__init__.py' if slot['arm']=='microrank' else Path('D:/RCA-ext/src/RCAEval/RCAEval/e2e/tracerca.py')
 cls={'scope':'DEV_BASELINE_REPRODUCTION_ONLY','origin':'method_implementation_assumption',
      'job_sha256':fingerprint(job),'result_sha256':fingerprint(envelope),'invocation_sha256':fingerprint(inv),
      'baseline_reference':old_ref,'input_audit':audit,'code_evidence':[ref(core),ref(ROOT/'src/p3/adapters'/ (slot['arm']+'.py'))],
      'main_policy_not_selected':True,'reason':'Reproduces previously scored ERROR on same authorized dev source, with code/input audit; not inferred from error string alone.'}
 cpin=atomic(attempt/'dev-error-reproduction.json',cls)
 verify_attempt(attempt,job,row['token'])
 receipt=atomic(attempt/'verified-dev-error.json',{'job_sha256':fingerprint(job),'result':ref(attempt/'result.json'),
              'invocation':ref(attempt/'invocation.json'),'dev_error_reproduction':cpin})
 row.update(state='VERIFIED',receipt=receipt,reason='DEV_ERROR_REPRODUCTION_CLASSIFIED')
dest=RUN/'pilot-local-006';dest.mkdir(exist_ok=False);new=copy.deepcopy(plan)
new['directory']=str(dest/'queue');new['prior_plan_ref']=meta['plan']
new['continuation_reason']='C-d3 wrapper uses sealed extra.canh; only failed operational CD3 repeated. Two dev ERRORs independently audited against baseline, not converted to OK.'
for job in new['jobs']:
 if job['slot']['arm']=='C-d3':
  job['code_pins'].update({p.relative_to(ROOT).as_posix():ref(p)['sha256'] for p in (OUT/'scripts').glob('*.py')})
p=atomic(dest/'plan.json',new);authority=read_pin(meta['authority']);authority['previous_authority']=meta['authority'];authority['plan_sha256']=fingerprint(new)
a=atomic(dest/'authority.json',authority);q=dest/'queue';q.mkdir()
for key,row in state['jobs'].items():
 cost=read_pin(ref(Path(row['attempt'])/'cost.json'))
 atomic(q/key/'attempt-inherited'/'cost.json',cost)
 if jobs[key]['slot']['arm']=='C-d3':continue
 assert row['state']=='VERIFIED'
 append(q/'events.jsonl',dict({k:v for k,v in row.items() if k!='utc'},inherited_event_utc=row['utc'],inherited_from=meta['plan']))
start=read_pin(ref(old/'queue/budget-start.json'));start['plan_sha256']=fingerprint(new);atomic(q/'budget-start.json',start)
atomic(dest/'metadata.json',dict(meta,plan=p,authority=a,prior_metadata=ref(old/'metadata.json')))
atomic(dest/'continuation.json',{'only_new_method_call':'C-d3 operational fix','inherited_verified_slots':31,'budget_start_and_all_prior_costs_preserved':True,'main_seal_unchanged':True})
r=subprocess.run([MAIN,'-B',str(OUT/'scripts/p7.py'),'run','--plan',p['path'],'--sha256',p['sha256'],'--authority',a['path'],'--authority-sha256',a['sha256']],env=ENV,capture_output=True)
atomic(dest/'launch.json',{'exit_code':r.returncode,'stdout':r.stdout.decode('utf-8'),'stderr':r.stderr.decode('utf-8')})
print(r.stdout.decode('utf-8'));print(r.stderr.decode('utf-8'));r.check_returncode()
'''
    subprocess.run([MAIN, '-B', '-c', code], cwd=ROOT, env=ENV, check=True)
