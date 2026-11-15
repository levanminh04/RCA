# T-063 — B16 bản 2: tự phản biện chuẩn quan sát và đề xuất (13/11/2026, Claude, luồng L4)

- **Trạng thái:** tài liệu **đề xuất** cho Minh. Chưa đưa vào repo FlashTicket. Không khuyến nghị nào dưới đây đã được kiểm trên máy, trừ khi ghi rõ "đã đo".
- **Đối tượng phản biện:** `B16-v0.1` (`D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md`, gọi tắt **B16**, số dòng theo bản đọc ngày 13/11).
- **Quy ước đường dẫn:** `FT:` = repo `D:/Project/flash-ticket-platform`, nhánh `rca/quan-sat-log`, cây làm việc ở commit `fba6bc8`. Bản đang chạy trên `exp-app` là `6b21ed55`. Đã kiểm: `deploy/rca-test/compose.yml`, `deploy/Dockerfile.integration-java21` không khác giữa hai commit. Thư mục `deploy/k8s/`, `deploy/k3s/` chỉ có ở `fba6bc8` (29 file mới), chưa triển khai.
- **Dữ kiện dùng lại, không đo lại:** [`span-goc/PHAN-TICH.md`](span-goc/PHAN-TICH.md), [`ca-nen/PHAN-TICH.md`](ca-nen/PHAN-TICH.md), [`cpu-book/PHAN-TICH.md`](cpu-book/PHAN-TICH.md), [`quan-sat/bang-huong-tin-hieu.md`](quan-sat/bang-huong-tin-hieu.md), [`quan-sat/thay-doi-may.md`](quan-sat/thay-doi-may.md) (TD-01..03), `results/T-062/kiem-du-lieu/bao-cao-B1.md` (R-01..R-10), `results/T-040/yeu-cau-quan-sat-p9.md`.
- **Cấu hình `exp-obs` ngoài Prometheus** (Collector trung tâm, Loki, Tempo) đọc từ bản chép công khai của T-058 (`results/T-058/dem-2026-11-10/config-public/obs/`, 10/11). TD-01 xác nhận lại phần Loki không có compactor/retention và Tempo không khai `block_retention`. Phần còn lại (dimension của service graph, `reject_old_samples_max_age`) **chưa kiểm** còn trùng bản đang chạy.
- **Đếm thêm trong lượt này** (chỉ đọc, laptop; lệnh ở Phụ lục A): thuộc tính span và bản ghi log của gói ca T-062 `a5539fba`; tên, nhãn, nhịp mẫu của 217 tên metric trong `results/T-062/ca/_metric-bo-sung/prometheus-tho-1794416400-1794450600.jsonl.gz`.

## 0. Tóm tắt

B16 bản 1 đặt đúng các nguyên tắc lớn: correlation bền khác traceId, một đường xuất mỗi tín hiệu, nhãn có giới hạn, retention tối thiểu. Phần yếu nằm ở chỗ chuẩn chỉ nói **nội dung** ("có metric pool", "có span quyết định"), không nói **hợp đồng dữ liệu**: tên, thuộc tính, phiên bản quy ước, đơn vị, nhịp, nhãn. Vì thiếu hợp đồng, triển khai lệch mà không ai phát hiện. Ví dụ: span DB dùng quy ước cũ còn cấu hình phía sau dùng tên mới (A1); metric nghiệp vụ đã viết trong mã nhưng không tới kho (B6). Phần triển khai chưa đạt chủ yếu đã được T-063 sửa một phần (TD-01..03). Phần còn lại cần lượt triển khai cuối và tải mua vé.

| Nhóm | Số điểm | Ảnh hưởng chính tới hướng T-064 |
|---|---|---|
| A. Thiếu đặc tả | 11 (A1–A11) | H1 (cạnh DB/queue), H3, H4, H6, H8 (adapter, log) |
| B. Có đặc tả, triển khai chưa đạt | 9 (B1–B9) | H2, H3, H4, H5, H6 |
| C. Chưa xác định cơ chế | 6 (C1–C6) | H2, H4, H5, H6 |

Đề xuất bản 2: 17 thay đổi (mục 4). Phần còn mở: mục 6.

---

## 1. Nhóm A — Thiếu đặc tả

Mỗi điểm: **Quan sát** (bằng chứng) → **Hệ quả** → **Đề xuất** (mã ĐX ở mục 4).

### A1. Không ghim phiên bản quy ước ngữ nghĩa (semantic conventions — semconv, bộ tên thuộc tính chuẩn của OTel) và phiên bản agent

- **Quan sát (đã đo).** Gói `a5539fba`: 69.647 span DB đều mang tên **cũ** `db.system`, `db.statement`; 63.561 có `db.name`; 52.192 có `db.operation`; 0 span có `db.system.name` hay `db.namespace`. Span HTTP thì dùng tên **ổn định** (`http.request.method` 19.496 span, `url.path` 12.760). Vậy cùng một agent (`telemetry.distro.version` = 2.33.1, có ở resource của mọi service kể cả Keycloak) phát hai thế hệ quy ước.
- Cấu hình phía sau lại dùng tên mới. Collector trung tâm: `service_graph.dimensions = ["db.system.name", "messaging.system"]` (`results/T-058/dem-2026-11-10/config-public/obs/collector.json`). Prometheus nâng `db.namespace` thành nhãn (`quan-sat/prometheus/prometheus-sau.json`). **Suy luận, chưa kiểm:** hai cấu hình này không có tác dụng với span DB hiện tại (nhãn rỗng). Cách kiểm: đếm nhãn `db_system_name` trên `traces_service_graph_*`.
- Resource dùng `deployment.environment` (Collector `resource/host`, `FT:services/booking-service/docker-entrypoint.sh:13`). Tên này đã bị thay bằng `deployment.environment.name` trong semconv. Loki chỉ nâng tên mới thành nhãn theo mặc định.
- Rủi ro sắp tới: theo blog OTel về Java agent 3.0, quy ước DB trở thành mặc định ổn định, metric pool đổi tên và đổi đơn vị ms → s, instrumentation Hibernate mặc định **tắt**. Hibernate chính là nguồn của 30.946 span gốc Keycloak (`span-goc/PHAN-TICH.md` §1). Nâng agent mà không ghim sẽ làm mất nhóm span này và đổi tên kênh M1 đang đọc. Chưa kiểm: 3.0 đã phát hành chính thức chưa.
- **Hệ quả.** H1 (DB thành nút) và adapter M1 phụ thuộc tên thuộc tính. Không ghim thì so sánh giữa các đợt thu có thể gãy âm thầm.
- **Nguồn.** <https://opentelemetry.io/docs/specs/semconv/database/database-spans/> (biến `OTEL_SEMCONV_STABILITY_OPT_IN=database` hoặc `database/dup`); <https://opentelemetry.io/blog/2026/java-agent-3.0-preview>; <https://opentelemetry.io/docs/specs/semconv/registry/attributes/deployment/>.
- **Đề xuất:** ĐX-01.

