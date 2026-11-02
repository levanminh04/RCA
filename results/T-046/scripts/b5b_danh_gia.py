"""T-046 bước 5 bản 3: tính (a), (b), (c1) và áp luật chọn B3 (SPEC T-046 bảng mức; B1–B3; A3 điểm 6; A6).
Không đọc nhãn, không đọc C-e. Thay `b5_danh_gia.py` (bản 2, chưa chạy).

- (a) cổng phân vị g ∈ {G0, G1, G3, G4}: mọi ô phân vị (cấu hình, dataset, nhóm) trừ metric Nezha-OB, đo được và tỷ lệ
  qua cổng ở A/A <= 2α (`chan-doan-cong-ban3.json#/qua_cong_aa`). GE: không có (a) trên A/A; đạt điều kiện vào luật khi
  mọi ô hiệu chuẩn được có ngưỡng (không ô nào "trượt"); (a′) kiểm sau khóa trên C-e (B6).
- (a) cổng đếm c ∈ {D0, D1}: mọi ô đếm đo được, tỷ lệ qua cổng ở A/A <= 2α (`#/don_vi_dem`). DE: như GE.
- (b), (c1) cho từng dataset như bản 2 (`b5_danh_gia.py`), với ngưỡng GE/DE theo ô của dataset (`#/nguong`).
- Thứ tự: g (G0, G1, G3, G4, GE) → c (D0, D1, DE) → v (V0, V3, V1); bỏ V1 khi g = GE hoặc c = DE. Chọn bộ đầu tiên
  đạt. Tới bộ có V1 với G3 hoặc G4 mà (a) của g và c đều đạt: dừng, cần tinh p G3 theo A3 điểm 6 trước khi xét.

Chạy: $PY -B results/T-046/scripts/b5b_danh_gia.py --cu results/T-046/runs/b3-aa-001 --moi results/T-046/runs/b3b-aa-001
      --chan-doan results/T-046/chan-doan-cong-ban3.json --ra results/T-046/ung-vien.json
"""
import argparse
import hashlib
import json
from pathlib import Path

import t046
from t046 import wilson

ALPHA = 0.01
MUC_A, MUC_B, MUC_C1 = 2 * ALPHA, 0.20, 0.80
MIN_CUA_SO_B = 10
CONG_PV = ('G0', 'G1', 'G3', 'G4', 'GE')
CONG_DEM = ('D0', 'D1', 'DE')
VERDICT = ('V0', 'V3', 'V1')


def thu_tu():
    for g in CONG_PV:
        for c in CONG_DEM:
            for v in VERDICT:
                if v == 'V1' and (g == 'GE' or c == 'DE'):
                    continue
                yield g, c, v


def dat_a(cd):
    pv = {}
    for g in CONG_PV:
        if g == 'GE':
            truot = sorted(k for k, r in cd['nguong']['GE'].items() if r['truot'])
            pv[g] = {'dat': not truot, 'ghi_chu': '(a) thay bằng (a′) sau khóa', 'o_truot': truot}
            continue
        o_ = {}
        for k, q in cd['qua_cong_aa'].items():
            if k.endswith('|Nezha-OB|metric'):
                continue
            do_ = cd['ho_tro'][k]['do_duoc']
            o_[k] = {'ty_le': q[g]['ty_le'], 'n': q[g]['n'], 'do_duoc': do_, 'dat': bool(do_ and q[g]['ty_le'] <= MUC_A)}
        pv[g] = {'dat': all(x['dat'] for x in o_.values()), 'o': o_}
    dem = {}
    for c in CONG_DEM:
        if c == 'DE':
            truot = sorted(k for k, r in cd['nguong']['DE'].items() if r['truot'])
            dem[c] = {'dat': not truot, 'ghi_chu': '(a) thay bằng (a′) sau khóa', 'o_truot': truot}
            continue
        o_ = {}
        for k, r in cd['don_vi_dem'].items():
            o_[k] = {'ty_le': r[c]['ty_le'], 'n': r[c]['n'], 'do_duoc': r['do_duoc'],
                     'dat': (r[c]['ty_le'] <= MUC_A) if r['do_duoc'] else None}
        dem[c] = {'dat': all(x['dat'] for x in o_.values() if x['do_duoc']),
                  'o_khong_do_duoc': sorted(k for k, x in o_.items() if not x['do_duoc']), 'o': o_}
    return pv, dem


def nguong_ds(cd, ds):
    out = {}
    for loai in ('GE', 'DE'):
        out[loai] = {}
        for k, r in cd['nguong'][loai].items():
            d_, nhom, h = k.split('|')
            if d_ == ds:
                out[loai][(nhom, h)] = r['nguong']
    return out


