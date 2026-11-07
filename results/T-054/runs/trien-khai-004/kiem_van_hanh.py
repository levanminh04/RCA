"""Kiểm đúng các thay đổi vận hành; không chạy lại baseline hoặc đọc test."""
import copy
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT/'results/T-054/scripts'), str(ROOT/'src')]
from bien_nhan import (atomic, ref, read_pin, fingerprint, events, Blocked,
                       known_operation_error, verify_method_failure)
from dieu_phoi import supervise, status, launch, check_budget, open_budget, budget_limits
from cham import snapshot_from_status, verify_snapshot


def jobs(n, seconds=1):
    result=[]
    for i in range(n):
        s=dict(dataset='SYNTHETIC', opaque_id='fixture-'+str(i), member_sha256='a'*64,
               arm='M1' if i==0 else 'bo-E'+str(i), view='main', seed=None,
               source_sha256='b'*64, window=[700,1000,1300], config_sha256='c'*64,
               environment_sha256='d'*64)
        result.append(dict(slot=s, kind='synthetic', executable=sys.executable, timeout_s=15,
                           scenario='slow_ok', sleep_s=seconds, a4=True,
                           synthetic_records=[{'status':'NO_EVIDENCE','blocks':[]}]))
    return result


def plan(name, n=2, seconds=1):
    return dict(schema='T054-PLAN-1', mode='synthetic', host_role='local', workers=2,
                directory=str(RUN/name), jobs=jobs(n,seconds),
                monitor={'poll_s':.1,'max_monitor_gap_s':5,'score_phases':['method']})


def denied(fn):
    try: fn()
    except (Blocked, KeyError, ValueError): return
    raise AssertionError('không chặn đầu vào sai')


def spawn(p):
    f=RUN/(Path(p['directory']).name+'-plan.json');pin=atomic(f,p)
    return launch(sys.executable,[str(ROOT/'results/T-054/scripts/p7.py'),'_supervise',
                  '--plan',pin['path'],'--sha256',pin['sha256']],
                  RUN/(f.stem+'-stdout.txt'),RUN/(f.stem+'-stderr.txt'))


def wait_until(fn, seconds=30):
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline:
        result=fn()
        if result:return result
        time.sleep(.1)
    raise AssertionError('fixture chưa đạt mốc trong thời gian khai')


def done(p):
    d=Path(p['directory']);st=status(d)
    return st if st['last_event'] and st['last_event']['state']=='SUPERVISOR_STOPPED' else None


def verified(p):
    st=status(p['directory']);assert len(st['jobs'])==len(p['jobs'])
    assert all(s['state']=='VERIFIED' for s in st['jobs'].values()),st
    verify_snapshot(snapshot_from_status(p,st),p['jobs'])
    return st


