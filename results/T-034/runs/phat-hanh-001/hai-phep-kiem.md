# T-034 — Kết quả hai phép kiểm E1 và E2

Ngày 13/10/2026. Người làm: Claude. Người phản biện kết quả: Codex.

Hai phép này trả lời hai câu mà gói đính chính ngày 13/10 của T-032 và T-033 ghi là “còn kiểm được, chưa chạy”. Cả hai chỉ dùng ca dev. Cả hai là **chẩn đoán**: không thay số, cấu hình hay cách chấm của bảng baseline đã khóa.

Thiết kế và bảng diễn giải được viết trước khi chạy nhánh đổi: `results/T-034/thiet-ke-hai-phep-kiem.md` (bản đầu và năm mục nối có thời điểm). Số trong file này lấy từ `results/T-034/hai-phep-kiem.json`; file đó gom đầu ra của các lượt trong `results/T-034/runs/`.

## 0. Tóm tắt

**E1 (TraceRCA, quy tắc pattern).** Bản cài theo lời văn của bài chấm một dịch vụ bằng giá trị lớn nhất qua mọi tập dịch vụ được giữ có chứa nó. Phép kiểm chỉ đổi đúng điểm đó: chỉ cho tập một dịch vụ đóng góp điểm, giữ nguyên mọi thứ khác.

- Ở cờ một lần độ lệch chuẩn (mặc định của bài): 1/7 cặp Nezha-OB có hiện tượng đổi chiều, 0/3 cặp RE2-TT đổi chiều. Vậy quy tắc “chấm qua tập nhiều dịch vụ” **không** phải bước đưa dịch vụ gọi lên trên root ở cấu hình này.
- Ở cờ ba lần độ lệch chuẩn: 4/5 cặp Nezha-OB đổi chiều, cả hai bên vẫn còn bằng chứng. Ở cấu hình này quy tắc đó là bước quyết định ở phần lớn cặp Nezha-OB.
- RE2-TT không đổi ở cả ba nhánh: root không có tập nào được giữ, nên quy tắc pattern không chạm tới root.

**E2 (BOCPD, miền log).** Tính lại toàn bộ posterior trong miền log trên bốn chuỗi của hai ca có underflow.

- 3/4 chuỗi: trạng thái có xác suất cao nhất (MAP) và điểm đổi (CP) trùng bản gốc ở mọi bước.
- 1 chuỗi (đầu vào full của dev-3ae0a6c15a): MAP khác ở 12 bước liên tiếp ngay sau mốc tiêm; bản gốc có 1 điểm đổi mà phép tính đúng không có và thiếu 3 điểm đổi. Mọi khác biệt nằm trong 45 giây đầu sau mốc.
- Ở cả bốn chuỗi, báo động đầu và mọi điểm đổi trước mốc tiêm giữ nguyên. Underflow không giải thích các báo động trước mốc của hai ca này.

## 1. E1 — Quy tắc pattern của TraceRCA

### 1.1 Câu hỏi và yếu tố bị đổi

Câu hỏi: ở các cặp (root, dịch vụ gọi) mà dịch vụ gọi đứng trên root trong bản cài theo lời văn, việc cho dịch vụ lấy điểm từ tập nhiều dịch vụ có phải là bước gây ra điều đó không?

Giữ nguyên: lời gọi, cờ bất thường, trace nào chứa dịch vụ nào, tập phổ biến đã khai phá, tập được giữ sau bước chọn, công thức điểm, quy tắc hòa. Đổi đúng một thứ: tập nào trong chính danh sách được giữ được phép đóng góp điểm (mọi tập, hoặc chỉ tập một dịch vụ). Không khai phá lại, không thêm tập một dịch vụ đã bị loại.

Phạm vi khai trước: 13 cặp thuộc 11 ca trong bảng đối chiếu của gói đính chính (`closure-ledger-review-001.json`, mục `h6_pair_audit`). Ba nhánh cờ: `to_p` (một lần độ lệch chuẩn, span phía gọi; nhánh chính), `to_p3` (ba lần), `to_c` (span phía được gọi; báo phụ). Các cặp chung một ca không độc lập.

Trước khi can thiệp tôi đọc lại Mục III-B và III-C của bài TraceRCA và mã tác giả đã ghim. Bài viết điểm dịch vụ là giá trị lớn nhất qua **mọi** tập nghi ngờ chứa nó. Mã tác giả chỉ chấm tập một dịch vụ. Vậy bản cài theo lời văn khớp bài ở điểm này; không có căn cứ gọi quy tắc “chấm qua mọi tập” là lỗi cài.

