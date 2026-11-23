# T-074 — Câu hỏi cho Minh (gom một lần, AGENTS §5a.3)

Soạn 20/11/2026, Claude (phiên `danh-gia-w6`). Mỗi câu: đề xuất, mặt trái, phương án khác, mục bị ảnh hưởng. Chi tiết ở `thiet-ke-w6.md` (§ dẫn trong câu). Số ở `du-toan.json`.

**Câu gấp cho điều phối:** Q-W6-08 (hạn bán, sức chứa) liên quan E1 đang mở.

---

## Q-W6-01. Kiểm soát trạng thái DB trong W7 (§5.3)

- **Đề xuất:** quy tắc khai trước theo kết quả W4: trôi E2→E4 vượt mức T-072 đặt → K2 (khôi phục về mốc đầu mỗi khối 6–9 chu kỳ, trộn trong khối), với điều kiện E6 chứng minh khôi phục nhất quán; ngược lại hoặc E6 trượt → K0 (giữ tích lũy, trộn khối) + 3 ô mốc BINH-THUONG rải đều (K3).
- **Mặt trái:** W7 chờ kết quả W4 và E6. K2 thêm 6–10 lần khôi phục, mỗi lần chưa đo; khôi phục chỉ PostgreSQL có thể lệch với Redis/RabbitMQ.
- **Phương án khác:** (a) chọn ngay K0 + K3, không chờ W4, chấp nhận giới hạn "DB trôi trong đợt"; (b) K1: khôi phục một lần trước đợt; (c) K2 vô điều kiện.

## Q-W6-02. Phạm vi ô đánh giá (§4)

- **Đề xuất:** A + B (SLOW-EVENT, POOL-BOOK, TICKET-PAUSE, DB-BOOK-LAT, NET-GW-EVENT, NET-PAY-BOOK, REDIS-GW; thêm CPU-EVENT theo Q-W6-03). 51–57 chu kỳ, 26,7–29,8 giờ thu. Proxy mới đặt **trước** W4 E4 nếu kịp, để luật W4 được đo báo động giả trên đúng topology W7.
- **Mặt trái:** đổi topology (proxy mới, tạo lại Booking/Gateway/Payment với cấu hình khác); vượt sức chứa vé (Q-W6-08); thêm việc cài đặt và xác nhận 4 proxy. Nếu proxy đặt sau W4 thì luật W4 chưa được đo trên topology đó.
- **Phương án khác:** (a) chỉ A: 3–4 ô, 14,1–17,3 giờ, không đổi gì trên máy; kết luận RQ5 rất hẹp, không có ô cạnh mạng/dữ liệu ở vị trí mới. (b) A + B + C: thêm HTTP5-BOOK (đổi hook hoặc hỗn hợp tải), SAGA-TICKET-FAIL (image Ticket mới), VNPAY-REFUND-LAT (thêm hoàn tiền vào tải) — lệch bản ghim W3–W7. (c) Giảm lặp xuống 2: bớt một phần ba giờ thu, mất phần đo dao động trong ô.
- **Câu phụ:** chạy thêm nhóm "đã phát triển" ở chế độ (b)? Đề xuất: có, 11 chu kỳ (5,8 giờ), nếu sức chứa cho phép. Phương án khác: bỏ, chỉ báo nhóm đó ở chế độ (a) từ gói T-069.

## Q-W6-03. CPU-EVENT khi Event không có quota CPU (§4.2)

- **Đề xuất:** đặt quota CPU cho Event bằng cách Booking đang có (1,0) trước W4 E4 (cùng lý do topology ở Q-W6-02), rồi dùng cùng cách đốt như CPU-BOOK-1.
- **Mặt trái:** đổi cấu hình máy; quota có thể làm Event chậm hơn ở ×3 (chưa đo), đổi nền của luật.
- **Phương án khác:** (a) bỏ CPU-EVENT khỏi W7, ghi giới hạn "họ CPU không có vị trí đánh giá"; (b) đốt không quota (ảnh hưởng cả máy; cơ chế khác CPU-BOOK, nhãn khó xác nhận).

## Q-W6-04. Nhánh dự phòng khi che G-inst (nhiều chuỗi runtime, H8a) (§3.3)

- **Đề xuất:** hành vi P7: ca có nhiều chuỗi runtime thì bản che báo lỗi chạy, tính trượt (như WHY-96).
- **Mặt trái:** bản che "thua" do lỗi chạy chứ không do thiếu thông tin; chỉ xảy ra ở ca có container tạo lại (có thể không có ca nào trong ô đánh giá A/B → nhóm che này không phân xử được).
- **Phương án khác:** giữ chuỗi mới nhất (một phép xử lý mới, chưa thử trên dev, làm bản che không còn đúng là "V082 thiếu thông tin").

