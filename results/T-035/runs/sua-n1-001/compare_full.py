"""So bản sửa với đầu ra cũ đã kiểm manifest; không đọc raw ngoài runner."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
OUT = ROOT / 'results/T-035'


def read(path):
    return json.loads(path.read_text('utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    current = read(BASE / 'day-du-002/summary.json')
    old = read(OUT / 'runs/day-du-001/summary.json')
    previous_manifest = read(BASE / 'before/results/T-035/manifest.json')
    expected_hash = {x['path']: x['sha256'] for x in previous_manifest['files']}
    assert sha(OUT / 'runs/day-du-001/summary.json') == expected_hash['results/T-035/runs/day-du-001/summary.json']
    assert current['status'] == old['status'] == 'PASS'
    old_cases = {(x['dataset'], x['opaque_id']): x for x in old['cases']}
    assert len(current['cases']) == len(old_cases) == 52
    assert {(x['dataset'], x['opaque_id']) for x in current['cases']} == set(old_cases)
    rows = []
    for case in current['cases']:
        key = (case['dataset'], case['opaque_id'])
        before = old_cases[key]
        comparisons = {}
        # Chỉ thời gian/chi phí máy có thể khác; mọi nội dung kết quả phải bằng nhau.
        for field in sorted(set(case) | set(before)):
            if field in ('steps_s', 'seconds', 'peak_rss_bytes'):
                continue
            left, right = case.get(field), before.get(field)
            if field == 'windows':
                left = {k: {a: b for a, b in v.items() if a != 'seconds'} for k, v in left.items()}
                right = {k: {a: b for a, b in v.items() if a != 'seconds'} for k, v in right.items()}
            comparisons[field] = left == right
        rows.append({'dataset': key[0], 'opaque_id': key[1], 'fields_equal': comparisons,
                     'pass': all(comparisons.values()), 'windows': len(case['windows']),
                     'checks_pass': all(all(c[k] for k in ['K1', 'K2_repeat', 'K4', 'K5']) for c in case['checks'])})
    graphs = []
    edge_types = set()
    for path in sorted((OUT / 'do-thi').rglob('*.json')):
        relative = path.relative_to(ROOT).as_posix()
        assert sha(path) == expected_hash[relative], relative
        new = BASE / 'day-du-002/do-thi' / path.relative_to(OUT / 'do-thi')
        equal = new.is_file() and path.read_bytes() == new.read_bytes()
        graph = read(path)
        edge_types.update(e['type'] for e in graph['edges'])
        graphs.append({'old': relative, 'new': new.relative_to(ROOT).as_posix(),
                       'level': graph['level'], 'byte_equal': equal})
    progress = [json.loads(line) for line in (BASE / 'day-du-002/progress.jsonl').read_text('utf-8').splitlines()]
    assert not any(x['stage'] == 'reused' for x in progress)
    result = {'created_utc': datetime.now(timezone.utc).isoformat(), 'cases': rows, 'graphs': graphs,
              'case_count': len(rows), 'window_count': sum(x['windows'] for x in rows),
              'graph_count': len(graphs), 'edge_types': sorted(edge_types),
              'graph_byte_equal': all(x['byte_equal'] for x in graphs),
              'case_semantics_equal': all(x['pass'] for x in rows),
              'all_K1_K2_K4_K5': all(x['checks_pass'] for x in rows),
              'reused_cases': 0, 'seconds': current['seconds'],
              'peak_rss_bytes': max(x['peak_rss_bytes'] for x in current['cases'])}
    result['pass'] = result['graph_byte_equal'] and result['case_semantics_equal'] and result['all_K1_K2_K4_K5']
    with (BASE / 'comparison.json').open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in result.items() if k not in ['cases', 'graphs']}, ensure_ascii=False))
    assert result['pass'], 'regression_changed'


if __name__ == '__main__':
    main()
