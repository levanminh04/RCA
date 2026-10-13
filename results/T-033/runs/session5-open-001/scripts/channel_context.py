"""T-033: descriptive context from hash-checked dev telemetry, on metric seconds.

EC2 only. No root/fault/proxy labels, detector, error regex, anomaly threshold or
new analysis window. Zero counts are observed artifact counts; collector coverage
is unknown. Duration retains its raw unit (OPEN), not a physical time claim.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import resource
import shutil
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import psutil
import pyarrow as pa
import pyarrow.parquet as pq

CLOCK_SOURCE_SHA256 = '1c509f98b44363e3cf4a5055a6be9bd27da5fd950f7a61229f8ef8eb8600147c'
PARENT_SOURCE_SHA256 = 'd1b8fe8bc1d1300463fbbceb26eee83d049ca7517627557d13c1daac478db185'
CARD_SHA256 = 'a7a4c0b720c8266a6aad3bae34ba3053d632bd253d95c311b9a7d55e826f4643'
TRACE_COLUMNS = ['traceID', 'spanID', 'serviceName', 'parentSpanID',
                 'startTimeMillis', 'startTime', 'duration', 'statusCode']
TRACE_INTS = ['startTimeMillis', 'startTime', 'duration', 'statusCode']
TRACE_STRINGS = ['time', 'traceID', 'spanID', 'serviceName', 'methodName',
                 'operationName', 'parentSpanID']
LOG_COLUMNS = ['timestamp', 'container_name', 'message']


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                    allow_nan=False) + '\n', encoding='utf-8')


def manifest_entry(run, name):
    meta = read(run / 'manifest.json')[name]
    path = run / name
    require(path.is_file() and path.stat().st_size == meta['bytes'] and sha(path) == meta['sha256'],
            'Source manifest mismatch: ' + str(path))
    return path


def update_manifest(run):
    write(run / 'manifest.json', {
        p.name: {'sha256': sha(p), 'bytes': p.stat().st_size}
        for p in sorted(run.iterdir()) if p.is_file() and p.name != 'manifest.json'})


def progress(home, message):
    line = datetime.now(timezone.utc).isoformat() + ' CHANNEL_CONTEXT ' + message
    print(line, flush=True)
    with (home / 'trang-thai.txt').open('a', encoding='utf-8') as handle:
        handle.write(line + '\n')


def guard(home, source, started, projected=0):
    require(not (home / 'STOP').exists(), 'STOP user/agent')
    elapsed = (datetime.now(timezone.utc) - started).total_seconds()
    require(0 <= elapsed < source['budget_compute_s'], 'BUDGET_STOP: approved total calendar budget')
    used = sum(p.stat().st_size for p in home.rglob('*') if p.is_file())
    free = shutil.disk_usage(home).free
    require(used + projected < source['budget_bytes'], 'BUDGET_STOP: approved storage before write')
    require(projected < free, 'DISK_STOP: insufficient free bytes before write')
    return {'new_bytes': used, 'disk_free_bytes': free,
            'ram_available_bytes': psutil.virtual_memory().available,
            'machine_elapsed_since_first_compute_s': elapsed}


def integer_values(series, name):
    """Preserve exact int64 and missing masks; no fallback for missing timestamps."""
    numeric = pd.to_numeric(series, errors='raise')
    valid = numeric.notna().to_numpy()
    values = np.zeros(len(series), dtype=np.int64)
    if valid.any():
        raw = numeric.loc[valid]
        require(np.isfinite(raw.to_numpy(dtype=float)).all(), name + ': nonfinite values')
        integers = raw.astype(np.int64)
        require(bool(raw.eq(integers).all()), name + ': not exact int64')
        values[valid] = integers.to_numpy(dtype=np.int64)
    return values, valid


def entity_codes(series):
    """Null and literal empty string differ; no service/container alias is inferred."""
    labels = sorted(series.dropna().unique().tolist())
    require(all(isinstance(label, str) for label in labels), 'Non-string entity label')
    labels += [None] if series.isna().any() else []
    lookup = {label: i for i, label in enumerate(labels) if label is not None}
    codes = series.map(lookup)
    if None in labels:
        codes = codes.fillna(labels.index(None))
    require(codes.notna().all(), 'Entity coding lost rows')
    return codes.to_numpy(dtype=np.int32), labels


def identity_present(series):
    return (series.notna() & series.ne('')).to_numpy(dtype=bool)


def dense_counts(groups, field, times, entities):
    """Zero means no events observed in the supplied file bin; coverage is OPEN."""
    out = np.zeros((len(times), len(entities)), dtype=np.int64)
    if len(groups):
        indexes = pd.Index(times).get_indexer(groups['second'])
        keep = indexes >= 0
        out[indexes[keep], groups.loc[keep, 'entity'].to_numpy(dtype=np.int32)] = (
            groups.loc[keep, field].to_numpy(dtype=np.int64))
    return out


def alignment(seconds, valid, times):
    actual = seconds[valid]
    on = np.isin(actual, times)
    observed = np.unique(actual)
    overlap = np.intersect1d(observed, times)
    return {'rows': len(seconds), 'missing_timestamp_rows': int((~valid).sum()),
            'timestamped_rows': int(valid.sum()), 'on_metric_grid_rows': int(on.sum()),
            'off_metric_grid_rows': int((~on).sum()),
            'before_metric_grid_rows': int((actual < times[0]).sum()),
            'after_metric_grid_rows': int((actual > times[-1]).sum()),
            'event_seconds_observed': len(observed),
            'metric_seconds_with_observed_events': len(overlap),
            'metric_seconds_without_observed_events': len(times) - len(overlap),
            'event_second_min': int(actual.min()) if len(actual) else None,
            'event_second_max': int(actual.max()) if len(actual) else None,
            'collector_coverage': 'OPEN: no sampling/heartbeat/completeness metadata',
            'zero_count': 'No events observed in artifact bin; completeness unknown',
            'bin': '[metric_time, metric_time+1) using source timestamp; no smoothing'}


def schema_checked(path, modality):
    schema = pq.read_schema(path)
    ints = TRACE_INTS if modality == 'trace' else ['timestamp']
    strings = TRACE_STRINGS if modality == 'trace' else ['container_name', 'message']
    require(set(ints + strings) <= set(schema.names), modality + ': missing schema fields')
    for name in ints:
        require(pa.types.is_int64(schema.field(name).type), modality + ': expected int64 ' + name)
    for name in strings:
        dtype = schema.field(name).type
        require(pa.types.is_string(dtype) or pa.types.is_large_string(dtype),
                modality + ': expected string ' + name)
    return [{'name': f.name, 'type': str(f.type), 'nullable': f.nullable} for f in schema]


def trace_context(frame, times, us):
    start, valid = integer_values(frame['startTime'], 'trace startTime')
    millis, millis_valid = integer_values(frame['startTimeMillis'], 'trace startTimeMillis')
    joint = valid & millis_valid
    relation = start[joint] // 1000 == millis[joint]
    require(bool(relation.all()), 'CLOCK_STOP: startTime//1000 differs from startTimeMillis')
    require(not len(frame) or bool(joint.any()), 'CLOCK_STOP: no joint timestamp for verification')
    seconds = start // us
    codes, entities = entity_codes(frame['serviceName'])
    # T-002 inspect_local.py:83-84. Root-or-empty-parent metadata is not a
    # confirmed external request; unresolved nonempty parents are not roots.
    parent = frame['parentSpanID'].fillna('').astype(str)
    root = parent.str.fullmatch(r'(?:|0+|None|null)', case=False).to_numpy(dtype=bool)
    trace_present = identity_present(frame['traceID'])
    span_present = identity_present(frame['spanID'])
    duration, duration_valid = integer_values(frame['duration'], 'trace duration raw')
    status_values, status_valid = integer_values(frame['statusCode'], 'trace statusCode raw')
    duration_float = duration.astype(float)
    duration_float[~duration_valid] = np.nan
    work = pd.DataFrame({'second': seconds[valid], 'entity': codes[valid],
        'root': root[valid].astype(np.int64),
        'trace_id': frame['traceID'].where(trace_present).to_numpy()[valid],
        'root_trace_id': frame['traceID'].where(trace_present & root).to_numpy()[valid],
        'trace_id_missing': (~trace_present[valid]).astype(np.int64),
        'span_id_missing': (~span_present[valid]).astype(np.int64),
        'duration_raw': duration_float[valid],
        'duration_negative': (duration[valid] < 0).astype(np.int64),
        'status_present': status_valid[valid].astype(np.int64)})
    stats = work.groupby(['second', 'entity'], sort=True, dropna=False).agg(
        span_count=('second', 'size'), root_or_empty_parent_count=('root', 'sum'),
        trace_id_distinct=('trace_id', 'nunique'), root_trace_id_distinct=('root_trace_id', 'nunique'),
        trace_id_missing=('trace_id_missing', 'sum'), span_id_missing=('span_id_missing', 'sum'),
        duration_count=('duration_raw', 'count'), duration_negative=('duration_negative', 'sum'),
        duration_min_raw=('duration_raw', 'min'), duration_max_raw=('duration_raw', 'max'),
        duration_mean_raw=('duration_raw', 'mean'), duration_median_raw=('duration_raw', 'median'),
        status_present=('status_present', 'sum')).reset_index()
    stats['duration_missing'] = stats['span_count'] - stats['duration_count']
    stats['status_missing'] = stats['span_count'] - stats['status_present']
    arrays = {('trace_group_' + name): stats[name].to_numpy(dtype=(float if name.endswith('_raw') else np.int64))
              for name in stats}
    for name in ('span_count', 'root_or_empty_parent_count', 'trace_id_distinct',
                 'root_trace_id_distinct', 'status_present', 'status_missing'):
        arrays['trace_grid_' + name] = dense_counts(stats, name, times, entities)
    global_stats = work.groupby('second', sort=True).agg(span_count=('second', 'size'),
        trace_id_distinct=('trace_id', 'nunique'), root_trace_id_distinct=('root_trace_id', 'nunique')).reset_index()
    global_stats['entity'] = 0
    for name in ('span_count', 'trace_id_distinct', 'root_trace_id_distinct'):
        arrays['trace_global_grid_' + name] = dense_counts(global_stats, name, times, [None])[:, 0]
    status_frame = pd.DataFrame({'entity': codes[status_valid], 'status_raw': status_values[status_valid]})
    freq = status_frame.groupby(['entity', 'status_raw'], sort=True).size().reset_index(name='rows')
    for name in freq:
        arrays['trace_status_all_' + name] = freq[name].to_numpy(dtype=np.int64)
    checks = {'timestamp_field_relation_exact': bool(relation.all()),
        'grouped_span_rows_conserved': int(stats['span_count'].sum()) == int(valid.sum()),
        'grouped_root_rows_conserved': int(stats['root_or_empty_parent_count'].sum()) == int(root[valid].sum()),
        'grid_span_rows_conserved': int(arrays['trace_grid_span_count'].sum()) == int(np.isin(seconds[valid], times).sum()),
        'status_rows_conserved': int(freq['rows'].sum()) == int(status_valid.sum()),
        'duration_partition': bool(np.all(stats['duration_count'] + stats['duration_missing'] == stats['span_count']))}
    require(all(checks.values()), 'Trace conservation failed: ' + str(checks))
    summary = {'status': 'OBSERVED_ARTIFACT', 'entities': entities,
        'entity_field': 'literal serviceName; null has separate code; no alias inferred',
        'alignment': alignment(seconds, valid, times),
        'timestamp_conversion': 'startTime//p3.cua_so.US; US=1000000; startTime//1000==startTimeMillis checked',
        'timestamp_relation_joint_rows': int(joint.sum()),
        'timestamp_relation_missing_either_rows': int((~joint).sum()),
        'subsecond_start_rows': int(((start % us != 0) & valid).sum()),
        'root_or_empty_parent_count_all': int(root.sum()),
        'root_definition': 'parentSpanID null, empty, 0+, None or null, case insensitive (T-002)',
        'observed_trace_id_distinct_all': int(frame.loc[trace_present, 'traceID'].nunique()),
        'trace_id_missing_or_empty_all': int((~trace_present).sum()),
        'span_id_missing_or_empty_all': int((~span_present).sum()),
        'request_count_semantics': 'OPEN: distinct observed traceIDs/root traceIDs are proxies, not confirmed external requests; a trace can appear in several seconds/services',
        'duration': {'unit': 'OPEN_RAW_UNIT', 'source': 'results/T-002/the-rcaeval.md §4',
                     'present_rows': int(duration_valid.sum()), 'missing_rows': int((~duration_valid).sum()),
                     'negative_rows': int(((duration < 0) & duration_valid).sum()),
                     'physical_conversion_or_end_time_filter_used': False},
        'status': {'present_rows': int(status_valid.sum()), 'missing_rows': int((~status_valid).sum()),
                   'interpretation': 'Raw values only; no error/status semantics assumed'},
        'checks': checks}
    return arrays, summary


def log_context(frame, times):
    seconds, valid = integer_values(frame['timestamp'], 'log timestamp seconds')
    codes, entities = entity_codes(frame['container_name'])
    missing = frame['message'].isna().to_numpy()
    digests = np.zeros((len(frame), 32), dtype=np.uint8)
    for row, message in enumerate(frame['message']):
        if not missing[row]:
            require(isinstance(message, str), 'Message must be original string or null')
            digests[row] = np.frombuffer(hashlib.sha256(message.encode('utf-8')).digest(), dtype=np.uint8)
    work = pd.DataFrame({'second': seconds[valid], 'entity': codes[valid],
                         'message_missing': missing[valid].astype(np.int64)})
    stats = work.groupby(['second', 'entity'], sort=True, dropna=False).agg(
        row_count=('second', 'size'), message_missing=('message_missing', 'sum')).reset_index()
    arrays = {'log_message_sha256': digests, 'log_row_timestamp': seconds,
              'log_row_timestamp_present': valid, 'log_row_entity_code': codes,
              'log_row_message_missing': missing}
    for name in stats:
        arrays['log_group_' + name] = stats[name].to_numpy(dtype=np.int64)
    for name in ('row_count', 'message_missing'):
        arrays['log_grid_' + name] = dense_counts(stats, name, times, entities)
    checks = {'grouped_log_rows_conserved': int(stats['row_count'].sum()) == int(valid.sum()),
        'grouped_message_missing_conserved': int(stats['message_missing'].sum()) == int(missing[valid].sum()),
        'grid_log_rows_conserved': int(arrays['log_grid_row_count'].sum()) == int(np.isin(seconds[valid], times).sum()),
        'message_digest_index_shape': digests.shape == (len(frame), 32),
        'missing_message_digests_zero': bool((digests[missing] == 0).all())}
    require(all(checks.values()), 'Log conservation failed: ' + str(checks))
    return arrays, {'status': 'OBSERVED_ARTIFACT', 'entities': entities,
        'entity_field': 'literal container_name; no service/container alias inferred',
        'alignment': alignment(seconds, valid, times), 'message_missing_rows': int(missing.sum()),
        'message_empty_string_rows': int((frame['message'].eq('') & frame['message'].notna()).sum()),
        'hash_index': {'row_index': '0-based original parquet row order, implicit array position; no sort/dedup',
            'digest': 'SHA256 of exact message UTF-8 bytes without strip/normalization',
            'missing_message': 'Separate bool mask; zero digest placeholder is not a real message hash',
            'source_text_exported': False,
            'readback': 'Hash-check original logs.parquet; use row index and compare SHA256 of original message'},
        'checks': checks}


def fixtures(us):
    """Short metadata/count/hash fixtures; executed only on EC2, no detector."""
    times = np.array([100, 101], dtype=np.int64)
    starts = np.array([100 * us, 101 * us - 1, 101 * us, 99 * us, 102 * us], dtype=np.int64)
    trace = pd.DataFrame({'startTime': starts, 'startTimeMillis': starts // 1000,
        'serviceName': ['s', 's', 's', 's', None], 'parentSpanID': ['', '0', 'p', 'None', 'p'],
        'traceID': ['a', 'b', 'a', 'c', 'd'], 'spanID': ['1', '2', '3', '4', '5'],
        'duration': [3, 4, 5, np.nan, -1], 'statusCode': [np.nan, 0, 1, np.nan, 2]})
    a, s = trace_context(trace, times, us)
    require(np.array_equal(a['trace_grid_span_count'][:, 0], [2, 1]), 'Fixture start bin boundaries')
    require(np.array_equal(a['trace_grid_root_or_empty_parent_count'][:, 0], [2, 0]), 'Fixture root metadata count')
    require(np.array_equal(a['trace_global_grid_trace_id_distinct'], [2, 1]), 'Fixture distinct traceID')
    require(s['alignment']['off_metric_grid_rows'] == 2, 'Fixture off-grid conservation')
    keep = (a['trace_group_second'] == 100) & (a['trace_group_entity'] == 0)
    require(a['trace_group_duration_mean_raw'][keep].tolist() == [3.5]
            and a['trace_group_duration_median_raw'][keep].tolist() == [3.5], 'Fixture raw duration arithmetic')
    require(s['duration']['unit'] == 'OPEN_RAW_UNIT', 'Fixture duration unit not invented')
    logs = pd.DataFrame({'timestamp': [100, 100, 101, 99, 102],
        'container_name': ['s', 's', 's', None, 's'], 'message': ['a', None, '', 'b', 'a']})
    a, s = log_context(logs, times)
    require(np.array_equal(a['log_grid_row_count'][:, 0], [2, 1]), 'Fixture log bin count')
    require(np.array_equal(a['log_grid_message_missing'][:, 0], [1, 0]), 'Fixture missing message')
    require(np.array_equal(a['log_message_sha256'][0], a['log_message_sha256'][4]), 'Fixture repeated message')
    require(bytes(a['log_message_sha256'][2]).hex() == hashlib.sha256(b'').hexdigest(), 'Fixture empty digest')
    require(s['alignment']['off_metric_grid_rows'] == 2, 'Fixture log off-grid conservation')
    return {'status': 'PASS', 'checks': ['start bin boundary', 'root-or-empty-parent metadata',
        'distinct observed traceID', 'off-grid conservation', 'duration arithmetic/raw unit OPEN',
        'null vs empty message', 'original-row repeated message hash']}


def input_path(source, inventory_case, item, name):
    meta = item['files'][name]
    rel = Path(meta['path'])
    require(not rel.is_absolute() and '..' not in rel.parts
            and rel.parts[:2] == ('data', 'rcaeval') and len(rel.parts) == 4
            and rel.parts[2].startswith('re2tt_') and rel.name == name,
            'Source outside approved RE2-TT telemetry path shape')
    path = Path(inventory_case['files'][name]).resolve()
    expected = [(Path(root) / rel).resolve() for root in source['source_roots_remote']]
    require(path in expected and any(path.is_relative_to(Path(root).resolve())
                                    for root in source['source_roots_remote']),
            'Inventory differs from exact allowlisted source path')
    require(not any(part.lower() in ('locked', 'test', 'heldout', 't-032', 'flash-ticket-rca-research')
                    for part in path.parts), 'Forbidden dataset/task/archive path')
    require(path.is_file() and path.stat().st_size == meta['bytes'] and sha(path) == meta['sha256'],
            'Source telemetry hash/bytes mismatch: ' + name)
    return path, {'path': str(path), 'sha256': meta['sha256'], 'bytes': meta['bytes']}


def case_context(item, source, inventory_case, us, phase):
    paths, provenance = {}, {}
    for name in ('metrics.parquet', 'traces.parquet', 'logs.parquet'):
        if name in item['files']:
            paths[name], provenance[name] = input_path(source, inventory_case, item, name)
    require('metrics.parquet' in paths and 'traces.parquet' in paths, 'Required metric/trace source missing')
    phase('METRIC')
    metrics = pd.read_parquet(paths['metrics.parquet'])
    times, valid = integer_values(metrics['time'], 'metric seconds')
    require(bool(valid.all()) and len(times) == inventory_case['T'] == 1441
            and np.all(np.diff(times) == 1) and times[0] == inventory_case['time_start']
            and times[-1] == inventory_case['time_end'], 'Verified metric grid changed')
    columns = [name for name in metrics.columns if name.endswith('_workload')]
    workload = metrics[columns].to_numpy(dtype=float)
    arrays = {'times': times, 'workload_raw': workload, 'workload_columns': np.array(columns, dtype=str),
              'workload_nan': np.isnan(workload), 'workload_inf': np.isinf(workload)}
    metric = {'status': 'OBSERVED_ARTIFACT', 'T': len(times), 'columns': columns,
        'dtypes': {name: str(metrics[name].dtype) for name in columns},
        'values': 'Raw *_workload; no fill/scaling/drop/alias; metric units not inferred',
        'missing_cells': int(np.isnan(workload).sum()), 'infinite_cells': int(np.isinf(workload).sum()),
        'coverage': 'Every grid row exists; a null workload is missing, not zero',
        'time_start': int(times[0]), 'time_end': int(times[-1])}
    phase('TRACE')
    trace_schema = schema_checked(paths['traces.parquet'], 'trace')
    trace = pd.read_parquet(paths['traces.parquet'], columns=TRACE_COLUMNS)
    trace_arrays, trace_summary = trace_context(trace, times, us)
    arrays.update(trace_arrays)
    del trace
    phase('LOG')
    if 'logs.parquet' in paths:
        log_schema = schema_checked(paths['logs.parquet'], 'log')
        logs = pd.read_parquet(paths['logs.parquet'], columns=LOG_COLUMNS)
        log_arrays, log_summary = log_context(logs, times)
        arrays.update(log_arrays)
        del logs
    else:
        log_schema = None
        log_summary = {'status': 'N/A_MISSING_CHANNEL', 'entities': None, 'alignment': None,
            'message_missing_rows': None, 'counts': None,
            'interpretation': 'No source log in allowlist; no zero counts synthesized'}
    for name, path in paths.items():
        require(sha(path) == provenance[name]['sha256'], 'Source changed during processing: ' + name)
    return arrays, {'metric': metric, 'trace': trace_summary, 'log': log_summary,
                    'schema': {'trace': trace_schema, 'log': log_schema}, 'source_files': provenance}


def main(args):
    require(platform.system() == 'Linux', 'Research execution restricted to approved EC2 Linux')
    home = Path(os.environ['T033_HOME']).resolve()
    require(home == (Path.home() / 'rca/T-033').resolve(), 'T033_HOME must be approved ~/rca/T-033')
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run) is not None, 'Run name must be basename')
    run = home / 'runs' / args.run
    run.mkdir(parents=True, exist_ok=False)
    source_path = home / 'inputs/source.json'
    status = {'status': 'RUNNING', 'pid': os.getpid(), 'started_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': sha(__file__), 'source_sha256': sha(source_path),
              'command': sys.argv, 'cases': {}, 'units_completed': 0}
    write(run / 'status.json', status)
    t0 = time.perf_counter()
    try:
        source = read(source_path)
        require(source['task'] == 'T-033' and len(source['cases']) == 30
                and len({item['opaque_id'] for item in source['cases']}) == 30, 'Wrong task/source coverage')
        require(sum('traces.parquet' in item['files'] for item in source['cases']) == 30
                and sum('logs.parquet' in item['files'] for item in source['cases']) == 29,
                'Approved trace/log coverage changed')
        require((np.__version__, pd.__version__) == ('1.26.4', '2.2.3'), 'Source package versions changed')
        first_status = read(manifest_entry(home / 'runs/nsigma-first-001', 'status.json'))
        require(first_status['status'] == 'PASS' and first_status['source_sha256'] == status['source_sha256'],
                'Approved core source.json identity mismatch')
        started = datetime.fromisoformat(first_status['started_utc'])
        status['resources'] = guard(home, source, started)
        from p3 import cua_so
        clock_path = Path(cua_so.__file__).resolve()
        require(sha(clock_path) == CLOCK_SOURCE_SHA256 and cua_so.US == 1_000_000,
                'CLOCK_STOP: approved timestamp source/US changed')
        require(any(clock_path.is_relative_to(Path(root).resolve()) for root in source['source_roots_remote']),
                'Clock code outside approved source repo')
        preflight = home / 'runs/preflight-002'
        environment = read(preflight / 'environment.json')
        inventory = read(preflight / 'inventory.json')
        verification = read(preflight / 'verification.json')
        require(environment['source_json_sha256'] == status['source_sha256']
                and inventory['status'] == verification['status'] == 'PASS', 'Preflight/source not PASS')
        lookup = {row['opaque_id']: row for row in inventory['cases']}
        require(len(lookup) == len(inventory['cases']) == 30
                and set(lookup) == {item['opaque_id'] for item in source['cases']}, 'Inventory source identity mismatch')
        status['contracts'] = {
            'clock_source': {'path': str(clock_path), 'sha256': CLOCK_SOURCE_SHA256, 'US': cua_so.US,
                             'metric_time': 'seconds', 'log_timestamp': 'seconds'},
            'parent_source': {'path': 'results/T-002/inspect_local.py', 'sha256': PARENT_SOURCE_SHA256, 'lines': [83, 84]},
            'duration_unit_source': {'path': 'results/T-002/the-rcaeval.md', 'sha256': CARD_SHA256,
                                     'section': '4', 'unit': 'OPEN_RAW_UNIT'},
            'preflight_sha256': {name: sha(preflight / name) for name in
                                 ('environment.json', 'inventory.json', 'verification.json')},
            'labels_or_proxy_used_in_statistics': False,
            'no_service_container_alias_assumed': True, 'coverage_unknown_without_collector_metadata': True}
        write(run / 'fixtures.json', fixtures(cua_so.US))
        update_manifest(run)
        cases = source['cases'][:1] if args.first else (source['cases'] if args.all else source['cases'][1:])
        if args.cases:
            wanted = args.cases.split(',')
            require(len(wanted) == len(set(wanted)) and set(wanted) <= {item['opaque_id'] for item in cases},
                    'Requested cases outside selected source scope or duplicate')
            cases = [item for item in cases if item['opaque_id'] in wanted]
        require(bool(cases), 'No selected source cases')
        for item in cases:
            oid = item['opaque_id']
            begin = time.perf_counter()
            status['active_case'] = oid
            def phase(name):
                status['resources'] = guard(home, source, started)
                status['phase'] = name
                write(run / 'status.json', status)
                progress(home, oid + ' ' + name)
            arrays, summary = case_context(item, source, lookup[oid], cua_so.US, phase)
            estimated_bytes = sum(a.nbytes for a in arrays.values()) + 4 * 2**20
            guard(home, source, started, projected=estimated_bytes)
            destination = run / (oid + '--context.npz')
            np.savez_compressed(destination, **arrays)
            with np.load(destination, allow_pickle=False) as archive:
                require(set(archive.files) == set(arrays), 'Output readback keys differ')
                for name, a in arrays.items():
                    equal = np.array_equal(archive[name], a, equal_nan=True) if a.dtype.kind in 'fc' else np.array_equal(archive[name], a)
                    require(equal, 'Output readback differs: ' + name)
            record = {'status': 'PASS', 'opaque_id': oid, 'source_sha256': status['source_sha256'],
                'output_npz': destination.name, 'sha256': sha(destination), 'bytes': destination.stat().st_size,
                'uncompressed_array_bytes': sum(a.nbytes for a in arrays.values()),
                'arrays': {name: {'shape': list(a.shape), 'dtype': str(a.dtype)} for name, a in arrays.items()},
                'wall_s': time.perf_counter() - begin,
                'rss_peak_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                'checks': {'source_hash_before_and_after': True, 'metric_grid_exact': True,
                    'timestamp_contract_and_field_relation': True, 'all_output_arrays_readback': True,
                    'trace_count_conservation': all(summary['trace']['checks'].values()),
                    'log_count_conservation_if_channel_present': all(summary['log'].get('checks', {}).values()),
                    'missing_log_not_zero': ('log_grid_row_count' in arrays) == ('logs.parquet' in item['files'])},
                'summary': summary}
            write(run / (oid + '--context.json'), record)
            status['cases'][oid] = {'status': 'PASS', 'record': oid + '--context.json',
                'output_npz': destination.name, 'sha256': record['sha256'],
                'wall_s': record['wall_s'], 'bytes': record['bytes']}
            status['units_completed'] += 1
            status['resources'] = guard(home, source, started)
            write(run / 'status.json', status)
            update_manifest(run)
            progress(home, 'PASS ' + oid + ' wall_s=' + str(round(record['wall_s'], 3)) + ' bytes=' + str(record['bytes']))
            del arrays, summary
        require(status['units_completed'] == len(cases), 'Context coverage incomplete')
        write(run / 'context-index.json', {'status': 'PASS', 'source_sha256': status['source_sha256'],
            'records': status['cases'], 'selected_case_count': len(cases),
            'interpretation': 'Descriptive observations only; no independent channel, physical onset, clean baseline or cause established; duration raw unit and request/collector coverage OPEN'})
        status['resources'] = guard(home, source, started)
        status['status'] = 'PASS'
    except BaseException as exc:
        status['status'] = 'STOPPED'
        status['error'] = type(exc).__name__ + ': ' + str(exc)
        traceback.print_exc()
        progress(home, 'STOP ' + status['error'])
        raise
    finally:
        status['wall_s'] = time.perf_counter() - t0
        status['ended_utc'] = datetime.now(timezone.utc).isoformat()
        write(run / 'status.json', status)
        update_manifest(run)
        progress(home, status['status'] + ' ' + args.run)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--first', action='store_true', help='First source case pilot only')
    selection.add_argument('--all', action='store_true', help='All cases; default is rest after pilot')
    parser.add_argument('--cases', help='Optional selected opaque IDs; incomplete units only')
    main(parser.parse_args())
