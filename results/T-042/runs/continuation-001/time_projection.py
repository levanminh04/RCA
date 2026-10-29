"""Source TimeStamp projection on already allowlisted native Time-selected rows only."""
import csv
from collections import defaultdict
import math
import time
import pandas as pd
import numpy as np
from simple_runner import ROOT, OUT, read, sha, write, load_kernels, tie_groups
from p3 import nezha


def metrics(selection, network, source_time):
    t=selection['t_ns'];lo=t-300*10**9;hi=t+300*10**9
    long=[];wide=[];audit=[]
    wanted={'CpuUsageRate(%)','MemoryUsageRate(%)','PodClientLatencyP90(s)','PodServerLatencyP90(s)','PodClientLatencyP99(s)','PodServerLatencyP99(s)'}
    for rel,meta in sorted(selection['files'].items()):
        if '/metric/' not in rel or rel.endswith('front_service.csv'):continue
        values=[]
        with nezha._open_source(meta) as stream:
            reader=csv.DictReader(stream)
            for row in reader:
                stamp=nezha.parse_time_ns(row['Time'])
                if not lo<=stamp<hi:continue
                service=nezha.POD_ALIASES[row['PodName']]
                assert rel.endswith('/'+row['PodName']+'_metric.csv')
                clock=int(row['TimeStamp'])*10**9
                values.append((stamp,clock,service,{k:nezha._numeric(row[k]) for k in nezha.RESOURCE_CHANNELS}))
        values.sort(key=lambda v:v[0]);assert len(values)==10 and sum(v[0]<t for v in values)==5
        saved=0
        for stamp,clock,service,numbers in values:
            at=clock if source_time else stamp
            if not lo<=at<hi:continue
            wide.append(dict(service_name=service,time=at,**numbers));saved+=1
            for k in wanted:long.append(dict(service_name=service,time=at,metric=k,value=numbers[k]))
        audit.append(dict(source=rel,sha256=meta['sha256'],selected_native_rows=10,retained_rows=saved,
                          timestamps=[dict(Time_ns=a,TimeStamp_ns=b) for a,b,_,_ in values],
                          unique_native_times=len({a for a,b,_,_ in values}),unique_source_times=len({b for a,b,_,_ in values})))
    long=pd.DataFrame(long);wide=pd.DataFrame(wide)
    ms={p:network(long.loc[(long.time<t) if p=='N' else (long.time>=t)].copy()) for p in ['N','A']}
    ws={p:wide.loc[(wide.time<t) if p=='N' else (wide.time>=t)].copy() for p in ['N','A']}
    return ms,ws,audit


def independent_metric(ms,scores):
    rows={}
    for service in ms['A'].service_name.unique():
        a=ms['A'].loc[ms['A'].service_name==service];n=ms['N'].loc[ms['N'].service_name==service]
        total=0;parts=[]
        for name,weight in [('Cpu|CPU',100),('Network_Latency',50),('Latency',20)]:
            matcha=(a.metric==name) if name=='Network_Latency' else a.metric.str.contains(name,case=False)
            if name=='Latency':matcha &= a.metric!='Network_Latency'
            matchn=(n.metric==name) if name=='Network_Latency' else n.metric.str.contains(name,case=False)
            av=a.loc[matcha,'value'].dropna();nv=n.loc[matchn,'value'].dropna()
            if not len(av):continue
            sample=nv if len(nv)>1 else av
            th=float(sample.mean()+6*sample.std()) if len(sample)>1 else float(sample.max())
            count=int(sum(av>th));total+=weight*count
            parts.append(dict(pattern=name,normal_n=len(nv),incident_n=len(av),threshold=th,count=count,weight=weight))
        assert scores[service]==total
        rows[service]=dict(score=total,pools=parts)
    return rows


def main():
    folder=OUT/'time-projection-001';folder.mkdir(exist_ok=False)
    write(folder/'config.json',dict(labels_read=False,source_clock='TimeStamp*1e9 exact generator expression',
        restriction='Only rows already selected by approved native Time window; projection never adds outside rows',
        source_plan='plan.json + supplementary WHY-54',script_sha256=sha(__file__),branches=['T-M0','T-M1','T-L0','T-L1','T-L2']))
    kernels,pins=load_kernels();ns,net,nz=kernels;write(folder/'source-pins.json',pins)
    allow=nezha.nap_allowlist(ROOT/'results/T-026/allowlist-dev.json')
    old={}
    for row in read(OUT/'simple-full-001/diagnoses-frozen.json')['records']:
        assert sha(ROOT/row['path'])==row['sha256'];old[(row['opaque_id'],row['branch'])]=read(ROOT/row['path'])['result']
    levels={}
    for row in read(OUT/'level-seed0-001/diagnoses-frozen.json')['records']:
        assert sha(ROOT/row['path'])==row['sha256'];levels[(row['opaque_id'],row['branch'])]=read(ROOT/row['path'])['result']
    records=[];started=time.perf_counter()
    for oid in sorted(allow):
        selection=nezha.chon_ca(allow,oid,ROOT)
        original,ow,oa=metrics(selection,net['calculate_network_latency'],False)
        projected,pw,pa=metrics(selection,net['calculate_network_latency'],True)
        om=ns['analyze_metrics'](original['A'],original['N'])
        assert om==old[(oid,'M0')]['components']['metric']
        op=nz['_detect_metric_anomalies'](ow['N'],ow['A']);assert op==old[(oid,'N1-partial')]['metric_ranks']
        sm=ns['analyze_metrics'](projected['A'],projected['N']);audit=independent_metric(projected,sm)
        pm=nz['_detect_metric_anomalies'](pw['N'],pw['A'])
        write(folder/f'{oid}-audit.json',dict(native_sources=oa,projected_sources=pa,metric_audit=audit,
                                            original_main_scores=om,projected_main_scores=sm,original_partial_metric_ranks=op,
                                            projected_partial_metric_ranks=pm,labels_read=False))
        for name in ['M0','M1','L0','L1','L2']:
            if name.startswith('M'):
                before=old[(oid,name)];scores=ns['combine_scores'](before['components']['log'],before['components']['trace'],sm,list(before['scores']))
                ranks=sorted(scores,key=lambda x:-scores[x]);scope='same log/trace scores; main metric TimeStamp projection'
            else:
                before=levels[(oid,name)];scores={}
                for nodes,weight in [(pm,1.2),(before['trace_ranks'],1.),(before['log_ranks'],1.)]:
                    for i,s in enumerate(nodes[:5]):scores[s]=scores.get(s,0)+(5-i)*weight
                ranks=nz['_vote_combine_results'](pm,before['trace_ranks'],before['log_ranks'])
                assert ranks==sorted(scores,key=lambda x:-scores[x])[:5]
                scope='same observed severity/log and physical trace ranks; Nezha metric TimeStamp projection'
            dest=folder/f'{oid}-T-{name}.json'
            write(dest,dict(opaque_id=oid,branch='T-'+name,result=dict(scores=scores,native_ranks=ranks,tie_groups=tie_groups(scores),scope=scope),labels_read=False,raw_payload_saved=False))
            records.append(dict(opaque_id=oid,branch='T-'+name,path=dest.relative_to(ROOT).as_posix(),sha256=sha(dest)))
    write(folder/'diagnoses-frozen.json',dict(records=records,completed=True,labels_read=False))
    write(folder/'cost.json',dict(wall_s=time.perf_counter()-started,records=len(records),raw_log_trace_reads=0))
    print('FROZEN',len(records))


if __name__=='__main__':main()
