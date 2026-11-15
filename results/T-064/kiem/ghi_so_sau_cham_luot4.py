# -*- coding: utf-8 -*-
"""Ghi 4 dòng sau_cham lượt 4 (đối chứng bỏ quan hệ) vào sổ + results/T-064/cham/dc-luot4-so-cha.json. Chấm: cham/dc-luot4-tap{12,13}.json, dc-luot4-t062.json.
Dùng: D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B results/T-064/kiem/ghi_so_sau_cham_luot4.py"""
import json, sys, datetime
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket/results/T-064'); L = lambda p: json.loads((R / p).read_text(encoding='utf-8'))
CHA = {'V048-DC-P7-boQH': 'P7', 'V049-DC-V002-boQH': 'V002-H8s1', 'V050-DC-V032-boQH': 'V032-H5b', 'V051-DC-V041-boQH': 'V041-R1-H1c+H5b+H8s1'}
out = {}; tap = {}
for t in (12, 13):
    n4 = L(f'cham/dc-luot4-tap{t}.json')['ban']; pool = {}
    for k in (3, 2, 1):
        f = R / f'cham/chon-dev2-luot{k}-tap{t}.json'
        if f.exists():
            for m, v in json.loads(f.read_text(encoding='utf-8'))['ban'].items(): pool.setdefault(m, v)
    for b, c in CHA.items():
        a, p = n4[b], pool[c]; ca, cp = a['ca'], p['ca']
        tap.setdefault(b, {})[f'tap{t}'] = {'bo_QH': {'tong': a['tong'], 'K': a['K']}, 'cha': {'ma': c, 'tong': p['tong'], 'K': p['K']},
            'o_khac_hang_hoac_verdict': {m: {'cha': [cp[m].get('hang_ky_vong'), cp[m].get('verdict')], 'bo_QH': [ca[m].get('hang_ky_vong'), ca[m].get('verdict')]}
                                         for m in ca if (cp[m].get('hang_ky_vong'), cp[m].get('verdict')) != (ca[m].get('hang_ky_vong'), ca[m].get('verdict'))}}
(R / 'cham/dc-luot4-so-cha.json').write_text(json.dumps(tap, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
t62 = L('cham/dc-luot4-t062.json')
so = R / 'so-bien-the.jsonl'; utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'); n = 0
da = {(r.get('ma'), r.get('loai'), r.get('vai_tro')) for r in map(json.loads, so.read_text(encoding='utf-8').splitlines())}
with so.open('a', encoding='utf-8', newline='\n') as f:
    for b in CHA:
        if (b, 'sau_cham', 'doi_chung_bo_quan_he_luot4') in da: continue
        f.write(json.dumps({'loai': 'sau_cham', 'utc': utc, 'ma': b, 'vai_tro': 'doi_chung_bo_quan_he_luot4', 'cha': CHA[b], 'so_voi_cha': tap[b],
                            'kiem_cai_dat_T062': t62.get('ban', {}).get(b) if isinstance(t62, dict) else None,
                            'nguon': ['cham/dc-luot4-tap12.json', 'cham/dc-luot4-tap13.json', 'cham/dc-luot4-t062.json', 'cham/dc-luot4-so-cha.json']}, ensure_ascii=False, default=str) + '\n'); n += 1
print('ghi', n, utc)
