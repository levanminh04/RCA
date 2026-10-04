# DeepTraLog Train Ticket — thẻ đã kiểm F/normal/all-log/graph được duyệt

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: DeepTraLog ICSE 2022, Chenxi Zhang và cộng sự, FudanSELab; Train Ticket v0.2.0, nhánh code có lỗi; SkyWalking, Elasticsearch. [Repository](https://github.com/FudanSELab/DeepTraLog), [trang tác giả](https://fudanselab.github.io/DeepTraLog/), [paper đã lưu](runs/run-001/sources/paper.pdf). Revision, URL, hash và snapshot ở [manifest nguồn](runs/run-001/manifest.json). Repository/trang tác giả đã lưu chưa cho điều khoản license dữ liệu/code rõ; công khai không chứng minh đầy đủ quyền sử dụng. Không gọi thiếu license là dữ liệu bất hợp pháp.

Q-47 cho kiểm số đo DeepTraLog trên EC2 mới. Đã tải 32 file chính thức: 14 ZIP F, 10 ZIP normal, tám phần GraphData, 515.614.981 byte; [download-002](runs/download-002/manifest.json) giữ byte/checksum/revision. Tám phần graph ghép thành ZIP, CRC mọi member được kiểm. Đã đọc toàn raw/normal/graph và ba bảng CSV trong graph. Sau khi thấy thiếu lineage normal/coverage log, thực hiện bước 4 có điều kiện trong SPEC/kế hoạch: tải thêm năm phần all-log 213.216.632 byte, tổng Deep 37 file/728.831.613 byte. Root xác nhận đây là tiếp phạm vi đã trình, không ứng viên/phương pháp mới. [Download thêm](runs/download-003/manifest.json), [all-log CRC/schema/count](runs/inspect-007/summary.json), [coverage từng nhãn](runs/inspect-008/per-label-coverage.json). All-log là bản gộp cùng lineage, không modality/dataset độc lập. Toàn F/normal/all-log/graph của inventory dữ liệu đã đọc; không full-unpack log ra đĩa.

[Raw/CRC](runs/inspect-002/summary.json), [lineage/graph sửa shape](runs/inspect-005/summary.json), [CSV mapping](runs/inspect-006/tables.json). `inspect-002` đọc nhầm edge_index E×2 thành 2×E: số cạnh/bad-index của graph run này bị thay bằng inspect-005; raw/CRC giữ sau kiểm. Hai lượt bổ sung lỗi header/Counter được giữ trong inspect-003/004, không ghi đè. Chạy `inspect_deep.py`, `inspect_lineage.py` và `inspect_graph_tables.py` trong scripts với `--data /home/ubuntu/rca-t003/data/deeptralog --out <run-mới>`; không training/RCA.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1. Công khai/giấy phép | File tải/CRC được, điều khoản permission OPEN. |
| 2. Root/thời điểm | Nhãn trace bất thường có thật; chưa có nhãn root service hoặc injection/onset riêng. |
| 3. Trace cha–con | 12.303.544 dòng span raw, scoped parent ở mục 4. |
| 4. Metric/log | Log thực có ID ghép; resource metric riêng không có trong tree/raw/graph đã kiểm. Latency span không thay resource metric. |
| 5. Root/vị trí | Raw có 35 service, graph có service ID map; không nhãn root nên không suy vị trí root từ bậc event. |
| 6. Loại lỗi | Paper nhóm inter-service/data consistency/multi-threading/monolithic; 70 nhãn instance code trong graph, chưa mapping root×fault. |
| 7. Ngoài root | Không thể phân loại ngoài-root có căn cứ khi nhãn root thiếu; không tạo nhãn từ log ERROR. |
| 8. Normal | 10 ZIP normal có dữ liệu thực; khoảng/thể tích và nguy cơ nhiễm ở mục 5. |
| 9. Độc lập | Nhóm tác giả/faulty branch/stack có nguồn; cần so reuse với RCAEval/Eadro/Nezha tại G1. |

## 3. Nhãn, số ca và khả năng phân xử

Paper công bố 132.485 trace, 23.334 abnormal trace, 7.705.050 log, 73 fault instances/14 fault cases. Graph thực đếm đúng 132.485 trace-ID duy nhất, 109.151 normal và 23.334 abnormal, không ID trùng hoặc nhãn thiếu/xung đột; 70 `error_trace_type` khác normal. Raw có 83 thư mục storage được inspector đếm, 83 có span; không coi folder, fault branch và trace là cùng đơn vị incident. Root×fault×lần lặp không có nhãn service-ground-truth nên không tạo census giả.

| Nhãn graph instance | Abnormal trace trong graph | Trace-ID raw cùng thư mục |
|---|---|---|
| F01-01 | 341 | 341 |
| F01-02 | 400 | 400 |
| F01-03 | 352 | 352 |
| F01-04 | 480 | 480 |
| F01-05 | 480 | 480 |
| F02-01 | 400 | 400 |
| F02-02 | 400 | 400 |
| F02-03 | 399 | 399 |
| F02-04 | 317 | 317 |
| F02-05 | 317 | 317 |
| F02-06 | 318 | 318 |
| F03-01 | 319 | 319 |
| F03-02 | 265 | 265 |
| F03-03 | 330 | 330 |
| F03-04 | 329 | 329 |
| F03-05 | 341 | 341 |
| F03-06 | 360 | 360 |
| F03-07 | 310 | 310 |
| F03-08 | 310 | 310 |
| F04-01 | 330 | 330 |
| F04-02 | 326 | 326 |
| F04-03 | 320 | 320 |
| F04-04 | 329 | 329 |
| F04-05 | 267 | 267 |
| F04-06 | 314 | 314 |
| F04-07 | 330 | 330 |
| F04-08 | 330 | 330 |
| F05-01 | 333 | 333 |
| F05-02 | 383 | 383 |
| F05-03 | 364 | 364 |
| F05-04 | 270 | 270 |
| F05-05 | 315 | 315 |
| F07-01 | 685 | 685 |
| F07-02 | 450 | 450 |
| F07-03 | 340 | 340 |
| F07-04 | 420 | 420 |
| F07-05 | 414 | 414 |
| F08-01 | 151 | 151 |
| F08-02 | 250 | 250 |
| F08-03 | 248 | 248 |
| F08-04 | 199 | 199 |
| F08-05 | 250 | 750 |
| F11-01 | 347 | 347 |
| F11-02 | 353 | 353 |
| F11-03 | 347 | 347 |
| F11-04 | 350 | 350 |
| F11-05 | 350 | 350 |
| F12-01 | 298 | 298 |
| F12-02 | 283 | 283 |
| F12-03 | 294 | 294 |
| F12-05 | 299 | 299 |
| F13-01 | 378 | 378 |
| F13-02 | 299 | 299 |
| F13-03 | 402 | 402 |
| F13-04 | 350 | 350 |
| F13-05 | 350 | 350 |
| F14-01 | 286 | 286 |
| F14-02 | 291 | 291 |
| F14-03 | 293 | 293 |
| F23-01 | 300 | 300 |
| F23-02 | 300 | 300 |
| F23-03 | 300 | 300 |
| F23-04 | 300 | 300 |
| F23-05 | 300 | 300 |
| F24-01 | 330 | 330 |
| F24-02 | 326 | 326 |
| F24-03 | 322 | 322 |
| F25-01 | 300 | 300 |
| F25-02 | 300 | 300 |
| F25-03 | 300 | 300 |

Raw `F12-04` và `back0729` không có abnormal graph tag cùng tên; nhãn xử lý không được suy từ tên. Tất cả 23.334 abnormal graph ID có mặt raw của đúng named case. 104.369/132.485 graph ID có trong toàn raw tải; 28.116 vắng raw. Không gọi lineage normal đầy đủ: release raw có thể subset, graph có thêm lượt, hoặc khác quá trình xuất; nguồn chưa giải thích. [Từng count](runs/inspect-005/summary.json). Trong 28.116 normal graph ID vắng span raw, 28116 ID có all-log và 0 vắng cả hai. All-log giúp chứng minh có log cho phần lớn normal graph nhưng không khôi phục parent/span vắng; provenance normal vẫn chỉ nhãn trace. [Partition từng label](runs/inspect-008/per-label-coverage.json).

Raw graph service dựng từ parent service→child service, bỏ self-edge, tại từng storage case; [toàn bảng cạnh từng ca](runs/inspect-002/raw-cases.json). Service ID map trong id_service.csv có 35 entity khớp tập raw. Graph xử lý là TEG event graph (đồ thị sự kiện), không coi 27.288.193 event node hay bậc event là vị trí root service. Nhãn root service không được thấy trong các file được duyệt nên không có bảng bậc root thật.

## 4. Schema thật và chất lượng nguồn tín hiệu

FACT raw: CSV StartTime/EndTime (epoch ms), URL, SpanType, Service, SpanId, TraceId, Peer, ParentSpan, Component; 87 CSV header có IsError, ba header thiếu IsError. Span type/status riêng từng case ở raw-cases. Tổng IsError: 12119834 False, 44782 True, 138928 thiếu trường; thiếu trường không tự gán False. IsError từng span không bằng nhãn trace/ranking root.

Tổng span 12.303.544; sentinel/root theo file: 106310; parent cần resolve 12197234. Khóa `(TraceId,SpanId)` trong storage case: 12160234 tìm một dòng cha, 20 thiếu, 36980 nhiều dòng. Đây là strict-row resolution; span ID trùng giữ riêng trong từng ca, không coi row duplicate là parent mất. Tỷ lệ cộng tử/mẫu, không trung bình tỷ lệ từng ca. File/time bị cắt, instrumentation hoặc dòng export trùng cũng giải thích thiếu/ambiguous.

Log 5835230 dòng trong F/normal; 5835230 dòng có SW_CTX. Không cột trace_id riêng; context chứa trace/segment/span. 5374436 dòng ghép trace, 5372329 ghép scoped span bằng `segment+'.'+span`; quality riêng từng ca/file và reverse order được giữ. Nhiều file log có thứ tự giảm thời gian; không dùng row order thay clock. All-log stream đếm đúng 7.705.050 dòng paper, cùng SW_CTX; 141621 trace-ID trong log. 130920/132.485 graph ID có log: 108075/109.151 normal, 22845/23.334 abnormal. 1565 graph ID không có log (1076 normal, 489 abnormal). ID có trong log chưa chứng minh span raw/clock sạch hoặc root. All-log có 4006550 cặp dòng đảo thời gian; không dùng thứ tự dòng làm timeline.

Graph: cả tám JSONS đúng sáu trường trace_id/trace_bool/error_trace_type/node_info/edge_index/edge_attr. edge_index **E×2**, 29855076 cạnh, 27288193 event node; 0 endpoint sai/edge-attr length mismatch. trace_bool True→normal (code y=0), False→abnormal; type/label nhất quán với error_trace_type. Ba CSV graph: id_service 35 dòng, id_url+temp 1.513, id_url+type 1.878; first-ID duy nhất, không trường rỗng hoặc width sai. Loader còn đòi embedding_id_url+type.csv, file này không có trong ZIP graph kiểm; chưa chạy loader/baseline, không gọi distribution này chạy được nguyên trạng.

## 5. Bình thường và mốc thời gian

10 ZIP normal chứa 9.999.974 dòng span, 81.037 trace-ID duy nhất. Khoảng min/max là phạm vi xuất file, không duration normal liên tục hay lượng label injection. Có normal graph ID ghép raw normal 81035; abnormal graph không ghép raw normal (0). Warm-up/khôi phục/đại diện tải vẫn không được tên normal chứng minh.

| Normal storage | Dòng span | Min epoch ms | Max epoch ms |
|---|---|---|---|
| F02-04-normal | 677580 | 1629255748323 | 1629256353532 |
| F02normal01 | 117578 | 1629188305950 | 1629189474235 |
| normal0726data | 660384 | 1627276477485 | 1627281702590 |
| normal0728data | 134000 | 1627473201181 | 1627474332935 |
| normal0730data | 1652150 | 1627631428811 | 1627635167400 |
| normal0809_01 | 246322 | 1628474914002 | 1628475232908 |
| normal0809_02 | 2526923 | 1628481645915 | 1628497998031 |
| normal0809_03 | 3291517 | 1628511959942 | 1628524765685 |
| normal0822_02 | 681520 | 1629617400523 | 1629623896851 |
| normal_put_consign | 12000 | 1628954159630 | 1628954449088 |

Raw có clock span ms/log text; timezone log không được xác nhận từ file. Graph không có timestamp injection/onset/window, chỉ trace ID. Không suy injection từ phần số trong SkyWalking ID hoặc chuyển graph label thành nhãn thời gian. Không tự nối các phiên normal/fault thành một chuỗi.

## 6. Triệu chứng ngoài root — tiêu chí 7

OPEN do **release được kiểm không có ground truth root service và resource metric riêng**, không do còn chờ quyền đọc. Span latency/log level đã kiểm trong toàn phạm vi; không thể gọi service “ngoài root” có căn cứ. Trace_bool/error_trace_type là nhãn trace, không root; log ERROR có thể symptom chứ không nguyên nhân. Không tạo root/region từ regex hoặc coi nhiều service trong trace là propagation. Cần nguồn nhãn root nếu muốn thực hiện q theo service ngoài root; chưa có bằng chứng để lấp nhãn này trong task.

## 7. Task chấm được

| Task | Nhãn thực và phạm vi |
|---|---|
| Trace anomaly | Có toàn 132.485 label, nhất quán; P/R/F1 theo đơn vị trace có căn cứ, chưa chạy phương pháp. |
| Ranking root | Không root service per instance; error_trace_type không thay root, MRR/Hit@k OPEN. |
| Phát hiện thời gian | Không onset/injection interval thật trong graph/nhãn đã kiểm; không chấm window bằng suy đoán ID. |
| Vùng ảnh hưởng | Không label tập service bị ảnh hưởng, không chấm từ event graph hoặc IsError. |

Loader normal-only training/split theo paper/code là giao thức nguồn, không quyết định G1. Ngân sách label và phương pháp chuyển hệ chưa chọn.

## 8. Rò nhãn và độc lập

Tên F/normal, tên file SUCCESS/ERROR, trace_bool/error_trace_type có thể lộ class; chỉ census/chấm hoặc ngân sách học được duyệt. Adapter không dùng path/name/root-derived SLI; chưa có adapter nên không claim đã an toàn. Graph giữ fault type trong Data; cần loại khỏi input phương pháp. Không chia raw và graph của cùng trace sang hai phía dev/test. Lineage mapping abnormal đã xác minh; normal raw→processed chỉ một phần, không ép được đầy đủ từ số tổng.

Nhóm Fudan/faulty branches/SkyWalking khác nguồn Eadro Chaosblade/Jaeger; Train Ticket là hệ dùng chung. Khác stack/tác giả không chứng minh độc lập mọi trục hoặc không reuse. Chưa quyết dataset/split/holdout.

## 9. Dung lượng và chi phí

37 file tải 728.831.613 byte theo hai manifest download-002/003; download-002 giữ thời gian từng file/checksum. Raw/CRC run-002 123,845 giây; audit lineage/graph inspect-005 147.63 giây; bảng CSV inspect-006 chạy streaming. EC2 mới, không instance T-007, timeout mỗi lệnh <1 giờ. Không cài training environment; không RCA. [Byte member sau giải nén chính xác](runs/inspect-008/logical-member-sizes.json): raw F 1889223799 byte, normal 4160637720, graph 1468001498, all-log 3085469085; tổng 10603332102 byte, gồm 1.320 byte ancillary ẩn. Tất cả member đã CRC kiểm; đây là dung lượng logical uncompressed, không phải disk đã ghi khi stream; all-log member 3.085.469.085 byte được stream (run-007 65.96 giây) và CRC xác nhận, không ghi member ra đĩa. Coverage run-008 76.381 giây. Chi phí RAM đỉnh/adapter/phương pháp chưa đo, không ngoại suy từ parsing.

## 10. OPEN và kết luận phạm vi

Đã kiểm toàn raw/normal/graph trong danh sách Q-47 được tải, tự kiểm graph shape/label/lineage và lưu lỗi. License chưa chứng minh đủ permission; tác giả/nguồn điều khoản cần làm rõ khi dùng ngoài inspection. Nhãn root/injection/region không thấy trong corpus được kiểm; muốn chấm các task đó cần nguồn nhãn thật, không suy từ IsError. 28.116 graph normal ID vắng raw cần giải thích lineage nếu dùng raw vs graph. All-log đã kiểm toàn phần có điều kiện; loader embedding còn thiếu. Những điều này không phủ định trace-label census đã kiểm và không là lý do tự chọn/bỏ dataset thay Minh.
