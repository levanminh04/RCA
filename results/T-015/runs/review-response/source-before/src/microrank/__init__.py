"""MicroRank-RCAEval sửa đầu vào (explicit variant, not original MicroRank)."""
import math
import pandas as pd
from .graph import get_pagerank_graph
from .official import trace_pagerank, calculate_spectrum_without_delay_list
from . import official

VARIANT='MicroRank-RCAEval sửa đầu vào'
COLS=['traceID','spanID','parentSpanID','serviceName','methodName','operationName','startTime','duration']

def spectrum_cells(anomaly_result,normal_result,anomaly_count,normal_count,anomaly_nums,normal_nums):
    cells={}
    for op,w in anomaly_result.items():
        cells[op]={'ef':w*anomaly_nums[op],'nf':w*(anomaly_count-anomaly_nums[op])}
        if op in normal_result:
            cells[op].update(ep=normal_result[op]*normal_nums[op],np=normal_result[op]*(normal_count-normal_nums[op]))
        else:cells[op].update(ep=1e-7,np=1e-7)
    for op,w in normal_result.items():
        if op not in cells:cells[op]={'ep':(1+w)*normal_nums[op],'np':normal_count-normal_nums[op],'ef':1e-7,'nf':1e-7}
    return cells

def microrank(data,incident_time_us,include_graph=False):
    """Only observed measurements + an explicitly supplied incident boundary.

    Statistics use pre-boundary spans ending before incident_time_us.
    Diagnosis uses post-boundary spans. A trace has any abnormal span or none;
    both graphs and spectrum counts use those exact disjoint trace groups.
    """
    missing=set(COLS)-set(data.columns)
    if missing:raise ValueError('Missing trace columns: '+','.join(sorted(missing)))
    df=data[COLS].copy()
    for col in ['traceID','spanID','serviceName']:
        if df[col].isna().any():raise ValueError('Null '+col)
    if not math.isfinite(incident_time_us):raise ValueError('Invalid incident boundary')
    if (df.duration<0).any() or df[['duration','startTime']].isna().any().any():raise ValueError('Invalid span time')
    # An exact repeat retains its occurrence, as in the original graph code.
    # A reused identity carrying different observations is ambiguous.
    identities=df[COLS].drop_duplicates()
    if identities.duplicated(['traceID','spanID']).any():raise ValueError('Conflicting observations for traceID/spanID')
    df['methodName']=df.methodName.fillna(df.operationName)
    if df.methodName.isna().any():raise ValueError('Missing operation name')
    df['operation']=df.serviceName+'_'+df.methodName
    pairs=df[['operation','serviceName','methodName']].drop_duplicates()
    if pairs.operation.duplicated().any():raise ValueError('Ambiguous service_method key')
    op_services=dict(zip(pairs.operation,pairs.serviceName))
    df=df.sort_values(['traceID','startTime','spanID'],kind='mergesort')
    before=df[df.startTime+df.duration<incident_time_us]
    after=df[df.startTime+df.duration>=incident_time_us].copy()
    if before.empty or after.empty:return {'variant':VARIANT,'status':'missing_window','ranks':[],'scores':{}}
    stats=before.groupby('operation',sort=True).duration.agg(['mean','std','count'])
    stats['mean']=(stats['mean']/1000).round(2);stats['std']=(stats['std']/1000).round(2)
    newops=set(after.operation)-set(stats.index)
    if newops:raise ValueError('No normal baseline for: '+','.join(sorted(newops)))
    if stats.loc[after.operation.unique(),'std'].isna().any():raise ValueError('Normal std undefined (<2 spans)')
    after['abnormal']=after.duration/1000 >= after.operation.map(stats['mean'])+3*after.operation.map(stats['std'])
    all_traces=set(after.traceID.astype(str))
    abnormal=set(after.loc[after.abnormal,'traceID'].astype(str))
    normal=all_traces-abnormal
    raw_normal=set(after.loc[~after.abnormal,'traceID'].astype(str))
    assert not normal&abnormal and normal|abnormal==all_traces
    result={'variant':VARIANT,'detector':'span3sigma_any_disjoint','status':'ok','ranks':[],
            'counts':{'normal':len(normal),'anomaly':len(abnormal),'all':len(all_traces),'overlap':0,'spans_before':len(before),'spans_after':len(after),'abnormal_spans':int(after.abnormal.sum())},
            'operation_services':op_services,'options':{'d':0.85,'alpha':0.01,'iterations':25,'top_max':5},
            'baseline_slo_ms':{op:{'mean':float(row['mean']),'std':float(row['std']),'count':int(row['count'])} for op,row in stats.iterrows()},'groups':{}}
    result['rcaeval_partition_reference']={'normal_count':len(raw_normal),'anomaly_count':len(abnormal),'overlap':len(raw_normal&abnormal),'before_graph_trace_count':int(before.traceID.nunique()),'after_graph_trace_count':len(all_traces),'meaning':'counts only: same span flags as RCAEval; no baseline method rerun'}
    if not abnormal or not normal:
        result['status']='no_anomalous_traces' if not abnormal else 'no_normal_traces'
        return result
    for name,traces,is_anomaly in [('normal',normal,False),('anomaly',abnormal,True)]:
        part=after[after.traceID.astype(str).isin(traces)]
        rows=list(part[['traceID','spanID','parentSpanID','operation']].itertuples(index=False,name=None))
        graph,audit=get_pagerank_graph(rows)
        captured={}
        previous=official.pageRank
        if include_graph:
            def capture(p_ss,p_sr,p_rs,v,operation_length,trace_length,d=0.85,alpha=0.01):
                vector=previous(p_ss,p_sr,p_rs,v,operation_length,trace_length,d,alpha)
                captured['prior']={tid:float(v[i,0]) for i,tid in enumerate(graph['operation_trace'])}
                captured['service_vector']={op:float(vector[i,0]) for i,op in enumerate(graph['operation_operation'])}
                return vector
            official.pageRank=capture
        try:
            weights,nums=trace_pagerank(graph['operation_operation'],graph['operation_trace'],graph['trace_operation'],graph['pr_trace'],is_anomaly)
        finally:
            official.pageRank=previous
        group={'trace_count':len(traces),'audit':audit,'official':{'weights':{k:float(v) for k,v in weights.items()},'tracecounts':nums}}
        group['official'].update(captured)
        if include_graph:group['graph']=graph
        result['groups'][name]=group
    n=result['groups']['normal']['official'];a=result['groups']['anomaly']['official']
    kwargs=dict(anomaly_result=a['weights'],normal_result=n['weights'],anomaly_list_len=len(abnormal),normal_list_len=len(normal),normal_num_list=n['tracecounts'],anomaly_num_list=a['tracecounts'],spectrum_method='dstar2')
    top,top_scores=calculate_spectrum_without_delay_list(top_max=5,**kwargs)
    full,full_scores=calculate_spectrum_without_delay_list(top_max=max(len(op_services),5),**kwargs)
    result['spectrum']=spectrum_cells(a['weights'],n['weights'],len(abnormal),len(normal),a['tracecounts'],n['tracecounts'])
    if any(not math.isfinite(v) or v<0 for d in result['spectrum'].values() for v in d.values()):raise ValueError('Invalid weighted spectrum')
    if any(not math.isfinite(float(v)) for v in full_scores):raise ValueError('Non-finite suspiciousness')
    result['ranks']=top;result['scores']={k:float(v) for k,v in zip(full,full_scores)}
    result['full_ranks']=full
    result['service_ranks_top11']=list(dict.fromkeys(op_services[op] for op in top))
    result['service_ranks_full']=list(dict.fromkeys(op_services[op] for op in full))
    result['row_order_canonical']=True
    return result
