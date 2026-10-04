# LEMMA-RCA OT — SWaT và WADI, thẻ danh mục

Ngày kiểm 03/10/2026. Phần này giữ cả hai hệ OT trong phạm vi T-011. Chỉ kiểm nguồn, code và hằng số nhãn; chưa tải dữ liệu. Không quyết định phù hợp/loại khỏi G1.

## 1. Danh tính, nguồn và phạm vi đã kiểm

| Biến thể | Nguồn/version |
|---|---|
| SWaT gốc và LEMMA subset | [iTrust SWaT](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/); LEMMA OT README dùng December 2015 làm ví dụ; subset release mapping OPEN |
| WADI gốc và LEMMA subset | [iTrust WADI](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/wadi/); LEMMA OT README dùng WADI.A1; iTrust có bản A2 sửa ngày/normal/label |
| Code và paper | [Kho LEMMA](https://github.com/lemma-rca/rca_baselines), [paper v4](https://arxiv.org/html/2406.05375v4), [catalog](https://lemma-rca.github.io/docs/data.html). [Manifest](runs/run-001/manifest.json) ghim code/hash/source. |
| Quyền dùng | [iTrust terms](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/) yêu cầu xin dataset, attribution và không chia sẻ lại. License LEMMA NC/ND mâu thuẫn không override nguồn gốc. |
| Phạm vi đã kiểm | 0 file/ca telemetry trên máy, quyền telemetry chờ Minh; số nguồn/code/nhãn literal có trong manifest/labels-from-code. Không truy cập `data/locked`. |
| Chạy lại | `py -3 -B results/T-011/scripts/collect_metadata.py --verify --validate-counts`; không chạy code OT tác giả |

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | SWaT | WADI | Giới hạn/giải thích khác |
|---|---|---|---|
| 1. Công khai/tải/license | Catalog public; phải xin dữ liệu | Tương tự | Chưa gửi yêu cầu; không đồng nghĩa tải trực tiếp HF |
| 2. Root/thời điểm | Nguồn có attack labels; subset mapping OPEN | Hằng số code có root/ranges; mapping OPEN | Nhãn attack không đồng nghĩa onset symptom |
| 3. Trace cha–con | Không phải modality trace span trong catalog | Tương tự | Network traffic gốc không phải distributed span; graph kiến trúc chỉ CANDIDATE |
| 4. Metric/log | Sensor/actuator time series theo nguồn | Tương tự | Không coi historian là log ứng dụng/trace; chất lượng file chưa kiểm |
| 5. Nhiều root/vị trí | OPEN số root subset/graph | Code root strings có đếm; graph OPEN | Node/sensor không là service microservice |
| 6. Resource/network/code | Attack scenarios OT; mapping MRP OPEN | Tương tự | Không tự dùng phân loại microservice cho cyberphysical attack |
| 7. Triệu chứng ngoài root | OPEN — chưa kiểm | OPEN — chưa kiểm | Không telemetry; đồng thời sensor không tự là lan nhân quả |
| 8. Normal học ngưỡng | Nguồn có normal; chất lượng subset OPEN | Nguồn có normal; phiên bản quan trọng | Chắp đoạn/tải thay đổi có thể làm ngưỡng sai |
| 9. Độc lập | iTrust testbed và acquisition khác IT | iTrust cùng nhóm với SWaT | Không coi SWaT/WADI hoặc raw/subset độc lập hoàn toàn chỉ do khác tên |

## 3. Nhãn, số ca và khả năng phân xử

| Bộ/nguồn đếm | Số được nguồn/codе nêu | Phạm vi |
|---|---:|---|
| SWaT A1 iTrust | 41 attacks; 51 sensors/actuators | Toàn phiên gốc nguồn công bố; không đếm file |
| SWaT catalog LEMMA | 16 faults | Subset mô tả, mapping về 41 còn OPEN |
| WADI A1 iTrust | 15 attacks; 123 sensors/actuators | Gốc; A2 có sửa ngày/labels |
| WADI catalog LEMMA | 9 faults | Không đồng nhất với số attack gốc |
| WADI segmentation code | 14 intervals | Hằng số `attack_time_ranges`, chưa chạy trên raw |
| OT evaluation code | 14 nhóm root, 6 nhóm đa root, 22 chuỗi entity khác nhau | Hai evaluator có cùng literal; chưa ghép thứ tự ra archive/ca thật |

Kết quả literal tại [labels-from-code](runs/run-001/labels-from-code.json). Appendix D nói chọn single-sensor/actuator nhưng code nhãn có nhóm đa root; giữ mâu thuẫn OPEN. Số loại lỗi, root×fault×lặp, ô thiếu theo subset: chưa xác minh. Đồ thị/cạnh hướng, bậc root tại đúng ca, node/edge count: OPEN. Schema `Node_Name`/`Pod_Name` trong code là cách nhóm stage/sensor, không chứng minh có Kubernetes.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

| Nguồn | Ca thật đã kiểm | Source schema | Chất lượng |
|---|---:|---|---|
| Metric/historian | 0 | README OT: Sequence, Time, Node_Name, KPI_Feature; raw timestamp/sensor/label | Đơn vị từng sensor, gap/NaN/constant/duplicate, đồng bộ chưa kiểm |
| Log ứng dụng | 0 | Không mô tả modality này trong LEMMA OT catalog | Không suy từ network/historian là log ứng dụng |
| Trace span | 0 | Không mô tả trace ID/span ID/parent ID | Tổng span/root/resolve/ambiguous/missing không áp từ source hiện có; chưa có trace để đo |

Code WADI có fill missing bằng 0 và drop all-NaN columns; đây là FACT code, chưa chứng minh output mọi release đã dùng cùng script. Không coi số 0 là đo thật. Bản iTrust A2 bỏ normal readings bất ổn; cần version cụ thể trước so chất lượng.

## 5. Dữ liệu bình thường và mốc thời gian

iTrust SWaT A1: 11 ngày gồm 7 normal và 4 attack; WADI A1: 16 ngày gồm 14 normal và 2 attack (lời nguồn). SWaT normal version 1 bỏ 30 phút đầu draining của version 0; WADI A2 sửa bảng ngày và bổ sung nhãn -1/1. Không tự chọn bản thay tác giả.

Paper Appendix D mô tả subset dài 2 giờ, ghép normal trước/sau và đưa attack giữa segment. Code WADI thực có các khoảng normal từ ngày khác; chưa chứng minh output cuối giống paper. Nhãn injection/attack không phải onset/end triệu chứng quan sát. Dữ liệu normal thật/cadence/số điểm sau chuyển đổi và độ đủ học ngưỡng: OPEN.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa quyền telemetry/giữ ngoài và chưa license/version/subset thống nhất. Không chạy threshold, không tạo nhãn lan từ nhóm sensor. Plant coupling, chắp đoạn normal, sensor hỏng và chung controller đều có thể giải thích biến đổi đồng thời.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Phạm vi hỗ trợ từ nguồn | Giới hạn |
|---|---|---|
| Ranking root | Có target sensor/actuator trong code/gốc | CANDIDATE sau mapping ca; không tự chuyển thành service ranking |
| Detection theo thời gian | Nguồn có attack interval/labels | Chỉ attack-regime khi xác minh bản và cửa sổ; onset thật OPEN |
| Vùng ảnh hưởng | Chưa nhãn toàn vùng | Tập target nhiều sensor có thể là nhiều nguyên nhân, không là toàn vùng |
| Bất thường trace | Không trace labels được thấy | Chưa có căn cứ chấm trace unit |

Giám sát/không giám sát và split theo attack/entity còn để G1 quyết. Nhãn -1/1 không được đưa vào feature của phương pháp hoặc chọn ngưỡng test.

## 8. Rò nhãn và thông tin phục vụ G1

Code dùng attack times để cắt dữ liệu; nhãn có trong data intermediate. Paper đặt attack giữa segment nên có nguy cơ đoán mốc từ vị trí/biên dù bỏ cột label. Đây là FACT quy tắc nguồn; extent file thực còn OPEN. Không thay cách cắt khi chưa Minh quyết.

Paper mô tả tạo KPI liên tục từ detector cho OT; KPI như vậy không phải nhãn onset độc lập. Trình tự khai thác label trong code/adapter cần xác minh trước phương pháp. Raw và subset cùng nguồn không được coi là hai bộ giữ ngoài độc lập.

## 9. Kích thước và chi phí

Catalog ghi SWaT 236M, WADI 848M; paper Table 2 ghi 4.47G/5.67G, đơn vị/phạm vi phiên bản chưa thống nhất. Đây là số công bố ở [snapshot catalog](runs/run-001/sources/author-catalog.html) và [paper](runs/run-001/sources/paper-v4.html), không phải byte ZIP đã audit. Không có public manifest HF cho OT trong bốn kho IT đã kiểm.

Byte cần xin/tải, giải nén, RAM/giây đọc: OPEN. Dữ liệu chưa tải; chỉ code/docs/label literals dưới ngân sách nguồn. Cần Minh và iTrust để tiếp phần truy cập; không nhầm thời gian chờ iTrust với runtime xử lý.

## 10. Những điều còn mở

| OPEN | Owner/đầu vào | Hệ quả |
|---|---|---|
| Bản/subset và mapping 41→16, 15→9/14 | Tác giả LEMMA/iTrust và file label đúng phiên bản | Không chốt census hay single/multi root |
| Quyền truy cập/telemetry/giữ ngoài | Minh; iTrust nếu xin dataset | Không kiểm số đo trước quyền |
| Terms upstream và NC/ND | Nguồn sở hữu, Minh quyết bước tiếp | Không tự phân phối/sử dụng theo một license chọn lọc |
| Đồ thị vật lý, alias và unit đánh giá | Sơ đồ/mapping có nguồn, dữ liệu được phép | Không đánh đồng với đồ thị span/service |
| Normal/biên/label flow | File thật/adapter sau quyền | Detection validity và tiêu chí 7/8 |

Thẻ này bảo toàn OT để G1 xét có chủ đích. Chưa đủ căn cứ loại/chọn chỉ vì khác domain hoặc không có distributed span trong catalog.
