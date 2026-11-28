# Runbook: bật RCA trực tuyến cho diễn tập demo (T-076 bước 10)

**Trạng thái: NHÁP bản 3, 28/11/2026, chưa được Minh duyệt. Không chạy bất kỳ bước nào trước khi Minh duyệt bản này** (SPEC bản 6, bước 10). Bản 3 sửa theo Codex `REVIEW-7` (R1–R5, R9; bảng phản hồi cuối bản đó). Bản 2 (sửa theo phản biện bổ sung F1–F8) và bản 1 xem lịch sử git của file này.

Mục đích: một lượt trọn vòng trên bản FlashTicket demo ở exp-app: tải mua vé → tiêm lỗi → Grafana cảnh báo → RCA trực tuyến chế độ (b) → trang ca trên dashboard. Tiêu chí đạt là C6 của SPEC, dùng lại tiêu chí E5 đã khóa (`results/T-073/khai-truoc-e5.json#/tieu_chi/ket_qua_chuc_nang`, `#/N`). Đây là diễn tập một ca: chỉ chứng minh đường tích hợp chạy được trên bản mới, không đánh giá độ chính xác RCA.

## 1. Điều kiện trước khi bắt đầu

| # | Điều kiện | Kiểm bằng |
|---|---|---|
| D1 | Bước 9 xong: exp-app chạy bản demo build từ commit merge PR #17, kiểm tín hiệu đạt, bản ghim demo ghi đủ (C5) | `results/T-076/exp-app/` của bước 9 |
| D2 | T-070 `REVIEW-6` đã kiểm bản sửa lab R1/R2 và Minh kết luận về RCA trực tuyến | `tasks/T-070-dieu-phoi-giai-doan-2/` |
| D3 | Lab ở **đúng** commit `94bb11e` (sửa R1/R2 của T-070, đường dẫn `/canh-bao`) hoặc commit Minh chỉ định sau D2; đã push và có trên obs, cây sạch | `git -C /opt/flashticket-rca rev-parse HEAD`, `git status --porcelain` rỗng |
| D4 | Minh duyệt các điểm lệch SPEC ở §3, bảng nơi ghi §3.2 và các commit lab DEMO/HOAN-TAC với SHA cụ thể | LOG T-076 |
| D5 | Sự kiện tải còn hạn bán ở giờ demo (hạn hiện tại 02/12/2026 22:16Z; Q9 kiểm ở bước 8) | bước 8 |
| D6 | Không có job khác trên ba máy: `pgrep -af 'chuoi_tai|tai_linux|stage_b|orchestrator|inject.py|xuat_chuoi'` rỗng; không có `/srv/flashticket-rca/runs/STOP` (STOP chung, `orchestrator.py:54,93`) | lệnh đọc |
| D7 | Container payment của bản demo đúng tên mà `inject.py` dùng (`flash-ticket-payment-service-payment-service-1`); đầu dò payment trong Prometheus (`httpcheck_status`, cổng của payment trên bản demo) | `docker ps` trên exp-app; bước 8 ghi tên và cổng thật |
| D8 | Sổ tiêm trên obs (như E5, `results/T-073/e5/e5_luot.sh`) và quyền `sudo -n -u ledger` cho thao tác viên | bước 8 |
| D9 | Minh mở được Grafana: đường hầm SSH tới cổng 3000 của obs (Grafana chỉ nghe ở IP riêng, `observability/compose.yaml:74`) và phiên đăng nhập của Minh. Cần cho A1, A5, A6, B12, C3 | Minh |
| D10 | Khung thời gian Minh duyệt (§2): ~75 phút cộng phần chờ ca đang xử lý | Minh |

Thiếu điều kiện nào thì không bắt đầu; ghi lý do vào `demo.md`.

## 2. Tham số khai trước (điền trước giờ chạy, không đổi sau khi bắt đầu)

Mỗi **lần phát** có một mã riêng `<L>` = `<ngày>-<số thứ tự>` (ví dụ `20261201-01`). Lượt bị ngắt giữ nguyên; lần phát sau tăng số thứ tự. Bộ G1 **hiển thị** giữ tên cố định để dùng lại một cặp commit DEMO/HOAN-TAC (REVIEW-7 R3).

