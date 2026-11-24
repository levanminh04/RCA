# Bước 0: hiện trạng trước khi dời (chỉ đọc)

Đây là số đo "trước" của kế hoạch dọn [`../KE-HOACH-DON.md`](../KE-HOACH-DON.md) (bản 3, §9 bước 0). Sau khi dời, các phép kiểm ở §10 so lại với file này.

- **Thời điểm chụp:** 24/11/2026, khoảng 15:37Z. Giờ chính xác của từng máy nằm ở trường `utc` trong file JSON.
- **Cách chụp:** chạy `buoc0.py` trên từng máy bằng lệnh `sudo -n python3 - <may>`, đưa script qua `../../kiem-ke/tho/lenh/ssh.sh`.
- **Script chỉ đọc**, với hai ngoại lệ:
  - tạo một thư mục tạm trong `/tmp` trên obs để thử tải một gói từ PyPI, rồi xóa ngay;
  - mở một giao dịch `read only` trên PostgreSQL và kết thúc bằng `rollback`.
- **Không có giá trị bí mật trong file:**
  - biến môi trường chỉ ghi tên kèm `sha256:` 16 ký tự hex;
  - lệnh khởi động (`cmd`) của container nào có đối số mang chữ pass/secret/token/key thì chỉ ghi hash. Đây là trường hợp của postgres và redis.
  - Đã kiểm: mọi giá trị env trong ba file đều ở dạng hash.

| File | Máy | Nội dung |
|---|---|---|
| `obs.json` | exp-obs | Container; sha256 của bản chụp M1 (149 file); các file ghim; chuẩn hồi quy; `pip freeze` của venv; sha256 bộ hiển thị `t065-l11-001` (3.676 file); quyền thư mục; phép cách ly; cờ STOP; thử PyPI; luật, folder, dashboard và contact point Grafana; số mẫu từ kho dữ liệu; quét đường cũ |
| `app.json` | exp-app | Container (env đã hash, mount, bộ nhớ, mạng, cấu hình log); nội dung `compose-dir`; quyền thư mục; sha256 các env file; số đơn trong DB theo trạng thái; tiến trình chạy trần; quét đường cũ |
| `tai.json` | máy tải | 106 container k6 đã thoát (đầu ra, `container.log`, cỡ log Docker); 4 ngoại lệ; quyền thư mục; cổng 19091; quét đường cũ |
| `buoc0.py` | — | Script đã chạy |

## Số chính

Đường dẫn ghi theo dạng `file#/trường` trong JSON.

