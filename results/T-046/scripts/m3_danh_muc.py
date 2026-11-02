"""T-046 Phần M3 (kiểm không nhãn của danh mục metric; `danh-muc-metric.md`). Không đọc nhãn, không tính MRR.

(a) Mức trùng giữa kênh bị bỏ và kênh giữ cùng thực thể: hệ số tương quan hạng Spearman.
    - RE2-TT: trên N = [t − 300, t) của cửa sổ thật (trước mốc tiêm), lưới 1 giây.
    - Nezha-OB: trên cả miền [t − 300, t + 300), vì N chỉ có 5 điểm. Phần A có lỗi, nên đây là tương quan
      trong cửa sổ có lỗi; ghi giới hạn.
(b) Theo loại kênh (hậu tố) và hướng, ở A/A R0 (bảng b3 truyền vào): số phép hợp lệ, tỷ lệ qua cổng G0, G3.
(c) Số đơn vị metric hợp lệ mỗi cửa sổ thật R0: toàn bộ so với danh mục.

(d) Qua cổng G3 ở C-e theo loại kênh, từ kết quả sau khóa (chỉ RE2-TT có C-e).

Chạy: $PY -B results/T-046/scripts/m3_danh_muc.py --b3 results/T-046/runs/b3-sua2-aa-001
      --kiem-ce results/T-046/kiem-sau-khoa-sua2.json --ra results/T-046/danh-muc-metric-m3-sua2.json
"""
import argparse
import json
import statistics
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

import t046
from t046 import wilson

BO = {'RE2-TT': {'latency-50': 'latency-90'},
      'Nezha-OB': {'CpuUsage-m': 'CpuUsageRate-pct', 'MemoryUsage-Mi': 'MemoryUsageRate-pct',
                   'PodServerLatencyP95-s': 'PodServerLatencyP90-s', 'PodServerLatencyP99-s': 'PodServerLatencyP90-s',
                   'PodClientLatencyP90-s': 'PodServerLatencyP90-s', 'PodClientLatencyP95-s': 'PodServerLatencyP90-s',
                   'PodClientLatencyP99-s': 'PodServerLatencyP90-s'}}
GIU_SAU_M3 = 'PodClientLatencyP90-s'  # danh mục hiện tại giữ lại kênh này (sửa 19:20)
ALPHA = 0.01


def tuong_quan(mt):
    out = {}
    for ds, oids in (('RE2-TT', sorted(mt['re'])), ('Nezha-OB', sorted(mt['nz']))):
        for oid in oids:
            ca, t, _ = t046.nap(ds, oid, 'that', mt)
            he = 1 if ds == 'RE2-TT' else 10 ** 9
            lo, hi = (t - 300, t) if ds == 'RE2-TT' else (t - 300, t + 300)
            rows = [r for r in ca['metrics'] if lo <= r['time'] / he < hi]
            cols = {k for r in rows for k in r if k != 'time'}
            for c in cols:
                e, duoi = c.split('_', 1)
                if duoi not in BO[ds]:
                    continue
                c2 = f'{e}_{BO[ds][duoi]}'
                if c2 not in cols:
                    continue
                x = np.array([(r.get(c), r.get(c2)) for r in rows], dtype=float)
                x = x[~np.isnan(x).any(axis=1)]
                if len(x) < 5 or np.std(x[:, 0]) == 0 or np.std(x[:, 1]) == 0:
                    continue
                rho = spearmanr(x[:, 0], x[:, 1]).correlation
                k = f'{ds}|{duoi}~{BO[ds][duoi]}'
                if np.isfinite(rho):
                    out.setdefault(k, []).append(float(rho))
                else:  # một kênh hằng sau khi bỏ NaN theo cặp: đếm riêng
                    out.setdefault(k + '|khong_tinh_duoc', []).append(0.0)
    return {k: {'n': len(v), 'trung_vi': round(statistics.median(v), 4),
                'tu_phan_vi': [round(q, 4) for q in statistics.quantiles(v, n=4)[::2]] if len(v) >= 4 else None}
            for k, v in sorted(out.items())}


def theo_hau_to(b3):
    ca = t046.nap_luot(b3)
    q, dem = {}, {}
    for oid, x in ca.items():
        ds = x['dataset']
        for u in x['cua_so']['aa|R0']['bang']['pv']:
            if not (u['hop_le'] and u['trong_U']) or u['nhom'] != 'metric':
                continue
            duoi = u['ma'].split('|', 1)[1].split('_', 1)[1]
            for d, h in u['huong'].items():
                o = q.setdefault(f'{ds}|{duoi}|{d}', {'n': 0, 'G0': 0, 'G3': 0})
                o['n'] += 1
                o['G0'] += int(h['p_G0'] < ALPHA)
                o['G3'] += int(h['p_G3'] < ALPHA)
        n_all = n_dm = n_ht = 0
        for u in x['cua_so']['that|R0']['bang']['pv']:
            if not (u['hop_le'] and u['trong_U']) or u['nhom'] != 'metric':
                continue
            n_all += 1
            duoi = u['ma'].split('|', 1)[1].split('_', 1)[1]
            n_dm += int(duoi not in BO[ds])
            n_ht += int(duoi not in BO[ds] or duoi == GIU_SAU_M3)
        dem.setdefault(ds, []).append((n_all, n_dm, n_ht))
    aa = {k: dict(o, ty_le_G0=round(o['G0'] / o['n'], 4), ty_le_G3=round(o['G3'] / o['n'], 4),
                  wilson95_G3=wilson(o['G3'], o['n'])) for k, o in sorted(q.items())}
    so = {ds: {'cua_so': len(v), 'trung_vi_toan_bo': statistics.median(x[0] for x in v),
               'trung_vi_danh_muc_ban_dau': statistics.median(x[1] for x in v),
               'trung_vi_danh_muc_hien_tai': statistics.median(x[2] for x in v)} for ds, v in dem.items()}
    return aa, so


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--b3', required=True)
    ap.add_argument('--kiem-ce', default=None, help='kiem-sau-khoa*.json: thêm qua cổng G3 ở C-e theo loại kênh (RE2-TT)')
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    mt = t046.moi_truong()
    out = {'bo_khoi_danh_muc': BO, 'tuong_quan_kenh_bo_kenh_giu': tuong_quan(mt)}
    out['qua_cong_aa_theo_hau_to'], out['so_don_vi_metric_that'] = theo_hau_to(a.b3)
    if a.kiem_ce:
        k = json.loads(Path(a.kiem_ce).read_bytes().decode('utf-8'))
        out['qua_cong_ce_G3_theo_hau_to_RE2'] = k['qua_cong_ce_theo_hau_to']
    Path(a.ra).write_bytes((json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    print(json.dumps(out['tuong_quan_kenh_bo_kenh_giu'], ensure_ascii=False))
    print(json.dumps(out['so_don_vi_metric_that'], ensure_ascii=False))


if __name__ == '__main__':
    main()
