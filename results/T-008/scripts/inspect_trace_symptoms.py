"""Raw trace duration deviations per pod/operation; descriptive only."""
import argparse,bisect,collections,csv,datetime as dt,json,math,statistics,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];BASE=ROOT/'data/ngoai-rcaeval/nezha';parser=argparse.ArgumentParser();parser.add_argument('--run',default='trace-symptoms-001');args=parser.parse_args();OUT=ROOT/'results/T-008/runs'/args.run;OUT.mkdir(exist_ok=False)
labels=json.loads((ROOT/'results/T-008/runs/run-001/labels.json').read_text());csv.field_size_limit(10_000_000)
def epoch(s):return dt.datetime.fromisoformat(s).replace(tzinfo=dt.timezone.utc).timestamp()
def quantile(values,q):
    v=sorted(values);p=(len(v)-1)*q;i=int(p);return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(p-i)
def records(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            try:t=int(r['StartTimeUnixNano'])/1e9;x=float(r['Duration'])
            except (KeyError,ValueError):continue
            if math.isfinite(x):yield t,r['PodName'],r['OperationName'],x
results=[];controls=[];group=[];began=time.monotonic()
for ds,sys in [('OB','online-boutique'),('TT','train-ticket')]:
    dates=sorted({l['date'] for l in labels if l['dataset']==ds})
    for date in dates:
        normal=BASE/sys/'construct_data'/date/'trace';fault=BASE/sys/'rca_data'/date/'trace';observations=collections.defaultdict(list)
        for p in sorted(normal.glob('*.csv')):
            for t,pod,op,x in records(p):observations[(pod,op)].append((t,x))
        refs={}
        for (pod,op),values in observations.items():
            v=sorted(values);cut=len(v)//2
            if cut<2 or len(v)-cut<2:continue
            train=[x for _,x in v[:cut]];test=[x for _,x in v[cut:]];med=statistics.median(train);delta=[abs(x-med) for x in train]
            for q in [.95,.99,.995]:
                band=quantile(delta,q);refs[(pod,op,q)]=(med,band)
                controls.append(dict(dataset=ds,date=date,pod=pod,operation=op,q=q,reference_n=len(train),control_n=len(test),zero_band=band==0,band=band,median=med,control_exceed=sum(abs(x-med)>band for x in test),reference_start=v[0][0],reference_end=v[cut-1][0],control_start=v[cut][0],control_end=v[-1][0]))
        ordered={};times={};aggregates=collections.defaultdict(collections.Counter);dropped=collections.Counter()
        for clock in ['text_as_utc','epoch']:
            ordered[clock]=sorted([l for l in labels if l['dataset']==ds and l['date']==date],key=lambda l:epoch(l['inject_time_raw']) if clock=='text_as_utc' else float(l['inject_timestamp_raw']))
            times[clock]=[epoch(l['inject_time_raw']) if clock=='text_as_utc' else float(l['inject_timestamp_raw']) for l in ordered[clock]]
        fault_rows=0
        for p in sorted(fault.glob('*.csv')):
            for t,pod,op,x in records(p):
                fault_rows+=1
                for clock in ordered:
                    idx=bisect.bisect_right(times[clock],t)-1
                    if idx<0:dropped[(clock,'before_first_injection')]+=1;continue
                    if (pod,op,.95) not in refs:
                        dropped[(clock,'no_normal_pod_operation_reference')]+=1;continue
                    for q in [.95,.99,.995]:
                        ref=refs.get((pod,op,q))
                        if ref is None:dropped[(clock,'no_normal_pod_operation_reference')]+=1;continue
                        med,band=ref;a=aggregates[(clock,idx,pod,op,q)];a['n']+=1;a['exceed']+=abs(x-med)>band
        for (clock,idx,pod,op,q),v in aggregates.items():
            l=ordered[clock][idx];service=pod.rsplit('-',2)[0]
            results.append(dict(dataset=ds,date=date,clock=clock,event_index=idx,root=l['service'],fault=l['fault'],pod=pod,service=service,operation=op,channel='raw_span_Duration',q=q,outside_root=service!=l['service'],**v))
        group.append(dict(dataset=ds,date=date,normal_rows=sum(len(v) for v in observations.values()),fault_rows=fault_rows,normal_pod_operations=len(observations),reference_pod_operations=len(refs)//3,dropped=[dict(clock=k[0],reason=k[1],count=n) for k,n in dropped.items()]))
        print(ds,date,'normal',group[-1]['normal_rows'],'fault',fault_rows,flush=True)
payload=dict(groups=group,calibration=controls,results=results,elapsed_seconds=round(time.monotonic()-began,3),scope='All source-designated normal and fault trace CSV, raw Duration per pod+operation, chrono first half reference and second half control, q95/99/99.5 abs deviation from median; root appended after measurement aggregation. Injection-to-next-injection only descriptive intervals, not onset or known failure ends. No OR across channels or propagation truth.',limitations='One short normal trace window/date; correlated spans and load/operation coverage may affect tails; native Duration units not converted until compared timestamps. Differences outside root do not establish causal propagation. Absent normal operation is missing reference, never zero score. Last injection interval includes later observed trace points, not confirmed failure duration.')
(OUT/'result.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
