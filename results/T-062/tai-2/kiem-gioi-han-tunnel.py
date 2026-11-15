import datetime as dt,json,subprocess
from pathlib import Path
root=Path('/opt/flash-ticket-app/l1-vnpay/tunnel')
command=['ssh','-i',str(root/'forward-only.key'),'-o','BatchMode=yes','-o','IdentitiesOnly=yes',
    '-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(root/'tai-known-hosts'),
    '-o','ConnectTimeout=10','ubuntu@3.24.8.49','true']
r=subprocess.run(command,capture_output=True,text=True,timeout=20)
print(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'test':'Dedicated forwarding key cannot execute true',
    'exit':r.returncode,'noRemoteShell':r.returncode==1,'stdoutBytes':len(r.stdout),'stderrBytes':len(r.stderr)}))
if r.returncode!=1:raise SystemExit('Unexpected forced-command result; inspect restrictions')
