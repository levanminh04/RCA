"""Q-125 TraceRCA: one immutable segment of the remaining 49 exact replays.

Only replay_tracerca_v3.py's ``one`` CLI invokes a method. This controller and
its saved-result validators use the standard library. No retry, source change,
tolerance, label-conditioned selection, or mechanism/physical-wait conclusion.
The pinned pilot validator is reused for every existing invariant; additional
stdlib checks authenticate the entire record, source route and capture binding.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import subprocess
import sys
import time
import traceback

BASE = Path('/home/ubuntu/rca/T-032')
REPO = BASE / 'repo'
SCRIPTS = BASE / 'scripts'
PYTHON = Path('/home/ubuntu/rca/T-025/envs/main/bin/python')
RUN = BASE / 'runs/tracerca-cohort-001'
PROPOSAL = BASE / 'runs/tracerca-cohort-proposal-001'
PLAN = PROPOSAL / 'plan-52.json'
PLAN_SHA = '2e26428c26ef2fd699a72abdd9e30662b7cbda61f97aec3c3eca1e33d89b2ebe'
FORECAST = PROPOSAL / 'forecast.json'
FORECAST_SHA = '9e1a527a60f25b31f9882943e8b0966230f85179b6afe7110de448d677fed50f'
PRIOR = BASE / 'runs/tracerca-pilots-root-001/closed-inventory.json'
PRIOR_SHA = 'a9019b899c3e0c095878767e4c917ea77c5672f7048ec1d5c5ef46ca26a9a6bf'
TOOLS = PROPOSAL / 'tool-check/tool-pins.json'
PILOT_SCRIPT = SCRIPTS / 'run_tracerca_path_pilots_v2.py'
PILOT_SHA = '136e76e69993b502c28ac18b7a3ab8e1a81b8bb5eac4e97ce413952e3a96d466'
WRAPPER = SCRIPTS / 'replay_tracerca_v3.py'
OLD_PINS = {
    'replay_tracerca_v3.py': '3127b73285cbce3cf7ba68483a7ca5d651007e097b5d913ac7544dc76ef064ee',
    'capture_tracerca.py': 'a883dfddc56abbb68447052b40764613b10b86621b9e8c80d86e143976f7ebe4',
    'replay_microrank.py': '193166089f7d0bf30a2f81551c374bec610f705241f6ad495aa5ff7181126562',
    'capture_microrank.py': 'b842b4be0d92470f1fc673e2afb30b5b0b76781c211a4b99ff6518c648b00c8b',
    'audit_tracerca_posthoc_v1.py': '3651353b4be2d3412906ad8b99bccbbac5d2c0b615393222a81adb050ca659ed',
}
EXACT_FIELDS = (
    'opaque_id', 'method', 'method_version', 'variant', 'mode', 'detector',
    'detector_columns', 'seed', 'hashseed', 'config_id', 'why_ids', 'window',
    'input_shape', 'status', 'method_status_raw', 'error', 'ranking_native',
    'ranking', 'entity_ranking', 'blocks', 'sets', 'diagnostics', 'extra', 'input_sha256',
)
EXCLUDED_FIELDS = {
    'run_id': 'new execution identifier; source identifier is preserved in source.json',
    'cost': 'new measured execution cost including observation; never copied from source',
}
MAX_WALL_S = 16200
MAX_NEW_BYTES = 5 * 2**29
MAX_CASE_S = 600
MAX_CASE_BYTES = 150 * 2**20
MAX_COMBINED_BYTES = 12 * 2**30
LAPTOP_RESERVE_BYTES = 4 * 2**30
MAX_RSS_BYTES = 6 * 2**30
MIN_AVAILABLE_BYTES = 2**30
RESERVE_BYTES = 2 * 2**20
REUSE = {('RE2-TT', 'dev-03d4910932'): 'posthoc',
         ('RE2-TT', 'dev-12a1a88069'): 're2-ok',
         ('Nezha-OB', 'dev-14701a3bbb'): 'nezha-ok'}
SUCCESS = {'CHECKPOINT', 'PASS_FULL_52_EXACT'}


class CohortError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise CohortError(message)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(2**20), b''):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    def invalid(token):
        raise CohortError('nonfinite JSON token: ' + token)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), parse_constant=invalid)


def now():
    return datetime.now(timezone.utc).isoformat()


def dump_new(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def atomic(path, value):
    temporary = Path(str(path) + '.tmp')
    with temporary.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
    temporary.replace(path)


def safe(root, relative):
    pure = PurePosixPath(relative)
    require(isinstance(relative, str) and not pure.is_absolute() and '\\' not in relative
            and '..' not in pure.parts and pure.parts, 'unsafe relative artifact/source path')
    path = Path(root) / pure
    require(path.resolve() == path and path.resolve().is_relative_to(Path(root).resolve())
            and not path.is_symlink(), 'redirected or escaped artifact/source')
    require('locked' not in pure.parts and not any(x == 'T-033' for x in pure.parts), 'forbidden source')
    return path


def logical_size(root):
    total = 0
    for parent, directories, files in os.walk(root):
        require(not any((Path(parent) / name).is_symlink() for name in directories), 'symlink directory in task inventory')
        for name in files:
            path = Path(parent) / name
            require(not path.is_symlink(), 'symlink file in task inventory')
            try:
                total += path.stat().st_size
            except FileNotFoundError:
                pass  # only atomic status/temp replacement may disappear
    return total


def inventory(root, exclude=()):
    return [{'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)}
            for path in sorted(Path(root).rglob('*')) if path.is_file()
            and path.relative_to(root).as_posix() not in exclude]


def verify_inventory(root, rows, excludes=()):
    seen = set()
    require(isinstance(rows, list), 'full manifest missing')
    for row in rows:
        require(row['path'] not in seen, 'duplicate manifest path')
        path = safe(root, row['path'])
        require(path.is_file() and path.stat().st_size == row['bytes'] and sha(path) == row['sha256'],
                'manifest hash/size differs: ' + row['path'])
        seen.add(row['path'])
    actual = {p.relative_to(root).as_posix() for p in Path(root).rglob('*') if p.is_file()}
    require(actual == seen | set(excludes), 'manifest missing or extra files')
    return len(seen)


def identical(left, right):
    """Value, Python JSON type, float hex, dictionary keys and list order exact."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(identical(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(identical(a, b) for a, b in zip(left, right))
    if isinstance(left, float):
        return left.hex() == right.hex()
    return left == right


