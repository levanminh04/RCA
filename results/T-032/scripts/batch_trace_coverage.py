"""Plan/run trace interval audit, reusing verified pilots and preserving failures."""
import argparse
import gc
import json
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
import psutil
import trace_coverage as c

BASE = c.BASE
PILOTS = {'RE2-TT': ('trace-coverage-re2-first-001', 'dev-03d4910932'),
          'Nezha-OB': ('trace-coverage-nezha-first-001', 'dev-14701a3bbb')}
NAMES = ('batch_trace_coverage.py', 'trace_coverage.py')
def require(ok, reason):
    if not ok:
        raise ValueError(reason)
def scripts():
    return {n: c.sha(BASE/'scripts'/n) for n in NAMES}
def env():
    return {'python': sys.version, 'hashseed': os.environ.get('PYTHONHASHSEED')}
def pilot(dataset):
    name, oid = PILOTS[dataset]
    directory = BASE/'runs'/name
    manifest = c.read(directory/'manifest.json')
    monitor = c.read(BASE/'runs'/(name+'-monitor')/'status.json')
    require(monitor['status']=='PASS' and monitor['exit_code']==0, 'pilot monitor not PASS')
    require(manifest['status']=='PASS_OBSERVATION_AUDIT_ONLY' and len(manifest['outputs'])==1, 'pilot incomplete')
    require(manifest['script_sha256']==scripts()['trace_coverage.py'], 'pilot script changed')
    row = manifest['outputs'][0]
    require(row['path']==dataset+'-'+oid+'.json', 'pilot output identity changed')
    path = directory/row['path']
    require(path.stat().st_size==row['bytes'] and c.sha(path)==row['sha256'], 'pilot output bytes changed')
    value = c.read(path)
    require(value['dataset']==dataset and value['opaque_id']==oid, 'pilot metadata changed')
    require(all(x['passed'] for x in value['frozen_method_facing_count_checks'].values()), 'pilot F counts invalid')
    return {'dataset': dataset, 'opaque_id': oid, 'path': str(path), 'sha256': row['sha256'],
            'bytes': row['bytes'], 'manifest_sha256': c.sha(directory/'manifest.json'),
            'monitor_sha256': c.sha(BASE/'runs'/(name+'-monitor')/'status.json'),
            'elapsed_s': monitor['elapsed_s'], 'peak_rss_bytes': monitor['peak_tree_rss_bytes'],
            'source_trace_bytes': sum(x['bytes'] for x in manifest['inputs'] if '/data/' in x.get('absolute_path','')),
            'frozen_F_rows': sum(x['actual'] for k,x in value['frozen_method_facing_count_checks'].items() if k.endswith('_start'))}
def inventory(reader):
    allows, refs, aliases = c.preparation(reader)
    items=[]
    for ds in ('RE2-TT','Nezha-OB'):
        require(len(allows[ds]['cases'])==(30 if ds=='RE2-TT' else 22), 'allowlist cardinality changed')
        for case in sorted(allows[ds]['cases'],key=lambda x:x['opaque_id']):
            marker, source, counts, count_source = c.case_marker(reader,ds,case,refs[ds])
            trace_bytes=sum(x['bytes'] for key,x in case['files'].items() if x is not None and
                            (key=='traces.parquet' if ds=='RE2-TT' else '/trace/' in x['path']))
            items.append({'dataset':ds,'opaque_id':case['opaque_id'],'case':case,
                          'marker_source':source,'count_source':count_source,
                          'frozen_F_rows':sum(v for k,v in counts.items() if k.endswith('_start')),
                          'source_trace_bytes':trace_bytes})
    return allows,refs,aliases,items
