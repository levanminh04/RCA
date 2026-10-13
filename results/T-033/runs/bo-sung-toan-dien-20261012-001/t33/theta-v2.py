"""All-case diagnostics using retained channels/statistics; no new labels."""
import collections,hashlib,importlib.util,json,pathlib,re,sys,time
import numpy as np,pandas as pd
from scipy.special import gammaln
from scipy.stats import multivariate_t
spec=importlib.util.spec_from_file_location('w',pathlib.Path(__file__).with_name('worker-v3.py'));w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
O=w.OUT;S=w.S;CAT=w.CAT
PAIRS=json.loads((O/'locked-pairs.json').read_text())
def context_rel(oid):return next(k for k in CAT if k.endswith('/'+oid+'--context.npz') and '/channel-' in k)
def nsigma_rel(oid,det):
 return next(k for k in CAT if k.endswith('/'+oid+'--'+det+'.npz') and ('/nsigma-first-001/' in k or '/nsigma-rest-001/' in k))
def array_fields(z):return {k:z[k] for k in z.files}
def safe(v):
 if isinstance(v,np.ndarray):return safe(v.tolist())
 if isinstance(v,(np.floating,float)):return float(v) if np.isfinite(v) else None
 if isinstance(v,(np.integer,)):return int(v)
 if isinstance(v,list):return [safe(x) for x in v]
 if isinstance(v,dict):return {k:safe(x) for k,x in v.items()}
 return v
def histogram(x):return dict(collections.Counter(str(v) for v in x))
def curve(flags,times,proxy):
 alarm=times[np.asarray(flags,dtype=bool)];post=alarm[alarm>=proxy];pre=alarm[alarm<proxy]
 cooldown=[]
 for t in alarm:
  if not cooldown or t>=cooldown[-1]+300:cooldown.append(int(t))
 D=np.arange(0,int(times[-1]-proxy)+1);hits=np.searchsorted(post,proxy+D,side='right')
 notif=np.array(cooldown,dtype=np.int64);npost=notif[notif>=proxy]
 return {'first_alarm_offset':int(alarm[0]-proxy) if len(alarm) else None,'early_alarm_count':len(pre),'first_post_offset':int(post[0]-proxy) if len(post) else None,'D_seconds':D.tolist(),'post_alarm_count_by_D':hits.tolist(),'post_any_alarm_by_D':(hits>0).tolist(),'new_notifications_post_by_D':np.searchsorted(npost,proxy+D,side='right').tolist(),'followup_seconds':int(times[-1]-proxy),'definition':'inclusive proxy through proxy+D; no physical end/onset inference'}