### 1.2 Kiểm tương đương (V6: PASS)

- Bản giữ nguyên quy tắc cho kết quả trùng bản lưu của T-032 ở 11/11 ca, 0 khác biệt trên mọi trường (điểm dạng phân số, hạng, tập tốt nhất, trạng thái).
- Bản tính lại độc lập (khai phá bằng cách khác, số học phân số) trùng tập phổ biến, tập được giữ và điểm của cả hai nhánh ở 28/28 kết quả nhánh có điểm.
- 5 kết quả nhánh không có đặc trưng hữu ích; ghi trạng thái, không tính là điểm.
- Ví dụ nhỏ tính tay (ví dụ Hình 2 của bài) đúng cho cả hai quy tắc.
- Thời gian máy: 30 giây cho cả 11 ca trên EC2 của T-032.

### 1.3 Kết quả theo cặp

**Nhánh chính `to_p` (cờ một lần độ lệch chuẩn).**

| Dataset | Ca | Root | Dịch vụ gọi | Quan hệ, chấm qua mọi tập | Quan hệ, chỉ tập một dịch vụ | Điểm root (mọi tập → một dịch vụ) | Điểm dịch vụ gọi (mọi tập → một dịch vụ) | Cỡ tập quyết định điểm dịch vụ gọi | Mã tác giả, ngưỡng chọn đặc trưng một / ba (root so với dịch vụ gọi) | Phân loại |
|---|---|---|---|---|---|---|---|---|---|---|
| RE2-TT | dev-12a1a88069 | ts-order-service | ts-seat-service | root dưới | root dưới | 0,0 → 0,0 | 101,3 → 101,3 | 1 | trên / hòa | không đổi; root không có tập nào được giữ |
| RE2-TT | dev-db293894ab | ts-travel-service | ts-seat-service | root dưới | root dưới | 0,0 → 0,0 | 99,6 → 99,6 | 1 | dưới / trên | không đổi; root không có tập nào được giữ |
| RE2-TT | dev-f36d0647d5 | ts-order-service | ts-seat-service | root dưới | root dưới | 0,0 → 0,0 | 75,9 → 75,9 | 1 | trên / hòa | không đổi; root không có tập nào được giữ |
| RE2-TT | dev-f36d0647d5 | ts-order-service | ts-travel-service | hòa | hòa | 0,0 → 0,0 | 0,0 → 0,0 | — | trên / hòa | không đổi; cả hai không có tập nào được giữ |
| Nezha-OB | dev-14701a3bbb | shippingservice | frontend | root dưới | root dưới | 54,8 → 54,8 | 206,8 → 201,7 | 2 | trên / trên | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-3e27669440 | adservice | frontend | root dưới | root dưới | 279,7 → 279,7 | 470,6 → 441,5 | 2 | trên / trên | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-515c5f2190 | recommendationservice | frontend | root dưới | root dưới | 55,0 → 55,0 | 282,5 → 266,1 | 2 | dưới / dưới | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-5467884de4 | recommendationservice | frontend | root dưới | root dưới | 365,2 → 365,2 | 401,1 → 391,7 | 3 | trên / trên | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-63c30faf34 | recommendationservice | frontend | root dưới | root trên | 500,2 → 500,2 | 527,4 → 485,3 | 2 | trên / trên | đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-6c9afc9822 | emailservice | frontend | root dưới | root dưới | 0,0 → 0,0 | 236,9 → 236,9 | 1 | trên / trên | không đổi; root không có tập nào được giữ |
| Nezha-OB | dev-6c9afc9822 | emailservice | checkoutservice | hòa | hòa | 0,0 → 0,0 | 0,0 → 0,0 | — | trên / trên | không đổi; cả hai không có tập nào được giữ |
| Nezha-OB | dev-7d3c2fe6d1 | shippingservice | frontend | root dưới | root dưới | 76,4 → 76,4 | 237,7 → 237,4 | 2 | trên / trên | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-95e164235f | paymentservice | checkoutservice | không có quan hệ (NO_USEFUL_FEATURE) | — | — | — | — | — | nhánh không có đặc trưng hữu ích |

**Nhánh `to_p3` (cờ ba lần độ lệch chuẩn).**

