# Thẻ dataset họ RCAEval — T-002

Kiểm dữ liệu ngày 02/10/2026; bổ sung diễn giải R1–R5 ngày 04/10 sau phản biện và Minh duyệt. Mục đích: cung cấp bằng chứng cho tiêu chí MRP §4/P2, phục vụ RQ1/RQ3 và G1. Đây là thẻ mô tả, chưa chọn dataset hoặc cách chia. Bốn bộ cùng tác giả/công cụ/stack không đáp ứng riêng tiêu chí bộ độc lập. Chỉ so với ứng viên khác khi có đủ thẻ, theo Q-31.

**USER_CONFIRMED:** SPEC cho phép kiểm 30 ca dev RE2-TT và 5 ca mẫu đang có. Đã kiểm schema cả 35 ca; khảo sát metric của 32 ca thuộc bốn bộ mục tiêu. Không mở dữ liệu khóa. Không chạy phương pháp RCA. Không thêm quyết định **DECIDED**.

## Căn cứ chung và cách đọc

- [Mẫu thẻ dùng chung](mau-the-dataset.md). Các mục 1–10 dưới mỗi bộ theo đúng mẫu; bảng khả năng chấm và phép tính chung ở cuối được áp dụng cho từng thẻ. FACT từ metadata chỉ xác nhận tên/file/số byte; FACT từ telemetry chỉ áp dụng phần đã kiểm. OPEN ghi đầu vào/người cần giải quyết. CANDIDATE không phải quyết định.

- [Nguồn công khai](public-sources.md), [số đếm toàn kho](public-metadata/run-002/count-summary.json), [từng ô nhãn](public-metadata/run-002/root-fault-cells.csv). Snapshot README, LICENSE, bài v2 và tree nằm trong thư mục nguồn của lượt đó; URL/revision/hash nằm trong [manifest nguồn](public-metadata/run-002/source-manifest.json).

- [Số đo tổng hợp cục bộ](local-inspection/run-002/summary.json), [từng ca và đồ thị](local-inspection/run-002/cases.json), [schema từng file](local-inspection/run-002/schemas.json), [danh sách file đã đọc](local-inspection/run-002/manifest.json). [Script kiểm](inspect_local.py) và [script tổng hợp](summarize_local.py) giữ số trung gian; lệnh tái lập ở LOG.

- FACT nguồn: giấy phép dữ liệu được HF và README tác giả khai báo MIT. README nói dữ liệu/code do tác giả cung cấp dùng MIT. File LICENSE nêu điều kiện giữ thông báo bản quyền. Trạng thái truy cập được kiểm qua metadata và các mẫu có sẵn; chưa tải lại toàn kho.

- FACT nguồn: RE2 dùng stress-ng cho cpu/mem/disk/socket và tc cho delay/loss. RE3 sửa mã nguồn: f1 sai giá trị tham số; f2 thiếu tham số; f3 thiếu lời gọi hàm; f4 sai giá trị trả về; f5 thiếu xử lý ngoại lệ. Thu thập trên Kubernetes bằng Prometheus/cAdvisor/Istio, Jaeger và Vector/Loki/Elasticsearch. Bài mô tả tải ngẫu nhiên 10–200 requests/s. Nguồn: bài v2 §3.1–3.3 trong snapshot đã lưu. Tên lỗi không chứng minh lỗi biểu hiện ở mọi tín hiệu.

- Mốc nhãn là Unix timestamp lúc tiêm, không phải onset (lúc bắt đầu biểu hiện) độc lập. Bài v2 §3 nói mỗi ca có service gốc và root cause indicator (chỉ báo nguyên nhân gốc); §3.2 mô tả chỉ báo metric/log/response code theo loại lỗi. Tuy nhiên tree đã lưu chỉ có 8 `root_cause.txt`, đều ở RE3-SS; bốn bộ mục tiêu không có file tên này. Chưa xác minh nhãn chỉ báo chi tiết trong hình thức khác, chưa có nhãn vùng ảnh hưởng, operation gốc hoặc từng trace bất thường ở nguồn đã đọc. Không suy từ tên fault thành ground truth mới. Đối chiếu lời nguồn và artifact ở [public-sources.md](public-sources.md); các giới hạn chấm ở bảng cuối.

- **FACT trên mẫu:** 32/32 ca mục tiêu có injection đúng giữa timestamp metric đầu/cuối. Biên trace của 32 ca lệch biên metric dưới 1 giây; log của 31 ca lệch tối đa 2 giây. Nguồn: cases.json. Đây là biên hàng quan sát, chưa chứng minh cơ chế exporter cắt cả ba nguồn. Bỏ `inject_time.txt` vẫn chưa loại nguy cơ suy injection từ biên file; chưa có bộ phát hiện nào trong task bị chứng minh khai thác đường này. Phần chưa đọc, gồm RE3-OB, còn OPEN.

## RE2-TT

### 1. Danh tính, nguồn và phạm vi đã kiểm

**FACT:** Train Ticket, họ RCAEval của Pham et al.; nguồn và giấy phép MIT áp dụng theo mục chung. Toàn kho có 90 ca theo directory tại revision trong manifest. Telemetry đã kiểm 30/90 ca: 30 ca dev, 10 ô × 3 lần lặp; không mở 60 ca khóa. Các ca còn lại chỉ đếm metadata file công khai, không đọc dữ liệu đo. Ngày kiểm: 02/10/2026.

### 2. Bảng tiêu chí 1–9

| Tiêu chí | Kết quả/trạng thái | Giới hạn/giải thích khác |
|---|---|---|
| 1 | FACT: công khai, MIT; metadata truy cập được | Nguồn chung; chưa tải/kiểm toàn bộ file |
| 2 | FACT nguồn: service gốc, fault, repeat và lúc tiêm | Onset/end/affected-region chưa có; tiêm chưa chắc gây triệu chứng ngay |
| 3 | FACT trên 30 ca: có traceID/spanID/parentSpanID; resolve 99,10% | Mất cha có thể do lấy mẫu/cắt cửa sổ/instrumentation; không suy topology đầy đủ |
| 4 | FACT trên 30 ca: metric có; log 29/30; không có cột trace ID | File có mặt chưa bảo đảm nội dung; log có thể chỉ nối được service + thời gian |
| 5 | FACT: 5 service gốc; vị trí ở mục 3 | Danh tính service, vị trí và loại lỗi có thể confound (lẫn tác động) |
| 6 | FACT nguồn: tài nguyên + mạng; không có lỗi mã nguồn trong bộ | Một bộ riêng không đủ ba nhóm; loại lỗi không bảo đảm có cùng mức triệu chứng |
| 7 | FACT khảo sát: số vượt ngưỡng theo ba phân vị ở mục 6 | OR nhiều kênh và mem có thể chiếm phần lớn mức vượt; tùy bộ/ngưỡng. Tiêu chí lan truyền nhân quả vẫn chưa xác lập |
| 8 | FACT: 720–720 điểm 1 giây trước tiêm; đủ cho khảo sát này, chưa khẳng định đủ học phương pháp | Trước tiêm chưa chắc sạch/đại diện; warm-up và drift có thể làm ngưỡng lệch |
| 9 | FACT phả hệ: cùng nhóm RCAEval/công cụ/stack | OPEN về bộ dataset chọn; cần ứng viên độc lập của T-003/G1 |

### 3. Nhãn, số ca và khả năng phân xử

**FACT metadata:** 5 service gốc, 6 loại lỗi, 30/30 ô gốc × lỗi có ca; 3–3 lần lặp/ô. Nguồn: count-summary và root-fault-cells ở mục chung. Không coi ô thiếu là ca thất bại.

| Service gốc | Số ca công khai |
|---|---|
| ts-auth-service | 18 |
| ts-order-service | 18 |
| ts-route-service | 18 |
| ts-train-service | 18 |
| ts-travel-service | 18 |

Loại lỗi / số ca: `cpu`: 15; `delay`: 15; `disk`: 15; `loss`: 15; `mem`: 15; `socket`: 15.

| Service gốc | Bậc (vào, ra) trong trace trước tiêm |
|---|---|
| ts-auth-service | (0, 0) ở 30/30 ca |
| ts-order-service | (1, 1) ở 6/30 ca; (5, 1) ở 24/30 ca |
| ts-route-service | (2, 0) ở 6/30 ca; (3, 0) ở 24/30 ca |
| ts-train-service | (2, 0) ở 6/30 ca; (3, 0) ở 24/30 ca |
| ts-travel-service | (2, 3) ở 6/30 ca; (4, 5) ở 24/30 ca |

Cạnh là parent-service → child-service khác tên, resolve bằng (traceID, spanID) trong cùng ca. Bậc là số hàng xóm phân biệt, chưa phải quan hệ có kiểu hay nhân quả. Cửa sổ trước tiêm lọc theo start của child; parent được tra trong cùng file. Không đặt ngưỡng hub. Một node không có cạnh quan sát có thể do thiếu instrumentation hoặc workload không gọi nó.

