"""Run author code components unchanged with a latency-only, short-reference adapter."""
import pathlib,sys,json,hashlib,time,importlib,importlib.util,traceback,collections
import numpy as np
import pandas as pd
B=pathlib.Path('/home/ubuntu/rca/T-032');O=B/'runs/bo-sung-toan-dien-20261012-001/author-tracerca';SRC=O/'source'
sys.path[:0]=[str(O/'deps'),str(SRC),str(B/'scripts')]
import tracerca_core_and_td_v1 as td
from replay_tracerca_v3 import table_columns
selection=importlib.import_module('run_selecting_features');detection=importlib.import_module('run_anomaly_detection_invo');mining=importlib.import_module('run_localization_association_rule_mining_20210516')
spec=importlib.util.spec_from_file_location('author_stream_v3',O.parent/'author_streaming-v4-instrumented.py');stream=importlib.util.module_from_spec(spec);spec.loader.exec_module(stream)
plan=td.read(td.PLAN)['rows'];labels=td.read(td.LABELS)['main_rows'];labelmap={(x['dataset'],x['opaque_id']):x for x in labels if x['method']=='tracerca'}
attempt=O/sys.argv[1];attempt.mkdir(exist_ok=False);rows=[];sources={};start=time.time()
for p in SRC.rglob('*.py'):sources[str(p)]=td.sha(p)
for row in plan:
 oid=row['opaque_id'];dataset=row['dataset'];directory=td.REUSED.get(row.get('replay_phase_already_valid'),td.COHORT/'cases'/dataset/oid);cp=directory/'capture/calls/001-adapter.json'
 try:
  if cp.exists():
   sources[str(cp)]=td.sha(cp);meta=td.read(cp);sp=pd.DataFrame(table_columns(directory/'capture',meta['entry']['input']));t=int(meta['entry']['t_seconds'])*1000000
  elif dataset=='RE2-TT':
   sys.path.insert(0,str(B/'repo/src'));from p3 import selector,cua_so
   allow=selector.nap_allowlist(B/'repo/results/T-022/allowlist-dev.json');files=selector.chon_ca(allow,oid,pathlib.Path('/home/ubuntu/rca/T-031/repo'),kiem_hash=True)
   t=int(row['window']['t'])*1000000;sp=cua_so.cat_span(pd.read_parquet(files['traces.parquet']),t//1000000)
   sources[str(files['traces.parquet'])]=td.sha(files['traces.parquet'])
  else:raise FileNotFoundError(cp)
  key=sp.traceID.astype(str)+'|'+sp.spanID.astype(str);dup=key.duplicated(False);lookup={k:i for i,k in enumerate(key) if not dup.iloc[i]};pa=sp.traceID.astype(str)+'|'+sp.parentSpanID.astype(str);par=np.array([lookup.get(k,-1) for k in pa]);svc=sp.serviceName.astype(str).to_numpy();st=sp.startTime.to_numpy(np.int64);dur=sp.duration.to_numpy(np.int64);tr=sp.traceID.astype(str).to_numpy()
  eligible=np.flatnonzero((par>=0)&np.array([svc[i]!=svc[j] if j>=0 else False for i,j in enumerate(par)])); seen=set();inv=[]
  for i in eligible:
   j=int(par[i]);u=(j,svc[i])
   if u in seen:continue
   seen.add(u);inv.append({'source':svc[j],'target':svc[i],'trace_id':tr[i],'start':int(st[j]),'end':int(st[j]+dur[j]),'latency':float(dur[j])/1000})
  base_df=pd.DataFrame(inv)
  for unit_scale,latency_unit in [(1.,'ms'),(1000.,'us')]:
   df=base_df.copy();df['latency']*=unit_scale;normal=df[df.end<t];anomal=df[df.end>=t].copy();normal_groups={pair:g.latency.to_numpy() for pair,g in normal.groupby(['source','target'])};cache={}
   for pair,x in normal_groups.items():cache[f'reference-{pair[0]}-{pair[1]}-latency-mean-variance']={'mean':float(x.mean()),'std':float(max(x.std(),.1))}
   for threshold in [1.,3.]:
    empirical_groups={pair:g.latency.to_numpy() for pair,g in anomal.groupby(['source','target'])};features={p:['latency'] for p,x in empirical_groups.items() if p in normal_groups and selection.stderr_criteria(np.sort(x),np.sort(normal_groups[p]),threshold)}
    current=anomal.set_index(['source','target'],drop=False).sort_index();detection.threshold=1.
    flagged=detection.anomaly_detection_3sigma(current,'Ours-predict',None,features,cache);flagged['predict']=flagged['Ours-predict'];before_flags=int(flagged['predict'].sum());native_input=mining.inject_noise(flagged,ratio=0);after_flags=int(native_input['predict'].sum());capture={};klass=mining.TraceRCA
    if after_flags:
     rank,details,stream_stat=stream.stream_rank(native_input,mining)
     capture={'item_ret':details};score={sv:float(details[sv]['score']) for sv in rank};status='OK' if rank else 'NO_EVIDENCE'
    else:rank=[];score={};status='NO_EVIDENCE';stream_stat={'patterns_seen':0,'patterns_retained':0}
    # Root is joined only after feature/flag/mining/rank computations.
    lab=labelmap[(dataset,oid)];root=lab['root'];v=score.get(root);rmin=1+sum(x>v for x in score.values()) if v is not None else None;rmax=sum(x>=v for x in score.values()) if v is not None else None
    item={'dataset':dataset,'opaque_id':oid,'feature_selection_threshold':threshold,'latency_unit':latency_unit,'status':status,'root':root,'fault':lab['fault'],'root_rank_min':rmin,'root_rank_max':rmax,'ranking':rank,'scores':score,'N_invocations':len(normal),'A_invocations':len(anomal),'N_pairs':len(normal_groups),'A_pairs':len(empirical_groups),'selected_pairs':len(features),'missing_history_pairs':sum(p not in normal_groups for p in empirical_groups),'span_duplicate_identity_count':int(dup.sum()),'flags_before_default_noise0':before_flags,'flags_after_default_noise0':after_flags,'stream':stream_stat,'patterns_retained':stream_stat.get('patterns_retained',0),'selected_pair_names':[list(p) for p in sorted(features)],'feature_missing_history_pairs_ignored':sum(p not in normal_groups for p in empirical_groups),'native_cache_fallback_pairs_used':0,'score_details':{s:{k:(sorted(vv) if isinstance(vv,frozenset) else float(vv) if isinstance(vv,(np.integer,np.floating)) else vv) for k,vv in x.items()} for s,x in (capture.get('item_ret') or {}).items()},'limit':'LATENCY_ONLY; SHORT_HISTORY; parent duration mapping may aggregate children. Default http_status unavailable. Not published/default reproduction.'}
    rows.append(item)
    (attempt/(dataset+'--'+oid+'--'+latency_unit+'--'+str(int(threshold))+'.json')).write_text(json.dumps(item,ensure_ascii=False,indent=1),encoding='utf-8')
 except Exception as e:
  rows.append({'dataset':dataset,'opaque_id':oid,'status':'ERROR','error':repr(e),'traceback':traceback.format_exc()})
 (attempt/'progress.json').write_text(json.dumps({'cases_done':len({(r['dataset'],r['opaque_id']) for r in rows}),'elapsed_s':time.time()-start}),encoding='utf-8')
 print(json.dumps({'case':oid,'dataset':dataset,'rows_done':len(rows),'elapsed_s':time.time()-start}),flush=True)
 if '--pilot' in sys.argv:break
r={'schema':'TraceRCA-author-code-latency-only-supported-probe','source_revision':'b9087c72d201fbb17d724114cd389de4854815ad','source_hashes':sources,'rows':rows,'elapsed_s':time.time()-start,'default_pipeline_status':'UNSUPPORTED: missing http_status, missing raw decoder module, no multi-day reference; no fill of unavailable outcomes.'}
(attempt/'summary.json').write_text(json.dumps(r,ensure_ascii=False,indent=1),encoding='utf-8');print(json.dumps({'done':True,'rows':len(rows),'elapsed_s':time.time()-start}))
