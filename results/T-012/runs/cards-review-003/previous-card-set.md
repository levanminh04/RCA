# Thẻ dataset 2025–2026 — khảo sát nguồn có giới hạn và bổ sung kiểm file sau REVIEW

Giữ14biếnthể trongscope. Đãkiểmfull3archiveAnoMod/TRCA/FSE628.411.611byte tải đạt checksum; Bank chỉ metadata/schema/labelrange, không sốđo. Các biếnthể còn lại vẫn nguồn-only đúng giới hạn đãnêu. Không gọi PASS hash là quality hoặc chọn G1. [Các nguồn trước](runs/run-002/source-manifest.json), [nguồn bổ sung](runs/review-sources-001/manifest.json), [lineage](independence-matrix.md), [phạm vi kiểm](inspection-plan.md).

# FSE fault-propagation benchmark — artifact rút gọn

## 1. Danh tính, nguồn và phạm vi đã kiểm

Fang và cộng sự; Train Ticket, OTel/Prometheus/Hubble và ChaosMesh theo bài. Đã tải đúng record19522409, kiểm mọi member và đọc mọi input của artifact rút gọn; không chạy vendor/RCA hoặc dùng saved scores. [Metadata/checksum](runs/review-sources-001/sources/zenodo-19522409.json), [download](runs/download-review-001/manifest.json). Accepted paper main.pdf trong archive đã đối chiếu: vẫn công bố 1.430 ca/9.152 injection/25 loại; [text và manifest](runs/fse-paper-review-001/manifest.json), không lấy số toàn bài thay census artifact. Record ghi Apache2, nhưng [LICENSE nội bộ](runs/fse-file-inspect-003/LICENSE.txt) giới hạn root packaging/support và giữ upstream terms cho vendor/paper; phạm vi permission của raw input còn OPEN, không tự đồng nhất cả gói.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1 | Archive công khai tải/hash/CRC được; license scope ở mục1. |
| 2 | Nhãn root set/start/end tiêm thực đọc. |
| 3 | Parent scoped(trace_id,span_id), unique/missing/ambiguous và graph từng phase/ca đã đo. |
| 4 | Parquet metric/log/trace có thật; log-ID và match trace/span tách riêng. |
| 5 | 11 root service khác nhau ở tám ca không có invalid marker; graph/degree riêng từng ca. |
| 6 | Tám mã fault type ở tám ca không invalid, không đại diện 25 loại của bài. |
| 7 | Đã probe metric raw và duration ở tám ca, ba q, reference/control; không là nhãn propagation. |
| 8 | Normal trước tiêm khoảng240s theo env; sạch/đại diện load chưa độc lập chứng minh. |
| 9 | Cùng upstream TT với OpenRCA2; artifact không là corpus độc lập thứ hai. |

## 3. Nhãn, số ca và khả năng phân xử

Có 10 thư mục ca, 2 có .invalid rỗng (không kèm lý do); không lấy chúng vào probe. Tám ca còn lại có 11 service gốc, tám mã fault, tám ô root-set×fault, mỗi ô một lần. Không có lặp đủ để ngoại suy. Marker vắng không thay tự chứng minh SLI valid. [census](runs/fse-file-inspect-003/census.json), [từng ca/graph/parent/clock/linkage](runs/fse-file-inspect-003/cases.json), [schema](runs/fse-file-inspect-003/schemas.json).

| Ca | Tập service gốc | Fault type | Invalid marker |
|---|---|---|---|
| ts8-ts-route-plan-service-request-delay-5dmjfm | ts-route-plan-service, ts-travel2-service | 7 | False |
| ts3-ts-contacts-service-container-kill-262mnp | ts-contacts-service | 2 | False |
| ts2-ts-order-service-stress-8vtw2p | ts-order-service | 28 | False |
| ts4-ts-route-plan-service-bandwidth-z6g6ng | ts-route-plan-service, ts-travel-plan-service | 21 | False |
| ts5-ts-order-service-corrupt-bd4p5g | ts-order-service, ts-ui-dashboard | 20 | True |
| ts4-ts-auth-service-pod-failure-97s6xl | ts-auth-service | 1 | False |
| ts2-ts-train-service-exception-plrfk2 | ts-train-service | 25 | False |
| ts5-ts-route-plan-service-partition-khgj4c | ts-route-plan-service, ts-travel-plan-service | 22 | True |
| ts3-ts-food-service-response-replace-body-skvngv | ts-food-service, ts-station-food-service | 9 | False |
| ts0-ts-security-service-request-replace-method-j6gpxx | ts-security-service, ts-order-other-service | 12 | False |

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Toàn 113 Parquet đã đọc, schema/count từng file ở [census](runs/fse-file-inspect-003/census.json), [từng ca/graph/parent/clock/linkage](runs/fse-file-inspect-003/cases.json), [schema](runs/fse-file-inspect-003/schemas.json); input chính normal/abnormal trace, metric, log, còn sum/histogram/conclusion tách riêng. conclusion/causal_graph là kết quả suy từ dữ liệu, không nhãn vùng độc lập. Trace time timestamp ns UTC được giữ exact integer ns khi đọc; duration giữ đơn vị raw (chưa chứng minh physical unit). Metric series giữ đủ tag/entity, NaN/constant/duplicate/cadence/gap theo từng series; step ở đơn vị timestamp gốc ns. Graph là call graph từ parent unique, không đủ message/data edges.

## 5. Dữ liệu bình thường và mốc thời gian

env.json có NORMAL_START/END, ABNORMAL_START/END epoch-second; injection start/end ISO UTC. Không sửa payload hoặc biến mốc tiêm thành onset. Trace normal khoảng bốn phút mỗi ca; normal-end có thể chạm injection-start. Phase cắt trước/đang tiêm không đủ để tự tạo healthy gold cho mọi điểm hoặc nối ca thành continuous stream.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

[Bands từng ca/entity/kênh/q](runs/fse-file-inspect-003/descriptive-bands.json): 86352 dòng gồm cả thiếu reference. Normal first half theo thời gian reference, second half control; median và quantile độ lệch tuyệt đối q=.95/.99/.995. Root-set chỉ gắn sau đo. Giữ zero-band, n nhỏ, missing, control exceed/fault exceed; không OR. Metric raw có counter/gauge chưa khóa unit/type nên exceedance chỉ mô tả, không chẩn đoán. Load/mix, boundary, tag đổi và clock có thể giải thích ngoài-root. Không suy tám ca thành toàn benchmark.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn thực và giới hạn |
|---|---|
| Ranking | Có ground_truth.service dạng tập root, container/pod/metric/span theo từng ca; phải chấm tập/cấp nhãn đúng, không ép một root. |
| Phát hiện theo thời gian | Có start/end tiêm UTC, chưa onset/recovery. Normal/abnormal đã cắt theo tiêm nên cần protocol điều kiện; chưa là phát hiện liên tục mù thời điểm. |
| Vùng ảnh hưởng | Không có nhãn vùng độc lập được xác minh; không chấm từ exceedance/causal_graph. |
| Trace anomaly | Không thấy nhãn anomalous từng trace; tên abnormal là phase, không nhãn mọi trace. |

## 8. Rò nhãn và thông tin phục vụ G1

Tên ca, injection.json, ground_truth, phase folder và env cut bounds lộ thông tin nhãn. Chỉ dùng census/chấm, không detector tự phát hiện. Normal/abnormal cùng ca không tự là hai nguồn độc lập; artifact và OpenRCA2 TT cùng upstream. Bậc graph không tự ground truth vùng.

