#!/usr/bin/env python3
"""T-063 bộ chạy bản 3 — chạy TRÊN exp-obs (Minh quyết 13/11, DECISIONS "Chạy bộ điều phối đợt thu trên exp-obs").
Dùng (trên exp-obs, thư mục ~/rca-dieu-phoi): nohup setsid python3 -B runner3.py thu --lich lich-2.json > chay/runner3.out 2>&1 &
Khác runner2 (laptop) CHỈ ở phần vận chuyển: M1/đóng gói chạy cục bộ, SSH tới exp-app bằng khóa ~/rca-dieu-phoi/keys,
tải qua tai_linux.py (bản Python của chay-tai.ps1, L1), sổ/gói ca/nhật ký trong ~/rca-dieu-phoi. Logic chu kỳ, đầu dò,
kiểm sạch, thử lại, stage lại khi M1 lỗi giữ nguyên runner2 (đã qua REVIEW T-063 R1).

Nền: results/T-062/chay/runner.py (sổ tiêm hash nối dòng, mã ca mờ, M1 qua stage-m1/run-m1 ghim, M1 tuần tự ở luồng nền,
STOP). Thay đổi có lý do: results/T-063/chay/THIET-KE-BO-CHAY-2.md (#1–#7).
- Tải: kịch bản hành trình mua vé của L1 (results/T-062/tai-2/chay-tai.ps1 -Scenario hanh-trinh); FLASH: đổi bậc ×3 tại
  mốc t trong cùng lượt (-Multiplier 3 -BuocTai 600, chờ L1 bổ sung — nếu chưa có, lệnh tải báo lỗi và ô bị chặn).
- Tiêm: ~/inj2.py trên exp-app (results/T-063/tiem-loi/inj2.py). Đầu dò không gọi HTTP của app; đối xứng t−240 và t+60;
  đầu dò dài sau cửa sổ ở t+330.
- Sau M1 mỗi ca: gói ghim (safe-export.py) + gói metric bổ sung (results/T-063/dong-goi/xuat_bo_sung.py) → results/T-063/ca/<id>/.
- Phục hồi: M1/stage lỗi → stage lại cùng t với mã mờ mới (một lần), giữ thư mục cũ; ghi ánh xạ trong nhật ký.
- Luật 21: lỗi một ô chỉ chặn ô đó; tải không khởi động được 2 lần → dừng lượt; dữ liệu đã thu giữ nguyên.
Dừng khẩn: ~/rca-dieu-phoi/STOP (trên exp-obs).
"""
import datetime as dt, hashlib, json, os, queue, secrets, subprocess, sys, threading, time, traceback
from pathlib import Path

BASE = Path('/home/ubuntu/rca-dieu-phoi')
OUTR = Path(os.environ.get('RCA_DP_OUT', str(BASE)))  # chạy thử ngắn: RCA_DP_OUT=~/rca-dieu-phoi/thu-ngan, không lẫn sổ đợt thu
CHAY = OUTR / 'chay'; SO = OUTR / 'tiem-loi/so-thu2.jsonl'; CA = OUTR / 'ca'
STOP = BASE / 'STOP'
SSH = 'ssh'
KEYS = {'app': (str(BASE / 'keys/exp-app.key'), 'ubuntu@129.221.208.47')}
KNOWN = str(BASE / 'keys/known_hosts')
TAI = BASE / 'tai_linux.py'
XUAT = BASE / 'xuat_bo_sung.py'
PHASE = 600
LOCK = threading.Lock()


def now(): return dt.datetime.now(dt.timezone.utc)
def iso(t=None): return (t or now()).isoformat()


def log(msg, **k):
    line = json.dumps({'t': iso(), 'msg': msg, **k}, ensure_ascii=False)
    with LOCK:
        with open(CHAY / 'nhat-ky-2.jsonl', 'a', encoding='utf-8') as f: f.write(line + '\n')
    print(line, flush=True)


