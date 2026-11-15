"""Install or inspect L1 reverse forwarding without touching existing SSH credentials."""
import base64,datetime as dt,hashlib,json,os,subprocess,time
from pathlib import Path
root=Path('/opt/flash-ticket-app/l1-vnpay/tunnel')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
if ACTION=='prepare':
    os.umask(0o077);root.mkdir(mode=0o700,parents=True,exist_ok=True)
    key=root/'forward-only.key'
    if not key.exists():
        subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-C','l1-mock-forward-only','-f',str(key)],check=True,capture_output=True)
    source=base64.b64decode(SOURCE_B64);known=base64.b64decode(KNOWN_B64)
    before={n:digest(root/n) for n in ['tunnel-supervisor.py','tai-known-hosts']}
    (root/'tunnel-supervisor.py').write_bytes(source);(root/'tai-known-hosts').write_bytes(known)
    print(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'publicKey':(key.with_suffix('.key.pub')).read_text().strip(),
        'before':before,'after':{n:digest(root/n) for n in before},
        'privateKeyStoredOnlyOn':'exp-app:/opt/flash-ticket-app/l1-vnpay/tunnel/forward-only.key'}))
elif ACTION in ['status','start']:
    pidpath=root/'supervisor.pid'
    pid=int(pidpath.read_text().strip()) if pidpath.exists() else None
    alive=False
    if pid:
        try:alive=str(root/'tunnel-supervisor.py').encode() in Path(f'/proc/{pid}/cmdline').read_bytes()
        except (FileNotFoundError,PermissionError):pass
    restarted=False
    if ACTION=='start' and not alive:
        for name in ['tunnel-supervisor.py','forward-only.key','tai-known-hosts']:
            if not (root/name).exists():raise SystemExit('Tunnel not provisioned')
        with (root/'supervisor.stderr.log').open('ab',buffering=0) as log:
            p=subprocess.Popen(['python3',str(root/'tunnel-supervisor.py')],cwd=root,
                stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
        time.sleep(1);pid=p.pid;alive=p.poll() is None;restarted=True
    sshpid=int((root/'ssh.pid').read_text().strip()) if (root/'ssh.pid').exists() else None
    parent=int(Path(f'/proc/{pid}/stat').read_text().split()[3]) if alive else None
    session=os.getsid(pid) if alive else None
    print(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'supervisorPid':pid,'supervisorParentPid':parent,'supervisorSessionId':session,'alive':alive,'sshPid':sshpid,
        'startedNow':restarted,'launcher':'remote Python start_new_session; SSH supervised on exp-app',
        'events':str(root/'events.jsonl')}))
    if ACTION=='start' and not alive:raise SystemExit(2)
