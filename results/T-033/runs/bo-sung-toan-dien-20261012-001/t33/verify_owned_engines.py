"""Source/input/output invariants for owned engine cases; no method rerun."""
import datetime,importlib.util,json,pathlib
import numpy as np
sp=importlib.util.spec_from_file_location('w',pathlib.Path(__file__).with_name('worker-v3.py'));w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
branches=['prior_df4','prior_kappa4','prior_precision4','causal_fixed','causal_expanding','compressed_row','compressed_calendar'];rows=[];pins=[]
for ci,item in enumerate(w.S['cases'][:14]):
 oid=item['opaque_id'];rel,z=w.input_arrays(oid);X=z['X'];times=z['times'];sham=w.OUT/(oid+'--full-sham-thread1.json');sv=json.loads(sham.read_text());assert sv['native_full_sham_exact'] and sv['source']==rel;pins.append({'file':sham.name,'bytes':sham.stat().st_size,'sha256':w.sha(sham)})
 compact=w.OUT/'migration-inputs-001';manifest=json.loads((compact/'manifest.json').read_text());meta=manifest['cases'][ci];q=compact/meta['file'];assert w.sha(q)==meta['sha256'];raw=np.load(q,allow_pickle=False)['causal_raw'];columns=np.load(q,allow_pickle=False)['causal_columns'].tolist()
 for branch in branches:
  q=w.OUT/(oid+'--'+branch+'.json');v=json.loads(q.read_text());assert v['status']=='PASS' and v['source']==rel and v['opaque_id']==oid and v['branch']==branch
  m=np.array(v['m']);engine=np.array(v['engine_CP_flags'],bool);flags=np.array(v['CP_flags'],bool);mapping=np.array(v['retained_original_indices']);alarmidx=np.array(v['alarm_original_indices']);alarms=np.array(v['alarms']);assert np.array_equal(engine,np.r_[False,np.abs(np.diff(m))>1]);assert (m>=0).all() and (m<=np.arange(len(m))+1).all()
  if branch.startswith('causal'):
   xx=w.causal(raw,'fixed' if branch=='causal_fixed' else 'expanding');assert v['schema_columns']==columns;expected=engine.copy();expected[:100]=False;assert v['alarm_evaluation_start']==100
  elif branch.startswith('compressed'):
   keep=np.r_[True,np.any(X[1:]!=X[:-1],axis=1)];assert np.array_equal(mapping,np.flatnonzero(keep));xx=X[keep];expected=engine
  else:xx=X;expected=engine
  if not branch.startswith('compressed'):assert np.array_equal(mapping,np.arange(len(X)))
  assert np.array_equal(flags,expected) and list(xx.shape)==v['X_shape'] and __import__('hashlib').sha256(xx.tobytes()).hexdigest()==v['X_sha256']
  assert np.array_equal(mapping[np.flatnonzero(flags)],alarmidx) and np.array_equal(times[alarmidx],alarms)
  old=times[z['CP_flags']];assert v['CP_set_added']==sorted(set(alarms.tolist())-set(old.tolist())) and v['CP_set_removed']==sorted(set(old.tolist())-set(alarms.tolist()))
  assert len(v['selected_posterior'])==int(engine.sum())
  for a in v['selected_posterior']:
   i=a['index'];assert engine[i] and a['m']==int(m[i]) and np.isfinite(a['p_map']) and 0<=a['p_map']<=1 and 0<=a['p_reset']<=1
  pins.append({'file':q.name,'bytes':q.stat().st_size,'sha256':w.sha(q)});rows.append({'case':ci+1,'opaque_id':oid,'branch':branch,'n':len(m),'d':xx.shape[1],'CP_count':int(flags.sum()),'native_sham':True,'source_X_exact_hash':True,'engine_CP_rule_exact':True,'warmup_release_or_mapping_exact':True,'wall_s':v['wall_s'],'file':q.name})
boundary=[]
for pid,last,startcase in [(51071,13,15),(51840,14,16)]:
 q=w.OUT/('migration-boundary-'+str(pid)+'.json');v=json.loads(q.read_text());assert v['status']=='OWNED_CASES_COMPLETE_PROCESS_INTERRUPTED_AT_UNOWNED_NATIVE_START' and v['last_owned_case']==last and v['interrupted_start']=={'case':startcase,'branch':'native-full-sham-thread1','state':'START'};boundary.append(v);pins.append({'file':q.name,'bytes':q.stat().st_size,'sha256':w.sha(q)})
 q2=w.OUT/(w.S['cases'][startcase-1]['opaque_id']+'--full-sham-thread1.json');assert not q2.exists(),'Unowned native output unexpectedly completed on T33'
complete=w.OUT/'migration-boundary-complete.json';v=json.loads(complete.read_text());assert v['owned_cases']==list(range(1,15)) and v['delegated_cases']==list(range(15,31));pins.append({'file':complete.name,'bytes':complete.stat().st_size,'sha256':w.sha(complete)})
w.write('owned-engine-verification-001.json',{'status':'PASS_OWNED_14CASES_112SLOTS','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_sham_slots':14,'intervention_slots':len(rows),'scientific_slots':14+len(rows),'rows':rows,'source_files':pins,'boundary_receipts':boundary,'interpretation':'Cases1–14 completed with native m/CP sham gates recorded and new X/CP/mapping invariants verified; native attempted starts15/16 intentionally interrupted at ownership boundary and excluded. Verification does not recompute posterior or infer operational quality from CP counts.'});w.emit({'owned_engine_verification':'PASS','native_shams':14,'branches':len(rows),'slots':14+len(rows),'bytes':sum(x['bytes'] for x in pins)})
