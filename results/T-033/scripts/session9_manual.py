"""EC2 only: arrange already saved chains/controls/duration; no detector calls."""
import pathlib,json,hashlib,gzip,math,time,shutil,collections
import numpy as np,psutil
H=pathlib.Path('/home/ubuntu/rca/T-033');OUT=H/'runs/session9-manual-001';OUT.mkdir(exist_ok=False)
verified={}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def checked(rel):
 p=(H/rel).resolve();assert p.is_relative_to(H)
 if rel not in verified:
  m=INPUT['pins'][rel];assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],rel;verified[rel]=m
 return p
def read(rel):return json.loads(checked(rel).read_text())
def clean(x):
 if isinstance(x,np.ndarray):return clean(x.tolist())
 if isinstance(x,np.generic):return clean(x.item())
 if isinstance(x,float) and not math.isfinite(x):return None
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
def write(n,x):
 b=(json.dumps(clean(x),ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode()
 used=sum(p.stat().st_size for p in H.rglob('*') if p.is_file())
 assert used+len(b)+8*2**20<5*2**30 and shutil.disk_usage(H).free>len(b)+8*2**20
 assert time.perf_counter()-_start<_ledger['remaining_approved_s'] and psutil.virtual_memory().percent<95
 (OUT/n).write_bytes(b)
E='runs/session8-evidence-001/'
C=read(E+'chuoi-bang-chung.json');F=read(E+'phan-ra-tien-xu-ly.json');G=read(E+'bao-phu-nhom.json');T=read(E+'tai-log.json')
stats=read('runs/session8-stats-001/stats.json');fact={r['opaque_id']:r for r in F['cases']};context={r['opaque_id']:r for r in T['cases']}
allunits=[];pairs=[];durations=[];safety=collections.Counter();unitmap={};display=[]
for oid in sorted(fact):
 run='session7-manual-pilot-001' if oid=='dev-03d4910932' else 'session7-manual-rest-001'
 pointrel='runs/'+run+'/'+oid+'--points.json.gz';body=json.loads(gzip.decompress(checked(pointrel).read_bytes()))
 cr=context[oid]['record'];ctx=read(cr);nr=(pathlib.Path(cr).parent/ctx['output_npz']).as_posix()
 with np.load(checked(nr),allow_pickle=False) as z:
  second=z['trace_group_second'];entity=z['trace_group_entity'];tnames=ctx['summary']['trace']['entities']
  for i in sorted({p['index'] for u in body['units'] for p in u['points']}):
   sec=int(z['times'][i]);indices=np.flatnonzero(second==sec);dd=[]
   for q in indices:
    dd.append({'source_row':int(q),'entity_index':int(entity[q]),'entity':tnames[int(entity[q])],**{k:clean(z[k][q]) for k in z.files if k.startswith('trace_group_duration_')},'span_count':int(z['trace_group_span_count'][q]),'status_present':int(z['trace_group_status_present'][q]),'status_missing':int(z['trace_group_status_missing'][q])})
   durations.append({'opaque_id':oid,'index':i,'second':sec,'source_npz':nr,'selection':'exact second and entity in trace_group_*; span starts, not duration end','duration_unit':'OPEN_RAW_UNIT','observed_entities':dd,'absent_entity_semantics':'no observed group; not proof of no requests'})
 for u in body['units']:
  det,branch=u['detector'],u['branch'];cu=next(r for r in C['units'] if (r['opaque_id'],r['detector'],r['branch'])==(oid,det,branch))
  dossier={'opaque_id':oid,'detector':det,'branch':branch,'native_status':u['native_status'],'full_points_source':pointrel,'source_unit_index':body['units'].index(u),'points':cu['points'],'delay':cu['delay'],'labels_for_analysis_only':cu['analysis_labels_only'],'physical_onset':'OPEN','scope':'saved computational path; no cause or new detector selection','same_column_controls':[]}
  for p in u['points']:
   if det=='bocpd':
    safety['BO_points']+=1;safety['theta_present' if p['theta_available'] else 'theta_absent']+=1
    assert math.isfinite(p['normalizer']) and p['normalizer']>0
    assert p['CP_flag']==(p['index']>=1 and p['absolute_m_change']>1)
    safety['BO_CP' if p['CP_flag'] else 'BO_noCP']+=1
    if p['CP_flag']:safety['BO_CP_mode_increase' if p['m']>p['previous_m'] else 'BO_CP_mode_decrease']+=1
   else:
    safety['NS_points']+=1;assert p['merged_flag']==any(p['flags'])
    safety['NS_nonfinite_stats_cells']+=sum(not b for b in p['finite_statistics_mask'])
    safety['NS_nonfinite_trigger_cells']+=sum(f and not v for f,v in zip(p['flags'],p['finite_statistics_mask']))
    for phase in ['pre','post']:
     alarm=next((v for v in u['points'] if 'first_'+phase+'_proxy_alarm' in v['roles']),None)
     control=next((v for v in u['points'] if 'nearest_no_alarm_to_first_'+phase in v['roles']),None)
     if alarm is not p:continue
     cols=[j for j,v in enumerate(alarm['flags']) if v];out={'phase':phase,'alarm_index':alarm['index'],'control_index':control['index'] if control else None,'control_status':'LOCKED_NO_MERGED_FLAG' if control else 'NO_VALID_POINT_UNDER_LOCKED_RULE','same_column_values':[]}
     for j in cols:
      c=alarm['columns'][j];v={'column':c,'alarm':{k:alarm[k][j] for k in ['raw_values','x','count','mean','std','threshold','margin','flags','finite_statistics_mask']},'control':None}
      if control:
       assert control['columns']==alarm['columns'] and not control['merged_flag'];v['control']={k:control[k][j] for k in ['raw_values','x','count','mean','std','threshold','margin','flags','finite_statistics_mask']}
      out['same_column_values'].append(v)
     dossier['same_column_controls'].append(out);pairs.append({'opaque_id':oid,'detector':det,**out,'source':pointrel})
  key=(oid,det,branch);unitmap[key]=len(allunits);allunits.append(dossier)
  display.append({'unit_index':unitmap[key],'opaque_id':oid,'detector':det,'branch':branch,'status':u['native_status'],'first_group':cu['analysis_labels_only']['first_group'],'points':[{k:v[k] for k in ['index','roles','flag','trigger_count','CP_flag','m','previous_m','absolute_m_change','MAP_posterior','runner_up','runner_posterior','normalizer','MAP_parent_predictive_density','MAP_parent_prior_posterior','previous_MAP_continuation_posterior','theta_available'] if k in v} for v in cu['points']], 'first_two_alarm_columns':[v['same_column_values'][:2] for v in dossier['same_column_controls']], 'same_column_control_status':[v['control_status'] for v in dossier['same_column_controls']]})
group_rows=[]
for gi,g in enumerate(G['matching']['groups']):
 oid=g['representative'];det=g['detector'];control=g['control'];name=g['group'];paths=['full']
 if name.startswith('factorial/'):
  paths=[name.split('/')[1]]
 elif name.startswith('contrast/') or name.startswith('input-identical/'):
  paths=['FF','FP','PF','PP']
 if det!='bocpd':paths=['full']
 reps=[unitmap[(oid,det,b)] for b in paths if (oid,det,b) in unitmap];controls=[unitmap[(control,det,b)] for b in paths if (control,det,b) in unitmap] if control else []
 assert reps,(name,oid,det,paths)
 row={'group_index':gi,**g,'representative_unit_indices':reps,'control_unit_indices':controls,'underlying_chain_file':'unit-dossiers.json#/units','new_group_members_source':'runs/session6-groups-001/bao-phu-nhom.json#/new_groups' if gi>=40 else 'runs/session6-groups-001/bao-phu-nhom.json#/original_groups_preserved','interpretation':'OBSERVATION_ONLY_PENDING_ROOT_READING; grouping flag alone is not cause','cross_case_limit':'matched preference, not controlled causal experiment; inspect missing_conditions'}
 group_rows.append(row)
interaction=[];identities=[];range0=[]
for oid,f in fact.items():
 co=f['contrasts']['interaction'];interaction.append({'opaque_id':oid,'defined':co['defined'],'m_nonzero_points':sum(v!=0 for v in co.get('signed_m_interaction',[])),'CP_nonzero_points':sum(v!=0 for v in co.get('signed_CP_flag_interaction',[])),'signed_CP_count_interaction':co.get('signed_CP_count_interaction'),'signed_first_CP_interaction':co.get('signed_first_CP_interaction'),'first_shift_defined':co.get('first_shift_defined'),'source':f['description_record']+'#/contrasts/interaction'})
 for pair,v in f['same_input_checks'].items():identities.append({'opaque_id':oid,'pair':pair,'same':v,'source':f['description_record']+'#/same_input_checks/'+pair})
 for branch,m in f['metadata']['branches'].items():range0.append({'opaque_id':oid,'branch':branch,'d':m['d'],'native_prior':m['native_prior'],'range0_columns':m['range0_columns'],'nonfinite_raw_prefix_cells':m['nonfinite_raw_prefix_cells'],'nonfinite_processed_cells':m['nonfinite_processed_cells'],'status':f['branches'][branch]['result']['status'],'source':f['description_record']+'#/metadata/branches/'+branch})
supp={'point_safety':dict(safety),'interaction_rows':interaction,'input_identical_rows':identities,'range0_rows':range0,'denominators':G['frozen_groups']['denominators'],'interaction_nonzero_m_cases':sum(v['m_nonzero_points']>0 for v in interaction),'interaction_nonzero_CP_cases':sum(v['CP_nonzero_points']>0 for v in interaction),'causal_limits':'CP flag and parent mass inspected, but theta not saved at every contrast; individual channel/prior cause remains OPEN where absent'}
assert len(allunits)==210 and len(group_rows)==64 and sum(len(v['points']) for v in allunits)==968
write('unit-dossiers.json',{'units':allunits,'root_manual_reading':'PENDING','no_detector_rerun':True})
write('display-units.json',{'units':display})
write('group-dossiers.json',{'groups':group_rows,'root_manual_reading':'PENDING','frozen_selection_preserved':True})
write('nsigma-same-column-controls.json',{'rows':pairs,'controls_from_original_full_gzip':True})
write('duration-at-locked-points.json',{'rows':durations,'unit':'OPEN_RAW_UNIT','not_own_time_or_external_load':True})
write('supplemental-stats.json',supp)
write('source-verification.json',{'status':'PASS','files':verified,'body_s':time.perf_counter()-_start,'detectors_reexecuted':False,'source_after':sha(H/'inputs/source.json')})
write('manifest.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()})
print(json.dumps({'status':'PASS','run':'session9-manual-001','units':210,'groups':64,'points':968,'point_safety':dict(safety),'interaction_nonzero_m_cases':supp['interaction_nonzero_m_cases'],'interaction_nonzero_CP_cases':supp['interaction_nonzero_CP_cases'],'files':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()}},ensure_ascii=False))