### A2. Không có bảng thuộc tính span bắt buộc theo loại span

- **Quan sát.** B16 §5 (dòng 76–83) liệt kê span "quyết định" theo service. Không có danh sách thuộc tính bắt buộc cho span HTTP server/client, DB, message, job. T-040 phải tự định nghĩa R-01..R-04 và ghi "B16 … chưa liệt kê thuộc tính span bắt buộc" (`results/T-040/yeu-cau-quan-sat-p9.md`, dòng R-01, R-03, R-04).
- Đang đạt được là nhờ agent mặc định, không nhờ chuẩn: R-01 đạt (76.383 CLIENT có `server.address`), R-02 đạt (12.760/12.760 SERVER có `http.route`) (`bao-cao-B1.md` dòng 15–16). Span message chưa kiểm được (0 PRODUCER/CONSUMER trên tải đọc).
- **Hệ quả.** Không có tiêu chí nghiệm thu tự động. Một thay đổi cấu hình agent có thể bỏ thuộc tính mà không vi phạm chữ nào của B16.
- **Nguồn.** HTTP: <https://opentelemetry.io/docs/specs/semconv/http/http-spans/>; DB: như A1; message: <https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/> (B16 đã dẫn).
- **Đề xuất:** ĐX-02.

### A3. Metric không có tên, đơn vị, loại, nhịp thu; đường xuất metric ứng dụng chưa chốt

- **Quan sát (đã đo).** B16 §2 dòng 24 nói "Actuator/Micrometer → Prometheus cho application metric". Thực tế metric ứng dụng đến từ **agent OTel qua OTLP**: `http_server_request_duration_seconds_*`, `jvm_*`, `db_client_connections_*` có mặt; Actuator chỉ mở `health,info` (`FT:services/booking-service/src/main/resources/application.yaml:140-147`). Hai đường cùng được nhắc, không đường nào được chốt là đường duy nhất.
- Đơn vị lẫn lộn: `db_client_connections_wait_time_milliseconds_*` (ms) bên cạnh `http_server_request_duration_seconds_*` (s).
- Histogram HTTP có 15 bucket (1.590 chuỗi bucket / 106 chuỗi count), khớp bộ biên mặc định của semconv, bucket nhỏ nhất 5 ms. Thao tác nền chỉ lệch ~0,1 ms (`ca-nen/PHAN-TICH.md` §2) nằm hoàn toàn dưới bucket đầu. Metric HTTP không phân giải được mức này; chỉ span làm được.
- Nhịp: trung vị bước mẫu của mọi metric app trên kho là 10 s. Nhưng `FT:deploy/rca-test/compose.yml` không đặt `OTEL_METRIC_EXPORT_INTERVAL`; mặc định của SDK Java là 60.000 ms. T-058 đặt 10 s qua biến môi trường ngoài repo (`results/T-058/dem-2026-11-10/huong-dan-trien-khai.md:159`). Nhịp 10 s hiện nay vì thế phụ thuộc file env trên máy (xem A11).
- **Hệ quả.** Bộ đóng gói và M1 giả định nhịp 10 s. Triển khai lại từ repo (hoặc trên K3s) sẽ cho 60 s mà không vi phạm B16.
- **Nguồn.** <https://opentelemetry.io/docs/languages/java/configuration/> (`otel.metric.export.interval` mặc định 60000); <https://opentelemetry.io/docs/specs/semconv/http/http-metrics/> (biên bucket); <https://prometheus.io/docs/practices/naming/> (đơn vị cơ sở); <https://prometheus.io/docs/practices/histograms/>.
- **Đề xuất:** ĐX-03, ĐX-04.

### A4. Không định nghĩa "khỏe" theo route

- **Quan sát.** B16 không có SLI (service level indicator — chỉ số mức dịch vụ) nào. Gói ca T-062 đo "khỏe" theo service: p50, p90, 5xx, lưu lượng (`bang-huong-tin-hieu.md`, dòng H7: "`workload`/`error` theo service (không theo route)"). Kho đã có `http_route`, `error_type`, `http_response_status_code` trên `http_server_request_duration_seconds_*` (đã đo, danh sách nhãn).
- Endpoint health mang hai nghĩa khác nhau. Docker healthcheck gọi `/actuator/health` (`FT:deploy/rca-test/compose.yml:380`). K8s dùng `/actuator/health/liveness` và `/readiness` (`FT:deploy/k8s/booking-service/deployment.yaml:60,67,74`). Eureka gọi health indicator định kỳ vì `eureka.client.healthcheck.enabled: true` (`application.yaml:137-138`); đây chính là nguồn 1.652 span `*_db` gốc trên luồng `DiscoveryClient-InstanceInfoReplicator` (`span-goc/PHAN-TICH.md` §1).
- **Hệ quả.** H7 (tải tăng so với sự cố) cần phân biệt "lưu lượng tăng" với "lỗi tăng" theo route. Health check có phụ thuộc DB làm DB chậm lan thành "service không khỏe" ở Eureka.
- **Nguồn.** <https://docs.spring.io/spring-boot/reference/actuator/endpoints.html> (liveness không nên phụ thuộc hệ thống ngoài; readiness là lựa chọn có đánh đổi); <https://opentelemetry.io/docs/specs/semconv/http/http-metrics/>.
- **Đề xuất:** ĐX-07.

### A5. Không quy định thuộc tính tài nguyên nào phải thành nhãn Prometheus/Loki

- **Quan sát (đã đo, TD-02).** B16 §5 dòng 85 chỉ cấm ID nghiệp vụ làm nhãn. Không nói cái gì **phải** là nhãn. Bộ nhận `rabbitmq` và `postgresql` đặt tên queue/bảng ở thuộc tính tài nguyên. Prometheus không nâng nên mọi queue gộp thành 2 chuỗi, mọi bảng gộp thành 5 chuỗi; counter ghi đè nhau cho tốc độ âm (`ca-nen/PHAN-TICH.md` §2, "Phát hiện kèm"). Sau TD-02: 62 chuỗi `rabbitmq_message_current`, 153 chuỗi `postgresql_table_size_bytes` (`thay-doi-may.md` TD-02).
- Phía Loki: mặc định Loki nâng `service.instance.id` thành nhãn chỉ mục. Hiện vô hại vì log gắn tĩnh `<svc>-1`. Nếu sửa A9 (dùng UUID mỗi lần khởi động) thì thành nhãn nhiều giá trị.
- **Hệ quả.** Dữ liệu H1/H4 trước 21:35Z 12/11 không dùng được. Lỗi loại này lặp lại với mọi bộ nhận mới.
- **Nguồn.** <https://prometheus.io/docs/guides/opentelemetry/> ("mặc định Prometheus không nâng thuộc tính nào"); <https://grafana.com/docs/loki/latest/send-data/otel/> (danh sách 17 thuộc tính mặc định); <https://grafana.com/docs/loki/latest/get-started/labels/cardinality/> (B16 đã dẫn).
- **Đề xuất:** ĐX-06.

