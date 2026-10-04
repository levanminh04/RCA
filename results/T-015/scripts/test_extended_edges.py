"""Additional low-cost, label-free input and truncation checks. No dataset method runs."""
import json,pathlib,sys
import pandas as pd
ROOT=pathlib.Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
from microrank import microrank,COLS
from test_adapter import frame
OUT=ROOT/'results/T-015/runs/extended-edge';OUT.mkdir(parents=True,exist_ok=True)
checks={}
def rejected(data,text):
    try:microrank(data,15000)
    except ValueError as e:return text in str(e)
    return False
df=frame()
one=df[(df.startTime>=15000)|(df.traceID=='b0')]
checks['one_span_std_undefined_rejected']=rejected(one,'Normal std undefined')
collision=df.copy();collision.loc[collision.serviceName=='s1',['serviceName','methodName']]=['s_a','b'];collision.loc[collision.serviceName=='s2',['serviceName','methodName']]=['s','a_b']
checks['concatenation_key_collision_rejected']=rejected(collision,'Ambiguous')
nan=df.copy();nan.loc[nan.index[-1],'duration']=float('nan')
checks['missing_duration_rejected']=rejected(nan,'Invalid span time')
constant=df.copy();constant['duration']=1000
r=microrank(constant,15000)
checks['std_zero_equality_is_abnormal']=r['status']=='no_normal_traces' and r['counts']['anomaly']==2 and not r['ranks']
cross=df.copy();cross.loc[len(cross)]=['cross','a','lost-parent','s1','same','same',14000,2000]
r=microrank(cross,15000,True)
checks['crossing_span_uses_end_boundary']=r['counts']['spans_after']==5 and r['counts']['spans_before']==8
checks['crossing_parent_not_fabricated']=r['groups']['anomaly']['audit']['missing_parent_spans']>0
rows=[]
for op in range(15):
    for i,d in enumerate([800,1000,1200]):rows.append([f'b{i}',str(op),None,'svc'+str(op),'same','same',1000+i*2000,d])
    for trace,d in [('n',1000),('f',4000)]:rows.append([trace,str(op),None,'svc'+str(op),'same','same',20000,d])
r=microrank(pd.DataFrame(rows,columns=COLS),15000,True)
checks['top_max_plus_six_exact']=len(r['ranks'])==11 and len(r['full_ranks'])==15
checks['isolated_operation_can_rank']=all(not children for g in r['groups'].values() for children in g['graph']['operation_operation'].values()) and len(r['full_ranks'])==15
checks['missing_service_not_invented']='absent' not in r['service_ranks_full']
summary={'checks':checks,'all_passed':all(checks.values()),'scope':'synthetic inputs, not dataset method runs; std0 is an observed equality failure mode','top11':r['ranks'],'full':r['full_ranks']}
(OUT/'result.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary))
assert summary['all_passed']
