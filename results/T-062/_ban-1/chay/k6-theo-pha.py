#!/usr/bin/env python3
"""T-062: số k6 theo pha (nền [t-600,t), lỗi [t,t+600), hồi phục [t+600,t+1200)) cho mỗi chu kỳ E1 — xác nhận can thiệp
độc lập với M1 (số phía tải, gồm ~290 ms trễ mạng AWS→Oracle). Đọc sổ để lấy t và ô (đây là lớp chấm, sau khi đã băm kết quả).
Dùng: py -3 -B results/T-062/chay/k6-theo-pha.py > results/T-062/chay/k6-theo-pha.md"""
import json, statistics, sys, datetime as dt
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
O = Path(__file__).resolve().parents[1]
so = [json.loads(l) for l in (O / 'tiem-loi/so.jsonl').read_text(encoding='utf-8').splitlines()]
mo = {e['opaque_id']: e['cell'] for e in so if e['event'] == 'cycle-begin'}
tt = {e['opaque_id']: e['t'] for e in so if e['event'] == 'm1-queued'}
R = {'GET /api/v1/events/{id}': 'event', 'GET /api/v1/orders/{id}': 'order', 'GET /api/v1/orders/{id}/payment': 'payment', 'GET /api/v1/orders/{id}/tickets': 'tickets'}
print('| Ca | Ô | Pha | event p50 / 5xx | order p50 / 5xx | payment p50 / 5xx | tickets 5xx | req | rơi |')
print('|---|---|---|---|---|---|---|---|---|')
for oid, t in tt.items():
    raw = O / 'tai/out' / f'e1-{oid}' / 'raw.json'
    pts, drops = [], []
    for line in raw.open(encoding='utf-8'):
        if '"Point"' not in line: continue
        if '"http_req_duration"' in line:
            d = json.loads(line); tg = d['data']['tags']
            if tg.get('route') in R:
                pts.append((dt.datetime.fromisoformat(d['data']['time'].replace('Z', '+00:00')).timestamp(), R[tg['route']], int(tg.get('status') or 0), d['data']['value']))
        elif '"dropped_iterations"' in line:
            d = json.loads(line); drops.append(dt.datetime.fromisoformat(d['data']['time'].replace('Z', '+00:00')).timestamp())
    for ten, a, b in (('nền', t - 600, t), ('lỗi', t, t + 600), ('hồi phục', t + 600, t + 1200)):
        x = [p for p in pts if a <= p[0] < b]
        def c(r):
            y = [p for p in x if p[1] == r]
            return f"{statistics.median([p[3] for p in y]):.0f} / {sum(1 for p in y if p[2] >= 500)}" if y else '—'
        tk = [p for p in x if p[1] == 'tickets']
        print(f"| `{oid}` | {mo[oid]} | {ten} | {c('event')} | {c('order')} | {c('payment')} | {sum(1 for p in tk if p[2] >= 500)}/{len(tk)} | {len(x)} | {sum(1 for d in drops if a <= d < b)} |")
