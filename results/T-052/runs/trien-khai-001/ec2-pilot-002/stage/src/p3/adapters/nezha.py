"""Các lời gọi Nezha-OB đã duyệt ở Q-85; không nhận nhãn hay locator.

BARO nhận đúng 5 N + 5 A theo thứ tự từng nguồn, với marker ns của front.
SimpleRCA dùng arrays riêng từng kênh. Trace giữ hàng lặp; bảng độ nhạy chỉ
cắt bớt N theo end ns, không đưa phần bị bỏ sang A và không dịch đồng hồ.
CIRCA/TORAI B chỉ tạo UNSUPPORTED, không import hay chạy phương pháp đó.
"""
import math
from collections import Counter
from numbers import Integral

from . import LoiRunner, loi

NS = 1_000_000_000
METHODS = ('baro', 'simplerca', 'microrank', 'tracerca', 'circa', 'torai_B')
VARIANTS = {'baro': 'native', 'simplerca': 'M4', 'microrank': 'full',
            'tracerca': 'finite', 'circa': 'ols+rht_da', 'torai_B': 'B'}
VERSIONS = {'baro': 'RCAEval 259ea41 e2e/baro.py; Nezha Q-85',
            'simplerca': 'src/simplerca (T-017, M4); Nezha Q-85',
            'microrank': 'src/microrank (MicroRank-RCAEval sửa đầu vào); Nezha Q-85',
            'tracerca': 'RCAEval 259ea41 e2e/tracerca.py + lọc hữu hạn; Nezha Q-85',
            'circa': 'UNSUPPORTED Nezha-OB theo Q-85, không gọi CIRCA',
            'torai_B': 'UNSUPPORTED Nezha-OB theo Q-85, không gọi TORAI B'}
UNSUPPORTED = {
    'circa': 'Q-85: metric chỉ có 1–2 phép đo thật trong train; ở 19/22 ca, '
             'loader gốc nội suy đuôi train về điểm A, làm nền lẫn dữ liệu sau mốc. '
             'Không viết wrapper per-node, không sửa loader hay chạy thăm dò.',
    'torai_B': 'Q-85: schema trace Nezha-OB thiếu statusCode để dựng tracets_err; '
               'cadence metric khoảng 60 s không khớp stride 15 hàng của TORAI. '
               'Không giả trường, đổi stride, nội suy hoặc chạy biến thể cứu.'}


def _nguyen(value, field):
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise LoiRunner(field + ' phải là số nguyên')
    return int(value)


def _trace(payload, guard):
    """Trả span cho phương pháp end-split, vẫn giữ membership A ban đầu."""
    spans = payload['spans']
    t_ns = _nguyen(payload['t_ns'], 't_ns')
    if t_ns % NS:
        raise LoiRunner('mốc Nezha phải là giây nguyên trước khi gọi phương pháp trace')
    required = {'_start_ns', '_end_ns', 'startTime', 'duration', 'serviceName'}
    if not required <= set(spans.columns):
        raise LoiRunner('span thiếu cột kiểm ns/µs')
    st_ns, en_ns = spans['_start_ns'], spans['_end_ns']
    us = t_ns // 1000
    en_us = spans['startTime'] + spans['duration']
    if not ((st_ns < t_ns) == (spans['startTime'] < us)).all():
        raise LoiRunner('đổi ns→µs làm đổi membership start tại t')
    if not ((en_ns < t_ns) == (en_us < us)).all():
        raise LoiRunner('đổi ns→µs làm đổi membership end tại t')
    keep = (en_ns < t_ns - guard * NS) | (en_ns >= t_ns)
    selected = spans.loc[keep].copy().reset_index(drop=True)
    diag = {'trace_guard_s': guard, 'trace_rows_outer': int(len(spans)),
            'trace_rows_N_end': int((en_ns < t_ns - guard * NS).sum()),
            'trace_rows_A_end': int((en_ns >= t_ns).sum()),
            'trace_rows_removed_N_gap': int((~keep).sum()),
            'trace_ns_us_membership_check': 'pass', 'dedup': 'none'}
    return selected, diag