FACT: đồ thị toàn cửa sổ có 3 cấu trúc: 27 nút/55 cạnh ở 24/30 ca; 20 nút/20 cạnh ở 5/30 ca; 21 nút/21 cạnh ở 1/30 ca. Đồ thị trước tiêm của từng ca có cùng tập nút/cạnh với toàn cửa sổ (đối chiếu cases.json). Có thể cấu trúc ổn định thật, hoặc workload/độ phủ đo giới hạn cấu trúc quan sát; chưa khái quát toàn bộ hệ.

Bảng bậc phía trên theo dõi mỗi service trên cả 30 ca, kể cả khi nó không phải root. Bảng sau chỉ lấy các ca chính service đó là root; mẫu số riêng cho từng root. Nguồn: cases.json, graph pre_injection. Đây là hai phạm vi khác nhau, không thay định nghĩa hub hoặc cách chia.

| Service gốc | Bậc (vào, ra) trong chính ca làm root |
|---|---|
| ts-auth-service | (0, 0) ở 6/6 ca |
| ts-order-service | (1, 1) ở 4/6 ca; (5, 1) ở 2/6 ca |
| ts-route-service | (3, 0) ở 6/6 ca |
| ts-train-service | (3, 0) ở 6/6 ca |
| ts-travel-service | (2, 3) ở 2/6 ca; (4, 5) ở 4/6 ca |

Các graph nhỏ trước tiêm dưới đây được so với hợp tập node quan sát của dev, không phải kiến trúc đầy đủ. Nguồn: cases.json.

| Ca | Nút/cạnh | Node vắng | Tên node vắng so với graph 27 nút |
|---|---|---|---|
| re2tt_ts-order-service_disk_2 | 20/20 | 7 | ts-contacts-service, ts-payment-service, ts-preserve-other-service, ts-preserve-service, ts-seat-service, ts-security-service, ts-user-service |
| re2tt_ts-order-service_disk_3 | 20/20 | 7 | ts-contacts-service, ts-payment-service, ts-preserve-other-service, ts-preserve-service, ts-seat-service, ts-security-service, ts-user-service |
| re2tt_ts-order-service_loss_2 | 20/20 | 7 | ts-contacts-service, ts-payment-service, ts-preserve-other-service, ts-preserve-service, ts-seat-service, ts-security-service, ts-user-service |
| re2tt_ts-order-service_loss_3 | 20/20 | 7 | ts-contacts-service, ts-payment-service, ts-preserve-other-service, ts-preserve-service, ts-seat-service, ts-security-service, ts-user-service |
| re2tt_ts-travel-service_disk_2 | 21/21 | 6 | ts-contacts-service, ts-preserve-other-service, ts-preserve-service, ts-seat-service, ts-security-service, ts-user-service |
| re2tt_ts-travel-service_disk_3 | 20/20 | 7 | ts-contacts-service, ts-payment-service, ts-preserve-other-service, ts-preserve-service, ts-seat-service, ts-security-service, ts-user-service |

**FACT đã kiểm giới hạn:** đọc lại metric trước tiêm của order×disk lặp 1/2 và travel×disk lặp 1/3 cho thấy số workload khác nhau. Các cột preserve/preserve-other/seat/security/user/contacts vắng ở order×disk lặp 2, có nhưng bằng 0 ở travel×disk lặp 3; payment_workload cũng bằng 0 trong hai ca nhỏ này. Nguồn raw: `data/rcaeval/re2tt_ts-order-service_disk_{1,2}/metrics.parquet` và `data/rcaeval/re2tt_ts-travel-service_disk_{1,3}/metrics.parquet`; phép kiểm và số trung gian ở [LOG phiên tự soát 03/10](../../tasks/T-002-the-dataset-rcaeval/LOG.md). Các ca nhỏ khác chưa được đối chiếu raw workload trong phần này; không suy kết quả hai ca nhỏ sang cả sáu ca. **CANDIDATE — chưa kiểm nguyên nhân:** luồng đặt vé có thể ít được gọi; cũng có thể exporter, bộ đo hoặc cách tạo tải làm thiếu/zero cột. Số đo trước tiêm không chứng minh đồ thị nhỏ do lỗi được tiêm; task mô tả không có kiểm soát workload/instrumentation để phân xử.

K2 §2/ST3 cũ ghi 2 đồ thị (24 + 6 ca). Phép dựng literal ở đây cho 3 (24 + 5 + 1): `re2tt_ts-travel-service_disk_2` có thêm `ts-payment-service` và cạnh `ts-inside-payment-service → ts-payment-service` so với cấu trúc 20 nút/20 cạnh. K2 chưa được kiểm lại; khác biệt có thể do phép lọc/vocabulary của audit trước hoặc đếm cũ sai. Không đủ căn cứ xác định lý do từ tài liệu hiện có; không đọc archive và không sửa K2 trong task này.

### 4. Schema thật và chất lượng ba nguồn tín hiệu

**FACT trên mẫu:** metric dạng wide (mỗi chỉ báo một cột), 340–375 cột ngoài `time`, bước 1 giây, 101.118 ô thiếu, 0 timestamp trùng. Tên cột `<entity>_<metric>`; có thành phần hạ tầng, không đồng nhất số cột với số service. Đơn vị từng metric chưa kiểm toàn bộ; xem schema và case-summary.

Trace có 11 trường: `time`, `traceID`, `spanID`, `serviceName`, `methodName`, `operationName`, `parentSpanID`, `startTimeMillis`, `startTime`, `duration`, `statusCode`. Kiểu từng file ở schemas.json. `startTime // 1000 == startTimeMillis` trên phần đã kiểm; quy đổi startTimeMillis/1000 khớp epoch metric/log. Đơn vị duration còn OPEN; không dùng duration để xếp hạng. Không có span kind hay thuộc tính resource/db/messaging đủ dựng cạnh có kiểu.

| Phép đếm trace | Số đo trên mẫu |
|---|---|
| Tổng span | 22.834.238 |
| Không có parent/root | 194.449 |
| Có parent cần resolve | 22.639.789 |
| Tìm được key cha cùng trace | 22.437.039 |
| Không tìm được cha | 202.750 |
| Tỷ lệ cộng số đếm | 99,10% |
| Min–max tỷ lệ theo ca | 82,66%–100,00% |
| Hàng trùng (traceID,spanID) / key khác service | 0 / 0 |
| Duration thiếu / âm | 0 / 0 |
| Status có giá trị / khác 0 | 0 / 0 |

Log: 29/30 ca, 6.554.154 hàng; ba cột `timestamp` (int64), `container_name`, `message` (string). Không có cột trace/span ID; quét tất cả message: 0 nhắc khóa traceid/spanid/traceparent, 0 chuỗi ID hợp regex. Regex không bắt mọi định dạng hoặc ID không có khóa; ghép request-level còn OPEN. Nối service + thời gian là CANDIDATE, cần alias/clock hợp lệ, không phải nối từng request.

Parent resolve chỉ cho biết cha có trong artifact, không chứng minh sampling đầy đủ hay nhân quả. Status thiếu có thể do xuất/lược trường; duration không âm không chứng minh đơn vị đúng. Metric NaN có thể do không có request hoặc bộ đo thiếu; log không có ID có thể là thiết kế exporter, chưa chứng minh không có liên kết ở hệ gốc.

Ca `re2tt_ts-auth-service_delay_1` có tỷ lệ cha thấp nhất 82,66%; giữ ca này. Status rỗng toàn bộ phần dev. 99,10% ở đây là 30 ca dev; không đối chiếu như tái lập 98,45% của audit 90 ca trong K2. Khác tỷ lệ có thể do phạm vi ca khác nhau.

### 5. Dữ liệu bình thường và mốc thời gian

**FACT:** 720–720 hàng metric 1 giây trước lúc tiêm, tương đương 12–12 phút theo số điểm; sau tiêm 721–721 hàng. Bài nói thu bình thường 10 phút; file mẫu dài hơn. Cửa sổ lưu/export có thể khác giao thức mô tả. Mốc tiêm dùng để mô tả hai chế độ, không làm đầu vào bộ tự phát hiện. Trước tiêm chưa có kiểm chứng độc lập rằng mọi điểm sạch; clock và healthy workloads đa chế độ còn OPEN. Không gọi khoảng injection − timestamp đầu tiên là thời lượng đo nếu dữ liệu thưa hoặc injection nằm ngoài file.

**FACT trên 30 ca đã đọc:** biên metric so với injection là −720/+720 giây; điểm giữa hai timestamp đầu/cuối cho lại mốc tiêm. Đây là rò thông tin về injection có thể xảy ra qua chính telemetry, dù bỏ tên ca/file nhãn; injection chưa là onset thật. Giao thức tự phát hiện P3/P7 cần xử lý nguy cơ này trước khi chấm. Task này chưa chọn cách cắt mới hoặc kiểm một detector khai thác vị trí giữa file; biết trước mốc để khảo sát/RCA phải ghi rõ chế độ.

### 6. Ước lượng thô triệu chứng ngoài service gốc

| Phân vị q | Kênh | Ca | Đối chứng trước tiêm | Sau tiêm | Chênh min–max từng ca (điểm %) |
|---|---|---|---|---|---|
| 0.95 | Tất cả metric | 30 | 48,22% | 76,38% | 9,10 đến 42,54 |
| 0.95 | Latency p90 | 30 | 9,29% | 23,33% | 0,06 đến 41,92 |
| 0.99 | Tất cả metric | 30 | 34,80% | 68,18% | 14,67 đến 54,27 |
| 0.99 | Latency p90 | 30 | 5,72% | 19,57% | -0,67 đến 39,94 |
| 0.995 | Tất cả metric | 30 | 33,70% | 67,59% | 14,08 đến 57,46 |
| 0.995 | Latency p90 | 30 | 5,36% | 19,10% | -0,67 đến 39,64 |

