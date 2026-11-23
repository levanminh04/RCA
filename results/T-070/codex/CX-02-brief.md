Việc phụ CX-02 (chỉ đọc; không sửa file, không SSH, không commit, không chạy mạng).
Soát code file mới D:/Project/rca-lab-wt/T-071/load/controller/chuoi_tai.py (sha256 73a0105f…, chưa commit) so với D:/Project/rca-lab-wt/T-071/load/controller/tai_linux.py (commit 407b4f5) và kế hoạch D:/RCA-flashticket/results/T-071/khai-truoc-e2.json. Ngữ cảnh luật: D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md (I7, I8, I11), D:/RCA-flashticket/tasks/T-071-w4a-nen/SPEC.md mục "Chi phí, chạy nền, xử lý lỗi".
Trả lời từng câu ĐÚNG / SAI / ĐÚNG MỘT PHẦN, kèm file:dòng:
C1. Tag mỗi lượt được ghi (có fsync) vào nhật ký TRƯỚC khi gọi `tai_linux.py start`; chạy lại cùng lệnh không start lại tag đã ghi.
C2. Mọi lệnh `stop` đều có `--tag`; không đường nào gọi stop không tag.
C3. Chuỗi dừng trước lượt kế khi: STOP, file DUNG, commit /opt/rca-lab đổi hoặc cây bẩn, 2 lượt liền không start, 0 mẫu gateway.
C4. Lỗi cục bộ một lượt không dừng chuỗi; không có lượt bù tự động.
C5. Đúng 8 lượt theo kế hoạch (6 ×1 3600 s, 2 flash 1800 s bậc 600 s ×3), tham số truyền sang tai_linux đúng tên cờ (--seconds, --buoc-tai, --multiplier, --tag).
C6. Truy vấn Prometheus của chuỗi chỉ nhẹ (bao nhiêu truy vấn mỗi lượt, cửa sổ bao lâu).
C7. Có đường nào làm chuỗi chết giữa chừng mà không ghi trạng thái (ngoại lệ không bắt, mã hóa stdout, hết thời gian subprocess), hoặc làm mất/ghi đè đầu ra receive.
Cuối: liệt kê lỗi thật (nếu có) theo mức CHẶN/KHÔNG CHẶN; không có thì nói không có. Tiếng Việt, bảng ngắn.
