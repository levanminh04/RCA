# -*- coding: utf-8 -*-
"""Phiên C — lần cơ chế các ca đổi (luật 15): với mỗi cặp (đối chiếu A, bản xét B) và mỗi ca đổi đại lượng chấm trong
<cham.json> (đầu ra `cham_phien_c.py`), in thứ hạng nhóm đầu và các kênh có cờ (thực thể, kênh, hướng, s, khởi phát so với
t GỐC) của hai bản. Đối chiếu thêm một ca KHÔNG đổi cùng ô khi có. Chỉ đọc đầu ra M1 đã lưu; nhãn (ô) chỉ để chú thích.
Dùng: py -3 -B co_che_ca_doi.py <cham.json> <ra.md> [<cặp>...]"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket')
C = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
chon = sys.argv[3:] or list(C['cap'])
NS = 10 ** 9


def doc(ten, tap, ma):
    p = R / C['spec']['ban'][ten][tap].format(id=ma)
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None


def t_goc(rec):
    dt = ((rec.get('extra') or {}).get('m1_ft') or {}).get('doi_t')
    if dt:
        return dt['t_goc']
    w = rec.get('window') or {}
    return w['A'][0] / NS if isinstance(w, dict) and w.get('A') else None  # bản d = 0: t = đầu phía A


def tom(rec, t0, n=4):
    if rec is None:
        return ['(thiếu)']
    if rec.get('status') != 'OK':
        return [f"status {rec.get('status')}: {str(rec.get('error'))[:160]}"]
    xs = [f"verdict {rec.get('verdict')}"]
    hang = rec['entity_ranking'][:n]
    xs.append('hạng: ' + '; '.join(f"{r['tie_group'] + 1}:{r['entity']}" for r in hang))
    co = rec['extra'].get('kenh_co', [])
    for e in [r['entity'] for r in hang]:
        kk = sorted([k for k in co if k['thuc_the'] == e], key=lambda k: -k['s'])[:4]
        if kk:
            xs.append(f'  {e}: ' + ', '.join(
                f"{k['ten']}/{k['huong']} s={k['s']:.3g}" + (f" kp={(k['khoi_phat'] / NS - t0):+.0f}s" if k.get('khoi_phat') and t0 else '')
                for k in kk))
    return xs


out = ['# Cơ chế các ca đổi (sinh tự động bởi `co_che_ca_doi.py`)', '',
       'kp = khởi phát của kênh có cờ, tính theo giây so với **t gốc** (không phải t\' của bản dời). Chỉ đọc đầu ra đã lưu.', '']
for cap in chon:
    a, b = [x.strip() for x in cap.split('->')]
    for tap, v in C['cap'][cap].items():
        if not v['doi']:
            continue
        out.append(f'## {cap} — {tap}: so_voi {v["so_voi"]}, dK {v["dK"]}, ca đổi {v["so_ca_doi_dai_luong"]}')
        for ma, d in v['doi'].items():
            if not set(d) - {'_sha_khac', 'o'}:
                continue
            ra, rb = doc(a, tap, ma), doc(b, tap, ma)
            t0 = None
            for r in (rb, ra):
                if r is not None and t0 is None:
                    t0 = t_goc(r)
            out.append(f"### {ma} ({d['o']}) — đổi: " + ', '.join(f'{k} {d[k][0]}→{d[k][1]}' for k in d if k not in ('_sha_khac', 'o') and not k.startswith('nhom')))
            if 'nhom_hang_1' in d:
                out.append(f"- nhóm hạng 1: {d['nhom_hang_1'][0]} → {d['nhom_hang_1'][1]}")
            out.append(f'- {a}:'); out += ['  - ' + x for x in tom(ra, t0)]
            out.append(f'- {b}:'); out += ['  - ' + x for x in tom(rb, t0)]
        out.append('')
Path(sys.argv[2]).write_text('\n'.join(out) + '\n', encoding='utf-8')
print('ghi', sys.argv[2], len(out), 'dòng')
