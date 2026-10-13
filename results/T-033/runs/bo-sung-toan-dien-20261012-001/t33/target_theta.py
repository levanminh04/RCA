"""Targeted native conjugate states; keep stored predictive density authoritative."""
import hashlib,importlib.util,json,pathlib,sys,time
import numpy as np
from scipy.special import gammaln
from scipy.stats import multivariate_t
sp=importlib.util.spec_from_file_location('w',pathlib.Path(__file__).with_name('worker-v3.py'));w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
FIELDS=['dof','kappa','mu','scale']
def state_before(X,i,r):
 assert 0<=r<=i
 mo=w.MultivariateT(dims=X.shape[1])
 # Original update is rowwise: branch r is prior updated in order on X[i-r:i].
 # After each update discard the unused prior row; retain its growth row.
 for x in X[i-r:i]:
  mo.update_theta(x)
  for f in FIELDS:setattr(mo,f,getattr(mo,f)[1:].copy())
  assert len(mo.kappa)==1
 return {f:getattr(mo,f)[0].copy() for f in FIELDS}
def run(pilot=False):
 locks=json.loads((w.OUT/'bocpd-locks.json').read_text());parts=locks[:4] if pilot else locks
 for ci,unit in enumerate(parts):
  oid=unit['opaque_id'];rel=unit['npz'];stem=oid+'--theta-target-density-'+hashlib.sha256(rel.encode()).hexdigest()[:8]+'.json';dest=w.OUT/stem
  if dest.exists():
   assert json.loads(dest.read_text())['status']=='PASS';continue
  started=time.perf_counter();z=np.load(w.source(rel),allow_pickle=False)
  a={k:z[k] for k in ['X','m','R','CP_flags','predictive_density','runner_up','theta_points','theta_parent_indices','normalizer']+['theta_before_'+f for f in FIELDS]}
  X=a['X'];d=X.shape[1];m=a['m'];R=a['R'];pred=a['predictive_density'];stored={int(i):j for j,i in enumerate(a['theta_points'])};rows=[];theta_checks=0;maxlogerr=0.;maxpdfrelative=0.
  # Include saved anchors and the locked points, so numerical path is verified.
  points=sorted(set(unit['points'])|{0})
  for i in points:
   runner=int(a['runner_up'][i]);parents=sorted(set([0,max(0,int(m[i])-1),max(0,runner-1),int(m[i-1]) if i else 0]));states=[state_before(X,i,r) for r in parents]
   if i in stored:
    j=stored[i]
    for slot,r in enumerate(a['theta_parent_indices'][j]):
     if r<0:continue
     assert int(r) in parents
     st=states[parents.index(int(r))]
     for f in FIELDS:
      assert np.array_equal(st[f],a['theta_before_'+f][j,slot],equal_nan=True),(oid,rel,i,int(r),f,'target-state-exact')
      theta_checks+=1
   model=w.MultivariateT(dims=d)
   for f in FIELDS:setattr(model,f,np.stack([s[f] for s in states]))
   model.t=len(parents)-1;native_small_batch=model.pdf(X[i]);details=[]
   for j,r in enumerate(parents):
    st=states[j];df=float(st['dof']-d+1);kap=float(st['kappa']);shape=np.linalg.inv((kap*df/(kap+1))*st['scale']);mu=st['mu'];sgn,ld=np.linalg.slogdet(shape);assert sgn>0
    delta=X[i]-mu;q=float(delta@np.linalg.solve(shape,delta));norm=float(gammaln((df+d)/2)-gammaln(df/2)-.5*d*np.log(df*np.pi)-.5*ld);res=float(-.5*(df+d)*np.log1p(q/df));lp=norm+res;lpscipy=float(multivariate_t.logpdf(X[i],df=df,loc=mu,shape=shape));algerr=abs(lp-lpscipy);assert algerr<1e-10
    saved=float(pred[i,r]);batch=float(native_small_batch[j]);relative=abs(saved-batch)/abs(saved) if saved else None
    # Source density remains the numeric result. Fixed error bound verifies
    # explanatory log-density algebra only, never CP or source states.
    saved_log_error=abs(lp-np.log(saved)) if saved>0 else None
    if saved_log_error is not None:assert saved_log_error<1e-10,(oid,i,r,'source log-density bound',saved_log_error)
    maxlogerr=max(maxlogerr,algerr,saved_log_error or 0.);maxpdfrelative=max(maxpdfrelative,relative or 0.)
    details.append({'parent':r,'history_start':i-r,'history_end_exclusive':i,'predictive_df':df,'kappa':kap,'shape_logdet':float(ld),'mahalanobis':q,'logpdf_normalizer':norm,'logpdf_residual':res,'logpdf_sum':lp,'logpdf_scipy':lpscipy,'logpdf_algebra_abs_error':algerr,'logpdf_vs_authoritative_saved_abs_error':saved_log_error,'pdf_authoritative_saved':saved,'pdf_native_selected_batch':batch,'native_selected_batch_exact_source':batch==saved,'native_selected_batch_relative_difference':relative,'prior_parent_posterior':float(R[r,i]),'growth_mass_authoritative':float(R[r,i]*saved*.98),'underflow_saved_pdf_zero':saved==0})
   masses=np.zeros(R.shape[0]);masses[1:i+2]=R[:i+1,i]*pred[i,:i+1]*.98;masses[0]=np.sum(R[:i+1,i]*pred[i,:i+1]*.02);normalizer=float(masses.sum());assert normalizer==a['normalizer'][i] and np.array_equal(masses/normalizer,R[:,i+1]);assert int(np.argmax(masses))==int(m[i])
   rows.append({'index':i,'was_locked':i in unit['points'],'CP_flag':bool(a['CP_flags'][i]),'m':int(m[i]),'previous_m':int(m[i-1]) if i else None,'had_saved_theta':i in stored,'parents':details,'normalizer_reconstruction_exact':True,'normalizer_saved':normalizer,'MAP_posterior_saved':float(R[m[i],i+1])})
  w.write(stem,{'status':'PASS','opaque_id':oid,'source':rel,'theta_exact_stored_checks':theta_checks,'log_density_max_abs_error':maxlogerr,'native_selected_batch_max_relative_difference':maxpdfrelative,'rows':rows,'body_wall_s':time.perf_counter()-started,'method':'Each native statebefore(i,r) reconstructed from native prior updates on X[i-r:i], same order; source density kept authoritative; CP and normalization exact; no posterior rerun'});w.emit({'target_theta_unit':ci+1,'source':rel,'wall_s':time.perf_counter()-started,'theta_exact_checks':theta_checks,'max_log_density_error':maxlogerr,'max_selected_batch_pdf_relative_difference':maxpdfrelative})
 w.emit({'target_theta':'PILOT_COMPLETE' if pilot else 'COMPLETE','source_count':len(parts)})
if __name__=='__main__':run(len(sys.argv)>1 and sys.argv[1]=='pilot')
