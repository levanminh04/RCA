# -*- coding: utf-8 -*-
"""T-069 bước 7 — thống kê span theo câu lệnh trong gói ca (chỉ đọc; chạy trên máy qua stdin, in stdout).
Dùng: sudo -n python3 - <goi raw-traces.jsonl> <N_bat_dau_s> <A_bat_dau_s> <A_ket_thuc_s> <service> <ten span>[,<ten span>...] < span_thong_ke.py
Với mỗi span khớp (service, tên): nhóm theo db.query.text/db.statement (cắt 140 ký tự); đếm và trung vị/p90 thời lượng (ms)
trong N = [N_bat_dau, A_bat_dau) và A = [A_bat_dau, A_ket_thuc). Không đọc nhãn."""
import json, sys, collections, statistics
sys.stdout.reconfigure(encoding="utf-8")
f, n0, a0, a1, svc, names = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5], set(sys.argv[6].split(','))
d = collections.defaultdict(lambda: {'N': [], 'A': []})
tong = {'N': collections.Counter(), 'A': collections.Counter()}


def attr(xs, k):
    for a in xs:
        if a['key'] == k:
            v = a['value']; return v.get('stringValue') or v.get('intValue')


for line in open(f, encoding='utf-8'):
    o = json.loads(line)
    for rs in o.get('resourceSpans', []):
        if attr(rs['resource'].get('attributes', []), 'service.name') != svc: continue
        for ss in rs.get('scopeSpans', []):
            for sp in ss.get('spans', []):
                st = int(sp['startTimeUnixNano']) / 1e9
                w = 'N' if n0 <= st < a0 else ('A' if a0 <= st < a1 else None)
                if not w: continue
                tong[w][sp['name']] += 1
                if sp['name'] not in names: continue
                at = sp.get('attributes', [])
                q = (attr(at, 'db.query.text') or attr(at, 'db.statement') or '?')[:140]
                d[(sp['name'], q)][w].append((int(sp['endTimeUnixNano']) - int(sp['startTimeUnixNano'])) / 1e6)


def tk(v):
    if not v: return '   -'
    v = sorted(v); return f'n={len(v):5d} p50={statistics.median(v):7.2f} p90={v[int(0.9 * (len(v) - 1))]:7.2f} max={v[-1]:8.1f}'


for (nm, q), x in sorted(d.items(), key=lambda kv: -(len(kv[1]['N']) + len(kv[1]['A']))):
    print(f'{nm} | {q}\n    N: {tk(x["N"])}\n    A: {tk(x["A"])}')
for nm in sorted(names):
    print(f'TỔNG {nm}: N {tk([v for (n, q), x in d.items() if n == nm for v in x["N"]])} | A {tk([v for (n, q), x in d.items() if n == nm for v in x["A"]])}')
print('Số span của service theo tên (N, A) — 12 tên nhiều nhất:', [(k, tong['N'][k], tong['A'][k]) for k, _ in (tong['N'] + tong['A']).most_common(12)])
