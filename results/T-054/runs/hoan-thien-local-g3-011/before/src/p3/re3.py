"""RE3-OB input contract. Units/ownership are declared, never inferred from labels.

This module grants no data access. The task worker validates the independent grant
before calling read_case. prepare_tables is also usable with generated fixtures.
"""
import copy
import hashlib
from numbers import Integral
from pathlib import Path

import numpy as np
import pandas as pd

NS = 10**9
FACTORS = {'s': NS, 'ms': 10**6, 'us': 1000, 'ns': 1}
CHANNELS = {'cpu', 'mem', 'diskio', 'socket', 'workload', 'error', 'latency-50', 'latency-90'}
KINDS = {'tài nguyên', 'lưu lượng', 'lỗi', 'độ trễ'}
TRACE = {'time', 'traceID', 'spanID', 'serviceName', 'methodName', 'operationName',
         'parentSpanID', 'startTimeMillis', 'startTime', 'duration', 'statusCode'}
LOG = {'timestamp', 'container_name', 'message'}


class ContractError(ValueError):
    """Input/profile defect, never a method failure."""


def _integer(x):
    if isinstance(x, (bool, np.bool_)) or not isinstance(x, Integral):
        raise ContractError('RE3 requires integer timestamps/resolution')
    return int(x)


def validate_profile(profile):
    if not isinstance(profile, dict):
        raise ContractError('RE3 profile missing')
    required = {'schema', 'dataset', 'status', 'time_units', 'observation_r_ns', 'inventory',
                'aliases', 'metric_channels', 'log_rule', 'evidence'}
    if not required <= set(profile) or set(profile) - required - {'trace_status_kind'}:
        raise ContractError('RE3 profile missing/unknown fields')
    if (profile['schema'] != 'RE3-OB-PROFILE-1' or profile['dataset'] != 'RE3-OB'
            or profile['status'] != 'DECLARED'):
        raise ContractError('RE3 profile not declared for this dataset')
    units = profile['time_units']
    if not isinstance(units, dict) or set(units) != {'metric', 'log', 'span_start', 'span_duration'} or any(
            x not in FACTORS for x in units.values()):
        raise ContractError('RE3 unit must be explicitly s/ms/us/ns')
    resolution = profile['observation_r_ns']
    if not isinstance(resolution, dict) or set(resolution) != {'trace', 'log', 'metric'} or any(
            _integer(x) <= 0 for x in resolution.values()):
        raise ContractError('RE3 observation resolution missing/invalid')
    inventory = profile['inventory']
    if (not isinstance(inventory, list) or not inventory or any(not isinstance(x, str) or not x for x in inventory)
            or len(inventory) != len(set(inventory))):
        raise ContractError('RE3 inventory must be a unique explicit list')
    aliases = profile['aliases']
    if not isinstance(aliases, dict) or any(not isinstance(k, str) or not k or v not in inventory
                                          or (k in inventory and k != v) for k, v in aliases.items()):
        raise ContractError('RE3 alias target/chain/canonical collision')
    channels = profile['metric_channels']
    if not isinstance(channels, dict) or set(channels) != CHANNELS or any(x not in KINDS for x in channels.values()):
        raise ContractError('RE3 needs all eight declared metric channels')
    rule = profile['log_rule']
    if (not isinstance(rule, dict) or set(rule) != {'kieu', 'tu_khoa'} or rule['kieu'] != 'tu_khoa'
            or not isinstance(rule['tu_khoa'], list) or not rule['tu_khoa']
            or any(not isinstance(x, str) or not x for x in rule['tu_khoa'])):
        raise ContractError('RE3 explicit keyword log rule required; no inferred severity')
    evidence = profile['evidence']
    fields = {'time_units', 'observation_r_ns', 'inventory', 'aliases', 'metric_channels', 'log_rule'}
    if not isinstance(evidence, dict) or not fields <= set(evidence) or any(
            not isinstance(evidence[k], str) or not evidence[k].strip() for k in fields):
        raise ContractError('RE3 profile lacks source declarations')
    if profile.get('trace_status_kind') not in (None, 'binary_error'):
        raise ContractError('RE3 status interpretation not supported')
    return copy.deepcopy(profile)