def _simple(payload, guard):
    from simplerca import Config, diagnose
    arrays = payload['metric_arrays']
    normal, anomalous, mappings = {}, {}, {}
    for column, values in arrays.items():
        if not isinstance(column, str) or '_' not in column:
            raise LoiRunner('metric column phải là service_suffix')
        service, suffix = column.rsplit('_', 1)
        if not service or not suffix or '_' in service:
            raise LoiRunner('metric mapping Nezha không hợp lệ: ' + column)
        normal[column], anomalous[column] = values['normal'], values['anomalous']
        mappings[column] = service
    spans = payload['spans']
    t_ns = _nguyen(payload['t_ns'], 't_ns')
    before = spans['_start_ns'] < t_ns
    if guard:
        before &= spans['_end_ns'] < t_ns - guard * NS
    after = spans['_start_ns'] >= t_ns

    def durations(mask):
        return {str(service): part['duration'].tolist()
                for service, part in spans.loc[mask].groupby('serviceName', sort=True)}

    logs = payload['logs']
    incident_logs = None
    observed = set(mappings.values()) | set(spans.loc[before | after, 'serviceName'])
    if logs is not None:
        observed.update(logs['container_name'])
        ts = logs['_timestamp_ns'] if '_timestamp_ns' in logs else logs['timestamp']
        incident_logs = {str(service): part['message'].tolist()
                         for service, part in logs.loc[ts >= t_ns].groupby('container_name', sort=True)}
    shape = {'metric_cols': len(arrays), 'metric_rows_N_per_channel': {
                 k: len(v) for k, v in normal.items()},
             'metric_rows_A_per_channel': {k: len(v) for k, v in anomalous.items()},
             'spans': int((before | after).sum()),
             'spans_N_start': int(before.sum()), 'spans_A_start': int(after.sum()),
             'log_rows_A': None if incident_logs is None else sum(map(len, incident_logs.values()))}
    try:
        result = diagnose(normal_metrics=normal, incident_metrics=anomalous,
                          metric_services=mappings, normal_traces=durations(before),
                          incident_traces=durations(after), incident_logs=incident_logs,
                          observed_services=tuple(sorted(observed)), config=Config())
    except Exception as exc:  # lỗi của core, không thay loại trạng thái
        out = loi(exc)
        out.update(input_shape=shape, observed_entities=sorted(observed))
        return out
    abstain = result['status'] == 'abstain'
    items = [] if abstain else [(s, s, (float(result['scores'][s]['score']),))
                               for s in result['ranks']]
    return {'status': 'NO_EVIDENCE' if abstain else 'OK',
            'method_status_raw': result['status'], 'error': None, 'items': items,
            'ranking_native': result['ranks'], 'observed_entities': sorted(observed),
            'input_shape': shape, 'diagnostics': {
                'key_check': 'pass', 'metric_arrays_native': True,
                'metric_unavailable_channels': sum(v['status'] != 'ok' for v in result['metrics'].values()),
                'metric_missing_N_values': sum(v['missing_normal'] for v in result['metrics'].values()),
                'metric_missing_A_values': sum(v['missing_incident'] for v in result['metrics'].values()),
                'trace_unavailable_services': sum(v['status'] != 'ok' for v in result['traces'].values()),
                'trace_guard_s': guard, 'trace_rows_N_start': int(before.sum()),
                'trace_rows_A_start': int(after.sum()),
                'trace_rows_removed_N_gap': int(((spans['_start_ns'] < t_ns) & ~before).sum()),
                'dedup': 'none', 'metric_filling': 'none',
                'tie_groups_goc': len(result['tie_groups'])}}


