# Sổ ca đã nhìn — bằng chứng trung gian T-020

Đơn vị union là identity có bằng chứng đã lưu. TX0 chỉ metadata/nhãn; TX1 số đo mô tả đã đọc; TX2 đã có kết quả phương pháp theo ca. T005 timing-only có ran_method=true nhưng không tự khẳng định đã thấy rank. Không chọn chính sách hay chia tập.

735 ca RCAEval public được lấy từ HF catalog đã lưu; identity dùng content hash metric và Git oid inject. 60 RE2-TT suy từ census90 trừ allowlist30, không mở/đếm thư mục locked. Cả60 có factual_seen TX0 và không có ran_method.

T019 có 1245 dòng quan hệ nhưng 435 identity unit trong union đã chứng minh. Tổng row/case-source không phải số ca duy nhất. source-reconciliation.csv và source-intersections.csv giải thích từng nguồn và phần giao.

T006 bổ sung125 local RE1OB;40 delay/loss (4 roots×2 faults×5 repeats) cùng SHA256 với fseOB đã được nối. Quan hệ local RE1OB↔HF RE1OB còn OPEN; không đẩy TX2 theo tên. T019 xác nhận toraiSS↔RE2SS90, toraiOB↔RE2OB90 và RE1SS125↔HF nội dung. T016 xác nhận TT bằng toàn bảng metric, không chỉ cùng tên/mốc.

| Dataset | Đơn vị | Tổng | TX0 | TX1 | TX2 | Ô nhãn | Identity OPEN |
|---|---|---:|---:|---:|---:|---:|---:|
| AnoMod-SN_data | experiment capture; root binding OPEN | 13 | 0 | 13 | 0 | 0 | 13 |
| AnoMod-TT_data | experiment capture; root binding OPEN | 13 | 0 | 13 | 0 | 0 | 13 |
| BARO-FSE-OB | incident | 100 | 0 | 0 | 100 | 20 | 0 |
| BARO-bundled-example | example time series; incident identity OPEN | 1 | 0 | 0 | 1 | 0 | 1 |
| DeepTraLog-TT | storage capture | 83 | 0 | 83 | 0 | 0 | 83 |
| Eadro-SN | incident | 36 | 0 | 36 | 0 | 36 | 0 |
| Eadro-TT | incident | 81 | 0 | 81 | 0 | 81 | 0 |
| FSE-2026-propagation-TT | injection event (possibly multiple roots) | 10 | 0 | 10 | 0 | 10 | 0 |
| LEMMA-Cloud_Computing-Original | date capture | 6 | 6 | 0 | 0 | 0 | 6 |
| LEMMA-Cloud_Computing-Preprocessed | date capture | 6 | 5 | 1 | 0 | 0 | 6 |
| LEMMA-Product_Review-Original | date capture | 4 | 4 | 0 | 0 | 0 | 4 |
| LEMMA-Product_Review-Preprocessed | date capture | 4 | 3 | 1 | 0 | 0 | 4 |
| MSL-bundled-GDN | multivariate time series sample; incident census OPEN | 1 | 0 | 0 | 1 | 0 | 1 |
| Nezha-OB | incident | 56 | 0 | 56 | 0 | 33 | 0 |
| Nezha-TT | labelled incident (clock mapping OPEN) | 45 | 0 | 45 | 0 | 23 | 45 |
| OpenRCA-Bank | labelled incident at pod/component level | 136 | 136 | 0 | 0 | 52 | 0 |
| RE1-OB | incident | 125 | 124 | 1 | 0 | 25 | 0 |
| RE1-OB-local-Zenodo | incident | 85 | 0 | 0 | 85 | 17 | 85 |
| RE1-SS | incident | 125 | 0 | 25 | 100 | 25 | 0 |
| RE1-TT | incident | 125 | 125 | 0 | 0 | 25 | 0 |
| RE2-OB | incident | 90 | 0 | 0 | 90 | 30 | 0 |
| RE2-SS | incident | 90 | 0 | 0 | 90 | 30 | 0 |
| RE2-TT | incident | 90 | 60 | 0 | 30 | 30 | 0 |
| RE3-OB | incident | 30 | 30 | 0 | 0 | 10 | 0 |
| RE3-SS | incident | 30 | 0 | 30 | 0 | 9 | 0 |
| RE3-TT | incident | 30 | 29 | 1 | 0 | 8 | 0 |
| Synthetic | fixture | 2 | 0 | 0 | 2 | 0 | 0 |

Census Nezha/Eadro dùng tuple entity+fault+inject timestamp. NezhaTT45 là label records; hai dòng cùng epoch nhưng text giờ tiêm khác giữ riêng, quan hệ OPEN. Bank dùng tuple level+component+timestamp+reason, chưa đọc telemetry; root là component/pod. DeepTraLog83 là storage capture/trace labels;82 có trace-ID census. AnoMod26 là experiment capture, mapping nhãn gốc OPEN. LEMMA có20 date/release captures,2 preprocessed đã đọc và18 chỉ metadata. Không cộng những đơn vị này như sự cố, không giả thành ô service×fault.

dataset-census-membership.csv giữ census đầy đủ mỗi release/copy; dataset-membership-exposure.csv có local RE1OB125=40 identity fseOB+85 source-scoped units. Bảng trên là ownership của canonical union nên localRE1OB85 là phần tăng union, không phải tổng ca dataset. FSE propagation có10 injection folders,2 invalid markers và8 valid theo nguồn; không tự chọn dùng tất cả10.

Kiểm số: 1762 leaf có phép tính đối chiếu, chọn SHA256(seed|task|path|key) tối thiểu5 nghĩa/task tại numeric-check-selected.csv. Giữ cả pool trước chọn. Có 0 số lệch/chưa tái lập đúng; xem run-assertions.json. Mọi số kết luận-trọng yếu census, sources, intersections đều tính lại count/group/sum.

Root cần kiểm độc lập số trọng yếu trước dùng file cuối. Chưa quyết định, chưa khuyến nghị, chưa chia dev/test; chưa xem số đo mới TX0/TX1; không chạy script task cũ hay RCA/detector.