### A6. Không quy định cách lọc span health mà không để con mồ côi

- **Quan sát (đã đo).** Collector `exp-app` bỏ span có `http.route == "/actuator/health"` (`quan-sat/collector-exp-app/config-sau-da-che.json`, `processors.filter/health`). Lọc theo **từng span**: cha SERVER bị bỏ, con JDBC/Redis giữ lại → 92 span mồ côi ở Booking trên 9 ca (`span-goc/PHAN-TICH.md` §1, dòng cuối bảng). README của filter processor cảnh báo đúng hiện tượng này.
- Điều kiện lọc so khớp chính xác một route. Trên K8s, probe gọi `/actuator/health/liveness|readiness`. **Chưa kiểm:** agent gán `http.route` nào cho hai đường này; nếu khác `/actuator/health` thì bộ lọc không bắt.
- **Hệ quả.** R-09 bị nhiễu bởi mồ côi do lọc. Mồ côi do lọc và mồ côi do mất ngữ cảnh trông giống nhau trong dữ liệu.
- **Nguồn.** <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md> (mục Warnings, "Orphaned Telemetry"); <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/tailsamplingprocessor/README.md> (quyết định theo cả trace).
- **Đề xuất:** ĐX-08.

### A7. Log JSON B16 §4 không được ánh xạ sang mô hình log OTel

- **Quan sát (đã đo).** Gói `a5539fba`: 7.524 bản ghi log; 0 bản ghi có `severityNumber`/`severityText`; 0 có `traceId` ở cấp bản ghi. Trường `traceId`, `spanId`, `severity` của B16 chỉ nằm trong thuộc tính lồng `attributes.app` (7.500 bản ghi). R-06 đạt vì bộ kiểm đọc thân log, không vì hạ tầng hiểu liên kết (`bao-cao-B1.md` dòng 20).
- Thời điểm bản ghi lấy từ `docker.time` (Collector `json_parser` id `docker`), không từ trường `timestamp` của ứng dụng. B16 §4 dòng 52 yêu cầu thời điểm tại nguồn.
- **Hệ quả.** Grafana không nhảy log ↔ trace bằng cơ chế chuẩn. Khớp với `results/T-062/codex/g1-that-2/BAO-CAO.md`: 0 URL Loki ở bảng bằng chứng (`CHIEN-DICH-M1-FT.md` §2). Lọc theo mức lỗi ở Loki không dùng được trường chuẩn.
- **Nguồn.** <https://opentelemetry.io/docs/specs/otel/logs/data-model/> (TraceId, SpanId, SeverityNumber là trường cấp bản ghi); <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/types/trace.md>; <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/types/severity.md>.
- **Đề xuất:** ĐX-09.

### A8. Danh tính instance không có luật ổn định và luật nhất quán giữa ba tín hiệu

- **Quan sát.** B16 §4 dòng 54 chỉ nói "instance duy nhất mỗi process". Triển khai có ba cách khác nhau:
  - app: UUID ngẫu nhiên mỗi lần khởi động (`FT:services/booking-service/docker-entrypoint.sh:5`);
  - log: Collector gắn tĩnh `service.instance.id = <svc>-1` (filelog `add` operator);
  - Keycloak: `keycloak-1` cả ở trace.
  R-05 vì thế chỉ "một phần" (`bao-cao-B1.md` dòng 19, "Còn lệch: resource log mang ID tĩnh").
- Prometheus lấy `instance` từ `service.instance.id`. Mỗi lần tạo lại container sinh chuỗi mới. Đây là điều kiện lỗi adapter H8 ("container tạo lại", `bang-huong-tin-hieu.md`).
- `HOST_ID: local-docker` trong `FT:deploy/rca-test/compose.yml` (7 service, ví dụ dòng 354), rồi bị Collector ghi đè `host.id=exp-app` (`resource/host`, `action: upsert`). Giá trị đúng trên một máy, nhưng do Collector quyết, không do triển khai.
- **Nguồn.** <https://opentelemetry.io/docs/specs/semconv/resource/service/> (duy nhất theo `service.namespace, service.name`; UUID ngẫu nhiên mặc định, UUID v5 nếu cần ổn định); <https://prometheus.io/docs/guides/opentelemetry/> (ánh xạ `job`/`instance`).
- **Đề xuất:** ĐX-10.

### A9. B16 §3 chỉ nói scheduler nghiệp vụ; không nói tác vụ nền của thành phần không do nhóm viết

- **Quan sát (đã đo).** B16 §3 dòng 40 yêu cầu mỗi lần xử lý scheduler tạo trace riêng. Job Spring của nhóm đạt (36.287 span `spring-scheduling`). Các tác vụ nền khác làm gốc trace mà B16 không phân loại: Keycloak Hibernate 30.946, JDBC Keycloak/JGroups 1.770, JDBC `*_db` Spring từ Eureka/Hikari 1.652, HTTP Eureka 2.160 + 1.080, Redis `INFO` 360, Mongo 360 (`span-goc/PHAN-TICH.md` §1).
- Các span này là nguồn của "thao tác nền dịch ~0,1 ms" gây cờ ở ca bình thường (`ca-nen/PHAN-TICH.md` §3).
- **Hệ quả.** H6 cần biết span nào là thao tác nền. Hiện chỉ suy được từ `thread.name`, là thuộc tính không ổn định giữa phiên bản thư viện.
- **Nguồn.** <https://opentelemetry.io/docs/zero-code/java/agent/annotations/> (`otel.instrumentation.methods.include` tạo span cho phương thức không cần sửa mã).
- **Đề xuất:** ĐX-11.

### A10. Không có cấu hình quan sát "dưới dạng mã" (config as code)

- **Quan sát.** Cấu hình thật trên `exp-app` nằm ngoài repo: `env-t062/*.env`, `compose-t062/*.yml`, `collector/config.json` (`results/T-062/ha-tang/thay-doi.md` dòng 7, 10, 12). Collector `exp-app` ghim ID container trong đường dẫn filelog (`config-sau-da-che.json`, 8 receiver `filelog/<svc>`). B16 §8 mục 4 yêu cầu manifest ghi cấu hình exporter/sampling, nhưng không yêu cầu cấu hình nằm trong kho mã có phiên bản.
- **Hệ quả.** Không dựng lại được cùng dữ liệu từ repo. Nhịp metric (A3) và nhãn log (A7, A8) đều phụ thuộc file trên máy.
- **Nguồn.** Không có tài liệu chính thức riêng cho điểm này. Lý do dựa trên bằng chứng nội bộ ở trên và R-07/R-10 (`results/T-040/yeu-cau-quan-sat-p9.md`).
- **Đề xuất:** ĐX-16.

