# Bàn giao 3 — tích hợp sau bảo trì exp-app

2026-11-13T03:08:34.1972771Z. Codex L1 → Claude điều phối/phản biện. Đã tiếp tục đúng ba việc trong `results/T-062/codex/L1-tiep-1-brief.md`. D2 `d2b-2a7f481a` được giữ nguyên; chỉ bắt đầu kiểm tải sau khi máy tải không còn container `rca-tai-` đang chạy. Marker bảo trì hoàn tất: `EXP-APP-BAO-TRI-1-XONG`, 12/11 23:41:18Z; ứng dụng vẫn image hiện hành, không redeploy trong L1.

**Giao dịch mới:** orderId f6dd8088-0f15-46a9-b666-3a6adc097b6d, final COMPLETED, 1 ticket(s), ticket state VALID. Chuỗi trạng thái API quan sát PENDING_PAYMENT -> ISSUING -> COMPLETED. IPN/return/checkout {"httpStatus":200,"body":{"attemptId":"52e1f4d8-6109-4005-831c-7f8107216b52","ipn":{"RspCode":"00","Message":"Confirm success"},"returnStatus":302}}. Chỉ gọi API hợp lệ, không sửa DB/code nghiệp vụ, không tự phát traceparent. Đường dẫn bằng chứng: `bo-sung-1/giao-dich-sau-bao-tri.json`; log/trace bổ sung theo file tại cùng thư mục.

**Pilot 5 phút:** `l1maint20261113a`: 361 journeys, 39 purchases completed, 1429 gateway requests; failed=33, dropped=0, 401=0, refresh failed=0; gateway missing=0, mismatch=0, extra=22. Không dùng pilot cũ trước bảo trì thay phép kiểm này. Source/config và JSON/CSV giữ trong thư mục lượt; đổi bậc tải là nhánh tùy chọn, pilot chuẩn vẫn một scenario.

Pilot ban dau l1maint20261113a: 361 journeys, 39/72 purchases completed; 33 create-payment failures (19x504 + 14x503). No dropped/401 from k6; original raw/log/trace retained. Subsequent stepped run clean; one additional standard pilot planned before dispatch in bo-sung-1/ke-hoach-kiem-lai-pilot.json. Cause of initial 503/504 remains OPEN; current clean window does not erase it.

**Bậc tải:** `Start-Tai` có `-BuocTai`; kết quả lượt 240 s, bậc 120 s, ×3 ở `bo-sung-1/buoc-tai.md`. Báo request/s theo 30 s ở cả k6 và gateway; không tự đặt ngưỡng chênh lệch. Trong lượt khỏe đã kiểm, maxVUs=20 mỗi scenario không gây dropped hoặc lỗi hành trình. Đây là kết quả ở mức tải/thời gian này, không bảo đảm đủ cho mọi lỗi hoặc chu kỳ dài.

**Độ bền:** `Test-L1Duong` kiểm PID/health mock, health từ AWS và token count/hạn/quyền file. Tunnel đã chuyển sang reverse SSH trực tiếp exp-app → AWS, supervisor chạy riêng trên exp-app; không còn phụ thuộc process Codex/laptop. Khóa mới chỉ forward AWS loopback 19091 tới mock exp-app 19090, không cấp shell, private key chỉ ở exp-app. Bằng chứng ở phuc-hoi-remote-ssh.json, phuc-hoi-mock.json và tunnel-independent-launcher-proof.json; phép kiểm no-shell ở gioi-han-tunnel.json; không đồng nhất kiểm PID cũ với độ bền qua phiên.. Giữ state/audit/log cũ và sự kiện khôi phục, không mở firewall. Script từ chối đổi đường/token khi có workload đang chạy hoặc marker bảo trì chưa hoàn tất.

```powershell
. ./results/T-062/tai-2/chay-tai.ps1
Test-L1Duong
Start-Tai -Scenario hanh-trinh -Seconds 1800 -Tag <ma-moi> -May tai
# Một lượt tăng bậc:
Start-Tai -Scenario hanh-trinh -Seconds 1800 -BuocTai 600 -Multiplier 3 -Tag <ma-moi-khac> -May tai
Get-Tai -Tag <ma> -May tai
Receive-Tai -Scenario hanh-trinh -Tag <ma> -May tai
Stop-Tai -Tag <ma> -May tai
```

Không gọi hai Start đồng thời. Start tự gọi Test và cấp phiên mới ngoài cửa sổ; không dùng `-Rate 5` cũ vì nhánh hành trình đếm trên 10 s. Mốc bậc phải còn trong hạn seed refresh của scenario chờ; Start kiểm và báo trước khi phát. Trong chu kỳ, VU tự refresh ở tuổi 200 s. R-04/R-09 toàn gói và các quyết định cấu hình thu vẫn thuộc T-063/điều phối; các lượt khỏe không bảo đảm 20 VU đủ khi mọi request bị chậm 35 s.

**Phạm vi và kiểm:** chỉ file trong tai-2, codex/L1-* và nối ha-tang/thay-doi.md. Không sửa tasks/docs/src, C1 cũ, repo FlashTicket, không commit/push. Các snapshot và manifest cũ được giữ. Hash/script/đầu ra bổ sung nằm ở `bo-sung-1/manifest-bo-sung-1.json`. Prompt phản biện trung tính: `PROMPT-CLAUDE-bo-sung-1.md`. Những điểm chưa chắc và hạn chế cụ thể ghi trong báo cáo bổ sung; không tự đóng câu hỏi nghiên cứu hoặc nghiệm thu T-063.
