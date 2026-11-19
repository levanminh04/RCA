# T-067 — Kiểm tín hiệu RCA trên bản ghim (bước 7)

Bản: FlashTicket `rca/exp-2026-11` = `36a3725d…`, image `arm64-t067-36a3725d` (chuỗi container ở `trien-khai/chuoi-container.json`).
Cửa sổ: 18/11/2026 07:21:22–07:31:24Z (epoch 1794986482–1794987084). Lượt k6 `t067-tin-hieu-001`, ×1, 600 s.
Bộ kiểm: repo lab `862b208` `tests/signals/check_purchase_journey.py`, đọc thẳng Tempo/Loki/Prometheus trên exp-obs.
Danh sách cặp RabbitMQ và ngưỡng khai trước, commit trước khi có dữ liệu bản ghim (`tests/signals/cap-rabbitmq.json`, `tieu-chi.json`).
Kết quả máy đọc: `kiem-tin-hieu/kiem-tin-hieu-lan1.json`; phân tích bổ sung: `kiem-tin-hieu/phan-tich-bo-sung-lan1.json`.

Câu kết luận giới hạn đúng SPEC: **đạt các yêu cầu đã kiểm trên các đường thực sự chạy**; không ghi "đủ R-01…R-10".

## Kết quả theo mục khai trước

| Mục | Kết quả | Số (con trỏ JSON trong `kiem-tin-hieu-lan1.json`) |
|---|---|---|
| Span SERVER có `http.route` (gateway, booking, event, payment) | đạt | `#/span/server_http_route/*` — ≥ 5 trace mỗi service |
| Span CLIENT gateway → booking, event, payment (có span SERVER con) | đạt | `#/span/client_gateway/*` |
| Span DB client `event_db`, `booking_db`, `payment_db`, `ticket_db` | đạt | `#/span/db/*` |
| Redis ở booking và gateway | đạt | `#/span/redis/*` |
| User + Mongo (`GET /api/v1/me` có span server user-service và span `mongodb` cùng trace) | đạt | `#/span/user_mongo` — 3 trace (3 lời gọi lúc 07:21:33–07:21:40Z, HTTP 200) |
| RabbitMQ: 6 cặp P1–P6, PRODUCER → CONSUMER nối cha–con | đạt 6/6 | `#/rabbitmq_cua_so/*` (≥ 20 trace mỗi cặp), `#/luong_chinh/rabbitmq_cua_don/*` |
| Luồng chính: đơn COMPLETED, đúng 1 vé, correlationId qua service | đạt | đơn `e7a6a11c-1b41-4321-807a-adf0fa4b2efd`; log correlation ở booking, payment, ticket (`#/luong_chinh/service_co_log_correlation`); DB: `COMPLETED`, đặt 1, 1 vé, 1 issuance (truy vấn trên exp-app, LOG 07:4xZ) |
| Log nối span ≥ 95% theo service | đạt | gateway 3119/3179 = 98,1%; booking 936/936; payment 1440/1440; ticket 432/432 (`#/log/*`) |
| Log đủ 13 trường bắt buộc B16 | đạt | 100% dòng ở điểm bắt buộc (`#/log/*/du_truong_B16`) |
| Mọi điểm log bắt buộc có dòng | đạt | `#/log/*/diem_khong_co_dong` rỗng |
| Metric: JVM, HTTP server (7 service), pool DB, queue RabbitMQ, docker_stats (7 container), httpcheck | đạt | `#/metric/*` |

## Phân tích bổ sung (sau khi xem kết quả, báo riêng)

- **Cặp đúng bản tin của đơn:** trong trace của đơn có 3–4 cặp mỗi loại vì worker outbox gom nhiều bản tin một trace. Lần từ dòng log `*.message.processed` của chính đơn: mỗi cặp P1–P6 có đúng 1 span CONSUMER đúng queue, cha là PRODUCER đúng service và routing key (`phan-tich-bo-sung-lan1.json#/cap_dung_ban_tin`).
- **60 dòng gateway không khớp span:** đều là `gateway.request.completed`, HTTP 200, `routeId=unmatched`, trace không có trong Tempo. 60 dòng trong 600 s khớp nhịp `httpcheck` 10 s gọi `/actuator/health/liveness` của gateway. Giải thích khả dĩ: lời dò sức khỏe không xuất trace [chưa kiểm trực tiếp]. Ngưỡng vẫn đạt khi tính cả các dòng này.

## Đường chưa kiểm

- Luồng không chạy trong lượt: hủy sự kiện, hoàn tiền, đơn hết hạn có phát vé lỗi (`booking.issuance-failed.v1`), cấu hình sự kiện (`event.*`), tạo người dùng (`identity.user-created.v1`), check-in. Không ghi là đạt.
- Service không có điểm log bắt buộc: event-service, user-service, discovery-server (chỉ kiểm span và metric).
- Kiểm thử bộ kiểm trên dữ liệu bản 3 (17/11): `kiem-tin-hieu/thu-bo-kiem-ban3-20261117.json` — phép thử công cụ, không phải bằng chứng bản ghim.
