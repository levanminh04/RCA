"""Descriptive post-hash analysis; preserve the original confirmed-time bins."""
import datetime,json
from pathlib import Path
root=Path(__file__).resolve().parent
ledger=[json.loads(x) for x in (root/'so-tiem-loi.jsonl').read_text(encoding='utf8').splitlines()]
start,end=ledger
requested=start['requested']['epoch_ns']/1e9; confirmed=start['confirmed']['epoch_ns']/1e9
recovered=end['confirmed']['epoch_ns']/1e9
rows=[]
for filename,offset in [('light-load.jsonl',0),('light-load-v2.jsonl',3600)]:
 for line in (root/filename).read_text().splitlines():
  row=json.loads(line);row['sequence']+=offset;rows.append(row)
rows.sort(key=lambda r:r['sequence'])
paths=sorted({r['path'] for r in rows})
by_path={}
for path in paths:
 selected=[r for r in rows if r['path']==path]
 bad=[r for r in selected if r['epoch']>=requested and r['status']!=200]
 last=max((r['completed_epoch'] for r in bad),default=recovered)
 success=[r for r in selected if r['epoch']>=max(recovered,last) and r['status']==200]
 by_path[path]={'non200_after_command_requested':len(bad),
                'first_non200_request':bad[0] if bad else None,
                'last_non200_request':bad[-1] if bad else None,
                'first_200_started_after_recovery_and_last_failure_completed':success[0] if success else None,
                'note':'For a path with no failure, this is continued availability, not evidence of recovery'}
clean=[r for r in rows if requested-300<=r['epoch']<requested]
straddle=[r for r in rows if requested<=r['epoch']<confirmed]
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'original_bins_preserved':'load-impact.json groups by actual client start against Docker confirmation; not rewritten',
        'command_request_epoch':requested,'docker_confirmation_epoch':confirmed,
        'command_confirmation_bracket_seconds':confirmed-requested,
        'requests_started_between_request_and_confirmation':straddle,
        'before_command_request_5m':{'requests':len(clean),'non200':sum(r['status']!=200 for r in clean)},
        'by_path':by_path,
        'plan_v2_assumption_correction':{'claim':'All three read paths reach event-service',
          'finding':'False: gateway routes /api/v1/events/*/availability to booking-service; catalog/detail to event-service',
          'evidence':['Gateway application.yaml route predicates','load-impact.json#/windows/during/by_path'],
          'treatment':'Keep frozen plan v2 unchanged; annotate after-output correction; do not change method input, t, thresholds or workload'},
        'limits':['Client request start/completion and Docker request/confirmation bracket the observations; no exact application impact onset is inferred',
                  'The total 4800-request log includes earlier OOM/reconfiguration failures; do not attribute them all to the deliberate pause',
                  'Availability remained 200 during the pause, so its success is not a recovery marker for event-service']}
(root/'load-impact-detail.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(root/'m1-plan-v2-deviations.json').write_text(json.dumps({'utc':result['utc'],'original_plan_preserved':True,
    'correction':result['plan_v2_assumption_correction'],'method_or_workload_changed':False},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Before command request:',result['before_command_request_5m'],'straddle',len(straddle))
for path,d in by_path.items():
 r=d['first_200_started_after_recovery_and_last_failure_completed']
 print(path,'non200 after command',d['non200_after_command_requested'],'later 200',r['utc'] if r else None)
