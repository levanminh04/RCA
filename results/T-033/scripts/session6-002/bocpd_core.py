"""Quan sát native BOCPD; không thay loop, likelihood, hazard hay theta."""
import inspect
from functools import partial

import numpy as np
from baro._bocpd import MultivariateT, constant_hazard, online_changepoint_detection
from baro.utility import find_cps
from p3.adapters.phat_hien import diem_doi_tu_R

class Observer:
    def __init__(self, dims, T, tick=None):
        self.native = MultivariateT(dims=dims)
        self.T=T
        self.pred=np.full((T,T),np.nan)
        self.normalizer=np.full(T,np.nan)
        self.reset_mass=np.full(T,np.nan)
        self.m_online=np.full(T,-1,dtype=int)
        self.runner=np.full(T,-1,dtype=int)
        self.states={}
        self.previous=None
        self.keep_next=False
        self.first_post_cp=None
        self.tick=tick
        self.native_error=None
        self.partial_R=None
        self.partial_maxes=None

    def pdf(self,x):
        frame=inspect.currentframe().f_back
        assert frame.f_code is online_changepoint_detection.__code__
        self.partial_R=frame.f_locals['R']
        self.partial_maxes=frame.f_locals['maxes']
        del frame
        try:
            result=self.native.pdf(x)
        except Exception as exc:
            self.native_error=f'{type(exc).__name__}: {exc}'
            raise
        i=self.native.t-1
        self.pred[i,:len(result)]=result
        return result

    def update_theta(self,x,**kwargs):
        frame=inspect.currentframe().f_back
        assert frame.f_code is online_changepoint_detection.__code__
        loc=frame.f_locals
        i=loc['t']; R=loc['R']; pred=loc['predprobs']; hazard=loc['H']
        mass=np.zeros(R.shape[0])
        mass[1:i+2]=R[:i+1,i]*pred*(1-hazard)
        mass[0]=np.sum(R[:i+1,i]*pred*hazard)
        total=np.sum(mass)
        self.normalizer[i]=total
        self.reset_mass[i]=mass[0]
        with np.errstate(all='ignore'):
            reconstructed=mass/total
        assert np.array_equal(reconstructed,R[:,i+1],equal_nan=True), 'native normalization operands mismatch'
        finite=np.isfinite(R[:,i+1]).all()
        m=int(R[:,i+1].argmax()) if finite else -1
        self.m_online[i]=m
        # Chỉ các hàng có support; tie giữ chỉ số thấp nhất như argmax.
        rank=np.argsort(-R[:i+2,i+1],kind='stable') if finite else np.array([0])
        runner=int(rank[1]) if finite and len(rank)>1 else -1
        self.runner[i]=runner
        old=int(self.m_online[i-1]) if i else -1
        cp=finite and i>=1 and old>=0 and abs(m-old)>1
        if i>=720 and cp and self.first_post_cp is None: self.first_post_cp=i
        parents=sorted(set([0]+[r for r in [m-1,runner-1,old] if 0<=r<=i]))
        index=np.full(4,-1,dtype=int); index[:len(parents)]=parents
        before={k:getattr(self.native,k)[parents].copy() for k in ('dof','kappa','mu','scale')}
        try:
            self.native.update_theta(x,**kwargs)
        except Exception as exc:
            self.native_error=f'{type(exc).__name__}: {exc}'
            raise
        after={k:getattr(self.native,k)[np.array(parents)+1].copy() for k in ('dof','kappa','mu','scale')}
        # Hàng0 vẫn là prior; hàng r+1 là update của hàngr, không nhầm ánh xạ.
        for k in ('dof','kappa','mu','scale'):
            assert np.array_equal(getattr(self.native,k)[0],before[k][0],equal_nan=True)
        state={'index':index,'before':before,'after':after}
        keep=cp or self.keep_next or i in (0,719,720) or (i>=720 and (self.first_post_cp is None or i<=self.first_post_cp))
        if cp and self.previous is not None: self.states[i-1]=self.previous
        if keep: self.states[i]=state
        self.previous=state
        self.keep_next=cp
        if self.tick and (i%100==0 or i==self.T-1): self.tick(i)
        del frame

    def arrays(self):
        out={'predictive_density':self.pred,'normalizer':self.normalizer,
             'reset_mass':self.reset_mass,'m_online':self.m_online,'runner_up':self.runner,
             'theta_points':np.array(sorted(self.states),dtype=int)}
        if not self.states: return out
        out['theta_parent_indices']=np.stack([self.states[i]['index'] for i in sorted(self.states)])
        for period in ('before','after'):
            for field in ('dof','kappa','mu','scale'):
                rows=[]
                for i in sorted(self.states):
                    arr=self.states[i][period][field]
                    padded=np.full((4,)+arr.shape[1:],np.nan)
                    padded[:len(arr)]=arr
                    rows.append(padded)
                out['theta_'+period+'_'+field]=np.stack(rows)
        return out

