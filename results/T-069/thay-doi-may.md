# T-069 — thay đổi trên máy

Giờ theo `date -u` trên máy. Mọi thay đổi trong "Phạm vi ghi" của SPEC; mục có dấu ⚠ là đường ghi do runner/bộ tiêm đặt sẵn (LOG phiên 2, Bước 0 điểm 0.9).

| # | Giờ (UTC 19/11) | Máy | Thay đổi | Trước → sau | Hoàn tác |
|---|---|---|---|---|---|
| M1 | 06:48:29 | exp-obs | `/opt/rca-lab` `git fetch` + `git checkout ddb22dc` | `ee91432` → `ddb22dc`; chỉ đổi `faults/injectors/docker/inj3.py`, thêm `campaigns/schedules/lich-t069*.json` | `git checkout ee91432` |
| M2 | 06:48:31 | exp-app | như M1 | `5a39028` → `ddb22dc`; 33 file đổi = `git diff --name-only 5a39028 ddb22dc` (`lab-exp-app-truoc.sha256`, `lab-exp-app-sau-checkout.sha256`); Collector agent dùng `observability/collector/` không đổi giữa hai commit | `git checkout 5a39028` |
| M3 | 06:48:43 | exp-app | Ghi `/home/ubuntu/t063/inj/compose-dir` = `/opt/flash-ticket-build/t067-compose/hieu-luc` (sha256 `7109f2c1…`) | file mới trong thư mục trạng thái của `inj3.py` | xóa file (RECREATE-PAY trở về `compose-t062`) |
| M4 | 06:50:40 | exp-obs | Lượt thu thử `t069-thu`: `RCA_DP_OUT=/srv/rca-lab/runs/t069-thu setsid -f nohup python3 -B /opt/rca-lab/campaigns/runner/runner4.py thu --lich /opt/rca-lab/campaigns/schedules/lich-t069-thu.json > /srv/rca-lab/runs/t069-thu.out` | tạo `/srv/rca-lab/runs/t069-thu{,.out}`, sổ `/srv/rca-lab/ledger/t069-thu.jsonl` (user ledger); ca mới trong `/srv/rca-lab/m1/{cases,outputs,v082,bo-sung}/`, ⚠ `m1/export-audit/export-audit-<mã>.json`; chỉ mục G1 `/srv/rca-lab/rca-results`; ⚠ `/srv/rca-lab/load-controller/tai-out/t3-<mã>`, sổ sự kiện bộ tải | giữ (luật cứng 10) |
| M5 | trong M4 | exp-app | Tiêm lỗi theo lịch (toxic, lease hook, ⚠ tạm `/tmp/ctl-<uuid>.json` của `write_lease` rồi xóa); RECREATE-PAY tạo lại container Payment | xem sổ tiêm | bộ tiêm tự gỡ; Payment không hoàn tác (cùng image/cấu hình) |
| M6 | trong M4 | máy tải | ⚠ `/srv/rca-lab/load-runs/t3-<mã>` (runner đặt tag `t3-`, SPEC ghi `t069-*`) | thư mục mới | giữ |
| M7 | 08:26–08:27 | exp-obs | Ca RECREATE-PAY `a707078c` (P7 lỗi adapter): `xuat_bo_sung.py --t 1795075439` → `runs/t069-thu/ca/a707078c/prometheus-bo-sung.json`, cài `m1/bo-sung/a707078c/` (root:rca 640); V082 → `m1/v082/a707078c/`; `sau_v082.py` → chỉ mục G1 `/srv/rca-lab/rca-results/t065-l11-001`; `runs/t069-thu/ca/a707078c.tgz` (`cases/a707078c`) | file mới | giữ |
| — | 08:20–08:32 | exp-app | Chỉ đọc: `docker logs` Booking, SELECT `event_db`, `booking_db` (`information_schema`, `tbl_events`) | không đổi | — |
| M8 | 09:20:14 | exp-app | SQL dời mốc sự kiện `3e7c1df9` +14 ngày (Minh chọn B): `event_db.event_schema.tbl_events` (`sale_ends_at`, `starts_at`, `ends_at`, `checkin_*`), `booking_db.booking_schema.tbl_event_sales_snapshots` (`sale_ends_at`, JSON `saleEndsAt`/`eventStartsAt`/`eventEndsAt`) | `sua-su-kien/truoc.jsonl` → `sau.jsonl` | UPDATE ngược −14 ngày theo `truoc.jsonl` |
| M9 | 09:20:33–09:33:57 | exp-obs, máy tải | Tải kiểm `t069-kiem-ban-001` 180 s (`tai-out/t069-kiem-ban-001`, `load-runs/t069-kiem-ban-001`) | thư mục mới | giữ |
| M10 | 09:34:20 | exp-obs, exp-app | `/opt/rca-lab` → `ca5d6f5` (thêm `lich-t069-chinh.json`) | `ddb22dc` → `ca5d6f5` | `git checkout ddb22dc` |
| M11 | 09:34:55 | exp-obs | Lượt chính `t069-chinh` (như M4 với `lich-t069-chinh.json`, `RCA_DP_OUT=/srv/rca-lab/runs/t069-chinh`) | như M4–M6 | giữ |
| M12 | 18:39:49–20:45:36 | exp-obs, exp-app | `/opt/rca-lab` → `407b4f5` (thêm `lich-t069-lap.json`); lượt lặp `t069-lap` (như M11) | như M4–M6 | giữ |
| M13 | 18:29:58–18:31:36 | exp-obs | Ca RECREATE-PAY `c4d7999f` (P7 lỗi adapter): như M7 (`runs/t069-chinh/ca/c4d7999f*`, `m1/bo-sung/c4d7999f/`, `m1/v082/c4d7999f/`, chỉ mục G1) | file mới | giữ |
| — | 18:31 | exp-app | Chỉ đọc: `kiem_db.sh` (count, `pg_indexes`, `EXPLAIN` không chạy câu lệnh, `pg_stat_user_tables`) | không đổi | — |
