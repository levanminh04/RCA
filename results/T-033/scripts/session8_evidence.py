"""EC2 saved-evidence synthesis, no detector replay or parameter changes."""
import pathlib,json,gzip,hashlib,math,time,shutil,collections
import numpy as np,pandas as pd,psutil
H=pathlib.Path('/home/ubuntu/rca/T-033');OUT=H/'runs/session8-evidence-001';OUT.mkdir(exist_ok=False)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def clean(v):
 if isinstance(v,np.ndarray):return clean(v.tolist())
 if isinstance(v,np.generic):return clean(v.item())
 if isinstance(v,float) and not math.isfinite(v):return None
 if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [clean(x) for x in v]
 return v
verified={}
def checked(rel):
 p=(H/rel).resolve();assert p.is_relative_to(H)
 if rel not in verified:
  m=INPUT['pins'][rel];assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],rel;verified[rel]=m
 return p
def read(rel):return json.loads(checked(rel).read_text())
def load(rel,keys=None):
 with np.load(checked(rel),allow_pickle=False) as z:return {k:z[k].copy() for k in (keys or z.files)}
def write(name,x):
 b=(json.dumps(clean(x),ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode()
 used=sum(p.stat().st_size for p in H.rglob('*') if p.is_file())
 assert used+len(b)+8*2**20<5*2**30 and shutil.disk_usage(H).free>len(b)+8*2**20
 assert time.perf_counter()-_start<_ledger['remaining_approved_s'] and psutil.virtual_memory().percent<95
 (OUT/name).write_bytes(b)
S=read('inputs/source.json');cases={c['opaque_id']:c for c in S['cases']}
G=read('runs/session6-groups-001/bao-phu-nhom.json');M=read('inputs/session6-groups-001/source.json')
labels={(r['opaque_id'],r['detector']):r for r in M['old_rows']}
points={};extraction={}
for n in ['session7-manual-pilot-001','session7-manual-rest-001']:
 idx=read('runs/'+n+'/point-index.json')
 for item in idx['cases']:
  oid=item['opaque_id'];rel='runs/'+n+'/'+item['file'];points[oid]=json.loads(gzip.decompress(checked(rel).read_bytes()));extraction[oid]=rel
assert len(points)==30
delay=[]
for rel in INPUT['pins']:
 if rel.endswith('/delay.json') and any('/'+v+'/' in rel for v in ['nsigma-delay-pilot-001','nsigma-delay-rest-001','bocpd-delay-pilot-001','bocpd-delay-rest-001']):
  for row in read(rel)['rows']:delay.append(dict(row,description_record=rel))
assert len(delay)==90
dmap={(r['opaque_id'],r['detector']):r for r in delay}
factorial=[dict(read(rel),description_record=rel) for rel in M['factorial_records']];assert len(factorial)==30
fmap={v['opaque_id']:v for v in factorial}
fixed=[dict(read(v['record']),description_record=v['record']) for v in INPUT['locator']['fixed']];assert len(fixed)==60
fxmap={(v['opaque_id'],v['detector']):v for v in fixed}
unit_rows=[];context_rows=[];ns_pairs=[];contrasts=[];log_excerpts=[]
for oid in sorted(cases):
 body=points[oid];assert len(body['units'])==7
 ctxrel='runs/channel-'+('pilot' if oid=='dev-03d4910932' else 'rest')+'-001/'+oid+'--context.json';ctx=read(ctxrel)
 inv=json.loads((H/'runs/preflight-002/inventory.json').read_text());iv=next(v for v in inv['cases'] if v['opaque_id']==oid)
 rawp=pathlib.Path(iv['files']['metrics.parquet']);raw=pd.read_parquet(rawp)
 bas=raw.drop(columns=['time']).ffill().fillna(0)
 # Log excerpts keep exact row/message and digest; deterministic first+last per locked second.
 if 'logs.parquet' in cases[oid]['files']:
  lp=pathlib.Path(iv['files']['logs.parquet']);lm=cases[oid]['files']['logs.parquet'];assert sha(lp)==lm['sha256']
  logs=pd.read_parquet(lp);secs=pd.to_numeric(logs['timestamp'],errors='raise')
  for i in sorted({p['index'] for u in body['units'] for p in u['points']}):
   ii=np.flatnonzero((secs==int(raw['time'].iloc[i])).to_numpy());selected=sorted(set([int(ii[0]),int(ii[-1])])) if len(ii) else []
   samples=[]
   for q in selected:
    row=logs.iloc[q];msg=row['message'];present=not pd.isna(msg)
    samples.append({'original_row':q,'container':None if pd.isna(row['container_name']) else row['container_name'],'message':msg if present else None,'message_sha256':hashlib.sha256(msg.encode('utf-8')).hexdigest() if present else None})
   log_excerpts.append({'opaque_id':oid,'index':i,'time':int(raw['time'].iloc[i]),'observed_rows_at_exact_second':len(ii),'selected_rows_rule':'first and last original row at locked second; not chosen by content','source_log_sha256':lm['sha256'],'samples':samples,'event_causality':'OPEN'})
  del logs
 else:log_excerpts.append({'opaque_id':oid,'status':'N/A_MISSING_CHANNEL','absence_not_zero':True})
 context_rows.append({'opaque_id':oid,'record':ctxrel,'summary':ctx['summary'],'point_source':extraction[oid],'log_text_pointer':'tai-log.json#/log_excerpts','physical_cause':'OPEN','collector_completeness':'OPEN'})
 bo={}
 for u in body['units']:
  det,branch=u['detector'],u['branch'];row={'opaque_id':oid,'detector':det,'branch':branch,'point_source':extraction[oid],'source_unit_pointer':{'detector':det,'branch':branch},'native_status':u['native_status'],'points':[],'physical_onset':'OPEN'}
  if det=='bocpd':
   rel=u['points'][0]['source_arrays_pointer']['npz'];a=load(rel,['X','m','R','predictive_density','columns','times']);bo[branch]=a
  for p in u['points']:
   i=p['index'];v={'index':i,'roles':p['roles'],'time':p['time'],'source_pointer':p['source_arrays_pointer']}
   if det!='bocpd':
    ids=[j for j,f in enumerate(p['flags']) if f];finite=[j for j,m in enumerate(p['margin']) if m is not None]
    ranked=sorted(finite,key=lambda j:(-p['margin'][j],p['columns'][j]))
    inspected=sorted(set(ids+ranked[:1]))
    v.update(flag=p['merged_flag'],evaluated=p['evaluated'],trigger_count=len(ids),nonfinite_statistics_columns=[c for c,m in zip(p['columns'],p['finite_statistics_mask']) if not m],fixed_status=p['fixed_comparison_status'],columns=[])
    for j in inspected:
     col={'column':p['columns'][j],'raw':p['raw_values'][j],'x_after_Inf_NaN_ffill':p['x'][j],'n':p['count'][j],'mean_past':p['mean'][j],'std_ddof1_past':p['std'][j],'threshold_3sd':p['threshold'][j],'margin':p['margin'][j],'flag':p['flags'][j],'fixed_mean':p['fixed_baseline']['mean_fixed'][j],'fixed_std':p['fixed_baseline']['std_fixed'][j]}
     if p['fixed_arrays']:col.update({k:p['fixed_arrays'][k][j] for k in p['fixed_arrays']})
     v['columns'].append(col)
   else:
    old=p['previous_m'];parent=old if old is not None else 0;continued=parent+1
    cmass=a['R'][parent,i]*a['predictive_density'][i,parent]*0.98
    v.update({k:p[k] for k in ['CP_flag','m','previous_m','runner_up','MAP_posterior','runner_posterior','normalizer','reset_posterior','MAP_growth_mass','runner_growth_mass','MAP_parent_predictive_density','MAP_parent_prior_posterior','theta_available']})
    v.update(d=len(p['columns']),previous_MAP_growth_parent=parent,previous_MAP_continuation_mass=cmass,previous_MAP_continuation_posterior=a['R'][continued,i+1],absolute_m_change=p['absolute_m_change'])
    # Retain raw/fill/scale for every channel, not only a root-linked channel.
    meta=fmap[oid]['metadata']['branches']['FF' if branch=='full' else branch]
    v['input_channels']=[{'column':c,'raw':p['raw_values'][j],'after_fill':bas[c].iloc[i],'X':p['X'][j],'minmax':meta['minmax_after_native_fill'][c]} for j,c in enumerate(p['columns'])]
   row['points'].append(v)
  if det!='bocpd':row['fixed_summary']={k:v for k,v in fxmap[(oid,det)]['summary'].items() if k!='columns'}
  row['delay']=dmap[(oid,det)] if branch=='full' else None
  # Attach analysis labels after scalar descriptions; they were not detector inputs.
  row['analysis_labels_only']=labels[(oid,det)];unit_rows.append(row)
 narrow=next(v for v in body['units'] if v['detector']=='nsigma');wide=next(v for v in body['units'] if v['detector']=='nsigma_doi_chung')
 ns_pairs.append({'opaque_id':oid,'narrow_first':dmap[(oid,'nsigma')]['first_alarm_index'],'wide_first':dmap[(oid,'nsigma_doi_chung')]['first_alarm_index'],'same_common_column_statistics':'Verified native independent-column contract; old raw/core checks exact','source_points':extraction[oid]})
 for name,c in fmap[oid]['contrasts'].items():
  if name=='interaction':continue
  if not c.get('defined'):contrasts.append({'opaque_id':oid,'contrast':name,'defined':False});continue
  ia=np.flatnonzero(np.array(c['signed_m_difference'])!=0);ic=np.flatnonzero(np.array(c['signed_CP_flag_difference'])!=0)
  pair={'scale_with_M_F':('FF','FP'),'scale_with_M_P':('PF','PP'),'mask_d_prior_with_S_F':('FF','PF'),'mask_d_prior_with_S_P':('FP','PP'),'total_full_preprocessing_vs_prefix':('FF','PP')}[name]
  q=int(ia[0]) if len(ia) else None;rawdiff=[]
  if q is not None:
   aa,bb=bo[pair[0]],bo[pair[1]];common=sorted(set(aa['columns'])&set(bb['columns']))
   for col in common:
    ja=aa['columns'].tolist().index(col);jb=bb['columns'].tolist().index(col);xa=aa['X'][q,ja];xb=bb['X'][q,jb]
    if xa!=xb:rawdiff.append({'column':col,'raw':raw[col].iloc[q],'after_fill':bas[col].iloc[q],'X_a':xa,'X_b':xb,'scale_a':fmap[oid]['metadata']['branches'][pair[0]]['minmax_after_native_fill'][col],'scale_b':fmap[oid]['metadata']['branches'][pair[1]]['minmax_after_native_fill'][col]})
  contrasts.append({'opaque_id':oid,'contrast':name,'pair':pair,'defined':True,'first_m_difference':q,'first_CP_difference':int(ic[0]) if len(ic) else None,'m_difference_points':len(ia),'CP_difference_points':len(ic),'first_m_input_differences':rawdiff,'first_m_states':{b:{'d':len(bo[b]['columns']),'m':int(bo[b]['m'][q]),'MAP_posterior':float(bo[b]['R'][int(bo[b]['m'][q]),q+1]),'reset_posterior':float(bo[b]['R'][0,q+1])} for b in pair} if q is not None else None,'factorial_source':fmap[oid]['description_record']})
 del bo,raw,bas
 print('EVIDENCE '+oid,flush=True)
write('chuoi-bang-chung.json',{'status':'SAVED_OBSERVATIONS_WITH_SCALAR_CHAINS','units':unit_rows,'unit_count':len(unit_rows),'manual_interpretation':'OPEN','not_an_operational_onset_label':True})
write('phan-ra-tien-xu-ly.json',{'cases':factorial,'contrast_chains':contrasts,'group_denominators':G['separate_denominators'] if 'separate_denominators' in G else G.get('denominators'),'interpretation':'Scale within fixed mask; mask/d/prior bundle; both paths and interaction preserved; no causal detector selected'})
write('do-tre-sau-moc.json',{'rows':delay,'units':90,'proxy_not_onset':True})
write('nsigma-nguong-co-dinh.json',{'rows':fixed,'units':60,'contrast':'Joint effect of updating mean and std; not separate std effect, not clean baseline'})
write('doi-chieu.json',{'rows':M['old_rows'],'columnset_pairs':ns_pairs,'units':90,'labels_attached_after_descriptors':True})
write('tai-log.json',{'cases':context_rows,'log_excerpts':log_excerpts,'physical_cause':'OPEN','channels_not_independent':True})
write('bao-phu-nhom.json',{'frozen_groups':G,'matching':read('runs/session7-manual-001/coverage-matching.json'),'point_lock':read('runs/session7-manual-001/points-lock.json'),'all_units':[{k:r[k] for k in ['opaque_id','detector','branch','point_source']} for r in unit_rows],'manual_interpretation':'OPEN'})
summary={}
for det in ['nsigma','nsigma_doi_chung','bocpd']:
 rr=[r for r in delay if r['detector']==det];valid=[r for r in rr if r.get('signed_seconds_from_proxy') is not None]
 summary[det]={'cases':len(rr),'no_post':sum(r['no_post_alarm_to_end'] for r in rr),'post_offsets':[r['signed_seconds_from_proxy'] for r in valid],'pre_fraction':[r['pre_proxy'].get('fraction_flag_points',r['pre_proxy'].get('fraction_CP_points')) for r in rr],'preexisting_post_segment':sum(bool(r.get('first_post_alarm_in_preexisting_segment',r.get('first_post_CP_in_segment_started_before_proxy'))) for r in rr),'first_groups':dict(collections.Counter(labels[(r['opaque_id'],det)]['first_group'] for r in rr))}
write('digest.json',{'detector_summary':summary,'unit_count':210,'point_count':sum(len(r['points']) for r in unit_rows),'nsigma_pairs':ns_pairs,'contrast_chains':[{k:v for k,v in r.items() if k not in ['first_m_input_differences']} for r in contrasts],'sources_verified':len(verified),'manual_interpretation':'OPEN'})
write('source-verification.json',{'status':'PASS','files':verified,'source_after_sha256':sha(H/'inputs/source.json'),'logical_bytes':sum(p.stat().st_size for p in H.rglob('*') if p.is_file()),'body_s':time.perf_counter()-_start,'detectors_reexecuted':False})
write('manifest.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()})
print(json.dumps({'status':'PASS','run':'session8-evidence-001','unit_count':210,'files':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()},'manual_interpretation':'OPEN'}))
