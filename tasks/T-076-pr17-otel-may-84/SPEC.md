# T-076 — Làm lại PR #17 trên main mới nhất; FlashTicket mới chạy cho demo trên Oracle; mở đường quan sát máy 84

- **Trạng thái:** **Minh duyệt bản 6 ngày 27/11/2026** ("Duyệt luôn bản 6"), gồm Q1–Q10 theo cột đề xuất. Sửa theo `REVIEW-4.md` (Codex, R1–R4) của bản 5. Hướng H1 + H4 Minh duyệt 27/11. Bản cũ: `SPEC.ban-1.md` … `SPEC.ban-5.md`.
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P9 (kho quan sát và tích hợp), P10 (thực nghiệm trên FlashTicket và demo) — **Cổng:** ngoài G0–G4 (tích hợp, không đánh giá phương pháp)

## Mục tiêu

**Nguồn:** DT18-NV1 (hệ thống bán vé phân tán), DT18-NV2 (thu log, trace, metric; `docs/reference/sources/DT18-de-tai-va-nhiem-vu.md` §2), MRP P9a (chuẩn B16, `service.name` thống nhất ba tín hiệu), MRP P10 (thực nghiệm và demo trên FlashTicket).

**Mong muốn của Minh:**
- 24/11: Y11 toàn quyền phần quan sát của FlashTicket, miễn không ảnh hưởng hệ thống; Y12 dùng bản mới nhất cho thống nhất.
- 26/11: không sửa tay trên máy 84; dọn chỗ lỗi thời của PR #17; **chỉ một PR** (làm lại chính PR #17).
- 27/11: chọn H1 + H4. **Demo phải chỉn chu.** **Thiết kế mở:** sau này chuyển sang quan sát máy 84 (AWS) thì chỉ **thêm**, hoặc sửa nhỏ (IP, cổng, thông tin kết nối); không xóa, không đổi cấu trúc thư mục.

**Task này gồm hai phần:**
- **Phần A — PR #17:** đưa chuẩn quan sát B16 vào main mới nhất của nhóm. Agent có sẵn trong image và **bị tắt cứng** trên K8s. Máy 84 không gửi dữ liệu quan sát đi đâu (H1).
- **Phần B — exp-app cho demo:** dựng lại bản FlashTicket thử nghiệm trên exp-app (Oracle) từ main mới nhất có PR #17, kiểm tín hiệu, diễn tập demo trọn vòng tải → sự cố → cảnh báo → RCA (H4). Chỉ phục vụ demo; **không** chọn bản cho W7 (xem C5).

**Không thuộc task (mục "Mở rộng sang máy 84"):** bật quan sát cho máy 84. Bị chặn bởi RAM của cụm và việc triển khai Collector qua CD của nhóm.

Task không đánh giá phương pháp RCA, không đổi phương pháp. Một lần demo chạy đúng chỉ chứng minh đường tích hợp; không cho kết luận về tỷ lệ báo động giả, độ nhạy hay độ đúng vùng (thuộc W7 hoặc đánh giá đã khai riêng).

## Hiện trạng đã kiểm (26–27/11/2026, chỉ đọc trừ phần ghi rõ)

