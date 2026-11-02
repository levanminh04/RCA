"""T-046 bước 6–7: tổng hợp phép sau khóa và thang điểm (SPEC T-046 bước 6, 7; (b′), (c2), (S); A5; S9; bản 3 B6).
Không đọc nhãn, không tính MRR. Bộ khóa 'g|c|v' và ngưỡng GE/DE đọc từ `ung-vien.json`.

- (b′): tỷ lệ CAUSE_FOUND của bộ khóa ở 30 cửa sổ C-e RE2-TT (cửa sổ có phép hợp lệ; INSUFFICIENT_EVIDENCE riêng);
  so mức (b) = 0,20; kèm (G0, D0, V0) để đối chiếu.
- (a′) (chỉ khi bộ khóa có GE hoặc DE): tỷ lệ qua cổng ở C-e theo ô (nhóm, hướng) <= 2α.
- (c2): theo cặp cùng ca RE2-TT, số đơn vị có cờ theo bộ khóa ở cửa sổ thật (bảng ghép b3 + b3b) so với C-e.
- K-đủ (A5, chỉ báo cáo): tỷ lệ CAUSE_FOUND ở A/A và cửa sổ thật theo V0 (chuỗi), V3, V1.
- C3 / (S): tỷ lệ kênh phân vị có cờ đạt rA = 1 ở cửa sổ thật của R0 với cổng khóa, riêng từng dataset và gộp, theo
  nhóm; mở thay thang khi một trong ba số >= 25%. Thực thể hòa ở phần tử đầu của khóa tầng 1; bão hòa trên K-đủ.

Chạy: $PY -B results/T-046/scripts/b6_tong_hop.py --ung-vien results/T-046/ung-vien.json --cu results/T-046/runs/b3-aa-001
      --moi results/T-046/runs/b3b-aa-001 --luot results/T-046/runs/<lượt b6>
      --ra-kiem results/T-046/kiem-sau-khoa.json --ra-thang results/T-046/thang-diem.json
"""
import argparse
import hashlib
import json
import statistics
from pathlib import Path

import t046
from t046 import wilson
from b6_sau_khoa import _so_co, _bao_hoa, nguong_ds

ALPHA = 0.01
MUC_B, MUC_S = 0.20, 0.25


def _doc(d):
    return {f.stem: json.loads(f.read_bytes().decode('utf-8')) for f in sorted(Path(d).glob('*.json'))}


