# Bộ tiêm lỗi T-062 cho 7 ô phát triển (D1)

Công cụ: `scripts/inj.py` (chạy trên exp-app, `~/inj.py start|stop|probe <Ô>`), topology `scripts/d1-topology.sh`. Cường độ chọn **trước** D2, cố định cho E1. Đầu dò (`probe`) chỉ ghi vào sổ `so.jsonl`, không vào telemetry/M1.

| Ô (T-059) | Can thiệp | Cường độ | Đầu dò độc lập | Lệch so với T-059 |
|---|---|---|---|---|
| EVENT-DB-LAT | Toxiproxy `event-jdbc` (127.0.0.1:15433→5432), toxic latency chiều downstream | +30 ms mỗi phản hồi DB (D2: 200 ms làm rơi lượt k6, hạ xuống) | toxic đang bật; RTT SSLRequest PostgreSQL qua proxy so với trực tiếp; số kết nối JVM tới 15433 | Không có đầu dò Hikari/SQL server riêng (chưa làm) |
| REDIS-BOOK | Toxiproxy `booking-redis` (16379→6379), latency downstream | +200 ms | Redis PING qua proxy so với trực tiếp; kết nối JVM tới 16379 | **Hỗn hợp tải cố định không có GET availability** (route chính của ô). Nếu D2 không thấy lệnh Redis của Booking dưới tải thì ô không xác nhận được. |
| HTTP5-EVENT | Hook `rca-test` Event `http.error` trên `GET /api/v1/events/{id}` với event fixture | mọi request đích | audit `http.error.executed` (thư mục audit riêng) | — |
| SLOW-BOOK | Hook `rca-test` Booking `http.delay` trên `GET /api/v1/orders/{id}`, đúng chủ đơn | +1000 ms | audit `http.delay.started/finished` | Không có mốc đo pool/JDBC riêng ngoài span |
| NET-GW-BOOK | Booking đăng ký Eureka cổng 18082 = Toxiproxy `gateway-booking-http` → 8082; chỉ Gateway (lb://) đi qua; latency downstream | +300 ms | health Booking qua proxy so với trực tiếp; kết nối tới 18082 | Thay netem bằng Toxiproxy (theo hướng Minh đồng ý 12/11); proxy là tầng TCP giữa hai service, không phải egress namespace |
| CPU-BOOK | 2 vòng lặp bận chạy trong container Booking (`docker exec`, cùng cgroup), Booking quota CPU cố định 1.0 ở mọi pha | 2 luồng / quota 1 CPU | `cpu.stat` (nr_throttled, throttled_usec), `cpu.pressure` của cgroup Booking; số tiến trình đốt | Không dùng Pumba; quota 1.0 áp cả nền (topology cố định) |
| FLASH-HEALTHY | Không can thiệp hệ thống; k6 `ramping-arrival-rate` 5→15 req/s trong pha giữa (`chay/k6/workload-t062-flash.js`) | ×3 nhịp | k6 dropped_iterations, 429/5xx theo route | Không có hồ sơ ngưỡng khỏe đã khóa (T-059 OPEN) → chỉ khám phá |

Ca bình thường (`BINH-THUONG`): không can thiệp, `t` = mốc giữa chu kỳ.

Điều kiện nền chung đã biết (không do tiêm): route `GET /api/v1/orders/{id}/tickets` (10% hỗn hợp) luôn trả 500 vì `GlobalExceptionHandler` của Ticket đứng trước `TicketApiExceptionHandler` nên 404 "chưa có phát vé" thành 500 (lỗi có sẵn trên `main`, cũng thấy ở T-058). Không sửa trong lượt này (chờ Minh).
