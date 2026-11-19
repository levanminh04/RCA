# T-067 — Thay đổi trên máy

Mỗi dòng: giờ (UTC, 18/11/2026), máy, thay đổi, hash, cách hoàn tác. Ghi thêm ở cuối; không sửa dòng cũ.
Phạm vi ghi theo SPEC T-067. exp-obs và máy tải: không ghi gì (bộ kiểm tín hiệu chạy trên laptop qua đường hầm SSH chỉ đọc).

## exp-app (129.221.208.47)

| Giờ | Thay đổi | Hash / kiểm | Hoàn tác |
|---|---|---|---|
| ~05:54 | Tạo rồi xóa ngay `/tmp/t067-agent.yaml` (bản `agent-docker-host.yaml` của lab, để so cấu hình agent). **Ngoài phạm vi ghi** — LOG S0-16 | — | đã xóa |
| 06:01 | `git -C /opt/flash-ticket-src fetch origin` (cập nhật nhánh theo dõi); `git worktree add --detach /opt/flash-ticket-build/t067-36a3725d 36a3725` | HEAD = `36a3725d9b20…`, cây sạch | `git -C /opt/flash-ticket-src worktree remove /opt/flash-ticket-build/t067-36a3725d` |
| 06:01 | Thư mục log build `/opt/flash-ticket-build/t067-36a3725d-logs/` (ubuntu): `build.sh` chép từ lab `68c43ee`, log từng bước, `tien-do.tsv`, `build-manifest.json`, thư mục thử `thu-hieu-luc/` | `build.sh` `d0f5f4f0…` nguồn = đích | xóa thư mục |
| 06:01–06:2x | Lượt `build.sh … t067 all`: 9 lượt `mvnw verify` (Testcontainers kéo image thử về Docker), 7 image `ft-local/<svc>:arm64-t067-36a3725d` | `build-manifest.json` | `docker image rm` 7 image |
| 06:04 | Tạo `/srv/rca-lab` (root 755), `/srv/rca-lab/backups` (root 755), `/srv/rca-lab/backups/t067-20261118` (root 700): `pg_dumpall.sql.gz`, `{event,booking,payment,ticket,keycloak}_db.dump`, `mongo.archive.gz`, `SHA256SUMS` (file 600) | xem bảng Dump bên dưới | giữ (đường lùi dữ liệu) |
| 06:06 | Tạo `/etc/rca-lab` (root 755), `/etc/rca-lab/payment-ngrok-gia.env` (root 644; `NGROK_DOMAIN=disabled.invalid`, `NGROK_AUTHTOKEN=disabled-not-a-token`, giá trị giả, không bí mật) | `1b4d30c8…` | xóa file |
| 06:08 | Tạo `/opt/flash-ticket-build/t067-compose/` (ubuntu): `overrides/` + `hieu_luc.py` chép từ lab `99eeca0` (`git show`), `nguon.sha256`, `hieu-luc/` (cấu hình hiệu lực) | 8/8 nguồn = đích; `hieu-luc/SHA256SUMS` | xóa thư mục |
| 06:21–06:27 | Worktree đối chứng `/opt/flash-ticket-build/t067-dc-640dbaf9`, `/opt/flash-ticket-build/t067-dc-bb84d64f` (detached tại hai commit cha); `mvnw verify` Ticket, Booking; log `…-logs/doi-chung/` | HEAD đúng commit | `git -C /opt/flash-ticket-src worktree remove <thư mục>` |
| ~06:23 | Ghi tạm `/tmp/x` rồi xóa ngay trong cùng lệnh băm. **Ngoài phạm vi ghi** — LOG | — | đã xóa |

