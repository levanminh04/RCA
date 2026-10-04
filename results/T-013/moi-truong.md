# Môi trường T-013

Phương pháp chạy bằng môi trường đã duyệt WHY-15: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe`, Python3.12.10, pandas2.2.3, numpy1.26.4, scipy1.14.1, sklearn1.6.0. Danh sách thực của phiên: `trung-gian/freeze-py312-pin.txt`; cách dựng ghim đã có ở `results/T-006/moi-truong.md`. Không cài/sửa env hoặc source. PYTHONDONTWRITEBYTECODE=1; thread compute đặt1. Hai source HEAD/status trước/sau ở manifest và kiểm bàn giao.

`py312-pin` không có engineParquet và không có pip vì tạo bằnguv. Vì vậy dùng `py312` đã có chỉ đọc metrics.parquet→NPZ float64 trong `D:/RCA-ext/work/T-013/`, rồi pin đọc mảng, kiểm hash/shape. Không đổi rule chọnca và không chạy scorer bằngpy312. Freeze dùng `D:/RCA-ext/envs/tools/Scripts/uv.exe pip freeze --python ...`, chỉ đọc metadata.

Chạy từ `D:/RCA-flashticket`:

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
& D:/RCA-ext/envs/py312/Scripts/python.exe results/T-013/scripts/doc_parquet.py
& D:/RCA-ext/envs/py312-pin/Scripts/python.exe results/T-013/scripts/kiem_co_che.py
& D:/RCA-ext/envs/py312-pin/Scripts/python.exe results/T-013/scripts/kiem_ket_qua_cu.py
```

Lượt chính đã hoàn tất method checks rồi lỗi ở lệnh pipfreeze. Không chạy lại phần valid: `hoan_tat_kiem.py <run_dir>` nạp checks đã lưu, bổ sung mốc A ranker và kiểm rẻ còn thiếu, ghi summary/freeze. Script chỉ lấy function definitions của kiểm cơ chế, không chạy lại top-level. `kiem-tra.json` trỏ run được dùng.

Các lượt hỏng/progress/console được giữ ở `runs/`; không coi lỗi ghi stdout mã hóa là mất file đã ghi. LOG ghi lý do khắc phục. Không có dữ liệu tải mới; mẫuCSV đã tải T-006 và hash khớp caOB được phép.

Laptop đang có nhiều phiên. Mọi seconds ở T-013 chỉ là thời gian ghi tiến độ trên máy bận, không dùng như benchmark chính thức. Ước lượng toàn dataset lấy file kết quả T-005/T-007 và ghi giả định. Không chạy lượt >1 giờ, khôngEC2.
