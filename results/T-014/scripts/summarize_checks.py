import json,csv
from pathlib import Path
out=Path('D:/RCA-flashticket/results/T-014')
items={p.parent.name:json.loads(p.read_text()) for p in (out/'runs').glob('*/snapshot.json') if 'architecture' in p.parent.name}
base=items['example-architecture'];repeat=items.get('example-architecture-repeat')
comparison={'architecture_repeat':None}
if repeat:
    comparison['architecture_repeat']=dict(same_scores=all(base['nodes'][n]['rht_score']==repeat['nodes'][n]['rht_score'] for n in base['nodes']),same_ranking=base['ranks']==repeat['ranks'],same_da=base['ranks_da']==repeat['ranks_da'])
normal=items.get('normal-normal-architecture-pretrace',items.get('normal-normal-architecture'))
top=normal['ranks'][0][0];node=normal['nodes'][top]
explain=dict(control='all train/test and graph trace cutoff before real injection; pseudo detect supplied for sanity only',top_metric=top,score=node['rht_score'],parents=node['parents'],train_y_min=min(node['train_y']),train_y_max=max(node['train_y']),train_mean=node['residual_mean'],train_scale=node['residual_scale'],test_y_min=min(node['test_y']),test_y_max=max(node['test_y']),test_z=node['z'],scores_ge3=sum(v['rht_score']>=3 for v in normal['nodes'].values()),maxscore=normal['ranks'][0][1],numerically_verified=True,sanity_verdict='FAIL: threshold3 produces apparent root evidence on pre-injection windows; ranker itself has no incident detection/abstention',possible_explanations=['normal reference does not cover natural memory drift/warmup','nonstationarity or workload variation before injection','short reference/no-parent marginal scoring, small normal variance','pre-injection is a dataset proxy, not independently labeled healthy interval'],scope='single P1 negative control; no P4 prevalence claim; do not tune windows to force pass')
(out/'runs/normal-sanity-explained.json').write_text(json.dumps(explain,indent=2))
(out/'runs/scoring-repeat-summary.json').write_text(json.dumps(comparison,indent=2))
graphs=list(csv.DictReader((out/'graphs/summary.csv').open()))
raw_graphs=[json.loads(p.read_text(encoding='utf-8')) for p in (out/'graphs').glob('re2tt_*.json')]
summary=dict(cases=len(graphs),unknown_total=sum(int(r['unknown']) for r in graphs),metric_edges_min=min(int(r['metric_edges']) for r in graphs),metric_edges_max=max(int(r['metric_edges']) for r in graphs),service_edges_min=min(int(r['service_edges']) for r in graphs),service_edges_max=max(int(r['service_edges']) for r in graphs),auth_without_call_cases=sum(r['auth_without_call']=='True' for r in graphs),metric_dag_cases=sum(r['dag']=='True' for r in graphs),isolates_min=min(int(r['isolated']) for r in graphs),isolates_max=max(int(r['isolated']) for r in graphs))
summary.update(call_dag_cases=sum(r['call_dag'] for r in raw_graphs),meta_dag_cases=sum(r['meta_dag'] for r in raw_graphs),call_cyclic_cases=sum(not r['call_dag'] for r in raw_graphs),meta_cyclic_cases=sum(not r['meta_dag'] for r in raw_graphs))
(out/'graphs/cycle-summary.csv').write_text('case,call_dag,meta_dag,metric_dag\n'+'\n'.join(f"{r['case']},{r['call_dag']},{r['meta_dag']},{r['dag']}" for r in sorted(raw_graphs,key=lambda x:x['case']))+'\n')
(out/'graphs/aggregate.json').write_text(json.dumps(summary,indent=2));print(json.dumps(dict(graphs=summary,scoring=comparison,normal_control=explain),ensure_ascii=False))
