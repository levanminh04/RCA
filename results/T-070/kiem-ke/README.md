# Kiểm kê chỉ đọc trước khi dọn (T-070, slot S7)

Ngày 24/11/2026, 10:45–11:20Z. Người làm: Claude (phiên kiểm kê do phiên điều phối T-070 mở). Minh duyệt "kiểm kê chỉ đọc" ngày 24/11.

Phạm vi: ba máy (exp-obs, exp-app, máy tải), repo lab `D:/Project/flashticket-rca-lab` (main `4b6c4b2`), repo RCA `D:/RCA-flashticket` (HEAD `74b2515d8` lúc kiểm).
Không sửa gì trên máy và trong repo, ngoài thư mục này. Không đọc nội dung `.env`, `grafana.env`, `secrets/`, `~/.ssh`, `~/.bash_history`. Không truy vấn Prometheus/Loki/Tempo. Không mở `data/locked/`.
Tài liệu này chỉ ghi dữ kiện và rủi ro. **Không đề xuất cấu trúc mới.**

## Cách đọc

| File | Nội dung |
|---|---|
| `may-thu-muc.tsv` | Thư mục trên ba máy: chủ, quyền, dung lượng (`du`) |
| `may-container.tsv` | Container: image, compose project, file compose, env file, mount |
| `may-tien-trinh-cron-unit.tsv` | Tiến trình dài, cron, unit/timer tự tạo |
| `may-git.tsv` | Mọi checkout git trên máy: HEAD, trạng thái |
| `may-dia.tsv` | Dung lượng đĩa |
| `duong-dan-ai-dung.tsv` | **Đường dẫn → ai dùng** (container, unit, cron, script, dashboard) kèm bằng chứng |
| `lab-file.tsv` | 129 file git của repo lab: vai trò, nơi dùng, bản trên từng máy, đường dẫn viết cứng, file tham chiếu, mã task trong tên |
| `lab-dashboard.tsv` | Dashboard: UID, provider, thư mục Grafana, datasource, URL đọc dữ liệu, liên kết |
| `lab-luat-canh-bao.tsv` | Luật cảnh báo và contact point: UID, file nguồn, nơi UID được dùng |
| `lab-nhanh-commit.tsv` | Nhánh, worktree, commit ngoài `main` được dẫn trong hồ sơ |
| `rca-chua-track-theo-thu-muc.tsv` | File chưa đưa vào git của repo RCA, theo thư mục: số file, MB, loại a/b/c, có trong manifest, khớp hash kho |
| `rca-chua-track-chi-tiet.tsv.gz` | Như trên, từng file (70.570 dòng) |
| `rca-duong-dan-cung.tsv` | File trong `src/` và `results/` (py/sh/ps1, đã track) viết cứng đường dẫn máy hoặc lab |
| `rca-file-dang-sua.txt` | File đã track đang sửa chưa commit |
| `m1-ban-chup.tsv` | Bản chụp M1 trên exp-obs: từng file, so với cây làm việc, HEAD và commit `25550d2a5` |
| `tho/<máy>/` | Đầu ra thô của lệnh, theo máy. `tho/lenh/` là chính các script đã chạy; `tho/laptop/` là đầu ra phía laptop |

Lệnh SSH: `tho/lenh/ssh.sh <app|obs|tai> < script` (khóa ở `D:/RCA-ext/keys/`, không chép vào đây). Mỗi script `p1.sh`–`p6*.sh` chỉ gồm lệnh đọc trong danh sách được phép (thêm `getent`, `ss -tln`, `sha256sum`, `pgrep`, đọc `/proc/<pid>/cmdline`: đều chỉ đọc). Đường dẫn khóa trong dòng lệnh `ssh` của exp-app đã được thay bằng `<key-path>` ở `p4-app.txt`; ở `p2-app.txt` còn đường dẫn file khóa, không có nội dung khóa.

## 1. Ba máy — đã thấy