| Điều | Thực tế | Nguồn |
|---|---|---|
| Main, PR | `origin/main` `f178870`; PR #17 `bb84d64` OPEN, CONFLICTING, 124 file, 13 xung đột | `git`, `gh` (LOG phiên 4) |
| Bảng file PR | Giữ 93 / sửa 17 / bỏ 14; Minh duyệt 26/11. Phần thêm khi dựng (K8s) ghi theo bản 3, bản 5 đổi (chênh ghi ở bước 3) | `results/T-076/bang-file-pr17.md` |
| Nhánh dựng lại | Local `rca/quan-sat-log-dung-lai` (worktree `D:/Project/ft-pr17-dung-lai`), 6 commit trên `f178870`, chưa push. Commit cuối `ae5a870` theo bản 3 | LOG phiên 4 |
| Kiểm cục bộ bản 3 | 8/8 `verify`, 7/7 kiểm B16 đạt; Event `-P rca-test` đạt; **Booking `-P rca-test` 67 error** (3 lớp `@WebMvcTest` thiếu bean `RcaFaults`; có từ `bb84d64`) | `results/T-076/kiem-cuc-bo/README.md` |
| Agent gửi gì (Collector thử không processor) | Lộ query (`url.query`, exemplar metric); không lộ header Authorization/Cookie, body, client secret; SQL đã sanitize; event `exception` có `exception.message` và `exception.stacktrace` (12/12 message khác rỗng nằm cả trong stacktrace, đếm của Codex REVIEW-3 R6) | như trên, §3 |
| Thứ tự biến môi trường trong pod | `envFrom`: ConfigMap rồi Secret (Secret thắng khi trùng khóa); `env:` thắng cả hai (quy tắc K8s). CD đưa vào Secret mọi khóa có tên trong file mẫu và có giá trị trong `ENV_<SVC>`; giá trị hiện có của `ENV_<SVC>` không ai đọc được | `deployment.yaml:59–63`, `deploy-k8s-service.sh:198–221` @main |
| Biến tác động khi agent tắt | `SPRING_AUTOCONFIGURE_EXCLUDE` do Spring đọc (đổi hành vi app). Các biến `OTEL_*` chỉ agent đọc: không service nào có starter OpenTelemetry/Micrometer tracing của Spring | `grep` `pom.xml` @nhánh |
| VNPay, tham số query | `vnpay/return`, `vnpay/ipn` là GET có `vnp_*` ở query; cần che `q` và 28 tên `vnp_*` | `PaymentController.java:52,59` @nhánh |
| Cụm máy 84 | K3s 3 node: `ft84` 7,6 GiB (55%; kèm Postgres, Mongo, RabbitMQ, Redis), `server-1` 1,9 GiB, `server-2` 3,7 GiB (83%, limits 115%). Booking 654/411, Payment 689/368 MiB ở hai bản cùng service; nhóm đang triển khai lúc đo | SSH chỉ đọc 27/11 (LOG phiên 4) |
| CD của nhóm | Chỉ build `maven`/`node`, triển khai tuần tự từng service. Trạng thái mỗi service ở `<app_root>/state/k8s/<svc>/`: `current`, `previous`, mỗi revision có `image` (và `secret-env.json` — không đọc). `rollback` chỉ về `previous` và digest phải khớp `image` của nó; `previous` đổi sau mỗi lần triển khai thành công; service chưa có revision trước thì CD không quay lại được (chỉ in hướng dẫn) | `_deploy-service.yml:134–136`, `deploy-k8s-service.sh:13,24,170–175,261–271,285–295` @nhánh |
| exp-app | Bản ghim `36a3725d` (T-067): Payment image `arm64-t067-36a3725d`, Keycloak ghim riêng `arm64-776d9c9e`, Collector theo lab. Dựng từ `deploy/app/<svc>.yml` của nhóm + file phủ lab. Main bỏ service ngrok trong `payment-service.yml`; file phủ lab và `hieu_luc.py` vẫn khai ngrok | REVIEW-3 R5, R7; lab `test-environment/` |
| Sự kiện tải | Hết hạn bán 02/12/2026 22:16Z | `results/T-070/don/KE-HOACH-DON.md` §2 |
| Tuyến vận hành trên lab `c1da15f` | Bộ chuỗi tải và RCA trực tuyến chưa dùng lại: chờ Codex kiểm bản sửa (T-070, chưa có `REVIEW-5.md`). Q4 của T-070 chạy thẳng `tai_linux.py start` từ obs (ghi nhật ký/trạng thái obs, làm mới token, có thể khôi phục mock/đường hầm, ghi đầu ra trên máy tải). Trên obs: bộ nhận `t072-bo-nhan` chạy, `t073-webhook` không chạy; integration T-073 đã gỡ. G1 trực tuyến ghi `rca/results/online-<lượt>`; dashboard hiện đọc `public/rca/dev`; `build_dashboards.py` sinh được bản đọc nguồn `online-*`. Runbook hoàn tác E5 (`results/T-073/trien-khai-e5.md` §5) dùng đường và checkout trước đợt dọn (`/opt/rca-lab`, `1bb40ca`, `t065-l11-001`) — không dùng lại nguyên | LOG T-070, `docker ps` obs (REVIEW-3 R3, REVIEW-4 R2) |
| Obs | CA và chứng chỉ máy nhận đã tạo 27/11 (root 600); script `observability/tls/tao-chung-chi.sh` và `ca.crt` ở lab (chưa commit) | LOG phiên 4 |

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Lựa chọn | Phép kiểm | Còn mở |
|---|---|---|---|
| **C1.** PR #17 giữ gì | Theo bảng đã duyệt; phần K8s theo C2 (chênh ghi ở bước 3) | Đã có | — |
| **C2.** Cấu hình trong PR để agent tắt chắc chắn và sau này chỉ cần thêm | **Tắt cứng:** `OTEL_AGENT_ENABLED: "false"` trong `env:` của 7 `deployment.yaml` (thắng mọi giá trị từ ConfigMap/Secret), cạnh `HOST_ID` = `spec.nodeName`. **File mẫu Secret không đổi so với main** (không thêm khóa OTEL). **ConfigMap 7 service:** `ENVIRONMENT=production` (entrypoint ghi vào log); các biến chỉ agent đọc: `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318` (Service trong cụm, thêm ở giai đoạn sau), `http/protobuf`, lấy mẫu 10%, metric `otlp`, log `none`, `OTEL_METRICS_EXEMPLAR_FILTER=always_off`, khóa log `traceId`/`spanId`, `…SENSITIVE_QUERY_PARAMETERS` = `q` + 28 tên `vnp_*`, thuộc tính RabbitMQ (event, booking, payment, ticket). **Bỏ:** `SPRING_AUTOCONFIGURE_EXCLUDE` (chuyển sang giai đoạn sau, áp cùng lúc bật agent), `OTEL_CA_PEM_B64`, khối CA trong entrypoint | Bước 4: (a) Collector thử tên `otel-collector`, không TLS, không processor: agent bật (ghi đè thủ công trong lượt thử) gửi được, tham số trong danh sách thành `REDACTED`, không có exemplar; (b) agent tắt: log không có dòng khởi động agent, Collector không nhận gì; (c) render manifest: `env` của container có `OTEL_AGENT_ENABLED=false` | Thứ tự `env` > `envFrom` là quy tắc K8s, không mô phỏng được trên laptop; kiểm thật ở bước 7 |
| **C3.** Lỗi Booking `-P rca-test` (Q1) | Sửa trong `src/rca-test`: `RcaFaultsWebConfig` bỏ qua đăng ký khi không có bean `RcaFaults` (chỉ xảy ra trong test slice). Lỗi này chặn `build.sh verify|all` của exp-app (có `set -e`); mode `build` (`-DskipTests`) không bị | `-P rca-test verify` Booking 0 error; jar production không có lớp `rca-test`; trên exp-app (bước 9): hook Booking nhận lệnh từ file điều khiển như T-067 | — |
| **C4.** Merge có ảnh hưởng máy 84 không? (Q7, Q8, Q10) | Agent tắt cứng; `SPRING_AUTOCONFIGURE_EXCLUDE` không áp ở Phần A. Code B16 **vẫn chạy thật** khi agent tắt: log JSON, filter correlation (gateway, booking), bọc listener RabbitMQ (`RabbitTelemetry`), bỏ `@Valid` trùng ở 6 DTO; đã qua `verify` và kiểm B16, phần ngữ nghĩa (outcome, MDC, ACK) đánh giá ở lượt soát PR bước 5. **Trước merge (bước 6):** đọc chỉ-đọc trạng thái CD của từng service trong plan CD của diff sắp merge (`current`, `previous`, `image`; không đọc `secret-env.json`); service không có đích quay lại thì báo Minh trước khi merge; hẹn nhóm không triển khai trong 60 phút theo dõi; nền bộ nhớ ≤ 30 phút trước merge và GET Q8. **Quay lại:** CD `rollback` khi `previous` còn đúng đích (đối chiếu lại lúc cần); không còn thì PR revert khẩn cấp (Q10). Người bấm: Minh | Bước 7, 60 phút: pod Ready, 0 OOM/restart do bản mới; log không có dòng khởi động agent; log có `environment=production`, `hostId` = tên node; bộ nhớ so Q7; GET Q8 đạt như trước. **Dừng và quay lại** khi pod crash/OOM hoặc GET Q8 trượt mà trước merge đạt. **Báo và trình** khi bộ nhớ vượt Q7 hoặc thiếu mẫu | Kết luận giới hạn ở rollout, tài nguyên và vài request công khai quan sát được; không suy ra đã kiểm toàn bộ giao dịch hay p95 dưới tải |
| **C5.** Dựng exp-app bản mới cho demo (Q5) | Chỉ cho demo. Ghi bản ghim demo: commit, digest image, cấu hình Compose hiệu lực, thành phần giữ nguyên (Keycloak `776d9c9e`, Collector lab, hạ tầng), đích hoàn tác. Chọn bản nào cho W7 để khi Minh mở lại W6/W7 (đối chiếu ngưỡng, fixture, luật, collector, nguồn đầu dò). Kết quả E2/E4, Q4, T-069, T-073 giữ theo pin gốc | Bước 9: kiểm tín hiệu như Q4 T-070; hồi quy V082 hai ca dev (chỉ chứng minh lõi lặp lại trên dữ liệu cũ) | Bản mới có thể khác p95 so với ngưỡng T-072: phát hiện ở lượt nền bước 10 |
| **C6.** Demo đạt nghĩa là gì? (Q6) | Dùng lại tiêu chí chức năng đã khóa của E5 (`results/T-073/khai-truoc-e5.json#/tieu_chi/ket_qua_chuc_nang`, `#/N`, `#/ca_nghiem_thu`). Kịch bản: tải k6 ×1 hành trình mua vé chạy liên tục ≥ 600 s → tiêm `PAUSE-PAYMENT` `--seconds 600` (Docker, không cần hook Booking) → cảnh báo → RCA trực tuyến (W5) → dashboard. **Điều kiện trước khi tiêm:** mọi luật ở trạng thái bình thường, cảnh báo lớp quan sát (mất mẫu) đã hết, và **không có sự cố lớp `he-thong` nào đang mở** trong bộ điều phối (để ca mới không bị gom vào ca cũ, `incidents.py:138–144,183–207`). **Đạt khi:** có sự cố lớp `he-thong` với t̂ ∈ [mốc tiêm, mốc tiêm + 600 s); `che_do_b.kiem_t.t_loi_bang_t_hat = true`; V082 `trung_sha = true`; **mở được** trang ca của chính sự cố đó trên Grafana trong N = 25 phút từ t̂, có đồ thị con và danh sách hạng. **Bỏ sót** (không có sự cố trong cửa sổ) và **quá N** ghi đúng tên như E5. Thiếu phủ đầu vào V082 báo riêng theo WHY-111, không tính là hỏng tuyến khi chức năng đạt. Sổ tiêm chỉ đọc sau lượt. Cảnh báo lớp quan sát ghi riêng. Frontend: không | Bước 10 | Luật im vì thiếu mẫu: kiểm đường thu hoặc kéo dài nền trong thời lượng đã khai; nền khỏe đủ mẫu vẫn cháy: trình T-072 xét ngưỡng cho demo. Một ca đạt chỉ chứng minh đường tích hợp trên bản mới. Phương án trình bày dự phòng: phát lại offline ca E5 (ghi rõ là phát lại) |

