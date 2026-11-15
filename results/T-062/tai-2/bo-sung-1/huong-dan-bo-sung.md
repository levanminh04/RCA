# L1 tiếp nối — bậc tải và độ bền

EXECUTE theo `results/T-062/codex/L1-tiep-1-brief.md`, tiếp nhận ngày 13/11/2026 02:32Z. Không mở lại kết quả hợp lệ của lượt trước. D2 của Claude giữ độc quyền máy tải tới khi không còn container `rca-tai-` đang chạy; không dừng container đó.

## Bậc tải

```powershell
. ./results/T-062/tai-2/chay-tai.ps1
Start-Tai -Scenario hanh-trinh -Seconds 240 -BuocTai 120 -Multiplier 3 -Tag <ma-moi> -May tai
```

`-Rate` trong scenario `hanh-trinh` là số hành trình trên 10 s, mặc định 12. Có `-BuocTai`: scenario standard chạy nhịp chuẩn từ 0 tới mốc, scenario increased bắt đầu đúng mốc và chạy nhịp chuẩn × Multiplier tới hết. Các hành trình chuẩn đã bắt đầu được hoàn tất theo gracefulStop; không cắt giao dịch đang làm. Hai scenario dùng cùng hỗn hợp và dữ liệu, phiên token riêng theo VU; cùng 20 người mua, cấp 40 phiên để không chia sẻ refresh token. Mỗi scenario có maxVUs 20; tổng k6 dự phòng tối đa 40 khi hai nhóm chồng lúc hoàn tất hành trình.

Không có `-BuocTai`: giữ một scenario, Multiplier áp dụng từ đầu. Cấu hình bằng `k6 inspect` không phát HTTP đã xác nhận cả hai nhánh trong `k6-inspect.json`. Lượt inspect đầu thiếu cờ truyền biến môi trường nên dừng tại init; được giữ trên AWS trong thư mục inspect đầu. Không dùng lượt đó làm bằng chứng tải.

Token access 300 s, seed refresh 1800 s. Hàm Start chặn mốc bậc quá trễ làm phiên của scenario thứ hai hết hạn khi còn chờ; thông báo trước khi phát tải. Cấu hình chiến dịch với bậc 120 s hoặc 600 s nằm trong khoảng này. Refresh của VU đang chạy vẫn ở tuổi 200 s. Không đăng nhập lại bằng password trong cửa sổ đo.

## Đường tới mock

```powershell
. ./results/T-062/tai-2/chay-tai.ps1
Test-L1Duong                # bộ chạy gọi giữa hai chu kỳ
Test-L1Duong -LamMoiToken   # chủ động cấp phiên mới trước cửa sổ
```

Test từ chối khi có tải `rca-tai-` đang chạy, tránh ghi lại token/tunnel giữa chu kỳ của agent khác. Nó kiểm PID mock đúng command line, health trực tiếp và health từ AWS, số phiên/hạn token/quyền file 0600. Mock chết thì khởi động lại từ cài đặt hiện hữu, giữ state/audit, tạo log mới; không tự chế cấu hình khi thiếu file. Một cổng đang khỏe nhưng PID không khớp sẽ báo lỗi thay vì thay tiến trình không rõ chủ sở hữu. Mọi sự kiện và hash trước/sau ở `su-kien-duong.jsonl`/`thay-doi-may.md`.

Tunnel cũ qua laptop có tự dựng lại PID chết, nhưng đã chết sau khi phiên Codex kết thúc. Không coi thử PID cũ là bằng chứng sống độc lập phiên. Bổ sung tuyến trực tiếp exp-app → AWS, reverse forward chỉ AWS loopback 19091 → mock exp-app 19090. Dùng khóa ed25519 mới, private key chỉ ở `/opt/flash-ticket-app/l1-vnpay/tunnel/forward-only.key`; không chép khóa hiện hữu hoặc đọc `~/.ssh`. AWS nhận đúng một dòng public key bằng append-only, hạn chế source IP exp-app, permitlisten/permitopen 127.0.0.1:19091, command /bin/false, không shell/PTY/agent/X11. Host key AWS lấy từ pin đã có trên laptop, không tự tin keyscan.

Supervisor ở exp-app chạy phiên tiến trình riêng, giữ khóa singleton, tự kết nối lại SSH sau exit và ghi log. Cài đặt/chuyển tuyến chỉ sau D2. Script không đổi firewall, sshd, ứng dụng hoặc biến thanh toán. Cách hoàn tác: dừng đúng PID supervisor L1 đã kiểm, chuyển về tuyến cũ khi cần; quản trị viên có thể thu hồi đúng dòng khóa `l1-mock-forward-only`, giữ các khóa cũ. Agent không đọc file `.ssh` để làm thao tác đó.

Windows Task Scheduler probe không chạy được (HRESULT 0x80070003); ghi `scheduler-register.json`. Không sửa quyền hoặc tìm cách vượt sandbox. Tuyến remote dùng các máy đã được cấp quyền trong yêu cầu L1.

## Kiểm tích hợp

Marker bảo trì hoàn tất 23:41:18Z đã có. Sau khi D2 rời máy tải: kiểm phục hồi helper khi không có tải; một giao dịch mới phải COMPLETED và có vé; pilot 300 s trên cấu hình mới; một lượt 240 s tăng ×3 ở giây 120. Bảng 30 s báo cả request gửi k6 và completed k6/gateway, lấy mốc thực từ k6; giữ phần đuôi gracefulStop riêng. Báo đủ lỗi, dropped và đỉnh hành trình đồng thời, không suy 20 VU đủ cho mọi mức lỗi/chậm từ một phép thử khỏe.

Checkpoint sống: `checkpoint.json`, cùng `../CHECKPOINT.md`. Script tiếp nối: `../chay-bo-sung-1.ps1`. Chưa coi mã đã viết hoặc inspect thành bằng chứng thực chạy; các trường kết quả chỉ ghi sau khi có đầu ra hợp lệ.


Điều chỉnh tại 02:45Z: phiên sandbox không đọc được Path/StartTime của PID SSH do Claude dựng. Không dừng các PID đó; giữ tuyến19090 của Claude, dùng cổng AWS loopback19091 riêng. k6 vẫn xác minh paymentUrl thuộc mock19090 rồi chỉ chuyển prefix transport sang19091; không đổi signed query. Test-L1Duong kiểm health theo tuyến mới. Lỗi kiểm Windows PID được ghi, không tìm cách vượt quyền để dừng tiến trình.


Mốc đo 30 s dùng startTime thực của scenario đầu theo [k6/execution chính thức](https://grafana.com/docs/k6/latest/javascript-api/k6-execution/); lưu thêm sai lệch mốc suy ra của scenario sau. Không lấy thời gian tạo container hoặc nhận file làm t0 của bảng rate.
