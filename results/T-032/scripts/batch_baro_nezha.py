"""Prepare and run remaining Nezha main BARO cases, no repeated valid pilot."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback
import psutil
import batch_baro as b
import replay_baro as r

H = Path('/home/ubuntu/rca/T-032')
PILOT = H/'runs/baro-nezha-first-001'
PILOT_ID = 'dev-14701a3bbb'
NAMES = ('batch_baro_nezha.py','replay_baro.py','capture_baro.py','replay_microrank.py','capture_microrank.py')

def scripts(): return {n:r.sha(H/'scripts'/n) for n in NAMES}
def check_output(directory,oid,entry,frozen):
    check=r.read(directory/'check.json')
    b.require(check['status']=='PASS' and check['intermediates_eligible'] is True,'worker not valid')
    b.require((check['dataset'],check['method'],check['opaque_id'])==('Nezha-OB','baro',oid),'identity mismatch')
    b.require(check['frozen_path']==entry['path'] and check['frozen_sha256']==entry['sha256'],'source mismatch')
    b.require(check['compare']['pass'] and check['compare']['difference_count']==0 and not check['differences'],'not exact')
    b.require(check['capture_check']['pass'] and check['capture_check']['native_adapter_keys_exact'],'capture failed')
    b.require(check['manifest_excludes']==['check.json'],'unexpected manifest exclusion')
    b.require(r.artifact_manifest(directory)==check['artifact_manifest'],'artifact bytes changed')
    b.require(not r.compare_records(frozen,r.read(directory/'ban-ghi-0.json')),'frozen comparison changed')
    b.require(all(x['pass'] for x in r.read(directory/'source-checks.json')['checks']),'source check failed')
    invocation=r.read(directory/'invocation.json')
    for name in NAMES[1:]: b.require(invocation['scripts'][name]==scripts()[name],'wrapper changed since pilot')
    b.require(invocation['python']==sys.version and invocation['hashseed']=='0','environment differs')
    n=sum(p.stat().st_size for p in directory.rglob('*') if p.is_file())
    return {'opaque_id':oid,'status':'PASS','check_path':str(directory/'check.json'),'check_sha256':r.sha(directory/'check.json'),
            'artifact_manifest_sha256':b.json_hash(check['artifact_manifest']),'logical_bytes':n,'n_artifacts':len(check['artifact_manifest'])}

def source(oid,audit):
    entry,frozen,index,hashes=r.source_for('Nezha-OB',oid,audit)
    return entry,frozen

def prepare(out):
    audit=[]
    index=r.verified_index26(audit)
    ids=sorted(x['opaque_id'] for x in index['unique_records'] if x['worker_method']=='baro' and x['source_view']=='main')
    b.require(len(set(ids))==len(ids)==22 and ids[0]==PILOT_ID,'main cohort differs')
    entries=[]
    for oid in ids:
        entry,frozen=source(oid,audit)
        entries.append({'opaque_id':oid,'entry':entry,'shape':frozen['input_shape'],'window':frozen['window'],'cost':frozen['cost']})
    entry,frozen=source(PILOT_ID,audit)
    verified=check_output(PILOT,PILOT_ID,entry,frozen)
    monitor=r.read(H/'runs/baro-nezha-first-001-monitor/status.json')
    b.require(monitor['status']=='PASS' and monitor['exit_code']==0,'pilot monitor failed')
    row0=next(x for x in entries if x['opaque_id']==PILOT_ID)
    basecols=row0['shape']['metric_cols']; basetime=row0['cost']['wall_s']
    estimated=[]
    for x in entries:
        if x['opaque_id']==PILOT_ID: continue
        factor=max(1.,x['shape']['metric_cols']/basecols,x['cost']['wall_s']/basetime)
        estimated.append({'opaque_id':x['opaque_id'],'factor':factor,
                          'seconds':2*factor*(monitor['elapsed_s']+2),
                          'new_bytes':int(2*factor*verified['logical_bytes'])})
    plan={'status':'PREPARED_NOT_STARTED','dataset':'Nezha-OB','method':'baro','pilot':verified,'main_ids':ids,
          'remaining_ids':[oid for oid in ids if oid!=PILOT_ID],'sources':entries,'scripts':scripts(),'environment':b.environment(),
          'estimate':{'remaining_s':sum(x['seconds'] for x in estimated),'remaining_bytes':sum(x['new_bytes'] for x in estimated),
                      'estimated_peak_rss_bytes':int(2*max(x['factor'] for x in estimated)*monitor['peak_tree_rss_bytes']),
                      'cases':estimated,'note':'2x pilot/source cost/columns allowance; unverified estimate, no detector threshold/timeout'},
          'resources':{'remote_bytes':sum(p.stat().st_size for p in H.rglob('*') if p.is_file()),
                       'available_ram_bytes':psutil.virtual_memory().available,'free_disk_bytes':shutil.disk_usage(H).free}}
    r.dump(out/'source-checks.json',{'checks':audit})
    r.dump(out/'plan.json',plan)
    print(json.dumps({'status':plan['status'],'estimate':plan['estimate'],'resources':plan['resources']}),flush=True)

def run(plan_dir,out):
    plan=r.read(plan_dir/'plan.json')
    b.require(plan['status']=='PREPARED_NOT_STARTED' and plan['scripts']==scripts() and plan['environment']==b.environment(),'plan changed')
    rows=[]; audit=[]; start=time.perf_counter()
    status={'status':'RUNNING','pid':os.getpid(),'plan_sha256':r.sha(plan_dir/'plan.json'),'completed_ids':[],
            'reused_ids':[PILOT_ID],'active_id':None,'started_utc':r.now()}
    def save():
        status['elapsed_s']=time.perf_counter()-start
        (out/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    try:
        entry,frozen=source(PILOT_ID,audit); check_output(PILOT,PILOT_ID,entry,frozen)
        for oid in plan['remaining_ids']:
            b.require(scripts()==plan['scripts'],'wrapper changed midrun')
            entry,frozen=source(oid,audit)
            expected=next(x for x in plan['sources'] if x['opaque_id']==oid)
            b.require(expected['entry']==entry and expected['shape']==frozen['input_shape'] and expected['window']==frozen['window'],'source changed')
            directory=out/'cases'/oid
            directory.parent.mkdir(exist_ok=True)
            (out/'logs').mkdir(exist_ok=True)
            status['active_id']=oid; save()
            with (out/'logs'/(oid+'.stdout.txt')).open('x') as stdout, (out/'logs'/(oid+'.stderr.txt')).open('x') as stderr:
                child=subprocess.Popen([sys.executable,'-B','-X','utf8',str(H/'scripts/replay_baro.py'),
                                        'one','Nezha-OB',oid,str(directory)],cwd=H,stdout=stdout,stderr=stderr,env=dict(os.environ))
                status['child_pid']=child.pid; save()
                code=child.wait()
            b.require(code==0,'worker failed; no retry or skip '+oid)
            row=check_output(directory,oid,entry,frozen)
            rows.append(row); status['completed_ids'].append(oid); status['active_id']=None; save()
            with (out/'completed-cases.jsonl').open('a') as f: f.write(json.dumps(row)+'\n')
            print('CASE_PASS',len(rows),len(plan['remaining_ids']),oid,flush=True)
        r.dump(out/'source-checks.json',{'checks':audit})
        status['status']='PASS'; status['n_main_valid']=len(rows)+1
    except BaseException as exc:
        status['status']='STOPPED'; status['error']=type(exc).__name__+': '+str(exc)
        r.dump(out/'failure.json',status.copy()); traceback.print_exc(); raise
    finally:
        save(); r.dump(out/'manifest.json',{'files':r.artifact_manifest(out)})

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('mode',choices=['prepare','run']); p.add_argument('paths',nargs='+'); a=p.parse_args()
    if a.mode=='prepare':
        assert len(a.paths)==1; out=b.new_run(a.paths[0]); prepare(out); r.dump(out/'manifest.json',{'files':r.artifact_manifest(out)})
    else:
        assert len(a.paths)==2; run(b.inside_run(a.paths[0]),b.new_run(a.paths[1]))
