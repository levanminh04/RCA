# Việc chờ quyết và việc cần làm (FlashTicket cho RCA)

- **Trạng thái:** bản nháp, sửa dần. Minh duyệt ghi (chat 11/11/2026: "duyệt ghi trước, sau đó soạn các phần chờ tôi và nhóm quyết và làm ... bản duyệt ghi chỉ coi là nháp, sẽ sửa dần").
- **Người soạn:** Claude, 11/11/2026.
- **Đọc cùng:** `KE-HOACH-GIAI-DOAN-2.md` (kế hoạch), `results/T-058/so-khac-phuc.md` (sổ khắc phục).
- Mục 2 và 3 viết để gửi thẳng cho nhóm hệ thống. Người phụ trách lấy theo `docs/reference/sources/roles.md` (18/09/2026); Minh giao lại nếu khác.

## 1. Minh quyết

| # | Việc | Đề xuất | Chưa quyết thì ảnh hưởng gì |
|---|---|---|---|
| M1 | Người phản biện T-058 | Phản biện chéo theo phần: phiên Codex mới kiểm phần Claude làm (Redis, RabbitMQ, log); phiên Claude mới kiểm phần Codex làm (lượt đêm) | T-058 chưa đóng được phần khả thi |
| M2 | Commit kết quả lượt đêm | Commit phần còn lại; gói dữ liệu thô 126 MB để ngoài git, giữ mã băm | Kết quả chỉ nằm trên một máy |
| M3 | Máy AWS `3.24.8.49` | Giữ làm máy tải (chặng 2). Chưa bắt đầu chặng 2 thì Stop (giữ đĩa) | Đang chạy, tốn tín dụng AWS |
| M4 | Giao việc mục 2, 3 cho thành viên | Gửi file này; mỗi người nhận dòng của mình | Chặng 1b không bắt đầu |
| M5 | Đưa mục tổng quát của sổ khắc phục vào `docs/LESSONS.md` | Claude soạn đoạn ghi, Minh duyệt | Bài học chỉ nằm trong sổ của T-058 |
| M6 | Giao diện kết quả RCA đặt ở đâu | **Đã quyết (chat 11/11):** phương án A (Grafana, panel Node graph) trước; B (trang riêng của RCA) thử sau nếu A không ổn; G2 do Minh làm. Kế hoạch: `KE-HOACH-GIAI-DOAN-2.md` §7 | — |
| M7 | Chia đợt phát triển và đợt đánh giá trên FlashTicket: cho phép lần lặp của cùng một ô (vị trí × loại lỗi) nằm ở cả hai đợt không | Cho phép, nhưng báo tách hai nhóm "vị trí đã thấy khi phát triển" và "vị trí mới". Đang OPEN ở `docs/KE-HOACH-GIAI-DOAN-TOI.md` D.9 | Chưa chốt được danh mục lỗi (chặng 3) |
| M8 | Lịch mở lại P8 (LLM giải thích), đang hoãn từ 09/11 | Sau chặng 4, trước demo | DT18 và bước 5 của cô cần phần này |
| M9 | Ra B16 bản 2 (chuẩn log, trace) | Claude soạn bản nháp v2 = v1 + các bổ sung ở mục 3.3; Minh duyệt rồi đưa vào repo FlashTicket | Mỗi người tiếp tục làm log một kiểu |

## 2. Nhóm hệ thống làm

