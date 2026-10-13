"""Timed, pinned receive of public RE2 dev saved evidence, no archive/deletion."""
import pathlib,json,subprocess,time,tarfile,hashlib
from session9_control import ROOT,OPEN,SSH,sha,write,stamp,read
DEST=ROOT/'results/T-033/runs/session9-manual-receive-001';DEST.mkdir(exist_ok=False)
j=read(OPEN/'session9-manual-001.stdout');assert j['status']=='PASS'
files={'runs/session9-manual-001/'+k:v for k,v in j['files'].items()}
write(DEST/'artifact-inventory.json',{'status':'PASS','files':files,'source':str((OPEN/'session9-manual-001.stdout').relative_to(ROOT))})
target=DEST/'artifacts';target.mkdir()
base=ROOT/'results/T-033/runs/session8-compute-evidence-checkpoint-001/ledger.json';ledger=read(base)
charges=[{'source':str(p.relative_to(ROOT)),'sha256':sha(p),'charged_processing_s':read(p)['charged_processing_s'],'basis':read(p)['basis'],'exit_code':read(p)['exit_code']} for p in sorted(OPEN.glob('*.timer.json'))]
ledger['charges']+=charges;ledger['new_processing_charged_s']+=sum(v['charged_processing_s'] for v in charges)
ledger['remaining_approved_s']=ledger['approved_max_new_processing_s']-ledger['new_processing_charged_s'];assert ledger['remaining_approved_s']>0
ledger['approved_total_processing_s']=ledger['approved_prior_processing_s']+ledger['new_processing_charged_s'];ledger['previous_snapshot']={'path':str(base.relative_to(ROOT)),'sha256':sha(base)};ledger['at']=stamp()
write(DEST/'stream-ledger.json',ledger)
assert all(v.startswith('runs/session9-manual-001/') and ' ' not in v and '..' not in v for v in files)
cmd=SSH+['tar -C /home/ubuntu/rca/T-033 -cf - '+' '.join(files)]
begin=time.perf_counter();started=stamp();proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);received={}
try:
 with tarfile.open(fileobj=proc.stdout,mode='r|') as archive:
  for member in archive:
   assert time.perf_counter()-begin<ledger['remaining_approved_s']
   assert member.isfile() and member.name in files and member.name not in received
   q=(target/member.name).resolve();assert q.is_relative_to(target.resolve());q.parent.mkdir(parents=True,exist_ok=True)
   h=hashlib.sha256();total=0;src=archive.extractfile(member)
   with q.open('xb') as f:
    for b in iter(lambda:src.read(1<<20),b''):f.write(b);h.update(b);total+=len(b)
   m={'sha256':h.hexdigest(),'bytes':total};assert m==files[member.name],member.name;received[member.name]=m
 proc.stdout.close();err=proc.stderr.read();rc=proc.wait();assert rc==0,err.decode(errors='replace');assert received==files
 write(DEST/'receive-verification.json',{'status':'PASS','files':len(received),'bytes':sum(x['bytes'] for x in received.values()),'two_end_hashes_verified':True,'stream_without_ec2_archive':True})
 print('PASS received',len(received),'files',sum(x['bytes'] for x in received.values()),'bytes')
finally:
 elapsed=time.perf_counter()-begin
 write(OPEN/'session9-receive-stream-001.timer.json',{'started':started,'ended':stamp(),'charged_processing_s':elapsed,'basis':'full SSH tar stream elapsed conservative bound including local hash/IO/network','exit_code':proc.returncode,'command':cmd,'ledger_sha256':sha(DEST/'stream-ledger.json')})
