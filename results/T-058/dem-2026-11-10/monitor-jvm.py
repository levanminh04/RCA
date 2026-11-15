"""Light operator monitor: cgroup OOM counters survive JVM automatic restarts."""
import datetime,json,subprocess,sys,time
from pathlib import Path
seconds=int(sys.argv[1]); path=Path('/home/ubuntu/t058/memory-after-fix.jsonl')
if path.exists(): raise SystemExit('Refuse overwrite')
start=time.monotonic()
while time.monotonic()-start<=seconds:
 ids=subprocess.check_output(['docker','ps','-aq'],text=True).split(); records=[]
 for c in json.loads(subprocess.check_output(['docker','inspect',*ids])):
  if not c['Config']['Image'].startswith('ft-local/'): continue
  group=Path('/sys/fs/cgroup/system.slice')/('docker-'+c['Id']+'.scope')
  events=dict((line.split()[0],int(line.split()[1])) for line in (group/'memory.events').read_text().splitlines())
  processes=[]
  for pid in (group/'cgroup.procs').read_text().split():
   proc=Path('/proc')/pid
   try:
    if proc.joinpath('comm').read_text().strip()!='java': continue
    status=dict(line.split(':',1) for line in proc.joinpath('status').read_text().splitlines() if ':' in line)
    processes.append({'pid':int(pid),'rss_kib':int(status['VmRSS'].split()[0]),'rss_anon_kib':int(status['RssAnon'].split()[0])})
   except FileNotFoundError: pass
  records.append({'name':c['Name'],'id':c['Id'],'limit_bytes':c['HostConfig']['Memory'],'memory_current_bytes':int((group/'memory.current').read_text()),
                  'memory_peak_bytes':int((group/'memory.peak').read_text()),'memory_events':events,
                  'restart_count':c['RestartCount'],'running':c['State']['Running'],'paused':c['State']['Paused'],'java_processes':processes})
 row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'epoch':time.time(),'containers':records}
 with path.open('a') as stream: stream.write(json.dumps(row,separators=(',',':'))+'\n')
 print(row['utc'],'oom_kill',sum(r['memory_events']['oom_kill'] for r in records),'restarts',sum(r['restart_count'] for r in records),flush=True)
 time.sleep(15)
Path('/home/ubuntu/t058/memory-after-fix.done').touch()
