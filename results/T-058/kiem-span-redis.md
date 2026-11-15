# T-058 — Vì sao thiếu span Redis, và cách sửa (11/11/2026, Claude)

Tiếp điểm OPEN của `dem-2026-11-10/kiem-agent.md` §2. Minh yêu cầu tra nguyên nhân (chat 11/11).

## Kết luận

Trong điều kiện Spring Boot 4.1.1 có `spring-boot-data-redis` và agent OpenTelemetry 2.33.1, lớp tự cấu hình `LettuceObservationAutoConfiguration` của Spring Boot làm mất span Redis của agent. Khi loại lớp này bằng một biến môi trường, span Redis xuất hiện và nối đúng vào trace của request. Không sửa code, không đổi image.

Phần đã xác nhận bằng thí nghiệm: **loại lớp đó thì có span; không loại thì không có**. Phần là suy luận, chưa đọc mã để xác nhận: cơ chế bên trong (Spring đặt bộ tracing kiểu Micrometer của Lettuce lên `ClientResources`, thay bộ tracing mà agent gắn; ứng dụng không có cầu nối Micrometer Tracing nên không span nào được sinh).

## Bằng chứng

1. **Trước khi sửa** (lượt đêm): Redis nhận lệnh thật (`INFO commandstats`: GET 57→75, SET 8→10), agent đã biến đổi các lớp Lettuce, Tempo trả 0 trace với `{span.db.system="redis" || span.db.system.name="redis"}`.
2. **JAR của booking-service** (đọc bằng `zipfile` trên `exp-app`): có `spring-boot-data-redis-4.1.1.jar` chứa `org/springframework/boot/data/redis/autoconfigure/observation/LettuceObservationAutoConfiguration.class`, được liệt kê trong `AutoConfiguration.imports`; có `lettuce-core-7.5.2.RELEASE.jar` chứa `io/lettuce/core/tracing/MicrometerTracing.class`; có `micrometer-observation-1.17.1.jar`; **không có** thư viện `micrometer-tracing`. Agent có module `lettuce/v5_1`.
3. **Thí nghiệm** (01:13Z ngày 11/11, chỉ đổi một biến trên booking-service rồi tạo lại container):

   ```text
   SPRING_AUTOCONFIGURE_EXCLUDE=org.springframework.boot.data.redis.autoconfigure.observation.LettuceObservationAutoConfiguration
   ```

   Sau đó gọi `GET /api/v1/events/<id>/availability` qua gateway. Tempo trả trace có span Redis của booking-service, ví dụ một trace 5 span qua `api-gateway` và `booking-service`, trong đó:

   ```text
   scope io.opentelemetry.lettuce-5.1, name GET, kind CLIENT, có span cha
   db.system=redis, db.operation=GET, server.address=127.0.0.1, server.port=6379
   db.statement=GET flash-ticket:dev:booking:availability:v2:<eventId>:generation
   ```

   Lệnh xác thực hiện là `HELLO 3 AUTH ? ?`: mật khẩu đã được agent che.
4. **Áp cho service khác.** Kiểm JAR của 6 service còn lại: chỉ `api-gateway` có `spring-boot-data-redis`; user, event, ticket, payment, discovery không có. Thêm cùng biến cho `api-gateway` (01:15Z). Kiểm sau đó, 3 phút gần nhất: `api-gateway` 9 trace có span Redis, `booking-service` 22 trace. Gateway trả 200 cho 15/15 request; hai container không restart.

## Thay đổi trên `exp-app`

- Thêm một dòng `SPRING_AUTOCONFIGURE_EXCLUDE=...` vào `/opt/flash-ticket-app/env/booking-service.env` và `api-gateway.env`. Bản trước khi sửa lưu cạnh đó, đuôi `.truoc-thu-redis-20261111`.
- Tạo lại hai container bằng `docker compose -f <svc>.yml -p flash-ticket-<svc> up -d --force-recreate` trong `/opt/flash-ticket-app/compose-exp`, giữ nguyên image.

## Giới hạn và việc còn lại

- Chưa đọc mã nguồn Spring Boot và agent để xác nhận cơ chế; chưa thử phương án khác (thêm cầu nối Micrometer Tracing, hoặc cấu hình agent).
- Loại lớp này làm mất các observation của Lettuce phía Micrometer (nếu có ai dùng); hệ thống hiện không xuất metric Micrometer ra ngoài nên chưa thấy ảnh hưởng. Chưa kiểm metric Redis phía client của agent.
- `db.statement` chứa khóa Redis có mã sự kiện. Cần xét theo danh sách trường được phép của B16 trước khi coi là cấu hình chính thức.
- Hai cửa sổ M1 của lượt đêm (22:01 và 22:17Z) được thu **trước** khi sửa, nên không có span Redis. Không so trực tiếp chúng với dữ liệu thu sau sửa.
- Muốn đưa vào hệ thống thật thì thêm biến này vào env của `booking-service` và `api-gateway` (secret `ENV_*` của CD); đó là việc của repo FlashTicket, cần Minh quyết.
- Span RabbitMQ thiếu tên queue và vhost (R-04) là vấn đề khác, chưa tra.