### A11. Chuẩn gắn với cách chạy Docker; không có hợp đồng tín hiệu độc lập runtime

- **Quan sát.** Bản K3s mới (`FT:deploy/k8s/`, chỉ ở `fba6bc8`) không có biến `OTEL_*` nào (grep `OTEL_AGENT_ENABLED|otel` trong `deploy/k8s` và `deploy/k3s`: 0 file). Entrypoint mặc định `OTEL_AGENT_ENABLED=false` (`docker-entrypoint.sh:16`) → trên K3s **không có trace và metric ứng dụng**. Deployment chỉ có `requests.cpu: 200m`, không có giới hạn CPU (`deployment.yaml:38-43`) → không có throttling, cơ chế CPU-BOOK khác hẳn (`cpu-book/PHAN-TICH.md` §3 dựa trên quota 1 lõi).
- Nguồn metric hạ tầng cũng khác: `docker_stats` có throttling/restart (TD-03); trên K8s, `kubeletstats` **không** có throttling và restart; restart lấy từ `k8s_cluster`, throttling từ cAdvisor.
- **Hệ quả.** Một đợt thu trên K3s sẽ cho dữ liệu khác loại mà vẫn "đạt" B16 bản 1.
- **Nguồn.** <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/dockerstatsreceiver/documentation.md>; <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/kubeletstatsreceiver/documentation.md>; <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/k8sclusterreceiver/documentation.md>; <https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md>.
- **Đề xuất:** ĐX-13, ĐX-17.

---

## 2. Nhóm B — Có đặc tả, triển khai chưa đạt

| Mã | Mục B16 | Đặc tả | Triển khai (bằng chứng) | Trạng thái 13/11 |
|---|---|---|---|---|
| B1 | §6 dòng 97 | Log/trace nóng 7 ngày, metric 14 ngày | Prometheus 2 ngày → **30d + 40GB** từ 21:16Z 12/11 (TD-01). Loki: không bật compactor/retention → giữ vô hạn; `reject_old_samples_max_age: 48h` (`config-public/obs/loki.json`). Tempo: không khai `block_retention` → mặc định 336 h = 14 ngày. Cờ chạy Tempo chưa kiểm (`thay-doi-may.md` TD-01, "Ghi chú đọc kèm") | Metric đạt; log lệch (vô hạn, nguy cơ đầy đĩa); trace dài hơn chuẩn |
| B2 | §5 dòng 83 | Connection pool, queue ready/unacked, restart/OOM | Trên kho: pool có cho 4 service Hikari (`db_client_connections_*`, nhãn `pool_name`); Keycloak (Agroal), user-service (Mongo) **không**. Queue theo tên chỉ từ 21:35Z (TD-02). Restart từ 21:39Z (TD-03). OOM: không có nguồn. Gói ca: **không** chứa metric nào ở trên (7 kênh) (`bang-huong-tin-hieu.md` H3, H4, H5) | Thiếu ở gói; thiếu pool 2 thành phần; thiếu OOM |
| B3 | §7 dòng 106 | Một host nhiều node: gắn metric host với trace | Throttling CPU không thu tới 21:39Z (TD-03). PSI (pressure stall information — thời gian tiến trình chờ CPU) không có trên kho; phép thử CPU-BOOK phải đọc `/proc/pressure/cpu` bằng script riêng (`cpu-book/PHAN-TICH.md` §2) | Throttling đạt từ TD-03; PSI chưa |
| B4 | §2 dòng 24, §5 dòng 83 | Log JSON → collector → Loki; điểm quan sát hạ tầng | Không thu log Postgres, RabbitMQ, Redis, Mongo (8 receiver filelog: 7 service ứng dụng + Keycloak). Filelog ghim ID container → tạo lại container là mất log (KP-19, `results/T-062/ha-tang/thay-doi.md` dòng 12) | Chưa đạt; chờ cách A ở lượt triển khai cuối |
| B5 | §3 dòng 40 | Mỗi lần xử lý scheduler tạo trace riêng | Job Keycloak do nhóm đăng ký qua SPI (`OutboxDrainerTask`, `FT:services/keycloak-spi/.../RegistrationEventListenerFactory.java:84`) không có span bọc → 5.400 SELECT + 5.400 DELETE `OutboxEntryEntity` mỗi câu là một trace (`span-goc/PHAN-TICH.md` §1) | Chưa đạt; đề xuất bọc bằng cấu hình agent (span-goc §3.1) |
| B6 | §5 dòng 78–82 | Event: publish backlog/age; Booking: lock wait, expiry lag, outbox retry; Payment: Saga pending age… | Mã có gauge Micrometer (`event.outbox.backlog`, `event.outbox.oldest.age`, `FT:services/event-service/.../OutboxWorker.java:48-49`; `UserTelemetry.java`). Kho: 0/217 tên metric nghiệp vụ (grep `outbox|backlog|saga|expiry|reserve|refund|issuance`: chỉ trúng `redis_replication_backlog_*`). Nguyên nhân hợp lý: Actuator không mở endpoint metric (A3) và cầu nối Micrometer của agent 2.x tắt mặc định. Nguyên nhân chính xác: **chưa kiểm** (chưa đọc log khởi động agent) | Chưa đạt |
| B7 | §5 dòng 83, §7 dòng 108 | Theo dõi collector dropped/export failure | Metric có trên kho: `otelcol_exporter_send_failed_log_records_total`, `otelcol_processor_filter_spans_filtered_total`, `otelcol_receiver_refused_*` (đã đo). Không vào gói ca, không vào manifest. Đã xảy ra mất dữ liệu: lô > 4 MB bị Collector `exp-obs` từ chối 19:16–20:38Z 11/11 (`results/T-062/ha-tang/thay-doi.md` dòng 12). Batch processor không đặt `send_batch_max_size` (mặc định 0 = không giới hạn). Drop phía agent: chưa kiểm (`bao-cao-B1.md` R-08) | Một phần |
| B8 | §4 dòng 54–55, §7 dòng 106 | `instanceId`, `hostId` trên ba tín hiệu | Xem A8: log mang ID tĩnh; host do Collector ghi đè. R-05 "một phần" | Một phần |
| B9 | §2 dòng 24 | Java agent là đường mặc định | K3s manifest không bật agent, không có giới hạn CPU (A11). Chưa triển khai, nhưng đang nằm trên nhánh | Chưa đạt ở nhánh K3s |

