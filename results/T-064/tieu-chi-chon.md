# T-064 — Tiêu chí chọn ứng viên M1-FlashTicket (khai trước khi chấm biến thể)

- **Trạng thái:** Minh duyệt tổng thể 13/11/2026 ("tổng thể đề xuất đã ổn"). Đã qua hai lượt phản biện của Codex trong chat (R1, R2; điểm 1, 2). Hash file này phải được ghi vào `tasks/T-064-m1-flashticket/LOG.md` **trước** khi chấm biến thể đầu tiên. Sửa sau khi đã xem kết quả biến thể phải dừng hỏi Minh và khai là sửa sau.
- **Phạm vi:** chọn trên dữ liệu **phát triển** FlashTicket. So với bản P7 khóa và bản bỏ từng thành phần. **Không** so baseline (Minh chốt: so sau khi khóa).

## 1. Dữ liệu

| Tập | Nội dung | Vai trò |
|---|---|---|
| Dev bản 2 | Đợt thu chính của T-063 trên tải có mua vé: các ô lỗi phát triển (T-059 + ô dev bổ sung) và ca không tiêm lỗi, mỗi ô **một lần thu** | **Tập chọn** |
| 9 ca T-062 | Tải đọc, bản 12/11 (`results/T-062/ca/`), kèm metric bổ sung ở `ca/_metric-bo-sung/` | Tập **không hồi quy**, báo riêng, không gộp vào tập chọn (khác chuẩn tải) |
| Ô đánh giá T-059, dữ liệu khóa | — | **Không dùng** |

Ca nào vào tập chọn phải được liệt kê (mã mờ) trong LOG T-064 trước khi chấm. Ca có can thiệp không được đầu dò xác nhận không vào tập chọn.

## 2. Cách chấm

**Dùng bộ chấm và quy ước của P7(a):** `src/p3/danh_gia.py` — nhóm hòa (`tie_group`) được chấm bằng **kỳ vọng dưới hoán vị ngẫu nhiên đều trong nhóm** (§8.4). Không dùng "hạng nhóm" như `results/T-062/e2.py`. *(Chưa kiểm: bộ chấm P3 có nhận trực tiếp bản ghi của bản FlashTicket hay cần lớp chuyển; việc đầu của T-064.)*

**Bảng nút (mọi ô lỗi).** Tập chấp nhận lấy từ T-059 (`results/T-059/danh-muc-loi.json#/cells/*/common_accepted_entities`) và danh mục ô dev bổ sung của T-063. Với mỗi ca: xác suất đáp án (thành phần tốt nhất trong tập chấp nhận) nằm trong top 1 và top 3; hạng kỳ vọng. Bản có đầu ra cạnh: chiếu về nút — một cạnh ở hạng k cho hai đầu nút hạng k nếu chúng chưa có hạng tốt hơn — rồi chấm như trên.

**Bảng cạnh (chỉ ô có gốc là cạnh, theo T-059 `label_rules` "Chấm cạnh").** Hạng của **đúng cạnh có hướng và loại** trong danh sách cạnh của bản. Bản không có đầu ra cạnh (P7): ghi `UNSUPPORTED` ở bảng này, **không** quy thành trượt ở bảng nút và không quy công từ điểm nút.

**Ca không tiêm lỗi.** K = số ca M1 **không** trả `NO_INTRINSIC_ANOMALY` (`CAUSE_FOUND`, `INSUFFICIENT_EVIDENCE`, lỗi chạy, không hỗ trợ đều tính). **Đếm thô**, không trừ theo chú thích. Bảng chú thích thao tác nền (thao tác nào gây cờ, mức thay đổi, giao dịch có suy giảm không) là báo cáo kèm, không đổi cách đếm. FLASH-HEALTHY và ca có lỗi nền đã khai được báo thành nhóm riêng bên cạnh tổng.

**Trạng thái đặc biệt.** Lỗi chạy, `UNSUPPORTED`, đáp án không có trong danh sách: tính là **trượt** (hạng vô cùng). Thành phần mới không nhận được đầu vào nào: trước hết tự sửa cấu hình/bộ đóng gói/instrumentation trong quyền; chỉ khi thật sự không thể mới ghi "không thử được" — không tính đạt hay trượt, nêu bằng chứng thiếu.

