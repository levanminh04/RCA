"""Q-125 launcher and detached watchdog; immutable segments, full closed streams.

Run on EC2 only, after root source/code review and a fresh approved-budget
snapshot. Parent returns after spawning a new session; no SSH/laptop lifetime
dependency. --supervise is internal. No native imports or method/fixture calls.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback
import threading
import hashlib

BASE = Path('/home/ubuntu/rca/T-032')
PYTHON = Path('/home/ubuntu/rca/T-025/envs/main/bin/python')
RUN = BASE / 'runs/tracerca-cohort-001'
TOOLS = BASE / 'runs/tracerca-cohort-proposal-001/tool-check-v2/tool-pins.json'
CONTROLLER = BASE / 'scripts/run_tracerca_cohort_v2.py'


def load_controller(expected):
    import hashlib
    digest = hashlib.sha256(TOOLS.read_bytes()).hexdigest()
    if digest != expected:
        raise RuntimeError('tool receipt hash differs before controller import')
    pins = json.loads(TOOLS.read_text(encoding='utf-8-sig'))
    actual = hashlib.sha256(CONTROLLER.read_bytes()).hexdigest()
    if actual != pins['scripts']['run_tracerca_cohort_v2.py']:
        raise RuntimeError('controller pin differs before stdlib-only import')
    spec = importlib.util.spec_from_file_location('tracerca_cohort_pinned_stdlib', CONTROLLER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.tool_pins(expected)
    return module


def parameters():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--segment', required=True, type=int)
    parser.add_argument('--previous-closure-sha256')
    parser.add_argument('--previous-accounting-sha256')
    parser.add_argument('--snapshot', required=True)
    parser.add_argument('--snapshot-sha256', required=True)
    parser.add_argument('--tool-pins-sha256', required=True)
    parser.add_argument('--case-limit', required=True, type=int)
    parser.add_argument('--supervise', action='store_true')
    parser.add_argument('--account', action='store_true')
    return parser.parse_args()


def controller_argv(args):
    command = [str(PYTHON), '-B', '-X', 'utf8', str(CONTROLLER),
        '--segment', str(args.segment), '--snapshot', args.snapshot,
        '--snapshot-sha256', args.snapshot_sha256, '--tool-pins-sha256', args.tool_pins_sha256,
        '--case-limit', str(args.case_limit)]
    if args.previous_closure_sha256 is not None:
        command += ['--previous-closure-sha256', args.previous_closure_sha256]
    if args.previous_accounting_sha256 is not None:
        command += ['--previous-accounting-sha256', args.previous_accounting_sha256]
    return command


def close_stdio():
    """The wrapper owns the stream; close a non-owning raw descriptor once."""
    for stream in (sys.stdout, sys.stderr):
        descriptor = stream.fileno()
        raw_owns_descriptor = stream.buffer.raw.closefd
        stream.flush()
        stream.close()
        if not raw_owns_descriptor:
            os.close(descriptor)


def signal_stop(c, known, child=None):
    table = c.proc_table()
    for pid in c.tree_pids(os.getpid(), table) - {os.getpid()}:
        known.add((pid, table[pid]['start_ticks']))
    for number in (signal.SIGTERM, signal.SIGKILL):
        table = c.proc_table()
        for pid, identity in tuple(known):
            if pid in table and table[pid]['start_ticks'] == identity and table[pid]['state'] != 'Z':
                try:
                    os.kill(pid, number)
                except ProcessLookupError:
                    pass
        if child is not None:
            try:
                child.wait(timeout=3)
            except subprocess.TimeoutExpired:
                pass
    table = c.proc_table()
    c.require(not any(pid in table and table[pid]['start_ticks'] == identity and table[pid]['state'] != 'Z'
                      for pid, identity in known), 'known descendant survived fail-stop')


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def run_supervisor(c, args, segment):
    started = time.monotonic()
    child = None
    known = set()
    state = {'status': 'STARTING', 'supervisor_pid': os.getpid(), 'segment': args.segment,
             'started_utc': c.now(), 'controller_command': controller_argv(args), 'controller_pid': None,
             'manual_complete': False, 'research_complete': False, 'physical_wait': 'OPEN'}
    c.dump_new(segment / 'supervisor.pid.json', {'pid': os.getpid(), 'start_ticks': c.proc_table()[os.getpid()]['start_ticks']})

    def save(event):
        state.update(updated_utc=c.now(), elapsed_s=time.monotonic() - started)
        c.atomic(segment / 'supervisor-status.json', state)
        with (segment / 'supervisor-progress.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'event': event, **state}, ensure_ascii=False, allow_nan=False) + '\n')

    def on_signal(number, _frame):
        raise RuntimeError('supervisor signal ' + str(number))

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    save('START')
    try:
        c.tool_pins(args.tool_pins_sha256)
        with (segment / 'controller-stdout.txt').open('x', encoding='utf-8') as out, (segment / 'controller-stderr.txt').open('x', encoding='utf-8') as err:
            child = subprocess.Popen(controller_argv(args), cwd=BASE, env=os.environ.copy(), stdout=out, stderr=err,
                                     stdin=subprocess.DEVNULL, start_new_session=True, close_fds=True)
            identity = c.proc_table().get(child.pid, {}).get('start_ticks')
            c.require(isinstance(identity, int) and identity > 0, 'controller identity missed')
            known.add((child.pid, identity))
            state.update(status='RUNNING', controller_pid=child.pid, controller_start_ticks=identity)
            save('CONTROLLER_STARTED')
            while child.poll() is None:
                table = c.proc_table()
                known.update((pid, table[pid]['start_ticks']) for pid in c.tree_pids(os.getpid(), table) - {os.getpid()})
                time.sleep(0.1)
            state['controller_exit_code'] = child.returncode
        signal_stop(c, known, child)
        terminal = c.read(segment / 'terminal.json')
        c.require(child.returncode == 0 and terminal['controller_exit_code'] == 0 and terminal['status'] in c.SUCCESS,
                  'controller failed or lacks successful terminal proof')
        c.require(terminal['table_sha256'] == c.sha(segment / 'table-52.json')
                  and terminal['status_sha256'] == c.sha(segment / 'status.json'), 'controller terminal binding differs')
        state['status'] = terminal['status']
    except BaseException as exc:
        try:
            signal_stop(c, known, child)
        except BaseException as stop_error:
            state['stop_error'] = str(stop_error)
        state.update(status='FAIL_STOP', error=str(exc), traceback=traceback.format_exc(),
                     controller_exit_code=None if child is None else child.returncode)
        c.dump_new(segment / 'supervisor-failure.json', state)
        if not (segment / 'table-52.json').exists():
            c.dump_new(segment / 'table-52.json', {'plan_sha256': c.PLAN_SHA,
                'rows': c.read(segment / 'initial-table-52.json')['rows'], 'status': 'FAIL_STOP',
                'all_results_unverified': True, 'manual_complete': False})
    state['descendant_identities'] = [{'pid': pid, 'start_ticks': ticks} for pid, ticks in sorted(known)]
    save('TERMINAL')
    c.dump_new(segment / 'supervisor-terminal.json', {'status': state['status'], 'controller_exit_code': state.get('controller_exit_code'),
        'table_sha256': c.sha(segment / 'table-52.json'), 'descendant_identities': state['descendant_identities'],
        'supervisor_status_sha256': c.sha(segment / 'supervisor-status.json'), 'retained_all_outputs': True})
    # Child streams closed above. Parent accountant closes supervisor streams
    # only after actual supervisor exit, then authenticates this preliminary seal.
    cases = [{'directory': str(p), 'files': c.inventory(p)} for p in sorted((RUN / 'cases').iterdir()) if p.is_dir()]
    c.dump_new(segment / 'closed-manifest.json', {'status': state['status'], 'root': str(segment), 'at_utc': c.now(),
        'controller_exit_code': state.get('controller_exit_code'), 'streams_closed': True,
        'stream_scope': 'controller and case streams; supervisor streams closed by accountant after exit',
        'supervisor_pid': os.getpid(), 'supervisor_elapsed_before_final_seal_s': time.monotonic() - started,
        'case_files': cases, 'files': c.inventory(segment), 'manifest_excludes': ['closed-manifest.json'],
        'whole_supervisor_accounting_required': True, 'research_complete': False, 'manual_complete': False, 'physical_wait': 'OPEN'})
    return 0 if state['status'] in c.SUCCESS else 1


def run_accountant(c, args, segment, directory):
    # This enclosing process charges actual supervisor startup, controller,
    # terminal, complete hashing/sealing, stream closure and supervisor exit.
    started = time.monotonic()
    child = None
    known = set()
    lock = threading.Lock()
    stopping = threading.Event()
    resource_failure = []
    peak = 0
    max_gap = 0.0
    samples = 0
    prior_wall, old_baseline = c.previous_accounting(args.segment, args.previous_closure_sha256, args.previous_accounting_sha256)
    snapshot, _ = c.validate_snapshot(args.snapshot, args.snapshot_sha256, prior_wall, old_baseline)
    baseline = snapshot['remote_task_bytes'] if old_baseline is None else old_baseline
    own_identity = c.proc_table()[os.getpid()]['start_ticks']
    c.dump_new(directory / 'accountant.pid.json', {'pid': os.getpid(), 'start_ticks': own_identity})
    command = [str(PYTHON), '-B', '-X', 'utf8', str(Path(__file__)), *[a for a in sys.argv[1:] if a != '--account'], '--supervise']
    state = {'status': 'STARTING', 'segment': args.segment, 'accountant_pid': os.getpid(),
             'initial_baseline_task_bytes': baseline, 'prior_charged_elapsed_s': prior_wall,
             'at_utc': c.now(), 'supervisor_command': command, 'controller_command': controller_argv(args)}
    c.dump_new(directory / 'invocation.json', {**state, 'argv': sys.argv, 'script_sha256': c.sha(__file__),
        'tool_pins_sha256': args.tool_pins_sha256, 'snapshot_sha256': args.snapshot_sha256,
        'snapshot_path': args.snapshot, 'previous_accounting_sha256': args.previous_accounting_sha256})

    def sample_resources():
        nonlocal peak, max_gap, samples
        last = time.monotonic()
        try:
            with (directory / 'resource-samples.jsonl').open('x', encoding='utf-8') as stream:
                while not stopping.is_set():
                    timestamp = time.monotonic()
                    table = c.proc_table()
                    pids = c.tree_pids(os.getpid(), table)
                    memory = {line.split(':')[0]: int(line.split()[1]) * 1024
                              for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith('MemAvailable:')}
                    rss = sum(table[pid]['rss'] for pid in pids)
                    available = memory['MemAvailable']
                    with lock:
                        known.update((pid, table[pid]['start_ticks']) for pid in pids - {os.getpid()})
                        peak = max(peak, rss)
                        max_gap = max(max_gap, timestamp - last)
                        samples += 1
                    stream.write(json.dumps({'at_utc': c.now(), 'monotonic': timestamp, 'sampled_tree_rss_bytes': rss,
                        'available_ram_bytes': available, 'identities': [[pid, table[pid]['start_ticks']] for pid in sorted(pids)]},
                        ensure_ascii=False, allow_nan=False) + '\n')
                    stream.flush()
                    if rss > c.MAX_RSS_BYTES or available < c.MIN_AVAILABLE_BYTES:
                        raise RuntimeError('independent RSS/RAM guard reached')
                    last = timestamp
                    stopping.wait(0.1)
        except BaseException as exc:
            with lock:
                resource_failure.append(str(exc))
                identities = set(known)
            # Stop current descendants immediately even if main is hashing or
            # measuring a large inventory. PID creation ticks prevent reuse kill.
            try:
                signal_stop(c, identities, child)
            except BaseException as stop_error:
                with lock:
                    resource_failure.append('resource stop: ' + str(stop_error))

    def guard():
        with lock:
            c.require(not resource_failure, 'resource monitor failed: ' + '; '.join(resource_failure))
        measured = c.logical_size(BASE)
        c.require(measured >= baseline and measured - baseline + c.RESERVE_BYTES <= c.MAX_NEW_BYTES, 'accountant: package growth cap')
        c.require(measured + c.LAPTOP_RESERVE_BYTES + c.RESERVE_BYTES <= c.MAX_COMBINED_BYTES, 'accountant: combined 12 GiB cap')
        c.require(time.monotonic() - started + prior_wall + c.CLOSING_ALLOCATION_S <= c.MAX_WALL_S, 'accountant: whole package wall cap')
        disk = os.statvfs(BASE)
        c.require(disk.f_bavail * disk.f_frsize >= c.RESERVE_BYTES and not (RUN / 'STOP').exists(), 'accountant: disk/root stop')
        if (segment / 'status.json').is_file():
            active = c.read(segment / 'status.json').get('active')
            if active:
                c.require(time.monotonic() - active['started_monotonic'] + c.CASE_CLOSING_ALLOCATION_S <= c.MAX_CASE_S,
                          'accountant: whole case verification/sealing time cap')
                c.require(measured - active['baseline_task_bytes'] + c.RESERVE_BYTES <= c.MAX_CASE_BYTES,
                          'accountant: whole case verification/sealing bytes cap')
        return measured

    def on_signal(number, _frame):
        raise RuntimeError('accountant signal ' + str(number))

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    monitor = threading.Thread(target=sample_resources, name='existing-resource-guard', daemon=True)
    monitor.start()
    supervisor_actual = None
    try:
        guard()
        with (directory / 'supervisor-stdout.txt').open('x', encoding='utf-8') as out, (directory / 'supervisor-stderr.txt').open('x', encoding='utf-8') as err:
            supervisor_started = time.monotonic()
            child = subprocess.Popen(command, cwd=BASE, env=os.environ.copy(), stdout=out, stderr=err,
                                     stdin=subprocess.DEVNULL, start_new_session=True, close_fds=True)
            identity = c.proc_table().get(child.pid, {}).get('start_ticks')
            c.require(isinstance(identity, int) and identity > 0, 'supervisor identity missed')
            with lock:
                known.add((child.pid, identity))
            c.dump_new(directory / 'supervisor-process.json', {'pid': child.pid, 'start_ticks': identity, 'command': command})
            while child.poll() is None:
                guard()
                time.sleep(0.1)
            supervisor_actual = time.monotonic() - supervisor_started
        # Closing the parent-owned supervisor stdout/stderr now follows exit.
        with lock:
            identities = set(known)
        signal_stop(c, identities, child)
        c.require(child.returncode == 0, 'supervisor failed')
        closed = c.closure(segment)
        state['status'] = closed['status']
        guard()
    except BaseException as exc:
        with lock:
            identities = set(known)
        try:
            signal_stop(c, identities, child)
        except BaseException as stop_error:
            state['stop_error'] = str(stop_error)
        state.update(status='FAIL_STOP', error=str(exc), traceback=traceback.format_exc())
        c.dump_new(directory / 'failure.json', state)
    finally:
        stopping.set()
        monitor.join(timeout=3)
    with lock:
        state.update(descendant_identities=[{'pid': pid, 'start_ticks': ticks} for pid, ticks in sorted(known)],
                     resource_failure=list(resource_failure), sampled_peak_tree_rss_bytes=peak,
                     max_sampling_gap_s=max_gap, sample_count=samples)
    if monitor.is_alive() or state['resource_failure']:
        state['status'] = 'FAIL_STOP'
    c.dump_new(directory / 'resource-summary.json', {**state,
        'measurement_note': 'independent sampled RSS tree; may miss shorter peaks; no OS lifetime-peak claim',
        'poll_s': 0.1, 'inventory_on_resource_thread': False})
    # No output is printed after this point. Every expensive saved-byte hash is
    # computed before taking the charged time; only two small final files remain.
    closed_sha = c.sha(segment / 'closed-manifest.json') if (segment / 'closed-manifest.json').exists() else None
    close_stdio()
    existing_files = c.inventory(directory, ('ledger.json', 'manifest.json'))
    measured = c.logical_size(BASE)
    observed = time.monotonic() - started
    charged = observed + c.CLOSING_ALLOCATION_S
    budget_pass = (state['status'] in c.SUCCESS and 0 <= measured - baseline + c.RESERVE_BYTES <= c.MAX_NEW_BYTES
                   and measured + c.LAPTOP_RESERVE_BYTES + c.RESERVE_BYTES <= c.MAX_COMBINED_BYTES
                   and prior_wall + charged <= c.MAX_WALL_S)
    final_status = state['status'] if budget_pass else 'FAIL_STOP'
    ledger = {**state, 'status': final_status, 'segment_root': str(segment), 'supervisor_exit_code': None if child is None else child.returncode,
        'supervisor_closed_sha256': closed_sha,
        'supervisor_actual_elapsed_s': supervisor_actual, 'accountant_observed_elapsed_s': observed,
        'closing_allocation_s': c.CLOSING_ALLOCATION_S, 'charged_elapsed_s': charged,
        'previous_accounting_sha256': args.previous_accounting_sha256, 'budget_pass': budget_pass,
        'task_bytes_before_final_receipts': measured, 'new_bytes_including_final_reserve': measured - baseline + c.RESERVE_BYTES,
        'byte_reserve': c.RESERVE_BYTES, 'whole_supervisor_observed': supervisor_actual is not None,
        'streams_closed': True, 'closing_allocation_is_measured': False,
        'accountant_time_note': 'observed through supervisor actual exit/closed streams and saved-byte hashing; explicit20s covers final two small receipt writes and accountant exit, not a measured duration',
        'manual_complete': False, 'research_complete': False, 'physical_wait': 'OPEN'}
    ledger_bytes = encode(ledger)
    files = existing_files + [{'path': 'ledger.json', 'bytes': len(ledger_bytes), 'sha256': hashlib.sha256(ledger_bytes).hexdigest()}]
    manifest_bytes = encode({'status': final_status, 'files': sorted(files, key=lambda x: x['path']), 'manifest_excludes': ['manifest.json']})
    c.require(len(ledger_bytes) + len(manifest_bytes) <= c.RESERVE_BYTES, 'final receipts exceed explicit byte reserve')
    with (directory / 'ledger.json').open('xb') as stream:
        stream.write(ledger_bytes)
    with (directory / 'manifest.json').open('xb') as stream:
        stream.write(manifest_bytes)
    return 0 if final_status in c.SUCCESS else 1


def main():
    args = parameters()
    c = load_controller(args.tool_pins_sha256)
    c.require(Path(sys.executable).resolve() == PYTHON.resolve() and Path.home() == Path('/home/ubuntu'), 'unapproved host/interpreter')
    c.require(1 <= args.segment <= 49 and 1 <= args.case_limit <= 49 and not (args.supervise and args.account), 'segment/case-limit/role invalid')
    segment = RUN / 'segments' / f'{args.segment:03d}'
    directory = RUN / 'accounting' / segment.name
    if args.supervise:
        c.require(segment.is_dir() and not (segment / 'supervisor-status.json').exists(), 'existing supervisor; no retry')
        return run_supervisor(c, args, segment)
    if args.account:
        c.require(directory.is_dir() and not (directory / 'invocation.json').exists(), 'existing accountant; no retry')
        return run_accountant(c, args, segment, directory)
    prior_wall, baseline = c.previous_accounting(args.segment, args.previous_closure_sha256, args.previous_accounting_sha256)
    c.validate_snapshot(args.snapshot, args.snapshot_sha256, prior_wall, baseline)
    rows = c.load_plan()
    if args.segment == 1:
        c.require(not RUN.exists(), 'cohort already exists; no restart')
        RUN.mkdir()
        (RUN / 'segments').mkdir()
        (RUN / 'cases').mkdir()
        (RUN / 'accounting').mkdir()
    else:
        c.require(RUN.is_dir() and (RUN / 'accounting').is_dir(), 'missing whole-supervisor package history')
    segment.mkdir(exist_ok=False)
    (segment / 'logs').mkdir()
    directory.mkdir(exist_ok=False)
    c.dump_new(segment / 'initial-table-52.json', {'plan_sha256': c.PLAN_SHA, 'rows': c.table_initial(rows), 'status': 'NOT_LAUNCHED', 'manual_complete': False})
    command = [str(PYTHON), '-B', '-X', 'utf8', str(Path(__file__)), *sys.argv[1:], '--account']
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8', PYTHONHASHSEED='0',
               PYTHONPATH=str(BASE / 'scripts') + ':' + str(BASE / 'repo/src') +
               ':/home/ubuntu/rca/T-025/src/RCAEval:/home/ubuntu/rca/T-025/src/baro:/home/ubuntu/rca/T-025/src/CIRCA',
               TMPDIR=str(BASE / 'tmp'), XDG_CACHE_HOME=str(BASE / 'cache'), MPLCONFIGDIR=str(BASE / 'cache/mpl'), MPLBACKEND='Agg')
    c.require((BASE / 'tmp').is_dir() and (BASE / 'cache/mpl').is_dir(), 'approved existing temp/cache missing')
    with (directory / 'accountant-stdout.txt').open('x', encoding='utf-8') as out, (directory / 'accountant-stderr.txt').open('x', encoding='utf-8') as err:
        child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                 cwd=BASE, env=env, start_new_session=True, close_fds=True)
        c.dump_new(segment / 'launcher.json', {'at_utc': c.now(), 'accountant_pid': child.pid,
            'accountant_command': command, 'controller_command': controller_argv(args),
            'snapshot_sha256': args.snapshot_sha256, 'tool_pins_sha256': args.tool_pins_sha256,
            'detached_session': True, 'single_heavy_worker': True, 'thread_environment_preserved': True})
    print(json.dumps({'status': 'DETACHED_START_REQUESTED', 'accountant_pid': child.pid, 'segment': str(segment), 'accounting': str(directory)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())
