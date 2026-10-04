"""DeepTraLog raw/graph lineage, corrected E-by-2 edges, scoped trace IDs."""
import argparse,collections,csv,hashlib,io,json,time,zipfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic();data=Path(a.data)
rawids=collections.defaultdict(set);normalids=set();normalcases=set();rawrows=[]
for f in sorted(data.glob('TraceLogData/**/*.zip')):
    normal='normal' in f.parts
    with zipfile.ZipFile(f) as z:
        for m in z.infolist():
            if '__MACOSX' in m.filename or Path(m.filename).name.startswith('.') or 'SpanData' not in m.filename or not m.filename.endswith('.csv'):continue
            case=Path(m.filename).parent.name;counts=collections.Counter();ids=set()
            with z.open(m) as src:
                for r in csv.DictReader(io.TextIOWrapper(src,encoding='utf-8-sig',newline='')):ids.add(r['TraceId']);counts[r.get('IsError','MISSING')]+=1
            rawids[case].update(ids)
            if normal:normalids.update(ids);normalcases.add(case)
            rawrows.append(dict(archive=str(f.relative_to(data)),member=m.filename,case=case,trace_ids=len(ids),span_is_error=dict(counts)))
    print('raw ids',f.name,flush=True)
allraw=set().union(*rawids.values());gid=set();graphrows=[];labelcase=collections.Counter();crossnormal=0;abnormalnormal=0;badlabel=0;duplicates=0;lineagecounts=collections.Counter();examples=[]
with zipfile.ZipFile(data/'GraphData/graph_data-combined.zip') as z:
    for m in z.infolist():
        if not m.filename.endswith('.jsons'):continue
        count=collections.Counter();schemas=collections.Counter();labels=collections.Counter();errors=collections.Counter();nodewidths=collections.Counter();edgeattrs=collections.Counter();h=hashlib.sha256()
        with z.open(m) as src:
            for line in src:
                h.update(line)
                if not line.strip():continue
                r=json.loads(line);count['graphs']+=1;t=r['trace_id'];lb=r['trace_bool'];fault=r['error_trace_type'];schemas[tuple(sorted(r))]+=1;labels[str(lb)]+=1;errors[fault]+=1
                duplicates+=t in gid;gid.add(t);badlabel+=type(lb) is not bool or (lb!=(fault=='normal'))
                count['nodes']+=len(r['node_info']);nodewidths.update(len(n) for n in r['node_info']);edgeattrs.update(map(str,r['edge_attr']))
                for pair in r['edge_index']:
                    count['edges']+=1
                    if len(pair)!=2:count['bad_edge_shape']+=1;continue
                    count['bad_edge_indices']+=any(type(j) is not int or j<0 or j>=len(r['node_info']) for j in pair)
                count['edge_attr_length_mismatch']+=len(r['edge_index'])!=len(r['edge_attr'])
                if t in allraw:lineagecounts['graph_trace_in_raw']+=1
                else:lineagecounts['graph_trace_absent_raw']+=1
                if fault!='normal':
                    labelcase[fault]+=1
                    if t in rawids.get(fault,set()):lineagecounts['abnormal_trace_in_named_case']+=1
                    else:lineagecounts['abnormal_trace_absent_named_case']+=1
                    abnormalnormal+=t in normalids
                else:crossnormal+=t in normalids
                if len(examples)<3:examples.append(dict(trace_id=t,trace_bool=lb,error_trace_type=fault,node_info_first=r['node_info'][:3],edge_index_first=r['edge_index'][:3]))
        graphrows.append(dict(member=m.filename,sha256=h.hexdigest(),counts=dict(count),trace_bool=dict(labels),error_trace_type=dict(errors),schemas=[dict(keys=list(k),count=v) for k,v in schemas.items()],node_width_histogram=dict(nodewidths),edge_attr_histogram=dict(edgeattrs)))
        (out/'graph-audit.json').write_text(json.dumps(graphrows,indent=2),encoding='utf-8');print('graph',m.filename,count['graphs'],flush=True)
summary=dict(unique_raw_trace_ids=len(allraw),unique_normal_trace_ids=len(normalids),normal_cases=sorted(normalcases),raw_case_trace_counts={k:len(v) for k,v in rawids.items()},graph_records=sum(r['counts']['graphs'] for r in graphrows),graph_unique_trace_ids=len(gid),graph_duplicate_trace_ids=duplicates,graph_total_nodes=sum(r['counts']['nodes'] for r in graphrows),graph_total_edges=sum(r['counts']['edges'] for r in graphrows),graph_bad_edges=sum(r['counts'].get('bad_edge_indices',0)+r['counts'].get('bad_edge_shape',0) for r in graphrows),edge_attr_length_mismatch=sum(r['counts']['edge_attr_length_mismatch'] for r in graphrows),label_inconsistent=badlabel,normal_graph_in_raw_normal=crossnormal,abnormal_graph_in_raw_normal=abnormalnormal,lineage=dict(lineagecounts),abnormal_case_counts=dict(labelcase),graph_cases_not_raw=sorted(set(labelcase)-set(rawids)),raw_cases_without_abnormal_graph=sorted(k for k in rawids if k not in normalcases and k not in labelcase),elapsed_seconds=round(time.monotonic()-start,3),supersedes='inspect-002 graph edges_total and bad_edge_indices only; old edge shape assumption incorrect',no_root_service_mapping=True,no_timestamp_graph=True)
for n,v in [('raw-id-census',rawrows),('graph-audit',graphrows),('graph-examples',examples),('summary',summary)]:
    (out/(n+'.json')).write_text(json.dumps(v,indent=2),encoding='utf-8')
print(json.dumps(summary),flush=True)
