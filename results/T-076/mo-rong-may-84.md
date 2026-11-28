# Mở rộng sang quan sát máy 84 (giai đoạn sau, không làm trong T-076)

Bản 2, 28/11/2026, sửa theo Codex `REVIEW-7` R6–R8 (bản 1 xem lịch sử git). Đầu ra SPEC T-076 bản 6 (tiêu chí xong 5). Nguồn: SPEC §"Mở rộng sang máy 84", LOG T-076 (đọc máy 84 lúc 05:07Z 27/11; kiểm cục bộ bản 3, bản 6, sau REVIEW-5, sau REVIEW-6), PR #17 @`cd21f17` trên main `f0a5d30`.

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
| **Thêm** | Đường nhận trên obs: Collector + Prometheus riêng cho dữ liệu chạy thật, datasource Prometheus và Tempo riêng cho chạy thật, dashboard chạy thật; tường lửa chỉ mở cho IP máy 84 | lab `observability/` (file mới) |
| **Thêm** | Đường tin cậy TLS cho Collector trong cụm: CA **công khai** của đường nhận (mount/trust), tên kết nối khớp SAN của chứng chỉ server, exporter trỏ Secret token. Khóa riêng chỉ ở máy nhận | FlashTicket `deploy/k8s/otel-collector/` (cấu hình exporter); nguồn CA xem dưới bảng |
| **Thêm** | `SPRING_AUTOCONFIGURE_EXCLUDE` (Lettuce observation) ở gateway, booking, assistant | ConfigMap các service đó |
| **Thêm** | Biến chỉ agent đọc (`OTEL_*` như 7 service kia) nếu bật cả Discovery: ConfigMap Discovery hiện chỉ có `ENVIRONMENT`, chưa có khối `OTEL_*` | `deploy/k8s/discovery-server/configmap.yaml` |
| **Sửa file có sẵn** | Bộ kiểm tín hiệu đọc Tempo theo service/route, **không lọc môi trường** (`tests/signals/check_purchase_journey.py:107–119`): khi Tempo chung có trace của 84 thì thêm điều kiện `resource.deployment.environment = "exp"` (hoặc dùng Tempo riêng) cho các truy vấn thực sự dùng | lab `tests/signals/check_purchase_journey.py` |
| **Sửa file có sẵn** | Datasource Tempo thực nghiệm gắn `serviceMap` với `prometheus` thực nghiệm (`observability/grafana/provisioning/datasources/datasources.yaml:30–31`): datasource chạy thật phải gắn Prometheus chạy thật; kiểm số liệu exp và production không tính lẫn | lab `observability/grafana/provisioning/datasources/datasources.yaml` |
| **Sửa file có sẵn** | Script CD chỉ nhận 10 service đã liệt kê và image `ghcr.io/levanminh04/flash-ticket-platform/<service>@sha256:…` (`deploy-k8s-service.sh:9–10`): Collector dùng image upstream dựng sẵn cần nhánh riêng (tên service, nguồn image được duyệt, digest, không kiểm Eureka), giới hạn đúng service đó | FlashTicket `deploy/scripts/deploy-k8s-service.sh`, `.github/workflows/_deploy-service.yml` (nhóm duyệt) |
| **Sửa nhỏ** | `OTEL_AGENT_ENABLED: "false"` → `"true"` cho từng service bật | `deployment.yaml` của 7 service; **`statefulset.yaml`** của Discovery |
| **Sửa nhỏ** | Nâng giới hạn bộ nhớ của service bật agent nếu đo thấy cần (§3) | `deployment.yaml`; `statefulset.yaml` của Discovery (nhóm quyết RAM cụm) |

Không phải xóa file nào của Phần A.

**Nguồn CA.** `git ls-tree -r 94bb11e -- observability/tls` rỗng: thư mục `observability/tls/` chỉ có trên laptop (chưa theo dõi bằng git), nên clone lab không mang CA. Chứng chỉ server đã tạo trên obs (`/etc/flashticket-rca/production/`) là ghi nhận lịch sử, chưa chứng minh Collector mới tin đúng CA và tên. Khi bật: chọn một đường phân phối CA công khai có thể xác minh (ví dụ đưa CA công khai vào repo cùng sha256, hoặc bàn giao qua nhóm), đối chiếu SAN với tên Collector dùng để kết nối. Không cần cấp lại chứng chỉ chỉ vì đổi checkout.

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

Suy luận, **chưa kiểm**: với Booking, cộng mức tăng đo trên laptop (+75 … +118 MiB) vào bản 654 MiB trên 84 thì được ~729–772 MiB, sát hoặc vượt giới hạn 768 Mi. Mức tăng của Payment, Event và các service khác **chưa đo**; Payment (689/768) và Event (456/512) đã gần giới hạn nên là các service cần đo trước. Số laptop không dùng làm dự báo dưới tải.

Về sức chứa node: Kubernetes xếp pod theo **requests** so với phần có thể phân bổ của node, không theo limits ([Kubernetes, quản lý tài nguyên Pod và container](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)). `server-2` cam kết 115 % limits và dùng 83 % là **nguy cơ** áp lực RAM, không tự buộc dời pod hay thêm RAM khi đổi một limit. Ví dụ Payment ở PR có request 512Mi, limit 768Mi (`deploy/k8s/payment-service/deployment.yaml:49–52`): giữ request mà đỉnh thực còn chỗ thì có thể giữ bố trí; đỉnh thực hoặc rolling update gây áp lực thì mới cần dời hoặc tăng tài nguyên. Quyết RAM sau khi đo dưới tải và đo chỗ cho rollout (§4), không thay toàn cụm theo số laptop.

