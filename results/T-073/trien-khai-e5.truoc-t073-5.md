# T-073 — Gói triển khai E5 (S4): đích cảnh báo, nguồn dashboard, thứ tự, hoàn tác

Bản 1, 22/11/2026, phiên `rca-w5`. **Chưa commit, chưa triển khai.** Điều phối cho Codex soát rồi trình Minh duyệt commit.

## 1. Diff

Worktree `D:/Project/rca-lab-wt/T-073-e5`, nhánh `t073-e5`, gốc **`ecdeed2`** (commit G đang chạy trên exp-obs, nhánh tích hợp `t070-e3`). Toàn văn: `results/T-073/e5.diff`.

| File | Thay đổi | Mục |
|---|---|---|
| `observability/grafana/provisioning/alerting/t073-e5.yaml` | **mới**: thêm integration webhook `t073-webhook-e5` → `http://t073-webhook:8080/t073/canh-bao` vào contact point **`t072-bo-nhan-nhe`** | (a) |
| `observability/grafana/provisioning/alerting/t073-e5-go.yaml.mau` | **mới**: `deleteContactPoints` uid `t073-webhook-e5` (hoàn tác; Grafana không nạp đuôi `.mau`) | (a) |
| `observability/grafana/build_dashboards.py` | biến `RCA_G1_BO` (mặc định `t065-l11-001`); khác mặc định thì đổi mọi URL `public/rca/t065-l11-001` và tên bộ trong ghi chú; dừng nếu còn sót | (b) |
| `observability/grafana/dashboards/{00-start-here,20-incidents,30-replay}/*.json` | sinh lại với `RCA_G1_BO=t073-e5-001`: 43 dòng, chỉ khác tên bộ (1 + 28 + 13 URL, 1 ghi chú) | (b) |
| `campaigns/online/g1_b.py` | cờ `--chi-khoi-tao` (dựng bộ `--ra` theo `--khoi-tao`, không ghi ca) | (b) |

Không đổi: `t072-luat.yaml` (11 luật, file do script T-072 sinh), `compose.yaml`, `compose.t073-webhook.yaml`, lõi M1, các file khác của `campaigns/online/`.

### Ba commit cần Minh duyệt cùng lúc (CX-17)

| Commit | Gốc | Nội dung | Ở đâu | Dùng ở |
|---|---|---|---|---|
| **E5** | `ecdeed2` | 7 file như bảng trên | worktree `D:/Project/rca-lab-wt/T-073-e5` (chưa commit), toàn văn `results/T-073/e5.diff` | S4-4 trở đi |
| **P** (bật lưu trữ, tạm) | E5 | `provisioning/dashboards/providers.yaml`: thêm provider `luu-tru-tam` (đúng mẫu `observability/grafana/README.md`) | `results/T-073/commit-e5/P-bat-luu-tru.patch` | chỉ trong S4-7b |
| **H** (hoàn tác) | E5 | 3 dashboard về bản `ecdeed2` (nguồn `t065-l11-001`, trùng byte), xóa `t073-e5.yaml`, `t073-e5-go.yaml.mau` → `t073-e5-go.yaml` (`deleteContactPoints` uid `t073-webhook-e5`) | `results/T-073/commit-e5/H-hoan-tac.patch` | §5 |

"Trả về" sau P là đổi checkout lại **commit E5** (không cần commit mới). Kiểm trên laptop: `git apply --check` của P và H trên worktree E5 đều đạt; áp H lên bản sao tạm → 3 dashboard trùng byte `ecdeed2`, thư mục alerting còn `t073-e5-go.yaml`, không còn `t073-e5.yaml`. Tạo commit: `git apply <patch>` trên commit gốc tương ứng, rồi commit (khi Minh duyệt).

## 2. (a) Đích cảnh báo: thêm integration vào contact point sẵn có

