# T-071 bước 0 — trạng thái máy khi mở khung S0 (chỉ đọc)

Kiểm 20/11/2026, giờ lấy bằng `date -u` trên từng máy. Chỉ lệnh đọc; không ghi file nào lên máy. Script chạy qua stdin SSH (`remote.ps1` của T-058); máy tải đi qua exp-obs bằng khóa bộ điều khiển `/etc/rca-lab/controller/` (cùng đường `tai_linux.py` dùng).

## exp-app (12:55:03Z – 12:55:20Z)

| Mục | Kết quả | Đạt |
|---|---|---|
| Container FlashTicket | api-gateway, booking, discovery, event, payment, ticket, user: image `ft-local/*:arm64-t067-36a3725d` (bản ghim `36a3725`); keycloak `arm64-776d9c9e`; payment "Up 19 hours" (tạo lại bởi ô RECREATE-PAY của T-069, khớp README §2); hạ tầng postgres 16.15, rabbitmq 4.3.6, redis 7.4.11, mongo 7.0 healthy; `flash-ticket-collector`, `rca-toxiproxy` | có |
| `/opt/rca-lab` | `407b4f5489b9…`, `git status --porcelain` 0 dòng | có |
| Tiêm lỗi | `inj3.py verify` → `{"sach": true, "con_lai": []}` (12:55:20Z); trước đó kiểm 0 file `*.pause-deadline` nên `verify` không gỡ gì; toxiproxy 4 proxy, 0 toxic | có |
| Tiến trình | không có `inj3`, `_renew`, `rcaburn`, `runner4`, `tai_linux`, `chuoi_tai`, `k6` | có |
| Lịch | không crontab ubuntu; không systemd timer khớp rca/t06/t07/m1 | có |
| `compose-dir` của inj3 | `/opt/flash-ticket-build/t067-compose/hieu-luc` (khớp README §2) | có |
| Đĩa `/` | 48G, dùng 26G, trống 22G (55%) | — |
| `/home/ubuntu/t071` | chưa có | — |

## exp-obs (12:55:40Z)

| Mục | Kết quả | Đạt |
|---|---|---|
| Container | collector, grafana, loki, prometheus, tempo (Up 2–3 ngày) | có |
| `/opt/rca-lab` | `407b4f5489b9…`, 0 dòng bẩn | có |
| STOP | không có `/srv/rca-lab/runs/STOP`, `/srv/rca-lab/load-controller/STOP` | có |
| Tiến trình | không có `runner4`, `chuoi_tai`, `tai_linux`, `stage_m1`, `run_m1`, `xuat_bo_sung`, `sau_v082`, `safe_export`, `k6` | có |
| Lịch | không crontab ubuntu; không timer khớp | có |
| Prometheus | `/-/ready` 200; `up` 3 target, 0 down; khởi động 2026-11-17T12:08:01Z; giữ `30d or 40GiB` | có |
| `/srv/rca-lab/load-controller/` | `tai-linux-events.jsonl` sửa lần cuối 19/11 20:45 (khớp lượt cuối `t069-lap`), `tai-linux.lock` rỗng, `tai-out/` | có |
| `/srv/rca-lab/runs/t07*` | chưa có | — |
| Đĩa `/` | 135G, trống 90G | — |

## Máy tải AWS `3.24.8.49` (12:56:04Z – 12:56:24Z)

| Mục | Kết quả | Đạt |
|---|---|---|
| Container `rca-tai-*` đang chạy | 0 (`sudo -n docker ps`: không container nào chạy) | có |
| Container `rca-tai-*` đã dừng | nhiều, mới nhất `rca-tai-t3-690d426a` Exited (0) 16 giờ trước (lượt T-069) | — (không đụng) |
| Tiến trình k6 | không | có |
| `/srv/rca-lab/load-runs/t07*` | chưa có | — |
| Lịch | không crontab ubuntu | có |
| Đĩa `/` | 48G, trống 40G | — |

## Kết luận

Không lệch README §2 theo cách ảnh hưởng an toàn: không job không rõ chủ, cây `/opt/rca-lab` sạch ở `407b4f5` trên cả exp-app và exp-obs, không STOP, không tiêm lỗi. Khung S0 tiếp tục sang E1.

Ghi nhận không chặn: `uptime` exp-app báo "3 users" nhưng `who` rỗng (phiên không có tty, có thể là SSH chạy lệnh của chính phiên này); máy tải "2 users" tương tự.
