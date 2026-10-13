"""T033 migration wrapper. Original v3 engine/preprocessing body unchanged."""
import argparse, hashlib, importlib.util, inspect, json, os, pathlib, platform, sys, time, traceback
import numpy as np
import pandas as pd
import scipy
from scipy.stats import multivariate_t
from functools import partial
OUT=pathlib.Path(__file__).resolve().parent
INPUT=OUT/'migration-inputs-001'
MANIFEST=json.loads((INPUT/'manifest.json').read_text())
ASSIGNMENT=json.loads((OUT/'migration-assignment.json').read_text())
ASSIGNED=ASSIGNMENT['case_numbers']
S={'cases':MANIFEST['cases']}
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def checked(p,m):
 assert p.is_file() and p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],str(p)
 return p
native=checked(INPUT/'_bocpd.py',MANIFEST['native'])
sp=importlib.util.spec_from_file_location('native_bocpd',native);bm=importlib.util.module_from_spec(sp);sp.loader.exec_module(bm)
MultivariateT=bm.MultivariateT;online_changepoint_detection=bm.online_changepoint_detection;constant_hazard=bm.constant_hazard
for pkg in ['numpy','pandas','scipy']:assert globals()[{'numpy':'np','pandas':'pd','scipy':'scipy'}[pkg]].__version__==MANIFEST['environment'][pkg],pkg
def item_for(oid):return next(x for x in MANIFEST['cases'] if x['opaque_id']==oid)
def compact(oid):
 item=item_for(oid);return np.load(checked(INPUT/item['file'],item),allow_pickle=False)
def input_arrays(oid):
 item=item_for(oid);z=compact(oid);return item['source_native']['relative'],{k:z[k] for k in ['X','times','columns','m','CP_flags']}
def raw_selected(oid):
 z=compact(oid);return z['causal_raw'],z['causal_columns'].tolist()
def write(name,value):
 q=OUT/name;assert not q.exists(),name;q.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def emit(x):print(json.dumps(x,ensure_ascii=False,allow_nan=False),flush=True)
def causal(raw,kind,warmup=100):
 x=pd.DataFrame(raw).replace([np.inf,-np.inf],np.nan).ffill().fillna(0).to_numpy(float)
 low=x[:warmup].min(axis=0); high=x[:warmup].max(axis=0);div=np.where(high>low,high-low,1.)
 y=np.zeros_like(x);y[:warmup]=(x[:warmup]-low)/div
 if kind=='fixed':
  y[warmup:]=(x[warmup:]-low)/div
 else:
  for i in range(warmup,len(x)):
   low=x[:i].min(axis=0); high=x[:i].max(axis=0);div=np.where(high>low,high-low,1.)
   y[i]=(x[i]-low)/div
 assert np.isfinite(y).all()
 return y
def run_engine(X,times,kind='native'):
 d=X.shape[1];model=MultivariateT(dims=d)
 if kind=='prior_df4':model.dof[:]=d+3
 elif kind=='prior_kappa4':model.kappa[:]=4
 elif kind=='prior_precision4':model.scale[0]=4*np.eye(d)
 if kind=='compressed_calendar':
  gaps=np.r_[1,np.diff(times)];tick=[0]
  def hazard(r):
   i=tick[0];tick[0]+=1;return (-np.expm1(gaps[i]*np.log(.98)))*np.ones(r.shape)
 else:hazard=partial(constant_hazard,50)
 t=time.perf_counter();R,mx=online_changepoint_detection(X,hazard,model);elapsed=time.perf_counter()-t
 assert np.isfinite(R).all() and np.max(np.abs(R[:,1:].sum(0)-1))<1e-10
 m=R[:,1:].argmax(0);flags=np.r_[False,np.abs(np.diff(m))>1]
 selected=np.flatnonzero(flags)
 post=[{'index':int(i),'m':int(m[i]),'p_map':float(R[m[i],i+1]),'p_reset':float(R[0,i+1])} for i in selected]
 return m,flags,post,elapsed
