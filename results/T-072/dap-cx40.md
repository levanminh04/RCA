# T-072 — Đáp CX-40 / CX-40b: bộ chấm v2e, chữ WHY-110 bản sửa, đơn vị rủi ro ticket

Ngày 24/11/2026, người làm Claude T-072, lượt 15. Căn cứ: DECISIONS khối 24/11 mục 2 (dùng v2d khi lưới đủ; lưới khuyết báo "chưa phân xử" và đếm riêng; dừng sửa logic lỗ) và mục 3 (WHY-110 sửa câu nhầm trạng thái/lần chuyển rồi trình lại).

Phạm vi lượt: không máy, không commit, không chấm lại E4, không đổi quy tắc đã khóa. Các file cũ giữ nguyên hash: v2, v2_claude, v2c, v2d, `dap-cx19.md`, `dap-cx33.md`, `troi-p95-e2-e4.md`. sha256 của lượt này: `SHA256SUMS-dap-cx40`.

## 1. Bộ chấm v2e (CX-40 CHẶN 1–2, CX-40b, cờ Pending)

File `v2/cham_offline_v2e.py`, sinh bởi `v2/tao_v2e.py` từ v2d. Ca thử: `v2/thu_ca_gia_v2e.py`, kết quả ở `v2/ra/thu-ca-gia-v2e.txt`.

- **Lưới đủ:** kết quả trùng v2d từng trường (8 ca A/D).
- **Lưới khuyết:** trả `chua-phan-xu`, để trống tử số khả dĩ (`tu_so_kha_di = null`), và đếm riêng trong mục `luoi_khuyet`: số đoạn, số bước, số phút có bước khuyết, số phút khỏe bị ảnh hưởng, số phút khỏe ngoài lưới.
  - "Lưới khuyết" nghĩa là: một luật hệ thống có bước khuyết trong lưới, hoặc một phút khỏe theo bảng phân loại không có bước lưới nào.
  - Bảng liệt kê sự cố vẫn giữ, chỉ để tham khảo.
  - Hai phản ví dụ của CX-40 (CHẶN 1 lỗ dài và CHẶN 2 mất trọn một phút) nay ra "chưa phân xử". Phép liệt kê của v2d không được dùng để kết luận khi lưới khuyết.
  - Không sửa tiếp logic lỗ, theo quyết định 24/11.
- **CX-40b (hai file xuất chồng thời gian):** đây là lỗi cơ học trong `Du.them`. v2e ghi lại, theo từng chuỗi, các bước có quan sát hợp lệ. Một bước chỉ là khuyết khi **không file nào** cho quan sát hợp lệ. Với ca của CX-40b, v2e trả 1/3 ở cả hai thứ tự nạp file.
- **Cờ `pending-sau-lo-luoi`:** chỉ gắn khi bước khuyết đứng **trước** Pending trong cùng đơn vị.
- **Kiểm:**
  - Các ca lưới khuyết: D2, D3, D4, D6, D7, CX-40 CHẶN 1a và 1b, CHẶN 2, phút khỏe ngoài lưới.
  - Mỗi ca CX-40 đều tái hiện được lỗi của v2d để chứng minh phép thử bắt đúng lỗi.
  - Hồi quy 9 ca cũ đạt 9/9, `len(khoang_chay)` = [0, 1, 2, 2, 2, 2, 2, 2]; `tu_kiem()` không sai ca nào.
  - Đột biến 3/3 bị bắt.
- **Hệ quả cho E2/E4:** lưới liền, 0 khúc lỗi, nên v2e cho kết quả như v2d và như bản khóa. Theo giao việc, không chạy lại.

## 2. Chữ WHY-110 bản sửa (C3) — thay `dap-cx33.md` §3; chỉ soạn, điều phối trình Minh

Lỗi đã sửa (CX-40 CHẶN 3, CX-40b mục 3): câu cũ "luật **vào** Alerting tại t khi và chỉ khi S(t) > θ" nhầm *trạng thái* Alerting với *thời điểm chuyển* vào Alerting. Phản ví dụ: tín hiệu vượt liên tục từ 20 đến 110 cho một khoảng [80, 120). Tại 90 vẫn có S > θ, nhưng t̂ = 80. Câu bảo đảm về bộ chấm cũng được thu hẹp lại.

Giữ nguyên quyết định, công thức, hệ số, sàn, kết quả đầu và các dòng **Chọn gì**, **Giới hạn**, **Bằng chứng (chỉ kiểm code)**, **Kết luận phụ thuộc**. Thay hoặc thêm các ý sau.

