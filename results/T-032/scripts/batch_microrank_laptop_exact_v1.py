"""Q-124 laptop exact cohort: guarded preparation, pilot checkpoint, then resume.

The wrapper runs only in guarded child processes. This module has stdlib-only
top-level imports; psutil is used only for process/resource supervision. It
does not SSH, install packages, change thread variables, pass labels to methods,
apply numerical tolerance, retry a case or start A-prime. Every failure stops
the whole branch. The first segment always stops after one Nezha pilot.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import subprocess
import sys
import time
import traceback

REPO = Path('D:/RCA-flashticket')
BASE = REPO / 'results/T-032'
OUT = BASE / 'runs/microrank-laptop-cohort-001'
PYTHON = Path('D:/RCA-ext/envs/T-014-main/Scripts/python.exe')
WRAPPER = BASE / 'scripts/replay_microrank_laptop_exact_v1.py'
CATALOG = BASE / 'runs/microrank-cohort-failure-001/cohort/52-cases.json'
CATALOG_SHA256 = '9208b29b1a123a8ff3eff97b5159d83389eba94eada36a3efff63aa1af5125bf'
TRANSPORT = BASE / 'runs/microrank-cohort-failure-001/transport-check.json'
TRANSPORT_SHA256 = '21098b72ee3823ab096557538273458bc531440ee50e91dba546b6d023815612'
PROPOSAL = BASE / 'de-xuat-microrank-laptop-cohort-001.md'
PROPOSAL_SHA256 = 'c113d20c6ef6d4ce2b2db8e55c020e8425b11abbeeb8ab036faf997fc8d44bc1'
RETROSPECTIVE = ('RE2-TT', 'dev-3defe3d34b')
PILOT = ('Nezha-OB', 'dev-14701a3bbb')
THREAD_NAMES = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')
MAX_WALL_S = 10800
MAX_NEW_BYTES = 2684354560
MAX_LOCAL_BYTES = 4294967296
MAX_TOTAL_BYTES = 12884901888
MAX_CASE_S = 600
MAX_CASE_BYTES = 157286400
MAX_TREE_RSS = 4286316544
MIN_AVAILABLE_RAM = 4554752000
MIN_REMAINING_RAM = 268435456
RESERVE_BYTES = 65536
POLL_S = 0.5
BUDGET_FRESH_S = 300
EXACT_FIELDS = (
    'opaque_id', 'method', 'method_version', 'variant', 'mode', 'detector',
    'detector_columns', 'seed', 'hashseed', 'config_id', 'why_ids', 'window',
    'input_shape', 'status', 'method_status_raw', 'error', 'ranking_native',
    'ranking', 'entity_ranking', 'blocks', 'sets', 'diagnostics', 'extra', 'input_sha256',
)
EXCLUDED_FIELDS = {'run_id': 'new execution identifier', 'cost': 'new measured execution cost'}


class CohortError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise CohortError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    def invalid(token):
        raise CohortError('nonfinite JSON token: ' + token)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), parse_constant=invalid)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def safe_output(path):
    path = Path(path)
    require(path.resolve().is_relative_to(OUT.resolve()) and not path.is_symlink(), 'output outside approved cohort')
    return path


def dump_new(path, value):
    path = safe_output(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def dump_view(path, value):
    path = safe_output(path)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def logical_size(directory):
    total = 0
    for parent, directories, files in os.walk(directory):
        require(not Path(parent).is_symlink(), 'symlink in task directory')
        require(all(not (Path(parent) / name).is_symlink() for name in directories), 'symlink task subdirectory')
        for name in files:
            path = Path(parent) / name
            require(not path.is_symlink(), 'symlink task artifact')
            try:
                total += path.stat().st_size
            except FileNotFoundError:
                pass
    return total


def manifest(directory, excluded=()):
    excluded = set(excluded)
    return [{'path': path.relative_to(directory).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}
            for path in sorted(directory.rglob('*')) if path.is_file()
            and path.relative_to(directory).as_posix() not in excluded]


def verify_manifest(directory, rows, excluded=()):
    seen = set()
    for row in rows:
        relative = PurePosixPath(row['path'])
        require(not relative.is_absolute() and '..' not in relative.parts and '\\' not in row['path']
                and row['path'] not in seen, 'invalid/duplicate artifact path')
        path = directory / relative
        require(path.resolve().is_relative_to(directory.resolve()) and not path.is_symlink(), 'artifact redirected/escaped')
        require(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], 'artifact changed: ' + row['path'])
        seen.add(row['path'])
    actual = {p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file()}
    require(actual == seen | set(excluded), 'artifact manifest missing/extra files')


def exact_differences(expected, actual, pointer=''):
    differences = []
    if type(expected) is not type(actual):
        return [{'pointer': pointer, 'kind': 'type', 'expected_type': type(expected).__name__, 'actual_type': type(actual).__name__}]
    if isinstance(expected, dict):
        if set(expected) != set(actual):
            differences.append({'pointer': pointer, 'kind': 'keys'})
        for key in sorted(set(expected) & set(actual)):
            differences.extend(exact_differences(expected[key], actual[key], pointer + '/' + str(key)))
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            differences.append({'pointer': pointer, 'kind': 'length'})
        for index, (left, right) in enumerate(zip(expected, actual)):
            differences.extend(exact_differences(left, right, pointer + '/' + str(index)))
    elif isinstance(expected, float):
        if expected.hex() != actual.hex():
            differences.append({'pointer': pointer, 'kind': 'float_exact', 'expected_hex': expected.hex(), 'actual_hex': actual.hex()})
    elif expected != actual:
        differences.append({'pointer': pointer, 'kind': 'value'})
    return differences


def compare_records(frozen, record):
    require(set(frozen) == set(EXACT_FIELDS) | set(EXCLUDED_FIELDS)
            and set(record) == set(EXACT_FIELDS) | set(EXCLUDED_FIELDS), 'record field schema differs')
    return exact_differences({key: frozen[key] for key in EXACT_FIELDS}, {key: record[key] for key in EXACT_FIELDS})


def child_gate(check, dataset, opaque_id, mode, job_sha, frozen_sha, frozen, record, native=None):
    require(check.get('status') == 'PASS' and check.get('passed') is True, 'child did not pass')
    require(check['dataset'] == dataset and check['opaque_id'] == opaque_id and check['mode'] == mode
            and check['job_sha256'] == job_sha and check['frozen_sha256'] == frozen_sha,
            'closed child identity/source/job binding differs')
    require(check.get('source_checks_passed') is True and check.get('frozen_exact') is True,
            'child source/exact invariants missing')
    require(check.get('differences') == [] and check.get('native_observed_differences') == []
            and check.get('worker_streams_closed') is True, 'child exact differences/stream closure failed')
    require(not compare_records(frozen, record), mode + ' parent frozen exact comparison failed')
    if mode == 'native':
        require(check.get('native_observer_absent') is True and check.get('native_frozen_exact') is True,
                'native observer/exact invariants missing')
    else:
        require(mode == 'observed' and check.get('observed_frozen_exact') is True
                and check.get('native_observed_exact') is True and check.get('capture_check', {}).get('pass') is True,
                'observed exact/capture invariant missing')
        require(native is not None and not compare_records(native, record), 'parent native-observed exact failed')


def lock_plan():
    require(sha(CATALOG) == CATALOG_SHA256 and sha(TRANSPORT) == TRANSPORT_SHA256 and sha(PROPOSAL) == PROPOSAL_SHA256,
            'catalog/transport/approved proposal pin differs')
    receipt = read(TRANSPORT)
    binding = [row for row in receipt['files'] if Path(row['local']).resolve() == CATALOG.resolve()]
    require(receipt['status'] == 'PASS' and len(binding) == 1 and binding[0]['pass'] is True
            and binding[0]['sha256'] == CATALOG_SHA256 and binding[0]['bytes'] == CATALOG.stat().st_size, 'catalog transport binding failed')
    rows = [{'dataset': r['dataset'], 'opaque_id': r['opaque_id'], 'source_status': r['source_status'],
             'source_sha256': r['source_sha256'], 'authority_pointer': '/rows/' + str(i)} for i, r in enumerate(read(CATALOG)['rows'])]
    require(len(rows) == 52 and len({(r['dataset'], r['opaque_id']) for r in rows}) == 52, 'catalog is not unique 52')
    require(sum(r['dataset'] == 'RE2-TT' for r in rows) == 30 and sum(r['dataset'] == 'Nezha-OB' for r in rows) == 22, 'dataset counts differ')
    require(all(re.fullmatch(r'dev-[0-9a-f]{10}', r['opaque_id']) and re.fullmatch(r'[0-9a-f]{64}', r['source_sha256']) for r in rows), 'invalid source identity')
    require(all(r['source_status'] in ('OK', 'ERROR', 'NO_EVIDENCE', 'UNSUPPORTED', 'TIMEOUT') for r in rows), 'undeclared source status')
    rows.sort(key=lambda r: (r['dataset'], r['opaque_id']))
    require(RETROSPECTIVE in {(r['dataset'],r['opaque_id']) for r in rows}, 'retrospective absent')
    nezha_ok = [(r['dataset'],r['opaque_id']) for r in rows if r['dataset'] == 'Nezha-OB' and r['source_status'] == 'OK']
    require(min(nezha_ok) == PILOT, 'Nezha pilot not locked smallest source OK')
    return {'schema': 'T032-MicroRank-laptop-exact-plan-v1', 'authority': 'Q-124', 'source_catalog': str(CATALOG),
            'source_catalog_sha256': CATALOG_SHA256, 'transport_sha256': TRANSPORT_SHA256,
            'ordering': 'dataset then opaque_id; retrospective and pilot are fixed initial exceptions', 'rows': rows}


def initial_rows(plan):
    return [{**row, 'case_status': 'not_run', 'laptop_status': None, 'classification': 'not_run',
             'matched_score_count': None, 'max_ulp_distance': None, 'max_relative': None,
             'native_frozen_exact': None, 'observed_frozen_exact': None, 'native_observed_exact': None,
             'capture_pass': None, 't028_pass': None, 'intermediates_eligible': False, 'reason': 'not run',
             'artifacts': None} for row in plan['rows']]


def verdict_gate(check):
    require(check.get('status') == 'PASS' and check.get('passed') is True, 'audit not PASS')
    for key in ('native_frozen_exact', 'observed_frozen_exact', 'native_observed_exact', 'capture_pass', 't028_pass'):
        require(check.get(key) is True, 'audit invariant missing/failed: ' + key)
    for key in ('numeric_differences', 'service_order_tie_differences', 'other_differences'):
        require(check.get(key) == [], 'audit differences found: ' + key)
    numeric = check['numeric_summary']
    count = numeric['matched_score_count']
    require(type(count) is int and count >= 0, 'invalid matched score count')
    if count:
        require(numeric['max_ulp_distance'] == 0 and numeric['max_relative'] == 0, 'exact audit had nonzero score deviation')
    else:
        require(numeric['max_ulp_distance'] is None and numeric['max_relative'] is None, 'no score pairs must remain null')
    return numeric


def read_budget(path, expected):
    path = Path(path).resolve()
    require(path.is_relative_to(BASE.resolve()) and not path.is_symlink() and sha(path) == expected, 'budget source unsafe/pin differs')
    value = read(path)
    require(value['schema'] == 'T032-laptop-cohort-budget-v1' and value['remote_scope'] == '/home/ubuntu/rca/T-032', 'budget schema/scope differs')
    stamp = datetime.fromisoformat(value['measured_utc'].replace('Z', '+00:00'))
    require(stamp.tzinfo is not None and 0 <= (datetime.now(timezone.utc) - stamp).total_seconds() <= BUDGET_FRESH_S, 'budget measurement is not just before segment launch')
    for key in ('remote_task_bytes', 'remote_growth_reserve_bytes', 'local_task_bytes', 'package_baseline_task_bytes'):
        require(type(value[key]) is int and value[key] >= 0, 'invalid measured budget scalar: ' + key)
    snapshot = Path(value['remote_snapshot_path']).resolve()
    require(snapshot.is_relative_to(BASE.resolve()) and sha(snapshot) == value['remote_snapshot_sha256'], 'remote actual measurement receipt differs')
    remote = read(snapshot)
    require(remote['remote_scope'] == value['remote_scope'] and remote['remote_task_bytes'] == value['remote_task_bytes']
            and remote['measured_utc'] == value['measured_utc'], 'budget does not bind actual remote snapshot')
    actual_local = logical_size(BASE)
    require(actual_local >= value['local_task_bytes'] and actual_local - value['local_task_bytes'] <= 1024 * 1024,
            'local measurement no longer matches fresh task size')
    require(actual_local <= MAX_LOCAL_BYTES and value['package_baseline_task_bytes'] <= actual_local, 'local/baseline budget invalid')
    return value


class Guard:
    def __init__(self, budget, wall_used_s, segment_started):
        import psutil
        self.psutil = psutil
        self.budget, self.wall_used_s, self.segment_started = budget, wall_used_s, segment_started
        self.child = None
        self.worker_processes = {}
        self.active_started = self.active_baseline = None
        self.peak_tree_rss = self.peak_local = self.peak_new = 0
        self.interrupted = None

    def check(self):
        require(self.interrupted is None, 'interrupted active work; no retry')
        elapsed = self.wall_used_s + time.perf_counter() - self.segment_started
        require(elapsed < MAX_WALL_S - 20, 'approved 3 hour package wall reached')
        current = logical_size(BASE)
        new = max(0, current - self.budget['package_baseline_task_bytes'])
        self.peak_local, self.peak_new = max(self.peak_local, current), max(self.peak_new, new)
        require(new + RESERVE_BYTES <= MAX_NEW_BYTES, 'approved 2.5 GiB package new-byte cap reached')
        require(current + RESERVE_BYTES <= MAX_LOCAL_BYTES, 'approved 4 GiB local cap reached')
        require(current + self.budget['remote_task_bytes'] + self.budget['remote_growth_reserve_bytes'] + RESERVE_BYTES <= MAX_TOTAL_BYTES,
                'approved combined 12 GiB cap reached')
        require(shutil.disk_usage(BASE).free >= MAX_CASE_BYTES + RESERVE_BYTES, 'disk reserve insufficient for one case')
        require(self.psutil.virtual_memory().available >= MIN_REMAINING_RAM, 'remaining RAM guard reserve reached')
        if self.active_started is not None:
            require(time.perf_counter() - self.active_started < MAX_CASE_S - 20, 'case 600 s budget reached')
            require(max(0, current - self.active_baseline) + RESERVE_BYTES <= MAX_CASE_BYTES, 'case 150 MiB cap reached')
        if self.child is not None and self.child.poll() is None:
            try:
                parent = self.psutil.Process(self.child.pid)
                tree = [parent] + parent.children(recursive=True)
                for process in tree:
                    self.worker_processes[process.pid] = process.create_time()
                rss = sum(p.memory_info().rss for p in tree if p.is_running())
                self.peak_tree_rss = max(self.peak_tree_rss, rss)
                require(rss <= MAX_TREE_RSS, 'worker tree RSS above approved bound')
            except self.psutil.NoSuchProcess:
                pass

    def before_worker(self):
        self.check()
        require(self.psutil.virtual_memory().available >= MIN_AVAILABLE_RAM, 'available RAM below 4,554,752,000 B; no worker launch')
        require(all(os.environ.get(name) is None for name in THREAD_NAMES), 'current thread variables must all remain unset')

    def stop_child(self):
        processes = []
        if self.child is not None and self.child.poll() is None:
            try:
                parent = self.psutil.Process(self.child.pid)
                for process in [parent] + parent.children(recursive=True):
                    self.worker_processes[process.pid] = process.create_time()
            except self.psutil.NoSuchProcess:
                pass
        for pid, created in self.worker_processes.items():
            try:
                process = self.psutil.Process(pid)
                if process.create_time() == created and process.is_running():
                    processes.append(process)
            except self.psutil.NoSuchProcess:
                pass
        for process in processes:
            try:
                process.terminate()
            except self.psutil.NoSuchProcess:
                pass
        _gone, alive = self.psutil.wait_procs(processes, timeout=5)
        for process in alive:
            try:
                process.kill()
            except self.psutil.NoSuchProcess:
                pass
        if alive:
            _gone, alive = self.psutil.wait_procs(alive, timeout=5)
        require(not alive, 'could not stop recorded worker tree; manual inspection required')
        if self.child is not None:
            self.child.wait(timeout=5)

    def children_closed(self):
        for pid, created in self.worker_processes.items():
            try:
                process = self.psutil.Process(pid)
                if process.create_time() == created and process.is_running():
                    return False
            except self.psutil.NoSuchProcess:
                pass
        return self.child is None or self.child.poll() is not None

    def report(self):
        return {'wall_used_s': self.wall_used_s + time.perf_counter() - self.segment_started,
                'peak_tree_rss_bytes': self.peak_tree_rss, 'peak_local_bytes': self.peak_local,
                'peak_new_task_bytes': self.peak_new, 'new_task_bytes_now': max(0, logical_size(BASE) - self.budget['package_baseline_task_bytes']),
                'remote_task_bytes_measured': self.budget['remote_task_bytes'], 'remote_growth_reserve_bytes': self.budget['remote_growth_reserve_bytes'],
                'max_wall_s': MAX_WALL_S, 'max_new_bytes': MAX_NEW_BYTES, 'max_local_bytes': MAX_LOCAL_BYTES,
                'max_total_bytes': MAX_TOTAL_BYTES, 'min_available_ram_before_worker': MIN_AVAILABLE_RAM,
                'max_tree_rss': MAX_TREE_RSS, 'poll_s': POLL_S, 'polling_can_overshoot': True, 'filesystem_quota_claimed': False}


def selfcheck():
    good = {'status': 'PASS', 'passed': True, 'native_frozen_exact': True, 'observed_frozen_exact': True,
            'native_observed_exact': True, 'capture_pass': True, 't028_pass': True, 'numeric_differences': [],
            'service_order_tie_differences': [], 'other_differences': [],
            'numeric_summary': {'matched_score_count': 1, 'max_ulp_distance': 0, 'max_relative': 0.0}}
    verdict_gate(good)
    checks = []
    for key in ('native_frozen_exact', 'observed_frozen_exact', 'native_observed_exact', 'capture_pass', 't028_pass'):
        changed = {**good, key: False}
        try:
            verdict_gate(changed)
        except CohortError:
            checks.append(key)
        else:
            raise CohortError('failed gate would permit next case: ' + key)
    for key in ('numeric_differences', 'service_order_tie_differences', 'other_differences'):
        try:
            verdict_gate({**good, key: [{'mutation': True}]})
        except CohortError:
            checks.append(key)
        else:
            raise CohortError('difference would permit next case')
    require(exact_differences(0.0, -0.0) and exact_differences(1.0, math.nextafter(1.0, 2.0))
            and exact_differences(1, True) and exact_differences([1,2], [2,1]), 'exact controller gate insensitive')
    verdict_gate({**good, 'numeric_summary': {'matched_score_count': 0, 'max_ulp_distance': None, 'max_relative': None}})
    try:
        verdict_gate({**good, 'numeric_summary': {'matched_score_count': 0, 'max_ulp_distance': 0, 'max_relative': 0.0}})
    except CohortError:
        checks.append('empty score pairs cannot be zero')
    else:
        raise CohortError('null-score rule not enforced')
    fake_record = {key: None for key in EXACT_FIELDS + tuple(EXCLUDED_FIELDS)}
    fake_record['extra'] = {'zero': 0.0, 'count': 2, 'mapping': ['service-a','service-b']}
    fake_child = {'status':'PASS', 'passed':True, 'dataset':'RE2-TT', 'opaque_id':'dev-0000000000',
                  'mode':'native', 'job_sha256':'a'*64, 'frozen_sha256':'b'*64,
                  'source_checks_passed':True, 'frozen_exact':True, 'differences':[], 'native_observed_differences':[],
                  'worker_streams_closed':True, 'native_observer_absent':True, 'native_frozen_exact':True}
    def fake_gate(check, record):
        child_gate(check, 'RE2-TT', 'dev-0000000000', 'native', 'a'*64, 'b'*64, fake_record, record)
    fake_gate(fake_child, fake_record)
    mutations = [('failed child', {'status':'FAIL_STOP'}), ('failed source', {'source_checks_passed':False}),
                 ('job binding', {'job_sha256':'c'*64}), ('frozen binding', {'frozen_sha256':'c'*64}),
                 ('mode binding', {'mode':'observed'}), ('record identity', {'opaque_id':'dev-1111111111'}),
                 ('open worker streams', {'worker_streams_closed':False}), ('attached native observer', {'native_observer_absent':False})]
    for name, mutation in mutations:
        try:
            fake_gate({**fake_child, **mutation}, fake_record)
        except CohortError:
            checks.append('native blocks observed: ' + name)
        else:
            raise CohortError('native gate accepted mutation: ' + name)
    for name, extra in [('zero sign', {'zero':-0.0,'count':2,'mapping':['service-a','service-b']}),
                        ('count', {'zero':0.0,'count':3,'mapping':['service-a','service-b']}),
                        ('mapping order', {'zero':0.0,'count':2,'mapping':['service-b','service-a']}),
                        ('type', {'zero':0,'count':2,'mapping':['service-a','service-b']})]:
        try:
            fake_gate(fake_child, {**fake_record, 'extra':extra})
        except CohortError:
            checks.append('native blocks observed: record ' + name)
        else:
            raise CohortError('parent full-record gate accepted mutation: ' + name)
    return {'status': 'PASS_CONTROLLER_GATES_ONLY', 'checks': checks, 'method_calls': 0,
            'scope': 'pure stdlib fake-verdict gates; not observer/bridge/frozen fixture certification'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('selfcheck')
    run = sub.add_parser('run')
    run.add_argument('--budget-file', required=True)
    run.add_argument('--budget-sha256', required=True)
    run.add_argument('--wrapper-sha256', required=True)
    run.add_argument('--segment-id', required=True)
    run.add_argument('--resume', action='store_true')
    run.add_argument('--forecast-file')
    run.add_argument('--forecast-sha256')
    run.add_argument('--max-cases-this-segment', type=int, default=50,
                     help='operational checkpoint after this many closed remainder cases; no selection/skip/retry')
    args = parser.parse_args()
    if args.command == 'selfcheck':
        print(json.dumps(selfcheck(), ensure_ascii=False))
        return 0
    require(os.name == 'nt' and Path(sys.executable).resolve() == PYTHON.resolve(), 'source Windows interpreter required')
    require(os.environ.get('PYTHONHASHSEED') == '0' and os.environ.get('PYTHONDONTWRITEBYTECODE') == '1'
            and sys.dont_write_bytecode, 'startup hashseed/bytecode policy differs')
    require(all(os.environ.get(name) is None for name in THREAD_NAMES), 'thread variables must remain unset')
    require(re.fullmatch(r'[0-9]{3}', args.segment_id), 'invalid segment ID')
    require(1 <= args.max_cases_this_segment <= 50, 'segment checkpoint case count must be 1..50')
    require(re.fullmatch(r'[0-9a-f]{64}', args.wrapper_sha256) and sha(WRAPPER) == args.wrapper_sha256, 'wrapper pin differs')
    require(OUT.is_dir() and not OUT.is_symlink(), 'approved cohort metadata directory missing')
    segment = OUT / 'segments' / args.segment_id
    require(segment.is_dir() and (segment / 'launcher.json').is_file(), 'approved hidden launcher must bootstrap segment')
    started = time.perf_counter()
    budget = None
    plan = None
    rows = []
    state = {'status': 'STARTING', 'pid': os.getpid(), 'segment_id': args.segment_id, 'started_utc': now(),
             'active': None, 'completed_case_count': 0, 'pilot_checkpoint_required': True,
             'cohort_complete': False, 'a_prime_authorized': False, 'retry_allowed': False}
    guard = None
    active_row = None
    failed_child_check = None

    def save(event, **fields):
        state.update(updated_utc=now(), elapsed_segment_s=time.perf_counter()-started)
        dump_view(segment / 'status.json', state)
        dump_view(OUT / 'status.json', state)
        item = {'at_utc': now(), 'event': event, 'segment_id': args.segment_id, **fields}
        for path in (segment / 'progress.jsonl', OUT / 'progress.jsonl'):
            with path.open('a', encoding='utf-8', newline='\n') as stream:
                stream.write(json.dumps(item, ensure_ascii=False, allow_nan=False) + '\n')
        print(json.dumps(item, ensure_ascii=False, allow_nan=False), flush=True)

    def table():
        require(plan is not None and len(rows) == 52, 'cannot invent unverified 52-row plan')
        counts = {name: sum(row['classification'] == name for row in rows) for name in
                  ('exact', 'non_OK_exact', 'numeric_difference', 'service_order_tie_difference', 'other_error', 'not_run')}
        value = {'schema': 'T032-MicroRank-laptop-exact-52-v1', 'status': state['status'], 'rows': rows, 'counts': counts,
                 'all_52_complete': counts['exact'] + counts['non_OK_exact'] == 52,
                 'A_prime_authorized': False, 'plan_sha256': sha(OUT / 'plan-52.json'),
                 'limits': 'operational exactness counts are not mechanism proportions; numeric null when no audited score pairs'}
        dump_view(OUT / '52-cases.json', value)
        lines = ['# MicroRank laptop exact — 52 ca', '', '| Dataset | Ca | Nguồn | Laptop | Trạng thái | Cặp điểm | max ULP | max tương đối |',
                 '|---|---|---|---|---|---:|---:|---:|']
        for row in rows:
            display = lambda v: 'N/A' if v is None else str(v)
            lines.append('| ' + ' | '.join(display(row[k]) for k in ('dataset','opaque_id','source_status','laptop_status','classification',
                                                                   'matched_score_count','max_ulp_distance','max_relative')) + ' |')
        (OUT / '52-cases.md.tmp').write_text('\n'.join(lines) + '\n', encoding='utf-8')
        (OUT / '52-cases.md.tmp').replace(OUT / '52-cases.md')

    def run_worker(phase, command, work_directory):
        nonlocal failed_child_check
        failed_child_check = None
        guard.before_worker()
        require(sha(WRAPPER) == args.wrapper_sha256, 'wrapper changed before child')
        logs = segment / 'logs'
        logs.mkdir(exist_ok=True)
        token = phase.replace('/', '-').replace(':', '-')
        require(re.fullmatch(r'[A-Za-z0-9_-]+', token), 'invalid child phase')
        dump_new(logs / (token + '-command.json'), {'argv': command, 'at_utc': now(), 'cwd': str(REPO), 'phase': phase})
        state['active'] = {'phase': phase, 'command': command, 'directory': str(work_directory)}
        save('CHILD_START', phase=phase)
        child_started = time.perf_counter()
        with (logs / (token + '-stdout.txt')).open('x', encoding='utf-8') as stdout:
            with (logs / (token + '-stderr.txt')).open('x', encoding='utf-8') as stderr:
                guard.child = subprocess.Popen(command, cwd=REPO, env=os.environ.copy(), stdin=subprocess.DEVNULL,
                    stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
                process = guard.psutil.Process(guard.child.pid)
                guard.worker_processes[process.pid] = process.create_time()
                state['active']['pid'] = guard.child.pid
                dump_new(logs / (token + '-pid.json'), {'pid': guard.child.pid, 'argv': command, 'at_utc': now()})
                save('CHILD_RUNNING', phase=phase, child_pid=guard.child.pid)
                last = 0
                while guard.child.poll() is None:
                    guard.check()
                    if time.perf_counter()-child_started-last >= 10:
                        save('CHILD_POLL', phase=phase, guard=guard.report())
                        last = time.perf_counter()-child_started
                    time.sleep(POLL_S)
                code = guard.child.wait()
        cost = {'pid': guard.child.pid, 'exit_code': code, 'wall_s': time.perf_counter()-child_started,
                'phase': phase, 'peak_tree_rss_bytes_so_far': guard.peak_tree_rss}
        dump_new(logs / (token + '-process.json'), cost)
        guard.child = None
        guard.check()
        require(guard.children_closed(), phase + ' worker descendants remain; no next stage')
        if (work_directory / 'check.json').is_file():
            candidate_check = read(work_directory / 'check.json')
            require('artifact_manifest' in candidate_check, phase + ' missing full closed child manifest')
            require(candidate_check.get('manifest_excludes') == ['check.json'], phase + ' unexpected manifest exclusions')
            verify_manifest(work_directory, candidate_check['artifact_manifest'], candidate_check.get('manifest_excludes', ['check.json']))
            failed_child_check = candidate_check
        require(code == 0, phase + ' child failed; no next stage/retry')
        check = failed_child_check
        require(check is not None, phase + ' child missing closed check')
        require(check.get('status') == 'PASS' and check.get('passed') is True, phase + ' check not PASS')
        verify_manifest(work_directory, check['artifact_manifest'], check.get('manifest_excludes', ['check.json']))
        state['active'] = None
        save('CHILD_PASS', phase=phase)
        return check, cost

    def audit_row(row, check, directory, case_started, case_baseline):
        numeric = verdict_gate(check)
        require(check['dataset'] == row['dataset'] and check['opaque_id'] == row['opaque_id'], 'audit case identity differs')
        source_status = check.get('source_status', check.get('frozen_status'))
        require(source_status == row['source_status'], 'audit source status differs')
        require(check.get('intermediates_eligible') is (source_status == 'OK'), 'audit eligibility not consistent with exact source status')
        logs = segment / 'logs'
        selected_logs = [path for path in sorted(logs.glob('*')) if path.is_file()
                         and (row['opaque_id'] in path.name or 'retrospective' in path.name and (row['dataset'],row['opaque_id']) == RETROSPECTIVE)]
        dump_new(directory / 'stream-receipts.json', {'all_child_streams_closed': True,
            'files': [{'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)} for path in selected_logs],
            'manifest_note': 'external immutable segment logs bound here and in launcher final manifest'})
        dump_new(directory / 'case-terminal.json', {'status': 'PASS_EXACT' if source_status == 'OK' else 'PASS_NON_OK_EXACT',
            'at_utc': now(), 'dataset': row['dataset'], 'opaque_id': row['opaque_id'], 'source_status': source_status,
            'audit_check_sha256': sha(directory / 'audit/check.json'), 'wall_s': time.perf_counter()-case_started,
            'new_task_bytes_delta': max(0, logical_size(BASE)-case_baseline), 'guard': guard.report(),
            'intermediates_eligible': check['intermediates_eligible']})
        closed = {'status': 'CLOSED_EXACT_CASE', 'files': manifest(directory, ('closed.json',)), 'manifest_excludes': ['closed.json']}
        dump_new(directory / 'closed.json', closed)
        verify_manifest(directory, closed['files'], ['closed.json'])
        row.update(case_status='PASS', laptop_status=source_status,
            classification='exact' if source_status == 'OK' else 'non_OK_exact', matched_score_count=numeric['matched_score_count'],
            max_ulp_distance=numeric['max_ulp_distance'], max_relative=numeric['max_relative'], native_frozen_exact=True,
            observed_frozen_exact=True, native_observed_exact=True, capture_pass=True, t028_pass=True,
            intermediates_eligible=check['intermediates_eligible'], reason=None,
            artifacts={'path': str(directory), 'closed_sha256': sha(directory / 'closed.json'),
                       'audit_check_sha256': sha(directory / 'audit/check.json'), 'source': check.get('source'),
                       'native': check.get('native'), 'observed': check.get('observed')})
        state['completed_case_count'] = sum(r['case_status'] == 'PASS' for r in rows)
        table()

    def execute_case(row):
        nonlocal active_row
        active_row = row
        require(row['source_status'] != 'TIMEOUT', 'TIMEOUT native replay unsupported; stop before case')
        directory = OUT / 'cases' / row['dataset'] / row['opaque_id']
        require(not directory.exists(), 'case directory exists; no replay/retry')
        guard.before_worker()
        case_started, case_baseline = time.perf_counter(), logical_size(BASE)
        guard.active_started, guard.active_baseline = case_started, case_baseline
        directory.mkdir(parents=True)
        command = [str(PYTHON), '-B', '-W', 'ignore', '-X', 'utf8', str(WRAPPER)]
        prepared, _cost = run_worker('prepare-' + row['opaque_id'], command + ['prepare', row['dataset'], row['opaque_id'], str(directory / 'prepare')], directory / 'prepare')
        payload = read(directory / 'prepare/prepare.json')
        require(payload['entry']['sha256'] == row['source_sha256'] and payload['frozen']['status'] == row['source_status'], 'prepared frozen source differs from locked catalog')
        dump_new(directory / 'source-binding.json', {'entry': payload['entry'], 'source_checks': payload['source_checks'],
                 'input_checks': payload['input_checks'], 'code_hashes': payload['code_hashes'], 'frozen': payload['frozen']})
        for mode in ('native', 'observed'):
            mode_dir = directory / mode
            mode_dir.mkdir()
            if mode == 'native':
                dump_new(mode_dir / 'job.json', payload['job'])
            else:
                shutil.copyfile(directory / 'native/job.json', mode_dir / 'job.json')
                require(sha(mode_dir / 'job.json') == sha(directory / 'native/job.json'), 'observed job not byte-identical')
            job_sha = sha(mode_dir / 'job.json')
            child_check, _cost = run_worker(mode + '-' + row['opaque_id'], command + ['child', mode, row['dataset'], row['opaque_id'], str(mode_dir),
                '--job-sha256', job_sha, '--frozen-sha256', row['source_sha256']], mode_dir)
            child_gate(child_check, row['dataset'], row['opaque_id'], mode, job_sha, row['source_sha256'],
                       payload['frozen'], read(mode_dir / 'ban-ghi-0.json'),
                       read(directory / 'native/ban-ghi-0.json') if mode == 'observed' else None)
            guard.check()
        check, _cost = run_worker('audit-' + row['opaque_id'], command + ['audit', row['dataset'], row['opaque_id'],
            str(directory / 'native'), str(directory / 'observed'), str(directory / 'audit')], directory / 'audit')
        audit_row(row, check, directory, case_started, case_baseline)
        guard.check()
        guard.active_started = guard.active_baseline = None
        active_row = None
        return {**read(directory / 'case-terminal.json'),
                'controller_case_closed_wall_s': time.perf_counter() - case_started,
                'controller_case_closed_new_task_bytes': max(0, logical_size(BASE) - case_baseline),
                'case_closed_sha256': sha(directory / 'closed.json'),
                'measurement_note': 'controller measurements include case manifest verification and table update; terminal.json cost precedes final case seal'}

    try:
        plan = lock_plan()
        rows = initial_rows(plan)
        if args.resume and (OUT / '52-cases.json').is_file():
            prior_table_rows = read(OUT / '52-cases.json')['rows']
            require(len(prior_table_rows) == 52 and all(
                all(old[key] == locked[key] for key in locked)
                for old, locked in zip(prior_table_rows, plan['rows'])), 'resume immutable row/source fields differ')
            rows = prior_table_rows
        budget = read_budget(args.budget_file, args.budget_sha256)
        wall_used = 0.0
        if args.resume:
            require((OUT / 'status.json').exists(), 'no valid checkpoint to resume')
            require(not list((OUT / 'segments').rglob('supervisor-failure.json')),
                    'appended supervisor failure blocks whole branch; no retry/resume')
            require(not any(read(path).get('status') == 'FAIL_STOP'
                            for path in (OUT / 'segments').rglob('launcher-terminal.json')),
                    'failed launcher segment blocks whole branch; no retry/resume')
            prior = read(OUT / 'status.json')
            require(prior['status'] in ('STOP_CHECKPOINT_PILOT', 'STOP_CHECKPOINT_BETWEEN_CASES'), 'failure/incomplete active branch cannot resume')
            require(args.forecast_file and args.forecast_sha256, 'root pilot forecast required before remainder')
            forecast = read(Path(args.forecast_file))
            require(Path(args.forecast_file).resolve().is_relative_to(BASE.resolve()) and not Path(args.forecast_file).is_symlink(),
                    'forecast outside approved task')
            require(sha(Path(args.forecast_file)) == args.forecast_sha256 and forecast['status'] == 'ROOT_VERIFIED_WITHIN_Q124_BUDGET'
                    and forecast['root_verified'] is True and forecast['metadata_scale_coverage_considered'] is True, 'root forecast not verified')
            require(forecast['plan_sha256'] == sha(OUT / 'plan-52.json') and forecast['remaining_wall_s_estimate'] >= 0
                    and forecast['remaining_new_bytes_estimate'] >= 0, 'forecast plan/estimates invalid')
            require(len(rows) == 52 and [(r['dataset'],r['opaque_id']) for r in rows] == [(r['dataset'],r['opaque_id']) for r in plan['rows']], 'resume table/plan differs')
            prior_segment = OUT / 'segments' / prior['segment_id']
            terminal = read(prior_segment / 'terminal.json')
            launcher_closed = read(prior_segment / 'launcher-closed.json')
            require(terminal['status'] == prior['status'] and terminal['active'] is None
                    and terminal['all_children_closed'] is True and launcher_closed['status'] == prior['status'],
                    'prior terminal not between closed cases')
            verify_manifest(prior_segment, launcher_closed['files'], ['launcher-closed.json'])
            require(not exact_differences(read(OUT / '52-cases.json'), read(prior_segment / 'table-final.json')),
                    'resume live table differs from immutable closed segment table')
            wall_used = terminal['guard']['wall_used_s']
            original_pins = read(OUT / 'source-pin-manifest.json')
            require(original_pins['wrapper_sha256'] == args.wrapper_sha256
                    and original_pins['controller_sha256'] == sha(__file__)
                    and original_pins['package_baseline_task_bytes'] == budget['package_baseline_task_bytes'],
                    'resume changed tool pins or package baseline')
            require(forecast['pilot_closed_sha256'] == sha(OUT / 'cases' / PILOT[0] / PILOT[1] / 'closed.json')
                    and forecast['fixture_check_sha256'] == sha(OUT / 'tool-check/runtime-001/check.json')
                    and forecast['retrospective_check_sha256'] == sha(OUT / 'retrospective-dev-3defe3d34b/audit/check.json'),
                    'root forecast does not bind valid pilot/fixture/retrospective')
            require(wall_used + forecast['remaining_wall_s_estimate'] <= MAX_WALL_S
                    and logical_size(BASE)-budget['package_baseline_task_bytes']+forecast['remaining_new_bytes_estimate'] <= MAX_NEW_BYTES,
                    'remaining forecast exceeds package budget')
            for row in rows:
                require(row['case_status'] in ('PASS','not_run'), 'blocked/partial case forbids whole branch resume')
                if row['case_status'] == 'PASS':
                    directory = Path(row['artifacts']['path'])
                    require(sha(directory / 'closed.json') == row['artifacts']['closed_sha256'], 'closed case pin changed')
                    verify_manifest(directory, read(directory / 'closed.json')['files'], ['closed.json'])
                    for file in read(directory / 'stream-receipts.json')['files']:
                        require(Path(file['path']).resolve().is_relative_to(OUT.resolve())
                                and sha(Path(file['path'])) == file['sha256'] and Path(file['path']).stat().st_size == file['bytes'],
                                'closed case external stream/log changed')
            require(not exact_differences(read(OUT / 'plan-52.json'), plan), 'locked plan changed')
            dump_new(segment / 'resume-source.json', {'prior_status': prior, 'prior_terminal_sha256': sha(prior_segment / 'terminal.json'),
                'forecast': forecast, 'forecast_sha256': args.forecast_sha256, 'closed_cases_checked': sum(r['case_status']=='PASS' for r in rows)})
        else:
            require(not (OUT / 'plan-52.json').exists() and not (OUT / 'status.json').exists(), 'initial branch already initialized; no retry')
            dump_new(OUT / 'plan-52.json', plan)
            dump_new(OUT / 'source-pin-manifest.json', {'authority': 'Q-124', 'catalog_sha256': CATALOG_SHA256,
                'transport_sha256': TRANSPORT_SHA256, 'proposal_sha256': PROPOSAL_SHA256,
                'wrapper_sha256': args.wrapper_sha256, 'controller_sha256': sha(__file__), 'exact_fields': EXACT_FIELDS,
                'excluded_fields': ['run_id','cost'], 'case_count': 52, 'no_tolerance': True,
                'package_baseline_task_bytes': budget['package_baseline_task_bytes']})
        guard = Guard(budget, wall_used, started)
        for signum in (signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, lambda number, _frame: setattr(guard, 'interrupted', number))
        dump_new(segment / 'command.json', {'argv': sys.argv, 'controller_sha256': sha(__file__), 'wrapper_sha256': args.wrapper_sha256,
            'pid': os.getpid(), 'budget': budget, 'budget_sha256': args.budget_sha256, 'at_utc': now()})
        (segment / 'controller.pid').write_text(str(os.getpid()) + '\n', encoding='utf-8')
        state['completed_case_count'] = sum(r['case_status']=='PASS' for r in rows)
        save('START')
        table()
        guard.check()
        command = [str(PYTHON), '-B', '-W', 'ignore', '-X', 'utf8', str(WRAPPER)]
        if not args.resume:
            check, _cost = run_worker('fixture-full52', command + ['fixture', str(OUT / 'tool-check/runtime-001')], OUT / 'tool-check/runtime-001')
            require(check.get('frozen_self_check_count') == 52 and check.get('all_fixture_checks_passed') is True,
                    'full fixtures or 52 frozen T028 self-check not passed')
            require(check.get('original_comparator_fixtures_pass') is True, 'original comparator fixtures did not all pass')
            retrospective_started, retrospective_baseline = time.perf_counter(), logical_size(BASE)
            guard.active_started, guard.active_baseline = retrospective_started, retrospective_baseline
            active_row = next(r for r in rows if (r['dataset'],r['opaque_id']) == RETROSPECTIVE)
            check, _cost = run_worker('retrospective', command + ['audit-retrospective', str(OUT / 'retrospective-dev-3defe3d34b/audit')],
                    OUT / 'retrospective-dev-3defe3d34b/audit')
            row = next(r for r in rows if (r['dataset'],r['opaque_id']) == RETROSPECTIVE)
            audit_row(row, check, OUT / 'retrospective-dev-3defe3d34b', retrospective_started, retrospective_baseline)
            guard.check()
            guard.active_started = guard.active_baseline = None
            active_row = None
            row = next(r for r in rows if (r['dataset'],r['opaque_id']) == PILOT)
            benchmark = execute_case(row)
            dump_new(OUT / 'benchmark.json', {'dataset': PILOT[0], 'opaque_id': PILOT[1], 'measured': benchmark,
                'pilot_is_not_upper_bound': True, 'remaining_new_cases': 50,
                'requires_root_forecast_before_remainder': True})
            state['status'] = 'STOP_CHECKPOINT_PILOT'
            save('STOP_CHECKPOINT_PILOT', benchmark_sha256=sha(OUT / 'benchmark.json'))
        else:
            segment_completed = 0
            for row in rows:
                if row['case_status'] == 'PASS':
                    continue
                execute_case(row)
                segment_completed += 1
                if segment_completed >= args.max_cases_this_segment:
                    break
            state['cohort_complete'] = all(row['case_status'] == 'PASS' for row in rows)
            state['status'] = 'PASS_FULL52_LAPTOP_EXACT' if state['cohort_complete'] else 'STOP_CHECKPOINT_BETWEEN_CASES'
            save('FINISHED_FULL52' if state['cohort_complete'] else 'STOP_CHECKPOINT_BETWEEN_CASES')
        table()
        dump_new(segment / 'table-final.json', read(OUT / '52-cases.json'))
        state['active'] = None
        dump_new(segment / 'terminal.json', {**state, 'guard': guard.report(), 'ended_utc': now(),
            'all_children_closed': guard.children_closed(), 'manifest_requires_launcher_stream_close': True, 'a_prime_authorized': False})
        return 0
    except BaseException as error:
        stop_error = None
        if guard is not None:
            try:
                guard.stop_child()
            except BaseException as stopping:
                stop_error = str(stopping)
        if active_row is not None:
            active_row.update(case_status='FAIL_STOP', classification='other_error', reason=str(error), intermediates_eligible=False)
            if failed_child_check is not None:
                if failed_child_check.get('service_order_tie_differences'):
                    active_row['classification'] = 'service_order_tie_difference'
                elif failed_child_check.get('numeric_differences') and not failed_child_check.get('other_differences'):
                    active_row['classification'] = 'numeric_difference'
                summary = failed_child_check.get('numeric_summary', {})
                if type(summary.get('matched_score_count')) is int and summary['matched_score_count'] > 0:
                    active_row.update(matched_score_count=summary['matched_score_count'], max_ulp_distance=summary.get('max_ulp_distance'),
                                      max_relative=summary.get('max_relative'))
                active_row['laptop_status'] = failed_child_check.get('record_status')
                active_row['failure_check'] = failed_child_check
        state.update(status='FAIL_STOP', error_type=type(error).__name__, error=str(error), active=None)
        if stop_error is not None:
            state['worker_stop_error'] = stop_error
        dump_new(segment / 'failure.json', {'error': str(error), 'traceback': traceback.format_exc(), 'state': state,
            'guard': None if guard is None else guard.report(), 'retained': 'all artifacts retained; branch stopped; no retry'})
        if plan is not None and len(rows) == 52:
            if not (OUT / 'plan-52.json').exists():
                dump_new(OUT / 'plan-52.json', plan)
            table()
        save('FAIL_STOP', error=str(error))
        dump_new(segment / 'terminal.json', {**state, 'guard': None if guard is None else guard.report(), 'ended_utc': now(),
            'all_children_closed': guard is None or guard.children_closed(), 'a_prime_authorized': False})
        return 1
    finally:
        if guard is not None and not guard.children_closed():
            try:
                guard.stop_child()
            except BaseException as stopping:
                print('WORKER_STOP_FAILURE: ' + str(stopping), file=sys.stderr, flush=True)


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())