Mỗi ô tỷ lệ là trung bình không trọng số: trước hết tỷ lệ hàng thời gian vượt band ở từng service ngoài root, rồi trung bình các service, rồi các ca. Không phải tỷ lệ ca lan hoặc tỷ lệ request lỗi. Công thức, các giới hạn và mapping chỉ để báo ở mục chung cuối. [Từng ca/ngưỡng](local-inspection/run-002/probe-case-summary.csv), [từng ô/ngưỡng](local-inspection/run-002/probe-cell-summary.csv), [từng service](local-inspection/run-002/symptom-entity-rates.csv), [band từng kênh](local-inspection/run-002/symptom-channel-bands.csv).

**CANDIDATE — chưa kiểm:** có tín hiệu ngoài root tăng sau tiêm, có thể chứa triệu chứng lan. Cũng có thể tải chung/drift/nhiễu, thay đổi metric hằng hoặc nhiều kênh OR giải thích nó. Không xác lập causal propagation, không gắn nhãn lan từng ca. Không thấy lệch metric cũng chưa loại trừ biểu hiện ở log/trace.

Phân rã kênh mem dưới đây dùng cùng service ngoài root và cách trung bình như bảng OR; lấy số vượt/số hợp lệ từ symptom-channel-bands.csv. Trên mẫu đã kiểm, mem và OR có cùng mẫu số hàng hợp lệ ở từng service/ca/ngưỡng. Đây là mức vượt của mem, không phải đóng góp độc lập khi bỏ mem khỏi OR.

| Phân vị q | Mem đối chứng | Mem sau tiêm | OR đối chứng | OR sau tiêm |
|---|---|---|---|---|
| 0.95 | 36,28% | 66,11% | 48,22% | 76,38% |
| 0.99 | 27,84% | 57,80% | 34,80% | 68,18% |
| 0.995 | 27,43% | 57,55% | 33,70% | 67,59% |

**OPEN — chưa phân xử nguyên nhân:** mem tăng có thể do tải, warm-up, drift, thay đổi mức nền hoặc lỗi thật; mem lớn không tự chứng minh lan hoặc drift. CSV chỉ lưu số biên từng kênh, không có giao các hàng vượt giữa kênh, nên chưa tính được OR khi bỏ mem. Chưa có đo kiểm soát tải/nhãn vùng độc lập trong task mô tả để phân xử. Không bỏ mem hoặc đổi q chỉ để giảm tỷ lệ; việc đó có thể bỏ biểu hiện mem fault thật.

Cùng phạm vi OR ngoài root tại q=.995, cận tỷ lệ OR của riêng các kênh band0 là 0,33%–0,42% ở đối chứng và 1,03%–1,27% sau tiêm. Cận dưới lấy max số vượt từng kênh band0; cận trên lấy min(tổng số vượt band0, số vượt OR), chia mẫu số OR rồi trung bình service/ca. Nguồn: hai CSV bands/rates ở trên. Chưa có giao kênh để gọi đây là OR chính xác; không dùng tỷ lệ mọi kênh band0 với mẫu số khác để giải thích mức OR. Mem chiếm phần lớn mức vượt ở q=.995 trên RE2-TT; không khái quát sang mọi bộ/ngưỡng.

Không đọc nhóm 60 ca khóa. Trong dev có chênh latency p90 âm ở một số ca khi q cao (xem cột min–max); không biến mức tăng trung bình thành mẫu hình của mọi ô. Ba lần lặp/ô không phải ba topology độc lập.

### 7. Task nào chấm được?

Áp dụng bảng nhãn chung cuối tài liệu: xếp hạng root-service theo ca có nhãn; phát hiện chỉ chấm theo injection-regime với giới hạn; vùng ảnh hưởng/operation/từng trace chưa chấm trực tiếp được. Với bộ chưa kiểm schema, khả năng thực thi adapter còn OPEN. Không lấy khảo sát mục 6 làm nhãn chuẩn.

### 8. Rò nhãn và thông tin phục vụ G1

Tên thư mục chứa root/fault/repeat; inject_time là nhãn biên. Biên file telemetry cũng có thể tiết lộ injection, như các ca có mẫu ở mục 5; phần chưa đọc còn OPEN. Chỉ bỏ file nhãn/tên ca chưa đủ loại đường rò này. Chỉ dùng nhãn cho đếm/mô tả/chấm. `metric_excursions` nhận bảng metric và mốc biên, không nhận root/fault/path; root được gắn sau để báo ngoài root. Đây là khảo sát known-window (biết trước mốc), không phải tự phát hiện. Adapter P3 và giao thức tự phát hiện cần kiểm đường biên file; chưa được làm/kiểm trong task mô tả. Rò SLI của runner chính thức được MRP P2 nêu, chưa khẳng định đã sửa. Dataset/cách chia/nhãn học còn OPEN ở G1; WHY-04 là đề xuất.

### 9. Kích thước và chi phí

**FACT metadata:** 1.965.747.924 byte (1965.748 MB thập phân) trong các thư mục ca công khai, gồm parquet và inject_time; không phải RAM hoặc ZIP giải nén. **FACT phần đã kiểm:** 656.358.942 byte telemetry parquet. Chi phí adapter và RAM cực đại **OPEN — chưa đo**; không suy từ file nhỏ rằng huấn luyện toàn bộ chạy được. Cài gói dưới 1 GB, không tải telemetry mới; thời gian/phiên bản nằm trong manifest và install.log, chi phí riêng không cộng vào khả năng phân xử.

### 10. Điều còn mở

- Onset/end, nhãn vùng và clock độc lập: cần nguồn nhãn bổ sung hoặc thực nghiệm có nhãn thật; người làm task tương ứng báo Minh trước khi dùng cho P7.

- Độ đại diện schema/topology/log và tiêu chí 7 của phần chưa đọc: chỉ 30/90 ca được kiểm. Người làm P2/task tiếp theo cần mẫu được phép; không mở dữ liệu khóa. Nút ít/thiếu có thể do workload hoặc đo thiếu.

- Tính đủ dữ liệu bình thường, phép chia/nhãn học và bộ độc lập: Minh quyết ở G1 sau các thẻ ứng viên; chưa kết luận từ kích thước hoặc dữ liệu sẵn có.

- Cạnh có kiểu, duration unit, alias và khả năng huấn luyện/chuyển hệ: cần xác minh exporter/adapter và giao thức của phương pháp ở task sau. Không biến OPEN thành lỗi dataset hoặc quyết định loại dataset.

- Cơ chế tạo sáu graph nhỏ và khác biệt bậc root: workload mới đối chiếu trên bốn ca disk, chưa là giải thích cho mọi ca. Muốn dùng vị trí để kết luận RQ1, task đo cần phân biệt danh tính root, loại lỗi, tải và độ phủ đo; T-002 chỉ mô tả bậc và số thiếu, không chốt hub hay chia lại dữ liệu.

## RE2-OB

### 1. Danh tính, nguồn và phạm vi đã kiểm

**FACT:** Online Boutique, họ RCAEval của Pham et al.; nguồn và giấy phép MIT áp dụng theo mục chung. Toàn kho có 90 ca theo directory tại revision trong manifest. Telemetry đã kiểm 1/90 ca: re2ob_productcatalogservice_loss_1. Các ca còn lại chỉ đếm metadata file công khai, không đọc dữ liệu đo. Ngày kiểm: 02/10/2026.

### 2. Bảng tiêu chí 1–9

| Tiêu chí | Kết quả/trạng thái | Giới hạn/giải thích khác |
|---|---|---|
| 1 | FACT: công khai, MIT; metadata truy cập được | Nguồn chung; chưa tải/kiểm toàn bộ file |
| 2 | FACT nguồn: service gốc, fault, repeat và lúc tiêm | Onset/end/affected-region chưa có; tiêm chưa chắc gây triệu chứng ngay |
| 3 | FACT trên 1 ca: có traceID/spanID/parentSpanID; resolve 99,88% | Mất cha có thể do lấy mẫu/cắt cửa sổ/instrumentation; không suy topology đầy đủ |
| 4 | FACT trên 1 ca: metric có; log 1/1; không có cột trace ID | File có mặt chưa bảo đảm nội dung; log có thể chỉ nối được service + thời gian |
| 5 | FACT: 5 service gốc; vị trí ở mục 3 | Danh tính service, vị trí và loại lỗi có thể confound (lẫn tác động) |
| 6 | FACT nguồn: tài nguyên + mạng; không có lỗi mã nguồn trong bộ | Một bộ riêng không đủ ba nhóm; loại lỗi không bảo đảm có cùng mức triệu chứng |
| 7 | FACT khảo sát: số vượt ngưỡng theo ba phân vị ở mục 6 | OR nhiều kênh và mem có thể chiếm phần lớn mức vượt; tùy bộ/ngưỡng. Tiêu chí lan truyền nhân quả vẫn chưa xác lập |
| 8 | FACT: 720–720 điểm 1 giây trước tiêm; đủ cho khảo sát này, chưa khẳng định đủ học phương pháp | Trước tiêm chưa chắc sạch/đại diện; warm-up và drift có thể làm ngưỡng lệch |
| 9 | FACT phả hệ: cùng nhóm RCAEval/công cụ/stack | OPEN về bộ dataset chọn; cần ứng viên độc lập của T-003/G1 |

