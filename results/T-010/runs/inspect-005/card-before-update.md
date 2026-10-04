# DeepTraLog — Train Ticket : thẻ dataset

Ngày kiểm: 03/10/2026. **Phần nguồn/metadata đã kiểm; toàn task chưa xong.** Không có quyết định chọn dataset. Thẻ phục vụ MRP §4/P2, DT18-NV2/NV3 và G1. FACT nguồn không đồng nghĩa FACT trên dữ liệu đo.

## 1. Danh tính, nguồn và phạm vi đã kiểm

| Mục | Bằng chứng |
|---|---|
| Danh tính | DeepTraLog, FudanSELab; bài ICSE 2022 của Chenxi Zhang và cộng sự. Paper §4.1 mô tả Train Ticket V0.2.0, lỗi từ các nhánh của hệ; SkyWalking thu trace/log, Elasticsearch lưu. |
| Biến thể | `TraceLogData/F01–F14.zip` chứa lỗi; `normal/` dữ liệu bình thường; `alllog/` gộp log; `GraphData/` đồ thị xử lý từ raw. Trang tác giả nêu quan hệ này; chưa kiểm ghép raw–processed. |
| Nguồn | [Kho tác giả](https://github.com/FudanSELab/DeepTraLog), [trang dữ liệu](https://fudanselab.github.io/DeepTraLog/), [paper](https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf). Snapshot trong [manifest](runs/run-001/manifest.json). Revision/hash chỉ ghi ở manifest/inventory. |
| Giấy phép | **OPEN** cho code lẫn dữ liệu: tree đầy đủ không có đường dẫn LICENSE/COPYING, README không cấp phép. Công khai không đủ chứng minh quyền dùng; cần tác giả làm rõ trước phần sử dụng phụ thuộc. |
| Đơn vị số đếm | FACT metadata: [count-summary](runs/run-001/count-summary.json) có 14 archive lỗi, 10 archive normal, 5 phần alllog, 8 phần graph. Không coi archive/part là số incident độc lập. |
| Số công bố | Paper §4.1: 132.485 trace, 23.334 trace bất thường, 7.705.050 log, 73 fault instances trong 14 fault cases; một case có thể chứa nhiều instance ở nhiều service. Đây là số tác giả công bố, chưa đếm file. |
| Đã có / được phép / thực kiểm | Telemetry tải về: 0 archive; ca được phép đọc: chưa xác định, chờ Minh; ca thực kiểm: 0. Đã đọc source/code và metadata toàn Git tree; không đọc archive nội bộ. |
| Tái lập | `py -3 -B results/T-010/scripts/collect_metadata.py --verify --validate-counts`; lấy nguồn vào lượt mới bằng `--sources --run run-002 --verify`. Lượt đầu, byte và thời gian ở manifest; giữ nguyên lượt cũ. |

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả/trạng thái | Bằng chứng và giới hạn |
|---|---|---|
| 1. Công khai/tải/giấy phép | FACT kho/source truy cập được; OPEN archive và giấy phép | Manifest có HTTP/hash nguồn. Không tải ZIP; không lấy quyền từ việc GitHub cho tải. |
| 2. Root và thời điểm lỗi | OPEN | Code có nhãn trace và loại trace lỗi; chưa có census root/service hoặc onset/injection theo ca. Một fault branch có thể chứa nhiều lỗi. |
| 3. Trace cha–con | FACT paper mô tả; OPEN chất lượng file | Paper §3 có parent/child và lời gọi đồng bộ/bất đồng bộ. Code graph không thay schema raw. |
| 4. Metric/log | FACT nguồn nói trace/log; OPEN metric riêng | `alllog` không phải modality độc lập với log ở F/normal. Chưa thấy metric release riêng trong tree; có latency trong span cũng không chứng minh resource metrics. |
| 5. Nhiều root/vị trí | OPEN | 73 fault instances không cho số root khác nhau hoặc bậc của chúng. Cần mapping nhãn và graph đúng ca. |
| 6. Tài nguyên/mạng/mã nguồn | FACT bốn nhóm gốc ở mục 3; OPEN nhóm MRP | Không chuyển tên nhóm lỗi sang resource/network/code bằng suy đoán. |
| 7. Triệu chứng ngoài root | OPEN — chưa kiểm | Chưa quyền telemetry và chưa census root. Nhiều trace lỗi có thể cùng một căn nguyên hoặc workflow. |
| 8. Normal đủ học ngưỡng | FACT có normal archives; OPEN độ dài/chất lượng | Tên file và train split không chứng minh tải đại diện hoặc normal sạch. |
| 9. Bộ độc lập | OPEN ở mức bộ chọn | Nhóm Fudan, faulty branches, SkyWalking/Elasticsearch là thông tin so sánh. Dùng lại Train Ticket không tự chứng minh độc lập với RCAEval/Eadro/Nezha; cần lineage giữa thẻ. |

## 3. Nhãn, số ca và khả năng phân xử

Các nhóm dưới là Table 1 của paper, không phải nhóm lỗi đã quyết của nghiên cứu. Bảng archive thật nằm trong [inventory](runs/run-001/inventory.csv).

| Nhãn nhóm gốc | Fault case theo paper | Root / repetition / ô root×fault |
|---|---|---|
| Asynchronous Interaction | F1, F2, F13 | OPEN |
| Multi-Instance | F8, F11, F12 | OPEN |
| Configuration | F3, F4, F5, F7 | OPEN |
| Monolithic | F6, F9, F10, F14 | OPEN |

Đếm metadata xác minh tên archive F01–F14; chưa xác minh từng fault instance hoặc số lần lặp. Tổng root, root×fault, ô thiếu, lỗi parse nhãn: OPEN vì label lẫn trong archive, không có label riêng được thấy ở tree. Số service toàn hệ trong paper không thay số service gốc.

| Đồ thị | Hướng cạnh / node | Bậc root raw, số node/cạnh, khác topology |
|---|---|---|
| Raw span → service graph | CANDIDATE: cha→con; cần schema ID và mapping service thật | OPEN toàn bộ; chưa quyền số đo |
| Processed TEG | Nguồn: node là event; cạnh có sequence, request, response, async | Không coi TEG là đồ thị service hoặc lấy bậc event làm vị trí root service |

## 4. Schema thật và chất lượng ba nguồn tín hiệu

| Nguồn/biến thể | Đã kiểm ca telemetry | Schema có căn cứ | Chất lượng chưa kiểm |
|---|---|---|---|
| Trace trong F/normal | 0 | Paper mô tả span; exact field/time/status/sentinel chưa kiểm | Span count, trùng/null ID, ghép parent, coverage service |
| Log F/normal/alllog | 0 | Trang tác giả xác nhận log; exact field và trace ID trong payload OPEN | Có cột ID/có giá trị/chuỗi giống ID/ghép được đều OPEN |
| Metric riêng | 0 | Không thấy file riêng ở tree bên ngoài ZIP; nội bộ OPEN | NaN/gap/cadence/đơn vị/service mapping OPEN |
| GraphData | 0 | [dataset.py](runs/run-001/sources/model__dataset.py): `node_info`, `edge_index`, `edge_attr`, `trace_bool`, `trace_id`, `error_trace_type`; đây là schema loader kỳ vọng | Chưa xác minh member, độ phủ hay mapping về raw |

Code `dataset.py` chuyển `trace_bool is True` thành `y=0`, còn lại `y=1`; [main.py](runs/run-001/sources/model__main.py) quy 0 normal/1 abnormal. Đây là FACT về code; null/missing cũng đi nhánh 1 trong loader, nên phải kiểm giá trị gốc trước dùng nhãn. Chưa thực thi loader.

| Phép đếm parent | Kết quả |
|---|---|
| Tổng span; root theo sentinel | OPEN, chưa đọc trace |
| Có parent cần resolve; cha duy nhất | OPEN, chưa có tử/mẫu |
| Cha thiếu; cha không duy nhất; tỷ lệ resolve | OPEN; không ghi 0% khi chưa có mẫu |

Liên kết có thật không tự chứng minh nhân quả. Status/error, server/client duplication, MQ/database coverage còn OPEN; thiếu cha có thể do sampling/cắt file/mất span.

## 5. Dữ liệu bình thường và mốc thời gian

Normal có vùng riêng theo trang tác giả và 10 ZIP ở metadata. Loader tách normal bằng nhãn trace, shuffle rồi chia 60% train, 10% validation, 30% test; mọi abnormal vào test (code main.py). Đây là giao thức công bố, không phải phương án G1 của Minh.

Mốc injection/onset/end, clock/timezone, cửa sổ trước/sau theo từng ca: OPEN. Dữ liệu từ phiên bản lỗi không tự là một chuỗi normal→fault liên tục. Độ dài normal, độ ổn định tải và khả năng học ngưỡng còn OPEN; tên normal không loại được nhiễm lỗi hoặc warm-up.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

**OPEN — chưa kiểm.** Chưa quyền đọc telemetry và chưa nhãn root đủ để xác định “ngoài root”. Không chạy q=.95/.99/.995, không tạo nhãn lan. Cả F/normal/alllog/GraphData đều chưa kiểm số đo. Trace có nhiều service hoặc event bất thường không thay nhãn vùng ảnh hưởng; đồng thời còn có thể do workload, branch lỗi hay instrumentation.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn đã xác minh ở mức nào | Chấm được đến đâu |
|---|---|---|
| Xếp hạng root | Chưa file root/service theo từng instance | OPEN MRR/Hit/NDCG; `error_trace_type` không tự là root |
| Phát hiện theo thời gian | Chưa onset/interval | OPEN P/R/F1 cửa sổ và độ trễ; nhãn trace không chuyển tự động |
| Vùng ảnh hưởng | Chưa tập thành phần thật | OPEN; TEG/attention không phải ground truth vùng |
| Bất thường từng trace | Loader có nhãn nhị phân, paper dùng đơn vị trace | CANDIDATE P/R/F1 trace sau audit label/raw–processed; chưa kiểm độ phủ nhãn |

Code train dùng normal labels; ngân sách nhãn và khả năng baseline chuyển hệ phải chốt ở G1. Chưa huấn luyện, chưa suy “đủ” từ tổng trace công bố.

## 8. Rò nhãn và thông tin phục vụ G1

Fault nằm trong tên F archive, normal folder, `trace_bool` và `error_trace_type`. Chỉ dùng để census/chấm hoặc đúng ngân sách học được duyệt. Loader giữ `error_trace_type`/`trace_id` trong Data; việc adapter lõi có loại bỏ chúng còn OPEN. Không thấy root-derived SLI được chứng minh trong phần code đã đọc; không gọi như vậy là adapter đã an toàn.

Biên/order file có tiết lộ thời điểm hay class: OPEN; không áp cảnh báo cửa sổ đối xứng của RCAEval thành FACT ở đây. Raw, alllog và graph có thể trùng trace/log vì cùng lineage; chưa được chia sang dev/test khác phía khi chưa kiểm ID. WHY-04 là đề xuất, G1 chưa chốt split/holdout cho DeepTraLog.

## 9. Kích thước và chi phí

FACT byte blob từ [summary](runs/run-001/count-summary.json); gồm archive nén, không phải giải nén:

| Nhóm | File/part | Byte |
|---|---:|---:|
| F01–F14 | 14 | 124.562.627 |
| normal | 10 | 209.086.987 |
| alllog | 5 | 213.216.632 |
| GraphData | 8 | 181.965.367 |

Toàn tree: 54 blob, 981.899.762 byte, bao gồm kết quả công bố và code; không lấy tổng này làm dung lượng dataset độc lập. Dung lượng giải nén, RAM/giây đọc mẫu, chi phí adapter: OPEN. [inspection-plan](inspection-plan.md) ghi archive cụ thể và phạm vi cần duyệt; chưa tải.

## 10. Những điều còn mở

| OPEN | Đầu vào/owner | Kết luận phụ thuộc |
|---|---|---|
| Quyền telemetry/giữ ngoài | Minh tại gói T-003 | Mọi phép kiểm số đo; tiêu chí 7 chờ G3 nếu giữ ngoài |
| Giấy phép code/dữ liệu | Tác giả làm rõ; Minh quyết bước tiếp | Tiêu chí 1, dùng/chia sẻ artifact |
| Root×fault×lặp và nhãn thời gian | Metadata bên trong archive sau đúng quyền; Codex | Tiêu chí 2/5/6 và ranking/time evaluation |
| Schema, parent, raw↔processed, normal | File cụ thể ở kế hoạch; Codex | Đồ thị và ánh xạ đa nguồn |
| Độc lập với các release TT khác | Đối chiếu nguồn tất cả thẻ tại G1 | Tiêu chí 9; cùng tên hệ không đủ kết luận |

Bằng chứng hiện có mô tả distribution và loader, chưa phân xử chất lượng telemetry, vị trí root hoặc triệu chứng lan. Không chọn/bỏ DeepTraLog từ thẻ này.
