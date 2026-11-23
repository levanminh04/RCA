# T-069 — Phân tích nguyên nhân các ô đổi hạng (bước 7)

Ghi 19/11/2026 ~18:55Z, sau lượt chính `t069-chinh`; lượt lặp `t069-lap` đang chạy (mục 7 bổ sung sau). Mọi số có đường dẫn.
Quan sát, suy luận, kết luận và phần chưa biết tách riêng (luật 14, 15, 17).

## 1. Tóm tắt

- **Kết quả theo tiêu chí khai trước:** 17/17 ô ghép được. V082 cũ → mới AC@1 9 → 9, AC@3 11 → 11, tổng hạng cắt 13 → 14, K 4 → 4. P7: 7 → 7, 9 → 9, 23 → 24, K 5 → 6. **D1–D5 đều không xảy ra.** Một ô tụt: CPU-BOOK-1, hạng 1 → 3 (`bang-theo-o-chinh.json#/dieu_kien_dung`, `#/hang`).
- **Câu hỏi của Minh: tụt do code, do tải hay do log/trace/metric thay đổi?**

| Giải thích | Kết luận | Bằng chứng chính |
|---|---|---|
| Thành phần riêng của V082 (H5b, H8s1, H8a) | **Loại** | P7 cho cùng ba thực thể đầu, cùng khóa, ở cả CPU-BOOK-1 và HTTP5-EVENT (mục 3) |
| Code service đổi | **Không là nguyên nhân trực tiếp** | Câu truy vấn nền giữ nguyên giữa `6b21ed55` và `36a3725d`; CPU nền của mọi service ứng dụng không đổi (mục 4) |
| Hồ sơ tải (kịch bản, nhịp, hành trình) | **Không đổi** | Cùng kịch bản và nhịp; số đơn tạo, số thanh toán, số hành trình hỏng ở ô lỗi ≈ ca cũ (mục 4) |
| Log/trace/metric (loại tín hiệu, độ phủ) | **Không đổi** | Kênh hợp lệ 328 → 329, cạnh 18 = 18, metric 77 = 77, không nguồn nào hỏng (`phan-tich/do-phu.txt`) |
| **Trạng thái dữ liệu tích lũy (DB lớn ~10 lần)** | **Nguyên nhân gốc đã lần được** | Truy vấn nền quét tuần tự chậm 7–9 lần; CPU PostgreSQL ở nền tăng 4–5 lần; mẫu lớn nhất quyết định điểm ở kênh dẫn đầu là chính các truy vấn nền này (mục 4–6) |
| Đặc tính chấm của lõi P7 (E4 `diem_z`: một mẫu max chia IQR, trên đơn vị op gộp mọi câu lệnh) | **Điều kiện khuếch đại** (có từ trước, dùng chung P7 và V082) | Công thức `src/m1/e4.py::_diem_z_native`; z tính lại từ span thô khớp s của M1 (`phan-tich/z-kiem.txt`) |
| Nhiễu một lần thu | **Chưa phân xử** — lượt lặp đang chạy | Hạng đúng của ca cũ CPU-BOOK-1 cũng chỉ nhờ một mẫu đuôi 262,6 ms (mục 5) |

Vậy, "tụt" ở bản ghim **không do V082 và không do code đổi**. Nó do hệ thống thử nghiệm đã "già" về dữ liệu: các bảng đơn và vé lớn gấp ~10 lần so với lúc thu ca cũ, và cách chấm theo một mẫu đuôi của lõi khiến các truy vấn nền chậm che tín hiệu thật.

## 2. Số theo ô

`bang-theo-o-chinh.md` (bản lượt chính; `bang-theo-o.md` sẽ có thêm cột lần lặp). Đổi hạng V082: CPU-BOOK-1 1 → 3, HTTP5-EVENT 1 → 2, CPU-BOOK-2 2 → 1, HTTP5-EVENT-FLASH 2 → 1. Ô không lỗi: BINH-THUONG thứ 3 0 → 1, BINH-THUONG-X3 1 → 0. P7 đổi cùng chiều ở mọi ô V082 đổi hạng (CPU-BOOK-1 1 → 3, HTTP5-EVENT 1 → 2, HTTP5-EVENT-FLASH 2 → 1), riêng CPU-BOOK-2 P7 giữ hạng 1.

