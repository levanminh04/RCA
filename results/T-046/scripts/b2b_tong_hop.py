"""T-046 bước 2 cho ứng viên bản 3 (SPEC T-046 B4; khai trước khi chạy).

G4 (làm trắng AR(1)) trên AR(1) φ ∈ {0; 0,5; 0,9; 0,98}, cỡ 300 + 300 và 150 + 150, hai hướng; AR(1) φ = 0,9 cộng xu hướng
tuyến tính tăng một σ mỗi 300 giây (σ độ lệch chuẩn biên); bước nhảy c·σ ở A với φ = 0,5, c ∈ {0,25; 0,5} (chỉ báo
cáo, để so độ nhạy với G0, G1, G3 ở `runs/b2-tong-hop-001`). 2.000 lần mỗi kịch bản; seed 20261101 + 100 + chỉ số.
D1 trên số đếm tổng hợp, N = [t − 300, t), A = [t, t + 300), T_N = T_A = 300, h₀ = t − 300: Poisson tốc độ 0,1 và
0,5 sự kiện/giây; Poisson gộp cụm cùng tốc độ trung bình (cụm Poisson tốc độ λ/3, cỡ cụm hình học trung bình 3, các sự
kiện của cụm rơi đều trong cùng ô 10 giây chứa tâm cụm). 2.000 lần mỗi kịch bản; seed 20261101 + 200 + chỉ số.
Điều kiện đạt: G4 ở φ = 0 và D1 ở Poisson: khoảng Wilson 99% của tỷ lệ qua cổng chứa α hoặc nằm dưới α (mọi cỡ, hướng).

Chạy: $PY -B results/T-046/scripts/b2b_tong_hop.py --ra results/T-046/runs/b2b-tong-hop-001
"""
import argparse
import json
import math
import time
from pathlib import Path

import numpy as np

import cong
from m1 import e4
from b2_tong_hop import ar1_tu_e, wilson