## 9. Kích thước và chi phí

Tải 91418171 byte; logical member 339482164 byte, 3519 entries. Streaming không ghi đầy đủ cây ra đĩa. [census](runs/fse-file-inspect-003/census.json), [từng ca/graph/parent/clock/linkage](runs/fse-file-inspect-003/cases.json), [schema](runs/fse-file-inspect-003/schemas.json); [archive CRC/size/time](runs/fse-file-inspect-003/archive.json), [thời gian semantic](runs/fse-file-inspect-003/validation.json). Python3.12 + pyarrow23.0.1 isolated data/ngoai-rcaeval/T-012/python-packages; script inspect_review_archives.py --kind fse --archive <archive> --run <mới>. Lượt thiếu tzdata/conversion ns được giữ; lần3 đọc exact int ns thành công.

## 10. Những điều còn mở

OPEN: license raw scope cần chủ nguồn; lý do hai .invalid thiếu cần nguồn; duration physical unit, onset/recovery, đủ graph message/data và quality toàn corpus chưa có. Chỉ đã kiểm trọn artifact reduced; không tải hay ngoại suy toàn dataset trong bài. Không còn gọi ba archive nhỏ là chờ quyền.

# AnoMod — SocialNetwork

## 1. Danh tính, nguồn và phạm vi đã kiểm

AnoMod MSR2026, nhóm Helsinki. Data CC-BY4 theo record18342898, repo MIT; [metadata](runs/review-sources-001/sources/zenodo-18342898.json), [download](runs/download-review-001/manifest.json), [collector/configs ghim](runs/anomod-collector-review-001/manifest.json). Đã đọc toàn ZIP/mọi member và telemetry của cả hai hệ; HTML/coverage chỉ hash/CRC, không chạy. TT/SN dùng collector khác nhau theo README, không áp một stack cho cả gói.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1 | Tải/hash/CRC PASS; data/code license riêng. |
| 2 | Tên experiment và cấu hình đích được đọc; chưa có gold runtime incident/onset/end riêng. |
| 3 | CSV Jaeger SN/JSON SkyWalking TT; parent unique/missing/ambiguous có actual census. |
| 4 | Metric CSV, container logs, trace, API response, coverage có thật; 0 SW_CTX trong log đã đọc, không khẳng định mọi kiểu ID đều vắng. |
| 5 | 12 faulty capture +1 baseline; target graph degree có điều kiện theo source, không root gold. |
| 6 | SN exporter dùng datetime.fromtimestamp: CSV time là naive local; JSON Jaeger epoch microseconds giữ nguồn gốc. Ba Code_Stop thực hiện docker stop, không seeded defect trong source code. Ba performance target host/disk/docker0; Redis target là database, không ép vào service. JSON và CSV cùng trace/span-ID set, đã kiểm mọi 13 export. |
| 7 | Đã khảo sát duration theo service/operation, baseline reference/control/3q; outside declared target có điều kiện, không outside-root gold. |
| 8 | Một baseline thật mỗi hệ; normal load/reset/warmup và recovery chưa độc lập xác minh. |
| 9 | Campaign/nhóm mới theo nguồn; stack/injector overlap Eadro/Deep và LO2, không đủ ba trục chỉ từ tên. |

## 3. Nhãn, số ca và khả năng phân xử

Thực kiểm: 13 capture/hệ =12fault-name+1normal-name. 2635 trace occurrences, 25577 span rows; đây không phải incident độc lập hay nhãn trace anomaly. 145555 metric rows và 3959028 log lines. Mỗi fault-family một capture, chưa proof incident/repetition từ runtime label. .DS_Store ở SN không tính ca. [file/schema/quality](runs/anomod-file-inspect-003/files.json), [parent/graph/từng capture](runs/anomod-file-inspect-003/cases.json), [target-source/capture census](runs/anomod-followup-002/captures.json). Target configs và code đọc ở collector manifest; đếm đích nguồn khác đếm root gold. Không tạo một nhãn mới chỉ để kín bảng.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

SN exporter dùng datetime.fromtimestamp: CSV time là naive local; JSON Jaeger epoch microseconds giữ nguồn gốc. Ba Code_Stop thực hiện docker stop, không seeded defect trong source code. Ba performance target host/disk/docker0; Redis target là database, không ép vào service. JSON và CSV cùng trace/span-ID set, đã kiểm mọi 13 export.

[file/schema/quality](runs/anomod-file-inspect-003/files.json), [parent/graph/từng capture](runs/anomod-file-inspect-003/cases.json), [target-source/capture census](runs/anomod-followup-002/captures.json). Metric cadence/gap/constant/duplicate/nonfinite theo series và tag, không trộn instance. API response chỉ đếm/schema, không chép Authorization/password/body. Logs đã đọc toàn line và đếm context marker; không có SW_CTX nên không claim ID join theo SkyWalking context. Cần khai báo structured-ID format nếu muốn log→trace match khác; không chạy regex ERROR để tạo root.

## 5. Dữ liệu bình thường và mốc thời gian

Baseline `Normal_Baseline_20251103_220228` có 205 trace; first-half chronological reference/second-half control. Tên normal và reset code không chứng minh sạch/đủ nhiều workload. Nhãn time trong runname không chứng minh tiêm hay recovery. Không nối13capture thành continuous benchmark.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

[Duration bands](runs/anomod-followup-002/descriptive-bands.json), q=.95/.99/.995, theo từng service×operation; unit SNµs/TTms theo schema, entity không có baseline giữ missing. Median/band/control/tử-mẫu giữ riêng; đích cấu hình gắn sau đo, ngoài đích chỉ có điều kiện với target-level service, host/DB để null. Chưa thể gọi các số đó ngoài-root hoặc vùng ảnh hưởng thật vì thiếu runtime gold. Thay tải/operation mix, collector/errorcode và cut-window đều có thể giải thích vượt band. Không OR/causality.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn thực và giới hạn |
|---|---|
| Ranking | CANDIDATE theo đích cấu hình tiêm, chưa có nhãn runtime root/time từng incident đóng đủ. Host/database không tự service root. |
| Phát hiện theo thời gian | Không có injection start/end/onset riêng được ghép với từng capture; timestamp tên run không phải injection. Chưa chấm onset/F1 thời gian thật. |
| Vùng ảnh hưởng | Không có nhãn vùng độc lập được xác minh; không chấm từ exceedance/causal_graph. |
| Trace anomaly | is_error/status là observed instrumentation, chưa gold anomalous từng trace; không gán class toàn capture. |

## 8. Rò nhãn và thông tin phục vụ G1

EXP_NAME/path chứa fault và đích; tránh làm input detector. JSON↔CSV/coverage/API cùng run không corpus độc lập. [Overlap actual](runs/anomod-followup-002/overlap.json): không shared trace-ID giữa khác capture trong release, điều này chưa chứng minh collector/injector độc lập với các dataset khác. Source-target không gold; không dùng lỗi để chọn operation/metric.

## 9. Kích thước và chi phí

ZIP chung hai hệ 201917396 byte, 3076340723 logical byte/44291 entries; không gán cả byte cho mỗi hệ hoặc cộng đôi. [Member/hash/CRC](runs/anomod-file-inspect-003/members.json), [thời gian](runs/anomod-file-inspect-003/validation.json). Không giải nén trọn; Python stdlib, script inspect_review_archives.py --kind anomod và inspect_anomod_followup.py --run <mới>. Giữ lượt parse lỗi; không delete sau khảo sát.

