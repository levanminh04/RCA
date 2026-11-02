"""T-046 bước 5: tính (a), (b), (c1) cho mọi tổ hợp cổng × verdict, áp luật chọn và ghi phần khóa (SPEC T-046 bảng
mức, Luật chọn, A3 điểm 6–7, A6). Không đọc nhãn, không đọc C-e.

- (a) theo cổng: mọi ô phân vị (cấu hình, dataset, nhóm) của `chan-doan-cong.json`, trừ metric Nezha-OB, đo được
  (>= 100 phép) và tỷ lệ qua cổng ở A/A <= 2α.
- (b) theo tổ hợp và dataset: tỷ lệ CAUSE_FOUND ở cửa sổ A/A của R0 có ít nhất một phép hợp lệ; INSUFFICIENT_EVIDENCE
  báo riêng; dataset dưới 10 cửa sổ đo được là không đo được; mức <= 0,20 cho từng dataset; báo số gộp.
- (c1) theo tổ hợp và dataset: tỷ lệ CAUSE_FOUND ở cửa sổ thật của R0, mọi cửa sổ trong mẫu số; mức >= 0,80 cho
  từng dataset; báo số gộp.
- Luật chọn: tổ hợp đầu tiên theo thứ tự cổng trước (G0, V0), (G0, V3), (G0, V1), (G1, V0), … đạt (a), (b), (c1).
  Đi tới (G3, V1) thì dừng: cần tinh p theo A3 điểm 6 trước khi xét.
- Báo kèm: số cửa sổ CAUSE_FOUND chỉ nhờ NEW_OP/STOPPED; chẩn đoán phân giải A3 điểm 6 (G3 × V1) và điểm 7 (G1 × V1).

Chạy: $PY -B results/T-046/scripts/b5_danh_gia.py --luot results/T-046/runs/b3-aa-001
      --chan-doan results/T-046/chan-doan-cong.json --ra results/T-046/ung-vien.json
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import t046
from t046 import wilson

ALPHA = 0.01
MUC_A, MUC_B, MUC_C1 = 2 * ALPHA, 0.20, 0.80
MIN_CUA_SO_B = 10
THU_TU = [(g, v) for g in ('G0', 'G1', 'G3') for v in ('V0', 'V3', 'V1')]


def dat_a(cd):
    out = {}
    for g in t046.CONG:
        o_ = {}
        for o, q in cd['qua_cong_aa'].items():
            if o.endswith('|Nezha-OB|metric'):
                continue
            do_duoc = cd['ho_tro'][o]['do_duoc']
            r = q[g]['ty_le']
            o_[o] = {'ty_le': r, 'n': q[g]['n'], 'do_duoc': do_duoc, 'dat': bool(do_duoc and r <= MUC_A)}
        out[g] = {'o': o_, 'dat': all(x['dat'] for x in o_.values()),
                  'khong_do_duoc': sorted(o for o, x in o_.items() if not x['do_duoc'])}
    return out


def _phan_giai(bang, g):
    """Chẩn đoán A3 điểm 6, 7 cho một cửa sổ: m, số phép phân vị mà p nhỏ nhất đạt được > α/m."""
    phep, _ = t046.co_theo_cong(bang, g)
    m = len(phep)
    if not m:
        return {'m': 0, 'khong_the_qua_buoc_dau': 0}
    nguong = ALPHA / m
    k = 0
    for u in bang['pv']:
        if not (u['hop_le'] and u['trong_U']):
            continue
        kh = u.get('khoi') or {}
        for d, h in u['huong'].items():
            cach = h.get(f'cach_{g}') or ''
            if g == 'G3' and cach == 'G3':
                ct = h.get('G3') or {}
                pmin = 1 / ct['so_cach'] if ct.get('cach') == 'duyet_het' else 1 / (2000 + 1)
            elif g == 'G1' and cach == 'G1:chinh_xac':
                pmin = 1 / math.comb(kh['so_khoi_N'] + kh['so_khoi_A'], kh['so_khoi_A'])
            else:
                continue
            k += int(pmin >= nguong)
    return {'m': m, 'khong_the_qua_buoc_dau': k}


def danh_gia(ca):
    kq = {}
    for g, v in THU_TU:
        r = {}
        for ds in ('RE2-TT', 'Nezha-OB'):
            aa = [x['cua_so']['aa|R0']['bang'] for x in ca.values() if x['dataset'] == ds]
            th = [x['cua_so']['that|R0']['bang'] for x in ca.values() if x['dataset'] == ds]
            vaa = [t046.verdict_R0(b, g, v) for b in aa]
            vth = [t046.verdict_R0(b, g, v) for b in th]
            do_ = [x for x in vaa if x != 'INSUFFICIENT_EVIDENCE']
            kb = sum(1 for x in do_ if x == 'CAUSE_FOUND')
            kc = sum(1 for x in vth if x == 'CAUSE_FOUND')
            r[ds] = {
                'b': {'k': kb, 'n': len(do_), 'ty_le': round(kb / len(do_), 6) if do_ else None,
                      'wilson95': wilson(kb, len(do_)), 'insufficient': len(vaa) - len(do_),
                      'do_duoc': len(do_) >= MIN_CUA_SO_B,
                      'chi_nho_NEW_OP_STOPPED': sum(1 for b in aa if t046.chi_nho_truc_tiep(b, g, v))},
                'c1': {'k': kc, 'n': len(vth), 'ty_le': round(kc / len(vth), 6) if vth else None,
                       'wilson95': wilson(kc, len(vth)),
                       'insufficient': sum(1 for x in vth if x == 'INSUFFICIENT_EVIDENCE'),
                       'chi_nho_NEW_OP_STOPPED': sum(1 for b in th if t046.chi_nho_truc_tiep(b, g, v))}}
            if v == 'V1' and g in ('G1', 'G3'):
                pg = [_phan_giai(b, g) for b in aa]
                r[ds]['phan_giai_aa'] = {'m_trung_vi': sorted(x['m'] for x in pg)[len(pg) // 2] if pg else None,
                                         'phep_khong_the_qua_buoc_dau': sum(x['khong_the_qua_buoc_dau'] for x in pg)}
                pg = [_phan_giai(b, g) for b in th]
                r[ds]['phan_giai_that'] = {'m_trung_vi': sorted(x['m'] for x in pg)[len(pg) // 2] if pg else None,
                                           'phep_khong_the_qua_buoc_dau': sum(x['khong_the_qua_buoc_dau'] for x in pg)}
        nb = sum(r[d]['b']['n'] for d in r)
        kb = sum(r[d]['b']['k'] for d in r)
        nc = sum(r[d]['c1']['n'] for d in r)
        kc = sum(r[d]['c1']['k'] for d in r)
        r['gop'] = {'b': {'k': kb, 'n': nb, 'ty_le': round(kb / nb, 6) if nb else None, 'wilson95': wilson(kb, nb)},
                    'c1': {'k': kc, 'n': nc, 'ty_le': round(kc / nc, 6) if nc else None, 'wilson95': wilson(kc, nc)}}
        r['dat_b'] = all(r[d]['b']['do_duoc'] and r[d]['b']['ty_le'] <= MUC_B for d in ('RE2-TT', 'Nezha-OB'))
        r['b_khong_do_duoc'] = [d for d in ('RE2-TT', 'Nezha-OB') if not r[d]['b']['do_duoc']]
        r['dat_c1'] = all(r[d]['c1']['ty_le'] >= MUC_C1 for d in ('RE2-TT', 'Nezha-OB'))
        kq[f'{g}|{v}'] = r
    return kq


def chon(a_, to_hop):
    vet = []
    for g, v in THU_TU:
        k = f'{g}|{v}'
        x = to_hop[k]
        if (g, v) == ('G3', 'V1'):
            dat = a_[g]['dat'] and x['dat_b'] and x['dat_c1']
            vet.append({'to_hop': k, 'dat_a': a_[g]['dat'], 'dat_b': x['dat_b'], 'dat_c1': x['dat_c1'],
                        'ghi_chu': 'tới G3 × V1: dừng, cần tinh p theo A3 điểm 6 trước khi xét (số ở B = 2.000 chỉ báo cáo)'})
            return None, vet, 'can_tinh_G3_V1'
        vet.append({'to_hop': k, 'dat_a': a_[g]['dat'], 'dat_b': x['dat_b'], 'dat_c1': x['dat_c1']})
        if a_[g]['dat'] and x['dat_b'] and x['dat_c1']:
            return k, vet, 'chon'
    return None, vet, 'khong_to_hop_nao_dat'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luot', required=True)
    ap.add_argument('--chan-doan', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    cd = json.loads(Path(a.chan_doan).read_bytes().decode('utf-8'))
    ca = t046.nap_luot(a.luot)
    a_ = dat_a(cd)
    to_hop = danh_gia(ca)
    k, vet, ket = chon(a_, to_hop)
    out = {'luot': a.luot, 'chan_doan': a.chan_doan,
           'sha256_chan_doan': hashlib.sha256(Path(a.chan_doan).read_bytes()).hexdigest(),
           'muc': {'a': MUC_A, 'b': MUC_B, 'c1': MUC_C1, 'min_cua_so_b': MIN_CUA_SO_B}, 'thu_tu': [f'{g}|{v}' for g, v in THU_TU],
           'a': a_, 'to_hop': to_hop, 'luat_chon': {'ket_qua': ket, 'to_hop_chon': k, 'vet': vet}}
    du = (json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    Path(a.ra).write_bytes(du)
    print('ket_qua', ket, 'to_hop', k)
    print('sha256', hashlib.sha256(du).hexdigest())


if __name__ == '__main__':
    main()
