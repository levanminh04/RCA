"""Remaining edge/supervisor/timeout checks, all generated or mocked process receipts."""
from pathlib import Path
import sys
import copy
import json
import hashlib
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
OUT = RUN/sys.argv[1]
OUT.mkdir(exist_ok=False)
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'results/T-054/scripts'),
                'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages']
import pandas as pd
from p3 import re3
from m1 import adapter
import worker
import dieu_phoi
import bien_nhan as receipts
from bien_nhan import ref, atomic, read_pin, fingerprint, Blocked

checks = []


def check(name, fn):
    try:
        result = fn()
        checks.append({'name': name, 'PASS': True, 'detail': result if isinstance(result, dict) else None})
    except Exception as e:
        checks.append({'name': name, 'PASS': False, 'error': repr(e), 'traceback': traceback.format_exc()})
        (OUT/'checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
        raise
    (OUT/'checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS '+name, flush=True)


def reject(fn):
    try: fn()
    except (Blocked, re3.ContractError, ValueError): return
    raise AssertionError('invalid input accepted')


base = RUN/'synthetic-004'
job = read_pin(ref(base/'worker-baro/job.json'))
p = read_pin(job['re3_profile_ref'])
files = {k: str(Path(job['data_root'])/v['path']) for k, v in job['source']['files'].items()}
m = pd.read_parquet(files['metrics.parquet'])
tr = pd.read_parquet(files['traces.parquet'])
lg = pd.read_parquet(files['logs.parquet'])
t = job['t']
evidence_path = ROOT/'results/T-054/runs/phan-xu-truoc-g3-007/bang-chung.json'
manifest = read_pin(ref(ROOT/'results/T-054/manifest-phan-xu-truoc-g3-007.json'))
assert ref(evidence_path)['sha256'] == manifest['outputs'][str(evidence_path.relative_to(ROOT)).replace('\\','/')]['sha256']
evidence = json.loads(evidence_path.read_bytes())['RE3']['metadata_requests']
schemas = {tuple(c['name'] for c in item['schema'] if c['name'] != 'time') for item in evidence if item['path'].endswith('/metrics.parquet')}
for i, columns in enumerate(sorted(schemas)):
    def schema(columns=columns):
        profile = copy.deepcopy(p)
        profile['inventory'] = sorted({'a', 'b'} | {c.rsplit('_', 1)[0] for c in columns})
        metrics = pd.DataFrame({c: [1., 2., float('nan'), 3.] for c in columns})
        metrics.insert(0, 'time', [t-2, t-1, t, t+1])
        payload = re3.prepare_tables(metrics, tr, lg, t, profile)
        case = adapter.ca_re3(payload, profile)
        assert len(case['params_ca']['nguon_metric']) == len(columns)
        assert all(case['metrics'][2][c] is None for c in columns)
        return {'schema_columns': len(columns), 'profile': 'GENERATED SCHEMA-CONFORMANCE ONLY; NOT SELECTED REAL U'}
    check('all_columns_schema_'+str(i+1), schema)


def whole_second_trace_unit():
    pr = copy.deepcopy(p); pr['time_units']['span_start'] = pr['time_units']['span_duration'] = 's'
    tr1 = tr.iloc[:1].copy(); tr1['startTime'] = t; tr1['duration'] = 1
    out = re3.prepare_tables(m, tr1, lg, t, pr)
    assert out['traces'].iloc[0]['startTime'] == t*10**6
    assert out['traces'].iloc[0]['duration'] == 10**6


check('declared_seconds_trace_exact', whole_second_trace_unit)
def lossy_clock():
    pr = copy.deepcopy(p); pr['time_units']['span_start'] = 'ns'
    tr1 = tr.copy(); tr1['startTime'] = tr1['startTime']*1000+1
    reject(lambda: re3.prepare_tables(m, tr1, lg, t, pr))
check('reject_lossy_ns_to_us', lossy_clock)
for v in [True, 1.5, -1, 2**64]:
    check('reject_clock_'+str(v), lambda v=v: reject(lambda: re3.to_ns([v], 'ns')))


def ambiguous_metric_owner():
    pr = copy.deepcopy(p); pr['inventory'] = ['name_with_underscore', 'b']; pr['aliases'] = {'a': 'name_with_underscore'}
    payload = re3.prepare_tables(m, tr, lg, t, pr)
    reject(lambda: adapter.ca_re3(payload, pr))
check('M1_unsupported_metric_delimiter_blocks_instead_of_wrong_owner', ambiguous_metric_owner)


def empty_sources():
    out = re3.prepare_tables(m.iloc[:0], tr.iloc[:0], lg.iloc[:0], t, p)
    case = adapter.ca_re3(out, p)
    assert not case['metrics'] and not case['spans'] and not case['logs']
    assert all(not x['khoang'] for x in case['params_ca']['coverage'].values())
check('empty_sources_no_invented_rows_or_coverage', empty_sources)
for name, column, value in [('method_type', 'methodName', 7), ('status_type', 'statusCode', 'error')]:
    def invalid_field(column=column, value=value):
        tt = tr.copy(); tt[column] = tt[column].astype(object); tt.loc[0, column] = value
        reject(lambda: re3.prepare_tables(m, tt, lg, t, p))
    check('reject_trace_'+name, invalid_field)
def boolean_metric():
    mm = m.copy(); mm['a_cpu'] = True
    reject(lambda: re3.prepare_tables(mm, tr, lg, t, p))
check('reject_boolean_metric', boolean_metric)
def wrong_bytes_before_parquet():
    expected = copy.deepcopy(job['source']['files'])
    expected['metrics.parquet']['sha256'] = '0'*64
    with patch('pyarrow.parquet.read_table', side_effect=AssertionError('parser must not be reached')):
        reject(lambda: re3.read_case(files, t, p, expected=expected))
check('changed_source_bytes_block_before_parquet_parse', wrong_bytes_before_parquet)
def pinned_reader_positive():
    out = re3.read_case(files, t, p, expected=job['source']['files'])
    assert all(out['provenance'][name]['sha256'] == meta['sha256'] for name,meta in job['source']['files'].items())
check('exact_bytes_read_bound_to_granted_pins', pinned_reader_positive)

# Test receiver on copies of a real generated successful attempt.
circa = RUN/'integration-001/worker-circa'
cjob = read_pin(ref(circa/'job.json'))
inv = read_pin(ref(circa/'invocation.json'))
envelope = read_pin(ref(circa/'result.json'))
def receiver_mutation(name, mutate):
    j, x, v = copy.deepcopy(cjob), copy.deepcopy(envelope), copy.deepcopy(inv)
    mutate(j, x, v)
    x['record_sha256'] = fingerprint(x['records'])
    x['invocation_sha256'] = fingerprint(v)
    d = OUT/name; d.mkdir()
    atomic(d/'result.json', x); atomic(d/'invocation.json', v)
    reject(lambda: dieu_phoi.verify_attempt(d, j, 'GENERATED-CONTINUATION'))
check('CIRCA_receiver_missing_variant', lambda: receiver_mutation('missing-variant', lambda j,x,v:x['records'].pop()))
check('CIRCA_receiver_wrong_current', lambda: receiver_mutation('wrong-current', lambda j,x,v:x['records'][0]['window'].update(circa_current=t+999)))

# Only the output-construction layer is mocked here. No real process is killed.
# Classification still rejects pre-method/missing-observation conditions separately.
def timeout_variants(dataset, expected):
    dest = OUT/('timeout-'+dataset); dest.mkdir()
    j = copy.deepcopy(cjob); j['slot']['dataset'] = dataset
    invocation = dict(inv, slot_sha256=fingerprint(j['slot']))
    atomic(dest/'invocation.json', invocation)
    atomic(dest/'timeout.json', {'fixture': 'generated monitor receipt'})
    atomic(dest/'launch.json', {'fixture': 'generated launch receipt'})
    atomic(dest/'phases.jsonl', {})
    j['failure_policy_ref'] = {'fixture': 'mocked policy'}
    phases = [{'invocation_sha256': fingerprint(invocation)}]
    with patch('bien_nhan.failure_policy', return_value={'monitor': {}}), patch('bien_nhan.events', return_value=phases), \
            patch('bien_nhan.timeout_classification', return_value=('COMPLETE_UNVERIFIED', 'DECLARED_METHOD_TIMEOUT')), \
            patch('bien_nhan.verify_method_failure', return_value=True):
        receipts.finalize_timeout(dest, j, 'GENERATED-CONTINUATION')
    result = read_pin(ref(dest/'result.json'))
    assert [r['variant'] for r in result['records']] == expected
    assert all(r['status'] == 'TIMEOUT' for r in result['records'])
    return {'dataset': dataset, 'variants': expected, 'mocked': 'classification and process receipts only'}
check('CIRCA_RE3_timeout_two_variants', lambda: timeout_variants('RE3-OB', ['ols+rht_da', 'ols+rht']))
check('CIRCA_TT_timeout_unchanged', lambda: timeout_variants('RE2-TT', ['ols+rht_da', 'ols+rht']))
check('CIRCA_Nezha_timeout_unchanged', lambda: timeout_variants('Nezha-OB', ['ols+rht_da']))
atomic(OUT/'summary.json', {'PASS': True, 'checks': len(checks), 'telemetry': 'GENERATED_ONLY',
                           'timeout_mock_scope': 'constructor only; no claim to have tested actual kill/monitor in this run'})
print(json.dumps({'PASS': True, 'checks': len(checks)}), flush=True)
