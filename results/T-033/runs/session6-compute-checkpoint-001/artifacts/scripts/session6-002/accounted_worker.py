"""One autonomous monitored EC2 job. Stops child on approved budget/resource failure."""
import argparse,pathlib,os,json,time,sys,subprocess,datetime,traceback,resource
import psutil
from common import H,STAGE,sha,read,write,guard,load_pins

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--config-sha256',required=True);a=p.parse_args()
 config=H/a.config;assert sha(config)==a.config_sha256;c=read(config)
 name=c['run'];assert name and '/' not in name and '\\' not in name
 control=H/'runs'/(name+'--control');control.mkdir(exist_ok=False)
 began=time.perf_counter();stat={'status':'RUNNING','pid':os.getpid(),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'config':a.config,'config_sha256':a.config_sha256,'child_command':None,'max_tree_rss_bytes':0,'min_ram_available_bytes':None,'resources':{}}
 write(control/'status.json',stat);proc=None
 try:
  pins=load_pins();S=read(H/'inputs/source.json');wanted=c['cases'];assert len(wanted)==len(set(wanted)) and set(wanted)<={x['opaque_id'] for x in S['cases']}
  assert len(wanted)==1 if c['phase']=='pilot' else len(wanted)>0
  stat['resources']=guard(64*2**20)
  # Verify both staged approved guard implementations on valid accounting before pilot.
  import channel_context as channel,bocpd_delay as bd
  source_args=argparse.Namespace(source_sha256=pins['source_sha256'])
  dummy=object.__new__(bd.Description);dummy.home=H;dummy.args=source_args;dummy.source=S
  dummy.guard(0);channel.guard(H,S,None)
  write(control/'guard-valid-accounting.json',{'status':'PASS','both_guards_accept_valid_ledger':True,'ledger':os.environ['T033_PROCESSING_LEDGER_PATH'],'sha256':os.environ['T033_PROCESSING_LEDGER_SHA256']})
  from fixtures import fixtures
  write(control/'fixtures.json',fixtures(c['kind']))
  cmd=[sys.executable,'-B','-X','utf8',str(STAGE/({'nsigma':'nsigma_delay.py','bocpd':'bocpd_delay.py','channel':'channel_context.py'}[c['kind']])),'--run',name,'--cases',','.join(wanted)]
  if c['kind']=='bocpd':
   cmd+=['--source-sha256',pins['source_sha256'],'--core-first-sha256',pins['files']['runs/bocpd-first-002/manifest.json']['sha256'],'--core-rest-sha256',pins['files']['runs/bocpd-rest-001/manifest.json']['sha256'],'--first-compute-status-sha256',pins['files']['runs/nsigma-first-001/status.json']['sha256']]
  if c['kind']=='channel':cmd+=['--all']
  stat['child_command']=cmd;write(control/'status.json',stat)
  with (control/'stdout.txt').open('x') as out,(control/'stderr.txt').open('x') as err:
   proc=subprocess.Popen(cmd,stdout=out,stderr=err,start_new_session=True);stat['child_pid']=proc.pid;write(control/'status.json',stat)
   while proc.poll() is None:
    guard(64*2**20);v=psutil.virtual_memory();stat['min_ram_available_bytes']=min(stat['min_ram_available_bytes'] or v.available,v.available)
    assert v.percent<95,'RAM_STOP'
    try:
     pp=psutil.Process(proc.pid);rss=sum(x.memory_info().rss for x in [pp]+pp.children(recursive=True));stat['max_tree_rss_bytes']=max(stat['max_tree_rss_bytes'],rss)
    except psutil.NoSuchProcess:pass
    write(control/'status.json',stat);time.sleep(.25)
  stat['child_exit_code']=proc.returncode;assert proc.returncode==0,'Child failed; preserve run'
  run=H/'runs'/name;rstatus=read(run/'status.json');assert rstatus['status']=='PASS'
  assert rstatus['source_sha256']==pins['source_sha256']
  if c['kind']=='bocpd':assert set(rstatus['completed_cases'])==set(wanted)
  elif c['kind']=='nsigma':assert set(rstatus['completed_units'])=={x+'--'+d for x in wanted for d in ('nsigma','nsigma_doi_chung')}
  else:assert set(rstatus['cases'])==set(wanted)
  for n,m in read(run/'manifest.json').items():assert sha(run/n)==m['sha256'] and (run/n).stat().st_size==m['bytes']
  for rel,m in pins['files'].items():assert sha(H/rel)==m['sha256'],'Source changed'
  stat.update(status='PASS',resources=guard(),output_bytes=sum(p.stat().st_size for p in run.iterdir() if p.is_file()),source_hash_after=True)
 except BaseException as e:
  stat.update(status='STOPPED',error=type(e).__name__+': '+str(e));traceback.print_exc()
  if proc and proc.poll() is None:
   os.killpg(proc.pid,15)
   try:proc.wait(timeout=10)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,9);proc.wait()
  raise
 finally:
  stat.update(ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),supervisor_wall_s=time.perf_counter()-began,rss_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
  write(control/'status.json',stat)
  with (H/'trang-thai.txt').open('a') as f:f.write(stat['ended_utc']+' SESSION6 '+name+' '+stat['status']+'\n')
  write(control/'manifest.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in control.iterdir() if p.is_file() and p.name!='manifest.json'})
if __name__=='__main__':main()
