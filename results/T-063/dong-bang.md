# T-063 — Hồ sơ đóng băng đợt thu dev bản 2 (13/11/2026 03:44Z)

Bản máy đọc: [`dong-bang/dong-bang.json`](dong-bang/dong-bang.json) (sha256 `993dc85b…`; thu bằng `dong-bang/dong_bang.py`, chỉ đọc).

- **Ứng dụng:** 7 service `ft-local/<svc>:arm64-t062-6b21ed55`, Keycloak `ft-local/keycloak:arm64-776d9c9e` (WHY-84); image ID từng container ở `#/exp_app_image_id`. Repo FlashTicket cục bộ HEAD `fba6bc8` (không dùng để build lại).
- **Cấu hình `exp-app`:** Collector cách A + httpcheck + lọc health (TD-04), proxy `booking-amqp` + Booking nối qua proxy (TD-05), hạ tầng nhãn log + log autovacuum (TD-06), app nhãn log (TD-07), span bọc job Keycloak (TD-08); hash ở `#/exp_app_file_sha256` (env chỉ băm, không đọc).
- **Cấu hình `exp-obs`:** Prometheus 30d/40GiB (TD-01), nhãn queue/bảng (TD-02); hash `pinned/*.json` ở `#/exp_obs_file_sha256`; M1 P7 ghim (`stage-m1.py`, `run-m1.py`, `m1-p7-config.json`, `safe-export.py`) cùng chỗ.
- **Tải:** kịch bản hành trình L1 (`results/T-062/tai-2/k6/hanh-trinh.js`, `cau-hinh.json`, `chay-tai.ps1` — hash `#/laptop_file_sha256`), 12 hành trình/10 s (70/20/5/5), FLASH và HTTP5-EVENT-FLASH: ×3 từ giây 600 (`-BuocTai 600 -Multiplier 3`); tunnel mock remote trên `exp-app` (`Test-L1Duong` trước mỗi Start).
- **Tiêm:** `results/T-063/tiem-loi/inj2.py` (hash trên laptop và `/home/ubuntu/inj2.py` trùng — kiểm ở `#/laptop_file_sha256`, `#/exp_app_file_sha256`); danh mục ô `results/T-063/chay/D2B-KET-QUA.md`.
- **Bộ chạy:** `results/T-063/chay/runner2.py`; lịch `results/T-063/chay/lich-2.json` (13 chu kỳ); đóng gói bổ sung `results/T-063/dong-goi/xuat_bo_sung.py` (bản 3).
- **Tiêu chí chọn T-064** `results/T-064/tieu-chi-chon.md` hash `e6513b0e…` (không đổi).

## Bản 2 — 13/11/2026 07:13Z (sau sửa REVIEW T-063 R1/R2 và chuyển bộ chạy lên `exp-obs`)

Bản máy đọc: [`dong-bang/dong-bang-2.json`](dong-bang/dong-bang-2.json). Thu bằng `dong_bang.py dong-bang-2.json`. Bản 1 giữ nguyên, không ghi đè.

Khác bản 1, có lý do:
- `inj2.py` (cả laptop và `exp-app`): sửa R1 (`verify`/`cleanup` báo lỗi, tự hết hạn toxic/pause), thêm `psi_cpu_may` (R4).
- `collector/config.json`: TD-09 (đổi tên log hạ tầng; `results/T-063/quan-sat/thay-doi-may.md`).
- `runner2.py`: sửa R1.
- Mới: `runner3.py`, `tai_linux.py` (L1d), bản sao k6, lịch và `xuat_bo_sung.py` ở `exp-obs:~/rca-dieu-phoi/`.

Đã kiểm hash trùng giữa repo và bản đang chạy (`#/laptop_file_sha256` đối chiếu `#/exp_obs_file_sha256` và `#/exp_app_file_sha256`): `runner3.py`, `tai_linux.py`, `k6/hanh-trinh.js`, `k6/cau-hinh.json`, `lich-2.json`, `xuat_bo_sung.py`, `inj2.py`.

Không đổi: danh sách container và image ở cả hai máy, cờ retention Prometheus, `tieu-chi-chon.md` của T-064 (`e6513b0e…`), lịch `lich-2.json` (`9bc6a329…`).

**Bộ chạy của lượt chính:** `runner3.py thu --lich lich-2.json` trên `exp-obs`. Hồ sơ luật 21 ở `chay/HO-SO-LUOT.md`, phụ lục 13/11 ~06:15Z.

## Bản 3 — 14/11/2026 06:14Z (thu bù 3, phiên B)

Bản máy đọc: [`dong-bang/dong-bang-3.json`](dong-bang/dong-bang-3.json). Thu bằng `thu3/scripts/dong_bang_3.py dong-bang-3.json` (bản sao `dong_bang.py`, thêm file thu3; từ chối ghi đè). Bản 1, bản 2 giữ nguyên. Bản chạy trước khi chốt điều kiện xác nhận giữ ở `dong-bang/dong-bang-3-truoc-chot.json` (khác duy nhất hash `thu3/dieu-kien-xac-nhan-3.md`).

**Thay đổi duy nhất về ứng dụng: image Event.** `flash-ticket-event-service-event-service-1`: `sha256:20dd6a11…` (`arm64-t062-6b21ed55`) → `sha256:01493da5…` (`arm64-t063h3-76b34d5e` = `6b21ed55` + bản vá hook H3, commit nhánh `e557307`). Lý do: hook `pool.hold` chỉ chạy ở Booking nên POOL-EVENT không thử được; Minh duyệt sửa hook (DECISIONS 14/11). Chi tiết, lệnh, hoàn tác: `thu3/thay-doi-may.md` T3-03…T3-05.

Khác bản 2, không phải thay đổi cấu hình:
- container payment có Id mới (`a541c049…`, cùng image `arm64-t062-6b21ed55`, cùng compose/env) do chạy thử RECREATE-PAY 06:11Z (`thay-doi-may.md` T3-13);
- file mới: `inj3.py`, `runner4.py`, `lich-3.json`, script thu3 (danh sách ở `#/exp_app_file_sha256`, `#/exp_obs_file_sha256`, `#/laptop_file_sha256`).

Không đổi (đối chiếu `dong-bang-2.json`, mọi khóa chung trùng hash): Collector, compose/env `-t062` của mọi service (env chỉ băm), Toxiproxy, `inj2.py`, `runner3.py`, `tai_linux.py`, k6, `xuat_bo_sung.py`, M1 P7 ghim, cờ retention Prometheus, container `exp-obs`, `tieu-chi-chon.md` T-064.

**Bộ chạy:** `runner4.py thu --lich lich-3.json` trên `exp-obs` (`RCA_DP_OUT=~/rca-dieu-phoi/thu3`). Lịch 6 chu kỳ; hồ sơ luật 21 ở `thu3/KE-HOACH.md` §8 và bổ sung 5. Điều kiện xác nhận khai trước: `thu3/dieu-kien-xac-nhan-3.md` (sha256 `9dbdca16…`; dòng "Chốt" ghi 06:16Z, giờ ghi thật 06:14:03Z — lệch do ghi giờ ước trong tiêu đề, giữ nguyên để khớp hash đã đóng băng). Nhãn `service.version` trong telemetry Event vẫn là `6b21ed55…` (lấy từ env).
