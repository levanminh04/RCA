"""Kiểm lại riêng CIRCA sau sửa metadata mốc current; giữ kết quả/scoring dev đầu."""
import copy
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

old = RUN / 'pilot-local-006'; state = status(old / 'queue')
assert state['controller'] is None and len(state['jobs']) == 32
meta = read_pin(ref(old / 'metadata.json')); plan = copy.deepcopy(read_pin(meta['plan']))
dest = RUN / 'pilot-local-007'; dest.mkdir(exist_ok=False)
plan['directory'] = str(dest / 'queue'); plan['prior_plan_ref'] = meta['plan']
plan['continuation_reason'] = 'CIRCA records actual diagnostics.circa_current in window, same method/config; validate full wrapper again; DEV labels already viewed, not independent test'
changed = []
for job in plan['jobs']:
    if job['slot']['arm'] == 'circa' and job['slot']['dataset'] == 'RE2-TT':
        changed.append(fingerprint(job['slot']))
        job['code_pins'].update({p.relative_to(ROOT).as_posix(): ref(p)['sha256'] for p in (OUT / 'scripts').glob('*.py')})
assert len(changed) == 1
p = atomic(dest / 'plan.json', plan)
authority = read_pin(meta['authority']); authority['plan_sha256'] = fingerprint(plan); authority['previous_authority'] = meta['authority']
a = atomic(dest / 'authority.json', authority)
q = dest / 'queue'; q.mkdir()
for key,row in state['jobs'].items():
    cost = read_pin(ref(Path(row['attempt']) / 'cost.json'))
    atomic(q / key / 'attempt-inherited' / 'cost.json', cost)
    if key in changed:
        continue
    assert row['state'] == 'VERIFIED'
    append(q / 'events.jsonl', dict({k:v for k,v in row.items() if k != 'utc'},
           inherited_event_utc=row['utc'], inherited_from=meta['plan']))
start = read_pin(ref(old / 'queue/budget-start.json')); start['plan_sha256'] = fingerprint(plan)
atomic(q / 'budget-start.json', start)
atomic(dest / 'metadata.json', dict(meta, plan=p, authority=a, prior_metadata=ref(old / 'metadata.json')))
atomic(dest / 'continuation.json', {'only_rerun': 'TT CIRCA metadata current', 'prior_output_preserved': True,
       'same_method_config_source': True, 'DEV_labels_already_viewed': True, 'test_opened': False})
r = subprocess.run([MAIN, '-B', str(OUT / 'scripts/p7.py'), 'run', '--plan', p['path'], '--sha256', p['sha256'],
                    '--authority', a['path'], '--authority-sha256', a['sha256']], env=ENV, capture_output=True)
atomic(dest / 'launch.json', {'exit_code': r.returncode, 'stdout': r.stdout.decode('utf-8'), 'stderr': r.stderr.decode('utf-8')})
print(r.stdout.decode('utf-8')); print(r.stderr.decode('utf-8')); r.check_returncode()
