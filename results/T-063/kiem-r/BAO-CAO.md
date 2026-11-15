# T-063 bước 6 — Bộ kiểm R trên tải mua vé (lượt 1, 13/11/2026 02:20Z)

**Gói kiểm:** `krb4a3d5` — tạo bằng `stage-m1.py` ghim T-058 cho t = 1794524225 (12/11 22:57:05Z), giữa lượt tải `l1r20261112v2a` của L1 (22:52–23:02Z, k6 v2 không gửi `traceparent`). Chỉ để kiểm dữ liệu, **không** chạy M1, không thuộc tập chọn. Gói `krb4a3d5/t063-kr-krb4a3d5.tgz` (sha256 `20a1d0ce…`). Cửa sổ nằm **trước** bảo trì `exp-app` lượt 1 (TD-04..08, 23:26–23:41Z).

**Kết quả** (`results/T-062/kiem-du-lieu/kiem-r.py` không sửa → [`krb4a3d5/kiem-r.json`](krb4a3d5/kiem-r.json)):

| R | Kết quả | Số đo chính | Ghi chú |
|---|---|---|---|
| R-01 | THIẾU | 153.612/156.734 span CLIENT có đích | 3.122 thiếu đều là thao tác điều khiển AMQP (`basic.ack`, `Channel.waitForConfirms`, scope `rabbitmq-2.7`) của payment/booking/ticket — giới hạn của instrumentation; đầu bị gọi suy được là `broker` theo scope (adapter M1-FT) |
| R-02 | ĐẠT | 12.920 SERVER có `http.route`, 0 tên chứa UUID | |
| R-03 | ĐẠT | 147.014 span DB có hệ/namespace/đích | |
| R-04 | **ĐẠT** (lần đầu) | 1.561 PRODUCER, 1.561 CONSUMER, đủ queue và exchange/routing | `consumer_co_link` 0: consumer là con của producer qua header (không dùng span link) |
| R-05 | MỘT PHẦN | host có ở cả trace/log/metric | `service.instance.id` của log (`<svc>-1`, do Collector) ≠ của trace (UUID của agent); metric dịch vụ không mang instance id. Không ảnh hưởng thứ hạng M1 (theo service); ghi vào B16 bản 2 (A8) |
| R-06 | ĐẠT | 11.782/11.782 log B16 nối được span | |
| R-07 | CHƯA KIỂM | — | tổng hợp ở hồ sơ đóng băng |
| R-08 | ĐẠT | 5.601/5.601 request gateway có span SERVER cùng trace | |
| R-09 | **0 span mồ côi** | 23.504 span gốc | so T-062 tải đọc: mồ côi Booking ~10/ca do lọc health + đầu dò |

**Span gốc** ([`phan_loai_kr.py`](phan_loai_kr.py) → [`krb4a3d5/phan-loai-goc.json`](krb4a3d5/phan-loai-goc.json)): CONSUMER gốc 0 (ngữ cảnh truyền qua RabbitMQ đúng); Payment 288 điểm vào HTTP (callback VNPay giả gọi thẳng `127.0.0.1:8083`); mới: `basic.ack` của Booking làm gốc 288 lần trên luồng `RabbitListenerEndpointContainer` (ack sau khi span consumer đóng — hạ tầng thư viện, nhóm như H6a); Keycloak 3.204 SQL gốc (trước bảo trì; sau TD-08 đã bọc — kiểm lại trên gói sau bảo trì).

**Còn phải làm:** chạy lại trên một gói sau bảo trì (khi L1b chạy được lượt 5 phút — L1b đang chờ hạn mức Codex hồi 03:08Z) để xác nhận TD-04..08 không làm hỏng R-04/R-06/R-08/R-09 và gốc Keycloak đã bọc.
