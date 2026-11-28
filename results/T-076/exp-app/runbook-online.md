# Runbook: bật RCA trực tuyến cho diễn tập demo (T-076 bước 10)

**Trạng thái: NHÁP bản 2, 28/11/2026, chưa được Minh duyệt. Không chạy bất kỳ bước nào trước khi Minh duyệt bản này** (SPEC bản 6, bước 10). Bản 2 sửa theo phiên phản biện bổ sung 28/11 (F1–F8; LOG T-076) và đổi đường dẫn bộ nhận `/t073/canh-bao` → `/canh-bao`.

Mục đích: một lượt trọn vòng trên bản FlashTicket demo ở exp-app: tải mua vé → tiêm lỗi → Grafana cảnh báo → RCA trực tuyến chế độ (b) → trang ca trên dashboard. Tiêu chí đạt là C6 của SPEC, dùng lại tiêu chí E5 đã khóa (`results/T-073/khai-truoc-e5.json#/tieu_chi/ket_qua_chuc_nang`, `#/N`). Đây là diễn tập một ca: chỉ chứng minh đường tích hợp chạy được trên bản mới, không đánh giá độ chính xác RCA.

## 1. Điều kiện trước khi bắt đầu

| # | Điều kiện | Kiểm bằng |
|---|---|---|
| D1 | Bước 9 xong: exp-app chạy bản demo build từ commit merge PR #17, kiểm tín hiệu đạt, bản ghim demo ghi đủ (C5) | `results/T-076/exp-app/` của bước 9 |
| D2 | T-070 `REVIEW-6` đã kiểm bản sửa lab R1/R2 và Minh kết luận về RCA trực tuyến | `tasks/T-070-dieu-phoi-giai-doan-2/` |
| D3 | Lab commit có sửa R1/R2 và đường dẫn bộ nhận `/canh-bao` (sau `da9c843`, sau khi Codex kiểm) đã push và có trên obs, cây sạch | `git -C /opt/flashticket-rca rev-parse HEAD`, `git status --porcelain` rỗng |
| D4 | Minh duyệt các điểm lệch SPEC ở §3 và các commit lab DEMO/HOAN-TAC (§3) với SHA cụ thể | LOG T-076 |
| D5 | Sự kiện tải còn hạn bán ở giờ demo (hạn hiện tại 02/12/2026 22:16Z; Q9 kiểm ở bước 8) | bước 8 |
| D6 | Không có job khác trên ba máy: `pgrep -af 'chuoi_tai|tai_linux|stage_b|orchestrator|inject.py|xuat_chuoi'` rỗng; không có `STOP` cũ ở `/srv/flashticket-rca/load/` và `/srv/flashticket-rca/runs/STOP` (bộ điều phối dừng theo file chung này, `orchestrator.py:54,93`) | lệnh đọc |
| D7 | Container payment của bản demo đúng tên mà `inject.py` dùng (`flash-ticket-payment-service-payment-service-1`) | `docker ps` trên exp-app (bước 8 ghi tên thật) |
| D8 | Sổ tiêm trên obs (như E5, `results/T-073/e5/e5_luot.sh`) và quyền `sudo -n -u ledger` cho thao tác viên | bước 8 |
| D9 | Minh mở được Grafana: đường hầm SSH tới cổng 3000 của obs (Grafana chỉ nghe ở IP riêng, `observability/compose.yaml:74`) và phiên đăng nhập của Minh. Cần cho A5, A6, B12 | Minh |

Thiếu điều kiện nào thì không bắt đầu; ghi lý do vào `demo.md`.

## 2. Tham số khai trước (điền trước giờ chạy, không đổi sau khi bắt đầu)

