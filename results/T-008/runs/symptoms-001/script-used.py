"""Descriptive metric deviations; not anomaly labels or an RCA method."""
import csv,datetime as dt,json,math,statistics,time
from collections import defaultdict,Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];BASE=ROOT/'data/ngoai-rcaeval/nezha';OUT=ROOT/'results/T-008/runs/symptoms-001';OUT.mkdir(exist_ok=False)
labels=json.loads((ROOT/'results/T-008/runs/run-001/labels.json').read_text())
CHANNELS=['CpuUsageRate(%)','MemoryUsageRate(%)','PodClientLatencyP90(s)','PodServerLatencyP90(s)','PodWorkload(Ops)','PodSuccessRate(%)']
def epoch(s):return dt.datetime.fromisoformat(s[:19]).replace(tzinfo=dt.timezone.utc).timestamp()
def svc(p):return p.rsplit('-',2)[0]
def quantile(v,q):
    v=sorted(v);pos=(len(v)-1)*q;i=int(pos);return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(pos-i)
def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            try:t=epoch(r['Time'])
            except (ValueError,KeyError):continue
            vals={}
            for k in CHANNELS:
                try:
                    x=float(r[k])
                    if math.isfinite(x):vals[k]=x
                except (ValueError,KeyError):pass
            yield t,r['PodName'],vals
started=time.monotonic();grouped=defaultdict(list)
for l in labels:grouped[(l['dataset'],l['date'])].append(l)
results=[];calibration=[]
for (dataset,date),events in sorted(grouped.items()):
    system='online-boutique' if dataset=='OB' else 'train-ticket';normal=BASE/system/'construct_data'/date/'metric';fault=BASE/system/'rca_data'/date/'metric'
    if not normal.exists() or not fault.exists():continue
    references={};samples=defaultdict(list)
    for p in sorted(normal.glob('*_metric.csv')):
        for t,pod,v in rows(p):
            for k,x in v.items():samples[(pod,k)].append((t,x))
    for (pod,k),v in samples.items():
        ordered=sorted(v);cut=len(ordered)//2;train=[x for _,x in ordered[:cut]];control=[x for _,x in ordered[cut:]]
        if len(train)<2 or len(control)<2:continue
        med=statistics.median(train);deviations=[abs(x-med) for x in train]
        for q in [.95,.99,.995]:
            band=quantile(deviations,q);references[(pod,k,q)]=(med,band)
            calibration.append(dict(dataset=dataset,date=date,pod=pod,channel=k,q=q,reference_n=len(train),control_n=len(control),median=med,band=band,zero_band=band==0,control_exceed=sum(abs(x-med)>band for x in control),reference_start=ordered[0][0],reference_end=ordered[cut-1][0],control_start=ordered[cut][0],control_end=ordered[-1][0]))
    faults=defaultdict(list)
    for p in sorted(fault.glob('*_metric.csv')):
        for t,pod,v in rows(p):faults[pod].append((t,v))
    # Two clock interpretations are retained separately; neither is auto-corrected.
    for interpretation in ['inject_text_as_utc','inject_epoch']:
        timing=lambda l:epoch(l['inject_time_raw']) if interpretation=='inject_text_as_utc' else float(l['inject_timestamp_raw'])
        ordered=sorted(events,key=timing)
        final=max((t for seq in faults.values() for t,_ in seq),default=0)+.001
        for i,l in enumerate(ordered):
            begin=timing(l);end=timing(ordered[i+1]) if i+1<len(ordered) else final
            for q in [.95,.99,.995]:
                for pod,seq in sorted(faults.items()):
                    for k in CHANNELS:
                        ref=references.get((pod,k,q));v=[x[k] for t,x in seq if begin<=t<end and k in x]
                        if not ref:continue
                        med,band=ref
                        results.append(dict(dataset=dataset,date=date,event_index=i,root=l['service'],fault=l['fault'],clock_interpretation=interpretation,begin=begin,end=end,pod=pod,service=svc(pod),outside_root=svc(pod)!=l['service'],channel=k,q=q,n=len(v),exceed=sum(abs(x-med)>band for x in v),zero_band=band==0))
    print(dataset,date,'reference_channels',len(samples),'rows',len(results),flush=True)
result=dict(channels=CHANNELS,calibration=calibration,results=results,elapsed_seconds=round(time.monotonic()-started,3),scope='All downloaded resource metric CSVs for four dates; normal first half reference, second half control. Post-injection until next injection is only descriptive interval, not onset/failure duration or region truth. Last interval capped at actual fault metric end. Clock hypotheses separated; no auto correction; no OR across channels.',warning='Published normal designation is not proof of clean recovery/load stationarity; excess may arise from common load, contamination, missing samples or clocks, not propagation causality.')
(OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
