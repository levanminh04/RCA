# T-072 — Đề xuất mục WHY cho biểu thức luật cảnh báo W4 (chờ Minh duyệt; chưa ghi `docs/WHY.md`)

Trạng thái: **đề xuất, trước khi dùng** (trước E2). Phiên điều phối gom trình Minh (I6, R2). Mỗi mục tách quan sát (đã kiểm, có nguồn), suy luận và phần chưa kiểm. File máy đọc: `bieu-thuc.json` (`T072-bieu-thuc-1`), `quy-tac-gom.json` (`T072-gom-1`); khảo sát ở `khao-sat/`.

## WHY-a. "p95 theo route ở gateway" = theo **mã route Spring Cloud Gateway**

- **Chọn gì:** p95 và tỷ lệ 5xx tính trên histogram `http_server_request_duration_seconds` của `service_name="api-gateway"`, gom theo nhãn `http_route`. Nhãn này là **id route của gateway** (`booking`, `event`, `payment`, `ticket`, …), không phải từng đường dẫn API. Một route gộp nhiều API và nhiều method (ví dụ `booking` gồm GET availability, POST orders, GET poll đơn).
- **Vì sao:** đây là mức chi tiết duy nhất của histogram ở gateway. Quan sát: 9–17 tổ hợp (route, method, mã) ở 5 thời điểm 18–20/11; giá trị `http_route` chỉ gồm 5 id route có tải, `user`, `/actuator/health/{*path}` và chuỗi không nhãn (401) (`khao-sat/khao-sat-1.out`, mục `nhan-route`). Id route khớp `application.yaml` của gateway ở FlashTicket `36a3725d`.
- **Phương án đã xét:** (1) theo đường dẫn API: không có trong metric gateway; muốn có phải lấy từ span (Tempo) hoặc histogram phía service, không phải "ở gateway". (2) Tách thêm theo method trong route: số request mỗi ô nhỏ hơn (POST payment ≈ 70/5 phút ở ×1), p95 dao động mạnh hơn; chưa có lý do cần. (3) Một p95 chung toàn gateway: route nhiều request (`event`, `booking`) che route ít request (`payment`, `ticket`).
- **Giới hạn:** API chậm trong một route đông (ví dụ chỉ POST orders chậm) có thể không đẩy p95 của cả route `booking` vượt ngưỡng. Chưa đo được độ lớn của che lấp này trước E2/E4.
- **Kết luận phụ thuộc:** mọi số báo động giả và phát hiện của W4; t̂ của chế độ (b) (W5).

## WHY-b. Tập route có luật: `booking`, `event`, `payment`, `ticket`

- **Chọn gì:** luật p95 và luật lỗi chỉ cho bốn route này.
- **Vì sao:** bộ tải `purchase-journey.js` (lab `407b4f5`) chỉ gọi bốn route này. Ngưỡng phải chọn từ dữ liệu E2, nên route không có tải thì không có căn cứ ngưỡng. Quan sát: `user` tăng 0 request/5 phút ở cả 5 thời điểm khảo sát.
- **Không phủ:** `user`, `event-images`, `payment-vnpay-callbacks`, request không khớp route. Lỗi chỉ ở các route này không mở sự cố qua p95/lỗi; liveness của `user-service` vẫn có.

## WHY-c. Cửa sổ 5 phút và chặn khi < 30 request

- **Chọn gì:** `rate`/`increase` trên `[5m]`; luật p95 và lỗi chỉ có giá trị khi route có ≥ 30 request trong 5 phút.
- **Vì sao:** `payment`, `ticket` có ≈ 70 request/5 phút ở ×1 (≈ 14/phút) (`khao-sat/kiem-xuat-1.jsonl`, `phu/tong-*`). Cửa sổ 1 phút chỉ có ≈ 14 mẫu, p95 gần bằng max, dễ báo giả. Chặn 30 request: giữa hai lượt (không tải) tổng = 0 thì không tính p95 (tránh NaN) và luật về NoData → OK; ở ×1 các route đều ≥ 70.
- **Phương án đã xét:** 1m (quá ồn ở route ít request), 10m (trễ phát hiện dài, vẫn cháy lâu sau khi hết lỗi).
- **Đánh đổi:** tín hiệu còn chứa lỗi tới 5 phút sau khi lỗi dừng → khoảng cháy dài; gom sự cố dùng khoảng ghép 300 s cho khớp (`quy-tac-gom.json`). Lỗi làm lưu lượng một route tụt dưới 30/5 phút sẽ làm luật p95/lỗi của route đó im (quan sát: `ticket` tụt về 0 khi PAUSE-PAYMENT, vì hành trình dừng ở bước thanh toán). Liveness và luật của route khác vẫn chạy.

## WHY-d. Lỗi = mã 5xx; cần ≥ 3 lỗi 5xx trong 5 phút

