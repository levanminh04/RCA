"""Q-191: explicit normal-source contrast; bounded reader, no shared code edits."""
import os
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_k]='1'
import argparse, ast, contextlib, csv, gzip, hashlib, importlib.util, io, json, math, sys, time, traceback
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import numpy as np
import pandas as pd
import psutil

ROOT=Path('D:/RCA-flashticket')
BASE=Path(__file__).resolve().parent
OLD=ROOT/'results/T-042/runs/continuation-001'
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'results/T-042/scripts'),str(OLD)]
from p3 import nezha
from simplerca import Config, diagnose
import microrank as repaired
import simple_runner as sr
from kiem_doc_lap import arithmetic, metric_time
NS=10**9

def now():return datetime.now(timezone.utc).isoformat()
def read(p):
    p=Path(p)
    with (gzip.open(p,'rt',encoding='utf-8') if p.suffix=='.gz' else p.open(encoding='utf-8-sig')) as f:return json.load(f)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def clean(v):
    if isinstance(v,np.ndarray):return clean(v.tolist())
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [clean(x) for x in v]
    return sr.plain(v)
def digest(v):return hashlib.sha256(json.dumps(clean(v),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(p,v):
    p=Path(p);assert p.resolve().is_relative_to(BASE)
    p.parent.mkdir(parents=True,exist_ok=True)
    with (gzip.open(p,'xt',encoding='utf-8') if p.suffix=='.gz' else p.open('x',encoding='utf-8')) as f:
        json.dump(clean(v),f,ensure_ascii=False,allow_nan=False,indent=1);f.write('\n')
def event(folder,name,**kw):
    v=dict(utc=now(),event=name,**kw)
    with (folder/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(v,ensure_ascii=True)+'\n')
    print(json.dumps(v,ensure_ascii=True),flush=True)
def size():return sum(p.stat().st_size for p in BASE.rglob('*') if p.is_file())
def limit(start):
    if size()>20_000_000:raise RuntimeError('Q191 20MB output limit exceeded')
    if time.perf_counter()-start>3500:raise RuntimeError('Stop before one hour')
def frame_digest(df):
    return hashlib.sha256(pd.util.hash_pandas_object(df,index=False).values.tobytes()+str(list(df.columns)).encode()).hexdigest()

def prepare(folder):
    checks=[]
    for mp in (ROOT/'results/T-042/manifest.json',OLD/'manifest.json'):
        m=read(mp)
        for row in m['files']:
            assert sha(ROOT/row['path'])==row['sha256'],row['path']
        checks.append(dict(manifest=str(mp),sha256=sha(mp),checked=len(m['files'])))
    frozen=read(ROOT/'results/T-026/ban-ghi-dua-vao-cham.json')
    sourcepins={}
    for p,h in frozen['source_hashes'].items():
        if p.startswith(('src/p3/','src/simplerca/','src/microrank/')) or p=='results/T-026/allowlist-dev.json':
            assert sha(ROOT/p)==h,p;sourcepins[p]=h
    inventory=ROOT/'results/T-008/runs/download-001/manifest.json'
    assert sha(inventory)=='30d8e5bef26189f2ff27dccc6b6392e3ad5777290a583875d60532a0b5d145af'
    pin=read(inventory)
    allow=nezha.nap_allowlist(ROOT/'results/T-026/allowlist-dev.json')
    days={}
    for day,minute in [('2022-08-22','03_51'),('2022-08-23','17_00')]:
        lo=int(datetime.fromisoformat(day+'T'+minute.replace('_',':')+':00+00:00').timestamp())*NS
        candidates={Path(p).name for a in allow.values() for p in a['files'] if '/'+day+'/metric/' in p}
        assert len(candidates)==11
        wanted={('metric',name) for name in candidates}|{('log',minute+'_log.csv'),('trace',minute+'_trace.csv')}
        rows=[]
        prefix='online-boutique/construct_data/'+day+'/'
        for item in pin['items']:
            p=Path(item['path'])
            if item['path'].startswith(prefix) and (p.parent.name,p.name) in wanted:
                rel='data/ngoai-rcaeval/nezha/'+item['path'];full=ROOT/rel
                assert full.resolve().is_relative_to((ROOT/'data/ngoai-rcaeval/nezha/online-boutique/construct_data'/day).resolve())
                assert item['status']=='ok' and full.stat().st_size==item['bytes']
                assert sha(full)==item['sha256'],rel
                rows.append(dict(path=rel,sha256=item['sha256'],bytes=item['bytes'],git_blob_sha=item['git_blob_sha'],kind=p.parent.name))
        assert len(rows)==13 and {(x['kind'],Path(x['path']).name) for x in rows}==wanted
        days[day]=dict(low_ns=lo,high_ns=lo+60*NS,files=sorted(rows,key=lambda x:x['path']),
                       selection='metric Time; trace start>=low and end<high; log low<=time<high; original timestamps')
    write(BASE/'normal-allowlist.json',dict(days=days,source_inventory_sha256=sha(inventory),all_raw_hashes_match=True,normal_health='UNVERIFIED'))
    plan=dict(authorization='Q-191',created_utc=now(),dev_ids=sorted(allow),N=['preincident300s reusable baseline','converter-minute source with P3 representation'],
              A='original P3 [t,t+300s), unchanged native timestamps, per-method split unchanged',methods=['M4-S0','main-M0','MicroRank-repaired-sham'],
              fixed=['Config','channels165','aliases','metric clock Time','trace Duration microseconds','evaluator','A payload'],
              not_claimed=['normal fault-free','full converter or historical author pipeline','N cleanliness isolated from duration or coverage','new baseline selected'],
              F2=dict(metric_indices_early=[0,1],late=[3,4],std_denominator='population std of all five, null if zero',trace_log='first/last150s; empty half marked unavailable',root_blind=True),
              micro_adapter='only replace two before/after AST assignments with explicit source-group index; no timestamp shift',
              insufficient='M4 unavailable channels; native MAIN fallback audited; Micro missing baseline/std is error, no fill',
              pilot='smallest dev input, exact replay old N with explicit adapter, then N contrast; full reuses pilot',
              output_limit_bytes=20_000_000,run_limit_s=3500,download_install=False,labels_until_frozen=False,
              old_output_checks=checks,source_pins=sourcepins,python=sys.executable,numpy=np.__version__,pandas=pd.__version__,hashseed=os.environ.get('PYTHONHASHSEED'))
    write(BASE/'plan.json',plan)
    _,pins=sr.load_kernels();write(folder/'source-checks.json',dict(old_outputs=checks,core=sourcepins,kernels=pins,labels_read=False))
    event(folder,'PREPARE_PASS',raw_normal_files=sum(len(v['files']) for v in days.values()),raw_normal_bytes=sum(x['bytes'] for v in days.values() for x in v['files']),old_results_checked=sum(x['checked'] for x in checks))

def normal_read(day):
    entry=read(BASE/'normal-allowlist.json')['days'][day];lo,hi=entry['low_ns'],entry['high_ns']
    arrays={};meta={};spanrows=[];logrows=[];sources={};seen={};duplicates=0
    csv.field_size_limit(10_000_000)
    for item in entry['files']:
        p=ROOT/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256']
        times=[];kept=[]
        with p.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f);kind=item['kind']
            for row in reader:
                if kind=='metric':
                    stamp=nezha.parse_time_ns(row['Time'])
                    if not lo<=stamp<hi:continue
                    assert stamp==metric_time(row['Time'])
                    front=p.name=='front_service.csv';idcol='ServiceName' if front else 'PodName'
                    aliases=nezha.SERVICE_ALIASES if front else nezha.POD_ALIASES
                    assert row[idcol] in aliases
                    if not front:assert p.name==row[idcol]+'_metric.csv'
                    kept.append((stamp,aliases[row[idcol]],row));times.append(stamp)
                elif kind=='trace':
                    st,en=int(row['StartTimeUnixNano']),int(row['EndTimeUnixNano'])
                    if not lo<=st or not en<hi:continue
                    assert en>=st and row['PodName'] in nezha.POD_ALIASES
                    d=Decimal(row['Duration']);assert d.is_finite() and d>=0 and d==int(d)
                    d=int(d);assert 0<=en-st-d*1000<1000
                    assert row['TraceID'] and row['SpanID']
                    ident=(row['TraceID'],row['SpanID']);sig=tuple(sorted(row.items()))
                    if ident in seen:assert seen[ident]==sig;duplicates+=1
                    seen[ident]=sig
                    spanrows.append([row['TraceID'],row['SpanID'],row['ParentID'],nezha.POD_ALIASES[row['PodName']],row['OperationName'],row['OperationName'],st//1000,d,st,en]);times.append(st)
                else:
                    stamp=int(row['TimeUnixNano'])
                    if not lo<=stamp<hi:continue
                    assert row['PodName'] in nezha.POD_ALIASES and nezha._log_time_ns(row['Timestamp'])==stamp
                    logrows.append([stamp,nezha.POD_ALIASES[row['PodName']],row['Log'],stamp]);times.append(stamp)
        if item['kind']=='metric':
            kept.sort(key=lambda x:x[0]);front=p.name=='front_service.csv';channels=nezha.FRONT_CHANNELS if front else nezha.RESOURCE_CHANNELS
            ident=nezha.SERVICE_ALIASES['Frontend'] if front else nezha.POD_ALIASES[p.name[:-11]]
            for col,suffix in channels.items():
                key=ident+'_'+suffix;assert key not in arrays
                arrays[key]=np.array([nezha._numeric(row[col]) for _,_,row in kept],dtype=float)
                meta[key]=dict(source=item['path'],source_column=col,timestamps_ns=[s for s,_,_ in kept],finite=int(np.isfinite(arrays[key]).sum()))
        sources[item['path']]=dict(kind=item['kind'],rows=len(times),first_ns=min(times) if times else None,last_ns=max(times) if times else None,sha256=item['sha256'])
    assert len(arrays)==165
    spans=pd.DataFrame(spanrows,columns=nezha.SPAN_COLUMNS);logs=pd.DataFrame(logrows,columns=nezha.LOG_COLUMNS)
    for c in ('startTime','duration','_start_ns','_end_ns'):spans[c]=spans[c].astype('int64')
    for c in ('timestamp','_timestamp_ns'):logs[c]=logs[c].astype('int64')
    return dict(arrays=arrays,meta=meta,spans=spans,logs=logs,entry=entry,audit=dict(day=day,interval=[lo,hi],sources=sources,channels=meta,
       metric_n_finite_histogram=dict(Counter(v['finite'] for v in meta.values())),spans=len(spans),logs=len(logs),duplicate_spans_retained=duplicates,
       trace_services=spans.groupby('serviceName').size().to_dict(),log_services=logs.groupby('container_name').size().to_dict(),clock_shift_ns=0,raw_payload_saved=False,labels_read=False))

def n_frames(n,network):
    rows=[]
    wanted={'CpuUsageRate(%)','MemoryUsageRate(%)','PodClientLatencyP90(s)','PodServerLatencyP90(s)','PodClientLatencyP99(s)','PodServerLatencyP99(s)'}
    for k,a in n['arrays'].items():
        m=n['meta'][k]
        if m['source_column'] not in wanted:continue
        for stamp,v in zip(m['timestamps_ns'],a):rows.append(dict(service_name=k.rsplit('_',1)[0],time=stamp,metric=m['source_column'],value=float(v)))
    m=network(pd.DataFrame(rows,columns=['service_name','time','metric','value']))
    l=n['logs'].rename(columns={'container_name':'service_name','_timestamp_ns':'time'})[['service_name','time','message']].copy();l['message']=l.message.map(sr.extract_message)
    t=n['spans'].rename(columns={'serviceName':'service_name','spanID':'span_id','parentSpanID':'parent_span_id'})[['service_name','span_id','parent_span_id','duration','_start_ns','_end_ns']].copy()
    return m,l,t

def explicit_micro():
    p=ROOT/'src/microrank/__init__.py';tree=ast.parse(p.read_text(encoding='utf-8-sig'))
    f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='microrank');original=ast.dump(f,include_attributes=False)
    replaced=[]
    for i,node in enumerate(f.body):
        if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('before','after'):
            name=node.targets[0].id;expr='df.loc[df.index < _normal_rows].copy()' if name=='before' else 'df.loc[df.index >= _normal_rows].copy()'
            f.body[i]=ast.Assign(targets=node.targets,value=ast.parse(expr,mode='eval').body);replaced.append(name)
    assert replaced==['before','after'];ast.fix_missing_locations(f)
    ns=dict(repaired.__dict__);exec(compile(ast.Module(body=[f],type_ignores=[]),str(BASE/'explicit-N-A-adapter'),'exec'),ns)
    def call(n,a):
        ns['_normal_rows']=len(n)
        df=pd.concat([n[repaired.COLS],a[repaired.COLS]],ignore_index=True)
        return ns['microrank'](df,0,include_graph=False)
    pin=dict(source_sha256=sha(p),original_ast_sha256=hashlib.sha256(original.encode()).hexdigest(),adapter_ast_sha256=hashlib.sha256(ast.dump(f,include_attributes=False).encode()).hexdigest(),only_assignments_replaced=replaced)
    return call,pin

def micro_audit(n,a):
    def ops(df):
        x=df.copy();x['operation']=x.serviceName+'_'+x.methodName.fillna(x.operationName);return x
    n,a=ops(n),ops(a);g=n.groupby('operation').duration.agg(['count','mean','std']);g['mean']=(g['mean']/1000).round(2);g['std']=(g['std']/1000).round(2)
    missing=sorted(set(a.operation)-set(g.index));insufficient=sorted(op for op in set(a.operation)&set(g.index) if not math.isfinite(g.loc[op,'std']))
    result=dict(normal_spans=len(n),A_spans=len(a),normal_operation_count=len(g),A_operation_count=a.operation.nunique(),missing_operations=missing,undefined_std_operations=insufficient,
                normal_slo_ms={op:{k:float(v) for k,v in row.items()} for op,row in g.iterrows()})
    if not missing and not insufficient:
        flags=a.duration/1000>=a.operation.map(g['mean'])+3*a.operation.map(g['std'])
        result['A_abnormal_spans_by_operation']=a.assign(flag=flags).groupby('operation').flag.agg(['count','sum']).to_dict('index')
        result['abnormal_spans']=int(flags.sum());result['abnormal_traces']=int(a.loc[flags].traceID.nunique())
    return result

def statistics(values):
    a=np.array(values,dtype=float);a=a[np.isfinite(a)]
    return dict(n=len(a),mean=float(a.mean()) if len(a) else None,std=float(a.std(ddof=0)) if len(a) else None,min=float(a.min()) if len(a) else None,max=float(a.max()) if len(a) else None)
def f2(payload):
    rows={}
    for k,x in payload['metric_arrays'].items():
        n=x['normal'];assert len(n)==5
        e,l=statistics(n[:2]),statistics(n[3:]);alln=statistics(n)
        delta=l['mean']-e['mean'] if e['n'] and l['n'] else None
        rows[k]=dict(early=e,late=l,delta=delta,all_normal=alln,delta_over_std=delta/alln['std'] if delta is not None and alln['std']>0 else None,
                     timestamps_ns=payload['provenance']['channels'][k]['timestamps_ns'][:5])
    t=payload['t_ns'];mid=t-150*NS;lo=t-300*NS;tr=payload['spans'];lg=payload['logs'];halves={}
    for name,low,high in [('early',lo,mid),('late',mid,t)]:
        tf=tr.loc[(tr._start_ns>=low)&(tr._start_ns<high)];lf=lg.loc[(lg._timestamp_ns>=low)&(lg._timestamp_ns<high)]
        halves[name]=dict(trace={s:dict(**statistics(g.duration),spans=len(g),traces=int(g.traceID.nunique())) for s,g in tf.groupby('serviceName')},
                          log={s:dict(rows=len(g),keyword_rows=sum(any(w in str(m).upper() for w in ('ERROR','FAIL','EXCEPTION')) for m in g.message)) for s,g in lf.groupby('container_name')})
    return dict(metric=rows,trace_log_halves=halves,claim='descriptive drift only; no recovery attribution',labels_read=False)

def read_baselines():
    manifest=read(ROOT/'results/T-042/manifest.json');m4={}
    for row in manifest['files']:
        if row['path'].endswith('-S0.json'):
            d=read(ROOT/row['path']);m4[d['opaque_id']]=dict(path=row['path'],sha256=row['sha256'])
    main={x['opaque_id']:x for x in read(OLD/'simple-full-001/diagnoses-frozen.json')['records'] if x['branch']=='M0'}
    micro={x['opaque_id']:x for x in read(OLD/'micro/full-004/diagnosis-list.json')['records'] if x['branch']=='repaired_sham'}
    assert len(m4)==len(main)==len(micro)==22
    return dict(M4=m4,MAIN=main,MICRO=micro)

def execute(folder,pilot):
    start=time.perf_counter();peak=0;allow=nezha.nap_allowlist(ROOT/'results/T-026/allowlist-dev.json');baseline=read_baselines()
    kernels,pins=sr.load_kernels();ns,network,_=kernels;micro,pin=explicit_micro();normal={};records=[]
    order=sorted(allow,key=lambda k:(sum(v['bytes'] for v in allow[k]['files'].values()),k))
    if pilot:order=order[:1]
    write(folder/'config.json',dict(order=order,pilot=pilot,source_script_sha256=sha(__file__),plan_sha256=sha(BASE/'plan.json'),kernels=pins,explicit_micro=pin,labels_read=False))
    for ix,oid in enumerate(order):
        if not pilot:
            cached=read(BASE/'pilot-001/diagnoses-frozen.json');reuse=[x for x in cached['records'] if x['opaque_id']==oid]
            if reuse:
                assert cached['source_script_sha256']==sha(__file__)
                for p in reuse:assert sha(ROOT/p['path'])==p['sha256']
                records.extend(reuse);event(folder,'REUSE_PILOT',opaque_id=oid);continue
        event(folder,'CASE_START',opaque_id=oid,index=ix+1,total=len(order));s=time.perf_counter()
        selection=nezha.chon_ca(allow,oid,ROOT);payload=nezha.doc_cua_so(selection);day=next(iter(selection['files'])).split('/')[-3]
        if day not in normal:
            normal[day]=normal_read(day);write(folder/('normal-'+day+'-audit.json'),normal[day]['audit'])
            event(folder,'NORMAL_COUNTS',day=day,metric_finite=normal[day]['audit']['metric_n_finite_histogram'],spans=len(normal[day]['spans']),logs=len(normal[day]['logs']))
        n=normal[day];oldkwargs=sr.inputs(payload);kwargs=dict(oldkwargs)
        assert set(n['arrays'])==set(kwargs['normal_metrics'])
        kwargs['normal_metrics']=n['arrays'];kwargs['normal_traces']={str(k):g.duration.tolist() for k,g in n['spans'].groupby('serviceName',sort=True)}
        assert set(kwargs['normal_traces'])<=set(kwargs['observed_services'])
        A_hash=dict(metrics=digest(kwargs['incident_metrics']),traces=digest(kwargs['incident_traces']),logs=digest(kwargs['incident_logs']),mapping=digest(kwargs['metric_services']))
        assert A_hash==dict(metrics=digest(oldkwargs['incident_metrics']),traces=digest(oldkwargs['incident_traces']),logs=digest(oldkwargs['incident_logs']),mapping=digest(oldkwargs['metric_services']))
        ms,wide,ls,ts=sr.dataframes(payload,network['calculate_network_latency']);newm,newl,newt=n_frames(n,network['calculate_network_latency'])
        newms=dict(ms,N=newm);newls=dict(ls,N=newl);newts=dict(ts,N=newt)
        assert frame_digest(newms['A'])==frame_digest(ms['A']) and frame_digest(newls['A'])==frame_digest(ls['A']) and frame_digest(newts['A'])==frame_digest(ts['A'])
        boundary=payload['t_ns']//1000;spans=payload['spans'][repaired.COLS].copy();nold=spans.loc[spans.startTime+spans.duration<boundary];a=spans.loc[spans.startTime+spans.duration>=boundary]
        newn=n['spans'][repaired.COLS];ma=micro_audit(newn,a)
        replay={}
        if pilot:
            original=repaired.microrank(spans,boundary,include_graph=False);explicit=micro(nold,a)
            assert digest(original)==digest(explicit);replay['explicit_split_vs_core_exact']=True
            bm=read(ROOT/baseline['M4'][oid]['path'])['diagnosis'];re=diagnose(**oldkwargs,config=Config());assert digest(bm)==digest(re);replay['M4_old_exact']=True
            main=sr.run_main(ns,ms,ls,ts);bm=read(ROOT/baseline['MAIN'][oid]['path'])['result'];assert digest(main)==digest(bm);replay['MAIN_old_exact']=True
            write(folder/'matched-replay-checks.json',dict(checks=replay,labels_read=False))
        values={}
        method_start=time.perf_counter();m4=diagnose(**kwargs,config=Config());m4check=arithmetic(kwargs,Config(),m4)
        values['M4']=dict(status='OK',diagnosis=m4,independent=m4check,method_s=time.perf_counter()-method_start)
        method_start=time.perf_counter();main=sr.run_main(ns,newms,newls,newts)
        values['MAIN']=dict(status='OK',result=main,method_s=time.perf_counter()-method_start)
        method_start=time.perf_counter()
        try:
            mr=micro(newn,a)
            assert mr['status']=='ok',mr['status']
            # All weighted spectrum cells independently checked from saved class counts/weights.
            n_group=mr['groups']['normal']['official'];a_group=mr['groups']['anomaly']['official']
            cells=repaired.spectrum_cells(a_group['weights'],n_group['weights'],mr['counts']['anomaly'],mr['counts']['normal'],a_group['tracecounts'],n_group['tracecounts'])
            assert digest(cells)==digest(mr['spectrum'])
            for op,v in mr['scores'].items():
                c=cells[op];assert math.isclose(v,c['ef']**2/(c['ep']+c['nf']),rel_tol=1e-14,abs_tol=0)
            values['MICRO']=dict(status='OK',result=mr,independent_spectrum='PASS',method_s=time.perf_counter()-method_start)
        except (ValueError,AssertionError) as exc:
            if not (ma['missing_operations'] or ma['undefined_std_operations']):raise
            values['MICRO']=dict(status='UNSUPPORTED_NORMAL_INPUT',error=dict(type=type(exc).__name__,message=str(exc)),audit=ma,method_s=time.perf_counter()-method_start)
        audit=dict(opaque_id=oid,day=day,A_payload_fingerprints=A_hash,MAIN_A_fingerprints={k:frame_digest(v['A']) for k,v in [('metric',ms),('log',ls),('trace',ts)]},MICRO_A_fingerprint=frame_digest(a),MICRO_A_rows=len(a),
                   window=payload['window'],MICRO_normal_time_relation='after incident possible; explicit source groups, no clock shift',MICRO_audit=ma,matched_replay=replay,labels_read=False,raw_payload_saved=False)
        write(folder/'cases'/oid/'input-audit.json',audit);write(folder/'cases'/oid/'F2.json.gz',f2(payload))
        for method,value in values.items():
            dest=folder/'cases'/oid/(method+'.json.gz');write(dest,dict(opaque_id=oid,method=method,normal_source_day=day,baseline=baseline[method][oid],**value,labels_read=False,raw_payload_saved=False))
            records.append(dict(opaque_id=oid,method=method,path=dest.relative_to(ROOT).as_posix(),sha256=sha(dest)))
        peak=max(peak,psutil.Process().memory_info().rss);event(folder,'CASE_DONE',opaque_id=oid,elapsed_s=time.perf_counter()-s,statuses={k:v['status'] for k,v in values.items()});limit(start)
    write(folder/'diagnoses-frozen.json',dict(completed=True,created_utc=now(),records=records,source_script_sha256=sha(__file__),labels_read=False))
    write(folder/'cost.json',dict(wall_s=time.perf_counter()-start,peak_sampled_rss_bytes=peak,records=len(records),new_output_bytes=size()));event(folder,'FROZEN',records=len(records))

def fixtures(folder):
    call,pin=explicit_micro();checks={}
    # Opposite chronology must not change explicit source-group assignment.
    rows=[]
    for trace,dur in [('n1',1000),('n2',2000),('a1',1000),('a2',100000)]:
        rows.append(dict(traceID=trace,spanID=trace,parentSpanID=None,serviceName='s',methodName='op',operationName='op',startTime=0 if trace.startswith('n') else 10**6,duration=dur))
    df=pd.DataFrame(rows);n,a=df.iloc[:2].copy(),df.iloc[2:].copy()
    x=repaired.microrank(df,500000);y=call(n,a);checks['split_adapter_matches_original']=digest(x)==digest(y)
    n.startTime=10**9;z=call(n,a);checks['normal_after_incident_without_shift']=z['scores']==y['scores'] and z['baseline_slo_ms']==y['baseline_slo_ms']
    assert all(checks.values());write(folder/'checks.json',dict(status='PASS',checks=checks,adapter=pin,labels_read=False))
    event(folder,'FIXTURES_PASS',checks=len(checks))

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','fixtures','pilot','full']);p.add_argument('run_id');args=p.parse_args()
    folder=BASE/args.run_id;folder.mkdir(exist_ok=False)
    write(folder/'invocation.json',dict(argv=sys.argv,utc=now(),python=sys.executable,script_sha256=sha(__file__)))
    (folder/'source-at-start.py').write_bytes(Path(__file__).read_bytes())
    with (folder/'stdout.txt').open('x',encoding='utf-8') as stdout,(folder/'stderr.txt').open('x',encoding='utf-8') as stderr:
        class Tee:
            def write(self,s):stdout.write(s);sys.__stdout__.write(s)
            def flush(self):stdout.flush();sys.__stdout__.flush()
        with contextlib.redirect_stdout(Tee()),contextlib.redirect_stderr(stderr):
            try:
                if args.stage=='prepare':prepare(folder)
                elif args.stage=='fixtures':fixtures(folder)
                else:execute(folder,args.stage=='pilot')
            except BaseException as exc:
                event(folder,'FAILED',error=type(exc).__name__+': '+str(exc));traceback.print_exc();raise
if __name__=='__main__':main()
