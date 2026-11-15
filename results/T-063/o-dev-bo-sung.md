# T-063 — Ô phát triển bổ sung (nháp 1, 12/11/2026 22:07Z — chưa cài, chưa xác nhận can thiệp)

Không sửa T-059. Mọi ô dưới ở **vị trí khác** ô đánh giá của `results/T-059/danh-muc-loi.json` (đánh giá: DB-BOOK-LAT, POOL-BOOK, DB-BOOK-DOWN, REDIS-GW, TICKET-PAUSE, HTTP5-BOOK, SLOW-EVENT, NET-GW-EVENT, NET-PAY-BOOK, CPU-EVENT, VNPAY-REFUND-LAT, SAGA-TICKET-FAIL). Ô dev T-059 giữ nguyên (EVENT-DB-LAT, REDIS-BOOK, HTTP5-EVENT, SLOW-BOOK, NET-GW-BOOK, CPU-BOOK, FLASH-HEALTHY). Tập chấp nhận khai trước; ô chưa được đầu dò xác nhận không vào tập chọn.

| Mã | Hướng phân xử | Cách tiêm (ứng viên) | Đầu dò độc lập | Xác nhận khi | Tập chấp nhận | Trạng thái |
|---|---|---|---|---|---|---|
| POOL-EVENT | H3 | Hook `src/rca-test` của Event chiếm connection Hikari có giới hạn, tự nhả (cơ chế như POOL-BOOK của T-059 — 2i-B, chưa có hook pool) | `db_client_connections_*` của pool Event qua Prometheus + JMX/actuator đọc Active/Idle/Pending (ngoài cửa sổ hoặc không qua span) | Active = max, Idle = 0, pending > 0; DB trực tiếp khỏe | event-service | **thiếu hook pool** (Booking/Event mới có hook HTTP delay/error) → cần cài hook trong `src/rca-test` (không phải code nghiệp vụ) |
| CONSUMER-BOOK-SLOW | H4 | Toxiproxy trên kết nối AMQP của Booking (proxy mới `booking-amqp`, độ trễ downstream) → consumer xử lý chậm, queue `booking.*.q` tồn | `rabbitmq_message_current{ready}` theo queue (TD-02), số consumer; publish vs ack | ready tăng ở queue của Booking, ack/s giảm, broker khỏe với client khác | booking-service, cạnh booking-service→broker | cần tải mua vé (message Saga) + trỏ AMQP của Booking qua proxy (tạo lại container Booking) |
| PAUSE-PAYMENT | H5 | `docker pause` payment-service (khác Ticket của TICKET-PAUSE) | `httpcheck` liveness (đề xuất H5), docker state | liveness lỗi/timeout trong suốt pha, tiến trình còn (`Paused=true`) | payment-service | cần `httpcheck` (bước 5) |
| SLOW-BOOK-FLASH | H7 | SLOW-BOOK (cùng hook/cường độ) dưới tải ×3 (FLASH) | như SLOW-BOOK + lưu lượng gateway | như SLOW-BOOK; tải tăng đúng hệ số | booking-service | theo `split_rules` "Phát triển" T-059 (cùng lỗi ở hai mức tải) |
| CPU-BOOK-1 | H2 | 1 luồng đốt trong cgroup Booking (quota 1,0) | `nr_throttled`, PSI, throttling Prometheus (TD-03) | Booking ~1 lõi, throttle thấp; PSI máy tăng ≤ ×2 (`cpu-book/PHAN-TICH.md`) | booking-service | sẵn (đổi `workers`) |
| CPU-BOOK-2 | H2 | = CPU-BOOK T-062 (2 luồng) | như trên | throttle ≥ 80% chu kỳ | booking-service | sẵn — dùng lại định nghĩa T-062 (giữ để đo nhiễu hàng xóm) |

Ghi chú: CPU-BOOK-2 trùng cường độ ô CPU-BOOK của T-059 (dev); CPU-BOOK-1 là ô bổ sung. Lý do giữ cả hai: `results/T-063/cpu-book/PHAN-TICH.md` §4.

## Ghi chú 12/11 22:50Z — hook HTTP và tải mua vé mới

