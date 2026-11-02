"""T-046 bước 5 bản 4: chọn cổng theo minimax, chọn `verdict` theo (b), (c1), V4 khi cần (SPEC T-046 Bản 4 C1–C3).
Không đọc nhãn, không đọc C-e. Đầu vào: `chan-doan-cong-ban3.json`, lượt ghép b3 + b3b; tùy chọn p G3 đã tinh (A3 điểm 6).

- g*: cổng trong G0, G1, G3, G4 có max tỷ lệ qua cổng ở A/A trên các ô phân vị (trừ metric Nezha-OB) nhỏ nhất; hòa
  theo thứ tự G0 < G1 < G3 < G4. c*: trong D0, D1, max trên ô đếm đo được nhỏ nhất; hòa D0 < D1.
- v*: V0, V3, V1 theo thứ tự, cái đầu tiên đạt (b), (c1) từng dataset. V1 với g* ∈ {G3, G4} cần `--g3-tinh`; thiếu thì
  dừng ở trạng thái 'can_tinh_G3_V1'. Không đạt cả ba thì V4 với q* nhỏ nhất (lưới 0,005..1,000) của tỷ lệ đơn vị có
  cờ, cho (b) <= 0,20 mọi dataset đo được ở A/A; V4 phải đạt (c1) (SPEC bản 4 C2, sửa 15:01).
- Ghi `--ra-danh-gia` (mọi lượt); chỉ khi chọn được mới ghi `--ra-khoa` (ung-vien.json, tệp khóa).

Chạy: $PY -B results/T-046/scripts/b5c_danh_gia.py --cu results/T-046/runs/b3-aa-001 --moi results/T-046/runs/b3b-aa-001
      --chan-doan results/T-046/chan-doan-cong-ban3.json --ra-danh-gia results/T-046/danh-gia-ban4.json
      --ra-khoa results/T-046/ung-vien.json [--g3-tinh results/T-046/runs/<lượt tinh>]
"""
import argparse
import hashlib
import json
from pathlib import Path

import t046
from t046 import wilson

ALPHA = 0.01
MUC_B, MUC_C1 = 0.20, 0.80
MIN_CUA_SO_B = 10
K_MAX = 500


def minimax(cd):
    pv = {}
    for g in ('G0', 'G1', 'G3', 'G4'):
        o = [(q[g]['ty_le'], k) for k, q in cd['qua_cong_aa'].items() if not k.endswith('|Nezha-OB|metric')]
        pv[g] = {'max': max(o), 'o': {k: r for r, k in o}}
    g = min(('G0', 'G1', 'G3', 'G4'), key=lambda x: (pv[x]['max'][0], ('G0', 'G1', 'G3', 'G4').index(x)))
    dm = {}
    for c in ('D0', 'D1'):
        o = [(r[c]['ty_le'], k) for k, r in cd['don_vi_dem'].items() if r['do_duoc']]
        dm[c] = {'max': max(o), 'o': {k: r for r, k in o}}
    c = min(('D0', 'D1'), key=lambda x: (dm[x]['max'][0], ('D0', 'D1').index(x)))
    return g, c, pv, dm


def ap_tinh(ca, thu_muc):
    """Thay p_G3 (và p_G4 của đơn vị sự kiện) bằng p đã tinh (A3 điểm 6) cho các phép có trong tệp tinh."""
    n = 0
    for f in sorted(Path(thu_muc).glob('*.json')):
        x = json.loads(f.read_bytes().decode('utf-8'))
        for k, ds in x['p_tinh'].items():
            b = ca[x['opaque_id']]['cua_so'][k]['bang']
            idx = {u['ma']: u for u in b['pv']}
            for ma, d, p in ds:
                h = idx[ma]['huong'][d]
                h['p_G3'] = p
                if idx[ma]['nhom'] != 'metric':
                    h['p_G4'] = p
                n += 1
    return n


def mot_to_hop(ca, g, c, v):
    r = {}
    for ds in ('RE2-TT', 'Nezha-OB'):
        aa = [x['cua_so']['aa|R0']['bang'] for x in ca.values() if x['dataset'] == ds]
        th = [x['cua_so']['that|R0']['bang'] for x in ca.values() if x['dataset'] == ds]
        vaa = [t046.verdict_R0(b, g, v, c=c) for b in aa]
        vth = [t046.verdict_R0(b, g, v, c=c) for b in th]
        do_ = [x for x in vaa if x != 'INSUFFICIENT_EVIDENCE']
        kb = sum(1 for x in do_ if x == 'CAUSE_FOUND')
        kc = sum(1 for x in vth if x == 'CAUSE_FOUND')
        r[ds] = {'b': {'k': kb, 'n': len(do_), 'ty_le': round(kb / len(do_), 6) if do_ else None,
                       'wilson95': wilson(kb, len(do_)), 'insufficient': len(vaa) - len(do_),
                       'do_duoc': len(do_) >= MIN_CUA_SO_B,
                       'chi_nho_NEW_OP_STOPPED': sum(1 for b in aa if t046.chi_nho_truc_tiep(b, g, v, c))},
                 'c1': {'k': kc, 'n': len(vth), 'ty_le': round(kc / len(vth), 6) if vth else None,
                        'wilson95': wilson(kc, len(vth)),
                        'insufficient': sum(1 for x in vth if x == 'INSUFFICIENT_EVIDENCE'),
                        'chi_nho_NEW_OP_STOPPED': sum(1 for b in th if t046.chi_nho_truc_tiep(b, g, v, c))}}
    r['dat_b'] = all(r[d]['b']['do_duoc'] and r[d]['b']['ty_le'] <= MUC_B for d in ('RE2-TT', 'Nezha-OB'))
    r['b_khong_do_duoc'] = [d for d in ('RE2-TT', 'Nezha-OB') if not r[d]['b']['do_duoc']]
    r['dat_c1'] = all(r[d]['c1']['ty_le'] >= MUC_C1 for d in ('RE2-TT', 'Nezha-OB'))
    return r


