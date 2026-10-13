"""Recover selected frozen-normalizer lineages; native m/CP stay authoritative."""
import hashlib,importlib.util,json,math,pathlib,time
import numpy as np
from scipy.stats import multivariate_t
sp=importlib.util.spec_from_file_location('t',pathlib.Path(__file__).with_name('target_theta.py'));t=importlib.util.module_from_spec(sp);sp.loader.exec_module(t);w=t.w
def finite_logpdf(X,i,r):
 st=t.state_before(X,i,r);d=X.shape[1];df=float(st['dof']-d+1);k=float(st['kappa']);shape=np.linalg.inv(k*df/(k+1)*st['scale'])
 np.linalg.cholesky(shape);assert df>0 and np.isfinite(X[i]).all()
 lp=float(multivariate_t.logpdf(X[i],df=df,loc=st['mu'],shape=shape));assert math.isfinite(lp)
 return lp,{'df':df,'shape_SPD_cholesky':True,'X_finite':True}
def lineage(z,i,r):
 X=z['X'];R=z['R'];f=z['predictive_density'];Z=z['normalizer'];start=i-r;v=float(R[0,start]);assert v>0
 logweight=math.log(v);events=[];pdf0=[];first=None;errors=[]
 for s in range(start,i):
  j=s-start;density=float(f[s,j]);parent=float(R[j,s]);child=float(R[j+1,s+1]);normal=float(Z[s]);assert normal>0 and math.isfinite(normal)
  if density>0:lp=math.log(density)
  else:
   lp,gate=finite_logpdf(X,s,j);pdf0.append({'index':s,'parent':j,'logpdf':lp,**gate})
  loggrowth=logweight+lp+math.log(.98);logweight=loggrowth-math.log(normal)
  if child==0 and first is None:
   # Source operator ordering stays authoritative; this diagnostic explains
   # where finite positive mathematical lineage was rounded to zero.
   numerator=float(parent*density*.98);lpmodel,gate=finite_logpdf(X,s,j)
   first={'index':s,'parent':j,'parent_R_native':parent,'PDF_native':density,'native_growth_numerator':numerator,'normalizer_native':normal,'native_child_R':child,'log_child_frozen_normalizer_lineage':logweight,'log_model_pdf':lpmodel,**gate,'numeric_class':'growth_product_underflow' if parent>0 and density>0 and numerator==0 else ('normalization_underflow' if numerator>0 else 'already_zero_parent_or_pdf_zero')}
  if child>=np.finfo(float).tiny and first is None:errors.append(abs(logweight-math.log(child)))
 current=float(f[i,r]);currentlp=math.log(current) if current>0 else finite_logpdf(X,i,r)[0]
 return {'parent':r,'history_start':start,'initial_reset_posterior_native':v,'native_parent_R':float(R[r,i]),'log_parent_R_frozen_normalizer_lineage':logweight,'current_PDF_native':current,'current_logpdf':currentlp,'current_log_growth_frozen_normalizer_lineage':logweight+currentlp+math.log(.98),'first_native_zero':first,'PDF_zero_events':pdf0,'max_pre_underflow_normal_R_logerror':max(errors,default=0.)}
def run():
 out=[]
 for oid in ['dev-3ae0a6c15a','dev-ba831dbeb8']:
  a=json.loads((w.OUT/(oid+'--marginal-channel.json')).read_text());i=a['first_m_difference'];row=next(x for x in a['points'] if x['index']==i);rf=row['FF_m']-1;rp=row['PF_m']-1;assert min(rf,rp)>=0
  zf=np.load(w.source(a['full_source']),allow_pickle=False);zp=np.load(w.source(a['PF_source']),allow_pickle=False)
  assert np.array_equal(zf['m'],np.argmax(zf['R'][:,1:],axis=0)) and np.array_equal(zp['m'],np.argmax(zp['R'][:,1:],axis=0))
  F=[lineage(zf,i,r) for r in [rf,rp]];P=[lineage(zp,i,r) for r in [rf,rp]]
  feedback=(F[0]['log_parent_R_frozen_normalizer_lineage']-F[1]['log_parent_R_frozen_normalizer_lineage'])-(P[0]['log_parent_R_frozen_normalizer_lineage']-P[1]['log_parent_R_frozen_normalizer_lineage'])
  extra=(F[0]['current_logpdf']-F[1]['current_logpdf'])-(P[0]['current_logpdf']-P[1]['current_logpdf'])
  fg=F[0]['current_log_growth_frozen_normalizer_lineage']-F[1]['current_log_growth_frozen_normalizer_lineage'];pg=P[0]['current_log_growth_frozen_normalizer_lineage']-P[1]['current_log_growth_frozen_normalizer_lineage'];err=abs(fg-pg-feedback-extra);assert err<1e-10
  out.append({'opaque_id':oid,'index':i,'FF_MAP_native':row['FF_m'],'PF_MAP_native':row['PF_m'],'native_CP_unchanged':True,'FF_lineages':F,'PF_lineages':P,'frozen_normalizer_loglineage_contrast':{'FF_growth_logratio':fg,'PF_growth_logratio':pg,'feedback_Rparent_logratio_difference':feedback,'conditional_extra_relative_logpdf_difference':extra,'algebra_error':err},'source_FF':a['full_source'],'source_PF':a['PF_source'],'source_marginal':oid+'--marginal-channel.json'})
 w.write('zero-lineage-summary-001.json',{'status':'COMPLETE','cases':out,'interpretation':'Native zero parent R is numerical extinction when finite positive density/support confirmed. Frozen-normalizer loglineage is an explanatory diagnostic, not rerun detector posterior or change to native CP; recovery does not certify fully renormalized log-domain method.'});w.emit({'zero_lineage':'COMPLETE','cases':len(out),'first_events':[x['FF_lineages'][1]['first_native_zero'] for x in out]})
if __name__=='__main__':run()
