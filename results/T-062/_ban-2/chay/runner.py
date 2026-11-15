#!/usr/bin/env python3
"""T-062 bộ chạy (laptop). Chạy: py -3 -B results/T-062/chay/runner.py d2|e1 [--lich chay/lich.json]

d2: xác nhận can thiệp (B4) từng ô trong một lượt tải riêng, ngoài chu kỳ chính.
e1: mỗi ô một chu kỳ 10/10/10 phút (nền/lỗi/hồi phục) dưới tải cố định; ca bình thường xen giữa.
    Mã ca mờ ngẫu nhiên; M1 chỉ nhận t qua request.json (stage-m1.py trên exp-obs); sổ tiêm lỗi
    results/T-062/tiem-loi/so.jsonl chỉ ghi thêm, hash nối dòng, không đi vào bộ đọc M1.
Dừng khẩn: tạo D:/RCA-overnight/STOP → tắt lỗi, dừng tải ở ranh giới gần nhất, ghi trạng thái.
Luật 21: lỗi một ô chỉ dừng ô đó; lỗi tải/hạ tầng dừng lượt; dữ liệu đã thu giữ nguyên.
"""
import datetime as dt, hashlib, json, os, queue, secrets, subprocess, sys, threading, time, traceback
from pathlib import Path

REPO = Path('D:/RCA-flashticket'); OUT = REPO / 'results/T-062'
CHAY = OUT / 'chay'; SO = OUT / 'tiem-loi/so.jsonl'; CA = OUT / 'ca'
STOP = Path('D:/RCA-overnight/STOP')
SSH = 'C:/Program Files/Git/usr/bin/ssh.exe'; SCP = 'C:/Program Files/Git/usr/bin/scp.exe'
KEYS = {'app': ('D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key', 'ubuntu@129.221.208.47'),
        'obs': ('D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key', 'ubuntu@213.35.116.128')}
KNOWN = 'D:/RCA-ext/overnight-T058/out/known_hosts'
PS_HELPER = (CHAY / 'tai-e1.ps1').as_posix()
PHASE = 600  # giây mỗi pha
LOCK = threading.Lock()

def now(): return dt.datetime.now(dt.timezone.utc)
def iso(t=None): return (t or now()).isoformat()

def log(msg, **k):
    line = json.dumps({'t': iso(), 'msg': msg, **k}, ensure_ascii=False)
    with LOCK:
        with open(CHAY / 'nhat-ky.jsonl', 'a', encoding='utf-8') as f: f.write(line + '\n')
    print(line, flush=True)

def ledger(event, **k):
    """Sổ tiêm lỗi: chỉ ghi thêm, mỗi dòng mang sha256 của dòng trước."""
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
    p = CHAY / 'trang-thai.json'
    with LOCK:
        d = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        d.update(k, heartbeat_utc=iso())
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')

def ssh(m, cmd, timeout=180, check=True):
    key, tgt = KEYS[m]
    r = subprocess.run([SSH, '-i', key, '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=15', '-o', 'ServerAliveInterval=20',
                        '-o', f'UserKnownHostsFile={KNOWN}', tgt, cmd], capture_output=True, text=True, timeout=timeout,
                       encoding='utf-8', errors='replace', stdin=subprocess.DEVNULL)
    if check and r.returncode != 0: raise RuntimeError(f'ssh {m} rc={r.returncode}: {r.stderr[-400:]}')
    return r.stdout

def ps(cmd, timeout=600):
    r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command',
                        f"$ErrorActionPreference='Stop'; $OutputEncoding=[Text.UTF8Encoding]::new($false); [Console]::OutputEncoding=[Text.UTF8Encoding]::new($false); Set-Location D:/RCA-flashticket; . '{PS_HELPER}'; {cmd}"],
                       capture_output=True, text=True, timeout=timeout, encoding='utf-8', errors='replace', stdin=subprocess.DEVNULL)
    if r.returncode != 0: raise RuntimeError(f'ps rc={r.returncode}: {(r.stdout + r.stderr)[-800:]}')
    return r.stdout

def inj(op, cell='-', seconds=None):
    cmd = f'python3 ~/inj.py {op} {cell}' + (f' --seconds {seconds}' if seconds else '')
    out = ssh('app', cmd, timeout=120)
    recs = [json.loads(l) for l in out.splitlines() if l.startswith('{')]
    return recs[-1] if recs else {}

def stopped(): return STOP.exists()

def wait_until(t_epoch, what):
    while time.time() < t_epoch:
        if stopped(): raise KeyboardInterrupt('STOP')
        time.sleep(min(5, max(0.2, t_epoch - time.time())))
        state(waiting=what, remaining_s=int(t_epoch - time.time()))