LUOI_Q = [round(0.005 * i, 3) for i in range(1, 201)]


def chon_k(ca, g, c):
    """q* nhỏ nhất trong lưới 0,005..1,000 cho tỷ lệ CAUSE_FOUND ở A/A R0 <= 0,20 ở mọi dataset đo được (C2, sửa 15:01).
    So sánh dùng đúng verdict_R0 (tỷ lệ đơn vị có cờ / đơn vị có phép hợp lệ >= q)."""
    so = {}
    for ds in ('RE2-TT', 'Nezha-OB'):
        so[ds] = []
        for x in ca.values():
            b = x['cua_so']['aa|R0']['bang']
            if x['dataset'] == ds and b['so_cham_hop_le'] > 0:
                so[ds].append(round(t046.so_don_vi_co(b, g, c) / max(t046.so_don_vi_hop_le(b), 1), 6))
    do_ = [ds for ds in so if len(so[ds]) >= MIN_CUA_SO_B]
    for q in LUOI_Q:
        ok = True
        for ds in do_:
            aa = [x['cua_so']['aa|R0']['bang'] for x in ca.values() if x['dataset'] == ds]
            vs = [t046.verdict_R0(b, g, f'V4:{q}', c=c) for b in aa]
            do = [v for v in vs if v != 'INSUFFICIENT_EVIDENCE']
            if sum(1 for v in do if v == 'CAUSE_FOUND') / len(do) > MUC_B:
                ok = False
                break
        if ok:
            return q, {ds: sorted(v) for ds, v in so.items()}
    return None, {ds: sorted(v) for ds, v in so.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cu', required=True)
    ap.add_argument('--moi', required=True)
    ap.add_argument('--chan-doan', required=True)
    ap.add_argument('--ra-danh-gia', required=True)
    ap.add_argument('--ra-khoa', required=True)
    ap.add_argument('--g3-tinh', default=None)
    a = ap.parse_args()
    if Path(a.ra_khoa).exists():
        raise SystemExit('tệp khóa đã có: không ghi đè')
    cd = json.loads(Path(a.chan_doan).read_bytes().decode('utf-8'))
    ca, kiem = t046.nap_ghep(a.cu, a.moi)
    g, c, pv, dm = minimax(cd)
    out = {'ban': 4, 'luot_cu': a.cu, 'luot_moi': a.moi, 'kiem_ghep': kiem, 'chan_doan': a.chan_doan,
           'sha256_chan_doan': hashlib.sha256(Path(a.chan_doan).read_bytes()).hexdigest(),
           'muc': {'b': MUC_B, 'c1': MUC_C1, 'min_cua_so_b': MIN_CUA_SO_B, 'k_max': K_MAX},
           'minimax': {'cong_phan_vi': g, 'cong_dem': c, 'phan_vi': pv, 'dem': dm}, 'to_hop': {}, 'vet': []}
    if a.g3_tinh:
        out['g3_tinh'] = {'thu_muc': a.g3_tinh, 'so_phep_thay': ap_tinh(ca, a.g3_tinh)}
    chon = None
    ket = None
    for v in ('V0', 'V3', 'V1'):
        if v == 'V1' and g in ('G3', 'G4') and not a.g3_tinh:
            out['vet'].append({'to_hop': f'{g}|{c}|V1', 'ghi_chu': 'cần tinh p G3 theo A3 điểm 6'})
            ket = 'can_tinh_G3_V1'
            break
        r = mot_to_hop(ca, g, c, v)
        out['to_hop'][f'{g}|{c}|{v}'] = r
        out['vet'].append({'to_hop': f'{g}|{c}|{v}', 'dat_b': r['dat_b'], 'dat_c1': r['dat_c1']})
        if r['dat_b'] and r['dat_c1']:
            chon, ket = f'{g}|{c}|{v}', 'chon'
            break
    if ket is None:
        k, so = chon_k(ca, g, c)
        out['V4'] = {'q_sao': k, 'ty_le_don_vi_co_aa': so}
        if k is None:
            ket = 'khong_co_k'
        else:
            v = f'V4:{k}'
            r = mot_to_hop(ca, g, c, v)
            out['to_hop'][f'{g}|{c}|{v}'] = r
            out['vet'].append({'to_hop': f'{g}|{c}|{v}', 'dat_b': r['dat_b'], 'dat_c1': r['dat_c1']})
            ket, chon = ('chon', f'{g}|{c}|{v}') if (r['dat_b'] and r['dat_c1']) else ('V4_truot_c1', None)
    out['luat_chon'] = {'ket_qua': ket, 'to_hop_chon': chon}
    du = (json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    Path(a.ra_danh_gia).write_bytes(du)
    print('ket_qua', ket, 'to_hop', chon, 'sha256_danh_gia', hashlib.sha256(du).hexdigest())
    if ket == 'chon':
        out['nguong'] = cd['nguong']  # để b6_sau_khoa đọc cùng định dạng; GE/DE không dùng ở bản 4
        du2 = (json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
        Path(a.ra_khoa).write_bytes(du2)
        print('sha256_ung_vien', hashlib.sha256(du2).hexdigest())


if __name__ == '__main__':
    main()
