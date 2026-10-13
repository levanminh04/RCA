"""T-033 ca đầu lõi full/FF/PP; giữ mọi lượt và dừng CP lệch."""
import argparse
import hashlib
import json
import os
import resource
import shutil
import sys
import time
import traceback
from datetime import datetime,timezone
from pathlib import Path

import numpy as np
import pandas as pd
from baro.utility import drop_constant
from p3.adapters.phat_hien import cot_bocpd,tien_xu_ly_bocpd,bocpd as adapter
from bocpd_core import observed,plain,compare_same_input

H=Path(os.environ['T033_HOME']).resolve()
S=json.loads((H/'inputs/source.json').read_text())
INV=json.loads((H/'runs'/os.environ['T033_PREFLIGHT']/'inventory.json').read_text())
PATHS={r['opaque_id']:r['files'] for r in INV['cases']}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False))
def used(): return sum(p.stat().st_size for p in H.rglob('*') if p.is_file())
def progress(s):
    line=datetime.now(timezone.utc).isoformat()+' '+s
    print(line,flush=True)
    with (H/'trang-thai.txt').open('a') as f: f.write(line+'\n')

def fixtures():
    checks=[]
    for name,X in [('constant',np.zeros((12,1))),('step',np.r_[np.zeros(6),np.ones(6)].reshape(-1,1)),
                   ('repeated',np.tile([0.,1.],6).reshape(-1,1)),('nan',np.array([0.,np.nan,1.]).reshape(-1,1)),
                   ('inf',np.array([0.,np.inf,1.]).reshape(-1,1)),('d0',np.empty((3,0)))]:
        t=np.arange(len(X))
        ob,arr=observed(X,t,1,['a'])
        direct,R,mx=plain(X,t,1,['a'])
        c=compare_same_input(ob,arr,direct,R,mx)
        assert all(c.values()),(name,c)
        checks.append({'fixture':name,'checks':c,'status':ob['status']})
    ob,arr=observed(np.zeros((1,1)),np.array([100]),1,['a'])
    assert np.allclose(arr['predictive_density'][0,0],1/(2*np.sqrt(2)),rtol=1e-14)
    assert np.allclose(arr['R'][:,1],[.02,.98],rtol=1e-14)
    assert arr['theta_after_dof'][0,0]==3 and arr['theta_after_kappa'][0,0]==2
    assert arr['theta_after_mu'][0,0,0]==0 and arr['theta_after_scale'][0,0,0,0]==1
    checks.append({'fixture':'scalar_prior_likelihood_update','pass':True})
    raw=pd.DataFrame({'a':[np.nan,0.,1.,1.],'constant':[0.,0.,0.,0.]})
    full=tien_xu_ly_bocpd(raw)
    pref=tien_xu_ly_bocpd(raw.iloc[:2].copy())
    assert list(full)==list(pref)==['a']
    assert np.array_equal(full['a'],[0.,0.,1.,1.]) and np.array_equal(pref['a'],[0.,0.])
    checks.append({'fixture':'manual_drop_fill_range0','pass':True})
    # Engine cùng ma trận prefix đã xử lý, không gọi lại preprocessing.
    ob,arr=observed(np.arange(12.).reshape(-1,1),np.arange(12),1,['a'])
    d,R,mx=plain(arr['X'][:6],np.arange(6),1,['a'])
    assert np.array_equal(arr['m'][:6],R[:,1:].argmax(axis=0))
    checks.append({'fixture':'fixed_matrix_prefix_m_CP','pass':True})
    return checks

