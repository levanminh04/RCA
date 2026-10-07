"""T-031 chẩn đoán thêm (sau khi đã khóa SVR; không đổi khóa): SVR(sigmoid) có hồi quy thật theo cha không.

LESSONS SL36, QT5: soi giá trị trung gian và so với bản bỏ thành phần. Trên các ca pilot CIRCA, với mỗi nút có cha
hiệu lực: tỉ số std(dự đoán trên train)/std(y train) của SVR và của OLS (gần 0 = dự đoán gần hằng, residual ≈ y).
So điểm RHT của SVR với điểm RHT của OLS và với z-score trực tiếp (không hồi quy) trên mọi nút: tương quan hạng
Spearman và độ trùng top-10 nút. Không dùng nhãn, không in thứ hạng. Chạy với PYTHONHASHSEED=0 (cùng đồ thị lượt khóa).

python chan_doan_svr.py <oid,oid,...> <tom-tat lượt khóa SVR h0>
"""
import json
import os
import sys
from datetime import timedelta

import networkx as nx
import numpy as np
import pandas as pd

import chung
from p3 import cua_so
from p3.adapters import circa


def diem(frame, graph, t, current, regressor):
    from RCAEval.classes.graph import Node, MemoryGraph
    from RCAEval.classes.data import CaseData, MemoryDataLoader
    from RCAEval.graph_heads.rht import RHTScorer, ANMRegressor
    from circa_kien_truc.builder import metric_mapping
    mapped = {r['column']: r for r in metric_mapping(graph.nodes)}
    nodes = {n: Node(mapped[n]['service'], mapped[n]['metric']) for n in graph.nodes}
    g = nx.DiGraph(); g.add_nodes_from(nodes.values()); g.add_edges_from((nodes[a], nodes[b]) for a, b in graph.edges)
    mg = MemoryGraph(g); byname = {v: k for k, v in nodes.items()}
    raw = {}
    for n, node in nodes.items():
        raw.setdefault(node.entity, {})[node.metric] = list(zip(frame.time, frame[n]))
    case = CaseData(MemoryDataLoader(raw), sli=nodes[sorted(nodes)[0]], detect_time=t, interval=timedelta(seconds=1))
    series = case.load_data(mg, current)
    sc = RHTScorer(regressor=ANMRegressor(regressor=regressor()) if regressor else None)
    out = {byname[n]: float(s.score) for n, s in sc.score(mg, case, current).items()}
    return out, mg, series, sc, case, byname


def main(ids, tom_khoa):
    from scipy.stats import spearmanr
    from sklearn.linear_model import LinearRegression
    from sklearn.svm import SVR
    assert os.environ.get('PYTHONHASHSEED') == '0'
    al, moc = chung.nap()
    L = chung.Luot('chan-doan-svr', {'ca': ids, 'tom_khoa': tom_khoa})
    luot = {r['opaque_id']: r['run_id'] for r in json.loads(open(tom_khoa, encoding='utf-8').read())['luot']}
    res = {}
    for oid in ids:
        f = chung.selector.chon_ca(al, oid, chung.ROOT)
        t = moc[oid]
        win, _ = cua_so.cat_ca(pd.read_parquet(f['metrics.parquet']), pd.read_parquet(f['traces.parquet']), None, t)
        clean = circa.chuan_bi(win['metric'])
        graph, _ = circa.do_thi([c for c in clean.columns if c != 'time'], win['traces'], t)
        current = int(clean[clean['time'] >= t]['time'].max())
        s_svr, mg, series, sc, case, byname = diem(clean, graph, t, current, lambda: SVR(kernel='sigmoid'))
        s_ols, *_ = diem(clean, graph, t, current, LinearRegression)
        ratio_svr, ratio_ols = [], []
        for node in series:
            parents = list(mg.parents(node))
            px, tx, py, ty = sc.split_data(series, node, parents, case)
            if len(px) == 0 or np.std(py) == 0:
                continue
            ratio_svr.append(float(np.std(SVR(kernel='sigmoid').fit(px, py).predict(px)) / np.std(py)))
            ratio_ols.append(float(np.std(LinearRegression().fit(px, py).predict(px)) / np.std(py)))
        # z-score trực tiếp: RHT với nút coi như không cha (regressor không dùng khi px rỗng)
        from RCAEval.graph_heads.rht import zscore
        s_z = {}
        for node in series:
            px, tx, py, ty = sc.split_data(series, node, [], case)
            z = np.abs(zscore(train_y=py, test_y=ty))
            s_z[byname[node]] = float(np.max(z)) if len(z) else float('nan')
        ks = sorted(s_svr)
        from pathlib import Path
        khop = None
        for bg in sorted((Path(tom_khoa).parent / 'luot' / luot[oid]).glob('ban-ghi-*.json')):
            r = json.loads(bg.read_text(encoding='utf-8'))
            if r['variant'] == 'svr+rht':
                rk = {x['item']: x['key'][0] for x in r['ranking']}
                khop = max(abs(rk[k] - s_svr[k]) for k in ks) if set(rk) == set(ks) else 'tap_nut_khac'

        def sp(a, b):
            x, y = np.array([a[k] for k in ks]), np.array([b[k] for k in ks])
            m = np.isfinite(x) & np.isfinite(y)
            return float(spearmanr(x[m], y[m]).correlation)

        def top(a, b, k=10):
            ta = set(sorted(ks, key=lambda n: -a[n])[:k]); tb = set(sorted(ks, key=lambda n: -b[n])[:k])
            return len(ta & tb)
        q = lambda v: [float(np.quantile(v, x)) for x in (0, 0.25, 0.5, 0.75, 1)] if v else None
        res[oid] = {'so_nut': len(ks), 'so_nut_co_cha_va_y_khong_hang': len(ratio_svr),
                    'ty_so_std_du_doan_svr_q0_25_50_75_100': q(ratio_svr),
                    'ty_so_std_du_doan_ols_q0_25_50_75_100': q(ratio_ols),
                    'svr_du_doan_gan_hang_lt_0.01': sum(r < 0.01 for r in ratio_svr),
                    'spearman_svr_ols': sp(s_svr, s_ols), 'spearman_svr_zscore': sp(s_svr, s_z),
                    'spearman_ols_zscore': sp(s_ols, s_z),
                    'top10_trung_svr_ols': top(s_svr, s_ols), 'top10_trung_svr_zscore': top(s_svr, s_z),
                    'top10_trung_ols_zscore': top(s_ols, s_z),
                    'diem_svr_lech_max_so_voi_ban_ghi_khoa': khop}
        L.ghi(f'{oid}: {json.dumps(res[oid])}')
    doc = {'mo_ta': __doc__.strip(), 'run': L.dir.name, 'ket_qua': res}
    chung.ghi_json(L.dir / 'chan-doan-svr.json', doc)
    chung.ghi_json(chung.OUT / 'chan-doan-svr.json', doc)
    L.xong({'so_ca': len(res)})


if __name__ == '__main__':
    main(sys.argv[1].split(','), sys.argv[2])
