# Ví dụ tính tay — hai ca chọn trước khi nhìn kết quả

Nguồn mọi số: `results\T-013\runs\20261004-083543`; run được trỏ bởi `kiem-tra.json`. Code independent/official ở `scripts/kiem_co_che.py`; file CSV ghi từng metric, quantile/mean/std/scale và điểm. MốcA dùng lại T-006, không benchmark toàn dataset. Mọi thời gian chỉ tham khảo trên máy bận.

## 1. Quy tắc và đầu vào

- TT: `re2tt_ts-auth-service_delay_3`, shape [1441, 360]; chọn theo rule SPEC. Timestamp injection 1708817505 cùng đơn vị giây với time. Nhãn root chỉ nối sau khi lưu ranks.
- OB: `fse-ob/cartservice_cpu/1`, shape [721, 58]; chọn theo rule SPEC. Timestamp injection 1692569339 cùng đơn vị giây với time. Nhãn root chỉ nối sau khi lưu ranks.

TT là metrics.parquet lớn nhất trong 30 ca dev, không phải ca có tổng metrics+trace lớn nhất củaT-005. OB trùng hash mẫu README (một bản trùng); không chọn vì rank đẹp. Hash trong chon-ca/manifest. Rule ca/mapping dùng để minh họa **chờ WHY, xem de-xuat-tai-lieu-chung.md**.

## 2. Tính RobustScorer và N-Sigma từng bước


### TT: vì sao root (service gốc) `ts-auth-service` đứng ở hạng đó

| Window/scorer | Metric | median hoặc mean | IQR hoặc std | scale hiệu dụng | max hậu | điểm |
|---|---|---:|---:|---:|---:|---:|
| 10/robust | ts-user-service_latency | 0.02307142857 | 0.0003924107143 | 0.0003924107143 | 0.03625 | 33.58361775 |
| 10/robust | ts-consign-price-service_latency | 0.02335713545 | 0.0004285714286 | 0.0004285714286 | 0.0325 | 21.33335062 |
| 10/robust | ts-auth-service_latency | 0.7706896552 | 0.23984375 | 0.23984375 | 1.942857143 | 4.887212978 |
| 10/standard | ts-user-service_latency | 0.02305118686 | 0.000311573844 | 0.000311573844 | 0.03625 | 42.36174951 |
| 10/standard | ts-consign-price-service_latency | 0.0232482293 | 0.0002831484939 | 0.0002831484939 | 0.0325 | 32.67462445 |
| 10/standard | ts-auth-service_latency | 0.7552615784 | 0.1781618551 | 0.1781618551 | 1.942857143 | 6.66582397 |
| 20/robust | ts-consign-price-service_latency | 0.0235 | 0.0001427091535 | 0.0001427091535 | 0.0325 | 63.06533099 |
| 20/robust | ts-config-service_latency | 0.009622340426 | 0.000289427261 | 0.000289427261 | 0.02081578947 | 38.67448079 |
| 20/robust | ts-auth-service_latency | 0.7728448276 | 0.2464320959 | 0.2464320959 | 2.030769231 | 5.104547761 |
| 20/standard | ts-config-service_latency | 0.00958422963 | 0.0002247200149 | 0.0002247200149 | 0.02081578947 | 49.98023807 |
| 20/standard | ts-news-service_mem | 1.983249067 | 0.005857323761 | 0.005857323761 | 2.076672 | 15.94976429 |
| 20/standard | ts-auth-service_latency | 0.7698261067 | 0.1864572118 | 0.1864572118 | 2.030769231 | 6.762640674 |

| Window/scorer | Root service rank | Số service đứng trước | Metric thắng của root | Điểm root |
|---|---:|---:|---|---:|
| 10/robust | 11 | 10 | ts-auth-service_latency | 4.887212978 |
| 10/standard | 10 | 9 | ts-auth-service_latency | 6.66582397 |
| 20/robust | 24 | 23 | ts-auth-service_latency | 5.104547761 |
| 20/standard | 13 | 12 | ts-auth-service_latency | 6.762640674 |

