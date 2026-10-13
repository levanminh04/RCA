"""T-033: BOCPD delay/density descriptions from verified native full NPZ.

Run on EC2 only. No engine, preprocessing, metric or label file is opened.
Proxy is used solely to index this diagnostic description. Each NPZ is loaded
once; array pointers retain the original intermediate evidence without dumping
large posterior, predictive or covariance matrices to JSON.
"""
import argparse
import contextlib
import hashlib
import json
import os
import platform
import shutil
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import psutil


HAZARD = 1 / 50


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def encode(value):
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    if isinstance(value, np.ndarray):
        return encode(value.tolist())
    if isinstance(value, np.generic):
        return encode(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return {'nonfinite': 'NaN' if np.isnan(value) else ('+Inf' if value > 0 else '-Inf')}
    return value


def write(path, document, new=True):
    with path.open('x' if new else 'w', encoding='utf-8') as handle:
        json.dump(encode(document), handle, ensure_ascii=False, indent=2, allow_nan=False)


def segments(flags, times, proxy_index):
    """Only contiguous True CP flags at consecutive grid ticks form a segment."""
    output, start = [], None
    for i, value in enumerate(flags):
        if start is not None and (not value or int(times[i] - times[i - 1]) != 1):
            end = i - 1
            output.append({'start_index': start, 'end_index': end, 'start_time': int(times[start]),
                           'end_time': int(times[end]), 'points': end - start + 1,
                           'starts_before_and_reaches_proxy': start < proxy_index <= end})
            start = None
        if value and start is None:
            start = i
        if start is not None and i == len(flags) - 1:
            output.append({'start_index': start, 'end_index': i, 'start_time': int(times[start]),
                           'end_time': int(times[i]), 'points': i - start + 1,
                           'starts_before_and_reaches_proxy': start < proxy_index <= i})
    return output


class Description:
    def __init__(self, args, home, run):
        self.args, self.home, self.run = args, home, run
        self.input_files = {}
        self.begin = time.perf_counter()
        self.status = {'status': 'RUNNING', 'pid': os.getpid(), 'started_utc': now(),
                       'command': sys.argv, 'completed_cases': [], 'case_files': {},
                       'scripts': {'bocpd_delay.py': sha(Path(__file__))},
                       'stdout': str((run / 'stdout.txt').relative_to(home)),
                       'stderr': str((run / 'stderr.txt').relative_to(home)),
                       'progress': str((run / 'progress.txt').relative_to(home))}
        self.save_status()

    def save_status(self):
        write(self.run / 'status.json', self.status, new=False)

    def progress(self, message):
        text = now() + ' ' + message
        print(text, flush=True)
        for path in (self.run / 'progress.txt', self.home / 'trang-thai.txt'):
            with path.open('a', encoding='utf-8') as handle:
                handle.write(text + '\n')

    def scoped(self, relative):
        path = (self.home / relative).resolve()
        assert path.is_relative_to(self.home), 'Outside T033_HOME'
        return path

    def checked(self, path, expected_sha, expected_bytes=None):
        path = Path(path)
        actual = sha(path)
        assert actual == expected_sha, 'Hash mismatch: ' + str(path)
        if expected_bytes is not None:
            assert path.stat().st_size == expected_bytes, 'Size mismatch: ' + str(path)
        self.input_files[str(path)] = {'sha256': actual, 'bytes': path.stat().st_size}
        return path

    def load(self, path, expected_sha, expected_bytes=None):
        return json.loads(self.checked(path, expected_sha, expected_bytes).read_text(encoding='utf-8'))

    def guard(self, reserve=0):
        if (self.home / 'STOP').exists():
            raise RuntimeError('STOP: preserve all completed descriptions')
        ledger_path = self.scoped(os.environ['T033_PROCESSING_LEDGER_PATH'])
        expected_ledger = os.environ.get('T033_PROCESSING_LEDGER_SHA256')
        if not expected_ledger or sha(ledger_path) != expected_ledger:
            raise RuntimeError('BUDGET_LEDGER_HASH: processing ledger must be pinned')
        ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
        if not ledger['accounting_valid_for_next_run'] or ledger['approved_total_processing_s'] is None:
            raise RuntimeError('BUDGET_LEDGER_INCOMPLETE: missing processing time; no new allocation')
        if ledger['source_sha256'] != self.args.source_sha256:
            raise RuntimeError('BUDGET_LEDGER_SOURCE: source identity mismatch')
        used_before = float(ledger['approved_total_processing_s'])
        active_started = datetime.fromisoformat(os.environ['T033_ACTIVE_PROCESS_STARTED_UTC'])
        active_wall = (datetime.now(timezone.utc) - active_started).total_seconds()
        elapsed = used_before + active_wall
        if not 0 <= active_wall or not 0 <= used_before <= elapsed < self.source['budget_compute_s']:
            raise RuntimeError('BUDGET_STOP: cumulative processing budget exhausted')
        used = sum(p.stat().st_size for p in self.home.rglob('*') if p.is_file())
        if used + reserve >= self.source['budget_bytes']:
            raise RuntimeError('STORAGE_STOP: approved 4 GiB limit; do not delete prior runs')
        if shutil.disk_usage(self.home).free < reserve + 8 * 2**20:
            raise RuntimeError('DISK_STOP: insufficient space for descriptions')
        return {'new_bytes': used, 'disk_free_bytes': shutil.disk_usage(self.home).free,
                'ram_available_bytes': psutil.virtual_memory().available,
                'cumulative_processing_s': elapsed,
                'remaining_compute_s': self.source['budget_compute_s'] - elapsed}

    def core_run(self, name, manifest_sha):
        path = self.scoped('runs/' + name)
        manifest = self.load(path / 'manifest.json', manifest_sha)
        entry = manifest['status.json']
        status = self.load(path / 'status.json', entry['sha256'], entry['bytes'])
        assert status['status'] == 'PASS' and status['source_sha256'] == self.args.source_sha256
        self.checked(Path(__file__).with_name('bocpd_core.py'), status['scripts']['bocpd_core.py'])
        return {'directory': path, 'manifest': manifest, 'status': status}

    def setup(self):
        assert os.name == 'posix' and self.home.name == 'T-033', 'EC2 T033_HOME required'
        self.source = self.load(self.home / 'inputs/source.json', self.args.source_sha256)
        assert self.source['task'] == 'T-033' and len(self.source['cases']) == 30
        budget = self.load(self.home / 'runs/nsigma-first-001/status.json', self.args.first_compute_status_sha256)
        assert budget['source_sha256'] == self.args.source_sha256
        self.first_compute = datetime.fromisoformat(budget['started_utc'])
        self.first = self.core_run(self.args.core_first, self.args.core_first_sha256)
        self.rest = self.core_run(self.args.core_rest, self.args.core_rest_sha256)
        self.selected = min(self.source['cases'], key=lambda c: (
            c['expected']['bocpd']['input_shape']['cot_sau_tien_xu_ly'], c['opaque_id']))['opaque_id']
        self.status.update(source_sha256=self.args.source_sha256,
                           environment={'python': sys.version, 'platform': platform.platform(),
                                        'numpy': np.__version__}, resources=self.guard(64 * 2**20))
        self.save_status()

    def source_arrays(self, item):
        oid = item['opaque_id']
        oldrun = self.first if oid == self.selected else self.rest
        name = oid + '--full.json'
        entry = oldrun['manifest'][name]
        record = self.load(oldrun['directory'] / name, entry['sha256'], entry['bytes'])
        assert record['status'] == 'PASS' and all(record['checks'].values())
        assert oldrun['status']['cases'][oid]['full'] == record
        expected = item['expected']['bocpd']
        keys = ['status', 'alarms', 'input_shape', 'detector_columns', 'diagnostics']
        keys += ['chi_so'] if expected['status'] == 'OK' else ['error']
        assert all(record['result'].get(k) == expected.get(k) for k in keys)
        npz = record['npz']
        assert '/' not in npz and '\\' not in npz
        entry = oldrun['manifest'][npz]
        assert entry['sha256'] == record['sha256'] and entry['bytes'] == record['bytes']
        path = self.checked(oldrun['directory'] / npz, entry['sha256'], entry['bytes'])
        # Cache each array once. Repeated archive access would decompress per tick.
        with np.load(path, allow_pickle=False) as archive:
            arrays = {key: archive[key].copy() for key in archive.files}
        return record, arrays, {'record': str((oldrun['directory'] / name).relative_to(self.home)),
                               'npz': str(path.relative_to(self.home)), 'sha256': record['sha256'],
                               'raw_metrics': {'path': item['files']['metrics.parquet']['path'],
                                               'expected_sha256': item['files']['metrics.parquet']['sha256'],
                                               'opened_by_this_description': False}}

    def point(self, i, arrays, times, flags, theta_rows, source):
        R, m, runner = arrays['R'], arrays['m'], arrays['runner_up']
        r, competitor = int(m[i]), int(runner[i])
        previous = int(m[i - 1]) if i else None
        normalizer, reset = float(arrays['normalizer'][i]), float(arrays['reset_mass'][i])
        predictive = arrays['predictive_density'][i]
        ratio = reset / normalizer
        row = {'index': i, 'time': int(times[i]), 'CP_flag': bool(flags[i]), 'm': r,
               'previous_m': previous, 'absolute_m_change': abs(r - previous) if previous is not None else None,
               'runner_up_run_length': competitor, 'MAP_posterior': float(R[r, i + 1]),
               'runner_up_posterior': float(R[competitor, i + 1]),
               'MAP_minus_runner_posterior': float(R[r, i + 1] - R[competitor, i + 1]),
               'normalizer': normalizer, 'reset_mass_before_normalization': reset,
               'reset_mass_divided_by_normalizer': ratio, 'reset_posterior': float(R[0, i + 1]),
               'constant_hazard': HAZARD, 'reset_ratio_minus_hazard': ratio - HAZARD,
               'MAP_growth_parent': r - 1 if r > 0 else None,
               'MAP_parent_predictive_density': float(predictive[r - 1]) if r > 0 else None,
               'runner_growth_parent': competitor - 1 if competitor > 0 else None,
               'runner_parent_predictive_density': float(predictive[competitor - 1]) if competitor > 0 else None,
               'MAP_reset_is_mixture_of_all_parents': r == 0,
               'posterior_pointer': {'npz': source['npz'], 'array': 'R', 'column': i + 1,
                                     'support_rows_inclusive': [0, i + 1]},
               'predictive_pointer': {'npz': source['npz'], 'array': 'predictive_density', 'row': i,
                                      'valid_parent_columns_inclusive': [0, i]},
               'processed_input_pointer': {'npz': source['npz'], 'array': 'X', 'row': i,
                                          'column_names_array': 'columns'},
               'raw_input_pointer': {'metrics_path': source['raw_metrics']['path'], 'row': i,
                                     'expected_sha256': source['raw_metrics']['expected_sha256']}}
        theta_row = theta_rows.get(i)
        row['theta_available'] = theta_row is not None
        row['theta_pointer'] = None if theta_row is None else {
            'npz': source['npz'], 'row': theta_row, 'time_index_array': 'theta_points',
            'parent_index_array': 'theta_parent_indices',
            'saved_parent_indices': [int(v) for v in arrays['theta_parent_indices'][theta_row] if v >= 0],
            'before_arrays': ['theta_before_' + k for k in ('dof', 'kappa', 'mu', 'scale')],
            'after_arrays': ['theta_after_' + k for k in ('dof', 'kappa', 'mu', 'scale')],
            'mapping': 'after parent slot contains update of before run length r into run length r+1; native prior row0 unchanged and is not represented by an after slot'}
        return row

    def describe(self, item):
        oid = item['opaque_id']
        self.guard(64 * 2**20)
        self.progress('BOCPD DELAY START ' + oid)
        record, arrays, source = self.source_arrays(item)
        times, X = arrays['times'], arrays['X']
        T = len(times)
        assert T == 1441 and np.isfinite(times).all() and np.array_equal(times, times.astype(np.int64))
        assert np.all(np.diff(times) == 1)
        resolved = np.flatnonzero(times == item['proxy'])
        assert len(resolved) == 1 and int(resolved[0]) == 720
        cut = int(resolved[0])
        assert X.shape == (T, record['result']['input_shape']['cot_sau_tien_xu_ly'])
        assert len(arrays['columns']) == X.shape[1]
        basic = {'opaque_id': oid, 'detector': 'bocpd', 'branch': 'full',
                 'native_status': record['result']['status'], 'native_result': record['result'],
                 'source': source, 'index_map': {'i_proxy': cut, 't_proxy': int(times[cut]),
                                               'time_start': int(times[0]), 'time_end': int(times[-1]),
                                               'points': T, 'grid_step_seconds': 1},
                 'processed_columns': arrays['columns'].tolist(),
                 'interpretation': 'Observed retrospective CP position relative to proxy; before-proxy CP is not an operational false alarm; no true onset or physical cause inferred'}
        index = {'opaque_id': oid, 'detector': 'bocpd', 'branch': 'full', 'source': source,
                 'arrays_and_shapes': {k: list(v.shape) for k, v in arrays.items()},
                 'R_mapping': 'm[i] = argmax R[:,i+1]; growth rowr uses predictive parent r-1',
                 'predictive_mapping': 'predictive_density[i,0:i+1] describes parents before data index i',
                 'raw_vs_processed': 'raw reference is untouched parquet; X is full-native preprocessing with look-ahead mask/minmax',
                 'native_evaluated_indices': 'i>=1 only when complete native posterior is valid'}
        if record['result']['status'] != 'OK':
            # Adapter ERROR discards alarms. It does not establish a valid no-CP observation.
            basic.update(status='NATIVE_NON_OK', delay_defined=False, density_defined=False,
                         first_alarm_index=None, first_post_proxy_index=None,
                         signed_seconds_from_proxy=None, no_post_alarm_to_end=None,
                         consecutive_true_segments=None, pre_proxy=None,
                         missing='Complete valid native CP/m trajectory unavailable; preserve native error/diagnostics')
            write(self.run / (oid + '--delay.json'), basic)
            return basic, index
        R, m, flags = arrays['R'], arrays['m'], arrays['CP_flags']
        runner, pred = arrays['runner_up'], arrays['predictive_density']
        assert R.shape == (T + 1, T + 1) and np.isfinite(R).all()
        assert m.shape == flags.shape == runner.shape == arrays['normalizer'].shape == arrays['reset_mass'].shape == (T,)
        assert pred.shape == (T, T) and np.issubdtype(m.dtype, np.integer)
        assert np.array_equal(m, R[:, 1:].argmax(axis=0)) and np.array_equal(m, arrays['m_online'])
        expected_flags = np.r_[False, np.abs(np.diff(m)) > 1]
        assert np.array_equal(flags, expected_flags)
        cp = np.flatnonzero(flags).tolist()
        assert cp == record['result']['chi_so'] and times[flags].astype(int).tolist() == record['result']['alarms']
        original = np.flatnonzero(np.abs(np.diff(arrays['maxes'])) > 1) + 1
        assert original.tolist() == record['result']['diagnostics']['diem_doi_maxes_goc']
        assert bool(len(original) and original[-1] == T) == record['result']['diagnostics']['co_sentinel_goc']
        theta = arrays['theta_points']
        assert np.array_equal(theta, np.sort(np.unique(theta))) and np.all((theta >= 0) & (theta < T))
        theta_rows = {int(i): row for row, i in enumerate(theta)}
        assert arrays['theta_parent_indices'].shape == (len(theta), 4)
        d = X.shape[1]
        expected_theta_shapes = {'dof': (len(theta), 4), 'kappa': (len(theta), 4),
                                 'mu': (len(theta), 4, d), 'scale': (len(theta), 4, d, d)}
        for period in ('before', 'after'):
            for field, shape in expected_theta_shapes.items():
                assert arrays['theta_' + period + '_' + field].shape == shape
        for row, i in enumerate(theta):
            parents = arrays['theta_parent_indices'][row]
            valid = parents[parents >= 0]
            assert len(valid) >= 1 and valid[0] == 0 and np.all(valid <= i)
            assert np.array_equal(valid, np.sort(np.unique(valid)))
            assert np.all(parents[len(valid):] == -1)
            for period in ('before', 'after'):
                for field in ('dof', 'kappa', 'mu', 'scale'):
                    values = arrays['theta_' + period + '_' + field][row]
                    assert np.isfinite(values[:len(valid)]).all()
                    assert np.isnan(values[len(valid):]).all()
            for field in ('dof', 'kappa'):
                assert np.array_equal(arrays['theta_after_' + field][row, :len(valid)],
                                      arrays['theta_before_' + field][row, :len(valid)] + 1)
        assert R[0, 0] == 1 and np.all(R[1:, 0] == 0)
        max_hazard_difference = 0.0
        for i in range(T):
            if i % 200 == 0:
                self.guard()
            pdf = pred[i, :i + 1]
            assert np.isfinite(pdf).all() and np.all(pdf >= 0)
            assert np.isnan(pred[i, i + 1:]).all(), 'Unused predictive padding must remain NaN'
            ranking = np.argsort(-R[:i + 2, i + 1], kind='stable')
            assert int(runner[i]) == int(ranking[1]) and int(m[i]) == int(ranking[0])
            mass = np.zeros(T + 1)
            hazard = HAZARD * np.ones(i + 1)
            mass[1:i + 2] = R[:i + 1, i] * pdf * (1 - hazard)
            mass[0] = np.sum(R[:i + 1, i] * pdf * hazard)
            normalizer = np.sum(mass)
            assert np.isfinite(normalizer) and normalizer > 0
            assert normalizer == arrays['normalizer'][i] and mass[0] == arrays['reset_mass'][i]
            assert np.array_equal(mass / normalizer, R[:, i + 1])
            max_hazard_difference = max(max_hazard_difference, abs(float(mass[0] / normalizer) - HAZARD))
        evaluated = np.arange(T) >= 1
        pre = evaluated & (times < item['proxy'])
        post = evaluated & (times >= item['proxy'])
        before_indices = np.flatnonzero(pre)
        post_indices = np.flatnonzero(flags & post)
        first = cp[0] if cp else None
        first_post = int(post_indices[0]) if len(post_indices) else None
        allsegments = segments(flags, times, cut)
        containing = next((s for s in allsegments if first_post is not None and s['start_index'] <= first_post <= s['end_index']), None)
        end = first_post if first_post is not None else T - 1
        chain = [self.point(i, arrays, times, flags, theta_rows, source) for i in range(cut, end + 1)]
        assert all(row['theta_available'] for row in chain), 'Missing stored theta in proxy-to-first-post/end region'
        neighboring = sorted({i for c in cp for i in (c - 1, c, c + 1) if 0 <= i < T})
        evidence = [self.point(i, arrays, times, flags, theta_rows, source) for i in neighboring]
        assert all(row['theta_available'] for row in evidence), 'Missing stored CP/neighbor theta'
        pre_count = int(pre.sum())
        basic.update(status='VALID_NATIVE', delay_defined=first_post is not None, density_defined=True,
                     first_alarm_index=first, first_alarm_time=int(times[first]) if first is not None else None,
                     first_alarm_signed_seconds_from_proxy=int(times[first] - item['proxy']) if first is not None else None,
                     first_post_proxy_index=first_post, t_hat_plus=int(times[first_post]) if first_post is not None else None,
                     signed_seconds_from_proxy=int(times[first_post] - item['proxy']) if first_post is not None else None,
                     no_post_alarm_to_end=first_post is None, followup_end_time=int(times[-1]),
                     post_proxy_followup_elapsed_seconds=int(times[-1] - item['proxy']),
                     post_proxy_native_evaluated_points=int(post.sum()),
                     pre_proxy={'CP_points': int(np.sum(flags & pre)), 'native_evaluated_points': pre_count,
                                'fraction_CP_points': float(np.sum(flags & pre) / pre_count) if pre_count else None,
                                'first_evaluated_index': int(before_indices[0]) if pre_count else None,
                                'last_evaluated_index': int(before_indices[-1]) if pre_count else None,
                                'first_evaluated_time': int(times[before_indices[0]]) if pre_count else None,
                                'last_evaluated_time': int(times[before_indices[-1]]) if pre_count else None,
                                'grid_point_seconds_coverage': pre_count,
                                'elapsed_first_to_last_seconds': int(times[before_indices[-1]] - times[before_indices[0]]) if pre_count else None},
                     consecutive_true_segments=allsegments,
                     first_post_CP_containing_segment=containing,
                     first_post_CP_in_segment_started_before_proxy=containing['starts_before_and_reaches_proxy'] if containing else None,
                     proxy_to_first_post_or_end={'start_index': cut, 'end_index': end, 'points': chain},
                     CP_and_neighbor_evidence=evidence,
                     numerical_checks={'R_m_CP_time_source_exact': True, 'runner_stable_rank_exact': True,
                                       'predictive_support_and_padding_valid': True,
                                       'native_mass_normalizer_posterior_reconstruction_exact': True,
                                       'max_abs_reset_ratio_minus_constant_hazard': max_hazard_difference,
                                       'reset_posterior_role': 'Structural constant-hazard relationship; not a new score or delay detector'},
                     mechanism_status='Stored computation described; interpretation and competing physical/protocol explanations remain OPEN')
        index.update(theta_points=theta.tolist(), theta_point_to_row={str(k): v for k, v in theta_rows.items()},
                     CP_and_neighbor_indices=neighboring, proxy_chain_indices_inclusive=[cut, end],
                     source_keys_validated=True)
        write(self.run / (oid + '--delay.json'), basic)
        return basic, index

    def execute(self):
        rows, indexes = [], []
        try:
            self.setup()
            for item in sorted([c for c in self.source['cases'] if c['opaque_id'] in self.args.cases.split(',')], key=lambda c: c['opaque_id']):
                row, index = self.describe(item)
                # Keep the overview compact; detailed point chains remain per case.
                rows.append({k: v for k, v in row.items() if k not in ('proxy_to_first_post_or_end', 'CP_and_neighbor_evidence')})
                indexes.append(index)
                oid = item['opaque_id']
                self.status['completed_cases'].append(oid)
                self.status['case_files'][oid] = oid + '--delay.json'
                self.status['resources'] = self.guard()
                self.save_status()
                self.progress('BOCPD DELAY PASS ' + oid + ' native_status=' + row['native_status'])
            for path, meta in self.input_files.items():
                assert sha(path) == meta['sha256'], 'Old source changed during description'
            write(self.run / 'delay.json', {'status': 'PASS', 'rows': rows, 'cases': len(rows),
                                          'scope': 'BOCPD full only; no detector or protocol changes',
                                          'interpretation': 'Retrospective CP offset from proxy, not operational delay from known onset'})
            write(self.run / 'intermediate-index.json', {'status': 'PASS', 'items': indexes,
                                                        'large_arrays_remain_in_verified_source_NPZ': True})
            self.status['status'] = 'PASS'
        except BaseException as exc:
            self.status.update(status='STOPPED', error=type(exc).__name__ + ': ' + str(exc))
            traceback.print_exc()
            self.progress('BOCPD DELAY STOP ' + self.status['error'])
            raise
        finally:
            self.status.update(ended_utc=now(), wall_s=time.perf_counter() - self.begin, input_files=self.input_files)
            self.save_status()
            self.progress('BOCPD DELAY ' + self.status['status'] + ' ' + self.args.run)
            write(self.run / 'manifest.json', {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size}
                                               for p in self.run.iterdir() if p.is_file() and p.name not in ('manifest.json', 'stdout.txt', 'stderr.txt')})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    parser.add_argument('--cases', required=True)
    parser.add_argument('--core-first', default='bocpd-first-002')
    parser.add_argument('--core-rest', default='bocpd-rest-001')
    parser.add_argument('--core-first-sha256', required=True)
    parser.add_argument('--core-rest-sha256', required=True)
    parser.add_argument('--source-sha256', required=True)
    parser.add_argument('--first-compute-status-sha256', required=True)
    args = parser.parse_args()
    assert os.name == 'posix', 'Research calculations are authorized on EC2 only'
    for name in (args.run, args.core_first, args.core_rest):
        assert name and name not in ('.', '..') and '/' not in name and '\\' not in name
    home = Path(os.environ['T033_HOME']).resolve()
    run = home / 'runs' / args.run
    run.mkdir(parents=True, exist_ok=False)
    try:
        with (run / 'stdout.txt').open('x', encoding='utf-8') as stdout, (run / 'stderr.txt').open('x', encoding='utf-8') as stderr:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                try:
                    Description(args, home, run).execute()
                finally:
                    stdout.flush(); stderr.flush()
    finally:
        write(run / 'logs-manifest.json', {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size}
                                           for p in (run / 'stdout.txt', run / 'stderr.txt') if p.is_file()})


if __name__ == '__main__':
    main()