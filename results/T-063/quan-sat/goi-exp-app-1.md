# T-063 — Gói thay đổi `exp-app` lượt 1 (soạn 12/11/2026 22:13Z; **chưa áp** — chờ L1 ghi `results/T-062/tai-2/EXP-APP-XONG`)

Mục tiêu: dữ liệu đủ cho H1–H8 trước đóng băng (`bang-huong-tin-hieu.md` mục "Điều kiện đóng băng" 3–4). Một lượt đổi, một lần tạo lại container, kiểm ngay sau. Ghi biên bản vào `thay-doi-may.md` (TD-04…), hash trước/sau, cách hoàn tác.

## 1. Collector cách A (KP-19 T-058) — log mọi container, `service.name` từ dòng log

- **Docker:** thêm `labels: "com.docker.compose.service"` vào `logging.options` ở `compose-t062/_common.yml` (mọi app kế thừa qua `extends`) và `compose-exp/keycloak.yml`; hạ tầng dùng file chồng mới `/opt/flash-ticket-infra/deploy/docker-compose.rca-log.yml` (chỉ khối `logging` cho postgres, redis, rabbitmq, user-db), không sửa file gốc. json-file khi đó ghi `"attrs":{"com.docker.compose.service":"<svc>"}` vào **từng dòng** (tài liệu Docker json-file `labels`).
- **Collector:** thay 8 receiver `filelog/<svc>` ghim ID container bằng **một** `filelog/docker` `include: /var/lib/docker/containers/*/*-json.log` (+ `*-json.log.*` nếu xoay vòng), `json_parser` → `attributes.docker`; `move attributes.docker.attrs["com.docker.compose.service"]` → `resource["service.name"]`; `filter` bỏ dòng không có nhãn (toxiproxy, collector, container lạ); giữ `file_storage` (offset), `start_at: end` cho file mới. Ánh xạ tên hạ tầng → thực thể do adapter làm như hiện nay (`INFRA`).
- **Postgres:** thêm `command` chồng `-c log_autovacuum_min_duration=0 -c log_checkpoints=on -c log_lock_waits=on` (phân xử đợt Keycloak DELETE — `ca-nen/PHAN-TICH.md`). **Chưa kiểm** khối lượng log thêm; kiểm sau 10 phút.
- **Kiểm sau:** Loki có log của 12 dịch vụ (8 app + 4 hạ tầng) với đúng `service_name`; tạo lại một container app → log tiếp tục không mất (đây là lỗi của cách cũ); đếm dòng/phút trước–sau theo service.

## 2. Đầu dò hộp đen H5 — receiver `httpcheck`

- Targets: `GET http://127.0.0.1:<cổng>/actuator/health/liveness` của 7 service Java (cổng lấy từ cấu hình đang chạy), `collection_interval: 10s`, timeout 2 s. Bản `6b21ed55` có thể trả 401 cho liveness — vẫn chứng minh tiến trình phản hồi (`httpcheck.status` theo mã).
- Mở rộng `filter/health` của traces: thêm `IsMatch(attributes["url.path"], "^/actuator/health")` để bỏ span SERVER của lời gọi này. **Chưa kiểm:** liveness có sinh span con (DB/Redis) — nếu có, xem lại cách lọc (mồ côi, `span-goc/PHAN-TICH.md`).
- Kiểm: `httpcheck_status` có chuỗi cho 7 endpoint; thử `docker pause` 30 s một service → `httpcheck.error` tăng trong đúng khoảng.

## 3. Span bọc tác vụ định kỳ Keycloak — chỉ cấu hình agent

- Env Keycloak: `OTEL_INSTRUMENTATION_METHODS_INCLUDE=org.keycloak.services.scheduled.ScheduledTaskRunner[run];org.keycloak.expiration.jpa.impl.DefaultExpirationTask[run];org.keycloak.expiration.jpa.impl.RealmAwareExpirationTask[run]` (tên lớp đã kiểm có trong jar Keycloak 26.8.0 của image đang chạy, 22:28Z; **chưa kiểm** chữ ký `run` của từng lớp).
- Kiểm: Tempo có span INTERNAL mới trên `Timer-0` và `user-session-purge-expired`; SQL Hibernate `OutboxEntryEntity`, `PersistentUserSessionEntity` thành con (chạy lại `span-goc/phan_loai.py` trên một cửa sổ 10 phút: nhóm `internal_khac` của Keycloak → ~0).

## 4. Thứ tự và cách hoàn tác

1. Sao lưu: `compose-t062/`, `compose-exp/keycloak.yml`, `collector/config.json`, env Keycloak (`.bak-T063-<ngày>`), ghi hash.
2. Collector mới (cách A + httpcheck + lọc) → `docker restart flash-ticket-collector` → kiểm log/metric 2 phút.
3. Tạo lại hạ tầng với file chồng (postgres, redis, rabbitmq, user-db) → chờ healthy.
4. Tạo lại 7 app + Keycloak với cùng image (`IMAGE=<digest hiện tại>`), từng service, chờ đăng ký Eureka.
5. Kiểm mục 1–3; chạy một giao dịch mua trọn (kịch bản L1) để kiểm đường tải sau tạo lại.
- Hoàn tác: chép lại các `.bak`, `docker restart flash-ticket-collector`, tạo lại container bằng file cũ.
- Ảnh hưởng: gián đoạn app vài phút; không có lượt thu nào chạy; L1 phải chạy lại kiểm một giao dịch sau bước 4 (phối hợp qua file `EXP-APP-TRA-QUYEN-<n>` trong `results/T-062/tai-2/`).