| Tham số | Giá trị đề xuất | Ghi chú |
|---|---|---|
| Mã lần phát | `<L>` | dùng chung cho OUT, spool, env, tag, sổ |
| Thư mục lượt (obs) | `/srv/flashticket-rca/runs/online-demo-<L>/` | `OUT` của bộ điều phối; spool `OUT/spool`; mỗi lần phát một thư mục mới, nên không có `STOP`, `spool-da-doc.json`, `su-co/` của lần trước |
| Bộ G1 hiển thị | `/srv/flashticket-rca/rca/results/online-demo-001`, khởi tạo lần đầu `chep:/srv/flashticket-rca/rca/results/dev` | tên cố định; giữ ca cũ để xem được trên dashboard; chỉ một tiến trình ghi (khóa theo OUT) |
| Tag tải | `demo-<L>` | `tai_linux` từ chối tag đã dùng |
| Sổ tiêm (obs) | `/srv/flashticket-rca/ledger/demo-<L>.jsonl` | như E5 |
| Thời lượng tải | `--seconds 2100`, mức ×1 | tiêm muộn nhất ở giây 900 (B9); t̂ có thể tới mốc tiêm + 600 s; gói cần dữ liệu tới t̂ + 600 s → 900 + 600 + 600 = 2100. Profile có `gracefulStop` thêm tối đa 90 s |
| Ô tiêm | `PAUSE-PAYMENT`, `--seconds 600` (cửa sổ danh nghĩa) | `docker pause` payment; hẹn gỡ tự động `seconds + 5` (`inject.py:149`); không cần hook Booking (C6) |
| N | 25 phút từ t̂ | E5 `#/N` |
| Khung thời gian | xem dưới | trình Minh (D10) |

**Khung thời gian** (giây; dự toán theo giả định, chưa gồm chờ ca đang xử lý trước đó):

| Trường hợp | Chuẩn bị A | Tới mốc tiêm | Tiêm → t̂ | Chờ N | Hoàn tác C | Tổng |
|---|---|---|---|---|---|---|
| Tiêm giây 600, t̂ sau 56 s (như E5) | 900 | 600 | 56 | 1500 | 600 | ~61 phút |
| Tiêm giây 600, t̂ sát cuối cửa sổ | 900 | 600 | 600 | 1500 | 600 | ~70 phút |
| Tiêm giây 900, t̂ sát cuối cửa sổ | 900 | 900 | 600 | 1500 | 600 | ~75 phút |

Đề xuất: Minh duyệt khung ~75 phút cộng phần chờ thực tế ghi rõ trong `demo.md`. Không rút N, không tiêm khi nền chưa sạch để vừa giờ. Nếu một giờ là giới hạn cứng: tách A (chuẩn bị) và C (hoàn tác) thành hai phiên Minh duyệt riêng, hoặc dời lượt. Độ trễ 56 s của E5 đo trên bản cũ, không là lời hứa cho bản mới.

## 3. Điểm lệch SPEC cần Minh quyết (đề xuất, chưa kiểm)

SPEC bản 6 ghi: "thêm integration vào contact point hiện có **qua API Grafana**", "sinh dashboard đọc nguồn đó bằng `build_dashboards.py`", áp và hoàn tác "trên `c1da15f`" (dòng 101), tổng "≤ 1 giờ", và Phạm vi ghi lab không gồm `observability/grafana/` (dòng 77). Runbook lệch ở năm chỗ; duyệt runbook nghĩa là Minh duyệt cả năm chỗ này. Codex `REVIEW-7` (bảng "Năm lựa chọn") đề xuất cùng hướng ở bốn chỗ đầu; chỗ thời lượng đề xuất khung ~75 phút như §2.

| Việc | SPEC | Đề xuất | Lý do | Mặt trái |
|---|---|---|---|---|
| Đích cảnh báo | API Grafana | **Chỉ dùng file provisioning + restart**, như E5 (T-073): file thêm integration `t076-webhook-demo` → `http://t073-webhook:8080/canh-bao` vào contact point `t072-bo-nhan-nhe`; hoàn tác bằng file `deleteContactPoints` | (1) đã chạy ở E5 (thêm, Test, gỡ, đọc lại sau restart: `results/T-073/e5/hoan-tac/s5-4-kiem-sau-restart.txt`); image Grafana ở E5 (`ecdeed2`) và `94bb11e` cùng digest; (2) contact point `t072-bo-nhan-nhe` do file tạo, thêm integration qua API chưa ai kiểm; (3) cấu hình nằm trong commit, dễ hoàn tác và mang sang chỗ khác | restart Grafana hai lần; luật đánh giá lại sau restart (chọn lúc chưa tải) |
| Nguồn dashboard | chạy `build_dashboards.py` trên obs | **sinh sẵn trên laptop** (Git Bash: `RCA_G1_BO=online-demo-001 py -3 -B observability/grafana/build_dashboards.py`; PowerShell đặt `$env:RCA_G1_BO` trước), gộp vào commit DEMO | một checkout bật cả hai, một checkout hoàn tác cả hai; chạy trên obs làm cây `/opt/flashticket-rca` bẩn suốt lượt | script viết lại 4 file; chỉ đưa vào commit file có diff (dự kiến `00-start-here/start.json`, `20-incidents/rca-incidents.json`, `30-replay/rca-replay.json`); kiểm diff chỉ đổi tên bộ, giữ UID |
| Gốc lab | `c1da15f` | **đúng** `94bb11e` (D3), hoặc commit Minh chỉ định sau D2; DEMO/HOAN-TAC đặt trên đúng commit đó | bước 10 cần bản sửa `g1_b.py` và đường dẫn `/canh-bao`; "sau `da9c843`" không chỉ một bản duy nhất | đổi revision ghim của bước 10; khi gốc lab đổi phải dựng lại cặp DEMO/HOAN-TAC (áp lại đúng diff cấu hình, so với dev của gốc mới) |
| Phạm vi ghi lab | không gồm `observability/grafana/` | thêm `observability/grafana/provisioning/alerting/t076-demo.yaml`, `t076-demo-go.yaml.mau` (DEMO), đổi tên thành `t076-demo-go.yaml` (HOAN-TAC), và các dashboard có diff | cần cho hai điểm đầu | mở rộng phạm vi SPEC; không sửa bộ sinh, `rules.yaml`, `providers.yaml` |
| Thời lượng | ≤ 1 giờ | khung ~75 phút cộng phần chờ thực tế (§2) | không tiêm khi nền chưa sạch (B9) | vượt 1 giờ; phương án giữ 1 giờ ở §2 |