11 luật thật (`t072-luat.yaml`) đều định tuyến từng luật `notification_settings.receiver: t072-bo-nhan-nhe` (kiểm: 11/11). Contact point đó có một integration `t072-webhook` → `http://t072-bo-nhan:9172/t072`.

| Cách | Đổi luật? | Bằng chứng T-072 | Chọn |
|---|---|---|---|
| **Thêm integration thứ hai vào `t072-bo-nhan-nhe` bằng file riêng** | Không: truy vấn, ngưỡng, `for`, nhãn, `notification_settings` giữ nguyên | Giữ (Grafana gửi tới mọi integration của contact point) | **Có** |
| Contact point mới + đổi `receiver` của 11 luật | Có: đổi định nghĩa luật (phiên bản luật mới), dù không đổi biểu thức | Phải liệt kê lại cả hai đích | Không |
| Sửa `t072-luat.yaml` bằng tay | Không | Giữ | Không: file "sinh bởi `sinh_luat_grafana.py`, không sửa tay" |

**Chưa kiểm:** Grafana 13.3 nạp hai file provisioning cùng `name` contact point thành **một** contact point có hai integration (provisioning theo `uid` từng receiver, nhóm theo `name`). Kiểm ở S4-6. Không đạt (chỉ thấy một integration, hoặc log Grafana báo lỗi provisioning) → hoàn tác thực hiện toàn bộ §5 (bỏ bước 1 dừng bộ điều phối nếu chưa khởi chạy), và phương án dự phòng: T-072 sinh lại `t072-luat.yaml` bằng `sinh_luat_grafana.py` với hai receiver trong cùng contact point (việc của T-072, cần điều phối/Minh).

Hệ quả: bộ nhận T-073 nhận cả hai luật lớp `quan-sat` (`t072-mat-do`, `t072-mat-gw`) và tin Test của Grafana; bộ gom xếp lớp quan sát, không chạy RCA (`incidents.py`, T072-i1-1 (a)).

## 3. (b) Nguồn dashboard: bộ `rca-results/t073-e5-001`

- Dashboard đọc qua mount chỉ đọc `rca-results` → `/usr/share/grafana/public/rca`. Commit này đổi ba dashboard sang `public/rca/t073-e5-001`.
- Bộ `t073-e5-001` dựng **trước** khi đổi checkout bằng bản chép `du-lieu/` và `service-graph/` của `t065-l11-001` (giống `g1_b.py --khoi-tao chep:`), nên ca cũ vẫn xem và phát lại được; ca E5 do `g1_b.py` thêm vào chỉ mục (chỉ thêm, không sửa mục cũ). `t065-l11-001` không bị ghi.
- Dashboard nạp bằng provider file (`updateIntervalSeconds: 30`): đổi checkout là đổi hiển thị trong ≤ 30 s, không cần restart cho phần này.
- Kiểm trên laptop: sinh lại mặc định → 4 dashboard trùng byte bản `ecdeed2`; sinh với `t073-e5-001` → 0 chuỗi `t065-l11-001` còn lại, 43 dòng đổi chỉ khác tên bộ; tên bộ sai dạng bị từ chối. `--chi-khoi-tao` (hàm `khoi_tao`, chép) thử trên thư mục giả: chép `du-lieu/`, `service-graph/`, bỏ thư mục khác; chạy lần hai → `da_co`.

## 4. Thứ tự ở S4 (I7: chỉ khi không có job; mỗi bước ghi giờ vào `results/T-073/e5/`)

Điều kiện mở: E4 xong; điều phối mở S4 cho T-073; **trước S4-4**, Minh đã duyệt **cả ba** commit E5, P, H với SHA cụ thể; cả ba đã push và lấy được trên exp-obs (`git -C /opt/rca-lab fetch` rồi `git cat-file -e <SHA>^{commit}` cho từng SHA); cha của P và của H đúng là SHA E5 (`git rev-parse <P>^ <H>^`); `khai-truoc-e5.json` (`5883c4e2…`) và `khoa-boc-e5.json` (`27b0a61d…`) đã khóa; ô đã bốc là **`PAUSE-PAYMENT`**, hạt `32323232` (LOG T-073, 22/11/2026 11:19:49Z). Kiểm các điều kiện áp dụng cho ô theo `bang-o-e5.md` ở các bước dưới đây.

