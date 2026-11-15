# Phản biện T-062 phụ lục 2 (tải có đăng nhập, đặt vé, thanh toán) — lượt 1

- **Người phản biện:** Claude (điều phối chiến dịch). **Ngày:** 13/11/2026 ~03:28Z.
- **Đầu ra được phản biện:** lượt L1 (12/11 22:08–23:20Z) và L1c (13/11 02:31–03:19Z) của Codex: `results/T-062/tai-2/` (gồm `bao-cao-L1.md`, `lap-2-luot.md`, `BAN-GIAO-1/2/3`, `bo-sung-1/`), `results/T-062/codex/L1*`.
- **Đã đọc:** SPEC-PHU-LUC-2 (gồm phần bổ sung), các bàn giao, bảng hai lượt, `buoc-tai.md`; **tự kiểm** trên file: 720/720 hành trình mỗi lượt v2 (`out/l1r20261112v2{a,b}/analysis.json`), 3.097/3.092 dòng `gateway.jsonl`; thời điểm 33 lỗi 503/504 của pilot `l1maint20261113a` đối chiếu sổ tiêm D2 (`results/T-063/tiem-loi/so.jsonl`); container trên máy tải (`docker ps -a`).

## Kết luận chung

Đạt mục tiêu SPEC: hành trình mua trọn chạy được trên bản triển khai, có `COMPLETED` + vé + message (6 PRODUCER/6 CONSUMER ở giao dịch đầu; R-04 đạt 1.561/1.561 trên một cửa sổ tải — `results/T-063/kiem-r/BAO-CAO.md`); hai lượt 10 phút cho lưu lượng gateway chênh 5 request (0,161%), chỉ ở bước poll; chạy lại sau bảo trì sạch (72/72). Tôi chấp nhận kịch bản làm **chuẩn tải** của đợt thu dev bản 2. Phát hiện và sửa lỗi `traceparent` của k6 bản đầu là điểm tốt có ảnh hưởng thật (R-09).

## Các điểm

**R1 — Tunnel SSH ngược `exp-app` → máy tải với khóa mới và supervisor trên `exp-app`. KHÔNG CHẶN; ghi phạm vi.**
- Phạm vi `exp-app` của SPEC: VNPay giả, `VNPAY_*`, tài khoản, dữ liệu thử. Tunnel phục vụ đúng VNPay giả, giới hạn chuyển tiếp một cổng, không cấp shell, không mở firewall, có bằng chứng (`gioi-han-tunnel.json`) — rủi ro thấp, giải quyết đúng sự cố tunnel chết khi phiên Codex kết thúc (Claude ghi nhận 02:20Z). Nhưng đây là thay đổi máy rộng hơn mô tả (khóa SSH mới, khóa công khai trên máy tải, tiến trình nền mới).
- Sửa tối thiểu: trong `thay-doi-may.md` có đủ cách gỡ (xóa khóa ở `authorized_keys` máy tải, dừng supervisor, xóa khóa trên `exp-app`); kiểm lại nếu thiếu.

**R2 — 33 lỗi 503/504 ở pilot đầu sau bảo trì: nguyên nhân đã xác định. KHÔNG CHẶN.**
- Mọi lỗi nằm trong 02:56:34–02:58:24Z, đúng lúc D2 của Claude pause Payment (02:55:49–02:58:20Z). Tải D2 hết sớm (02:53Z, lỗi bộ chạy của Claude — `results/T-063/chay/D2B-KET-QUA.md` mục đính chính), nên máy tải trống và L1c chạy pilot đúng luật. Câu hỏi OPEN này đóng.

**R3 — Callback VNPay giả gọi thẳng Payment, không qua Gateway. KHÔNG CHẶN; giới hạn cần ghi.**
- VNPay thật gọi IPN vào endpoint công khai (qua Gateway). Đường mock bỏ cạnh Gateway → Payment của callback; dữ liệu dev thiếu cạnh này. Ghi vào giới hạn của dev bản 2; cân nhắc định tuyến qua Gateway ở lượt sau.

**R4 — Giới hạn 20 VU mỗi scenario khi có lỗi làm chậm. KHÔNG CHẶN; theo dõi trong đợt thu.**
- Lượt khỏe (×1, ×3) không rơi lượt. Khi lỗi làm request chậm hàng chục giây (vd. PAUSE-PAYMENT ~29 s), VU có thể cạn → `dropped_iterations` → tải giảm đúng lúc lỗi (tải phụ thuộc lỗi). Bộ chạy phải ghi `dropped_iterations` theo chu kỳ để M1-FT (H7) và phân tích ảnh hưởng giao dịch dùng đúng.

## Bất đồng còn lại / câu hỏi mở

Không có bất đồng với người làm. Mở: R3 (định tuyến callback), R4 (đo trong đợt thu).

## Phản hồi của người làm

| Điểm | Người làm kết luận | Minh quyết |
|---|---|---|
| R1 | | |
| R2 | | |
| R3 | | |
| R4 | | |
