"""Isolate pinned author's graph function with synthetic identical copies."""
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
SOURCE=Path('C:/Users/84583/AppData/Local/Temp/claude/D--RCA-flashticket/faa9e437-da55-49ba-b763-6e8484c8c9a6/scratchpad/ext/MicroRank/preprocess_data.py')
parsed=ast.parse(SOURCE.read_text(encoding='utf-8'))
function=next(n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name=='get_pagerank_graph')
namespace={'deepcopy':deepcopy}
exec(compile(ast.Module(body=[function],type_ignores=[]),str(SOURCE),'exec'),namespace)
def doc(span,parent,pod):
    return {'_source':{'traceID':'toy','spanID':span,'operationName':'op',
                       'references':[{'spanID':parent}] if parent else [],
                       'process':{'tags':[{'key':'name','value':pod}]},'tags':[]}}
a,b=doc('a',None,'pod-A'),doc('b','a','pod-B')
regular=namespace['get_pagerank_graph'](['toy'],[a,b])
duplicated=namespace['get_pagerank_graph'](['toy'],[a,b,deepcopy(b)])
assert duplicated[:3]==regular[:3]
assert regular[3]['toy']==['pod-A_op','pod-B_op']
assert duplicated[3]['toy']==['pod-A_op','pod-B_op','pod-B_op']
out={'synthetic':True,'root_label_used':False,'author_function_only_no_full_method':True,
     'source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
     'source_lines':{'span_lookup_overwrites':'preprocess_data.py:402-421',
                     'pr_trace_preserves_rows':'preprocess_data.py:442-444',
                     'coverage_unique':'preprocess_data.py:446-449',
                     'edges_unique':'preprocess_data.py:454-462'},
     'three_relations_unchanged_with_identical_duplicate':True,
     'pr_trace_multiplicity_preserved':True,'regular':regular,'duplicated':duplicated,
     'scope':'Graph only. SLO preprocessing is another path; the RCAEval span detector retains raw rows.'}
(ROOT/'results/T-015/runs/tt-local/original-duplicate-graph-check.json').write_text(
    json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: pinned original graph preserves repeated row in pr_trace, unique lookup/edges/coverage')
