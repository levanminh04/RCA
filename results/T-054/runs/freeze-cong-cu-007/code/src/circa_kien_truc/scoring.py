"""Use unmodified RCAEval RHT/DA with an explicitly supplied graph."""
from datetime import timedelta
import copy
import math
import sys
import networkx as nx
import numpy as np

def graph_from_pc(adj,names):
    """Exact edge conversion in RCAEval rht, including its final reverse."""
    graph=nx.DiGraph()
    for a in range(len(adj)):
        for b in range(len(adj)):
            u,v=adj[a,b],adj[b,a]
            if u==v==0:continue
            if u==v==-1:graph.add_edge(names[b],names[a])
            elif u==1 and v==-1:graph.add_edge(names[b],names[a])
            elif u==-1 and v==1:graph.add_edge(names[a],names[b])
            else:raise ValueError(f'Unexpected endpoints: {u},{v}')
    return graph.reverse(copy=True)

def score_graph(frame, graph, detect_time, current=None, da_threshold=3):
    from RCAEval.classes.graph import Node,MemoryGraph
    from RCAEval.classes.data import CaseData,MemoryDataLoader
    from RCAEval.graph_heads.rht import RHTScorer,DAScorer
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
    from .builder import metric_mapping
    mapped={r['column']:r for r in metric_mapping(graph.nodes)}
    if any(r['status']!='mapped' for r in mapped.values()):raise ValueError('Unmapped metric in scoring graph')
    nodes={name:Node(mapped[name]['service'],mapped[name]['metric']) for name in graph.nodes}
    converted=nx.DiGraph();converted.add_nodes_from(nodes.values());converted.add_edges_from((nodes[a],nodes[b]) for a,b in graph.edges)
    mg=MemoryGraph(converted);byname={v:k for k,v in nodes.items()}
    raw={}
    for name,node in nodes.items():
        if name in frame:raw.setdefault(node.entity,{})[node.metric]=list(zip(frame.time,frame[name]))
    if not nodes:return dict(meta={'empty':True},graph={'nodes':[],'edges':[],'topological_groups':[]},nodes={},da={},ranks=[])
    current=detect_time+300 if current is None else current
    case=CaseData(MemoryDataLoader(raw),sli=nodes[sorted(nodes)[0]],detect_time=detect_time,interval=timedelta(seconds=1))
    series=case.load_data(mg,current);scorer=RHTScorer();scores=scorer.score(mg,case,current)
    snapshots={}
    for node,score in scores.items():
        parents=list(mg.parents(node));px,tx,py,ty=scorer.split_data(series,node,parents,case)
        fallback=len(px)==0
        route='no_effective_parents' if fallback else 'linear_regression'
        regression_error=None
        if not fallback:
            try:
                model=LinearRegression().fit(px,py);pe=py-model.predict(px);te=ty-model.predict(tx)
                coef=model.coef_.tolist();intercept=float(model.intercept_)
            except ValueError as exc:
                fallback=True
                route='value_error_fallback'
                regression_error=str(exc)
        if fallback:pe=py;te=ty;coef=[];intercept=None
        scale=StandardScaler().fit(pe.reshape(-1,1));z=scale.transform(te.reshape(-1,1))[:,0]
        snapshots[byname[node]]=dict(parents=[byname[p] for p in parents if p in series],train_x=px.tolist(),test_x=tx.tolist(),x_memory_order='F' if px.flags.f_contiguous or px.strides[0]<=px.strides[1] else 'C',train_y=py.tolist(),test_y=ty.tolist(),rht_score=float(score.score),confidence=float(score['Confidence']),official_train_residual=pe.tolist(),official_test_residual=te.tolist(),regression_fallback=fallback,regression_route=route,regression_error=regression_error,coefficient=coef,intercept=intercept,residual_mean=float(scale.mean_[0]),residual_var=float(scale.var_[0]),residual_scale=float(scale.scale_[0]),z=z.tolist())
    da_order=[]
    da_scorer=DAScorer(threshold=da_threshold)
    def capture(frame,event,arg):
        if event=='return' and frame.f_locals.get('self') is da_scorer:
            da_order[:]=[[byname[n] for n in group] for group in frame.f_locals.get('sorted_nodes',[])]
    old_profile=sys.getprofile();sys.setprofile(capture)
    try:adjusted=da_scorer.score(mg,case,current,copy.deepcopy(scores))
    finally:sys.setprofile(old_profile)
    da={byname[node]:dict(score=float(score.score),key=list(score.key),child_score=score.get('child_score'),index=score['index']) for node,score in adjusted.items()}
    ranks=sorted([[byname[n],float(s.score)] for n,s in scores.items()],key=lambda x:(-x[1],x[0]))
    ranks_da=sorted([[byname[n],float(s.score),list(s.key)] for n,s in adjusted.items()],key=lambda x:tuple(-v for v in x[2])+(x[0],))
    return dict(meta=dict(detect_time=detect_time,current=current,train_window=case.train_window,test_window=case.test_window,da_threshold=da_threshold,score_mode='RHT reference + diagnostic RHTDA',candidate_unit='metric',ranking_tie_policy='lexical for display within identical score/key',dropped_constant_or_missing=sorted(set(nodes)-set(snapshots))),graph=dict(nodes=sorted(graph.nodes),edges=sorted(map(list,graph.edges)),topological_groups=[sorted(byname[n] for n in group) for group in mg.topological_sort],da_iteration_order=da_order,dag=nx.is_directed_acyclic_graph(graph)),nodes=snapshots,da=da,ranks=ranks,ranks_da=ranks_da)
