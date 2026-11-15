# Đề xuất SPEC chặng 4 — Đợt phát triển M1 trên FlashTicket (chờ Minh duyệt)

- **Trạng thái:** ĐỀ XUẤT, chưa duyệt. Claude soạn trong lượt T-062 (12/11/2026). Chưa tạo task, chưa chạy gì theo file này.
- **Thuộc:** `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §3 chặng 4 ("Chạy M1 và baseline trên dữ liệu phát triển. Thử cho M1 dùng thông tin giàu hơn … Mỗi thay đổi là một thành phần có đối chứng bỏ nó; tiêu chí chọn khai trước").
- **Đầu vào đã có từ T-062:** lượt phát triển đầu với **M1 bản khóa P7** (không chỉnh) trên các ô phát triển T-059. Kết quả, bảng chấm và giới hạn: `results/T-062/bao-cao-sang.md`.

## 1. Câu hỏi chặng 4 phải trả lời

1. Trên dữ liệu FlashTicket phát triển, bản khóa P7 xếp thành phần gốc ở đâu, theo từng ô và họ lỗi? (T-062 trả lời một lượt, n=1 mỗi ô.)
2. Mỗi thành phần đề xuất (mục 3) có cải thiện xếp hạng thành phần gốc so với chính bản không có nó, trên cùng ca, không làm tăng báo động giả trên ca bình thường/FLASH-HEALTHY?
3. Chọn một phiên bản M1 cho FlashTicket để khóa ở chặng 5, theo tiêu chí khai **trước** khi xem kết quả của các biến thể.

Không trả lời ở chặng 4: hiệu quả trên tập đánh giá (chặng 6), RQ5, lợi ích đồ thị trên dữ liệu khóa.

## 1b. Điều T-062 cho thấy (n = 1, chỉ định hướng)

5/5 ô lỗi có đáp án ở hạng 1, nhưng 4/4 ca không lỗi M1 vẫn kết luận `CAUSE_FOUND` (`results/T-062/bao-cao-sang.md` §2). Vì vậy tiêu chí chặng 4 **phải** đo cả phân biệt ca lỗi/không lỗi, không chỉ AC@k. Câu hỏi chặng 4 nên thêm: thành phần nào (ngưỡng nổi bật, kênh, đồ thị) giảm báo động giả mà giữ hạng ở ca lỗi. Ô NET-GW-BOOK cho thấy M1 không biểu diễn root là cạnh (đổ cho phía bị gọi) — ứng viên C4-a mở rộng sang cạnh HTTP.

## 2. Dữ liệu

| Tập | Nội dung | Dùng để |
|---|---|---|
| Phát triển (dev) | 7 ô phát triển T-059 × **3 lặp** mỗi ô (T-062 mới có 1) + ≥ 6 ca bình thường + FLASH-HEALTHY ×2 | Chọn biến thể |
| Giữ lại trong dev (held-out dev) | 1 lặp mới của mỗi ô, chạy **sau** khi khai tiêu chí, không xem trước khi chọn | Kiểm biến thể đã chọn không quá khớp |
| Đánh giá | Ô "đợt đánh giá" của T-059 | **Không dùng ở chặng 4** (luật cứng 1) |

Chi phí ước lượng: 7×2 lặp thêm + 6 bình thường + 2 FLASH + 7 held-out ≈ 29 chu kỳ × 30 phút ≈ 14,5 giờ máy (hai đêm). Theo luật 21 phải có mục "lỗi ở 10/50/99%" trước khi phát (bộ chạy T-062 đã đáp ứng: lỗi ô chỉ chặn ô đó, M1 chạy theo từng ca).

## 3. Thành phần ứng viên (mỗi cái một đối chứng bỏ nó)

| Mã | Thay đổi | Lý do (nguồn) | Đối chứng |
|---|---|---|---|
| C4-a | DB, cache, broker thành nút từ thuộc tính span (`db.system`, `server.address`, `messaging.destination`) | T-058 KP: M1 bỏ thuộc tính span; ô EVENT-DB-LAT, REDIS-BOOK có root là cạnh dữ liệu | P7 không có C4-a |
| C4-b | Thêm kênh JVM (CPU cgroup, GC, heap) | ô CPU-BOOK; T-058 KP-04/18 | P7 không có C4-b |
| C4-c | Thêm kênh pool kết nối (Hikari) | ô POOL-BOOK (đánh giá), SLOW-BOOK đối chứng | P7 không có C4-c |
| C4-d | Thêm kênh queue (RabbitMQ ready/unacked) | ô TICKET-PAUSE (đánh giá) | P7 không có C4-d |
| C4-e | Giữ thành phần "chết im" (không loại khi mất kênh) | T-058 KP-10 | P7 không có C4-e |

Hướng 2 (M1 xếp hạng thao tác) và LLM gợi ý thao tác: **ngoài** chặng 4, giữ ứng viên.

## 4. Tiêu chí chọn (khai trước, Minh duyệt trước khi chạy biến thể)

Đơn vị: ca. Chỉ số chính: **hạng tốt nhất của tập chấp nhận T-059** trong xếp hạng M1 (`ket-qua/phat-lai/bang-cham.json#/ca/*/hang_tot_nhat`).

