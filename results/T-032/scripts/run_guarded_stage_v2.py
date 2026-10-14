"""Run one T-032 command detached from SSH, retaining PID, progress and failures."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback
import psutil

BASE = Path.home() / 'rca/T-032'

def size_tree(root):
    total = 0
    for parent, directories, files in os.walk(root):
        for name in files:
            p = Path(parent) / name
            if not p.is_symlink():
                try:
                    total += p.stat().st_size
                except FileNotFoundError:
                    pass
    return total

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--local-bytes', required=True, type=int)
    parser.add_argument('--max-wall-s', type=float, required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    assert args.name and all(c.isalnum() or c in '-_' for c in args.name)
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    assert command and Path(command[0]).resolve() == Path(sys.executable).resolve()
    script_paths = [Path(x).resolve() for x in command[1:] if x.endswith('.py')]
    assert len(script_paths) == 1 and script_paths[0].is_relative_to(BASE / 'scripts')
    run = BASE / 'runs' / args.name
    run.mkdir(parents=True, exist_ok=False)
    (run / 'supervisor.pid').write_text(str(os.getpid()) + '\n')
    start = time.perf_counter()
    stage_limit = int(os.environ.get('T032_STAGE_BYTES_MAX', '0'))
    stage_baseline = size_tree(BASE)
    child = None
    peak = 0
    state = {'status':'STARTING', 'supervisor_pid':os.getpid(), 'command':command,
             'cwd':str(BASE), 'python':sys.executable,
             'local_bytes_reserved':args.local_bytes, 'budget_new_bytes':8 * 2**30,
             'max_wall_s':args.max_wall_s, 'stage_byte_limit':stage_limit,
             'stage_baseline_bytes':stage_baseline,
             'limits_note':'operating limits only; no RCA threshold or numerical tolerance changed',
             'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    def save(event):
        state.update(elapsed_s=time.perf_counter()-start, peak_tree_rss_bytes=peak,
                     updated_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        temp = run / 'status.tmp'
        temp.write_text(json.dumps(state, indent=2) + '\n')
        temp.replace(run / 'status.json')
        with (run / 'progress.jsonl').open('a') as stream:
            stream.write(json.dumps({'event':event, **state}) + '\n')
        print(state['updated_utc'], event, state['status'], round(state['elapsed_s'], 1), flush=True)
    def terminate():
        if child is not None and child.poll() is None:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
    def on_signal(number, frame):
        raise RuntimeError('supervisor received signal ' + str(number))
    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    try:
        remote_bytes = size_tree(BASE)
        assert remote_bytes + args.local_bytes < 8 * 2**30, 'new-byte budget already exceeded'
        with (run / 'stdout.txt').open('w') as out, (run / 'stderr.txt').open('w') as err:
            child = subprocess.Popen(command, cwd=BASE, stdout=out, stderr=err,
                                     env=dict(os.environ), start_new_session=True)
            (run / 'worker.pid').write_text(str(child.pid) + '\n')
            state.update(status='RUNNING', worker_pid=child.pid)
            save('START')
            last_disk_check = 0
            while child.poll() is None:
                try:
                    proc = psutil.Process(child.pid)
                    rss = sum(p.memory_info().rss for p in [proc] + proc.children(recursive=True)
                              if p.is_running())
                    peak = max(peak, rss)
                except psutil.NoSuchProcess:
                    pass
                elapsed = time.perf_counter()-start
                if stage_limit:
                    current_bytes = size_tree(BASE)
                    state['stage_measured_new_bytes'] = current_bytes - stage_baseline
                    if current_bytes - stage_baseline >= stage_limit:
                        raise RuntimeError('approved stage new-byte limit reached; polling may overshoot, retain and stop')
                if elapsed > args.max_wall_s:
                    raise RuntimeError('approved stage wall budget exceeded; checkpoint and stop')
                if (BASE / ('STOP-' + args.name)).exists():
                    raise RuntimeError('task stop marker requested')
                if elapsed-last_disk_check >= 10 or last_disk_check == 0:
                    remote_bytes = size_tree(BASE)
                    free = psutil.disk_usage(str(BASE)).free
                    available = psutil.virtual_memory().available
                    state.update(remote_task_bytes=remote_bytes, free_disk_bytes=free,
                                 available_ram_bytes=available)
                    if remote_bytes + args.local_bytes >= 8 * 2**30:
                        raise RuntimeError('8 GiB combined new-byte budget reached')
                    if free < 512 * 2**20 or available < 256 * 2**20:
                        raise RuntimeError('insufficient remaining disk/RAM; stop before exhaustion')
                    last_disk_check = elapsed
                    save('POLL')
                time.sleep(1)
        if stage_limit and size_tree(BASE) - stage_baseline >= stage_limit:
            raise RuntimeError('approved stage new-byte limit reached at finish; retain and stop')
        state.update(status='PASS' if child.returncode == 0 else 'FAIL', exit_code=child.returncode,
                     remote_task_bytes=size_tree(BASE))
        save('FINISH')
        return child.returncode
    except BaseException as exc:
        terminate()
        state.update(status='STOPPED', error=str(exc), traceback=traceback.format_exc(),
                     exit_code=None if child is None else child.returncode)
        save('STOP')
        return 1

if __name__ == '__main__':
    sys.exit(main())
