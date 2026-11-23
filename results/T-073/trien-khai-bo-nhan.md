# T-073 — Bộ nhận webhook trong container: diff, triển khai, hoàn tác

Bản 2, phiên `rca-w5`, giờ máy 20/11/2026 ~22:0xZ. Bản 1 sửa theo Codex CX-07 (`results/T-070/codex/CX-07.jsonl`): thêm bộ nhận nhẹ của T-072 (I12), lệnh `down` truyền đủ biến. Theo quyết định Minh (LOG T-070 "Lượt 4", 14:49Z): "(b) duyệt cách nối: bộ nhận trong container trên mạng Docker của Grafana; nghiệm thu = Grafana phát, bộ nhận lưu đúng tin và giờ nhận, nhận cả thông báo resolved. Commit/triển khai theo diff trình riêng." **Chưa commit, chưa triển khai.**

## 1. Diff (worktree `D:/Project/rca-lab-wt/T-073`, nhánh `t073-truc-tuyen`, gốc `407b4f5`)

| File | Thay đổi |
|---|---|
| `observability/compose.t073-webhook.yaml` | **mới**: project Compose `t073-webhook`, hai service |
| `campaigns/online/README.md` | cách chạy bộ nhận T-073 bằng container (file mới của T-073) |
| `observability/compose.yaml` | **không đổi** |

| Service | Dùng ở | Tên DNS trên mạng chung, URL contact point | Chạy | Gắn vào |
|---|---|---|---|---|
| `t072-bo-nhan` | E3 (T-072, kiểm giao nhận) | **`t072-bo-nhan`** → `http://t072-bo-nhan:9172/t072` | `python -B /app/bo_nhan.py --nghe 0.0.0.0:9172 --ra /ra/webhook.jsonl` | `./t072-bo-nhan` → `/app` chỉ đọc; `${T072_RA_DIR}` (`/srv/rca-lab/runs/t072-e3-01`) → `/ra` đọc-ghi |
| `t073-webhook` | E5 (T-073, chế độ (b)) | **`t073-webhook`** → `http://t073-webhook:8080/t073/canh-bao` | `python -B /app/webhook_receiver.py --nghe 0.0.0.0:8080 --duong-dan /t073/canh-bao --spool /spool` | `../campaigns/online` → `/app` chỉ đọc; `${T073_SPOOL_DIR}` → `/spool` đọc-ghi |

Chung cho cả hai: cùng image Python chính thức ghim digest qua biến bắt buộc `T073_WEBHOOK_IMAGE` (một lần kiểm đường mạng cho cả hai, theo `results/T-072/ke-hoach-e3.md` §4); uid:gid `1001:1001` (ubuntu, chủ `/srv/rca-lab/runs` 700); `read_only: true`; `mem_limit: 64m`; `restart: unless-stopped`; log json-file 10 MB × 3; mạng `obs` = `flash-ticket-obs-pinned_default` khai `external`; **không publish cổng ra host**; mọi bind dạng dài với `create_host_path: false` (thiếu thư mục/file thì `up` báo lỗi, không để Docker tạo thư mục bằng root). Healthcheck: T-073 gọi `GET /t073/canh-bao/song`; T-072 kiểm cổng 9172 nghe (bộ nhận T-072 không có GET).

`bo_nhan.py` là file của T-072 (worktree `D:/Project/rca-lab-wt/T-072`, nhánh `t072-luat`, `observability/t072-bo-nhan/bo_nhan.py`). T-073 **không chép, không sửa**: compose gắn nó chỉ đọc từ checkout triển khai. Vì vậy commit triển khai lên `/opt/rca-lab` phải chứa cả file của T-072 (gộp hai nhánh, điều phối trình Minh); thiếu file thì `up` lỗi ở bước gắn.

## 2. Vì sao project riêng, không thêm service vào `compose.yaml`

| Cách | Ảnh hưởng tới service khác | Hoàn tác |
|---|---|---|
| Thêm service vào `observability/compose.yaml` | `docker compose -p flash-ticket-obs-pinned up -d` sau khi đổi file có thể tạo lại service có cấu hình lệch (Grafana gắn `./grafana/provisioning` theo checkout, I7); phải nhớ luôn chỉ định tên service | Sửa lại file chính + `rm -s` service |
| **Project riêng, mạng external** (chọn) | `up`/`down` chỉ chạm hai container `flash-ticket-t072-bo-nhan`, `flash-ticket-t073-webhook`; không tạo lại, không khởi động lại Prometheus, Loki, Tempo, Grafana, Collector | `down` project riêng; file chính không đổi |
| Cổng trên host + luật tường lửa (a) | Đổi cấu hình bảo mật máy | Minh không chọn |

