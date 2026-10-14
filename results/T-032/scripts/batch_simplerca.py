"""T-032 exact SimpleRCA cohort: plan after both pilots, fail-stop single child.

Reuse the first RE2 call only through its separate successful verifier audit.
Never replace the retained failed verifier check or silently skip a case.
"""
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
import replay_simplerca_v3 as r

BASE = Path('/home/ubuntu/rca/T-032')
NAMES = ('batch_simplerca.py', 'replay_simplerca_v3.py', 'audit_simplerca_output_v2.py',
         'replay_simplerca.py', 'capture_simplerca.py', 'replay_microrank.py', 'capture_microrank.py')
PILOTS = {'RE2-TT': ('dev-03d4910932', 'simplerca-re2-first-001'),
          'Nezha-OB': ('dev-14701a3bbb', 'simplerca-nezha-first-001')}

def require(condition, message):
    if not condition:
        raise r.ReplayError(message)
def scripts():
    return {name: r.sha(BASE/'scripts'/name) for name in NAMES}
def environment():
    keys = ('PYTHONHASHSEED', 'PYTHONPATH', 'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
            'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'TMPDIR', 'XDG_CACHE_HOME', 'MPLCONFIGDIR')
    return {'python': sys.version, 'env': {key: os.environ.get(key) for key in keys}}
def size(directory):
    return sum(path.stat().st_size for path in directory.rglob('*') if path.is_file())
def save_status(directory, value):
    temporary = directory/'status.tmp'
    temporary.write_text(json.dumps(value, indent=2)+'\n')
    temporary.replace(directory/'status.json')

def validate(directory, ds, oid, entry, frozen):
    check = r.read(directory/'check.json')
    require(check['status']=='PASS' and check['intermediates_eligible'] is True, 'case not verified')
    require((check['dataset'],check['method'],check['opaque_id'])==(ds,'simplerca',oid), 'identity changed')
    require(check['frozen_path']==entry['path'] and check['frozen_sha256']==entry['sha256'], 'source changed')
    require(check['compare']['pass'] and not check['differences'] and check['compare']['difference_count']==0, 'not exact')
    require(check['capture_check']['pass'], 'capture invalid')
    require(check['manifest_excludes']==['check.json'], 'manifest exclusions changed')
    require(check['artifact_manifest']==r.artifact_manifest(directory), 'case artifact bytes changed')
    require(not r.compare_records(frozen,r.read(directory/'ban-ghi-0.json')), 'saved record no longer exact')
    require(all(row['pass'] for row in r.read(directory/'source-checks.json')['checks']), 'source check failed')
    inv = r.read(directory/'invocation.json')
    for name, digest in inv['scripts'].items():
        require(name in NAMES and scripts()[name]==digest, 'case script changed')
    require(inv['python']==sys.version and inv['hashseed']=='0', 'case environment differs')
    return {'dataset':ds,'opaque_id':oid,'path':str(directory),'check_sha256':r.sha(directory/'check.json'),
            'record_sha256':r.sha(directory/'ban-ghi-0.json'),'logical_bytes':size(directory)}

def pilot(ds, entry, frozen):
    oid, name = PILOTS[ds]
    directory = BASE/'runs'/name
    monitor = r.read(BASE/'runs'/(name+'-monitor')/'status.json')
    if ds=='Nezha-OB':
        require(monitor['status']=='PASS' and monitor['exit_code']==0, 'Nezha pilot failed')
        row = validate(directory,ds,oid,entry,frozen)
        elapsed = monitor['elapsed_s']
    else:
        audit_dir = BASE/'runs/simplerca-re2-audit-001'
        audit = r.read(audit_dir/'check.json')
        audit_monitor = r.read(BASE/'runs/simplerca-re2-audit-001-monitor/status.json')
        require(audit_monitor['status']=='PASS' and audit_monitor['exit_code']==0, 'RE2 audit process failed')
        require(audit['status']=='PASS' and audit['record_exact'] and audit['capture_check']['pass']
                and audit['intermediates_eligible'] and audit['methods_executed'] is False, 'RE2 audit invalid')
        require(audit['original_run']==str(directory) and audit['frozen_path']==entry['path']
                and audit['frozen_sha256']==entry['sha256'], 'RE2 audit source binding failed')
        for relative, digest in audit['original_control_hashes'].items():
            require(r.sha(directory/relative)==digest, 'RE2 original control changed')
        require(audit['original_artifact_manifest']==r.artifact_manifest(directory), 'RE2 original artifact changed')
        require(not r.compare_records(frozen,r.read(directory/'ban-ghi-0.json')), 'RE2 record not exact')
        require(all(x['pass'] for x in audit['source_checks']), 'RE2 audit source failed')
        row = {'dataset':ds,'opaque_id':oid,'path':str(directory),'logical_bytes':size(directory),
               'audit_path':str(audit_dir),'audit_check_sha256':r.sha(audit_dir/'check.json'),
               'record_sha256':r.sha(directory/'ban-ghi-0.json'),
               'original_monitor_status':monitor['status'],
               'original_failure':'verifier dtype error; retained, successful native call reused by separate audit'}
        # Account for the original failed verifier and successful audit, not only native compute.
        elapsed = monitor['elapsed_s']+audit_monitor['elapsed_s']
    row.update(elapsed_s=elapsed,peak_rss_bytes=monitor['peak_tree_rss_bytes'])
    return row

def sources(audit):
    m24 = r.read(r.safe_source(r.M24))
    i24 = r.read(r.verify(r.I24,m24['source_hashes'][r.I24],r.M24+'#/source_hashes',audit))
    i26 = r.verified_index26(audit)
    ids = {'RE2-TT':sorted(x['opaque_id'] for x in i24['records'] if x['method']=='simplerca' and x['variant']=='native'),
           'Nezha-OB':sorted(x['opaque_id'] for x in i26['unique_records'] if x['worker_method']=='simplerca' and x['source_view']=='main')}
    rows = []
    for ds, cohort in ids.items():
        require(len(cohort)==len(set(cohort))==(30 if ds=='RE2-TT' else 22), 'cohort cardinality changed')
        for oid in cohort:
            entry,frozen,_index,_hashes = r.source_for(ds,oid,audit)
            rows.append({'dataset':ds,'opaque_id':oid,'entry':entry,'shape':frozen['input_shape'],
                         'window':frozen['window'],'source_cost':frozen['cost'],'source_status':frozen['status']})
    return rows

def prepare(out):
    audit = []
    rows = sources(audit)
    pilots = {}
    estimates = []
    for ds,(oid,_name) in PILOTS.items():
        entry,frozen,_index,_hashes = r.source_for(ds,oid,audit)
        pilots[ds] = pilot(ds,entry,frozen)
    for row in rows:
        ds,oid = row['dataset'],row['opaque_id']
        if oid==PILOTS[ds][0]:
            continue
        baseline = next(x for x in rows if x['dataset']==ds and x['opaque_id']==PILOTS[ds][0])
        shape, base_shape = row['shape'],baseline['shape']
        ratios = [1., row['source_cost']['wall_s']/max(baseline['source_cost']['wall_s'],1e-6)]
        for key,value in shape.items():
            base_value = base_shape.get(key)
            if type(value) is int and type(base_value) is int and base_value>0:
                ratios.append(value/base_value)
        factor = max(ratios)
        estimates.append({'dataset':ds,'opaque_id':oid,'factor':factor,
            'seconds':2*factor*(pilots[ds]['elapsed_s']+2),
            'new_bytes':int(2*factor*pilots[ds]['logical_bytes']),
            'peak_rss_bytes':int(2*factor*pilots[ds]['peak_rss_bytes'])})
    plan = {'status':'PREPARED_NOT_STARTED','method':'simplerca','sources':rows,'pilots':pilots,
            'scripts':scripts(),'environment':environment(),'source_checks':audit,
            'estimate':{'remaining_s':sum(x['seconds'] for x in estimates),
                'remaining_bytes':sum(x['new_bytes'] for x in estimates),
                'estimated_peak_rss_bytes':max(x['peak_rss_bytes'] for x in estimates),'cases':estimates,
                'note':'Unverified 2x allowance from observed+audit elapsed/source wall/input_shape. No scientific threshold or source timeout.'},
            'resources':{'remote_bytes':size(BASE),'available_ram_bytes':psutil.virtual_memory().available,
                         'free_disk_bytes':shutil.disk_usage(BASE).free}}
    r.dump(out/'plan.json',plan)
    print(json.dumps({'status':plan['status'],'estimate':plan['estimate'],'resources':plan['resources']}),flush=True)

def run(plan_dir,out):
    plan = r.read(plan_dir/'plan.json')
    require(plan['status']=='PREPARED_NOT_STARTED' and plan['scripts']==scripts()
            and plan['environment']==environment(),'plan environment/scripts changed')
    audit = []
    require(sources(audit)==plan['sources'],'source metadata changed')
    for ds,(oid,_name) in PILOTS.items():
        entry,frozen,_index,_hashes = r.source_for(ds,oid,audit)
        require(pilot(ds,entry,frozen)==plan['pilots'][ds],'pilot changed')
    state = {'status':'RUNNING','pid':os.getpid(),'started_utc':r.now(),
             'plan_sha256':r.sha(plan_dir/'plan.json'),'reused':plan['pilots'], 'completed':[],'active':None}
    started = time.perf_counter()
    def save():
        state['elapsed_s']=time.perf_counter()-started
        save_status(out,state)
    try:
        for expected in plan['sources']:
            ds,oid = expected['dataset'],expected['opaque_id']
            if oid==PILOTS[ds][0]:
                continue
            require(scripts()==plan['scripts'],'scripts changed midrun')
            entry,frozen,_index,_hashes = r.source_for(ds,oid,audit)
            require(entry==expected['entry'] and frozen['input_shape']==expected['shape']
                    and frozen['window']==expected['window'],'case source changed')
            directory = out/'cases'/ds/oid
            directory.parent.mkdir(parents=True,exist_ok=True)
            logs = out/'logs'/ds
            logs.mkdir(parents=True,exist_ok=True)
            state['active']={'dataset':ds,'opaque_id':oid};save()
            with (logs/(oid+'.stdout.txt')).open('x') as stdout,(logs/(oid+'.stderr.txt')).open('x') as stderr:
                child = subprocess.Popen([sys.executable,'-B','-X','utf8',str(BASE/'scripts/replay_simplerca_v3.py'),
                    'one',ds,oid,str(directory)],cwd=BASE,stdout=stdout,stderr=stderr,env=dict(os.environ))
                state['child_pid']=child.pid;save()
                code=child.wait()
            require(code==0,'worker failed; no retry/skip '+ds+'/'+oid)
            row = validate(directory,ds,oid,entry,frozen)
            state['completed'].append(row);state['active']=None;save()
            with (out/'completed-cases.jsonl').open('a') as stream:
                stream.write(json.dumps(row)+'\n')
            print('CASE_PASS',len(state['completed']),50,ds,oid,flush=True)
        state['status']='PASS';state['n_main_valid']=len(state['completed'])+2
        r.dump(out/'source-checks.json',{'checks':audit})
    except BaseException as error:
        state['status']='STOPPED';state['error']=type(error).__name__+': '+str(error)
        r.dump(out/'failure.json',{'status':state.copy(),'traceback':traceback.format_exc()})
        raise
    finally:
        save()
        r.dump(out/'manifest.json',{'files':r.artifact_manifest(out)})

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['prepare','run']);parser.add_argument('paths',nargs='+')
    args=parser.parse_args()
    require(os.name=='posix' and Path.home()==Path('/home/ubuntu'),'EC2 only')
    require(len(args.paths)==(1 if args.mode=='prepare' else 2),'wrong path count')
    out=Path(args.paths[-1]).expanduser().resolve()
    require(out.parent==(BASE/'runs').resolve(),'new output outside T032 runs')
    out.mkdir(exist_ok=False)
    if args.mode=='prepare':
        prepare(out);r.dump(out/'manifest.json',{'files':r.artifact_manifest(out)})
    else:
        plan_dir=Path(args.paths[0]).expanduser().resolve()
        require(plan_dir.parent==(BASE/'runs').resolve(),'plan outside T032 runs')
        run(plan_dir,out)
