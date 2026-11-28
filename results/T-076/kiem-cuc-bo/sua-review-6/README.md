# Kiểm bản sửa theo REVIEW-6 (28/11/2026)

Nhánh local `rca/quan-sat-log-dung-lai` @`cd21f17`, rebase lên main `f0a5d30` (PR #59, tạm một Pod, đổi script CD). Bản sửa là commit cuối (11 file). Trước rebase: `943962b` trên `f40b849` (còn trong reflog). Minh duyệt sửa ngày 28/11 (LOG T-076 Phiên 7). Chưa push.

`git range-diff 4d57225..f40b849 f0a5d30..cd21f17`: 8 commit cũ trùng nguyên (`=`), thêm 1 commit. Rebase không xung đột. `git diff --check f0a5d30 cd21f17` sạch. Commit không đổi file K8s, CI hay script.

## Thay đổi

| Điểm | File | Sửa |
|---|---|---|
| R3 | Payment `PaymentMessageListener.java` (5 hàm bọc) | `catch (IOException \| ShutdownSignalException)` → `UNKNOWN/BROKER_COMMAND_FAILED`, đặt trước `RuntimeException`. Kênh đóng khi ACK sau commit, hay khi NACK, không còn ghi `RETRY/TRANSACTION_UNAVAILABLE` |
| R4 | Booking `BusinessTelemetry.correlationLinked`, `OrderController.createOrder` | khi correlation trong MDC (mã tạm) khác orderId: ghi `eventName=order.correlation-linked`, `correlationId` = mã tạm, `orderId`, `outcome=SUCCESS`, `reasonCode=ORDER_CORRELATION_ASSIGNED` |
| R5 | Payment `MessagingService(Impl).rescheduleOutbox` → `boolean`; `PaymentWorker` | không dời được lịch (đã published hoặc lease khác) → `UNKNOWN/LEASE_CHANGED`; message log theo bước ("…after broker confirm" / "…unconfirmed") |
| R5 | Ticket `TicketOutboxPublisher.java` | lấy số hàng của lệnh dời lịch; 0 hàng → `UNKNOWN/LEASE_CHANGED` |

Không đổi điều kiện DB, mã lưu DB (`last_error_code`), lịch dời, ACK/NACK.

Test mới: Payment `ListenerTelemetryTests` +2 (ACK ném `AlreadyClosedException` sau commit; NACK ném lỗi kênh), `worker/PaymentWorkerTelemetryTests` 2 (dời được / lease đổi); Ticket `TicketPostgresIT.outboxFailureAfterLeaseChangeIsNotLoggedAsRetry` (Postgres thật, worker khác tăng `attempts` lúc chờ confirm); Booking `OrderControllerTests` (tạo đơn) kiểm dòng nối với header `X-Correlation-Id` mã tạm. Ca ACK của Payment phân biệt được bản cũ và bản mới: bản cũ cho `RETRY`. Spotless áp cho 3 service, chỉ đổi file đã sửa.

## Kết quả

| Kiểm | Kết quả | File |
|---|---|---|
| `verify` + B16 (`chay-verify.sh`) | payment 157 + 57, ticket 229, booking 457 test, 0 lỗi; B16 PASS cả 3 | `verify/tien-do.tsv`, `verify/log/` |
| Booking `-P rca-test verify` | 466, 0 lỗi | `verify/log/booking-service-rca-test-verify.log` |
| Booking `-P integration verify` | 457 + 173, 0 lỗi | `verify/log/booking-service-integration-verify.log` |
| Ticket `TicketPostgresIT` | 23 đạt (22 cũ + 1 mới) | `verify/log/ticket-service-postgres-it.log` |
| Bộ kiểm K8s, lượt 1 (python venv B16) | 3/4 **hỏng hạ tầng**: venv không có `yaml` (`ModuleNotFoundError`); `test-k8s-discovery.py` đạt. Giữ log | `verify/log/test-*.log` |
| Bộ kiểm K8s, lượt 2 (`py -3`, PyYAML 6.0.2) | 4/4 đạt trên main `f0a5d30` (gồm fixture một Pod mới của main) | `verify/k8s-py3/` |

Không chạy lại: Event (không đổi code), manifest 8 service (commit không đổi file K8s, 8 commit cũ trùng), image/agent (không đổi Dockerfile, entrypoint). `test-k8s-deploy-routing.sh` cần `jq`, để CI chạy như các lượt trước.

**Chưa kiểm:** CI trên GitHub cho đầu mới (sau khi Minh duyệt push); hành vi trên cụm thật (bước 6–7).
