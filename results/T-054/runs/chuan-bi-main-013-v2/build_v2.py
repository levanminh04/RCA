"""Dựng metadata v2 từ ứng viên013 đã khóa: chỉ đổi pin hai file sửa (bien_nhan, dieu_phoi), ba helper v2,
failure-policy v2, gốc code EC2 work-v2 và thư mục queue/report v2. Slot/config/seed/source/window/env giữ nguyên."""
import copy
import json
import sys
from pathlib import Path
from unittest.mock import patch

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
OUT = ROOT / 'results/T-054'
V1 = OUT / 'runs/chuan-bi-main-013'
sys.path[:0] = [str(OUT / 'scripts'), str(ROOT / 'src'), str(ROOT / 'results/T-052/scripts')]
from bien_nhan import atomic, digest, fingerprint, read_pin, ref
from nguon import validate_locked_plan, validate_aggregate_plan
from cham import validate_ce_plan
from p7 import load_plan

REMOTE = '/home/ubuntu/rca-p7/T-054/checkpoint013'


def pin(path):
    value = ref(path)
    if Path(value['path']).is_relative_to(ROOT):
        value['path'] = Path(value['path']).relative_to(ROOT).as_posix()
    return value


def write(name, value):
    atomic(RUN / name, value)
    return pin(RUN / name)


def v1(name):
    return json.loads((V1 / name).read_bytes())


