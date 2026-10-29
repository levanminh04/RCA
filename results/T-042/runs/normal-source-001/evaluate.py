"""Post-freeze P3 scoring, paired intermediates, root-blind drift summaries."""
from collections import Counter,defaultdict
import math
import run as task
from p3.ban_ghi import xep_thuc_the
from p3.danh_gia import cham_ca, tong_hop
R=task.ROOT;B=task.BASE

def representation(method,d,new):
    status='OK'
    if new and d['status']!='OK':return dict(status='UNSUPPORTED',entity_ranking=[],ranking_native=[]),{},[]
    if method=='M4':
        v=d['diagnosis'];scores={s:x['score'] for s,x in v['scores'].items()};native=v['ranks']
        if v['status']=='abstain':status='NO_EVIDENCE'
    elif method=='MAIN':
        v=d['result'];scores=v['scores'];native=v['native_ranks']
    elif new:
        v=d['result'];scores={}
        for op,value in v['scores'].items():
            s=v['operation_services'][op];scores[s]=max(scores.get(s,-math.inf),value)
        native=v['service_ranks_full']
    else:
        v=d['diagnosis'];scores={s:x['score'] for s,x in v['entities'].items()}
        # Cached scores preserve the full operation API order, including ties.
        op_order=list(d['scores']);assert all(d['scores'][a]>=d['scores'][b] for a,b in zip(op_order,op_order[1:]))
        native=list(dict.fromkeys(d['operation_services'][op] for op in op_order))
    items=[(s,s,(scores[s],)) for s in native if s in scores]
    assert set(native)==set(scores)
    return dict(status=status,entity_ranking=xep_thuc_the(items),ranking_native=native),scores,native

def score(rec,scores,native,root):
    value=cham_ca(rec,root)
    if rec['status']=='OK' and root in scores:
        higher=sum(v>scores[root] for v in scores.values());equal=sum(v==scores[root] for v in scores.values())
        positions=list(range(higher+1,higher+equal+1))
        independent_hit=sum(p<=1 for p in positions)/len(positions);independent_rr=sum(1/p for p in positions)/len(positions)
        assert math.isclose(value['hit@1'],independent_hit,rel_tol=1e-14,abs_tol=0)
        assert math.isclose(value['rr'],independent_rr,rel_tol=1e-14,abs_tol=0)
    rank=native.index(root)+1 if rec['status']=='OK' and root in native else None
    value.update(native_rank=rank,native_hit1=int(rank==1),native_mrr=1/rank if rank else 0,root_score=scores.get(root))
    return value

def component_chain(method,old,new,root):
    if new['status']!='OK':return dict(status=new['status'],error=new.get('error'),audit=new.get('audit'))
    if method=='M4':
        a,b=old['diagnosis'],new['diagnosis']
        services={s:dict(old=a['scores'][s],new=b['scores'][s],old_trace=a['traces'].get(s),new_trace=b['traces'].get(s),log_same=a['logs'][s]==b['logs'][s]) for s in a['scores']}
        changes={k:dict(old=a['metrics'][k],new=b['metrics'][k]) for k in a['metrics'] if a['metrics'][k]!=b['metrics'][k]}
        assert all(v['log_same'] for v in services.values())
        return dict(services=services,root_components=services[root],metric_changes=changes,usable_metric_before=sum(v['status']=='ok' for v in a['metrics'].values()),usable_metric_after=sum(v['status']=='ok' for v in b['metrics'].values()))
    if method=='MAIN':
        a,b=old['result']['independent'],new['result']['independent']
        services={s:dict(old=a['fusion'][s],new=b['fusion'][s],old_metric=a['metrics'].get(s),new_metric=b['metrics'].get(s),old_log=a['logs'].get(s),new_log=b['logs'].get(s),old_trace=a['traces'].get(s),new_trace=b['traces'].get(s),trace_same=a['traces'].get(s)==b['traces'].get(s)) for s in a['fusion']}
        assert all(v['trace_same'] for v in services.values())
        return dict(services=services,root_components=services[root],log_duration_before=a['log_duration_minutes'],log_duration_after=b['log_duration_minutes'],
                    fallback_old=sum(p['fallback_to_incident'] for s in a['metrics'].values() for p in s['pools']),fallback_new=sum(p['fallback_to_incident'] for s in b['metrics'].values() for p in s['pools']))
    a,b=old,new['result']
    ops={op:dict(old=a['baseline_slo_ms'].get(op),new=b['baseline_slo_ms'].get(op)) for op in sorted(set(a['baseline_slo_ms'])|set(b['baseline_slo_ms']))}
    return dict(counts_old=a['counts'],counts_new=b['counts'],baseline_slo_changes=ops,
                root_operations=[op for op,s in b['operation_services'].items() if s==root],
                spectrum_old=a['spectrum'],spectrum_new=b['spectrum'],scores_old=a['scores'],scores_new=b['scores'],
                groups_old={g:{k:v for k,v in x.items() if k!='graph'} for g,x in a['groups'].items()},groups_new=b['groups'])

