"""I/O bền và liên kết lượt thực chạy; không cấp quyền dữ liệu."""
import hashlib
import json
import math
import os
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-054'


class Blocked(ValueError):
    pass


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
    p = Path(pin['path'])
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


def append(path, value):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('ab', buffering=0) as f:
        f.write(canonical(dict(utc=utc(), **value)) + b'\n')
        os.fsync(f.fileno())


def events(path):
    p = Path(path)
    if not p.exists():
        return []
    result = []
    lines = p.read_bytes().splitlines(keepends=True)
    for i, line in enumerate(lines):
        try:
            if not line.endswith(b'\n'):
                raise ValueError('event dở')
            result.append(json.loads(line))
        except ValueError:
            if i != len(lines) - 1:
                raise Blocked('event hỏng giữa lịch sử')
            break
    return result


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