def compare_exact(frozen, replay):
    schema = set(EXACT_FIELDS) | set(EXCLUDED_FIELDS)
    require(set(frozen) == schema and set(replay) == schema, 'record schema changed')
    require(identical({key: frozen[key] for key in EXACT_FIELDS},
                      {key: replay[key] for key in EXACT_FIELDS}), 'independent frozen record comparison differs')


def tool_pins(expected):
    require(re.fullmatch('[0-9a-f]{64}', expected or '') and sha(TOOLS) == expected, 'tool-pin receipt differs')
    pins = read(TOOLS)
    require(pins['status'] == 'STATIC_ONLY_NOT_RUNTIME_VERIFIED'
            and set(pins['scripts']) == {'run_tracerca_cohort_v1.py', 'start_tracerca_cohort_001.py', 'verify_tracerca_cohort_001.py'},
            'tool-pin receipt scope differs')
    for name, value in pins['scripts'].items():
        require(sha(SCRIPTS / name) == value, 'new tool pin differs: ' + name)
    for name, value in OLD_PINS.items():
        require(sha(SCRIPTS / name) == value, 'preserved source tool pin differs: ' + name)
    require(sha(PILOT_SCRIPT) == PILOT_SHA, 'preserved pilot validator changed')
    return pins


def pilot_validator():
    require(sha(PILOT_SCRIPT) == PILOT_SHA, 'pilot validator changed before stdlib-only import')
    spec = importlib.util.spec_from_file_location('tracerca_pilot_pinned_stdlib', PILOT_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_plan():
    require(sha(PLAN) == PLAN_SHA and sha(FORECAST) == FORECAST_SHA, 'approved source plan/forecast changed')
    plan, forecast = read(PLAN), read(FORECAST)
    rows = plan['rows']
    require(len(rows) == 52 and sum(r['new_method_needed'] is True for r in rows) == 49, '52/49 source scope differs')
    keys = [(r['dataset'], r['opaque_id']) for r in rows]
    require(len(set(keys)) == 52 and [r['dataset'] for r in rows] == ['RE2-TT'] * 30 + ['Nezha-OB'] * 22,
            'locked dataset/order/count differs')
    for dataset in ('RE2-TT', 'Nezha-OB'):
        ids = [r['opaque_id'] for r in rows if r['dataset'] == dataset]
        require(ids == sorted(ids) and all(re.fullmatch('dev-[0-9a-f]{10}', oid) for oid in ids), 'locked opaque order differs')
    require({k: r['replay_phase_already_valid'] for k, r in zip(keys, rows) if not r['new_method_needed']} == REUSE,
            'three previously closed cases changed')
    require(forecast['plan_sha256'] == PLAN_SHA and forecast['remaining_case_count'] == 49, 'forecast source binding differs')
    for relative, expected in forecast['sources'].items():
        root, item = (BASE, relative[len('results/T-032/'):]) if relative.startswith('results/T-032/') else (REPO, relative)
        require(sha(safe(root, item)) == expected, 'forecast source pin differs: ' + relative)
    return rows


def source_binding(row):
    index = read(safe(REPO, row['source_index']))
    pointer = row['source_pointer'].split('/')
    require(len(pointer) == 3 and pointer[0] == '' and pointer[1] in ('records', 'unique_records'), 'source pointer invalid')
    entry = index[pointer[1]][int(pointer[2])]
    require(entry['opaque_id'] == row['opaque_id'] and entry['path'] == row['frozen_path']
            and entry['sha256'] == row['frozen_sha256'] and entry.get('seed') is None, 'source pointer binding differs')
    require(entry.get('method') == 'tracerca' and (row['dataset'] == 'RE2-TT' and entry['variant'] == 'native'
            or row['dataset'] == 'Nezha-OB' and entry['worker_method'] == 'tracerca'
            and entry['source_view'] == 'main' and entry['trace_guard_s'] == 0), 'method/dataset/source-view differs')
    path = safe(REPO, row['frozen_path'])
    require(sha(path) == row['frozen_sha256'], 'frozen source changed')
    frozen = read(path)
    require(frozen['opaque_id'] == row['opaque_id'] and frozen['method'] == 'tracerca'
            and frozen['mode'] == 'a' and frozen['seed'] is None and frozen['hashseed'] == 0
            and frozen['variant'] == ('native' if row['dataset'] == 'RE2-TT' else 'finite')
            and frozen['status'] == row['source_status'] and frozen['status'] in ('OK', 'ERROR', 'NO_EVIDENCE')
            and identical(frozen['window'], row['window']) and frozen['config_id'] == row['config_id'], 'frozen main/F/a/h0/config/window differs')
    if row['dataset'] == 'RE2-TT':
        config = safe(REPO, entry['source_config'])
        require(sha(config) == entry['source_config_sha256'], 'source configuration hash differs')
        code_hashes = read(config)['src_p3']['tep']
        route = 'full'
    else:
        code_hashes = {p: h for p, h in index['source_hashes'].items() if p.startswith('src/p3/') and p.endswith('.py')}
        route = 'reused_pilot' if entry['reused_pilot'] else 'full'
        script = 'results/T-026/scripts/run_pilot.py' if entry['reused_pilot'] else 'results/T-026/scripts/run.py'
        script_path = safe(REPO, script)
        require(sha(script_path) == index['source_hashes'][script], 'source reconstruction script hash differs')
        constants = {}
        for node in ast.parse(script_path.read_text(encoding='utf-8-sig')).body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in ('WHY', 'CONFIG'):
                        constants[target.id] = ast.literal_eval(node.value)
        require(set(constants) == {'WHY', 'CONFIG'} and constants['CONFIG'] == frozen['config_id']
                and identical(constants['WHY'], frozen['why_ids']), 'Nezha original route constants differ')
        wanted_extra = {'pilot_view': 'main', 'pilot_only': True} if entry['reused_pilot'] else {'source_view': 'main', 'pilot_only': False}
        require(all(identical(frozen['extra'].get(k), v) for k, v in wanted_extra.items())
                and frozen['extra']['source_provenance_file'] == 'ket-qua.json', 'Nezha source route extra differs')
    require(route == row['code_route'], 'full/reused-pilot source route changed')
    for relative, expected in code_hashes.items():
        require(sha(safe(REPO, relative)) == expected, 'frozen p3 source changed: ' + relative)
    return entry, frozen, code_hashes


def verify_saved_source(directory, row, check, original=None):
    entry, frozen, code_hashes = source_binding(row)
    replay_dir = original or directory
    source = read(replay_dir / 'source.json')
    require(source['dataset'] == row['dataset'] and source['opaque_id'] == row['opaque_id']
            and identical(source['entry'], entry) and source['source_run_id'] == frozen['run_id']
            and source['source_status'] == row['source_status']
            and source['selected_allowlist_hashes_equal_frozen_inputs'] is True
            and source['exact_fields'] == list(EXACT_FIELDS) and source['excluded_fields'] == EXCLUDED_FIELDS,
            'saved source/input/record-policy binding differs')
    compare_exact(frozen, read(replay_dir / 'ban-ghi-0.json'))
    require(check['exact_fields'] == list(EXACT_FIELDS) and check['excluded_fields'] == EXCLUDED_FIELDS
            and check['compare']['exact_fields'] == list(EXACT_FIELDS)
            and check['compare']['excluded_fields'] == EXCLUDED_FIELDS, 'child comparison policy differs')
    audit = read(directory / 'source-checks.json')['checks']
    for item in audit:
        require(item.get('pass') is True, 'source audit failed')
        if 'path' in item:
            path = Path(item['path']) if item['path'].startswith('/') else safe(REPO, item['path'])
            require(path.resolve() == path and not path.is_symlink()
                    and (path.is_relative_to(REPO) or path.is_relative_to(BASE / 'sources')), 'audit source outside pinned roots')
            require(item['expected'] == item['actual'] == sha(path), 'actual audit source hash differs')
            if 'bytes' in item:
                require(item['bytes'] == path.stat().st_size, 'audit source size differs')
        else:
            require(item.get('authority') == 'approved TraceRCA-only source path selection'
                    and item['selected_parent'] == str(BASE / 'sources/rcaeval'), 'unknown source audit row')
    for item in source['actual_imports'] + check['actual_imports_after']:
        require(item['path'] in code_hashes and item['sha256'] == code_hashes[item['path']]
                and sha(safe(REPO, item['path'])) == item['sha256'], 'actual p3 import differs')
    external = source['external']
    require(external['versions'] == {'numpy': '1.26.4', 'pandas': '2.2.3'}
            and external['closure_revision'] == '259ea4167160256a74ad30004aa3d96a998c846e'
            and external['closure_inventory_sha256'] == 'c07cbd357b860d164a8d4eef0177015e8620928107192a2b98301e79b3ad0bd5',
            'external revision/closure/versions differ')
    allow_path = Path(source['allowlist_path'])
    expected_allow = safe(REPO, 'results/T-022/allowlist-dev.json' if row['dataset'] == 'RE2-TT' else 'results/T-026/allowlist-dev.json')
    require(allow_path == expected_allow and sha(allow_path) == source['allowlist_sha256'], 'dev allowlist path/hash differs')
    cases = [r for r in read(allow_path)['cases'] if r['opaque_id'] == row['opaque_id']]
    require(len(cases) == 1, 'dev allowlist membership not unique')
    files = {name: item for name, item in cases[0]['files'].items() if item is not None}
    require({name: item['sha256'] for name, item in files.items()} == frozen['input_sha256'], 'allowlist input hashes differ')
    job = read(replay_dir / 'job.json')
    if row['dataset'] == 'RE2-TT':
        raw_root = Path('/home/ubuntu/rca/T-031/repo')
        require(job['kind'] == 'ranker' and job['method'] == 'tracerca' and job['model'] is None
                and identical(job['t'], frozen['window']['t']) and set(job['files']) == set(files), 'RE2 job differs')
        for name, meta in files.items():
            path = safe(raw_root, meta['path'])
            require(job['files'][name] == {'path': str(path), 'sha256': meta['sha256']}, 'RE2 job selected path/hash differs')
    else:
        require(job == {'allowlist_path': str(allow_path), 'opaque_id': row['opaque_id'], 'repo_root': str(REPO),
                        'view': 'main', 'method': 'tracerca', 'trace_guard_s': 0}, 'Nezha main worker job differs')
    summary = read(replay_dir / 'capture/capture.json')
    require(summary['status'] == 'captured_unverified_replay' and not summary['errors']
            and summary['trace_restored'] is True and summary['profile_restored'] is True,
            'capture incomplete/hooks not restored')
    require(sorted(call['function'] for call in summary['calls']) == ['adapter', 'native', 'operation_slo'], 'missing/duplicate native call')
    for item in summary['artifacts']:
        path = safe(replay_dir / 'capture', item['path'])
        require(path.stat().st_size == item['bytes'] and sha(path) == item['sha256'], 'capture artifact hash differs')
    start = read(replay_dir / 'capture/capture-start.json')
    require(start['packages'] == external['versions'] and start['thread_environment']['PYTHONHASHSEED'] == '0', 'capture packages/hashseed differ')
    functions = {'adapter': (REPO / 'src/p3/adapters/tracerca.py', 'chay'),
                 'native': (BASE / 'sources/rcaeval/RCAEval/e2e/tracerca.py', 'tracerca'),
                 'operation_slo': (BASE / 'sources/rcaeval/RCAEval/e2e/tracerca.py', 'get_operation_slo')}
    require(set(start['sources']) == set(functions), 'captured function set differs')
    for name, (path, function) in functions.items():
        definitions = [node for node in ast.parse(path.read_text(encoding='utf-8-sig')).body
                       if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function]
        require(len(definitions) == 1 and start['sources'][name] == {'path': str(path), 'sha256': sha(path),
                'first_line': definitions[0].lineno}, 'actual captured function binding differs: ' + name)
    require(summary['adapter_status'] == row['source_status']
            and summary['adapter_threw'] is False and summary['native_outcome'] == check['capture_check']['native_outcome'],
            'native/adapter status binding differs')
    return {'record_exact': True, 'source_binding_exact': True, 'single_native_capture': True,
            'code_route': row['code_route'], 'frozen_sha256': row['frozen_sha256'],
            'record_path': str(replay_dir / 'ban-ghi-0.json'), 'capture_path': str(replay_dir / 'capture/capture.json')}


def verify_case(directory, row, validator, phase='cohort'):
    identity = (phase, row['dataset'], row['opaque_id'], row['source_status'], row['frozen_sha256'])
    result = validator.validate_child(directory, phase, identity)
    check = read(directory / 'check.json')
    original = BASE / 'runs/tracerca-path-pilots-001/re2-error' if phase == 'posthoc' else None
    result.update(verify_saved_source(directory, row, check, original))
    result.update(check_path=str(directory / 'check.json'), check_pointer='',
                  intermediates_exact_eligible=True,
                  mechanism_status='N/A_NON_OK' if row['source_status'] != 'OK' else 'OPEN_MANUAL_ANALYSIS',
                  numerical_tolerance=None, physical_wait='OPEN')
    return result


def verify_reuse(rows, validator):
    require(sha(PRIOR) == PRIOR_SHA, 'closed prior inventory changed')
    prior = read(PRIOR)
    require(prior['base'] == str(BASE) and len(prior['files']) == 198, 'closed prior scope differs')
    for item in prior['files']:
        path = safe(BASE, item['path'])
        require(path.stat().st_size == item['bytes'] and sha(path) == item['sha256'], 'closed prior file changed')
    actual = set()
    for root in prior['roots']:
        path = Path(root)
        require(path.is_relative_to(BASE) and path.resolve() == path, 'prior root escaped')
        candidates = [path] if path.is_file() else [p for p in path.rglob('*') if p.is_file()]
        actual.update(p.relative_to(BASE).as_posix() for p in candidates)
    require(actual == {x['path'] for x in prior['files']}, 'prior full inventory missing/extra files')
    old = BASE / 'runs/tracerca-path-pilots-002'
    validator.validate_child(old / 'fixture', 'fixture', None)  # saved fixture metadata; never re-run fixtures
    reused = {}
    for row in rows:
        key = (row['dataset'], row['opaque_id'])
        if key in REUSE:
            reused[key] = verify_case(old / REUSE[key], row, validator, REUSE[key])
    return reused


def proc_table():
    result = {}
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        try:
            raw = (entry / 'stat').read_text()
            fields = raw[raw.rfind(')') + 2:].split()
            result[int(entry.name)] = {'ppid': int(fields[1]), 'state': fields[0],
                                      'start_ticks': int(fields[19]), 'rss': int(fields[21]) * os.sysconf('SC_PAGE_SIZE')}
        except (FileNotFoundError, ProcessLookupError):
            pass
    return result


def tree_pids(root_pid, table):
    wanted = {root_pid} if root_pid in table else set()
    while True:
        larger = wanted | {pid for pid, meta in table.items() if meta['ppid'] in wanted}
        if larger == wanted:
            return wanted
        wanted = larger


def resources(root_pid):
    table = proc_table()
    pids = tree_pids(root_pid, table)
    memory = {line.split(':')[0]: int(line.split()[1]) * 1024 for line in Path('/proc/meminfo').read_text().splitlines()
              if line.startswith(('MemAvailable:', 'MemTotal:'))}
    stat = os.statvfs(BASE)
    return {'at_utc': now(), 'tree_rss_bytes': sum(table[pid]['rss'] for pid in pids),
            'available_ram_bytes': memory['MemAvailable'], 'total_ram_bytes': memory['MemTotal'],
            'free_disk_bytes': stat.f_bavail * stat.f_frsize, 'tree_pids': sorted(pids)}


def validate_snapshot(path, expected):
    path = Path(path)
    require(path.is_relative_to(BASE / 'runs') and path.resolve() == path and sha(path) == expected, 'snapshot scope/hash differs')
    snapshot = read(path)
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(snapshot['at_utc'])).total_seconds()
    require(0 <= age <= 300, 'resource/SPEC snapshot older than five minutes')
    require(snapshot['micro_laptop_segment_running'] is False and snapshot['no_other_ec2_heavy_worker'] is True,
            'EC2 writes forbidden during Micro laptop segment or another heavy job')
    require(0 <= snapshot['local_task_bytes'] <= LAPTOP_RESERVE_BYTES
            and snapshot['laptop_reserve_bytes'] == LAPTOP_RESERVE_BYTES
            and snapshot['max_combined_bytes'] == MAX_COMBINED_BYTES, 'local/global cap snapshot differs')
    require(snapshot['spec_remaining_wall_s'] >= MAX_WALL_S and snapshot['spec_remaining_new_bytes'] >= MAX_NEW_BYTES,
            'cumulative SPEC budget insufficient; checkpoint and ask Minh')
    measured = logical_size(BASE)
    require(0 <= measured - snapshot['remote_task_bytes'] <= RESERVE_BYTES, 'remote just-before-launch snapshot stale')
    require(measured + LAPTOP_RESERVE_BYTES + MAX_NEW_BYTES + RESERVE_BYTES <= MAX_COMBINED_BYTES, 'forecast cannot fit combined 12 GiB')
    resource = resources(os.getpid())
    require(resource['available_ram_bytes'] >= MAX_RSS_BYTES + MIN_AVAILABLE_BYTES,
            'not enough available RAM for 6 GiB tree ceiling plus 1 GiB reserve')
    require(resource['free_disk_bytes'] >= MAX_NEW_BYTES + RESERVE_BYTES, 'not enough free disk for approved cap')
    return snapshot, resource


