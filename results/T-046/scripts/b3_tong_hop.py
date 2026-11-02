"""T-046 bước 3–4: tổng hợp chẩn đoán C1 từ lượt b3 (SPEC T-046 C1, A2, A5, A6; D-1). Không đọc nhãn.

Thứ tự in ra theo thứ tự được nhìn: (1) số phép hợp lệ theo ô và mức đo được (A6); (2) tỷ lệ qua cổng A/A theo ô,
cổng, hướng; (3) chẩn đoán phụ A2; (4) tự tương quan và b trên N; (5) kiểm D-1 cho đơn vị đếm.
Ô = (cấu hình, dataset, nhóm đơn vị); nguồn suy từ nhóm (op_full, op_excl, canh: trace; metric: metric; log_loi,
mau_loi, mau_thuong: log). Chỉ phép hợp lệ, thực thể thuộc U, hướng thuộc `huong_cham`. NEW_OP, STOPPED (gồm ô mẫu
mới) là cờ trực tiếp, đếm riêng. Metric Nezha-OB loại khỏi (a) (SPEC).

Chạy: $PY -B results/T-046/scripts/b3_tong_hop.py --luot results/T-046/runs/b3-aa-001 --ra results/T-046/chan-doan-cong.json
"""
import argparse
import json
import statistics
from pathlib import Path

import t046
from t046 import wilson

ALPHA = 0.01
NGUON = {'op_full': 'trace', 'op_excl': 'trace', 'canh': 'trace', 'metric': 'metric', 'log_loi': 'log',
         'mau_loi': 'log', 'mau_thuong': 'log', 'mau_moi': 'log', 'tan_suat': 'trace'}
MIN_PHEP = 100
RHO1_NHOM = (('<0,25', -2, 0.25), ('0,25–0,75', 0.25, 0.75), ('0,75–0,95', 0.75, 0.95), ('>=0,95', 0.95, 2))


def _o(cfg, ds, nhom):
    return f'{cfg}|{ds}|{nhom}'


def tong_hop(luot):
    ca = t046.nap_luot(luot)
    so_ca = {'RE2-TT': 0, 'Nezha-OB': 0}
    pv, dem, tt = {}, {}, {}
    pv_that = {}
    rho = {}
    for oid, x in ca.items():
        ds = x['dataset']
        so_ca[ds] += 1
        for k, w in x['cua_so'].items():
            kieu, cfg = k.split('|')
            b = w['bang']
            for u in b['pv']:
                if not (u['hop_le'] and u['trong_U']):
                    continue
                o = _o(cfg, ds, u['nhom'])
                kh = u.get('khoi') or {}
                if kieu == 'that':
                    pv_that.setdefault(o, []).append({'roi_G0': kh.get('roi_G0'), 'b': kh.get('b'),
                                                      'rho1': kh.get('rho1'), 'cham_tran': kh.get('cham_tran')})
                    continue
                rho.setdefault(o, []).append({'b': kh.get('b'), 'rho1': kh.get('rho1'), 'roi_G0': kh.get('roi_G0'),
                                              'cham_tran': kh.get('cham_tran')})
                for d, h in u['huong'].items():
                    pv.setdefault(o, []).append(dict(h, d=d, roi_G0=kh.get('roi_G0'), b=kh.get('b'),
                                                     cham_tran=kh.get('cham_tran'), rho1=kh.get('rho1'),
                                                     ma=u['ma'], ca=oid))
            if kieu != 'aa':
                continue
            for u in b['dem']:
                if not (u['hop_le'] and u['trong_U']):
                    continue
                o = _o(cfg, ds, u['nhom'])
                if u['nhan'] in ('NEW_OP', 'STOPPED'):
                    tt.setdefault(o, {}).setdefault(u['nhan'], 0)
                    tt[o][u['nhan']] += 1
                    continue
                for d in u['huong_cham']:
                    dem.setdefault(o, []).append({'p': u[f'p_{d}'], 'F': u[f'F_raw_{d}'], 'd': d})
    return ca, so_ca, pv, dem, tt, pv_that, rho


