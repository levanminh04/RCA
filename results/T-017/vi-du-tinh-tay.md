# Ví dụ tính tay và tính độc lập

Ca chọn trước khi xem kết quả bằng rule SPEC: tên đầu thứ tự từ điển trong allowlist30dev, **re2tt_ts-auth-service_cpu_1**. Metadata/mốc và hash nguồn ở run004 summary, `sources/injection-manifest.json`; normalized inputs tại `D:/RCA-ext/work/T-017/example-input-run-dev-004/`. Bản normalized cũ được giữ riêng. Quy ước M4 **(quy ước triển khai T017, xem docs/WHY.md WHY-17; chưa chốt P3)**.

## 1. Chia cửa sổ và tính mọi ứng viên

Adapter chia normal[t−300,t), incident[t,t+300), không dùng root để chọn cột. Tính 369 kênh của 68 entity, gồm DB chưa gộp. Script `scripts/independent_example.py` đọc normalized CSV, tự viết mean/std/count/percentile/fusion/tie, **không import hoặc gọi lõi/adapter chính**. 12 nhóm self-test known-answer độc lập kiểm trước phép so. Phép so này kiểm score engine, không tự chứng minh adapter raw→CSV; schema/boundary/alias có kiểm riêng.

## 2. Các phép tính metric

Để người đọc thấy phép cộng, bảng dưới chỉ trình bày một entity; phần tính độc lập trước đó đã làm mọi entity. Nhãn root chỉ dùng sau khi JSON thứ hạng đã được ghi. Mỗi θ=μ+3σ, mỗi điểm x>θ được1 cảnh báo; equality không tính. Bảng làm tròn để đọc, số fullprecision ở `vi-du-metric.csv`.

| Kênh | μ | σ(ddof0) | θ | Normal finite | Incident finite | Count vượt θ |
|---|---:|---:|---:|---:|---:|---:|
| cpu | 13.9820521 | 1.25574399 | 17.749284 | 300 | 297 | 293 |
| diskio | 49831.8835 | 14993.2803 | 94811.7246 | 300 | 297 | 40 |
| latency-50 | 0.178932756 | 0.00291813192 | 0.187687151 | 300 | 300 | 279 |
| latency-90 | 0.250265551 | 0.018542502 | 0.305893057 | 300 | 300 | 279 |
| mem | 257349018 | 6076.50033 | 257367247 | 300 | 300 | 297 |
| socket | 13.5333333 | 0.579271573 | 15.2711481 | 300 | 300 | 252 |
| workload | 2.8133 | 0.213987328 | 3.45526198 | 300 | 300 | 0 |

Ví dụ CPU: θ=13.982052080+3×1.255743985=17.749284036; đếm 293 điểm trên ngưỡng. CPU/diskio có3 điểm incident thiếu; không ffill và không coi thiếu là0. Tổng metric = 293+40+279+279+297+252+0=1440. Không lọc latency/mem/socket dù tên ca nói CPU.

## 3. Trace, log và điểm cuối

Trace entity này có 2105 span normal, 2085 incident. P95normal=161529, P95incident=401617, threshold3×normal=484587. P95incident<threshold nên phiếu trace0. Đơn vị vật lý OPEN; so cùng nguồn không cần đổi đơn vị. Đây là gộp span durations theo entity, chưa chứng minh service-latency end-to-end.

Ca không có logs.parquet. Log status=unavailable, đóng góp0 để cộng phần còn quan sát; không khẳng định error count0. Điểm cuối S=1440+0+0=1440.

| Hạng hiển thị | Entity | Metric | Trace | Log đóng góp | Score |
|---|---|---:|---:|---:|---:|
| 1 | ts-auth-service | 1440 | 0 | 0 | 1440 |
| 2 | ts-ui-dashboard | 369 | 0 | 0 | 369 |
| 3 | ts-config-service | 328 | 0 | 0 | 328 |
| 4 | ts-user-service | 268 | 0 | 0 | 268 |
| 5 | ts-contacts-service | 238 | 0 | 0 | 238 |
| 6 | ts-preserve-mongo | 222 | 0 | 0 | 222 |
| 7 | ts-payment-service | 220 | 0 | 0 | 220 |
| 8 | ts-order-other-service | 216 | 0 | 0 | 216 |

Nguồn mọi ô: `vi-du-score.csv`, JSON diagnosis run004 và `runs/independent-example-v2.json`. Sau khi ranking cố định, evaluator đọc root=ts-auth-service: root đứng1 vì score1440 cao nhất, không có hòa ở đầu. Đây là giải thích **cơ chế xếp hạng**, không chứng minh CPU hay service này là nguyên nhân bằng causal inference. Các nguyên nhân khác của điểm cao gồm mức tiêm mạnh, persistence, nhiều kênh tương quan và baseline ít biến động; task chưa phân xử chúng.

## 4. Khớp độc lập và biến thể đã khóa

`runs/example-comparison-v2.json`: 2226 so sánh đạt; count/score/ranking bằng tuyệt đối. Float dùng tolerance1e−10 tương đối hoặc tuyệt đối, max absolute error=1.16415321827e-10; không nói mọi absolute error nhỏ hơn1e−10. Sai khác làm tròn thống kê không đổi count/vote/score.

| Biến thể | Score entity ví dụ | Metric | Trace | Log |
|---|---:|---:|---:|---:|
| p95 | 1488 | 1488 | 0 | 0 |
| channels | 6 | 6 | 0 | 0 |
| log1 | 1440 | 1440 | 0 | 0 |
| log10 | 1440 | 1440 | 0 | 0 |
| trace2 | 1441 | 1440 | 1 | 0 |
| trace4 | 1440 | 1440 | 0 | 0 |
| half600 | 2903 | 2903 | 0 | 0 |

Nguồn `runs/run-dev-004/sensitivity.json`; không chọn winner theo accuracy. Ngưỡng log1/10 trên ca thiếu log không phân xử được log rule. Vì vậy kiểm thêm ca thứ hai có log, rule chọn cũng theo allowlist: re2tt_ts-auth-service_cpu_2. Ngưỡng0/1/10 đều có một entity nhận phiếu log, score/ranking không đổi; keyword count được tính lại độc lập bằng substring ba từ rồi so từng entity (`runs/supplement-001/summary.json`). Không ngoại suy ổn định này cho ca/dataset khác.