## 10. Những điều còn mở

OPEN: xác nhận script/config revision đúng từng run và injection execution record, entity root-level cho host/DB, onset/end/recovery, log-ID schema và clock timezone SN. Thiếu các dữ kiện này giới hạn census gold/ranking/ngoài-root; không gọi không kiểm do chi phí là không thể kiểm. Đã kiểm mọi capture thực; không suy quality từ taxonomy hoặc số paper.

# AnoMod — TrainTicket

## 1. Danh tính, nguồn và phạm vi đã kiểm

AnoMod MSR2026, nhóm Helsinki. Data CC-BY4 theo record18342898, repo MIT; [metadata](runs/review-sources-001/sources/zenodo-18342898.json), [download](runs/download-review-001/manifest.json), [collector/configs ghim](runs/anomod-collector-review-001/manifest.json). Đã đọc toàn ZIP/mọi member và telemetry của cả hai hệ; HTML/coverage chỉ hash/CRC, không chạy. TT/SN dùng collector khác nhau theo README, không áp một stack cho cả gói.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1 | Tải/hash/CRC PASS; data/code license riêng. |
| 2 | Tên experiment và cấu hình đích được đọc; chưa có gold runtime incident/onset/end riêng. |
| 3 | CSV Jaeger SN/JSON SkyWalking TT; parent unique/missing/ambiguous có actual census. |
| 4 | Metric CSV, container logs, trace, API response, coverage có thật; 0 SW_CTX trong log đã đọc, không khẳng định mọi kiểu ID đều vắng. |
| 5 | 12 faulty capture +1 baseline; target graph degree có điều kiện theo source, không root gold. |
| 6 | TT SkyWalking JSON trace.summary và spans có node_id/parent_node_id gồm segment và span index, không ghép integer span_id xuyên segment. Tất cả13 metadata ghi lookback24h. Kiểm actual: không trace-ID trùng giữa các capture và không span bắt đầu trước timestamp tên run; vì vậy chưa có bằng chứng trộn lỗi từ overlap, nhưng timestamp tên vẫn không là injection/onset. Ba code scenarios là JVM return/throw tại security/order/travel theo script; lỗi database có cấu hình network-delay, không suy nhãn DB semantics từ tên. |
| 7 | Đã khảo sát duration theo service/operation, baseline reference/control/3q; outside declared target có điều kiện, không outside-root gold. |
| 8 | Một baseline thật mỗi hệ; normal load/reset/warmup và recovery chưa độc lập xác minh. |
| 9 | Campaign/nhóm mới theo nguồn; stack/injector overlap Eadro/Deep và LO2, không đủ ba trục chỉ từ tên. |

## 3. Nhãn, số ca và khả năng phân xử

Thực kiểm: 13 capture/hệ =12fault-name+1normal-name. 63975 trace occurrences, 115025 span rows; đây không phải incident độc lập hay nhãn trace anomaly. 4019540 metric rows và 1694538 log lines. Mỗi fault-family một capture, chưa proof incident/repetition từ runtime label. .DS_Store ở SN không tính ca. [file/schema/quality](runs/anomod-file-inspect-003/files.json), [parent/graph/từng capture](runs/anomod-file-inspect-003/cases.json), [target-source/capture census](runs/anomod-followup-002/captures.json). Target configs và code đọc ở collector manifest; đếm đích nguồn khác đếm root gold. Không tạo một nhãn mới chỉ để kín bảng.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

TT SkyWalking JSON trace.summary và spans có node_id/parent_node_id gồm segment và span index, không ghép integer span_id xuyên segment. Tất cả13 metadata ghi lookback24h. Kiểm actual: không trace-ID trùng giữa các capture và không span bắt đầu trước timestamp tên run; vì vậy chưa có bằng chứng trộn lỗi từ overlap, nhưng timestamp tên vẫn không là injection/onset. Ba code scenarios là JVM return/throw tại security/order/travel theo script; lỗi database có cấu hình network-delay, không suy nhãn DB semantics từ tên.

[file/schema/quality](runs/anomod-file-inspect-003/files.json), [parent/graph/từng capture](runs/anomod-file-inspect-003/cases.json), [target-source/capture census](runs/anomod-followup-002/captures.json). Metric cadence/gap/constant/duplicate/nonfinite theo series và tag, không trộn instance. API response chỉ đếm/schema, không chép Authorization/password/body. Logs đã đọc toàn line và đếm context marker; không có SW_CTX nên không claim ID join theo SkyWalking context. Cần khai báo structured-ID format nếu muốn log→trace match khác; không chạy regex ERROR để tạo root.

## 5. Dữ liệu bình thường và mốc thời gian

Baseline `Normal_case_em_20251103T134716Z` có 4688 trace; first-half chronological reference/second-half control. Tên normal và reset code không chứng minh sạch/đủ nhiều workload. Nhãn time trong runname không chứng minh tiêm hay recovery. Không nối13capture thành continuous benchmark.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

[Duration bands](runs/anomod-followup-002/descriptive-bands.json), q=.95/.99/.995, theo từng service×operation; unit SNµs/TTms theo schema, entity không có baseline giữ missing. Median/band/control/tử-mẫu giữ riêng; đích cấu hình gắn sau đo, ngoài đích chỉ có điều kiện với target-level service, host/DB để null. Chưa thể gọi các số đó ngoài-root hoặc vùng ảnh hưởng thật vì thiếu runtime gold. Thay tải/operation mix, collector/errorcode và cut-window đều có thể giải thích vượt band. Không OR/causality.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn thực và giới hạn |
|---|---|
| Ranking | CANDIDATE theo đích cấu hình tiêm, chưa có nhãn runtime root/time từng incident đóng đủ. Host/database không tự service root. |
| Phát hiện theo thời gian | Không có injection start/end/onset riêng được ghép với từng capture; timestamp tên run không phải injection. Chưa chấm onset/F1 thời gian thật. |
| Vùng ảnh hưởng | Không có nhãn vùng độc lập được xác minh; không chấm từ exceedance/causal_graph. |
| Trace anomaly | is_error/status là observed instrumentation, chưa gold anomalous từng trace; không gán class toàn capture. |

## 8. Rò nhãn và thông tin phục vụ G1

EXP_NAME/path chứa fault và đích; tránh làm input detector. JSON↔CSV/coverage/API cùng run không corpus độc lập. [Overlap actual](runs/anomod-followup-002/overlap.json): không shared trace-ID giữa khác capture trong release, điều này chưa chứng minh collector/injector độc lập với các dataset khác. Source-target không gold; không dùng lỗi để chọn operation/metric.

## 9. Kích thước và chi phí

ZIP chung hai hệ 201917396 byte, 3076340723 logical byte/44291 entries; không gán cả byte cho mỗi hệ hoặc cộng đôi. [Member/hash/CRC](runs/anomod-file-inspect-003/members.json), [thời gian](runs/anomod-file-inspect-003/validation.json). Không giải nén trọn; Python stdlib, script inspect_review_archives.py --kind anomod và inspect_anomod_followup.py --run <mới>. Giữ lượt parse lỗi; không delete sau khảo sát.

## 10. Những điều còn mở

