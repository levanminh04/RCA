"""V5: independent scalar calculations of N1-N4, B1/B4; evaluate after step5."""
import json
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'results/T-029'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def check(rows):
    from p3.selector import nap_allowlist, chon_ca
    from p3.adapters.phat_hien import cot_bocpd
    from baro.utility import drop_constant
    al=nap_allowlist(ROOT/'results/T-022/allowlist-dev.json')
    nm=read(OUT/'runs/nsigma-002/manifest.json')
    differences=[]; details=[]
    def equal(key, actual, expected):
        details.append({'field':key,'equal':actual==expected})
        if actual!=expected: differences.append({'field':key,'independent':actual,'primary':expected})
    assert len(rows)==90 and len({(r['opaque_id'],r['detector']) for r in rows})==90
    for row in rows:
        oid,det=row['opaque_id'],row['detector']
        f=read(ROOT/row['feature_source']['path'])
        primary=row['flags_flat']
        assert sha(ROOT/row['feature_source']['path'])==row['feature_source']['sha256']
        paths=chon_ca(al,oid,ROOT,kiem_hash=True,tep=['metrics.parquet'])
        raw=pd.read_parquet(paths['metrics.parquet'])
        key=oid+'/'+det+'/'
        if det!='bocpd':
            src=nm['cases'][oid]['bo'][det]; assert sha(ROOT/src['npz'])==src['sha256']
            with np.load(ROOT/src['npz'],allow_pickle=False) as zfile:
                z=zfile['Z'].copy(); cols=zfile['columns'].tolist()
            firsts=np.where(np.sum(z,axis=1)>0)[0]; th=int(firsts[0]) if len(firsts) else None
            d=z.shape[1]
            h=sum(int(x) for x in z[100:200].ravel())/(100*d)
            t=sum(int(x) for x in z[400:720].ravel())/(320*d)
            for k in (1.5,2.,3.):
                equal(key+'N1/'+str(k),th is not None and th<200 and h>=k*t,primary['N1/'+str(k)])
                equal(key+'N1/feature/'+str(k),primary['N1/'+str(k)],f['N1'][str(k)])
            triggered=[j for j in range(d) if th is not None and z[th,j]]
            for k in (5,10,20):
                dense=any(sum(bool(x) for x in z[100:720,j])/620>k*.0027 for j in triggered)
                equal(key+'N2/'+str(k),dense,primary['N2/'+str(k)])
                equal(key+'N3/'+str(k),th is not None and th<720 and not dense,primary['N3/'+str(k)])
                equal(key+'N2/feature/'+str(k),primary['N2/'+str(k)],f['N2'][str(k)])
                equal(key+'N3/feature/'+str(k),primary['N3/'+str(k)],f['N3'][str(k)])
            dd=raw[cols].replace([np.inf,-np.inf],np.nan).ffill()
            zero=False
            for j in triggered:
                x=dd.iloc[:th,j].dropna().to_numpy()
                zero=zero or (len(x)>1 and float(np.std(x,ddof=1))==0)
            equal(key+'N4',bool(zero),primary['N4'])
            equal(key+'N4/feature',primary['N4'],f['N4'])
            equal(key+'B1_not_applicable',primary['B1'],None)
            for w in (15,30,60):
                for k in (2,3,5): equal(key+f'B4/w{w}/k{k}_not_applicable',primary[f'B4/w{w}/k{k}'],None)
        else:
            kept=drop_constant(raw[cot_bocpd(raw.columns)])
            th=f['t_hat_index']
            valid=th is not None and 3<=th<=717
            ends=[]
            for c in kept:
                present=[i for i,v in enumerate(kept[c].notna()) if v]
                if present and present[0]>0: ends.append(present[0])
            flag=any(abs(i-th)<=2 for i in ends) if valid else None
            equal(key+'B1',flag,primary['B1'])
            equal(key+'B1/feature',primary['B1'],f['B1_t_hat']['flag'])
            for n in ('N1','N2','N3','N4'):
                levels=(1.5,2.,3.) if n=='N1' else (5,10,20)
                if n=='N4': equal(key+'N4_not_applicable',primary['N4'],None)
                else:
                    for k in levels: equal(key+n+'/'+str(k)+'_not_applicable',primary[n+'/'+str(k)],None)
            filled=kept.ffill().fillna(0)
            for w in (15,30,60):
                ok=th is not None and 1+w+30<=th<=720-w
                maximum=None
                if ok:
                    ratios=[]
                    for c in filled:
                        x=filled[c].to_numpy()
                        background=x[1:th-w]
                        median=float(np.median(background))
                        mad=float(np.median([abs(v-median) for v in background]))
                        if mad>0:
                            jump=abs(float(np.median(x[th:th+w]))-float(np.median(x[th-w:th])))
                            ratios.append(jump/(1.4826*mad))
                    maximum=max(ratios) if ratios else None
                for k in (2,3,5):
                    actual=None if not ok else maximum is not None and maximum>=k
                    equal(key+f'B4/w{w}/k{k}',actual,primary[f'B4/w{w}/k{k}'])
                    equal(key+f'B4/w{w}/k{k}/feature',primary[f'B4/w{w}/k{k}'],f['B4_t_hat'][str(w)]['flags'][str(k)])
    return {'status':'PASS' if not differences else 'FAIL','rows_checked':len(rows),
            'comparisons':len(details),'mismatch_count':len(differences),'differences':differences,
            'details':details,'independence':'No calls to nsigma_flags or bocpd_features; raw std and scalar median/MAD recalculated.',
            'script_sha256':sha(__file__)}

if __name__=='__main__':
    import sys
    rows=read(OUT/'theo-ca.json')['rows']
    result=check(rows)
    path=OUT/'runs/step5-001/V5.json'
    assert not path.exists()
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','rows_checked','comparisons','mismatch_count')}))
    sys.exit(0 if result['status']=='PASS' else 1)
