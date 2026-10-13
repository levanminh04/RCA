"""Ma trận hai yếu tố đã khai SPEC; chỉ gọi sau lõi ca được xác minh."""
import numpy as np
from baro.utility import drop_constant
from p3.adapters.phat_hien import cot_bocpd,tien_xu_ly_bocpd

def matrices(metrics,i_proxy):
    columns=cot_bocpd(metrics.columns)
    raw=metrics[columns]
    prefix=raw.iloc[:i_proxy].copy()
    assert len(prefix)>0
    MF=list(drop_constant(raw).columns)
    MP=list(drop_constant(prefix).columns)
    assert set(MP)<=set(MF)
    filled_full=raw.ffill().fillna(0)
    filled_prefix=prefix.ffill().fillna(0)
    scale={'F':(filled_full.min(),filled_full.max()),
           'P':(filled_prefix.min(),filled_prefix.max())}
    mats={}; metadata={}
    for branch,mask,s in [('FF',MF,'F'),('FP',MF,'P'),('PF',MP,'F'),('PP',MP,'P')]:
        lo,hi=scale[s]
        result=filled_prefix[mask].copy()
        for c in mask:
            # Nguyên biểu thức native; range0/Inf giữ chia→NaN→ffill/fill0.
            result[c]=(result[c]-lo[c])/(hi[c]-lo[c])
        result=result.ffill().fillna(0)
        mats[branch]=result
        metadata[branch]={'mask_source':branch[0],'scale_source':s,'columns':mask,
                          'd':len(mask),'native_prior_dof':len(mask)+1,'native_prior_kappa':1,
                          'range0_columns':[c for c in mask if hi[c]-lo[c]==0],
                          'nonfinite_raw_prefix_cells':int((~np.isfinite(prefix[mask].to_numpy())).sum()),
                          'nonfinite_processed_cells':int((~np.isfinite(result.to_numpy())).sum()),
                          'no_input_channels':len(mask)==0,
                          'source_still_lookahead':'full' if s=='F' or branch[0]=='F' else 'within-prefix'}
    nativefull=tien_xu_ly_bocpd(raw).iloc[:i_proxy].copy()
    nativeprefix=tien_xu_ly_bocpd(prefix)
    for b,native in [('FF',nativefull),('PP',nativeprefix)]:
        assert list(mats[b])==list(native)
        assert np.array_equal(mats[b].to_numpy(),native.to_numpy(),equal_nan=True), 'Native diagonal input mismatch '+b
    # Contrast scale không đổi mask/d/prior; contrast gói giữ scale cột chung.
    for a,b in [('FF','FP'),('PF','PP')]:
        assert list(mats[a])==list(mats[b])
    return mats,metadata

def contrast(a,b):
    if a['result']['status']!='OK' or b['result']['status']!='OK':
        return {'defined':False,'reason':'Native non-OK; không gán zero contrast'}
    # `m` và CP_flags là output thời gian cùng lưới, không là score onset thật.
    am=np.asarray(a['m'],dtype=int); bm=np.asarray(b['m'],dtype=int)
    af=np.asarray(a['CP_flags'],dtype=int); bf=np.asarray(b['CP_flags'],dtype=int)
    assert len(am)==len(bm) and len(af)==len(bf)==len(am)
    ac=set(a['result']['chi_so']); bc=set(b['result']['chi_so'])
    return {'defined':True,'signed_m_difference':(am-bm).tolist(),
            'signed_CP_flag_difference':(af-bf).tolist(),
            'CP_added_a_vs_b':sorted(ac-bc),'CP_lost_a_vs_b':sorted(bc-ac),
            'signed_CP_count_difference':len(ac)-len(bc)}
