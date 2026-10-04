"""Check scoring of the completed PC graph; no new PC learning."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,hashlib
from pathlib import Path
import numpy as np,pandas as pd,networkx as nx
sys.path[:0]=['D:/RCA-flashticket/src','D:/RCA-ext/src/RCAEval']
from RCAEval.io.time_series import preprocess
from circa_kien_truc import graph_from_pc,score_graph
out=Path('D:/RCA-flashticket/results/T-014')
case=json.loads((out/'runs/selection-before-scores.json').read_text())['selected']
row=next(r for r in json.loads((out/'runs/inventory.json').read_text()) if r['case']==case)
raw=pd.read_parquet(row['source']);td=row['inject_time']
raw=raw.loc[:,~raw.columns.str.endswith('_latency-50')].replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
raw=raw.rename(columns={c:c.replace('_latency-90','_latency') for c in raw if c.endswith('_latency-90')})
win=pd.concat([raw[raw.time<td].tail(300),raw[raw.time>=td].head(300)],ignore_index=True)
clean=preprocess(win.copy(),dataset='re2-tt');names=list(clean);clean['time']=win.time
source=out/'runs/ec2-default-003';source_names=json.loads((source/'nodes.json').read_text());assert names==source_names
adj=np.load(source/'adj.npy');assert adj.shape==(len(names),len(names))
graph=graph_from_pc(adj,names);base=json.loads((out/'runs/example-pc/snapshot.json').read_text())
official=dict(json.loads((source/'scores.json').read_text()));local={k:n['rht_score'] for k,n in base['nodes'].items()}
errors={k:abs(local[k]-official[k]) for k in local};same_nodes=set(local)==set(official)
assert same_nodes and all(np.isclose(local[k],official[k],atol=1e-7,rtol=1e-7) for k in local)
reports={}
for mode,frame in [('example-pc-repeat',clean),('example-pc-permuted-score-only',clean[clean.columns[::-1]])]:
    snapshot=score_graph(frame,graph,td);dest=out/'runs'/mode;dest.mkdir(exist_ok=True)
    (dest/'snapshot.json').write_text(json.dumps(snapshot,indent=2))
    reports[mode]=dict(same_scores=all(local[k]==snapshot['nodes'][k]['rht_score'] for k in local),same_ranking=base['ranks']==snapshot['ranks'],same_DA=base['ranks_da']==snapshot['ranks_da'])
    assert all(reports[mode].values())
normal_raw=raw[raw.time<td];normal=preprocess(normal_raw.copy(),dataset='re2-tt');normal['time']=normal_raw.time
snapshot=score_graph(normal,graph,td-301,td-1)
dest=out/'runs/normal-normal-pc-cached-fault-graph';dest.mkdir(exist_ok=True)
(dest/'snapshot.json').write_text(json.dumps(snapshot,indent=2))
reports['normal_scoring_given_cached_fault_graph']=dict(top=snapshot['ranks'][0],scored=len(snapshot['nodes']),scores_ge3=sum(v['rht_score']>=3 for v in snapshot['nodes'].values()),limit='Scoring windows normal; graph learned from incident window. This does not replace full normal-PC pipeline control.')
reports.update(ec2_official_RHT_matches_local=same_nodes,max_ec2_local_abs_error=max(errors.values()),adjacency_columns_match=True,PC_input_points=len(win),PC_input_time_first=float(win.time.min()),PC_input_time_last=float(win.time.max()),input_processed_count=len(names),graph_nodes=len(graph),graph_edges=graph.number_of_edges(),graph_dag=nx.is_directed_acyclic_graph(graph),SCC_larger_than1=[sorted(c) for c in nx.strongly_connected_components(graph) if len(c)>1],PC_isolates_dropped=sorted(set(names)-set(graph)),loader_pruned=base['meta']['dropped_constant_or_missing'],scored=len(local),test_last_point_outside_prepared_input=bool((td+300)>win.time.max()))
(out/'runs/pc-cached-checks.json').write_text(json.dumps(reports,indent=2));print(json.dumps({k:v for k,v in reports.items() if k!='SCC_larger_than1'}))
