# Bước 3: dời trên exp-app (24/11/2026, 16:29–16:41Z)

- **Kế hoạch:** `../KE-HOACH-DON.md` §9 bước 3.
- **Danh sách dời và hoàn tác** đã ghi vào LOG T-070 (mục 21:00Z, giờ ghi LOG) trước khi làm.
- **Thời gian FlashTicket thử nghiệm ngừng:** 16:29:48Z → 16:39:43Z (khoảng 10 phút). Lần này đo được; kế hoạch chỉ ước lượng.

| File | Nội dung |
|---|---|
| `lenh-1-dung.sh`, `.out` | Dừng theo thứ tự: VNPay giả và đường hầm → agent → 7 service → Keycloak → toxiproxy (đổi tên thành `rca-toxiproxy-cu`, giữ lại) → hạ tầng (`down -t 60`, không `-v`) |
| `lenh-2-doi.sh`, `.out` | Tạo thư mục mới, `mv` theo bảng §7.2; sửa 3 bind của Keycloak; ghi lại nội dung `compose-dir` |
| `lenh-3-hieu-luc.sh`, `.out` | Checkout lab `85ace52`; `git worktree repair`; dựng cấu hình hiệu lực bằng `hieu_luc.py`; so với bộ T-067 |
| `lenh-4-bat.sh`, `.out` | Bật hạ tầng, toxiproxy, Keycloak, 7 service. SSH bị máy đóng giữa lúc `deploy.sh` chạy (16:37Z), xem mục "Sự cố" |
| `deploy.tsv` | Tiến độ `deploy.sh` (7/7 service: health đạt, đăng ký Eureka đạt) |
| `lenh-5-bat-tiep.sh`, `.out` | Bật agent, VNPay giả, đường hầm |
| `sau_app.py`, `app.json` | Kiểm sau dời, cùng cách đo với `../truoc/app.json` (env chỉ ghi hash) |
| `lenh-6-kiem-telemetry.sh` | Kiểm log và trace từ app về tới obs |

## Kết quả so với bước 0

| Kiểm | Kết quả |
|---|---|
| B8 cấu hình hiệu lực | 7/7 file mới trùng bộ T-067 sau khi thay đường cũ → mới (`lenh-3-hieu-luc.out`); các phép tự kiểm của `hieu_luc.py` đạt |
| B7, B8 container | 14/14 container cùng tên. Với từng container, các trường sau trùng bước 0: image (tên và id), bộ nhớ, `NetworkMode`, cấu hình log, restart, cổng, user, lệnh, nhãn, mọi biến môi trường (tên và hash giá trị). Mount trùng sau khi thay đường cũ → mới. File compose trỏ đúng chỗ mới |
| Env file | 11/11 file trong `/opt/flashticket/env` trùng hash với bản gốc (7 `env-t062/*.env` + 4 file của `env/`) |
| B9 DB | `booking_db`: CANCELLED 10.510, COMPLETED 41.705, EXPIRED 11.398, trùng bước 0. Volume có tên của hạ tầng được dùng lại |
| MongoDB `/data/configdb` | Đây là volume không tên do image MongoDB tự khai. Lần tạo lại container sinh volume không tên mới (`8c4f99bc…`). Bản cũ (`6360e5cb…`) rỗng (4 KB), nên không mất gì. Dữ liệu MongoDB thật ở volume có tên `flash-ticket-infra_user-data`, vẫn được dùng lại |
| Mount `schema.cjs` | Nguồn mới `/opt/flashticket/docs/architecture/data/mongodb/schema.cjs`: thư mục rỗng, như cũ (§7.2) |
| Toxiproxy | 4 proxy như `proxies.json` (15433, 16379, 15673, 18082), đều bật |
| VNPay giả, đường hầm | Chạy từ `/srv/flashticket-rca/faults/vnpay` (helper khôi phục; cấu hình mock không đổi hash). Từ máy tải, `127.0.0.1:19091/health` → `{"status": "UP"}` |
| `compose-dir` | `/opt/flashticket/compose` |
| Telemetry | Từ 16:37Z đến 16:40Z, Loki nhận log của 11 nguồn; Tempo có 431 trace trong 5 phút |
| Đường cũ | `/opt/rca-lab`, `/srv/rca-lab`, `/etc/rca-lab`, `/opt/flash-ticket-src`, `/opt/flash-ticket-infra`, `/home/ubuntu/t063` không còn; lab @`85ace52` |

## Sự cố trong lúc làm

- **Mất kết nối SSH lúc 16:37Z, giữa lúc `deploy.sh` đang chạy.** Đây là lỗi kết nối giữa laptop và máy, không phải lỗi của việc dời:
  - không thấy tiến trình nào bị hệ thống diệt vì thiếu bộ nhớ;
  - bộ nhớ còn trống 7,6 GB.
- **`deploy.sh` vẫn chạy tiếp trên máy và xong lúc 16:39:13Z.** Theo luật đứt SSH, tôi đọc lại trạng thái rồi chỉ chạy phần chưa làm (agent, VNPay giả, đường hầm). Không chạy lại phần đã xong.
- **`git worktree repair` báo `.git file broken`** ở `/opt/flash-ticket-build/{event-service,user-service}`. Đó là 2 trong 13 checkout cũ, sẽ xóa ở việc nhẹ §11. Worktree đang dùng (`/opt/flashticket/build/36a3725d`) đã được sửa và đúng commit `36a3725d`.
- Nhật ký `deploy.sh` bị ghi tạm vào `/srv/flashticket-rca/faults/deploy-don-2026-11.tsv`. Theo khung, chỗ đúng là `runs/`; bản chép nằm ở đây.

## Còn giữ để hoàn tác (chưa vào archive)

- `/opt/flash-ticket-build/t067-compose/`, 13 checkout cũ và phần còn lại của `/opt/flash-ticket-app/`.
- Container đã dừng `rca-toxiproxy-cu`.
- `/opt/docs` (nguồn bind cũ của MongoDB, rỗng).
- Volume không tên `6360e5cb…` (rỗng, không container nào dùng).

Khi Minh xác nhận hết nhu cầu hoàn tác: chuyển các thư mục vào `archive/2026-11/`. Xóa container và volume là việc nhẹ, trình riêng.
