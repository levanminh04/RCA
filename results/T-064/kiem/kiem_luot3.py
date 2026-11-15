# -*- coding: utf-8 -*-
"""Kiểm không nhãn sau khi nhận lô lượt chọn 3 (sửa R1), trước khi chấm: đủ (bản, ca), status, trùng SHA hai lần chạy,
hai bản đối chứng mã nguồn trùng lượt trước ngoài siêu dữ liệu, và đếm đầu vào thật của bản sửa (số cạnh theo loại).
Dùng: py -3 -B results/T-064/kiem/kiem_luot3.py -> results/T-064/kiem/kiem-luot3.json"""
import json, sys
from collections import Counter
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket/results/T-064')
V = ['V038-R1-H1c', 'V039-R1-H1c+H8s1', 'V040-R1-H1c+H7c+H8s1', 'V041-R1-H1c+H5b+H8s1', 'V042-R1-H1c+H5b+H7c+H8s1', 'V043-R1-H1a',
     'V044-R1-H1b', 'V045-R1-GOP-H1cr', 'V046-KC-V028', 'V047-KC-V002']
KC = {'V046-KC-V028': ('V028-H1c+H8s1', 'ra-khong-hoi-quy-2'), 'V047-KC-V002': ('V002-H8s1', 'ra-khong-hoi-quy-1')}
CHA = {'V038-R1-H1c': ('V014-H1c', 'ra-khong-hoi-quy-1'), 'V039-R1-H1c+H8s1': ('V028-H1c+H8s1', 'ra-khong-hoi-quy-2'),
       'V040-R1-H1c+H7c+H8s1': ('V015-H1c+H7c+H8s1', 'ra-khong-hoi-quy-1'), 'V041-R1-H1c+H5b+H8s1': ('V034-H1c+H5b+H8s1', 'ra-khong-hoi-quy-2'),
       'V042-R1-H1c+H5b+H7c+H8s1': ('V033-H1c+H5b+H7c+H8s1', 'ra-khong-hoi-quy-2'), 'V043-R1-H1a': ('V009-H1a', 'ra-khong-hoi-quy-1'),
       'V044-R1-H1b': ('V010-H1b', 'ra-khong-hoi-quy-1'), 'V045-R1-GOP-H1cr': ('V031-GOP-H1cr', 'ra-khong-hoi-quy-2')}
DEV = (R / 'kiem/ca-dev2-13.txt').read_text().split(); T62 = (R / 'kiem/ca-t062-9.txt').read_text().split()
MOI = ('so_canh_goi_message', 'so_canh_goi_khong_ro', 'gop_loai_cu')


def duong(b, c, tap, tm=None):
    return (R / 'cham/dau-ra-dev2' / b / c) if tap == 'dev2' else (R / 'bien-the' / b / (tm or 'ra-khong-hoi-quy-3') / c)


def doc(p):
    return json.loads((p / 'method-output-1.json').read_text(encoding='utf-8'))


def bo_meta(r):
    r = json.loads(json.dumps(r)); r.pop('variant', None); ft = r['extra']['m1_ft']
    for k in ('ban', 'ma_nguon_sha256', 'cau_hinh_sha256'): ft.pop(k, None)
    for v in (ft.get('chu_thich') or {}).values():
        if isinstance(v, dict):
            for k in MOI: v.pop(k, None)
    return r


def nut(r): return [(e['entity'], e['tie_group']) for e in r.get('entity_ranking', [])]
def canh_co(r): return sorted((c['nguon'], c['dich'], c['loai'], c['hang']) for c in (r['extra']['m1_ft'].get('canh_xep_hang') or []) if c['co'])


out = {'thieu': [], 'khong_OK': [], 'khong_trung_sha': [], 'doi_chung': {}, 'loai_canh': {}, 'so_voi_cha': {}}
n = 0
for tap, ids in (('dev2', DEV), ('t062', T62)):
    for b in V:
        for c in ids:
            p = duong(b, c, tap)
            if not (p / 'summary.json').exists(): out['thieu'].append([tap, b, c]); continue
            s = json.loads((p / 'summary.json').read_text(encoding='utf-8')); n += 1
            if s['status'] != 'OK': out['khong_OK'].append([tap, b, c, s['status']])
            if not s['trung_sha']: out['khong_trung_sha'].append([tap, b, c])
    for kc, (goc, tm) in KC.items():
        khac = []
        for c in ids:
            a, g = duong(kc, c, tap), duong(goc, c, tap, tm)
            if not (a / 'method-output-1.json').exists() or not (g / 'method-output-1.json').exists(): khac.append(c + ':thieu'); continue
            if bo_meta(doc(a)) != bo_meta(doc(g)): khac.append(c)
        out['doi_chung'][f'{tap}:{kc}=={goc}'] = {'so_ca': len(ids), 'khac': khac}
    for b, (cha, tm) in CHA.items():
        dem = Counter(); doi_nut, doi_canh_co, khong_ro = [], [], 0
        for c in ids:
            a, g = duong(b, c, tap), duong(cha, c, tap, tm)
            if not (a / 'method-output-1.json').exists() or not (g / 'method-output-1.json').exists(): continue
            ra, rg = doc(a), doc(g)
            cx = ra['extra']['m1_ft'].get('canh_xep_hang') or []
            dem.update((x['loai'], x['nguon_xac_minh']) for x in cx); khong_ro += sum(x['loai'] == 'khong_ro' for x in cx)
            if nut(ra) != nut(rg): doi_nut.append(c)
            if canh_co(ra) != canh_co(rg): doi_canh_co.append(c)
        out['loai_canh'][f'{tap}:{b}'] = {f'{k[0]}|{k[1]}': v for k, v in sorted(dem.items())}
        out['so_voi_cha'][f'{tap}:{b} vs {cha}'] = {'ca_doi_thu_tu_nut': doi_nut, 'ca_doi_canh_co_co': doi_canh_co, 'so_canh_khong_ro': khong_ro}
out['so_ban_ca_co_summary'] = n; out['ky_vong'] = len(V) * (len(DEV) + len(T62))
(R / 'kiem/kiem-luot3.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('có summary', n, '/', out['ky_vong'], '| thiếu', len(out['thieu']), '| không OK', len(out['khong_OK']), '| không trùng SHA', len(out['khong_trung_sha']))
for k, v in out['doi_chung'].items(): print('  đối chứng', k, 'khác:', v['khac'])
for k, v in out['so_voi_cha'].items(): print('  so với cha', k, v)