**Phạm vi "log không lỗi" ở mọi bước dưới:** chỉ xét dòng `level=error` của logger `provisioning.alerting` và `provisioning.dashboard`. Bản nền `ecdeed2` đã có `logger=provisioning.plugins … level=error … open /etc/grafana/provisioning/plugins: no such file or directory` (`results/T-072/e3/b4-restart.txt` dòng 64, `b10-restart-g.txt` dòng 28): ghi lại, không tính là lỗi của E5.

**Kiểm I7 ngay trước mỗi lần đổi checkout**, kể cả ở §5. Tại `/opt/rca-lab`, đối chiếu `git rev-parse HEAD` với commit nguồn dự kiến của lần đổi đó, kiểm `git status --porcelain` rỗng và dùng `pgrep -af 'chuoi_tai|runner4|tai_linux|stage_b|orchestrator|inj3|do-0|xuat_chuoi'` để kiểm job. Chỉ đổi khi HEAD khớp, cây sạch và đã xác nhận không có job. Sau mỗi lần đổi, kiểm HEAD khớp commit đích và báo SHA trước/sau cho điều phối; điều phối ghi `LICH-MAY.md` (I15), T-073 không ghi file này.

1. **S4-1** Kiểm chỉ đọc. Dùng mẫu job I7 ở trên, kiểm không có job, không có STOP, `/opt/rca-lab` ở `ecdeed2` và cây sạch, các container `flash-ticket-obs-*`, `flash-ticket-t072-bo-nhan` đang Up. Với `PAUSE-PAYMENT`, kiểm phần chỉ đọc K1, K5, K6, K7, K9 theo `bang-o-e5.md`.

   **S4-1a — thao tác có thay đổi trạng thái.** Chạy `inj3.py ensure` khi điều kiện của ô yêu cầu (K2), rồi `inj3.py verify` cho K10. `ensure` có thể tạo proxy. `verify` có thể bỏ pause và xóa file hạn. Với `PAUSE-PAYMENT`, chỉ K10 áp dụng trong bước này. Ghi kết quả trước khi tiếp tục.
