# Bảng giữ / bỏ / sửa từng file của PR #17 (T-076, bước 1, C1)

Lập ngày 26/11/2026. Chỉ đọc repo FlashTicket. **Chờ Minh duyệt bảng** trước bước 2.

## Mốc đã chốt

| Mục | Giá trị |
|---|---|
| `origin/main` | `f178870` (không đổi từ lúc soát SPEC) |
| `origin/rca/quan-sat-log` (PR #17) | `bb84d64` (không đổi) |
| merge-base | `d147d49` |
| Lệch | PR trước 10 commit, tụt 92 |
| Diff PR so với merge-base | 124 file (46 thêm, 78 sửa), +5.028/−214 |
| Xung đột khi ghép vào main | 13 file (`bang-file/xung-dot.txt`), đúng danh sách trong SPEC |
| File PR sửa mà main cũng đổi sau merge-base | 25 (`bang-file/main-doi.txt`), gồm 13 file xung đột; 12 file còn lại ghép tự động, vẫn đọc lại |

Lệnh: `git diff --name-status d147d49 bb84d64`; `git merge-tree --write-tree --name-only f178870 bb84d64`. Bảng chi tiết sinh bằng `bang-file/lap_bang.py` từ ba file đầu vào cùng thư mục; quy tắc phân loại nằm trong script.

## Tóm tắt

| Quyết định | Số file | Gồm |
|---|---|---|
| **Giữ** | 93 | Mã Java B16: 20 lớp quan sát (thêm/sửa), 24 file nghiệp vụ chỉ chèn log/telemetry (trong đó 6 DTO bỏ `@Valid` trùng, 3 file xung đột); 9 test (7 `ObservabilityTests` + 2 test cấu hình log, GOV-155); 10 file hook `rca-test`; 7 `application.yaml`; 4 `pom.xml`; 7 `.dockerignore`; 7 `.env.example` của service; 3 file chuẩn B16 (`log.schema.json`, `verify_logs.py`, `requirements.txt`); hunk `SERVICE_VERSION` trong `_deploy-service.yml`; `decision-register.md` (GOV-150..156) |
| **Sửa khi áp** | 17 | 7 Dockerfile (dựng trên Dockerfile main, chèn agent); 7 `docker-entrypoint.sh` (thêm CA qua biến môi trường); `_maven-verify.yml`, `detect-changes.sh` (B16 theo danh sách); `deploy/observability/README.md` (viết lại theo K8s) |
| **Bỏ** | 14 | 7 file `deploy/app/*` (Compose dự phòng; lab đã phủ cùng giá trị cho exp-app); `.env.example`, `.gitignore` gốc; Postgres (`docker-compose.postgresql.yml`, `00-business-databases.sh` đổi quyền, 2 file `90-erd-reader.sql`); `keycloak-spi/Dockerfile` (tracing nướng vào image production) |

Mã Java ngoài test: 44 file (16 thêm, 28 sửa). SPEC ghi "39 file nghiệp vụ" là số cũ; bước 5 đọc đủ 44.

## Điểm cần Minh xem kỹ khi duyệt

1. **Bỏ 7 file `deploy/app/*`.** Đây là Compose dự phòng của nhóm; main chạy K8s. exp-app dựng cấu hình từ các file này cộng file phủ lab. File phủ đã đặt đúng các giá trị PR thêm (bộ nhớ booking/event/payment 1g, discovery 768m, nhãn log cả 7 service), nên cấu hình hiệu lực exp-app không đổi. Pha 4 kiểm lại bằng `hieu_luc.py` như T-070.
2. **Bỏ Keycloak tracing** (`keycloak-spi/Dockerfile`, `deploy/app/keycloak.yml`, biến `KC_*` ở `.env.example` gốc). Lý do: `ENV KC_TRACING_ENABLED=true` trong image sẽ bật tracing Keycloak trên máy 84 mà không có đích gửi. Keycloak exp-app hiện không dùng (không có biến `KC_TRACING*`, SSH 26/11). Hệ quả: chưa có trace Keycloak ở cả hai nơi; muốn có thì là việc riêng.
3. **Bỏ phần Postgres** (log chẩn đoán, quyền đọc ERD). Đổi Postgres của nhóm nằm ngoài việc bật agent. exp-app có cấu hình Postgres riêng ở lab.
4. **Giữ `decision-register.md`** (GOV-150..156): lịch sử quyết định của Minh cho chính PR này; nhắc GOV-151 "phần a (build đa kiến trúc) do Sơn phụ trách" — main đã có build hai kiến trúc.
5. **6 DTO bỏ `@Valid` ở khai báo danh sách** (`Availability`, `OrderItemView`, `OrderView`, `Problem`, `PurchaseSnapshot`, `SalesConfiguration`): phần tử vẫn `@Valid`, nên vẫn kiểm từng phần tử; mục đích là tránh cảnh báo Hibernate Validator vào log. **Chưa kiểm** hành vi trên main mới; kiểm bằng test ở bước 4.

## Thêm khi dựng (không có trong PR, theo SPEC bản 3)

| File | Việc |
|---|---|
| `deploy/observability/b16-services.txt` (mới) | Danh sách 7 service có hợp đồng B16: discovery-server, api-gateway, user-service, event-service, ticket-service, booking-service, payment-service |
| `deploy/k8s/<svc>/configmap.yaml` (7: api-gateway, user, event, ticket, booking, payment, assistant) | `ENVIRONMENT=production`, `HOST_ID`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`, `OTEL_CA_PEM_B64`, `OTEL_TRACES_SAMPLER=parentbased_traceidratio` + `OTEL_TRACES_SAMPLER_ARG=0.1` (Q8), `OTEL_METRICS_EXPORTER=otlp`, `OTEL_LOGS_EXPORTER=none`; các biến telemetry PR đã dùng ở `.env.example` (`SPRING_AUTOCONFIGURE_EXCLUDE` cho Lettuce observation, `OTEL_INSTRUMENTATION_RABBITMQ_EXPERIMENTAL_SPAN_ATTRIBUTES`) nếu service có dùng; cấu hình lọc ở nguồn chọn ở bước 4 |
| `deploy/k8s/examples/<svc>.secret.env.example` (7) | Mục `# Optional`: `OTEL_AGENT_ENABLED=`, `OTEL_EXPORTER_OTLP_HEADERS=` |
| `services/assistant-service/{Dockerfile,docker-entrypoint.sh,.dockerignore}` | Agent như 6 service kia (Q2 (a)); không vào danh sách B16 |
| Mô tả PR #17 | Bảng này rút gọn; cách bật/tắt agent qua `ENV_<SVC>` + CD `restart` từng service; hoàn tác (SPEC C5, Q10) |

`discovery-server` có log B16 nhưng không bật agent lần đầu (không có Secret qua CD; SPEC C3b).

## Bảng từng file

<!-- SINH_TU_DANH_SACH: 124 file; Giữ 93, Sửa 17, Bỏ 14 -->
| # | Nhóm | File | PR | Quyết định | Lý do | Ghi chú ghép |
|---|---|---|---|---|---|---|
| 1 | Build | `services/booking-service/pom.xml` | sửa | **Giữ** | Thêm `opentelemetry-api` 1.59.0 (booking, payment, ticket) cho telemetry nghiệp vụ; profile `rca-test` (booking, event) chỉ khi build `-P rca-test` |  |
| 2 | Build | `services/event-service/pom.xml` | sửa | **Giữ** | Thêm `opentelemetry-api` 1.59.0 (booking, payment, ticket) cho telemetry nghiệp vụ; profile `rca-test` (booking, event) chỉ khi build `-P rca-test` | main cũng đổi, ghép tự động; đọc lại |
| 3 | Build | `services/payment-service/pom.xml` | sửa | **Giữ** | Thêm `opentelemetry-api` 1.59.0 (booking, payment, ticket) cho telemetry nghiệp vụ; profile `rca-test` (booking, event) chỉ khi build `-P rca-test` |  |
| 4 | Build | `services/ticket-service/pom.xml` | sửa | **Giữ** | Thêm `opentelemetry-api` 1.59.0 (booking, payment, ticket) cho telemetry nghiệp vụ; profile `rca-test` (booking, event) chỉ khi build `-P rca-test` |  |
| 5 | CI | `.github/scripts/detect-changes.sh` | sửa | **Sửa** | Quy tắc `deploy/observability/*` chọn mọi service trừ keycloak/frontend, gồm cả Assistant. Sửa: chỉ chọn service trong danh sách B16 | main cũng đổi, ghép tự động; đọc lại |
| 6 | CI | `.github/workflows/_deploy-service.yml` | sửa | **Giữ** | Diff ròng so với merge-base chỉ còn hunk truyền `SERVICE_VERSION={github.sha}` cho service Maven; build hai kiến trúc đã có ở main (dòng 79–82, 118). Cần để `service.version` = revision | main cũng đổi, ghép tự động; đọc lại |
| 7 | CI | `.github/workflows/_maven-verify.yml` | sửa | **Sửa** | Bước kiểm B16 chạy cho mọi service trừ keycloak; Assistant (main) sẽ đỏ (REVIEW R5). Sửa: chỉ chạy cho service trong `deploy/observability/b16-services.txt`; service trong danh sách thiếu file mẫu = lỗi | main cũng đổi, ghép tự động; đọc lại |
| 8 | Chuẩn B16 | `deploy/observability/README.md` | thêm | **Sửa** | Viết lại theo K8s: bỏ liên kết `deploy/rca-test`, `.local/rca-test`, danh sách file thời Compose; thêm cách bật/tắt agent qua `ENV_<SVC>` + CD `restart` |  |
| 9 | Chuẩn B16 | `deploy/observability/log.schema.json` | thêm | **Giữ** | Schema, bộ kiểm và phụ thuộc của kiểm log B16 trong CI |  |
| 10 | Chuẩn B16 | `deploy/observability/requirements.txt` | thêm | **Giữ** | Schema, bộ kiểm và phụ thuộc của kiểm log B16 trong CI |  |
| 11 | Chuẩn B16 | `deploy/observability/verify_logs.py` | thêm | **Giữ** | Schema, bộ kiểm và phụ thuộc của kiểm log B16 trong CI |  |
| 12 | Compose (dự phòng) | `deploy/app/README.md` | sửa | **Bỏ** | Thêm mục "Gói a–i" hướng dẫn vận hành thời Compose, trỏ `deploy/rca-test` đã bỏ. Lấy bản main. Cách bật agent ghi trong mô tả PR và `deploy/observability/README.md` | **xung đột** |
| 13 | Compose (dự phòng) | `deploy/app/_common.yml` | sửa | **Bỏ** | Nâng `mem_limit`/nhãn log cho Compose; main chạy K8s. Với exp-app, file phủ lab `test-environment/overrides/` đã đặt cùng giá trị (booking, event, payment 1g; discovery 768m; nhãn log cả 7), nên bỏ không đổi cấu hình hiệu lực |  |
| 14 | Compose (dự phòng) | `deploy/app/booking-service.yml` | sửa | **Bỏ** | Nâng `mem_limit`/nhãn log cho Compose; main chạy K8s. Với exp-app, file phủ lab `test-environment/overrides/` đã đặt cùng giá trị (booking, event, payment 1g; discovery 768m; nhãn log cả 7), nên bỏ không đổi cấu hình hiệu lực |  |
| 15 | Compose (dự phòng) | `deploy/app/discovery-server.yml` | sửa | **Bỏ** | Nâng `mem_limit`/nhãn log cho Compose; main chạy K8s. Với exp-app, file phủ lab `test-environment/overrides/` đã đặt cùng giá trị (booking, event, payment 1g; discovery 768m; nhãn log cả 7), nên bỏ không đổi cấu hình hiệu lực |  |
| 16 | Compose (dự phòng) | `deploy/app/event-service.yml` | sửa | **Bỏ** | Nâng `mem_limit`/nhãn log cho Compose; main chạy K8s. Với exp-app, file phủ lab `test-environment/overrides/` đã đặt cùng giá trị (booking, event, payment 1g; discovery 768m; nhãn log cả 7), nên bỏ không đổi cấu hình hiệu lực |  |
| 17 | Compose (dự phòng) | `deploy/app/keycloak.yml` | sửa | **Bỏ** | Bật log JSON và tracing native cho Keycloak, nâng bộ nhớ. Keycloak exp-app (`ft-local/keycloak:arm64-776d9c9e`) không có biến `KC_TRACING*`/`KC_LOG_CONSOLE*` (SSH 26/11): không dùng; ngoài phạm vi | main cũng đổi, ghép tự động; đọc lại |
| 18 | Compose (dự phòng) | `deploy/app/payment-service.yml` | sửa | **Bỏ** | Nâng `mem_limit`/nhãn log cho Compose; main chạy K8s. Với exp-app, file phủ lab `test-environment/overrides/` đã đặt cùng giá trị (booking, event, payment 1g; discovery 768m; nhãn log cả 7), nên bỏ không đổi cấu hình hiệu lực | **xung đột** |
| 19 | Cấu hình gốc | `.env.example` | sửa | **Bỏ** | Chẩn đoán PostgreSQL và tracing Keycloak cho Compose cũ; ngoài phạm vi agent máy 84; Postgres/Keycloak của exp-app cấu hình ở lab | main cũng đổi, ghép tự động; đọc lại |
| 20 | Cấu hình gốc | `.gitignore` | sửa | **Bỏ** | `/.local/rca-test/` thuộc bản nháp `deploy/rca-test` đã chuyển sang repo lab |  |
| 21 | Cấu hình log | `infrastructure/api-gateway/src/main/resources/application.yaml` | sửa | **Giữ** | Log JSON logstash, customizer `LogFields`, máy in stacktrace an toàn, mức log (B16) | main cũng đổi, ghép tự động; đọc lại |
| 22 | Cấu hình log | `infrastructure/discovery-server/src/main/resources/application.yaml` | sửa | **Giữ** | Log JSON logstash, customizer `LogFields`, máy in stacktrace an toàn, mức log (B16) |  |
| 23 | Cấu hình log | `services/booking-service/src/main/resources/application.yaml` | sửa | **Giữ** | Log JSON logstash, customizer `LogFields`, máy in stacktrace an toàn, mức log (B16) | main cũng đổi, ghép tự động; đọc lại |
| 24 | Cấu hình log | `services/event-service/src/main/resources/application.yaml` | sửa | **Giữ** | Log JSON logstash, customizer `LogFields`, máy in stacktrace an toàn, mức log (B16) |  |
| 25 | Cấu hình log | `services/payment-service/src/main/resources/application.yaml` | sửa | **Giữ** | Log JSON logstash, customizer `LogFields`, máy in stacktrace an toàn, mức log (B16) |  |
| 26 | Cấu hình log | `services/ticket-service/src/main/resources/application.yaml` | sửa | **Giữ** | Log JSON logstash, customizer `LogFields`, máy in stacktrace an toàn, mức log (B16) |  |
| 27 | Cấu hình log | `services/user-service/src/main/resources/application.yaml` | sửa | **Giữ** | Log JSON logstash, customizer `LogFields`, máy in stacktrace an toàn, mức log (B16) | main cũng đổi, ghép tự động; đọc lại |
| 28 | Cấu hình service | `infrastructure/api-gateway/.env.example` | sửa | **Giữ** | Tài liệu biến cho chạy local/Compose (`OTEL_*`, ở booking/event thêm `FT_FAULT*`); K8s lấy từ ConfigMap/Secret ở bước 3. exp-app đặt `FT_FAULT*` ở `/opt/flashticket/env/{booking,event}-service.env` | main cũng đổi, ghép tự động; đọc lại |
| 29 | Cấu hình service | `infrastructure/discovery-server/.env.example` | sửa | **Giữ** | Tài liệu biến cho chạy local/Compose (`OTEL_*`, ở booking/event thêm `FT_FAULT*`); K8s lấy từ ConfigMap/Secret ở bước 3. exp-app đặt `FT_FAULT*` ở `/opt/flashticket/env/{booking,event}-service.env` |  |
| 30 | Cấu hình service | `services/booking-service/.env.example` | sửa | **Giữ** | Tài liệu biến cho chạy local/Compose (`OTEL_*`, ở booking/event thêm `FT_FAULT*`); K8s lấy từ ConfigMap/Secret ở bước 3. exp-app đặt `FT_FAULT*` ở `/opt/flashticket/env/{booking,event}-service.env` |  |
| 31 | Cấu hình service | `services/event-service/.env.example` | sửa | **Giữ** | Tài liệu biến cho chạy local/Compose (`OTEL_*`, ở booking/event thêm `FT_FAULT*`); K8s lấy từ ConfigMap/Secret ở bước 3. exp-app đặt `FT_FAULT*` ở `/opt/flashticket/env/{booking,event}-service.env` |  |
| 32 | Cấu hình service | `services/payment-service/.env.example` | sửa | **Giữ** | Tài liệu biến cho chạy local/Compose (`OTEL_*`, ở booking/event thêm `FT_FAULT*`); K8s lấy từ ConfigMap/Secret ở bước 3. exp-app đặt `FT_FAULT*` ở `/opt/flashticket/env/{booking,event}-service.env`. Xung đột: ghép dòng `OTEL_*` vào bản main | **xung đột** |
| 33 | Cấu hình service | `services/ticket-service/.env.example` | sửa | **Giữ** | Tài liệu biến cho chạy local/Compose (`OTEL_*`, ở booking/event thêm `FT_FAULT*`); K8s lấy từ ConfigMap/Secret ở bước 3. exp-app đặt `FT_FAULT*` ở `/opt/flashticket/env/{booking,event}-service.env` |  |
| 34 | Cấu hình service | `services/user-service/.env.example` | sửa | **Giữ** | Tài liệu biến cho chạy local/Compose (`OTEL_*`, ở booking/event thêm `FT_FAULT*`); K8s lấy từ ConfigMap/Secret ở bước 3. exp-app đặt `FT_FAULT*` ở `/opt/flashticket/env/{booking,event}-service.env` | main cũng đổi, ghép tự động; đọc lại |
| 35 | Hook tiêm lỗi | `services/booking-service/src/rca-test/java/com/flashticket/booking_service/testing/RcaFaults.java` | thêm | **Giữ** | Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1) |  |
| 36 | Hook tiêm lỗi | `services/booking-service/src/rca-test/java/com/flashticket/booking_service/testing/RcaFaultsWebConfig.java` | thêm | **Giữ** | Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1) |  |
| 37 | Hook tiêm lỗi | `services/booking-service/src/rca-test/resources/application-rca-test.yaml` | thêm | **Giữ** | Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1) |  |
| 38 | Hook tiêm lỗi | `services/booking-service/src/rca-test/test-java/com/flashticket/booking_service/RcaFaultsTests.java` | thêm | **Giữ** | Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1) |  |
| 39 | Hook tiêm lỗi | `services/booking-service/src/rca-test/test-java/com/flashticket/booking_service/RcaFaultsWebConfigTests.java` | thêm | **Giữ** | Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1) |  |
| 40 | Hook tiêm lỗi | `services/event-service/src/rca-test/java/com/flashticket/event_service/testing/RcaFaults.java` | thêm | **Giữ** | Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1) |  |
| 41 | Hook tiêm lỗi | `services/event-service/src/rca-test/java/com/flashticket/event_service/testing/RcaFaultsWebConfig.java` | thêm | **Giữ** | Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1) |  |
| 42 | Hook tiêm lỗi | `services/event-service/src/rca-test/resources/application-rca-test.yaml` | thêm | **Giữ** | Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1) |  |
| 43 | Hook tiêm lỗi | `services/event-service/src/rca-test/test-java/com/flashticket/event_service/RcaFaultsTests.java` | thêm | **Giữ** | Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1) |  |
| 44 | Hook tiêm lỗi | `services/event-service/src/rca-test/test-java/com/flashticket/event_service/RcaFaultsWebConfigTests.java` | thêm | **Giữ** | Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1) |  |
| 45 | Image | `infrastructure/api-gateway/.dockerignore` | sửa | **Giữ** | Một dòng `!docker-entrypoint.sh` (GOV-156) |  |
| 46 | Image | `infrastructure/api-gateway/Dockerfile` | sửa | **Sửa** | Xung đột. Lấy Dockerfile main (giải nén theo lớp, digest ảnh nền của main, `curl`/`jq`), chèn: tải agent 2.33.1 có checksum, `docker-entrypoint.sh`, `SERVICE_VERSION`, `SERVICE_NAME`. Không lấy đổi digest ảnh nền của PR | **xung đột** |
| 47 | Image | `infrastructure/api-gateway/docker-entrypoint.sh` | thêm | **Sửa** | Giữ phần nhận diện tài nguyên và bật/tắt agent; thêm: giải `OTEL_CA_PEM_B64` ra `/tmp/otel-ca.pem`, đặt `OTEL_EXPORTER_OTLP_CERTIFICATE` (SPEC C3b). Vẫn `OTEL_LOGS_EXPORTER=none` |  |
| 48 | Image | `infrastructure/discovery-server/.dockerignore` | sửa | **Giữ** | Một dòng `!docker-entrypoint.sh` (GOV-156) |  |
| 49 | Image | `infrastructure/discovery-server/Dockerfile` | sửa | **Sửa** | Xung đột. Lấy Dockerfile main (giải nén theo lớp, digest ảnh nền của main, `curl`/`jq`), chèn: tải agent 2.33.1 có checksum, `docker-entrypoint.sh`, `SERVICE_VERSION`, `SERVICE_NAME`. Không lấy đổi digest ảnh nền của PR | **xung đột** |
| 50 | Image | `infrastructure/discovery-server/docker-entrypoint.sh` | thêm | **Sửa** | Giữ phần nhận diện tài nguyên và bật/tắt agent; thêm: giải `OTEL_CA_PEM_B64` ra `/tmp/otel-ca.pem`, đặt `OTEL_EXPORTER_OTLP_CERTIFICATE` (SPEC C3b). Vẫn `OTEL_LOGS_EXPORTER=none` |  |
| 51 | Image | `services/booking-service/.dockerignore` | sửa | **Giữ** | Một dòng `!docker-entrypoint.sh` (GOV-156) |  |
| 52 | Image | `services/booking-service/Dockerfile` | sửa | **Sửa** | Xung đột. Lấy Dockerfile main (giải nén theo lớp, digest ảnh nền của main, `curl`/`jq`), chèn: tải agent 2.33.1 có checksum, `docker-entrypoint.sh`, `SERVICE_VERSION`, `SERVICE_NAME`. Không lấy đổi digest ảnh nền của PR | **xung đột** |
| 53 | Image | `services/booking-service/docker-entrypoint.sh` | thêm | **Sửa** | Giữ phần nhận diện tài nguyên và bật/tắt agent; thêm: giải `OTEL_CA_PEM_B64` ra `/tmp/otel-ca.pem`, đặt `OTEL_EXPORTER_OTLP_CERTIFICATE` (SPEC C3b). Vẫn `OTEL_LOGS_EXPORTER=none` |  |
| 54 | Image | `services/event-service/.dockerignore` | sửa | **Giữ** | Một dòng `!docker-entrypoint.sh` (GOV-156) |  |
| 55 | Image | `services/event-service/Dockerfile` | sửa | **Sửa** | Xung đột. Lấy Dockerfile main (giải nén theo lớp, digest ảnh nền của main, `curl`/`jq`), chèn: tải agent 2.33.1 có checksum, `docker-entrypoint.sh`, `SERVICE_VERSION`, `SERVICE_NAME`. Không lấy đổi digest ảnh nền của PR | **xung đột** |
| 56 | Image | `services/event-service/docker-entrypoint.sh` | thêm | **Sửa** | Giữ phần nhận diện tài nguyên và bật/tắt agent; thêm: giải `OTEL_CA_PEM_B64` ra `/tmp/otel-ca.pem`, đặt `OTEL_EXPORTER_OTLP_CERTIFICATE` (SPEC C3b). Vẫn `OTEL_LOGS_EXPORTER=none` |  |
| 57 | Image | `services/payment-service/.dockerignore` | sửa | **Giữ** | Một dòng `!docker-entrypoint.sh` (GOV-156) |  |
| 58 | Image | `services/payment-service/Dockerfile` | sửa | **Sửa** | Xung đột. Lấy Dockerfile main (giải nén theo lớp, digest ảnh nền của main, `curl`/`jq`), chèn: tải agent 2.33.1 có checksum, `docker-entrypoint.sh`, `SERVICE_VERSION`, `SERVICE_NAME`. Không lấy đổi digest ảnh nền của PR | **xung đột** |
| 59 | Image | `services/payment-service/docker-entrypoint.sh` | thêm | **Sửa** | Giữ phần nhận diện tài nguyên và bật/tắt agent; thêm: giải `OTEL_CA_PEM_B64` ra `/tmp/otel-ca.pem`, đặt `OTEL_EXPORTER_OTLP_CERTIFICATE` (SPEC C3b). Vẫn `OTEL_LOGS_EXPORTER=none` |  |
| 60 | Image | `services/ticket-service/.dockerignore` | sửa | **Giữ** | Một dòng `!docker-entrypoint.sh` (GOV-156) |  |
| 61 | Image | `services/ticket-service/Dockerfile` | sửa | **Sửa** | Xung đột. Lấy Dockerfile main (giải nén theo lớp, digest ảnh nền của main, `curl`/`jq`), chèn: tải agent 2.33.1 có checksum, `docker-entrypoint.sh`, `SERVICE_VERSION`, `SERVICE_NAME`. Không lấy đổi digest ảnh nền của PR | **xung đột** |
| 62 | Image | `services/ticket-service/docker-entrypoint.sh` | thêm | **Sửa** | Giữ phần nhận diện tài nguyên và bật/tắt agent; thêm: giải `OTEL_CA_PEM_B64` ra `/tmp/otel-ca.pem`, đặt `OTEL_EXPORTER_OTLP_CERTIFICATE` (SPEC C3b). Vẫn `OTEL_LOGS_EXPORTER=none` |  |
| 63 | Image | `services/user-service/.dockerignore` | sửa | **Giữ** | Một dòng `!docker-entrypoint.sh` (GOV-156) |  |
| 64 | Image | `services/user-service/Dockerfile` | sửa | **Sửa** | Xung đột. Lấy Dockerfile main (giải nén theo lớp, digest ảnh nền của main, `curl`/`jq`), chèn: tải agent 2.33.1 có checksum, `docker-entrypoint.sh`, `SERVICE_VERSION`, `SERVICE_NAME`. Không lấy đổi digest ảnh nền của PR | **xung đột** |
| 65 | Image | `services/user-service/docker-entrypoint.sh` | thêm | **Sửa** | Giữ phần nhận diện tài nguyên và bật/tắt agent; thêm: giải `OTEL_CA_PEM_B64` ra `/tmp/otel-ca.pem`, đặt `OTEL_EXPORTER_OTLP_CERTIFICATE` (SPEC C3b). Vẫn `OTEL_LOGS_EXPORTER=none` |  |
| 66 | Keycloak | `services/keycloak-spi/Dockerfile` | sửa | **Bỏ** | `ENV KC_TRACING_ENABLED=true` nướng vào image Keycloak mà main triển khai lên máy 84: tracing bật mà không có endpoint. Ngoài phạm vi; exp-app không dùng |  |
| 67 | Kiểm B16 | `infrastructure/api-gateway/src/test/java/com/flashticket/api_gateway/ObservabilityTests.java` | thêm | **Giữ** | Sinh `target/b16-log-samples.jsonl` cho bước kiểm CI |  |
| 68 | Kiểm B16 | `infrastructure/discovery-server/src/test/java/com/flashticket/discovery_server/ObservabilityTests.java` | thêm | **Giữ** | Sinh `target/b16-log-samples.jsonl` cho bước kiểm CI |  |
| 69 | Kiểm B16 | `services/booking-service/src/test/java/com/flashticket/booking_service/ObservabilityTests.java` | thêm | **Giữ** | Sinh `target/b16-log-samples.jsonl` cho bước kiểm CI |  |
| 70 | Kiểm B16 | `services/event-service/src/test/java/com/flashticket/event_service/ObservabilityTests.java` | thêm | **Giữ** | Sinh `target/b16-log-samples.jsonl` cho bước kiểm CI |  |
| 71 | Kiểm B16 | `services/payment-service/src/test/java/com/flashticket/payment_service/ObservabilityTests.java` | thêm | **Giữ** | Sinh `target/b16-log-samples.jsonl` cho bước kiểm CI |  |
| 72 | Kiểm B16 | `services/ticket-service/src/test/java/com/flashticket/ticket_service/ObservabilityTests.java` | thêm | **Giữ** | Sinh `target/b16-log-samples.jsonl` cho bước kiểm CI |  |
| 73 | Kiểm B16 | `services/ticket-service/src/test/java/com/flashticket/ticket_service/TicketLocalConfigurationTests.java` | sửa | **Giữ** | Đổi assertion cấu hình log (GOV-155) |  |
| 74 | Kiểm B16 | `services/user-service/src/test/java/com/flashticket/user_service/BundledConfigurationTests.java` | sửa | **Giữ** | Đổi assertion cấu hình log (GOV-155) |  |
| 75 | Kiểm B16 | `services/user-service/src/test/java/com/flashticket/user_service/ObservabilityTests.java` | thêm | **Giữ** | Sinh `target/b16-log-samples.jsonl` cho bước kiểm CI |  |
| 76 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/dto/response/Availability.java` | sửa | **Giữ** | Bỏ `@Valid` trùng ở khai báo danh sách; phần tử vẫn `@Valid` nên vẫn kiểm từng phần tử (tránh cảnh báo Hibernate Validator vào log). Kiểm bằng test bước 4 |  |
| 77 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/dto/response/OrderItemView.java` | sửa | **Giữ** | Bỏ `@Valid` trùng ở khai báo danh sách; phần tử vẫn `@Valid` nên vẫn kiểm từng phần tử (tránh cảnh báo Hibernate Validator vào log). Kiểm bằng test bước 4 |  |
| 78 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/dto/response/OrderView.java` | sửa | **Giữ** | Bỏ `@Valid` trùng ở khai báo danh sách; phần tử vẫn `@Valid` nên vẫn kiểm từng phần tử (tránh cảnh báo Hibernate Validator vào log). Kiểm bằng test bước 4 | main cũng đổi, ghép tự động; đọc lại |
| 79 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/dto/response/Problem.java` | sửa | **Giữ** | Bỏ `@Valid` trùng ở khai báo danh sách; phần tử vẫn `@Valid` nên vẫn kiểm từng phần tử (tránh cảnh báo Hibernate Validator vào log). Kiểm bằng test bước 4 |  |
| 80 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/dto/snapshot/PurchaseSnapshot.java` | sửa | **Giữ** | Bỏ `@Valid` trùng ở khai báo danh sách; phần tử vẫn `@Valid` nên vẫn kiểm từng phần tử (tránh cảnh báo Hibernate Validator vào log). Kiểm bằng test bước 4 |  |
| 81 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/dto/snapshot/SalesConfiguration.java` | sửa | **Giữ** | Bỏ `@Valid` trùng ở khai báo danh sách; phần tử vẫn `@Valid` nên vẫn kiểm từng phần tử (tránh cảnh báo Hibernate Validator vào log). Kiểm bằng test bước 4 |  |
| 82 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/messaging/AcceptPaymentListener.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 83 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/messaging/BookingIssuanceResultListener.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 84 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/messaging/EventCancellationListener.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 85 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/messaging/SalesConfigurationListener.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 86 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/order/service/impl/OrderServiceImpl.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5). Xung đột: lấy logic main, chỉ chèn lệnh ghi log của PR | **xung đột** |
| 87 | Mã nghiệp vụ | `services/booking-service/src/main/java/com/flashticket/booking_service/promotion/service/impl/PromotionServiceImpl.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5). Xung đột: lấy logic main, chỉ chèn lệnh ghi log của PR | **xung đột** |
| 88 | Mã nghiệp vụ | `services/payment-service/src/main/java/com/flashticket/payment_service/controller/FinanceController.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 89 | Mã nghiệp vụ | `services/payment-service/src/main/java/com/flashticket/payment_service/messaging/PaymentMessageListener.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 90 | Mã nghiệp vụ | `services/payment-service/src/main/java/com/flashticket/payment_service/service/PaymentService.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 91 | Mã nghiệp vụ | `services/payment-service/src/main/java/com/flashticket/payment_service/service/impl/FinanceServiceImpl.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 92 | Mã nghiệp vụ | `services/payment-service/src/main/java/com/flashticket/payment_service/service/impl/PaymentSagaServiceImpl.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 93 | Mã nghiệp vụ | `services/payment-service/src/main/java/com/flashticket/payment_service/service/impl/RefundServiceImpl.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5). Xung đột: lấy logic main, chỉ chèn lệnh ghi log của PR | **xung đột** |
| 94 | Mã nghiệp vụ | `services/payment-service/src/main/java/com/flashticket/payment_service/worker/PaymentWorker.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 95 | Mã nghiệp vụ | `services/ticket-service/src/main/java/com/flashticket/ticket_service/application/TicketService.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 96 | Mã nghiệp vụ | `services/ticket-service/src/main/java/com/flashticket/ticket_service/messaging/TicketBusinessListeners.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 97 | Mã nghiệp vụ | `services/ticket-service/src/main/java/com/flashticket/ticket_service/worker/TicketDeliveryWorker.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 98 | Mã nghiệp vụ | `services/ticket-service/src/main/java/com/flashticket/ticket_service/worker/TicketOutboxPublisher.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 99 | Mã nghiệp vụ | `services/user-service/src/main/java/com/flashticket/user_service/identity/KeycloakAdminClient.java` | sửa | **Giữ** | Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5) |  |
| 100 | Mã quan sát | `infrastructure/api-gateway/src/main/java/com/flashticket/api_gateway/observability/LogFields.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 101 | Mã quan sát | `infrastructure/api-gateway/src/main/java/com/flashticket/api_gateway/observability/SafeStackTracePrinter.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 102 | Mã quan sát | `infrastructure/api-gateway/src/main/java/com/flashticket/api_gateway/web/CorrelationIdFilter.java` | sửa | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 103 | Mã quan sát | `infrastructure/discovery-server/src/main/java/com/flashticket/discovery_server/observability/LogFields.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 104 | Mã quan sát | `infrastructure/discovery-server/src/main/java/com/flashticket/discovery_server/observability/SafeStackTracePrinter.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 105 | Mã quan sát | `services/booking-service/src/main/java/com/flashticket/booking_service/observability/BusinessTelemetry.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 106 | Mã quan sát | `services/booking-service/src/main/java/com/flashticket/booking_service/observability/LogFields.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 107 | Mã quan sát | `services/booking-service/src/main/java/com/flashticket/booking_service/observability/RabbitTelemetry.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 108 | Mã quan sát | `services/booking-service/src/main/java/com/flashticket/booking_service/observability/SafeStackTracePrinter.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 109 | Mã quan sát | `services/booking-service/src/main/java/com/flashticket/booking_service/web/CorrelationFilter.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 110 | Mã quan sát | `services/event-service/src/main/java/com/flashticket/event_service/observability/EventLogCustomizer.java` | sửa | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 111 | Mã quan sát | `services/payment-service/src/main/java/com/flashticket/payment_service/observability/BusinessTelemetry.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 112 | Mã quan sát | `services/payment-service/src/main/java/com/flashticket/payment_service/observability/LogFields.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 113 | Mã quan sát | `services/payment-service/src/main/java/com/flashticket/payment_service/observability/RabbitTelemetry.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 114 | Mã quan sát | `services/payment-service/src/main/java/com/flashticket/payment_service/observability/SafeStackTracePrinter.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 115 | Mã quan sát | `services/ticket-service/src/main/java/com/flashticket/ticket_service/config/TicketLogFields.java` | sửa | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 116 | Mã quan sát | `services/ticket-service/src/main/java/com/flashticket/ticket_service/observability/BusinessTelemetry.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 117 | Mã quan sát | `services/ticket-service/src/main/java/com/flashticket/ticket_service/observability/RabbitTelemetry.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 118 | Mã quan sát | `services/user-service/src/main/java/com/flashticket/user_service/observability/SafeStackTracePrinter.java` | thêm | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 119 | Mã quan sát | `services/user-service/src/main/java/com/flashticket/user_service/observability/UserLogCustomizer.java` | sửa | **Giữ** | Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ) |  |
| 120 | Postgres | `deploy/docker-compose.postgresql.yml` | sửa | **Bỏ** | Bật log chẩn đoán Postgres (và đổi quyền file 644→755) cho Postgres của nhóm; ngoài phạm vi agent; exp-app có `test-environment/infra/docker-compose.rca-log.yml` riêng |  |
| 121 | Postgres | `deploy/postgres/00-business-databases.sh` | sửa | **Bỏ** | Bật log chẩn đoán Postgres (và đổi quyền file 644→755) cho Postgres của nhóm; ngoài phạm vi agent; exp-app có `test-environment/infra/docker-compose.rca-log.yml` riêng |  |
| 122 | Postgres | `services/event-service/database/90-erd-reader.sql` | thêm | **Bỏ** | Tạo quyền đọc ERD (`*_erd`); không thuộc quan sát, lab không dùng |  |
| 123 | Postgres | `services/payment-service/database/90-erd-reader.sql` | thêm | **Bỏ** | Tạo quyền đọc ERD (`*_erd`); không thuộc quan sát, lab không dùng |  |
| 124 | Tài liệu | `docs/project/decision-register.md` | sửa | **Giữ** | GOV-150..156: lịch sử quyết định của Minh cho PR; main dừng ở GOV-149, không trùng mã |  |

## Chênh bản 5 (SPEC bản 5–6, 27/11/2026)

Bảng trên giữ nguyên số và bằng chứng lúc Minh duyệt (26/11). Phần "Thêm khi dựng" đổi theo SPEC bản 6 (C2):

| File | Theo bảng (bản 3) | Theo bản 6 |
|---|---|---|
| `deploy/k8s/<svc>/configmap.yaml` (7) | Máy nhận HTTPS ở obs, `OTEL_CA_PEM_B64`, `SPRING_AUTOCONFIGURE_EXCLUDE` | Đích `http://otel-collector:4318` trong cụm; bỏ CA và biến Spring; thêm `OTEL_METRICS_EXEMPLAR_FILTER=always_off` và danh sách che `q` + 28 `vnp_*` |
| `deploy/k8s/<svc>/deployment.yaml` (7) | — | `env:` thêm `HOST_ID` = `spec.nodeName` và `OTEL_AGENT_ENABLED="false"` (tắt cứng) |
| `deploy/k8s/examples/<svc>.secret.env.example` (7) | Thêm `OTEL_AGENT_ENABLED`, `OTEL_EXPORTER_OTLP_HEADERS` | **Không đổi** (giữ bản main) |
| `*/docker-entrypoint.sh` (8) | Thêm giải CA từ `OTEL_CA_PEM_B64` | Không thêm (giữ đúng bản PR) |
| `services/booking-service/src/rca-test/…/RcaFaultsWebConfig.java` + test | Giữ | **Sửa** (Q1): không có bean `RcaFaults` thì không đăng ký interceptor; thêm 1 test |

