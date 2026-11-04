"""CANDIDATE chưa duyệt tích hợp: thứ tự chuẩn trong o_1s/tu_tuong_quan.

Không gắn vào M1, không dùng chọn K; chỉ chẩn đoán và test. Không thêm epsilon,
không đổi công thức/giới hạn/rơi G0 của G3.
"""
import numpy as np
from m1 import cong


def o_1s(moc_ns,gia_tri,t_ns,phia):
    samples={}
    for x,v in zip(moc_ns,gia_tri):
        if phia=='N':
            if x>=t_ns:raise ValueError('mẫu N có mốc >= t')
            j=(t_ns-x-1)//cong.NS
        else:
            if x<t_ns:raise ValueError('mẫu A có mốc < t')
            j=(x-t_ns)//cong.NS
        if j>=cong.W:continue
        samples.setdefault(j,[]).append(float(v))
    return {j:sum(sorted(samples[j]))/len(samples[j]) for j in sorted(samples,reverse=True)}


def tu_tuong_quan(o):
    if len(o)<cong.CAP_TOI_THIEU:return None,'it_o'
    order=sorted(o,reverse=True)
    x=np.array([o[j] for j in order],float)
    m=float(x.mean());v=float(((x-m)**2).mean())
    if v<=0:return None,'phuong_sai_0'
    rho={}
    for k in range(1,cong.K_MAX+1):
        pairs=[(o[j]-m)*(o[j+k]-m) for j in order if j+k in o]
        rho[k]=(sum(pairs)/len(pairs))/v if len(pairs)>=cong.CAP_TOI_THIEU else None
    return rho,None