| Tham số | Giá trị đề xuất | Ghi chú |
|---|---|---|
| Tên lượt | `online-demo-001` | bộ G1 mới, chỉ một tiến trình ghi (T-070 REVIEW-5 đề xuất bước 10) |
| Thư mục lượt (obs) | `/srv/flashticket-rca/runs/<ngày>-online-demo/` | `OUT` của bộ điều phối; spool mặc định `OUT/spool` |
| Bộ G1 | `/srv/flashticket-rca/rca/results/online-demo-001`, khởi tạo `chep:/srv/flashticket-rca/rca/results/dev` | giữ ca cũ để xem được trên dashboard |
| Tag tải | `demo-<ngày>-001` | tag mới; `tai_linux` từ chối tag đã dùng |
| Thời lượng tải | `--seconds 2100`, mức ×1 | tiêm muộn nhất ở giây 900 (B9); t̂ có thể tới mốc tiêm + 600 s; gói cần dữ liệu tới t̂ + 600 s → 900 + 600 + 600 = 2100 |
| Ô tiêm | `PAUSE-PAYMENT`, `--seconds 600` | `docker pause` payment; không cần hook Booking (C6) |
| N | 25 phút từ t̂ | E5 `#/N` |
| Tổng thời gian | tiêm ở giây 600: ~51 phút (chuẩn bị ~15 + tới t̂ ≈ giây 656 + chờ kết quả tới t̂ + 25 phút); tiêm muộn nhất giây 900: tới ~65 phút; hoàn tác thêm ~10 | SPEC: ≤ 1 giờ cho phần chạy — trường hợp tiêm muộn vượt (§3) |

## 3. Điểm lệch SPEC cần Minh quyết (đề xuất, chưa kiểm)

SPEC bản 6 ghi: "thêm integration vào contact point hiện có **qua API Grafana**", "sinh dashboard đọc nguồn đó bằng `build_dashboards.py`", áp và hoàn tác "trên `c1da15f`" (dòng 101), tổng "≤ 1 giờ", và Phạm vi ghi lab không gồm `observability/grafana/` (dòng 77). Runbook lệch ở năm chỗ; duyệt runbook nghĩa là Minh duyệt cả năm chỗ này (mở rộng phạm vi ghi lab):

| Việc | SPEC | Đề xuất | Lý do | Mặt trái |
|---|---|---|---|---|
| Đích cảnh báo | API Grafana | **File provisioning** như E5 (T-073): file mới thêm integration `t076-webhook-demo` → `http://t073-webhook:8080/canh-bao` vào contact point `t072-bo-nhan-nhe`; hoàn tác bằng file `deleteContactPoints` | (1) cách file đã chạy được ở E5 (thêm, bấm Test, gỡ) và image Grafana ở E5 cùng digest với lab hiện tại, nên bằng chứng áp đúng bản đang chạy; (2) contact point `t072-bo-nhan-nhe` do file tạo, thêm integration vào nó qua API chưa ai kiểm; (3) cấu hình nằm trong commit, dễ hoàn tác và dễ chuyển sang chỗ khác. Ở cả hai cách Minh đều phải đăng nhập Grafana (D9); cách API thì Minh phải tự gọi API bằng phiên admin vì agent không cầm mật khẩu | restart Grafana hai lần (bật, hoàn tác); trạng thái cảnh báo đánh giá lại sau restart; thêm hai commit lab |
| Nguồn dashboard | chạy `build_dashboards.py` trên obs | **sinh sẵn trên laptop** (`RCA_G1_BO=online-demo-001 py -3 -B observability/grafana/build_dashboards.py`, đúng cách docstring của script ghi), gộp vào commit DEMO cùng đích cảnh báo | một lần checkout bật cả hai, một lần checkout hoàn tác cả hai; chạy trên obs làm cây `/opt/flashticket-rca` bẩn suốt lượt (4 file dashboard có git theo dõi) | nếu Minh chọn API cho điểm trên thì chạy trên obs nhẹ hơn, hoàn tác bằng `git checkout -- observability/grafana/dashboards` |
| Gốc lab | `c1da15f` | commit D3 (sau `da9c843`: sửa R1/R2 của T-070 REVIEW-5, đường dẫn `/canh-bao`) | bước 10 cần bản sửa `g1_b.py` (khởi tạo đủ) và tên đường dẫn mới | đổi revision ghim của bước 10 |
| Phạm vi ghi lab | không gồm `observability/grafana/` | thêm `observability/grafana/provisioning/alerting/t076-demo*.yaml` và 4 file `observability/grafana/dashboards/*` (chỉ trong commit DEMO/HOAN-TAC) | cần cho hai điểm đầu | mở rộng phạm vi SPEC |
| Thời lượng | ≤ 1 giờ | ~51 phút khi tiêm ở giây 600; tới ~65 phút khi phải chờ nền sạch tới giây 900 | không tiêm khi nền chưa sạch (B9, F1) | trường hợp chậm vượt 1 giờ |

