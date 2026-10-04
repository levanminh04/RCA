"""Diagnostic depth cap in causal-learn 0.1.3.8; retains original algorithm prefix.

This is NOT pc_default. Exact source + one loop-condition change is saved.
"""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,time,inspect,hashlib,argparse,threading,traceback
from pathlib import Path
import pandas as pd,numpy as np
sys.path[:0]=['D:/RCA-flashticket/src','D:/RCA-ext/src/RCAEval']
from RCAEval.io.time_series import preprocess
from circa_kien_truc import graph_from_pc,score_graph
import causallearn.utils.PCUtils.SkeletonDiscovery as sd
from causallearn.search.ConstraintBased.PC import pc
ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=0);ap.add_argument('--alpha',type=float,default=.05);ap.add_argument('--run',default='pc-depth0-alpha005');args=ap.parse_args()
root=Path('D:/RCA-flashticket');out=root/'results/T-014';dest=out/'runs'/args.run;dest.mkdir(exist_ok=True)
case=json.loads((out/'runs/selection-before-scores.json').read_text())['selected']
row=next(r for r in json.loads((out/'runs/inventory.json').read_text()) if r['case']==case)
td=row['inject_time'];raw=pd.read_parquet(row['source'])
raw=raw.loc[:,~raw.columns.str.endswith('_latency-50')].replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
raw=raw.rename(columns={c:c.replace('_latency-90','_latency') for c in raw if c.endswith('_latency-90')})
win=pd.concat([raw[raw.time<td].tail(300),raw[raw.time>=td].head(300)],ignore_index=True)
data=preprocess(win.copy(),dataset='re2-tt');names=list(data);data['time']=win.time
source=inspect.getsource(sd.skeleton_discovery)
old='while cg.max_degree() - 1 > depth:'
assert source.count(old)==1
modified=source.replace(old,'while cg.max_degree() - 1 > depth and depth < T014_MAX_DEPTH:')
(dest/'skeleton-source-before.py').write_text(source);(dest/'skeleton-source-used.py').write_text(modified)
sd.T014_MAX_DEPTH=args.depth;exec(compile(modified,str(dest/'skeleton-source-used.py'),'exec'),sd.__dict__)
start=time.monotonic();state={'stage':'PC','depth_cap':args.depth,'alpha':args.alpha,'case':case,'columns':len(names)}
def heartbeat():
    while True:
        with (dest/'progress.jsonl').open('a') as f:f.write(json.dumps(dict(elapsed=time.monotonic()-start,**state))+'\n')
        time.sleep(15)
threading.Thread(target=heartbeat,daemon=True).start()
try:
    cg=pc(data.drop(columns='time').to_numpy().astype(float),alpha=args.alpha,show_progress=False,node_names=names)
    adj=cg.G.graph;np.save(dest/'adj.npy',adj);(dest/'names.json').write_text(json.dumps(names))
    state['pc_elapsed']=time.monotonic()-start;state['stage']='RHT'
    graph=graph_from_pc(adj,names)
    snapshot=score_graph(data,graph,td)
    (dest/'snapshot.json').write_text(json.dumps(snapshot,indent=2));state['stage']='complete';state['scores']=len(snapshot['nodes'])
    state['elapsed']=time.monotonic()-start;state['large_scores']=[k for k,v in snapshot['nodes'].items() if v['rht_score']>1e6]
    (dest/'status.json').write_text(json.dumps(state,indent=2));print(json.dumps(state))
except Exception as e:
    (dest/'error.json').write_text(json.dumps(dict(type=type(e).__name__,message=str(e),elapsed=time.monotonic()-start,**state),indent=2));traceback.print_exc();sys.exit(1)
