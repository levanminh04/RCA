# Q4: lượt mua vé 10 phút sau đợt dọn (25/11/2026, 03:21–03:31Z)

Làm đúng như T-067 bước 7, tiêu chí khai trước ở lab `tests/signals/tieu-chi.json#/buoc_7`. Lab `85ace52` trên cả ba máy.

| Bước | Kết quả | File |
|---|---|---|
| Tải | `tai_linux.py start --tag kiem-sau-don-001 --seconds 600`, mức ×1 (12 hành trình/10 s), từ `/opt/flashticket-rca` trên obs. Preflight đạt: mock VNPay sống, không phải khởi động lại. Container k6 03:21:25–03:31:27Z, thoát mã 0, không bị diệt vì thiếu bộ nhớ. 720/720 hành trình xong, 3.317 request, `http_req_failed` 0, p95 (phản hồi mong đợi) 535,6 ms. T-067: 721 hành trình, 0 lỗi, p95 562 ms | `k6-state.json`, `k6-summary.json`, `tai-get-receive.sh` |
| `GET /api/v1/me` | 3 lần từ máy tải bằng 1 token trong pool (không in): 200, 200, 200, mỗi lần 246 byte | `get-me.*` |
| Đơn và DB | Đơn COMPLETED đầu tiên trong cửa sổ: `0058ea5c-011e-44e3-b702-db8a143688e1`; số lượng 1, đúng 1 vé (`ticket_db.tbl_tickets` theo `order_item_id`), 1 lần phát vé. Cả cửa sổ: COMPLETED 144, CANCELLED 36, PENDING_PAYMENT 36 | `don-db.*` |
| Bộ kiểm tín hiệu | Cùng nội dung `tests/signals/run_remote.sh` gửi đi (tiêu chí và cặp RabbitMQ nhúng base64 + `check_purchase_journey.py`), qua `ssh.sh obs`. Cửa sổ 1795576885–1795577488, có `--don` và `--don-db-json`. **Đạt mọi mục**, kể cả "một đơn COMPLETED đúng một vé" (T-067 để `chua_kiem` mục này) | `kiem-tin-hieu.json` |
| Cảnh báo tới bộ nhận ở đường mới | `webhook.jsonl` ở `/srv/flashticket-rca/alerts/bo-nhan/` nhận 14 thông báo, có cả `firing` lẫn `resolved`: 5 thông báo trước Q4 (dòng 1–5: dừng service lúc dời 24/11 và hai lần nhắc lại), 9 thông báo trong Q4 (dòng 6–14). Đường Grafana → bộ nhận chạy thật | `canh-bao-nhan.*` |

## Chi tiết bộ kiểm (`kiem-tin-hieu.json`)

| Nhóm | Kết quả |
|---|---|
| Span server có `http.route` | Gateway, booking, event, payment: đạt |
| Span client của gateway → service | Booking, event, payment: đạt |
| Span DB | Đủ 4 DB (event, booking, payment, ticket): đạt |
| Redis | Booking, gateway: đạt |
| User + Mongo (3 trace `/me`) | Đạt |
| RabbitMQ trong cửa sổ | 6/6 cặp đạt |
| Luồng chính | Correlation qua các service đạt; một vé đạt; RabbitMQ của đơn P1–P6 đạt |
| Metric | 6/6 nhóm đạt |
| Log nối đúng span | Gateway 3.126/3.186 (98,1%; T-067 98,1%); booking 936/936; payment 1.440/1.440; ticket 432/432. Đủ 13 trường B16 ở mọi dòng |

## Hai điều thấy ở cảnh báo (không phải lỗi do dời)

