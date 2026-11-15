# -*- coding: utf-8 -*-
"""Tạo runner3.py (chạy trên exp-obs) từ runner2.py: chỉ đổi phần vận chuyển (đường dẫn, SSH, lệnh tải, đóng gói cục bộ).
Dùng: py -3 -B results/T-063/chay/tao_runner3.py"""
import ast, re

s = open('results/T-063/chay/runner2.py', encoding='utf-8').read()


def thay(cu, moi):
    global s
    assert cu in s, cu[:70]
    s = s.replace(cu, moi)


thay('"""T-063 bộ chạy bản 2 (laptop). Dùng: py -3 -B results/T-063/chay/runner2.py d2|thu [--lich results/T-063/chay/lich-2.json]',
     '"""T-063 bộ chạy bản 3 — chạy TRÊN exp-obs (Minh quyết 13/11, DECISIONS "Chạy bộ điều phối đợt thu trên exp-obs").\n'
     'Dùng (trên exp-obs, thư mục ~/rca-dieu-phoi): nohup setsid python3 -B runner3.py thu --lich lich-2.json > chay/runner3.out 2>&1 &\n'
     'Khác runner2 (laptop) CHỈ ở phần vận chuyển: M1/đóng gói chạy cục bộ, SSH tới exp-app bằng khóa ~/rca-dieu-phoi/keys,\n'
     'tải qua tai_linux.py (bản Python của chay-tai.ps1, L1), sổ/gói ca/nhật ký trong ~/rca-dieu-phoi. Logic chu kỳ, đầu dò,\n'
     'kiểm sạch, thử lại, stage lại khi M1 lỗi giữ nguyên runner2 (đã qua REVIEW T-063 R1).')
thay('Dừng khẩn: D:/RCA-overnight/STOP.', 'Dừng khẩn: ~/rca-dieu-phoi/STOP (trên exp-obs).')
thay("""REPO = Path('D:/RCA-flashticket'); OUT = REPO / 'results/T-063'
CHAY = OUT / 'chay'; SO = OUT / 'tiem-loi/so.jsonl'; CA = OUT / 'ca'
STOP = Path('D:/RCA-overnight/STOP')
SSH = 'C:/Program Files/Git/usr/bin/ssh.exe'; SCP = 'C:/Program Files/Git/usr/bin/scp.exe'
KEYS = {'app': ('D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key', 'ubuntu@129.221.208.47'),
        'obs': ('D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key', 'ubuntu@213.35.116.128')}
KNOWN = 'D:/RCA-ext/overnight-T058/out/known_hosts'
PS_HELPER = (REPO / 'results/T-062/tai-2/chay-tai.ps1').as_posix()
XUAT = OUT / 'dong-goi/xuat_bo_sung.py'""", """BASE = Path('/home/ubuntu/rca-dieu-phoi')
OUTR = Path(os.environ.get('RCA_DP_OUT', str(BASE)))  # chạy thử ngắn: RCA_DP_OUT=~/rca-dieu-phoi/thu-ngan, không lẫn sổ đợt thu
CHAY = OUTR / 'chay'; SO = OUTR / 'tiem-loi/so-thu2.jsonl'; CA = OUTR / 'ca'
STOP = BASE / 'STOP'
SSH = 'ssh'
KEYS = {'app': (str(BASE / 'keys/exp-app.key'), 'ubuntu@129.221.208.47')}
KNOWN = str(BASE / 'keys/known_hosts')
TAI = BASE / 'tai_linux.py'
XUAT = BASE / 'xuat_bo_sung.py'""")
thay("""def ssh(m, cmd, timeout=180, check=True, stdin=None):
    key, tgt = KEYS[m]""", """def ssh(m, cmd, timeout=180, check=True, stdin=None):
    if m == 'obs':  # chạy cục bộ trên exp-obs
        r = subprocess.run(['bash', '-c', cmd], capture_output=True, text=True, timeout=timeout, encoding='utf-8',
                           errors='replace', input=stdin)
        if check and r.returncode != 0: raise RuntimeError(f'local rc={r.returncode}: {r.stderr[-400:]}')
        return r.stdout
    key, tgt = KEYS[m]""")
a = s.index('def ps(cmd, timeout=600):'); b = s.index('\n\n\ndef inj(')
s = s[:a] + '''def tai(*args, timeout=900):
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
    return bool(r['state']['Running'])''' + s[b:]
