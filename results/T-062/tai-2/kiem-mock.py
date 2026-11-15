"""Inspect/recover only the existing L1 mock. State/audit and configuration stay intact."""
import datetime as dt,hashlib,json,os,subprocess,time,urllib.request
from pathlib import Path
root=Path('/opt/flash-ticket-app/l1-vnpay')
pidfile=root/'pid'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
before={n:digest(root/n) for n in ['mock-runner.py','mock_vnpay.py','mock.env','pid','state.json']}
pid=int(pidfile.read_text().strip()) if pidfile.exists() else None
alive=False
if pid:
    try:
        cmdline=Path(f'/proc/{pid}/cmdline').read_bytes()
        alive=str(root/'mock-runner.py').encode() in cmdline
    except (FileNotFoundError,PermissionError):pass
def healthy():
    try:
        with urllib.request.urlopen('http://127.0.0.1:19090/health',timeout=3) as r:
            return r.code==200 and json.load(r).get('status')=='UP'
    except OSError:return False
health=healthy();restarted=False
if RECOVER and not alive:
    if health:raise SystemExit('Mock PID invalid but port is healthy; do not replace an unknown listener')
    for n in ['mock-runner.py','mock_vnpay.py','mock.env']:
        if not (root/n).exists():raise SystemExit('Existing mock installation missing; no config fabricated')
    os.umask(0o077)
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    logpath=root/('process-recovery-'+stamp+'.log')
    with logpath.open('ab',buffering=0) as log:
        process=subprocess.Popen(['python3',str(root/'mock-runner.py')],cwd=root,
            env={**os.environ,'FT_TEST_ENVIRONMENT':'true'},stdout=log,stderr=log,start_new_session=True)
    pid=process.pid;pidfile.write_text(str(pid)+'\n');os.chmod(pidfile,0o600)
    for _ in range(3):
        time.sleep(1)
        if healthy():break
    alive=process.poll() is None;health=healthy();restarted=True
    (root/('recovery-'+stamp+'.json')).write_text(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'pid':pid,'log':str(logpath),'reason':'recorded mock process absent','before':before}))
after={n:digest(root/n) for n in before}
print(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'pid':pid,'alive':alive,'health200':health,
    'restarted':restarted,'before':before,'after':after}))
if not alive or not health:raise SystemExit(2)
