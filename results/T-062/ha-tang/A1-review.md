# A1 — review diff FlashTicket và PR (T-062, 12/11/2026)

Repo `D:/Project/flash-ticket-platform`, nhánh `rca/quan-sat-log`, PR **nháp** levanminh04/flash-ticket-platform#17 vào `main` (không merge). Sao lưu trước khi đụng: `D:/RCA-ext/backup-flashticket-20261112/`.

## Commit trên nhánh

| Commit | Nhóm |
|---|---|
| `f7e6207` feat(observability) | chuẩn log B16 cho 7 service (allowlist chung, định danh chung SERVICE_VERSION/ENVIRONMENT/HOST_ID/INSTANCE_ID, SafeStackTracePrinter, BusinessTelemetry ghi sau commit, RabbitTelemetry, Gateway log mọi request), test |
| `40bf552` ci(observability) | `_maven-verify.yml` kiểm mẫu log B16 bằng `deploy/observability/verify_logs.py` |
| `a3aa316` build | OTel Java agent 2.33.1 trong image (tắt mặc định), entrypoint, image amd64+arm64, Keycloak native tracing |
| `f022f44` deploy | mem_limit, nhãn log Docker, chẩn đoán PostgreSQL, SQL reader |
| `84e794f` test(rca) | hook tiêm lỗi chỉ ở `src/rca-test` (profile `rca-test`), `deploy/rca-test/` |
| `ac33155` docs | GOV-150..156 |
| `6b21ed5` merge | đồng bộ `origin/main` (15 commit mới); gỡ 4 xung đột: giữ cả hai phía ở `OrderServiceImpl`, `PromotionServiceImpl`; `OrderPage` theo main; workflow giữ bước QEMU của main + build-arg SERVICE_VERSION |

CI trên đầu `6b21ed5`: 14 check đạt (7 Maven có test đầy đủ + kiểm mẫu log B16, keycloak, CodeQL, Dependency Review, Deploy scripts, Detect changes, Required), Frontend bỏ qua, 0 lỗi. Kiểm local trước push: 7 service `mvnw verify -DskipTests` và booking/event `-P rca-test` đạt.

## Đã soát (không thấy lỗi chặn)

- Telemetry nghiệp vụ không đổi luồng nghiệp vụ: `BusinessTelemetry.committed` chép giá trị, đăng ký `afterCommit` (không log khi rollback); các `Map.of(...)` đều nhận giá trị không null (UUID khóa chính, cột `nullable=false`, correlation do controller sinh).
- `RabbitTelemetry` khôi phục MDC trong `close()`; `PaymentMessageListener` đặt MDC bên trong try-with-resources nên không rò sang message sau.
- Log customizer 4 service (Event/Ticket/User/khác) thống nhất; trường `traceId/spanId` lấy từ MDC agent, kiểm định dạng hex.
- `docker-entrypoint.sh`: dừng (exit 64) nếu `JAVA_TOOL_OPTIONS` còn `-javaagent:` hoặc `OTEL_RESOURCE_ATTRIBUTES` khai định danh — **phải dọn secret `ENV_*` trước khi deploy production** (ghi trong mô tả PR).
- Line ending: `.gitattributes` `eol=lf`, entrypoint là LF.
- Không có bí mật trong 62 file mới (quét mẫu password/secret/token/apikey có giá trị).

## Ghi chú (không chặn, để Minh/nhóm xem)

1. Bỏ `@Valid` ở cấp danh sách trong 6 DTO Booking (giữ `@Valid` ở phần tử) — tương đương hành vi, nhưng là dòng ngoài phạm vi log (Codex sửa trước đó).
2. Hai dòng `log.info` của `FinanceController` bị bỏ, thay bằng `BusinessTelemetry` trong service (cùng thông tin, có actor/state).
3. Gateway ghi INFO mọi request — lượng log tăng theo tải (đúng quy tắc §4e mới).
4. Lỗi có sẵn trên `main`, không do PR: `GET /api/v1/orders/{id}/tickets` trả 500 thay vì 404 vì `GlobalExceptionHandler` (bắt `Exception`) đứng trước `TicketApiExceptionHandler` (không có `@Order`). Sửa tối thiểu đề xuất: `@Order(Ordered.HIGHEST_PRECEDENCE)` cho `TicketApiExceptionHandler` — **chờ Minh**.
5. Event `GET /api/v1/events/{id}` chạy khoảng 30 lượt đọc DB mỗi request (đo gián tiếp ở D2: +200 ms mỗi phản hồi DB → +6,3 s) — có thể N+1; để nhóm xem.
6. Merge vào `main` = `cd.yml` triển khai production máy 84. Trước khi merge: dọn `ENV_*` theo `deploy/app/README.md`, xem lại mem_limit tăng.
