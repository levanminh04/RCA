# -*- coding: utf-8 -*-
"""T-069 bước 7 — CPU từng container trên exp-app trong cửa sổ nền N của ca cũ và ca mới cùng ô (Prometheus exp-obs, chỉ đọc;
chạy qua stdin, in stdout). Cửa sổ N = [t−570, t−30] như điều kiện xác nhận T-063; t lấy từ sổ (đối số).
Dùng: python3 - <ô>:<t_cũ>:<t_mới> [...] < cpu_container.py
Đơn vị: lõi CPU trung bình = rate(container_cpu_usage_nanoseconds_total[1m]) / 1e9, trung bình theo bước 15 s."""
import json, sys, urllib.parse, urllib.request


def q(expr, a, b):
    u = 'http://localhost:9090/api/v1/query_range?' + urllib.parse.urlencode({'query': expr, 'start': a, 'end': b, 'step': 15})
    return json.load(urllib.request.urlopen(u, timeout=120))['data']['result']


E = 'sum by (container_name) (rate(container_cpu_usage_nanoseconds_total[1m])) / 1e9'
for arg in sys.argv[1:]:
    o, tc, tm = arg.split(':'); tc, tm = int(tc), int(tm)
    res = {}
    for phia, t in (('cu', tc), ('moi', tm)):
        for s in q(E, t - 570, t - 30):
            v = [float(x[1]) for x in s['values']]
            res.setdefault(s['metric'].get('container_name', '?'), {})[phia] = sum(v) / len(v) if v else None
    print(f'== {o}  (t cũ {tc}, t mới {tm}) — lõi CPU trung bình ở nền N')
    tong = {'cu': 0, 'moi': 0}
    for c, d in sorted(res.items(), key=lambda kv: -(kv[1].get('moi') or 0)):
        for p in tong: tong[p] += d.get(p) or 0
        print(f'   {c[:48]:48s} {d.get("cu") or 0:6.3f} → {d.get("moi") or 0:6.3f}')
    print(f'   {"TỔNG":48s} {tong["cu"]:6.3f} → {tong["moi"]:6.3f}')
