# T-071 — thay đổi trên máy

Mọi thay đổi trên exp-app, máy tải, exp-obs do T-071 làm. Giờ UTC lấy từ máy. Chỉ ghi thêm.

## exp-app (129.221.208.47)

| Giờ UTC | Thay đổi | Trước → sau | Kiểm | Hoàn tác |
|---|---|---|---|---|
| 12:59:37Z | Tạo `/home/ubuntu/t071/e1/` (ubuntu); ghi `ticket.out`, `payment.out` (đầu ra psql của hai giao dịch) | chưa có → có | — | `rm -rf /home/ubuntu/t071/e1` |
| 12:59:38.57Z | `ticket_db.ticket_schema.tbl_event_access_snapshots`, dòng `event_id = 3e7c1df9-…`: `event_starts_at`, `event_ends_at`. Một giao dịch, `SELECT … FOR UPDATE` lưu cũ, `UPDATE … WHERE` khớp giá trị cũ, `ROW_COUNT = 1` nếu không thì `RAISE` (giao dịch hủy) | 2026-11-19T22:16:31.402736Z / 2026-11-20T22:16:31.402736Z → 2026-12-03T22:16:31.402736Z / 2026-12-04T22:16:31.402736Z (= `event_db.tbl_events.starts_at/ends_at`) | NOTICE `ticket rows=1`, COMMIT; đọc lại 12:59:54Z khớp Event | `UPDATE … SET event_starts_at='2026-11-19 22:16:31.402736+00', event_ends_at='2026-11-20 22:16:31.402736+00' WHERE event_id='3e7c1df9-…'` (giá trị ở `e1/truoc.jsonl`) |
| 12:59:38.71Z | `payment_db.payment_schema.tbl_event_finance_snapshots`, dòng `event_id = 3e7c1df9-…`: `event_ends_at`. Cùng cách | 2026-11-20T22:16:31.402736Z → 2026-12-04T22:16:31.402736Z (= `event_db.tbl_events.ends_at`) | NOTICE `payment rows=1`, COMMIT; đọc lại khớp | `UPDATE … SET event_ends_at='2026-11-20 22:16:31.402736+00' WHERE event_id='3e7c1df9-…'` |
| 13:01:07–13:01:41Z | Tạo `/home/ubuntu/t071/db-moc/20261120T130107Z/`: `pg_dump -Fc` 5 DB (booking, event, payment, ticket, keycloak), `so-dong.txt`, `trang-thai-{truoc,sau}.txt`, `SHA256SUMS`; tổng 90.027.377 byte. Chỉ đọc DB | đĩa trống 23.186.194.432 → 23.091.245.056 byte | `sha256sum -c` OK; `pg_restore -l` đọc được | `rm -rf /home/ubuntu/t071/db-moc/20261120T130107Z` (không hoàn tác trước khi hết E5: là mốc của I13) |

Không đổi cột khác (`organizer_subject`, `event_status`, `source_config_version`, `received_at`, `fee_rate`, …). Không đổi `event_db`, `booking_db`. Script: `results/T-071/e1/sua_ngay.sh`.

## Máy tải (3.24.8.49)

Chưa có thay đổi.

## exp-obs (213.35.116.128)

| Giờ UTC | Thay đổi | Trước → sau | Kiểm | Hoàn tác |
|---|---|---|---|---|
| 13:24:18Z | Tạo `/srv/rca-lab/runs/t071-xuat/` (ubuntu); chép `xuat_chuoi.py` (`90872186…`), `bieu-thuc.json` (`1a4aee67…`) | chưa có → có | sha256 hai đầu khớp | `rm -rf /srv/rca-lab/runs/t071-xuat` |
| 13:24:56–13:26:16Z | Chạy `xuat_chuoi.py` (chỉ đọc Prometheus, 224 truy vấn, nghỉ 0,3 s); ghi `/srv/rca-lab/runs/t071-xuat-thu-001/` (514 KB), `/srv/rca-lab/runs/t071-xuat-thu-001.start`, `t071-xuat/thu-001.log`, `t071-xuat/thu-001.tgz` (`473a8d6d…`) | chưa có → có | `SHA256SUMS` OK trên máy và sau khi kéo về | xóa các đường dẫn trên (giữ cho tới khi T-071 đóng: luật giữ mọi lượt) |

