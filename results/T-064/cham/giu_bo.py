# -*- coding: utf-8 -*-
"""Áp luật giữ thành phần (results/T-064/tieu-chi-chon.md §4) lên kết quả chấm lượt chọn.
Dùng: py -3 -B results/T-064/cham/giu_bo.py <chon-...-tapN.json> → in bảng + ghi <cùng tên>-giu-bo.json
Phép 1: bản thêm riêng so với P7. Phép 2: bản gộp V019 so với bản bỏ thành phần (thành phần = V019 − V0xx)."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True; sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); sys.path.insert(0, str(R))
from src.m1_ft import cham
f = Path(sys.argv[1]); d = json.loads(f.read_text(encoding='utf-8'))['ban']
PHEP1 = {'H8s1': 'V002-H8s1', 'H6a': 'V003-H6a', 'H7': 'V005-H7', 'H7c': 'V016-H7c', 'H1a': 'V009-H1a', 'H1b': 'V010-H1b',
         'H1c': 'V014-H1c', 'H2': 'V012-H2', 'H3': 'V013-H3', 'H4': 'V017-H4', 'H5': 'V018-H5'}
PHEP2 = {'H6a': 'V020-GOP-H6a', 'H2': 'V021-GOP-H2', 'H3': 'V022-GOP-H3', 'H4': 'V023-GOP-H4', 'H5': 'V024-GOP-H5',
         'H1c': 'V025-GOP-H1c', 'H7c': 'V026-GOP-H7c', 'H8s1': 'V027-GOP-H8s1'}
TO_HOP = {'H6a+H8s1': 'V004-H6a+H8s1', 'H7+H8s1': 'V006-H7+H8s1', 'H6a+H7+H8s1': 'V007-H6a+H7+H8s1', 'H7c+H8s1': 'V008-H7c+H8s1',
          'H1b+H7c+H8s1': 'V011-H1b+H7c+H8s1', 'H1c+H7c+H8s1': 'V015-H1c+H7c+H8s1', 'GOP': 'V019-GOP'}


def xet(co, khong, la_canh):
    """co = bản có thành phần, khong = bản không có. Trả kết luận theo §4."""
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


out = {'nguon': str(f), 'phep1_them_vao_P7': {}, 'phep2_bo_khoi_gop': {}, 'to_hop_vs_P7': {}}
for h, v in PHEP1.items(): out['phep1_them_vao_P7'][h] = xet(d[v], d['P7'], h.startswith('H1'))
for h, v in PHEP2.items(): out['phep2_bo_khoi_gop'][h] = xet(d['V019-GOP'], d[v], h.startswith('H1'))
for h, v in TO_HOP.items(): out['to_hop_vs_P7'][h] = xet(d[v], d['P7'], 'H1' in h or h == 'GOP')
Path(str(f).replace('.json', '-giu-bo.json')).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for k, t in out.items():
    if not isinstance(t, dict): continue
    print('==', k)
    for h, r in t.items():
        print(f"  {h:14s} {r['ket_luan']:16s} X={r['X']:8s} kxd={r['khong_xau_di']!s:5s} dK={r['dK']:+d} canh={r['canh_top3']}/{r['so_o_canh']} "
              f"AC1 {r['tong_co']['AC@1']:.3f}/{r['tong_khong']['AC@1']:.3f} hang {r['tong_co']['tong_hang_cat']:.1f}/{r['tong_khong']['tong_hang_cat']:.1f}")
