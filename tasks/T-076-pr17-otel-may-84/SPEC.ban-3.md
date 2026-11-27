# T-076 — Làm lại PR #17 trên main mới nhất, bật OTel agent cho FlashTicket chạy thật (máy 84)

- **Trạng thái:** **Minh duyệt bản 3 ngày 26/11/2026** ("Duyệt luôn bản 3"), gồm Q1–Q10 theo cột đề xuất; còn chờ IP ra Internet của máy 84 (trước bước 6) và người giữ bản đầy đủ `ENV_<SVC>` (Q9, trước bước 9). Sửa theo `REVIEW.md` (R1–R7) và `REVIEW-2.md` (N1–N4) của Codex. Bản cũ: `SPEC.ban-1.md`, `SPEC.ban-2.md`.
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P9 (kho quan sát và tích hợp), P10 (thực nghiệm trên FlashTicket và demo) — **Cổng:** ngoài G0–G4 (việc tích hợp, không phải đánh giá phương pháp)

## Mục tiêu

**Nguồn:**
- DT18-NV1: hệ thống bán vé phân tán.
- DT18-NV2: "Dữ liệu log, trace và metrics được thu thập…", đối chiếu `docs/reference/sources/DT18-de-tai-va-nhiem-vu.md` §2.
- MRP P9a: yêu cầu quan sát cho RCA theo chuẩn B16; `service.name` thống nhất trên cả ba tín hiệu.
- MRP P10: thực nghiệm và demo trên FlashTicket.

**Mong muốn của Minh (chat 24–26/11/2026):**
- Y11: phần log, telemetry, observability của FlashTicket do Minh toàn quyền quyết, miễn không ảnh hưởng hệ thống.
- Y12: dùng bản FlashTicket mới nhất cho thống nhất.
- Ngày 26/11: bật Java agent cho máy 84 **không sửa tay trên máy**. Dọn những chỗ lỗi thời của PR #17. **Chỉ một PR:** làm lại chính PR #17, không merge PR #17 rồi tạo thêm PR khác.

**Task này là cài đặt và tích hợp:**
- Đưa chuẩn quan sát B16 (log JSON, OTel agent) từ PR #17 vào main mới nhất của nhóm.
- Cho bản chạy thật trên K8s (máy 84) gửi trace và metric về máy quan sát exp-obs, qua một đường **tách hẳn** khỏi đường thực nghiệm.

**Task không đánh giá phương pháp RCA**, không đổi phương pháp, không đổi đường dữ liệu vào RCA. Đạt task này cho:
- (a) FlashTicket chạy thật có trace và metric trên Grafana (log máy 84 để sau, xem C2);
- (b) một nhánh "main mới nhất + quan sát" để sau này ghim lại bản thử nghiệm trên exp-app (pha 4, duyệt riêng).

Task không cho kết luận nào về chất lượng RCA trên bản chạy thật. Ánh xạ ba tín hiệu của máy 84 lên đồ thị, phát hiện và xếp hạng trên máy 84 nằm ngoài task.

## Hiện trạng đã kiểm (26/11/2026, chỉ đọc)