Phương án thứ ba cho điểm đầu, **chưa kiểm trên 13.3**: vẫn dùng file, nhưng nạp lại bằng `POST /api/admin/provisioning/alerting/reload` (Minh gọi bằng phiên admin) thay cho restart; lời gọi lỗi thì quay về restart. Bước A5 (bấm Test) phân xử được mọi phương án trước khi chạy tải. Dùng cùng tên bộ `online-demo-001` cho mọi lượt diễn tập, để chỉ phải làm DEMO/HOAN-TAC một lần.

Hai commit lab, Minh duyệt trước (D4), đặt trên commit D3:

- **DEMO**: thêm `observability/grafana/provisioning/alerting/t076-demo.yaml` (integration) và `t076-demo-go.yaml.mau` (`deleteContactPoints` uid `t076-webhook-demo`; Grafana không nạp đuôi `.mau`); 3–4 dashboard sinh lại với `RCA_G1_BO=online-demo-001` (chỉ khác tên bộ; script dừng nếu còn sót tên cũ).
- **HOAN-TAC** (con của DEMO): xóa `t076-demo.yaml`; đổi `t076-demo-go.yaml.mau` → `t076-demo-go.yaml`; dashboard về bản D3 (trùng byte). Lý do giữ file `deleteContactPoints`: chỉ xóa file thêm thì integration đã nạp **không** bị gỡ (E5 §5).

Nếu Minh giữ đúng SPEC (API): Minh tự gọi API bằng tài khoản của Minh (agent không cầm mật khẩu); lưu JSON contact point trước/sau; hoàn tác `DELETE /api/v1/provisioning/contact-points/<uid>`. Runbook giữ nguyên các bước khác.

## 4. Các bước

Mỗi bước ghi giờ UTC và kết quả vào `results/T-076/exp-app/demo.md`. Máy: **obs** (Grafana, bộ nhận, bộ điều phối, điều khiển tải), **app** (FlashTicket, tiêm lỗi), **tải** (k6, điều khiển từ obs).

### A. Chuẩn bị (không tải, không tiêm)

1. **Kiểm chỉ đọc (D1–D8).** Thêm: `docker ps` trên obs có `flash-ticket-obs-*`, `flash-ticket-t072-bo-nhan` Up; ghi `HEAD` lab ở cả ba máy.
2. **Dựng bộ G1 mới** (obs, root): `sudo python3 -B /opt/flashticket-rca/rca/online/g1_b.py --chi-khoi-tao --ra /srv/flashticket-rca/rca/results/online-demo-001 --khoi-tao chep:/srv/flashticket-rca/rca/results/dev`. Đạt khi in `"khoi_tao": "chep"` (lượt diễn tập sau dùng lại bộ: `"da_co"`); bản sửa R2 dừng nếu nguồn thiếu chỉ mục/đồ thị hoặc đích dở. Ghi số file và sha256 của `du-lieu/chi-muc-ban.json` hai bên.
3. **Bộ nhận T-073** (obs, ubuntu):
   - `install -d -m 0700 /srv/flashticket-rca/runs/<ngày>-online-demo/spool`
   - tạo `/srv/flashticket-rca/runs/<ngày>-online-demo/receiver.env` = chép `/srv/flashticket-rca/alerts/receiver.env`, chỉ đổi `T073_SPOOL_DIR` sang spool mới (không sửa file dùng chung; `T072_RA_DIR` giữ nguyên để không tạo lại `t072-bo-nhan`)
   - `cd /opt/flashticket-rca/observability/alert-receiver && docker compose -p t073-webhook --env-file /srv/flashticket-rca/runs/<ngày>-online-demo/receiver.env -f compose.yaml up -d t073-webhook`
   - đạt khi `t073-webhook` healthy và `t072-bo-nhan` giữ nguyên thời gian Up.
