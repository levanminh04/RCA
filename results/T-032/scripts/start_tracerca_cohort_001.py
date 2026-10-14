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

BASE = Path('/home/ubuntu/rca/T-032')
PYTHON = Path('/home/ubuntu/rca/T-025/envs/main/bin/python')
RUN = BASE / 'runs/tracerca-cohort-001'
TOOLS = BASE / 'runs/tracerca-cohort-proposal-001/tool-check/tool-pins.json'
CONTROLLER = BASE / 'scripts/run_tracerca_cohort_v1.py'


def load_controller(expected):
    import hashlib
    digest = hashlib.sha256(TOOLS.read_bytes()).hexdigest()
    if digest != expected:
        raise RuntimeError('tool receipt hash differs before controller import')
    pins = json.loads(TOOLS.read_text(encoding='utf-8-sig'))
    actual = hashlib.sha256(CONTROLLER.read_bytes()).hexdigest()
    if actual != pins['scripts']['run_tracerca_cohort_v1.py']:
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
    parser.add_argument('--snapshot', required=True)
    parser.add_argument('--snapshot-sha256', required=True)
    parser.add_argument('--tool-pins-sha256', required=True)
    parser.add_argument('--case-limit', required=True, type=int)
    parser.add_argument('--supervise', action='store_true')
    return parser.parse_args()


def controller_argv(args):
    command = [str(PYTHON), '-B', '-X', 'utf8', str(CONTROLLER),
        '--segment', str(args.segment), '--snapshot', args.snapshot,
        '--snapshot-sha256', args.snapshot_sha256, '--tool-pins-sha256', args.tool_pins_sha256,
        '--case-limit', str(args.case_limit)]
    if args.previous_closure_sha256 is not None:
        command += ['--previous-closure-sha256', args.previous_closure_sha256]
    return command