def ledger(event, **k):
    with LOCK:
        SO.parent.mkdir(parents=True, exist_ok=True)
        prev, seq = '0' * 64, 0
        if SO.exists():
            lines = SO.read_text(encoding='utf-8').splitlines()
            if lines:
                prev = hashlib.sha256(lines[-1].encode()).hexdigest(); seq = json.loads(lines[-1])['seq'] + 1
        rec = {'seq': seq, 'utc': iso(), 'event': event, **k, 'prev_sha256': prev}
        with open(SO, 'a', encoding='utf-8') as f: f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + '\n')


def state(**k):
    if threading.current_thread().name != 'MainThread': return
    p = CHAY / 'trang-thai-2.json'
    with LOCK:
        d = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        d.update(k, heartbeat_utc=iso())
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')


def ssh(m, cmd, timeout=180, check=True, stdin=None):
    if m == 'obs':  # chạy cục bộ trên exp-obs
        r = subprocess.run(['bash', '-c', cmd], capture_output=True, text=True, timeout=timeout, encoding='utf-8',
                           errors='replace', input=stdin)
        if check and r.returncode != 0: raise RuntimeError(f'local rc={r.returncode}: {r.stderr[-400:]}')
        return r.stdout
    key, tgt = KEYS[m]
    r = subprocess.run([SSH, '-i', key, '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=15', '-o', 'ServerAliveInterval=20',
                        '-o', f'UserKnownHostsFile={KNOWN}', tgt, cmd], capture_output=True, text=True, timeout=timeout,
                       encoding='utf-8', errors='replace', input=stdin)
    if check and r.returncode != 0: raise RuntimeError(f'ssh {m} rc={r.returncode}: {r.stderr[-400:]}')
    return r.stdout


def tai(*args, timeout=900):
    """Gọi tai_linux.py (L1); trả JSON một dòng; lỗi → ngoại lệ."""
    r = subprocess.run(['python3', '-B', str(TAI)] + [str(x) for x in args], capture_output=True, text=True,
                       timeout=timeout, encoding='utf-8', errors='replace', stdin=subprocess.DEVNULL)
    dong = [l for l in r.stdout.splitlines() if l.strip().startswith('{')]
    if r.returncode != 0: raise RuntimeError(f'tai {args[0]} rc={r.returncode}: {(r.stdout + r.stderr)[-600:]}')
    if not dong: raise RuntimeError(f'tai {args[0]}: không có dòng JSON')
    v = json.loads(dong[-1])
    if not v.get('ok'): raise RuntimeError(f'tai {args[0]}: ' + json.dumps(v)[-600:])
    return v['result']


def dang_chay(r):
    """Kết quả `tai get` → container k6 còn chạy? (docker State.Running)."""
    return bool(r['state']['Running'])


def inj(op, cell='-', seconds=None):
    """Lỗi từ inj2 (ssh rc ≠ 0, dòng cleanup-error) được ném lên — không nuốt (REVIEW T-063 R1)."""
    cmd = f'python3 ~/inj2.py {op} {cell}' + (f' --seconds {seconds}' if seconds else '')
    recs = [json.loads(l) for l in ssh('app', cmd, timeout=120).splitlines() if l.startswith('{')]
    if any(r.get('op') == 'cleanup-error' for r in recs): raise RuntimeError(f'inj2 {op}: ' + json.dumps(recs)[-400:])
    return recs[-1] if recs else {}


def bao_dam_sach(nhan):
    """Trước mỗi chu kỳ và sau mỗi lỗi: môi trường phải sạch; thử dọn một lần; không sạch thì dừng lượt (luật 21: lỗi
    môi trường dừng cả máy). Ghi sổ để biết khoảng ảnh hưởng."""
    v = inj('verify')
    if v.get('sach'): return True
    ledger('dirty', where=nhan, con_lai=v.get('con_lai'))
    try:
        c = inj('cleanup')
    except Exception as e:
        c = {'sach': False, 'err': str(e)[-300:]}
    if c.get('sach'): ledger('dirty-cleaned', where=nhan); return True
    ledger('run-abort-dirty', where=nhan, cleanup=c); log('DỪNG LƯỢT: không đưa được môi trường về sạch', where=nhan, cleanup=c)
    return False


