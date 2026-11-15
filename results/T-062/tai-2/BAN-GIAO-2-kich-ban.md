# Bàn giao 2 — kịch bản cuối đã kiểm pilot

Cập nhật 2026-11-12T22:51:55.6157436Z. Codex L1 → Claude điều phối/T-063.

Kịch bản hiện hành `k6/hanh-trinh.js`, `k6/cau-hinh.json`: 12 hành trình/10 s, tỷ lệ 70/20/5/5, 20 VU, refresh ở tuổi 200 s. Không gửi traceparent tự tạo. Chỉ đọc requestId/correlationId do ứng dụng trả về để nối log; không gửi mã lượt hoặc nhãn.

Pilot cuối `l1p20261112v2`, 300 s: 361 hành trình; số theo nhóm {"browse":253,"purchase":72,"abandon":18,"cancel":18}. Hoàn thành 361; lỗi 0, dropped 0, HTTP 401 0. Refresh thành công 20. Gateway 1555 request; 1555 nối được với log gateway, thiếu 0, lệch status/route 0. `out/l1p20261112v2/analysis.json`, `routes.csv`, JSON/CSV thô, summary, trạng thái đơn và manifest giữ đủ.

Các lượt v1 giữ ở thư mục out nhưng không dùng làm chuẩn cuối/R-09; lý do và bằng chứng ở `SU-CO-TRACEPARENT.md`. Việc sửa chỉ ảnh hưởng kịch bản và đối chiếu log; không tạo lại mock/tài khoản/sự kiện hoặc ứng dụng. EXP-APP-XONG vẫn có hiệu lực. Hai lượt 10 phút của source cuối đang làm tiếp, chưa tự đặt ngưỡng chênh lệch đạt; đọc CHECKPOINT.md/lap-2-luot.md.

```powershell
. ./results/T-062/tai-2/chay-tai.ps1
Start-Tai -Scenario hanh-trinh -Seconds 1800 -Tag a7c94f120e37 -May tai
Get-Tai -Tag a7c94f120e37 -May tai
Receive-Tai -Scenario hanh-trinh -Tag a7c94f120e37 -May tai
Stop-Tai -Tag a7c94f120e37 -May tai
```

Tag phải mới; không gửi tag vào HTTP. FLASH ở lượt riêng: `-Multiplier 3` khi Start. Không có Scenario vẫn gọi tải đọc cũ; file cũ không sửa. Hai SSH tunnel loopback qua laptop phải còn sống; Start kiểm mock health trước khi phát. Không chạy hai workload đồng thời trên máy tải. Mức đã kiểm là cấu hình khởi điểm; Claude quyết cấu hình thu chính theo quyền điều phối.
