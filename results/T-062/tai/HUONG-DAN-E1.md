# Dùng tải cho E1

Từ PowerShell ở `D:/RCA-flashticket`:

```powershell
. ./results/T-062/tai/chay-tai.ps1
Start-Tai -Seconds 1800 -Rate 5 -Tag <ma-mo> -May tai
Get-Tai -Tag <ma-mo> -May tai
# Chờ State.Running=false rồi nhận kết quả:
Receive-Tai -Tag <ma-mo> -May tai
# Dừng sớm khi cần, vẫn giữ container và kết quả:
Stop-Tai -Tag <ma-mo> -May tai
```

Thay `<ma-mo>` bằng mã mờ chữ thường/số/gạch ngang do runner cấp. Mỗi mã dùng một lần. Có thể gọi `Stop-Tai` không có Tag để dừng container tải C1 đang chạy. Không gọi khi một phiên C1 khác còn quản lý lượt đó. `Start-Tai` không chờ tải xong; trả container ID và metadata token không có bí mật. `Get-Tai` trả JSON trạng thái Docker; caller có thể `ConvertFrom-Json`.

Máy mặc định `tai` là AWS. URL Gateway/Keycloak theo `k6/cau-hinh.json#/targets`; các hàm nhận `-May tai|obs`. `obs` chỉ dùng khi AWS hỏng, ghi lý do vào `thay-doi-may-tai.md`; script chép đúng ba file k6 trong `/opt/rca-tai/k6/`, đăng nhập mới và chạy container k6 cùng digest. Nhánh obs chưa chạy tải trong C1; không thay đổi stack quan sát. Không chạy đồng thời hai máy.

Điều kiện: có `results/T-062/ha-tang/A2-XONG`, không có `D:/RCA-overnight/STOP`. Start từ chối khi đã có tải C1 trên máy hoặc mã đầu ra đã tồn tại. Runner phải gọi `Stop-Tai` khi thấy STOP; hàm dừng vẫn hoạt động khi STOP tồn tại. Script chờ/chạy thử C1 kiểm STOP mỗi 5 giây. Không có một daemon độc lập tiếp tục giữ tải nếu laptop mất nguồn; mỗi lượt Docker tự kết thúc theo thời lượng đã khai.

Đầu ra máy: `/opt/rca-tai/out/<ma-mo>/`; nhận về `results/T-062/tai/out/<ma-mo>/`. Mỗi lượt giữ bản chép workload/config/fixtures, hash đầu vào, `run.json`, giờ bắt đầu, `raw.json` NDJSON k6, `summary.json`, log và trạng thái container, hash đầu ra. Không đưa mã mờ vào request, header hoặc URL ứng dụng. Không bật `--http-debug` vì có Authorization/refresh token.

Hỗn hợp GET theo 100 iteration: event 50, order 25, payment 15, tickets 10; cùng fixture cho mọi pha. Rate là iteration đến mỗi giây, mỗi iteration một request Gateway; request refresh Keycloak được đếm riêng. Giữ executor và mức cấp VU từ workload nguồn: 4 cấp trước, tối đa 16. Khi xử lý quá chậm có thể có dropped iterations; phải báo số thực tế, không coi nhịp cấu hình là thông lượng đạt được.

Mỗi Start đăng nhập PKCE mới bằng tài khoản BUYER qua Python in-memory trên exp-app, pipe token sang máy tải. k6 tự refresh ở tuổi 200 giây; lỗi refresh dừng và giữ lượt. Không cần giữ phiên hơn 10 giờ. Dừng rồi Start mã mới là cách đăng nhập lại. Thời lượng một lượt tối đa 3600 giây theo workload nguồn.

Tổng hợp một lượt đã nhận:

```powershell
py -3 ./results/T-062/tai/tong-hop.py ./results/T-062/tai/out/<ma-mo>
```

Lệnh ghi `phan-tich.json` trong thư mục lượt và `chay-thu-5p.md` ở thư mục cha; báo cáo tự động này dùng cho lượt thử C1. Với E1, dùng số trong JSON rồi đặt báo cáo riêng để không ghi đè báo cáo thử. 429/401 là tập con của 4xx; p95 loại request refresh. Giữ số lỗi 5xx/transport ngay cả khi Docker exit 0.
