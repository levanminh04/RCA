# -*- coding: utf-8 -*-
"""Kiểm không nhãn sau khi nhận lô lượt chọn 2 (trước khi chấm): đủ (bản, ca), status, trùng SHA hai lần chạy,
ba bản đối chứng mã nguồn trùng lượt 1 ngoài siêu dữ liệu, và đếm đầu vào thật của hai tham số mới.
Dùng: py -3 -B results/T-064/kiem/kiem_luot2.py → results/T-064/kiem/kiem-luot2.json"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket/results/T-064')
V = ['V028-H1c+H8s1', 'V029-H1c+H5+H7c+H8s1', 'V030-GOP-H1cp', 'V031-GOP-H1cr', 'V032-H5b', 'V033-H1c+H5b+H7c+H8s1',
     'V034-H1c+H5b+H8s1', 'V035-KC-V015', 'V036-KC-V018', 'V037-KC-V019']
KC = {'V035-KC-V015': 'V015-H1c+H7c+H8s1', 'V036-KC-V018': 'V018-H5', 'V037-KC-V019': 'V019-GOP'}
DEV = (R / 'kiem/ca-dev2-13.txt').read_text().split(); T62 = (R / 'kiem/ca-t062-9.txt').read_text().split()


def duong(b, c, tap):
    return (R / 'cham/dau-ra-dev2' / b / c) if tap == 'dev2' else (R / 'bien-the' / b / ('ra-khong-hoi-quy-2' if b in V else 'ra-khong-hoi-quy-1') / c)


def bo_meta(r):
    r = json.loads(json.dumps(r)); r.pop('variant', None)
    for k in ('ban', 'ma_nguon_sha256'): r['extra']['m1_ft'].pop(k, None)
    return r


out = {'thieu': [], 'khong_OK': [], 'khong_trung_sha': [], 'doi_chung': {}, 'chet_im': {}, 'dinh_vi': {}}
n = 0
for tap, ids in (('dev2', DEV), ('t062', T62)):
    for b in V:
        for c in ids:
            p = duong(b, c, tap)
            if not (p / 'summary.json').exists(): out['thieu'].append([tap, b, c]); continue
            s = json.loads((p / 'summary.json').read_text(encoding='utf-8')); n += 1
            if s['status'] != 'OK': out['khong_OK'].append([tap, b, c, s['status']])
            if not s['trung_sha']: out['khong_trung_sha'].append([tap, b, c])
            ct = s.get('chu_thich') or {}
            ci = (ct.get('H5-liveness') or {}).get('chet_im')
            if ci is not None: out['chet_im'].setdefault(b, {})[c] = sorted(ci['thanh_phan'])
            h1 = ct.get('H1c-canh-chung') or {}
            if 'bo_kenh_dinh_vi' in h1: out['dinh_vi'].setdefault(b, {})[c] = {'dinh_vi': h1['dinh_vi'], 'bi_bo': {e: len(v) for e, v in h1['bang_chung_bi_bo'].items()}}
    for kc, goc in KC.items():
        khac = []
        for c in ids:
            a, g = duong(kc, c, tap) / 'method-output-1.json', duong(goc, c, tap) / 'method-output-1.json'
            if not a.exists() or not g.exists(): khac.append(c + ':thieu'); continue
            if bo_meta(json.loads(a.read_text(encoding='utf-8'))) != bo_meta(json.loads(g.read_text(encoding='utf-8'))): khac.append(c)
        out['doi_chung'][f'{tap}:{kc}=={goc}'] = {'so_ca': len(ids), 'khac': khac}
out['so_ban_ca_co_summary'] = n; out['ky_vong'] = len(V) * (len(DEV) + len(T62))
(R / 'kiem/kiem-luot2.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('có summary', n, '/', out['ky_vong'], '| thiếu', len(out['thieu']), '| không OK', len(out['khong_OK']), '| không trùng SHA', len(out['khong_trung_sha']))
for k, v in out['doi_chung'].items(): print('  đối chứng', k, 'khác:', v['khac'])
for b, v in out['chet_im'].items(): print('  chết im', b, {c: e for c, e in v.items() if e})
for b, v in out['dinh_vi'].items(): print('  định vị', b, 'ca có bằng chứng bị bỏ:', {c: x['bi_bo'] for c, x in v.items() if x['bi_bo']})
