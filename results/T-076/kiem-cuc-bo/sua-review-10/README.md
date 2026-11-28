# Kiểm bản sửa theo REVIEW-10 (28/11/2026)

Nhánh local `rca/quan-sat-log-dung-lai` @`e086fdc` trên `e19fc53` (đầu PR #17 lúc soát); main `f0a5d30` không đổi (`git fetch` 28/11), không rebase. Bản sửa là commit cuối (4 file: 2 mã, 2 test). Minh duyệt sửa ngày 28/11 ("Duyệt, cả user-service"). Chưa push. `git diff --check f0a5d30 e086fdc` sạch.

## Thay đổi

| Điểm | File | Sửa |
|---|---|---|
| R1 | Ticket `messaging/TicketBusinessListeners.java` | đặt `UNKNOWN/BROKER_COMMAND_FAILED` ngay trước `basicReject`/`basicNack`/`basicAck`; kết cục cụ thể (`REJECTED`, `RETRY`, `SUCCESS`) sau khi lệnh trả về |
| N1 | User `identity/IdentityConsumer.java` (mã main, PR trước đó không đụng) | `brokerCommand()` chạy lệnh kênh, lỗi → quyết định `UNKNOWN/BROKER_COMMAND_FAILED` rồi ném lại; quyết định `REJECTED`/`RETRY`/`SUCCESS` ghi **sau** khi lệnh trả về |
| R2 | `results/T-076/mo-ta-pr17.md` (repo RCA) | hai mã dừng trước khôi phục của Discovery (`DISCOVERY_MIGRATION_FINALIZE_FAILED`, `LEGACY_APPLICATION_UNDRAIN_FAILED`) và bước kiểm workload, con trỏ |

Test: Ticket `TicketListenerTests` thêm kiểm log cho ca ACK lỗi có sẵn, ca reject/NACK thành công, và hai ca mới reject lỗi, NACK lỗi; User `IdentityConsumerTests` thêm 4 ca (ACK, NACK, reject lỗi; thành công). Spotless áp cho hai service, chỉ đổi file đã sửa.

## Kết quả

| Kiểm | Kết quả | File |
|---|---|---|
| Test mới trên `e086fdc` | Ticket `TicketListenerTests` 10, User `IdentityConsumerTests` 8, 0 lỗi | lệnh trong LOG |
| Cùng test, mã chính trả về `e19fc53` (`git stash` 2 file chính) | Ticket 3 failure, User 3 failure (đúng các ca lệnh kênh lỗi) → test phân biệt được | lệnh trong LOG |
| `chay-verify.sh` | Ticket verify 231, `TicketPostgresIT` 23, User verify 74, 0 lỗi; B16 PASS cả hai | `verify/tien-do.tsv`, `verify/log/` |

Không chạy lại: Payment, Booking, Event (không đổi code), bộ kiểm K8s (không đổi file K8s/CD, main không tiến), image/agent.

**Chưa kiểm:** CI trên GitHub cho đầu mới (sau khi Minh duyệt push); hành vi trên cụm thật (bước 6–7).