OPEN: xác nhận script/config revision đúng từng run và injection execution record, entity root-level cho host/DB, onset/end/recovery, log-ID schema và clock timezone SN. Thiếu các dữ kiện này giới hạn census gold/ranking/ngoài-root; không gọi không kiểm do chi phí là không thể kiểm. Đã kiểm mọi capture thực; không suy quality từ taxonomy hoặc số paper.

# TrainTicketTrace

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Urbanke và Fischer, SCCH; dataset Zenodo công bố 2025, trình bày SANER 2026. TrainTicket clean/faulty versions, collector/injector cụ thể chưa khóa.

Nguồn: [record](runs/run-002/sources/zenodo-17811972-latest.json); [conference abstract](runs/run-002/sources/traintickettrace-conference.html).

Giấy phép dữ liệu/code: Data CC-BY-4.0 theo record; code license chưa thấy trong metadata đã đọc.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Tên archive F1/F2/... là nhãn version, chưa chứng minh root/time theo incident. |
| 3 | Abstract công bố trace/metric/log; schema parent và nhãn trace còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Seeded faults theo abstract; mapping F-code sang root/fault/line chưa kiểm. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Clean reference version có nguồn; tính tương ứng workload và nhãn normal mỗi trace chưa kiểm. |
| 9 | Nhóm SCCH khác các họ còn lại, cùng TT. Chưa xác định injector/collector hoặc quan hệ với faulty branches DeepTraLog; không suy reuse chỉ từ F-code giống. |

Nguồn cho bảng: [record](runs/run-002/sources/zenodo-17811972-latest.json); [conference abstract](runs/run-002/sources/traintickettrace-conference.html).

## 3. Nhãn, số ca và khả năng phân xử

Record có 11 tar: 10 tên lỗi và 1 cleaned. Abstract hội nghị nói clean + 9 faulty versions. Chưa đồng nhất được hai cách đếm; không dùng tar làm incident.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Không có schema file thật trong phạm vi đã đọc.

Abstract công bố trace/metric/log; schema parent và nhãn trace còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Clean reference version có nguồn; tính tương ứng workload và nhãn normal mỗi trace chưa kiểm.

Ngữ nghĩa injection/onset/end và timezone còn OPEN. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. |
| Phát hiện thời gian | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Tên ca/thư mục có thể mang nhãn; chưa có adapter để kiểm loại rò.

Nhóm SCCH khác các họ còn lại, cùng TT. Chưa xác định injector/collector hoặc quan hệ với faulty branches DeepTraLog; không suy reuse chỉ từ F-code giống. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

Tổng 26.920.437.760 byte / 11 tar; từng tar ở record-summary. Không tải.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | Nhóm SCCH khác các họ còn lại, cùng TT. Chưa xác định injector/collector hoặc quan hệ với faulty branches DeepTraLog; không suy reuse chỉ từ F-code giống. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Chênh 9 faulty versions ở abstract so 10 tar có F-code; có thể version, scope hoặc archive split. Giữ cả hai; tác giả hoặc nhãn/source cần giải thích. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# Check Your Trace First (TRCA) — TrainTicket

## 1. Danh tính, nguồn và phạm vi đã kiểm

TRCA record19335897, Anonymous, 2026. CC-BY4 metadata, code license riêng chưa khóa. [Metadata](runs/review-sources-001/sources/zenodo-19335897.json), [download retry đạt checksum](runs/download-review-002/manifest.json), [README](runs/trca-reuse-001/README.md). Toàn archive CRC/hash kiểm, không chạy phương pháp. Cả1.165CSV và4nhãn byte-identical với Nezha; đây là reuse FACT, không chỉ chung tên hệ.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1 | Tải/checksum/CRC PASS; license record riêng nguồn Nezha không tự giải phạm vi quyền reused data. |
| 2 | Cùng nhãn Nezha đã census toàn: OB56/TT45,10root/hệ. |
| 3 | Cùng byte trace nên reuse đúng kiểm parent T008, không cần đọc lại để tạo số mới. |
| 4 | Cùng metric/log/linkage/clock T008; artifact có code không thêm dữ liệu mới. |
| 5 | Cùng root×fault/cell/repetition/graph T008. |
| 6 | Cùng fault categories Nezha; không thêm loại vì paper mới. |
| 7 | Dùng lại probe T008 đúng hash; giới hạn window/reference không biến mất. |
| 8 | Construct metric trùng fault và normal trace ngắn như T008. |
| 9 | Không độc lập với Nezha: fullinput CSV vàlabels identical. |

## 3. Nhãn, số ca và khả năng phân xử

[hash đối chiếu mọi CSV/labels](runs/trca-reuse-001/result.json). OBScope bốn ngày: NezhaOB56/10root/33cells, TT45/10root/23cells; mọi source labelmatch. Đếm TRCA+Nezha thành hai bộ đánh giá sẽ double-count cùng quan sát. Hash từng path kèm source path có thật; không suy chỉ từ overall ZIP size.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Đọc/hash toàn1.273entry,1.165CSV data; [hash đối chiếu mọi CSV/labels](runs/trca-reuse-001/result.json). Schema/NaN/parent/clock/log join/cadence/graph và negative coverage dùng lại [T008 đã kiểm](../T-008/the-dataset.md), vì raw từng byte cùng nhau; không gọi đây là semantic audit chưa làm. Model outputs/checkpoints trong ZIP chỉ checksum, không gold hoặc bằng chứng dataset.

## 5. Dữ liệu bình thường và mốc thời gian

Bốn construct trace minute-file và calendar metric như T008; không healthy giả giữa các capture. Nhãn injection text/epoch chưa onset/end; clock TT/OB có lỗi đã giữ.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

Probe theo [Nezha](../T-008/runs/trace-symptoms-002/result.json) và [metric reference không đủ](../T-008/runs/symptoms-003/result.json) được dùng lại đúng lineage; không tạo số đẹp hoặc claim propagation mới từ phương pháp TRCA.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn thực và giới hạn |
|---|---|
| Ranking | Như Nezha cùng hệ: root service record tiêm, có điều kiện clock/mapping/window. |
| Phát hiện theo thời gian | Trace/log injection-conditioned chỉ phút tiêm,+1,+2; không chấm continuous blind F1 từ release này. Metric ngày có scope khác, cần clock/normal. |
| Vùng ảnh hưởng | Không có nhãn vùng độc lập được xác minh; không chấm từ exceedance/causal_graph. |
| Trace anomaly | Không có nhãn anomalous từng trace thật trong labels. |

## 8. Rò nhãn và thông tin phục vụ G1

Trace/log/traceid tồn tại đúng ba phút quanh từng label; đổi tên không sửa selection. Tất cả fullCSVlabels trùng Nezha, không dùng một phía để dev và phía kia để test/giữ ngoài. Protocol code tác giả chưa được dùng làm benchmark phương pháp.

## 9. Kích thước và chi phí

ZIP335.076.044byte; logical3.048.387.906byte,1.273entry theo [size/CRC](runs/trca-inventory-001/archive.json). Lượt1 thiếu20.804byte, không đạt MD5, giữ file hỏng; lượt2 official record fileURL thành công. Download time ở hai manifest, không giấu lượt lỗi hoặc nhân đôi unique payload. Script inspect_review_archives.py --kind inventory và inspect_trca_reuse.py.

## 10. Những điều còn mở