Lệnh: `tho/lenh/p1.sh`, `p2.sh`, `p3.sh` trên cả ba máy; `p4app.sh`, `p5app.sh` (exp-app); `p6obs.sh`, `p6tai.sh`.

### exp-obs (213.35.116.128)

- Đĩa: 59/135 GB (44%). Docker volume 21,33 GB (4 volume `flash-ticket-obs-pinned_*`).
- `/srv/rca-lab` 14 GB: `collector-gateway` 5,1 GB (53 file vòng: traces 21, metrics 21, logs 11; cấu hình vòng 100 MB × 10–20 nên có trần), `load-controller/tai-out` 3,5 GB (47 tag), `trace-goi` 2,0 GB, `rca-results` 1,4 GB, `runs` 1,3 GB (29 thư mục con, 28 mang mã task), `venv-m1` 451 MB, `m1-snapshots` 1,3 MB.
- Thư mục cách ly: `/srv/rca-lab/m1` root:rca 750, `/srv/rca-lab/ledger` ledger 700, `/var/lib/flash-ticket-ledger` ledger 750, `/srv/rca-lab/runs` và `load-controller` ubuntu 700, `/etc/rca-lab/controller` ubuntu 700, `/etc/rca-lab/grafana.env` và `credential-hash-catalog.json` root 600.
- 6 container: 5 của project `flash-ticket-obs-pinned` (`/opt/rca-lab/observability/compose.yaml`, env file `/opt/rca-lab/inventory/oracle-exp.env`) và `flash-ticket-t072-bo-nhan` của project `t073-webhook` (`compose.t073-webhook.yaml`, env file `/srv/rca-lab/runs/t072-e3-01-cfg/webhook.env`).
- **`t072-bo-nhan` còn chạy** (từ 22/11 05:16Z, healthy), ghi `/srv/rca-lab/runs/t072-e3-01/webhook.jsonl` (sửa lần cuối 23/11 02:33Z).
- Không cron, không unit/timer tự tạo, không tmux/screen. Không tiến trình RCA nào ngoài container (bộ điều phối (b) đã dừng).
- Git: chỉ `/opt/rca-lab` @`1bb40ca` (detached, sạch; bỏ qua `__pycache__` theo `.gitignore`).
- `/home/ubuntu` chỉ có `t063/` 8 KB. Không còn `/opt/flash-ticket-rca`, `/opt/rca-m1ft`, `/opt/flash-ticket-obs`, `~/rca-dieu-phoi` (các đường cũ vẫn được nhắc trong mã, xem rủi ro R15).
- Python hệ thống có PyYAML 6.0.1 (tai_linux.py cần).

### exp-app (129.221.208.47)

- Đĩa: 27/48 GB (55%). Image Docker 39 cái, 10,06 GB (4,5 GB không dùng theo `docker system df`); build cache 7,86 GB.
- 14 container: 7 service FlashTicket image `ft-local/*:arm64-t067-36a3725d`, mỗi service một project, file compose `/opt/flash-ticket-build/t067-compose/hieu-luc/<svc>.yml`, env file `/opt/flash-ticket-app/env-t062/<svc>.env`; Keycloak từ `/opt/flash-ticket-app/compose-exp/keycloak.yml`; hạ tầng `flash-ticket-infra` (5 file compose ở `/opt/flash-ticket-infra/deploy/`, env `/opt/flash-ticket-infra/.env`); Collector agent `flash-ticket-collector` từ `/opt/rca-lab/observability/collector/agent-compose.yaml`; `rca-toxiproxy` tạo bằng `docker run` (không compose, nhãn `t062=topology`).
- **Ba tiến trình trần ppid 1 từ 13/11 02:54–02:55Z, không unit, không cron**: `tunnel-supervisor.py`, `ssh -R 127.0.0.1:19091:127.0.0.1:19090 ubuntu@3.24.8.49`, `mock-runner.py` (VNPay giả), cùng ở `/opt/flash-ticket-app/l1-vnpay/`.
- 16 checkout git, tất cả sạch: `/opt/flash-ticket-src` (repo chính, có `.git/worktrees`), 14 thư mục ở `/opt/flash-ticket-build/` (7 theo tên service ở commit cũ 08–11/11, `t062-*`, `t063-h3`, `t067-36a3725d`, `t067-dc-*`), `/opt/rca-lab` @`407b4f5` (khác exp-obs).
- `/opt/flash-ticket-build` 2,9 GB; `/opt/flash-ticket-app` 1,4 GB (trong đó `collector/data` 1,3 GB, file mới nhất 18/11 06:56Z, không container nào gắn); `/srv/rca-lab/collector-agent` 1,3 GB (vòng 50 MB × 5 log, 100 MB × 10 trace).
- `/home/ubuntu`: `t058` 3,8 MB, `t062`, `t063` (gồm `t063/inj` là trạng thái của inj3.py), `t071` 86 MB (`db-moc`), các script `*-t062.*`, `inj*.py`, `.m2` 435 MB.
- Không cron, không unit tự tạo.

