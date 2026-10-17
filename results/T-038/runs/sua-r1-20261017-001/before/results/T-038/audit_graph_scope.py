"""Kiểm miền graph T-035 đã lưu; tuyệt đối không mở dữ liệu thô."""
import collections
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))


def sha(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def main():
    out = ROOT / 'results/T-038/runs' / sys.argv[1]
    out.mkdir(parents=True, exist_ok=False)
    (out / 'audit_graph_scope.py').write_bytes(Path(__file__).read_bytes())
    result = {'task': 'T-038', 'raw_telemetry_opened': False,
              'command': 'py -3 -X utf8 -B results/T-038/audit_graph_scope.py ' + sys.argv[1]}
    try:
        manifest = {x['path']: x for x in load('results/T-035/manifest.json')['files']}

        def verified(name):
            row = manifest[name]
            assert sha(name) == row['sha256'] and (ROOT / name).stat().st_size == row['bytes']
            return load(name)

        checks = verified('results/T-035/runs/sua-hop-dong-001/input-verification.json')['checks']
        for index in [331, 352]:
            assert checks[index]['pass'] and sha(checks[index]['path']) == checks[index]['expected']
        allow = load(checks[331]['path'])
        # Chỉ lấy opaque ID và hash metadata, không chuyển case_dir/nhãn vào phương pháp.
        summary = verified('results/T-035/runs/sua-hop-dong-001/day-du-001/summary.json')
        prefix = 'results/T-035/do-thi/RE2-TT/'
        paths = sorted(p for p in manifest if p.startswith(prefix))
        assert set(paths) == {p.relative_to(ROOT).as_posix() for p in (ROOT / prefix).rglob('*.json')}
        ids = {p[len(prefix):].split('/')[0] for p in paths}
        tt = [x for x in summary['cases'] if x['dataset'] == 'RE2-TT']
        assert ids == {x['opaque_id'] for x in tt}
        allowed = {x['opaque_id']: x for x in allow['cases']}
        assert {x['opaque_id'] for x in tt} <= set(allowed)
        result['source_domains'] = [{'opaque_id': x['opaque_id'],
                                     'domain': x['provenance']['domain']}
                                    for x in tt]
        assert all(x['domain'] == 'whole_dev_trace_table' for x in result['source_domains'])
        counts, types = collections.Counter(), collections.Counter()
        nodes = collections.defaultdict(set)
        shapes = collections.defaultdict(set)
        intervals = {}
        for path in paths:
            graph = verified(path)
            dev, level, filename = path[len(prefix):].split('/')
            assert graph['level'] == {'thuc-the': 'entity', 'thao-tac': 'operation'}[level]
            family = filename.split('-')[0].removesuffix('.json')
            counts[(level, family)] += 1
            shapes[level].add(tuple(sorted(graph)))
            nodes[level].update(n['id'] for n in graph['nodes'])
            types.update(e['type'] for e in graph['edges'])
            intervals[(dev, level, filename)] = graph['interval_ns']
            if family == 'full':
                assert graph['interval_ns'] is None
            else:
                lo, hi = graph['interval_ns']
                assert hi - lo == (60 if family == 's60' else 300) * 10**9
        for dev in ids:
            for level in ['thuc-the', 'thao-tac']:
                assert intervals[(dev, level, 'N.json')][1] == intervals[(dev, level, 'A.json')][0]
            for filename in ['full.json', 'N.json', 'A.json']:
                assert intervals[(dev, 'thuc-the', filename)] == intervals[(dev, 'thao-tac', filename)]
        result.update(ok=True, graph_count=len(paths), total_graph_bytes=sum(manifest[p]['bytes'] for p in paths),
                      opaque_dev_count=len(ids), by_level_family=[{'level': a, 'family': b, 'count': n}
                           for (a, b), n in sorted(counts.items())],
                      distinct_observed_nodes={k: len(v) for k, v in nodes.items()},
                      edge_type_occurrences=dict(types), shapes={k: list(v) for k, v in shapes.items()},
                      metadata_links=[checks[i] for i in [331, 352]],
                      cost_note='Không là phép đo đối chiếu T-038; không suy thời gian/RAM từ kiểm hash.')
    except BaseException as exc:
        result.update(ok=False, error=repr(exc))
        raise
    finally:
        (out / 'graph-scope.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({k: v for k, v in result.items() if k in ['ok', 'error', 'graph_count', 'opaque_dev_count',
                          'total_graph_bytes', 'distinct_observed_nodes', 'edge_type_occurrences']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
