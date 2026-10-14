"""Metadata/resource forecast only. Never runs a method, comparator or bridge."""
import hashlib
import json
import os
import time
from pathlib import Path

ROOT=Path('D:/RCA-flashticket/results/T-032')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
transport=read(ROOT/'runs/microrank-cohort-failure-001/transport-check.json')
assert transport['status']=='PASS' and len(transport['files'])==15
checks=[]
for row in transport['files']:
 p=Path(row['local']);assert ROOT in p.resolve().parents
 assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes']
 checks.append({'path':str(p),'sha256':row['sha256'],'pass':True})
pp=ROOT/'runs/tiep-tuc-003/microrank-plan-001.json'
assert sha(pp)=='5cd51540018115e94db163c22ef9ab56627c3ae073104bc1a850d5c65881f05e'
plan=read(pp)
table=read(ROOT/'runs/microrank-cohort-failure-001/cohort/52-cases.json')
rows=table['rows'];assert len(rows)==52
remaining={(r['dataset'],r['opaque_id']) for r in rows if r['classification']=='not_run'}
assert len(remaining)==41
estimates=[r for r in plan['estimate']['cases'] if (r['dataset'],r['opaque_id']) in remaining]
assert len(estimates)==41
files=0;local_bytes=0
for parent,dirs,names in os.walk(ROOT):
 for name in names:
  p=Path(parent)/name
  if p.is_symlink():raise RuntimeError('symlinked T032 output')
  local_bytes+=p.stat().st_size;files+=1
remote=read(ROOT/'runs/preflight-trace-path-001.json')
assert not remote['processes']
expected_bytes=sum(r['new_bytes'] for r in estimates)
output={
 'status':'PROPOSAL_ONLY_NOT_APPROVED_NOT_STARTED','measured_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
 'remaining_case_count':41,'remaining_by_dataset':{d:sum(ds==d for ds,_ in remaining) for d in ['RE2-TT','Nezha-OB']},
 'remaining_estimated_seconds':sum(r['seconds'] for r in estimates),
 'remaining_estimated_remote_bytes':expected_bytes,
 'remaining_estimated_peak_tree_rss_bytes':max(r['peak_rss_bytes'] for r in estimates),
 'estimate_status':'CHUA_KIEM_FULL_41; unchanged prior 2x pilot/source ratios, not a bound or new benchmark',
 'measured_local_task_bytes':local_bytes,'local_file_count':files,
 'measured_ec2':remote,'current_combined_bytes':local_bytes+remote['remote_task_bytes'],
 'prospective_combined_bytes_with_full_download_and_200MiB_archive_reserve':local_bytes+remote['remote_task_bytes']+2*expected_bytes+200*2**20,
 'global_ceiling_bytes':8*2**30,
 'require_fresh_resources_after_trace_pilots_before_launch':True,
 'no_native_or_comparator_executed':True,'source_checks':checks,
 'plan_path':str(pp),'plan_sha256':sha(pp),'cases':estimates,
 'blocker':'Existing blocked ca has t028_flags=NOT_PERFORMED; cannot continue until new independent diagnostic flag audit passes under explicit approval.'}
out=ROOT/'runs/microrank-continue41-proposal-001'
out.mkdir(exist_ok=False)
with (out/'forecast.json').open('x',encoding='utf-8') as f:json.dump(output,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({k:v for k,v in output.items() if k not in ['cases','source_checks']},ensure_ascii=False),flush=True)
