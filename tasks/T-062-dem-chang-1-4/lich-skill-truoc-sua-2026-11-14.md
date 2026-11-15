---
name: m1ft-tiep-nhan
description: Mỗi giờ kiểm checkpoint chiến dịch M1-FlashTicket; nếu không có phiên điều phối nào đang hoạt động thì tiếp quản theo PROMPT-PHIEN-MOI.md.
---

Thư mục làm việc: D:\RCA-flashticket. Đây là lịch tự tiếp nhận chiến dịch M1-FlashTicket (Minh cho phép tạo ngày 13/11/2026).

Bước 1. Đọc D:\RCA-flashticket\tasks\T-062-dem-chang-1-4\CHECKPOINT-CHIEN-DICH.md (đặc biệt các mục "Nhịp tim" cuối file). Lấy giờ UTC hiện tại. Chưa ghi nhịp tim hoặc thay tên phiên điều phối ở bước này.

Bước 2. Quyết định:
- Nếu tồn tại file D:\RCA-overnight\STOP: không làm gì, thoát.
- Nếu checkpoint ghi chiến dịch đã xong M4 hoặc ghi "DỪNG LỊCH": không làm gì, thoát.
- Kiểm phiên điều phối và các tiến trình/session/lệnh nền ghi trong checkpoint bằng trạng thái thực tế (công cụ liệt kê session của ứng dụng: phiên Claude "điều phối" có đang chạy không; tiến trình python/codex trên máy; file trạng thái results/*/codex/*-trang-thai.json). Nếu chủ cũ còn hoạt động (phiên điều phối đang chạy, hoặc nhịp tim mới hơn 45 phút), không phát thêm điều phối hay công việc trùng, thoát lượt lịch.
- Nhịp tim cũ hơn 45 phút là dấu hiệu cần kiểm thêm. Xác định chủ cũ đã kết thúc hoặc dừng (ví dụ hết hạn mức) và trạng thái các lệnh con trước khi tiếp quản. Nếu chưa phân xử được, giữ các lệnh đang chạy và báo đúng phần chưa rõ, không ghi đè quyền sở hữu.
- Khi đã xác nhận có thể tiếp quản, đọc prompt ở bước 3 rồi ghi phiên mới/nhịp tim và tiếp tục từ đầu ra hợp lệ. Không phát lại lượt đã xong chỉ vì đổi phiên.

Bước 3 (chỉ khi tiếp quản). Đọc D:\RCA-flashticket\tasks\T-062-dem-chang-1-4\PROMPT-PHIEN-MOI.md và làm đúng theo khối prompt trong file đó (gồm đọc AGENTS.md, các SPEC, quyền ở docs/DECISIONS.md mục "Bổ sung quyền điều phối chiến dịch nhiều ngày"). Cập nhật hạn mức theo thông báo thực tế, các giờ cũ trong checkpoint là lịch sử. Tiếp tục tới M4, sau báo cáo sáng hoặc báo cáo mốc vẫn làm phần trong quyền. Gọi Codex bằng results/T-063/dieu-phoi/goi_codex.py (--che-do sandbox; tiếp phiên bằng --tiep-phien).