| Điều | Thực tế | Nguồn |
|---|---|---|
| Repo FlashTicket trên laptop | Nhánh `rca/exp-2026-11` @`36a3725` = main `640dbaf` (18/11) + PR #17 `bb84d64` | `git log` |
| Main trên GitHub | `f178870` (22/11), hơn `640dbaf` 52 commit / 171 file | `gh api compare` |
| PR #17 (`rca/quan-sat-log`) | OPEN, CONFLICTING; trước main 10 commit, tụt 92; sửa 124 file (+5.028/−214) | `gh pr view 17`; `git diff --stat` |
| Xung đột với main | 13 file: 7 Dockerfile; `OrderServiceImpl`, `PromotionServiceImpl`, `RefundServiceImpl`; `payment-service/.env.example`; `deploy/app/{README.md,payment-service.yml}` | `git merge-tree` |
| Triển khai trên main | 10/10 service `runtime: k8s`. CD chạy khi push `main`: build image **hai kiến trúc** (`linux/amd64,linux/arm64`), SSH vào máy 84, triển khai | `.github/services.json`, `_deploy-service.yml:79–82,118` @main |
| Bí mật qua CD | CD ghi `ENV_<SVC>` thành file dotenv trên máy 84 (**ghi thay toàn bộ**), rồi script chỉ đưa vào Secret K8s **những khóa có khai** trong `deploy/k8s/examples/<svc>.secret.env.example` (khóa dưới `# Optional` không bắt buộc). `discovery-server`, `frontend` không có Secret | `deploy/scripts/deploy-k8s-service.sh:196–236` @main |
| Bật lại/hoàn tác qua CD | `cd.yml` chạy tay có ba chế độ: `deploy`; `restart` (tạo lại với digest đang chạy, dùng sau khi cập nhật `ENV_<SVC>`); `rollback` (một service, digest phải đúng image của revision ghi trong `previous`, áp lại cả snapshot Secret của revision đó). CD chỉ nhớ **một** revision trước: mỗi lần `deploy`/`restart` thành công ghi `previous` = `current` cũ. Nhóm `k8s` gồm cả 10 service (kể cả discovery, Keycloak, frontend) | `cd.yml:6–18`; `deploy-k8s-service.sh:46–50,170–190,261–271`; `.github/scripts/plan-deploy.sh:19–28` @main |
| Pod | `runAsNonRoot`, không đặt `readOnlyRootFilesystem`; booking giới hạn 768 MiB; `envFrom` ConfigMap rồi Secret | `deploy/k8s/booking-service/deployment.yaml` @main |
| Agent trên main | Không có. Dockerfile chạy `java` trực tiếp | `services/*/Dockerfile` @main |
| Agent trong PR #17 | Agent 2.33.1 và `docker-entrypoint.sh`; mặc định `OTEL_AGENT_ENABLED=false`; khi bật thì `OTEL_LOGS_EXPORTER=none` | `docker-entrypoint.sh` @`bb84d64` |
| CI kiểm B16 trong PR | Bước `Validate B16` chạy cho mọi service Maven trừ `keycloak`, đọc `target/b16-log-samples.jsonl`; chỉ 7 service có file mẫu này | `_maven-verify.yml:94` @`bb84d64` |
| Máy quan sát | Gateway OTLP nghe `10.0.0.215:4317/4318` (IP nội bộ Oracle), chỉ có `memory_limiter`, `batch`; ghi trace/metric/log vào file vòng `capture` mà RCA dùng; trace qua connector `span_metrics`, `service_graph` sinh metric vào Prometheus. iptables chỉ nhận `10.0.0.0/24` và SSH. RAM còn trống ~10 GB/12 GB, đĩa 46% | lab `c1da15f` `observability/collector/gateway.yaml:114–153`; SSH `free -m`, `df` |
| Lớp lọc ở exp-app | Collector agent exp-app có `filter/health` và `transform/sanitize` (bỏ query URL) trước khi gửi gateway | lab `observability/collector/agent-docker-host.yaml:161–182,225–234` |
| Đọc Tempo | Hai bộ đóng gói RCA không đọc Tempo. Bộ kiểm tín hiệu `tests/signals/check_purchase_journey.py` (dùng ở T-067, Q4 T-070) tìm trace trong Tempo bằng TraceQL theo tên service/route, **không lọc môi trường**. Trace exp-app có `resource.deployment.environment="exp"`: trong cửa sổ Q4, `booking-service` 200/200 trace có nhãn này, 0 trace không có (giới hạn 200). Grafana: datasource `tempo` trỏ bản đồ dịch vụ (`serviceMap`) về Prometheus thực nghiệm; provisioning mount từ `observability/grafana/provisioning` | lab `c1da15f` `tests/signals/check_purchase_journey.py:41–54`, `provisioning/datasources/datasources.yaml:21–33`; SSH truy vấn Tempo 26/11 |
| RCA đọc metric | Bộ đóng gói lấy metric bằng truy vấn **gộp theo `service_name`**, không lọc môi trường (`sum by(service_name)`, `sum by(le,service_name)`), nằm trong bản chụp phương pháp đã khóa. Luật cảnh báo cũng lọc theo `service_name` | RCA `25550d2a5:src/m1/adapter_flashticket.py:24–36`; lab `rca/lib/stage_m1.py:81`, `rca/online/stage_b.py:149–163` |

