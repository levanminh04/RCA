"""File quality and descriptive quantile survey, not an RCA/detection method."""
import collections, csv, hashlib, json, pathlib, re, sys, time
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from acquire import ROOT, OUT, DATA, REV, dump, csvout, hashcheck
QS=(.95,.99,.995)

def survey(frame, boundary):
    # No root, fault, case name or path enters this calculation.
    f=frame.sort_values('time');pre=f.loc[f.time<boundary];post=f.loc[f.time>=boundary]
    cut=2*len(pre)//3; ref=pre.iloc[:cut];ctrl=pre.iloc[cut:]
    periods={'pre':len(pre),'reference':len(ref),'control':len(ctrl),'post':len(post)}
    assert len(ref)+len(ctrl)==len(pre)
    if len(ref)<30 or len(ctrl)<10 or len(post)<10:return [],[],{**periods,'status':'insufficient_rows'}
    num=[c for c in f.select_dtypes('number') if c!='time']
    finite=lambda s:s.replace([np.inf,-np.inf],np.nan)
    channel=[];entity=[]
    for q in QS:
        cf={};pf={};cv={};pv={}
        for c in num:
            rv=finite(ref[c]).dropna()
            if len(rv)<30:continue
            center=float(rv.median());band=float((rv-center).abs().quantile(q))
            a=finite(ctrl[c]);b=finite(post[c]);cv[c]=a.notna();pv[c]=b.notna()
            cf[c]=((a-center).abs()>band)&cv[c];pf[c]=((b-center).abs()>band)&pv[c]
            channel.append({'metric':c,'entity':c.rsplit('_',1)[0] if '_' in c else 'UNMAPPED','kind':c.rsplit('_',1)[-1],'q':q,'reference_valid':len(rv),'center':center,'band':band,'flat_band':band==0,'control_valid':int(cv[c].sum()),'post_valid':int(pv[c].sum()),'control_exceed':int(cf[c].sum()),'post_exceed':int(pf[c].sum()),'control_rate':float(cf[c].sum()/cv[c].sum()) if cv[c].any() else None,'post_rate':float(pf[c].sum()/pv[c].sum()) if pv[c].any() else None})
        entities=sorted({c.rsplit('_',1)[0] for c in num if '_' in c})
        for e in entities:
            own=[c for c in cf if c.rsplit('_',1)[0]==e]
            groups={'all_metrics':own,'latency90':[c for c in own if c.endswith('_latency-90')],'cpu':[c for c in own if c.endswith('_cpu')],'mem':[c for c in own if c.endswith('_mem')],'workload':[c for c in own if c.endswith('_workload')],'error':[c for c in own if c.endswith('_error')]}
            for group,cols in groups.items():
                if not cols:continue
                ac=pd.concat([cf[c] for c in cols],axis=1).any(axis=1);ap=pd.concat([pf[c] for c in cols],axis=1).any(axis=1)
                vc=pd.concat([cv[c] for c in cols],axis=1).any(axis=1);vp=pd.concat([pv[c] for c in cols],axis=1).any(axis=1)
                cr=float(ac.sum()/vc.sum()) if vc.any() else None;pr=float(ap.sum()/vp.sum()) if vp.any() else None
                if cr is not None:assert 0<=cr<=1
                if pr is not None:assert 0<=pr<=1
                entity.append({'entity':e,'group':group,'q':q,'channels':len(cols),'control_valid':int(vc.sum()),'post_valid':int(vp.sum()),'control_exceed':int(ac.sum()),'post_exceed':int(ap.sum()),'control_rate':cr,'post_rate':pr,'difference':pr-cr if pr is not None and cr is not None else None})
    return channel,entity,{**periods,'status':'descriptive_only'}

