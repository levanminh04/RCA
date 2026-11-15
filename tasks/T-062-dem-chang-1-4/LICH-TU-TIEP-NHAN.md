# Lịch tự tiếp nhận `m1ft-tiep-nhan` — Minh tạo tay

Theo checkpoint lịch sử, Claude thử tạo lịch bằng công cụ scheduled-tasks lúc 12/11 ~19:22Z và **bị bộ phân loại an toàn của ứng dụng từ chối**. Chưa có bằng chứng lịch tự tiếp nhận đã được tạo và kích hoạt. Phiên điều phối kiểm trạng thái hiện tại và ghi kết quả thật. Duyệt bổ sung 13/11 cấp quyền điều phối tới M4, kết quả từ chối công cụ vẫn phải được tôn trọng. Nếu cần Minh tạo tay, nêu đúng hành động và lý do từ chối, đồng thời tiếp tục việc độc lập còn được phép.

Cách tạo (ứng dụng Claude desktop → Scheduled tasks → New): thư mục `D:\RCA-flashticket`, chạy **mỗi giờ** (cron `20 * * * *`), chế độ quyền như phiên điều phối. Ứng dụng phải đang mở thì lịch mới chạy. Dán prompt dưới đây:

```text
Thư mục làm việc: D:\RCA-flashticket. Đây là lịch tự tiếp nhận chiến dịch M1-FlashTicket.

Bước 1. Đọc D:\RCA-flashticket\tasks\T-062-dem-chang-1-4\CHECKPOINT-CHIEN-DICH.md. Lấy giờ UTC hiện tại. Chưa ghi nhịp tim hoặc thay tên phiên điều phối ở bước này.

Bước 2. Quyết định:
- Nếu tồn tại file D:\RCA-overnight\STOP: không làm gì, thoát.
- Nếu checkpoint ghi chiến dịch đã xong M4 hoặc ghi "DỪNG LỊCH": không làm gì, thoát.
- Kiểm phiên điều phối và các tiến trình/session/lệnh nền ghi trong checkpoint bằng trạng thái thực tế. Nếu chủ cũ còn hoạt động, không phát thêm điều phối hoặc công việc trùng, thoát lượt lịch.
- Nhịp tim cũ hơn 45 phút là dấu hiệu cần kiểm thêm. Xác định chủ cũ đã kết thúc hoặc bàn giao, cùng trạng thái các lệnh con trước khi tiếp quản. Nếu chưa phân xử được, giữ các lệnh đang chạy và báo đúng phần chưa rõ, không ghi đè quyền sở hữu.
- Khi đã xác nhận có thể tiếp quản, đọc prompt ở bước 3 rồi ghi phiên mới/nhịp tim và tiếp tục từ đầu ra hợp lệ. Không phát lại lượt đã xong chỉ vì đổi phiên.

Bước 3 (chỉ khi tiếp quản). Đọc D:\RCA-flashticket\tasks\T-062-dem-chang-1-4\PROMPT-PHIEN-MOI.md và làm đúng theo khối prompt trong file đó. Cập nhật hạn mức theo thông báo thực tế, các giờ cũ trong checkpoint là lịch sử. Tiếp tục tới M4, sau báo cáo sáng hoặc báo cáo mốc vẫn làm phần trong quyền.
```

Tắt lịch: xóa trong ứng dụng, hoặc ghi dòng "DỪNG LỊCH" vào checkpoint, hoặc tạo file `D:\RCA-overnight\STOP`.

Kiểm vận hành và ghi tại `results/T-063/dieu-phoi/` trạng thái bật, lần kích hoạt, cách nhận biết hết hạn mức, gọi tiếp từ checkpoint và tránh trùng phiên. Ghi rõ phép thử mô phỏng và phần thực tế đã kiểm. M0 chưa đủ bằng chứng tự phục hồi vẫn cho phép các việc độc lập trong SPEC tiếp tục.

## Trạng thái thực tế (13/11/2026 02:33Z)

Minh cho phép tạo lịch (DECISIONS mục "Đánh thức Claude bằng lịch tự tiếp nhận"). Claude tạo bằng công cụ scheduled-tasks: **đã tạo, `enabled: true`**, cron `20 * * * *` (giờ máy, có độ trễ ≤ 49 s), lần chạy đầu `2026-11-13T03:20:49Z`, lưu ở `C:\Users\84583\.claude\scheduled-tasks\m1ft-tiep-nhan\SKILL.md`, chế độ Auto. Chưa có lần kích hoạt nào; kết quả lần đầu ghi vào checkpoint. Ứng dụng phải đang mở thì lịch mới chạy (đóng thì chạy ở lần mở kế tiếp). Lịch chỉ tiếp quản khi nhịp tim checkpoint cũ hơn 45 phút và không còn phiên điều phối đang chạy.

## Sửa cơ chế 14/11/2026 (04:09Z), Minh duyệt

Căn cứ: `docs/DECISIONS.md`, mục "Sửa cơ chế lịch tự tiếp nhận".

**Vấn đề cũ:**
- Lịch chạy mỗi giờ và chỉ tiếp quản khi nhịp tim cũ hơn 45 phút.
- Một phiên tự dừng sớm mà không ghi "KẾT LƯỢT" tạo khoảng trống 15 phút tới gần 2 giờ. Ví dụ 03:06–04:21Z ngày 14/11.

**Cơ chế mới:**
- Cron `*/15 * * * *` (giờ máy, ứng dụng thêm độ trễ vài chục giây), tên "M1-FT tự tiếp nhận chiến dịch (15 phút)".
- Lượt dò chỉ đọc `DIEU-PHOI-TRANG-THAI.json`.
- Tiếp quản ngay khi phiên chủ không chạy và không còn lệnh nền của chủ.
- Nhịp tim 45 phút chỉ còn là dự phòng.

Prompt lịch hiện hành nằm ở `C:\Users\84583\.claude\scheduled-tasks\m1ft-tiep-nhan\SKILL.md`. Bản cũ chép ở `lich-skill-truoc-sua-2026-11-14.md`. Nghĩa vụ của phiên điều phối ghi trong `PROMPT-PHIEN-MOI.md`.

**Hoàn tác:**
- đặt lại cron `20 * * * *`;
- dán lại prompt từ bản chép;
- bỏ qua file trạng thái.

**Chi phí:** khoảng 96 lượt dò mỗi ngày. Mỗi lượt chỉ đọc một file JSON nhỏ và liệt kê session, chưa đo mức hạn mức tiêu.