## 3. Loại giải thích "thành phần V082"

Ba thực thể đầu và khóa xếp hạng của chúng ở ca mới (`dau-ra/dev3/d0/{P7,V082-V066+H8a}/<mã>/method-output-1.json#/entity_ranking`):
- CPU-BOOK-1 `03573b63`: cả hai bản xếp `ticket-service` [2; 945,79], `keycloak` [2; 696,21], `booking-service` [2; 449,66]. Hai bản chỉ khác số kênh có cờ ở vị trí khóa thứ 4 (H8s1 bỏ vài kênh dưới 1 ms).
- HTTP5-EVENT `30ae6ac0`: cả hai bản xếp `booking-service` 1, `event-service` 2.

P7 là "V082 bỏ cả ba thành phần". Bỏ cả ba vẫn cho đúng thứ tự đó, nên không thành phần nào gây đổi hạng. Vì vậy **không chạy offline biến thể** (SPEC bước 7.4); P7 đã trả lời câu hỏi "bỏ thành phần nào thì hết tụt" (không thành phần nào).

## 4. Trạng thái dữ liệu: bảng lớn, truy vấn nền quét tuần tự, PostgreSQL tốn CPU

**Quan sát:**
- Số dòng (`phan-tich/kiem-db.txt`, 19/11 18:31Z; số "trước mốc" theo `created_at`, giả định không xóa dòng):

| Bảng | Hiện nay | Tạo trước 13/11 07:14Z (thu2) | Trước 14/11 07:24Z (thu bù 3) |
|---|---|---|---|
| `booking_schema.tbl_orders` | 37.477 | 3.713 | 15.133 |
| `ticket_schema.tbl_ticket_deliveries` / `tbl_issuances` | 24.438 | 2.412 | 9.875 |

- Truy vấn của worker hết hạn đơn: `EXPLAIN` cho `Seq Scan on tbl_orders`. `pg_stat_user_tables`: `tbl_issuances` 7.141.875 lượt quét tuần tự, 92.992.449.315 dòng đọc; `tbl_ticket_deliveries` 7.330.618 lượt, 93.031.378.432 dòng.
- Thời lượng truy vấn nền ở nền N, cùng câu lệnh (`phan-tich/span-http5-*.txt`, `span-cpu1-cu-moi.txt`):

| Truy vấn nền | Cũ p50 | Mới p50 |
|---|---|---|
| Booking: `tbl_orders where lifecycle_state=? and expires_at<=?` | 3,93 ms | 34,77 ms |
| Booking: `tbl_orders join tbl_reservations …` | 6,33 / 5,69 ms | 42,60 / 24,60 ms |
| Ticket: `tbl_ticket_deliveries join tbl_issuances …` | 2,66 ms | 19,17 ms |

- Câu lệnh không đổi: `OrderRepository` (dòng 48) giống nhau giữa `6b21ed55` và `36a3725d`; Booking không có migration mới; Ticket chỉ đổi 2 file (+6 dòng, sửa 404).
- CPU từng container ở nền N (`phan-tich/cpu-container-nen.txt`; lõi CPU trung bình): PostgreSQL 0,064–0,089 → 0,288–0,408 (thu2 → mới), 0,269 → 0,412 (thu bù 3 → mới). Booking 0,016–0,018 → 0,017–0,020; Ticket 0,098–0,137 → 0,103–0,118; các service khác không đổi.
- Áp lực CPU máy (PSI `some avg60`, đầu dò `inj3`, `phan-tich/psi.txt`): nền cũ 11,8–16,3%, mới 15,5–18,3%. Tổng thời gian chờ CPU giữa t+60 và t+330: BINH-THUONG cũ 32,7–42,5 s, mới 47,2–51,8 s; CPU-BOOK-1 79,7 → 91,5 s. CPU Booking dùng ở nền không đổi (4,2–4,7 s/270 s); lượng CPU bị đốt khi tiêm như nhau (244,0 so 238,6 s).
- Tải: mọi chu kỳ mới có `create_order` 201 (`thu/t069-chinh/tai-create-order.json`). Hành trình hỏng ở ô lỗi gần ca cũ: HTTP5-EVENT 720 = 720, HTTP5-EVENT-FLASH 2162/2161, PAUSE-PAYMENT 154/159, CONSUMER 1207/1205 (`xac-nhan/t069-chinh-thu*.json#/ca/<mã>/k6`).

