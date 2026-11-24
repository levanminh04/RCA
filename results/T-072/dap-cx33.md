# T-072 — Đáp CX-33/33b (phần B) và CX-36b: bộ chấm v2d, phạm vi "bảo đảm p95", chữ sửa WHY-110 cập nhật

Ngày 24/11/2026, người làm Claude T-072. Không máy, không commit, không chấm lại E4, không đổi quy tắc đã khóa (`quy-tac-*.json`). Bản `dap-cx19.md` giữ nguyên (hash ở `SHA256SUMS-dap-cx19`); các chỗ thay nó được ghi rõ dưới đây. sha256 của lượt này: `SHA256SUMS-dap-cx33`.

## 1. Bộ chấm v2d (đáp CX-36b)

- **Hai lỗi của v2c:** đã tự kiểm trên code, đúng cả hai.
  - Dòng 134: không xét trường hợp dãy đúng trước lỗ đủ `for` ngay trong lỗ, nên v2c chốt 0 sai.
  - Dòng 265: v2c xét cả các phút không thể là mốc Alerting, nên báo chưa phân xử khi tử số chắc chắn.
- **Sửa:** `v2/cham_offline_v2d.py`, sinh bởi `v2/tao_v2d.py` từ v2c. Thay phép suy đoán theo từng trường hợp bằng **liệt kê chính xác**:
  - Chuỗi của mỗi luật được cắt thành các đơn vị, ngăn bởi bước đã thấy là SAI. Bước sai đặt lại Pending, nên các đơn vị độc lập với nhau.
  - Trong mỗi đơn vị, liệt kê mọi cách điền bước khuyết (2^k, k ≤ 14), rồi tổ hợp các đơn vị hệ thống (≤ 4096 tổ hợp).
  - Mỗi tổ hợp được gom theo `T072-gom-3` và đếm tử số đúng như phép chấm đã khóa.
  - Nếu mọi tổ hợp cho một giá trị thì chốt giá trị đó. Nếu có nhiều giá trị thì trả `chua-phan-xu` kèm `tu_so_kha_di`.
  - Đơn vị quá lớn chỉ được bỏ qua khi nó không chạm phút khỏe và không ở gần khoảng nào (≤ 300 s).
  - Bảng liệt kê dùng cách điền "mọi bước khuyết = sai", trùng hành vi cũ.
  - Giữ sửa A của v2c: tử số và mẫu số cùng tập phút.
- **Kiểm** (`v2/thu_ca_gia_v2d.py` → `v2/ra/thu-ca-gia-v2d.txt`, có hash mã thực chạy):
  - A: đạt.
  - D1–D7: đạt.
  - CX-36b-1: `chua-phan-xu` {0, 1}. CX-36b-2: chốt 1.
  - Hồi quy bộ cũ 9/9, `len(khoang_chay)` = [0, 1, 2, 2, 2, 2, 2, 2]; `tu_kiem()` không sai ca nào.
  - Đột biến 5/5 bị bắt.
- **Khác v2c có chủ ý, ca D4:** lỗ 30–110, bước 120 thấy sai, đúng 130–240, đầu chấm 180.
  - v2c chốt tử số 1.
  - Nếu 30–110 thật sự đúng, có khoảng cháy [90, 120). Sự cố 190 ghép vào nó vì 190 ≤ 120 + 300 (`quy-tac-gom.json#/gom_su_co`), nên t̂ = 90, nằm ngoài phút được tính, và tử số là 0.
  - Chạy đối chứng trên chuỗi đủ cho đúng hai giá trị 0 và 1, nên v2d trả `chua-phan-xu` {0, 1}.
- **Phạm vi:** v2d chỉ đổi kết quả khi lưới có bước khuyết. E2 và E4 có lưới liền, 0 khúc lỗi và 0 khoảng cháy, nên kết quả đã chấm không đổi. Theo giao việc, không chạy lại.

## 2. Phạm vi "bảo đảm p95" (CX-33 B; thay `dap-cx19.md` §2 ý 1)

**Đúng:**
- Trên lưới xuất E2, xét một bước t thuộc phút khỏe ×1 và có đủ 7 mẫu trong [t − 60, t]. Luật p95 vào Alerting tại t khi và chỉ khi S(t) > θ.
- Vì θ ≥ M = max S trên các bước đó, không bước nào trong số đó vào Alerting.