def ty_le(ds, dk):
    n = len(ds)
    k = sum(1 for x in ds if dk(x))
    return {'k': k, 'n': n, 'ty_le': round(k / n, 6) if n else None, 'wilson95': wilson(k, n)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luot', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    ca, so_ca, pv, dem, tt, pv_that, rho = tong_hop(a.luot)
    out = {'luot': a.luot, 'so_ca': so_ca, 'alpha': ALPHA, 'muc_a': 2 * ALPHA, 'min_phep_A6': MIN_PHEP}
    # (1) hỗ trợ
    out['ho_tro'] = {o: {'so_phep': len(v), 'do_duoc': len(v) >= MIN_PHEP,
                         'nguon': NGUON[o.split('|')[2]]} for o, v in sorted(pv.items())}
    out['ho_tro_dem'] = {o: {'so_phep': len(v), 'do_duoc': len(v) >= MIN_PHEP} for o, v in sorted(dem.items())}
    out['co_truc_tiep_aa'] = tt
    # (2) tỷ lệ qua cổng ở A/A
    qua = {}
    for o, v in sorted(pv.items()):
        q = {}
        for g in t046.CONG:
            q[g] = ty_le(v, lambda x, g=g: x[f'p_{g}'] < ALPHA)
            q[g]['theo_huong'] = {d: ty_le([x for x in v if x['d'] == d], lambda x, g=g: x[f'p_{g}'] < ALPHA)
                                  for d in sorted({x['d'] for x in v})}
            q[g]['co_F_raw'] = ty_le(v, lambda x, g=g: x[f'p_{g}'] < ALPHA and x['chenh_duong'])
            q[g]['duoi_alpha_10'] = ty_le(v, lambda x, g=g: x[f'p_{g}'] < ALPHA / 10)
            q[g]['duoi_alpha_100'] = ty_le(v, lambda x, g=g: x[f'p_{g}'] < ALPHA / 100)
            if g != 'G0':
                ap_ = [x for x in v if not x['roi_G0']]
                roi = [x for x in v if x['roi_G0']]
                q[g]['ap_dung'] = ty_le(ap_, lambda x, g=g: x[f'p_{g}'] < ALPHA)
                q[g]['roi_G0'] = ty_le(roi, lambda x, g=g: x[f'p_{g}'] < ALPHA)
                q[g]['roi_G0_ly_do'] = {r: sum(1 for x in roi if x['roi_G0'] == r) for r in sorted({x['roi_G0'] for x in roi})}
                q[g]['b_duoi_60'] = ty_le([x for x in ap_ if not x['cham_tran']], lambda x, g=g: x[f'p_{g}'] < ALPHA)
                q[g]['b_cham_tran'] = ty_le([x for x in ap_ if x['cham_tran']], lambda x, g=g: x[f'p_{g}'] < ALPHA)
            # nhóm ρ(1) trên N″ (thêm 13:10, trước khi xem số A/A): so với mức AR(1) cùng φ của bước 2
            q[g]['theo_rho1'] = {ten: ty_le([x for x in v if x['rho1'] is not None and lo <= x['rho1'] < hi],
                                            lambda x, g=g: x[f'p_{g}'] < ALPHA)
                                 for ten, lo, hi in RHO1_NHOM}
            q[g]['theo_rho1']['khong_tinh_duoc'] = ty_le([x for x in v if x['rho1'] is None],
                                                         lambda x, g=g: x[f'p_{g}'] < ALPHA)
            gia = [x['e_tho'] for x in v if x[f'p_{g}'] < ALPHA and x['chenh_duong']]
            q[g]['do_lon_rA_rN_qua_gia'] = ({'trung_vi': round(statistics.median(gia), 6),
                                             'p90': round(sorted(gia)[int(0.9 * (len(gia) - 1))], 6)} if gia else None)
        qua[o] = q
    out['qua_cong_aa'] = qua
    # (3) A2: tỷ lệ rơi về G0 ở cỡ A/A so với cỡ thật (chỉ b và số khối)
    roi = {}
    for o in sorted(set(rho) | set(pv_that)):
        aa = rho.get(o, [])
        th = pv_that.get(o, [])
        roi[o] = {'aa': ty_le(aa, lambda x: bool(x['roi_G0'])), 'that': ty_le(th, lambda x: bool(x['roi_G0'])),
                  'aa_ly_do': {r: sum(1 for x in aa if x['roi_G0'] == r) for r in sorted({x['roi_G0'] for x in aa if x['roi_G0']})},
                  'that_ly_do': {r: sum(1 for x in th if x['roi_G0'] == r) for r in sorted({x['roi_G0'] for x in th if x['roi_G0']})}}
    out['roi_G0_aa_so_that'] = roi
    # (4) tự tương quan, b: trên N thật (52 ca) và N″ (A/A)
    tq = {}
    for nhan, src in (('N_that', pv_that), ('N_aa', rho)):
        for o, v in sorted(src.items()):
            r1 = [x['rho1'] for x in v if x['rho1'] is not None]
            bb = [x['b'] for x in v if x['b'] is not None]
            tq.setdefault(o, {})[nhan] = {
                'so_don_vi': len(v), 'co_rho1': len(r1),
                'rho1_trung_vi': round(statistics.median(r1), 4) if r1 else None,
                'rho1_tu_phan_vi': [round(statistics.quantiles(r1, n=4)[0], 4), round(statistics.quantiles(r1, n=4)[2], 4)] if len(r1) >= 4 else None,
                'b_trung_vi': statistics.median(bb) if bb else None,
                'b_cham_tran_60': sum(1 for x in v if x['cham_tran']), 'co_b': len(bb)}
    out['tu_tuong_quan'] = tq
    # (5) D-1: đơn vị đếm ở A/A
    d1 = {}
    for o, v in sorted(dem.items()):
        r = ty_le(v, lambda x: x['p'] < ALPHA)
        r['co_F_raw'] = ty_le(v, lambda x: x['F'] == 1)
        r['do_duoc'] = len(v) >= MIN_PHEP
        r['vuot_muc_a'] = (r['ty_le'] is not None and r['ty_le'] > 2 * ALPHA)
        d1[o] = r
    out['D1_don_vi_dem'] = d1
    out['D1_tom_tat'] = {
        'don_vi_dem_vuot_muc_a': sorted(o for o, r in d1.items() if r['vuot_muc_a']),
        'o_dem_khong_do_duoc': sorted(o for o, r in d1.items() if not r['do_duoc']),
        'o_phan_vi_khong_do_duoc': sorted(o for o, r in out['ho_tro'].items()
                                          if not r['do_duoc'] and not o.endswith('Nezha-OB|metric'))}
    Path(a.ra).write_bytes((json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    print(json.dumps(out['ho_tro'], ensure_ascii=False))
    print(json.dumps(out['D1_tom_tat'], ensure_ascii=False))


if __name__ == '__main__':
    main()
