"""KT7: additive source-A trace-latency attribution from exact saved intermediates."""
import pathlib,json,sys,hashlib,collections,time
import numpy as np
import pandas as pd
B=pathlib.Path('/home/ubuntu/rca/T-032');O=B/'runs/bo-sung-toan-dien-20261012-001/toraiA/attempt004-allcolumns';O.mkdir(parents=True,exist_ok=False)
sys.path.insert(0,str(B/'scripts'));import tracerca_core_and_td_v1 as td
from replay_tracerca_v3 import table_columns
sys.path.insert(0,str(B/'repo'));from src.p3.torai_b import ten_cot
sources={}
def read(p):
 sources[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text(encoding='utf-8-sig'))
table=read(B/'runs/torai-severity-table-a-001/summary.json');units={(u['opaque_id'],u['seed']):u for u in table['units']}
plan=read(td.PLAN)['rows'];plans={p['opaque_id']:p for p in plan if p['dataset']=='RE2-TT'}
cases=[];start=time.time()
for ud in sorted((B/'runs/torai-a-obs-001/units').glob('*-s0')):
 u=read(ud/'unit.json');oid=u['opaque_id']; loc=read(ud/'obs/locals.json')['locals'];rec=read(B/'runs/torai-a-obs-001'/u['sham_run_dir']/'ban-ghi-0.json');t=rec['window']['t']
 csv=B/'runs/torai-a-obs-001'/u['sham_run_dir']/'bang/tracets_lat.csv';sources[str(csv)]=hashlib.sha256(csv.read_bytes()).hexdigest();f=pd.read_csv(csv).ffill().fillna(0);ranks=dict(loc['trace_lat_ranks']);n=f[f.time<t];a=f[f.time>=t]
 raw={};cs={}
 for c,s in ranks.items():
  x=n[c].to_numpy(float);y=a[c].to_numpy(float);mean=x.mean();std=x.std();scale=std if std else 1.;raw[c]=float(np.max(np.abs((y-mean)/scale)));cs[c]={'share':s,'mean_N':float(mean),'std_N':float(std),'max_A':float(y.max()),'mean_A':float(y.mean())}
 total=sum(raw.values());worst=max((abs(raw[c]/total-s)/max(abs(s),1e-300) for c,s in ranks.items()),default=0) if total else 0
 assert worst<1e-9,(oid,worst)
 sys.path.insert(0,str(B/'repo/src'));from p3 import selector,cua_so
 allow=selector.nap_allowlist(B/'repo/results/T-022/allowlist-dev.json');files=selector.chon_ca(allow,oid,pathlib.Path('/home/ubuntu/rca/T-031/repo'),kiem_hash=True)
 sp=pd.read_parquet(files['traces.parquet']);sources[str(files['traces.parquet'])]=td.sha(files['traces.parquet'])
 names,_=ten_cot(sp)
 keys=sp.traceID.astype(str)+'|'+sp.spanID.astype(str);parent=sp.traceID.astype(str)+'|'+sp.parentSpanID.astype(str);dups=keys.duplicated(False);idx={k:i for i,k in enumerate(keys) if not dups.iloc[i]}
 parents=np.array([idx.get(k,-1) for k in parent]);svc=sp.serviceName.astype(str).to_numpy();children=collections.defaultdict(list)
 for i,j in enumerate(parents):
  if j>=0:children[j].append(i)
 lo=int(a.time.min())*1000000;hi=(int(a.time.max())+15)*1000000;after=(sp.startTime.to_numpy(np.int64)>=lo)&(sp.startTime.to_numpy(np.int64)<hi)
 by_service=collections.defaultdict(list)
 for c,v in sorted(ranks.items(),key=lambda x:-x[1]):by_service[c.split('_')[0]].append(c)
 columns={};service_rows={}
 for service,cols in by_service.items():
  for c in cols:
   ii=np.flatnonzero((names.to_numpy()==c)&after);direct=collections.Counter();desc=collections.Counter()
   for i in ii:
    for ch in children.get(i,[]):
     if svc[ch]!=svc[i]:direct[svc[ch]]+=1
    seen=set();stack=list(children.get(i,[]))
    while stack:
     ch=stack.pop()
     if ch in seen:continue
     seen.add(ch)
     if svc[ch]!=svc[i]:desc[svc[ch]]+=1
     stack.extend(children.get(ch,[]))
   x=n[c].to_numpy(float);y=a[c].to_numpy(float);zs=np.abs((y-x.mean())/(x.std() if x.std() else 1.));imax=int(np.argmax(zs))
   columns[c]={'column':c,**cs[c],'raw_max_abs_z':raw[c],'max_z_bin_time':int(a.time.iloc[imax]),'value_at_max_z':float(y[imax]),'n_matched_spans_A':int(len(ii)),'direct_callee_span_counts':dict(direct),'descendant_span_counts':dict(desc)}
  service_rows[service]={'trace_service_share':sum(ranks[c] for c in cols),'n_columns':len(cols),'top_column':cols[0],'operation_columns':[columns[c] for c in cols]}
 # Labels are joined only after all service computations.
 lab=units[(oid,0)];root=lab['root'];above=lab.get('above_root',[]);above_services=[x.get('entity',x.get('service')) for x in above]
 if any(s is None for s in above_services):raise RuntimeError('above-root field unknown')
 checks=[]
 root_share=service_rows.get(root,{}).get('trace_service_share',0.)
 assert abs(root_share-lab['root_vector']['trace_lat'])<1e-12,(oid,root,'trace root sum')
 for pair in above:
  service=pair['entity'];ss=service_rows.get(service,{}).get('trace_service_share',0.);diff=ss-root_share
  assert abs(diff-pair['difference_by_source']['trace_lat'])<1e-12,(oid,service,'trace margin')
  assert abs(sum(pair['difference_by_source'].values())/4-pair['severity_minus_root'])<1e-12
  cc=service_rows.get(service,{}).get('operation_columns',[])
  checks.append({'above_root_service':service,'largest_source_difference':pair['largest_source_difference'],'trace_margin':diff,'severity_margin':pair['severity_minus_root'],'all_trace_sum_matches_source':True,'n_columns':len(cc),'n_matched_columns':sum(z['n_matched_spans_A']>0 for z in cc),'n_columns_with_observed_descendant_root':sum(z['descendant_span_counts'].get(root,0)>0 for z in cc),'share_from_columns_with_observed_descendant_root':sum(z['share'] for z in cc if z['descendant_span_counts'].get(root,0)>0),'share_from_columns_without_observed_descendant_root':sum(z['share'] for z in cc if z['n_matched_spans_A']>0 and z['descendant_span_counts'].get(root,0)==0),'share_from_unmapped_columns':sum(z['share'] for z in cc if z['n_matched_spans_A']==0)})
 cases.append({'opaque_id':oid,'root':root,'fault':lab['fault'],'nativeA_rank_max':lab['root_rank_max'],'raw_start_bin_A_us':[lo,hi],'rebuild_relative_error':worst,'all_services':service_rows,'above_root_pairs':checks,'root_trace_share_matches_source':True,'coverage_limit':'All contributing columns, exact source-A start bins, full raw dev tree. Associated operation counts/shares do not identify the flagged spans; author encoder/threshold lineage not reproduced. A matching operation with root descendant does not establish physical waiting or root-caused score.'})

 print(json.dumps({'opaque_id':oid,'cases_done':len(cases),'elapsed_s':time.time()-start}),flush=True)
r={'schema':'KT7-TORAI-A-trace-attribution','method_rerun':False,'cases':cases,'source_hashes':sources,'elapsed_s':time.time()-start,'summary':{'cases':len(cases),'rebuild_pass':len(cases),'pairs_above_root':sum(len(c['above_root_pairs']) for c in cases),'pairs_any_column_observed_descendant_root':sum(p['n_columns_with_observed_descendant_root']>0 for c in cases for p in c['above_root_pairs'])}}
(O/'summary.json').write_text(json.dumps(r,ensure_ascii=False,indent=1),encoding='utf-8');print(json.dumps(r['summary'],ensure_ascii=False))
