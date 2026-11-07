"""Đổi đúng ba slot TORAI chưa chạy sau sửa kiểm kê; không reset budget/chạy lại slot đạt."""
import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-003'
sys.path[:0] = [str(OUT / 'scripts'), str(RUN)]
from bien_nhan import atomic, append, fingerprint, read_pin, ref
from dieu_phoi import status
from chuan_bi_pilot import ENV, MAIN

old = RUN / 'pilot-local-002'
state = status(old / 'queue')
assert state['controller'] is None, 'DRAIN chưa dừng supervisor'
assert all(r['state'] == 'VERIFIED' for r in state['jobs'].values()), 'Cần phân xử trạng thái trước nhận tiếp'
dest = RUN / (sys.argv[1] if len(sys.argv) > 1 else 'pilot-local-004')
dest.mkdir(exist_ok=False)
meta = read_pin(ref(old / 'metadata.json'))
plan = copy.deepcopy(read_pin(meta['plan']))
original_jobs = {fingerprint(j['slot']): j for j in plan['jobs']}
env = read_pin(ref(RUN / 'environments-corrected.json'))
changed = []
for job in plan['jobs']:
    if job['kind'] == 'torai_pipeline':
        assert fingerprint(job['slot']) not in state['jobs'], 'TORAI đã chạy; không được đổi âm thầm'
        changed.append({'seed': job['slot']['seed'], 'old_environment': job['slot']['environment_sha256']})
        job['slot']['environment_sha256'] = fingerprint(env['py38'])
assert len(changed) == 3
# Nguồn A chỉ đúng ca Minh vừa cấp; không liệt kê/mở các thư mục A khác.
sys.path.insert(0, str(ROOT / 'src'))
from p3.runner import _tac_gia_A
allow = read_pin(ref(ROOT / 'results/T-022/allowlist-dev.json'))
source_row = next(r for r in allow['cases'] if r['opaque_id'] == 'dev-a5cabe5fa7')
paths = _tac_gia_A(source_row['case_dir'])
author_root = Path('D:/RCA-ext/work/T-016/data/torai-TT')
files = {}
for kind, path in paths.items():
    path = Path(path)
    item = ref(path)
    files[kind] = {'path': path.relative_to(author_root).as_posix(), 'bytes': item['bytes'], 'sha256': item['sha256']}
base_job = next(j for j in plan['jobs'] if j['slot']['arm'] == 'torai_B' and j['slot']['seed'] == 0)
private = Path(base_job['runtime_ref']['path']).parent
author_doc = {'schema': 'T054-TORAI-A-SOURCE-1',
       'dataset': 'RE2-TT', 'g1_revision': base_job['g1_revision'], 'data_root': str(author_root),
       'grant': ref(RUN / 'grant-A-dev.json'),
       'cases_by_member': {base_job['slot']['member_sha256']: {'files': files}}}
author_path = private / 'A-source-dev-a5cabe5fa7.json'
if author_path.exists():
    author_ref = ref(author_path)
    assert read_pin(author_ref) == author_doc, 'Nguồn A cũ khác; không ghi đè'
else:
    author_ref = atomic(author_path, author_doc)
for seed in (0, 1, 2):
    a_job = copy.deepcopy(next(j for j in plan['jobs'] if j['slot']['arm'] == 'torai_B' and j['slot']['seed'] == seed))
    a_job['slot'].update(arm='torai_A', author_source_sha256=author_ref['sha256'])
    a_job['config']['method'] = 'torai_A'
    a_job['slot']['config_sha256'] = fingerprint(a_job['config'])
    a_job.update(author_source_ref=author_ref, a4=False)
    plan['jobs'].append(a_job)
plan['budget']['method_dataset_s']['RE2-TT|torai_A'] = 600
plan['directory'] = str(dest / 'queue')
plan['prior_plan_ref'] = meta['plan']
plan['continuation_reason'] = 'fix environment probe, retain verified and cumulative budget; no method/design change'
p = atomic(dest / 'plan.json', plan)
a = read_pin(meta['authority']); a['plan_sha256'] = fingerprint(plan)
a['previous_authority'] = meta['authority']
a.update(torai_A_source_grant=True, torai_A_source_sha256=author_ref['sha256'],
         additional_sources=[ref(RUN / 'grant-A-dev.json')])
ap = atomic(dest / 'authority.json', a)
queue = dest / 'queue'; queue.mkdir()
inherited = []
for key, row in state['jobs'].items():
    job = original_jobs[key]
    target_job = next(j for j in plan['jobs'] if fingerprint(j['slot']) == key)
    assert target_job == job
    receipt = read_pin(row['receipt']); assert receipt['job_sha256'] == fingerprint(job)
    append(queue / 'events.jsonl', dict({k: v for k, v in row.items() if k != 'utc'},
           inherited_event_utc=row['utc'], inherited_from=meta['plan']))
    # Sổ cost kế thừa để group cap qua resume không reset; attempt/output thật giữ nguyên ở gốc cũ.
    cost = read_pin(ref(Path(row['attempt']) / 'cost.json'))
    atomic(queue / key / 'attempt-inherited' / 'cost.json', cost)
    inherited.append(key)
start = read_pin(ref(old / 'queue/budget-start.json'))
start['plan_sha256'] = fingerprint(plan)
atomic(queue / 'budget-start.json', start)
atomic(dest / 'metadata.json', dict(meta, plan=p, authority=ap, prior_metadata=ref(old / 'metadata.json'),
                                  environments=ref(RUN / 'environments-corrected.json'), slot_count=len(plan['jobs']),
                                  A_source_ref=author_ref, A_grant=ref(RUN / 'grant-A-dev.json')))
atomic(dest / 'continuation.json', {'changed_only_unstarted_TORAI_environment': changed,
       'inherited_verified_slots': inherited, 'budget_start_preserved': True,
       'old_controller_stopped': True, 'source_and_method_unchanged': True})
result = subprocess.run([MAIN, '-B', str(OUT / 'scripts/p7.py'), 'run', '--plan', p['path'],
          '--sha256', p['sha256'], '--authority', ap['path'], '--authority-sha256', ap['sha256']],
          env=ENV, capture_output=True)
atomic(dest / 'launch.json', {'exit_code': result.returncode, 'stdout': result.stdout.decode('utf-8'),
                             'stderr': result.stderr.decode('utf-8')})
print(result.stdout.decode('utf-8')); print(result.stderr.decode('utf-8')); result.check_returncode()
