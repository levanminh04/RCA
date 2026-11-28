# Mở rộng sang quan sát máy 84 (giai đoạn sau, không làm trong T-076)

Bản 1, 28/11/2026. Đầu ra SPEC T-076 bản 6 (tiêu chí xong 5). Nguồn: SPEC §"Mở rộng sang máy 84", LOG T-076 (đọc máy 84 lúc 05:07Z 27/11; kiểm cục bộ bản 3, bản 6, sau REVIEW-5), PR #17 @`f40b849` trên main `4d57225`.

## 1. Hiện trạng sau PR #17

- Image 8 service Spring có OpenTelemetry Java agent 2.33.1 (checksum ghim), **tắt cứng** bằng `env:` `OTEL_AGENT_ENABLED: "false"` trong `deployment.yaml` (7 service) và `statefulset.yaml` (Discovery). `env:` thắng ConfigMap/Secret (kiểm mô phỏng; K8s thật kiểm ở bước 7).
- ConfigMap 7 service có sẵn biến chỉ agent đọc: đích `http://otel-collector:4318` (OTLP/HTTP, Service trong cụm, **chưa có**), sampler 10 %, exemplar tắt, che 29 tên tham số (`q` + 28 `vnp_*`), thuộc tính RabbitMQ. Agent dùng khóa MDC mặc định `trace_id`/`span_id` như exp-app (REVIEW-5 N1).
- Log B16 chạy thật khi agent tắt: `environment=production`, `hostId` = tên node, `serviceVersion` = commit.
- File mẫu Secret không đổi so với main.

## 2. Việc khi bật (chỉ thêm, cùng vài sửa nhỏ đã biết)

| Loại | Việc | Ở đâu |
|---|---|---|
| **Thêm** | Collector 1 pod: Deployment, Service `otel-collector`, ConfigMap. Nhận OTLP/HTTP trong cụm; lọc như exp-app (`filter/health`, `transform/sanitize` xóa toàn bộ query); thêm xóa `exception.message`, lọc hoặc bỏ `exception.stacktrace`; nén; gửi obs qua TLS + token; hàng đợi gửi lại; không ghi dữ liệu thô ra file | FlashTicket `deploy/k8s/otel-collector/` (mới) |
| **Thêm** | Đường CD cho image dựng sẵn (Collector không phải service Maven/Node): `.github/services.json`, nhánh "image" trong `_deploy-service.yml`, tên Collector và quy tắc kiểm (không Eureka) trong `deploy-k8s-service.sh`, bộ kiểm CD | FlashTicket `.github/`, `deploy/scripts/` (nhóm duyệt) |
| **Thêm** | Secret token của Collector | file mẫu mới trong `deploy/k8s/examples/` |
| **Thêm** | Đường nhận trên obs: Collector + Prometheus riêng cho dữ liệu chạy thật, datasource và dashboard chạy thật, truy vấn Tempo thực nghiệm lọc `deployment.environment=exp`; tường lửa chỉ mở cho IP máy 84 | lab `observability/` (file mới); CA đã có ở `observability/tls/` và `/etc/flashticket-rca/production/` trên obs |
| **Thêm** | `SPRING_AUTOCONFIGURE_EXCLUDE` (Lettuce observation) ở gateway, booking, assistant | ConfigMap các service đó |
| **Thêm** | Biến chỉ agent đọc (`OTEL_*` như 7 service kia) nếu bật cả Discovery: ConfigMap Discovery hiện chỉ có `ENVIRONMENT`, chưa có khối `OTEL_*` | `deploy/k8s/discovery-server/configmap.yaml` |
| **Sửa nhỏ** | `OTEL_AGENT_ENABLED: "false"` → `"true"` cho từng service bật | `deployment.yaml` của service đó |
| **Sửa nhỏ** | Nâng giới hạn bộ nhớ của service bật agent (§3) | `deployment.yaml` (nhóm quyết RAM cụm) |

Không phải xóa file nào của Phần A.

## 3. Bộ nhớ

**Máy 84, chưa có agent** (đọc 05:07Z 27/11, chỉ đọc; trước khi main thêm HA cho Payment ngày 27/11):

| Node | RAM | Dùng | Requests | Limits |
|---|---|---|---|---|
| `ft84` (172.31.41.236) | 7,6 GiB | 4.293 Mi (55 %) | 2.188 Mi | 3.498 Mi |
| `server-1` (172.31.43.219) | 1,9 GiB | 1.104 Mi (57 %) | — | — (chỉ discovery) |
| `server-2` (172.31.44.164) | 3,7 GiB | 3.184 Mi (**83 %**) | 2.720 Mi (71 %) | 4.416 Mi (**115 %**) |

