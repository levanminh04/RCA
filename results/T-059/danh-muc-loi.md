# Danh mục lỗi FlashTicket — T-059

**CANDIDATE — bản sửa chặng 1c, chờ kiểm văn bản và Minh duyệt bảng.** 11/11/2026.

- Nguồn đủ để soạn yêu cầu 2i. B4 cần chọn cấu hình thử, xác nhận từng cơ chế bằng đầu dò, kiểm chất lượng quan sát ở tải thấp/cao và nền trước khi khóa thực nghiệm.
- Không có ô fault đã xác nhận can thiệp ở T-059. Số ô định nghĩa không phải số ô hữu hiệu hoặc số lượt. Dấu hiệu RCA là dự kiến, khả năng phân biệt và kết quả RQ5 còn OPEN.

## Nguồn và mức bằng chứng

| Mức | Nguồn | Bằng chứng và phạm vi |
|---|---|---|
| Mục tiêu | DT18 §2 (NV1–NV3), hướng dẫn cô §1, MRP RQ5/P10 và D.1/D.9/D.11 | So phương pháp sau thực nghiệm công khai trên hệ bán vé thật, với tải đổi, lỗi có nguyên nhân được xác nhận và ca tải khỏe. Danh mục khai trước giúp tránh chọn ca theo kết quả và chuyển bằng chứng thành việc 2i. |
| Thiết kế | D.9, B1.9 T-043, B16 và R-01–R-10 | Quy tắc, loại cạnh và tín hiệu cần thu. Tên nút dùng inventory T-037 đã đóng trong flashticket-inventory-source.json. Thiết kế cạnh/thuộc tính là căn cứ đối chiếu; vị trí cụ thể dùng mã và runtime. |
| Checkout | D:/Project/flash-ticket-platform, HEAD 1d40c97076db402d3e0d529a3b48523d37837240 | Đọc Git blob của từng commit triển khai. Booking/Payment/Ticket không có diff trong thư mục service so với checkout; gateway và event có diff trong thư mục của mình. Dẫn dòng theo commit gốc dù tệp tương ứng trong checkout có thể giống. |
| Revision đang chạy | T-058 dem-2026-11-10/build-manifest.json và docker inspect trên exp-app 11:00:14Z, 11/11/2026 | Khớp image ID của 8 service. Booking e4304048, Gateway/Event 9eea593a, Payment/Ticket 5c6d1c13, discovery 5c6d1c13, User 22067803, Keycloak 776d9c9e. Các revision đầy đủ ở bảng mã và build manifest. Các tuyến áp dụng lại cần chụp image/config ở lượt B4. |
| Đường chạy và fixture | T-058 dem-2026-11-10/smoke-api-final.json, kiem-agent.md, kiem-telemetry.md, rca-ban-dau.md; docker inspect exp-app 11:02–11:04Z, 11:17Z | T-058 thấy catalog/detail vào Event, availability vào Booking, đã tạo đơn và trả URL thanh toán giả. Chưa có tải thanh toán–phát vé–hoàn tiền khép kín. Booking/Event/Payment/Ticket dùng PostgreSQL chung, Redis chung, RabbitMQ vhost /. App JVM dùng host networking, không có CapAdd hoặc quota CPU riêng trong các container đích. Booking 8082, Payment 8083, Ticket 8084, Event 8086. Ticket business/listener/worker bật. Payment có BOOKING_SERVICE_URL tới 127.0.0.1:8082. Kiểm 11:17Z xác nhận include filelog trùng LogPath của Booking, Event, Payment, Ticket và Gateway; độ phủ export vẫn cần kiểm. VNPay API và URL thanh toán hiện trỏ 127.0.0.1:9. |
| Toàn vẹn | T-040/manifest.json /files và T-058/dem-2026-11-10/artifacts-sha256.json /files | Khớp SHA-256 và byte của R-01–R-10 và 203/203 mục T-058. Hai mục manifest thiếu ở bản repo có bản đúng byte trong out của lượt gốc. Sổ KP đang nối tiếp và tài liệu truy cập ngoài snapshot không có digest chung. Dùng sổ để định vị, đối chiếu bản băm, mã hoặc kiểm đọc trực tiếp trước khi dùng làm bằng chứng. Giữ riêng cập nhật lịch sử KP chưa kiểm lại trong phiên. |
| Gói sửa sau phản biện | DECISIONS T-059 (11/11/2026), WHY-80 và D.9 | Bổ sung vị trí Event, giữ topology proxy cố định, quy tắc tải chung và nhóm 429. Kết quả kiểm bytecode dùng JAR Gateway theo BOM; image/config hiệu lực cần xác nhận ở B4. |
| Giới hạn | T-059 SPEC câu 1–7; chặng 1c và 2i; PLAN §5/B4 | Định nghĩa là CANDIDATE chờ kiểm văn bản/Minh duyệt bảng. Runtime kiểm chỉ đọc cho biết vị trí và điều kiện triển khai. Cường độ, can thiệp thật, ảnh hưởng, độ phủ, ngưỡng, chi phí đợt phát triển và hiệu quả RQ5 cần bằng chứng B4 trở đi. Toxiproxy và Pumba trên ARM còn cần xác nhận khi dựng bộ tiêm. |

## Quy tắc ghi nhãn và chấm

- **Ba lớp.** Giữ can thiệp dự định (vị trí và cơ chế), kết quả xác nhận độc lập và khả năng phân biệt của telemetry. Ở T-059 chưa thử ô nào. Root khai trước chỉ trở thành đáp án thật của lượt nếu đầu dò xác nhận. Khi đầu dò chưa xác nhận, ghi “can thiệp chưa xác nhận”, giữ bản ghi và tách khỏi mẫu đã xác nhận. Khi đã xác nhận nhưng RCA thiếu dữ liệu, giữ root thật và cờ giới hạn/coverage.
- **Cạnh và nút.** Root thật là cặp có hướng và loại cạnh với ô tiêm tuyến; root là thành phần đối với ô tiêm tại đích/ở trong service. POOL-BOOK giữ pool Hikari là vị trí vật lý và booking-service là nút chiếu. DB-BOOK-DOWN chỉ nhận booking_db nếu kiểm được mất ở đích độc lập với tuyến. Cạnh Booking→DB là biểu hiện có thể gặp ở cả ba cơ chế.
- **Chấm cạnh.** Ba cột tách riêng: (1) khớp root thật theo loại và hướng; nếu bản chỉ xếp hạng nút thì khai không hỗ trợ kết luận đúng cạnh thật, không quy công từ điểm nút; (2) điểm định vị qua tập chấp nhận chung {caller, callee} theo cơ chế cạnh, áp y hệt cho mọi phương pháp trên đầu ra thực thể; (3) bảng định vị cạnh có định danh/binding riêng, không có đầu ra cạnh thì UNSUPPORTED. Ghi loại đầu ra và mẫu số từng bảng. Ô nút chấm đúng nút; không dùng tập thay thế.
- **Quan sát và thiếu dữ liệu.** Theo B1.9, chỉ ghi một nút quan sát được nếu có span của chính nó, CLIENT từ caller có đích đã xác minh, hoặc metric/log của nó. Cờ ‘chỉ thấy qua caller’ tách riêng. Chưa có mẫu vì mất export/sampling khác với có mẫu 0 hoặc ca im lặng thật. Không gán số 0 để lấp mất kênh.
- **Ảnh hưởng endpoint.** Dùng k6/Synthetics độc lập theo route, tại thời điểm bắt đầu có tác động và hồi phục quan sát được. Chốt ngưỡng route trước lượt; đối chiếu dự đoán và nhãn ở cùng mức endpoint. Thời gian khởi/khôi phục can thiệp lấy từ đầu dò. Với MQ đo thêm backlog và trạng thái giao dịch ngoài RCA, không suy vùng thành phần từ endpoint.
- **Ca khỏe.** Chỉ gán root = null sau khi đạt ngưỡng backend khai trước và checks độc lập. Phân loại 429, tải suy giảm và ca chưa phân xử theo quy tắc tải. Giữ toàn bộ cảnh báo trong nhóm tương ứng.
- **Cách ly.** PLAN §5: mã lượt mờ; ledger JSONL chỉ nối, hash nối dòng, user ledger quyền 600 và user rca không đọc. Mốc tiêm, probe, lịch tải, tên ô, định danh hook/mock và log công cụ không vào adapter/phương pháp. Bản biết mốc nhận t (giây nguyên) qua điều phối. Bản tự phát hiện chỉ nhận t̂ từ cảnh báo; ghép nhãn sau khi băm đầu ra. Nút proxy không xuất hiện khi chỉ bật lỗi: giữ proxy trong mọi ô, mọi pha, các đêm nền và đối chứng, alias đích theo binding. Liveness định kỳ nếu đưa vào RCA phải tách khỏi probe xác nhận pause.
- **Điểm nghiên cứu.** Cùng ca và cách chấm cho bản P7 khóa chạy thẳng, bản FlashTicket khóa và từng bản che nhóm thông tin; ghi UNSUPPORTED khi cần. Giữ ablation bỏ cạnh có kiểu, báo từng kịch bản kể cả thua, kết quả đầu của bản khóa và mọi sửa dùng dữ liệu đánh giá. Báo riêng chuyển thẳng và sau thích nghi, phát hiện và chẩn đoán.

## Ứng viên nhãn mức thao tác (P59-1)

Ứng viên đáp án cho bộ chấm hướng 2 hoặc chấm gợi ý thao tác gốc của LLM nếu Minh chọn làm. Xếp hạng service của M1 và hiển thị thao tác hướng 1 dùng telemetry/đầu ra M1 độc lập với trường này.

Khai trước khi chạy các ca liên quan. Ở B4, nối bằng chứng hook từ đầu dò ngoài RCA với đúng request hoặc message và ánh xạ sang span đã xác minh. Nếu có nhiều span hợp lệ, khai trước quy tắc chọn hoặc tập đáp án chấp nhận. Chỉ chấm nhãn đã xác minh theo quy tắc khóa trước lượt đánh giá. Lưu bên bộ chấm, ghép sau khi băm đầu ra, giữ cách ly với M1 và lớp hiển thị thông thường.

