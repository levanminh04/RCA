#!/usr/bin/env python3
"""T-063 — bộ tiêm lỗi bản 2 trên exp-app (dựa trên ~/inj.py của T-062, sha256 bc711063…, giữ nguyên cách tiêm của ô cũ).

Dùng:  python3 inj2.py start <O> [--seconds N] | stop <O> | probe <O> | cleanup | ensure
In một dòng JSON mỗi lệnh. Không gửi nhãn tới ứng dụng. Đầu dò **không gọi HTTP của app** (T-063 span-goc, THIET-KE-BO-CHAY-2 #1).
Ô (danh mục: results/T-063/o-dev-bo-sung.md; thay SLOW-BOOK: WHY-83):
  EVENT-DB-LAT, REDIS-BOOK, NET-GW-BOOK  toxic latency (như T-062)
  HTTP5-EVENT, HTTP5-EVENT-FLASH          hook http.error của Event, target = sự kiện tải mới (FLASH: bộ chạy tăng tải ×3)
  CPU-BOOK-1, CPU-BOOK-2                  1 / 2 luồng đốt trong cgroup Booking (CPU-BOOK-2 = CPU-BOOK T-062)
  POOL-EVENT                              hook pool.hold = 4 connection của Event (pool max 5)
  PAUSE-PAYMENT                           docker pause payment-service
  CONSUMER-BOOK-SLOW                      toxic latency trên proxy AMQP booking-amqp (cần proxy + RABBITMQ_PORT của Booking)
  FLASH-HEALTHY, BINH-THUONG              không can thiệp
"""
import json, os, signal, socket, subprocess, sys, time, uuid, datetime as dt, urllib.request, pathlib

A = pathlib.Path('/opt/flash-ticket-app')
STATE = pathlib.Path('/home/ubuntu/t063/inj'); STATE.mkdir(parents=True, exist_ok=True)
TOXI = 'http://127.0.0.1:8474'
EVENT_ID = '3e7c1df9-ada4-4081-94a1-548b80a5da86'   # sự kiện tải mua vé (results/T-062/tai-2/BAN-GIAO-1-giao-dich.md)
BOOK = 'flash-ticket-booking-service-booking-service-1'
PAY = 'flash-ticket-payment-service-payment-service-1'
AMQP_PROXY = {'name': 'booking-amqp', 'listen': '127.0.0.1:15673', 'upstream': '127.0.0.1:5672', 'enabled': True}

CELLS = {
    'EVENT-DB-LAT': dict(kind='toxic', proxy='event-jdbc', latency=30),
    'REDIS-BOOK': dict(kind='toxic', proxy='booking-redis', latency=200),
    'NET-GW-BOOK': dict(kind='toxic', proxy='gateway-booking-http', latency=300),
    # bản 2 (D2 d2b-2a7f481a): latency 200 ms không giới hạn thông lượng → không tồn queue; đổi sang bandwidth (KB/s)
    'CONSUMER-BOOK-SLOW': dict(kind='toxic', proxy='booking-amqp', toxic='bandwidth', rate=1),  # lần 3 (lần 2 rate=2 không tồn queue)
    'HTTP5-EVENT': dict(kind='hook', service='event-service', action='http.error', target=EVENT_ID, value=0),
    'HTTP5-EVENT-FLASH': dict(kind='hook', service='event-service', action='http.error', target=EVENT_ID, value=0),
    'POOL-EVENT': dict(kind='hook', service='event-service', action='pool.hold', target=None, value=4),
    'CPU-BOOK-1': dict(kind='cpu', workers=1),
    'CPU-BOOK-2': dict(kind='cpu', workers=2),
    'PAUSE-PAYMENT': dict(kind='pause', container=PAY),
    'FLASH-HEALTHY': dict(kind='none'),
    'BINH-THUONG': dict(kind='none'),
}


def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def out(**k): print(json.dumps({'t': now(), **k}, ensure_ascii=False)); sys.stdout.flush()
def sh(*c, check=True): return subprocess.run(c, capture_output=True, text=True, check=check).stdout


