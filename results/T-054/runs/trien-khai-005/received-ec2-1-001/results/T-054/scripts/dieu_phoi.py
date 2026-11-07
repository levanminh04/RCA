"""Một supervisor, partition cố định, worker độc lập phiên agent/SSH."""
import contextlib
import json
import math
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

from bien_nhan import (Blocked, ROOT, OUT, append, atomic, canonical, events, iter_events, fingerprint,
                       read_pin, ref, timeout_classification, verify_envelope)


@contextlib.contextmanager
def exclusive(path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    stream = p.open('a+b')
    if os.fstat(stream.fileno()).st_size == 0:
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
    jobs = {}
    last = sample = wait = controller = None
    for row in iter_events(directory / 'events.jsonl'):
        last = row
        if row.get('state') == 'SUPERVISOR':
            wait = None
            controller = row.get('identity')
        if row.get('state') == 'SUPERVISOR_STOPPED':
            controller = None
        if str(row.get('state', '')).startswith('WAIT_'):
            wait = row
        if 'job_id' in row and 'state' in row:
            jobs[row['job_id']] = row
    for sample in iter_events(directory / 'resources.jsonl'):
        pass
    counts = {}
    for row in jobs.values():
        counts[row['state']] = counts.get(row['state'], 0) + 1
    return {'jobs': jobs, 'counts': counts, 'last_event': last, 'last_monitor': sample, 'wait': wait, 'controller': controller,
            'warning': 'Heartbeat cũ không xác minh process đã dừng; dùng resume để đối chiếu PID/token.'}


class BudgetStop(Blocked):
    pass


def budget_group(job):
    return job['slot']['dataset'] + '|' + job['slot']['arm']


def _positive(value):
    return type(value) in (float, int) and math.isfinite(value) and value > 0


def check_budget(plan):
    budget = plan.get('budget')
    if budget is None and plan['mode'] == 'synthetic':
        return
    if isinstance(budget, dict) and budget.get('mode') == 'UNTIL_COHORT_COMPLETE':
        decision = read_pin(budget['decision_ref'])
        if (decision.get('status') != 'USER_CONFIRMED' or budget.get('wall_s') is not None
                or budget.get('method_dataset_s') != {} or not decision.get('budget', {}).get('rule', '').startswith('no fixed cumulative cap')):
            raise Blocked('chính sách không trần thiếu nguồn Minh hoặc có trần ẩn')
        return
    if (not isinstance(budget, dict) or not _positive(budget.get('wall_s'))
            or not isinstance(budget.get('method_dataset_s'), dict)):
        raise Blocked('WAIT_POLICY_BUDGET: thiếu trần thời gian bằng số')
    groups = {budget_group(j) for j in plan['jobs']}
    caps = budget['method_dataset_s']
    if any(not _positive(v) for v in caps.values()) or (plan['mode'] != 'synthetic' and set(caps) != groups):
        raise Blocked('WAIT_POLICY_BUDGET: thiếu/sai trần method×dataset')


def open_budget(plan, directory):
    """Ngân sách dùng lại mốc bắt đầu/cost đã đóng, không reset khi resume."""
    check_budget(plan)
    if plan.get('budget') is None:
        return None
    import psutil
    path = directory / 'budget-start.json'
    if path.exists():
        start = read_pin(ref(path))
        if start['plan_sha256'] != fingerprint(plan):
            raise Blocked('budget cũ không cùng plan')
    else:
        start = {'plan_sha256': fingerprint(plan), 'started_epoch': time.time(),
                 'started_monotonic': time.monotonic(), 'boot_time': psutil.boot_time()}
        atomic(path, start)
    used = {}
    for cost in directory.glob('*/attempt-*/cost.json'):
        row = read_pin(ref(cost))
        group = row['budget_group']
        used[group] = used.get(group, 0) + row['wall_s']
    return {'policy': plan['budget'], 'start': start, 'used': used}


def budget_limits(budget, job, launch_record):
    if budget is None:
        return {}
    import psutil
    start = budget['start']; limits = {}
    same_boot = start['boot_time'] == psutil.boot_time()
    if budget['policy'].get('mode') == 'UNTIL_COHORT_COMPLETE':
        return {}
    limits['whole_run'] = {'epoch': start['started_epoch'] + budget['policy']['wall_s']}
    if same_boot:
        limits['whole_run']['monotonic'] = start['started_monotonic'] + budget['policy']['wall_s']
    group = budget_group(job)
    cap = budget['policy']['method_dataset_s'].get(group)
    if cap is not None:
        remaining = cap - budget['used'].get(group, 0)
        limits['method_dataset'] = {'epoch': launch_record['started_epoch'] + remaining}
        if launch_record.get('boot_time') == psutil.boot_time():
            limits['method_dataset']['monotonic'] = launch_record['started_monotonic'] + remaining
    return limits


def exhausted(limits):
    for name, limit in limits.items():
        if time.time() >= limit['epoch'] or ('monotonic' in limit and time.monotonic() >= limit['monotonic']):
            return name
    return None


def close_cost(attempt, job, budget):
    import psutil
    path = attempt / 'cost.json'
    if path.exists():
        return
    launch_record = read_pin(ref(attempt / 'launch.json'))
    elapsed = max(0, time.time() - launch_record['started_epoch'])
    if launch_record['boot_time'] == psutil.boot_time():
        elapsed = max(elapsed, time.monotonic() - launch_record['started_monotonic'])
    row = {'budget_group': budget_group(job), 'wall_s': elapsed,
           'job_sha256': fingerprint(job), 'token': launch_record['token']}
    atomic(path, row)
    if budget is not None:
        g = row['budget_group']; budget['used'][g] = budget['used'].get(g, 0) + elapsed


def launch_record(token, timeout_s):
    import psutil
    return {'token': token, 'started_epoch': time.time(), 'started_monotonic': time.monotonic(),
            'deadline_epoch': time.time() + timeout_s, 'boot_time': psutil.boot_time()}


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


def saved_identity(attempt):
    actual = attempt / 'actual-process.json'
    return read_pin(ref(actual if actual.exists() else attempt / 'identity.json'))


def bind_actual_process(attempt, token, launcher, phases):
    """Windows venv launcher có thể khác PID của Python thật ghi pha."""
    import psutil
    path = attempt / 'actual-process.json'
    if path.exists():
        actual = read_pin(ref(path))
        if actual['token'] != token:
            raise Blocked('actual-process khác token')
        return actual
    ids = {p['pid'] for p in phases if p.get('token') == token and p.get('pid')}
    if not ids:
        return launcher
    if len(ids) != 1:
        raise Blocked('pha cùng lượt có nhiều PID, chưa xác minh chủ')
    pid, = ids
    if pid == launcher['pid']:
        return launcher
    try:
        proc = psutil.Process(pid)
        actual = identity(pid, token)
        parents = {p.pid for p in proc.parents()}
        if launcher['pid'] not in parents or token not in proc.cmdline() or actual['created'] < launcher['created']:
            raise Blocked('PID pha không phải worker con của launcher')
        atomic(path, actual)
        return actual
    except psutil.NoSuchProcess:
        # Worker có thể đã đóng output trước lần poll đầu. Không nhận PID khác thay nó.
        return launcher


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
        return subprocess.Popen([executable, '-B', *args], stdin=subprocess.DEVNULL,
                                stdout=out, stderr=err, env=env, **options)


def _monitor(attempt, token, ident, deadline, policy, before=None, limits=None, resources=None):
    import psutil
    samples = events(attempt / 'monitor.jsonl')
    gap = max((r['max_monitor_gap_s'] for r in samples), default=0)
    peak = max((r.get('peak_tree_rss', 0) for r in samples), default=0)
    previous = time.monotonic(); previous_wall = time.time(); sample = None
    clock_anomaly = any(r.get('clock_anomaly') for r in samples)
    # Khoảng mất quan sát khi controller restart tính từ clock wall đã lưu; không lấp bằng heartbeat mới.
    if samples:
        gap = max(gap, max(0, time.time() - samples[-1]['wall_clock']))
    while alive(ident):
        now = time.monotonic()
        wall = time.time()
        clock_anomaly = clock_anomaly or abs((wall - previous_wall) - (now - previous)) > policy['max_monitor_gap_s']
        gap = max(gap, now - previous)
        previous = now; previous_wall = wall
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
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        phases = events(attempt / 'phases.jsonl')
        ident = bind_actual_process(attempt, token, ident, phases)
        sample = {'token': token, 'wall_clock': time.time(), 'max_monitor_gap_s': gap,
                  'peak_tree_rss': peak, 'tree_rss': rss, 'tree_cpu_s': cpu,
                  'tree_read_bytes': read_bytes, 'tree_write_bytes': write_bytes,
                  'free_disk': psutil.disk_usage(str(attempt)).free,
                  'host_available_ram': memory.available, 'host_swap_used': swap.used,
                  'host_swap_in': swap.sin, 'host_swap_out': swap.sout,
                  'last_phase_sha256': fingerprint(phases[-1]) if phases else None,
                  'phase': phases[-1].get('phase') if phases else None, 'pid': ident['pid'],
                  'clock_anomaly': clock_anomaly, 'poll_s': policy['poll_s']}
        append(attempt / 'monitor.jsonl', sample)
        append(resources or attempt.parent.parent / 'resources.jsonl', sample)
        budget_reason = exhausted(limits or {})
        if budget_reason:
            sample['budget_exhausted'] = budget_reason
            atomic(attempt / 'budget-stop.json', sample)
            terminate_tree(ident['pid'])
            return True, sample
        if time.time() >= deadline:
            # Ghi bằng chứng trước khi kill, không suy pha từ chuỗi lỗi.
            sample['deadline_observed_epoch'] = time.time()
            sample['max_monitor_gap_s'] = max(gap, time.monotonic() - previous)
            atomic(attempt / 'timeout.json', sample)
            terminate_tree(ident['pid'])
            return True, sample
        time.sleep(policy['poll_s'])
    sample = sample or (samples[-1] if samples else {'token': token, 'max_monitor_gap_s': gap})
    return False, sample


def verify_attempt(attempt, job, token):
    envelope = read_pin(ref(attempt / 'result.json'))
    invocation = read_pin(ref(attempt / 'invocation.json'))
    records = verify_envelope(envelope, invocation, job['slot'], token)
    from nguon import validate_execution_links
    validate_execution_links(job, invocation)
    if job['kind'] != 'synthetic' or job.get('fixture_route') or job.get('pipeline_fixture'):
        sys.path.insert(0, str(ROOT / 'src'))
        from p3 import danh_gia
        s = job['slot']
        family = s['arm'] in ('M1', 'bo-E1', 'bo-E2', 'bo-E5', 'C-a0', 'C-a1', 'T12-on')
        expected_method = 'M1' if family else 'torai' if s['arm'] in ('torai_A', 'torai_B') else s['arm']
        expected_variants = ([s['arm']] if family else ['ols+rht_da', 'ols+rht']
                              if s['arm'] == 'circa' and s['dataset'] == 'RE2-TT' else
                              [{'baro': 'native', 'simplerca': 'M4', 'microrank': 'full', 'C-d3': 'cd3',
                                'tracerca': 'finite', 'circa': 'ols+rht_da', 'torai_B': 'B', 'torai_A': 'A'}[s['arm']]])
        if [r.get('variant') for r in records] != expected_variants:
            raise Blocked('variant thiếu/sai/thừa so với slot')
        for record in records:
            if s['arm'] == 'circa' and s['dataset'] == 'RE2-TT' and record.get('status') == 'OK':
                current = record.get('diagnostics', {}).get('circa_current')
                if type(current) is not int or record.get('window', {}).get('circa_current') != current:
                    raise Blocked('CIRCA thiếu/sai mốc current thực dùng trong window')
            if record.get('method') != expected_method or record.get('mode') != 'a' or record.get('seed') != s['seed']:
                raise Blocked('method/mode/seed thực chạy khác slot')
            if family and record.get('config_id') != s['arm']:
                raise Blocked('M1 sai config_id')
            if record['status'] == 'OK':
                views = [record['worlds'][w] for w in ('P', 'S_lo', 'S_hi')] if family else [record]
                if any(not danh_gia.khoi_tu_ban_ghi(v) for v in views):
                    raise Blocked('record OK không có thứ hạng hợp lệ')
    if any(r.get('status') in ('ERROR', 'TIMEOUT') for r in records):
        failure = attempt / 'method-failure.json'
        if failure.is_file():
            from bien_nhan import verify_method_failure
            verify_method_failure(ref(failure), job, envelope, invocation)
            return records
        from bien_nhan import verify_dev_error_reproduction
        path = attempt / 'dev-error-reproduction.json'
        if not path.is_file():
            raise Blocked('lỗi phương pháp cần phân loại với bằng chứng, chưa tự tính trượt')
        verify_dev_error_reproduction(ref(path), job, envelope, invocation)
    return records


def resolve_dependency(job, jobs_by_slot, current, directory):
    if not job.get('main_dependency'):
        return job
    from nguon import main_dependency_record
    dep = job['main_dependency']; parent_id = fingerprint(dep['slot'])
    parent_job = jobs_by_slot.get(parent_id); state = current.get(parent_id)
    if (parent_job is None or fingerprint(parent_job) != dep['job_sha256'] or not state
            or state['state'] != 'VERIFIED'):
        raise Blocked('WAIT_MAIN_SEAL: dependency chưa VERIFIED hoặc khác plan')
    receipt = read_pin(state['receipt'])
    if receipt['job_sha256'] != dep['job_sha256']:
        raise Blocked('parent receipt khác job khai trước')
    record, = verify_attempt(Path(state['attempt']), parent_job, state['token'])
    key = '|'.join(str(dep['slot'][k]) for k in ('dataset', 'opaque_id', 'arm', 'view', 'seed'))
    doc = {'schema': 'T054-MAIN-SEAL-2', 'parent_slot_sha256': parent_id,
           'parent_job_sha256': dep['job_sha256'], 'producer_receipt': state['receipt'], 'records': {key: record}}
    path = directory / 'seals' / (parent_id + '.json')
    if path.exists():
        pin = ref(path)
        if read_pin(pin) != doc:
            raise Blocked('main seal cũ khác producer')
    else:
        pin = atomic(path, doc)
    main_dependency_record(job, pin)
    return dict(job, main_seal=pin, main_key=key)


def pipeline(job, attempt, token, deadline, policy, limits=None, resources=None):
    """Prep và py38 có identity/deadline riêng; restart không lặp prep đã đóng."""
    stage_jobs = [('prepare', dict(job, kind='torai_prep'), job['prep_executable']),
                  ('method', dict(job, kind='torai_run'), job['method_executable'])]
    for name, item, executable in stage_jobs:
        if job.get('pipeline_fixture'):
            if job['kind'] != 'synthetic':
                raise Blocked('pipeline_fixture chỉ cho plan tổng hợp')
            item['fixture_route'] = item['kind']
            item['kind'] = 'synthetic'
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
                from bien_nhan import finalize_error
                finalize_error(stage, job)
                verify_attempt(stage, job, token)
            continue
        if name == 'method':
            item['prepared'] = ref(attempt / 'prepare/prepared.json')
            # Môi trường method py38 được ghim riêng; invocation cuối giữ environment của slot method.
        if stage.exists():
            if not (stage / 'identity.json').exists():
                raise Blocked('stage chưa biết chủ, giữ attempt')
            ident = saved_identity(stage)
            if not alive(ident):
                raise Blocked('stage chết chưa đóng output, không tự retry')
        else:
            stage.mkdir()
            atomic(stage / 'job.json', item)
            os.link(attempt / 'launch.json', stage / 'launch.json')
            p = launch(executable, [str(OUT / 'scripts/worker.py'), str(stage / 'job.json'), str(stage), token],
                       stage / 'stdout.txt', stage / 'stderr.txt')
            ident = identity(p.pid, token)
            atomic(stage / 'identity.json', ident)
        timed_out, sample = _monitor(stage, token, ident, deadline, policy, limits=limits, resources=resources)
        if timed_out:
            if sample.get('budget_exhausted'):
                raise BudgetStop(sample['budget_exhausted'])
            if name == 'method' and job.get('failure_policy_ref'):
                from bien_nhan import finalize_timeout
                finalize_timeout(stage, job, token)
                continue
            classified = timeout_classification(job['slot'], events(stage / 'phases.jsonl'), sample, policy)
            raise Blocked('TORAI ' + name + ' timeout: ' + classified[1])
        if not expected_output.exists():
            raise Blocked('TORAI ' + name + ' worker chưa đóng output')
        if name == 'method':
            from bien_nhan import finalize_error
            finalize_error(stage, job)
    for name in ('result.json', 'invocation.json', 'method-failure.json'):
        dest = attempt / name
        if not dest.exists() and (attempt / 'method' / name).exists():
            os.link(attempt / 'method' / name, dest)
    verify_attempt(attempt, job, token)


def _run_one(job, plan, directory, budget, old_jobs, jobs_by_slot, emit):
    """Một slot, không retry; scheduler giữ độc quyền nhóm method×dataset."""
    job_id = fingerprint(job['slot'])
    old = old_jobs.get(job_id)
    if old is None:
        candidate = directory / job_id / 'attempt-001'
        if candidate.exists():
            try:
                saved_job = read_pin(ref(candidate / 'job.json'))
                saved_launch = read_pin(ref(candidate / 'launch.json'))
                if fingerprint(saved_job) != fingerprint(job):
                    raise Blocked('attempt cũ không cùng job')
                old = {'state': 'RUNNING', 'attempt': str(candidate), 'token': saved_launch['token']}
                emit(dict(old, job_id=job_id, action='RECOVER_ATTEMPT_METADATA'))
            except (Blocked, OSError, ValueError, KeyError) as exc:
                emit({'job_id': job_id, 'state': 'BLOCKED', 'reason': 'ATTEMPT_OWNER_UNKNOWN:' + str(exc)})
                return False
    if old and old['state'] == 'VERIFIED':
        attempt = Path(old['attempt'])
        records = verify_attempt(attempt, job, old['token'])
        sealed = read_pin(old['receipt'])
        if sealed['result'] != ref(attempt / 'result.json') or sealed['invocation'] != ref(attempt / 'invocation.json'):
            raise Blocked('VERIFIED file bị đổi sau receipt')
        return False
    if old and old['state'] in ('BLOCKED', 'FAILED_OPERATIONAL'):
        return False  # không tự thử lại bằng chứng lỗi chưa phân xử
    if not old:
        controls = events(directory / 'control.jsonl')
        if controls and controls[-1]['action'] == 'DRAIN':
            return True
        limits = budget_limits(budget, job, launch_record('preflight', job['timeout_s']))
        reason = exhausted(limits)
        if reason:
            emit({'state': 'WAIT_BUDGET', 'reason': reason, 'next_job_id': job_id})
            return True
    try:
        execution = resolve_dependency(job, jobs_by_slot, old_jobs, directory)
    except (Blocked, OSError, KeyError, ValueError) as exc:
        emit({'job_id': job_id, 'state': 'BLOCKED', 'reason': str(exc)})
        return False
    if job['kind'] == 'torai_pipeline' or (job['kind'] == 'synthetic' and job.get('pipeline_fixture')):
        if old:
            attempt, token = Path(old['attempt']), old['token']
            deadline = read_pin(ref(attempt / 'launch.json'))['deadline_epoch']
        else:
            token = uuid.uuid4().hex
            attempt = directory / job_id / 'attempt-001'
            attempt.mkdir(parents=True, exist_ok=False)
            deadline = time.time() + job['timeout_s']
            atomic(attempt / 'job.json', job)
            started = launch_record(token, job['timeout_s']); deadline = started['deadline_epoch']
            atomic(attempt / 'launch.json', started)
        emit(dict(job_id=job_id, state='RUNNING', attempt=str(attempt), token=token))
        limits = budget_limits(budget, job, read_pin(ref(attempt / 'launch.json')))
        try:
            pipeline(job, attempt, token, deadline, plan['monitor'], limits=limits, resources=directory / 'resources.jsonl')
            receipt = ref(attempt / 'verified.json') if (attempt / 'verified.json').exists() else atomic(attempt / 'verified.json', {'job_sha256': fingerprint(job),
                             'result': ref(attempt / 'result.json'), 'invocation': ref(attempt / 'invocation.json'),
                             **({'method_failure': ref(attempt / 'method-failure.json')}
                                if (attempt / 'method-failure.json').exists() else {})})
            close_cost(attempt, job, budget)
            emit(dict(job_id=job_id, state='VERIFIED', attempt=str(attempt), token=token, receipt=receipt))
        except BudgetStop as exc:
            close_cost(attempt, job, budget)
            emit(dict(job_id=job_id, state='BLOCKED', attempt=str(attempt), token=token, reason='BUDGET:' + str(exc)))
            emit({'state': 'WAIT_BUDGET', 'reason': str(exc)})
            return True
        except (Blocked, OSError, ValueError) as exc:
            close_cost(attempt, job, budget)
            emit(dict(job_id=job_id, state='BLOCKED', attempt=str(attempt), token=token, reason=str(exc)))
        return False
    if old:
        attempt = Path(old['attempt']); token = old['token']
        if not (attempt / 'identity.json').is_file():
            emit(dict(job_id=job_id, state='BLOCKED', reason='PROCESS_OWNER_UNKNOWN', attempt=str(attempt), token=token)); return False
        ident = saved_identity(attempt)
        if not alive(ident) and not (attempt / 'result.json').exists():
            emit(dict(job_id=job_id, state='BLOCKED', reason='DEAD_PARTIAL_RETAINED', attempt=str(attempt), token=token)); return False
        emit(dict(job_id=job_id, state='RUNNING', action='ADOPT', attempt=str(attempt), token=token))
        deadline = read_pin(ref(attempt / 'launch.json'))['deadline_epoch']
    else:
        token = uuid.uuid4().hex
        attempt = directory / job_id / 'attempt-001'
        attempt.mkdir(parents=True, exist_ok=False)
        atomic(attempt / 'job.json', job)
        started = launch_record(token, job['timeout_s']); deadline = started['deadline_epoch']
        atomic(attempt / 'launch.json', started)
        emit(dict(job_id=job_id, state='RUNNING', attempt=str(attempt), token=token))
        execution_path = attempt / 'job.json'
        if execution != job:
            execution_path = attempt / 'execution-job.json'
            atomic(execution_path, execution)
        p = launch(job['executable'], [str(OUT / 'scripts/worker.py'), str(execution_path), str(attempt), token],
                   attempt / 'stdout.txt', attempt / 'stderr.txt')
        try:
            ident = identity(p.pid, token)
            atomic(attempt / 'identity.json', ident)
        except Exception:
            terminate_tree(p.pid)
            raise
    limits = budget_limits(budget, job, read_pin(ref(attempt / 'launch.json')))
    timed_out, monitor = _monitor(attempt, token, ident, deadline, plan['monitor'], limits=limits)
    close_cost(attempt, job, budget)
    if timed_out:
        if monitor.get('budget_exhausted'):
            emit(dict(job_id=job_id, state='BLOCKED', reason='BUDGET:' + monitor['budget_exhausted'], attempt=str(attempt), token=token))
            emit({'state': 'WAIT_BUDGET', 'reason': monitor['budget_exhausted']})
            return True
        state, reason = timeout_classification(job['slot'], events(attempt / 'phases.jsonl'), monitor, plan['monitor'])
        try:
            from bien_nhan import finalize_timeout
            if not job.get('failure_policy_ref'):
                raise Blocked(reason)
            finalize_timeout(attempt, job, token)
        except (Blocked, OSError, ValueError, KeyError) as exc:
            emit(dict(job_id=job_id, state='BLOCKED', reason=str(exc), phase_state=state, attempt=str(attempt), token=token))
            return False
    try:
        emit(dict(job_id=job_id, state='COMPLETE_UNVERIFIED', attempt=str(attempt), token=token))
        from bien_nhan import finalize_error
        finalize_error(attempt, job)
        verify_attempt(attempt, job, token)
        receipt_path = attempt / 'verified.json'
        if receipt_path.exists():
            receipt = ref(receipt_path)
        else:
            receipt = atomic(receipt_path, {'result': ref(attempt / 'result.json'),
                             'invocation': ref(attempt / 'invocation.json'), 'job_sha256': fingerprint(job),
                             **({'method_failure': ref(attempt / 'method-failure.json')}
                                if (attempt / 'method-failure.json').exists() else {})})
        emit(dict(job_id=job_id, state='VERIFIED', attempt=str(attempt), token=token, receipt=receipt))
    except (Blocked, OSError, ValueError, KeyError) as exc:
        emit(dict(job_id=job_id, state='BLOCKED', reason=str(exc), attempt=str(attempt), token=token))
    return False


def supervise(plan, directory):
    """Một supervisor; tối đa hai worker. Plan bất biến quyết số worker."""
    import threading
    from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
    count = plan.get('workers', 1)
    if type(count) is not int or count not in (1, 2):
        raise Blocked('workers phải là 1 hoặc 2, khai trong plan')
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with exclusive(directory / 'supervisor.lock'):
        budget = open_budget(plan, directory)
        journal = directory / 'events.jsonl'
        append(directory / 'control.jsonl', {'action': 'RESUME'})
        append(journal, {'state': 'SUPERVISOR', 'pid': os.getpid(), 'plan_sha256': fingerprint(plan),
                         'workers': count, 'identity': identity(os.getpid(), 'supervisor')})
        current = status(directory)['jobs']
        jobs_by_slot = {fingerprint(j['slot']): j for j in plan['jobs']}
        lock = threading.Lock()
        def emit(row):
            with lock:
                append(journal, dict(row, wall_clock=time.time()))
                if 'job_id' in row and 'state' in row:
                    current[row['job_id']] = row
        # Lượt đang sống được nhận trước lượt mới; không tăng số worker khi resume.
        pending = sorted(plan['jobs'], key=lambda j: 0 if current.get(fingerprint(j['slot']), {}).get('state')
                         in ('RUNNING', 'COMPLETE_UNVERIFIED') else 1)
        active = {}; groups = set(); stop = False
        try:
            with ThreadPoolExecutor(max_workers=count) as pool:
                while pending or active:
                    controls = events(directory / 'control.jsonl')
                    if controls and controls[-1]['action'] == 'DRAIN':
                        stop = True
                    if not stop:
                        for job in list(pending):
                            if len(active) >= count:
                                break
                            group = budget_group(job)
                            if group in groups:
                                continue
                            dep = job.get('main_dependency')
                            if dep:
                                parent = fingerprint(dep['slot'])
                                parent_state = current.get(parent, {}).get('state')
                                if parent_state not in ('VERIFIED', 'BLOCKED', 'FAILED_OPERATIONAL'):
                                    continue
                            pending.remove(job); groups.add(group)
                            future = pool.submit(_run_one, job, plan, directory, budget, current, jobs_by_slot, emit)
                            active[future] = (group, fingerprint(job['slot']))
                    if not active:
                        if stop or not pending:
                            break
                        raise Blocked('dependency không có producer có thể thực hiện')
                    done, _ = wait(active, timeout=0.2, return_when=FIRST_COMPLETED)
                    for future in done:
                        group, job_id = active.pop(future)
                        groups.remove(group)
                        requested_stop = future.result()
                        if current.get(job_id, {}).get('state') in ('BLOCKED', 'FAILED_OPERATIONAL'):
                            emit({'state': 'WAIT_ERROR', 'blocked_job_id': job_id,
                                  'reason': current[job_id].get('reason')})
                            requested_stop = True
                        if requested_stop:
                            stop = True
        finally:
            append(journal, {'state': 'SUPERVISOR_STOPPED', 'pid': os.getpid(), 'wall_clock': time.time()})
