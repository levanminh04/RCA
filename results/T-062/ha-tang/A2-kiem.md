# A2 — kiểm sau triển khai (exp-app, 2026-11-11T18:56:08Z)

- Commit: `ac3315535bb0760f35163afa397144cab7ed2efc` (nhánh `rca/quan-sat-log`, PR nháp levanminh04/flash-ticket-platform#17). Image: `A2-build-manifest.json`; jar booking/event có 4 lớp RcaFaults, 5 service còn lại 0.
- 7 service chạy image T-062, restarts=0 (`A2-sau-trien-khai.txt`). Keycloak giữ image cũ `arm64-776d9c9e` (đổi Keycloak không cần cho lượt này; tránh rủi ro realm).
- `GET /api/v1/events` qua Gateway: 200 (3/3).
- Log B16: Gateway ghi `gateway.request.completed` có traceId/spanId, `serviceVersion`=commit trên; event-service báo profile `rca-test` active.
- exp-obs (18:55Z): Tempo tìm thấy trace `resource.service.version`=commit trên từ api-gateway, booking, discovery, event, payment, ticket; Loki có dòng log 5 phút gần nhất từ cả 7 service; Prometheus có `jvm_memory_used_bytes` theo `service_instance_id` mới.
- **Khác bản T-058:** `service.instance.id` giờ là UUID sinh mỗi lần container khởi động (entrypoint), không còn `<svc>-1`. Bộ đọc nào gom theo instance cần gom theo `service_name`.
- Chưa kiểm: test đầy đủ cần DB/MQ (để CI PR); Keycloak tracing native (Keycloak không đổi).

## Lượt 2 (19:21Z) — bản đang dùng cho D2/E1

- Commit `6b21ed55ecfef2217a90d23b560e44af2d425b36` = nhánh `rca/quan-sat-log` sau khi merge `origin/main` (gỡ 4 xung đột, giữ cả hai phía). Laptop: 7 service `mvnw verify -DskipTests` và booking/event `-P rca-test` đạt.
- 7 image `ft-local/<svc>:arm64-t062-6b21ed55` (`A2-lan2-build-manifest.json`), triển khai `A2-lan2-deploy.out`: health đạt, restarts=0.
- Topology D1 giữ nguyên sau recreate: Eureka BOOKING-SERVICE 127.0.0.1:18082 UP; kết nối JVM tới 15433/16379; quota Booking 1 CPU; GET events 200.
- Chạy thử 5 phút của Codex (C1) chạy trên bản lượt 1 (`ac331553`), không dùng cho RCA.
