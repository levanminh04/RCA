#!/usr/bin/env python3
"""T-062 D1 — bộ tiêm lỗi trên exp-app cho 7 ô phát triển (T-059).

Dùng:  python3 inj.py start <O> [--seconds N]   bật ô O (tự gia hạn lease hook trong N giây)
       python3 inj.py stop  <O>                 tắt ô O, dọn sạch
       python3 inj.py probe <O>                 đầu dò độc lập (JSON) — không phải đầu vào RCA
       python3 inj.py cleanup                   tắt mọi lỗi (dùng khi khẩn)
In một dòng JSON cho mỗi lệnh. Không ghi gì vào kênh telemetry; không gửi nhãn tới ứng dụng.
"""
import json, os, subprocess, sys, time, uuid, datetime as dt, urllib.request, signal, pathlib

A = pathlib.Path('/opt/flash-ticket-app')
STATE = pathlib.Path('/home/ubuntu/t062/inj'); STATE.mkdir(parents=True, exist_ok=True)
TOXI = 'http://127.0.0.1:8474'
EVENT_ID = '68bbd408-d7c0-4236-b139-0ecf9cd5d826'   # results/T-062/tai/k6/fixtures.json
ORDER_ID = 'b16ae2e8-3893-466d-94eb-08ace3a9ace2'
BOOK = 'flash-ticket-booking-service-booking-service-1'

# Cường độ cố định (chọn trước D2, ghi trong results/T-062/tiem-loi/o-loi.md)
CELLS = {
    'EVENT-DB-LAT': dict(kind='toxic', proxy='event-jdbc', latency=30),
    'REDIS-BOOK':   dict(kind='toxic', proxy='booking-redis', latency=200),
    'NET-GW-BOOK':  dict(kind='toxic', proxy='gateway-booking-http', latency=300),
    'HTTP5-EVENT':  dict(kind='hook', service='event-service', action='http.error', target=EVENT_ID, value=0),
    'SLOW-BOOK':    dict(kind='hook', service='booking-service', action='http.delay', target=ORDER_ID, value=1000),
    'CPU-BOOK':     dict(kind='cpu', workers=2),
    'FLASH-HEALTHY': dict(kind='none'),   # tải tăng do bộ chạy điều khiển ở máy tải
}

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def out(**k): print(json.dumps({'t': now(), **k}, ensure_ascii=False)); sys.stdout.flush()
def sh(*c, check=True): return subprocess.run(c, capture_output=True, text=True, check=check).stdout

def http(method, path, body=None):
    req = urllib.request.Request(TOXI + path, method=method,
                                 data=None if body is None else json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=5) as r:
        t = r.read(); return json.loads(t) if t else None

def subject():
    s = sh('docker', 'exec', 'flash-ticket-infra-postgres-1', 'psql', '-U', 'postgres', '-d', 'booking_db', '-tAc',
           f"select buyer_subject from booking_schema.tbl_orders where id='{ORDER_ID}'").strip()
    if not s: raise SystemExit('không tìm thấy chủ đơn fixture')
    return s

def write_lease(service, action, target, value, subj, seconds=300):
    d = A / 'rca-faults' / service / 'control'
    c = {'leaseId': str(uuid.uuid4()), 'expiresAt': (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=seconds)).isoformat(),
         'action': action, 'value': value, 'subject': subj}
    if target: c['targetId'] = target
    tmp = f'/tmp/ctl-{uuid.uuid4().hex}.json'
    pathlib.Path(tmp).write_text(json.dumps(c) + '\n')
    sh('sudo', 'install', '-o', '10001', '-g', '10001', '-m', '0640', tmp, str(d / 'control.tmp'))
    sh('sudo', 'mv', '-f', str(d / 'control.tmp'), str(d / 'control.json'))
    os.unlink(tmp)
    return c['leaseId']

def renewer(cell, seconds):
    """Tiến trình nền: gia hạn lease mỗi 120 s (mỗi lease 180 s) cho tới hết N giây hoặc bị dừng."""
    c = CELLS[cell]; subj = subject() if c['service'] == 'booking-service' else ''
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        lid = write_lease(c['service'], c['action'], c['target'], c['value'], subj, seconds=min(180, int(end - time.monotonic()) + 5))
        with open(STATE / f'{cell}.leases', 'a') as f: f.write(json.dumps({'t': now(), 'leaseId': lid}) + '\n')
        time.sleep(min(120, max(1, end - time.monotonic())))
    write_lease(c['service'], 'off', None, 0, '', seconds=30)

def start(cell, seconds):
    c = CELLS[cell]
    if c['kind'] == 'toxic':
        http('POST', f"/proxies/{c['proxy']}/toxics",
             {'name': 't062', 'type': 'latency', 'stream': 'downstream', 'toxicity': 1.0,
              'attributes': {'latency': c['latency'], 'jitter': 0}})
    elif c['kind'] == 'hook':
        p = subprocess.Popen([sys.executable, __file__, '_renew', cell, str(seconds)],
                             stdout=open(STATE / f'{cell}.renew.log', 'a'), stderr=subprocess.STDOUT, start_new_session=True)
        (STATE / f'{cell}.pid').write_text(str(p.pid))
    elif c['kind'] == 'cpu':
        for i in range(c['workers']):
            sh('docker', 'exec', '-d', BOOK, 'timeout', str(seconds), 'sh', '-c', ': rcaburn; while :; do :; done')
    out(op='start', cell=cell, seconds=seconds, params=c)