**Nguồn cho nhóm B:** <https://grafana.com/docs/loki/latest/operations/storage/retention/> (không bật compactor retention thì log giữ vô hạn); <https://grafana.com/docs/tempo/latest/configuration/> (`block_retention` mặc định 336h); <https://prometheus.io/docs/prometheus/latest/storage/>; <https://opentelemetry.io/docs/collector/internal-telemetry/>; <https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md>; <https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/tag/v2.0.0> (cầu nối Micrometer tắt mặc định, bật bằng `OTEL_INSTRUMENTATION_MICROMETER_ENABLED=true`).

---

## 3. Nhóm C — Chưa xác định cơ chế

| Mã | Câu hỏi | Đã biết | Còn thiếu để phân xử | Ảnh hưởng |
|---|---|---|---|---|
| C1 | Ngữ cảnh trace có đi qua outbox → RabbitMQ → consumer, và callback VNPay không? Consumer dùng `traceparent` làm cha, làm link, hay bỏ? | Envelope có trường `traceparent` (`FT:services/booking-service/.../dto/message/Envelope.java:23`, `entity/OutboxMessage.java:48`). Agent RabbitMQ cũng tự truyền header. 0 span PRODUCER/CONSUMER trên tải đọc (R-04 chưa kiểm, R-09 chưa phân xử) | Gói ca từ tải mua vé; chạy lại `span-goc/phan_loai.py` để đếm CONSUMER gốc và mồ côi trên đường Saga; đọc mã consumer xem nguồn ngữ cảnh. Có thể có **hai** nguồn ngữ cảnh (header agent và trường envelope) cho cùng bản tin | H4, R-04, R-09 |
| C2 | Đợt Keycloak `DELETE OutboxEntryEntity` [t+60, t+240) và xu hướng tăng ở outbox/issuance là do gì? | Có cấu trúc thời gian, < 0,2 ms, CPU/GC Keycloak và CPU Postgres không đổi (`ca-nen/PHAN-TICH.md` §2–3) | Metric Postgres theo bảng (đã có từ TD-02); log Postgres (autovacuum, chờ khóa) — chưa thu (B4); kích thước bảng theo thời gian | H6 |
| C3 | Cơ chế "cụm CFS": Booking chiếm cả hai lõi đầu mỗi chu kỳ 100 ms rồi bị throttle | Suy từ throttle 84% chu kỳ + PSI gấp ~3 lần (`cpu-book/PHAN-TICH.md` §2–3) | Quan sát trực tiếp lịch CPU (`perf sched` hoặc `schedstat`); PSI theo cgroup từng container. Trên K3s không có giới hạn CPU (A11) nên cơ chế không chuyển sang được | H2 |
| C4 | Prometheus tự khởi động lại 19:16Z 12/11 khi truy vấn nặng, `OOMKilled=false` | Trùng truy vấn 9,5 giờ của `traces_span_metrics_duration_seconds_bucket` (`results/T-062/ca/_metric-bo-sung/SU-CO.md`) | `docker logs` trước 19:16:33Z, `dmesg`; giới hạn truy vấn của Prometheus. Đã giảm rủi ro (mem 3 GB, cắt khúc) nhưng chưa biết nguyên nhân | Độ tin cậy kho, bộ đóng gói |
| C5 | `docker_stats` báo gì khi container bị `pause`/`stop`? | Tài liệu bản hiện hành mô tả metric đếm container theo trạng thái (`container.state.status`). Bản Collector đang chạy chưa kiểm có metric này; chưa thử `docker pause` | Thử pause một container ngoài cửa sổ thí nghiệm, đọc chuỗi trên kho | H5 |
| C6 | Span DB gốc từ health indicator (Eureka) và Hikari có thay đổi khi DB chậm, và có làm M1 gắn cờ sai chỗ không? | Nguồn đã xác định (`span-goc` §1) | So các span này giữa ca nền và ca DB chậm (EVENT-DB-LAT) trên dữ liệu đã có | H1, H6 |

---

## 4. Đề xuất bản 2

Nguyên tắc chung: B16 bản 2 chia làm hai lớp. **Lớp hợp đồng tín hiệu** (tên, thuộc tính, đơn vị, nhãn, nhịp, phiên bản) độc lập cách chạy. **Lớp ánh xạ nguồn** cho từng runtime (Docker Compose, K3s), mỗi runtime phải qua cùng bộ kiểm R (`results/T-062/kiem-du-lieu/kiem-r.py`, mở rộng). Mọi cái giá dưới đây là **ước lượng, chưa đo**, trừ chỗ có số.

