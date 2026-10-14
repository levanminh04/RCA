$ErrorActionPreference='Stop'
Set-Location D:/RCA-flashticket
$where='results/T-032/runs/research-baro-transfer-001'
$inv=Get-Content -LiteralPath "$where/inventory.json" -Raw | ConvertFrom-Json
$key=@('-i','D:/RCA-ext/keys/key2.pem','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes')
if((Get-FileHash -LiteralPath $inv.archive.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $inv.archive.sha256){throw 'archive changed'}
$invHash=(Get-FileHash -LiteralPath "$where/inventory.json" -Algorithm SHA256).Hash.ToLowerInvariant()
& ssh @key ubuntu@3.26.62.217 'test ! -e /home/ubuntu/rca/T-032/inputs/research-baro-transfer-001.tar.gz && test ! -e /home/ubuntu/rca/T-032/inputs/research-baro-transfer-001.json'
if($LASTEXITCODE -ne 0){throw 'destination exists'}
& scp @key $inv.archive.path ubuntu@3.26.62.217:/home/ubuntu/rca/T-032/inputs/research-baro-transfer-001.tar.gz
if($LASTEXITCODE -ne 0){throw 'archive transfer failed'}
& scp @key "$where/inventory.json" ubuntu@3.26.62.217:/home/ubuntu/rca/T-032/inputs/research-baro-transfer-001.json
if($LASTEXITCODE -ne 0){throw 'inventory transfer failed'}
$s=@'
import os,sys,json,hashlib,tarfile,psutil,shutil,subprocess,time
from pathlib import Path,PurePosixPath
b=Path('/home/ubuntu/rca/T-032')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
i=b/'inputs/research-baro-transfer-001.json';assert sha(i)==sys.argv[1]
inv=json.loads(i.read_text());a=b/'inputs/research-baro-transfer-001.tar.gz';assert sha(a)==inv['archive']['sha256']
rows={r['relative']:r for r in inv['files']};assert len(rows)==9
with tarfile.open(a,'r:gz') as tf:
 ms=tf.getmembers();assert len(ms)==len(rows) and {m.name for m in ms}==set(rows)
 for m in ms:
  p=PurePosixPath(m.name);assert m.isfile() and not p.is_absolute() and '..' not in p.parts
  assert m.name.startswith('repo/results/T-032/') or m.name in ['sources/research-baro-004-plan.json','scripts/research_baro_chain_v1.py']
  dst=b/m.name;assert dst.resolve()==dst and not dst.is_symlink()
  data=tf.extractfile(m).read();r=rows[m.name];assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
  if dst.exists():assert sha(dst)==r['sha256'],'existing source differs'
 for m in ms:
  dst=b/m.name
  if not dst.exists():
   dst.parent.mkdir(parents=True,exist_ok=True)
   with dst.open('xb') as f:f.write(tf.extractfile(m).read())
checks=[]
for rel,r in rows.items():
 p=b/rel;assert sha(p)==r['sha256'];checks.append({'remote':str(p),'local_source':r['local'],'bytes':p.stat().st_size,'sha256':sha(p),'pass':True})
for proc in psutil.process_iter(['pid','cmdline']):
 try:
  argv=proc.info['cmdline'] or [];assert proc.pid==os.getpid() or not any(str(b) in x and x.endswith('.py') for x in argv),'T032 process active'
 except (psutil.NoSuchProcess,psutil.AccessDenied):pass
n=sum((Path(par)/f).stat().st_size for par,ds,fs in os.walk(b) for f in fs if not (Path(par)/f).is_symlink())
assert n+1100000000+100*2**20<8*2**30 and psutil.virtual_memory().available>2*2**30
print(json.dumps({'status':'TRANSFER_AND_PREFLIGHT_PASS','files':checks,'remote_bytes':n,'local_reserve_bytes':1100000000,'available_ram_bytes':psutil.virtual_memory().available,'free_disk_bytes':shutil.disk_usage(b).free,'at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}),flush=True)
p=b/'sources/research-baro-004-plan.json'
r=subprocess.run(['bash',str(b/'scripts/start_script.sh'),'research-baro-004','1100000000','1200','research_baro_chain_v1.py','--plan',str(p),'--plan-sha256',inv['plan_sha256'],'--out',str(b/'runs/execution-research-baro-004')],check=True,capture_output=True,text=True)
print(r.stdout,flush=True)
'@
$out=$s | & ssh @key ubuntu@3.26.62.217 "/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 - $invHash"
if($LASTEXITCODE -ne 0){throw 'research transfer/launch failed; preserve outputs'}
[IO.File]::WriteAllText((Join-Path (Get-Location) "$where/transfer-launch.txt"),($out -join "`n"),[Text.UTF8Encoding]::new($false))
$out