def _tracerca_doc_lap(spans, t_seconds, result):
    """Đếm ji độc lập theo T-015, không gọi hàm tác giả hoặc dùng nhãn."""
    from pandas import isna
    baseline, post = {}, []
    t_us = t_seconds * 1_000_000
    cols = ['serviceName', 'methodName', 'operationName', 'startTime', 'duration']
    for service, method, operation, start, duration in spans[cols].itertuples(index=False, name=None):
        if isna(method):
            method = operation
        op = service + '_' + method
        if start + duration < t_us:
            baseline.setdefault(op, []).append(float(duration))
        else:
            post.append((op, float(duration)))
    stats = {}
    for op, values in baseline.items():
        mean = math.fsum(values) / len(values)
        std = math.sqrt(math.fsum((x - mean) ** 2 for x in values) / (len(values) - 1)) if len(values) > 1 else math.nan
        stats[op] = (round(mean / 1000, 2), round(std / 1000, 2))
    counts, total = {}, 0
    for op, duration in post:
        mean, std = stats[op]
        flag = int(duration / 1000 >= mean + 3 * std)
        cell = counts.setdefault(op, [0, 0])
        cell[0] += 1
        cell[1] += flag
        total += flag
    expected = {}
    for op, (count, flag) in counts.items():
        support = flag / total if total else math.nan
        confidence = flag / count
        denominator = support + confidence
        score = 2 * support * confidence / denominator if denominator else math.nan
        if math.isfinite(score):
            expected[op] = score
    actual = {op: float(key[0]) for op, _service, key in result.get('items', [])}
    if set(actual) != set(expected):
        raise LoiRunner('TraceRCA: tập ji hữu hạn không khớp phép tính độc lập')
    differences = [abs(actual[op] - value) for op, value in expected.items()]
    if any(not math.isclose(actual[op], value, rel_tol=1e-10, abs_tol=1e-10)
           for op, value in expected.items()):
        raise LoiRunner('TraceRCA: ji không khớp phép tính độc lập')
    return {'status': 'pass', 'finite_operations': len(expected),
            'nonfinite_operations': len(counts) - len(expected),
            'abnormal_spans': total, 'max_abs_difference': max(differences, default=0.0)}


def _diagnostics(result):
    items = result.get('items') or []
    keys = [tuple(float(x) for x in key) for _item, _entity, key in items]
    if any(not all(math.isfinite(v) for v in key) for key in keys):
        raise LoiRunner('khóa xếp hạng không hữu hạn')
    counts = Counter(keys)
    diag = result.setdefault('diagnostics', {})
    diag.update(empty_ranking=not items, returned_items=len(items),
                returned_entities=len({entity for _item, entity, _key in items}),
                ranking_nonfinite_keys=0, exact_tie_group_sizes=sorted(counts.values(), reverse=True),
                all_items_tied=bool(items) and len(counts) == 1)
    return result


def chay(method, payload=None, trace_guard_s=0):
    """Một result/variant; payload chỉ dữ liệu, marker, thống kê và provenance."""
    if method not in METHODS:
        raise LoiRunner('phương pháp Nezha không được duyệt: ' + str(method))
    guard = _nguyen(trace_guard_s, 'trace_guard_s')
    if guard not in (0, 32, 41):
        raise LoiRunner('trace_guard_s không thuộc cấu hình đã duyệt')
    if method in UNSUPPORTED:
        return [dict(status='UNSUPPORTED', method_status_raw=None, error=UNSUPPORTED[method],
                     items=[], ranking_native=[], observed_entities=[], input_shape={},
                     variant=VARIANTS[method], diagnostics={'method_called': False,
                     'empty_ranking': True, 'returned_items': 0, 'returned_entities': 0,
                     'seed': None})]
    if not isinstance(payload, dict):
        raise LoiRunner('phương pháp được hỗ trợ cần payload Nezha')
    if method == 'baro':
        if guard:
            raise LoiRunner('bảng độ nhạy trace không áp dụng BARO')
        from .baro import chay as baro
        result = baro(payload['metric'], _nguyen(payload['t_ns'], 't_ns'))
        result.setdefault('diagnostics', {}).update(metric_layout='5N+5A ordinal; front marker ns',
                                                   no_simultaneity_assumption=True)
    elif method == 'simplerca':
        result = _simple(payload, guard)
    else:
        spans, trace_diag = _trace(payload, guard)
        t_seconds = int(payload['t_ns']) // NS
        if method == 'microrank':
            from .microrank import chay as microrank
            result = microrank(spans, t_seconds)
        else:
            from .tracerca import chay as tracerca
            result = tracerca(spans, t_seconds)
            if result['status'] in ('OK', 'NO_EVIDENCE'):
                result.setdefault('diagnostics', {})['independent_ji_check'] = _tracerca_doc_lap(spans, t_seconds, result)
        result.setdefault('diagnostics', {}).update(trace_diag)
    result['variant'] = VARIANTS[method]
    result.setdefault('method_status_raw', None)
    result.setdefault('error', None)
    return [_diagnostics(result)]
