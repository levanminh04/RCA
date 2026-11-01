"""T-045 phiên 2 — lần theo cơ chế bổ sung theo phản biện lượt 1 (REVIEW.md A1, A7). Chỉ mô tả, không đổi lựa chọn,
không chạy lại phương pháp. Đọc bản ghi pha 1 đã băm (qua `pha2_khoi_k.doc_ban_ghi`, có kiểm tệp tách) và nhãn dev ở
pha 2 (như `co_che_khoi_k.py`).

(A1) E5 tại E1+E2 (cặp E1+E2 → E1+E2+E5), theo ca và ô, cả ca root tụt lẫn ca root lên:
     - ca tụt: kênh của root bị E5 xóa (`inherited_by`, `ap_dung`) theo quy tắc nào;
     - ca lên: kênh của các thực thể từng đứng trước root mà nay không còn đứng trước, bị xóa theo quy tắc nào.
     E5 chỉ xóa kênh, nên root chỉ tụt khi chính root mất kênh và chỉ lên khi thực thể đứng trước mất kênh.
     Đối chiếu ca có điều kiện tương ứng (SPEC T-045 dòng 115): mọi ca root mất ít nhất một kênh, tách theo RR tụt,
     không đổi, lên.
(A1) Cờ M5 (codebook T-028 §4; `m1_danh_gia.m5`): ở K-R0, K-E1+E2, K-E1+E2+E5, ca có điều kiện "có e ≠ root,
     có đường e → root trong G_N, e có kênh tự sinh (F_I = 1) ở P" tách thành có cờ M5 (e đứng trước hẳn root) và
     không có cờ.
(A7) Hai phép không nhãn của E5 ở K-E1+E2+E5, thế giới P:
     (1) E9 sẽ phủ quyết bao nhiêu lần xóa: dựng lại kênh từ `extra.kenh_co_the_gioi.P` (khởi phát lấy từ
         `extra.kenh_co`), cạnh từ `extra.canh`; kiểm tái lập (E9 tắt phải ra đúng F_I và `inherited_by` của bản
         ghi); rồi chạy `e5.phan_loai` với E9 bật (Đ11, CĐ9; o_s = 10 s, τ = 1 ms như `chuoi._chay`). Cạnh E2 bất
         thường dựng lại từ đơn vị `canh|a|b` của kênh có cờ ở P (xấp xỉ: chỉ kênh của thực thể thuộc U).
     (2) Kênh giải thích của mỗi lần xóa có cờ ở cửa sổ giả cùng ca, cùng cấu hình, cùng mã kênh không (RE2-TT).
     Cả hai báo trên mọi lần xóa (không nhãn) và riêng phần xóa kênh root ở ca tụt (cần nhãn, pha 2).
(A7) Bảng ô mục tiêu (E_X) và ngoài mục tiêu cho E3, E5: P, M, P′, M′ và tổng ΔRR trong và ngoài E_X, theo dataset.
(A5) Tổng ΔRR theo ô cho E1 → E1+E2, E2 → E1+E2, R0 → E1+E2; phần đến từ các ô trễ mạng Nezha-OB.
Chạy: $PY -B results/T-045/scripts/co_che_bo_sung.py --ra results/T-045/co-che-bo-sung.json
"""
import argparse
import collections
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m1 import e5  # noqa: E402
from m1.chuoi import NS  # noqa: E402
from m1.kieu import Kenh  # noqa: E402
from m1_danh_gia import m5, rr  # noqa: E402
import pha2_khoi_k as pk  # noqa: E402

O_S, TAU = 10 * NS, 10 ** 6  # như chuoi._chay


def vi_tri(blocks):
    return {e: (bi, gi) for bi, b in enumerate(blocks or []) for gi, g in enumerate(b['groups']) for e in g}


def truoc(a, r):
    return a[0] < r[0] or (a[0] == r[0] and a[1] < r[1])


def f(x):
    return float(x) if isinstance(x, Fraction) else x


def nhom_quy_tac(qt):
    return 'nhom_vong' if qt.get('nhom_vong') else ('thuong' if qt else 'khong_xoa')