| 13:33:51–13:36:59Z | Tạo `/srv/rca-lab/runs/t071-chuoi-kho/` (bản sao `load/controller/chuoi_tai.py` để chạy khô, `khai-truoc-e2.json`, `kho/chay-kho-*.json`, `kho/chay-kho-2.out`). Chạy khô gọi `tai_linux.py get` (chỉ đọc) 8 tag + 1 tag cũ đối chứng; `tai-linux-events.jsonl` không thêm sự kiện | chưa có → có | sha256 bản sao = worktree (`73a0105f…`) | `rm -rf /srv/rca-lab/runs/t071-chuoi-kho` |
| 13:58–14:00:37Z | Trong `/srv/rca-lab/runs/t071-chuoi-kho/`: thêm `thu/` (`chuoi_tai.py` bản 2 `5ad71328…`, `tai_gia.py`, `thu_chuoi.py`, `ket-qua-obs.txt`), `thu-chay-<UTC>/` (repo git tạm và kho thử của bộ thử giả: chỉ tai_linux giả và Prometheus giả trên cổng localhost ngẫu nhiên), `kho3/`, `kho3.out`; thay `load/controller/chuoi_tai.py` bằng bản 2, `khai-truoc-e2.json` bằng nháp-4. Chạy khô gọi `tai_linux.py get` (chỉ đọc) 8 tag; `tai-linux-events.jsonl` 428 dòng trước = sau | — | sha256 hai đầu khớp | `rm -rf /srv/rca-lab/runs/t071-chuoi-kho` |
| 14:2x–14:23:58Z | Trong `/srv/rca-lab/runs/t071-chuoi-kho/`: thêm `thu3/` (bản 3 `5ceb3ea1…`, `tai_gia.py`, `thu_chuoi.py`, `ket-qua-obs.txt`), `thu3-chay-<UTC>/` (repo tạm, kho thử giả), `kho4/`, `kho4.out`; thay `load/controller/chuoi_tai.py` bằng bản 3. Chạy khô `get` chỉ đọc 8 tag; `tai-linux-events.jsonl` 428 = 428 | — | sha256 hai đầu khớp | `rm -rf /srv/rca-lab/runs/t071-chuoi-kho` |
| 14:56:36–14:56:37Z | **`/opt/rca-lab` exp-obs: `407b4f5` → `e9a0857`** (`git fetch origin t071-nen`, `git checkout e9a08574…`, detached). Trước: 0 job (`runner4/chuoi_tai/tai_linux/stage_m1/run_m1/xuat_bo_sung/sau_v082/safe_export/xuat_chuoi/k6`), không STOP, cây sạch. `git diff --stat 407b4f5 e9a0857`: 1 file `load/controller/chuoi_tai.py` +540; `-- observability/` 0 dòng (I7: không đổi Grafana). Sau: HEAD `e9a0857`, cây sạch, `chuoi_tai.py` `5ceb3ea1…`, `tai_linux.py` `01cf477d…` (= bản 407b4f5) | `407b4f5` → `e9a0857` | như cột trước | `git -C /opt/rca-lab checkout 407b4f5` (khi không có job) |
Không đổi Prometheus, Grafana. `/opt/rca-lab` chỉ đổi ở dòng 14:56Z.


## E2 (phát 20/11 15:03:22Z)

