# -*- coding: utf-8 -*-
"""Áp luật giữ (tieu-chi-chon.md §4) và thứ tự chọn (§5) lên kết quả `cham_dev3.py` (lô 5, tập dev bản 3).
Dùng: py -3 -B giu_bo_dev3.py <kết quả cham_dev3 có tập 'chon' và 't062'> <ra.json>
Hàm `xet` chép nguyên logic `cham/giu_bo.py::xet` (§4 luật 1–3, đánh đổi, không tác dụng). Phép 1 = thêm riêng vào P7;
phép 2 = bỏ khỏi bản gộp (cặp ghi trong PHEP2). §5: ứng viên = bản GIỮ so với P7 trên tập chọn và không ca nào tụt quá 2 bậc;
xếp theo (1) AC@1, AC@3, tổng hạng cắt; (2) K; (3) cạnh top 3; (4) số thành phần; (5) — (thời gian chạy không xét ở đây).
Kiểm không hồi quy T-062 (§5): X không xấu đi và K không tăng so với P7."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True; sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); sys.path.insert(0, str(R)); T = R / 'results/T-064'
from src.m1_ft import cham  # noqa: E402


def xet(co, khong, la_canh):
    x = cham.so_sanh(co['tong'], khong['tong']); kxd = cham.khong_xau_di(co['tong'], khong['tong'])
    dK = co['K'] - khong['K']
    bc = co['bang_canh']; nua = bc['so_o'] > 0 and bc['top3'] >= bc['so_o'] / 2
    l1 = x == 'tot_len' and dK <= 0; l2 = dK < 0 and kxd; l3 = la_canh and kxd and dK <= 0 and nua
    tot = x == 'tot_len' or dK < 0; xau = (not kxd) or dK > 0 or x == 'xau_di'
    if l1 or l2 or l3: kl = 'GIU (' + ','.join(n for n, v in (('l1', l1), ('l2', l2), ('l3', l3)) if v) + ')'
    elif tot and xau: kl = 'DANH_DOI'
    elif not tot and not xau and dK == 0 and x == 'bang': kl = 'KHONG_TAC_DUNG'
    else: kl = 'BO'
    return {'X': x, 'khong_xau_di': kxd, 'dK': dK, 'canh_top3': bc['top3'], 'so_o_canh': bc['so_o'], 'ket_luan': kl,
            'tong_co': co['tong'], 'tong_khong': khong['tong'], 'K_co': co['K'], 'K_khong': khong['K']}


PHEP1 = {'H8s0': 'V001-H8s0', 'H8s1': 'V002-H8s1', 'H6a': 'V003-H6a', 'H7': 'V005-H7', 'H7c': 'V016-H7c', 'H2': 'V012-H2',
         'H3': 'V013-H3', 'H4': 'V017-H4', 'H5': 'V018-H5', 'H5b': 'V032-H5b', 'H1c': 'V038-R1-H1c', 'H1a': 'V043-R1-H1a',
         'H1b': 'V044-R1-H1b', 'H8a': 'V060-H8a', 'H8lk': 'V062-H8lk', 'H8lc': 'V064-H8lc'}
# (thành phần, bản có, bản không)
PHEP2 = [('H3', 'V070-V061+H3+H4', 'V069-V061+H4'), ('H4', 'V070-V061+H3+H4', 'V068-V061+H3'),
         ('H3+H4', 'V070-V061+H3+H4', 'V061-V032+H8a'), ('H8a', 'V061-V032+H8a', 'V032-H5b'),
         ('H8a', 'V071-V041+H8a', 'V041-R1-H1c+H5b+H8s1'), ('H3+H4', 'V072-V071+H3+H4', 'V071-V041+H8a'),
         ('H5b', 'V061-V032+H8a', 'V060-H8a'), ('H1c', 'V041-R1-H1c+H5b+H8s1', 'V066-V041-boH1c'),
         ('H8s1', 'V066-V041-boH1c', 'V032-H5b'), ('H8lk', 'V063-V032+H8lk', 'V032-H5b'), ('H8lc', 'V065-V032+H8lc', 'V032-H5b'),
         # thêm sau khi chạy V082 (Minh duyệt 15:46Z, sổ dòng 180): bỏ từng thành phần khỏi V082 = H5b+H8s1+H8a; H1c thêm vào V082 = V071
         ('H8a', 'V082-V066+H8a', 'V066-V041-boH1c'), ('H8s1', 'V082-V066+H8a', 'V061-V032+H8a'), ('H1c', 'V071-V041+H8a', 'V082-V066+H8a')]
# Đối chứng quan hệ (không phải thành phần đề xuất): (tên, bản có quan hệ, bản bỏ)
QUAN_HE = [('E1/E2/E5 trên P7', 'P7', 'V048-DC-P7-boQH'), ('E1/E2/E5 trên V002', 'V002-H8s1', 'V049-DC-V002-boQH'),
           ('E1/E2/E5 trên V032', 'V032-H5b', 'V050-DC-V032-boQH'), ('E1/E2/E5 khi giữ H1c (V041)', 'V041-R1-H1c+H5b+H8s1', 'V051-DC-V041-boQH'),
           ('toàn bộ quan hệ của V041 (H1c + E1/E2/E5)', 'V041-R1-H1c+H5b+H8s1', 'V067-DC-V041-boQH-tron'),
           ('riêng H1c trong V041', 'V041-R1-H1c+H5b+H8s1', 'V066-V041-boH1c'),
           ('E1/E2/E5 trên nền không H1 (V066)', 'V066-V041-boH1c', 'V067-DC-V041-boQH-tron')]


def so_tp(ban):
    if ban == 'P7': return 0
    tp = json.loads((T / 'bien-the' / ban / 'cau-hinh.json').read_text(encoding='utf-8'))['thanh_phan']
    return sum(1 for x in tp if x['ma'] != 'DC-bo-quan-he')


def main():
    d = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))['ban']
    chon = {b: v['chon'] for b, v in d.items()}; t062 = {b: v.get('t062') for b, v in d.items()}
    co = lambda b: b in chon
    out = {'nguon': sys.argv[1], 'phep1': {}, 'phep2': [], 'quan_he': [], 'to_hop_vs_P7': {}, 'xep_5': []}
    for h, b in PHEP1.items():
        if co(b): out['phep1'][h] = dict(xet(chon[b], chon['P7'], h.startswith('H1')), ban=b)
    for h, a, b in PHEP2:
        if co(a) and co(b): out['phep2'].append(dict(xet(chon[a], chon[b], h.startswith('H1')), thanh_phan=h, co=a, khong=b))
    for ten, a, b in QUAN_HE:
        if co(a) and co(b):
            x = xet(chon[a], chon[b], False)
            out['quan_he'].append({'ten': ten, 'co_quan_he': a, 'bo': b, 'X_co_so_bo': x['X'], 'dK_co_tru_bo': x['dK'],
                                   'tong_co': x['tong_co'], 'tong_bo': x['tong_khong'], 'K_co': x['K_co'], 'K_bo': x['K_khong']})
    for b in chon:
        if b == 'P7' or 'DC-' in b: continue
        la_canh = any(h in b for h in ('H1', 'V071', 'V072'))
        x = xet(chon[b], chon['P7'], la_canh)
        tut = cham.tut_qua_2_bac({m: v for m, v in _loi(chon[b]).items()}, _loi(chon['P7']))
        hq = None
        if t062.get(b) and t062.get('P7'):
            hq = {'khong_xau_di': cham.khong_xau_di(t062[b]['tong'], t062['P7']['tong']), 'dK': t062[b]['K'] - t062['P7']['K'],
                  'thieu': t062[b]['thieu'], 'tong': t062[b]['tong'], 'K': t062[b]['K']}
        out['to_hop_vs_P7'][b] = dict(x, tut_qua_2_bac=tut, so_thanh_phan=so_tp(b), khong_hoi_quy_T062=hq,
                                      thieu=chon[b]['thieu'], loi_chay=chon[b]['loi_chay'])
    ung = [(b, v) for b, v in out['to_hop_vs_P7'].items() if v['ket_luan'].startswith('GIU') and not v['tut_qua_2_bac']]
    ung.sort(key=lambda bv: (-round(bv[1]['tong_co']['AC@1'], 9), -round(bv[1]['tong_co']['AC@3'], 9),
                             round(bv[1]['tong_co']['tong_hang_cat'], 9), bv[1]['K_co'], -bv[1]['canh_top3'], bv[1]['so_thanh_phan']))
    out['xep_5'] = [{'ban': b, 'AC@1': v['tong_co']['AC@1'], 'AC@3': v['tong_co']['AC@3'], 'tong_hang_cat': v['tong_co']['tong_hang_cat'],
                     'K': v['K_co'], 'canh_top3': v['canh_top3'], 'so_thanh_phan': v['so_thanh_phan'], 'luat': v['ket_luan'],
                     'khong_hoi_quy_T062': v['khong_hoi_quy_T062']} for b, v in ung]
    Path(sys.argv[2]).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('== phép 1'); [print(f"  {h:6s} {r['ket_luan']:16s} X={r['X']:8s} dK={r['dK']:+d} AC1 {r['tong_co']['AC@1']:.3f}/{r['tong_khong']['AC@1']:.3f} hang {r['tong_co']['tong_hang_cat']:.2f}/{r['tong_khong']['tong_hang_cat']:.2f}") for h, r in out['phep1'].items()]
    print('== phép 2'); [print(f"  {r['thanh_phan']:6s} {r['ket_luan']:16s} X={r['X']:8s} dK={r['dK']:+d} {r['co']} vs {r['khong']}") for r in out['phep2']]
    print('== quan hệ'); [print(f"  {r['ten']:42s} co_so_bo={r['X_co_so_bo']:8s} dK={r['dK_co_tru_bo']:+d} AC1 {r['tong_co']['AC@1']:.2f}/{r['tong_bo']['AC@1']:.2f} AC3 {r['tong_co']['AC@3']:.2f}/{r['tong_bo']['AC@3']:.2f} hang {r['tong_co']['tong_hang_cat']:.2f}/{r['tong_bo']['tong_hang_cat']:.2f}") for r in out['quan_he']]
    print('== §5'); [print(f"  {i+1:2d} {x['ban']:28s} {x['AC@1']:.3f} {x['AC@3']:.3f} {x['tong_hang_cat']:.2f} K{x['K']} c{x['canh_top3']} n{x['so_thanh_phan']} {x['luat']} T062={x['khong_hoi_quy_T062'] and (x['khong_hoi_quy_T062']['khong_xau_di'], x['khong_hoi_quy_T062']['dK'])}") for i, x in enumerate(out['xep_5'])]


def _loi(kq):
    """Rút bảng ca lỗi (p1/hang) từ kết quả cham_dev3 (không còn '_loi'): ca có khóa 'p1'."""
    return {m: {'hang_ky_vong': v.get('hang_ky_vong')} for m, v in kq['ca'].items() if 'p1' in v}


if __name__ == '__main__':
    main()
