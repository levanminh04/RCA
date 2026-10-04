"""EC2 runner. Writes only T-015 output/cache. Whitelist explicit; progress from first case."""
import argparse,datetime,hashlib,json,os,pathlib,resource,sys,time,traceback

HERE=pathlib.Path(__file__).resolve()
ROOT=HERE.parents[3] if 'results' in HERE.parts else HERE.parent
sys.path.insert(0,str(ROOT/'src'))
import pandas as pd
from microrank import microrank,COLS

def ts():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--cases',required=True);ap.add_argument('--out',required=True);ap.add_argument('--half',type=int,default=600);ap.add_argument('--snapshot',default='');ap.add_argument('--budget',type=int,default=2880);a=ap.parse_args()
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    cases=a.cases.split(',');assert all(c.startswith(('re2ob_','re2tt_')) for c in cases)
    start=time.monotonic();durations=[]
    progress=out/'progress.jsonl'
    def log(record):
        record['utc']=ts()
        with progress.open('a') as f:f.write(json.dumps(record)+'\n')
        print(json.dumps(record),flush=True)
    log({'event':'block_start','cases':cases,'half_seconds':a.half,'python':sys.version,'pandas':pd.__version__,'hash_seed':os.environ.get('PYTHONHASHSEED'),'timing_official':False})
    for i,case in enumerate(cases):
        elapsed=time.monotonic()-start
        estimated=max(durations[-3:]) if durations else 0
        if elapsed+estimated>a.budget:
            log({'event':'budget_stop','elapsed':elapsed,'completed':i,'pending':cases[i:]});break
        p=pathlib.Path(a.data)/case;target=out/(case+'.json')
        if target.exists():raise RuntimeError('Preserve previous run: output already exists '+str(target))
        t=time.monotonic();log({'event':'case_start','case':case,'index':i})
        try:
            f=p/'traces.parquet';inj=int((p/'inject_time.txt').read_text().strip())*1000000
            raw=pd.read_parquet(f,columns=COLS)
            lo=inj-a.half*1000000;hi=inj+a.half*1000000
            df=raw[(raw.startTime>=lo)&(raw.startTime<hi)]
            snapshot=case in a.snapshot.split(',')
            r=microrank(df,inj,include_graph=snapshot)
            r.update(case_id=case,source_file=str(f),source_sha256=sha(f),half_seconds=a.half,hash_seed=os.environ.get('PYTHONHASHSEED'),timing_official=False)
            r['boundary_trace_count']=int(len(set(raw.loc[~raw.index.isin(df.index),'traceID'])&set(df.traceID)))
            if (p/'metrics.parquet').exists():
                import pyarrow.parquet as pq
                columns=pq.read_schema(p/'metrics.parquet').names
                services=sorted(set(c.rsplit('_',1)[0] for c in columns if c.startswith('ts-')))
                seen=set(df.serviceName)
                r['candidate_audit']={'metric_services':services,'trace_services':sorted(seen),'metric_services_absent_from_trace':sorted(set(services)-seen),'trace_services_absent_from_full_rank':sorted(seen-set(r.get('service_ranks_full',[]))),'trace_services_absent_from_top11':sorted(seen-set(r.get('service_ranks_top11',[])))}
            target.write_text(json.dumps(r,ensure_ascii=False,allow_nan=False),encoding='utf-8')
            dur=time.monotonic()-t;durations.append(dur)
            log({'event':'case_end','case':case,'status':r['status'],'seconds':dur,'rss_mb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'counts':r.get('counts'),'sha256':sha(target),'forecast_remaining_seconds':max(durations[-3:])*(len(cases)-i-1)})
        except Exception as e:
            failure={'case_id':case,'status':'failed','error':str(e),'traceback':traceback.format_exc(),'half_seconds':a.half,'hash_seed':os.environ.get('PYTHONHASHSEED')}
            target.write_text(json.dumps(failure),encoding='utf-8')
            log({'event':'case_end','case':case,'status':'failed','seconds':time.monotonic()-t,'error':str(e)})
    log({'event':'block_end','elapsed_seconds':time.monotonic()-start})

if __name__=='__main__':main()