| Dataset | Ca | Root | Dịch vụ gọi | Quan hệ, chấm qua mọi tập | Quan hệ, chỉ tập một dịch vụ | Điểm root (mọi tập → một dịch vụ) | Điểm dịch vụ gọi (mọi tập → một dịch vụ) | Cỡ tập quyết định điểm dịch vụ gọi | Mã tác giả, ngưỡng chọn đặc trưng một / ba (root so với dịch vụ gọi) | Phân loại |
|---|---|---|---|---|---|---|---|---|---|---|
| RE2-TT | dev-12a1a88069 | ts-order-service | ts-seat-service | root dưới | root dưới | 0,0 → 0,0 | 34,9 → 34,9 | 1 | trên / hòa | không đổi; root không có tập nào được giữ |
| RE2-TT | dev-db293894ab | ts-travel-service | ts-seat-service | root dưới | root dưới | 0,0 → 0,0 | 48,2 → 48,2 | 1 | dưới / trên | không đổi; root không có tập nào được giữ |
| RE2-TT | dev-f36d0647d5 | ts-order-service | ts-seat-service | root dưới | root dưới | 0,0 → 0,0 | 32,2 → 32,2 | 1 | trên / hòa | không đổi; root không có tập nào được giữ |
| RE2-TT | dev-f36d0647d5 | ts-order-service | ts-travel-service | hòa | hòa | 0,0 → 0,0 | 0,0 → 0,0 | — | trên / hòa | không đổi; cả hai không có tập nào được giữ |
| Nezha-OB | dev-14701a3bbb | shippingservice | frontend | root dưới | root trên | 78,4 → 78,4 | 79,3 → 74,9 | 2 | trên / trên | đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-3e27669440 | adservice | frontend | root dưới | root trên | 286,9 → 284,2 | 306,6 → 264,2 | 3 | trên / trên | đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-515c5f2190 | recommendationservice | frontend | root dưới | root dưới | 55,9 → 55,9 | 277,8 → 225,0 | 2 | dưới / dưới | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-5467884de4 | recommendationservice | frontend | root dưới | root trên | 403,7 → 402,8 | 412,3 → 353,1 | 3 | trên / trên | đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-63c30faf34 | recommendationservice | frontend | root dưới | root trên | 517,0 → 517,0 | 525,5 → 443,8 | 2 | trên / trên | đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-6c9afc9822 | emailservice | frontend | hòa | root trên | 5,1 → 5,1 | 5,1 → 0,0 | 2 | trên / trên | đổi vì một bên mất mọi tập được chấm |
| Nezha-OB | dev-6c9afc9822 | emailservice | checkoutservice | root trên | root trên | 5,1 → 5,1 | 0,0 → 0,0 | 1 | trên / trên | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-7d3c2fe6d1 | shippingservice | frontend | root trên | root trên | 105,4 → 105,4 | 95,7 → 84,4 | 2 | trên / trên | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-95e164235f | paymentservice | checkoutservice | không có quan hệ (NO_USEFUL_FEATURE) | — | — | — | — | — | nhánh không có đặc trưng hữu ích |

**Nhánh `to_c` (span phía được gọi, báo phụ).**

