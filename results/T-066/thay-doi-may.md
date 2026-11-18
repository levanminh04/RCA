# T-066 — Thay đổi trên máy

Mỗi dòng: giờ (UTC, 17/11/2026), máy, thay đổi, hash trước/sau, cách hoàn tác. Ghi thêm ở cuối; không sửa dòng cũ.

## exp-obs (213.35.116.128)

| Giờ | Thay đổi | Hash trước → sau | Hoàn tác |
|---|---|---|---|
| 11:40 | Tạo `/opt/rca-lab` (ubuntu 755), `/etc/rca-lab` (root 755), `/etc/rca-lab/controller` (ubuntu 700), `/srv/rca-lab` (root 755) và `m1/{cases,bo-sung}` (root:rca 750), `m1/{outputs,v082}` (rca 750), `m1/export-audit` (root 700), `m1-snapshots` (root 755), `ledger` (ledger 700), `runs`, `load-controller` (ubuntu 700). Trước đó không tồn tại (`test ! -e`) | — | `sudo rm -rf /opt/rca-lab /etc/rca-lab /srv/rca-lab` (chỉ sau khi chuyển ngược compose) |
| 11:40 | Chép `/opt/flash-ticket-obs/grafana.env` → `/etc/rca-lab/grafana.env` (root 600). Bản gốc giữ nguyên | nguồn = đích `87371bf3…` | xóa bản đích |
| 11:40 | Chép `/home/ubuntu/t058/credential-hash-catalog.json` → `/etc/rca-lab/` (root 600) | `4173af64…` = | xóa bản đích |
| 11:41 | Chép `m1-p7-config.json`, `m1-source-pins.json`, `flashticket-inventory-source.json` từ `/opt/flash-ticket-rca` → `/srv/rca-lab/m1/` (root:rca 640) | `eb7dddd7…`, `8aebdf2a…`, `7e09059c…` = | xóa bản đích |
| 11:41 | `tar` `/opt/rca-m1ft/goc-12` → `/srv/rca-lab/m1-snapshots/b0f79a4d…/` (root, go-w) | 149/149 khớp danh sách hash archive; `ma_nguon_sha256` = `b0f79a4d…` | xóa thư mục đích |
| 11:41 | Venv `/srv/rca-lab/venv-m1` (451 MB) từ `requirements-m1.txt`, tải gói từ PyPI | `pip freeze --all` trùng venv P7 | xóa thư mục |
| 11:42 | `tar` `cases/46aab4be`, `cases/ebd5ef38`, `outputs/46aab4be/method-input.json` từ `/opt/flash-ticket-rca` → `/srv/rca-lab/m1/` | 13/13 file khớp hash bước 0 | xóa bản đích |
| 11:42 | Chép gói bổ sung hồi quy → `/srv/rca-lab/m1/bo-sung-hoi-quy/{46aab4be,ebd5ef38}/` | `2f4ef463…`, `e549f706…` = | xóa |
| 11:42–11:44 | Đầu ra hồi quy V082 → `/srv/rca-lab/m1/v082-hoi-quy/` | `results/T-066/hoi-quy-v082.json` | giữ (luật cứng 10) |
| 11:45 | Tạo cặp khóa ed25519 `rca-lab-controller` trong `/etc/rca-lab/controller/` (khóa riêng 600, không rời máy); vân tay `SHA256:tzVU95z38qtZ2PQkBu7VgOieaJdG4N0JUBqL8aWic7g` | — | xóa `id_ed25519*` |
| 11:45 | `/etc/rca-lab/controller/known_hosts` (600): khóa máy chủ ed25519 của exp-app và máy tải, lấy từ bản đã kiểm trên laptop | — | xóa |

## exp-app (129.221.208.47)

