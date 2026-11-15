# -*- coding: utf-8 -*-
"""Ghi 10 dòng `sau_cham` của lượt chọn 3 (sửa R1) vào sổ biến thể (chỉ ghi thêm).
Nguồn: results/T-064/cham/chon-dev2-luot3-tap{12,13}.json, khong-hoi-quy-3.json, kiem/kiem-luot3.json.
Dùng: py -3 -B results/T-064/kiem/ghi_so_sau_cham_luot3.py"""
import json, sys, datetime
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket/results/T-064')
doc = lambda p: json.loads((R / p).read_text(encoding='utf-8'))
A, B = doc('cham/chon-dev2-luot3-tap12.json')['ban'], doc('cham/chon-dev2-luot3-tap13.json')['ban']
KH = doc('cham/khong-hoi-quy-3.json')['ban']; KI = doc('kiem/kiem-luot3.json')
so = R / 'so-bien-the.jsonl'
da_co = {(r.get('ma'), r.get('loai'), r.get('vai_tro')) for r in map(json.loads, so.read_text(encoding='utf-8').splitlines())}
utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
tom = lambda v: {'tong': v['tong'], 'K': v['K'], 'bang_canh': v['bang_canh'], 'so_voi_P7': v.get('so_voi_P7'), 'tut_qua_2_bac': v.get('tut_qua_2_bac')}
n = 0
with so.open('a', encoding='utf-8', newline='\n') as f:
    for ma in A:
        if ma == 'P7' or (ma, 'sau_cham', 'chon_dev2_luot3') in da_co: continue
        k = KH[ma]
        svc = {x: v for x, v in KI['so_voi_cha'].items() if f':{ma} vs ' in x}
        dc = {x: v for x, v in KI['doi_chung'].items() if f':{ma}==' in x}
        r = {'loai': 'sau_cham', 'utc': utc, 'ma': ma, 'vai_tro': 'chon_dev2_luot3', 'tap_A_12': tom(A[ma]), 'tap_B_13': tom(B[ma]),
             'khong_hoi_quy_T062': {'tong': k['tong'], 'K': k['K'], 'khong_xau_di': k['khong_xau_di'], 'bang_canh': k['bang_canh']},
             'so_voi_ban_cha_khong_nhan': svc, 'doi_chung_ma_nguon': dc,
             'ca_B': {m: {x: c[x] for x in ('o', 'k', 'hang_ky_vong', 'verdict') if x in c} for m, c in B[ma]['ca'].items()},
             'nguon': ['cham/chon-dev2-luot3-tap12.json', 'cham/chon-dev2-luot3-tap13.json', 'cham/khong-hoi-quy-3.json', 'kiem/kiem-luot3.json']}
        f.write(json.dumps(r, ensure_ascii=False) + '\n'); n += 1
print('ghi', n, 'dòng sau_cham lượt 3,', utc)
