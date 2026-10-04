"""T-013. Independent algebra vs untouched official code. No locked data.
Run with py312-pin; every output is scoped to results/T-013.
"""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['OMP_NUM_THREADS']=os.environ['OPENBLAS_NUM_THREADS']=os.environ['MKL_NUM_THREADS']='1'
import sys, json, csv, time, hashlib, subprocess, tarfile, platform, datetime
from pathlib import Path
from functools import partial
import numpy as np
import pandas as pd
from scipy.special import gammaln

ROOT=Path('D:/RCA-flashticket'); OUT=ROOT/'results/T-013'
for d in ['runs','trung-gian']: (OUT/d).mkdir(exist_ok=True)
RUN=OUT/'runs'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
RUN.mkdir(exist_ok=False)
def dump(p,obj):
    def safe(x):
        if isinstance(x,dict):return {str(k):safe(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)):return [safe(v) for v in x]
        if hasattr(x,'item'):x=x.item()
        if isinstance(x,float) and not np.isfinite(x):return 'NaN' if np.isnan(x) else 'Infinity' if x>0 else '-Infinity'
        return x
    Path(p).write_text(json.dumps(safe(obj),ensure_ascii=False,indent=2,allow_nan=False,default=str),encoding='utf-8')
def log(event,**kw):
    row={'time':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat(),'event':event,**kw}
    with (RUN/'tien-do.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    print(event,kw,flush=True)
def tasklog(s):
    with (ROOT/'tasks/T-013-ho-so-baro/LOG.md').open('a',encoding='utf-8') as f:f.write('\n- '+datetime.datetime.now().strftime('%H:%M:%S')+' — '+s+'\n')
def hashfile(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# All publication targets are read and recorded before any method is run.
moc={'paper':'https://arxiv.org/html/2405.09330v1','Table2':{'N-Sigma':{'OB':[.54,1,.70],'SS':[.56,1,.72],'TT':[.50,1,.67]},'BARO':{'OB':[.69,1,.82],'SS':[.60,1,.75],'TT':[.68,1,.81]}},'Table3_inject_Avg5':{'N-Sigma':{'OB':[.90,.93,.94,.66,.86],'SS':[.98,.98,.98,.90,.96]},'RobustScorer':{'OB':[.90,.94,.94,.65,.86],'SS':[.98,.98,.98,.86,.95]}},'README_A':{'timestep':243,'top5':['checkoutservice_latency','cartservice_mem','cartservice_latency','cartservice_cpu','main_mem']},'scope':'paper aggregate reused from T006/T007; new runs are mechanism checks, not full-table reproduction'}
dump(OUT/'doi-chieu-moc.json',moc)
log('publication_targets_recorded_before_runs')

sys.path.insert(0,'D:/RCA-ext/src/baro')
sys.path.insert(0,'D:/RCA-ext/src/RCAEval')
import importlib
br=importlib.import_module('baro.root_cause_analysis')
ad=importlib.import_module('baro.anomaly_detection')
bc=importlib.import_module('baro._bocpd')
re=importlib.import_module('RCAEval.e2e.baro')
reinit=importlib.import_module('RCAEval.e2e')

ledger=[]; checks=[]; cases=[]
def record(case,source,method,purpose,reason):
    ledger.append({'ca':case,'file_nguon':str(source),'phuong_phap':method,'muc_dich':purpose,'ly_do':reason})
    with (OUT/'ca-da-chay.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(ledger[0])); w.writeheader(); w.writerows(ledger)
def add(name,**kw):checks.append({'check':name,**kw}); dump(RUN/'checks-partial.json',checks)
def clean(d):
    d=d.drop(columns=['time.1'],errors='ignore')
    d=d.loc[:,~d.columns.str.endswith('_latency-50')]
    d=d.replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
    return d.rename(columns={c:c.replace('_latency-90','_latency') for c in d if c.endswith('_latency-90')})
def indep_pre(d,kind,dataset):
    # Independent literal pipeline with column behavior exposed.
    if kind=='re' and dataset is None:return d.copy()
    if kind=='re':
        d=d.drop(columns=['time.1'],errors='ignore')
        if 'time' in d:d=d.drop(columns='time')
        elif 'Time' in d:d=d.drop(columns='Time')
        if dataset=='causalrca-sock-shop':return d.copy()
    else:d=d.drop(columns=['time','Time','timestamp'],errors='ignore')
    if len(d):d=d.loc[:,(d!=d.iloc[0]).any()]
    for c in d:
        if c.endswith('_mem'):d[c]=d[c]/1e6
    return d
def independent_rank(d,inj,scorer,kind='re',dataset='re2-tt',cut=None):
    a,b=(d[d.time<inj],d[d.time>=inj]) if cut is None else (d.head(cut),d.tail(len(d)-cut))
    a=indep_pre(a.copy(),kind,dataset); b=indep_pre(b.copy(),kind,dataset)
    cols=[c for c in a if c in b]; rows=[]
    for c in cols:
        x=a[c].to_numpy(dtype=float); y=b[c].to_numpy(dtype=float)
        if scorer=='robust':
            q25,q50,q75=np.nanpercentile(x,[25,50,75]); scale=q75-q25; center=q50
            # sklearn RobustScaler _handle_zeros_in_scale(array) uses 10*eps.
            scale_eff=1. if scale<10*np.finfo(np.float64).eps else scale
        else:
            q25,q50,q75=np.nanpercentile(x,[25,50,75]); center=np.nanmean(x); scale=np.sqrt(np.nanvar(x,ddof=0)); scale_eff=1. if scale==0 else scale
        z=(y-center)/scale_eff; score=max(z)
        rows.append({'metric':c,'n_normal':len(x),'n_post':len(y),'q25':q25,'median':q50,'q75':q75,'mean':np.nanmean(x),'std_ddof0':np.sqrt(np.nanvar(x,ddof=0)),'scale_raw':scale,'scale_effective':scale_eff,'max_post':np.nanmax(y),'min_post':np.nanmin(y),'score':score,'max_abs_score':np.nanmax(np.abs(z))})
    ranks=[r['metric'] for r in sorted(rows,key=lambda r:r['score'],reverse=True)]
    return rows,ranks
def official_rank(d,inj,scorer,kind='re',dataset='re2-tt',cut=None):
    mod=br if kind=='br' else (re if scorer=='robust' else reinit)
    func=br.robust_scorer if kind=='br' and scorer=='robust' else br.nsigma if kind=='br' else re.baro if scorer=='robust' else reinit.nsigma
    attr='RobustScaler' if scorer=='robust' else 'StandardScaler'; original=getattr(mod,attr); observed=[]
    class Recorder(original):
        def transform(self,x,*args,**kw):
            y=super().transform(x,*args,**kw); observed.append({'score':float(max(y[:,0])),'center':self.center_.tolist() if hasattr(self,'center_') else self.mean_.tolist(),'scale':self.scale_.tolist()});return y
    setattr(mod,attr,Recorder)
    try:o=func(d.copy(),inj,dataset=dataset,anomalies=None if cut is None else [cut],dk_select_useful=False,sli=None)
    finally:setattr(mod,attr,original)
    return o,dict(zip(o['node_names'],observed))
def services(ranks):
    out=[]
    for r in ranks:
        s=r.split('_')[0]
        if s not in out:out.append(s)
    return out
def compare_ranks(tag,d,inj,scorer,kind,case,source,dataset,cut=None,reason='b'):
    log('rank_start',tag=tag,shape=list(d.shape))
    record(case,source,('BR' if kind=='br' else 'RE')+' '+scorer,tag,reason)
    t=time.perf_counter(); rows,ranks=independent_rank(d,inj,scorer,kind,dataset,cut)
    o,obs=official_rank(d,inj,scorer,kind,dataset,cut); elapsed=time.perf_counter()-t
    for r in rows:r['official_score']=obs[r['metric']]['score']; r['abs_error']=abs(r['score']-r['official_score'])
    finite=[r for r in rows if np.isfinite(r['score']) and np.isfinite(r['official_score'])]
    err=max((r['abs_error']/max(1,abs(r['official_score'])) for r in finite),default=0.)
    pd.DataFrame(rows).to_csv(RUN/(tag+'-metric.csv'),index=False,encoding='utf-8-sig')
    dump(RUN/(tag+'-ranks.json'),{'ranks':ranks,'official':o,'service_ranks':services(ranks),'observed_scalers':obs,'elapsed_shared_machine_sec':elapsed})
    assert ranks==o['ranks'],tag
    assert err<=1e-10,(tag,err)
    add(tag,n_metrics=len(rows),empty=not ranks,rank_matches=True,max_normalized_score_error=err,column_order_equals=ranks==o['node_names'],fallback=False,seconds_shared_machine=elapsed)
    log('rank_end',tag=tag,n=len(rows),max_error=err,seconds_shared_machine=elapsed)
    return rows,ranks

# Rule fixed in SPEC: size only, no results or label.
dev=sorted((ROOT/'data/rcaeval').glob('re2tt_*'))
assert len(dev)==30
tt=sorted([p/'metrics.parquet' for p in dev],key=lambda p:(-p.stat().st_size,str(p)))[0]
ttinj=Path('D:/RCA-ext/dl/rcaeval-inject')/tt.parent.name/'inject_time.txt'
if not ttinj.exists():ttinj=ROOT/'results/T-002/local-inspection/run-002/injection-metadata'/(tt.parent.name+'.txt')
adapter=json.loads(Path('D:/RCA-ext/work/T-013/metrics-selected.json').read_text())
assert str(tt)==adapter['source'] and hashfile(tt)==adapter['source_sha256']
adapter_file=Path(adapter['output']);assert hashfile(adapter_file)==adapter['output_sha256']
with np.load(adapter_file,allow_pickle=False) as z:raw_tt=pd.DataFrame(z['values'],columns=z['columns'].tolist())
inj_tt=int(ttinj.read_text().strip())
obs=sorted(Path('D:/RCA-ext/data/fse-ob').glob('**/simple_data.csv'))
sample=Path('D:/RCA-ext/dl/baro-simple_data.csv'); sample_hash=hashfile(sample)
matching=[p for p in obs if hashfile(p)==sample_hash]
ob=matching[0] if matching else obs[0]
raw_ob=pd.read_csv(ob); inj_ob=int((ob.parent/'inject_time.txt').read_text().strip())
cases=[('TT',tt.parent.name,tt,raw_tt,inj_tt,'re2-tt'),('OB','fse-ob/'+str(ob.parent.relative_to('D:/RCA-ext/data/fse-ob')).replace('\\','/'),ob,raw_ob,inj_ob,'fse-ob')]
selection={'rule_tt':'largest metrics.parquet among exactly 30 permitted dev; tie path','rule_ob':'hash match README else lex first with old A block','sample_matches':len(matching),'selected':[{'tag':tag,'case':case,'source':str(src),'sha256':hashfile(src),'shape':list(d.shape),'inject_time':inj,'time_min':float(d.time.min()),'time_max':float(d.time.max())} for tag,case,src,d,inj,ds in cases]}
selection['tt_injection_source']=str(ttinj)
dump(OUT/'trung-gian/chon-ca.json',selection)
assert ob.exists()
results={}
for tag,case,src,raw,inj,ds in cases:
    d=clean(raw)
    for length in [10,20]:
        half=length*30; w=pd.concat([d[d.time<inj].tail(half),d[d.time>=inj].head(half)],ignore_index=True)
        for scorer in ['robust','standard']:
            name=f'{tag}-L{length}-{scorer}'
            rows,ranks=compare_ranks(name,w,inj,scorer,'re',case,src,ds)
            results[name]={'rows':rows,'ranks':ranks}
            _,rbr=compare_ranks(name+'-BR',w,inj,scorer,'br',case,src,ds)
            add(name+'-BR-RE',equal=rbr==ranks)
            o2,_=official_rank(w,inj,scorer,'re',ds); record(case,src,'RE '+scorer,'repeat '+name,'a')
            rev=w[list(reversed(w.columns))]
            oo,obs_rev=official_rank(rev,inj,scorer,'re',ds); record(case,src,'RE '+scorer,'column permutation '+name,'b')
            base_scores={r['metric']:r['official_score'] for r in rows}
            same_score=all(np.isclose(v['score'],base_scores[k],rtol=1e-10,atol=1e-10) for k,v in obs_rev.items())
            add(name+'-repeat-permutation',repeat_equal=o2['ranks']==ranks,score_permutation_equal=same_score,rank_permutation_equal=oo['ranks']==ranks,tied_groups=[{'score':score,'metrics':[k for k,v in base_scores.items() if v==score]} for score in sorted(set(base_scores.values()),reverse=True) if sum(v==score for v in base_scores.values())>1])
            assert o2['ranks']==ranks and same_score
    normal=d[d.time<inj].tail(300).reset_index(drop=True); boundary=normal.time.iloc[len(normal)//2]
    for scorer in ['robust','standard']:
        rows,ranks=compare_ranks(tag+'-normal-normal-'+scorer,normal,boundary,scorer,'re',case,src,ds)
        add(tag+'-normal-normal-interpretation',scorer=scorer,returns_rank=bool(ranks),max_score=max((r['score'] for r in rows),default=None),meaningful_cause_valid=False)
    # Root label is parsed ONLY after all ranks saved; it is not an argument to any method.
    label=case.split('/')[-2].rsplit('_',1)[0] if tag=='OB' else case.removeprefix('re2tt_').rsplit('_',2)[0]
    labelrows={k:{'root':label,'root_service_rank':services(v['ranks']).index(label)+1 if label in services(v['ranks']) else None,'top5_services':services(v['ranks'])[:5]} for k,v in results.items() if k.startswith(tag+'-')}
    dump(RUN/(tag+'-labels-after-rank.json'),labelrows)
tasklog('bước 2: hai ca theo rule, BARO/N-Sigma BR/RE ở L10/L20; so từng điểm, lặp lại/đảo cột/normal-normal đã lưu '+str(RUN.relative_to(ROOT)))

# Multivariate Student-t predictive density: independent analytic formula, not scipy.stats call.
def bocpd_ind(x,hazard=50,mu0=0.,kappa0=1.,nu0=None):
    x=np.asarray(x,dtype=float); T,d=x.shape
    R=np.zeros((T+1,T+1)); R[0,0]=1; maxes=np.zeros(T+1)
    # store covariance inverse W^{-1}; avoid official inverse-of-inverse update.
    nu_prior=float(d+1) if nu0 is None else float(nu0)
    nu=np.array([nu_prior]); k=np.array([kappa0]); mu=np.full((1,d),mu0); cov=np.eye(d)[None,:,:]
    for t,obs in enumerate(x):
        preds=[]
        for j in range(t+1):
            df=nu[j]-d+1; shape=cov[j]*(k[j]+1)/(k[j]*df)
            delta=obs-mu[j]; sign,ld=np.linalg.slogdet(shape)
            q=delta@np.linalg.solve(shape,delta)
            lp=gammaln((df+d)/2)-gammaln(df/2)-.5*(d*np.log(df*np.pi)+ld)-(df+d)/2*np.log1p(q/df)
            preds.append(np.exp(lp))
        masses=R[:t+1,t]*preds
        R[1:t+2,t+1]=masses*(1-1/hazard);R[0,t+1]=sum(masses)/hazard
        R[:,t+1]/=sum(R[:,t+1])
        delta=obs-mu
        cov=np.concatenate([np.eye(d)[None,:,:],cov+(k/(k+1))[:,None,None]*delta[:,:,None]*delta[:,None,:]])
        mu=np.concatenate([np.full((1,d),mu0),(k[:,None]*mu+obs)/(k+1)[:,None]])
        nu=np.r_[nu_prior,nu+1];k=np.r_[kappa0,k+1]
        maxes[t]=np.argmax(R[:,t]) # deliberate reproduction of official off-by-one for comparison
    cps=[(i,float(abs(maxes[i]-maxes[i-1]))) for i in range(1,T+1) if abs(maxes[i]-maxes[i-1])>1]
    return R,maxes,cps
def prep_boc(d):
    cols=[c for c in d if 'queue-master' not in c and 'rabbitmq_' not in c and ('latency' in c or '_error' in c)]
    if not cols:cols=[c for c in d if c!='time']
    v=d[cols].copy()
    if not v.empty:v=v.loc[:,(v!=v.iloc[0]).any()]
    v=v.ffill().fillna(0)
    for c in v:
        rg=v[c].max()-v[c].min();v[c]=0 if rg==0 or pd.isna(rg) else (v[c]-v[c].min())/rg
    return v.ffill().fillna(0)
def boccheck(name,d,case='synthetic',source='generated',hazard=50):
    log('bocpd_start',tag=name,shape=list(d.shape)); record(case,source,'BOCPD',name,'b')
    v=prep_boc(d); x=v.to_numpy()
    if v.empty:
        o=ad.bocpd(d);add(name,empty_input=True,official=o);return
    t=time.perf_counter(); Ri,mi,cpi=bocpd_ind(x,hazard)
    Ro,mo=bc.online_changepoint_detection(x,partial(bc.constant_hazard,hazard),bc.MultivariateT(dims=x.shape[1]))
    err=float(np.nanmax(abs(Ri-Ro))); cpo=[(i,float(abs(mo[i]-mo[i-1]))) for i in range(1,len(mo)) if abs(mo[i]-mo[i-1])>1]
    assert err<=1e-10,(name,err); assert np.array_equal(mi,mo); assert cpi==cpo
    if hazard==50:
        oo=ad.bocpd(d.copy());assert oo==[p[0] for p in cpo]
    else:oo=[p[0] for p in cpo]
    np.savez_compressed(RUN/(name+'-posterior.npz'),independent=Ri,official=Ro)
    v.to_csv(RUN/(name+'-normalized.csv'),index=False,encoding='utf-8-sig')
    dump(RUN/(name+'-detail.json'),{'maxes':mi.tolist(),'cps':cpi,'cps_in_range':[p for p in cpi if p[0]<len(d)],'last_posterior_mode':int(np.argmax(Ri[:,-1])),'time_unit':'cps are row indices, not time values','dims':x.shape[1],'T':len(d),'first_posterior':Ri[:3,:3].tolist(),'seconds_shared_machine':time.perf_counter()-t})
    add(name,posterior_max_abs_error=err,maxes_equal=True,cps_equal=True,anomalies=oo,sentinel_out_of_range=len(d) in oo,normalized_dims=x.shape[1],T=len(d),seconds_shared_machine=time.perf_counter()-t)
    log('bocpd_end',tag=name,error=err,seconds_shared_machine=time.perf_counter()-t)
def nsind(d,k=3,start=100):
    hits=[];detail=[]
    for c in d:
        if c=='time':continue
        x=d[c].to_numpy(dtype=float)
        for i in range(start,len(d)):
            past=x[:i]; m=np.nanmean(past);s=np.nanstd(past,ddof=1);hit=bool(abs(x[i]-m)>k*s)
            if hit:hits.append(d.time.iloc[i])
            if i==start or hit:detail.append({'metric':c,'i':i,'time':float(d.time.iloc[i]),'value':x[i],'mean':m,'std_ddof1':s,'threshold':k*s,'hit':hit})
    return hits,detail
for tag,case,src,raw,inj,ds in cases:
    prefix=raw.iloc[:120].copy()
    boccheck(tag+'-prefix120-bocpd',prefix,case,str(src))
    hits,detail=nsind(raw); t=time.perf_counter();record(case,src,'N-Sigma detector','full independent vs official','b'); official=ad.nsigma(raw.copy())
    assert hits==official
    pd.DataFrame(detail).to_csv(RUN/(tag+'-nsigma-detail.csv'),index=False,encoding='utf-8-sig')
    dump(RUN/(tag+'-nsigma-hits.json'),{'official':official,'independent':hits,'first_list':hits[0] if hits else None,'earliest_time':min(hits) if hits else None,'distinct':len(set(hits)),'count':len(hits)})
    rev=ad.nsigma(raw[list(reversed(raw.columns))].copy()); record(case,src,'N-Sigma detector','column permutation full','b')
    add(tag+'-nsigma-full',exact_match=True,count=len(hits),distinct=len(set(hits)),first_list=float(hits[0]) if hits else None,earliest_time=float(min(hits)) if hits else None,permutation_sorted_equal=sorted(rev)==sorted(hits),permutation_list_equal=rev==hits,seconds_shared_machine=time.perf_counter()-t)
    # BOCPD permutation on the same prefix; covariance prior isotropic.
    o1=ad.bocpd(prefix); o2=ad.bocpd(prefix[list(reversed(prefix.columns))]);record(case,src,'BOCPD','prefix permutation/repeat','a')
    add(tag+'-bocpd-repeat-permutation',equal=o1==o2)
tasklog('bước 3: detector hai prefix/ca, N-Sigma nguyên ca, posterior độc lập; mọi lượt và chi phí tham khảo trong runs.')

# Small reproducible counterexamples; no dataset benchmark or detector redesign.
synthetics={
 'iqr-zero':pd.DataFrame({'time':range(12),'a_cpu':[0,0,0,0,0,1,2,3,4,5,6,7],'b_cpu':[1,2,3,4,5,6,7,8,9,10,11,12]}),
 'constant-half':pd.DataFrame({'time':range(12),'a_cpu':[1]*6+[2,3,4,5,6,7],'b_cpu':[1,2,3,4,5,6]*2,'c_cpu':[3]*12}),
 'falling':pd.DataFrame({'time':range(12),'a_cpu':[10,11,12,13,14,15,1,2,3,4,5,6],'b_cpu':[1,2,3,4,5,6]*2}),
 'ties':pd.DataFrame({'time':range(12),'a_cpu':[1,2,3,4,5,6]*2,'b_cpu':[1,2,3,4,5,6]*2}),
 'nan':pd.DataFrame({'time':range(12),'a_cpu':[np.nan,1,2,3,4,5,np.nan,7,8,9,10,11],'b_cpu':[np.nan]*12}),
 'unit-IQR0':pd.DataFrame({'time':range(12),'a_cpu':[0,0,0,0,0,1,2,3,4,5,6,7],'a_mem':np.array([0,0,0,0,0,1,2,3,4,5,6,7])*1e6}),
 'empty-normal':pd.DataFrame({'time':range(12),'a_cpu':range(12)}),
 'one-normal':pd.DataFrame({'time':range(12),'a_cpu':range(12)}),
 'short-normal':pd.DataFrame({'time':range(12),'a_cpu':range(12)}),
}
for name,d in synthetics.items():
    inj=0 if name=='empty-normal' else 1 if name=='one-normal' else 3 if name=='short-normal' else 6
    for sc in ['robust','standard']:
        for kind in ['br','re']:
            try:
                o,pts=official_rank(d,inj,sc,kind,'fse-ob');add('edge-'+name+'-'+sc+'-'+kind,result=o,points=pts)
            except Exception as e:add('edge-'+name+'-'+sc+'-'+kind,error=type(e).__name__+': '+str(e))
    if name in ['iqr-zero','constant-half','falling','ties','unit-IQR0']:
        compare_ranks('edge-'+name,d,inj,'robust','re','synthetic','generated','fse-ob')
    if name=='ties':
        o,_=official_rank(d[list(reversed(d.columns))],inj,'robust','re','fse-ob');add('edge-ties-reverse',ranks=o['ranks'])
    if name=='falling':
        # Implement paper two-sided expression and BR dict index quantiles separately.
        independent=[]
        for c in ['a_cpu','b_cpu']:
            x=sorted(d.loc[d.time<inj,c]);y=d.loc[d.time>=inj,c].tolist();n=len(x)
            med=x[n//2];iqr=x[int(n*.75)]-x[int(n*.25)] or 1
            independent.append((c,abs(max(y)-med)/iqr))
        metrics={c:list(zip(d.time,d[c])) for c in ['a_cpu','b_cpu']}
        od=br.robust_scorer(metrics,inject_time=inj)
        assert od['scores']==sorted(independent,key=lambda v:v[1],reverse=True)
        add('edge-dict-falling',official=od,independent=independent)
        # Boundary argument uses positions even when anomaly list contains epoch seconds.
        epoch=d.copy();epoch.time=1700000000+np.arange(12)
        try:o,_=official_rank(epoch,None,'robust','br','fse-ob',cut=1700000006);add('edge-epoch-as-anomalies',result=o)
        except Exception as e:add('edge-epoch-as-anomalies',error=repr(e))

small=pd.DataFrame({'time':np.arange(12)*7+1700000000,'a_latency':np.arange(12)%3})
boccheck('edge-no-change',small)
for at in [1,10]:
    d=small.copy();d['a_latency']=(np.arange(12)>=at).astype(float)+np.arange(12)%2*.01
    boccheck('edge-change-'+str(at),d)
for h in [5,250]:boccheck('edge-hazard-'+str(h),small,hazard=h)
for dims in [1,2]:
    prior=bc.MultivariateT(dims=dims)
    add('edge-prior-dims-'+str(dims),nu=prior.dof.tolist(),kappa=prior.kappa.tolist(),mu=prior.mu.tolist(),scale=prior.scale.tolist())
for name,d in [('all-constant',pd.DataFrame({'time':range(12),'a_latency':[1]*12})),('no-matching-name',pd.DataFrame({'time':range(12),'a_cpu':np.arange(12)%3})),('NaN-leading',pd.DataFrame({'time':range(12),'a_latency':[np.nan,1,2,3,4,5,6,7,8,9,10,11]})),('only-time',pd.DataFrame({'time':range(12)}))]:boccheck('edge-bocpd-'+name,d)
for start in [100,1]:
    hits,detail=nsind(small,start=start);o=ad.nsigma(small,startsfrom=start);assert hits==o
    add('edge-nsigma-start-'+str(start),hits=hits,detail=detail)
# N-Sigma column order: first list element can fail to be earliest alert.
ns=pd.DataFrame({'time':range(110),'late_latency':np.r_[np.zeros(108),10.,0.],'early_latency':np.r_[np.zeros(100),10.,np.zeros(9)]})
hi,de=nsind(ns);ho=ad.nsigma(ns);assert hi==ho
add('edge-nsigma-first-vs-min',hits=ho,first=ho[0],earliest=min(ho),reverse=ad.nsigma(ns[list(reversed(ns.columns))]))
# Dataset and naming core differences.
for ds in [None,'causalrca-sock-shop','fse-ob']:
    d=synthetics['ties'].copy();d['timestamp']=range(12);d['time.1']=range(12)
    for kind in ['br','re']:
        try:o,_=official_rank(d,6,'robust',kind,ds);add('edge-dataset-'+str(ds)+'-'+kind,result=o)
        except Exception as e:add('edge-dataset-'+str(ds)+'-'+kind,error=repr(e))

# Old aggregate window difference is re-read, not copied from narrative.
p10=ROOT/'results/T-006/cham/l4-nsigma-fse-ob-len10-lan1.json';p20=ROOT/'results/T-006/cham/l4-nsigma-fse-ob-lan1.json'
old10=json.loads(p10.read_text());old20=json.loads(p20.read_text())
window={'sources':[str(p10),str(p20)],'delay_Avg5_L10':old10['diem']['delay']['Avg5'],'delay_Avg5_L20':old20['diem']['delay']['Avg5'],'difference':old10['diem']['delay']['Avg5']-old20['diem']['delay']['Avg5']}
dump(OUT/'trung-gian/cua-so-cu.json',window)
add('old-window-aggregate',**window)

freeze=subprocess.check_output(['D:/RCA-ext/envs/tools/Scripts/uv.exe','pip','freeze','--python',sys.executable],text=True,encoding='utf-8')
(OUT/'trung-gian/freeze-py312-pin.txt').write_text(freeze,encoding='utf-8')
summary={'run_dir':str(RUN),'checks':checks,'selection':selection,'window':window,'python':sys.version,'executable':sys.executable,'elapsed_is_official_benchmark':False,'status':'complete','all_inputs_scoped':True,'no_locked_data':True}
dump(OUT/'kiem-tra.json',summary)
tasklog('bước 3/4: hoàn tất synthetic edge cases, cửa sổ ô DELAY chênh đọc lại từ JSON, môi trường freeze đã lưu; kết quả kiểm-tra.json.')
log('complete',checks=len(checks),ledger=len(ledger))
