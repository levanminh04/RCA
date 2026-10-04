"""Read release archives inertly: CRC/hash inventory and actual input schemas.

Never executes bundled code, deserializes pickle, or treats saved method results
as labels. Run in a fresh folder. Telemetry excluded from Bank by construction.
"""
import argparse,collections,csv,datetime,hashlib,io,json,math,re,statistics,sys,tarfile,time,zipfile
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=B.parents[1]
csv.field_size_limit(100_000_000)
def save(o,name,x):(o/name).write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
def quantile(x,q):
    x=sorted(x);i=(len(x)-1)*q;l=int(i);return x[l]+(x[min(l+1,len(x)-1)]-x[l])*(i-l)
def graph(rows,roots):
    keys=collections.defaultdict(list)
    for r in rows:keys[(r['trace'],r['span'])].append(r)
    counts=collections.Counter();edges=set();nodes={r['entity'] for r in rows}
    for r in rows:
        if r['parent'] in ('',None,'-1','0','0000000000000000'):counts['root_sentinel']+=1;continue
        parents=keys.get((r['trace'],r['parent']),[])
        counts['unique_parent' if len(parents)==1 else 'missing_parent' if not parents else 'ambiguous_parent']+=1
        if len(parents)==1 and parents[0]['entity']!=r['entity']:edges.add((parents[0]['entity'],r['entity']))
    positions=[dict(root=r,present=r in nodes,indegree=sum(y==r for x,y in edges),outdegree=sum(x==r for x,y in edges)) for r in roots]
    return dict(rows=len(rows),trace_ids=len({r['trace'] for r in rows}),services=sorted(nodes),parent=dict(counts),duplicate_keys=sum(len(x)-1 for x in keys.values()),edges=[list(x) for x in sorted(edges)],root_positions=positions)
def numeric_series(rows,time_key,value_key,entity_key,channel_key):
    series=collections.defaultdict(list);bad=collections.Counter()
    for r in rows:
        try:
            v=float(r[value_key]);t=r[time_key]
            if isinstance(t,str):
                try:t=float(t)
                except ValueError:t=datetime.datetime.fromisoformat(t.replace('Z','+00:00'))
            if not math.isfinite(v):bad['nonfinite']+=1;continue
            if t is None:bad['missing_time']+=1;continue
            entity=str(r.get(entity_key) or '<missing>');channel=str(r.get(channel_key) or value_key)
            # Keep differing resource/tag attributes separate; do not mix pods.
            tags=tuple(sorted((k,str(v)) for k,v in r.items() if k not in (time_key,value_key,entity_key,channel_key,'datetime') and v not in (None,'')))
            series[(entity,channel,tags)].append((t,v))
        except (TypeError,ValueError,KeyError):bad['invalid']+=1
    summary=[]
    for key,obs in series.items():
        obs.sort(key=lambda x:x[0]);vals=[v for t,v in obs];ts=[t for t,v in obs];steps=[]
        for a,b in zip(ts,ts[1:]):
            d=b-a;steps.append(d.total_seconds() if hasattr(d,'total_seconds') else float(d))
        summary.append(dict(entity=key[0],channel=key[1],tags=key[2],n=len(obs),start=ts[0],end=ts[-1],constant=min(vals)==max(vals),duplicate_times=len(ts)-len(set(ts)),positive_step_min=min((d for d in steps if d>0),default=None),positive_step_max=max((d for d in steps if d>0),default=None)))
    return series,dict(rows=len(rows),series=summary,bad=dict(bad))
