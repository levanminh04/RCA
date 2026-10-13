"""Đầu vào Nezha-OB đã duyệt cho T-026; chỉ runner đọc locator.

Không import phương pháp. CSV được quét timestamp trước, chỉ chuyển giá trị của
cửa sổ được phép. Payload ở RAM, timestamp gốc ns và các hàng lặp được giữ.
"""
import calendar
import csv
import json
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath

import numpy as np
import pandas as pd

from .selector import LoiRunner, sha256_file

NS = 1_000_000_000
DATA_PREFIX = ('data', 'ngoai-rcaeval', 'nezha', 'online-boutique', 'rca_data')
MA_MO = re.compile(r'^dev-[0-9a-f]{10}$')
TIME_RE = re.compile(
    r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.(\d{1,9}) '
    r'\+0000 UTC m=[+-]\d+(?:\.\d+)?$')
LOG_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})\.(\d{1,9})Z$')
POD_ALIASES = {
    'adservice-5f6585d649-fnmft': 'adservice',
    'cartservice-579f59597d-wc2lz': 'cartservice',
    'checkoutservice-578fcf4766-9csqn': 'checkoutservice',
    'currencyservice-cf787dd48-vpjrd': 'currencyservice',
    'emailservice-55fdc5b988-f6xth': 'emailservice',
    'frontend-579b9bff58-t2dbm': 'frontend',
    'paymentservice-9cdb6588f-554sm': 'paymentservice',
    'productcatalogservice-668d5f85fb-wckp8': 'productcatalogservice',
    'productcatalogservice-668d5f85fb-jhwx9': 'productcatalogservice',
    'recommendationservice-6cfdd55578-gfj6q': 'recommendationservice',
    'shippingservice-7b598fc7d-lmggd': 'shippingservice',
}
ALIASES = POD_ALIASES
SERVICE_ALIASES = {'Frontend': 'frontend'}
UNIVERSE = sorted(set(POD_ALIASES.values()))
RESOURCE_CHANNELS = {
    'CpuUsage(m)': 'CpuUsage-m',
    'CpuUsageRate(%)': 'CpuUsageRate-pct',
    'MemoryUsage(Mi)': 'MemoryUsage-Mi',
    'MemoryUsageRate(%)': 'MemoryUsageRate-pct',
    'SyscallRead': 'SyscallRead',
    'SyscallWrite': 'SyscallWrite',
    'NetworkReceiveBytes': 'NetworkReceiveBytes',
    'NetworkTransmitBytes': 'NetworkTransmitBytes',
    'PodClientLatencyP90(s)': 'PodClientLatencyP90-s',
    'PodServerLatencyP90(s)': 'PodServerLatencyP90-s',
    'PodClientLatencyP95(s)': 'PodClientLatencyP95-s',
    'PodServerLatencyP95(s)': 'PodServerLatencyP95-s',
    'PodClientLatencyP99(s)': 'PodClientLatencyP99-s',
    'PodServerLatencyP99(s)': 'PodServerLatencyP99-s',
    'PodWorkload(Ops)': 'PodWorkload-Ops',
    'PodSuccessRate(%)': 'PodSuccessRate-pct',
}
FRONT_CHANNELS = {
    'SuccessRate(%)': 'FrontSuccessRate-pct',
    'LatencyP50(s)': 'FrontLatencyP50-s',
    'LatencyP90(s)': 'FrontLatencyP90-s',
    'LatencyP95(s)': 'FrontLatencyP95-s',
    'LatencyP99(s)': 'FrontLatencyP99-s',
}
SPAN_COLUMNS = ['traceID', 'spanID', 'parentSpanID', 'serviceName', 'methodName',
                'operationName', 'startTime', 'duration', '_start_ns', '_end_ns']
LOG_COLUMNS = ['timestamp', 'container_name', 'message', '_timestamp_ns']
FORBIDDEN_LABEL_KEYS = {'case', 'root', 'fault', 'fault_type', 'cell', 'nhom_loi',
                        'nhom_vi_tri_p75', 'labels', 'ground_truth'}


def _integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise LoiRunner(f'{name}: cần số nguyên')
    return value


