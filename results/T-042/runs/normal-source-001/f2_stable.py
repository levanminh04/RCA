"""Q191: exact arithmetic for descriptive F2, same five P3 metric observations."""
import csv, math, time
from fractions import Fraction
from collections import Counter
import run as task
B=task.BASE;R=task.ROOT

def stats(a):
    a=[float(x) for x in a if math.isfinite(float(x))];f=[Fraction.from_float(x) for x in a]
    if not f:return dict(n=0,mean=None,std=None,min=None,max=None),None,None
    mean=sum(f,Fraction())/len(f);var=sum(((x-mean)**2 for x in f),Fraction())/len(f)
    return dict(n=len(f),mean=float(mean),std=math.sqrt(float(var)),min=min(a),max=max(a)),mean,var

def main():
    folder=B/'F2-stable-001';folder.mkdir(exist_ok=False);start=time.perf_counter()
    task.write(folder/'invocation.json',dict(utc=task.now(),script_sha256=task.sha(__file__),indices_early=[0,1],indices_late=[3,4],arithmetic='exact Fraction from binary64; no epsilon or floors'))
    freeze=task.read(B/'full-001/diagnoses-frozen.json');assert freeze['completed'] and len(freeze['records'])==66
    pointers={r['opaque_id']:(R/r['path']).parent/'F2.json.gz' for r in freeze['records']}
    allow=task.nezha.nap_allowlist(R/'results/T-026/allowlist-dev.json');allrows=[];percase={};allcomparisons=[]
    for oid in sorted(allow):
        task.event(folder,'CASE_START',opaque_id=oid);selection=task.nezha.chon_ca(allow,oid,R);t=selection['t_ns'];old=task.read(pointers[oid])['metric'];arrays={};stamps={}
        for rel,item in sorted(selection['files'].items()):
            p=task.Path(item['absolute_path'])
            if p.parent.name!='metric':continue
            front=p.name=='front_service.csv';cols=task.nezha.FRONT_CHANNELS if front else task.nezha.RESOURCE_CHANNELS
            aliases=task.nezha.SERVICE_ALIASES if front else task.nezha.POD_ALIASES;idcol='ServiceName' if front else 'PodName';rows=[]
            with p.open(encoding='utf-8-sig',newline='') as f:
                for row in csv.DictReader(f):
                    ts=task.nezha.parse_time_ns(row['Time'])
                    if not t-300*task.NS<=ts<t:continue
                    assert row[idcol] in aliases
                    rows.append((ts,aliases[row[idcol]],row))
            rows.sort(key=lambda x:x[0]);assert len(rows)==5
            for original,suffix in cols.items():
                key=rows[0][1]+'_'+suffix;arrays[key]=[task.nezha._numeric(x[2][original]) for x in rows];stamps[key]=[x[0] for x in rows]
        assert set(arrays)==set(old) and len(arrays)==165
        output={};changes=0
        for key,values in arrays.items():
            e,em,_=stats(values[:2]);l,lm,_=stats(values[3:]);n,nm,var=stats(values)
            delta=float(lm-em) if lm is not None and em is not None else None
            norm=delta/math.sqrt(float(var)) if delta is not None and var else None
            assert norm is None or abs(norm)<=math.sqrt(5)*(1+1e-14)
            prev=old[key];assert stamps[key]==prev['timestamps_ns']
            for new,part in [(e,'early'),(l,'late'),(n,'all_normal')]:
                assert all(new[k]==prev[part][k] for k in ('n','min','max'))
            changes+=int(prev['delta_over_std']!=norm)
            output[key]=dict(early=e,late=l,all_normal=n,delta=delta,delta_over_std=norm,timestamps_ns=stamps[key])
            allrows.append(dict(opaque_id=oid,channel=key,**output[key]))
        task.write(folder/'cases'/(oid+'.json.gz'),dict(opaque_id=oid,metric=output,labels_read=False,raw_payload_saved=False))
        percase[oid]=dict(comparisons=165,normalized_lastbit_changes=changes)
        task.event(folder,'CASE_DONE',opaque_id=oid,compared=165);task.limit(start)
    defined=[abs(x['delta_over_std']) for x in allrows if x['delta_over_std'] is not None]
    summary=dict(case_channel_pairs=len(allrows),defined_normalized=len(defined),undefined_normalized=len(allrows)-len(defined),
                 median_abs_delta_over_std=float(task.np.median(defined)),p90_abs_delta_over_std=float(task.np.quantile(defined,.9)),max_abs_delta_over_std=max(defined),
                 positive_delta=sum(x['delta'] is not None and x['delta']>0 for x in allrows),negative_delta=sum(x['delta'] is not None and x['delta']<0 for x in allrows),zero_delta=sum(x['delta']==0 for x in allrows),
                 input_counts_times_minmax_match_old=True,all_normalized_within_Cauchy_bound=True,by_case=percase,
                 claim='descriptive change in five observations, not proof of recovery or source health; tiny changes may reflect recording precision')
    task.write(folder/'summary.json',summary);task.write(folder/'cost.json',dict(wall_s=time.perf_counter()-start,method_runs=0,raw_payload_saved=False))
    print(task.json.dumps(summary))
if __name__=='__main__':main()
