# Techstack cho FlashTicket làm nguồn dữ liệu RCA — nghiên cứu

- **Trạng thái:** ĐỀ XUẤT, chưa duyệt. Không phải SPEC; không thay MRP, KE-HOACH, WHY, DECISIONS.
- **Người soạn:** Claude, ngày 10/11/2026. Người phản biện: chưa có (Minh quyết sau).
- **Quyền ghi:** prompt của Minh ngày 10/11/2026 cho phép đúng hai file trong `docs/techstack/`. File đi kèm: [PLAN-TRIEN-KHAI.md](PLAN-TRIEN-KHAI.md).
- **Phục vụ:** MRP P9 (kho quan sát, bộ đọc), P10 (thực nghiệm FlashTicket, demo); DT18-NV2 (log, trace, metric ánh xạ lên đồ thị), DT18-NV3 (áp dụng trên hệ bán vé); mục tiêu "RCA bản đầu trên FlashTicket trong 7 ngày" (DECISIONS, mục 09/11/2026).

**Nhãn dùng trong file.**

| Nhãn | Nghĩa |
|---|---|
| [REPO] | File trong repo RCA `D:\RCA-flashticket` |
| [CODE] | Code hoặc cấu hình repo FlashTicket `D:/Project/flash-ticket-platform` (commit `1d40c97`, đã fetch 10/11/2026 00:08) |
| [MÁY] | Lệnh chỉ đọc đã chạy, kèm kết quả. Máy demo: `52.64.237.84`, user `ubuntu`, qua `plink -batch`; giờ máy 09/11/2026 18:45 UTC |
| [WEB] | Tài liệu hoặc API chính thức, URL ở §9, truy cập 10/11/2026 |
| [TÍNH] | Tự tính, ghi công thức và giả định |
| [CHƯA BIẾT] / [CHƯA KIỂM] | Không có nguồn hoặc chưa kiểm; kèm cách kiểm |
| [SUY LUẬN] | Suy ra từ dữ kiện có nhãn khác; chưa kiểm trực tiếp |

---

## 0. Tóm tắt khuyến nghị

| Lớp | Khuyến nghị | Mức chắc chắn |
|---|---|---|
| Ứng dụng | Gắn **OTel Java agent 2.33.1** qua `JAVA_TOOL_OPTIONS`, không sửa code Java. Log giữ JSON của Spring, đổi tên khóa MDC của agent thành `traceId`/`spanId` | Trung bình: agent hỗ trợ Spring Boot 4 theo changelog; chưa chạy trên FlashTicket |
| CSDL, nhắn tin | Giữ nguyên PostgreSQL 16.15, MongoDB 7.0, Redis 7.4.11, RabbitMQ 4.3.6. Thu metric bằng receiver của Collector | Cao cho phần giữ nguyên; trung bình cho receiver (beta) |
| Định danh, cổng vào | Giữ Keycloak 26.8.0 và Spring Cloud Gateway. Tải lấy token trước; thí nghiệm dùng mock VNPay, không dùng ngrok chung | Trung bình |
| Thu thập, kho | **OTel Collector contrib 0.165.0** → Prometheus 3.16.0 (OTLP), Loki 3.7.9 (OTLP), Tempo 3.1.1 (monolithic), Grafana 13.3.0. Thêm **bản xuất file theo lượt** làm nguồn chấm | Trung bình: chưa đo RAM, dung lượng |
| Sinh tải | **k6 2.3.0** trên máy riêng | Cao |
| Tiêm lỗi | **Toxiproxy 2.13.0** cho cạnh tới DB/cache/broker/đối tác; **Pumba 1.6.0** cho pause/stress/kill; cờ lỗi trong code cho Saga; Chaos Monkey 4.0.0 là phương án phụ | Trung bình: `network_mode: host` chặn netem theo từng service |
| Bộ đọc RCA | Adapter Python mới, xuất đúng định dạng nội bộ của `src/m1/adapter.py`; đọc bản xuất file cho thực nghiệm, đọc API cho demo trực tuyến | Trung bình |
| CI/CD, triển khai | Giữ CD hiện có cho ứng dụng; kho quan sát và công cụ tiêm lỗi là compose riêng, ghim digest, do Minh vận hành | Trung bình |

Lý do, phương án đã xét và điều kiện làm khuyến nghị sai ở §4.

---

## 1. Ràng buộc rút ra từ dữ kiện

### 1.1 Nghiên cứu cần gì từ FlashTicket

- G4 duyệt ngày 09/11/2026: M1 không hơn rõ baseline mạnh ở bộ nào; quan hệ chỉ giúp có điều kiện [REPO `results/T-057/ho-so-g4.md` §0, `tasks/T-057-ho-so-g4/LOG.md` phiên 3 tiếp].
- Phần G4 thiếu: P/R/F1 phát hiện (RQ3a), P/R/F1 vùng (RQ3c), cạnh dữ liệu và thông điệp (DT18-NV2) [REPO `results/T-057/ho-so-g4.md` §0 "Thiếu so với DT18 và cô"].
- Các OPEN chỉ FlashTicket phân xử được: định vị vật lý của trễ E2 cần span client và server ở hai đầu cạnh; độ đúng của E5 cần nhãn mức thành phần; nguồn kênh cực trị cần đo trực tiếp [REPO `results/T-057/ho-so-g4.md` §12].
- Hợp đồng chuyển giao đã duyệt: ba bản phải so trên FlashTicket (bản P7 chạy thẳng, bản FlashTicket, bản FlashTicket che từng nhóm thông tin) [REPO `tasks/T-043-thiet-ke-rca-m1/SPEC.md` B1.9; DECISIONS Q-201].
- Mục tiêu gần: RCA bản đầu chạy trên FlashTicket tới 16/11/2026 [REPO `docs/DECISIONS.md`, mục "Khép T-054, T-055, T-056; hoãn P8; mục tiêu FlashTicket 7 ngày"].

### 1.2 Định dạng đầu vào M1 đã có

- M1 nhận đúng bảy tham số: `spans`, `metrics`, `logs`, `inventory`, `aliases`, `t`, `params` [REPO `results/T-043/hop-dong.json#/vao/tham_so_duy_nhat`].
- Span: `traceID`, `spanID`, `parentSpanID`, `owner`, `operation`, `start_us`, `duration_us`. Không có trường kiểu span hay thuộc tính [REPO `results/T-043/hop-dong.json#/vao/spans`; `src/m1/adapter.py:63-64`].
- Metric: cột `time` và cột `<thực thể>_<kênh>`. Kênh RE2-TT theo hậu tố: `cpu`, `mem`, `diskio`, `socket`, `workload`, `error`, `latency-50`, `latency-90` [REPO `results/T-043/hop-dong.json#/kenh/RE2-TT/metric_theo_hau_to`].
- Log: `timestamp`, `entity`, `message`, có thể có `severity_raw` [REPO `results/T-043/hop-dong.json#/vao/logs`].
- Tham số E4 cần tối thiểu 20 span và 5 điểm metric cho một đơn vị [REPO `results/T-043/hop-dong.json#/vao/params/tham_so_E4`].
- Trên FlashTicket, tập ứng viên là các nút của mô hình T-037: dịch vụ, gateway, DB logic, cache, broker, đối tác ngoài, máy [REPO `results/T-043/hop-dong.json#/flashticket_B1_9`].
- Thời gian chạy M1 một ca trên EC2: TT khoảng 118 và 212 giây, OB khoảng 49 và 51 giây (lượt lạnh, gồm đọc nguồn) [REPO `results/T-054/reports/tu-soat-003/bao-cao.md:77`].

