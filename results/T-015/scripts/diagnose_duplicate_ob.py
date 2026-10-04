import hashlib,json,pathlib,time
import pandas as pd
task=pathlib.Path.home()/'rca/T-015';out=task/'runs/duplicate-input-audit';out.mkdir(parents=True,exist_ok=True)
summary=[]
for case in ['re2ob_recommendationservice_loss_1','re2ob_recommendationservice_loss_2']:
    started=time.monotonic();source=task/'data'/case/'traces.parquet';raw=pd.read_parquet(source)
    incident=int((source.parent/'inject_time.txt').read_text())*1000000
    df=raw[(raw.startTime>=incident-600000000)&(raw.startTime<incident+600000000)]
    duplicated=df[df.duplicated(['traceID','spanID'],keep=False)]
    counts=duplicated.groupby(['traceID','spanID'],dropna=False).size()
    distinct=duplicated.drop_duplicates().groupby(['traceID','spanID'],dropna=False).size()
    conflicts=distinct[distinct>1]
    changing={}
    for column in df.columns:
        n=duplicated.groupby(['traceID','spanID'],dropna=False)[column].nunique(dropna=False)
        changing[column]=int((n>1).sum())
    r={'case':case,'source':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'all_source_columns':list(df.columns),'raw_rows':len(raw),'window_rows':len(df),'duplicate_rows':len(duplicated),'duplicate_span_keys':len(counts),'exact_duplicate_keys':int((distinct==1).sum()),'conflicting_span_keys':len(conflicts),'column_conflict_counts':changing,'all_duplicate_groups_identical':len(conflicts)==0,'whole_row_copies_removed_if_dedup':len(df)-len(df.drop_duplicates()),'timing_official':False,'elapsed_observed_seconds':time.monotonic()-started}
    (out/(case+'.json')).write_text(json.dumps(r,indent=2));summary.append(r)
    print(json.dumps(r),flush=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2))