2. **S4-2** Dựng bộ: `sudo install -d -o root -g root -m 0755 /srv/rca-lab/rca-results/t073-e5-001 && sudo cp -a /srv/rca-lab/rca-results/t065-l11-001/du-lieu /srv/rca-lab/rca-results/t065-l11-001/service-graph /srv/rca-lab/rca-results/t073-e5-001/`; ghi số file và sha256 danh sách chỉ mục hai bên.
3. **S4-3** Bộ nhận T-073: `install -d -m 0700 /srv/rca-lab/runs/t073-e5-01/spool`; file env `/srv/rca-lab/runs/t073-e5-01/webhook.env` = cùng `T073_WEBHOOK_IMAGE` và `T072_RA_DIR` như `/srv/rca-lab/runs/t072-e3-01-cfg/webhook.env` (để không tạo lại `t072-bo-nhan`), thêm `T073_SPOOL_DIR=/srv/rca-lab/runs/t073-e5-01/spool`; `cd /opt/rca-lab/observability && docker compose -p t073-webhook --env-file /srv/rca-lab/runs/t073-e5-01/webhook.env -f compose.t073-webhook.yaml up -d t073-webhook`; kiểm `healthy`, `t072-bo-nhan` giữ nguyên thời gian Up.
4. **S4-4** Kiểm I7 ngay trước khi đổi checkout `/opt/rca-lab` từ `ecdeed2` sang commit E5 đã duyệt. Kiểm và ghi commit sau khi đổi theo I7.
5. **S4-5** Restart Grafana như T-072 E3 bước 4 (`results/T-072/e3.md`, `e3/b4-restart.txt`); chờ `/api/health` ok và ghi `version`, `commit` (bản ghi E3 sau commit G: `results/T-072/e3/b10-restart-g.txt`, `version 13.3.0`, `commit 6f8ce3c693…`; phải trùng); lưu log Grafana sau restart.
6. **S4-6** Kiểm (a): trang Alerting → Contact points: `t072-bo-nhan-nhe` có **hai** integration (`t072-webhook`, `t073-webhook-e5`); 11 luật giữ uid, biểu thức, ngưỡng (đối chiếu `t072-luat.yaml`); log không có dòng `level=error` của logger `provisioning.alerting` hay `provisioning.dashboard`. Trước khi bấm Test, lưu kết quả `sha256sum /srv/rca-lab/runs/t072-e3-01/webhook.jsonl` và `tail -n 1 /srv/rca-lab/runs/t072-e3-01/webhook.jsonl` cùng giờ UTC vào hồ sơ E5 để xác định mốc cuối của E4. **Test theo từng integration** (đã kiểm mã nguồn Grafana tag `v13.3.0`, chỉ đọc: mỗi integration trong form contact point có nút Test riêng, gửi đúng một integration — `ChannelSubForm.tsx`, `ReceiverForm.tsx` gọi `onTestChannel(getValues().items[index])`, thân yêu cầu `{ integration: {uid, type, settings, …}, alert }` trong `hooks/useTestContactPoint.ts`; contact point provisioned vẫn cho Test nếu tài khoản có quyền test, `useContactPointAbility.ts`; bản đang chạy báo `version 13.3.0`, `commit 6f8ce3c693…` theo `results/T-072/e3/b10-restart-g.txt`; mã UI đọc ở tag `v13.3.0` trên GitHub (lượt 13, qua một subagent — Minh không cho dùng subagent, ghi ở LOG; CX-17 không đọc lại được đúng commit). Vì chưa xác nhận độc lập trên đúng commit, bước xác nhận hai đích dưới đây là **bắt buộc** trước khi đi tiếp). Thứ tự:
   - (i) Mở contact point `t072-bo-nhan-nhe`, bấm Test của integration **`t073-webhook-e5`** (tin mặc định `alertname=TestAlert`). Ghi giờ UTC bấm. Kiểm: spool `/srv/rca-lab/runs/t073-e5-01/spool/canh-bao-*.jsonl` có **đúng một** dòng mới, `than.alerts[0].labels.alertname = TestAlert`, `nhan_webhook_utc` sau giờ bấm; `webhook.jsonl` của T-072 **không** đổi (sha256 như mốc vừa lưu). Tin này là tin dùng cho K8 ở S4-9.
   - (ii) Bấm Test của integration **`t072-webhook`**. Kiểm: `webhook.jsonl` của T-072 có đúng một dòng mới với `TestAlert`; spool T-073 không thêm dòng.
   - (iii) Nếu bản Grafana đang chạy lại chỉ có một nút Test cho cả contact point (khác mã `v13.3.0`): bấm một lần, kiểm mỗi đích có đúng một dòng `TestAlert` mới; ghi rõ trường hợp nào đã gặp.
   - Đạt khi mỗi đích nhận đúng tin Test của mình (hoặc cả hai nhận tin chung ở (iii)) và giao diện liệt kê hai integration. Không thấy nút Test (tài khoản thiếu quyền test) hoặc một đích không nhận → thực hiện toàn bộ §5 (bỏ bước 1 dừng bộ điều phối nếu chưa khởi chạy) và phương án dự phòng §2; không đi tiếp.
