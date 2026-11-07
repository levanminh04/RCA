"""I/O bền và liên kết lượt thực chạy; không cấp quyền dữ liệu."""
import hashlib
import json
import math
import os
import time
from contextlib import contextmanager
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-054'
_RECEIVE_PATHS = {}


def receive_paths(mapping):
    """Lớp nhận đọc bản sao đã kiểm hash, không sửa path trong receipt/envelope gốc."""
    global _RECEIVE_PATHS
    checked = {}
    for origin, target in mapping.items():
        destination = Path(target).resolve()
        if not destination.is_relative_to(ROOT.resolve()) or not origin.startswith('/'):
            raise Blocked('ánh xạ nhận ngoài repo hoặc nguồn không tuyệt đối')
        checked[origin.rstrip('/')] = destination
    _RECEIVE_PATHS = checked


def resolve_path(path):
    value = str(path).replace('\\', '/')
    for origin in sorted(_RECEIVE_PATHS, key=len, reverse=True):
        if value == origin or value.startswith(origin + '/'):
            suffix = value[len(origin):].lstrip('/')
            result = (_RECEIVE_PATHS[origin] / suffix).resolve()
            if not result.is_relative_to(_RECEIVE_PATHS[origin]):
                raise Blocked('path nhận vượt thư mục đã khai')
            return result
    return Path(path)


class Blocked(ValueError):
    pass


class UnclassifiedMethodError(Blocked):
    """v2: lỗi phương pháp có output hợp lệ nhưng chưa có quy tắc; chỉ chặn slot này và slot phụ thuộc."""


class DependencyBlocked(Blocked):
    """v2: slot phụ thuộc vào slot đã BLOCKED vì lỗi phương pháp chưa phân loại."""


def utc():
    return datetime.now(timezone.utc).isoformat()


def encode(x):
    if isinstance(x, Fraction):
        return {'phan_so': [x.numerator, x.denominator]}
    if type(x).__module__.startswith('numpy') and hasattr(x, 'tolist'):
        return encode(x.tolist())
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    return x


def canonical(x):
    return json.dumps(encode(x), sort_keys=True, ensure_ascii=False,
                      allow_nan=False, separators=(',', ':')).encode('utf-8')


def fingerprint(x):
    return hashlib.sha256(canonical(x)).hexdigest()


def digest(path):
    with Path(path).open('rb') as f:
        h = hashlib.sha256()
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
        return h.hexdigest()


def ref(path):
    p = Path(path).resolve()
    return {'path': str(p), 'sha256': digest(p), 'bytes': p.stat().st_size}


def read_pin(pin):
    p = resolve_path(pin['path'])
    if not p.is_absolute():
        p = ROOT / p
    raw = p.read_bytes()
    if (hashlib.sha256(raw).hexdigest() != pin['sha256'] or
            ('bytes' in pin and len(raw) != pin['bytes'])):
        raise Blocked('file khác pin: ' + str(p))
    return json.loads(raw)