Anonymous provenance tác giả và quyền reused data còn cần nguồn; nhưng reuse corpus với Nezha đã FACT, không còn OPEN. Ranking/time/normal limits kế thừa T008; không cần một experiment RCA để xác minh những điều này.

# Check Your Trace First (TRCA) — OnlineBoutique

## 1. Danh tính, nguồn và phạm vi đã kiểm

TRCA record19335897, Anonymous, 2026. CC-BY4 metadata, code license riêng chưa khóa. [Metadata](runs/review-sources-001/sources/zenodo-19335897.json), [download retry đạt checksum](runs/download-review-002/manifest.json), [README](runs/trca-reuse-001/README.md). Toàn archive CRC/hash kiểm, không chạy phương pháp. Cả1.165CSV và4nhãn byte-identical với Nezha; đây là reuse FACT, không chỉ chung tên hệ.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1 | Tải/checksum/CRC PASS; license record riêng nguồn Nezha không tự giải phạm vi quyền reused data. |
| 2 | Cùng nhãn Nezha đã census toàn: OB56/TT45,10root/hệ. |
| 3 | Cùng byte trace nên reuse đúng kiểm parent T008, không cần đọc lại để tạo số mới. |
| 4 | Cùng metric/log/linkage/clock T008; artifact có code không thêm dữ liệu mới. |
| 5 | Cùng root×fault/cell/repetition/graph T008. |
| 6 | Cùng fault categories Nezha; không thêm loại vì paper mới. |
| 7 | Dùng lại probe T008 đúng hash; giới hạn window/reference không biến mất. |
| 8 | Construct metric trùng fault và normal trace ngắn như T008. |
| 9 | Không độc lập với Nezha: fullinput CSV vàlabels identical. |

## 3. Nhãn, số ca và khả năng phân xử

[hash đối chiếu mọi CSV/labels](runs/trca-reuse-001/result.json). OBScope bốn ngày: NezhaOB56/10root/33cells, TT45/10root/23cells; mọi source labelmatch. Đếm TRCA+Nezha thành hai bộ đánh giá sẽ double-count cùng quan sát. Hash từng path kèm source path có thật; không suy chỉ từ overall ZIP size.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Đọc/hash toàn1.273entry,1.165CSV data; [hash đối chiếu mọi CSV/labels](runs/trca-reuse-001/result.json). Schema/NaN/parent/clock/log join/cadence/graph và negative coverage dùng lại [T008 đã kiểm](../T-008/the-dataset.md), vì raw từng byte cùng nhau; không gọi đây là semantic audit chưa làm. Model outputs/checkpoints trong ZIP chỉ checksum, không gold hoặc bằng chứng dataset.

## 5. Dữ liệu bình thường và mốc thời gian

Bốn construct trace minute-file và calendar metric như T008; không healthy giả giữa các capture. Nhãn injection text/epoch chưa onset/end; clock TT/OB có lỗi đã giữ.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

Probe theo [Nezha](../T-008/runs/trace-symptoms-002/result.json) và [metric reference không đủ](../T-008/runs/symptoms-003/result.json) được dùng lại đúng lineage; không tạo số đẹp hoặc claim propagation mới từ phương pháp TRCA.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn thực và giới hạn |
|---|---|
| Ranking | Như Nezha cùng hệ: root service record tiêm, có điều kiện clock/mapping/window. |
| Phát hiện theo thời gian | Trace/log injection-conditioned chỉ phút tiêm,+1,+2; không chấm continuous blind F1 từ release này. Metric ngày có scope khác, cần clock/normal. |
| Vùng ảnh hưởng | Không có nhãn vùng độc lập được xác minh; không chấm từ exceedance/causal_graph. |
| Trace anomaly | Không có nhãn anomalous từng trace thật trong labels. |

## 8. Rò nhãn và thông tin phục vụ G1

Trace/log/traceid tồn tại đúng ba phút quanh từng label; đổi tên không sửa selection. Tất cả fullCSVlabels trùng Nezha, không dùng một phía để dev và phía kia để test/giữ ngoài. Protocol code tác giả chưa được dùng làm benchmark phương pháp.

## 9. Kích thước và chi phí

ZIP335.076.044byte; logical3.048.387.906byte,1.273entry theo [size/CRC](runs/trca-inventory-001/archive.json). Lượt1 thiếu20.804byte, không đạt MD5, giữ file hỏng; lượt2 official record fileURL thành công. Download time ở hai manifest, không giấu lượt lỗi hoặc nhân đôi unique payload. Script inspect_review_archives.py --kind inventory và inspect_trca_reuse.py.

## 10. Những điều còn mở

Anonymous provenance tác giả và quyền reused data còn cần nguồn; nhưng reuse corpus với Nezha đã FACT, không còn OPEN. Ranking/time/normal limits kế thừa T008; không cần một experiment RCA để xác minh những điều này.

# OpenRCA — Telecom

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Xu và cộng sự, ICLR 2025; dữ liệu phát sinh từ AIOps Challenge, qua downsample/đổi tên/hiệu chỉnh/lọc. root có thể OS/pod/database; trace+metric, không có log theo paper A.2.

Nguồn: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

Giấy phép dữ liệu/code: Telemetry CC BY-NC 4.0 theo paper A.1; repo code MIT. Không lấy MIT áp vào telemetry.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | README có root occurrence datetime/component/reason, record.csv và query.csv. Bản phát hành/nhãn thật chưa đọc. |
| 3 | Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. |
| 4 | Trace+metric, không log theo A.2; schema sample của bài không thay kiểm file. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | CPU/network/database theo A.2. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias. |
| 9 | FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. |

Nguồn cho bảng: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

## 3. Nhãn, số ca và khả năng phân xử

Paper Table 1: 51 failure cases, 15 unique root components, 5 reasons. Đây là số công bố, không census query.csv hoặc record.csv.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Repo chỉ có dataset/README dẫn Drive; không có nhãn thật riêng trong tree ghim. Không mở Drive telemetry/Bank; census chưa làm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: CSV theo paper; root/time/reason là nhãn chấm. Giữ nguyên unit pod/node/service đến khi có mapping hợp lệ.

Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. Trace+metric, không log theo A.2; schema sample của bài không thay kiểm file.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias.

README/paper khai báo UTC+8. Occurrence time chưa được độc lập xác nhận là injection hoặc onset quan sát; không suy thời điểm kết thúc. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE chấm đúng entity OS/pod/database khi census/mapping đủ; không chấm service nếu nhãn chỉ pod. |
| Phát hiện thời gian | Có occurrence time; thiếu định nghĩa onset/end độc lập. Query cho khoảng và số lỗi không tương đương detector tự phát hiện. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

record.csv/query.csv chứa nhãn, query synthesis biết khoảng/số lỗi. main/task_specification.json ghi các đầu vào đó. Không đưa nhãn hoặc số lỗi thật vào detector tự phát hiện.

FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

Paper Table1 ghi 17,6 GB telemetry, không phải byte archive nén hay số byte đã tải. Google Drive có liên kết từ README nhưng chưa kiểm inventory file.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Repo chỉ có dataset/README dẫn Drive; không có nhãn thật riêng trong tree ghim. Không mở Drive telemetry/Bank; census chưa làm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Bản AIOps cụ thể, injector/collector, inventory/revision data và thời gian lỗi chưa khóa. Bảo toàn họ Bank theo quyết định root; các hệ khác không tự suy độc lập với Bank. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# OpenRCA — Bank

