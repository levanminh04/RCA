# T-072 — Kế hoạch E3 (khung S2): nạp luật, kiểm cảnh báo tới nơi, ghi giờ hiệu lực

Trạng thái: **đề xuất, 20/11 21:5xZ; sửa theo CX-07 20/11 22:0xZ, CX-09 21/11 03:1xZ**, chưa chạy. Căn cứ: SPEC T-072 bước 5–6; Minh duyệt (a), (b) theo Codex (LOG T-070 "Lượt 4"); HOP-DONG I1 (d), I5, I7, I12; `ke-hoach-e3-duong.md`. Thay phần "Đề xuất cho E3" của `ke-hoach-e3-duong.md` ở chỗ khác nhau: nay **có** một lượt ×1 1800 s trong E3.

## 0. Ai giữ gì

| Tài nguyên | Chủ ở S2 | Ghi chú |
|---|---|---|
| Grafana (container `flash-ticket-obs-grafana`), `/opt/rca-lab` exp-obs (đổi checkout = đổi Grafana, I7) | **T-072** | chỉ khi không có job nào chạy từ `/opt/rca-lab` |
| Bộ nhận nhẹ T-072 (container trên mạng `flash-ticket-obs-pinned_default`) | **T-072** | compose do T-073 viết diff (mục 4) |
| exp-app, máy tải AWS, `chuoi_tai.py`, lượt `t071-e3-duong-01` | **T-071** | ×1, 1800 s, ngoài mẫu số |
| Prometheus | T-072 truy vấn nhẹ theo khúc khi S2 mở; T-071 xuất chuỗi lượt E3 | I11 |

## 1. Điều kiện trước khi mở S2

1. E2 xong; T-071 đã xuất 8 lượt (`xuat_chuoi.py`, mỗi lượt một thư mục `xuat/<tag>/`) và phân loại phút (`phan_loai_phut.py`, độc lập tín hiệu luật). T-072 không sửa file nào của T-071; đọc qua `chuyen_dinh_dang.py` (CX-07 điểm 1), rồi chạy đúng quy tắc khóa, không chỉnh tay:
   - `py -3 results/T-072/chuyen_dinh_dang.py xuat <E2>/xuat/t071-e2-01-x1 … <E2>/xuat/t071-e2-08-x1 --ra-thu-muc results/T-072/e2/xuat`
   - `py -3 results/T-072/chuyen_dinh_dang.py phut <phân loại phút E2 của T-071>.json --ra results/T-072/e2/phut.json` — thoát 1 (dừng) nếu số phút theo từng nhãn trước/sau khác nhau, có phút trùng, hoặc số phút `khoe-x1` khác `tom_tat.khoe_x1_phut` của T-071.
   - `py -3 results/T-072/cham_offline.py chon-nguong --xuat results/T-072/e2/xuat/*.t072.json --phut results/T-072/e2/phut.json --ra results/T-072/nguong.json`
   - Ghi sha256 của mọi đầu vào (thư mục T-071, file đã chuyển) và của `nguong.json` vào LOG. Route thiếu dữ liệu (< 120 bước) → dừng, trình. So `phut_khoe_x1` mà bộ chấm đếm trên lưới xuất với `khoe_x1_phut` của T-071: chênh = phút khỏe không có chuỗi xuất; báo số đó.
2. Sinh file luật thật (tên DNS dịch vụ bộ nhận T-072 trong compose: **`t072-bo-nhan`**, cổng 9172, đường dẫn `/t072`, T-073 đặt, điều phối báo 20/11 22:0xZ):
   `py -3 results/T-072/sinh_luat_grafana.py --nguong results/T-072/nguong.json --webhook http://t072-bo-nhan:9172/t072 --ra <worktree>/observability/grafana/provisioning/alerting/t072-luat.yaml`
