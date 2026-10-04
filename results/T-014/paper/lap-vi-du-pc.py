"""Xuất ví dụ tính tay PC default từ kết quả đã lưu; không chạy phương pháp."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path

import numpy as np

paper = Path(__file__).resolve().parent
task = paper.parent
snapshot_path = task / 'runs/example-pc/snapshot.json'
s = json.loads(snapshot_path.read_text(encoding='utf-8'))
r = json.loads((paper/'compare-example-pc-001/comparison.json').read_text(encoding='utf-8'))
w = json.loads((paper/'window-example-pc-001/window-comparison.json').read_text(encoding='utf-8'))
a = json.loads((paper/'pc-source-alignment.json').read_text(encoding='utf-8'))
sha = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
assert r['pass'] and w['pass'] and a['pass']
assert sha == r['snapshot_sha256'] == w['snapshot_sha256']
name = s['ranks'][0][0]  # Chọn top1 trước khi đọc nhãn.
n, c, da = s['nodes'][name], r['nodes'][name], r['da'][name]
maximum = max(range(len(c['test_z'])), key=lambda j: abs(c['test_z'][j]))
assert c['regression_route'] == 'OLS' and not c['regression_fallback']
assert len(n['train_y']) == 111 and len(n['test_y']) == 10
def tied_groups(ranks, full_key=False):
    groups = defaultdict(list)
    for row in ranks:
        groups[tuple(row[2]) if full_key else row[1]].append(row[0])
    return [{'key': key, 'metrics': values} for key, values in groups.items() if len(values) > 1]

ties_rht = tied_groups(s['ranks'])
ties_da_score, ties_da_key = tied_groups(s['ranks_da']), tied_groups(s['ranks_da'], True)
# Nhãn được mở sau khi ranking/top1 đã tồn tại. Đây chỉ là diễn giải kết quả.
i = json.loads((task/'runs/example-pc/interpretation.json').read_text(encoding='utf-8'))
def services(ranks):
    result = []
    for metric, *_ in ranks:
        service = metric.split('_')[0]
        if service not in result:
            result.append(service)
    return result
root_rht = services(s['ranks']).index(i['root_service']) + 1
root_da = services(s['ranks_da']).index(i['root_service']) + 1
names = json.loads((task/'runs/ec2-default-003/nodes.json').read_text(encoding='utf-8'))
adj = np.load(task/'runs/ec2-default-003/adj.npy', allow_pickle=False)
target_index = names.index(name)
train_x = np.asarray(n['train_x'])
parents = [dict(label=label, coefficient=coef,
                unique_train_values=len(set(train_x[:,j])),
                adjacency_parent_node=[int(adj[names.index(label), target_index]),
                                       int(adj[target_index, names.index(label)])])
           for j,(label,coef) in enumerate(zip(n['parents'],c['coefficients']))]
test = [dict(offset_seconds=291+j, x=n['test_x'][j], y=n['test_y'][j],
             prediction=n['test_y'][j]-c['test_residual'][j],
             residual=c['test_residual'][j], z=c['test_z'][j]) for j in range(10)]
source = {
    'case': i['case'], 'configuration': 'default PC alpha .05/Fisher-Z/stable, no depth cap; RHT reference + diagnostic DA threshold3',
    'snapshot_sha256': sha, 'metric_selection_rule': 'top1 of saved RHT ranking; root label read only afterward',
    'metric': name, 'parents': parents, 'intercept': c['intercept'],
    'ols_rank': c['ols_rank'], 'singular_values': c['ols_singular_values'],
    'normal': c['normal'], 'regression_route': c['regression_route'],
    'test': test, 'first_max_index': maximum, 'rht_score': c['rht_score'],
    'confidence': c['confidence'], 'DA': da,
    'graph': {'nodes': a['edge_node_count'], 'edges': a['rebuilt_edge_count'],
              'is_DAG': a['is_DAG'], 'nontrivial_SCC_sizes': [len(v) for v in a['nontrivial_SCCs']],
              'selected_metric_SCC_size': len(a['selected_metric_SCC']),
              'selected_metric_SCC': a['selected_metric_SCC'],
              'endpoint_pair_counts': a['endpoint_pair_counts'],
              'isolates_dropped': a['source_isolates_dropped_by_wrapper'],
              'CaseData_pruned': a['graph_nodes_pruned_by_CaseData']},
    'raw_to_grid': w['raw_to_grid'][name],
    'tie_groups': {'RHT_score': ties_rht, 'DA_score': ties_da_score, 'DA_full_key': ties_da_key},
    'DA_unresolved_child_evidence_count': len(r['DA_unresolved_child_evidence']),
    'root_service_after_ranking': i['root_service'], 'root_RHT_service_rank': root_rht,
    'root_DA_service_rank': root_da, 'root_metrics_RHT': i['root_metrics'],
    'checks': {'numeric_count': r['checks_count'], 'window_arrays': len(w['checks']),
               'numeric_max_abs_error': max(v.get('max_abs_error',0) for v in r['checks']),
               'numeric_max_relative_nonzero': max(v.get('max_relative_error_nonzero_reference',0) for v in r['checks']),
               'array_max_abs_error': max(v.get('max_abs_error',0) for v in w['checks']),
               'all_PASS': True},
}
(paper/'vi-du-pc.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
parent_table = '\n'.join(f'| {p["label"]} | {p["coefficient"]:.17g} | {p["unique_train_values"]} |' for p in parents)
test_table = '\n'.join(f'| +{t["offset_seconds"]}s | {t["y"]:.17g} | {t["prediction"]:.17g} | {t["residual"]:.17g} | {t["z"]:.17g} |' for t in test)
root_table = '\n'.join(f'| {m["metric"]} | {m["rank"]} | {m["score"]:.17g} |' for m in i['root_metrics'])
max_point = test[maximum]
child = max(da['child_evidence'], key=da['child_evidence'].get)
md = rf'''# Ví dụ tính tay CIRCA-PC mặc định

Ca `{i['case']}` được chọn trước kết quả theo số cột processed nhỏ nhất trong 30 ca dev; nếu hòa dùng tên ca tăng dần (`runs/selection-before-scores.json`). Ví dụ dùng PC **mặc định**, alpha0.05, Fisher-Z, stable=True, không giới hạn depth; adjacency hoàn tất trên EC2 ở `runs/ec2-default-003/adj.npy`. Metric minh họa là top1 RHT đã lưu, không chọn bằng nhãn.

## Từ bảng metric tới graph và cửa sổ

PC nhận600 hàng từ t_d−300 tới t_d+299,273 metric. Thứ tự tên trong `nodes.json`, `input.json` và raw preprocessing độc lập khớp hoàn toàn. Kiểm byte hash, shape, identity, endpoint và graph snapshot đều PASS (`paper/pc-source-alignment.json`). Không align matrix theo field node_names có time của e2e wrapper.

Ma trận có{a['endpoint_pair_counts']['directed_pairs']} cặp directed và{a['endpoint_pair_counts']['undirected_pairs']} cặp undirected. Adapter RCAEval đảo mọi directed edge; mỗi undirected thành hai hướng. Graph thực thi có{a['edge_node_count']} node/{a['rebuilt_edge_count']} edge, không DAG. Các SCC (thành phần liên thông mạnh) không tầm thường có kích thước{json.dumps(source['graph']['nontrivial_SCC_sizes'])}. `{name}` nằm trong SCC{len(a['selected_metric_SCC'])} node. Đây là cấu trúc thực thi, không phải DAG nhân quả đã được xác nhận.

Hai metric không có cạnh PC bị wrapper bỏ: `{json.dumps(a['source_isolates_dropped_by_wrapper'])}`. CaseData còn bỏ `{json.dumps(a['graph_nodes_pruned_by_CaseData'])}` vì hằng trong khoảng nạp. Vì vậy output có270 metric dù PC học273 metric. Không có output rỗng hoặc fallback ở cấp ca.

Mốc t_d={s['meta']['detect_time']}; train111 điểm t_d−120…t_d−10; test10 điểm t_d+291…t_d+300. Cửa sổ nạp421 điểm. Raw input đã cắt dừng ở+299, nên **+300 được fill bằng giá trị cuối +299**: source420 điểm/grid421, right_extrapolated_bins=1. Đây là thiếu endpoint trong input protocol; raw file đầy đủ còn dữ liệu sau đó. Kiểm độc lập mean-bin/nội suy/parents của270 metric và1080 mảng PASS, sai số0 (`paper/window-example-pc-001/window-comparison.json`).111/10 không tự bảo đảm từng điểm là quan sát độc lập.

## Parents và hồi quy

Các parents hiệu lực của `{name}` như dưới. Mỗi cặp có endpoint `[1,−1]` khi đọc `[adj[parent,node],adj[node,parent]]`: causal-learn định hướng node→parent, nhưng bước reverse của wrapper đưa parent→node vào scorer. Vì vậy không diễn giải chúng như parents kiến trúc hay dependency được paper xác nhận.

| Parent thực thi | β | Số giá trị khác nhau trong train |
|---|---:|---:|
{parent_table}

OLS có intercept b={c['intercept']:.17g}. Ma trận111×4, rank={c['ols_rank']}; singular values={json.dumps(c['ols_singular_values'])}. Contacts socket hằng5 trên train, nên centered column bằng0 và hệ số0; regressor vẫn giải least squares, **không chuyển ValueError fallback**. Có parents và route OLS; đây không phải N-Sigma do node không cha.

Residual train có μ={c['normal']['mean']:.17g}, population variance={c['normal']['variance']:.17g}, scale={c['normal']['scale']:.17g}. Variance lớn hơn near-constant bound{c['normal']['near_constant_upper_bound']:.17g}, nên scale=√variance, không phải scale1. Toàn bộ111 train arrays/residuals lưu trong snapshot và comparison JSON, không chỉ có một điểm minh họa.

## Mười điểm test và RHT

Ở điểm đầu tiên đạt max (t_d+{max_point['offset_seconds']}s), x={json.dumps(max_point['x'])}, y={max_point['y']:.17g}. Tính ŷ=b+xᵀβ={max_point['prediction']:.17g}; e=y−ŷ={max_point['residual']:.17g}. Vì vậy:

\[
z=\frac{{{max_point['residual']:.17g}-({c['normal']['mean']:.17g})}}{{{c['normal']['scale']:.17g}}}={max_point['z']:.17g}.
\]

| Thời gian | y | ŷ | Residual | z |
|---|---:|---:|---:|---:|
{test_table}

s=max|z|={c['rht_score']:.17g}; confidence=erf(s/√2)={c['confidence']:.17g}. Confidence bão hòa1, không phải xác suất service gốc chắc chắn là nguyên nhân. Score lớn vì conditional deviation khoảng0.35–0.38 chia cho residual normal scale khoảng0.000249. Parent graph sai, proxy regression sai, regime shift hoặc interpolation cũng có thể tạo deviation này; arithmetic không loại được các giải thích đó.

Script độc lập không gọi CIRCA/RCAEval/sklearn. Tất cả270 nodes/{r['checks_count']} checks gồm residual train/test, score, confidence và DA đều PASS. Max absolute error={source['checks']['numeric_max_abs_error']:.17g}, max relative trên giá trị tham chiếu khác0={source['checks']['numeric_max_relative_nonzero']:.17g}. Không sàn hoặc cắt score để khớp. Kiểm số học không xác minh true causal graph.

## DA, SCC, hòa điểm và service rank

DA threshold3 giữ tất cả scored nodes. Child evidence của metric này là `{json.dumps(da['child_evidence'])}`. Các child này đều≥3, nên ở riêng node này dùng trực tiếp, không đi xuyên child dưới ngưỡng. Child lớn nhất là `{child}` với{da['child_score']:.17g}. Score thành{s['nodes'][name]['rht_score']:.17g}+{da['child_score']:.17g}={da['score']:.17g}; key={json.dumps(da['key'])}. Không chọn DA vì score lớn hơn.

Toàn graph cyclic có{len(r['DA_unresolved_child_evidence'])} lần cần evidence của child dưới3 nhưng child chưa được xử lý ở cùng generation. So independent đã dùng **thứ tự thực tế của DAScorer** được snapshot ghi ở graph.da_iteration_order. Do đó phép khớp chứng minh đúng một lượt thực thi. Nó không biến DA trên SCC thành suy ancestor trên DAG. Fixture hashseed ở `audit/da-cycle.json` đã cho DA thay cả score khi đổi thứ tự; cần giữ giới hạn này dù top1 ca này khớp.

Có{len(ties_rht)} nhóm hòa RHT score, {len(ties_da_score)} nhóm hòa DA score, {len(ties_da_key)} nhóm hòa toàn key DA trong ca này. Danh sách ở `paper/vi-du-pc.json`. Adapter hiển thị theo tên metric tăng dần trong nhóm cùng score/key; core sorted giữ thứ tự dictionary/set khi hòa. Không có hòa ở top1 nên chính sách hiển thị không giải thích rank1 ở đây.

Nhãn được đọc sau ranking cho biết service gốc là `{i['root_service']}`. Dedup theo lần xuất hiện đầu cho RHT service rank{root_rht}, DA service rank{root_da}; đây là adapter từ metric sang service. RHT metric tiếp theo là `{s['ranks'][1][0]}` với{s['ranks'][1][1]:.17g}, nhỏ hơn top1. Các metric của service gốc:

| Metric | Hạng RHT metric | Score |
|---|---:|---:|
{root_table}

Service đứng đầu nhờ latency, không phải mọi metric của service đều xếp đầu. PC được học trên cả đoạn sau mốc, nên graph chứa thông tin telemetry dưới intervention; mốc và cửa sổ lấy từ chế độ tái lập đã biết. Ví dụ không chứng minh vận hành tự phát hiện không cần nhãn, không thay tái lập số KDD'22 và không cho phép chọn scorer theo rank này.
'''
(paper/'vi-du-pc.md').write_text(md, encoding='utf-8')
print(json.dumps({'metric': name, 'RHT':c['rht_score'], 'DA': da['score'],
                  'service_ranks': [root_rht,root_da], 'tie_groups': [len(ties_rht),len(ties_da_score),len(ties_da_key)],
                  'source_checks_PASS':True},ensure_ascii=False))
