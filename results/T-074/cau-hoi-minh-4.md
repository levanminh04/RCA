# T-074 — Quyết định W6 cần Minh (danh sách duy nhất, bản 4)

Soạn 23/11/2026, Claude (phiên `danh-gia-w6`). **Thay toàn bộ** `cau-hoi-minh.md`, `-2.md`, `-3.md` (giữ làm lịch sử). Chi tiết ở `thiet-ke-w6-4.md` (§ dẫn trong câu), số ở `du-toan-4.json`, E6 ở `e6-spec-nhap.md`.

**Đã có quyết định, không hỏi lại:** D2 — giữ cấu hình từ E2 qua hết E4; proxy và quota Event thuộc W6 (LOG T-070 lượt 6). R9 — hạn bán và sức chứa sửa ở E6, sau E5 (`docs/DECISIONS.md`). W4 xong (R5 đạt theo phép so đã khai), E5 xong.

Mỗi câu: đề xuất · lý do · mặt trái · phương án khác.

---

**1. Kiểm soát trạng thái DB trong W7** (bản 2 §5.3, bản 3 §F, §G)
- **Đề xuất:** K0 — giữ DB tích lũy, trộn khối, ghi kích thước bảng mỗi ca; dùng lại 3 đối chứng BINH-THUONG ×1 làm ô mốc, mỗi khối một ô ở cùng vị trí. Không làm bước 5–6 (đo khôi phục) ở E6.
- **Lý do:** dữ liệu W4 không cho thấy trôi p95 payment/ticket ở mức cả lượt (`results/T-072/troi-p95-e2-e4.md` §3); khôi phục chỉ PostgreSQL có rủi ro lệch Redis/RabbitMQ chưa kiểm; tiết kiệm 3 chu kỳ và 25–55 phút E6.
- **Mặt trái:** ca cuối đợt gặp DB lớn hơn; đối chứng ×1 không còn trộn, K ×1 đo ở vị trí cố định; báo cáo mang giới hạn "DB trôi trong đợt".
- **Khác:** K2 — đo khôi phục ở E6; nếu nhất quán, khôi phục về mốc W7 trước mỗi khối (3 lần). Hoặc K0 với 3 chu kỳ mốc riêng (+3 chu kỳ, đối chứng vẫn trộn).

**2. Phạm vi ô đánh giá** (bản 2 §4; `du-toan-4.json#/phuong_an`)
- **Đề xuất:** A + CPU-EVENT (SLOW-EVENT, POOL-BOOK, TICKET-PAUSE, CPU-EVENT): 33 chu kỳ, 17,3 giờ thu, 43.416 đơn bảo thủ, đủ 46.402 vé còn mà không cần nâng sức chứa nhiều.
- **Lý do:** không đổi topology so với W4 (chỉ thêm quota Event); đủ vé; số ô vẫn ít nhưng có bốn họ lỗi khác nhau (trễ thao tác, pool, dừng consumer, CPU).
- **Mặt trái:** không có ô cạnh mạng/dữ liệu/cache ở vị trí mới → không trả lời "cạnh có ích trên vị trí mới"; 4 ô là ít, mọi kết luận RQ5 chỉ mô tả theo ô.
- **Khác:** A + B (+ CPU-EVENT): 51–57 chu kỳ, 26,7–29,8 giờ, cần 4 proxy mới (SPEC E6b), vượt vé theo giả định bảo thủ → nâng sức chứa ở E6; topology khác W4, báo động giả trên topology W7 chỉ đo trong W7. Hoặc chỉ A (27 chu kỳ). Câu phụ: nhóm "đã phát triển" chế độ (b), 11 chu kỳ — đề xuất **không** chạy (chế độ (a) của nhóm này đã có ở gói T-069).

**3. CPU-EVENT** (bản 2 §4.2; D2)
- **Đề xuất:** đặt quota CPU Event 1,0 như Booking ở W6 (SPEC E6b nhỏ, sau E6), dùng cùng cách đốt CPU-BOOK-1.
- **Lý do:** cùng cơ chế với ô dev CPU-BOOK, nhãn xác nhận được bằng throttle.
- **Mặt trái:** đổi cấu hình máy; Event có thể chậm hơn ở ×3 (chưa đo); nền khác W4.
- **Khác:** bỏ CPU-EVENT (về phương án A).

**4. Nhánh dự phòng khi che G-inst (nhiều chuỗi runtime, H8a)** (bản 2 §3.3)
- **Đề xuất:** hành vi P7: báo lỗi chạy, tính trượt.
- **Lý do:** không bịa dữ liệu; đúng với "bản che = V082 thiếu thông tin".
- **Mặt trái:** bản che thua vì lỗi chạy; chỉ xảy ra ở ca tạo lại container — có thể không có ca nào trong ô đánh giá, nhóm che này khi đó không phân xử được.
- **Khác:** giữ chuỗi mới nhất (phép xử lý mới, chưa thử).

**5. Mốc độ trễ và vùng endpoint (R-07)** (bản 4 §9; bản 3 §H)
- **Đề xuất:** số chính "độ trễ từ mốc tiêm theo lịch" (t̂ − t), ghi kèm độ lệch bộ tiêm xác nhận; không thêm đầu dò onset ở W7. Nếu Minh muốn nhãn vùng mức endpoint, thiết kế offline trên k6 `raw.json` đã lưu của T-069 (0 giờ tải) trước W7.
- **Lý do:** dữ liệu theo request đã có; onset cần quy tắc và số request đủ mỗi route chưa có.
- **Mặt trái:** không có kết luận "độ trễ từ lúc tác động bắt đầu"; vùng ảnh hưởng chỉ báo "đồ thị con nghi ngờ, độ đúng OPEN" nếu không làm phần endpoint.
- **Khác:** làm phần endpoint (≈ 0,5–1 ngày phân tích, CHƯA-KIỂM).