## Đầu vào

- Repo FlashTicket `D:/Project/flash-ticket-platform` và worktree `D:/Project/ft-pr17-dung-lai`; chốt `origin/main` và đầu `origin/rca/quan-sat-log` lúc push.
- Repo lab `D:/Project/flashticket-rca-lab` @ main hiện tại (`c1da15f`); đổi file lab thì ghi commit mới và xét lại bước phụ thuộc.
- Chuẩn B16; kết quả T-067, T-069, T-070 (Q4), T-072, T-073 (`khai-truoc-e5.json`); `results/T-076/`.
- Đọc máy: `results/T-070/kiem-ke/tho/lenh/ssh.sh` (exp-app, obs, máy tải); máy 84 chỉ đọc bằng `plink` như LOG phiên 4.
- Không đọc dữ liệu khóa. Không sửa gì trên máy 84.

## Đầu ra

- **PR #17 làm lại** (một PR): `rca/quan-sat-log` đẩy đè bằng `--force-with-lease` khớp đầu nhánh đã soát. Mô tả PR có bảng giữ/bỏ, nói rõ agent tắt cứng, cách mở rộng sau.
- `results/T-076/bang-file-pr17.md` thêm mục "Chênh bản 5" (không sửa số và bằng chứng bản 3).
- `results/T-076/kiem-cuc-bo/` thêm lượt bản 5.
- `results/T-076/sau-merge/`: nền trước merge, digest, kiểm C4 trong 60 phút (chỉ đọc máy 84, cộng request Q8).
- `results/T-076/exp-app/`: kiểm trước, build, cấu hình hiệu lực, triển khai, kiểm tín hiệu, hồi quy V082, lượt nền, diễn tập, `demo.md` (lệnh chạy demo).
- `results/T-076/mo-rong-may-84.md`: việc thêm khi chuyển sang quan sát máy 84.

