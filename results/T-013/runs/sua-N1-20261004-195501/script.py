"""Focused verification of the approved N1/N2/N3 corrections.

Loads function definitions only, keeps historical runs, and compares against
the untouched pinned author/sklearn code. Never reruns the full task.
"""
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
import argparse
import ast
import csv
import datetime
import hashlib
import importlib
import json
import sys
import time
from functools import partial
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

ROOT = Path('D:/RCA-flashticket')
OUT = ROOT / 'results/T-013'
parser = argparse.ArgumentParser()
parser.add_argument('--run', required=True)
args = parser.parse_args()
RUN = Path(args.run).resolve()
assert RUN.is_relative_to(OUT / 'runs') and RUN.is_dir()
START = time.perf_counter()
checks, ledger = [], []


def safe(value):
    if isinstance(value, dict):
        return {str(k): safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [safe(v) for v in value]
    if hasattr(value, 'item'):
        return safe(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return 'NaN' if np.isnan(value) else ('Infinity' if value > 0 else '-Infinity')
    return value


def dump(path, value):
    path.write_text(json.dumps(safe(value), ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def progress(event, **values):
    item = {'time': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat(),
            'elapsed_shared_machine_s': time.perf_counter() - START, 'event': event, **values}
    with (RUN / 'tien-do.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(safe(item), ensure_ascii=False) + '\n')
    print(event, safe(values), flush=True)


def record(case, source, method, purpose, reason):
    ledger.append({'ca': case, 'file_nguon': str(source), 'phuong_phap': method,
                   'muc_dich': purpose, 'ly_do': reason})


def finish_check(name, **values):
    checks.append({'check': name, 'status': 'pass', **values})
    dump(RUN / 'checks.json', checks)


def load_functions(path, scope):
    names = {'clean', 'indep_pre', 'independent_standard_params', 'independent_rank', 'official_rank', 'services'}
    tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    module = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[])
    exec(compile(module, str(path) + ':functions-only', 'exec'), scope)
    return scope


def metric_error(left, right):
    return abs(left - right) / max(1., abs(right))


def test():
    progress('start', scope='N1 focused synthetic + two old examples; N2/N3 conditions')
    sys.path.insert(0, 'D:/RCA-ext/src/baro')
    sys.path.insert(0, 'D:/RCA-ext/src/RCAEval')
    br = importlib.import_module('baro.root_cause_analysis')
    re = importlib.import_module('RCAEval.e2e.baro')
    reinit = importlib.import_module('RCAEval.e2e')
    bc = importlib.import_module('baro._bocpd')
    scope = load_functions(OUT / 'scripts/kiem_co_che.py', {'np': np, 'pd': pd, 'br': br, 're': re, 'reinit': reinit})
    old_scope = load_functions(RUN / 'truoc-kiem_co_che.py', {'np': np, 'pd': pd})
    samples = {
        'reported-near-constant': (1e16 + np.arange(6)*2., 1e16 + np.arange(6, 12)*2.),
        'ordinary': (np.arange(6, dtype=float), np.arange(6, 12, dtype=float)),
        'exact-constant': (np.full(6, 7.), np.arange(6, 12, dtype=float)),
        'above-near-constant-bound': (1e16 + np.arange(6)*128., 1e16 + np.arange(6, 12)*128.),
        'tiny-centered-scale': (np.array([-3., -2., -1., 1., 2., 3.])*1e-20, np.arange(6.)*1e-20),
        'missing-samples': (np.array([np.nan, 1., 2., np.nan, 4., 5.]), np.arange(6.)+6),
        'missing-near-constant': (np.array([np.nan, 1e16, 1e16+2, 1e16+4, 1e16+6, 1e16+8]), 1e16+np.arange(6)*2+10),
        'small-variance-large-offset': (1e12 + np.arange(20)*1e-3, 1e12 + np.arange(20, 40)*1e-3),
    }
    for name, (normal, post) in samples.items():
        progress('synthetic_start', case=name)
        record('synthetic', 'generated', 'N-Sigma independent + pinned StandardScaler', name, 'c')
        mean, var, scale = scope['independent_standard_params'](normal)
        official = StandardScaler().fit(normal[:, None])
        assert metric_error(mean, official.mean_[0]) <= 1e-14
        assert metric_error(var, official.var_[0]) <= 1e-12
        assert metric_error(scale, official.scale_[0]) <= 1e-12
        predicted = (post - mean)/scale
        expected = official.transform(post[:, None])[:, 0]
        assert np.max(np.abs(predicted-expected)/np.maximum(1, np.abs(expected))) <= 1e-10
        if name == 'reported-near-constant':
            d = pd.DataFrame({'time': np.arange(12), 'a_cpu': np.r_[normal, post]})
            old_rows, _ = old_scope['independent_rank'](d, 6, 'standard', 're', 'fse-ob')
            new_rows, _ = scope['independent_rank'](d, 6, 'standard', 're', 'fse-ob')
            assert old_rows[0]['score'] != float(expected.max())
            assert new_rows[0]['score'] == float(expected.max()) == 18.
            finish_check('N1-original-counterexample-fixed', old_score=old_rows[0]['score'], new_score=new_rows[0]['score'], official_score=float(expected.max()), scale=scale)
        finish_check('N1-params-' + name, mean=mean, variance=var, raw_std=float(np.sqrt(var)), scale=scale,
                     official_mean=official.mean_[0], official_variance=official.var_[0], official_scale=official.scale_[0],
                     max_normalized_transform_error=float(np.max(np.abs(predicted-expected)/np.maximum(1, np.abs(expected)))))

    summary = json.loads((OUT / 'kiem-tra.json').read_text(encoding='utf-8'))
    old_run = Path(summary['run_dir'])
    source_cases = summary['selection']['selected']
    metric_count = 0
    for case in source_cases:
        tag = case['tag']; source = Path(case['source']); inj = case['inject_time']
        if tag == 'TT':
            with np.load('D:/RCA-ext/work/T-013/metrics-selected.npz', allow_pickle=False) as data:
                raw = pd.DataFrame(data['values'], columns=data['columns'].tolist())
        else:
            raw = pd.read_csv(source)
        raw = scope['clean'](raw)
        dataset = 're2-tt' if tag == 'TT' else 'fse-ob'
        for length in [10, 20]:
            window = pd.concat([raw[raw.time < inj].tail(length*30), raw[raw.time >= inj].head(length*30)], ignore_index=True)
            for kind in ['re', 'br']:
                name = f'{tag}-L{length}-standard-{kind}'
                progress('actual_start', case=case['case'], name=name, shape=list(window.shape))
                record(case['case'], source, f'{kind} N-Sigma RCA', 'verify corrected helper ' + name, 'c')
                independent, ranks = scope['independent_rank'](window, inj, 'standard', kind, dataset)
                official, observed = scope['official_rank'](window, inj, 'standard', kind, dataset)
                assert ranks == official['ranks']
                assert independent
                for row in independent:
                    row['official_score'] = observed[row['metric']]['score']
                    row['abs_error'] = abs(row['score'] - row['official_score'])
                    assert metric_error(row['score'], row['official_score']) <= 1e-10
                # Historical points are retained. Check any numerical differences,
                # and require the old rank to remain unchanged.
                suffix = '-BR' if kind == 'br' else ''
                historical = pd.read_csv(old_run / f'{tag}-L{length}-standard{suffix}-metric.csv')
                old_scores = dict(zip(historical.metric, historical.score))
                assert set(old_scores) == {r['metric'] for r in independent}
                old_error = max(metric_error(r['score'], old_scores[r['metric']]) for r in independent)
                assert old_error <= 1e-10
                saved = json.loads((old_run / f'{tag}-L{length}-standard{suffix}-ranks.json').read_text(encoding='utf-8'))
                assert ranks == saved['ranks']
                repeat_rows, repeat_ranks = scope['independent_rank'](window, inj, 'standard', kind, dataset)
                assert repeat_ranks == ranks and [r['score'] for r in repeat_rows] == [r['score'] for r in independent]
                reversed_rows, reversed_ranks = scope['independent_rank'](window[list(reversed(window.columns))], inj, 'standard', kind, dataset)
                assert {r['metric']: r['score'] for r in reversed_rows} == {r['metric']: r['score'] for r in independent}
                pd.DataFrame(independent).to_csv(RUN / (name + '-metric.csv'), index=False, encoding='utf-8-sig')
                dump(RUN / (name + '-ranks.json'), {'ranks': ranks, 'official': official, 'service_ranks': scope['services'](ranks)})
                metric_count += len(independent)
                finish_check('N1-real-' + name, n_metrics=len(independent), rank_equals_official_and_historical=True,
                             max_normalized_score_error=max(metric_error(r['score'], r['official_score']) for r in independent),
                             max_normalized_historical_error=old_error, repeat_equal=True, permutation_scores_equal=True,
                             permutation_ranks_equal=reversed_ranks == ranks)
            progress('actual_window_complete', tag=tag, length=length)

    sample = pd.Series([1., 2., np.inf, np.nan])
    assert sample.count() == 3 and np.isfinite(sample).sum() == 2
    assert np.isinf(sample.mean()) and np.isnan(sample.std())
    finish_check('N2-pandas-non-NaN-not-finite', count=int(sample.count()), finite_count=int(np.isfinite(sample).sum()), mean=sample.mean(), std=sample.std())
    record('synthetic', 'generated', 'pandas N-Sigma formula', 'N2 nonfinite interpretation', 'c')

    x = np.full((1, 100), 1e4)
    probability = bc.MultivariateT(dims=100).pdf(x[0])[0]
    assert probability == 0 and np.isfinite(probability)
    posterior, _ = bc.online_changepoint_detection(x, partial(bc.constant_hazard, 50), bc.MultivariateT(dims=100))
    assert np.isnan(posterior[:, 1]).all()
    positive, _ = bc.online_changepoint_detection(np.array([[0.]]), partial(bc.constant_hazard, 50), bc.MultivariateT(dims=1))
    assert np.allclose(positive[:, 1], [.02, .98], rtol=0, atol=1e-15)
    finish_check('N3-positive-mass-condition', zero_mass=probability, zero_mass_posterior=posterior[:, 1].tolist(), positive_mass_posterior=positive[:, 1].tolist(), scope='core only; not wrapper normalization')
    record('synthetic', 'generated', 'BOCPD core', 'N3 zero versus positive mass', 'c')

    result = {'status': 'pass', 'run': str(RUN), 'checks': checks, 'real_metric_points_checked': metric_count,
              'real_cases': [c['case'] for c in source_cases], 'method_calls_scope': 'eight N-Sigma author branches on two previously selected examples; no full BOCPD or dataset benchmark',
              'seconds_shared_machine': time.perf_counter()-START, 'elapsed_is_official_benchmark': False}
    dump(RUN / 'ket-qua.json', result)
    with (RUN / 'ca-da-chay.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['ca', 'file_nguon', 'phuong_phap', 'muc_dich', 'ly_do'])
        writer.writeheader(); writer.writerows(ledger)
    progress('complete', checks=len(checks), metric_points=metric_count)


try:
    test()
except Exception as error:
    progress('failure', error=repr(error))
    dump(RUN / 'failure.json', {'error': repr(error), 'partial_checks': checks})
    raise
