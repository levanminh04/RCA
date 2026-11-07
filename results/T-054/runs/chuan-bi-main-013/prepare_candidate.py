"""Compile immutable candidates from pinned metadata, without opening test payloads."""
from collections import Counter
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
OUT = ROOT / 'results/T-054'
sys.path[:0] = [str(OUT / 'scripts'), str(ROOT / 'src'), str(ROOT / 'results/T-052/scripts')]
from bien_nhan import atomic, digest, fingerprint, read_pin, ref
from nguon import compare_sources, placement_key, validate_locked_plan, validate_aggregate_plan
from cham import validate_ce_plan
from p7 import load_plan


def pin(path):
    value = ref(path)
    if Path(value['path']).is_relative_to(ROOT):
        value['path'] = Path(value['path']).relative_to(ROOT).as_posix()
    return value


def write(name, value):
    atomic(RUN / name, value)
    return pin(RUN / name)


def main():
    m11 = json.loads((OUT / 'manifest-hoan-thien-local-g3-011.json').read_bytes())['outputs']
    oldroot = 'results/T-054/runs/hoan-thien-local-g3-011/'
    def old(name):
        path = oldroot + name
        return read_pin(dict(m11[path], path=path))
    bundle = old('source-bundle-candidate.json')
    runtimes = {}
    originals = {}
    projections = {}
    original_refs = copy.deepcopy(bundle['independent_source_refs'])
    for dataset in ('RE2-TT', 'Nezha-OB'):
        runtime = read_pin(bundle['runtime_refs'][dataset])
        independent = read_pin(bundle['independent_source_refs'][dataset])
        compare_sources(runtime, independent, dataset, runtime['g1_revision'])
        originals[dataset] = runtime
        if dataset == 'RE2-TT':
            runtime = copy.deepcopy(runtime)
            independent = copy.deepcopy(independent)
            for oid, row in runtime['cases'].items():
                for kind, meta in row['files'].items():
                    meta['path'] = f'data/locked/rcaeval-re2tt-60/{oid}/{kind}'
            members = {row['member_sha256']: oid for oid, row in runtime['cases'].items()}
            for member, row in independent['cases_by_member'].items():
                for kind, meta in row['files'].items():
                    meta['path'] = f'data/locked/rcaeval-re2tt-60/{members[member]}/{kind}'
        compare_sources(runtime, independent, dataset, runtime['g1_revision'])
        tag = 'TT' if dataset == 'RE2-TT' else 'OB'
        runtime_ref = write('sources/' + tag + '-runtime.json', runtime)
        independent_ref = write('sources/' + tag + '-independent.json', independent)
        # Preparation binding hashes, not a G3 runtime attestation.
        projections[dataset] = dict(runtime=runtime_ref, independent=independent_ref,
                                    cases=compare_sources(runtime, independent, dataset, runtime['g1_revision']))
        runtimes[dataset] = runtime
    write('R1-projection-check.json', dict(PASS=True, cases={ds: len(rt['cases']) for ds, rt in runtimes.items()},
          original_source_refs=original_refs, private_map_reused=True, raw_payloads_read=False,
          evidence='Each independent row projected from the separately pinned source; all byte/SHA/time fields retained'))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0',
               OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    local_env = {}
    for name, executable in [('main', 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe'),
                             ('py38', 'D:/RCA-ext/envs/py38-rcdlock/Scripts/python.exe')]:
        result = json.loads(subprocess.check_output([executable, '-X', 'utf8', '-B',
             str(OUT / 'runs/hoan-thien-local-g3-011/capture_runtime_environment.py')], env=env))
        local_env[name] = result
    environments = {'local': local_env}
    remote = '/home/ubuntu/rca-p7/T-054/checkpoint013'
    # Current cloud results and their archives are verified by collect.py first.
    cloud = json.loads((RUN / 'cloud-verification.json').read_bytes())
    numeric = read_pin(pin(RUN / 'numeric-parity-Ce-decision.json'))
    assert numeric['general_tolerance'] is False and numeric['max_observed_ulps'] == 1
    mapping = {'ec2_1': 'ec2-large-disk', 'ec2_2': 'ec2-small-disk'}
    for host, name in mapping.items():
        environments[host] = cloud['hosts'][name]['environments']
    envref = write('environments.json', environments)
    code = old('current-code-pins.json')['code_pins']
    code = {p: digest(ROOT / p) for p in code if p.startswith(('src/', 'results/T-052/scripts/', 'results/T-054/scripts/'))}
    for name in ('activate.py', 'main.py', 'receive_main.py'):
        path = RUN / name
        code[path.relative_to(ROOT).as_posix()] = digest(path)
    write('code-pins.json', {'code_pins': code, 'files': {p: pin(ROOT / p) for p in code}})
    policy = read_pin(bundle['failure_policy_ref'])
    for evidence in policy['code_evidence']:
        evidence.update(pin(ROOT / evidence['path']))
    policy.update(scope='CANDIDATE_013_NOT_LOCKED', main_allowed=False)
    policy_ref = write('failure-policy.json', policy)
    m6 = json.loads((OUT / 'manifest-chuan-bi-main-006.json').read_bytes())['outputs']
    audit_path = 'results/T-054/runs/chuan-bi-main-006/OB-metric-time-window-check.json'
    audit = read_pin(dict(m6[audit_path], path=audit_path))
    # Case IDs are opaque, selected from the already recorded timestamp audit.
    affected = set()
    def find_ids(value):
        if isinstance(value, dict):
            if isinstance(value.get('opaque_id'), str) and value['opaque_id'].startswith('test-'):
                affected.add(value['opaque_id'])
            for row in value.values():
                find_ids(row)
        elif isinstance(value, list):
            for row in value:
                find_ids(row)
    find_ids(audit['issues'])
    assert len(affected) == 4, affected
    obref = write('OB-group-decision.json', dict(status='USER_CONFIRMED', affected_opaque_ids=sorted(affected),
                source=pin(RUN / 'preparation-permission.json'), audit=dict(m6[audit_path], path=audit_path),
                rule='paired M1-M4 Hit5 descriptions all34/remaining30/affected4; A4 unchanged'))
    parts = {host: [] for host in ('ec2_1', 'ec2_2', 'local')}
    support = {host: [] for host in parts}
    old_jobs = [job for host in parts for job in old('prepared/' + host + '-plan.json')['jobs']]
    old_support = [row for host in parts for row in old('prepared/' + host + '-plan.json')['ce_support']]
    tt_ids = sorted(runtimes['RE2-TT']['cases'])
    # Two identical EC2 types; final candidate uses one worker on each after review.
    owners = {oid: 'ec2_1' if i < 30 else 'ec2_2' for i, oid in enumerate(tt_ids)}
    for job in old_jobs:
        s = job['slot']
        host = ('local' if s['dataset'] == 'Nezha-OB' or s['arm'] in ('circa', 'microrank', 'torai_A')
                else owners[s['opaque_id']])
        parts[host].append(copy.deepcopy(job))
    for row in old_support:
        support[owners[row['opaque_id']]].append(copy.deepcopy(row))
    placement = dict(schema='T054-PLACEMENT-1', status='CANDIDATE_013', hosts={}, TT_case_owner=owners,
                     no_dynamic_reassignment=True, source_transferred=False)
    for host in parts:
        placement['hosts'][host] = [placement_key(j['slot']) for j in parts[host]]
        placement['hosts'][host] += [placement_key(dict(row, arm='M1', view='ce', seed=None)) for row in support[host]]
    placement_ref = write('placement.json', placement)
    contract = old('dispatch-contract-candidate.json')
    contract.update(code_pins=code, partition_ref=placement_ref, failure_policy_candidate_ref=policy_ref,
                    ob_sensitivity_ref=obref, status='CANDIDATE_013')
    local_peaks = {**contract['hosts']['ec2_2'].get('resources', {}).get('expected_peak_bytes', {}),
                   **contract['hosts']['local'].get('resources', {}).get('expected_peak_bytes', {})}
    for host in parts:
        hc = contract['hosts'][host]
        hc.update(code_pins=code, ob_sensitivity_ref=obref,
                  environment_sha256={key: fingerprint(value) for key, value in environments[host].items() if key in ('main', 'py38')})
        if host == 'local':
            hc.update(code_root=str(ROOT), data_root=str(ROOT),
                      workers=2, auxiliary_A_policy='AFTER_NON_A_VERIFIED_PREFLIGHT_AND_PRESERVE_BLOCKED')
            hc['resources']['expected_peak_bytes'] = local_peaks
        else:
            hc.pop('auxiliary_A_policy', None)
            hc.update(code_root=remote + '/work', data_root=remote + '/data-root', workers=1,
                      executable=remote + '/envs/main/bin/python', prep_executable=remote + '/envs/main/bin/python',
                      method_executable=remote + '/envs/py38/bin/python', pythonpath=[remote + '/work/upstream/rcaeval'])
            for group, peak in cloud['hosts'][mapping[host]].get('peaks', {}).items():
                hc['resources']['expected_peak_bytes'][group] = max(hc['resources']['expected_peak_bytes'].get(group, 0), peak)
        hc['environment_evidence'] = str(envref['path'])
        hc['resources']['note'] = ('DEV observations with retained provisional reservations; factor/reserve unchanged; '
                                    'scheduler rechecks available RAM before each dispatch; not a peak upper bound')
    contract_ref = write('dispatch-contract.json', contract)
    protocol = old('protocol-candidate.json')
    protocol.update(status='CANDIDATE_NOT_LOCKED', real_execution_ready=False, source_code=code,
                    dispatch_contract_ref=contract_ref, runtime_environments_ref=envref,
                    runtime='TT30/30 on new EC2; OB/CIRCA/MicroRank/A on laptop; A strictly last',
                    open_before_execution=['WAIT_MINH_EXACT_013_G3_SOURCE_TRANSFER_MAIN_AND_SCORE_GRANTS'],
                    RE3_preparation_disposition='OPEN_ACCEPTED_FOR_MAIN_ONLY',
                    execution_candidate={'placement': placement_ref, 'contract': contract_ref,
                                         'prepared_root': RUN.relative_to(ROOT).as_posix() + '/prepared'})
    protocol['fingerprint'] = fingerprint({k: v for k, v in protocol.items() if k != 'fingerprint'})
    protocol_ref = write('protocol-candidate.json', protocol)
    runtime_refs = {ds: row['runtime'] for ds, row in projections.items()}
    independent_refs = {ds: row['independent'] for ds, row in projections.items()}
    bundle.update(runtime_refs=runtime_refs, independent_source_refs=independent_refs, original_source_refs=original_refs,
                  failure_policy_ref=policy_ref, source_projection_ref=pin(RUN / 'R1-projection-check.json'),
                  note='013 projected metadata; original private maps remain on laptop; source transfer and methods require final grants',
                  open_before_run=protocol['open_before_execution'])
    bundle['historical_preparation_binding_refs'] = bundle.pop('runtime_binding_refs')
    bundle['historical_source_readiness_ref'] = bundle.pop('source_readiness_ref')
    bundle['hosts'] = {h: dict(main_executable=hc['executable'], py38_executable=hc['method_executable'],
                             pythonpath=hc['pythonpath']) for h,hc in contract['hosts'].items()}
    bundle['evaluation'].update(runtime_refs=runtime_refs, output=str(OUT / 'reports/main-013'))
    bundle_ref = write('source-bundle.json', bundle)
    planrefs = []
    parents = {}
    counts = {}
    from bien_nhan import failure_policy
    def candidate_policy(job):
        value = failure_policy(dict(job, evaluation_mode='dev'))
        return dict(value, scope='LOCKED_P7', main_allowed=True)
    for host in parts:
        hc = dict(contract, **contract['hosts'][host])
        parts[host].sort(key=lambda j: j['slot']['arm'] == 'torai_A')
        for job in parts[host]:
            s = job['slot']; ds = s['dataset']; arm = s['arm']
            row = runtimes[ds]['cases'][s['opaque_id']]
            torai = arm in ('torai_A', 'torai_B') and ds == 'RE2-TT'
            s.update(source_sha256=fingerprint(row), environment_sha256=hc['environment_sha256']['py38' if torai else 'main'])
            job.update(source=row, runtime_ref=runtime_refs[ds], independent_source_ref=independent_refs[ds],
                       protocol_ref=protocol_ref, code_pins=code, failure_policy_ref=policy_ref,
                       data_root=hc['data_root'], executable=hc['executable'], pythonpath=hc['pythonpath'],
                       prep_executable=hc['prep_executable'], method_executable=hc['method_executable'],
                       prep_environment_sha256=hc['environment_sha256']['main'])
            job.pop('runtime_binding_ref', None)
            if arm == 'M1' and s['view'] == 'main':
                parents[(ds, s['opaque_id'])] = job
            if arm == 'C-d3':
                parent = parents[(ds, s['opaque_id'])]
                job['main_dependency'] = dict(slot=parent['slot'], job_sha256=fingerprint(parent))
        for row in support[host]:
            row['source_sha256'] = fingerprint(runtimes['RE2-TT']['cases'][row['opaque_id']])
        plan = dict(schema='T054-PLAN-1', mode='test', host_role=host, jobs=parts[host], ce_support=support[host],
                    protocol_ref=protocol_ref, preparation_only=True, workers=hc['workers'], resources=hc['resources'],
                    monitor=hc['monitor'], budget=hc['budget'], ob_sensitivity_ref=obref,
                    sensitivity_decision_ref=hc['sensitivity_decision_ref'],
                    inventories={ds: rt['inventory'] for ds, rt in runtimes.items()},
                    directory=hc['code_root'] + '/results/T-054/runs/main-013/queue', open_before_run=protocol['open_before_execution'])
        if hc.get('auxiliary_A_policy'):
            plan['auxiliary_A_policy'] = hc['auxiliary_A_policy']
        pr = write('prepared/' + host + '-plan.json', plan)
        load_plan(ROOT / pr['path'], pr['sha256'])
        # Validate future locked semantics without publishing a fake LOCKED artifact.
        with patch('bien_nhan.failure_policy', side_effect=candidate_policy):
            validate_locked_plan(plan, protocol, verify_host=False)
        planrefs.append(pr)
        counts[host] = dict(jobs=len(plan['jobs']), ce_support=len(support[host]), workers=plan['workers'],
                            groups=dict(Counter(j['slot']['dataset'] + '|' + j['slot']['arm'] for j in plan['jobs'])))
    aggregate = old('prepared/aggregate-plan.json')
    aggregate.update(jobs=[j for rows in parts.values() for j in rows], ce_support=[r for rows in support.values() for r in rows],
                     execution_plan_refs=planrefs, protocol_ref=protocol_ref, ob_sensitivity_ref=obref,
                     auxiliary_A_policy=contract['hosts']['local']['auxiliary_A_policy'], evaluation=bundle['evaluation'],
                     directory=str(RUN / 'aggregate'), open_before_run=protocol['open_before_execution'])
    write('prepared/aggregate-plan.json', aggregate)
    with patch('bien_nhan.failure_policy', side_effect=candidate_policy):
        validate_aggregate_plan(aggregate, protocol)
    validate_ce_plan(aggregate, runtimes['RE2-TT'])
    assert len(aggregate['jobs']) == 1640 and len(aggregate['ce_support']) == 2
    write('candidate-validation.json', dict(PASS=True, hosts=counts, jobs=1640, positions=1642,
          validation_policy='in-memory future LOCKED semantics only; all saved artifacts remain CANDIDATE',
          numeric_exception=pin(RUN / 'numeric-parity-Ce-decision.json'),
          source_bundle=bundle_ref, G3=False, test_opened=False, main_started=False))
    print(json.dumps(dict(PASS=True, hosts=counts), ensure_ascii=False))


if __name__ == '__main__':
    main()