def atomic(path, value):
    """Không ghi đè: hard-link commit nguyên tử từ file đã flush/fsync."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    temp = p.with_name(p.name + '.partial-' + str(os.getpid()))
    with temp.open('xb') as f:
        f.write(canonical(value) + b'\n')
        f.flush()
        os.fsync(f.fileno())
    os.link(temp, p)  # đích tồn tại => giữ cả bản cũ và partial, báo lỗi
    temp.unlink()
    return ref(p)


@contextmanager
def journal_lock(path):
    """Khóa OS cho một lần nối, kể cả khi CLI và supervisor cùng ghi control."""
    stream = Path(path).open('a+b')
    if os.fstat(stream.fileno()).st_size == 0:
        stream.write(b'0'); stream.flush()
    started = time.monotonic()
    try:
        while True:
            stream.seek(0)
            try:
                if os.name == 'nt':
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() - started > 2:
                    raise Blocked('journal đang được ghi, chưa xác minh chủ')
                time.sleep(.01)
        yield
    finally:
        stream.close()


def append(path, value):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with journal_lock(p.with_name(p.name + '.lock')):
        # Giữ byte dở trước khi cắt phần chưa commit. Không nối JSON mới vào đuôi JSON dở.
        with p.open('a+b', buffering=0) as f:
            end = f.seek(0, os.SEEK_END)
            if end:
                f.seek(-1, os.SEEK_END)
                if f.read(1) != b'\n':
                    f.seek(0); raw = f.read()
                    prefix = raw.rfind(b'\n') + 1
                    tail = raw[prefix:]
                    sha = hashlib.sha256(tail).hexdigest()
                    saved = p.with_name(p.name + '.torn-' + sha + '.bin')
                    if saved.exists():
                        if saved.read_bytes() != tail:
                            raise Blocked('bản byte dở không khớp')
                    else:
                        with saved.open('xb') as archive:
                            archive.write(tail); archive.flush(); os.fsync(archive.fileno())
                    f.seek(prefix); f.truncate(); os.fsync(f.fileno())
                    recovery = {'utc': utc(), 'event': 'JOURNAL_TAIL_PRESERVED',
                                'valid_prefix_bytes': prefix, 'tail_sha256': sha, 'tail_bytes': len(tail),
                                'archive': saved.name}
                    f.write(canonical(recovery) + b'\n'); os.fsync(f.fileno())
            f.write(canonical(dict(utc=utc(), **value)) + b'\n')
            os.fsync(f.fileno())


def iter_events(path):
    p = Path(path)
    if not p.exists():
        return
    with p.open('rb') as f:
        for line in f:
            if not line.endswith(b'\n'):
                return  # Chỉ đọc: không sửa đuôi chưa commit.
            try:
                yield json.loads(line)
            except ValueError as exc:
                raise Blocked('event hỏng giữa lịch sử')


def events(path):
    return list(iter_events(path))


def no_labels(value):
    if isinstance(value, dict):
        if set(value) & {'root', 'fault', 'cell', 'labels', 'ground_truth', 'nhan', 'answer'}:
            raise Blocked('nhãn trong đầu vào phương pháp')
        for v in value.values():
            no_labels(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            no_labels(v)


def normalized_digest(value):
    """Dấu vân tay tại API, bao schema/thứ tự/dtype; ghim phiên bản pandas/numpy."""
    h = hashlib.sha256()

    def walk(x):
        if type(x).__module__.startswith('pandas') and hasattr(x, 'columns'):
            import pandas as pd
            h.update(canonical({'columns': list(x.columns), 'dtypes': [str(v) for v in x.dtypes]}))
            h.update(pd.util.hash_pandas_object(x, index=True).to_numpy().tobytes())
        elif isinstance(x, dict):
            h.update(b'{')
            for k in sorted(x):
                h.update(canonical(k)); walk(x[k])
            h.update(b'}')
        elif isinstance(x, (list, tuple)):
            h.update(b'[')
            for v in x:
                walk(v); h.update(b',')
            h.update(b']')
        elif hasattr(x, 'dtype') and hasattr(x, 'tobytes'):
            h.update(canonical([str(x.dtype), list(x.shape)])); h.update(x.tobytes())
        elif isinstance(x, float) and not math.isfinite(x):
            h.update(canonical({'nonfinite': str(x)}))
        else:
            h.update(canonical(x))
    walk(value)
    return h.hexdigest()


def verify_envelope(envelope, invocation, slot, token):
    expected = {'slot_sha256': fingerprint(slot), 'token': token}
    if envelope.get('schema') != 'T054-RESULT-1' or invocation.get('schema') != 'T054-INVOKE-1':
        raise Blocked('sai schema lượt thực chạy')
    for k, v in expected.items():
        if envelope.get(k) != v or invocation.get(k) != v:
            raise Blocked('tráo token hoặc slot trước khi gắn ca')
    if envelope.get('invocation_sha256') != fingerprint(invocation):
        raise Blocked('kết quả không cùng invocation')
    if envelope.get('record_sha256') != fingerprint(envelope.get('records')):
        raise Blocked('kết quả khác hash')
    if invocation.get('config_sha256') != slot['config_sha256']:
        raise Blocked('config thực chạy khác slot')
    for name in ('source_sha256', 'window', 'seed', 'environment_sha256'):
        if invocation.get(name) != slot.get(name):
            raise Blocked('liên kết thực chạy khác slot: ' + name)
    if not isinstance(invocation.get('normalized_input_sha256'), str) or len(invocation['normalized_input_sha256']) != 64:
        raise Blocked('thiếu dấu vân tay đầu vào đã xử lý')
    no_labels(envelope)
    return envelope['records']


def timeout_classification(slot, phase_events, monitor, policy):
    """Không nhận lời tự gán method của một bản review làm bằng chứng."""
    threshold = policy.get('max_monitor_gap_s')
    gap = monitor.get('max_monitor_gap_s')
    if threshold is None or gap is None or not gap < threshold:
        return 'BLOCKED', 'MONITOR_GAP_OR_POLICY_UNKNOWN'
    own = [e for e in phase_events if e.get('token') == monitor.get('token')]
    if (not own or own[-1].get('phase') != 'method' or own[-1].get('state') != 'start'
            or not own[-1].get('invocation_sha256') or monitor.get('last_phase_sha256') != fingerprint(own[-1])):
        return 'BLOCKED', 'NO_DURABLE_METHOD_START'
    if 'method' not in policy.get('score_phases', []):
        return 'BLOCKED', 'METHOD_TIMEOUT_POLICY_OPEN'
    return 'COMPLETE_UNVERIFIED', 'DECLARED_METHOD_TIMEOUT'


def verify_dev_error_reproduction(pin, job, envelope, invocation):
    """Chỉ ERROR dev đã tái hiện đúng baseline gốc và có audit code/đầu vào.

    Không cấp chính sách lỗi test/TIMEOUT; các trường hợp đó vẫn BLOCKED.
    """
    c = read_pin(pin)
    if (job.get('evaluation_mode') != 'dev' or c.get('scope') != 'DEV_BASELINE_REPRODUCTION_ONLY'
            or c.get('job_sha256') != fingerprint(job)
            or c.get('result_sha256') != fingerprint(envelope)
            or c.get('invocation_sha256') != fingerprint(invocation)):
        raise Blocked('phân loại lỗi dev không cùng job/output/phạm vi')
    old = read_pin(c['baseline_reference'])
    record, = envelope['records']
    if (record.get('status') != 'ERROR' or old.get('status') != 'ERROR'
            or old.get('opaque_id') != job['slot']['opaque_id']):
        raise Blocked('không suy giấy tái hiện ERROR sang TIMEOUT/lỗi khác')
    for key in ('method', 'mode', 'seed', 'status', 'error', 'window', 'blocks', 'entity_ranking', 'ranking_native', 'observed_entities'):
        if old.get(key) != record.get(key):
            raise Blocked('ERROR dev khác bản gốc: ' + key)
    if c.get('origin') != 'method_implementation_assumption':
        raise Blocked('chưa phân xử nguồn lỗi')
    from nguon import compare_sources
    compare_sources(read_pin(job['runtime_ref']), read_pin(job['independent_source_ref']),
                    job['slot']['dataset'], job['g1_revision'])
    audit = read_pin(c['input_audit'])
    arm = job['slot']['arm']
    if (arm not in ('microrank', 'tracerca') or audit['t'] != job['t']
            or audit['trace_sha256'] != job['source']['files']['traces.parquet']['sha256']
            or audit['normal_count'][arm] != 0 or audit['anomalous_count'][arm] <= 0):
        raise Blocked('thiếu bằng chứng operation mới tại đầu vào hợp lệ')
    if len(c.get('code_evidence', [])) < 2:
        raise Blocked('thiếu code method và adapter ánh xạ lỗi')
    for item in c['code_evidence']:
        path = Path(item['path'])
        if not path.is_absolute():
            path = ROOT / path
        if digest(path) != item['sha256']:
            raise Blocked('code phân loại lỗi thay đổi')
    return c


def failure_policy(job):
    policy = read_pin(job['failure_policy_ref'])
    if policy.get('schema') != 'T054-FAILURE-POLICY-1':
        raise Blocked('chính sách lỗi sai schema')
    if job.get('evaluation_mode') == 'test' and policy.get('scope') != 'LOCKED_P7':
        raise Blocked('chính sách lỗi chưa khóa trước test')
    for pin in policy.get('code_evidence', []):
        path = Path(pin['path'])
        if not path.is_absolute():
            path = ROOT / path
        if digest(path) != pin['sha256']:
            raise Blocked('code phân loại khác bản khóa')
    return policy


def known_operation_error(job, envelope, invocation):
    """Xác minh cơ chế operation mới trên đầu vào thật, không chỉ đọc chuỗi lỗi."""
    policy = failure_policy(job)
    arm = job['slot']['arm']
    if (job['slot']['dataset'] != 'RE2-TT' or arm not in ('microrank', 'tracerca')
            or 'NEW_OPERATION_WITHOUT_NORMAL_BASELINE' not in policy.get('error_rules', [])
            or len(policy.get('code_evidence', [])) < 4):
        raise UnclassifiedMethodError('ERROR chưa có quy tắc phù hợp; giữ BLOCKED để điều tra')
    record, = envelope['records']
    if record.get('status') != 'ERROR':
        raise Blocked('quy tắc operation chỉ nhận ERROR')
    import sys
    sys.path.insert(0, str(ROOT / 'src'))
    from nguon import source_row, compare_sources
    from p3 import worker, cua_so
    compare_sources(read_pin(job['runtime_ref']), read_pin(job['independent_source_ref']),
                    job['slot']['dataset'], job['g1_revision'])
    paths = source_row(job['source'], job['data_root'])
    raw = {key: worker._doc_parquet(paths, name) for key, name in
           [('metric', 'metrics.parquet'), ('traces', 'traces.parquet')]}
    raw['logs'] = None  # Hai adapter này không đọc log ở worker thật.
    win, _ = cua_so.cat_ca(raw['metric'], raw['traces'], raw['logs'], job['t'])
    if normalized_digest([win, job['t']]) != invocation['normalized_input_sha256']:
        raise Blocked('audit lỗi khác normalized input thực chạy')
    df = win['traces'].copy()
    df['methodName'] = df['methodName'].fillna(df['operationName'])
    ops = df['serviceName'] + '_' + df['methodName']
    before = df['startTime'] + df['duration'] < job['t'] * 1_000_000
    new = sorted(set(ops[~before]) - set(ops[before]))
    error = record.get('error')
    valid = (error == 'ValueError: No normal baseline for: ' + ','.join(new) if arm == 'microrank'
             else any(error == 'KeyError: ' + repr(op) for op in new))
    # v2 (Minh duyệt 07/11/2026): dưới 2 span bình thường, kiểm lại từ đầu vào thật.
    counts = ops[before].value_counts()
    single_normal = sorted(str(op) for op, n in counts.items() if int(n) == 1)
    single_after = sorted(set(single_normal) & set(map(str, ops[~before])))
    if arm == 'microrank':
        low = (not new and bool(single_after) and error == 'ValueError: Normal std undefined (<2 spans)')
        low_ops = single_after
    else:
        low = bool(single_normal) and error == "TypeError: type NAType doesn't define __round__ method"
        low_ops = single_normal
    if low and 'INSUFFICIENT_NORMAL_SPANS' in policy.get('error_rules', []):
        return {'rule': 'INSUFFICIENT_NORMAL_SPANS', 'single_normal_span_operations': low_ops,
                'new_operations': new, 'normal_spans': {op: int(counts[op]) for op in low_ops},
                'anomalous_spans': {op: int(((ops == op) & ~before).sum()) for op in low_ops}}
    if not new or not valid:
        raise UnclassifiedMethodError('ERROR không khớp cơ chế đã khóa và operation thực')
    return {'rule': 'NEW_OPERATION_WITHOUT_NORMAL_BASELINE', 'new_operations': new,
            'normal_spans': {op: int(((ops == op) & before).sum()) for op in new},
            'anomalous_spans': {op: int(((ops == op) & ~before).sum()) for op in new}}


def verify_method_failure(pin, job, envelope, invocation):
    c = read_pin(pin)
    policy = failure_policy(job)
    if (c.get('schema') != 'T054-METHOD-FAILURE-1' or c.get('job_sha256') != fingerprint(job)
            or c.get('result_sha256') != fingerprint(envelope)
            or c.get('invocation_sha256') != fingerprint(invocation)
            or c.get('policy') != job['failure_policy_ref']):
        raise Blocked('phân loại lỗi không cùng job/output/policy')
    if c.get('kind') == 'ERROR':
        if c['audit'] != known_operation_error(job, envelope, invocation):
            raise Blocked('audit lỗi khác bằng chứng nguồn')
    elif c.get('kind') == 'TIMEOUT':
        phases = read_pin(c['phases'])
        monitor = read_pin(c['monitor'])
        launch = read_pin(c['launch'])
        state, reason = timeout_classification(job['slot'], phases, monitor, policy['monitor'])
        if (state != 'COMPLETE_UNVERIFIED' or reason != 'DECLARED_METHOD_TIMEOUT'
                or launch['token'] != envelope['token'] or monitor['token'] != envelope['token']
                or monitor.get('budget_exhausted') or monitor.get('clock_anomaly')
                or monitor.get('poll_s') != policy['monitor']['poll_s']
                or monitor.get('deadline_observed_epoch', monitor['wall_clock']) < launch['deadline_epoch']
                or phases[-1]['invocation_sha256'] != fingerprint(invocation)
                or any(r.get('status') != 'TIMEOUT' for r in envelope['records'])):
            raise Blocked('TIMEOUT thiếu bằng chứng method/clock/đầu vào')
    else:
        raise Blocked('loại lỗi chưa khai')
    return c


def finalize_error(attempt, job):
    """Controller phân loại trước verify; các lệnh kiểm/đọc không tạo receipt."""
    attempt = Path(attempt)
    if (attempt / 'method-failure.json').exists() or not job.get('failure_policy_ref'):
        return
    envelope = read_pin(ref(attempt / 'result.json'))
    if not any(r.get('status') == 'ERROR' for r in envelope['records']):
        return
    invocation = read_pin(ref(attempt / 'invocation.json'))
    audit = known_operation_error(job, envelope, invocation)
    c = dict(schema='T054-METHOD-FAILURE-1', kind='ERROR', job_sha256=fingerprint(job),
             result_sha256=fingerprint(envelope), invocation_sha256=fingerprint(invocation),
             policy=job['failure_policy_ref'], audit=audit)
    atomic(attempt / 'method-failure.json', c)


def finalize_timeout(attempt, job, token):
    """Chỉ đóng TIMEOUT sau giám sát/kill; prep và mất quan sát vẫn BLOCKED."""
    attempt = Path(attempt)
    policy = failure_policy(job)
    phases = events(attempt / 'phases.jsonl')
    monitor = read_pin(ref(attempt / 'timeout.json'))
    state, _ = timeout_classification(job['slot'], phases, monitor, policy['monitor'])
    if state != 'COMPLETE_UNVERIFIED' or monitor.get('clock_anomaly'):
        raise Blocked('timeout ngoài pha method hoặc mất quan sát')
    invocation = read_pin(ref(attempt / 'invocation.json'))
    s = job['slot']; arm = s['arm']
    family = arm in ('M1', 'bo-E1', 'bo-E2', 'bo-E5', 'C-a0', 'C-a1', 'T12-on')
    variants = ([arm] if family else ['ols+rht_da', 'ols+rht'] if arm == 'circa' and s['dataset'] in ('RE2-TT', 'RE3-OB')
                else [{'baro': 'native', 'simplerca': 'M4', 'microrank': 'full', 'tracerca': 'finite',
                       'circa': 'ols+rht_da', 'torai_A': 'A', 'torai_B': 'B', 'C-d3': 'cd3'}[arm]])
    method = 'M1' if family else 'torai' if arm.startswith('torai_') else arm
    records = [dict(method=method, variant=v, mode='a', seed=s['seed'], status='TIMEOUT',
                    config_id=arm, blocks=[], error='DECLARED_METHOD_TIMEOUT') for v in variants]
    envelope = dict(schema='T054-RESULT-1', token=token, slot_sha256=fingerprint(s),
                    invocation_sha256=fingerprint(invocation), records=records, record_sha256=fingerprint(records))
    # Giữ mọi output hoàn tất nếu có cuộc đua tại deadline; không ghi đè rồi tự chấm.
    if (attempt / 'result.json').exists():
        raise Blocked('output đã đóng tại deadline; cần phân xử, không ghi đè')
    c = dict(schema='T054-METHOD-FAILURE-1', kind='TIMEOUT', job_sha256=fingerprint(job),
             result_sha256=fingerprint(envelope), invocation_sha256=fingerprint(invocation),
             policy=job['failure_policy_ref'], phases=atomic(attempt / 'timeout-phases.json', phases),
             monitor=ref(attempt / 'timeout.json'), launch=ref(attempt / 'launch.json'))
    pin = atomic(attempt / 'method-failure.json', c)
    verify_method_failure(pin, job, envelope, invocation)
    atomic(attempt / 'result.json', envelope)
    return pin
