"""Validate one newly learned PC graph; preserve every old result."""
import os,sys,json,argparse,time
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1'
sys.path[:0]=['D:/RCA-flashticket/src','D:/RCA-ext/src/RCAEval']
import numpy as np,pandas as pd,networkx as nx
from RCAEval.io.time_series import preprocess
from circa_kien_truc import graph_from_pc,score_graph
root=Path('D:/RCA-flashticket');out=root/'results/T-014'
ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['permuted','normal'],required=True);a=ap.parse_args()
dest=out/'runs'/('ec2-2-'+a.mode);status=json.loads((dest/'status.json').read_text())
if not status['complete']:
    print(json.dumps(dict(mode=a.mode,status=status,equivalence='not established: worker did not finish')));sys.exit(0)
case=json.loads((out/'runs/selection-before-scores.json').read_text())['selected']
row=next(r for r in json.loads((out/'runs/inventory.json').read_text()) if r['case']==case)
raw=pd.read_parquet(row['source']);true_td=row['inject_time']
raw=raw.loc[:,~raw.columns.str.endswith('_latency-50')].replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
raw=raw.rename(columns={c:c.replace('_latency-90','_latency') for c in raw if c.endswith('_latency-90')})
if a.mode=='normal':td=true_td-301;win=raw[raw.time<true_td].copy();snapshot_mode='normal-normal-pc-full'
else:td=true_td;win=pd.concat([raw[raw.time<td].tail(300),raw[raw.time>=td].head(300)],ignore_index=True);snapshot_mode='example-pc-full-permuted'
clean=preprocess(win.copy(),dataset='re2-tt')
if a.mode=='permuted':clean=clean.loc[:,list(reversed(clean.columns))]
names=list(clean);clean['time']=win.time.to_numpy();remote_names=json.loads((dest/'nodes.json').read_text());assert names==remote_names
adj=np.load(dest/'adj.npy');assert adj.shape==(len(names),len(names))
graph=graph_from_pc(adj,names);start=time.monotonic();snapshot=score_graph(clean,graph,td,td+300)
snapdir=out/'runs'/snapshot_mode;snapdir.mkdir(exist_ok=True);(snapdir/'snapshot.json').write_text(json.dumps(snapshot,indent=2))
official=dict(json.loads((dest/'scores.json').read_text()));local={k:n['rht_score'] for k,n in snapshot['nodes'].items()}
same=set(official)==set(local);checks={k:bool(np.isclose(local[k],official[k],atol=1e-7,rtol=1e-7)) for k in local if k in official}
assert same and all(checks.values()),'Direct EC2 rht vs local snapshot mismatch'
report=dict(mode=a.mode,status=status,raw_source=row['source'],names_match=True,shape=[len(clean),len(names)],scored=len(local),graph_nodes=len(graph),graph_edges=graph.number_of_edges(),graph_dag=nx.is_directed_acyclic_graph(graph),direct_rht_matches_snapshot=same and all(checks.values()),max_ec2_local_abs_error=max(abs(local[k]-official[k]) for k in local),snapshot_mode=snapshot_mode,elapsed_local_diagnostic=time.monotonic()-start,top=snapshot['ranks'][0],scores_ge3=sum(v>=3 for v in local.values()),fallback_valueerror=sum(n['regression_route']=='value_error_fallback' for n in snapshot['nodes'].values()))
if a.mode=='permuted':
    old=out/'runs/ec2-default-003';old_names=json.loads((old/'nodes.json').read_text());original=np.load(old/'adj.npy');index=[names.index(k) for k in old_names];aligned=adj[np.ix_(index,index)];old_points=dict(json.loads((old/'scores.json').read_text()))
    changes=[dict(metric=k,original=old_points.get(k),permuted=official.get(k)) for k in sorted(set(old_points)|set(official)) if k not in old_points or k not in official or not np.isclose(old_points[k],official[k],atol=1e-7,rtol=1e-7)]
    changed_pairs=[]
    for i in range(len(old_names)):
        for j in range(i+1,len(old_names)):
            if original[i,j]!=aligned[i,j] or original[j,i]!=aligned[j,i]:changed_pairs.append(dict(a=old_names[i],b=old_names[j],original=[int(original[i,j]),int(original[j,i])],permuted=[int(aligned[i,j]),int(aligned[j,i])]))
    report.update(endpoint_matrices_identical=bool(np.array_equal(aligned,original)),skeleton_identical=bool(np.array_equal(aligned!=0,original!=0)),changed_endpoint_pair_count=len(changed_pairs),changed_endpoint_pairs=changed_pairs,changed_score_count=len(changes),changed_scores=changes,candidate_set_identical=set(old_points)==set(official),score_equivalence=len(changes)==0,comparison_scope='column permutation plus host/runtime build change; package versions and critical source hashes matched; not a same-host repeat')
else:
    assert win.time.max()<true_td and snapshot['meta']['current']<true_td
    report.update(normal_pc_input_strictly_before_injection=True,normal_score_windows_strictly_before_injection=True,normal_sanity_verdict='FAIL apparent evidence on pre-injection proxy' if report['scores_ge3'] else 'No >=3 scores in this control',limit='One pre-injection proxy, not independently verified healthy; no prevalence/calibration claim; do not treat rank1 as known root',top_details=snapshot['nodes'][snapshot['ranks'][0][0]])
(dest/'comparison.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ['changed_endpoint_pairs','changed_scores','top_details']},ensure_ascii=True))
