# T-007 — Dựng môi trường trên EC2

Dựng ngày 03/10/2026. Đủ để dựng lại từ một máy Ubuntu 24.04 trắng. Mọi thứ nằm trong `~/rca/`, trừ gói hệ thống cài bằng apt. Không có dữ liệu khóa nào trên máy (Q-42).

## 1. Máy

| Mục | Giá trị |
|---|---|
| Loại | EC2 m7i-flex.large (Q-42), vùng ap-southeast-2 |
| Hệ điều hành | Ubuntu 24.04.4 LTS, x86_64, Python 3.12.3 có sẵn |
| CPU, RAM | 2 vCPU (Xeon Platinum 8488C, 1 lõi × 2 luồng), 7,6 GiB, không có swap |
| Đĩa | 29 GB |
| Múi giờ | UTC |

Kết nối từ laptop (Windows, OpenSSH có sẵn):

```
C:\Windows\System32\OpenSSH\ssh.exe -i D:\RCA-ext\keys\keys.pem -o UserKnownHostsFile=D:\RCA-ext\keys\known_hosts ubuntu@<địa chỉ IP>
```

Địa chỉ IP đổi sau mỗi lần Stop/Start. Lần dựng này: `3.104.124.160`.

## 2. Dựng môi trường (E0)

**Bước 0 — tạo thư mục và chép script** (phải làm trước E0, E1, vì lệnh `nohup ... > ~/rca/runs/...` mở file log trước khi script chạy; phiên 1 đã chạy các lệnh này tay qua SSH):

```
ssh -i D:\RCA-ext\keys\keys.pem -o UserKnownHostsFile=D:\RCA-ext\keys\known_hosts ubuntu@<IP> "mkdir -p ~/rca/scripts ~/rca/runs/e0 ~/rca/runs/e1 ~/rca/runs/thu"
scp -i D:\RCA-ext\keys\keys.pem -o UserKnownHostsFile=D:\RCA-ext\keys\known_hosts results/T-007/scripts/* ubuntu@<IP>:rca/scripts/
```

Nếu script mang ký tự xuống dòng Windows, chạy thêm trên EC2: `sed -i "s/\r$//" ~/rca/scripts/*.sh ~/rca/scripts/*.py`.

Rồi chạy E0:

```
mkdir -p ~/rca/runs/e0 && nohup bash ~/rca/scripts/e0_dung_moi_truong.sh > ~/rca/runs/e0/e0.log 2>&1 &
```

Script làm theo thứ tự:

1. `apt-get install build-essential libxml2 libxml2-dev zlib1g-dev python3-tk graphviz python3.12-venv` (gói theo README RCAEval, thêm `python3.12-venv`).
2. Clone RCAEval, BARO và checkout đúng revision mục 9 của `results/T-001/danh-sach-phuong-phap.md`: RCAEval `259ea4167160256a74ad30004aa3d96a998c846e`, BARO `e35f4ec1095e5cac891d52de9ad18a5b32a37ec8`. Script dừng nếu `git rev-parse HEAD` không khớp.
3. uv trong môi trường riêng `~/rca/envs/tools` (`pip install uv`, ra uv 0.12.22).
4. `py312`: `python3 -m venv`, `pip install -e ".[default]"` trong thư mục RCAEval, thêm `pyarrow psutil` (như `py312` của T-005 trên laptop). Bản mới nhất ngày 03/10/2026.
5. `py312-pin`: `uv pip install --exclude-newer 2024-12-22 -e "RCAEval[default]" pyarrow psutil` (cách của SPEC T-006). Cài được trọn, không phải dùng phương án dự phòng.
6. `pip check` và import thử `RCAEval.e2e.microrank`, `RCAEval.e2e.tracerca`, `baro.anomaly_detection`, `baro.reproducibility` ở cả hai môi trường; ghi `pip freeze --exclude-editable`.

Biến môi trường để không ghi ra ngoài `~/rca`: `XDG_CACHE_HOME`, `PIP_CACHE_DIR`, `UV_CACHE_DIR`, `MPLCONFIGDIR`, `TMPDIR` đều trỏ vào `~/rca/cache` hoặc `~/rca/tmp`. pip chạy `--no-cache-dir`, uv chạy `--no-cache`.

