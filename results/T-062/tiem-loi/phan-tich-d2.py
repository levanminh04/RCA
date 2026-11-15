#!/usr/bin/env python3
"""T-062 D2: bảng xác nhận can thiệp từng ô từ (1) k6 raw của lượt D2, (2) đầu dò trong sổ so.jsonl.
Dùng: py -3 -B results/T-062/tiem-loi/phan-tich-d2.py <tag d2>
Ghi: results/T-062/tiem-loi/d2-xac-nhan.json và .md. Quy tắc xác nhận khai trong o-loi.md, áp như dưới (không chỉnh theo kết quả).
"""
import json, re, statistics, sys, datetime as dt
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
OUT = Path('D:/RCA-flashticket/results/T-062')
tag = sys.argv[1]
plan = json.loads((OUT / 'chay' / f'{tag}-plan.json').read_text(encoding='utf-8'))
raw = OUT / 'tai' / 'out' / tag / 'raw.json'
pts = []
with raw.open(encoding='utf-8') as f:
    for line in f:
        if '"http_req_duration"' not in line or '"Point"' not in line: continue
        d = json.loads(line)
        tg = d['data']['tags']
        if tg.get('route') in (None, 'auth'): continue
        ts = dt.datetime.fromisoformat(d['data']['time'].replace('Z', '+00:00')).timestamp()
        pts.append((ts, tg['route'], int(tg.get('status', 0) or 0), d['data']['value']))
drops = []
with raw.open(encoding='utf-8') as f:
    for line in f:
        if '"dropped_iterations"' in line and '"Point"' in line:
            d = json.loads(line); drops.append((dt.datetime.fromisoformat(d['data']['time'].replace('Z', '+00:00')).timestamp(), d['data']['value']))
probes = [json.loads(l) for l in (OUT / 'tiem-loi' / 'so.jsonl').read_text(encoding='utf-8').splitlines()]
# chỉ lấy đầu dò của đúng lượt D2 này (sổ có cả các lượt D2 hỏng trước đó)
begin = max(i for i, p in enumerate(probes) if p['event'] == 'd2-begin' and p.get('tag') == tag)
probes = [p for p in probes[begin:] if p['event'] == 'd2-probe']

def win(a, b):
    r = {}
    for route in sorted({p[1] for p in pts}):
        xs = [p for p in pts if a <= p[0] < b and p[1] == route]
        if not xs: continue
        lat = sorted(x[3] for x in xs)
        r[route] = {'n': len(xs), 'p50_ms': round(statistics.median(lat), 1), 'p95_ms': round(lat[int(0.95 * (len(lat) - 1))], 1),
                    'err5xx': sum(1 for x in xs if x[2] >= 500), 'non2xx': sum(1 for x in xs if not 200 <= x[2] < 300)}
    return r

def probe(cell, phase):
    for p in probes:
        if p.get('cell') == cell and p.get('phase') == phase: return p['probe']
    return None