- **Vì sao** (thay):
  > Trên lưới xuất E2, xét bước t thuộc phút khỏe ×1 có đủ bảy mẫu trong [t − 60 s, t]. S(t) > θ khi và chỉ khi điều kiện p95 > θ đã duy trì suốt cửa sổ đó, tức luật đang ở trạng thái Alerting tại t. Thời điểm chuyển vào Alerting (t̂) là bước đầu tiên đủ `for` của một dãy vượt ngưỡng. Với θ ≥ M = max S trên tập bước đó, không bước nào trong tập thỏa điều kiện này. Không có bảo đảm cho phút flash, phút biên, bước thiếu mẫu, hay lưới đánh giá khác pha. Số sự cố trên toàn E2 xác định bằng chạy bộ chấm với ngưỡng đã chọn: 0. E2 có 356 phút khỏe ×1 (< 360), nên E2 là khoảng chọn ngưỡng, không dùng để kết luận R5. Với luật 5xx, chuỗi tính M đã chặn ≥ 30 request; luật thật chặn thêm ≥ 3 lỗi 5xx, nên θ ≥ M chỉ là điều kiện đủ trên tập bước đang xét. Ví dụ 2 lỗi / 32 request vượt 5% nhưng không cháy. Biên k và sàn dành cho trôi giữa E2 và E4 và cho bucket thô (p95 ~0,03–0,15 s nằm trong bucket 0,025–0,25 s). Sàn lỗi 5% ≈ 3,5 lỗi trên 70 request, khớp WHY-106.
- **Phương án đã xét** (thay; mục (b) đổi tên theo CX-40b):
  > (a) Phân vị cao (ví dụ 99%) của tín hiệu E2: loại, vì cần thêm một tham số tùy ý (mức phân vị) và không gắn với ngữ nghĩa `for`. Một bước vượt phân vị không tất yếu thành cảnh báo, nhưng phương án này *cho phép* các bước trong mẫu vượt ngưỡng. Max S gắn trực tiếp với `for` và không cần tham số đó.
  > (b) Tối ưu tỷ lệ báo động giả trên E2 (chọn θ để số sự cố trên E2 vừa đạt mục tiêu R5): loại. Chọn trên E2 theo một mục tiêu khai trước tự nó **không** làm E4 mất độc lập. Lý do loại là mục tiêu đó không xác định duy nhất θ: nhiều θ cùng đạt, nên phải khai trước cách phá hòa. Cách tự nhiên nhất, θ nhỏ nhất vẫn đạt, đặt θ sát biên E2 và bỏ phần biên cho trôi giữa E2 và E4.
  > (c) Ngưỡng cố định theo kinh nghiệm: loại, vì không có căn cứ trên hệ này.
- **Điều kiện thất bại** (thêm một ý vào cuối):
  > Trên E3, offline và Grafana lệch −4 s ở bốn luật thử, phù hợp với chênh pha lưới. Phép này không tách được pha với độ trễ nạp mẫu và không đo cho luật thật. Khi lưới xuất khuyết, bộ chấm (v2e, DECISIONS 24/11 mục 2) trả "chưa phân xử" và đếm riêng phần khuyết; tử số khi đó phải lấy từ lịch sử trạng thái Grafana.
- **Bằng chứng sau khi dùng** (thêm):
  > E4 (khoảng độc lập, lưới liền): 0 sự cố / 383 phút khỏe ×1. Max S / θ: booking 0,48, event 0,46, payment 0,84, ticket 0,84 (`results/T-072/bang-bao-dong-gia.md`). Với giả định 72 request mỗi cửa sổ 5 phút, ticket chỉ cần 4 request > 0,1 s trong một cửa sổ là p95 của cửa sổ đó vượt θ. Đây là mô hình, chưa kiểm, và đơn vị là cửa sổ chứ không phải sự cố (`results/T-072/troi-p95-e2-e4.md`, đính chính `dap-cx40.md` §3).

## 3. Đơn vị rủi ro ticket (CX-33 C, CX-40, CX-40b) — đính chính `troi-p95-e2-e4.md` §4 và dòng STATE

- **Đúng:** đầu ra mô hình là **kỳ vọng số cửa sổ 5 phút có p95 vượt θ, trên 72 cửa sổ rời nhau mỗi 6 giờ**. Ở tỷ lệ chậm của lượt E4-06 là 1,0424 cửa sổ / 6 giờ (`troi-p95-rui-ro.json#/route/ticket/theo_ty_le/max_luot_x1`).
- Giả định của mô hình: 72 request / cửa sổ; request chậm độc lập; mọi request chậm nằm trong bucket (0,1; 0,25] s.
- Mô hình **chưa** áp `for` 60 s trên lưới trượt, **chưa** ghép 300 s thành sự cố.
- **Sai cần sửa:** câu "kỳ vọng tăng lên khoảng 1 / 6 giờ, chạm ngưỡng R5" (`troi-p95-e2-e4.md` dòng 67) và cụm "rủi ro ≈ 1/6 giờ" trong STATE đọc như số sự cố. Điều đó sai: cùng một số cửa sổ vượt có thể là nhiều đợt rời nhau hoặc một đợt kéo dài, nên không so trực tiếp với R5 được. Muốn có tần suất sự cố cần chuỗi thời gian tương ứng rồi áp `for` và ghép; đây là câu hỏi mở. Bảng đáp lượt 14 thiếu điểm C; đã bổ sung ở bảng lượt 15 trong LOG.