def parse_time_ns(value):
    """Parse toàn bộ Time UTC, giữ 1–9 chữ số phần lẻ; không dùng TimeStamp."""
    m = TIME_RE.fullmatch(value or '')
    if not m:
        raise LoiRunner('Time: định dạng UTC/phần lẻ không hợp lệ')
    try:
        wall, frac = m.groups()
        seconds = calendar.timegm(datetime.strptime(wall, '%Y-%m-%d %H:%M:%S').timetuple())
    except ValueError as exc:
        raise LoiRunner('Time: ngày giờ không hợp lệ') from exc
    return seconds * NS + int(frac.ljust(9, '0'))


def _log_time_ns(value):
    m = LOG_RE.fullmatch(value or '')
    if not m:
        raise LoiRunner('Timestamp log: cần RFC3339 UTC/phần lẻ')
    day, wall, frac = m.groups()
    seconds = calendar.timegm(datetime.strptime(day + ' ' + wall, '%Y-%m-%d %H:%M:%S').timetuple())
    return seconds * NS + int(frac.ljust(9, '0'))


def _relative_path(rel):
    if not isinstance(rel, str) or not rel or '\\' in rel or rel.startswith('/'):
        raise LoiRunner('Nezha: locator phải là đường dẫn POSIX tương đối')
    if re.match(r'^[A-Za-z]:', rel) or any(p in ('', '.', '..') for p in rel.split('/')):
        raise LoiRunner('Nezha: locator có traversal hoặc đường dẫn tuyệt đối')
    p = PurePosixPath(rel)
    if p.parts[:len(DATA_PREFIX)] != DATA_PREFIX or len(p.parts) != len(DATA_PREFIX) + 3:
        raise LoiRunner('Nezha: locator ngoài OB rca_data được phép')
    day, kind, name = p.parts[-3:]
    if day not in ('2022-08-22', '2022-08-23') or kind not in ('metric', 'trace', 'log'):
        raise LoiRunner('Nezha: ngày/nguồn ngoài phạm vi')
    if kind == 'metric':
        allowed = {'front_service.csv'} | {pod + '_metric.csv' for pod in POD_ALIASES}
        if name not in allowed:
            raise LoiRunner('Nezha: nguồn metric ngoài 11 nguồn Time')
    elif not re.fullmatch(r'\d{2}_\d{2}_' + kind + r'\.csv', name):
        raise LoiRunner('Nezha: tên minute-file không hợp lệ')
    return p


