# Bước 4 (máy tải) và bước 5 (kiểm cuối), 24/11/2026

Kế hoạch: `../KE-HOACH-DON.md` §9 bước 4, §10. Minh duyệt Q3 và Q6. **Q4 (lượt mua vé 10 phút, có phát tải) chưa chạy**, vì theo đề xuất Q4 cần duyệt riêng.

## Bước 4: máy tải (17:0xZ)

| Việc | Kết quả |
|---|---|
| `/srv/rca-lab/load-runs` (47 tag) → `/srv/flashticket-rca/archive/2026-11/load-runs` | 47/47; `runs/` mới ubuntu 755 (như `load-runs` cũ) |
| `/etc/rca-lab` → `/etc/flashticket-rca` | `load-secret` giữ ubuntu 700 |
| `/opt/rca-lab` → `/opt/flashticket-rca` | Checkout `85ace52` (cùng commit với obs và app), cây sạch |
| `/home/ubuntu/{x86-check, uvenv, arm-check*.tgz, rec-x86linux.json, dump_rec.py}` | → `archive/2026-11/home/` |
| `/opt/rca-tai` | Giữ nguyên (Q5) |

Lệnh: `buoc4-tai.sh`. Đầu ra: `buoc4-tai.out`. Đường hầm VNPay không bị ảnh hưởng: khóa đường hầm giới hạn theo cổng, không theo đường dẫn. Ở bước 3 đã kiểm `19091/health` UP.

## Q3 / B13: hồi quy V082 (17:09–17:11Z, obs)

Chạy bằng user `rca`, venv mới `/srv/flashticket-rca/rca/venv`, bản chụp ở `rca/method/b0f79a4d…`, đích `rca/hoi-quy-sau-don/`. Ca `ebd5ef38` chạy với `--dung-lai-dau-vao`, như T-066.

| Ca | Kết luận | `method-output-1/2` | Chuẩn T-066/T-064 |
|---|---|---|---|
| `46aab4be` | CAUSE_FOUND, hạng 1 payment-service | `573df32d…` ×2 | trùng byte |
| `ebd5ef38` | CAUSE_FOUND, hạng 1 payment-service | `563f449d…` ×2 | trùng byte |

Lệnh: `q3-hoi-quy.sh`. Đầu ra: `q3-hoi-quy.out`. Lần chạy đầu in lỗi `sha256sum` vì shell không mở rộng được `*` trong thư mục 750; đã so lại qua `sudo sh -c`.

## Q6: phát lại một ca dev qua tuyến RCA trực tuyến (17:12–17:14Z, obs)

- Ca cũ `2d5a56fe`, capture giả có sẵn ở `rca/online-dev/sim-capture/` (sha256 trùng gói gốc).
- Chạy `rca/online/orchestrator.py mot --t 1795071679` từ `/opt/flashticket-rca` (lab `85ace52`), `RCA_M1_ROOT=/srv/flashticket-rca/rca/online-dev`, đích G1 `rca/results/online-dev-001`. Đây là lần đầu chạy đúng điều kiện L1 mới.
- Không phát tải.
- **Chuỗi xử lý:** stage → P7 → bổ sung → V082 → kiểm đầu vào → G1. Trạng thái `xong`, không bước nào lỗi (`q6/b104d97898.json`, `q6/nhat-ky.jsonl`).
- **So với ca cũ** bằng `check_old_case.py so` (`q6/so-ca-cu.json`; đọc từng mục, không chỉ `trung_tat_ca`):

| Mục | Kết quả |
|---|---|
| Gói ca (5 file) | Trùng hết |
| Đầu vào P7 `method-input.json` | `3ea3dea3…` trùng |
| V082 `method-output-1/2` | `d98b1db3…` trùng; `trung_sha` true |
| Gói bổ sung | `5838e145…` trùng |
| G1 (3 file) | Trùng ngoài khối thêm, không có khóa khác |
| Đồ thị dịch vụ | `service-graph-5`, trạng thái `ok` (`q6/service-graph-60186b05.status.json`) |

Các hash trên trùng với lần phát lại cùng ca ở T-073 (lượt dev-004, `results/T-073/kiem/dev/t073-dev-004/so-ca-cu.json`).

**Dữ liệu sinh ra trên obs:**
- `rca/online-dev/{cases,outputs,v082,bo-sung}/60186b05`;
- `rca/results/online-dev-001/`;
- `runs/2026-11-24-kiem-online-dev/`;
- `rca/hoi-quy-sau-don/`.

## Kiểm tên (`kiem-ten.sh`, ba máy, ngoài `archive/` và `/var/lib/docker`)

| Máy | Còn tên cũ | Lý do |
|---|---|---|
| obs | `ledger/{t069-chinh,t069-lap,t069-thu,t073-e5-01}.jsonl` | Sổ tiêm của các lượt cũ, đặt tên theo lượt; nằm trong thư mục sổ đang dùng (ledger 700). Chưa có trong bảng dời. Đề xuất: chuyển vào `archive/2026-11/ledger/`, giữ chủ `ledger` và quyền 700 |
| app | `/opt/flash-ticket-app/…`, `/opt/flash-ticket-build/…` | Giữ để hoàn tác bước 3; chuyển vào archive khi Minh xác nhận |
| tải | `/opt/rca-tai/k6*/workload-t062*.js` | `/opt/rca-tai` giữ theo Q5 |