- `services/*/src/rca-test/.../RcaFaults.java:103`: `http.error`/`http.delay` **bắt buộc** `targetId`; Booking còn bắt buộc `subject` (dòng 129). `~/inj.py` (T-062) nhắm `ORDER_ID` fixture cho SLOW-BOOK và `EVENT_ID` fixture cũ cho HTTP5-EVENT.
- Tải mua vé của L1 dùng sự kiện mới `3e7c1df9-ada4-4081-94a1-548b80a5da86` và **đơn mới mỗi hành trình** → SLOW-BOOK như cũ không chạm lưu lượng thật; HTTP5-EVENT phải đổi `target` sang sự kiện mới (không cần build lại).
- `pool.hold` (giá trị 1–5 connection, không cần target) có sẵn ở Booking và Event → POOL-EVENT làm được nếu 5 connection đủ làm cạn pool Event (cần đọc `db_client_connections_max` của pool Event — **chưa kiểm**).
- Phương án cho SLOW-BOOK: (a) hook nhận target đại diện "mọi đơn" — sửa `src/rca-test` (module kiểm thử, không phải code nghiệp vụ) + build lại image Booking/Event với `-P rca-test`; (b) giữ hook, thêm bước "tra cứu đơn cố định" vào tải. Chưa quyết.
- Kiểm 22:47Z (`db_client_connections_max` trên Prometheus): pool Hikari của event, ticket, booking, payment đều **max = 5**, idle_min 1. → POOL-EVENT dùng `pool.hold` có sẵn: giá trị 4 (còn 1 connection — bão hòa một phần, request phải chờ) là ứng viên; 5 = cạn hoàn toàn. Xác nhận bằng `db_client_connections_pending_requests` > 0 và `usage{state=used}` = 5. Không cần build lại.

## Thu bù 3 — 14/11/2026 (phiên B; trạng thái đầy đủ ở `thu3/KE-HOACH.md`, `thu3/BAN-GIAO-B.md`)

Các dòng trên giữ nguyên làm lịch sử. Bảng này ghi định nghĩa ô dùng trong đợt thu bù 3 trên **bản 3** (Event `arm64-t063h3-76b34d5e`, `thu3/thay-doi-may.md`). Điều kiện xác nhận: `thu3/dieu-kien-xac-nhan-3.md`.

| Mã | Hướng | Cách tiêm (đã cài, `thu3/scripts/inj3.py`) | Cường độ | Đầu dò độc lập | Tập chấp nhận | Trạng thái trước đợt |
|---|---|---|---|---|---|---|
| POOL-EVENT | H3 | hook `pool.hold` Event (sửa `RcaFaults.java`, commit `e557307`) | 5 connection / pool max 5, 600 s | audit `pool.hold.started`; Prometheus `db_client_connections_usage{state=used}`, `pending_requests` | event-service | chạy thử đạt (`thu3/KE-HOACH.md` bổ sung 2) |
| CONSUMER-BOOK-SLOW-X3 | H4 | toxic bandwidth downstream `booking-amqp`, tải ×3 suốt chu kỳ | 1 KB/s, 600 s | `rabbitmqctl` ready/unacked `booking.*.q`, `send_oct` kết nối Booking | booking-service; cạnh booking-service ↔ broker | chạy thử đạt (bổ sung 3) |
| BINH-THUONG-X3 | đối chứng H4 | không can thiệp, tải ×3 | — | như BINH-THUONG | — | — |
| RECREATE-PAY | H8-adapter | `docker compose … up -d --force-recreate --no-deps` payment-service tại t, cùng image/env | một lần | `docker inspect` Id/StartedAt; httpcheck :8083 | payment-service | yêu cầu phiên C (`results/T-064/phien-c/YEU-CAU-O.md`); chưa chạy thử trước đợt |

Ô cũ chạy lại trên bản 3 để so: BINH-THUONG, EVENT-DB-LAT (cách tiêm như đợt 2). CONSUMER-BOOK-SLOW (×1) của dòng trên: không xác nhận được ở đợt 2, không thu lại ở ×1.