## Phạm vi ghi

Ngoài `LOG.md` của task và dòng T-076 trong `docs/STATE.md`:
- `results/T-076/`.
- **Repo FlashTicket:** chỉ nhánh `rca/quan-sat-log` (ngoại lệ `AGENTS.md` §12 đã ghi); nhánh local tạm và worktree của nó. Commit `ae5a870` (chưa push) được thay bằng commit theo bản 5.
- **Repo lab:** `observability/tls/` (đã có); `test-environment/` khi bản mới cần (file phủ, xử lý ngrok, `build.sh`, `deploy.sh`) — trình diff trước khi dùng. Không sửa `rca/`, `observability/collector/`, `observability/prometheus/`, luật cảnh báo.
- **exp-app (Phần B, Minh duyệt từng lần dừng/đổi service):** worktree build mới dưới `/opt/flashticket/build/`; cấu hình hiệu lực ghi vào thư mục mới (không ghi đè bộ đang dùng); image mới; triển khai bằng `deploy.sh`; dấu vết tiêm/gỡ lỗi; đổi ngày bán sự kiện tải nếu Q9 cần. Giữ image, cấu hình cũ để hoàn tác.
- **Máy tải (Phần B):** lượt k6 (Q4 bước 9, nền và lượt demo bước 10); đầu ra lượt theo `tai_linux.py`.
- **Obs (Phần B, bước 9):** chạy thẳng `tai_linux.py start` như Q4 T-070 (không dùng `chuoi_tai`): nhật ký và trạng thái ở `/srv/flashticket-rca/load/`, làm mới token pool, khôi phục mock VNPay/đường hầm nếu xảy ra, nhận đầu ra; chạy bộ kiểm tín hiệu (đọc).
- **Obs (Phần B, bước 10, theo runbook `results/T-076/exp-app/runbook-online.md` Minh duyệt trước):** bật bộ nhận T-073 (spool, container), thêm integration vào contact point hiện có qua API Grafana (lưu JSON trước/sau), bộ điều phối RCA trực tuyến ghi `rca/results/online-<lượt>`, sinh dashboard đọc nguồn đó bằng `build_dashboards.py` (sao lưu dashboard hiện tại). Hoàn tác: trả dashboard về `dev`, gỡ integration, dừng bộ nhận T-073. Giữ `t072-bo-nhan` và luật. Không checkout lại bản lab cũ.
- **exp-app (Phần B):** cũng gồm đơn mua phát sinh trong DB thử do lượt k6 (không hoàn tác được bằng đổi image).
- **Máy 84:** không ghi gì; chỉ đọc (pod, bộ nhớ, log, trạng thái CD `current`/`previous`/`image`) và request Q8.
- **Ngoài quyền agent, Minh làm:** merge PR, bấm `rollback` nếu cần, báo nhóm hệ thống.