a = s.index('def ps_thu_lai('); b = s.index('\n\n\ndef finish_load(')
s = s[:a] + '''def tai_thu_lai(*args, timeout=900, lan=4):
    """SSH tới máy tải có thể chập chờn → thử lại, giãn 30 s (chỉ get/receive, không start)."""
    for k in range(lan):
        try: return tai(*args, timeout=timeout)
        except Exception as e:
            if k == lan - 1: raise
            log('tai lỗi, thử lại', args=[str(x) for x in args][:2], lan=k + 1, err=str(e)[-200:]); time.sleep(30)''' + s[b:]
thay("""    extra = ' -Multiplier 3 -BuocTai 600' if flash else ''
    out = ps(f"Start-Tai -Scenario hanh-trinh -Seconds {seconds} -Tag {tag} -May tai{extra}")
    t_k6 = time.time()
    log('load started', tag=tag, flash=flash, out=out.strip()[-300:])
    time.sleep(20)
    st = ps(f"Get-Tai -Tag {tag} -May tai").replace(' ', '')
    if '"Running":true' not in st: raise RuntimeError('k6 không chạy sau 20 s: ' + st[-300:])""",
     """    extra = ['--buoc-tai', 600, '--multiplier', 3] if flash else []
    out = tai('start', '--tag', tag, '--seconds', seconds, *extra)
    t_k6 = time.time()
    log('load started', tag=tag, flash=flash, out=json.dumps(out)[-300:])
    time.sleep(20)
    st = tai_thu_lai('get', '--tag', tag)
    if not dang_chay(st): raise RuntimeError('k6 không chạy sau 20 s: ' + json.dumps(st)[-300:])""")
thay("""        if '"Running":false' in ps_thu_lai(f"Get-Tai -Tag {tag} -May tai").replace(' ', ''): break
        time.sleep(5)
    out = ps_thu_lai(f"Receive-Tai -Scenario hanh-trinh -Tag {tag} -May tai", timeout=900)
    log('load received', tag=tag, files=len(out.splitlines()))""", """        if not dang_chay(tai_thu_lai('get', '--tag', tag)): break
        time.sleep(5)
    out = tai_thu_lai('receive', '--tag', tag)
    log('load received', tag=tag, out=json.dumps(out)[-300:])""")
a = s.index('def nhan_ca(oid, t):'); b = s.index('\n\n\nM1Q = queue.Queue()')
s = s[:a] + '''def nhan_ca(oid, t):
    """Gói ghim + gói bổ sung, cục bộ trên exp-obs: ~/rca-dieu-phoi/ca/<oid>.tgz, <oid>/prometheus-bo-sung.json."""
    CA.mkdir(parents=True, exist_ok=True)
    ex = ssh('obs', f'sudo python3 /home/ubuntu/t058/safe-export.py case {oid} >/dev/null && sudo tar -czf {CA}/{oid}.tgz '
                    f'-C /opt/flash-ticket-rca cases/{oid} outputs/{oid} && sudo chown ubuntu {CA}/{oid}.tgz && sha256sum {CA}/{oid}.tgz',
             timeout=600)
    bs = ssh('obs', f'python3 {XUAT} --t {t}', timeout=900)
    (CA / oid).mkdir(parents=True, exist_ok=True)
    (CA / oid / 'prometheus-bo-sung.json').write_text(bs, encoding='utf-8')
    return ex.split()[0], hashlib.sha256(bs.encode()).hexdigest()''' + s[b:]
thay("log('STOP giữa chu kỳ', i=i); inj('cleanup'); ps(f'Stop-Tai -Tag {tag} -May tai')",
     "log('STOP giữa chu kỳ', i=i); inj('cleanup'); tai('stop', '--tag', tag)")
thay("ps(f'Stop-Tai -Tag {tag} -May tai'); time.sleep(30)", "tai('stop', '--tag', tag); time.sleep(30)")
thay("""    lich = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--lich' else CHAY / 'lich-2.json'""",
     """    lich = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--lich' else BASE / 'lich-2.json'
    (OUTR / 'tiem-loi').mkdir(parents=True, exist_ok=True)""")
thay('import datetime as dt, hashlib, json, queue,', 'import datetime as dt, hashlib, json, os, queue,')
ast.parse(s)
con = [l for l in s.splitlines() if re.search(r'\bps\(|ps_thu_lai|D:/|SCP', l)]
assert not con, con
open('results/T-063/chay/runner3.py', 'w', encoding='utf-8', newline='\n').write(s)
print('runner3 ok,', len(s.splitlines()), 'dòng')