### 3. Nhãn, số ca và khả năng phân xử

**FACT metadata:** 5 service gốc, 6 loại lỗi, 30/30 ô gốc × lỗi có ca; 3–3 lần lặp/ô. Nguồn: count-summary và root-fault-cells ở mục chung. Không coi ô thiếu là ca thất bại.

| Service gốc | Số ca công khai |
|---|---|
| checkoutservice | 18 |
| currencyservice | 18 |
| emailservice | 18 |
| productcatalogservice | 18 |
| recommendationservice | 18 |

Loại lỗi / số ca: `cpu`: 15; `delay`: 15; `disk`: 15; `loss`: 15; `mem`: 15; `socket`: 15.

| Service gốc | Bậc (vào, ra) trong trace trước tiêm |
|---|---|
| checkoutservice | (1, 4) ở 1/1 ca |
| currencyservice | (2, 0) ở 1/1 ca |
| emailservice | (1, 0) ở 1/1 ca |
| productcatalogservice | (3, 0) ở 1/1 ca |
| recommendationservice | (1, 1) ở 1/1 ca |

Cạnh là parent-service → child-service khác tên, resolve bằng (traceID, spanID) trong cùng ca. Bậc là số hàng xóm phân biệt, chưa phải quan hệ có kiểu hay nhân quả. Cửa sổ trước tiêm lọc theo start của child; parent được tra trong cùng file. Không đặt ngưỡng hub. Một node không có cạnh quan sát có thể do thiếu instrumentation hoặc workload không gọi nó.

FACT: đồ thị toàn cửa sổ có 1 cấu trúc: 7 nút/9 cạnh ở 1/1 ca. Đồ thị trước tiêm của từng ca có cùng tập nút/cạnh với toàn cửa sổ (đối chiếu cases.json). Có thể cấu trúc ổn định thật, hoặc workload/độ phủ đo giới hạn cấu trúc quan sát; chưa khái quát toàn bộ hệ.

Năm root công khai đều có mặt trong graph mẫu. Checkout có cạnh vào/ra; currency/email/productcatalog chỉ có cạnh vào trong mẫu; recommendation có cả hai. `frontend` ở metric khác literal `frontendservice` ở trace. Không tự chuẩn hóa alias hay coi 7 node mẫu là toàn kiến trúc Online Boutique.

**FACT trên một ca:** `adservice`, `cartservice`, `shippingservice` và `redis` có entity trong metric/log nhưng vắng graph trace; ba service đầu có cả metric latency-90. Nguồn: cases.json (graph và log.entities), schemas.json và symptom-entity-rates.csv. `frontend`/`frontendservice` là khác tên cần alias, không gộp vào nhóm chắc chắn thiếu. Phương pháp chỉ nhận graph quan sát sẽ thiếu các node này dù metric/log có tín hiệu; mapping ba nguồn phải giữ rõ độ phủ để tránh diễn giải graph mẫu thành toàn hệ. Có thể do workload, instrumentation hoặc export, chưa xác định nguyên nhân.

### 4. Schema thật và chất lượng ba nguồn tín hiệu

**FACT trên mẫu:** metric dạng wide (mỗi chỉ báo một cột), 72–72 cột ngoài `time`, bước 1 giây, 916 ô thiếu, 0 timestamp trùng. Tên cột `<entity>_<metric>`; có thành phần hạ tầng, không đồng nhất số cột với số service. Đơn vị từng metric chưa kiểm toàn bộ; xem schema và case-summary.

Trace có 11 trường: `time`, `traceID`, `spanID`, `serviceName`, `methodName`, `operationName`, `parentSpanID`, `startTimeMillis`, `startTime`, `duration`, `statusCode`. Kiểu từng file ở schemas.json. `startTime // 1000 == startTimeMillis` trên phần đã kiểm; quy đổi startTimeMillis/1000 khớp epoch metric/log. Đơn vị duration còn OPEN; không dùng duration để xếp hạng. Không có span kind hay thuộc tính resource/db/messaging đủ dựng cạnh có kiểu.

| Phép đếm trace | Số đo trên mẫu |
|---|---|
| Tổng span | 254.889 |
| Không có parent/root | 17.108 |
| Có parent cần resolve | 237.781 |
| Tìm được key cha cùng trace | 237.492 |
| Không tìm được cha | 289 |
| Tỷ lệ cộng số đếm | 99,88% |
| Min–max tỷ lệ theo ca | 99,88%–99,88% |
| Hàng trùng (traceID,spanID) / key khác service | 0 / 0 |
| Duration thiếu / âm | 0 / 0 |
| Status có giá trị / khác 0 | 242.255 / 216 |

Log: 1/1 ca, 117.601 hàng; ba cột `timestamp` (int64), `container_name`, `message` (string). Không có cột trace/span ID; quét tất cả message: 0 nhắc khóa traceid/spanid/traceparent, 0 chuỗi ID hợp regex. Regex không bắt mọi định dạng hoặc ID không có khóa; ghép request-level còn OPEN. Nối service + thời gian là CANDIDATE, cần alias/clock hợp lệ, không phải nối từng request.

Parent resolve chỉ cho biết cha có trong artifact, không chứng minh sampling đầy đủ hay nhân quả. Status thiếu có thể do xuất/lược trường; duration không âm không chứng minh đơn vị đúng. Metric NaN có thể do không có request hoặc bộ đo thiếu; log không có ID có thể là thiết kế exporter, chưa chứng minh không có liên kết ở hệ gốc.

Độ phủ ba nguồn không trùng nhau ở các entity nêu trong mục 3. Có file trace và resolve cha cao không bảo đảm mọi service có metric/log đều có node; việc ghép theo service và thời gian còn cần kiểm mapping/clock ở adapter.

### 5. Dữ liệu bình thường và mốc thời gian

**FACT:** 720–720 hàng metric 1 giây trước lúc tiêm, tương đương 12–12 phút theo số điểm; sau tiêm 721–721 hàng. Bài nói thu bình thường 10 phút; file mẫu dài hơn. Cửa sổ lưu/export có thể khác giao thức mô tả. Mốc tiêm dùng để mô tả hai chế độ, không làm đầu vào bộ tự phát hiện. Trước tiêm chưa có kiểm chứng độc lập rằng mọi điểm sạch; clock và healthy workloads đa chế độ còn OPEN. Không gọi khoảng injection − timestamp đầu tiên là thời lượng đo nếu dữ liệu thưa hoặc injection nằm ngoài file.

**FACT trên 1 ca đã đọc:** biên metric so với injection là −720/+720 giây; điểm giữa hai timestamp đầu/cuối cho lại mốc tiêm. Đây là rò thông tin về injection có thể xảy ra qua chính telemetry, dù bỏ tên ca/file nhãn; injection chưa là onset thật. Giao thức tự phát hiện P3/P7 cần xử lý nguy cơ này trước khi chấm. Task này chưa chọn cách cắt mới hoặc kiểm một detector khai thác vị trí giữa file; biết trước mốc để khảo sát/RCA phải ghi rõ chế độ.

### 6. Ước lượng thô triệu chứng ngoài service gốc

| Phân vị q | Kênh | Ca | Đối chứng trước tiêm | Sau tiêm | Chênh min–max từng ca (điểm %) |
|---|---|---|---|---|---|
| 0.95 | Tất cả metric | 1 | 39,31% | 97,55% | 58,24 đến 58,24 |
| 0.95 | Latency p90 | 1 | 6,30% | 75,51% | 69,21 đến 69,21 |
| 0.99 | Tất cả metric | 1 | 31,57% | 97,09% | 65,51 đến 65,51 |
| 0.99 | Latency p90 | 1 | 3,38% | 75,09% | 71,71 đến 71,71 |
| 0.995 | Tất cả metric | 1 | 31,44% | 96,98% | 65,54 đến 65,54 |
| 0.995 | Latency p90 | 1 | 3,38% | 74,86% | 71,48 đến 71,48 |

Mỗi ô tỷ lệ là trung bình không trọng số: trước hết tỷ lệ hàng thời gian vượt band ở từng service ngoài root, rồi trung bình các service, rồi các ca. Không phải tỷ lệ ca lan hoặc tỷ lệ request lỗi. Công thức, các giới hạn và mapping chỉ để báo ở mục chung cuối. [Từng ca/ngưỡng](local-inspection/run-002/probe-case-summary.csv), [từng ô/ngưỡng](local-inspection/run-002/probe-cell-summary.csv), [từng service](local-inspection/run-002/symptom-entity-rates.csv), [band từng kênh](local-inspection/run-002/symptom-channel-bands.csv).