def start_load(tag, flash=False):
    if flash: out = ps(f"Start-TaiFlash -Tag {tag} -Rate 5 -FlashRate 15 -May tai")
    else: out = ps(f"Start-Tai -Seconds 1800 -Rate 5 -Tag {tag} -May tai")
    log('load started', tag=tag, flash=flash, out=out.strip()[-300:])
    time.sleep(20)   # k6 chết lúc khởi động (token/fixture hỏng) phải bị phát hiện ngay, không chạy chu kỳ rỗng
    st = ps(f"Get-Tai -Tag {tag} -May tai").replace(' ', '')
    if '"Running":true' not in st:
        raise RuntimeError('k6 không chạy sau 20 s: ' + st[-300:])

def finish_load(tag):
    for _ in range(60):
        st = ps(f"Get-Tai -Tag {tag} -May tai")
        if '"Running":false' in st.replace(' ', ''): break
        time.sleep(5)
    out = ps(f"Receive-Tai -Tag {tag} -May tai", timeout=900)
    log('load received', tag=tag, files=len(out.splitlines()))

# ---------- M1 (exp-obs) — một luồng nền xử lý tuần tự ----------
M1Q = queue.Queue()
def m1_worker():
    while True:
        job = M1Q.get()
        if job is None: return
        oid, t = job['id'], job['t']
        try:
            wait_until(t + PHASE + 150, f'M1 {oid} chờ flush')
        except KeyboardInterrupt:
            log('M1 bỏ qua do STOP', id=oid); continue
        try:
            r1 = ssh('obs', f'sudo /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/stage-m1.py --id {oid} --t {t}', timeout=900)
            r2 = ssh('obs', f'sudo -u rca /opt/flash-ticket-rca/venv/bin/python /opt/flash-ticket-rca/run-m1.py --id {oid}', timeout=1800)
            s = json.loads(r2[r2.index('{'):])
            ex = ssh('obs', f'sudo python3 /home/ubuntu/t058/safe-export.py case {oid} >/dev/null && sudo tar -czf /home/ubuntu/t062-ca-{oid}.tgz -C /opt/flash-ticket-rca cases/{oid} outputs/{oid} && sudo chmod 644 /home/ubuntu/t062-ca-{oid}.tgz && sha256sum /home/ubuntu/t062-ca-{oid}.tgz', timeout=600)
            dest = CA / oid; dest.mkdir(parents=True, exist_ok=True)
            key, tgt = KEYS['obs']
            subprocess.run([SCP, '-q', '-i', key, '-o', f'UserKnownHostsFile={KNOWN}', f'{tgt}:/home/ubuntu/t062-ca-{oid}.tgz', str(dest / f'{oid}.tgz')], check=True, timeout=900)
            local = hashlib.sha256((dest / f'{oid}.tgz').read_bytes()).hexdigest()
            if local != ex.split()[0]: raise RuntimeError('hash gói ca lệch')
            subprocess.run(['C:/Windows/System32/tar.exe', '-xf', str(dest / f'{oid}.tgz'), '-C', str(dest)], check=True)
            log('M1 xong', id=oid, status=s.get('status'), deterministic=s.get('deterministic_repeat'),
                top3=[e['entity'] for e in (s.get('entity_ranking') or [])[:3]], tgz_sha256=local)
        except Exception as e:
            log('M1 LỖI (chỉ chặn ca này)', id=oid, err=str(e)[-600:])

# ---------- D2 ----------
D2_CELLS = os.environ.get('T062_D2_CELLS', 'EVENT-DB-LAT,REDIS-BOOK,NET-GW-BOOK,HTTP5-EVENT,SLOW-BOOK,CPU-BOOK').split(',')
def run_d2():
    tag = 'd2-' + secrets.token_hex(4)
    ledger('d2-begin', tag=tag, note='B4 xác nhận can thiệp; không phải ca RCA')
    start_load(tag); t0 = time.time()
    ledger('d2-load-start', tag=tag)
    plan = []
    try:
        wait_until(t0 + 120, 'd2 nền')
        ledger('d2-probe', cell='-', phase='baseline', probe=inj('probe'))
        cur = t0 + 120
        for cell in D2_CELLS:
            s = inj('start', cell, 150); ts = time.time()
            ledger('d2-start', cell=cell, inj=s)
            wait_until(ts + 45, f'd2 {cell}'); ledger('d2-probe', cell=cell, phase='fault+45', probe=inj('probe', cell))
            wait_until(ts + 140, f'd2 {cell}'); ledger('d2-probe', cell=cell, phase='fault+140', probe=inj('probe', cell))
            wait_until(ts + 150, f'd2 {cell}')
            e = inj('stop', cell); te = time.time(); ledger('d2-stop', cell=cell, inj=e)
            plan.append({'cell': cell, 'start_epoch': ts, 'stop_epoch': te})
            wait_until(te + 30, f'd2 {cell} hồi'); ledger('d2-probe', cell=cell, phase='after+30', probe=inj('probe', cell))
            wait_until(te + 75, 'd2 khoảng nghỉ')
    except KeyboardInterrupt:
        log('STOP trong D2'); inj('cleanup'); ps(f'Stop-Tai -Tag {tag} -May tai')
    finally:
        (CHAY / f'{tag}-plan.json').write_text(json.dumps(plan, indent=1), encoding='utf-8')
        ps(f'Stop-Tai -Tag {tag} -May tai'); time.sleep(50)
        finish_load(tag); ledger('d2-end', tag=tag)
        log('D2 xong', tag=tag)

