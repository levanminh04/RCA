# Brief L12 cho Codex — T-065 S2, S4, U2 và chốt nghiệm thu (15/11/2026 06:15Z)

Bạn là Codex (`gpt-6.1-sol`), **người làm** T-065 trong repo `D:\RCA-flashticket`; Claude là người phản biện. Phiên điều phối giao việc.

## Quyết định
Minh trả lời M4 (chat 15/11/2026 ~06:09Z; ghi ở `docs/DECISIONS.md` mục 15/11 "M4 chiến dịch M1-FlashTicket: trả lời 9 câu hỏi"): "Tôi đồng ý các đề xuất 1–8. T-065 nghiệm thu sau khi lưu ảnh S1 và bổ sung ảnh U1." Với T-065 (mục 6): S2 thêm câu "V082 vẫn dùng quan hệ E1/E2/E5 bên trong"; S3 giữ OPEN; S4 áp đính chính đã nhận vào báo cáo; R4 xác nhận hồi tố việc xóa folder Grafana `RCA` rỗng. Ảnh U1 đã được điều phối lưu ở `results/T-065/kiem/011-u1-anh-minh/` (ảnh S1 ở `kiem/009-s1-anh-minh/`).

## Đọc trước
`AGENTS.md`; SPEC và mục cuối LOG T-065; gói S2/S4 trong mục L9 của LOG T-065 (khoảng dòng 1738–1810, gồm "Description panel 5 S2 dự kiến" và khối S4); `tasks/T-065-giao-dien-grafana/REVIEW-5.md` (U2); `results/T-065/kiem/010-chi-muc-3/BAO-CAO.md`; `kiem/011-u1-anh-minh/GHI-CHU.md`.

## Việc
1. **S2:** thêm câu giải thích vào `description` của panel nêu ở gói L9 trong dashboard hiện hành `t065-l8b-rca` (và trang phát lại nếu cùng panel), nội dung: V082 không có đầu ra cạnh nhưng vẫn dùng quan hệ E1/E2/E5 bên trong lõi P7 (`results/T-064/ho-so-chon.md` §15). Hash dự kiến trong gói L9 đã cũ vì L11b đổi dashboard: GET hash live trước = pin hiện hành của L11b; ghi hash trước/sau, lưu byte cũ, cách hoàn tác. Không đổi target/truy vấn.
2. **S4:** nối đúng khối S4 của gói L9 vào `results/T-065/kiem/003-trinh-duyet/BAO-CAO.md` và `results/T-065/BAN-GIAO-L5.md` (chỉ nối, giữ câu cũ).
3. **U2:** trong `kiem/010-chi-muc-3/BAO-CAO.md` câu "đính chính L11b của Minh" sai nguồn — brief L11b do điều phối soạn. Sửa bằng một dòng đính chính nối cuối (không xóa câu cũ).
4. **R4, S3:** ghi vào báo cáo/`XONG.md`: R4 Minh xác nhận hồi tố; S3 giữ OPEN.
5. Ghim `kiem/011-u1-anh-minh/` vào manifest (giữ bản trước); cập nhật `XONG.md` (trạng thái: G-a, G-b, G-c đạt; OPEN còn lại), `CHECKPOINT.md`; nối mục L12 vào LOG T-065 kèm mục kết thúc task theo AGENTS §7 (đủ để agent khác tiếp nhận). Không ghi STATE (điều phối ghi).

## Phạm vi ghi
`results/T-065/`; nối LOG T-065; trên exp-obs chỉ file dashboard hiện hành cần cho S2 trong `/opt/flash-ticket-obs/pinned/provisioning/dashboards/`. Không sửa `results/T-064/`, SPEC, STATE, docs, REVIEW. Thấy cần làm khác: dừng, ghi checkpoint, trình lại.

## Dừng / báo xong
Có `D:/RCA-overnight/STOP` hoặc `~/rca-dieu-phoi/STOP`: dừng ở ranh giới. Báo bốn mục: đã làm gì; file đổi; kiểm đã chạy và kết quả; điều chưa chắc.
