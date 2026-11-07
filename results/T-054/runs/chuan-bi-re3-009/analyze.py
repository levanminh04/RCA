"""RE3 preparation: saved schema and synthetic values only; no telemetry reader."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))


def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(name, value):
    (RUN / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


evidence_path = 'results/T-054/runs/phan-xu-truoc-g3-007/bang-chung.json'
manifest = json.loads((ROOT / 'results/T-054/manifest-phan-xu-truoc-g3-007.json').read_text(encoding='utf-8'))
assert pin(ROOT / evidence_path) == manifest['outputs'][evidence_path]
evidence = json.loads((ROOT / evidence_path).read_text(encoding='utf-8'))['RE3']
requests = evidence['metadata_requests']
assert len(requests) == 90 and all(r['metadata_only'] and not r['values_read'] for r in requests)
groups = {}
for r in requests:
    if r['path'].endswith('/metrics.parquet'):
        columns = tuple(c['name'] for c in r['schema'] if c['name'] != 'time')
        groups.setdefault(columns, []).append(r['path'])
common = set.intersection(*[{c.rsplit('_', 1)[0] for c in cols} for cols in groups])
union = set.union(*[{c.rsplit('_', 1)[0] for c in cols} for cols in groups])
schema_groups = []
for i, (columns, files) in enumerate(groups.items(), 1):
    owners = sorted({c.rsplit('_', 1)[0] for c in columns})
    schema_groups.append({'id': f'metric-schema-{i}', 'files': files, 'columns': list(columns),
                          'column_count': len(columns), 'owner_tokens': owners,
                          'additional_to_common': sorted(set(owners) - common)})
save('inventory-schema.json', {
    'classification': 'FACT_SCHEMA_NAMES_ONLY_NOT_DEPLOYMENT_INVENTORY',
    'source': evidence_path + '#/RE3/metadata_requests', 'telemetry_opened': False,
    'common_owner_tokens': sorted(common), 'all_owner_tokens': sorted(union),
    'additional_owner_tokens': sorted(union - common), 'schema_groups': schema_groups,
    'cases_with_additional_tokens': sum(len(g['files']) for g in schema_groups if g['additional_to_common']),
    'do_not_infer': ['extra columns are non-null', 'extra columns are causal signals',
                     'all prefixes are deployed OB services', 'root labels define U',
                     'frontend-external aliases frontend', 'Nezha-OB architecture is RE3-OB deployment']})

# Production helpers on invented inputs: verify present behavior and mapping coverage.
import numpy as np
import pandas as pd
from p3.cua_so import cat_metric, cat_span, cat_log, tien_xu_ly_main, doi_ten_latency
from p3.adapters.torai import chuan_bi_metric
from circa_kien_truc.builder import metric_mapping, service_calls

checks = []


def check(name, condition, detail=None):
    checks.append({'name': name, 'PASS': bool(condition), 'detail': detail})
    assert condition, name


for g in schema_groups:
    frame = pd.DataFrame({c: [1., 2., 3., 4.] for c in g['columns']})
    frame.insert(0, 'time', [1699999998, 1699999999, 1700000000, 1700000001])
    old = chuan_bi_metric(frame)
    check(g['id'] + ':current_TORAI_TT_filter_loses_all_metrics', list(old.columns) == ['time'])
    candidate = doi_ten_latency(tien_xu_ly_main(frame, chi_ts=False))
    check(g['id'] + ':candidate_OB_filter_keeps_non_ts_metrics', len(candidate.columns) > 1,
          {'remaining': len(candidate.columns) - 1, 'synthetic_values_only': True})
    mapping = metric_mapping(g['columns'])
    check(g['id'] + ':CIRCA_suffix_mapping_covers_schema', all(x['status'] == 'mapped' for x in mapping))

t = 1700000000
mt = pd.DataFrame({'time': [t-301, t-300, t-1, t, t+299, t+300], 'neutral_cpu': range(6)})
check('metric_half_open_window', cat_metric(mt, t)['time'].tolist() == [t-300, t-1, t, t+299])
lg = pd.DataFrame({'timestamp': mt.time, 'container_name': ['neutral']*6, 'message': ['x']*6})
check('log_second_contract_half_open', cat_log(lg, t).timestamp.tolist() == [t-300, t-1, t, t+299])
tr = pd.DataFrame({'startTime': [(t-300)*10**6, (t-300)*10**6-1, t*10**6, (t+300)*10**6-1],
                   'duration': [1, 1, 1, 1], 'spanID': ['lo', 'before', 'at', 'end']})
check('trace_us_contract_full_span_window', cat_span(tr, t).spanID.tolist() == ['lo', 'at'])

# Exact arithmetic candidate, deliberately requiring an explicit unit declaration.
def to_ns(values, declared_unit):
    factors = {'s': 10**9, 'ms': 10**6, 'us': 1000, 'ns': 1}
    if declared_unit not in factors:
        raise ValueError('unit must be declared, not guessed')
    if any(isinstance(x, (bool, np.bool_)) or not isinstance(x, (int, np.integer)) for x in values):
        raise ValueError('integer timestamps required')
    return [int(x)*factors[declared_unit] for x in values]

for unit, v in [('s', t), ('ms', t*1000), ('us', t*10**6), ('ns', t*10**9)]:
    check('explicit_' + unit + '_exact_conversion', to_ns([v], unit) == [t*10**9])
for name, values, unit in [('undeclared', [t], None), ('float', [float(t)], 's'), ('boolean', [True], 's')]:
    try:
        to_ns(values, unit)
    except ValueError:
        check('reject_' + name, True)
    else:
        check('reject_' + name, False)

parents = pd.DataFrame([
    ['one', 'same', '', 'caller1', (t-2)*10**6],
    ['one', 'child', 'same', 'callee1', (t-1)*10**6],
    ['two', 'same', '', 'caller2', (t-2)*10**6],
    ['two', 'child', 'same', 'callee2', (t-1)*10**6],
], columns=['traceID', 'spanID', 'parentSpanID', 'serviceName', 'startTime'])
graph, report = service_calls(parents, t)
check('CIRCA_parent_lookup_scoped_by_trace', set(graph.edges) == {('caller1', 'callee1'), ('caller2', 'callee2')})
check('external_name_not_silently_merged', 'frontend-external' in common and 'frontend' in common)
save('synthetic-checks.json', {'scope': 'production preprocessing/window/graph helpers and explicit conversion prototype; NOT installed RE3 adapter or scientific results',
                               'telemetry_opened': False, 'checks': checks, 'passed': len(checks),
                               'source_pins': {str(p.relative_to(ROOT)): pin(p) for p in [
                                   ROOT/'src/p3/cua_so.py', ROOT/'src/p3/adapters/torai.py', ROOT/'src/circa_kien_truc/builder.py']}})
print(json.dumps({'schemas': len(groups), 'cases': sum(len(x) for x in groups.values()),
                  'owner_tokens_common': len(common), 'owner_tokens_union': len(union),
                  'additional_namespace_cases': sum(len(g['files']) for g in schema_groups if g['additional_to_common']),
                  'synthetic_checks_PASS': len(checks)}))
