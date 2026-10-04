"""Correct only root/missing audit metadata of saved OB runs, in batches.

No MicroRank/PageRank function is imported or run. The sole changed root token
is <NA>. We prove it cannot name a span and verify the saved partition/flags.
Use pandas 2.2.3, NumPy 1.26.4, PyArrow 18.1.0 with default pandas conversion.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

sys.dont_write_bytecode=True
COLS=['traceID','spanID','parentSpanID','serviceName','methodName','operationName','startTime','duration']
ALLOWED={'re2ob_'+f'{s}_{fault}_{i}' for s in ['checkoutservice','currencyservice','emailservice','productcatalogservice','recommendationservice'] for fault in ['cpu','mem','disk','socket','delay','loss'] for i in [1,2,3]}
OLD_ROOTS={'','0','0000000000000000','nan','None'}

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda:stream.read(1048576),b''):h.update(part)
    return h.hexdigest()

def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2),encoding='utf-8')

def snapshots(dirs):
    result={}
    for directory in dirs:
        for path in sorted(directory.glob('re2ob_*.json')):
            case=path.stem
            if case not in ALLOWED:continue # Before reading artifact bodies.
            value=json.loads(path.read_text(encoding='utf-8'))
            assert value['case_id']==case and value['half_seconds']==600
            if case in result:
                assert result[case][0].get('scores')==value.get('scores'),case
                continue
            result[case]=(value,path)
    assert set(result)==ALLOWED,'exactly 90 whitelisted snapshots required'
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',required=True,type=Path)
    parser.add_argument('--fixed-dir',action='append',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--batch-size',type=int,default=65536)
    args=parser.parse_args()
    assert pd.__version__=='2.2.3' and np.__version__=='1.26.4' and pa.__version__=='18.1.0','use the pinned EC2 runtime'
    assert not pd.get_option('future.infer_string'),'match original read_parquet conversion'
    assert not args.out.exists(),'preserve prior correction attempts; choose a fresh directory'
    args.out.mkdir(parents=True)
    started=time.monotonic()
    def progress(event,**extra):
        line={'event':event,'elapsed_observed_seconds':round(time.monotonic()-started,3),**extra}
        with (args.out/'progress.jsonl').open('a',encoding='utf-8') as stream:stream.write(json.dumps(line)+'\n')
        print(json.dumps(line),flush=True)
    progress('metadata_block_start',method_not_rerun=True,batch_size=args.batch_size)
    selected=snapshots(args.fixed_dir);results=[];csv_rows=[];not_applicable=[]
    for case in sorted(ALLOWED):
        source=args.data/case/'traces.parquet';target=args.out/(case+'.json')
        saved,saved_path=selected[case]
        case_start=time.monotonic()
        progress('metadata_case_start',case=case)
        try:
            if saved.get('status')=='failed':
                # The failed run never wrote counts/stats/group graph. Do not
                # fabricate a successful metadata correction from that output.
                reason='saved method failed before group metadata was written: '+saved.get('error','unknown error')
                record={'case':case,'snapshot':str(saved_path),'snapshot_sha256':digest(saved_path),
                        'status':'metadata_not_applicable','reason':reason,'method_not_rerun':True,
                        'saved_points_untouched':True,'source_not_opened':True}
                save(target,record);not_applicable.append(case)
                results.append({'case':case,'path':str(target),'sha256':digest(target),'status':'metadata_not_applicable'})
                for name in ['normal','anomaly']:
                    csv_rows.append({'ca':case,'nhom':name,'status':saved['status'],
                                     'missing_parent_cu':'not_stored','root_cu':'not_stored',
                                     'missing_parent_sua':'not_applicable','root_sua':'not_applicable',
                                     'delta_null_token':'not_applicable','span_current_nhom':'not_stored',
                                     'input_numerical_graph_unchanged':'not_applicable: no saved graph','phuong_phap_khong_chay_lai':True})
                progress('metadata_case_not_applicable',case=case,reason=reason)
                continue
            assert source.exists(),case
            source_hash=digest(source)
            assert source_hash==saved['source_sha256'],'source bytes differ from saved run'
            tau=int((source.parent/'inject_time.txt').read_text().strip())*1000000
            lower,upper=tau-600000000,tau+600000000
            stats=saved['baseline_slo_ms']
            thresholds={op:v['mean']+3*v['std'] for op,v in stats.items()}
            parquet=pq.ParquetFile(source)
            window_count=before_count=after_count=abnormal_count=forbidden_span_ids=0
            all_traces,abnormal_traces=set(),set()
            dtypes={};null_types=Counter();null_tokens=Counter();parent_null_samples=[]
            def batches():
                for batch in parquet.iter_batches(batch_size=args.batch_size,columns=COLS,use_pandas_metadata=True):
                    # Same default table-to-pandas conversion as pd.read_parquet;
                    # retain source schema pandas metadata on each record batch.
                    frame=batch.to_pandas()
                    frame=frame.loc[(frame.startTime>=lower)&(frame.startTime<upper)].copy()
                    if len(frame):yield frame
            for frame in batches():
                dtypes.update({col:str(dtype) for col,dtype in frame.dtypes.items()})
                window_count+=len(frame)
                forbidden_span_ids+=int((frame.spanID.astype(str)=='<NA>').sum())
                end=frame.startTime+frame.duration
                before_count+=int((end<tau).sum())
                current=frame.loc[end>=tau].copy();after_count+=len(current)
                if current.empty:continue
                methods=current.methodName.where(current.methodName.notna(),current.operationName)
                operations=current.serviceName+'_'+methods
                cutoff=operations.map(thresholds)
                assert cutoff.notna().all(),'current operation lacks saved reference'
                flags=current.duration/1000>=cutoff
                abnormal_count+=int(flags.sum())
                all_traces.update(current.traceID.astype(str))
                abnormal_traces.update(current.loc[flags,'traceID'].astype(str))
                for value in current.loc[current.parentSpanID.isna(),'parentSpanID']:
                    null_types[type(value).__module__+'.'+type(value).__name__]+=1
                    null_tokens[str(value)]+=1
                    if len(parent_null_samples)<3:parent_null_samples.append({'type':type(value).__module__+'.'+type(value).__name__,'str':str(value),'is_None':value is None})
            assert forbidden_span_ids==0,'<NA> is a real span ID; token reclassification could alter edge lookup'
            normal_traces=all_traces-abnormal_traces
            expected=saved['counts']
            checks={
                'normal_trace_count':len(normal_traces)==expected['normal'],
                'anomaly_trace_count':len(abnormal_traces)==expected['anomaly'],
                'all_trace_count':len(all_traces)==expected['all'],
                'disjoint_groups':not(normal_traces&abnormal_traces) and expected['overlap']==0,
                'abnormal_span_count':abnormal_count==expected['abnormal_spans'],
                'before_span_count':before_count==expected['spans_before'],
                'after_span_count':after_count==expected['spans_after'],
                'no_span_id_matches_new_root_token':forbidden_span_ids==0,
            }
            assert all(checks.values()),(case,checks)
            counters={name:Counter() for name in ['normal','anomaly']}
            for frame in batches():
                current=frame.loc[frame.startTime+frame.duration>=tau]
                for trace,parent in zip(current.traceID,current.parentSpanID):
                    name='anomaly' if str(trace) in abnormal_traces else 'normal'
                    token=None if parent is None else str(parent)
                    counters[name]['spans']+=1
                    counters[name]['parent_isna']+=int(pd.isna(parent))
                    counters[name]['added_root_token_spans']+=int(token=='<NA>')
                    counters[name]['old_root_token_spans']+=int(token is None or token in OLD_ROOTS)
            groups={}
            for name in ['normal','anomaly']:
                count=dict(counters[name]);delta=count.get('added_root_token_spans',0)
                old_group=saved.get('groups',{}).get(name)
                if old_group:
                    old=old_group['audit'];new=dict(old)
                    new['missing_parent_spans']=old['missing_parent_spans']-delta
                    new['explicit_root_spans']=old['explicit_root_spans']+delta
                    assert new['missing_parent_spans']>=0
                    assert all(old[k]==new[k] for k in old if k not in ['missing_parent_spans','explicit_root_spans'])
                    correction={'original_audit':old,'corrected_audit':new,'missing_to_root_delta':delta,'raw_token_counts':count}
                    csv_rows.append({'ca':case,'nhom':name,'status':saved['status'],
                                     'missing_parent_cu':old['missing_parent_spans'],'root_cu':old['explicit_root_spans'],
                                     'missing_parent_sua':new['missing_parent_spans'],'root_sua':new['explicit_root_spans'],
                                     'delta_null_token':delta,'span_current_nhom':count.get('spans',0),
                                     'input_numerical_graph_unchanged':True,'phuong_phap_khong_chay_lai':True})
                else:
                    correction={'original_audit':'not stored for evidence-empty result','corrected_audit':'not applicable: saved method did not build group graph','missing_to_root_delta':None,'raw_token_counts':count}
                    csv_rows.append({'ca':case,'nhom':name,'status':saved['status'],
                                     'missing_parent_cu':'not_stored','root_cu':'not_stored',
                                     'missing_parent_sua':'not_applicable','root_sua':'not_applicable',
                                     'delta_null_token':delta,'span_current_nhom':count.get('spans',0),
                                     'input_numerical_graph_unchanged':True,'phuong_phap_khong_chay_lai':True})
                groups[name]=correction
            result={'case':case,'source':str(source),'source_sha256':source_hash,
                    'snapshot':str(saved_path),'snapshot_sha256':digest(saved_path),'groups':groups,
                    'checks':checks,'all_passed':True,'null_scalar_types':dict(null_types),'null_scalar_tokens':dict(null_tokens),
                    'parent_null_samples':parent_null_samples,'pandas_dtypes':dtypes,
                    'runtime':{'python':platform.python_version(),'pandas':pd.__version__,'numpy':np.__version__,'pyarrow':pa.__version__},
                    'numerical_graph_input_unchanged':True,'proof':'Only <NA> root-vs-missing classification changed. No spanID equals <NA>; unresolved parent creates no edge in either version. All other graph construction steps are unchanged. Saved partition and abnormal flags match. No graph or PageRank rerun.',
                    'saved_points_untouched':True,'method_not_rerun':True,'reason':'c',
                    'window_spans':window_count,'elapsed_observed_seconds':round(time.monotonic()-case_start,3)}
            save(target,result);results.append({'case':case,'path':str(target),'sha256':digest(target),'all_passed':True})
            progress('metadata_case_end',case=case,all_passed=True,seconds=round(time.monotonic()-case_start,3))
        except Exception as error:
            save(args.out/(case+'-failed.json'),{'case':case,'error':repr(error),'method_not_rerun':True})
            progress('metadata_case_failed',case=case,error=repr(error));raise
    with (args.out/'tung-ca.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(csv_rows[0]));writer.writeheader();writer.writerows(csv_rows)
    save(args.out/'manifest.json',{'exact_whitelist':sorted(ALLOWED),'cases':results,'script_sha256':digest(Path(__file__)),
                                 'all_available_metadata_passed':len(results)==90,'method_not_rerun':True,'saved_points_untouched':True,
                                 'metadata_audited_cases':len(results)-len(not_applicable),'metadata_not_applicable_cases':not_applicable,
                                 'elapsed_observed_seconds':round(time.monotonic()-started,3)})
    progress('metadata_block_end',cases=len(results),all_passed=True)

if __name__=='__main__':main()