`ft84` còn chạy Docker ngoài cụm: PostgreSQL 444/2.048 MiB, MongoDB 277/512, RabbitMQ 86/1.024, Redis 4/256, frontend 4/64. Đĩa `/` dùng 88 % (còn 3,7 GiB).

Pod (dùng / giới hạn): booking 654/768 và 411/768 (2 bản), payment 689/768 và 368/768, ticket 580/768, keycloak 571/768, event 456/512, gateway 291/768, assistant 256/768, user 256/768, discovery 229/384. Lúc đọc, nhóm đang triển khai (nhiều pod tạo trong 04:33–05:07Z, payment có ReplicaSet mới lúc 05:07Z), nên đây chưa phải số nền ổn định.

**Phần agent thêm, đo trên laptop** (Booking, giới hạn 768 MiB, Compose, có request thử, không phải tải thật):

| Lượt | Agent tắt | Agent bật | Chênh |
|---|---|---|---|
| Bản 3 (`kiem-cuc-bo/README.md`) | 381 MiB | 499 MiB | +118 MiB |
| Bản 6 (`kiem-cuc-bo/ban-6/README.md`) | 386–417 MiB | 492 MiB | +75 … +106 MiB |
| Sau REVIEW-5 (`kiem-cuc-bo/sua-review-5/`) | 416 MiB | — | — |

Suy luận, **chưa kiểm**: với Booking, cộng mức tăng đo trên laptop (+75 … +118 MiB) vào bản 654 MiB trên 84 thì được ~729–772 MiB, sát hoặc vượt giới hạn 768 Mi. Mức tăng của Payment, Event và các service khác **chưa đo**; Payment (689/768) và Event (456/512) đã gần giới hạn nên là các service cần đo trước. `server-2` đã cam kết 115 % limits và dùng 83 %, nên nâng giới hạn cần nhóm xếp lại pod hoặc thêm RAM. Số laptop không dùng làm dự báo dưới tải. Từ 26–27/11 main thêm 2 pod cho Booking, Payment và đọc replica (PR #52–#58), nên phải đọc lại nền trước khi tính.

## 4. Điều kiện trước khi bật (OPEN)

| Điều kiện | Vì sao | Bằng chứng cần |
|---|---|---|
| Kiểm payload thô bằng bộ sentinel giả ở nguồn và ở bản ghi đầu tiên gửi ra ngoài cụm, gồm span event | agent gửi `url.query` (chỉ che 29 tên đã liệt kê; email, số điện thoại còn), `exception.message`, `exception.stacktrace` (bản 6 `bat-ghi-de`) | lượt sentinel trên cụm thử có Collector |
| Minh quyết Collector trong cụm có được coi là biên lọc của B16 §6 ("whitelist trước khi ghi/xuất") hay phải lọc trước khi rời tiến trình Java | B16 §6 đặt filter ở collector là lớp dự phòng | quyết định của Minh; nếu phải lọc trong Java: hạn chế instrumentation hoặc lọc trong mã |
| Đo bộ nhớ thật dưới tải của từng service bật agent | §3 chỉ có số laptop của Booking | lượt đo trên cụm thử hoặc 84 ngoài giờ |
| Phí AWS cho lượng gửi ra Internet (**chưa kiểm**) | trace/metric gửi từ AWS sang obs (Oracle) tính phí egress | ước lượng byte/phút từ lượt đo, nhân giá egress hiện hành |
| CD từ chối image mới khi service đang bật đọc replica (Booking, Event, Ticket, Payment) | guard "writer cùng digest" của `deploy-k8s-service.sh` (REVIEW-5 R2) | mọi lần bật agent đổi image/cấu hình qua CD đều cần lịch writer-only như lần merge PR #17 |
| Thứ tự MDC khi agent bật ở Event (`span_id` của agent so với `spanId` bộ lọc chép từ `traceparent`) | chỉ suy từ mã (REVIEW-5 R7) | một lượt Event bật agent, đọc log |

## 5. Việc không cần làm lại

- Bảng giữ/bỏ file, log B16, hook `rca-test`, CI kiểm B16: đã vào PR #17.
- CA và chứng chỉ server cho đường nhận trên obs: đã tạo (`observability/tls/`, `/etc/flashticket-rca/production/`).
- Cấu hình che tham số và tắt exemplar: đã có trong ConfigMap; chỉ cần Collector lọc phần còn lại.
