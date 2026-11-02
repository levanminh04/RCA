"""T-046 bước 2: kiểm G0, G1, G3 trên dữ liệu tổng hợp đã biết đáp án (SPEC T-046 bước 2; A7, khai trước).

1. Tái lập số G0 của SPEC T-043 dòng 415 theo cài đặt ở LOG T-043 dòng 1829: AR(1), 300 + 300 điểm (một chuỗi 600 điểm,
   300 đầu là N, 300 sau là A), 2.000 lần mỗi mức, `numpy.random.default_rng(0)` dùng tuần tự cho bốn mức
   φ = 0; 0,5; 0,9; 0,98; x[0] = e[0]/sqrt(1 − φ²); `mannwhitneyu(A, N, alternative="greater", method="asymptotic",
   use_continuity=True)`; đếm p < 0,01. Phải ra 0,011; 0,073; 0,288; 0,386. Kiểm thêm `e4.p_cong` cho cùng p.
2. G0, G1, G3 trên AR(1) cùng cách sinh, cỡ 300 + 300 và 150 + 150, φ ∈ {0; 0,5; 0,9; 0,98}, hai hướng; trôi bậc
   thang: AR(1) φ = 0,5 cộng c·σ (σ = 1/sqrt(1 − φ²)) cho mọi điểm của A, c ∈ {0,25; 0,5}. 2.000 lần mỗi kịch bản;
   seed kịch bản = 20261101 + chỉ số kịch bản. Mẫu đặt mỗi giây: N ở t − (n − i) + 0,5 giây, A ở t + i + 0,5 giây.
3. Điều kiện đạt (A7): ở φ = 0, khoảng Wilson 99% của tỷ lệ qua cổng của G1, G3 chứa α hoặc nằm dưới α (cả hai cỡ,
   hai hướng). Kịch bản khác chỉ báo cáo.

Chạy: $PY -B results/T-046/scripts/b2_tong_hop.py --ra results/T-046/runs/b2-tong-hop-001
"""
import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.stats import mannwhitneyu

import cong
from m1 import e4

NS = cong.NS
TS = {'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05, 'n_exact_max': 100}
ALPHA = 0.01
PHI = (0.0, 0.5, 0.9, 0.98)
SO_LAN = 2000


def wilson(k, n, z):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [(c - r) / d, (c + r) / d]


def ar1_tu_e(e, phi):
    x = np.empty(len(e))
    x[0] = e[0] / math.sqrt(1 - phi ** 2)
    for i in range(1, len(e)):
        x[i] = phi * x[i - 1] + e[i]
    return x


def tai_lap_T043():
    rng = np.random.default_rng(0)
    out = {}
    for phi in PHI:
        k_scipy = k_e4 = 0
        lech = 0
        for _ in range(SO_LAN):
            x = ar1_tu_e(rng.standard_normal(600), phi)
            N, A = x[:300], x[300:]
            p1 = mannwhitneyu(A, N, alternative='greater', method='asymptotic', use_continuity=True).pvalue
            p2, cach = e4.p_cong(list(A), list(N), 'len', 100)
            assert cach == 'xap_xi'
            lech += int(p1 != p2)
            k_scipy += int(p1 < ALPHA)
            k_e4 += int(p2 < ALPHA)
        out[str(phi)] = {'ty_le_scipy': k_scipy / SO_LAN, 'ty_le_e4': k_e4 / SO_LAN, 'so_p_lech': lech}
    mong = {'0.0': 0.011, '0.5': 0.073, '0.9': 0.288, '0.98': 0.386}
    out['khop'] = all(round(out[k]['ty_le_scipy'], 3) == v and out[k]['ty_le_e4'] == out[k]['ty_le_scipy']
                      for k, v in mong.items())
    out['mong_doi'] = mong
    return out


def kich_ban():
    ds = []
    for n in (300, 150):
        for phi in PHI:
            ds.append({'ten': f'ar1_phi{phi}_n{n}', 'n': n, 'phi': phi, 'c': 0.0})
        for c in (0.25, 0.5):
            ds.append({'ten': f'bac_thang_phi0.5_c{c}_n{n}', 'n': n, 'phi': 0.5, 'c': c})
    return ds


def chay_kich_ban(i, kb):
    rng = np.random.default_rng(20261101 + i)
    n, phi, c = kb['n'], kb['phi'], kb['c']
    t = 10_000 * NS
    mN = [t - (n - j) * NS + NS // 2 for j in range(n)]
    mA = [t + j * NS + NS // 2 for j in range(n)]
    dem = {f'{g}|{d}': 0 for g in ('G0', 'G1', 'G3') for d in ('len', 'xuong')}
    roi = {'it_o': 0, 'phuong_sai_0': 0, 'it_khoi': 0}
    b_ds = []
    t0 = time.perf_counter()
    for r in range(SO_LAN):
        x = ar1_tu_e(rng.standard_normal(2 * n), phi)
        x[n:] += c / math.sqrt(1 - phi ** 2)
        N, A = [float(v) for v in x[:n]], [float(v) for v in x[n:]]
        kbk = cong.chuan_bi_khoi(N, mN, A, mA, t)
        if kbk['roi_G0']:
            roi[kbk['roi_G0']] += 1
        else:
            b_ds.append(kbk['b'])
        for d in ('len', 'xuong'):
            for g in ('G0', 'G1', 'G3'):
                p = cong.p_theo_cong(g, N, mN, A, mA, t, d, TS, f"gia|{kb['ten']}|{r}", kb=kbk)['p']
                dem[f'{g}|{d}'] += int(p < ALPHA)
    out = {'kich_ban': kb, 'so_lan': SO_LAN, 'roi_G0': roi, 'giay': round(time.perf_counter() - t0, 1),
           'b_trung_vi': float(np.median(b_ds)) if b_ds else None,
           'b_cham_tran_60': int(sum(1 for b in b_ds if b == 60)), 'ty_le': {}}
    for k, v in dem.items():
        out['ty_le'][k] = {'k': v, 'ty_le': v / SO_LAN, 'wilson95': wilson(v, SO_LAN, 1.959964),
                           'wilson99': wilson(v, SO_LAN, 2.575829)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    ra = Path(a.ra)
    ra.mkdir(parents=True, exist_ok=False)
    kq = {'bat_dau': time.strftime('%Y-%m-%dT%H:%M:%S%z')}

    def ghi():
        (ra / 'tong-hop.json').write_bytes((json.dumps(kq, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    t0 = time.time()
    kq['tai_lap_T043'] = tai_lap_T043()
    kq['giay_tai_lap'] = round(time.time() - t0, 1)
    ghi()
    print('tai lap', kq['tai_lap_T043']['khop'], flush=True)
    kq['kich_ban'] = []
    for i, kb in enumerate(kich_ban()):
        kq['kich_ban'].append(chay_kich_ban(i, kb))
        ghi()
        print(kb['ten'], kq['kich_ban'][-1]['giay'], flush=True)
    dat = {}
    for x in kq['kich_ban']:
        if x['kich_ban']['phi'] == 0.0 and x['kich_ban']['c'] == 0.0:
            for g in ('G1', 'G3'):
                for d in ('len', 'xuong'):
                    w = x['ty_le'][f'{g}|{d}']['wilson99']
                    dat[f"{x['kich_ban']['ten']}|{g}|{d}"] = w[0] <= ALPHA
    kq['dieu_kien_phi0'] = dat
    kq['dat_A7'] = kq['tai_lap_T043']['khop'] and all(dat.values())
    kq['xong'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    ghi()
    print('dat_A7', kq['dat_A7'], flush=True)


if __name__ == '__main__':
    main()
