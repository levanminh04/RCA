import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,networkx as nx
from pathlib import Path
sys.path.insert(0,'D:/RCA-flashticket/src')
from circa_kien_truc import build_graph
out=Path('D:/RCA-flashticket/results/T-014');checks=[]
for p in sorted((out/'graphs').glob('re2tt_*.json')):
    r=json.loads(p.read_text(encoding='utf-8'));calls=nx.DiGraph(r['call_edges'])
    graph,report=build_graph([x['column'] for x in r['mapping']],calls,'D:/RCA-ext/work/T-014/CIRCA')
    old={tuple(e) for e in r['edges']};new=set(graph.edges)
    checks.append(dict(case=r['case'],call_dag=report['call_dag'],meta_dag=report['meta_dag'],metric_dag=report['dag'],old_edges=len(old),new_edges=len(new),edge_symmetric_difference=sorted(old^new),nodes_equal=set(graph.nodes)==set(r['nodes'])))
seed=os.environ.get('PYTHONHASHSEED','unset')
(out/f'runs/builder-hashseed-{seed}.json').write_text(json.dumps(dict(seed=seed,cases=len(checks),cases_with_edge_change=sum(bool(r['edge_symmetric_difference']) for r in checks),checks=checks),indent=2))
print(f'seed {seed}: {sum(bool(r["edge_symmetric_difference"]) for r in checks)}/{len(checks)} cases change edges')
