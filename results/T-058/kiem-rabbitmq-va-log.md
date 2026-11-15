# T-058 — RabbitMQ (queue, vhost) và log nối span (11/11/2026, Claude)

Tiếp `kiem-span-redis.md`. Minh yêu cầu tra tiếp các chỗ thiếu của trace (chat 11/11: "Có, tra tiếp").

## 1. RabbitMQ: vhost đã có, tên queue vẫn thiếu

**Trước khi sửa** (Tempo, lượt hủy sự kiện lúc 20:38Z ngày 10/11):
- Span gửi `business.ex publish` (event-service, scope `io.opentelemetry.rabbitmq-2.7`, kind PRODUCER): có `messaging.destination.name=business.ex`, `messaging.rabbitmq.destination.routing_key=event.cancelled.v1`; không có vhost, không có message ID.
- Span nhận `event.cancelled.v1 process` (booking, payment, ticket; scope `io.opentelemetry.spring-rabbit-1.0`, kind CONSUMER): có `messaging.destination.name=event.cancelled.v1` (đây là **routing key**, không phải tên queue), có `messaging.message.id`; không có vhost, không có tên queue.

**Thí nghiệm** (01:20–01:23Z ngày 11/11): thêm `OTEL_INSTRUMENTATION_RABBITMQ_EXPERIMENTAL_SPAN_ATTRIBUTES=true` vào env của event, booking, payment, ticket; tạo lại container; chạy lại `traffic-probe.py` của lượt đêm (tạo một sự kiện thử thứ hai rồi gọi API hủy, trả 200). RabbitMQ ghi thêm 1 publish, 3 deliver, 3 ack.

**Sau khi bật:**
- Span gửi có thêm `messaging.rabbitmq.vhost.name=/`, `messaging.rabbitmq.cluster.name=rabbit@rabbitmq`, `rabbitmq.command=basic.publish`, `rabbitmq.delivery_mode=2`.
- Các span lệnh mức thấp (`basic.ack`, `basic.consume`, `queue.declare`, `basic.qos`, `confirm.select`) có thêm vhost và `rabbitmq.command`.
- Span nhận `event.cancelled.v1 process` của Spring **không đổi**: vẫn không có vhost, vẫn không có tên queue.
- Không span nào có tên queue: TraceQL `{span.rabbitmq.queue != nil}` trả 0 trace; xem trực tiếp `basic.consume` và `queue.declare` cũng không có.

**Hệ quả cho đồ thị:** từ trace dựng được cạnh `event-service → business.ex` (theo routing key) và cạnh tới từng service nhận (cùng message ID, có span cha). Không dựng được nút queue. Bảng binding của nhóm (`deploy/rabbitmq/definitions.json`: 1 vhost `/`, 30 queue, 30 binding) cho biết `event.cancelled.v1` đi tới đúng 3 queue `booking.event-cancelled.q`, `payment.event-cancelled.q`, `ticket.event-cancelled.q`, và mỗi routing key khác của `business.ex` đi tới đúng 1 queue. Vì vậy **tên queue suy được chính xác từ (routing key, service nhận) qua bảng binding tĩnh**, với điều kiện bảng binding khớp runtime (chưa kiểm bằng Management API).

**Cách có tên queue trực tiếp trong span** (chưa làm, cần sửa code hoặc cấu hình hệ thống): đặt thuộc tính queue trong listener, hoặc thêm cầu nối Micrometer Tracing để observation của Spring AMQP sinh span có thông tin listener. Đây là việc của repo FlashTicket.

**Giữ lại trên `exp-app`:** cờ thử nghiệm vẫn bật ở 4 service (có thêm vhost, cluster, lệnh, không mất gì). Env cũ lưu cạnh đó, đuôi `.truoc-thu-rabbit-20261111`.

## 2. Log nối span: cấu hình đúng, nhưng service hầu như không ghi log trong request

Đếm trong Loki, khung có tải 21:15–22:30Z ngày 10/11 (giới hạn 5000 dòng mỗi service):

| Service | Dòng log | Có `traceId` và `spanId` | Đối chiếu một mẫu với Tempo |
|---|---:|---:|---|
| api-gateway | 504 | 456 | trace có, `spanId` khớp |
| booking-service | 184 | 9 | trace có, `spanId` khớp |
| discovery-server | 163 | 30 | trace có, `spanId` khớp |
| event-service | 92 | 3 | trace có, `spanId` khớp |
| payment-service | 102 | 0 | không có mẫu |
| ticket-service | 48 | 0 | không có mẫu |
| user-service | 48 | 0 | không có mẫu |
| keycloak | 35 | 0 (log không phải JSON) | không có mẫu |

