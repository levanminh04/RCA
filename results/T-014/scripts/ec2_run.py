"""Bounded original PC run. All writes/caches are under task directory."""
import os,sys,json,time,threading,traceback,subprocess,argparse,signal
from pathlib import Path
from datetime import datetime,timezone,timedelta
ap=argparse.ArgumentParser()
ap.add_argument('--base',required=True);ap.add_argument('--source',required=True)
ap.add_argument('--case',required=True);ap.add_argument('--timeout',type=int,default=7200)
ap.add_argument('--worker',action='store_true');a=ap.parse_args()
base=Path(a.base).expanduser().resolve(); out=base/'runs/default-pc';out.mkdir(parents=True,exist_ok=True)
os.environ.update(PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
for var,dirname in [('XDG_CACHE_HOME','cache'),('PIP_CACHE_DIR','cache'),('MPLCONFIGDIR','cache/mpl'),('TMPDIR','tmp')]:
    d=base/dirname;d.mkdir(parents=True,exist_ok=True);os.environ[var]=str(d)
def emit(path,obj):
    with path.open('a') as f:f.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),**obj))+'\n');f.flush()
if not a.worker:
    start=time.monotonic()
    child=subprocess.Popen([sys.executable,__file__,'--base',str(base),'--source',a.source,'--case',a.case,'--worker'],stdout=(out/'worker.log').open('w'),stderr=subprocess.STDOUT,start_new_session=True)
    emit(out/'supervisor.jsonl',dict(event='start',pid=child.pid,timeout=a.timeout,case=a.case))
    import psutil
    interrupted=False;paused=False;paused_total=0.;paused_start=None
    while child.poll() is None:
        elapsed=time.monotonic()-start
        try:
            p=psutil.Process(child.pid);rss=p.memory_info().rss
            load=os.getloadavg()
            others=[]
            for q in psutil.process_iter(['pid','name','cmdline']):
                if q.pid in [os.getpid(),child.pid] or not q.info['name'].startswith(('python','Rscript')):continue
                cmd=' '.join(q.info['cmdline'] or [])
                if 'T-014' not in cmd:others.append(dict(pid=q.pid,command=cmd))
            emit(out/'supervisor.jsonl',dict(event='heartbeat',elapsed=elapsed,rss_bytes=rss,load=load,other_python=others))
            if others and not paused:
                emit(out/'supervisor.jsonl',dict(event='pause_own_worker',policy='SIGSTOP only own process group; preserve PC cache; wall time includes pause'))
                os.killpg(child.pid,signal.SIGSTOP);paused=True;paused_start=time.monotonic()
            elif not others and paused:
                paused_total+=time.monotonic()-paused_start
                emit(out/'supervisor.jsonl',dict(event='resume_own_worker',paused_total=paused_total))
                os.killpg(child.pid,signal.SIGCONT);paused=False;paused_start=None
        except psutil.NoSuchProcess:break
        if elapsed>=a.timeout:
            emit(out/'supervisor.jsonl',dict(event='timeout',elapsed=elapsed))
            os.killpg(child.pid,signal.SIGCONT);os.killpg(child.pid,signal.SIGTERM);break
        time.sleep(30)
    try: rc=child.wait(timeout=10)
    except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);rc=child.wait()
    if paused_start is not None:paused_total+=time.monotonic()-paused_start
    status=dict(returncode=rc,elapsed=time.monotonic()-start,timeout=a.timeout,case=a.case,concurrent_stop=interrupted,paused_total=paused_total,complete=(out/'scores.json').exists(),official_runtime=False if paused_total else 'instrumented EC2, no other Python observed')
    (out/'status.json').write_text(json.dumps(status,indent=2));print(json.dumps(status),flush=True)
    sys.exit(0)
sys.path.insert(0,a.source)
import numpy as np,pandas as pd,psutil
from RCAEval.io.time_series import preprocess
from RCAEval.graph_construction.pc import pc_default
from RCAEval.graph_heads.rht import rht
state=dict(stage='load',ci_calls=0,depth=None)
worker_start=time.monotonic();stop=threading.Event()
def heartbeat():
    while not stop.wait(15):
        frames=sys._current_frames()
        for fr in frames.values():
            while fr:
                if fr.f_code.co_name=='skeleton_discovery':
                    state['depth']=fr.f_locals.get('depth');state['node']=fr.f_locals.get('x')
                    cg=fr.f_locals.get('cg')
                    if cg is not None:state['remaining_max_degree']=int(cg.max_degree())
                fr=fr.f_back
        emit(out/'progress.jsonl',dict(elapsed=time.monotonic()-worker_start,rss_bytes=psutil.Process().memory_info().rss,**state))
threading.Thread(target=heartbeat,daemon=True).start()
try:
    data=pd.read_parquet(base/'data'/a.case/'metrics.parquet');td=int((base/'data'/a.case/'inject_time.txt').read_text().strip())
    data=data.loc[:,~data.columns.str.endswith('_latency-50')].replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
    data=data.rename(columns={c:c.replace('_latency-90','_latency') for c in data if c.endswith('_latency-90')})
    win=pd.concat([data[data.time<td].tail(300),data[data.time>=td].head(300)],ignore_index=True)
    clean=preprocess(win.copy(),dataset='re2-tt');names=list(clean.columns);clean['time']=win.time
    (out/'input.json').write_text(json.dumps(dict(shape=list(clean.shape),columns=names,inject=td,pc_first=float(win.time.iloc[0]),pc_last=float(win.time.iloc[-1])),indent=2))
    from causallearn.graph.GraphClass import CausalGraph
    old=CausalGraph.ci_test
    def ci(self,*args,**kwargs):state['ci_calls']+=1;return old(self,*args,**kwargs)
    CausalGraph.ci_test=ci
    state['stage']='PC';emit(out/'progress.jsonl',dict(event='PC_start',shape=[len(clean),len(names)],**state))
    tic=time.monotonic();adj=pc_default(clean.drop(columns='time'))
    np.save(out/'adj.npy',adj);(out/'nodes.json').write_text(json.dumps(names))
    emit(out/'progress.jsonl',dict(event='PC_end',pc_elapsed=time.monotonic()-tic,**state))
    state['stage']='RHT';tic=time.monotonic();scores=rht(adj,td,clean)
    (out/'scores.json').write_text(json.dumps(scores,indent=2))
    emit(out/'progress.jsonl',dict(event='RHT_end',rht_elapsed=time.monotonic()-tic,score_count=len(scores)))
except Exception as exc:
    traceback.print_exc();(out/'error.json').write_text(json.dumps(dict(type=type(exc).__name__,message=str(exc),**state),indent=2));sys.exit(1)
finally:stop.set()
