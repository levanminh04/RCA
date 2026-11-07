"""Meaningful H2 contract/integration checks; only generated telemetry is opened."""
import os
for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_k] = '1'
import copy
import importlib.util
import json
from pathlib import Path
import sys
import time
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
DEST = RUN/sys.argv[1]
DEST.mkdir(exist_ok=False)
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'results/T-054/scripts'), str(ROOT/'results/T-044/tests'),
                'D:/RCA-ext/src/RCAEval', 'D:/RCA-ext/src/baro', 'D:/RCA-ext/work/T-014/CIRCA',
                'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages']
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from bien_nhan import atomic, ref, fingerprint, normalized_digest, Blocked
from p3 import re3
from m1 import adapter, runner, chuoi, e4
import nguon
import worker
import cham

checks = []
started = time.monotonic()


def save():
    value = {'checks': checks, 'passed': sum(c['PASS'] for c in checks),
             'elapsed_s': time.monotonic()-started, 'telemetry': 'GENERATED_ONLY'}
    (DEST/'checks.json').write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def check(name, fn):
    begin = time.monotonic()
    try:
        detail = fn()
        checks.append({'name': name, 'PASS': True, 'elapsed_s': time.monotonic()-begin,
                       'detail': detail if isinstance(detail, (str, int, float, dict)) else None})
    except Exception as exc:
        checks.append({'name': name, 'PASS': False, 'elapsed_s': time.monotonic()-begin,
                       'error': repr(exc), 'traceback': traceback.format_exc()})
        save()
        raise
    save()
    print('PASS '+name, flush=True)


def equal(a, b):
    assert fingerprint(a) == fingerprint(b)


def reject(fn, error=(re3.ContractError, Blocked, KeyError, ValueError)):
    try:
        fn()
    except error:
        return
    raise AssertionError('invalid input was accepted')


