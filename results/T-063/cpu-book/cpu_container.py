# -*- coding: utf-8 -*-
"""T-063 bước 2 — CPU từng container và CPU máy quanh mốc t của các ca T-062 (từ _metric-bo-sung, không truy vấn Prometheus).
Dùng: py -3 -B results/T-063/cpu-book/cpu_container.py → results/T-063/cpu-book/cpu-container.json + bảng in ra.
Khúc: N = [t-300, t), L1 = [t, t+150) (thời gian lỗi của ô T-062), L2 = [t+150, t+300). Đơn vị: lõi CPU (ns/ns)."""
import gzip, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); MB = R / 'results/T-062/ca/_metric-bo-sung/prometheus-tho-1794416400-1794450600.jsonl.gz'
CA = {m: json.loads((R / f'results/T-062/ca/{m}/cases/{m}/request.json').read_text())['t'] for m in
      ['00eaea92', '1ad3afeb', '2e2a5541', '6c1a9fd8', 'a5539fba', 'a89954d1', 'bf17acbf', 'e8661e0a', 'f728fce2']}
WANT = {'container_cpu_usage_nanoseconds_total', 'system_cpu_time_seconds_total', 'container_cpu_utilization_ratio'}
data = {}
with gzip.open(MB, 'rt', encoding='utf-8') as fh:
    next(fh)
    for line in fh:
        r = json.loads(line)
        if r['name'] in WANT: data[r['name']] = r['resp']['data']['result']

def rate(vals, a, b):
    """Tốc độ tăng của counter trong [a, b): (v_cuối − v_đầu)/(t_cuối − t_đầu) trên các mẫu nằm trong khúc; reset → None."""
    pts = [(float(t), float(v)) for t, v in vals if a <= float(t) < b]
    if len(pts) < 2: return None
    if any(y2 < y1 for (_, y1), (_, y2) in zip(pts, pts[1:])): return None
    return (pts[-1][1] - pts[0][1]) / (pts[-1][0] - pts[0][0])

out = {}
for m, t in CA.items():
    khuc = {'N': (t - 300, t), 'L1': (t, t + 150), 'L2': (t + 150, t + 300)}
    row = {}
    for s in data['container_cpu_usage_nanoseconds_total']:
        sv = s['metric'].get('service_name'); cid = s['metric'].get('container_id', '')[:12]
        vals = s['values']
        if not any(t - 300 <= float(x[0]) < t + 300 for x in vals): continue
        row[sv] = {k: (None if (v := rate(vals, a, b)) is None else round(v / 1e9, 4)) for k, (a, b) in khuc.items()}
    # CPU máy: tổng mọi state trừ idle / số lõi
    host = {}
    for k, (a, b) in khuc.items():
        busy = idle = 0.0; ok = True
        for s in data['system_cpu_time_seconds_total']:
            v = rate(s['values'], a, b)
            if v is None: ok = False; break
            (idle := idle + v) if s['metric'].get('state') == 'idle' else None
            if s['metric'].get('state') != 'idle': busy += v
        host[k] = round(busy, 4) if ok else None
    out[m] = {'t': t, 'container_loi_cpu': row, 'may_ban_loi_cpu': host}
(R / 'results/T-063/cpu-book/cpu-container.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for m in ('bf17acbf', 'a5539fba'):
    print('==', m, 't', CA[m], 'máy (lõi bận):', out[m]['may_ban_loi_cpu'])
    for sv, v in sorted(out[m]['container_loi_cpu'].items(), key=lambda x: -(x[1]['L1'] or 0)):
        print(f"  {sv:18s} N={v['N']}  L1={v['L1']}  L2={v['L2']}")
