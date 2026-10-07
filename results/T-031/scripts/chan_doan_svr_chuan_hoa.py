"""T-031 chẩn đoán nguyên nhân SVR(sigmoid) cho dự đoán gần hằng (không đổi khóa, không dùng nhãn).

Giả thuyết: kernel sigmoid bão hòa vì metric RE2-TT có độ lớn rất khác nhau và không được chuẩn hóa.
Kiểm trên 3 ca pilot CIRCA, mọi nút có cha và y train không hằng: (a) SVR trên dữ liệu gốc (như lượt khóa);
(b) SVR sau khi chuẩn hóa X, y bằng mean/std của train (chỉ để chẩn đoán). Đo tỉ lệ std(dự đoán)/std(y),
và độ lớn của X·X' (đầu vào của tanh trong kernel sigmoid, gamma='scale') ở hai trường hợp.

python chan_doan_svr_chuan_hoa.py <oid,oid,...>
"""
import os
import sys

import numpy as np
import pandas as pd

import chung
from p3 import cua_so
from p3.adapters import circa
from chan_doan_svr import diem


def main(ids):
    from sklearn.svm import SVR
    from sklearn.linear_model import LinearRegression
    assert os.environ.get('PYTHONHASHSEED') == '0'
    al, moc = chung.nap()
    L = chung.Luot('chan-doan-svr-chuan-hoa', {'ca': ids})
    res = {}
    for oid in ids:
        f = chung.selector.chon_ca(al, oid, chung.ROOT)
        t = moc[oid]
        win, _ = cua_so.cat_ca(pd.read_parquet(f['metrics.parquet']), pd.read_parquet(f['traces.parquet']), None, t)
        clean = circa.chuan_bi(win['metric'])
        graph, _ = circa.do_thi([c for c in clean.columns if c != 'time'], win['traces'], t)
        current = int(clean[clean['time'] >= t]['time'].max())
        _, mg, series, sc, case, byname = diem(clean, graph, t, current, LinearRegression)
        goc, chuan, ols, kgoc, kchuan = [], [], [], [], []
        for node in series:
            px, tx, py, ty = sc.split_data(series, node, list(mg.parents(node)), case)
            if len(px) == 0 or np.std(py) == 0:
                continue
            s = SVR(kernel='sigmoid')
            goc.append(float(np.std(s.fit(px, py).predict(px)) / np.std(py)))
            g = 1.0 / (px.shape[1] * px.var()) if px.var() > 0 else 1.0
            kgoc.append(float(np.median(np.abs(g * px @ px.T))))
            mx, sx = px.mean(0), px.std(0); sx[sx == 0] = 1
            X = (px - mx) / sx; Y = (py - py.mean()) / py.std()
            chuan.append(float(np.std(SVR(kernel='sigmoid').fit(X, Y).predict(X)) / np.std(Y)))
            g2 = 1.0 / (X.shape[1] * X.var()) if X.var() > 0 else 1.0
            kchuan.append(float(np.median(np.abs(g2 * X @ X.T))))
            ols.append(float(np.std(LinearRegression().fit(px, py).predict(px)) / np.std(py)))
        q = lambda v: [round(float(np.quantile(v, x)), 6) for x in (0.25, 0.5, 0.75)]
        res[oid] = {'so_nut': len(goc), 'svr_goc_lt_0.01': sum(v < 0.01 for v in goc),
                    'svr_chuan_hoa_lt_0.01': sum(v < 0.01 for v in chuan),
                    'ty_so_svr_goc_q25_50_75': q(goc), 'ty_so_svr_chuan_hoa_q25_50_75': q(chuan),
                    'ty_so_ols_q25_50_75': q(ols),
                    'trung_vi_abs_gamma_XXt_goc': q(kgoc), 'trung_vi_abs_gamma_XXt_chuan_hoa': q(kchuan)}
        L.ghi(f'{oid}: {res[oid]}')
    chung.ghi_json(L.dir / 'chan-doan-svr-chuan-hoa.json', {'mo_ta': __doc__.strip(), 'ket_qua': res})
    chung.ghi_json(chung.OUT / 'chan-doan-svr-chuan-hoa.json', {'mo_ta': __doc__.strip(), 'run': L.dir.name, 'ket_qua': res})
    L.xong({'so_ca': len(res)})


if __name__ == '__main__':
    main(sys.argv[1].split(','))
