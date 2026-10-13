"""Correlation fields and explicitly non-identifying coarse time/entity joins."""
import collections,importlib.util,json,pathlib,re,time
import numpy as np,pandas as pd
import pyarrow.parquet as pq
sp=importlib.util.spec_from_file_location('c',pathlib.Path(__file__).with_name('context.py'));c=importlib.util.module_from_spec(sp);sp.loader.exec_module(c);w=c.w
ID=re.compile(r'\b(trace[-_ ]?id|span[-_ ]?id|request[-_ ]?id|correlation[-_ ]?id|x-b3-traceid|x-b3-spanid|traceparent)\s*[:=]\s*[\'\"]?([A-Za-z0-9-]+)',re.I)
TOKEN=re.compile(r'\b(?:trace[-_ ]?id|span[-_ ]?id|request[-_ ]?id|correlation[-_ ]?id|x-b3-traceid|x-b3-spanid|traceparent)\b',re.I)
rows=[]
for ci,item in enumerate(w.S['cases']):
 oid=item['opaque_id'];p=w.OUT/(oid+'--log-semantics.json')
 # Dependency: complete decoder artifact required; never infer no-outcomes.
 if not p.exists():raise RuntimeError('Log decoder not complete: '+oid)
 decoded=json.loads(p.read_text())
 if decoded['status']=='N/A_MISSING_CHANNEL':rows.append({'opaque_id':oid,'status':'N/A_MISSING_CHANNEL'});continue
 started=time.perf_counter();logpath=w.raw_path(item,'logs.parquet');logs=pd.read_parquet(logpath);_,z=w.input_arrays(oid);times=z['times'];points=decoded['region_points'];region=np.zeros(len(logs),bool)
 for point in points:region|=(logs['timestamp'].to_numpy()>=times[max(0,point-60)])&(logs['timestamp'].to_numpy()<times[min(len(times)-1,point+59)]+1)
 assert int(region.sum())==decoded['region_rows'];explicit=[];tokens_without_values=[]
 for ix in np.flatnonzero(region):
  msg=logs.iloc[ix]['message']
  if pd.isna(msg):continue
  found=ID.findall(msg)
  if found:explicit.append({'source_row':int(ix),'container_name':str(logs.iloc[ix]['container_name']),'timestamp':int(logs.iloc[ix]['timestamp']),'fields':[{'literal_key':key,'literal_value':value} for key,value in found]})
  elif TOKEN.search(msg):tokens_without_values.append(int(ix))
 contextrel=c.context_rel(oid);ctx=np.load(w.source(contextrel),allow_pickle=False);metadata=w.read(contextrel[:-4]+'.json')['summary'];entities=metadata['trace']['entities'];counts={}
 for s,e,n in zip(ctx['trace_group_second'],ctx['trace_group_entity'],ctx['trace_group_span_count']):counts[(int(s),entities[int(e)])]=int(n)
 a=np.load(w.OUT/(oid+'--http-access-observed.npz'),allow_pickle=False);hist=collections.Counter();byentity={}
 for timestamp,entity,status in zip(a['timestamp'],a['container_name'],a['status']):
  n=counts.get((int(timestamp),str(entity)),0);key='zero_span_candidate' if n==0 else ('one_span_candidate' if n==1 else 'multiple_span_candidates');hist[key]+=1
  ee=byentity.setdefault(str(entity),{'HTTP_rows':0,'trace_entity_literal_present':str(entity) in entities,'same_second_span_candidate_count_histogram':collections.Counter(),'HTTP_status_counts':collections.Counter()});ee['HTTP_rows']+=1;ee['same_second_span_candidate_count_histogram'][str(n)]+=1;ee['HTTP_status_counts'][str(status)]+=1
 traceraw=w.raw_path(item,'traces.parquet')
 rows.append({'opaque_id':oid,'status':'PASS','region_rows':int(region.sum()),'HTTP_observed_rows':len(a['timestamp']),'explicit_correlation_ID_rows':explicit,'correlation_token_without_parse_source_rows':tokens_without_values,'same_literal_entity_same_second_coarse_candidate_histogram':dict(hist),'HTTP_entities':byentity,'trace_source_columns':pq.read_schema(traceraw).names,'log_source_columns':logs.columns.tolist(),'trace_context_source':contextrel,'log_semantics_source':{'file':p.name,'bytes':p.stat().st_size,'sha256':w.sha(p)},'join_meaning':'Same container name and source second is a coarse co-occurrence check, never a certified invocation join. One candidate can still differ due start/completion semantics, clockoffset, missing/duplicate spans and logging coverage. UI access status cannot be attached to internal span without verified correlation key/protocol mapping.','body_wall_s':time.perf_counter()-started});w.emit({'log_correlation_case':ci+1,'HTTP_rows':len(a['timestamp']),'explicit_ID_rows':len(explicit),'coarse_candidates':dict(hist)})
w.write('log-correlation-summary-001.json',{'status':'COMPLETE','cases':rows,'semantic_scope':'Outcome availability depends channel/location. Parsed access HTTP statuses exist for recorded UI requests; per-invocation outcomes on internal trace edges and full system truth remain unverified without correlation/completeness.'});w.emit({'log_correlation':'COMPLETE','cases':len(rows)})