Nhánh local: 7 commit trên `f178870`, 129 file so với main (`git diff --stat f178870 HEAD`).

## Rebase lên main `6b77144` (27/11/2026)

Main tiến `f178870` → `6b77144` (22 commit của nhóm) trước khi push. Rebase 7 commit, giữ bản cũ ở nhánh local `rca/quan-sat-log-f178870`.

- `git range-diff f178870..rca/quan-sat-log-f178870 origin/main..HEAD`: 5 commit trùng nội dung; 2 commit chỉ đổi dòng ngữ cảnh (`.env.example` của Ticket; dòng `SPRING_APPLICATION_JSON` cạnh khối `OTEL_*` trong ConfigMap Event, Ticket).
- 2 xung đột mới, `deploy/k8s/{event,ticket}-service/configmap.yaml`: lấy dòng `SPRING_APPLICATION_JSON` của main (readiness thêm `db`), giữ khối `OTEL_*`. So với main, hai file chỉ thêm khối `OTEL_*`.
- 129 file so với main (`git diff --stat origin/main HEAD`), như trước rebase. File mẫu Secret vẫn trùng main (main thêm khóa replica cho booking, event, ticket; nhánh không đụng).
- Kết quả kiểm lại: `kiem-cuc-bo/ban-6-main-6b77144/README.md`.