## Các bước

**Phần A — PR #17**
1. ✔ Bảng file (Minh duyệt 26/11).
2. ✔ Dựng lại nhánh (5 commit: log B16, `rca-test`, CI, agent, GOV).
3. **K8s theo C2:** thay commit `ae5a870` bằng commit mới; ghi "Chênh bản 5" vào bảng file. Kiểm bằng bộ kiểm K8s của nhóm (`test-k8s-*.py`).
4. **Sửa lỗi `rca-test` (C3)** và **kiểm cục bộ lại** bằng script đã có (lượt mới dùng Collector HTTP tên `otel-collector`, bỏ phần TLS/token của lượt bản 3): đủ phép kiểm C2, C3.
5. Push có lease; CI GitHub; Codex soát PR (khối Soát kết quả); Minh đọc theo hướng dẫn review (44 file Java ngoài test).
6. Trước merge (C4): đọc trạng thái CD từng service trong plan CD; hẹn nhóm không triển khai trong 60 phút; nền bộ nhớ và GET Q8. Ghi `results/T-076/sau-merge/truoc.md`. Service không có đích quay lại: báo Minh, Minh quyết merge hay dời. Minh merge vào giờ chọn với nhóm. CD tự triển khai.
7. **Sau merge (C4)**, 60 phút, ghi `results/T-076/sau-merge/`.

