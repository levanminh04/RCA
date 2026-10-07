"""T-031 chẩn đoán thêm (QT5: điểm > 1e6 thì tìm nguyên nhân; không đổi khóa): nút CIRCA có điểm RHT SVR > 1e6.

Với mỗi nút như vậy trong lượt khóa (SVR, hash seed 0): std của y train, std dự đoán SVR trên train, std residual
train của SVR và của OLS, điểm RHT của OLS và của z-score trực tiếp cho cùng nút. Không dùng nhãn, không in thứ hạng.
Chạy với PYTHONHASHSEED=0.

python chan_doan_diem_lon.py <tom-tat lượt khóa SVR h0>
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import chung
from p3 import cua_so
from p3.adapters import circa
from chan_doan_svr import diem


def main(tom):
    from sklearn.linear_model import LinearRegression
    from sklearn.svm import SVR
    from RCAEval.graph_heads.rht import zscore
    assert os.environ.get('PYTHONHASHSEED') == '0'
    al, moc = chung.nap()
    L = chung.Luot('chan-doan-diem-lon', {'tom': tom})
    rows = []
    for r in json.loads(open(tom, encoding='utf-8').read())['luot']:
        kq = json.loads((Path(tom).parent / 'luot' / r['run_id'] / 'ket-qua.json').read_text(encoding='utf-8'))
        nodes = kq['ket_qua_nhieu'][0]['diagnostics']['nodes']
        lon = [n for n, v in nodes.items() if v['rht_score'] > 1e6]
        if not lon:
            continue
        oid = r['opaque_id']
        f = chung.selector.chon_ca(al, oid, chung.ROOT)
        t = moc[oid]
        win, _ = cua_so.cat_ca(pd.read_parquet(f['metrics.parquet']), pd.read_parquet(f['traces.parquet']), None, t)
        clean = circa.chuan_bi(win['metric'])
        graph, _ = circa.do_thi([c for c in clean.columns if c != 'time'], win['traces'], t)
        current = int(clean[clean['time'] >= t]['time'].max())
        s_svr, mg, series, sc, case, byname = diem(clean, graph, t, current, lambda: SVR(kernel='sigmoid'))
        s_ols, *_ = diem(clean, graph, t, current, LinearRegression)
        name2node = {v: k for k, v in byname.items()}
        for n in lon:
            node = name2node[n]
            px, tx, py, ty = sc.split_data(series, node, list(mg.parents(node)), case)
            sv = SVR(kernel='sigmoid').fit(px, py)
            ol = LinearRegression().fit(px, py)
            z0 = np.abs(zscore(train_y=py, test_y=ty))
            rows.append({'opaque_id': oid, 'nut': n, 'so_cha': int(px.shape[1]),
                         'diem_svr_ban_ghi': nodes[n]['rht_score'], 'diem_svr_tinh_lai': s_svr[n], 'diem_ols': s_ols[n],
                         'diem_zscore_truc_tiep': float(z0.max()),
                         'std_y_train': float(np.std(py)), 'so_gia_tri_y_train_khac_nhau': int(len(np.unique(py))),
                         'std_y_test': float(np.std(ty)),
                         'std_du_doan_svr_train': float(np.std(sv.predict(px))),
                         'std_residual_svr_train': float(np.std(py - sv.predict(px))),
                         'std_residual_ols_train': float(np.std(py - ol.predict(px)))})
            L.ghi(json.dumps(rows[-1], ensure_ascii=False))
    doc = {'mo_ta': __doc__.strip(), 'run': L.dir.name, 'nut': rows}
    chung.ghi_json(L.dir / 'chan-doan-diem-lon.json', doc)
    chung.ghi_json(chung.OUT / 'chan-doan-diem-lon.json', doc)
    L.xong({'so_nut': len(rows)})


if __name__ == '__main__':
    main(sys.argv[1])
