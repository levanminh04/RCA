"""FlashTicket OTLP files + Prometheus API -> the unchanged seven-argument M1 API.

No ledger, scenario name, injected service, directory, or case ID is passed to M1.
This is an initial adapter, not an approved FlashTicket method or an evaluation.
Native gauge times come from timestamp(metric), not PromQL evaluation-grid times.
Derived RED series explicitly use their evaluation times as their source clock.
"""
from collections import Counter, defaultdict
from decimal import Decimal
import json
import math
from pathlib import Path
import re
import urllib.parse
import urllib.request

NS = 10**9
ALIASES = {'discovery-server': 'config-discovery'}
INFRA = {'postgres': 'postgresql-shared-instance', 'user-db': 'mongodb-instance',
         'redis': 'cache', 'rabbitmq': 'broker'}
CHANNELS = {'cpu': 'tài nguyên', 'mem': 'tài nguyên', 'db-size': 'tài nguyên',
            'workload': 'lưu lượng', 'error': 'lỗi',
            'latency-50': 'độ trễ', 'latency-90': 'độ trễ'}
TOTAL_RATE = 'sum by(service_name) (rate(http_server_request_duration_seconds_count[1m]))'
QUERIES = [
    {'channel': 'cpu', 'query': 'container_cpu_utilization_ratio', 'native': True},
    {'channel': 'mem', 'query': 'container_memory_usage_total_bytes', 'native': True},
    {'channel': 'db-size', 'query': 'postgresql_db_size_bytes', 'native': True},
    {'channel': 'workload', 'query': TOTAL_RATE, 'native': False},
    {'channel': 'error', 'query':
     'sum by(service_name) (rate(http_server_request_duration_seconds_count{http_response_status_code=~"5.."}[1m])) '
     'or on(service_name) (0 * (' + TOTAL_RATE + '))', 'native': False},
    {'channel': 'latency-50', 'query':
     'histogram_quantile(0.5, sum by(le,service_name) (rate(http_server_request_duration_seconds_bucket[1m])))', 'native': False},
    {'channel': 'latency-90', 'query':
     'histogram_quantile(0.9, sum by(le,service_name) (rate(http_server_request_duration_seconds_bucket[1m])))', 'native': False},
]


def otlp_value(v):
    for name in ('stringValue', 'intValue', 'doubleValue', 'boolValue', 'bytesValue'):
        if name in v:
            return v[name]
    if 'kvlistValue' in v:
        return attributes(v['kvlistValue'].get('values', []))
    if 'arrayValue' in v:
        return [otlp_value(x) for x in v['arrayValue'].get('values', [])]
    return None


def attributes(items):
    return {x['key']: otlp_value(x['value']) for x in items}


def jsonl(paths):
    """Ignore only an unfinished final line of an actively appended JSONL file."""
    for path in sorted(map(Path, paths)):
        with path.open(encoding='utf-8') as stream:
            for line in stream:
                if not line.endswith('\n'):
                    continue
                yield json.loads(line)


def hex_id(value, width, root=False):
    if root and (value is None or value == '' or value == '0' * width):
        return ''
    if not isinstance(value, str) or not re.fullmatch('[0-9a-fA-F]{' + str(width) + '}', value):
        raise ValueError('Invalid OTLP hexadecimal ID')
    if value == '0' * width:
        raise ValueError('Invalid all-zero OTLP ID')
    return value.lower()


def _finite(value):
    try:
        number = float(value)
    except (ValueError, TypeError):
        return None
    return number if math.isfinite(number) else None


def _ns(seconds):
    return int(Decimal(str(seconds)) * NS)


def _owner(labels, inventory):
    db = labels.get('postgresql_database_name')
    if db:
        return db if db in inventory else None
    service = labels.get('service_name')
    service = ALIASES.get(service, INFRA.get(service, service))
    return service if service in inventory else None


def query_range(url, query, start, end, step=15):
    params = {'query': query, 'start': start, 'end': end, 'step': step}
    with urllib.request.urlopen(url.rstrip('/') + '/api/v1/query_range?' + urllib.parse.urlencode(params), timeout=45) as response:
        result = json.load(response)
    if result.get('status') != 'success' or result['data'].get('resultType') != 'matrix':
        raise ValueError('Prometheus range query did not return a successful matrix')
    return result['data']['result']


def collect_metrics(url, start, end, step=15):
    """Collector/runner calls this outside the M1 method; keep full API responses."""
    bundles = []
    for item in QUERIES:
        result = query_range(url, item['query'], start, end, step)
        clock = query_range(url, 'timestamp(' + item['query'] + ')', start, end, step) if item['native'] else None
        bundles.append(dict(item, step_seconds=step, result=result, native_timestamps=clock))
    return bundles


def _labels_key(labels):
    return tuple(sorted((k, v) for k, v in labels.items() if k != '__name__'))