BARO không cài thành gói (`fse-baro`); code BARO lấy từ repo bằng cách thêm `~/rca/src/baro` vào `sys.path`, như T-005.

### Phiên bản các thư viện chính

| Gói | `py312` | `py312-pin` |
|---|---|---|
| Python | 3.12.3 | 3.12.3 |
| pandas | 3.0.6 | 2.2.3 |
| numpy | 1.26.4 | 1.26.4 |
| scipy | 1.17.1 | 1.14.1 |
| scikit-learn | 1.7.2 | 1.6.0 |
| causal-learn | 0.1.4.8 | 0.1.3.8 |
| pyarrow | 25.0.1 | 18.1.0 |
| torch | 2.8.0+cu128 | 2.5.1+cu124 |
| tqdm | 4.65.0 | 4.65.0 |
| matplotlib | 3.11.2 | 3.10.0 |

Danh sách đầy đủ: `runs/e0/freeze-py312.txt` (192 gói), `runs/e0/freeze-py312-pin.txt` (186 gói). Log: `runs/e0/e0.log`.

Lưu ý:
- pip trên Linux lấy torch bản CUDA (kéo theo các gói `nvidia-*`), nên `py312` nặng 7,6 GB, `py312-pin` 5,9 GB. MicroRank, TraceRCA, BOCPD không dùng torch.
- `--exclude-newer 2024-12-22` là ngày theo múi giờ máy. EC2 chạy UTC nên mốc là 22/12/2024 00:00 UTC; trên laptop (UTC+7) cùng lệnh cho mốc 21/12/2024 17:00 UTC.
- **So với `py312-pin` của T-006 trên laptop** (`results/T-006/runs/freeze-py312-pin.txt`, 173 gói): mọi gói có ở cả hai máy đều cùng phiên bản, kể cả torch 2.5.1. Khác nhau chỉ ở gói riêng của từng hệ điều hành (`nvidia-*`, `triton` chỉ có trên Linux; `pywin32` chỉ có trên Windows), cách viết tên (`flufl.lock` / `flufl-lock`, `ruamel.yaml` / `ruamel-yaml`, `zc.lockfile` / `zc-lockfile`), và `pyarrow` (chỉ EC2 cài, để đọc parquet). Tức lệch múi giờ ở trên không đổi bản gói nào.

## 3. Tải dữ liệu (E1)

```
mkdir -p ~/rca/runs/e1 && nohup python3 ~/rca/scripts/e1_tai_du_lieu.py > ~/rca/runs/e1/e1.log 2>&1 &
```

Chỉ dùng thư viện chuẩn của Python hệ thống.

