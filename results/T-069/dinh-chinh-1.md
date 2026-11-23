# T-069 — Đính chính 1 (theo phản biện Codex R1–R7 và tự soát N1–N5; Minh duyệt 20/11/2026)

Các file gốc giữ nguyên, đã ghim trong `SHA256SUMS` lần đầu (318 file): `phan-tich-nguyen-nhan.md`, `bang-theo-o*.{json,md}`, `phan-tich/*.txt`, `thay-doi-may.md`. Đính chính này thay các câu nêu dưới; chỗ nào hai file mâu thuẫn thì theo file này.

## 1. Kết luận W3 (R1)

Thay §1 dòng "V082 không hồi quy…" và §9 gạch đầu dòng 1 của `phan-tich-nguyen-nhan.md`, cùng câu "chuyển W4/W5 (theo SPEC, điều kiện không dừng đã đạt)" ở LOG phiên 2:

> **Một ô tụt vượt ngưỡng khai trước và tái lập: CPU-BOOK-1, V082 hạng 1 → 3 ở lần thu chính và lần lặp (P7 cùng 1 → 3). D1–D5 đều không kích hoạt** (V082 AC@1 9 → 9, AC@3 11 → 11, tổng hạng cắt 13 → 14, K 4 → 4). Kế hoạch §8.2 W3 ghi "V082 tụt thì dừng, trình Minh". **Minh quyết chấp nhận ô tụt cho demo hay giữ W3.**

Lý do sai: SPEC có hai tầng — ngưỡng tụt theo ô (dòng 58) và điều kiện dừng theo tổng D1–D5. Tôi chỉ dùng tầng thứ hai, tầng thứ nhất bị các ô tốt lên bù. Thiếu mục WHY cho quan hệ hai tầng; xem `docs/WHY.md` mục mới.

## 2. Nguyên nhân: "DB tích lũy là nguyên nhân gốc" hạ xuống ứng viên (R2, N1)

Thay §1 bảng giải thích (dòng "Code service đổi", "Trạng thái dữ liệu tích lũy") và §4–§6 phần "Kết luận theo luật 15" của `phan-tich-nguyen-nhan.md`.

**Quan sát giữ nguyên (đã kiểm):** CPU PostgreSQL ở nền tăng 4–5 lần, CPU service ứng dụng không đổi (`phan-tich/cpu-container-nen.txt`); PSI máy cao hơn ở mọi ô (`phan-tich/psi.txt`); thứ tự xếp hạng được quyết định bởi khóa thứ hai (max z) của các kênh SQL gộp; ở các kênh SQL lá, mẫu max A thường là truy vấn nền.

**Số sửa — kích thước bảng tại đúng thời điểm từng ca** (đếm `created_at < t` của ca, 20/11 ~02:20Z, chỉ đọc; giả định không xóa dòng):

| Ô | `tbl_orders` ca cũ → mới | Tỉ lệ | `tbl_issuances` |
|---|---|---|---|
| CPU-BOOK-1 lượt chính (`19b17e22` → `03573b63`) | 5.225 → 24.921 | 4,8× | 3.420 → 16.242 |
| CPU-BOOK-1 lượt lặp (→ `85255a46`) | 5.225 → 37.585 | 7,2× | 3.420 → 24.510 |
| HTTP5-EVENT (`e9c9679b` → `30ae6ac0`) | 5.873 → 36.190 | 6,2× | 3.852 → 23.610 |

"~10 lần" ở báo cáo so số cuối lượt mới với số trước đầu lượt cũ; không dùng làm số đo tại ô.

**Phản ví dụ đã xác nhận:**
- Ở CPU-BOOK-1 lượt chính, mẫu max A của Ticket (257,5 ms) là câu `SELECT count(*) … tbl_ticket_deliveries JOIN tbl_issuances`, trung vị nền 0,30 → 0,30 ms (không chậm đi). Mức 2,66 → 19,17 ms là của câu `SELECT d.id …` khác. Đuôi ở đây khớp với **tranh chấp CPU** hơn là câu chậm do bảng lớn. Ở lượt lặp, mẫu max của Ticket là câu `SELECT d.id …` (339,9 ms).
- Code đường mua vé của Booking **có đổi**: kênh chỉ có ở bản ghim gồm `INSERT tbl_orders`, `INSERT tbl_order_items`, `SELECT/UPDATE tbl_purchase_limits`, `POST /internal/v1/orders/{orderId}/purchase-snapshot`, câu `select distinct …` từ `findByIdAndBuyerSubject` `join fetch` (`phan_tich_o.py` trên `03573b63`; diff `6b21ed55..36a3725d`). Đổi này làm thay đổi hỗn hợp câu lệnh trong đơn vị op gộp dùng để chuẩn hóa.
- `EXPLAIN` đã lưu là của một câu Booking rút gọn; không là kế hoạch thực thi của mẫu Ticket.