def normalize_metrics(bundles, inventory):
    """Sparse rows, explicit native clock per channel/entity; no forward filling."""
    series = defaultdict(dict)
    identities = defaultdict(set)
    diagnostics = {'unmapped_series': [], 'empty_queries': [], 'nonfinite_points': 0,
                   'repeated_native_points': 0}
    steps = {}
    aliases = {}
    prefixes = {entity: entity.replace('_', '-') for entity in inventory}
    if len(set(prefixes.values())) != len(prefixes):
        raise ValueError('Inventory cannot be represented by collision-free metric prefixes')
    for entity, prefix in prefixes.items():
        if entity != prefix:
            if prefix in inventory and prefix != entity:
                raise ValueError('Metric prefix collides with another inventory entity')
            aliases[prefix] = entity
    for bundle in bundles:
        channel = bundle['channel']
        if channel not in CHANNELS:
            raise ValueError('Undeclared metric channel')
        result = bundle['result']
        if not result:
            diagnostics['empty_queries'].append(channel)
        clocks = {_labels_key(x['metric']): {str(t): v for t, v in x['values']}
                  for x in (bundle.get('native_timestamps') or [])}
        for item in result:
            labels = item['metric']
            owner = _owner(labels, inventory)
            if owner is None:
                diagnostics['unmapped_series'].append({'channel': channel, 'labels': labels})
                continue
            source = 'metric:' + channel + ':' + prefixes[owner]
            column = prefixes[owner] + '_' + channel
            identities[source].add(_labels_key(labels))
            if len(identities[source]) != 1:
                raise ValueError('Multiple runtime series map to one logical metric without a declared aggregation')
            steps[source] = (10 if bundle['native'] else bundle['step_seconds']) * NS
            native = clocks.get(_labels_key(labels), {})
            for evaluation, raw in item['values']:
                if bundle['native']:
                    timestamp = native.get(str(evaluation))
                    if timestamp is None or _finite(timestamp) is None:
                        raise ValueError('Native gauge sample timestamp missing')
                    when = _ns(timestamp)
                else:
                    when = _ns(evaluation)
                number = _finite(raw)
                if number is None:
                    diagnostics['nonfinite_points'] += 1
                key = (when, column)
                if key in series[source]:
                    if series[source][key] != number:
                        raise ValueError('Conflicting values at one native sample time')
                    diagnostics['repeated_native_points'] += 1
                series[source][key] = number
    rows, owners, indices, clocks, coverage = [], {}, {}, {}, {}
    for source in sorted(series):
        indices[source] = []
        clocks[source] = []
        for (when, column), number in sorted(series[source].items()):
            indices[source].append(len(rows))
            rows.append({'time': when, column: number})
            owners[column] = source
            clocks[source].append(when)
        coverage[source] = {'khoang': [[min(clocks[source]), max(clocks[source])]], 'r_ns': steps[source]}
    return rows, owners, indices, clocks, coverage, aliases, diagnostics