def e5_theo_ca(nhan, E_X):
    ds, tong, dc = [], collections.defaultdict(lambda: [0, Fraction(0)]), collections.defaultdict(list)
    for L in pk.LUOT_THAT:
        rt, rb = pk.doc_ban_ghi(L, 'K-E1+E2'), pk.doc_ban_ghi(L, 'K-E1+E2+E5')
        for o in sorted(rb):
            root, cell = nhan[o]['root'], nhan[o]['o']
            a, b = rr.rr_ca(rt[o]['blocks'] or [], root), rr.rr_ca(rb[o]['blocks'] or [], root)
            ib_root = [i for i in rb[o]['inherited_by'] if i['thuc_the'] == root and i['trang_thai'] == 'ap_dung']
            if ib_root:  # đối chiếu ca có điều kiện tương ứng: root mất ít nhất một kênh
                con_tu_sinh = any(k['F_I'] == 1 for k in rb[o]['extra']['kenh_co'] if k['thuc_the'] == root)
                dc['tut' if b < a else ('len' if b > a else 'khong_doi')].append(
                    {'ca': o, 'dataset': nhan[o]['dataset'], 'o': cell, 'RR': [f(a), f(b)],
                     'so_kenh_root_bi_xoa': len({i['ma'] for i in ib_root}),
                     'root_con_kenh_tu_sinh': con_tu_sinh,
                     'quy_tac': dict(collections.Counter(i['quy_tac'] for i in ib_root))})
            if a == b:
                continue
            vt, vb = vi_tri(rt[o]['blocks']), vi_tri(rb[o]['blocks'])
            if b < a:
                ai = {root}
            elif root in vt and root in vb:
                ai = {e for e in vt if truoc(vt[e], vt[root])} - {e for e in vb if truoc(vb[e], vb[root])}
            else:
                ai = set()
            qt = collections.Counter(i['quy_tac'] for i in rb[o]['inherited_by']
                                     if i['thuc_the'] in ai and i['trang_thai'] == 'ap_dung')
            huong = 'tut' if b < a else 'len'
            g = nhom_quy_tac(qt)
            tong[(huong, g)][0] += 1
            tong[(huong, g)][1] += b - a
            ds.append({'ca': o, 'dataset': nhan[o]['dataset'], 'o': cell, 'o_trong_E_X_E5': cell in E_X['E5'],
                       'huong': huong, 'RR': [f(a), f(b)], 'thuc_the_tinh': sorted(ai), 'quy_tac': dict(qt),
                       'nhom_quy_tac': g})
    rong = collections.defaultdict(Fraction)
    for (h, g), (n, s) in tong.items():
        rong[g] += s
    return {'ca': ds,
            'tong_theo_huong_va_quy_tac': {f'{h}|{g}': {'so_ca': n, 'tong_dRR': f(s)} for (h, g), (n, s) in sorted(tong.items())},
            'rong_theo_quy_tac': {g: f(s) for g, s in sorted(rong.items())},
            'tong_dRR': f(sum(rong.values(), Fraction(0))), 'tong_dMRR_52_ca': f(sum(rong.values(), Fraction(0)) / 52),
            'doi_chieu_root_mat_kenh': {k: {'so_ca': len(v), 'so_ca_root_con_tu_sinh': sum(x['root_con_kenh_tu_sinh'] for x in v),
                                            'ca': v} for k, v in sorted(dc.items())}}


def doi_chieu_M5(nhan):
    out = {}
    for cid in ('K-R0', 'K-E1+E2', 'K-E1+E2+E5'):
        nhom = collections.defaultdict(list)
        for L in pk.LUOT_THAT:
            for o, r in sorted(pk.doc_ban_ghi(L, cid).items()):
                root = nhan[o]['root']
                G_N = {tuple(c) for c in r['extra'].get('G_N') or []}
                b = r['blocks'] or []
                nguon = m5._toi({(x, y) for x, y in G_N if x != y}, root) - {root}
                tu_sinh = {k['thuc_the'] for k in r['extra']['kenh_co'] if k['F_I'] == 1}
                dk = sorted(nguon & tu_sinh)
                co = r['status'] == 'OK' and m5.co_M5(b, root, G_N)
                k = ('dieu_kien' if dk else 'khong_dieu_kien') + ('|M5' if co else '|khong_M5')
                nhom[k].append({'ca': o, 'dataset': nhan[o]['dataset'], 'o': nhan[o]['o'],
                                'RR': f(rr.rr_ca(b, root)), 'so_thuc_the_dieu_kien': len(dk)})
        out[cid] = {k: {'so_ca': len(v), 'RR_trung_binh': sum(x['RR'] for x in v) / len(v), 'ca': v}
                    for k, v in sorted(nhom.items())}
    return out


def dung_kenh(r, w='P'):
    kp = {k['ma']: k['khoi_phat'] for k in r['extra']['kenh_co']}
    return [Kenh(k['thuc_the'], k['ten'], k['huong'], k['lop'], k['s'], don_vi=k['don_vi'], khoi_phat=kp.get(k['ma']))
            for k in r['extra']['kenh_co_the_gioi'][w]]


def ib_khoa(ds):
    return sorted((i['ma'], i['giai_thich_ma'], i['quy_tac'], i['trang_thai']) for i in ds)


