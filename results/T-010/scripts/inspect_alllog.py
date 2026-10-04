"""Join approved split archive, stream complete log, compare trace-ID coverage."""
import argparse,collections,hashlib,io,json,re,time,zipfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();data=Path(a.data);out=Path(a.out);out.mkdir(exist_ok=False,parents=True);started=time.monotonic()
parts=sorted((data/'TraceLogData/alllog').glob('alllog.zip.[0-9][0-9][0-9]'));assert len(parts)==5
combined=data/'TraceLogData/alllog/alllog-combined.zip';h=hashlib.sha256()
if not combined.exists():
    with combined.open('xb') as dst:
        for p in parts:
            with p.open('rb') as src:
                for b in iter(lambda:src.read(1024*1024),b''):dst.write(b)
with combined.open('rb') as src:
    for b in iter(lambda:src.read(1024*1024),b''):h.update(b)
graph={}
with zipfile.ZipFile(data/'GraphData/graph_data-combined.zip') as z:
    for i in z.infolist():
        if i.filename.endswith('.jsons'):
            with z.open(i) as src:
                for line in src:
                    if line.strip():r=json.loads(line);graph[r['trace_id']]=r['trace_bool']
records=[];ids=set();total=collections.Counter();schemas=[]
with zipfile.ZipFile(combined) as z:
    inventory=[dict(member=i.filename,bytes=i.file_size,compressed_bytes=i.compress_size) for i in z.infolist()]
    print(json.dumps({'inventory':inventory}),flush=True)
    for i in z.infolist():
        if i.is_dir() or '__MACOSX' in i.filename or Path(i.filename).name.startswith('.'):continue
        counts=collections.Counter();levels=collections.Counter();svc=collections.Counter();mh=hashlib.sha256();minclock=maxclock=None;prev=None
        with z.open(i) as src:
            for line in src:
                mh.update(line);counts['lines']+=1;text=line.decode('utf-8',errors='replace')
                if counts['lines']==1:schemas.append(dict(member=i.filename,first_line_field_shape='SW_CTX log text' if '[SW_CTX:' in text else 'other',first_line_chars=len(text)))
                m=re.search(r'\[SW_CTX:\[([^\]]+)\]\]',text)
                if m:
                    fields=m.group(1).split(',');counts['context_lines']+=1
                    if len(fields)>=5:
                        service,_,tid,segment,sid=fields[:5];ids.add(tid);svc[service]+=1;counts['in_graph_normal']+=graph.get(tid) is True;counts['in_graph_abnormal']+=graph.get(tid) is False;counts['not_in_graph']+=tid not in graph
                lev=re.search(r'\]\s+(TRACE|DEBUG|INFO|WARN|ERROR)\s',text)
                if lev:levels[lev[1]]+=1
                mt=re.match(r'(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+)',text)
                if mt:
                    ts=mt[1];minclock=ts if minclock is None else min(minclock,ts);maxclock=ts if maxclock is None else max(maxclock,ts);counts['descending_adjacent']+=prev is not None and ts<prev;prev=ts
        records.append(dict(member=i.filename,sha256=mh.hexdigest(),counts=dict(counts),levels=dict(levels),services=dict(svc),min_clock_text=minclock,max_clock_text=maxclock));total.update(counts)
        print(json.dumps({'member':i.filename,'lines':counts['lines']}),flush=True)
    assert z.testzip() is None
missing=[tid for tid in graph if tid not in ids]
summary=dict(split_parts=5,compressed_bytes=sum(p.stat().st_size for p in parts),combined_sha256=h.hexdigest(),all_members_crc_ok=True,member_count=len(inventory),log_counts=dict(total),unique_context_trace_ids=len(ids),graph_ids_covered=len(set(graph)&ids),graph_normal_ids_covered=sum(graph[t] is True for t in set(graph)&ids),graph_abnormal_ids_covered=sum(graph[t] is False for t in set(graph)&ids),graph_ids_missing_log=len(missing),normal_graph_ids_missing_log=sum(graph[t] is True for t in missing),abnormal_graph_ids_missing_log=sum(graph[t] is False for t in missing),elapsed_seconds=round(time.monotonic()-started,3),no_model_execution=True,note='ID presence links modality but does not provide raw span coverage, root label, clock alignment or incident normal provenance')
for name,v in [('summary',summary),('members',records),('archive-directory',inventory),('schema',schemas)]:
    (out/(name+'.json')).write_text(json.dumps(v,indent=2),encoding='utf-8')
print(json.dumps(summary),flush=True)
