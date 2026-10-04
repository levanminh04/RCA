# T-006 — Dựng hai môi trường mới: `py312-pin`, `py38-rcdlock`

Dựng ngày 03/10/2026 trên laptop Windows 11, i5-1240P, RAM 16 GB. Mọi thứ nằm ở `D:\RCA-ext\`, ngoài repo. Ba môi trường của T-005 (`py312`, `py38-rcd`, `py38-gdn`) giữ nguyên, xem `results/T-005/moi-truong.md`.

Lệnh dưới đây chạy trong Git Bash, từ `D:\RCA-ext\`. Code RCAEval ở `src/RCAEval` revision `259ea41` (kiểm bằng `git rev-parse HEAD`).

Ghi chú: cài RCAEval ở chế độ editable (`-e`) ghi lại thư mục `src/RCAEval/RCAEval.egg-info` (siêu dữ liệu đóng gói, git bỏ qua). Không dòng code nào của tác giả bị sửa; `git -C src/RCAEval status --short` vẫn rỗng.

## 1. Công cụ: uv

```
py -3.12 -m venv envs/tools
envs/tools/Scripts/python.exe -m pip install uv          # uv 0.12.22
```

Lượt đầu hỏng: tải wheel uv bị cắt giữa chừng nên sai hash (`runs/11-cai-uv-py312-pin.log`). Chạy lại thì xong (`runs/11b-cai-uv-py312-pin-lan2.log`). uv chỉ nằm trong `envs/tools`, không cài vào Python hệ thống.

## 2. `py312-pin` — RCAEval `[default]`, chỉ bản phát hành trước 22/12/2024

Dùng cho: BARO, N-Sigma, CIRCA-PC, N-Sigma phát hiện (T-006); bộ thư viện đã chốt ở X1 (`x1-chot-moi-truong.md`).

```
envs/tools/Scripts/uv.exe venv --python 'C:\Users\84583\AppData\Local\Programs\Python\Python312\python.exe' envs/py312-pin
cd src/RCAEval
../../envs/tools/Scripts/uv.exe pip install --python ../../envs/py312-pin/Scripts/python.exe --exclude-newer 2024-12-22 -e ".[default]"
```

- 22/12/2024 là ngày nộp bài RCAEval (SPEC). Mọi gói đều có bản dựng sẵn trước ngày đó, nên **không dùng phương án dự phòng** của SPEC.
- Bản chính: Python 3.12.10; pandas 2.2.3; numpy 1.26.4; causal-learn 0.1.3.8; scikit-learn 1.6.0; scipy 1.14.1; statsmodels 0.14.4; networkx 2.5; torch 2.5.1; tigramite 5.2.7.0; pyagrum 1.17.2.
- `baro` (BOCPD, N-Sigma phát hiện, `reproduce_*`) lấy từ `src/baro` qua `sys.path`, không cài gói `fse-baro`, như T-005.
- Kiểm (`runs/12-kiem-py312-pin.log`): `uv pip check` sạch (174 gói); import `RCAEval.e2e` (có `baro`, `nsigma`, `circa`) và `baro.anomaly_detection`, `baro.root_cause_analysis`, `baro.reproducibility` được. Lượt import đầu lỗi vì mã hóa console (in chữ tiếng Việt); chạy lại với `PYTHONIOENCODING=utf-8` thì qua.
- Danh sách gói đầy đủ: `runs/freeze-py312-pin.txt`.

## 3. `py38-rcdlock` — chế độ RCD theo `docs/SETUP.md`, trừ `tigramite`

Dùng cho: L3 (RCD trên RE1-OB, mốc của `docs/SETUP.md`).

Theo `docs/SETUP.md`:

```
py -3.8 -m venv envs/py38-rcdlock
P=envs/py38-rcdlock/Scripts/python.exe
$P -m pip install pip==20.0.2
$P -m pip install wheel
cd src/RCAEval && ../../$P -m pip install -e ".[rcd]"      # hỏng ở tigramite, xem dưới
```

**Lệch so với `SETUP.md` (Minh duyệt 03/10/2026).** `tigramite==4.2.2.1` không có bản dựng sẵn cho Windows; dựng từ mã nguồn cần Microsoft C++ Build Tools, nên lệnh `-e ".[rcd]"` dừng ở gói này (`runs/10-cai-py38-rcdlock.log`). `tigramite` chỉ được import trong `RCAEval/e2e/easyrca.py`, `microcause.py`, `graph_construction/pcmci.py`; đường chạy RCD không dùng. Cách xử lý:

```
# requirements_rcd_khong_tigramite.lock = requirements_rcd.lock bỏ dòng tigramite==4.2.2.1 (lưu ở results/T-006/)
$P -m pip install -r <repo>/results/T-006/requirements_rcd_khong_tigramite.lock
cd src/RCAEval && ../../$P -m pip install --no-deps -e .
```

Log: `runs/10b-cai-py38-rcdlock-khong-tigramite.log`. File lock gốc dùng xuống dòng CRLF (git trên Windows), bản đã bỏ dòng dùng LF; ngoài dòng `tigramite`, nội dung giống nhau (`diff --strip-trailing-cr`).

**File vá.** `script/link.sh` tạo 5 symlink theo đường dẫn Linux. Trên Windows chép 5 file từ `src/RCAEval/lib/` đè vào site-packages, giữ bản gốc với đuôi `.orig` (`runs/13-va-py38-rcdlock.log`, có SHA-256 trước và sau):

```
SP=envs/py38-rcdlock/Lib/site-packages
cp src/RCAEval/lib/pyAgrum/lib/image.py                          $SP/pyAgrum/lib/
cp src/RCAEval/lib/causallearn/search/ConstraintBased/FCI.py     $SP/causallearn/search/ConstraintBased/
cp src/RCAEval/lib/causallearn/utils/Fas.py                      $SP/causallearn/utils/
cp src/RCAEval/lib/causallearn/utils/PCUtils/SkeletonDiscovery.py $SP/causallearn/utils/PCUtils/
cp src/RCAEval/lib/causallearn/graph/GraphClass.py               $SP/causallearn/graph/
```

**Kiểm theo yêu cầu của Minh** (`runs/14-kiem-py38-rcdlock.log`):
1. `pip freeze` so với `requirements_rcd.lock` gốc (170 gói): chỉ thiếu `tigramite`; không gói nào khác bản. Có thêm 8 gói phụ thuộc bắc cầu mà lock không ghim, pip tự cài: importlib-metadata 8.5.0, importlib-resources 6.4.5, ipython 8.12.3, matplotlib 3.7.5, matplotlib-inline 0.1.7, pywin32 311, xarray 2023.1.0, zipp 3.20.2. Danh sách đầy đủ: `runs/freeze-py38-rcdlock.txt`.
2. `pip check`: "No broken requirements found."
3. `main.py --method rcd --dataset online-boutique --test` chạy qua `scripts/main_kiem_module.py` (chạy `main.py` nguyên văn bằng `runpy`): sau khi chạy, `'tigramite' in sys.modules` = False; `causallearn.utils.PCUtils.SkeletonDiscovery` nạp từ bản đã vá trong site-packages (`runs/thu-rcdlock-rcd-online-boutique.tar.gz`).

Bản chính (giống `py38-rcd` của T-005): Python 3.8.10; causal-learn 0.1.2.3; numpy 1.23.5; pandas 2.0.1; scikit-learn 1.2.2; scipy 1.10.1; networkx 2.5; torch 1.12.1. Khác `py38-rcd`: lock đầy đủ của RCD (thêm dvc, pyagrum 1.8.0, torch, …) và 5 file vá thay vì 2.

## 4. Dữ liệu tải trong T-006

| Dữ liệu | Nguồn | Kích thước | Kiểm | Nơi để |
|---|---|---|---|---|
| `RE1-OB.zip`, `RE1-SS.zip` | Zenodo 14590730 | 30 966 778 B; 79 089 075 B | MD5 khớp API Zenodo | `dl/`, giải nén vào `data/RE1-OB`, `data/RE1-SS` |
| `fse-ob.zip`, `fse-ss.zip` | Zenodo 11046533 | 150 740 576 B; 126 610 585 B | MD5 khớp API Zenodo | `dl/`, giải nén vào `data/fse-ob`, `data/fse-ss` |
| `baro-simple_data.csv` | `github.com/phamquiluan/baro/releases/download/0.0.4/simple_data.csv` | 570 409 B | nguồn không công bố hash; SHA-256 ghi trong log | `dl/` |
| `torai-OB/`, `torai-SS/` | giải nén từ `dl/torai-data.zip` (T-005, MD5 khớp Figshare, kiểm lại) | 108 544 545 B; 112 789 403 B | 90 + 90 ca | `data/` |
| Đuôi 128 KB của `online-boutique.zip`, `sock-shop-2.zip` (Zenodo 13305663) | HTTP Range, chỉ mục lục zip | 2 × 131 072 B | dùng để so CRC-32 với RE1 | thư mục tạm của phiên, không giữ |

Lệnh tải: `scripts/tai_du_lieu.sh`; log: `runs/00-tai-du-lieu.log`. Giải nén: `scripts/giai_nen_torai.py`, `runs/01-…`, `runs/03-…`, `runs/04-…`. Không giải nén và không đọc gì trong `torai-TT` ngoài một ca T-005 đã có.

Lấy lại `torai-OB`, `torai-SS` từ zip:

```
py -3 <repo>/results/T-006/scripts/giai_nen_torai.py
```

## 5. Cách chạy các khối

- `scripts/chay_khoi.py`: một khối = một thư mục làm việc `work/T-006/<khối>/`, liên kết thư mục (junction) tới dữ liệu, `OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=1`, ghi tiến độ từng ca, RAM, giới hạn 3 giờ, nén vào `runs/<khối>.tar.gz`.
- `scripts/chay_luong.py <luồng> [--song-song N]`: chạy các khối của một luồng (L1, L2, L3, X1, L4, GDN).
- Chấm: `scripts/cham.py`, tổng hợp: `scripts/tong_hop.py` (ghi `cham/`).
