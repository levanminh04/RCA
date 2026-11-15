# Lượt lỗi chuẩn bị được giữ

- `rg` và `py` không có trên PATH của sandbox. Không cài lại; dùng PowerShell để điều khiển, Python 3.12 sẵn có trên EC2/Oracle để xử lý.
- Git platform báo dubious ownership. Không ghi global config; đọc revision với tùy chọn safe.directory chỉ trong lệnh, không đổi repo. Không có lỗi sandbox từ chối cần tìm đường vòng.
- `api-1.jsonl`: transport ban đầu nhận chuỗi base64 thay vì JSON do cách truyền command dài. Chưa dùng làm bằng chứng API. Đã đổi sang stdin SSH, giữ kết quả cũ.
- Thử API qua `127.0.0.1:8081` bị connection refused; gateway thực nghe `10.0.0.158:8081`. Lượt đó chỉ là chuẩn bị đọc; chưa tạo giao dịch. Bản sửa kiểm kê ở `api-1c.jsonl`.
- Probe detail ban đầu dùng ID không phải fixture hiện hành, trả 404. Đã dùng ID từ API/fixture thay vì coi đây là lỗi detail.
- Lệnh tạo sự kiện đầu đã thành công và checkpoint PUBLISHED. Lệnh gọi nhầm lần hai phát hiện checkpoint và dừng, không tạo sự kiện thứ hai. Đã đọc và dùng lại checkpoint.
- Payment recreate: request đầu qua gateway 503. Giữ `giao-dich-1.json`; tiếp tục đúng đơn ở `giao-dich-2.json`, không xóa hay tạo lại lượt cũ để giấu lỗi.
