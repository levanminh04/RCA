# -*- coding: utf-8 -*-
"""T-063 bước 2 — phân loại span gốc và span mồ côi trên gói ca T-062 (OTLP JSON `raw-traces.jsonl`).

Nhóm (B16 §3: job định kỳ là gốc hợp lệ; điểm vào HTTP là gốc hợp lệ):
  diem_vao_http      gốc SERVER có http.request.method / http.route
  job_hop_le         gốc INTERNAL của bộ lập lịch (scope spring-scheduling / quartz / tên `Lớp.phương_thức` không có http)
  consumer_goc       gốc CONSUMER (message không mang ngữ cảnh cha — Saga lẽ ra có cha từ producer)
  client_goc_db      gốc CLIENT có db.system (SQL chạy ngoài span cha: mất ngữ cảnh hoặc job không được bọc)
  client_goc_khac    gốc CLIENT khác (HTTP/redis… không có cha)
  internal_khac      gốc INTERNAL không nhận ra
  mo_coi             có parentSpanId nhưng cha không có trong cả gói (khác: cha ngoài cửa sổ phương pháp)
Đếm theo (service, nhóm, scope, kind, tên) trong cửa sổ [t−300, t+300). Không đọc nhãn.
Dùng: py -3 -B results/T-063/span-goc/phan_loai.py [mã ca ...] → results/T-063/kiem-tich-hop/phan-loai-goc-kt57fcd7.json
"""
import collections, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); CA = R / 'results/T-063/ca'
IDS = sys.argv[1:] or sorted(p.name for p in CA.iterdir() if p.is_dir() and not p.name.startswith('_'))
KIND = {1: 'INTERNAL', 2: 'SERVER', 3: 'CLIENT', 4: 'PRODUCER', 5: 'CONSUMER', 0: 'UNSPECIFIED'}
SCHED = ('spring-scheduling', 'quartz', 'scheduling', 'executor')


def av(v):
    for k in ('stringValue', 'intValue', 'boolValue', 'doubleValue'):
        if k in v: return v[k]
    return None


def attrs(lst): return {a['key']: av(a['value']) for a in (lst or [])}


def nhom(s):
    a, k, sc = s['a'], s['kind'], s['scope']
    if k == 'SERVER' and ('http.request.method' in a or 'http.route' in a or 'http.method' in a): return 'diem_vao_http'
    if k == 'CONSUMER': return 'consumer_goc'
    if k == 'CLIENT': return 'client_goc_db' if ('db.system' in a or 'db.system.name' in a) else 'client_goc_khac'
    if k == 'INTERNAL' and (any(x in sc for x in SCHED) or ('code.function' in a or 'code.function.name' in a)):
        return 'job_hop_le'
    return 'internal_khac'


tong = {}
for ca in IDS:
    t = json.loads((CA / ca / 'cases' / ca / 'request.json').read_text())['t']
    lo, hi = (t - 300) * 10 ** 9, (t + 300) * 10 ** 9
    spans = {}
    with open(CA / ca / 'cases' / ca / 'raw-traces.jsonl', encoding='utf-8') as fh:
        for line in fh:
            d = json.loads(line)
            for rs in d.get('resourceSpans', []):
                svc = attrs(rs['resource'].get('attributes')).get('service.name')
                for ss in rs.get('scopeSpans', []):
                    sc = (ss.get('scope') or {}).get('name', '')
                    for sp in ss.get('spans', []):
                        spans[sp['spanId']] = {'svc': svc, 'scope': sc, 'kind': KIND.get(sp.get('kind', 0), str(sp.get('kind'))),
                                               'name': sp.get('name'), 'parent': sp.get('parentSpanId') or None,
                                               'st': int(sp['startTimeUnixNano']), 'en': int(sp['endTimeUnixNano']),
                                               'a': attrs(sp.get('attributes'))}
    dem = collections.Counter(); vi_du = {}
    n_cua_so = 0
    for sid, s in spans.items():
        if not (s['st'] >= lo and s['en'] < hi): continue
        n_cua_so += 1
        if s['parent'] is None: g = nhom(s)
        elif s['parent'] not in spans: g = 'mo_coi'
        else: continue
        key = (s['svc'], g, s['scope'], s['kind'], s['name'])
        dem[key] += 1
        if key not in vi_du:
            a = s['a']
            vi_du[key] = {k: (str(a[k])[:160]) for k in ('thread.name', 'db.statement', 'db.query.text', 'code.function', 'code.namespace',
                                                         'code.function.name', 'messaging.destination.name', 'http.route', 'server.address') if k in a}
    theo_nhom = collections.Counter()
    for (svc, g, *_), c in dem.items(): theo_nhom[(svc, g)] += c
    tong[ca] = {'t': t, 'so_span_cua_so': n_cua_so,
                'theo_service_nhom': {f'{svc}|{g}': c for (svc, g), c in sorted(theo_nhom.items())},
                'chi_tiet': [{'service': k[0], 'nhom': k[1], 'scope': k[2], 'kind': k[3], 'ten': k[4], 'so': c, 'vi_du_thuoc_tinh': vi_du[k]}
                             for k, c in dem.most_common()]}
    print('==', ca, 'span trong cửa sổ', n_cua_so)
    for (svc, g), c in sorted(theo_nhom.items(), key=lambda x: -x[1])[:14]: print(f'   {svc:18s} {g:16s} {c}')
(R / 'results/T-063/kiem-tich-hop/phan-loai-goc-kt57fcd7.json').write_text(json.dumps(tong, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