Nền đã đổi: 26–27/11 main thêm 2 pod cho Booking, Payment và đọc replica (PR #52–#58); 28/11 main `f0a5d30` (PR #59) tạm đưa HPA Booking/Payment về 1/1 (`git diff f40b849 cd21f17 -- deploy/k8s/{booking-service,payment-service}/hpa.yaml`). Đây là cấu hình nguồn, không phải số pod quan sát trên máy; phải đọc lại nền trước khi tính.

## 4. Điều kiện trước khi bật (OPEN)

| Điều kiện | Vì sao | Bằng chứng cần |
|---|---|---|
| Kiểm payload thô bằng bộ sentinel giả ở nguồn và ở bản ghi đầu tiên gửi ra ngoài cụm, gồm span event | agent gửi `url.query` (chỉ che 29 tên đã liệt kê; email, số điện thoại còn), `exception.message`, `exception.stacktrace` (bản 6 `bat-ghi-de`) | lượt sentinel trên cụm thử có Collector |
| Minh quyết Collector trong cụm có được coi là biên lọc của B16 §6 ("whitelist trước khi ghi/xuất") hay phải lọc trước khi rời tiến trình Java | B16 §6 đặt filter ở collector là lớp dự phòng | quyết định của Minh; nếu phải lọc trong Java: hạn chế instrumentation hoặc lọc trong mã |
| Đo bộ nhớ thật dưới tải của từng service bật agent | §3 chỉ có số laptop của Booking | lượt đo trên cụm thử hoặc 84 ngoài giờ |
| Phí AWS cho lượng gửi ra Internet (**chưa kiểm**) | trace/metric gửi từ AWS sang obs (Oracle) tính phí egress | ước lượng byte/phút từ lượt đo, nhân giá egress hiện hành |
| CD có thể từ chối khi service đang bật đọc replica (Booking, Event, Ticket, Payment) | guard reader của `deploy-k8s-service.sh` khác nhau theo service: Booking `writer_revision` so image, vị trí, HPA/PDB; Event so thêm env/ConfigMap; Ticket, Payment so manifest đã chuẩn hóa; trên main `f0a5d30` baseline reader phải là bản 2 Pod (REVIEW-5 R2, REVIEW-7 R8) | khi bật: khai trạng thái reader, digest và thay đổi thật của từng service bật; dùng writer-only khi guard của service đó yêu cầu. Không mặc định mọi đổi cấu hình đều cần lịch writer-only ở cả bốn |
| Thứ tự MDC khi agent bật ở Event (`span_id` của agent so với `spanId` bộ lọc chép từ `traceparent`) | chỉ suy từ mã (REVIEW-5 R7) | một lượt Event bật agent, đọc log |

## 5. Lọc dữ liệu: các nhánh (Minh quyết, điều kiện 2 ở §4)

B16 §6 yêu cầu whitelist trước khi ghi/xuất; filter ở Collector là lớp dự phòng. Kết quả cục bộ (`kiem-cuc-bo/ban-6/bat-ghi-de/phan-tich.txt`): các tên tham số đã liệt kê thành `REDACTED`, exemplar bằng 0, nhưng sentinel email/điện thoại vẫn có trong trace trước processor. Vì vậy ConfigMap hiện tại **chưa đủ** để bật:

- **Mặc định đề xuất (theo B16 hiện hành):** giữ agent tắt cho tới khi đường ở nguồn đáp ứng B16 (hạn chế instrumentation hoặc lọc trong tiến trình Java cho các trường cấm); Collector vẫn lọc dự phòng. Chi phí chỉnh instrumentation chưa có số; thử một service trên cụm thử khi được phép đủ để loại phương án không đạt cho service đó.
- **Nếu Minh/nhóm chấp nhận Collector trong cụm là biên lọc** cho một phạm vi trace cụ thể: ghi thẩm quyền quyết định, nơi đầu tiên dữ liệu được ghi/xuất (agent → Collector trong cụm, chưa rời cụm) và giới hạn; đối chiếu sentinel ở nguồn và ở bản ghi đầu tiên rời cụm, gồm span event (điều kiện 1 ở §4).

Quyết định này ảnh hưởng đường bật production, không ảnh hưởng demo trên exp-app.

## 6. Quay lại khi đã bật agent trên 84

- Công tắc cứng nằm trong workload: tắt lại bằng một revision/CD hợp lệ (`"true"` → `"false"`), không sửa tay trên cụm.
- Trước khi bật, ghi đích tắt đã biết cho từng service (revision, digest, `writer-baseline` nếu có) theo quy tắc mục Hoàn tác của PR #17 (`results/T-076/mo-ta-pr17.md`): `previous` được ghi sau mỗi lần phát, nên không mặc định digest trước đây còn là đích.
- Giữ đường nhận trên obs tới khi xác nhận service đã tắt (không còn gửi), rồi mới gỡ đường nhận nếu cần.
- Không đòi đổi bố cục repo, không thử trên 84 trong T-076.

## 7. Việc không cần làm lại

- Bảng giữ/bỏ file, log B16, hook `rca-test`, CI kiểm B16: đã vào PR #17.
- Chứng chỉ server cho đường nhận trên obs: đã tạo (`/etc/flashticket-rca/production/`); còn đường phân phối CA công khai (§2).
- Cấu hình che 29 tên tham số và tắt exemplar: đã có trong ConfigMap; phần còn lại theo §5.
