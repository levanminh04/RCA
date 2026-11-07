"""Kiểm tuyến baseline v2 trên hai ca dev đã chạy trước. Chỉ gọi sau quyền chạy F3."""
import time

from common import ROOT, RUN, metadata, pin, read, save
from p3 import danh_gia, nezha, selector
from p7_entry_v2 import METHODS, run_baseline

SCORED_NAMES = {'microrank': 'microrank_full', 'circa': 'circa_ols_da'}


def ranking(record):
    return [b['groups'] for b in danh_gia.khoi_tu_ban_ghi(record)]


def window_match(actual, expected):
    a, b = actual['window'], expected['window']
    if a is None or b is None:
        return a is b
    return all(k in a and a[k] == v for k, v in b.items()
               if k in ('t', 'N', 'A', 't_ns', 'N_ns', 'A_ns', 'trace_guard_s'))


def main():
    start = time.monotonic()
    out = RUN / 'pilot-f3-v2-001'
    out.mkdir()
    inputs = read('results/T-052/manifest.json')['upstream_inputs_verified']
    pins = {r['path']: r for r in inputs}
    entries, _, _ = metadata()
    comparisons = []
    for dataset, index, source_path in [('RE2-TT', 53, 'results/T-024/cham-a.json'),
                                        ('Nezha-OB', 62, 'results/T-026/cham-a.json')]:
        job = entries[index]['job']
        assert job['dataset'] == dataset and job['window'] == 'that'
        oid = job['opaque_id']
        pin(source_path, pins[source_path])
        source = read(source_path)
        if dataset == 'RE2-TT':
            allow = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
            selected = selector.chon_ca(allow, oid, ROOT)
            source_meta = allow[oid]['files']
            methods = source['methods']
        else:
            allow = nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json')
            selected = nezha.chon_ca(allow, oid, ROOT)
            source_meta = selected['files']
            methods = source['tables']['main']['methods']
        for method in METHODS:
            seed = 0 if method == 'torai_B' and dataset == 'RE2-TT' else None
            refs = methods[SCORED_NAMES.get(method, method)]['source_records']
            expected = []
            for ref in refs:
                if ref['opaque_id'] == oid:
                    pin(ref['path'], ref)
                    candidate = read(ref['path'])
                    if candidate.get('seed') == seed:
                        expected.append(candidate)
            assert len(expected) == 1, (dataset, method)
            reference = expected[0]
            budget = min(180, 600 - (time.monotonic() - start))
            if budget <= 0:
                raise RuntimeError('hết trần pilot F3; giữ các lượt đã có')
            run_dir = out / (dataset + '-' + method)
            candidates = run_baseline(dataset, selected, source_meta, oid, method, run_dir, budget, t=job['t'], seed=seed)
            actual, = [r for r in candidates if r['variant'] == reference['variant']]
            checks = {'status': actual['status'] == reference['status'],
                      'ordered_ties': ranking(actual) == ranking(reference), 'window': window_match(actual, reference),
                      'input': actual['input_sha256'] == reference['input_sha256']}
            result = {'dataset': dataset, 'method': method, 'seed': seed, 'checks': checks, 'PASS': all(checks.values())}
            comparisons.append(result)
            save(run_dir / 'compare.json', result)
    save(out / 'summary.json', {'PASS': all(r['PASS'] for r in comparisons), 'elapsed_s': time.monotonic() - start,
                                'comparisons': comparisons})
    if not all(r['PASS'] for r in comparisons):
        raise RuntimeError('tuyến v2 chưa tương đương nguồn trên pilot F3')


if __name__ == '__main__':
    main()