def http(method, path, body=None):
    req = urllib.request.Request(TOXI + path, method=method, data=None if body is None else json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=5) as r:
        t = r.read(); return json.loads(t) if t else None


def write_lease(service, action, target, value, seconds=300):
    d = A / 'rca-faults' / service / 'control'
    c = {'leaseId': str(uuid.uuid4()), 'action': action, 'value': value, 'subject': '',
         'expiresAt': (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=seconds)).isoformat()}
    if target: c['targetId'] = target
    tmp = f'/tmp/ctl-{uuid.uuid4().hex}.json'
    pathlib.Path(tmp).write_text(json.dumps(c) + '\n')
    sh('sudo', 'install', '-o', '10001', '-g', '10001', '-m', '0640', tmp, str(d / 'control.tmp'))
    sh('sudo', 'mv', '-f', str(d / 'control.tmp'), str(d / 'control.json'))
    os.unlink(tmp)
    return c['leaseId']


def renewer(cell, seconds):
    c = CELLS[cell]; end = time.monotonic() + seconds
    while time.monotonic() < end:
        lid = write_lease(c['service'], c['action'], c['target'], c['value'], seconds=min(180, int(end - time.monotonic()) + 5))
        with open(STATE / f'{cell}.leases', 'a') as f: f.write(json.dumps({'t': now(), 'leaseId': lid}) + '\n')
        time.sleep(min(120, max(1, end - time.monotonic())))
    write_lease(c['service'], 'off', None, 0, seconds=30)


def ensure():
    """Proxy AMQP của Booking phải tồn tại (Booking kết nối qua nó). Idempotent."""
    px = http('GET', '/proxies')
    if AMQP_PROXY['name'] not in px:
        http('POST', '/proxies', AMQP_PROXY)
    out(op='ensure', proxies=sorted(http('GET', '/proxies')))


def start(cell, seconds):
    c = CELLS[cell]
    if c['kind'] == 'toxic':
        if c.get('toxic') == 'bandwidth':
            body = {'name': 't063', 'type': 'bandwidth', 'stream': 'downstream', 'toxicity': 1.0, 'attributes': {'rate': c['rate']}}
        else:
            body = {'name': 't063', 'type': 'latency', 'stream': 'downstream', 'toxicity': 1.0,
                    'attributes': {'latency': c['latency'], 'jitter': 0}}
        http('POST', f"/proxies/{c['proxy']}/toxics", body)
    elif c['kind'] == 'hook':
        p = subprocess.Popen([sys.executable, __file__, '_renew', cell, str(seconds)], stdout=open(STATE / f'{cell}.renew.log', 'a'),
                             stderr=subprocess.STDOUT, start_new_session=True)
        (STATE / f'{cell}.pid').write_text(str(p.pid))
    elif c['kind'] == 'cpu':
        for _ in range(c['workers']):
            sh('docker', 'exec', '-d', BOOK, 'timeout', str(seconds), 'sh', '-c', ': rcaburn; while :; do :; done')
    elif c['kind'] == 'pause':
        sh('docker', 'pause', c['container'])
        (STATE / f'{cell}.pause-deadline').write_text(str(time.time() + seconds))
    if c['kind'] in ('toxic', 'pause'):
        # Tự gỡ đúng hạn trên exp-app, độc lập laptop (mất mạng laptop 13/11 04:19–05:00Z): tiến trình tách phiên,
        # ngủ tới hạn + 5 s rồi gọi stop (idempotent). Hook có lease tự hết; CPU có `timeout`.
        p = subprocess.Popen([sys.executable, __file__, '_het_han', cell, str(time.time() + seconds + 5)],
                             stdout=open(STATE / f'{cell}.het-han.log', 'a'), stderr=subprocess.STDOUT, start_new_session=True)
        (STATE / f'{cell}.het-han.pid').write_text(str(p.pid))
    out(op='start', cell=cell, seconds=seconds, params=c)


def het_han(cell, deadline):
    time.sleep(max(0, float(deadline) - time.time()))
    try:
        stop(cell); out(op='het-han-stop', cell=cell)
    except Exception as e:
        out(op='het-han-loi', cell=cell, err=str(e)[:200])
    finally:
        for pf in STATE.glob(f'{cell}.het-han.pid'): pf.unlink()