def prepare(out):
    reader=c.Sources()
    _allows,_refs,_aliases,items=inventory(reader)
    pilots={ds:pilot(ds) for ds in PILOTS}
    estimates=[]
    for item in items:
        ds,oid=item['dataset'],item['opaque_id']
        anchor=pilots[ds]
        if oid==anchor['opaque_id']:
            require(item['source_trace_bytes']==anchor['source_trace_bytes'] and item['frozen_F_rows']==anchor['frozen_F_rows'], 'pilot inputs changed')
            continue
        factor=max(1., item['source_trace_bytes']/anchor['source_trace_bytes'],
                   item['frozen_F_rows']/max(anchor['frozen_F_rows'],1))
        estimates.append({'dataset':ds,'opaque_id':oid,'factor':factor,
                          'seconds':2*factor*(anchor['elapsed_s']+1),
                          'new_bytes':int(2*factor*anchor['bytes']),
                          'peak_rss_bytes':int(2*factor*anchor['peak_rss_bytes'])})
    resources={'remote_bytes':sum(p.stat().st_size for p in BASE.rglob('*') if p.is_file()),
               'available_ram_bytes':psutil.virtual_memory().available,'free_disk_bytes':shutil.disk_usage(BASE).free}
    estimate={'remaining_s':sum(x['seconds'] for x in estimates),
              'remaining_bytes':sum(x['new_bytes'] for x in estimates),
              'estimated_peak_rss_bytes':max(x['peak_rss_bytes'] for x in estimates),
              'cases':estimates,'note':'Unverified 2x allowance from measured pilot, compressed source bytes and F rows. No physical timing or scientific threshold inferred.'}
    plan={'status':'PREPARED_NOT_STARTED','sources':items,'pilots':pilots,'scripts':scripts(),
          'environment':env(),'estimate':estimate,'resources':resources,'source_checks':reader.inputs}
    c.write(out/'plan.json',plan)
    print(json.dumps({'status':plan['status'],'estimate':estimate,'resources':resources}),flush=True)
def run(plan_dir,out):
    plan=c.read(plan_dir/'plan.json')
    require(plan['status']=='PREPARED_NOT_STARTED' and plan['scripts']==scripts() and plan['environment']==env(),'plan changed')
    reader=c.Sources()
    allows,refs,aliases,items=inventory(reader)
    require(items==plan['sources'],'source metadata changed after plan')
    require({ds:pilot(ds) for ds in PILOTS}==plan['pilots'],'pilot changed after plan')
    outputs=[]
    started=time.perf_counter()
    state={'status':'RUNNING','pid':os.getpid(),'started_utc':c.datetime.now(c.timezone.utc).isoformat(),
           'plan_sha256':c.sha(plan_dir/'plan.json'),'completed':[],'reused':list(plan['pilots'].values()),'active':None}
    def save():
        state['elapsed_s']=time.perf_counter()-started
        temp=out/'status.tmp'
        temp.write_text(json.dumps(state,indent=2)+'\n')
        temp.replace(out/'status.json')
    try:
        for item in items:
            ds,oid=item['dataset'],item['opaque_id']
            if oid==plan['pilots'][ds]['opaque_id']:
                continue
            require(scripts()==plan['scripts'],'wrapper changed midrun')
            state['active']={'dataset':ds,'opaque_id':oid};save()
            row=c.audit_case(reader,ds,item['case'],refs[ds],aliases,out)
            outputs.append(row)
            state['completed'].append({'dataset':ds,'opaque_id':oid});state['active']=None;save()
            gc.collect()
        state['status']='PASS';state['n_main_valid']=len(outputs)+2;save()
        c.write(out/'manifest.json',{'status':'PASS_OBSERVATION_AUDIT_ONLY','script_sha256':scripts(),
                'source_plan_sha256':c.sha(plan_dir/'plan.json'),'inputs':reader.inputs,
                'outputs':outputs,'reused_outputs':list(plan['pilots'].values()),'n_main_valid':len(outputs)+2,
                'limits':'Structure/interval audit only; no wait/self-time or RCA causal conclusion.'})
    except BaseException as exc:
        state['status']='STOPPED';state['error']=type(exc).__name__+': '+str(exc);save()
        c.write(out/'failure.json',{'status':state,'outputs_completed':outputs,'inputs':reader.inputs,
                                  'traceback':traceback.format_exc()})
        raise
    finally:
        save()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['prepare','run']);parser.add_argument('paths',nargs='+')
    args=parser.parse_args()
    require(os.name=='posix' and Path.home()==Path('/home/ubuntu'), 'EC2 only')
    require(len(args.paths)==(1 if args.mode=='prepare' else 2),'wrong CLI path count')
    out=Path(args.paths[-1]).resolve();require(out.parent==(BASE/'runs').resolve(),'output outside T-032/runs')
    out.mkdir(exist_ok=False)
    if args.mode=='prepare':prepare(out)
    else:run(Path(args.paths[0]).resolve(),out)