def probes(normal,abnormal,roots,case,channel):
    out=[]
    for key in sorted(set(normal)|set(abnormal),key=str):
        ns=sorted(normal.get(key,[]),key=lambda x:x[0]);fs=abnormal.get(key,[]);n=len(ns)//2;ref=[v for t,v in ns[:n]];ctrl=[v for t,v in ns[n:]]
        for q in (.95,.99,.995):
            r=dict(case=case,channel=channel,entity=key[0],feature=key[1],tags=key[2] if len(key)>2 else [],outside_root=key[0] not in roots,q=q,reference_n=n,control_n=len(ctrl),fault_n=len(fs))
            if n<2 or len(ctrl)<2:r['status']='missing_or_short_reference';out.append(r);continue
            med=statistics.median(ref);band=quantile([abs(v-med) for v in ref],q);ce=sum(abs(v-med)>band for v in ctrl);fe=sum(abs(v-med)>band for t,v in fs)
            r.update(status='descriptive_only',median=med,band=band,zero_band=band==0,control_exceed=ce,fault_exceed=fe);out.append(r)
    return out
def inventory(path,o):
    start=time.monotonic();rows=[];zipmode=path.suffix=='.zip';z=zipfile.ZipFile(path) if zipmode else tarfile.open(path,'r:gz')
    for m in z.infolist() if zipmode else z:
        name=m.filename if zipmode else m.name;size=m.file_size if zipmode else m.size;regular=not m.is_dir() if zipmode else m.isfile();h=hashlib.sha256();n=0
        if regular:
            with z.open(m) if zipmode else z.extractfile(m) as f:
                for block in iter(lambda:f.read(1024*1024),b''):n+=len(block);h.update(block)
            if n!=size:raise ValueError('member size '+name)
        rows.append(dict(name=name,bytes=size,regular=regular,sha256=h.hexdigest() if regular else None,crc32=m.CRC if zipmode else None))
    z.close();save(o,'members.json',rows);save(o,'archive.json',dict(path=path.relative_to(ROOT).as_posix(),compressed_bytes=path.stat().st_size,member_bytes=sum(x['bytes'] for x in rows if x['regular']),members=len(rows),all_member_bytes_read=True,zip_crc_or_gzip_integrity_ok=True,seconds=time.monotonic()-start))
    print('inventory PASS',len(rows),flush=True);return rows