Không dùng API hay `POST /api/admin/provisioning/alerting/reload` trong runbook này: dùng chung với file sẽ có hai nơi quản lý một đích (REVIEW-7 R5), và quyền reload khác quyền đăng nhập UI (chưa kiểm). Nếu Minh muốn API, cần soạn một nhánh riêng có bước thêm/gỡ UID và đổi nguồn dashboard tương ứng, không nạp file integration.

### 3.1. Hai commit lab (Minh duyệt SHA trước, D4), đặt trên commit D3

- **DEMO**: thêm `observability/grafana/provisioning/alerting/t076-demo.yaml` (integration) và `t076-demo-go.yaml.mau` (`deleteContactPoints` uid `t076-webhook-demo`; Grafana chỉ nạp `.yaml`/`.yml`, nên không nạp đuôi `.mau`); các dashboard có diff, sinh với `RCA_G1_BO=online-demo-001`.
- **HOAN-TAC** (con của DEMO): xóa `t076-demo.yaml`; đổi `t076-demo-go.yaml.mau` → `t076-demo-go.yaml`; dashboard về bản D3 (trùng byte). Giữ file `deleteContactPoints` vì chỉ xóa file thêm thì integration đã nạp **không** bị gỡ (E5 §5).

Dùng lại cặp này cho mọi lần phát cùng gốc lab (bộ hiển thị cố định). Ghi SHA D3, DEMO, HOAN-TAC và `git diff D3 DEMO --stat`, `git diff DEMO HOAN-TAC --stat` vào LOG trước khi Minh duyệt.

### 3.2. Nơi bước 10 sẽ ghi (Minh duyệt cùng runbook)

| Máy | Ai ghi | Đường | Giữ sau hoàn tác |
|---|---|---|---|
| obs `/opt/flashticket-rca` | thao tác viên | checkout D3 → DEMO → HOAN-TAC (chỉ đổi file trong §3.1) | ở HOAN-TAC |
| obs Grafana | restart | contact point thêm/gỡ integration `t076-webhook-demo`; dashboard đọc `public/rca/online-demo-001` rồi về `dev`; trạng thái luật đánh giá lại | trạng thái về như trước (C3) |
| obs `/srv/flashticket-rca/runs/online-demo-<L>/` | ubuntu, bộ nhận, bộ điều phối | `receiver.env`, `spool/`, `spool-da-doc.json`, `su-co/`, `ca/`, `nhat-ky.jsonl`, `orchestrator.out`, `STOP`, `.lock` | giữ |
| obs `/srv/flashticket-rca/rca/` | bộ điều phối qua `sudo` (user rca) | `stage_b.py` → `cases/<id>`; `run_m1.py` → `outputs/<id>`; `bo-sung/<id>/`; `v082/`; `results/online-demo-001/` (G1: file ca, `du-lieu/chi-muc-ban.json`, `<bản>/chi-muc.json`) | giữ |
| obs `/srv/flashticket-rca/load/` | `tai_linux.py` | `tai-linux-events.jsonl`, `tai-out/demo-<L>/` (nhận đầu ra), trạng thái lệnh | giữ |
| máy tải | `tai_linux.py start` (`preflight(force=True)`) | `/srv/flashticket-rca/runs/demo-<L>/` (k6); làm mới pool token người mua (file quyền 600) | giữ |
| app | `tai_linux.py start` (`preflight`) | có thể khởi động lại mock thanh toán (`RECOVER=True`) và tunnel nếu hỏng; ghi sự kiện ở obs | giữ |
| app | `inject.py` | `/srv/flashticket-rca/faults/inject-state/` (pid, hạn pause, log hẹn giờ); `docker pause`/`unpause` payment | trạng thái sạch (`verify`) |
| app DB demo | k6 | đơn mua phát sinh | không hoàn tác được (SPEC bước 8) |
| obs `/srv/flashticket-rca/ledger/demo-<L>.jsonl` | user ledger | sổ tiêm | giữ |
| repo RCA | người làm | `results/T-076/exp-app/demo.md`, ảnh | giữ |

