Việc phụ CX-09 (chỉ đọc; không sửa file, không SSH, không commit, không mạng). Soát gói commit E3 trước khi Minh duyệt. Gói sẽ là một nhánh tích hợp lab tách từ commit e9a0857 (nhánh t071-nen, đã chạy E2), cộng các file chưa theo dõi của hai worktree:
- D:/Project/rca-lab-wt/T-072: observability/grafana/provisioning/alerting/{README.md, t072-luat.yaml, t072-thu-e3.yaml.mau, t072-thu-e3-go.yaml.mau, t072-hoan-tac-n.yaml.mau}, observability/t072-bo-nhan/bo_nhan.py.
- D:/Project/rca-lab-wt/T-073: campaigns/online/*.py + README.md, observability/compose.t073-webhook.yaml.
Ngữ cảnh: D:/RCA-flashticket/results/T-072/ke-hoach-e3.md, nguong.json, bieu-thuc.json, quy-tac-chon-nguong.json; D:/RCA-flashticket/results/T-073/trien-khai-bo-nhan.md, thiet-ke.md, khai-truoc-e5.json; HOP-DONG D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md (I1, I7, I9, I12); lượt soát trước CX-07, CX-06 ở D:/RCA-flashticket/results/T-070/codex/.
Kiểm, mỗi câu ĐÚNG/SAI/ĐÚNG MỘT PHẦN kèm file:dòng:
Q1. t072-luat.yaml dùng đúng ngưỡng của nguong.json, đúng 11 luật của bieu-thuc.json, contact point http://t072-bo-nhan:9172/t072, NoData/Error xử lý như bieu-thuc.json; Grafana sẽ không nạp file .mau.
Q2. Hai service trong compose.t073-webhook.yaml (t073-webhook, t072-bo-nhan) không publish cổng, cùng mạng flash-ticket-obs-pinned_default, spool đúng vùng I9, image ghim digest; `up`/`down` theo trien-khai-bo-nhan.md không khởi động lại Prometheus/Grafana/Collector; hoàn tác có thật.
Q3. Các lỗi CX-07 (hạt bốc, down thiếu biến, thiếu bộ nhận T-072, lệch định dạng T-071/T-072, hoàn tác nạp một phần) và CX-06 #5, #6 đã sửa trong mã/tài liệu hiện có chưa.
Q4. Code campaigns/online/* không đọc sổ tiêm, đáp án, tên ô (luật cứng 6) — grep đường đọc file.
Q5. Có xung đột nào khi gộp hai worktree lên e9a0857 (cùng đường dẫn, cùng file) không.
Cuối: lỗi CHẶN/KHÔNG CHẶN kèm sửa tối thiểu, hoặc nói không có. Tiếng Việt, bảng ngắn.