def stopped(): return STOP.exists()


def wait_until(t_epoch, what):
    while time.time() < t_epoch:
        if stopped(): raise KeyboardInterrupt('STOP')
        time.sleep(min(5, max(0.2, t_epoch - time.time())))
        state(waiting=what, remaining_s=int(t_epoch - time.time()))


def start_load(tag, flash=False, seconds=1800):
    extra = ['--buoc-tai', 600, '--multiplier', 3] if flash else []
    out = tai('start', '--tag', tag, '--seconds', seconds, *extra)
    t_k6 = time.time()
    log('load started', tag=tag, flash=flash, out=json.dumps(out)[-300:])
    time.sleep(20)
    st = tai_thu_lai('get', '--tag', tag)
    if not dang_chay(st): raise RuntimeError('k6 không chạy sau 20 s: ' + json.dumps(st)[-300:])
    return t_k6


def tai_thu_lai(*args, timeout=900, lan=4):
    """SSH tới máy tải có thể chập chờn → thử lại, giãn 30 s (chỉ get/receive, không start)."""
    for k in range(lan):
        try: return tai(*args, timeout=timeout)
        except Exception as e:
            if k == lan - 1: raise
            log('tai lỗi, thử lại', args=[str(x) for x in args][:2], lan=k + 1, err=str(e)[-200:]); time.sleep(30)


def finish_load(tag):
    for _ in range(60):
        if not dang_chay(tai_thu_lai('get', '--tag', tag)): break
        time.sleep(5)
    out = tai_thu_lai('receive', '--tag', tag)
    log('load received', tag=tag, out=json.dumps(out)[-300:])


def nhan_ca(oid, t):
    """Gói ghim + gói bổ sung, cục bộ trên exp-obs: ~/rca-dieu-phoi/ca/<oid>.tgz, <oid>/prometheus-bo-sung.json."""
    CA.mkdir(parents=True, exist_ok=True)
    ex = ssh('obs', f'sudo python3 /home/ubuntu/t058/safe-export.py case {oid} >/dev/null && sudo tar -czf {CA}/{oid}.tgz '
                    f'-C /opt/flash-ticket-rca cases/{oid} outputs/{oid} && sudo chown ubuntu {CA}/{oid}.tgz && sha256sum {CA}/{oid}.tgz',
             timeout=600)
    bs = ssh('obs', f'python3 {XUAT} --t {t}', timeout=900)
    (CA / oid).mkdir(parents=True, exist_ok=True)
    (CA / oid / 'prometheus-bo-sung.json').write_text(bs, encoding='utf-8')
    return ex.split()[0], hashlib.sha256(bs.encode()).hexdigest()


M1Q = queue.Queue()


def m1_worker():
    while True:
        job = M1Q.get()
        if job is None: return
        oid, t = job['id'], job['t']
        try: wait_until(t + PHASE + 150, f'M1 {oid} chờ flush')
        except KeyboardInterrupt: log('M1 bỏ qua do STOP', id=oid); continue
        for lan, ma in enumerate([oid, oid + secrets.token_hex(2)]):
            try:
                ssh('obs', f'sudo /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/stage-m1.py --id {ma} --t {t}', timeout=900)
                r2 = ssh('obs', f'sudo -u rca /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/run-m1.py --id {ma}', timeout=1800)
                s = json.loads(r2[r2.index('{'):])
                tgz, bs = nhan_ca(ma, t)
                log('M1 xong', id=ma, goc=oid, lan=lan, status=s.get('status'), deterministic=s.get('deterministic_repeat'),
                    tgz_sha256=tgz, bo_sung_sha256=bs)
                break
            except Exception as e:
                log('M1 LỖI (chỉ chặn ca này)', id=ma, goc=oid, lan=lan, err=str(e)[-600:])