1. **AC@1, AC@3** trên ca lỗi dev (tỷ lệ ca có hạng tốt nhất ≤ 1, ≤ 3). Ca M1 trả ERROR/UNSUPPORTED tính là trượt.
2. **Báo động giả:** tỷ lệ ca bình thường + FLASH-HEALTHY có kết luận `CAUSE_FOUND`.
3. Một thành phần được giữ khi: AC@3 tăng ≥ 1 ca (trên 21 ca lỗi dev) so với bản bỏ nó, **và** báo động giả không tăng, **và** không làm mất hạng ở ô nào khác quá 2 bậc. Hòa thì giữ bản đơn giản hơn.
4. Biến thể chọn phải giữ tính tất định (2 lần chạy trùng SHA) và chạy ≤ 60 s/ca trên exp-obs.
5. Kiểm held-out: AC@3 của biến thể chọn trên held-out không thấp hơn P7 trên cùng held-out; nếu thấp hơn thì báo, không tự đổi lựa chọn.

Tiêu chí trên là đề xuất; Minh có thể đổi ngưỡng trước khi chạy. Sau khi đã xem kết quả biến thể thì không đổi (AGENTS luật cứng 13–14).

## 5. Điều kiện vào (phải xong trước)

- PR FlashTicket `rca/quan-sat-log` có CI xanh và Minh quyết merge hay giữ nhánh (merge vào `main` = triển khai production, cần Minh).
- Quyết định về route `tickets` trả 500 (lỗi có sẵn, `results/T-062/tiem-loi/o-loi.md`): sửa thứ tự `@RestControllerAdvice` hay giữ là điều kiện nền.
- Ô REDIS-BOOK: thêm GET availability vào hỗn hợp tải (đổi kịch bản chuẩn, cần Minh) hoặc bỏ ô khỏi dev.
- Ngưỡng khỏe FLASH-HEALTHY (T-059 OPEN).
- Phản biện T-062 (chưa chỉ định).

## 6. Đầu ra

`results/T-0xx/`: bảng AC@k từng biến thể × ô; hồ sơ chọn; mã M1 biến thể trong `src/` (cần SPEC liệt kê); không đụng bản P7.

## 7. Chưa kiểm

Số lặp 3 có đủ phân biệt thành phần hay không (chưa có phương sai giữa lặp; T-062 chỉ có 1 lặp/ô). Nếu phương sai giữa lặp lớn, tiêu chí "≥ 1 ca" có thể nhiễu — khi đó đề xuất tăng lặp, không hạ ngưỡng.
