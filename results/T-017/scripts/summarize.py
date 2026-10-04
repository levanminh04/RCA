"""All manuscript numbers are derived from preserved result files."""
import csv,json,math
from pathlib import Path
out=Path('D:/RCA-flashticket/results/T-017');run=out/'runs/run-dev-004'
rows=json.loads((run/'summary.json').read_text(encoding='utf-8'))
assert len(rows)==30 and set(x['case'] for x in rows)==set(json.loads((out/'allowlist.json').read_text()))
assert all(x['status']!='failed' for x in rows)
main=json.loads((run/'re2tt_ts-auth-service_cpu_1.json').read_text(encoding='utf-8'))
summary={'source_run':'run-dev-004','cases':len(rows),'hit1_sum':sum(x['top1']['hit_fractional'] for x in rows),
         'hit1_fractional':sum(x['top1']['hit_fractional'] for x in rows)/len(rows),
         'hit3_fractional':sum(x['top3']['hit_fractional'] for x in rows)/len(rows),
         'hit5_fractional':sum(x['top5']['hit_fractional'] for x in rows)/len(rows),
         'mrr_fractional':sum(x['top1']['mrr_fractional'] for x in rows)/len(rows),
         'repeat_exact':all(x['checks'].get('repeat_exact',True) for x in rows),
         'permutation_exact':all(x['checks'].get('permutation_exact',True) for x in rows),
         'repeat_checked_cases':sum('repeat_exact' in x['checks'] for x in rows),
         'permutation_checked_cases':sum('permutation_exact' in x['checks'] for x in rows),
         'nonempty':all(x['checks']['nonempty'] for x in rows),
         'not_fallback':all(x['checks']['not_fallback'] for x in rows),
         'score_sum':all(x['checks']['score_sum'] for x in rows),
         'column_order_matches':sum(x['checks']['ranking_equals_metric_column_order'] for x in rows),
         'normal_controls':[{'case':x['case'],**x['normal_control']} for x in rows if 'normal_control' in x],
         'logs_unavailable_cases':[], 'official_timing':False,'example_services':len(main['scores']),
         'example_metrics':len(main['metrics']),'example_root_score':main['scores']['ts-auth-service'],
         'example_top2_score':main['scores'][main['ranks'][1]]}
for row in rows:
    r=json.loads(Path(row['score_file']).read_text(encoding='utf-8'))
    if all(v['status']=='unavailable' for v in r['logs'].values()):summary['logs_unavailable_cases'].append(row['case'])
    assert 'ts' not in r['scores'], 'false service from old regex'
type_rows=list(csv.DictReader((out/'ty-le-type-cong-bo.csv').open(encoding='utf-8')))
summary['published_table3_arithmetic']=[]
for row in type_rows:
    a=float(row['type_I_rate']);b=float(row['type_II_rate']);c=float(row['type_I_II_rate'])
    if abs(a+b-c)>0.015+1e-12:
        summary['published_table3_arithmetic'].append({'dataset':row['dataset'],'type_I':a,'type_II':b,'I_II':c,'displayed_sum':a+b,'exceeds_three_rounding_intervals':True})
(out/'runs/final-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
with (out/'diem-dev.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(['ca','trang_thai','hit1_fractional','hit1_pessimistic','hit1_optimistic','hit3_fractional','hit5_fractional','mrr_fractional','file_ket_qua'])
    for row in rows:w.writerow([row['case'],row['status'],row['top1']['hit_fractional'],row['top1']['hit_pessimistic'],row['top1']['hit_optimistic'],row['top3']['hit_fractional'],row['top5']['hit_fractional'],row['top1']['mrr_fractional'],row['score_file']])
cols=['metric','mean','std0','threshold','normal_finite','incident_finite','alert_count']
with (out/'vi-du-metric.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(cols)
    for key,v in main['metrics'].items():
        if v['service']=='ts-auth-service':w.writerow([key,v.get('mean'),v.get('std'),v.get('threshold'),v['n_normal'],v['n_incident'],v['count']])
with (out/'vi-du-score.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(['thu_tu_hien_thi','service','metric','trace','log','score'])
    for i,s in enumerate(main['ranks'],1):w.writerow([i,s,*[main['scores'][s][x] for x in ('metric','trace','log','score')]])
print(json.dumps(summary,ensure_ascii=False,indent=2))