**Vì sao user, ticket, payment không có dòng nào nối span:**
- Cấu hình log của ba service này **có** `traceId` và `spanId` trong danh sách trường được phép (`logging.structured.json.include` trong `application.yaml`; đã kiểm).
- Ba service hầu như **không ghi log nào trong lúc xử lý request**. Gọi thử 6 API tới ticket, user, payment (403, 404, 500, 200) lúc 01:25Z: trong 5 phút sau, Loki có 1 dòng của user-service (dòng Eureka định kỳ), 0 dòng của ticket, payment, event, booking.
- Các dòng log hiện có là log khởi động, định kỳ, hoặc lỗi nền, nên không có span đang chạy để nối.

**Kết luận:** việc nối log với span hoạt động đúng ở mọi service có ghi log trong request (4 service, `spanId` khớp Tempo). Với user, ticket, payment thì chưa kiểm được vì không có dòng log nào trong request; cấu hình cho thấy sẽ nối được, nhưng đó là suy luận. **Vấn đề thật là log nghèo**: chỉ gateway ghi một dòng cho mỗi request; các service nghiệp vụ không ghi. Với RCA, kênh log của các service này gần như trống trong cửa sổ sự cố, đúng như đã thấy ở ca tạm dừng đêm qua (event-service có 234 dòng log trong cửa sổ lỗi nhưng gần như không có trong cửa sổ bình thường).

**Cách làm giàu log** (cần sửa hệ thống, việc của repo FlashTicket, chưa làm): mỗi service ghi một dòng có cấu trúc cho mỗi request hoặc mỗi message xử lý (tương tự gateway, các trường `eventName`, `httpStatus`, `durationMs`, `outcome` đã có trong danh sách cho phép). Keycloak ghi log dạng văn bản; muốn nối span phải bật log JSON của Keycloak.

## 3. Tổng hợp độ đầy đủ của trace sau hai lượt sửa

| Loại | Trạng thái |
|---|---|
| HTTP giữa service, PostgreSQL, MongoDB | Có |
| Redis | Có từ 01:13Z ngày 11/11 (`kiem-span-redis.md`) |
| RabbitMQ gửi và nhận, nối cùng trace | Có |
| RabbitMQ vhost | Có ở span gửi và span lệnh, không có ở span nhận của Spring |
| RabbitMQ tên queue | Không có; suy được từ bảng binding tĩnh |
| Log nối span | Đúng ở 4 service có log trong request; 3 service không có log trong request |

## Đính chính 11/11/2026 (Claude, sau khi đọc code gateway)

- Mục 2 ghi "chỉ gateway ghi một dòng cho mỗi request" là **sai**. `CorrelationIdFilter` của gateway chỉ ghi log khi response là 4xx hoặc 5xx (điều kiện `status.isError()`); request thành công không có dòng log. Vậy 456 dòng có `traceId` của gateway trong khung 21:15–22:30Z là các request bị từ chối hoặc lỗi, không phải toàn bộ request. Kết luận "log nghèo" vẫn đúng và nặng hơn: không service nào ghi log cho request thành công.
- Cùng ngày, trong đời container hiện tại, payment, ticket, user có 7, 4, 3 dòng mang `traceId` (khởi tạo servlet ở request đầu, cảnh báo validator, một dòng tạo thanh toán, một dòng `ticket.request.failed`). Số 0 dòng ở mục 2 là của khung 21:15–22:30Z, không mâu thuẫn.
- Chi tiết từng service: `docs/techstack/VIEC-CHO-QUYET-VA-LAM.md` mục 3; sổ khắc phục KP-15, KP-16.

## Đính chính 2 — 11/11/2026 (Claude, sau KP-19)

- Phép thử lúc 01:25Z ở mục 2 ("gọi thử 6 API ... 0 dòng của ticket, payment, event, booking") đọc Loki khi đường thu log của bốn service này đã đứt. Nguyên nhân: Collector ghim ID container cũ, còn container đã được tạo lại lúc 01:13–01:20Z để bật cấu hình Redis, RabbitMQ (sổ khắc phục KP-19). Kết quả 0 dòng của bốn service đó không dùng được.
- Sau khi sửa đường thu và lấy bù log (09:15Z), khung 01:24–01:31Z cho kết quả: ticket có 4 dòng mang `traceId` lúc 01:25:46Z (3 dòng khởi tạo servlet ở request đầu, 1 dòng `ticket.request.failed` mức ERROR); payment, user, event, booking chỉ có dòng Eureka định kỳ.
- Kết luận của mục 2 sửa lại: payment, user không ghi log cho các request thử; ticket chỉ ghi khi request lỗi. Kết luận "log nghèo" vẫn đúng. Khung 21:15–22:30Z ngày 10/11 có trước lần tạo lại container, nên các số đếm của khung đó không bị ảnh hưởng.
- Chi tiết: `so-khac-phuc.md` KP-19 (bổ sung), KP-20.