def stop(cell):
    c = CELLS[cell]
    hp = STATE / f'{cell}.het-han.pid'
    if hp.exists() and sys.argv[1:2] != ['_het_han']:  # dừng sớm bình thường: hủy tiến trình hẹn giờ
        try: os.killpg(int(hp.read_text()), signal.SIGTERM)
        except (ProcessLookupError, ValueError): pass
        hp.unlink(missing_ok=True)
    if c['kind'] == 'toxic':
        try: http('DELETE', f"/proxies/{c['proxy']}/toxics/t063")
        except urllib.error.HTTPError as e:
            if e.code != 404: raise  # 404 = không còn toxic (đã sạch); lỗi khác phải báo lên bộ chạy
        except Exception:
            raise
    elif c['kind'] == 'hook':
        pf = STATE / f'{cell}.pid'
        if pf.exists():
            try: os.killpg(int(pf.read_text()), signal.SIGTERM)
            except ProcessLookupError: pass
            pf.unlink()
        write_lease(c['service'], 'off', None, 0, seconds=30)
    elif c['kind'] == 'cpu':
        sh('docker', 'exec', BOOK, 'pkill', '-f', 'rcaburn', check=False)
    elif c['kind'] == 'pause':
        r = subprocess.run(['docker', 'unpause', c['container']], capture_output=True, text=True)
        if r.returncode != 0 and 'is not paused' not in r.stderr: raise RuntimeError('unpause lỗi: ' + r.stderr[-200:])
        for pf in STATE.glob(f'{cell}.pause-deadline'): pf.unlink()
    out(op='stop', cell=cell)


def cgroup(name):
    cid = sh('docker', 'inspect', name, '--format', '{{.Id}}').strip()
    b = pathlib.Path(f'/sys/fs/cgroup/system.slice/docker-{cid}.scope')
    st = dict(l.split() for l in (b / 'cpu.stat').read_text().splitlines())
    pr = (b / 'cpu.pressure').read_text().splitlines()[0] if (b / 'cpu.pressure').exists() else ''
    return {'usage_usec': int(st['usage_usec']), 'nr_throttled': int(st.get('nr_throttled', 0)),
            'throttled_usec': int(st.get('throttled_usec', 0)), 'pressure': pr}


def probe(cell):
    """Đầu dò độc lập, không gọi HTTP của app (không sinh span ứng dụng)."""
    r = {'cell': cell}
    try: r['toxics'] = {k: [t['name'] + ':' + str(t['attributes']) for t in v.get('toxics', [])] for k, v in http('GET', '/proxies').items()}
    except Exception as e: r['toxics_error'] = str(e)[:200]
    for svc in ('booking-service', 'event-service'):
        f = A / 'rca-faults' / svc / 'audit' / 'executions.jsonl'
        lines = sh('sudo', 'tail', '-n', '2000', str(f), check=False).splitlines()
        ops = {}
        for l in lines:
            try: o = json.loads(l); k = o.get('operation') or o.get('event')
            except Exception: continue
            ops[k] = ops.get(k, 0) + 1
        r[f'audit_{svc}'] = {'lines_tail2000': len(lines), 'ops': ops}
    try: r['cgroup_booking'] = cgroup(BOOK)
    except Exception as e: r['cgroup_booking'] = str(e)[:120]
    r['burn_procs'] = sh('docker', 'exec', BOOK, 'sh', '-c', "ps -o args | grep -c '^sh -c : rcaburn'", check=False).strip()
    r['payment_state'] = sh('docker', 'inspect', PAY, '--format', '{{.State.Status}} {{.State.Paused}}', check=False).strip()
    try:  # áp lực CPU toàn máy (REVIEW T-063 R4): dòng some/full, avg10/60/300 và total (µs)
        r['psi_cpu_may'] = pathlib.Path('/proc/pressure/cpu').read_text().strip().splitlines()
    except Exception as e: r['psi_cpu_may'] = str(e)[:80]
    def rtt(port):
        t = time.perf_counter(); s = socket.create_connection(('127.0.0.1', port), timeout=3); s.close()
        return round((time.perf_counter() - t) * 1000, 2)
    r['tcp_connect_ms'] = {}
    for p in (5432, 15433, 6379, 16379, 5672, 15673, 8082, 18082):
        try: r['tcp_connect_ms'][str(p)] = rtt(p)
        except Exception as e: r['tcp_connect_ms'][str(p)] = str(e)[:40]
    def redis_ping(port):
        s = socket.create_connection(('127.0.0.1', port), timeout=3); t = time.perf_counter()
        s.sendall(b'PING\r\n'); s.recv(64); s.close(); return round((time.perf_counter() - t) * 1000, 2)
    try: r['redis_ping_ms'] = {'direct': redis_ping(6379), 'proxy': redis_ping(16379)}
    except Exception as e: r['redis_ping_ms'] = str(e)[:120]
    def pg_rtt(port):
        s = socket.create_connection(('127.0.0.1', port), timeout=3); t = time.perf_counter()
        s.sendall(b'\x00\x00\x00\x08\x04\xd2\x16\x2f'); s.recv(1); s.close(); return round((time.perf_counter() - t) * 1000, 2)
    try: r['pg_sslrequest_ms'] = {'direct': pg_rtt(5432), 'proxy_event': pg_rtt(15433)}
    except Exception as e: r['pg_sslrequest_ms'] = str(e)[:120]
    out(op='probe', **r)


