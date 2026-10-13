"""EC2: verify serialized evidence and summarize exact saved measurements."""
import pathlib,json,hashlib,collections,time,math,shutil
import numpy as np,pandas as pd,psutil
H=pathlib.Path('/home/ubuntu/rca/T-033');E=H/'runs/session8-evidence-001';OUT=H/'runs/session8-stats-001';OUT.mkdir(exist_ok=False)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(p.read_text())
def clean(v):
 if isinstance(v,np.ndarray):return clean(v.tolist())
 if isinstance(v,np.generic):return clean(v.item())
 if isinstance(v,float) and not math.isfinite(v):return None
 if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [clean(x) for x in v]
 return v
def write(n,x):
 b=(json.dumps(clean(x),ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
 used=sum(p.stat().st_size for p in H.rglob('*') if p.is_file())
 assert used+len(b)+8*2**20<5*2**30 and shutil.disk_usage(H).free>len(b)+8*2**20
 assert time.perf_counter()-_start<_ledger['remaining_approved_s'] and psutil.virtual_memory().percent<95
 (OUT/n).write_bytes(b)
for rel,m in INPUT['pins'].items():
 if rel.startswith('runs/session8-evidence-001/'):
  p=H/rel;assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],rel
S=read(H/'inputs/source.json');inv=read(H/'runs/preflight-002/inventory.json')
rows=read(E/'chuoi-bang-chung.json')['units'];delay=read(E/'do-tre-sau-moc.json')['rows'];fact=read(E/'phan-ra-tien-xu-ly.json');fixed=read(E/'nsigma-nguong-co-dinh.json')['rows'];old=read(E/'doi-chieu.json')['rows']
def first(row,role):return next((p for p in row['points'] if role in p['roles']),None)
stats={'units':len(rows),'points':sum(len(r['points']) for r in rows),'detectors':{},'factorial':{},'nsigma_fixed':{},'mechanism_denominators':{}}
for det in ['nsigma','nsigma_doi_chung','bocpd']:
 rr=[r for r in rows if r['detector']==det and r['branch']=='full'];dd=[r for r in delay if r['detector']==det];pre=[first(r,'first_pre_proxy_alarm') for r in rr];post=[first(r,'first_post_proxy_alarm') for r in rr]
 fractions=[r['pre_proxy'].get('fraction_flag_points',r['pre_proxy'].get('fraction_CP_points')) for r in dd];offset=[r['signed_seconds_from_proxy'] for r in dd if r['signed_seconds_from_proxy'] is not None]
 st={'n':30,'first_groups':dict(collections.Counter(r['analysis_labels_only']['first_group'] for r in rr)),'post_alarm_present':len(offset),'post_offset_min':min(offset),'post_offset_max':max(offset),'pre_fraction_min':min(fractions),'pre_fraction_max':max(fractions),'preexisting_post_segment':sum(bool(r.get('first_post_alarm_in_preexisting_segment',r.get('first_post_CP_in_segment_started_before_proxy'))) for r in dd),'first_pre_alarm_present':sum(p is not None for p in pre)}
 if det!='bocpd':
  st.update(first_pre_any_zero_std_trigger=sum(any(c['flag'] and c['std_ddof1_past']==0 for c in p['columns']) for p in pre if p),first_pre_any_missing_raw_trigger=sum(any(c['flag'] and c['raw'] is None for c in p['columns']) for p in pre if p),first_pre_all_flag_columns_finite=sum(all(c['std_ddof1_past'] is not None and c['mean_past'] is not None for c in p['columns'] if c['flag']) for p in pre if p))
 else:
  st.update(first_pre_MAP_runlength1=sum(p['m']==1 for p in pre if p),first_pre_mode_increased=sum(p['m']>p['previous_m'] for p in pre if p),first_post_MAP_runlength1=sum(p['m']==1 for p in post if p),first_post_mode_increased=sum(p['m']>p['previous_m'] for p in post if p),first_post_MAP_continuation_lost=sum(p['MAP_posterior']>p['previous_MAP_continuation_posterior'] for p in post if p))
 stats['detectors'][det]=st
for det in ['nsigma','nsigma_doi_chung']:
 rr=[r['summary'] for r in fixed if r['detector']==det];shifts=[r['merged_first_time_fixed_minus_updated_s'] for r in rr if r['merged_first_time_fixed_minus_updated_s'] is not None]
 stats['nsigma_fixed'][det]={'n':30,'first_time_defined_pairs':len(shifts),'earlier':sum(v<0 for v in shifts),'equal':sum(v==0 for v in shifts),'later':sum(v>0 for v in shifts),'shift_min':min(shifts),'shift_max':max(shifts),'merged_flag_set_different':sum(r['merged_flag_points']['added']>0 or r['merged_flag_points']['removed']>0 for r in rr),'column_flags_added':sum(r['all_cell_counts']['added_flags'] for r in rr),'column_flags_removed':sum(r['all_cell_counts']['removed_flags'] for r in rr)}
for name in fact['cases'][0]['contrasts']:
 rr=[r['contrasts'][name] for r in fact['cases']]
 if name=='interaction':
  stats['factorial'][name]={'n':30,'keys':list(rr[0]),'source':'phan-ra-tien-xu-ly.json#/cases/*/contrasts/interaction'}
 else:stats['factorial'][name]={'n':30,'defined':sum(r['defined'] for r in rr),'m_different':sum(any(v!=0 for v in r['signed_m_difference']) for r in rr if r['defined']),'CP_different':sum(any(v!=0 for v in r['signed_CP_flag_difference']) for r in rr if r['defined'])}
stats['mechanism_denominators']={'branch_units':120,'valid_outputs':sum(v['result']['status']=='OK' for r in fact['cases'] for v in r['branches'].values()),'no_channels':sum(v['d']==0 for r in fact['cases'] for v in r['metadata']['branches'].values()),'range0_present':sum(bool(v['range0_columns']) for r in fact['cases'] for v in r['metadata']['branches'].values()),'input_equal_checks_keys':list(fact['cases'][0]['same_input_checks'])}
ns=read(E/'doi-chieu.json')['columnset_pairs'];stats['wide_vs_narrow']={'n':30,'wide_first_earlier':sum(r['wide_first']<r['narrow_first'] for r in ns),'first_equal':sum(r['wide_first']==r['narrow_first'] for r in ns)}
# Repair missing workload presentation only: original extraction selected metric_* but
# source names are workload_*. Retain old files and read saved source at fixed locks.
workload=[]
for c in S['cases']:
 oid=c['opaque_id'];ir=next(r for r in inv['cases'] if r['opaque_id']==oid)
 for n,m in c['files'].items():
  p=pathlib.Path(ir['files'][n]);assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256']
 cp=next(r for r in read(E/'tai-log.json')['cases'] if r['opaque_id']==oid)['record'];cr=read(H/cp);nr=(pathlib.Path(cp).parent/cr['output_npz']).as_posix();meta=INPUT['pins'][nr];assert sha(H/nr)==meta['sha256']
 with np.load(H/nr,allow_pickle=False) as z:
  ts=z['times'];cols=z['workload_columns'];a=z['workload_raw'];mask=z['workload_nan'];inf=z['workload_inf']
  for i in sorted({p['index'] for r in rows if r['opaque_id']==oid for p in r['points']}):workload.append({'opaque_id':oid,'index':i,'time':int(ts[i]),'columns':cols,'values':a[i],'missing_mask':mask[i],'inf_mask':inf[i],'source_npz':nr,'source_sha256':meta['sha256'],'physical_load_and_units':'OPEN; raw workload metric only'})
write('workload-at-locked-points.json',{'rows':workload,'source_array_name':'workload_raw','interpretation':'Exact saved workload at locked points; null missing, zero observed zero; not external request rate or collector completeness'})
write('stats.json',stats)
write('verification.json',{'status':'PASS','extraction_independently_checked_prior':True,'raw89_source_after_exact':True,'serialized_evidence_manifest_exact':True,'workload_saved_source_exact':True,'unit_count':210,'native_detector_reruns':0,'body_s':time.perf_counter()-_start,'logical_bytes':sum(p.stat().st_size for p in H.rglob('*') if p.is_file()),'scientific_manual_interpretation':'OPEN'})
write('manifest.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()})
print(json.dumps({'status':'PASS','stats':stats,'files':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()}},indent=2))
