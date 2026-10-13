"""EC2-only, read verified saved intermediates; lock points before extraction.

No detector/likelihood rerun, no parameter changes. Input contains inventories
already verified on the laptop. All source paths remain within T-033/dev.
"""
import os, sys, platform, shutil, hashlib, json, pathlib, time, math, gzip
import numpy as np
import pandas as pd
import scipy, psutil

assert os.name == 'posix' and platform.machine() == 'x86_64'
assert sys.version.startswith('3.12.3')
assert (np.__version__,pd.__version__,scipy.__version__)==('1.26.4','2.2.3','1.14.1')
assert INPUT.get('storage_extension_authorized') is True, 'DRAFT_NOT_AUTHORIZED'
assert INPUT.get('approved_storage_limit_bytes') == 5*2**30, 'DRAFT_NOT_AUTHORIZED'
STORAGE_LIMIT=INPUT['approved_storage_limit_bytes']
assert INPUT.get('run_name') in ('session7-manual-pilot-001','session7-manual-rest-001')
H=pathlib.Path('/home/ubuntu/rca/T-033'); OUT=H/'runs'/INPUT['run_name']
OUT.mkdir(exist_ok=False)
SOURCE_SHA='3071381a24edcfe82c1df19ffe4b816b2356a3afad1117fdae260f6c04f9079c'
verified={}
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''): h.update(chunk)
    return h.hexdigest()
def guard(additional=64*2**20):
    assert time.perf_counter()-_start < _ledger['remaining_approved_s'], 'BUDGET_STOP'
    assert not (H/'STOP').exists()
    used=sum(p.stat().st_size for p in H.rglob('*') if p.is_file())
    assert used+additional < STORAGE_LIMIT, 'STORAGE_STOP_BEFORE_WRITE'
    assert shutil.disk_usage(H).free > additional+8*2**20, 'DISK_STOP_BEFORE_WRITE'
    assert psutil.virtual_memory().percent <95, 'RAM_STOP'
def checked(rel):
    p=(H/rel).resolve(); assert p.is_relative_to(H)
    meta=INPUT['pins'][rel]
    if rel not in verified:
        assert p.stat().st_size==meta['bytes'] and sha(p)==meta['sha256'], rel
        verified[rel]=meta
    return p
