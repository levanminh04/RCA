# T-005 — Dựng lại ba môi trường chạy phương pháp

Dựng ngày 03/10/2026 trên laptop Windows 11, i5-1240P (16 luồng), RAM 16 GB, không GPU. Mọi thứ nằm ở `D:\RCA-ext\`, ngoài repo. Không chép code ngoài vào repo.

Mọi lệnh dưới đây chạy trong Git Bash, từ `D:\RCA-ext\`. Log của từng lượt cài ở `results/T-005/runs/`. Danh sách gói đầy đủ (pip freeze, không kể gói cài dạng editable) ở `runs/freeze-<môi trường>.txt`.

## 1. Python

| Bản | Nguồn | Kiểm |
|---|---|---|
| 3.12.10 | Có sẵn trên máy (`py -3.12`) | — |
| 3.8.10 | `https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe` (28 296 784 B) | MD5 khớp số python.org công bố qua API `release_file` |

Cài 3.8.10 cho riêng tài khoản người dùng, không thêm vào PATH, không đổi liên kết file:

```
python-3.8.10-amd64.exe /quiet InstallAllUsers=0 PrependPath=0 Include_launcher=0 AssociateFiles=0 Shortcuts=0 Include_test=0
```

Kiểm: `py -3.8 --version` in `Python 3.8.10`. Log: `runs/01-cai-python38.tar.gz`.

## 2. Code, đúng revision

```
git clone https://github.com/phamquiluan/RCAEval src/RCAEval && git -C src/RCAEval checkout 259ea4167160256a74ad30004aa3d96a998c846e
git clone https://github.com/phamquiluan/baro    src/baro    && git -C src/baro    checkout e35f4ec1095e5cac891d52de9ad18a5b32a37ec8
git clone https://github.com/d-ailin/GDN         src/GDN     && git -C src/GDN     checkout 9853899da860682669a134e4af315d036aab4eca
```

Kiểm: `git -C <thư mục> rev-parse HEAD` khớp mục 9 của `results/T-001/danh-sach-phuong-phap.md`. Log: `runs/02-clone.log`.

**Không sửa dòng code nào** của ba repo. Hai chỗ GDN không chạy được nguyên trạng trên Windows được xử lý trong script đo (mục 6), không sửa code GDN.

## 3. Môi trường `py312` — RCAEval chế độ mặc định

Dùng cho: BARO, N-Sigma, CIRCA-PC, MicroRank, TraceRCA, BOCPD, N-Sigma phát hiện.

```
py -3.12 -m venv envs/py312
envs/py312/Scripts/python.exe -m pip install --upgrade pip
cd src/RCAEval && ../../envs/py312/Scripts/python.exe -m pip install -e ".[default]" && cd ../..
envs/py312/Scripts/python.exe -m pip install pyarrow psutil
```

- BOCPD và N-Sigma phát hiện lấy từ repo BARO bằng cách thêm `src/baro` vào `sys.path`; không cài gói `fse-baro`. RCAEval không có BOCPD.
- Lượt cài đầu bị dừng giữa chừng vì giới hạn chạy nền 10 phút đặt quá ngắn; chạy lại cùng lệnh thì xong (`runs/03-…`, `runs/03b-…`).
- Kiểm: `pip check` sạch; import `RCAEval.e2e` (baro, nsigma, circa, microrank, tracerca), `baro.anomaly_detection` (`runs/11-kiem-py312.log`).

**Lưu ý, chưa kiểm ảnh hưởng.** `requirements.txt` của RCAEval không ghim nhiều gói, nên pip lấy bản mới nhất ngày 03/10/2026: pandas 3.0.6, numpy 1.26.4, scikit-learn 1.7.2, causal-learn 0.1.4.8, torch 2.8.0+cpu. Pandas 3 đổi cách sao chép dữ liệu (copy-on-write) và kiểu chuỗi mặc định. README của RCAEval chạy thử với Python 3.12.12 nhưng không ghi bản pandas. Nếu P3 cần khớp số công bố của RCAEval, phải kiểm lại trên một ca có số công bố; nếu lệch, ghim pandas 2.x. Muốn dựng lại đúng bộ gói đã đo thì dùng `runs/freeze-py312.txt`.

## 4. Môi trường `py38-rcd` — RCD và TORAI

Theo `docs/TORAI.md` của RCAEval:

```
py -3.8 -m venv envs/py38-rcd
envs/py38-rcd/Scripts/python.exe -m pip install --upgrade pip
cd src/RCAEval
../../envs/py38-rcd/Scripts/python.exe -m pip install -r requirements_torai.lock
../../envs/py38-rcd/Scripts/python.exe -m pip install -e .
cd ../..
```

**File vá.** `script/link-torai.sh` tạo symlink theo đường dẫn Linux. Trên Windows chép tay 2 file từ `src/RCAEval/lib/` vào site-packages (Minh duyệt 03/10/2026, thay cho 5 file của `link.sh` ghi trong SPEC):

```
SP=envs/py38-rcd/Lib/site-packages
cp src/RCAEval/lib/causallearn/utils/PCUtils/SkeletonDiscovery.py $SP/causallearn/utils/PCUtils/
cp src/RCAEval/lib/causallearn/graph/GraphClass.py                $SP/causallearn/graph/
```

Vì sao 2 file, không phải 5: `requirements_torai.lock` không có pyAgrum nên `pyAgrum/lib/image.py` không có chỗ chép; `FCI.py`, `Fas.py` chỉ dùng cho FCI, RCD và TORAI không import. Bản gốc của 2 file được giữ cạnh đó với đuôi `.orig`. Hash trước và sau khi chép ở `runs/09-va-py38-rcd.log`.

Kiểm: `pip check` sạch; `from RCAEval.e2e import rcd, torai` chạy được và `SkeletonDiscovery` nạp từ bản vá (`runs/09-va-py38-rcd.log`).

## 5. Môi trường `py38-gdn` — GDN

Theo `install.sh` của GDN, đổi bản CUDA 10.2 thành bản CPU:

```
py -3.8 -m venv envs/py38-gdn
P=envs/py38-gdn/Scripts/python.exe
$P -m pip install --upgrade pip
$P -m pip install "torch==1.5.1+cpu" -f https://download.pytorch.org/whl/torch_stable.html
$P -m pip install --no-index torch-scatter     -f https://data.pyg.org/whl/torch-1.5.0+cpu.html
$P -m pip install --no-index torch-cluster     -f https://data.pyg.org/whl/torch-1.5.0+cpu.html
$P -m pip install --no-index torch-spline-conv -f https://data.pyg.org/whl/torch-1.5.0+cpu.html
$P -m pip install torch-geometric==1.5.0 "numpy<1.20"
$P -m pip install --no-index torch-sparse      -f https://data.pyg.org/whl/torch-1.5.0+cpu.html
$P -m pip install googledrivedownloader==0.4
```

Bản đã cài: torch 1.5.1+cpu, torch-scatter 2.0.5, torch-sparse 0.6.7, torch-cluster 1.5.7, torch-spline-conv 1.2.0, torch-geometric 1.5.0, numpy 1.19.5. Đây là bản mới nhất trong kho `torch-1.5.0+cpu` của PyG, đúng nghĩa lệnh `--no-index -f` trong `install.sh`.

Hai chỗ phải xử lý, theo thứ tự đã gặp:
1. `torch-sparse` cần scipy, mà `--no-index` không cho tải scipy từ PyPI. Cách xử lý: cài torch-sparse **sau** torch-geometric (lúc đó scipy đã có). Lượt hỏng: `runs/07-cai-py38-gdn.log`; lượt sửa: `runs/07b-…`.
2. torch-geometric 1.5.0 import module `google_drive_downloader`; pip kéo về `googledrivedownloader` 1.1.0, bản này đã đổi tên module. Cách xử lý: hạ về 0.4. Lượt hỏng: `runs/10-…`; lượt sửa: `runs/10b-…`.

Kiểm: `pip check` sạch; import `torch`, `torch_geometric` và các module của GDN (`models.GDN`, `train`, `test`, `evaluate`) từ thư mục `src/GDN` (`runs/10b-…`). Không phải dùng phương án dự phòng (torch/PyG đời mới) của SPEC.

## 6. Hai chỗ GDN không chạy nguyên trạng trên Windows (xử lý trong script, không sửa code GDN)

- `Main.get_save_path` đặt tên file theo mẫu `'%m|%d-%H:%M:%S'`; ký tự `|` và `:` không hợp lệ trong tên file Windows. Script đo (`scripts/chay_mot_luot.py`) gọi thẳng `train()` và `test()` với đường dẫn mô hình riêng, nên không đi qua hàm này.
- `test.csv` bắt buộc có cột `attack` (nhãn 0/1). Script chuẩn bị dữ liệu đặt toàn 0; đây không phải nhãn và không tính F1 (Minh duyệt 03/10/2026).

## 7. Dữ liệu đã tải

| Dữ liệu | Nguồn | Kích thước | Kiểm | Nơi để |
|---|---|---|---|---|
| `torai-data.zip` | Figshare article 31925976, file 63402423, `https://ndownloader.figshare.com/files/63402423` | 91 262 227 B | MD5 khớp `supplied_md5` của Figshare (`runs/04-tai-torai-zip.log`) | `D:\RCA-ext\dl\` |
| Một ca giải nén từ zip trên | `torai-TT/ts-route-service_socket/1/` (5 file) | khoảng 6,4 MB | chỉ giải nén đúng thư mục này (`runs/05-liet-ke-zip.log`); trùng ca dev `re2tt_ts-route-service_socket_1` đã được chứng minh ở T-016 (`results/T-016/runs/s0-cung-ca.json`) | `D:\RCA-ext\data\` |
| `inject_time.txt` của 6 ca RCAEval | HF `phamquiluan/RCAEval`, revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`, đường dẫn `<ca>/inject_time.txt` | 10 B mỗi file | git blob oid khớp HF (file nhỏ không qua LFS nên HF không công bố SHA-256) (`runs/08-tai-inject-time.log`) | `D:\RCA-ext\dl\rcaeval-inject\` |

Zip TORAI chứa cả các ca đang khóa. Chỉ đọc danh sách tên mục để tìm đúng ca; không giải nén và không đọc ca khác.

Lấy lại một ca từ zip:

```
py -3 -c "import zipfile; z=zipfile.ZipFile('dl/torai-data.zip'); [z.extract(i,'data') for i in z.namelist() if i.startswith('torai-TT/ts-route-service_socket/1/') and not i.endswith('/')]"
```

## 8. Chạy lại phép đo

```
envs/py312/Scripts/python.exe <repo>/results/T-005/scripts/chuan_bi_dau_vao.py
envs/py312/Scripts/python.exe <repo>/results/T-005/scripts/do.py baro:win baro:full ...
```

`chuan_bi_dau_vao.py` ghi đầu vào đã cắt ra `D:\RCA-ext\work\T-005\` (khoảng 126 MB). `do.py` nhận danh sách `<mục>:<win|full>`; các mục có trong biến `MUC_ENV` của script.

## 9. Dung lượng

| Thư mục | Dung lượng |
|---|---|
| `envs/py312` | 2,4 GB |
| `envs/py38-gdn` | 1,1 GB |
| `envs/py38-rcd` | 424 MB |
| `src` | 19 MB |
| `dl` (bộ cài Python, zip TORAI, 6 file mốc tiêm) | 115 MB |
| `data` (một ca TORAI) | 6,2 MB |
| `work` (đầu vào đã cắt, mô hình GDN, thứ hạng chưa đọc) | 126 MB |
| **Tổng** | khoảng 4,2 GB |

Nguồn: `runs/13-dung-luong.log`. Vượt ước lượng 2–3 GB của SPEC, chủ yếu do `py312` (torch 2.8 và các gói của RCAEval).
