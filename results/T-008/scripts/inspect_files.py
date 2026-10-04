"""Whole downloaded Nezha CSV audit; no RCA, no locked dataset access."""
import argparse, collections, concurrent.futures, csv, datetime as dt, hashlib, json, math, statistics, time
from pathlib import Path

parser=argparse.ArgumentParser();parser.add_argument('--run',required=True);args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[3]; BASE=ROOT/'data/ngoai-rcaeval/nezha';OUT=ROOT/'results/T-008/runs'/args.run;OUT.mkdir(exist_ok=False)
csv.field_size_limit(10_000_000)
started=time.monotonic()

def service(pod):
    parts=pod.rsplit('-',2)
    return parts[0] if len(parts)==3 else pod

def epoch_text(value):
    try:return dt.datetime.fromisoformat(value[:19]).replace(tzinfo=dt.timezone.utc).timestamp()
    except (ValueError,TypeError):return None

def readrows(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        yield from csv.DictReader(f)

def audit(path):
    relative=path.relative_to(BASE).as_posix(); info=dict(path=relative,bytes=path.stat().st_size,status='ok'); count=0
    try:
        with path.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f);info['columns']=reader.fieldnames
            if '/trace/' in relative:
                spans=collections.defaultdict(list);links=[];services=collections.Counter();time_min=None;time_max=None
                for row in reader:
                    count+=1;key=(row.get('TraceID'),row.get('SpanID'));pod=row.get('PodName','');spans[key].append(pod);links.append((row.get('TraceID'),row.get('ParentID'),pod));services[service(pod)]+=1
                    try:t=int(row['StartTimeUnixNano'])/1e9;time_min=t if time_min is None else min(time_min,t);time_max=t if time_max is None else max(time_max,t)
                    except (ValueError,KeyError):pass
                parent=collections.Counter();edges=collections.Counter()
                for tid,pid,pod in links:
                    if pid in ['root','','0','0000000000000000',None]:parent['root_sentinel']+=1;continue
                    matches=spans.get((tid,pid),[])
                    if not matches:parent['missing_within_file']+=1
                    elif len(matches)>1:parent['ambiguous_within_file']+=1
                    else:
                        parent['unique_resolved_within_file']+=1
                        a,b=service(matches[0]),service(pod)
                        if a!=b:edges[(a,b)]+=1
                info.update(parent=dict(parent),duplicate_span_keys=sum(len(v)-1 for v in spans.values()),services=dict(services),edges=[dict(parent=a,child=b,spans=n) for (a,b),n in sorted(edges.items())],start_epoch=time_min,end_epoch=time_max,trace_count=len({x[0] for x in spans}))
                counterpart=path.parent.parent/'log'/path.name.replace('_trace.csv','_log.csv');joined=collections.Counter()
                if counterpart.exists():
                    for row in readrows(counterpart):
                        joined['log_rows']+=1;tid=row.get('TraceID','');sid=row.get('SpanID','')
                        if tid:joined['trace_id_present']+=1
                        if sid:joined['span_id_present']+=1
                        n=len(spans.get((tid,sid),[]));joined['unique_span_link' if n==1 else 'ambiguous_span_link' if n>1 else 'missing_span_link']+=1
                info['paired_log']=dict(joined)
            elif '/metric/' in relative and path.name.endswith('_metric.csv'):
                finite=collections.Counter();invalid=collections.Counter();values=collections.defaultdict(list);times=[];offsets=collections.Counter();pods=collections.Counter()
                for row in reader:
                    count+=1;pods[row.get('PodName','')]+=1;t=epoch_text(row.get('Time',''));raw=row.get('TimeStamp','')
                    if t is not None:times.append(t)
                    try:
                        if t is not None:offsets[str(round(float(raw)-t,3))]+=1
                    except ValueError:pass
                    for key,value in row.items():
                        if key in ['Time','TimeStamp','PodName']:continue
                        try:
                            v=float(value)
                            if math.isfinite(v):finite[key]+=1;values[key].append(v)
                            else:invalid[key]+=1
                        except (ValueError,TypeError):invalid[key]+=1
                gaps=[b-a for a,b in zip(times,times[1:])];info.update(pods=dict(pods),timestamp_minus_time_text_seconds=dict(offsets),start_text_epoch=min(times) if times else None,end_text_epoch=max(times) if times else None,duplicate_text_times=len(times)-len(set(times)),nonincreasing_steps=sum(g<=0 for g in gaps),cadence_seconds=dict(collections.Counter(gaps)),numeric={k:dict(finite=finite[k],invalid=invalid[k],minimum=min(v),maximum=max(v),median=statistics.median(v),constant=min(v)==max(v)) for k,v in values.items()})
            else:
                ids=collections.Counter()
                for row in reader:
                    count+=1
                    for k in ['TraceID','SpanID','PodName']:
                        if row.get(k):ids[k]+=1
                info['nonempty_ids']=dict(ids)
        info['rows']=count
    except Exception as exc:info.update(status='error',rows=count,error=str(exc))
    (OUT/(hashlib.sha256(relative.encode()).hexdigest()+'.json')).write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(path=relative,status=info['status'],rows=count)),flush=True)
    return info

paths=sorted(BASE.rglob('*.csv'))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(audit,paths))
summary=dict(files=len(results),bytes=sum(r['bytes'] for r in results),rows=sum(r.get('rows',0) for r in results),errors=[r for r in results if r['status']!='ok'],elapsed_seconds=round(time.monotonic()-started,3),scope='all CSV physically acquired at run start, counts per file; missing parent within file may be boundary artifact',results=results)
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(0 if not summary['errors'] else 1)