## 1. Danh tính, nguồn và phạm vi đã kiểm


FACT nguồn: Xu và cộng sự, ICLR 2025; dữ liệu phát sinh từ AIOps Challenge, qua downsample/đổi tên/hiệu chỉnh/lọc. root mức pod; README chỉ trace ngang pod, không có vertical deployment structure.

Nguồn: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

Giấy phép dữ liệu/code: Telemetry CC BY-NC 4.0 theo paper A.1; repo code MIT. Không lấy MIT áp vào telemetry.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.



Đính chính R3 sau REVIEW: [Metadata Drive/ZIPdirectory](runs/bank-metadata-001/summary.json), [inventory95member](runs/bank-metadata-001/zip-members.json), [census nhãn tái lập](runs/bank-label-reproduce-002/census.json): 136record/14root/8reason/9ngày/52ô root×reason. Chỉ inflate Bank/record.csv8.668byte, size/CRC/hash PASS; không telemetry/predictions. FileBank.zip 2829139841byte nén, 26400499433byte logical từcentraldirectory. Drive mutable: pin id/size/modified time/directoryhash/labelhash, chưa wholeZIPhash hoặc immutable data revision.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1 | Drive publicmetadata/range label truy cập được; không tải fullZIP. Data NC,codeMIT riêng. |
| 2 | Nhãn record thực cócomponent/time/reason; epoch/textUTC+8khớp. |
| 3 | Schema nguồn cóparent/span/trace, chất lượng file giữ tớiG3. |
| 4 | Ba modality theo nguồn; linkagequality chưa đọc. |
| 5 | 14root/52cells, từngroot×reason×date/lặp đãcensus; graphpositionG3. |
| 6 | 8reason CPU/memory/disk/network/JVM; khôngnhãn lỗi mã nguồn. |
| 7 | Không đọc telemetry theo quyết định bảo toàn WHY13. |
| 8 | Normal sạch/load/clock chưa kiểmG3. |
| 9 | AIOpsreuseFACT; công cụ/collector gốcOPEN, không đủtiêuchí9. |

## 3. Nhãn, số ca và khả năng phân xử

[Metadata Drive/ZIPdirectory](runs/bank-metadata-001/summary.json), [inventory95member](runs/bank-metadata-001/zip-members.json), [census nhãn tái lập](runs/bank-label-reproduce-002/census.json): 136record/14root/8reason/9ngày/52ô root×reason. Chỉ inflate Bank/record.csv8.668byte, size/CRC/hash PASS; không telemetry/predictions. FileBank.zip 2829139841byte nén, 26400499433byte logical từcentraldirectory.

Lặp theo ô/ngày ởcensus; không lấy querycount thayincident.14root đúng componentlabel, khôngnormalizepod→service tựý. Source sốcôngbố136/14/8 khớp actualnhưng khôngchứngminh quality đo.

## 4. Schema thật và chất lượng ba nguồn tín hiệu


Schema công bố: CSV theo paper; root/time/reason là nhãn chấm. Giữ nguyên unit pod/node/service đến khi có mapping hợp lệ.

Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. Metric+trace+log theo A.2; schema sample của bài không thay kiểm file.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.



## 5. Dữ liệu bình thường và mốc thời gian


Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias.

README/paper khai báo UTC+8. Occurrence time chưa được độc lập xác nhận là injection hoặc onset quan sát; không suy thời điểm kết thúc. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.



Epoch khớp datetimeUTC+8 toàn136record; chỉngữpháp nhãn, chưa xácnhận occurrence làtiêm/onset.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7


OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.



## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn thực và giới hạn |
|---|---|
| Ranking | Có136 label root component ở mức pod; cần entity mapping G3, không tự gọi service root. |
| Phát hiện theo thời gian | Occurrence datetime UTC+8 khớp epoch ở136record; chưa chứng minh injection/onset/end. Query biết khoảng/số lỗi không continuous detection. |
| Vùng ảnh hưởng | Không có nhãn vùng độc lập được xác minh; không chấm từ exceedance/causal_graph. |
| Trace anomaly | Nhãn trace anomalous chưa có bằng chứng; bảo toàn không đọc số đo. |

## 8. Rò nhãn và thông tin phục vụ G1


record.csv/query.csv chứa nhãn, query synthesis biết khoảng/số lỗi. main/task_specification.json ghi các đầu vào đó. Không đưa nhãn hoặc số lỗi thật vào detector tự phát hiện.

FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.



## 9. Kích thước và chi phí

[Metadata Drive/ZIPdirectory](runs/bank-metadata-001/summary.json), [inventory95member](runs/bank-metadata-001/zip-members.json), [census nhãn tái lập](runs/bank-label-reproduce-002/census.json): 136record/14root/8reason/9ngày/52ô root×reason. Chỉ inflate Bank/record.csv8.668byte, size/CRC/hash PASS; không telemetry/predictions. FileBank.zip 2829139841byte nén, 26400499433byte logical từcentraldirectory.

Only ZIPmetadata tail65.557byte vàlocalheader/labelrange1.757byte; không inflate telemetry. Driveid/size/modified+directoryCRCmanifest khóa bản đã quan sát, không hứa Drive bất biến. Dung lượng đĩa khi mởG3 gần26,4GB logical chưa tính scratch; laptop/EC2 budget cần kiểm trước tải.

## 10. Những điều còn mở

Còn giữ ngoài: parentquality, metric/log/clock/normal/position/symptom tớiG3; lý do là quyền bảo toàn, không chi phí. Injector/collector và exactAIOpsedition thiếu nguồn. Chọn Bank trước measurement không đồng nghĩa đạtđộđộc lập hoặc đảm bảoRCA. RQ3 ngoài thiết kế chỉ bao quát8reason của Bank, không kiểm lỗi mã nguồn. Nhãnactual đãcensus khôngcòn OPEN; wholearchivehash/immutablerevision thiếu vì khôngtảifulltelemetry.

# OpenRCA — Market

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Xu và cộng sự, ICLR 2025; dữ liệu phát sinh từ AIOps Challenge, qua downsample/đổi tên/hiệu chỉnh/lọc. root node/pod/service; hai cloudbed có telemetry thu riêng.

Nguồn: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

Giấy phép dữ liệu/code: Telemetry CC BY-NC 4.0 theo paper A.1; repo code MIT. Không lấy MIT áp vào telemetry.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | README có root occurrence datetime/component/reason, record.csv và query.csv. Bản phát hành/nhãn thật chưa đọc. |
| 3 | Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. |
| 4 | Metric+trace+log theo A.2; schema sample của bài không thay kiểm file. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | CPU/memory/disk/network/process theo A.2. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias. |
| 9 | FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. |

Nguồn cho bảng: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

## 3. Nhãn, số ca và khả năng phân xử

Paper Table 1: 148 failure cases, 44 unique root components, 15 reasons. Đây là số công bố, không census query.csv hoặc record.csv.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Repo chỉ có dataset/README dẫn Drive; không có nhãn thật riêng trong tree ghim. Không mở Drive telemetry/Bank; census chưa làm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: CSV theo paper; root/time/reason là nhãn chấm. Giữ nguyên unit pod/node/service đến khi có mapping hợp lệ.

Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. Metric+trace+log theo A.2; schema sample của bài không thay kiểm file.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias.

