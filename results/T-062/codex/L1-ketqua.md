L1 XONG

1. Đã dựng VNPay giả, 20 người mua và sự kiện 100.000 chỗ. Giao dịch mua trọn có vé; đã ghi `EXP-APP-XONG`.
2. Hai lượt cuối: mỗi lượt 720 hành trình, 144 mua thành công, **0 lỗi/401/dropped**. Gateway khớp **3.097/3.092 request**, chênh **5 request (0,161%)**, đều ở bước poll.
3. [Báo cáo đầy đủ](D:/RCA-flashticket/results/T-062/tai-2/bao-cao-L1.md), [bảng so sánh](D:/RCA-flashticket/results/T-062/tai-2/lap-2-luot.md). Đã kiểm manifest; giữ đủ sáu lượt, gồm v1 bị lỗi parent và lượt dừng.
4. Chờ Claude đánh giá độ lặp và kiểm R toàn gói. Không còn k6 chạy; mock/tunnel giữ sẵn.

```powershell
. ./results/T-062/tai-2/chay-tai.ps1
Start-Tai -Scenario hanh-trinh -Seconds 1800 -Tag a7c94f120e37 -May tai
```

Lệnh đọc metadata tiến trình `Get-CimInstance` bị từ chối; chỉ ảnh hưởng chẩn đoán đóng gói, đã ghi trong báo cáo.