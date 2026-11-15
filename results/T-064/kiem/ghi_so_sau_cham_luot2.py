# -*- coding: utf-8 -*-
"""Ghi 10 dòng `sau_cham` của lượt chọn 2 vào sổ biến thể (chỉ ghi thêm). Cùng khuôn với dòng sau_cham lượt 1.
Nguồn: results/T-064/cham/chon-dev2-luot2-tap{12,13}.json, …-giu-bo.json, khong-hoi-quy-2.json.
Dùng: py -3 -B results/T-064/kiem/ghi_so_sau_cham_luot2.py"""
import json, sys, datetime
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket/results/T-064')
doc = lambda p: json.loads((R / p).read_text(encoding='utf-8'))
A, B = doc('cham/chon-dev2-luot2-tap12.json')['ban'], doc('cham/chon-dev2-luot2-tap13.json')['ban']
GA, GB = doc('cham/chon-dev2-luot2-tap12-giu-bo.json'), doc('cham/chon-dev2-luot2-tap13-giu-bo.json')
KH = doc('cham/khong-hoi-quy-2.json')['ban']
so = R / 'so-bien-the.jsonl'
da_co = {(r.get('ma'), r.get('loai'), r.get('vai_tro')) for r in map(json.loads, so.read_text(encoding='utf-8').splitlines())}
utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def gb(g, ma):
    return [f"{nhom}:{ten}:{'co' if r['ban_co'] == ma else 'khong'}:{r['ket_luan']}" for nhom, ps in g.items() if isinstance(ps, dict)
            for ten, r in ps.items() if ma in (r['ban_co'], r['ban_khong'])]


def tom(v, flash=False):
    o = {'tong': v['tong'], 'K': v['K'], 'bang_canh': v['bang_canh'], 'so_voi_P7': v.get('so_voi_P7'), 'tut_qua_2_bac': v.get('tut_qua_2_bac')}
    if flash: o['K_flash'] = v['K_flash']
    return o


n = 0
with so.open('a', encoding='utf-8', newline='\n') as f:
    for ma in A:
        if ma == 'P7': continue
        if (ma, 'sau_cham', 'chon_dev2_luot2') in da_co: print('đã có', ma); continue
        k = KH[ma]
        ca = {m: {x: c[x] for x in ('o', 'k', 'hang_ky_vong', 'verdict') if x in c} for m, c in B[ma]['ca'].items()}
        r = {'loai': 'sau_cham', 'utc': utc, 'ma': ma, 'vai_tro': 'chon_dev2_luot2', 'tap_A_12': tom(A[ma], True), 'tap_B_13': tom(B[ma]),
             'khong_hoi_quy_T062': {'tong': k['tong'], 'K': k['K'], 'khong_xau_di': k['khong_xau_di'], 'bang_canh': k['bang_canh']},
             'giu_bo_A': gb(GA, ma), 'giu_bo_B': gb(GB, ma), 'ca_B': ca,
             'nguon': ['cham/chon-dev2-luot2-tap12.json', 'cham/chon-dev2-luot2-tap13.json', 'cham/khong-hoi-quy-2.json', 'kiem/kiem-luot2.json']}
        f.write(json.dumps(r, ensure_ascii=False) + '\n'); n += 1
print('ghi', n, 'dòng sau_cham lượt 2,', utc)
