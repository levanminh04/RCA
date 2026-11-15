# -*- coding: utf-8 -*-
"""T-063 bước 2 — ca nền: thời gian độc quyền E1 (U) của các thao tác M1 gắn cờ, theo từng khúc 10 s, bằng chính code M1
(`span.chuan_bi`, `span.mau_thao_tac`, cùng cách cắt miền của `chuoi._chay`), trên `method-input.json` đã lưu.
Phân xử: (H1) đầu dò bộ chạy lúc t+63 → vượt ngưỡng dồn quanh khúc [60, 70) s; (H3) ngẫu nhiên → rải đều.
Ngưỡng h lấy từ bản ghi P7 (`extra.don_vi_phan_vi[ma].h`) — cùng ngưỡng M1 đã dùng. Không đọc nhãn.
Dùng (môi trường ghim): .../py312-pin/Scripts/python.exe -B results/T-063/ca-nen/doc_quyen_10s.py"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); sys.path.insert(0, str(R / 'src'))
from m1 import span, chuoi
NS = 10 ** 9
out = {}
for ca in ['a5539fba', '6c1a9fd8', 'e8661e0a', '00eaea92']:
    o = R / f'results/T-062/ca/{ca}/outputs/{ca}'
    spans, metrics, logs, inventory, aliases, t, params = json.loads((o / 'method-input.json').read_text(encoding='utf-8'))
    rec = json.loads((o / 'method-output-1.json').read_text(encoding='utf-8'))
    he = chuoi._he_so_ns(params['don_vi_thoi_gian']['spans.start_us'])
    t_ns = int(round(t * NS)); lo, hi = t_ns - 300 * NS, t_ns + 300 * NS
    rows = [dict(r, owner=chuoi._alias(aliases, r['owner'])) for r in spans
            if r['start_us'] * he >= lo and (r['start_us'] + r['duration_us']) * he < hi]
    prep = span.chuan_bi(rows, t=t_ns / he, tau=10 ** 6 / he, tinh_CP=False)
    mtt = span.mau_thao_tac(prep, 'U')
    pv = {u['ma']: u for u in rec['extra']['don_vi_phan_vi']}
    co = [k for k in rec['extra']['kenh_co'] if k['don_vi'].startswith('op|')]
    ca_out = {}
    for k in co:
        _, chu, op = k['don_vi'].split('|', 2); h = pv[k['don_vi']]['h']; m = mtt[(chu, op)]
        bins = {}
        for phia in ('N', 'A'):
            for v, end in zip(m[phia], m['moc_' + phia]):
                b = int((end * he - t_ns) // (10 * NS)) * 10
                c = bins.setdefault(b, [0, 0]); c[0] += 1; c[1] += int(v > h)
        tong_A = sum(c[1] for b, c in bins.items() if b >= 0); n_A = sum(c[0] for b, c in bins.items() if b >= 0)
        dinh = sorted(((c[1], b) for b, c in bins.items() if b >= 0), reverse=True)[:3]
        quanh_63 = sum(bins.get(b, [0, 0])[1] for b in (50, 60, 70))
        ca_out[k['don_vi']] = {'h_us': h, 'n_A': n_A, 'vuot_A': tong_A, 'vuot_khuc_50_80s': quanh_63,
                               'ba_khuc_vuot_nhieu_nhat_A': [{'khuc_s': b, 'vuot': v} for v, b in dinh],
                               'theo_khuc': {str(b): c for b, c in sorted(bins.items())}}
        print(f"{ca} {k['don_vi'][:60]:60s} n_A={n_A:4d} vượt_A={tong_A:3d} trong[50,80)={quanh_63:3d} đỉnh={[(b, v) for v, b in dinh]}")
    out[ca] = ca_out
(R / 'results/T-063/ca-nen/doc-quyen-10s.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
