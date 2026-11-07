"""Finish worker, grant and held-out table checks using generated fixture004."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import copy
import json
from pathlib import Path
import sys
import time
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
BASE = RUN/'synthetic-004'
OUT = RUN/sys.argv[1]
OUT.mkdir(exist_ok=False)
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'results/T-054/scripts'), 'D:/RCA-ext/src/RCAEval',
                'D:/RCA-ext/src/baro', 'D:/RCA-ext/work/T-014/CIRCA',
                'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages']
from bien_nhan import atomic, ref, read_pin, fingerprint, Blocked, verify_envelope, events
import worker
import nguon
import cham
import dieu_phoi
from p3 import re3
import pandas as pd

checks = []


def check(name, fn):
    if len(sys.argv) > 2 and sys.argv[2] == 'metadata' and name.startswith('worker_RE3_'):
        previous = RUN/'integration-001/checks.json'
        prior = json.loads(previous.read_bytes())
        assert any(r['name'] == name and r['PASS'] for r in prior)
        checks.append({'name': name, 'PASS': True, 'reused_from': ref(previous), 'rerun': False})
        return
    start = time.monotonic()
    try:
        detail = fn()
        checks.append({'name': name, 'PASS': True, 'seconds': time.monotonic()-start,
                       'detail': detail if isinstance(detail, (str, dict, int)) else None})
    except Exception as exc:
        checks.append({'name': name, 'PASS': False, 'error': repr(exc), 'traceback': traceback.format_exc()})
        (OUT/'checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
        raise
    (OUT/'checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS '+name, flush=True)


def reject(fn, errors=(Blocked, re3.ContractError, ValueError, KeyError)):
    try:
        fn()
    except errors:
        return
    raise AssertionError('invalid contract accepted')


template = json.loads((BASE/'worker-baro/job.json').read_bytes())
profile = read_pin(template['re3_profile_ref'])
files = nguon.source_row(template['source'], template['data_root'])
payload = re3.read_case(files, template['t'], profile)
atomic(OUT/'reused-fixtures.json', {'checks004': ref(BASE/'checks.json'),
                                  'source_refs': template['source']['files'],
                                  'reason': 'continue new/unresolved integration checks; no rerun of48 accepted checks004'})

for arm, route in [('microrank', 'baseline'), ('tracerca', 'baseline'), ('circa', 'baseline'), ('torai_B', 'torai_prep')]:
    def run(arm=arm, route=route):
        job = copy.deepcopy(template)
        job['slot']['arm'] = arm; job['slot']['seed'] = 0 if arm == 'torai_B' else None
        job['fixture_route'] = route
        dest = OUT/('worker-'+arm); dest.mkdir()
        p = atomic(dest/'job.json', job)
        worker.main(p['path'], str(dest), 'GENERATED-CONTINUATION')
        result = read_pin(ref(dest/('prepared.json' if route == 'torai_prep' else 'result.json')))
        if route == 'torai_prep':
            assert result['re3_profile_ref'] == template['re3_profile_ref']
            assert len(pd.read_csv(result['tables']['metric']['path']).columns) > 1
        else:
            inv = read_pin(ref(dest/'invocation.json'))
            verify_envelope(result, inv, job['slot'], 'GENERATED-CONTINUATION')
            assert inv['re3_profile_ref'] == job['re3_profile_ref']
            if arm == 'microrank':
                assert result['records'][0]['status'] == 'NO_EVIDENCE'
                assert result['records'][0]['method_status_raw'] == 'no_normal_traces'
            else:
                assert all(r['status'] == 'OK' for r in result['records']), [r.get('error') for r in result['records']]
            if arm == 'circa':
                assert [r['variant'] for r in result['records']] == ['ols+rht_da', 'ols+rht']
                dieu_phoi.verify_attempt(dest, job, 'GENERATED-CONTINUATION')
        return {'result': 'PREPARED' if route == 'torai_prep' else [r['status'] for r in result['records']]}
    check('worker_RE3_'+arm, run)

check('private_locator_dataframe', lambda: reject(lambda: worker.re3_private_input_check(
    pd.DataFrame({'message': [files['logs.parquet']]}), template)))
check('private_identifier_nested', lambda: reject(lambda: worker.re3_private_input_check(
    {'nested': [template['slot']['opaque_id']]}, template)))

# All metadata below are fictional; these grant-shaped fixtures grant no real access.
members = [fingerprint('GENERATED-MEMBER-'+str(i)) for i in range(30)]
runtime = {'dataset': 'RE3-OB', 'g1_revision': fingerprint('GENERATED-G1'),
           'inventory': profile['inventory'], 'aliases': profile['aliases'],
           'profile_sha256': template['re3_profile_ref']['sha256'], 'cases': {}}
slots = []
for i, member in enumerate(members):
    row = dict(template['source'], member_sha256=member)
    oid = 'generated-'+str(i)
    runtime['cases'][oid] = row
    s = dict(template['slot'], opaque_id=oid, member_sha256=member, source_sha256=fingerprint(row))
    slots.append(s)
independent = {'dataset': 'RE3-OB', 'g1_revision': runtime['g1_revision'],
               'cases_by_member': {row['member_sha256']: row for row in runtime['cases'].values()}}
failure_ref = atomic(OUT/'failure-policy-FICTIONAL.json', {'schema': 'T054-FAILURE-POLICY-1', 'scope': 'LOCKED_RE3', 'dataset': 'RE3-OB'})
protocol = {'schema': 'T054-RE3-PROTOCOL-1', 'dataset': 'RE3-OB', 'status': 'LOCKED_FINAL_RE3',
            'final_version': True, 'case_count': 30, 'cell_count': 10, 'members': members,
            'g1_revision': runtime['g1_revision'], 'arms': {'baro': [None]}, 'slots': slots,
            'worlds': ['P'], 'metrics': ['rr', 'hit@5'], 'seed_aggregation': 'mean_complete_case',
            'support_policy': {'NO_EVIDENCE': 'zero', 'ERROR': 'zero', 'TIMEOUT': 'zero', 'UNSUPPORTED': 'separate'},
            'variants': {'baro': ['native']}, 'partitions': {'local': [fingerprint(s) for s in slots]},
            'dispatch': {'code_pins': {'src/p3/re3.py': ref(ROOT/'src/p3/re3.py')['sha256']},
                         'configurations': {'baro': template['config']},
                         'environments': {'main': template['slot']['environment_sha256']},
                         'failure_policy_ref': failure_ref}}
protocol_ref = atomic(OUT/'protocol-FICTIONAL.json', protocol)
runtime_ref = atomic(OUT/'runtime-FICTIONAL.json', runtime)
independent_ref = atomic(OUT/'independent-FICTIONAL.json', independent)
binding = {'protocol_sha256': protocol_ref['sha256'], 'profile_sha256': template['re3_profile_ref']['sha256'],
           'runtime_sha256': runtime_ref['sha256'], 'independent_source_sha256': independent_ref['sha256']}
binding_ref = atomic(OUT/'binding-FICTIONAL.json', binding)
source_ref = atomic(OUT/'authority-source-FICTIONAL.json', {'source': 'GENERATED FIXTURE ONLY; DOES NOT RECORD OR GRANT REAL RE3 PERMISSION'})
authority = {'re3_grant': True, 'g3': True, 'source': source_ref, **binding, 'runtime_binding_sha256': binding_ref['sha256']}
authority_ref = atomic(OUT/'authority-FICTIONAL.json', authority)
jobs = []
for s in slots:
    j = copy.deepcopy(template)
    j.pop('fixture_route'); j.pop('fixture_origin')
    j.update(kind='baseline', evaluation_mode='heldout', slot=s, source=runtime['cases'][s['opaque_id']],
             code_pins=protocol['dispatch']['code_pins'], g1_revision=runtime['g1_revision'],
             protocol_ref=protocol_ref, runtime_ref=runtime_ref, independent_source_ref=independent_ref,
             runtime_binding_ref=binding_ref, re3_grant_ref=authority_ref, failure_policy_ref=failure_ref)
    jobs.append(j)
plan = {'schema': 'T054-PLAN-1', 'mode': 'heldout', 'host_role': 'aggregate', 'jobs': jobs,
        'protocol_ref': protocol_ref, 're3_grant_ref': authority_ref, 're3_profile_ref': template['re3_profile_ref'],
        'budget': {'fixture': True}}
check('registered_protocol_complete30', lambda: nguon.validate_re3_protocol(protocol))
check('independent_RE3_job_binding_positive_metadata_only', lambda: nguon.validate_re3_job(jobs[0]))
for name, field, value in [('test_grant', 'evaluation_mode', 'test'), ('TT_dataset', 'slot', dict(slots[0], dataset='RE2-TT')),
                           ('wrong_t', 't', template['t']+1), ('wrong_inventory', 'inventory', ['a']),
                           ('wrong_code', 'code_pins', {'not-bound': 'x'})]:
    def bad_job(field=field, value=value):
        j = copy.deepcopy(jobs[0]); j[field] = value
        reject(lambda: nguon.validate_re3_job(j))
    check('reject_RE3_job_'+name, bad_job)
check('missing_RE3_grant', lambda: reject(lambda: nguon.authorize(plan, {}, 'run')))
def missing_g3():
    no_g3 = dict(authority); no_g3.pop('g3')
    pin = atomic(OUT/'authority-no-g3-FICTIONAL.json', no_g3)
    job = dict(jobs[0], re3_grant_ref=pin)
    reject(lambda: nguon.validate_re3_job(job))
check('RE3_grant_without_G3_rejected', missing_g3)
check('A4_rejects_RE3', lambda: reject(lambda: cham.validate_a4_slots(plan, {'RE3-OB': runtime})))
for name, mutate in [('missing_member', lambda p: p['members'].pop()),
                      ('missing_slot', lambda p: p['slots'].pop()),
                      ('duplicate_slot', lambda p: p['slots'].append(p['slots'][0])),
                      ('wrong_final', lambda p: p.update(final_version=False)),
                      ('unavailable_A', lambda p: p['arms'].update(torai_A=[0]))]:
    def bad_protocol(mutate=mutate):
        p = copy.deepcopy(protocol); mutate(p)
        reject(lambda: nguon.validate_re3_protocol(p))
    check('reject_protocol_'+name, bad_protocol)
for name, mutate in [('partition_overlap', lambda p: p['partitions'].update(other=p['partitions']['local'])),
                      ('partition_gap', lambda p: p['partitions']['local'].pop())]:
    def bad_partition(mutate=mutate):
        pr = copy.deepcopy(protocol); mutate(pr)
        reject(lambda: nguon.validate_re3_protocol(pr))
    check('reject_'+name, bad_partition)
def two_host_binding():
    pr = copy.deepcopy(protocol)
    pr['partitions'] = {'host1': [fingerprint(s) for s in slots[:15]], 'host2': [fingerprint(s) for s in slots[15:]]}
    pr['dispatch'] = {'hosts': {'host1': copy.deepcopy(protocol['dispatch']), 'host2': copy.deepcopy(protocol['dispatch'])}}
    pr_ref = atomic(OUT/'protocol-two-host-FICTIONAL.json', pr)
    b = dict(binding, protocol_sha256=pr_ref['sha256'])
    b_ref = atomic(OUT/'binding-two-host-FICTIONAL.json', b)
    a = dict(authority, protocol_sha256=pr_ref['sha256'], runtime_binding_sha256=b_ref['sha256'])
    a_ref = atomic(OUT/'authority-two-host-FICTIONAL.json', a)
    j = dict(jobs[0], protocol_ref=pr_ref, runtime_binding_ref=b_ref, re3_grant_ref=a_ref, re3_host='host1')
    nguon.validate_re3_job(j)
    reject(lambda: nguon.validate_re3_job(dict(j, re3_host='host2')))
    return {'matrix_partition': [15, 15], 'scope': 'metadata fixture only, no SSH/real hosts'}
check('two_host15_15_metadata_binding', two_host_binding)

# Labels are generated too. Mock receipt verification only for table arithmetic;
# the real worker/envelope verifier was exercised above with its saved records.
raw = read_pin(ref(BASE/'worker-baro/result.json'))['records']
result_map = {fingerprint(j['slot']): copy.deepcopy(raw) for j in jobs}
labels = {'dataset': 'RE3-OB', 'g1_revision': runtime['g1_revision'],
          'alias_sha256': fingerprint(profile['aliases']), 'cases': {}}
for i, j in enumerate(jobs):
    s = j['slot']; root = 'a' if i % 2 == 0 else 'b'; fault = 'generated-f'+str(i % 5)
    labels['cases'][s['opaque_id']] = {'member_sha256': s['member_sha256'], 'root': root,
                                      'fault': fault, 'cell': ['RE3-OB', root, fault]}
label_ref = atomic(OUT/'labels-GENERATED.json', labels)
canonical_ref = atomic(OUT/'canonical-labels-GENERATED.json', {
    'dataset': 'RE3-OB', 'g1_revision': runtime['g1_revision'], 'alias_sha256': fingerprint(profile['aliases']),
    'by_member': {r['member_sha256']: r for r in labels['cases'].values()}})
snapshot = {'plan_sha256': fingerprint(plan), 'slots': {fingerprint(j['slot']): {'state': 'VERIFIED'} for j in jobs}}
args = ({'RE3-OB': label_ref}, {'RE3-OB': canonical_ref}, {'RE3-OB': runtime},
        {'RE3-OB': profile['aliases']}, {'RE3-OB': profile['inventory']})


def separate_tables():
    dest = OUT/'table-generated'; dest.mkdir()
    with patch('cham.verify_snapshot', return_value=result_map):
        result = cham.evaluate(snapshot, plan, *args, dest)
    assert result['schema'] == 'T054-RE3-TABLES-1'
    assert result['case_count'] == 30 and result['cell_count'] == 10
    assert len(result['per_case']) == 30 and len(result['by_cell']) == 10
    assert result['by_arm'][0]['total_cases'] == 30
    assert not (dest/'a4.json').exists()
    return {'cases': 30, 'cells': 10, 'method_tables': len(result['by_arm'])}


check('separate_RE3_tables30cells10_no_A4', separate_tables)


def blocked_before_labels():
    bad = copy.deepcopy(snapshot); bad['slots'][fingerprint(jobs[0]['slot'])]['state'] = 'BLOCKED'
    def no_read(pin):
        if pin in (label_ref, canonical_ref):
            raise AssertionError('label reader was reached')
        return read_pin(pin)
    with patch('cham.read_pin', side_effect=no_read):
        reject(lambda: cham.evaluate(bad, plan, *args, OUT/'must-not-exist'))


check('unresolved_slot_blocks_before_label_read', blocked_before_labels)
check('wrong_dataset_label_bundle_rejected', lambda: reject(lambda: cham.evaluate(
    snapshot, plan, {'RE2-TT': label_ref}, args[1], args[2], args[3], args[4], OUT/'no-label-join')))
atomic(OUT/'summary.json', {'PASS': True, 'checks': len(checks), 'real_RE3_telemetry_opened': False,
                           'grant_fixtures': 'fictional metadata; no real permission generated',
                           'mocked_scope': 'table arithmetic uses mocked verified snapshot, separate from real worker/envelope checks'})
print(json.dumps({'PASS': True, 'checks': len(checks)}), flush=True)