README/paper khai báo UTC+8. Occurrence time chưa được độc lập xác nhận là injection hoặc onset quan sát; không suy thời điểm kết thúc. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE chấm đúng entity node/pod/service khi census/mapping đủ; không chấm service nếu nhãn chỉ pod. |
| Phát hiện thời gian | Có occurrence time; thiếu định nghĩa onset/end độc lập. Query cho khoảng và số lỗi không tương đương detector tự phát hiện. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

record.csv/query.csv chứa nhãn, query synthesis biết khoảng/số lỗi. main/task_specification.json ghi các đầu vào đó. Không đưa nhãn hoặc số lỗi thật vào detector tự phát hiện.

FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

Paper Table1 ghi 24,5 GB telemetry, không phải byte archive nén hay số byte đã tải. Google Drive có liên kết từ README nhưng chưa kiểm inventory file.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Repo chỉ có dataset/README dẫn Drive; không có nhãn thật riêng trong tree ghim. Không mở Drive telemetry/Bank; census chưa làm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Bản AIOps cụ thể, injector/collector, inventory/revision data và thời gian lỗi chưa khóa. Bảo toàn họ Bank theo quyết định root; các hệ khác không tự suy độc lập với Bank. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# OpenRCA 2.0 — TrainTicket

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Fang và cộng sự, arXiv v2 năm 2026; TrainTicket; ChaosMesh, OpenTelemetry/Parquet/Prometheus. TT xây trên dữ liệu Fang/FSE; hai hệ còn lại chiến dịch mới theo paper.

Nguồn: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

Giấy phép dữ liệu/code: Paper A.6 nêu data CC-BY-SA4.0, pipeline Apache2.0. Giấy phép arXiv CC BY-NC-SA của bài là phạm vi khác. Public release chưa khóa.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | OPEN: A.6 nói preview/full anonymous trong submission, public sau acceptance; không có public archive ghim trong nguồn đã đọc. |
| 2 | Paper có service/pod/container/function/span/metric và injection window; chưa có census release. |
| 3 | FACT nguồn có trace; liên kết cha–con thật còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Application/resource/network/pod interventions theo paper; loại cụ thể theo hệ chưa census. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file. |
| 9 | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. |

Nguồn cho bảng: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

## 3. Nhãn, số ca và khả năng phân xử

Paper nói 500 evaluable instances tổng ba hệ, 27 primary kinds; không gán tổng này cho riêng TrainTicket.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Theo A.2/A.4: Parquet trace/metric/log, nhãn root và graph PAVE. Schema thật chưa có payload kiểm.

FACT nguồn có trace; liên kết cha–con thật còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file.

Paper có injection window [t0,t0+duration]; không suy onset thật. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE root set theo cấp nhãn công bố; cần release/census. |
| Phát hiện thời gian | CANDIDATE injection-regime nếu khoảng tiêm đủ; onset quan sát OPEN. |
| Vùng ảnh hưởng | Có graph propagation do PAVE tạo từ telemetry/quy tắc; không tự xem là nhãn vùng độc lập để chấm RQ3c. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

PAVE dùng root/injection tạo label; cần tách label/graph khỏi input phương pháp. Chọn ca qua SLI/path và loại graph trivial/cycle tạo selection bias.

TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

OPEN: chưa có inventory public archive ghim; số instance không chuyển thành byte.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Tình trạng public artifact hiện hành chưa xác minh thêm ngoài lượt tìm giới hạn; không khẳng định không tồn tại. Nhãn PAVE không mặc nhiên đáp ứng nhãn vùng độc lập MRP. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# OpenRCA 2.0 — OpenTelemetry Demo

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Fang và cộng sự, arXiv v2 năm 2026; OpenTelemetry Demo; ChaosMesh, OpenTelemetry/Parquet/Prometheus. TT xây trên dữ liệu Fang/FSE; hai hệ còn lại chiến dịch mới theo paper.

Nguồn: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

Giấy phép dữ liệu/code: Paper A.6 nêu data CC-BY-SA4.0, pipeline Apache2.0. Giấy phép arXiv CC BY-NC-SA của bài là phạm vi khác. Public release chưa khóa.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | OPEN: A.6 nói preview/full anonymous trong submission, public sau acceptance; không có public archive ghim trong nguồn đã đọc. |
| 2 | Paper có service/pod/container/function/span/metric và injection window; chưa có census release. |
| 3 | FACT nguồn có trace; liên kết cha–con thật còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Application/resource/network/pod interventions theo paper; loại cụ thể theo hệ chưa census. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file. |
| 9 | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. |

Nguồn cho bảng: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

## 3. Nhãn, số ca và khả năng phân xử

Paper nói 500 evaluable instances tổng ba hệ, 27 primary kinds; không gán tổng này cho riêng OpenTelemetry Demo.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Theo A.2/A.4: Parquet trace/metric/log, nhãn root và graph PAVE. Schema thật chưa có payload kiểm.

FACT nguồn có trace; liên kết cha–con thật còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file.

Paper có injection window [t0,t0+duration]; không suy onset thật. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE root set theo cấp nhãn công bố; cần release/census. |
| Phát hiện thời gian | CANDIDATE injection-regime nếu khoảng tiêm đủ; onset quan sát OPEN. |
| Vùng ảnh hưởng | Có graph propagation do PAVE tạo từ telemetry/quy tắc; không tự xem là nhãn vùng độc lập để chấm RQ3c. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

PAVE dùng root/injection tạo label; cần tách label/graph khỏi input phương pháp. Chọn ca qua SLI/path và loại graph trivial/cycle tạo selection bias.

TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

OPEN: chưa có inventory public archive ghim; số instance không chuyển thành byte.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Tình trạng public artifact hiện hành chưa xác minh thêm ngoài lượt tìm giới hạn; không khẳng định không tồn tại. Nhãn PAVE không mặc nhiên đáp ứng nhãn vùng độc lập MRP. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# OpenRCA 2.0 — Hotel Reservation

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Fang và cộng sự, arXiv v2 năm 2026; Hotel Reservation; ChaosMesh, OpenTelemetry/Parquet/Prometheus. TT xây trên dữ liệu Fang/FSE; hai hệ còn lại chiến dịch mới theo paper.

Nguồn: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

Giấy phép dữ liệu/code: Paper A.6 nêu data CC-BY-SA4.0, pipeline Apache2.0. Giấy phép arXiv CC BY-NC-SA của bài là phạm vi khác. Public release chưa khóa.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | OPEN: A.6 nói preview/full anonymous trong submission, public sau acceptance; không có public archive ghim trong nguồn đã đọc. |
| 2 | Paper có service/pod/container/function/span/metric và injection window; chưa có census release. |
| 3 | FACT nguồn có trace; liên kết cha–con thật còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Application/resource/network/pod interventions theo paper; loại cụ thể theo hệ chưa census. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file. |
| 9 | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. |

Nguồn cho bảng: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

## 3. Nhãn, số ca và khả năng phân xử

Paper nói 500 evaluable instances tổng ba hệ, 27 primary kinds; không gán tổng này cho riêng Hotel Reservation.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Theo A.2/A.4: Parquet trace/metric/log, nhãn root và graph PAVE. Schema thật chưa có payload kiểm.

FACT nguồn có trace; liên kết cha–con thật còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file.