**Phần B — exp-app cho demo** (sau bước 7)

8. **Kiểm trước, không đổi gì đang chạy:** diff `deploy/app/*.yml` main mới với `36a3725d`; xử lý ngrok trong file phủ lab; dựng cấu hình hiệu lực bằng `hieu_luc.py` vào thư mục mới và so với bộ đang dùng; tag image cũ còn tồn tại; nơi đặt mock VNPay; schema/realm/fixture bản mới có cần đổi dữ liệu không (đổi thì trình riêng quyền và thời gian); ngày bán sự kiện tải so với lịch demo (Q9); mode `build.sh` dùng; dự toán thời gian build (dựa trên lượt build ARM của T-067) và thời gian dừng; các bước hoàn tác và giới hạn (hoàn tác image không hoàn tác đơn mua đã ghi vào DB thử). Trình Minh.
9. Build ARM trên exp-app từ commit merge, triển khai (`deploy.sh`), kiểm tín hiệu như Q4 T-070 (lượt `tai_linux.py start` 10 phút ×1, đơn COMPLETED, bộ kiểm tín hiệu), hồi quy V082 hai ca dev, hook Booking/Event nhận lệnh như T-067. Ghi bản ghim demo (C5).
10. **Diễn tập demo** theo C6. Điều kiện bắt đầu: T-070 `REVIEW-5` đã kiểm bản sửa lab và Minh kết luận về RCA trực tuyến; Minh duyệt `runbook-online.md` (áp và hoàn tác trên `c1da15f`, thời lượng nền ≥ 600 s, tiêm 600 s, chờ kết quả tới N = 25 phút, tổng ≤ 1 giờ). Trước khi tiêm kiểm hai đường: Grafana → spool của bộ nhận, và dashboard đọc đúng bộ `online-<lượt>`. Ghi mốc thời gian, `results/T-076/exp-app/demo.md`. Xong: hoàn tác theo runbook nếu Minh không muốn giữ.

## Mở rộng sang máy 84 (giai đoạn sau, không làm trong task)

Phần A được thiết kế để giai đoạn này **chỉ thêm**, cùng vài sửa nhỏ đã biết trước:

