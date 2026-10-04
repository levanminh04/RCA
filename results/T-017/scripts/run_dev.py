"""Reproducible dev-only correctness run. Every attempt and elapsed step kept.

The frozen allowlist is validated before any run is created or telemetry opened. Core does not receive
paths/case identifiers/root labels. Scoring starts only after result is written.
"""
import argparse,csv,hashlib,json,os,sys,time,traceback
from dataclasses import replace
from datetime import datetime,timezone,timedelta
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow
from simplerca import Config,diagnose,score_root
from simplerca.adapter import prepare,core_input

ROOT=Path('D:/RCA-flashticket')
OUT=ROOT/'results/T-017'
WORK=Path('D:/RCA-ext/work/T-017')

def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def load_allowlist(path=OUT/'allowlist.json'):
    names=json.loads(path.read_text(encoding='utf-8'))
    if (not isinstance(names,list) or len(names)!=30
            or any(not isinstance(n,str) or not n.startswith('re2tt_')
                   or Path(n).name!=n or '/' in n or '\\' in n for n in names)
            or len(set(names))!=30):
        raise RuntimeError('invalid frozen allowlist')
    return sorted(names)


def guard_case(path,allowed,data_root):
    if path.name not in allowed or path.resolve() != data_root.resolve()/path.name:
        raise RuntimeError('forbidden source case')


def validate_cases(dirs,allowed,data_root):
    if len(dirs)!=len(allowed) or {p.name for p in dirs}!=set(allowed):
        raise RuntimeError('case identities differ from frozen allowlist')
    for p in dirs:
        guard_case(p,allowed,data_root)
        if not p.is_dir(): raise RuntimeError('allowed case directory missing')
        for name in ('metrics.parquet','traces.parquet','logs.parquet'):
            source=p/name
            if source.exists(): guard_file(source,p)

def guard_file(path,case):
    if path.resolve().parent != case.resolve():
        raise RuntimeError('source file escapes allowed case')