NS = cong.NS
TS = {'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05, 'n_exact_max': 100}
ALPHA = 0.01
SO_LAN = 2000


def kich_ban_G4():
    ds = []
    for n in (300, 150):
        for phi in (0.0, 0.5, 0.9, 0.98):
            ds.append({'ten': f'ar1_phi{phi}_n{n}', 'n': n, 'phi': phi, 'c': 0.0, 'xu_huong': 0.0})
        ds.append({'ten': f'ar1_phi0.9_xu_huong1_n{n}', 'n': n, 'phi': 0.9, 'c': 0.0, 'xu_huong': 1.0})
        for c in (0.25, 0.5):
            ds.append({'ten': f'bac_thang_phi0.5_c{c}_n{n}', 'n': n, 'phi': 0.5, 'c': c, 'xu_huong': 0.0})
    return ds


def chay_G4(i, kb):
    rng = np.random.default_rng(20261101 + 100 + i)
    n, phi = kb['n'], kb['phi']
    sig = 1 / math.sqrt(1 - phi ** 2)
    t = 10_000 * NS
    mN = [t - (n - j) * NS + NS // 2 for j in range(n)]
    mA = [t + j * NS + NS // 2 for j in range(n)]
    dem = {f'{g}|{d}': 0 for g in ('G0', 'G4') for d in ('len', 'xuong')}
    roi = {}
    t0 = time.perf_counter()
    for _ in range(SO_LAN):
        x = ar1_tu_e(rng.standard_normal(2 * n), phi)
        x += kb['xu_huong'] * sig * np.arange(2 * n) / 300.0
        x[n:] += kb['c'] * sig
        N, A = [float(v) for v in x[:n]], [float(v) for v in x[n:]]
        for d in ('len', 'xuong'):
            dem[f'G0|{d}'] += int(cong.p_G0(N, A, d, TS)[0] < ALPHA)
            r = cong.p_G4_metric(N, mN, A, mA, t, d, TS)
            dem[f'G4|{d}'] += int(r['p'] < ALPHA)
            if r['roi_G0']:
                roi[r['roi_G0']] = roi.get(r['roi_G0'], 0) + 1
    return {'kich_ban': kb, 'roi_G0': roi, 'giay': round(time.perf_counter() - t0, 1),
            'ty_le': {k: {'k': v, 'ty_le': v / SO_LAN, 'wilson99': wilson(v, SO_LAN, 2.575829)} for k, v in dem.items()}}


def kich_ban_D1():
    ds = []
    for lam in (0.1, 0.5):
        ds.append({'ten': f'poisson_{lam}', 'lam': lam, 'cum': False})
        ds.append({'ten': f'gop_cum_{lam}', 'lam': lam, 'cum': True})
    return ds


def _su_kien(rng, lam, cum, lo, W):
    if not cum:
        k = rng.poisson(lam * W)
        return list(lo + rng.uniform(0, W, k))
    k = rng.poisson(lam / 3 * W)
    out = []
    for c in rng.uniform(0, W, k):
        o = math.floor(c / 10) * 10
        out += list(lo + o + rng.uniform(0, 10, rng.geometric(1 / 3)))
    return out


def chay_D1(i, kb):
    rng = np.random.default_rng(20261101 + 200 + i)
    t = 10_000 * NS
    dem = {f'{g}|{d}': 0 for g in ('D0', 'D1') for d in ('len', 'xuong')}
    phi_ds = []
    t0 = time.perf_counter()
    for _ in range(SO_LAN):
        sN = _su_kien(rng, kb['lam'], kb['cum'], -300.0, 300.0)
        sA = _su_kien(rng, kb['lam'], kb['cum'], 0.0, 300.0)
        nN, nA = len(sN), len(sA)
        if nN + nA == 0:
            continue
        mocN = [t + int(round(x * NS)) for x in sN]
        mocN = [min(m, t - 1) for m in mocN]
        phi, _ = cong.he_so_phan_tan(mocN, t - 300 * NS, t)
        phi_ds.append(phi)
        for d in ('len', 'xuong'):
            dem[f'D0|{d}'] += int(e4.p_nhi_thuc(nA, nN + nA, 0.5, d) < ALPHA)
            dem[f'D1|{d}'] += int(cong.p_D1(nN, nA, 300.0, 300.0, phi, d) < ALPHA)
    return {'kich_ban': kb, 'giay': round(time.perf_counter() - t0, 1),
            'phi_trung_vi': float(np.median(phi_ds)),
            'ty_le': {k: {'k': v, 'ty_le': v / SO_LAN, 'wilson99': wilson(v, SO_LAN, 2.575829)} for k, v in dem.items()}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    ra = Path(a.ra)
    ra.mkdir(parents=True, exist_ok=False)
    kq = {'bat_dau': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'G4': [], 'D1': []}

    def ghi():
        (ra / 'tong-hop.json').write_bytes((json.dumps(kq, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    for i, kb in enumerate(kich_ban_D1()):
        kq['D1'].append(chay_D1(i, kb))
        ghi()
        print(kb['ten'], kq['D1'][-1]['giay'], flush=True)
    for i, kb in enumerate(kich_ban_G4()):
        kq['G4'].append(chay_G4(i, kb))
        ghi()
        print(kb['ten'], kq['G4'][-1]['giay'], flush=True)
    dat = {}
    for x in kq['G4']:
        if x['kich_ban']['phi'] == 0.0 and x['kich_ban']['c'] == 0.0 and x['kich_ban']['xu_huong'] == 0.0:
            for d in ('len', 'xuong'):
                dat[f"{x['kich_ban']['ten']}|G4|{d}"] = x['ty_le'][f'G4|{d}']['wilson99'][0] <= ALPHA
    for x in kq['D1']:
        if not x['kich_ban']['cum']:
            for d in ('len', 'xuong'):
                dat[f"{x['kich_ban']['ten']}|D1|{d}"] = x['ty_le'][f'D1|{d}']['wilson99'][0] <= ALPHA
    kq['dieu_kien'] = dat
    kq['dat_B4'] = all(dat.values())
    kq['xong'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    ghi()
    print('dat_B4', kq['dat_B4'], flush=True)


if __name__ == '__main__':
    main()
