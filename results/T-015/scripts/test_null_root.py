import json,pathlib,sys
import pandas as pd
ROOT=pathlib.Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
from microrank.graph import get_pagerank_graph
base=[('t','r',None,'A'),('t','c','r','B'),('t','o','lost','C')]
graph,audit=get_pagerank_graph(base)
other,other_audit=get_pagerank_graph([('t','r',pd.NA,'A'),*base[1:]])
assert graph==other and audit==other_audit
assert audit['explicit_root_spans']==1 and audit['missing_parent_spans']==1
p=ROOT/'results/T-015/runs/null-root-toy';p.mkdir(parents=True,exist_ok=True)
(p/'result.json').write_text(json.dumps({'all_passed':True,'graph_same_for_None_and_pdNA':True,'audit_same':True,'audit':audit},indent=2),encoding='utf-8')
print('PASS: pd.NA and None root markers have same graph and audit')