4. **Đổi checkout sang DEMO** (obs): cây sạch, không job (D6) → `git -C /opt/flashticket-rca checkout <DEMO>`; ghi SHA trước/sau. Restart Grafana: `docker restart flash-ticket-obs-grafana` (như E5), chờ `/api/health` ok, ghi `version`/`commit`; log không có `level=error` của `provisioning.alerting`/`provisioning.dashboard` (dòng `provisioning.plugins … no such file` đã có từ trước, ghi lại, không tính).
5. **Kiểm đường Grafana → spool:** giao diện Contact points: `t072-bo-nhan-nhe` có **hai** integration; 11 luật giữ uid/biểu thức/ngưỡng (`rules.yaml`). Lưu sha256 `webhook.jsonl` của `t072-bo-nhan` → bấm Test của integration `t076-webhook-demo` → spool mới có đúng một dòng `TestAlert`, `webhook.jsonl` không đổi. Không thấy hai integration hoặc spool không nhận → hoàn tác §C, không đi tiếp.
6. **Kiểm dashboard đọc đúng bộ:** trang "RCA — sự cố" liệt kê đủ ca cũ (số ca = chỉ mục `dev`); mở một ca cũ, có đồ thị con và danh sách hạng; URL panel chứa `public/rca/online-demo-001`. Ảnh chụp.
7. **Phát bộ điều phối** (obs): `RCA_ONLINE_OUT=/srv/flashticket-rca/runs/<ngày>-online-demo setsid -f nohup python3 -B /opt/flashticket-rca/rca/online/orchestrator.py chay --ra /srv/flashticket-rca/rca/results/online-demo-001 > /srv/flashticket-rca/runs/<ngày>-online-demo/orchestrator.out 2>&1 < /dev/null`. Đạt khi log đọc tin Test và gom thành sự cố lớp `quan-sat` (không chạy RCA).

### B. Chạy

8. **Tải** (obs): `python3 -B /opt/flashticket-rca/load/controller/tai_linux.py start --tag demo-<ngày>-001 --seconds 2100`. Ghi `StartedAt` từ `get`.
9. **Chờ nền ≥ 600 s rồi kiểm điều kiện C6 trên file sự cố, không dùng log** (F1). Bộ gom nhập cảnh báo mới vào sự cố cũ cùng lớp, ở mọi trạng thái, nếu t̂ mới ≤ `t_het` lớn nhất + 300 s; còn cảnh báo chưa hết thì coi như vô hạn (`incidents.py:172–174, 193–194`; WHY-109). Ví dụ Q4: bốn luật p95 cháy trong nền, hết muộn nhất ở giây 483 sau khi bắt đầu tải; tiêm ở giây 600 thì t̂ ≈ giây 656 ≤ 783, ca tiêm bị nhập vào ca nền, không chạy RCA mới.
   - Kiểm (obs): `python3 -c 'import json,glob,time; c=[json.load(open(p)) for p in glob.glob("/srv/flashticket-rca/runs/<ngày>-online-demo/su-co/*.json")]; h=[s for s in c if s["lop"]=="he-thong"]; mo=[s["ma"] for s in h if any(a.get("t_het") is None for a in s["canh_bao"])]; t=max([a["t_het"] for s in h for a in s["canh_bao"] if a.get("t_het")] or [0]); print(json.dumps({"ca_he_thong": [s["ma"] for s in h], "dang_mo": mo, "tiem_duoc_tu_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t + 301)) if t else None, "bay_gio_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}))'`
   - Tiêm được khi `dang_mo` rỗng **và** giờ hiện tại sau `tiem_duoc_tu_utc` (không có ca `he-thong` nào thì không có ràng buộc này). Thêm: luật p95/5xx/liveness đang bình thường; cảnh báo lớp quan sát (`t072-mat-do`, `t072-mat-gw`) đã hết.
   - Ca nền (nếu có) cũng chạy RCA và hiện trên dashboard: ghi mã, t̂, kết quả vào `demo.md`, tách khỏi ca tiêm.
   - Chưa đạt → chờ trong thời lượng tải còn lại, tối đa tới giây 900 kể từ khi bắt đầu tải; quá mốc đó → dừng tải, ghi **"nền chưa sạch"**, không tiêm (không ghi "bỏ sót").
