"""Detached finite queue; no retries or source mutation. Small progress output."""
import datetime,json,os,pathlib,subprocess,sys,time,traceback
import psutil
P=pathlib.Path(__file__).resolve().parent
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def append(x):
 x['utc']=stamp()
 with (P/'supervisor-events.jsonl').open('a') as f:f.write(json.dumps(x)+'\n')
 print(json.dumps(x),flush=True)
def run(name,args):
 out=(P/(name+'.stdout')).open('xb');err=(P/(name+'.stderr')).open('xb')
 env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
 p=subprocess.Popen([sys.executable,'-B','-X','utf8']+args,cwd=P,stdout=out,stderr=err,stdin=subprocess.DEVNULL,env=env,start_new_session=True)
 append({'event':'START','name':name,'pid':p.pid,'args':args,'thread_env':{k:env[k] for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']}})
 return p,time.perf_counter(),name
def wait(processes):
 active=list(processes);bad=False;peak={x[2]:0 for x in active}
 while active:
  for x in list(active):
   p,t,name=x;code=p.poll()
   if code is not None:
    append({'event':'END','name':name,'pid':p.pid,'exit':code,'wall_s':time.perf_counter()-t,'peak_rss_bytes':peak[name]});bad|=code!=0;active.remove(x)
   else:
    try:peak[name]=max(peak[name],psutil.Process(p.pid).memory_info().rss)
    except psutil.Error:pass
  (P/'queue-status.json').write_text(json.dumps({'utc':stamp(),'active':[{'name':n,'pid':p.pid,'wall_s':time.perf_counter()-t,'peak_rss_bytes':peak[n]} for p,t,n in active],'failed_stage':bad,'disk_free_bytes':psutil.disk_usage(P).free,'ram_available_bytes':psutil.virtual_memory().available},indent=2))
  if psutil.disk_usage(P).free<100*2**20:
   for p,t,n in active:p.terminate()
   append({'event':'DISK_STOP','threshold_bytes':100*2**20});raise RuntimeError('Disk under100MiB; keep all attempts')
  if active:time.sleep(10)
 return not bad
if __name__=='__main__':
 append({'event':'SUPERVISOR_START','pid':os.getpid(),'queue':['context-fast-v2','theta','engine-part0','engine-part1']})
 if not wait([run('context-fast-v3-check',['context.py','fast'])]):raise SystemExit('STOP context failed')
 if not wait([run('theta-v2',['theta-v2.py','theta'])]):raise SystemExit('STOP theta failed')
 ok=wait([run('engine-part0',['worker-v3.py','engines','0']),run('engine-part1',['worker-v3.py','engines','1'])])
 append({'event':'QUEUE_FINISHED','status':'COMPLETE' if ok else 'FAILED_WITH_PRESERVED_OUTPUTS'})