def chay_lich(lich):
    items = json.loads(Path(lich).read_text(encoding='utf-8'))['chu_ky']
    threading.Thread(target=m1_worker, daemon=True).start()
    ledger('thu2-begin', lich=str(lich), lich_sha256=hashlib.sha256(Path(lich).read_bytes()).hexdigest(), n=len(items))
    ssh('app', 'python3 ~/inj2.py ensure', timeout=60)
    for i, it in enumerate(items):
        if stopped(): log('STOP trước chu kỳ', i=i); break
        try:
            sach = bao_dam_sach(f'truoc-chu-ky-{i}')
        except Exception as e:
            ledger('run-abort-dirty', where=f'truoc-chu-ky-{i}', err=str(e)[-300:]); sach = False
        if not sach: break
        cell = it['o']; oid = secrets.token_hex(4); tag = 't2-' + oid; flash = cell in ('FLASH-HEALTHY', 'HTTP5-EVENT-FLASH')
        state(cycle=i, of=len(items), opaque_id=oid, phase='start')
        ledger('cycle-begin', i=i, opaque_id=oid, cell=cell, load_tag=tag)
        try:
            S = start_load(tag, flash=flash)
        except Exception as e:
            log('LỖI khởi động tải — thử lại sau 60 s', err=str(e)[-400:]); time.sleep(60)
            try: S = start_load(tag, flash=flash)
            except Exception as e2:
                ledger('cycle-abort', i=i, opaque_id=oid, reason='load', err=str(e2)[-400:]); log('DỪNG LƯỢT: tải hỏng'); break
        ledger('load-start', opaque_id=oid, epoch=S)
        t = int(S + PHASE); fault_ok = None
        try:
            wait_until(t - 240, 'nền'); ledger('probe', opaque_id=oid, phase='t-240', probe=inj('probe'))
            wait_until(t, 'nền')
            if cell in ('BINH-THUONG', 'FLASH-HEALTHY'):
                ledger('mark', opaque_id=oid, t=t, cell=cell)
            else:
                try:
                    s = inj('start', cell, PHASE); ledger('fault-start', opaque_id=oid, cell=cell, t=t, inj=s); fault_ok = True
                except Exception as e:
                    ledger('fault-start-failed', opaque_id=oid, cell=cell, err=str(e)[-400:]); fault_ok = False
            wait_until(t + 60, 'lỗi'); ledger('probe', opaque_id=oid, phase='t+60', probe=inj('probe', cell))
            wait_until(t + 330, 'lỗi'); ledger('probe', opaque_id=oid, phase='t+330', probe=inj('probe', cell))
            wait_until(S + 2 * PHASE, 'lỗi')
            if fault_ok: ledger('fault-stop', opaque_id=oid, cell=cell, inj=inj('stop', cell))
            if fault_ok is not False:
                M1Q.put({'id': oid, 't': t}); ledger('m1-queued', opaque_id=oid, t=t)
            else:
                ledger('m1-skipped', opaque_id=oid, reason='can thiệp không khởi động được')
            wait_until(S + 2 * PHASE + 60, 'hồi phục'); ledger('probe', opaque_id=oid, phase='hoi+60', probe=inj('probe', cell))
            wait_until(S + 3 * PHASE + 5, 'hồi phục')
        except KeyboardInterrupt:
            log('STOP giữa chu kỳ', i=i); inj('cleanup'); tai('stop', '--tag', tag)
            ledger('cycle-stopped', opaque_id=oid); finish_load(tag); break
        except Exception as e:
            log('LỖI chu kỳ (chỉ chặn ô này)', i=i, err=traceback.format_exc()[-800:])
            ledger('cycle-error', opaque_id=oid, err=str(e)[-400:])
            try: sach = bao_dam_sach(f'sau-loi-chu-ky-{i}')
            except Exception as e2:
                ledger('run-abort-dirty', where=f'sau-loi-chu-ky-{i}', err=str(e2)[-300:]); sach = False
            if not sach:
                try: finish_load(tag)
                except Exception: pass
                ledger('cycle-end', opaque_id=oid); break
        try: finish_load(tag)
        except Exception as e: log('LỖI nhận tải', tag=tag, err=str(e)[-400:])
        ledger('cycle-end', opaque_id=oid)
    M1Q.put(None)
    while any(x.name != 'MainThread' and x.is_alive() for x in threading.enumerate()): time.sleep(10)
    ledger('thu2-end'); state(phase='XONG'); log('Lượt thu xong')