def main(args):
    run=H/'runs'/args.run
    run.mkdir(parents=True,exist_ok=False)
    status={'status':'RUNNING','pid':os.getpid(),'started_utc':datetime.now(timezone.utc).isoformat(),
            'scripts':{p.name:sha(p) for p in [Path(__file__),Path(__file__).with_name('bocpd_core.py')]},
            'source_sha256':sha(H/'inputs/source.json'),'cases':{},'command':sys.argv,
            'posterior_check_tolerance':{'rtol':1e-12,'atol':1e-14,'cannot_waive_m_CP_status_source_mismatch':True}}
    write(run/'status.json',status)
    t0=time.perf_counter()
    try:
        write(run/'fixtures.json',{'status':'PASS','checks':fixtures()})
        # Chi phí thấp nhất theo d nguồn, tie ID; không chọn theo kết quả CP.
        selected=min(S['cases'],key=lambda c:(c['expected']['bocpd']['input_shape']['cot_sau_tien_xu_ly'],c['opaque_id']))
        cases=[selected] if args.first else [c for c in S['cases'] if c['opaque_id']!=selected['opaque_id']]
        for item in cases:
            oid=item['opaque_id']; case={}
            if (H/'STOP').exists(): raise RuntimeError('STOP user/agent')
            assert time.perf_counter()-t0 < S['budget_compute_s']
            p=Path(PATHS[oid]['metrics.parquet'])
            assert sha(p)==item['files']['metrics.parquet']['sha256']
            df=pd.read_parquet(p); times=df['time'].to_numpy(); cols=cot_bocpd(df.columns)
            full=tien_xu_ly_bocpd(df[cols]); pp=tien_xu_ly_bocpd(df[cols].iloc[:720].copy())
            assert set(pp.columns)<=set(full.columns)
            for branch,data,ts,expected in [('full',full,times,item['expected']['bocpd']),('PP',pp,times[:720],item['pp_expected'])]:
                progress('BOCPD START '+oid+'/'+branch)
                begin=time.perf_counter(); X=data.to_numpy()
                # Bound trước tính; gồm covariance chọn tại tối đa mọi điểm, +512MiB dự trữ N-Sigma song song.
                upper=2*(len(X)+1)**2*8+len(X)*4*(2*X.shape[1]**2+2*X.shape[1]+4)*8+len(X)*X.shape[1]*8+2**20
                assert used()+upper+512*2**20 < S['budget_bytes'], 'Storage budget before BOCPD case'
                core,arr=observed(X,ts,len(cols),list(data),tick=lambda i:progress(f'BOCPD {oid}/{branch} i={i}/{len(X)}'))
                dest=run/(oid+'--'+branch+'.npz')
                np.savez_compressed(dest,**arr)
                # Giữ native source diagnostics kể cả non-OK; không đổi lỗi thành no-alarm.
                keys=['status','alarms','input_shape','detector_columns','diagnostics']
                keys+=['chi_so'] if expected['status']=='OK' else ['error']
                checks={k:core.get(k)==expected.get(k) for k in keys}
                if args.first:
                    direct,R,mx=plain(X,ts,len(cols),list(data))
                    checks.update({'same_input_'+k:v for k,v in compare_same_input(core,arr,direct,R,mx).items()})
                record={'status':'PASS' if all(checks.values()) else 'FAIL','branch':branch,'result':core,
                        'checks':checks,'npz':dest.name,'sha256':sha(dest),'bytes':dest.stat().st_size,
                        'wall_s':time.perf_counter()-begin,'rss_peak_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                        'theta_points':arr['theta_points'].tolist(),
                        'normalizer_source':'tái tính nguyên biểu thức native từ Rprevious/predprobs/H; posterior tái tính khớp tuyệt đối ngay mỗi bước',
                        'finite_normalization_max_error':float(np.max(np.abs(arr['normalization_error']))) if core['status']=='OK' else None}
                write(run/(oid+'--'+branch+'.json'),record)
                case[branch]=record; status['cases'][oid]=case; write(run/'status.json',status)
                if not all(checks.values()): raise RuntimeError('BOCPD source/native mismatch '+oid+'/'+branch+' '+str(checks))
                if branch=='full':
                    # Kiểm FF native độc lập cùng ma trận full cắt; CP từ full hợp lệ được tái dùng.
                    f,resultR,mx=plain(X[:720],times[:720],len(cols),list(data))
                    ff={'status':f['status'],'native_result':f,'processed_input_equal':True}
                    if core['status']=='OK' and f['status']=='OK':
                        ff['m_prefix_match']=np.array_equal(arr['m'][:720],resultR[:,1:].argmax(axis=0))
                        ff['cp_prefix_match']=[i for i in core['chi_so'] if i<720]==f['chi_so']
                        ff['max_posterior_abs_difference']=float(np.max(np.abs(arr['R'][:721,:721]-resultR)))
                        write(run/(oid+'--FF-check.json'),ff)
                        assert ff['m_prefix_match'] and ff['cp_prefix_match'], 'Fixed processed matrix prefix m/CP mismatch'
                    else:
                        # Full non-OK không có alarms nguồn để ép prefix trùng; prefix native giữ riêng.
                        ff['source_prefix_comparison']='Full non-OK: so native prefix, không so alarms rỗng full'
                        write(run/(oid+'--FF-check.json'),ff)
                    case['FF']=ff
                progress('BOCPD PASS '+oid+'/'+branch+' wall_s='+str(round(record['wall_s'],2)))
            status['resources']={'new_bytes':used(),'disk_free_bytes':shutil.disk_usage(H).free}
            write(run/'status.json',status)
        status['status']='PASS'
    except BaseException as exc:
        status['status']='STOPPED'; status['error']=type(exc).__name__+': '+str(exc)
        traceback.print_exc(); progress('BOCPD STOP '+status['error']); raise
    finally:
        status['wall_s']=time.perf_counter()-t0; status['ended_utc']=datetime.now(timezone.utc).isoformat()
        write(run/'status.json',status)
        write(run/'manifest.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in run.iterdir() if p.is_file() and p.name!='manifest.json'})
        progress('BOCPD '+status['status']+' '+args.run)

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--run',required=True); p.add_argument('--first',action='store_true')
    main(p.parse_args())
