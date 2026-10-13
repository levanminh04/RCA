"""Stream new EC2 artifacts to laptop, without creating an EC2 archive or deleting files."""
import pathlib,json,subprocess,time,tarfile,hashlib,datetime,sys
from session6_control import ROOT,OPEN,SSH,remote,sha,write,stamp
RUNS=['nsigma-delay-pilot-001','nsigma-delay-rest-001','bocpd-delay-pilot-001','bocpd-delay-rest-001','channel-pilot-001','channel-rest-001']
DEST=ROOT/'results/T-033/runs/session6-compute-checkpoint-001'
DEST.mkdir(exist_ok=False)
roots=['scripts/session6-001','scripts/session6-002','scripts/session6-groups-001','inputs/session6-groups-001','runs/session6-groups-001','runs/session6-groups-budget-001']
for n in RUNS:roots += ['runs/'+n,'runs/'+n+'--control','runs/'+n+'--budget']
code="import pathlib,json,hashlib,subprocess\nH=pathlib.Path('/home/ubuntu/rca/T-033')\nroots="+repr(roots)+"\nnames="+repr(RUNS)+"\nfiles=[]\nfor r in roots:\n p=H/r;assert p.is_dir();files += [x for x in p.rglob('*') if x.is_file()]\nfor n in names:\n files += [x for x in (H/'runs').glob(n+'.*') if x.is_file()]\nfiles += [H/'trang-thai.txt']\nrows={}\nfor p in sorted(set(files)):\n h=hashlib.sha256()\n with p.open('rb') as f:\n  for b in iter(lambda:f.read(1<<20),b''):h.update(b)\n rows[p.relative_to(H).as_posix()]={'sha256':h.hexdigest(),'bytes':p.stat().st_size}\nps=subprocess.check_output(['ps','-eo','pid,args'],text=True).splitlines()\nworkers=[s for s in ps if str(H) in s and ('accounted_worker.py' in s or '/job.sh' in s)]\nassert not workers\nprint(json.dumps({'status':'PASS','files':rows,'worker_candidates':workers,'logical_bytes':sum(x.stat().st_size for x in H.rglob('*') if x.is_file())}))\n"
p=remote('receive-inventory-001',code);assert p.returncode==0
j=json.loads(p.stdout);write(DEST/'artifact-inventory.json',j)
files=j['files'];target=DEST/'artifacts';target.mkdir()
cmd=SSH+['tar -C /home/ubuntu/rca/T-033 -cf - '+' '.join(files)]
begin=time.perf_counter();started=stamp();proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
received={}
try:
 with tarfile.open(fileobj=proc.stdout,mode='r|') as archive:
  for member in archive:
   assert member.isfile() and member.name in files,member.name
   assert member.name not in received
   q=(target/member.name).resolve();assert q.is_relative_to(target.resolve())
   q.parent.mkdir(parents=True,exist_ok=True);h=hashlib.sha256();total=0
   src=archive.extractfile(member)
   with q.open('xb') as f:
    for b in iter(lambda:src.read(1<<20),b''):f.write(b);h.update(b);total+=len(b)
   m={'sha256':h.hexdigest(),'bytes':total};assert m==files[member.name],member.name;received[member.name]=m
 proc.stdout.close();err=proc.stderr.read();rc=proc.wait();assert rc==0,err.decode(errors='replace')
 assert received==files
 write(DEST/'receive-verification.json',{'status':'PASS','files':len(received),'bytes':sum(x['bytes'] for x in received.values()),'two_end_hashes_verified':True,'stream_without_ec2_archive':True,'no_files_deleted':True})
 print('PASS received',len(received),'files',sum(x['bytes'] for x in received.values()),'bytes')
finally:
 elapsed=time.perf_counter()-begin
 write(OPEN/'receive-stream-001.timer.json',{'started':started,'ended':stamp(),'charged_processing_s':elapsed,'basis':'full SSH tar stream elapsed upper bound including laptop receive/hash/IO/network; no separate child timer charged','exit_code':proc.returncode,'command':cmd})