### 1.3 FlashTicket thật (code)

| Dữ kiện | Nhãn |
|---|---|
| Spring Boot 4.1.1, Java 21, Spring Cloud 2025.1.3 ở mọi service Java | [CODE] `services/*/pom.xml`, `infrastructure/*/pom.xml` |
| Không pom nào có OpenTelemetry, Micrometer Prometheus, logstash encoder hay Micrometer Tracing | [CODE] `grep -rniE "opentelemetry\|micrometer\|prometheus\|logstash\|tracing" --include=pom.xml` → không dòng nào |
| Actuator chỉ mở `health,info` | [CODE] `services/*/src/main/resources/application.yaml`, khóa `management.endpoints.web.exposure.include` |
| Log JSON dạng `logstash` ở event, payment, ticket, user, gateway; booking chưa có | [CODE] cùng các file trên, khóa `logging.structured.format.console` |
| Danh sách trường log có `traceId`, `spanId`, chưa có `hostId` | [CODE] `services/payment-service/src/main/resources/application.yaml:107` |
| event-service tự đọc header `traceparent` và đặt `traceId`/`spanId` vào MDC; không tạo span | [CODE] `services/event-service/src/main/java/com/flashticket/event_service/web/CorrelationFilter.java:46-50` |
| booking lưu `traceparent` trong envelope outbox | [CODE] `services/booking-service/.../entity/OutboxMessage.java:48-49` |
| Phụ thuộc dữ liệu: event, ticket, booking, payment dùng JPA (PostgreSQL); user dùng MongoDB; booking dùng Redis; gateway dùng Redis reactive; mọi service nghiệp vụ dùng AMQP; booking dùng OpenFeign | [CODE] `services/*/pom.xml` |
| Image app: `eclipse-temurin:21-jre-alpine` theo digest; `JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC"` đặt sẵn trong image | [CODE] `services/booking-service/Dockerfile` |
| Container app chạy `network_mode: host`, `read_only: true`, user 10001, không giới hạn CPU, log `json-file` 10 MB × 3 | [CODE] `deploy/app/_common.yml` |
| Keycloak 26.8.0 tự build kèm SPI outbox gửi RabbitMQ | [CODE] `services/keycloak-spi/Dockerfile:1` |
| Thanh toán gọi VNPay sandbox, URL đổi được qua biến môi trường; chưa có mock | [CODE] `services/payment-service/src/main/resources/application.yaml:84-90`; không tìm thấy lớp mock |
| ngrok trên máy 84 và ngrok local dùng chung một `NGROK_DOMAIN` | [CODE] `deploy/app/README.md`, mục "Lưu ý về Ngrok" |

### 1.4 Máy demo `52.64.237.84`

| Dữ kiện | Nhãn |
|---|---|
| `c7i-flex.large`, `ap-southeast-2b`, on-demand | [MÁY] IMDSv2 `meta-data/instance-type`, `placement/availability-zone`, `instance-life-cycle` |
| 2 vCPU Xeon Platinum 8488C (1 lõi × 2 luồng); RAM 3812 MiB; swap file 4 GiB, đang dùng 1433 MiB; available 758 MiB | [MÁY] `nproc`, `lscpu`, `free -m`, `swapon --show` |
| Đĩa 29 GB, dùng 24 GB (83%), còn 5,0 GB. Image Docker 11,73 GB, trong đó 8,712 GB có thể thu hồi | [MÁY] `df -h /`, `docker system df` |
| 14 container chạy: 9 ứng dụng từ `/opt/flash-ticket-app/compose/`, 4 hạ tầng từ `/opt/flash-ticket-infra/`, cộng ngrok | [MÁY] `docker compose ls`, `docker ps` |
| Tổng `MemUsage` của 14 container 2443,7 MiB lúc rảnh; tổng `mem_limit` 9024 MiB | [MÁY] `docker stats --no-stream`; `docker inspect --format {{.HostConfig.Memory}}`. [TÍNH] cộng 14 dòng |
| CPU lúc rảnh: user 11–13%, system 3–4% | [MÁY] `vmstat 2 3` |
| Không container nào OOM hay khởi động lại; ứng dụng khởi động 08/11/2026 13:31–13:46 UTC | [MÁY] `docker inspect` (`RestartCount`, `OOMKilled`, `StartedAt`) |
| Revision trong label image khớp các commit trên `main`: `5c6d1c13`, `e4304048`, `437724b7`, `776d9c9e`, `7d5125b2` | [MÁY] label `org.opencontainers.image.revision`; [CODE] `git log -1 <rev>` |
| Docker 29.1.3, Compose 2.40.3; NTP đã đồng bộ, múi giờ UTC | [MÁY] `docker version`, `timedatectl show` |
| Cổng nghe: 8081–8086 và 8761 trên mọi địa chỉ; 5672, 15672, 6379, 8080, 5173 trên `0.0.0.0`; PostgreSQL, MongoDB chỉ `127.0.0.1` | [MÁY] `ss -ltn` |
| Bản nháp stack quan sát ở `~/flashticket` (ngày 19/09/2026) dùng tag `latest`, Collector chỉ xuất `debug` và Tempo, Prometheus chỉ tự scrape chính nó; không chạy | [MÁY] đọc `otel/config.yaml`, `prometheus/prometheus.yml`, `tempo/config.yaml`, dòng `image:` của `docker-compose.yml` (không đọc dòng chứa mật khẩu) |

**Máy này có phải "máy 84" của CD không.** Rất có khả năng có. Bằng chứng:
- CD ghi vào `/opt/flash-ticket-app` (biến `APP_ROOT`) và đặt tên bước "Deploy … to 84" [CODE `.github/workflows/_deploy-service.yml`].
- Máy có đúng cấu trúc `compose/`, `env/`, `state/<svc>.current` mà CD tạo [MÁY `ls -la /opt/flash-ticket-app /opt/flash-ticket-app/state`].
- Lượt CD số 11 bắt đầu 08/11/2026 13:31:15Z [WEB GitHub Actions API]; các container ứng dụng khởi động 13:31:46Z–13:46:11Z [MÁY].
- **Chưa kiểm trực tiếp** biến `FT84_SSH_HOST`. Cách kiểm: GitHub → repo `flash-ticket-platform` → Settings → Secrets and variables → Actions → tab Variables. Biến (không phải secret) xem được giá trị.

### 1.5 Laptop

| Dữ kiện | Nhãn |
|---|---|
| RAM 15,7 GiB, lúc kiểm còn trống 6,3 GiB; i5-1240P | [MÁY] PowerShell `Get-CimInstance Win32_OperatingSystem`, `Win32_Processor` |
| Ổ C còn 54,1 GB; **ổ D còn 12,7 GB** (AGENTS §12 ghi khoảng 65 GB ngày 02/10) | [MÁY] `Get-PSDrive C,D` |
| Docker client 28.3.2; engine đang tắt; không có `.wslconfig` | [MÁY] `docker version`; `Test-Path $env:USERPROFILE\.wslconfig` |
| WSL2 mặc định cấp 50% RAM (khoảng 7,8 GiB) | [REPO `docs/KE-HOACH-GIAI-DOAN-TOI.md` Phần B, dòng Laptop, nguồn Microsoft] |

### 1.6 AWS

