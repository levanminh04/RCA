"""Postfreeze evaluation and mechanism contrasts. Labels never reach diagnosis."""
from collections import defaultdict, Counter
import math
from pathlib import Path
from simple_runner import ROOT, OUT, read, sha, write


def metric(result, root, cutoff=None):
    scores=result['scores'];native=result['native_ranks']
    nr=native.index(root)+1 if root in native else None
    if root not in scores:
        positions=[]
    else:
        higher=sum(v>scores[root] for v in scores.values())
        equal=sum(v==scores[root] for v in scores.values())
        positions=list(range(higher+1,higher+equal+1))
    def mean(fn):return sum(fn(p) for p in positions)/len(positions) if positions else 0
    return dict(native_rank=nr,native_mrr=1/nr if nr else 0,native_hit1=int(nr==1),
                native_hit3=int(nr is not None and nr<=3),native_hit5=int(nr is not None and nr<=5),
                root_score=scores.get(root),positions=positions,
                expected_hit1=mean(lambda p:int(p<=1)),expected_hit3=mean(lambda p:int(p<=3)),
                expected_hit5=mean(lambda p:int(p<=5)),expected_mrr=mean(lambda p:1/p if cutoff is None or p<=cutoff else 0),
                observed_score_candidates=len(scores),api_candidates=len(native),
                note='Expected ties use internal exact score; partial API truncated5 so RR outside5 becomes0; native API reported separately')


def aggregate(rows):
    keys=['native_hit1','native_hit3','native_hit5','native_mrr','expected_hit1','expected_hit3','expected_hit5','expected_mrr']
    return dict(n=len(rows),**{k:sum(r[k] for r in rows)/len(rows) for k in keys},
                native_MRR_given_returned_hit=sum(r['native_mrr'] for r in rows)/sum(r['native_rank'] is not None for r in rows) if any(r['native_rank'] is not None for r in rows) else None,
                native_missing=sum(r['native_rank'] is None for r in rows))


def main():
    folder=OUT/'simple-evaluate-001';folder.mkdir(exist_ok=False)
    frozen=read(OUT/'simple-full-001/diagnoses-frozen.json');assert frozen['completed'] and not frozen['labels_read']
    meta=read(ROOT/'results/T-026/ban-ghi-dua-vao-cham.json')
    lp=ROOT/'results/T-026/nhan-dev.json';assert sha(lp)==meta['source_hashes']['results/T-026/nhan-dev.json']
    labels={r['opaque_id']:r for r in read(lp)['cases']}
    rows=[];cases=defaultdict(dict)
    for pointer in frozen['records']:
        path=ROOT/pointer['path'];assert sha(path)==pointer['sha256']
        value=read(path);oid=value['opaque_id'];branch=value['branch'];result=value['result'];root=labels[oid]['root']
        case=dict(opaque_id=oid,branch=branch,root=root,cell=labels[oid]['cell'],source=pointer,
                  **metric(result,root,cutoff=5 if branch.startswith('N') else None))
        rows.append(case);cases[oid][branch]=dict(data=value,evaluation=case)
    branches=sorted({r['branch'] for r in rows})
    summary={b:aggregate([r for r in rows if r['branch']==b]) for b in branches}
    bycell={c:{b:aggregate([r for r in rows if r['cell']==c and r['branch']==b]) for b in branches} for c in sorted({r['cell'] for r in rows})}
    contrasts={};details=[]
    for first,second in [('M0','M1'),('M1','M2'),('N0-partial','N1-partial'),('M4-no-log','N1-partial')]:
        changed=[]
        for oid,values in sorted(cases.items()):
            a=values[first];b=values[second]
            if a['data']['result']['scores']!=b['data']['result']['scores']:
                changed.append(oid)
            if a['evaluation']['positions']!=b['evaluation']['positions']:
                details.append(dict(opaque_id=oid,cell=labels[oid]['cell'],contrast=[first,second],
                                    first=a['evaluation'],second=b['evaluation']))
        contrasts[first+' -> '+second]=dict(scores_changed=len(changed),ids=changed,
            root_positions_changed=sum(cases[o][first]['evaluation']['positions']!=cases[o][second]['evaluation']['positions'] for o in cases),
            native_rank_changed=sum(cases[o][first]['evaluation']['native_rank']!=cases[o][second]['evaluation']['native_rank'] for o in cases))
    chains=[];fusion_counts={}
    for branch in ['M0','M1','M2']:
        counts=Counter()
        for oid,values in sorted(cases.items()):
            result=values[branch]['data']['result'];root=labels[oid]['root'];ind=result['independent']
            fusion=ind['fusion'];counts.update(v['branch'] for v in fusion.values())
            rootrow=fusion[root]
            greater=[dict(service=s,**v) for s,v in fusion.items() if v['score']>rootrow['score']]
            chains.append(dict(opaque_id=oid,branch=branch,cell=labels[oid]['cell'],root=root,
                evaluation=values[branch]['evaluation'],root_fusion=rootrow,
                root_metric=ind['metrics'].get(root),root_trace=ind['traces'].get(root),root_log=ind['logs'].get(root),
                higher_scores=sorted(greater,key=lambda v:-v['score']),
                trace_ignored_services=[s for s,v in fusion.items() if v['trace_ignored']],
                log_duration_minutes=ind['log_duration_minutes']))
        fusion_counts[branch]=dict(counts)
    write(folder/'evaluation.json',dict(summary=summary,by_cell=bycell,rows=rows,contrasts=contrasts,
                                     changed_rank_details=details,fusion_branch_counts=fusion_counts,
                                     source_labels_sha256=sha(lp),diagnoses_frozen_sha256=sha(OUT/'simple-full-001/diagnoses-frozen.json')))
    write(folder/'mechanism-chains.json',dict(chains=chains,claim='observed intermediates and exact arithmetic; no selection of new winner'))
    lines=['# Chẩn đoán SimpleRCA bổ sung — cùng22dev','',
           'Các kernel nguồn chạy nguyên hàm, bộ bọc đầu vào là phép đối chiếu P3. Không coi đây là tái lập chương trình/bảng công bố. M0 duration literal; M1 đổi duration vềns; M2 thêm timestamp datetime cho log. N0/N1 là partial metric+trace, thiếu severity.','',
           '| Nhánh | Top1 kỳ vọng | Top3 | Top5 | MRR | Top1 native |','|---|---:|---:|---:|---:|---:|']
    for b,s in summary.items():lines.append(f"| {b} | {s['expected_hit1']:.6f} | {s['expected_hit3']:.6f} | {s['expected_hit5']:.6f} | {s['expected_mrr']:.6f} | {s['native_hit1']:.6f} |")
    lines+=['','## Từng ô','', '| Ô | Nhánh | n | Top1 kỳ vọng | MRR |','|---|---|---:|---:|---:|']
    for cell,results in bycell.items():
        for b,s in results.items():lines.append(f"| {cell} | {b} | {s['n']} | {s['expected_hit1']:.6f} | {s['expected_mrr']:.6f} |")
    lines+=['','## Từng ca','', '| Ca | Nhánh | Vị trí gốc kỳ vọng | Vị trí native |','|---|---|---|---:|']
    for row in sorted(rows,key=lambda r:(r['opaque_id'],r['branch'])):lines.append(f"| {row['opaque_id']} | {row['branch']} | {row['positions']} | {row['native_rank']} |")
    (folder/'tables.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(summary)


if __name__=='__main__':main()
