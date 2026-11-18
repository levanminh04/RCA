# T-066 — Danh sách xóa đề xuất (bước 11, chờ Minh duyệt)

Lập 17/11/2026. **Chưa xóa gì.** Minh duyệt từng mục (hoặc theo nhóm); mục không duyệt giữ nguyên.
Bằng chứng: lệnh chỉ đọc chạy 17/11 (LOG T-066 phiên 2). "Có bản trên laptop" nghĩa là sha256 của từng file trên máy
xuất hiện trong tập hash của `results/T-062…T-065`, `D:/RCA-archive` hoặc `results/T-064/manifest-3.json`.
Dung lượng: `du -sh` trên máy. Đĩa exp-obs hiện 57/135 GB.

## Nhóm 1 — xóa được ngay, đã có bản tương đương hoặc dựng lại được

| # | Máy | Mục | Dung lượng | Bằng chứng còn bản / dựng lại được | Đề xuất |
|---|---|---|---|---|---|
| 1.1 | exp-obs | `/opt/flash-ticket-obs/pinned/data/capture`, `…/data/queue` | 5,1 GB + 38 MB | Vùng ghi vòng của Collector cũ; Collector đã chuyển sang `/srv/rca-lab/collector-gateway` lúc 12:07Z. Dữ liệu đã vào Tempo/Loki/Prometheus; các ca cũ đã đóng gói (45/45 gói ca có bản, mục 1.2) | Xóa |
| 1.2 | exp-obs | `/opt/flash-ticket-rca/cases/` (45 ca), `outputs/` (38) | 14 GB + 1,2 GB | 12 ca có trong `D:/RCA-archive/exp-obs/cases` (danh sách hash), 33 ca có tgz trên laptop (`results/T-058|T-062|T-063`, khớp manifest khi kéo 16/11; tgz chứa cả `cases/<id>` và `outputs/<id>`). Hai ca hồi quy đã chép sang `/srv/rca-lab/m1` | Xóa |
| 1.3 | exp-obs | `/opt/flash-ticket-rca/{venv, src, stage-m1.py, run-m1.py, m1-*.json, flashticket-inventory-source.json, results}` | ~0,5 GB | venv thay bằng `/srv/rca-lab/venv-m1` (`pip freeze --all` trùng); `src` = 39 file trong bản chụp `goc-12` (khớp `m1-source-pins.json`); script và cấu hình có bản trong repo RCA `results/T-058/dem-2026-11-10/` và `/srv/rca-lab/m1/` | Xóa cả `/opt/flash-ticket-rca` (cùng 1.2) |
| 1.4 | exp-obs | `/opt/rca-m1ft/goc`, `goc-2…goc-12`, `bo-sung`, `bo-sung-dev2`, `bo-sung-dev3` | ~0,3 GB | Có trong `D:/RCA-archive/exp-obs/m1ft-inputs` (1.684 file khớp hash); `goc-12` đã chép sang `/srv/rca-lab/m1-snapshots/b0f79a4d…` | Xóa |
| 1.5 | exp-obs | `/opt/rca-m1ft/out/{l5, r9, r9-bo-sung, l5-bo-sung-dt, pc-bo-sung-dt, pc-doi-moc, pc-h8, pc-recreate, chon-dev2-2, chon-dev2-3, dc-dev2-4, dc-t062-4, khong-hoi-quy-1..3, kiem-cai-dat-1..5}`, `tuong-duong-p7.json` | ~0,9 GB | Mọi file (json/jsonl/log/tgz) có bản trùng hash trên laptop: ví dụ `l5` 2385/2385, `pc-doi-moc` 528/528, `khong-hoi-quy-1` 729/729, `r9` 36/36 | Xóa |
| 1.6 | exp-obs | `/opt/rca-m1ft/out/l5-dem`, `pc-doi-moc-dem` | 5,0 GB + 2,8 GB | Bộ đệm đầu vào dựng lại; README archive ghi "dựng lại được" (`chay_ca.py --dung-lai-dau-vao` từ gói ca + `m1-p7-config.json`; mỗi mục có `moc.json` để kiểm hash khi dùng lại) | Xóa |
| 1.7 | exp-obs | `~/rca-dieu-phoi/` trừ mục 2.2 | ~2,3 GB | 528/530 file có bản trên laptop (`tai-out` 390/390, `ca` 26/26, `thu3` 14/14, script = repo lab); `__pycache__` (2 file) là bộ đệm Python | Xóa sau khi làm 2.2 |
| 1.8 | exp-obs | Volume Docker `pinned_grafana-data` | 0 B | Không container nào dùng (`docker system df -v`: LINKS 0) | Xóa |
| 1.9 | exp-obs | Thư mục Grafana rỗng cũ: `RCA FlashTicket`, `0 · Bắt đầu tại đây`, `1 · Kết quả hiện hành`, `9 · Lưu trữ`, `G2 bản 6 · 12-11`, `L3 · P7 · 13-11`, `L4 · Bộ bản tạm · 14-11` | — | 9 dashboard đã nạp lại vào thư mục mới từ repo lab (12:08:11Z) | Xóa trong Grafana (cần đăng nhập: Minh làm, hoặc cho phép agent dùng tài khoản quản trị) |
| 1.10 | exp-obs | `/srv/rca-lab/rca-results/kiem-g1-t066`, `/srv/rca-lab/ledger/kiem-cach-ly-t066.jsonl` | nhỏ | File thử của bước 9 (so byte G1) và bước 6 (2 dòng thử); kết quả đã ghi ở `results/T-066/` | Xóa |

