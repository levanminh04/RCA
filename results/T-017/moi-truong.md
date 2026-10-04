# Môi trường riêng T-017

Python3.12.10 Windows x64. Môi trường mới `D:/RCA-ext/envs/T-017-simple/`; không sửa env/src có sẵn. Phiên bản đầy đủ ở `requirements.lock`; gồm numpy1.26.4, pandas2.2.3, pyarrow17.0.0 và mọi dependency phụ. Numpy/pandas theo bộ đã dùng T006 (WHY15); pyarrow17 cùng môi trường kiểm dataset T002, vì cần đọc parquet. Không có SciPy/torch/causal-learn trong bản M4.

```powershell
py -3 -m venv D:/RCA-ext/envs/T-017-simple
py -3 -m pip --python D:/RCA-ext/envs/T-017-simple/Scripts/python.exe install -r D:/RCA-flashticket/results/T-017/requirements.lock
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH='D:/RCA-ext/envs/T-017-simple/Lib/site-packages;D:/RCA-flashticket/src'
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
py -3 -m unittest discover -s D:/RCA-flashticket/src/simplerca/tests -v
```

Trong tool phiên này, gọi trực tiếp venv python.exe không cho output đáng tin; lệnh trên dùng launcher Python cùng ABI3.12 và site-packages riêng. Không cài vào Python hệ thống, không ghi cache vào env/src cũ. Gói mới tải/cached khoảng100MB, không tải dataset. Freeze đã lưu trước dev; kiểm import/versions trước runner. Ghim dependency phụ lấy từ freeze, không mặc định đó là phiên bản tác giả dùng SimpleRCA; tác giả có lock khác nhưng code không khớp bài.

Lệnh chạy lại (phải dùng mã run mới; không ghi đè runs):

```powershell
py -3 D:/RCA-flashticket/results/T-017/scripts/fetch_injection.py
py -3 D:/RCA-flashticket/results/T-017/scripts/run_dev.py --run <mã-lượt-mới>
py -3 D:/RCA-flashticket/results/T-017/scripts/independent_example.py --input-dir D:/RCA-ext/work/T-017/example-input-<mã-lượt-mới> --out D:/RCA-flashticket/results/T-017/runs/<đầu-ra-mới>.json
```

Lượt cuối khoa học là run-dev-004; run001/003 dùng regex alias sai đã giữ, run001/002 có failed case vì thiếu metadata nguồn dự kiến. Metadata mốc30dev đã kiểm đúng hash T002/HuggingFace revision, chỉ tải file10byte/ca; không telemetry mới.

Đọc/render PDF dùng bundled runtime26.904.11930 (pypdf6.10.0, pypdfium2 có sẵn), script read_pdfs.py. Không tạo hoặc chỉnh PDF; chỉ trích text và ảnh bảng trong work T017. Các PDF/tài liệu nguồn/zipcode và hashes có trong inventory/provenance. Time log là Asia/Saigon; run001 naive host cùng timezone, run002–004 ghi+07 rõ.

**Chi phí:** tổng elapsed đúng run004 được ghi trong progress.jsonl; vì tới8phiên khác cùng laptop, đây chỉ là số tiến độ. Không dùng thời gian đó so5.99s/case của PDF hoặc quyết ngân sách P3. Không lượt nào vượt1giờ; không EC2. Byte nguồn thực lấy manifest, không đoán RAM/CPU cost từ kích thước file.