| Dataset | Ca | Root | Dịch vụ gọi | Quan hệ, chấm qua mọi tập | Quan hệ, chỉ tập một dịch vụ | Điểm root (mọi tập → một dịch vụ) | Điểm dịch vụ gọi (mọi tập → một dịch vụ) | Cỡ tập quyết định điểm dịch vụ gọi | Mã tác giả, ngưỡng chọn đặc trưng một / ba (root so với dịch vụ gọi) | Phân loại |
|---|---|---|---|---|---|---|---|---|---|---|
| RE2-TT | dev-12a1a88069 | ts-order-service | ts-seat-service | root dưới | root dưới | 0,0 → 0,0 | 104,1 → 104,1 | 1 | trên / hòa | không đổi; root không có tập nào được giữ |
| RE2-TT | dev-db293894ab | ts-travel-service | ts-seat-service | root dưới | root dưới | 0,0 → 0,0 | 55,5 → 55,5 | 1 | dưới / trên | không đổi; root không có tập nào được giữ |
| RE2-TT | dev-f36d0647d5 | ts-order-service | ts-seat-service | root dưới | root dưới | 0,0 → 0,0 | 46,6 → 46,6 | 1 | trên / hòa | không đổi; root không có tập nào được giữ |
| RE2-TT | dev-f36d0647d5 | ts-order-service | ts-travel-service | hòa | hòa | 0,0 → 0,0 | 0,0 → 0,0 | — | trên / hòa | không đổi; cả hai không có tập nào được giữ |
| Nezha-OB | dev-14701a3bbb | shippingservice | frontend | root dưới | root dưới | 17,7 → 17,7 | 190,2 → 190,0 | 2 | trên / trên | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-3e27669440 | adservice | frontend | root dưới | root dưới | 221,4 → 220,6 | 397,3 → 396,7 | 2 | trên / trên | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-515c5f2190 | recommendationservice | frontend | root dưới | root dưới | 234,1 → 234,1 | 316,1 → 316,1 | 1 | dưới / dưới | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-5467884de4 | recommendationservice | frontend | không có quan hệ (NO_USEFUL_FEATURE) | — | — | — | — | — | nhánh không có đặc trưng hữu ích |
| Nezha-OB | dev-63c30faf34 | recommendationservice | frontend | không có quan hệ (NO_USEFUL_FEATURE) | — | — | — | — | — | nhánh không có đặc trưng hữu ích |
| Nezha-OB | dev-6c9afc9822 | emailservice | frontend | không có quan hệ (NO_USEFUL_FEATURE) | — | — | — | — | — | nhánh không có đặc trưng hữu ích |
| Nezha-OB | dev-6c9afc9822 | emailservice | checkoutservice | không có quan hệ (NO_USEFUL_FEATURE) | — | — | — | — | — | nhánh không có đặc trưng hữu ích |
| Nezha-OB | dev-7d3c2fe6d1 | shippingservice | frontend | root dưới | root dưới | 34,1 → 34,1 | 168,1 → 167,9 | 2 | trên / trên | không đổi; cả hai còn tập được chấm |
| Nezha-OB | dev-95e164235f | paymentservice | checkoutservice | hòa | hòa | 0,0 → 0,0 | 0,0 → 0,0 | — | hòa / không có bằng chứng | không đổi; cả hai không có tập nào được giữ |

Cột “Mã tác giả” lấy nguyên từ bảng đối chiếu của gói đính chính, để đặt cạnh. Đó là pipeline khác; chênh giữa hai pipeline không phải tác dụng của phép đổi này.

### 1.4 Đọc kết quả

**Nezha-OB, nhánh chính.** Trong 7 cặp có hiện tượng (root dưới dịch vụ gọi):

- 6 cặp có điểm của dịch vụ gọi do một tập nhiều dịch vụ quyết định, và điểm đó giảm ở 6 cặp khi chỉ chấm tập một dịch vụ. Mức giảm tương đối lớn nhất là 8,0%.
- Chỉ 1 cặp đổi chiều; 6 cặp giữ nguyên. Trong số giữ nguyên có 1 cặp root không có tập nào được giữ.
- Vậy phép đổi **có tác động lên điểm** ở hầu hết các cặp, nhưng **không đổi quan hệ thứ hạng** ở hầu hết các cặp. Tập một dịch vụ của frontend tự nó đã đủ cao.

Trung gian cho thấy vì sao. Ở 7 cặp có dịch vụ gọi là frontend, frontend mang cờ ở lời gọi đi ra trong 95,8% đến 100% số trace bất thường. Trong đó có từ 28 đến 387 trace mà root không mang cờ ở lời gọi đi vào. Đây là mô tả từ bảng cờ đã lưu, chưa phải phép đổi: nó chỉ ra bước cần xét tiếp là **lời gọi nào được gắn cờ**, không phải cách gộp tập.

**Nezha-OB, cờ ba lần.** 4/5 cặp có hiện tượng đổi sang “root trên”, cả root và dịch vụ gọi vẫn còn tập được chấm. Thêm 1 cặp chuyển từ hòa sang “root trên” vì dịch vụ gọi mất mọi tập được chấm; trường hợp này ghi riêng là mất bằng chứng, không tính là bằng chứng dịch vụ gọi bình thường.

**RE2-TT.** Ở cả ba nhánh, 3 cặp có hiện tượng đều giữ nguyên; điểm của dịch vụ gọi không đổi ở cặp nào (0 cặp đổi điểm). Lý do nằm ở bước trước đó: root không có tập nào trong danh sách được giữ ở 3/3 cặp. Tập chỉ gồm root là tập phổ biến ở 3/3 ca (có mặt trong 26% đến 37% trace bất thường) nhưng lọt vào danh sách được giữ ở 0 ca. Bước loại nó là bước chọn tập theo điểm, không phải quy tắc chấm.