Hệ quả: nếu máy 84 gửi vào gateway và Prometheus hiện có, metric hai môi trường bị cộng lẫn trước khi RCA đọc, và trace máy 84 lẫn vào file capture. Không sửa được bằng lọc ở phía RCA mà không đổi bản phương pháp đã khóa (REVIEW R1). Trace máy 84 vào Tempo chung thì bộ kiểm tín hiệu cần lọc `exp` (REVIEW-2 N2).

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Lựa chọn và giải thích khác | Phép kiểm, bằng chứng | Phần còn mở |
|---|---|---|---|
| **C1.** Phần nào của PR #17 còn cần? | Giữ: log B16, kiểm log trong CI (sửa theo C6), agent và entrypoint (sửa theo C3), hook `rca-test`, truyền `SERVICE_VERSION` khi build. Bỏ: build đa kiến trúc của PR (main đã có), phần Compose/CI thời Compose. Xét riêng: Keycloak native tracing (exp-app có receiver `otlp/keycloak`), `decision-register.md` | Bước 1: bảng từng file và từng hunk (giữ / bỏ / sửa), lý do, đối chiếu main và file phủ lab `test-environment/overrides`. Minh duyệt bảng | Phần exp-app còn dùng (Keycloak tracing): ghi trong bảng; nếu bỏ, pha 4 khai rõ tín hiệu mất |
| **C2.** Log của máy 84 (Q1) | (a) OTLP log từ agent. (b) Collector DaemonSet đọc log pod. **(c) Lần bật đầu chỉ trace và metric** (đề xuất). Lý do: (a) chưa có bằng chứng giữ đủ trường B16 và sạch dữ liệu; (b) thêm vận hành trên K8s | (c): không có log máy 84 trong Loki | Thiếu log máy 84: không nghiệm thu đủ ba tín hiệu ở máy 84, không dùng H8 ở đó. Ba tín hiệu cho thực nghiệm vẫn từ exp-app. Mở (a)/(b) là quyết định sau, kèm kiểm schema B16 với sentinel |
| **C3.** Đường gửi và bảo mật (Q4) | **Collector riêng cho máy 84** (`collector-production`) trên obs: OTLP/HTTP qua **HTTPS** (giao thức mặc định của Java agent 2.x), chứng chỉ do CA tự ký, SAN = IP công khai của obs; xác thực token bearer (extension `bearertokenauth`); nghe trên IP nội bộ `10.0.0.215`, cổng mới; iptables và Security List chỉ mở cho IP ra Internet của máy 84. **Lọc trường cấm theo B16 §6 ở nguồn** (cấu hình agent, REVIEW-2 N3); lớp lọc ở `collector-production` giống agent exp-app (`filter/health`, `transform/sanitize`) chỉ là dự phòng | Bước 4 (trước khi dữ liệu rời nguồn): agent gửi tới collector cục bộ **không processor**, xuất thô ra file; request giả có sentinel trong query URL, header, body, tham số DB; payload thô không có sentinel, vẫn còn span/metric dùng được (route, status, DB/queue). Bước 6: đúng token đạt; sai token, không token bị từ chối 401; không TLS bị từ chối; máy tải làm đối chứng bị chặn ở tường lửa; bản ghi nhận được không có sentinel | IP ra của máy 84 (Minh cung cấp). Nếu IP đổi hoặc không xác minh được: không bật agent. Agent không lọc được ở nguồn một loại instrumentation: tắt instrumentation đó, hoặc giữ agent tắt tới khi Minh duyệt cách lọc khác |
| **C3b.** Token và CA tới pod (REVIEW R2) | Token: khóa `OTEL_EXPORTER_OTLP_HEADERS` thêm vào mục `# Optional` của file mẫu Secret 7 service (api-gateway, user, event, ticket, booking, payment, assistant). Bật/tắt: khóa `OTEL_AGENT_ENABLED` cũng ở `# Optional` (không khai = tắt). CA (công khai): `OTEL_CA_PEM_B64` trong `configmap.yaml` của từng service; entrypoint giải ra `/tmp/otel-ca.pem` và đặt `OTEL_EXPORTER_OTLP_CERTIFICATE`. Không sửa script CD chung. `discovery-server` không bật agent lần đầu | Bước 4: chạy đoạn Python lọc khóa của `deploy-k8s-service.sh` với file dotenv giả → Secret có đủ hai khóa; entrypoint với CA giả → file CA đúng, agent nhận đường dẫn. **Chưa kiểm**: agent đọc CA và header đúng dạng (`Authorization=Bearer%20…`) | Thiếu trace `discovery-server` (khai phủ). `ENV_<SVC>` bị CD ghi thay toàn bộ: phải có người giữ bản đầy đủ trước khi sửa (Q9) |
| **C4.** Dữ liệu máy 84 có làm bẩn thực nghiệm không? (REVIEW R1) | **Tách ở lớp thu**: `collector-production` không ghi file `capture`, không đi qua gateway hiện có; metric (kể cả metric sinh từ trace bằng connector riêng của nó) vào **Prometheus riêng** (`prometheus-production`); trace vào Tempo chung và log (nếu có sau này) vào Loki chung, gắn `deployment.environment=production`. Không sửa `stage_m1.py`, `stage_b.py`, luật T-072, bản phương pháp. Phương án khác: lọc nhãn trên Prometheus chung — phải sửa truy vấn trong bản đã khóa, bỏ | Bước 7, cửa sổ trộn: gửi dữ liệu tổng hợp gắn `production` qua cổng mới, đủ để làm đổi các truy vấn RCA nếu bị trộn, đồng thời exp-app có tải nền. Kiểm: đối chứng dương — dấu tổng hợp có trong `prometheus-production` và Tempo với nhãn `production`; Prometheus thực nghiệm **0 chuỗi** có `deployment_environment="production"`; file `capture` không có span `production`; hai bộ đóng gói chạy truy vấn Prometheus thật trên cửa sổ trộn (`RCA_M1_ROOT` thử riêng, mã mờ mới; không dùng `--prom-tu-file`): gói trace không có dấu `production`, metric exp-app vẫn đủ; 11 luật không đổi trạng thái do dữ liệu `production`; bộ kiểm tín hiệu (đã lọc `exp`) trên cửa sổ trộn không lấy trace `production`. Hồi quy V082 hai ca trùng byte | **Tempo chung** (REVIEW-2 N2): mọi truy vấn Tempo dùng làm bằng chứng thực nghiệm phải lọc `resource.deployment.environment="exp"` — sửa bộ kiểm tín hiệu ở lab; dashboard chạy thật lọc `production`. Tách Tempo riêng chưa làm (tốn tài nguyên), xét lại nếu tải kho chung tăng |
| **C5.** Agent có làm hỏng hệ thống chạy thật không? (REVIEW R4) | Ngưỡng khai trước (Q7, Minh duyệt): đo **phía client** bằng một kiểm hành trình ngắn từ máy tải tới URL công khai của 84 (GET công khai; mua thử chỉ khi Minh cho), cùng kịch bản trước và sau khi bật agent: p95 sau ≤ 1,3 × p95 trước, tỷ lệ lỗi không tăng; pod Ready, 0 OOM, 0 restart trong 60 phút; `collector-production` không từ chối/rơi dữ liệu (`otelcol_receiver_refused_*`, `otelcol_exporter_send_failed_*` = 0) và tuổi mẫu thực nghiệm (luật `t072-mat-*`) không đổi | Bước 8–9. Hoàn tác (REVIEW-2 N1), làm **từng service**, không dùng nhóm `k8s`/`all`: (i) sau merge, agent tắt: kiểm nền; image mới (B) có lỗi → `rollback` về image trước merge (A) **ngay lúc này**, khi `previous` còn là A; (ii) sau khi bật: vượt ngưỡng → bỏ hai khóa khỏi bản đầy đủ `ENV_<SVC>`, `restart` → B tắt agent (không dùng `rollback`, vì snapshot Secret của `previous` có thể còn khóa bật). Trước mỗi `restart`, `ENV_<SVC>` trên GitHub là bản đầy đủ đúng trạng thái muốn có | Overhead thật dưới tải chạy thật: chỉ đo được sau khi bật; kiểm hành trình ngắn không đại diện tải thật (khai giới hạn). **Giới hạn (Q10):** sau khi đã bật agent, CD không còn quay về A; muốn về A phải có commit revert trên main (một PR khác) hoặc một đường CD do nhóm hệ thống chỉ ra trước bước 9 |
| **C7.** Grafana hiện dữ liệu máy 84 đúng nguồn? (REVIEW-2 N4) | Thêm datasource `prometheus-production` và `tempo-production` (cùng Tempo, `serviceMap` trỏ `prometheus-production`, mặc định lọc `production`); dashboard hệ thống bản chạy thật dùng hai datasource này. Nạp bằng API `POST /api/admin/provisioning/datasources/reload` (quyền admin hiện có), không restart Grafana. Giữ nguyên UID, datasource, luật cũ | Bước 6: sau reload, API liệt kê đủ datasource cũ + 2 mới, health OK; dashboard mới mở được; ở bước 9, panel thấy metric và trace của máy 84; dashboard thực nghiệm không đổi (4/4 mở, dữ liệu 109 ca như kiểm 26/11) | Reload lỗi: Minh chọn cửa sổ restart Grafana (ảnh hưởng đánh giá cảnh báo vài chục giây) hoặc dời phần dashboard, ghi tiêu chí chưa đạt |
| **C6.** CI kiểm B16 và `assistant-service` (Q2, REVIEW R5) | Kiểm B16 chỉ cho danh sách service có hợp đồng B16 (file danh sách trong `deploy/observability/`); service trong danh sách mà thiếu file mẫu = lỗi; thay verifier/schema thì chạy lại đúng danh sách. Assistant: **(a) chỉ agent** (đề xuất), không vào danh sách B16; (b) agent + log B16; (c) không đụng. Giữ cách main cài Maven/registry cho Assistant | CI xanh trên GitHub; local chạy đúng lệnh registry của từng service | Log Assistant ngoài B16 (a) |

