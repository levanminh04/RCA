# SimpleRCA M4 của T-017

Cài độc lập mô tả §3.1.2 của bài FSE26. Các lựa chọn bài bỏ ngỏ được khóa trong SPEC T017 và nháp WHY; đây chưa phải chương trình sinh số0,80 của tác giả.

Lõi `diagnose` chỉ nhận số đo, tên service quan sát và cấu hình. Adapter `prepare` biết mốc chia normal/incident; nhãn root chỉ ở scorer sau serialize. Không dùng đồ thị, statusCode, parentSpanID hoặc case path trong diagnosis. Score là tổng cảnh báo, không phải xác suất nguyên nhân.

Môi trường và lệnh đầy đủ: `results/T-017/moi-truong.md`. Chạy test bằng Python3.12 với `PYTHONPATH` trỏ site-packages môi trường T017 và `src/`, `PYTHONDONTWRITEBYTECODE=1`:

```powershell
py -3 -m unittest discover -s src/simplerca/tests -v
```

Đọc hồ sơ, kiểm đúng đắn và ví dụ tại `results/T-017/`. Normal controls thực có cảnh báo dương; không sử dụng ranking để khẳng định incident/root có ý nghĩa thống kê. Không có fallback trả thứ tự cột.
