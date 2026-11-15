# Ứng viên revision FlashTicket cho đợt thu (nháp, 12/11/2026 21:51Z — chưa chốt)

- Đang chạy trên `exp-app`: image `ft-local/<svc>:arm64-t062-6b21ed55` (7 service), Keycloak `ft-local/keycloak:arm64-776d9c9e`.
- Nhánh `rca/quan-sat-log` (GitHub và cục bộ): `fba6bc8` = merge `main` (K3s, bỏ thống kê Event).
- Khác biệt code nghiệp vụ `6b21ed55..fba6bc8` (lệnh `git diff 6b21ed55 fba6bc8 -- services/*/src/main`):
  - Event: xóa `StatisticsController`/`StatisticsService` (`GET /api/v1/organizer/events/{id}/statistics`), bỏ `bookingBaseUrl` của read-model; mở `GET /actuator/health/liveness|readiness`.
  - Payment: `payment.booking.discovery-enabled` (mặc định `false` → giữ `BOOKING_SERVICE_URL` như cũ); bắt `IllegalStateException` của LoadBalancer thành `BOOKING_UNAVAILABLE`; mở hai probe.
  - Ticket: mở hai probe.
- Đánh giá sơ bộ: trên Docker với discovery tắt, luồng mua (order → payment → VNPay → saga → vé) không đổi về hành vi; khác biệt là API thống kê organizer (không thuộc tải) và probe.
- Việc còn lại trước khi chốt: L1 kiểm luồng lõi trên bản đang chạy; nếu instrumentation (span bọc outbox Keycloak, cấu hình agent) cần build lại image app thì build từ đầu nhánh + commit instrumentation, kiểm lại luồng lõi trên bản mới; ghi WHY, commit, image digest, cấu hình vào `dong-bang.md`.
