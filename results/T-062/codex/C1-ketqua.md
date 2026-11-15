C1 XONG MỘT PHẦN

- Đã hoàn thành máy tải AWS, k6 ghim digest, tự refresh token và bộ lệnh E1.
- Lượt thử 5 phút: **1.501 request**, p95 **295,659 ms**, 4 refresh thành công; **0 HTTP 401, 0 dropped iterations**.
- **Tickets trả 500 ở 150/150 request**; ba route còn lại đều 200. Cần điều phối xử lý trước khi coi nền ứng dụng ổn định.
- Hash và đối chiếu raw/summary đều đạt. Không còn tải đang chạy; không commit/push.

File và bằng chứng chỉ ghi trong `results/T-062/tai/`: [báo cáo C1](D:/RCA-flashticket/results/T-062/tai/bao-cao-C1.md), [số liệu từng route](D:/RCA-flashticket/results/T-062/tai/chay-thu-5p.md), [hướng dẫn E1](D:/RCA-flashticket/results/T-062/tai/HUONG-DAN-E1.md).

```powershell
. ./results/T-062/tai/chay-tai.ps1
Start-Tai -Seconds 1800 -Rate 5 -Tag <ma-mo> -May tai
Stop-Tai -Tag <ma-mo>
Receive-Tai -Tag <ma-mo>
```

`Receive-Tai` dùng sau khi container kết thúc.