# T-058 — Bàn giao lượt chạy qua đêm (viết 11/11/2026)

File này để agent (Claude hoặc Codex) làm tiếp mà không bỏ sót gì, kể cả khi ngữ cảnh bị nén hoặc đổi phiên. Đọc cùng: `AGENTS.md`, `tasks/T-058-ha-tang-rca-ban-dau/SPEC.md` và `LOG.md`, `results/T-058/thay-doi-ha-tang-2026-11-11.md`, `docs/techstack/PLAN-TRIEN-KHAI.md`, `docs/techstack/TECHSTACK-NGHIEN-CUU.md`.

## 0. Trạng thái duyệt (đọc trước)

Lượt chạy đêm **chỉ bắt đầu khi Minh trả lời "duyệt" cho gói quyền ở mục 2**. Chưa có câu duyệt đó tính tới lúc viết file này. Không có câu duyệt thì chỉ được đọc, không cài, không push, không chạy container.

## 1. Mục tiêu

Sáng hôm sau Minh muốn thấy:
1. FlashTicket (8 service + 4 hạ tầng) chạy trên `exp-app`.
2. Kho quan sát (Collector, Prometheus, Loki, Tempo, Grafana) chạy trên `exp-obs`, thấy trace, log, metric của FlashTicket.
3. Gây được một lỗi thử và thấy nó trên Grafana. M1 ra xếp hạng trên dữ liệu thật là mục tiêu thêm, **không hứa**.
4. Tài liệu `huong-dan-trien-khai.md` (mục 6) đủ để Minh tự làm lại.

Đây là cài đặt và kiểm khả thi (SPEC T-058), **không phải đánh giá**. Không rút kết luận về hiệu quả M1.

## 2. Gói quyền cần Minh duyệt

| # | Quyền | Ghi chú |
|---|---|---|
| 1 | Đính chính SPEC: hạ tầng là hai máy Oracle ARM (thay AWS x86) | SPEC hiện ghi "đổi lên `m7i-flex.large`" |
| 2 | Cài Docker, JDK 21; mở `iptables` nội bộ; chạy container trên `exp-app` và `exp-obs` | Không cài gì lên máy 84 |
| 3 | Repo FlashTicket: tạo **nhánh** `ci/arm64`, thêm file workflow mới, push nhánh. **Không đụng `main`** | SPEC đang ghi "Không sửa repo FlashTicket"; AGENTS §12 ghi chỉ đọc |
| 4 | Máy 84, **chỉ đọc**: lấy digest, nhãn image, file env, `pg_dump`, `mongodump` | Env chép thẳng 84 → `exp-app`, không in ra chat, không ghi vào repo |
| 5 | Dùng cách build ARM ngay trên `exp-app` (`mvnw -DskipTests`) làm lưới an toàn | Khác CI ở chỗ không chạy test |
| 6 | Lượt dài khoảng 6–8 giờ (luật 8, 21) | Không tải gì về laptop ngoài gói kết quả nhỏ |

Minh đã nói "chọn cách B" (sửa CD thành đa kiến trúc) và "levanminh04 có quyền bypass main". Agent **không** push `main` khi chưa có câu duyệt riêng cho việc đó. Lý do: push `main` chạy CD của cả nhóm, và việc sửa file workflow trên `main` **không tự build gì** (xem mục 4.2).

## 3. Máy và cách vào

| Vai trò | IP công khai | IP nội bộ | Cấu hình | Khóa |
|---|---|---|---|---|
| `exp-app` (Oracle) | `129.221.208.47` | `10.0.0.158` | A1 ARM, 2 OCPU, 11 GB, đĩa 50 GB, Ubuntu 24.04.5, `ap-singapore-1` | `D:\RCA-ext\keys\exp-app\ssh-key-2026-11-10 (1).key` |
| `exp-obs` (Oracle) | `213.35.116.128` | `10.0.0.215` | A1 ARM, 2 OCPU, 11 GB, đĩa 150 GB, Ubuntu 24.04.5, `ap-singapore-1` | `D:\RCA-ext\keys\exp-obs\ssh-key-2026-11-10.key` |
| Máy 84 (nhóm) | `52.64.237.84` | — | x86, 3,7 GiB RAM | `D:\RCA-ext\keys\FlashTicket-Control-Diagnosis.ppk`, **chỉ đọc**, cách vào ở `docs/STATE.md` |
| AWS `exp-app` cũ | `3.24.8.49` | `172.31.2.212` | `m7i-flex.large` x86, 8 GiB | `D:\RCA-ext\keys\Hahaa123.pem`. Minh nói không dùng AWS nữa; máy còn đó, chưa quyết xóa |

