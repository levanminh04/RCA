"""Final inexpensive checks, without new dataset or parameter selection."""
import argparse,json,re,time,sys
from pathlib import Path
from datetime import datetime,timezone,timedelta
from unittest.mock import Mock
import pandas as pd
from simplerca import Config,diagnose
from simplerca.adapter import prepare,core_input
from run_dev import guard_case,guard_file,load_allowlist,validate_cases,ROOT,OUT,WORK,dump

parser=argparse.ArgumentParser()
parser.add_argument('--run',default='supplement-001')
parser.add_argument('--baseline-run',default='run-dev-004')
args=parser.parse_args()
allowed=load_allowlist()
data_root=ROOT/'data/rcaeval'
validate_cases(sorted(data_root.glob('re2tt_*')),allowed,data_root)
run=OUT/'runs'/args.run
if run.exists(): raise RuntimeError('preserve all attempts')
run.mkdir()
t0=time.perf_counter()
def progress(event,**kw):
    row={'time_local':datetime.now(timezone(timedelta(hours=7))).isoformat(),'event':event,**kw}
    with (run/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    print(json.dumps(row,ensure_ascii=False),flush=True)
progress('start',estimated_total_seconds=60,official_timing=False)
checked=[]
for name in allowed:
    p=data_root/name;guard_case(p,allowed,data_root)
    for filename in ('metrics.parquet','traces.parquet','logs.parquet'):
        f=p/filename
        if f.exists(): guard_file(f,p);checked.append(str(f))
for p in (WORK/allowed[0],data_root/'re2tt_unallowed_cpu_1'):
    try: guard_case(p,allowed,data_root)
    except RuntimeError: pass
    else: raise AssertionError('case escape accepted')
fake_case=Mock();fake_case.name=allowed[0];fake_case.resolve.return_value=data_root/allowed[1]
try:guard_case(fake_case,allowed,data_root)
except RuntimeError:pass
else:raise AssertionError('case identity changed inside data root')
replaced=[data_root/n for n in allowed[:-1]+['re2tt_SYNTHETIC_NOT_ALLOWED']]
try:validate_cases(replaced,allowed,data_root)
except RuntimeError:pass
else:raise AssertionError('same-count case replacement accepted')
fake=Mock();fake.resolve.return_value=WORK/'outside.parquet'
try:guard_file(fake,data_root/allowed[0])
except RuntimeError:pass
else:raise AssertionError('file escape accepted')
dump(run/'guard-check.json',{'status':'PASS','allowed_cases':len(allowed),'source_files_checked':checked,'forbidden_case_tests':2,'escaped_file_test':True,'resolved_identity_test':True,'same_count_replacement_test':True,'frozen_manifest_used':True,'data_opened_for_guard_tests':False})
progress('guard_complete',cases=len(allowed),files=len(checked))
case=allowed[1];p=data_root/case
boundary=int((WORK/'injection'/(case+'.txt')).read_text().strip())
m=pd.read_parquet(p/'metrics.parquet');t=pd.read_parquet(p/'traces.parquet',columns=['serviceName','startTime','duration']);l=pd.read_parquet(p/'logs.parquet')
inputs=core_input(prepare(m,t,l,boundary));baseline=diagnose(**inputs)
previous=json.loads((OUT/'runs'/args.baseline_run/(case+'.json')).read_text())
# Serialization turns tuples into lists, so compare JSON-normalized values.
assert json.loads(json.dumps(baseline))==previous
counts={s:sum(any(k in message.upper() for k in ('ERROR','FAIL','EXCEPTION')) for message in entries) for s,entries in inputs['incident_logs'].items()}
variants=[]
for threshold in (0,1,10):
    result=diagnose(**inputs,config=Config(log_threshold=threshold))
    for s,row in result['logs'].items():
        assert row['count']==counts.get(s,0)
        assert row['vote']==int(counts.get(s,0)>threshold)
    dump(run/f'log-threshold-{threshold}.json',result)
    variants.append({'threshold':threshold,'positive_log_services':sum(v['vote'] for v in result['logs'].values()),'ranking_same_as_baseline':result['ranks']==baseline['ranks'],'scores_same_as_baseline':result['scores']==baseline['scores']})
dump(run/'summary.json',{'case':case,'baseline_run':args.baseline_run,'baseline_matches':True,'independent_log_count_check':'PASS','variants':variants,'elapsed_seconds_concurrent_laptop':time.perf_counter()-t0,'official_timing':False})
progress('complete',elapsed_s=time.perf_counter()-t0,baseline_exact=True,variants=variants)
