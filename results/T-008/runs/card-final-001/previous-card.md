# Nezha Online Boutique — thẻ giai đoạn metadata

Chưa hoàn tất kiểm dataset. Quyền đọc telemetry và ứng viên giữ ngoài chờ Minh. Các số dưới đây lấy từ `runs/run-001/summary.json`, `cells.json`, `labels.json`; mô tả paper từ `source_claims.json`. Không chọn dataset thay Minh.

## 1. Danh tính, nguồn và phạm vi đã kiểm

Nezha Online Boutique; năm công bố 2023; tác giả: Guangba Yu, Pengfei Chen, Yufeng Li, Hongyang Chen, Xiaoyun Li, Zibin Zheng. Stack: OpenTelemetry SDK/Collector → Tempo; Promtail → Loki; cAdvisor + Istio + Node Exporter → Prometheus. Tiêm lỗi: Code: Java Byteman, Python Hypno, Go Failpoint (refs 4/28/52). CPU/network tool cụ thể OPEN trong đoạn nguồn đã kiểm..

Nguồn: [repo](https://github.com/IntelligentDDS/Nezha); [paper trong repo](sources/FSE2023_Nezha.pdf); [README](sources/README.md); [Zenodo metadata](sources/zenodo.json).

FACT: LICENSE gốc repo là MIT. Metadata artifact Zenodo v0.1 ghi other-open; phạm vi giấy phép riêng dữ liệu và quan hệ revision artifact với GitHub còn OPEN. Không coi hai bản là đồng nhất.

Revision, ngày UTC lấy nguồn, byte, SHA256 và URL chính xác ở [manifest](runs/run-001/manifest.json). Script `scripts/collect_metadata.py --validate-counts --run-id run-001` tính lại offline. Manifest ghi thời gian tải. Script chỉ cho tài liệu/metadata/nhãn riêng. Đã có và đọc telemetry: 0; chưa có quyền đọc ca nào. Nhãn riêng và inventory toàn phạm vi nêu trên đã kiểm. Không coi số sự kiện tiêm là số file.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1. Công khai/giấy phép | Tài liệu và nhãn tải được; giấy phép dữ liệu OPEN như mục 1. |
| 2. Root/thời điểm | Có nhãn thành phần và injection; onset thật OPEN; bất nhất/interval ở mục 5. |
| 3. Parent-linked trace | Code yêu cầu TraceID/SpanID/ParentID; schema file và resolve chưa kiểm. |
| 4. Metric/log | Có tên file trong inventory; chưa kiểm giá trị, chất lượng hoặc mapping. |
| 5. Root/vị trí | 10 root từ nhãn; bậc và vị trí graph OPEN. |
| 6. Loại lỗi | Có tài nguyên, mạng và mã nguồn trong nhãn. Tên lỗi không bảo đảm biểu hiện. |
| 7. Triệu chứng ngoài root | OPEN: không đọc telemetry khi chưa có quyền. |
| 8. Bình thường | README chỉ construct_data là fault-free; độ dài/chất lượng OPEN. |
| 9. Độc lập | Tác giả/công cụ/stack có nguồn; reuse raw và độc lập đủ ba trục OPEN. Cùng hệ hay khác tên không đủ. |

## 3. Nhãn, số ca và khả năng phân xử

FACT nhãn: 56 sự kiện tiêm; 10 root; 5 loại; 33 ô root × loại. Lần lặp theo ô: 10 ô có 1 lần, 23 ô có 2 lần.

Paper ghi 42 resource + 14 code; nhóm từ nhãn khớp.

| Root | Loại lỗi gốc | Số sự kiện |
|---|---|---|
| adservice | cpu_consumed | 1 |
| adservice | cpu_contention | 1 |
| adservice | exception | 2 |
| adservice | network_delay | 1 |
| adservice | return | 2 |
| cartservice | cpu_contention | 2 |
| cartservice | network_delay | 2 |
| checkoutservice | cpu_consumed | 1 |
| checkoutservice | cpu_contention | 1 |
| checkoutservice | exception | 2 |
| checkoutservice | network_delay | 2 |
| checkoutservice | return | 2 |
| currencyservice | cpu_contention | 2 |
| currencyservice | network_delay | 2 |
| emailservice | cpu_consumed | 1 |
| emailservice | cpu_contention | 2 |
| emailservice | network_delay | 2 |
| frontend | cpu_consumed | 2 |
| frontend | cpu_contention | 2 |
| frontend | exception | 2 |
| frontend | return | 2 |
| paymentservice | cpu_contention | 2 |
| paymentservice | network_delay | 2 |
| productcatalogservice | cpu_consumed | 2 |
| productcatalogservice | exception | 1 |
| productcatalogservice | network_delay | 1 |
| productcatalogservice | return | 1 |
| recommendationservice | cpu_consumed | 2 |
| recommendationservice | cpu_contention | 2 |
| recommendationservice | network_delay | 2 |
| shippingservice | cpu_consumed | 1 |
| shippingservice | cpu_contention | 2 |
| shippingservice | network_delay | 2 |

Bảng tính trực tiếp từ nhãn riêng; `summary.json/missing_cross_product` liệt kê ô vắng, không giả định lưới phải đầy. Pod→service bỏ hai hậu tố cuối, cùng cách code `data_integrate.py` làm; các event khớp mapping root_cause. Mapping có thêm service/loại không chứng minh có event.

Bậc vào/ra, root có trong graph ca chính nó, số nút/cạnh và thay đổi topology: OPEN. Chưa đọc trace. Thiếu node sau này có thể do instrumentation hoặc lấy mẫu, không tự gọi cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

FACT code `sources/data_integrate.py` đọc CSV trace: TraceID, SpanID, ParentID, PodName, StartTimeUnixNano, EndTimeUnixNano, OperationName. Code dùng sentinel `root`. Log đọc TimeUnixNano, SpanID, Log; ghép theo SpanID. Đây là schema kỳ vọng của code, chưa phải schema file kiểm thực. Đơn vị từ tên Nano cần đối chiếu giá trị sau quyền đọc. Metric inventory là CSV; code alarm đọc metric theo cấu hình.

Tổng span, parent root/không root, unique-parent numerator/denominator, missing/ambiguous, NaN/gap/constant/duplicate, cadence, clock, entity mapping, log trace_id có giá trị và ghép được: tất cả OPEN vì chưa đọc telemetry. Không báo tỷ lệ từ code hoặc paper.

## 5. Dữ liệu bình thường và mốc thời gian

Nhãn có inject_time text và inject_timestamp epoch; không có trường end. Chênh text (tạm diễn dịch UTC chỉ để đối chiếu) trừ epoch: {'0': 55, '60': 1}; số epoch bị lặp vượt bản ghi đầu: 0. Không tự chọn timezone/correct timestamp. Đây có thể là lệch timezone hoặc nhập nhãn; một timezone duy nhất không giải thích mọi sai khác.
Paper ghi mỗi lần tiêm 180 giây. Không biến số công bố thành end/onset thật từng ca. README phân biệt construct_data với rca_data; độ dài và sạch của normal, biên trước/sau tiêm còn OPEN. Lỗi trước/warm-up/tải có thể làm normal không đại diện.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không đọc telemetry trước câu trả lời Minh về giữ ngoài. Chưa tính ngưỡng, OR hay bất thường ngoài root. Khi được phép, theo SPEC dùng ba q .95/.99/.995, tách normal tham chiếu/đối chứng, kênh/ca/ô. Đồng thời bất thường có thể do tải, drift hoặc lỗi đo; không làm nhãn vùng hoặc bằng chứng nhân quả.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn thực có; giới hạn |
|---|---|
| Ranking root | Nhãn một thành phần/sự kiện; có thể chấm Hit@k/MRR theo mapping đã xác minh. Cần giải quyết time/alias và giao thức; chưa chạy RCA. |
| Phát hiện theo thời gian | Chỉ injection-regime. Thiếu end theo ca, time xung đột cần giải quyết trước. Không gọi Precision/Recall/F1 là phát hiện onset thực. |
| Vùng ảnh hưởng | Không thấy nhãn tập bị ảnh hưởng trong nhãn riêng đã kiểm. Root không thay vùng; không chấm vùng bằng probe. |
| Bất thường từng trace | Không có nhãn trace riêng trong tập nhãn đã đọc; phần chưa đọc OPEN. |

Inner-service labels ánh xạ service×fault→resource type/code region giữa log statements; không phải nhãn từng span hay vùng ảnh hưởng.
Ngân sách nhãn học/dev/chấm, split theo ô, baseline chuyển hệ: G1 còn OPEN; tổng số ca không chứng minh đủ huấn luyện.

## 8. Rò nhãn và thông tin phục vụ G1

Tên file/đường dẫn/nhãn/mốc tiêm chỉ phục vụ census hoặc chấm; không vào phương pháp. Biên file, thứ tự ca, SLI chọn theo root có thể tiết lộ nhãn; chưa đọc telemetry để kiểm biên. Không tự chốt cách cắt/split.
Runner Nezha là nghiên cứu biết mốc: `pattern_ranker.py` đọc fault list. Chưa khẳng định adapter đã chống rò.

Nhóm tác giả Nezha và Eadro khác tên tác giả; stack có thành phần dùng chung Prometheus/cAdvisor, hệ TT cũng dùng chung. Tiêm code Nezha khác Chaosblade Eadro; công cụ resource Nezha chưa đủ nguồn. So với RCAEval phải dùng đủ thẻ T-002 và nguồn, không suy độc lập hoàn toàn từ một yếu tố. Reuse raw/hash giữa release chưa kiểm.

## 9. Kích thước và chi phí

Tổng byte blob telemetry được liệt kê trong proposed_files.json cho OB: 2,677,369,464 byte. Đây là kích thước file GitHub cộng, không archive nén. Zenodo artifact v0.1 có archive riêng (sources/zenodo.json), chưa kiểm tương đương revision.
Lượt metadata hai biến thể tải 4,266,063 byte trong 10.615 giây; telemetry tải 0 byte. RAM/thời gian parser và adapter toàn bộ OPEN; chưa thể ngoại suy từ nhãn nhỏ.

## 10. Những điều còn mở

| OPEN | Đầu vào và người giải quyết | Hệ quả |
|---|---|
| Quyền đọc, ứng viên giữ ngoài | Minh, trước bước telemetry của SPEC | Schema/chất lượng/lan chưa kết luận |
| Giấy phép dữ liệu | Điều khoản release rõ; Minh quyết bước xin nguồn khi cần | Tiêu chí 1 chưa chốt |
| Bất nhất paper/nhãn hoặc clock | Snapshot hiện có, nguồn sửa/giải thích của tác giả; Minh quyết cách dùng | Số ca/giao thức thời gian |
| Parent/metric/log/normal/root position | File trong inspection-plan sau quyền đọc | Tiêu chí 3–5/7/8 và DT18 mapping |
| Độc lập và split/ngân sách nhãn | Bảng đủ ứng viên, G1 do Minh quyết | So sánh RQ1/RQ3 hợp lệ |

Bằng chứng hiện tại đủ mô tả nguồn, kiểm nhãn riêng và trình file cần đọc. Chưa đủ chọn dataset hoặc kết luận độ lan/giá trị đồ thị. Không coi khác biệt số đếm là bằng chứng dataset kém nếu phạm vi release chưa được giải thích.

---

# Nezha Train Ticket — thẻ giai đoạn metadata

Chưa hoàn tất kiểm dataset. Quyền đọc telemetry và ứng viên giữ ngoài chờ Minh. Các số dưới đây lấy từ `runs/run-001/summary.json`, `cells.json`, `labels.json`; mô tả paper từ `source_claims.json`. Không chọn dataset thay Minh.

## 1. Danh tính, nguồn và phạm vi đã kiểm

Nezha Train Ticket; năm công bố 2023; tác giả: Guangba Yu, Pengfei Chen, Yufeng Li, Hongyang Chen, Xiaoyun Li, Zibin Zheng. Stack: OpenTelemetry SDK/Collector → Tempo; Promtail → Loki; cAdvisor + Istio + Node Exporter → Prometheus. Tiêm lỗi: Code: Java Byteman, Python Hypno, Go Failpoint (refs 4/28/52). CPU/network tool cụ thể OPEN trong đoạn nguồn đã kiểm..

Nguồn: [repo](https://github.com/IntelligentDDS/Nezha); [paper trong repo](sources/FSE2023_Nezha.pdf); [README](sources/README.md); [Zenodo metadata](sources/zenodo.json).

FACT: LICENSE gốc repo là MIT. Metadata artifact Zenodo v0.1 ghi other-open; phạm vi giấy phép riêng dữ liệu và quan hệ revision artifact với GitHub còn OPEN. Không coi hai bản là đồng nhất.

Revision, ngày UTC lấy nguồn, byte, SHA256 và URL chính xác ở [manifest](runs/run-001/manifest.json). Script `scripts/collect_metadata.py --validate-counts --run-id run-001` tính lại offline. Manifest ghi thời gian tải. Script chỉ cho tài liệu/metadata/nhãn riêng. Đã có và đọc telemetry: 0; chưa có quyền đọc ca nào. Nhãn riêng và inventory toàn phạm vi nêu trên đã kiểm. Không coi số sự kiện tiêm là số file.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1. Công khai/giấy phép | Tài liệu và nhãn tải được; giấy phép dữ liệu OPEN như mục 1. |
| 2. Root/thời điểm | Có nhãn thành phần và injection; onset thật OPEN; bất nhất/interval ở mục 5. |
| 3. Parent-linked trace | Code yêu cầu TraceID/SpanID/ParentID; schema file và resolve chưa kiểm. |
| 4. Metric/log | Có tên file trong inventory; chưa kiểm giá trị, chất lượng hoặc mapping. |
| 5. Root/vị trí | 10 root từ nhãn; bậc và vị trí graph OPEN. |
| 6. Loại lỗi | Có tài nguyên, mạng và mã nguồn trong nhãn. Tên lỗi không bảo đảm biểu hiện. |
| 7. Triệu chứng ngoài root | OPEN: không đọc telemetry khi chưa có quyền. |
| 8. Bình thường | README chỉ construct_data là fault-free; độ dài/chất lượng OPEN. |
| 9. Độc lập | Tác giả/công cụ/stack có nguồn; reuse raw và độc lập đủ ba trục OPEN. Cùng hệ hay khác tên không đủ. |

## 3. Nhãn, số ca và khả năng phân xử

FACT nhãn: 45 sự kiện tiêm; 10 root; 4 loại; 23 ô root × loại. Lần lặp theo ô: 8 ô có 1 lần, 8 ô có 2 lần, 7 ô có 3 lần.

Paper ghi 20 resource + 25 code; file nhãn có 21 resource + 24 code. Giữ cả hai. Chưa biết do sửa nhãn, phân loại hay revision; không tự sửa.

| Root | Loại lỗi gốc | Số sự kiện |
|---|---|---|
| ts-basic-service | cpu_contention | 1 |
| ts-basic-service | exception | 1 |
| ts-basic-service | network_delay | 2 |
| ts-basic-service | return | 3 |
| ts-contacts-service | cpu_contention | 1 |
| ts-contacts-service | network_delay | 1 |
| ts-contacts-service | return | 3 |
| ts-food-service | cpu_contention | 2 |
| ts-food-service | network_delay | 2 |
| ts-food-service | return | 2 |
| ts-preserve-service | cpu_contention | 1 |
| ts-preserve-service | network_delay | 1 |
| ts-price-service | exception | 3 |
| ts-route-service | exception | 3 |
| ts-route-service | network_delay | 2 |
| ts-security-service | network_delay | 2 |
| ts-travel-service | cpu_contention | 1 |
| ts-travel-service | exception | 3 |
| ts-travel-service | network_delay | 2 |
| ts-travel2-service | exception | 3 |
| ts-verification-code-service | cpu_contention | 1 |
| ts-verification-code-service | network_delay | 2 |
| ts-verification-code-service | return | 3 |

Bảng tính trực tiếp từ nhãn riêng; `summary.json/missing_cross_product` liệt kê ô vắng, không giả định lưới phải đầy. Pod→service bỏ hai hậu tố cuối, cùng cách code `data_integrate.py` làm; các event khớp mapping root_cause. Mapping có thêm service/loại không chứng minh có event.

Bậc vào/ra, root có trong graph ca chính nó, số nút/cạnh và thay đổi topology: OPEN. Chưa đọc trace. Thiếu node sau này có thể do instrumentation hoặc lấy mẫu, không tự gọi cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

FACT code `sources/data_integrate.py` đọc CSV trace: TraceID, SpanID, ParentID, PodName, StartTimeUnixNano, EndTimeUnixNano, OperationName. Code dùng sentinel `root`. Log đọc TimeUnixNano, SpanID, Log; ghép theo SpanID. Đây là schema kỳ vọng của code, chưa phải schema file kiểm thực. Đơn vị từ tên Nano cần đối chiếu giá trị sau quyền đọc. Metric inventory là CSV; code alarm đọc metric theo cấu hình.

Tổng span, parent root/không root, unique-parent numerator/denominator, missing/ambiguous, NaN/gap/constant/duplicate, cadence, clock, entity mapping, log trace_id có giá trị và ghép được: tất cả OPEN vì chưa đọc telemetry. Không báo tỷ lệ từ code hoặc paper.

## 5. Dữ liệu bình thường và mốc thời gian

Nhãn có inject_time text và inject_timestamp epoch; không có trường end. Chênh text (tạm diễn dịch UTC chỉ để đối chiếu) trừ epoch: {'28740': 4, '28800': 15, '28760': 1, '29303': 1, '28710': 1, '28780': 1, '28860': 1, '0': 17, '-60': 1, '60': 3}; số epoch bị lặp vượt bản ghi đầu: 1. Không tự chọn timezone/correct timestamp. Đây có thể là lệch timezone hoặc nhập nhãn; một timezone duy nhất không giải thích mọi sai khác.
Paper ghi mỗi lần tiêm 180 giây. Không biến số công bố thành end/onset thật từng ca. README phân biệt construct_data với rca_data; độ dài và sạch của normal, biên trước/sau tiêm còn OPEN. Lỗi trước/warm-up/tải có thể làm normal không đại diện.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không đọc telemetry trước câu trả lời Minh về giữ ngoài. Chưa tính ngưỡng, OR hay bất thường ngoài root. Khi được phép, theo SPEC dùng ba q .95/.99/.995, tách normal tham chiếu/đối chứng, kênh/ca/ô. Đồng thời bất thường có thể do tải, drift hoặc lỗi đo; không làm nhãn vùng hoặc bằng chứng nhân quả.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn thực có; giới hạn |
|---|---|
| Ranking root | Nhãn một thành phần/sự kiện; có thể chấm Hit@k/MRR theo mapping đã xác minh. Cần giải quyết time/alias và giao thức; chưa chạy RCA. |
| Phát hiện theo thời gian | Chỉ injection-regime. Thiếu end theo ca, time xung đột cần giải quyết trước. Không gọi Precision/Recall/F1 là phát hiện onset thực. |
| Vùng ảnh hưởng | Không thấy nhãn tập bị ảnh hưởng trong nhãn riêng đã kiểm. Root không thay vùng; không chấm vùng bằng probe. |
| Bất thường từng trace | Không có nhãn trace riêng trong tập nhãn đã đọc; phần chưa đọc OPEN. |

Inner-service labels ánh xạ service×fault→resource type/code region giữa log statements; không phải nhãn từng span hay vùng ảnh hưởng.
Ngân sách nhãn học/dev/chấm, split theo ô, baseline chuyển hệ: G1 còn OPEN; tổng số ca không chứng minh đủ huấn luyện.

## 8. Rò nhãn và thông tin phục vụ G1

Tên file/đường dẫn/nhãn/mốc tiêm chỉ phục vụ census hoặc chấm; không vào phương pháp. Biên file, thứ tự ca, SLI chọn theo root có thể tiết lộ nhãn; chưa đọc telemetry để kiểm biên. Không tự chốt cách cắt/split.
Runner Nezha là nghiên cứu biết mốc: `pattern_ranker.py` đọc fault list. Chưa khẳng định adapter đã chống rò.

Nhóm tác giả Nezha và Eadro khác tên tác giả; stack có thành phần dùng chung Prometheus/cAdvisor, hệ TT cũng dùng chung. Tiêm code Nezha khác Chaosblade Eadro; công cụ resource Nezha chưa đủ nguồn. So với RCAEval phải dùng đủ thẻ T-002 và nguồn, không suy độc lập hoàn toàn từ một yếu tố. Reuse raw/hash giữa release chưa kiểm.

## 9. Kích thước và chi phí

Tổng byte blob telemetry được liệt kê trong proposed_files.json cho TT: 360,765,178 byte. Đây là kích thước file GitHub cộng, không archive nén. Zenodo artifact v0.1 có archive riêng (sources/zenodo.json), chưa kiểm tương đương revision.
Lượt metadata hai biến thể tải 4,266,063 byte trong 10.615 giây; telemetry tải 0 byte. RAM/thời gian parser và adapter toàn bộ OPEN; chưa thể ngoại suy từ nhãn nhỏ.

## 10. Những điều còn mở

| OPEN | Đầu vào và người giải quyết | Hệ quả |
|---|---|
| Quyền đọc, ứng viên giữ ngoài | Minh, trước bước telemetry của SPEC | Schema/chất lượng/lan chưa kết luận |
| Giấy phép dữ liệu | Điều khoản release rõ; Minh quyết bước xin nguồn khi cần | Tiêu chí 1 chưa chốt |
| Bất nhất paper/nhãn hoặc clock | Snapshot hiện có, nguồn sửa/giải thích của tác giả; Minh quyết cách dùng | Số ca/giao thức thời gian |
| Parent/metric/log/normal/root position | File trong inspection-plan sau quyền đọc | Tiêu chí 3–5/7/8 và DT18 mapping |
| Độc lập và split/ngân sách nhãn | Bảng đủ ứng viên, G1 do Minh quyết | So sánh RQ1/RQ3 hợp lệ |

Bằng chứng hiện tại đủ mô tả nguồn, kiểm nhãn riêng và trình file cần đọc. Chưa đủ chọn dataset hoặc kết luận độ lan/giá trị đồ thị. Không coi khác biệt số đếm là bằng chứng dataset kém nếu phạm vi release chưa được giải thích.