| Giờ | Thay đổi | Hash trước → sau | Hoàn tác |
|---|---|---|---|
| 11:46 | Thêm 1 dòng `from="213.35.116.128" ssh-ed25519 … rca-lab-controller` vào `~ubuntu/.ssh/authorized_keys`. Nguồn đo: log sshd `Connection closed by authenticating user ubuntu 213.35.116.128` lúc 11:45:39 (khác dự kiến `10.0.0.215` vì kết nối qua IP công khai) | `6815b558…` (1 dòng) → `0ce85c2d…` (2 dòng) | `sed -i '/rca-lab-controller$/d' ~/.ssh/authorized_keys` |
| 11:46 | Tạo `/opt/rca-lab` (ubuntu 755) | — | `rm -rf /opt/rca-lab` |

## Máy tải (3.24.8.49)

| Giờ | Thay đổi | Hash trước → sau | Hoàn tác |
|---|---|---|---|
| 11:46 | Thêm 1 dòng `from="213.35.116.128" … rca-lab-controller` vào `~ubuntu/.ssh/authorized_keys`. Nguồn đo: log sshd 11:45:41 | `402d7177…` (2 dòng) → `9fda7054…` (3 dòng) | `sed -i '/rca-lab-controller$/d' ~/.ssh/authorized_keys` |
| 11:46 | Tạo `/opt/rca-lab` (ubuntu 755), `/etc/rca-lab` (root 755), `/etc/rca-lab/load-secret` (ubuntu 700), `/srv/rca-lab` (root 755), `/srv/rca-lab/load-runs` (ubuntu 755) | — | `sudo rm -rf` ba thư mục |
| 11:46 | Chép (cp -p) `/opt/rca-tai/secret/{l1-forward-key.json, l1-tokens.json, tokens.json}` → `/etc/rca-lab/load-secret/` | `58acd432…`, `e10bb30c…`, `a2186665…` = | xóa bản đích |

## Thu hồi khóa bộ điều khiển (Q1(b))

Xóa dòng `rca-lab-controller` ở `authorized_keys` của exp-app và máy tải; xóa `/etc/rca-lab/controller/id_ed25519*` trên exp-obs.

## Bổ sung (ghi sau, theo LOG bước 7, 9, 10)

| Giờ | Máy | Thay đổi | Hash / kiểm | Hoàn tác |
|---|---|---|---|---|
| 12:07 | exp-obs | Chép `/opt/flash-ticket-obs/rca-ket-qua` → `/srv/rca-lab/rca-results` (tar) | 8013/8013 khớp; danh sách `/srv/rca-lab/rca-results-chep-2026-11-17.sha256` (`a328c98f…`) | xóa bản đích |
| 12:07 | exp-obs | Tạo `/srv/rca-lab/collector-gateway/{capture,queue}` (root 755) | — | xóa |
| 12:07:48 | exp-obs | Compose quan sát chuyển sang `/opt/rca-lab/observability/compose.yaml` (project `flash-ticket-obs-pinned`, 4 volume giữ nguyên); 5 container tạo lại | container trước: `46ab71625f37` prometheus, `6540f936c846` grafana, `5b3b4baf9405` loki, `9f328ee1b131` tempo, `0710b6abc6fc` collector; image digest không đổi | `cd /opt/flash-ticket-obs/pinned && sudo docker compose -p flash-ticket-obs-pinned -f compose.json up -d` (cần phục hồi `data/` rỗng — đã có) |
| 12:10 | exp-obs | Sampler Tempo `/srv/rca-lab/runs/tempo-do-t066/` (tiến trình nền, tự dừng sau 25 giờ) | `tempo_do.sh` `e14519a0…` | `touch …/DUNG` |
| 12:13–12:15 | exp-obs, máy tải, exp-app | `/opt/rca-lab` checkout `f78ed52` rồi `ab1c52c`; `tai_linux test-duong` làm mới token `/etc/rca-lab/load-secret/l1-tokens.json` (`e10bb30c…` → `56a858f5…`) | — | token: tạo lại pool |
| 12:14–12:46 | cả ba | Lượt `e2e-001`: tải, tiêm PAUSE-PAYMENT 12:25–12:35 trên exp-app (đã gỡ, `fault-stop`), dữ liệu ca ở `/srv/rca-lab/{m1,runs,ledger,load-controller}`, thêm ca 7ffb2305 vào chỉ mục `/srv/rca-lab/rca-results/t065-l11-001/du-lieu/` | `results/T-066/e2e-001/hash-tren-may.sha256` | giữ (luật cứng 10) |

