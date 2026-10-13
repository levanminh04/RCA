"""EC2-only, read verified saved intermediates; lock points before extraction.

No detector/likelihood rerun, no parameter changes. Input contains inventories
already verified on the laptop. All source paths remain within T-033/dev.
"""
import os, sys, platform, shutil, hashlib, json, pathlib, time, math
import numpy as np
import pandas as pd
import scipy, psutil

assert os.name == 'posix' and platform.machine() == 'x86_64'
assert sys.version.startswith('3.12.3')
assert (np.__version__,pd.__version__,scipy.__version__)==('1.26.4','2.2.3','1.14.1')
H=pathlib.Path('/home/ubuntu/rca/T-033'); OUT=H/'runs/session7-manual-001'
OUT.mkdir(exist_ok=False)
SOURCE_SHA='3071381a24edcfe82c1df19ffe4b816b2356a3afad1117fdae260f6c04f9079c'
verified={}
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''): h.update(chunk)
    return h.hexdigest()
def guard():
    assert time.perf_counter()-_start < _ledger['remaining_approved_s'], 'BUDGET_STOP'
    assert not (H/'STOP').exists()
    used=sum(p.stat().st_size for p in H.rglob('*') if p.is_file())
    assert used+64*2**20 < 4*2**30, 'STORAGE_STOP'
    assert shutil.disk_usage(H).free > 64*2**20, 'DISK_STOP'
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
    with (OUT/name).open('x',encoding='utf-8') as f:
        json.dump(clean(value),f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
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
matching=[]
for old in (True,False):
    groups=G['original_groups_preserved']['groups'] if old else G['new_groups']
    for g in groups:
        rep=g['representative'] if old else g['representative']['opaque_id']
        det=g['detector'] if old else 'bocpd'
        members=g['all_members'] if old else [x['opaque_id'] for x in g['members']]
        assert rep==min(members)
        candidates=[x for x in CASES if x not in members]
        lr=labels[(rep,det)]; d=lr.get('d') or 0
        if old:
            candidates.sort(key=lambda x:(labels[(x,det)]['cell']!=lr['cell'],abs((labels[(x,det)].get('d') or 0)-d),x))
            ctrl=g['control']
        else:
            coverage=cv(rep)
            candidates.sort(key=lambda x:(labels[(x,det)]['cell']!=lr['cell'],cv(x)[0]!=coverage[0],
                abs(cv(x)[1]-coverage[1]),abs(cv(x)[2]-coverage[2]),abs((labels[(x,det)].get('d') or 0)-d),x))
            ctrl=g['control']['opaque_id'] if g['control'] else None
        assert ctrl==(candidates[0] if candidates else None), g['group']
        matching.append({'group':g['group'],'representative':rep,'control':ctrl,'detector':det,
            'frozen_selection_rule_verified':True,'representative_observed_coverage':cv(rep),
            'control_observed_coverage':cv(ctrl) if ctrl else None,
            'same_cell':labels[(ctrl,det)]['cell']==lr['cell'] if ctrl else None,
            'representative_d':lr.get('d'),'control_d':labels[(ctrl,det)].get('d') if ctrl else None,
            'collector_completeness':'OPEN','physical_correctness_of_control':'OPEN',
            'missing_conditions':['No outside-group case'] if ctrl is None else
                (['Different cell'] if labels[(ctrl,det)]['cell']!=lr['cell'] else [])+
                (['Different observed coverage; cannot infer collector coverage'] if cv(ctrl)!=cv(rep) else [])+
                (['Different dimension'] if labels[(ctrl,det)].get('d')!=lr.get('d') else [])})
write('coverage-matching.json',{'status':'PASS_FROZEN_CHOICE_AUDITED','groups':matching,
    'no_reselection':True,'interpretation':'Matching limitations remain; grouped flags are not causes.'})

# Lock rows using only time, flags and frozen contrast trajectories.
locks=[]
for (oid,det,branch),u in sorted(units.items()):
    guard();keys=['times','CP_flags','m'] if det=='bocpd' else ['times','Z','evaluated']
    a=load(u['npz'],keys);times=a['times']; cut=720
    if branch=='FF':times=times[:cut]
    assert len(times) in (720,1441) and np.all(np.diff(times)==1)
    assert int(times[0])+720==CASES[oid]['proxy']
    flags=a['CP_flags'][:len(times)] if det=='bocpd' else a['Z'].any(axis=1)
    eligible=np.arange(len(times)) >= (1 if det=='bocpd' else 100)
    point_roles={}
    def add(i,role):
        if i is not None: point_roles.setdefault(int(i),[]).append(role)
    def neighbor(i):
        choices=np.flatnonzero(eligible & ~flags)
        if not len(choices):return None
        return int(min(choices,key=lambda j:(abs(int(j)-i),int(j))))
    pre=np.flatnonzero(flags & eligible & (np.arange(len(times))<cut))
    post=np.flatnonzero(flags & eligible & (np.arange(len(times))>=cut))
    first=int(pre[0]) if len(pre) else None;firstpost=int(post[0]) if len(post) else None
    add(first,'first_pre_proxy_alarm');add(neighbor(first),'nearest_no_alarm_to_first_pre') if first is not None else None
    add(firstpost,'first_post_proxy_alarm');add(neighbor(firstpost),'nearest_no_alarm_to_first_post') if firstpost is not None else None
    add(min(cut,len(times)-1),'proxy_or_prefix_end');add(len(times)-1,'end_of_record')
    if not len(pre):add(int(np.flatnonzero(eligible)[0]),'first_evaluated_no_pre_alarm')
    if det=='bocpd' and branch!='full':
        fj=factorial[oid][1]
        pairbranches={'scale_with_M_F':['FF','FP'],'scale_with_M_P':['PF','PP'],
            'mask_d_prior_with_S_F':['FF','PF'],'mask_d_prior_with_S_P':['FP','PP'],
            'total_full_preprocessing_vs_prefix':['FF','PP'],'interaction':['FF','FP','PF','PP']}
        for cname,c in fj['contrasts'].items():
            if not c['defined'] or branch not in pairbranches[cname]:continue
            mv=c['signed_m_interaction'] if cname=='interaction' else c['signed_m_difference']
            fv=c['signed_CP_flag_interaction'] if cname=='interaction' else c['signed_CP_flag_difference']
            for kind,v in [('m',mv),('CP',fv)]:
                changed=np.flatnonzero(np.asarray(v)!=0)
                if len(changed):add(int(changed[0]),'first_'+kind+'_difference/'+cname)
    locks.append({'opaque_id':oid,'detector':det,'branch':branch,'source':u,'indices':sorted(point_roles),
        'point_roles':point_roles,'first_pre_alarm':first,'first_post_alarm':firstpost,
        'nearest_no_alarm_absent':first is not None and neighbor(first) is None,
        'points':len(times),'selection':'First pre/post alarm; nearest evaluated no-alarm, ties lower index; proxy/end; first frozen m/CP contrast difference. No scalar-informed selection.',
        'interpretation_status':'LOCKED_BEFORE_VALUE_EXTRACTION'})
write('points-lock.json',{'status':'LOCKED_BEFORE_MANUAL_INTERPRETATION','units':locks,'unit_count':len(locks),
    'group_source':'runs/session6-groups-001/bao-phu-nhom.json','source_sha256':SOURCE_SHA,
    'rule_is_diagnostic_proxy_informed':True,'new_detector':False})

# Saved scalar extraction; native loop is never called.
point_evidence=[]; raw_inventory=json.loads((H/'runs/preflight-002/inventory.json').read_text())
raw_paths={x['opaque_id']:x['files']['metrics.parquet'] for x in raw_inventory['cases']}
fixed={(x['opaque_id'],x['detector']):x for x in INPUT['locator']['fixed']}
for oid in sorted(CASES):
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
                # Array schema is read from the saved frozen source, not guessed.
                r['fixed_arrays']={k:(v[i] if v.ndim>=1 and v.shape[0]==len(a['times']) else v)
                    for k,v in fz.items() if k not in ('times','columns','x')}
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
    filename=oid+'--points.json';write(filename,{'opaque_id':oid,'units':casepoints})
    point_evidence.append({'opaque_id':oid,'file':filename,'unit_count':len(casepoints)})
    print('EXTRACTED '+oid, file=sys.stderr,flush=True)
    del raw,cz
write('point-index.json',{'status':'PASS_SAVED_VALUES_EXTRACTED','cases':point_evidence,
    'units':len(locks),'manual_interpretation':'OPEN','detectors_reexecuted':False})
write('source-verification.json',{'status':'PASS','sources':verified,'raw_metrics':[
    {'opaque_id':oid,'sha256':CASES[oid]['files']['metrics.parquet']['sha256']} for oid in CASES],
    'source_after_sha256':sha(H/'inputs/source.json'),'normalization_recomputed':'Not rerun; saved operands extracted',
    'resources':{'logical_bytes':sum(p.stat().st_size for p in H.rglob('*') if p.is_file()),
                 'ram_available_bytes':psutil.virtual_memory().available},'manual_interpretation':'OPEN'})
write('manifest.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()})
print(json.dumps({'status':'PASS','run':'runs/session7-manual-001','units':len(locks),
    'files':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()}}))
