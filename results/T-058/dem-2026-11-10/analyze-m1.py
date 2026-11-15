"""Read frozen inputs/outputs, without rerunning or tuning M1."""
from collections import Counter
import hashlib,json,math
from pathlib import Path
root=Path(__file__).resolve().parent; base=root/'rca-ban-dau'
result={}
for opaque in ['c12e47ab','f4a8c021']:
 case=base/'cases'/opaque; folder=base/'outputs'/opaque
 manifest=json.loads((case/'manifest.json').read_text(encoding='utf8'))
 for name,meta in manifest['files'].items():
  if hashlib.sha256((case/name).read_bytes()).hexdigest()!=meta['sha256']: raise SystemExit('Frozen input hash mismatch')
 summary=json.loads((folder/'summary.json').read_text(encoding='utf8'))
 for n,expected in enumerate(summary['output_sha256'],1):
  if hashlib.sha256((folder/f'method-output-{n}.json').read_bytes()).hexdigest()!=expected: raise SystemExit('Output hash mismatch')
 spans,metrics,logs,inventory,aliases,t,params=json.loads((folder/'method-input.json').read_text(encoding='utf8'))
 output=json.loads((folder/'method-output-1.json').read_text(encoding='utf8'))
 point=t*10**9; lo=point-300*10**9; hi=point+300*10**9
 channels={}
 for row in metrics:
  if not lo<=row['time']<hi: continue
  for name,value in row.items():
   if not name.startswith('event-service_'): continue
   c=channels.setdefault(name,{'N_finite':0,'A_finite':0,'N_missing':0,'A_missing':0})
   side='N' if row['time']<point else 'A'
   c[side+('_finite' if value is not None and math.isfinite(value) else '_missing')]+=1
 event_spans=Counter('N' if (r['start_us']+r['duration_us'])*1000<point else 'A' for r in spans if r['owner']=='event-service')
 event_logs=Counter('N' if r['timestamp']<point else 'A' for r in logs if r['entity']=='event-service')
 units=[u for u in output['extra']['don_vi_phan_vi'] if '|event-service|' in u['ma'] or u['ma'].startswith('metric|event-service_')]
 # Keep all remaining possible metric naming forms in the evidence, then
 # summarize the event-owned entries explicitly below.
 all_named=[u for u in output['extra']['don_vi_phan_vi'] if 'event-service' in u['ma']]
 graph=output['extra']['canh']
 nodes=sorted({n for edge in graph for n in edge})
 result[opaque]={'status':summary['status'],'deterministic_repeat':summary['deterministic_repeat'],
                 'input_files_verified':len(manifest['files']),'source_pins_checked':summary['source_pins_checked'],
                 'inventory':len(inventory),'spans':len(spans),'metric_rows':len(metrics),'logs':len(logs),
                 'observed':summary['sets']['observed'],'returned':summary['sets']['returned'],
                 'graph_nodes':nodes,'graph_node_count':len(nodes),'graph_edges':graph,'graph_edge_count':len(graph),
                 'diagnostics':summary['diagnostics'],'event_service_span_counts':dict(event_spans),
                 'event_service_log_counts':dict(event_logs),'event_service_metric_sample_counts':channels,
                 'event_named_unit_status_counts':dict(Counter(u['trang_thai'] for u in all_named)),
                 'event_named_units':all_named,'run_seconds':summary['run_seconds'],
                 'adapter_diagnostics':summary['adapter_diagnostics']}
(root/'m1-feasibility-details.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for opaque,d in result.items():
 print(opaque,'graph',d['graph_node_count'],d['graph_edge_count'],'event span N/A',d['event_service_span_counts'])
 print('event metrics',d['event_service_metric_sample_counts'])
 print('event unit statuses',d['event_named_unit_status_counts'])