| Giờ UTC | Máy | Thay đổi | Kiểm | Hoàn tác / dừng |
|---|---|---|---|---|
| 15:03:22Z | exp-obs | Tạo `/srv/rca-lab/runs/t071-e2/` (bản khóa `khai-truoc-e2.json` b63f2e09…, `chuoi.jsonl`, `trang-thai.json`, `chuoi.lock`), `/srv/rca-lab/runs/t071-e2.out`, `t071-e2.phat-utc`; tiến trình `chuoi_tai.py` PID 906913 (setsid nohup, từ /opt/rca-lab e9a0857) | sha256 bản khóa trên máy = laptop | Dừng trước lượt kế: `touch /srv/rca-lab/runs/t071-e2/DUNG`. Dừng khẩn một lượt: `tai_linux.py stop --tag <tag>` (luôn có --tag) |
| 15:03:22–15:03:54Z | exp-app, máy tải | Do `tai_linux.py start` lượt 1 (preflight): kiểm/khôi phục mock, tunnel; cấp mới 20 token PKCE vào `/etc/rca-lab/load-secret/l1-tokens.json` (máy tải); `/srv/rca-lab/load-runs/t071-e2-01-x1/`; container `rca-tai-t071-e2-01-x1` (60419d2f…) | sự kiện ở `/srv/rca-lab/load-controller/tai-linux-events.jsonl` | theo tai_linux; mỗi lượt sau lặp lại cùng loại thay đổi với tag của lượt |

| 21/11 02:46:01–02:56:48Z | exp-obs | Tạo `/srv/rca-lab/runs/t071-e2-xuat/` (`code/` 6 file, `ra/` đầu ra xuất 8 lượt + `tien-do.jsonl`, `xuat.out`, `ra-SHA256SUMS`, `ra.tgz` bb52963a…). `xuat_e2.py` PID 916017: chỉ đọc Prometheus (khúc ≤ 600 s, nghỉ 0,3 s) và `tai-out/t071-e2-*` | sha256 hai đầu khớp | `rm -rf /srv/rca-lab/runs/t071-e2-xuat` (giữ tới khi T-071 đóng) |

| 22/11 05:24:50–06:00:34Z | exp-obs, exp-app, máy tải | E3 (a): `/srv/rca-lab/runs/t071-e3-code/` (`e3_chay.sh` e71f4192…, `e3.out`, `goi-e3.sh` 2546571a…, `xuat-tin-hieu.json` 02740275…), `/srv/rca-lab/runs/t071-e3/` (DA-PHAT, DA-XONG, start.json, get.log, receive.json, k6-phut.json). `tai_linux.py start` lượt `t071-e3-duong-01`: preflight (mock, tunnel, 20 token mới ở máy tải), `/srv/rca-lab/load-runs/t071-e3-duong-01/`, container `rca-tai-t071-e3-duong-01`; receive → `tai-out/t071-e3-duong-01/`. DB: +648 đơn do tải (I13: không sửa) | 12 hash receive khớp; xuất 0 khúc lỗi | xóa hai thư mục `t071-e3*` khi T-071 đóng |

## Laptop — repo lab

| Giờ UTC | Thay đổi | Hoàn tác |
|---|---|---|
| ~13:29Z | `git worktree add D:/Project/rca-lab-wt/T-071 -b t071-nen 407b4f5` (I10); thêm `load/controller/chuoi_tai.py` (chưa add, chưa commit). Checkout chính `D:/Project/flashticket-rca-lab` giữ `407b4f5`, sạch | `git -C D:/Project/flashticket-rca-lab worktree remove D:/Project/rca-lab-wt/T-071; git -C D:/Project/flashticket-rca-lab branch -D t071-nen` |

## E3 (a) — lượt `t071-e3-duong-01` (22/11, ngoài mẫu số E2/E4)

Ghi lại thành bảng riêng (dòng 22/11 05:24:50Z ở mục E2 phía trên là cùng nội dung, nằm lệch bảng; giữ nguyên).