Lệnh vào từ laptop (Git Bash). Host key lưu vào file riêng, không ghi đè `known_hosts` của Minh:

```bash
ssh -i "D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key" -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$SCRATCH/kh_exp-obs" ubuntu@213.35.116.128
```

Quy tắc: không in nội dung file khóa, không chép khóa vào repo, không đưa khóa vào prompt hay LOG.

## 4. Kế hoạch từng chặng

Mỗi chặng ghi LOG ngay khi xong (giờ, kết quả, file). Lệnh nào **chạy thành công** thì chép vào `huong-dan-trien-khai.md` (mục 6); lệnh hỏng chỉ ghi ở LOG.

### 4.0 Việc của Minh trước khi đi ngủ (Oracle web)
- Networking → Virtual cloud networks → `exp-vcn` → Security Lists → Default Security List → Add Ingress Rules: Source CIDR `10.0.0.0/24`, IP Protocol **All Protocols**.
- Không mở cổng nào ra internet. Xem Grafana và gọi gateway qua đường hầm SSH (MobaXterm → Tunneling).
- Phương án nếu Minh quên quy tắc trên: đường hầm SSH giữa hai máy (cổng 22 đã thông, đã đo trung vị 1 ms).
- Laptop: cắm sạc, tắt chế độ ngủ; phiên Claude ở chế độ tự chấp nhận lệnh.

### 4.1 Chặng 1 — Docker và mạng nội bộ (cả hai máy)
- `sudo apt update && sudo apt upgrade -y`, rồi `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`, `sudo usermod -aG docker $USER` (đăng nhập lại).
- Ghi phiên bản Docker và Compose. Compose phải từ 2.30 trở lên (file RabbitMQ của nhóm dùng `post_start`).
- Mở nội bộ trên `iptables` (chuỗi `INPUT` ban đầu: cho phép phiên đã có, ICMP, loopback, cổng 22, rồi REJECT): chèn quy tắc `-s 10.0.0.0/24 -j ACCEPT` **trước** dòng REJECT. Lưu lại cho khởi động sau; cách lưu chưa kiểm trên image này, kiểm khi làm.
- Xong khi: `docker run --rm hello-world` chạy; `exp-app` kết nối được `10.0.0.215:4317` sau khi Collector chạy.
- Không tạo swap (xem mục 7).

### 4.2 Chặng 2 — Image ARM cho 8 service
Hai nguồn, theo thứ tự ưu tiên. Hết hạn mức 2 giờ mà chưa có image ARM thì dùng nguồn B, không chờ.

**Nguồn A — CI của GitHub.**
- Tên 8 service: `discovery-server`, `api-gateway`, `user-service`, `event-service`, `ticket-service`, `booking-service`, `payment-service`, `keycloak`. **Bỏ `frontend`** (gắn cứng địa chỉ 84).
- Digest trên 84 đã đổi sau khi tôi lưu `manifest-digest.json` (CD chạy lúc 15:01Z và 19:04Z ngày 10/11; `api-gateway`, `event-service`, `user-service` có digest mới). **Đọc lại** `/opt/flash-ticket-app/state/<svc>.current` trên 84 và đọc nhãn `org.opencontainers.image.revision` trong cấu hình của từng image (lấy qua API registry của GHCR, ẩn danh được). Mỗi service có một commit riêng.
- Workflow mới `.github/workflows/build-arm64.yml` trên nhánh `ci/arm64`, kích hoạt khi **push lên nhánh** (không cần bấm tay, không cần token): với mỗi service, `actions/checkout` ở đúng commit đã đọc, build JAR (`./mvnw -B -ntp verify` như CI hoặc `-DskipTests`; ghi rõ cách nào), build image `linux/arm64`, đẩy lên GHCR với tag `arm64-<commit>` (`provenance: false`). **Không deploy gì lên 84.** Danh sách commit để trong file `ci/arm64-revisions.json` của nhánh.
- Cách này không phải cách B Minh chọn. Cách B (sửa `_deploy-service.yml` thêm `linux/arm64` và bước QEMU) giữ làm PR riêng cho Minh. Lý do không dùng B cho lượt đêm: merge file workflow vào `main` **không build gì**, vì `detect-changes.sh` chỉ tính file nằm trong thư mục service hoặc `deploy/app/`; muốn chạy phải `workflow_dispatch` (cần token hoặc Minh bấm) hoặc đẩy thay đổi vào thư mục service (chạy CD và deploy lên 84 của nhóm).
- Chưa kiểm: workflow này chạy được trên GitHub; Keycloak dưới QEMU (`RUN kc.sh build`) mất bao lâu.

