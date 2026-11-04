"""Chẩn đoán chỉ hai đơn vị lệch T1 và counterpart; không sửa src hoặc đọc nhãn chấm."""
import hashlib
import json
import math
import random
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq
import adapter_t047 as ad
from m1 import cong,runner
from p3 import selector,nhan


def main():
    output=ad.OUT/'runs/t1-xao-dieu-tra-001'
    output.mkdir(parents=True,exist_ok=False)
    allow=selector.nap_allowlist(ad.ROOT/'results/T-022/allowlist-dev.json')
    tmap=nhan.nap_moc(ad.ROOT/'results/T-022/nhan-dev.json')
    rows=[]
    col='ts-admin-travel-service_latency-90';ma='metric|'+col
    for oid in ('dev-98bc73c499','dev-ba831dbeb8','dev-03d4910932'):
        files=selector.chon_ca(allow,oid,ad.ROOT,tep=['metrics.parquet'])
        frame=pq.read_table(files['metrics.parquet'],columns=['time',col]).to_pandas()
        t=tmap[oid];m=frame.loc[(frame['time']>=t-300)&(frame['time']<t+300)].reset_index(drop=True)
        tt=m['time'].to_numpy();vv=m[col].to_numpy()
        summary=json.loads((ad.OUT/'runs/b2-t1-seed0-001/cases'/oid/'summary.json').read_text(encoding='utf-8'))
        diag=summary['adapter'];rng=random.Random(0)
        dummy=list(range(diag['span_trong_mien']));rng.shuffle(dummy)
        dummy=list(range(diag['dong_log_trong_mien']));rng.shuffle(dummy)
        order=list(range(len(m)));rng.shuffle(order)
        versions={}
        for name,idx in [('original',list(range(len(m)))),('shuffled',order),('sorted_shuffled',sorted(order,key=lambda i:tt[i]))]:
            N=[float(vv[i]) for i in idx if tt[i]<t and math.isfinite(vv[i])]
            A=[float(vv[i]) for i in idx if tt[i]>=t and math.isfinite(vv[i])]
            mn=[int(tt[i])*10**9 for i in idx if tt[i]<t and math.isfinite(vv[i])]
            maA=[int(tt[i])*10**9 for i in idx if tt[i]>=t and math.isfinite(vv[i])]
            rec=json.loads((ad.OUT/'runs/b2-t1-seed0-001/cases'/oid/'phase1/records/00000.json').read_text(encoding='utf-8'))
            bounds=cong.bien_phia(rec['coverage']['metric'],t*10**9)
            one=cong.o_1s(mn,N,t*10**9,'N');rho,reason=cong.tu_tuong_quan(one)
            kb=cong.chuan_bi_khoi(N,mn,A,maA,t*10**9,*bounds)
            x=np.array(list(one.values()),float)
            p,cach=cong.p_theo_G3(N,mn,A,maA,t*10**9,*bounds,'len',runner.TS_HOP_DONG,ma)
            versions[name]=dict(N=N,A=A,mocN=mn,mocA=maA,ordered_seconds=list(one),one_second_values=list(one.values()),
                unique_N=sorted(set(N)),unique_1s=sorted(set(one.values())),
                mean_np=float(x.mean()),var_np=float(((x-x.mean())**2).mean()),mean_fsum=math.fsum(x)/len(x),
                rho=rho,rho_reason=reason,b=kb.get('b'),fallback=kb.get('roi_G0'),
                n_blocksN=len(kb.get('khoi_N',{})),n_blocksA=len(kb.get('khoi_A',{})),p=p,cach=cach,
                saved_p=next(u['p_len'] for u in rec['extra']['don_vi_phan_vi'] if u['ma']==ma))
        record=dict(oid=oid,unit=ma,raw_sha256=allow[oid]['files']['metrics.parquet']['sha256'],versions=versions)
        ad.ghi(output/(oid+'.json'),record)
        rows.append(dict(oid=oid,versions={k:{z:v[z] for z in ('unique_N','unique_1s','mean_np','var_np','mean_fsum','b','n_blocksN','n_blocksA','p','saved_p')}
                                        for k,v in versions.items()}))
    ad.ghi(output/'summary.json',rows)
    print(json.dumps(rows,ensure_ascii=False,indent=1))


if __name__=='__main__':main()
