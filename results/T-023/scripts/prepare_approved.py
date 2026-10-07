"""Promote only the human-approved frozen proposal; metadata only, no archive."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-023'
QUOTE = 'Duyệt phương án chia phiên Eadro-TT trong results/T-023/de-xuat-chia-phien.md: 3 phiên dev, 6 phiên test, reference 2022-04-21T105158, control 2022-04-21T153246, phiên 2022-04-20 không nhãn bị loại; seed 20261004; đúng 145 member trong allowlist-phien.json. Cho đọc metric/trace/log của đúng 5 phiên này, kèm các điều kiện dưới đây.'


def load(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))


def save(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    run = OUT / 'runs/approval-001'
    run.mkdir(exist_ok=False)
    p = OUT / 'allowlist-phien.json'
    original = p.read_bytes()
    a = json.loads(original)
    assert a['status'] == 'proposed' and a['approved_sessions'] == []
    assert a['seed'] == 20261004
    approved = a['proposed_sessions']
    assert len(approved) == 5 and sum(len(x['members']) for x in approved) == 145
    assert [x['role'] for x in approved].count('dev') == 3
    (run / 'allowlist-before.json').write_bytes(original)
    raw = [x for x in load('results/T-009/runs/inspect-004/raw-sessions.json') if x['dataset'] == 'TT']
    # One representation per logical session; nested duplicate is never opened.
    unique = {}
    for x in raw:
        s = x['case'].split('/')[-1]
        if s not in unique or x['origin'] == 'outer':
            unique[s] = x
    events = list(csv.DictReader((OUT / 'runs/metadata-001/events.csv').open(encoding='utf-8-sig')))
    bounds = []
    population = []
    roles = {x['session']: x['role'] for x in approved}
    roles.update({s: 'test' for s in a['test_sessions']})
    roles.update({s: 'unlabelled' for s in a['unlabelled_sessions']})
    normals = load('results/T-009/runs/run-001/normal_intervals.json')
    for s, role in roles.items():
        x = unique[s]
        mstart = min(m['time_min'] for m in x['metrics'])
        mend = max(m['time_max'] for m in x['metrics'])
        ev = [e for e in events if e['session'] == s]
        label = [n for n in normals if n['dataset'] == 'TT' and s in n['source'].replace('.fault-', '.')]
        starts = [mstart] + [float(e['session_start_s']) for e in ev] + [n['start'] for n in label]
        ends = [mend] + [float(e['session_end_s']) for e in ev] + [n['end'] for n in label]
        bounds.append({'session': s, 'role': role, 'start_s': min(starts), 'end_s': max(ends),
                       'metric_start_s': mstart, 'metric_end_s': mend})
        population.append({'session': s, 'role': role, 'span_count_before_B1': x['trace']['counts']['spans'],
                           'source': 'results/T-009/runs/inspect-004/raw-sessions.json'})
    a.update(status='approved', approved_by='Minh', approved_at='2026-10-05', approval_quote=QUOTE,
             approved_sessions=approved, proposed_sessions=[])
    a['B1'] = {'declared_before_raw': 'results/T-023/ke-hoach-kiem.md section 8',
               'hypotheses_seconds': {'H0': 0, 'H+8': 28800, 'H-8': -28800},
               'intervals': bounds, 'closed_boundaries': True,
               'span_policy': 'reject any [start,start+duration] overlap with test/unlabelled under any H',
               'log_policy': 'timestamp prefix gate before service/message semantic decode',
               'denied_output': 'counts by interval/hypothesis only; unknown_clock count; no content/ID/service/latency',
               'unknown_clock': 'deny', 'clock_alignment': 'forbidden'}
    a['reference_check'] = 'whole reference vs control and all predeclared Q64 dev pre-intervals; no clean-segment selection'
    a['note'] = 'Approved member framing only; record contents additionally restricted by B1. Labels audit only.'
    save(p, a)
    save(run / 'allowlist-after.json', a)
    save(run / 'population-metadata.json', population)
    save(run / 'verification.json', {'PASS': True, 'seed_unchanged': True,
          'split_and_member_objects_unchanged': a['approved_sessions'] == json.loads(original)['proposed_sessions'],
          'test_unchanged': a['test_sessions'] == json.loads(original)['test_sessions'],
          'unlabelled_unchanged': a['unlabelled_sessions'] == json.loads(original)['unlabelled_sessions'],
          'approved_members': 145, 'before_sha256': hashlib.sha256(original).hexdigest(),
          'plan_sha256_before_raw': hashlib.sha256((OUT / 'ke-hoach-kiem.md').read_bytes()).hexdigest()})
    print('approval-001: PASS, five sessions, 145 unchanged members; no archive opened')