| Dữ kiện | Nhãn |
|---|---|
| Gói Free: 100 USD khi tạo, thêm tối đa 100 USD qua hoạt động; hết sau 6 tháng hoặc khi hết tín dụng; khi đó tài khoản tự đóng, giữ dữ liệu 90 ngày | [WEB] AWS Billing, Free plan |
| Gói Free không bị tính tiền vượt tín dụng; gói Paid trả tiền phần vượt | [WEB] cùng trang |
| Tham gia AWS Organizations thì gói Free tự lên Paid | [WEB] cùng trang |
| Tài khoản tạo từ 15/07/2025: loại máy free-tier là `t3.micro`, `t3.small`, `t4g.micro`, `t4g.small`, `c7i-flex.large`, `m7i-flex.large` | [WEB] EC2 Free Tier usage |
| `c7i-flex.large`: 2 vCPU, 4 GiB, nền 40% mỗi vCPU, "scale up to full compute performance most of the time" | [WEB] trang C7i |
| `m7i-flex.large`: 2 vCPU, 8 GiB (7,6 GiB dùng được) | [REPO `results/T-007/moi-truong-ec2.md` §1] |
| Quota mặc định "Running On-Demand Standard" = **5 vCPU mỗi vùng**, xin tăng được (mã `L-1216C47A`) | [WEB] EC2 instance quotas |
| IPv4 công khai 0,005 USD/giờ, cả khi dùng và khi rảnh | [WEB] VPC pricing |
| Giá `m7i-flex.large` 0,1197 USD/giờ theo console của Minh | [REPO `tasks/T-005-do-kha-thi/LOG.md:168`] |
| Giá `c7i-flex.large` ở ap-southeast-2; giá EBS gp3; phí truyền dữ liệu ra internet | [CHƯA BIẾT]. Kiểm: EC2 console → Launch instance → chọn loại máy xem giá; trang AWS Pricing Calculator |
| Ngày mở, số dư tín dụng, gói (Free/Paid), quota thật của 3 tài khoản | [CHƯA BIẾT]. Kiểm: Billing → Free plan; Service Quotas → EC2 → `L-1216C47A` từng tài khoản, vùng ap-southeast-2 |

### 1.7 Mâu thuẫn giữa nguồn (cần Minh xác nhận)

| Điểm | Nguồn A | Nguồn B | Xử lý trong file này |
|---|---|---|---|
| Grafana Cloud | `KE-HOACH-GIAI-DOAN-TOI.md` E-11: "Đã trả lời (M-36): dùng, không đắn đo" [REPO] | Prompt 10/11/2026 §4.2: Minh chưa quyết đưa dữ liệu ra ngoài | Coi là **chưa quyết**; kho tự cài là nguồn chấm; Grafana Cloud là phương án phụ (§4.4). Câu hỏi Q4 ở PLAN §9 |
| Topology đích | Hai máy 8 GiB, mỗi máy khoảng 6 GiB cho tiến trình [CODE `docs/architecture/aws-runtime-baseline.md` §4] | Một máy `c7i-flex.large` 4 GiB chạy toàn bộ [MÁY] | Dùng số đo thật; tài liệu thiết kế chỉ tham khảo |
| Metric ứng dụng | B16: Actuator/Micrometer → Prometheus [CODE `docs/architecture/B16-observability-baseline.md` §2] | Không có registry Prometheus, actuator chỉ `health,info` [CODE] | Đề xuất metric qua agent và Collector (§4.1, §4.4); không cần sửa pom |
| `hostId` trong log | B16 §4: bắt buộc ở runtime thật | Danh sách trường log chưa có [CODE] | Gắn `host.id` ở thuộc tính tài nguyên của agent (§6.1); log cần nhóm hệ thống thêm khóa |
| Số tài khoản AWS | 4 tài khoản Free [REPO `KE-HOACH` Phần B] | 3 tài khoản còn dùng được, 1 bị tạm khóa (prompt 10/11) | Dùng 3 tài khoản |

---

## 2. Dữ liệu RCA cần và đối chiếu với dữ liệu đã có

"Có/không" của ba bộ công khai lấy từ kết quả đã có, không đọc lại dữ liệu. Ô ghi "?" là chưa có bằng chứng trong repo.

| # | Thông tin cần | Dùng cho | RE2-TT | Nezha-OB | RE3-OB | Nguồn trên FlashTicket | Cách kiểm |
|---|---|---|---|---|---|---|---|
| D1 | Span có cha–con, owner, operation, start, duration | Lõi M1: E1, E2, E5; đồ thị quan sát | Có; 98,45% span cha resolve được [REPO `docs/LESSONS.md` ST2] | Có; gốc ghi `ParentID = "root"` [REPO `docs/STATE.md`, lưu ý adapter] | Có; 12/30 ca bên được gọi không có trace [REPO `results/T-057/ho-so-g4.md` §13] | Agent: HTTP server/client, gateway, Feign | Tỷ lệ span có cha trong cùng export; mọi service có span |
| D2 | Kiểu span CLIENT/SERVER và đích lời gọi | E2 dùng cặp CLIENT–SERVER (B1.9); định vị trễ cạnh | Không | Không | Không [REPO `results/T-057/ho-so-g4.md` §7: cạnh "không có kiểu"; `results/T-040/yeu-cau-quan-sat-p9.md` R-01] | Agent, quy ước ngữ nghĩa OTel | R-01: mọi span CLIENT có đích; ghép CLIENT→SERVER |
| D3 | Span DB/cache: hệ, DB logic, địa chỉ | Cạnh "phụ thuộc dữ liệu" của DT18; nút DB trong tập ứng viên | Không; 26 thực thể DB/cache xếp hạng nhưng không có cạnh [REPO `results/T-057/ho-so-g4.md` §7] | Không | Không | Agent: JDBC, Lettuce, MongoDB | R-03: 12 cạnh dữ liệu T-037 có span tương ứng |
| D4 | Span PRODUCER/CONSUMER, đích, message ID, link | Cạnh "trao đổi thông điệp" của DT18; Saga | Không | Không | Không [REPO `results/T-057/ho-so-g4.md` §7] | Agent: Spring RabbitMQ; envelope `traceparent` sẵn có | R-04, R-09 |
| D5 | Log mang `traceId`, `spanId` | Nối log–span (B1.9; WHY-61 hoãn ở bản P7) | Không có cột ID [REPO `results/T-043/hop-dong.json#/kenh/RE2-TT/cot_ID_log` = false] | Baseline phải nối theo service và thời gian [REPO `results/T-040/yeu-cau-quan-sat-p9.md` R-06] | ? | Agent đặt MDC; Spring ghi JSON | R-06: tỷ lệ log nối được vào span tồn tại |
| D6 | Trạng thái lỗi ở span của service phát sinh; `errorType` trong log | Kênh lỗi; lỗi mã nguồn lan lên bên gọi | `statusCode` rỗng toàn bộ [REPO `docs/LESSONS.md` ST2] | ? | Lỗi lan lên bên gọi qua status, log, trace [REPO `results/T-057/ho-so-g4.md` §10] | Agent đặt status khi 5xx/exception; log B16 | Đếm span ERROR khi tiêm lỗi code |
| D7 | Metric tài nguyên theo container | E1 lỗi CPU; tài nguyên chung | Có `cpu`, `mem`, `diskio`, `socket` [REPO `hop-dong.json#/kenh/RE2-TT`] | Có CPU, Memory, Syscall, Network [REPO `hop-dong.json#/kenh/Nezha-OB`] | Có theo profile [REPO `src/m1/adapter.py:39-43`] | Receiver `docker_stats` hoặc cAdvisor | Mỗi service có đủ cột |
| D8 | RED theo service và theo cạnh | Kênh `workload`, `error`, `latency-*`; "tải vào" ở B1.9 | Có [REPO `hop-dong.json#/kenh/RE2-TT`] | Có PodClient/ServerLatency, Workload | ? | Connector `spanmetrics`, `servicegraph`; metric HTTP của agent | So số request k6 gửi với số đếm spanmetrics |
| D9 | Metric DB, cache, broker, pool kết nối | Nút DB/broker; kịch bản cạn pool, consumer dừng | Không có nút DB trong trace | Không | Không | Receiver postgresql/redis/mongodb/rabbitmq; pool HikariCP qua agent | B16 §5: connection pool, queue ready/unacked |
| D10 | Host ID và instance ID trên cả ba tín hiệu | Cạnh triển khai; tài nguyên chung (G2-H11) | Không [REPO `yeu-cau-quan-sat-p9.md` R-05] | Node OPEN | ? | Thuộc tính tài nguyên của agent; receiver hostmetrics | R-05 |
| D11 | Đoạn nền sạch, đủ dài, đã xác nhận | Ngưỡng E4; RQ3a; phép thử giả C-e | Không có nền sạch [REPO `docs/DECISIONS.md` Q-140] | Nền ngắn [REPO `yeu-cau-quan-sat-p9.md` R-08, G2-H19] | ? | Lượt nền riêng có kiểm | R-07, R-08 |
| D12 | Mốc tiêm, onset có tác động, hồi phục | Chế độ (a); độ trễ phát hiện RQ3a | Chỉ thời điểm tiêm [REPO `docs/LESSONS.md` ST1] | ? | ? | Sổ thực nghiệm; số đo phía người dùng của k6 | R-07; PLAN §5 |
| D13 | Nhãn vùng ảnh hưởng, nhãn mức thành phần | RQ3c P/R/F1; độ đúng của E5 | Không | Không | Không [REPO `results/T-057/ho-so-g4.md` §3, §7] | k6 gắn tag theo endpoint; giao thức P10 | B1.9 "Nhãn và chấm" |
| D14 | Tải thay đổi có kiểm soát (flash sale, tải tăng không lỗi) | Câu phụ RQ5; phân biệt retry với tải vào | Tải gần đều [REPO `tasks/T-043-thiet-ke-rca-m1/SPEC.md:484`] | như trên | như trên | k6 `ramping-arrival-rate` | Dòng thời gian tải trong manifest |
| D15 | Manifest lượt: digest, version agent, sampling, lệch đồng hồ, số drop | Tái lập; R-07, R-08, R-10 | Không | Không | Không | CD lưu digest; Collector tự báo drop | R-10 |
| D16 | Lấy mẫu trace 100% và đếm drop | Độ phủ cạnh | ? | ? | ? | Sampler `parentbased_always_on`; metric nội bộ Collector | R-08 |
| D17 | Nhiều vị trí root (lá, giữa, hub) và nhiều họ lỗi | MRP §4 tiêu chí 5–7; chia theo ô (WHY-04) | 5 root [REPO `docs/LESSONS.md` ST1] | 10 dịch vụ | 4 root (ad, cart, currency, email) [REPO `KE-HOACH` Phần B] | Danh mục kịch bản [REPO `KE-HOACH` D.9] | Đếm ô hữu hiệu trước chiến dịch |