**Nguồn B — build ngay trên `exp-app` ARM** (lưới an toàn):
- Cài JDK 21 (`sudo apt install -y openjdk-21-jdk-headless`), `git clone` repo FlashTicket, với mỗi service `git worktree add` đúng commit, `./mvnw -B -ntp -DskipTests package` rồi `docker build`. Keycloak: build JAR trong `services/keycloak-spi` bằng `mvn -B -ntp clean verify`, rồi `docker build` (Dockerfile của nó chạy `kc.sh build`).
- Image gắn tên cục bộ, ví dụ `ft-local/booking-service:arm64-<commit>`.

Xong khi: 8 image `arm64` có trên `exp-app` (`docker images`; `docker image inspect --format '{{.Architecture}}'` trả `arm64`). Service nào lỗi build thì ghi LOG, làm tiếp service khác.

### 4.3 Chặng 3 — Hạ tầng, env, dữ liệu, bật 8 service (`exp-app`)
- Thư mục giống 84: `sudo mkdir -p /opt/flash-ticket-app/{compose,env,state,secrets/ticket-qr}` và `/opt/flash-ticket-infra`, `chown` sang `ubuntu`.
- `git clone https://github.com/levanminh04/flash-ticket-platform.git`, ghim `1d40c97` (hoặc commit mới hơn; ghi rõ).
- **Env.** Đọc `/opt/flash-ticket-app/env/*.env` và `/opt/flash-ticket-infra/.env` trên 84 (chỉ đọc), chuyển thẳng sang `exp-app` bằng ống `ssh | ssh`, mode 600, **không in ra màn hình, không vào chat, LOG hay repo**. Vì cả 84 lẫn `exp-app` chạy kiểu một máy với `network_mode: host` và địa chỉ `127.0.0.1`, phần lớn biến giữ nguyên. Phải đổi:
  - `KC_HOSTNAME` của Keycloak thành địa chỉ `exp-app`; `KEYCLOAK_ISSUER_URI` của gateway phải khớp (nếu không, gateway từ chối token).
  - Payment: không chạy ngrok; `VNPAY_RETURN_URL`, `VNPAY_IPN_URL` trỏ giả (chưa có VNPay giả; luồng đặt vé dừng ở bước thanh toán).
  - `key-ring.json` của ticket (`/opt/flash-ticket-app/secrets/ticket-qr/`, owner 10001, mode 0440): chép từ 84 như env.
- **Hạ tầng.** Dùng `deploy/docker-compose.postgresql.yml`, `redis.yml`, `rabbitmq.yml`, `deploy/mongodb/` như nhóm (cần `.env` gốc trong repo ở `exp-app`). Postgres và MongoDB lấy dữ liệu bằng **một trong hai** cách (quyết lúc làm, ghi lý do vào LOG):
  - (a) `pg_dump` của từng database và `mongodump` từ 84 (chỉ đọc; làm lúc nhóm ít dùng, vì 84 chỉ còn khoảng 0,9 GiB RAM trống), rồi nạp vào `exp-app`. Mật khẩu role trong env phải giống 84.
  - (b) Khởi tạo trống bằng `00-business-databases.sh` (đã đọc: tạo database, role và schema, DDL ở `docs/architecture/data/postgres/*.sql`) và realm `deploy/keycloak/import/flash-ticket-realm.json` (5 người dùng, client `frontend`, `internal-service`). Chưa kiểm script này chạy được trọn vẹn.
- **Bật service.** Dùng `deploy/app/*.yml` và `deploy-service.sh` của nhóm hoặc `docker compose -f deploy/app/<svc>.yml -p flash-ticket-<svc> up -d` với `IMAGE=<ảnh arm64>`. Thứ tự: discovery-server, rồi các service khác, keycloak (cần network `flash-ticket-infra`). `deploy-service.sh` đòi token GHCR qua stdin và kiểm sức khỏe qua Eureka; nếu không chạy được thì dùng lệnh compose, ghi chỗ lệch.
- Xong khi: mọi service `UP` trong Eureka (`curl -s -H "Accept: application/json" http://127.0.0.1:8761/eureka/apps`); `docker ps` không có container restart; lấy được một token từ Keycloak và gọi được một API qua gateway (`127.0.0.1:8081`).

