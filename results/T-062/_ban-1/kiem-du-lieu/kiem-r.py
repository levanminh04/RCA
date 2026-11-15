#!/usr/bin/env python3
"""T-062 B1 (chặng 1a): bộ kiểm chất lượng dữ liệu R-01–R-10 (results/T-040/yeu-cau-quan-sat-p9.md) trên một gói ca
đã đóng băng (cùng dữ liệu M1 đọc: raw-traces.jsonl, raw-logs.jsonl, prometheus.json).

Dùng: py -3 -B results/T-062/kiem-du-lieu/kiem-r.py <thư mục gói ca (cases/<mã>)> [--ra <file.json>]
Mỗi R trả: so_do (số đếm), dat ∈ {DAT, THIEU, CHUA_KIEM}, ly_do. Ngưỡng ghi ngay trong mã (khai trước khi chạy).
Không đọc sổ tiêm lỗi; không dùng nhãn. R-07, R-10 kiểm thêm hồ sơ lượt (manifest build, sổ) nếu truyền --ho-so.
"""
import json, re, sys, collections
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
UUID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)
KIND = {1: 'INTERNAL', 2: 'SERVER', 3: 'CLIENT', 4: 'PRODUCER', 5: 'CONSUMER',
        'SPAN_KIND_INTERNAL': 'INTERNAL', 'SPAN_KIND_SERVER': 'SERVER', 'SPAN_KIND_CLIENT': 'CLIENT',
        'SPAN_KIND_PRODUCER': 'PRODUCER', 'SPAN_KIND_CONSUMER': 'CONSUMER'}

def attrs(lst):
    out = {}
    for a in lst or []:
        v = a.get('value', {})
        out[a['key']] = next(iter(v.values()), None) if v else None
    return out

def jsonl(p):
    with open(p, encoding='utf-8') as f:
        for l in f:
            if l.strip(): yield json.loads(l)