def to_ns(values, unit):
    if unit not in FACTORS:
        raise ContractError('undeclared time unit')
    out = [_integer(x)*FACTORS[unit] for x in values]
    if any(x < 0 or x > np.iinfo(np.int64).max for x in out):
        raise ContractError('RE3 time outside supported int64 ns range')
    return out


def _exact(values, divisor):
    if any(x % divisor for x in values):
        raise ContractError('RE3 clock cannot be represented exactly in canonical unit')
    return [x//divisor for x in values]


def _owner(x, profile):
    if not isinstance(x, str) or not x:
        raise ContractError('missing RE3 owner')
    canonical = profile['aliases'].get(x, x)
    if canonical not in profile['inventory']:
        raise ContractError('RE3 owner outside declared inventory')
    return canonical


def _bounds(values):
    return [[min(values), max(values)]] if values else []


def _schema(df, columns):
    if set(df.columns) != columns or len(df.columns) != len(columns):
        raise ContractError('RE3 missing/unknown/duplicate schema columns')


def prepare_tables(metrics, traces, logs, t, profile):
    """Canonical metric seconds, span us, log seconds plus exact log ns for M1.

    Null metrics are not filled. Full-file observation bounds are retained separately
    from the selected window, without exporting paths or case labels to methods.
    """
    p = validate_profile(profile)
    t = _integer(t)
    lo, hi = (t-300)*NS, (t+300)*NS
    if t < 300:
        raise ContractError('RE3 boundary outside supported epoch')
    m, tr, lg = metrics.copy(deep=True), traces.copy(deep=True), logs.copy(deep=True)
    _schema(tr, TRACE)
    _schema(lg, LOG)
    if 'time' not in m or not m.columns.is_unique:
        raise ContractError('RE3 metric time/schema missing')
    names = {}
    owners = {}
    for c in m.columns:
        if c == 'time':
            continue
        if not isinstance(c, str) or '_' not in c or c.rsplit('_', 1)[1] not in CHANNELS:
            raise ContractError('RE3 unknown metric suffix')
        owner, suffix = c.rsplit('_', 1)
        canonical = _owner(owner, p)
        if canonical in owners and owners[canonical] != owner:
            raise ContractError('RE3 metric alias collision')
        owners[canonical] = owner
        names[c] = canonical+'_'+suffix
        if not pd.api.types.is_numeric_dtype(m[c].dtype) or pd.api.types.is_bool_dtype(m[c].dtype):
            raise ContractError('RE3 metric values must be numeric')
    mn = to_ns(m['time'], p['time_units']['metric'])
    if len(mn) != len(set(mn)) or mn != sorted(mn):
        raise ContractError('RE3 metric timestamps duplicate/out of order')
    m['time'] = _exact(mn, NS)
    m = m.rename(columns=names)
    starts = to_ns(tr['startTime'], p['time_units']['span_start'])
    durations = to_ns(tr['duration'], p['time_units']['span_duration'])
    ends = [a+b for a, b in zip(starts, durations)]
    if any(x > np.iinfo(np.int64).max for x in ends):
        raise ContractError('RE3 span end overflow')
    tr['startTime'], tr['duration'] = _exact(starts, 1000), _exact(durations, 1000)
    for c in ('traceID', 'spanID'):
        if any(not isinstance(x, str) or not x for x in tr[c]):
            raise ContractError('RE3 trace/span ID must be a nonempty string')
    if tr.duplicated(['traceID', 'spanID']).any():
        raise ContractError('RE3 ambiguous duplicate trace/span ID')
    tr['parentSpanID'] = tr['parentSpanID'].fillna('')
    if any(not isinstance(x, str) for x in tr['parentSpanID']):
        raise ContractError('RE3 parent ID must be string')
    if any(not isinstance(x, str) or not x for x in tr['operationName']):
        raise ContractError('RE3 operation name missing')
    if any(not pd.isna(x) and not isinstance(x, str) for x in tr['methodName']):
        raise ContractError('RE3 method name must be string/null')
    if any(not pd.isna(x) and (isinstance(x, (bool, np.bool_)) or not isinstance(x, (Integral, float, np.floating))
                               or not np.isfinite(x) or not float(x).is_integer()) for x in tr['statusCode']):
        raise ContractError('RE3 statusCode must be integer/null; semantics remain declared separately')
    tr['serviceName'] = [_owner(x, p) for x in tr['serviceName']]
    ln = to_ns(lg['timestamp'], p['time_units']['log'])
    lg['container_name'] = [_owner(x, p) for x in lg['container_name']]
    # Baselines consume seconds; M1 consumes the exact int64 clock, not this float.
    lg['timestamp'] = [x//NS if x % NS == 0 else x/NS for x in ln]
    lg['_timestamp_ns'] = ln
    lg['message'] = lg['message'].fillna('')
    if any(not isinstance(x, str) for x in lg['message']):
        raise ContractError('RE3 log message must be string/null')
    selected = {
        'metric': m.loc[[lo <= x < hi for x in mn]].reset_index(drop=True),
        'traces': tr.loc[[a >= lo and b < hi for a, b in zip(starts, ends)]].reset_index(drop=True),
        'logs': lg.loc[[lo <= x < hi for x in ln]].reset_index(drop=True)}
    coverage = {k: {'khoang': _bounds(x), 'r_ns': int(p['observation_r_ns'][k])}
                for k, x in [('metric', mn), ('trace', ends), ('log', ln)]}
    mt = selected['metric']['time']
    window = {'t': t, 'N': [t-300, t], 'A': [t, t+300],
              'rows_N': int((mt < t).sum()), 'rows_A': int((mt >= t).sum()),
              'spans_N': int((selected['traces']['startTime'] < t*10**6).sum()),
              'spans_A': int((selected['traces']['startTime'] >= t*10**6).sum()),
              'log_rows_N': int((selected['logs']['_timestamp_ns'] < t*NS).sum()),
              'log_rows_A': int((selected['logs']['_timestamp_ns'] >= t*NS).sum())}
    selected.update(window=window, coverage=coverage,
                    diagnostics={'full_rows': {'metric': len(m), 'trace': len(tr), 'log': len(lg)},
                                 'selected_rows': {k: len(v) for k, v in selected.items()},
                                 'clock': {'metric': 's', 'trace': 'us', 'log_exact': 'ns'}})
    return selected


def read_case(files, t, profile, expected=None):
    validate_profile(profile)  # before ANY telemetry I/O
    if set(files) != {'metrics.parquet', 'traces.parquet', 'logs.parquet'}:
        raise ContractError('RE3 requires exactly three signal files')
    if expected is not None and set(expected) != set(files):
        raise ContractError('RE3 file pins missing/extra')
    # The py38 TORAI method process validates profiles but only reads CSV.
    import pyarrow.parquet as pq
    tables, provenance = {}, {}
    for name in ('metrics.parquet', 'traces.parquet', 'logs.parquet'):
        path = Path(files[name])
        b = path.read_bytes()
        provenance[name] = {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
        if expected is not None and any(provenance[name][k] != expected[name].get(k) for k in ('bytes', 'sha256')):
            raise ContractError('RE3 bytes read differ from independently granted file pin')
        # Parse the exact bytes hashed above, avoiding a path re-open race.
        import pyarrow as pa
        tables[name] = pq.read_table(pa.BufferReader(b)).to_pandas()
    result = prepare_tables(tables['metrics.parquet'], tables['traces.parquet'], tables['logs.parquet'], t, profile)
    result['provenance'] = provenance
    return result