def normalize_spans(documents, lo_ns, hi_ns, inventory):
    seen = {}
    times = []
    details = {'records_seen': 0, 'duplicate_records': 0, 'root_spans': 0,
               'parent_missing_in_window': 0, 'outside_window': 0,
               'sub_microsecond_spans': 0, 'span_kinds': Counter(), 'resources': {}}
    for document in documents:
        for resource_spans in document.get('resourceSpans', document.get('batches', [])):
            resource = attributes(resource_spans.get('resource', {}).get('attributes', []))
            owner = resource.get('service.name')
            if not owner or ALIASES.get(owner, owner) not in inventory:
                raise ValueError('Trace service is missing or outside the fixed source inventory')
            details['resources'][owner] = {k: resource.get(k) for k in ['service.name', 'service.instance.id', 'host.id', 'service.version']}
            for group in resource_spans.get('scopeSpans', resource_spans.get('instrumentationLibrarySpans', [])):
                for raw in group.get('spans', []):
                    details['records_seen'] += 1
                    start = int(raw['startTimeUnixNano']); end = int(raw['endTimeUnixNano'])
                    if end < start:
                        raise ValueError('Negative OTLP span duration')
                    times.append(end)
                    if start < lo_ns or end >= hi_ns:
                        details['outside_window'] += 1
                        continue
                    tid = hex_id(raw['traceId'], 32)
                    sid = hex_id(raw['spanId'], 16)
                    parent = hex_id(raw.get('parentSpanId'), 16, root=True)
                    if not parent:
                        details['root_spans'] += 1
                    row = {'traceID': tid, 'spanID': sid, 'parentSpanID': parent,
                           'owner': owner, 'operation': raw['name'],
                           'start_us': start // 1000, 'duration_us': end // 1000 - start // 1000}
                    if end - start < 1000:
                        details['sub_microsecond_spans'] += 1
                    key = (tid, sid)
                    if key in seen:
                        if seen[key] != row:
                            raise ValueError('Conflicting duplicate OTLP span')
                        details['duplicate_records'] += 1
                        continue
                    seen[key] = row
                    details['span_kinds'][str(raw.get('kind'))] += 1
    rows = sorted(seen.values(), key=lambda s: (s['start_us'], s['traceID'], s['spanID']))
    details['parent_missing_in_window'] = sum(bool(r['parentSpanID']) and (r['traceID'], r['parentSpanID']) not in seen for r in rows)
    details['unique_spans'] = len(rows)
    details['span_kinds'] = dict(details['span_kinds'])
    details['owners'] = dict(Counter(row['owner'] for row in rows))
    # Span times have deliberately been rounded down to microseconds, as the
    # frozen API requires. Parent IDs are retained, including missing parents.
    coverage = {'khoang': [[min(times), max(times)]] if times else [], 'r_ns': 1000}
    return rows, coverage, details


def normalize_logs(documents, lo_ns, hi_ns, inventory):
    rows, times = [], []
    diagnostics = {'records_seen': 0, 'structured_records': 0, 'outside_window': 0,
                   'unknown_severity': 0, 'log_span_ids_present': 0}
    for document in documents:
        for resource_logs in document.get('resourceLogs', []):
            resource = attributes(resource_logs.get('resource', {}).get('attributes', []))
            owner = resource.get('service.name')
            if ALIASES.get(owner, owner) not in inventory:
                raise ValueError('Log service outside the fixed source inventory')
            for group in resource_logs.get('scopeLogs', []):
                for record in group.get('logRecords', []):
                    diagnostics['records_seen'] += 1
                    when = int(record.get('timeUnixNano') or record.get('observedTimeUnixNano'))
                    times.append(when)
                    if not lo_ns <= when < hi_ns:
                        diagnostics['outside_window'] += 1
                        continue
                    body = otlp_value(record.get('body', {}))
                    parsed = {}
                    if isinstance(body, str):
                        try:
                            parsed = json.loads(body)
                            parsed = parsed if isinstance(parsed, dict) else {}
                        except ValueError:
                            pass
                    elif isinstance(body, dict):
                        parsed = body
                    if parsed:
                        diagnostics['structured_records'] += 1
                    severity = parsed.get('severity') or parsed.get('level') or record.get('severityText')
                    if not severity and isinstance(body, str):
                        match = re.search(r'\b(TRACE|DEBUG|INFO|WARN|WARNING|ERROR|FATAL)\b', body)
                        severity = match[1] if match else None
                    if severity not in ['TRACE', 'DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL']:
                        diagnostics['unknown_severity'] += 1
                    if parsed.get('traceId') and parsed.get('spanId'):
                        diagnostics['log_span_ids_present'] += 1
                    message = parsed.get('message') if parsed else body
                    rows.append({'timestamp': when, 'entity': owner, 'message': '' if message is None else str(message), 'severity_raw': severity})
    rows.sort(key=lambda r: (r['timestamp'], r['entity'], r['message']))
    coverage = {'khoang': [[min(times), max(times)]] if times else [], 'r_ns': 1}
    diagnostics['records_in_window'] = len(rows)
    return rows, coverage, diagnostics


def adapt(trace_documents, log_documents, metric_bundles, inventory, t):
    """Pure conversion. The caller keeps all provenance and opaque IDs outside it."""
    inventory = list(inventory)
    lo, hi = (int(t) - 300) * NS, (int(t) + 300) * NS
    spans, tc, td = normalize_spans(trace_documents, lo, hi, inventory)
    logs, lc, ld = normalize_logs(log_documents, lo, hi, inventory)
    metrics, sources, indices, clocks, mc, metric_aliases, md = normalize_metrics(metric_bundles, inventory)
    aliases = dict(ALIASES, **metric_aliases)
    params = {
        'ho_so_nguon': {'kenh_metric': {'kieu': 'hau_to', 'bang': dict(CHANNELS)},
                       'quy_tac_log': {'kieu': 'severity', 'loi': ['ERROR', 'FATAL'],
                                      'khong_loi': ['TRACE', 'DEBUG', 'INFO', 'WARN', 'WARNING']},
                       'nguon_khoi_phat': ['trace', 'metric']},
        'don_vi_thoi_gian': {'spans.start_us': 'us', 'metrics.time': 'ns', 'logs.timestamp': 'ns'},
        'coverage': {'trace': tc, 'log': lc, **mc},
        'nguon_metric': sources, 'chi_so_hang_metric': indices,
        'thoi_gian_nguon': clocks, 'phan_hoach_NA_da_kiem': {},
    }
    return {'spans': spans, 'metrics': metrics, 'logs': logs, 'inventory': inventory,
            'aliases': aliases, 'params_ca': params,
            'chan_doan_adapter': {'trace': td, 'log': ld, 'metric': md,
                                 'metric_rows': len(metrics), 'metric_sources': len(clocks),
                                 'inventory_entities': len(inventory),
                                 'known_limits': ['Redis spans absent in observed preflight',
                                                  'P7 owns DB client spans at the JVM service, not the logical database',
                                                  'Design host bindings not inferred from Oracle deployment',
                                                  'Only tested runtime routes/messages have coverage evidence']}}
