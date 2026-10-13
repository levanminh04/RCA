"""Independent aggregate arithmetic on the first eligible cases; no ranker.

Uses only the guarded RAM reader from the producer. All arithmetic and graph
construction below are separate code, with no producer statistics helpers.
"""
import argparse
from collections import defaultdict, deque
import itertools
import json
import math
from pathlib import Path
import sys
import time
from datetime import datetime, timezone, timedelta

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(Path(__file__).parent))
sys.dont_write_bytecode=True


def q95(values):
    vv=sorted(float(x) for x in values)
    if not vv:return None
    pos=(len(vv)-1)*.95
    lo=math.floor(pos);hi=math.ceil(pos)
    return vv[lo]+(vv[hi]-vv[lo])*(pos-lo)


def independently_graph(spans, mask):
    grouped=defaultdict(list)
    cols=['traceID','spanID','parentSpanID','serviceName','startTime','duration']
    for index,tid,sid,parent,service,start,duration in spans[cols].itertuples(index=True,name=None):
        par=None if parent is None or parent!=parent else str(parent)
        grouped[(str(tid),str(sid))].append(((str(service),par,int(start),int(duration)),bool(mask.loc[index])))
    conflicts={key for key,rows in grouped.items() if len({sig for sig,n in rows})>1}
    normal={key:rows[0][0] for key,rows in grouped.items() if rows[0][1] and key not in conflicts}
    adj={sig[0]:set() for sig in normal.values()}
    orphan=selfloops=removed=0
    for key,(service,parent,st,dur) in normal.items():
        pkey=(key[0],parent)
        if pkey not in normal:
            orphan+=1;removed+=pkey in conflicts
        elif normal[pkey][0]==service:selfloops+=1
        else:adj[normal[pkey][0]].add(service)
    reverse=defaultdict(set)
    for a,bb in adj.items():
        for b in bb:reverse[b].add(a)
    return adj,{'unique_effective_spans_N':len(normal),'conflict_keys_outer':len(conflicts),
                'input_rows_N':int(mask.sum()),
                'duplicate_rows_outer':sum(sum(sig==rows[0][0] for sig,n in rows[1:]) for rows in grouped.values()),
                'duplicate_rows_N':sum(sum(n and sig==rows[0][0] for sig,n in rows[1:]) for rows in grouped.values()),
                'conflict_keys_with_N':sum(any(n for sig,n in grouped[key]) for key in conflicts),
                'orphan_rows':orphan,'edges_to_conflicts_removed':removed,'self_loop_span_rows':selfloops,
                'nodes':len(adj),'effective_edges':sum(map(len,adj.values())),
                'isolated_services':sum(not adj[n] and not reverse[n] for n in adj)}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run-id',required=True);a=parser.parse_args()
    run=ROOT/'results/T-028/runs'/a.run_id
    outpath=run/'independent-statistics.json'
    if outpath.exists():raise RuntimeError('Preserve existing check; use a new output/run')
    doc=json.loads((run/'ca-sai.json').read_text(encoding='utf-8'))
    from native_stats import load_case
    import numpy as np
    checks=[];selected={};began=time.perf_counter()
    def check(kind,ds,oid,expected,actual,src,approx=False):
        if approx and expected is not None and actual is not None:
            passed=math.isclose(float(expected),float(actual),rel_tol=1e-10,abs_tol=1e-9)
        else:passed=expected==actual
        checks.append({'kind':kind,'dataset':ds,'opaque_id':oid,'expected':expected,'actual':actual,'passed':passed,'source':src})
    for ds in ('RE2-TT','Nezha-OB'):
        candidates=sorted([r for r in doc['main_rows'] if r['dataset']==ds and r['method']=='baro'],key=lambda r:r['opaque_id'])
        chosen=[]
        by_kind={kind:[] for kind in ('metric','span','log','graph','operation')}
        for row in candidates:
            oid=row['opaque_id'];feature_path=row['evidence']['source']['path']
            agg=json.loads((ROOT/feature_path).read_text(encoding='utf-8'))['aggregate']
            eligibility={'metric':any(v['availability']=='available' for v in agg['metrics'].values()),
                         'span':any(v['availability']=='available' for v in agg['trace_end'].values()),
                         'log':any(v['availability']=='available' for v in agg['logs_A'].values()),
                         'graph':agg['graph_end']['availability']=='available',
                         'operation':any(v['availability']=='available' for v in agg['operations_end']['operations'].values())}
            needed=[kind for kind in by_kind if len(by_kind[kind])<3 and eligibility[kind]]
            if not needed:continue
            for kind in needed:by_kind[kind].append(oid)
            chosen.append(oid)
            payload=load_case(ROOT,ds,oid,t=agg['window'].get('t'))
            src={'path':feature_path,'json_pointer':'/aggregate'}
            # Saved input provenance is checked against the guarded raw source
            # for both datasets, even if the saved method status is non-OK.
            for methodrow in doc['main_rows']:
                if methodrow['dataset']!=ds or methodrow['opaque_id']!=oid:continue
                for ref in methodrow['source']['records']:
                    rec=json.loads((ROOT/ref['path']).read_text(encoding='utf-8'))
                    if rec['status']=='UNSUPPORTED':continue
                    if ds=='RE2-TT':
                        for name,meta in agg['provenance']['sources'].items():check('input_sha256',ds,oid,meta.get('sha256'),rec['input_sha256'].get(name),{'path':ref['path'],'json_pointer':'/input_sha256/'+name})
                        check('window_t',ds,oid,payload['t_seconds'],rec['window']['t'],src)
                    else:
                        for name,meta in agg['provenance']['sources'].items():check('input_sha256',ds,oid,meta['sha256'],rec['input_sha256'].get(name),{'path':ref['path'],'json_pointer':'/input_sha256/'+name})
                        check('window_t_ns',ds,oid,payload['t_ns'],rec['window'].get('t_ns'),src)
            for col,arrays in payload['metric_arrays'].items():
                n=[float(x) for x in arrays['normal'] if math.isfinite(float(x))]
                aa=[float(x) for x in arrays['anomalous'] if math.isfinite(float(x))]
                rr=agg['metrics'][col]
                check('metric_count_N',ds,oid,len(n),rr['nN'],src)
                check('metric_count_A',ds,oid,len(aa),rr['nA'],src)
                check('metric_missing_N',ds,oid,len(arrays['normal'])-len(n),rr['missing_N'],src)
                check('metric_missing_A',ds,oid,len(arrays['anomalous'])-len(aa),rr['missing_A'],src)
                if len(n)>=2 and aa:
                    mu=math.fsum(n)/len(n);std=math.sqrt(math.fsum((x-mu)**2 for x in n)/len(n))
                    events=sum(x>mu+3*std for x in aa)
                    check('metric_mean',ds,oid,mu,rr['muN']['value'],src,True)
                    check('metric_sigma_ddof0',ds,oid,std,rr['sigmaN']['value'],src,True)
                    check('metric_threshold',ds,oid,mu+3*std,rr['theta']['value'],src,True)
                    check('metric_strict_events',ds,oid,events,rr['events']['value'],src)
            spans=payload['spans'];tus=payload['t_seconds']*1000000
            masks={'start':spans['startTime']<tus,'end':spans['startTime']+spans['duration']<tus}
            for split,mask in masks.items():
                if ds=='Nezha-OB':
                    ns_mask=spans['_start_ns']<payload['t_ns'] if split=='start' else spans['_end_ns']<payload['t_ns']
                    check('ns_us_membership_'+split,ds,oid,True,bool((mask==ns_mask).all()),src)
                for service,part in spans.groupby('serviceName'):
                    normal=part.loc[mask.loc[part.index],'duration'].tolist()
                    aa=part.loc[~mask.loc[part.index],'duration'].tolist()
                    rr=agg['trace_'+split][str(service)]
                    check('span_count_N_'+split,ds,oid,len(normal),rr['nN'],src)
                    check('span_count_A_'+split,ds,oid,len(aa),rr['nA'],src)
                    check('span_P95N_'+split,ds,oid,q95(normal),rr['P95N']['value'],src,True)
                    check('span_P95A_'+split,ds,oid,q95(aa),rr['P95A']['value'],src,True)
                    if normal and aa:
                        for tau in (2,3,4):check('proxy_tau_'+str(tau)+'_'+split,ds,oid,q95(aa)>tau*q95(normal),rr['latency_up'][str(tau)]['value'],src)
                adj,counts=independently_graph(spans,mask)
                for field,v in counts.items():check('graph_'+split+'_'+field,ds,oid,v,agg['graph_'+split][field],src)
                root=row['root'];rev=defaultdict(set)
                for caller,targets in adj.items():
                    for target in targets:rev[target].add(caller)
                distance={root:0};queue=deque([root])
                while queue:
                    child=queue.popleft()
                    for par in rev[child]:
                        if par not in distance:distance[par]=distance[child]+1;queue.append(par)
                related=[r for r in doc['main_rows'] if r['dataset']==ds and r['opaque_id']==oid and r['evidence']['native_trace_split']==split and r['status']=='OK']
                for rr in related:
                    for seed in rr['evidence']['seed_evidence'].values():
                        check('graph_ancestor_membership_'+split,ds,oid,sorted(set(distance)-{root}),seed['ancestors']['value'],src)
            logs=payload['logs'];boundary=payload['t_ns'] if ds=='Nezha-OB' else payload['t_seconds']
            if logs is not None:
                post=logs.loc[logs['timestamp']>=boundary]
                for service,rr in agg['logs_A'].items():
                    entries=post.loc[post['container_name']==service,'message'].fillna('').astype(str).tolist()
                    hits=sum(any(word in msg.upper() for word in ('ERROR','FAIL','EXCEPTION')) for msg in entries)
                    check('log_rows_A',ds,oid,len(entries),rr['rows_A']['value'],src)
                    check('log_keyword_count_A',ds,oid,hits,rr['keyword_count_A']['value'],src)
            ops=spans.copy();ops['methodName']=ops['methodName'].fillna(ops['operationName']);ops['operation']=ops['serviceName']+'_'+ops['methodName']
            normal=ops.loc[masks['end']];post=ops.loc[~masks['end']]
            thresholds={'operations_end':{},'operations_end_tracerca':{}}
            for op,rr in agg['operations_end']['operations'].items():
                vv=normal.loc[normal['operation']==op,'duration'].to_numpy(dtype=float)/1000
                aa=post.loc[post['operation']==op,'duration'].to_numpy(dtype=float)/1000
                if len(vv)<2 or rr['availability']!='available':continue
                mu=float(np.round(vv.mean(),2));std=float(np.round(vv.std(ddof=1),2))
                check('operation_mu_round2',ds,oid,mu,rr['muN_round']['value'],src)
                check('operation_sigma_ddof1_round2',ds,oid,std,rr['sigmaN_round']['value'],src)
                check('operation_threshold',ds,oid,mu+3*std,rr['threshold']['value'],src)
                thresholds['operations_end'][op]=mu+3*std
                check('operation_abnormal_ge',ds,oid,int(np.sum(aa>=mu+3*std)),rr['abnormal_spans_A']['value'],src)
            for op,rr in agg['operations_end_tracerca']['operations'].items():
                vv=normal.loc[normal['operation']==op,'duration'].to_numpy(dtype=float)
                aa=post.loc[post['operation']==op,'duration'].to_numpy(dtype=float)/1000
                if len(vv)<2 or rr['availability']!='available':continue
                mu=float(round(vv.mean()/1000,2));std=float(round(vv.std(ddof=1)/1000,2))
                check('TraceRCA_operation_mu_round2',ds,oid,mu,rr['muN_round']['value'],src)
                check('TraceRCA_operation_sigma_round2',ds,oid,std,rr['sigmaN_round']['value'],src)
                check('TraceRCA_operation_threshold',ds,oid,mu+3*std,rr['threshold']['value'],src)
                thresholds['operations_end_tracerca'][op]=mu+3*std
                check('TraceRCA_operation_abnormal_ge',ds,oid,int(np.sum(aa>=mu+3*std)),rr['abnormal_spans_A']['value'],src)
            for table in ('operations_end','operations_end_tracerca'):
                independent_flags={}
                for op,rr in agg[table]['operations'].items():
                    check(table+'_operation_count_N',ds,oid,int((normal['operation']==op).sum()),rr['nN'],src)
                    check(table+'_operation_count_A',ds,oid,int((post['operation']==op).sum()),rr['nA'],src)
                    if rr['availability']=='available':
                        subset=post.loc[post['operation']==op]
                        threshold=thresholds[table][op]
                        for idx,duration in subset['duration'].items():independent_flags[idx]=float(duration)/1000>=threshold
                eligible=all(agg[table]['operations'][op]['availability']=='available' for op in set(post['operation']))
                alltraces=set(post['traceID'].astype(str))
                abnormal=set(post.loc[[idx for idx in post.index if independent_flags.get(idx) is True],'traceID'].astype(str))
                check(table+'_trace_A_count',ds,oid,len(alltraces),agg[table]['trace_A_count']['value'],src)
                if eligible:
                    check(table+'_total_abnormal_spans_A',ds,oid,sum(independent_flags.values()),agg[table]['total_abnormal_spans_A']['value'],src)
                    check(table+'_trace_A_abnormal_count',ds,oid,len(abnormal),agg[table]['trace_A_abnormal_count']['value'],src)
                    for op,rr in agg[table]['operations'].items():
                        optraces=set(post.loc[post['operation']==op,'traceID'].astype(str))
                        check(table+'_trace_A_contains_operation',ds,oid,len(optraces),rr['trace_A_contains_operation']['value'],src)
                        check(table+'_trace_A_abnormal_contains_operation',ds,oid,len(optraces&abnormal),rr['trace_A_abnormal_contains_operation']['value'],src)
            print(json.dumps({'dataset':ds,'opaque_id':oid,'checks_so_far':len(checks),'elapsed_s':time.perf_counter()-began}),flush=True)
            del payload,spans,logs,ops
            if all(len(v)==3 for v in by_kind.values()):break
        selected[ds]=by_kind
    report={'status':'passed' if checks and all(c['passed'] for c in checks) and all(len(v)==3 for ds in selected.values() for v in ds.values()) else 'failed',
            'checked_at':datetime.now(timezone(timedelta(hours=7))).isoformat(),'elapsed_s':time.perf_counter()-began,
            'selection_rule':'first three eligible opaque ids per dataset; all metric/span/log/graph aggregates checked',
            'selected_cases':selected,'checks':checks,'checks_n':len(checks),'no_method_execution':True,'payload_saved':False}
    outpath.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(report['status'],len(checks),'failures',sum(not c['passed'] for c in checks))
    if report['status']!='passed':raise SystemExit(1)


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');main()
