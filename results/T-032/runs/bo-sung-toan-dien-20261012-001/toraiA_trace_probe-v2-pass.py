"""KT7: additive source-A trace-latency attribution from exact saved intermediates."""
import pathlib,json,sys,hashlib,collections,time
import numpy as np
import pandas as pd
B=pathlib.Path('/home/ubuntu/rca/T-032');O=B/'runs/bo-sung-toan-dien-20261012-001/toraiA/attempt002';O.mkdir(parents=True,exist_ok=False)
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
 p=plans[oid];directory=td.REUSED.get(p.get('replay_phase_already_valid'),td.COHORT/'cases'/'RE2-TT'/oid)
 if (directory/'capture/calls/001-adapter.json').exists():
  meta=read(directory/'capture/calls/001-adapter.json');sp=pd.DataFrame(table_columns(directory/'capture',meta['entry']['input']))
 else:
  sys.path.insert(0,str(B/'repo/src'));from p3 import selector,cua_so
  allow=selector.nap_allowlist(B/'repo/results/T-022/allowlist-dev.json');files=selector.chon_ca(allow,oid,pathlib.Path('/home/ubuntu/rca/T-031/repo'),kiem_hash=True)
  sp=cua_so.cat_span(pd.read_parquet(files['traces.parquet']),t)
 names,_=ten_cot(sp)
 keys=sp.traceID.astype(str)+'|'+sp.spanID.astype(str);parent=sp.traceID.astype(str)+'|'+sp.parentSpanID.astype(str);dups=keys.duplicated(False);idx={k:i for i,k in enumerate(keys) if not dups.iloc[i]}
 parents=np.array([idx.get(k,-1) for k in parent]);svc=sp.serviceName.astype(str).to_numpy();children=collections.defaultdict(list)
 for i,j in enumerate(parents):
  if j>=0:children[j].append(i)
 after=(sp.startTime.to_numpy(np.int64)+sp.duration.to_numpy(np.int64)>=t*1000000)
 top={}
 for c,v in sorted(ranks.items(),key=lambda x:-x[1]):top.setdefault(c.split('_')[0],c)
 service_rows={}
 for service,c in top.items():
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
  service_rows[service]={'top_column':c,**cs[c],'n_matched_spans_A':len(ii),'direct_callee_span_counts':dict(direct),'descendant_span_counts':dict(desc)}
 # Labels are joined only after all service computations.
 lab=units[(oid,0)];root=lab['root'];above=lab.get('above_root',[]);above_services=[x.get('entity',x.get('service')) for x in above]
 if any(s is None for s in above_services):raise RuntimeError('above-root field unknown')
 cases.append({'opaque_id':oid,'root':root,'fault':lab['fault'],'nativeA_rank_max':lab['root_rank_max'],'rebuild_relative_error':worst,'all_services':service_rows,'above_root_services':above_services,'above_root_root_descendant':{s:service_rows.get(s,{}).get('descendant_span_counts',{}).get(root,0) for s in above_services},'coverage_limit':'Source-A table may use full-file threshold/aligned15s bins; tree attribution reads locked native window only. Counts are span occurrences, not independent traces or physical waiting.'})
 print(json.dumps({'opaque_id':oid,'cases_done':len(cases),'elapsed_s':time.time()-start}),flush=True)
r={'schema':'KT7-TORAI-A-trace-attribution','method_rerun':False,'cases':cases,'source_hashes':sources,'elapsed_s':time.time()-start,'summary':{'cases':len(cases),'rebuild_pass':len(cases),'pairs_above_root':sum(len(c['above_root_services']) for c in cases),'pairs_top_column_observed_descendant_root':sum(v>0 for c in cases for v in c['above_root_root_descendant'].values())}}
(O/'summary.json').write_text(json.dumps(r,ensure_ascii=False,indent=1),encoding='utf-8');print(json.dumps(r['summary'],ensure_ascii=False))
