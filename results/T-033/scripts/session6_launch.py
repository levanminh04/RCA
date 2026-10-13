"""Laptop prepares exact files/ledger and transports approved EC2 jobs."""
import argparse,pathlib,json,base64,ast,datetime
from session6_control import ROOT,OPEN,sha,write,remote
STAGE=ROOT/'results/T-033/scripts/session6-002'
def charges():
 rows=[]
 for p in sorted(OPEN.glob('*.timer.json')):
  j=json.loads(p.read_text());rows.append({'source':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'charged_processing_s':j['charged_processing_s'],'basis':j['basis'],'exit_code':j['exit_code']})
 # Autonomous job timings are copied verbatim from EC2; child/unit timings are never added again.
 for p in sorted(OPEN.glob('*.processing-timer.json')):
  j=json.loads(p.read_text());rows.append({'source':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'charged_processing_s':(j['end_ns']-j['start_ns'])/1e9,'basis':j['scope'],'exit_code':j['exit_code']})
 return rows
def ledger(name):
 prior=ROOT/'results/T-033/runs/session5-approval-checkpoint-001/approved-accounting.json';j=json.loads(prior.read_text());rows=charges();s=sum(x['charged_processing_s'] for x in rows)
 assert s<14400
 doc=dict(j,status='VALID_ACCOUNTING_SNAPSHOT',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),approved_total_processing_s=28800+s,new_processing_charged_s=s,remaining_approved_s=14400-s,charges=rows,accounting_source={'path':prior.relative_to(ROOT).as_posix(),'sha256':sha(prior)},remaining_basis='approved 4h new minus summed measured full command/job processing; conservative SSH upper bounds; overlaps with launch/poll control charged separately')
 d=ROOT/'results/T-033/runs'/name;d.mkdir(exist_ok=False);write(d/'ledger.json',doc);return d/'ledger.json'
def payload(files):
 encoded={n:base64.b64encode(p.read_bytes()).decode() for n,p in files.items()}
 return "import pathlib,base64,hashlib,json\nH=pathlib.Path('/home/ubuntu/rca/T-033')\nfiles="+repr(encoded)+"\nfor rel,data in files.items():\n p=(H/rel).resolve();assert p.is_relative_to(H);p.parent.mkdir(parents=True,exist_ok=True);b=base64.b64decode(data)\n if p.exists():assert p.read_bytes()==b,'Refuse different existing file'\n else:p.open('xb').write(b)\n assert hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(b).hexdigest()\nprint(json.dumps({'status':'PASS','files':{r:{'sha256':hashlib.sha256(base64.b64decode(b)).hexdigest(),'bytes':len(base64.b64decode(b))} for r,b in files.items()}}))\n"
def main():
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['stage','launch','observe']);p.add_argument('--kind');p.add_argument('--phase');p.add_argument('--name',required=True);a=p.parse_args()
 if a.mode=='stage':
  for f in STAGE.glob('*.py'):ast.parse(f.read_text())
  files={'scripts/session6-002/'+f.name:f for f in STAGE.iterdir() if f.is_file()};code=payload(files)
 elif a.mode=='launch':
  S=json.loads((ROOT/'results/T-033/runs/checkpoint-handoff-001/artifacts/inputs/source.json').read_text());cases=[x['opaque_id'] for x in S['cases']]
  cases=cases[:1] if a.phase=='pilot' else cases[1:]
  # Require each completed pilot to have passed all stored checks before selecting rest.
  if a.phase=='rest':
   pilot=OPEN/(a.kind+'-delay-pilot-001.observation.json' if a.kind!='channel' else 'channel-pilot-001.observation.json')
   j=json.loads(pilot.read_text());assert j['control']['status']=='PASS' and j['validation']['status']=='PASS'
  lp=ledger(a.name+'--budget');cf=OPEN/(a.name+'.config.json');write(cf,{'run':a.name,'kind':a.kind,'phase':a.phase,'cases':cases})
  lrel='runs/'+lp.parent.name+'/ledger.json';crel='runs/'+a.name+'.config.json'
  code="import subprocess,os,json,pathlib\nH=pathlib.Path('/home/ubuntu/rca/T-033')\nrows=subprocess.check_output(['ps','-eo','pid,args'],text=True).splitlines()\nassert not [s for s in rows if str(H) in s and any(k in s for k in ['accounted_worker.py','/job.sh'])], 'Existing active job; refuse duplicate'\n"
  code+=payload({lrel:lp,crel:cf})
  cmd=['bash',str(pathlib.PurePosixPath('/home/ubuntu/rca/T-033/scripts/session6-002/job.sh')),a.name,crel,sha(cf),lrel,sha(lp),sha(STAGE/'pins.json')]
  code+="cmd="+repr(cmd)+"\nout=(H/'runs'/"+repr(a.name+'.nohup.out')+").open('xb');err=(H/'runs'/"+repr(a.name+'.nohup.err')+").open('xb')\np=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)\nprint(json.dumps({'status':'LAUNCHED','pid':p.pid,'command':cmd,'ledger_used_before_s':"+str(json.loads(lp.read_text())['approved_total_processing_s'])+"}))\n"
  with (ROOT/'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md').open('ab') as f:f.write(('\n- Trước launch '+a.name+': ledger '+lp.relative_to(ROOT).as_posix()+'; charged mới '+str(json.loads(lp.read_text())['new_processing_charged_s'])+' giây, hạch toán cũ 28800 giây, còn '+str(json.loads(lp.read_text())['remaining_approved_s'])+' giây. Lệnh nền '+repr(cmd)+'. Python pin; độc lập SSH; stdout/stderr/progress/PID/status/exit trong runs/'+a.name+' và '+a.name+'--control, trang-thai.txt. Không khởi lại PASS.\n').encode())
 elif a.mode=='observe':
  code=(STAGE/'observe.py').read_text().replace("RUN_NAME = None",'RUN_NAME = '+repr(a.name))
 else:raise ValueError()
 evidence_name=a.name+'-'+a.mode
 ix=1
 while (OPEN/(evidence_name+'.timer.json')).exists():
  ix+=1;evidence_name=a.name+'-'+a.mode+'-'+str(ix).zfill(3)
 (OPEN/(evidence_name+'.payload.py')).write_text(code,encoding='utf-8')
 result=remote(evidence_name,code)
 if result.returncode:raise SystemExit(result.returncode)
 if a.mode=='observe':
  j=json.loads(result.stdout);op=OPEN/(a.name+'.observation.json')
  if op.exists():op=OPEN/(evidence_name+'.observation.json')
  write(op,j)
  if j.get('processing_timer'):
   tp=OPEN/(a.name+'.processing-timer.json')
   if tp.exists():assert json.loads(tp.read_text())==j['processing_timer'],'Immutable processing timer changed'
   else:write(tp,j['processing_timer'])
if __name__=='__main__':main()
