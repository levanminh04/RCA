"""Operator-only validation of v2 settling/control/pre-intervention periods."""
import datetime,json,math,sys,time
from pathlib import Path
role,phase=sys.argv[1:3]
if role not in ['app','obs'] or phase not in ['settling','normal','pre_fault']: raise SystemExit('Bad arguments')
root=Path('/home/ubuntu/t058')
plan=json.loads((root/'m1-execution-plan-v2.json').read_text())
normal=plan['planned_cases'][0]; pause=plan['planned_cases'][1]
recovery=datetime.datetime.fromisoformat(plan['recovery_confirmed_utc']).timestamp()
start=datetime.datetime.fromisoformat(normal['method_bounds_utc'][0]).timestamp()
end=datetime.datetime.fromisoformat(normal['method_bounds_utc'][1]).timestamp()
lo,hi={'settling':(recovery,start),'normal':(start,end),'pre_fault':(recovery,pause['scheduled_not_before_epoch'])}[phase]
if time.time()<hi: raise SystemExit('Window has not ended')
result={'role':role,'phase':phase,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bounds_epoch':[lo,hi]}
def records(path):
 if not path.exists(): return []
 return [json.loads(line) for line in path.read_text().splitlines(keepends=True) if line.endswith('\n')]
if role=='obs':
 rows=records(root/'light-load.jsonl')+records(root/'light-load-v2.jsonl')
 rows=[r for r in rows if lo<=r['scheduled_epoch']<hi]
 expected=set(range(math.ceil(lo),math.ceil(hi)))
 actual={int(r['scheduled_epoch']) for r in rows}
 result.update(requests=len(rows),expected_requests=len(expected),schedule_complete=actual==expected,
               non200=sum(r['status']!=200 for r in rows),client_errors=sum(bool(r['error']) for r in rows),
               maximum_lag_ms=max((r['schedule_lag_ms'] for r in rows),default=None),
               first_request=rows[0]['utc'] if rows else None,last_request=rows[-1]['utc'] if rows else None)
 result['passed']=result['schedule_complete'] and len(rows)==len(expected) and result['non200']==0 and result['client_errors']==0
else:
 expected={r['name']:r['id'] for r in json.loads((root/'jvm-memory-fix.json').read_text())['after']}
 all_rows=records(root/'memory-after-fix.jsonl')
 rows=[r for r in all_rows if lo<=r['epoch']<=hi]
 result.update(samples=len(rows),first_sample=rows[0]['utc'] if rows else None,last_sample=rows[-1]['utc'] if rows else None,
               maximum_cgroup_oom_kill=max((c['memory_events']['oom_kill'] for r in rows for c in r['containers']),default=None),
               maximum_restart_count=max((c['restart_count'] for r in rows for c in r['containers']),default=None),
               identities_unchanged=bool(rows) and all({c['name']:c['id'] for c in r['containers']}==expected for r in rows),
               every_jvm_running=bool(rows) and all(c['running'] and not c['paused'] and len(c['java_processes'])==1 for r in rows for c in r['containers']),
               note='Cgroup counters are cumulative since container creation; initial settling samples start after recovery, and zero counters also cover the preceding interval for unchanged IDs')
 result['passed']=bool(rows) and result['maximum_cgroup_oom_kill']==0 and result['maximum_restart_count']==0 and result['identities_unchanged'] and result['every_jvm_running']
target=root/('stability-'+phase+'-'+role+'.json')
if target.exists(): raise SystemExit('Refuse overwrite')
target.write_text(json.dumps(result,indent=2)+'\n')
target.chmod(0o644)
print(json.dumps(result,indent=2))
if not result['passed']: raise SystemExit('Stability check failed')