| Mã | Mục B16 | Thay đổi đề xuất | Lý do (điểm) | Nguồn | Cái giá / đánh đổi |
|---|---|---|---|---|---|
| ĐX-01 | §2 (thêm §2a "Phiên bản") | Ghim phiên bản agent và semconv trong chuẩn. Đặt `OTEL_SEMCONV_STABILITY_OPT_IN` rõ ràng: `database/dup` trong giai đoạn chuyển, sau đó `database`. Mọi cấu hình phía sau (service graph, nhãn Prometheus, adapter M1) dùng cùng thế hệ tên. Đổi thuộc tính tài nguyên `deployment.environment` → `deployment.environment.name`. Ghi phiên bản vào manifest lượt | A1 | semconv DB spans; blog Java agent 3.0; registry `deployment` | `dup` làm span DB nặng hơn (thêm khoảng 4–6 thuộc tính mỗi span, chưa đo). Adapter M1 phải đọc tên mới. **Chỉ đổi giữa hai đợt thu**, không đổi trong một đợt |
| ĐX-02 | §5 (thêm bảng) | Bảng thuộc tính bắt buộc theo loại span. HTTP server: `http.request.method`, `http.route`, `http.response.status_code`, `error.type` khi lỗi. HTTP client: thêm `server.address`, `server.port`. DB client: hệ DB, tên DB logic, loại thao tác, bảng/collection, `server.address`. Message: `messaging.system`, `messaging.destination.name`, loại thao tác, `messaging.message.id`, routing key RabbitMQ. Job: tên job, `code.function(.name)`. Bộ kiểm R tự kiểm bảng này | A2 | semconv HTTP spans, DB spans, messaging spans | Bảng phải cập nhật theo phiên bản semconv. Bảng chỉ có ích khi đi kèm bộ kiểm chạy được |
| ĐX-03 | §5 (thêm bảng metric) | Mỗi metric bắt buộc ghi: tên, đơn vị cơ sở (s, byte), loại (counter/gauge/histogram), nhãn cho phép, nhịp. Nhịp xuất 10 s ghim bằng `OTEL_METRIC_EXPORT_INTERVAL=10000` trong cấu hình có phiên bản. HTTP giữ biên bucket semconv; thao tác dưới 5 ms đo bằng span, không bằng metric (ghi rõ giới hạn) | A3 | Java SDK configuration; semconv HTTP metrics; Prometheus naming, histograms | Nhịp 10 s gấp 6 lần số mẫu so với 60 s. Thêm bucket nhỏ thì mỗi bucket là một chuỗi mới × số route × số mã trạng thái |
| ĐX-04 | §2 dòng 24 | Chốt **một** đường metric ứng dụng: agent OTLP. Metric Micrometer tùy chỉnh đi qua cầu nối của agent (`OTEL_INSTRUMENTATION_MICROMETER_ENABLED=true`). Sửa câu "Actuator/Micrometer → Prometheus" | A3, B6 | agent v2.0.0 release notes; Spring Boot metrics (OTLP) | Bật cầu nối có thể sinh metric Spring trùng nghĩa với metric agent → cần danh sách tắt. Phương án khác (Spring OTLP registry) thêm đường thứ hai, trái nguyên tắc một đường |
| ĐX-05 | §5 dòng 78–82 | Metric nghiệp vụ tối thiểu có tên cụ thể và phép kiểm "có mẫu trong cửa sổ": backlog/tuổi outbox mỗi service, tuổi Saga đang chờ, độ trễ expiry, đếm kết quả reserve | B6 | Như ĐX-03 | Ngoài Event, cần **thêm mã vào service** → vượt quyền chiến dịch ("dừng khi cần sửa code nghiệp vụ", `CHIEN-DICH-M1-FT.md` §6). Minh và nhóm hệ thống quyết |
| ĐX-06 | §5 dòng 85 | Allowlist nhãn. Prometheus: `service.name`→`job`, `service.instance.id`→`instance`, `host.id`, `deployment.environment.name`, `container.name` hoặc `k8s.pod.name`/`k8s.namespace.name`, và **mọi thuộc tính định danh thực thể của bộ nhận hạ tầng** (queue, vhost, schema, bảng, index, DB). Phép kiểm: số chuỗi ≥ số thực thể. Loki: nhãn chỉ `service.name`, `deployment.environment.name`, `severity`; instance để ở structured metadata | A5, A8 | Prometheus OTel guide; Loki OTel; Loki cardinality | Số chuỗi tăng theo số bảng/queue (đã đo: 153 chuỗi bảng, 62 chuỗi queue). Loki cần cấu hình `otlp_config` để bỏ `service.instance.id` khỏi nhãn mặc định |
| ĐX-07 | §5 (thêm mục "khỏe") | SLI theo route lõi (đăng nhập, đặt vé, thanh toán, xem vé): lưu lượng, tỷ lệ lỗi theo `error.type`/5xx, p90/p99 từ histogram. Route health không tính vào SLI. Liveness không phụ thuộc hệ thống ngoài; readiness có DB hay không phải ghi rõ lựa chọn. Health indicator gửi cho Eureka ghi rõ các phụ thuộc | A4 | Spring Boot probes; semconv HTTP metrics | Cần Minh duyệt danh sách route lõi. Ngưỡng "khỏe" phụ thuộc tải; nên lấy dải nền từng lượt, không chốt số tuyệt đối |
| ĐX-08 | §7 (thêm dòng) | Cấm lọc span theo từng span khi span đó có thể là cha. Ba phương án: (a) lọc theo **cả trace** (tail sampling, chính sách `drop`); (b) giữ span health, gắn dấu, bộ đọc RCA bỏ cả cây; (c) đưa nguồn gọi health ra ngoài cửa sổ thí nghiệm. Khuyến nghị cho dữ liệu nghiên cứu: (b) + (c), vì giữ dữ liệu thô. Điều kiện lọc phải phủ mọi đường health (`/actuator/health/**`) | A6 | filter processor README; tail sampling README | (a): tốn bộ nhớ, trễ quyết định mặc định 30 s, mọi span của một trace phải tới cùng một Collector (K3s nhiều Collector cần thêm lớp cân bằng tải). (b): tốn dung lượng Tempo, chưa đo. (c): ràng buộc lịch đầu dò |
| ĐX-09 | §4 (thêm "ánh xạ OTel") | Trường JSON B16 phải điền vào trường chuẩn của bản ghi log OTel: `traceId`/`spanId` → TraceId/SpanId, `severity` → SeverityNumber/Text, `timestamp` → Timestamp. Làm ở Collector (`trace_parser`, `severity_parser`, `time_parser` trên filelog) | A7 | OTel logs data model; stanza trace/severity | Thêm bước xử lý ở Collector, chi phí CPU nhỏ (chưa đo). Nếu sau này chuyển sang OTLP log appender của agent thì phải tắt filelog cho app để không trùng |
| ĐX-10 | §4 dòng 54–55 | `service.instance.id` = UUID mỗi lần khởi động process, **cùng một giá trị trên trace, metric, log**. Log lấy từ trường `instanceId` trong thân, Collector không gắn tĩnh. Thêm thuộc tính nối runtime: `container.id` (Docker) hoặc `k8s.pod.uid` (K3s). `host.id` lấy từ phát hiện tài nguyên, không ghi đè thủ công. Manifest xuất bảng service → instance → host theo thời gian | A8, B8 | semconv resource service; Prometheus OTel guide | Mỗi lần khởi động tạo chuỗi Prometheus mới (churn). Adapter phải gộp theo service khi cần. Lợi: H8 phát hiện được tạo lại container |
| ĐX-11 | §3 dòng 40 | Phân loại gốc trace hợp lệ: điểm vào, job của nhóm, **tác vụ định kỳ nhóm đăng ký vào thành phần ngoài** (phải có span bọc, ví dụ Keycloak outbox qua `OTEL_INSTRUMENTATION_METHODS_INCLUDE`), tác vụ nền thư viện (Hikari, Eureka, JGroups, health indicator: được làm gốc nhưng phải nhận diện được bằng scope và tên luồng). Ghi bảng phân loại này vào B16 | A9, B5 | Java agent annotations (`methods.include`) | Thêm số span tương đương số lượt chạy (outbox Keycloak ~1 lượt/giây). Tên lớp Keycloak đổi theo phiên bản → phải ghim image Keycloak. Lớp/phương thức cụ thể chưa kiểm (`span-goc/PHAN-TICH.md` §3.1) |
| ĐX-12 | §6 dòng 97 | Mỗi kho ghi **tối thiểu và trần**: Prometheus `retention.time` + `retention.size`; Loki bật compactor, `retention_enabled`, `retention_period`, `delete_request_store`; Tempo `block_retention`. Đo dung lượng/ngày ở tải mua vé và ghi vào manifest | B1 | Loki retention; Tempo configuration; Prometheus storage | Đĩa: Prometheus ~215 MB/ngày ở tải đọc (TD-01); Loki, Tempo chưa đo. Loki thêm compactor. Retention Loki không áp ngược cho log đã nạp |
| ĐX-13 | §5 dòng 83 | Metric hạ tầng theo **khái niệm**, kèm bảng nguồn từng runtime: CPU dùng / giới hạn / chu kỳ bị throttle / thời gian throttle; PSI CPU; bộ nhớ và OOM; restart; trạng thái chạy/dừng; mọi pool kết nối (cả Agroal, Mongo); queue ready/unacked/consumer theo queue; DB theo bảng. Docker: `docker_stats` (bật metric tùy chọn như TD-03). K3s: cAdvisor qua kubelet (`container_cpu_cfs_throttled_*`, `container_oom_events_total`), `k8s_cluster` (restart, ready) | B2, B3, A11 | docker_stats, kubeletstats, k8s_cluster docs; cAdvisor Prometheus docs | Tên metric khác nhau giữa runtime → adapter cần bảng ánh xạ có phiên bản. K3s cần quyền đọc kubelet. Pool Agroal/Mongo có thể không có instrumentation sẵn (chưa kiểm) |
| ĐX-14 | §2, §5 | Thu log **mọi** container, cả DB/broker, theo nhãn hoặc mẫu đường dẫn, không ghim ID. Docker: cách A (KP-19). K3s: filelog `/var/log/pods/...` + `container` operator + metadata K8s. Log Postgres có ích cho RCA: chờ khóa, autovacuum, câu lệnh chậm trên ngưỡng | B4, C2 | container operator; <https://www.postgresql.org/docs/current/runtime-config-logging.html> | Dung lượng log tăng (chưa đo). Nhiều định dạng log phải parse. Bật log Postgres chi tiết có thể làm chậm DB nếu ngưỡng quá thấp |
| ĐX-15 | §7 dòng 103, 108 | Metric Collector là **bắt buộc trong gói ca và manifest**: `otelcol_receiver_refused_*`, `otelcol_exporter_send_failed_*`, `otelcol_exporter_enqueue_failed_*`, kích thước/sức chứa queue, đếm span bị lọc. Đặt `send_batch_max_size` nhỏ hơn giới hạn nhận của Collector đích | B7 | Collector internal telemetry; batch processor README | Nhỏ. Lợi: R-08 kiểm được drop theo lượt thay vì "chưa kiểm" |
| ĐX-16 | §8 mục 4 | Mọi cấu hình quan sát (biến `OTEL_*`, Collector, Prometheus, Loki, Tempo, nhãn log) nằm trong repo, đã che bí mật, băm vào manifest. Cấm cấu hình chỉ tồn tại trên máy | A10 | (nội bộ, R-07/R-10) | Kỷ luật triển khai; mọi sửa nóng trên máy phải chép ngược về repo |
| ĐX-17 | §1 (thêm "phạm vi runtime") | B16 tách lớp hợp đồng và lớp ánh xạ runtime. Mỗi runtime mới phải chạy bộ kiểm R trước khi thu dữ liệu. Ghi rõ: quota CPU là một phần của điều kiện thí nghiệm (ô CPU phụ thuộc giới hạn CPU) | A11, B9 | Như ĐX-13 | Phải duy trì hai bảng ánh xạ và chạy bộ kiểm trên cả hai |

