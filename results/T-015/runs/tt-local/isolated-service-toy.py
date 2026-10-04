"""Small synthetic candidate check. No dataset or root label is read."""
import json
import pathlib
import sys
import pandas as pd

ROOT=pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'src'))
from microrank import microrank, COLS

rows=[]
for i,duration in enumerate([1000,1200,800,1100]):
    for span,service in [('a','s1'),('b','s2')]:
        rows.append([f'reference{i}',span,None,service,'same','same',1000+i*2000,duration])
for trace,duration in [('normal',1000),('anomaly',4000)]:
    for span,service in [('a','s1'),('b','s2')]:
        rows.append([trace,span,None,service,'same','same',20000,duration])
result=microrank(pd.DataFrame(rows,columns=COLS),15000,include_graph=True)
assert result['status']=='ok'
assert set(result['service_ranks_full'])=={'s1','s2'}
assert set(result['service_ranks_top11'])=={'s1','s2'}
assert all(group['audit']['operation_edges']==0 for group in result['groups'].values())
assert all(len(group['audit']['isolated_operations'])==2 for group in result['groups'].values())
out={'synthetic':True,'root_label_used':False,'status':'pass',
     'zero_edges_both_groups':True,'both_services_in_full_and_truncated_ranks':True,
     'result':result}
(ROOT/'results/T-015/runs/tt-local/isolated-service-toy.json').write_text(
    json.dumps(out,ensure_ascii=False,allow_nan=False,indent=2),encoding='utf-8')
print('PASS: services with no operation edge are ranked in synthetic input')
