import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,copy
from pathlib import Path
import numpy as np,pandas as pd,networkx as nx
sys.path[:0]=['D:/RCA-flashticket/src','D:/RCA-ext/src/RCAEval']
from circa_kien_truc import score_graph
checks=[]
def check(name,val):
    assert val,name
    checks.append(dict(check=name,pass_=bool(val)))
rng=np.random.default_rng(44);x=rng.normal(size=600);noise=rng.normal(0,.1,600);x[120:]+=8
df=pd.DataFrame({'time':np.arange(600),'a_cpu':x,'b_latency':2*x+noise,'c_error':rng.normal(size=600),'d_mem':np.ones(600)})
g=nx.DiGraph();g.add_nodes_from(['a_cpu','b_latency','c_error','d_mem']);g.add_edge('a_cpu','b_latency')
s=score_graph(df,g,120)
check('intervention root higher than explained child',s['nodes']['a_cpu']['rht_score']>s['nodes']['b_latency']['rht_score'])
check('constant node pruned transparently','d_mem' not in s['nodes'] and 'd_mem' in s['meta']['dropped_constant_or_missing'])
check('nonempty finite genuine scores',len(s['nodes'])==3 and all(np.isfinite(n['rht_score']) for n in s['nodes'].values()))
check('not input column order',s['ranks']!=[[n,0] for n in df if n!='time'])
p=score_graph(df[df.columns[::-1]],g,120)
check('column permutation preserves scores',s['ranks']==p['ranks'])
repeat=score_graph(df,g,120)
check('repeat same input exact score',s['ranks']==repeat['ranks'])
empty=score_graph(df,nx.DiGraph(),120)
check('empty PC graph explicit empty candidate set',empty['ranks']==[])
# Chain shows DA evidence passing through below-threshold intermediate child.
from RCAEval.classes.graph import MemoryGraph,Node
from RCAEval.graph_heads.rht import DAScorer
from RCAEval.graph_heads.random_walk import Score
a,b,c=Node('a','cpu'),Node('b','latency'),Node('c','error')
chain=MemoryGraph(nx.DiGraph([(a,b),(b,c)]));scores={a:Score(4),b:Score(1),c:Score(9)}
for v in scores.values():v['z-score']=v.score
adjusted=DAScorer(threshold=3).score(chain,None,None,copy.deepcopy(scores))
check('DA skips below-threshold intermediate but gathers descendant',adjusted[a].score==13 and adjusted[b].score==1)
out=Path('D:/RCA-flashticket/results/T-014/runs')
(out/'scoring-fixtures.json').write_text(json.dumps(dict(checks=checks,snapshot=s,da_chain={str(n):v.score for n,v in adjusted.items()}),indent=2))
print(f'{len(checks)} meaningful scoring checks passed')
