"""Một supervisor, partition cố định, worker độc lập phiên agent/SSH."""
import contextlib
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

from bien_nhan import (Blocked, ROOT, OUT, append, atomic, canonical, events, fingerprint,
                       read_pin, ref, timeout_classification, verify_envelope)


@contextlib.contextmanager
def exclusive(path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    stream = p.open('a+b')
    stream.seek(0)
    if not stream.read(1):
        stream.write(b'0'); stream.flush()
    stream.seek(0)
    try:
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        stream.close()
        raise Blocked('supervisor/partition đang có chủ') from exc
    try:
        yield
    finally:
        stream.close()


def status(directory):
    directory = Path(directory)
    rows = events(directory / 'events.jsonl')
    jobs = {}
    for row in rows:
        if 'job_id' in row and 'state' in row:
            jobs[row['job_id']] = row
    samples = events(directory / 'resources.jsonl')
    return {'jobs': jobs, 'last_event': rows[-1] if rows else None,
            'last_monitor': samples[-1] if samples else None,
            'warning': 'Heartbeat cũ không xác minh process đã dừng; dùng resume để đối chiếu PID/token.'}


def identity(pid, token):
    import psutil
    p = psutil.Process(pid)
    return {'pid': pid, 'created': p.create_time(), 'command_sha256': fingerprint(p.cmdline()), 'token': token}


def alive(ident):
    import psutil
    try:
        return identity(ident['pid'], ident['token']) == ident and ident['token'] in psutil.Process(ident['pid']).cmdline()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def terminate_tree(pid):
    import psutil
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try: child.kill()
            except psutil.NoSuchProcess: pass
        parent.kill()
        psutil.wait_procs(children + [parent], timeout=10)
    except psutil.NoSuchProcess:
        pass


def launch(executable, args, stdout, stderr):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8',
               PYTHONHASHSEED='0', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    options = {'creationflags': subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}
    with Path(stdout).open('ab') as out, Path(stderr).open('ab') as err:
        return subprocess.Popen([executable, '-B', *args], stdout=out, stderr=err, env=env, **options)


def _monitor(attempt, token, ident, deadline, policy, before=None):
    import psutil
    samples = events(attempt / 'monitor.jsonl')
    gap = max((r['max_monitor_gap_s'] for r in samples), default=0)
    peak = max((r.get('peak_tree_rss', 0) for r in samples), default=0)
    previous = time.monotonic()
    # Khoảng mất quan sát khi controller restart tính từ clock wall đã lưu; không lấp bằng heartbeat mới.
    if samples:
        gap = max(gap, max(0, time.time() - samples[-1]['wall_clock']))
    while alive(ident):
        now = time.monotonic()
        gap = max(gap, now - previous)
        previous = now
        rss = read_bytes = write_bytes = 0
        cpu = 0.0
        try:
            p = psutil.Process(ident['pid'])
            for q in [p, *p.children(recursive=True)]:
                try:
                    rss += q.memory_info().rss
                    cpu += sum(q.cpu_times()[:2])
                    io = q.io_counters(); read_bytes += io.read_bytes; write_bytes += io.write_bytes
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except psutil.NoSuchProcess:
            pass
        peak = max(peak, rss)
        phases = events(attempt / 'phases.jsonl')
        sample = {'token': token, 'wall_clock': time.time(), 'max_monitor_gap_s': gap,
                  'peak_tree_rss': peak, 'tree_rss': rss, 'tree_cpu_s': cpu,
                  'tree_read_bytes': read_bytes, 'tree_write_bytes': write_bytes,
                  'free_disk': psutil.disk_usage(str(attempt)).free,
                  'last_phase_sha256': fingerprint(phases[-1]) if phases else None}
        append(attempt / 'monitor.jsonl', sample)
        append(attempt.parent.parent / 'resources.jsonl', sample)
        if time.time() >= deadline:
            # Ghi bằng chứng trước khi kill, không suy pha từ chuỗi lỗi.
            atomic(attempt / 'timeout.json', sample)
            terminate_tree(ident['pid'])
            return True, sample
        time.sleep(policy['poll_s'])
    sample = samples[-1] if samples else {'token': token, 'max_monitor_gap_s': gap}
    return False, sample


def verify_attempt(attempt, job, token):
    envelope = read_pin(ref(attempt / 'result.json'))
    invocation = read_pin(ref(attempt / 'invocation.json'))
    records = verify_envelope(envelope, invocation, job['slot'], token)
    if job['kind'] == 'torai_pipeline':
        prep = read_pin(invocation['prepared_ref'])
        if prep['token'] != token or prep['slot_sha256'] != fingerprint(job['slot']):
            raise Blocked('TORAI method không cùng prep đã xử lý')
        from worker import read_pin_path
        for pin in prep['tables'].values():
            read_pin_path(pin)
    if job['kind'] != 'synthetic' or job.get('fixture_route'):
        sys.path.insert(0, str(ROOT / 'src'))
        from p3 import danh_gia
        s = job['slot']
        family = s['arm'] in ('M1', 'bo-E1', 'bo-E2', 'bo-E5', 'C-a0', 'C-a1', 'T12-on')
        expected_method = 'M1' if family else 'torai' if s['arm'] == 'torai_B' else s['arm']
        expected_variants = ([s['arm']] if family else ['ols+rht_da', 'ols+rht']
                              if s['arm'] == 'circa' and s['dataset'] == 'RE2-TT' else
                              [{'baro': 'native', 'simplerca': 'M4', 'microrank': 'full', 'C-d3': 'cd3',
                                'tracerca': 'finite', 'circa': 'ols+rht_da', 'torai_B': 'B'}[s['arm']]])
        if [r.get('variant') for r in records] != expected_variants:
            raise Blocked('variant thiếu/sai/thừa so với slot')
        for record in records:
            if record.get('method') != expected_method or record.get('mode') != 'a' or record.get('seed') != s['seed']:
                raise Blocked('method/mode/seed thực chạy khác slot')
            if family and record.get('config_id') != s['arm']:
                raise Blocked('M1 sai config_id')
            if record['status'] == 'OK':
                views = [record['worlds'][w] for w in ('P', 'S_lo', 'S_hi')] if family else [record]
                if any(not danh_gia.khoi_tu_ban_ghi(v) for v in views):
                    raise Blocked('record OK không có thứ hạng hợp lệ')
    if any(r.get('status') in ('ERROR', 'TIMEOUT') for r in records):
        raise Blocked('lỗi phương pháp cần phân loại với bằng chứng, chưa tự tính trượt')
    return records


def pipeline(job, attempt, token, deadline, policy):
    """Prep và py38 có identity/deadline riêng; restart không lặp prep đã đóng."""
    stage_jobs = [('prepare', dict(job, kind='torai_prep'), job['prep_executable']),
                  ('method', dict(job, kind='torai_run'), job['method_executable'])]
    for name, item, executable in stage_jobs:
        stage = attempt / name
        expected_output = stage / ('prepared.json' if name == 'prepare' else 'result.json')
        if expected_output.exists():
            if name == 'prepare':
                prep = read_pin(ref(expected_output))
                if prep['slot_sha256'] != fingerprint(job['slot']) or prep['token'] != token:
                    raise Blocked('prep cũ không cùng lượt')
                from worker import read_pin_path
                for pin in prep['tables'].values(): read_pin_path(pin)
            else:
                verify_attempt(stage, job, token)
            continue
        if name == 'method':
            item['prepared'] = ref(attempt / 'prepare/prepared.json')
            # Môi trường method py38 được ghim riêng; invocation cuối giữ environment của slot method.
        if stage.exists():
            if not (stage / 'identity.json').exists():
                raise Blocked('stage chưa biết chủ, giữ attempt')
            ident = read_pin(ref(stage / 'identity.json'))
            if not alive(ident):
                raise Blocked('stage chết chưa đóng output, không tự retry')
        else:
            stage.mkdir()
            atomic(stage / 'job.json', item)
            p = launch(executable, [str(OUT / 'scripts/worker.py'), str(stage / 'job.json'), str(stage), token],
                       stage / 'stdout.txt', stage / 'stderr.txt')
            ident = identity(p.pid, token)
            atomic(stage / 'identity.json', ident)
        timed_out, sample = _monitor(stage, token, ident, deadline, policy)
        if timed_out:
            classified = timeout_classification(job['slot'], events(stage / 'phases.jsonl'), sample, policy)
            raise Blocked('TORAI ' + name + ' timeout: ' + classified[1])
        if not expected_output.exists():
            raise Blocked('TORAI ' + name + ' worker chưa đóng output')
    for name in ('result.json', 'invocation.json'):
        dest = attempt / name
        if not dest.exists():
            os.link(attempt / 'method' / name, dest)
    verify_attempt(attempt, job, token)


def supervise(plan, directory):
    """Plan đã kiểm pin/quyền trước hàm này. Không auto retry khi chính sách chưa duyệt."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with exclusive(directory / 'supervisor.lock'):
        journal = directory / 'events.jsonl'
        append(directory / 'control.jsonl', {'action': 'RESUME'})
        append(journal, {'state': 'SUPERVISOR', 'pid': os.getpid(), 'plan_sha256': fingerprint(plan)})
        for job in plan['jobs']:
            job_id = fingerprint(job['slot'])
            old = status(directory)['jobs'].get(job_id)
            if old and old['state'] == 'VERIFIED':
                attempt = Path(old['attempt'])
                records = verify_attempt(attempt, job, old['token'])
                sealed = read_pin(old['receipt'])
                if sealed['result'] != ref(attempt / 'result.json') or sealed['invocation'] != ref(attempt / 'invocation.json'):
                    raise Blocked('VERIFIED file bị đổi sau receipt')
                continue
            if old and old['state'] in ('BLOCKED', 'FAILED_OPERATIONAL'):
                continue  # không tự thử lại bằng chứng lỗi chưa phân xử
            if job['kind'] == 'torai_pipeline':
                if old:
                    attempt, token = Path(old['attempt']), old['token']
                    deadline = read_pin(ref(attempt / 'launch.json'))['deadline_epoch']
                else:
                    token = uuid.uuid4().hex
                    attempt = directory / job_id / 'attempt-001'
                    attempt.mkdir(parents=True, exist_ok=False)
                    deadline = time.time() + job['timeout_s']
                    atomic(attempt / 'job.json', job)
                    atomic(attempt / 'launch.json', {'token': token, 'deadline_epoch': deadline})
                append(journal, dict(job_id=job_id, state='RUNNING', attempt=str(attempt), token=token))
                try:
                    pipeline(job, attempt, token, deadline, plan['monitor'])
                    receipt = atomic(attempt / 'verified.json', {'job_sha256': fingerprint(job),
                                     'result': ref(attempt / 'result.json'), 'invocation': ref(attempt / 'invocation.json')})
                    append(journal, dict(job_id=job_id, state='VERIFIED', attempt=str(attempt), token=token, receipt=receipt))
                except (Blocked, OSError, ValueError) as exc:
                    append(journal, dict(job_id=job_id, state='BLOCKED', attempt=str(attempt), token=token, reason=str(exc)))
                continue
            if old:
                attempt = Path(old['attempt']); token = old['token']
                if not (attempt / 'identity.json').is_file():
                    append(journal, dict(job_id=job_id, state='BLOCKED', reason='PROCESS_OWNER_UNKNOWN', attempt=str(attempt), token=token)); continue
                ident = read_pin(ref(attempt / 'identity.json'))
                if not alive(ident) and not (attempt / 'result.json').exists():
                    append(journal, dict(job_id=job_id, state='BLOCKED', reason='DEAD_PARTIAL_RETAINED', attempt=str(attempt), token=token)); continue
                append(journal, dict(job_id=job_id, state='RUNNING', action='ADOPT', attempt=str(attempt), token=token))
                deadline = read_pin(ref(attempt / 'launch.json'))['deadline_epoch']
            else:
                controls = events(directory / 'control.jsonl')
                if controls and controls[-1]['action'] == 'DRAIN':
                    break
                token = uuid.uuid4().hex
                attempt = directory / job_id / 'attempt-001'
                attempt.mkdir(parents=True, exist_ok=False)
                atomic(attempt / 'job.json', job)
                deadline = time.time() + job['timeout_s']
                atomic(attempt / 'launch.json', {'deadline_epoch': deadline, 'token': token})
                append(journal, dict(job_id=job_id, state='RUNNING', attempt=str(attempt), token=token))
                p = launch(job['executable'], [str(OUT / 'scripts/worker.py'), str(attempt / 'job.json'), str(attempt), token],
                           attempt / 'stdout.txt', attempt / 'stderr.txt')
                try:
                    ident = identity(p.pid, token)
                    atomic(attempt / 'identity.json', ident)
                except Exception:
                    terminate_tree(p.pid)
                    raise
            timed_out, monitor = _monitor(attempt, token, ident, deadline, plan['monitor'])
            if timed_out:
                state, reason = timeout_classification(job['slot'], events(attempt / 'phases.jsonl'), monitor, plan['monitor'])
                # COMPLETE_UNVERIFIED chỉ đủ bằng chứng pha; đóng TIMEOUT khoa học còn cần policy/grant.
                append(journal, dict(job_id=job_id, state='BLOCKED', reason=reason, phase_state=state, attempt=str(attempt), token=token))
                continue
            try:
                append(journal, dict(job_id=job_id, state='COMPLETE_UNVERIFIED', attempt=str(attempt), token=token))
                verify_attempt(attempt, job, token)
                receipt_path = attempt / 'verified.json'
                if receipt_path.exists():
                    receipt = ref(receipt_path)
                else:
                    receipt = atomic(receipt_path, {'result': ref(attempt / 'result.json'),
                                     'invocation': ref(attempt / 'invocation.json'), 'job_sha256': fingerprint(job)})
                append(journal, dict(job_id=job_id, state='VERIFIED', attempt=str(attempt), token=token, receipt=receipt))
            except (Blocked, OSError, ValueError, KeyError) as exc:
                append(journal, dict(job_id=job_id, state='BLOCKED', reason=str(exc), attempt=str(attempt), token=token))
        append(journal, {'state': 'SUPERVISOR_STOPPED', 'pid': os.getpid()})
