"""Trace/metric adapter for CIRCA 0215e18 structural rules; no labels."""
from pathlib import Path
import os
import sys
import networkx as nx
import pandas as pd

TYPES = {'workload':'T','cpu':'S','mem':'S','socket':'S','diskio':'S',
         'latency-50':'L','latency-90':'L','latency':'L','lat50':'L',
         'lat90':'L','lat99':'L','lat_50':'L','lat_90':'L','lat_99':'L','error':'E'}

def metric_mapping(columns):
    """Longest suffix prevents loss of a service name containing underscores."""
    rows=[]
    for column in columns:
        if column in {'time','Time','time.1'}:continue
        matches=[s for s in TYPES if column.endswith('_'+s)]
        if matches:
            suffix=max(matches,key=len);service=column[:-len(suffix)-1]
            valid=bool(service)
            rows.append(dict(column=column,service=service or None,metric=suffix,
                             type=TYPES[suffix] if valid else None,
                             status='mapped' if valid else 'missing_service'))
        else:
            rows.append(dict(column=column,service=None,metric=None,type=None,status='unmapped'))
    return rows

def service_calls(traces, cutoff_seconds):
    required=['traceID','spanID','parentSpanID','serviceName','startTime']
    if any(c not in traces for c in required):raise ValueError('Missing trace fields')
    pre=traces.loc[traces.startTime < cutoff_seconds*1_000_000,required].copy()
    if pre[required[:2]].isna().any().any():raise ValueError('Missing trace/span ID')
    pre['traceID']=pre.traceID.astype(str);pre['spanID']=pre.spanID.astype(str)
    pre['parentSpanID']=pre.parentSpanID.astype(str)
    dup=pre.duplicated(['traceID','spanID'],keep=False)
    ambiguous=pre.loc[dup].groupby(['traceID','spanID']).serviceName.nunique()
    if (ambiguous>1).any():raise ValueError('Ambiguous duplicate span ownership')
    parents=pre.drop_duplicates(['traceID','spanID'])[['traceID','spanID','serviceName']].rename(columns={'spanID':'parentSpanID','serviceName':'caller'})
    merged=pre.merge(parents,on=['traceID','parentSpanID'],how='left',validate='many_to_one')
    graph=nx.DiGraph();graph.add_nodes_from(sorted(pre.serviceName.dropna().astype(str).unique()))
    resolved=merged.caller.notna() & merged.serviceName.notna()
    cross=resolved & merged.caller.ne(merged.serviceName)
    graph.add_edges_from(sorted(set(zip(merged.loc[cross,'caller'],merged.loc[cross,'serviceName']))))
    report=dict(pre_spans=len(pre),resolved_parents=int(resolved.sum()),orphan_or_root=int((~resolved).sum()),self_call_spans=int((resolved & ~cross).sum()),duplicate_rows=int(dup.sum()),service_nodes=len(graph),service_edges=graph.number_of_edges(),cutoff_seconds=cutoff_seconds,both_parent_and_child_before_cutoff=True,key=['traceID','spanID'])
    report['python_hashseed']=os.environ.get('PYTHONHASHSEED','unrecorded')
    report['cycle_semantics']='native single SCC visit; output DAG does not establish valid DAG input; edges may depend on hashseed'
    return graph,report

def build_graph(columns, call_graph, circa_source, retain_isolates=True):
    """Invoke exact upstream StructuralGraph.visit, then explicitly report coverage.

    The adapter can retain mapped isolated candidates. This is an explicit node
    coverage correction, not an additional causal edge. Original mode is returned
    in the report for comparison.
    """
    source=Path(circa_source).resolve();sys.path.insert(0,str(source))
    from circa.graph.structural import Config,ComponentConfig,StructuralGraph
    config=Config.__new__(Config);config.types=set('TSLE')
    assumptions={'graph':{'T':['S','L','E'],'S':['L','E'],'L':['E']},
                 'parents':{'T':['T']},'children':{'L':['L'],'E':['E']},
                 'ancestors':{},'descendents':{'E':['E']}}
    for name,rule in assumptions.items():setattr(config,'assumed_'+name,Config.parse_assumptions(rule,config.types))
    mapping=metric_mapping(columns);known=[r for r in mapping if r['status']=='mapped']
    services=sorted(set(call_graph.nodes)|{r['service'] for r in known})
    config.components=[]
    for service in services:
        metrics={r['metric']:[{'type':r['type'],'component':service}] for r in known if r['service']==service}
        dependencies={service:sorted(call_graph.successors(service))} if service in call_graph else {}
        config.components.append(ComponentConfig(dict(name=service,dependencies=dependencies,mappings=metrics),config.types))
    structural=StructuralGraph(config=config)
    upstream=structural.visit()
    graph=nx.DiGraph();graph.add_edges_from((f'{u.entity}_{u.metric}',f'{v.entity}_{v.metric}') for u,v in upstream.edges)
    graph.add_nodes_from(f'{u.entity}_{u.metric}' for u in upstream.nodes)
    missing=sorted({r['column'] for r in known}-set(graph.nodes))
    if retain_isolates:graph.add_nodes_from(sorted(r['column'] for r in known))
    scc=sorted([sorted(x) for x in nx.strongly_connected_components(graph) if len(x)>1],key=lambda x:x[0])
    isolated=sorted(nx.isolates(graph))
    report=dict(mapping=mapping,unknown=[r for r in mapping if r['status']!='mapped'],original_missing_nodes=missing,retain_isolates=retain_isolates,metric_nodes=len(graph),metric_edges=graph.number_of_edges(),dag=nx.is_directed_acyclic_graph(graph),call_dag=nx.is_directed_acyclic_graph(call_graph),meta_dag=nx.is_directed_acyclic_graph(structural._skeleton),nontrivial_scc=scc,isolated=isolated,service_without_trace=sorted({r['service'] for r in known}-set(call_graph.nodes)),service_without_call_edge=sorted(s for s in {r['service'] for r in known} if s not in call_graph or call_graph.degree(s)==0),call_edges=sorted(map(list,call_graph.edges)),assumptions=assumptions,source_revision='0215e1880096aa02a305c697f1c23cac4600ebd2',empty_meta_forwarding='upstream StructuralGraph.visit',coverage_policy='retain mapped isolated nodes; pending WHY' if retain_isolates else 'original candidate coverage')
    return graph,report