def fse(path,o):
    sys.path.insert(0,str(ROOT/'data/ngoai-rcaeval/T-012/python-packages'));import pyarrow as pa;import pyarrow.parquet as pq
    prefix='FSE_26_RCA_dataset_study_artifact_clean/reproduction/data/rcabench-platform-v2/data/rcabench/'
    cases=collections.defaultdict(dict);files=[]
    with tarfile.open(path,'r:gz') as z:
        for m in z:
            if not m.isfile():continue
            if m.name.endswith('/LICENSE') and m.name.count('/')==1: (o/'LICENSE.txt').write_bytes(z.extractfile(m).read())
            if '/reproduction/data/rcabench-platform-v2/CASELIST.txt' in m.name:(o/'CASELIST.txt').write_bytes(z.extractfile(m).read())
            if not m.name.startswith(prefix):continue
            tail=m.name[len(prefix):];case,filename=tail.split('/',1);raw=z.extractfile(m).read();d=cases[case]
            if filename.endswith('.parquet'):
                pf=pq.ParquetFile(pa.BufferReader(raw));cols=pf.schema_arrow.names
                # Read all actual inputs, retaining only values needed for inspection.
                table=pf.read()
                for i,field in enumerate(table.schema):
                    if pa.types.is_timestamp(field.type):table=table.set_column(i,field.name,table.column(i).cast(pa.int64()))
                rows=table.to_pylist();files.append(dict(case=case,file=filename,rows=len(rows),schema=str(pf.schema_arrow),timestamp_representation='exact integer in original schema time unit, no rounding'))
                if filename in ('normal_traces.parquet','abnormal_traces.parquet','normal_metrics.parquet','abnormal_metrics.parquet','normal_logs.parquet','abnormal_logs.parquet'):d[filename]=rows
            elif filename in ('env.json','injection.json'):d[filename]=json.loads(raw)
            elif filename=='.invalid':d['invalid']=raw.decode('utf-8',errors='replace')
    summaries=[];bands=[]
    for case,d in cases.items():
        inj=d.get('injection.json',{});roots=inj.get('ground_truth',{}).get('service') or [];r=dict(case=case,invalid_marker='invalid' in d,invalid_reason=d.get('invalid'),injection=inj,environment=d.get('env.json'),roots=roots,phases={})
        series={}
        for phase in ('normal','abnormal'):
            trace=d.get(phase+'_traces.parquet',[]);logs=d.get(phase+'_logs.parquet',[]);metrics=d.get(phase+'_metrics.parquet',[])
            spans=[dict(trace=x['trace_id'],span=x['span_id'],parent=x['parent_span_id'],entity=x['service_name']) for x in trace];g=graph(spans,roots);pairs={(x['trace'],x['span']) for x in spans};tids={x['trace'] for x in spans}
            r['phases'][phase]=dict(trace=g,log=dict(rows=len(logs),with_trace=sum(bool(x.get('trace_id')) for x in logs),trace_matches=sum(x.get('trace_id') in tids for x in logs),span_matches=sum((x.get('trace_id'),x.get('span_id')) in pairs for x in logs)))
            ms,quality=numeric_series(metrics,'time','value','service_name','metric');r['phases'][phase]['metric']=quality
            ts=collections.defaultdict(list)
            for x in trace:
                if x.get('duration') is not None:ts[(str(x['service_name']),str(x['span_name']))].append((x['time'],float(x['duration'])))
            series[phase]=(ms,ts)
            r['phases'][phase]['trace']['time_min']=min((x['time'] for x in trace),default=None);r['phases'][phase]['trace']['time_max']=max((x['time'] for x in trace),default=None)
        if roots and not r['invalid_marker']:
            for i,c in enumerate(('metric_raw','trace_duration')):bands+=probes(series['normal'][i],series['abnormal'][i],roots,case,c)
        summaries.append(r);print('fse case',case,flush=True)
    save(o,'schemas.json',files);save(o,'cases.json',summaries);save(o,'descriptive-bands.json',bands)
    valid=[x for x in summaries if not x['invalid_marker']];save(o,'census.json',dict(case_folders=len(summaries),invalid=len(summaries)-len(valid),valid_cases=len(valid),root_sets=[dict(case=x['case'],roots=x['roots'],fault_type=x['injection'].get('fault_type'),start=x['injection'].get('start_time'),end=x['injection'].get('end_time')) for x in summaries],root_count=len({r for x in valid for r in x['roots']}),fault_types=sorted({x['injection'].get('fault_type') for x in valid}),probe_rows=len(bands),scope='complete reduced artifact; not full paper',pyarrow_version=pa.__version__))
