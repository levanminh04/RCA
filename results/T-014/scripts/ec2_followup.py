"""Same-revision PC checks on one allowed case, bounded aggregate active wall."""
import os,sys,json,time,hashlib,signal,subprocess,argparse,threading,traceback,types,importlib.metadata as md
from pathlib import Path
from datetime import datetime,timezone
BASE=Path('/home/ubuntu/rca/T-014'); CASE='re2tt_ts-order-service_loss_3'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',TMPDIR=str(BASE/'tmp'),XDG_CACHE_HOME=str(BASE/'cache'),MPLCONFIGDIR=str(BASE/'cache/mpl'))
ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['preflight','permuted','normal','supervisor'],required=True);ap.add_argument('--limit',type=float);a=ap.parse_args()
def emit(path,**obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a') as f:f.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),**obj))+'\n');f.flush()
def other_jobs(own):
    import psutil
    found=[]
    for p in psutil.process_iter(['pid','name','cmdline','cpu_percent','memory_info']):
        try:
            cmd=' '.join(p.info['cmdline'] or [])
            if p.pid not in own and p.info['name'].startswith(('python','Rscript','R')) and '/rca/T-014/' not in cmd: found.append(dict(pid=p.pid,cmd=cmd,rss=p.info['memory_info'].rss))
        except (psutil.NoSuchProcess,psutil.AccessDenied):pass
    return found
if a.mode=='supervisor':
    import psutil
    old=5675.098176376;reserve=900.;limit=10800.-old-reserve-10.;used=0.
    statuses=[]
    for mode in ['permuted','normal']:
        dest=BASE/'runs'/('ec2-2-'+mode);dest.mkdir(parents=True,exist_ok=True)
        cap=min(2100.,limit-used) if mode=='permuted' else limit-used
        if cap<=0:break
        queue_start=time.monotonic()
        while True:
            others=other_jobs({os.getpid()});available=psutil.virtual_memory().available
            emit(dest/'supervisor.jsonl',event='queue',other_jobs=others,available_bytes=available,queue_seconds=time.monotonic()-queue_start)
            if not others and available>6*1024**3:break
            if time.monotonic()-queue_start>600:
                (dest/'status.json').write_text(json.dumps(dict(complete=False,reason='second host busy; no worker started',active_wall_seconds=0,queue_seconds=time.monotonic()-queue_start),indent=2));sys.exit(0)
            time.sleep(15)
        start=time.monotonic();child=subprocess.Popen([sys.executable,__file__,'--mode',mode],stdout=(dest/'worker.log').open('w'),stderr=subprocess.STDOUT,start_new_session=True)
        emit(dest/'supervisor.jsonl',event='start',pid=child.pid,active_cap_seconds=cap)
        paused=False;paused_at=None;pause_total=0.;timeout=False;deadline=start+cap
        while child.poll() is None:
            now=time.monotonic();others=other_jobs({os.getpid(),child.pid})
            try:rss=psutil.Process(child.pid).memory_info().rss
            except psutil.NoSuchProcess:break
            emit(dest/'supervisor.jsonl',event='heartbeat',wall_seconds=now-start,active_seconds=now-start-pause_total-(now-paused_at if paused else 0),rss_bytes=rss,load=os.getloadavg(),other_jobs=others)
            if others and not paused:os.killpg(child.pid,signal.SIGSTOP);paused=True;paused_at=now;emit(dest/'supervisor.jsonl',event='pause_own_worker')
            elif not others and paused:
                delta=now-paused_at;pause_total+=delta;deadline+=delta;os.killpg(child.pid,signal.SIGCONT);paused=False;paused_at=None;emit(dest/'supervisor.jsonl',event='resume_own_worker')
            if (not paused and now>=deadline) or now-start>=5400:
                timeout=True;os.killpg(child.pid,signal.SIGCONT);os.killpg(child.pid,signal.SIGTERM);emit(dest/'supervisor.jsonl',event='timeout');break
            time.sleep(min(5,max(.1,deadline-time.monotonic())))
        try:rc=child.wait(timeout=5)
        except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);rc=child.wait()
        end=time.monotonic()
        if paused_at is not None:pause_total+=end-paused_at
        active=end-start-pause_total;used+=active
        status=dict(mode=mode,returncode=rc,complete=(dest/'scores.json').exists() and rc==0,active_wall_seconds=active,wall_seconds=end-start,queue_seconds=start-queue_start,pause_seconds=pause_total,cap_seconds=cap,timeout=timeout,official_runtime=False,case=CASE)
        (dest/'status.json').write_text(json.dumps(status,indent=2));statuses.append(status)
        emit(BASE/'runs/followup-supervisor.jsonl',event='block_terminal',**status)
    (BASE/'runs/followup-cost.json').write_text(json.dumps(dict(old_worker_wall_seconds=old,reservation_seconds=reserve,new_worker_wall_seconds=used,total_with_reservation_seconds=old+reserve+used,limit_seconds=10800,under_limit=old+reserve+used<=10800,statuses=statuses),indent=2));sys.exit(0)