7. **S4-7** Kiểm (b): dashboard "RCA — sự cố" liệt kê đủ ca cũ từ `t073-e5-001` (số ca = chỉ mục `t065-l11-001`); mở một ca cũ và trang phát lại của nó; ảnh chụp.

   **S4-7b Dashboard lưu trữ, mở từng trang khi nguồn E5 đang hoạt động** (sửa theo CX-17 điểm 2; bản 13 thay bằng diff + hash là thu hẹp yêu cầu W5 "kiểm dashboard hiện hành, lưu trữ và phát lại khi đổi nguồn JSON", SPEC dòng 20, 53):
   1. Ngay trước: `cd /srv/rca-lab/rca-results && find t065-l3-001 t065-l4-001 t065-l11-001 mau phat-lai -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum` → ghi (lặp lại sau E5; hai lần phải trùng — bằng chứng phụ, không thay việc mở trang).
   2. Kiểm I7 → đổi checkout `/opt/rca-lab` commit E5 → **commit P**; báo SHA trước/sau cho điều phối (điều phối ghi `LICH-MAY.md`, I15; T-073 không ghi file này). Restart Grafana; health như S4-5; log không có dòng `level=error` của logger `provisioning.dashboard`.
   3. Mở lần lượt sáu trang lưu trữ (thư mục Grafana theo `90-archive/<ngày-…>`): `2026-11-12-g2-v6/rca-g2-chinh`, `rca-g2-phat-lai` (chọn `thu_muc` = bộ trong `rca-results/{mau, phat-lai}`, một ca có sẵn); `2026-11-13-l3-p7/t065-rca`, `t065-phat-lai` (một ca trong chỉ mục `t065-l3-001`); `2026-11-14-l4-temporary/t065-l4-rca`, `t065-l4-phat-lai` (một ca trong chỉ mục `t065-l4-001`). Mỗi trang ghi: nạp được (có/không), panel danh sách có ca, mở ca → panel có dữ liệu (có/không, panel nào trống), ảnh chụp, giờ UTC. Đồng thời mở trang hiện hành "RCA — sự cố" để xác nhận nó vẫn đọc `t073-e5-001` khi provider lưu trữ đang bật.
   4. Kiểm I7 → đổi checkout lại **commit E5**; báo SHA trước/sau cho điều phối ghi `LICH-MAY.md`. Restart Grafana; health; kiểm: sáu trang lưu trữ không còn trên giao diện (README: bỏ provider + restart thì gỡ; nếu vẫn còn → ghi, trình điều phối, không xóa tay), `t072-bo-nhan-nhe` vẫn hai integration, 11 luật như S4-6.
   5. Trang lưu trữ không nạp hoặc không đọc được ca: ghi đúng trang và panel; đây là kết quả kiểm W5 (không lặp, không sửa dashboard lưu trữ trong E5); trình điều phối trước S4-8.
