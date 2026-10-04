"""Synthetic, no dataset/labels: does DA on an SCC depend on hash order?"""
import json
import os
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode=True
out=Path(__file__).resolve().parent
if len(sys.argv)>1 and sys.argv[1]=='worker':
    sys.path.insert(0,'D:/RCA-ext/work/T-014/CIRCA')
    import networkx as nx
    from circa.alg.base import Score
    from circa.alg.ci import DAScorer
    from circa.model.graph import MemoryGraph,Node
    nodes={label:Node(label,'cpu') for label in 'abc'}
    configurations={}
    for label,edges in [('DAG',[('a','b'),('b','c')]),('cycle',[('a','b'),('b','c'),('c','b')])]:
        graph=nx.DiGraph();graph.add_nodes_from(nodes.values())
        graph.add_edges_from((nodes[a],nodes[b]) for a,b in edges)
        memory=MemoryGraph(graph)
        scores={nodes[key]:Score(value,info={'z-score':value}) for key,value in {'a':4.0,'b':1.0,'c':4.0}.items()}
        adjusted=DAScorer(threshold=3).score(memory,None,0,scores)
        configurations[label]={'input_edges':edges,'input_scores':{'a':4,'b':1,'c':4},
                               'SCC_layer_iteration':[[n.entity for n in layer] for layer in memory.topological_sort],
                               'DA_scores':{n.entity:s.score for n,s in adjusted.items()},
                               'DA_key':{n.entity:s.key for n,s in adjusted.items()}}
    print(json.dumps({'seed':os.environ.get('PYTHONHASHSEED'),'configurations':configurations}))
else:
    records=[]
    for seed in range(6):
        env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1')
        completed=subprocess.run([sys.executable,'-B',str(Path(__file__).resolve()),'worker'],
                                 env=env,capture_output=True,text=True,check=False)
        (out/f'da-cycle-seed{seed}.log').write_text(completed.stdout+completed.stderr,encoding='utf-8')
        assert completed.returncode==0,completed.stderr
        records.append(json.loads(completed.stdout))
    dag_values={tuple(sorted(row['configurations']['DAG']['DA_scores'].items())) for row in records}
    cycle_values={tuple(sorted(row['configurations']['cycle']['DA_scores'].items())) for row in records}
    result={'no_dataset_or_labels':True,'threshold':3,'seeds':records,
            'dag_unique_score_vectors':len(dag_values),'cycle_unique_score_vectors':len(cycle_values),
            'cycle_DA_score_depends_on_hashseed':len(cycle_values)>1}
    assert len(dag_values)==1
    (out/'da-cycle.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='seeds'},indent=2))
