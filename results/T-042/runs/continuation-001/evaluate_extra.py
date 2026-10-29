"""Postfreeze evaluation for severity and source-time contrasts."""
from collections import defaultdict
import json
from simple_runner import ROOT, OUT, read, sha, write
from evaluate_simple import metric, aggregate


def main():
    folder=OUT/'extra-evaluate-001';folder.mkdir(exist_ok=False)
    manifests=[(f'level-seed{s}',OUT/f'level-seed{s}-001/diagnoses-frozen.json') for s in ['0','1','2']]
    manifests.append(('time',OUT/'time-projection-001/diagnoses-frozen.json'))
    docs={}
    for name,path in manifests:
        frozen=read(path);assert frozen['completed'] and not frozen['labels_read']
        for rec in frozen['records']:
            assert sha(ROOT/rec['path'])==rec['sha256']
            value=read(ROOT/rec['path']);assert not value['labels_read'];docs[(name,value['opaque_id'],value['branch'])]=dict(value=value,source=rec)
    write(folder/'pre-label-freeze.json',dict(manifests={name:dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path)) for name,path in manifests},verified=len(docs),labels_read=False))
    lp=ROOT/'results/T-026/nhan-dev.json';pins=read(ROOT/'results/T-026/ban-ghi-dua-vao-cham.json')
    assert sha(lp)==pins['source_hashes']['results/T-026/nhan-dev.json'];labels={r['opaque_id']:r for r in read(lp)['cases']}
    rows=[];bykey={};seedcompare=[]
    for (family,oid,b),r in sorted(docs.items()):
        result=r['value']['result'];m=metric(result,labels[oid]['root'],None if b.startswith('T-M') else 5)
        row=dict(family=family,opaque_id=oid,branch=b,cell=labels[oid]['cell'],root=labels[oid]['root'],**m)
        rows.append(row);bykey[(family,oid,b)]=row
    keys=sorted({(r['family'],r['branch']) for r in rows})
    summary={family+'/'+b:aggregate([r for r in rows if r['family']==family and r['branch']==b]) for family,b in keys}
    cells={c:{family+'/'+b:aggregate([r for r in rows if r['cell']==c and r['family']==family and r['branch']==b]) for family,b in keys} for c in sorted({r['cell'] for r in rows})}
    for oid in sorted(labels):
        for b in ['L0','L1','L2']:
            results=[docs[(f'level-seed{s}',oid,b)]['value']['result'] for s in ['0','1','2']]
            seedcompare.append(dict(opaque_id=oid,branch=b,log_order_changed=any(r['log_ranks']!=results[0]['log_ranks'] for r in results),
                borda_scores_changed=any(r['scores']!=results[0]['scores'] for r in results),
                native_rank_changed=any(r['native_ranks']!=results[0]['native_ranks'] for r in results),
                root_ranks={s:bykey[(f'level-seed{s}',oid,b)]['native_rank'] for s in ['0','1','2']}))
    rootchanges=[]
    simple=read(OUT/'simple-evaluate-001/evaluation.json')
    prior={(r['opaque_id'],r['branch']):r for r in simple['rows']}
    for oid in labels:
        for b in ['M0','M1','L0','L1','L2']:
            before=prior[(oid,b)] if b.startswith('M') else bykey[('level-seed0',oid,b)]
            after=bykey[('time',oid,'T-'+b)]
            rootchanges.append(dict(opaque_id=oid,cell=labels[oid]['cell'],branch=b,
                                  before=before['native_rank'],after=after['native_rank'],
                                  changed=before['native_rank']!=after['native_rank']))
    write(folder/'summary.json',dict(summary=summary,by_cell=cells,rows=rows,hash_seed_contrasts=seedcompare,
                                    time_root_rank_contrasts=rootchanges,labels_sha256=sha(lp),
                                    interpretation='No winner chosen; native truncated API and internal score tie expectation separated'))
    lines=['# Severity và TimeStamp — kết quả bổ sung','',
           '| Nhánh | n | Top1 native | Top1 kỳ vọng tie | Top3 native | Top5 native | MRR native |','|---|---:|---:|---:|---:|---:|---:|']
    for name,s in summary.items():lines.append(f"| {name} | {s['n']} | {s['native_hit1']:.6f} | {s['expected_hit1']:.6f} | {s['native_hit3']:.6f} | {s['native_hit5']:.6f} | {s['native_mrr']:.6f} |")
    lines+=['','L0 literal +null; L1 uppercase observed +null; L2 uppercase observed, drop missing. Null!=INFO trong source không phải nhãn lỗi thật. Time projection không thêm hàng ngoài cửa sổ đã allowlist.','',
            '## Từng ô','', '| Ô | Nhánh | n | Top1 native | MRR native |','|---|---|---:|---:|---:|']
    for c,data in cells.items():
        for b,s in data.items():lines.append(f"| {c} | {b} | {s['n']} | {s['native_hit1']:.6f} | {s['native_mrr']:.6f} |")
    lines+=['','## Từng ca','', '| Ca | Nhánh | Native rank | Vị trí tie |','|---|---|---:|---|']
    for r in rows:lines.append(f"| {r['opaque_id']} | {r['family']}/{r['branch']} | {r['native_rank']} | {r['positions']} |")
    (folder/'tables.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=1))


if __name__=='__main__':main()
