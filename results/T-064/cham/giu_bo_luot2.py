# -*- coding: utf-8 -*-
"""Áp luật giữ thành phần (results/T-064/tieu-chi-chon.md §4) lên kết quả chấm lượt chọn 2.
Dùng: py -3 -B results/T-064/cham/giu_bo_luot2.py <chon-dev2-luot2-tapN.json> → in bảng + ghi <cùng tên>-giu-bo.json
Danh sách phép so khai trong file này TRƯỚC khi có kết quả lượt 2 (ghi 13/11 ~19:45Z, lô còn đang chạy).
Mỗi phép: (bản có thành phần, bản không có, có phải thành phần cạnh). Hàm `xet` chép nguyên từ giu_bo.py."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True; sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); sys.path.insert(0, str(R))
from src.m1_ft import cham
f = Path(sys.argv[1]); d = json.loads(f.read_text(encoding='utf-8'))['ban']
V15, V18, V19 = 'V035-KC-V015', 'V036-KC-V018', 'V037-KC-V019'  # bản đối chứng cùng mã nguồn lượt 2
PHEP = {
    'to_hop_vs_P7': {'H1c+H8s1': ('V028-H1c+H8s1', 'P7', True), 'H1c+H7c+H8s1': (V15, 'P7', True),
                     'H1c+H5+H7c+H8s1': ('V029-H1c+H5+H7c+H8s1', 'P7', True), 'H1c+H5b+H7c+H8s1': ('V033-H1c+H5b+H7c+H8s1', 'P7', True),
                     'H1c+H5b+H8s1': ('V034-H1c+H5b+H8s1', 'P7', True), 'GOP-H1cp': ('V030-GOP-H1cp', 'P7', True),
                     'GOP-H1cr': ('V031-GOP-H1cr', 'P7', True)},
    'them_rieng_vao_P7': {'H5': (V18, 'P7', False), 'H5b': ('V032-H5b', 'P7', False)},
    'bo_khoi_to_hop': {'H7c khỏi H1c+H7c+H8s1': (V15, 'V028-H1c+H8s1', False),
                       'H5 khỏi H1c+H5+H7c+H8s1': ('V029-H1c+H5+H7c+H8s1', V15, False),
                       'H5b khỏi H1c+H5b+H7c+H8s1': ('V033-H1c+H5b+H7c+H8s1', V15, False),
                       'H5b khỏi H1c+H5b+H8s1': ('V034-H1c+H5b+H8s1', 'V028-H1c+H8s1', False),
                       'H7c khỏi H1c+H5b+H7c+H8s1': ('V033-H1c+H5b+H7c+H8s1', 'V034-H1c+H5b+H8s1', False)},
    'doi_tham_so': {'H5b so với H5 (riêng)': ('V032-H5b', V18, False), 'H5b so với H5 (trong tổ hợp)': ('V033-H1c+H5b+H7c+H8s1', 'V029-H1c+H5+H7c+H8s1', False),
                    'định vị bỏ pool so với gộp': ('V030-GOP-H1cp', V19, True), 'định vị bỏ pool+JVM so với gộp': ('V031-GOP-H1cr', V19, True)},
}


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


def tut(co, khong):
    """Ca có hạng kỳ vọng tụt quá 2 bậc (§3), tính lại từ bảng từng ca."""
    inf = float('inf'); o = []
    for m, v in d[co]['ca'].items():
        if 'hang_ky_vong' not in v and 'p1' not in v: continue
        a = v.get('hang_ky_vong'); b = d[khong]['ca'][m].get('hang_ky_vong')
        a = inf if a is None else a; b = inf if b is None else b
        if a != b and a - b > 2 + 1e-9: o.append(m)
    return o


out = {'nguon': str(f)}
for nhom, ps in PHEP.items():
    out[nhom] = {}
    print('==', nhom)
    for ten, (co, khong, la_canh) in ps.items():
        r = xet(d[co], d[khong], la_canh); r['ban_co'], r['ban_khong'], r['tut_qua_2_bac'] = co, khong, tut(co, khong)
        out[nhom][ten] = r
        print(f"  {ten:34s} {r['ket_luan']:16s} X={r['X']:8s} kxd={r['khong_xau_di']!s:5s} dK={r['dK']:+d} canh={r['canh_top3']}/{r['so_o_canh']} "
              f"AC1 {r['tong_co']['AC@1']:.3f}/{r['tong_khong']['AC@1']:.3f} AC3 {r['tong_co']['AC@3']:.3f}/{r['tong_khong']['AC@3']:.3f} "
              f"hang {r['tong_co']['tong_hang_cat']:.1f}/{r['tong_khong']['tong_hang_cat']:.1f} tut2={r['tut_qua_2_bac']}")
Path(str(f).replace('.json', '-giu-bo.json')).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