10. **Tiêm, sổ ghi trên obs theo cách E5** (`results/T-073/e5/e5_luot.sh`; F4). Giờ lấy từ đồng hồ obs, không gõ tay; ghi **trước** lệnh tiêm, rồi ghi đầu ra của lệnh tiêm:
    - mốc (obs): `printf '{"utc": "%s", "event": "mark", "cell": "PAUSE-PAYMENT", "tag_tai": "demo-<ngày>-001"}' "$(date -u +%FT%T.%6NZ)" | sudo -n -u ledger python3 -B /opt/flashticket-rca/rca/lib/ledger_append.py /srv/flashticket-rca/ledger/demo-<ngày>.jsonl`
    - tiêm (app, ngay sau mốc): `python3 -B /opt/flashticket-rca/faults/injectors/docker/inject.py start PAUSE-PAYMENT --seconds 600` — lưu nguyên đầu ra một dòng JSON và mã thoát.
    - ghi đầu ra vào sổ (obs): bản ghi `{"event": "fault-start", "cell": "PAUSE-PAYMENT", "inj": <đầu ra>}`, hoặc `fault-start-failed` kèm `rc` nếu mã thoát khác 0. Đầu ra tiêm chỉ vào sổ, không vào `demo.md`.
    - Bộ hẹn giờ của `inject.py` tự `unpause` khi hết 600 s; `inject.py verify` sau đó phải báo sạch.
11. **Theo dõi** (chỉ đọc): spool có cảnh báo `he-thong` (ghi `startsAt` = t̂ và `nhan_webhook_utc`); log bộ điều phối qua các bước stage → P7 → bổ sung → V082 → kiểm đầu vào → G1.
12. **Đo đích cuối:** làm mới trang "RCA — sự cố" (trang đặt `refresh: ""`); ghi giờ UTC lần đầu thấy mã ca, mở ca, có đồ thị con và danh sách hạng; lưu ảnh và phản hồi API của panel danh sách.
13. **Chấm theo C6** (sau lượt; sổ tiêm chỉ đọc lúc này):
    - **Đạt:** có sự cố `he-thong` với t̂ ∈ [mốc tiêm, mốc tiêm + 600 s); `che_do_b.kiem_t.t_loi_bang_t_hat = true`; V082 `trung_sha = true`; mở được trang ca trong N = 25 phút từ t̂.
    - **Bỏ sót:** không có sự cố `he-thong` trong cửa sổ — kết quả, không lặp.
    - **Quá N:** có sự cố nhưng trang ca hiện sau 25 phút hoặc không hiện.
    - Thiếu phủ đầu vào V082 báo riêng (WHY-111), không tính hỏng tuyến khi chức năng đạt. Cảnh báo lớp quan sát ghi riêng.
14. **Nhận đầu ra tải** (obs): `tai_linux.py get --tag …` tới khi `Running=false`, rồi `receive`.

### C. Hoàn tác (đảo thứ tự; giữ mọi dữ liệu)

1. Dừng bộ điều phối (F2; như E5 `results/T-073/e5/hoan-tac/s5-1-stop.txt`): `touch /srv/flashticket-rca/runs/<ngày>-online-demo/STOP` chỉ chặn bước mới, **không** làm tiến trình thoát (`orchestrator.py:216–228` là vòng `while True`). Đọc `su-co/*.json`: không còn ca `dang_chay` (ca đang chạy thì chờ ghi `xong` hoặc `loi`). Sau đó dừng đúng tiến trình bằng SIGTERM: `pkill -TERM -f 'orchestrator.py chay --ra /srv/flashticket-rca/rca/results/online-demo-001'`; kiểm `pgrep -af orchestrator.py` rỗng; ghi PID và giờ.
2. Cây sạch, không job → `git -C /opt/flashticket-rca checkout <HOAN-TAC>`; `docker restart flash-ticket-obs-grafana`; health; log không lỗi provisioning.
3. Kiểm: `t072-bo-nhan-nhe` còn **một** integration `t072-webhook`; 11 luật như trước; dashboard đọc lại `public/rca/dev` (mở một ca cũ).
4. Dừng bộ nhận T-073: `docker compose -p t073-webhook --env-file /srv/flashticket-rca/runs/<ngày>-online-demo/receiver.env -f /opt/flashticket-rca/observability/alert-receiver/compose.yaml stop t073-webhook` (dùng `stop`, không `down`: cùng project có `t072-bo-nhan` chạy liên tục).
5. Giữ trên host: spool, env của lượt, bộ `online-demo-001`, đầu ra tải, sổ tiêm. `inject.py verify` báo sạch.
6. Lab ở lại `HOAN-TAC` (file `deleteContactPoints` có hiệu lực, chạy lại không đổi gì). Đổi commit lab về sau: kiểm cây sạch, không job.
7. Đơn mua phát sinh trong DB thử do lượt k6 không hoàn tác được bằng đổi image/commit (giới hạn đã nêu ở SPEC bước 8).