def e9_phu_quyet(nhan):
    """Phép (1): trên K-E1+E2+E5, cửa sổ thật (hai dataset) và mốc giả (RE2-TT)."""
    out = {}
    for ten, luot in (('that', pk.LUOT_THAT), ('moc_gia', [pk.LUOT_MG])):
        dem = collections.Counter()
        root_tut = collections.Counter()
        khong_tai_lap = []
        for L in luot:
            rt = pk.doc_ban_ghi(L, 'K-E1+E2') if ten == 'that' else {}
            for o, r in sorted(pk.doc_ban_ghi(L, 'K-E1+E2+E5').items()):
                kenh, canh = dung_kenh(r), [tuple(c) for c in r['extra']['canh']]
                goc = e5.phan_loai(kenh, canh, bat=True, doc_nhom_vong='co_vong')
                ok = (ib_khoa(goc['inherited_by']) == ib_khoa(r['inherited_by'])
                      and all(goc['F_I'].get(k['ma'], 1) == k['F_I'] for k in r['extra']['kenh_co_the_gioi']['P']))
                if not ok:
                    khong_tai_lap.append(o)
                    continue
                canh_E2 = {tuple(k.don_vi.split('|')[1:3]) for k in kenh if k.don_vi.startswith('canh|')}
                root = nhan[o]['root'] if ten == 'that' else None
                tut = ten == 'that' and rr.rr_ca(r['blocks'] or [], root) < rr.rr_ca(rt[o]['blocks'] or [], root)
                # biến thể: theo CĐ9 (miễn trên cạnh E2 bất thường); bỏ miễn trừ CĐ9 (cận trên số lần phủ quyết,
                # vì tập cạnh E2 dựng lại chỉ là xấp xỉ)
                for bien_the, ce2 in (('theo_CD9', canh_E2), ('bo_mien_tru_CD9', set())):
                    e9 = e5.phan_loai(kenh, canh, bat=True, doc_nhom_vong='co_vong',
                                      e9={'bat': True, 'o_s': O_S, 'tau': TAU, 'canh_E2_bat_thuong': ce2})
                    theo_kenh = {i['ma']: (i['trang_thai'], i['ly_do_E9'], i['thuc_the']) for i in e9['inherited_by']}
                    for tt, ly_do, e in theo_kenh.values():
                        dem[f'{bien_the}|{tt}|{ly_do}'] += 1
                        if tut and e == root:
                            root_tut[f'{bien_the}|{tt}|{ly_do}'] += 1
        out[ten] = {'kenh_bi_xoa_khi_E9_tat': sum(v for k, v in dem.items() if k.startswith('theo_CD9|')),
                    'theo_trang_thai_khi_E9_bat': dict(sorted(dem.items())),
                    'khong_tai_lap': khong_tai_lap}
        if ten == 'that':
            out[ten]['kenh_root_o_ca_tut'] = dict(sorted(root_tut.items()))
    return out


def giai_thich_co_o_moc_gia(nhan):
    """Phép (2), RE2-TT: kênh giải thích có cờ ở cửa sổ giả cùng ca, cùng cấu hình, cùng mã kênh."""
    L = 'b2b-k16-re2-001'
    rt, rb, mg = (pk.doc_ban_ghi(L, 'K-E1+E2'), pk.doc_ban_ghi(L, 'K-E1+E2+E5'),
                  pk.doc_ban_ghi(pk.LUOT_MG, 'K-E1+E2+E5'))
    dem, root_tut = collections.Counter(), collections.Counter()
    for o, r in sorted(rb.items()):
        co_mg = {k['ma'] for k in mg[o]['extra']['kenh_co']} if o in mg else set()
        root = nhan[o]['root']
        tut = rr.rr_ca(r['blocks'] or [], root) < rr.rr_ca(rt[o]['blocks'] or [], root)
        for i in r['inherited_by']:
            if i['trang_thai'] != 'ap_dung':
                continue
            x = 'co_o_moc_gia' if i['giai_thich_ma'] in co_mg else 'khong_co_o_moc_gia'
            dem[x] += 1
            if tut and i['thuc_the'] == root:
                root_tut[x] += 1
    return {'cap_xoa_giai_thich': dict(dem), 'cap_xoa_kenh_root_o_ca_tut': dict(root_tut),
            'ghi_chu': 'đếm theo cặp (kênh bị xóa, kênh giải thích) trong inherited_by; một kênh có thể có nhiều bên giải thích'}


