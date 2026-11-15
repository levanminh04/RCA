# VNPay giả đã kiểm

FACT, 12/11/2026 UTC. Đã dùng nguyên byte `deploy/rca-test/mock_vnpay.py` từ nhánh `rca/quan-sat-log`. Adapter `mock-runner.py` thêm callback return sau IPN, audit an toàn, bind loopback; không sửa repo FlashTicket. Python 3.12 sẵn có trên exp-app; không cài lại hay tải image.

`vnpay-install.json` lưu hash trước/sau, PID, container ID và image. Đổi đúng 7 biến `VNPAY_*`, tạo lại **chỉ** payment-service. Image trước/sau giống nhau, ứng dụng vẫn revision `6b21ed55`. Backup bí mật ở `/opt/flash-ticket-app/l1-vnpay/payment-service.env.before`, mode 0600. Hoàn tác: phục hồi backup vào `env-t062/payment-service.env`, recreate riêng payment-service cùng image, sau đó dừng đúng PID mock nếu cần; giữ state/audit. Không thao tác hoàn tác trong lượt này.

Mock chạy tại `/opt/flash-ticket-app/l1-vnpay/`, PID ghi ở `pid`, cổng `127.0.0.1:19090`. Mock xác minh chữ ký request, lưu giao dịch để idempotency, ký IPN. IPN và return gọi trực tiếp payment `127.0.0.1:8083`, không qua gateway. Return không theo redirect ra ngoài. Audit không chứa chữ ký hoặc query string. Bằng chứng một đơn: `giao-dich-2.json#/mock`, `log-giao-dich.jsonl` dòng mockAudit: checkout 200, RspCode 00, return 302.

Máy tải tới mock qua hai SSH tunnel, khóa giữ trên laptop: local `29090 → exp-app:127.0.0.1:19090`, reverse `tai:127.0.0.1:19090 → local:29090`. Không đổi firewall hoặc mở cổng mới. PID và stderr ở `tunnel-state.json`, `tunnel-*.stderr.txt`. Máy tải health 200 đã kiểm. Laptop/tunnel phải còn sống khi chạy tải; mất tunnel là lỗi hạ tầng, không quy thành lỗi phương pháp. Không dùng VNPay thật hoặc ngrok.

Lượt tạo payment đầu sau recreate gặp gateway 503. Payment khởi động và đăng ký Eureka lại; đã đọc readiness rồi tiếp tục đúng đơn, lần sau 200. Không khẳng định nguyên nhân chính xác của 503 chỉ từ thời điểm. Chi tiết giữ ở `giao-dich-1.json`, `payment-readiness.jsonl` và `giao-dich-2.json`.
