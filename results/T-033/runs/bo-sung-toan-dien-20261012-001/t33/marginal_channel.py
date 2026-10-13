"""Real FF/PF marginal coherence and conditional extra-channel evidence."""
import hashlib,importlib.util,json,pathlib,time
import numpy as np
from scipy.stats import multivariate_t
sp=importlib.util.spec_from_file_location('t',pathlib.Path(__file__).with_name('target_theta.py'));t=importlib.util.module_from_spec(sp);sp.loader.exec_module(t);w=t.w
def run():
 for ci,item in enumerate(w.S['cases']):
  oid=item['opaque_id'];dest=w.OUT/(oid+'--marginal-channel.json')
  if dest.exists():continue
  accepted=json.loads((w.OUT/'bocpd-locks.json').read_text());pr=next(v['npz'] for v in accepted if v['opaque_id']==oid and v['npz'].endswith('--PF.npz'))
  started=time.perf_counter();fr=w.full_rel(oid);fz=np.load(w.source(fr),allow_pickle=False);pz=np.load(w.source(pr),allow_pickle=False)
  F={k:fz[k] for k in ['X','columns','m','R','predictive_density','CP_flags']};P={k:pz[k] for k in ['X','columns','m','R','predictive_density','CP_flags']};T=len(P['X']);idx=[F['columns'].tolist().index(c) for c in P['columns'].tolist()];extra=[c for c in F['columns'].tolist() if c not in set(P['columns'].tolist())]
  assert np.array_equal(F['X'][:T,idx],P['X']),'SF common processed history must be identical'
  m_diff=np.flatnonzero(F['m'][:T]!=P['m']);cp_diff=np.flatnonzero(F['CP_flags'][:T]!=P['CP_flags']);points=sorted(set([0,T-1]+([int(m_diff[0])] if len(m_diff) else [])+([int(cp_diff[0])] if len(cp_diff) else [])));details=[];maxshape=0.;maxlog=0.
  for i in points:
   parents=sorted(set([0,max(0,int(F['m'][i])-1),max(0,int(P['m'][i])-1),int(F['m'][i-1]) if i else 0,int(P['m'][i-1]) if i else 0]));row=[]
   for r in parents:
    sf=t.state_before(F['X'],i,r);ss=t.state_before(P['X'],i,r);dfF=float(sf['dof']-F['X'].shape[1]+1);dfP=float(ss['dof']-P['X'].shape[1]+1)
    assert dfF==dfP and sf['kappa']==ss['kappa'] and np.array_equal(sf['mu'][idx],ss['mu'])
    psiF=np.linalg.inv(sf['scale']);psiP=np.linalg.inv(ss['scale']);a=psiF[np.ix_(idx,idx)];err=float(np.max(np.abs(a-psiP))/max(1.,np.max(np.abs(psiP))));assert err<1e-10;maxshape=max(maxshape,err)
    coef=float((sf['kappa']+1)/(sf['kappa']*dfF));shape=coef*a;lp=float(multivariate_t.logpdf(P['X'][i],df=dfF,loc=sf['mu'][idx],shape=shape));savedP=float(P['predictive_density'][i,r]);savedF=float(F['predictive_density'][i,r]);logP=np.log(savedP) if savedP>0 else None;logF=np.log(savedF) if savedF>0 else None;le=abs(lp-logP) if logP is not None else None
    if le is not None:assert le<1e-10;maxlog=max(maxlog,le)
    row.append({'parent':r,'predictive_df_common':dfF,'kappa_common':int(sf['kappa']),'mu_common_exact':True,'psi_common_relative_error':err,'marginal_logpdf_projected_from_full':lp,'PF_logpdf_authoritative':float(logP) if logP is not None else None,'FF_joint_logpdf_authoritative':float(logF) if logF is not None else None,'conditional_extra_logpdf':float(logF-lp) if logF is not None else None,'marginal_logpdf_error':le,'FF_parent_posterior':float(F['R'][r,i]),'PF_parent_posterior':float(P['R'][r,i]),'PF_pdf_underflow':savedP==0,'FF_pdf_underflow':savedF==0})
   details.append({'index':i,'FF_m':int(F['m'][i]),'PF_m':int(P['m'][i]),'FF_CP':bool(F['CP_flags'][i]),'PF_CP':bool(P['CP_flags'][i]),'parents':row})
  w.write(dest.name,{'status':'PASS','opaque_id':oid,'full_source':fr,'PF_source':pr,'common_history_exact':True,'d_full':F['X'].shape[1],'d_prefixmask':P['X'].shape[1],'extra_channels':extra,'first_m_difference':int(m_diff[0]) if len(m_diff) else None,'first_CP_difference':int(cp_diff[0]) if len(cp_diff) else None,'marginal_inverse_precision_scale_max_relative_error':maxshape,'marginal_logpdf_max_error':maxlog,'points':details,'body_wall_s':time.perf_counter()-started,'interpretation':'Native initial df2/mean0/kappa1/identity inverse precision-scale are marginally consistent. FullvsPF changes added-channel joint/conditional evidence and accumulated run-length posterior, not an independently identified static-prior defect. Floating shape/logpdf bound verifies algebra only; frozen CP/R/PDF remain authoritative.'});w.emit({'marginal_case':ci+1,'extra_count':len(extra),'first_m_difference':int(m_diff[0]) if len(m_diff) else None,'wall_s':time.perf_counter()-started,'max_shape_error':maxshape,'max_logpdf_error':maxlog})
 w.emit({'marginal_channel':'COMPLETE'})
if __name__=='__main__':run()
