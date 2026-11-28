# Kiểm bản sửa theo REVIEW-8 (28/11/2026)

Nhánh local `rca/quan-sat-log-dung-lai` @`e19fc53` trên `cd21f17` (đầu PR #17 lúc soát), main `f0a5d30` không đổi (`git fetch` 28/11), nên không rebase. Bản sửa là commit cuối (5 file Payment). Minh duyệt sửa ngày 28/11 (LOG T-076). Chưa push. `git diff --check f0a5d30 e19fc53` sạch.

## Thay đổi

| Điểm | File | Sửa |
|---|---|---|
| R1 | Payment `observability/RabbitTelemetry.java`, `messaging/PaymentMessageListener.java` (5 hàm bọc) | `track(channel)` bọc `Channel` bằng proxy JDK, ghi bước: `basicAck`/`basicNack` ném lỗi (client RabbitMQ hoặc proxy Spring) → `UNKNOWN/BROKER_COMMAND_FAILED`; `basicNack(requeue=true)` trả về bình thường → `RETRY/TRANSACTION_UNAVAILABLE`; còn lại `FAILED`. Hợp đồng sai giữ `REJECTED/INVALID_CONTRACT`. Không đổi lệnh, tham số, thứ tự, chữ ký hàm trong |
| R4 | Payment `worker/PaymentWorker.java` | hai dòng `payment.outbox.result` thêm `correlationId` từ dòng outbox |
| R2, R3 | `results/T-076/mo-ta-pr17.md` (repo RCA) | điều kiện số Pod theo hai nhóm service; ba trường hợp khi phát lỗi |

Test mới: Payment `ListenerTelemetryTests` +2 (`IllegalStateException("Channel closed; cannot ack/nack")` ở ACK sau commit và ở NACK → `UNKNOWN`); `PaymentWorkerTelemetryTests` thêm kiểm `messageId` và `correlationId` khác nhau. Spotless áp cho Payment, chỉ đổi file đã sửa.

## Kết quả

| Kiểm | Kết quả | File |
|---|---|---|
| Test mới trên mã `e19fc53` | `ListenerTelemetryTests` 8, `PaymentWorkerTelemetryTests` 2, 0 lỗi | lệnh trong LOG |
| Cùng test, mã chính trả về `cd21f17` (`git stash` 3 file chính) | 4 failure: hai test proxy Spring, hai test worker → test phân biệt được bản cũ | lệnh trong LOG |
| Payment `verify` + B16 (`chay-verify.sh`) | 159 + 57 test, 0 lỗi; B16 PASS | `verify/tien-do.tsv`, `verify/log/` |

Không chạy lại: Booking, Ticket, Event (không đổi code), bộ kiểm K8s (không đổi file K8s/CD, main không tiến), image/agent (không đổi Dockerfile, entrypoint).

**Chưa kiểm:** CI trên GitHub cho đầu mới (sau khi Minh duyệt push); hành vi trên cụm thật (bước 6–7).