1. **`t072-mat-gw` cháy từ 16:32:00Z ngày 24/11 tới 03:21:40Z ngày 25/11** (giờ Grafana ghi hết; bộ nhận nhận thông báo lúc 03:21:47,79Z).
   - Luật đo tuổi mẫu mới nhất `time() - max(timestamp(http_server_request_duration_seconds_count{service_name="api-gateway",http_route=~"booking|event|payment|ticket"}))`; cháy khi tuổi `> 60` s kéo dài `60s`, hoặc khi không có dữ liệu (`noDataState: Alerting`); đánh giá mỗi 10 s (lab `observability/grafana/provisioning/alerting/rules.yaml`).
   - Lệnh dừng ở bước 3 chạy 16:29:48–16:31:18Z, dừng **cả Collector agent lẫn các service, gồm gateway** (`sau-buoc-3/lenh-1-dung.out` dòng 1, 79; log không ghi giờ riêng từng container). Tuổi mẫu đọc lại từ Prometheus: 9,479 s lúc 16:29:40Z, 119,479 s lúc 16:31:50Z, 129,479 s lúc 16:32:00Z. Luật cháy lúc 16:32:00Z vì tuổi mẫu vượt ngưỡng đủ lâu. Dữ liệu hiện có không tách được phần do dừng gateway với phần do dừng Collector agent. `t072-mat-do` cháy cùng đợt (16:31:50Z) và tự hết 16:39:40Z (bộ nhận nhận 16:39:44,59Z).
   - Bắt đầu triển khai gateway lúc 16:38:32Z; đến 16:39:13Z script đã xác nhận health và Eureka (`sau-buoc-3/deploy.tsv` dòng 13–14: `START` rồi `END health=yes eureka=yes`). Truy vấn cùng biểu thức lúc 16:38:40Z (trong lúc triển khai), 16:39:50Z (sau mốc xác nhận) và 03:21:20Z ngày 25/11 đều rỗng (không có chuỗi mới); truy vấn lúc 03:21:45Z thấy mẫu mới có tuổi 9,667 s. Luật tiếp tục cháy, Grafana nhắc lại lúc 20:32Z và 00:32Z. **Chưa kiểm** log truy cập gateway, nên chưa khẳng định suốt khoảng này không có request nào vào 4 route; request hiếm hoặc đường đo chưa phát mẫu cũng cho cùng kết quả.
   - Grafana ghi luật hết lúc 03:21:40Z (`alerts[].endsAt`), khoảng 14,75 s sau khi k6 bắt đầu (03:21:25,254Z, `k6-state.json#/StartedAt`); bộ nhận nhận thông báo lúc 03:21:47,79Z (`nhan_webhook_utc`), khoảng 22,54 s. Nguồn: `/srv/flashticket-rca/alerts/bo-nhan/webhook.jsonl` trên obs, bản tin `resolved` lọc theo `labels.t072_uid` (đọc 28/11).
   - Trước khi dời, trong khoảng nghỉ 23/11 02:33Z → 24/11 16:10Z, bộ nhận không nhận thông báo nào: chuỗi metric cũ còn từ lượt tải trước.
   - Hệ quả: dừng gateway hoặc Collector agent, hoặc khởi động lại gateway mà chưa có tải, làm luật này cháy khi tuổi mẫu vượt 60 s quá 60 s hoặc không có dữ liệu, đúng theo cấu hình luật. Không dùng Q4 để suy tỷ lệ báo động giả.
   - Đính chính 28/11 (REVIEW-5 R3): mốc 03:21:47Z và 16:39:44Z ở bản trước là giờ bộ nhận nhận thông báo, không phải giờ luật hết.
   - Đính chính 28/11 (REVIEW-6 R4): 16:38:32Z ở bản trước là giờ bắt đầu triển khai gateway, không phải giờ gateway đã lên; kết quả rỗng lúc 16:38:40Z chưa phân biệt gateway còn đang lên với đã lên mà chưa có mẫu.
   - Đính chính 26/11 (REVIEW-3 R6, REVIEW-4 R3): bản đầu gán thời điểm bắt đầu cháy cho lúc gateway được tạo lại (16:39Z); bản sửa lần một quy nguyên nhân riêng cho việc dừng gateway. Bản này chỉ giữ cơ chế tuổi mẫu và các mốc đo được.
2. **4 luật p95 cháy trong 4–6 phút đầu lượt tải** (booking, event 03:22:50Z; payment 03:24:40Z; ticket 03:25:00Z), rồi tự hết lúc 03:26–03:29Z.
   - Ngưỡng ở `results/T-072/nguong.json`: booking 0,098 s, event 0,097 s, payment 0,184 s, ticket 0,112 s.
   - **Giả thuyết, chưa kiểm:** JVM của các service vừa khởi động lại ở bước 3 nên chạy chậm trong vài phút đầu, đẩy p95 qua ngưỡng.
   - **Trường hợp giả thuyết sai:** nguyên nhân khác, ví dụ mức nền mới khác mức nền lúc chọn ngưỡng.
   - **Phân xử được bằng:** không phải `k6-summary.json` (chỉ có p95 toàn lượt) hay p95 phía máy tải, vì bốn luật đo histogram ở gateway theo từng route trên cửa sổ trượt 5 phút, cần đủ 30 request (lab `observability/grafana/provisioning/alerting/rules.yaml`). Muốn xem cảnh báo đã hạ cho lần quan sát: đọc lại biểu thức luật và số request theo route ở hai cửa sổ có tải tương đương (dữ liệu đã lưu). Muốn quy riêng cho JVM: cần tín hiệu JVM hoặc đối chứng lạnh/ấm tương đương về tải và trạng thái phụ thuộc. Phân bố hành trình đầu lượt và thời gian xử lý hạ nguồn cũng giải thích được chênh lệch.
   - **Kết luận phụ thuộc:** trước một lượt tiêm lỗi sau khi khởi động lại service, có cần thời gian làm ấm để cảnh báo p95 không cháy sẵn hay không.