def trang_thai_sach():
    """Kiểm môi trường không còn can thiệp (REVIEW T-063 R1): toxic t063, pause, luồng đốt, lease hook đang hiệu lực."""
    con = []
    for name, v in http('GET', '/proxies').items():
        if any(t.get('name') == 't063' for t in v.get('toxics', [])): con.append(f'toxic:{name}')
    if 'true' in sh('docker', 'inspect', PAY, '--format', '{{.State.Paused}}', check=False).lower(): con.append('pause:payment')
    n = sh('docker', 'exec', BOOK, 'sh', '-c', "ps -o args | grep -c '^sh -c : rcaburn' || true", check=False).strip() or '0'
    if n != '0': con.append(f'burn:{n}')
    for svc in ('booking-service', 'event-service'):
        f = A / 'rca-faults' / svc / 'control' / 'control.json'
        try:
            c = json.loads(sh('sudo', 'cat', str(f)))
            if c.get('action') != 'off' and dt.datetime.fromisoformat(c['expiresAt']) > dt.datetime.now(dt.timezone.utc):
                con.append(f'lease:{svc}:{c.get("action")}')
        except Exception:
            pass
    for pf in STATE.glob('*.pid'): con.append(f'renewer:{pf.stem}')
    return con


def cleanup():
    loi = []
    for k, c in CELLS.items():
        if c['kind'] != 'none':
            try: stop(k)
            except Exception as e: loi.append({'cell': k, 'err': str(e)[:200]}); out(op='cleanup-error', cell=k, err=str(e)[:200])
    con = trang_thai_sach()
    out(op='cleanup', sach=not con, con_lai=con, loi=loi)


def verify():
    """Gỡ pause/toxic quá hạn (deadline ghi lúc start) rồi báo trạng thái sạch. Không tự gỡ can thiệp còn hạn."""
    for pf in STATE.glob('*.pause-deadline'):
        try:
            if time.time() > float(pf.read_text()):
                sh('docker', 'unpause', PAY, check=False); pf.unlink()
        except ValueError:
            pass
    con = trang_thai_sach()
    out(op='verify', sach=not con, con_lai=con)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == '_renew': renewer(a[1], int(a[2]))
    elif a[0] == 'start': start(a[1], int(a[3]) if len(a) > 3 and a[2] == '--seconds' else 600)
    elif a[0] == 'stop': stop(a[1])
    elif a[0] == 'probe': probe(a[1] if len(a) > 1 else '-')
    elif a[0] == 'cleanup': cleanup()
    elif a[0] == 'ensure': ensure()
    elif a[0] == 'verify': verify()
    elif a[0] == '_het_han': het_han(a[1], a[2])
    else: raise SystemExit(__doc__)