### Máy tải AWS (3.24.8.49)

- Đĩa: 11/48 GB (22%).
- `/srv/rca-lab/load-runs` 3,5 GB, 47 tag (cùng danh sách 47 tag với `exp-obs:/srv/rca-lab/load-controller/tai-out`); `/opt/rca-tai` 2,1 GB (hệ tải cũ; `out/` 56 thư mục, cùng 56 thư mục trong `D:/RCA-archive/load-generator`); `/etc/rca-lab/load-secret` ubuntu 700 (3 file, chỉ liệt kê tên).
- Cổng `127.0.0.1:19091` đang nghe (đầu nhận đường hầm từ exp-app).
- Git: `/opt/rca-lab` @`5a39028` (sạch). Không thấy mã nào dùng `/opt/rca-lab` trên máy này.
- Không cron, không unit tự tạo, 0 `containerd-shim` (không container đang chạy).

Bảng đầy đủ đường dẫn → người dùng: `duong-dan-ai-dung.tsv` (50 dòng).

## 2. Repo lab — đã thấy

Lệnh: `git ls-files`, `git ls-tree -r <commit>`, `git branch -a -vv`, `git worktree list`, `tho/lenh/lab_files.py`, so `sha256sum` hai đầu (`p5app.sh`).

- 129 file git. 25 file có mã task trong tên (`t062`, `t065`, `t066`, `t069`, `t072`, `t073`; danh sách ở `lab-file.tsv` cột 2); thêm `campaigns/g1/l8b-xuat.py` mang mã lượt `l8b`.
- Bản trên máy: exp-obs `1bb40ca` (mọi file trùng `main` trừ `README.md`); exp-app `407b4f5` (không có `campaigns/online/`, `alerting/`, `chuoi_tai.py`, `t072-bo-nhan/`; `build_dashboards.py` khác); máy tải `5a39028`.
- File chạy ngoài `/opt/rca-lab` nhưng trùng hash với repo lab: `faults/mocks/vnpay/*.py` = bản đang chạy ở `/opt/flash-ticket-app/l1-vnpay/`; `faults/toxiproxy/proxies.json` = bản gắn vào `rca-toxiproxy`; `app-host/overrides/*`, `app-host/scripts/hieu_luc.py`, `deploy.sh` = bản ở `/opt/flash-ticket-build/t067-compose/`; `app-host/infra/docker-compose.rca-log.yml` = bản của `flash-ticket-infra`.
- `app-host/services/*.yml` trùng `/opt/flash-ticket-app/compose-t062/` (bản trước T-067), **không** phải file của 7 service đang chạy. Các file đang chạy (`t067-compose/hieu-luc/*.yml`) không có trong repo lab; chúng được sinh bởi `hieu_luc.py` (có `SHA256SUMS`, `so-sanh.json` trên máy). `app-host/services/keycloak.yml` khác hash với `compose-exp/keycloak.yml` đang chạy. `app-host/README.md` còn ghi image `arm64-t062-6b21ed55` (đã cũ).
- `tunnel-supervisor.py` đang chạy trên exp-app không có trong repo lab.
- `rca-service/` và `provisioning/` chỉ có `README.md` (ghi "chưa làm").
- Dashboard (`lab-dashboard.tsv`): 4 dashboard hiện qua 4 provider (`rca-bat-dau`, `rca-he-thong`, `rca-su-co`, `rca-phat-lai`); 3/4 có UID mang mã task (`t065-l5-muc-luc`, `t065-l8b-rca`, `t065-l8b-phat-lai`) và đọc Infinity `infinity-rca` từ `http://localhost:3000/public/rca/t065-l11-001/...`; `flashticket-he-thong` đọc `prometheus`, `tempo`, `loki`. 6 dashboard `90-archive` gắn vào container nhưng không provider nào quét.
- Luật cảnh báo (`lab-luat-canh-bao.tsv`): 11 luật `t072-*` nhóm `t072-w4`, folder Grafana "T-072 W4 cảnh báo", contact point `t072-webhook` → `http://t072-bo-nhan:9172/t072`. Hai file `*-go.yaml` là lệnh xóa, chạy mỗi lần Grafana khởi động. `campaigns/online/incidents.py` không viết cứng UID; dùng nhãn `__alert_rule_uid__`/`alertname`. UID `t072-*` xuất hiện trong 382 file đã track của repo RCA (`results/T-072` 322).
- Nhánh (`lab-nhanh-commit.tsv`): 8 nhánh local, 6 trên origin, 0 tag; 7 worktree ở `D:/Project/rca-lab-wt/`. **Commit duy nhất ngoài `main`: `779f90c` (nhánh `t073-e5-p`)**, được dẫn trong `results/T-070/codex/CX-21-tin-cuoi.md`, `results/T-073/e5/s47b-*.txt`, `tasks/T-070…/LICH-MAY.md`, `TRANG-THAI.json`. Worktree `T-072`, `T-073` có file chưa track; nội dung trùng `main` hoặc trùng commit N `d677244` (đã đối chiếu hash).