**CANDIDATE — chưa kiểm:** có tín hiệu ngoài root tăng sau tiêm, có thể chứa triệu chứng lan. Cũng có thể tải chung/drift/nhiễu, thay đổi metric hằng hoặc nhiều kênh OR giải thích nó. Không xác lập causal propagation, không gắn nhãn lan từng ca. Không thấy lệch metric cũng chưa loại trừ biểu hiện ở log/trace.

Phân rã kênh mem dưới đây dùng cùng service ngoài root và cách trung bình như bảng OR; lấy số vượt/số hợp lệ từ symptom-channel-bands.csv. Trên mẫu đã kiểm, mem và OR có cùng mẫu số hàng hợp lệ ở từng service/ca/ngưỡng. Đây là mức vượt của mem, không phải đóng góp độc lập khi bỏ mem khỏi OR.

| Phân vị q | Mem đối chứng | Mem sau tiêm | OR đối chứng | OR sau tiêm |
|---|---|---|---|---|
| 0.95 | 20,37% | 56,22% | 39,31% | 97,55% |
| 0.99 | 18,75% | 55,48% | 31,57% | 97,09% |
| 0.995 | 18,75% | 55,48% | 31,44% | 96,98% |

**OPEN — chưa phân xử nguyên nhân:** mem tăng có thể do tải, warm-up, drift, thay đổi mức nền hoặc lỗi thật; mem lớn không tự chứng minh lan hoặc drift. CSV chỉ lưu số biên từng kênh, không có giao các hàng vượt giữa kênh, nên chưa tính được OR khi bỏ mem. Chưa có đo kiểm soát tải/nhãn vùng độc lập trong task mô tả để phân xử. Không bỏ mem hoặc đổi q chỉ để giảm tỷ lệ; việc đó có thể bỏ biểu hiện mem fault thật.

### 7. Task nào chấm được?

Áp dụng bảng nhãn chung cuối tài liệu: xếp hạng root-service theo ca có nhãn; phát hiện chỉ chấm theo injection-regime với giới hạn; vùng ảnh hưởng/operation/từng trace chưa chấm trực tiếp được. Với bộ chưa kiểm schema, khả năng thực thi adapter còn OPEN. Không lấy khảo sát mục 6 làm nhãn chuẩn.

### 8. Rò nhãn và thông tin phục vụ G1

Tên thư mục chứa root/fault/repeat; inject_time là nhãn biên. Biên file telemetry cũng có thể tiết lộ injection, như các ca có mẫu ở mục 5; phần chưa đọc còn OPEN. Chỉ bỏ file nhãn/tên ca chưa đủ loại đường rò này. Chỉ dùng nhãn cho đếm/mô tả/chấm. `metric_excursions` nhận bảng metric và mốc biên, không nhận root/fault/path; root được gắn sau để báo ngoài root. Đây là khảo sát known-window (biết trước mốc), không phải tự phát hiện. Adapter P3 và giao thức tự phát hiện cần kiểm đường biên file; chưa được làm/kiểm trong task mô tả. Rò SLI của runner chính thức được MRP P2 nêu, chưa khẳng định đã sửa. Dataset/cách chia/nhãn học còn OPEN ở G1; WHY-04 là đề xuất.

### 9. Kích thước và chi phí

**FACT metadata:** 922.484.805 byte (922.485 MB thập phân) trong các thư mục ca công khai, gồm parquet và inject_time; không phải RAM hoặc ZIP giải nén. **FACT phần đã kiểm:** 7.330.444 byte telemetry parquet. Chi phí adapter và RAM cực đại **OPEN — chưa đo**; không suy từ file nhỏ rằng huấn luyện toàn bộ chạy được. Cài gói dưới 1 GB, không tải telemetry mới; thời gian/phiên bản nằm trong manifest và install.log, chi phí riêng không cộng vào khả năng phân xử.

### 10. Điều còn mở

- Onset/end, nhãn vùng và clock độc lập: cần nguồn nhãn bổ sung hoặc thực nghiệm có nhãn thật; người làm task tương ứng báo Minh trước khi dùng cho P7.

- Độ đại diện schema/topology/log và tiêu chí 7 của phần chưa đọc: chỉ 1/90 ca được kiểm. Người làm P2/task tiếp theo cần mẫu được phép; không mở dữ liệu khóa. Nút ít/thiếu có thể do workload hoặc đo thiếu.

- Tính đủ dữ liệu bình thường, phép chia/nhãn học và bộ độc lập: Minh quyết ở G1 sau các thẻ ứng viên; chưa kết luận từ kích thước hoặc dữ liệu sẵn có.

- Cạnh có kiểu, duration unit, alias và khả năng huấn luyện/chuyển hệ: cần xác minh exporter/adapter và giao thức của phương pháp ở task sau. Không biến OPEN thành lỗi dataset hoặc quyết định loại dataset.

## RE3-TT

### 1. Danh tính, nguồn và phạm vi đã kiểm

**FACT:** Train Ticket, họ RCAEval của Pham et al.; nguồn và giấy phép MIT áp dụng theo mục chung. Toàn kho có 30 ca theo directory tại revision trong manifest. Telemetry đã kiểm 1/30 ca: re3tt_ts-route-service_f2_1. Các ca còn lại chỉ đếm metadata file công khai, không đọc dữ liệu đo. Ngày kiểm: 02/10/2026.

### 2. Bảng tiêu chí 1–9

| Tiêu chí | Kết quả/trạng thái | Giới hạn/giải thích khác |
|---|---|---|
| 1 | FACT: công khai, MIT; metadata truy cập được | Nguồn chung; chưa tải/kiểm toàn bộ file |
| 2 | FACT nguồn: service gốc, fault, repeat và lúc tiêm | Onset/end/affected-region chưa có; tiêm chưa chắc gây triệu chứng ngay |
| 3 | FACT trên 1 ca: có traceID/spanID/parentSpanID; resolve 100,00% | Mất cha có thể do lấy mẫu/cắt cửa sổ/instrumentation; không suy topology đầy đủ |
| 4 | FACT trên 1 ca: metric có; log 1/1; không có cột trace ID | File có mặt chưa bảo đảm nội dung; log có thể chỉ nối được service + thời gian |
| 5 | FACT: 2 service gốc; vị trí ở mục 3 | Danh tính service, vị trí và loại lỗi có thể confound (lẫn tác động) |
| 6 | FACT nguồn: mã nguồn; không có tài nguyên/mạng trong bộ | Nhãn chỉ báo chi tiết chưa xác minh; RE3-TT mẫu có status trống, log mới rà regex (mục 4); RE3-OB chưa có mẫu |
| 7 | FACT khảo sát: số vượt ngưỡng theo ba phân vị ở mục 6 | OR nhiều kênh và mem có thể chiếm phần lớn mức vượt; tùy bộ/ngưỡng. Tiêu chí lan truyền nhân quả vẫn chưa xác lập |
| 8 | FACT: 900–900 điểm 1 giây trước tiêm; đủ cho khảo sát này, chưa khẳng định đủ học phương pháp | Trước tiêm chưa chắc sạch/đại diện; warm-up và drift có thể làm ngưỡng lệch |
| 9 | FACT phả hệ: cùng nhóm RCAEval/công cụ/stack | OPEN về bộ dataset chọn; cần ứng viên độc lập của T-003/G1 |

### 3. Nhãn, số ca và khả năng phân xử

**FACT metadata:** 2 service gốc, 4 loại lỗi, 8/8 ô gốc × lỗi có ca; 3–6 lần lặp/ô. Nguồn: count-summary và root-fault-cells ở mục chung. Không coi ô thiếu là ca thất bại.

| Service gốc | Số ca công khai |
|---|---|
| ts-auth-service | 15 |
| ts-route-service | 15 |

Loại lỗi / số ca: `f1`: 7; `f2`: 7; `f3`: 10; `f4`: 6.

| Gốc | Lỗi | Ca/lặp |
|---|---|---|
| ts-auth-service | f1 | 4 |
| ts-auth-service | f2 | 4 |
| ts-auth-service | f3 | 4 |
| ts-auth-service | f4 | 3 |
| ts-route-service | f1 | 3 |
| ts-route-service | f2 | 3 |
| ts-route-service | f3 | 6 |
| ts-route-service | f4 | 3 |

| Service gốc | Bậc (vào, ra) trong trace trước tiêm |
|---|---|
| ts-auth-service | (0, 0) ở 1/1 ca |
| ts-route-service | (3, 0) ở 1/1 ca |

Cạnh là parent-service → child-service khác tên, resolve bằng (traceID, spanID) trong cùng ca. Bậc là số hàng xóm phân biệt, chưa phải quan hệ có kiểu hay nhân quả. Cửa sổ trước tiêm lọc theo start của child; parent được tra trong cùng file. Không đặt ngưỡng hub. Một node không có cạnh quan sát có thể do thiếu instrumentation hoặc workload không gọi nó.

FACT: đồ thị toàn cửa sổ có 1 cấu trúc: 27 nút/55 cạnh ở 1/1 ca. Đồ thị trước tiêm của từng ca có cùng tập nút/cạnh với toàn cửa sổ (đối chiếu cases.json). Có thể cấu trúc ổn định thật, hoặc workload/độ phủ đo giới hạn cấu trúc quan sát; chưa khái quát toàn bộ hệ.

