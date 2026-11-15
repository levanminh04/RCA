# Ghi chú của Claude (viết 22:30Z ngày 10/11/2026, khi Claude hết usage)

Claude hết usage lúc khoảng 22:30Z nên **ngừng giám sát**. Codex vẫn chạy tiếp tự động:
- `guard/launcher2.sh` chạy Codex, tự chờ và resume khi Codex hết usage, dừng hẳn lúc 00:00Z (07:00 giờ Việt Nam).
- `guard/watchdog2.sh` vẫn tự dừng Codex nếu có thay đổi trong repo RCA, repo FlashTicket, thư mục khóa, hoặc nhánh mới trên GitHub do `levanminh04` tạo. Không chặn máy 84 (chỉ ghi cảnh báo).
- Từ 23:15Z Codex viết `out/bao-cao-sang.md`, rồi tạo `out/DONE.md`.

## Sáng mai Minh xem theo thứ tự
1. `out/bao-cao-sang.md` (báo cáo của Codex) và `out/DONE.md`.
2. `guard/ALERT.txt`: các dòng "VI PHAM" (nếu có) nghĩa là Codex đã bị dừng vì vượt phạm vi. Các dòng ref `refs/pull/...` và "trang thai may 84 thay doi" lúc 20:24Z là của nhóm (Tuyến push `73c10fa5`, CD deploy lại `user-service` trên 84), không phải Codex.
3. `out/LOG-dem.md`, `out/huong-dan-trien-khai.md`, `out/kiem-agent.md`, `out/STEER.md` (4 chỉ đạo Claude đã gửi).

## Claude đã kiểm độc lập trong đêm
- 8 image ARM build đúng commit của máy 84 (đọc nhãn image lúc 19:46Z).
- FlashTicket chạy trên `exp-app`: 6 service UP trong Eureka, gateway trả 200.
- Kho quan sát ghim phiên bản trên `exp-obs`, chỉ mở trong mạng nội bộ; trace, log, metric về đủ 8 service.
- **Thiếu span Redis** (lưu lượng Redis có thật; nguyên nhân OPEN). RabbitMQ có span khi có lưu lượng thật.
- **booking-service bị OOM 2 lần** ở giới hạn 512 MiB của nhóm khi gắn agent; Codex nâng giới hạn trong bản compose riêng của `exp-app` (booking, payment, event 1 GiB; keycloak 1,5 GiB; discovery 768 MiB). Đây là lệch cấu hình so với máy 84; heap JVM cũng tăng theo vì `MaxRAMPercentage=50`. Các cửa sổ đo trước 21:50Z có sự cố không nhãn.
- Kế hoạch M1 bản 1 (21:15Z) giữ nguyên; bản 2 (21:52Z) khóa trước khi có đầu ra M1. Cửa sổ bình thường 22:01–22:11Z sạch; tạm dừng `event-service` 22:17–22:22Z, đã phục hồi.

## Chưa làm, cần Minh hoặc phiên sau
- Rà đầu ra M1 (chạy sau 22:23Z) và báo cáo sáng của Codex; chưa có ai phản biện.
- Chép kết quả từ `out/` vào repo RCA (`results/T-058/`, `src/m1/adapter_flashticket.py`) chỉ sau khi Minh duyệt; cập nhật LOG T-058, STATE, đính chính SPEC; commit.
- `exp-app` chạy `user-service` ở commit `22067803`, cũ hơn máy 84 một commit (nhóm deploy `73c10fa5` lúc 20:09Z).
- PR cách B (CD đa kiến trúc) chưa làm.
