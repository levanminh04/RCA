"""Xác minh toàn bộ trung gian lõi từ manifest; không phát lại detector."""
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

H=Path(os.environ['T033_HOME']).resolve()
S=json.loads((H/'inputs/source.json').read_text())
OUT=H/'runs/core-audit-002'
OUT.mkdir(exist_ok=False)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def load(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False))
def progress(s):
    line=datetime.now(timezone.utc).isoformat()+' AUDIT '+s
    print(line,flush=True)
    with (H/'trang-thai.txt').open('a') as f:f.write(line+'\n')

files={}; rows=[]
runs=['nsigma-first-001','nsigma-rest-001','bocpd-first-001','bocpd-first-002','bocpd-rest-001']
try:
    for name in runs:
        run=H/'runs'/name
        manifest=load(run/'manifest.json')
        for rel,expect in manifest.items():
            p=run/rel
            assert p.stat().st_size==expect['bytes'] and sha(p)==expect['sha256'],(name,rel,'hash')
            files[str(p.relative_to(H))]=expect
        status=load(run/'status.json')
        assert status['status']==('STOPPED' if name=='bocpd-first-001' else 'PASS')
    verify=load(H/'runs/full-metadata-recheck-001/verification.json')
    assert verify['status']=='PASS'
    for item in S['cases']:
        oid=item['opaque_id']
        for det in ['nsigma','nsigma_doi_chung']:
            paths=[H/'runs'/name/(oid+'--'+det+'.json') for name in ['nsigma-first-001','nsigma-rest-001']]
            paths=[p for p in paths if p.is_file()];assert len(paths)==1
            p=paths[0];rec=load(p);assert rec['status']=='PASS' and all(rec['checks'].values())
            npz=p.parent/rec['output_npz'];assert sha(npz)==rec['sha256']
            with np.load(npz,allow_pickle=False) as z:
                times=z['times'];flags=z['Z'];evaluated=z['evaluated']
                assert len(times)==1441 and np.all(np.diff(times)==1) and times[720]==item['proxy']
                assert flags.shape==z['x'].shape==z['mean'].shape==z['std'].shape==z['count'].shape
                assert not flags[:100].any() and np.array_equal(evaluated,np.arange(len(times))>=100)
                with np.errstate(all='ignore'):
                    assert np.array_equal(flags[evaluated],(np.abs(z['x']-z['mean'])>3*z['std'])[evaluated])
                assert times[flags.any(axis=1)].astype(int).tolist()==item['expected'][det]['alarms']
            rows.append({'opaque_id':oid,'branch':det,'status':'PASS','record':str(p.relative_to(H)),'npz':str(npz.relative_to(H)),'sha256':rec['sha256']})
        paths=[H/'runs'/name/(oid+'--full.json') for name in ['bocpd-first-002','bocpd-rest-001']]
        paths=[p for p in paths if p.is_file()];assert len(paths)==1
        fullpath=paths[0]; fullrec=load(fullpath)
        for branch,expected in [('full',item['expected']['bocpd']),('PP',item['pp_expected'])]:
            p=fullpath.parent/(oid+'--'+branch+'.json');rec=load(p)
            assert rec['status']=='PASS' and all(rec['checks'].values())
            for field in ['status','alarms','input_shape','detector_columns','diagnostics']:
                assert rec['result'].get(field)==expected.get(field),(oid,branch,field)
            npz=p.parent/rec['npz'];assert sha(npz)==rec['sha256']
            with np.load(npz,allow_pickle=False) as z:
                times=z['times'];X=z['X'];T=len(times)
                assert T==(1441 if branch=='full' else 720) and np.all(np.diff(times)==1)
                assert X.shape==(T,len(z['columns']))
                if rec['result']['status']=='OK':
                    R=z['R'];m=z['m'];flags=z['CP_flags']
                    assert R.shape==(T+1,T+1) and np.isfinite(R).all()
                    assert np.array_equal(m,R[:,1:].argmax(axis=0))
                    assert np.array_equal(m,z['m_online'])
                    assert np.array_equal(flags,np.r_[False,np.abs(np.diff(m))>1])
                    assert np.flatnonzero(flags).tolist()==rec['result']['chi_so']
                    assert times[flags].astype(int).tolist()==rec['result']['alarms']
                    assert np.allclose(R[:,1:].sum(axis=0),1,rtol=1e-12,atol=1e-14)
                    assert np.allclose(R[0,1:],.02,rtol=1e-12,atol=1e-14)
                    assert np.isfinite(z['normalizer']).all() and (z['normalizer']>0).all()
                    assert np.allclose(z['reset_mass']/z['normalizer'],R[0,1:],rtol=1e-12,atol=1e-14)
                    predictive=z['predictive_density']
                    assert predictive.shape==(T,T)
                    for i in range(T):assert np.isfinite(predictive[i,:i+1]).all()
                    for field in ['theta_before_dof','theta_before_kappa','theta_before_mu','theta_before_scale','theta_after_dof','theta_after_kappa','theta_after_mu','theta_after_scale']:
                        for row,parents in zip(z[field],z['theta_parent_indices']):assert np.isfinite(row[parents>=0]).all()
                    cp=set(np.flatnonzero(flags));required={0,T-1 if T==720 else 720,719}|cp|{i-1 for i in cp if i>0}|{i+1 for i in cp if i+1<T}
                    assert required<=set(z['theta_points'].tolist()),(oid,branch,'theta coverage')
                else:assert rec['result']['alarms']==[]
            rows.append({'opaque_id':oid,'branch':branch,'status':'PASS','record':str(p.relative_to(H)),'npz':str(npz.relative_to(H)),'sha256':rec['sha256'],'native_status':rec['result']['status']})
        ff=load(fullpath.parent/(oid+'--FF-check.json'))
        if fullrec['result']['status']=='OK' and ff['status']=='OK':assert ff['m_prefix_match'] and ff['cp_prefix_match']
        progress(oid+' PASS')
    assert len(rows)==120
    write(OUT/'verification.json',{'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'source_sha256':sha(H/'inputs/source.json'),'files':files,'rows':rows,'core_records':120,'nsigma_records':60,'bocpd_full_PP_records':60,'question_closure':False})
    progress('PASS 120 records; source and manifest exact')
except BaseException as exc:
    write(OUT/'verification.json',{'status':'STOPPED','error':repr(exc),'files':files,'rows_completed':rows})
    progress('STOP '+repr(exc));raise
