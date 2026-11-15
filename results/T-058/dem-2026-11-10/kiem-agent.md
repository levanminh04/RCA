# Kiểm agent T-058 — C1 đạt một phần

FACT, mốc kiểm 10/11/2026 20:37Z. Không ghi chặng 4 đạt đầy đủ. Agent 2.33.1 đã chạy trên 8 JVM ARM, gồm 7 Spring Boot 4.1.1 và Keycloak 26.8.0. Luồng API trước và sau khi gắn agent đều chạy tới URL thanh toán giả. Không kiểm thanh toán thật, phát vé sau thanh toán hoặc gửi email.

## 1. Bằng chứng đã có

| Điều kiện TECHSTACK §4.1 | Kết quả | Nguồn |
|---|---|---|
| HTTP span có kind, route; gateway → booking | Có SERVER gateway, CLIENT gateway, SERVER booking. Route gateway là tên route `booking`; booking có mẫu `/api/v1/events/{eventId}/availability` | `telemetry-app-after-probe.json#/request_traces`; `grafana-evidence.json#/grafana_proxies/traces` |
| JDBC PostgreSQL | Có span CLIENT JDBC, thao tác SELECT/INSERT/UPDATE và địa chỉ PostgreSQL | `telemetry-app-after-probe.json#/db_systems/postgresql`; `#/request_traces` |
| Redis span | Chưa đạt: không thấy trong file thu tại chỗ hoặc Tempo, dù Redis thực sự nhận GET/SET | §2 dưới đây |
| RabbitMQ PRODUCER/CONSUMER | Có sau khi tạo đúng lưu lượng: một PRODUCER và ba CONSUMER, chung trace, consumer có parent là producer | `broker-span-evidence.json`; `traffic-probe.json` |
| Log JSON nối span | Đã có ví dụ nối bằng cả traceId và spanId ở gateway, booking, event, payment, discovery. Chưa xác minh đầy đủ cho user/ticket; Keycloak log dạng khác | `telemetry-app-after-probe.json#/logs_joined_to_span`; `#/joined_log_examples` |
| Metric qua Grafana | Grafana proxy Prometheus trả chuỗi HTTP metric cho đủ 8 JVM | `grafana-evidence.json#/grafana_proxies/metrics` |
| Sức khỏe và restart ổn định | API smoke thành công và có sáu client Eureka UP, nhưng C3 không ổn định: booking OOM cgroup ở cả pha rảnh và tải, tự restart. Đã tăng giới hạn riêng sau C3; đang kiểm cửa sổ mới theo STEER #4 | `smoke-api-baseline.json`, `smoke-api-agent.json`, `unplanned-oom.json`, `kiem-bo-nho.md`, `jvm-memory-fix.json` |

API health của gateway/payment trả 403 với tài khoản thử, do chính sách của ứng dụng. Không đổi chính sách để lấy health. Dùng Eureka và API nghiệp vụ làm bằng chứng tương ứng; không gọi HTTP 403 là health UP.

## 2. Phân xử thiếu Redis theo STEER #2

FACT: probe `INFO commandstats` trước/sau một lượt catalog → availability → tạo đơn → replay → payment URL giả → hủy hold ghi GET `57 → 75`, SET `8 → 10`; không có lệnh bị từ chối hoặc lỗi trong các bộ đếm này. Vì vậy giả thuyết “luồng thử không gọi Redis” không giải thích được việc thiếu span. Probe đọc riêng trước đó cũng tăng GET `49 → 57`, SET `7 → 8`.

FACT: file JAR booking chứa `lettuce-core-7.5.2.RELEASE` và `spring-data-redis-4.1.1`. Code `AvailabilityCacheService` gọi `RedisService`, rồi `StringRedisTemplate`. Đã bật debug agent cho đúng booking trong một lượt chuẩn bị, đọc log qua bộ lọc bí mật, rồi tắt trước phép đo tài nguyên. Log ghi nhận agent transform các lớp `RedisClient`, `DefaultEndpoint`, `CommandHandler`, `AsyncCommand`, `CommandEncoder` và các lớp Lettuce khác. Không có cấu hình tắt Lettuce trong env do lượt đêm tạo. Log chẩn đoán nằm ở `/home/ubuntu/t058/lettuce-agent-debug-redacted.log` trên `exp-app`.