### 4.4 Chặng 4 — Agent, Collector, kho quan sát
- **`exp-obs`.** Dựng kho thử bằng `grafana/otel-lgtm:0.40.0` (một container: Collector + Prometheus + Loki + Tempo + Grafana) để có kết quả sớm. Bước sau thay bằng kho ghim riêng theo `TECHSTACK-NGHIEN-CUU.md` §5: Collector `0.165.0`, Prometheus `v3.16.0`, Loki `3.7.9`, Tempo `3.1.1`, Grafana `13.3.0`; cấu hình ở `infra/exp/obs/` trong repo RCA.
- **Agent.** Tải `opentelemetry-javaagent.jar` bản `v2.33.1` về `/opt/flash-ticket-app/otel/` trên `exp-app`; gắn vào mỗi service bằng cách thêm vào file env của service (không sửa image, không sửa code) các biến ở `TECHSTACK-NGHIEN-CUU.md` §6.1:
  `JAVA_TOOL_OPTIONS` (phải chép lại `-XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC` vì biến này **thay** giá trị trong image), `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`, `OTEL_TRACES_SAMPLER=parentbased_always_on`, `OTEL_LOGS_EXPORTER=none`, `OTEL_METRIC_EXPORT_INTERVAL`, và hai biến khóa `traceId`/`spanId`. Phải thêm bind mount `/opt/flash-ticket-app/otel:/otel:ro` vào compose của từng service (bản sao compose đặt riêng cho `exp-app`, **không sửa file trong repo**). Container chạy `read_only: true`, mount chỉ đọc là đủ.
- **Collector tại chỗ** (container riêng, `network_mode: host`, trên `exp-app`): nhận OTLP ở `127.0.0.1:4318`, đọc log container (`/var/lib/docker/containers`, cần root), `docker_stats` (Docker socket), `hostmetrics`, receiver DB; loại trừ container của công cụ tiêm lỗi và k6; xuất `otlp` sang `exp-obs:4317` với `retry_on_failure` và `sending_queue` có `storage` (hàng đợi lưu đĩa).
- Xong khi (bốn điều của `TECHSTACK-NGHIEN-CUU.md` §4.1 "Cách kiểm"): một request gateway → booking → PostgreSQL/Redis/RabbitMQ cho span có kind và `http.route`, có span JDBC, Redis, RabbitMQ; `traceId` trong log JSON trùng span; metric lên Prometheus; health UP, không restart. Thiếu tín hiệu nào thì ghi đúng tín hiệu đó, không bỏ.
- Chưa kiểm: agent `v2.33.1` với Spring Boot 4.1.1; tên biến `OTEL_INSTRUMENTATION_COMMON_LOGGING_*` (nếu agent không nhận thì dùng `-Dotel.instrumentation.common.logging.trace-id-key=traceId` trong `JAVA_TOOL_OPTIONS`); đường `/otlp` của Loki 3.7.9.

### 4.5 Chặng 5 — Tải nhẹ, một lỗi thử, M1
- Tải nhẹ cố định (tài liệu hóa lệnh); chạy 1 giờ rảnh và 1 giờ tải nhẹ để lấy số RAM, CPU, drop, GB mỗi giờ (SPEC C3).
- Một lỗi thử không cần sửa code: dừng một container bằng `docker pause`/`docker stop`. Ghi mốc vào sổ tiêm lỗi (PLAN §5; RCA không đọc sổ).
- Viết `src/m1/adapter_flashticket.py` (file mới, **không sửa** `src/m1/adapter.py`, vì có thể đang bị ghim trong manifest cũ) và chạy M1. Trước khi tin kết quả: kiểm quy ước dữ liệu nguồn (span gốc, đơn vị thời gian, alias tên service; SL39); trạng thái đồng loạt (toàn rỗng, toàn `NO_TARGET`) phải lần tới đầu vào (rule 12 của `docs/review-prompt.md`).
- Không đạt thì dừng ở chặng 4 và báo đúng phần thiếu.

### 4.6 Chặng 6 — Tài liệu và báo cáo
- Hoàn thiện `huong-dan-trien-khai.md`, `moi-truong.md`, `manifest-digest.json` (digest mới, commit, phiên bản), `so-do-tai-nguyen.json`, `kiem-agent.md`, `kiem-telemetry.md`, `bao-cao.md` theo SPEC mục "Đầu ra".
- Mục LOG kết thúc phiên theo `AGENTS.md` mục 7, cập nhật dòng T-058 trong `docs/STATE.md`, soạn prompt cho Codex theo `docs/review-prompt.md` (chép nguyên văn, chỉ điền thông tin trung tính).

## 5. Gặp lỗi giữa chừng (luật 21)