**Đặt cạnh mã tác giả.** Ở Nezha-OB mã tác giả (ngưỡng chọn đặc trưng một) cho root trên dịch vụ gọi ở 7/8 cặp. Phép E1 ở cùng mức cờ chỉ đổi chiều 1 cặp. Vậy khác biệt giữa hai pipeline ở mức cờ này **không** do quy tắc pattern; nó nằm ở các bước E1 không đụng tới (dựng lời gọi, chọn đặc trưng theo cặp, chuẩn nền, chọn tập).

### 1.5 Kết luận trong phạm vi đã thử

| Câu | Trả lời | Mức |
|---|---|---|
| Ở cờ một lần độ lệch chuẩn, chấm qua tập nhiều dịch vụ có phải bước đưa dịch vụ gọi lên trên root? | Đã loại, trong 13 cặp đã khai: đổi quy tắc chỉ đổi chiều 1 cặp Nezha-OB và 0 cặp RE2-TT | CT |
| Ở cờ ba lần độ lệch chuẩn? | Đã xác lập cho Nezha-OB: 4/5 cặp đổi chiều khi chỉ đổi quy tắc này | CT |
| Bước nào gây chênh giữa bản cài theo lời văn và mã tác giả ở cờ một lần? | Chưa phân xử. Hai ứng viên có trung gian chỉ ra: cờ ở lời gọi đi ra của frontend; bước chọn tập loại tập chỉ gồm root ở RE2-TT | MT |

Phép này **không** cho biết: dịch vụ gọi có thật sự chờ root hay không (không đo lan vật lý); quy tắc nào “đúng”; phương pháp nào tốt hơn. Kết quả không suy rộng ra ngoài 13 cặp và ba nhánh cờ đã khai.

### 1.6 Hệ quả

- Bản đồ hạn chế, dòng G2-H05: thay “ứng viên pattern nhiều dịch vụ, chưa kiểm riêng” bằng kết quả trên.
- Ứng viên “quy tắc chấm pattern” ở mục 5 của gói G2: có căn cứ ở cờ ba lần; ở cờ một lần thì không.
- Hai phép còn kiểm được trên dev, chưa được giao (mục 6 của gói G2): chỉ đổi bước chọn tập; đối chiếu cờ theo từng lời gọi với nhánh mã tác giả.

## 2. E2 — BOCPD đầy đủ trong miền log

### 2.1 Câu hỏi và yếu tố bị đổi

BOCPD bản BARO nhân xác suất rất nhỏ qua nhiều bước. Khi một giá trị nhỏ hơn mức số thực biểu diễn được, nó bị làm tròn thành không (underflow) và nhánh đó không bao giờ sống lại. Câu hỏi: điều đó có làm đổi posterior, MAP hay điểm đổi không?

Giữ nguyên: dữ liệu X, thứ tự cột, prior, hazard, lớp phân phối dự báo và phép cập nhật tham số của mã gốc, quy ước chỉ số và quy tắc điểm đổi. Đổi đúng một thứ: phép đệ quy posterior được tính bằng log-mật độ và chuẩn hóa log-sum-exp ở mọi bước, thay cho nhân và chia số thực thường. Không thêm sàn, nhiễu hay cắt run length.

Phạm vi: hai ca `dev-3ae0a6c15a` và `dev-ba831dbeb8`; mỗi ca hai chuỗi: FF (tiền xử lý trên cả bản ghi, là đầu vào của baseline) và PF (tiền xử lý chỉ trên đoạn trước mốc, nhánh chẩn đoán của T-033).

### 2.2 Kiểm tương đương (V7: PASS)

