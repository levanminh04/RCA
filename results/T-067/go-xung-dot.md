# T-067 — Gỡ xung đột khi tạo `rca/exp-2026-11`

Nhánh `rca/exp-2026-11` = commit `36a3725` (merge, cha 1 `640dbaf` = `main` ghim, cha 2 `bb84d64` = `rca/quan-sat-log`).
Đã push lên origin ngày 18/11/2026. Không mở PR vào `main`; `main` không đổi.

Quy tắc (SPEC bước 1, Minh: "main là chuẩn"): mọi đoạn logic lấy theo `main`. Phần quan sát của PR chỉ chèn lại
dạng gọi telemetry quanh điểm xử lý của `main`, không đổi luồng. Giữ từ PR: `src/rca-test` và profile trong pom,
cấu hình log B16, agent trong image, test quan sát. Thay đổi `deploy/*` của PR không mang theo.

Kiểm lại: `git merge-tree --write-tree 640dbaf bb84d64` ra đúng 10 file xung đột (18/11).

## 1. Mười file xung đột

| File | Lấy phía nào | Thêm từ PR | Vì sao |
|---|---|---|---|
| `infrastructure/api-gateway/Dockerfile` và 6 Dockerfile cùng mẫu (`discovery-server`, `booking`, `event`, `payment`, `ticket`, `user`) | `main` (giữ `FROM eclipse-temurin…@sha256:b48e02e0…`, `apk add curl jq`, nhãn `runtime-tools`) | Khối của PR sau dòng `COPY target/*.jar`: `ADD --checksum=sha256:e43a270d…` jar OpenTelemetry Java agent 2.33.1, `chmod /otel`, `COPY docker-entrypoint.sh`, `ARG/ENV SERVICE_VERSION`, `ENV SERVICE_NAME`; `ENTRYPOINT ["/app/docker-entrypoint.sh"]` | SPEC: Dockerfile lấy `main` làm gốc, chỉ thêm dòng tải agent có checksum, entrypoint, biến môi trường. PR còn đổi digest `FROM` (`ac05c3c4…`): **không mang theo**. Hệ quả: ảnh gốc khác bản 3 (T-062 dùng `ac05c3c4…`), ghi ở `thay-doi-main.md`. Gộp bằng script (chép khối PR nguyên văn), kiểm bằng `git diff 640dbaf` |
| `services/booking-service/…/promotion/service/impl/PromotionServiceImpl.java` | `main` (dùng `OrderViewAssembler`) | `import …observability.BusinessTelemetry`; lời gọi `BusinessTelemetry.committed("promotion", …, "PROMOTION_APPLIED")` ngay sau `orderRepository.save(lockedOrder)` | Đúng vị trí PR đặt; không đổi câu lệnh nào của `main` |
| `services/booking-service/…/order/service/impl/OrderServiceImpl.java` | `main` (dùng `OrderViewAssembler`) | 1 khối xung đột: thêm `BusinessTelemetry.committed("reserve", …, "RESERVATION_HELD")` trước `return orderViewAssembler.toView(order)`. Các khối khác git tự gộp: `transition(order, state)` thay `setLifecycleState` ở 7 chỗ (đặt cùng trạng thái rồi ghi telemetry khi trạng thái đổi), telemetry `freeze` | `transition()` gán đúng giá trị như `setLifecycleState` cũ, chỉ thêm log sau commit; `main` thêm 1 chỗ `setLifecycleState(PENDING_PAYMENT)` mới (dòng ~1969) không có telemetry — giữ nguyên |
| `services/payment-service/…/service/impl/RefundServiceImpl.java` | `main` nguyên bản (commit `782e557`, Quốc Tuấn: hoàn tiền chỉ ghi DB trong `sendRefund`, outcome `DB_ONLY`) | `import …observability.BusinessTelemetry`, `import java.util.Map`; trong `sendRefund`: `var before = refund.getState()` ngay trước `refund.setState(SUCCEEDED)`, rồi `BusinessTelemetry.committed("refund-result", {orderId, correlationId, refundId, outcome: "SUCCESS"}, before, refund.getState(), attempt.getOutcome())` | Quyết định của Minh 17–18/11 (LOG T-067 phiên 2, quyết định 2). Phía PR đặt lời gọi trong `recordGatewayResult` — hàm `main` đã bỏ. `reasonCode` = `attempt.getOutcome()` = `"DB_ONLY"`. `BusinessTelemetry` chỉ ghi log sau khi giao dịch commit (`afterCommit`) |