base_probe = next(p['probe'] for p in probes if p.get('phase') == 'baseline')
res = []
for c in plan:
    cell, s, e = c['cell'], c['start_epoch'], c['stop_epoch']
    before, during = win(s - 70, s - 5), win(s + 15, e)
    p45, p140, after = probe(cell, 'fault+45'), probe(cell, 'fault+140'), probe(cell, 'after+30')
    d = lambda r: (during.get(r, {}).get('p50_ms', 0) - before.get(r, {}).get('p50_ms', 0))
    ev, od = 'GET /api/v1/events/{id}', 'GET /api/v1/orders/{id}'
    pay = 'GET /api/v1/orders/{id}/payment'
    ok, why = False, []
    if cell == 'EVENT-DB-LAT':
        rt = [p['pg_sslrequest_ms'] for p in (p45, p140)]
        why.append(f"RTT PG qua proxy {[x['proxy_event'] for x in rt]} ms, trực tiếp {[x['direct'] for x in rt]} ms")
        why.append(f"p50 event +{d(ev):.0f} ms; order +{d(od):.0f} ms (đối chứng)")
        # Ngưỡng theo cường độ L đặt trong inj.py (sửa 20:26Z sau khi hạ L 200→30 ms; bản cũ cứng 150 ms):
        # tuyến proxy chậm thêm ≥ 0,75·L, GET event chậm thêm ≥ 100 ms, đối chứng order |Δ|<100 ms, k6 rơi ≤ 5 lượt.
        L = int(re.search(r"'EVENT-DB-LAT': dict\(kind='toxic', proxy='event-jdbc', latency=(\d+)", (OUT / 'tiem-loi/scripts/inj.py').read_text(encoding='utf-8')).group(1))
        nd = int(sum(v for t, v in drops if s + 15 <= t < e))
        ok = all(x['proxy_event'] - x['direct'] >= 0.75 * L for x in rt) and d(ev) >= 100 and abs(d(od)) < 100 and nd <= 5
    elif cell == 'REDIS-BOOK':
        rt = [p['redis_ping_ms'] for p in (p45, p140)]
        why.append(f"Redis PING qua proxy {[x['proxy'] for x in rt]} ms, trực tiếp {[x['direct'] for x in rt]} ms")
        why.append(f"p50 order +{d(od):.0f}, payment +{d(pay):.0f}, event +{d(ev):.0f} ms")
        ok = all(x['proxy'] - x['direct'] >= 150 for x in rt) and max(d(od), d(pay)) >= 150
        if not ok and all(x['proxy'] - x['direct'] >= 150 for x in rt):
            why.append('toxic có trên tuyến nhưng các route trong hỗn hợp tải không đổi → tải không đi qua Redis của Booking')
    elif cell == 'NET-GW-BOOK':
        h = [p['booking_health'] for p in (p45, p140)]
        why.append(f"health Booking qua proxy {[x['proxy']['ms'] for x in h]} ms, trực tiếp {[x['direct']['ms'] for x in h]} ms")
        why.append(f"p50 order +{d(od):.0f}, payment +{d(pay):.0f}, event +{d(ev):.0f} ms (đối chứng)")
        ok = all(x['proxy']['ms'] - x['direct']['ms'] >= 200 for x in h) and d(od) >= 200 and abs(d(ev)) < 100
    elif cell == 'HTTP5-EVENT':
        a0 = (probe(cell, 'fault+45') or {}).get('audit_event-service', {}).get('ops', {})
        a1 = (after or {}).get('audit_event-service', {}).get('ops', {})
        why.append(f"audit Event: {a1}")
        r = during.get(ev, {})
        why.append(f"event 5xx {r.get('err5xx')}/{r.get('n')}; order 5xx {during.get(od, {}).get('err5xx')}/{during.get(od, {}).get('n')} (đối chứng)")
        ok = a1.get('http.error.executed', 0) > 0 and r.get('n') and r['err5xx'] / r['n'] >= 0.9 and during.get(od, {}).get('err5xx', 1) == 0
    elif cell == 'SLOW-BOOK':
        a1 = (after or {}).get('audit_booking-service', {}).get('ops', {})
        why.append(f"audit Booking: {a1}")
        why.append(f"p50 order +{d(od):.0f}, payment +{d(pay):.0f}, event +{d(ev):.0f} ms")
        ok = a1.get('http.delay.started', 0) > 0 and d(od) >= 800 and abs(d(ev)) < 100
    elif cell == 'CPU-BOOK':
        c0 = base_probe['cgroup_booking']; c1 = p140['cgroup_booking']; c2 = after['cgroup_booking']
        why.append(f"burn_procs {p45['burn_procs']},{p140['burn_procs']},{after['burn_procs']}; nr_throttled {c0['nr_throttled']}→{c1['nr_throttled']}→{c2['nr_throttled']}")
        why.append(f"pressure lúc lỗi: {c1['pressure']}")
        why.append(f"p50 order +{d(od):.0f}, event +{d(ev):.0f} ms")
        ok = str(p140['burn_procs']) == '2' and c1['nr_throttled'] - c0['nr_throttled'] > 100 and str(after['burn_procs']) == '0'
    why.append(f"lượt k6 bị rơi trong lỗi: {int(sum(v for t, v in drops if s + 15 <= t < e))}")
    res.append({'cell': cell, 'xac_nhan': bool(ok), 'bang_chung': why, 'k6_truoc': before, 'k6_trong': during})

(OUT / 'tiem-loi' / 'd2-xac-nhan.json').write_text(json.dumps({'tag': tag, 'ket_qua': res}, ensure_ascii=False, indent=1), encoding='utf-8')
md = [f'# D2 — xác nhận can thiệp (lượt `{tag}`)', '',
      'Mỗi ô bật 150 s dưới tải 5 req/s; so cửa sổ 65 s trước bật với [bật+15 s, tắt). Quy tắc: `phan-tich-d2.py`.', '',
      '| Ô | Xác nhận | Bằng chứng |', '|---|---|---|']
for r in res: md.append(f"| {r['cell']} | {'**ĐẠT**' if r['xac_nhan'] else '**KHÔNG**'} | {'; '.join(r['bang_chung'])} |")
md += ['', 'FLASH-HEALTHY không có can thiệp hệ thống; không thuộc D2 (xác nhận bằng số k6 trong chu kỳ E1).']
(OUT / 'tiem-loi' / 'd2-xac-nhan.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
print('\n'.join(md))