Không ghi gì lên máy 84. Không sửa lõi RCA, luật, dữ liệu cũ.

## 4. Các bước

Mỗi bước ghi giờ UTC và kết quả vào `results/T-076/exp-app/demo.md`. Máy: **obs** (Grafana, bộ nhận, bộ điều phối, điều khiển tải), **app** (FlashTicket, tiêm lỗi), **tải** (k6, điều khiển từ obs).

### A. Chuẩn bị (không tải, không tiêm)

1. **Kiểm chỉ đọc (D1–D9) và ghi trạng thái trước.** `docker ps` trên obs có `flash-ticket-obs-*`, `flash-ticket-t072-bo-nhan` Up (ghi thời gian Up); ghi `HEAD` lab ở cả ba máy. Ghi trạng thái Grafana trước khi đổi: ảnh trang Contact points (`t072-bo-nhan-nhe` một integration `t072-webhook`), sha256 các file `observability/grafana/provisioning/alerting/*.yaml` và `observability/grafana/dashboards/**/*.json` ở checkout D3, ảnh trang "RCA — sự cố" (đọc `public/rca/dev`). Khác trạng thái dev/T-072 dự kiến → dừng, trình Minh.
2. **Bộ G1 hiển thị** (obs, root):
   - **Lần đầu:** `sudo python3 -B /opt/flashticket-rca/rca/online/g1_b.py --chi-khoi-tao --ra /srv/flashticket-rca/rca/results/online-demo-001 --khoi-tao chep:/srv/flashticket-rca/rca/results/dev`. Đạt khi in `"khoi_tao": "chep"`.
   - **Kiểm bản chép lần đầu:** ngay sau `chep`, danh sách đường dẫn + sha256 của `du-lieu/` và `service-graph/` ở bộ demo phải trùng nguồn `dev`; lưu danh sách này (manifest lần đầu) vào `demo.md`. Lab sau sửa T-070 REVIEW-6 R2 chép vào `.khoi-tao-tam` rồi đổi tên, nên `du-lieu/chi-muc-ban.json` chỉ xuất hiện khi cây đã đủ; bộ demo tạo bằng bản lab trước sửa đó thì vẫn phải so như trên trước khi dùng. Lệch → giữ nguyên, dừng, trình Minh.
   - **Kiểm khi dùng lại (`da_co`):** mọi file trong manifest lần đầu **trừ** hai chỉ mục (`du-lieu/chi-muc-ban.json`, `du-lieu/<bản>/chi-muc.json`) phải còn, cùng hash. Hai chỉ mục được G1 nối thêm ca mới (`g1_b.py:177–183`), nên không so byte mà **so hai chiều** với tập kỳ vọng (T-070 REVIEW-7 R2):
     - Tập kỳ vọng = các mục của hai chỉ mục lần đầu (lấy từ bản đã lưu ở manifest lần đầu, hoặc từ chỉ mục nguồn `dev` nếu hash còn khớp manifest) ∪ các mã ca **đã công bố vào G1** ở các lần phát trước (ghi trong `demo.md` của từng lần; lần phát không sinh ca G1 không thêm mã nào).
     - Đối chiếu cho cả `ban[<bản>].cac_ca` của `chi-muc-ban.json` và `su_co[].ma` của `<bản>/chi-muc.json`: không **thiếu** mục kỳ vọng, không **thừa** mục ngoài tập, không **trùng**; nội dung các mục lần đầu không đổi.
     - Lệch bất kỳ → giữ nguyên, dừng, trình Minh. Có `.khoi-tao-tam` trong bộ demo → lần khởi tạo trước bị ngắt (lab sau sửa REVIEW-7 R3 cũng dừng ở trường hợp này); dừng, trình Minh.
   - Ghi tập ID ca của bộ demo trước lượt (đọc `du-lieu/chi-muc-ban.json` và `<bản>/chi-muc.json`).
3. **Bộ nhận T-073** (obs, ubuntu):
   - `install -d -m 0700 /srv/flashticket-rca/runs/online-demo-<L>/spool`
   - tạo `/srv/flashticket-rca/runs/online-demo-<L>/receiver.env` = chép `/srv/flashticket-rca/alerts/receiver.env`, chỉ đổi `T073_SPOOL_DIR` sang spool mới (không sửa file dùng chung; `T072_RA_DIR` giữ nguyên để không tạo lại `t072-bo-nhan`)
   - `cd /opt/flashticket-rca/observability/alert-receiver && docker compose -p t073-webhook --env-file /srv/flashticket-rca/runs/online-demo-<L>/receiver.env -f compose.yaml up -d t073-webhook` (tạo lại container nếu đã có, để gắn spool mới)
   - đạt khi `t073-webhook` healthy, mount spool là đúng thư mục `online-demo-<L>` (`docker inspect`), và `t072-bo-nhan` giữ nguyên thời gian Up.