def o_muc_tieu(nhan, E_X):
    kq = pha2_kq()
    out = {}
    for x, cap in (('E3', ('K-R0', 'K-E3')), ('E3', ('K-E1+E2', 'K-E1+E2+E3')),
                   ('E5', ('K-R0', 'K-E5')), ('E5', ('K-E1+E2', 'K-E1+E2+E5'))):
        a, b = (kq['cau_hinh'][c]['ca'] for c in cap)
        theo = collections.defaultdict(Fraction)
        for o in a:
            d = b[o]['theo_the_gioi']['P']['RR'] - a[o]['theo_the_gioi']['P']['RR']
            vung = 'trong_E_X' if nhan[o]['o'] in E_X[x] else 'ngoai_E_X'
            theo[f"{vung}|{nhan[o]['dataset']}"] += d
            theo[vung] += d
        p = json.loads((ROOT / 'results/T-045/khoi-k.json').read_text(encoding='utf-8'))['cap'][
            f"{cap[0][2:]}|{cap[1][2:]}"]['theo_the_gioi']['P']
        out[f'{x}: {cap[0]} → {cap[1]}'] = {'so_o_E_X': len(E_X[x]), 'P': p['P'], 'M': p['M'], 'P_phay': p['P_phay'],
                                           'M_phay': p['M_phay'], 'ket_cuc': p['ket_cuc'],
                                           'tong_dRR': {k: f(v) for k, v in sorted(theo.items())}}
    return out


def dRR_theo_o(nhan):
    """A5: tổng ΔRR theo ô cho các cặp có E1, E2 tại cấu hình thắng; phần đến từ các ô trễ mạng của Nezha-OB (nhóm lỗi
    mà E2 được thiết kế từ đó, G2-H06)."""
    kq = pha2_kq()
    out = {}
    for a, b in (('K-E1', 'K-E1+E2'), ('K-E2', 'K-E1+E2'), ('K-R0', 'K-E1+E2')):
        theo = collections.defaultdict(Fraction)
        for o, c in kq['cau_hinh'][a]['ca'].items():
            theo[nhan[o]['o']] += kq['cau_hinh'][b]['ca'][o]['theo_the_gioi']['P']['RR'] - c['theo_the_gioi']['P']['RR']
        tong = sum(theo.values(), Fraction(0))
        tre = sum((v for k, v in theo.items() if nhan_o_ds(nhan, k) == 'Nezha-OB' and k.endswith('|network_delay')),
                  Fraction(0))
        out[f'{a[2:]} → {b[2:]}'] = {'tong_dRR': f(tong), 'dRR_o_tre_mang_Nezha': f(tre),
                                    'ty_le': f(tre / tong) if tong else None,
                                    'theo_o': {k: f(v) for k, v in sorted(theo.items(), key=lambda x: -x[1]) if v}}
    return out


def nhan_o_ds(nhan, o):
    return next(v['dataset'] for v in nhan.values() if v['o'] == o)


def pha2_kq():
    from m1_danh_gia import pha2
    return pha2.giai_ma_json(json.loads((ROOT / 'results/T-045/khoi-k/kq.json').read_text(encoding='utf-8')))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    nhan, E_X = pk.nap_nhan(False), pk.nap_E_X(False)
    t = e5_theo_ca(nhan, E_X)
    out ={'nguon': 'REVIEW.md T-045 lượt 1, A1 và A7; chỉ mô tả, không dùng để chọn',
           'A1_E5_theo_ca': t, 'A1_M5_doi_chieu': doi_chieu_M5(nhan),
           'A7_E9_phu_quyet': e9_phu_quyet(nhan), 'A7_giai_thich_co_o_moc_gia': giai_thich_co_o_moc_gia(nhan),
           'A7_o_muc_tieu': o_muc_tieu(nhan, E_X), 'A5_dRR_theo_o': dRR_theo_o(nhan)}
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    tom = {k: v for k, v in out['A1_E5_theo_ca'].items() if k not in ('ca', 'doi_chieu_root_mat_kenh')}
    print(json.dumps(tom, ensure_ascii=False))
    print({k: (v['so_ca'], v['so_ca_root_con_tu_sinh']) for k, v in out['A1_E5_theo_ca']['doi_chieu_root_mat_kenh'].items()})
    print(json.dumps({c: {k: (v['so_ca'], round(v['RR_trung_binh'], 3)) for k, v in m.items()}
                      for c, m in out['A1_M5_doi_chieu'].items()}, ensure_ascii=False))
    print(json.dumps(out['A7_E9_phu_quyet'], ensure_ascii=False))
    print(json.dumps(out['A7_giai_thich_co_o_moc_gia'], ensure_ascii=False))
    print(json.dumps(out['A7_o_muc_tieu'], ensure_ascii=False))


if __name__ == '__main__':
    main()
