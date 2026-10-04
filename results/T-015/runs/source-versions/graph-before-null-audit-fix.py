"""Accumulate call edges and coverage on exactly the selected trace set.

The four dictionaries have the names used by the MIT MicroRank source.
Span lookup is scoped by trace, unlike the global lookup in RCAEval.
"""
from collections import defaultdict

def get_pagerank_graph(rows):
    by_trace=defaultdict(dict)
    for trace,span,parent,operation in sorted(rows,key=lambda r:(str(r[0]),str(r[1]))):
        trace,span,operation=str(trace),str(span),str(operation)
        parent=None if parent is None else str(parent)
        if span in by_trace[trace]:
            raise ValueError('Duplicate spanID within trace: '+trace+'/'+span)
        by_trace[trace][span]=(parent,operation)
    edges=defaultdict(set); coverage={}; reverse=defaultdict(set); repeated={}
    missing=0; explicit_roots=0
    for trace,spans in sorted(by_trace.items()):
        repeated[trace]=[op for parent,op in spans.values()]
        coverage[trace]=sorted(set(repeated[trace]))
        for span,(parent,op) in spans.items():
            edges[op]  # isolated operations remain candidates
            reverse[op].add(trace)
            if parent in spans:
                edges[spans[parent][1]].add(op)
            elif parent in [None,'','0','0000000000000000','nan','None']:
                explicit_roots+=1
            else:
                missing+=1
    graph={
        'operation_operation':{op:sorted(children) for op,children in sorted(edges.items())},
        'operation_trace':coverage,
        'trace_operation':{op:sorted(traces) for op,traces in sorted(reverse.items())},
        'pr_trace':repeated,
    }
    degree={op:len(children) for op,children in graph['operation_operation'].items()}
    for children in graph['operation_operation'].values():
        for op in children: degree[op]+=1
    audit={'missing_parent_spans':missing,'explicit_root_spans':explicit_roots,'isolated_operations':[op for op,d in degree.items() if d==0],'operation_edges':sum(map(len,graph['operation_operation'].values())),'traces':len(coverage),'operations':len(edges)}
    return graph,audit
