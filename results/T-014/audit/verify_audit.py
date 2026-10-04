"""Check saved artifacts and independently compute service Avg@5 and DA."""
import csv
from datetime import datetime
import hashlib
from itertools import chain
import json
from pathlib import Path
import subprocess
import networkx as nx
import numpy as np

out=Path(__file__).resolve().parent
records=json.loads(Path('D:/RCA-ext/work/T-014/audit-r/mem-target/inputs.json').read_text())
max_da_difference=0.0
rank_column_order=[]
num=0
for record in records:
    stem=record['stem']
    linear=json.loads((out/'mem-target'/(stem+'.json')).read_text())
    configs={label:json.loads((out/'mem-target-prior'/label/(stem+'.json')).read_text())
             for label in ('SVR_sigmoid_RHT','linear_RHT_DA3','SVR_sigmoid_RHT_DA3')}
    assert linear['scores'] and len(linear['ranks_author_stable_sort'])==len(linear['scores'])
    assert np.isfinite(list(linear['scores'].values())).all()
    assert linear['context']['loaded_lengths']==[421]
    if linear['ranks_author_stable_sort']==record['columns']:rank_column_order.append(stem)
    # Node in official CIRCA hashes the (entity, metric) tuple. Reproduce only
    # this traversal representation independently; no author graph/scorer calls.
    parse=lambda value:tuple(value.split('_',1))
    render=lambda value:'_'.join(value)
    graph=nx.DiGraph();graph.add_nodes_from(map(parse,record['columns']))
    graph.add_edges_from((parse(a),parse(b)) for a,b in linear['graph_edges'])
    traversal={node:set(graph.successors(node)) for node in set(graph.nodes)}
    components=list(nx.strongly_connected_components(nx.DiGraph(traversal)))
    node_to_component={node:i for i,component in enumerate(components) for node in component}
    condensed={i:{node_to_component[child] for node in component for child in traversal[node]}-{i}
               for i,component in enumerate(components)}
    layers=[set(chain(*(components[i] for i in layer)))
            for layer in nx.topological_generations(nx.DiGraph(condensed))]
    for raw,adjusted in ((linear['scores'],configs['linear_RHT_DA3']['scores']),
                         (configs['SVR_sigmoid_RHT']['scores'],configs['SVR_sigmoid_RHT_DA3']['scores'])):
        keyed={parse(node):score for node,score in raw.items()}
        scored_layers=[{node for node in layer if node in keyed} for layer in layers]
        child_scores={}
        for layer in reversed(scored_layers):
            for node in layer:
                children={}
                for child in set(graph.successors(node)):
                    if child in keyed:
                        children[child]=keyed[child]
                        if keyed[child]<3:children.update(child_scores.get(child,{}))
                child_scores[node]=children
        independent={render(node):score+(max(child_scores[node].values())
                                   if score>=3 and child_scores[node] else 0) for node,score in keyed.items()}
        assert set(independent)==set(adjusted)
        max_da_difference=max(max_da_difference,max(abs(independent[node]-adjusted[node]) for node in independent))
    for label,value in configs.items():
        assert value['scores'] and np.isfinite(list(value['scores'].values())).all()
        assert set(value['ranks_author_key_stable_sort'])==set(value['scores'])
        num+=1
assert max_da_difference==0
assert not rank_column_order

old_summary=json.loads((out/'mem-target-summary.json').read_text())
new_summary=json.loads((out/'mem-prior-config-summary.json').read_text())
def independent_average(rows,get_rank):
    # Avg@5 is mean of the five Hit@k values per case.
    return float(np.mean([np.mean([float(get_rank(row) is not None and get_rank(row)<=k)
                                   for k in range(1,6)]) for row in rows]))
for label in new_summary['aggregate']:
    value=independent_average(new_summary['per_case'],lambda row:row['configs'][label]['true_service_rank'])
    assert abs(value-new_summary['aggregate'][label]['Avg5'])<1e-12
for label in old_summary['aggregate']:
    value=independent_average(old_summary['per_case'],lambda row:row[label]['true_service_rank'])
    assert abs(value-old_summary['aggregate'][label]['Avg5'])<1e-12

coverage=[]
for task in range(13):
    task_name=f'T-{task:03}'
    folder=Path('results')/task_name
    paths=sorted(folder.glob('*.md'))
    if task==0:
        paths=[Path('tasks/T-000-nen-tang/SPEC.md'),Path('docs/knowledge/K1-phuong-phap-rca.md')]
    if not paths:
        coverage.append({'task':task_name,'file':'không có results top-level Markdown','bytes':0,'sha256':'',
                         'CIRCA_lines':'','coverage':'census; T004 không có task/results tại lúc kiểm' if task==4 else 'census'})
    for path in paths:
        payload=path.read_bytes();content=payload.decode('utf-8-sig')
        matches=[i for i,line in enumerate(content.splitlines(),1) if 'circa' in line.lower() or 'rht' in line.lower()]
        coverage.append({'task':task_name,'file':path.as_posix(),'bytes':len(payload),
                         'sha256':hashlib.sha256(payload).hexdigest(),'CIRCA_lines':';'.join(map(str,matches)),
                         'coverage':'census top-level docs; CIRCA/code/scoring assertions inspected where present; no full audit of other methods/data'})
with (out/'coverage-task-cu.csv').open('w',encoding='utf-8-sig',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=list(coverage[0]));writer.writeheader();writer.writerows(coverage)
source={}
for name,ref in (('RCAEval_main','HEAD'),('RCAEval_ase24','origin/ase24'),('RCAEval_fse26','origin/fse26')):
    source[name]=subprocess.check_output(['git','-C','D:/RCA-ext/src/RCAEval','rev-parse',ref],text=True).strip()
source['BARO']=subprocess.check_output(['git','-C','D:/RCA-ext/src/baro','rev-parse','HEAD'],text=True).strip()
source['CIRCA']=subprocess.check_output(['git','-C','D:/RCA-ext/work/T-014/CIRCA','rev-parse','HEAD'],text=True).strip()
(out/'source-revisions.json').write_text(json.dumps(source,indent=2),encoding='utf-8')
result={'at':datetime.now().isoformat(),'mem_cases':len(records),'new_saved_scorer_variant_files':num,
        'independent_DA_max_difference':max_da_difference,'rank_equals_input_columns':rank_column_order,
        'finite_nonempty_scores':True,'independent_Avg5_matches_all_saved_aggregates':True,
        'coverage_note':'top-level old-doc census plus detailed CIRCA T001/T005/T006/source audit; not a claim all old artifacts verified'}
(out/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