def read(rel):return json.loads(checked(rel).read_text())
def clean(x):
    if isinstance(x,np.ndarray):return clean(x.tolist())
    if isinstance(x,np.generic):return clean(x.item())
    if isinstance(x,float) and not math.isfinite(x):return None
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x
def write(name,value):
    # Measure the exact serialized/compressed size before every output write.
    b=(json.dumps(clean(value),ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')
    if name.endswith('--points.json'):
        b=gzip.compress(b,compresslevel=6,mtime=0);name+='.gz'
    guard(len(b)+8*2**20)
    with (OUT/name).open('xb') as f:f.write(b)
    return name
def load(rel,keys=None):
    with np.load(checked(rel),allow_pickle=False) as z:
        return {k:z[k].copy() for k in (keys if keys is not None else z.files)}

assert sha(H/'inputs/source.json')==SOURCE_SHA
S=read('inputs/source.json'); CASES={c['opaque_id']:c for c in S['cases']}
G=read('runs/session6-groups-001/bao-phu-nhom.json')
M=read('inputs/session6-groups-001/source.json')
assert G['original_groups_preserved']==M['old_groups']
assert len(CASES)==30
units={}
for item in INPUT['locator']['core']:
    oid=item['opaque_id']; branch=item['branch']
    key=(oid,'bocpd' if branch in ('full','PP') else branch,branch if branch in ('full','PP') else 'full')
    units[key]={'record':item['record'],'npz':item['npz']}
for item in INPUT['locator']['factorial']:
    units[(item['opaque_id'],'bocpd',item['branch'])]={'record':item['record'],'npz':item['npz']}
for oid in CASES:
    # FF is the checked prefix of the complete native full. No replay.
    full=units[(oid,'bocpd','full')]
    units[(oid,'bocpd','FF')]=dict(full)
assert len(units)==210

factorial={}
for rel in M['factorial_records']:
    j=read(rel);factorial[j['opaque_id']]=(rel,j)
context={}
for run in ('channel-pilot-001','channel-rest-001'):
    for oid,m in read('runs/'+run+'/context-index.json')['records'].items():
        rel='runs/'+run+'/'+m['record'];context[oid]=(rel,read(rel))

# Verify case/control choice using the frozen rule, before reading scalar values.
labels={(r['opaque_id'],r['detector']):r for r in M['old_rows']}
def cv(oid):
    a=context[oid][1]['summary']['trace']['alignment']
    return ('logs.parquet' in CASES[oid]['files'],a['metric_seconds_with_observed_events'],a['on_metric_grid_rows'])
matching=read('runs/session7-manual-001/coverage-matching.json')
assert matching['status']=='PASS_FROZEN_CHOICE_AUDITED'
write('coverage-matching.json',matching)
locked=read('runs/session7-manual-001/points-lock.json')
assert locked['status']=='LOCKED_BEFORE_MANUAL_INTERPRETATION' and locked['unit_count']==210
locks=locked['units']
for lk in locks:
    assert lk['source']==units[(lk['opaque_id'],lk['detector'],lk['branch'])]
    lk['point_roles']={int(k):v for k,v in lk['point_roles'].items()}
write('points-lock.json',locked)

# Saved scalar extraction; native loop is never called.
point_evidence=[]; raw_inventory=json.loads((H/'runs/preflight-002/inventory.json').read_text())
raw_paths={x['opaque_id']:x['files']['metrics.parquet'] for x in raw_inventory['cases']}
fixed={(x['opaque_id'],x['detector']):x for x in INPUT['locator']['fixed']}
assert INPUT.get('selected_case_ids') and set(INPUT['selected_case_ids']) <= set(CASES)
for oid in sorted(INPUT['selected_case_ids']):
    guard();rawpath=pathlib.Path(raw_paths[oid]);rm=CASES[oid]['files']['metrics.parquet']
    assert str(rawpath)==str(pathlib.Path(S['source_roots_remote'][0])/rm['path'])
    assert rawpath.stat().st_size==rm['bytes'] and sha(rawpath)==rm['sha256']
    raw=pd.read_parquet(rawpath)
    context_rel,ctx=context[oid]; ctxnpz=str(pathlib.Path(context_rel).parent/ctx['output_npz'])
    cz=load(ctxnpz,[k for k in ctx['arrays'] if k.startswith(('metric_','trace_grid_','trace_global_grid_','log_grid_'))])
    casepoints=[]
    for lk in [x for x in locks if x['opaque_id']==oid]:
        det,branch=lk['detector'],lk['branch'];a=load(lk['source']['npz'])
        cols=a['columns'].tolist(); rows=[]
        fz=load(fixed[(oid,det)]['npz']) if det!='bocpd' else None
        for i in lk['indices']:
            r={'index':i,'time':int(a['times'][i]),'roles':lk['point_roles'][i],
                'raw_columns':cols,'raw_values':raw.iloc[i][cols].to_numpy(),
                'source_arrays_pointer':{'npz':lk['source']['npz'],'row':i},'source_sha256':INPUT['pins'][lk['source']['npz']]['sha256']}
            if det!='bocpd':
                r.update(columns=cols,x=a['x'][i],count=a['count'][i],mean=a['mean'][i],std=a['std'][i],
                    threshold=a['threshold'][i],margin=a['margin'][i],flags=a['Z'][i],
                    merged_flag=bool(a['Z'][i].any()),evaluated=bool(a['evaluated'][i]),
                    finite_statistics_mask=np.isfinite(a['mean'][i]) & np.isfinite(a['std'][i]),
                    fixed_source=fixed[(oid,det)]['npz'])
                # Baselines have shape(d); time-varying frozen arrays are POST
                # only, shape(721,d). Use the explicit saved index map.
                r['fixed_baseline']={k:fz[k] for k in ('mean_fixed','std_fixed','count_fixed','threshold_fixed')}
                postrow=np.flatnonzero(fz['post_indices']==i)
                assert np.array_equal(fz['columns'],a['columns']), 'Fixed/native column order drift'
                assert len(postrow)<=1, 'Duplicate fixed post index'
                if len(postrow):assert int(fz['times'][int(postrow[0])])==int(a['times'][i])
                r['fixed_comparison_status']='DEFINED_POST_GRID' if len(postrow) else 'NOT_APPLICABLE_PRE_PROXY'
                r['fixed_post_array_row']=int(postrow[0]) if len(postrow) else None
                r['fixed_arrays']={}
                for k in ('Z_fixed','margin_fixed','mean_updated_minus_fixed',
                          'threshold_updated_minus_fixed','finite_statistics_both','contrast_defined'):
                    assert fz[k].shape==(len(fz['post_indices']),len(cols)), (k,fz[k].shape)
                    if len(postrow):r['fixed_arrays'][k]=fz[k][int(postrow[0])]
            else:
                m=int(a['m'][i]);prev=int(a['m'][i-1]) if i else None;ru=int(a['runner_up'][i])
                pred=a['predictive_density'][i,:i+1];prior=a['R'][:i+1,i]
                r.update(columns=cols,X=a['X'][i],CP_flag=bool(a['CP_flags'][i]),m=m,previous_m=prev,
                    absolute_m_change=abs(m-prev) if prev is not None else None,runner_up=ru,
                    MAP_posterior=float(a['R'][m,i+1]),runner_posterior=float(a['R'][ru,i+1]),
                    normalizer=float(a['normalizer'][i]),reset_mass=float(a['reset_mass'][i]),
                    reset_posterior=float(a['R'][0,i+1]),constant_hazard=0.02,
                    MAP_growth_parent=m-1 if m else None,runner_growth_parent=ru-1 if ru else None,
                    MAP_parent_predictive_density=float(pred[m-1]) if m else None,
                    MAP_parent_prior_posterior=float(prior[m-1]) if m else None,
                    MAP_growth_mass=float(prior[m-1]*pred[m-1]*0.98) if m else None,
                    runner_parent_predictive_density=float(pred[ru-1]) if ru else None,
                    runner_parent_prior_posterior=float(prior[ru-1]) if ru else None,
                    runner_growth_mass=float(prior[ru-1]*pred[ru-1]*0.98) if ru else None)
                theta=np.flatnonzero(a['theta_points']==i)
                r['theta_available']=bool(len(theta))
                if len(theta):
                    q=int(theta[0]);r['theta_source_row']=q;r['theta_parent_indices']=a['theta_parent_indices'][q]
                    r['theta']={k:v[q] for k,v in a.items() if k.startswith(('theta_before_','theta_after_'))}
                r['posterior_pointer']={'array':'R','column':i+1,'support_rows':[0,i+1]}
                r['predictive_pointer']={'array':'predictive_density','row':i,'parent_columns':[0,i]}
                r['native_prior']={'d':len(cols),'dof':len(cols)+1,'kappa':1,'mu':[0]*len(cols),'scale':'identity'}
            r['context']={'record':context_rel,'npz':ctxnpz,'array_row':i,
                'workload_columns':ctx['summary']['metric']['columns'],
                'trace_entities':ctx['summary']['trace']['entities'],
                'log_entities':ctx['summary']['log'].get('entities'),
                'collector_completeness':'OPEN','duration_physical_unit':'OPEN',
                'log_status':ctx['summary']['log']['status'],
                'saved_arrays':{k:v[i] for k,v in cz.items() if v.ndim>=1 and len(v)==1441}}
            rows.append(r)
        casepoints.append({'opaque_id':oid,'detector':det,'branch':branch,'points':rows,
            'native_status':read(lk['source']['record']).get('result',{}).get('status','OK'),
            'observation_only':True,'manual_interpretation':'OPEN'})
    filename=write(oid+'--points.json',{'opaque_id':oid,'units':casepoints})
    point_evidence.append({'opaque_id':oid,'file':filename,'unit_count':len(casepoints)})
    print('EXTRACTED '+oid, file=sys.stderr,flush=True)
    del raw,cz
write('point-index.json',{'status':'PASS_SAVED_VALUES_EXTRACTED','cases':point_evidence,
    'locked_units':len(locks),'extracted_units':sum(x['unit_count'] for x in point_evidence),'manual_interpretation':'OPEN','detectors_reexecuted':False})
write('source-verification.json',{'status':'PASS','sources':verified,'raw_metrics':[
    {'opaque_id':oid,'sha256':CASES[oid]['files']['metrics.parquet']['sha256']} for oid in INPUT['selected_case_ids']],
    'source_after_sha256':sha(H/'inputs/source.json'),'normalization_recomputed':'Not rerun; saved operands extracted',
    'resources':{'logical_bytes':sum(p.stat().st_size for p in H.rglob('*') if p.is_file()),
                 'ram_available_bytes':psutil.virtual_memory().available},'manual_interpretation':'OPEN'})
write('manifest.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()})
print(json.dumps({'status':'PASS','run':'runs/'+INPUT['run_name'],'locked_units':len(locks),'extracted_units':sum(x['unit_count'] for x in point_evidence),
    'files':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()}}))