## Nhóm 2 — cần một bước trước khi xóa

| # | Máy | Mục | Việc trước khi xóa | Lý do |
|---|---|---|---|---|
| 2.1 | exp-obs | `/opt/rca-m1ft/out/chon-dev2-1`, `chon-dev2-1b` (~0,2 GB) | Kéo về 6 `summary.json` chưa có bản (vd `chon-dev2-1/V012-H2/19b17e22/summary.json`) vào `D:/RCA-archive/exp-obs/m1ft-out/` kèm danh sách hash | 1065/1071 file có bản; 6 summary khác hash (có thời gian chạy) |
| 2.2 | exp-obs | `~/rca-dieu-phoi/tai-linux-events.jsonl` | Kéo về `D:/RCA-archive/exp-obs/` kèm hash | Nhật ký sự kiện của bộ điều khiển tải cũ (mutation, gia hạn token); chưa có bản |
| 2.3 | exp-obs | `/opt/flash-ticket-obs/rca-ket-qua` (0,9 GB), `/opt/flash-ticket-obs/pinned/` (compose cũ, provisioning, `*.bak-*`), `/opt/flash-ticket-obs/grafana.env` | Giữ tới khi Minh nghiệm thu T-066 (đường hoàn tác bước 7) | Bản chép `/srv/rca-lab/rca-results` khớp 8013/8013; cấu hình có bản tương đương trong repo lab (JSON ≡ YAML) |
| 2.4 | exp-obs | Container `flash-ticket-lgtm` (dừng từ 11/11), image `grafana/otel-lgtm:0.40.0` (3,58 GB), volume `flash-ticket-obs_lgtm-data` (680 MB), `/opt/flash-ticket-obs/compose-lgtm.yml` | Minh quyết có giữ dữ liệu LGTM đầu T-058 (10–11/11) không | Kho LGTM đầu tiên của T-058, đã thay bằng bộ ghim; dữ liệu trong volume chưa có bản nào |
| 2.5 | exp-obs | `~/t058` (15 MB), `~/t062-ca-*.tgz`, `~/t063-*.tgz`, `~/l5`, `~/phien-c`, `~/*.log`, `~/*.sh`, `~/ca-*.txt`, `~/danh-sach-phat-lai*.json`, `~/kiem-r.py`, `/opt/rca-tai` | Đối chiếu hash từng file như 1.5 (chưa làm) | Thư mục làm việc của T-058…T-064; phần lớn có bản trên laptop theo tên, chưa kiểm hash |
| 2.6 | Máy tải | `/opt/rca-tai` (k6 cũ, `out/`, `secret/`) | Sau T-067 (lượt tải 1 giờ chạy bằng đường mới `/srv/rca-lab/load-runs`, `/etc/rca-lab/load-secret`) | `out/` đã kéo về archive; `secret/` đã chép sang `/etc/rca-lab/load-secret` (3/3 hash trùng) |
| 2.7 | exp-app | `~/inj.py`, `~/inj2.py`, `~/inj3.py`, `~/build-t062.sh`, `~/deploy-t062.sh`, `~/rollback-t062.sh`, `~/prepare-t062.py` | Sau T-067 (đường hoàn tác container T-062 dùng `rollback-t062.sh`) | `inj3.py` và 4 script có bản trong repo lab (hash trùng); `inj.py`, `inj2.py` là bản cũ chưa kiểm. **Giữ** `~/t063/inj` (thư mục trạng thái mà `inj3.py` vẫn dùng) |
| 2.8 | Laptop | 2 dòng khóa máy chủ (213.35.116.128, 129.221.208.47) đã lỡ thêm vào `D:/RCA-ext/keys/known_hosts` (LOG S0-15) | Minh chọn giữ hay xóa | Khóa trùng bản đã kiểm; giữ không hại, xóa để về trạng thái trước phiên |