## 3. Repo RCA — đã thấy

Lệnh: `git ls-files -o --exclude-standard -z` (`tho/lenh/rca_untracked.py`, kết quả `tho/laptop/rca-git-ls-files-o.tsv.gz`), phân loại `tho/lenh/rca_classify.py`, `git grep`.

- **70.570 file chưa track, 17,09 GB** (lúc ~11:05Z; con số 70.723 trong đề bài là trước khi phiên khác commit `74b2515d8`). Không có file chưa track trong `results/T-066…T-068`, `T-071`, `T-072`, `T-074`, `T-075`.
- Phân loại máy móc (quy tắc trong `rca_classify.py`; không phải khuyến nghị commit):
  - (a) hồ sơ nhẹ (đuôi văn bản, < 1 MB, ngoài thư mục đầu ra chạy): 475 file, 36,4 MB. Nhiều nhất: `T-065/du-lieu` 154, `T-050/ec2-00{1,2}-download` 168, `T-073/e5` 42, `T-064/phien-c` 38, `T-058/dem-2026-11-10` 37.
  - (b) đầu ra chạy (≥ 1 MB, hoặc gz/tgz/jsonl, hoặc trong `runs/`, `ca/`, `thu2/`…): 64.346 file, 17,06 GB.
  - (c) tạm (`.lock`, `.pid`, `.partial-*`): 5.749 file, 0,6 MB (5.708 `.lock` ở `T-054/runs`).