4. **Đổi checkout sang DEMO** (obs): cây sạch, không job (D6) → `git -C /opt/flashticket-rca checkout <DEMO>`; ghi SHA trước/sau. Restart Grafana: `docker restart flash-ticket-obs-grafana` (như E5), chờ `/api/health` ok, ghi `version`/`commit`; log không có `level=error` của `provisioning.alerting`/`provisioning.dashboard` (dòng `provisioning.plugins … no such file` đã có từ trước, ghi lại, không tính).
5. **Kiểm đường Grafana → spool:** trang Contact points: `t072-bo-nhan-nhe` có **hai** integration; 11 luật giữ uid/biểu thức/ngưỡng (`rules.yaml`). Bấm Test của integration `t076-webhook-demo` → spool mới có đúng một dòng mới loại Test, giờ nhận sau lúc bấm. Bấm Test của `t072-webhook` → `webhook.jsonl` của `t072-bo-nhan` có đúng một dòng Test mới, spool mới không có thêm dòng. Đối chiếu dòng mới theo loại và giờ, không theo hash toàn file (tin thật có thể đến cùng lúc). Không đạt → hoàn tác §C, không đi tiếp.
6. **Kiểm dashboard đọc đúng bộ:** trang "RCA — sự cố" liệt kê đủ các ID ca đã ghi ở A2 (có thể có thêm ca của lượt trước, không yêu cầu số ca bằng `dev`); mở một ca cũ, có đồ thị con và danh sách hạng; URL panel chứa `public/rca/online-demo-001`. Ảnh chụp.
7. **Phát bộ điều phối** (obs): `RCA_ONLINE_OUT=/srv/flashticket-rca/runs/online-demo-<L> setsid -f nohup python3 -B /opt/flashticket-rca/rca/online/orchestrator.py chay --ra /srv/flashticket-rca/rca/results/online-demo-001 > /srv/flashticket-rca/runs/online-demo-<L>/orchestrator.out 2>&1 < /dev/null`. Đạt khi `nhat-ky.jsonl` có sự cố mới lớp `quan-sat` từ dòng Test của A5 (không chạy RCA) và `spool-da-doc.json` có offset bằng kích thước file spool.

### B. Chạy

8. **Tải** (obs): `python3 -B /opt/flashticket-rca/load/controller/tai_linux.py start --tag demo-<L> --seconds 2100`. Lưu nguyên đầu ra `start` (gồm `preflight`: mock, tunnel, pool token). Gọi `get --tag demo-<L>` tối đa 3 lần cách 5 s: đạt khi `ok=true` và `result.state.Running=true` (như E5 `e5_luot.sh` bước 1); ghi `StartedAt`. Không đạt → không tiêm, ghi "lỗi điều kiện chạy: tải".
9. **Chờ nền ≥ 600 s rồi kiểm điều kiện tiêm.** Tất cả phải đạt cùng lúc; ghi đầu ra mọi lệnh:
   1. **Tải còn chạy:** `get --tag demo-<L>`: `Running=true`. Lưu `ExitCode`, `OOMKilled` nếu có.
   2. **Tín hiệu tải trước tiêm, như E5** (`e5_luot.sh` bước 2, Prometheus obs): `sum by (http_route) (increase(http_server_request_duration_seconds_count{service_name="api-gateway",http_route="payment"}[10m]))` > 0; và `time() - max by (http_url) (timestamp(httpcheck_status{http_url=~".*:<cổng payment>/.*",http_status_code!=""}))` < 60 (cổng theo D7). Ví dụ một lượt hợp lệ ở E5: `results/T-073/e5/luot/k6-sau-tai.txt` 139,322 request và tuổi mẫu 7,292 s.
   3. **Bộ điều phối đã đọc hết spool:** với mỗi file `spool/canh-bao-*.jsonl`, offset trong `spool-da-doc.json` bằng số byte tới hết dòng hoàn chỉnh cuối (`incidents.doc_spool` bỏ dòng chưa xong); không có ca `dang_chay`. Chưa đạt → chờ (bộ điều phối xử lý ca đồng bộ, `orchestrator.py:216–228`).
   4. **Không ca hệ thống nào có thể nhập ca tiêm.** Bộ gom nhập cảnh báo mới vào sự cố cùng lớp ở mọi trạng thái nếu t̂ mới ≤ `t_het` lớn nhất + 300 s; cảnh báo chưa hết coi như vô hạn (`incidents.py:172–174, 193–194`; WHY-109; `t_het` lấy từ `endsAt`, `incidents.py::_ket_thuc`). Kiểm (obs): `python3 -c 'import json,glob,time; c=[json.load(open(p)) for p in glob.glob("/srv/flashticket-rca/runs/online-demo-<L>/su-co/*.json")]; h=[s for s in c if s["lop"]=="he-thong"]; mo=[s["ma"] for s in h if any(a.get("t_het") is None for a in s["canh_bao"])]; t=max([a["t_het"] for s in h for a in s["canh_bao"] if a.get("t_het")] or [0]); print(json.dumps({"ca_he_thong": [s["ma"] for s in h], "dang_mo": mo, "tiem_duoc_tu_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t + 301)) if t else None, "bay_gio_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}))'`. Đạt khi `dang_mo` rỗng **và** giờ hiện tại sau `tiem_duoc_tu_utc` (không có ca `he-thong` thì không có ràng buộc này). In thêm số file sự cố để phân biệt "không có ca" với glob sai thư mục (phải ≥ 1, vì A7 đã tạo ca `quan-sat`).
   5. **Luật và lớp quan sát:** luật p95/5xx/liveness đang bình thường; cảnh báo lớp quan sát (`t072-mat-do`, `t072-mat-gw`) đã hết.
   6. **Không can thiệp tồn dư:** đọc `/srv/flashticket-rca/faults/inject-state/` trên app (không có hạn pause còn hiệu lực) và `docker inspect` payment `State.Paused=false`. Không gọi `inject.py verify` ở đây: `verify` có thể tự gỡ can thiệp đã quá hạn.
   - Ca nền (nếu có) cũng chạy RCA và hiện trên dashboard: ghi mã, t̂, kết quả vào `demo.md`, tách khỏi ca tiêm.
   - Chưa đạt → chờ trong thời lượng tải còn lại, tối đa tới giây 900 kể từ `StartedAt`. Quá mốc đó → dừng tải (`tai_linux.py stop --tag demo-<L>`), ghi đúng lý do: **"nền chưa sạch"** (mục 4, 5), **"lỗi điều kiện chạy"** (mục 1, 2, 3, 6: mất tải, mất dữ liệu, bộ đọc ngừng). Không tiêm, không ghi "bỏ sót".
   - Ví dụ Q4 (vì sao cần mục 4): bốn luật p95 cháy trong nền; bản tin resolved cuối được **nhận** lúc 03:29:28Z (`results/T-070/don/q4/canh-bao-nhan.out` dòng 14), tức giây ~483 sau `StartedAt`. File đó không lưu `endsAt`, nên không biết đúng biên ghép; biên của lượt mới tính từ `t_het` trong file sự cố như mục 4.
