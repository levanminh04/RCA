# Brief L10 cho Codex — T-065 sửa S1 (REVIEW-3) theo gói L9 đã được duyệt (15/11/2026 ~02:15Z)

Bạn là Codex (`gpt-6.1-sol`), **người làm** T-065 trong repo `D:\RCA-flashticket`; Claude là người phản biện. Phiên điều phối chiến dịch giao việc.

## Quyết định
Minh duyệt (chat 15/11/2026 ~02:10Z, nguyên văn "Duyệt cả ba"; ghi ở `docs/DECISIONS.md` mục 15/11 "Sửa R9, R10 (T-064, REVIEW-4) và S1 (T-065, REVIEW-3)"). Với T-065 chỉ **S1** được duyệt; S2, S3, S4 **chưa** duyệt — không làm.

## Đọc trước
`AGENTS.md`; `tasks/T-065-giao-dien-grafana/SPEC.md`; `tasks/T-065-giao-dien-grafana/REVIEW-3.md` (S1 và bảng phản hồi); mục L9 trong `tasks/T-065-giao-dien-grafana/LOG.md` (gói sửa S1: bảng file/thao tác/hoàn tác, bảng hash dự kiến, nội dung panel mục lục dự kiến, khoảng dòng 1738–1790); `results/T-065/CHECKPOINT.md` mục cuối.

## Việc (đúng gói L9, không rộng hơn)
1. Tạo nguồn phát hành mới `results/T-065/grafana-l10/t065-l5-muc-luc.json` từ mục lục L5: chỉ thay `panels[0].options.content` (hai UID L8b `t065-l8b-rca`, `t065-l8b-phat-lai`; 28 ca × 3 bản; V082 đề xuất cuối Minh chọn, V071 thay thế; `t065-l4-*` là lưu trữ); giữ UID và mọi trường khác. Giữ file L5 cũ.
2. Trên exp-obs: GET hash live của file mục lục và hai file L4 trước khi ghi; phải bằng pin trước trong gói L9, khác thì dừng và ghi checkpoint. Thay đúng file mục lục; chuyển đúng `t065-l4-rca.json` và `t065-l4-phat-lai.json` sang `RCA FlashTicket/9 · Lưu trữ/L4 · Bộ bản tạm · 14-11/` (kiểm không có file đích; không ghi đè; giữ nguyên byte/UID).
3. Kiểm: hash sau đúng bảng dự kiến; API folders/search cho thấy mục lục mới, hai L4 ở folder Lưu trữ, hai L8b ở folder hiện hành; liên kết từ mục lục tới hai UID L8b. Một ảnh Mục lục: nếu lượt CLI không chụp được bằng trình duyệt, dùng API render của Grafana nếu có; không được thì ghi rõ phần ảnh chưa làm để Minh chạy app.
4. Ghi hash trước/sau và lệnh hoàn tác vào `results/T-065/` (thư mục `kiem/008-s1/`), cập nhật `XONG.md`, `CHECKPOINT.md`, manifest (giữ bản trước), nối mục L10 vào LOG T-065, điền một dòng "S1 (sửa)" vào bảng phản hồi cuối `REVIEW-3.md` (để trống "Minh quyết"), kèm prompt cho Claude kiểm lại (nguyên văn mẫu `docs/review-prompt.md`, khối "Kiểm lại phản hồi và sửa", thông tin trung tính).

## Phạm vi ghi
`results/T-065/`; nối LOG T-065; một dòng bảng phản hồi REVIEW-3; trên exp-obs chỉ file mục lục và hai file L4 nêu trên trong `/opt/flash-ticket-obs/pinned/provisioning/dashboards/`, và khởi động lại/tải lại provisioning Grafana nếu cần. Không sửa `results/T-064/`, SPEC, STATE, docs. Thấy cần làm khác gói L9: dừng, ghi checkpoint và trình lại.

## Dừng
Có `D:/RCA-overnight/STOP` hoặc `~/rca-dieu-phoi/STOP`: dừng ở ranh giới.

## Báo xong
Bốn mục: đã làm gì; file đổi; kiểm đã chạy và kết quả; điều chưa chắc.