**Kết luận sửa:** bước xếp hạng được giải thích (đã kiểm): điểm z một mẫu max chia IQR trên đơn vị op gộp cho các mẫu đuôi DB ở service không bị tiêm vượt đường tác động thật của Booking. **Nguồn sinh các mẫu đuôi là ứng viên, chưa phân xử:** (a) bảng lớn làm truy vấn nền quét tuần tự chậm và PostgreSQL tốn CPU; (b) code đường mua mới đổi hỗn hợp câu lệnh và tải DB; (c) tranh chấp CPU máy khi ép CPU Booking (cộng với (a)); (d) dao động mẫu đuôi. Lần lặp cho thấy hạng tái xuất hiện trên bản ghim; nó không tách được (a)–(c) vì image, code, thời điểm và trạng thái DB cùng đổi. Phép phân xử: cùng image `36a3725d` và cùng tải, hai trạng thái DB đã biết (ví dụ khôi phục bản dump nhỏ rồi thu lại CPU-BOOK-1 và HTTP5-EVENT); chi phí ~2 chu kỳ × 31 phút + dựng/kiểm trạng thái. Kết luận phụ thuộc: chỉ quyết định nào cần quy riêng cho DB (ví dụ chính sách khôi phục DB cho W4/W7) mới cần phép này.

## 3. Phép tính lại z từ span thô (R3)

Thay câu "z tính lại từ span thô khớp s của M1" (§1, §5 và LOG). `z_kiem.py` dùng toàn thời lượng span và chia N/A theo thời điểm bắt đầu; lõi dùng E1-U (thời gian độc quyền, bỏ span bọc, chia theo `end`; `src/m1/span.py::mau_thao_tac`). Hai cách khớp ở các kênh SQL lá đã liệt kê (span không có con). **Không khớp ở kênh có span con**: `GET /api/v1/events/{id}` của Event cho 5,0 (thô) so với 151,4 (M1) ở ca mới; Codex tính lại ca cũ: 4,0222 (thô) so với 85,17647 (E1-U, khớp đầu ra). Bảng và so sánh dùng điểm M1 trong đầu ra; `z-kiem*.txt` chỉ dùng để chỉ ra mẫu max của kênh SQL lá.

## 4. Thành phần V082 (R4) — đã chạy phép bỏ từng thành phần (bước 7.4)

Thay §3 của `phan-tich-nguyen-nhan.md` (câu "không chạy offline biến thể"). Ghi chú cũ cũng sai một chi tiết: khóa của P7 và V082 khác ở cả phần tử thứ 4 và 5 (H8s1 bỏ 12 cờ hướng ở `03573b63`).

Đã chạy (20/11 02:31–02:38Z, exp-obs, `chay_ca.py` của bản chụp `goc-12`, cấu hình khớp `manifest-3.json`) V060 (chỉ H8a), V061 (H5b + H8a = V082 bỏ H8s1), V066 (H5b + H8s1 = V082 bỏ H8a) trên `03573b63`, `85255a46`, `30ae6ac0`; ra `/srv/rca-lab/m1/t069-phan-tich/<bản>/`, chép về `phan-tich/bien-the/` (hash hai đầu khớp; mọi lần `trung_sha` true). Hạng nút đáp án (`phan-tich/bien-the/hang.txt`):

| Ô | P7 | V060 | V061 | V066 | V082 |
|---|---|---|---|---|---|
| CPU-BOOK-1 lượt chính | 3 | 3 | 3 | 3 | 3 |
| CPU-BOOK-1 lượt lặp | 3 | 3 | 3 | 3 | 3 |
| HTTP5-EVENT | 2 | 2 | 2 | 2 | 2 |

