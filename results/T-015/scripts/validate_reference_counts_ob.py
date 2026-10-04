"""Audit RCAEval reference arithmetic without rerunning either RCA ranker."""
import argparse,json,pathlib,time
import pandas as pd
ap=argparse.ArgumentParser();ap.add_argument('--root',type=pathlib.Path,required=True);a=ap.parse_args();task=a.root
assert pd.__version__=='2.2.3'
out=task/'runs/ob-reference-audit';assert not out.exists();out.mkdir()
fixed={}
for name in ['ob-pilot-ec2-2','ob-block-1','ob-block-2','ob-block-3','ob-duplicate-rerun']:
    for p in (task/'runs'/name).glob('re2ob_*.json'):
        value=json.loads(p.read_text());case=value['case_id']
        if case not in fixed or value['status']=='ok':fixed[case]=value
assert len(fixed)==90 and all(v['status']=='ok' for v in fixed.values())
cols=['traceID','serviceName','methodName','operationName','startTime','duration']
results=[];begin=time.monotonic()
for case,saved in sorted(fixed.items()):
    p=task/'data'/case; tau=int((p/'inject_time.txt').read_text().strip())*1000000
    df=pd.read_parquet(p/'traces.parquet',columns=cols);df=df[(df.startTime>=tau-600000000)&(df.startTime<tau+600000000)].copy()
    df['operation']=df.serviceName+'_'+df.methodName.fillna(df.operationName)
    before=df[df.startTime+df.duration<tau];after=df[df.startTime+df.duration>=tau]
    # Exact arithmetic of RCAEval get_operation_slo, including original row
    # order and Python round; no author function, PageRank or ranking is called.
    stats={}
    for op in before.operation.dropna().unique():
        duration=before.loc[before.operation==op,'duration']
        stats[op]={'mean':float(round(duration.mean()/1000,2)), 'std':float(round(duration.std()/1000,2))}
    diffs={op:{'raw':v,'saved':saved['baseline_slo_ms'].get(op)} for op,v in stats.items() if op not in saved['baseline_slo_ms'] or any(v[k]!=saved['baseline_slo_ms'][op][k] for k in v)}
    threshold=after.operation.map({op:v['mean']+3*v['std'] for op,v in stats.items()})
    flags=after.duration/1000>=threshold
    normal=set(after.loc[~flags,'traceID']);anomaly=set(after.loc[flags,'traceID'])
    ref={'normal_count':len(normal),'anomaly_count':len(anomaly),'overlap':len(normal&anomaly),'before_graph_trace_count':int(before.traceID.nunique()),'after_graph_trace_count':int(after.traceID.nunique())}
    checks={'rounded_slo_exact':not diffs,'reference_counts_exact':all(v==saved['rcaeval_partition_reference'][k] for k,v in ref.items()),'flagged_span_count_exact':int(flags.sum())==saved['counts']['abnormal_spans']}
    row={'case':case,'checks':checks,'all_passed':all(checks.values()),'rounded_slo_differences':diffs,'reference_counts':ref}
    results.append(row);print(json.dumps({'case':case,'all_passed':row['all_passed']}),flush=True)
summary={'cases':results,'all_passed':all(r['all_passed'] for r in results),'scope':'Original row order and RCAEval SLO/flags arithmetic only; no ranker, no labels','baseline_ranker_not_rerun':True,'elapsed_observed_seconds':time.monotonic()-begin,'timing_official':False}
(out/'summary.json').write_text(json.dumps(summary,indent=2));assert summary['all_passed']
