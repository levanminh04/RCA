# C1 — đang làm

18:40Z 11/11/2026. Codex đã cài Docker chính thức trên AWS, k6 1.4.2 cùng digest trên AWS và obs. Đồng hồ cả hai đã đồng bộ; không đổi giờ/cấu hình obs. AWS 8081 từ chối, 8080 trả 302. Đã tạo `/opt/rca-tai/` trên obs theo v2; chỉ container `rca-tai-*`. PKCE thành công; token chỉ ở bộ nhớ và secret obs.

Chưa chạy tải; chờ `results/T-062/ha-tang/A2-XONG`. Đã có script k6 và lệnh Start/Stop/Receive cho E1, đang kiểm.

API đọc hiện tại: event, order và order/payment 200; order/tickets 500 với đơn cũ CANCELLED (bằng chứng `tai/fixture-doc.json`). Chưa kết luận nguyên nhân. Đang rà thêm các ID từ smoke receipt cũ qua API đọc; không tạo đơn vì đã tìm thấy đơn của buyer. Sẽ kiểm lại sau A2. C1 chưa chứng minh nền ổn định.

Phạm vi C1 read-mix 50/25/15/10 không hoàn thành toàn bộ chặng 2 của kế hoạch nguồn: chặng đó còn yêu cầu đăng nhập/đặt vé trong tải và lặp hai lượt so lưu lượng gateway. Không tự chạy thêm ngoài brief.
