import argparse,collections,csv,io,json,re,time,zipfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();data=Path(a.data);out=Path(a.out);out.mkdir(exist_ok=False,parents=True);start=time.monotonic()
rawids=set();normalraw=set()
for f in sorted(data.glob('TraceLogData/**/*.zip')):
    if 'alllog' in f.parts:continue
    with zipfile.ZipFile(f) as z:
        for m in z.infolist():
            if '__MACOSX' in m.filename or 'SpanData' not in m.filename or not m.filename.endswith('.csv'):continue
            with z.open(m) as src:
                ids={r['TraceId'] for r in csv.DictReader(io.TextIOWrapper(src,encoding='utf-8-sig',newline=''))};rawids.update(ids)
                if 'normal' in f.parts:normalraw.update(ids)
print('raw span ID inventory complete',flush=True)
logs=set()
with zipfile.ZipFile(data/'TraceLogData/alllog/alllog-combined.zip') as z,z.open('alllog.log') as src:
    for line in io.TextIOWrapper(src,encoding='utf-8'):
        m=re.search(r'\[SW_CTX:\[([^\]]+)\]\]',line)
        if m:
            fields=m[1].split(',')
            if len(fields)>=5:logs.add(fields[2])
print('alllog ID inventory complete',flush=True)
cells=collections.defaultdict(collections.Counter);checks=collections.Counter()
with zipfile.ZipFile(data/'GraphData/graph_data-combined.zip') as z:
    for m in z.infolist():
        if not m.filename.endswith('.jsons'):continue
        with z.open(m) as src:
            for line in src:
                if not line.strip():continue
                r=json.loads(line);t=r['trace_id'];c=cells[r['error_trace_type']];c['graph']+=1;c['in_raw_span']+=t in rawids;c['in_raw_normal_span']+=t in normalraw;c['in_alllog']+=t in logs;c['raw_and_log']+=t in rawids and t in logs;c['raw_without_log']+=t in rawids and t not in logs;c['log_without_raw']+=t in logs and t not in rawids;c['neither_raw_nor_log']+=t not in rawids and t not in logs
for label,c in cells.items():assert c['raw_and_log']+c['raw_without_log']+c['log_without_raw']+c['neither_raw_nor_log']==c['graph']
summary=dict(raw_unique_trace_ids=len(rawids),normal_raw_unique_trace_ids=len(normalraw),alllog_unique_trace_ids=len(logs),graph_labels=len(cells),total_graphs=sum(c['graph'] for c in cells.values()),normal_graph_raw_span_missing=cells['normal']['log_without_raw']+cells['normal']['neither_raw_nor_log'],normal_graph_raw_span_missing_with_alllog=cells['normal']['log_without_raw'],normal_graph_raw_span_missing_without_alllog=cells['normal']['neither_raw_nor_log'],elapsed_seconds=round(time.monotonic()-start,3),all_balances_ok=True,note='Graph normal is trace-level label; presence alllog does not recover absent span or certify clean continuous normal/injection clock')
(out/'per-label-coverage.json').write_text(json.dumps({k:dict(v) for k,v in sorted(cells.items())},indent=2),encoding='utf-8');(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary),flush=True)