## Q-W6-05. R-07: mốc độ trễ phát hiện (§6)

- **Đề xuất:** giữ mặc định "độ trễ theo mốc tiêm". Đồng thời cho phép đọc (chỉ đọc) đầu ra k6 hiện có để biết có ghi từng request không; nếu có, thêm đầu dò dòng thời gian (0 giờ máy thu, ~0,5 ngày code) vì nó cũng cho nhãn vùng mức endpoint (§9.3).
- **Mặt trái:** thêm code phân tích; ô không có tác động endpoint không có onset, phải báo riêng.
- **Phương án khác:** (a) chỉ mốc tiêm, vùng ảnh hưởng báo "đồ thị con nghi ngờ, độ đúng OPEN"; (b) bắt buộc đầu dò onset kể cả khi phải đổi đầu ra k6 (đổi kịch bản tải → vào khóa bản, áp mọi ô).

## Q-W6-06. Các việc rẻ dùng lại dữ liệu đã có (luật 12, 20) (§4.4, §5.4, §10)

- **Đề xuất (ba việc, đều chỉ tính toán trừ việc 3):**
  1. Chạy baseline, bản che, đối chứng quan hệ trên 17 gói T-069 → nhóm "đã phát triển" chế độ (a).
  2. Đếm trên 17 gói T-069 số ca mà khóa thứ hai của thực thể hạng 1 đến từ mẫu truy vấn nền (đo tần suất điểm yếu "một mẫu max" trên dev).
  3. Ở E6, sau khôi phục, chạy CPU-BOOK-1 và HTTP5-EVENT (2 chu kỳ, ~1 giờ) để tách một phần giả thuyết "DB lớn" khỏi "code đường mua" của T-069.
- **Mặt trái:** việc 1–2 cần adapter baseline (gói code W7) và chạy trên exp-obs hoặc laptop; việc 3 thêm ~1 giờ máy ở E6 và không tách được tranh chấp CPU.
- **Phương án khác:** làm từng việc riêng; hoặc để sau W7.

## Q-W6-07. Có thêm baseline trace hoặc đa nguồn không (§7)

- **Đề xuất:** không thêm; giữ SimpleRCA + BARO theo §8.3. SimpleRCA là baseline đơn giản đã công bố và mạnh trên RE2-TT.
- **Mặt trái:** bước 4 của cô so với "các phương pháp RCA cơ sở hiện có"; không có baseline dùng trace/đồ thị (MicroRank, TraceRCA) thì không so được với họ phương pháp đồ thị khác trên FlashTicket.
- **Phương án khác:** thêm một baseline trace (MicroRank hoặc TraceRCA, adapter đã có cho RE2-TT/Nezha ở `src/p3/adapters/`); chi phí viết adapter FlashTicket chưa ước lượng (0 giờ máy thu, vì chạy trên gói đã niêm).

## Q-W6-08 (gấp, điều phối). Hạn bán 02/12 22:16Z và sức chứa vé (§5.5)

- **Sự thật:** Booking bán tới 02/12 22:16Z. Vé còn 73.834; W4+W5 dùng tối đa 26.136 (`results/T-071/e1/suc-chua.json`). I13 cấm sửa DB từ E1 tới hết E5, nên chỉ sửa được trong E1 (đang mở) hoặc ở E6.
- **Đề xuất:** trong E1, gia hạn hạn bán của sự kiện tải (ví dụ tới 31/12) và nâng sức chứa ticket type đủ cho W7 phương án Minh chọn (A+B+CPU-EVENT cần tới 74.520 vé theo giả định bảo thủ, vượt 47.698 còn lại). Một lần sửa, ghi giá trị cũ, áp trước E2 nên E2, E4, W7 cùng điều kiện "đang bán".
- **Mặt trái:** sửa dữ liệu nghiệp vụ thêm một lần; E1 phải mở rộng phạm vi (SPEC T-071 chỉ có đồng bộ ngày Ticket/Payment và kiểm sức chứa); nếu E1 đã chụp mốc DB thì phải chụp lại.
- **Phương án khác:** (a) sửa ở E6 (sau E5) — chỉ an toàn nếu E2–E5 xong trước 02/12 22:16Z; nếu trễ, W4/W5 cũng hỏng; (b) chọn phạm vi ô nhỏ (A) để không cần nâng sức chứa, vẫn cần gia hạn bán nếu W7 sau 02/12.