3. Ba commit ở repo lab, trình diff, Minh duyệt, push (I5). P = commit đang chạy trên `/opt/rca-lab` exp-obs ngay trước N (hiện `e9a0857`):
   - **Commit N (nạp):** trên `e9a0857`, gộp file của T-072 và T-073. Phần T-072: `t072-luat.yaml` (11 luật + contact point `t072-bo-nhan-nhe`), **`t072-thu-e3.yaml`** (4 luật thử, đang hoạt động), `t072-thu-e3-go.yaml.mau` và `t072-hoan-tac-n.yaml.mau` (giữ đuôi `.mau`, Grafana không nạp), README, `observability/t072-bo-nhan/bo_nhan.py`; phần T-073: `observability/compose.t073-webhook.yaml` và README của nó (danh sách: `de-xuat-commit-lab.md`).
   - **Commit G (gỡ):** con của N; xóa `t072-thu-e3.yaml`, đổi tên `t072-thu-e3-go.yaml.mau` → `t072-thu-e3-go.yaml` (`deleteRules` cho đúng 4 uid `t072-thu-*`); giữ `t072-hoan-tac-n.yaml.mau`. Xóa file thôi thì **không** xóa luật đã nạp trong DB của Grafana; phải có `deleteRules`.
   - **Commit H (hoàn tác N, chỉ dùng khi N nạp lỗi hoặc một phần; CX-07 điểm 2):** con của P (không chứa file luật nào của N), thêm `t072-hoan-tac-n.yaml` (đổi tên từ `.mau`): `deleteRules` cho 15 uid (11 luật thật + 4 luật thử) và `deleteContactPoints` cho `t072-webhook`. H không chứa `compose.t073-webhook.yaml`, nên bộ nhận phải gỡ **khi còn ở N** (mục 7).
   - **Gốc của nhánh:** `/opt/rca-lab` exp-obs đang ở `e9a0857` (`t071-nen`, có `chuoi_tai.py` mà lượt E3 và E4 cần). Nhánh `t072-luat` tách từ `407b4f5`, nên N phải có `e9a0857` làm tổ tiên (rebase các file mới của T-072 lên `e9a0857`, hoặc gộp `t071-nen`). Giữa hai commit đó `observability/` không đổi; điều phối quyết cách gộp với nhánh của T-073.
4. Điều phối mở S2 trong `LICH-MAY.md` (exp-app nghỉ ngoài lượt E3 của T-071; không job nào chạy từ `/opt/rca-lab` exp-obs).

## 2. Các bước E3 theo thứ tự

Mỗi bước ghi giờ UTC vào LOG T-072; lệnh chạy qua `ssh … 'bash -s' < script` (script giữ ở `results/T-072/e3/`).

| # | Ai | Việc | Kiểm / đầu ra |
|---|---|---|---|
| 1 | T-072 | Chỉ đọc: `git -C /opt/rca-lab rev-parse HEAD`, `git status --porcelain`; `pgrep -af "chuoi_tai|runner4|tai_linux"`; `docker ps` (Grafana, bộ nhận); kiểm cách Grafana lưu lịch sử trạng thái: `docker exec flash-ticket-obs-grafana sh -c 'echo "$GF_UNIFIED_ALERTING_STATE_HISTORY_ENABLED|$GF_UNIFIED_ALERTING_STATE_HISTORY_BACKEND"'` (chỉ in hai biến này, không in env khác); cấu trúc bảng DB Grafana (mục 3) | `e3/truoc.txt`. Có job chạy từ `/opt/rca-lab` → dừng, báo điều phối |
| 2 | T-072 | `git -C /opt/rca-lab fetch && git -C /opt/rca-lab checkout <N>`; ghi commit trước/sau (điều phối ghi `LICH-MAY.md`) | HEAD = N, cây sạch |
| 3 | T-072 | Bật bộ nhận bằng project riêng của T-073 (`results/T-073/trien-khai-bo-nhan.md` §4; không dùng project quan sát, không đụng Prometheus/Grafana/Collector): ảnh `python:3.12-slim` ghim digest, thư mục và file env `E=/srv/rca-lab/runs/t073-<lượt>/webhook.env` theo §3 của file đó (`T072_RA_DIR=/srv/rca-lab/runs/t072-e3-01`); `cd /opt/rca-lab/observability && docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml up -d t072-bo-nhan`, kiểm `… ps` và các container `flash-ticket-obs-*` giữ nguyên giờ Up; ghi một tin thử tay từ trong mạng Docker tới đường dẫn **`/t072-tay`** (không phải `/t072`) để kiểm đường mạng | bộ nhận ghi 1 dòng `/t072-tay`; dòng này không tính là Grafana phát |
| 4 | T-072 | `docker restart flash-ticket-obs-grafana`; chờ `curl -s http://10.0.0.215:3000/api/health` trả `database: ok` | ghi `t_restart_N`, `t_health_N` |
| 5 | T-072 | Xác nhận nạp và được đánh giá (mục 3): 15 uid (11 thật + 4 thử) có trong bảng luật; mọi instance có giờ đánh giá cuối tăng qua 3 lần đọc cách 15 s; không có Error; luật thật ở Normal (không tải) | **giờ hiệu lực E3** = thời điểm sớm nhất mà cả 11 luật thật đã được đánh giá ít nhất một lần sau `t_health_N` và không luật nào Error |
| 6 | T-071 | Phát lượt `t071-e3-duong-01` (×1, 1800 s) bằng `chuoi_tai.py` theo kế hoạch khóa của T-071 | giờ load-start, load-end; T-071 kiểm tiêu chí khỏe như E2 |
| 7 | T-072 | Theo dõi nhẹ: mỗi 5 phút đọc trạng thái 4 luật thử và 11 luật thật (mục 3), danh sách dòng bộ nhận | kỳ vọng: 4 luật thử Pending → Alerting trong vài phút đầu lượt; luật thật **không** bắt buộc Normal (cháy thì ghi, không tính vào E4) |
| 8 | T-072 | Sau load-end ≥ 7 phút (cửa sổ 5 phút + `for` + gửi tin): 4 luật thử về Normal (chặn < 30 request → NoData → OK) → tin resolved | bộ nhận có, mỗi luật thử, ≥ 1 tin `firing` và ≥ 1 tin `resolved` |
| 9 | T-072 | Thu: bộ nhận `webhook.jsonl`; lịch sử trạng thái và trạng thái hiện tại của 15 luật (mục 3); T-071 xuất chuỗi `tin-hieu/*` của lượt E3 (`xuat_tin_hieu.py`, khúc ≤ 600 s) | `e3/` (hash vào LOG) |
| 10 | T-072 | **Chỉ khi** lượt `t071-e3-duong-01` đã xong (`chuoi_tai.py` thoát, T-071 báo nhận đủ) **và** phép đo của T-073 trong lượt đó đã thoát (T-073 báo), kiểm `pgrep -af "chuoi_tai|runner4|tai_linux|stage_b|orchestrator"` rỗng (I7); ghi commit trước (N) và sau (G) để điều phối ghi `LICH-MAY.md`. Gỡ luật thử: `git -C /opt/rca-lab checkout <G>`; `docker restart flash-ticket-obs-grafana`; kiểm 4 uid `t072-thu-*` không còn trong bảng luật; 11 luật thật được đánh giá lại | **giờ hiệu lực E4** = như bước 5, sau lần khởi động lại này. E4 chỉ tính từ giờ này (ghi `e3.md`) |
| 11 | T-072 | Báo điều phối đóng S2; bộ nhận nhẹ chạy tiếp qua E4 để ghi giờ tin của luật thật (chỉ ghi thư mục `t072-*`), tắt sau E4 — **điều phối quyết** | `e3.md` |

