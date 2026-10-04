"""Same fixed architecture/context, original CIRCA vs saved RCAEval scorer.

No graph learning, no root label evaluation. Also reverses each node's parent
list explicitly; input column permutation alone does not exercise this path.
"""
import os
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('MKL_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import sys,json,time,csv,copy
from datetime import datetime,timedelta
from pathlib import Path
sys.dont_write_bytecode=True
sys.path[:0]=['D:/RCA-ext/work/T-014/CIRCA','D:/RCA-ext/src/RCAEval']
out=Path('D:/RCA-flashticket/results/T-014/audit')
tic=time.perf_counter()
print(datetime.now().isoformat(),'START same-graph original architecture and parent-order probe; estimate <60s; shared timing diagnostic',flush=True)
import numpy as np,pandas as pd,networkx as nx
from RCAEval.io.time_series import preprocess
from circa.alg.ci import RHTScorer,DAScorer
from circa.model.case import CaseData
from circa.model.data_loader import MemoryDataLoader
from circa.model.graph import MemoryGraph,Node
root=out.parent
selected=json.loads((root/'runs/selection-before-scores.json').read_text())['selected']
assert selected.startswith('re2tt_')
row=next(r for r in json.loads((root/'runs/inventory.json').read_text()) if r['case']==selected)
snapshot=json.loads((root/'runs/example-architecture/snapshot.json').read_text())
raw=pd.read_parquet(row['source']);td=row['inject_time']
raw=raw.loc[:,~raw.columns.str.endswith('_latency-50')].replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
raw=raw.rename(columns={c:c.replace('_latency-90','_latency') for c in raw if c.endswith('_latency-90')})
win=pd.concat([raw[raw.time<td].tail(300),raw[raw.time>=td].head(300)],ignore_index=True)
clean=preprocess(win.copy(),dataset='re2-tt');clean['time']=win.time
node_by_name={name:Node(*name.rsplit('_',1)) for name in snapshot['graph']['nodes']}
g=nx.DiGraph();g.add_nodes_from(node_by_name.values());g.add_edges_from((node_by_name[a],node_by_name[b]) for a,b in snapshot['graph']['edges'])
loader={}
for name in clean:
    if name=='time':continue
    entity,metric=name.rsplit('_',1)
    loader.setdefault(entity,{})[metric]=list(zip(clean.time,clean[name]))
context=CaseData(MemoryDataLoader(loader),next(iter(node_by_name.values())),td,interval=timedelta(seconds=1))
graph=MemoryGraph(g);current=td+300
print(datetime.now().isoformat(),'SCORING_BEGIN metrics',len(g),'edges',len(g.edges),flush=True)
score_tic=time.perf_counter();raw_scores=RHTScorer().score(graph,context,current)
adjusted=DAScorer(threshold=3).score(graph,context,current,copy.deepcopy(raw_scores))
base_names={node:f'{node.entity}_{node.metric}' for node in node_by_name.values()}
values={base_names[n]:v.score for n,v in raw_scores.items()}
da_values={base_names[n]:v.score for n,v in adjusted.items()}
raw_errors={k:abs(v-snapshot['nodes'][k]['rht_score']) for k,v in values.items()}
da_errors={k:abs(v-snapshot['da'][k]['score']) for k,v in da_values.items()}
assert set(values)==set(snapshot['nodes']) and set(da_values)==set(snapshot['da'])
raw_match=all(np.isclose(v,snapshot['nodes'][k]['rht_score'],atol=1e-7,rtol=1e-7) for k,v in values.items())
da_match=all(np.isclose(v,snapshot['da'][k]['score'],atol=1e-7,rtol=1e-7) for k,v in da_values.items())
fixed_orders={node:list(graph.parents(node)) for node in g}
class OrderedGraph(MemoryGraph):
    def __init__(self,graph,reverse=False):
        super().__init__(graph);self.reverse=reverse
    def parents(self,node,**kwargs):
        parents=fixed_orders.get(node,[])
        return parents[::-1] if self.reverse else list(parents)
reversed_scores=RHTScorer().score(OrderedGraph(g,True),context,current)
reversed_values={base_names[n]:v.score for n,v in reversed_scores.items()}
parent_errors={k:abs(values[k]-reversed_values[k]) for k in values}
parent_match=all(np.isclose(values[k],reversed_values[k],atol=1e-7,rtol=1e-7) for k in values)
result=dict(case=selected,source=row['source'],labels_given_to_method=False,snapshot='results/T-014/runs/example-architecture/snapshot.json',graph_relearned=False,context=dict(interval_seconds=1,train=context.train_window,test=context.test_window,current=current),original_rht_scores=values,original_da_scores=da_values,reverse_parent_rht_scores=reversed_values,comparison=dict(candidates=len(values),original_rht_matches_snapshot=raw_match,original_da_matches_snapshot=da_match,max_rht_abs_error=max(raw_errors.values()),max_da_abs_error=max(da_errors.values()),parent_permutation_matches_tolerance=parent_match,max_parent_permutation_abs_error=max(parent_errors.values()),parent_permutation_changed_scores={k:dict(original=values[k],reversed=reversed_values[k],abs_error=e) for k,e in parent_errors.items() if e},parents_with_two_or_more=sum(len(v)>=2 for v in fixed_orders.values())),diagnostic_scoring_seconds=time.perf_counter()-score_tic,diagnostic_total_seconds=time.perf_counter()-tic,timing_note='shared laptop; diagnostic, not official runtime')
(out/'architecture-original.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
with (out/'architecture-original-cases.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['ca','file_nguon','phuong_phap','muc_dich','ly_do'])
    w.writerow([selected,row['source'],'CIRCA-original RHT+DA same architecture 1s','original code comparison for all saved metric scores; no label input','b'])
    w.writerow([selected,row['source'],'CIRCA-original RHT reverse parents same architecture','explicit parent-order permutation at fixed graph/context','b'])
print(datetime.now().isoformat(),'DONE',json.dumps(result['comparison']), 'diagnostic_seconds',result['diagnostic_total_seconds'],flush=True)
assert raw_match and da_match and parent_match
