# Kiểm lại sau rebase lên main `4d57225` (28/11/2026)

Main tiến `6b77144` → `4d57225` (PR #58 của nhóm: Payment đọc báo cáo qua replica, 2 pod HA) trước khi push bản sửa REVIEW-5. Rebase 8 commit; bản cũ giữ ở nhánh local `rca/quan-sat-log-6b77144` @`f29073f`. Đầu mới `f40b849`, 138 file so với main. Đã push lên PR #17 (`--force-with-lease` khớp `2a275b5`).

- `git range-diff 6b77144..rca/quan-sat-log-6b77144 origin/main..HEAD`: 7 commit trùng nội dung; commit agent đổi ở `services/payment-service/.env.example` (1 xung đột: giữ khối `PAYMENT_REPORT_REPLICA_*` của main rồi khối `OTEL_*` của nhánh).
- Chỉ kiểm lại phần main đổi (Payment, manifest, script K8s); phần khác dùng lại `../README.md`.

| Kiểm | Kết quả | File |
|---|---|---|
| Payment `verify` + B16 (`chay-verify-payment.sh`) | surefire 153 + failsafe 57 (test mới của main), 0 lỗi; B16 PASS | `verify/` |
| Manifest 8 service (gồm Discovery) | `OTEL_AGENT_ENABLED=false`, `HOST_ID` = `spec.nodeName`, `ENVIRONMENT=production`, không khóa MDC tùy chỉnh, mọi giá trị chuỗi; mẫu Secret trùng main; `deployment.yaml` Payment so với main chỉ thêm 2 biến | `log/kiem-manifest.txt` |
| Bộ kiểm K8s (bản main mới, có fixture Payment HA) | 4/4 đạt | `log/test-k8s-*.log`, `log/k8s-tom-tat.txt` |
| Quét bí mật diff so với main | 0 dòng | lệnh trong LOG |

CD main mới có guard writer/cùng digest cho Payment như Booking, Event, Ticket (REVIEW-5 R2 áp cả Payment).
