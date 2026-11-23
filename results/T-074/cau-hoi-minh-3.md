# T-074 — Câu hỏi cho Minh, bản 3 (bổ sung bản 2)

Soạn 22/11/2026, Claude (phiên `danh-gia-w6`). Bản 3 = `cau-hoi-minh-2.md` (Q-W6-01…08) + các câu mới và sửa dưới đây, theo Codex CX-08 điểm 1–7. Sửa so bản 2: **Q-W6-06 việc 3 rút lại** (hai chu kỳ E6 không phân xử được DB, `thiet-ke-w6-3.md` §G); **Q-W6-08** số vé theo `du-toan-3.json` (còn 46.402 cho W7 theo mô hình, sau D1 và lượt E3; đọc lại ở E6). Chi tiết ở `thiet-ke-w6-3.md`.

## Q-W6-09. Dung sai ghép G của độ đo phát hiện (`thiet-ke-w6-3.md` §A)

- **Đề xuất:** G = 370 s là quy ước chính (= `for` 60 + `eval_interval` 10 + cửa sổ rate 300 của luật đã khóa, `results/T-072/bieu-thuc.json`); G = 120 s báo phụ, gọi là "mục tiêu vận hành". TP phát hiện do t̂ quyết định; trạng thái RCA (đủ phủ / thiếu phủ / A vượt biên chu kỳ) báo cột riêng, ca vẫn trong mẫu số.
- **Mặt trái:** dung sai dài làm dễ ghép cảnh báo không liên quan; sự cố ghép muộn cần dữ liệu RCA tới S+1870, quá biên chu kỳ S+1800 → runner phải chờ thêm tối đa ~70 s + thời gian xả (chưa đo) hoặc chấp nhận A lẫn đầu chu kỳ sau.
- **Phương án khác:** chỉ G = 120 s (đơn giản, không vượt biên; nhưng phạt luật vì độ trễ do chính cấu hình, không đo đúng "luật đã khóa có phát hiện không").

## Q-W6-10. Báo động giả ở mức tải ×3 (`thiet-ke-w6-3.md` §B.3)

- **Đề xuất:** giữ nguyên bộ phân loại phút của T-071 (chỉ có `khoe_x1`). Ở ×1 tính "báo động giả mỗi giờ khỏe ×1" trên phút `khoe_x1` trong đoạn âm. Ở ×3 chỉ báo "sự cố trên giờ quan sát ×3"; câu báo động giả mỗi giờ khỏe ×3 để OPEN.
- **Mặt trái:** không có kết luận báo động giả cho ×3.
- **Phương án khác:** định nghĩa `khoe_x3` trước W7 (cùng tiêu chí K1–K5, B1–B2, mức kỳ vọng theo hệ số tải), ghi WHY; tiêu chí mới chưa kiểm trên dữ liệu ×3 nào.

## Q-W6-11. Baseline gặp đầu vào nhiều chuỗi runtime (`thiet-ke-w6-3.md` §C.2)

- **Đề xuất:** ghi `LOI_ADAPTER_DA_CHUOI`, giữ trong mẫu số chính như trượt, báo riêng số ca; không gộp chuỗi cho baseline.
- **Mặt trái:** baseline thua ở ca như RECREATE-PAY vì giới hạn adapter chứ không vì chất lượng xếp hạng (báo riêng để tách).
- **Phương án khác:** cho mọi baseline dùng bước nối chuỗi H8a như tiền xử lý chung bổ sung, khai rõ; BARO/SimpleRCA khi đó lệch đường dữ liệu P3, và phép so V082–baseline không còn chứa phần lợi H8a.

## Q-W6-12. Ô mốc đo trôi DB khi giữ K0 (`thiet-ke-w6-3.md` §F)

- **Đề xuất:** dùng lại 3 đối chứng BINH-THUONG ×1 có sẵn làm ô mốc, đặt cố định một ô ở cùng vị trí trong mỗi khối (ví dụ chu kỳ đầu). Tiết kiệm 3 chu kỳ (~1,6 giờ, 1.944 đơn).
- **Mặt trái:** ba đối chứng này không còn trộn; vị trí gắn với thời gian; K ×1 đo ở vị trí cố định.
- **Phương án khác:** thêm 3 chu kỳ mốc riêng, đối chứng vẫn trộn (A+B+CPU-EVENT thành 60 chu kỳ, ~31,4 giờ, 76.464 đơn bảo thủ — vượt 46.402).
