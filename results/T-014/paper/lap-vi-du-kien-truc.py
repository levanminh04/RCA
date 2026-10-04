"""Ghi số tính tay từ các file kết quả đã lưu, không chạy phương pháp."""
import json
import hashlib
from pathlib import Path

p = Path(__file__).resolve().parent
task = p.parent
s = json.loads((task/'runs/example-architecture/snapshot.json').read_text(encoding='utf-8'))
r = json.loads((p/'compare-example-architecture/comparison.json').read_text(encoding='utf-8'))
i = json.loads((task/'runs/example-architecture/interpretation.json').read_text(encoding='utf-8'))
w = json.loads((p/'window-example-architecture-002/window-comparison.json').read_text(encoding='utf-8'))
assert r['pass'] and w['pass']
snapshot_sha = hashlib.sha256((task/'runs/example-architecture/snapshot.json').read_bytes()).hexdigest()
if r.get('snapshot_sha256') is not None:
    assert r['snapshot_sha256'] == snapshot_sha, 'Không dùng comparison cũ sau rebuild'
if w.get('snapshot_sha256') is not None:
    assert w['snapshot_sha256'] == snapshot_sha, 'Phải kiểm raw window đúng snapshot'
name = s['ranks'][0][0]  # metric top1; nhãn đã đọc sau rank ở runner.
n, c = s['nodes'][name], r['nodes'][name]
max_index = max(range(len(c['test_z'])), key=lambda j: abs(c['test_z'][j]))
parent_lines = '\n'.join(f'| {parent} | {coef:.17g} |' for parent, coef in zip(n['parents'], c['coefficients']))
z_lines = '\n'.join(f'| +{291+j}s | {n["test_y"][j]:.17g} | {c["test_residual"][j]:.17g} | {c["test_z"][j]:.17g} |' for j in range(10))
da = r['da'][name]
mem = r['da']['ts-order-service_mem']
source = {
    'case':i['case'], 'metric_selection_rule':'top1 metric of saved architecture RHT ranking',
    'metric': name, 'parents': n['parents'], 'coefficients':c['coefficients'],
    'intercept':c['intercept'], 'normal':c['normal'], 'max_test_index':max_index,
    'max_test_offset_seconds':291+max_index,
    'max_test_y':n['test_y'][max_index], 'max_test_x':n['test_x'][max_index],
    'max_test_prediction':n['test_y'][max_index]-c['test_residual'][max_index],
    'max_test_residual':c['test_residual'][max_index],
    'score':c['rht_score'], 'confidence':c['confidence'],
    'da':da, 'da_order_mem':mem,
    'root_service_after_ranking':i['root_service'], 'root_service_rank':i['root_service_rank'],
    'numeric_checks':r['checks_count'],'array_checks':len(w['checks']),
}
(p/'vi-du-kien-truc.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md = rf'''# Ví dụ tính tay CIRCA kiến trúc

Ca `{i['case']}` được chọn trước kết quả theo số cột processed nhỏ nhất trong 30 ca dev; nếu hòa dùng tên ca tăng dần. Nguồn quy tắc: `runs/selection-before-scores.json`. Metric minh họa là top1 của ranking RHT đã lưu, không chọn bằng nhãn root. Nhãn chỉ dùng ở cuối để giải thích service rank.

## Cửa sổ và parents

Mốc t_d={s['meta']['detect_time']}. Train111 điểm từ t_d−120s tới t_d−10s; test10 điểm từ t_d+291s tới t_d+300s. Raw có nhịp1s, đủ coverage; kiểm độc lập từng mảng và effective parents PASS với sai số0 (`window-example-architecture-002/window-comparison.json`).

Metric `{name}` có parents theo thứ tự dưới đây. `ts-station-service_latency` đến từ call order→station và luật L_callee→L_caller; workload/Saturation của order là quan hệ nội service. Đây là cấu trúc từ trace/meta rules, không phải dùng service root để thêm cạnh.

| Parent | Hệ số β |
|---|---:|
{parent_lines}

b={c['intercept']:.17g}. OLS rank={c['ols_rank']}; có111 mẫu và6 parents. Các111 hàng train X/y, hệ số,111 residuals đều ở `compare-example-architecture/comparison.json` và snapshot. Không chỉ soi một điểm max rồi gọi toàn scorer đúng.

## Từ regression tới score

Residual train có μ={c['normal']['mean']:.17g}, variance={c['normal']['variance']:.17g}, scale={c['normal']['scale']:.17g}. Near-constant=False theo bound StandardScaler, nên scale=√variance. Đây không phải nhánh scale1 hay ValueError fallback.

Ở điểm t_d+{291+max_index}s, x={json.dumps(n['test_x'][max_index])}, y={n['test_y'][max_index]:.17g}. Tính ŷ=b+xᵀβ={source['max_test_prediction']:.17g}; e=y−ŷ={c['test_residual'][max_index]:.17g}. Vì vậy:

\[
z=\frac{{{c['test_residual'][max_index]:.17g}-({c['normal']['mean']:.17g})}}{{{c['normal']['scale']:.17g}}}={c['test_z'][max_index]:.17g}.
\]

| Thời gian | y test | Residual | z |
|---|---:|---:|---:|
{z_lines}

Max|z|={c['rht_score']:.17g}, confidence={c['confidence']:.17g}. Confidence đã bão hòa ở1, nên nó không phân biệt được score1880 với score139 và không phải xác suất root service bằng1. Ranking chính dùng score gốc.

Independent script không gọi CIRCA/RCAEval/sklearn; so272 nodes và{r['checks_count']} thành phần RHT/residual/confidence/DA đều PASS. Sai số tuyệt đối lớn nhất {max(check.get('max_abs_error',0) for check in r['checks']):.17g}; fullerrors ở comparison JSON/CSV. Kiểm này không tự xác minh true causal graph.

## DA và thứ hạng service

DA threshold3. Node latency này thu child evidence `{json.dumps(da['child_evidence'])}`. Nó đủ ngưỡng nên thành {c['rht_score']:.17g}+{da['child_score']:.17g}={da['score']:.17g}, key `{json.dumps(da['key'])}`. Parent `ts-order-service_mem` có RHT{mem['key'][2]:.17g}, nhận bằng chứng latency{mem['child_score']:.17g} và thành{mem['score']:.17g}; vì vậy topmetric DA khác topmetric RHT. Không đổi scorer chính vì biến thể nào xếp đẹp hơn.

Sau khi lưu ranking, đối chiếu nhãn cho biết service gốc là `{i['root_service']}`. Nó đứng hạng{i['root_service_rank']} khi dedup service theo lần xuất hiện đầu, vì latency của nó có score{c['rht_score']:.17g}, lớn hơn mọi metric khác; metric kế tiếp là `{s['ranks'][1][0]}` với{s['ranks'][1][1]:.17g}. Dedup service là adapter, còn output CIRCA là metric.

Vì sao score lớn: latency test cao hơn mức regression dự đoán khoảng0.35–0.38, trong khi residual normal scale chỉ khoảng0.0002. Đây là mô tả arithmetic của ca, không phải chứng minh duy nhất về cơ chế fault. Parent graph sai, proxy regression sai, regime shift hoặc sampling cũng có thể tạo conditional deviation. Kiểm normal/normal trên chính ca có nhiều metric≥3, nên score/anomaly rank cần detector/context để có nghĩa vận hành; không suy từ ca này rằng phương pháp luôn phân biệt lỗi với nền.
'''
(p/'vi-du-kien-truc.md').write_text(md,encoding='utf-8')
print(json.dumps({'metric':name,'score':c['rht_score'],'example_source_files_verified':True},ensure_ascii=False))
