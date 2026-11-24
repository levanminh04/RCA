# Bước 2: dời trên exp-obs (24/11/2026, 16:10–16:25Z)

Kế hoạch: `../KE-HOACH-DON.md` §9 bước 2. Danh sách dời và lệnh ngược đã ghi vào LOG T-070 (19:40Z giờ ghi LOG) trước khi làm.

| File | Nội dung |
|---|---|
| `lenh-1-dung.sh` | `down` bộ nhận (project `t073-webhook`) rồi bộ quan sát (không `-v`) |
| `lenh-2-doi.sh`, `.out` | Tạo thư mục mới, `mv` theo bảng §7.1, chép `receiver.env`; kết quả `stat` |
| `lenh-3-checkout-venv.sh`, `.out` | Checkout lab `85ace52`; dựng venv mới; `pip freeze --all` |
| `lenh-4-bat.sh` | `up` bộ quan sát (project `flash-ticket-obs-pinned` từ `name:`), `up -d t072-bo-nhan` |
| `sau_obs.py`, `obs.json` | Kiểm sau dời (cùng cách đo với `../truoc/obs.json`) |
| `lenh-5-kiem-bo-nhan.sh` | Kiểm đường Grafana → bộ nhận và quyền ghi |

## Kết quả so với bước 0

| Bất biến | Kết quả |
|---|---|
| B2 bản chụp M1 | 149/149 sha256 trùng (`obs.json#/snapshot_sha256`) |
| B3 file ghim, cấu hình V082 | Trùng |
| Chuẩn hồi quy V082 | 4 file trùng |
| B4 venv | `pip freeze --all` 18/18 dòng trùng, kể cả `pip==24.0`; Python 3.12.3 |
| B6 cách ly | user `rca` bị từ chối: đọc `archive/2026-11/runs/t069-chinh.out` (root xác nhận có thật), đi qua `archive/2026-11/runs`, `runs` mới, `ledger`, đọc 5 sổ tiêm. Vẫn đọc được pins và đi qua `cases` (đúng vai) |
| B9 kho dữ liệu | Prometheus 1080 và 22.020, Loki 42.134, Tempo 30.574: trùng bước 0. Không có volume mới (RR3 đạt) |
| B10 dữ liệu hiển thị | 3.676/3.676 file `rca/results/dev` trùng `t065-l11-001`; `GET /public/rca/dev/du-lieu/chi-muc-ban.json` → 200 |
| B11 luật | 11 luật, UID, `title`, nhãn `t072_uid`, receiver trùng; nằm ở folder mới "Cảnh báo FlashTicket", nhóm `canh-bao`; không có bản trùng (RR2 đạt) |
| B12 dashboard | 4 dashboard, UID và folder như cũ |
| Datasource | prometheus, loki, tempo, infinity-rca: OK |
| Bộ nhận | healthy; user 1001; ghi `/srv/flashticket-rca/alerts/bo-nhan` (rw); từ container Grafana kết nối TCP tới `t072-bo-nhan:9172` được. Gửi thông báo thử qua API không làm được: Grafana 13.3.0 trả 410 cho `/api/alertmanager/grafana/config/api/v1/receivers/test`; không gửi dữ liệu giả vào `webhook.jsonl` |
| Đường cũ | `/opt/rca-lab`, `/srv/rca-lab`, `/etc/rca-lab`, `/home/ubuntu/t063` không còn; lab @`85ace52` |

## Còn lại

- Grafana còn 2 folder rỗng: "T-072 W4 cảnh báo" (`cg51evuk4md4wb`, rỗng sau khi luật chuyển sang folder mới) và "T-072 E3 thử" (`ag51evv3jtxxcf`). Xóa qua API là việc nhẹ, chờ Minh duyệt.
- Log Grafana có 1 lỗi: thiếu thư mục `/etc/grafana/provisioning/plugins`. Repo chưa từng có thư mục này nên lỗi có từ trước, không ảnh hưởng.
- Collector agent trên exp-app gửi tới gateway: dữ liệu trong khoảng gateway dừng (16:10:30–16:12:20Z) có thể mất. Lúc đó không có lượt chạy nào.
