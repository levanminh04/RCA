"""Independent single-mapping projection; reproduces native SCC traversal."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from pathlib import Path
import json,networkx as nx,itertools
root=Path('D:/RCA-flashticket/results/T-014')
checks=[]
for path in sorted((root/'graphs').glob('re2tt_*.json')):
    report=json.loads(path.read_text(encoding='utf-8'))
    rows=[r for r in report['mapping'] if r['status']=='mapped']
    observed=nx.DiGraph(report['call_edges'])
    services=set(observed.nodes)|{r['service'] for r in rows}
    calls=nx.DiGraph()
    for s in sorted(services):
        calls.add_node(s)
        calls.add_edges_from((s,c) for c in set(observed.successors(s)) if s in observed) if s in observed else None
    types=set('TSLE');meta=nx.DiGraph()
    # hash((type,component)) matches the native MetaVariable hash.
    meta.add_nodes_from((t,s) for t in types for s in calls)
    intra={'T':set('SLE'),'S':set('LE'),'L':{'E'}}
    for b in calls:
        for a,targets in intra.items():
            meta.add_edges_from(((a,b),(t,b)) for t in targets)
        for t in types:
            for a in calls.predecessors(b):
                if t=='T':meta.add_edge(('T',a),('T',b))
                if t in {'L','E'}:meta.add_edge((t,b),(t,a))
            if t=='E':
                for a in nx.ancestors(calls,b):meta.add_edge(('E',b),('E',a))
    # The paper formula is a DAG algorithm. For cyclic inputs, compare actual
    # code semantics only: native code visits each member of an SCC once.
    adjacency={v:set(meta.successors(v)) for v in meta}
    components=list(nx.strongly_connected_components(nx.DiGraph(adjacency)))
    membership={v:i for i,c in enumerate(components) for v in c}
    quotient={i:{membership[w] for v in c for w in adjacency[v]}-{i} for i,c in enumerate(components)}
    order=[set(itertools.chain.from_iterable(components[i] for i in layer)) for layer in nx.topological_generations(nx.DiGraph(quotient))]
    if not nx.is_directed_acyclic_graph(meta):
        checks.append(dict(case=report['case'],meta_dag=False,status='not_independently_equivalent: cyclic native object/set traversal; see retained failed SCC reconstruction and native YAML equivalence/hashseed test'))
        continue
    mapped={v:set() for v in meta}
    for r in rows:mapped[(r['type'],r['service'])].add(r['column'])
    visible={v:set() for v in meta};edges=set()
    for v in itertools.chain.from_iterable(order):
        parents=set().union(*(visible[u] for u in meta.predecessors(v)))
        edges|={(u,w) for u in parents for w in mapped[v]}
        visible[v]=mapped[v] or parents
    official={tuple(e) for e in report['edges']}
    native_nodes=set().union(*(set(e) for e in edges))
    metrics={r['column'] for r in rows}
    result=dict(case=report['case'],meta_dag=nx.is_directed_acyclic_graph(meta),independent_edges=len(edges),saved_edges=len(official),edge_symmetric_difference=sorted(edges^official),retained_nodes_match=metrics==set(report['nodes']),native_missing_nodes_match=metrics-native_nodes==set(report['original_missing_nodes']))
    assert not result['edge_symmetric_difference'] and result['retained_nodes_match'] and result['native_missing_nodes_match'],result
    checks.append(result)
Path('D:/RCA-flashticket/results/T-020/trung-gian/method_evidence/runs/circa-graph-independent-001.json').write_text(json.dumps(dict(dag_cases_passed=sum(r.get('meta_dag',False) for r in checks),cyclic_cases_not_equivalent=sum(not r.get('meta_dag',False) for r in checks),formula='single-mapping empty-meta forwarding on DAG; no author/task builder imports; no independent equivalence claim for cyclic graphs',checks=checks),indent=2))
print(f'{sum(r.get("meta_dag",False) for r in checks)} DAG cases independently match; {sum(not r.get("meta_dag",False) for r in checks)} cyclic cases explicitly excluded from this DAG proof')