## 2. File không xung đột nhưng đưa về `640dbaf`

| Nhóm | Số file | Vì sao |
|---|---|---|
| `deploy/*` (gồm 4 file PR thêm trong `deploy/observability/`) | 13 | SPEC: thay đổi `deploy/*` của PR không mang theo. Cấu hình chạy của lab nằm ở repo lab (`app-host/overrides/`) |
| `.github/*` (CI) | 3 | Không thuộc nhóm được giữ; CI không dùng cho bản ghim (lab tự chạy `mvnw verify`) |
| `docs/project/decision-register.md` | 1 | Tài liệu của nhóm, không thuộc nhóm được giữ |
| `services/keycloak-spi/Dockerfile` | 1 | Keycloak không nằm trong 7 service build lại; không thuộc nhóm được giữ |
| 6 DTO Booking (`dto/response/{Availability,OrderItemView,OrderView,Problem}.java`, `dto/snapshot/{PurchaseSnapshot,SalesConfiguration}.java`) | 6 | PR bỏ `@Valid` ở mức danh sách (giữ `@Valid` ở phần tử). Đây là thay đổi kiểm hợp lệ, không phải telemetry |
| `services/{event,payment}-service/database/90-erd-reader.sql` | 2 | `main` đã xóa hai file này |

## 3. File khác `640dbaf` sau merge (98 file), theo nhóm

Lệnh: `git diff --name-status 640dbaf 36a3725`. Đã đọc diff các file "mã nghiệp vụ": chỉ thêm `BusinessTelemetry`/`RabbitTelemetry`,
dòng log có cấu trúc, `MDC` correlation; listener RabbitMQ có thêm hàm bọc (annotation `@RabbitListener` chuyển sang hàm bọc,
hàm bọc gọi hàm xử lý cũ); `TicketBusinessListeners` đặt khối xử lý cũ vào trong `try (RabbitTelemetry)`, giữ thứ tự
decode → transaction → ACK và ACK ngoài khối bắt lỗi nghiệp vụ; gateway log mọi request thay vì chỉ request lỗi.
Không đổi điều kiện, câu lệnh ghi DB hay giá trị trả về. Đây là các thay đổi đã chạy trong bản 3 (`6b21ed55`).

### khai biến B16, bỏ qua thư mục rca-test cục bộ (giữ từ PR) — 9 file

- `M .env.example`
- `M .gitignore`
- `M infrastructure/api-gateway/.env.example`
- `M infrastructure/discovery-server/.env.example`
- `M services/booking-service/.env.example`
- `M services/event-service/.env.example`
- `M services/payment-service/.env.example`
- `M services/ticket-service/.env.example`
- `M services/user-service/.env.example`

### image: agent trong image, entrypoint (giữ từ PR; Dockerfile gỡ xung đột) — 21 file

- `M infrastructure/api-gateway/.dockerignore`
- `M infrastructure/api-gateway/Dockerfile`
- `A infrastructure/api-gateway/docker-entrypoint.sh`
- `M infrastructure/discovery-server/.dockerignore`
- `M infrastructure/discovery-server/Dockerfile`
- `A infrastructure/discovery-server/docker-entrypoint.sh`
- `M services/booking-service/.dockerignore`
- `M services/booking-service/Dockerfile`
- `A services/booking-service/docker-entrypoint.sh`
- `M services/event-service/.dockerignore`
- `M services/event-service/Dockerfile`
- `A services/event-service/docker-entrypoint.sh`
- `M services/payment-service/.dockerignore`
- `M services/payment-service/Dockerfile`
- `A services/payment-service/docker-entrypoint.sh`
- `M services/ticket-service/.dockerignore`
- `M services/ticket-service/Dockerfile`
- `A services/ticket-service/docker-entrypoint.sh`
- `M services/user-service/.dockerignore`
- `M services/user-service/Dockerfile`
- `A services/user-service/docker-entrypoint.sh`

