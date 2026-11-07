"""Phản ví dụ cho nguồn nhãn gốc, phân loại ERROR dev và metadata CIRCA."""
import copy
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]; OUT=ROOT/'results/T-054';RUN=OUT/'runs/trien-khai-003'
sys.path.insert(0,str(OUT/'scripts'))
from bien_nhan import Blocked,atomic,fingerprint,read_pin,ref,verify_dev_error_reproduction
from dieu_phoi import status,verify_attempt
from cham import snapshot_from_status,verify_snapshot
from nguon import compare_labels,original_dev_labels

checks=[]
def reject(name, fn):
    try: fn()
    except (Blocked, KeyError): checks.append(name)
    else: raise AssertionError(name)

dest=RUN/'pilot-local-007';meta=read_pin(ref(dest/'metadata.json'));plan=read_pin(meta['plan']);state=status(dest/'queue')
job=next(j for j in plan['jobs'] if j['slot']['arm']=='microrank' and j['slot']['dataset']=='RE2-TT')
row=state['jobs'][fingerprint(job['slot'])];attempt=Path(row['attempt'])
env=read_pin(ref(attempt/'result.json'));inv=read_pin(ref(attempt/'invocation.json'));cpin=ref(attempt/'dev-error-reproduction.json')
verify_dev_error_reproduction(cpin,job,env,inv);checks.append('audited_native_error_positive')
wrong=copy.deepcopy(job);wrong['evaluation_mode']='test'
reject('dev_error_receipt_never_authorizes_test',lambda:verify_dev_error_reproduction(cpin,wrong,env,inv))
bad=copy.deepcopy(env);bad['records'][0]['status']='TIMEOUT'
forged=read_pin(cpin);forged['result_sha256']=fingerprint(bad)
forged_pin=atomic(RUN/'forged-timeout-reproduction.json',forged)
reject('dev_ERROR_receipt_not_TIMEOUT_policy_even_rehashed',lambda:verify_dev_error_reproduction(forged_pin,job,bad,inv))
bad=copy.deepcopy(env);bad['records'][0]['error']='different'
forged=read_pin(cpin);forged['result_sha256']=fingerprint(bad)
forged_pin=atomic(RUN/'forged-different-error-reproduction.json',forged)
reject('rehashed_different_method_error_rejected',lambda:verify_dev_error_reproduction(forged_pin,job,bad,inv))
snapshot=snapshot_from_status(plan,state);verify_snapshot(snapshot,plan['jobs']);checks.append('complete_snapshot_with_audited_ERROR_positive')
receipt=read_pin(row['receipt']);receipt.pop('dev_error_reproduction')
bad_ref=atomic(RUN/'unclassified-receipt-counterexample.json',receipt)
bad_snapshot=copy.deepcopy(snapshot);bad_snapshot['slots'][fingerprint(job['slot'])]['receipt']=bad_ref
reject('snapshot_VERIFIED_cannot_skip_ERROR_classification',lambda:verify_snapshot(bad_snapshot,plan['jobs']))
for ds,runtime_ref in meta['runtime_refs'].items():
    runtime=read_pin(runtime_ref);private=Path(runtime_ref['path']).parent;prefix='TT' if ds=='RE2-TT' else 'OB'
    canonical=read_pin(ref(private/(prefix+'-canonical-label-source.json')))
    local=read_pin(ref(private/(prefix+'-labels.json')))
    compare_labels(local,canonical,runtime,{},plan['inventories'][ds]);checks.append(ds+': G1 label positive')
    for key in ('root','fault','cell'):
        bad_labels=copy.deepcopy(local);oid=next(iter(bad_labels['cases']))
        bad_labels['cases'][oid][key]=['bad'] if key=='cell' else 'bad'
        reject(ds+': poisoned '+key+' rejected against original G1',lambda b=bad_labels,c=canonical,r=runtime,d=ds:compare_labels(b,c,r,{},plan['inventories'][d]))
circa=next(j for j in plan['jobs'] if j['slot']['arm']=='circa' and j['slot']['dataset']=='RE2-TT')
state_c=state['jobs'][fingerprint(circa['slot'])]
verify_attempt(Path(state_c['attempt']),circa,state_c['token']);checks.append('CIRCA_actual_current_positive')
original=Path(state_c['attempt']);fake=RUN/'CIRCA-missing-current-counterexample';fake.mkdir(exist_ok=False)
record=read_pin(ref(original/'result.json'));record['records'][0]['window']['circa_current']=None
record['record_sha256']=fingerprint(record['records'])
atomic(fake/'result.json',record);atomic(fake/'invocation.json',read_pin(ref(original/'invocation.json')))
reject('CIRCA_current_missing_even_after_rehash',lambda:verify_attempt(fake,circa,state_c['token']))
atomic(RUN/'new-guard-checks.json',{'PASS':True,'count':len(checks),'checks':checks,
       'scope':'existing sealed DEV/synthetic metadata, no new method or test read'})
print(json.dumps({'PASS':True,'count':len(checks)}))