**Đọc bảng.** D2, D3, D4, D9, D13, D14 không có ở cả ba bộ công khai. Đây là phần FlashTicket thêm được. Thêm trường chưa chứng minh RCA tốt hơn; lợi ích chỉ đo được ở P10 [REPO `results/T-040/yeu-cau-quan-sat-p9.md` mục 3].

---

## 3. Tiêu chí chọn

| Mã | Tiêu chí | Vì sao |
|---|---|---|
| T1 | Sinh đủ D1–D17 | Đây là lý do dùng FlashTicket (MRP P10) |
| T2 | Ít sửa repo FlashTicket, không đổi logic nghiệp vụ | Repo của nhóm hệ thống; Luật 0; B16 |
| T3 | Vừa tài nguyên máy sẵn có (2 vCPU, 4–8 GiB mỗi máy) | Gói Free chỉ cho tới `m7i-flex.large` (§1.6) |
| T4 | Ghim phiên bản, tái lập được bằng digest | LESSONS SL29; manifest R-10 |
| T5 | Không rò nhãn vào phương pháp | AGENTS luật cứng 6 |
| T6 | Chạy với Spring Boot 4.1.1, Java 21 | Code thật (§1.3) |
| T7 | Một người vận hành được, có tài liệu chính thức | Minh chưa có kinh nghiệm hạ tầng (KE-HOACH M-10) |
| T8 | Đổi backend được sau này | OTLP là giao thức chuẩn; tránh khóa vào một nhà cung cấp |

---

## 4. Từng lớp

Mỗi lớp: hiện trạng, phương án, khuyến nghị, khi nào khuyến nghị sai, cách kiểm.

### 4.1 Ứng dụng: sinh trace, log, metric

**Hiện trạng.** Không có tracing. Log JSON ở 5/6 ứng dụng Spring. Không có metric ứng dụng ra ngoài (§1.3).

| Phương án | Ưu | Nhược | Nguồn |
|---|---|---|---|
| **A. OTel Java agent 2.33.1** gắn qua `JAVA_TOOL_OPTIONS` | Không sửa code. Có span cho Spring WebMVC, WebFlux, Spring Cloud Gateway, JDBC, Lettuce, MongoDB, Spring RabbitMQ, HikariCP; metric HTTP và pool | Sửa bytecode lúc chạy; overhead phải tự đo; cần đưa file jar vào container | [WEB] supported-libraries v2.33.1; changelog: "Added support for Spring Framework 7.0" (bản 2.22.0), "Spring WebMVC/WebFlux/Spring Cloud Gateway: support Spring Boot 4" (bản 2.23.0) |
| B. `spring-boot-starter-opentelemetry` (Spring Boot 4.1) | Chính chủ Spring; không sửa bytecode | Phải sửa pom và cấu hình 7 service; mặc định chỉ lấy mẫu 10%; độ phủ JDBC, Redis, RabbitMQ, Mongo chưa kiểm | [WEB] Spring Boot 4.1.2 docs, Tracing: "By default, Spring Boot samples only 10% of requests" |
| C. Giữ nguyên, chỉ log và metric | Không đổi gì | Không có D1–D4: M1 mất đầu vào chính | §1.2 |

**Khuyến nghị: A.** B16 cũng chọn agent làm mặc định [CODE `docs/architecture/B16-observability-baseline.md` §2].

**Cấu hình then chốt** (đề xuất, [CHƯA KIỂM] trên FlashTicket):
- Sampler `parentbased_always_on` cho lượt thực nghiệm (D16).
- Đổi khóa MDC của agent sang tên Spring đang ghi: `otel.instrumentation.common.logging.trace-id-key=traceId`, `...span-id-key=spanId`. Mặc định của agent là `trace_id`, `span_id` [WEB] README logback-mdc v2.33.1.
- `otel.logs.exporter=none`: log đi đường stdout JSON (§4.4), tránh đếm trùng (B16 §2: một đường xuất cho mỗi tín hiệu).
- Thuộc tính tài nguyên: `service.name`, `service.instance.id`, `host.id`, `deployment.environment`.
- Biến `JAVA_TOOL_OPTIONS` từ env file **thay** giá trị trong image, nên phải chép lại `-XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC` [SUY LUẬN từ cách Docker ưu tiên biến môi trường lúc chạy; kiểm bằng `docker inspect` sau khi chạy].
- Đưa jar vào container (sửa 10/11/2026, Minh duyệt): **thử lần đầu bằng cách gắn jar tạm trên `exp-app`**; chạy được với Boot 4.1.1 thì Minh **thêm jar vào Dockerfile** qua PR, jar nằm sẵn trong image và chỉ bật khi env có `-javaagent`. Khi đó compose của `exp-app` và 84 không khác nhau; 84 muốn bật chỉ cần sửa secret env. Phương án đã xét: bind mount chỉ đọc trong `deploy/app/*.yml`. CD ghi đè thư mục compose mỗi lần deploy [CODE `deploy/app/README.md`], nên sửa tay trên máy sẽ mất.

