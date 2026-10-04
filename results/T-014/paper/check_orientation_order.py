"""Controlled conflicting-collider fixture: only node order changes, same host.

No dataset or CI testing. Separating sets are explicitly supplied and identical
by name. This identifies a mechanism; it does not replay the real-case sepsets.
"""
from pathlib import Path
import json,itertools
import numpy as np
from causallearn.graph.GraphClass import CausalGraph
from causallearn.utils.PCUtils.UCSepset import uc_sepset
edges=[('a','b'),('b','c'),('c','d')]
def run(names):
    graph=CausalGraph(4,node_names=names)
    for i in range(4):
        for j in range(i+1,4):
            pair={names[i],names[j]}
            if not any(pair==set(e) for e in edges):
                graph.G.remove_edge(graph.G.get_edge(graph.G.nodes[i],graph.G.nodes[j]))
                graph.sepset[i,j]=graph.sepset[j,i]=[()]
    initial=graph.G.graph.copy();result=uc_sepset(graph,priority=2).G.graph
    # Independent literal rule for the supplied empty separators.
    manual=initial.copy();adjacent=list(zip(*np.where(initial!=0)))
    triples=[(p[0],p[1],q[1]) for p,q in itertools.permutations(adjacent,2) if p[1]==q[0] and p[0]!=q[1] and initial[p[0],q[1]]==0 and p[0]<q[1]]
    for x,y,z in triples:
        directed_yx=manual[y,x]==-1 and manual[x,y]==1
        directed_yz=manual[y,z]==-1 and manual[z,y]==1
        if not directed_yx and not directed_yz:
            manual[x,y]=-1;manual[y,x]=1;manual[z,y]=-1;manual[y,z]=1
    assert np.array_equal(manual,result)
    index=[names.index(n) for n in ['a','b','c','d']]
    return dict(order=names,named_triples=[[names[i] for i in t] for t in triples],aligned_endpoint_matrix=result[np.ix_(index,index)].tolist(),independent_rule_matches=True)
forward=run(['a','b','c','d']);reverse=run(['d','c','b','a'])
assert forward['aligned_endpoint_matrix']!=reverse['aligned_endpoint_matrix']
report=dict(forward=forward,reverse=reverse,only_node_order_changed=True,separating_sets_by_name={'a,c':[[]],'a,d':[[]],'b,d':[[]]},skeleton_same=True,orientation_differs=True,mechanism='uc_priority2 preserves previously oriented colliders; unshielded triples enumerated by numeric node index. stable=True concerns skeleton removal, not this order-dependent conflict policy.',scope='Controlled synthetic contradictory-CI/sepset fixture; no claim that every real changed edge has this cause. Real permutation also changes host/build.',source='causal-learn0.1.3.8: PC.py25-26,111-116; UCSepset.py40-42,95-111; GraphClass.py92-107')
out=Path('D:/RCA-flashticket/results/T-014/paper');(out/'orientation-order-fixture.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
