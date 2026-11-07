"""Bind reviewed metadata only after the exact final Minh decision."""
import copy
from pathlib import Path
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
sys.path[:0] = [str(ROOT / 'results/T-054/scripts'), str(ROOT / 'src'), str(ROOT / 'results/T-052/scripts')]
from bien_nhan import Blocked, atomic, digest, fingerprint, read_pin, ref
from nguon import validate_locked_plan, validate_aggregate_plan
from p7_guard_v3 import attest_runtime


def pin(path):
    value = ref(path)
    if Path(value['path']).is_relative_to(ROOT):
        value['path'] = Path(value['path']).relative_to(ROOT).as_posix()
    return value


def require_grant(grant):
    required = ('g3', 'test_grant', 'main_dispatch', 'materialize_source_grant', 'transfer_test_grant', 'score_grant')
    if any(grant.get(key) is not True for key in required):
        raise Blocked('WAIT_MINH_FINAL_013_G3_SOURCE_TRANSFER_MAIN_SCORE')
    source = grant.get('source', {})
    path = Path(source.get('path', ''))
    if path.is_absolute() or '..' in path.parts or '\\' in source.get('path', ''):
        raise Blocked('nguồn quyết định phải là locator tương đối trong repo để kiểm trên mọi máy')
    path = ROOT / path
    if not path.is_file() or digest(path) != source.get('sha256'):
        raise Blocked('nguồn quyết định Minh thiếu hoặc lệch pin')
    for name, key in [('protocol-candidate.json', 'approved_candidate_protocol_sha256'),
                      ('source-bundle.json', 'approved_source_bundle_sha256')]:
        if grant.get(key) != digest(RUN / name):
            raise Blocked('quyền không nhận diện đúng gói 013 đã phản biện')
    if grant.get('main_operating_policy_approved') is not True:
        raise Blocked('WAIT_LOCKED_OPERATING_POLICY')
    manifest_hash = grant.get('approved_preparation_manifest_sha256')
    if not manifest_hash or digest(RUN / 'manifest.json') != manifest_hash:
        raise Blocked('quyền chưa ghim manifest của gói chuẩn bị đã soát')
    manifest = read_pin(pin(RUN / 'manifest.json'))
    for name, expected in manifest['outputs'].items():
        path = ROOT / name
        if not path.is_file() or path.stat().st_size != expected['bytes'] or digest(path) != expected['sha256']:
            raise Blocked('đầu ra chuẩn bị đã đổi sau review: ' + name)
    if grant.get('RE3_preparation_disposition') != 'OPEN_ACCEPTED_FOR_MAIN_ONLY':
        raise Blocked('quyền main chưa khai đúng D2')
    return grant


def activate(grant_ref):
    grant = require_grant(read_pin(grant_ref))
    candidate = read_pin(pin(RUN / 'protocol-candidate.json'))
    bundle = read_pin(pin(RUN / 'source-bundle.json'))
    for path, expected in candidate['source_code'].items():
        if digest(ROOT / path) != expected:
            raise Blocked('code đã đổi sau review: ' + path)
    destination = RUN / 'activated-001'
    receipt_file = destination / 'activation-receipt.json'
    if receipt_file.exists():
        receipt = read_pin(pin(receipt_file))
        if receipt['grant'] != grant_ref:
            raise Blocked('lần kích hoạt cũ thuộc quyền khác')
        for item in receipt['plans'] + [receipt['aggregate'], receipt['protocol']]:
            read_pin(item)
        return receipt
    destination.mkdir(exist_ok=False)
    policy = read_pin(bundle['failure_policy_ref'])
    policy.update(scope='LOCKED_P7', main_allowed=True)
    atomic(destination / 'failure-policy.json', policy)
    policy_ref = pin(destination / 'failure-policy.json')
    protocol = copy.deepcopy(candidate)
    protocol.update(status='LOCKED_G3', real_execution_ready=True, G3_decision_source=grant['source'],
                    open_before_execution=[], readiness='LOCKED_METADATA_SOURCE_CHECKS_REQUIRED_BEFORE_DISPATCH')
    protocol['fingerprint'] = fingerprint({k: v for k, v in protocol.items() if k != 'fingerprint'})
    atomic(destination / 'protocol.json', protocol)
    protocol_ref = pin(destination / 'protocol.json')
    bindings = {}
    for dataset, runtime in bundle['runtime_refs'].items():
        target = destination / (('TT' if dataset == 'RE2-TT' else 'OB') + '-runtime-binding.json')
        attest_runtime(protocol_ref, runtime, bundle['independent_source_refs'][dataset], target, granted=True)
        bindings[dataset] = pin(target)
    parents = {}
    plans = []
    all_jobs = []
    all_support = []
    for host in ('ec2_1', 'ec2_2', 'local'):
        plan = read_pin(pin(RUN / 'prepared' / (host + '-plan.json')))
        plan.update(protocol_ref=protocol_ref, preparation_only=False, open_before_run=[])
        for job in plan['jobs']:
            s = job['slot']
            job.update(protocol_ref=protocol_ref, runtime_binding_ref=bindings[s['dataset']], failure_policy_ref=policy_ref)
            if s['arm'] == 'C-d3':
                parent = parents[(s['dataset'], s['opaque_id'])]
                job['main_dependency'] = dict(slot=parent['slot'], job_sha256=fingerprint(parent))
            if s['arm'] == 'M1' and s['view'] == 'main':
                parents[(s['dataset'], s['opaque_id'])] = job
        validate_locked_plan(plan, protocol, verify_host=False)
        target = destination / (host + '-plan.json')
        atomic(target, plan)
        plans.append(pin(target))
        authority = dict(grant, plan_sha256=fingerprint(plan),
                         torai_A_source_sha256=bundle['author_source_ref']['sha256'])
        atomic(destination / (host + '-authority.json'), authority)
        all_jobs.extend(plan['jobs']); all_support.extend(plan['ce_support'])
    aggregate = read_pin(pin(RUN / 'prepared/aggregate-plan.json'))
    aggregate.update(jobs=all_jobs, ce_support=all_support, execution_plan_refs=plans,
                     protocol_ref=protocol_ref, preparation_only=False, open_before_run=[])
    validate_aggregate_plan(aggregate, protocol)
    atomic(destination / 'aggregate-plan.json', aggregate)
    aggregate_ref = pin(destination / 'aggregate-plan.json')
    atomic(destination / 'aggregate-authority.json', dict(grant, plan_sha256=fingerprint(aggregate),
            torai_A_source_sha256=bundle['author_source_ref']['sha256']))
    result = dict(grant=grant_ref, protocol=protocol_ref, plans=plans, aggregate=aggregate_ref,
                  main_started=False, source_checks_required=True)
    atomic(receipt_file, result)
    return result
