"""Stop loaded v3 workers only after all branches of their last owned case."""
import datetime,json,os,pathlib,signal,time
import psutil
P=pathlib.Path(__file__).resolve().parent
targets={51071:('engine-part0.stdout',13),51840:('engine-part1.stdout',14)}
source=json.loads((P/'migration-inputs-001/manifest.json').read_text())
branch=['prior_df4','prior_kappa4','prior_precision4','causal_fixed','causal_expanding','compressed_row','compressed_calendar']
for pid,(log,last) in targets.items():
 p=P/('migration-boundary-'+str(pid)+'.json');assert not p.exists()
while targets:
 for pid,(log,last) in list(targets.items()):
  try:
   proc=psutil.Process(pid);cmd=proc.cmdline()
   if proc.status()==psutil.STATUS_ZOMBIE:raise psutil.NoSuchProcess(pid)
  except psutil.NoSuchProcess:
   (P/('migration-boundary-'+str(pid)+'.json')).write_text(json.dumps({'status':'PROCESS_ALREADY_EXITED','pid':pid,'last_owned_case':last,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2));del targets[pid];continue
  assert 'worker-v3.py' in cmd and 'engines' in cmd,(pid,cmd)
  rows=[]
  for line in (P/log).read_text().splitlines():
   try:rows.append(json.loads(line))
   except json.JSONDecodeError:pass
  current=next((x for x in reversed(rows) if x.get('state')=='START'),None)
  if current is None or current['case']<=14:continue
  oid=source['cases'][last-1]['opaque_id']
  outputs=[]
  for b in branch:
   q=P/(oid+'--'+b+'.json');v=json.loads(q.read_text());assert v['status']=='PASS';outputs.append(q.name)
  sham=json.loads((P/(oid+'--full-sham-thread1.json')).read_text());assert sham['native_full_sham_exact']
  assert current['branch']=='native-full-sham-thread1',(pid,current)
  proc.send_signal(signal.SIGSTOP)
  receipt={'status':'OWNED_CASES_COMPLETE_PROCESS_INTERRUPTED_AT_UNOWNED_NATIVE_START','pid':pid,'cmdline':cmd,'last_owned_case':last,'last_owned_outputs':outputs,'interrupted_start':current,'elapsed_s':time.time()-proc.create_time(),'cpu_times':proc.cpu_times()._asdict(),'rss':proc.memory_info().rss,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scientific_meaning':'No owned branch killed or result removed. Unowned native attempt START is retained, not complete. Case15–30 ownership moved to EC2 T32.'}
  (P/('migration-boundary-'+str(pid)+'.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
  proc.send_signal(signal.SIGTERM);proc.send_signal(signal.SIGCONT)
  print(json.dumps(receipt,ensure_ascii=False),flush=True);del targets[pid]
 time.sleep(.5)
(P/'migration-boundary-complete.json').write_text(json.dumps({'status':'COMPLETE','owned_cases':list(range(1,15)),'delegated_cases':list(range(15,31))},indent=2)+'\n')