**Không bảo đảm:**
- Bước thuộc phút flash hoặc biên. Phản ví dụ: booking lúc 18:21:50Z, phút flash của E2-04, có S ≥ 0,0508 s > M = 0,0475 s (CX-33b B).
- Bước thiếu mẫu.
- Lưới đánh giá của Grafana khác pha với lưới xuất.

Số sự cố trên toàn E2 được xác định bằng cách chạy bộ chấm với ngưỡng đã chọn (`nguong.json#/trong_mau` = {}, tức 0 ở mọi lớp), không suy từ mệnh đề trên.

**Luật 5xx:**
- Chuỗi dùng tính M (`phu/ty-le-loi-chua-chan-5xx-*`) **đã** chặn ≥ 30 request. Câu ở `dap-cx19.md` §2 nói "luật thật có thêm hai chặn: ≥ 30 request và ≥ 3 lỗi" là sai một nửa; chặn thêm duy nhất là ≥ 3 lỗi 5xx.
- Vì vậy θ ≥ M là điều kiện đủ để không có Alerting ở các bước khỏe đủ mẫu; chiều ngược không đúng. Phản ví dụ: 2 lỗi / 32 request = 6,25% > 5%, nhưng luật không cháy.

## 3. Chữ sửa WHY-110 (C3), cập nhật — thay `dap-cx19.md` §4; chỉ soạn, điều phối trình Minh

Giữ nguyên quyết định, công thức, hệ số, sàn và kết quả đầu. Thay hai gạch đầu dòng, thêm hai ý.

- **Vì sao** (thay):
  > Với luật p95, trên lưới xuất E2: tại một bước thuộc phút khỏe ×1 và đủ mẫu trong cửa sổ `for`, luật vào Alerting khi và chỉ khi S > θ. Vì vậy θ ≥ M = max S trên các bước đó bảo đảm không bước nào trong số đó vào Alerting. Không có bảo đảm cho phút flash, phút biên, bước thiếu mẫu, hay lưới đánh giá khác pha. Số sự cố trên toàn E2 xác định bằng chạy bộ chấm (0). Với luật 5xx, chuỗi tính M đã chặn ≥ 30 request; luật thật chặn thêm ≥ 3 lỗi, nên θ ≥ M chỉ là điều kiện đủ. Biên k và sàn dành cho trôi giữa E2 và E4 và cho bucket thô (p95 ~0,03–0,15 s nằm trong bucket 0,025–0,25 s). Sàn lỗi 5% ≈ 3,5 lỗi trên 70 request, khớp WHY-106.
- **Phương án đã xét** (thay; giữ như `dap-cx19.md` §4):
  > (a) Phân vị cao (ví dụ 99%) của tín hiệu E2: loại, vì cần thêm một tham số tùy ý (mức phân vị) và không gắn với ngữ nghĩa `for`. Một bước vượt phân vị không tất yếu thành cảnh báo, nhưng phương án này *cho phép* các bước trong mẫu vượt ngưỡng. Max S gắn trực tiếp với `for` và không cần tham số đó.
  > (b) Chọn θ trên E2 theo mục tiêu R5: loại. Chọn trên E2 theo một mục tiêu khai trước tự nó **không** làm E4 mất độc lập. Lý do loại là R5 không xác định duy nhất θ: nhiều θ cùng đạt trên E2, nên phải khai trước cách phá hòa. Cách tự nhiên nhất, θ nhỏ nhất vẫn đạt R5, đặt θ sát biên E2 và bỏ phần biên cho trôi giữa E2 và E4.
  > (c) Ngưỡng cố định theo kinh nghiệm: loại, vì không có căn cứ trên hệ này.
- **Điều kiện thất bại** (thêm một ý vào cuối):
  > Trên E3, offline và Grafana lệch −4 s ở bốn luật thử, phù hợp với chênh pha lưới. Phép này không tách được pha với độ trễ nạp mẫu và không đo cho luật thật. Khi lưới xuất có bước khuyết, bộ chấm v2d trả "chưa phân xử" nếu tử số không xác định duy nhất; khi đó phải đếm bằng lịch sử trạng thái Grafana.
- **Bằng chứng sau khi dùng** (thêm, như `dap-cx19.md` §4):
  > E4 (khoảng độc lập): 0 sự cố / 383 phút khỏe ×1. Max S / θ: booking 0,48, event 0,46, payment 0,84, ticket 0,84 (`results/T-072/bang-bao-dong-gia.md`). Ticket chỉ cần 4 request > 0,1 s trong 5 phút là vượt θ (mô hình, chưa kiểm; `results/T-072/troi-p95-e2-e4.md`).