def _ty(k, n):
    return {'k': k, 'n': n, 'ty_le': round(k / n, 6) if n else None, 'wilson95': wilson(k, n)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ung-vien', required=True)
    ap.add_argument('--cu', required=True)
    ap.add_argument('--moi', required=True)
    ap.add_argument('--luot', required=True)
    ap.add_argument('--ra-kiem', required=True)
    ap.add_argument('--ra-thang', required=True)
    a = ap.parse_args()
    du = Path(a.ung_vien).read_bytes()
    uv = json.loads(du.decode('utf-8'))
    k = uv['luat_chon']['to_hop_chon']
    g, c, v = k.split('|')
    ca, _ = t046.nap_ghep(a.cu, a.moi)
    luot = Path(a.luot)
    kiem = {'bo_khoa': k, 'sha256_ung_vien': hashlib.sha256(du).hexdigest()}
    ng = {ds: nguong_ds(uv, ds) for ds in ('RE2-TT', 'Nezha-OB')}
    ce = _doc(luot / 'ce') if (luot / 'ce').exists() else {}
    if ce:
        kiem['ce_trung_T045'] = sum(1 for x in ce.values() if x['trung_T045'])
        for ten in sorted(next(iter(ce.values()))['verdict']):
            vs = [x['verdict'][ten] for x in ce.values()]
            do = [x for x in vs if x != 'INSUFFICIENT_EVIDENCE']
            kk = sum(1 for x in do if x == 'CAUSE_FOUND')
            kiem[f'b_phay|{ten}'] = dict(_ty(kk, len(do)), insufficient=len(vs) - len(do))
        kiem['b_phay'] = dict(kiem['b_phay|khoa'], muc=MUC_B,
                              dat=kiem['b_phay|khoa']['ty_le'] is not None and kiem['b_phay|khoa']['ty_le'] <= MUC_B,
                              chi_nho_truc_tiep=sum(1 for x in ce.values() if x['chi_nho_truc_tiep']))
        kiem['verdict_chuoi_bo_khoa_khop_V0'] = None
        if v == 'V0':
            kiem['verdict_chuoi_bo_khoa_khop_V0'] = sum(1 for x in ce.values()
                                                       if x['verdict_chuoi_bo_khoa'] == x['verdict']['khoa'])
        if True:  # bản 4: luôn báo tỷ lệ qua cổng theo ô ở C-e (chỉ mô tả khi không có GE/DE)
            o = {}
            for x in ce.values():
                for kk, r in x['phep_theo_o'].items():
                    t = o.setdefault(kk, {'n': 0, 'qua': 0})
                    t['n'] += r['n']
                    t['qua'] += r['qua']
            kiem['a_phay'] = {kk: dict(_ty(r['qua'], r['n']), dat=r['qua'] / r['n'] <= 2 * ALPHA if r['n'] else None)
                              for kk, r in sorted(o.items())}
            kiem['a_phay_dat'] = (all(x['dat'] for x in kiem['a_phay'].values() if x['dat'] is not None)
                                  if (g == 'GE' or c == 'DE') else 'khong_ap_dung (chỉ báo cáo)')
        cap = []
        for oid, x in ce.items():
            th = ca[oid]['cua_so']['that|R0']['bang']
            cap.append({'ca': oid, 'that': _so_co(th, g, c, ng['RE2-TT'])['don_vi_co'], 'ce': x['so_co']['khoa']['don_vi_co'],
                        'ty_le_that': round(t046.so_don_vi_co(th, g, c, ng['RE2-TT']) / max(t046.so_don_vi_hop_le(th), 1), 6),
                        'ty_le_ce': round(x.get('ty_le_don_vi_co', float('nan')), 6)})
        ht = {}
        for x in ce.values():
            for kk, r in (x.get('phep_theo_hau_to') or {}).items():
                t = ht.setdefault(kk, {'n': 0, 'qua': 0})
                t['n'] += r['n']
                t['qua'] += r['qua']
        if all('doi_chung_G1' in x for x in ce.values()):  # N5: chỉ báo cáo
            o1 = {}
            for x in ce.values():
                for kk, r in x['doi_chung_G1']['phep_theo_o'].items():
                    t = o1.setdefault(kk, {'n': 0, 'qua': 0})
                    t['n'] += r['n']
                    t['qua'] += r['qua']
            kiem['doi_chung_G1_ce'] = {
                'V0_CAUSE_FOUND': sum(1 for x in ce.values() if x['doi_chung_G1']['verdict_V0'] == 'CAUSE_FOUND'),
                'so_ca': len(ce),
                'don_vi_co_trung_vi': statistics.median(x['doi_chung_G1']['so_co']['don_vi_co'] for x in ce.values()),
                'ty_le_don_vi_co_trung_vi': statistics.median(x['doi_chung_G1']['ty_le_don_vi_co'] for x in ce.values()),
                'qua_cong_theo_o': {kk: _ty(r['qua'], r['n']) for kk, r in sorted(o1.items())}}
        kiem['qua_cong_ce_theo_hau_to'] = {kk: _ty(r['qua'], r['n']) for kk, r in sorted(ht.items())}
        kiem['c2'] = {'cap': sorted(cap, key=lambda z: z['ca']),
                      'that_lon_hon': sum(1 for z in cap if z['that'] > z['ce']),
                      'bang': sum(1 for z in cap if z['that'] == z['ce']),
                      'that_nho_hon': sum(1 for z in cap if z['that'] < z['ce']),
                      'trung_vi_that': statistics.median(z['that'] for z in cap),
                      'trung_vi_ce': statistics.median(z['ce'] for z in cap),
                      'ty_le_that_lon_hon': sum(1 for z in cap if z['ty_le_that'] > z['ty_le_ce']),
                      'ty_le_trung_vi_that': statistics.median(z['ty_le_that'] for z in cap),
                      'ty_le_trung_vi_ce': statistics.median(z['ty_le_ce'] for z in cap)}
    kdu = _doc(luot / 'kdu') if (luot / 'kdu').exists() else {}
    if kdu:
        r = {}
        for kieu in ('aa', 'that', 'ce'):
            for ds in ('RE2-TT', 'Nezha-OB'):
                xs = [x[kieu] for x in kdu.values() if x['dataset'] == ds and kieu in x]
                if not xs:
                    continue
                o = {}
                for x in xs:
                    for kk, rr in x.get('phep_theo_o', {}).items():
                        t = o.setdefault(kk, {'n': 0, 'qua': 0})
                        t['n'] += rr['n']
                        t['qua'] += rr['qua']
                r[f'{kieu}|{ds}|qua_cong_theo_o'] = {kk: _ty(t['qua'], t['n']) for kk, t in sorted(o.items())}
                r[f'{kieu}|{ds}|ty_le_don_vi_co_trung_vi'] = statistics.median(x['ty_le_don_vi_co'] for x in xs)
                for vv in xs[0]['verdict'] if xs else ():
                    vs = [x['verdict'][vv] for x in xs]
                    do = [x for x in vs if x != 'INSUFFICIENT_EVIDENCE'] if kieu == 'aa' else vs
                    kk = sum(1 for x in do if x == 'CAUSE_FOUND')
                    r[f'{kieu}|{ds}|{vv}'] = dict(_ty(kk, len(do)), insufficient=sum(
                        1 for x in vs if x == 'INSUFFICIENT_EVIDENCE'))
                r[f'{kieu}|{ds}|V0_khop_chuoi'] = sum(1 for x in xs if x['verdict']['V0'] == x['verdict_chuoi'])
        kiem['K_du'] = r
    Path(a.ra_kiem).write_bytes((json.dumps(kiem, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    thang = {'bo_khoa': k, 'cong_khoa': g, 'muc_S': MUC_S}
    bh = {}
    for oid, x in ca.items():
        ds = x['dataset']
        for nhom, cc in _bao_hoa(x['cua_so']['that|R0']['bang'], g, ng[ds]).items():
            for key in (ds, 'gop'):
                o = bh.setdefault(key, {}).setdefault(nhom, {'co': 0, 'rA_1': 0})
                o['co'] += cc['co']
                o['rA_1'] += cc['rA_1']
    s = {}
    for key, nh in bh.items():
        co = sum(cc['co'] for cc in nh.values())
        r1 = sum(cc['rA_1'] for cc in nh.values())
        s[key] = {'theo_nhom': nh, 'co': co, 'rA_1': r1, 'ty_le': round(r1 / co, 6) if co else None, 'wilson95': wilson(r1, co)}
    thang['bao_hoa_R0_that'] = s
    thang['mo_thay_thang'] = any(x['ty_le'] is not None and x['ty_le'] >= MUC_S for x in s.values())
    r0 = _doc(luot / 'r0') if (luot / 'r0').exists() else {}
    if r0:
        tt = {}
        for ds in ('RE2-TT', 'Nezha-OB'):
            xs = [x for x in r0.values() if x['dataset'] == ds]
            tt[ds] = {'so_cua_so': len(xs),
                      'hoa_dinh_trung_vi': statistics.median(x['hoa_phan_tu_dau_o_dinh'] for x in xs) if xs else None,
                      'cua_so_hoa_dinh_tren_1': sum(1 for x in xs if x['hoa_phan_tu_dau_o_dinh'] > 1),
                      'tang1_s_bang_1_trung_vi': statistics.median(x['tang1_s_bang_1'] for x in xs) if xs else None,
                      'khoi_dau_nhieu_thuc_the': sum(1 for x in xs if x['so_thuc_the_khoi_dau'] > 1),
                      'khoi_dau_nhieu_thuc_the_T4c': sum(1 for x in xs if (x.get('so_thuc_the_khoi_dau_T4c') or 0) > 1),
                      'khoi_dau_trung_vi': statistics.median(x['so_thuc_the_khoi_dau'] for x in xs) if xs else None,
                      'khoi_dau_trung_vi_T4c': statistics.median(x['so_thuc_the_khoi_dau_T4c'] or 0 for x in xs) if xs else None,
                      'so_khoi_trung_vi': statistics.median(x['so_khoi'] for x in xs) if xs else None,
                      'so_khoi_trung_vi_T4c': statistics.median(x['so_khoi_T4c'] or 0 for x in xs) if xs else None,
                      'tang1_trung_vi': statistics.median(x['tang1'] for x in xs) if xs else None,
                      'R4_doi_khoi_dau': sum(1 for x in xs if (x.get('doi_hang_T4c') or {}).get('doi_khoi_dau')),
                      'R4_doi_thuc_the_dau': sum(1 for x in xs if (x.get('doi_hang_T4c') or {}).get('doi_thuc_the_dau_duy_nhat')),
                      'R4_cap_doi_quan_he': sum((x.get('doi_hang_T4c') or {}).get('cap_doi_quan_he', 0) for x in xs),
                      'R4_so_cap_tang1': sum((x.get('doi_hang_T4c') or {}).get('so_cap_tang1', 0) for x in xs),
                      'verdict_chuoi_khop_bo_khoa_V0': (sum(1 for x in xs if x['verdict_chuoi'] == x['verdict_bo_khoa'])
                                                        if v == 'V0' else None)}
        thang['hoa_khoa_tang1'] = tt
    if kdu:
        bk = {}
        for x in kdu.values():
            for nhom, cc in x['that']['bao_hoa'].items():
                o = bk.setdefault(x['dataset'], {}).setdefault(nhom, {'co': 0, 'rA_1': 0})
                o['co'] += cc['co']
                o['rA_1'] += cc['rA_1']
        thang['bao_hoa_K_du_that_chi_bao_cao'] = bk
    Path(a.ra_thang).write_bytes((json.dumps(thang, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    print(json.dumps({'b_phay': kiem.get('b_phay'), 'a_phay_dat': kiem.get('a_phay_dat'),
                      'mo_thay_thang': thang['mo_thay_thang']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
