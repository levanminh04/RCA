"""Đóng snapshot rồi mới ghép nhãn DEV từ G1, xuất bảng và đo thời gian."""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-003'
sys.path.insert(0, str(OUT / 'scripts'))
from bien_nhan import atomic, fingerprint, read_pin, ref
from dieu_phoi import status
from cham import snapshot_from_status, verify_snapshot, evaluate
from nguon import original_dev_labels, compare_labels

dest = RUN / (sys.argv[1] if len(sys.argv) > 1 else 'pilot-local-007')
meta = read_pin(ref(dest / 'metadata.json'))
plan = read_pin(meta['plan'])
state = status(dest / 'queue')
assert state['controller'] is None, 'chưa kết thúc pilot'
assert len(state['jobs']) == len(plan['jobs']), 'còn job chưa phát'
assert all(s['state'] == 'VERIFIED' for s in state['jobs'].values()), 'có nhánh chặn, chưa xuất bảng'
snapshot = snapshot_from_status(plan, state)
records = verify_snapshot(snapshot, plan['jobs'])
snapshot_ref = atomic(dest / 'sealed-snapshot.json', snapshot)
runtimes = {ds: read_pin(pin) for ds, pin in meta['runtime_refs'].items()}
aliases = {ds: {} for ds in runtimes}
labels = {}; canonical = {}
for ds, runtime in runtimes.items():
    private = Path(meta['runtime_refs'][ds]['path']).parent
    prefix = 'TT' if ds == 'RE2-TT' else 'OB'
    descriptor = {'schema': 'T054-DEV-LABEL-ORIGINALS-1',
                  'source_descriptor': read_pin(meta['original_refs'][ds])}
    canonical_path = private / (prefix + '-canonical-label-source.json')
    if canonical_path.exists():
        canonical[ds] = ref(canonical_path)
        assert read_pin(canonical[ds]) == descriptor
    else:
        canonical[ds] = atomic(canonical_path, descriptor)
    trusted = original_dev_labels(descriptor, aliases[ds])
    local = {'dataset': ds, 'g1_revision': runtime['g1_revision'],
             'alias_sha256': fingerprint(aliases[ds]),
             'cases': {oid: trusted['by_member'][row['member_sha256']] for oid, row in runtime['cases'].items()}}
    compare_labels(local, descriptor, runtime, aliases[ds], plan['inventories'][ds])
    label_path = private / (prefix + '-labels.json')
    if label_path.exists():
        labels[ds] = ref(label_path)
        assert read_pin(labels[ds]) == local
    else:
        labels[ds] = atomic(label_path, local)
report = OUT / 'reports' / (sys.argv[2] if len(sys.argv) > 2 else 'pilot-local-002')
report.mkdir(exist_ok=False)
before = time.perf_counter()
evaluate(snapshot, plan, labels, canonical, runtimes, aliases, plan['inventories'], report)
score_s = time.perf_counter() - before
groups = {}; costs = []; status_rows = []; prep = {}
for job in plan['jobs']:
    key = fingerprint(job['slot']); row = state['jobs'][key]
    attempt = Path(row['attempt']); cost = read_pin(ref(attempt / 'cost.json'))
    ds, arm = job['slot']['dataset'], job['slot']['arm']
    group = ds + '|' + arm
    groups.setdefault(group, []).append(cost['wall_s'])
    costs.append(cost['wall_s'])
    status_rows.append({'dataset': ds, 'arm': arm, 'seed': job['slot']['seed'],
                        'status': [r.get('status') for r in records[key]], 'cost_s': cost['wall_s']})
    if job['kind'] == 'torai_pipeline':
        doc = read_pin(ref(attempt / 'prepare/prepared.json'))
        prep.setdefault(arm, []).append({'seed': job['slot']['seed'],
             'tables': {k: v['sha256'] for k, v in doc['tables'].items()},
             'normalized_input_sha256': doc['normalized_input_sha256'], 'prepared_ref': ref(attempt / 'prepare/prepared.json')})
prep_checks = {}
for arm, rows in prep.items():
    prep_checks[arm] = {'all_three_seeds': sorted(r['seed'] for r in rows) == [0, 1, 2],
                       'byte_equal': all(len({r['tables'][k] for r in rows}) == 1 for k in rows[0]['tables']),
                       'normalized_equal': len({r['normalized_input_sha256'] for r in rows}) == 1,
                       'rows': rows}
start = read_pin(ref(dest / 'queue/budget-start.json'))
summary = {'status': 'LOCAL_TWO_CASE_PIPELINE_COMPLETED_NOT_FULL_PILOT_COVERAGE',
   'plan': meta['plan'], 'snapshot': snapshot_ref, 'slots': len(plan['jobs']),
   'DEV_cases': {ds: len(r['cases']) for ds, r in runtimes.items()},
   'method_statuses': status_rows, 'group_wall_s': groups, 'sum_attempt_wall_s': sum(costs),
   'elapsed_since_original_start_s': time.time() - start['started_epoch'],
   'score_s': score_s, 'prep_parity_local': prep_checks,
   'main_ETA': None, 'main_ETA_status': 'not enough case/concurrency/cold-warm coverage',
   'test_opened': False, 'A_scope': 'one explicitly granted DEV case only',
   'remaining': ['source parity per actual field/variant', 'C-e and help/harm branch coverage',
                 'throughput at 2/3 workers and full plan', 'declared scientific policies and G3/main grants']}
atomic(dest / 'summary.json', summary)
print(json.dumps({'status': summary['status'], 'slots': len(plan['jobs']),
                  'sum_attempt_wall_s': sum(costs), 'prep_parity': {k: {a: b for a, b in v.items() if a != 'rows'} for k,v in prep_checks.items()},
                  'report': str(report), 'test_opened': False}))
