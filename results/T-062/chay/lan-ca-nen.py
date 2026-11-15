#!/usr/bin/env python3
"""T-062: lần cơ chế CAUSE_FOUND ở ca không tiêm lỗi — với mỗi thao tác M1 gắn cờ, đếm span và trung vị thời lượng
trong cửa sổ nền [t-300,t) và sự cố [t,t+300) từ raw-traces.jsonl của gói ca (cùng dữ liệu M1 đọc). Chỉ đọc."""
import json, statistics, sys, collections
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
O = Path(__file__).resolve().parents[1]
def at(l): return {a['key']: next(iter(a['value'].values()), None) for a in l or []}
out = {}
for m in sys.argv[1:]:
    k = json.load(open(O / f'ket-qua/{m}.json', encoding='utf-8'))
    t = k['su_co']['moc']['t_ns'] // 10**9
    ops = set()
    for n in k['nut']:
        if n.get('tang_m1') == 1:
            for b in n['bang_chung']:
                p = b.split('|')
                if p[1] == 'op': ops.add((p[0], p[3]))
    st = collections.defaultdict(lambda: {'nen': [], 'su_co': [], 'moc_nen': [], 'moc_su_co': []})
    for line in open(O / f'ca/{m}/cases/{m}/raw-traces.jsonl', encoding='utf-8'):
        d = json.loads(line)
        for rs in d['resourceSpans']:
            svc = at(rs['resource']['attributes']).get('service.name')
            for ss in rs['scopeSpans']:
                for s in ss['spans']:
                    if (svc, s['name']) not in ops: continue
                    a = int(s['startTimeUnixNano']) / 1e9; dur = (int(s['endTimeUnixNano']) - int(s['startTimeUnixNano'])) / 1e6
                    w = 'nen' if t - 300 <= a < t else ('su_co' if t <= a < t + 300 else None)
                    if w: st[(svc, s['name'])][w].append(dur); st[(svc, s['name'])]['moc_' + w].append(round(a - t))
    r = {}
    for key, v in st.items():
        f = lambda x: (len(x), round(statistics.median(x), 2) if x else None, round(max(x), 2) if x else None)
        r[' | '.join(key)] = {'nen(n,p50ms,max)': f(v['nen']), 'su_co(n,p50ms,max)': f(v['su_co']),
                              'moc_su_co_gan_t_nhat_s': sorted(v['moc_su_co'])[:5], 'moc_nen_s': sorted(v['moc_nen'])[-5:]}
    out[m] = r
    print('==', m)
    for kk, vv in r.items(): print('  ', kk, vv)
(O / 'chay/lan-ca-nen.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
