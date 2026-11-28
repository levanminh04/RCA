# Kiểm lại sau rebase lên main `85b5033` (28/11/2026)

Nhánh local `rca/quan-sat-log-dung-lai` @`1ee1c7c` trên `85b5033`. Bản trước rebase giữ ở nhánh local `rca/quan-sat-log-f0a5d30` @`e086fdc` (= đầu PR #17 trên GitHub lúc kiểm). Minh duyệt rebase ngày 28/11. Chưa push.

Main tiến từ `f0a5d30` lên `85b5033` (PR #60, `39a6f34`): Payment định tuyến PostgreSQL theo trạng thái read-only của transaction (`PG_RW_HOST`/`PG_RO_HOST`), bỏ cờ `PAYMENT_REPORT_REPLICA_*` và health gate; `deploy-k8s-service.sh` bỏ guard reader và `writer-baseline` của Payment, từ chối Secret còn khóa cũ (`RETIRED_PAYMENT_DB_KEYS`); `test-k8s-deploy.py` đổi fixture Payment.

- `git rebase origin/main`: 1 xung đột ở `services/payment-service/.env.example`: giữ phần của main (hai dòng chú thích định tuyến, không còn biến `PAYMENT_REPORT_REPLICA_*`), thêm khối `OTEL_*` của PR.
- `git range-diff f0a5d30..e086fdc 85b5033..1ee1c7c`: 10 commit trùng (`=`), 1 commit (agent) chỉ đổi ngữ cảnh `.env.example`. `git diff --check 85b5033 1ee1c7c` sạch.
- 8 file cả hai bên cùng sửa ngoài `.env.example` (configmap Payment, `application.yaml`, 5 file Java Payment) tự gộp; configmap giữ khối `OTEL_*`, `application.yaml` giữ `LogFields`/`SafeStackTracePrinter`.

## Kết quả

| Kiểm | Kết quả | File |
|---|---|---|
| Payment `verify` + B16 (`chay-verify-payment.sh`) | 156 + 59 test, 0 lỗi (số khác lượt trước do PR #60 xóa/thêm test Payment); B16 PASS | `verify/tien-do.tsv`, `verify/log/` |
| Bộ kiểm K8s (`py -3`) | 4/4 đạt; `test-k8s-deploy.py` mới: "Payment routing fixtures passed: PG keys, one-Pod profile, source guards and old/new snapshot rollback" | `k8s/` |

Không chạy lại: Booking, Event, Ticket, User (main không đổi các service này; các commit PR trùng nguyên), image/agent.

**Đối chiếu mục Hoàn tác** (`results/T-076/mo-ta-pr17.md`) với script CD tại `85b5033`: Payment không còn cờ reader, `writer-baseline`, nên đã bỏ Payment khỏi điều kiện reader trước merge và danh sách `writer-baseline`; thêm dòng Payment định tuyến theo transaction. Booking (`deploy-k8s-service.sh:508–534`), Event (`681–702`), Ticket (`880–`) giữ cơ chế cũ.

**Chưa kiểm:** CI trên GitHub cho đầu mới; `results/T-076/mo-rong-may-84.md` §4 còn nhắc guard reader của Payment (ngoài phạm vi rebase được duyệt).
