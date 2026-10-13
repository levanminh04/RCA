"""Swap to verified targeted extraction; preserve old attempt/process metadata."""
import datetime,json,os,pathlib,signal,subprocess,sys,time
import psutil
P=pathlib.Path(__file__).resolve().parent
old=int((P/'theta-v3.pid').read_text());proc=psutil.Process(old)
assert any('theta-v3.py' in x for x in proc.cmdline()),'Only the authorized old diagnostic PID'
meta={'old_pid':old,'old_cmdline':proc.cmdline(),'old_create_time':proc.create_time(),'old_cpu_seconds':sum(proc.cpu_times()[:2]),'paused_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'Targeted-state pilot four sources exacttheta/nativePDF, 0.3–1.6s vsfullupdate12–48s; keep every output and stopped attempt'}
(P/'theta-switch-001.json').write_text(json.dumps(meta,indent=2));proc.suspend()
f=(P/'theta-target-all.stdout').open('xb');e=(P/'theta-target-all.stderr').open('xb')
q=subprocess.Popen([sys.executable,'-B','-X','utf8',str(P/'target_theta.py')],cwd=P,stdin=subprocess.DEVNULL,stdout=f,stderr=e,start_new_session=True)
(P/'theta-target-all.pid').write_text(str(q.pid));t=time.perf_counter();code=q.wait()
meta.update(target_pid=q.pid,target_exit=code,target_wall_s=time.perf_counter()-t,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(P/'theta-switch-result-001.json').write_text(json.dumps(meta,indent=2))
if code==0:
 # Original slow attempt is intentionally ended only after successful target.
 proc.terminate();proc.resume()
 print('Targeted complete; slow attempt ended, enginepart1 coordinator may continue',flush=True)
else:
 print('Targeted failed; old diagnostic remains paused; notify root, no automatic retry or resume',flush=True)
 raise SystemExit(code)
