L1 XONG

- Đã thêm `-BuocTai` và `Test-L1Duong`; tunnel chạy độc lập trên `exp-app`, tự phục hồi. Không dừng/sửa D2 của Claude.
- Lượt ×3: **577 hành trình, 117 mua trọn, 0 lỗi/401/dropped**. Nhịp gửi **5,13 → 15,48 req/s**; đỉnh đồng thời 10, giới hạn 20 VU đủ trong lượt này.
- Pilot sau bảo trì cuối: **72/72 mua trọn**, không lỗi. Giữ riêng pilot đầu có **33 lỗi 503/504**, nguyên nhân còn OPEN.
- JSON/CSV và hash đều khớp; đã kiểm manifest và quét bí mật.

[Bàn giao 3](D:/RCA-flashticket/results/T-062/tai-2/BAN-GIAO-3-sau-bao-tri.md) · [Bảng 30 giây](D:/RCA-flashticket/results/T-062/tai-2/bo-sung-1/buoc-tai.md) · [Báo cáo đầy đủ](D:/RCA-flashticket/results/T-062/codex/L1-tiep-2-ket-qua.md)

```powershell
. ./results/T-062/tai-2/chay-tai.ps1
Test-L1Duong
Start-Tai -Scenario hanh-trinh -Seconds 1800 -BuocTai 600 -Multiplier 3 -Tag a7c94f120e38 -May tai
```