## Đầu vào

- Repo FlashTicket `D:/Project/flash-ticket-platform`: chốt `origin/main` và đầu `origin/rca/quan-sat-log` ngay lúc dựng (hiện `f178870`, `bb84d64`); `origin/rca/exp-2026-11` @`36a3725`.
- Repo lab `D:/Project/flashticket-rca-lab` @`c1da15f` (main hiện tại). `85ace52` chỉ dùng khi dẫn bằng chứng Q4 của T-070.
- Chuẩn B16: `docs/architecture/B16-observability-baseline.md` (repo FlashTicket).
- Kết quả T-067 (bản ghim, kiểm tín hiệu), T-070 (đợt dọn, Q4), T-072 (luật cảnh báo).
- Đọc máy bằng `results/T-070/kiem-ke/tho/lenh/ssh.sh`, chỉ lệnh đọc, trừ các bước ghi đã duyệt ở dưới.
- **Không** đọc dữ liệu khóa. **Không** vào máy 84 bằng tay; mọi thay đổi trên máy 84 đi qua CD của nhóm.

## Đầu ra

- **PR #17 làm lại** trên `main` mới nhất: nhánh `rca/quan-sat-log` dựng lại và đẩy đè bằng `--force-with-lease` khớp đầu nhánh đã soát. Mô tả PR có bảng giữ / bỏ, cách bật/tắt agent qua `ENV_<SVC>` + CD `restart`, cách hoàn tác.
- `results/T-076/bang-file-pr17.md`: bảng giữ / bỏ / sửa từng file và hunk (C1).
- `results/T-076/kiem-cuc-bo/`: build và test (lệnh registry), kiểm entrypoint (tắt, bật, CA, header), kiểm payload thô của agent có sentinel (lọc ở nguồn), kiểm lọc khóa Secret với dotenv giả, render manifest K8s.
- **Commit repo lab:** `collector-production` và `prometheus-production` trong compose, cấu hình Collector riêng, Prometheus riêng, datasource `prometheus-production`, `tempo-production` và một dashboard hệ thống cho bản chạy thật (UID mới), bộ kiểm tín hiệu lọc `exp` khi đọc Tempo, script chứng chỉ và tường lửa, tài liệu. Không đổi gateway, Prometheus, luật cảnh báo, bộ đóng gói hiện có.
- `results/T-076/kiem-tach/`: kiểm C3 (token, TLS), C4 (cửa sổ trộn, bộ kiểm tín hiệu, hồi quy), C7 (reload datasource).
- `results/T-076/kiem-sau-bat/`: kiểm C5 trước và sau khi bật agent.
- (Pha 4, nếu Minh duyệt riêng) `results/T-076/ban-ghim-moi/`.