Điều kiện thất bại: (1) project quan sát bị `down`/tạo lại mạng → hai container mất kết nối, phải `up -d` lại project này; Docker không xóa được mạng chung khi container còn gắn → dừng project này **trước**. (2) Grafana phải dùng URL theo tên dịch vụ; Grafana đã ở mạng này với alias `grafana` (`docker inspect` 20/11 12:59Z).

## 3. Biến: một file env cho mọi lệnh

Compose nội suy cả file cho **mọi** lệnh (`up`, `ps`, `logs`, `stop`, `down`) và dừng khi thiếu biến bắt buộc. Nên ba biến đặt trong một file env của lượt, và mọi lệnh dùng `--env-file` cùng file đó:

```
# /srv/rca-lab/runs/t073-<lượt>/webhook.env   (ubuntu, 600; không chứa bí mật)
T073_WEBHOOK_IMAGE=python@sha256:<digest>
T073_SPOOL_DIR=/srv/rca-lab/runs/t073-<lượt>/spool
T072_RA_DIR=/srv/rca-lab/runs/t072-e3-01
```

Kiểm trên laptop (Docker 28.3.2, `docker compose … config`; daemon không chạy):

| Trường hợp | Kết quả |
|---|---|
| Đủ ba biến | đạt; hai service đúng lệnh, user, bind (chỉ đọc ở `/app`), alias, không `ports`, mạng external `flash-ticket-obs-pinned_default` |
| Thiếu `T073_WEBHOOK_IMAGE` | dừng: `required variable T073_WEBHOOK_IMAGE is missing a value` |
| Thiếu `T072_RA_DIR` | dừng: `required variable T072_RA_DIR is missing a value` |
| Thiếu `T073_SPOOL_DIR` | dừng: `required variable T073_SPOOL_DIR is missing a value` |
| `down --dry-run` không biến | dừng ở nội suy (như trên) — lý do phải truyền đủ biến khi `down` |
| `down --dry-run` đủ biến | qua nội suy; dừng ở bước nối Docker daemon (laptop không bật daemon) |

Chưa chạy container thật, chưa kéo image.

## 4. Triển khai (chỉ ở khung có Grafana, I7; người làm khung đó)

Điều kiện: Minh duyệt commit (gồm file T-072); nhánh được push; `/opt/rca-lab` trên exp-obs đổi sang commit đó **khi không có job** (I7); ghi commit trước/sau vào `LICH-MAY.md`. Đổi checkout ở exp-obs là đổi Grafana — chỉ ở S2 (E3) hoặc S4 (E5).

1. Image: `docker pull python:3.12-slim` (tải image ~50 MB, việc tải theo luật của khung), lấy digest `docker image inspect --format '{{index .RepoDigests 0}}' python:3.12-slim`; ghi digest vào LOG khung và vào file env.
2. Bằng ubuntu: `install -d -m 0700 /srv/rca-lab/runs/t073-<lượt>/spool /srv/rca-lab/runs/t072-e3-01`; viết `webhook.env` như §3, `chmod 600`.
3. `cd /opt/rca-lab/observability; E=/srv/rca-lab/runs/t073-<lượt>/webhook.env`
   - E3: `docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml up -d t072-bo-nhan`
   - E5: `docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml up -d t073-webhook`
4. Kiểm: `docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml ps` (`healthy`); `docker ps` — các container `flash-ticket-obs-*` giữ nguyên thời gian Up.
5. Contact point Grafana (thuộc file luật của T-072): E3 `http://t072-bo-nhan:9172/t072`; E5 `http://t073-webhook:8080/t073/canh-bao`. Ghi URL vào `LICH-MAY.md`. Nghiệm thu theo Minh: Grafana phát (không phải tin thử tay), bộ nhận lưu đúng thân tin và giờ nhận, nhận cả `resolved`.

## 5. Hoàn tác

Luôn dùng cùng file env với lệnh `up`:

- Gỡ cả hai: `docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml down` — xóa hai container; mạng chung không bị xóa (external); thư mục `/srv/rca-lab/runs/t072-e3-01`, `/srv/rca-lab/runs/t073-<lượt>/spool` và file env **giữ nguyên trên host** (giữ mọi lượt, luật cứng 10; không dùng `down -v`, project không có volume).
- Gỡ riêng bộ nhận E3 sau E3: `docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml rm -s -f t072-bo-nhan`.
- Gỡ contact point trỏ tới hai URL trên (phần của T-072).
- Trả `/opt/rca-lab` về commit cũ nếu cần: theo I7, ghi `LICH-MAY.md`.