## 3. Đọc trạng thái luật và lịch sử trạng thái (không cần token Grafana)

API của Grafana cần đăng nhập; tạo tài khoản dịch vụ/token là tạo quyền truy cập mới (cần Minh). Đề xuất đọc DB của Grafana **chỉ đọc**, không chép DB ra khỏi máy, chỉ lấy cột cần:
`sudo python3 - <<'PY'` mở `file:/var/lib/docker/volumes/flash-ticket-obs-pinned_grafana-data/_data/grafana.db?mode=ro` (sqlite3 của thư viện chuẩn), đọc:
- bảng luật (`alert_rule`: `uid`, `title`, `updated`, `interval_seconds`, `for`) → luật đã nạp;
- trạng thái hiện tại (`alert_instance`: `rule_uid`, `labels`, `current_state`, `current_state_since`, `last_eval_time`) → được đánh giá;
- lịch sử trạng thái (backend mặc định là annotation: bảng `annotation`, các dòng `alert_id` của luật, `prev_state`, `new_state`, `epoch`) → giờ chuyển Pending → Alerting và Alerting → Normal.
**Chưa kiểm:** tên bảng/cột trên Grafana 13.3 (bước 1 đọc `sqlite_master` trước); backend lịch sử trạng thái (nếu là Loki thì đọc qua Loki, truy vấn nhẹ). Đọc DB bằng `sudo` là thao tác chỉ đọc nhưng chạm dữ liệu Grafana: **cần điều phối/Minh đồng ý** khi mở S2. Phương án thay: Minh tạo token chỉ đọc cho API `GET /api/prometheus/grafana/api/v1/rules` và API lịch sử trạng thái.

## 4. Yêu cầu nối bộ nhận vào compose (T-073 viết diff)

- Dịch vụ riêng của T-072 (I12: đường dẫn/cổng riêng), trên mạng `flash-ticket-obs-pinned_default`, **không** mở cổng ra host; nghe `0.0.0.0:9172`, đường dẫn `/t072`. T-073 thêm dịch vụ này vào compose (điều phối giao, CX-07 điểm 4). URL contact point: `http://t072-bo-nhan:9172/t072` (tên DNS `t072-bo-nhan` do T-073 chọn).
- Chạy `observability/t072-bo-nhan/bo_nhan.py --nghe 0.0.0.0:9172 --ra /ra/webhook.jsonl`: file mount chỉ đọc; `/ra` mount `/srv/rca-lab/runs/t072-e3-01/` đọc-ghi; user uid/gid của `ubuntu` (thư mục `runs/` 700); image có `python3` thư viện chuẩn, ghim digest; nếu exp-obs chưa có image đó thì việc tải là việc mới, nêu dung lượng trước.
- Cùng image/kiểu chạy với bộ nhận của T-073 nếu được (một lần kiểm đường mạng cho cả hai).
- Nghiệm thu (Minh, (b)): Grafana phát (không phải tin thử tay), bộ nhận lưu đúng thân tin và giờ nhận, nhận cả tin resolved.