- **Ví dụ nhỏ (F1–F4), chạy trên cùng máy và môi trường:** đạt cả bốn (trường `fixtures_pass`: có). F1 không underflow: bản miền log trùng bản gốc. F2 có underflow: bản miền log trùng tham chiếu độ chính xác cao (mpmath). F3 là đối chứng dương: một nhánh đã bị bản gốc cho bằng không phải sống lại; bản miền log trùng tham chiếu, bản gốc thì không. F4 kiểm chính tham chiếu số thực mở rộng.
- **Bản giữ nguyên:** chạy lại mã gốc cho R trùng bản lưu của T-033 **từng bit** ở 4/4 chuỗi.
- **Tham chiếu độc lập trên chuỗi thật:** chạy đúng đệ quy tuyến tính của mã gốc bằng số thực mở rộng 80 bit (không có log-sum-exp). MAP và CP của tham chiếu trùng bản miền log ở 4/4 chuỗi; lệch log lớn nhất 1,3e-10 (ngưỡng khai trước `1e-8`).
- **Trước khi underflow có khối lượng đáng kể,** trạng thái sạch lệch nhiều nhất 2,2e-11 giữa bản gốc và bản miền log (ngưỡng `1e-9`).
- **Đối chiếu với phép cũ của T-033** (giữ cố định hệ số chuẩn hóa, từng nhánh): lệch nhiều nhất 1,2e-12.

Lượt đầu (`e2-001`) tôi đặt một luồng tính cho thư viện đại số, khác cấu hình của lượt gốc. Khi đó R không trùng từng bit: mật độ lệch tương đối tới 2,1e-12 và chỉ 55% phần tử R trùng bit; với cấu hình của nguồn thì 720/720 hàng mật độ trùng bit. MAP và CP của bản miền log ở lượt đó trùng lượt dùng để kết luận ở 4/4 chuỗi. Lượt `e2-001` được giữ làm đối chiếu, không dùng để kết luận.

### 2.3 Bốn chuỗi

| Ca | Nhánh | Số điểm | Số chiều | Bản giữ nguyên trùng bản lưu từng bit | Trạng thái bị bản gốc cho bằng không | Trạng thái dưới chuẩn hóa | Lệch log lớn nhất so với tham chiếu mở rộng | Số điểm MAP khác | Số điểm đổi (bản gốc / miền log) | Khoảng cách biến thiên toàn phần lớn nhất | Báo động đầu giữ nguyên |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dev-3ae0a6c15a | tiền xử lý trên đoạn trước mốc (PF) | 720 | 30 | có | 45.875 | 5.035 | 1,2e-11 | 0 | 2 / 2 | 4,8e-14 | có |
| dev-3ae0a6c15a | tiền xử lý trên cả bản ghi (FF) | 1.441 | 36 | có | 763.494 | 8.263 | 1,3e-10 | 12 | 14 / 16 | 9,8e-01 | có |
| dev-ba831dbeb8 | tiền xử lý trên đoạn trước mốc (PF) | 720 | 30 | có | 26.185 | 2.603 | 1,1e-11 | 0 | 3 / 3 | 4,9e-13 | có |
| dev-ba831dbeb8 | tiền xử lý trên cả bản ghi (FF) | 1.441 | 36 | có | 728.823 | 5.272 | 1,2e-10 | 0 | 16 / 16 | 6,7e-13 | có |

Bản gốc cho bằng không từ 26.185 đến 763.494 trạng thái mỗi chuỗi. Bản miền log hữu hạn ở mọi trạng thái đạt được.

### 2.4 Chuỗi có khác biệt: đầu vào full của dev-3ae0a6c15a

- MAP khác ở 12 bước liên tiếp, chỉ số 752 đến 763 (mốc tiêm ở chỉ số `720`).
- Ở bước khác đầu tiên, bản gốc chọn nhánh bắt đầu từ chỉ số 40; bản miền log chọn nhánh bắt đầu từ chỉ số 240. Bản gốc đã cho nhánh thứ hai khối lượng đúng bằng 0 từ trước.
- Phân loại 12 bước: 8 bước trạng thái MAP đúng là trạng thái bị underflow; 4 bước là hệ quả trong cùng đoạn phân kỳ; 0 bước không giải thích được.
- Khối lượng của các trạng thái bị ảnh hưởng vượt `1e-12` lần đầu ở cột 750 và lên tới 0,98. Hai posterior phân kỳ (khoảng cách biến thiên toàn phần trên `1e-6`) ở 15 cột liên tiếp, 752 đến 766; khoảng cách lớn nhất 0,98.
- Điểm đổi: bản gốc 14, bản miền log 16. Bản gốc có điểm đổi tại chỉ số 755 mà bản miền log không có; bản miền log có tại 752, 760, 764 mà bản gốc không có. Mọi điểm đổi khác trùng nhau.
- Điểm đổi đầu tiên sau mốc: 35 giây sau mốc ở bản gốc, 32 giây ở bản miền log.
- Không đổi: báo động đầu (chỉ số 649, trước mốc); 3 điểm đổi trước mốc ở cả hai bản; số cửa sổ 60 giây đổi trạng thái: 0.