def main():
    args = parameters()
    c = load_controller(args.tool_pins_sha256)
    c.require(Path(sys.executable).resolve() == PYTHON.resolve() and Path.home() == Path('/home/ubuntu'), 'unapproved host/interpreter')
    c.require(1 <= args.segment <= 49 and 1 <= args.case_limit <= 49, 'segment/case-limit invalid')
    segment = RUN / 'segments' / f'{args.segment:03d}'
    if not args.supervise:
        # Authorization/snapshot preflight is read-only. Failure here launches
        # nothing and does not create a misleading partial scientific result.
        c.validate_snapshot(args.snapshot, args.snapshot_sha256)
        rows = c.load_plan()
        if args.segment == 1:
            c.require(not RUN.exists() and args.previous_closure_sha256 is None, 'cohort already exists; no restart')
            RUN.mkdir()
            (RUN / 'segments').mkdir()
            (RUN / 'cases').mkdir()
        else:
            c.require(RUN.is_dir() and args.previous_closure_sha256 is not None, 'missing explicit previous checkpoint')
            c.closure(RUN / 'segments' / f'{args.segment - 1:03d}', args.previous_closure_sha256)
        segment.mkdir(exist_ok=False)
        (segment / 'logs').mkdir()
        c.dump_new(segment / 'initial-table-52.json', {'plan_sha256': c.PLAN_SHA, 'rows': c.table_initial(rows),
                   'status': 'NOT_LAUNCHED', 'manual_complete': False})
        command = [str(PYTHON), '-B', '-X', 'utf8', str(Path(__file__)), *sys.argv[1:], '--supervise']
        env = os.environ.copy()
        env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8', PYTHONHASHSEED='0',
                   PYTHONPATH=str(BASE / 'scripts') + ':' + str(BASE / 'repo/src') +
                   ':/home/ubuntu/rca/T-025/src/RCAEval:/home/ubuntu/rca/T-025/src/baro:/home/ubuntu/rca/T-025/src/CIRCA',
                   TMPDIR=str(BASE / 'tmp'), XDG_CACHE_HOME=str(BASE / 'cache'),
                   MPLCONFIGDIR=str(BASE / 'cache/mpl'), MPLBACKEND='Agg')
        # Preserve thread-related settings. Q-125 authorizes no environment repair.
        c.require((BASE / 'tmp').is_dir() and (BASE / 'cache/mpl').is_dir(), 'approved existing temp/cache missing')
        with (segment / 'launcher-stdout.txt').open('x', encoding='utf-8') as out, (segment / 'launcher-stderr.txt').open('x', encoding='utf-8') as err:
            child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                     cwd=BASE, env=env, start_new_session=True, close_fds=True)
            c.dump_new(segment / 'launcher.json', {'at_utc': c.now(), 'supervisor_pid': child.pid,
                       'supervisor_command': command, 'controller_command': controller_argv(args),
                       'snapshot_sha256': args.snapshot_sha256, 'tool_pins_sha256': args.tool_pins_sha256,
                       'detached_session': True, 'single_heavy_worker': True,
                       'pythonhashseed': '0', 'thread_environment_preserved': True})
        print(json.dumps({'status': 'DETACHED_START_REQUESTED', 'supervisor_pid': child.pid,
                          'segment': str(segment), 'progress': str(segment / 'supervisor-progress.jsonl')}, ensure_ascii=False))
        return 0

    # The detached process writes terminal status, then closes BOTH its own
    # inherited streams and the controller streams before hashing the segment.
    # A manifest failure leaves an unclosed segment, which cannot be continued.
    started = time.monotonic()
    c.require(segment.is_dir() and not (segment / 'supervisor-status.json').exists(), 'existing supervisor; no retry')
    state = {'status': 'STARTING', 'at_utc': c.now(), 'supervisor_pid': os.getpid(),
             'controller_command': controller_argv(args), 'controller_pid': None,
             'max_tree_rss_bytes': c.MAX_RSS_BYTES, 'ram_reserve_bytes': c.MIN_AVAILABLE_BYTES,
             'peak_tree_rss_bytes': 0, 'segment': args.segment, 'closed': False}
    c.dump_new(segment / 'supervisor.pid.json', {'pid': os.getpid(), 'start_ticks': c.proc_table()[os.getpid()]['start_ticks']})
    child = None
    known = {}
    prior_wall = 0.0
    baseline = None
    controller_return = None
    last_progress = 0.0

    def save(event):
        state.update(updated_utc=c.now(), elapsed_s=time.monotonic() - started)
        c.atomic(segment / 'supervisor-status.json', state)
        with (segment / 'supervisor-progress.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'event': event, **state}, ensure_ascii=False, allow_nan=False) + '\n')

    def stop_tree():
        nonlocal known
        table = c.proc_table()
        for pid in c.tree_pids(os.getpid(), table) - {os.getpid()}:
            known[pid] = table[pid]['start_ticks']
        for number in (signal.SIGTERM, signal.SIGKILL):
            table = c.proc_table()
            for pid, identity in list(known.items()):
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
                          for pid, identity in known.items()), 'descendant process survived fail-stop')

    def on_signal(number, _frame):
        raise RuntimeError('supervisor signal ' + str(number))

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    save('START')
    try:
        c.tool_pins(args.tool_pins_sha256)
        c.validate_snapshot(args.snapshot, args.snapshot_sha256)
        if args.segment > 1:
            for i in range(1, args.segment):
                closed = c.closure(RUN / 'segments' / f'{i:03d}', args.previous_closure_sha256 if i == args.segment - 1 else None)
                prior_wall += closed['segment_elapsed_s']
            baseline = c.read(RUN / 'segments/001/invocation.json')['initial_baseline_task_bytes']
        else:
            baseline = c.read(args.snapshot)['remote_task_bytes']
        state.update(initial_baseline_task_bytes=baseline, prior_segment_wall_s=prior_wall)
        with (segment / 'controller-stdout.txt').open('x', encoding='utf-8') as out, (segment / 'controller-stderr.txt').open('x', encoding='utf-8') as err:
            child = subprocess.Popen(controller_argv(args), cwd=BASE, env=os.environ.copy(), stdout=out, stderr=err,
                                     stdin=subprocess.DEVNULL, start_new_session=True, close_fds=True)
            state.update(status='RUNNING', controller_pid=child.pid)
            save('CONTROLLER_STARTED')
            while child.poll() is None:
                measured = c.logical_size(BASE)
                resource = c.resources(os.getpid())
                table = c.proc_table()
                for pid in c.tree_pids(os.getpid(), table) - {os.getpid()}:
                    known[pid] = table[pid]['start_ticks']
                state.update(resources=resource, remote_task_bytes=measured, measured_new_bytes=measured - baseline,
                             peak_tree_rss_bytes=max(state['peak_tree_rss_bytes'], resource['tree_rss_bytes']))
                c.require(measured >= baseline and measured - baseline + c.RESERVE_BYTES <= c.MAX_NEW_BYTES, 'watchdog: 2.5 GiB growth cap')
                c.require(measured + c.LAPTOP_RESERVE_BYTES + c.RESERVE_BYTES <= c.MAX_COMBINED_BYTES, 'watchdog: combined 12 GiB cap')
                c.require(time.monotonic() - started + prior_wall < c.MAX_WALL_S - 10, 'watchdog: cumulative 4.5 hour cap')
                c.require(resource['tree_rss_bytes'] <= c.MAX_RSS_BYTES and resource['available_ram_bytes'] >= c.MIN_AVAILABLE_BYTES,
                          'watchdog: RSS/RAM reserve')
                c.require(resource['free_disk_bytes'] >= c.RESERVE_BYTES and not (RUN / 'STOP').exists(), 'watchdog: disk/root stop')
                if (segment / 'status.json').is_file():
                    active = c.read(segment / 'status.json').get('active')
                    if active:
                        c.require(time.monotonic() - active['started_monotonic'] < c.MAX_CASE_S - 6, 'watchdog: case 600 s cap')
                        c.require(measured - active['baseline_task_bytes'] + c.RESERVE_BYTES <= c.MAX_CASE_BYTES,
                                  'watchdog: case 150 MiB cap')
                if time.monotonic() - started - last_progress >= 10:
                    save('POLL')
                    last_progress = time.monotonic() - started
                time.sleep(0.5)
            controller_return = child.returncode
        # All controller/native stdout/stderr handles have now been closed.
        stop_tree()
        terminal = c.read(segment / 'terminal.json')
        c.require(controller_return == 0 and terminal['controller_exit_code'] == 0 and terminal['status'] in c.SUCCESS,
                  'controller failed or lacks terminal proof')
        c.require(terminal['table_sha256'] == c.sha(segment / 'table-52.json')
                  and terminal['status_sha256'] == c.sha(segment / 'status.json'), 'terminal table/status binding differs')
        state.update(status=terminal['status'], controller_exit_code=controller_return)
    except BaseException as exc:
        try:
            stop_tree()
        except BaseException as stopping_error:
            state['stop_error'] = str(stopping_error)
        state.update(status='FAIL_STOP', error=str(exc), traceback=traceback.format_exc(),
                     controller_exit_code=None if child is None else child.returncode)
        c.dump_new(segment / 'supervisor-failure.json', state)
        # Preserve the controller's last table. If it died before writing one,
        # provide all 52 rows with explicit unverified/pending status.
        if not (segment / 'table-52.json').exists():
            c.dump_new(segment / 'table-52.json', {'plan_sha256': c.PLAN_SHA,
                'rows': c.read(segment / 'initial-table-52.json')['rows'], 'status': 'FAIL_STOP',
                'all_results_unverified': True, 'manual_complete': False})
    state.update(descendant_identities={str(pid): ticks for pid, ticks in known.items()},
                 remote_task_bytes=c.logical_size(BASE), resources=c.resources(os.getpid()))
    save('TERMINAL_STREAMS_CLOSING')
    c.dump_new(segment / 'supervisor-terminal.json', {'status': state['status'], 'controller_exit_code': state.get('controller_exit_code'),
        'table_sha256': c.sha(segment / 'table-52.json'), 'descendant_identities': state['descendant_identities'],
        'supervisor_status_sha256': c.sha(segment / 'supervisor-status.json'), 'retained_all_outputs': True})
    # Close our inherited stdout/stderr, then never print again.
    sys.stdout.flush()
    sys.stderr.flush()
    sys.stdout.close()
    sys.stderr.close()
    os.close(1)
    os.close(2)
    cases = [{'directory': str(p), 'files': c.inventory(p)} for p in sorted((RUN / 'cases').iterdir()) if p.is_dir()]
    measured = c.logical_size(BASE)
    elapsed = time.monotonic() - started
    within_budget = (baseline is not None and 0 <= measured - baseline + c.RESERVE_BYTES <= c.MAX_NEW_BYTES
                     and measured + c.LAPTOP_RESERVE_BYTES + c.RESERVE_BYTES <= c.MAX_COMBINED_BYTES
                     and elapsed + prior_wall <= c.MAX_WALL_S)
    final_status = state['status'] if within_budget else 'FAIL_STOP'
    c.dump_new(segment / 'closed-manifest.json', {'status': final_status, 'root': str(segment),
        'at_utc': c.now(), 'segment_elapsed_s': elapsed, 'prior_segment_wall_s': prior_wall,
        'controller_exit_code': state.get('controller_exit_code'), 'streams_closed': True,
        'supervisor_pid': os.getpid(), 'budget_including_close_pass': within_budget,
        'remote_task_bytes_before_manifest': measured, 'case_files': cases,
        'files': c.inventory(segment), 'manifest_excludes': ['closed-manifest.json'],
        'research_complete': False, 'manual_complete': False, 'physical_wait': 'OPEN'})
    return 0 if final_status in c.SUCCESS else 1


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())
