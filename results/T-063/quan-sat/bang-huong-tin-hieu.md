# T-063 — Bảng hướng H1–H8 → tín hiệu → có trên kho? → có trong gói ca? (bản 1, 12/11/2026 21:54Z)

Nguồn kiểm: danh mục 545 tên metric Prometheus `exp-obs` (21:20Z); nhãn từ `results/T-062/ca/_metric-bo-sung/` (dữ liệu 11–12/11); TD-02, TD-03 (`thay-doi-may.md`); gói ca T-062 (`cases/<id>/prometheus.json` = 7 kênh: cpu, mem, db-size, workload, error, latency-50, latency-90; `raw-traces.jsonl`; `raw-logs.jsonl`). "Gói" = gói do `safe-export.py` ghim T-058 tạo (không sửa); "gói bổ sung" = file mới của bộ đóng gói mở rộng T-063 (`dong-goi/`, chưa dựng).

| Hướng | Tín hiệu cần | Trên kho | Trong gói | Còn thiếu / việc |
|---|---|---|---|---|
| H1 DB/cache/broker thành nút, cạnh xếp hạng | span CLIENT có `db.system`, `server.address`, `db.namespace`; span PRODUCER/CONSUMER có `messaging.destination.name`; metric DB theo CSDL/bảng, Redis, RabbitMQ theo queue | span DB/Redis: **có** (gói trace). Span message: **chưa kiểm** (tải đọc → 0 PRODUCER/CONSUMER). PostgreSQL theo bảng, RabbitMQ theo queue: **có từ 21:35Z 12/11** (TD-02; trước đó gộp chuỗi, tốc độ âm) | trace: có; metric DB/queue: **không** (chỉ `db-size`) | tải mua vé (L1) để có span message; gói bổ sung: `postgresql_*` theo bảng, `redis_*`, `rabbitmq_*` theo queue |
| H2 JVM/cgroup | `jvm_gc_duration_seconds_*`, `jvm_memory_used_bytes{pool}`, `jvm_thread_count{state}`, `jvm_cpu_recent_utilization_ratio`; `container_cpu_throttling_data_*`, `container_cpu_limit` | JVM: **có** (8 service Java). Throttling/limit: **có từ 21:39Z 12/11** (TD-03) | **không** | gói bổ sung: các metric trên theo `service_name` |
| H3 pool kết nối | `db_client_connections_usage{state}`, `_pending_requests`, `_max`, `_wait_time_*`, `_use_time_*` | **có** cho booking, event, payment, ticket (5 pool, có nhãn `pool_name`); Keycloak (Agroal), user-service (Mongo) **không** | **không** | gói bổ sung; ô dev pool (vd. POOL-EVENT) |
| H4 queue | `rabbitmq_message_current{queue,state=ready/unacknowledged}`, `rabbitmq_consumer_count{queue}`, `rabbitmq_message_published/delivered/acknowledged_total{queue}`; span PRODUCER/CONSUMER | metric theo queue: **có từ 21:35Z** (30 queue). Span: **chưa kiểm** | **không** | tải mua vé; gói bổ sung; ô dev consumer chậm |
| H5 thành phần chết im | nguồn sống/chết độc lập telemetry của chính service: `container_uptime_seconds`, `container_restarts_total`, trạng thái container (docker), `up` của scrape | uptime/restarts: **có từ 21:39Z** (TD-03); `up` chỉ có job tự scrape; trạng thái pause của Docker: **không** (docker_stats bỏ qua container đã dừng? — **chưa kiểm** với `docker pause`) | **không** | kiểm hành vi docker_stats khi pause/stop; gói bổ sung; ô dev tạm dừng một service khác Ticket |
| H6 thao tác nền | span job (`spring-scheduling`), `thread.name`, phân loại gốc (`span-goc/`) | **có** | trace: có | — (dùng được trên 9 ca cũ để kiểm cài đặt) |
| H7 tải tăng so với sự cố | lưu lượng theo route (`http_server_request_duration_seconds_count{http_route}`), tỷ lệ lỗi theo route, độ trễ theo route; số liệu k6 | **có** | `workload`/`error` theo service (không theo route) | gói bổ sung theo route; ô "tải tăng kèm lỗi" |
| H8 sàn độ lớn E4 | (không cần tín hiệu mới) | — | — | cài trong M1-FT |
| H8 adapter khi container tạo lại | `container_id`/`service_instance_id` đổi giữa N và A | có | có | kiểm adapter với ca có tạo lại container |
| H8 kênh log nghiệp vụ | log B16 có `outcome`, `reasonCode` trên đường mua vé | **chưa kiểm** (tải đọc) | log: có (`raw-logs.jsonl`) | tải mua vé; log hạ tầng (Postgres, RabbitMQ…) **không thu** — Collector cách A |

## Điều kiện đóng băng rút ra

1. Tải mua vé chạy trọn (L1) → kiểm span message, log nghiệp vụ, R-04/R-09.
2. Bộ đóng gói mở rộng xuất gói bổ sung (H1–H5, H7) theo khúc thời gian ngắn ngay sau mỗi chu kỳ.
3. Collector cách A (log hạ tầng + không mất log khi tạo lại container) và span bọc job Keycloak.
4. Kiểm `docker_stats` với container bị `pause`/`stop` (H5).
