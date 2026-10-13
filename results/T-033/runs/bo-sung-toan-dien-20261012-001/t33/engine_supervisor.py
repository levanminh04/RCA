"""Independent engine queue; second worker after original-thread theta finishes."""
import json,pathlib,time,sys
import psutil
from supervisor import P,append,run,wait
p0=run('engine-part0',['worker-v3.py','engines','0'])
theta_pid=int((P/'theta-v3.pid').read_text())
while True:
 try:
  q=psutil.Process(theta_pid)
  if q.status()==psutil.STATUS_ZOMBIE or not any('theta-v3.py' in x for x in q.cmdline()):break
 except psutil.Error:break
 code=p0[0].poll()
 if code is not None and code!=0:
  append({'event':'ENGINE_NATIVE_DEPENDENCY_STOP','pid':p0[0].pid,'exit':code});raise SystemExit(code)
 (P/'engine-queue-status.json').write_text(json.dumps({'engine_part0_pid':p0[0].pid,'waiting_theta_original_thread_pid':theta_pid,'utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'disk_free_bytes':psutil.disk_usage(P).free,'ram_available_bytes':psutil.virtual_memory().available},indent=2))
 time.sleep(10)
p1=run('engine-part1',['worker-v3.py','engines','1'])
ok=wait([p0,p1]);append({'event':'ENGINE_QUEUE_FINISHED','status':'COMPLETE' if ok else 'FAILED_WITH_PRESERVED_OUTPUTS'})
