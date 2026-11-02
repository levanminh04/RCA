"""T-046 bước 3 bổ sung bản 3 (chỉ báo cáo; thêm 14:10 sau khi xem chan-doan-cong-ban3.json): cấu trúc thời gian của
chuỗi metric RE2-TT trong N = [t − 300, t) của 30 ca dev, để phân biệt chuỗi dừng tự tương quan (AR) với chuỗi không
dừng (kiểu bước ngẫu nhiên, giữ giá trị). Không đọc nhãn; chỉ dữ liệu trước mốc tiêm.

Theo từng cột metric có ít nhất 200 giây có giá trị và phương sai > 0 (lưới 1 giây, `metrics.time`):
- ty_le_giu: tỷ lệ giây có giá trị bằng đúng giây trước (dấu hiệu lấy mẫu rồi giữ);
- rho1: tự tương quan bậc 1 (như cong.tu_tuong_quan);
- VR60: tỷ số phương sai var(x_{s+60} − x_s) / (60·var(x_{s+1} − x_s)). Bước ngẫu nhiên cho khoảng 1; AR(1) dừng φ = 0,94
  cho khoảng (1 − 0,94^60)/(60·0,06) ≈ 0,27; nhiễu trắng cho 1/60;
- chenh_nua: |trung bình nửa sau − nửa đầu| / độ lệch chuẩn trong nửa (gộp), so với mức của AR(1) cùng ρ1.
Gộp theo hậu tố kênh (cpu, mem, …): trung vị, tứ phân vị.

Chạy: $PY -B results/T-046/scripts/b3c_cau_truc_metric.py --ra results/T-046/cau-truc-metric-re2.json
"""
import argparse
import json
import statistics
from pathlib import Path

import numpy as np

import cong
import t046

NS = t046.NS


def mot_cot(x):
    """x: mảng giá trị theo giây (NaN là thiếu), thứ tự thời gian."""
    ok = ~np.isnan(x)
    if ok.sum() < 200:
        return None
    v = x[ok]
    if float(np.var(v)) <= 0:
        return None
    cap = ok[1:] & ok[:-1]
    giu = float(np.mean(x[1:][cap] == x[:-1][cap])) if cap.any() else None
    o = {j: float(x[j]) for j in range(len(x)) if ok[j]}
    rho, _ = cong.tu_tuong_quan(o)
    d1 = x[1:] - x[:-1]
    d60 = x[60:] - x[:-60]
    d1, d60 = d1[~np.isnan(d1)], d60[~np.isnan(d60)]
    vr = float(np.var(d60) / (60 * np.var(d1))) if len(d1) > 10 and len(d60) > 10 and np.var(d1) > 0 else None
    n = len(x) // 2
    a, b = x[:n][~np.isnan(x[:n])], x[n:][~np.isnan(x[n:])]
    sd = float(np.sqrt((np.var(a) + np.var(b)) / 2)) if len(a) > 1 and len(b) > 1 else 0.0
    ch = float(abs(b.mean() - a.mean()) / sd) if sd > 0 else None
    return {'ty_le_giu': giu, 'rho1': rho.get(1) if rho else None, 'VR60': vr, 'chenh_nua': ch}


def tom(ds):
    ds = [x for x in ds if x is not None]
    if not ds:
        return None
    q = statistics.quantiles(ds, n=4) if len(ds) >= 4 else [None, None, None]
    return {'n': len(ds), 'trung_vi': round(statistics.median(ds), 4),
            'tu_phan_vi': [round(q[0], 4), round(q[2], 4)] if q[0] is not None else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    mt = t046.moi_truong()
    theo = {}
    for oid in sorted(mt['re']):
        ca, t, _ = t046.nap('RE2-TT', oid, 'that', mt)
        cols = sorted({k for r in ca['metrics'] for k in r if k != 'time'})
        x = {c: np.full(300, np.nan) for c in cols}
        for r in ca['metrics']:
            j = int(r['time']) - (t - 300)
            if 0 <= j < 300:
                for c in cols:
                    v = r.get(c)
                    if v is not None:
                        x[c][j] = v
        for c in cols:
            kq = mot_cot(x[c])
            if kq is None:
                continue
            hau_to = c.split('_', 1)[1]
            theo.setdefault(hau_to, []).append(kq)
    out = {}
    for h, ds in sorted(theo.items(), key=lambda z: -len(z[1])):
        out[h] = {k: tom([d[k] for d in ds]) for k in ('ty_le_giu', 'rho1', 'VR60', 'chenh_nua')}
    tat_ca = [d for ds in theo.values() for d in ds]
    out['_tat_ca'] = {k: tom([d[k] for d in tat_ca]) for k in ('ty_le_giu', 'rho1', 'VR60', 'chenh_nua')}
    Path(a.ra).write_bytes((json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    for h, r in out.items():
        print(h, json.dumps(r, ensure_ascii=False))


if __name__ == '__main__':
    main()
