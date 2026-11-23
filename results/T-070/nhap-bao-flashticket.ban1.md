# Bản nháp báo nhóm FlashTicket — truy vấn nền quét tuần tự (Q8)

**Trạng thái:** bản nháp do phiên điều phối T-070 soạn ngày 23/11/2026 theo Q8 (`docs/techstack/ban-giao-dieu-phoi-2026-11-20/thong-nhat.md` §1.4). **Chưa gửi.** Gửi hay không, gửi cho ai, sửa chữ thế nào là quyết định của Minh (R3: không gửi gì ra ngoài khi Minh chưa quyết). Số liệu lấy từ `results/T-069/phan-tich-nguyen-nhan.md` §4, `results/T-069/phan-tich/kiem-db.txt`, giới hạn theo `results/T-069/dinh-chinh-1.md`.

---

**Tiêu đề:** Hai truy vấn nền của Booking và Ticket đang quét tuần tự bảng đơn/vé; chậm 7–9 lần khi dữ liệu tăng khoảng 10 lần

Chào nhóm FlashTicket,

Trong lúc chạy thực nghiệm RCA trên bản FlashTicket `36a3725d` (môi trường thử nghiệm, dữ liệu tích lũy từ các lượt tải), nhóm RCA quan sát thấy một số truy vấn nền chậm dần theo kích thước bảng. Chúng tôi gửi số đo để nhóm tham khảo. Đây là quan sát trên môi trường thử, chưa phải chẩn đoán trên production.

**1. Kích thước bảng** (đếm ngày 19/11/2026; cột "trước" đếm theo `created_at`, giả định không xóa dòng):

| Bảng | Số dòng hiện tại | Tạo trước 13/11 | Kích thước |
|---|---|---|---|
| `booking_schema.tbl_orders` | 37.477 | 3.713 | 61 MB |
| `ticket_schema.tbl_ticket_deliveries` | 24.438 | 2.412 | 10 MB |
| `ticket_schema.tbl_issuances` | 24.438 | 2.412 | 46 MB |

**2. Truy vấn nền chậm đi** (p50 thời lượng span, cùng câu lệnh, lúc hệ thống không có lỗi):

| Truy vấn | Khi bảng nhỏ | Khi bảng lớn |
|---|---|---|
| Booking: `tbl_orders where lifecycle_state=? and expires_at<=?` (worker hết hạn đơn) | 3,93 ms | 34,77 ms |
| Booking: `tbl_orders join tbl_reservations …` | 6,33 / 5,69 ms | 42,60 / 24,60 ms |
| Ticket: `tbl_ticket_deliveries join tbl_issuances …` (giao vé) | 2,66 ms | 19,17 ms |

**3. Kế hoạch thực thi và thống kê bảng:**
- `EXPLAIN` một câu rút gọn của truy vấn hết hạn đơn cho `Seq Scan on tbl_orders`, dù bảng có chỉ mục `orders_expiry_idx (expires_at)`.
- `pg_stat_user_tables`: `tbl_issuances` 7.141.875 lượt quét tuần tự, khoảng 93 tỷ dòng đọc; `tbl_ticket_deliveries` 7.330.618 lượt, khoảng 93 tỷ dòng đọc.
- CPU trung bình của PostgreSQL lúc nền tăng từ 0,06–0,09 lõi lên 0,29–0,41 lõi (máy 2 vCPU); CPU của các service ứng dụng gần như không đổi.

**4. Giới hạn — những gì chúng tôi chưa khẳng định:**
- Chưa chạy `EXPLAIN ANALYZE` trên câu lệnh đầy đủ, nên chưa biết vì sao bộ lập kế hoạch không dùng `orders_expiry_idx`. Ứng viên: điều kiện `lifecycle_state` kém chọn lọc, hoặc thống kê bảng cũ.
- `EXPLAIN` đã lưu là của câu Booking rút gọn, không phải kế hoạch của truy vấn Ticket.
- Chúng tôi **không** kết luận dữ liệu tích lũy là nguyên nhân duy nhất của độ trễ: trong cùng giai đoạn, image và code đường mua vé của Booking cũng đổi, và máy thử có tranh chấp CPU. Một số mẫu chậm nhất của Ticket là câu `count(*)` có trung vị không đổi (0,30 ms), khớp với tranh chấp CPU hơn là bảng lớn.
- Số liệu từ một môi trường thử 2 vCPU với tải tổng hợp; production có thể khác.

**5. Gợi ý để nhóm kiểm (nếu thấy cần):** chạy `EXPLAIN (ANALYZE, BUFFERS)` cho hai truy vấn worker ở trên trên dữ liệu cỡ tương tự; xem chỉ mục ghép theo điều kiện thực tế của worker (ví dụ `(lifecycle_state, expires_at)`) hoặc `ANALYZE` lại bảng.

Nhóm RCA có thể gửi thêm span thô hoặc script đếm nếu nhóm cần.

---

*Ghi chú cho Minh (không gửi):* bỏ hoặc sửa mục 5 nếu không muốn đưa gợi ý kỹ thuật; tên người gửi, kênh gửi do Minh chọn. Bản nháp không nêu địa chỉ máy, khóa hay dữ liệu cá nhân.
