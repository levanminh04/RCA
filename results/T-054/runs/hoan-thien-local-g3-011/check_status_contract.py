"""Approved gRPC guard refinement, invented signals only."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[k] = '1'
from pathlib import Path
import copy
import json
import sys
import traceback

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
OUT = RUN/sys.argv[1]
OUT.mkdir(exist_ok=False)
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'results/T-054/scripts'),
                'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages']
import pandas as pd
from p3 import re3, torai_b
from p3.adapters import torai
from bien_nhan import atomic, ref, read_pin, fingerprint
import worker

checks = []
def check(name, fn):
    try:
        value = fn(); checks.append({'name':name,'PASS':True,'detail':value if isinstance(value,dict) else None})
    except Exception as exc:
        checks.append({'name':name,'PASS':False,'error':repr(exc),'traceback':traceback.format_exc()})
        (OUT/'checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
        raise
    (OUT/'checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS '+name,flush=True)

def reject(fn):
    try:fn()
    except re3.ContractError:return
    raise AssertionError('invalid profile/code accepted')

old = ROOT/'results/T-054/runs/cai-re3-h2-010'
binary = read_pin(ref(old/'synthetic-004/profile.json'))
grpc = copy.deepcopy(binary)
grpc.update(trace_status_kind='grpc_status_code', trace_status_values=list(range(17)))
grpc['evidence']['trace_status_kind'] = 'author docs/CONVERT.md at revision pinned in011; fixture only, not real RE3 profile'
check('binary_default_unchanged',lambda:re3.validate_torai_status([0,1,None],binary))
for code in [0,1,2,13,16]:
    check('grpc_'+str(code),lambda code=code:re3.validate_torai_status([code],grpc))
for code in [-1,17,True,'13',2.5]:
    check('reject_code_'+str(code),lambda code=code:reject(lambda:re3.validate_torai_status([code],grpc)))
for field in ['trace_status_values','trace_status_kind']:
    def missing(field=field):
        p=copy.deepcopy(grpc);p.pop(field)
        reject(lambda:re3.validate_torai_status([2],p))
    check('missing_'+field,missing)
def no_evidence():
    p=copy.deepcopy(grpc);p['evidence'].pop('trace_status_kind')
    reject(lambda:re3.validate_profile(p))
check('missing_status_source',no_evidence)
check('binary_still_rejects_nonbinary',lambda:reject(lambda:re3.validate_torai_status([2],binary)))

source_job = read_pin(ref(old/'integration-001/worker-torai_B/job.json'))
source_files = {k:Path(source_job['data_root'])/v['path'] for k,v in source_job['source']['files'].items()}
tables = {k:pd.read_parquet(path) for k,path in source_files.items()}
t = source_job['t']
traces = tables['traces.parquet']
traces.loc[traces['startTime']>=t*10**6,'statusCode']=13
payload = re3.prepare_tables(tables['metrics.parquet'],traces,tables['logs.parquet'],t,grpc)

def native_sum():
    re3.validate_torai_status(payload['traces']['statusCode'],grpc)
    _,errors,_,_=torai_b.nguon_b(payload['traces'],payload['logs'],t)
    value=float(errors.to_numpy().sum())
    expected=float(payload['traces']['statusCode'].sum())
    error_spans=int((payload['traces']['statusCode']!=0).sum())
    assert value==expected and value==13*error_spans and value!=error_spans
    return {'native_sum':value,'generated_error_span_count':error_spans,'not_re3_measurement':True}
check('native_sum_is_preserved_not_binary_count',native_sum)

def worker_prep():
    data_root=OUT/'synthetic-data';data_root.mkdir()
    files={}
    for name,tab in tables.items():
        p=data_root/name;tab.to_parquet(p,index=False);files[name]=dict(ref(p),path=name)
    profile_ref=atomic(OUT/'profile-GENERATED.json',grpc)
    job=copy.deepcopy(source_job);job['data_root']=str(data_root);job['re3_profile_ref']=profile_ref
    job['source']['files']=files;job['slot']['source_sha256']=fingerprint(job['source'])
    job['fixture_origin']=atomic(OUT/'origin.json',{'schema':'T054-GENERATED-FIXTURE','scope':'invented constants from010 only'})
    attempt=OUT/'worker';attempt.mkdir();jp=atomic(attempt/'job.json',job)
    worker.main(jp['path'],str(attempt),'GENERATED-GRPC-PREP')
    prep=read_pin(ref(attempt/'prepared.json'))
    assert prep['details']['trace_error_series_semantics']=='native_sum_of_status_codes_not_error_span_count'
    assert prep['re3_profile_ref']==profile_ref
    err=pd.read_csv(prep['tables']['tracets_err']['path']).drop(columns=['time'])
    assert float(err.to_numpy().sum())==float(traces['statusCode'].sum())
    return {'status':'PREPARED','native_values_retained':True}
check('worker_grpc_prep_profile_and_csv_exact',worker_prep)
atomic(OUT/'summary.json',{'PASS':True,'checks':len(checks),'signals':'GENERATED ONLY',
                          'real_RE3_status_column_read':False,'kernel_changed':False})
print(json.dumps({'PASS':True,'checks':len(checks)}),flush=True)