**Sai khi:**
- Agent làm ứng dụng lỗi khởi động hoặc sai hành vi trên Boot 4.1.1 (changelog nói hỗ trợ Boot 4, không nói 4.1.x cụ thể).
- Overhead làm máy 2 vCPU quá tải. Tài liệu OTel không đưa số overhead, khuyên tự đo [REPO `KE-HOACH` Phần B, dòng Công cụ].
- MDC `traceId` do event-service tự đặt (là span của **bên gọi**) đè giá trị agent. Agent ghi vào bản sao MDC của sự kiện log, không vào MDC luồng [WEB README logback-mdc]; ai thắng khi trùng khóa thì [CHƯA KIỂM].

**Cách kiểm (bước H1 ở PLAN §6):** một request gateway → booking → PostgreSQL/Redis/RabbitMQ. Đạt khi: span có kind và `http.route`; có span JDBC, Redis, RabbitMQ; `traceId` trong log JSON trùng span; metric lên Prometheus; health UP, không restart.

### 4.2 Cơ sở dữ liệu và nhắn tin

**Hiện trạng.** PostgreSQL 16.15, MongoDB 7.0, Redis 7.4.11-alpine, RabbitMQ 4.3.6-management, mỗi cái một container [MÁY `docker ps`].

| Phương án | Ưu | Nhược |
|---|---|---|
| **A. Giữ nguyên, thêm thu metric** | Không đổi hệ thống; tiêm lỗi được ở mức container và mạng | Thêm receiver hoặc exporter |
| B. Dịch vụ quản lý (RDS, ElastiCache, Amazon MQ) | Ít vận hành | Không tiêm lỗi container được; có thể ngoài gói Free [CHƯA KIỂM]; đổi B12 |

**Khuyến nghị: A.** Thu metric bằng receiver của Collector: `postgresql`, `redis`, `mongodb`, `rabbitmq` (đều beta với metric) [WEB README v0.165.0]. Phương án phụ: exporter riêng `postgres_exporter` 0.20.1, `redis_exporter` 1.97.0, `mongodb_exporter` 0.54.0. Chọn receiver để bớt container trên máy nhỏ (T3).

- RabbitMQ có plugin Prometheus sẵn ở cổng 15692: [CHƯA KIỂM] plugin đã bật. Image có khai cổng 15691–15692 [MÁY `docker ps`], chưa chứng minh plugin bật. Kiểm: `curl -s 127.0.0.1:15692/metrics | head` trên máy thực nghiệm.
- Receiver cần tài khoản giám sát chỉ đọc trên PostgreSQL, MongoDB. B16 §6 cấm RCA có quyền đọc DB nghiệp vụ; tài khoản này dành cho **Collector**, chỉ đọc thống kê, không đọc bảng nghiệp vụ.

**Sai khi:** receiver beta thiếu metric cần (pool, queue ready/unacked). Khi đó dùng exporter.

### 4.3 Định danh và cổng vào

**Hiện trạng.** Keycloak 26.8.0; Spring Cloud Gateway WebFlux có Redis và Resilience4j [CODE `infrastructure/api-gateway/pom.xml`]; VNPay sandbox qua ngrok.

| Vấn đề | Phương án | Khuyến nghị |
|---|---|---|
| Token cho tải | (a) k6 lấy token trước trong `setup()` cho N người dùng thử; (b) bỏ xác thực ở môi trường thử | (a). (b) đổi hệ thống, kết quả NV1 mất giá trị |
| Trace của Keycloak | (a) không trace Keycloak, chỉ thấy span client từ service gọi tới; (b) bật tracing của Keycloak | (a) trước. (b): [CHƯA KIỂM] tùy chọn tracing của Keycloak 26.8.0; kiểm trong tài liệu Keycloak khi cần nút Keycloak có span riêng |
| VNPay trong thực nghiệm | (a) mock HTTP (WireMock 3.13.2) đặt qua biến `VNPAY_API_URL`, `VNPAY_PAYMENT_URL`; (b) sandbox thật qua ngrok | (a). Lý do: ngrok dùng chung domain với máy 84 [CODE `deploy/app/README.md`], chạy song song sẽ tranh webhook; sandbox ngoài tạo biến động không kiểm soát được. Kịch bản "VNPay chậm" cần mock để tiêm trễ [REPO `KE-HOACH` D.9] |

### 4.4 Thu thập và kho quan sát

**Hiện trạng.** Chưa chạy. Bản nháp dùng tag `latest`, chưa có đường metric và log (§1.4).

**Collector.**

| Phương án | Ưu | Nhược |
|---|---|---|
| **A. OTel Collector contrib 0.165.0** | Đúng B16; có `spanmetrics`, `servicegraph`, `tail_sampling`, `filelog`, `docker_stats`, `hostmetrics`, receiver DB; tự báo drop | Nhiều thành phần alpha: `spanmetrics`, `servicegraph`, `docker_stats`, `file` exporter [WEB README v0.165.0] |
| B. Grafana Alloy 1.21.3 | Bản phân phối của Collector, có nguồn log Docker riêng | Cấu hình ngôn ngữ riêng; lệch B16 về tên |
| C. Agent gửi thẳng tới kho | Ít thành phần | Mất spanmetrics/servicegraph, không đếm drop tập trung, không sao gửi hai đích |

**Khuyến nghị: A.** Không có `lokiexporter` trong contrib 0.165.0 (README không còn khối Stability) [WEB]; gửi log sang Loki bằng `otlphttp` vì Loki 3 nhận OTLP [CHƯA KIỂM đường `/otlp` trên Loki 3.7.9; kiểm ở B2].

**Đường đi tín hiệu đề xuất.**

| Tín hiệu | Đường | Lý do |
|---|---|---|
| Trace | Agent → OTLP (`127.0.0.1`) → Collector tại chỗ → Collector trung tâm → (a) `spanmetrics`, `servicegraph` → Prometheus; (b) Tempo; (c) file OTLP JSON theo lượt | (c) là nguồn chấm: đủ mọi span trong cửa sổ, băm được, phát lại offline được |
| Log ứng dụng | stdout JSON → `json-file` của Docker → `filelog` của **Collector tại chỗ trên `exp-app`** (đọc `/var/lib/docker/containers`, cần quyền root) → Collector trung tâm → Loki và file theo lượt | Giữ nguyên whitelist trường của B16 do Spring ghi; không cần cấu hình OTLP appender |
| Metric ứng dụng | Agent → OTLP (`127.0.0.1`) → Collector tại chỗ → Collector trung tâm → Prometheus (OTLP receiver) | Không cần sửa pom (khác B16 §2, xem §1.7) |
| Metric container, máy | `docker_stats`, `hostmetrics` trong **Collector tại chỗ trên `exp-app`** (đọc Docker socket và thông số của máy đó) | Bớt container; phương án phụ cAdvisor 0.60.6 + node_exporter 1.12.1 |
| Metric DB, broker | Receiver DB trong Collector tại chỗ (cùng máy với DB) | §4.2 |

**Kho.**