10. **Tiêm, sổ ghi trên obs theo cách E5** (`results/T-073/e5/e5_luot.sh`). Giờ lấy từ đồng hồ obs, không gõ tay:
    - `mark` (obs, trước lệnh tiêm): `printf '{"utc": "%s", "event": "mark", "cell": "PAUSE-PAYMENT", "tag_tai": "demo-<L>"}' "$(date -u +%FT%T.%6NZ)" | sudo -n -u ledger python3 -B /opt/flashticket-rca/rca/lib/ledger_append.py /srv/flashticket-rca/ledger/demo-<L>.jsonl`. `ledger_append.py` thêm số thứ tự và hash dòng trước; không tự gán giờ, không chứng minh lệnh tiêm thành công.
    - tiêm (app, ngay sau `mark`): `python3 -B /opt/flashticket-rca/faults/injectors/docker/inject.py start PAUSE-PAYMENT --seconds 600` — lưu nguyên đầu ra (dòng JSON `op=start` có trường `t`, ghi sau khi đã pause và lập hẹn giờ) và mã thoát.
    - ghi vào sổ (obs): mã thoát 0 → `{"event": "fault-start", "cell": "PAUSE-PAYMENT", "inj": <đầu ra>}`; khác 0 → `fault-start-failed` kèm `rc` và `inj-out` (đầu ra cuối). Đầu ra tiêm chỉ vào sổ, không vào `demo.md`.
    - Tiêm lỗi, đã pause một phần, hoặc ghi sổ hỏng → giữ bằng chứng; `inject.py stop PAUSE-PAYMENT`, rồi `verify`; ghi **"lỗi thao tác, chưa chấm được"**. Không chấm "bỏ sót", không tiêm lại trong lần phát này.
    - Bộ hẹn giờ của `inject.py` tự `unpause` sau `600 + 5` s. Thời lượng pause thực đọc từ log hẹn giờ (`inject-state/PAUSE-PAYMENT.het-han.log`) và `docker inspect`; "sạch sau `verify`" không đo được thời lượng.
