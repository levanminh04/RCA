# Kiểm bản sửa theo REVIEW-5 (28/11/2026)

Nhánh local `rca/quan-sat-log-dung-lai`, commit `f29073f` (28 file) trên `2a275b5` (đầu PR #17 lúc soát). Minh duyệt sửa 1–9 ngày 28/11 (LOG T-076 Phiên 6). Chưa push.

## Thay đổi

| Điểm | File | Sửa |
|---|---|---|
| R1 | `BookingPersistenceIT.java` | 5 fixture listener trỏ vào hàm `*Delivery(Envelope, Message)` đang mang `@RabbitListener` |
| R4 | Payment `BusinessTelemetry.java` | `stateAfter=UNKNOWN` → `outcome=UNKNOWN` |
| R5 | `PaymentMessageListener.java` (5 hàm bọc) | `REJECTED/INVALID_CONTRACT` khi hợp đồng sai; `RETRY/TRANSACTION_UNAVAILABLE` sau NACK giao lại; `UNKNOWN/BROKER_COMMAND_FAILED` khi `basicAck/basicNack` lỗi |
| R5 | 4 listener Booking (5 hàm bọc), `RabbitTelemetry.rejected` | `REJECTED/<ErrorCode>` khi `AmqpRejectAndDontRequeueException` (DLQ); `RETRY` khi lỗi khác (AUTO ACK giao lại theo quorum `x-delivery-limit`) |
| R6 | `deploy/k8s/discovery-server/{configmap,statefulset}.yaml` | `ENVIRONMENT: production`; `env:` `HOST_ID` = `spec.nodeName`, `OTEL_AGENT_ENABLED: "false"` |
| R7 | Event `EventLogCustomizer.java` | không xuất `spanId` khi bằng đoạn span của MDC `traceparent` và không có `span_id` của agent |
| N1 | 7 `deploy/k8s/*/configmap.yaml` | bỏ `OTEL_INSTRUMENTATION_COMMON_LOGGING_{TRACE,SPAN}_ID_KEY` (agent dùng `trace_id`/`span_id` như exp-app) |
| R8 | `TicketOutboxPublisher.java`, `TicketDeliveryWorker.java`, Payment `PaymentWorker.java` | log ghi `PUBLISH_FAILED` cho lỗi không thuộc broker (Ticket: lỗi runtime ngoài `AmqpException`; Payment: lỗi sau khi broker xác nhận); `retryCount = max(0, attempt − 1)`. Mã lưu DB (`last_error_code`) và lịch retry không đổi |
| R3 | Booking `OrderController.java`, `GlobalExceptionHandler.java` | tạo đơn trả `X-Correlation-Id` = orderId (gateway giữ header của Booking: `CorrelationIdFilter` "giữ giá trị của nó"); phản hồi lỗi dùng correlation trong MDC cho log, header, body |

Test mới: Payment `messaging/ListenerTelemetryTests` (4), Booking `messaging/ListenerTelemetryTests` (3), `HttpErrorHandlingTests.errorResponseAndLogReuseTheCorrelationNormalizedByTheFilter`, assertion header trong `OrderControllerTests`, Event `ObservabilityTests.propagatedParentSpanIsNotExportedAsCurrentSpan`. Spotless áp cho 4 service; chỉ đổi file đã sửa.

## Kết quả

| Kiểm | Kết quả | File |
|---|---|---|
| `verify` + B16 (`chay-verify-sua.sh`) | payment 144, event 179, ticket 229, booking 457 test, 0 lỗi; B16 PASS cả 4 | `verify/tien-do.tsv`, `verify/log/` |
| `-P rca-test verify` | Event 187, Booking 466, 0 lỗi | `verify/log/*-rca-test-verify.log` |
| Booking `-P integration verify` (Testcontainers Postgres + RabbitMQ) | surefire 457 + failsafe 173, 0 lỗi; `BookingPersistenceIT` 157 ca | `verify/log/booking-service-integration-verify.log` |
| Ticket `TicketPostgresIT` (Postgres CI) | 22 đạt | `verify/log/ticket-service-postgres-it.log` |
| `test-ticket-replica.sh` (bản sao tạm, dưới) | `prepare` đạt lần 3; `run '-Dtest=TicketPostgresIT,TicketSagaBrokerIT' test` 25 đạt; `run verify` 229 test, 4 failure ở `TicketLocalConfigurationTests` | `log/ticket-replica-*.log` |
| Đối chứng 4 failure trên main `6b77144` (`git archive`, cùng env bộ thử, `-Dtest=TicketLocalConfigurationTests`) | cùng 4 failure → do công thức `run … verify` nạp biến replica cho test cấu hình cục bộ, không do PR | `log/ticket-replica-main-6b77144-config-test.log` |
| Bộ kiểm K8s | `test-k8s-deploy.py`, `test-k8s-discovery.py`, `test-https-config.py`, `test-k8s-rollout-hooks.py` đạt | `log/test-k8s-*.log`, `log/test-https-config.py.log` |
| Test đơn vị trước khi có Docker | payment 6, booking 74, event 2 | `log/unit-*.log` |
| Jar production Booking | 0 lớp `RcaFaults` | `log/booking-package-production.log` |
| Agent `tat-secret-true` (image `f29073f`, `../ban-6/chay-agent-v6.sh`) | env cuối `false`, 0 dòng khởi động agent, 0 byte traces/metrics, 416 MiB / 768 MiB; 135/135 dòng log đúng commit và `environment=production` | `tat-secret-true/` |
| Quét bí mật diff commit; log bộ thử | sạch; 0 file log có biến mật khẩu | lệnh trong LOG |

## Bộ thử replica Ticket: điều chỉnh môi trường

Script của nhóm (`.github/scripts/test-ticket-replica.sh`, `TESTING.md` ghi "recipe chưa kiểm runtime") không chạy được nguyên bản trên laptop:

1. Lần 1: RabbitMQ lỗi đọc `.erlang.cookie` (eacces) — cùng lỗi laptop đã gặp ở `../ban-6/`.
2. Lần 2 (bản sao thêm `--user 999:999`): script gọi `add_vhost` khi ứng dụng RabbitMQ chưa chạy — phép chờ `rabbitmq-diagnostics ping` chỉ xác nhận nút Erlang. Đây là lỗi chờ trong script của main, không thuộc PR.
3. Lần 3 (bản sao đổi thêm phép chờ sang `check_running`): đạt.

Bản sao `test-ticket-replica.local-tam.sh` đặt tạm trong worktree, xóa sau khi chạy, không commit; khác script gốc đúng 2 dòng (`log/ticket-replica-khac-ban-tam.diff`). Mỗi lần hỏng đều dọn bằng `cleanup` của script (0 container còn lại).

## Chưa kiểm

- Tuyến thật trên K8s (`env` thắng `envFrom`, CD cùng digest khi reader bật — REVIEW-5 R2): bước 6–7.
- Khi agent bật: thứ tự ghi MDC `span_id` của agent so với `spanId` của bộ lọc Event chỉ được suy từ mã; chưa chạy Event với agent bật.
- Đối chứng test tích hợp Booking trên `2a275b5` (trước sửa) không chạy; lỗi R1 xác nhận bằng mã và bytecode (REVIEW-5).