def main():
    case = Path(sys.argv[1]); ra = sys.argv[sys.argv.index('--ra') + 1] if '--ra' in sys.argv else None
    spans, res_of = [], {}
    for doc in jsonl(case / 'raw-traces.jsonl'):
        for rs in doc.get('resourceSpans', []):
            r = attrs(rs.get('resource', {}).get('attributes'))
            for ss in rs.get('scopeSpans', []):
                for s in ss.get('spans', []):
                    s['_k'] = KIND.get(s.get('kind'), str(s.get('kind'))); s['_a'] = attrs(s.get('attributes')); s['_r'] = r
                    spans.append(s)
    logs = []
    for doc in jsonl(case / 'raw-logs.jsonl'):
        for rl in doc.get('resourceLogs', []):
            r = attrs(rl.get('resource', {}).get('attributes'))
            for sl in rl.get('scopeLogs', []):
                for lr in sl.get('logRecords', []):
                    body = (lr.get('body') or {}).get('stringValue')
                    parsed = {}
                    if isinstance(body, str) and body.startswith('{'):
                        try: parsed = json.loads(body)
                        except Exception: parsed = {}
                    logs.append({'r': r, 'p': parsed, 'raw': lr})
    by_id = {s['spanId']: s for s in spans}
    svc = lambda s: s['_r'].get('service.name')
    out = {'goi_ca': str(case), 'so_span': len(spans), 'so_log': len(logs), 'R': {}}
    R = out['R']

    # R-01 kiểu span và đích lời gọi
    cl = [s for s in spans if s['_k'] == 'CLIENT']
    http_cl = [s for s in cl if 'http.request.method' in s['_a'] or 'http.method' in s['_a']]
    co_dich = [s for s in cl if s['_a'].get('server.address') or s['_a'].get('peer.service') or s['_a'].get('net.peer.name')]
    cap = collections.Counter()
    for s in spans:
        if s['_k'] == 'SERVER' and s.get('parentSpanId') in by_id:
            p = by_id[s['parentSpanId']]
            if p['_k'] == 'CLIENT' and svc(p) != svc(s): cap[f'{svc(p)}→{svc(s)}'] += 1
    R['R-01'] = {'so_do': {'span_theo_kind': dict(collections.Counter(s['_k'] for s in spans)), 'client': len(cl),
                           'client_co_dich': len(co_dich), 'client_http': len(http_cl), 'cap_client_server_khac_service': dict(cap)},
                 'dat': 'DAT' if cl and len(co_dich) == len(cl) and cap else 'THIEU',
                 'ly_do': 'mọi CLIENT có server.address/peer và có cặp CLIENT→SERVER khác service'}
    # R-02 tên thao tác ổn định
    srv = [s for s in spans if s['_k'] == 'SERVER']
    co_id = [s['name'] for s in spans if UUID.search(s['name'] or '')]
    co_route = [s for s in srv if s['_a'].get('http.route')]
    R['R-02'] = {'so_do': {'server': len(srv), 'server_co_http_route': len(co_route), 'ten_span_chua_uuid': len(co_id),
                           'vi_du_ten_chua_uuid': sorted(set(co_id))[:5], 'so_ten_server_khac_nhau': len({(svc(s), s['name']) for s in srv})},
                 'dat': 'DAT' if not co_id and srv and len(co_route) / len(srv) >= 0.95 else 'THIEU',
                 'ly_do': 'không tên span nào chứa UUID; ≥95% SERVER có http.route. Bảng ánh xạ B13→tên span: CHUA_KIEM (ngoài dữ liệu)'}
    # R-03 cạnh dữ liệu
    db = [s for s in cl if s['_a'].get('db.system') or s['_a'].get('db.system.name')]
    sysn = collections.Counter((svc(s), s['_a'].get('db.system') or s['_a'].get('db.system.name'),
                                s['_a'].get('db.namespace') or s['_a'].get('db.name'),
                                f"{s['_a'].get('server.address')}:{s['_a'].get('server.port')}") for s in db)
    thieu_ns = [k for k in sysn if k[1] != 'redis' and not k[2]]
    R['R-03'] = {'so_do': {'span_db_client': len(db), 'nhom_service_he_db_namespace_dich': {' | '.join(map(str, k)): v for k, v in sysn.most_common(20)}},
                 'dat': 'DAT' if db and not thieu_ns else 'THIEU',
                 'ly_do': 'span CLIENT có db.system, tên DB logic (trừ redis), địa chỉ instance. Bảng DB logic→instance→host theo thời gian: CHUA_KIEM'}
    # R-04 thông điệp
    msg = [s for s in spans if s['_k'] in ('PRODUCER', 'CONSUMER')]
    co_q = [s for s in msg if s['_k'] == 'CONSUMER' and (s['_a'].get('messaging.destination.name') or s['_a'].get('rabbitmq.queue'))]
    co_rk = [s for s in msg if s['_k'] == 'PRODUCER' and (s['_a'].get('messaging.rabbitmq.destination.routing_key') or s['_a'].get('messaging.destination.name'))]
    R['R-04'] = {'so_do': {'producer': sum(1 for s in msg if s['_k'] == 'PRODUCER'), 'consumer': sum(1 for s in msg if s['_k'] == 'CONSUMER'),
                           'consumer_co_queue': len(co_q), 'producer_co_exchange_routing': len(co_rk),
                           'consumer_co_link': sum(1 for s in msg if s['_k'] == 'CONSUMER' and s.get('links'))},
                 'dat': 'CHUA_KIEM' if not msg else ('DAT' if len(co_q) == sum(1 for s in msg if s['_k'] == 'CONSUMER') else 'THIEU'),
                 'ly_do': 'cần lưu lượng có message trong cửa sổ; tải đọc cố định T-062 có thể không sinh message'}
    # R-05 host/instance
    rs = {(svc(s), s['_r'].get('host.id'), s['_r'].get('service.instance.id')) for s in spans}
    lr = {(l['r'].get('service.name'), l['r'].get('host.id'), l['r'].get('service.instance.id')) for l in logs}
    prom = json.loads((case / 'prometheus.json').read_text(encoding='utf-8'))
    prom_s = json.dumps(prom)[:2_000_000]
    R['R-05'] = {'so_do': {'trace_resource_thieu_host': sorted(str(x) for x in rs if not x[1]), 'log_resource_thieu_host': sorted(str(x) for x in lr if not x[1]),
                           'metric_co_nhan_host_id': 'host_id' in prom_s, 'so_instance_trace': len({x[2] for x in rs})},
                 'dat': 'DAT' if all(x[1] for x in rs) and all(x[1] for x in lr) else 'THIEU',
                 'ly_do': 'host.id + service.instance.id trên trace/log/metric. Bảng service→instance→host theo thời gian: lấy từ ha-tang/A2-*'}
    # R-06 log nối span
    app = [l for l in logs if l['p'].get('serviceName')]
    co_tid = [l for l in app if l['p'].get('traceId') and l['p'].get('spanId')]
    noi = [l for l in co_tid if l['p']['spanId'] in by_id]
    theo_svc = collections.defaultdict(lambda: [0, 0, 0])
    for l in app:
        k = l['p']['serviceName']; theo_svc[k][0] += 1
        if l['p'].get('traceId'): theo_svc[k][1] += 1
        if l['p'].get('spanId') in by_id: theo_svc[k][2] += 1
    R['R-06'] = {'so_do': {'log_ung_dung_B16': len(app), 'co_trace_span_id': len(co_tid), 'span_ton_tai_trong_export': len(noi),
                           'theo_service_[tong,co_traceId,noi_duoc]': dict(theo_svc)},
                 'dat': 'DAT' if co_tid and len(noi) / len(co_tid) >= 0.95 else 'THIEU',
                 'ly_do': '≥95% log có spanId nối được vào span có trong export (log runtime không request thì không có traceId — đúng chuẩn)'}
    # R-08 mỗi request gateway có span SERVER gateway cùng trace
    gw = [l for l in app if l['p'].get('eventName', '').startswith('gateway.request.')]
    gw_tid = [l for l in gw if l['p'].get('traceId')]
    srv_gw = {s['traceId'] for s in spans if s['_k'] == 'SERVER' and svc(s) == 'api-gateway'}
    R['R-08'] = {'so_do': {'log_request_gateway': len(gw), 'co_traceId': len(gw_tid), 'co_span_server_gateway': sum(1 for l in gw_tid if l['p']['traceId'] in srv_gw)},
                 'dat': 'DAT' if gw_tid and all(l['p']['traceId'] in srv_gw for l in gw_tid) else ('CHUA_KIEM' if not gw_tid else 'THIEU'),
                 'ly_do': 'mỗi request gateway (log B16) có đúng span SERVER gateway cùng trace. Drop của agent: CHUA_KIEM'}
    # R-09 ranh giới trace mới: span có parent không có trong export
    mo = [s for s in spans if s.get('parentSpanId') and s['parentSpanId'] not in by_id]
    R['R-09'] = {'so_do': {'span_co_parent_vang': len(mo), 'theo_service_kind': dict(collections.Counter(f'{svc(s)}/{s["_k"]}' for s in mo).most_common(15)),
                           'span_goc': sum(1 for s in spans if not s.get('parentSpanId'))},
                 'dat': 'CHUA_KIEM', 'ly_do': 'parent vắng có thể do biên cửa sổ đóng gói (span cha ngoài [t-600,t+600)); cần phân loại (a)(b)(c) theo B16 §3 — báo số, chưa quy cơ chế'}
    # R-07, R-10 từ hồ sơ lượt
    ver = collections.Counter((svc(s), s['_r'].get('service.version')) for s in spans)
    R['R-10'] = {'so_do': {'service_version': {f'{k[0]}': k[1] for k in ver}},
                 'dat': 'DAT' if len({v for (k, v) in ver if k not in ('keycloak',)}) == 1 else 'THIEU',
                 'ly_do': 'mọi service ứng dụng cùng một commit (results/T-062/ha-tang/A2-lan2-build-manifest.json có image id/commit)'}
    R['R-07'] = {'so_do': {}, 'dat': 'CHUA_KIEM', 'ly_do': 'manifest lượt (commit, image, agent, sampling, đồng hồ, lịch tải, mốc tiêm) nằm ở ha-tang/, tai/may-tai.md, tiem-loi/so.jsonl; onset/hồi phục độc lập: đầu dò trong sổ — tổng hợp ở báo cáo B1'}
    s = json.dumps(out, ensure_ascii=False, indent=1)
    if ra: Path(ra).write_text(s + '\n', encoding='utf-8')
    for k, v in R.items(): print(k, v['dat'], '—', json.dumps(v['so_do'], ensure_ascii=False)[:300])

if __name__ == '__main__': main()
