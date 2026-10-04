# Ví dụ tính tay CIRCA kiến trúc

Ca `re2tt_ts-order-service_loss_3` được chọn trước kết quả theo số cột processed nhỏ nhất trong 30 ca dev; nếu hòa dùng tên ca tăng dần. Nguồn quy tắc: `runs/selection-before-scores.json`. Metric minh họa là top1 của ranking RHT đã lưu, không chọn bằng nhãn root. Nhãn chỉ dùng ở cuối để giải thích service rank.

## Cửa sổ và parents

Mốc t_d=1706071770. Train111 điểm từ t_d−120s tới t_d−10s; test10 điểm từ t_d+291s tới t_d+300s. Raw có nhịp1s, đủ coverage; kiểm độc lập từng mảng và effective parents PASS với sai số0 (`window-example-architecture-002/window-comparison.json`).

Metric `ts-order-service_latency` có parents theo thứ tự dưới đây. `ts-station-service_latency` đến từ call order→station và luật L_callee→L_caller; workload/Saturation của order là quan hệ nội service. Đây là cấu trúc từ trace/meta rules, không phải dùng service root để thêm cạnh.

| Parent | Hệ số β |
|---|---:|
| ts-station-service_latency | 0.078190876843173315 |
| ts-order-service_workload | 0.00046158671763060543 |
| ts-order-service_mem | 0.00062954519960666552 |
| ts-order-service_diskio | 1.7196666919237422e-09 |
| ts-order-service_cpu | 6.5589307669042504e-05 |
| ts-order-service_socket | 2.9078564300202206e-06 |

b=-0.14949284581942529. OLS rank=6; có111 mẫu và6 parents. Các111 hàng train X/y, hệ số,111 residuals đều ở `compare-example-architecture/comparison.json` và snapshot. Không chỉ soi một điểm max rồi gọi toàn scorer đúng.

## Từ regression tới score

Residual train có μ=6.3575271173636493e-17, variance=4.0157130977163111e-08, scale=0.0002003924424152845. Near-constant=False theo bound StandardScaler, nên scale=√variance. Đây không phải nhánh scale1 hay ValueError fallback.

Ở điểm t_d+296s, x=[0.007169811320754716, 0.4, 272.850944, 48328.95784785109, 0.20489366095392397, 9.0], y=0.39999999999999991. Tính ŷ=b+xᵀβ=0.023147123945248205; e=y−ŷ=0.37685287605475171. Vì vậy:

\[
z=\frac{0.37685287605475171-(6.3575271173636493e-17)}{0.0002003924424152845}=1880.5742946821233.
\]

| Thời gian | y test | Residual | z |
|---|---:|---:|---:|
| +291s | 0.37499999999999967 | 0.35187147631024407 | 1755.9119099962911 |
| +292s | 0.37499999999999967 | 0.35187147631024407 | 1755.9119099962911 |
| +293s | 0.37499999999999967 | 0.35184950199000997 | 1755.8022535642958 |
| +294s | 0.37499999999999967 | 0.35184950199000997 | 1755.8022535642958 |
| +295s | 0.37499999999999967 | 0.35184950199000997 | 1755.8022535642958 |
| +296s | 0.39999999999999991 | 0.37685287605475171 | 1880.5742946821233 |
| +297s | 0.39999999999999991 | 0.3767947985260004 | 1880.2844757246251 |
| +298s | 0.39999999999999991 | 0.37681242015967054 | 1880.3724113446401 |
| +299s | 0.39999999999999991 | 0.37675102912622566 | 1880.0660573090042 |
| +300s | 0.39999999999999991 | 0.37675102912622566 | 1880.0660573090042 |

Max|z|=1880.5742946821233, confidence=1. Confidence đã bão hòa ở1, nên nó không phân biệt được score1880 với score139 và không phải xác suất root service bằng1. Ranking chính dùng score gốc.

Independent script không gọi CIRCA/RCAEval/sklearn; so272 nodes và2176 thành phần RHT/residual/confidence/DA đều PASS. Sai số tuyệt đối lớn nhất 3.3306690738754696e-16; fullerrors ở comparison JSON/CSV. Kiểm này không tự xác minh true causal graph.

## DA và thứ hạng service

DA threshold3. Node latency này thu child evidence `{"ts-inside-payment-service_latency": 1.7265}`. Nó đủ ngưỡng nên thành 1880.5742946821233+1.7264999999999999=1882.3007946821233, key `[1882.3007946821233, -7, 1880.5742946821233]`. Parent `ts-order-service_mem` có RHT4.9145622857432079, nhận bằng chứng latency1880.5742946821233 và thành1885.4888569678665; vì vậy topmetric DA khác topmetric RHT. Không đổi scorer chính vì biến thể nào xếp đẹp hơn.

Sau khi lưu ranking, đối chiếu nhãn cho biết service gốc là `ts-order-service`. Nó đứng hạng1 khi dedup service theo lần xuất hiện đầu, vì latency của nó có score1880.5742946821233, lớn hơn mọi metric khác; metric kế tiếp là `ts-route-service_mem` với139.57500228651926. Dedup service là adapter, còn output CIRCA là metric.

Vì sao score lớn: latency test cao hơn mức regression dự đoán khoảng0.35–0.38, trong khi residual normal scale chỉ khoảng0.0002. Đây là mô tả arithmetic của ca, không phải chứng minh duy nhất về cơ chế fault. Parent graph sai, proxy regression sai, regime shift hoặc sampling cũng có thể tạo conditional deviation. Kiểm normal/normal trên chính ca có nhiều metric≥3, nên score/anomaly rank cần detector/context để có nghĩa vận hành; không suy từ ca này rằng phương pháp luôn phân biệt lỗi với nền.