## 5. Kiểm `startsAt` so với lịch sử trạng thái (I1 điểm d)

Với mỗi luật thử (và mỗi luật thật nếu nó cháy) trong E3:
- Δ_bắt_đầu = `startsAt` (tin firing) − giờ chuyển Pending → Alerting trong lịch sử trạng thái; Δ_kết_thúc = `endsAt` (tin resolved) − giờ chuyển Alerting → Normal.
- Đạt nếu |Δ| ≤ 10 s (một nhịp đánh giá) cho mọi luật thử → `da_doi_chieu_E3 = true` (i1-schema). Lệch > 10 s → điều phối mở việc mới (HOP-DONG I1 (d)); T-072 không tự sửa.
- Ghi thêm: độ trễ gửi = `nhan_webhook_utc` − `startsAt`; so t̂ offline (`cham_offline.py cham` với ngưỡng thử 0,005 s trên chuỗi xuất của lượt E3) với lịch sử trạng thái (lệch pha lưới ≤ 10 s là kỳ vọng).

## 6. Bằng chứng: E3 chứng minh gì, không chứng minh gì

- Chứng minh (nếu đạt): luật nạp và được đánh giá trên Grafana 13.3; biểu thức p95 chạy trong Grafana ra giá trị khớp offline; đường Grafana → bộ nhận cho cả firing và resolved; nguồn t̂.
- **Không** chứng minh: luật p95/lỗi nào phát hiện được lỗi thật. Luật thử cháy vì ngưỡng 0,005 s thấp hơn p95 khỏe, không vì lỗi. Bảy luật chưa có dương thật (`p95-booking`, `p95-event`, `p95-ticket`, `loi-booking`, `loi-ticket`, `mat-do`, `mat-gw`) giữ nguyên trạng thái bằng chứng (`ke-hoach-e3-duong.md`).
- Luật thật cháy trong lượt E3: ghi riêng, không tính vào E4 và không dùng để sửa ngưỡng (ngưỡng khóa từ E2).

## 7. Gặp lỗi giữa chừng (luật cứng 21, mức nhẹ vì E3 < 1 giờ máy)

| Lúc | Lỗi | Xử lý |
|---|---|---|
| Bước 4–5 | Grafana không lên, hoặc luật nạp lỗi/một phần/Error | không phát lượt E3. Hoàn tác (không có job nào chạy, I7), theo thứ tự: (1) **khi còn ở N**: `cd /opt/rca-lab/observability && docker compose -p t073-webhook --env-file $E -f compose.t073-webhook.yaml rm -s -f t072-bo-nhan` (cùng `$E` với lệnh `up`; thư mục `t072-e3-01` giữ trên host); (2) `checkout <H>`, `docker restart flash-ticket-obs-grafana`; (3) **kiểm trước khi trả khung:** 15 uid không còn trong bảng luật, `t072-webhook` không còn trong contact point (bảng cấu hình/provenance, mục 3), Grafana `api/health` ok, dashboard hiện hành mở được; container `flash-ticket-t072-bo-nhan` không còn; (4) `checkout <P>` và khởi động lại lần nữa (cây về đúng P; việc gỡ đã ghi vào DB). Ghi commit P → N → H → P. Thư mục Grafana do N tạo còn lại (provisioning không xóa thư mục): ghi, gỡ bằng tay nếu Minh muốn. Trình điều phối |
| Bước 6–8 | Luật thử không cháy, hoặc không có tin | giữ lượt (không phát lại ngay); kiểm đường mạng bằng tin tay `/t072-tay`, nhật ký Grafana (`docker logs --since`); phát lại lượt E3 là lượt mới, cần điều phối |
| Bước 10 | `deleteRules` không gỡ được | **không** mở E4; trình điều phối (phương án: tạm dừng luật thử bằng `isPaused: true` trong commit mới) |

**Chưa kiểm** (phân xử ở bước 1/5 của E3): Grafana 13.3 bỏ qua `deleteRules` với uid chưa tồn tại (cần khi N nạp một phần); thứ tự Grafana áp `deleteRules` và `deleteContactPoints` trong cùng file (contact point còn luật trỏ tới thì không xóa được: nếu lỗi, tách thành hai lần khởi động lại, gỡ luật trước).
