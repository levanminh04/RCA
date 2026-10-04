# Ví dụ tính tay CIRCA-PC mặc định

Ca `re2tt_ts-order-service_loss_3` được chọn trước kết quả theo số cột processed nhỏ nhất trong 30 ca dev; nếu hòa dùng tên ca tăng dần (`runs/selection-before-scores.json`). Ví dụ dùng PC **mặc định**, alpha0.05, Fisher-Z, stable=True, không giới hạn depth; adjacency hoàn tất trên EC2 ở `runs/ec2-default-003/adj.npy`. Metric minh họa là top1 RHT đã lưu, không chọn bằng nhãn.

## Từ bảng metric tới graph và cửa sổ

PC nhận600 hàng từ t_d−300 tới t_d+299,273 metric. Thứ tự tên trong `nodes.json`, `input.json` và raw preprocessing độc lập khớp hoàn toàn. Kiểm byte hash, shape, identity, endpoint và graph snapshot đều PASS (`paper/pc-source-alignment.json`). Không align matrix theo field node_names có time của e2e wrapper.

Ma trận có854 cặp directed và21 cặp undirected. Adapter RCAEval đảo mọi directed edge; mỗi undirected thành hai hướng. Graph thực thi có271 node/896 edge, không DAG. Các SCC (thành phần liên thông mạnh) không tầm thường có kích thước[149, 6, 4, 2, 2, 2]. `ts-order-service_latency` nằm trong SCC149 node. Đây là cấu trúc thực thi, không phải DAG nhân quả đã được xác nhận.

Hai metric không có cạnh PC bị wrapper bỏ: `["ts-admin-travel-service_latency", "ts-order-other-service_mem"]`. CaseData còn bỏ `["ts-rebook-service_socket"]` vì hằng trong khoảng nạp. Vì vậy output có270 metric dù PC học273 metric. Không có output rỗng hoặc fallback ở cấp ca.

Mốc t_d=1706071770; train111 điểm t_d−120…t_d−10; test10 điểm t_d+291…t_d+300. Cửa sổ nạp421 điểm. Raw input đã cắt dừng ở+299, nên **+300 được fill bằng giá trị cuối +299**: source420 điểm/grid421, right_extrapolated_bins=1. Đây là thiếu endpoint trong input protocol; raw file đầy đủ còn dữ liệu sau đó. Kiểm độc lập mean-bin/nội suy/parents của270 metric và1080 mảng PASS, sai số0 (`paper/window-example-pc-001/window-comparison.json`).111/10 không tự bảo đảm từng điểm là quan sát độc lập.

## Parents và hồi quy

Các parents hiệu lực của `ts-order-service_latency` như dưới. Mỗi cặp có endpoint `[1,−1]` khi đọc `[adj[parent,node],adj[node,parent]]`: causal-learn định hướng node→parent, nhưng bước reverse của wrapper đưa parent→node vào scorer. Vì vậy không diễn giải chúng như parents kiến trúc hay dependency được paper xác nhận.

| Parent thực thi | β | Số giá trị khác nhau trong train |
|---|---:|---:|
| ts-travel2-service_mem | -0.0063568557453754877 | 5 |
| ts-consign-service_cpu | -5.8502272440313029e-05 | 39 |
| ts-admin-basic-info-service_cpu | -0.0010908665849353244 | 37 |
| ts-contacts-service_socket | 0 | 1 |

OLS có intercept b=1.7057122732641765. Ma trận111×4, rank=3; singular values=[1.388846849092163, 0.5610965108515207, 0.06304322013725959, 0.0]. Contacts socket hằng5 trên train, nên centered column bằng0 và hệ số0; regressor vẫn giải least squares, **không chuyển ValueError fallback**. Có parents và route OLS; đây không phải N-Sigma do node không cha.

Residual train có μ=7.3295973894875906e-16, population variance=6.1937529291394826e-08, scale=0.00024887251614309449. Variance lớn hơn near-constant bound1.5265712585909754e-21, nên scale=√variance, không phải scale1. Toàn bộ111 train arrays/residuals lưu trong snapshot và comparison JSON, không chỉ có một điểm minh họa.

## Mười điểm test và RHT

Ở điểm đầu tiên đạt max (t_d+296s), x=[264.675328, 0.15459783556225556, 0.29613471971067673, 6.0], y=0.39999999999999991. Tính ŷ=b+xᵀβ=0.022877306013168619; e=y−ŷ=0.37712269398683129. Vì vậy:

\[
z=\frac{0.37712269398683129-(7.3295973894875906e-16)}{0.00024887251614309449}=1515.3247929152449.
\]

