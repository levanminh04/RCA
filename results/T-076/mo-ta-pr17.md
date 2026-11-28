# Chuẩn quan sát B16 (log JSON, CI kiểm log, OpenTelemetry Java agent tắt) trên main mới nhất

PR này **làm lại** PR #17 trên `main` `f0a5d30` (28/11/2026). Nhánh `rca/quan-sat-log` được dựng lại từ main và đẩy đè; nội dung cũ `bb84d64` được giữ theo bảng giữ/bỏ bên dưới. Chỉ một PR.

## Thay đổi khi chạy thật (máy 84)

- **Log B16:** 7 service Spring (discovery, gateway, user, event, ticket, booking, payment) ghi log JSON theo `docs/architecture/B16-observability-baseline.md`: trường cố định, stacktrace không chứa nội dung exception, correlation ID, log sau commit ở điểm nghiệp vụ. Không đổi logic nghiệp vụ.
- **`ENVIRONMENT=production`, `HOST_ID` = tên node** (downward API): ghi vào trường `environment`, `hostId` của log.
- **OpenTelemetry Java agent 2.33.1 có trong image nhưng tắt cứng**: `OTEL_AGENT_ENABLED: "false"` trong `env:` của `deployment.yaml` (thắng mọi giá trị từ ConfigMap/Secret). Khi tắt, service chạy `java -jar` như cũ, không gửi dữ liệu đi đâu.
- File mẫu Secret (`deploy/k8s/examples/`) **không đổi**.

## CI

- Bước kiểm mẫu log B16 sau `verify`, chỉ cho service trong `deploy/observability/b16-services.txt`; service trong danh sách thiếu file mẫu là lỗi.
- `detect-changes.sh`: đổi `deploy/observability/` chỉ build lại service trong danh sách.
- `SERVICE_VERSION={github.sha}` truyền vào image (giữ build hai kiến trúc của main).

## Giữ / bỏ so với PR cũ (`bb84d64`, 124 file)

| Quyết định | Số file | Gồm |
|---|---|---|
| Giữ | 93 | Mã B16 (lớp quan sát, chèn log ở file nghiệp vụ, 6 DTO bỏ `@Valid` trùng), test B16, hook `rca-test`, `application.yaml`, `pom.xml`, `.dockerignore`, `.env.example` của service, chuẩn B16, hunk `SERVICE_VERSION`, GOV-150..156 |
| Sửa khi áp | 17 | 7 Dockerfile (dựng trên Dockerfile main, chèn agent), 7 entrypoint, 2 file CI (B16 theo danh sách), README quan sát (viết lại theo K8s) |
| Bỏ | 14 | `deploy/app/*` (Compose dự phòng), tracing Keycloak, chẩn đoán Postgres, `.env.example`/`.gitignore` gốc |

Gỡ 13 xung đột của PR cũ với main `f178870` theo code main, rồi rebase lên `6b77144`: thêm 2 xung đột ở `deploy/k8s/{event,ticket}-service/configmap.yaml` (giữ dòng `SPRING_APPLICATION_JSON` của main, chỉ thêm khối `OTEL_*`); rebase lên `4d57225`: 1 xung đột ở `services/payment-service/.env.example` (giữ khối replica của main và khối `OTEL_*`); rebase lên `f0a5d30` (main tạm một Pod, đổi script CD): không xung đột. Ba file Java: `OrderServiceImpl` (giữ `orderViewAssembler`), `PromotionServiceImpl` (bỏ import `OrderMapper` main đã thay), `RefundServiceImpl` (main bỏ đường VNPay refund; telemetry `refund-result` chuyển vào `sendRefund`).

Thêm: `deploy/k8s/<svc>/configmap.yaml` có khối biến chỉ agent đọc (đích `http://otel-collector:4318` — Collector trong cụm, **chưa có**), `deploy/observability/b16-services.txt`, agent cho `assistant-service` (không log B16), sửa hook `rca-test` của Booking để test slice chạy được với `-P rca-test`.

## Đã kiểm (local, trước khi đẩy)