- **Chọn gì:** tỷ lệ lỗi = số request 5xx / tổng request của route trong 5 phút; luật chỉ được kích hoạt khi có ≥ 3 lỗi 5xx. Không tính 401, 409, 429.
- **Vì sao:** 5xx là lỗi phía máy chủ (gồm 503 khi circuit breaker mở, 504 timeout của gateway); quan sát được ở các ca HTTP5-EVENT, PAUSE-PAYMENT (`khao-sat-1.out`). 409 (booking, xung đột/hết vé) và 401 là phản hồi nghiệp vụ/xác thực. 429 do bộ giới hạn tốc độ theo địa chỉ nguồn; toàn bộ tải k6 đi từ một máy, nên 429 phụ thuộc mức tải, không phải lỗi thành phần; T-071 theo dõi 429 riêng trong tiêu chí giờ khỏe. Ngưỡng tối thiểu 3 lỗi: với 70 request, một lỗi lẻ đã là 1,4%; ba lỗi tránh mở sự cố vì một request hỏng.
- **Phương án đã xét:** tính cả 429 (loại, lý do trên); không đặt số lỗi tối thiểu (ngưỡng tỷ lệ chọn từ E2 có thể bằng 0 vì giờ khỏe thường không có 5xx, khi đó một lỗi là đủ mở sự cố).
- **Giới hạn [đã biết từ cách Prometheus tính]:** tổ hợp (route, mã 5xx) xuất hiện lần đầu sinh chuỗi mới với giá trị đã > 0; `increase` không thấy phần trước mẫu đầu. Lỗi kéo dài vẫn thấy từ mẫu thứ hai (10 s sau). Số 3 là tham số khai trước; Minh có thể đổi **trước** E2.

## WHY-e. Liveness ba trạng thái theo lần dò mới nhất, tuổi tối đa 60 s

- **Chọn gì:** tại lần đánh giá t, với mỗi đích dò: lần dò mới nhất trong 5 phút là mẫu mới nhất của `httpcheck_error` (lỗi) hoặc của `httpcheck_status` có nhãn `http_status_code` (có phản hồi, mọi mã). Dò tốt nếu lần mới nhất là phản hồi và tuổi ≤ 60 s; dò lỗi nếu là lỗi và tuổi ≤ 60 s; thiếu lần dò nếu không có lần nào tuổi ≤ 60 s. Luật `t072-live` cháy khi dò lỗi liên tục 20 s; thiếu lần dò thuộc luật mất quan sát `t072-mat-do`, không thuộc lớp hệ thống.
- **Vì sao:** cùng ngữ nghĩa "lần dò mới nhất" với WHY-99 (tránh lỗi cũ còn trong lookback giữ trạng thái chết). Quan sát ở PAUSE-PAYMENT 19/11 (`khao-sat-2.out`, `khao-sat-3.out`): khi đầu dò lỗi, receiver vẫn ghi 5 chuỗi `httpcheck_status` giá trị 0 **không có** `http_status_code`, nên phải lọc `http_status_code!=""`; lỗi được ghi mỗi 30 s và các đích khác cũng chỉ được dò mỗi ≈ 30 s trong lúc treo; phản hồi trở lại ở +576 s thì biểu thức về 0 ngay. 60 s ≥ hai nhịp 30 s. `timestamp()` trên selector trả đúng giờ mẫu (đã kiểm: `ts-sel`, `ts-ok`).
- **Khác WHY-99:** thêm tuổi tối đa 60 s (WHY-99 không có trạng thái "thiếu"). Kênh `live-down` của M1 không đổi.
- **Phương án đã xét:** `max_over_time(httpcheck_error[15s])` (WHY-99 đã loại); `for` = 0 (một lần dò hỏng lẻ mở sự cố); `for` = 60 s (có thể lỡ RECREATE-PAY, lỗi kéo dài ≈ 50 s theo WHY-99).
- **Chưa kiểm:** độ trễ nạp mẫu của Prometheus lúc Grafana đánh giá (mẫu chưa tới thì tuổi lớn hơn lúc xuất lại); phân xử ở E3 bằng so trạng thái luật với bộ chấm offline.

## WHY-f. Nhịp đánh giá 10 s; `for` 60 s (p95, lỗi), 20 s (liveness)

- **Chọn gì:** một nhóm luật, `interval` 10 s; `for` như trên; `keep_firing_for` 0.
- **Vì sao:** Grafana chỉ nhận khoảng đánh giá là bội của 10 s [theo tài liệu Grafana, chưa kiểm trên bản đang chạy]; 10 s bằng nhịp mẫu histogram (đo: 60 mẫu/10 phút, `mau-10m`) và nhịp dò. Mỗi truy vấn luật mất ≤ 0,03 s trên Prometheus (đo bằng query_range 10 phút, `kiem-xuat-1.jsonl` trường `dt`), nên tải thêm lên Prometheus nhỏ. `for` 60 s: một bước nhảy p95 kéo dài dưới 1 phút không mở sự cố.
- **Kết luận phụ thuộc:** độ trễ phát hiện (thuộc W6–W7), số báo động giả.

## WHY-g. Gom sự cố: ghép khi cách nhau ≤ 300 s; quy về phút chứa t̂

- Nội dung ở `quy-tac-gom.json`. Lý do 300 s: bằng cửa sổ rate và nửa cửa sổ dữ liệu RCA. Sự cố vắt qua biên đếm một lần theo phút bắt đầu; bắt đầu trong biên thì không vào tử số; đang cháy lúc bắt đầu khoảng thì không đếm. Ngưỡng R5 (≤ 1 sự cố / 6 giờ khỏe ×1) vẫn **chờ Minh**.
