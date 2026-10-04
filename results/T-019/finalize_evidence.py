"""Additional descriptive exclusions, runner source and assembled exposure ledger."""
import csv, hashlib, json, pathlib
import pandas as pd
import numpy as np
from urllib.request import urlopen, Request
from acquire import ROOT, OUT, dump, csvout

def main():
    cases=json.loads((OUT/'inspection/cases.json').read_text(encoding='utf-8'))
    refinements=[]
    for c in cases:
        m=pd.read_parquet(ROOT/'data/T-019'/c['case']/'metrics.parquet')
        unique=m.select_dtypes('number').replace([np.inf,-np.inf],np.nan).nunique(dropna=True)
        old=c.get('metric_constant_or_all_null_columns',c['metric_constant_columns'])
        c['metric_constant_or_all_null_columns']=old
        c['metric_constant_columns']=int((unique==1).sum());c['metric_all_null_columns']=int((unique==0).sum())
        refinements.append({'case':c['case'],'constant_or_all_null_before':old,'constant_exact':c['metric_constant_columns'],'all_null':c['metric_all_null_columns']})
    dump(OUT/'inspection/cases.json',cases);dump(OUT/'inspection/quality-refinement.json',refinements)
    manifest=json.loads((OUT/'inspection/manifest.json').read_text(encoding='utf-8'))
    manifest['postprocessing']={'script':'results/T-019/finalize_evidence.py','script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'quality_scope':'constant exactly one finite distinct value versus all-null; prior combined count retained; metric-only re-read of all245 cases','probe_scope':'saved entity rates reaggregated only over finite paired control/post rows; original channel bands/rates unchanged; prior aggregates retained in inspection-summary-001-before-paired'}
    dump(OUT/'inspection/manifest.json',manifest)
    schemas=json.loads((OUT/'inspection/schemas.json').read_text(encoding='utf-8'))
    channels=pd.read_csv(OUT/'inspection/channel-bands.csv');entities=pd.read_csv(OUT/'inspection/entity-rates.csv')
    # Paired comparisons require finite rates for the same entity in both windows.
    excluded=entities[entities.control_rate.isna()|entities.post_rate.isna()].copy()
    excluded['reason']='no_finite_observations_in_control_or_post; no rate defined'
    excluded.to_csv(OUT/'inspection/paired-entity-exclusions.csv',index=False)
    outer=entities[(~entities.is_root)&entities.control_rate.notna()&entities.post_rate.notna()].copy()
    case_stats=outer.groupby(['dataset','case','root','fault','repetition','group','q'],as_index=False).agg(control_mean=('control_rate','mean'),post_mean=('post_rate','mean'),entities=('entity','count'),services_increased=('difference',lambda x:int((x>0).sum())))
    case_stats.to_csv(OUT/'inspection/probe-cases.csv',index=False)
    case_stats.groupby(['dataset','root','fault','group','q'],as_index=False).agg(cases=('case','nunique'),control_mean=('control_mean','mean'),post_mean=('post_mean','mean'),case_any_increase=('services_increased',lambda x:int((x>0).sum()))).to_csv(OUT/'inspection/probe-cells.csv',index=False)
    case_stats.groupby(['dataset','group','q'],as_index=False).agg(cases=('case','nunique'),control_mean=('control_mean','mean'),post_mean=('post_mean','mean'),cases_any_increase=('services_increased',lambda x:int((x>0).sum()))).to_csv(OUT/'inspection/probe-summary.csv',index=False)
    ex=[];exc=[]
    for c in cases:
        if c['dataset']=='RE1-SS':continue
        band=channels[channels.case==c['case']];names={r['name'] for r in schemas[c['metric_schema_id']]['fields'] if r['name']!='time'}
        available=set(band.metric)
        for name in sorted(names-available):exc.append({'case':c['case'],'dataset':c['dataset'],'metric':name,'reason':'fewer_than_30_finite_reference_values','reference_rows':c['survey_periods']['reference']})
        own=outer[outer.case==c['case']]
        for group in ['all_metrics','latency90','cpu','mem','error','workload']:
            for q in [.95,.99,.995]:
                if own[(own.group==group)&(own.q==q)].empty:
                    suffix={'latency90':'latency-90'}.get(group,group)
                    candidate=[x for x in names if x.rsplit('_',1)[0]!=c['root'] and (group=='all_metrics' or x.rsplit('_',1)[-1]==suffix)]
                    ex.append({'case':c['case'],'dataset':c['dataset'],'root':c['root'],'fault':c['fault'],'group':group,'q':q,'reason':'no_outside_root_channel_in_schema' if not candidate else 'outside_channels_insufficient_reference_or_control_or_post','candidate_channels':'|'.join(sorted(candidate))})
    csvout(OUT/'inspection/probe-exclusions.csv',ex);csvout(OUT/'inspection/channel-exclusions.csv',exc)
    ledger=pd.read_csv(OUT/'lineage/so-ca-da-nhin.csv',keep_default_na=False)
    ledger['exposure']='RCA_result' # Refined for local RE1 disk below; original task_ran retained.
    mask=(ledger.source=='RE1-SS')&ledger['case'].str.contains('_disk_')
    ledger.loc[mask,'exposure']='T006_metadata_census_T019_metric_inspection_no_direct_RCA_evidence'
    add=[]
    fields=list(ledger.columns)
    for c in cases:
        add.append({**{f:'' for f in fields},'case':c['case'],'source':'HF_RCAEval_T019_inspection','public_family':c['dataset'].replace('-',''),'public_case':c['case'],'task_ran':'T-019 (file inspection, no RCA/detector)','evidence':'618 source hashes verified; actual metric/log/labels read as available','identity':'pinned_file_identity','inject_time':c['injection'],'comparison_ref':'inspection/cases.json','metric_input':str(ROOT/'data/T-019'/c['case']/'metrics.parquet'),'run_ref':'inspection/manifest.json','exposure':'telemetry_inspection_only'})
    times=json.loads((OUT/'lineage/public-time-inventory.json').read_text(encoding='utf-8'))
    for c in times:
        if c['family']!='re2ob':continue
        add.append({**{f:'' for f in fields},'case':c['case'],'source':'HF_RCAEval_T019_OB_metric_inspection','public_family':'RE2OB','public_case':c['case'],'task_ran':'T-019 (metric inspection, no RCA/detector)','evidence':'metric/injection source hash and full metric comparison verified; no log/trace read','identity':'pinned_file_identity','inject_time':c['inject_time'],'comparison_ref':'lineage/public-metric-comparisons.json','metric_input':str(pathlib.Path(c['path'])/'metrics.parquet'),'run_ref':'lineage/download-manifest.json','exposure':'telemetry_inspection_only'})
    allrows=pd.concat([ledger,pd.DataFrame(add)],ignore_index=True);allrows.to_csv(OUT/'so-ca-da-nhin.csv',index=False)
    dump(OUT/'ledger-summary.json',{'prior_ledger_rows':len(ledger),'T019_inspected_cases':len(add),'total_rows':len(allrows),'note':'one row per source/case/public-family relation plus actual T019 inspections; row count is not unique incident count','exposure_counts':allrows.exposure.value_counts().to_dict()})
    dump(OUT/'inspection/exclusions-summary.json',{'probe_missing_group_case_q_rows':len(ex),'missing_channel_reference_rows':len(exc),'group_counts':pd.DataFrame(ex).groupby(['dataset','group']).size().to_dict().__repr__() if ex else {},'scope':'reporting only; no threshold/class selected'})

if __name__=='__main__':main()