Hai root công khai có mặt trong graph mẫu: auth không có cạnh quan sát, route chỉ có cạnh vào. Đây là vị trí trong một ca route×f2, chưa chứng minh cùng cấu trúc ở cả 30 ca. HF card bảng ghi f1–f5 cho TT nhưng prose cùng card, tree và GitHub README chỉ f1–f4. Paper nói lặp 3–5; tree có ô route×f3 lặp 6. Giữ số đếm file, không sửa nguồn (public-sources.md).

### 4. Schema thật và chất lượng ba nguồn tín hiệu

**FACT trên mẫu:** metric dạng wide (mỗi chỉ báo một cột), 316–316 cột ngoài `time`, bước 1 giây, 21.494 ô thiếu, 0 timestamp trùng. Tên cột `<entity>_<metric>`; có thành phần hạ tầng, không đồng nhất số cột với số service. Đơn vị từng metric chưa kiểm toàn bộ; xem schema và case-summary.

Trace có 11 trường: `time`, `traceID`, `spanID`, `serviceName`, `methodName`, `operationName`, `parentSpanID`, `startTimeMillis`, `startTime`, `duration`, `statusCode`. Kiểu từng file ở schemas.json. `startTime // 1000 == startTimeMillis` trên phần đã kiểm; quy đổi startTimeMillis/1000 khớp epoch metric/log. Đơn vị duration còn OPEN; không dùng duration để xếp hạng. Không có span kind hay thuộc tính resource/db/messaging đủ dựng cạnh có kiểu.

| Phép đếm trace | Số đo trên mẫu |
|---|---|
| Tổng span | 183.623 |
| Không có parent/root | 2.623 |
| Có parent cần resolve | 181.000 |
| Tìm được key cha cùng trace | 181.000 |
| Không tìm được cha | 0 |
| Tỷ lệ cộng số đếm | 100,00% |
| Min–max tỷ lệ theo ca | 100,00%–100,00% |
| Hàng trùng (traceID,spanID) / key khác service | 0 / 0 |
| Duration thiếu / âm | 0 / 0 |
| Status có giá trị / khác 0 | 0 / 0 |

Log: 1/1 ca, 74.449 hàng; ba cột `timestamp` (int64), `container_name`, `message` (string). Không có cột trace/span ID; quét tất cả message: 0 nhắc khóa traceid/spanid/traceparent, 0 chuỗi ID hợp regex. Regex không bắt mọi định dạng hoặc ID không có khóa; ghép request-level còn OPEN. Nối service + thời gian là CANDIDATE, cần alias/clock hợp lệ, không phải nối từng request.

Parent resolve chỉ cho biết cha có trong artifact, không chứng minh sampling đầy đủ hay nhân quả. Status thiếu có thể do xuất/lược trường; duration không âm không chứng minh đơn vị đúng. Metric NaN có thể do không có request hoặc bộ đo thiếu; log không có ID có thể là thiết kế exporter, chưa chứng minh không có liên kết ở hệ gốc.

**FACT mẫu:** `statusCode` trống ở toàn bộ 183.623 span, nên không dùng kênh này làm bằng chứng response code lỗi trên ca route×f2 đã đọc. Paper §3.4 nói response code khi có sẵn; thiếu có thể do exporter hoặc lược trường, không bác bỏ chẩn đoán code fault trên toàn RE3. Log của ca này đã rà bằng regex `Exception`, ký tự tab + `at `, hoặc `ERROR`; có hàng khớp sau tiêm ở service khác root. Các hàng root khớp regex là INFO khởi động chứa tên lớp/chữ ký hàm, chưa là log lỗi đã xác minh. Nguồn raw: `data/rcaeval/re3tt_ts-route-service_f2_1/logs.parquet`; đối chiếu ngữ cảnh ở [LOG phiên tự soát 03/10](../../tasks/T-002-the-dataset-rcaeval/LOG.md). Số hàng regex không là số sự cố độc lập, nhãn vùng hay code line gốc. **OPEN — chưa xác lập:** chỉ báo log thật và liên kết với nhãn chi tiết; chưa có mapping nhãn chỉ báo đã xác minh trong mẫu, regex không đủ. Không gọi log là kênh chính của toàn RE3 từ một ca.

### 5. Dữ liệu bình thường và mốc thời gian

**FACT:** 900–900 hàng metric 1 giây trước lúc tiêm, tương đương 15–15 phút theo số điểm; sau tiêm 901–901 hàng. Bài nói thu bình thường 10 phút; file mẫu dài hơn. Cửa sổ lưu/export có thể khác giao thức mô tả. Mốc tiêm dùng để mô tả hai chế độ, không làm đầu vào bộ tự phát hiện. Trước tiêm chưa có kiểm chứng độc lập rằng mọi điểm sạch; clock và healthy workloads đa chế độ còn OPEN. Không gọi khoảng injection − timestamp đầu tiên là thời lượng đo nếu dữ liệu thưa hoặc injection nằm ngoài file.

**FACT trên 1 ca đã đọc:** biên metric so với injection là −900/+900 giây; điểm giữa hai timestamp đầu/cuối cho lại mốc tiêm. Đây là rò thông tin về injection có thể xảy ra qua chính telemetry, dù bỏ tên ca/file nhãn; injection chưa là onset thật. Giao thức tự phát hiện P3/P7 cần xử lý nguy cơ này trước khi chấm. Task này chưa chọn cách cắt mới hoặc kiểm một detector khai thác vị trí giữa file; biết trước mốc để khảo sát/RCA phải ghi rõ chế độ.

### 6. Ước lượng thô triệu chứng ngoài service gốc

| Phân vị q | Kênh | Ca | Đối chứng trước tiêm | Sau tiêm | Chênh min–max từng ca (điểm %) |
|---|---|---|---|---|---|
| 0.95 | Tất cả metric | 1 | 37,91% | 62,14% | 24,23 đến 24,23 |
| 0.95 | Latency p90 | 1 | 8,47% | 14,04% | 5,57 đến 5,57 |
| 0.99 | Tất cả metric | 1 | 6,09% | 15,06% | 8,96 đến 8,96 |
| 0.99 | Latency p90 | 1 | 4,78% | 6,94% | 2,16 đến 2,16 |
| 0.995 | Tất cả metric | 1 | 5,13% | 9,10% | 3,96 đến 3,96 |
| 0.995 | Latency p90 | 1 | 4,02% | 5,75% | 1,73 đến 1,73 |

Mỗi ô tỷ lệ là trung bình không trọng số: trước hết tỷ lệ hàng thời gian vượt band ở từng service ngoài root, rồi trung bình các service, rồi các ca. Không phải tỷ lệ ca lan hoặc tỷ lệ request lỗi. Công thức, các giới hạn và mapping chỉ để báo ở mục chung cuối. [Từng ca/ngưỡng](local-inspection/run-002/probe-case-summary.csv), [từng ô/ngưỡng](local-inspection/run-002/probe-cell-summary.csv), [từng service](local-inspection/run-002/symptom-entity-rates.csv), [band từng kênh](local-inspection/run-002/symptom-channel-bands.csv).

**CANDIDATE — chưa kiểm:** có tín hiệu ngoài root tăng sau tiêm, có thể chứa triệu chứng lan. Cũng có thể tải chung/drift/nhiễu, thay đổi metric hằng hoặc nhiều kênh OR giải thích nó. Không xác lập causal propagation, không gắn nhãn lan từng ca. Không thấy lệch metric cũng chưa loại trừ biểu hiện ở log/trace.

Phân rã kênh mem dưới đây dùng cùng service ngoài root và cách trung bình như bảng OR; lấy số vượt/số hợp lệ từ symptom-channel-bands.csv. Trên mẫu đã kiểm, mem và OR có cùng mẫu số hàng hợp lệ ở từng service/ca/ngưỡng. Đây là mức vượt của mem, không phải đóng góp độc lập khi bỏ mem khỏi OR.

| Phân vị q | Mem đối chứng | Mem sau tiêm | OR đối chứng | OR sau tiêm |
|---|---|---|---|---|
| 0.95 | 25,88% | 52,64% | 37,91% | 62,14% |
| 0.99 | 0,14% | 5,83% | 6,09% | 15,06% |
| 0.995 | 0,00% | 0,21% | 5,13% | 9,10% |

**OPEN — chưa phân xử nguyên nhân:** mem tăng có thể do tải, warm-up, drift, thay đổi mức nền hoặc lỗi thật; mem lớn không tự chứng minh lan hoặc drift. CSV chỉ lưu số biên từng kênh, không có giao các hàng vượt giữa kênh, nên chưa tính được OR khi bỏ mem. Chưa có đo kiểm soát tải/nhãn vùng độc lập trong task mô tả để phân xử. Không bỏ mem hoặc đổi q chỉ để giảm tỷ lệ; việc đó có thể bỏ biểu hiện mem fault thật.

Tất cả metric giảm từ 62,14% (q=.95) xuống 9,10% (q=.995) sau tiêm trong mẫu: ước lượng rất nhạy ngưỡng. Một ca route×f2 không đại diện f1/f3/f4 hay auth. Có thể vùng biểu hiện nhỏ, baseline biến động hoặc band rộng, chưa phân xử được cơ chế.

### 7. Task nào chấm được?

