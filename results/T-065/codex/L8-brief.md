# Brief L8 cho Codex — T-065 G-c: kiểm cuối trên bản M1-FT đề xuất cuối V082 (14/11/2026 16:33Z)

Bạn là Codex (`gpt-6.1-sol`), **người làm** T-065 trong repo `D:\RCA-flashticket`. Phiên Claude điều phối chiến dịch M1-FlashTicket giao việc; Claude là **người phản biện**. Quyền: `docs/DECISIONS.md` mục "Bổ sung quyền điều phối chiến dịch nhiều ngày"; SPEC T-065 phần bổ sung cuối file ("G-c tích hợp thử từ đầu ra phù hợp đầu tiên … rồi kiểm lại trên bản M1-FT đề xuất cuối").

## Đọc trước (bắt buộc)
1. `AGENTS.md`.
2. `tasks/T-065-giao-dien-grafana/SPEC.md` toàn bộ gồm phần bổ sung; `tasks/T-065-giao-dien-grafana/LOG.md` các mục L4 (G-c thử) và L7 (mục cuối).
3. `results/T-065/XONG.md`, `CHECKPOINT.md` (mục cuối), `manifest.json`, `thay-doi-may.md`; brief L4 `results/T-065/codex/L4-brief.md` (G-c thử trên bản tạm).
4. `results/T-064/hop-dong-dau-ra.md` và **chỉ mục bản cuối** `results/T-064/ban-xuat/chi-muc-ban.json` (`phien_ban_chi_muc: 2`; SHA-256 file = `7e893ec237ce55c04bdea13d8981670e9e8f3e19e848959e1067d6d6bac9b6e6`). Bản tạm L4–L7 đã dùng giữ ở `results/T-064/ban-xuat/chi-muc-ban-tam-1.json`.
5. Quyết định bản cuối: `docs/DECISIONS.md` mục 14/11 "Bản đề xuất cuối M1-FlashTicket (T-064): V082"; `docs/WHY.md` WHY-98; `results/T-064/cau-hinh-de-xuat.json`.

## Dữ kiện về chỉ mục bản 2 (kiểm lại, không tin brief)
- Ba bản: `p7` (`khoa_P7`), `V082-V066+H8a` (`de_xuat`; không có đầu ra cạnh), `V071-V041+H8a` (`thay_the`; có `extra.m1_ft.canh_xep_hang`).
- Mỗi bản 28 ca: 13 ca dev bản 2, 6 ca dev bản 3 (thu bù 3 của T-063: `86dea661`, `659a9dfb1ab0`, `1e5a3dc5`, `ebd5ef38`, `7d1ee32f`, `0a45b2e0`), 9 ca T-062. Ca P7 `ebd5ef38` là lỗi chạy: `dau_ra = null`, có `loi_chay`.
- Kiểm SHA từng `dau_ra` trước khi dùng; lệch thì dừng phần phụ thuộc và ghi checkpoint.

## Việc
- **G-c kiểm cuối:** đưa chỉ mục bản 2 vào bộ xuất dữ liệu và dashboard (chiều **bản**: chọn `p7` / `V082-V066+H8a` / `V071-V041+H8a` cho cùng ca). Trang ca hiện mã bản, `trang_thai`, `cau_hinh_sha256`, `ma_nguon_sha256`, cửa sổ `[t−300, t+300)`; cờ và hạng đúng theo `method-output-1.json` của bản đó. V082: hiện đúng "không có đầu ra cạnh", không suy ra. Ca lỗi chạy: hiện trạng thái lỗi chạy và đường dẫn `loi_chay`, không dựng hạng. Không tự xếp lại, không chấm điểm, không hiện đáp án trên trang chính.
- **Ca dev bản 3:** dựng liên kết bằng chứng khi nguồn trace/metric/log của ca có trên `exp-obs` (`/opt/flash-ticket-rca/cases|outputs/<mã>`, `/opt/rca-m1ft/bo-sung-dev3/<mã>`; cách gọi máy ở `results/T-063/thu3/CHECKPOINT.md`, không in khóa). Thiếu nguồn thì giữ mức bảng xếp hạng và ghi giới hạn; không dựng bằng chứng giả.
- **Giữ bản cũ:** dashboard và dữ liệu xuất của G-c thử (bản tạm) giữ nguyên làm lịch sử; thêm bản mới.
- **Kiểm:** mỗi bản ít nhất 3 ca (gồm `ebd5ef38`, một ca có cạnh của V071, một ca T-062) đối chiếu số hiển thị với `method-output-1.json` (hạng, cờ, hash). Kiểm qua API/dữ liệu xuất; nếu cần ảnh/bấm thật trên Chrome mà lượt CLI không làm được, ghi rõ phần chưa kiểm để Minh chạy lượt app.

## Phạm vi ghi
Theo SPEC T-065 "Phạm vi ghi": `results/T-065/`; trên `exp-obs` chỉ file dashboard **mới** trong `/opt/flash-ticket-obs/pinned/provisioning/dashboards/`, thư mục con mới trong `/opt/flash-ticket-obs/rca-ket-qua/`, khởi động lại container Grafana. Nối mục L8 vào `tasks/T-065-giao-dien-grafana/LOG.md`. Không sửa `results/T-064/`, REVIEW, SPEC, STATE, docs.

## Checkpoint, hạn mức, dừng
`results/T-065/CHECKPOINT.md` sau mỗi bước con. Hết hạn mức: bộ gọi sẽ `resume`. Có `D:/RCA-overnight/STOP`: dừng ở ranh giới. Lượt dài hơn 1 giờ: ghi trước "lỗi ở 10%/50%/99% xử lý thế nào" (luật 21).

## Báo xong
Cập nhật `XONG.md` (G-c đạt/một phần, chặn, bước tiếp), `manifest.json` (giữ bản trước), và prompt cho Claude kiểm lại (nguyên văn mẫu `docs/review-prompt.md`, khối "Kiểm lại phản hồi và sửa", thông tin trung tính; gộp phần L6, L7 đang chờ kiểm và L8). Tóm tắt cuối lượt: đã làm gì; file đổi; kiểm đã chạy và kết quả; điều chưa chắc.
