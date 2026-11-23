# T-074 — Quyết định W6 cần Minh, bản 5 (danh sách duy nhất)

Soạn 23/11/2026, Claude (phiên `danh-gia-w6`). **Thay** `cau-hoi-minh-4.md` và các bản trước (giữ làm lịch sử). Chỉ gồm câu thật sự cần Minh. Chi tiết: `e6-spec-nhap-2.md` (phần A), `thiet-ke-w6-5.md` + `thiet-ke-w6-4.md` (phần B), số ở `du-toan-4.json`.

**Đã quyết, không hỏi lại:** D2 (cấu hình giữ qua E4; proxy/quota thuộc W6), R9 (ngày bán, sức chứa sửa ở E6), Q2 (nhận R5 trên E4 và chức năng E5), Q8 (phát E6 khi bản đã qua hai phiên Codex), Q9 (E7 được đi trước E6 nếu đủ điều kiện).

---

## Phần A — cần để phát E6 (máy)

**A1. Kiểm soát DB trong W7: K0 hay K2**
- **Đề xuất:** K0 — giữ DB tích lũy, trộn khối, ghi kích thước bảng mỗi ca; dùng lại 3 đối chứng BINH-THUONG ×1 làm ô mốc (mỗi khối một ô, cùng vị trí). E6 chỉ làm nhánh K0 (`e6-spec-nhap-2.md` §1–§8).
- **Lý do:** K2 cần đường xác thực Redis, quyền dừng/khởi động service, tải ngắn, đường lui khi restore dở — chưa có cái nào (CX-29 #2); W4 không cho thấy trôi p95 ở mức cả lượt; Codex (CX-29b) cũng đề xuất K0 cho đợt đầu.
- **Mặt trái:** ca cuối đợt gặp DB lớn hơn ca đầu; đối chứng ×1 bị cố định vị trí; báo cáo mang giới hạn "DB trôi trong đợt".
- **Khác:** K2 — cần SPEC bổ sung riêng (§9 của nháp) và cấp đường xác thực Redis; hoặc K0 với 3 chu kỳ mốc riêng (+3 chu kỳ).

**A2. Quyền từng máy ở E6 (nhánh K0)**
- **Đề xuất:** exp-app: chủ khung, ghi đúng các dòng ngày/sức chứa đã duyệt ở bước 1, tạo `/home/ubuntu/t074/`; exp-obs: chỉ đọc (đồng hồ, commit `/opt/rca-lab`, `docker inspect`); máy tải AWS: chỉ đọc (đồng hồ, phiên bản k6). Không runner, không tải, không Grafana/Prometheus.
- **Lý do:** đủ cho sửa ngày/sức chứa, mốc PostgreSQL và khóa bản; không tạo ca RCA (bỏ chu kỳ BINH-THUONG qua runner).
- **Mặt trái:** E6 không có giao dịch mua → xác nhận "còn bán" phía dịch vụ có thể chỉ hoàn tất ở lần mua đầu của pilot W7.
- **Khác:** cho phép một hành trình mua thật ở bước 3 (cần máy tải hoặc lệnh mua trên exp-app; tạo 1 đơn trước dump mốc → phải chờ yên lại).

**A3. Giá trị đích hạn bán và sức chứa**
- **Đề xuất:** hạn bán 2026-12-30T22:16:31.402736Z; diễn và check-in 31/12 → 01/01/2027 (giá trị đích, mọi bản sao); sức chứa = `purchased` đọc ở bước 1 + 1,5 × nhu cầu cả đợt K0 của phương án ô chọn ở B1, làm tròn lên nghìn.
- **Lý do:** đủ dư cho lặp/bù và sai số mô hình ×3; giữ thứ tự bán → diễn; dùng nhu cầu cả đợt để vẫn đủ nếu đổi sang K2.
- **Mặt trái:** thêm một lần sửa dữ liệu nghiệp vụ; giả định W7 xong trước 23/12; ngày diễn khác dữ liệu dev.
- **Khác:** hạn bán muộn hơn; không nâng sức chứa nếu B1 chọn phương án đủ vé hiện có (vẫn phải gia hạn bán).

**A4. Redis và MongoDB trong mốc E6**
- **Đề xuất:** không đọc; mốc E6 là **mốc PostgreSQL**, ghi rõ giới hạn Redis (`NOAUTH`) và MongoDB `user-db` (cần xác thực).
- **Lý do:** thông tin xác thực nằm trong cấu hình bí mật mà agent không được đọc (AGENTS §12); K0 không cần khôi phục Redis.
- **Mặt trái:** không biết trạng thái giữ chỗ/cache Redis lúc chụp mốc; không chứng minh được "hệ yên" phía Redis.
- **Khác:** Minh cấp một đường đọc Redis chỉ đọc (ví dụ lệnh do Minh chạy, hoặc người dùng Redis chỉ đọc) — cần thiết nếu sau này chọn K2.

---

## Phần B — khóa W7 (không chặn E6)

**B1. Phạm vi ô đánh giá và CPU-EVENT**
- **Đề xuất:** phương án A (SLOW-EVENT, POOL-BOOK, TICKET-PAUSE), dùng lại đối chứng làm mốc: 27 chu kỳ, 14,1 giờ thu, 35.640 đơn bảo thủ. CPU-EVENT là **ứng viên**: thêm vào khi gói code W7 tham số hóa container cho đốt/gỡ/đầu dò (`thiet-ke-w6-5.md` §6) và có SPEC E6b đặt quota Event; khi đó A + CPU-EVENT: 33 chu kỳ, 17,3 giờ.
- **Lý do:** bộ tiêm hiện đốt CPU cố định trong Booking (`inj3.py:117`); không đổi topology so với W4; đủ vé.
- **Mặt trái:** 3–4 ô là ít; không có ô cạnh mạng/dữ liệu/cache, Saga, lỗi phụ thuộc ở vị trí mới (`thiet-ke-w6-5.md` §9); kết luận RQ5 chỉ mô tả theo ô.
- **Khác:** A + B (+ CPU-EVENT): 51–57 chu kỳ, 26,7–29,8 giờ, cần 4 proxy (SPEC E6b), topology khác W4, vượt vé theo giả định bảo thủ → nâng sức chứa ở E6.

**B2. Dung sai ghép G và cảnh báo muộn**
- **Đề xuất:** G = 370 s chính, 120 s báo phụ; không kéo dài tải; chụp bất đồng bộ; ghi cờ số giây A rơi vào khoảng không tải.
- **Lý do:** đánh giá đúng luật đã khóa ở W4; không đổi thời lượng tải so dev/W4; không tăng đơn.
- **Mặt trái:** dung sai dài dễ ghép cảnh báo không liên quan; A của cảnh báo muộn có tới ~70 s không tải.
- **Khác:** kéo dài tải +90 s mỗi lượt (+85,5 phút cho 57 chu kỳ; đơn tăng — ví dụ A + CPU-EVENT có 3 mốc riêng: 47.693, vượt 46.402; `thiet-ke-w6-5.md` §7); hoặc chỉ G = 120 s.

**B3. Báo động giả ở ×3**
- **Đề xuất:** mức tải phút lấy từ lịch; ×3 báo "sự cố trên giờ quan sát ×3 đủ điều kiện"; câu báo động giả mỗi giờ khỏe ×3 để OPEN.
- **Lý do:** bộ phân loại T-071 không có nhãn khỏe ×3 và xếp ×3 cả lượt thành ×1.
- **Mặt trái:** không kết luận báo động giả ×3.
- **Khác:** định nghĩa `khoe_x3` có căn cứ riêng cho từng chỉ tiêu.

**B4. Nhánh dự phòng khi che G-inst (H8a)**
- **Đề xuất:** hành vi P7: lỗi chạy, tính trượt.
- **Lý do:** không bịa dữ liệu; đúng "bản che = V082 thiếu thông tin".
- **Mặt trái:** bản che thua vì lỗi chạy; có thể không có ca nào kích hoạt trong ô đánh giá → nhóm che không phân xử được.
- **Khác:** giữ chuỗi mới nhất (phép xử lý mới, chưa thử).

**B5. Mốc độ trễ và vùng endpoint (R-07)**
- **Đề xuất:** số chính "độ trễ từ mốc tiêm theo lịch", kèm độ lệch bộ tiêm xác nhận; không thêm đầu dò onset; nếu muốn nhãn vùng mức endpoint, thiết kế offline trên k6 `raw.json` đã lưu của T-069 trước W7.
- **Lý do:** dữ liệu theo request đã có; quy tắc onset chưa có.
- **Mặt trái:** không có "độ trễ từ lúc tác động bắt đầu"; vùng ảnh hưởng chỉ "đồ thị con nghi ngờ, độ đúng OPEN" nếu không làm phần endpoint.
- **Khác:** làm phần endpoint (0,5–1 ngày phân tích, CHƯA-KIỂM).

**B6. Baseline**
- **Đề xuất:** M4 (SimpleRCA, quy ước T-017) + BARO RobustScorer (RCAEval `259ea41`); không dùng số công bố 0,80 làm căn cứ cho M4; ca nhiều chuỗi runtime ghi `LOI_ADAPTER_DA_CHUOI`, giữ trong mẫu số như trượt, báo riêng.
- **Lý do:** đúng §8.3; một baseline đơn giản đa nguồn không dùng đồ thị và một baseline metric đã công bố; adapter P3 có sẵn (wrapper FlashTicket viết mới theo `thiet-ke-w6-5.md` §4).
- **Mặt trái:** không có baseline trace/đồ thị độc lập → không đối chiếu V082 với phương pháp cùng họ trên FlashTicket; baseline có thể thua ở ca tạo lại container vì giới hạn adapter.
- **Khác:** thêm MicroRank hoặc TraceRCA (adapter chưa ước lượng; 0 giờ máy thu); cho baseline dùng bước nối H8a như tiền xử lý chung (khai rõ).

**B7. Việc rẻ dùng lại dữ liệu đã có (khi có adapter W7)**
- **Đề xuất:** (1) chạy baseline, bản che, đối chứng quan hệ trên 17 gói T-069 (nhóm "đã phát triển", chế độ (a)); (2) đếm trên 17 gói số ca khóa thứ hai của thực thể hạng 1 đến từ mẫu truy vấn nền; (3) chạy bộ phân loại phút trên 10 phút đầu các lượt E4 đã lưu để kiểm quy tắc trên đoạn N ngắn.
- **Lý do:** luật 20; kiểm adapter và quy tắc trên dev, chỉ tính toán.
- **Mặt trái:** cần code adapter trước; gói T-069 thu trước khóa W6.
- **Khác:** để sau W7.