def main():
    start=time.monotonic();run=OUT/'inspection';run.mkdir(exist_ok=False)
    plan=json.loads((OUT/'download-plan.json').read_text());entries={e['path']:e for e in plan['files']}
    with (OUT/'census-cases.csv').open(encoding='utf-8') as f:cases=list(csv.DictReader(f))
    bounds=[];qualities=[];channels=[];entities=[];schemas={};rootlabels=[];checks=[]
    for i,r in enumerate(cases,1):
        case=r['case'];p=DATA/case;inject=int((p/'inject_time.txt').read_text());detail={'case':case,'dataset':r['dataset'],'root':r['root'],'fault':r['fault'],'injection':inject}
        for path in p.iterdir():
            key=f'{case}/{path.name}';ch=hashcheck(path.read_bytes(),entries[key]);assert ch['valid'];checks.append({'path':key,**ch})
        m=pd.read_parquet(p/'metrics.parquet'); ts=m['time'];valid=ts.dropna()
        off0=float(valid.min()-inject);off1=float(valid.max()-inject)
        b={'case':case,'dataset':r['dataset'],'modality':'metric','rows':len(m),'min_epoch':float(valid.min()),'max_epoch':float(valid.max()),'start_minus_injection':off0,'end_minus_injection':off1,'midpoint_minus_injection':(off0+off1)/2,'pre_rows':int((ts<inject).sum()),'post_rows':int((ts>=inject).sum()),'null_time':int(ts.isna().sum()),'duplicate_time':int(ts.dropna().duplicated().sum()),'median_step':float(valid.sort_values().diff().median())}
        bounds.append(b);num=m.select_dtypes('number');finite=num.replace([np.inf,-np.inf],np.nan)
        detail.update({'metric_rows':len(m),'metric_columns':len(m.columns),'metric_entities':sorted({c.rsplit('_',1)[0] for c in m if c!='time'}),'metric_nulls':int(m.isna().sum().sum()),'metric_infinite':int(np.isinf(num.to_numpy()).sum()),'metric_constant_columns':int((finite.nunique(dropna=True)<=1).sum()),'metric_time_outside':not(valid.min()<=inject<=valid.max()),'metric_duplicate_time':b['duplicate_time'],'metric_null_time':b['null_time']})
        schema=pq.read_schema(p/'metrics.parquet');sig=hashlib.sha256(str(schema.remove_metadata()).encode()).hexdigest();schemas[sig]={'modality':'metric','fields':[{'name':c.name,'type':str(c.type)} for c in schema],'cases':schemas.get(sig,{}).get('cases',[])+[case]};detail['metric_schema_id']=sig
        if r['dataset']!='RE1-SS':
            cc,ee,periods=survey(m,inject);detail['survey_periods']=periods
            for x in cc:channels.append({'case':case,'dataset':r['dataset'],'root':r['root'],'fault':r['fault'],'repetition':r['repetition'],**x,'is_root':x['entity']==r['root']})
            for x in ee:entities.append({'case':case,'dataset':r['dataset'],'root':r['root'],'fault':r['fault'],'repetition':r['repetition'],**x,'is_root':x['entity']==r['root']})
        log=p/'logs.parquet'
        if log.is_file():
            l=pd.read_parquet(log);lt=l['timestamp'].dropna();messages=l['message'].fillna('').astype(str)
            direct=[c for c in l if re.sub('[_-]','',c.lower()) in ('traceid','spanid','traceparent')]
            keyed=messages.str.contains(r'(?:trace[_-]?id|span[_-]?id|traceparent)\s*[=:]|\[[^\]\n]*,[0-9a-f]{16},[0-9a-f]{16},',case=False,regex=True)
            hexrows=messages.str.contains(r'(?<![0-9a-f])[0-9a-f]{16}(?:[0-9a-f]{16})?(?![0-9a-f])',case=False,regex=True)
            detail['log']={'rows':len(l),'columns':list(l.columns),'nulls':l.isna().sum().to_dict(),'entities':sorted(l['container_name'].dropna().unique().tolist()),'direct_id_columns':direct,'keyed_or_spring_context_rows':int(keyed.sum()),'hex16or32_rows':int(hexrows.sum()),'example_context_messages':messages.loc[keyed].head(1).tolist(),'trace_join':'not_applicable_no_trace_file'}
            bounds.append({'case':case,'dataset':r['dataset'],'modality':'log','rows':len(l),'min_epoch':float(lt.min()) if len(lt) else None,'max_epoch':float(lt.max()) if len(lt) else None,'start_minus_injection':float(lt.min()-inject) if len(lt) else None,'end_minus_injection':float(lt.max()-inject) if len(lt) else None,'midpoint_minus_injection':float((lt.min()+lt.max())/2-inject) if len(lt) else None,'pre_rows':int((lt<inject).sum()),'post_rows':int((lt>=inject).sum()),'null_time':int(l.timestamp.isna().sum()),'duplicate_time':int(lt.duplicated().sum()),'median_step':None})
            schema=pq.read_schema(log);sig=hashlib.sha256(str(schema.remove_metadata()).encode()).hexdigest();schemas[sig]={'modality':'log','fields':[{'name':c.name,'type':str(c.type)} for c in schema],'cases':schemas.get(sig,{}).get('cases',[])+[case]};detail['log_schema_id']=sig
        label=p/'root_cause.txt'
        if label.is_file():
            raw=label.read_text();row=next(csv.reader([raw.strip()]));assert len(row)==6
            ns=int(row[1]);rootlabels.append({'case':case,'path':str(label),'root':r['root'],'fault':r['fault'],'injection':inject,'fields':row,'epoch_seconds':ns/1e9,'label_time_minus_injection':ns/1e9-inject,'in_metric_interval':bool(valid.min()<=ns/1e9<=valid.max()),'raw_text':raw})
        qualities.append(detail)
        with (run/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'case':case,'elapsed_seconds':time.monotonic()-start})+'\n')
        if i%25==0:print('inspected',i,'of',len(cases),'elapsed',round(time.monotonic()-start,1),flush=True)
    dump(run/'cases.json',qualities);dump(run/'schemas.json',schemas);dump(run/'root-cause-labels.json',rootlabels);dump(run/'hash-recheck.json',checks)
    csvout(run/'boundaries.csv',bounds);csvout(run/'channel-bands.csv',channels);csvout(run/'entity-rates.csv',entities)
    er=pd.DataFrame(entities);outer=er[~er.is_root].copy();case_stats=outer.groupby(['dataset','case','root','fault','repetition','group','q'],as_index=False).agg(control_mean=('control_rate','mean'),post_mean=('post_rate','mean'),entities=('entity','count'),services_increased=('difference',lambda x:int((x>0).sum())))
    case_stats.to_csv(run/'probe-cases.csv',index=False)
    cell=case_stats.groupby(['dataset','root','fault','group','q'],as_index=False).agg(cases=('case','nunique'),control_mean=('control_mean','mean'),post_mean=('post_mean','mean'),case_any_increase=('services_increased',lambda x:int((x>0).sum())))
    cell.to_csv(run/'probe-cells.csv',index=False)
    totals=case_stats.groupby(['dataset','group','q'],as_index=False).agg(cases=('case','nunique'),control_mean=('control_mean','mean'),post_mean=('post_mean','mean'),cases_any_increase=('services_increased',lambda x:int((x>0).sum())))
    totals.to_csv(run/'probe-summary.csv',index=False)
    dump(run/'manifest.json',{'revision':REV,'elapsed_seconds':time.monotonic()-start,'python':sys.version,'pandas':pd.__version__,'numpy':np.__version__,'pyarrow':pa.__version__,'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'cases':len(qualities),'root_cause_labels':len(rootlabels),'hash_files':len(checks),'trace_files':0,'parent_resolution':None,'runtime_root_degrees':None,'status':'success'})
    print('complete',len(qualities),'labels',len(rootlabels),'seconds',round(time.monotonic()-start,1))

if __name__=='__main__':main()
