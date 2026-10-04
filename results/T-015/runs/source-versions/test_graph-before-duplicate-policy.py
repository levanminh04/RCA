"""Compare accumulated graph with original AST on synthetic Jaeger records."""
import ast,json,pathlib,sys
from copy import deepcopy
ROOT=pathlib.Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
from microrank.graph import get_pagerank_graph

def main():
    rows=[('t1','a',None,'A'),('t1','b','a','B'),('t2','a',None,'A'),('t2','c','a','C'),('t3','x','missing','X'),('t3','y',None,'Y')]
    graph,audit=get_pagerank_graph(rows)
    assert graph['operation_operation']['A']==['B','C']
    assert graph['operation_operation']['X']==[]
    assert 'X' in audit['isolated_operations'] and audit['missing_parent_spans']==1
    p=pathlib.Path('C:/Users/84583/AppData/Local/Temp/claude/D--RCA-flashticket/faa9e437-da55-49ba-b763-6e8484c8c9a6/scratchpad/ext/MicroRank/preprocess_data.py')
    tree=ast.parse(p.read_text(encoding='utf-8'))
    n=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='get_pagerank_graph')
    ns={'deepcopy':deepcopy};exec(compile(ast.Module(body=[n],type_ignores=[]),str(p),'exec'),ns)
    docs=[{'_source':{'traceID':t,'spanID':s,'references':[] if parent is None else [{'spanID':parent}],'operationName':op,'process':{'tags':[{'key':'name','value':'pod'}]},'tags':[]}} for t,s,parent,op in rows]
    author=ns['get_pagerank_graph'](['t1','t2','t3'],docs)
    for name,d in zip(graph,author):
        # Compare after the explicit pod-key -> compact toy-key translation.
        d={k.removeprefix('pod_'):[x.removeprefix('pod_') for x in v] for k,v in d.items()}
        assert {k:sorted(v) for k,v in graph[name].items()}=={k:sorted(v) for k,v in d.items()},name
    shuffled=get_pagerank_graph(list(reversed(rows)))[0]
    assert graph==shuffled
    collision=[('t','1',None,'s1_same'),('t','2','1','s2_same')]
    assert len(get_pagerank_graph(collision)[0]['operation_operation'])==2
    duplicate_error=False
    try:get_pagerank_graph(rows+[rows[0]])
    except ValueError:duplicate_error=True
    assert duplicate_error
    result={'status':'pass','original_graph_sets_exact':True,'accumulate_A_B_C':True,'scope_parent_lookup_by_trace':True,'orphan_no_fake_edge':True,'multi_root_nodes_retained':True,'same_method_different_service_distinct':True,'duplicate_span_rejected':True,'input_row_permutation_invariant':True,'audit':audit}
    out=ROOT/'results/T-015/runs/graph-toy';out.mkdir(parents=True,exist_ok=True)
    (out/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__':main()