### gói observability: log B16, telemetry (giữ từ PR) — 18 file

- `A infrastructure/api-gateway/src/main/java/com/flashticket/api_gateway/observability/LogFields.java`
- `A infrastructure/api-gateway/src/main/java/com/flashticket/api_gateway/observability/SafeStackTracePrinter.java`
- `A infrastructure/discovery-server/src/main/java/com/flashticket/discovery_server/observability/LogFields.java`
- `A infrastructure/discovery-server/src/main/java/com/flashticket/discovery_server/observability/SafeStackTracePrinter.java`
- `A services/booking-service/src/main/java/com/flashticket/booking_service/observability/BusinessTelemetry.java`
- `A services/booking-service/src/main/java/com/flashticket/booking_service/observability/LogFields.java`
- `A services/booking-service/src/main/java/com/flashticket/booking_service/observability/RabbitTelemetry.java`
- `A services/booking-service/src/main/java/com/flashticket/booking_service/observability/SafeStackTracePrinter.java`
- `M services/event-service/src/main/java/com/flashticket/event_service/observability/EventLogCustomizer.java`
- `A services/payment-service/src/main/java/com/flashticket/payment_service/observability/BusinessTelemetry.java`
- `A services/payment-service/src/main/java/com/flashticket/payment_service/observability/LogFields.java`
- `A services/payment-service/src/main/java/com/flashticket/payment_service/observability/RabbitTelemetry.java`
- `A services/payment-service/src/main/java/com/flashticket/payment_service/observability/SafeStackTracePrinter.java`
- `M services/ticket-service/src/main/java/com/flashticket/ticket_service/config/TicketLogFields.java`
- `A services/ticket-service/src/main/java/com/flashticket/ticket_service/observability/BusinessTelemetry.java`
- `A services/ticket-service/src/main/java/com/flashticket/ticket_service/observability/RabbitTelemetry.java`
- `A services/user-service/src/main/java/com/flashticket/user_service/observability/SafeStackTracePrinter.java`
- `M services/user-service/src/main/java/com/flashticket/user_service/observability/UserLogCustomizer.java`

### mã nghiệp vụ: chỉ chèn lời gọi telemetry hoặc log (giữ từ PR; 3 file gỡ xung đột) — 20 file

- `M infrastructure/api-gateway/src/main/java/com/flashticket/api_gateway/web/CorrelationIdFilter.java`
- `M services/booking-service/src/main/java/com/flashticket/booking_service/messaging/AcceptPaymentListener.java`
- `M services/booking-service/src/main/java/com/flashticket/booking_service/messaging/BookingIssuanceResultListener.java`
- `M services/booking-service/src/main/java/com/flashticket/booking_service/messaging/EventCancellationListener.java`
- `M services/booking-service/src/main/java/com/flashticket/booking_service/messaging/SalesConfigurationListener.java`
- `M services/booking-service/src/main/java/com/flashticket/booking_service/order/service/impl/OrderServiceImpl.java`
- `M services/booking-service/src/main/java/com/flashticket/booking_service/promotion/service/impl/PromotionServiceImpl.java`
- `A services/booking-service/src/main/java/com/flashticket/booking_service/web/CorrelationFilter.java`
- `M services/payment-service/src/main/java/com/flashticket/payment_service/controller/FinanceController.java`
- `M services/payment-service/src/main/java/com/flashticket/payment_service/messaging/PaymentMessageListener.java`
- `M services/payment-service/src/main/java/com/flashticket/payment_service/service/PaymentService.java`
- `M services/payment-service/src/main/java/com/flashticket/payment_service/service/impl/FinanceServiceImpl.java`
- `M services/payment-service/src/main/java/com/flashticket/payment_service/service/impl/PaymentSagaServiceImpl.java`
- `M services/payment-service/src/main/java/com/flashticket/payment_service/service/impl/RefundServiceImpl.java`
- `M services/payment-service/src/main/java/com/flashticket/payment_service/worker/PaymentWorker.java`
- `M services/ticket-service/src/main/java/com/flashticket/ticket_service/application/TicketService.java`
- `M services/ticket-service/src/main/java/com/flashticket/ticket_service/messaging/TicketBusinessListeners.java`
- `M services/ticket-service/src/main/java/com/flashticket/ticket_service/worker/TicketDeliveryWorker.java`
- `M services/ticket-service/src/main/java/com/flashticket/ticket_service/worker/TicketOutboxPublisher.java`
- `M services/user-service/src/main/java/com/flashticket/user_service/identity/KeycloakAdminClient.java`