FACT: tới mốc báo cáo, thống kê file OTLP tại chỗ có PostgreSQL và MongoDB, không có `db.system`/`db.system.name` Redis; danh sách instrumentation trong span chưa có scope Lettuce. Tempo trả 0 trace với truy vấn dưới đây. Processor tại chỗ chỉ lọc health check và bỏ query string URL, không có luật lọc Redis.

OPEN: chưa xác định bước nào không sinh hoặc không giữ span Redis. Khả năng còn lại gồm thay đổi API/hook của Lettuce 7.5.2, tích hợp tracing của thư viện hoặc cơ chế suppression trong agent. “Đã transform lớp” chưa chứng minh command instrumenter tạo span. Chưa có bằng chứng đủ để quy lỗi chung cho Spring Boot 4.1.1. Cần một probe tối thiểu Lettuce cùng phiên bản và theo dõi command instrumenter, hoặc thử starter/agent khác trong task được duyệt. Lượt đêm giữ đúng agent 2.33.1 và không sửa pom/source để ép đủ tiêu chí. C1 và cạnh Redis của R-03 còn mở.

## 3. Phân xử RabbitMQ theo STEER #2

FACT: luồng tạo đơn/giữ chỗ/tạo URL thanh toán giả/hủy hold không tăng bộ đếm publish/deliver của RabbitMQ. SQL seed đã đặt sẵn snapshot, còn luồng thử dừng trước VNPay; không mặc nhiên coi việc chạy luồng này là đã kiểm trao đổi message.

Đã tạo một event synthetic thứ hai bằng cùng cấu trúc SQL, tách khỏi event dùng tải. Sau đó gọi API quản trị hủy event bằng token ADMIN hợp lệ. API trả 200, trạng thái `CANCELLED`. Không gửi message giả vào broker để thay producer nghiệp vụ.

FACT: sau API, Management API ghi `publish=1`, `confirm=1`, `deliver=3`, `ack=3`, `redeliver=0`. OTLP ghi một span `business.ex publish` kind PRODUCER của event-service và ba span CONSUMER của booking/payment/ticket. Ba consumer có chung message ID và parentSpanId trỏ tới span producer. Điều này hỗ trợ truyền context của đúng luồng fan-out đã thử. Nó không kiểm đủ mọi message, retry hay ranh giới outbox.

Phần R-04 còn thiếu: consumer đang ghi đích `event.cancelled.v1`, chưa có tên queue riêng và vhost trong các span mẫu; producer có exchange và routing key nhưng không có message ID trong span mẫu. Không bổ sung các trường chưa ghi bằng suy đoán.

## 4. Truy vấn đã chạy

Thực hiện qua Tempo HTTP API `GET /api/search`, cửa sổ một giờ kết thúc khoảng 20:36:58Z, `limit=1000`. Lệnh trong `out/grafana-evidence.py` dùng URL encoding; dữ liệu trả về nằm trong `grafana-evidence.json#/traceql`.

```traceql
{ span.db.system = "redis" || span.db.system.name = "redis" }
{ span.messaging.system = "rabbitmq" }
{ kind = producer || kind = consumer }
{ span.db.system = "postgresql" || span.db.system.name = "postgresql" }
```

Số trace trả về lần lượt: 0, 44, 1, 1000. PostgreSQL chạm giới hạn nên 1000 không phải tổng số trace. Số trace RabbitMQ không phải số message; nó còn gồm thao tác điều khiển kết nối. Số span PRODUCER/CONSUMER từ file thu là 1 và 3.

Grafana proxy đã trả đúng trace availability gồm 18 span, 10 dòng log booking và metric cho 8 JVM. Dashboard `/d/t058-flashticket/flashticket-t-058` đã tạo qua API. Chưa kiểm bố cục bằng trình duyệt; không lấy việc tạo dashboard thay cho kiểm dữ liệu.

## 5. Giới hạn kết luận

C1 đạt một phần. R-01 được kiểm trên các đường API mẫu, chưa phủ mọi cạnh HTTP. R-04 có bằng chứng fan-out cụ thể, còn thiếu queue/vhost và độ phủ toàn bộ message. Chặng 4 có đủ ba loại tín hiệu để tiếp tục kiểm khả thi và đo tài nguyên, chưa đủ để xác nhận toàn bộ R-01–R-10. Không có kết luận về hiệu quả M1.