### Thứ tự gợi ý (theo phụ thuộc, để Minh cân nhắc)

1. **Trước đợt thu chính T-063, rẻ, trong quyền chiến dịch** (chưa kiểm hết, cần xác nhận phạm vi quyền): ĐX-06 (đã làm một phần ở TD-02), ĐX-09, ĐX-10 phần log, ĐX-14 cách A, ĐX-15, ĐX-08 (c), ĐX-11. Các việc này đều là cấu hình Collector/agent, không sửa mã nghiệp vụ.
2. **Ghim ngay, không đổi trong đợt thu:** ĐX-01 (ghi rõ đang dùng quy ước cũ cho DB), ĐX-03 (ghi 10 s vào cấu hình có phiên bản).
3. **Cần Minh và nhóm hệ thống:** ĐX-04, ĐX-05 (động tới service), ĐX-07 (route lõi), ĐX-12 Loki, ĐX-17 (K3s).

---

## 5. Đối chiếu độc lập cách chạy

| Khái niệm | Docker Compose (hiện tại) | K3s (nhánh `fba6bc8`, chưa triển khai) | Rủi ro nếu không ghi vào chuẩn |
|---|---|---|---|
| Bật agent | `OTEL_AGENT_ENABLED: true` trong compose | Không có biến → agent tắt | Mất toàn bộ trace và metric ứng dụng |
| Nhịp metric | 10 s qua env ngoài repo | Mặc định 60 s | Bộ đóng gói và M1 sai nhịp |
| Định danh instance | UUID app; log tĩnh `<svc>-1` | `POD_UID` có trong env (`deployment.yaml:49-52`) nhưng chưa dùng làm thuộc tính | R-05 lệch theo cách khác nhau |
| Log container | filelog ghim ID → cách A | `/var/log/pods` + `container` operator | Mất log khi tạo lại |
| CPU throttling | `docker_stats` tùy chọn (TD-03) | cAdvisor; **không có giới hạn CPU** nên không có throttling | Ô CPU đổi cơ chế |
| Restart / OOM | `docker_stats` restart; OOM không có | `k8s_cluster` restart; cAdvisor `container_oom_events_total` | H5 khác nguồn |
| Health | `/actuator/health` | `/actuator/health/liveness`, `/readiness` | Bộ lọc health không khớp |

---

## 6. Phần còn mở

- **Chưa đo:** overhead của tracing (B16 §7 dòng 109 yêu cầu đo); dung lượng/ngày của Loki và Tempo; kích thước tăng thêm khi bật `database/dup`; dung lượng nếu giữ span health (ĐX-08 b).
- **Chưa kiểm:** nhãn `db_system_name` trên metric service graph (A1); route agent gán cho `/actuator/health/liveness` (A6); nguyên nhân chính xác của B6 (log khởi động agent); Agroal/Mongo có metric pool qua agent không (ĐX-13); `container.state.status` có trong bản Collector đang chạy (C5); Java agent 3.0 đã phát hành chính thức chưa.
- **Cơ chế chưa phân xử:** C1–C6 ở mục 3. C1 và C2 cần tải mua vé và log hạ tầng; đây là điều kiện để R-04/R-09 có kết luận.
- **Quyết định cần Minh:** (1) có trình B16 bản 2 cho nhóm hệ thống không, và trình nguyên bản hay tách theo thứ tự ở mục 4; (2) ĐX-05 cần sửa mã service, vượt quyền chiến dịch; (3) danh sách route lõi cho ĐX-07; (4) chọn phương án lọc health (ĐX-08); (5) đợt thu chính T-063 giữ quy ước DB cũ (khuyến nghị, để so được với 9 ca T-062) hay chuyển trước khi thu.
- **Giới hạn của tài liệu này.** Đây là phản biện chuẩn và cấu hình, không phải đánh giá RCA. Việc các thay đổi giúp M1 tốt hơn chỉ trả lời được sau T-064. Nguồn tham khảo là tài liệu chính thức đọc ngày 13/11/2026; tài liệu có thể đổi theo phiên bản.