- Theo task (MB): T-063 3.150, T-062 2.425, T-047 2.173, T-065 1.708, T-054 1.655, T-064 1.306, T-053 1.003, T-032 986, T-048 889, T-045 554, T-042 306, T-069 199, T-046 191, T-049 186, T-058 137 (đủ ở `rca-chua-track-theo-thu-muc.tsv`).
- Manifest: quét 1.509 file manifest (`SHA256SUMS*`, `*.sha256`, `manifest*.json`, `NEN-*.jsonl`) cả đã track lẫn chưa. Đầu ra (b) có đường dẫn nằm trong ít nhất một manifest: 15,42 GB; **không tìm thấy trong manifest: 1,64 GB**, chủ yếu `T-054/runs/chuan-bi-main-013-v2` 1.164 MB, `main-013-v2` 172 MB, `main-013` 96 MB, `T-062/ca/_metric-bo-sung` 102 MB, `T-058/dem-2026-11-10/rca-ban-dau` 25 MB, log `codex/` của T-062, T-065, T-070.
- Các manifest nén `results/T-045|047|048|049|053/NEN-2026-11-15.jsonl` vẫn chưa track. `results/T-065/manifest.json` (2,1 MB) chưa track.
- Kho `D:/RCA-archive` (7,2 GB): băm 2,61 GB file chưa track có cùng tên + cỡ với file trong kho → **679 file, 2.581 MB khớp hash** một danh sách của kho (`T-062/tai`, `T-062/tai-2`, `T-063/thu2`, `T-063/thu3`, `T-063/chay`, `T-064/bien-the` (khớp `m1ft-inputs`), `T-069/thu` 3 file); 539 file cùng tên + cỡ nhưng khác hash.
- Kho có hai nhóm chưa ghi trong `D:/RCA-archive/README.md`: `exp-obs/t066-nhom2/` (652 MB) và `T-069/raw-json/` (190 MB), mỗi nhóm có `SHA256SUMS` riêng.
- File đã track đang sửa: chỉ `tasks/T-070-dieu-phoi-giai-doan-2/LOG.md` (`rca-file-dang-sua.txt`). Danh sách sửa trong ảnh chụp đầu phiên (STATE, LICH-MAY, LOG T-072, T-074…) đã được phiên khác commit.
- `.gitignore` RCA: `data/*` (trừ README), `.venv/`, `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`, IDE, `*.parquet`, `*.zip`, `results/T-023/runs/stream-*/*.csv`. Không loại `*.gz`, `*.tgz`, `*.jsonl` (bản chép ở `tho/laptop/rca-gitignore.txt`). `.gitignore` lab loại `*.env` (trừ `inventory/*.env`), khóa, `runs/`, `out/`, `*.tgz`, `*.jsonl`.
- Đường dẫn viết cứng (`rca-duong-dan-cung.tsv`): 597 file py/sh/ps1 đã track trong `results/` nhắc đường máy/lab; **`src/` không có**. Nhiều nhất: `/home/ubuntu/rca*` (EC2 cũ của T-032…T-054), `/home/ubuntu/t058`, `rca-dieu-phoi`, `/opt/rca-tai/out`, `/srv/rca-lab/runs`, `/opt/flash-ticket-rca/venv`, `/opt/rca-lab`, `D:/Project/flashticket-rca-lab` (29), `rca-lab-wt` (24).

## 4. Lõi M1 trên máy — đã thấy

Lệnh: `find … | xargs sha256sum` trên exp-obs (`tho/exp-obs/m1-snapshot-obs.txt`), so với repo RCA (`m1-ban-chup.tsv`).