# ---------- E1 ----------
def run_e1(lich):
    items = json.loads(Path(lich).read_text(encoding='utf-8'))['chu_ky']
    threading.Thread(target=m1_worker, daemon=True).start()
    ledger('e1-begin', lich=str(lich), lich_sha256=hashlib.sha256(Path(lich).read_bytes()).hexdigest(), n=len(items))
    for i, it in enumerate(items):
        if stopped(): log('STOP trước chu kỳ', i=i); break
        cell = it['o']; oid = secrets.token_hex(4); tag = 'e1-' + oid
        state(cycle=i, of=len(items), opaque_id=oid, phase='start')
        ledger('cycle-begin', i=i, opaque_id=oid, cell=cell, load_tag=tag)
        try:
            start_load(tag, flash=(cell == 'FLASH-HEALTHY'))
        except Exception as e:
            log('LỖI khởi động tải — thử lại sau 60 s', err=str(e)[-400:]); time.sleep(60)
            try: start_load(tag, flash=(cell == 'FLASH-HEALTHY'))
            except Exception as e2:
                ledger('cycle-abort', i=i, opaque_id=oid, reason='load', err=str(e2)[-400:]); log('DỪNG LƯỢT: tải hỏng'); break
        S = time.time(); ledger('load-start', opaque_id=oid, epoch=S)
        fault_ok = None; t = None
        try:
            wait_until(S + PHASE / 2, 'nền'); ledger('probe', opaque_id=oid, phase='baseline', probe=inj('probe'))
            wait_until(S + PHASE, 'nền')
            if cell in ('BINH-THUONG',) :
                t = int(S + PHASE); ledger('normal-mark', opaque_id=oid, t=t)
            elif cell == 'FLASH-HEALTHY':
                t = int(S + PHASE); ledger('flash-ramp-start', opaque_id=oid, t=t, note='tải tăng theo lịch k6; không can thiệp hệ thống')
            else:
                try:
                    s = inj('start', cell, PHASE); t = int(dt.datetime.fromisoformat(s['t']).timestamp())
                    ledger('fault-start', opaque_id=oid, cell=cell, t=t, inj=s); fault_ok = True
                except Exception as e:
                    ledger('fault-start-failed', opaque_id=oid, cell=cell, err=str(e)[-400:]); fault_ok = False
                    t = int(S + PHASE)
            wait_until(S + PHASE + 60, 'lỗi'); ledger('probe', opaque_id=oid, phase='fault+60', probe=inj('probe', cell))
            wait_until(S + PHASE + 480, 'lỗi'); ledger('probe', opaque_id=oid, phase='fault+480', probe=inj('probe', cell))
            wait_until(S + 2 * PHASE, 'lỗi')
            if fault_ok:
                e = inj('stop', cell); ledger('fault-stop', opaque_id=oid, cell=cell, inj=e)
            if t is not None and fault_ok is not False:
                M1Q.put({'id': oid, 't': t}); ledger('m1-queued', opaque_id=oid, t=t)
            elif fault_ok is False:
                ledger('m1-skipped', opaque_id=oid, reason='can thiệp không khởi động được')
            wait_until(S + 2 * PHASE + 60, 'hồi phục'); ledger('probe', opaque_id=oid, phase='after+60', probe=inj('probe', cell))
            wait_until(S + 3 * PHASE + 5, 'hồi phục')
        except KeyboardInterrupt:
            log('STOP giữa chu kỳ', i=i); inj('cleanup'); ps(f'Stop-Tai -Tag {tag} -May tai')
            ledger('cycle-stopped', opaque_id=oid); finish_load(tag); break
        except Exception as e:
            log('LỖI chu kỳ (chỉ chặn ô này)', i=i, err=traceback.format_exc()[-800:])
            try: inj('cleanup')
            except Exception: pass
            ledger('cycle-error', opaque_id=oid, err=str(e)[-400:])
        try: finish_load(tag)
        except Exception as e: log('LỖI nhận tải', tag=tag, err=str(e)[-400:])
        ledger('cycle-end', opaque_id=oid)
    # chờ M1 các ca cuối
    M1Q.put(None)
    while any(t.name != 'MainThread' and t.is_alive() for t in threading.enumerate()):
        time.sleep(10)
    ledger('e1-end'); state(phase='XONG'); log('E1 xong')

if __name__ == '__main__':
    CHAY.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1]
    if mode == 'd2': run_d2()
    elif mode == 'e1': run_e1(sys.argv[3] if len(sys.argv) > 3 else CHAY / 'lich.json')
    else: raise SystemExit(__doc__)
