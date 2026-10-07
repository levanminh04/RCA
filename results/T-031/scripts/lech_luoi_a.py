"""T-031 bước 4: lệch lưới nguồn A (dữ liệu torai-TT tác giả) ở 30 ca, không chạy TORAI, không dùng nhãn.

Dùng đúng `p3.adapters.torai.chuan_bi_A` (cắt 20 dòng mỗi phía theo time < t) trên `logts.csv` tác giả và cửa sổ
metric; ghi lệch giữa bin tác giả đầu tiên ≥ t và t, phạm vi N, A mà 20 bin phủ (tương đối với t), và kiểm lưới
`tracets_err`, `tracets_lat` trùng lưới `logts`. Báo theo mã mờ.

python lech_luoi_a.py
"""
import numpy as np
import pandas as pd

import chung
from p3 import cua_so
from p3.adapters import torai
from p3.runner import _tac_gia_A


def main():
    al, moc = chung.nap()
    L = chung.Luot('lech-luoi-a')
    rows = []
    for oid in sorted(al):
        t = moc[oid]
        f = chung.selector.chon_ca(al, oid, chung.ROOT, tep=['metrics.parquet'])
        a = _tac_gia_A(al[oid]['case_dir'])
        lt, te, tl = (pd.read_csv(a[k]) for k in ('logts', 'tracets_err', 'tracets_lat'))
        m = cua_so.cat_metric(pd.read_parquet(f['metrics.parquet']), t)
        _, lt20, te20, tl20, info = torai.chuan_bi_A(m, lt, te, tl, t)
        rel = lambda x: None if x is None else [x[0] - t, x[1] - t]
        r = {'opaque_id': oid, 'lech_luoi_s': info['lech_luoi_s'], 'N_phu_tuong_doi': rel(info['N_phu']),
             'A_phu_tuong_doi': rel(info['A_phu']), 'so_dong_20': [int(len(lt20)), int(len(te20)), int(len(tl20))],
             'luoi_trace_trung_log': bool(np.array_equal(lt['time'].to_numpy('int64'), te['time'].to_numpy('int64'))
                                          and np.array_equal(lt['time'].to_numpy('int64'), tl['time'].to_numpy('int64'))),
             'buoc_luoi_s': sorted(set(lt['time'].diff().dropna().astype(int)))}
        rows.append(r)
        L.ghi(f'{oid} lech={r["lech_luoi_s"]} N={r["N_phu_tuong_doi"]} A={r["A_phu_tuong_doi"]}')
    phan_bo = {}
    for r in rows:
        phan_bo[r['lech_luoi_s']] = phan_bo.get(r['lech_luoi_s'], 0) + 1
    doc = {'mo_ta': __doc__.strip(), 'run': L.dir.name, 'phan_bo_lech_s': phan_bo, 'ca': rows}
    chung.ghi_json(L.dir / 'lech-luoi-a.json', doc)
    L.xong({'phan_bo_lech_s': phan_bo})


if __name__ == '__main__':
    main()
