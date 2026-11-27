# Bước 4 theo SPEC bản 6 — kiểm cục bộ (27/11/2026)

Nhánh local `rca/quan-sat-log-dung-lai` @`d46f3ae` (7 commit trên `f178870`, 129 file so với main). Bản theo SPEC bản 3 giữ ở nhánh local `rca/quan-sat-log-ban-3` @`ae5a870`. Dùng lại kết quả lượt bản 3 (`../README.md`) cho phần code không đổi; chỉ chạy lại phần đổi.

## Phần đổi so với lượt bản 3

`git diff rca/quan-sat-log-ban-3 HEAD`: 32 file — 7 `configmap.yaml`, 7 `deployment.yaml`, 7 file mẫu Secret (trả về bản main), 8 `docker-entrypoint.sh` (bỏ khối CA, trùng bản PR), `deploy/observability/README.md`, 2 file `rca-test` của Booking. Code Java ngoài `rca-test` không đổi, nên `verify` của 7 service còn lại dùng lại kết quả lượt bản 3.

## Kết quả

| Kiểm | Kết quả | File |
|---|---|---|
| Bộ kiểm K8s của nhóm | `test-k8s-deploy.py`, `test-k8s-discovery.py`, `test-https-config.py`, `test-k8s-rollout-hooks.py` đạt (lần đầu chạy được bản cuối vì Docker bật) | lệnh trong LOG |
| Manifest | 7 container có `OTEL_AGENT_ENABLED=false` và `HOST_ID` = `spec.nodeName` trong `env:`; ConfigMap đích `http://otel-collector:4318`, không có `OTEL_CA_PEM_B64`, không có `SPRING_AUTOCONFIGURE_EXCLUDE`, 29 tên tham số che (`q` + 28 `vnp_*`), mọi giá trị là chuỗi; file mẫu Secret trùng main | lệnh trong LOG |
| Booking `-P rca-test verify` | **454 test, 0 error** (trước: 453 test, 67 error); `RcaFaultsWebConfigTests` 3/3, gồm test mới "không có bean → không đăng ký interceptor" | `log/booking-rca-test-verify-2.log` |
| Booking `verify` (production) | 445 test đạt; kiểm B16 đạt; jar production không có lớp `RcaFaults` | `log/booking-verify.log` |
| Image Booking, Assistant | build lại từ `d46f3ae` (Dockerfile tạm chỉ thay dòng `ADD`, như lượt bản 3) | `log/image-*.log` |

**Agent** (`chay-agent-v6.sh`; env dựng theo thứ tự K8s: ConfigMap → Secret giả → `env:` của `deployment.yaml` đặt sau cùng — mô phỏng quy tắc "`env` thắng `envFrom`" bằng thứ tự dòng, không phải K8s thật; Collector thử tên `otel-collector`, HTTP, không processor):

| Lượt | Secret giả | Env cuối | Dòng khởi động agent | Collector nhận | Bộ nhớ (giới hạn 768 MiB) |
|---|---|---|---|---|---|
| `tat-secret-true` | `OTEL_AGENT_ENABLED=true` | `false` | 0 | 0 byte | 417 MiB |
| `tat-khong-secret` | không có khóa | `false` | 0 | 0 byte | 386 MiB |
| `bat-ghi-de` | không có khóa, ghi đè thủ công `true` | `true` | 1 | 748 KB trace, 428 KB metric | 492 MiB |

Lượt `bat-ghi-de` (`bat-ghi-de/phan-tich.txt`): `url.query` = `email=…&phone=…&q=REDACTED&vnp_SecureHash=REDACTED&vnp_TxnRef=REDACTED` — tham số trong danh sách bị che; email, số điện thoại còn (không phải tên tham số FlashTicket dùng; lọc toàn bộ query là việc của Collector khi mở rộng). Header Authorization/Cookie, client secret không gửi. Exemplar: 0. Thuộc tính tài nguyên: `service.version` = commit, `deployment.environment=production`, `host.id` = `HOST_ID`.

Log B16 khi agent tắt (`tat-secret-true/booking.log`): `environment=production`, `hostId` = `HOST_ID`, `serviceVersion` = commit.

## Môi trường thử

- RabbitMQ cho `-P rca-test` lỗi đọc `.erlang.cookie` (eacces) ba lần liền khi chạy mặc định; chạy container bằng user `rabbitmq` (`--user 999:999`) thì đạt. Lần chạy đầu `-P rca-test` (1 error `contextLoads`, không kết nối được RabbitMQ) giữ ở `log/booking-rca-test-verify.log`.
- Booking dùng initdb và cờ `missing-queues-fatal=false` như lượt bản 3.
