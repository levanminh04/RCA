"""Account saved run durations, pauses/waits, RSS and predeclared reservations."""
from pathlib import Path
import json
out=Path('D:/RCA-flashticket/results/T-014');runs=out/'runs'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jl(p):return [json.loads(l) for l in p.read_text(encoding='utf-8-sig').splitlines() if l.strip()]
attempts=[]
for name in ['ec2-default-001','ec2-default-002','ec2-default-003','ec2-default-permuted']:
    p=runs/name/'status.json'
    if p.exists():
        s=load(p);attempts.append(dict(name=name,status_source=str(p),elapsed_seconds=s['elapsed'],complete=s['complete'],status=s))
default_total=sum(a['elapsed_seconds'] for a in attempts)
progress=jl(runs/'ec2-default-003/progress.jsonl');supervisor=jl(runs/'ec2-default-003/supervisor.jsonl')
last=load(runs/'pc-depth0-alpha005/status.json')['last_progress']['elapsed']
pc_end=next(r for r in progress if r.get('event')=='PC_end')
rht_end=next(r for r in progress if r.get('event')=='RHT_end')
graph_time=sum(r.get('elapsed_diagnostic',0) for r in jl(runs/'build-progress.jsonl'))
score_time=sum(r.get('elapsed_diagnostic',0) for r in jl(runs/'example-progress.jsonl'))
cost=dict(predeclared=dict(default_PC_seconds=7200,capped_PC_seconds=2700,other_PC_checks_reservation_seconds=900,total_PC_dataset_seconds=10800),default_attempts=attempts,default_total_seconds=default_total,default_complete=any(a['complete'] for a in attempts),permutation_terminal=(runs/'ec2-default-permuted/status.json').exists(),
    capped_PC_actual_seconds=last,capped_status_source=str(runs/'pc-depth0-alpha005/status.json'),
    PC_dataset_accounting_with_full_other_reservation_seconds=default_total+last+900,
    PC_dataset_under_3h_with_reservation=(default_total+last+900)<=10800,
    completed_default=dict(pc_seconds=pc_end['pc_elapsed'],rht_seconds=rht_end['rht_elapsed'],CI_calls=pc_end['ci_calls'],last_observed_depth=pc_end['depth'],depth_warning='Last sampled depth, not a proof of the maximum depth visited',peak_observed_RSS_bytes=max(r.get('rss_bytes',0) for r in progress+supervisor),time_official=False,time_caveat='Instrumented run on shared host; no other Python observed, background load not excluded'),
    architecture=dict(build_all_logged_seconds=graph_time,example_scoring_snapshot_logged_seconds=score_time,source_logs=['runs/build-progress.jsonl','runs/example-progress.jsonl'],caveat='Diagnostic aggregate of logged operations; includes failed/repeated operations when logged. Hashseed/native-check wall timings without duration fields are not inferred. This is not a clean benchmark.'),
    missing_durations='Some small fixture/YAML-equivalence checks have outputs/logs but no isolated wall timer; only predeclared reservation is used for PC, not invented runtime.',
    monetary_cost='chua_kiem: instance is shared and task has no isolated billed-use interval or verified price; no dollar estimate inferred',
    no_new_dataset_download=True)
audit=out/'audit/cost-summary.json'
if audit.exists():cost['audit_fseOB']=load(audit)
(runs/'chi-phi-tong.json').write_text(json.dumps(cost,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:cost[k] for k in ['default_total_seconds','capped_PC_actual_seconds','PC_dataset_accounting_with_full_other_reservation_seconds','PC_dataset_under_3h_with_reservation','permutation_terminal']}))