def stop_group(process):
    if process is None or process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=3)
    except ProcessLookupError:
        return
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=3)


def closure(segment, expected=None):
    path = segment / 'closed-manifest.json'
    if expected is not None:
        require(sha(path) == expected, 'previous closed segment hash differs')
    closed = read(path)
    require(closed['root'] == str(segment) and closed['streams_closed'] is True
            and closed['controller_exit_code'] == 0 and closed['status'] in SUCCESS, 'previous segment not successfully closed; no retry')
    verify_inventory(segment, closed['files'], ('closed-manifest.json',))
    return closed


def table_initial(rows):
    return [{**row, 'row_index': i, 'state': 'PENDING', 'record_exact': None,
             'intermediates_exact_eligible': False, 'mechanism_status': 'N/A_NON_OK' if row['source_status'] != 'OK' else 'OPEN_NOT_CAPTURED',
             'result': None, 'physical_wait': 'OPEN'} for i, row in enumerate(rows)]


def history(segment_number, previous_sha, rows):
    require(segment_number >= 1, 'invalid segment number')
    table = table_initial(rows)
    completed = 0
    total_wall = 0.0
    initial_baseline = None
    routes = set()
    require((segment_number == 1 and previous_sha is None) or (segment_number > 1 and previous_sha is not None), 'explicit predecessor closure required')
    existing = sorted((RUN / 'segments').iterdir())
    require([p.name for p in existing] == [f'{i:03d}' for i in range(1, segment_number + 1)], 'missing/extra segment history')
    for i in range(1, segment_number):
        prior = RUN / 'segments' / f'{i:03d}'
        closure(prior, previous_sha if i == segment_number - 1 else None)
        status = read(prior / 'status.json')
        require(status['status'] == 'CHECKPOINT', 'finished/failed segment cannot be continued')
        old_table = read(prior / 'table-52.json')['rows']
        require(len(old_table) == 52 and all(all(identical(old[key], row[key]) for key in row)
                for old, row in zip(old_table, rows)), 'previous table source scope changed')
        require(status['new_case_completed_total'] >= completed, 'completed case count regressed')
        completed = status['new_case_completed_total']
        total_wall += status['elapsed_s']
        baseline = read(prior / 'invocation.json')['initial_baseline_task_bytes']
        require(initial_baseline is None or initial_baseline == baseline, 'cohort baseline changed between segments')
        initial_baseline = baseline
        table = old_table
        routes = set(status['new_routes_checked'])
    require(not any(row['state'] in ('FAILED', 'RUNNING') for row in table), 'incomplete/failed case cannot be retried')
    return table, completed, total_wall, initial_baseline, routes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--segment', type=int, required=True)
    parser.add_argument('--previous-closure-sha256')
    parser.add_argument('--snapshot', required=True)
    parser.add_argument('--snapshot-sha256', required=True)
    parser.add_argument('--tool-pins-sha256', required=True)
    parser.add_argument('--case-limit', type=int, required=True)
    args = parser.parse_args()
    segment = RUN / 'segments' / f'{args.segment:03d}'
    require(segment.is_dir() and not (segment / 'invocation.json').exists(), 'launcher must create a fresh segment')
    require(Path(sys.executable).resolve() == PYTHON.resolve() and Path.home() == Path('/home/ubuntu'), 'unapproved EC2 interpreter/host')
    require(os.environ.get('PYTHONHASHSEED') == '0' and 1 <= args.case_limit <= 49, 'hashseed/case-limit invalid')
    started = time.monotonic()
    child = None
    active = None
    rows = load_plan()
    table = table_initial(rows)
    state = {'status': 'STARTING', 'controller_pid': os.getpid(), 'segment': args.segment, 'started_utc': now(),
             'active': None, 'new_case_completed_total': 0, 'new_routes_checked': [], 'prior_elapsed_s': 0.0,
             'research_complete': False, 'manual_complete': False, 'physical_wait': 'OPEN', 'no_retry_no_skip': True}
    baseline = logical_size(BASE)
    last_poll = 0.0

    def save(event):
        state.update(updated_utc=now(), elapsed_s=time.monotonic() - started)
        atomic(segment / 'table-52.json', {'plan_sha256': PLAN_SHA, 'rows': table, 'method': 'tracerca',
               'status': state['status'], 'record_policy': 'all exact fields; only run_id/cost excluded',
               'non_OK_mechanism': 'N/A; exact non-OK is retained', 'manual_complete': False})
        atomic(segment / 'status.json', state)
        with (segment / 'progress.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'event': event, **state}, ensure_ascii=False, allow_nan=False) + '\n')
        print(now(), event, state['status'], flush=True)

    def guard():
        measured = logical_size(BASE)
        state.update(remote_task_bytes=measured, measured_cohort_new_bytes=measured - baseline,
                     resources=resources(os.getpid()))
        require(measured >= baseline and measured - baseline + RESERVE_BYTES <= MAX_NEW_BYTES, 'cohort 2.5 GiB cap reached')
        require(measured + LAPTOP_RESERVE_BYTES + RESERVE_BYTES <= MAX_COMBINED_BYTES, 'combined 12 GiB cap reached')
        require(time.monotonic() - started + state['prior_elapsed_s'] < MAX_WALL_S - 10, 'cohort 4.5 hour cap reached')
        require(state['resources']['tree_rss_bytes'] <= MAX_RSS_BYTES
                and state['resources']['available_ram_bytes'] >= MIN_AVAILABLE_BYTES, 'RSS/RAM guard reached')
        require(state['resources']['free_disk_bytes'] >= RESERVE_BYTES, 'disk reserve reached')
        require(not (RUN / 'STOP').exists(), 'root stop marker')
        if active:
            require(time.monotonic() - active['started_monotonic'] < MAX_CASE_S - 10, 'case 600 s cap reached')
            require(measured - active['baseline_task_bytes'] + RESERVE_BYTES <= MAX_CASE_BYTES, 'case 150 MiB cap reached')
        tool_pins(args.tool_pins_sha256)

    def on_signal(number, _frame):
        raise CohortError('controller signal ' + str(number))

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    save('START_SOURCE_VALIDATION')
    try:
        pins = tool_pins(args.tool_pins_sha256)
        snapshot, resource = validate_snapshot(args.snapshot, args.snapshot_sha256)
        table, completed, prior_wall, old_baseline, routes = history(args.segment, args.previous_closure_sha256, rows)
        baseline = snapshot['remote_task_bytes'] if old_baseline is None else old_baseline
        state.update(new_case_completed_total=completed, prior_elapsed_s=prior_wall, new_routes_checked=sorted(routes))
        dump_new(segment / 'invocation.json', {'argv': sys.argv, 'python': sys.executable, 'at_utc': now(),
            'script_sha256': sha(__file__), 'tool_pins': pins, 'tool_pins_sha256': args.tool_pins_sha256,
            'snapshot_path': args.snapshot, 'snapshot_sha256': args.snapshot_sha256, 'snapshot': snapshot,
            'preflight_resources': resource, 'initial_baseline_task_bytes': baseline, 'plan_sha256': PLAN_SHA,
            'forecast_sha256': FORECAST_SHA, 'prior_inventory_sha256': PRIOR_SHA,
            'caps': {'wall_s': MAX_WALL_S, 'new_bytes': MAX_NEW_BYTES, 'case_s': MAX_CASE_S,
                     'case_bytes': MAX_CASE_BYTES, 'combined_bytes': MAX_COMBINED_BYTES,
                     'laptop_reserved_bytes': LAPTOP_RESERVE_BYTES, 'tree_rss_bytes': MAX_RSS_BYTES,
                     'ram_reserve_bytes': MIN_AVAILABLE_BYTES},
            'counter_note': 'logical file-byte polling, including task/cache/temp/monitor growth; may overshoot; no hard filesystem quota'})
        validator = pilot_validator()
        for row in rows:
            source_binding(row)
        reused = verify_reuse(rows, validator)
        for row in table:
            key = (row['dataset'], row['opaque_id'])
            if key in reused:
                row.update(state='REUSED_EXACT', record_exact=True, intermediates_exact_eligible=True, result=reused[key],
                           mechanism_status=reused[key]['mechanism_status'])
            elif row['state'] == 'EXACT':
                verdict = verify_case(Path(row['result']['check_path']).parent, row, validator)
                require(identical(verdict, row['result']), 'completed case proof changed')
        state['status'] = 'RUNNING'
        save('SOURCE_AND_REUSE_PASS')
        done_here = 0
        for i, row in enumerate(table):
            if row['state'] in ('REUSED_EXACT', 'EXACT'):
                continue
            guard()
            directory = RUN / 'cases' / (row['dataset'] + '-' + row['opaque_id'])
            require(row['state'] == 'PENDING' and not directory.exists(), 'case exists or not pending; no retry')
            source_binding(row)
            command = [str(PYTHON), '-B', '-X', 'utf8', str(WRAPPER), 'one', row['dataset'], row['opaque_id'], str(directory)]
            active = {'row_index': i, 'command': command, 'directory': str(directory), 'pid': None,
                      'started_monotonic': time.monotonic(), 'baseline_task_bytes': logical_size(BASE)}
            row['state'] = 'RUNNING'
            state['active'] = active
            save('CASE_START')
            name = f'{i:02d}'
            logs = segment / 'logs'
            with (logs / (name + '.stdout.txt')).open('x', encoding='utf-8') as out, (logs / (name + '.stderr.txt')).open('x', encoding='utf-8') as err:
                child = subprocess.Popen(command, cwd=BASE, env=os.environ.copy(), stdout=out, stderr=err, start_new_session=True)
                active['pid'] = child.pid
                dump_new(logs / (name + '.pid.json'), {'pid': child.pid, 'command': command,
                         'start_ticks': proc_table().get(child.pid, {}).get('start_ticks')})
                save('CASE_RUNNING')
                while child.poll() is None:
                    guard()
                    elapsed = time.monotonic() - started
                    if elapsed - last_poll >= 10:
                        save('CASE_POLL')
                        last_poll = elapsed
                    time.sleep(0.5)
            cost = {'pid': child.pid, 'exit_code': child.returncode, 'elapsed_s': time.monotonic() - active['started_monotonic'], 'command': command}
            dump_new(logs / (name + '.process.json'), cost)
            require(child.returncode == 0 and cost['elapsed_s'] <= MAX_CASE_S, 'case failed/time cap; stop whole method')
            guard()
            verdict = verify_case(directory, row, validator)
            dump_new(logs / (name + '.verified.json'), verdict)
            row.update(state='EXACT', record_exact=True, intermediates_exact_eligible=True, result=verdict,
                       mechanism_status=verdict['mechanism_status'])
            route = row['dataset'] + ':' + row['code_route'] + ':' + row['source_status']
            unseen_route = route not in routes
            routes.add(route)
            completed += 1
            done_here += 1
            state.update(active=None, new_case_completed_total=completed, new_routes_checked=sorted(routes))
            child = active = None
            save('CASE_EXACT')
            guard()
            if completed == 1 or unseen_route or done_here >= args.case_limit:
                state.update(status='CHECKPOINT', checkpoint_reason='FIRST_NEW_CASE' if completed == 1 else 'UNSEEN_ROUTE' if unseen_route else 'ROOT_SEGMENT_CASE_LIMIT')
                break
        if all(row['state'] in ('REUSED_EXACT', 'EXACT') for row in table):
            state.update(status='PASS_FULL_52_EXACT', checkpoint_reason=None)
        require(state['status'] in SUCCESS, 'segment ended without checkpoint/full exact status')
        guard()
        save('TERMINAL')
        dump_new(segment / 'terminal.json', {'status': state['status'], 'controller_exit_code': 0,
            'table_sha256': sha(segment / 'table-52.json'), 'status_sha256': sha(segment / 'status.json'),
            'new_case_completed_total': completed, 'all_52_exact': state['status'] == 'PASS_FULL_52_EXACT',
            'manual_complete': False, 'research_complete': False, 'physical_wait': 'OPEN'})
        return 0
    except BaseException as exc:
        stop_group(child)
        if active:
            row = table[active['row_index']]
            row.update(state='FAILED', record_exact=None, intermediates_exact_eligible=False,
                       mechanism_status='N/A_NON_OK' if row['source_status'] != 'OK' else 'OPEN_FAILED_CAPTURE',
                       error=str(exc), result=None)
            cost_path = segment / 'logs' / (f"{active['row_index']:02d}" + '.process.json')
            if not cost_path.exists():
                dump_new(cost_path, {'pid': active['pid'], 'exit_code': None if child is None else child.returncode,
                    'command': active['command'], 'elapsed_s': time.monotonic() - active['started_monotonic'], 'error': str(exc)})
        state.update(status='FAIL_STOP', error=str(exc), error_type=type(exc).__name__, active=None)
        dump_new(segment / 'failure.json', {'at_utc': now(), 'traceback': traceback.format_exc(), 'error': str(exc), 'retained': 'every partial result, segment and stream; no retry'})
        save('FAIL_STOP')
        dump_new(segment / 'terminal.json', {'status': 'FAIL_STOP', 'controller_exit_code': 1,
            'table_sha256': sha(segment / 'table-52.json'), 'status_sha256': sha(segment / 'status.json'),
            'all_52_exact': False, 'manual_complete': False, 'research_complete': False})
        return 1
    finally:
        stop_group(child)


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())
