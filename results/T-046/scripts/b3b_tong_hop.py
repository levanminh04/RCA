"""T-046 bước 3–4 bản 3: tổng hợp chẩn đoán cho G4, D1 trên lượt ghép (SPEC T-046 B1, B2, B5; A2, A6; D-1).
Không đọc nhãn. Ghép `runs/b3-aa-001` (G0, G1, G3) với `runs/b3b-aa-001` (G0, G4, D1) bằng `t046.nap_ghep`.

Thứ tự in ra theo thứ tự nhìn: (1) kiểm ghép; (2) số phép theo ô; (3) tỷ lệ qua cổng ở A/A của G0, G1, G3, G4 theo ô
phân vị, hướng, nhóm ρ(1), áp dụng hay rơi về G0; (4) đơn vị đếm D0, D1 theo ô, φ̂_d; (5) ngưỡng GE, DE theo ô
(dataset, nhóm, hướng) theo B1, B2 (ô dưới 100 phép dùng α, ghi không hiệu chuẩn được); (6) tóm tắt D-1 bản 3.

Chạy: $PY -B results/T-046/scripts/b3b_tong_hop.py --cu results/T-046/runs/b3-aa-001 --moi results/T-046/runs/b3b-aa-001
      --ra results/T-046/chan-doan-cong-ban3.json
"""
import argparse
import json
import statistics
from pathlib import Path

import t046
from t046 import wilson

ALPHA = 0.01
MIN_PHEP = 100
CONG_PV = ('G0', 'G1', 'G3', 'G4')
O_PV = {'R0': ('op_full', 'metric'), 'K-du': ('op_excl', 'canh')}
O_DEM = {'R0': ('log_loi',), 'K-du': ('mau_loi', 'mau_thuong')}
RHO1_NHOM = (('<0,25', -2, 0.25), ('0,25–0,75', 0.25, 0.75), ('0,75–0,95', 0.75, 0.95), ('>=0,95', 0.95, 2))


def ty_le(ds, dk):
    n = len(ds)
    k = sum(1 for x in ds if dk(x))
    return {'k': k, 'n': n, 'ty_le': round(k / n, 6) if n else None, 'wilson95': wilson(k, n)}


def gom(ca):
    """Phép ở A/A theo ô (cấu hình, dataset, nhóm) cho đơn vị phân vị và đơn vị đếm (không gồm NEW_OP/STOPPED)."""
    pv, dem = {}, {}
    for oid, x in ca.items():
        ds = x['dataset']
        for cfg in ('R0', 'K-du'):
            b = x['cua_so'][f'aa|{cfg}']['bang']
            for u in b['pv']:
                if not (u['hop_le'] and u['trong_U']) or u['nhom'] not in O_PV[cfg]:
                    continue
                kh = u.get('khoi') or {}
                for d, h in u['huong'].items():
                    pv.setdefault((cfg, ds, u['nhom']), []).append(dict(h, d=d, rho1=kh.get('rho1'), ma=u['ma']))
            for u in b['dem']:
                if not (u['hop_le'] and u['trong_U']) or u['nhan'] in ('NEW_OP', 'STOPPED') or u['nhom'] not in O_DEM[cfg]:
                    continue
                for d in u['huong_cham']:
                    dem.setdefault((cfg, ds, u['nhom']), []).append(
                        {'d': d, 'p_D0': u[f'p_{d}'], 'p_D1': u[f'p_D1_{d}'], 'phi': u['D1_phi'], 'so_o': u['D1_so_o'],
                         'F_D0': u[f'F_raw_{d}'], 'chenh': u[f'chenh_{d}_duong']})
    return pv, dem