| 06:56 | Tạo `/srv/rca-lab/collector-agent` (root 755); `cp -p` `/opt/flash-ticket-app/collector/collector.env` → `/etc/rca-lab/collector.env` (root 600, không đọc nội dung); dừng agent cũ 06:56:31; `cp -a` `…/collector/data/queue` → `/srv/rca-lab/collector-agent/queue` (12 file); chạy agent bằng `/opt/rca-lab/observability/collector/agent-compose.yaml` 06:56:33 | env `4c76776c…` nguồn = đích; danh sách hash queue `a546719f…` nguồn = đích | chép `queue/` ngược về `/opt/flash-ticket-app/collector/data/queue` (agent đã đọc tiếp), rồi `cd /opt/flash-ticket-app/collector && sudo docker compose -p flash-ticket-collector -f compose.json up -d` [chưa thử] |
| 06:57 | `/opt/flash-ticket-build/t067-compose/`: `deploy.sh` (lab `18a59fe`), `migrations/` (2 file từ `640dbaf`), `nguon.sha256` | 3/3 nguồn = đích | xóa |
| 06:58 | `event_db-truoc-migration.dump` vào thư mục backup (dump `event_db` ngay trước migration; đọc lại 12 bảng) | `0add24f7…` | giữ |
| 06:58:29 | Áp 2 migration lên `event_db` | — | khôi phục `event_db-truoc-migration.dump` (đã thử 07:06) |
| 06:58–07:05 | `deploy.sh trien-khai`: 7 container tạo lại bằng image `arm64-t067-36a3725d` | `trien-khai/trien-khai-1.tsv` | `deploy.sh hoan-tac /opt/flash-ticket-app/compose-t062 arm64-t062-6b21ed55` (đã thử) |
| 07:05–07:12 | **Thử hoàn tác:** dừng Event, `pg_restore --clean --if-exists --single-transaction` `event_db`, `deploy.sh hoan-tac` về bản 3 | `trien-khai/hoan-tac-1.tsv` | — |
| 07:13–07:19 | Áp lại 2 migration; `deploy.sh trien-khai` lần 2 | `trien-khai/trien-khai-2.tsv` | như trên |

## exp-obs và máy tải: đầu ra của lượt tải đã duyệt

| Giờ | Máy | Thay đổi | Hoàn tác |
|---|---|---|---|
| 07:20–07:32 | exp-obs, máy tải | Lượt `t067-tin-hieu-001` bằng `tai_linux.py` (lab `8dccb34`): trạng thái và kết quả ở `/srv/rca-lab/load-controller/` (exp-obs, `tai-out/t067-tin-hieu-001`), `/srv/rca-lab/load-runs/t067-tin-hieu-001` (máy tải); pool token `/etc/rca-lab/load-secret/l1-tokens.json` cấp mới | giữ (luật cứng 10) |
| 07:21 | máy tải | 3 lời gọi `GET /api/v1/me` bằng 1 token pool (đọc bằng sudo, không in) | — |
| 07:57– | exp-obs, máy tải | Lượt `t067-tai-1gio-001` (như trên) | giữ |

### Dump (bước 5)

| File | sha256 |
|---|---|
| `pg_dumpall.sql.gz` | `e38750a6ce17e1d0f41fd9b299b940b2c997172766bee86374ffc330b249c3f9` |
| `event_db.dump` | `209385cbd84a00e8924b9cc90738a3924b40b5bc51c367aca4e1fdd8f6921e38` |
| `booking_db.dump` | `948030de843ac2615bbf9d3882c365a23588feae139771006a1742558bb64bab` |
| `payment_db.dump` | `f5f41e569f09a0e266b4b1965950609431d121c68c0a87e440e575739675b467` |
| `ticket_db.dump` | `ee82d0ec51f03969d11defd7740ec7f28e99bee6bfb2e7a72298b569b1d3ac89` |
| `keycloak_db.dump` | `d332542033011279ad9fcf397c6bf1cc4a4b49bee2fdad84d6519a7dbfbd0de9` |
| `mongo.archive.gz` | `617ab3b2f235f854332b2fabe71e58c2d0ac2d127a5106a05a38f5a432bf65f7` |

## Laptop

| Giờ | Thay đổi | Hoàn tác |
|---|---|---|
| ~05:52 | `git fetch origin` trong `D:/Project/flash-ticket-platform` (nhánh theo dõi `origin/main` → `c331d6b`) | không cần |
| 06:00 | Nhánh `rca/exp-2026-11` (`36a3725`) tạo, push lên origin | `git push origin --delete rca/exp-2026-11` (chỉ khi Minh quyết) |
| 06:0x | Đường hầm SSH chỉ đọc tới exp-obs (`127.0.0.1:13200→3200`, `13100→3100`, `19090→9090`) cho bộ kiểm tín hiệu | tắt tiến trình ssh |
