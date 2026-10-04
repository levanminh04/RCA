"""Capture actual RHT frames on EC2; no PC rerun and no replacement math."""
import os,sys,json,time,types
from pathlib import Path
BASE=Path('/home/ubuntu/rca/T-014');CASE='re2tt_ts-order-service_loss_3'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',TMPDIR=str(BASE/'tmp'),XDG_CACHE_HOME=str(BASE/'cache'),MPLCONFIGDIR=str(BASE/'cache/mpl'))
sys.path.insert(0,str(BASE/'src'))
import numpy as np,pandas as pd
from RCAEval.io.time_series import preprocess
from RCAEval.graph_heads.rht import rht
dest=BASE/'runs/normal-normal-pc-official-capture';dest.mkdir(exist_ok=True);start=time.monotonic()
raw=pd.read_parquet(BASE/'data'/CASE/'metrics.parquet');true_td=int((BASE/'data'/CASE/'inject_time.txt').read_text())
raw=raw.loc[:,~raw.columns.str.endswith('_latency-50')].replace([np.inf,-np.inf],np.nan).ffill().fillna(0);raw=raw.rename(columns={c:c.replace('_latency-90','_latency') for c in raw if c.endswith('_latency-90')})
normal=raw[raw.time<true_td].copy();clean=preprocess(normal,dataset='re2-tt');names=list(clean);clean['time']=normal.time.to_numpy();td=true_td-301
adj=np.load(BASE/'runs/ec2-2-normal/adj.npy');assert names==json.loads((BASE/'runs/ec2-2-normal/nodes.json').read_text())
records={};last_reg={};last_scale={};graph_info={};context={}
def label(n):return n.entity+'_'+n.metric
def profile(frame,event,arg):
    global last_reg,last_scale,graph_info,context
    if event!='return' or not frame.f_code.co_filename.endswith('rht.py'):return
    loc=frame.f_locals;name=frame.f_code.co_name
    if name=='zscore' and 'scaler' in loc:
        sc=loc['scaler'];last_scale=dict(mean=float(sc.mean_[0]),variance=float(sc.var_[0]),scale=float(sc.scale_[0]),z=np.asarray(arg).tolist())
    elif name=='_score' and 'train_x' in loc and 'train_err' in loc:
        model=loc['self']._regressor
        last_reg=dict(train_x_id=id(loc['train_x']),pe=loc['train_err'].tolist(),te=loc['test_err'].tolist(),coefficient=model.coef_.tolist(),intercept=float(model.intercept_))
    elif name=='score_node' and arg is not None:
        node=loc['node'];px=loc['train_x'];tx=loc['test_x'];py=loc['train_y'];ty=loc['test_y'];parents=[p for p in loc['parents'] if p in loc['series']]
        has_reg=bool(len(px) and last_reg.get('train_x_id')==id(px));fallback=not has_reg
        records[label(node)]=dict(parents=[label(p) for p in parents],train_x=px.tolist(),test_x=tx.tolist(),train_y=py.tolist(),test_y=ty.tolist(),x_memory_order='F' if px.flags.f_contiguous or px.strides[0]<=px.strides[1] else 'C',rht_score=float(arg.score),confidence=float(arg['Confidence']),official_train_residual=last_reg['pe'] if has_reg else py.tolist(),official_test_residual=last_reg['te'] if has_reg else ty.tolist(),coefficient=last_reg['coefficient'] if has_reg else [],intercept=last_reg['intercept'] if has_reg else None,residual_mean=last_scale['mean'],residual_var=last_scale['variance'],residual_scale=last_scale['scale'],z=last_scale['z'],regression_fallback=fallback,regression_route='linear_regression' if has_reg else ('no_effective_parents' if not len(px) else 'value_error_fallback'),regression_error=None)
        g=loc['graph'];case=loc['data'];context=dict(detect_time=td,current=td+300,train_window=case.train_window,test_window=case.test_window,score_mode='actual RCAEval rht frame capture, RHT only; no DA run',candidate_unit='metric')
        graph_info=dict(nodes=sorted(label(n) for n in g.nodes),edges=sorted([label(a),label(b)] for a,b in g.edges),topological_groups=[])
np.random.seed(0);sys.setprofile(profile)
try:scores=rht(adj,td,clean)
finally:sys.setprofile(None)
original=dict(json.loads((BASE/'runs/ec2-2-normal/scores.json').read_text()));current=dict(scores)
assert set(original)==set(current)==set(records)
assert all(original[k]==current[k] for k in original),'Original RHT same-host repeat changed'
snapshot=dict(meta=context,graph=graph_info,nodes=records,da={},ranks=scores,ranks_da=[])
(dest/'snapshot.json').write_text(json.dumps(snapshot,indent=2));(dest/'capture-status.json').write_text(json.dumps(dict(actual_rht_same_host_repeat_exact=True,count=len(scores),elapsed_diagnostic=time.monotonic()-start,source='sys.setprofile captures return frames of unchanged rht.py; no re-fit or approximation; RHT only'),indent=2))
print(json.dumps(dict(count=len(scores),repeat_exact=True,elapsed=time.monotonic()-start)))
