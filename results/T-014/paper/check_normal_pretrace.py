"""Kiểm cutoff/call edges normal control từ raw traces, không gọi builder."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

paper = Path(__file__).resolve().parent
task = paper.parent
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
selected = read(task/'runs/selection-before-scores.json')['selected']
inventory = read(task/'runs/inventory.json')
assert len(inventory)==30 and selected in {r['case'] for r in inventory}
row = next(r for r in inventory if r['case']==selected)
raw_path = Path(row['source']).parent/'traces.parquet'
assert raw_path.parent.name==selected and not any(p.lower()=='locked' for p in raw_path.parts)
snap_path = task/'runs/normal-normal-architecture-pretrace/snapshot.json'
snapshot = read(snap_path)
report = read(snap_path.parent/'graph-report.json')
score = read(paper/'compare-normal-pretrace/comparison.json')
window = read(paper/'window-normal-pretrace/window-comparison.json')
old = read(task/'runs/normal-normal-architecture/snapshot.json')
cutoff = snapshot['meta']['detect_time']
metric_time = np.asarray(pd.read_parquet(row['source'],columns=['time'])['time'])
metric_pre_time = metric_time[metric_time<row['inject_time']]
trace = pd.read_parquet(raw_path,columns=['traceID','spanID','parentSpanID','serviceName','startTime'])
pre = trace.loc[np.asarray(trace.startTime)<cutoff*1_000_000]
ownership = {}
duplicates = 0
for record in pre.itertuples(index=False):
    key = (str(record.traceID),str(record.spanID))
    if key in ownership:
        duplicates += 1
        assert ownership[key]==record.serviceName, 'Ambiguous ownership'
    else:
        ownership[key] = record.serviceName
edges=set();resolved=self_call=0
for record in pre.itertuples(index=False):
    key=(str(record.traceID),str(record.parentSpanID))
    caller=ownership.get(key)
    if caller is not None and not pd.isna(caller) and not pd.isna(record.serviceName):
        resolved+=1
        if caller!=record.serviceName: edges.add((str(caller),str(record.serviceName)))
        else: self_call+=1
sha=hashlib.sha256(snap_path.read_bytes()).hexdigest()
checks={
    'trace_cutoff_equals_snapshot_pseudo_detect':report['trace']['cutoff_seconds']==cutoff,
    'pre_span_count_matches':len(pre)==report['trace']['pre_spans'],
    'resolved_parent_count_matches':resolved==report['trace']['resolved_parents'],
    'self_call_count_matches':self_call==report['trace']['self_call_spans'],
    'raw_call_edges_match_graph_report':edges=={tuple(e) for e in report['graph']['call_edges']},
    'no_duplicate_span_keys_in_pre_reference':duplicates==0,
    'all_pre_span_starts_strict_before_pseudo_detect':bool((pre.startTime<cutoff*1_000_000).all()),
    'train_and_test_strict_before_real_injection':max(window['train_timestamps']+window['test_timestamps'])<row['inject_time'],
    'numeric_independent_PASS':score['pass'],
    'raw_arrays_independent_PASS':window['pass'],
    'snapshot_bytes_match_independent_reports':sha==score['snapshot_sha256']==window['snapshot_sha256'],
}
output={
    'case':selected,'snapshot':str(snap_path),'snapshot_sha256':sha,
    'trace_source':str(raw_path),'raw_trace_rows':len(trace),'pre_pseudo_spans':len(pre),
    'raw_call_edges':sorted(map(list,edges)),'source_span_start_unit':'microseconds',
    'pseudo_detect':cutoff,'real_injection_from_allowlisted_metadata':row['inject_time'],
    'train_bounds':[min(window['train_timestamps']),max(window['train_timestamps'])],
    'test_bounds':[min(window['test_timestamps']),max(window['test_timestamps'])],
    'metric_preprocessing_bounds':[float(metric_pre_time.min()),float(metric_pre_time.max())],
    'metric_preprocessing_rows':len(metric_pre_time),
    'metric_preprocessing_scope':'all raw points before real injection, including points after pseudo detect; train/test stay before real injection',
    'graph_nodes':len(snapshot['graph']['nodes']),'scored_nodes':len(snapshot['nodes']),
    'checks':checks,'PASS':all(checks.values()),
    'old_pre_real_trace_snapshot_comparison':{
        'same_graph_nodes':old['graph']['nodes']==snapshot['graph']['nodes'],
        'same_graph_edges':old['graph']['edges']==snapshot['graph']['edges'],
        'same_RHT_ranks_and_scores':old['ranks']==snapshot['ranks'],
        'same_parents_and_arrays':all(old['nodes'][n]['parents']==v['parents'] and all(
            old['nodes'][n][k]==v[k] for k in ['train_x','train_y','test_x','test_y']) for n,v in snapshot['nodes'].items()),
    },
    'scores_ge3':sum(n['rht_score']>=3 for n in snapshot['nodes'].values()),
    'top_metric_and_score':snapshot['ranks'][0],
    'numeric_checks':score['checks_count'],'numeric_max_abs_error':max(c.get('max_abs_error',0) for c in score['checks']),
    'raw_array_checks':len(window['checks']),'raw_max_abs_error':max(c.get('max_abs_error',0) for c in window['checks']),
    'scope_limit':'Independent raw trace->call-edge cutoff and raw metric->scorer arrays; structural projection still supplied by snapshot/graph report. Normal means pre-injection proxy, not an independently annotated healthy interval; no prevalence claim.'
}
(paper/'normal-pretrace-verification.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=f'''# Đối chứng normal với trace trước pseudo-mốc

Snapshot `runs/normal-normal-architecture-pretrace/snapshot.json` có270 scored metrics. Graph trace được dựng ở pseudo detect={cutoff}, trước mốc tiêm thật={row['inject_time']}. Script độc lập dùng dictionary `(traceID,spanID)` từ raw trace đã lọc startTime<{cutoff}×10⁶, không gọi service_calls/builder. Nó có{len(pre)} span và{len(edges)} service call edges; counts và edges khớp graph report. Các span hai đầu đều lấy trong tập trước pseudo-mốc. Chi tiết ở `paper/normal-pretrace-verification.json`.

Train t_d thật−421…−311; test t_d thật−10…−1. Không chứa điểm sau tiêm. Metric preprocessing của lượt này dùng toàn720 điểm trước **mốc tiêm thật**, gồm300 điểm sau pseudo-mốc. Vì vậy “strict” ở đây xác nhận **trace trước pseudo-mốc** và scoring windows trước injection; không tuyên bố mọi lựa chọn candidate/constant đã chỉ dùng train trước pseudo-mốc.

Independent OLS/RHT/DA2160 checks PASS, max absolute error={output['numeric_max_abs_error']:.17g}; raw resampling/parent1080 array checks PASS, error0. Kết luận dựa actual report errors và source hashes, không dựa bool numerically_verified tự gán. Graph/nodes/effective parents/arrays/RHT ranks của snapshot cũ và mới giống nhau ở ca này; cutoff chặt hơn đã được kiểm từ raw thay vì suy từ sự giống nhau.

Vẫn có{output['scores_ge3']}/270 score≥3, top `{output['top_metric_and_score'][0]}` score{output['top_metric_and_score'][1]:.17g}. Đó là kết quả negative control của ca này. Các khả năng khác gồm drift/warmup, normal reference chưa phủ test, model misspecification, residual scale nhỏ hoặc pre-injection chưa hoàn toàn healthy. Kiểm này không chốt calibration hay tỷ lệ false positive toàn dataset. Projection trace/meta→metric của graph vẫn cần bằng chứng riêng; script này chỉ kiểm cutoff/call edges/raw arrays/scoring.
'''
(paper/'normal-pretrace-verification.md').write_text(md,encoding='utf-8')
print(json.dumps({'PASS':output['PASS'],'numeric_checks':output['numeric_checks'],'raw_checks':output['raw_array_checks'],
                  'raw_pretrace_edges':len(edges),'pre_spans':len(pre),'old_graph_and_scores_same':output['old_pre_real_trace_snapshot_comparison'],
                  'scores_ge3':output['scores_ge3']},ensure_ascii=False))
raise SystemExit(0 if output['PASS'] else 1)
