"""T-033 FP/PF diagnostics after validated full/FF/PP; EC2 only.

The caller supplies hashes of the completed core manifests. All old files used
are checked before reading, and their hashes are recorded in the new run.
No native engine, preprocessing helper, threshold or source output is changed.
"""
import argparse
import contextlib
import hashlib
import itertools
import json
import os
import platform
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
import scipy
from baro import _bocpd
from baro.utility import drop_constant
from p3.adapters import phat_hien
from bocpd_core import observed, plain, compare_same_input, result_from_R
from factorial_matrices import matrices, contrast


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def plain_json(value):
    """Preserve nonfinite diagnostic values explicitly, never as invented zero."""
    if isinstance(value, dict):
        return {str(k): plain_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain_json(v) for v in value]
    if isinstance(value, np.ndarray):
        return plain_json(value.tolist())
    if isinstance(value, np.generic):
        return plain_json(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return {'nonfinite': 'NaN' if np.isnan(value) else ('+Inf' if value > 0 else '-Inf')}
    return value


def write_new(path, document):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(plain_json(document), handle, ensure_ascii=False, indent=2, allow_nan=False)


def write_status(path, document):
    # The sole mutable output is this run's process status.
    with path.open('w', encoding='utf-8') as handle:
        json.dump(plain_json(document), handle, ensure_ascii=False, indent=2, allow_nan=False)


class Driver:
    def __init__(self, args, run):
        self.args, self.run = args, run
        self.home = run.parent.parent
        self.inputs = {}
        self.status = {'status': 'RUNNING', 'pid': os.getpid(), 'started_utc': now(),
                       'command': sys.argv, 'cases': {}, 'validated_core_cases': [],
                       'posterior_tolerance': {'rtol': 1e-12, 'atol': 1e-14,
                                               'm_CP_status_exact': True},
                       'stdout': str((run / 'stdout.txt').relative_to(self.home)),
                       'stderr': str((run / 'stderr.txt').relative_to(self.home)),
                       'progress': str((run / 'progress.txt').relative_to(self.home)),
                       'scientific_scope': 'Prefix factorial diagnostics; proxy-informed cut; no online detector or onset claim'}
        self.begin = time.perf_counter()
        self.save_status()

    def home_path(self, relative):
        path = (self.home / relative).resolve()
        assert path.is_relative_to(self.home), 'Outside T033_HOME: ' + str(path)
        return path

    def checked(self, path, expected_sha=None, expected_bytes=None):
        path = Path(path)
        actual = sha(path)
        if expected_sha is not None:
            assert actual == expected_sha, 'Source hash mismatch: ' + str(path)
        if expected_bytes is not None:
            assert path.stat().st_size == expected_bytes, 'Source size mismatch: ' + str(path)
        self.inputs[str(path)] = {'sha256': actual, 'bytes': path.stat().st_size}
        return path

    def load(self, path, expected_sha=None, expected_bytes=None):
        return json.loads(self.checked(path, expected_sha, expected_bytes).read_text(encoding='utf-8'))

    def save_status(self):
        write_status(self.run / 'status.json', self.status)

    def progress(self, message):
        line = now() + ' ' + message
        print(line, flush=True)
        for path in (self.run / 'progress.txt', self.home / 'trang-thai.txt'):
            with path.open('a', encoding='utf-8') as handle:
                handle.write(line + '\n')

    def bytes_used(self):
        return sum(p.stat().st_size for p in self.home.rglob('*') if p.is_file())

    def guard(self, additional_bytes=0):
        if (self.home / 'STOP').exists():
            raise RuntimeError('STOP: user/agent checkpoint; preserve completed units')
        elapsed = (datetime.now(timezone.utc) - self.first_compute).total_seconds()
        if elapsed >= self.source['budget_compute_s']:
            raise RuntimeError('BUDGET_STOP: 12 hours since first compute; checkpoint and present to Minh')
        used = self.bytes_used()
        if used + additional_bytes >= self.source['budget_bytes']:
            raise RuntimeError('STORAGE_STOP: approved 4 GiB bound; preserve all runs')
        if shutil.disk_usage(self.home).free < additional_bytes + 8 * 2**20:
            raise RuntimeError('DISK_STOP: insufficient space for next output')
        return {'new_bytes': used, 'disk_free_bytes': shutil.disk_usage(self.home).free,
                'ram_available_bytes': psutil.virtual_memory().available,
                'elapsed_since_first_compute_s': elapsed,
                'remaining_compute_s': self.source['budget_compute_s'] - elapsed}

    def run_sources(self, name, anchor):
        path = self.home_path('runs/' + name)
        manifest_path = path / 'manifest.json'
        manifest = self.load(manifest_path, anchor)
        entry = manifest['status.json']
        status = self.load(path / 'status.json', entry['sha256'], entry['bytes'])
        assert status['status'] == 'PASS', 'Core/first run incomplete: ' + name
        assert status['source_sha256'] == sha(self.home / 'inputs/source.json')
        assert status['scripts']['bocpd_core.py'] == sha(Path(__file__).with_name('bocpd_core.py'))
        return {'directory': path, 'manifest': manifest, 'status': status}

    def old_json(self, oldrun, name):
        entry = oldrun['manifest'][name]
        return self.load(oldrun['directory'] / name, entry['sha256'], entry['bytes'])

    def old_arrays(self, oldrun, record):
        name = record['npz']
        entry = oldrun['manifest'][name]
        path = self.checked(oldrun['directory'] / name, entry['sha256'], entry['bytes'])
        assert record['sha256'] == entry['sha256'] and record['bytes'] == entry['bytes']
        with np.load(path, allow_pickle=False) as archive:
            return {k: archive[k].copy() for k in archive.files}

    def setup(self):
        assert os.name == 'posix', 'Research computation is authorized on EC2 only'
        self.source = self.load(self.home / 'inputs/source.json', self.args.source_sha256)
        assert self.source['task'] == 'T-033' and len(self.source['cases']) == 30
        self.core_first = self.run_sources(self.args.core_first, self.args.core_first_sha256)
        self.core_rest = self.run_sources(self.args.core_rest, self.args.core_rest_sha256)
        first_status = self.load(self.home / 'runs/nsigma-first-001/status.json', self.args.first_compute_status_sha256)
        assert first_status['source_sha256'] == sha(self.home / 'inputs/source.json')
        self.first_compute = datetime.fromisoformat(first_status['started_utc'])
        self.selected = min(self.source['cases'], key=lambda c: (
            c['expected']['bocpd']['input_shape']['cot_sau_tien_xu_ly'], c['opaque_id']))['opaque_id']
        preflight = self.home_path('runs/' + os.environ['T033_PREFLIGHT'])
        verified = self.load(preflight / 'verification.json', self.args.preflight_verification_sha256)
        inventory = self.load(preflight / 'inventory.json', self.args.preflight_inventory_sha256)
        assert verified['status'] == inventory['status'] == 'PASS'
        self.paths = {c['opaque_id']: c for c in inventory['cases']}
        assert set(self.paths) == {c['opaque_id'] for c in self.source['cases']}
        self.core = {}
        for item in self.source['cases']:
            oid = item['opaque_id']
            oldrun = self.core_first if oid == self.selected else self.core_rest
            records = {}
            for branch in ('full', 'PP'):
                record = self.old_json(oldrun, oid + '--' + branch + '.json')
                assert record['status'] == 'PASS' and all(record['checks'].values())
                expected = item['expected']['bocpd'] if branch == 'full' else item['pp_expected']
                keys = ['status', 'alarms', 'input_shape', 'detector_columns', 'diagnostics']
                keys += ['chi_so'] if expected['status'] == 'OK' else ['error']
                assert all(record['result'].get(k) == expected.get(k) for k in keys)
                entry = oldrun['manifest'][record['npz']]
                self.checked(oldrun['directory'] / record['npz'], record['sha256'], record['bytes'])
                assert entry == {'sha256': record['sha256'], 'bytes': record['bytes']}
                assert oldrun['status']['cases'][oid][branch] == record
                records[branch] = record
            ff = self.old_json(oldrun, oid + '--FF-check.json')
            assert ff['processed_input_equal'] and ff['status'] == ff['native_result']['status']
            if records['full']['result']['status'] == ff['status'] == 'OK':
                assert ff['m_prefix_match'] and ff['cp_prefix_match']
            self.core[oid] = {'run': oldrun, 'records': records, 'FF': ff}
            self.status['validated_core_cases'].append(oid)
        native_dir = Path(_bocpd.__file__).parent
        for name, expected in self.source['native_hash'].items():
            self.checked(native_dir / name, expected)
        self.checked(Path(phat_hien.__file__), self.source['adapter_sha256'])
        assert (np.__version__, pd.__version__, scipy.__version__) == ('1.26.4', '2.2.3', '1.14.1')
        scripts = ['bocpd_factorial.py', 'bocpd_core.py', 'bocpd_run.py', 'factorial_matrices.py']
        self.status['scripts'] = {name: sha(Path(__file__).with_name(name)) for name in scripts}
        self.status['source_sha256'] = sha(self.home / 'inputs/source.json')
        self.status['environment'] = {'python': sys.version, 'os': platform.platform(),
                                      'architecture': platform.machine(), 'numpy': np.__version__,
                                      'pandas': pd.__version__, 'scipy': scipy.__version__,
                                      'variables': {k: os.environ.get(k) for k in (
                                          'PYTHONPATH', 'PYTHONHASHSEED', 'PYTHONDONTWRITEBYTECODE',
                                          'OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS')}}
        self.reuse = None
        if self.args.verified_first:
            self.reuse = self.run_sources(self.args.verified_first, self.args.verified_first_sha256)
            assert self.reuse['status']['scripts']['factorial_matrices.py'] == self.status['scripts']['factorial_matrices.py']
            fixtures = self.old_json(self.reuse, 'fixtures.json')
            assert fixtures['status'] == 'PASS'
            for branch in ('FP', 'PF'):
                record = self.old_json(self.reuse, self.selected + '--' + branch + '.json')
                assert record['status'] == 'PASS' and all(record['checks'].values())
                assert any(k.startswith('same_input_') for k in record['checks'])
        if not self.args.first:
            assert self.reuse is not None, '--rest requires validated supplemental first run and manifest hash'
        self.status['resources'] = self.guard()
        self.save_status()
        write_new(self.run / 'core-verification.json', {
            'status': 'PASS', 'cases': self.status['validated_core_cases'], 'selected_first': self.selected,
            'source_sha256': self.status['source_sha256'], 'sources': self.inputs,
            'selection': 'Smallest original full d, then opaque_id; unchanged from core driver'})

    def fixtures(self):
        # Reuse the exact native-wrapper and independent scalar fixtures of core.
        from bocpd_run import fixtures as core_fixtures
        self.guard()
        checks = core_fixtures()
        raw = pd.DataFrame({'a_error': [0., 1., 2., 3.], 'late_error': [0., 0., 2., 4.],
                            'missing_error': [np.nan, 1., 2., 3.], 'constant_error': [7., 7., 7., 7.]})
        raw['time'] = np.arange(4)
        mats, metadata = matrices(raw, 2)
        assert metadata['FF']['columns'] == ['a_error', 'late_error', 'missing_error']
        assert metadata['PP']['columns'] == ['a_error', 'missing_error']
        assert np.array_equal(mats['FF'].to_numpy(), [[0., 0., 0.], [1/3, 0., 1/3]])
        assert np.array_equal(mats['FP'].to_numpy(), [[0., 0., 0.], [1., 0., 1.]])
        assert np.array_equal(mats['PF'].to_numpy(), [[0., 0.], [1/3, 1/3]])
        assert np.array_equal(mats['PP'].to_numpy(), [[0., 0.], [1., 1.]])
        assert metadata['FP']['range0_columns'] == ['late_error']
        checks.append({'fixture': 'manual_four_paths_mask_before_fill_and_range0', 'pass': True})
        for branch in ('FP', 'PF'):
            X = mats[branch].to_numpy()
            result, arrays = observed(X, np.arange(2), 4, list(mats[branch]))
            direct, R, mx = plain(X, np.arange(2), 4, list(mats[branch]))
            comparison = compare_same_input(result, arrays, direct, R, mx)
            assert all(comparison.values()), (branch, comparison)
            checks.append({'fixture': 'factorial_' + branch + '_native_same_input', 'checks': comparison,
                           'native_status': result['status']})
        self.guard()
        write_new(self.run / 'fixtures.json', {'status': 'PASS', 'checks': checks})

    def diagonal(self, item, mats, times, raw_columns, cut):
        old = self.core[item['opaque_id']]
        full = self.old_arrays(old['run'], old['records']['full'])
        pp = self.old_arrays(old['run'], old['records']['PP'])
        assert np.array_equal(full['times'], times) and np.array_equal(pp['times'], times[:cut])
        assert full['columns'].tolist() == list(mats['FF'])
        assert pp['columns'].tolist() == list(mats['PP'])
        assert np.array_equal(full['X'][:cut], mats['FF'].to_numpy(), equal_nan=True)
        assert np.array_equal(pp['X'], mats['PP'].to_numpy(), equal_nan=True)
        ff_result = old['FF']['native_result']
        pp_result = old['records']['PP']['result']
        paths = {'FF': {'result': ff_result}, 'PP': {'result': pp_result}}
        for branch, arrays, result in [('FF', full, ff_result), ('PP', pp, pp_result)]:
            if result['status'] == 'OK':
                if branch == 'FF':
                    R = arrays.get('R', arrays.get('R_partial'))
                    assert R is not None and R.shape[0] >= cut + 1 and R.shape[1] >= cut + 1
                    prefix_R = R[:cut + 1, :cut + 1]
                    assert np.isfinite(prefix_R[:, 1:]).all(), 'CORE_FF_INTERMEDIATE_MISSING; do not invent m'
                    m = prefix_R[:, 1:].argmax(axis=0)
                else:
                    m = arrays['m']
                flags = np.r_[False, np.abs(np.diff(m)) > 1]
                assert np.flatnonzero(flags).tolist() == result['chi_so']
                assert [int(times[i]) for i in result['chi_so']] == result['alarms']
                paths[branch].update(m=m, CP_flags=flags)
            paths[branch]['provenance'] = str(old['run']['directory'].relative_to(self.home))
        del full, pp
        return paths

    def metadata(self, df, cut, mats, metadata):
        columns = phat_hien.cot_bocpd(df.columns)
        raw = df[columns]
        MF = list(drop_constant(raw).columns)
        MP = list(drop_constant(raw.iloc[:cut].copy()).columns)
        assert set(MP) <= set(MF)
        assert [c for c in MF if c in set(MP)] == MP
        fill = {'F': raw.ffill().fillna(0), 'P': raw.iloc[:cut].copy().ffill().fillna(0)}
        for branch, meta in metadata.items():
            base = fill[meta['scale_source']]
            meta['minmax_after_native_fill'] = {
                c: {'min': base[c].min(), 'max': base[c].max(), 'range': base[c].max() - base[c].min()}
                for c in meta['columns']}
            meta['native_prior'] = {'dims': meta['d'], 'dof': meta['d'] + 1,
                                    'kappa': 1, 'mu': 'zero vector', 'scale': 'identity precision matrix'}
            meta['hazard_denominator'] = 50
            meta['matrix_shape'] = list(mats[branch].shape)
            meta['matrix_bytes_sha256'] = hashlib.sha256(mats[branch].to_numpy().tobytes()).hexdigest()
            meta['fill'] = 'raw ffill then fillna(0); scale then ffill then fillna(0); Inf is not replaced'
        return {'M_F': MF, 'M_P': MP, 'M_P_subset_M_F_before_fill': True, 'branches': metadata}

    def identity(self, mats, paths):
        output = {}
        for a, b in itertools.combinations(('FF', 'FP', 'PF', 'PP'), 2):
            same = list(mats[a]) == list(mats[b]) and np.array_equal(
                mats[a].to_numpy(), mats[b].to_numpy(), equal_nan=True)
            row = {'same_input_shape_order_and_native_params': same}
            if same:
                ra, rb = paths[a]['result'], paths[b]['result']
                checks = {k: ra.get(k) == rb.get(k) for k in ('status', 'error', 'chi_so', 'alarms', 'diagnostics')}
                if ra['status'] == rb['status'] == 'OK':
                    checks.update(m=np.array_equal(paths[a]['m'], paths[b]['m']),
                                  CP_flags=np.array_equal(paths[a]['CP_flags'], paths[b]['CP_flags']))
                row['exact_output_checks'] = checks
                assert all(checks.values()), ('Identical input differs', a, b, checks)
            output[a + '_vs_' + b] = row
        return output

    def contrasts(self, paths):
        pairs = [('FF', 'FP', 'scale_with_M_F'), ('PF', 'PP', 'scale_with_M_P'),
                 ('FF', 'PF', 'mask_d_prior_with_S_F'), ('FP', 'PP', 'mask_d_prior_with_S_P'),
                 ('FF', 'PP', 'total_full_preprocessing_vs_prefix')]
        output = {}
        for a, b, name in pairs:
            row = contrast(paths[a], paths[b])
            row.update(a=a, b=b, sign='a minus b')
            if row['defined']:
                ca, cb = paths[a]['result']['chi_so'], paths[b]['result']['chi_so']
                row['first_CP_index_a'] = ca[0] if ca else None
                row['first_CP_index_b'] = cb[0] if cb else None
                row['signed_first_CP_shift'] = ca[0] - cb[0] if ca and cb else None
                row['first_shift_defined'] = bool(ca and cb)
                if not (ca and cb):
                    row['first_shift_reason'] = 'At least one valid branch has no CP; no invented zero shift'
            output[name] = row
        interaction = {'defined': all(paths[b]['result']['status'] == 'OK' for b in paths),
                       'formula': '(FF - FP) - (PF - PP); equivalently (FF - PF) - (FP - PP)'}
        if interaction['defined']:
            for field, target in [('m', 'signed_m_interaction'), ('CP_flags', 'signed_CP_flag_interaction')]:
                vals = {b: np.asarray(paths[b][field], dtype=int) for b in paths}
                interaction[target] = (vals['FF'] - vals['FP'] - vals['PF'] + vals['PP']).tolist()
            interaction['signed_CP_count_interaction'] = (
                len(paths['FF']['result']['chi_so']) - len(paths['FP']['result']['chi_so'])
                - len(paths['PF']['result']['chi_so']) + len(paths['PP']['result']['chi_so']))
            first = {b: paths[b]['result']['chi_so'] for b in paths}
            interaction['first_shift_defined'] = all(first.values())
            interaction['signed_first_CP_interaction'] = (
                first['FF'][0] - first['FP'][0] - first['PF'][0] + first['PP'][0]
                if all(first.values()) else None)
        else:
            interaction['reason'] = 'At least one native non-OK; CP/m contrast is undefined'
        output['interaction'] = interaction
        return output

    def case(self, item):
        oid = item['opaque_id']
        self.guard()
        path = Path(self.paths[oid]['files']['metrics.parquet']).resolve()
        assert any(path.is_relative_to(Path(p).resolve()) for p in self.source['source_roots_remote'])
        assert 'locked' not in path.parts and 'T-032' not in path.parts
        self.checked(path, item['files']['metrics.parquet']['sha256'], item['files']['metrics.parquet']['bytes'])
        df = pd.read_parquet(path)
        times = df['time'].to_numpy()
        assert len(times) == 1441 and np.isfinite(times).all()
        assert np.array_equal(times, times.astype(np.int64)) and np.all(np.diff(times) == 1)
        resolved = np.flatnonzero(times == item['proxy'])
        assert len(resolved) == 1
        cut = int(resolved[0])
        assert cut == self.paths[oid]['i_proxy'] == 720
        mats, metadata = matrices(df, cut)
        meta = self.metadata(df, cut, mats, metadata)
        raw_columns = phat_hien.cot_bocpd(df.columns)
        paths = self.diagonal(item, mats, times, raw_columns, cut)
        case = {'status': 'RUNNING', 'index_map': {'i_proxy': cut, 't_proxy': int(times[cut])},
                'metadata': meta, 'branches': {}}
        self.status['cases'][oid] = case
        self.save_status()
        for branch in ('FP', 'PF'):
            self.guard()
            X = mats[branch].to_numpy()
            self.progress('FACTORIAL START ' + oid + '/' + branch)
            start = time.perf_counter()
            if oid == self.selected and self.reuse is not None:
                record = self.old_json(self.reuse, oid + '--' + branch + '.json')
                arrays = self.old_arrays(self.reuse, record)
                assert np.array_equal(arrays['X'], X, equal_nan=True)
                assert np.array_equal(arrays['times'], times[:cut]) and arrays['columns'].tolist() == list(mats[branch])
                result, checks = record['result'], dict(record['checks'])
                record_source = str((self.reuse['directory'] / (oid + '--' + branch + '.json')).relative_to(self.home))
                record = dict(record, reused_record=record_source, reuse_wall_s=time.perf_counter() - start)
            else:
                d, T = X.shape[1], len(X)
                upper = 2*(T+1)**2*8 + T*4*(2*d*d + 2*d + 4)*8 + T*d*8 + 2**20
                self.guard(upper + 512*2**20)
                def tick(i):
                    self.guard()
                    self.progress(f'FACTORIAL {oid}/{branch} i={i}/{T}')
                result, arrays = observed(X, times[:cut], len(raw_columns), list(mats[branch]),
                                          tick=tick, detector_columns=raw_columns)
                observed_wall = time.perf_counter() - start
                destination = self.run / (oid + '--' + branch + '.npz')
                assert not destination.exists()
                np.savez_compressed(destination, **arrays)
                checks = {'input': np.array_equal(arrays['X'], X, equal_nan=True),
                          'time': np.array_equal(arrays['times'], times[:cut]),
                          'processed_columns': arrays['columns'].tolist() == list(mats[branch]),
                          'native_raw_columns': result['detector_columns'] == raw_columns}
                if self.args.first:
                    self.guard()
                    direct, R, mx = plain(X, times[:cut], len(raw_columns), list(mats[branch]), detector_columns=raw_columns)
                    checks.update({'same_input_' + k: v for k, v in compare_same_input(result, arrays, direct, R, mx).items()})
                    self.guard()
                record = {'status': 'PASS' if all(checks.values()) else 'FAIL', 'opaque_id': oid,
                          'branch': branch, 'result': result, 'checks': checks, 'npz': destination.name,
                          'sha256': sha(destination), 'bytes': destination.stat().st_size,
                          'observed_wall_s': observed_wall, 'wall_s': time.perf_counter() - start,
                          'rss_peak_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                          'theta_points': arrays['theta_points'].tolist(),
                          'normalization_max_abs_error': float(np.max(np.abs(arrays['normalization_error']))) if result['status'] == 'OK' else None}
                write_new(self.run / (oid + '--' + branch + '.json'), record)
            case['branches'][branch] = record
            self.save_status()
            assert record['status'] == 'PASS' and all(checks.values()), ('Wrapper validation failed', oid, branch, checks)
            paths[branch] = {'result': result, 'provenance': record.get('reused_record', self.args.run)}
            if result['status'] == 'OK':
                paths[branch].update(m=arrays['m'], CP_flags=arrays['CP_flags'])
            del arrays
            self.progress('FACTORIAL PASS ' + oid + '/' + branch + ' native_status=' + result['status'])
        identity = self.identity(mats, paths)
        comparisons = self.contrasts(paths)
        branches = {}
        for branch, entry in paths.items():
            branches[branch] = dict(entry, metadata=metadata[branch],
                                   native_error=entry['result'].get('error'),
                                   valid_computational_output=entry['result']['status'] == 'OK',
                                   no_input_channels=metadata[branch]['no_input_channels'],
                                   range0_processing=bool(metadata[branch]['range0_columns']))
        write_new(self.run / (oid + '--factorial.json'), {
            'status': 'PASS', 'opaque_id': oid, 'index_map': case['index_map'], 'metadata': meta,
            'branches': branches, 'same_input_checks': identity, 'contrasts': comparisons,
            'interpretation': 'Scale effects conditional on mask; mask bundles columns/d/prior; no onset or physical cause assertion'})
        case.update(status='PASS', same_input_checks=identity,
                    factorial_record=oid + '--factorial.json')
        self.status['resources'] = self.guard()
        self.save_status()

    def execute(self):
        try:
            self.setup()
            if self.args.first:
                self.fixtures()
            else:
                write_new(self.run / 'fixtures.json', {
                    'status': 'PASS', 'reused_from': self.args.verified_first + '/fixtures.json',
                    'sha256': self.reuse['manifest']['fixtures.json']['sha256'],
                    'same_native_wrapper_and_factorial_helper_hashes': True})
            cases = [c for c in self.source['cases'] if not self.args.first or c['opaque_id'] == self.selected]
            if self.args.cases:
                wanted = set(self.args.cases.split(','))
                assert wanted <= {c['opaque_id'] for c in cases} and wanted
                cases = [c for c in cases if c['opaque_id'] in wanted]
            for item in sorted(cases, key=lambda c: c['opaque_id']):
                self.case(item)
            for path, meta in self.inputs.items():
                assert sha(path) == meta['sha256'], 'Old source changed during run: ' + path
            self.status['status'] = 'PASS'
        except BaseException as exc:
            self.status.update(status='STOPPED', error=type(exc).__name__ + ': ' + str(exc))
            traceback.print_exc()
            self.progress('FACTORIAL STOP ' + self.status['error'])
            raise
        finally:
            self.status.update(ended_utc=now(), wall_s=time.perf_counter() - self.begin,
                               input_files=self.inputs)
            self.save_status()
            self.progress('FACTORIAL ' + self.status['status'] + ' ' + self.args.run)
            write_new(self.run / 'manifest.json', {
                p.name: {'sha256': sha(p), 'bytes': p.stat().st_size}
                for p in self.run.iterdir() if p.is_file() and p.name not in ('manifest.json', 'stdout.txt', 'stderr.txt')})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--first', action='store_true')
    mode.add_argument('--rest', action='store_true')
    parser.add_argument('--cases')
    parser.add_argument('--core-first', default='bocpd-first-002')
    parser.add_argument('--core-rest', default='bocpd-rest-001')
    parser.add_argument('--core-first-sha256', required=True)
    parser.add_argument('--core-rest-sha256', required=True)
    parser.add_argument('--source-sha256', required=True)
    parser.add_argument('--first-compute-status-sha256', required=True)
    parser.add_argument('--preflight-inventory-sha256', required=True)
    parser.add_argument('--preflight-verification-sha256', required=True)
    parser.add_argument('--verified-first')
    parser.add_argument('--verified-first-sha256')
    args = parser.parse_args()
    assert bool(args.verified_first) == bool(args.verified_first_sha256)
    assert not args.first or not args.verified_first, 'First must validate the new branches directly'
    for name in (args.run, args.core_first, args.core_rest, args.verified_first):
        if name is not None:
            assert name and '/' not in name and '\\' not in name and name not in ('.', '..')
    home = Path(os.environ['T033_HOME']).resolve()
    assert home.name == 'T-033' and os.name == 'posix'
    run = home / 'runs' / args.run
    run.mkdir(parents=True, exist_ok=False)
    try:
        with (run / 'stdout.txt').open('x', encoding='utf-8') as stdout, (run / 'stderr.txt').open('x', encoding='utf-8') as stderr:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                driver = Driver(args, run)
                try:
                    driver.execute()
                finally:
                    stdout.flush(); stderr.flush()
    finally:
        # Closed logs are hashed on both successful and stopped runs.
        write_new(run / 'logs-manifest.json', {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size}
                                              for p in (run / 'stdout.txt', run / 'stderr.txt') if p.is_file()})


if __name__ == '__main__':
    main()