"""Root takeover transport after subagent capacity interruption; additive logs."""
import pathlib,subprocess,time,json,sys
OUT=pathlib.Path(__file__).parent
SSH=['ssh','-i','D:/RCA-ext/keys/keys.pem','-o','UserKnownHostsFile=D:/RCA-flashticket/results/T-033/runs/prepare-001/known_hosts','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=20','ubuntu@3.107.246.249']
script=sys.stdin.read().replace('\r\n','\n').replace('\r','\n');name=sys.argv[1];start=time.time();r=subprocess.run(SSH+['bash -s'],input=script.encode('utf-8'),capture_output=True)
for token,data in [('stdout',r.stdout),('stderr',r.stderr)]:
 p=OUT/(name+'-'+token+'.txt');assert not p.exists();p.write_bytes(data)
with (OUT/'root-t33-commands.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'name':name,'command':SSH+['bash -s'],'stdin':script,'exit_code':r.returncode,'wall_s':time.time()-start},ensure_ascii=False)+'\n')
print(json.dumps({'name':name,'exit_code':r.returncode,'wall_s':time.time()-start,'stdout':r.stdout.decode(errors='replace')[-3000:],'stderr':r.stderr.decode(errors='replace')[-500:]},ensure_ascii=False),flush=True)
if r.returncode:raise RuntimeError('remote failed, attempt preserved')
