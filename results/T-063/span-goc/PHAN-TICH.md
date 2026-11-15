# T-063 — Phân loại span gốc và span mồ côi trên 9 ca T-062 (12/11/2026 21:53Z, Claude)

Câu hỏi SPEC T-063: "Span gốc nào là hợp lệ, span nào mất ngữ cảnh?" → bổ sung instrumentation ở đâu.

Phép kiểm: [`phan_loai.py`](phan_loai.py) đọc `raw-traces.jsonl` (OTLP JSON) của 9 gói ca, lấy span trong `[t−300, t+300)`, phân loại span không có `parentSpanId` theo kind/scope/thuộc tính và span có `parentSpanId` nhưng cha không có trong cả gói. Đầu ra: [`phan-loai.json`](phan-loai.json) (từng ca, từng (service, nhóm, scope, kind, tên), một ví dụ thuộc tính gồm `thread.name`), [`phan-loai.log`](phan-loai.log).

## 1. Bảng tổng 9 ca (số span gốc / mồ côi)

| Service | Nhóm | Số | Cơ chế (bằng chứng: `thread.name`, scope) | Phân loại B16 §3 |
|---|---|---|---|---|
| keycloak | INTERNAL Hibernate làm gốc | 30.946 | `SELECT PersistentUserSessionEntity` trên luồng `user-session-purge-expired` (19.995); `SELECT`/`DELETE OutboxEntryEntity` trên `Timer-0` (5.400 + 5.400) | **Job hợp lệ nhưng thiếu span job bọc**: tác vụ định kỳ nội bộ của Keycloak (dọn phiên hết hạn; `org.keycloak.events.outbox.OutboxDrainerTask` do SPI đăng ký qua `TimerProvider`, `services/keycloak-spi/.../RegistrationEventListenerFactory.java:84`). Mỗi câu SQL thành một trace riêng |
| api-gateway | SERVER HTTP | 29.902 | Netty `GET event/booking/payment/ticket` | Điểm vào hợp lệ |
| ticket/payment/event/booking/user | INTERNAL `spring-scheduling` | 36.287 | `TicketJobs.*`, `PaymentWorker.*`, `OutboxWorker.relay`, `BookingOutboxWorker…`, `OrderExpiryWorker…` | Job hợp lệ (đã có span job) |
| keycloak | CLIENT JDBC gốc | 1.770 | `JGROUPS_PING` trên `jgroups-*`/`Timer runner-*` (khám phá cụm JGroups qua DB); `keycloak_db` trên `agroal-11` (pool) | Hạ tầng nền hợp lệ (cụm, pool), thiếu span bọc |
| booking/payment/event/ticket | CLIENT JDBC `<svc>_db` gốc | 1.652 | `DiscoveryClient-InstanceInfoReplicator-%d` (health indicator DB do Eureka gọi định kỳ); `HikariPool-1:housekeeper` / `connection-adder` (bảo trì pool) | Hạ tầng nền hợp lệ; **đây là nguồn của "span `*_db` gốc ở Spring — chưa rõ nguồn"** trong hồ sơ chiến dịch |
| mọi service Spring | CLIENT HTTP gốc | 2.160 | `DiscoveryClient-HeartbeatExecutor` (PUT), `CacheRefreshExecutor` (GET) tới Eureka | Hạ tầng nền hợp lệ |
| discovery-server | CLIENT HTTP gốc | 1.080 | `TaskBatchingWorker-target_localhost-*` (Eureka sao chép tới chính nó) | Hạ tầng nền hợp lệ |
| booking/gateway | CLIENT Redis `INFO` gốc | 360 | `lettuce-nioEventLoop-*` (health indicator Redis) | Hạ tầng nền hợp lệ |
| user-service | CLIENT Mongo gốc | 360 | `hello admin`, `listDatabases admin` trên `DiscoveryClient-InstanceInfoReplicator` | Hạ tầng nền hợp lệ |
| keycloak | SERVER HTTP | 123 | điểm vào Keycloak | Điểm vào hợp lệ |
| booking-service | **mồ côi** | 92 (≈10/ca) | JDBC connect `booking_db` (6–8/ca) trên `http-nio-127.0.0.1-8082-exec-*` + Redis `INFO server` (4/ca) | **Mất cha do lọc**: cha là span SERVER `/actuator/health`, bị `filter/health` của Collector `exp-app` bỏ (`attributes["http.route"] == "/actuator/health"`), con không bị bỏ. Nguồn lời gọi health: đầu dò `inj.py probe` gọi health Booking trực tiếp + qua proxy |

CONSUMER làm gốc: 0 (tải T-062 chỉ đọc, không có message Saga; R-04 chưa kiểm được — cần tải mua vé).

## 2. Kết luận

- **Quan sát → cơ chế (đã kiểm bằng thuộc tính span):** mọi span gốc không phải điểm vào/job Spring đều thuộc tác vụ nền xác định được theo luồng; không thấy nhóm "mất ngữ cảnh trong đường giao dịch" trên tải đọc. Nhóm lớn nhất (Keycloak, 31 nghìn span/9 ca) là job nội bộ không có span bọc.
- **Span mồ côi Booking** là hệ quả của lọc theo từng span ở Collector + đầu dò của bộ chạy, không phải lỗi lan truyền ngữ cảnh của ứng dụng.
- **Chưa kiểm:** đường giao dịch có message (Saga, callback VNPay) — cần tải mua vé (L1). Có thể xuất hiện CONSUMER gốc nếu ngữ cảnh không truyền qua RabbitMQ.

## 3. Đề xuất bổ sung (thực hiện ở bước 5 T-063, khi phối hợp `exp-app`)

1. **Keycloak — span job bọc tác vụ định kỳ, chỉ bằng cấu hình agent** (không sửa Keycloak/SPI): `OTEL_INSTRUMENTATION_METHODS_INCLUDE` cho phương thức chạy tác vụ của `TimerProvider` (ứng viên `org.keycloak.services.scheduled.ScheduledTaskRunner[run]`) và của tác vụ dọn phiên. **Chưa kiểm:** tên lớp/phương thức trong bản Keycloak đang chạy (kiểm bằng danh sách lớp trong jar trên image trước khi bật). Kiểm sau: span INTERNAL mới có trong Tempo, SQL Hibernate thành con.
2. **Đầu dò bộ chạy không gọi `/actuator/health` của app trong cửa sổ phương pháp** (hoặc gọi đối xứng N/A — xem `ca-nen/PHAN-TICH.md`). Giữ `filter/health` (lời gọi health của hạ tầng không phải giao dịch); ghi rõ trong B16 bản 2 rằng lọc theo span để lại con mồ côi, nên nguồn lời gọi health phải nằm ngoài cửa sổ hoặc lọc theo trace.
3. **Không bọc** các nhóm hạ tầng nền (Hikari, Eureka, JGroups, health indicator): đó là gốc hợp lệ theo B16 §3; adapter/M1-FT xử lý như thao tác nền (H6).
4. Sau tải mua vé: chạy lại `phan_loai.py` trên gói ca mới để kiểm CONSUMER gốc và mồ côi trên đường Saga (gắn với R-04).
