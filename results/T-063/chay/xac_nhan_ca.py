# -*- coding: utf-8 -*-
"""T-063 — hậu kiểm can thiệp từng ca theo results/T-063/chay/dieu-kien-xac-nhan.md (khai trước 13/11 ~07:30Z).
Dùng: py -3 -B results/T-063/chay/xac_nhan_ca.py <thư mục đợt thu> <file ra.json>
  <thư mục> chứa: tiem-loi/so-thu2.jsonl, tai-out-<tag>/ (k6), audit/event-executions.jsonl (bản đầy đủ chép từ exp-app).
Prometheus truy vấn trên exp-obs qua SSH (chỉ đọc). Không đọc kết quả M1. Không đưa nhãn vào phương pháp (chỉ phía chấm).
"""
import datetime as dt, json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
G = Path(sys.argv[1]); RA = Path(sys.argv[2])
SUA_SAU_1 = '--sua-sau-1' in sys.argv  # dieu-kien-xac-nhan.md "Sửa sau 1": pause = cờ Paused (từ cuối) true, không đòi Status 'running'
SSH = 'ssh'
OBS = ['-i', 'D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key', '-o', 'BatchMode=yes', '-o',
       'UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts', 'ubuntu@213.35.116.128']
EVENT_ID = '3e7c1df9-ada4-4081-94a1-548b80a5da86'
TOXIC = {'EVENT-DB-LAT': 'event-jdbc', 'REDIS-BOOK': 'booking-redis', 'NET-GW-BOOK': 'gateway-booking-http'}
ts = lambda s: dt.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()

so = [json.loads(l) for l in (G / 'tiem-loi/so-thu2.jsonl').read_text(encoding='utf-8').splitlines()]
ca = {}
for d in so:
    oid = d.get('opaque_id')
    if not oid: continue
    c = ca.setdefault(oid, {'su_kien': [], 'probe': {}})
    c['su_kien'].append(d['event'])
    if d['event'] == 'cycle-begin': c['cell'] = d['cell']; c['tag'] = d['load_tag']
    if d['event'] == 'load-start': c['S'] = d['epoch']; c['t'] = int(d['epoch'] + 600)
    if d['event'] == 'probe': c['probe'][d['phase']] = d['probe']

audit_f = G / 'audit/event-executions.jsonl'
audit = []
if audit_f.exists():
    for l in audit_f.read_text(encoding='utf-8').splitlines():
        try: o = json.loads(l)
        except Exception: continue
        if o.get('operation') == 'http.error.executed' and o.get('targetId') == EVENT_ID: audit.append(ts(o['timestamp']))


def prom(expr, a, b):
    sc = ('import json,urllib.parse,urllib.request\nu="http://localhost:9090/api/v1/query_range?"+urllib.parse.urlencode('
          '{"query":%r,"start":%d,"end":%d,"step":15})\nr=json.load(urllib.request.urlopen(u,timeout=60))["data"]["result"]\n'
          'print(json.dumps([float(x[1]) for s in r for x in s["values"] if x[1] not in ("NaN","+Inf","-Inf")]))\n') % (expr, a, b)
    r = subprocess.run([SSH] + OBS + ['python3 -'], input=sc, capture_output=True, text=True, encoding='utf-8', timeout=180)
    if r.returncode != 0: raise RuntimeError('prom: ' + r.stderr[-300:])
    return json.loads(r.stdout)


def tb(v): return round(sum(v) / len(v), 3) if v else None


def toxic_co(p, proxy): return bool((p.get('toxics') or {}).get(proxy))


def khong_toxic(p): return 'toxics' in p and not any((p.get('toxics') or {}).values())


