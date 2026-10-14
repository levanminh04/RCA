"""Approved dtype repair, saved ERROR audit, then exactly two TraceRCA pilots.

EC2 only. Fixture and posthoc share 300 s / 50 MiB; only after both PASS may
RE2 OK and Nezha OK run, sequentially, within 1200 s / 150 MiB and 600 s each.
No cohort, skip, retry, source/adapter/environment change or score tolerance.
Logical-byte polling is not a hard filesystem quota; preserve every failure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import signal
import subprocess
import sys
import time
import traceback

BASE = Path('/home/ubuntu/rca/T-032')
SCRIPTS = BASE / 'scripts'
PYTHON = Path('/home/ubuntu/rca/T-025/envs/main/bin/python')
WRAPPER = SCRIPTS / 'replay_tracerca_v3.py'
WRAPPER_SHA256 = '3127b73285cbce3cf7ba68483a7ca5d651007e097b5d913ac7544dc76ef064ee'
AUDITOR = SCRIPTS / 'audit_tracerca_posthoc_v1.py'
AUDITOR_SHA256 = '3651353b4be2d3412906ad8b99bccbbac5d2c0b615393222a81adb050ca659ed'
SHARED_PINS = {
    'capture_tracerca.py': 'a883dfddc56abbb68447052b40764613b10b86621b9e8c80d86e143976f7ebe4',
    'replay_microrank.py': '193166089f7d0bf30a2f81551c374bec610f705241f6ad495aa5ff7181126562',
    'capture_microrank.py': 'b842b4be0d92470f1fc673e2afb30b5b0b76781c211a4b99ff6518c648b00c8b',
}
INVENTORY = BASE / 'sources/tracerca-path-002-inventory.json'
INVENTORY_SHA256 = 'c07cbd357b860d164a8d4eef0177015e8620928107192a2b98301e79b3ad0bd5'
ORIGINAL_INVENTORY = BASE / 'runs/tracerca-dtype-source-inventory-001.json'
ORIGINAL_INVENTORY_SHA256 = '873f5a5ff947dfbbf3ae77168c40002cb7c8ddf64c0077ec2dd8b92ae33b159d'
ORIGINAL_ERROR = BASE / 'runs/tracerca-path-pilots-001/re2-error'
ERROR_FROZEN_SHA256 = '7d4e3f96986ec5d9c1dc27f8d869b0db2eb53b75fac35c4aa95e9930d26e2b09'
MAX_REPAIR_S = 300
MAX_REPAIR_BYTES = 50 * 1024 * 1024
MAX_PILOTS_S = 1200
MAX_PILOTS_BYTES = 150 * 1024 * 1024
MAX_GROUP_S = MAX_REPAIR_S + MAX_PILOTS_S
MAX_CHILD_S = 600
MAX_NEW_BYTES = MAX_REPAIR_BYTES + MAX_PILOTS_BYTES
MAX_TOTAL_BYTES = 12 * 1024 * 1024 * 1024
MAX_LAPTOP_BYTES = 2 * 1024 * 1024 * 1024
FINAL_RESERVE_BYTES = 64 * 1024
POLL_S = 0.5
PILOTS = (
    ('re2-ok', 'RE2-TT', 'dev-12a1a88069', 'OK', 'd6e57bdbbf03b8cc764de85ea6a94aebcbef3cb8fe091a7aff1ebb67d6c081e5'),
    ('nezha-ok', 'Nezha-OB', 'dev-14701a3bbb', 'OK', 'e9bd73e1e0cc16462ad1e22bb7be3bd015884a665b5cefaf46a0c3576481ecff'),
)
FIXTURE_NAMES = ('scalar', 'zero_support', 'zero_abnormal', 'single_baseline_std_nan',
                 'new_operation_error', 'mapping_collision_error', 'adapter_extension_tables')
SERIALIZER_NAMES = tuple('serializer_' + name for name in (
    'string', 'string_NA', 'Int64', 'Int64_NA', 'boolean', 'boolean_NA', 'Float64',
    'Float64_NA', 'native_float_special', 'object_missing_special'))


class PilotError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise PilotError(message)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    def invalid(token):
        raise PilotError('nonfinite JSON token: ' + token)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), parse_constant=invalid)


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def dump_new(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def logical_size(root):
    total = 0
    for parent, _directories, files in os.walk(root):
        for name in files:
            path = Path(parent) / name
            if not path.is_symlink():
                try:
                    total += path.stat().st_size
                except FileNotFoundError:
                    pass
    return total


def verify_original_inventory():
    require(sha(ORIGINAL_INVENTORY) == ORIGINAL_INVENTORY_SHA256, 'closed ERROR inventory differs')
    inventory = read(ORIGINAL_INVENTORY)
    require(inventory['root'] == str(ORIGINAL_ERROR) and inventory['old_verdict'] == 'FAIL'
            and inventory['old_intermediates_eligible'] is False, 'closed inventory ERROR scope differs')
    seen = set()
    for row in inventory['files']:
        relative = PurePosixPath(row['path'])
        require(not relative.is_absolute() and '\\' not in row['path'] and '..' not in relative.parts
                and row['path'] not in seen, 'invalid/duplicate closed ERROR artifact')
        path = ORIGINAL_ERROR / relative
        require(path.resolve().is_relative_to(ORIGINAL_ERROR) and not path.is_symlink(), 'ERROR artifact escaped/redirected')
        require(sha(path) == row['sha256'] and path.stat().st_size == row['bytes'], 'closed ERROR artifact changed')
        seen.add(row['path'])
    actual = {p.relative_to(ORIGINAL_ERROR).as_posix() for p in ORIGINAL_ERROR.rglob('*') if p.is_file()}
    require(actual == seen and read(ORIGINAL_ERROR / 'check.json')['status'] == 'FAIL', 'closed ERROR directory/old verdict changed')
    return inventory


def verify_artifacts(directory, check, phase):
    require(isinstance(check.get('artifact_manifest'), list), 'child artifact manifest missing')
    seen = set()
    for item in check['artifact_manifest']:
        relative = PurePosixPath(item['path'])
        require(not relative.is_absolute() and '..' not in relative.parts and '\\' not in item['path']
                and item['path'] not in seen, 'invalid/duplicate child artifact path')
        path = directory / relative
        require(path.resolve().is_relative_to(directory.resolve()) and not path.is_symlink(), 'child artifact redirected/escaped')
        require(sha(path) == item['sha256'] and path.stat().st_size == item['bytes'], 'child artifact hash/size differs')
        seen.add(item['path'])
    actual = {p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file() and p != directory / 'check.json'}
    require(actual == seen, 'child full artifact manifest missing/extra files')
    require('source-checks.json' in seen and 'invocation.json' in seen, 'child manifest missing source/invocation')
    source = read(directory / 'source-checks.json')
    require(source.get('checks') and all(item.get('pass') is True for item in source['checks']), 'child source audit failed')
    for item in source['checks']:
        if item.get('authority') == 'approved TraceRCA-only source path selection':
            require(item['selected_parent'] == str(BASE / 'sources/rcaeval'), 'source path selection differs')
    invocation = read(directory / 'invocation.json')
    require(invocation['scripts']['replay_tracerca_v3.py'] == WRAPPER_SHA256, 'child wrapper pin differs')
    require(all(invocation['scripts'].get(name) == expected for name, expected in SHARED_PINS.items()),
            'child shared capture/replay pin differs')
    require(invocation['hashseed'] == '0', 'child hashseed differs')
    if phase == 'posthoc':
        require(invocation['script_sha256'] == AUDITOR_SHA256 and invocation['methods_executed'] is False
                and invocation['original_inventory_sha256'] == ORIGINAL_INVENTORY_SHA256, 'posthoc invocation differs')
    return len(seen)


def validate_child(directory, phase, pilot):
    check = read(directory / 'check.json')
    require(check.get('status') == 'PASS', 'child verdict not PASS')
    count = verify_artifacts(directory, check, phase)
    if phase == 'fixture':
        fixtures = check.get('fixtures', [])
        require(tuple(item['name'] for item in fixtures) == FIXTURE_NAMES, 'original six/extension fixture set/order changed')
        require(all(item.get('pass') is True and item.get('input_unchanged') is True and not item.get('differences')
                    and item.get('invariants') and all(value is True for value in item['invariants'].values()) for item in fixtures),
                'native/observed fixture check failed')
        require(all(item.get('capture_check', {}).get('hooks_restored') is True for item in fixtures), 'fixture hooks not restored')
        serializers = check.get('serializer_fixtures', [])
        require(tuple(item['name'] for item in serializers) == SERIALIZER_NAMES, 'typed serializer fixture set/order changed')
        require(all(item.get('pass') is True and item.get('input_unchanged') is True and item.get('methods_executed') is False
                    and not item.get('differences') and item.get('invariants')
                    and all(value is True for value in item['invariants'].values()) for item in serializers), 'typed serializer fixture failed')
        require(read(directory / 'serializer_tables/check.json').get('unknown_values_rejected') is True,
                'typed unknown missing/nonfinite values not rejected')
    else:
        if phase == 'posthoc':
            dataset, opaque_id, source_status, frozen_sha = 'RE2-TT', 'dev-03d4910932', 'ERROR', ERROR_FROZEN_SHA256
            require(check.get('methods_executed') is False and check.get('record_exact') is True
                    and check.get('original_full_inventory_verified') is True
                    and check.get('original_verdict_retained') == 'FAIL' and check.get('original_run') == str(ORIGINAL_ERROR)
                    and check.get('original_inventory_sha256') == ORIGINAL_INVENTORY_SHA256, 'posthoc scope/old FAIL invariant failed')
            verify_original_inventory()
        else:
            _name, dataset, opaque_id, source_status, frozen_sha = pilot
        require(check.get('dataset') == dataset and check.get('opaque_id') == opaque_id
                and check.get('frozen_sha256') == frozen_sha, 'pilot/posthoc frozen identity/hash differs')
        require(check.get('frozen_status') == source_status and check.get('replay_status') == source_status, 'frozen/replay status differs')
        require(check.get('intermediates_eligible') is True and check.get('compare', {}).get('pass') is True
                and not check.get('differences') and check['compare']['difference_count'] == 0, 'exact frozen record comparison failed')
        require(check.get('capture_status') == 'captured_unverified_replay', 'capture status invalid')
        capture = check.get('capture_check', {})
        for key in ('pass', 'hooks_restored', 'native_mutation_preserved', 'adapter_input_unchanged', 'partition_restored', 'native_slo_exact'):
            require(capture.get(key) is True, 'capture invariant missing/failed: ' + key)
        require(capture.get('adapter_status') == source_status and capture.get('adapter_threw') is False, 'adapter classification not preserved')
        if source_status == 'OK':
            require(capture.get('native_count_and_score_formulas_exact') is True, 'native formula check failed')
        else:
            require(capture.get('native_outcome') == 'exception', 'ERROR posthoc did not preserve native exception')
    return {'phase': phase, 'status': 'PASS', 'check_sha256': sha(directory / 'check.json'),
            'verified_artifact_count': count, 'limits': 'exact fixture/audit/pilot only; no cohort or mechanism claim'}


def terminate(process):
    if process is not None and process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=10)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    parser.add_argument('--baseline-task-bytes', required=True, type=int)
    parser.add_argument('--laptop-reserve-bytes', required=True, type=int)
    args = parser.parse_args()
    output = Path(args.out).resolve()
    require(output.parent == BASE / 'runs' and all(c.isalnum() or c in '-_' for c in output.name), 'output outside new T-032 run')
    require(not output.exists() and args.baseline_task_bytes > 0, 'existing run/invalid baseline')
    require(0 <= args.laptop_reserve_bytes <= MAX_LAPTOP_BYTES, 'laptop reserve exceeds approved 2 GiB')
    require(Path(sys.executable).resolve() == PYTHON.resolve() and Path.home() == Path('/home/ubuntu'), 'unapproved EC2 interpreter/host')
    require(os.environ.get('PYTHONHASHSEED') == '0', 'hashseed must be 0 before startup')

    def pins():
        require(sha(WRAPPER) == WRAPPER_SHA256 and sha(AUDITOR) == AUDITOR_SHA256, 'wrapper/auditor pin changed')
        require(sha(INVENTORY) == INVENTORY_SHA256 and sha(ORIGINAL_INVENTORY) == ORIGINAL_INVENTORY_SHA256, 'source/original inventory changed')
        require(all(sha(SCRIPTS / name) == expected for name, expected in SHARED_PINS.items()), 'shared capture/replay pin changed')

    pins()
    verify_original_inventory()
    before_launch_bytes = logical_size(BASE)
    require(0 <= before_launch_bytes - args.baseline_task_bytes <= 1024 * 1024, 'baseline is not just-before-launch task size')
    require(before_launch_bytes + args.laptop_reserve_bytes + MAX_NEW_BYTES <= MAX_TOTAL_BYTES, 'repair/pilot forecast exceeds combined 12 GiB')
    output.mkdir()
    logs = output / 'logs'
    logs.mkdir()
    started = time.perf_counter()
    phase_started = started
    phase_baseline = args.baseline_task_bytes
    budget_phase = 'repair'
    phase_seconds, phase_bytes = MAX_REPAIR_S, MAX_REPAIR_BYTES
    peak_delta = 0
    process = active = None
    state = {'status': 'STARTING', 'pid': os.getpid(), 'started_utc': now(), 'active': None, 'completed': [],
             'baseline_task_bytes': args.baseline_task_bytes, 'laptop_reserve_bytes': args.laptop_reserve_bytes,
             'max_total_bytes': MAX_TOTAL_BYTES, 'max_laptop_bytes': MAX_LAPTOP_BYTES,
             'max_group_s': MAX_GROUP_S, 'max_child_s': MAX_CHILD_S, 'max_new_bytes': MAX_NEW_BYTES,
             'repair_caps': {'seconds': MAX_REPAIR_S, 'bytes': MAX_REPAIR_BYTES},
             'pilots_caps': {'seconds': MAX_PILOTS_S, 'bytes': MAX_PILOTS_BYTES},
             'poll_s': POLL_S, 'no_retry_no_skip': True, 'cohort_authorized': False,
             'limits': 'all task monitor/temp growth counted; logical-byte polling may overshoot; laptop reserve is a just-measured upper estimate, not live laptop telemetry'}
    dump_new(output / 'invocation.json', {'argv': sys.argv, 'python': sys.executable, 'script_sha256': sha(__file__),
        'wrapper_sha256': WRAPPER_SHA256, 'auditor_sha256': AUDITOR_SHA256, 'shared_pins': SHARED_PINS,
        'inventory_sha256': INVENTORY_SHA256, 'original_inventory_sha256': ORIGINAL_INVENTORY_SHA256,
        'pilots': PILOTS, 'fixture_names': FIXTURE_NAMES, 'serializer_names': SERIALIZER_NAMES})

    def save(event, **fields):
        state.update(elapsed_s=time.perf_counter() - started, peak_measured_new_bytes=peak_delta, updated_utc=now(),
                     budget_phase=budget_phase, budget_phase_elapsed_s=time.perf_counter() - phase_started)
        temporary = output / 'status.tmp'
        temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
        temporary.replace(output / 'status.json')
        item = {'event': event, 'at_utc': now(), **fields, 'elapsed_s': state['elapsed_s']}
        with (output / 'progress.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(item, ensure_ascii=False, allow_nan=False) + '\n')
        print(json.dumps(item, ensure_ascii=False, allow_nan=False), flush=True)

    def guard():
        nonlocal peak_delta
        current = logical_size(BASE)
        delta = max(0, current - args.baseline_task_bytes)
        phase_delta = max(0, current - phase_baseline)
        peak_delta = max(peak_delta, delta)
        state.update(task_logical_bytes=current, measured_new_bytes=delta, measured_phase_bytes=phase_delta)
        require(delta + FINAL_RESERVE_BYTES <= MAX_NEW_BYTES, 'approved total 200 MiB output cap reached')
        require(phase_delta + FINAL_RESERVE_BYTES <= phase_bytes, 'approved ' + budget_phase + ' byte cap reached')
        require(current + args.laptop_reserve_bytes + FINAL_RESERVE_BYTES <= MAX_TOTAL_BYTES, 'combined 12 GiB cap reached')
        require(time.perf_counter() - phase_started < phase_seconds - 20, 'approved ' + budget_phase + ' time cap reached')
        require(time.perf_counter() - started < MAX_GROUP_S - 20, 'approved 1500 s total cap reached')
        pins()

    def on_signal(number, _frame):
        raise PilotError('controller received signal ' + str(number))

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    save('START')
    try:
        stages = [('posthoc', None), ('fixture', None)] + [(pilot[0], pilot) for pilot in PILOTS]
        for phase, pilot in stages:
            if phase == PILOTS[0][0]:
                guard()
                require([v['phase'] for v in state['completed']] == ['posthoc', 'fixture'], 'repair/audit gate not fully passed')
                verify_original_inventory()
                state['repair_cost'] = {'elapsed_s': time.perf_counter() - phase_started,
                                        'measured_new_bytes': max(0, logical_size(BASE) - phase_baseline)}
                phase_started, phase_baseline = time.perf_counter(), logical_size(BASE)
                budget_phase, phase_seconds, phase_bytes = 'pilots', MAX_PILOTS_S, MAX_PILOTS_BYTES
                save('REPAIR_PASS_PILOTS_START')
            guard()
            directory = output / phase
            command = [str(PYTHON), '-B', '-X', 'utf8']
            if phase == 'posthoc':
                command += [str(AUDITOR), str(directory)]
            else:
                command += [str(WRAPPER)] + (['fixture', str(directory)] if phase == 'fixture' else ['one', pilot[1], pilot[2], str(directory)])
            child_started = time.perf_counter()
            active = {'phase': phase, 'command': command, 'directory': str(directory), 'pid': None}
            state['active'] = active
            save('CHILD_START', phase=phase)
            with (logs / (phase + '.stdout.txt')).open('x', encoding='utf-8') as stdout:
                with (logs / (phase + '.stderr.txt')).open('x', encoding='utf-8') as stderr:
                    process = subprocess.Popen(command, cwd=BASE, env=os.environ.copy(), stdout=stdout, stderr=stderr, start_new_session=True)
                    active['pid'] = process.pid
                    dump_new(logs / (phase + '.pid.json'), {'pid': process.pid, 'command': command})
                    save('CHILD_RUNNING', phase=phase, child_pid=process.pid)
                    last_progress = 0
                    while process.poll() is None:
                        guard()
                        child_elapsed = time.perf_counter() - child_started
                        require(child_elapsed < MAX_CHILD_S - 20, 'approved child 600 s cap reached')
                        if child_elapsed - last_progress >= 10:
                            save('CHILD_POLL', phase=phase, child_elapsed_s=child_elapsed, measured_new_bytes=state['measured_new_bytes'])
                            last_progress = child_elapsed
                        time.sleep(POLL_S)
            child_cost = {'pid': process.pid, 'exit_code': process.returncode, 'elapsed_s': time.perf_counter() - child_started, 'command': command}
            dump_new(logs / (phase + '.process.json'), child_cost)
            require(process.returncode == 0 and child_cost['elapsed_s'] <= MAX_CHILD_S, 'child failed; no next stage')
            guard()
            verdict = validate_child(directory, phase, pilot)
            verdict['cost'] = child_cost
            dump_new(logs / (phase + '.verified.json'), verdict)
            state['completed'].append(verdict)
            state['active'] = active = process = None
            save('CHILD_PASS', phase=phase)
        guard()
        verify_original_inventory()
        state.update(status='PASS_DTYPE_FIXTURE_ERROR_AUDIT_AND_TWO_PILOTS', cohort_authorized=False)
        save('FINISH')
        return 0
    except BaseException as error:
        terminate(process)
        if active is not None and not (logs / (active['phase'] + '.process.json')).exists():
            dump_new(logs / (active['phase'] + '.process.json'), {'pid': active['pid'],
                'exit_code': process.returncode if process is not None else None, 'command': active['command'],
                'error': str(error), 'retained': 'all partial outputs/stdout/stderr'})
        state.update(status='FAIL_STOP', error_type=type(error).__name__, error=str(error), cohort_authorized=False)
        dump_new(output / 'failure.json', {'error': str(error), 'traceback': traceback.format_exc(), 'state': state})
        save('FAIL_STOP', error=str(error), active=active)
        return 1
    finally:
        terminate(process)


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())
