# Bộ dựng đồ thị phụ thuộc P5

Đặc tả: `results/T-035/dac-ta-do-thi.md` (v1), bản trước chạy ở `dac-ta-do-thi-v0.md`. Đây là bộ dựng cấu trúc và độ phủ, chưa phát hiện bất thường hoặc xếp hạng.

`build(spans, interval, aliases, universe)` trả hai đồ thị thực thể/thao tác. `interval` dùng nanosecond hoặc null cho toàn bảng được caller cho phép. `Prepared` tạo chỉ mục một lần cho nhiều khoảng. `from_p3` thêm các trường tùy chọn rỗng. `project` trả tập nút/cạnh chiếu từ mức thao tác; inventory được giữ riêng ở đồ thị thực thể. Thao tác thuộc thực thể bằng khóa cặp, component_context giữ endpoint không có thao tác quan sát.

Không đưa locator, tên ca, mốc tiêm, root, fault hoặc nhãn vào API này. Runner T-035 chọn file theo allowlist, kiểm hash, cắt Nezha bằng p3; bộ đọc Node bổ sung chỉ lọc dev và kiểm đồng hồ trước xuất giá trị. Các CSV mức ngày chỉ được so mô tả ngoài bộ dựng.

Môi trường đo dùng Python 3.12, numpy/pandas `py312-pin`; Parquet reader pyarrow có sẵn từ môi trường T-014. Không cài hoặc đổi môi trường trong T-035. Phiên bản và vị trí thực tế ở `results/T-035/runs/day-du-001/environment.json`. Máy khác cần dựng dữ liệu theo `data/README.md`, môi trường theo các manifest môi trường P3 và có reader Parquet đúng phiên bản đã ghi; nếu thiếu, dừng phần đọc Parquet, không bỏ kiểm hash hoặc đổi dataset.

Tại máy đo:

```powershell
$env:PYTHONHASHSEED='0'
& 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -B results/T-035/fixture/check.py <tên-run-mới>
& 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -B results/T-035/scripts/run.py <tên-run-mới> --pilot
```

Chỉ chạy lượt đầy đủ khi chi phí pilot dưới trần và có quyền trong SPEC. Tên run phải mới; file kết quả dùng chế độ tạo mới, giữ lượt lỗi. Lệnh của phiên thực tế và thứ tự tiếp nhận nằm trong LOG T-035. `scripts/report.py` chỉ ghép nhãn sau khi toàn bộ đồ thị và thống kê không nhãn đã ghi.
