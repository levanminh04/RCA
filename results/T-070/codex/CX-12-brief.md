Việc phụ CX-12 (chỉ đọc; không sửa file, không commit, không mạng; SSH KHÔNG được dùng). Minh yêu cầu: kiểm các phiên Claude làm việc có bị ảnh hưởng bởi các lần hết hạn mức (20/11 ~22Z, 21/11, 22/11 ~06–07Z và ~10–11Z) không, và tránh việc kết luận vội để kịp hạn mức.
Phạm vi: bốn task T-071 (tasks/T-071-w4a-nen/, results/T-071/), T-072 (tasks/T-072-w4b-luat-canh-bao/, results/T-072/), T-073 (tasks/T-073-w5-rca-truc-tuyen/, results/T-073/), T-074 (tasks/T-074-w6-thiet-ke-danh-gia/, results/T-074/) trong D:/RCA-flashticket; worktree D:/Project/rca-lab-wt/T-071, T-072, T-073, T-073-e5, T-070-e3; nhật ký điều phối D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md và TRANG-THAI.json.
Với mỗi task, kiểm trên file thật (không tin tóm tắt LOG):
1. Mục LOG cuối có mục kết thúc lượt đầy đủ không; có lượt nào dừng giữa chừng (bước ghi "đang chạy"/"chờ" mà không có dòng kết thúc) — liệt kê.
2. Mọi file kết quả LOG nói đã có thì có thật, hash khớp manifest tương ứng (chạy sha256sum -c ở đúng thư mục; ghi số khớp/lệch). Có file dở (rỗng, cắt cụt, JSON hỏng) không.
3. Kết luận nào ghi mạnh hơn bằng chứng (ví dụ "đạt", "xác nhận", "đủ", "mọi") mà file chỉ là nháp, mẫu nhỏ, chưa chạy, hoặc ghi "chưa kiểm" ở chỗ khác; kết luận nào viết sau khi phiên báo sắp hết hạn mức mà thiếu phép kiểm đã hứa.
4. Có ghi ra ngoài phạm vi SPEC/HOP-DONG (I9, I10) không; có sửa file đã khóa/đã ghim (khai-truoc-e2.json b63f2e09, khai-truoc-e4.json 463cf596, khai-truoc-e5.json, khoa-boc-e5.json, results/T-069 SHA256SUMS*) không.
5. Đối chiếu TRANG-THAI.json và LOG T-070 với LOG từng task: chỗ nào lệch (trạng thái, hash, giờ).
Cuối: bảng theo task — vấn đề, mức CHẶN/KHÔNG CHẶN, bằng chứng (file:dòng, lệnh), sửa tối thiểu. Nếu không có vấn đề, nói thẳng. Tiếng Việt, ngắn.
