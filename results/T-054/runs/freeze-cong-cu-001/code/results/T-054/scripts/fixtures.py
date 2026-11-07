"""Phản ví dụ tích hợp trên dữ liệu giả; không đọc telemetry test/dev."""
import copy
import json
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import patch

from bien_nhan import (ROOT, OUT, Blocked, atomic, fingerprint, ref, read_pin, events,
                       verify_envelope, timeout_classification)
from nguon import compare_labels, compare_sources, authorize, source_row
from cham import verify_snapshot, cd3_after_main
from dieu_phoi import exclusive, status, supervise, terminate_tree


def main(directory, readers=True):
    target = Path(directory).resolve()
    if not target.is_relative_to(OUT):
        raise Blocked('fixture output ngoài T054')
    target.mkdir(parents=True, exist_ok=False)
    checks = []

    def check(name, fn):
        fn(); checks.append(name)

    def denied(fn):
        try: fn()
        except (Blocked, PermissionError, FileExistsError): return
        raise AssertionError('đường sai không bị chặn')

    row = {'member_sha256': 'a' * 64, 't': 1000, 'ce_history': 'verified', 'files': {'x': {'path': 'fake/x', 'sha256': 'b' * 64, 'bytes': 1}}}
    runtime = {'dataset': 'RE2-TT', 'g1_revision': 'g1-fixture', 'cases': {'f1': row}}
    independent = {'dataset': 'RE2-TT', 'g1_revision': 'g1-fixture', 'cases_by_member': {'a' * 64: row}}
    check('source_independent_positive', lambda: compare_sources(runtime, independent, 'RE2-TT', 'g1-fixture'))
    for field, value in [('t', 1001), ('ce_history', 'insufficient'), ('member_sha256', 'c' * 64)]:
        bad = copy.deepcopy(runtime); bad['cases']['f1'][field] = value
        check('source_rehashed_swap_' + field, lambda b=bad: denied(lambda: compare_sources(b, independent, 'RE2-TT', 'g1-fixture')))
    with patch('pathlib.Path.is_file', side_effect=AssertionError('traversal before I/O')):
        bad = copy.deepcopy(row); bad['files']['x']['path'] = '../outside'
        check('traversal_before_payload', lambda: denied(lambda: source_row(bad, target)))
    lab = {'member_sha256': 'a' * 64, 'root': 'svc', 'fault': 'cpu', 'cell': ['RE2-TT', 'svc', 'cpu']}
    labels = {'dataset': 'RE2-TT', 'g1_revision': 'g1-fixture', 'alias_sha256': fingerprint({}), 'cases': {'f1': lab}}
    canonical = {'dataset': 'RE2-TT', 'g1_revision': 'g1-fixture', 'alias_sha256': fingerprint({}), 'by_member': {'a' * 64: lab}}
    check('label_independent_positive', lambda: compare_labels(labels, canonical, runtime, {}, ['svc', 'other']))
    for field, value in [('root', 'other'), ('fault', 'mem'), ('cell', ['RE2-TT', 'svc', 'mem'])]:
        bad = copy.deepcopy(labels); bad['cases']['f1'][field] = value
        check('label_rehash_poison_' + field, lambda b=bad: denied(lambda: compare_labels(b, canonical, runtime, {}, ['svc', 'other'])))
    for field in ('dataset', 'g1_revision', 'alias_sha256'):
        bad = copy.deepcopy(labels); bad[field] = 'wrong'
        check('label_' + field, lambda b=bad: denied(lambda: compare_labels(b, canonical, runtime, {}, ['svc'])))
    check('root_outside_U_blocks', lambda: denied(lambda: compare_labels(labels, canonical, runtime, {}, ['other'])))

    slot = {'dataset': 'SYNTHETIC', 'opaque_id': 'fixture-1', 'member_sha256': 'a' * 64,
            'arm': 'M1', 'view': 'main', 'seed': None, 'source_sha256': 'b' * 64,
            'window': [700, 1000, 1300], 'config_sha256': 'c' * 64, 'environment_sha256': 'd' * 64}
    job = {'slot': slot, 'kind': 'synthetic', 'executable': sys.executable, 'timeout_s': 15,
           'a4': True, 'synthetic_records': [{'status': 'NO_EVIDENCE', 'blocks': []}]}
    plan = {'schema': 'T054-PLAN-1', 'mode': 'synthetic', 'host_role': 'local', 'jobs': [job],
            'monitor': {'poll_s': .03, 'max_monitor_gap_s': 1, 'score_phases': ['method']}}
    invoke = {'schema': 'T054-INVOKE-1', 'token': 't1', 'slot_sha256': fingerprint(slot),
              **{k: slot[k] for k in ('source_sha256', 'window', 'seed', 'config_sha256', 'environment_sha256')},
              'normalized_input_sha256': 'e' * 64}
    env = {'schema': 'T054-RESULT-1', 'token': 't1', 'slot_sha256': fingerprint(slot),
           'invocation_sha256': fingerprint(invoke), 'records': job['synthetic_records'],
           'record_sha256': fingerprint(job['synthetic_records'])}
    check('envelope_positive', lambda: verify_envelope(env, invoke, slot, 't1'))
    for field in ('source_sha256', 'window', 'seed', 'config_sha256', 'environment_sha256'):
        bad = copy.deepcopy(invoke); bad[field] = 'changed'
        modified = dict(env, invocation_sha256=fingerprint(bad))
        check('invocation_rehash_wrong_' + field, lambda b=bad, e=modified: denied(lambda: verify_envelope(e, b, slot, 't1')))
    check('output_swap_before_assignment', lambda: denied(lambda: verify_envelope(dict(env, token='t2'), invoke, slot, 't1')))
    policy = {'max_monitor_gap_s': 1, 'score_phases': ['method']}
    phase = {'token': 't1', 'phase': 'method', 'state': 'start', 'invocation_sha256': 'x'}
    monitor = {'token': 't1', 'max_monitor_gap_s': .5, 'last_phase_sha256': fingerprint(phase)}
    for gap in (None, 1, 1.1):
        check('monitor_gap_blocks_' + str(gap), lambda g=gap: assert_equal(timeout_classification(slot, [phase], dict(monitor, max_monitor_gap_s=g), policy)[0], 'BLOCKED'))
    check('method_timeout_phase_positive', lambda: assert_equal(timeout_classification(slot, [phase], monitor, policy)[0], 'COMPLETE_UNVERIFIED'))
    check('self_declared_method_without_start_blocks', lambda: assert_equal(timeout_classification(slot, [], monitor, policy)[0], 'BLOCKED'))
    check('prepare_timeout_blocks', lambda: assert_equal(timeout_classification(slot, [dict(phase, phase='prepare')], monitor, policy)[0], 'BLOCKED'))
    check('missing_policy_blocks', lambda: assert_equal(timeout_classification(slot, [phase], monitor, {})[0], 'BLOCKED'))
    check('dev_grant_before_IO', lambda: denied(lambda: authorize(dict(plan, mode='dev'), {}, 'run')))
    check('test_g3_before_IO', lambda: denied(lambda: authorize(dict(plan, mode='test'), {}, 'run')))
    check('test_grant_separate', lambda: denied(lambda: authorize(dict(plan, mode='test'), {'g3': True}, 'run')))

    run = target / 'queue-ok'
    supervise(plan, run)
    state = status(run)
    check('worker_envelope_real_process', lambda: assert_equal(next(iter(state['jobs'].values()))['state'], 'VERIFIED'))
    initial_attempts = list(run.rglob('job.json'))
    supervise(plan, run)
    check('resume_does_not_duplicate_verified', lambda: assert_equal(initial_attempts, list(run.rglob('job.json'))))
    last = next(iter(state['jobs'].values()))
    receipt = read_pin(last['receipt'])
    result_pin = receipt['result']
    snapshot = {'slots': {fingerprint(slot): {'state': 'VERIFIED', 'receipt': last['receipt'], 'token': last['token']}}}
    check('verified_snapshot_positive', lambda: verify_snapshot(snapshot, [job]))
    blocked_snapshot = {'slots': {fingerprint(slot): {'state': 'BLOCKED'}}}
    check('blocked_A4_blocks_every_table', lambda: denied(lambda: verify_snapshot(blocked_snapshot, [job])))
    check('missing_seed_or_case_blocks_snapshot', lambda: denied(lambda: verify_snapshot({'slots': {}}, [job])))
    with exclusive(target / 'double-controller.lock'):
        check('two_controllers_exclusive_claim', lambda: denied(lambda: exclusive_probe(target / 'double-controller.lock')))

    slow = dict(job, scenario='slow_ok', sleep_s=3, timeout_s=15)
    recovering = dict(plan, jobs=[slow], directory=str(target / 'recovery'))
    plan_ref = atomic(target / 'recovery-plan.json', recovering)
    command = [sys.executable, '-B', str(OUT / 'scripts/p7.py'), '_supervise', '--plan', plan_ref['path'],
               '--sha256', plan_ref['sha256']]
    with (target / 'recovery-controller.stdout').open('wb') as so, (target / 'recovery-controller.stderr').open('wb') as se:
        controller = subprocess.Popen(command, stdout=so, stderr=se)
        started = time.monotonic()
        while not list((target / 'recovery').rglob('invocation.json')):
            if time.monotonic() - started > 8:
                controller.kill(); raise AssertionError('controller chưa phát worker')
            time.sleep(.03)
        controller.kill(); controller.wait(timeout=5)
    supervise(recovering, target / 'recovery')
    recovered = next(iter(status(target / 'recovery')['jobs'].values()))
    check('controller_restart_adopts_live_worker', lambda: assert_equal(recovered['state'], 'VERIFIED'))
    check('controller_restart_one_attempt', lambda: assert_equal(len(list((target / 'recovery').rglob('job.json'))), 1))
    check('controller_restart_one_method_start', lambda: assert_equal(sum(e.get('phase') == 'method' and e.get('state') == 'start'
          for e in events(Path(recovered['attempt']) / 'phases.jsonl')), 1))

    for scenario in ('before_method_timeout', 'method_timeout', 'partial', 'source_error'):
        j = dict(job, scenario=scenario, sleep_s=4, timeout_s=.7 if 'timeout' in scenario else 10)
        pl = dict(plan, jobs=[j])
        d = target / scenario
        supervise(pl, d)
        s = next(iter(status(d)['jobs'].values()))
        check('operational_' + scenario, lambda s=s: assert_equal(s['state'], 'BLOCKED'))
        check('retain_attempt_' + scenario, lambda d=d: assert_equal(len(list(d.rglob('job.json'))), 1))

    mainseal = atomic(target / 'main-seal.json', {'records': {'TT|case|M1|main|None': {'extra': {'dau_vao_cd3': {}}}}})
    before = read_pin(mainseal)
    check('cd3_failure_retains_main', lambda: assert_equal(cd3_after_main(mainseal, 'TT|case|M1|main|None', lambda _: 1/0)['trang_thai'], 'ERROR'))
    check('cd3_main_unchanged', lambda: assert_equal(read_pin(mainseal), before))
    check('cd3_wrong_lookup_blocks', lambda: denied(lambda: cd3_after_main(mainseal, 'wrong', lambda _: {})))

    sys.path[:0] = [str(ROOT / 'results/T-052/scripts'), str(ROOT / 'src')]
    from thong_ke import e04
    from a4_v2 import ob_pass, cell_sign_exact
    from fractions import Fraction
    check('strict_E04_boundary', lambda: assert_equal(e04({'lo': -.05, 'hi': .1})['pass_formula'], False))
    check('degenerate_E04_no_transfer', lambda: assert_equal(e04({'lo': 0., 'hi': 0.})['transfer_OB_alpha'], .025))
    check('OB_exact_threshold_inclusive', lambda: assert_equal(ob_pass(Fraction(1, 40), Fraction(1, 40)), True))
    check('zero_cells_keep_sign_denominator', lambda: assert_equal(cell_sign_exact({'a': Fraction(0), 'b': Fraction(1)}, {'a': 'a', 'b': 'b'})['p_exact'], Fraction(1, 2)))

    # Tuyến đọc/cắt và M1 thật trên parquet/CSV tự sinh, không là pilot dev.
    sys.path.insert(0, str(ROOT / 'results/T-044/tests'))
    from test_adapter import _re2, _nezha, U_S
    from p3 import nezha
    from bien_nhan import digest
    generated = target / 'synthetic-data'
    origin = atomic(generated / 'origin.json', {'schema': 'T054-GENERATED-FIXTURE',
                    'generator': 'results/T-044/tests/test_adapter.py:_re2,_nezha'})
    for name, data, expected_status in [('dag', {'canh': [['x', 'y']], 'diem': {'x': [1, 1], 'y': [2, 1]}, 'dich': ['x']}, 'OK'),
            ('cyclic', {'canh': [['x', 'y'], ['y', 'x']], 'diem': {'x': [1, 1], 'y': [2, 1]}, 'dich': ['x']}, 'UNSUPPORTED_CYCLIC'),
            ('no-target', {'canh': [['x', 'y']], 'diem': {'x': [1, 1], 'y': [2, 1]}, 'dich': []}, 'NO_TARGET')]:
        key = 'RE2-TT|fixture-0123456789|M1|main|None'
        sr = atomic(target / ('cd3-main-' + name + '.json'), {'records': {key: {'extra': {'dau_vao_cd3': data}}}})
        s = dict(slot, dataset='RE2-TT', arm='C-d3', source_sha256=fingerprint({'seal': sr['sha256'], 'key': key}))
        cj = dict(job, slot=s, fixture_route='cd3', fixture_origin=origin, data_root=str(generated),
                  main_seal=sr, main_key=key)
        d = target / ('cd3-worker-' + name); d.mkdir()
        jp = atomic(d / 'job.json', cj)
        done = subprocess.run([sys.executable, '-B', str(OUT / 'scripts/worker.py'), jp['path'], str(d), 'cd3-fixture'],
                              capture_output=True, timeout=15)
        (d / 'stdout.txt').write_bytes(done.stdout); (d / 'stderr.txt').write_bytes(done.stderr)
        assert done.returncode == 0, done.stderr
        result = verify_envelope(read_pin(ref(d / 'result.json')), read_pin(ref(d / 'invocation.json')), s, 'cd3-fixture')
        check('real_cd3_worker_' + name, lambda r=result, st=expected_status: assert_equal(r[0]['status'], st))
        check('real_cd3_worker_preserves_main_' + name, lambda sr=sr: read_pin(sr))
    tt_epoch = 1700000000
    ptt, _, _ = _re2(generated, t=tt_epoch)
    pob, tns = _nezha(generated)
    protocol = json.loads((ROOT / 'results/T-052/giao-thuc-p7-a-003.json').read_bytes())
    for ds, al, universe in ([('RE2-TT', ptt, U_S), ('Nezha-OB', pob, nezha.UNIVERSE)] if readers else []):
        sr = json.loads(al.read_bytes())['cases'][0]
        sr.pop('opaque_id', None); sr.pop('case_dir', None)
        sr['member_sha256'] = 'a' * 64
        for v in sr['files'].values():
            v['bytes'] = (generated / v['path']).stat().st_size
        if ds == 'RE2-TT': sr.update(t=tt_epoch, ce_history='verified')
        for arm in ('M1', 'C-a0', 'C-a1', 'bo-E1', 'bo-E2', 'bo-E5', 'T12-on', 'simplerca'):
            config = protocol['configurations'].get(arm, {'sha256': 'f' * 64, 'config': {}})
            s = dict(slot, dataset=ds, arm=arm, opaque_id='fixture-0123456789',
                     source_sha256=fingerprint(sr), config_sha256=config['sha256'],
                     window={'t': tt_epoch if ds == 'RE2-TT' else tns // 10**9, 'half_width_s': 300})
            item = dict(job, slot=s, fixture_route='baseline' if arm == 'simplerca' else 'm1',
                        fixture_origin=origin, source=sr, data_root=str(generated), inventory=universe,
                        t=tt_epoch if ds == 'RE2-TT' else tns // 10**9, config=config['config'],
                        pythonpath=['D:/RCA-ext/src/RCAEval', 'D:/RCA-ext/src/baro', 'D:/RCA-ext/work/T-014/CIRCA',
                                    'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages'],
                        m1_contract=ref(ROOT / 'results/T-043/hop-dong.json'),
                        static_snapshot=protocol['snapshots'][ds], method_version='src/simplerca (T-017, M4)')
            d = target / ('reader-' + ds + '-' + arm)
            d.mkdir()
            jp = atomic(d / 'job.json', item)
            completed = subprocess.run([sys.executable, '-B', str(OUT / 'scripts/worker.py'), jp['path'], str(d), 'fixture-route'],
                                       capture_output=True, timeout=45)
            (d / 'stdout.txt').write_bytes(completed.stdout); (d / 'stderr.txt').write_bytes(completed.stderr)
            assert completed.returncode == 0, (ds, arm, completed.stderr.decode('utf-8', errors='replace')[-1800:])
            recs = verify_envelope(read_pin(ref(d / 'result.json')), read_pin(ref(d / 'invocation.json')), s, 'fixture-route')
            check('actual_reader_and_core_' + ds + '_' + arm, lambda r=recs: assert_equal(r[0]['status'], 'OK'))
            if arm == 'simplerca':
                check('M4_variant_' + ds, lambda r=recs: assert_equal(r[0]['variant'], 'M4'))
            else:
                check('separate_cd3_' + ds + '_' + arm, lambda r=recs: assert_equal('C-d3' in r[0]['extra']['doi_chung'], False))

    atomic(target / 'summary.json', {'checks': checks, 'count': len(checks), 'PASS': True,
           'scope': 'synthetic transport/source/labels/phase/queue/A4 boundary; no scientific pilot',
           'test_opened': False, 'real_methods_on_dev': False})
    print(json.dumps({'PASS': True, 'checks': len(checks), 'output': str(target)}, ensure_ascii=False))


def assert_equal(a, b):
    assert a == b, (a, b)


def report_checks(target, reader_source):
    """Record transport tổng hợp quanh output lõi trên dữ liệu giả; không phải baseline pilot."""
    from cham import evaluate
    target = Path(target).resolve(); target.mkdir(parents=True, exist_ok=False)
    reader_source = Path(reader_source).resolve()
    if not reader_source.is_relative_to(OUT / 'runs'):
        raise Blocked('nguồn fixture ngoài T054')
    jobs, slots = [], {}
    runtimes, labels, canonicals, inventories = {}, {}, {}, {}
    for ds in ('RE2-TT', 'Nezha-OB'):
        base_dir = reader_source / ('reader-' + ds + '-simplerca')
        base_job = json.loads((base_dir / 'job.json').read_bytes())
        inventories[ds] = base_job['inventory']
        oid = base_job['slot']['opaque_id']; member = base_job['slot']['member_sha256']
        root = 'R' if ds == 'RE2-TT' else 'cartservice'
        lr = {'member_sha256': member, 'root': root, 'fault': 'synthetic', 'cell': [ds, root, 'synthetic']}
        rt = {'dataset': ds, 'g1_revision': 'fixture-g1', 'cases': {oid: {'member_sha256': member}}}
        runtimes[ds] = rt
        labels[ds] = atomic(target / (ds + '-labels.json'), {'dataset': ds, 'g1_revision': 'fixture-g1',
                       'alias_sha256': fingerprint({}), 'cases': {oid: lr}})
        canonicals[ds] = atomic(target / (ds + '-canonical.json'), {'dataset': ds, 'g1_revision': 'fixture-g1',
                           'alias_sha256': fingerprint({}), 'by_member': {member: lr}})
        for arm in ('M1', 'C-a0', 'C-a1', 'bo-E1', 'bo-E2', 'bo-E5', 'T12-on',
                    'baro', 'simplerca', 'tracerca', 'microrank', 'circa', 'torai_B'):
            family = arm in ('M1', 'C-a0', 'C-a1', 'bo-E1', 'bo-E2', 'bo-E5', 'T12-on')
            raw_path = reader_source / ('reader-' + ds + '-' + (arm if family else 'simplerca')) / 'result.json'
            actual = json.loads(raw_path.read_bytes())['records'][0]
            seeds = (0, 1, 2) if ds == 'RE2-TT' and arm == 'torai_B' else (None,)
            for seed in seeds:
                s = dict(base_job['slot'], arm=arm, seed=seed)
                record = copy.deepcopy(actual)
                if family:
                    records = [record]
                else:
                    record.update(method='torai' if arm == 'torai_B' else arm, seed=seed,
                                  variant={'baro': 'native', 'simplerca': 'M4', 'tracerca': 'finite',
                                           'microrank': 'full', 'circa': 'ols+rht_da', 'torai_B': 'B'}[arm])
                    records = [record]
                    if ds == 'Nezha-OB' and arm in ('circa', 'torai_B'):
                        record.update(status='UNSUPPORTED', blocks=[], entity_ranking=[], ranking=[])
                    if ds == 'RE2-TT' and arm == 'circa':
                        records.append(dict(record, variant='ols+rht'))
                j = {'kind': 'synthetic', 'slot': s, 'a4': arm == 'M1' or arm == ('torai_B' if ds == 'RE2-TT' else 'simplerca')}
                key = fingerprint(s); token = 'synthetic-report'
                inv = {'schema': 'T054-INVOKE-1', 'token': token, 'slot_sha256': key,
                       **{k: s[k] for k in ('config_sha256', 'source_sha256', 'environment_sha256', 'window', 'seed')},
                       'normalized_input_sha256': 'e' * 64}
                result = {'schema': 'T054-RESULT-1', 'token': token, 'slot_sha256': key,
                          'invocation_sha256': fingerprint(inv), 'records': records, 'record_sha256': fingerprint(records)}
                ip = atomic(target / key / 'invocation.json', inv)
                rp = atomic(target / key / 'result.json', result)
                receipt = atomic(target / key / 'receipt.json', {'job_sha256': fingerprint(j), 'invocation': ip, 'result': rp})
                slots[key] = {'state': 'VERIFIED', 'receipt': receipt, 'token': token}
                jobs.append(j)
    plan = {'mode': 'synthetic', 'jobs': jobs, 'inventories': inventories}
    snapshot = {'schema': 'T054-SNAPSHOT-1', 'plan_sha256': fingerprint(plan), 'slots': slots}
    result = evaluate(snapshot, plan, labels, canonicals, runtimes, {k: {} for k in runtimes}, inventories, target / 'report')
    table = json.loads((target / 'report/tables.json').read_bytes())
    assert len(table['regions']) == 4 and len(table['position_N']) == 2
    assert {r['arm'] for r in table['rows']} >= {'M1', 'C-a0', 'C-a1', 'C-c', 'C-g', 'C-d1', 'C-d2', 'circa_rht_aux'}
    assert all(r['seed_count'] == 3 for r in table['rows'] if r['dataset'] == 'RE2-TT' and r['arm'] == 'torai_B')
    atomic(target / 'summary.json', {'PASS': True, 'slots': len(slots), 'rows': len(table['rows']),
          'regions': len(table['regions']), 'positions': len(table['position_N']),
          'scope': 'synthetic labels + synthetic baseline records + real M1 on generated data; not scientific pilot'})
    print(json.dumps({'PASS': True, 'report_rows': len(table['rows']), 'output': str(target)}))


def exclusive_probe(path):
    with exclusive(path):
        pass


if __name__ == '__main__':
    try:
        if '--reports-from' in sys.argv:
            report_checks(sys.argv[1], sys.argv[sys.argv.index('--reports-from') + 1])
        else:
            main(sys.argv[1], readers='--transport-only' not in sys.argv)
    except BaseException as exc:
        import traceback
        d = Path(sys.argv[1])
        if d.exists():
            atomic(d / 'fixture-failure.json', {'type': type(exc).__name__, 'traceback': traceback.format_exc()})
        raise
