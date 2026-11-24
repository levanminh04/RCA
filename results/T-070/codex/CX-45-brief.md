Yêu cầu của Minh (22/11): KHÔNG dùng subagent hay agent con; tự làm toàn bộ trong phiên này. Đọc có chọn lọc (grep, đọc đúng đoạn cần), không đọc lại toàn bộ file lớn khi không cần.

Bạn là phiên Codex SỬA LỖI NHỎ cho T-074 E6, repo D:\RCA-flashticket. Đọc AGENTS.md trước (Luật 0, luật cứng 1, 7, 21).

Căn cứ quyền: Minh duyệt ngày 24/11/2026 "Duyệt kết hợp" cho E6: giữ SQL thuận v2 biến thể B; Codex sửa ngay các lỗi nhỏ
mà hai bên đã đồng thuận (quy tắc Minh 24/11: lỗi nhỏ hai bên đồng thuận thì Codex sửa luôn), một phiên Codex khác kiểm;
hoàn tác bằng khôi phục dump (phần này do Claude T-074 làm, KHÔNG phải việc của bạn).

PHẠM VI GHI (chỉ được tạo các file sau, không sửa/xóa file nào khác, kể cả results/T-074/e6/v2/ và mọi SHA256SUMS cũ):
- results/T-074/e6/v3/b1c-yen.sh   (bản sửa của results/T-074/e6/v2/b1c-yen.sh)
- results/T-074/e6/v3/b0.sh        (bản sửa của results/T-074/e6/v2/b0-v2.sh)
- results/T-074/e6/v3/thu-codex/   (phép thử giả lập của bạn: script, docker/ssh giả, đầu ra .out, SHA256SUMS cho 2 script trên và bộ thử)
- results/T-074/e6/v3/thu-codex/GHI-CHU.md (ngắn: sửa gì, vì sao, bảng ca thử và kết quả, giới hạn còn lại)
Không SSH, không kết nối DB hay máy nào, không commit, không dùng subagent. Thư mục v3/ khác do Claude T-074 ghi song song: không đụng.
Nếu thấy cần sửa ngoài phạm vi trên (ví dụ chay.sh, SQL, nháp E6): KHÔNG sửa; ghi đề xuất vào GHI-CHU.md mục "Ngoài phạm vi".

Lỗi phải sửa (đã được hai phiên Codex CX-41 và CX-41b xác nhận ĐÚNG · CHẶN; đọc results/T-070/codex/CX-41-tin-cuoi.md và CX-41b-tin-cuoi.md):
1. b1c-yen.sh (kiểm yên trước dump và ghi, CHỈ SELECT):
   - `GROUP BY 1` trên biểu thức chứa count(*) → nhóm theo lifecycle_state.
   - Outbox: xác định ĐÚNG bảng outbox và cột mốc gửi của từng dịch vụ (event, booking, ticket, payment) từ mã nguồn FlashTicket
     D:/Project/flash-ticket-platform tại commit 36a3725 (migration/entity; chỉ đọc, dùng git show/grep, không checkout). Ghi đường dẫn bằng chứng vào GHI-CHU.
     Truy vấn tường minh từng bảng; đòi đủ bốn kết quả số.
   - Giữ mã lỗi của psql và rabbitmqctl; script trả khác 0 khi bất kỳ truy vấn nào lỗi hoặc thiếu kết quả; in rõ từng số
     (đơn chưa kết thúc theo trạng thái, held/purchased, 4 số outbox, hàng đợi khác 0) để người trực đối chiếu với tiêu chí yên
     ở results/T-074/e6-spec-nhap-3.md, e6-spec-nhap-5.md. Tham khảo cách ghi mốc E1: results/T-071/e1/moc/.
   - Nếu đủ rõ từ nháp: thêm chế độ đánh giá tự động (YEN/KHONG_YEN) theo tiêu chí đã có trong nháp; không tự đặt tiêu chí mới — nếu nháp chưa định lượng, chỉ in số và ghi "người trực đối chiếu".
2. b0.sh (bước 0, CHỈ ĐỌC, ba máy):
   - Nhận diện tiến trình theo tên thực thi và đối số (ví dụ `k6 --quiet run x.js`, `python3 runner4.py --output /tmp/grep.log` phải bị bắt);
     chỉ loại PID của chính lệnh dò (và tiến trình con của nó), không loại cả dòng vì có chữ grep.
   - Đọc đủ crontab (không head -3) ở cả máy chính và máy tải.
   - Phân biệt "lỗi thu thập" (ps/docker/ssh/crontab lỗi) với "không có tiến trình": lỗi thu thập → in LOI_THU_THAP và trả khác 0.
   - Giữ nguyên các phần còn lại của b0-v2.sh (git, docker ps, STOP, compose, máy tải qua khóa bộ điều khiển, inj, paused, toxics, lease, timers) trừ khi chúng có cùng loại lỗi.
3. Phép thử giả lập (bash trên laptop, docker/ssh/ps/crontab giả): phải có ít nhất các phản ví dụ CX-41/41b
   (docker trả 3 cho truy vấn đơn; rabbitmqctl trả 1; thiếu bảng outbox; `k6 --quiet run load.js`; `runner4.py --output /tmp/grep.log`; crontab có dòng lạ ở dòng 5)
   cộng ca sạch đạt. Chạy `bash -n` cả hai script. Ghi đầu ra thật của lần chạy vào thu-codex/*.out.

Tự kiểm trước khi kết thúc: diff v2→v3 của hai script; mọi ca thử đạt; không file nào ngoài phạm vi bị đổi (`git status --porcelain` trước/sau, chỉ liệt kê thay đổi trong results/T-074/e6/v3/b1c-yen.sh, b0.sh, thu-codex/).
Cuối lượt báo (tiếng Việt, ngắn): 1. Đã làm gì. 2. File đã tạo. 3. Kiểm đã chạy và kết quả. 4. Điều chưa chắc, ngoài phạm vi, cần Minh/Claude quyết.
