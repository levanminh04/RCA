# T-074 E6 · Hai lệnh kiểm chỉ đọc

**Bước 1c.** `b1c-yen.sh` nhóm đơn theo `lifecycle_state`, in đủ sáu trạng thái và cộng `PENDING_PAYMENT` với `ISSUING` để lấy số đơn chưa kết thúc. Mỗi lần đọc cần đúng một cặp held/purchased, một số outbox cho từng DB và số liệu RabbitMQ. Script in từng hàng đợi khác 0, dừng khi thiếu số hoặc khi lệnh lỗi, giữ mã psql/RabbitMQ.

Theo nháp 3 §5 bước 2 và nháp 5 §3, khi người trực đã xác nhận thời gian không tải, truyền số phút qua `--phut-khong-tai N`. `YEN` cần N ≥ 10 và tất cả chỉ số yêu cầu bằng 0. `purchased` chỉ để đối chiếu. Chỉ số bận hoặc N < 10 trả `KHONG_YEN` (mã 1). Nếu số đo sạch nhưng thiếu N, script yêu cầu người trực đối chiếu (mã 2). Lỗi đọc có dấu `LOI_THU_THAP`, kể cả khi trùng mã 1.

**Nguồn FlashTicket tại `36a3725`.** DDL trong `docs/architecture/data/postgres/` khai bảng `outbox_messages`. Khi khởi tạo, `deploy/postgres/00-business-databases.sh` áp dụng `services/99-table-prefix.sql` để thêm tiền tố `tbl_`. Cả bốn truy vấn đếm `published_at IS NULL`, gồm cả bản tin đang chờ thử lại.

| DB | Bảng sau khởi tạo | Nguồn DDL và mã dịch vụ (đường dẫn từ gốc repo FlashTicket) |
|---|---|---|
| event_db | event_schema.tbl_outbox_messages | `docs/architecture/data/postgres/10-event.sql:145`, `services/event-service/src/main/java/com/flashticket/event_service/messaging/OutboxStore.java:108` |
| booking_db | booking_schema.tbl_outbox_messages | `docs/architecture/data/postgres/20-booking.sql:177`, `services/booking-service/src/main/java/com/flashticket/booking_service/entity/OutboxMessage.java:14,51` |
| ticket_db | ticket_schema.tbl_outbox_messages | `docs/architecture/data/postgres/40-ticket.sql:76`, `services/ticket-service/src/main/java/com/flashticket/ticket_service/entity/OutboxMessage.java:14,51` |
| payment_db | payment_schema.tbl_outbox_messages | `docs/architecture/data/postgres/30-payment.sql:147`, `services/payment-service/src/main/java/com/flashticket/payment_service/entity/OutboxMessage.java:18,73` |

Miền trạng thái đơn nằm ở `docs/architecture/data/postgres/20-booking.sql:23`. Trạng thái cuối khi phát vé thất bại được giải thích ở `docs/java-workflow/specs/2026-10-30-booking-event-cancellation-design.md:65`.

**Bước 0.** `b0.sh` dùng cùng phép dò tên thực thi và đối số trên ba máy. PID và PID cha xác định cây lệnh dò cần bỏ. Script đọc hết crontab. Chỉ mã 1 kèm đúng thông báo `no crontab for <user hiện tại>` được hiểu là chưa có lịch. Mã 0 của bước 0 cho biết đã thu được bằng chứng. Người trực vẫn xét tiến trình, cron và các mục theo nháp 4 §4 bước 0.

| Ca giả lập | Kết quả bản cuối |
|---|---|
| Số sạch với N = 10, N = 9, hoặc thiếu N | Lần lượt `YEN`/0, `KHONG_YEN`/1, đối chiếu/2 |
| Truy vấn đơn lỗi, RabbitMQ lỗi, thiếu bảng ticket | `LOI_THU_THAP`, lần lượt mã 3, 1, 3 |
| Thiếu trạng thái đơn, kho, số outbox hoặc hàng đợi; outbox lặp số; RabbitMQ sai định dạng | Mã 2 |
| Đơn chưa xong, held, outbox hoặc hàng đợi đầu tiên khác 0 | In số bận, `KHONG_YEN`/1 |
| `k6 --quiet run load.js`, `runner4.py --output /tmp/grep.log`; cron lạ ở dòng 5 | Thấy hai tiến trình và dòng cron trên cả ba máy |
| Máy sạch, không có crontab; lỗi ps/docker/ssh/crontab/git/timer | Phân biệt sạch với lỗi. Lỗi thu thập trả khác 0 và nêu máy, bước |

Chạy `bash chay-thu.sh` bằng Git Bash trên laptop. [Lượt 3](luot-3.out) kiểm lại đúng bộ thử của [lượt 2](luot-2.out). Cả hai script qua `bash -n`, 36/36 ca đạt. [Lượt 1](luot-1.out) ghi kết quả trước khi bổ sung kiểm đủ từng trạng thái đơn. Chạy `sha256sum -c SHA256SUMS` trong thư mục này để kiểm hai script v3, bộ thử, ghi chú và cả ba đầu ra.

## Ngoài phạm vi

Chưa kiểm trên PostgreSQL, RabbitMQ hay ba máy thật. Đề nghị Claude bổ sung cách gọi ở nháp 6 §2 bước 0. Chạy `bash v3/b0.sh app` trên exp-app và `bash v3/b0.sh obs` trên exp-obs để thu cả máy tải. Với mỗi lần kiểm yên trước/sau dump, ghi nguồn xác nhận thời gian không tải rồi chạy `bash v3/b1c-yen.sh --phut-khong-tai N` với số phút thực tế. Nếu bỏ đối số như lệnh hiện ghi trong nháp, dù số đo sạch script vẫn trả 2. SQL thuận B ở v2 và phục hồi bằng dump thuộc phần Claude. Phần sửa CX-45 chờ phiên Codex khác kiểm độc lập.