sys.path.insert(0,str(BASE/'src'))
# Avoid graph_construction.__init__ importing unrelated RCA methods. The leaf PC source is unchanged.
pkg=types.ModuleType('RCAEval.graph_construction');pkg.__path__=[str(BASE/'src/RCAEval/graph_construction')];sys.modules['RCAEval.graph_construction']=pkg
import numpy as np,pandas as pd,psutil
from RCAEval.io.time_series import preprocess
from RCAEval.graph_construction.pc import pc_default
from RCAEval.graph_heads.rht import rht
source_files=['RCAEval/graph_construction/pc.py','RCAEval/io/time_series.py','RCAEval/graph_heads/rht.py','RCAEval/classes/data.py','RCAEval/classes/graph.py']
if a.mode=='preflight':
    report=dict(python=sys.version,packages={p:md.version(p) for p in ['numpy','pandas','scipy','scikit-learn','causal-learn','networkx','pyarrow','psutil','matplotlib']},source_sha256={f:hashlib.sha256((BASE/'src'/f).read_bytes()).hexdigest() for f in source_files},case_source_sha256=hashlib.sha256((BASE/'data'/CASE/'metrics.parquet').read_bytes()).hexdigest(),seed=0,import_route='namespace only skips unused constructor imports; leaf PC/preprocess/RHT files unchanged')
    (BASE/'environment-followup.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));sys.exit(0)
dest=BASE/'runs'/('ec2-2-'+a.mode);dest.mkdir(parents=True,exist_ok=True)
state=dict(stage='load',ci_calls=0,depth=None);start=time.monotonic();stop=threading.Event()
def heartbeat():
    while not stop.wait(15):
        for f in sys._current_frames().values():
            while f:
                if f.f_code.co_name=='skeleton_discovery':state.update(depth=f.f_locals.get('depth'),node=f.f_locals.get('x'))
                f=f.f_back
        emit(dest/'progress.jsonl',elapsed=time.monotonic()-start,rss_bytes=psutil.Process().memory_info().rss,**state)
threading.Thread(target=heartbeat,daemon=True).start()
try:
    raw=pd.read_parquet(BASE/'data'/CASE/'metrics.parquet');true_td=int((BASE/'data'/CASE/'inject_time.txt').read_text())
    raw=raw.loc[:,~raw.columns.str.endswith('_latency-50')].replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
    raw=raw.rename(columns={c:c.replace('_latency-90','_latency') for c in raw if c.endswith('_latency-90')})
    if a.mode=='normal':td=true_td-301;win=raw[raw.time<true_td].copy()
    else:td=true_td;win=pd.concat([raw[raw.time<td].tail(300),raw[raw.time>=td].head(300)],ignore_index=True)
    clean=preprocess(win.copy(),dataset='re2-tt')
    if a.mode=='permuted':clean=clean.loc[:,list(reversed(clean.columns))]
    names=list(clean);clean['time']=win.time.to_numpy();np.random.seed(0)
    (dest/'input.json').write_text(json.dumps(dict(shape=[len(clean),len(names)],columns=names,detect_time=td,true_inject_time=true_td,current=td+300,pc_first=float(win.time.min()),pc_last=float(win.time.max()),normal_proxy=a.mode=='normal'),indent=2))
    from causallearn.graph.GraphClass import CausalGraph
    old_ci=CausalGraph.ci_test
    def ci(self,*args,**kw):state['ci_calls']+=1;return old_ci(self,*args,**kw)
    CausalGraph.ci_test=ci;state['stage']='PC';tic=time.monotonic();emit(dest/'progress.jsonl',event='PC_start',**state)
    adj=pc_default(clean.drop(columns='time'));np.save(dest/'adj.npy',adj);(dest/'nodes.json').write_text(json.dumps(names));emit(dest/'progress.jsonl',event='PC_end',pc_elapsed=time.monotonic()-tic,**state)
    state['stage']='RHT';tic=time.monotonic();scores=rht(adj,td,clean);(dest/'scores.json').write_text(json.dumps(scores,indent=2));emit(dest/'progress.jsonl',event='RHT_end',rht_elapsed=time.monotonic()-tic,score_count=len(scores))
except Exception as e:
    traceback.print_exc();(dest/'error.json').write_text(json.dumps(dict(type=type(e).__name__,message=str(e),**state),indent=2));sys.exit(1)
finally:stop.set()
