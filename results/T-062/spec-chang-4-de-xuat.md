# Đề xuất SPEC chặng 4 — Đợt phát triển M1 trên FlashTicket (chờ Minh duyệt)

- **Trạng thái:** ĐỀ XUẤT, chưa duyệt. Claude soạn trong lượt T-062 (12/11/2026). Chưa tạo task, chưa chạy gì theo file này.
- **Bản 3 (12/11/2026):** sửa R6, R7 của `REVIEW-2.md` (Minh duyệt): định nghĩa K' tính lỗi chạy là không đạt; thêm ca khỏe giữ lại; ba bảng chấm T-059 cho cạnh. Bản 2 ở `_ban-2/`.
- **Bản 2 (12/11/2026):** sửa theo R1, R3, R4, R5 của `tasks/T-062-dem-chang-1-4/REVIEW.md` (Minh duyệt sửa). Bản 1 ở `results/T-062/_ban-1/spec-chang-4-de-xuat.md`.
- **Thuộc:** `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §3 chặng 4: *"Chạy M1 và baseline trên dữ liệu phát triển. Thử cho M1 dùng thông tin giàu hơn … Mỗi thay đổi là một thành phần có đối chứng bỏ nó; tiêu chí chọn khai trước"*. Phép so chuyển giao D14 (`results/T-043/bang-chuyen-giao.json#/phep_so_FT_D14`).
- **Đầu vào đã có từ T-062:** lượt phát triển đầu với **M1 bản khóa P7** (không chỉnh) trên 5 ô lỗi phát triển và 4 ca không tiêm lỗi. Kết quả và giới hạn: `results/T-062/bao-cao-sang.md` (bản 2).

## 1. Câu hỏi chặng 4 phải trả lời

1. Trên dữ liệu FlashTicket phát triển, bản khóa P7 xếp thành phần gốc ở đâu, theo từng ô và họ lỗi?
2. So với P7 và các baseline chạy trên **cùng gói dữ liệu**, bản FlashTicket có xếp đúng hơn không, và nhờ nhóm thông tin nào (phép so D14 (1)(2)(3))?
3. Mỗi thành phần đề xuất (mục 3) cải thiện **chất lượng xếp hạng** hay **khả năng không kết luận có nguyên nhân khi không có lỗi**, mà không làm xấu đại lượng kia?
4. Chọn một phiên bản M1 cho FlashTicket để khóa ở chặng 5, theo tiêu chí khai **trước** khi xem kết quả biến thể.

Không trả lời ở chặng 4: hiệu quả trên tập đánh giá (chặng 6), RQ5, lợi ích đồ thị trên dữ liệu khóa.

## 1b. Điều T-062 cho thấy (n = 1, chỉ định hướng)

- 5/5 ô lỗi có thành phần thuộc tập chấp nhận ở hạng 1. Với ô cạnh (NET-GW-BOOK) M1 lưu cờ trên cạnh `api-gateway→booking-service` nhưng đầu ra xếp hạng là nút (Booking) — định vị qua tập chấp nhận, chưa phải tìm đúng cạnh gốc.
- 4/4 ca **không tiêm lỗi mới** vẫn có `CAUSE_FOUND`. Đây **không** phải tỷ lệ báo động giả trên ca khỏe: 3 ca bình thường có lỗi nền (tickets 500 cố định), FLASH có 244 phản hồi 429 và chưa có ngưỡng khỏe (T-059). Chế độ a không buộc `CAUSE_FOUND` (`src/m1/xep_hang.py::verdict`).
- Hệ quả cho thiết kế chặng 4: cần đo cả xếp hạng ở ca lỗi lẫn kết luận ở ca **khỏe đã xác nhận**; muốn có ca khỏe phải khóa ngưỡng sức khỏe trước (điều kiện vào).

## 2. Dữ liệu

Bảy ô phát triển T-059 = **6 ô lỗi + FLASH-HEALTHY** (`results/T-059/danh-muc-loi.json#/cells`). REDIS-BOOK chưa xác nhận được can thiệp (D2) — bảng dưới tính hai trường hợp.