Ví dụ thế số metric đầu RobustScorer L10: (0.03625 − 0.02307142857)/0.0003924107143 = 33.58361775. Vì sort giảm rồi bỏ trùng service, root đứng sau đúng số service trong bảng. Đây là lý do số học của thứ hạng, chưa chứng minh service đứng đầu là nguyên nhân thật.

Ở ca TT này, nhiều latency service khác lệch mạnh hơn metric của auth. Khả năng khác gồm latency nền rất nhỏ, symptom/tải đổi, thiếu metric phản ánh lỗi tại root hoặc loại cột hằng; task không xác minh lan truyền/nhân quả. Không gọi thứ hạng này là bằng chứng đồ thị có ích.

### OB: vì sao root (service gốc) `cartservice` đứng ở hạng đó

| Window/scorer | Metric | median hoặc mean | IQR hoặc std | scale hiệu dụng | max hậu | điểm |
|---|---|---:|---:|---:|---:|---:|
| 10/robust | cartservice_mem | 41.0624 | 0.02048 | 0.02048 | 45.64992 | 224 |
| 10/robust | checkoutservice_latency | 0.04781195597 | 0.001443794946 | 0.001443794946 | 0.2421186441 | 134.5805293 |
| 10/standard | recommendationservice_mem | 47.98076245 | 0.0009203602526 | 0.0009203602526 | 48.25088 | 293.4911041 |
| 10/standard | cartservice_mem | 41.06336939 | 0.02705654924 | 0.02705654924 | 45.64992 | 169.5172054 |
| 20/robust | cartservice_mem | 41.0624 | 0.028672 | 0.028672 | 45.682688 | 161.1428571 |
| 20/robust | checkoutservice_latency | 0.04774074074 | 0.001289507009 | 0.001289507009 | 0.2421186441 | 150.7381518 |
| 20/standard | cartservice_mem | 41.06006756 | 0.03028937756 | 0.03028937756 | 45.682688 | 152.615234 |
| 20/standard | cartservice_cpu | 5.345519934 | 0.6372129473 | 0.6372129473 | 30.02759025 | 38.73441432 |

| Window/scorer | Root service rank | Số service đứng trước | Metric thắng của root | Điểm root |
|---|---:|---:|---|---:|
| 10/robust | 1 | 0 | cartservice_mem | 224 |
| 10/standard | 2 | 1 | cartservice_mem | 169.5172054 |
| 20/robust | 1 | 0 | cartservice_mem | 161.1428571 |
| 20/standard | 1 | 0 | cartservice_mem | 152.615234 |

Ví dụ thế số metric đầu RobustScorer L10: (45.64992 − 41.0624)/0.02048 = 224. Vì sort giảm rồi bỏ trùng service, root đứng sau đúng số service trong bảng. Đây là lý do số học của thứ hạng, chưa chứng minh service đứng đầu là nguyên nhân thật.

Ở OB L10 N-Sigma, recommendationservice_mem có nền std rất nhỏ nên lên trước cartservice; RobustScorer giữ cartservice đầu. Đổi L20 thay nền/cực đại và N-Sigma đưa cartservice lên đầu. Điều này có thể do gai nền, xu thế hoặc snapshot, không tự chứng minh tính khái quát của một scorer.

## 3. Nối mốc A của OB

Cùng bytes mẫu README, tiền xử lýread_data tương đương khi không cắt quanh injection; dùng điểm 243 đã được T-006 tái lập BOCPD. T-013 không chạy lại BOCPD full OB, chỉ tính lại từng điểm ranker độc lập tại 243. Đây là điểm đầu được detector trả, không phải mốc injection 360 trong file.