def old_module(name, rel):
    spec = importlib.util.spec_from_file_location(name, RUN/'before'/rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


t = 1700000000
channels = {'cpu': 'tài nguyên', 'mem': 'tài nguyên', 'diskio': 'tài nguyên', 'socket': 'tài nguyên',
            'workload': 'lưu lượng', 'error': 'lỗi', 'latency-50': 'độ trễ', 'latency-90': 'độ trễ'}
profile = {'schema': 'RE3-OB-PROFILE-1', 'dataset': 'RE3-OB', 'status': 'DECLARED',
           'time_units': {'metric': 's', 'log': 's', 'span_start': 'us', 'span_duration': 'us'},
           'observation_r_ns': {'metric': 10**9, 'log': 10**9, 'trace': 1000},
           'inventory': ['a', 'b'], 'aliases': {}, 'metric_channels': channels,
           'log_rule': {'kieu': 'tu_khoa', 'tu_khoa': ['ERROR', 'FAIL', 'EXCEPTION']},
           'trace_status_kind': 'binary_error',
           'evidence': {k: 'GENERATED FIXTURE DECLARATION; NOT RE3 SOURCE EVIDENCE'
                        for k in ['time_units', 'observation_r_ns', 'inventory', 'aliases', 'metric_channels', 'log_rule']}}
times = list(range(t-310, t+311, 10))
metric = pd.DataFrame({'time': times})
for owner in ['a', 'b']:
    for k in channels:
        metric[owner+'_'+k] = [2+(i % 7)*.2+(8 if x >= t and owner == 'b' else 0) for i, x in enumerate(times)]
metric.loc[5, 'a_mem'] = np.nan
span_rows = []
for i, second in enumerate(range(t-300, t+300, 5)):
    a_start = second*10**6
    duration = 1000+(i % 5)*30+(9000 if second >= t else 0)
    for sid, par, owner, st, dur in [('01', '', 'a', a_start, duration+300), ('02', '01', 'b', a_start+100, duration)]:
        span_rows.append({'time': 'generated', 'traceID': f'{i:08d}', 'spanID': sid,
                          'parentSpanID': par, 'serviceName': owner, 'operationName': owner+'_op',
                          'methodName': owner+'_method', 'startTimeMillis': st//1000,
                          'startTime': st, 'duration': dur, 'statusCode': int(second >= t)})
traces = pd.DataFrame(span_rows)
logs = pd.DataFrame({'timestamp': [t-301, t-300, t-1, t, t+299, t+300],
                     'container_name': ['a', 'a', 'b', 'b', 'a', 'a'],
                     'message': ['INFO generated', 'INFO generated', None, 'ERROR generated', 'INFO generated', 'INFO generated']})
origin = atomic(DEST/'origin.json', {'schema': 'T054-GENERATED-FIXTURE', 'source': 'check_h2.py constants only'})
data_root = DEST/'synthetic-data'
data_root.mkdir()
files = {}
for name, table in [('metrics.parquet', metric), ('traces.parquet', traces), ('logs.parquet', logs)]:
    p = data_root/name
    table.to_parquet(p, index=False)
    files[name] = str(p)
profile_ref = atomic(DEST/'profile.json', profile)
payload = re3.read_case(files, t, profile)
data = adapter.ca_re3(payload, profile)
protocol_main = json.loads((ROOT/'results/T-054/protocol.json').read_bytes())
configs = protocol_main['configurations']
contract_ref = protocol_main['m1_contract_ref']


def normal_contract():
    assert payload['window']['rows_N'] == payload['window']['rows_A'] == 30
    assert len(payload['logs']) == 4
    assert payload['logs']['message'].iloc[1] == ''
    assert payload['traces']['traceID'].iloc[0] == '00000000'
    assert sum(r['a_mem'] is None for r in data['metrics']) == 1
    assert not any('severity' in r for r in data['logs'])
    assert data['params_ca']['coverage']['metric']['khoang'][0][0] == (t-310)*10**9
    assert all(r['timestamp'] >= (t-300)*10**9 for r in data['logs'])


check('reader_normal_window_null_ids_full_coverage_no_fake_severity', normal_contract)
for field in ['time_units', 'inventory', 'aliases', 'observation_r_ns', 'evidence', 'log_rule']:
    bad = copy.deepcopy(profile); bad.pop(field)
    check('missing_profile_'+field, lambda bad=bad: reject(lambda: re3.validate_profile(bad)))
for field in ['metric', 'log', 'span_start', 'span_duration']:
    bad = copy.deepcopy(profile); bad['time_units'][field] = 'OPEN'
    check('unknown_unit_'+field, lambda bad=bad: reject(lambda: re3.validate_profile(bad)))
check('missing_profile_blocks_before_any_file_read', lambda: reject(lambda: re3.read_case(
    {'metrics.parquet': 'MUST_NOT_OPEN'}, t, {}), re3.ContractError))
for unit in ['s', 'ms', 'us', 'ns']:
    def clocks(unit=unit):
        p = copy.deepcopy(profile)
        p['time_units']['metric'] = p['time_units']['log'] = unit
        mm, ll = metric.copy(), logs.copy()
        factor = 10**9//re3.FACTORS[unit]
        mm['time'] *= factor; ll['timestamp'] *= factor
        x = re3.prepare_tables(mm, traces, ll, t, p)
        for k in ['metric', 'traces', 'logs']:
            assert_frame_equal(payload[k], x[k])
    check('explicit_clock_'+unit, clocks)
for unit in ['ms', 'us', 'ns']:
    def span_clocks(unit=unit):
        p = copy.deepcopy(profile); p['time_units']['span_start'] = p['time_units']['span_duration'] = unit
        tr = traces.copy()
        if unit == 'ms':
            tr['startTime'] = tr['startTime']//1000
            tr['duration'] = tr['duration']//1000
            expected = traces.copy(); expected['duration'] = expected['duration']//1000*1000
            expected['startTime'] = expected['startTime']//1000*1000
        elif unit == 'ns':
            tr['startTime'] *= 1000; tr['duration'] *= 1000; expected = traces
        else:
            expected = traces
        actual = re3.prepare_tables(metric, tr, logs, t, p)
        normal = re3.prepare_tables(metric, expected, logs, t, profile)
        assert_frame_equal(actual['traces'], normal['traces'])
    check('explicit_span_clock_'+unit, span_clocks)


def exact_log_ns():
    p = copy.deepcopy(profile); p['time_units']['log'] = 'ns'
    ll = logs.copy(); ll['timestamp'] = ll['timestamp']*10**9
    ll.loc[3, 'timestamp'] += 1
    out = adapter.ca_re3(re3.prepare_tables(metric, traces, ll, t, p), p)
    assert any(r['timestamp'] == t*10**9+1 for r in out['logs'])


check('M1_log_ns_no_float_roundtrip', exact_log_ns)
for name, alter in [
    ('outside_owner', lambda m, tr, l, p: m.rename(columns={'a_cpu': 'foreign_cpu'})),
    ('unknown_suffix', lambda m, tr, l, p: m.rename(columns={'a_cpu': 'a_newmetric'})),
    ('alias_collision', lambda m, tr, l, p: p.update(inventory=['a'], aliases={'b': 'a'})),
    ('metric_duplicate_clock', lambda m, tr, l, p: m.__setitem__('time', [t]*len(m))),
    ('ambiguous_span_id', lambda m, tr, l, p: tr.__setitem__('traceID', ['same']*len(tr))),
    ('missing_trace_field', lambda m, tr, l, p: tr.drop(columns=['parentSpanID'], inplace=True)),
    ('wrong_resolution_bool', lambda m, tr, l, p: p['observation_r_ns'].update(log=True)),
]:
    def invalid(alter=alter):
        m, tr, l, p = metric.copy(), traces.copy(), logs.copy(), copy.deepcopy(profile)
        result = alter(m, tr, l, p)
        if isinstance(result, pd.DataFrame): m = result
        reject(lambda: re3.prepare_tables(m, tr, l, t, p))
    check('reject_'+name, invalid)


def boundaries():
    tr = traces.iloc[:4].copy()
    tr['traceID'] = ['one', 'two', 'three', 'four']
    tr['startTime'] = [(t-300)*10**6, (t-300)*10**6-1, t*10**6, (t+300)*10**6-1]
    tr['duration'] = [1, 1, 1, 1]
    out = re3.prepare_tables(metric, tr, logs, t, profile)
    assert out['traces']['traceID'].tolist() == ['one', 'three']


check('full_span_boundary_and_strict_upper_end', boundaries)
for arm in ['M1', 'bo-E1', 'bo-E2', 'bo-E5', 'C-a0', 'C-a1', 'T12-on']:
    def m1(arm=arm):
        case = copy.deepcopy(data)
        params = runner._params(configs[arm]['config'], case)
        params['tach_cd3'] = True
        if arm == 'T12-on':
            params['canh_tinh'] = {'revision': 'GENERATED GRAPH ONLY', 'canh': [['a', 'b']]}
        chuoi.CACHE = e4.CacheCong()
        result = chuoi.chay(case['spans'], case['metrics'], case['logs'], case['inventory'], case['aliases'], t, params)
        atomic(DEST/(arm+'-core.json'), result)
        assert result['status'] == 'OK', result.get('error')
        return {'status': result['status'], 'worlds': sorted(result['worlds'])}
    check('M1_RE3_profile_'+arm, m1)

# Default adapter parity against exact snapshots, generated data only.
from test_adapter import _re2, _nezha, U_S
from p3 import selector, nezha
old_adapter = old_module('m1._h2old_adapter', 'src/m1/adapter.py')
contract = json.loads((ROOT/'results/T-043/hop-dong.json').read_bytes())


def tt_default():
    allow, _, _ = _re2(DEST/'TT', t=t)
    al = selector.nap_allowlist(allow); oid = next(iter(al))
    equal(adapter.ca_re2tt(al, oid, t, DEST/'TT', contract, U_S),
          old_adapter.ca_re2tt(al, oid, t, DEST/'TT', contract, U_S))


check('TT_M1_adapter_default_exact', tt_default)


def ob_default():
    args = _nezha(DEST/'OB')
    allow = nezha.nap_allowlist(args[0]); oid = next(iter(allow))
    equal(adapter.ca_nezha(allow, oid, DEST/'OB', contract),
          old_adapter.ca_nezha(allow, oid, DEST/'OB', contract))


check('OB_M1_adapter_default_exact', ob_default)

# Real frozen baseline kernels on generated tables; compare complete native output.
from p3.adapters import baro, circa, tracerca, torai
old_baro = old_module('p3.adapters._h2old_baro', 'src/p3/adapters/baro.py')
old_circa = old_module('p3.adapters._h2old_circa', 'src/p3/adapters/circa.py')
old_trace = old_module('p3.adapters._h2old_trace', 'src/p3/adapters/tracerca.py')
old_torai = old_module('p3.adapters._h2old_torai', 'src/p3/adapters/torai.py')
check('BARO_default_complete_output_exact', lambda: equal(baro.chay(payload['metric'], t), old_baro.chay(payload['metric'], t)))
check('BARO_RE3_generic_preprocess_output_exact', lambda: equal(baro.chay(payload['metric'], t, dataset='re3-ob'), old_baro.chay(payload['metric'], t)))
check('TraceRCA_default_complete_output_exact', lambda: equal(tracerca.chay(payload['traces'], t), old_trace.chay(payload['traces'], t)))
check('TraceRCA_RE3_generic_output_exact', lambda: equal(tracerca.chay(payload['traces'], t, dataset='re3-ob'), old_trace.chay(payload['traces'], t)))
check('CIRCA_default_complete_two_outputs_exact', lambda: equal(circa.chay(payload['metric'], payload['traces'], t, 'ols'), old_circa.chay(payload['metric'], payload['traces'], t, 'ols')))
check('CIRCA_RE3_generic_output_exact', lambda: equal(circa.chay(payload['metric'], payload['traces'], t, 'ols', dataset='re3-ob'), old_circa.chay(payload['metric'], payload['traces'], t, 'ols')))
check('TORAI_default_filter_exact', lambda: assert_frame_equal(torai.chuan_bi_metric(metric), old_torai.chuan_bi_metric(metric)))


def torai_B():
    old = old_torai.chuan_bi_B(payload['metric'], payload['traces'], payload['logs'], t)
    new = torai.chuan_bi_B(payload['metric'], payload['traces'], payload['logs'], t)
    for a, b in zip(old[:4], new[:4]): assert_frame_equal(a, b)
    equal(old[4], new[4])
    ob = torai.chuan_bi_B(payload['metric'], payload['traces'], payload['logs'], t, chi_ts=False)
    assert len(ob[0].columns) > 1 and list(new[0].columns) == ['time']
    for a, b in zip(ob[1:4], new[1:4]): assert_frame_equal(a, b)
    return {'OB_metric_columns': len(ob[0].columns)-1}


check('TORAI_B_default_tables_exact_OB_metrics_retained', torai_B)

# Worker fixture route calls the real reader, wrappers and kernels, no grant to real data.
source = {'member_sha256': fingerprint('GENERATED MEMBER'), 't': t,
          'files': {name: dict(ref(path), path=name) for name, path in files.items()}}


def fixture_job(arm, kind):
    config = configs[arm]['config'] if arm in configs else {'fixture': 'generated baseline'}
    slot = {'dataset': 'RE3-OB', 'opaque_id': 'generated-case-token', 'member_sha256': source['member_sha256'],
            'arm': arm, 'view': 'main', 'seed': 0 if arm == 'torai_B' else None,
            'window': {'t': t, 'half_width_s': 300}, 'source_sha256': fingerprint(source),
            'config_sha256': fingerprint(config), 'environment_sha256': 'generated-only'}
    return {'kind': 'synthetic', 'fixture_route': kind, 'fixture_origin': origin, 'slot': slot,
            'data_root': str(data_root), 'source': source, 't': t, 'config': config,
            're3_profile_ref': profile_ref, 'inventory': profile['inventory'], 'm1_contract': contract_ref,
            'method_version': 'GENERATED KERNEL CHECK', 'code_pins': {}, 'pythonpath': []}


worker_results = {}
for arm, kind in [('M1', 'm1'), ('baro', 'baseline'), ('simplerca', 'baseline'),
                  ('microrank', 'baseline'), ('tracerca', 'baseline'), ('circa', 'baseline'), ('torai_B', 'torai_prep')]:
    def route(arm=arm, kind=kind):
        job = fixture_job(arm, kind)
        path = DEST/('worker-'+arm); path.mkdir()
        job_ref = atomic(path/'job.json', job)
        worker.main(job_ref['path'], str(path), 'GENERATED-WORKER-TOKEN')
        out = json.loads((path/('prepared.json' if kind == 'torai_prep' else 'result.json')).read_bytes())
        if kind == 'torai_prep':
            assert out['re3_profile_ref'] == profile_ref
        else:
            inv = json.loads((path/'invocation.json').read_bytes())
            assert inv['re3_profile_ref'] == profile_ref
            if arm == 'microrank':
                assert out['records'][0]['status'] == 'NO_EVIDENCE'
                assert out['records'][0]['method_status_raw'] == 'no_normal_traces'
            else:
                assert all(r['status'] == 'OK' for r in out['records']), [r.get('error') for r in out['records']]
        worker_results[arm] = {'job': job, 'path': path, 'output': out}
        return {'status': 'PREPARED' if kind == 'torai_prep' else [r['status'] for r in out['records']]}
    check('worker_generated_RE3_'+arm, route)

check('private_locator_dataframe_rejected', lambda: reject(lambda: worker.re3_private_input_check(
    pd.DataFrame({'message': [str(data_root/'logs.parquet')]}), fixture_job('baro', 'baseline'))))
check('private_identifier_nested_rejected', lambda: reject(lambda: worker.re3_private_input_check(
    {'signals': ['generated-case-token']}, fixture_job('baro', 'baseline'))))

# More integration checks, grant/source fixtures and separate held-out tables appended below.
save()
print(json.dumps({'PASS': True, 'checks': len(checks), 'destination': str(DEST)}), flush=True)
