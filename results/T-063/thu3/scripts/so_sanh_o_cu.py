# -*- coding: utf-8 -*-
"""T-063 thu3 — so đầu dò và tải của ô cũ (BINH-THUONG, EVENT-DB-LAT) giữa đợt 2 (bản 2) và thu bù 3 (bản 3). Chỉ đọc file đã nhận.
Dùng: py -3 -B results/T-063/thu3/scripts/so_sanh_o_cu.py → results/T-063/thu3/so-sanh-o-cu.json
Nguồn: results/T-063/chay/xac-nhan-ca-2.json (đợt 2), results/T-063/thu3/xac-nhan-ca-3.json (thu3); sổ hai đợt cho đầu dò.
Không đọc kết quả M1. Mã mờ ↔ ô chỉ nằm ở phía chấm (file này)."""
import json, statistics as st
from pathlib import Path
R = Path(__file__).resolve().parents[4]
T = R / 'results/T-063'


def doc_so(p):
    ca = {}
    for l in p.read_text(encoding='utf-8').splitlines():
        d = json.loads(l); oid = d.get('opaque_id')
        if not oid: continue
        c = ca.setdefault(oid, {'probe': {}})
        if d['event'] == 'cycle-begin': c['cell'] = d['cell']
        if d['event'] == 'probe': c['probe'][d['phase']] = d['probe']
    return ca


def tom(xn, so, o):
    rows = []
    for oid, v in xn['ca'].items():
        if v['cell'] != o: continue
        P = so.get(oid, {}).get('probe', {})
        psi = {k: (P.get(k) or {}).get('psi_cpu_may') for k in ('t-240', 't+60', 't+330')}
        rows.append({'ma': oid, 'xac_nhan': v['xac_nhan'], 'k6': v.get('k6'), 'pg_proxy_ms': v.get('pg_proxy_ms'),
                     'pg_direct_ms': [(P.get(k) or {}).get('pg_sslrequest_ms', {}).get('direct') for k in ('t+60', 't+330')],
                     'tcp_15433_ms': [(P.get(k) or {}).get('tcp_connect_ms', {}).get('15433') for k in ('t-240', 't+60', 't+330')],
                     'psi_cpu_may_some_avg60': {k: (x[0].split()[2] if x else None) for k, x in psi.items()}})
    return rows


xn2 = json.loads((T / 'chay/xac-nhan-ca-2.json').read_text(encoding='utf-8'))
xn3 = json.loads((T / 'thu3/xac-nhan-ca-3.json').read_text(encoding='utf-8'))
so2 = doc_so(T / 'thu2/tiem-loi/so-thu2.jsonl'); so3 = doc_so(T / 'thu3/thu/tiem-loi/so-thu3.jsonl')
out = {o: {'ban2': tom(xn2, so2, o), 'ban3': tom(xn3, so3, o)} for o in ('BINH-THUONG', 'EVENT-DB-LAT')}
for o, v in out.items():
    for b in ('ban2', 'ban3'):
        jf = [r['k6']['journey_failed'] / max(1, r['k6']['journey_started']) for r in v[b] if r.get('k6')]
        v[b + '_ty_le_hanh_trinh_hong_tb'] = round(st.mean(jf), 4) if jf else None
(T / 'thu3/so-sanh-o-cu.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(json.dumps(out, ensure_ascii=False)[:3000])