- Trên main `f178870`: `verify` 8/8 service, kiểm B16 7/7. Sau rebase lên `6b77144`, chạy lại cho 4 service main đổi code (user, event, ticket, booking): user 70, event 178, ticket 229, booking 453 test, 0 lỗi; B16 đạt cả 4; Event `-P rca-test` 186, Booking `-P rca-test` 462 test, 0 lỗi; Ticket `TicketPostgresIT` 22 đạt.
- Bộ kiểm K8s của repo trên `6b77144` (`test-k8s-deploy.py`, `test-k8s-discovery.py`, `test-k8s-rollout-hooks.py`, `test-https-config.py`) 4/4; `test-k8s-deploy-routing.sh` cần `jq`, để CI chạy.
- Image Booking, Assistant: chạy bằng uid 10001, agent đúng checksum, `SERVICE_VERSION` = commit. Image Booking build lại sau rebase.
- Agent tắt: kể cả khi Secret giả có `OTEL_AGENT_ENABLED=true`, giá trị cuối là `false`, không có dòng khởi động agent, không gửi dữ liệu.

## Sửa sau phản biện trước merge (28/11)

- Kết cục log khớp hành vi thật: callback VNPay chưa rõ ghi `UNKNOWN`; listener Payment/Booking ghi `RETRY` khi bản tin được giao lại, `REJECTED` khi bị loại; outbox ghi `PUBLISH_FAILED` cho lỗi không thuộc broker, `retryCount` là số lần thử lại. Không đổi ACK/NACK, mã lưu DB hay lịch retry.
- Correlation: tạo đơn trả `X-Correlation-Id` = orderId; phản hồi lỗi của Booking dùng cùng mã với log.
- Discovery có `ENVIRONMENT=production`, `HOST_ID`, `OTEL_AGENT_ENABLED="false"`. ConfigMap bỏ khóa MDC trace/span tùy chỉnh của agent; Event không ghi span của bên gọi thành span hiện tại.
- `BookingPersistenceIT` trỏ vào đúng hàm nhận tin; `-P integration` 173 test đạt.
- Sau rebase lên `4d57225` (main đổi Payment): Payment `verify` 153 + 57 test, 0 lỗi, B16 đạt; manifest 8 service; bộ kiểm K8s chạy lại.
- Lượt sau (REVIEW-6): kênh RabbitMQ đóng khi ACK/NACK ở Payment ghi `UNKNOWN`, không ghi `RETRY`; tạo đơn ghi dòng `order.correlation-linked` nối correlation tạm với orderId (B16 §3); outbox Payment/Ticket không dời lịch được (worker khác đã nhận) ghi `UNKNOWN/LEASE_CHANGED`.

## Bật agent sau này (không thuộc PR này)

Chỉ thêm: Collector 1 pod (`deploy/k8s/otel-collector/`, lọc dữ liệu nhạy cảm trước khi gửi ra ngoài cụm), đường CD cho image dựng sẵn, `SPRING_AUTOCONFIGURE_EXCLUDE` cho service dùng Redis; sửa nhỏ: `OTEL_AGENT_ENABLED` → `"true"` và nâng giới hạn bộ nhớ của service bật. Chi tiết: `deploy/observability/README.md`.

## Hoàn tác

**Điều kiện trước merge:** nếu Booking, Event, Ticket hoặc Payment đang bật đọc replica, CD từ chối image mới khi thiếu bản writer-only cùng image; nhóm chuyển về writer-only trên bản đang chạy trước khi merge. Trên main hiện tại, bản một Pod không làm baseline cho reader được (baseline phải là bản 2 Pod).

**Đích hoàn tác.** CD `rollback` đọc file `previous` **ghi sau lần phát PR này**, không phải file `previous` đọc trước merge.

- Trước merge: ghi `current` (gọi là C0) của từng service.
- Sau lần phát, `previous` là:
  - `writer-baseline` của revision mới, nếu CD ghi file này (Booking, Event, Ticket, Payment khi đang hoặc vừa dùng reader);
  - Discovery: `compatible-previous`, nếu lần phát hoàn tất migration;
  - còn lại: C0.
- Phát lỗi giữa chừng: CD tự khôi phục về cùng đích này.
- Trước khi bấm `rollback`: đọc file `previous` cùng image và profile (số Pod, reader) của đích. Đích không như mong muốn thì dùng PR revert (cũng qua CD).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
