"""Một ca TT dev để kiểm môi trường/chi phí P7 local; không đọc test."""
import subprocess
import time
from common import ROOT, RUN, digest, event, metadata, pin, read, save, timing
from p3 import runner, selector, danh_gia


def groups(record):
    return [b['groups'] for b in danh_gia.khoi_tu_ban_ghi(record)]


def main():
    start = time.perf_counter()
    target = RUN / 'baseline-local-001'
    target.mkdir()
    assert subprocess.check_output(['git','-C','D:/RCA-ext/src/RCAEval','rev-parse','HEAD'],text=True).strip().startswith('259ea41')
    assert not subprocess.check_output(['git','-C','D:/RCA-ext/src/RCAEval','status','--porcelain','--untracked-files=no'])
    es, _, _ = metadata()
    job = es[53]['job']
    assert job['dataset'] == 'RE2-TT' and job['window'] == 'that'
    source = read('results/T-024/cham-a.json')['methods']
    allow = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
    rows = []
    methods = [('baro','baro'),('simplerca','simplerca'),('microrank','microrank_full'),
               ('tracerca','tracerca'),('circa','circa_ols_da'),('torai_B','torai_B')]
    save(target / 'plan.json', {'job': job, 'methods': methods, 'timeout_per_method_seconds': 180,
           'max_method_seconds': 1080, 'TORAI_seed': 0, 'source_code': 'RCAEval 259ea41 clean',
           'baseline_envs': runner.ENVS, 'scientific_source': 'P3 variant, no test opened'})
    for method, name in methods:
        event('baseline_local_start', method=method)
        begin = time.perf_counter()
        old_ref = next(r for r in source[name]['source_records'] if r['opaque_id'] == job['opaque_id'] and
                      (method != 'torai_B' or r['seed'] == 0))
        pin(old_ref['path'], old_ref)
        old = read(old_ref['path'])
        try:
            records = runner.chay_luot(allow, job['opaque_id'], method, 'a', job['t'], target,
                180, repo_root=ROOT, seed=0 if method == 'torai_B' else None,
                hashseed=0, model='ols' if method == 'circa' else None, config_id='T052-local-pilot')
            actual = records[0]
            match = actual['status'] == old['status'] and groups(actual) == groups(old)
            row = timing('baseline_method', begin, method=method, status=actual['status'],
                         ordered_ties_match_source=match, source=old_ref['path'], cost=actual['cost'])
        except Exception as exc:
            row = timing('baseline_method', begin, method=method, execution_error=repr(exc),
                         ordered_ties_match_source=False)
        save(target / (method + '-summary.json'), row)
        rows.append(row)
        event('baseline_local_result', method=method, match=row['ordered_ties_match_source'], seconds=row['elapsed_seconds'])
    save(target / 'summary.json', timing('baseline_local', start, PASS=all(r['ordered_ties_match_source'] for r in rows),
          comparisons=rows, not_test_ETA=True,
          limits='Một ca TT/seed0; không phải trần cho mọi ca/ba seed, OB hoặc 60 cửa sổ C-e.'))


if __name__ == '__main__': main()