def k6(tag):
    d = G / 'tai-out' / tag  # bố cục thu2 (nhan_thu2.sh); lượt thử dùng tai-out-<tag>
    if not (d / 'state.json').exists(): d = G / f'tai-out-{tag}'
    if not (d / 'state.json').exists(): return None
    st = json.loads((d / 'state.json').read_text(encoding='utf-8'))
    m = json.loads((d / 'summary.json').read_text(encoding='utf-8'))['metrics']
    cnt = lambda k: (m.get(k) or {}).get('count', 0)
    r = {'ExitCode': st.get('ExitCode'), 'journey_started': cnt('journey_started'), 'journey_failed': cnt('journey_failed'),
         'dropped_iterations': cnt('dropped_iterations'), 'token_refresh_failure': cnt('token_refresh_failure')}
    return r, d


kq = {}
for oid, c in ca.items():
    cell, t = c.get('cell'), c.get('t'); P = c['probe']; dk = {}; thieu = []
    if t is None: kq[oid] = {'cell': cell, 'xac_nhan': False, 'khong_du_du_lieu': True, 'ly_do': 'không có load-start'}; continue
    ev = c['su_kien']
    dk['C0_chu_ky'] = ('cycle-end' in ev and 'cycle-error' not in ev and 'dirty' not in ev and
                       (cell in ('BINH-THUONG', 'FLASH-HEALTHY') or ('fault-start' in ev and 'fault-stop' in ev)))
    kk = k6(c['tag'])
    if kk is None: thieu.append('k6'); dk['C1_k6'] = None
    else:
        k6r, kd = kk; dk['C1_k6'] = k6r['ExitCode'] == 0; c['k6'] = k6r
        if cell in ('FLASH-HEALTHY', 'HTTP5-EVENT-FLASH'):
            tr, sau = 0, 0
            for l in (kd / 'raw.json').read_text(encoding='utf-8').splitlines():
                if '"journey_started"' not in l or '"Point"' not in l: continue
                x = ts(json.loads(l)['data']['time'])
                if t - 590 <= x < t - 10: tr += 1
                elif t + 10 <= x < t + 590: sau += 1
            c['ty_le_tai_sau_truoc'] = round(sau / tr, 3) if tr else None
    p60, p330, ph = P.get('t+60'), P.get('t+330'), P.get('hoi+60')
    for ten, p in (('t+60', p60), ('t+330', p330), ('hoi+60', ph)):
        if not p: thieu.append('probe ' + ten)
    p60, p330, ph = p60 or {}, p330 or {}, ph or {}
    N, L, Sau = (t - 570, t - 30), (t + 30, t + 570), (t + 610, t + 1170)
    try:
        if cell in TOXIC:
            px = TOXIC[cell]
            dk['toxic_t60_t330'] = toxic_co(p60, px) and toxic_co(p330, px)
            dk['het_toxic_hoi60'] = khong_toxic(ph)
            if cell == 'EVENT-DB-LAT':
                v = [(p.get('pg_sslrequest_ms') or {}).get('proxy_event') for p in (p60, p330)]
                dk['pg_proxy_ge_20ms'] = all(x is not None and x >= 20 for x in v); c['pg_proxy_ms'] = v
            if cell == 'REDIS-BOOK':
                v = [(p.get('redis_ping_ms') or {}).get('proxy') for p in (p60, p330)]
                dk['redis_proxy_ge_150ms'] = all(x is not None and x >= 150 for x in v); c['redis_proxy_ms'] = v
            if cell == 'NET-GW-BOOK':
                e = ('histogram_quantile(0.5, sum by(le)(rate(http_client_request_duration_seconds_bucket{service_name="api-gateway",'
                     'server_address="127.0.0.1",server_port="18082"}[1m])))*1000')
                n, l = tb(prom(e, *N)), tb(prom(e, *L)); c['gw_18082_p50_ms'] = [n, l]
                if n is None or l is None: thieu.append('prom gw p50')
                dk['gw_p50_tang_ge_200ms'] = (n is not None and l is not None and l - n >= 200)
        elif cell in ('HTTP5-EVENT', 'HTTP5-EVENT-FLASH'):
            if not audit: thieu.append('audit')
            trong = [x for x in audit if t <= x <= t + 605]
            khe = {int((x - t) // 30) for x in trong if x < t + 600}
            dk['audit_co_trong_loi'] = len(trong) > 0
            dk['audit_phu_ge_90pct_khe30s'] = len(khe) >= 0.9 * 20
            dk['audit_khong_truoc'] = not any(t - 600 <= x < t for x in audit)
            dk['audit_khong_sau'] = not any(t + 605 < x <= t + 1200 for x in audit)
            c['audit'] = {'n_trong': len(trong), 'khe_30s': len(khe)}
        elif cell in ('CPU-BOOK-1', 'CPU-BOOK-2'):
            w = '1' if cell == 'CPU-BOOK-1' else '2'
            dk['burn_dung_so'] = str(p60.get('burn_procs')) == w and str(p330.get('burn_procs')) == w
            a = (p60.get('cgroup_booking') or {}).get('nr_throttled'); b = (p330.get('cgroup_booking') or {}).get('nr_throttled')
            dk['nr_throttled_tang'] = a is not None and b is not None and b > a; c['nr_throttled'] = [a, b]
            dk['het_burn_hoi60'] = str(ph.get('burn_procs')) == '0'
        elif cell == 'PAUSE-PAYMENT':
            if SUA_SAU_1:
                dk['paused_t60_t330'] = all((p.get('payment_state') or '').split()[-1:] == ['true'] for p in (p60, p330))
            else:
                dk['paused_t60_t330'] = p60.get('payment_state') == 'running true' and p330.get('payment_state') == 'running true'
            dk['unpaused_hoi60'] = ph.get('payment_state') == 'running false'
            e = 'max(httpcheck_error{http_url=~".*:8083.*"})'
            n, l = prom(e, *N), prom(e, *L); c['httpcheck_error_8083_max'] = [max(n) if n else None, max(l) if l else None]
            dk['httpcheck_loi_ge1'] = bool(l) and max(l) >= 1
            dk['httpcheck_nen_0'] = (not n) or max(n) == 0
        elif cell in ('BINH-THUONG', 'FLASH-HEALTHY'):
            ps = [p for p in P.values()]
            dk['khong_can_thiep_dau_do'] = all(khong_toxic(p) and str(p.get('burn_procs')) == '0' and p.get('payment_state') == 'running false' for p in ps)
            if not audit: thieu.append('audit')
            dk['audit_khong_hook'] = not any(t - 600 <= x <= t + 1200 for x in audit)
        else:
            thieu.append('ô không có điều kiện')
    except Exception as e:
        thieu.append('lỗi truy vấn: ' + str(e)[-200:])
    ok = all(v is True for v in dk.values()) and not thieu
    kq[oid] = {'cell': cell, 't': t, 'xac_nhan': ok, 'khong_du_du_lieu': bool(thieu), 'thieu': thieu, 'dieu_kien': dk,
               **{k: c[k] for k in ('k6', 'ty_le_tai_sau_truoc', 'pg_proxy_ms', 'redis_proxy_ms', 'gw_18082_p50_ms', 'audit',
                                    'nr_throttled', 'httpcheck_error_8083_max') if k in c}}
    if not ok: kq[oid]['ly_do'] = [k for k, v in dk.items() if v is not True] + thieu

RA.write_text(json.dumps({'nguon': str(G), 'dieu_kien': 'results/T-063/chay/dieu-kien-xac-nhan.md', 'sua_sau_1': SUA_SAU_1, 'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                          'ca': kq}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for oid, v in kq.items():
    print(oid, v['cell'], 'XÁC NHẬN' if v['xac_nhan'] else 'KHÔNG', v.get('ly_do', ''), {k: v[k] for k in v if k in ('audit', 'k6', 'ty_le_tai_sau_truoc')})