def anomod(path,o):
    files=[];cases=collections.defaultdict(dict);series={};z=zipfile.ZipFile(path)
    for m in z.infolist():
        n=m.filename
        if m.is_dir() or not n.startswith(('SN_data/','TT_data/')) or Path(n).name=='.DS_Store':continue
        parts=n.split('/');system,modality=parts[:2]
        if modality not in ('trace_data','metric_data','log_data','api_responses'):continue
        casepart=parts[2] if len(parts)>2 else ''
        match=re.match(r'(.*?202\d\d\d\d\d(?:T\d+Z(?:_em)?|_\d{6}))',casepart);case=match[1] if match else casepart
        key=(system,case);d=cases[key];d.setdefault('files',[]).append(n)
        if modality=='trace_data' and n.endswith('/all_traces.csv'):
            with z.open(m) as f:rows=list(csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig')))
            spans=[dict(trace=x['trace_id'],span=x['span_id'],parent=x['parent_span_id'],entity=x['service']) for x in rows];d['trace']=graph(spans,[]);d['trace_time_min']=min((x['start_time'] for x in rows),default=None);d['trace_time_max']=max((x['start_time'] for x in rows),default=None)
            d['_pairs']={(x['trace'],x['span']) for x in spans};d['_traceids']={x['trace'] for x in spans};files.append(dict(path=n,rows=len(rows),schema=list(rows[0]) if rows else []))
        elif modality=='trace_data' and system=='TT_data' and n.endswith('.json'):
            raw=json.loads(z.read(m))
            if not isinstance(raw,dict) or 'traces' not in raw:continue
            traces=raw['traces'];spans=[dict(trace=t.get('trace_id') or s.get('trace_id'),span=s['node_id'],parent=s.get('parent_node_id'),entity=s['service_code']) for t in traces for s in t['spans']];d['trace']=graph(spans,[]);d['collector_metadata']=raw.get('metadata');times=[s['start_timestamp_ms'] for t in traces for s in t['spans']];d['trace_time_min']=min(times,default=None);d['trace_time_max']=max(times,default=None);d['_pairs']={(x['trace'],x['span']) for x in spans};d['_traceids']={x['trace'] for x in spans};files.append(dict(path=n,traces=len(traces),rows=len(spans),schema=list(traces[0]['spans'][0]) if traces and traces[0]['spans'] else []))
        elif modality=='metric_data' and n.endswith('.csv'):
            with z.open(m) as f:rows=list(csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig')))
            headers=list(rows[0]) if rows else []
            entity=next((k for k in ('pod','kubernetes_pod_name','kubernetes_name','container','instance') if k in headers),'instance');tk=next((k for k in ('timestamp','time','Time') if k in headers),'timestamp');vk=next((k for k in ('value','Value') if k in headers),'value')
            ss,quality=numeric_series(rows,tk,vk,entity,'metric');files.append(dict(path=n,schema=headers,metric=quality));d['metric_files']=d.get('metric_files',0)+1;d['metric_rows']=d.get('metric_rows',0)+len(rows)
        elif modality=='log_data':
            # Only schema/line/ID presence; no log messages or credentials copied.
            count=0;sw=0
            with z.open(m) as f:
                for line in f:count+=1;sw+=b'SW_CTX' in line
            files.append(dict(path=n,lines=count,sw_ctx_lines=sw));d['log_files']=d.get('log_files',0)+1;d['log_lines']=d.get('log_lines',0)+count
        elif modality=='api_responses' and n.endswith('.jsonl'):
            count=0;columns=set()
            with z.open(m) as f:
                for line in f:
                    if line.strip():r=json.loads(line);count+=1;columns.update(r)
            files.append(dict(path=n,rows=count,top_level_columns=sorted(columns),payload_copied=False))
    z.close();out=[]
    for (system,case),d in cases.items():
        d.pop('_pairs',None);d.pop('_traceids',None);out.append(dict(system=system,case=case,**d))
    save(o,'files.json',files);save(o,'cases.json',out);save(o,'census.json',dict(by_system={s:dict(capture_names=len([x for x in out if x['system']==s]),trace_captures=sum('trace' in x for x in out if x['system']==s),baseline_names=[x['case'] for x in out if x['system']==s and 'normal' in x['case'].lower()]) for s in ('SN_data','TT_data')},root_gold_census=False,reason='case names are experiment hints, not independently bound per-incident root labels; collector config/run timestamp mapping must be verified before outside-root probe',all_input_files_inspected=True))
def main():
    p=argparse.ArgumentParser();p.add_argument('--kind',choices=['fse','anomod','inventory'],required=True);p.add_argument('--archive',required=True);p.add_argument('--run',required=True);a=p.parse_args();o=B/'runs'/a.run;o.mkdir(exist_ok=False);start=time.monotonic();path=Path(a.archive).resolve()
    try:
        inventory(path,o)
        if a.kind=='fse':fse(path,o)
        if a.kind=='anomod':anomod(path,o)
        save(o,'validation.json',dict(ok=True,seconds=time.monotonic()-start,no_pickle_or_vendor_code=True,bank_measurements_read=False))
    except Exception as e:save(o,'validation.json',dict(ok=False,error=repr(e),seconds=time.monotonic()-start));raise
if __name__=='__main__':main()
