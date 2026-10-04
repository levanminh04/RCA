# T-016 — Môi trường

Dựng ngày 04/10/2026. Không sửa môi trường nào có sẵn (`D:\RCA-ext\envs\py38-rcdlock`, `py312-pin` chỉ dùng để chạy).

## 1. Môi trường dùng lại (không sửa)

| Môi trường | Dùng cho | Nguồn cách dựng |
|---|---|---|
| `D:\RCA-ext\envs\py38-rcdlock` (Python 3.8.10) | chạy TORAI gốc, TORAI sửa, RCD, script tính tay | `results/T-006/moi-truong.md` mục 3 |
| `D:\RCA-ext\envs\py312-pin` (Python 3.12.10) | chấm điểm bằng `Evaluator` của RCAEval (`scripts/tong_hop_t016.py`, dùng `cham()` của T-006) | `results/T-006/moi-truong.md` mục 2 |

Các gói thực sự được nạp khi chạy TORAI/RCD trên laptop (34 gói, không có `torch`, `tigramite`): `runs/s11-goi-duoc-nap-laptop.txt`.

## 2. `D:\RCA-ext\envs\T-016-cong-cu` (mới, laptop)

Dùng để: đọc parquet (S0, S9), đọc PDF bài RCD, dựng `logts` bằng Drain (S9), ghép cột bằng phép gán Hungarian (S9). Không chạy phương pháp RCA.

```
D:\RCA-ext\envs\tools\Scripts\uv.exe venv --python C:\Users\84583\AppData\Local\Programs\Python\Python312\python.exe D:\RCA-ext\envs\T-016-cong-cu
D:\RCA-ext\envs\tools\Scripts\uv.exe pip install --python D:\RCA-ext\envs\T-016-cong-cu\Scripts\python.exe pandas==2.2.3 numpy==1.26.4 pyarrow==18.1.0 pypdf==5.1.0 drain3==0.9.11
D:\RCA-ext\envs\tools\Scripts\uv.exe pip install --python D:\RCA-ext\envs\T-016-cong-cu\Scripts\python.exe scipy==1.14.1
```

Bản cài được (`uv pip freeze`): cachetools 4.2.1, drain3 0.9.11, jsonpickle 1.5.1, numpy 1.26.4, pandas 2.2.3, pyarrow 18.1.0, pypdf 5.1.0, python-dateutil 2.9.0.post0, pytz 2026.4, scipy 1.14.1, six 1.17.0, tzdata 2026.5. Phiên bản pandas, numpy, pyarrow, scipy chọn trùng `py312-pin` (T-006) và EC2 (T-007). `drain3` 0.9.11 là bản mới nhất trên PyPI lúc cài; bài TORAI không ghi bản Drain dùng.

## 3. EC2 — `~/rca/T-016/envs/py38` (mới)

Máy: EC2 của T-007 (m7i-flex.large, 2 vCPU, 7,6 GiB, Ubuntu 24.04). Script: `scripts/e0_dung_ec2.sh` (log `~/rca/T-016/runs/e0.log`). `~/rca/envs/tools/bin/uv` chỉ được chạy. Đính chính (REVIEW R6): lần dựng 04/10 01:53 UTC đã ghi ra ngoài `~/rca/T-016/` ba đường: thư mục `~/.local`, `~/.local/bin` và liên kết `~/.local/bin/python3.8` (do `uv python install` tạo, vì script chỉ đặt `UV_PYTHON_INSTALL_DIR`). Không ảnh hưởng kết quả (mọi lượt gọi Python của môi trường bằng đường tuyệt đối). Minh duyệt hoàn tác; đã xóa ba đường này ngày 04/10 lúc 11:53 UTC, sau khi kiểm `~/.local` chỉ chứa đúng liên kết đó. Script nay đặt thêm `UV_PYTHON_BIN_DIR=$B/python/bin`, nên lần dựng sau chỉ ghi trong `~/rca/T-016/`.

- RCAEval: `git clone ~/rca/src/RCAEval ~/rca/T-016/src/RCAEval`, checkout `259ea4167160256a74ad30004aa3d96a998c846e` (script dừng nếu HEAD khác).
- Python 3.8.20 (python-build-standalone qua `uv python install 3.8`, cài vào `~/rca/T-016/python`). Laptop dùng 3.8.10; khác bản vá.
- Gói: `results/T-016/requirements_py38_ec2.lock` = `results/T-006/requirements_rcd_khong_tigramite.lock` bỏ thêm dòng `torch==1.12.1`. Lý do bỏ `torch`: đường chạy TORAI/RCD không nạp `torch` (`runs/s11-goi-duoc-nap-laptop.txt`), còn bản Linux của torch 1.12.1 nặng khoảng 750 MB. `tigramite` bỏ như T-006.
- RCAEval cài `--no-deps -e`; 5 file vá chép từ `~/rca/T-016/src/RCAEval/lib/` đè vào site-packages (giữ `.orig`), như T-006 mục 3.
- `uv pip check`: "All installed packages are compatible". Danh sách gói: `~/rca/T-016/runs/freeze-py38-ec2.txt` (bản sao: `runs/s11-freeze-py38-ec2.txt`).
- Biến môi trường khi chạy (`scripts/chay_ec2.sh`): `OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=1`; `XDG_CACHE_HOME`, `MPLCONFIGDIR`, `TMPDIR`, `PYTHONPYCACHEPREFIX` trỏ vào `~/rca/T-016/`.

## 4. Dữ liệu và code ngoài repo

| Thứ | Nơi | Nguồn, kiểm |
|---|---|---|
| RCD gốc | `D:\RCA-ext\work\T-016\src\rcd` (18 MB) | `git clone https://github.com/azamikram/rcd`, checkout `373882c6982db7a999ec1ff99ea54c644a48b409` (kiểm `git rev-parse HEAD`) |
| 30 ca dev TT dạng torai | `D:\RCA-ext\work\T-016\data\torai-TT\` (150 file, 181 MB) | giải nén từ `D:\RCA-ext\dl\torai-data.zip` đúng 30 thư mục `torai-TT/<10 ô dev>/{1,2,3}`; chứng minh trùng ca dev: `runs/s10-cung-ca.json` |
| torai-OB, torai-SS, TT socket/1 trên EC2 | `~/rca/T-016/data/` | tar 22 030 452 B, SHA-256 `ff51e4cca56f4aae7d5ab76233dc3ddcae5d99d003f4bc2476d8af6254b507f4` khớp hai đầu |
| Bài TORAI (HTML), bài RCD (PDF chính, phụ lục) | thư mục tạm của phiên (không vào repo) | arXiv `2604.13522v1`; proceedings.neurips.cc (file `c9fcd02e6445c7dfbad6986abee53d0d`) |

Lấy lại 30 ca TT trên máy mới:

```
py -3 -c "import zipfile; z=zipfile.ZipFile(r'D:\RCA-ext\dl\torai-data.zip'); dev={'ts-auth-service_cpu','ts-auth-service_delay','ts-order-service_disk','ts-order-service_loss','ts-route-service_mem','ts-route-service_socket','ts-train-service_cpu','ts-train-service_delay','ts-travel-service_disk','ts-travel-service_loss'}; [z.extract(i, r'D:\RCA-ext\work\T-016\data') for i in z.infolist() if i.filename.split('/')[0]=='torai-TT' and len(i.filename.split('/'))>=4 and i.filename.split('/')[1] in dev and i.filename.split('/')[2] in ('1','2','3') and not i.filename.endswith('/')]"
```