| Dữ liệu | Nguồn | Cách kiểm | Kết quả | Nơi để |
|---|---|---|---|---|
| RE2-OB: `traces.parquet`, `inject_time.txt` của 90 ca `re2ob_*` | Hugging Face `phamquiluan/RCAEval`, revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e` | SHA-256 do HF công bố (file LFS); git blob oid (file nhỏ) | 180/180 file khớp, 879,3 MB | `~/rca/data/re2ob/<ca>/` |
| `fse-ob.zip` | Zenodo 11046533 | MD5 do Zenodo công bố | khớp, 150 740 576 B; 100 ca × 12 file | `~/rca/data/fse/fse-ob/` |

- Danh sách ca RE2-OB lấy từ cây thư mục gốc của repo HF ở đúng revision, lọc ngay tiền tố `re2ob_`. Tên các ca khác (có ca RE2-TT đang khóa) không lưu, không in. Không tải `cases.parquet`.
- Hash từng file: `runs/e1/manifest-re2ob.json`, `runs/e1/manifest-fse-ob.json`.

## 4. Chạy và chấm

| Việc | Lệnh |
|---|---|
| Chạy thử đường ống (2 ca trace, 1 ca BOCPD, cả hai môi trường) | `bash ~/rca/scripts/thu_duong_ong.sh` |
| E2 + E3 cho một môi trường | `nohup bash ~/rca/scripts/chay_e2_e3.sh <py312-pin\|py312> > ~/rca/runs/chay-<env>.log 2>&1 &` |
| Chấm một thư mục kết quả | `<env>/bin/python ~/rca/scripts/cham.py <thư mục results> --json <file>` |
| So mốc | `python so_moc.py moc-torai-bang2-trace.json MicroRank=<cham.json> TraceRCA=<cham.json>` |
| Trích mốc từ bài TORAI | `curl -sL -o torai.html https://arxiv.org/html/2604.13522v1 && py -3 trich_moc.py torai.html moc-torai-bang2-trace.json` |
| Phép kiểm thêm (phiên 2): soi trung gian MicroRank, xáo thứ tự span | `nohup bash ~/rca/scripts/chay_kiem_them.sh > ~/rca/runs/kiem-them.log 2>&1 &` (bước 1 của lượt đã chạy hỏng; chạy lại bằng `chay_trung_gian_lai.sh`) |
| Hòa điểm và sắp xếp NaN của TraceRCA | `<env>/bin/python ~/rca/scripts/hoa_diem_tracerca.py --out <jsonl>`; phân tích trên laptop: `py -3 phan_tich_sap_xep_tracerca.py <jsonl> moc-torai-bang2-trace.json` |
| Biến thể cửa sổ ±600 s | `nohup bash ~/rca/scripts/chay_l20.sh > ~/rca/runs/chay-l20.log 2>&1 &` (gồm kiểm hồi quy với mặc định) |
| Biên file so với mốc tiêm | `<env>/bin/python ~/rca/scripts/bien_file.py --out <json>` |
| Thống kê cho báo cáo (laptop, đọc `runs/*.tar.gz`) | `py -3 results/T-007/scripts/thong_ke.py` → `cham/thong-ke.json` |

- `chay_e2_e3.sh` ghi vào `~/rca/work/<env>/<khối>/` và nén mỗi khối vào `~/rca/runs/<env>/<khối>.tar.gz` ngay khi xong.
- `chay_e2.py` có hai tùy chọn thêm ở phiên 2: `--length <phút>` (mặc định 10, tức ±300 s) và `--tron <seed>` (mặc định không xáo). Mặc định cho kết quả giống từng byte bản cũ (kiểm hồi quy 6/6 ca).
- Bản `chay_e2_e3.sh`, `chay_kiem_them.sh` đã chạy in dòng "mã thoát" luôn bằng 0 (lỗi ghi log, `$(ts)` đặt lại `$?`); bản trong repo đã sửa bằng `rc=$?`. Kết quả không bị ảnh hưởng.
- Khối `bocpd.tar.gz` chứa liên kết `data` → `~/rca/data/fse`; giải nén trên Windows dùng `--exclude=bocpd/data`.
- Python trên EC2: biến `XDG_CACHE_HOME`, `MPLCONFIGDIR`, `TMPDIR` đặt vào `~/rca/...` cho mọi lượt, để không ghi ra ngoài `~/rca`.

## 5. Dung lượng trên EC2 (cuối phiên 2, 03/10/2026)

| Thư mục | Dung lượng |
|---|---|
| `envs/py312` | 7,6 GB |
| `envs/py312-pin` | 5,9 GB |
| `envs/tools` | 63 MB |
| `src` | 18 MB |
| `data/fse` (zip + giải nén) | 621 MB |
| `data/re2ob` | 840 MB |
| `work` | 16 MB |
| `runs` | 912 KB |
| `cache`, `tmp` | 1,9 MB |
| **Tổng `~/rca`** | **15 GB** |

Đĩa còn trống 11 GB trên 29 GB. Mọi file trong `~/rca/runs` (34 file) đã chép về `results/T-007/runs/`, SHA-256 trùng từng file.

Tác dụng phụ ngoài `~/rca`: file rỗng `~/.sudo_as_admin_successful` (06:40 UTC), Ubuntu tự tạo khi `sudo` chạy lần đầu (lệnh `apt-get` ở E0). Ngoài ra chỉ có các gói hệ thống của E0.
