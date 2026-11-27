# Bước 4 lại sau rebase lên main `6b77144` (27/11/2026)

Main tiến `f178870` → `6b77144` (22 commit) trước khi push. Nhánh local `rca/quan-sat-log-dung-lai` rebase lên `6b77144`, đầu mới `2a275b5` (7 commit, 129 file so với main). Bản trên `f178870` giữ ở nhánh local `rca/quan-sat-log-f178870` @`d46f3ae`. Chênh nội dung: `../../bang-file-pr17.md` mục "Rebase lên main `6b77144`".

Chỉ chạy lại phần main đổi; phần không đổi dùng lại `../ban-6/README.md` và `../README.md` (discovery, gateway, payment, assistant `verify`; lượt agent `tat-khong-secret`, `bat-ghi-de` — đường gửi và danh sách che không đổi).

| Kiểm | Kết quả | File |
|---|---|---|
| Bộ kiểm K8s của nhóm (bản trên main mới) | `test-k8s-deploy.py`, `test-k8s-discovery.py`, `test-https-config.py`, `test-k8s-rollout-hooks.py` đạt. `test-k8s-deploy-routing.sh` không chạy được trên laptop (thiếu `jq`); CI GitHub chạy | `log/test-k8s-*.log` |
| Manifest C2 | 7 service: `OTEL_AGENT_ENABLED=false`, `HOST_ID` = `spec.nodeName` trong `env:`; ConfigMap đích `http://otel-collector:4318`, không CA, không `SPRING_AUTOCONFIGURE_EXCLUDE`, 29 tên che, exemplar tắt, mọi giá trị là chuỗi; file mẫu Secret trùng main; `deployment.yaml` Booking so với main chỉ thêm 2 biến (giữ `podAntiAffinity` của main) | `log/kiem-manifest.txt` |
| `verify` + kiểm B16 (`chay-verify-4.sh`) | user 70, event 178, ticket 229, booking 453 test, 0 lỗi; B16 đạt cả 4; Ticket `TicketPostgresIT` 22 đạt | `verify/tien-do.tsv`, `verify/log/` |
| `-P rca-test verify` | Event 186, Booking 462 test, 0 lỗi | `verify/log/*-rca-test-verify.log` |
| Jar production Booking | không có lớp `RcaFaults` | `log/booking-package-production.log` |
| Lượt agent `tat-secret-true` (image Booking mới, `../ban-6/chay-agent-v6.sh`) | env cuối `false`, 0 dòng khởi động agent, Collector 0 byte; 410 MiB / 768 MiB; log B16 `environment=production`, `hostId`, `serviceVersion` = commit (135/135 dòng) | `tat-secret-true/` |
| Quét bí mật trong diff so với main | không có khóa riêng, token, mật khẩu | lệnh trong LOG |

Không chạy: `.github/scripts/test-ticket-replica.sh` (bộ thử replica của nhóm, không có trong CI, không đụng code của PR).