| Hạng metric | Metric | Điểm độc lập=official |
|---:|---|---:|
| 1 | checkoutservice_latency | 124.1631508 |
| 2 | cartservice_mem | 94.16666667 |
| 3 | cartservice_latency | 39.91132957 |
| 4 | cartservice_cpu | 23.05193308 |
| 5 | main_mem | 5.882352941 |

Top 5 metric trùngREADME. Gộp service làm checkoutservice hạng1, cartservice hạng2; lỗiCPU ở cartservice không có nghĩa metricCPU phải cao nhất. Avg@5=0.86 mốc A tập lấy từ `trung-gian/T006-moc-A-reused.json`; không tính Avg@5 toàn tập từ ví dụ này.

## 4. BOCPD: một bước posterior và hai prefix thật

Với prior một chiều, x1=0: density=0.3535533906; mass đổi đoạn=0.007071067812, mass kéo dài=0.3464823228; chia tổng trở thành q1=(0.02,0.98). Giá trị chính xác trong check `hand-prior-density`. Với ca đa biến, cùng công thức mass/normalization; dimension và x1 khác nên density khác, posterior bước1 vẫn(q0,q1)=(0.02,0.98) nếu hữu hạn.

| Ca prefix | T | d sau preprocessing | Sai số posterior max | cps official=independent |
|---|---:|---:|---:|---|
| TT | 120 | 56 | 1.110223025e-16 | [120] |
| OB | 120 | 20 | 2.220446049e-16 | [120] |

Hai prefix lấy 120 dòng đầu, trước injection. Chỉ điểm 120 là sentinel ngoài 0..119; không có changepoint trong range. NPZ lưu toànR official/independent, detailJSON lưu maxes và modeposterior cuối. Raw code không có nhánh fallback xếp cột; trả điểm này do lỗi index, không vì phát hiện được nguyên nhân. Synthetic đổi gần biên/hazard khác cũng kiểm, không suy từ 12 điểm rằng detector bỏ sót toàn bộ dữ liệu.

## 5. N-Sigma phát hiện: thế số trên từng ca

| Ca/metric tại điểm100 | value | mean quá khứ | sample std | 3std | hit |
|---|---:|---:|---:|---:|---|
| TT/ts-admin-basic-info-service_cpu | 2.891129304 | 1.544270495 | 0.3108902661 | 0.9326707984 | True |
| OB/adservice_cpu | 0.9583057389 | 0.935577962 | 0.05427553654 | 0.1628266096 | False |

TT: list 5450 alarm, 1238 timestamp phân biệt. Điểm đầu list 1708816885; thời điểm sớm nhất 1708816885. Official và independent trùng từng phần tử; đảo cột giữ multiset nhưng đổi list.


OB: list 1099 alarm, 369 timestamp phân biệt. Điểm đầu list 1692569129; thời điểm sớm nhất 1692569079. Official và independent trùng từng phần tử; đảo cột giữ multiset nhưng đổi list.

Synthetic hai cột: list [108,100], đảo cột [100,108]; không truyền list[0] thẳng làm mốc sớm nhất. Chuỗi periodic normal 200 điểm có 0 alarm; raw short ≤100 có 0 alarm. Trong đoạn trước injection thật có thể vẫn có gai/tải/missing; “trước tiêm” là proxy nền, không nhãn chứng minh mọi điểm hoàn toàn bình thường.

## 6. Invariant và các phép kiểm không đạt

Các CSV hai ca khớp từng điểm, sai số normalized lớn nhất 0. Hai codeBR/RE và lặp lại khớp trong cấu hình đã nêu. Đảo cột giữ điểm; hòa có thể đổi vị trí nên không khẳng định rank invariance tuyệt đối. Normal-normal vẫn có rank và điểm lớn; không gán nó là nguyên nhân có nghĩa. Xem kiem-tra.json để kiểm từng invariant, kể cả lỗi/NaN/[] và sentinel; không đánh dấu mọi test là PASS chỉ vì lệnh chạy hết.