Nếu Minh muốn **giữ** cấu hình demo để trình bày lại: bỏ C2–C4; chỉ dừng bộ điều phối khi không dùng.

## 5. Gặp lỗi giữa chừng

| Lúc | Hiện tượng | Xử lý | Chạy lại gì, mất bao lâu |
|---|---|---|---|
| A2–A7 (chưa tải) | bước kiểm không đạt (khởi tạo, hai integration, Test, dashboard) | hoàn tác §C phần đã làm | sửa nguyên nhân rồi làm lại A; ~15 phút |
| B8–B9 (tải, chưa tiêm) | tải lỗi; hoặc tới giây 900 vẫn chưa đạt điều kiện B9 (ghi "nền chưa sạch") | dừng tải (`tai_linux.py stop --tag …`), không tiêm; giữ dữ liệu | lượt mới với tag mới, cùng bộ `online-demo-001`; ~50 phút |
| B10–B12 (đã tiêm) | bộ điều phối lỗi một bước | ghi `loai_loi`; chấm "lỗi xử lý"; không tiêm lại trong cùng lượt | lượt mới chỉ khi lỗi hạ tầng có bằng chứng (E5 `#/ca_nghiem_thu/so_lan`, tối đa 3) |
| B10–B12 | không có cảnh báo trong cửa sổ | chấm "bỏ sót" — là kết quả | không lặp; trình Minh (C6: luật im vì thiếu mẫu → kiểm đường thu; nền khỏe vẫn cháy → T-072 xét ngưỡng) |
| bất kỳ | payment không tự `unpause` | `inject.py stop PAUSE-PAYMENT`, rồi `verify` | — |
| bất kỳ | demo trước người xem mà tuyến hỏng | phát lại offline ca E5, ghi rõ là phát lại (C6) | — |

## 6. Ghi kết quả

`results/T-076/exp-app/demo.md`: SHA lab ở các bước, tham số §2, giờ từng bước, ba mốc E5 (tiêm → cảnh báo t̂ và `nhan_webhook_utc` → ca hiện), mã ca, kết quả chấm C6, ảnh, lệnh hoàn tác đã chạy.

## 7. Chưa kiểm

- Cách file provisioning trên commit lab mới (đã chạy ở E5 trên bản lab cũ `ecdeed2`, cùng digest image Grafana; bố cục lab đã đổi sau đợt dọn 11/2026). Nạp lại bằng `POST /api/admin/provisioning/alerting/reload` thay restart: chưa kiểm trên 13.3.
- Đường dẫn bộ nhận mới `/canh-bao`: mới kiểm biên dịch và cú pháp YAML trên laptop; chạy thật ở A3 (healthcheck `…/canh-bao/song`) và A5 (bấm Test).
- Tên container payment và máy đặt sổ tiêm trên bản demo mới (D7, D8 — bước 8).
- `build_dashboards.py` đọc `git show ab1c52c:…` nên cần commit đó trong lịch sử của checkout dùng để sinh (laptop có).
- Thời gian thật từ t̂ tới lúc trang ca hiện trên bản mới (E5 đo trên bản cũ; N = 25 phút là mục tiêu tạm).