### application.yaml: cấu hình log B16 (giữ từ PR) — 7 file

- `M infrastructure/api-gateway/src/main/resources/application.yaml`
- `M infrastructure/discovery-server/src/main/resources/application.yaml`
- `M services/booking-service/src/main/resources/application.yaml`
- `M services/event-service/src/main/resources/application.yaml`
- `M services/payment-service/src/main/resources/application.yaml`
- `M services/ticket-service/src/main/resources/application.yaml`
- `M services/user-service/src/main/resources/application.yaml`

### test quan sát (giữ từ PR) — 9 file

- `A infrastructure/api-gateway/src/test/java/com/flashticket/api_gateway/ObservabilityTests.java`
- `A infrastructure/discovery-server/src/test/java/com/flashticket/discovery_server/ObservabilityTests.java`
- `A services/booking-service/src/test/java/com/flashticket/booking_service/ObservabilityTests.java`
- `A services/event-service/src/test/java/com/flashticket/event_service/ObservabilityTests.java`
- `A services/payment-service/src/test/java/com/flashticket/payment_service/ObservabilityTests.java`
- `A services/ticket-service/src/test/java/com/flashticket/ticket_service/ObservabilityTests.java`
- `M services/ticket-service/src/test/java/com/flashticket/ticket_service/TicketLocalConfigurationTests.java`
- `M services/user-service/src/test/java/com/flashticket/user_service/BundledConfigurationTests.java`
- `A services/user-service/src/test/java/com/flashticket/user_service/ObservabilityTests.java`

### pom.xml: profile rca-test, thư viện log và test quan sát (giữ từ PR) — 4 file

- `M services/booking-service/pom.xml`
- `M services/event-service/pom.xml`
- `M services/payment-service/pom.xml`
- `M services/ticket-service/pom.xml`

### src/rca-test (giữ từ PR) — 10 file

- `A services/booking-service/src/rca-test/java/com/flashticket/booking_service/testing/RcaFaults.java`
- `A services/booking-service/src/rca-test/java/com/flashticket/booking_service/testing/RcaFaultsWebConfig.java`
- `A services/booking-service/src/rca-test/resources/application-rca-test.yaml`
- `A services/booking-service/src/rca-test/test-java/com/flashticket/booking_service/RcaFaultsTests.java`
- `A services/booking-service/src/rca-test/test-java/com/flashticket/booking_service/RcaFaultsWebConfigTests.java`
- `A services/event-service/src/rca-test/java/com/flashticket/event_service/testing/RcaFaults.java`
- `A services/event-service/src/rca-test/java/com/flashticket/event_service/testing/RcaFaultsWebConfig.java`
- `A services/event-service/src/rca-test/resources/application-rca-test.yaml`
- `A services/event-service/src/rca-test/test-java/com/flashticket/event_service/RcaFaultsTests.java`
- `A services/event-service/src/rca-test/test-java/com/flashticket/event_service/RcaFaultsWebConfigTests.java`

