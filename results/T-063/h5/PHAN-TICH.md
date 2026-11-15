# T-063 — H5 "thành phần chết im": thu nhận khi một service bị `docker pause` (12/11/2026 22:04Z, Claude)

**Phép thử.** `docker pause flash-ticket-user-service-user-service-1` 60 s (22:02:22–22:03:22Z, `exp-app`, không có tải chạy; [`pause-user-service.txt`](pause-user-service.txt)). Đọc mẫu thô Prometheus quanh khoảng đó ([`doc_prom_pause.py`](doc_prom_pause.py) → [`pause-user-service-prometheus.txt`](pause-user-service-prometheus.txt)). Sau unpause: `running`, `RestartCount=0`.

**Quan sát.**
- `container_cpu_usage_nanoseconds_total`, `container_memory_usage_total_bytes`, `container_uptime_seconds` (docker_stats, nhịp 10 s): **khe 70 s** (S+55 → S+125). docker_stats không báo container đang bị pause; `container_uptime_seconds` sau khe tăng đúng 70 s (đồng hồ thực, không phản ánh pause).
- Metric JVM tự báo qua OTLP (`jvm_cpu_recent_utilization_ratio`, `jvm_class_count`, `http_server_request_duration_seconds_count`): **khe 63 s**.
- Tức là khi pause, **mọi** tín hiệu của thành phần đó biến mất cùng lúc; không còn nguồn nào nói "container còn đó nhưng không phản hồi".

**Kết luận.** Với cấu hình hiện tại, H5 chỉ có thể dựa vào (a) sự vắng mặt của tín hiệu (khe) — M1 P7 loại thành phần mất tín hiệu khỏi xếp hạng — và (b) triệu chứng ở bên gọi (span CLIENT lỗi/timeout tới service đó) khi có tải đi qua. Chưa có nguồn sống/chết độc lập.

**Đề xuất (bước 5 T-063, cùng lượt đổi Collector cách A):** bật receiver `httpcheck` của Collector `exp-app` gọi `GET /actuator/health/liveness` của 7 service Java mỗi 10 s (đầu dò hộp đen, chuẩn thực hành): ra `httpcheck.status`, `httpcheck.duration`, `httpcheck.error` theo endpoint — độc lập với telemetry tự báo của service. Lưu ý: ở bản `6b21ed55` liveness cần quyền (trả 401 nhưng vẫn chứng minh tiến trình phản hồi); bản `fba6bc8` mở `permitAll` cho liveness/readiness (Event, Payment, Ticket — các service khác **chưa kiểm**). Span SERVER của lời gọi này phải được lọc (mở rộng `filter/health` theo `url.path`), và liveness không chạy health indicator DB nên không sinh con mồ côi (**chưa kiểm**). Hạ tầng (Postgres, Redis, RabbitMQ, Mongo): lỗi scrape của receiver tương ứng (`otelcol_scraper_errored_metric_points_total`) là nguồn độc lập sẵn có — **chưa kiểm** khi pause.