| Thời gian | y | ŷ | Residual | z |
|---|---:|---:|---:|---:|
| +291s | 0.37499999999999967 | 0.022877306013168619 | 0.35212269398683105 | 1414.8717562061775 |
| +292s | 0.37499999999999967 | 0.022877306013168619 | 0.35212269398683105 | 1414.8717562061775 |
| +293s | 0.37499999999999967 | 0.022877306013168619 | 0.35212269398683105 | 1414.8717562061775 |
| +294s | 0.37499999999999967 | 0.022877306013168619 | 0.35212269398683105 | 1414.8717562061775 |
| +295s | 0.37499999999999967 | 0.022877306013168619 | 0.35212269398683105 | 1414.8717562061775 |
| +296s | 0.39999999999999991 | 0.022877306013168619 | 0.37712269398683129 | 1515.3247929152449 |
| +297s | 0.39999999999999991 | 0.022877306013168619 | 0.37712269398683129 | 1515.3247929152449 |
| +298s | 0.39999999999999991 | 0.022877306013168619 | 0.37712269398683129 | 1515.3247929152449 |
| +299s | 0.39999999999999991 | 0.022878549853092789 | 0.37712145014690712 | 1515.3197950153422 |
| +300s | 0.39999999999999991 | 0.022878549853092789 | 0.37712145014690712 | 1515.3197950153422 |

s=max|z|=1515.3247929152449; confidence=erf(s/√2)=1. Confidence bão hòa1, không phải xác suất service gốc chắc chắn là nguyên nhân. Score lớn vì conditional deviation khoảng0.35–0.38 chia cho residual normal scale khoảng0.000249. Parent graph sai, proxy regression sai, regime shift hoặc interpolation cũng có thể tạo deviation này; arithmetic không loại được các giải thích đó.

Script độc lập không gọi CIRCA/RCAEval/sklearn. Tất cả270 nodes/2160 checks gồm residual train/test, score, confidence và DA đều PASS. Max absolute error=2.2204460492503131e-16, max relative trên giá trị tham chiếu khác0=1.7208917013044475e-15. Không sàn hoặc cắt score để khớp. Kiểm số học không xác minh true causal graph.

## DA, SCC, hòa điểm và service rank

DA threshold3 giữ tất cả scored nodes. Child evidence của metric này là `{"ts-auth-service_latency": 188.43553227662613, "ts-order-other-service_latency": 459.2473175394284, "ts-ui-dashboard_socket": 1237.93406616552}`. Các child này đều≥3, nên ở riêng node này dùng trực tiếp, không đi xuyên child dưới ngưỡng. Child lớn nhất là `ts-ui-dashboard_socket` với1237.9340661655201. Score thành1515.3247929152449+1237.9340661655201=2753.258859080765; key=[2753.258859080765, -6, 1515.3247929152449]. Không chọn DA vì score lớn hơn.

Toàn graph cyclic có124 lần cần evidence của child dưới3 nhưng child chưa được xử lý ở cùng generation. So independent đã dùng **thứ tự thực tế của DAScorer** được snapshot ghi ở graph.da_iteration_order. Do đó phép khớp chứng minh đúng một lượt thực thi. Nó không biến DA trên SCC thành suy ancestor trên DAG. Fixture hashseed ở `audit/da-cycle.json` đã cho DA thay cả score khi đổi thứ tự; cần giữ giới hạn này dù top1 ca này khớp.

Có2 nhóm hòa RHT score, 3 nhóm hòa DA score, 1 nhóm hòa toàn key DA trong ca này. Danh sách ở `paper/vi-du-pc.json`. Adapter hiển thị theo tên metric tăng dần trong nhóm cùng score/key; core sorted giữ thứ tự dictionary/set khi hòa. Không có hòa ở top1 nên chính sách hiển thị không giải thích rank1 ở đây.

Nhãn được đọc sau ranking cho biết service gốc là `ts-order-service`. Dedup theo lần xuất hiện đầu cho RHT service rank1, DA service rank1; đây là adapter từ metric sang service. RHT metric tiếp theo là `ts-ui-dashboard_socket` với1237.9340661655201, nhỏ hơn top1. Các metric của service gốc:

| Metric | Hạng RHT metric | Score |
|---|---:|---:|
| ts-order-service_latency | 1 | 1515.3247929152449 |
| ts-order-service_mem | 72 | 3.8661446968077513 |
| ts-order-service_workload | 94 | 2.7303970337884218 |
| ts-order-service_cpu | 115 | 2.1883076357350935 |
| ts-order-service_diskio | 139 | 1.7753700892703912 |
| ts-order-service_socket | 190 | 1.1493718397741619 |

Service đứng đầu nhờ latency, không phải mọi metric của service đều xếp đầu. PC được học trên cả đoạn sau mốc, nên graph chứa thông tin telemetry dưới intervention; mốc và cửa sổ lấy từ chế độ tái lập đã biết. Ví dụ không chứng minh vận hành tự phát hiện không cần nhãn, không thay tái lập số KDD'22 và không cho phép chọn scorer theo rank này.