def danh_gia(ca, cd):
    ng = {ds: nguong_ds(cd, ds) for ds in ('RE2-TT', 'Nezha-OB')}
    kq = {}
    for g, c, v in thu_tu():
        r = {}
        for ds in ('RE2-TT', 'Nezha-OB'):
            nguong = {}
            if g == 'GE':
                nguong.update(ng[ds]['GE'])
            if c == 'DE':
                nguong.update({k: a for k, a in ng[ds]['DE'].items()})
            aa = [x['cua_so']['aa|R0']['bang'] for x in ca.values() if x['dataset'] == ds]
            th = [x['cua_so']['that|R0']['bang'] for x in ca.values() if x['dataset'] == ds]
            vaa = [t046.verdict_R0(b, g, v, c=c, nguong=nguong) for b in aa]
            vth = [t046.verdict_R0(b, g, v, c=c, nguong=nguong) for b in th]
            do_ = [x for x in vaa if x != 'INSUFFICIENT_EVIDENCE']
            kb = sum(1 for x in do_ if x == 'CAUSE_FOUND')
            kc = sum(1 for x in vth if x == 'CAUSE_FOUND')
            r[ds] = {'b': {'k': kb, 'n': len(do_), 'ty_le': round(kb / len(do_), 6) if do_ else None,
                           'wilson95': wilson(kb, len(do_)), 'insufficient': len(vaa) - len(do_),
                           'do_duoc': len(do_) >= MIN_CUA_SO_B,
                           'chi_nho_NEW_OP_STOPPED': sum(1 for b in aa if t046.chi_nho_truc_tiep(b, g, v, c, nguong))},
                     'c1': {'k': kc, 'n': len(vth), 'ty_le': round(kc / len(vth), 6) if vth else None,
                            'wilson95': wilson(kc, len(vth)),
                            'insufficient': sum(1 for x in vth if x == 'INSUFFICIENT_EVIDENCE'),
                            'chi_nho_NEW_OP_STOPPED': sum(1 for b in th if t046.chi_nho_truc_tiep(b, g, v, c, nguong))}}
        nb = sum(r[d]['b']['n'] for d in ('RE2-TT', 'Nezha-OB'))
        kb = sum(r[d]['b']['k'] for d in ('RE2-TT', 'Nezha-OB'))
        nc = sum(r[d]['c1']['n'] for d in ('RE2-TT', 'Nezha-OB'))
        kc = sum(r[d]['c1']['k'] for d in ('RE2-TT', 'Nezha-OB'))
        r['gop'] = {'b': {'k': kb, 'n': nb, 'ty_le': round(kb / nb, 6) if nb else None},
                    'c1': {'k': kc, 'n': nc, 'ty_le': round(kc / nc, 6) if nc else None}}
        r['dat_b'] = all(r[d]['b']['do_duoc'] and r[d]['b']['ty_le'] <= MUC_B for d in ('RE2-TT', 'Nezha-OB'))
        r['b_khong_do_duoc'] = [d for d in ('RE2-TT', 'Nezha-OB') if not r[d]['b']['do_duoc']]
        r['dat_c1'] = all(r[d]['c1']['ty_le'] >= MUC_C1 for d in ('RE2-TT', 'Nezha-OB'))
        kq[f'{g}|{c}|{v}'] = r
    return kq


def chon(a_pv, a_dem, to_hop):
    vet = []
    for g, c, v in thu_tu():
        k = f'{g}|{c}|{v}'
        x = to_hop[k]
        dong = {'to_hop': k, 'dat_a_phan_vi': a_pv[g]['dat'], 'dat_a_dem': a_dem[c]['dat'], 'dat_b': x['dat_b'],
                'dat_c1': x['dat_c1']}
        if v == 'V1' and g in ('G3', 'G4') and a_pv[g]['dat'] and a_dem[c]['dat']:
            dong['ghi_chu'] = 'cần tinh p G3 theo A3 điểm 6 trước khi xét; số ở B = 2.000 chỉ báo cáo'
            vet.append(dong)
            return None, vet, 'can_tinh_G3_V1'
        vet.append(dong)
        if a_pv[g]['dat'] and a_dem[c]['dat'] and x['dat_b'] and x['dat_c1']:
            return k, vet, 'chon'
    return None, vet, 'khong_to_hop_nao_dat'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cu', required=True)
    ap.add_argument('--moi', required=True)
    ap.add_argument('--chan-doan', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    if Path(a.ra).exists():
        raise SystemExit('tệp ra đã có: giữ mọi lượt, dùng tên mới')
    cd = json.loads(Path(a.chan_doan).read_bytes().decode('utf-8'))
    ca, kiem = t046.nap_ghep(a.cu, a.moi)
    a_pv, a_dem = dat_a(cd)
    to_hop = danh_gia(ca, cd)
    k, vet, ket = chon(a_pv, a_dem, to_hop)
    out = {'ban': 3, 'luot_cu': a.cu, 'luot_moi': a.moi, 'kiem_ghep': kiem, 'chan_doan': a.chan_doan,
           'sha256_chan_doan': hashlib.sha256(Path(a.chan_doan).read_bytes()).hexdigest(),
           'muc': {'a': MUC_A, 'b': MUC_B, 'c1': MUC_C1, 'min_cua_so_b': MIN_CUA_SO_B},
           'thu_tu': [f'{g}|{c}|{v}' for g, c, v in thu_tu()], 'nguong': cd['nguong'],
           'a_phan_vi': a_pv, 'a_dem': a_dem, 'to_hop': to_hop,
           'luat_chon': {'ket_qua': ket, 'to_hop_chon': k, 'vet': vet}}
    du = (json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    Path(a.ra).write_bytes(du)
    print('ket_qua', ket, 'to_hop', k)
    print('sha256', hashlib.sha256(du).hexdigest())


if __name__ == '__main__':
    main()
