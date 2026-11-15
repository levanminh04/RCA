# -*- coding: utf-8 -*-
"""Phiên C — ghi sổ `sau_cham` V060–V065 (H8), chỉ thêm. Giữ/bỏ theo tieu-chi-chon.md §4, cùng logic `cham/giu_bo.py::xet`
(phép 1: so với P7; phép 2: so với V032-H5b). Nguồn: phien-c/cham/h8.json, kiem-lo-h8.json."""
import datetime, json, pathlib, sys
sys.path.insert(0, 'D:/RCA-flashticket')
from src.m1_ft import cham
R = pathlib.Path('results/T-064')
so = (R / 'so-bien-the.jsonl').read_text(encoding='utf-8')
if '"vai_tro_sau": "h8_phien_c_sau_cham"' in so: raise SystemExit('đã ghi')
C = json.loads((R / 'phien-c/cham/h8.json').read_text(encoding='utf-8'))
K = json.loads((R / 'phien-c/cham/kiem-lo-h8.json').read_text(encoding='utf-8'))


def xet(co, khong):  # như giu_bo.py::xet (la_canh = False: H8 không sinh đầu ra cạnh)
    x = cham.so_sanh(co['tong'], khong['tong']); kxd = cham.khong_xau_di(co['tong'], khong['tong']); dK = co['K'] - khong['K']
    l1 = x == 'tot_len' and dK <= 0; l2 = dK < 0 and kxd
    tot = x == 'tot_len' or dK < 0; xau = (not kxd) or dK > 0 or x == 'xau_di'
    if l1 or l2: kl = 'GIU (' + ','.join(n for n, v in (('l1', l1), ('l2', l2)) if v) + ')'
    elif tot and xau: kl = 'DANH_DOI'
    elif not tot and not xau and dK == 0 and x == 'bang': kl = 'KHONG_TAC_DUNG'
    else: kl = 'BO'
    return {'X': x, 'khong_xau_di': kxd, 'dK': dK, 'ket_luan': kl}


GHI = {'V060-H8a': 'không có tình huống trên 22 ca (0 metric logic > 1 định danh); đầu ra trùng bản cha ngoài extra.m1_ft 22/22 — chỉ là kiểm cài đặt, không phải bằng chứng "không tác dụng"; thuong01: P7 (V058 dựng lại) ERROR adapter, V060 chạy được',
       'V061-V032+H8a': 'như V060: trùng V032 ngoài extra.m1_ft 22/22',
       'V062-H8lk': 'đầu vào đổi đúng 10 ca dự báo (4.490 dòng UNKNOWN); không đại lượng chấm nào đổi',
       'V063-V032+H8lk': 'như V062',
       'V064-H8lc': 'PAUSE-PAYMENT: payment từ ngoài thứ hạng lên hạng 4 (log-kq-ok xuống của payment có cờ); ô này là ca người làm đã thấy khi đếm log (khai trong sổ trước chấm); K không đổi',
       'V065-V032+H8lc': 'V032 đã đưa payment hạng 1 ở PAUSE-PAYMENT bằng H5b; không đại lượng chấm nào đổi'}
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'); dong = []
for ma in [b for b in C['ban'] if b.startswith('V06')]:
    cha = 'P7' if '+' not in ma else 'V032'; cap = C['cap'][f'{cha} -> {ma}']
    x = {'loai': 'sau_cham', 'utc': now, 'ma': ma, 'vai_tro_sau': 'h8_phien_c_sau_cham', 'phep': 1 if cha == 'P7' else 2,
         'ban_cha': cha, 'phien': 'C', 'cho_WHY': True}
    for tap, ten in (('dev2', 'tap_B_13'), ('t062', 'khong_hoi_quy_T062')):
        b = C['ban'][ma][tap]; c = cap[tap]
        x[ten] = {'tong': b['tong'], 'K': b['K'], 'so_voi_ban_cha': c['so_voi'], 'dK': c['dK'], 'tut_qua_2_bac': c['tut_qua_2_bac'],
                  'ca_doi': {m: d for m, d in c['doi'].items() if set(d) - {'_sha_khac', 'o'}}}
    x['giu_bo_tap_B_13'] = xet(C['ban'][ma]['dev2'], C['ban'][cha]['dev2'])
    x['khong_hoi_quy_T062_so_P7'] = {'khong_xau_di': cham.khong_xau_di(C['ban'][ma]['t062']['tong'], C['ban']['P7']['t062']['tong']),
                                     'K_khong_tang': C['ban'][ma]['t062']['K'] <= C['ban']['P7']['t062']['K']}
    x['kiem_lo'] = K['ban'][ma]; x['ghi_chu'] = GHI[ma]
    x['nguon'] = ['phien-c/cham/h8.json', 'phien-c/cham/kiem-lo-h8.json']
    dong.append(x); print(ma, x['giu_bo_tap_B_13'], x['khong_hoi_quy_T062_so_P7'])
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8', newline='\n') as f:
    for x in dong: f.write(json.dumps(x, ensure_ascii=False) + '\n')
print('ghi', len(dong), now)