**Suy luận:** dữ liệu tích lũy từ các lượt tải (T-063 → T-067 → hôm nay) làm các worker nền (hết hạn đơn của Booking, giao vé của Ticket) quét tuần tự bảng lớn gấp ~10 lần. Hệ quả: (1) mỗi truy vấn nền chậm 7–9 lần; (2) PostgreSQL tốn thêm ~0,2–0,3 lõi CPU liên tục trên máy 2 vCPU, nên máy căng CPU hơn ở mọi ô. Đây là thay đổi trạng thái, không phải thay đổi code hay kịch bản tải. Một phần đã có ở thu bù 3 (PostgreSQL 0,27 lõi).

**Chưa biết:** vì sao truy vấn hết hạn đơn không dùng `orders_expiry_idx (expires_at)`. Ứng viên: bộ lập kế hoạch chọn quét tuần tự vì điều kiện `lifecycle_state` kém chọn lọc, hoặc thống kê bảng cũ. Chưa kiểm vì cần `EXPLAIN ANALYZE` (chạy câu lệnh) hoặc đổi chỉ mục; không cần cho kết luận W3.

## 5. Cơ chế ô CPU-BOOK-1 (hạng 1 → 3, cả P7)

**Bước tính dùng:** điểm của đơn vị op là `z = (max(A) − trung vị(N)) / IQR(N)` (`src/m1/e4.py::_diem_z_native`); khóa thứ hai của thực thể là z lớn nhất trong các kênh có cờ; thực thể xếp theo khóa này trước. Đơn vị op gộp mọi câu lệnh cùng tên span (ví dụ `SELECT ticket_db` gồm cả câu nhanh 0,2 ms và câu nền 19 ms).

**Chuỗi bằng chứng** (`phan-tich/z-kiem.txt`; z tính lại từ span thô khớp s của M1):

| Kênh | Ca cũ 19b17e22: med N / IQR N / max A → z | Ca mới 03573b63: med N / IQR N / max A → z | Mẫu max A ở ca mới |
|---|---|---|---|
| Booking `SELECT tbl_ticket_type_inventory` (đường đặt vé, chịu CPU trực tiếp) | 0,240 / 0,194 / **262,6** ms → **1352,3** | 0,285 / 0,262 / 15,2 ms → 56,9 | câu kho vé |
| Booking `SELECT booking_db` | 0,318 / 0,406 / 69,4 → 170,1 | 0,392 / 0,561 / 252,4 → 449,2 | **join đơn–giữ chỗ của worker hết hạn** |
| Ticket `SELECT ticket_db` (không bị tiêm) | 0,286 / 0,355 / 71,3 → 199,8 | 0,285 / 0,272 / **257,5** → **944,8** | **đếm giao vé join phát hành** |
| Keycloak `SELECT OUTBOX_ENTRY` (không bị tiêm, image không đổi) | 0,331 / 0,049 / 10,0 → 195,1 | 0,331 / 0,115 / 80,6 → 698,3 | câu outbox |

Ở cả hai phía, p50/p90 của truy vấn kho vé Booking tăng ~2 lần khi ép CPU (cũ 0,24/0,85 → 0,48/1,75 ms; mới 0,29/0,97 → 0,47/2,22 ms; `span-cpu1-cu-moi.txt`), nên tác động thật lên Booking giống nhau.

