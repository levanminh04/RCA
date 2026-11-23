# T-074 — Câu hỏi cho Minh, bản 2 (gom một lần, AGENTS §5a.3)

Soạn 20/11/2026, Claude (phiên `danh-gia-w6`). Mỗi câu: đề xuất, mặt trái, phương án khác, mục bị ảnh hưởng. Chi tiết ở `thiet-ke-w6.md` (§ dẫn trong câu). Số ở `du-toan.json`.

**Bản 2 (21/11/2026)** thay `cau-hoi-minh.md` (giữ nguyên). Đã có quyết định của Minh: **D2** (giữ cấu hình từ E2 qua hết E4; proxy và quota Event sang W6) và **R9** (hạn bán, sức chứa sửa ở E6, sau E5) — LOG T-070 lượt 3 và lượt 6. Sửa Q-W6-01 theo CX-06 điểm 7; Q-W6-02, Q-W6-03 bỏ phần "đặt trước E4"; Q-W6-08 đã được R9 trả lời, chỉ còn phần số lượng. Không còn câu gấp.

---

## Q-W6-01. Kiểm soát trạng thái DB trong W7 (§5.3) — bản 2

- **Đề xuất:** K0 + ô mốc (K3): giữ DB tích lũy, trộn khối, ghi kích thước bảng tại từng ca, 3 ô BINH-THUONG rải đều để đo trôi trên chính đợt. Không chờ W4, không dùng trôi E2→E4 để chọn (trôi E2→E4 chỉ báo mô tả).
- **Mặt trái:** ca cuối đợt gặp DB lớn hơn ca đầu (tới 74.520 đơn thêm theo giả định bảo thủ); trộn khối chỉ chống thiên lệch giữa ô; báo cáo mang giới hạn "DB trôi trong đợt".
- **Phương án khác:** (a) K2 — khôi phục về mốc đầu mỗi khối 6–9 chu kỳ; chỉ xét khi E6 chứng minh khôi phục nhất quán với Redis/RabbitMQ/mock, và Minh muốn chuẩn hóa trạng thái đầu; thêm 6–10 lần khôi phục, thời gian chưa đo. (b) K1 — khôi phục một lần trước đợt; vẫn trôi trong đợt.

## Q-W6-02. Phạm vi ô đánh giá (§4) — bản 2

- **Đề xuất:** A + B (SLOW-EVENT, POOL-BOOK, TICKET-PAUSE, DB-BOOK-LAT, NET-GW-EVENT, NET-PAY-BOOK, REDIS-GW; thêm CPU-EVENT theo Q-W6-03). 51–57 chu kỳ, 26,7–29,8 giờ thu. Proxy mới đặt ở W6 sau E5 (D2), giữ suốt W7.
- **Mặt trái:** đổi topology (proxy mới, tạo lại Booking/Gateway/Payment với cấu hình khác); luật W4 đo báo động giả trên topology không proxy (D2) → chuyển số W4 sang W7 là giới hạn, báo động giả trên topology W7 chỉ đo từ đoạn âm của W7; vượt sức chứa vé (Q-W6-08); thêm việc cài và xác nhận 4 proxy.
- **Phương án khác:** (a) chỉ A: 3–4 ô, 14,1–17,3 giờ, ít đổi máy; kết luận RQ5 rất hẹp, không có ô cạnh mạng/dữ liệu ở vị trí mới. (b) A + B + C: thêm HTTP5-BOOK, SAGA-TICKET-FAIL, VNPAY-REFUND-LAT — lệch bản ghim W3–W7. (c) Giảm lặp xuống 2: bớt một phần ba giờ thu, mất phần đo dao động trong ô.
- **Câu phụ:** chạy thêm nhóm "đã phát triển" ở chế độ (b)? Đề xuất: có, 11 chu kỳ (5,8 giờ), nếu sức chứa cho phép. Phương án khác: bỏ, chỉ báo nhóm đó ở chế độ (a) từ gói T-069.

## Q-W6-03. CPU-EVENT khi Event không có quota CPU (§4.2) — bản 2

- **Đề xuất:** đặt quota CPU cho Event bằng cách Booking đang có (1,0) ở W6 sau E5 (D2), cùng lúc với proxy; rồi dùng cùng cách đốt như CPU-BOOK-1.
- **Mặt trái:** đổi cấu hình máy; quota có thể làm Event chậm hơn ở ×3 (chưa đo), đổi nền so với W4 (giới hạn như Q-W6-02).
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

## Q-W6-08. Sức chứa vé cho W7 (§5.5) — bản 2

- **Đã quyết (R9):** sửa hạn bán và sức chứa ở E6, sau E5; nếu tới 28/11 E5 chưa xong thì điều phối trình lại Minh.
- **Còn cần Minh:** con số. Vé còn 73.834; W4+W5 dùng tối đa 26.136 (`results/T-071/e1/suc-chua.json`). Nhu cầu W7 theo phương án ô (`du-toan.json#/phuong_an`): A 35.640, A+CPU-EVENT 43.416, A+B 66.744, A+B+CPU-EVENT 74.520 (bảo thủ, mọi đơn giữ vé).
- **Đề xuất:** ở E6, đặt sức chứa sao cho vé còn ≥ nhu cầu bảo thủ của phương án Minh chọn cộng 50%, và hạn bán sau giờ kết thúc dự kiến của W7 ít nhất 7 ngày. Ghi giá trị cũ, đọc lại hai phía, đưa vào khóa bản.
- **Mặt trái:** thêm một lần sửa dữ liệu nghiệp vụ; nhu cầu ×3 là số suy ra (CHƯA-KIỂM).
- **Phương án khác:** chọn phạm vi A để không cần nâng sức chứa (vẫn cần gia hạn bán nếu W7 sau 02/12).