- Chỉ có một bản chụp: `/srv/rca-lab/m1-snapshots/b0f79a4dffd552f6e6026172b9058cd54ee9272475d927e35f19e22b04411b8d` (149 file: `src/m1`, `src/m1_ft`, `src/p3`, vài file `results/T-063`, `results/T-064`). Không có file pins hay `SHA256SUMS` trong thư mục.
- Tên thư mục là `ma_nguon_sha256` của T-064 (`results/T-064/cau-hinh-de-xuat-2.json`, `ban-xuat/chi-muc-ban*.json`), tính bởi `src/m1_ft/chay.py::sha_ma_nguon` (src/m1 + src/m1_ft, bỏ `tests`).
- 149/149 file trùng byte với **cây làm việc** hiện tại của repo RCA; tính lại `sha_ma_nguon` từ các byte đó ra đúng `b0f79a4d…`.
- 26/149 file **khác blob git** (cả HEAD lẫn `25550d2a5`) vì cây làm việc Windows dùng CRLF (`core.autocrlf=true`, `git ls-files --eol`: `i/lf w/crlf`); nội dung git là LF.
- `campaigns/runner/run_m1.py:18` và `stage_m1.py:17` viết cứng đường bản chụp này làm mặc định `RCA_M1_CODE`.
- exp-app và máy tải không có `m1-snapshots`.

## Chưa kiểm được

| Mục | Lý do |
|---|---|
| Container, image, volume trên máy tải | `ubuntu` không thuộc nhóm `docker`; `sudo docker` ngoài danh sách được phép. Chỉ biết 0 `containerd-shim` (không container đang chạy). Container đã dừng, image k6 trên máy tải: chưa biết |
| Dung lượng và danh sách file trong thư mục cách ly | Cần `sudo du/ls`: `/srv/rca-lab/m1`, `/srv/rca-lab/ledger`, `/var/lib/flash-ticket-ledger` (exp-obs); `/opt/flash-ticket-app/rca-faults`, `secrets/ticket-qr`, `/opt/flash-ticket-infra/{services,docs,keycloak}`, `/srv/rca-lab/backups/t067-20261118` (exp-app); `/var/lib/docker` |
| Cỡ từng Docker volume | Chỉ có tổng `docker system df` (obs 21,33 GB; app 1,70 GB); `docker system df -v` ngoài danh sách |
| Trạng thái sống của Grafana (luật đã nạp, dashboard tạo trên giao diện, folder UID của "T-072 W4 cảnh báo") | Đọc `alert_rule` cần sudo vào volume hoặc `docker exec`, ngoài danh sách; bảng dashboard không được phép đọc. Bảng ở đây dựa trên file provisioning. STATE ghi E5 hoàn tác: 11 luật trùng |
| Quy tắc `sudo -u ledger` | `/etc/sudoers.d` không liệt kê được (thiếu quyền) |
| `results/T-051/fixtures-tmp-002/` | `git` báo Permission denied trên laptop; không nằm trong danh sách chưa track |
| 315 chuỗi hex gần chữ "lab/commit" trong hồ sơ không phân giải được ở cả 3 repo | Regex bắt cả tiền tố hash file; chưa soát từng chuỗi. Chỉ khẳng định `779f90c` là commit lab ngoài `main` (`tho/laptop/hash_refs.txt`) |
| Độ phủ manifest | Chỉ so theo đường dẫn. File "không có trong manifest" có thể vẫn được phủ bằng hash ở định dạng khác (ví dụ hàng đợi T-054). Chưa đối chiếu hash |
| Độ phủ kho `D:/RCA-archive` | Chỉ băm file trùng tên + cỡ với file trong kho (2,61 GB). Phần còn lại chưa so hash với kho |
| Bản k6 thô 47 tag từ 17/11 | Đã thấy cùng danh sách tag ở máy tải và exp-obs; chưa so hash giữa hai bản. Tìm theo tên 5 tag (`t071-e2-01-x1`, `t3-7ffb2305`, `t073-e5-01-x1`, `t067-tai-1gio-001`, `t3-124242f0`): `raw.json`/`raw.csv`/`container.log` không có trong repo RCA, trừ `t3-124242f0` có trong kho (T-069). Repo RCA chỉ có tóm tắt (`k6-phut.json`, `summary.json`…) |
| Image Docker nào là đích hoàn tác | Chưa ánh xạ 39 image trên exp-app với kế hoạch hoàn tác |
| Vai trò file trong `lab-file.tsv` | Lấy máy móc từ dòng chú thích đầu file; chưa đọc hết từng file |