def main():
    rel = lambda p: p.relative_to(ROOT).as_posix()
    old_code = v1('code-pins.json')['code_pins']
    code = {}
    for path in old_code:
        if path.startswith(rel(V1) + '/'):
            path = rel(RUN / Path(path).name)
        code[path] = digest(ROOT / path)
    changed = sorted(p for p in code if old_code.get(p) not in (None, code[p]))
    write('code-pins.json', {'code_pins': code, 'files': {p: pin(ROOT / p) for p in code}})
    policy_ref = pin(RUN / 'failure-policy.json')
    policy = read_pin(policy_ref)
    assert 'INSUFFICIENT_NORMAL_SPANS' in policy['error_rules']
    contract = v1('dispatch-contract.json')
    contract.update(code_pins=code, failure_policy_candidate_ref=policy_ref, status='CANDIDATE_013_V2')
    for host, hc in contract['hosts'].items():
        hc['code_pins'] = code
        if host != 'local':
            hc.update(code_root=REMOTE + '/work-v2', pythonpath=[REMOTE + '/work-v2/upstream/rcaeval'])
    contract_ref = write('dispatch-contract.json', contract)
    protocol = v1('protocol-candidate.json')
    protocol.update(source_code=code, dispatch_contract_ref=contract_ref,
                    version='013-v2', v2_change='INSUFFICIENT_NORMAL_SPANS rule; unclassified method ERROR blocks only slot and dependents',
                    v1_protocol_ref=pin(V1 / 'protocol-candidate.json'))
    protocol['execution_candidate'] = dict(protocol['execution_candidate'], contract=contract_ref,
                                           prepared_root=rel(RUN) + '/prepared')
    protocol['fingerprint'] = fingerprint({k: v for k, v in protocol.items() if k != 'fingerprint'})
    protocol_ref = write('protocol-candidate.json', protocol)
    bundle = v1('source-bundle.json')
    bundle.update(failure_policy_ref=policy_ref, note='013-v2 metadata; sources/maps unchanged from 013')
    for host, hb in bundle['hosts'].items():
        hb['pythonpath'] = contract['hosts'][host]['pythonpath']
    bundle['evaluation'] = dict(bundle['evaluation'], output=str(OUT / 'reports/main-013-v2'))
    bundle_ref = write('source-bundle.json', bundle)
    from bien_nhan import failure_policy
    def candidate_policy(job):
        value = failure_policy(dict(job, evaluation_mode='dev'))
        return dict(value, scope='LOCKED_P7', main_allowed=True)
    planrefs, counts, all_jobs, all_support = [], {}, [], []
    for host in ('ec2_1', 'ec2_2', 'local'):
        old = v1('prepared/' + host + '-plan.json')
        hc = dict(contract, **contract['hosts'][host])
        plan = copy.deepcopy(old)
        parents = {}
        for job in plan['jobs']:
            s = job['slot']
            job.update(protocol_ref=protocol_ref, code_pins=code, failure_policy_ref=policy_ref, pythonpath=hc['pythonpath'])
            if s['arm'] == 'M1' and s['view'] == 'main':
                parents[(s['dataset'], s['opaque_id'])] = job
            if s['arm'] == 'C-d3':
                parent = parents[(s['dataset'], s['opaque_id'])]
                job['main_dependency'] = dict(slot=parent['slot'], job_sha256=fingerprint(parent))
        plan.update(protocol_ref=protocol_ref, directory=hc['code_root'] + '/results/T-054/runs/main-013-v2/queue')
        assert [j['slot'] for j in plan['jobs']] == [j['slot'] for j in old['jobs']] and plan['ce_support'] == old['ce_support']
        pr = write('prepared/' + host + '-plan.json', plan)
        load_plan(ROOT / pr['path'], pr['sha256'])
        with patch('bien_nhan.failure_policy', side_effect=candidate_policy):
            validate_locked_plan(plan, protocol, verify_host=False)
        planrefs.append(pr)
        all_jobs += plan['jobs']; all_support += plan['ce_support']
        counts[host] = dict(jobs=len(plan['jobs']), ce_support=len(plan['ce_support']), workers=plan['workers'])
    aggregate = v1('prepared/aggregate-plan.json')
    old_slots = [j['slot'] for j in aggregate['jobs']]
    aggregate.update(jobs=all_jobs, ce_support=all_support, execution_plan_refs=planrefs, protocol_ref=protocol_ref,
                     evaluation=bundle['evaluation'], directory=str(RUN / 'aggregate'))
    assert sorted(map(fingerprint, old_slots)) == sorted(fingerprint(j['slot']) for j in all_jobs)
    write('prepared/aggregate-plan.json', aggregate)
    with patch('bien_nhan.failure_policy', side_effect=candidate_policy):
        validate_aggregate_plan(aggregate, protocol)
    validate_ce_plan(aggregate, read_pin(bundle['runtime_refs']['RE2-TT']))
    assert len(aggregate['jobs']) == 1640 and len(aggregate['ce_support']) == 2
    packet = v1('main-packet.json')
    files = {}
    for key, meta in packet['files'].items():
        path = meta.get('source_path', key)
        for name in ('protocol-candidate.json', 'dispatch-contract.json', 'code-pins.json', 'failure-policy.json',
                     'prepared/ec2_1-plan.json', 'prepared/ec2_2-plan.json', 'activate.py', 'main.py', 'receive_main.py'):
            if key == rel(V1 / name):
                key = path = rel(RUN / name)
        if key in code:
            path = key
        meta = dict(meta, source_path=path, **{k: v for k, v in pin(ROOT / path).items() if k in ('bytes', 'sha256')})
        files[key] = meta
    for name in ('environments.json', 'environment-patches.json'):
        key = rel(RUN / name); files[key] = dict(source_path=key, **{k: v for k, v in pin(RUN / name).items() if k in ('bytes', 'sha256')})
    packet.update(files=files, schema='T054-013-V2-CODE-OPAQUE-METADATA')
    write('main-packet.json', packet)
    grant = v1('grant-template.json')
    grant.update(approved_candidate_protocol_sha256=protocol_ref['sha256'], approved_source_bundle_sha256=bundle_ref['sha256'],
                 approved_preparation_manifest_sha256='FILL_AFTER_MANIFEST')
    write('grant-template.json', grant)
    write('candidate-validation.json', dict(PASS=True, hosts=counts, jobs=1640, positions=1642, changed_code=changed,
          slots_configs_seeds_sources_windows_environments_unchanged=True, v1_protocol=pin(V1 / 'protocol-candidate.json')))
    print(json.dumps(dict(PASS=True, hosts=counts, changed_code=changed, protocol=protocol_ref['sha256'],
                          bundle=bundle_ref['sha256']), ensure_ascii=False))


if __name__ == '__main__':
    main()