| Tập | Nội dung | Số ca | Dùng để |
|---|---|---|---|
| Ca lỗi dev | 6 ô lỗi × 3 lặp (T-062 có 1 lặp/ô cho 5 ô) | **18** (15 nếu bỏ REDIS-BOOK) | Chọn |
| Ca khỏe dev | Ca bình thường **đạt ngưỡng sức khỏe khai trước** (không còn lỗi nền nếu sửa tickets; hoặc lỗi nền được khai là một phần "khỏe") | ≥ 6 | Chọn (đại lượng kết luận ở ca khỏe) |
| FLASH-HEALTHY | 2 lặp; ca đạt ngưỡng khỏe vào nhóm khỏe, ca bị giới hạn Gateway (429) hoặc suy giảm báo nhóm riêng (T-059 §phân loại) | 2 | Báo cáo; chỉ vào tiêu chí khi đạt ngưỡng |
| Held-out dev | 1 lặp mới mỗi ô lỗi + **2 ca khỏe mới**, chạy **sau** khi khai tiêu chí | 8 (7) | Kiểm không quá khớp cả X và K' |
| Đánh giá | Ô "đợt đánh giá" T-059 | — | **Không dùng** (luật cứng 1) |

Chi phí máy (ước lượng, chưa gồm baseline): lỗi dev thêm 2 lặp × 6 ô = 12 (10) chu kỳ; khỏe ≥ 6; FLASH 2; held-out 8 (7) → khoảng **28 (25) chu kỳ × 30 phút ≈ 14 (12,5) giờ**. Baseline chạy trên gói đã đóng băng, không cần thêm chu kỳ tải (mục 3b).

## 3. Thành phần ứng viên (mỗi cái một đối chứng bỏ nó)

| Mã | Thay đổi | Lý do (nguồn) | Ô dev phân xử | Đối chứng |
|---|---|---|---|---|
| C4-a | DB, cache, broker thành nút từ thuộc tính span; cờ cạnh được xếp hạng cùng nút | T-058 KP; ô cạnh EVENT-DB-LAT, NET-GW-BOOK (REDIS-BOOK nếu xác nhận được) | EVENT-DB-LAT, NET-GW-BOOK | P7 không có C4-a |
| C4-b | Kênh JVM/cgroup (CPU throttling, GC, heap) | ô CPU-BOOK; KP-04/18 | CPU-BOOK | bỏ C4-b |
| C4-c | Kênh pool kết nối (Hikari) | ô POOL-BOOK là ô **đánh giá** | **không có ô dev** | OPEN — không chọn ở chặng 4 nếu không có ô dev; nêu ô dev cần thêm (POOL-EVENT ứng viên) để Minh quyết |
| C4-d | Kênh queue (RabbitMQ ready/unacked) | TICKET-PAUSE là ô **đánh giá**; tải hiện chỉ đọc, không có message | **không có ô dev** | OPEN — cần tải có giao dịch (chặng 2) và một ô dev queue |
| C4-e | Giữ thành phần "chết im" | KP-10 | **không có ô dev** (pause là ô đánh giá) | OPEN |

C4-c/d/e không được chọn bằng ô đánh giá. Nếu Minh muốn chọn chúng ở chặng 4, cần thêm ô dev tương ứng vào T-059 (quyết định riêng).

## 3b. Ma trận so sánh (D14 và baseline) — sửa R4

Tất cả chạy trên **cùng gói ca đã đóng băng** (t, cửa sổ, tập ứng viên giống nhau), chấm bằng cùng bảng chấm.

| # | Bản | Vai trò | Dùng để chọn? |
|---|---|---|---|
| D14-(1) | P7 khóa chạy thẳng trên thông tin chung | đối chứng chuyển thẳng | không (mốc) |
| D14-(2) | Bản FlashTicket đã chọn (P7 + thành phần giữ) | đối tượng | là kết quả chọn |
| D14-(3) | Bản (2) che từng nhóm thông tin phong phú (đầu vào và dẫn xuất) | đo đóng góp từng nhóm | không — báo cáo; chính là đối chứng bỏ thành phần ở mục 3 |
| D14-(4) | (tùy chọn) gói thông tin chung tối ưu riêng | gọi đúng tên | không |
| B-x | Baseline đã cài (`src/p3/adapters/`: BARO, CIRCA, MicroRank, TraceRCA, Nezha, SimpleRCA, TORAI) — chạy được trên dữ liệu FlashTicket nào thì chạy | đặt kết quả M1 vào bối cảnh | **không** — chỉ báo cáo |

Cần Minh chọn: baseline nào bắt buộc ở chặng 4 (đề xuất: BARO (metric), MicroRank hoặc TraceRCA (trace), Nezha (đa nguồn) — mỗi họ một phương pháp; chi phí là viết adapter FlashTicket cho định dạng gói ca, chưa ước lượng). Nếu tách baseline sang gói sau: đầu ra chặng 4 chỉ là "chọn bản FlashTicket so với P7", **chưa** được kết luận M1 tốt hơn baseline trên FlashTicket.

## 4. Tiêu chí chọn (khai trước, Minh duyệt trước khi chạy biến thể) — sửa R3

Đơn vị: ca. Hai đại lượng:

