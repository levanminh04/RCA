# Bàn giao 1 — giao dịch đã kiểm

**Đính chính về R-09 (22:50Z):** HTTP probe kiểm kê/giao dịch dùng traceparent có parent không được xuất. Không dùng các root HTTP ấy để đánh giá R-09. Sáu trace Saga PRODUCER/CONSUMER bên dưới vẫn là bằng chứng message đã đọc thật; chúng là trace riêng. Tải cuối đã bỏ traceparent tự tạo; xem `SU-CO-TRACEPARENT.md` và bàn giao 2 hiện hành.

2026-11-12T22:20Z. Codex L1 → Claude điều phối/T-063. Chưa kết thúc L1.

Đơn `2f6c01b2-ab05-49d5-affc-3c0bbafb67a2` đã `COMPLETED` lúc 22:18:37Z, có 1 vé `VALID`. API quan sát `PENDING_PAYMENT → ISSUING → COMPLETED`; log nghiệp vụ bổ sung `freeze`, `accept-payment`, `issuance-result`, Saga `WAITING_BOOKING → WAITING_TICKETS → COMPLETED`. Xem `giao-dich-1.json`, `giao-dich-2.json`, `log-giao-dich.jsonl`. Lượt 1 gặp gateway 503 sau recreate; lượt 2 tiếp tục đúng đơn đó, không xóa kết quả cũ.

VNPay giả đã kiểm chữ ký, IPN RspCode `00`, return HTTP 302, checkout 200. Audit ở `/opt/flash-ticket-app/l1-vnpay/audit.jsonl`; bản đã nhận trong `log-giao-dich.jsonl`. Mock callback đi trực tiếp payment `127.0.0.1:8083`, không qua gateway. Source mock giữ nguyên byte; adapter L1 thêm return/audit và bind loopback, xem `mock-runner.py`/`vnpay-install.json`.

Tempo `tempo-giao-dich-2.jsonl`: 8 trace được đọc, trong đó 6 trace Saga có tổng 6 PRODUCER + 6 CONSUMER. Trace ví dụ `7ca3dcbae6bc41178554fa76281e994f`, `c6c075e2468997703e9be083609c1a78`. Trace tạo payment `01a40fbceeff4ab2a3d8b4d6382fe225`; trace lấy vé `c8101de67b294ca689c4f3d572b8a298`. Chưa kết luận R-04/R-09; bộ kiểm của T-063 đánh giá.

Đã tạo 20 người mua, password chỉ ở `/opt/flash-ticket-app/env/l1-buyers.json` mode 0600. Sự kiện mới `3e7c1df9-ada4-4081-94a1-548b80a5da86`, loại vé `ffb36fc7-e30a-4efe-987f-ca5533520453`, 100.000 chỗ và purchaseLimit 100.000. Tạo/submit/approve/publish qua API. Không sửa DB.

L1 đang hoàn thiện token pool và tuyến mock từ máy tải; chưa ghi EXP-APP-XONG ở mốc bàn giao này. Claude tiếp tục chỉ đọc exp-app cho đến marker đó.
