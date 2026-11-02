"""T-046 N5, sau phản biện lượt 2: so cờ F_raw của G1 và G3 theo cặp trên cùng phép ở A/A, không nhãn, không chạy chuỗi.

Theo từng ô (cấu hình, dataset, nhóm) của `chan-doan-cong-ban3`:
- bảng 2×2 theo phép; McNemar chính xác (bỏ qua phụ thuộc trong ca, chỉ để đối chiếu);
- theo ca: số ca G1 ít cờ hơn, nhiều hơn, bằng; dấu hai phía;
- bootstrap theo ca (ca là cụm; 5.000 lần; seed cố định): khoảng 95% của hiệu tỷ lệ cờ G1 − G3.
Toàn bộ: hiệu của ô tệ nhất (đại lượng minimax nếu đếm theo cờ), bootstrap theo ca trong từng dataset; không tính metric
Nezha-OB (như minimax bản 4).

Chạy: $PY -B results/T-046/scripts/n5_so_cap.py --cu results/T-046/runs/b3-sua2-aa-001 --moi results/T-046/runs/b3b-aa-001
      --ra results/T-046/so-cap-g1-g3.json
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

import t046
from b3b_tong_hop import ALPHA, O_PV

SEED = 20261102
LAP = 5000


def dem_theo_ca(ca):
    """{ô: {mã ca: [n, cờ G1, cờ G3, chỉ G1, chỉ G3]}}."""
    out = {}
    for oid, x in ca.items():
        ds = x['dataset']
        for cfg in ('R0', 'K-du'):
            for u in x['cua_so'][f'aa|{cfg}']['bang']['pv']:
                if not (u['hop_le'] and u['trong_U']) or u['nhom'] not in O_PV[cfg]:
                    continue
                for h in u['huong'].values():
                    c1 = h['p_G1'] < ALPHA and h['chenh_duong']
                    c3 = h['p_G3'] < ALPHA and h['chenh_duong']
                    o = out.setdefault(f"{cfg}|{ds}|{u['nhom']}", {}).setdefault(oid, [0, 0, 0, 0, 0])
                    o[0] += 1
                    o[1] += int(c1)
                    o[2] += int(c3)
                    o[3] += int(c1 and not c3)
                    o[4] += int(c3 and not c1)
    return out


def ty_le(a):
    return a[:, 1:3].sum(axis=0) / max(a[:, 0].sum(), 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cu', required=True)
    ap.add_argument('--moi', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    ca, _ = t046.nap_ghep(a.cu, a.moi)
    bang = dem_theo_ca(ca)
    rng = np.random.default_rng(SEED)
    out = {'seed': SEED, 'lap': LAP, 'alpha': ALPHA, 'o': {}}
    for k, v in sorted(bang.items()):
        arr = np.array([v[o] for o in sorted(v)], dtype=float)
        chi1, chi3 = int(arr[:, 3].sum()), int(arr[:, 4].sum())
        ca1 = int((arr[:, 1] < arr[:, 2]).sum())
        ca3 = int((arr[:, 1] > arr[:, 2]).sum())
        hieu = []
        for _ in range(LAP):
            r = ty_le(arr[rng.integers(0, len(arr), len(arr))])
            hieu.append(r[0] - r[1])
        r0 = ty_le(arr)
        out['o'][k] = {
            'n_phep': int(arr[:, 0].sum()), 'so_ca': len(arr), 'co_G1': int(arr[:, 1].sum()), 'co_G3': int(arr[:, 2].sum()),
            'chi_G1': chi1, 'chi_G3': chi3,
            'mcnemar_p_bo_qua_phu_thuoc': binomtest(chi1, chi1 + chi3, 0.5).pvalue if chi1 + chi3 else None,
            'ca_G1_it_co_hon': ca1, 'ca_G1_nhieu_co_hon': ca3, 'ca_bang': len(arr) - ca1 - ca3,
            'dau_p': binomtest(ca1, ca1 + ca3, 0.5).pvalue if ca1 + ca3 else None,
            'hieu_G1_tru_G3': round(float(r0[0] - r0[1]), 6),
            'hieu_khoang95_theo_ca': [round(float(q), 6) for q in np.percentile(hieu, [2.5, 97.5])]}
    # Ô tệ nhất theo cờ: mỗi dataset lấy lại ca một lần, dùng chung cho mọi ô của dataset
    o_ds = {ds: sorted({oid for k, v in bang.items() if f'|{ds}|' in k for oid in v}) for ds in ('RE2-TT', 'Nezha-OB')}
    tinh = [k for k in bang if not k.endswith('|Nezha-OB|metric')]

    def te_nhat(chon):
        m1, m3 = 0.0, 0.0
        for k in tinh:
            ds = k.split('|')[1]
            arr = np.array([bang[k].get(o, [0, 0, 0, 0, 0]) for o in chon[ds]], dtype=float)
            r = ty_le(arr)
            m1, m3 = max(m1, r[0]), max(m3, r[1])
        return m1, m3

    g1, g3 = te_nhat(o_ds)
    hieu, g1_thap = [], 0
    for _ in range(LAP):
        chon = {ds: [v[i] for i in rng.integers(0, len(v), len(v))] for ds, v in o_ds.items()}
        x1, x3 = te_nhat(chon)
        hieu.append(x1 - x3)
        g1_thap += int(x1 < x3)
    out['o_te_nhat'] = {'G1': round(g1, 6), 'G3': round(g3, 6), 'hieu_G1_tru_G3': round(g1 - g3, 6),
                        'hieu_khoang95_theo_ca': [round(float(q), 6) for q in np.percentile(hieu, [2.5, 97.5])],
                        'ty_le_lan_lap_G1_thap_hon': round(g1_thap / LAP, 4)}
    Path(a.ra).write_bytes((json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    for k, r in out['o'].items():
        print(k, r['co_G1'], r['co_G3'], 'chỉ', r['chi_G1'], r['chi_G3'], 'ca', r['ca_G1_it_co_hon'], r['ca_G1_nhieu_co_hon'],
              r['ca_bang'], 'dấu', round(r['dau_p'], 3) if r['dau_p'] is not None else None, 'hiệu', r['hieu_G1_tru_G3'], r['hieu_khoang95_theo_ca'])
    print(out['o_te_nhat'])


if __name__ == '__main__':
    main()