11. **Theo dõi** (chỉ đọc): spool có cảnh báo `he-thong` (ghi `startsAt` = t̂ và `nhan_webhook_utc`); `nhat-ky.jsonl` qua các bước stage → P7 → bổ sung → V082 → kiểm đầu vào → G1.
12. **Đo đích cuối:** làm mới trang "RCA — sự cố" (trang đặt `refresh: ""`). Ghi **hai** giờ UTC: (a) lần đầu thấy mã ca trong danh sách; (b) lần đầu **mở được đúng ca** có đồ thị con và danh sách hạng. Đối chiếu mã sự cố → `ma_ca_m1` → `che_do_b.su_co` của ca mở được. Lưu ảnh danh sách, ảnh panel của ca, phản hồi API của panel danh sách. Kiểm tập ID ca cũ (A2) vẫn còn và mã mới là của lần phát này.
13. **Chấm theo C6** (sau lượt; sổ tiêm chỉ đọc lúc này). **Mốc tiêm** = trường `t` trong `inj` của bản ghi `fault-start` (mã thoát 0) đúng tag `demo-<L>` và ô `PAUSE-PAYMENT`, UTC, giữ phần lẻ khi so biên. `mark`, giờ nhận webhook và giờ gỡ/`verify` chỉ dùng giải thích độ trễ. Ví dụ E5: `mark` 02:17:31,841Z, `inj.t` 02:17:34,233Z (`results/T-073/dap-cx21/dinh-chinh-e5-1.md` §1); một cảnh báo giữa hai mốc sẽ đổi kết luận nếu lấy nhầm.
    - **Đạt:** có sự cố `he-thong` với t̂ ∈ [mốc tiêm, mốc tiêm + 600 s); `che_do_b.kiem_t.t_loi_bang_t_hat = true`; V082 `trung_sha = true`; giờ (b) của B12 ≤ t̂ + 25 phút.
    - **Bỏ sót:** điều kiện B9 đạt, tiêm thành công, không có sự cố `he-thong` trong cửa sổ — kết quả, không lặp.
    - **Quá N:** có sự cố nhưng giờ (b) > t̂ + 25 phút hoặc không mở được ca. Hàng đợi chưa xử lý khi hết N: giữ trạng thái "quá N", ghi giờ xuất hiện muộn nếu có.
    - **Lỗi xử lý:** bộ điều phối ghi lỗi một bước; phân biệt lỗi P7 đã nhận diện với lỗi khác theo `khai-truoc-e5.json#/tieu_chi/ket_qua_chuc_nang/loi_xu_ly`.
    - **Chưa chấm được:** lỗi thao tác (B10) hoặc lỗi điều kiện chạy (B8, B9).
    - Thiếu phủ đầu vào V082 báo riêng (WHY-111), không tính hỏng tuyến khi chức năng đạt. Cảnh báo lớp quan sát ghi riêng. Đây không phải phép kiểm chất lượng xếp hạng.
14. **Nhận đầu ra tải** (obs): `tai_linux.py get --tag demo-<L>` tới khi `Running=false` (ghi `ExitCode`, `FinishedAt`), rồi `receive --tag demo-<L>`.

### C. Hoàn tác (đảo thứ tự; giữ mọi dữ liệu)

1. Dừng bộ điều phối (như E5 `results/T-073/e5/hoan-tac/s5-1-stop.txt`). Đang chấm "quá N" mà ca còn `cho` → giữ bằng chứng (file sự cố, ảnh) trước. `touch /srv/flashticket-rca/runs/online-demo-<L>/STOP` chỉ chặn bước mới, **không** làm tiến trình thoát (`orchestrator.py:216–228` là vòng `while True`). Đọc `su-co/*.json`: không còn ca `dang_chay` (chờ ghi `xong` hoặc `loi`). Sau đó SIGTERM đúng tiến trình: `pkill -TERM -f 'orchestrator.py chay --ra /srv/flashticket-rca/rca/results/online-demo-001'`; `pgrep -af orchestrator.py` rỗng; ghi PID và giờ. `STOP` nằm trong OUT của lần phát này, không ảnh hưởng lần phát sau.
2. Cây sạch, không job → `git -C /opt/flashticket-rca checkout <HOAN-TAC>`; `docker restart flash-ticket-obs-grafana`; health; log không lỗi provisioning.
3. **Kiểm trạng thái sau, so với A1:** trang Contact points `t072-bo-nhan-nhe` còn **một** integration `t072-webhook`; bấm Test của `t072-webhook` → `webhook.jsonl` có dòng Test mới; 11 luật như trước; trang "RCA — sự cố" đọc lại `public/rca/dev` (mở một ca cũ). Ảnh chụp. Đây là "trở về cấu hình dev"; lab vẫn ở HOAN-TAC (bước 6).
4. Dừng bộ nhận T-073: `docker compose -p t073-webhook --env-file /srv/flashticket-rca/runs/online-demo-<L>/receiver.env -f /opt/flashticket-rca/observability/alert-receiver/compose.yaml stop t073-webhook` (dùng `stop`, không `down`: cùng project có `t072-bo-nhan` chạy liên tục).
5. Giữ trên host mọi thứ ở §3.2. `inject.py verify` báo sạch.
6. Lab ở lại `HOAN-TAC` (file `deleteContactPoints` có hiệu lực, chạy lại không đổi gì). Chỉ về lại D3 (hoặc gốc mới) sau khi chỉ thị gỡ đã có hiệu lực và kiểm ở bước 3; kiểm cây sạch, không job.
7. Đơn mua phát sinh trong DB thử do lượt k6 không hoàn tác được bằng đổi image/commit (giới hạn đã nêu ở SPEC bước 8).