def main():
    checks=[]
    p=plan('parallel-positive');start=time.monotonic();supervise(p,p['directory']);verified(p)
    spans=[]
    for a in Path(p['directory']).glob('*/attempt-*'):
        phase=events(a/'phases.jsonl');method=[r for r in phase if r['phase']=='method']
        assert len(method)==2
        # Pha có UTC riêng do append; monitor mới ghi cả hai worker trước đóng.
        spans.append((read_pin(ref(a/'launch.json'))['started_epoch'],(a/'result.json').stat().st_mtime))
    assert max(x[0] for x in spans)<min(x[1] for x in spans)
    checks.append('two_processes_overlap_and_verify')
    for bad in [0,3,4,True,1.5]:denied(lambda b=bad:supervise(dict(p,workers=b),RUN/'bad-worker-count'))
    checks.append('only_one_or_two_workers')

    p=plan('drain-positive',4,2);proc=spawn(p)
    wait_until(lambda:len(status(p['directory'])['jobs'])==2)
    from bien_nhan import append
    append(Path(p['directory'])/'control.jsonl',{'action':'DRAIN'})
    wait_until(lambda:done(p));st=status(p['directory'])
    assert len(st['jobs'])==2 and all(r['state']=='VERIFIED' for r in st['jobs'].values())
    checks.append('DRAIN_finishes_two_active_without_new_dispatch')

    p=plan('resume-positive',2,5);proc=spawn(p)
    wait_until(lambda:len(list(Path(p['directory']).glob('*/attempt-*/actual-process.json')))==2)
    st=status(p['directory']);before={k:(r['attempt'],r['token']) for k,r in st['jobs'].items()}
    import psutil
    psutil.Process(st['controller']['pid']).kill()  # Giữ worker sống để kiểm nhận lại.
    wait_until(lambda:not psutil.pid_exists(st['controller']['pid']))
    pin=ref(RUN/'resume-positive-plan.json')
    resumed=launch(sys.executable,[str(ROOT/'results/T-054/scripts/p7.py'),'_supervise',
                    '--plan',pin['path'],'--sha256',pin['sha256']],
                    RUN/'resume-second-stdout.txt',RUN/'resume-second-stderr.txt')
    wait_until(lambda:done(p));st=verified(p)
    assert before=={k:(r['attempt'],r['token']) for k,r in st['jobs'].items()}
    assert len(list(Path(p['directory']).glob('*/attempt-*')))==2
    checks.append('restart_adopts_both_tokens_without_duplicate')

    policy=ref(RUN/'failure-policy-dev.json')
    for scenario,expected in [('method_timeout','VERIFIED'),('before_method_timeout','BLOCKED')]:
        p=plan('timeout-'+scenario,1,4);p['workers']=1
        p['jobs'][0].update(scenario=scenario,timeout_s=1,failure_policy_ref=policy)
        supervise(p,p['directory']);st=status(p['directory']);r=next(iter(st['jobs'].values()))
        assert r['state']==expected,r
        if expected=='VERIFIED':
            verified(p);attempt=Path(r['attempt']);receipt=read_pin(ref(attempt/'method-failure.json'))
            envelope=read_pin(ref(attempt/'result.json'));inv=read_pin(ref(attempt/'invocation.json'))
            assert envelope['records'][0]['status']=='TIMEOUT'
            forged=dict(receipt,kind='ERROR');bad=atomic(RUN/'forged-timeout-as-error.json',forged)
            denied(lambda:verify_method_failure(bad,p['jobs'][0],envelope,inv))
        checks.append(scenario+'_'+expected)

    # Kiểm quy tắc mới trên đúng đầu ra ERROR cũ, không chạy lại phương pháp.
    old=ROOT/'results/T-054/runs/trien-khai-003/pilot-local-005/queue'
    for path in old.glob('*/attempt-001/dev-error-reproduction.json'):
        attempt=path.parent;j=read_pin(ref(attempt/'job.json'));j['failure_policy_ref']=policy
        env=read_pin(ref(attempt/'result.json'));inv=read_pin(ref(attempt/'invocation.json'))
        audit=known_operation_error(j,env,inv)
        assert set(audit['normal_spans'].values())=={0} and min(audit['anomalous_spans'].values())>0
        wrong=copy.deepcopy(env);wrong['records'][0]['error']='ValueError: unrelated'
        denied(lambda:known_operation_error(j,wrong,inv))
        checks.append('known_'+j['slot']['arm']+'_audited_without_rerun')

    p=plan('unlimited-budget',1)
    p['budget']={'mode':'UNTIL_COHORT_COMPLETE','wall_s':None,'method_dataset_s':{},
                 'decision_ref':ref(RUN/'quyet-dinh-minh.json')}
    check_budget(p);d=Path(p['directory']);d.mkdir();b=open_budget(p,d)
    assert budget_limits(b,p['jobs'][0],{})=={}
    bad=copy.deepcopy(p);bad['budget']['wall_s']=3600;denied(lambda:check_budget(bad))
    checks.append('no_cumulative_cap_and_no_hidden_cap')
    atomic(RUN/'operational-checks.json',{'PASS':True,'checks':checks,'count':len(checks),
           'synthetic_only_except_reinspection_of_two_old_DEV_errors':True,
           'elapsed_s':time.monotonic()-start,'test_opened':False})
    print(json.dumps({'PASS':True,'checks':len(checks)},ensure_ascii=False))


if __name__=='__main__':
    try:main()
    except BaseException:
        import traceback
        atomic(RUN/'operational-failure-001.json',{'traceback':traceback.format_exc()})
        raise