## Phạm vi ghi

Ngoài `LOG.md` của task và dòng T-076 trong `docs/STATE.md`:
- `results/T-076/`.
- **Repo FlashTicket:** chỉ nhánh `rca/quan-sat-log` (PR #17), kể cả force-push có lease. **Không** đẩy vào `main`, không đụng nhánh khác. Merge PR là việc của Minh.
  - Cần ngoại lệ ở `AGENTS.md` §12 (Q5), ghi **trước** khi ghi repo FlashTicket. Đề xuất chữ: "Riêng nhánh `rca/quan-sat-log` (PR #17, task T-076) được sửa và force-push khi Minh duyệt; không đẩy vào `main`, không đụng nhánh khác."
- **Repo lab:** `observability/compose.yaml` (thêm hai service, không đổi service cũ), `observability/collector/production.yaml` (mới), `observability/prometheus/production.yaml` (mới), `observability/grafana/provisioning/datasources/*`, `observability/grafana/dashboards/10-system/` (thêm một file), `observability/grafana/build_dashboards.py` (chỉ thêm bản chạy thật), `observability/tls/` (CA công khai, script tạo chứng chỉ; **không** đưa khóa riêng, token vào git), `tests/signals/check_purchase_journey.py` (chỉ thêm lọc `resource.deployment.environment` vào truy vấn Tempo, mặc định `exp`), `inventory/`, `docs/`. **Không** sửa `gateway.yaml`, `prometheus.yaml`, `alerting/rules.yaml`, `rca/`.
- **Máy obs** (bước 6–7, sau khi Minh duyệt từng bước): bật hai container mới, iptables cho cổng mới, reload datasource provisioning của Grafana bằng API; khóa riêng và token ở `/etc/flashticket-rca/production/` (root 600).
- **GitHub Secrets** `ENV_<SVC>` của repo FlashTicket: chỉ ở bước 9, Minh duyệt riêng lúc làm, khi đã có bản đầy đủ của từng `ENV_<SVC>` (Q9).
- **Ngoài quyền của agent, Minh tự làm:** Security List trên Oracle, merge PR, chạy CD `restart`/`rollback` nếu Minh muốn tự bấm, báo nhóm hệ thống.

## Các bước

**Pha 1: PR (chưa đụng máy)**
1. **Kiểm kê C1** — bảng từng file và hunk của PR so với main tại thời điểm dựng, kèm file phủ lab. Minh duyệt bảng.
2. **Dựng lại nhánh.** Nhánh tạm từ `origin/main`, áp phần giữ thành vài commit theo chủ đề (log B16, CI B16 theo danh sách, agent + entrypoint, hook `rca-test`, K8s, assistant). Gỡ 13 xung đột theo code main; 3 file Java giữ logic nghiệp vụ của main, chỉ chèn lệnh ghi log. Kiểm: `git diff origin/main` chỉ gồm các nhóm trên.
3. **Thêm K8s:** khóa `# Optional` trong 7 file mẫu Secret (C3b); `OTEL_CA_PEM_B64`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `ENVIRONMENT=production`, `HOST_ID` trong `configmap.yaml` của 7 service; entrypoint ghi CA ra `/tmp`. Kiểm: script kiểm K8s có sẵn của nhóm (`.github/scripts/test-k8s-*.py`).
4. **Kiểm cục bộ** (vào `results/T-076/kiem-cuc-bo/`):
   - build và test bằng lệnh registry của từng service, gồm bước B16 cho danh sách, `-P rca-test` cho Booking và Event;
   - build image một service có agent (Booking) và Assistant; khởi động với agent tắt và bật (gửi tới một collector cục bộ có TLS + token giả), đo bộ nhớ lúc khởi động;
   - **lọc ở nguồn (N3):** collector cục bộ không processor, xuất thô ra file; gửi request giả có sentinel trong query URL, header, body, tham số DB; chọn cấu hình agent tới khi payload thô không có sentinel mà vẫn còn span/metric dùng được; không đạt thì ghi instrumentation phải tắt;
   - chạy đoạn lọc khóa Secret của CD với dotenv giả;
   - kiểm `service.version` = revision, không nhận `local-dev`.

   **Sau đó:** force-push có lease, CI GitHub chạy. **Chưa merge.**
5. **Phản biện.** Codex soát PR. Minh đọc theo hướng dẫn review (danh sách chỗ cần đọc kỹ, gồm 39 file nghiệp vụ).

**Pha 2: máy quan sát sẵn sàng (trước khi merge)**

6. **Đường thu riêng (C3).** Tạo CA và chứng chỉ (SAN = IP công khai obs), token; bật `collector-production`, `prometheus-production`; iptables chỉ cho IP máy 84. Minh mở Security List. Kiểm từ một nguồn được phép tạm thời (khai trước, gỡ sau kiểm) với cùng cấu hình TLS/token: đúng token đạt, sai/không token 401, không TLS bị từ chối; máy tải bị chặn. Bản ghi nhận được không còn sentinel (lớp dự phòng). Thêm datasource, reload provisioning bằng API, kiểm theo C7; datasource và dashboard cũ không đổi.
7. **Kiểm tách (C4)** như cột phép kiểm ở bảng trên, gồm bộ kiểm tín hiệu đã lọc `exp`. Kết quả vào `results/T-076/kiem-tach/`.

**Pha 3: merge và bật**

8. **Merge với agent tắt.** Trước khi merge: ghi digest đang chạy của từng service (A) và xác nhận với người vận hành `rollback` về A dùng được. Minh merge PR vào giờ đã chọn; CD triển khai image mới (B), agent tắt (chưa có khóa `OTEL_AGENT_ENABLED`). Kiểm: pod Ready, 0 OOM/restart, đo nền C5 (kiểm hành trình ngắn). Lỗi do B → `rollback` về A **trong pha này** (sau bước 9 không còn được). Minh quyết giữ B trước khi sang bước 9.
9. **Bật agent qua CD, từng service** (không dùng nhóm `k8s`/`all`), khi Minh duyệt và đã chấp nhận giới hạn Q10: thêm `OTEL_AGENT_ENABLED=true` và `OTEL_EXPORTER_OTLP_HEADERS` vào bản đầy đủ của `ENV_<SVC>`, chạy CD `restart` cho đúng service đó; kiểm ngắn rồi sang service kế. Kiểm C5 trong 60 phút sau service cuối; kiểm C7 trên dashboard mới. Vượt ngưỡng: bỏ hai khóa khỏi bản đầy đủ `ENV_<SVC>`, CD `restart` (B tắt agent); không dùng `rollback` ở pha này.

**Pha 4 (tùy chọn, Minh duyệt riêng): bản ghim thử nghiệm mới trên exp-app**

10. Build "main mới nhất + PR #17 mới" ARM trên exp-app bằng `build.sh` (profile `rca-test`), triển khai bằng `deploy.sh`, kiểm tín hiệu như Q4 của T-070, ghi bản ghim mới. Kiểm trước phụ thuộc Compose/Keycloak theo bảng C1. Đổi bản là đổi hệ thống được đo: kết quả RCA trước và sau không so thẳng với nhau.

## Kiểm đúng đắn

- **Không đổi phương pháp và đường dữ liệu vào RCA:** `src/m1`, `src/m1_ft`, `src/p3`, bản chụp `b0f79a4d…`, gateway, Prometheus, luật cảnh báo, `rca/` không đổi. Hồi quy V082 hai ca trùng byte sau bước 6–7.
- **Không trộn dữ liệu:** phép kiểm cửa sổ trộn ở bước 7, cho cả hai bộ đóng gói và luật.
- **Không lộ bí mật:** khóa riêng TLS và token không vào git (`git grep` trước mỗi commit); token chỉ ở `ENV_<SVC>` và `/etc/flashticket-rca/production/`.
- **Dữ liệu gửi đi sạch:** sentinel giả không có trong payload thô của agent trước mọi lớp lọc Collector (bước 4), và không có trong bản ghi nhận được (bước 6, lớp dự phòng).
- **Truy vấn Tempo làm bằng chứng thực nghiệm** lọc `exp`; dashboard chạy thật lọc `production`.
- **Thay đổi trên main của nhóm đúng nghĩa:** bảng C1, diff 3 file Java xung đột, CI xanh.

## Tiêu chí xong

1. PR #17 (một PR duy nhất) nằm trên main mới nhất, không xung đột, CI xanh, đã qua phản biện Codex và Minh đọc. Mô tả PR có bảng giữ / bỏ và cách bật/tắt/hoàn tác qua CD.
2. Đường thu riêng nhận dữ liệu qua TLS + token; sai token bị từ chối; payload thô của agent đã sạch ở nguồn (bước 4).
3. Dữ liệu `production` không vào Prometheus thực nghiệm, file `capture`, gói ca RCA, kết quả bộ kiểm tín hiệu, và không đổi trạng thái luật cảnh báo. Hồi quy V082 trùng byte.
4. Sau khi bật: máy 84 gửi trace và metric về đường riêng; dashboard bản chạy thật hiện được (C7); đạt ngưỡng C5 đã duyệt trong 60 phút.
5. Phần không đạt trong task (log máy 84, trace `discovery-server`) ghi rõ là thiếu phủ, kèm điều kiện mở.
6. Pha 4 chỉ tính vào tiêu chí xong nếu Minh duyệt làm.

## Không làm

- Không merge PR, không đẩy vào `main`, không vào máy 84 sửa tay.
- Không đổi phương pháp RCA, không chạy RCA trên dữ liệu máy 84.
- Không bật log máy 84 trong task này (trừ khi Minh đổi Q1).
- Không sửa script CD chung của nhóm.
- Không đụng frontend, keycloak-spi, trừ khi xung đột buộc phải đụng.

## Chi phí ước lượng

| Pha | Ước lượng |
|---|---|
| 1 | 1–2 phiên; build Maven trên laptop vài lần (chưa đo); build image hai service |
| 2 | 1 phiên; obs thêm 2 container (RAM còn ~10 GB), không dừng thành phần cũ |
| 3 | Theo giờ merge Minh chọn; 2 lần theo dõi (sau merge, sau bật), mỗi lần 60 phút |

Không có lượt chạy dài hơn 1 giờ ngoài việc theo dõi; không tải hơn 5 GB.

## Rủi ro và điều chưa chắc

- **Merge là triển khai ngay** (CD tự chạy). Giảm rủi ro: agent tắt lúc merge, CI, phản biện, chọn giờ merge, `rollback` digest.
- **Bộ nhớ (chưa kiểm):** agent có thể đẩy pod vượt giới hạn (booking 768 MiB). Đo lúc khởi động ở bước 4; đo thật ở bước 9. Cần nâng giới hạn thì là thay đổi trong cùng PR, trình Minh trước.
- **Header và CA qua biến môi trường (chưa kiểm):** kiểm ở bước 4.
- **`ENV_<SVC>` bị ghi thay toàn bộ:** sửa thiếu khóa cũ làm hỏng service. Chỉ sửa khi có bản đầy đủ (Q9).
- **Dung lượng obs:** trace 100% từ máy chạy thật làm tăng Tempo. Đặt tỷ lệ lấy mẫu ban đầu (Q8) và theo dõi đĩa sau bước 9.
- **IP ra Internet của máy 84:** chưa biết; cần cho tường lửa. Không có thì không bật.
- **Kiểm hành trình ngắn** không đại diện tải thật; overhead thật vẫn OPEN sau task.

## Quyết định cần Minh khi duyệt SPEC

| Mã | Câu hỏi | Đề xuất |
|---|---|---|
| Q1 | Log của máy 84 | (c) Lần đầu chỉ trace và metric; log sau, có kiểm schema B16 |
| Q2 | assistant-service | (a) Chỉ thêm agent, ngoài danh sách B16 |
| Q3 | Build đa kiến trúc | Giữ hai kiến trúc của CD main; bỏ phần đa kiến trúc của PR; giữ truyền `SERVICE_VERSION` |
| Q4 | Bảo mật và tách đường | Collector + Prometheus riêng cho máy 84; HTTPS CA tự ký + token; chỉ mở cho IP máy 84 |
| Q5 | Ngoại lệ `AGENTS.md` §12 | Chữ ở mục "Phạm vi ghi" |
| Q6 | Pha 4 | Làm sau pha 3, duyệt riêng |
| Q7 | Ngưỡng C5 | p95 phía client sau ≤ 1,3 × trước, lỗi không tăng, 0 OOM/restart trong 60 phút; kịch bản kiểm hành trình ngắn (GET công khai) |
| Q8 | Tỷ lệ lấy mẫu trace ban đầu cho máy 84 | 10% (`parentbased_traceidratio`), tăng sau khi xem dung lượng |
| Q9 | Ai giữ bản đầy đủ `ENV_<SVC>` | Minh hoặc nhóm hệ thống cung cấp trước bước 9; không có thì dừng ở bước 8 (agent tắt) |
| Q10 | Chấp nhận: sau khi bật agent, CD không quay về image trước merge (chỉ tắt agent được) | Chấp nhận, vì bước 8 có cửa sổ để quay về trước khi bật; nếu không chấp nhận, cần nhóm hệ thống chỉ ra đường CD khác trước bước 9 |
| — | IP ra Internet của máy 84 | Minh cung cấp |

## Prompt bàn giao

Prompt cho Codex soát bản 3 nằm ở cuối `LOG.md` của task này.
