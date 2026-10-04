"""Read only whitelisted OB measurements to validate the final input guard.

No ranker, labels, or root names enter this audit. Retains all row occurrences.
"""
import argparse,json,pathlib,time,hashlib
import pandas as pd
COLS=['traceID','spanID','parentSpanID','serviceName','methodName','operationName','startTime','duration']
a=argparse.ArgumentParser();a.add_argument('--data',type=pathlib.Path,required=True);a.add_argument('--out',type=pathlib.Path,required=True);args=a.parse_args()
assert pd.__version__=='2.2.3' and not args.out.exists()
args.out.mkdir(parents=True);results=[];begin=time.monotonic()
allowed=sorted('re2ob_'+f'{s}_{f}_{i}' for s in ['checkoutservice','currencyservice','emailservice','productcatalogservice','recommendationservice'] for f in ['cpu','mem','disk','socket','delay','loss'] for i in [1,2,3])
for case in allowed:
    p=args.data/case/'traces.parquet';tau=int((p.parent/'inject_time.txt').read_text().strip())*1000000
    df=pd.read_parquet(p,columns=COLS);df=df[(df.startTime>=tau-600000000)&(df.startTime<tau+600000000)]
    unique=df.drop_duplicates();conflicts=int(unique.duplicated(['traceID','spanID'],keep=False).sum())
    after=df[df.startTime+df.duration>=tau];copies=int(after.duplicated(['traceID','spanID']).sum())
    r={'case':case,'window_spans':len(df),'exact_row_copies':len(df)-len(unique),'conflicting_identity_rows':conflicts,'current_duplicate_occurrences':copies,'final_input_guard_passes':conflicts==0,'method_not_rerun':True}
    results.append(r);print(json.dumps(r),flush=True)
    (args.out/(case+'.json')).write_text(json.dumps(r,indent=2))
summary={'cases':results,'all_passed':all(r['final_input_guard_passes'] for r in results),'cases_with_current_duplicates':[r['case'] for r in results if r['current_duplicate_occurrences']],
         'retains_all_measurement_rows':True,'labels_not_read':True,'method_not_rerun':True,'elapsed_observed_seconds':time.monotonic()-begin,'timing_official':False}
(args.out/'summary.json').write_text(json.dumps(summary,indent=2));assert summary['all_passed']
