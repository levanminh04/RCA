# T-076 — Làm lại PR #17 trên main mới nhất, bật OTel agent cho FlashTicket chạy thật (máy 84)

- **Trạng thái:** đề xuất (Minh cho viết SPEC 26/11/2026; chờ duyệt SPEC)
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
- Bật agent cho bản chạy thật trên K8s (máy 84), gửi dữ liệu về máy quan sát exp-obs.

**Task không đánh giá phương pháp RCA** và không đổi phương pháp. Đạt task này cho:
- (a) FlashTicket chạy thật có trace và metric (log tùy Q1) trên Grafana;
- (b) một nhánh "main mới nhất + quan sát" để sau này ghim lại bản thử nghiệm trên exp-app.

Task không cho kết luận nào về chất lượng RCA trên bản chạy thật.

## Hiện trạng đã kiểm (26/11/2026, chỉ đọc)

| Điều | Thực tế | Nguồn |
|---|---|---|
| Repo FlashTicket trên laptop | Nhánh `rca/exp-2026-11` @`36a3725` = main `640dbaf` (18/11) + PR #17 `bb84d64` | `git log` |
| Main trên GitHub | `f178870` (22/11), hơn `640dbaf` **52 commit / 171 file** (chủ yếu assistant, frontend) | `gh api compare` |
| PR #17 (`rca/quan-sat-log`) | OPEN, CONFLICTING; đi trước main 10 commit, **tụt 92**; sửa 124 file (+5.028/−214) | `gh pr view 17`; `git diff --stat` |
| Xung đột với main | 13 file: 7 Dockerfile; `OrderServiceImpl`, `PromotionServiceImpl`, `RefundServiceImpl`; `payment-service/.env.example`; `deploy/app/{README.md,payment-service.yml}` | `git merge-tree --write-tree origin/main origin/rca/quan-sat-log` |
| Triển khai trên main | 10/10 service `runtime: k8s` (`.github/services.json`); Compose chỉ còn là đường dự phòng. CD (`cd.yml`, `_deploy-service.yml`) chạy khi push vào `main`: build image, SSH vào máy 84 rồi triển khai. Cấu hình ở `deploy/k8s/<svc>/configmap.yaml`, bí mật ở GitHub Secrets `ENV_<SVC>` | main `f178870` |
| Agent trên main | **Không có.** Dockerfile chỉ có `JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC"` | `services/booking-service/Dockerfile` @main |
| Agent trong PR #17 | Agent 2.33.1 (tải theo checksum) và `docker-entrypoint.sh`, mặc định `OTEL_AGENT_ENABLED=false`. Khi bật thì **`OTEL_LOGS_EXPORTER=none`**: agent gửi trace, metric, **không gửi log** | `docker-entrypoint.sh` @`bb84d64` |
| Thu log trên exp-app | Collector agent đọc file log Docker (filelog) → gateway → Loki. Máy 84 không có thành phần tương tự | lab `observability/collector/agent-docker-host.yaml` |
| PR #17 chưa có | `deploy/k8s` (agent không bật được trên 84); `assistant-service` (service Java mới trên main) | `git diff` |
| Máy quan sát | Gateway OTLP chỉ nghe `10.0.0.215:4317/4318` (IP nội bộ Oracle); iptables chỉ nhận `10.0.0.0/24` và SSH. Máy 84 dùng hạ tầng dải `172.31.x` (AWS), nên dữ liệu đi qua Internet giữa hai nhà cung cấp | lab `gateway.yaml`; `results/T-070/kiem-ke/` |
| RCA đọc dữ liệu | Bước chụp dữ liệu (`stage_m1.py`, `stage_b.py`) đọc **file ghi vòng của gateway** (`/srv/flashticket-rca/collector/capture`), không lọc theo môi trường. Luật cảnh báo lọc theo `service_name`, không theo môi trường | lab `rca/lib/stage_m1.py`, `alerting/rules.yaml` |

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Lựa chọn và giải thích khác | Phép kiểm, bằng chứng | Phần còn mở |
|---|---|---|---|
| **C1.** Phần nào của PR #17 còn cần, phần nào lỗi thời so với main K8s? | Giữ: log B16, kiểm log trong CI, agent và entrypoint, hook `rca-test`. Xét từng file: sửa Compose (`deploy/app/*`, `.env.example`, `docker-compose.postgresql.yml`, `deploy/postgres`), sửa CI/CD thời Compose, build đa kiến trúc, `decision-register.md` | Bước 1: bảng từng file (giữ / bỏ / sửa), mỗi dòng có lý do và đối chiếu main. Minh duyệt bảng | Có thể có phần exp-app còn dùng: đối chiếu với file phủ ở lab `test-environment/overrides` |
| **C2.** Lấy log của máy 84 thế nào? (Q1) | (a) Thêm biến cho entrypoint: `OTEL_LOGS_EXPORTER=otlp` khi bật trên K8s, giữ `none` trên exp-app để không thu trùng. (b) Collector dạng DaemonSet trên K3s đọc log pod. (c) Chỉ lấy trace và metric | (a): log tới Loki đủ 13 trường B16, có `traceId`/`spanId`. **Chưa kiểm**: bản ghi log OTLP có giữ trường `outcome` và cấu trúc như log JSON không | Ảnh hưởng việc chạy H8 (kênh log) trên dữ liệu máy 84 về sau |
| **C3.** Bảo mật đường gửi từ máy 84 tới máy quan sát (Q4) | (a) TLS với CA tự ký (CA công khai để trong repo) + token bearer trên gateway, cổng riêng, chỉ mở cho IP máy 84. (b) TLS bằng chứng chỉ Let's Encrypt (cần tên miền). (c) Chỉ chặn theo IP, không TLS | Gửi thử từ ngoài: có token đạt, sai token bị từ chối, không TLS bị từ chối. iptables và Security List chỉ mở cho IP máy 84 | Cần IP ra Internet của máy 84 (Minh cung cấp hoặc đọc qua CD) |
| **C4.** Dữ liệu máy 84 có làm bẩn thực nghiệm RCA trên exp-app không? | Phải tách: (i) bước chụp dữ liệu chỉ lấy `deployment.environment` của exp-app; (ii) luật cảnh báo và dashboard thực nghiệm lọc theo môi trường | Trên một cửa sổ có cả hai nguồn: gói ca chỉ có span của exp-app; luật cảnh báo không cháy vì dữ liệu máy 84; hồi quy V082 hai ca vẫn trùng byte | Nhãn môi trường hiện tại của exp-app: đọc ở bước 0 |
| **C5.** Agent có làm hỏng hệ thống chạy thật không? | Agent tốn thêm bộ nhớ; giới hạn K8s hiện ví dụ booking 768 MiB. Thêm nữa: log đổi sang JSON, 39 file nghiệp vụ được chèn lệnh ghi log | Sau khi triển khai: pod Ready, 0 OOM, 0 restart trong một khoảng theo dõi khai trước; p95 của gateway không xấu đi quá ngưỡng khai trước. Đọc từng dòng 39 file nghiệp vụ | Mức tăng bộ nhớ thật trên K8s: đo sau triển khai |
| **C6.** `assistant-service` (Q2) | (a) Chỉ thêm agent vào Dockerfile. (b) Agent + log B16. (c) Không đụng | (a): có trace của assistant trong Tempo | Log B16 cho assistant: để sau nếu Minh cần |