| Thành phần | Khuyến nghị | Phương án khác | Ghi chú |
|---|---|---|---|
| Trace | **Tempo 3.1.1, chế độ monolithic** | Jaeger 2.23.0; chỉ file | Tempo 3.0 bỏ chế độ scalable-single-binary; monolithic "No Kafka is required"; microservices cần Kafka [WEB Tempo 3.0 docs]. Không hạ cấp từ 3.x về 2.x được [WEB upgrade docs, qua kết quả tìm kiếm] |
| Metric | **Prometheus 3.16.0**, bật `--web.enable-otlp-receiver`, `out_of_order_time_window: 30m`, `promote_resource_attributes` gồm `service.name`, `service.instance.id`, `host.id` | VictoriaMetrics 1.156.0 (nhẹ hơn, [CHƯA KIỂM] mức RAM) | [WEB] Prometheus OTel guide. Luật cảnh báo Grafana đọc PromQL (M-38) |
| Log | **Loki 3.7.9** | VictoriaLogs; chỉ file | Nhãn Loki chỉ gồm tập hữu hạn (service, severity) theo B16 §5 |
| Giao diện, cảnh báo | **Grafana 13.3.0** | Grafana Cloud | Luật cảnh báo mở sự cố ở mức hệ thống (MRP §2.3, M-38) |
| Môi trường thử nhanh | `grafana/otel-lgtm` 0.40.0 (một container) | — | Chỉ để smoke trên laptop; không dùng cho lượt chấm |

**Vì sao thêm bản xuất file.**
- API tìm kiếm của Tempo trả theo giới hạn số trace mỗi lần [CHƯA KIỂM giá trị mặc định và trần của tham số `limit` ở 3.1.1; kiểm trong tài liệu API Tempo ở B2]. Lấy "mọi span trong 10 phút" qua API vì vậy kém chắc chắn.
- Bản file là ảnh chụp bất biến của một lượt, khớp cách repo đang làm (manifest, hash).
- Nó cũng là chế độ "phát lại offline" cho demo [REPO `KE-HOACH` D.11].
- Exporter `file` là alpha [WEB]. Nếu lỗi, phương án lùi: sau lượt, kéo trace từ Tempo theo trace ID lấy từ log.

**Grafana Cloud** (chưa quyết, §1.7). Đề xuất: không dùng làm nguồn chấm. Nếu Minh duyệt, chỉ gửi bản sao đã lọc (RED, log lỗi) để demo, sau khi kiểm không có dữ liệu cá nhân thật. Hạn mức Free: 10k chuỗi metric, 50 GB log, 50 GB trace mỗi tháng, giữ 14 ngày; trang giá ghi "No charges ever" [WEB grafana.com/pricing].

**Sai khi:**
- RAM kho quan sát vượt máy (chưa đo; PLAN §2).
- Lượng span mỗi request lớn hơn giả định 10 span của KE-HOACH D.8.5. Có span JDBC thì có thể nhiều hơn [SUY LUẬN]; dung lượng phải đo ở B2.

### 4.5 Sinh tải

| Phương án | Ưu | Nhược |
|---|---|---|
| **A. k6 2.3.0 OSS** | Kịch bản JS; executor theo tốc độ đến (`ramping-arrival-rate`) hợp cho flash sale; dùng chung với NV1 (KE-HOACH D.9 f) | k6 2.0 bỏ executor `externally-controlled`; đổi tùy chọn output OpenTelemetry [WEB release v2.0.0] |
| B. Gatling | Mạnh cho tải cao | JVM nặng, kịch bản Scala/Java |
| C. Locust | Python | Mỗi tiến trình bị GIL; cần nhiều worker cho tốc độ cao [SUY LUẬN] |
| D. Grafana Cloud k6 | Tải từ ngoài | 500 VU-giờ mỗi tháng [WEB]; phụ thuộc mạng ngoài |

**Khuyến nghị: A, chạy trên máy riêng** (PLAN §3). Đầu ra k6 theo endpoint là tín hiệu **độc lập** với RCA, dùng làm nhãn vùng mức endpoint và mốc onset có tác động (D12, D13) [REPO `KE-HOACH` D.9 "Nhãn"].

**Sai khi:** tải cần vượt sức một máy 2 vCPU. Khi đó chạy nhiều máy k6 hoặc dùng D.

### 4.6 Tiêm lỗi

**Ràng buộc quan trọng.** Container ứng dụng dùng `network_mode: host` [CODE `deploy/app/_common.yml`; MÁY `docker inspect` net=host]. Các service gọi nhau và gọi DB qua `127.0.0.1` [CODE `deploy/app/README.md`, bảng biến trên máy 84]. Vì vậy `pumba netem` trên một service sẽ tác động **cả namespace mạng của máy**, không cô lập được một service [SUY LUẬN từ hai dữ kiện trên; kiểm bằng thử trên máy thực nghiệm trước khi đưa vào danh mục].

| Công cụ | Dùng cho | Ưu | Nhược | Nguồn |
|---|---|---|---|---|
| **Toxiproxy 2.13.0** | Trễ, timeout, reset, giới hạn băng thông trên cạnh service → DB/Redis/RabbitMQ/VNPay mock | Cô lập theo cạnh dù dùng host network; điều khiển qua API | Phải đổi chuỗi kết nối sang cổng proxy (env); cạnh luôn đi qua proxy, cả lúc bình thường | [WEB] release |
| **Pumba 1.6.0** | `pause`, `stop`, `kill`, `stress` theo container | Không sửa ứng dụng | `netem` không cô lập (trên); container không giới hạn CPU nên `stress` tràn sang cả máy | [WEB] release; [CODE] `_common.yml` |
| Cờ lỗi trong code (KE-HOACH D.9 b) | Lỗi 5xx, chậm bên trong, phát vé lỗi để Saga bù trừ | Chính xác nhất cho lỗi mã nguồn và Saga | Nhóm hệ thống phải cài; cần quyền quản trị để bật | [REPO `KE-HOACH` D.9] |
| Chaos Monkey for Spring Boot 4.0.0 | Trễ, exception theo loại bean | "Upgrade to Spring Boot 4 and Spring Cloud 2025.1", build với Boot 4.0.2 | Thêm dependency vào service; cần mở endpoint actuator; [CHƯA KIỂM] với Boot 4.1.1 | [WEB] release v4.0.0 |
| Chaos Mesh, LitmusChaos | — | — | Cho Kubernetes; FlashTicket chạy Docker trên EC2 (MRP P10) | Loại |

**Khuyến nghị:** Toxiproxy + Pumba (trừ `netem`) + cờ lỗi trong code. Chaos Monkey là phương án phụ nếu nhóm hệ thống không kịp cài cờ.

- Lỗi CPU cô lập theo service cần `cpus:` cho từng container ở môi trường thực nghiệm. Đây là đổi cấu hình hệ thống; nếu không đổi thì ghi giới hạn "tài nguyên chung" cho kịch bản CPU [REPO `KE-HOACH` D.9, Bài học 6].
- Trễ mạng giữa hai service Java: dùng Toxiproxy đặt trên đường gọi (đổi URL qua Eureka khó; [CHƯA KIỂM] cách làm) hoặc thay bằng cờ "chậm bên trong" và ghi rõ cơ chế khác.

### 4.7 Bộ đọc RCA và adapter (P9b)

**Hiện trạng.** Có adapter RE2-TT, Nezha-OB, RE3-OB về một định dạng nội bộ [REPO `src/m1/adapter.py`]. Chưa có adapter FlashTicket. WHY-08 bắt buộc dùng chung một lõi [REPO `docs/WHY.md` WHY-08].