## Không đề xuất xóa

- Volume `flash-ticket-obs-pinned_*` (dữ liệu đang dùng), `/srv/rca-lab/*` (trừ 1.10), kết quả hồi quy `/srv/rca-lab/m1/v082-hoi-quy` và đầu vào chép `bo-sung-hoi-quy` (luật cứng 10: giữ mọi lượt chạy).
- Trên exp-app: `/opt/flash-ticket-app`, `/opt/flash-ticket-build`, `/opt/flash-ticket-src`, `/opt/flash-ticket-infra`, image `arm64-t062-6b21ed55` (T-067 dùng làm đường hoàn tác).

## Ước tính giải phóng

Nhóm 1: khoảng 31 GB trên exp-obs. Nhóm 2 sau khi xử lý: thêm khoảng 5 GB trên exp-obs (2.4 là phần lớn).

## Kết quả

- 17/11/2026: Minh duyệt nhóm 1 ("Duyệt nhóm 1"). Đã xóa 1.1–1.8, 1.10 lúc 12:53Z; chi tiết ở `thay-doi-may.md`. 1.9 chưa làm (cần đăng nhập Grafana). Nhóm 2 chưa duyệt.
- 18/11/2026: Minh chỉ đạo nhóm 2 ("cái nào không có giá trị sử dụng lại nhiều, không mang lại giá trị mới thì xóa đi, dùng lại được thì kéo"). Đối chiếu hash 1.297 file nhóm 2 trên exp-obs với laptop: 1.224 có bản, 73 chưa có. Kéo 65 file (log chạy, `export-audit-*.json`, `tai-linux-events.jsonl`, `compose-lgtm.yml`, `fixtures.json`…) vào `D:/RCA-archive/exp-obs/t066-nhom2/tep-le.tar` (65/65 khớp hash máy, danh sách `tep-le-may.sha256`) và volume LGTM thành `lgtm-data.tar` (`68ffdef5…`, khớp). Không kéo: 6 `summary.json` lượt lặp (đầu ra trùng laptop, chỉ khác số giây), `secret/tokens.json` cũ (bí mật hết hạn), `get-docker.sh` (script công khai). Đã xóa 2.1–2.5 trên exp-obs lúc 23:09:46–23:09:50Z (giờ máy); đĩa 30 → 25 GB. 2.8: gỡ 2 dòng khỏi `D:/RCA-ext/keys/known_hosts` (còn 2 dòng như trước phiên). **Giữ** 2.6 (máy tải `/opt/rca-tai`) và 2.7 (script trên exp-app): là đường hoàn tác của T-067; xóa sau T-067.