Paper có injection window [t0,t0+duration]; không suy onset thật. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE root set theo cấp nhãn công bố; cần release/census. |
| Phát hiện thời gian | CANDIDATE injection-regime nếu khoảng tiêm đủ; onset quan sát OPEN. |
| Vùng ảnh hưởng | Có graph propagation do PAVE tạo từ telemetry/quy tắc; không tự xem là nhãn vùng độc lập để chấm RQ3c. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

PAVE dùng root/injection tạo label; cần tách label/graph khỏi input phương pháp. Chọn ca qua SLI/path và loại graph trivial/cycle tạo selection bias.

TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

OPEN: chưa có inventory public archive ghim; số instance không chuyển thành byte.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Tình trạng public artifact hiện hành chưa xác minh thêm ngoài lượt tìm giới hạn; không khẳng định không tồn tại. Nhãn PAVE không mặc nhiên đáp ứng nhãn vùng độc lập MRP. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# LO2 v1

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Nhóm Oulu/Helsinki (Bakhtin, Nyyssölä, Wang, Ping, Mäntylä và cộng sự), Light-OAuth2. Locust correct/error API tasks; Docker/Prometheus/Jaeger, v2 bổ sung cAdvisor.

Nguồn: [LO2 paper](runs/run-001/sources/lo2-paper-v1.html); [record current](runs/run-002/sources/zenodo-14938118-latest.json).

Giấy phép dữ liệu/code: Data CC-BY4.0; v2 record nêu code Apache2.0; license code v1 không thay bằng license data.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Correct/error API test labels, không phải root cause service của incident. v2 run log có start/end test theo mô tả. |
| 3 | v1 §4.3: mỗi trace một span, nhiều file rỗng; không đủ call graph cha–con. v2 record nói có trace CSV nhưng không chứng minh hạn chế này đã sửa. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Erroneous API usage, không phải hardware/network fault injection theo paper v1. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Có correct test; error test trộn correct requests với thêm error task, nên không gán mọi event trong error test là bất thường. |
| 9 | v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. |

Nguồn cho bảng: [LO2 paper](runs/run-001/sources/lo2-paper-v1.html); [record current](runs/run-002/sources/zenodo-14938118-latest.json).

## 3. Nhãn, số ca và khả năng phân xử

Paper v1: 1.740 runs × 54 tests, gồm correct + 53 error tasks. Test API không là incident RCA độc lập.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Index v2 riêng 31.028.530 byte vượt dự kiến nguồn 25MB của SPEC; không mở rộng tải. Nhãn root/time incident không có chỉ từ index mô tả. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Trace CSV công bố Trace ID/Span ID/Operation Name/Start/End/Tags; v1 thiếu cha xuyên operation. JSON metrics và container logs; v2 run_log/index chứa thời gian test.

v1 §4.3: mỗi trace một span, nhiều file rỗng; không đủ call graph cha–con. v2 record nói có trace CSV nhưng không chứng minh hạn chế này đã sửa. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Có correct test; error test trộn correct requests với thêm error task, nên không gán mọi event trong error test là bất thường.

Thời gian bắt đầu/kết thúc test API không tự là onset/end của sự cố hệ thống. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | Không đủ nhãn root cause service theo nguồn hiện có; đích API không thay nhãn nguyên nhân. |
| Phát hiện thời gian | Có thể chấm correct/error ở đơn vị test theo protocol rõ; không mặc định chấm thời gian triệu chứng hoặc service RCA. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | Không suy nhãn từng trace từ correct/error của cả test. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Tên test và log khởi tạo chứa correctness; record v1 nêu reduce_logs.py loại dòng khởi tạo lộ nhãn. v2 shuffle/duration random giảm quy luật thứ tự, không chứng minh sạch rò.

v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

v1 toàn raw lo2-data.zip 46.483.584.345 byte; sample 1.070.011.492 byte chỉ log/metric, không thay raw.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Index v2 riêng 31.028.530 byte vượt dự kiến nguồn 25MB của SPEC; không mở rộng tải. Nhãn root/time incident không có chỉ từ index mô tả. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | v1 record nói superseded bởi v2, nhưng endpoint latest của v1 vẫn chính record cũ: v2 là hồ sơ mới, không âm thầm thay DOI. Trace improvement v2 và mapping root còn OPEN. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# LO2 v2

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Nhóm Oulu/Helsinki (Bakhtin, Nyyssölä, Wang, Ping, Mäntylä và cộng sự), Light-OAuth2. Locust correct/error API tasks; Docker/Prometheus/Jaeger, v2 bổ sung cAdvisor.

Nguồn: [LO2 paper](runs/run-001/sources/lo2-paper-v1.html); [record current](runs/run-002/sources/zenodo-18937117-latest.json).

Giấy phép dữ liệu/code: Data CC-BY4.0; v2 record nêu code Apache2.0; license code v1 không thay bằng license data.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Correct/error API test labels, không phải root cause service của incident. v2 run log có start/end test theo mô tả. |
| 3 | v1 §4.3: mỗi trace một span, nhiều file rỗng; không đủ call graph cha–con. v2 record nói có trace CSV nhưng không chứng minh hạn chế này đã sửa. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Erroneous API usage, không phải hardware/network fault injection theo paper v1. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Có correct test; error test trộn correct requests với thêm error task, nên không gán mọi event trong error test là bất thường. |
| 9 | v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. |

Nguồn cho bảng: [LO2 paper](runs/run-001/sources/lo2-paper-v1.html); [record current](runs/run-002/sources/zenodo-18937117-latest.json).

## 3. Nhãn, số ca và khả năng phân xử

Record v2: 115 runs × 54 tests; chỉ là số công bố, không census index. Test API không là incident RCA độc lập.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Index v2 riêng 31.028.530 byte vượt dự kiến nguồn 25MB của SPEC; không mở rộng tải. Nhãn root/time incident không có chỉ từ index mô tả. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Trace CSV công bố Trace ID/Span ID/Operation Name/Start/End/Tags; v1 thiếu cha xuyên operation. JSON metrics và container logs; v2 run_log/index chứa thời gian test.

v1 §4.3: mỗi trace một span, nhiều file rỗng; không đủ call graph cha–con. v2 record nói có trace CSV nhưng không chứng minh hạn chế này đã sửa. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Có correct test; error test trộn correct requests với thêm error task, nên không gán mọi event trong error test là bất thường.

Thời gian bắt đầu/kết thúc test API không tự là onset/end của sự cố hệ thống. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | Không đủ nhãn root cause service theo nguồn hiện có; đích API không thay nhãn nguyên nhân. |
| Phát hiện thời gian | Có thể chấm correct/error ở đơn vị test theo protocol rõ; không mặc định chấm thời gian triệu chứng hoặc service RCA. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | Không suy nhãn từng trace từ correct/error của cả test. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Tên test và log khởi tạo chứa correctness; record v1 nêu reduce_logs.py loại dòng khởi tạo lộ nhãn. v2 shuffle/duration random giảm quy luật thứ tự, không chứng minh sạch rò.

v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

v2 full LO2v2.zip 65.613.664.046 byte; index riêng 31.028.530 byte. Chưa tải; tất cả file/byte ở record-summary.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Index v2 riêng 31.028.530 byte vượt dự kiến nguồn 25MB của SPEC; không mở rộng tải. Nhãn root/time incident không có chỉ từ index mô tả. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | v1 record nói superseded bởi v2, nhưng endpoint latest của v1 vẫn chính record cũ: v2 là hồ sơ mới, không âm thầm thay DOI. Trace improvement v2 và mapping root còn OPEN. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.