| Việc | Ở đâu |
|---|---|
| **Thêm** Collector 1 pod (Deployment, Service `otel-collector`, ConfigMap): nhận OTLP trong cụm, lọc như exp-app (`filter/health`, `transform/sanitize` xóa query) và thêm xóa `exception.message`, lọc hoặc bỏ `exception.stacktrace`; nén; gửi obs qua TLS + token; hàng đợi gửi lại; không ghi dữ liệu thô ra file | FlashTicket `deploy/k8s/otel-collector/` (mới) |
| **Thêm** đường CD cho image dựng sẵn: `.github/services.json`, nhánh "image" trong `_deploy-service.yml`, tên Collector và quy tắc kiểm (không Eureka) trong `deploy-k8s-service.sh`, bộ kiểm CD | FlashTicket `.github/`, `deploy/scripts/` (nhóm duyệt) |
| **Thêm** Secret token của Collector | File mẫu mới trong `deploy/k8s/examples/` |
| **Thêm** đường nhận trên obs: Collector + Prometheus riêng, datasource và dashboard chạy thật, truy vấn Tempo thực nghiệm lọc `exp`, tường lửa cho IP máy 84 | Lab `observability/` (file mới); CA đã có |
| **Thêm** `SPRING_AUTOCONFIGURE_EXCLUDE` (Lettuce observation) ở gateway, booking, assistant | ConfigMap của các service đó |
| **Sửa nhỏ** `OTEL_AGENT_ENABLED: "false"` → `"true"` cho service bật | `deployment.yaml` của service đó |
| **Sửa nhỏ** giới hạn bộ nhớ của service bật agent | `deployment.yaml` (nhóm quyết RAM cụm) |

**Điều kiện trước khi bật (OPEN):** kiểm payload thô bằng bộ sentinel giả ở nguồn và ở bản ghi đầu tiên gửi ra ngoài, gồm span event; Minh quyết Collector trong cụm có được coi là biên lọc của B16 §6 ("whitelist trước khi ghi/xuất") hay phải lọc trước khi rời tiến trình Java (khi đó cần hạn chế instrumentation hoặc lọc trong Java); số đo bộ nhớ thật dưới tải của từng service (+118 MiB chỉ là số Booking trên laptop, không dùng làm dự báo chung); phí AWS cho lượng gửi ra Internet (**chưa kiểm**).

## Kiểm đúng đắn

- **Không đổi phương pháp:** `src/m1`, `src/m1_ft`, `src/p3`, bản chụp `b0f79a4d…`, lab `rca/` không đổi. Hồi quy V082 hai ca trùng byte ở bước 9.
- **Máy 84 không gửi dữ liệu:** tắt cứng bằng `env:`; kiểm bước 4 và bước 7.
- **Agent tắt và biến Spring không áp:** diff ConfigMap ở bước 3 không có biến Spring mới. Code B16 vẫn chạy thật (C4); ngữ nghĩa đánh giá ở lượt soát PR, vận hành kiểm ở bước 7 trong giới hạn Q8.
- **Không lộ bí mật:** không có khóa riêng, token trong git (`git grep` trước mỗi commit).
- **Đúng nghĩa thay đổi trên main:** bảng C1, 3 file Java xung đột qua test, CI xanh.
- **Thiết kế mở:** mục "Mở rộng" không đòi xóa file nào của Phần A; sửa chỉ ở giá trị công tắc, giới hạn bộ nhớ và thông tin kết nối.

## Tiêu chí xong

1. PR #17 (một PR) trên main mới nhất, không xung đột, CI xanh, qua phản biện Codex và Minh đọc; Minh merge.
2. Sau merge: agent không chạy trên máy 84 (log không có dòng khởi động agent), pod ổn định 60 phút và trong ngưỡng theo C4, kiểm chức năng đạt.
3. exp-app chạy bản demo mới, kiểm tín hiệu đạt như Q4, hồi quy V082 có kết quả; bản ghim demo ghi đủ; bản cũ còn hoàn tác được.
4. Diễn tập demo đạt theo C6, có `demo.md`.
5. `mo-rong-may-84.md` liệt kê đủ việc thêm, sửa nhỏ, điều kiện OPEN và số liệu RAM.

## Không làm

- Không bật agent hay gửi dữ liệu từ máy 84; không sửa CD chung của nhóm.
- Không đổi phương pháp RCA; không chọn lại ngưỡng cảnh báo (nếu C6 cho thấy cần, trình riêng cho T-072).
- Không chọn bản FlashTicket cho W7.
- Không đưa frontend vào exp-app.

## Chi phí ước lượng

