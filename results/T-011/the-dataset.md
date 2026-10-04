# LEMMA-RCA — thẻ IT sau kiểm mẫu Q-47

Nguồn: [xác minh nguồn và độc lập](xac-minh-nguon-va-doc-lap.md). File thật: [báo cáo kiểm](kiem-file.md), [summary](file-inspection-summary.json). Chỉ kiểm Preprocessed PR20211203 và Cloud20240124; Original và ngày khác chỉ metadata. OT bỏ theo Q-47. Bank bảo toàn theo Q-49; LEMMA không giữ ngoài.

# Product Review — Original và Preprocessed

## 1. Danh tính, nguồn và phạm vi

LEMMA-RCA, Zheng và cộng sự; [paper v4](https://arxiv.org/html/2406.05375v4), [code tác giả](https://github.com/lemma-rca/rca_baselines), [Original](https://huggingface.co/datasets/Lemma-RCA-NEC/Product_Review_Original), [Preprocessed](https://huggingface.co/datasets/Lemma-RCA-NEC/Product_Review_Preprocessed). Revision khóa tại [manifest](runs/source-final-001/manifest.json). Original/Preprocessed chung lineage. License NC/ND chính xác còn OPEN; kiểm nội bộ phi thương mại theo WHY-14 không cấp quyền chia sẻ payload phái sinh. Đã kiểm toàn bộ member hai ZIP metric/log ngày 20211203; các ngày khác và Original chỉ metadata.

## 2. Bảng tiêu chí MRP1–9

| Tiêu chí | Kết quả đúng phạm vi mẫu |
|---|---|
| 1. Công khai/tải/license | Byte/LFS SHA public revision khớp; license cuối OPEN. |
| 2. Root/time | Nhãn và clock theo mục3/5; không suy mốc tiêm thành onset đã kiểm. |
| 3. Trace cha–con | ZIP mẫu không có span table; parent/degree Original OPEN. |
| 4. Metric/log | 26 NPY, 43.314.418 CSV rows; chất lượng kiểm từng file. |
| 5. Root/vị trí | Có mapping entity; không có trace graph để đo bậc root. |
| 6. Nhóm lỗi | External storage disk full ảnh hưởng database; một scenario chưa phủ mọi nhóm. |
| 7. Triệu chứng ngoài root | Normal/mốc lỗi và KPI lineage chưa đủ; không nhãn vùng. |
| 8. Normal học ngưỡng | OPEN, không dùng phần đầu tùy ý. |
| 9. Độc lập | Raw/processed chung lineage; PR/Cloud chưa đủ coi hai bộ độc lập; không census raw reuse xuyên bộ. |

## 3. Nhãn, ca và khả năng phân xử

README gọi root MongoDB-v1. PPTX mô tả nguyên nhân external NFS đầy đĩa, nối MongoDB rồi ảnh hưởng ratings. Giữ riêng entity nhãn benchmark và nguyên nhân vận hành ngoài cluster; chưa thay pod bằng storage hoặc ngược lại. Một ngày mẫu không là census root×fault×repetition toàn release. Nguồn có 4 PR/6 Cloud date token; không coi chúng là incident count. Sơ đồ PPTX không thay trace graph. Bậc root và confound vị trí–loại lỗi vẫn OPEN.

## 4. Schema và chất lượng ba nguồn tín hiệu

NPY object dict dùng KPI_* hoặc jaeger_*, Sequence/time và Pod_Name/Node_Name. Log NPY có layout entity×time×feature; CSV structured có LineId, Time, Content, EventId, EventTemplate, ParameterList. Static reader không thực thi pickle. Có 2 nonfinite và 110 constant column occurrences, kể cả KPI/alias; 197.543 byte không giải được UTF-8 trong 16 CSV; 0 ragged rows. Encoding khác có thể giải thích, chưa gọi file hỏng. Cadence/gap/unit và từng kênh xem summaries; preprocessing có thể che missing raw.

Metric có 224 tên entity; structured log có 1177 tên file; giao chính xác 160; log-feature NPY có 132 entity. Ba tập giữ riêng. p2n có 302 pod→node, không là graph gọi dịch vụ. Không cột trace/span ID trong CSV; ID trong payload và khả năng ghép parent chưa có hợp đồng được xác minh. Không suy Original thiếu trace.

## 5. Normal và thời gian

KPI CSV dùng epoch microsecond, NPY dùng epoch giây và log UTC. Mốc injection/normal/recovery của ngày mẫu chưa xác minh; không lấy một phần đầu tùy ý làm normal. Ví dụ Jaeger trong PPTX có ngày khác, không là span thật của mẫu. Cadence là FACT file, tách khỏi lịch nguồn. Injection, narrative failure time và recovery là ba loại thông tin khác; không tự sửa clock/nhãn.

## 6. Mô tả thô triệu chứng ngoài root

Chưa có normal/mốc lỗi được xác minh và KPI provenance còn khác. Không tính band bằng một phần thời gian chọn tùy ý. Chất lượng toàn mẫu đã kiểm; cần nguồn mốc và normal để phép mô tả có ý nghĩa. Co-occurrence có thể do workload chung, nhiễu, threshold zero hoặc preprocessing. Không OR các kênh, không regex mức lỗi làm nhãn vùng, không kết luận propagation từ vượt band. Đây là mô tả P2, chưa chọn detector hoặc chia dev/test.

## 7. Task nào chấm được?

Ranking root là CANDIDATE theo đúng đơn vị nhãn sau chốt mapping. PR cần giữ khác biệt pod MongoDB và storage cause. Time detection cần giao thức và interval nhãn phù hợp, không gọi onset đã verified. Không nhãn vùng/trace thật để chấm segmentation hoặc trace anomaly. Không RCA/baseline/training chạy trong task.

## 8. Rò nhãn, provenance và G1

Không đưa date/PPTX/root vào đầu vào phương pháp. Case-dependent KPI/metric selector code nguồn chưa là adapter an toàn cho chế độ tự phát hiện. 46/46 Sequence case không nối đầy đủ hoặc khác giá trị so kpi.csv. CSV chỉ có ratings; NPY thêm reviews/reviews-v2/reviews-v3. Ví dụ node ratings: 63.976 điểm ghép, 37.938 điểm thiếu, 63.974 điểm khác. Cần giải thích provenance/KPI hoặc exporter; không tự sửa release. Vector trùng giữ ở summary, không đếm alias thành lặp. Không chia Original/Preprocessed cùng ca sang hai phía. Chưa chọn dataset thí nghiệm.

## 9. Kích thước và chi phí

Hai ZIP mẫu 1.472.841.528 byte; 16.268.296.541 byte member được stream. Toàn kho Original PR 53.633.808.946byte/Cloud 33.002.132.069byte theo [census](runs/run-001/count-summary.json), chưa tải. Full audit 200,284s, correction 135,206s, bổ sung schema 2,824s tái dùng kết quả; không gọi 2,824s là toàn scan. Xem kiem-file cho RAM/lượt lỗi/interrupt và giới hạn dự báo chi phí.

## 10. OPEN và owner

Tác giả: exact license, PR KPI provenance và mốc normal/injection. Codex/Minh: nguồn Original/parent, phủ ngày khác, đúng unit ranking; mở rộng cần quyền và byte cụ thể trước làm. Minh: chọn G1/thí nghiệm; Claude review gộp T003. Không xem kiểm một ngày là kiểm toàn release hoặc đáp ứng mọi tiêu chí G1.

# Cloud Computing — Original và Preprocessed

## 1. Danh tính, nguồn và phạm vi

LEMMA-RCA, Zheng và cộng sự; [paper v4](https://arxiv.org/html/2406.05375v4), [code tác giả](https://github.com/lemma-rca/rca_baselines), [Original](https://huggingface.co/datasets/Lemma-RCA-NEC/Cloud_Computing_Original), [Preprocessed](https://huggingface.co/datasets/Lemma-RCA-NEC/Cloud_Computing_Preprocessed). Revision khóa tại [manifest](runs/source-final-001/manifest.json). Original/Preprocessed chung lineage. License NC/ND chính xác còn OPEN; kiểm nội bộ phi thương mại theo WHY-14 không cấp quyền chia sẻ payload phái sinh. Đã kiểm toàn bộ member hai ZIP metric/log ngày 20240124; các ngày khác và Original chỉ metadata.

## 2. Bảng tiêu chí MRP1–9

| Tiêu chí | Kết quả đúng phạm vi mẫu |
|---|---|
| 1. Công khai/tải/license | Byte/LFS SHA public revision khớp; license cuối OPEN. |
| 2. Root/time | Nhãn và clock theo mục3/5; không suy mốc tiêm thành onset đã kiểm. |
| 3. Trace cha–con | ZIP mẫu không có span table; parent/degree Original OPEN. |
| 4. Metric/log | 16 NPY, 20.792.790 CSV rows; chất lượng kiểm từng file. |
| 5. Root/vị trí | Có mapping entity; không có trace graph để đo bậc root. |
| 6. Nhóm lỗi | API infinite loop gây CPU contention; một scenario chưa phủ mọi nhóm. |
| 7. Triệu chứng ngoài root | Đã có mô tả theo từng kênh/q kèm đối chứng; không nhãn vùng. |
| 8. Normal học ngưỡng | Có timeline 24 h trước lỗi, chưa nhãn healthy. |
| 9. Độc lập | Raw/processed chung lineage; PR/Cloud chưa đủ coi hai bộ độc lập; không census raw reuse xuyên bộ. |

## 3. Nhãn, ca và khả năng phân xử

PPTX xác định AP instance i-078923fb30cac1ede, bug lúc 03:10Z và failure time 03:10:51Z ngày 24/01/2024. Đây là nhãn theo tác giả, không phải onset đã kiểm độc lập. Epoch JSON riêng lệch sáu giờ. Một ngày mẫu không là census root×fault×repetition toàn release. Nguồn có 4 PR/6 Cloud date token; không coi chúng là incident count. Sơ đồ PPTX không thay trace graph. Bậc root và confound vị trí–loại lỗi vẫn OPEN.

## 4. Schema và chất lượng ba nguồn tín hiệu

NPY object dict dùng KPI_* hoặc jaeger_*, Sequence/time và Pod_Name/Node_Name. Log NPY có layout entity×time×feature; CSV structured có LineId, Time, Content, EventId, EventTemplate, ParameterList. Static reader không thực thi pickle. Có 0 nonfinite và 30 constant column occurrences, kể cả KPI/alias; 0 byte không giải được UTF-8 trong 0 CSV; 0 ragged rows. Encoding khác có thể giải thích, chưa gọi file hỏng. Cadence/gap/unit và từng kênh xem summaries; preprocessing có thể che missing raw.

Metric có 15 tên entity; structured log có 15 tên file; giao chính xác 15; log-feature NPY có 15 entity. Ba tập giữ riêng. Root instance có trong cả metric/log. Không cột trace/span ID trong CSV; ID trong payload và khả năng ghép parent chưa có hợp đồng được xác minh. Không suy Original thiếu trace.

## 5. Normal và thời gian

Nguồn ghi 24 h trước bug, nhưng cũng ghi có 502 trước lỗi. Phần này là tham chiếu theo timeline, không có nhãn healthy từng điểm. PPTX có UTCZ nên không dịch chín giờ thêm; không áp quy tắc này để sửa JSON. Cloud PCA log feature kết thúc trước injection. Cadence là FACT file, tách khỏi lịch nguồn. Injection, narrative failure time và recovery là ba loại thông tin khác; không tự sửa clock/nhãn.

## 6. Mô tả thô triệu chứng ngoài root

Đã tính q=.95/.99/.995, độ lệch tuyệt đối so median 12 h tham chiếu,12 h đối chứng và 24 h sau bug. Log CSV dùng event/giờ UTC đầy đủ, bỏ giờ cắt biên; q log chỉ có 11 mẫu mỗi nửa nên thô. Tử/mẫu và zero band từng entity/kênh ở cloud-descriptive-bands.csv; PCA sau lỗi có denominator 0 nên tỷ lệ để trống. Root gắn sau tính, không chọn SLI theo root. Co-occurrence có thể do workload chung, nhiễu, threshold zero hoặc preprocessing. Không OR các kênh, không regex mức lỗi làm nhãn vùng, không kết luận propagation từ vượt band. Đây là mô tả P2, chưa chọn detector hoặc chia dev/test.

## 7. Task nào chấm được?

Ranking root là CANDIDATE theo đúng đơn vị nhãn sau chốt mapping. Cloud có label instance trực tiếp. Time detection cần giao thức và interval nhãn phù hợp, không gọi onset đã verified. Không nhãn vùng/trace thật để chấm segmentation hoặc trace anomaly. Không RCA/baseline/training chạy trong task.

## 8. Rò nhãn, provenance và G1

Không đưa date/PPTX/root vào đầu vào phương pháp. Case-dependent KPI/metric selector code nguồn chưa là adapter an toàn cho chế độ tự phát hiện. 14/14 Sequence KPI case khớp phép tính trung bình CSV theo label/second, không thiếu hoặc khác điểm. Cloud log-feature NPY lưu KPI_Label ratings.book-info... trong khi metric/KPI CSV ghi scenario8_app_request. Chưa xác nhận vì sao metadata này khác; không suy numeric payload thuộc PR. Vector trùng giữ ở summary, không đếm alias thành lặp. Không chia Original/Preprocessed cùng ca sang hai phía. Chưa chọn dataset thí nghiệm.

## 9. Kích thước và chi phí

Hai ZIP mẫu 110.301.798 byte; 1.232.576.188 byte member được stream. Toàn kho Original PR 53.633.808.946byte/Cloud 33.002.132.069byte theo [census](runs/run-001/count-summary.json), chưa tải. Full audit 200,284s, correction 135,206s, bổ sung schema 2,824s tái dùng kết quả; không gọi 2,824s là toàn scan. Xem kiem-file cho RAM/lượt lỗi/interrupt và giới hạn dự báo chi phí.

## 10. OPEN và owner

Tác giả: exact license, JSON/PPTX time và Cloud log-feature KPI_Label. Codex/Minh: nguồn Original/parent, phủ ngày khác, đúng unit ranking; mở rộng cần quyền và byte cụ thể trước làm. Minh: chọn G1/thí nghiệm; Claude review gộp T003. Không xem kiểm một ngày là kiểm toàn release hoặc đáp ứng mọi tiêu chí G1.