8. **S4-8** Phát bộ điều phối: `RCA_ONLINE_OUT=/srv/rca-lab/runs/t073-e5-01 setsid -f nohup python3 -B /opt/rca-lab/campaigns/online/orchestrator.py chay --ra /srv/rca-lab/rca-results/t073-e5-001 --spool /srv/rca-lab/runs/t073-e5-01/spool > /srv/rca-lab/runs/t073-e5-01/orchestrator.out 2>&1 < /dev/null`; tin Test ở S4-6 phải được gom thành sự cố **quan sát** (không chạy RCA).
9. **S4-9** Sau S4-8 và trước khi tiêm, kiểm K8 theo `bang-o-e5.md`. Xác nhận Grafana đã nạp và đang đánh giá luật W4, contact point trỏ tới `http://t073-webhook:8080/t073/canh-bao`, bộ nhận `healthy` và nhật ký cho thấy bộ điều phối đang chạy, đã đọc tin Test từ spool. K8 chưa đạt thì dừng trước tiêm. Chạy lượt `PAUSE-PAYMENT` và ghi ba mốc giờ theo `khai-truoc-e5.json`.

   **Giới hạn đã biết khi kiểm trang ca (CX-13b, điều phối đã kiểm):** liên kết metric `live-down` trên trang ca hỏng: `campaigns/runner/xuat_bo_sung.py` trả `query = MO_TA_R9` (câu mô tả, không phải PromQL) cho kênh này, và `campaigns/g1/l8b-xuat.py` dùng nguyên `q['query']` làm biểu thức Prometheus của liên kết. Khi kiểm dashboard ở E5, ghi đây là giới hạn đã biết, **không** tính là lỗi tuyến E5; không sửa G1 trong E5 (file ghim T-067, cần Minh). Dữ liệu `live-down` vào lõi (gói bổ sung) không bị ảnh hưởng.

   Trang “RCA — sự cố” đặt `refresh: ""`. Khi theo dõi ca mới, làm mới hoặc mở lại trang dùng nguồn `t073-e5-001`. Ghi giờ UTC lần đầu thấy mã ca trong danh sách, mở ca để xác nhận xem được và lưu ảnh cùng phản hồi API của panel danh sách theo khai trước. Chu kỳ 30 giây của provider ở §3 chỉ dùng để nạp định nghĩa dashboard.

## 5. Hoàn tác bằng commit H (đảo thứ tự; giữ mọi dữ liệu)

1. **Dừng bộ điều phối:** `touch /srv/rca-lab/runs/t073-e5-01/STOP`; chờ tới khi nhật ký không còn bước đang chạy (bộ điều phối không bắt đầu bước mới khi có STOP); dừng tiến trình; kiểm `pgrep -af "campaigns/online/orchestrator.py"` rỗng.
2. **Kiểm I7** theo §4 (không job, cây sạch, HEAD hiện tại) → đổi checkout `/opt/rca-lab` sang **commit H**; báo SHA trước/sau cho điều phối (điều phối ghi `LICH-MAY.md`, I15; T-073 không ghi file này).
3. **Restart Grafana**; health như S4-5 (`version 13.3.0`, `commit 6f8ce3c693…`); log có "finished to provision alerting" và không có dòng `level=error` của logger `provisioning.alerting` hay `provisioning.dashboard`.
4. **Kiểm sau restart:** contact point `t072-bo-nhan-nhe` còn **đúng một** integration `t072-webhook`; 11 luật giữ uid/biểu thức/ngưỡng; trang "RCA — sự cố" và "phát lại" đọc lại `t065-l11-001` (mở một ca cũ); không có trang lưu trữ (H không có provider `luu-tru-tam`). Lý do H phải có `t073-e5-go.yaml`: chỉ xóa `t073-e5.yaml` thì integration đã nạp **không** bị gỡ.
5. **Bộ nhận T-073:** `docker compose -p t073-webhook --env-file /srv/rca-lab/runs/t073-e5-01/webhook.env -f /opt/rca-lab/observability/compose.t073-webhook.yaml rm -s -f t073-webhook`; spool, env và bộ `t073-e5-001` giữ trên host; `t072-bo-nhan` không đụng.
6. `/opt/rca-lab` ở lại commit H (file `t073-e5-go.yaml` có hiệu lực, chạy lại không đổi gì). Đổi sang commit khác về sau: I7 như trên.

## 6. Còn mở

- Gộp nhánh: `t073-e5` đặt trên `ecdeed2`; nếu điều phối muốn commit nằm trên `t070-e3` thì cherry-pick nguyên commit (không xung đột: chỉ thêm file và đổi các file chỉ T-073 chạm).
- (a) chưa kiểm trên Grafana thật (S4-6); mã UI nút Test chưa xác nhận độc lập trên đúng commit `6f8ce3c…` (bước hai đích ở S4-6 là bắt buộc).
- Lúc dashboard hiện ca mới: đo ở E5 (đích cuối của N).