| Phần | Ước lượng |
|---|---|
| A (bước 3–5) | 1 phiên; kiểm cục bộ khoảng 30 phút máy (lượt bản 3: verify ~16 phút) |
| A (bước 6–7) | Theo giờ merge; 60 phút theo dõi chỉ đọc |
| B | 1–2 phiên; build ARM (dự toán ở bước 8 từ lượt T-067); exp-app dừng khoảng 10 phút khi đổi bản (mốc T-070, cập nhật ở bước 8); nền + diễn tập khai thời lượng trước, mỗi lượt ≤ 1 giờ |

Không lượt nào dài hơn 1 giờ ngoài theo dõi; nếu dự toán bước 8 cho thấy vượt, trình chi phí và cách giữ phần đã xong (AGENTS §3.21). Không tải hơn 5 GB.

## Rủi ro và điều chưa chắc

- **Merge là triển khai ngay** trên máy 84; nhóm đang triển khai liên tục: chọn giờ merge với nhóm. Đường `rollback` hết hiệu lực sau lần triển khai thành công kế tiếp.
- **Bản mới trên exp-app** có thể khác hành vi so với `36a3725d` (p95, luồng mua vé, dữ liệu): phát hiện ở bước 8–10.
- **Tuyến vận hành lab** (bộ chuỗi tải, RCA trực tuyến) phụ thuộc kết luận T-070 REVIEW-5.
- **Hạn bán sự kiện tải** 02/12/2026 22:16Z: demo sau mốc này cần đổi ngày bán (Q9).
- **Danh sách chặn query** và tắt exemplar chỉ là lớp giảm dữ liệu cho giai đoạn sau.

## Quyết định cần Minh khi duyệt SPEC

Giữ quyết định đã duyệt ở bản 3: Assistant chỉ agent; build hai kiến trúc của main; ngoại lệ AGENTS §12 (đã ghi). Các mục bản 3 về đường nhận, ngưỡng bật agent, người giữ `ENV_<SVC>`, giới hạn rollback khi bật chuyển sang giai đoạn mở rộng.

| Mã | Câu hỏi | Đề xuất |
|---|---|---|
| Q1 | Sửa lỗi Booking `-P rca-test` trong PR này | Có |
| Q2 | Đích agent | `http://otel-collector:4318` trong cụm |
| Q3 | Lớp giảm dữ liệu ở nguồn | `q` + 28 tên `vnp_*`; tắt exemplar |
| Q4 | Công tắc agent | Tắt cứng bằng `env:` trong `deployment.yaml`; file mẫu Secret không đổi; bỏ CA/token khỏi pod |
| Q5 | Dựng exp-app cho demo | Sau bước 7; chỉ cho demo; chọn bản W7 để khi mở lại W6/W7 |
| Q6 | Nội dung demo | Kịch bản và tiêu chí C6, không frontend, có phương án phát lại offline dự phòng |
| Q7 | Ngưỡng bộ nhớ sau merge | Trung bình mỗi bản của từng service tăng quá 10% so với nền đo ngay trước merge thì **báo và trình** (không tự quay lại); số bản đổi hoặc thiếu mẫu thì báo riêng |
| Q8 | Kiểm chức năng ngắn trên máy 84 trước và sau merge | Có. Khai trước ở `sau-merge/truoc.md`: 2–3 GET công khai qua `http://52.64.237.84` (danh sách sự kiện; availability một sự kiện lấy từ danh sách), mỗi cái 3 lần; đạt khi HTTP 200 và có các trường chính của JSON như lần trước merge. Không phải kiểm giao dịch đầy đủ |
| Q9 | Ngày bán sự kiện tải nếu demo sau 02/12/2026 22:16Z | Kiểm ở bước 8, trình cách đổi (ghi DB thử trên exp-app) trước khi làm |
| Q10 | Đường quay lại khi CD không về được | Minh duyệt trước một PR revert khẩn cấp của commit merge PR #17, chỉ dùng khi sự cố (ngoại lệ có chủ đích với nguyên tắc một PR) |

## Prompt bàn giao

Prompt cho Codex kiểm lại bản 6 nằm ở cuối `LOG.md` của task này.
