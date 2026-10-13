"""Short independent scalar/metadata/native fixtures, never run on laptop."""
import numpy as np,pandas as pd
from common import sha,H,read
def fixtures(kind):
 out={'status':'PASS','kind':kind,'checks':{}}
 if kind=='channel':
  import channel_context as c
  out['existing']=c.fixtures(1_000_000)
  f=pd.DataFrame({'startTime':[100_000_000],'startTimeMillis':[100_000],'serviceName':['s'],'parentSpanID':[''],'traceID':['a'],'spanID':['1'],'duration':[3],'statusCode':[0]})
  a,s=c.trace_context(f,np.array([100]),1_000_000)
  assert s['status']=='OBSERVED_ARTIFACT' and s['status_code']=={'present_rows':1,'missing_rows':0,'interpretation':'Raw values only; no error/status semantics assumed'}
  out['checks']['status_metadata_schema']=True
 elif kind=='nsigma':
  from p3.adapters.phat_hien import nsigma
  # Constant, repeated values, jump, leading missing, inf fill and strict equality.
  vals=np.r_[np.zeros(100),3.,3.,0.,0.]
  f=pd.DataFrame({'time':np.arange(104),'s_latency-50':vals,'c_latency-50':np.zeros(104),'n_latency-50':np.r_[np.nan,np.zeros(99),3.,np.inf,0.,0.]})
  native=nsigma(f);clean=f.replace([np.inf,-np.inf],np.nan).ffill();manual=[]
  for col in clean.columns[1:]:
   for i in range(100,len(f)):
    past=clean[col].iloc[:i].dropna().to_numpy();mean=sum(past)/len(past);sd=(sum((v-mean)**2 for v in past)/(len(past)-1))**.5
    if abs(clean[col].iloc[i]-mean)>3*sd:manual.append(i)
  assert native['status']=='OK' and native['alarms']==sorted(set(manual))==[100,101]
  assert not abs(0.-0.)>3*0.
  out['checks'].update(independent_scalar_ddof_strict_flags=True,constant_repeat_nan_inf_boundary=True)
 elif kind=='bocpd':
  from p3.adapters.phat_hien import tien_xu_ly_bocpd,diem_doi_tu_R
  from baro._bocpd import online_changepoint_detection,constant_hazard
  from functools import partial
  from bocpd_core import observed,plain,compare_same_input
  f=pd.DataFrame({'v':[np.nan,2.,4.,4.],'constant':[2.,2.,2.,2.]})
  z=tien_xu_ly_bocpd(f);assert z.columns.tolist()==['v'] and np.array_equal(z.v,[0.,.5,1.,1.])
  collapse=tien_xu_ly_bocpd(pd.DataFrame({'nan':[np.nan,np.nan,np.nan]}));assert collapse.shape==(3,1) and np.array_equal(collapse.values,np.zeros((3,1)))
  class Ones:
   def __init__(self):self.n=0
   def pdf(self,x):self.n+=1;return np.ones(self.n)
   def update_theta(self,x,**kwargs):pass
  R,mx=online_changepoint_detection(np.zeros((4,1)),partial(constant_hazard,50),Ones())
  np.testing.assert_allclose(R[:2,1],[.02,.98],rtol=1e-12,atol=1e-14)
  np.testing.assert_allclose(R[:3,2],[.02,.0196,.9604],rtol=1e-12,atol=1e-14)
  cp,m=diem_doi_tu_R(R);assert cp==[] and m.tolist()==[1,2,3,4] and mx.tolist()==[0.,1.,2.,3.,0.]
  X=np.array([[0.],[.5],[1.],[1.]]);times=np.arange(4)
  r,a=observed(X,times,1,['v']);p,R0,m0=plain(X,times,1,['v']);assert all(compare_same_input(r,a,p,R0,m0).values())
  r2,a2=observed(X[:3],times[:3],1,['v']);assert np.array_equal(a['R'][:4,:4],a2['R']) and np.array_equal(a['m'][:3],a2['m'])
  from bocpd_delay import segments
  assert segments(np.array([True,True,False,True]),np.array([0,1,2,4]),1)==[{'start_index':0,'end_index':1,'start_time':0,'end_time':1,'points':2,'starts_before_and_reaches_proxy':True},{'start_index':3,'end_index':3,'start_time':4,'end_time':4,'points':1,'starts_before_and_reaches_proxy':False}]
  out['checks'].update(fill_drop_scale_collapse=True,scalar_normalization_m_CP_sentinel=True,observer_sham_exact_CP=True,fixed_input_prefix=True,segments_grid=True)
 else:raise ValueError(kind)
 return out