def main():
    folder=B/(task.sys.argv[1] if len(task.sys.argv)>1 else 'evaluate-001');folder.mkdir(exist_ok=False)
    (folder/'source-at-start.py').write_bytes(task.Path(__file__).read_bytes())
    task.write(folder/'invocation.json',dict(argv=task.sys.argv,utc=task.now(),script_sha256=task.sha(__file__)))
    frozen=task.read(B/'full-001/diagnoses-frozen.json');assert frozen['completed'] and not frozen['labels_read'] and len(frozen['records'])==66
    for row in frozen['records']:assert task.sha(R/row['path'])==row['sha256']
    task.write(folder/'pre-label-freeze-check.json',dict(utc=task.now(),records=66,frozen_sha256=task.sha(B/'full-001/diagnoses-frozen.json'),all_records_hash_match=True))
    index=task.read(R/'results/T-026/ban-ghi-dua-vao-cham.json');lp=R/'results/T-026/nhan-dev.json'
    assert task.sha(lp)==index['source_hashes']['results/T-026/nhan-dev.json']
    labels={x['opaque_id']:x for x in task.read(lp)['cases']}
    cases=[];per=defaultdict(dict);chains=[];states=Counter();drifts={};pointers={}
    for row in frozen['records']:
        d=task.read(R/row['path']);oid=row['opaque_id'];method=row['method'];root=labels[oid]['root'];base=d['baseline'];assert task.sha(R/base['path'])==base['sha256']
        old=task.read(R/base['path']);pair={}
        for n,v,isnew in [('old',old,False),('normal_source',d,True)]:
            rec,scores,native=representation(method,v,isnew);ev=score(rec,scores,native,root);per[method+'/'+n][oid]=ev;pair[n]=ev
        states[(method,d['status'])]+=1
        cases.append(dict(opaque_id=oid,method=method,root=root,cell=labels[oid]['cell'],old=pair['old'],normal_source=pair['normal_source'],
                          delta_hit1=pair['normal_source']['hit@1']-pair['old']['hit@1'],delta_mrr=pair['normal_source']['rr']-pair['old']['rr'],source=row,baseline=base))
        chains.append(dict(opaque_id=oid,method=method,cell=labels[oid]['cell'],root=root,**component_chain(method,old,d,root)))
        if oid not in drifts:
            f=(R/row['path']).parent/'F2.json.gz';drifts[oid]=task.read(f);pointers[oid]=dict(path=f.relative_to(R).as_posix(),sha256=task.sha(f))
    summary={};cells={}
    for method in ('M4','MAIN','MICRO'):
        summary[method]={n:tong_hop(per[method+'/'+n]) for n in ('old','normal_source')}
        for n in ('old','normal_source'):
            summary[method][n].update(native_hit1=sum(v['native_hit1'] for v in per[method+'/'+n].values())/22,native_mrr=sum(v['native_mrr'] for v in per[method+'/'+n].values())/22)
        summary[method]['delta']={k:summary[method]['normal_source'][k]-summary[method]['old'][k] for k in ('hit@1','mrr','native_hit1','native_mrr')}
        summary[method]['paired_cases']=dict(improved=sum(x['delta_mrr']>0 for x in cases if x['method']==method),worsened=sum(x['delta_mrr']<0 for x in cases if x['method']==method),same=sum(x['delta_mrr']==0 for x in cases if x['method']==method))
        cells[method]={c:{n:tong_hop({oid:v for oid,v in per[method+'/'+n].items() if labels[oid]['cell']==c}) for n in ('old','normal_source')} for c in sorted({v['cell'] for v in labels.values()})}
    task.write(folder/'evaluation.json',dict(summary=summary,by_cell=cells,cases=cases,statuses={str(k):v for k,v in states.items()},frozen_sha256=task.sha(B/'full-001/diagnoses-frozen.json'),label_sha256=task.sha(lp),independent_metrics='PASS'))
    task.write(folder/'mechanism-chains.json.gz',dict(chains=chains,scope='paired intermediate changes; source+duration+coverage not isolated'))
    f2rows=[];undefined=0
    for oid,v in drifts.items():
        for k,x in v['metric'].items():
            if x['delta_over_std'] is None:undefined+=1
            f2rows.append(dict(opaque_id=oid,channel=k,**x))
    defined=[abs(x['delta_over_std']) for x in f2rows if x['delta_over_std'] is not None]
    allow=task.nezha.nap_allowlist(R/'results/T-026/allowlist-dev.json');near=[]
    for a,b in zip(sorted(allow,key=lambda o:allow[o]['t_ns']),sorted(allow,key=lambda o:allow[o]['t_ns'])[1:]):
        gap=(allow[b]['t_ns']-allow[a]['t_ns'])/task.NS
        if 497<=gap<=551:near.append(dict(first=a,second=b,gap_s=gap,nominal_offset_N_start_after_previous_end_s=gap-300-180,note='adjacent within dev only; 180s nominal not recovery observation'))
    groups={};half_availability={}
    for oid in drifts:
        vals=[x['delta_over_std'] for x in f2rows if x['opaque_id']==oid and x['delta_over_std'] is not None]
        groups[oid]=dict(defined=len(vals),median_abs=float(task.np.median(task.np.abs(vals))) if vals else None,max_abs=max(map(abs,vals),default=None),positive=sum(x>0 for x in vals),negative=sum(x<0 for x in vals))
        halves=drifts[oid]['trace_log_halves'];half_availability[oid]={}
        for modality in ('trace','log'):
            services=set(halves['early'][modality])|set(halves['late'][modality])
            half_availability[oid][modality]={s:('both_halves_observed' if s in halves['early'][modality] and s in halves['late'][modality] else 'UNAVAILABLE_HALF') for s in sorted(services)}
    fsummary=dict(case_channel_pairs=len(f2rows),defined_normalized=len(defined),zero_variance_or_missing=undefined,
                  median_abs_delta_over_std=float(task.np.median(defined)),p90_abs_delta_over_std=float(task.np.quantile(defined,.9)),max_abs_delta_over_std=max(defined),
                  positive_delta=sum(x['delta'] is not None and x['delta']>0 for x in f2rows),negative_delta=sum(x['delta'] is not None and x['delta']<0 for x in f2rows),zero_delta=sum(x['delta']==0 for x in f2rows),
                  nearest_dev_pairs=near,by_case=groups,trace_log_half_availability=half_availability,claim='Descriptive change, not a test of recovery or source health; channels are dependent')
    task.write(folder/'F2-summary.json',dict(summary=fsummary,source_files=pointers))
    lines=['# Đổi nguồn normal N, giữ A300','', '| Phương pháp | Top1 cũ | Top1 N mới | MRR cũ | MRR N mới | Top1 native cũ/mới |','|---|---:|---:|---:|---:|---|']
    for m,s in summary.items():
        a,b=s['old'],s['normal_source'];lines.append(f"| {m} | {a['hit@1']:.6f} | {b['hit@1']:.6f} | {a['mrr']:.6f} | {b['mrr']:.6f} | {a['native_hit1']:.6f}/{b['native_hit1']:.6f} |")
    lines+=['','Top1/MRR chính dùng kỳ vọng hòa P3; native giữ thứ tự trả về. N mới có thể thiếu metric hoặc dùng fallback, không gọi đây là nền sạch.','', '| Ca | Ô | Phương pháp | Hạng gốc cũ | Hạng N mới | ΔMRR |','|---|---|---|---|---|---:|']
    for x in sorted(cases,key=lambda x:(x['cell'],x['opaque_id'],x['method'])):
        a,b=x['old'],x['normal_source'];lines.append(f"| {x['opaque_id']} | {x['cell']} | {x['method']} | {a['rank_min']}–{a['rank_max']} | {b['rank_min']}–{b['rank_max']} | {x['delta_mrr']:.6f} |")
    (folder/'tables.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(task.json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