## Đầu vào

- Repo FlashTicket `D:/Project/flash-ticket-platform`: `origin/main` @`f178870`, `origin/rca/quan-sat-log` @`bb84d64`, `origin/rca/exp-2026-11` @`36a3725`.
- Repo lab `D:/Project/flashticket-rca-lab` @`85ace52`.
- Chuẩn B16: `docs/architecture/B16-observability-baseline.md` (repo FlashTicket).
- Kết quả T-067 (bản ghim, kiểm tín hiệu), T-070 (đợt dọn, Q4), T-072 (luật cảnh báo).
- Đọc máy bằng `results/T-070/kiem-ke/tho/lenh/ssh.sh`, chỉ lệnh đọc, trừ các bước ghi đã duyệt ở dưới.
- **Không** đọc dữ liệu khóa. **Không** vào máy 84 bằng tay; mọi thay đổi trên máy 84 đi qua CD của nhóm.

## Đầu ra

- **PR #17 làm lại** trên `main` mới nhất: nhánh `rca/quan-sat-log` được dựng lại và đẩy đè (force-push), PR cũ tự cập nhật. Mô tả PR ghi phần giữ, phần bỏ và lý do, cách bật agent, cách hoàn tác.
- `results/T-076/bang-file-pr17.md`: bảng giữ / bỏ / sửa từng file của PR (C1).
- `results/T-076/kiem-cuc-bo/`: kết quả build và test cục bộ (CI tương đương), kiểm entrypoint, render manifest K8s.
- **Commit repo lab:** cổng OTLP có TLS và token trên gateway; tách dữ liệu theo môi trường cho bước chụp dữ liệu, luật cảnh báo và dashboard (C4); script tường lửa; tài liệu.
- `results/T-076/kiem-sau-trien-khai/`: kiểm theo C3, C4, C5 sau khi merge.
- (Pha 4, nếu Minh duyệt riêng) `results/T-076/ban-ghim-moi/`: bản ghim thử nghiệm mới trên exp-app.

