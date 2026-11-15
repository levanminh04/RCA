# T-063 thu3 — Đề xuất mục WHY (phiên B ghi; phiên điều phối chép vào `docs/WHY.md` trước khi T-064 dùng kết quả)

Ba mục, đánh số theo thứ tự còn trống khi điều phối chép (sau WHY-86 nếu chưa có mục mới). Số liệu dẫn file trong `results/T-063/thu3/`.

## (a) T-063 — Build lại riêng Event từ `6b21ed55` + bản vá hook H3, thu trên "bản 3"

- **Chọn gì:** sửa `RcaFaults.java` của Event (bỏ phép so tên service ở `start()` và `poll()` để `pool.hold` chạy ở Event; điều kiện `subject` của `http()` giữ nguyên), commit `e557307` trên `rca/quan-sat-log`. Image Event build từ worktree tách tại `6b21ed55` (bản đang chạy) + đúng bản vá đó → commit cục bộ `76b34d5e`, image `ft-local/event-service:arm64-t063h3-76b34d5e`. Sáu service khác, env, compose, Collector, Toxiproxy giữ nguyên.
- **Vì sao:** POOL-EVENT không thử được vì hook chỉ chạy ở Booking (`chay/D2B-KET-QUA.md`); Minh duyệt sửa hook (DECISIONS 14/11). Không build từ đầu nhánh `fba6bc8` vì nhánh đã merge code nghiệp vụ mới của Event (bỏ API thống kê) — sẽ đổi hành vi ngoài hook.
- **Phương án đã xét:** (1) build từ `fba6bc8`: loại vì đổi code nghiệp vụ; (2) chấp nhận H3 "chưa thử được": loại vì Minh đã cho sửa; (3) chọn đúng nền `6b21ed55` + bản vá: chọn.
- **Bằng chứng:** `thu3/thay-doi-may.md` T3-03…T3-05; test `RcaFaults*` 8/8 đạt trên `exp-app`; audit `pool.hold.started` ở Event khi tiêm thử (`thu3/KE-HOACH.md` bổ sung 2).
- **Hệ quả, giới hạn:** ca thu bù 3 nằm trên bản triển khai khác bản đóng băng 2 (watchdog hook 100 ms chạy ở Event cả khi không tiêm; container Event mới). Không gộp thẳng với 13 ca bản 2; dùng BINH-THUONG và EVENT-DB-LAT trên bản 3 để so. Nhãn `service.version` của Event vẫn là `6b21ed55…` vì lấy từ env, env không đổi (image mang nhãn revision `76b34d5e`).
- **Kết luận phụ thuộc:** mọi kết quả M1 trên ô POOL-EVENT, CONSUMER-BOOK-SLOW-X3 và hai ô đối chứng bản 3.

## (b) T-063 — Cường độ POOL-EVENT = 5 connection (cạn hẳn pool max 5)

- **Chọn gì:** `pool.hold` = 5 trên pool Hikari Event (max 5), 600 s.
- **Vì sao:** quy tắc khai trước (`KE-HOACH.md` §4): chọn 4 nếu có `pending` > 0; chạy thử ×1: mức 4 cho `used` = 4, `pending` = 0 suốt pha, p50 không tăng → không có tín hiệu chờ pool. Mức 5: `used` 5, idle 0, `pending` 2–25 (tb 10,1), 5xx Event 0,18–0,34/s, p50 lên tới 10 s; 182/709 hành trình hỏng (`KE-HOACH.md` bổ sung 2; `do/thu-pool-prom.json`).
- **Phương án đã xét:** 4 (bão hòa một phần) — không đủ tranh chấp ở tải ×1; tăng tải cho mức 4 — không làm vì đổi thêm một biến so với ô cũ.
- **Hệ quả:** ô là "cạn hẳn pool", gần với triệu chứng DB không phản hồi ở phía người gọi; phân biệt dựa trên kênh pool (`used` = max, `pending` cao) và DB khỏe. Hook nhả rồi chiếm lại mỗi 120 s khi gia hạn lease.
- **Kết luận phụ thuộc:** phân xử H3 trên POOL-EVENT.

## (c) T-063 — Ô H4: toxic bandwidth 1 KB/s trên AMQP của Booking dưới tải ×3, đối chứng BINH-THUONG-X3

- **Chọn gì:** `CONSUMER-BOOK-SLOW-X3`: toxic bandwidth 1 KB/s downstream trên proxy `booking-amqp` cả pha lỗi, tải hành trình ×3 suốt chu kỳ; đối chứng `BINH-THUONG-X3` cùng bậc tải.
- **Vì sao:** đợt 2 thử 3 cách ở tải ×1 không tồn queue. Đo trên bản hiện hành: byte broker→Booking ×1 tb 469 B/s, ×3 tb 1.393 B/s (`do/do-h4a-tom-tat.json`) — ×1 thấp hơn mức giới hạn nhỏ nhất của toxiproxy (1 KB/s), ×3 cao hơn. Thử 150 s ở ×3: tồn queue Booking 0 → 109, về 0 sau gỡ, cùng một kết nối, không có log heartbeat/ngắt (`KE-HOACH.md` bổ sung 3).
- **Phương án đã xét:** (1) tải > ×3 hoặc tăng tỷ lệ mua: cần sửa `tai_linux.py`/k6 (Codex), không cần vì ×3 đạt; (2) hook làm chậm xử lý consumer trong `src/rca-test` Booking: chưa có quyền Minh; (3) chọn (×3 + bandwidth).
- **Lệch kế hoạch đã ghi:** ngưỡng khả thi khai trước 1,5 KB/s ở ×3 không đạt (1,39 KB/s); vẫn thử trực tiếp vì phép thử rẻ và có điều kiện đạt riêng đã khai (`KE-HOACH.md` bổ sung 1).
- **Hệ quả, giới hạn:** cơ chế là giới hạn thông lượng giao message tới consumer Booking, không phải khâu xử lý consumer chậm; ô chạy ở bậc tải khác 13 ca cũ (×3), nên chỉ so được với BINH-THUONG-X3. Chưa kiểm TTL/DLQ của queue khi tồn 600 s.
- **Kết luận phụ thuộc:** phân xử H4; K của ca không lỗi ở tải ×3.