def fast():
 start=time.perf_counter();allrows=[]
 for ci,item in enumerate(S['cases']):
  oid=item['opaque_id'];dest=O/(oid+'--context.json')
  if dest.exists():continue
  ctime=time.perf_counter();_,b=w.input_arrays(oid);times=b['times'];proxy=item['proxy']
  # Native per-column statistics retained by the frozen observer.
  ns=[]
  for det in ['nsigma','nsigma_doi_chung']:
   rel=nsigma_rel(oid,det);z=np.load(w.source(rel),allow_pickle=False);a=array_fields(z)
   X=a['x'];native_column_flags=a['Z'].astype(bool);old=native_column_flags.any(1)
   names=a['columns'].tolist();frame=pd.DataFrame(X)
   means=np.full_like(X,np.nan);stds=np.full_like(X,np.nan)
   for i in range(100,len(X)):
    means[i]=frame.iloc[i-100:i].mean().to_numpy();stds[i]=frame.iloc[i-100:i].std(ddof=1).to_numpy()
   flags=np.abs(X-means)>3*stds;flags[:100]=False;merged=flags.any(1)
   assert np.array_equal(native_column_flags,np.abs(X-a['mean'])>a['threshold'])
   assert np.array_equal(native_column_flags.any(1),old)
   multiplicity=native_column_flags.sum(1)
   ns.append({'detector':det,'source':rel,'n_columns':len(names),'native_OR_trigger_count_histogram':histogram(multiplicity[100:]),'native_column_flag_rate':safe(native_column_flags[100:].mean(0)),'native_OR_rate':float(old[100:].mean()),'native_sum_column_rates':float(native_column_flags[100:].mean(0).sum()),'native_joint_OR_fraction_of_sum':float(old[100:].sum()/native_column_flags[100:].sum()) if native_column_flags[100:].sum() else None,'rolling_OR_rate':float(merged[100:].mean()),'rolling_alarm_indices':np.flatnonzero(merged).tolist(),'rolling_added_indices':np.flatnonzero(merged & ~old).tolist(),'rolling_removed_indices':np.flatnonzero(old & ~merged).tolist(),'rolling_std0_cells':int((stds[100:]==0).sum()),'rolling_std0_trigger_cells':int(((stds[100:]==0)&flags[100:]).sum()),'rolling_missing_stat_cells':int((~np.isfinite(stds[100:])).sum()),'native_trigger_cells':int(native_column_flags[100:].sum()),'native_curve':curve(old,times,proxy),'rolling_curve':curve(merged,times,proxy),'causal_contract':'rolling uses exactly previous100 observations and ddof1; no independence/normality/operational false-alarm claim'})
  ctxrel=context_rel(oid);ctx=np.load(w.source(ctxrel),allow_pickle=False)
  metadata=w.read(ctxrel[:-4]+'.json')['summary'];entities=metadata['trace']['entities'];logsmeta=metadata['log'];logentities=logsmeta.get('entities')
  points=sorted(set(p[k] for p in PAIRS if p['opaque_id']==oid for k in ['alarm_index','control_index'] if p[k] is not None))
  windows=[]
  for point in points:
   for width in [10,30,60]:
    for side,lo,hi in [('before',max(0,point-width),point),('after',point,min(len(times),point+width))]:
     secmask=(ctx['trace_group_second']>=times[lo])&(ctx['trace_group_second']<times[hi-1]+1) if hi>lo else np.zeros(len(ctx['trace_group_second']),bool)
     tracerows=[]
     for ei,entity in enumerate(entities):
      ix=np.flatnonzero(secmask & (ctx['trace_group_entity']==ei));count=ctx['trace_group_duration_count'][ix].sum();means=ctx['trace_group_duration_mean_raw'][ix]
      tracerows.append({'entity':entity,'observed_spans':int(ctx['trace_group_span_count'][ix].sum()),'duration_count':int(count),'duration_mean_raw_weighted':float(np.nansum(means*ctx['trace_group_duration_count'][ix])/count) if count else None,'duration_min_raw':safe(ctx['trace_group_duration_min_raw'][ix].min()) if len(ix) else None,'duration_max_raw':safe(ctx['trace_group_duration_max_raw'][ix].max()) if len(ix) else None,'status_present':int(ctx['trace_grid_status_present'][lo:hi,ei].sum())})
     load=ctx['workload_raw'][lo:hi]
     windows.append({'point':point,'width':width,'side':side,'lo':lo,'hi_exclusive':hi,'observed_seconds':hi-lo,'trace':tracerows,'workload_mean_raw':safe(np.nanmean(load,axis=0)) if hi>lo else None,'workload_finite_count':np.isfinite(load).sum(0).tolist(),'workload_columns':ctx['workload_columns'].tolist(),'log_counts_by_entity':ctx['log_grid_row_count'][lo:hi].sum(0).tolist() if 'log_grid_row_count' in ctx else None,'log_entities':logentities,'physical_state':'UNIDENTIFIABLE: no clean-negative/effective-onset/outcome standard'})
  # Entire messages in the union of declared60s windows, counted once.
  loganalysis={'status':'N/A_MISSING_CHANNEL'}
  if 'logs.parquet' in item['files']:
   logs=pd.read_parquet(w.raw_path(item,'logs.parquet'));secs=logs['timestamp'].to_numpy();region=np.zeros(len(logs),bool)
   for point in points:region|=(secs>=times[max(0,point-60)])&(secs<times[min(len(times)-1,point+59)]+1)
   msgs=logs.loc[region,'message'];counts=collections.Counter();samples={}
   for m in msgs.dropna():
    classes=tuple(sorted(set(re.findall(r'\b(?:INFO|WARN|WARNING|ERROR|DEBUG|TRACE|FATAL)\b',m))));counts[classes]+=1
    for tok in re.findall(r'\b[A-Za-z_$][\w$]*(?:Exception|Error)\b',m):samples.setdefault(tok,m[:300])
   loganalysis={'status':'FULL_MESSAGES_IN_DECLARED_REGIONS','rows':int(region.sum()),'messages_missing':int(msgs.isna().sum()),'level_token_combinations':{'|'.join(k):v for k,v in counts.items()},'exception_or_error_class_token_samples':samples,'coverage':'Observed complete region of supplied log artifact, not instrumentation completeness or request-success standard','whole_artifact_rows':len(logs),'timestamp_unit':'source context schema int seconds; no timing inference beyond saved alignment'}
  v={'status':'PASS','opaque_id':oid,'source_context':ctxrel,'source_full':w.full_rel(oid),'nsigma':ns,'bocpd_curve':curve(b['CP_flags'],times,proxy),'windows':windows,'full_log_region_semantics':loganalysis,'channel_metadata':metadata,'body_wall_s':time.perf_counter()-ctime}
  w.write(dest.name,safe(v));w.emit({'context_case':ci+1,'opaque_id':oid,'points':len(points),'wall_s':v['body_wall_s']})
 w.emit({'context':'COMPLETE','wall_s':time.perf_counter()-start})