| Phương án | Ưu | Nhược |
|---|---|---|
| **A. Đọc bản xuất file theo lượt (span, log) + Prometheus HTTP API (metric)** | Đủ dữ liệu, băm được, chạy lại offline | Cần bước đóng gói sau mỗi lượt |
| B. Đọc toàn bộ qua API Tempo, Loki, Prometheus | Đúng mô tả P9b; dùng được trực tuyến | Giới hạn tìm kiếm của Tempo (§4.4); khó băm nguồn |
| C. Plugin Grafana | Hiển thị đẹp | Không phải lõi RCA |

**Khuyến nghị: A cho thực nghiệm, B cho demo trực tuyến**, cùng một hàm adapter.

**Ánh xạ đề xuất** ([CHƯA KIỂM], chốt trong SPEC task):
- `owner` = `service.name`; `operation` = tên span; `start_us`, `duration_us` từ thời điểm span.
- Thuộc tính mở rộng (kind, đích, `db.*`, `messaging.*`, host) giữ trong một trường riêng cho các thành phần FlashTicket ở B1.9; bản P7 chạy thẳng không đọc trường này (D14 bản 1).
- Metric: dựng cột `<service>_cpu`, `_mem`, `_workload`, `_error`, `_latency-50`, `_latency-90` giống hậu tố RE2-TT, để bản P7 chạy được mà không đổi lõi.
- Bước metric: với cửa sổ nền 300 giây và `m_metric = 5`, chu kỳ 60 giây chỉ cho 5 điểm [TÍNH 300/60]. Đề xuất chu kỳ 5–15 giây ở lượt thực nghiệm; chu kỳ mặc định của agent [CHƯA KIỂM], kiểm trong tài liệu cấu hình SDK.
- Log: `entity` = `serviceName`; `severity_raw` = trường `severity` của B16.
- `inventory`: nút mô hình T-037 [REPO `hop-dong.json#/flashticket_B1_9/tap_ung_vien`].
- Chặn rò nhãn: dùng lại `src/m1/hop_dong.py` và `chuoi_cam`; thêm tên lượt, tên kịch bản, đường dẫn sổ vào `chuoi_cam` (PLAN §5).

### 4.8 CI/CD và triển khai

**Hiện trạng.** GitHub Actions build → GHCR theo digest → SSH vào máy 84 → `deploy-service.sh` kiểm RAM trống, health, tự rollback [CODE `.github/workflows/cd.yml`, `_deploy-service.yml`, `deploy/scripts/deploy-service.sh`]. Image GHCR **kéo ẩn danh được** [MÁY curl: token ẩn danh từ `ghcr.io/token`, manifest `api-gateway:sha-5c6d1c13…` trả HTTP 200].

| Phương án cho kho quan sát và công cụ tiêm lỗi | Ưu | Nhược |
|---|---|---|
| **A. Compose riêng, ghim digest, Minh dựng qua SSH** | Không chạm repo nhóm; nhanh | Ngoài CD; phải tự ghi manifest |
| B. Đưa vào CD (`services.json`) | Tái lập tốt | Sửa repo nhóm; CD hiện chỉ có một máy đích |
| C. Terraform/Ansible | Dựng lại máy tự động | Thêm công cụ mới; quá sức trong 7 tuần [SUY LUẬN] |

**Khuyến nghị: A trước, B nếu còn thời gian.** Môi trường thực nghiệm dùng **đúng digest** đang chạy trên máy 84 (đọc ở `state/<svc>.current`), để kết quả nói về cùng bản phần mềm.

**Phần cần nhóm hệ thống** (không tự sửa repo FlashTicket):
1. Gắn agent: bind mount jar và biến `OTEL_*` trong `deploy/app/*.yml`, hoặc thêm vào Dockerfile.
2. Bộ env riêng cho môi trường thực nghiệm (mật khẩu mới, không dùng ngrok của 84, URL VNPay mock, chuỗi kết nối qua Toxiproxy).
3. Thêm `hostId` vào danh sách trường log (§1.7).
4. Cờ lỗi trong code (KE-HOACH D.9 b).

---

## 5. Phiên bản ghim

Lấy từ `https://api.github.com/repos/<repo>/releases/latest` ngày 10/11/2026 (bản phát hành mới nhất không phải pre-release). **Ghim theo digest image lúc dựng** (bước H0), vì tag có thể bị ghi đè. Cột "Mới" đánh dấu bản phát hành trong vòng 7 ngày: nếu gặp lỗi lạ ở H1/B2, lùi về minor liền trước và ghi lý do.

| Thành phần | Bản | Ngày phát hành | Repo | Mới |
|---|---|---|---|---|
| OTel Java agent | v2.33.1 | 26/10/2026 | open-telemetry/opentelemetry-java-instrumentation | |
| OTel Collector (contrib) | v0.165.0 | 07/11/2026 | open-telemetry/opentelemetry-collector-releases | ✓ |
| Grafana Alloy (phụ) | v1.21.3 | 28/10/2026 | grafana/alloy | |
| Prometheus | v3.16.0 | 05/11/2026 | prometheus/prometheus | ✓ |
| Loki | v3.7.9 | 20/10/2026 | grafana/loki | |
| Tempo | v3.1.1 | 21/10/2026 | grafana/tempo | |
| Grafana | v13.3.0 | 27/10/2026 | grafana/grafana | |
| otel-lgtm (chỉ smoke) | v0.40.0 | 06/11/2026 | grafana/docker-otel-lgtm | ✓ |
| k6 | v2.3.0 | 21/09/2026 | grafana/k6 | |
| Toxiproxy | v2.13.0 | 14/10/2026 | Shopify/toxiproxy | |
| Pumba | 1.6.0 | 05/11/2026 | alexei-led/pumba | ✓ |
| Chaos Monkey for Spring Boot (phụ) | v4.0.0 | 06/02/2026 | codecentric/chaos-monkey-spring-boot | |
| WireMock (mock VNPay) | 3.13.2 | 14/11/2025 | wiremock/wiremock | |
| cAdvisor (phụ) | v0.60.6 | 18/09/2026 | google/cadvisor | |
| node_exporter (phụ) | v1.12.1 | 14/07/2026 | prometheus/node_exporter | |
| postgres_exporter (phụ) | v0.20.1 | 08/07/2026 | prometheus-community/postgres_exporter | |
| mongodb_exporter (phụ) | v0.54.0 | 22/10/2026 | percona/mongodb_exporter | |
| redis_exporter (phụ) | v1.97.0 | 04/11/2026 | oliver006/redis_exporter | ✓ |
| Jaeger (phụ) | v2.23.0 | 05/11/2026 | jaegertracing/jaeger | ✓ |
| VictoriaMetrics (phụ) | v1.156.0 | 09/11/2026 | VictoriaMetrics/VictoriaMetrics | ✓ |

**Đã ghim sẵn trong FlashTicket** [CODE, MÁY]: Spring Boot 4.1.1; Spring Cloud 2025.1.3; Java 21 (`eclipse-temurin:21-jre-alpine` theo digest); PostgreSQL 16.15; Redis 7.4.11-alpine; RabbitMQ 4.3.6-management; Keycloak 26.8.0; ngrok agent 3.39.13 theo digest. **MongoDB `mongo:7.0` trên máy 84 chạy theo tag, không theo digest** [MÁY `docker ps`]; bản nháp `~/flashticket` dùng `mongo:8` — hai bản lệch nhau.

---

## 6. Cấu hình then chốt (đề xuất, chưa kiểm)

