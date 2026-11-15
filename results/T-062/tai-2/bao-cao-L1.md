L1 XONG

Đã hoàn thành phần triển khai và đo của brief L1. Có API kiểm kê, VNPay giả, 20 người mua, sự kiện 100.000 chỗ, kịch bản mua trọn, pilot cuối và hai lượt 10 phút cùng source/config. Claude đánh giá độ lặp của lưu lượng; L1 không tự đặt ngưỡng đạt.

1. **Đã làm.** Đơn kiểm `2f6c01b2-ab05-49d5-affc-3c0bbafb67a2` tới COMPLETED và có 1 vé VALID. Log ghi đủ đặt chỗ → đóng băng snapshot → nhận thanh toán → phát vé → hoàn tất Saga. Pilot cuối `l1p20261112v2`: 361 hành trình, 72 mua trọn, 0 lỗi hành trình/401/refresh/dropped. Hai lượt cuối mỗi lượt 720 hành trình đúng 70/20/5/5, 144 mua trọn, 36 hủy, 36 bỏ; 0 lỗi hành trình/401/refresh/dropped. Đơn bỏ kiểm riêng đã EXPIRED. Nguồn số: `kiem-dau-ra-cuoi.json`, `out/*/analysis.json`, `kiem-cuoi-api.jsonl`.

2. **File đã ghi.** Đầu ra trong `results/T-062/tai-2/`: `api-kiem-ke.md/.json`, `vnpay-gia.md`, `tai-khoan.md`, `k6/hanh-trinh.js`, `k6/cau-hinh.json`, `chay-tai.ps1` và helper, hai bàn giao, `lap-2-luot.md/.json`, `CHECKPOINT.md`, `thay-doi-may.md`, bằng chứng log/Tempo và sáu thư mục lượt trong `out/`. Danh sách và hash đầy đủ ở `manifest-L1.json`. Có báo cáo trong `results/T-062/codex/L1-phu-luc-2-20261112.md`; nối thêm `results/T-062/ha-tang/thay-doi.md`. Không sửa source nghiệp vụ, repo FlashTicket, tasks/docs/src hoặc C1 cũ; không commit/push. Không có hash commit mới vì không sửa `deploy/rca-test/`.

3. **Kiểm và kết quả.** Gateway nhận 3.097 và 3.092 request ở hai lượt cuối, khớp đúng mọi request k6 theo ID trả về, không thừa/thiếu hoặc lệch status/route. Tổng chênh 5 request, 0,161% so với lượt A; cả 5 ở GET trạng thái đơn (397 so với 392, chênh 1,259% của endpoint đó). Nhịp gateway theo 600 s là 5,1617 và 5,1533 req/s. JSON/CSV, console counter và summary khớp; 36 mục hash gốc của ba lượt cuối đều hợp lệ; source/config A = B = hiện hành; 0 orderId dùng lại giữa hai lượt. `lap-2-luot.md` có cả bảng routeId gateway độc lập và bảng endpoint nối theo ID, cùng chênh tuyệt đối/tương đối. CSV theo route, bước và hành trình ở thư mục mỗi lượt.

   Với một đơn trong pilot cuối, sáu trace Saga liên quan có tổng 8 PRODUCER + 8 CONSUMER; audit mock có IPN thành công, return 302 và checkout 200 (`tempo-giao-dich-v2.jsonl`, `mock-audit-v2.jsonl`, `log-giao-dich-v2.jsonl`). Hai trace HTTP mẫu của pilot cuối có root hợp lệ, không có parent vắng (`parent-pilot-v2.jsonl`). Đây là bằng chứng mẫu; R-04/R-09 toàn gói do T-063 kiểm. 9 script PowerShell và 22 file Python qua kiểm cú pháp; quét mẫu JWT/private key được lưu riêng. Không truy vấn Prometheus nhiều chuỗi.

