# Chuẩn quan sát B16 (log JSON, CI kiểm log, OpenTelemetry Java agent tắt) trên main mới nhất

PR này **làm lại** PR #17 trên `main` `85b5033` (28/11/2026). Nhánh `rca/quan-sat-log` được dựng lại từ main và đẩy đè; nội dung cũ `bb84d64` được giữ theo bảng giữ/bỏ bên dưới. Chỉ một PR.

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

Gỡ 13 xung đột của PR cũ với main `f178870` theo code main, rồi rebase lên `6b77144`: thêm 2 xung đột ở `deploy/k8s/{event,ticket}-service/configmap.yaml` (giữ dòng `SPRING_APPLICATION_JSON` của main, chỉ thêm khối `OTEL_*`); rebase lên `4d57225`: 1 xung đột ở `services/payment-service/.env.example` (giữ khối replica của main và khối `OTEL_*`); rebase lên `f0a5d30` (main tạm một Pod, đổi script CD): không xung đột; rebase lên `85b5033` (Payment định tuyến PostgreSQL theo transaction read-only, bỏ cờ reader): 1 xung đột ở `services/payment-service/.env.example` (giữ phần của main, thêm khối `OTEL_*`). Ba file Java: `OrderServiceImpl` (giữ `orderViewAssembler`), `PromotionServiceImpl` (bỏ import `OrderMapper` main đã thay), `RefundServiceImpl` (main bỏ đường VNPay refund; telemetry `refund-result` chuyển vào `sendRefund`).

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
- Lượt sau (REVIEW-8): listener Payment chọn kết cục theo bước đã làm trên kênh (lệnh ACK/NACK ném lỗi, kể cả lỗi của proxy Spring khi kênh đóng, ghi `UNKNOWN`; chỉ NACK giao lại thành công mới ghi `RETRY`); log outbox Payment có `correlationId`.
- Lượt sau (REVIEW-10): listener Ticket và consumer định danh của User ghi `UNKNOWN/BROKER_COMMAND_FAILED` khi chính lệnh ACK/NACK/reject lỗi; User ghi quyết định sau khi lệnh trả về.

## Bật agent sau này (không thuộc PR này)

Chỉ thêm: Collector 1 pod (`deploy/k8s/otel-collector/`, lọc dữ liệu nhạy cảm trước khi gửi ra ngoài cụm), đường CD cho image dựng sẵn, `SPRING_AUTOCONFIGURE_EXCLUDE` cho service dùng Redis; sửa nhỏ: `OTEL_AGENT_ENABLED` → `"true"` và nâng giới hạn bộ nhớ của service bật. Chi tiết: `deploy/observability/README.md`.

## Hoàn tác

**Điều kiện trước merge:** nếu Booking, Event hoặc Ticket đang bật đọc replica, CD từ chối image mới khi thiếu bản writer-only cùng image; nhóm chuyển về writer-only trên bản đang chạy trước khi merge. Điều kiện số Pod của bản nền khác nhau theo service (`deploy-k8s-service.sh` tại đầu PR):

- **Booking:** bản nền cho reader phải là bản 2 Pod (HPA 2/2); bản một Pod chỉ là writer-only tạm.
- **Event, Ticket:** bản writer đòi HPA 1/1, cùng cấu hình và cùng image với bản đích.
- **Payment** (từ main `85b5033`): không còn cờ reader và `writer-baseline`; đọc replica theo transaction read-only qua `PG_RO_HOST`. CD từ chối Secret còn khóa cũ (`RETIRED_PAYMENT_DB_KEYS`). Payment không cần lịch writer-only khi merge PR này.

Người giữ cấu hình xác nhận cả trạng thái reader **đang chạy** lẫn **định phát** của ba service này; `writer-baseline` có thể còn sau khi đã tắt reader.

**Đích hoàn tác.** CD `rollback` đọc file `previous` **ghi sau lần phát PR này**, không phải file `previous` đọc trước merge.

- Trước merge: ghi `current` (gọi là C0) của từng service.
- Sau lần phát, `previous` là:
  - `writer-baseline` của revision mới, nếu CD ghi file này (Booking, Event, Ticket khi đang hoặc vừa dùng reader);
  - Discovery: `compatible-previous`, nếu lần phát hoàn tất migration;
  - còn lại: C0.
- Phát lỗi giữa chừng, CD **thử** khôi phục; kết quả tùy trường hợp:
  - lỗi kiểm cấu hình (reader, profile) trước khi áp workload: CD dừng, workload cũ vẫn chạy, không có bước khôi phục;
  - Discovery đang chuyển từ Deployment cũ mà áp/kiểm lỗi trước khi xong migration: CD khôi phục **Deployment cũ** (`RESTORED_LEGACY_DISCOVERY`), không phải `compatible-previous`; khôi phục lỗi thì `DISCOVERY_RESTORE_FAILED`, giữ cả hai workload;
  - lỗi áp/kiểm thông thường: CD thử áp lại `previous`; chỉ khi áp và kiểm lại đều đạt mới in `RESTORED_PREVIOUS`; có thể ra `RESTORE_FAILED` (cần người xử lý) hoặc `NO_PREVIOUS_K8S_REVISION`.
  - Discovery đang chuyển từ Deployment cũ có hai mã dừng **trước** mọi bước khôi phục: `DISCOVERY_MIGRATION_FINALIZE_FAILED` (bước kết thúc chuyển đổi lỗi sau khi áp và kiểm đích đạt; workload có thể đã đổi trong khi con trỏ còn cũ) và `LEGACY_APPLICATION_UNDRAIN_FAILED` (đưa ứng dụng cũ trở lại phục vụ lỗi). Gặp hai mã này thì CD chưa thử khôi phục: kiểm workload đang phục vụ và các con trỏ (`current`, `previous`) trước khi chọn đích.
  - Vì vậy sau một lần phát lỗi, đọc thông báo CD và workload thật đang phục vụ (image, số Pod) trước khi kết luận đã về đích nào.
- Trước khi bấm `rollback`: đọc file `previous` cùng image và profile (số Pod, reader) của đích. Đích không như mong muốn thì dùng PR revert (cũng qua CD).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