### 6.1 Biến môi trường agent cho một service (ví dụ booking)

```text
JAVA_TOOL_OPTIONS=-javaagent:/otel/opentelemetry-javaagent.jar -XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC
OTEL_SERVICE_NAME=booking-service
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=exp,host.id=<id máy>,service.instance.id=booking-1
OTEL_EXPORTER_OTLP_ENDPOINT=http://<collector>:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_TRACES_SAMPLER=parentbased_always_on
OTEL_LOGS_EXPORTER=none
OTEL_METRIC_EXPORT_INTERVAL=10000
OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY=traceId
OTEL_INSTRUMENTATION_COMMON_LOGGING_SPAN_ID_KEY=spanId
```

- Tên biến dạng `OTEL_INSTRUMENTATION_COMMON_LOGGING_*` là cách viết biến môi trường của thuộc tính hệ thống trong README [CHƯA KIỂM agent nhận dạng này; kiểm ở H1, nếu không thì dùng `-Dotel.instrumentation.common.logging.trace-id-key=traceId`].
- `host.id` không chứa thông tin nhạy cảm (B16 §4).

### 6.2 Collector: hai pipeline tối thiểu (sửa 10/11/2026)

**Collector tại chỗ, chạy trên `exp-app`:**
- Receiver: `otlp` (nghe `127.0.0.1`), `filelog` (log container), `docker_stats`, `hostmetrics`, receiver DB.
- Processor: `memory_limiter`, `batch`, `resource` (gắn host), `filter` (bỏ span health check), lọc **loại trừ container của công cụ tiêm lỗi, k6, Toxiproxy** khỏi log và metric (PLAN §5).
- Exporter: `otlp` sang Collector trung tâm trên `exp-obs`, với `retry_on_failure` và `sending_queue` bật. Theo [README exporterhelper](https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/README.md): `retry_on_failure` mặc định bật, thử lại tối đa 300 giây; `sending_queue` mặc định bật, 1000 mục; hàng đợi đầy thì dữ liệu "typically dropped"; đặt `storage` (ví dụ `filestorage`) thì hàng đợi ghi ra đĩa và gửi tiếp sau khi tiến trình khởi động lại. Cấu hình hàng đợi lưu đĩa cần thiết khi `exp-obs` đặt ở máy xa, ngoài VPC (PLAN §3).

**Collector trung tâm, chạy trên `exp-obs`:**
- Receiver: `otlp` từ Collector tại chỗ.
- Connector: `spanmetrics`, `servicegraph` (đặt **trước** mọi bước lấy mẫu).
- Exporter: `otlphttp` → Prometheus, Loki; `otlp` → Tempo; `file` → thư mục lượt.

**Tự giám sát** (cả hai Collector): metric nội bộ ở cổng 8888 của mỗi Collector (`otelcol_receiver_refused_*`, `otelcol_exporter_send_failed_*`) [REPO `KE-HOACH` Phần B, dòng Công cụ].

---

## 7. Khi nào toàn bộ khuyến nghị cần xét lại

- Agent không chạy được với Spring Boot 4.1.1 ở H1 → chuyển phương án B §4.1, cần nhóm hệ thống sửa pom.
- Nhóm hệ thống không kịp cờ lỗi và Toxiproxy → danh mục kịch bản chỉ còn lỗi container; RQ5 thu hẹp, phải khai.
- Quota hoặc tín dụng không đủ hai máy 8 GiB cùng tài khoản → PLAN phương án P-B hoặc P-C.
- Minh cấm dữ liệu ra ngoài → bỏ Grafana Cloud, không ảnh hưởng nguồn chấm.

---

## 8. Câu kỹ thuật còn mở

| Câu | Vì sao chưa biết | Giải thích khả thi | Cách phân xử, chi phí | Kết luận phụ thuộc |
|---|---|---|---|---|
| Agent 2.33.1 chạy đúng với Boot 4.1.1 không | Chưa chạy; changelog nói Boot 4 chung | Chạy được; lỗi khởi động; thiếu span một thư viện | H1, 0,5–1 ngày | Toàn bộ §4.1 |
| Overhead agent trên 2 vCPU | Tài liệu không có số | Nhỏ; đủ gây nghẽn khi tải | So p95 có/không agent ở cùng tải, 2 giờ máy | Mức tải chiến dịch; báo cáo NV1 |
| RAM và dung lượng kho quan sát | Chưa đo | Vừa 8 GiB; không vừa | B2: chạy 1 giờ ở 2 mức tải | Số máy (PLAN §3) |
| MDC `traceId` của event-service đè agent không | Hai nguồn cùng khóa | Agent thắng; app thắng | H1: so `traceId` log với span | D5 ở event-service |
| `netem` với host network | Chưa thử | Tác động cả máy; tác động đúng loopback | Thử trên máy thực nghiệm, 30 phút | Kịch bản trễ mạng |
| Trễ giữa hai service Java qua Toxiproxy | Gọi qua Eureka, không qua URL tĩnh | Làm được nếu đổi đăng ký; không làm được | Đọc code gọi Feign/RestClient; 1–2 giờ | Kịch bản "trễ mạng giữa hai service" |
| Giới hạn API tìm kiếm Tempo 3.1.1 | Chưa đọc tài liệu API | — | Đọc tài liệu, 15 phút | Bộ đọc trực tuyến |

---

## 9. Nguồn web (truy cập 10/11/2026)

- GitHub Releases API, mẫu `https://api.github.com/repos/<owner>/<repo>/releases/latest`, cho mọi dòng §5.
- OTel Java instrumentation v2.33.1: [supported-libraries](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/v2.33.1/docs/supported-libraries.md); [CHANGELOG](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/v2.33.1/CHANGELOG.md) (bản 2.22.0, 2.23.0, 2.26.1); [logger-mdc-instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/v2.33.1/docs/logger-mdc-instrumentation.md); [logback-mdc README](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/v2.33.1/instrumentation/logback/logback-mdc-1.0/javaagent/README.md).
- Collector contrib v0.165.0, README từng thành phần: `https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.165.0/<thư mục>`.
- [Spring Boot Tracing (docs 4.1.2)](https://docs.spring.io/spring-boot/reference/actuator/tracing.html).
- [Tempo deployment](https://grafana.com/docs/tempo/latest/setup/deployment/); [Tempo 3.0 deployment modes](https://grafana.com/docs/tempo/v3.0.x/set-up-for-tracing/setup-tempo/plan/deployment-modes/); [Tempo upgrade](https://grafana.com/docs/tempo/latest/setup/upgrade/).
- [Prometheus OpenTelemetry guide](https://prometheus.io/docs/guides/opentelemetry/).
- [Grafana pricing](https://grafana.com/pricing/).
- [k6 v2.0.0 release](https://github.com/grafana/k6/releases/tag/v2.0.0).
- [Chaos Monkey for Spring Boot v4.0.0](https://github.com/codecentric/chaos-monkey-spring-boot/releases/tag/v4.0.0).
- [AWS Free plan](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html); [EC2 Free Tier usage](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html); [EC2 instance quotas](https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-quotas.html); [C7i](https://aws.amazon.com/ec2/instance-types/c7i/); [VPC pricing](https://aws.amazon.com/vpc/pricing/).
- GitHub Actions API: `https://api.github.com/repos/levanminh04/flash-ticket-platform/actions/workflows/cd.yml/runs`.
- GHCR: `https://ghcr.io/token?scope=repository:levanminh04/flash-ticket-platform/api-gateway:pull`, `https://ghcr.io/v2/levanminh04/flash-ticket-platform/api-gateway/tags/list`.
