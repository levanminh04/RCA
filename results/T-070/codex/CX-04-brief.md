Việc phụ CX-04 (chỉ đọc; không sửa file, không SSH, không commit, không mạng). Soát bản nháp-5 D:/RCA-flashticket/results/T-071/khai-truoc-e2.json trước khi khóa và phát E2 (W4, khoảng nền 1).
Ngữ cảnh: SPEC D:/RCA-flashticket/tasks/T-071-w4a-nen/SPEC.md; hợp đồng D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md (I2, I11); LOG T-070 mục "Lượt 4"; luật W4 D:/RCA-flashticket/results/T-072/bieu-thuc.json, quy-tac-gom.json, quy-tac-chon-nguong.json; bộ chuỗi D:/Project/rca-lab-wt/T-071/load/controller/chuoi_tai.py (bản đã commit).
Kiểm, mỗi câu ĐÚNG/SAI/ĐÚNG MỘT PHẦN kèm con trỏ JSON hoặc file:dòng:
K1. Không tiêu chí xếp phút "khỏe" nào dùng chuỗi hoặc tín hiệu mà luật W4 (bieu-thuc.json) dùng để cảnh báo (p95/5xx theo route gateway, httpcheck liveness, mất quan sát) — tức một báo động giả không thể tự loại phút của nó khỏi mẫu số.
K2. Phút bị loại vì lý do độc lập (k6, backend, quota, biên, mất quan sát hạ tầng) vẫn được giữ cùng cảnh báo phát sinh trong đó, và được báo riêng.
K3. Danh sách lượt đúng R7: 8 lượt (6 ×1 3600 s; 2 flash 1800 s bậc ×3 ở 600 s), không lượt bù; tag khớp regex của tai_linux và chưa dùng.
K4. Tiêu chí, ngưỡng (k6, quota) và quy tắc biên có giá trị số cố định, không còn mục "CHỜ"/"chưa kiểm" làm thay đổi phân loại sau khi xem dữ liệu.
K5. Cách tính phút khỏe ×1 khớp quy-tac-gom.json (380 phút ×1/khoảng; "chưa đủ sáu giờ khỏe ×1" khi < 360).
Cuối: lỗi thật (CHẶN/KHÔNG CHẶN + sửa tối thiểu) hoặc nói không có. Tiếng Việt, bảng ngắn.