**Kết luận theo luật 15:** trong điều kiện bảng DB lớn (truy vấn nền 19–43 ms, PostgreSQL thêm 0,2–0,3 lõi) và CPU máy bão hòa do ô ép CPU, bước chấm z của lõi (một mẫu max chia IQR của đơn vị op gộp) cho điểm rất cao các service **không bị tiêm** (Ticket 945, Keycloak 698), vì mẫu đuôi 250 ms của truy vấn nền chia cho IQR ~0,3 ms của câu nhanh. Thông tin "service nào bị tác động trực tiếp" bị đánh giá sai: đường tác động thật của Booking (truy vấn kho vé, z 57) thấp hơn. Ở ca cũ, Booking hạng 1 nhờ **một** mẫu đuôi 262,6 ms ở đúng truy vấn kho vé; các service khác không có truy vấn nền đủ chậm để tạo đuôi tương đương.

**Phần còn mở:** mẫu đuôi rơi vào kênh nào khi CPU căng có yếu tố ngẫu nhiên. Ở cả hai phía, hạng của Booking phụ thuộc một mẫu. Lượt lặp phân xử phần nhiễu một lần thu (mục 7).

## 6. Cơ chế ô HTTP5-EVENT (hạng 1 → 2, cả P7)

**Quan sát** (`phan-tich/span-http5-{cu-e9c9679b,moi-30ae6ac0}.txt`, `z-kiem.txt`):
- Hook `http.error` làm hỏng bước xem chi tiết sự kiện, nên trong A hành trình mua dừng trước khi tạo đơn. Ở cả cũ và mới, các câu lệnh nhanh theo yêu cầu của Booking gần như biến mất trong A (ví dụ `select clock_timestamp()` cũ 780 → 74, mới 822 → 89; chọn đơn theo id cũ 452 → 14, mới 294 → 30). Các truy vấn nền giữ nguyên số lần (60/60).
- Theo từng câu lệnh, Booking **không chậm đi** trong A ở cả hai phía.
- Đơn vị gộp `SELECT tbl_orders`: cũ max A 9,4 ms → z 19,8; mới max A 215,3 ms (chính truy vấn hết hạn đơn) → z 332,0. `SELECT booking_db`: cũ 15,8 ms → z 38,9; mới 184,8 ms → z 292,5.
- Event giữ cùng ba kênh bằng chứng (`GET /api/v1/events/{id}`, `metric|event-service_error`, `log|event-service|log_loi`); s tăng 85,2 → 151,4. Ở lượt thử (không mua được vé, `2d5a56fe`), Event 1734,9 và Booking 229,2 → Event hạng 1.

**Kết luận theo luật 15:** trong điều kiện ô làm giảm yêu cầu mua (HTTP5 hỏng bước detail), đơn vị op gộp của Booking chỉ còn chủ yếu các truy vấn nền. Ở bản ghim, truy vấn nền chậm 9 lần do bảng lớn, nên mẫu max A (215 ms) chia IQR của câu nhanh (0,65 ms) cho z 332 > s của Event (151). Thông tin bị đánh giá sai: sự **đổi thành phần** câu lệnh (do hành trình dừng sớm) bị chấm như Booking chậm đi. Ở bản 3, truy vấn nền chỉ 4–6 ms nên hiệu ứng này nhỏ (z 20–39 < 85).

## 7. Lượt lặp

`t069-lap` 18:39:49Z → 20:45:36Z, 4 chu kỳ, cả 4 ca xác nhận tác động, tải mua vé hoạt động (`thu/t069-lap/tai-create-order.json`). P7 và V082 chạy, V082 `trung_sha` true. Hạng V082/P7 lần thu chính → lần lặp (`bang-theo-o.json#/hang/<i>/lap`):