## Xóa theo danh sách đã duyệt (nhóm 1, Minh duyệt 17/11/2026)

| Giờ | Máy | Mục (theo `danh-sach-xoa.md`) | Kết quả |
|---|---|---|---|
| 12:53:42–12:53:45 | exp-obs | 1.1 `/opt/flash-ticket-obs/pinned/data/{capture,queue}`; 1.2–1.3 `/opt/flash-ticket-rca`; 1.4 `/opt/rca-m1ft/{goc, goc-2…goc-12, bo-sung, bo-sung-dev2, bo-sung-dev3}`; 1.5–1.6 22 mục liệt kê trong `/opt/rca-m1ft/out/` (gồm `l5-dem`, `pc-doi-moc-dem`); 1.7 `~/rca-dieu-phoi/*` trừ `tai-linux-events.jsonl`; 1.8 volume `pinned_grafana-data`; 1.10 `/srv/rca-lab/rca-results/kiem-g1-t066`, `/srv/rca-lab/ledger/kiem-cach-ly-t066.jsonl` | Đã xóa, không hoàn tác được (bản còn ở laptop/archive theo cột bằng chứng). Đĩa `/` 58 GB → 27 GB dùng. Còn lại đúng: `/opt/rca-m1ft/out/{chon-dev2-1, chon-dev2-1b}`, `~/rca-dieu-phoi/tai-linux-events.jsonl` (nhóm 2). Container quan sát và sampler Tempo vẫn chạy |
| — | exp-obs | 1.9 thư mục Grafana rỗng | Chưa làm (cần đăng nhập Grafana) |
| 15:28:06 | exp-obs | 1.9 thư mục Grafana rỗng: `0 · Bắt đầu tại đây`, `1 · Kết quả hiện hành`, `G2 bản 6 · 12-11`, `L3 · P7 · 13-11`, `L4 · Bộ bản tạm · 14-11`, `9 · Lưu trữ`, `RCA FlashTicket` (xóa qua API Grafana bằng phiên Minh đăng nhập, qua tunnel). Trước khi xóa `/api/folders/<uid>/counts`: 0 dashboard, 0 alert, 0 library | 7/7 trả 200. Còn: `00-start-here`, `10-current-results`, `90-archive/{2026-11-12-g2-v6, 2026-11-13-l3-p7, 2026-11-14-l4-temporary}`; dashboard gốc `t058-flashticket`, `t061-infinity` (ngoài 9 UID, không thuộc danh sách xóa) giữ nguyên |

## Xóa nhóm 2 (Minh chỉ đạo 18/11/2026)

| Giờ (giờ máy) | Máy | Mục | Kết quả |
|---|---|---|---|
| 23:09:46–23:09:50 | exp-obs | `/opt/rca-m1ft` (còn `chon-dev2-1*`), `~/rca-dieu-phoi`, `~/{t058,l5,phien-c,t062-day}`, file lẻ trong `~` (log, sh, txt, json, tgz), `/opt/rca-tai`, `/opt/flash-ticket-obs` (compose cũ, `rca-ket-qua`, `grafana.env` cũ, `compose-lgtm.yml`); container `flash-ticket-lgtm`, `rca-tai-validate-01`, `rca-tai-version-01`; volume `flash-ticket-obs_lgtm-data`; image `grafana/otel-lgtm:0.40.0` | Đã xóa, không hoàn tác trên máy; bản cần giữ ở `D:/RCA-archive/exp-obs/t066-nhom2/` hoặc đã có trên laptop. Trước khi xóa: container đang chạy chỉ gắn `/opt/rca-lab`, `/srv/rca-lab` và 4 volume `flash-ticket-obs-pinned_*`. Đĩa `/` 30 → 25 GB. Đường hoàn tác compose cũ (bước 7) không còn |
| — | laptop | `D:/RCA-ext/keys/known_hosts`: gỡ 2 dòng 213.35.116.128, 129.221.208.47 (S0-15) | còn 2 dòng như trước phiên |
