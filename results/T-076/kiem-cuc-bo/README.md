# Bước 4 — kiểm cục bộ nhánh PR #17 dựng lại (27/11/2026)

Nhánh local `rca/quan-sat-log-dung-lai` @`ae5a870` (worktree `D:/Project/ft-pr17-dung-lai`). Laptop, Docker Desktop 28.3.2, Java 21.0.10, Maven 3.9.12. Dữ liệu, khóa, token trong các lượt thử đều giả; CA thử chỉ dùng ở đây (không phải CA của obs).

## 1. Maven như CI (`chay-verify.sh`, kết quả `verify/tien-do.tsv`, log `verify/log/`)

| Service | `verify` | Kiểm B16 | Khác |
|---|---|---|---|
| discovery-server, api-gateway, user-service, ticket-service, payment-service | đạt | đạt | Ticket: `TicketPostgresIT` đạt |
| event-service | đạt | đạt | `-P rca-test verify` đạt |
| booking-service | đạt | đạt | **`-P rca-test verify` lỗi: 453 test, 67 error** (dưới) |
| assistant-service | đạt (`mvn`, nạp `mvc.env` như CI) | không thuộc danh sách B16 | |

- 3 file Java đã gỡ xung đột ở bước 2 (`OrderServiceImpl`, `PromotionServiceImpl`, `RefundServiceImpl`) qua biên dịch và test của Booking, Payment.
- Booking `-P rca-test`: 67 error đều ở 3 lớp test `@WebMvcTest` (`SecurityConfigTests`, `OrderControllerTests`, `AvailabilityControllerTests`), cùng nguyên nhân "`RcaFaultsWebConfig` cần bean `RcaFaults` không có trong test slice" (thông báo xuất hiện đúng 3 lần, mỗi ngữ cảnh một lần). Đã có từ PR cũ: LOG T-067 ghi `bb84d64` hỏng 68 error + 1 failure cùng nguyên nhân, để sửa ở W6. CI của nhóm không chạy `-P rca-test`, nên không làm CI đỏ; build `-P rca-test` của exp-app (`build.sh verify`) thì bị.
- Dịch vụ phụ như CI (`postgres:16.15`, `rabbitmq:4.3.6-management`). Lần khởi động RabbitMQ đầu lỗi đọc `.erlang.cookie` (chạy cùng lúc đang tải image); chạy lại thì đạt, vòng chờ của script nhận ở lần 53.

## 2. Image có agent (`agent/build-image.sh`)

- Mạng laptop chặn tải asset GitHub Releases. Jar agent 2.33.1 lấy từ Maven Central, **SHA-256 trùng giá trị ghim** trong Dockerfile. Build dùng bản tạm của Dockerfile chỉ thay dòng `ADD` bằng `COPY` jar đó (script kiểm đúng 1 dòng khác); Dockerfile commit không đổi, CI GitHub chạy dòng `ADD` gốc.
- Booking (jar production, không có lớp `RcaFaults`) và Assistant: chạy bằng uid 10001, có `/app/app.jar`, entrypoint `/app/docker-entrypoint.sh`, checksum agent trong image đúng, `SERVICE_VERSION` = commit `ae5a870…` (không phải `local-dev`).

## 3. Agent gửi tới Collector thử (`agent/chay-agent.sh`, `agent/collector-tho.yaml`, `agent/phan-tich.py`)

Collector thử nhận OTLP/HTTP qua TLS + token bearer, **không có processor**, ghi nguyên payload: thứ thấy trong file là thứ đã rời máy nguồn. Booking dùng ConfigMap của nhánh, ghi đè chỉ phần trỏ hạ tầng giả. Request mang sentinel ở query (email, số điện thoại, token, `vnp_SecureHash`, `code`), header `Authorization`/`Cookie`, body, path.

**Token/TLS** (`*/tom-tat.tsv`): sai token 401, không token 401, đúng token 200, HTTP không TLS 400.

**Lượt `mac-dinh` (cấu hình hiện tại của nhánh):**

| Sentinel | Kết quả |
|---|---|
| query: email, số điện thoại, token, `vnp_SecureHash`, `code` | **Lộ** ở `url.query` của span SERVER, và ở exemplar của metric `http.server.request.duration` |
| header `Authorization`, `Cookie` | không gửi (agent mặc định không thu header) |
| body request | không gửi |
| client secret, token xuất | không gửi |
| path (`SENTINELPATHBAD`) | ở `url.path` (path là định danh nghiệp vụ, B16 cho phép) |

- SQL: `db.statement` đã thay giá trị bằng `?` (sanitizer mặc định); tham số JDBC không thu.
- Span có event `exception` với `exception.message` và `exception.stacktrace`. Ở lượt này nội dung vô hại (tên host giả, lỗi khởi tạo JwtDecoder), nhưng **không có cấu hình agent nào bỏ được** `exception.message`; B16 bỏ nội dung exception khỏi log (`SafeStackTracePrinter`) còn agent vẫn gửi trong trace.

**Lượt `loc-nguon-1`:** thêm `OTEL_INSTRUMENTATION_SANITIZATION_URL_EXPERIMENTAL_SENSITIVE_QUERY_PARAMETERS=email,phone,token,code,vnp_SecureHash` và `OTEL_METRICS_EXEMPLAR_FILTER=always_off` → các tham số trong danh sách thành `REDACTED`, metric không còn sentinel. Đây là **danh sách chặn theo tên**: tham số không có trong danh sách vẫn gửi nguyên giá trị (B16 §6 yêu cầu whitelist trước khi xuất).

Khóa cấu hình tìm trong jar 2.33.1 (không dựa trí nhớ): `…http.{server,client}.capture-request-headers` (mặc định tắt), `…jdbc.experimental.capture-query-parameters` (mặc định tắt), `…common.db.query-sanitization.enabled`, `…sanitization.url.experimental.sensitive-query-parameters`. Không có khóa bỏ hẳn `url.query` hay `exception.message`.

## 4. Bộ nhớ (`docker stats`, lúc nghỉ sau vài request; giới hạn 768 MiB như `deployment.yaml`)

| Service | Agent tắt | Agent bật |
|---|---|---|
| Booking | 381 MiB | 499 MiB (+118 MiB), sẵn sàng sau ~88 s, không OOM |
| Assistant | — | 348 MiB, sẵn sàng sau 18 s, không lỗi, trace có `service.name=assistant-service` |

Không giới hạn bộ nhớ thì Booking 459 → 621–653 MiB (JVM tự chọn heap lớn hơn), không so thẳng với K8s. Mức dùng dưới tải thật vẫn OPEN (đo ở bước 9).

## 5. Môi trường thử khác thật (để đọc đúng kết quả)

- Booking cần role `booking_owner` (kết nối chạy `SET ROLE booking_owner`) và schema thuộc role đó: `agent/initdb/00-schema.sql`.
- Queue RabbitMQ không khai sẵn như môi trường thật: chạy với `SPRING_RABBITMQ_LISTENER_SIMPLE_MISSING_QUEUES_FATAL=false` (chỉ ở lượt thử).
- `OTEL_TRACES_SAMPLER=always_on` (bắt mọi trace), lô xuất 1 s.