def result_from_R(R,maxes,times,raw_d,processed_d,columns):
    cps,m=diem_doi_tu_R(R)
    orig=[int(i) for i,_ in find_cps(maxes)]
    common={'alarms':[],'input_shape':{'T':len(times),'cot_tho':raw_d,'cot_sau_tien_xu_ly':processed_d},
            'detector_columns':columns}
    if cps is None:
        return dict(common,status='ERROR',error=f'posterior BOCPD không hữu hạn ở cột R {m}',
                    diagnostics={'cot_R_hong_dau_tien':m,'diem_doi_maxes_goc':orig})
    return dict(common,status='OK',alarms=[int(times[i]) for i in cps],chi_so=cps,
                bat_dau_danh_gia=1,diagnostics={'diem_doi_maxes_goc':orig,'co_sentinel_goc':bool(orig and orig[-1]==len(times))})

def observed(X,times,raw_d,columns,tick=None,detector_columns=None):
    ob=Observer(X.shape[1],len(X),tick)
    raw_columns=columns if detector_columns is None else detector_columns
    try:
        R,maxes=online_changepoint_detection(X,partial(constant_hazard,50),ob)
    except Exception:
        if ob.native_error is None: raise  # Lỗi observer không được miễn như native non-OK.
        result={'status':'ERROR','error':ob.native_error,'alarms':[],
                'input_shape':{'T':len(times),'cot_tho':raw_d,'cot_sau_tien_xu_ly':X.shape[1]},
                'detector_columns':raw_columns}
        arrays=ob.arrays()
        arrays.update(R_partial=ob.partial_R,maxes_partial=ob.partial_maxes,X=X,times=times,columns=np.array(columns))
        return result,arrays
    result=result_from_R(R,maxes,times,raw_d,X.shape[1],raw_columns)
    arrays=ob.arrays()
    arrays.update(R=R,maxes=maxes,X=X,times=times,columns=np.array(columns))
    if result['status']=='OK':
        m=R[:,1:].argmax(axis=0)
        assert np.array_equal(m,ob.m_online)
        arrays['m']=m
        flags=np.r_[False,np.abs(np.diff(m))>1]
        arrays['CP_flags']=flags
        arrays['normalization_error']=R[:,1:].sum(axis=0)-1
    return result,arrays

def plain(X,times,raw_d,columns,detector_columns=None):
    raw_columns=columns if detector_columns is None else detector_columns
    try:
        R,mx=online_changepoint_detection(X,partial(constant_hazard,50),MultivariateT(dims=X.shape[1]))
    except Exception as exc:
        return {'status':'ERROR','error':f'{type(exc).__name__}: {exc}','alarms':[],
                'input_shape':{'T':len(times),'cot_tho':raw_d,'cot_sau_tien_xu_ly':X.shape[1]},
                'detector_columns':raw_columns},None,None
    return result_from_R(R,mx,times,raw_d,X.shape[1],raw_columns),R,mx

def compare_same_input(obs,arrays,result,R,mx):
    checks={'status':obs['status']==result['status'],'alarms':obs['alarms']==result['alarms'],
            'indices':obs.get('chi_so')==result.get('chi_so'),
            'error':obs.get('error')==result.get('error')}
    if R is not None:
        checks['maxes']=np.array_equal(arrays['maxes'],mx,equal_nan=True)
        checks['posterior']=np.allclose(arrays['R'],R,rtol=1e-12,atol=1e-14,equal_nan=True)
    if obs['status']=='OK': checks['m']=np.array_equal(arrays['m'],R[:,1:].argmax(axis=0))
    return checks