Áp dụng bảng nhãn chung cuối tài liệu: xếp hạng root-service theo ca có nhãn; phát hiện chỉ chấm theo injection-regime với giới hạn; vùng ảnh hưởng/operation/từng trace chưa chấm trực tiếp được. Với bộ chưa kiểm schema, khả năng thực thi adapter còn OPEN. Không lấy khảo sát mục 6 làm nhãn chuẩn.

### 8. Rò nhãn và thông tin phục vụ G1

Tên thư mục chứa root/fault/repeat; inject_time là nhãn biên. Biên file telemetry cũng có thể tiết lộ injection, như các ca có mẫu ở mục 5; phần chưa đọc còn OPEN. Chỉ bỏ file nhãn/tên ca chưa đủ loại đường rò này. Chỉ dùng nhãn cho đếm/mô tả/chấm. `metric_excursions` nhận bảng metric và mốc biên, không nhận root/fault/path; root được gắn sau để báo ngoài root. Đây là khảo sát known-window (biết trước mốc), không phải tự phát hiện. Adapter P3 và giao thức tự phát hiện cần kiểm đường biên file; chưa được làm/kiểm trong task mô tả. Rò SLI của runner chính thức được MRP P2 nêu, chưa khẳng định đã sửa. Dataset/cách chia/nhãn học còn OPEN ở G1; WHY-04 là đề xuất.

### 9. Kích thước và chi phí

**FACT metadata:** 161.389.958 byte (161.390 MB thập phân) trong các thư mục ca công khai, gồm parquet và inject_time; không phải RAM hoặc ZIP giải nén. **FACT phần đã kiểm:** 6.837.461 byte telemetry parquet. Chi phí adapter và RAM cực đại **OPEN — chưa đo**; không suy từ file nhỏ rằng huấn luyện toàn bộ chạy được. Cài gói dưới 1 GB, không tải telemetry mới; thời gian/phiên bản nằm trong manifest và install.log, chi phí riêng không cộng vào khả năng phân xử.

### 10. Điều còn mở

- Onset/end, nhãn vùng và clock độc lập: cần nguồn nhãn bổ sung hoặc thực nghiệm có nhãn thật; người làm task tương ứng báo Minh trước khi dùng cho P7.

- Độ đại diện schema/topology/log và tiêu chí 7 của phần chưa đọc: chỉ 1/30 ca được kiểm. Người làm P2/task tiếp theo cần mẫu được phép; không mở dữ liệu khóa. Nút ít/thiếu có thể do workload hoặc đo thiếu.

- Tính đủ dữ liệu bình thường, phép chia/nhãn học và bộ độc lập: Minh quyết ở G1 sau các thẻ ứng viên; chưa kết luận từ kích thước hoặc dữ liệu sẵn có.

- Cạnh có kiểu, duration unit, alias và khả năng huấn luyện/chuyển hệ: cần xác minh exporter/adapter và giao thức của phương pháp ở task sau. Không biến OPEN thành lỗi dataset hoặc quyết định loại dataset.

## RE3-OB

### 1. Danh tính, nguồn và phạm vi đã kiểm

**FACT:** Online Boutique, họ RCAEval của Pham et al.; nguồn và giấy phép MIT áp dụng theo mục chung. Toàn kho có 30 ca theo directory tại revision trong manifest. Telemetry đã kiểm 0/30 ca: 0 ca; không có mẫu cục bộ. Các ca còn lại chỉ đếm metadata file công khai, không đọc dữ liệu đo. Ngày kiểm: 02/10/2026.

### 2. Bảng tiêu chí 1–9

| Tiêu chí | Kết quả/trạng thái | Giới hạn/giải thích khác |
|---|---|---|
| 1 | FACT: công khai, MIT; metadata truy cập được | Nguồn chung; chưa tải/kiểm toàn bộ file |
| 2 | FACT nguồn: service gốc, fault, repeat và lúc tiêm | Onset/end/affected-region chưa có; tiêm chưa chắc gây triệu chứng ngay |
| 3 | OPEN — chưa kiểm schema; metadata có 30 file trace | Mất cha có thể do lấy mẫu/cắt cửa sổ/instrumentation; không suy topology đầy đủ |
| 4 | OPEN — chưa kiểm nội dung; metadata có metric/log | File có mặt chưa bảo đảm nội dung; log có thể chỉ nối được service + thời gian |
| 5 | FACT: 4 service gốc; vị trí ở mục 3 | Danh tính service, vị trí và loại lỗi có thể confound (lẫn tác động) |
| 6 | FACT nguồn: mã nguồn; không có tài nguyên/mạng trong bộ | Nhãn chỉ báo chi tiết chưa xác minh; RE3-TT mẫu có status trống, log mới rà regex (mục 4); RE3-OB chưa có mẫu |
| 7 | OPEN — chưa kiểm; không có mẫu | OR nhiều kênh và mem có thể chiếm phần lớn mức vượt; tùy bộ/ngưỡng. Tiêu chí lan truyền nhân quả vẫn chưa xác lập |
| 8 | OPEN — chưa kiểm độ dài trên file; bài mô tả 10 phút | Trước tiêm chưa chắc sạch/đại diện; warm-up và drift có thể làm ngưỡng lệch |
| 9 | FACT phả hệ: cùng nhóm RCAEval/công cụ/stack | OPEN về bộ dataset chọn; cần ứng viên độc lập của T-003/G1 |

### 3. Nhãn, số ca và khả năng phân xử

**FACT metadata:** 4 service gốc, 5 loại lỗi, 10/20 ô gốc × lỗi có ca; 3–3 lần lặp/ô. Nguồn: count-summary và root-fault-cells ở mục chung. Không coi ô thiếu là ca thất bại.

| Service gốc | Số ca công khai |
|---|---|
| adservice | 9 |
| cartservice | 3 |
| currencyservice | 3 |
| emailservice | 15 |

Loại lỗi / số ca: `f1`: 9; `f2`: 3; `f3`: 6; `f4`: 6; `f5`: 6.

| Gốc | Lỗi | Ca/lặp |
|---|---|---|
| adservice | f3 | 3 |
| adservice | f4 | 3 |
| adservice | f5 | 3 |
| cartservice | f1 | 3 |
| currencyservice | f1 | 3 |
| emailservice | f1 | 3 |
| emailservice | f2 | 3 |
| emailservice | f3 | 3 |
| emailservice | f4 | 3 |
| emailservice | f5 | 3 |

| Service gốc | Bậc (vào, ra) trong trace trước tiêm |
|---|---|
| adservice | OPEN — chưa kiểm; không có mẫu |
| cartservice | OPEN — chưa kiểm; không có mẫu |
| currencyservice | OPEN — chưa kiểm; không có mẫu |
| emailservice | OPEN — chưa kiểm; không có mẫu |

Cạnh là parent-service → child-service khác tên, resolve bằng (traceID, spanID) trong cùng ca. Bậc là số hàng xóm phân biệt, chưa phải quan hệ có kiểu hay nhân quả. Cửa sổ trước tiêm lọc theo start của child; parent được tra trong cùng file. Không đặt ngưỡng hub. Một node không có cạnh quan sát có thể do thiếu instrumentation hoặc workload không gọi nó.

### 4. Schema thật và chất lượng ba nguồn tín hiệu

**OPEN — chưa kiểm:** schema, parent resolution, chất lượng log/metric, status/duration và clock: không có mẫu RE3-OB. Metadata có 30/30 file của mỗi modality. Không lấy schema hoặc tỷ lệ RE2-OB thay cho RE3-OB; exporter/phiên bản/code faults có thể khác.

**CANDIDATE — chưa kiểm:** nếu instrumentation RE3-OB giống mẫu RE2-OB, ad/cart có thể thiếu node trace dù có metric/log; hai root này có 12/30 ca công khai (ad 9, cart 3; count-summary.json). Giả thuyết có thể sai khi phiên bản, exporter hoặc workload khác. Không có telemetry RE3-OB được phép đọc trong task để kiểm; giữ tiêu chí 3/4 và vị trí root OPEN, không loại dataset từ mẫu RE2-OB.

### 5. Dữ liệu bình thường và mốc thời gian

**FACT nguồn:** bài mô tả 10 phút bình thường và inject_time Unix. **OPEN — chưa kiểm** độ dài/nhịp thực tế từng ca, contamination, thời gian onset/kết thúc và clock: không có mẫu. Đủ để học ngưỡng nào phụ thuộc phương pháp sau này.

### 6. Ước lượng thô triệu chứng ngoài service gốc

**OPEN — chưa kiểm:** không có mẫu nên không đo tiêu chí 7. Không suy từ RE2-OB hoặc từ nhãn code fault rằng triệu chứng sẽ lan. Cần mẫu được Minh cho phép; nếu chọn làm bộ giữ ngoài, giữ OPEN đến G3 theo MRP.

### 7. Task nào chấm được?

Áp dụng bảng nhãn chung cuối tài liệu: xếp hạng root-service theo ca có nhãn; phát hiện chỉ chấm theo injection-regime với giới hạn; vùng ảnh hưởng/operation/từng trace chưa chấm trực tiếp được. Với bộ chưa kiểm schema, khả năng thực thi adapter còn OPEN. Không lấy khảo sát mục 6 làm nhãn chuẩn.

### 8. Rò nhãn và thông tin phục vụ G1