Nếu Minh muốn **giữ** cấu hình demo để trình bày lại: bỏ C2–C4; dừng bộ điều phối (C1) khi không dùng. Bộ nhận vẫn ghi vào spool của lần phát này khi bộ điều phối dừng; lần phát sau tạo OUT mới và gắn lại bộ nhận (A3).

## 5. Gặp lỗi giữa chừng

| Lúc | Hiện tượng | Xử lý | Chạy lại gì, mất bao lâu |
|---|---|---|---|
| A1–A7 (chưa tải) | bước kiểm không đạt (trạng thái trước, bản chép, hai integration, Test, dashboard, bộ điều phối) | đảo các bước đã làm theo §C | sửa nguyên nhân, làm lại phần A chưa đạt; ~15 phút |
| B8–B9 (tải, chưa tiêm) | tải không Running; tín hiệu tải không đạt; bộ đọc tồn đọng; nền chưa sạch tới giây 900 | dừng tải, không tiêm; giữ dữ liệu; ghi "lỗi điều kiện chạy" hoặc "nền chưa sạch" | lần phát mới `<L>` mới, cùng bộ hiển thị, cùng cặp commit; ~50 phút. Chỉ lặp khi nguyên nhân là hạ tầng có bằng chứng (E5 `#/ca_nghiem_thu/so_lan`, tối đa 3) |
| B10 | lệnh tiêm lỗi, pause một phần, ghi sổ hỏng | `inject.py stop`, `verify`; giữ bằng chứng; "lỗi thao tác, chưa chấm được" | như dòng trên |
| B11–B13 (đã tiêm) | bộ điều phối lỗi một bước | ghi `loai_loi`; chấm "lỗi xử lý"; không tiêm lại trong cùng lần phát | lần phát mới chỉ khi lỗi hạ tầng có bằng chứng |
| B11–B13 | điều kiện B9 đạt, tiêm thành công, không có cảnh báo trong cửa sổ | chấm "bỏ sót" — là kết quả | không lặp; trình Minh (C6: luật im vì thiếu mẫu → kiểm đường thu; nền khỏe vẫn cháy → T-072 xét ngưỡng) |
| B12 (cuối lượt) | ca có trong file sự cố nhưng trang chậm hoặc không mở | dùng lại file ca, spool, ảnh để phân biệt chậm giao diện với lỗi xử lý; không chạy lại | — |
| bất kỳ | payment không tự `unpause` | `inject.py stop PAUSE-PAYMENT`, rồi `verify` | — |
| C | hoàn tác không về trạng thái A1 | dừng, giữ bằng chứng, trình Minh | ~10 phút dự trù |
| bất kỳ | demo trước người xem mà tuyến sống hỏng | **xem lại bằng chứng đã lưu**, gọi đúng tên: hai ảnh `results/T-073/e5/s49-anh-ca-moi-trong-danh-sach.jpg`, `results/T-073/e5/s49-anh-mo-ca-7577dd5b.jpg` và file ca E5 đã kiểm hash (`results/T-073/e5/ca-7577dd5b.SHA256SUMS`). Không hứa mở dashboard dev là thấy E5: bộ E5 đầy đủ nằm ở archive của obs, ngoài mount Grafana hiện tại (`docs/ARCHIVE-INDEX.md`) | không phải phát lại tương tác, không phải demo mới |

## 6. Ghi kết quả

`results/T-076/exp-app/demo.md`: mã lần phát `<L>`, SHA lab ở các bước, tham số §2, trạng thái trước (A1) và sau (C3), giờ từng bước, kết quả kiểm B9 (sáu mục), mốc E5 (mốc tiêm `inj.t` → t̂ và `nhan_webhook_utc` → hai giờ của B12), mã ca, kết quả chấm C6, ảnh, lệnh hoàn tác đã chạy, thời gian thực so với khung §2.

## 7. Chưa kiểm

- File provisioning trên commit lab mới (đã chạy ở E5 trên `ecdeed2`, cùng digest image Grafana; bố cục lab đã đổi sau đợt dọn 11/2026).
- Đường dẫn bộ nhận mới `/canh-bao`: mới kiểm biên dịch và cú pháp YAML trên laptop; chạy thật ở A3 (healthcheck `…/canh-bao/song`) và A5 (bấm Test).
- Tên container payment, cổng đầu dò payment và máy đặt sổ tiêm trên bản demo mới (D7, D8 — bước 8).
- `build_dashboards.py` đọc `git show ab1c52c:…` nên cần commit đó trong lịch sử của checkout dùng để sinh (laptop có).
- Thời gian thật từ t̂ tới lúc trang ca hiện trên bản mới (E5 đo trên bản cũ; N = 25 phút là mục tiêu tạm); thời gian chờ ca đang xử lý trước khi tiêm.
- Phép so bản chép G1 (A2) chưa có script; viết khi Minh duyệt runbook, chạy chỉ đọc.