D2_CELLS = ['EVENT-DB-LAT', 'REDIS-BOOK', 'NET-GW-BOOK', 'CONSUMER-BOOK-SLOW', 'HTTP5-EVENT', 'POOL-EVENT',
            'CPU-BOOK-1', 'CPU-BOOK-2', 'PAUSE-PAYMENT']


def chay_d2(cells=None):
    """Xác nhận can thiệp (ngoài chu kỳ chính): mỗi ô 150 s lỗi dưới tải, đầu dò t+45/t+140/sau+30; không phải ca RCA."""
    cells = cells or D2_CELLS; tag = 'd2b-' + secrets.token_hex(4)
    ledger('d2-begin', tag=tag, note='xác nhận can thiệp bản 2; không phải ca RCA', cells=cells)
    ssh('app', 'python3 ~/inj2.py ensure', timeout=60)
    # Tải phải phủ hết D2 (lượt d2b-2a7f481a: tải 1800 s hết ở 02:53Z khi còn 2 ô — D2B-KET-QUA.md)
    t0 = start_load(tag, seconds=min(3600, 180 + 260 * len(cells) + 60)); plan = []
    try:
        wait_until(t0 + 120, 'd2 nền'); ledger('d2-probe', cell='-', phase='baseline', probe=inj('probe'))
        for cell in cells:
            s = inj('start', cell, 150); ts = time.time(); ledger('d2-start', cell=cell, inj=s)
            wait_until(ts + 45, f'd2 {cell}'); ledger('d2-probe', cell=cell, phase='fault+45', probe=inj('probe', cell))
            wait_until(ts + 140, f'd2 {cell}'); ledger('d2-probe', cell=cell, phase='fault+140', probe=inj('probe', cell))
            wait_until(ts + 150, f'd2 {cell}')
            e = inj('stop', cell); te = time.time(); ledger('d2-stop', cell=cell, inj=e)
            plan.append({'cell': cell, 'start_epoch': ts, 'stop_epoch': te})
            wait_until(te + 30, f'd2 {cell} hồi'); ledger('d2-probe', cell=cell, phase='after+30', probe=inj('probe', cell))
            wait_until(te + 75, 'd2 khoảng nghỉ')
    except KeyboardInterrupt:
        log('STOP trong D2'); inj('cleanup')
    finally:
        (CHAY / f'{tag}-plan.json').write_text(json.dumps(plan, indent=1), encoding='utf-8')
        tai('stop', '--tag', tag); time.sleep(30)
        finish_load(tag); ledger('d2-end', tag=tag); log('D2 xong', tag=tag)


if __name__ == '__main__':
    CHAY.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1]
    lich = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--lich' else BASE / 'lich-2.json'
    (OUTR / 'tiem-loi').mkdir(parents=True, exist_ok=True)
    if mode == 'thu': chay_lich(lich)
    elif mode == 'd2': chay_d2(sys.argv[2].split(',') if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None)
    else: raise SystemExit(__doc__)