Không có lệnh nào phải dừng vì nghi không chỉ đọc. Sudo chỉ dùng cho `sudo -n true` (thử có cần mật khẩu không), `sudo -n crontab -l [-u user]` và `sudo -n -l` (liệt kê quyền của ubuntu trên exp-app).

## Rủi ro nếu dời hoặc đổi tên

| # | Rủi ro | Bằng chứng |
|---|---|---|
| R1 | 7 service FlashTicket: compose ghi nhớ `/opt/flash-ticket-build/t067-compose/hieu-luc/*.yml` và env file `/opt/flash-ticket-app/env-t062/*.env`. Dời hoặc đổi tên thì `docker compose` (recreate, down, hoàn tác) không tìm thấy file. `inj3.py` đọc thư mục compose từ `/home/ubuntu/t063/inj/compose-dir` (trỏ vào `hieu-luc`) và giữ trạng thái ở `/home/ubuntu/t063/inj` (viết cứng) | `may-container.tsv`; `p4-app.txt` compose_path_refs; `p5-app.txt`; `faults/injectors/docker/inj3.py:20-21` |
| R2 | Bộ quan sát: project `flash-ticket-obs-pinned` có working_dir `/opt/rca-lab/observability`, env file `/opt/rca-lab/inventory/oracle-exp.env`, 7 bind mount từ `/opt/rca-lab`. Collector agent trên exp-app cũng chạy từ `/opt/rca-lab` (@`407b4f5`) với env file cùng tên. Dời `/opt/rca-lab` thì restart container lỗi | `may-container.tsv` |
| R3 | `t072-bo-nhan`: env file của project nằm trong thư mục mang mã task `/srv/rca-lab/runs/t072-e3-01-cfg/webhook.env`; cần cho cả `down`. Container gắn `/srv/rca-lab/runs/t072-e3-01` (rw). Tên host `t072-bo-nhan` nằm trong URL contact point `t072-webhook` | `p6-obs.txt`; `t072-luat.yaml` |
| R4 | Dashboard: 3 dashboard đang hiện viết cứng URL `public/rca/t065-l11-001/...` và liên kết chéo bằng UID `t065-l8b-rca`, `t065-l8b-phat-lai`. `sau_v082.py` mặc định ghi vào `t065-l11-001`; `service_graph.py` ghi `service-graph/` ở đó. Đổi tên thư mục hoặc UID làm vỡ dashboard và link đã gửi | `lab-dashboard.tsv`; `campaigns/runner/sau_v082.py:147-159` |
| R5 | UID luật `t072-*` được dùng làm khóa trong hồ sơ chấm (382 file repo RCA) và trong `webhook.jsonl` đã ghi; `incidents.py` gom theo `__alert_rule_uid__`. Đổi UID thì chuỗi cảnh báo mới không nối được với hồ sơ cũ. Folder Grafana mang tên "T-072 W4 cảnh báo" | `lab-luat-canh-bao.tsv`; `campaigns/online/incidents.py:86-91` |
| R6 | Hash bản chụp M1 `b0f79a4d…` phụ thuộc byte CRLF của cây làm việc Windows. Clone mới trên Linux hoặc chép từ blob git cho 26 file khác byte → hash khác, không khớp `run_m1.py`/`stage_m1.py` (viết cứng) và `ma_nguon_sha256` trong chỉ mục T-064 | `m1-ban-chup.tsv`; `git ls-files --eol`; `campaigns/runner/run_m1.py:18` |
| R7 | VNPay giả và đường hầm chạy trần (ppid 1, không unit) từ `/opt/flash-ticket-app/l1-vnpay`. Khởi động lại máy thì mất; dời thư mục thì `kiem-mock.py`, `tunnel-remote.py` (viết cứng đường này) không khôi phục được. Luồng thanh toán của k6 cần cổng 19091 trên máy tải | `may-tien-trinh-cron-unit.tsv`; `load/controller/support/kiem-mock.py:4`, `tunnel-remote.py:4` |
| R8 | `rca-toxiproxy` (docker run, không compose) gắn `/opt/flash-ticket-app/rca-toxiproxy/proxies.json`; không có file compose để tạo lại, chỉ có lệnh cũ trong hồ sơ T-062 | `p4-app.txt` toxiproxy_inspect |
| R9 | Ba máy chạy ba commit lab khác nhau (`1bb40ca`, `407b4f5`, `5a39028`); `chuoi_tai.py` từ chối khi commit `/opt/rca-lab` đổi giữa kho; `runner4.py` gọi `inj3.py` tại `/opt/rca-lab` trên exp-app | `may-git.tsv`; `chuoi_tai.py:31,194`; `runner4.py:48` |
| R10 | Commit `779f90c` chỉ có ở nhánh `t073-e5-p` (local và origin). Xóa nhánh thì mất commit được hồ sơ E5 dẫn | `lab-nhanh-commit.tsv`; `tho/laptop/hash_refs.txt` |
| R11 | Bản k6 thô của 47 lượt từ 17/11 (E2, E3, E4, E5, T-067, T-069) nằm ở máy tải và exp-obs; repo RCA chỉ có tóm tắt; kho chỉ có 3 `raw.json` của T-069. Dọn máy trước khi kéo về là mất bản thô | mục "Chưa kiểm được" (kiểm theo 5 tag); `p6-tai.txt`; `p7-obs-taiout.txt` |
| R12 | 1,64 GB đầu ra chưa track không thấy trong manifest nào (nhất là T-054 `main-013*`, `chuan-bi-main-013-v2`; `T-062/ca/_metric-bo-sung`); 5 manifest `NEN-2026-11-15.jsonl` và `T-065/manifest.json` cũng chưa track. Xóa hoặc dời là mất dấu toàn vẹn | `rca-chua-track-theo-thu-muc.tsv`; chi tiết `.tsv.gz` |
| R13 | `/opt/flash-ticket-app/collector/` (1,3 GB, không container gắn) vẫn được `safe_export.py` đọc (`collector.env`); `safe_export.py` cũng đọc `/opt/flash-ticket-src/.env`, `/opt/flash-ticket-app/env/*.env`, `secrets/ticket-qr/key-ring.json` | `campaigns/runner/safe_export.py:14-44` |
| R14 | `t072-thu-e3-go.yaml`, `t073-e5-go.yaml` là lệnh xóa Grafana chạy mỗi lần khởi động; đổi tên đuôi hoặc dời làm thay đổi hành vi khởi động | `lab-luat-canh-bao.tsv` |
| R15 | Mã lab và RCA còn nhắc đường đã không còn trên exp-obs: `/opt/flash-ticket-rca/cases`, `/opt/rca-m1ft/bo-sung-dev3` (`sau_v082.py:29-30,158`, `l8b-xuat.py`), `~/rca-dieu-phoi/STOP` (`l8b-xuat.py:54`, docstring `runner4.py`). `/home/ubuntu` trong `results/` còn chỉ các máy EC2 cũ (T-032…T-054), khác `/home/ubuntu` của ba máy hiện tại | `rca-duong-dan-cung.tsv`; `p1-obs.txt` stat `/opt/*` |
| R16 | Worktree `D:/Project/rca-lab-wt/T-072`, `T-073` có file chưa track (trùng `main` hoặc commit N). Lệnh `git worktree remove` sẽ từ chối hoặc xóa chúng tùy cờ | `lab-nhanh-commit.tsv` |
| R17 | Hai nhóm trong `D:/RCA-archive` (`exp-obs/t066-nhom2`, `T-069/raw-json`) chưa có dòng trong README của kho | `D:/RCA-archive/README.md` |

## Toàn vẹn

`SHA256SUMS` liệt kê mọi file trong thư mục này (trừ chính nó). Kiểm: `cd results/T-070/kiem-ke && sha256sum -c SHA256SUMS`.
