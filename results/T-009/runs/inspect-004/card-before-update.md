# Eadro SocialNetwork — thẻ giai đoạn metadata

Chưa hoàn tất kiểm dataset. Quyền đọc telemetry và ứng viên giữ ngoài chờ Minh. Các số dưới đây lấy từ `runs/run-001/summary.json`, `cells.json`, `labels.json`; mô tả paper từ `source_claims.json`. Không chọn dataset thay Minh.

## 1. Danh tính, nguồn và phạm vi đã kiểm

Eadro SocialNetwork; năm công bố 2023; tác giả: Cheryl Lee, Tianyi Yang, Zhuangbin Chen, Yuxin Su, Michael R. Lyu. Stack: Jaeger; cAdvisor + Prometheus → InfluxDB; Fluentd, Elasticsearch, Kibana. Tiêm lỗi: Chaosblade: CPU exhaustion, network jam, packet loss.

Nguồn: [repo](https://github.com/BEbillionaireUSD/Eadro); [paper](https://arxiv.org/html/2302.05092v1); [README](sources/Readme.md); [Zenodo](https://zenodo.org/records/7615394).

OPEN: tree GitHub không có LICENSE; metadata Zenodo không có trường license. Inventory ZIP lớp ngoài không thấy LICENSE/README/COPYING. Mô tả yêu cầu trích dẫn paper chưa xác lập đầy đủ điều khoản dùng dữ liệu.

Revision, ngày UTC lấy nguồn, byte, SHA256 và URL chính xác ở [manifest](runs/run-001/manifest.json). Script `scripts/collect_metadata.py --validate-counts --run-id run-001` tính lại offline. Manifest ghi thời gian tải. Script chỉ cho tài liệu/metadata/nhãn riêng. Đã có và đọc telemetry: 0; chưa có quyền đọc ca nào. Nhãn riêng và inventory toàn phạm vi nêu trên đã kiểm. Không coi số sự kiện tiêm là số file.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1. Công khai/giấy phép | Tài liệu và nhãn tải được; giấy phép dữ liệu OPEN như mục 1. |
| 2. Root/thời điểm | Có nhãn thành phần và injection; onset thật OPEN; bất nhất/interval ở mục 5. |
| 3. Parent-linked trace | Inventory có spans.json; code parsed dùng latency list. Schema raw và parent chưa kiểm. |
| 4. Metric/log | Có tên file trong inventory; chưa kiểm giá trị, chất lượng hoặc mapping. |
| 5. Root/vị trí | 12 root từ nhãn; bậc và vị trí graph OPEN. |
| 6. Loại lỗi | Ba nhãn tài nguyên/mạng; không có nhãn code trong phần đếm. Tên lỗi không bảo đảm biểu hiện. |
| 7. Triệu chứng ngoài root | OPEN: không đọc telemetry khi chưa có quyền. |
| 8. Bình thường | Có no-fault labels; thời lượng metadata ở mục 5; đủ học ngưỡng chưa kiểm. |
| 9. Độc lập | Tác giả/công cụ/stack có nguồn; reuse raw và độc lập đủ ba trục OPEN. Cùng hệ hay khác tên không đủ. |

## 3. Nhãn, số ca và khả năng phân xử

FACT nhãn: 36 sự kiện tiêm; 12 root; 3 loại; 36 ô root × loại. Lần lặp theo ô: 36 ô có 1 lần.

Paper ghi 72 lần tiêm; nhãn lớp ngoài ZIP đếm 36. Chưa chứng minh thiếu toàn release: chỉ thấy ba archive no-fault chưa mở; không thấy SN-all. Cơ chế lệch vẫn OPEN.

| Root | Loại lỗi gốc | Số sự kiện |
|---|---|---|
| compose-post-service | cpu_load | 1 |
| compose-post-service | network_delay | 1 |
| compose-post-service | network_loss | 1 |
| home-timeline-service | cpu_load | 1 |
| home-timeline-service | network_delay | 1 |
| home-timeline-service | network_loss | 1 |
| media-service | cpu_load | 1 |
| media-service | network_delay | 1 |
| media-service | network_loss | 1 |
| nginx-thrift | cpu_load | 1 |
| nginx-thrift | network_delay | 1 |
| nginx-thrift | network_loss | 1 |
| post-storage-service | cpu_load | 1 |
| post-storage-service | network_delay | 1 |
| post-storage-service | network_loss | 1 |
| social-graph-service | cpu_load | 1 |
| social-graph-service | network_delay | 1 |
| social-graph-service | network_loss | 1 |
| text-service | cpu_load | 1 |
| text-service | network_delay | 1 |
| text-service | network_loss | 1 |
| unique-id-service | cpu_load | 1 |
| unique-id-service | network_delay | 1 |
| unique-id-service | network_loss | 1 |
| url-shorten-service | cpu_load | 1 |
| url-shorten-service | network_delay | 1 |
| url-shorten-service | network_loss | 1 |
| user-mention-service | cpu_load | 1 |
| user-mention-service | network_delay | 1 |
| user-mention-service | network_loss | 1 |
| user-service | cpu_load | 1 |
| user-service | network_delay | 1 |
| user-service | network_loss | 1 |
| user-timeline-service | cpu_load | 1 |
| user-timeline-service | network_delay | 1 |
| user-timeline-service | network_loss | 1 |

Bảng tính trực tiếp từ nhãn riêng; `summary.json/missing_cross_product` liệt kê ô vắng, không giả định lưới phải đầy. Container→service bỏ prefix/suffix theo cấu trúc tên; tên gốc giữ trong labels.json. Riêng SN nginx-thrift so code nginx-web-server là alias CANDIDATE chưa kiểm, không tự gộp.

Bậc vào/ra, root có trong graph ca chính nó, số nút/cạnh và thay đổi topology: OPEN. Chưa đọc trace. Thiếu node sau này có thể do instrumentation hoặc lấy mẫu, không tự gọi cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Inventory lớp ngoài có 4 spans.json và 4 logs.json cùng metric CSV. Code `single_process.py` đọc parsed traces theo timestamp→caller/callee→latency list; đó là đầu ra preprocessing, không chứng minh raw thiếu span. `util.py` có topology hard-code; không dùng làm graph quan sát.
Code kỳ vọng metric timestamp và bảy kênh cpu_usage_system, cpu_usage_total, cpu_usage_user, memory_usage, memory_working_set, rx_bytes, tx_bytes. Log parsed có timestamp/service/template. Schema raw, status, ID và đơn vị chưa kiểm.

Tổng span, parent root/không root, unique-parent numerator/denominator, missing/ambiguous, NaN/gap/constant/duplicate, cadence, clock, entity mapping, log trace_id có giá trị và ghép được: tất cả OPEN vì chưa đọc telemetry. Không báo tỷ lệ từ code hoặc paper.

## 5. Dữ liệu bình thường và mốc thời gian

Nhãn sự kiện có start và duration; end_derived=start+duration chỉ là khoảng tiêm suy theo nhãn. Phân bố duration: {'120': 36}. File phiên có start/end, không thay mốc lỗi. 3 file faults=[] cho tổng 4323.837137 giây (1.201066 giờ); nguồn `normal_intervals.json`. Paper công bố 1.2 giờ. Thời lượng nhãn không xác nhận telemetry đủ hoặc sạch.
Nhãn injection-regime khác onset triệu chứng. Mốc khôi phục, lệch clock và độ phủ kênh OPEN; lỗi trước hoặc warm-up vẫn có thể ảnh hưởng.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không đọc telemetry trước câu trả lời Minh về giữ ngoài. Chưa tính ngưỡng, OR hay bất thường ngoài root. Khi được phép, theo SPEC dùng ba q .95/.99/.995, tách normal tham chiếu/đối chứng, kênh/ca/ô. Đồng thời bất thường có thể do tải, drift hoặc lỗi đo; không làm nhãn vùng hoặc bằng chứng nhân quả.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn thực có; giới hạn |
|---|---|
| Ranking root | Nhãn một thành phần/sự kiện; có thể chấm Hit@k/MRR theo mapping đã xác minh. Cần giải quyết time/alias và giao thức; chưa chạy RCA. |
| Phát hiện theo thời gian | Chỉ injection-regime. Có start+duration nhưng chưa có onset thật. Không gọi Precision/Recall/F1 là phát hiện onset thực. |
| Vùng ảnh hưởng | Không thấy nhãn tập bị ảnh hưởng trong nhãn riêng đã kiểm. Root không thay vùng; không chấm vùng bằng probe. |
| Bất thường từng trace | Không có nhãn trace riêng trong tập nhãn đã đọc; phần chưa đọc OPEN. |

Paper detector gán window abnormal khi có injection. File raw có nhãn fault riêng; không dùng nhãn này làm đầu vào phương pháp.
Ngân sách nhãn học/dev/chấm, split theo ô, baseline chuyển hệ: G1 còn OPEN; tổng số ca không chứng minh đủ huấn luyện.

## 8. Rò nhãn và thông tin phục vụ G1

Tên file/đường dẫn/nhãn/mốc tiêm chỉ phục vụ census hoặc chấm; không vào phương pháp. Biên file, thứ tự ca, SLI chọn theo root có thể tiết lộ nhãn; chưa đọc telemetry để kiểm biên. Không tự chốt cách cắt/split.
`align.py` tạo cửa sổ trượt một giây rồi shuffle chia, có nguy cơ cửa sổ chồng lấn giữa train/test. Mô tả code không chứng minh paper dùng đúng lệnh này. Không dùng nguyên split đó thay WHY-04.

Nhóm tác giả Nezha và Eadro khác tên tác giả; stack có thành phần dùng chung Prometheus/cAdvisor, hệ TT cũng dùng chung. Tiêm code Nezha khác Chaosblade Eadro; công cụ resource Nezha chưa đủ nguồn. So với RCAEval phải dùng đủ thẻ T-002 và nguồn, không suy độc lập hoàn toàn từ một yếu tố. Reuse raw/hash giữa release chưa kiểm.

## 9. Kích thước và chi phí

ZIP công khai 78,753,809 byte (sources/zenodo.json). Inventory ngoài có 147 entry, cộng uncompressed size 669,505,265 byte, gồm metadata macOS và nested archives. Không phải full unpack nested và có thể chứa nội dung lặp.
Lượt metadata hai biến thể tải 629,385 byte trong 22.601 giây; telemetry tải 0 byte. RAM/thời gian parser và adapter toàn bộ OPEN; chưa thể ngoại suy từ nhãn nhỏ.

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

# Eadro Train Ticket — thẻ giai đoạn metadata

Chưa hoàn tất kiểm dataset. Quyền đọc telemetry và ứng viên giữ ngoài chờ Minh. Các số dưới đây lấy từ `runs/run-001/summary.json`, `cells.json`, `labels.json`; mô tả paper từ `source_claims.json`. Không chọn dataset thay Minh.

## 1. Danh tính, nguồn và phạm vi đã kiểm

Eadro Train Ticket; năm công bố 2023; tác giả: Cheryl Lee, Tianyi Yang, Zhuangbin Chen, Yuxin Su, Michael R. Lyu. Stack: Jaeger; cAdvisor + Prometheus → InfluxDB; Fluentd, Elasticsearch, Kibana. Tiêm lỗi: Chaosblade: CPU exhaustion, network jam, packet loss.

Nguồn: [repo](https://github.com/BEbillionaireUSD/Eadro); [paper](https://arxiv.org/html/2302.05092v1); [README](sources/Readme.md); [Zenodo](https://zenodo.org/records/7615394).

OPEN: tree GitHub không có LICENSE; metadata Zenodo không có trường license. Inventory ZIP lớp ngoài không thấy LICENSE/README/COPYING. Mô tả yêu cầu trích dẫn paper chưa xác lập đầy đủ điều khoản dùng dữ liệu.

Revision, ngày UTC lấy nguồn, byte, SHA256 và URL chính xác ở [manifest](runs/run-001/manifest.json). Script `scripts/collect_metadata.py --validate-counts --run-id run-001` tính lại offline. Manifest ghi thời gian tải. Script chỉ cho tài liệu/metadata/nhãn riêng. Đã có và đọc telemetry: 0; chưa có quyền đọc ca nào. Nhãn riêng và inventory toàn phạm vi nêu trên đã kiểm. Không coi số sự kiện tiêm là số file.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1. Công khai/giấy phép | Tài liệu và nhãn tải được; giấy phép dữ liệu OPEN như mục 1. |
| 2. Root/thời điểm | Có nhãn thành phần và injection; onset thật OPEN; bất nhất/interval ở mục 5. |
| 3. Parent-linked trace | Inventory có spans.json; code parsed dùng latency list. Schema raw và parent chưa kiểm. |
| 4. Metric/log | Có tên file trong inventory; chưa kiểm giá trị, chất lượng hoặc mapping. |
| 5. Root/vị trí | 27 root từ nhãn; bậc và vị trí graph OPEN. |
| 6. Loại lỗi | Ba nhãn tài nguyên/mạng; không có nhãn code trong phần đếm. Tên lỗi không bảo đảm biểu hiện. |
| 7. Triệu chứng ngoài root | OPEN: không đọc telemetry khi chưa có quyền. |
| 8. Bình thường | Có no-fault labels; thời lượng metadata ở mục 5; đủ học ngưỡng chưa kiểm. |
| 9. Độc lập | Tác giả/công cụ/stack có nguồn; reuse raw và độc lập đủ ba trục OPEN. Cùng hệ hay khác tên không đủ. |

## 3. Nhãn, số ca và khả năng phân xử

FACT nhãn: 81 sự kiện tiêm; 27 root; 3 loại; 81 ô root × loại. Lần lặp theo ô: 81 ô có 1 lần.

Paper ghi 162 lần tiêm; nhãn lớp ngoài ZIP đếm 81. Chưa chứng minh thiếu toàn release: còn TT-all.txz chưa mở.

| Root | Loại lỗi gốc | Số sự kiện |
|---|---|---|
| ts-assurance-service | cpu_load | 1 |
| ts-assurance-service | network_delay | 1 |
| ts-assurance-service | network_loss | 1 |
| ts-auth-service | cpu_load | 1 |
| ts-auth-service | network_delay | 1 |
| ts-auth-service | network_loss | 1 |
| ts-basic-service | cpu_load | 1 |
| ts-basic-service | network_delay | 1 |
| ts-basic-service | network_loss | 1 |
| ts-cancel-service | cpu_load | 1 |
| ts-cancel-service | network_delay | 1 |
| ts-cancel-service | network_loss | 1 |
| ts-config-service | cpu_load | 1 |
| ts-config-service | network_delay | 1 |
| ts-config-service | network_loss | 1 |
| ts-contacts-service | cpu_load | 1 |
| ts-contacts-service | network_delay | 1 |
| ts-contacts-service | network_loss | 1 |
| ts-food-map-service | cpu_load | 1 |
| ts-food-map-service | network_delay | 1 |
| ts-food-map-service | network_loss | 1 |
| ts-food-service | cpu_load | 1 |
| ts-food-service | network_delay | 1 |
| ts-food-service | network_loss | 1 |
| ts-inside-payment-service | cpu_load | 1 |
| ts-inside-payment-service | network_delay | 1 |
| ts-inside-payment-service | network_loss | 1 |
| ts-notification-service | cpu_load | 1 |
| ts-notification-service | network_delay | 1 |
| ts-notification-service | network_loss | 1 |
| ts-order-other-service | cpu_load | 1 |
| ts-order-other-service | network_delay | 1 |
| ts-order-other-service | network_loss | 1 |
| ts-order-service | cpu_load | 1 |
| ts-order-service | network_delay | 1 |
| ts-order-service | network_loss | 1 |
| ts-payment-service | cpu_load | 1 |
| ts-payment-service | network_delay | 1 |
| ts-payment-service | network_loss | 1 |
| ts-preserve-service | cpu_load | 1 |
| ts-preserve-service | network_delay | 1 |
| ts-preserve-service | network_loss | 1 |
| ts-price-service | cpu_load | 1 |
| ts-price-service | network_delay | 1 |
| ts-price-service | network_loss | 1 |
| ts-route-plan-service | cpu_load | 1 |
| ts-route-plan-service | network_delay | 1 |
| ts-route-plan-service | network_loss | 1 |
| ts-route-service | cpu_load | 1 |
| ts-route-service | network_delay | 1 |
| ts-route-service | network_loss | 1 |
| ts-seat-service | cpu_load | 1 |
| ts-seat-service | network_delay | 1 |
| ts-seat-service | network_loss | 1 |
| ts-security-service | cpu_load | 1 |
| ts-security-service | network_delay | 1 |
| ts-security-service | network_loss | 1 |
| ts-station-service | cpu_load | 1 |
| ts-station-service | network_delay | 1 |
| ts-station-service | network_loss | 1 |
| ts-ticketinfo-service | cpu_load | 1 |
| ts-ticketinfo-service | network_delay | 1 |
| ts-ticketinfo-service | network_loss | 1 |
| ts-train-service | cpu_load | 1 |
| ts-train-service | network_delay | 1 |
| ts-train-service | network_loss | 1 |
| ts-travel-plan-service | cpu_load | 1 |
| ts-travel-plan-service | network_delay | 1 |
| ts-travel-plan-service | network_loss | 1 |
| ts-travel-service | cpu_load | 1 |
| ts-travel-service | network_delay | 1 |
| ts-travel-service | network_loss | 1 |
| ts-travel2-service | cpu_load | 1 |
| ts-travel2-service | network_delay | 1 |
| ts-travel2-service | network_loss | 1 |
| ts-user-service | cpu_load | 1 |
| ts-user-service | network_delay | 1 |
| ts-user-service | network_loss | 1 |
| ts-verification-code-service | cpu_load | 1 |
| ts-verification-code-service | network_delay | 1 |
| ts-verification-code-service | network_loss | 1 |

Bảng tính trực tiếp từ nhãn riêng; `summary.json/missing_cross_product` liệt kê ô vắng, không giả định lưới phải đầy. Container→service bỏ prefix/suffix theo cấu trúc tên; tên gốc giữ trong labels.json. Riêng SN nginx-thrift so code nginx-web-server là alias CANDIDATE chưa kiểm, không tự gộp.

Bậc vào/ra, root có trong graph ca chính nó, số nút/cạnh và thay đổi topology: OPEN. Chưa đọc trace. Thiếu node sau này có thể do instrumentation hoặc lấy mẫu, không tự gọi cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Inventory lớp ngoài có 9 spans.json và 9 logs.json cùng metric CSV. Code `single_process.py` đọc parsed traces theo timestamp→caller/callee→latency list; đó là đầu ra preprocessing, không chứng minh raw thiếu span. `util.py` có topology hard-code; không dùng làm graph quan sát.
Code kỳ vọng metric timestamp và bảy kênh cpu_usage_system, cpu_usage_total, cpu_usage_user, memory_usage, memory_working_set, rx_bytes, tx_bytes. Log parsed có timestamp/service/template. Schema raw, status, ID và đơn vị chưa kiểm.

Tổng span, parent root/không root, unique-parent numerator/denominator, missing/ambiguous, NaN/gap/constant/duplicate, cadence, clock, entity mapping, log trace_id có giá trị và ghép được: tất cả OPEN vì chưa đọc telemetry. Không báo tỷ lệ từ code hoặc paper.

## 5. Dữ liệu bình thường và mốc thời gian

Nhãn sự kiện có start và duration; end_derived=start+duration chỉ là khoảng tiêm suy theo nhãn. Phân bố duration: {'600': 81}. File phiên có start/end, không thay mốc lỗi. 2 file faults=[] cho tổng 16213.652802 giây (4.503792 giờ); nguồn `normal_intervals.json`. Paper công bố 7 giờ. Thời lượng nhãn không xác nhận telemetry đủ hoặc sạch.
Nhãn injection-regime khác onset triệu chứng. Mốc khôi phục, lệch clock và độ phủ kênh OPEN; lỗi trước hoặc warm-up vẫn có thể ảnh hưởng.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không đọc telemetry trước câu trả lời Minh về giữ ngoài. Chưa tính ngưỡng, OR hay bất thường ngoài root. Khi được phép, theo SPEC dùng ba q .95/.99/.995, tách normal tham chiếu/đối chứng, kênh/ca/ô. Đồng thời bất thường có thể do tải, drift hoặc lỗi đo; không làm nhãn vùng hoặc bằng chứng nhân quả.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn thực có; giới hạn |
|---|---|
| Ranking root | Nhãn một thành phần/sự kiện; có thể chấm Hit@k/MRR theo mapping đã xác minh. Cần giải quyết time/alias và giao thức; chưa chạy RCA. |
| Phát hiện theo thời gian | Chỉ injection-regime. Có start+duration nhưng chưa có onset thật. Không gọi Precision/Recall/F1 là phát hiện onset thực. |
| Vùng ảnh hưởng | Không thấy nhãn tập bị ảnh hưởng trong nhãn riêng đã kiểm. Root không thay vùng; không chấm vùng bằng probe. |
| Bất thường từng trace | Không có nhãn trace riêng trong tập nhãn đã đọc; phần chưa đọc OPEN. |

Paper detector gán window abnormal khi có injection. File raw có nhãn fault riêng; không dùng nhãn này làm đầu vào phương pháp.
Ngân sách nhãn học/dev/chấm, split theo ô, baseline chuyển hệ: G1 còn OPEN; tổng số ca không chứng minh đủ huấn luyện.

## 8. Rò nhãn và thông tin phục vụ G1

Tên file/đường dẫn/nhãn/mốc tiêm chỉ phục vụ census hoặc chấm; không vào phương pháp. Biên file, thứ tự ca, SLI chọn theo root có thể tiết lộ nhãn; chưa đọc telemetry để kiểm biên. Không tự chốt cách cắt/split.
`align.py` tạo cửa sổ trượt một giây rồi shuffle chia, có nguy cơ cửa sổ chồng lấn giữa train/test. Mô tả code không chứng minh paper dùng đúng lệnh này. Không dùng nguyên split đó thay WHY-04.

Nhóm tác giả Nezha và Eadro khác tên tác giả; stack có thành phần dùng chung Prometheus/cAdvisor, hệ TT cũng dùng chung. Tiêm code Nezha khác Chaosblade Eadro; công cụ resource Nezha chưa đủ nguồn. So với RCAEval phải dùng đủ thẻ T-002 và nguồn, không suy độc lập hoàn toàn từ một yếu tố. Reuse raw/hash giữa release chưa kiểm.

## 9. Kích thước và chi phí

ZIP công khai 48,923,113 byte (sources/zenodo.json). Inventory ngoài có 577 entry, cộng uncompressed size 617,624,509 byte, gồm metadata macOS và nested archives. Không phải full unpack nested và có thể chứa nội dung lặp.
Lượt metadata hai biến thể tải 629,385 byte trong 22.601 giây; telemetry tải 0 byte. RAM/thời gian parser và adapter toàn bộ OPEN; chưa thể ngoại suy từ nhãn nhỏ.

## 10. Những điều còn mở

| OPEN | Đầu vào và người giải quyết | Hệ quả |
|---|---|
| Quyền đọc, ứng viên giữ ngoài | Minh, trước bước telemetry của SPEC | Schema/chất lượng/lan chưa kết luận |
| Giấy phép dữ liệu | Điều khoản release rõ; Minh quyết bước xin nguồn khi cần | Tiêu chí 1 chưa chốt |
| Bất nhất paper/nhãn hoặc clock | Snapshot hiện có, nguồn sửa/giải thích của tác giả; Minh quyết cách dùng | Số ca/giao thức thời gian |
| Parent/metric/log/normal/root position | File trong inspection-plan sau quyền đọc | Tiêu chí 3–5/7/8 và DT18 mapping |
| Độc lập và split/ngân sách nhãn | Bảng đủ ứng viên, G1 do Minh quyết | So sánh RQ1/RQ3 hợp lệ |

Bằng chứng hiện tại đủ mô tả nguồn, kiểm nhãn riêng và trình file cần đọc. Chưa đủ chọn dataset hoặc kết luận độ lan/giá trị đồ thị. Không coi khác biệt số đếm là bằng chứng dataset kém nếu phạm vi release chưa được giải thích.
