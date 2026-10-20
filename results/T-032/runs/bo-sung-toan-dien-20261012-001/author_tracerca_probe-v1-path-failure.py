"""Run author code components unchanged with a latency-only, short-reference adapter."""
import pathlib,sys,json,hashlib,time,importlib,traceback,collections
import numpy as np
import pandas as pd
B=pathlib.Path('/home/ubuntu/rca/T-032');O=B/'runs/bo-sung-toan-dien-20261012-001/author-tracerca';SRC=O/'source'
sys.path[:0]=[str(O/'deps'),str(SRC),str(B/'scripts')]
import tracerca_core_and_td_v1 as td
from replay_tracerca_v3 import table_columns
selection=importlib.import_module('run_selecting_features');detection=importlib.import_module('run_anomaly_detection_invo');mining=importlib.import_module('run_localization_association_rule_mining_20210516')
plan=td.read(td.PLAN)['rows'];labels=td.read(td.LABELS)['main_rows'];labelmap={(x['dataset'],x['opaque_id']):x for x in labels if x['method']=='tracerca'}
attempt=O/sys.argv[1];attempt.mkdir(exist_ok=False);rows=[];sources={};start=time.time()
for p in SRC.rglob('*.py'):sources[str(p)]=td.sha(p)
for row in plan:
 oid=row['opaque_id'];dataset=row['dataset'];directory=td.REUSED.get(row.get('replay_phase_already_valid'),td.COHORT/'cases'/dataset/oid);cp=directory/'capture/calls/001-adapter.json'
 try:
  sources[str(cp)]=td.sha(cp);meta=td.read(cp);sp=pd.DataFrame(table_columns(directory/'capture',meta['entry']['input']));t=int(meta['entry']['t_seconds'])*1000000
  key=sp.traceID.astype(str)+'|'+sp.spanID.astype(str);dup=key.duplicated(False);lookup={k:i for i,k in enumerate(key) if not dup.iloc[i]};pa=sp.traceID.astype(str)+'|'+sp.parentSpanID.astype(str);par=np.array([lookup.get(k,-1) for k in pa]);svc=sp.serviceName.astype(str).to_numpy();st=sp.startTime.to_numpy(np.int64);dur=sp.duration.to_numpy(np.int64);tr=sp.traceID.astype(str).to_numpy()
  eligible=np.flatnonzero((par>=0)&np.array([svc[i]!=svc[j] if j>=0 else False for i,j in enumerate(par)])); seen=set();inv=[]
  for i in eligible:
   j=int(par[i]);u=(j,svc[i])
   if u in seen:continue
   seen.add(u);inv.append({'source':svc[j],'target':svc[i],'trace_id':tr[i],'start':int(st[j]),'end':int(st[j]+dur[j]),'latency':float(dur[j])/1000})
  df=pd.DataFrame(inv);normal=df[df.end<t];anomal=df[df.end>=t].copy();normal_groups={pair:g.latency.to_numpy() for pair,g in normal.groupby(['source','target'])};cache={}
  for pair,x in normal_groups.items():cache[f'reference-{pair[0]}-{pair[1]}-latency-mean-variance']={'mean':float(x.mean()),'std':float(max(x.std(),.1))}
  for threshold in [1.,3.]:
   empirical_groups={pair:g.latency.to_numpy() for pair,g in anomal.groupby(['source','target'])};features={p:['latency'] for p,x in empirical_groups.items() if p in normal_groups and selection.stderr_criteria(x,normal_groups[p],threshold)}
   current=anomal.set_index(['source','target'],drop=False).sort_index();detection.threshold=1.
   flagged=detection.anomaly_detection_3sigma(current,'Ours-predict',None,features,cache);flagged['predict']=flagged['Ours-predict'];before_flags=int(flagged['predict'].sum());native_input=mining.inject_noise(flagged,ratio=0);after_flags=int(native_input['predict'].sum());capture={};klass=mining.TraceRCA
   if after_flags:
    def prof(frame,event,arg):
     if event=='return' and frame.f_code is klass.__call__.__code__:capture.update({k:frame.f_locals.get(k) for k in ['item_ret','patterns','pattern_scores']})
    old=sys.getprofile();sys.setprofile(prof)
    try:rank=klass()(native_input,min_support_rate=.1,k=100,quiet=True,forbidden_names=frozenset({'gateway'}),enable_PRFL=False)
    finally:sys.setprofile(old)
    score={s:float(capture['item_ret'][s]['score']) for s in rank} if rank else {};status='OK' if rank else 'NO_EVIDENCE'
   else:rank=[];score={};status='NO_EVIDENCE'
   # Root is joined only after feature/flag/mining/rank computations.
   lab=labelmap[(dataset,oid)];root=lab['root'];v=score.get(root);rmin=1+sum(x>v for x in score.values()) if v is not None else None;rmax=sum(x>=v for x in score.values()) if v is not None else None
   item={'dataset':dataset,'opaque_id':oid,'feature_selection_threshold':threshold,'status':status,'root':root,'fault':lab['fault'],'root_rank_min':rmin,'root_rank_max':rmax,'ranking':rank,'scores':score,'N_invocations':len(normal),'A_invocations':len(anomal),'N_pairs':len(normal_groups),'A_pairs':len(empirical_groups),'selected_pairs':len(features),'missing_history_pairs':sum(p not in normal_groups for p in empirical_groups),'span_duplicate_identity_count':int(dup.sum()),'flags_before_default_noise0':before_flags,'flags_after_default_noise0':after_flags,'patterns_retained':len(capture.get('patterns') or []),'score_details':{s:{k:(sorted(vv) if isinstance(vv,frozenset) else float(vv) if isinstance(vv,(np.integer,np.floating)) else vv) for k,vv in x.items()} for s,x in (capture.get('item_ret') or {}).items()},'limit':'LATENCY_ONLY; SHORT_HISTORY; parent duration mapping may aggregate children. Default http_status unavailable. Not published/default reproduction.'}
   rows.append(item)
 except Exception as e:
  rows.append({'dataset':dataset,'opaque_id':oid,'status':'ERROR','error':repr(e),'traceback':traceback.format_exc()})
 (attempt/'progress.json').write_text(json.dumps({'cases_done':len({(r['dataset'],r['opaque_id']) for r in rows}),'elapsed_s':time.time()-start}),encoding='utf-8')
 print(json.dumps({'case':oid,'dataset':dataset,'rows_done':len(rows),'elapsed_s':time.time()-start}),flush=True)
 if '--pilot' in sys.argv:break
r={'schema':'TraceRCA-author-code-latency-only-supported-probe','source_revision':'b9087c72d201fbb17d724114cd389de4854815ad','source_hashes':sources,'rows':rows,'elapsed_s':time.time()-start,'default_pipeline_status':'UNSUPPORTED: missing http_status, missing raw decoder module, no multi-day reference; no fill of unavailable outcomes.'}
(attempt/'summary.json').write_text(json.dumps(r,ensure_ascii=False,indent=1),encoding='utf-8');print(json.dumps({'done':True,'rows':len(rows),'elapsed_s':time.time()-start}))
