"""Sau quyết định G3/main riêng: đóng metadata thực thi, không gọi run/supervise/method."""
from pathlib import Path
import sys,copy,argparse,json
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'results/T-054';RUN=Path(__file__).resolve().parent
sys.path[:0]=[str(OUT/'scripts'),str(ROOT/'src'),str(ROOT/'results/T-052/scripts'),str(OUT/'runs/trien-khai-005')]
from bien_nhan import *
from nguon import validate_locked_plan,validate_aggregate_plan
from materialize_main import build
from p7_guard_v3 import attest_runtime
def pin(path):
    x=ref(path)
    if Path(path).resolve().is_relative_to(ROOT):x['path']=Path(path).resolve().relative_to(ROOT).as_posix()
    return x
def require_main_grant(grant):
    if not all(grant.get(k)is True for k in ['g3','test_grant','main_dispatch','torai_A_source_grant']):
        raise Blocked('WAIT_EXPLICIT_G3_MAIN_AND_TORAI_A_GRANT; preparation grant is insufficient')
    read_pin(grant['source'])if grant['source']['path'].endswith('.json')else None
    p=Path(grant['source']['path']);p=p if p.is_absolute()else ROOT/p
    if digest(p)!=grant['source']['sha256']:raise Blocked('main grant source hash differs')
def require_source_ready(bundle):
    if bundle.get('open_before_run'):
        raise Blocked('SOURCE_PREPARATION_BLOCKED: '+str(bundle['open_before_run']))
def activate(grant_ref):
    grant=read_pin(grant_ref);require_main_grant(grant)
    # Main authority must identify exactly the candidate reviewed by Minh.
    base=read_pin(ref(OUT/'protocol.json'))
    if grant.get('approved_candidate_protocol_sha256')!=ref(OUT/'protocol.json')['sha256']:
        raise Blocked('G3 grant does not pin candidate protocol')
    candidate=read_pin(ref(RUN/'source-bundle-final-prepared.json'))
    require_source_ready(candidate)
    if grant.get('approved_source_bundle_sha256')!=ref(RUN/'source-bundle-final-prepared.json')['sha256']:
        raise Blocked('G3 grant does not pin prepared source bundle')
    for rel,h in base['source_code'].items():
        if digest(ROOT/rel)!=h:raise Blocked('worker/scientific code differs from reviewed candidate')
    dest=RUN/'activated-001';dest.mkdir(exist_ok=False)
    policy=read_pin(candidate['failure_policy_ref']);policy.update(scope='LOCKED_P7',main_allowed=True)
    fp=atomic(dest/'failure-policy.json',policy);fp=pin(fp['path'])
    locked=copy.deepcopy(base);locked.update(status='LOCKED_G3',real_execution_ready=True,G3_decision_source=grant['source'],
        preparation_exposure=[pin(RUN/'checkpoint-01-sources.json'),pin(RUN/'OB-metric-time-window-check.json'),pin(RUN/'source-temporal-final-check.json')],readiness='LOCKED_METADATA_ACTIVATION_NOT_DISPATCH')
    locked['fingerprint']=fingerprint({k:v for k,v in locked.items()if k!='fingerprint'})
    atomic(dest/'protocol.json',locked);pp=pin(dest/'protocol.json')
    candidate['runtime_binding_refs']={};candidate['failure_policy_ref']=fp
    for ds,runtime in candidate['runtime_refs'].items():
        path=dest/('TT-binding.json'if ds=='RE2-TT'else'OB-binding.json')
        attest_runtime(pp,runtime,candidate['independent_source_refs'][ds],path,granted=True)
        candidate['runtime_binding_refs'][ds]=pin(path)
    atomic(dest/'source-bundle.json',candidate);bp=pin(dest/'source-bundle.json')
    refs,aggregate=build(pp,bp,grant,dest/'plans')
    for r in refs:validate_locked_plan(read_pin(r),locked,verify_host=False)
    validate_aggregate_plan(aggregate,locked)
    atomic(dest/'activation-receipt.json',dict(PASS=True,protocol=pp,source_bundle=bp,host_plans=refs,
        aggregate=pin(dest/'plans/aggregate-plan.json'),main_started=False,
        next='Transfer exact activation metadata+grant source to each existing code_root, verify pins/authority/environment/power then explicit p7 run; no new pilot.'))
    return pin(dest/'activation-receipt.json')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--grant',required=True);ap.add_argument('--sha256',required=True);args=ap.parse_args()
    print(json.dumps(activate({'path':args.grant,'sha256':args.sha256}),ensure_ascii=False))
