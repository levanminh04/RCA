"""Materialize locked metadata only after exact G3/main and cloud evidence grants.

Does not SSH, transfer data, dispatch workers or infer permission from preparation.
"""
from pathlib import Path
import argparse
import copy
import json
import sys

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(ROOT/'src'),str(ROOT/'results/T-052/scripts')]
from bien_nhan import Blocked,atomic,read_pin,ref,fingerprint,digest
from nguon import validate_locked_plan,validate_aggregate_plan
from p7_guard_v3 import attest_runtime


def pin(path):
    v=ref(path)
    if Path(path).resolve().is_relative_to(ROOT):v['path']=Path(path).resolve().relative_to(ROOT).as_posix()
    return v


def require_grant(grant):
    if not all(grant.get(k)is True for k in ['g3','test_grant','main_dispatch','torai_A_source_grant']):
        raise Blocked('WAIT_EXPLICIT_G3_MAIN_AND_A_SOURCE_GRANT')
    source=grant.get('source',{})
    if not source.get('path') or not source.get('sha256'):
        raise Blocked('WAIT_EXACT_USER_DECISION_SOURCE')
    path=Path(source['path']);path=path if path.is_absolute()else ROOT/path
    if digest(path)!=source['sha256']:raise Blocked('grant source changed')
    if (grant.get('approved_candidate_protocol_sha256')!=pin(RUN/'protocol-candidate.json')['sha256']
            or grant.get('approved_source_bundle_sha256')!=pin(RUN/'source-bundle-candidate.json')['sha256']):
        raise Blocked('grant does not identify the exact reviewed candidate')
    for host in ['ec2_1','ec2_2']:
        receipt=read_pin(grant.get('cloud_readiness_refs',{}).get(host,{}))
        expected=read_pin(pin(RUN/'packets'/(host+'-packet.json')))
        if (receipt.get('host')!=host or receipt.get('candidate_protocol_sha256')!=grant['approved_candidate_protocol_sha256']
                or receipt.get('packet_sha256')!=expected['archive']['sha256']
                or any(receipt.get(k)is not True for k in ['identity_verified','environment_verified','code_verified','sources_verified','RAM_disk_verified'])):
            raise Blocked('WAIT_CURRENT_CLOUD_READINESS:'+host)
    decisions=read_pin(grant.get('pre_G3_decisions_ref',{}))
    if (decisions.get('approved_candidate_protocol_sha256')!=grant['approved_candidate_protocol_sha256']
            or decisions.get('main_operating_policy_approved')is not True
            or decisions.get('RE3_preparation_disposition')not in ('RESOLVED_WITH_SOURCE','OPEN_ACCEPTED_FOR_MAIN_ONLY')):
        raise Blocked('WAIT_PRE_G3_DECISIONS')
    return grant


def activate(grant_ref):
    grant=require_grant(read_pin(grant_ref))
    candidate=read_pin(pin(RUN/'protocol-candidate.json'))
    bundle=read_pin(pin(RUN/'source-bundle-candidate.json'))
    for rel,sha in candidate['source_code'].items():
        if digest(ROOT/rel)!=sha:raise Blocked('reviewed code changed:'+rel)
    target=RUN/'activated-001';target.mkdir(exist_ok=False)
    policy=read_pin(bundle['failure_policy_ref']);policy.update(scope='LOCKED_P7',main_allowed=True)
    fp=atomic(target/'failure-policy.json',policy);fp=pin(fp['path'])
    protocol=copy.deepcopy(candidate)
    protocol.update(status='LOCKED_G3',real_execution_ready=True,G3_decision_source=grant['source'],
                    open_before_execution=[],readiness='LOCKED_METADATA_ONLY_NOT_DISPATCHED')
    protocol['fingerprint']=fingerprint({k:v for k,v in protocol.items()if k!='fingerprint'})
    pp=atomic(target/'protocol.json',protocol);pp=pin(pp['path'])
    bindings={}
    for ds,runtime in bundle['runtime_refs'].items():
        out=target/('TT-runtime-binding.json'if ds=='RE2-TT'else'OB-runtime-binding.json')
        attest_runtime(pp,runtime,bundle['independent_source_refs'][ds],out,granted=True)
        bindings[ds]=pin(out)
    parents={};refs=[];all_jobs=[];all_support=[]
    for host in ['ec2_1','ec2_2','local']:
        plan=read_pin(pin(RUN/'prepared'/(host+'-plan.json')))
        plan.update(protocol_ref=pp,preparation_only=False,open_before_run=[])
        for job in plan['jobs']:
            s=job['slot'];job.update(protocol_ref=pp,runtime_binding_ref=bindings[s['dataset']],failure_policy_ref=fp)
            if s['arm']=='C-d3':
                parent=parents[(s['dataset'],s['opaque_id'])]
                job['main_dependency']={'slot':parent['slot'],'job_sha256':fingerprint(parent)}
            if s['arm']=='M1'and s['view']=='main':parents[(s['dataset'],s['opaque_id'])]=job
        validate_locked_plan(plan,protocol,verify_host=False)
        pr=atomic(target/(host+'-plan.json'),plan);pr=pin(pr['path']);refs.append(pr)
        authority=dict(grant,plan_sha256=fingerprint(plan),torai_A_source_sha256=bundle['author_source_ref']['sha256'])
        atomic(target/(host+'-authority.json'),authority)
        all_jobs.extend(plan['jobs']);all_support.extend(plan['ce_support'])
    aggregate=read_pin(pin(RUN/'prepared/aggregate-plan.json'))
    aggregate.update(jobs=all_jobs,ce_support=all_support,execution_plan_refs=refs,protocol_ref=pp,
                     preparation_only=False,open_before_run=[])
    validate_aggregate_plan(aggregate,protocol)
    ap=atomic(target/'aggregate-plan.json',aggregate);ap=pin(ap['path'])
    atomic(target/'aggregate-authority.json',dict(grant,plan_sha256=fingerprint(aggregate),
                                                torai_A_source_sha256=bundle['author_source_ref']['sha256']))
    return atomic(target/'activation-receipt.json',{'protocol':pp,'plans':refs,'aggregate':ap,
                  'source_bundle':pin(RUN/'source-bundle-candidate.json'),'main_started':False,
                  'next':'Transfer and verify exact locked metadata as separately authorized; explicit p7 run only afterwards'})


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--grant',required=True);parser.add_argument('--sha256',required=True)
    args=parser.parse_args();print(json.dumps(activate({'path':args.grant,'sha256':args.sha256}),ensure_ascii=False))