### 2.5 Ba chuỗi không khác

MAP và CP trùng ở mọi bước. Ở chuỗi PF của `dev-ba831dbeb8` có 11.018 trạng thái lệch quá `1e-9` vì nhánh của chúng từng rơi xuống vùng số dưới chuẩn hóa (mất chữ số có nghĩa, chưa về không); lệch log lớn nhất 0,21. Khối lượng log lớn nhất của các trạng thái đó là -69,5, quá nhỏ để chạm tới MAP.

### 2.6 Kết luận trong phạm vi đã thử

| Câu | Trả lời | Mức |
|---|---|---|
| Underflow có làm đổi MAP hoặc điểm đổi không? | Có, ở 1/4 chuỗi đã kiểm, trong một đoạn 45 giây ngay sau mốc tiêm | CT |
| Underflow có giải thích báo động trước mốc của hai ca này không? | Đã loại: báo động đầu và mọi điểm đổi trước mốc giữ nguyên ở 4/4 chuỗi | CT |
| Có đổi số của bảng baseline không? | Không. Bảng baseline giữ nguyên số đã khóa. Ở chuỗi có khác biệt, không cửa sổ 60 giây nào đổi trạng thái | — |
| Còn ca nào khác bị ảnh hưởng? | Chưa biết. Chỉ hai ca này được tính lại trong miền log | CK |

Điều kết quả này sửa trong cách dùng số cũ: phép cũ của T-033 (giữ hệ số chuẩn hóa) đúng ở các điểm đã kiểm, nhưng câu “underflow không đổi MAP” không được mở rộng ra cả chuỗi. Ở chuỗi full của dev-3ae0a6c15a nó có đổi, ở một đoạn ngắn.

Không suy ra: bản miền log phát hiện tốt hơn; số điểm đổi nhiều hơn là tốt hơn; kết quả đúng cho các ca dev còn lại.

### 2.7 Chi phí đo được

Tổng thời gian máy của bốn chuỗi ở lượt dùng để kết luận: 2427 giây (mỗi chuỗi gồm bản giữ nguyên, bản miền log, tham chiếu mở rộng). Chuỗi full: 909 và 918 giây; chuỗi PF: 301 và 299 giây. Bộ nhớ đỉnh quan sát được: 277.192.704 byte. Mỗi chuỗi lưu một file gọn; chuỗi lớn nhất 177.844 byte.

## 3. Lượt chạy và nguồn

| Lượt (trong `results/T-034/runs/`) | Nội dung | Dùng để kết luận |
|---|---|---|
| `e1-001` | E1, đủ 11 ca, ba nhánh | Có |
| `e2-fixtures-laptop-001-fail` | Ví dụ F2 thiết kế sai (không tạo được underflow) | Không; giữ làm lượt lỗi |
| `e2-fixtures-laptop-002`, `e2-fixtures-laptop-003-v3` | Ví dụ nhỏ trên laptop | Kiểm phụ |
| `e2-001` | Bốn chuỗi, một luồng tính (khác cấu hình nguồn) | Không; đối chiếu |
| `e2-determinism-001` | Phép kiểm tất định theo số luồng | Kiểm phụ |
| `e2-fixtures-ec2-002-v3-fail`, `e2-fixtures-ec2-003-v3-fail` | Ví dụ F4 hỏng vì lỗi của bản cài tham chiếu | Không; giữ làm lượt lỗi |
| `e2-fixtures-ec2-004-v3` | Ví dụ F1–F4 đạt | Có |
| `e2-002` | Hai chuỗi PF; hai chuỗi FF bị dừng ở bước giữ nguyên vì chạy quá chậm | Phần PF: có |
| `e2-003` | Hai chuỗi FF, chạy lần lượt | Có |
| `e2-used-001` | Bản gom bốn chuỗi dùng để kết luận (chép từ hai lượt trên, có kiểm mã băm) | Có |

Mã nguồn không bị sửa: bản cài theo lời văn của T-032, mã BOCPD của BARO và mọi kết quả cũ chỉ được đọc. Script của hai phép nằm ở `results/T-034/scripts/` (`e1_pattern_rule.py`, `e2_bocpd_log_v3.py`). Mã băm hai đầu của từng lượt nằm cạnh thư mục lượt.