| Ô | Cũ | Lần thu chính | Lần lặp |
|---|---|---|---|
| CPU-BOOK-1 | 1 / 1 | 3 / 3 | **3 / 3** (`85255a46`, Ticket hạng 1) |
| HTTP5-EVENT | 1 / 1 | 2 / 2 | **2 / 2** (`8c2d139e`, Booking hạng 1) |
| CPU-BOOK-2 | 2 / 1 | 1 / 1 | 1 / 1 |
| HTTP5-EVENT-FLASH | 2 / 2 | 1 / 1 | 1 / 1 |

- Lần lặp trùng lần thu chính ở cả 4 ô, nên **đổi hạng không phải nhiễu một lần thu**. Cơ chế mục 5 lặp được: ở `85255a46`, mẫu max A của Ticket `SELECT ticket_db` là truy vấn giao vé 339,9 ms (z 1026,2); của Booking `SELECT booking_db` là join đơn–giữ chỗ của worker hết hạn 369,6 ms (z 599,8); đường tác động thật (kho vé) z 118,1 (`phan-tich/z-kiem-lap-cpu1.txt`).
- Về nhãn nhóm: `bang-theo-o.json` gắn HTTP5-EVENT "a+c" vì áp nguyên câu quy tắc khai trước (lần lặp nằm trong [cũ − 1, cũ + 1]). Ô này không tụt ngay từ lần đầu (1 → 2) và lần lặp **trùng** lần đầu, nên nhãn "c" (nghiêng nhiễu) không phản ánh dữ liệu. Diễn giải đúng: nhóm (a), không phải nhiễu. Không sửa file sinh tự động; ghi rõ ở đây và LOG (là diễn giải sau khi xem, không đổi tiêu chí).
- Ô vượt giới hạn lặp: EVENT-DB-LAT (chỉ P7 đổi 2 → 1), không lặp.

## 8. Ô không lỗi và ô tốt lên (không phải ô tụt; ghi ngắn)

- BINH-THUONG thứ 3 `a06231fd` (V082 0 → 1; P7 0 → 1): kênh `op|event-service|event_db` s 240,6, cùng `Transaction.commit`, `SELECT tbl_outbox_messages` — loại đơn vị op gộp như trên. Chưa lần mẫu max; K tổng không đổi (BINH-THUONG-X3 1 → 0).
- CPU-BOOK-2 (V082 2 → 1) và HTTP5-EVENT-FLASH (V082, P7 2 → 1): **chưa lần cơ chế**. Không dùng làm bằng chứng V082 tốt hơn; với cùng đặc tính chấm theo một mẫu, đổi hạng theo chiều tốt cũng có thể là may.

## 9. Hệ quả và giới hạn

- Kết luận W3 theo tiêu chí khai trước: V082 không hồi quy quá ngưỡng trên bản ghim; ô tụt và ô đổi hạng do trạng thái dữ liệu cộng với đặc tính chấm có sẵn của lõi, đổi cùng chiều ở P7. Đây là kiểm không hồi quy trên ô dev, mỗi ô một lần thu (+ lặp 4 ô), không phải ước lượng độ chính xác.
- Hệ thống thử nghiệm **trôi theo thời gian** vì dữ liệu tích lũy: cùng image và kịch bản nhưng PostgreSQL tốn CPU gấp 4–5 lần sau ~6 ngày tải. Mọi so sánh giữa hai thời điểm (W3, W4 đêm nền, W6–W7) phải kiểm soát trạng thái DB.
- Đặc tính "một mẫu max chia IQR trên đơn vị op gộp" của lõi P7 là điểm yếu chung (không riêng bản ghim). Bản ghim chỉ làm nó lộ rõ hơn. Không sửa trong T-069 (SPEC cấm sửa V082/M1).
- Giới hạn của phân tích: số dòng "trước mốc" giả định không xóa dòng; z tính lại dùng gộp span theo tên và không áp lọc span con vượt biên của E1 (khớp số cho thấy ảnh hưởng không đáng kể ở các kênh đã kiểm); chưa kiểm vì sao bộ lập kế hoạch quét tuần tự.
