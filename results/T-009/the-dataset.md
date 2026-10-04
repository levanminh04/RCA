# Eadro SocialNetwork — thẻ đã kiểm toàn release đã tải

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT: paper Eadro (2023), Cheryl Lee và cộng sự; Chaosblade; Jaeger, cAdvisor/Prometheus/InfluxDB và Fluentd/Elasticsearch/Kibana theo [nguồn đã lưu](runs/run-001/source_claims.json). [Repository](https://github.com/BEbillionaireUSD/Eadro), [Zenodo](https://zenodo.org/records/7615394). Revision/URL/hash nguồn ở [manifest metadata](runs/run-001/manifest.json); checksum ZIP ở [download](runs/download-001/manifest.json). Giấy phép dữ liệu/code OPEN: nguồn đã lưu không có điều khoản rõ; truy cập công khai và yêu cầu trích dẫn không thay giấy phép.

Q-47 cho đọc số đo bộ này; bộ Bank bảo toàn không bị mở. Đã tải hai ZIP Eadro; biến thể này có 7 phiên raw duy nhất, 11 bản biểu diễn đã đọc. Toàn member lớp ngoài và mọi nested TAR/XZ/GZIP được đọc, CRC ZIP đạt; [inventory](runs/inspect-004/nested-inventory.json) giữ hash từng file. 60 member raw/label nested trùng hash bản ngoài, không cộng thành ca mới. [Kết quả](runs/inspect-004/summary.json), [tính lại độc lập](runs/inspect-004/independent-summary.json). Chạy `py -3 -B results/T-009/scripts/inspect_files.py --data data/ngoai-rcaeval/eadro --out results/T-009/runs/<id-mới>`, rồi `summarize_files.py --run <id>`; không RCA.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | FACT và giới hạn |
|---|---|
| 1. Công khai/giấy phép | ZIP tải/hash/CRC được; điều khoản sử dụng OPEN. |
| 2. Root/thời điểm | 36 nhãn tiêm, 12 root; chỉ injection, không onset thật. |
| 3. Trace cha–con | Raw Jaeger đầy references; trùng bản export và clock là giới hạn có thật. |
| 4. Metric/log | Đọc 84 CSV metric và log mọi phiên raw; nguồn và ID ghép tách mục 4. |
| 5. Root/vị trí | Bậc raw từng root ở mục 3; graph theo injection chưa hợp lệ khi clock chưa rõ. |
| 6. Loại lỗi | CPU load/network delay/network loss; chưa có code fault trong release nhãn. |
| 7. Ngoài root | Đã probe metric ba q, đối chứng riêng; chưa là bằng chứng lan nhân quả. |
| 8. Normal | Có normal riêng và metric thực; warm-up/load cleanliness không được bảo đảm bởi tên. |
| 9. Độc lập | Nhóm tác giả/công cụ/stack có nguồn; cùng Train Ticket hoặc khác tên không đủ quyết độc lập. |

## 3. Nhãn, số ca và khả năng phân xử

FACT: 36 sự kiện, 12 root, 36 ô root×fault; mỗi ô đúng một lần trong release đã tải. Paper công bố 72, giữ cả hai số. Archive “all” trùng raw/label lớp ngoài theo hash nên không cung cấp lần lặp thứ hai. Phiên chứa nhiều sự kiện, không lấy số phiên thay số sự kiện.

| Root | Nhãn fault gốc | Sự kiện |
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

| Root | Phiên chính root (cpu_load) | Bậc vào | Bậc ra | Có trong trace |
|---|---|---|---|---|
| text-service | SN.2022-04-17T181245D2022-04-17T183616 | 1 | 2 | có |
| home-timeline-service | SN.2022-04-17T181245D2022-04-17T183616 | 2 | 2 | có |
| media-service | SN.2022-04-17T181245D2022-04-17T183616 | 1 | 0 | có |
| post-storage-service | SN.2022-04-17T183729D2022-04-17T190100 | 2 | 0 | có |
| social-graph-service | SN.2022-04-17T183729D2022-04-17T190100 | 2 | 1 | có |
| url-shorten-service | SN.2022-04-17T183729D2022-04-17T190100 | 1 | 0 | có |
| nginx-thrift | SN.2022-04-17T190213D2022-04-17T192544 | 0 | 0 | vắng |
| unique-id-service | SN.2022-04-17T190213D2022-04-17T192544 | 1 | 0 | có |
| user-service | SN.2022-04-17T190213D2022-04-17T192544 | 3 | 0 | có |
| compose-post-service | SN.2022-04-17T192658D2022-04-17T195031 | 1 | 7 | có |
| user-timeline-service | SN.2022-04-17T192658D2022-04-17T195031 | 1 | 0 | có |
| user-mention-service | SN.2022-04-17T192658D2022-04-17T195031 | 1 | 0 | có |

Hướng cạnh parent service→child service, bỏ self-edge, union trong toàn file raw sau gộp span trùng nội dung. [Bậc đủ mọi ca/ô](runs/inspect-004/root-degree-whole-file.json). Đây là graph file; không tự gọi graph đúng khoảng tiêm. Root vắng không được gọi cô lập. SN `nginx-thrift`→`nginx-web-server` vẫn là alias CANDIDATE; không dùng thay root đã xác minh.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

FACT toàn 7 phiên raw duy nhất: 1438191 dòng span, 25469 trace-ID cộng theo phiên (không khẳng định ID độc lập liên phiên). Jaeger: traceID/spanID/processes.serviceName/startTime/duration (microsecond theo schema và độ lớn)/tags/references CHILD_OF. Tổng 87853 span không có CHILD_OF; 1350338 reference cần cha. Khóa `(traceID,spanID)` trong phiên: 2909 tìm một dòng cha, 2682 thiếu, 1344747 nhiều dòng. Khi gộp bản span **giống hệt nội dung và service**, 1347656 reference tìm một identity; 0 xung đột. 1189801 dòng trùng khóa; 0 khóa có nội dung xung đột. Hai mẫu số/tỷ lệ không bị trộn. Trùng có thể do export nhiều trace lặp, không tự là mất dữ liệu.

Metric: timestamp epoch giây + bảy cột CPU/memory/rx/tx; 119640 dòng trong 84 CSV, invalid/nonfinite 0, timestamp trùng 0, 0 cặp file×kênh hằng. Delta/cadence/gap riêng từng file ở [raw-sessions](runs/inspect-004/raw-sessions.json); tên rx_bytes không đủ xác định raw byte hay rate, đơn vị/biến đổi nguồn OPEN. Không tự chuẩn hóa/sửa giá trị.

Log JSON map service→list text; 94319 dòng. Không cột trace_id riêng; payload `Span reported` có 0 dòng ID, 0 ghép trace và 0 ghép scoped span. Parser tìm đúng cấu trúc báo span, không coi regex khác là ID. SN phần đã đọc không thấy cấu trúc này; không suy mọi log thiếu ID. Level/timestamp/order theo file được giữ. Clock log chỉ tính UTC **giả định**, không khẳng định timezone nguồn.

## 5. Bình thường và mốc thời gian

Normal nested đã được đọc. SN có ba phiên faults=[]; TT có hai nhãn faults=[] lớp ngoài và thêm raw trong TT-no-fault.txz ngày 20/4 không có label riêng: phần thứ ba là CANDIDATE normal theo tổ chức release. Normal thứ ba này không vào phép probe khi thiếu nhãn riêng. Nhãn start/duration/end là khoảng tiêm, không ground truth onset/recovery.

Trace có timestamp lịch sử và lệch biểu kiến so metric/nhãn/log. Raw SN nhiều span nằm khoảng 8 giờ sau metric; TT cũng có trace từ thời gian trước phiên. [Khoảng thời gian từng nguồn](runs/inspect-004/raw-sessions.json) giữ số gốc; chưa có nguồn xác nhận timezone/cách export. Không dịch 8 giờ để làm graph hoặc claim trace/log đồng bộ. Graph theo injection ở root-positions vì vậy không được diễn giải bậc 0 là cô lập.

## 6. Ước lượng thô triệu chứng ngoài root — tiêu chí 7

FACT mô tả metric: reference là phiên có nhãn no-fault đầu tiên theo session, control là các phiên có nhãn no-fault còn lại; mỗi service×kênh dùng median reference và quantile tuyến tính của độ lệch tuyệt đối, `abs(x-median)>band`; không epsilon, giữ zero-band/missing. Root chỉ gắn sau đo tất cả service/kênh; ba sự kiện `nginx-thrift` không vào tổng ngoài-root do alias chưa xác minh. [Toàn bảng từng ca/kênh/q](runs/inspect-004/symptom-metrics.json) giữ nhãn/ô phục vụ mô tả, không vào phương pháp.

| q | Điểm vượt band ngoài root / điểm hợp lệ | Điểm vượt control / điểm hợp lệ | Cặp ca×kênh ngoài root có band=0 |
|---|---|---|---|
| 0.95 | 81416 / 304920 | 15670 / 242172 | 300 |
| 0.99 | 71126 / 304920 | 7511 / 242172 | 0 |
| 0.995 | 70398 / 304920 | 6472 / 242172 | 0 |

Tổng điểm là phép cộng mô tả, không OR service, không nhãn lan/vùng và không điểm detector. Drift/load, kênh hằng, scale khác giữa phiên hoặc lỗi đo cũng giải thích exceedance. Control được báo để không gọi mọi exceedance là fault. Độ nhạy theo ca/ô còn thấy trong bảng đầy đủ; không kết luận nhân quả từ đồng thời.

## 7. Task chấm được

Ranking root theo service: có nhãn riêng, cần giải quyết alias/clock và giao thức G1; không RCA. Phát hiện thời gian: chỉ injection-regime, onset/end triệu chứng thật không có. Vùng ảnh hưởng: không nhãn tập bị ảnh hưởng; probe không thay nhãn. Không có nhãn bất thường từng trace. Không dùng root label để chọn SLI; chưa chọn ngân sách học/dev/test.

## 8. Rò nhãn, độc lập và G1

Tên file/ca/fault label/mốc tiêm dùng census/chấm, phải loại khỏi đầu vào phương pháp. `align.py` tạo cửa sổ trượt một giây rồi shuffle split, có thể tạo overlap train/test; chưa chứng minh paper dùng chính lệnh đó. Hard-code topology trong util.py khác graph quan sát ở đây. Cùng stack/hệ giữa Eadro và Nezha/RCAEval không tự quyết reuse; hash nested Eadro chỉ chứng minh trùng nội bộ. Chưa chia dev/test hay chọn dataset thay Minh.

## 9. Dung lượng và chi phí

ZIP 78753809 byte; byte/MD5/SHA256 và thời gian tải ở download-001. Inspection streaming toàn hai ZIP trong 168.156 giây; không giải nén payload ra đĩa, không cài môi trường. [Inventory](runs/inspect-004/nested-inventory.json) có byte/hash cuối của từng member; tổng representation có trùng, không là dung lượng ca độc lập. RAM đỉnh chưa đo; runtime parsing không thay chi phí RCA hoặc adapter. [Byte file cuối chính xác](runs/inspect-004/logical-member-sizes.json) tách outer/nested và raw duplicate; không gồm TAR header/padding hoặc intermediate container. Đây là dung lượng logical nếu giải nén hết, không là disk đã ghi.

## 10. OPEN và giới hạn

Giấy phép: tác giả/nguồn điều khoản cần làm rõ trước dùng ngoài inspection. Clock/export trace và alias SN: cần nguồn xác minh, Minh quyết cách dùng; không tự sửa. Bình thường sạch/đại diện tải, onset và nhãn vùng không được release chứng minh. Chọn dataset/split/ngân sách nhãn là G1 của Minh. Đã kiểm toàn file trong release tải và giữ lượt hỏng; các thiếu nhãn/nguồn thật không được gọi đã giải quyết nhờ kiểm metadata.


---

# Eadro Train Ticket — thẻ đã kiểm toàn release đã tải

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT: paper Eadro (2023), Cheryl Lee và cộng sự; Chaosblade; Jaeger, cAdvisor/Prometheus/InfluxDB và Fluentd/Elasticsearch/Kibana theo [nguồn đã lưu](runs/run-001/source_claims.json). [Repository](https://github.com/BEbillionaireUSD/Eadro), [Zenodo](https://zenodo.org/records/7615394). Revision/URL/hash nguồn ở [manifest metadata](runs/run-001/manifest.json); checksum ZIP ở [download](runs/download-001/manifest.json). Giấy phép dữ liệu/code OPEN: nguồn đã lưu không có điều khoản rõ; truy cập công khai và yêu cầu trích dẫn không thay giấy phép.

Q-47 cho đọc số đo bộ này; bộ Bank bảo toàn không bị mở. Đã tải hai ZIP Eadro; biến thể này có 12 phiên raw duy nhất, 21 bản biểu diễn đã đọc. Toàn member lớp ngoài và mọi nested TAR/XZ/GZIP được đọc, CRC ZIP đạt; [inventory](runs/inspect-004/nested-inventory.json) giữ hash từng file. 270 member raw/label nested trùng hash bản ngoài, không cộng thành ca mới. [Kết quả](runs/inspect-004/summary.json), [tính lại độc lập](runs/inspect-004/independent-summary.json). Chạy `py -3 -B results/T-009/scripts/inspect_files.py --data data/ngoai-rcaeval/eadro --out results/T-009/runs/<id-mới>`, rồi `summarize_files.py --run <id>`; không RCA.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | FACT và giới hạn |
|---|---|
| 1. Công khai/giấy phép | ZIP tải/hash/CRC được; điều khoản sử dụng OPEN. |
| 2. Root/thời điểm | 81 nhãn tiêm, 27 root; chỉ injection, không onset thật. |
| 3. Trace cha–con | Raw Jaeger đầy references; trùng bản export và clock là giới hạn có thật. |
| 4. Metric/log | Đọc 324 CSV metric và log mọi phiên raw; nguồn và ID ghép tách mục 4. |
| 5. Root/vị trí | Bậc raw từng root ở mục 3; graph theo injection chưa hợp lệ khi clock chưa rõ. |
| 6. Loại lỗi | CPU load/network delay/network loss; chưa có code fault trong release nhãn. |
| 7. Ngoài root | Đã probe metric ba q, đối chứng riêng; chưa là bằng chứng lan nhân quả. |
| 8. Normal | Có normal riêng và metric thực; warm-up/load cleanliness không được bảo đảm bởi tên. |
| 9. Độc lập | Nhóm tác giả/công cụ/stack có nguồn; cùng Train Ticket hoặc khác tên không đủ quyết độc lập. |

## 3. Nhãn, số ca và khả năng phân xử

FACT: 81 sự kiện, 27 root, 81 ô root×fault; mỗi ô đúng một lần trong release đã tải. Paper công bố 162, giữ cả hai số. Archive “all” trùng raw/label lớp ngoài theo hash nên không cung cấp lần lặp thứ hai. Phiên chứa nhiều sự kiện, không lấy số phiên thay số sự kiện.

| Root | Nhãn fault gốc | Sự kiện |
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

| Root | Phiên chính root (cpu_load) | Bậc vào | Bậc ra | Có trong trace |
|---|---|---|---|---|
| ts-food-service | TT.2022-04-17T212101D2022-04-17T230842 | 0 | 0 | có |
| ts-travel-service | TT.2022-04-17T212101D2022-04-17T230842 | 0 | 3 | có |
| ts-contacts-service | TT.2022-04-17T212101D2022-04-17T230842 | 1 | 0 | có |
| ts-user-service | TT.2022-04-18T102520D2022-04-18T121301 | 0 | 0 | vắng |
| ts-notification-service | TT.2022-04-18T102520D2022-04-18T121301 | 0 | 0 | vắng |
| ts-inside-payment-service | TT.2022-04-18T102520D2022-04-18T121301 | 0 | 0 | vắng |
| ts-route-plan-service | TT.2022-04-18T121515D2022-04-18T140256 | 0 | 0 | vắng |
| ts-assurance-service | TT.2022-04-18T121515D2022-04-18T140256 | 0 | 0 | có |
| ts-price-service | TT.2022-04-18T121515D2022-04-18T140256 | 1 | 0 | có |
| ts-train-service | TT.2022-04-18T150729D2022-04-18T165511 | 2 | 0 | có |
| ts-order-service | TT.2022-04-18T150729D2022-04-18T165511 | 2 | 1 | có |
| ts-cancel-service | TT.2022-04-18T150729D2022-04-18T165511 | 0 | 0 | vắng |
| ts-basic-service | TT.2022-04-18T165807D2022-04-18T184548 | 1 | 4 | có |
| ts-order-other-service | TT.2022-04-18T165807D2022-04-18T184548 | 1 | 0 | có |
| ts-travel-plan-service | TT.2022-04-18T165807D2022-04-18T184548 | 0 | 0 | vắng |
| ts-food-map-service | TT.2022-04-18T184759D2022-04-18T203539 | 0 | 0 | có |
| ts-config-service | TT.2022-04-18T184759D2022-04-18T203539 | 1 | 0 | có |
| ts-security-service | TT.2022-04-18T184759D2022-04-18T203539 | 1 | 2 | có |
| ts-station-service | TT.2022-04-18T203805D2022-04-18T222547 | 2 | 0 | có |
| ts-travel2-service | TT.2022-04-18T203805D2022-04-18T222547 | 0 | 0 | vắng |
| ts-payment-service | TT.2022-04-18T203805D2022-04-18T222547 | 0 | 0 | vắng |
| ts-preserve-service | TT.2022-04-18T222801D2022-04-19T001541 | 0 | 2 | có |
| ts-seat-service | TT.2022-04-18T222801D2022-04-19T001541 | 0 | 0 | vắng |
| ts-verification-code-service | TT.2022-04-18T222801D2022-04-19T001541 | 1 | 0 | có |
| ts-auth-service | TT.2022-04-19T001753D2022-04-19T020534 | 0 | 1 | có |
| ts-route-service | TT.2022-04-19T001753D2022-04-19T020534 | 1 | 0 | có |
| ts-ticketinfo-service | TT.2022-04-19T001753D2022-04-19T020534 | 1 | 1 | có |

Hướng cạnh parent service→child service, bỏ self-edge, union trong toàn file raw sau gộp span trùng nội dung. [Bậc đủ mọi ca/ô](runs/inspect-004/root-degree-whole-file.json). Đây là graph file; không tự gọi graph đúng khoảng tiêm. Root vắng không được gọi cô lập. SN `nginx-thrift`→`nginx-web-server` vẫn là alias CANDIDATE; không dùng thay root đã xác minh.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

FACT toàn 12 phiên raw duy nhất: 290941 dòng span, 11995 trace-ID cộng theo phiên (không khẳng định ID độc lập liên phiên). Jaeger: traceID/spanID/processes.serviceName/startTime/duration (microsecond theo schema và độ lớn)/tags/references CHILD_OF. Tổng 26754 span không có CHILD_OF; 264187 reference cần cha. Khóa `(traceID,spanID)` trong phiên: 1224 tìm một dòng cha, 3196 thiếu, 259767 nhiều dòng. Khi gộp bản span **giống hệt nội dung và service**, 258247 reference tìm một identity; 2744 xung đột. 219347 dòng trùng khóa; 1243 khóa có nội dung xung đột. Hai mẫu số/tỷ lệ không bị trộn. Trùng có thể do export nhiều trace lặp, không tự là mất dữ liệu.

Metric: timestamp epoch giây + bảy cột CPU/memory/rx/tx; 2226690 dòng trong 324 CSV, invalid/nonfinite 0, timestamp trùng 0, 312 cặp file×kênh hằng. Delta/cadence/gap riêng từng file ở [raw-sessions](runs/inspect-004/raw-sessions.json); tên rx_bytes không đủ xác định raw byte hay rate, đơn vị/biến đổi nguồn OPEN. Không tự chuẩn hóa/sửa giá trị.

Log JSON map service→list text; 124571 dòng. Không cột trace_id riêng; payload `Span reported` có 50026 dòng ID, 50009 ghép trace và 49844 ghép scoped span. Parser tìm đúng cấu trúc báo span, không coi regex khác là ID. SN phần đã đọc không thấy cấu trúc này; không suy mọi log thiếu ID. Level/timestamp/order theo file được giữ. Clock log chỉ tính UTC **giả định**, không khẳng định timezone nguồn.

## 5. Bình thường và mốc thời gian

Normal nested đã được đọc. SN có ba phiên faults=[]; TT có hai nhãn faults=[] lớp ngoài và thêm raw trong TT-no-fault.txz ngày 20/4 không có label riêng: phần thứ ba là CANDIDATE normal theo tổ chức release. Normal thứ ba này không vào phép probe khi thiếu nhãn riêng. Nhãn start/duration/end là khoảng tiêm, không ground truth onset/recovery.

Trace có timestamp lịch sử và lệch biểu kiến so metric/nhãn/log. Raw SN nhiều span nằm khoảng 8 giờ sau metric; TT cũng có trace từ thời gian trước phiên. [Khoảng thời gian từng nguồn](runs/inspect-004/raw-sessions.json) giữ số gốc; chưa có nguồn xác nhận timezone/cách export. Không dịch 8 giờ để làm graph hoặc claim trace/log đồng bộ. Graph theo injection ở root-positions vì vậy không được diễn giải bậc 0 là cô lập.

## 6. Ước lượng thô triệu chứng ngoài root — tiêu chí 7

FACT mô tả metric: reference là phiên có nhãn no-fault đầu tiên theo session, control là các phiên có nhãn no-fault còn lại; mỗi service×kênh dùng median reference và quantile tuyến tính của độ lệch tuyệt đối, `abs(x-median)>band`; không epsilon, giữ zero-band/missing. Root chỉ gắn sau đo tất cả service/kênh; ba sự kiện `nginx-thrift` không vào tổng ngoài-root do alias chưa xác minh. [Toàn bảng từng ca/kênh/q](runs/inspect-004/symptom-metrics.json) giữ nhãn/ô phục vụ mô tả, không vào phương pháp.

| q | Điểm vượt band ngoài root / điểm hợp lệ | Điểm vượt control / điểm hợp lệ | Cặp ca×kênh ngoài root có band=0 |
|---|---|---|---|
| 0.95 | 2613952 / 8845200 | 190954 / 1532223 | 3900 |
| 0.99 | 2429732 / 8845200 | 136165 / 1532223 | 2808 |
| 0.995 | 2403967 / 8845200 | 116056 / 1532223 | 2808 |

Tổng điểm là phép cộng mô tả, không OR service, không nhãn lan/vùng và không điểm detector. Drift/load, kênh hằng, scale khác giữa phiên hoặc lỗi đo cũng giải thích exceedance. Control được báo để không gọi mọi exceedance là fault. Độ nhạy theo ca/ô còn thấy trong bảng đầy đủ; không kết luận nhân quả từ đồng thời.

## 7. Task chấm được

Ranking root theo service: có nhãn riêng, cần giải quyết alias/clock và giao thức G1; không RCA. Phát hiện thời gian: chỉ injection-regime, onset/end triệu chứng thật không có. Vùng ảnh hưởng: không nhãn tập bị ảnh hưởng; probe không thay nhãn. Không có nhãn bất thường từng trace. Không dùng root label để chọn SLI; chưa chọn ngân sách học/dev/test.

## 8. Rò nhãn, độc lập và G1

Tên file/ca/fault label/mốc tiêm dùng census/chấm, phải loại khỏi đầu vào phương pháp. `align.py` tạo cửa sổ trượt một giây rồi shuffle split, có thể tạo overlap train/test; chưa chứng minh paper dùng chính lệnh đó. Hard-code topology trong util.py khác graph quan sát ở đây. Cùng stack/hệ giữa Eadro và Nezha/RCAEval không tự quyết reuse; hash nested Eadro chỉ chứng minh trùng nội bộ. Chưa chia dev/test hay chọn dataset thay Minh.

## 9. Dung lượng và chi phí

ZIP 48923113 byte; byte/MD5/SHA256 và thời gian tải ở download-001. Inspection streaming toàn hai ZIP trong 168.156 giây; không giải nén payload ra đĩa, không cài môi trường. [Inventory](runs/inspect-004/nested-inventory.json) có byte/hash cuối của từng member; tổng representation có trùng, không là dung lượng ca độc lập. RAM đỉnh chưa đo; runtime parsing không thay chi phí RCA hoặc adapter. [Byte file cuối chính xác](runs/inspect-004/logical-member-sizes.json) tách outer/nested và raw duplicate; không gồm TAR header/padding hoặc intermediate container. Đây là dung lượng logical nếu giải nén hết, không là disk đã ghi.

## 10. OPEN và giới hạn

Giấy phép: tác giả/nguồn điều khoản cần làm rõ trước dùng ngoài inspection. Clock/export trace và alias SN: cần nguồn xác minh, Minh quyết cách dùng; không tự sửa. Bình thường sạch/đại diện tải, onset và nhãn vùng không được release chứng minh. Chọn dataset/split/ngân sách nhãn là G1 của Minh. Đã kiểm toàn file trong release tải và giữ lượt hỏng; các thiếu nhãn/nguồn thật không được gọi đã giải quyết nhờ kiểm metadata.