def nguong_theo_o(pv, dem):
    """B1, B2: α_ô theo (dataset, nhóm, hướng) trên A/A; ô dưới 100 phép dùng α (không hiệu chuẩn được)."""
    out = {'GE': {}, 'DE': {}}
    for (cfg, ds, nhom), v in pv.items():
        if ds == 'Nezha-OB' and nhom == 'metric':
            continue
        for d in sorted({x['d'] for x in v}):
            ps = [x['p_G4'] for x in v if x['d'] == d]
            a = t046.chon_nguong(ps, ALPHA) if len(ps) >= MIN_PHEP else None
            out['GE'][f'{ds}|{nhom}|{d}'] = {'n': len(ps), 'nguong': a if a is not None else ALPHA,
                                             'hieu_chuan': len(ps) >= MIN_PHEP, 'truot': len(ps) >= MIN_PHEP and a is None}
    for (cfg, ds, nhom), v in dem.items():
        for d in sorted({x['d'] for x in v}):
            ps = [x['p_D1'] for x in v if x['d'] == d]
            a = t046.chon_nguong(ps, ALPHA) if len(ps) >= MIN_PHEP else None
            out['DE'][f'{ds}|{nhom}|{d}'] = {'n': len(ps), 'nguong': a if a is not None else ALPHA,
                                             'hieu_chuan': len(ps) >= MIN_PHEP, 'truot': len(ps) >= MIN_PHEP and a is None}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cu', required=True)
    ap.add_argument('--moi', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    ca, kiem = t046.nap_ghep(a.cu, a.moi)
    pv, dem = gom(ca)
    out = {'luot_cu': a.cu, 'luot_moi': a.moi, 'kiem_ghep': kiem, 'alpha': ALPHA, 'muc_a': 2 * ALPHA}
    out['ho_tro'] = {'|'.join(k): {'so_phep': len(v), 'do_duoc': len(v) >= MIN_PHEP} for k, v in sorted(pv.items())}
    out['ho_tro_dem'] = {'|'.join(k): {'so_phep': len(v), 'do_duoc': len(v) >= MIN_PHEP} for k, v in sorted(dem.items())}
    qua = {}
    for k, v in sorted(pv.items()):
        q = {}
        for g in CONG_PV:
            q[g] = ty_le(v, lambda x, g=g: x[f'p_{g}'] < ALPHA)
            q[g]['theo_huong'] = {d: ty_le([x for x in v if x['d'] == d], lambda x, g=g: x[f'p_{g}'] < ALPHA)
                                  for d in sorted({x['d'] for x in v})}
            q[g]['co_F_raw'] = ty_le(v, lambda x, g=g: x[f'p_{g}'] < ALPHA and x['chenh_duong'])
            q[g]['duoi_alpha_100'] = ty_le(v, lambda x, g=g: x[f'p_{g}'] < ALPHA / 100)
            q[g]['theo_rho1'] = {ten: ty_le([x for x in v if x['rho1'] is not None and lo <= x['rho1'] < hi],
                                            lambda x, g=g: x[f'p_{g}'] < ALPHA) for ten, lo, hi in RHO1_NHOM}
        if k[2] == 'metric':
            ap_ = [x for x in v if x['cach_G4'].startswith('G4')]
            roi = [x for x in v if not x['cach_G4'].startswith('G4')]
            q['G4']['ap_dung'] = ty_le(ap_, lambda x: x['p_G4'] < ALPHA)
            q['G4']['roi_G0'] = ty_le(roi, lambda x: x['p_G4'] < ALPHA)
            phi = [x['G4_phi'] for x in ap_ if x.get('G4_phi') is not None]
            q['G4']['phi_trung_vi'] = round(statistics.median(phi), 4) if phi else None
        qua['|'.join(k)] = q
    out['qua_cong_aa'] = qua
    dd = {}
    for k, v in sorted(dem.items()):
        phi = [x['phi'] for x in v]
        dd['|'.join(k)] = {'D0': ty_le(v, lambda x: x['p_D0'] < ALPHA), 'D1': ty_le(v, lambda x: x['p_D1'] < ALPHA),
                           'D0_co': ty_le(v, lambda x: x['F_D0'] == 1),
                           'D1_co': ty_le(v, lambda x: x['p_D1'] < ALPHA and x['chenh']),
                           'theo_huong': {d: {'D0': ty_le([x for x in v if x['d'] == d], lambda x: x['p_D0'] < ALPHA),
                                              'D1': ty_le([x for x in v if x['d'] == d], lambda x: x['p_D1'] < ALPHA)}
                                          for d in sorted({x['d'] for x in v})},
                           'phi_trung_vi': round(statistics.median(phi), 4) if phi else None,
                           'phi_lon_hon_1': sum(1 for x in phi if x > 1), 'do_duoc': len(v) >= MIN_PHEP}
    out['don_vi_dem'] = dd
    out['nguong'] = nguong_theo_o(pv, dem)
    # D-1 bản 3: cổng đếm D1 trên ô đo được; cổng phân vị G4 trên ô phân vị (trừ metric Nezha-OB)
    out['D1_tom_tat'] = {
        'G4_o_vuot_muc_a': sorted(k for k, q in qua.items() if not k.endswith('Nezha-OB|metric')
                                  and q['G4']['ty_le'] > 2 * ALPHA),
        'D1_o_vuot_muc_a': sorted(k for k, r in dd.items() if r['do_duoc'] and r['D1']['ty_le'] > 2 * ALPHA),
        'o_dem_khong_do_duoc': sorted(k for k, r in dd.items() if not r['do_duoc']),
        'GE_o_truot': sorted(k for k, r in out['nguong']['GE'].items() if r['truot']),
        'DE_o_truot': sorted(k for k, r in out['nguong']['DE'].items() if r['truot'])}
    Path(a.ra).write_bytes((json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    print(json.dumps({'kiem_ghep': kiem, 'ho_tro_dem': out['ho_tro_dem']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