| Mã | Việc | Người phụ trách | Trạng thái 11/11 | Xong khi |
|---|---|---|---|---|
| a | CD build image cho cả x86 và ARM: thêm `docker/setup-qemu-action`, đổi `platforms` thành `linux/amd64,linux/arm64` trong `.github/workflows/_deploy-service.yml` | Minh (CI baseline) | **Nhóm đang làm, chưa xong.** Trong lúc chờ, `exp-app` tiếp tục chạy image ARM tự build từ đúng commit của máy 84 (KP-01) | Một digest chạy được trên cả máy 84 và máy Oracle |
| b | Nâng `mem_limit` khi bật agent: booking bị OOM ở 512 MiB; payment 95%, discovery 90% giới hạn | Chủ từng service; Minh (hạ tầng) | Chưa làm. `exp-app` đang dùng bản nâng riêng (KP-04) | Chạy tải 1 giờ không OOM |
| c | Thêm biến env: `SPRING_AUTOCONFIGURE_EXCLUDE=...LettuceObservationAutoConfiguration` (booking, gateway, để có span Redis); `OTEL_INSTRUMENTATION_RABBITMQ_EXPERIMENTAL_SPAN_ATTRIBUTES=true` (event, booking, payment, ticket, để có vhost); đưa jar agent vào image | Minh | Chưa làm. Đã thử trên `exp-app` (KP-05, KP-06) | Image và env của nhóm cho cùng kết quả như `exp-app` |
| d | Khởi tạo PostgreSQL: quyền thực thi cho `deploy/postgres/00-business-databases.sh`; thêm hai file SQL reader mà compose trỏ tới nhưng repo không có | Minh (hạ tầng) | Chưa làm (KP-03) | Dựng PostgreSQL mới từ repo không lỗi |
| e | Log: sửa theo bảng mục 3 | Chủ từng service | Chưa làm | Bộ kiểm log báo đạt ở mọi service |
| f | Tên queue trong span RabbitMQ: gắn thuộc tính tên queue trong listener, hoặc thêm cầu nối Micrometer Tracing | Sơn (booking), Tuấn (payment, ticket) | Chưa làm (KP-06) | Span nhận có tên queue |
| g | Keycloak ghi log JSON và có `traceId` | Sơn | Chưa làm; tên tùy chọn của bản 26.8.0 chưa thử | Log Keycloak trong Loki là JSON |
| h | Bật log có ích của hạ tầng: PostgreSQL ghi truy vấn chậm và chờ khóa (`log_min_duration_statement`, `log_lock_waits`) | Minh (hạ tầng) | Chưa làm; hiện đang tắt (KP-17) | Một truy vấn chậm thử xuất hiện trong log |
| i | Phần phục vụ tiêm lỗi: cờ lỗi trong code (chỉ bật ở môi trường thử), chuỗi kết nối cấu hình được để đi qua Toxiproxy, mock VNPay | Minh nhận làm (PLAN Q6, 10/11) | Chưa làm | Đủ cho các kịch bản ở `KE-HOACH-GIAI-DOAN-TOI.md` D.9 |

## 3. Tình trạng log từng service

### 3.1 Cách đo

- Đo ngày 11/11/2026 trên `exp-app`. Image build từ đúng commit đang chạy trên máy 84; từ đó tới commit mới nhất (`73c10fa5`) không có thay đổi cấu hình log.
- Đếm bằng `docker logs` trong đời container hiện tại (từ lần tạo lại gần nhất), tải thấp. Đọc thêm cấu hình `application.yaml` và đếm lệnh ghi log trong `src/main/java`.
- Biến `LOGGING_STRUCTURED_FORMAT_CONSOLE=logstash` nằm trong env của 7 service Spring, nên service nào không tự cấu hình thêm sẽ ra định dạng logstash mặc định.

### 3.2 Bảng