- Lỗi ở chặng nào chỉ chặn chặng đó và chặng phụ thuộc. Chặng 1 hỏng → cả đêm dừng, báo; chặng 2 một service lỗi → làm tiếp service khác; chặng 4 thiếu tín hiệu → ghi rõ và làm chặng 5 với tín hiệu có.
- Mỗi lần thử cùng một chỗ 3 lần không được thì dừng chỗ đó, ghi cái đã thử vào LOG và làm chỗ khác (AGENTS §5a).
- Hết hạn mức 2 giờ chờ CI (nguồn A): chuyển nguồn B, không chờ tiếp.
- Mọi lệnh dài chạy nền, ghi tiến độ và thời gian từng bước ngay từ đầu (SL25).
- Mọi số trong tài liệu lấy từ lệnh đã chạy, không viết từ trí nhớ (SL17). Điều chưa kiểm ghi "chưa kiểm" kèm lý do.

## 6. Tài liệu `results/T-058/huong-dan-trien-khai.md` (văn phong Minh)

Minh dùng MobaXterm, đã có ghi chú cho repo cũ. Viết theo đúng lối đó:
- Tiếng Việt, câu ngắn, có "tại sao".
- Chia mục đánh số: "1. SSH vào máy", "2. Cài Docker", ... Mỗi mục: khối lệnh, rồi giải thích **từng lệnh, từng tham số**:

```text
sudo usermod -aG docker $USER

Tác dụng: thêm tài khoản hiện tại vào nhóm docker.
sudo: chạy với quyền cao nhất (quản trị).
usermod -aG docker: thêm vào nhóm (group) tên docker, -a là thêm chứ không ghi đè nhóm cũ.
$USER: biến tự lấy tên đăng nhập (ở đây là ubuntu).
Sau lệnh này gõ exit rồi đăng nhập lại để quyền có hiệu lực. Nhờ vậy gõ docker không cần sudo.
```

- Mục đầu hướng dẫn MobaXterm: Session → SSH → Remote host (IP), tích Specify username (`ubuntu`), Advanced SSH settings → Use private key (chọn file khóa); và mục Tunneling để xem Grafana và gọi gateway từ laptop.
- Mục Collector: file cấu hình ở đâu, biến thêm vào file env của service, cách kiểm dữ liệu đã về (câu truy vấn, cổng, kết quả kỳ vọng).
- Cuối mỗi mục có "Kiểm: gõ ... thấy ...".
- **Chỉ ghi lệnh đã chạy thành công**, theo đúng thứ tự làm lại được. Lệnh thử hỏng không vào file này.
- Không ghi bí mật (mật khẩu, token, khóa). Chỗ cần bí mật ghi "lấy từ ... (Minh cấp)".
- Ghi kèm phiên bản và ngày để biết lúc nào lệnh còn đúng.

## 7. Điều không được làm

- Không sửa `main` của repo FlashTicket khi chưa có duyệt riêng; không sửa file ngoài `.github/workflows/build-arm64.yml` và `ci/arm64-revisions.json` trên nhánh `ci/arm64`.
- Không deploy hay sửa gì trên máy 84; chỉ lệnh đọc.
- Không tạo swap trên `exp-app` (swap che lỗi thiếu RAM và làm số đo nhiễu; PLAN §2.1). Nếu cần cho một phép đo ngắn thì tạo tạm, không ghi `fstab`.
- Không đọc `.env`, `~/.bash_history`, `~/.ssh` trên máy 84. Env của dịch vụ thì chỉ chuyển thẳng, không đọc nội dung.
- Không mở tập test hoặc dữ liệu khóa.
- Không đưa nhãn tiêm lỗi vào dữ liệu RCA nhận (luật cứng 6).
- Không tự gửi prompt sang agent khác; không commit khi Minh chưa duyệt (luật 11).

## 8. Điểm Minh chưa quyết hoặc chưa kiểm (không đoán)

- Tài khoản Oracle có bị giới hạn dịch vụ bằng 0 cho các shape x86 hay không (chỉ liên quan nếu quay lại x86).
- Còn boot volume của máy Oracle đầu tiên hay không (nếu còn, tổng đĩa vượt 200 GB miễn phí).
- Luật thu hồi máy rảnh của Oracle có áp dụng cho tenancy trả phí hay không; hai máy A1 cần có tải thực tế để không bị coi là rảnh.
- Hai máy A1 dùng 4 OCPU và 22 GB, sát hạn mức miễn phí 3000 OCPU-giờ và 18.000 GB-giờ mỗi tháng; không tạo thêm máy A1 thứ ba.