def theta():
 # Original update recurrence; not a new detector or full posterior replay.
 locks=json.loads((O/'bocpd-locks.json').read_text())
 for ci,unit in enumerate(locks):
  oid=unit['opaque_id'];rel=unit['npz'];dest=O/(oid+'--theta-density-'+hashlib.sha256(rel.encode()).hexdigest()[:8]+'.json')
  if dest.exists():continue
  z=np.load(w.source(rel),allow_pickle=False);X=z['X'];d=X.shape[1];m=z['m'];R=z['R'];pred=z['predictive_density'];model=w.MultivariateT(dims=d)
  points=set(unit['points']);rows=[];maxdensity=0.;maxlogerror=0.;thetachecks=0;exacttheta=True;started=time.perf_counter();stored={int(i):j for j,i in enumerate(z['theta_points'])}
  for i,x in enumerate(X):
   if i in points:
    model.t=i;native_densities=model.pdf(x)
    runner=int(z['runner_up'][i]);parents=sorted(set([0,max(0,int(m[i])-1),max(0,runner-1),int(m[i-1]) if i else 0]));details=[]
    for r in parents:
     df=float(model.dof[r]-d+1);kap=float(model.kappa[r]);shape=np.linalg.inv((kap*df/(kap+1))*model.scale[r]);mu=model.mu[r];sign,logdet=np.linalg.slogdet(shape);assert sign>0
     delta=x-mu;q=float(delta@np.linalg.solve(shape,delta));normal=float(gammaln((df+d)/2)-gammaln(df/2)-.5*d*np.log(df*np.pi)-.5*logdet);residual=float(-.5*(df+d)*np.log1p(q/df));lp=normal+residual
     lpscipy=float(multivariate_t.logpdf(x,df=df,loc=mu,shape=shape));diff=abs(lp-lpscipy);maxlogerror=max(maxlogerror,diff);assert diff<1e-10,(oid,i,r,'logdensity algebra',diff)
     manual_density=float(multivariate_t.pdf(x,df=df,loc=mu,shape=shape));density=float(native_densities[r]);saved=float(pred[i,r]);maxdensity=max(maxdensity,abs(density-saved));assert density==saved,(oid,i,r,density,saved)
     details.append({'parent':r,'predictive_df':df,'kappa':kap,'shape_logdet':float(logdet),'mahalanobis':q,'logpdf_normalizer':normal,'logpdf_residual':residual,'logpdf_sum':lp,'logpdf_scipy':lpscipy,'logpdf_abs_difference':diff,'pdf_native_batch':density,'pdf_manual_scalar':manual_density,'pdf_scalar_relative_difference':abs(manual_density-density)/abs(density) if density else None,'saved_pdf_exact':True,'prior_parent_posterior':float(R[r,i]),'growth_mass':float(R[r,i]*density*.98),'log_growth_mass':float(np.log(R[r,i])+lp+np.log(.98)) if R[r,i]>0 else None})
    if i in stored:
     j=stored[i]
     for slot,r in enumerate(z['theta_parent_indices'][j]):
      if r<0:continue
      for field in ['dof','kappa','mu','scale']:
       ok=np.array_equal(getattr(model,field)[r],z['theta_before_'+field][j,slot],equal_nan=True);exacttheta&=ok;thetachecks+=1;assert ok,(oid,i,r,field)
    masses=np.zeros(R.shape[0]);masses[1:i+2]=R[:i+1,i]*pred[i,:i+1]*.98;masses[0]=np.sum(R[:i+1,i]*pred[i,:i+1]*.02);normalizer=float(masses.sum());assert normalizer==z['normalizer'][i]
    assert np.array_equal(masses/normalizer,R[:,i+1]) and int(np.argmax(masses))==int(m[i])
    rows.append({'index':i,'CP_flag':bool(z['CP_flags'][i]),'m':int(m[i]),'previous_m':int(m[i-1]) if i else None,'had_saved_theta':i in stored,'parents':details,'normalizer_saved':float(z['normalizer'][i]),'normalizer_reconstruction_exact':True,'MAP_posterior_saved':float(R[m[i],i+1])})
   model.update_theta(x)
   if i>=max(points):break
  w.write(dest.name,safe({'status':'PASS','opaque_id':oid,'source':rel,'all_saved_theta_checks':thetachecks,'theta_exact':exacttheta,'predictive_density_max_abs_difference':maxdensity,'manual_log_density_max_abs_difference':maxlogerror,'rows':rows,'body_wall_s':time.perf_counter()-started,'method':'Native update_theta only; density exactly matches frozen selected parentpdf; no CP reclassification'}));w.emit({'theta_unit':ci+1,'source':rel,'wall_s':time.perf_counter()-started,'theta_checks':thetachecks,'density_exact':True})
if __name__=='__main__':
 if sys.argv[1]=='fast':fast()
 elif sys.argv[1]=='theta':theta()