| Service | Người phụ trách | Định dạng hiện tại | Ghi log khi nào | Vấn đề | Cần sửa |
|---|---|---|---|---|---|
| api-gateway | Minh | Logstash mặc định: `@timestamp`, `level`, `logger_name`, `thread_name`. Các trường B16 chỉ có ở dòng lỗi request | **Chỉ khi request trả 4xx hoặc 5xx** (`CorrelationIdFilter`, điều kiện `status.isError()`). Request thành công không ghi | 61/98 dòng là log của thư viện Eureka (`com.netflix.discovery`) | Một dòng cho **mọi** request (kể cả thành công): route, status, `durationMs`, `traceId`. Đổi `level`→`severity`; thêm `serviceName`, `serviceVersion`, `instanceId`, `environment`, `hostId` cho mọi dòng. Hạ log thư viện xuống WARN |
| discovery-server | Minh | Logstash mặc định, không có trường B16 | Log định kỳ của Eureka | 525/583 dòng của `com.netflix.eureka.registry` | Hạ log thư viện xuống WARN; thêm trường định danh như gateway |
| booking-service | Sơn | Logstash mặc định, không có trường B16 nào (`application.yaml` không có cấu hình log có cấu trúc) | Chỉ ở 3 worker (outbox, hủy sự kiện, hết hạn giữ chỗ); 9 lệnh ghi log trong code. Controller và service nghiệp vụ không ghi | 17/124 dòng là cảnh báo Hibernate Validator HV000271, HV000272 (`@Valid` trên List, cách viết đã lỗi thời); phần lớn còn lại là log thư viện | Dùng cùng khối cấu hình log với ticket, payment, user. Ghi log ở các điểm quyết định B16 §5: giữ chỗ, khuyến mãi, khóa đơn, chấp nhận thanh toán, hết hạn, nhả chỗ, kèm `stateBefore`, `stateAfter`, `reasonCode`. Sửa chú thích `@Valid` |
| event-service | Tuyến | Gần B16 nhất: bộ tùy biến riêng `EventLogCustomizer`; có `severity`, `timestamp`, `schemaVersion`, `hostId` | Outbox, audit, ảnh; 5 lệnh ghi log | Khối cấu hình khác ba service ticket, payment, user; không có tên logger | Dùng chung một khối cấu hình; giữ `hostId`; ghi log ở điểm quyết định B16 §5 (lưu nháp, công bố cấu hình, duyệt, hủy) |
| payment-service | Tuấn | Danh sách trường B16, nhưng **mất `timestamp`**: danh sách cho phép ghi `timestamp` còn định dạng logstash đặt tên `@timestamp`, nên trường bị lọc. Không có `schemaVersion` | Chỉ ở `PaymentWorker` và vài dòng controller; 22 lệnh ghi log | Thông điệp viết tự do (`"Payment created: orderId=..."`, `"[FinanceController] ..."`), không có `eventName`, `outcome`; cảnh báo HV000272 | Sửa để giữ `timestamp`, thêm `schemaVersion`. Ghi log có cấu trúc ở điểm quyết định: tạo lần thanh toán, kết quả callback, xác nhận, bước Saga, hoàn tiền |
| ticket-service | Tuấn | Danh sách trường B16 cộng bộ tùy biến `TicketLogFields` (có `timestamp`, `schemaVersion`) | Khi request lỗi (`ticket.request.rejected`, `ticket.request.failed`), khi xử lý message lỗi, ở job; 8 lệnh ghi log | Không ghi khi phát vé, giao vé, check-in thành công | Ghi log ở điểm quyết định B16 §5: phát vé, giao vé, check-in; mỗi message xử lý xong ghi một dòng kết quả |
| user-service | Tuyến | Danh sách trường B16 cộng `UserLogCustomizer` | Qua `UserTelemetry` (`user.<thao tác>`), 2 lệnh ghi log | Rất ít log trong request | Ghi log ở điểm quyết định B16 §5: cấp quyền, kết quả gọi Keycloak Admin API |
| keycloak | Sơn | Văn bản thường, không phải JSON | Cảnh báo cấu hình, đăng nhập | Không nối được với trace | Mục 2g |
| PostgreSQL | Minh (hạ tầng) | Văn bản | 216 dòng trong 24 giờ, toàn bộ là `checkpoint` | Log truy vấn chậm, chờ khóa, kết nối đều tắt | Mục 2h |
| MongoDB | Minh (hạ tầng) | JSON | 124.849 dòng trong 24 giờ | Khoảng 99% là mở và đóng kết nối (28.326 kết nối trong 24 giờ) | Tìm nguồn mở kết nối liên tục; Collector lọc bỏ khi thu |
| RabbitMQ | Minh (hạ tầng) | Văn bản | Khoảng 9.600 dòng trong 24 giờ | 9.450 dòng là tài khoản giám sát (`otel_monitor`) đăng nhập | Collector lọc bỏ khi thu |
| Redis | Minh (hạ tầng) | Văn bản | 121 dòng trong 24 giờ, chủ yếu lưu snapshot | Truy vấn chậm của Redis nằm trong bộ nhớ (`SLOWLOG`), không ra log | Không cần sửa log; lấy qua metric |

### 3.3 Quy tắc chung đề xuất (thay quy tắc 2 ở `KE-HOACH-GIAI-DOAN-2.md` §4e khi Minh duyệt)

1. Một khối cấu hình log giống hệt nhau cho mọi service Spring: cùng danh sách trường, cùng tên trường (`severity`, `timestamp`, `stackTrace`).
2. **Gateway** ghi một dòng cho mọi request. **Service nghiệp vụ** ghi một dòng ở mỗi điểm quyết định nghiệp vụ (B16 §5), mỗi message xử lý xong, và mỗi lỗi. Không bắt service nghiệp vụ ghi thêm một dòng cho mọi request thành công, vì span của request đã có thời gian và mã trạng thái; log cần mang thứ span không có: `reasonCode`, `stateBefore`, `stateAfter`, `outcome`.
3. Thư viện (`org.springframework`, `org.hibernate`, `com.netflix`, `io.lettuce`, `org.apache`) ở mức WARN; `com.flashticket` ở mức INFO.
4. Một phép kiểm tự động trong CI: chạy service, bắt vài dòng log, so với JSON Schema viết từ B16.
5. Ước lượng dung lượng của quy tắc 2 ở gateway [TÍNH, giả định 700 byte mỗi dòng]: 50 request/giây → khoảng 126 MB mỗi giờ trước nén.