| Hạng mục | Giá trị | Nguồn |
|---|---|---|
| Bản chụp M1 | 149 file | `obs.json#/snapshot_sha256` |
| File ghim | `m1-source-pins.json` `8aebdf2a…`; `m1-p7-config.json` `eb7dddd7…`; cấu hình V082 `01a64b60…` (khớp T-066) | `obs.json#/ghim_sha256` |
| Chuẩn hồi quy | `46aab4be` `573df32d…` ×2; `ebd5ef38` `563f449d…` ×2 (khớp T-066) | `obs.json#/hoi_quy_chuan_sha256` |
| Venv | Python 3.12.3; 18 dòng `pip freeze --all`, có `pip==24.0` | `obs.json#/venv_python`, `#/venv_pip_freeze` |
| PyPI từ obs | Tải được (`rc` 0, `six-1.16.0`). RR10 đạt | `obs.json#/pypi` |
| Cách ly | Mọi phép thử bằng user `rca` đều bị từ chối (trả 1). Gồm `test -r` trên `runs/t069-chinh.out` (root xác nhận file có thật), `test -x` trên `runs` và `ledger`, và `test -r` trên 5 file sổ tiêm | `obs.json#/cach_ly` |
| Cờ STOP | Cả hai đều không có | `obs.json#/stop` |
| Grafana | 11 luật, cùng folder `cg51evuk4md4wb` ("T-072 W4 cảnh báo"), nhóm `t072-w4`, receiver `t072-bo-nhan-nhe`; 4 dashboard; 1 contact point `t072-webhook` | `obs.json#/grafana` |
| Mẫu kho dữ liệu (23/11 03:00–04:00Z) | Prometheus: `sum(count_over_time(up[1h]))` = 1080; số chuỗi span metrics = 22.020. Loki (`service_name`): 42.134 dòng. Tempo: 30.574 trace | `obs.json#/mau_kho` |
| DB đơn (`booking_db`) | CANCELLED 10.510; COMPLETED 41.705; EXPIRED 11.398 | `app.json#/db_don` |
| `compose-dir` | `/opt/flash-ticket-build/t067-compose/hieu-luc` | `app.json#/compose_dir` |
| Container app | 14 đang chạy. Service Spring: `NetworkMode=host`, bộ nhớ 768 MiB hoặc 1 GiB. Keycloak và hạ tầng ở mạng `flash-ticket-infra`. `rca-toxiproxy` chạy `-host=127.0.0.1 -port=8474 -config=/config/proxies.json`, mạng host, nhãn `t062=topology`, restart `unless-stopped`, bộ nhớ 128 MiB | `app.json#/containers` |
| Container k6 máy tải | 106 đã thoát; ngoại lệ đúng 4: `rca-tai-d2-2e071903`, `rca-tai-verify-001..003` | `tai.json#/k6_container` |
| Filesystem | obs và app: `/dev/sda1`; máy tải: `/dev/nvme0n1p1` (lệnh `df` hiện là `/dev/root`). `/opt`, `/srv`, `/etc`, `/home` cùng filesystem trên mỗi máy | `*.json#/findmnt` |

## Phát hiện mới so với kế hoạch bản 3

Những điểm này cần ghi vào kế hoạch trước bước 1. Đề xuất sửa nằm ở LOG T-070.

1. **Grafana còn một folder rỗng "T-072 E3 thử (gỡ trước E4)"** (uid `ag51evv3jtxxcf`).
   - 4 luật thử và contact point `t073-webhook-e5` đều không còn.
   - Vì vậy bỏ hai file `*-go.yaml` là an toàn: điều kiện ở §6 đạt.
   - Folder rỗng có thể xóa qua API (việc nhẹ).
2. **`compose-exp/_common.yml` không được Keycloak dùng.** `keycloak.yml` không có `extends`. Ba bind thật của Keycloak (`docker inspect`) khớp đúng ba dòng 14–16 đã ghi ở §7.2.
3. **Quét đường cũ:** obs 1.045 file, app 1.389 file, máy tải 4.559 file (file văn bản dưới 1 MiB trong `/opt`, `/etc`, `/home`, `/root`).
   - **Máy tải:** 0 file trùng.
   - **obs:** chỉ `/etc/passwd`, `/etc/passwd-` và `.bash_history`. Dòng trong `/etc/passwd` là `rca:x:997:987::/opt/flash-ticket-rca:/usr/sbin/nologin`: thư mục nhà của user `rca` trỏ tới một đường đã không còn từ trước đợt dọn. Đường này không thuộc bảng dời và lượt hồi quy T-066 đã chạy được với hiện trạng ấy. Đề xuất giữ nguyên, không sửa user.
   - **app:** ngoài các file đã có trong bảng dời, chỉ có file lịch sử trong `/home/ubuntu` (chuyển vào archive) và cache `buildx`.
   - **app:** file của nhóm trong `/opt/flash-ticket-infra/deploy/` (`app/keycloak.yml`, `scripts/deploy-service.sh`, `app/README.md`) nhắc `/opt/flash-ticket-*`. Các file này **không** được stack đang chạy dùng. Chúng là bản sao file triển khai của nhóm, đi theo thư mục `infra/` và giữ nguyên nội dung.
   - Không thấy cron, unit hay script nào ngoài kiểm kê trỏ tới đường cũ.
4. **Bước quét dùng `find -size -1024k`.** Lần chạy đầu trên obs dùng `-size -1M` nên chỉ bắt file rỗng. Đã sửa rồi chạy lại cả ba máy; các file JSON ở đây là bản đã sửa.