def stop(cell):
    c = CELLS[cell]
    if c['kind'] == 'toxic':
        try: http('DELETE', f"/proxies/{c['proxy']}/toxics/t062")
        except Exception as e: out(op='stop-note', cell=cell, note=str(e)[:200])
    elif c['kind'] == 'hook':
        pf = STATE / f'{cell}.pid'
        if pf.exists():
            try: os.killpg(int(pf.read_text()), signal.SIGTERM)
            except ProcessLookupError: pass
            pf.unlink()
        write_lease(c['service'], 'off', None, 0, '', seconds=30)
    elif c['kind'] == 'cpu':
        sh('docker', 'exec', BOOK, 'pkill', '-f', 'rcaburn', check=False)
    out(op='stop', cell=cell)

def cgroup(name):
    cid = sh('docker', 'inspect', name, '--format', '{{.Id}}').strip()
    base = pathlib.Path(f'/sys/fs/cgroup/system.slice/docker-{cid}.scope')
    st = dict(l.split() for l in (base / 'cpu.stat').read_text().splitlines())
    pr = (base / 'cpu.pressure').read_text().splitlines()[0] if (base / 'cpu.pressure').exists() else ''
    return {'cpu.max': (base / 'cpu.max').read_text().strip(), 'usage_usec': int(st['usage_usec']),
            'nr_throttled': int(st.get('nr_throttled', 0)), 'throttled_usec': int(st.get('throttled_usec', 0)), 'pressure': pr}

def probe(cell):
    r = {'cell': cell}
    try:
        px = http('GET', '/proxies')
        r['toxics'] = {k: [t['name'] + ':' + str(t['attributes']) for t in v.get('toxics', [])] for k, v in px.items()}
    except Exception as e: r['toxics_error'] = str(e)[:200]
    # kết nối JVM qua listener proxy (đếm socket ESTAB tới cổng listen)
    ss = sh('ss', '-tnH', 'state', 'established', check=False)
    rows = [l.split() for l in ss.splitlines() if len(l.split()) >= 4]
    r['estab_to_listener'] = {p: sum(1 for x in rows if x[3].endswith(f':{p}')) for p in (15433, 16379, 18082)}
    for svc in ('booking-service', 'event-service'):
        f = A / 'rca-faults' / svc / 'audit' / 'executions.jsonl'
        try:
            lines = sh('sudo', 'tail', '-n', '2000', str(f), check=False).splitlines()
            ops = {}
            for l in lines:
                try: o = json.loads(l).get('operation') or json.loads(l).get('event')
                except Exception: continue
                ops[o] = ops.get(o, 0) + 1
            r[f'audit_{svc}'] = {'lines_tail2000': len(lines), 'ops': ops}
        except Exception as e: r[f'audit_{svc}'] = str(e)[:120]
    try: r['cgroup_booking'] = cgroup(BOOK)
    except Exception as e: r['cgroup_booking'] = str(e)[:120]
    r['burn_procs'] = sh('docker', 'exec', BOOK, 'sh', '-c', "ps -o args | grep -c '^sh -c : rcaburn'", check=False).strip()
    # RTT độc lập: TCP connect qua proxy và trực tiếp (không gửi dữ liệu ứng dụng)
    import socket
    def rtt(port):
        t = time.perf_counter(); s = socket.create_connection(('127.0.0.1', port), timeout=3); s.close()
        return round((time.perf_counter() - t) * 1000, 2)
    r['tcp_connect_ms'] = {str(p): rtt(p) for p in (5432, 15433, 6379, 16379, 8082, 18082)}
    # Redis PING qua proxy và trực tiếp (đo trễ phản hồi — toxic latency áp ở chiều downstream)
    def redis_ping(port):
        s = socket.create_connection(('127.0.0.1', port), timeout=3); t = time.perf_counter()
        s.sendall(b'PING\r\n'); s.recv(64); s.close(); return round((time.perf_counter() - t) * 1000, 2)
    try: r['redis_ping_ms'] = {'direct': redis_ping(6379), 'proxy': redis_ping(16379)}
    except Exception as e: r['redis_ping_ms'] = str(e)[:120]
    # PostgreSQL: SSLRequest (8 byte) → server trả 1 byte; đo trễ phản hồi qua proxy Event và trực tiếp
    def pg_rtt(port):
        s = socket.create_connection(('127.0.0.1', port), timeout=3); t = time.perf_counter()
        s.sendall(b'\x00\x00\x00\x08\x04\xd2\x16\x2f'); s.recv(1); s.close(); return round((time.perf_counter() - t) * 1000, 2)
    try: r['pg_sslrequest_ms'] = {'direct': pg_rtt(5432), 'proxy_event': pg_rtt(15433)}
    except Exception as e: r['pg_sslrequest_ms'] = str(e)[:120]
    # HTTP health Booking trực tiếp và qua proxy Gateway→Booking
    def hget(url):
        t = time.perf_counter()
        try: code = urllib.request.urlopen(url, timeout=5).status
        except urllib.error.HTTPError as e: code = e.code
        except Exception as e: code = str(e)[:60]
        return {'code': code, 'ms': round((time.perf_counter() - t) * 1000, 1)}
    r['booking_health'] = {'direct': hget('http://127.0.0.1:8082/actuator/health'), 'proxy': hget('http://127.0.0.1:18082/actuator/health')}
    out(op='probe', **r)

def cleanup():
    for k, c in CELLS.items():
        if c['kind'] != 'none':
            try: stop(k)
            except Exception as e: out(op='cleanup-error', cell=k, err=str(e)[:200])

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == '_renew': renewer(a[1], int(a[2]))
    elif a[0] == 'start': start(a[1], int(a[3]) if len(a) > 3 and a[2] == '--seconds' else 600)
    elif a[0] == 'stop': stop(a[1])
    elif a[0] == 'probe': probe(a[1] if len(a) > 1 else '-')
    elif a[0] == 'cleanup': cleanup()
    else: raise SystemExit(__doc__)