def register(case,paths,purpose):
    path=OUT/'ca-da-chay.csv'
    fresh=not path.exists()
    with path.open('a',encoding='utf-8',newline='') as f:
        w=csv.writer(f)
        if fresh:w.writerow(['ca','file_nguon','phuong_phap','muc_dich','ly_do'])
        w.writerow([case,';'.join(str(p) for p in paths),'SimpleRCA (M4)',purpose,'b: code và cấu hình M4 mới; a: repeat nếu ghi trong mục đích'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);ap.add_argument('--limit',type=int,default=30);ap.add_argument('--start-index',type=int,default=0)
    args=ap.parse_args();run=OUT/'runs'/args.run
    if run.exists():raise RuntimeError('never overwrite a run')
    allowed=load_allowlist()
    dirs=sorted((ROOT/'data/rcaeval').glob('re2tt_*'))
    validate_cases(dirs,allowed,ROOT/'data/rcaeval')
    run.mkdir(parents=True)
    dump(run/'environment.json',{'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__,'pyarrow':pyarrow.__version__,'concurrent_laptop':True,'official_timing':False,'estimated_total_minutes':3,'allowlist_sha256':sha(OUT/'allowlist.json'),'allowed_cases':allowed})
    progress=run/'progress.jsonl'
    def log(event,**kw):
        row={'time_local':datetime.now(timezone(timedelta(hours=7))).isoformat(),'event':event,**kw}
        with progress.open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
        print(json.dumps(row,ensure_ascii=False),flush=True)
    summary=[]
    t0=time.perf_counter(); log('start',cases=min(args.limit,len(dirs)),budget_seconds=2700)
    for idx,p in enumerate(dirs[:args.limit]):
        if idx<args.start_index: continue
        guard_case(p,allowed,ROOT/'data/rcaeval')
        case_start=time.perf_counter();paths=[p/'metrics.parquet',p/'traces.parquet']
        if (p/'logs.parquet').exists():paths.append(p/'logs.parquet')
        for source_path in paths: guard_file(source_path,p)
        register(p.name,paths,'primary và kiểm' if idx<2 else 'partial reproduction 30 dev')
        log('case_start',case=p.name,index=idx+1)
        try:
            hashes={str(x):{'sha256':sha(x),'bytes':x.stat().st_size} for x in paths}
            boundary_path=WORK/'injection'/(p.name+'.txt')
            boundary=int(boundary_path.read_text().strip().splitlines()[0])
            hashes[str(boundary_path)]={'sha256':sha(boundary_path),'bytes':boundary_path.stat().st_size}
            m=pd.read_parquet(paths[0]);t=pd.read_parquet(paths[1],columns=['serviceName','startTime','duration'])
            l=pd.read_parquet(p/'logs.parquet') if (p/'logs.parquet').exists() else None
            log('loaded',case=p.name,elapsed_s=time.perf_counter()-case_start,metric_shape=list(m.shape),trace_shape=list(t.shape),log_shape=None if l is None else list(l.shape))
            prepared=prepare(m,t,l,boundary)
            inputs=core_input(prepared)
            result=diagnose(**inputs)
            dump(run/f'{p.name}.json',result)  # rank fixed before any root label used
            row={'case':p.name,'status':result['status'],'source_hashes':hashes,'checks':{},'score_file':str(run/f'{p.name}.json')}
            # Name is used only by the evaluation layer after file is closed.
            root=p.name[len('re2tt_'):].rsplit('_',2)[0]
            row['root_for_evaluation']=root
            row['top1']=score_root(result,root,1);row['top3']=score_root(result,root,3);row['top5']=score_root(result,root,5)
            row['checks']['not_fallback']=result['fallback'] is False
            row['checks']['nonempty']=bool(result['ranks'])
            row['checks']['score_sum']=all(x['score']==x['metric']+x['trace']+x['log'] for x in result['scores'].values())
            row['checks']['ranking_equals_metric_column_order']=result['ranks']==list(dict.fromkeys(prepared.metric_services.values()))
            if idx<2:
                again=diagnose(**inputs);dump(run/f'{p.name}-repeat.json',again)
                perm=dict(inputs);perm['normal_metrics']=dict(reversed(list(inputs['normal_metrics'].items())));perm['incident_metrics']=dict(reversed(list(inputs['incident_metrics'].items())));perm['metric_services']=dict(reversed(list(inputs['metric_services'].items())))
                flipped=diagnose(**perm);dump(run/f'{p.name}-permuted.json',flipped)
                row['checks']['repeat_exact']=again==result;row['checks']['permutation_exact']=flipped==result
                control=diagnose(**core_input(prepare(m,t,l,boundary-300,150)))
                dump(run/f'{p.name}-normal-control.json',control)
                row['normal_control']={'status':control['status'],'max_score':max(x['score'] for x in control['scores'].values()),'positive_services':sum(x['score']>0 for x in control['scores'].values()),'passes_abstention':control['status']=='abstain'}
            if idx==0:
                ex=WORK/('example-input-'+args.run);ex.mkdir(parents=True,exist_ok=True)
                for name,df in zip(['normal_metrics','incident_metrics','normal_traces','incident_traces','incident_logs'],prepared[:5]):
                    if df is None:df=pd.DataFrame(columns=['service','message'])
                    df.to_csv(ex/f'{name}.csv',index=False)
                dump(ex/'metadata.json',{'metric_services':prepared.metric_services,'observed_services':prepared.observed_services,'logs_available':prepared.incident_logs is not None,'boundary':boundary,'half':300,'case_is_not_passed_to_core':True})
                sensitivity=[]
                variants=[('p95',Config(metric_rule='p95')),('channels',Config(metric_aggregation='channels')),('log1',Config(log_threshold=1)),('log10',Config(log_threshold=10)),('trace2',Config(trace_factor=2)),('trace4',Config(trace_factor=4))]
                for name,cfg in variants:
                    s=diagnose(**inputs,config=cfg);dump(run/f'example-{name}.json',s)
                    sensitivity.append({'name':name,'config':s['config'],'scores':s['scores'],'tie_groups':s['tie_groups']})
                s=diagnose(**core_input(prepare(m,t,l,boundary,600)));dump(run/'example-half600.json',s)
                sensitivity.append({'name':'half600','config':s['config'],'scores':s['scores'],'tie_groups':s['tie_groups']})
                dump(run/'sensitivity.json',sensitivity)
            row['elapsed_seconds_concurrent_laptop']=time.perf_counter()-case_start
            summary.append(row);dump(run/'summary.json',summary)
            log('case_complete',case=p.name,elapsed_s=row['elapsed_seconds_concurrent_laptop'],top1=row['top1']['hit_fractional'])
        except Exception as e:
            err={'case':p.name,'status':'failed','error':repr(e),'traceback':traceback.format_exc(),'elapsed_seconds':time.perf_counter()-case_start}
            dump(run/f'{p.name}-failed.json',err);summary.append(err);dump(run/'summary.json',summary);log('case_failed',case=p.name,error=repr(e));raise
        if time.perf_counter()-t0>2700:raise RuntimeError('total estimate exceeded; no next case')
    log('complete',elapsed_s=time.perf_counter()-t0,cases=len(summary))

if __name__=='__main__':main()