---

## 7. Danh sách nguồn ngoài (đọc 13/11/2026)

- OpenTelemetry semconv — DB spans: <https://opentelemetry.io/docs/specs/semconv/database/database-spans/>
- OpenTelemetry semconv — HTTP spans: <https://opentelemetry.io/docs/specs/semconv/http/http-spans/>
- OpenTelemetry semconv — HTTP metrics: <https://opentelemetry.io/docs/specs/semconv/http/http-metrics/>
- OpenTelemetry semconv — messaging spans: <https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/>
- OpenTelemetry semconv — resource `service`: <https://opentelemetry.io/docs/specs/semconv/resource/service/>
- OpenTelemetry semconv — registry `deployment`: <https://opentelemetry.io/docs/specs/semconv/registry/attributes/deployment/>
- OpenTelemetry logs data model: <https://opentelemetry.io/docs/specs/otel/logs/data-model/>
- OpenTelemetry Java SDK configuration: <https://opentelemetry.io/docs/languages/java/configuration/>
- OpenTelemetry Java agent — annotations / `methods.include`: <https://opentelemetry.io/docs/zero-code/java/agent/annotations/>
- OpenTelemetry Java agent — tắt instrumentation: <https://opentelemetry.io/docs/zero-code/java/agent/disable/>
- OpenTelemetry Java agent v2.0.0 release notes: <https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/tag/v2.0.0>
- OpenTelemetry blog — Java agent 3.0 preview: <https://opentelemetry.io/blog/2026/java-agent-3.0-preview>
- Collector internal telemetry: <https://opentelemetry.io/docs/collector/internal-telemetry/>
- Collector filter processor: <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md>
- Collector tail sampling processor: <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/tailsamplingprocessor/README.md>
- Collector batch processor: <https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md>
- Stanza `container` operator: <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/operators/container.md>
- Stanza trace / severity parsing: <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/types/trace.md>, <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/types/severity.md>
- docker_stats receiver: <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/dockerstatsreceiver/documentation.md>
- kubeletstats receiver: <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/kubeletstatsreceiver/documentation.md>
- k8s_cluster receiver: <https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/k8sclusterreceiver/documentation.md>
- cAdvisor Prometheus metrics: <https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md>
- Prometheus — OpenTelemetry guide: <https://prometheus.io/docs/guides/opentelemetry/>
- Prometheus — storage: <https://prometheus.io/docs/prometheus/latest/storage/>
- Prometheus — naming: <https://prometheus.io/docs/practices/naming/>; histograms: <https://prometheus.io/docs/practices/histograms/>
- Loki — OpenTelemetry ingestion: <https://grafana.com/docs/loki/latest/send-data/otel/>
- Loki — retention: <https://grafana.com/docs/loki/latest/operations/storage/retention/>
- Loki — cardinality: <https://grafana.com/docs/loki/latest/get-started/labels/cardinality/>
- Tempo — configuration: <https://grafana.com/docs/tempo/latest/configuration/>
- Spring Boot — actuator endpoints / probes: <https://docs.spring.io/spring-boot/reference/actuator/endpoints.html>
- Spring Boot — metrics (OTLP): <https://docs.spring.io/spring-boot/reference/actuator/metrics.html>
- PostgreSQL — logging: <https://www.postgresql.org/docs/current/runtime-config-logging.html>

Đọc trực tiếp và xác nhận trong lượt này: semconv DB spans, HTTP metrics, resource service, registry deployment; Java SDK configuration; annotations; blog 3.0; Collector internal telemetry, filter, tail sampling, batch, container operator, docker_stats, kubeletstats, k8s_cluster; cAdvisor; Prometheus OTel guide; Loki OTel và retention; Tempo configuration; Spring Boot endpoints. Thông tin cầu nối Micrometer lấy từ kết quả tìm kiếm trỏ tới release notes v2.0.0, chưa mở trực tiếp trang release. Các trang còn lại (HTTP spans, logs data model, stanza trace/severity, Prometheus storage/naming/histograms, Spring metrics phần histogram, PostgreSQL logging) dẫn làm tài liệu chuẩn, chưa đọc lại từng câu trong lượt này.

---

## Phụ lục A — Lệnh đã chạy trong lượt này (chỉ đọc)

1. Thuộc tính span và resource, gói `a5539fba` (`results/T-062/ca/a5539fba/cases/a5539fba/raw-traces.jsonl`, 117 MB): Python đọc từng dòng OTLP JSON, đếm kind, khóa thuộc tính theo nhóm (khóa bắt đầu `db.` / `messaging.` / `http.`), khóa resource. Kết quả: 130.701 span (CLIENT 76.383, INTERNAL 41.558, SERVER 12.760); khóa DB: `db.system` 69.647, `db.statement` 69.647, `db.name` 63.561, `db.operation` 52.192, `db.sql.table` 40.988, không có `db.system.name`/`db.namespace`; `db.statement` có hằng số dạng `= '…'` hoặc số ≥ 3 chữ số: 0/69.647 (agent đã che tham số).
2. Bản ghi log cùng gói (`raw-logs.jsonl`): 7.524 bản ghi (api-gateway 6.000, payment 900, ticket 600, keycloak 24); khóa cấp bản ghi chỉ có `attributes`, `body`, `observedTimeUnixNano`, `timeUnixNano`; `severityNumber` = None ở 7.524; `traceId` cấp bản ghi: 0; `attributes.app.traceId`: 7.500.
3. Metric xuất (`results/T-062/ca/_metric-bo-sung/prometheus-tho-1794416400-1794450600.jsonl.gz`): mỗi tên metric → số chuỗi, trung vị bước mẫu (`values[2][0] − values[1][0]`), tập nhãn. 217 tên; bước 10 s ở mọi metric app; grep `outbox|backlog|saga|expiry|reserve|refund|issuance|keycloak_|vendor_` → 1 tên (`redis_replication_backlog_first_byte_offset_bytes`). Bảng trung gian ở thư mục scratchpad của phiên, không lưu vào repo (dựng lại bằng lệnh này).
4. Repo FlashTicket (chỉ đọc): `git diff --stat 6b21ed55 fba6bc8 -- deploy/rca-test/compose.yml deploy/Dockerfile.integration-java21` → rỗng; `git ls-tree -r 6b21ed55 -- deploy/k8s deploy/k3s` → rỗng; grep `OTEL_AGENT_ENABLED|otel` trong `deploy/k8s deploy/k3s` → 0 file; grep `traceparent` trong `services/*/src/main` → Envelope, OutboxMessage (Booking), HttpEventSummaries (Event).
5. Không SSH vào máy nào, không chạy lệnh thay đổi.
