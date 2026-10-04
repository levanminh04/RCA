import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json
from pathlib import Path
import pandas as pd,networkx as nx
sys.path[:0]=['D:/RCA-flashticket/src','D:/RCA-ext/src/RCAEval']
from circa_kien_truc import metric_mapping,service_calls,build_graph
source='D:/RCA-ext/work/T-014/CIRCA';checks=[]
def check(name,predicate):
    assert predicate,name
    checks.append({'check':name,'pass':True})
records=[['one','p','0','a',1],['one','c','p','b',2],['two','p','0','x',1],['two','c','p','y',2],['one','post','c','z',100000000],['one','orphan','unknown','u',2],['one','self','p','a',2]]
t=pd.DataFrame(records,columns=['traceID','spanID','parentSpanID','serviceName','startTime'])
calls,report=service_calls(t,1)
check('traceID collision resolved separately',set(calls.edges)=={('a','b'),('x','y')})
check('exclude boundary/post and orphan',('b','z') not in calls.edges and calls.degree('u')==0)
columns=['a_workload','a_cpu','a_latency','a_error','b_workload','b_cpu','b_latency','b_error','auth_cpu','auth_mem','a_b_latency-50','globalvalue','_cpu','time']
mapping=metric_mapping(columns);check('longest service suffix',next(r for r in mapping if r['column']=='a_b_latency-50')['service']=='a_b')
check('unknown/missing service flag',len([r for r in mapping if r['status']!='mapped'])==2)
g,r=build_graph(columns,nx.DiGraph([('a','b')]),source)
check('call traffic forward',g.has_edge('a_workload','b_workload'))
check('call latency/error backward',g.has_edge('b_latency','a_latency') and g.has_edge('b_error','a_error'))
check('within resource to latency',g.has_edge('a_cpu','a_latency'))
check('auth isolates retained',all(n in r['isolated'] for n in ['auth_cpu','auth_mem']))
g2,r2=build_graph(['a_cpu','a_error'],nx.DiGraph(),source)
check('forward missing Latency meta',set(g2.edges)=={('a_cpu','a_error')})
g3,r3=build_graph(['a_workload','a_latency','b_workload','b_latency'],nx.DiGraph([('a','b'),('b','a')]),source)
check('call/meta cycles reported independently of metric result',not r3['call_dag'] and not r3['meta_dag'])
g4,_=build_graph(list(reversed(columns)),nx.DiGraph([('a','b')]),source)
check('mapping/permutation same graph',set(g.edges)==set(g4.edges) and set(g.nodes)==set(g4.nodes))
Path('D:/RCA-flashticket/results/T-014/runs/builder-fixtures.json').write_text(json.dumps(checks,indent=2))
print(f'{len(checks)} meaningful builder fixtures passed')