Tên thư mục chứa root/fault/repeat; inject_time là nhãn biên. Biên file telemetry cũng có thể tiết lộ injection, như các ca có mẫu ở mục 5; phần chưa đọc còn OPEN. Chỉ bỏ file nhãn/tên ca chưa đủ loại đường rò này. Chỉ dùng nhãn cho đếm/mô tả/chấm. `metric_excursions` nhận bảng metric và mốc biên, không nhận root/fault/path; root được gắn sau để báo ngoài root. Đây là khảo sát known-window (biết trước mốc), không phải tự phát hiện. Adapter P3 và giao thức tự phát hiện cần kiểm đường biên file; chưa được làm/kiểm trong task mô tả. Rò SLI của runner chính thức được MRP P2 nêu, chưa khẳng định đã sửa. Dataset/cách chia/nhãn học còn OPEN ở G1; WHY-04 là đề xuất.

### 9. Kích thước và chi phí

**FACT metadata:** 138.129.790 byte (138.130 MB thập phân) trong các thư mục ca công khai, gồm parquet và inject_time; không phải RAM hoặc ZIP giải nén. **FACT phần đã kiểm:** 0 byte telemetry parquet. Chi phí adapter và RAM cực đại **OPEN — chưa đo**; không suy từ file nhỏ rằng huấn luyện toàn bộ chạy được. Cài gói dưới 1 GB, không tải telemetry mới; thời gian/phiên bản nằm trong manifest và install.log, chi phí riêng không cộng vào khả năng phân xử.

### 10. Điều còn mở

- Onset/end, nhãn vùng và clock độc lập: cần nguồn nhãn bổ sung hoặc thực nghiệm có nhãn thật; người làm task tương ứng báo Minh trước khi dùng cho P7.

- Độ đại diện schema/topology/log và tiêu chí 7 của phần chưa đọc: chỉ 0/30 ca được kiểm. Người làm P2/task tiếp theo cần mẫu được phép; không mở dữ liệu khóa. Nút ít/thiếu có thể do workload hoặc đo thiếu.

- Tính đủ dữ liệu bình thường, phép chia/nhãn học và bộ độc lập: Minh quyết ở G1 sau các thẻ ứng viên; chưa kết luận từ kích thước hoặc dữ liệu sẵn có.

- Cạnh có kiểu, duration unit, alias và khả năng huấn luyện/chuyển hệ: cần xác minh exporter/adapter và giao thức của phương pháp ở task sau. Không biến OPEN thành lỗi dataset hoặc quyết định loại dataset.

## Phép tính và giới hạn chung cho mục 6 của bốn thẻ

Đây là khảo sát mô tả được SPEC yêu cầu, chưa chọn detector/threshold cho P3–P7. Căn cứ mục đích: WHY-03 và MRP P2 đã yêu cầu đếm khả năng phân xử trước giả thuyết. Không bổ sung lựa chọn nghiên cứu quan trọng vào WHY hoặc DECISIONS trong task này.

1. Sắp metric theo time. Chia trước tiêm: 2/3 đầu làm đoạn tham chiếu (480 điểm RE2, 600 điểm RE3-TT mẫu), 1/3 cuối làm đối chứng bình thường (240/300). Đây là cách thử tạm để nhìn drift, không khóa cách chia học/chấm.

2. Với mọi cột số, trừ time, có ít nhất 30 điểm hữu hạn tham chiếu: m là median; band b(q) là phân vị q của |x−m| trên tham chiếu, q ∈ {.95,.99,.995}. Điểm vượt khi |x−m| > b(q). Không có sàn epsilon hay chia cho độ lệch chuẩn. NaN không là vượt; hàng thiếu mọi kênh của một nhóm được loại khỏi mẫu số nhóm. Nếu service/nhóm không có điểm hợp lệ, tỷ lệ không xác định và bỏ khỏi trung bình, không thay bằng 0. Band 0 coi mọi thay đổi hữu hạn là vượt và được lưu riêng.

3. Tách entity bằng dấu `_` cuối tên cột. Nhóm tất cả metric dùng OR (chỉ cần một kênh vượt); nhóm latency90 chỉ dùng cột `_latency-90`. Tính band cho mọi entity trước khi biết root. Để mô tả service ngoài root, sau đó lọc tên entity kết thúc `service` hoặc là `frontend`, bỏ đúng tên root. Đây là heuristic (quy tắc thử theo tên), chưa mapping dịch vụ hoàn chỉnh; excludes DB/broker và có thể sai với hệ khác. Không chọn SLI theo root.

4. Báo tỷ lệ time-row và chênh trước/sau liên tục, từng service/ca/ô. Không ngưỡng hóa chênh để tạo nhãn lan. Nhiều metric OR làm tỷ lệ cao; mẫu ít làm q=.995 không ổn định; flat bands, tải/clock/drift cùng thay đổi là lời giải thích đối lập. Vì vậy bảng chỉ cho biết sự sẵn có của tín hiệu cần kiểm tiếp, chưa chứng minh đường lan hoặc lợi ích đồ thị.

5. Mức 1−q (0,5% khi q=.995) chỉ là mức danh nghĩa cho một kênh dưới phân phối tham chiếu ổn định và điều kiện phù hợp; phân vị hữu hạn, ties và phụ thuộc thời gian có thể làm lệch. Đây không phải mức kỳ vọng của OR nhiều kênh. Các số mem và cận band0 chỉ mô tả thành phần mức vượt trên cùng mẫu số; không chứng minh drift, đóng góp riêng của kênh hay tiêu chí lan truyền nhân quả. Đối chiếu thêm trên từng ô/ca trong CSV trước khi dùng cho task đo.

Phép thử đối chiếu rẻ: trong RE2-OB mẫu tại q=.99, paymentservice có tỷ lệ control all_metrics 59,17% nhưng latency90 0%; post lần lượt 100% và 0%. Một nhóm kênh tăng không đồng nghĩa request chậm ở service đó. Nguồn: symptom-entity-rates.csv. Các tỷ lệ và số band0 có thể kiểm lại từ CSV, không lấy từ trí nhớ.

Ca RE2-TT travel×disk lặp 2 có latency90 của ts-payment-service đủ điểm tham chiếu nhưng không có điểm hợp lệ ở control/post; rate để không xác định. Ca route×mem lặp 2 cũng thiếu mọi metric ở entity hạ tầng istio-init trong hai đoạn đó. Thiếu dữ liệu không phải bằng chứng không có triệu chứng. Nguồn: symptom-entity-rates.csv.

## Bảng khả năng chấm — áp dụng riêng cho từng thẻ

| Task | Nhãn thực có theo nguồn | Chấm được đến đâu | Giới hạn |
|---|---|---|---|
| Xếp hạng nguyên nhân gốc | Root service đơn theo ca, fault/repeat | MRR, Hit@k; NDCG nhị phân theo service | Không chấm được operation/code line từ tên service; nhãn tiêm chưa là kiểm chứng causal độc lập |
| Phát hiện theo thời gian | Timestamp tiêm; thời gian file | Có thể chấm injection-regime khi giao thức P7 ghi rõ và xử lý nguy cơ suy injection từ biên file | 32 ca mục tiêu có metric đối xứng; phần chưa đọc OPEN. Thiếu onset/end độc lập; chưa có detector bị chứng minh khai thác rò, không gọi P/R/F1 này là phát hiện triệu chứng thật |
| Vùng ảnh hưởng | Không thấy nhãn affected components ở nguồn đã đọc | Chưa chấm trực tiếp Precision/Recall/F1 vùng | Probe ngoài root không thay nhãn vùng |
| Bất thường từng trace / định vị operation | Chưa xác minh nhãn từng trace/operation gốc; paper nói có chỉ báo, tree chỉ có 8 root_cause.txt ở RE3-SS | Chưa chấm trực tiếp bằng artifact đã xác minh của bốn bộ | Không thấy tên file chưa chứng minh thiếu mọi nhãn chi tiết. RE3-TT mẫu status trống; status/latency/regex log và tên fault không tự trở thành nhãn |
| Học có giám sát/chuyển hệ | Ngân sách nhãn/cách chia chưa chốt | OPEN ở G1/P1/P3 | 5/2/4 root ít không đủ suy độ khái quát; không xếp chung điều kiện có/không giám sát thiếu ghi rõ |

## Mẫu phụ và đối chiếu nguồn

Schema cũng được lưu cho RE1-OB, RE2-SS và RE3-SS có sẵn. Hai mẫu Sock Shop không có trace parquet; không biến kiểm hai mẫu thành kết luận toàn kho SS trong task này. RE1-OB mẫu chỉ có 63 điểm metric ở khoảng 62 giây và mốc tiêm ngoài cửa sổ; không dùng nó để ước lượng triệu chứng. Không viết thẻ SS/RE1 hoặc chọn thêm bộ ngoài SPEC.

K2/README cũ là thông tin chưa kiểm; số mới không thay quyết định của Minh. RE3-TT F5/repeats và RE2-TT topology có điểm không khớp đã nêu rõ. Muốn sửa tài liệu nền phải đề xuất riêng theo Luật 0. Không chọn/bỏ bộ nào, chưa kết luận RCAEval hơn/kém ứng viên khác.
