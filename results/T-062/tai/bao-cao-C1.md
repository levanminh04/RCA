C1 XONG MỘT PHẦN

Đã hoàn thành máy tải và công cụ C1 theo brief v3 trên AWS `3.24.8.49`: dùng lại Docker/k6/chrony đã cài, ghim image bằng digest, lấy token PKCE qua exp-app trong bộ nhớ, k6 tự refresh, fixture qua API đọc, bộ lệnh Start/Stop/Get/Receive. exp-app chỉ chạy Python đọc trong bộ nhớ; không sửa máy hoặc repo FlashTicket, không chạm M1/test/nhật ký điều khiển tiêm lỗi, không commit/push. exp-obs giữ phần chuẩn bị v2, không phát tải ở đó trong v3.

Chạy sau `A2-XONG`, không tạo đơn mới. Lượt `d20261111190011`, container bắt đầu 19:00:21Z, kết thúc 19:05:21Z ngày 11/11/2026; exit 0, không OOM. Đầu ra thô 5.399.774 byte được giữ cả trên máy và hai thư mục nhận. Không chạy lại lượt này.

Kết quả từ `chay-thu-5p/phan-tich.json`, `summary.json`, `kiem-sau-chay.json`:

- 1.501 request Gateway, nhịp k6 đo 4,998830 req/s, 0 dropped iterations, 0 lỗi transport. 1.505 HTTP tổng gồm 4 request refresh Keycloak.
- 4 refresh thành công, 0 lỗi refresh, 0 HTTP 401. Refresh xảy ra 19:03:36–37Z. Không phải dùng phương án refresh qua exp-app; chỉ đăng nhập PKCE đầu lượt qua exp-app.
- Event 751/751, order 375/375, payment 225/225 trả 200. Tickets 150/150 trả 500. Không có 4xx/429. Hỗn hợp theo chu kỳ 100 iteration giữ 50/25/15/10; tổng 1.501 gồm 15 chu kỳ và thêm một request event.
- p95 Gateway 295,659 ms; theo route: event 294,379; order 289,998; payment 300,409; tickets 295,439 ms. Đây là latency đo từ AWS, chưa trừ trễ mạng. p95 Gateway loại request refresh; p95 tổng HTTP trong summary k6 vì vậy khác nhẹ.
- Hash đầu vào/đầu ra: 14 mục mỗi bản nhận, đều khớp. Workload/config/fixture trong snapshot khớp byte với file hiện hành. Raw count khớp summary. Quét file C1 không phát hiện mẫu JWT/khóa riêng. PowerShell parse, Python AST và k6 inspect đạt. Stop khi không có tải đạt; dừng giữa tải, nhánh obs và nhánh lỗi refresh chưa chạy thử vì không cần cho lượt này.

Sai thứ tự tự kiểm: hash `auth.py` được đối chiếu manifest sau lần PKCE chuẩn bị đầu tiên, chưa đúng yêu cầu kiểm trước khi dùng đầu ra cũ. Kết quả đối chiếu khớp (`kiem-hash-nguon.json`), không phát hiện lệch nguồn. Đã bổ sung kiểm hash vào `Initialize-C1Token` trước khi đọc/chạy nguồn cho các lần dùng tiếp theo. Lượt thử dùng nguồn đã được đối chiếu trước đó; không chạy lại chỉ vì đóng gói hoặc đổi phiên.

Phần chưa đạt: nền ứng dụng đủ bốn route chưa ổn định, vì tickets trả 500 trước và sau A2, rồi cả 150 request trong lượt thử. Chưa xác định cơ chế; dữ liệu HTTP phía tải không phân xử được lỗi xử lý đơn/issuance, xác thực liên dịch vụ hay cấu hình downstream. Không sửa ứng dụng vì C1 chỉ có quyền đọc exp-app. Đề xuất điều phối đọc lỗi và code của route tickets, kiểm cùng order và một fixture có issuance hợp lệ nếu đã có, rồi quyết sửa tối thiểu hoặc giới hạn sử dụng trước E1. Không đổi hỗn hợp, tạo thêm giao dịch hoặc bỏ route để làm số đẹp. Không dùng lượt này như bằng chứng nền ứng dụng không lỗi. Kiểm lại sau thay đổi chỉ phần bị ảnh hưởng; chỉ chạy lại 5 phút khi cần xác nhận nền đã ổn định.

File chính: `c1.ps1`, `chay-tai.ps1`, `doi-va-chay-thu.ps1`, `fixture.py`, `tong-hop.py`, `k6/workload-t062.js`, `k6/cau-hinh.json`, `k6/fixtures.json`, `k6/seed-orders.json`, `may-tai.md`, `ket-noi.md`, `fixture-v3.md`, `chay-thu-5p.md`, `chay-thu-5p/`, `out/d20261111190011/`, `HUONG-DAN-E1.md`, `CHECKPOINT.md`, các bằng chứng kiểm và `manifest-c1.json`. Danh sách file cuối cùng và hash nằm trong manifest; tài liệu/biên nhận v2 được giữ nguyên, `fixture-v3.md` nêu rõ khác biệt fixture hiện hành.

Lệnh E1 (thay mã ví dụ bằng mã mờ của runner; không có tải C1 nào còn chạy):

```powershell
. ./results/T-062/tai/chay-tai.ps1
Start-Tai -Seconds 1800 -Rate 5 -Tag a7c94f120e36 -May tai
Get-Tai -Tag a7c94f120e36 -May tai
# Khi State.Running=false:
Receive-Tai -Tag a7c94f120e36 -May tai
# Dừng sớm nếu cần:
Stop-Tai -Tag a7c94f120e36 -May tai
```

Quyết định mới: không thêm lựa chọn nghiên cứu. Máy AWS là USER_CONFIRMED theo brief v3; ứng dụng bốn route chưa sạch lỗi là FACT; cơ chế tickets 500 giữ OPEN, thuộc điều phối/app, ảnh hưởng khả năng dùng nền cho E1. C1 chỉ xác nhận công cụ tải và refresh ở một mức tải trong 5 phút, chưa trả lời mục tiêu mở rộng/ổn định giao dịch hay chất lượng RCA của DT18/MRP.

Phạm vi ghi của lượt này chỉ `results/T-062/tai/` và `codex/`; không ghi LOG/STATE/task. Điều phối nhận báo cáo để cập nhật hồ sơ chung theo quyền của mình. Prompt bàn giao trung tính ở `PROMPT-BAN-GIAO.md`; không tự mở phản biện. Nội dung cần đưa vào tài liệu chính thức: phiên bản/digest máy tải, hợp đồng workload, số đo thực tế và giới hạn route tickets. Đề xuất nội dung commit khi Minh yêu cầu: `T-062 C1: pinned k6 load runner, refresh and pilot evidence`; chưa commit hoặc push.
