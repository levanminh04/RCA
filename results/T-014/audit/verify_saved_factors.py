"""Independent recount of saved ranking metrics and conditional factor effects."""
import json,math
from pathlib import Path
out=Path('D:/RCA-flashticket/results/T-014/audit');s=json.loads((out/'graph-factor-summary.json').read_text())
recounts={};details=[];bad=[]
for row in s['per_case']:
    answer=row['case'].split('/')[1].split('_')[0];base=json.loads(Path(row['modes']['forward_keep']['source']).read_text());baseline=base['scores']
    for mode,item in row['modes'].items():
        r=json.loads(Path(item['source']).read_text());points=r['scores'] if mode=='forward_keep' else r['points'];ranks=r['ranks_author_stable_sort'] if mode=='forward_keep' else r['ranks']
        assert set(points)==set(ranks) and len(ranks)==len(set(ranks)) and points and all(math.isfinite(v) for v in points.values())
        assert all(points[ranks[i]]>=points[ranks[i+1]] for i in range(len(ranks)-1))
        services=[]
        for name in ranks:
            service=name.split('_')[0].replace('-db','')
            if service not in services:services.append(service)
        # Independent mean of five top-k hits, not the rank shortcut.
        average=sum(answer in services[:k] for k in range(1,6))/5
        assert abs(average-item['Avg5'])<1e-12
        recounts.setdefault(mode,[]).append(average)
        if mode=='forward_drop':
            mismatches=[n for n in points if not math.isclose(points[n],baseline[n],abs_tol=1e-7,rel_tol=1e-7)]
            details.append(dict(case=row['case'],forward_drop_changed_remaining_points=mismatches))
            if mismatches:bad.append(row['case'])
aggregate={mode:sum(values)/len(values) for mode,values in recounts.items()}
assert all(abs(aggregate[k]-s['aggregate_Avg5'][k])<1e-12 for k in aggregate)
report=dict(pass_=not bad,cases=25,configurations=100,score_rank_valid=True,independent_topk_recounts_match=True,forward_drop_remaining_points_match=not bad,aggregate=aggregate,details=details)
(out/'graph-factor-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='details'}));assert report['pass_']