- **X (xếp hạng):** AC@1 và AC@3 của **hạng tốt nhất trong tập chấp nhận T-059** trên ca lỗi dev (`bang-cham.json#/ca/*/hang_tot_nhat`). ERROR/UNSUPPORTED tính là trượt.
- **K' (kết luận ở ca khỏe, bản 3):** số ca khỏe đã xác nhận **không** trả `NO_INTRINSIC_ANOMALY` (càng ít càng tốt). `CAUSE_FOUND`, `INSUFFICIENT_EVIDENCE`, ERROR, UNSUPPORTED đều tính là **không đạt** — một bản lỗi chạy không được tính là cải thiện.
- **X-cạnh (bản 3, theo T-059 `label_rules/2`):** với ô có root là cạnh, chấm riêng ba phần: (i) khớp root thật (đúng cạnh có hướng và loại); (ii) định vị qua tập nút chấp nhận — **X-nút**: danh sách hỗn hợp cạnh–nút được chiếu về thực thể, mỗi cạnh hạng k cho hai đầu nhận hạng k nếu chưa có hạng tốt hơn; (iii) định vị cạnh: hạng của đúng cạnh root trong danh sách cạnh. Bản không có đầu ra cạnh (P7) ghi UNSUPPORTED ở (i) và (iii).

Một thành phần được giữ khi so với bản bỏ nó, trên cùng ca, đạt **một trong hai hướng**:

1. X tốt hơn (AC@3 của X-nút tăng ≥ 1 ca trên 18/15 ca lỗi) **và** K' không tăng; hoặc
2. K' giảm (≥ 1 ca) **và** AC@3 không giảm, AC@1 không giảm quá 1 ca; hoặc
3. (riêng C4-a) X-nút không giảm **và** X-cạnh (iii) từ UNSUPPORTED thành có hạng ≤ 3 trên ít nhất một nửa số ca của ô cạnh (EVENT-DB-LAT, NET-GW-BOOK; REDIS-BOOK nếu xác nhận).

Và: không ô nào mất quá 2 bậc; giữ tất định (2 lần chạy trùng SHA); chạy ≤ 60 s/ca. Khi hai hướng đánh đổi nhau giữa các thành phần (một cái tăng X, cái khác giảm K và không thể cùng giữ): **ưu tiên X** (đề xuất — Minh quyết trước khi chạy). Hòa thì giữ bản đơn giản hơn. Held-out: AC@3 (X-nút) và K' của bản chọn không xấu hơn P7 trên cùng held-out; xấu hơn thì báo, không đổi lựa chọn.

Tiêu chí là đề xuất; Minh có thể đổi trước khi chạy. Sau khi xem kết quả biến thể thì không đổi (AGENTS luật cứng 13–14, 16).

## 5. Điều kiện vào (phải xong trước)

- PR FlashTicket `rca/quan-sat-log`: Minh quyết merge hay giữ nhánh (merge vào `main` = triển khai production).
- Route `tickets` 500 (lỗi có sẵn): sửa thứ tự `@RestControllerAdvice` hay khai là lỗi nền trong định nghĩa "khỏe".
- **Ngưỡng sức khỏe** cho ca bình thường và FLASH-HEALTHY (T-059 OPEN) — thiếu thì đại lượng K không đo được.
- REDIS-BOOK: thêm GET availability vào hỗn hợp tải (đổi kịch bản chuẩn) hoặc bỏ ô khỏi dev.
- Chọn baseline (mục 3b).
- **Đường phục hồi khi M1/stage lỗi giữa lượt (sửa R5):** `stage-m1.py`/`run-m1.py` của T-058 (đã ghim) tạo thư mục `exist_ok=False`, không gọi lại được cùng mã; runner T-062 chỉ cách ly lỗi theo ca. Trước lượt dài mới cần wrapper tiếp nhận (ví dụ stage lại cùng `t` với mã mới, giữ attempt cũ) và kiểm đúng tình huống thư mục đã tồn tại. Không sửa runner T-058 (đổi hash đã ghim).

## 6. Đầu ra

`results/T-0xx/`: bảng X, K từng bản × ô; ma trận D14 và baseline; hồ sơ chọn; mã M1 biến thể trong `src/` (cần SPEC liệt kê); không đụng bản P7.

## 7. Chưa kiểm

- Số lặp 3 có đủ phân biệt thành phần hay không (chưa có phương sai giữa lặp). Nếu phương sai lớn, đề xuất tăng lặp, không hạ ngưỡng.
- Ngưỡng "≥ 1 ca" trên 18 ca có nhạy với nhiễu không — chỉ biết sau khi có phương sai giữa lặp.