def _validate_case(case):
    def no_labels(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in FORBIDDEN_LABEL_KEYS:
                    raise LoiRunner('Nezha allowlist: chứa nhãn bị cấm')
                no_labels(value)
        elif isinstance(obj, list):
            for value in obj:
                no_labels(value)
    no_labels(case)
    if not isinstance(case, dict) or not MA_MO.fullmatch(str(case.get('opaque_id', ''))):
        raise LoiRunner('Nezha: mã mờ không hợp lệ')
    t = _integer(case.get('t_ns'), 't_ns')
    if t % NS:
        raise LoiRunner('Nezha: mốc tiêm phải là giây nguyên')
    alternate = case.get('t_ns_sensitivity_A')
    if alternate is not None and _integer(alternate, 't_ns_sensitivity_A') % NS:
        raise LoiRunner('Nezha: mốc độ nhạy A không nguyên giây')
    guard = _integer(case.get('trace_guard_s'), 'trace_guard_s')
    files = case.get('files')
    if not isinstance(files, dict) or not files:
        raise LoiRunner('Nezha: manifest nguồn rỗng')
    days = set()
    for key, meta in files.items():
        if not isinstance(meta, dict) or key != meta.get('path'):
            raise LoiRunner('Nezha: khóa manifest không khớp path')
        p = _relative_path(key)
        days.add(p.parts[-3])
        if not re.fullmatch(r'[0-9a-f]{64}', str(meta.get('sha256', ''))):
            raise LoiRunner('Nezha: SHA-256 không hợp lệ')
        if _integer(meta.get('bytes'), 'bytes') <= 0:
            raise LoiRunner('Nezha: kích thước nguồn không hợp lệ')
    if len(days) != 1 or guard != {'2022-08-22': 41, '2022-08-23': 32}[next(iter(days))]:
        raise LoiRunner('Nezha: trace guard không khớp ngày nguồn')
    return case


def nap_allowlist(path):
    """Đọc manifest, không đọc dữ liệu hoặc nhãn; trả dict mã mờ → metadata."""
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise LoiRunner('Nezha allowlist: khóa JSON trùng')
            out[key] = value
        return out
    with open(path, encoding='utf-8') as f:
        doc = json.load(f, object_pairs_hook=unique)
    cases = doc.get('cases')
    if doc.get('dataset') != 'Nezha-OB' or not isinstance(cases, list) or doc.get('so_ca') != len(cases):
        raise LoiRunner('Nezha allowlist: dataset/số ca không hợp lệ')
    out = {}
    for case in cases:
        _validate_case(case)
        oid = case['opaque_id']
        if oid in out:
            raise LoiRunner('Nezha allowlist: mã mờ trùng')
        out[oid] = case
    return out


def chon_ca(allowlist, opaque_id, repo_root, view='main'):
    """Từ chối mã ngoài allowlist trước resolve/stat/hash/data I/O."""
    if not isinstance(opaque_id, str) or not MA_MO.fullmatch(opaque_id) or opaque_id not in allowlist:
        raise LoiRunner('Nezha: ca không thuộc allowlist dev')
    if view not in ('main', 'sensitivity_a', 'sensitivity_A'):
        raise LoiRunner('Nezha: view không hợp lệ')
    case = _validate_case(allowlist[opaque_id])
    # Kiểm mọi locator bằng chuỗi trước bất kỳ I/O dữ liệu nào.
    relative = {key: _relative_path(meta['path']) for key, meta in case['files'].items()}
    root = Path(repo_root).resolve()
    base = root.joinpath(*DATA_PREFIX).resolve()
    selected = {}
    for key, p in relative.items():
        meta = case['files'][key]
        full = root.joinpath(*p.parts).resolve()
        if not full.is_relative_to(base):
            raise LoiRunner('Nezha: locator thoát khỏi rca_data sau resolve')
        if not full.is_file() or full.stat().st_size != meta['bytes']:
            raise LoiRunner('Nezha: nguồn vắng hoặc kích thước đổi')
        if sha256_file(full) != meta['sha256']:
            raise LoiRunner('Nezha: SHA-256 nguồn không khớp')
        selected[key] = dict(meta, absolute_path=str(full))
    actual_view = 'main' if view == 'main' else 'sensitivity_A'
    alternate = case.get('t_ns_sensitivity_A')
    t_ns = case['t_ns'] if actual_view == 'main' or alternate is None else alternate
    return {'opaque_id': opaque_id, 'view': actual_view, 't_ns': t_ns,
            'trace_guard_s': case['trace_guard_s'], 'files': selected,
            'universe': list(UNIVERSE), 'aliases': dict(POD_ALIASES)}


def _open_source(meta):
    path = Path(meta['absolute_path'])
    if path.stat().st_size != meta['bytes'] or sha256_file(path) != meta['sha256']:
        raise LoiRunner('Nezha: nguồn đổi giữa selection và đọc cửa sổ')
    return path.open(encoding='utf-8-sig', newline='')


def _schema(reader, needed, kind):
    if reader.fieldnames is None or set(needed) - set(reader.fieldnames):
        raise LoiRunner(f'Nezha: thiếu cột {kind}')
    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise LoiRunner(f'Nezha: cột {kind} trùng')


def _stats(times, t):
    def side(values):
        return {'rows': len(values), 'seconds_with_rows': len({x // NS for x in values}),
                'first_ns': min(values) if values else None, 'last_ns': max(values) if values else None,
                'hull_s': (max(values) - min(values)) / NS if values else 0.0}
    return {'N': side([x for x in times if x < t]), 'A': side([x for x in times if x >= t])}


def _numeric(value):
    if value is None or not value.strip():
        return float('nan')
    try:
        return float(value)
    except ValueError as exc:
        raise LoiRunner('Nezha: giá trị metric sai schema số') from exc


def _doc_cua_so(selection, trace_guard_s=0):
    """Trả frame/arrays trong RAM; guard N được wrapper method áp riêng.

    metric.time là marker ns của front_service theo thứ tự; mỗi kênh vẫn giữ
    timestamp nguồn trong provenance. Không lưới/union/interpolate/dedup.
    """
    t = _integer(selection.get('t_ns'), 't_ns')
    guard = _integer(trace_guard_s, 'trace_guard_s')
    if guard not in (0, selection.get('trace_guard_s')):
        raise LoiRunner('Nezha: trace guard khác phạm vi đã duyệt')
    lo, hi = t - 300 * NS, t + 300 * NS
    csv.field_size_limit(10_000_000)
    sources, channel_values, arrays, channel_info = {}, {}, {}, {}
    marker = None
    for rel, meta in sorted(selection['files'].items()):
        p = _relative_path(rel)
        if p.parts[-2] != 'metric':
            continue
        front = p.name == 'front_service.csv'
        channels = FRONT_CHANNELS if front else RESOURCE_CHANNELS
        ident_col = 'ServiceName' if front else 'PodName'
        rows = []
        with _open_source(meta) as f:
            reader = csv.DictReader(f)
            _schema(reader, ['Time', ident_col] + list(channels), 'metric')
            for row in reader:
                timestamp = parse_time_ns(row['Time'])
                if not lo <= timestamp < hi:
                    continue
                ident = row[ident_col]
                aliases = SERVICE_ALIASES if front else POD_ALIASES
                if ident not in aliases or (not front and p.name != ident + '_metric.csv'):
                    raise LoiRunner('Nezha: định danh metric ngoài alias tường minh')
                rows.append((timestamp, aliases[ident], row))
        rows.sort(key=lambda item: item[0])
        times = [r[0] for r in rows]
        if len(rows) != 10 or sum(x < t for x in times) != 5:
            raise LoiRunner('Nezha: metric không giữ hợp đồng 5N+5A ordinal')
        if len({r[1] for r in rows}) != 1:
            raise LoiRunner('Nezha: một nguồn metric có nhiều service')
        if front:
            marker = times
        sources[rel] = dict(_stats(times, t), timestamps_ns=times,
                            sha256=meta['sha256'], bytes=meta['bytes'], kind='metric')
        for original, suffix in channels.items():
            name = rows[0][1] + '_' + suffix
            if name in channel_values:
                raise LoiRunner('Nezha: kênh metric sau alias bị trùng')
            values = np.asarray([_numeric(r[2][original]) for r in rows], dtype=float)
            n = np.asarray([v for x, v in zip(times, values) if x < t], dtype=float)
            a = np.asarray([v for x, v in zip(times, values) if x >= t], dtype=float)
            channel_values[name] = values
            arrays[name] = {'normal': n, 'anomalous': a}
            channel_info[name] = {'source': rel, 'source_column': original, 'timestamps_ns': times,
                                  'finite_N': int(np.isfinite(n).sum()), 'finite_A': int(np.isfinite(a).sum()),
                                  'nonfinite_N': int((~np.isfinite(n)).sum()),
                                  'nonfinite_A': int((~np.isfinite(a)).sum())}
    if marker is None or len(channel_values) != 165 or len(sources) != 11:
        raise LoiRunner('Nezha: không đủ 11 nguồn/165 kênh đã duyệt')
    for source in sources.values():
        if [x < t for x in source['timestamps_ns']] != [x < t for x in marker]:
            raise LoiRunner('Nezha: ordinal nguồn không cùng N/A với marker')
    metric = pd.DataFrame({'time': np.asarray(marker, dtype=np.int64), **channel_values})

    span_rows, seen, duplicate_spans = [], {}, 0
    for rel, meta in sorted(selection['files'].items()):
        if _relative_path(rel).parts[-2] != 'trace':
            continue
        starts, ends = [], []
        with _open_source(meta) as f:
            reader = csv.DictReader(f)
            _schema(reader, ['TraceID', 'SpanID', 'ParentID', 'PodName', 'OperationName',
                             'StartTimeUnixNano', 'EndTimeUnixNano', 'Duration'], 'trace')
            for row in reader:
                st, en = int(row['StartTimeUnixNano']), int(row['EndTimeUnixNano'])
                if st < lo or en >= hi:
                    continue
                if en < st or row['PodName'] not in POD_ALIASES or not row['TraceID'] or not row['SpanID']:
                    raise LoiRunner('Nezha: ID/service/thời gian span không hợp lệ')
                key = (row['TraceID'], row['SpanID'])
                signature = tuple(sorted(row.items()))
                if key in seen:
                    if seen[key] != signature:
                        raise LoiRunner('Nezha: span trùng khóa khác nội dung')
                    duplicate_spans += 1
                else:
                    seen[key] = signature
                try:
                    duration = Decimal(row['Duration'])
                except InvalidOperation as exc:
                    raise LoiRunner('Nezha: Duration không hợp lệ') from exc
                if not duration.is_finite() or duration < 0 or duration != int(duration):
                    raise LoiRunner('Nezha: Duration cần số nguyên us hữu hạn')
                duration = int(duration)
                if not 0 <= en - st - duration * 1000 < 1000:
                    raise LoiRunner('Nezha: Duration không khớp End-Start theo độ chính xác nguồn')
                us_end = (st // 1000 + duration) * 1000
                if (us_end < t) != (en < t) or (us_end < hi) != (en < hi):
                    raise LoiRunner('Nezha: đổi ns/us làm đổi membership end')
                span_rows.append([row['TraceID'], row['SpanID'], row['ParentID'],
                                  POD_ALIASES[row['PodName']], row['OperationName'], row['OperationName'],
                                  st // 1000, duration, st, en])
                starts.append(st)
                ends.append(en)
        sources[rel] = {'kind': 'trace', 'start_split': _stats(starts, t), 'end_split': _stats(ends, t),
                        'sha256': meta['sha256'], 'bytes': meta['bytes']}
    spans = pd.DataFrame(span_rows, columns=SPAN_COLUMNS)
    for col in ('startTime', 'duration', '_start_ns', '_end_ns'):
        spans[col] = spans[col].astype('int64')

    log_rows, log_seen, duplicate_logs = [], set(), 0
    for rel, meta in sorted(selection['files'].items()):
        if _relative_path(rel).parts[-2] != 'log':
            continue
        times = []
        with _open_source(meta) as f:
            reader = csv.DictReader(f)
            _schema(reader, ['TimeUnixNano', 'Timestamp', 'PodName', 'Log'], 'log')
            for row in reader:
                timestamp = int(row['TimeUnixNano'])
                if not lo <= timestamp < hi:
                    continue
                if row['PodName'] not in POD_ALIASES or _log_time_ns(row['Timestamp']) != timestamp:
                    raise LoiRunner('Nezha: định danh hoặc hai thời gian log không khớp')
                signature = tuple(sorted(row.items()))
                duplicate_logs += int(signature in log_seen)
                log_seen.add(signature)
                log_rows.append([timestamp, POD_ALIASES[row['PodName']], row['Log'], timestamp])
                times.append(timestamp)
        sources[rel] = dict(_stats(times, t), kind='log', sha256=meta['sha256'], bytes=meta['bytes'])
    logs = pd.DataFrame(log_rows, columns=LOG_COLUMNS)
    for col in ('timestamp', '_timestamp_ns'):
        logs[col] = logs[col].astype('int64')
    window = {'t_ns': t, 'N_ns': [lo, t], 'A_ns': [t, hi], 'trace_guard_s': guard,
              'metric_rows_N': 5, 'metric_rows_A': 5,
              'trace_rows_N_start': int((spans['_start_ns'] < t).sum()),
              'trace_rows_A_start': int((spans['_start_ns'] >= t).sum()),
              'trace_rows_N_end': int((spans['_end_ns'] < t).sum()),
              'trace_rows_A_end': int((spans['_end_ns'] >= t).sum()),
              'log_rows_N': int((logs['timestamp'] < t).sum()),
              'log_rows_A': int((logs['timestamp'] >= t).sum())}
    provenance = {'sources': sources, 'channels': channel_info,
                  'ordinal_marker_source': next(rel for rel in sources if rel.endswith('/front_service.csv')),
                  'ordinal_is_simultaneous_measurement': False,
                  'duplicates_retained': True, 'span_duplicate_rows': duplicate_spans,
                  'span_unique_keys': len(seen), 'log_identical_duplicate_rows': duplicate_logs,
                  'clock_shift_ns': 0, 'derived_payload_files': []}
    return {'metric': metric, 'metric_arrays': arrays, 'spans': spans, 'logs': logs,
            't_ns': t, 'window': window, 'provenance': provenance}


def doc_cua_so(selection, trace_guard_s=0):
    """Lỗi nguồn/schema là LoiRunner; không biến thành ERROR của phương pháp."""
    try:
        return _doc_cua_so(selection, trace_guard_s)
    except LoiRunner:
        raise
    except (ValueError, TypeError, KeyError, OverflowError, OSError, csv.Error) as exc:
        raise LoiRunner(f'Nezha: lỗi nguồn/schema {type(exc).__name__}: {exc}') from exc