**6. Việc rẻ dùng lại dữ liệu đã có** (bản 2 §4.4, §10)
- **Đề xuất:** (1) chạy baseline, bản che, đối chứng quan hệ trên 17 gói T-069 (nhóm "đã phát triển", chế độ (a)); (2) đếm trên 17 gói số ca khóa thứ hai của thực thể hạng 1 đến từ mẫu truy vấn nền. Cả hai chỉ tính toán, làm khi có adapter W7. (Việc 3 cũ — hai chu kỳ E6 phân xử DB — đã rút.)
- **Lý do:** luật 20; phép kiểm không nhãn của adapter trên dev.
- **Mặt trái:** cần code adapter trước; gói T-069 thu trước khóa W6, chỉ là nhóm "đã phát triển".
- **Khác:** để sau W7.

**7. Baseline** (bản 4 §11)
- **Đề xuất:** M4 (SimpleRCA, quy ước T-017) + BARO RobustScorer (RCAEval `259ea41`). Không dùng số công bố 0,80 làm căn cứ.
- **Lý do:** đúng §8.3; một baseline đơn giản đa nguồn không dùng đồ thị và một baseline metric đã công bố; adapter P3 có sẵn; BARO chỉ xếp hạng (K = UNSUPPORTED).
- **Mặt trái:** không có baseline trace/đồ thị độc lập → không đối chiếu V082 với phương pháp cùng họ trên FlashTicket.
- **Khác:** thêm MicroRank hoặc TraceRCA (adapter FlashTicket chưa ước lượng; 0 giờ máy thu).

**8. Giá trị đích hạn bán và sức chứa ở E6** (`e6-spec-nhap.md`)
- **Đề xuất:** hạn bán 2026-12-30T22:16:31Z, diễn 31/12–01/01 (giá trị đích, mọi bản sao); sức chứa = vé đã bán ở E6 + 1,5 × nhu cầu bảo thủ của phương án câu 2, làm tròn lên nghìn.
- **Lý do:** đủ dư cho lặp/bù; giữ thứ tự bán → diễn.
- **Mặt trái:** thêm một lần sửa dữ liệu; giả định W7 xong trước 23/12.
- **Khác:** hạn bán muộn hơn; hoặc không nâng sức chứa nếu chọn phương án A/A+CPU-EVENT (vẫn phải gia hạn bán).

**9. Dung sai ghép G và cảnh báo muộn** (bản 3 §A; bản 4 §6)
- **Đề xuất:** G = 370 s chính, 120 s báo phụ; chụp gói (b) bất đồng bộ; **không** kéo dài tải; cờ số giây A rơi vào khoảng không tải.
- **Lý do:** đánh giá đúng luật đã khóa; không đổi thời lượng tải so dev/W4; chi phí 0.
- **Mặt trái:** dung sai dài dễ ghép cảnh báo không liên quan; A của cảnh báo muộn có tới 70 s không tải.
- **Khác:** kéo dài mỗi lượt tải 90 s (+85,5 phút cho 57 chu kỳ); hoặc chỉ G = 120 s.

**10. Báo động giả ở ×3** (bản 4 §3)
- **Đề xuất:** mức tải phút lấy từ lịch; ×3 báo "sự cố trên giờ quan sát ×3 đủ điều kiện"; câu báo động giả mỗi giờ khỏe ×3 để OPEN.
- **Lý do:** bộ phân loại T-071 không có nhãn khỏe ×3 (và xếp nhầm ×3 cả lượt thành ×1).
- **Mặt trái:** không kết luận báo động giả ×3.
- **Khác:** định nghĩa `khoe_x3` có căn cứ riêng cho từng chỉ tiêu.

**11. Baseline gặp đầu vào nhiều chuỗi runtime** (bản 3 §C.2)
- **Đề xuất:** trạng thái `LOI_ADAPTER_DA_CHUOI`, giữ trong mẫu số như trượt, báo riêng.
- **Lý do:** không đổi đường dữ liệu P3 của baseline.
- **Mặt trái:** baseline thua vì giới hạn adapter (báo riêng để tách).
- **Khác:** cho mọi baseline dùng bước nối H8a như tiền xử lý chung (khi đó so V082–baseline không còn phần lợi H8a).

**12. Duyệt nháp SPEC E6** (`e6-spec-nhap.md`)
- **Đề xuất:** duyệt bước 0–4 và 7 (sửa ngày/sức chứa theo câu 8, chụp mốc W7, khóa bản); bước 5–6 chỉ nếu câu 1 chọn K2. Bước 1 dừng trình danh sách dòng sửa trước khi sửa.
- **Lý do:** R9; cần mốc W7 và khóa bản trước pilot.
- **Mặt trái:** dùng exp-app ~1,5–3 giờ ở S5; sửa dữ liệu nghiệp vụ.
- **Khác:** gộp E6 với E6b (proxy/quota) một khung nếu chọn phạm vi B hoặc CPU-EVENT — ít lần dừng máy hơn, nhưng diff cấu hình phải duyệt trước.