## 3. So sánh hai bản

Xếp hạng nút, theo thứ tự: (1) AC@1 = tổng xác suất top 1 trên các ca lỗi; (2) AC@3; (3) tổng hạng kỳ vọng, mỗi ca cắt ở 6. Hai giá trị coi là bằng nhau khi lệch dưới 1e-9.

- **"X tốt lên":** hơn ở tiêu chí đầu tiên có khác biệt.
- **"X không xấu đi":** AC@1 không giảm và AC@3 không giảm.
- Cả hai: **không ô nào có hạng kỳ vọng tụt quá 2 bậc** (giữ theo đề xuất chặng 4 bản 3).

## 4. Luật giữ một thành phần

So bản có thành phần với bản bỏ nó, trên cùng gói đã đóng băng, theo hai phép: thêm riêng vào P7, và bỏ khỏi bản gộp. Giữ khi đạt **một trong ba**:

1. X tốt lên **và** K không tăng.
2. K giảm **và** X không xấu đi.
3. (Riêng thành phần sinh đầu ra cạnh — H1) X không xấu đi, K không tăng **và** đúng cạnh nằm trong top 3 ở ít nhất một nửa số ô cạnh của tập chọn.

Kèm điều kiện kỹ thuật: hai lần chạy cho cùng kết quả (trùng SHA); đã qua kiểm không nhãn (đầu vào thật của thành phần: số kênh/nút/cạnh mới, số lần rơi nhánh dự phòng).

**Đánh đổi** (một đại lượng tốt, đại lượng kia xấu): **không** vào bản đề xuất chính; trình thành **bản thay thế** kèm bảng đánh đổi theo từng ca để Minh xem.

**Tổ hợp:** được thử tổ hợp có căn cứ kỹ thuật (thay đổi chỉ có ích khi đi cùng nhau); tổ hợp được coi như một thành phần khi áp luật trên, và phải báo cả kết quả từng phần riêng lẻ.

## 5. Chọn khi nhiều bản cùng đạt

Thứ tự: (1) xếp hạng nút theo mục 3; (2) K nhỏ hơn; (3) bảng cạnh tốt hơn; (4) ít thành phần hơn; (5) chạy nhanh hơn. *(Thứ tự (1) trước (2) là đề xuất của Claude; đưa vào báo cáo sáng để Minh xác nhận.)*

Bản chọn phải **không hồi quy** trên 9 ca T-062: X không xấu đi và K không tăng so với P7 trên tập đó. Hồi quy thì báo, phân tích cơ chế từng ca, và trình Minh — không tự đổi lựa chọn.

## 6. Tự chủ tìm kiếm và sổ biến thể

Giữ cố định: mục tiêu, cách chấm (file này), phạm vi dữ liệu. Được mở rộng biến thể trong H1–H8 khi có lý do kỹ thuật. Mỗi biến thể một dòng trong `results/T-064/so-bien-the.jsonl` (chỉ ghi thêm): **trước khi chấm** — mã, cha, thay đổi, lý do kỹ thuật, kỳ vọng, hash code/cấu hình; **sau khi chấm** — kết quả từng ca, giữ/bỏ, vì sao. Mọi bản và kết quả đều giữ. Hồ sơ cuối báo **tổng số bản đã chấm**.

Kết thúc tìm kiếm: theo `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md` mục 5.

## 7. Phép kiểm phụ (chỉ báo cáo)

- **Độ nhạy với mốc thời gian:** chạy lại bản chọn và P7 với `t` dời ±30 s trên cùng gói. Đây **không** phải phép đo độ lặp (cửa sổ 300 s, dời 30 s giữ 90% dữ liệu).
- **Chú thích thao tác nền** cho mọi ca không tiêm lỗi.

## 8. Giới hạn phải ghi trong hồ sơ chọn

Mỗi ô một lần thu, chưa đo dao động giữa các lần chạy → bản chọn là **tạm** cho tới khi chạy lặp. Chọn trên dữ liệu đã xem, càng chấm nhiều bản càng lạc quan. Chưa so baseline. Chưa dùng ô đánh giá.