def fixture():
 results=[]
 for d in [1,2,4]:
  mo=MultivariateT(dims=d);x=np.arange(d,dtype=float)/3;got=mo.pdf(x)[0]
  expected=multivariate_t.pdf(x,loc=np.zeros(d),shape=np.eye(d),df=2)
  assert got==expected;(results.append({'fixture':'native_predictive','d':d,'pass':True}))
 # Marginal of multivariate Student t uses covariance submatrix, fixed df.
 mf=MultivariateT(dims=3);ms=MultivariateT(dims=2)
 for x in np.array([[.2,.3,.5],[.7,.1,.9],[1.,.3,.4]]):
  mf.pdf(x);ms.pdf(x[:2]);mf.update_theta(x);ms.update_theta(x[:2])
  for r in range(len(ms.mu)):
   sf=(mf.kappa[r]+1)/(mf.kappa[r]*(mf.dof[r]-3+1))*np.linalg.inv(mf.scale[r])
   ss=(ms.kappa[r]+1)/(ms.kappa[r]*(ms.dof[r]-2+1))*np.linalg.inv(ms.scale[r])
   assert np.allclose(sf[:2,:2],ss,rtol=1e-12,atol=1e-14)
   assert np.array_equal(mf.mu[r,:2],ms.mu[r]) and mf.dof[r]-3==ms.dof[r]-2
 results.append({'fixture':'NIW_predictive_shape_marginal','pass':True,'numeric_covariance_tolerance':'1e-12/1e-14; not CP tolerance'})
 rr=np.r_[np.zeros((100,2)),np.ones((40,2)),np.full((20,2),3.)]
 for kind in ['fixed','expanding']:
  assert np.array_equal(causal(rr,kind)[:130],causal(rr[:130],kind));results.append({'fixture':'causal_suffix_X','kind':kind,'pass':True})
  a=causal(rr[:110],kind);b=causal(rr[:115],kind)
  ma,fa,_,_=run_engine(a,np.arange(len(a)));mb,fb,_,_=run_engine(b,np.arange(len(b)))
  assert np.array_equal(ma,mb[:len(ma)]) and np.array_equal(fa,fb[:len(fa)])
  results.append({'fixture':'causal_suffix_engine','kind':kind,'pass':True})
 write('fixtures.json',{'status':'PASS','checks':results,'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'pandas':pd.__version__,'machine':platform.machine()}})
 emit({'fixtures':'PASS'})
def pilot():
 fixture();item=S['cases'][0];oid=item['opaque_id'];rel,z=input_arrays(oid)
 for n in [128,len(z['X'])]:
  m,f,p,t=run_engine(z['X'][:n],z['times'][:n]);assert np.array_equal(m,z['m'][:n]);assert np.array_equal(f,z['CP_flags'][:n])
  write('pilot-'+str(n)+'.json',{'opaque_id':oid,'n':n,'d':z['X'].shape[1],'native_sham_exact':True,'wall_s':t,'source':rel,'selected':p})
  emit({'pilot':n,'wall_s':t,'native_sham_exact':True})
def engines():
 for ci,item in enumerate(S['cases']):
  if ci+1 not in ASSIGNED or (len(sys.argv)>2 and ci%2!=int(sys.argv[2])):continue
  oid=item['opaque_id'];rel,z=input_arrays(oid);X=z['X'];times=z['times']
  sham=OUT/(oid+'--prefix-sham.json')
  if not sham.exists():
   m,f,p,t=run_engine(X[:128],times[:128]);assert np.array_equal(m,z['m'][:128]) and np.array_equal(f,z['CP_flags'][:128])
   write(sham.name,{'native_sham_exact':True,'wall_s':t,'source':rel})
  full_sham=OUT/(oid+'--full-sham-thread1.json')
  if not full_sham.exists():
   emit({'case':ci+1,'branch':'native-full-sham-thread1','state':'START'})
   m,f,p,t=run_engine(X,times);assert np.array_equal(m,z['m']) and np.array_equal(f,z['CP_flags'])
   write(full_sham.name,{'native_full_sham_exact':True,'wall_s':t,'source':rel,'thread_environment':{k:os.environ.get(k) for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']}})
   emit({'case':ci+1,'branch':'native-full-sham-thread1','status':'PASS','wall_s':t})
  raw,cols=raw_selected(oid)
  for branch in ['prior_df4','prior_kappa4','prior_precision4','causal_fixed','causal_expanding','compressed_row','compressed_calendar']:
   target=OUT/(oid+'--'+branch+'.json')
   if target.exists():
    assert json.loads(target.read_text())['status']=='PASS','Existing failed branch must not be skipped: '+target.name
    continue
   emit({'case':ci+1,'total':len(S['cases']),'opaque_id':oid,'branch':branch,'state':'START'})
   start=time.perf_counter()
   if branch.startswith('causal'):
    xx=causal(raw,'fixed' if branch=='causal_fixed' else 'expanding');tt=times;mapping=np.arange(len(X))
    assert np.array_equal(xx[:500],causal(raw[:500],'fixed' if branch=='causal_fixed' else 'expanding'))
   elif branch.startswith('compressed'):
    keep=np.r_[True,np.any(X[1:]!=X[:-1],axis=1)];mapping=np.flatnonzero(keep);xx=X[keep];tt=times[keep]
   else:xx=X;tt=times;mapping=np.arange(len(X))
   try:
    m,f,p,t=run_engine(xx,tt,branch)
    engine_flags=f.copy()
    if branch.startswith('causal'): f[:100]=False
    idx=np.flatnonzero(f);orig=mapping[idx];alarm=tt[idx]
    changed=np.flatnonzero(f!=z['CP_flags']) if len(f)==len(z['CP_flags']) else None
    val={'status':'PASS','opaque_id':oid,'branch':branch,'source':rel,'engine_native_unchanged':True,'X_shape':list(xx.shape),'X_sha256':hashlib.sha256(xx.tobytes()).hexdigest(),'schema_columns':cols if branch.startswith('causal') else z['columns'].tolist(),'m':m.tolist(),'CP_flags':f.tolist(),'engine_CP_flags':engine_flags.tolist(),'alarm_evaluation_start':100 if branch.startswith('causal') else 1,'warmup_release':'fit first100 raw observations; transform actual warmup as initialization, no alarms before100' if branch.startswith('causal') else None,'retained_original_indices':mapping.tolist(),'alarm_original_indices':orig.tolist(),'alarms':alarm.tolist(),'selected_posterior':p,'CP_set_added':sorted(set(alarm.tolist())-set(times[z['CP_flags']].tolist())),'CP_set_removed':sorted(set(times[z['CP_flags']].tolist())-set(alarm.tolist())),'wall_s':t,'body_wall_s':time.perf_counter()-start}
    write(target.name,val);emit({'case':ci+1,'branch':branch,'status':'PASS','wall_s':t,'nCP':int(f.sum()),'n_input':len(xx),'d':xx.shape[1]})
   except Exception as exc:
    write(target.name,{'status':'ERROR','opaque_id':oid,'branch':branch,'error':repr(exc),'traceback':traceback.format_exc(),'body_wall_s':time.perf_counter()-start});raise
 part=int(sys.argv[2]) if len(sys.argv)>2 else -1
 write('engines-part'+str(part)+'-complete.json',{'status':'COMPLETE','part':part,'all_cases_for_part':len([i for i in range(len(S['cases'])) if i+1 in ASSIGNED and (part<0 or i%2==part)])})
 emit({'engines':'COMPLETE','part':part})
if __name__=='__main__':
 phase=sys.argv[1]
 if phase=='pilot':pilot()
 elif phase=='engines':engines()
