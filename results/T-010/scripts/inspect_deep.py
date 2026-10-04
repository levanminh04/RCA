"""Streaming full raw CSV/log and JSON graph audit; no model execution."""
import argparse, collections, csv, datetime, hashlib, io, json, re, time, zipfile
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--out',required=True);a=p.parse_args()
out=Path(a.out);out.mkdir(exist_ok=False,parents=True);started=time.monotonic()
csv.field_size_limit(10000000)
rows=[];checks=[]
for f in sorted(Path(a.data).glob('TraceLogData/**/*.zip')):
    begin=time.monotonic()
    with zipfile.ZipFile(f) as z:
        valid=[i for i in z.infolist() if not i.is_dir() and not i.filename.startswith('__MACOSX') and not Path(i.filename).name.startswith('.')]
        groups=collections.defaultdict(list)
        for i in valid:groups[str(Path(i.filename).parent)].append(i)
        for group,infos in sorted(groups.items()):
            keys={};refs=[];traces=set();services=collections.Counter();types=collections.Counter();errors=collections.Counter();headers=[];times=[];badtime=0;null=0;span_rows=0;duplicate_rows=0
            for i in infos:
                if 'SpanData' not in i.filename or not i.filename.endswith('.csv'):continue
                with z.open(i) as raw:
                    reader=csv.DictReader(io.TextIOWrapper(raw,encoding='utf-8-sig',errors='replace',newline=''));headers.append(reader.fieldnames)
                    for r in reader:
                        span_rows+=1;t=r.get('TraceId','');s=r.get('SpanId','');service=r.get('Service','');parent=r.get('ParentSpan','');key=(t,s)
                        if not t or not s:null+=1
                        if key in keys:duplicate_rows+=1;keys[key]=(keys[key][0]+1,keys[key][1])
                        else:keys[key]=(1,service)
                        traces.add(t);services[service]+=1;types[r.get('SpanType','')]+=1;errors[r.get('IsError','MISSING')]+=1
                        refs.append((t,parent,service))
                        try:
                            st=int(r['StartTime']);et=int(r['EndTime']);times.extend([st,et]);badtime+=et<st
                        except (ValueError,KeyError):badtime+=1
            counts=collections.Counter();edges=collections.Counter()
            for t,parent,service in refs:
                if parent in ('-1','',None):counts['sentinel_root']+=1;continue
                counts['parent_required']+=1;match=keys.get((t,parent))
                if match is None:counts['parent_missing']+=1
                elif match[0]!=1:counts['parent_ambiguous']+=1
                else:
                    counts['parent_unique']+=1
                    if match[1]!=service:edges[(match[1],service)]+=1
            logs=[]
            for i in infos:
                if not i.filename.endswith('.log'):continue
                n=ctx=tm=sm=0;levels=collections.Counter();logservices=collections.Counter();clock_min=clock_max=None;reverse=0;previous=None
                with z.open(i) as raw:
                    for line in io.TextIOWrapper(raw,encoding='utf-8',errors='replace'):
                        n+=1;m=re.search(r'\[SW_CTX:\[([^\]]+)\]\]',line)
                        if m:
                            fields=m.group(1).split(',');ctx+=1
                            if len(fields)>=5:
                                svc,_,tid,segment,sid=fields[:5];logservices[svc]+=1;tm+=tid in traces;sm+=(tid,segment+'.'+sid) in keys
                        lev=re.search(r'\]\s+(TRACE|DEBUG|INFO|WARN|ERROR)\s',line)
                        if lev:levels[lev.group(1)]+=1
                        mt=re.match(r'(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+)',line)
                        if mt:
                            stamp=mt.group(1);clock_min=stamp if clock_min is None else min(clock_min,stamp);clock_max=stamp if clock_max is None else max(clock_max,stamp)
                            reverse+=previous is not None and stamp<previous;previous=stamp
                logs.append(dict(member=i.filename,lines=n,context_lines=ctx,trace_matches=tm,span_matches=sm,services=dict(logservices),levels=dict(levels),clock_min=clock_min,clock_max=clock_max,descending_adjacent=reverse))
            row=dict(archive=str(f.relative_to(a.data)),case_directory=group,span_rows=span_rows,unique_span_keys=len(keys),duplicate_span_rows=duplicate_rows,null_id_rows=null,trace_ids=len(traces),headers=headers,services=dict(services),span_types=dict(types),is_error_values=dict(errors),time_min_ms=min(times) if times else None,time_max_ms=max(times) if times else None,invalid_time_rows=badtime,parent=dict(counts),service_edges=[dict(parent=k[0],child=k[1],count=v) for k,v in sorted(edges.items())],logs=logs,root_label_verified=False,injection_onset_verified=False)
            rows.append(row)
            assert counts['sentinel_root']+counts['parent_required']==span_rows
            assert counts['parent_unique']+counts['parent_missing']+counts['parent_ambiguous']==counts['parent_required']
        # Full payload CRC for all members, including structured/ancillary data.
        bad=z.testzip();assert bad is None
        checks.append(dict(archive=str(f.relative_to(a.data)),crc_all_members_ok=True,members=len(z.infolist()),elapsed_seconds=round(time.monotonic()-begin,3)))
    (out/'raw-cases.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    (out/'crc.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    print(json.dumps({'archive':str(f),'seconds':round(time.monotonic()-begin,2)}),flush=True)
graph=[]
f=Path(a.data)/'GraphData/graph_data-combined.zip'
with zipfile.ZipFile(f) as z:
    for i in z.infolist():
        if not i.filename.endswith('.jsons'):continue
        n=0;labels=collections.Counter();error_types=collections.Counter();schemas=collections.Counter();traceids=set();nodes=edges_n=bad_indices=missing=0
        with z.open(i) as raw:
            for line in io.TextIOWrapper(raw,encoding='utf-8'):
                if not line.strip():continue
                r=json.loads(line);n+=1;schemas[tuple(sorted(r))]+=1;labels[str(r.get('trace_bool','MISSING'))]+=1;error_types[str(r.get('error_trace_type','MISSING'))]+=1
                if 'trace_id' in r:traceids.add(str(r['trace_id']))
                else:missing+=1
                nodes+=len(r.get('node_info',[]));ei=r.get('edge_index',[])
                if len(ei)==2 and isinstance(ei[0],list):
                    edges_n+=len(ei[0]);bad_indices+=len(ei[0])!=len(ei[1]);bad_indices+=sum(j<0 or j>=len(r.get('node_info',[])) for arr in ei for j in arr)
        graph.append(dict(member=i.filename,graphs=n,trace_ids=len(traceids),missing_trace_id=missing,trace_bool=dict(labels),error_trace_type=dict(error_types),schemas=[dict(keys=list(k),count=v) for k,v in schemas.items()],nodes_total=nodes,edges_total=edges_n,bad_edge_indices=bad_indices))
        (out/'graph.json').write_text(json.dumps(graph,indent=2),encoding='utf-8');print(i.filename,n,flush=True)
    assert z.testzip() is None
summary=dict(raw_case_directories=len(rows),span_rows=sum(x['span_rows'] for x in rows),graph_count=sum(x['graphs'] for x in graph),raw_archives_crc_verified=len(checks),graph_crc_verified=True,elapsed_seconds=round(time.monotonic()-started,3),root_labels_verified=False,note='case directory is storage unit; graph trace_bool is trace label, not root/onset; raw-processed ID lineage not yet crosschecked')
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary),flush=True)