Khóa quyết định (max z của ba thực thể đầu) giống nhau ở cả năm bản. **Không thành phần nào của V082 (H5b, H8s1, H8a) gây hoặc sửa được đổi hạng ở các ô này**; đổi hạng thuộc lõi chung. Không có cấu hình "V082 bỏ H5b" (H8s1 + H8a) trong bản chụp; V060 và V066 bao phủ vai trò của H5b gián tiếp (giữ/bỏ H5b cùng kết quả).

## 5. Độ phủ (R5)

Thay §1 dòng "Log/trace/metric … Không đổi" và câu "Độ phủ tín hiệu gần như không đổi". Đếm đủ 17 cặp (`phan-tich/do-phu-17.txt`; bản 15 cặp `do-phu.txt` thiếu POOL-EVENT, RECREATE-PAY do danh sách ca nhập tay lúc chạy):
- Không đổi ở 17/17: số cạnh quan sát (18), số kênh metric (77), không nguồn coverage nào khác OK.
- Đổi: số kênh chấm hợp lệ đổi ở 14/17 cặp (đa số ±1; HTTP5-EVENT 164 → 198); span mồ côi tăng ở 16/17, giảm ở 1/17 (ví dụ HTTP5-EVENT 0 → 154, PAUSE-PAYMENT 11 → 182, POOL-EVENT 22 → 86; BINH-THUONG thứ 4 70 → 1); số span đổi −9,6% đến +2,9% (15/17 giảm; Ticket ít span và log hơn). Đếm từ `#/diagnostics` của đầu ra V082 cũ và mới.
- Chưa kiểm các kênh đổi trạng thái có trùng kênh quyết định hạng không. Vì vậy **không dùng độ phủ để loại hay nhận một giải thích**; chỉ nói đúng từng đại lượng như trên.

## 6. Phạm vi ghi thực tế (R6)

Ngoài "Phạm vi ghi" của SPEC, lượt thu đã ghi (do runner và bộ tiêm đặt sẵn; người làm thấy ở Bước 0 điểm 0.9 nhưng tự xếp KHÔNG CHẶN và **không xin Minh** — vi phạm quy trình):
- máy tải `/srv/rca-lab/load-runs/t3-<mã>` (3 + 17 + 4 chu kỳ; SPEC ghi `t069-*`), ngoài ra `t069-kiem-ban-001`;
- exp-obs `/srv/rca-lab/m1/export-audit/export-audit-<mã>.json` (file mới);
- exp-app `/tmp/ctl-<uuid>.json` tạm thời của `inj3.py::write_lease` (xóa ngay sau khi cài), dù prompt triển khai dặn không ghi `/tmp`.
Dữ liệu giữ nguyên. Minh duyệt đính chính (20/11); ghi `docs/DECISIONS.md`.

## 7. D4 (R7)

`bang_theo_o.py` (bản 1, giữ nguyên) loại ca thiếu đầu ra V082 khỏi tập ghép trước khi xét D4 và đặt D4 = `bool(loi_v082)` trước khi phân loại. Bản 2 `bang_theo_o_2.py` xét mọi ca đã thu, ghi trạng thái và phân loại (`PHAN_LOAI_D4`), D4 = có ca lỗi không phải hạ tầng. Chạy lại: `bang-theo-o-2.{json,md}`, `cham/cham-moi-A-2.{json,txt}`, `tap-moi-2.json`, `cham/spec-moi-2.json`; `#/hang` và tổng trùng bản 1; D4 = false (17/17 V082 có đầu ra OK).

## 8. Sự cố trong lúc sửa (ghi để kiểm)

Lần tạo `bang_theo_o_2.py` đầu tiên dừng ở phép `assert` khi thay chuỗi, file chưa được sửa (vẫn là bản chép của bản 1); lệnh kế tiếp đã chạy bản chép đó và ghi đè `bang-theo-o.{json,md}`, `tap-moi.json`, `cham/{spec-moi.json, cham-moi-A.json, cham-moi-A.txt}`. Kiểm ngay theo `SHA256SUMS`: 6/6 OK (trùng byte, vì cùng đầu vào). Sau đó tạo lại bản 2 đúng và kiểm không còn tên file đầu ra của bản 1 trước khi chạy.