| Giờ UTC | Máy | Thay đổi | Kiểm | Hoàn tác / dừng |
|---|---|---|---|---|
| 05:24:50Z | exp-obs | Tạo `/srv/rca-lab/runs/t071-e3-code/` (`e3_chay.sh` e71f4192…, `e3.out`) và `/srv/rca-lab/runs/t071-e3/` (`start-goi-utc.txt`, `start.json`, `DA-PHAT`, `get.log`, `DA-XONG`, `receive.json`, `k6-phut.json`); tiến trình `e3_chay.sh` PID 928814 (đã thoát 05:56:17Z) | sha256 script hai đầu | `rm -rf` hai thư mục khi T-071 đóng |
| 05:24:50–05:25:26Z | exp-app, máy tải | Do `tai_linux.py start --tag t071-e3-duong-01 --seconds 1800`: preflight mock/tunnel, cấp mới 20 token PKCE vào `/etc/rca-lab/load-secret/l1-tokens.json` (máy tải), `/srv/rca-lab/load-runs/t071-e3-duong-01/`, container `rca-tai-t071-e3-duong-01` (48e5e297…; StartedAt 05:25:26.478Z, FinishedAt 05:55:27.460Z, exit 0) | sự kiện ở `/srv/rca-lab/load-controller/tai-linux-events.jsonl` | theo tai_linux |
| 05:56Z | exp-obs | `receive` → `/srv/rca-lab/load-controller/tai-out/t071-e3-duong-01/` (12 file) | 12 hash khớp | giữ |
| 05:24:50–05:55:27Z | exp-app (DB) | +648 đơn do tải (I13: không sửa DB) | đếm trước/sau `results/T-071/e3/` | không hoàn tác (I13) |
| 05:59:57–06:00:34Z | exp-obs | Chép `goi-e3.sh` (2546571a…) vào `t071-e3-code/`, chạy → `xuat-tin-hieu.json` (02740275…, `.err`); chỉ đọc Prometheus | hash hai đầu | xóa cùng thư mục |

## E4 (22/11, khoa-1 `463cf596…`)

| Giờ UTC | Máy | Thay đổi | Kiểm | Hoàn tác / dừng |
|---|---|---|---|---|
| 06:12:13Z | exp-obs | Tạo `/srv/rca-lab/runs/t071-e4/` và chép bản khóa `khai-truoc-e4.json` | `sha256sum -c` OK | giữ |
| 06:12:15Z | exp-obs | Chạy khô: tạo `/srv/rca-lab/runs/t071-e4-kho/` (`chay-kho-*.json`), `/srv/rca-lab/runs/t071-e4-kho.out`; `tai_linux.py get` chỉ đọc 9 tag | 9/9 tag chưa có | `rm -rf` khi T-071 đóng |
| 10:12:58Z | exp-obs | `/srv/rca-lab/runs/t071-e4.phat-utc`, `t071-e4.out`; kho `t071-e4/` (`chuoi.jsonl`, `trang-thai.json`, `chuoi.lock`); tiến trình `chuoi_tai.py` PID 949967 (setsid nohup, từ `/opt/rca-lab` `ecdeed2`) | HEAD, cây, 0 job, không STOP kiểm trong cùng lệnh | Dừng trước lượt kế: `touch /srv/rca-lab/runs/t071-e4/DUNG`; dừng khẩn một lượt: `tai_linux.py stop --tag <tag>` |
| 10:12:59Z → (đang chạy) | exp-app, máy tải, exp-obs | Mỗi lượt `t071-e4-0N-*` (9 lượt): preflight (mock, tunnel, token mới), `/srv/rca-lab/load-runs/<tag>/`, container `rca-tai-<tag>`, receive → `tai-out/<tag>/`; DB tăng đơn do tải (I13) | theo `chuoi.jsonl` (`phat`, `xong`, `kiem_dat`, `nhan`) | theo tai_linux / chuoi_tai |
| 17:57:26Z | exp-obs | Chuỗi E4 `xong_chuoi` (9/9 xong); PID 949967 thoát; `tai-out/t071-e4-*` 9 thư mục (12 file mỗi lượt, `outputs.sha256` OK) | `chuoi.jsonl` | giữ |
| 19:06:48–19:18:08Z | exp-obs | Tạo `/srv/rca-lab/runs/t071-e4-xuat/` (`code/` 6 file, `ra/` xuất 9 lượt + `tien-do.jsonl`, `xuat.out`, `ra-SHA256SUMS` 424 file, `ra.tgz` e0b01d85…); `xuat_e2.py` PID 979223, chỉ đọc Prometheus (khúc ≤ 600 s) và `tai-out`. Gói dở 19:11Z (b20906ee…) đã xóa trên máy trước khi tạo gói chính | hash hai đầu khớp | `rm -rf /srv/rca-lab/runs/t071-e4-xuat` khi T-071 đóng |
