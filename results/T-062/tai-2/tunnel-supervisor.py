"""Own one loopback reverse forward; detached from laptop/Codex. No shell login."""
import datetime as dt,json,os,signal,subprocess,time
from pathlib import Path
root=Path(__file__).resolve().parent
command=['ssh','-N','-T','-i',str(root/'forward-only.key'),'-o','BatchMode=yes',
    '-o','IdentitiesOnly=yes','-o','StrictHostKeyChecking=yes',
    '-o','UserKnownHostsFile='+str(root/'tai-known-hosts'),
    '-o','ExitOnForwardFailure=yes','-o','ServerAliveInterval=20','-o','ServerAliveCountMax=3',
    '-o','ConnectTimeout=15','-R','127.0.0.1:19091:127.0.0.1:19090','ubuntu@3.24.8.49']
def event(kind,**details):
    with (root/'events.jsonl').open('a') as f:
        f.write(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'event':kind,**details})+'\n')
def main():
    os.umask(0o077)
    import fcntl
    lock=(root/'supervisor.lock').open('a')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise SystemExit('Supervisor already running')
    child=None;stopping=False
    def stop(*_):
        nonlocal stopping
        stopping=True
        if child and child.poll() is None:child.terminate()
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    (root/'supervisor.pid').write_text(str(os.getpid())+'\n')
    event('supervisor_started',pid=os.getpid(),ppid=os.getppid())
    consecutive_failures=0
    with (root/'ssh.stderr.log').open('ab',buffering=0) as output:
        while not stopping:
            launched=time.monotonic()
            child=subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=output)
            (root/'ssh.pid').write_text(str(child.pid)+'\n')
            event('ssh_started',pid=child.pid)
            result=child.wait()
            event('ssh_exited',pid=child.pid,exit=result)
            consecutive_failures=consecutive_failures+1 if time.monotonic()-launched<10 else 0
            if consecutive_failures>=3:
                event('reconnect_exhausted',consecutiveFastFailures=consecutive_failures)
                raise SystemExit(2)
            if not stopping:time.sleep(5)
    event('supervisor_stopped')
if __name__=='__main__':main()
