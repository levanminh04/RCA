"""Đối chiếu trường khoa học từ record đã verify; không chấm nhãn test."""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
sys.path.insert(0, str(OUT / 'scripts'))
from bien_nhan import atomic, fingerprint, read_pin, ref
from dieu_phoi import status, verify_attempt
from pilot import reference, comparable

MAP = {'C-a0': 'K-R0', 'C-a1': 'K-E1', 'M1': 'K-E1+E2+E5',
       'bo-E1': 'K-E2+E5', 'bo-E2': 'K-E1+E5', 'bo-E5': 'K-E1+E2'}


def differences(a, b, path='', limit=100):
    out = []
    if type(a) is not type(b):
        return [{'path': path, 'kind': 'type', 'left': type(a).__name__, 'right': type(b).__name__}]
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append({'path': path + '/' + k, 'kind': 'missing_left' if k not in a else 'missing_right'})
            else:
                out.extend(differences(a[k], b[k], path + '/' + k))
            if len(out) >= limit:
                break
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append({'path': path, 'kind': 'length', 'left': len(a), 'right': len(b)})
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                out.extend(differences(x, y, path + '/' + str(i)))
                if len(out) >= limit:
                    break
    elif a != b:
        out.append({'path': path, 'kind': 'value', 'left': str(a)[:150], 'right': str(b)[:150]})
    return out[:limit]


def inspect(dest):
    plan = read_pin(ref(dest / 'plan.json'))
    state = status(dest / 'queue')
    candidates = read_pin(ref(OUT / 'runs/trien-khai-003/before-files/pilot-plan.json'))['candidates']
    baseline = read_pin(ref(OUT / 'runs/trien-khai-002/pilot-proposal.json'))['baseline_jobs']
    results = []
    for job in plan['jobs']:
        slot = job['slot']; key = fingerprint(slot); observed = state['jobs'].get(key)
        row = {'slot': {k: slot[k] for k in ('dataset', 'opaque_id', 'arm', 'seed')},
               'state': observed['state'] if observed else 'PENDING'}
        if row['state'] != 'VERIFIED':
            row['reason'] = observed.get('reason') if observed else None
            results.append(row); continue
        records = verify_attempt(Path(observed['attempt']), job, observed['token'])
        row['attempt'] = observed['attempt']; row['cost'] = read_pin(ref(Path(observed['attempt']) / 'cost.json'))
        expected = None
        if slot['arm'] in MAP:
            cand = next(c for c in candidates if c['opaque_id'] == slot['opaque_id'] and c['window'] == 'that')
            expected = reference(cand['native_record'], MAP[slot['arm']])
            row['reference'] = cand['native_record']; row['native_config'] = MAP[slot['arm']]
        elif job['kind'] in ('baseline', 'torai_pipeline'):
            refs = [b['source_ref'] for b in baseline if all(b[k] == slot[k] for k in ('dataset', 'opaque_id', 'arm', 'seed'))]
            if len(refs) == 1:
                expected = read_pin(refs[0]); row['reference'] = refs[0]
                if slot['arm'] == 'circa':
                    row['circa_extra_record_count'] = len(records) - 1
        row['statuses'] = [r.get('status') for r in records]
        if expected is not None:
            # Chỉ metadata run/config ID bỏ ra theo comparator đã có; giữ mọi trường khoa học để trình diff.
            a = comparable(expected, control=slot['arm'] in ('C-a0', 'C-a1'))
            b = comparable(records[0], control=slot['arm'] in ('C-a0', 'C-a1'))
            row['exact_comparable'] = a == b
            row['differences'] = differences(a, b)
        else:
            row['comparison'] = 'NEEDS_SPECIFIC_REFERENCE_OR_DERIVED_CHECK'
        results.append(row)
    return {'status': 'LIVE_DIAGNOSTIC_NOT_ACCEPTANCE', 'slots': results,
            'controller': state['controller'], 'wait': state['wait'], 'test_opened': False}


if __name__ == '__main__':
    dest = Path(sys.argv[1]).resolve()
    result = inspect(dest)
    if len(sys.argv) > 2:
        target = dest / sys.argv[2]
        assert not target.exists()
        atomic(target, result)
    print(json.dumps(result, ensure_ascii=False))
