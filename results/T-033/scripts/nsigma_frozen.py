"""T-033: fixed [:i_proxy] N-Sigma diagnosis from verified native intermediates.

Only EC2 executes this file. Reuse original x/mean/std/count and independently
verify them on the original-dtype Series read from hash-checked raw metrics.
Only post-proxy points are compared; this is not a selected online detector.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import resource
import shutil
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import psutil

K = 3
START = 100
CORE_RUNS = ('nsigma-first-001', 'nsigma-rest-001')
DETECTORS = ('nsigma', 'nsigma_doi_chung')
ARRAY_KEYS = ('x', 'mean', 'std', 'count', 'threshold', 'margin', 'Z',
              'columns', 'times', 'evaluated')


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                    allow_nan=False) + '\n', encoding='utf-8')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def used(home):
    return sum(path.stat().st_size for path in home.rglob('*') if path.is_file())


def progress(home, message):
    line = datetime.now(timezone.utc).isoformat() + ' NSIGMA_FROZEN ' + message
    print(line, flush=True)
    with (home / 'trang-thai.txt').open('a', encoding='utf-8') as handle:
        handle.write(line + '\n')


def update_manifest(run):
    write(run / 'manifest.json', {
        path.name: {'sha256': sha(path), 'bytes': path.stat().st_size}
        for path in sorted(run.iterdir())
        if path.is_file() and path.name != 'manifest.json'})


def budget_guard(home, source, started, projected=0):
    require(not (home / 'STOP').exists(), 'STOP user/agent')
    elapsed = (datetime.now(timezone.utc) - started).total_seconds()
    require(elapsed >= 0, 'Source first-compute timestamp is in the future')
    require(elapsed < source['budget_compute_s'],
            'BUDGET_STOP: approved total calendar budget since first compute')
    byteused = used(home)
    require(byteused + projected < source['budget_bytes'],
            'BUDGET_STOP: approved storage before write')
    free = shutil.disk_usage(home).free
    require(projected < free, 'DISK_STOP: insufficient free bytes before write')
    return {'new_bytes': byteused, 'disk_free_bytes': free,
            'ram_available_bytes': psutil.virtual_memory().available,
            'machine_elapsed_since_first_compute_s': elapsed}


def manifest_entry(run, name):
    manifest = read(run / 'manifest.json')
    require(name in manifest, 'Source manifest missing ' + str(run / name))
    meta = manifest[name]
    path = run / name
    require(path.is_file() and path.stat().st_size == meta['bytes']
            and sha(path) == meta['sha256'], 'Source manifest hash mismatch ' + str(path))
    return path, meta


def load_core(home, item, detector, source_hash):
    oid = item['opaque_id']
    name = oid + '--' + detector + '.json'
    runs = [home / 'runs' / run for run in CORE_RUNS
            if (home / 'runs' / run / name).is_file()]
    require(len(runs) == 1, 'Core unit missing/duplicate ' + oid + '/' + detector)
    run = runs[0]
    status_path, unused = manifest_entry(run, 'status.json')
    status = read(status_path)
    require(status['status'] == 'PASS', 'Core run not PASS ' + run.name)
    require(status['source_sha256'] == source_hash, 'Core source.json hash mismatch')
    meta_path, unused = manifest_entry(run, name)
    meta = read(meta_path)
    require(meta['status'] == 'PASS' and all(meta['checks'].values()),
            'Core unit checks not PASS ' + name)
    require(status['cases'][oid][detector] == meta, 'Core status/record disagree ' + name)
    require(meta['opaque_id'] == oid and meta['detector'] == detector,
            'Core identity mismatch ' + name)
    npz_name = meta['output_npz']
    require(Path(npz_name).name == npz_name, 'Core output_npz must be a basename')
    npz_path, npz_manifest = manifest_entry(run, npz_name)
    require(meta['sha256'] == npz_manifest['sha256']
            and meta['bytes'] == npz_manifest['bytes'], 'Core record/manifest disagree')
    with np.load(npz_path, allow_pickle=False) as archive:
        require(set(ARRAY_KEYS) <= set(archive.files), 'Core arrays missing')
        arrays = {key: archive[key].copy() for key in ARRAY_KEYS}
    times, columns = arrays['times'], arrays['columns']
    shape = (len(times), len(columns))
    require(times.ndim == columns.ndim == 1 and len(set(columns.tolist())) == len(columns),
            'Core times/columns schema invalid')
    require(len(times) == meta['T'] == 1441 and len(columns) == meta['max_d'],
            'Core size does not match record')
    require(np.isfinite(times).all() and np.array_equal(times, times.astype(np.int64))
            and np.all(np.diff(times) == 1), 'Core timestamp grid invalid')
    matches = np.flatnonzero(times == item['proxy'])
    require(len(matches) == 1 and int(matches[0]) == 720, 'Proxy does not resolve on source grid')
    iproxy = int(matches[0])
    require(iproxy >= START and arrays['evaluated'].dtype == np.bool_
            and np.array_equal(arrays['evaluated'], np.arange(len(times)) >= START),
            'Native evaluation start mismatch')
    for key in ('x', 'mean', 'std', 'count', 'threshold', 'margin', 'Z'):
        require(arrays[key].shape == shape, 'Core array shape mismatch ' + key)
    require(arrays['Z'].dtype == np.bool_, 'Core flags must be bool')
    expected = item['expected'][detector]
    require(expected['status'] == 'OK' and columns.tolist() == expected['detector_columns'],
            'Core expected status/columns mismatch')
    alarms = [int(t) for t in times[arrays['Z'].any(axis=1)]]
    require(alarms == expected['alarms'], 'Core merged alarms mismatch')
    require(meta['source_flags'] == item['flags'][detector], 'Core source-flags provenance mismatch')
    flags_path = home / 'inputs' / item['flags'][detector]['path']
    require(sha(flags_path) == item['flags'][detector]['sha256'], 'Frozen original flags hash mismatch')
    with np.load(flags_path, allow_pickle=False) as archive:
        for key in ('Z', 'times', 'columns'):
            require(np.array_equal(arrays[key], archive[key]), 'Original flags identity mismatch ' + key)
    require(np.array_equal(arrays['threshold'], K * arrays['std'], equal_nan=True),
            'Core threshold does not use k=3')
    require(np.array_equal(arrays['margin'],
                           np.abs(arrays['x'] - arrays['mean']) - K * arrays['std'], equal_nan=True),
            'Core margin formula mismatch')
    provenance = {'run': run.name, 'status_sha256': sha(status_path),
                  'manifest_sha256': sha(run / 'manifest.json'),
                  'record': str(meta_path.relative_to(home)), 'record_sha256': sha(meta_path),
                  'npz': str(npz_path.relative_to(home)), 'npz_sha256': meta['sha256'],
                  'core_script_sha256': status['script_sha256'],
                  'reused_arrays': list(ARRAY_KEYS), 'original_flags': item['flags'][detector]}
    return arrays, iproxy, provenance


def same_statistics(left, right):
    return {'nan_mask': bool(np.array_equal(np.isnan(left), np.isnan(right))),
            'finite_mask': bool(np.array_equal(np.isfinite(left), np.isfinite(right))),
            'finite_values': bool(np.array_equal(left[np.isfinite(left)], right[np.isfinite(right)])),
            'all_values_including_inf': bool(np.array_equal(left, right, equal_nan=True))}


def original_baseline(home, source, item, detector, arrays, iproxy):
    """Independent reduction on original-dtype pandas Series from allowlisted raw."""
    from p3.adapters import phat_hien
    preflight = home / 'runs/preflight-002'
    verification_path = preflight / 'verification.json'
    inventory_path = preflight / 'inventory.json'
    environment_path = preflight / 'environment.json'
    require(read(verification_path)['status'] == 'PASS', 'Preflight verification not PASS')
    inventory = read(inventory_path)
    require(inventory['status'] == 'PASS', 'Preflight inventory not PASS')
    require(read(environment_path)['source_json_sha256'] == sha(home / 'inputs/source.json'),
            'Preflight source.json hash changed')
    matches = [row for row in inventory['cases'] if row['opaque_id'] == item['opaque_id']]
    require(len(matches) == 1, 'Metric inventory identity missing/duplicate')
    row = matches[0]
    require(row['i_proxy'] == iproxy and row['t_proxy'] == int(item['proxy']),
            'Inventory/core proxy mapping mismatch')
    metric_path = Path(row['files']['metrics.parquet']).resolve()
    require(any(metric_path.is_relative_to(Path(p).resolve()) for p in source['source_roots_remote'])
            and 'locked' not in metric_path.parts and 'T-032' not in metric_path.parts,
            'Metric path outside approved dev source roots')
    meta = item['files']['metrics.parquet']
    require(metric_path.is_file() and metric_path.stat().st_size == meta['bytes']
            and sha(metric_path) == meta['sha256'], 'Allowlisted raw metric hash/bytes mismatch')
    require(sha(phat_hien.__file__) == source['adapter_sha256'], 'Native column-selector/adapter source changed')
    raw = pd.read_parquet(metric_path)
    columns = (phat_hien.cot_bocpd(raw.columns) if detector == 'nsigma'
               else [column for column in raw.columns if column != 'time'])
    data = raw[['time'] + columns].replace([np.inf, -np.inf], np.nan).ffill()
    checks = {
        'independent_raw_columns_exact': columns == arrays['columns'].tolist(),
        'independent_raw_time_exact': bool(np.array_equal(raw['time'].to_numpy(), arrays['times'])),
        'independent_processed_time_exact': bool(np.array_equal(data['time'].to_numpy(), arrays['times'])),
        'independent_processed_x_all_points_exact': bool(np.array_equal(
            data[columns].to_numpy(), arrays['x'], equal_nan=True))}
    require(all(checks.values()), 'Original raw/processed data identity mismatch ' + str(checks))
    mu = np.full(len(columns), np.nan)
    sd = np.full(len(columns), np.nan)
    count = np.zeros(len(columns), dtype=arrays['count'].dtype)
    first_flags = np.zeros(len(columns), dtype=bool)
    first_margin = np.full(len(columns), np.nan)
    dtypes = []
    for j, column in enumerate(columns):
        col = data[column]  # Preserve the native Series dtype; do not rebuild from arrays['x'].
        history = col.iloc[:iproxy]
        mu[j] = history.mean()
        sd[j] = history.std()  # pandas ddof=1, skipna=True, exactly native.
        count[j] = history.count()
        first_flags[j] = abs(col.iloc[iproxy] - mu[j]) > K * sd[j]
        first_margin[j] = abs(col.iloc[iproxy] - mu[j]) - K * sd[j]
        dtypes.append({'column': column, 'raw_dtype': str(raw[column].dtype),
                       'processed_dtype': str(col.dtype)})
    checks.update({'independent_mean_' + key: value
                   for key, value in same_statistics(mu, arrays['mean'][iproxy]).items()})
    checks.update({'independent_std_' + key: value
                   for key, value in same_statistics(sd, arrays['std'][iproxy]).items()})
    checks['independent_count_exact'] = bool(np.array_equal(count, arrays['count'][iproxy]))
    checks['independent_first_scalar_flags_exact'] = bool(np.array_equal(first_flags, arrays['Z'][iproxy]))
    checks['independent_first_scalar_margin_exact'] = bool(np.array_equal(
        first_margin, arrays['margin'][iproxy], equal_nan=True))
    require(all(checks.values()), 'Independent original-Series baseline/source mismatch ' + str(checks))
    baseline = {'mean': mu, 'std': sd, 'count': count,
                'first_flags': first_flags, 'first_margin': first_margin}
    provenance = {'metrics_path': str(metric_path), 'metrics_sha256': meta['sha256'],
                  'metrics_bytes': meta['bytes'], 'preflight_inventory_sha256': sha(inventory_path),
                  'preflight_verification_sha256': sha(verification_path),
                  'preflight_environment_sha256': sha(environment_path),
                  'adapter_sha256': source['adapter_sha256'], 'columns_and_dtypes': dtypes,
                  'history_definition': 'Original processed pandas Series iloc[:i_proxy], mean()/std()/count()',
                  'x_check_scope': 'All points and columns after exact native Inf->NaN + ffill',
                  'no_numeric_tolerance': True}
    return baseline, checks, provenance


def freeze(arrays, iproxy, baseline=None):
    post = np.flatnonzero(arrays['evaluated'] & (np.arange(len(arrays['times'])) >= iproxy))
    require(len(post) and int(post[0]) == iproxy, 'First post-proxy point is not i_proxy')
    # Production receives independent original-Series statistics already checked
    # against the core; fixtures may reuse their own native row as the baseline.
    mu = (baseline['mean'] if baseline is not None else arrays['mean'][iproxy]).copy()
    sd = (baseline['std'] if baseline is not None else arrays['std'][iproxy]).copy()
    count = (baseline['count'] if baseline is not None else arrays['count'][iproxy]).copy()
    threshold = K * sd
    x = arrays['x'][post]
    flags = np.abs(x - mu) > threshold  # NaN compares False; std=0 remains strict >.
    margin = np.abs(x - mu) - threshold
    mu_updated, sd_updated = arrays['mean'][post], arrays['std'][post]
    finite_stats = (np.isfinite(mu)[None, :] & np.isfinite(sd)[None, :]
                    & np.isfinite(mu_updated) & np.isfinite(sd_updated))
    contrast_defined = finite_stats & np.isfinite(x)
    checks = {'first_mean_' + k: v for k, v in same_statistics(mu, arrays['mean'][post[0]]).items()}
    checks.update({'first_std_' + k: v for k, v in same_statistics(sd, arrays['std'][post[0]]).items()})
    checks['first_count_exact'] = bool(np.array_equal(count, arrays['count'][post[0]]))
    checks['first_threshold_exact'] = bool(np.array_equal(threshold, arrays['threshold'][post[0]], equal_nan=True))
    checks['first_flags_exact'] = bool(np.array_equal(flags[0], arrays['Z'][post[0]]))
    checks['first_margin_exact'] = bool(np.array_equal(margin[0], arrays['margin'][post[0]], equal_nan=True))
    require(all(checks.values()), 'Frozen first post-proxy statistics/flags/margin mismatch')
    frozen = {'post_indices': post, 'times': arrays['times'][post], 'columns': arrays['columns'],
              'mean_fixed': mu, 'std_fixed': sd, 'count_fixed': count,
              'threshold_fixed': threshold, 'Z_fixed': flags, 'margin_fixed': margin,
              'mean_updated_minus_fixed': mu_updated - mu,
              'threshold_updated_minus_fixed': arrays['threshold'][post] - threshold,
              'finite_statistics_both': finite_stats, 'contrast_defined': contrast_defined}
    return frozen, checks


def finite_number(value):
    return float(value) if np.isfinite(value) else None


def first_flag(flags, frozen, proxy):
    hits = np.flatnonzero(flags)
    if not len(hits):
        return {'index': None, 'time': None, 'seconds_from_proxy': None}
    k = int(hits[0])
    timestamp = int(frozen['times'][k])
    return {'index': int(frozen['post_indices'][k]), 'time': timestamp,
            'seconds_from_proxy': timestamp - proxy}


def contrast_status(valid):
    if not np.any(valid):
        return 'N/A_NONFINITE_STATISTICS_OR_X'
    return 'DEFINED' if np.all(valid) else 'PARTIALLY_DEFINED'


def counters(updated, fixed, valid):
    added, removed = fixed & ~updated, updated & ~fixed
    return {'post_evaluated_cells': int(updated.size), 'defined_cells': int(valid.sum()),
            'undefined_cells': int(valid.size - valid.sum()),
            'native_true': int(updated.sum()), 'fixed_true': int(fixed.sum()),
            'added_flags': int(added.sum()), 'removed_flags': int(removed.sum()),
            'added_flags_defined_cells': int((added & valid).sum()),
            'removed_flags_defined_cells': int((removed & valid).sum()),
            'added_flags_undefined_cells': int((added & ~valid).sum()),
            'removed_flags_undefined_cells': int((removed & ~valid).sum()),
            'status': contrast_status(valid),
            'undefined_native_flags_retained': True}


def describe(arrays, frozen, iproxy, proxy):
    post = frozen['post_indices']
    updated, fixed = arrays['Z'][post], frozen['Z_fixed']
    valid = frozen['contrast_defined']
    rows = []
    for j, column in enumerate(arrays['columns'].tolist()):
        native_first = first_flag(updated[:, j], frozen, proxy)
        fixed_first = first_flag(fixed[:, j], frozen, proxy)
        delta = (fixed_first['time'] - native_first['time']
                 if fixed_first['time'] is not None and native_first['time'] is not None else None)
        counts = counters(updated[:, j], fixed[:, j], valid[:, j])
        counts['native_flags_with_nonfinite_statistics'] = int((updated[:, j]
            & ~(np.isfinite(arrays['mean'][post, j]) & np.isfinite(arrays['std'][post, j]))).sum())
        counts['fixed_flags_with_nonfinite_statistics'] = int((fixed[:, j]
            & ~(np.isfinite(frozen['mean_fixed'][j]) & np.isfinite(frozen['std_fixed'][j]))).sum())
        td = frozen['threshold_updated_minus_fixed'][:, j]
        finite_delta = td[np.isfinite(td)]
        rows.append({'column': column, 'count_fixed': int(frozen['count_fixed'][j]),
                     'mean_fixed': finite_number(frozen['mean_fixed'][j]),
                     'std_fixed': finite_number(frozen['std_fixed'][j]),
                     'threshold_fixed': finite_number(frozen['threshold_fixed'][j]),
                     'fixed_mean_nan': bool(np.isnan(frozen['mean_fixed'][j])),
                     'fixed_std_nan': bool(np.isnan(frozen['std_fixed'][j])),
                     'fixed_statistics_finite': bool(np.isfinite(frozen['mean_fixed'][j])
                                                     and np.isfinite(frozen['std_fixed'][j])),
                     'fixed_std_zero': bool(frozen['std_fixed'][j] == 0),
                     'fixed_fewer_than_two_observations': bool(frozen['count_fixed'][j] < 2),
                     'first_updated': native_first, 'first_fixed': fixed_first,
                     'first_time_fixed_minus_updated_s': delta,
                     'first_time_contrast_status': 'DEFINED' if delta is not None else 'N/A_ONE_OR_BOTH_NO_FLAG',
                     'threshold_delta_finite_min': float(finite_delta.min()) if len(finite_delta) else None,
                     'threshold_delta_finite_max': float(finite_delta.max()) if len(finite_delta) else None,
                     'counts': counts})
    updated_any, fixed_any = updated.any(axis=1), fixed.any(axis=1)
    nf, ff = first_flag(updated_any, frozen, proxy), first_flag(fixed_any, frozen, proxy)
    return {'i_proxy': iproxy, 't_proxy': proxy, 'T': len(arrays['times']), 'd': len(rows),
            'post_points': len(post), 'history': [0, iproxy], 'history_stop_exclusive': True,
            'fixed_statistics_source': 'Independent original-Series mean/std/count iloc[:i_proxy], checked exact against verified native core row i_proxy',
            'k': K, 'ddof': 1, 'native_start_index': START,
            'preprocessing': 'Reuse native Inf->NaN then ffill; leading NaN retained; no fill0/minmax/drop_constant',
            'first_updated_merged': nf, 'first_fixed_merged': ff,
            'merged_first_time_fixed_minus_updated_s': ff['time'] - nf['time'] if ff['time'] is not None and nf['time'] is not None else None,
            'merged_flag_points': {'updated': int(updated_any.sum()), 'fixed': int(fixed_any.sum()),
                                  'added': int((fixed_any & ~updated_any).sum()),
                                  'removed': int((updated_any & ~fixed_any).sum())},
            'all_cell_counts': counters(updated, fixed, valid), 'columns': rows,
            'contrast_meaning': 'Observed effect of updating history under this diagnostic; not evidence of a clean baseline or true onset.',
            'nan_meaning': 'Nonfinite contrast status is separate from native bool flags; NaN comparison remains False.',
            'array_layout': 'Only post-proxy arrays here; original x/mean/std/count/flags stay in hash-verified source NPZ.'}


def fixtures():
    from nsigma_run import statistics
    from baro.anomaly_detection import nsigma as native
    checks = []
    definitions = [
        ('constant', np.full(120, 2.), 100),
        ('step_std0', np.r_[np.zeros(100), np.ones(20)], 100),
        ('repeated', np.tile([0., 1.], 60), 100),
        ('leading_missing_no_observation', np.r_[np.full(101, np.nan), np.arange(19.)], 100),
        ('leading_missing_one_observation', np.r_[np.full(101, np.nan), np.arange(19.)], 102),
        ('inf_nan_ffill', np.r_[np.zeros(100), np.inf, -np.inf, np.nan, np.ones(17)], 100),
        ('last_grid_point', np.tile([0., 1.], 60), 119),
        ('manual_ddof1', np.r_[np.tile([0., 2.], 50), 5., 4., np.ones(18)], 100)]
    for name, values, iproxy in definitions:
        frame = pd.DataFrame({'time': np.arange(120), 'a': values})
        data = frame.replace([np.inf, -np.inf], np.nan).ffill()
        core = statistics(data)
        frozen, identity = freeze(core, iproxy)
        expected = sorted(set(native(data, k=K, startsfrom=START)))
        require(core['times'][core['Z'].any(axis=1)].tolist() == expected, 'Fixture core/native mismatch ' + name)
        history = data['a'].iloc[:iproxy]
        mu, sd, count = history.mean(), history.std(), history.count()
        direct = np.asarray([abs(v - mu) > K * sd for v in data['a'].iloc[iproxy:]], dtype=bool)
        require(np.array_equal(direct, frozen['Z_fixed'][:, 0]), 'Fixture fixed scalar mismatch ' + name)
        require(all(same_statistics(np.array([mu]), frozen['mean_fixed']).values())
                and all(same_statistics(np.array([sd]), frozen['std_fixed']).values())
                and count == frozen['count_fixed'][0], 'Fixture history definition mismatch ' + name)
        if name == 'constant':
            require(sd == 0 and not frozen['Z_fixed'].any(), 'Constant/strict > fixture')
        if name == 'step_std0':
            require(mu == sd == 0 and count == 100 and frozen['Z_fixed'].all(), 'Std0 fixture')
        if name.startswith('leading_missing'):
            require(np.isnan(sd) and not frozen['Z_fixed'].any()
                    and not frozen['contrast_defined'].any(), 'NaN false/contrast N/A fixture')
        if name == 'inf_nan_ffill':
            require(np.array_equal(core['x'][100:103, 0], np.zeros(3)), 'Inf replacement/ffill fixture')
        if name == 'manual_ddof1':
            require(mu == 1 and sd == np.sqrt(100 / 99) and count == 100,
                    'Manual 50 zeros +50 twos: mean1, sample variance100/99')
            require(bool(frozen['Z_fixed'][0, 0]) and not bool(frozen['Z_fixed'][1, 0]),
                    'Manual threshold: x5 flags, x4 does not')
        checks.append({'fixture': name, 'status': 'PASS', 'first_post_identity': identity,
                       'pandas_history_scalar_flags_exact': True,
                       'manual_checks': name in ('constant', 'step_std0', 'manual_ddof1')})
    return checks


def main(args):
    require(platform.system() == 'Linux', 'Research execution restricted to approved EC2 Linux')
    home = Path(os.environ['T033_HOME']).resolve()
    require(home == (Path.home() / 'rca/T-033').resolve(), 'T033_HOME must be approved ~/rca/T-033')
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run) is not None,
            'Run name must be a basename, no traversal')
    run = home / 'runs' / args.run
    run.mkdir(parents=True, exist_ok=False)
    source_path = home / 'inputs/source.json'
    status = {'status': 'RUNNING', 'pid': os.getpid(), 'started_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': sha(__file__), 'source_sha256': sha(source_path),
              'command': sys.argv, 'cases': {}, 'units_completed': 0,
              'fixed_parameters': {'k': K, 'ddof': 1, 'native_start': START},
              'source_core_runs': list(CORE_RUNS)}
    write(run / 'status.json', status)
    t0 = time.perf_counter()
    summaries = []
    try:
        source = read(source_path)
        require(source['task'] == 'T-033', 'Wrong task source')
        require((np.__version__, pd.__version__) == ('1.26.4', '2.2.3'), 'Source package versions changed')
        first_status_path, unused = manifest_entry(home / 'runs' / CORE_RUNS[0], 'status.json')
        first_status = read(first_status_path)
        require(first_status['status'] == 'PASS'
                and first_status['source_sha256'] == status['source_sha256'], 'First core source/status not valid')
        started = datetime.fromisoformat(first_status['started_utc'])
        from baro import anomaly_detection
        require(sha(anomaly_detection.__file__) == source['native_hash']['anomaly_detection.py'],
                'Native N-Sigma source hash changed')
        require(sha(Path(__file__).with_name('nsigma_run.py')) == first_status['script_sha256'],
                'Core statistics script hash changed')
        status['resources'] = budget_guard(home, source, started)
        write(run / 'fixtures.json', {'status': 'PASS', 'checks': fixtures()})
        update_manifest(run)
        require(len(source['cases']) == 30
                and len({c['opaque_id'] for c in source['cases']}) == 30, 'Dev case coverage mismatch')
        # Match the native driver: first pilot separately, then only remaining units.
        cases = source['cases'][:1] if args.first else (source['cases'] if args.all else source['cases'][1:])
        if args.cases:
            wanted = args.cases.split(',')
            require(len(wanted) == len(set(wanted)) and set(wanted) <= {c['opaque_id'] for c in cases},
                    'Requested cases outside selected source scope or duplicate')
            cases = [c for c in cases if c['opaque_id'] in wanted]
        require(bool(cases), 'No selected dev cases')
        for item in cases:
            oid = item['opaque_id']
            for detector in DETECTORS:
                status['resources'] = budget_guard(home, source, started)
                progress(home, 'START ' + oid + '/' + detector)
                begin = time.perf_counter()
                arrays, iproxy, provenance = load_core(home, item, detector, status['source_sha256'])
                baseline, independent_checks, raw_provenance = original_baseline(
                    home, source, item, detector, arrays, iproxy)
                frozen, checks = freeze(arrays, iproxy, baseline=baseline)
                checks.update(independent_checks)
                checks['first_frozen_flags_original_series_exact'] = bool(np.array_equal(
                    frozen['Z_fixed'][0], baseline['first_flags']))
                checks['first_frozen_margin_original_series_exact'] = bool(np.array_equal(
                    frozen['margin_fixed'][0], baseline['first_margin'], equal_nan=True))
                require(all(checks.values()), 'Independent first-point fixed branch mismatch')
                provenance['independent_original_series'] = raw_provenance
                projected = sum(a.nbytes for a in frozen.values()) + 2 * 2**20
                budget_guard(home, source, started, projected=projected)
                dest = run / (oid + '--' + detector + '.npz')
                np.savez_compressed(dest, **frozen)
                summary = describe(arrays, frozen, iproxy, int(item['proxy']))
                record = {'status': 'PASS', 'opaque_id': oid, 'detector': detector,
                          'branch': 'fixed_pre_proxy_history', 'checks': checks,
                          'source': provenance, 'source_sha256': status['source_sha256'],
                          'output_npz': dest.name, 'sha256': sha(dest), 'bytes': dest.stat().st_size,
                          'wall_s': time.perf_counter() - begin,
                          'rss_peak_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                          'summary': summary}
                write(run / (oid + '--' + detector + '.json'), record)
                summaries.append(record)
                status['cases'].setdefault(oid, {})[detector] = {
                    'status': 'PASS', 'record': oid + '--' + detector + '.json',
                    'output_npz': dest.name, 'sha256': record['sha256'],
                    'wall_s': record['wall_s'], 'checks': checks}
                status['units_completed'] += 1
                status['resources'] = budget_guard(home, source, started)
                write(run / 'status.json', status)
                update_manifest(run)
                progress(home, 'PASS ' + oid + '/' + detector + ' wall_s=' + str(round(record['wall_s'], 3)))
                del arrays, frozen
        require(status['units_completed'] == 2 * len(cases), 'Fixed branch coverage incomplete')
        # Keep the top-level summary compact; per-column counters remain in each unit JSON.
        write(run / 'nsigma-nguong-co-dinh.json', {
            'status': 'PASS', 'units': status['units_completed'], 'source_sha256': status['source_sha256'],
            'records': [{'opaque_id': r['opaque_id'], 'detector': r['detector'],
                         'record': r['opaque_id'] + '--' + r['detector'] + '.json',
                         'first_updated_merged': r['summary']['first_updated_merged'],
                         'first_fixed_merged': r['summary']['first_fixed_merged'],
                         'merged_flag_points': r['summary']['merged_flag_points'],
                         'all_cell_counts': r['summary']['all_cell_counts']} for r in summaries],
            'interpretation': 'Diagnostic history-update contrast only; no clean baseline, onset or selected online detector established.'})
        status['resources'] = budget_guard(home, source, started)
        status['status'] = 'PASS'
    except BaseException as exc:
        status['status'] = 'STOPPED'
        status['error'] = type(exc).__name__ + ': ' + str(exc)
        traceback.print_exc()
        progress(home, 'STOP ' + status['error'])
        raise
    finally:
        status['wall_s'] = time.perf_counter() - t0
        status['ended_utc'] = datetime.now(timezone.utc).isoformat()
        write(run / 'status.json', status)
        update_manifest(run)
        progress(home, status['status'] + ' ' + args.run)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--first', action='store_true', help='First source case only; fresh run')
    selection.add_argument('--all', action='store_true', help='All cases in one fresh run; default is rest after pilot')
    parser.add_argument('--cases', help='Subset of selected source opaque IDs; use only incomplete units')
    main(parser.parse_args())
