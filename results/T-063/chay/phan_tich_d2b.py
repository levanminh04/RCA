# -*- coding: utf-8 -*-
"""T-063 — đánh giá D2 bản 2: mỗi ô có can thiệp lên đúng chỗ không (điều kiện ở results/T-063/o-dev-bo-sung.md, T-059).
Dùng: py -3 -B results/T-063/chay/phan_tich_d2b.py <tag d2>  → results/T-063/chay/d2b-<tag>-danh-gia.json + bảng in ra.
Nguồn: sổ results/T-063/tiem-loi/so.jsonl (đầu dò độc lập ở fault+45/+140/after+30) + Prometheus exp-obs (truy vấn ngắn
đúng khoảng nền [start-90, start) và lỗi [start+20, stop)). Chỉ đọc. Đây là xác nhận can thiệp, không phải ca RCA.
"""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); TAG = sys.argv[1]
SSH = 'C:/Program Files/Git/usr/bin/ssh.exe'
OBS = ['-i', 'D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key', '-o', 'BatchMode=yes', '-o',
       'UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts', 'ubuntu@213.35.116.128']

so = [json.loads(l) for l in (R / 'results/T-063/tiem-loi/so.jsonl').read_text(encoding='utf-8').splitlines()]
i0 = max(i for i, d in enumerate(so) if d['event'] == 'd2-begin')
d2 = so[i0:]
import datetime as dt
ts = lambda s: dt.datetime.fromisoformat(s).timestamp()
o = {}
for d in d2:
    c = d.get('cell')
    if d['event'] == 'd2-start': o.setdefault(c, {})['start'] = ts(d['utc'])
    if d['event'] == 'd2-stop': o.setdefault(c, {})['stop'] = ts(d['utc'])
    if d['event'] == 'd2-probe' and c and c != '-': o.setdefault(c, {}).setdefault('probe', {})[d['phase']] = d['probe']
base = next((d['probe'] for d in d2 if d['event'] == 'd2-probe' and d.get('cell') == '-'), {})

Q = {  # (truy vấn, gộp) — chỉ số tóm tắt theo khoảng
    'gw_booking_p50_ms': 'histogram_quantile(0.5, sum by(le)(rate(http_server_request_duration_seconds_bucket{service_name="booking-service"}[1m])))*1000',
    'gw_event_5xx_rps': 'sum(rate(http_server_request_duration_seconds_count{service_name="event-service",http_response_status_code=~"5.."}[1m]))',
    'event_pool_used': 'sum(db_client_connections_usage{service_name="event-service",state="used"})',
    'event_pool_pending': 'sum(db_client_connections_pending_requests{service_name="event-service"})',
    'booking_q_ready': 'sum(rabbitmq_message_current{state="ready",rabbitmq_queue_name=~"booking\\\\..*\\\\.q"})',
    'booking_q_unacked': 'sum(rabbitmq_message_current{state="unacknowledged",rabbitmq_queue_name=~"booking\\\\..*\\\\.q"})',
    'booking_throttle_ratio': 'sum(rate(container_cpu_throttling_data_throttled_periods_total{service_name="booking-service"}[1m]))/sum(rate(container_cpu_throttling_data_periods_total{service_name="booking-service"}[1m]))',
    'payment_live_down': '1 - clamp_max(sum(httpcheck_status{http_url=~".*:8083/.*",http_status_class=~"2xx|3xx|4xx"}), 1)',
    'payment_jvm_samples': 'count_over_time(jvm_cpu_recent_utilization_ratio{service_name="payment-service"}[30s])',
}
script = 'import json,urllib.parse,urllib.request\nW=json.loads(%r)\nQ=json.loads(%r)\nout={}\n' % (json.dumps({c: [v['start'], v['stop']] for c, v in o.items() if 'stop' in v}), json.dumps(Q)) + '''
def q(expr, a, b):
    u="http://localhost:9090/api/v1/query_range?"+urllib.parse.urlencode({"query":expr,"start":a,"end":b,"step":15})
    r=json.load(urllib.request.urlopen(u,timeout=60))["data"]["result"]
    v=[float(x[1]) for s in r for x in s["values"] if x[1] not in ("NaN","+Inf","-Inf")]
    return {"tb":round(sum(v)/len(v),4) if v else None,"max":round(max(v),4) if v else None,"n":len(v)}
for c,(a,b) in W.items():
    out[c]={k:{"nen":q(e,a-90,a),"loi":q(e,a+20,b)} for k,e in Q.items()}
print(json.dumps(out))
'''
r = subprocess.run([SSH] + OBS + ['python3 -'], input=script, capture_output=True, text=True, encoding='utf-8', timeout=600)
prom = json.loads(r.stdout) if r.returncode == 0 else {'loi': r.stderr[-400:]}

def pv(p, *k):
    for x in k:
        p = (p or {}).get(x) if isinstance(p, dict) else None
    return p

kq = {}
for c, v in o.items():
    p45, p140 = v.get('probe', {}).get('fault+45', {}), v.get('probe', {}).get('fault+140', {})
    pr = prom.get(c, {}) if isinstance(prom, dict) else {}
    tom = {'toxics_fault45': {k: t for k, t in (p45.get('toxics') or {}).items() if t},
           'redis_ping_ms': [pv(base, 'redis_ping_ms'), pv(p45, 'redis_ping_ms')],
           'pg_ms': [pv(base, 'pg_sslrequest_ms'), pv(p45, 'pg_sslrequest_ms')],
           'audit_event_ops': [pv(base, 'audit_event-service', 'ops'), pv(p140, 'audit_event-service', 'ops')],
           'burn_procs': p45.get('burn_procs'), 'payment_state': p45.get('payment_state'),
           'nr_throttled_delta_45_140': (pv(p140, 'cgroup_booking', 'nr_throttled') or 0) - (pv(p45, 'cgroup_booking', 'nr_throttled') or 0),
           'prom': pr}
    kq[c] = tom
out = R / f'results/T-063/chay/d2b-{TAG}-danh-gia.json'
out.write_text(json.dumps({'tag': TAG, 'o': o.keys().__len__(), 'ket_qua': kq}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for c, t in kq.items():
    pr = t['prom']
    s = {k: (pr[k]['nen']['tb'], pr[k]['loi']['tb']) for k in pr} if pr else {}
    print('==', c); print('  toxics', t['toxics_fault45'], '| burn', t['burn_procs'], '| payment', t['payment_state'], '| d_throttled', t['nr_throttled_delta_45_140'])
    print('  redis', t['redis_ping_ms'], '| pg', t['pg_ms'])
    print('  prom (nền→lỗi tb):', s)
