# Kiểm kê API hành trình

Ứng dụng đang chạy `6b21ed55`, không redeploy nhánh mới. Bằng chứng HTTP: `api-kiem-ke.json`, `api-1c.jsonl`, `giao-dich-1.json`, `giao-dich-2.json`, `su-kien-ket-qua.jsonl`. Trace id ở từng request là W3C traceparent đã gửi; đã đối chiếu một phần với log/Tempo, không phải chỉ correlation ID. Các probe kiểm kê này có parent client không được xuất: không dùng chúng để kết luận R-09. Tải cuối không gửi traceparent tự tạo (`SU-CO-TRACEPARENT.md`).

| API | Quan sát |
|---|---|
| GET /api/v1/events | 200 |
| GET /api/v1/events/{id} | 200 trên sự kiện mới; probe đầu dùng ID sai trả 404 EVENT_NOT_FOUND |
| GET /api/v1/events/{id}/availability | 503 CONFIG_NOT_READY ngay sau publish; sau xử lý message trả 200, 100000 chỗ |
| POST /api/v1/orders | 201, PENDING_PAYMENT; cùng idempotency key trả cùng orderId |
| POST /api/v1/payments | Lượt đầu 503 DEPENDENCY_UNAVAILABLE; tiếp tục cùng đơn sau readiness trả 200 |
| GET /api/v1/payments/vnpay/ipn | Không chữ ký: 200 với mã từ chối trong body; mock ký hợp lệ: RspCode 00 |
| GET /api/v1/payments/vnpay/return | 302; mock ký hợp lệ cũng 302, không theo redirect |
| GET /api/v1/orders/{id} | 200; quan sát PENDING_PAYMENT → ISSUING → COMPLETED |
| GET /api/v1/orders/{id}/payment | 200; latestAttempt SUCCEEDED |
| GET /api/v1/orders/{id}/tickets | 500 ở 3 đơn CANCELLED cũ; 200 ở đơn mới COMPLETED, 1 vé VALID |
| POST /api/v1/orders/{id}/cancel | 200, CANCELLED |

FACT: cơ chế tickets 500 nằm trong code xử lý lỗi. `tickets-log.jsonl` có ba stack trace cùng đường `TicketService.owned → missing → TicketProblem`, qua `GlobalExceptionHandler`. Đối chiếu code ở revision `6b21ed55`: `owned` ném TicketProblem khi không có issuance hoặc buyer không khớp; `missing` mang status 404/RESOURCE_NOT_FOUND. `GlobalExceptionHandler.handleException` dùng `ErrorCode.from`; switch không nhận TicketProblem nên rơi INTERNAL_ERROR/500. Không phải lỗi transport chung: cùng người mua lấy tickets của đơn COMPLETED trả 200.

Đã phân xử thêm bằng probe nội bộ chỉ đọc, giữa hai cửa sổ tải: `kiem-cuoi-api.jsonl`, `tickets-probe-log.jsonl`. Ba đơn CANCELLED cũ đều đi `TicketService.probe → missing`; probe không kiểm buyer, nên nhánh này là **thiếu issuance**, không phải buyer mismatch. Đơn COMPLETED có issuance và probe 200. Không truy vấn hoặc sửa DB. Không suy rằng tickets hỏng cho mọi đơn. Không sửa nghiệp vụ theo quyền L1. Nếu cần sửa, đề xuất hệ thống ánh xạ TicketProblem đúng status/code, giữ kiểm ownership; Claude/Minh quyết trong phạm vi sửa nghiệp vụ riêng.

Chuỗi mua trọn đã chạy được. Việc này tạo đầu vào HTTP/DB/cache/message/callback cho kiểm quan sát theo SPEC; chưa chứng minh tính đúng toàn hệ thống, khả năng mở rộng hoặc chất lượng RCA theo DT18/MRP. R-04/R-09 thuộc bộ kiểm T-063; L1 chỉ bàn giao bằng chứng.