| Ô nhắm một thao tác | Vị trí hook khai trước | Span ứng viên |
|---|---|---|
| [HTTP5-EVENT](#http5-event) | EventController.publicEvent trước service.readPublic. [G-route](#g-route), [E-event](#e-event), [E-read](#e-read), [E-db](#e-db) | Chờ ánh xạ B4 |
| [HTTP5-BOOK](#http5-book) | OrderController.getOrder trước orderService.getOrder. [G-route](#g-route), [B-order](#b-order), [B-read](#b-read) | Chờ ánh xạ B4 |
| [SLOW-BOOK](#slow-book) | OrderController.getOrder trước khi vào transaction của orderService.getOrder. [G-route](#g-route), [B-order](#b-order), [B-read](#b-read) | Chờ ánh xạ B4 |
| [SLOW-EVENT](#slow-event) | EventController.publicEvent trước khi vào transaction của service.readPublic. [G-route](#g-route), [E-event](#e-event), [E-read](#e-read), [E-db](#e-db) | Chờ ánh xạ B4 |
| [SAGA-TICKET-FAIL](#saga-ticket-fail) | TicketService.issue, transaction PENDING ngay trước nhánh tạo vé/QR; dùng hợp đồng FAILED, outbox/inbox hiện có và một mã lỗi thử đã được contract chấp nhận. [G-route](#g-route), [P-pay](#p-pay), [P-ipn](#p-ipn), [P-saga](#p-saga), [B-accept](#b-accept), [P-consume](#p-consume), [P-binding](#p-binding), [T-listen](#t-listen), [T-queue](#t-queue), [T-issue](#t-issue), [T-result](#t-result), [T-send](#t-send), [B-fail](#b-fail), [B-release](#b-release), [T-api](#t-api), [T-bind](#t-bind) | Chờ ánh xạ B4 |

Hook terminal thuộc TicketService.issue. Xác nhận hook chạy trên đúng lệnh phát vé và span bao nhánh lỗi; phân biệt span listener với span xử lý nghiệp vụ. Cả năm ô là CANDIDATE. Kết quả ánh xạ và nhãn đã xác minh đang để trống.

**Lỗi trên tuyến.** `DB-BOOK-LAT`, `EVENT-DB-LAT`, `REDIS-BOOK`, `REDIS-GW`, `NET-GW-BOOK`, `NET-GW-EVENT`, `NET-PAY-BOOK`, `VNPAY-REFUND-LAT`. Root giữ ở cạnh. Span CLIENT của bên gọi hỗ trợ định vị tuyến.

**Không định nghĩa thao tác gốc theo cách đặt ô.**

- `POOL-BOOK`. Pool dùng chung cho các thao tác lấy kết nối DB của Booking.
- `DB-BOOK-DOWN`. Can thiệp ở DB đích, ngoài đơn vị thao tác.
- `TICKET-PAUSE`. Pause toàn container Ticket, gồm cả listener, HTTP và worker.
- `CPU-BOOK`. Can thiệp ở cgroup Booking, có thể tác động nhiều thao tác.
- `CPU-EVENT`. Can thiệp ở cgroup Event, có thể tác động nhiều thao tác.
- `POOL-EVENT`. Nếu đưa vào danh mục, can thiệp nhắm pool Event dùng chung cho các thao tác DB. POOL-EVENT hiện là ứng viên vị trí ngoài bảng chia.

**Đối chứng.** `FLASH-HEALTHY` giữ quy tắc `root = null` của ca khỏe đã xác nhận.

## Hồ sơ tải và quy tắc 429

- **Hỗn hợp chung.** Dùng cùng hỗn hợp thao tác, tỷ trọng, lịch nghiệp vụ và topology cho mọi ô, mọi pha, các đêm nền và ca đối chứng khỏe trong chiến dịch. Giữ proxy JDBC của Event và Booking trong topology, kể cả nền dài. Thay tốc độ theo hồ sơ tải khai trước và giữ cơ hội kích hoạt từng tuyến. Lịch tới, tên hồ sơ, dữ liệu đầu dò và mã ô chỉ lưu trong sổ thử nghiệm.
- **Luồng đặc thù.** Ưu tiên chạy thanh toán–phát vé và hoàn tiền nhịp thấp theo lô fixture trên hỗn hợp chung. Giữ lịch hủy/IPN, số charge, thời hạn poll và nhịp trước–trong–sau ca tương ứng. Đo bằng mock và đầu dò ngoài RCA. Một lần hủy trước nền có thể tạo hết POST trước pha lỗi. Nếu không đủ fixture, dùng hồ sơ riêng với đối chứng cùng lịch; báo riêng nhóm có thể suy loại ca từ tập nút/tuyến có dữ liệu.
- **Quota và ngưỡng tải.** G-limit cấu hình 10 token/s, burst 20, 1 token/request. BOM Gateway 2025.1.3 trỏ tới 5.0.3; bytecode ghép route ID với khóa địa chỉ kết nối. B4 xác nhận image/config hiệu lực, ghi trước lượt chấm các ngưỡng số request/s thực đến từng service và khoảng đo cho từng mức tải. Dùng số đo độc lập ngoài RCA, ghi riêng tải gửi, tải Gateway chấp nhận, 429 theo nguồn/route và tải đến backend. Mức số chưa đo. Giữ quota thật nếu đạt hai mức tải khỏe. Nếu cần quota thử, trình Minh chốt trước khi khóa, ghim R-10 và dùng giống nhau ở phát triển/đánh giá.
- **Phân loại và mẫu số.** FLASH-HEALTHY chỉ được xác nhận nếu đạt ngưỡng backend đã khai và tiêu chí sức khỏe độc lập. 429 xác nhận do quota dự kiến mà backend không đạt ngưỡng thuộc nhóm bị giới hạn ở Gateway. Báo mọi cảnh báo, số ca và thời gian quan sát của nhóm này trong bảng riêng, ngoài mẫu số khỏe chính. Suy giảm thật báo riêng. Ca thiếu chứng cứ nguồn 429 hoặc ngưỡng tải báo riêng là chưa phân xử, giữ cảnh báo và số ca. Áp dụng quy tắc định trước khi xem đầu ra RCA.

- **Ngưỡng số.** OPEN — B4 hiệu chuẩn trước khi khóa. Các trường ngưỡng theo service, khoảng đo và quota hiệu lực để trống trong JSON tới khi có số đo B4.

## Danh mục theo D.9

| Kịch bản | Vị trí đã định nghĩa |
|---|---|
| D9-01 · Đường truy cập DB chậm | Event→event_db cho phát triển và Booking→booking_db cho đánh giá. Hai đường JDBC thật cần listener độc lập; cùng đích vật lý không có nghĩa cùng tuyến. |
| D9-02 · Cạn pool kết nối hoặc mất DB | Hai cơ chế riêng tại pool của Booking và DB logic booking_db. Mất đường riêng từ Booking vẫn là lỗi đường, không xác nhận DB chết. POOL-EVENT là ứng viên ngoài bảng chia, thiếu hook và kiểm cơ chế. |
| D9-03 · Redis chậm | Hai client thực trên Redis dùng chung, tách tuyến tại từng caller. |
| D9-04 · Consumer phát vé dừng | Chỉ Ticket nhận ticket.issue.v1. Pause cả container còn dừng HTTP và worker Ticket. Các consumer Booking/Payment xử lý thông điệp khác. |
| D9-05 · Thao tác trả lỗi 5xx | Hai điểm vào chỉ đọc thật của Event và Booking, cùng cơ chế cờ lỗi. |
| D9-06 · Thao tác chậm bên trong | Hai điểm vào chỉ đọc thật trước khi gọi tầng service/DB, cùng cơ chế cờ trễ. |
| D9-07 · Trễ mạng giữa hai service | Ba cạnh HTTP có thao tác tải chỉ ra được; phạm vi chặn hiện tại là cô lập đường đi. |
| D9-08 · Cạn CPU | Hai JVM có endpoint độc lập. Định danh đích stress theo cgroup; cùng host chưa có quota riêng. |
| D9-09 · VNPay chậm | Hai thao tác cùng HTTP client, đích và tuyến proxy. Một vị trí Payment→VNPay. |
| D9-10 · Saga phải bù trừ | Một điểm terminal khi phát vé. Exception retry và hủy event là cơ chế khác. |
| D9-11 · Flash sale, không có lỗi | Đối chứng không có root khi đạt tiêu chí sức khỏe. Hai hồ sơ tải tách biệt, giữ lịch và dữ liệu riêng. |

| Ô | Kịch bản | Root khai trước | Đợt | Tình trạng |
|---|---|---|---|---|
| [DB-BOOK-LAT](#db-book-lat) | D9-01 | `booking-service → booking_db` (data) | đánh giá | OPEN — tuyến JDBC tách riêng |
| [EVENT-DB-LAT](#event-db-lat) | D9-01 | `event-service → event_db` (data) | phát triển | OPEN — tuyến JDBC tách riêng |
| [POOL-BOOK](#pool-book) | D9-02 | `booking-service` | đánh giá | OPEN — thiếu hook và đầu dò Hikari |
| [DB-BOOK-DOWN](#db-book-down) | D9-02 | `booking_db` | đánh giá | OPEN — chưa có cách cô lập DB logic trong cấu hình hiện tại |
| [REDIS-BOOK](#redis-book) | D9-03 | `booking-service → cache` (data) | phát triển | OPEN — chưa có proxy riêng Booking |
| [REDIS-GW](#redis-gw) | D9-03 | `api-gateway → cache` (data) | đánh giá | OPEN — chưa có proxy riêng Gateway |
| [TICKET-PAUSE](#ticket-pause) | D9-04 | `ticket-service` | đánh giá | OPEN — chưa có tải phát vé sạch và probe liveness tách kênh |
| [HTTP5-EVENT](#http5-event) | D9-05 | `event-service` | phát triển | OPEN — thiếu cờ theo thao tác |
| [HTTP5-BOOK](#http5-book) | D9-05 | `booking-service` | đánh giá | OPEN — thiếu cờ theo thao tác |
| [SLOW-BOOK](#slow-book) | D9-06 | `booking-service` | phát triển | OPEN — thiếu cờ trễ và mốc đo riêng |
| [SLOW-EVENT](#slow-event) | D9-06 | `event-service` | đánh giá | OPEN — thiếu cờ trễ và mốc đo riêng |
| [NET-GW-BOOK](#net-gw-book) | D9-07 | `api-gateway → booking-service` (http) | phát triển | OPEN — host network dùng chung, chưa cô lập được egress |
| [NET-GW-EVENT](#net-gw-event) | D9-07 | `api-gateway → event-service` (http) | đánh giá | OPEN — host network dùng chung, chưa cô lập được egress |
| [NET-PAY-BOOK](#net-pay-book) | D9-07 | `payment-service → booking-service` (http) | đánh giá | OPEN — host network dùng chung, chưa cô lập được egress |
| [CPU-BOOK](#cpu-book) | D9-08 | `booking-service` | phát triển | OPEN — không có quota CPU riêng hoặc phép xác nhận stress ARM |
| [CPU-EVENT](#cpu-event) | D9-08 | `event-service` | đánh giá | OPEN — không có quota CPU riêng hoặc phép xác nhận stress ARM |
| [VNPAY-REFUND-LAT](#vnpay-refund-lat) | D9-09 | `payment-service → vnpay` (external-http) | đánh giá | OPEN — đích hiện tại là placeholder, thiếu mock/fixture refund |
| [SAGA-TICKET-FAIL](#saga-ticket-fail) | D9-10 | `ticket-service` | đánh giá | OPEN — thiếu hook terminal và đường thanh toán thử khép kín |
| [FLASH-HEALTHY](#flash-healthy) | D9-11 | `root = null` | phát triển + đối chứng đánh giá riêng | OPEN — thiếu hồ sơ tốc độ backend và ngưỡng khỏe đã khóa |

**POOL-EVENT (CANDIDATE).** Pool Hikari riêng được khai trong mã, GET event đọc event_db. Hook giữ connection đúng pool Event, chờ acquire độc lập khi DB/proxy khỏe, hồi phục sau nhả. Sau khi có thiết kế và phép kiểm, Minh mới quyết đưa vào ô phát triển. Minh (2i), chủ Event. [G-route](#g-route), [E-event](#e-event), [E-read](#e-read), [E-db](#e-db), [E-db-config](#e-db-config)

## Chi tiết từng ô

Các tham chiếu mã trỏ đến file, dòng và commit ở [bảng mã](#bảng-mã-theo-revision). Probe độc lập thuộc bộ thử/ledger. Các giá trị đo để trống tới khi có lượt.

### DB-BOOK-LAT

- **Thao tác tải.** GET /api/v1/orders/{orderId} với chủ đơn hợp lệ; tạo fixture trước pha. Có thể dùng availability cache miss làm phụ, không dùng cache hit để xác nhận.
- **Chiều gọi.** booking-service → booking_db, JDBC tới PostgreSQL; qua một cổng proxy riêng của Booking ở cả nền và lỗi.
- **Mã và revision.** [B-db](#b-db), [B-order](#b-order), [B-read](#b-read).
- **Vị trí tiêm.** Tuyến JDBC Booking, không ở pool hoặc tiến trình PostgreSQL.
- **Cơ chế dự định.** Toxiproxy trì hoãn một chiều cố định của luồng phản hồi TCP từ upstream. Cường độ dưới ngưỡng làm biến thành timeout trong phép đo thuần trễ.
- **Đầu dò độc lập.** Đo JDBC trước/sau qua cùng proxy và từ đường trực tiếp tới booking_db bằng client riêng; bằng chứng flow/cổng ghi byte của kết nối JVM; kiểm chờ lấy connection và SQL server bằng đầu dò riêng, thêm đối chứng event_db.
- **Điều kiện xác nhận.** JVM đi qua proxy, chỉ đường qua proxy tăng RTT truy vấn với cùng truy vấn; kết nối trực tiếp và SQL phía server trong dải nền; không cạn Hikari.
- **Khi chưa xác nhận.** JVM đi thẳng, cả hai đường cùng chậm, SQL server/pool đã suy giảm, hoặc chưa đo độ trễ thật. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `booking-service → booking_db` (data). Tập chấp nhận chung `booking-service`, `booking_db`. Ô chia là `booking-service→booking_db` × `D9-01`. Đợt đánh giá. OPEN — tuyến JDBC tách riêng.
- **Định vị cạnh.** booking-service → booking_db [data]; gán địa chỉ proxy về DB logic, có version.
- **Kiểm điều gì.** Bài học 1 và cạnh dữ liệu. Giả thuyết đồ thị (chưa kiểm) — Cạnh JDBC có thể giúp định vị tuyến chậm khi giữ được caller/đích và thời gian xử lý phía DB.
- **Đáp án telemetry có thể phân biệt.** OPEN. JDBC CLIENT hoặc latency của Booking và endpoint tăng. Span client có thể gộp truyền và xử lý DB. Tách với SQL chậm cần thời gian server/pool; bản P7 giữ span thuộc Booking. R-02/03/05, KP-09/17.
- **Phần việc và người xử lý.** 2i-A: BOOKING_DB_URL qua listener riêng, giữ role/schema, fixture order đọc được, kiểm hai đường và không đổi các URL DB khác. Minh (hạ tầng/2i), chủ Booking.

### EVENT-DB-LAT

- **Thao tác tải.** GET /api/v1/events/{id} với fixture PUBLISHED. Route phải vào Event và EventRepository.find phải đọc DB trong lượt.
- **Chiều gọi.** api-gateway → event-service → event_db qua JDBC; đích PostgreSQL dùng chung với Booking.
- **Mã và revision.** [G-route](#g-route), [E-event](#e-event), [E-read](#e-read), [E-db](#e-db), [E-db-config](#e-db-config).
- **Vị trí tiêm.** Listener Toxiproxy riêng của đường EVENT_DB_URL, nằm trong topology cố định cả chiến dịch.
- **Cơ chế dự định.** Thêm trễ phản hồi TCP trên đường JDBC riêng của Event, cùng cơ chế với DB-BOOK-LAT. B4 chọn cường độ thuần trễ trong biên timeout.
- **Đầu dò độc lập.** Đối chiếu kết nối và byte JVM Event trên listener; so RTT qua proxy và đường JDBC trực tiếp tới event_db bằng truy vấn đọc cùng loại. Kiểm riêng SQL phía DB, chờ acquire Hikari và đường Booking đối chứng.
- **Điều kiện xác nhận.** Lượt GET thực dùng listener Event. Chỉ đường qua proxy tăng RTT; đường trực tiếp, pool, SQL phía DB và đường Booking giữ dải nền. Kiểm lại sau bỏ trễ.
- **Khi chưa xác nhận.** GET chưa đến Event, Event không đi proxy, đường trực tiếp hoặc Booking cũng suy giảm, hoặc trễ chỉ do SQL, pool hoặc timeout. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `event-service → event_db` (data). Tập chấp nhận chung `event-service`, `event_db`. Ô chia là `event-service→event_db` × `D9-01`. Đợt phát triển. OPEN — tuyến JDBC tách riêng.
- **Định vị cạnh.** event-service → event_db [data]; ánh xạ listener Event sang DB logic theo R-10.
- **Kiểm điều gì.** Bài học 1 và cạnh dữ liệu. Giả thuyết đồ thị (chưa kiểm) — Cạnh JDBC có thể giúp định vị tuyến chậm khi giữ được caller/đích và thời gian xử lý phía DB.
- **Đáp án telemetry có thể phân biệt.** OPEN. JDBC CLIENT span và GET event có thể tăng latency. Span client có thể gộp đường mạng với thời gian xử lý SQL. Cần tín hiệu pool/DB và binding để phân biệt. R-02/03/05/10, KP-09/17.
- **Phần việc và người xử lý.** 2i-A: giữ role/schema và thay EVENT_DB_URL trong môi trường thử để dùng listener riêng suốt chiến dịch. Giữ đường JDBC trực tiếp cho đầu dò, có fixture PUBLISHED. Minh (hạ tầng/2i), chủ Event.

### POOL-BOOK

- **Thao tác tải.** Các GET đơn hợp lệ chạy đều; hook thử nghiệm chiếm connection trên đúng datasource Booking, trước pha xác nhận tải vẫn vào GET.
- **Chiều gọi.** GET → Booking → hàng đợi lấy connection Hikari trong Booking → booking_db.
- **Mã và revision.** [B-db](#b-db), [B-order](#b-order), [B-read](#b-read).
- **Vị trí tiêm.** Pool Hikari của booking-service; chiếm connection có giới hạn, không giữ khóa bảng/hàng và có tự nhả.
- **Cơ chế dự định.** Cờ giữ các connection rảnh của cùng pool đủ để request chờ acquire. Phân biệt cạn pool với pool cố tạo lại kết nối do DB mất.
- **Đầu dò độc lập.** JMX/kiểm thử riêng đọc Active/Idle/Total/ThreadsAwaiting và thời gian acquire, đo SELECT riêng qua proxy và trực tiếp, DB không lock/wait bất thường.
- **Điều kiện xác nhận.** Active=Total=maximum hiệu lực, Idle=0 và có request chờ acquire; đường qua proxy, truy vấn độc lập và DB khỏe; sau nhả, hàng đợi tan và GET phục hồi.
- **Khi chưa xác nhận.** Chỉ giảm cấu hình max, chỉ thấy timeout, không có pending, hoặc DB/proxy cũng không khỏe. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `booking-service`. Tập chấp nhận chung không áp dụng. Ô chia là `booking-service` × `D9-02-pool`. Đợt đánh giá. OPEN — thiếu hook và đầu dò Hikari.
- **Định vị cạnh.** Không áp dụng. Pool là vị trí tiêm nội bộ, Booking là nút chiếu.
- **Kiểm điều gì.** Bài học 2, phân biệt pool và DB đích. Giả thuyết đồ thị (chưa kiểm) — Tín hiệu trực tiếp ở pool hoặc DB có thể đủ. Cạnh hỗ trợ định vị nếu chỉ thấy lỗi từ caller.
- **Đáp án telemetry có thể phân biệt.** OPEN. Booking server span chậm, có thể ít/không có JDBC span cho request chờ; thiếu pool gauge/acquire làm khó phân biệt lỗi đường DB. R-02/03/06, KP-09/17.
- **Phần việc và người xử lý.** 2i-B: hook dùng datasource thật và lease tự nhả, quyền quản trị môi trường thử; đầu dò pool tách khỏi tín hiệu RCA, xuất metric pool vận hành riêng nếu cần. Minh (2i), chủ Booking.

### DB-BOOK-DOWN

- **Thao tác tải.** GET đơn hợp lệ trong lúc DB logic booking_db được làm mất khả dụng có kiểm soát trên môi trường thử.
- **Chiều gọi.** Booking và client kiểm trực tiếp → booking_db. Client đối chứng → event_db/payment_db.
- **Mã và revision.** [B-db](#b-db), [B-order](#b-order), [B-read](#b-read), [H-net](#h-net).
- **Vị trí tiêm.** Tại đích booking_db, gồm đường vào qua proxy và đường trực tiếp. PostgreSQL hiện dùng chung; dừng container chung sẽ làm đổi phạm vi root.
- **Cơ chế dự định.** CANDIDATE: làm DB logic thử nghiệm mất khả dụng cho tất cả client, gồm các phiên đang dùng; hoặc dựng DB thử cô lập, khai topology và đối chứng. Toxiproxy cắt một tuyến là ứng viên lỗi đường, chưa đủ để gọi là mất DB.
- **Đầu dò độc lập.** Probe truy vấn qua proxy, probe DB trực tiếp bỏ qua proxy và bằng chứng từ đích DB; kiểm event_db/payment_db cùng lúc, trạng thái pool chỉ đo triệu chứng.
- **Điều kiện xác nhận.** Hai đường tới booking_db đều hỏng do DB đích, gồm phiên cũ và kết nối mới, trong khi DB đối chứng khỏe; kiểm phục hồi tại đích và GET.
- **Khi chưa xác nhận.** Chỉ proxy/JVM mất kết nối, chỉ phiên mới bị chặn trong khi request qua phiên cũ vẫn chạy, hay toàn PostgreSQL dùng chung dừng. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `booking_db`. Tập chấp nhận chung không áp dụng. Ô chia là `booking_db` × `D9-02-database`. Đợt đánh giá. OPEN — chưa có cách cô lập DB logic trong cấu hình hiện tại.
- **Định vị cạnh.** Không áp dụng. booking-service → booking_db là cạnh biểu hiện, cần tách khỏi vị trí DB đích.
- **Kiểm điều gì.** Bài học 2, phân biệt pool và DB đích. Giả thuyết đồ thị (chưa kiểm) — Tín hiệu trực tiếp ở pool hoặc DB có thể đủ. Cạnh hỗ trợ định vị nếu chỉ thấy lỗi từ caller.
- **Đáp án telemetry có thể phân biệt.** OPEN. JDBC error/timeout, có thể timeout lấy connection sau đó. R-03/05 và KP-09/17 thiếu tín hiệu đích theo DB logic nên RCA có thể chỉ thấy Booking/cạnh.
- **Phần việc và người xử lý.** 2i-A: đường proxy và đường trực tiếp theo DB logic. B4 chọn cách cô lập DB và chứng minh giữ phạm vi trước khi dùng ô. Minh (hạ tầng/B4); chủ Booking kiểm kịch bản GET.

### REDIS-BOOK

- **Thao tác tải.** GET /api/v1/events/{eventId}/availability, TTL cache dương và event đã seed. Giữ tỷ lệ hit/miss hoặc phân tầng; lấy GET cache hit làm nhánh xác nhận thuần Redis.
- **Chiều gọi.** api-gateway → booking-service → cache. Rate limiter của gateway cũng có cạnh cache khác.
- **Mã và revision.** [B-av](#b-av), [B-cache](#b-cache), [B-redis](#b-redis), [B-stock](#b-stock), [G-route](#g-route).
- **Vị trí tiêm.** Tuyến Redis của Booking trên listener riêng, không tác động listener gateway hoặc Redis chung.
- **Cơ chế dự định.** Đưa trễ phản hồi Redis vào proxy Booking; dưới timeout cho nhánh thuần trễ. Fallback DB khi lỗi Redis là dấu hiệu khác cần ghi riêng.
- **Đầu dò độc lập.** Probe Redis TCP/GET qua cổng Booking và cổng gateway/đích, đối chiếu flow JVM Booking tới cổng riêng và delta lệnh trên Redis. k6 đo availability, GET event làm đối chứng.
- **Điều kiện xác nhận.** GET của Booking đi qua proxy, RTT chỉ tăng trên tuyến Booking; trực tiếp và gateway khỏe; ghi trạng thái hit/miss.
- **Khi chưa xác nhận.** TTL tắt, không có lệnh thật, trễ ở cả gateway và Booking, hoặc timeout làm đổi cơ chế cần kiểm. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `booking-service → cache` (data). Tập chấp nhận chung `booking-service`, `cache`. Ô chia là `booking-service→cache` × `D9-03`. Đợt phát triển. OPEN — chưa có proxy riêng Booking.
- **Định vị cạnh.** booking-service → cache [data]; ánh xạ host/port proxy Booking và Redis logic.
- **Kiểm điều gì.** Cạnh dữ liệu tới cache. Giả thuyết đồ thị (chưa kiểm) — Cạnh Redis có thể giúp phân biệt caller và DB fallback nếu giữ được định danh tuyến.
- **Đáp án telemetry có thể phân biệt.** OPEN. Redis CLIENT latency; Booking chậm, có thể tăng JDBC khi fallback. KP-05 có span sau chỉnh config; R-03/06 và KP-09 chưa chứng minh phân biệt hết tuyến/DB fallback.
- **Phần việc và người xử lý.** 2i-A: REDIS_HOST/PORT riêng cho Booking, proxy luôn có trong nền, giữ TTL dương; kiểm bằng cổng và thao tác GET thật. Minh (2i/hạ tầng), chủ Booking.

### REDIS-GW

- **Thao tác tải.** GET /api/v1/events/{id} qua route event có RequestRateLimiter, dưới quota. Dùng HTTP trực tiếp tới Event như đối chứng trong môi trường thử.
- **Chiều gọi.** api-gateway → cache ở bộ giới hạn tốc độ trước khi chuyển sang event-service.
- **Mã và revision.** [G-route](#g-route), [G-limit](#g-limit), [E-event](#e-event).
- **Vị trí tiêm.** Đường Redis của gateway tách cổng khỏi Booking.
- **Cơ chế dự định.** Trễ Redis trên cổng gateway, giữ Event và Redis server bình thường.
- **Đầu dò độc lập.** Probe trên cổng Redis gateway và Booking/direct; ghi lệnh rate limiter của đúng lượt và delta RTT, k6/đầu dò so gateway với Event trực tiếp.
- **Điều kiện xác nhận.** Tuyến Redis gateway tăng RTT, Event trực tiếp và tuyến Booking khỏe; request thực sự qua limiter và vẫn tới Event ở cường độ thuần trễ.
- **Khi chưa xác nhận.** Chỉ có route cấu hình, test gọi callback không đi qua limiter, request bị 429 từ quota hoặc các đường khác cũng bị ảnh hưởng. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `api-gateway → cache` (data). Tập chấp nhận chung `api-gateway`, `cache`. Ô chia là `api-gateway→cache` × `D9-03`. Đợt đánh giá. OPEN — chưa có proxy riêng Gateway.
- **Định vị cạnh.** api-gateway → cache [data]; cổng proxy khác với REDIS-BOOK.
- **Kiểm điều gì.** Cạnh dữ liệu tới cache. Giả thuyết đồ thị (chưa kiểm) — Cạnh Redis có thể giúp phân biệt caller và DB fallback nếu giữ được định danh tuyến.
- **Đáp án telemetry có thể phân biệt.** OPEN. Redis CLIENT ở gateway chậm trước HTTP downstream; latency tuyến người dùng có thể gộp limiter và service nếu thiếu cạnh. R-01/02/03; KP-05/15.
- **Phần việc và người xử lý.** 2i-A: cấu hình REDIS_HOST/PORT gateway độc lập; giữ xác thực và quota, dùng route event thường. Minh (2i/hạ tầng), chủ gateway.

### TICKET-PAUSE

- **Thao tác tải.** Tạo đơn, tạo attempt, mock IPN hợp lệ để Payment chấp nhận và gửi ticket.issue.v1. Poll GET /api/v1/orders/{orderId}/tickets; gửi đợt mới trong pha pause.
- **Chiều gọi.** Payment → broker → ticket.issuance.q → ticket-service; gateway → Ticket khi hỏi vé.
- **Mã và revision.** [G-route](#g-route), [P-pay](#p-pay), [P-ipn](#p-ipn), [P-saga](#p-saga), [B-accept](#b-accept), [T-listen](#t-listen), [T-queue](#t-queue), [T-api](#t-api), [T-bind](#t-bind).
- **Vị trí tiêm.** Container Ticket chạy listener; pause toàn container, cả HTTP và worker Ticket.
- **Cơ chế dự định.** Pumba pause trên đích ARM ở B4. Thông điệp vẫn vào broker trong pha pause, consumer không thực thi.
- **Đầu dò độc lập.** Docker State.Paused và identity container; broker management riêng đếm publish/deliver/ack, ready/unacked và độ tuổi message; k6 và poll trạng thái Ticket.
- **Điều kiện xác nhận.** Đúng container paused; broker khỏe và lệnh hợp lệ đến queue đích, ACK không tiến hoặc backlog tích lũy. Sau unpause consumer xử lý, độ trễ drain ghi riêng.
- **Khi chưa xác nhận.** Container paused nhưng không có message đủ điều kiện; broker ngừng nhận, đã ACK trước pha hoặc probe Ticket 403 do xác thực. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `ticket-service`. Tập chấp nhận chung không áp dụng. Ô chia là `ticket-service` × `D9-04`. Đợt đánh giá. OPEN — chưa có tải phát vé sạch và probe liveness tách kênh.
- **Định vị cạnh.** Không áp dụng. Broker → Ticket là tuyến quan sát, root thật là container Ticket.
- **Kiểm điều gì.** Bài học 5 và cạnh thông điệp. Giả thuyết đồ thị (chưa kiểm) — Cạnh MQ có thể hỗ trợ khi consumer im lặng và có bằng chứng queue độc lập.
- **Đáp án telemetry có thể phân biệt.** OPEN. Queue ready/unacked, publisher còn, consumer/ticket HTTP có thể im. KP-10 từng thấy pause Event làm M1 P7 mất kênh của root; cần đo với Ticket. R-04/06/08/09, KP-06/07/19.
- **Phần việc và người xử lý.** 2i-C: fixture thanh toán/issue thành công; B4 kiểm Pumba ARM, queue và health/liveness thông thường không mang cờ pause vào RCA. Minh (2i/B4), chủ Payment/Ticket.

### HTTP5-EVENT

- **Thao tác tải.** GET /api/v1/events/{id} với event PUBLISHED qua gateway
- **Chiều gọi.** api-gateway → event-service; nhánh lỗi kết thúc trong Event trước đọc DB.
- **Mã và revision.** [G-route](#g-route), [E-event](#e-event), [E-read](#e-read), [E-db](#e-db).
- **Vị trí tiêm.** EventController.publicEvent trước service.readPublic.
- **Cơ chế dự định.** Cờ thử nghiệm làm chính thao tác trả HTTP 5xx. Bật sau khi kịch bản baseline và điều kiện vào hợp lệ đã được kiểm. Không đổi DB, mạng hoặc pool.
- **Đầu dò độc lập.** Audit riêng xác nhận cờ, số lần hook vào nhánh, đối chiếu k6 trực tiếp và qua gateway với cùng fixture; kiểm response do origin phát và ghi mã fallback nếu gateway đổi mã.
- **Điều kiện xác nhận.** Hook hoạt động trên đúng request và origin sinh 5xx; tắt cờ cùng dữ liệu trả kết quả nghiệp vụ bình thường; route ngoài phạm vi còn khỏe.
- **Khi chưa xác nhận.** Chỉ thấy gateway 5xx, token/fixture sai, hoặc origin chưa đi vào hook. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `event-service`. Tập chấp nhận chung không áp dụng. Ô chia là `event-service` × `D9-05`. Đợt phát triển. OPEN — thiếu cờ theo thao tác.
- **Định vị cạnh.** Không áp dụng.
- **Kiểm điều gì.** Bài học 2, lỗi mã nguồn. Giả thuyết đồ thị (chưa kiểm) — 5xx ở origin là tín hiệu trực tiếp. Đây là đối chứng nơi cạnh có thể ít giúp.
- **Đáp án telemetry có thể phân biệt.** OPEN. Event SERVER error và tần suất lỗi; gateway có thể sinh fallback/circuit breaker. Lỗi có thể rõ qua trace/log dù CPU ít đổi. R-01/02/06, KP-08/15/19.
- **Phần việc và người xử lý.** 2i-B: hook lỗi tách khỏi hook trễ, áp đúng thao tác, audit riêng và trả lỗi có thể kiểm ở origin. Minh (2i), chủ Event.

### HTTP5-BOOK

- **Thao tác tải.** GET /api/v1/orders/{orderId}, token của chủ đơn và fixture tồn tại
- **Chiều gọi.** api-gateway → booking-service; nhánh lỗi kết thúc trong Booking trước đọc DB.
- **Mã và revision.** [G-route](#g-route), [B-order](#b-order), [B-read](#b-read).
- **Vị trí tiêm.** OrderController.getOrder trước orderService.getOrder.
- **Cơ chế dự định.** Cờ thử nghiệm làm chính thao tác trả HTTP 5xx. Bật sau khi kịch bản baseline và điều kiện vào hợp lệ đã được kiểm. Không đổi DB, mạng hoặc pool.
- **Đầu dò độc lập.** Audit riêng xác nhận cờ, số lần hook vào nhánh, đối chiếu k6 trực tiếp và qua gateway với cùng fixture; kiểm response do origin phát và ghi mã fallback nếu gateway đổi mã.
- **Điều kiện xác nhận.** Hook hoạt động trên đúng request và origin sinh 5xx; tắt cờ cùng dữ liệu trả kết quả nghiệp vụ bình thường; route ngoài phạm vi còn khỏe.
- **Khi chưa xác nhận.** Chỉ thấy gateway 5xx, token/fixture sai, hoặc origin chưa đi vào hook. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `booking-service`. Tập chấp nhận chung không áp dụng. Ô chia là `booking-service` × `D9-05`. Đợt đánh giá. OPEN — thiếu cờ theo thao tác.
- **Định vị cạnh.** Không áp dụng.
- **Kiểm điều gì.** Bài học 2, lỗi mã nguồn. Giả thuyết đồ thị (chưa kiểm) — 5xx ở origin là tín hiệu trực tiếp. Đây là đối chứng nơi cạnh có thể ít giúp.
- **Đáp án telemetry có thể phân biệt.** OPEN. Booking SERVER error và tần suất lỗi; gateway có thể sinh fallback/circuit breaker. Lỗi có thể rõ qua trace/log dù CPU ít đổi. R-01/02/06, KP-08/15/19.
- **Phần việc và người xử lý.** 2i-B: hook lỗi tách khỏi hook trễ, áp đúng thao tác, audit riêng và trả lỗi có thể kiểm ở origin. Minh (2i), chủ Booking.

### SLOW-BOOK

- **Thao tác tải.** GET /api/v1/orders/{orderId}, token của chủ đơn và fixture tồn tại
- **Chiều gọi.** api-gateway → booking-service → booking_db khi qua phần trì hoãn.
- **Mã và revision.** [G-route](#g-route), [B-order](#b-order), [B-read](#b-read).
- **Vị trí tiêm.** OrderController.getOrder trước khi vào transaction của orderService.getOrder.
- **Cơ chế dự định.** Chèn trễ định lượng trong xử lý request, trước acquire DB. Chọn biên dưới timeout để vẫn hoàn tất đúng nghiệp vụ và duy trì pool/mạng khỏe.
- **Đầu dò độc lập.** Đồng hồ monotonic ở hook ghi riêng thời gian chờ thực, k6 kiểm latency và payload; probe đường mạng và JDBC riêng.
- **Điều kiện xác nhận.** Hook trễ trên đúng request, chênh lệch xuất hiện ở cả origin và gateway, trạng thái đáp ứng đúng, DB/pool/mạng không suy giảm độc lập.
- **Khi chưa xác nhận.** Chỉ thấy HTTP chậm, hook không được chạy, trễ không giữ biên timeout hoặc pool/mạng/DB đồng thời suy giảm. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `booking-service`. Tập chấp nhận chung không áp dụng. Ô chia là `booking-service` × `D9-06`. Đợt phát triển. OPEN — thiếu cờ trễ và mốc đo riêng.
- **Định vị cạnh.** Không áp dụng.
- **Kiểm điều gì.** Đối chứng với trễ đường JDBC. Giả thuyết đồ thị (chưa kiểm) — Tín hiệu nội bộ có thể đủ khi phân biệt được phần thời gian xử lý với phần chờ downstream.
- **Đáp án telemetry có thể phân biệt.** OPEN. Booking SERVER tăng latency nội bộ. JDBC child không chậm tương ứng. Nếu thiếu kind/operation/độ phủ span, có thể nhầm với trễ cạnh. R-01/02/03/06.
- **Phần việc và người xử lý.** 2i-B: hook chậm có TTL và thời gian thật ngoài RCA; không ngủ trong khi giữ lock/connection. Giữ một lỗi dev ở hai mức tải. Minh (2i), chủ Booking.

### SLOW-EVENT

- **Thao tác tải.** GET /api/v1/events/{id} với event PUBLISHED qua gateway
- **Chiều gọi.** api-gateway → event-service → event_db khi qua phần trì hoãn.
- **Mã và revision.** [G-route](#g-route), [E-event](#e-event), [E-read](#e-read), [E-db](#e-db).
- **Vị trí tiêm.** EventController.publicEvent trước khi vào transaction của service.readPublic.
- **Cơ chế dự định.** Chèn trễ định lượng trong xử lý request, trước acquire DB. Chọn biên dưới timeout để vẫn hoàn tất đúng nghiệp vụ và duy trì pool/mạng khỏe.
- **Đầu dò độc lập.** Đồng hồ monotonic ở hook ghi riêng thời gian chờ thực, k6 kiểm latency và payload; probe đường mạng và JDBC riêng.
- **Điều kiện xác nhận.** Hook trễ trên đúng request, chênh lệch xuất hiện ở cả origin và gateway, trạng thái đáp ứng đúng, DB/pool/mạng không suy giảm độc lập.
- **Khi chưa xác nhận.** Chỉ thấy HTTP chậm, hook không được chạy, trễ không giữ biên timeout hoặc pool/mạng/DB đồng thời suy giảm. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `event-service`. Tập chấp nhận chung không áp dụng. Ô chia là `event-service` × `D9-06`. Đợt đánh giá. OPEN — thiếu cờ trễ và mốc đo riêng.
- **Định vị cạnh.** Không áp dụng.
- **Kiểm điều gì.** Đối chứng với trễ đường JDBC. Giả thuyết đồ thị (chưa kiểm) — Tín hiệu nội bộ có thể đủ khi phân biệt được phần thời gian xử lý với phần chờ downstream.
- **Đáp án telemetry có thể phân biệt.** OPEN. Event SERVER tăng latency nội bộ. JDBC child không chậm tương ứng. Nếu thiếu kind/operation/độ phủ span, có thể nhầm với trễ cạnh. R-01/02/03/06.
- **Phần việc và người xử lý.** 2i-B: hook chậm có TTL và thời gian thật ngoài RCA; không ngủ trong khi giữ lock/connection. Giữ một lỗi dev ở hai mức tải. Minh (2i), chủ Event.

### NET-GW-BOOK

- **Thao tác tải.** GET /api/v1/orders/{orderId}, token của chủ đơn và fixture tồn tại
- **Chiều gọi.** api-gateway → booking-service, HTTP đích 8082/tcp trên exp-app.
- **Mã và revision.** [G-route](#g-route), [B-order](#b-order), [B-read](#b-read), [H-net](#h-net).
- **Vị trí tiêm.** Egress của api-gateway tới đúng đích booking-service:8082, trong namespace cô lập hoặc đường thử tương đương; không áp cả host/loopback.
- **Cơ chế dự định.** Trễ mạng có hướng bằng netem/Pumba sau khi chứng minh scope. Dùng cùng topology trong nền, lỗi và hồi phục.
- **Đầu dò độc lập.** Đọc bộ đếm lớp lọc netem, timing/capture TCP độc lập qua đúng tuyến; so thời gian server và các tuyến đối chứng GET event qua cùng gateway và trực tiếp Booking.
- **Điều kiện xác nhận.** Flow thao tác khớp caller, đích và bộ lọc, RTT tăng trong pha; server xử lý gần nền; đường đối chứng và đường quan sát không trễ.
- **Khi chưa xác nhận.** Chỉ có NET_ADMIN, chưa thấy traffic trúng bộ lọc, trễ cả host/đích khác, hoặc downstream xử lý chậm thật. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `api-gateway → booking-service` (http). Tập chấp nhận chung `api-gateway`, `booking-service`. Ô chia là `api-gateway→booking-service` × `D9-07`. Đợt phát triển. OPEN — host network dùng chung, chưa cô lập được egress.
- **Định vị cạnh.** api-gateway → booking-service [http]; xác minh cặp CLIENT/SERVER, route, caller thật và binding theo revision.
- **Kiểm điều gì.** Bài học 1, trễ liên dịch vụ. Giả thuyết đồ thị (chưa kiểm) — Cặp CLIENT/SERVER và tuyến có hướng có thể giúp phân biệt trễ mạng với chậm origin.
- **Đáp án telemetry có thể phân biệt.** OPEN. CLIENT round-trip tăng, SERVER tại đích gần nền; gộp timeout, retry hoặc circuit breaker có thể làm mất cặp. Địa chỉ 127.0.0.1 chung chưa phân biệt được caller. R-01/02/05/08/10.
- **Phần việc và người xử lý.** 2i-D: cấp NET_ADMIN tối thiểu cho thành phần thử ở namespace riêng; giữ JWT/Eureka/route; kiểm phạm vi theo nguồn và đích. Kiểm target thực được Eureka chọn khi đổi topology. Minh (hạ tầng/2i/B4), chủ hai service theo cạnh.

### NET-GW-EVENT

- **Thao tác tải.** GET /api/v1/events/{id} với event PUBLISHED qua gateway
- **Chiều gọi.** api-gateway → event-service, HTTP đích 8086/tcp trên exp-app.
- **Mã và revision.** [G-route](#g-route), [E-event](#e-event), [E-read](#e-read), [H-net](#h-net), [E-db](#e-db).
- **Vị trí tiêm.** Egress của api-gateway tới đúng đích event-service:8086, trong namespace cô lập hoặc đường thử tương đương; không áp cả host/loopback.
- **Cơ chế dự định.** Trễ mạng có hướng bằng netem/Pumba sau khi chứng minh scope. Dùng cùng topology trong nền, lỗi và hồi phục.
- **Đầu dò độc lập.** Đọc bộ đếm lớp lọc netem, timing/capture TCP độc lập qua đúng tuyến; so thời gian server và các tuyến đối chứng GET đơn/availability qua cùng gateway và Event trực tiếp.
- **Điều kiện xác nhận.** Flow thao tác khớp caller, đích và bộ lọc, RTT tăng trong pha; server xử lý gần nền; đường đối chứng và đường quan sát không trễ.
- **Khi chưa xác nhận.** Chỉ có NET_ADMIN, chưa thấy traffic trúng bộ lọc, trễ cả host/đích khác, hoặc downstream xử lý chậm thật. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `api-gateway → event-service` (http). Tập chấp nhận chung `api-gateway`, `event-service`. Ô chia là `api-gateway→event-service` × `D9-07`. Đợt đánh giá. OPEN — host network dùng chung, chưa cô lập được egress.
- **Định vị cạnh.** api-gateway → event-service [http]; xác minh cặp CLIENT/SERVER, route, caller thật và binding theo revision.
- **Kiểm điều gì.** Bài học 1, trễ liên dịch vụ. Giả thuyết đồ thị (chưa kiểm) — Cặp CLIENT/SERVER và tuyến có hướng có thể giúp phân biệt trễ mạng với chậm origin.
- **Đáp án telemetry có thể phân biệt.** OPEN. CLIENT round-trip tăng, SERVER tại đích gần nền; gộp timeout, retry hoặc circuit breaker có thể làm mất cặp. Địa chỉ 127.0.0.1 chung chưa phân biệt được caller. R-01/02/05/08/10.
- **Phần việc và người xử lý.** 2i-D: cấp NET_ADMIN tối thiểu cho thành phần thử ở namespace riêng; giữ JWT/Eureka/route; kiểm phạm vi theo nguồn và đích. Kiểm target thực được Eureka chọn khi đổi topology. Minh (hạ tầng/2i/B4), chủ hai service theo cạnh.

### NET-PAY-BOOK

- **Thao tác tải.** POST /api/v1/payments với đơn payable, token hợp lệ, client credentials hoạt động và idempotency key mới. Request phải gọi snapshot Booking trước khi trả URL.
- **Chiều gọi.** payment-service → booking-service, HTTP đích 8082/tcp trên exp-app.
- **Mã và revision.** [G-route](#g-route), [P-pay](#p-pay), [P-start](#p-start), [P-snap](#p-snap), [P-env](#p-env), [P-http](#p-http), [B-snap](#b-snap), [H-net](#h-net).
- **Vị trí tiêm.** Egress của payment-service tới đúng đích booking-service:8082, trong namespace cô lập hoặc đường thử tương đương; không áp cả host/loopback.
- **Cơ chế dự định.** Trễ mạng có hướng bằng netem/Pumba sau khi chứng minh scope. Dùng cùng topology trong nền, lỗi và hồi phục.
- **Đầu dò độc lập.** Đọc bộ đếm lớp lọc netem, timing/capture TCP độc lập qua đúng tuyến; so thời gian server và các tuyến đối chứng GET Booking qua gateway và tuyến lấy token Keycloak.
- **Điều kiện xác nhận.** Flow thao tác khớp caller, đích và bộ lọc, RTT tăng trong pha; server xử lý gần nền; đường đối chứng và đường quan sát không trễ.
- **Khi chưa xác nhận.** Chỉ có NET_ADMIN, chưa thấy traffic trúng bộ lọc, trễ cả host/đích khác, hoặc downstream xử lý chậm thật. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `payment-service → booking-service` (http). Tập chấp nhận chung `payment-service`, `booking-service`. Ô chia là `payment-service→booking-service` × `D9-07`. Đợt đánh giá. OPEN — host network dùng chung, chưa cô lập được egress.
- **Định vị cạnh.** payment-service → booking-service [http]; xác minh cặp CLIENT/SERVER, route, caller thật và binding theo revision.
- **Kiểm điều gì.** Bài học 1, trễ liên dịch vụ. Giả thuyết đồ thị (chưa kiểm) — Cặp CLIENT/SERVER và tuyến có hướng có thể giúp phân biệt trễ mạng với chậm origin.
- **Đáp án telemetry có thể phân biệt.** OPEN. CLIENT round-trip tăng, SERVER tại đích gần nền; gộp timeout, retry hoặc circuit breaker có thể làm mất cặp. Địa chỉ 127.0.0.1 chung chưa phân biệt được caller. R-01/02/05/08/10.
- **Phần việc và người xử lý.** 2i-D: cấp NET_ADMIN tối thiểu cho thành phần thử ở namespace riêng; giữ JWT/Eureka/route; kiểm phạm vi theo nguồn và đích. BOOKING_SERVICE_URL đã có, giữ nguyên header/xác thực snapshot khi đổi tuyến. Minh (hạ tầng/2i/B4), chủ hai service theo cạnh.

### CPU-BOOK

- **Thao tác tải.** GET /api/v1/orders/{orderId}, token của chủ đơn và fixture tồn tại
- **Chiều gọi.** k6 → gateway → booking-service; cùng host có các JVM và DB khác.
- **Mã và revision.** [G-route](#g-route), [B-order](#b-order), [B-read](#b-read), [H-net](#h-net).
- **Vị trí tiêm.** Cgroup của booking-service, cùng quota đã định trong cả ba pha.
- **Cơ chế dự định.** Stress CPU thuộc đúng cgroup ở môi trường thử, giữ tài nguyên dư cho host/các cgroup khác. Dùng Pumba stress sau khi kiểm tính khả dụng ARM và phạm vi.
- **Đầu dò độc lập.** Đối chiếu ID cgroup của JVM và worker stress, delta cpu.stat throttling/cpu.pressure và CPU host/cgroup khác qua đầu dò riêng; k6 đo route đích và đối chứng.
- **Điều kiện xác nhận.** Stress thật trong cgroup đích, pressure hoặc throttling tăng so với nền; host còn dư và cgroup khác không bị stress trực tiếp; tắt tải stress thì hồi phục.
- **Khi chưa xác nhận.** Chỉ thấy CPU host/JVM cao; stress worker ở cgroup khác, không giữ cô lập hoặc nhiều service cùng bị stress trực tiếp. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `booking-service`. Tập chấp nhận chung không áp dụng. Ô chia là `booking-service` × `D9-08`. Đợt phát triển. OPEN — không có quota CPU riêng hoặc phép xác nhận stress ARM.
- **Định vị cạnh.** Không áp dụng.
- **Kiểm điều gì.** Bài học 6, các service chung máy. Giả thuyết đồ thị (chưa kiểm) — CPU cgroup có thể đủ khi cô lập được đích. Liên kết host có thể hữu ích nếu ảnh hưởng lan rộng.
- **Đáp án telemetry có thể phân biệt.** OPEN. CPU container/JVM Booking, request latency/throughput có thể đổi. CPU host chung dễ lẫn tài nguyên chia sẻ; không quy theo một host gauge. R-05/07/08/10, KP-04/18.
- **Phần việc và người xử lý.** 2i-D: quota/cgroup cô lập trên compose thử, fixture/tải không tự bão hòa; ghi tool image digest và kiểm ARM ở B4. Minh (hạ tầng/B4), chủ Booking.

### CPU-EVENT

- **Thao tác tải.** GET /api/v1/events/{id} với event PUBLISHED qua gateway
- **Chiều gọi.** k6 → gateway → event-service; cùng host có các JVM và DB khác.
- **Mã và revision.** [G-route](#g-route), [E-event](#e-event), [E-read](#e-read), [H-net](#h-net), [E-db](#e-db).
- **Vị trí tiêm.** Cgroup của event-service, cùng quota đã định trong cả ba pha.
- **Cơ chế dự định.** Stress CPU thuộc đúng cgroup ở môi trường thử, giữ tài nguyên dư cho host/các cgroup khác. Dùng Pumba stress sau khi kiểm tính khả dụng ARM và phạm vi.
- **Đầu dò độc lập.** Đối chiếu ID cgroup của JVM và worker stress, delta cpu.stat throttling/cpu.pressure và CPU host/cgroup khác qua đầu dò riêng; k6 đo route đích và đối chứng.
- **Điều kiện xác nhận.** Stress thật trong cgroup đích, pressure hoặc throttling tăng so với nền; host còn dư và cgroup khác không bị stress trực tiếp; tắt tải stress thì hồi phục.
- **Khi chưa xác nhận.** Chỉ thấy CPU host/JVM cao; stress worker ở cgroup khác, không giữ cô lập hoặc nhiều service cùng bị stress trực tiếp. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `event-service`. Tập chấp nhận chung không áp dụng. Ô chia là `event-service` × `D9-08`. Đợt đánh giá. OPEN — không có quota CPU riêng hoặc phép xác nhận stress ARM.
- **Định vị cạnh.** Không áp dụng.
- **Kiểm điều gì.** Bài học 6, các service chung máy. Giả thuyết đồ thị (chưa kiểm) — CPU cgroup có thể đủ khi cô lập được đích. Liên kết host có thể hữu ích nếu ảnh hưởng lan rộng.
- **Đáp án telemetry có thể phân biệt.** OPEN. CPU container/JVM Event, request latency/throughput có thể đổi. CPU host chung dễ lẫn tài nguyên chia sẻ; không quy theo một host gauge. R-05/07/08/10, KP-04/18.
- **Phần việc và người xử lý.** 2i-D: quota/cgroup cô lập trên compose thử, fixture/tải không tự bão hòa; ghi tool image digest và kiểm ARM ở B4. Minh (hạ tầng/B4), chủ Event.

### VNPAY-REFUND-LAT

- **Thao tác tải.** Tạo giao dịch thu thử hợp lệ. Hủy event fixture đã có charge bằng thao tác admin, để Payment nhận event.cancelled.v1, chọn charge và sinh refund PENDING. Worker send gọi refund. Muốn đo query, dùng fixture có attempt chưa kết thúc tới điều kiện poll và chứng minh một POST query riêng. Tạo URL thanh toán và IPN không kích hoạt cạnh đi ra. Lịch tạo charge và hủy event theo lô fixture, cùng nhịp ở các lượt ghép cặp; mock phải thấy đủ cơ hội gọi trước, trong và sau lỗi.
- **Chiều gọi.** payment-service → vnpay qua HTTP POST từ worker refund hoặc query. Trình duyệt/k6 → trang thanh toán và mock → callback là hai hướng khác.
- **Mã và revision.** [G-route](#g-route), [P-pay](#p-pay), [P-ipn](#p-ipn), [P-start](#p-start), [P-env](#p-env), [P-http](#p-http), [P-worker](#p-worker), [P-refund](#p-refund), [P-vnp](#p-vnp), [E-cancel](#e-cancel), [P-cancel](#p-cancel), [P-refund-select](#p-refund-select).
- **Vị trí tiêm.** Đường VNPAY_API_URL của Payment qua proxy riêng tới mock HTTP cục bộ. Hai loại POST chia sẻ một vị trí.
- **Cơ chế dự định.** Cùng mock HTTP trả contract đúng ở nền và lỗi. Proxy tăng latency phản hồi trong biên timeout hoặc khai riêng nếu muốn đo timeout.
- **Đầu dò độc lập.** Nhật ký mock nằm ngoài RCA ghi loại request, ID thử đã làm mờ, lúc nhận/trả và đối chiếu attempt; probe proxy vs trực tiếp; kiểm trạng thái refund bằng fixture và truy vấn đọc riêng.
- **Điều kiện xác nhận.** Mock thấy POST từ Payment đúng loại, trả được phản hồi hợp lệ; chênh lệch riêng trên tuyến proxy, đúng pha. Muốn gộp cả hai loại cần kiểm từng nhánh. Đếm POST từng loại theo pha; một đợt hủy hết việc trước cửa sổ không đạt tiêu chí độ phủ.
- **Khi chưa xác nhận.** Chỉ có URL/GET checkout/IPN, không có attempt đủ điều kiện, chỉ thấy POST do probe tự gửi, chữ ký mock sai hoặc không chứng minh POST do Payment. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `payment-service → vnpay` (external-http). Tập chấp nhận chung `payment-service`, `vnpay`. Ô chia là `payment-service→vnpay` × `D9-09`. Đợt đánh giá. OPEN — đích hiện tại là placeholder, thiếu mock/fixture refund.
- **Định vị cạnh.** payment-service → vnpay [external-http]; gán mock/proxy đã xác minh về vnpay. Không gán callback vào cạnh này.
- **Kiểm điều gì.** Phụ thuộc ngoài. Giả thuyết đồ thị (chưa kiểm) — Cạnh client đã xác minh có thể giúp định vị đối tác ngoài dù thiếu SERVER span.
- **Đáp án telemetry có thể phân biệt.** OPEN. CLIENT span/payment worker latency, trạng thái refund trễ; không có SERVER span đối tác trong bằng chứng chung. R-01/02/07/09/10, KP-07/16; cần ánh xạ alias và liên kết scheduler/attempt.
- **Phần việc và người xử lý.** 2i-C: mock hoàn tiền và tra cứu có phản hồi ký hợp lệ, mock checkout/IPN tách URL, VNPAY_API_URL qua proxy và tải làm phát sinh refund thật trên fixture; không gọi sandbox/prod. Bàn giao lịch fixture/hủy event và số POST refund/query theo pha; dùng lịch tương ứng ở ca đối chứng. Minh (2i/hạ tầng), chủ Payment.

### SAGA-TICKET-FAIL

- **Thao tác tải.** Đơn hợp lệ, charge qua IPN thử, Booking chấp nhận, Payment ở WAITING_TICKETS. Ticket nhận ticket.issue.v1 cho event không hủy. Cờ làm phát vé kết thúc FAILED trước tạo vé, quan sát bù trừ.
- **Chiều gọi.** Payment → broker → Ticket → broker → Payment → broker → Booking; worker hoàn tiền tới mock nếu kiểm refund terminal.
- **Mã và revision.** [G-route](#g-route), [P-pay](#p-pay), [P-ipn](#p-ipn), [P-saga](#p-saga), [B-accept](#b-accept), [P-consume](#p-consume), [P-binding](#p-binding), [T-listen](#t-listen), [T-queue](#t-queue), [T-issue](#t-issue), [T-result](#t-result), [T-send](#t-send), [B-fail](#b-fail), [B-release](#b-release), [T-api](#t-api), [T-bind](#t-bind).
- **Vị trí tiêm.** TicketService.issue, transaction PENDING ngay trước nhánh tạo vé/QR; dùng hợp đồng FAILED, outbox/inbox hiện có và một mã lỗi thử đã được contract chấp nhận.
- **Cơ chế dự định.** Lỗi terminal của nghiệp vụ phát vé. Giữ idempotency và không tạo vé dở dang; throw exception thường ở listener đi đường retry, hủy event gây cơ chế cạnh tranh.
- **Đầu dò độc lập.** Audit hook độc lập, đọc trạng thái Ticket/Payment/Booking hoặc API riêng bằng ID thử, kiểm mock refund và trạng thái resource; đối chiếu một case thành công và replay message có cùng nghiệp vụ.
- **Điều kiện xác nhận.** Ticket FAILED/0 vé, result được broker chuyển và Payment COMPENSATING/tạo đúng một refund vì TICKET_ISSUANCE_FAILED, Booking xử lý kết quả và trả resource đúng một lần. Phân biệt xác nhận khởi động bù trừ với refund/giải phóng hoàn tất; ghi kết quả và thời điểm mỗi bước.
- **Khi chưa xác nhận.** Chỉ ném lỗi/retry/DLQ, event bị hủy hoặc nhánh refund vì lý do khác, Ticket có vé, không thấy chuyển trạng thái ở Payment/Booking hoặc trùng refund/giải phóng. Hiện tại ghi “can thiệp chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `ticket-service`. Tập chấp nhận chung không áp dụng. Ô chia là `ticket-service` × `D9-10`. Đợt đánh giá. OPEN — thiếu hook terminal và đường thanh toán thử khép kín.
- **Định vị cạnh.** Không áp dụng. Các cạnh message để định vị lan truyền và kiểm cơ chế.
- **Kiểm điều gì.** Luồng bất đồng bộ và bù trừ. Giả thuyết đồ thị (chưa kiểm) — Cạnh message và ngữ cảnh liên kết có thể giúp phân biệt lỗi Ticket với refund/Booking là hậu quả.
- **Đáp án telemetry có thể phân biệt.** OPEN. Span consumer/outbox và lỗi/latency qua nhiều service, API hỏi vé có thể chậm hoặc rỗng; ACK thành công ở vận chuyển không đồng nghĩa phát vé thành công. R-04/06/09, KP-06/07/16/19 cần queue, message/link, outcome và nối thời điểm.
- **Phần việc và người xử lý.** 2i-B/C: terminal hook Ticket và fixture IPN/Booking, mock refund không trễ để tách với D9-09; kiểm contract/inbox/outbox và replay bằng dữ liệu thử. Minh (2i), chủ Ticket, Payment và Booking.

### FLASH-HEALTHY

- **Thao tác tải.** k6 chạy lịch thấp → tăng → plateau → hạ. Giữ hỗn hợp chung của chiến dịch, tỷ trọng và fixture khai trước. Đo tải đến từng backend; tách nhóm quota theo quy tắc tải.
- **Chiều gọi.** k6 → gateway → Event/Booking, rồi Payment/Ticket nếu chạy đủ lát cắt; gateway → Redis cho limiter.
- **Mã và revision.** [G-route](#g-route), [G-limit](#g-limit), [E-event](#e-event), [B-av](#b-av), [B-order](#b-order), [P-pay](#p-pay), [T-api](#t-api).
- **Vị trí tiêm.** Không can thiệp. Điều chỉnh lịch tải ở k6, cùng cấu hình hệ thống, không bật cờ/proxy lỗi.
- **Cơ chế dự định.** Tăng tải hợp lệ nhưng duy trì điều kiện dịch vụ khỏe. Mức tải tạo suy giảm được ghi thành ca tải suy giảm, giữ điều kiện quan sát và root chưa biết nếu chưa có chứng cứ.
- **Đầu dò độc lập.** k6 lưu tải gửi/hoàn thành, dropped_iterations, p95/p99, lỗi/timeout và 429 theo route. Đo độc lập tải đã tới từng backend, kết quả đơn–tồn kho–thanh toán/vé và backlog, OOM/restart, hồi phục. Số đo để chấm nằm ngoài dữ liệu RCA.
- **Điều kiện xác nhận.** Từng backend đạt ngưỡng tốc độ khai trước trong đúng khoảng đo; route chính đạt ngưỡng độc lập về latency, error và backlog; giao dịch đúng, không OOM/restart ngoài dự kiến và phục hồi ổn định. 429 được phân loại theo nguồn và tải thực đến backend.
- **Khi chưa xác nhận.** Chưa khóa ngưỡng, thiếu số đo tải backend hoặc chưa biết nguồn 429. Ca quota dự kiến dưới ngưỡng backend và ca tải làm suy giảm thật được báo ở nhóm riêng; giữ mọi cảnh báo và mẫu số. Hiện tại ghi “ca khỏe chưa xác nhận”. Kết quả đo chưa có.
- **Nhãn và chia đợt.** Root khai trước `root = null`. Tập chấp nhận chung không áp dụng. Đợt phát triển + đối chứng đánh giá riêng. OPEN — thiếu hồ sơ tốc độ backend và ngưỡng khỏe đã khóa.
- **Định vị cạnh.** Không áp dụng. Không tạo nút root cho tải tăng khỏe.
- **Kiểm điều gì.** Báo động giả và câu phụ RQ5. Giả thuyết đồ thị (chưa kiểm) — Kiểm tải tăng khỏe bằng đo độc lập. Lợi thế của cạnh trong phát hiện chưa kiểm.
- **Đáp án telemetry có thể phân biệt.** OPEN. Workload gateway/route tăng, các tín hiệu tỷ lệ lỗi, latency, queue có thể đổi trong giới hạn. Thu đủ dữ liệu để phân biệt retry, throttling và tải vào. R-01/02/05/07/08, KP-04/15/18.
- **Phần việc và người xử lý.** 2i-E: cùng hỗn hợp tải, ngưỡng backend bằng số khai trước, xác minh quota và 429, báo đủ các nhóm kết quả. Minh chốt nếu cần đổi quota trước khi khóa. Minh (tải/NV1/2i), chủ các endpoint trong hồ sơ.

## Đối chiếu yêu cầu quan sát

| Yêu cầu | Phần đã thấy và cần xác nhận |
|---|---|
| R-01 | G-route và kiem-telemetry.md: đã thấy CLIENT/SERVER của availability. Chưa có coverage per route, cặp hoàn chỉnh cho các NET/VNPAY. VNPay chỉ client trong bằng chứng chung. |
| R-02 | Route template mẫu đã thấy. Giữ version ánh xạ GET order/event, availability, snapshot, thao tác worker và listener; thiếu map thao tác runtime đủ cho ô. |
| R-03 | Mẫu JDBC/DB và Redis sau sửa tạm KP-05; DB đích dùng chung. Thiếu bảng logic→instance/host→cổng proxy theo lượt, gauge/acquire Hikari, metric/log chờ SQL đích KP-09/17. Không suy Booking→DB trễ vì DB server. |
| R-04 | Fan-out hủy event đã thấy, vhost đã bổ sung tạm KP-06; thiếu tên queue phía nhận và liên kết ID bao phủ ticket.issue/result/retry. Không dùng ca hủy event thay ca phát vé. |
| R-05 | Định danh host/instance có trong mẫu T-058, chưa xác nhận đủ theo ba tín hiệu. Cùng host cần mapping runtime/cgroup, không gộp hai máy thiết kế T-037 với Oracle. |
| R-06 | Có mẫu nối traceId/spanId, chưa có tỷ lệ theo route/queue. KP-07/08/15/16 hạn chế log nghiệp vụ, gateway chỉ lỗi, payment thiếu trường. KP-19 có lịch sử đứt filelog khi recreate; kiểm end-to-end lại sau thay topology. |
| R-07 | Hồ sơ B4 ghi digest, agent, sampling, đồng hồ/offset, lịch tải, mốc can thiệp theo probe, mốc ảnh hưởng/hồi phục. Cơ chế ledger đã thử ở T-058, chưa có lượt cho các ô trên. |
| R-08 | Cấu hình head parentbased_always_on, metric 10s, Prometheus 48h theo T-058. Đếm agent→Collector tại app→Collector obs→kho→adapter ở tải thấp và dự kiến. Báo drop/retention và clock nguồn, kiểm đủ request–span, MQ/worker theo R-08. KP-18 ghi sự cố kho; KP-10 ghi pause làm mất kênh. |
| R-09 | Phân biệt trace mới ở callback/scheduler/outbox/consumer, link có căn cứ với parent mất khi export. Tách retry khỏi tải mới, nối message/attempt, giữ span cha ngoài cửa sổ dưới dạng thiếu bản ghi. |
| R-10 | Ghim từng image ID/digest, commit và topology đang hiệu lực. Sau khi đổi proxy, mock, cgroup hay deploy, kiểm lại route thật với traffic, alias DB/cache/VNPay và R-01–09. Inventory tĩnh là thiết kế tham chiếu. |

## Chia đợt theo ô

- **Mặc định.** Chia theo (vị trí × họ lỗi), mọi lặp của một ô về một đợt. Bảng là phương án CANDIDATE. M7 vẫn OPEN, không dùng ngoại lệ. Một ô ở vị trí khác trong cùng họ kiểm chuyển vị trí theo họ đó, không đồng nghĩa service chưa từng xuất hiện ở một họ khác.
- **Một vị trí.** D9-04, D9-09, D9-10 để riêng đánh giá. D9-02 gồm hai cơ chế riêng: Pool Booking và DB đích Booking. POOL-EVENT là ứng viên chưa tính ô. D9-01 có Event phát triển và Booking đánh giá. Báo giới hạn phát triển với pool và consumer phát vé.
- **Phát triển.** FLASH-HEALTHY hồ sơ dev, EVENT-DB-LAT, REDIS-BOOK, HTTP5-EVENT, SLOW-BOOK, NET-GW-BOOK, CPU-BOOK khi đạt điều kiện. Dùng SLOW-BOOK (cùng hook/cường độ, cùng topology) ở tải cố định thấp và tải cố định cao hơn còn khỏe để đối chiếu cùng lỗi dưới tải khác. Dùng hồ sơ không lỗi tăng tải và nền dài riêng để hiệu chỉnh ngưỡng. Nếu SLOW-BOOK chưa đạt thì thay bằng một ô dev đủ bằng chứng, ghi trước khi chạy.
- **Đánh giá.** Chỉ lượt mới của ô dành riêng sau khóa bản FlashTicket. Dùng cùng hỗn hợp và topology đã khóa. Chọn trước một tập ô đánh giá đủ điều kiện để chạy ở hai mức tải, giữ cơ chế/cường độ và tách phép so vị trí mới ở tải tham chiếu với phép so đổi tải trong cùng ô. Mọi lần lặp của ô ở đánh giá. FLASH-HEALTHY là đối chứng mới, không dùng lại lượt/dữ liệu để hiệu chỉnh. Báo riêng khả năng lặp trong đợt phát triển.
- **Vị trí chưa tính.** Không đếm stop PostgreSQL chung vào DB Booking, Redis server chung vào một cạnh caller, dừng broker vào consumer Ticket, lỗi QR retry vào Saga terminal, URL/IPN vào cạnh HTTP Payment đi ra. Không mở thêm nhánh service/DB/Saga chỉ để cân số lượng. Kịch bản k6 B4 và các binding cần có bằng chứng trước khi tính ô hữu hiệu.
- **Dự toán.** Số lượt đánh giá = tổng lần lặp ở mức tham chiếu + tổng lần lặp ở mức thứ hai của các ô đã chọn. Tính mỗi lượt bổ sung một chu kỳ và thời gian nền/hồi phục cần thiết. Nếu số lặp bằng nhau thì một ô hai mức cần gấp đôi lượt của ô đó. Dự toán D.9 khoảng 20 ô × 3 là mốc cũ, chưa tính phần bổ sung. Tập ô đủ điều kiện, số lần lặp và thời lượng thực còn OPEN ở B4.

## Pha nền, lỗi và hồi phục

- **Số đã kiểm.** Exp-obs 11:02:07Z: query_range timestamp(metric) bước 5s trên 360s, lấy timestamp nguồn khác nhau. Các chuỗi JVM và docker stats đại diện có 37 timestamp, chênh khoảng 10s. Collector app (docker_stats, hostmetrics, Postgres, Redis, RabbitMQ) và receiver self ở obs đặt 10s. OTEL_METRIC_EXPORT_INTERVAL=10000 ở 5 JVM mục tiêu; trace parentbased_always_on. API Prometheus status/config và targets: scrape self 10s, evaluation mặc định 1m, rules 0. Grafana provisioning GET không có auth trả 401, hold và nhịp rule Grafana thực tế chưa đo.
- **Cửa sổ.** M1 dùng N=[t−300,t), A=[t,t+300); t hoặc t̂ theo chế độ. Lưới bộ đọc T-058 là 15s; RED dùng rate 60s. Mỗi nửa có khoảng 30 cơ hội mẫu nguồn và 20 điểm lưới, không suy đủ mẫu hữu hạn nếu drop/đích im. Mốc cảnh báo đến sau ảnh hưởng có thể làm nửa N chứa dữ liệu bất thường. Giữ lượt chính B1.1; D13 nền lùi chỉ báo cáo khi đủ lịch sử trạng thái, biểu thức và dữ liệu trước mốc, không dùng mốc tiêm để chọn N trong chế độ (b). Bản T-058 gói ±600s và giữ đồng hồ nguồn, m_metric=5 là ngưỡng bản khóa T-058/P7, không coi là số đủ xác nhận telemetry toàn hệ.
- **Nền.** Ứng viên 600s ở tải và topology đã ổn định, có ít nhất 300s sạch sát trước t và 60s lookback RED. Cộng warmup/queue drain nếu cần trước khi bắt đầu tính nền. Flash sale giữ nền thấp ổn định, gắn ramp và plateau riêng trong lịch.
- **Lỗi / plateau.** Ứng viên 600s hiệu lực. Cho cửa sổ +300s từ t0 và từ t̂ nếu t̂−t0 ≤ 300s. Khi luật được khai, kiểm thời gian phát hiện dự kiến D bằng khoảng từ tiêm đến tác động + lookback luật + hold + một nhịp đánh giá + độ trễ thu/chuyển, đo bằng lượt dev. Nếu mục tiêu là trọn nửa A trong lỗi, giữ pha ít nhất 300s + D, hoặc khai giới hạn cửa sổ. Với MQ phải đủ để thấy xử lý thật/backlog; không có t̂ thì giữ ca miss hoặc unsupported theo tình trạng dữ liệu, không thế mốc tiêm vào chế độ b.
- **Hồi phục.** Ứng viên 600s sau ngừng can thiệp/hạ tải. Chỉ chốt sau khi probe độc lập xác nhận route, queue và trạng thái giao dịch đã phục hồi, rồi giữ tối thiểu thêm 300s sạch. Nếu drain/circuit breaker/retry kéo dài hoặc cảnh báo chưa clear, kéo dài hoặc ghi hồi phục chưa xác nhận.
- **Mốc thời gian.** Lưu UTC thời điểm yêu cầu, trạng thái công cụ xác nhận, tác động đầu tiên thấy qua probe, t̂ và hồi phục. Ghi bất định theo độ phân giải/clock offset; probe thuộc ledger. Tính báo động giả bằng đêm nền hoặc ca khỏe độc lập, không dùng đoạn nền bị can thiệp xâm lấn.
- **Còn OPEN.** Interval/hold/lookback của rule Grafana cuối, độ trễ từ nguồn đến kho, phân bố tác động/hồi phục, mức tải khỏe, ngưỡng endpoint, cường độ và chi phí phát triển. 10+10+10 phút là ứng viên khớp quy mô 30 phút của D.9, chưa phải đo thực hoặc thời lượng khóa.

## Bảng mã theo revision

Tất cả đường dẫn dưới đây thuộc repo FlashTicket. Các dòng theo blob tại commit ghi cùng hàng.

| Mã | Commit | Đường dẫn và dòng | Vai trò |
|---|---|---|---|
| <a id="b-db"></a>`B-db` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/resources/application.yaml` dòng 33–40 | BOOKING_DB_URL, Hikari, DB logic booking_db theo cấu hình thực chạy. |
| <a id="b-order"></a>`B-order` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/java/com/flashticket/booking_service/order/controller/OrderController.java` dòng 27–36, 57–64 | GET đơn theo chủ đơn và POST đặt chỗ. |
| <a id="b-read"></a>`B-read` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/java/com/flashticket/booking_service/order/service/impl/OrderServiceImpl.java` dòng 185–196 | Đọc đơn thật qua repository, có transaction chỉ đọc. |
| <a id="b-av"></a>`B-av` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/java/com/flashticket/booking_service/availability/controller/AvailabilityController.java` dòng 14–25 | Route availability vào cache service. |
| <a id="b-cache"></a>`B-cache` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/java/com/flashticket/booking_service/availability/service/AvailabilityCacheService.java` dòng 32–82 | TTL tắt thì bỏ cache. GET generation/payload; miss hoặc lỗi đọc thì dùng DB. |
| <a id="b-redis"></a>`B-redis` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/java/com/flashticket/booking_service/redis/service/RedisService.java` dòng 10–26 | GET, SET thật bằng StringRedisTemplate. |
| <a id="b-stock"></a>`B-stock` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/java/com/flashticket/booking_service/availability/service/impl/AvailabilityServiceImpl.java` dòng 65–89 | Đọc snapshot và tồn kho trong DB khi bỏ cache hoặc cache miss. |
| <a id="b-snap"></a>`B-snap` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/java/com/flashticket/booking_service/order/controller/InternalOrderController.java` dòng 16–27 | POST snapshot nội bộ của Payment. |
| <a id="b-fail"></a>`B-fail` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/java/com/flashticket/booking_service/messaging/BookingIssuanceResultListener.java` dòng 39–47 | Nhận booking.issuance-failed.v1. |
| <a id="b-release"></a>`B-release` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/java/com/flashticket/booking_service/order/service/impl/OrderServiceImpl.java` dòng 429–448 | Trả tài nguyên và ghi ISSUANCE_FAILED khi xác nhận kết quả thất bại. |
| <a id="g-route"></a>`G-route` | `9eea593a14eb50522e7be987b56ad5f0d0c0da72` | `infrastructure/api-gateway/src/main/resources/application.yaml` dòng 12–18, 31–68, 94–104 | Redis gateway. Route callback, payment, ticket, booking và event; các route nghiệp vụ chọn RedisRateLimiter. |
| <a id="g-limit"></a>`G-limit` | `9eea593a14eb50522e7be987b56ad5f0d0c0da72` | `infrastructure/api-gateway/src/main/java/com/flashticket/api_gateway/routing/GatewayRouteConfiguration.java` dòng 14–32 | Bucket 10 token/s, burst 20, 1 token/request, key theo địa chỉ kết nối. |
| <a id="e-event"></a>`E-event` | `9eea593a14eb50522e7be987b56ad5f0d0c0da72` | `services/event-service/src/main/java/com/flashticket/event_service/api/EventController.java` dòng 94–108 | GET chi tiết và danh sách công khai. |
| <a id="e-read"></a>`E-read` | `9eea593a14eb50522e7be987b56ad5f0d0c0da72` | `services/event-service/src/main/java/com/flashticket/event_service/application/EventService.java` dòng 125–130 | Chi tiết đọc repository trong transaction. |
| <a id="p-pay"></a>`P-pay` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/controller/PaymentController.java` dòng 30–72 | POST tạo thanh toán, return/IPN đi vào, GET trạng thái. |
| <a id="p-start"></a>`P-start` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/service/PaymentService.java` dòng 69–85, 129–143, 277–306 | Gọi Booking trước transaction Payment, tạo và trả URL thanh toán. |
| <a id="p-snap"></a>`P-snap` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/client/BookingPurchaseClient.java` dòng 26–41 | POST snapshot qua HTTP, dùng client credentials. |
| <a id="p-env"></a>`P-env` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/resources/application.yaml` dòng 64–74, 84–96 | BOOKING_SERVICE_URL, VNPAY_API_URL, VNPAY_PAYMENT_URL tách nhau. |
| <a id="p-http"></a>`P-http` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/config/PaymentRuntimeConfig.java` dòng 35–49, 70–83 | HTTP client VNPay có base URL/timeout. HTTP client Booking độc lập. |
| <a id="p-worker"></a>`P-worker` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/worker/PaymentWorker.java` dòng 109–139, 144–157 | Worker gửi refund đủ điều kiện và poll attempt đã tới tuổi. |
| <a id="p-refund"></a>`P-refund` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/service/impl/RefundServiceImpl.java` dòng 160–179, 271–298 | Claim PENDING/attempt chưa xong, thực gọi VNPay ngoài transaction, cần giao dịch gốc có vnp_CreateDate. |
| <a id="p-vnp"></a>`P-vnp` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/client/VNPayRefundClient.java` dòng 61–107, 111–116, 138–185 | Hai HTTP POST refund và query, kiểm phản hồi. |
| <a id="p-saga"></a>`P-saga` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/service/impl/PaymentSagaServiceImpl.java` dòng 39–69, 94–117, 135–199 | Phát lệnh Booking chấp nhận thanh toán, phát lệnh issue sau ACCEPTED, nhận FAILED và tạo refund/kết quả cho Booking. |
| <a id="p-consume"></a>`P-consume` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/messaging/PaymentMessageListener.java` dòng 47–62 | Nhận kết quả Ticket, validate rồi chuyển cho Saga. |
| <a id="p-binding"></a>`P-binding` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/config/RabbitMqConfig.java` dòng 51–65 | Binding kết quả phát vé tới queue Payment. |
| <a id="t-listen"></a>`T-listen` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/ticket-service/src/main/java/com/flashticket/ticket_service/messaging/TicketBusinessListeners.java` dòng 54–79 | Listener issue rồi ACK, runtime exception đi đường retry/NACK. |
| <a id="t-queue"></a>`T-queue` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/ticket-service/src/main/resources/application.yaml` dòng 75–87 | Cờ worker/listener và tên queue/routing key. |
| <a id="t-issue"></a>`T-issue` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/ticket-service/src/main/java/com/flashticket/ticket_service/application/TicketService.java` dòng 196–245, 273–309 | Transaction xử lý issue, kết quả terminal FAILED/COMPLETED, outbox và inbox. |
| <a id="t-result"></a>`T-result` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/ticket-service/src/main/java/com/flashticket/ticket_service/contract/TicketSagaMessages.java` dòng 31–45 | Loại message kết quả theo trạng thái. |
| <a id="t-send"></a>`T-send` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/ticket-service/src/main/java/com/flashticket/ticket_service/worker/TicketOutboxPublisher.java` dòng 96–114 | Đưa bản ghi outbox lên broker. |
| <a id="t-api"></a>`T-api` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/ticket-service/src/main/java/com/flashticket/ticket_service/web/TicketApiController.java` dòng 24–34 | GET danh sách vé của đơn để kiểm kết quả từ phía khách. |
| <a id="h-net"></a>`H-net` | `1d40c97076db402d3e0d529a3b48523d37837240` | `deploy/app/_common.yml` dòng 1–17 | Compose checkout dùng host network. Runtime Oracle xác nhận riêng bằng docker inspect. |
| <a id="e-db"></a>`E-db` | `9eea593a14eb50522e7be987b56ad5f0d0c0da72` | `services/event-service/src/main/java/com/flashticket/event_service/persistence/EventRepository.java` dòng 28–39 | Repository đọc event qua SQL trong event_schema. |
| <a id="t-bind"></a>`T-bind` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `deploy/rabbitmq/definitions.json` dòng 517–524 | Thiết kế triển khai trong repo: business.ex → ticket.issuance.q theo ticket.issue.v1. Cần chứng minh binding hiệu lực trong lượt. |
| <a id="e-cancel"></a>`E-cancel` | `9eea593a14eb50522e7be987b56ad5f0d0c0da72` | `services/event-service/src/main/java/com/flashticket/event_service/api/CancellationController.java` dòng 68–81 | Admin hủy event thử với quyền và rowVersion hợp lệ. |
| <a id="p-cancel"></a>`P-cancel` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/messaging/PaymentMessageListener.java` dòng 87–105 | Nhận và ghi nhận event cancellation. |
| <a id="p-refund-select"></a>`P-refund-select` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/service/impl/RefundServiceImpl.java` dòng 93–126 | Chọn charge hợp lệ trong event refund run và tạo refund. |
| <a id="p-ipn"></a>`P-ipn` | `5c6d1c13ffad9110c9827f2cf0ced98fb9919258` | `services/payment-service/src/main/java/com/flashticket/payment_service/service/PaymentService.java` dòng 146–212 | IPN kiểm chữ ký và attempt, ghi charge thành công rồi gọi Saga. |
| <a id="b-accept"></a>`B-accept` | `e43040487c8f8090a7e171a5b058325fd8e196b5` | `services/booking-service/src/main/java/com/flashticket/booking_service/messaging/AcceptPaymentListener.java` dòng 18–31 | Booking nhận lệnh chấp nhận thanh toán, chuyển vào OrderService. |
| <a id="e-db-config"></a>`E-db-config` | `9eea593a14eb50522e7be987b56ad5f0d0c0da72` | `services/event-service/src/main/resources/application.yaml` dòng 15–22 | EVENT_DB_URL và cấu hình pool Hikari riêng (max 5 trong mã; giá trị runtime cần kiểm). |