## Phạm vi ghi

Ngoài `LOG.md` của task và dòng T-076 trong `docs/STATE.md`:
- `results/T-076/`.
- **Repo FlashTicket:** chỉ nhánh `rca/quan-sat-log` (PR #17), kể cả force-push nhánh này. **Không** đẩy vào `main`, không đụng nhánh khác. Merge PR là việc của Minh.
  - Cần thêm ngoại lệ vào `AGENTS.md` §12. Đề xuất chữ: "Riêng nhánh `rca/quan-sat-log` (PR #17) được sửa khi Minh duyệt; không đẩy thẳng vào `main`."
  - Minh duyệt chữ cùng lúc duyệt SPEC.
- **Repo lab:** `observability/collector/gateway.yaml`, `observability/compose.yaml`, `observability/grafana/provisioning/alerting/rules.yaml`, `observability/grafana/dashboards/*`, `observability/grafana/build_dashboards.py`, `rca/lib/stage_m1.py`, `rca/online/stage_b.py` (chỉ phần lọc môi trường), thư mục mới `observability/tls/` (CA công khai, script tạo chứng chỉ; **không** đưa khóa riêng vào git), `inventory/`, `docs/`.
  - Thay đổi ở `stage_m1.py` và `stage_b.py` chạm đường dữ liệu vào phương pháp. Phải qua phép kiểm C4 (hồi quy, gói ca) trước khi dùng.
- **Máy obs:** chỉ bộ quan sát (compose, iptables), theo bước 5 đã duyệt; chứng chỉ và token để ở `/etc/flashticket-rca/`.
- **GitHub Secrets** của repo FlashTicket: thêm token OTLP vào `ENV_<SVC>` bằng `gh secret set`, có Minh duyệt riêng lúc làm.
- **Ngoài quyền của agent, Minh tự làm:** Security List trên Oracle, merge PR, báo nhóm hệ thống.

## Các bước

**Pha 1: PR (chưa đụng máy)**
1. **Kiểm kê C1** — bảng từng file của PR so với main `f178870` và với file phủ ở lab. Minh duyệt bảng. Kiểm bằng: mỗi file "bỏ" có lý do; mỗi file "giữ" còn cần trên main.
2. **Dựng lại nhánh.** Tạo nhánh tạm từ `origin/main`, áp phần giữ thành vài commit theo chủ đề (log B16, CI kiểm log, agent và entrypoint, hook `rca-test`, K8s, assistant). Gỡ 13 xung đột theo code mới của main; với 3 file Java, giữ logic nghiệp vụ của main, chỉ chèn lệnh ghi log. Kiểm bằng: `git diff origin/main` chỉ gồm các nhóm trên.
3. **Thêm K8s.** Trong `deploy/k8s/<svc>/configmap.yaml` của các service Java: `OTEL_AGENT_ENABLED`, `ENVIRONMENT=production`, `HOST_ID`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_CERTIFICATE`, biến log theo Q1. Trong deployment: mount CA công khai. Token để ở secret `ENV_<SVC>`. Kiểm bằng: script kiểm K8s có sẵn của nhóm (`.github/scripts/test-k8s-*.py`), render manifest.
4. **Kiểm cục bộ:**
   - `mvnw verify` các service bị đổi, kể cả bước kiểm log B16, `-P rca-test` cho Booking và Event;
   - build image amd64 một service;
   - chạy entrypoint với agent bật và tắt.

   Kết quả vào `results/T-076/kiem-cuc-bo/`.

   **Sau đó:** force-push `rca/quan-sat-log`, CI trên GitHub chạy. **Chưa merge.**
5. **Phản biện.** Codex soát PR theo prompt (khối Soát kết quả). Minh đọc theo hướng dẫn review (danh sách chỗ cần đọc kỹ, gồm 39 file nghiệp vụ).

**Pha 2: máy quan sát sẵn sàng (trước khi merge)**

6. **Gateway nhận từ ngoài.** Thêm cổng OTLP có TLS và token bearer, chỉ cho IP máy 84. Cổng nội bộ cũ giữ nguyên để không đổi đường thu của exp-app (bất biến B7 ở T-070). iptables qua script trong lab. Minh mở Security List. Kiểm bằng: gửi span thử từ ngoài (từ máy tải) với token đúng, token sai, không TLS.
7. **Tách môi trường (C4):**
   - bước chụp dữ liệu và luật cảnh báo chỉ lấy dữ liệu của exp-app;
   - dashboard có biến chọn môi trường.

   Kiểm bằng:
   - hồi quy V082 trên 2 ca trùng byte như T-070;
   - phát lại một ca dev trùng;
   - gửi span thử gắn nhãn `production`: không vào file chụp, không làm luật nào cháy.

**Pha 3: bật trên máy 84**

8. **Lưu token** vào `ENV_<SVC>` (Minh duyệt lúc làm). Báo nhóm hệ thống. Minh merge PR vào giờ đã chọn. CD tự triển khai.
9. **Kiểm sau triển khai (C5):**
   - pod Ready, 0 OOM, 0 restart trong 1 giờ;
   - Tempo có trace, Prometheus có metric của `deployment.environment=production`, Loki có log nếu theo Q1(a);
   - exp-app và RCA không bị ảnh hưởng (như bước 7).

   **Hoàn tác** nếu hỏng: đặt `OTEL_AGENT_ENABLED: 'false'` qua PR, hoặc rollback digest qua CD (`cd.yml` có `rollback`).

**Pha 4 (tùy chọn, Minh duyệt riêng): bản ghim thử nghiệm mới trên exp-app**

10. Build "main mới nhất + PR #17 mới" trên exp-app, triển khai bằng `deploy.sh`, kiểm tín hiệu như Q4 của T-070, ghi bản ghim mới. Đổi bản là đổi hệ thống được đo: kết quả RCA trước và sau không so thẳng với nhau.

## Kiểm đúng đắn

- **Không đổi phương pháp:** `src/m1`, `src/m1_ft`, `src/p3` và bản chụp `b0f79a4d…` không đụng. Hồi quy V082 hai ca trùng byte sau mọi thay đổi ở lab (bước 7).
- **Không đổi đường thu của exp-app:** cấu hình Collector agent không đổi. Cổng nội bộ của gateway không đổi. Kiểm tín hiệu như Q4 sau bước 6–7, và sau pha 4 nếu làm.
- **Không lọt dữ liệu chạy thật vào gói ca:** phép kiểm span thử gắn nhãn `production` (bước 7).
- **Không lộ bí mật:** khóa riêng TLS và token không vào git; kiểm bằng `git grep` trước mỗi commit.
- **Thay đổi trên main của nhóm có đúng nghĩa không:** bảng C1 và diff của 3 file Java xung đột đối chiếu với code mới của main; CI xanh.

## Tiêu chí xong

1. PR #17 (một PR duy nhất) nằm trên main mới nhất, không xung đột, CI xanh, đã qua phản biện Codex và Minh đọc. Mô tả PR có bảng giữ / bỏ.
2. Máy quan sát nhận được dữ liệu từ ngoài qua TLS và token; sai token bị từ chối.
3. Dữ liệu của máy 84 không vào gói ca RCA và không làm cháy luật cảnh báo của thực nghiệm. Hồi quy V082 trùng byte.
4. Sau khi Minh merge: máy 84 gửi trace và metric (log theo Q1) về máy quan sát; hệ thống chạy thật không OOM, không restart trong 1 giờ.
5. Pha 4 chỉ tính vào tiêu chí xong nếu Minh duyệt làm.

## Không làm

- Không merge PR, không đẩy vào `main`, không vào máy 84 sửa tay.
- Không đổi phương pháp RCA, không chạy RCA trên dữ liệu máy 84.
- Không thêm log B16 cho assistant-service, trừ khi Minh chọn Q2(b).
- Không đụng frontend, keycloak-spi, trừ khi xung đột buộc phải đụng.

## Chi phí ước lượng

| Pha | Ước lượng |
|---|---|
| 1 | 1–2 phiên; build Maven trên laptop vài lần (mỗi lần cỡ vài phút tới chục phút, chưa đo) |
| 2 | 1 phiên; gateway và Grafana trên obs dừng vài phút |
| 3 | Theo giờ merge Minh chọn; 1 giờ theo dõi |

Không có lượt chạy dài hơn 1 giờ ngoài việc theo dõi; không tải hơn 5 GB.

## Rủi ro và điều chưa chắc

- **Merge là triển khai ngay** (CD tự chạy). Lỗi trong PR ảnh hưởng hệ thống thật của nhóm. Giảm rủi ro: CI, phản biện, chọn giờ merge, đường hoàn tác qua CD.
- **Bộ nhớ (chưa kiểm):** agent có thể đẩy pod vượt giới hạn K8s, ví dụ booking 768 MiB, gây OOM. Kiểm ở bước 9. Nếu cần nâng giới hạn thì là thay đổi trong cùng PR, trình Minh trước.
- **Log qua OTLP (chưa kiểm):** có giữ đủ trường B16 và `outcome` không (C2). Kiểm ở bước 4 hoặc 6 trước khi chọn Q1(a) làm mặc định.
- **Dung lượng obs:** lấy mẫu trace 100% từ máy chạy thật làm tăng dữ liệu Tempo và Loki. Đĩa obs hiện dùng 44%. Theo dõi sau bước 9; tỷ lệ lấy mẫu là quyết định của Minh nếu cần.
- **Thay đổi ở `stage_*.py`** chạm đường dữ liệu vào phương pháp. Bắt buộc hồi quy (bước 7) trước khi dùng cho thực nghiệm.
- **IP ra Internet của máy 84:** chưa biết. Cần cho tường lửa.

## Quyết định cần Minh khi duyệt SPEC

| Mã | Câu hỏi | Đề xuất |
|---|---|---|
| Q1 | Log của máy 84 | (a) Agent gửi log qua OTLP trên K8s, exp-app giữ như cũ. Kiểm trường B16 trước |
| Q2 | assistant-service | (a) Chỉ thêm agent |
| Q3 | Build đa kiến trúc trong PR | Bỏ: CD của main build amd64; exp-app tự build ARM bằng `build.sh` |
| Q4 | Bảo mật đường gửi | (a) TLS với CA tự ký + token, cổng riêng, chỉ mở cho IP máy 84 |
| Q5 | Ngoại lệ `AGENTS.md` §12 | Chữ ở mục "Phạm vi ghi" |
| Q6 | Pha 4 (bản ghim thử nghiệm mới) | Làm sau pha 3, duyệt riêng |

## Prompt bàn giao

Prompt cho Codex soát SPEC nằm ở cuối `LOG.md` của task này (phiên 1).