4. **Điều còn mở và quyết định phụ thuộc.** Claude cần đánh giá độ lặp và chốt cấu hình thu chính; chưa tự xác nhận chuẩn tải hoặc kết luận R-04/R-09 toàn gói. Tỷ lệ/mức tải hiện hành là khởi điểm của SPEC, chưa phải quyết định nghiên cứu mới. FLASH ×3 đã tham số hóa, chưa chạy xác nhận FLASH. Tải hiện dùng 20 VU/20 phiên và SSH tunnel loopback qua laptop; laptop/tunnel phải còn sống để checkout mock. Tài khoản/sự kiện/đơn giữ lại; expiry cũ có thể sinh công việc nền trong lượt sau, đã khai trong `tai-khoan.md`. Kết quả L1 cung cấp nền quan sát giao dịch cho DT18/MRP, chưa đánh giá chất lượng RCA, khả năng mở rộng hoặc độ ổn định dài hạn.

**Lỗi đã tìm và xử lý.** V1 tự phát traceparent với parent không được xuất. Đã giữ cả pilot v1, lượt 10 phút v1 và lượt v1 dừng sớm; sửa kịch bản bỏ header đó, dùng ID ứng dụng trả về, rồi kiểm lại đúng phần phụ thuộc. Xem `SU-CO-TRACEPARENT.md`; không dùng v1 làm chuẩn cuối/R-09. Lỗi tickets 500 của fixture cũ: thiếu issuance → TicketProblem 404 → handler chung ánh xạ 500; probe chỉ đọc và stack đã phân xử, đơn COMPLETED mới lấy vé 200. Đây là lỗi nghiệp vụ đã ghi bằng chứng, L1 không sửa. Các lượt 503 sau recreate, probe sai ID và lỗi chuẩn bị đều được giữ, không đổi thành kết quả khoa học.

**exp-app:** đã ghi `EXP-APP-XONG`. Thay đúng VNPay giả, 7 biến VNPAY_* và recreate riêng payment-service cùng image; tạo tài khoản/dữ liệu qua API. Bản ứng dụng vẫn `6b21ed55`. L1 không còn đổi cấu hình/file/container exp-app sau marker. Lệnh, hash cấu hình trước/sau và hoàn tác ở `thay-doi-may.md`, `vnpay-install.json`, `tai-khoan-ket-qua.json`. Không có k6 đang chạy khi bàn giao; giữ container và dữ liệu của cả sáu lượt. Mock và tunnel giữ để bộ chạy dùng tiếp.

Lệnh tải mới:

```powershell
. ./results/T-062/tai-2/chay-tai.ps1
Start-Tai -Scenario hanh-trinh -Seconds 1800 -Tag a7c94f120e37 -May tai
Get-Tai -Tag a7c94f120e37 -May tai
Receive-Tai -Scenario hanh-trinh -Tag a7c94f120e37 -May tai
Stop-Tai -Tag a7c94f120e37 -May tai
```

Tag phải mới. Trong scenario `hanh-trinh`, mặc định 12 hành trình/10 s; nếu truyền `-Rate`, đơn vị là hành trình/10 s. Không giữ `-Rate 5` từ runner tải đọc nếu muốn cấu hình đã kiểm này. FLASH ở lượt riêng thêm `-Multiplier 3`. Không có `-Scenario hanh-trinh` vẫn chạy tải đọc cũ. Bộ chạy cần đổi đường dẫn dot-source và thêm tham số scenario như trên.

Prompt phản biện trung tính: `PROMPT-CLAUDE.md`. Điều phối cập nhật LOG/STATE theo quyền của mình; brief L1 giới hạn ghi ngoài các đường dẫn kết quả đã nêu. Nội dung nên đưa vào hồ sơ chính thức: cấu hình tải cuối, bảng lưu lượng, lỗi tickets và đính chính traceparent. Đề xuất nội dung commit khi Minh cho phép: `T-062 appendix 2: authenticated purchase workload and validation evidence`.


Chẩn đoán đóng gói: lệnh Get-CimInstance Win32_Process bị Access denied trong sandbox. Chỉ ảnh hưởng đọc metadata tiến trình; không ảnh hưởng các lượt đã thu hoặc đóng gói file. Không thử vượt quyền. Lần quét cuối đã xong, manifest đã ghi và đang được kiểm lại.
