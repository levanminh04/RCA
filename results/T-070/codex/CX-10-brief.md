Việc phụ CX-10 (chỉ đọc; không sửa file, không SSH, không commit, không mạng). Soát D:/RCA-flashticket/results/T-071/khai-truoc-e4.json (nháp) trước khi khóa và phát E4.
Đối chiếu với: bản khóa E2 D:/RCA-flashticket/results/T-071/khai-truoc-e2.json (b63f2e09…); quyết định D1 (E4 = 8 lượt như E2 + 1 lượt ×1 1800 s, cùng quy tắc phân loại) và D2 (giữ cấu hình E2 qua E4) ở D:/RCA-flashticket/docs/DECISIONS.md mục cuối và D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md lượt 6; R5, R7; quy tắc gom D:/RCA-flashticket/results/T-072/quy-tac-gom.json (bản mới nhất, T072-gom-3); HOP-DONG D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md (I2, I11); bộ chuỗi D:/Project/rca-lab-wt/T-070-e3/load/controller/chuoi_tai.py.
Kiểm (ĐÚNG/SAI/ĐÚNG MỘT PHẦN kèm con trỏ JSON hoặc file:dòng):
K1. Đúng 9 lượt theo D1, tag chưa dùng, đúng regex tai_linux; không lượt bù.
K2. Quy tắc phân loại phút, tiêu chí khỏe, biên, quota, B1/B2/L1 GIỐNG bản khóa E2 (trừ phần thời gian/tag); không còn mục CHO.
K3. Mẫu số R5 tính đúng (khoe_x1, ≥ 360 phút; trần 383 khi lệch giây) và khớp T072-gom-3; chỉ tính sau giờ hiệu lực E4.
K4. Mục lỗi 10/50/99% (luật 21) đầy đủ và đúng hành vi chuoi_tai.py.
K5. Có chỗ để điền giờ hiệu lực E4 trước khi khóa; khóa trước khi xem dữ liệu E4.
Cuối: lỗi CHẶN/KHÔNG CHẶN + sửa tối thiểu, hoặc nói không có. Tiếng Việt, bảng ngắn.
