"""EC2 read-only independent saved-source scalar/readback verification."""
import pathlib,json,gzip,hashlib,time,math,shutil,subprocess
import numpy as np,pandas as pd,psutil
H=pathlib.Path('/home/ubuntu/rca/T-033');run=H/'runs'/INPUT['run_name']
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def clean(x):
 if isinstance(x,np.ndarray):return clean(x.tolist())
 if isinstance(x,np.generic):return clean(x.item())
 if isinstance(x,float) and not math.isfinite(x):return None
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
def eq(got,x,label):assert got==clean(x),label
verified={}
def checked(rel):
 p=(H/rel).resolve();assert p.is_relative_to(H)
 if rel not in verified:
  m=INPUT['pins'][rel];assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],rel
  verified[rel]=m
 return p
def load(rel):
 with np.load(checked(rel),allow_pickle=False) as z:return {k:z[k].copy() for k in z.files}
S=json.loads(checked('inputs/source.json').read_text());cases={v['opaque_id']:v for v in S['cases']}
inv=json.loads((H/'runs/preflight-002/inventory.json').read_text())
rawpaths={v['opaque_id']:v['files']['metrics.parquet'] for v in inv['cases']}
lock=json.loads(checked('runs/session7-manual-001/points-lock.json').read_text())
outlock=json.loads((run/'points-lock.json').read_text());assert outlock==lock
assert json.loads((run/'coverage-matching.json').read_text())==json.loads(checked('runs/session7-manual-001/coverage-matching.json').read_text())
index=json.loads((run/'point-index.json').read_text())
assert index['status']=='PASS_SAVED_VALUES_EXTRACTED' and index['detectors_reexecuted'] is False
assert {v['opaque_id'] for v in index['cases']}==set(INPUT['selected_case_ids'])
fixed={(v['opaque_id'],v['detector']):v['npz'] for v in INPUT['locator']['fixed']}
mf=json.loads((run/'manifest.json').read_text())
for name,m in mf.items():assert (run/name).stat().st_size==m['bytes'] and sha(run/name)==m['sha256']
counts={'units':0,'points':0,'fixed_pre':0,'fixed_post':0,'theta_present':0,'theta_absent':0,'finite_cells':0,'nonfinite_cells':0}
percase=[]
for case in index['cases']:
 assert time.perf_counter()-_start<_ledger['remaining_approved_s']
 oid=case['opaque_id'];p=run/case['file'];body=json.loads(gzip.decompress(p.read_bytes()))
 assert body['opaque_id']==oid and len(body['units'])==7
 rm=cases[oid]['files']['metrics.parquet'];rp=pathlib.Path(rawpaths[oid]);assert rp.stat().st_size==rm['bytes'] and sha(rp)==rm['sha256']
 raw=pd.read_parquet(rp);casepoints=0
 for unit in body['units']:
  det,branch=unit['detector'],unit['branch'];lk=next(v for v in lock['units'] if (v['opaque_id'],v['detector'],v['branch'])==(oid,det,branch))
  a=load(lk['source']['npz']);cols=a['columns'].tolist();assert np.array_equal(a['times'],raw['time'].to_numpy()[:len(a['times'])])
  assert [r['index'] for r in unit['points']]==lk['indices']
  if branch=='FF':assert all(r['index']<720 for r in unit['points'])
  fz=load(fixed[(oid,det)]) if det!='bocpd' else None
  if fz is not None:
   assert np.array_equal(fz['post_indices'],np.arange(720,len(a['times'])))
   assert len(set(fz['post_indices'].tolist()))==len(fz['post_indices'])
  for r in unit['points']:
   i=r['index'];counts['points']+=1;casepoints+=1
   eq(r['time'],int(a['times'][i]),'time');eq(r['roles'],lk['point_roles'][str(i)],'roles')
   eq(r['raw_values'],raw.iloc[i][cols].to_numpy(),'raw_values');eq(r['raw_columns'],cols,'raw_columns')
   eq(r['source_sha256'],INPUT['pins'][lk['source']['npz']]['sha256'],'pin')
   if det!='bocpd':
    for k,ak in [('x','x'),('count','count'),('mean','mean'),('std','std'),('threshold','threshold'),('margin','margin'),('flags','Z')]:eq(r[k],a[ak][i],k)
    eq(r['merged_flag'],bool(a['Z'][i].any()),'merged');eq(r['evaluated'],bool(a['evaluated'][i]),'evaluated')
    eq(r['finite_statistics_mask'],np.isfinite(a['mean'][i])&np.isfinite(a['std'][i]),'finite_mask')
    assert np.array_equal(a['Z'][i],(np.abs(a['x'][i]-a['mean'][i])>3*a['std'][i])&a['evaluated'][i])
    counts['finite_cells']+=int(np.isfinite(a['mean'][i]).sum());counts['nonfinite_cells']+=int((~np.isfinite(a['mean'][i])).sum())
    for k in ['mean_fixed','std_fixed','count_fixed','threshold_fixed']:assert fz[k].shape==(len(cols),);eq(r['fixed_baseline'][k],fz[k],k)
    if i<720:
     assert r['fixed_post_array_row'] is None and r['fixed_arrays']=={} and r['fixed_comparison_status']=='NOT_APPLICABLE_PRE_PROXY';counts['fixed_pre']+=1
    else:
     q=i-720;assert r['fixed_post_array_row']==q and r['fixed_comparison_status']=='DEFINED_POST_GRID';counts['fixed_post']+=1
     assert fz['times'][q]==a['times'][i]
     for k in ['Z_fixed','margin_fixed','mean_updated_minus_fixed','threshold_updated_minus_fixed','finite_statistics_both','contrast_defined']:
      assert fz[k].shape==(len(fz['post_indices']),len(cols));eq(r['fixed_arrays'][k],fz[k][q],k)
   else:
    m=int(a['m'][i]);ru=int(a['runner_up'][i]);prev=int(a['m'][i-1]) if i else None
    for k,v in [('X',a['X'][i]),('m',m),('previous_m',prev),('runner_up',ru),('CP_flag',bool(a['CP_flags'][i])),('MAP_posterior',a['R'][m,i+1]),('runner_posterior',a['R'][ru,i+1]),('normalizer',a['normalizer'][i]),('reset_mass',a['reset_mass'][i]),('reset_posterior',a['R'][0,i+1])]:eq(r[k],v,k)
    if prev is not None:assert r['CP_flag']==(abs(m-prev)>1)
    for prefix,parent in [('MAP',m-1 if m else None),('runner',ru-1 if ru else None)]:
     for suffix,v in [('parent_predictive_density',a['predictive_density'][i,parent] if parent is not None else None),('parent_prior_posterior',a['R'][parent,i] if parent is not None else None),('growth_mass',a['R'][parent,i]*a['predictive_density'][i,parent]*0.98 if parent is not None else None)]:eq(r[prefix+'_'+suffix],v,prefix+suffix)
    q=np.flatnonzero(a['theta_points']==i);eq(r['theta_available'],bool(len(q)),'theta_available')
    if len(q):
     counts['theta_present']+=1;q=int(q[0]);eq(r['theta_parent_indices'],a['theta_parent_indices'][q],'theta_parents')
     for k in r['theta']:eq(r['theta'][k],a[k][q],k)
    else:counts['theta_absent']+=1
   ctx=load(r['context']['npz'])
   for k,v in r['context']['saved_arrays'].items():eq(v,ctx[k][i],k)
  counts['units']+=1
 percase.append({'opaque_id':oid,'units':7,'points':casepoints,'gzip_bytes':p.stat().st_size,'sha256':sha(p),'status':'PASS_EXACT_SOURCE_SCALARS'})
assert counts['units']==7*len(INPUT['selected_case_ids'])
after=json.loads((run/'source-verification.json').read_text());assert after['source_after_sha256']==sha(H/'inputs/source.json')==INPUT['pins']['inputs/source.json']['sha256']
used=sum(p.stat().st_size for p in H.rglob('*') if p.is_file());assert used<5*2**30
print(json.dumps({'status':'PASS','run':INPUT['run_name'],'counts':counts,'cases':percase,'checks':['gzip_readback','manifest_exact_bytes_hash','raw_native_time_columns','fixed_post_indices_unique_projection','finite_null_masks_exact','N-Sigma_flags_scalar','BOCPD_MAP_predictive_prior_theta_CP','context_rows','locks_roles_unchanged','source_after_pin','storage_under_5GiB'],'logical_bytes':used,'disk_free_bytes':shutil.disk_usage(H).free,'ram_available_bytes':psutil.virtual_memory().available,'body_s':time.perf_counter()-_start,'detectors_reexecuted':False},indent=2))
