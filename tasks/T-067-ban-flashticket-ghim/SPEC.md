# T-067 — Bản FlashTicket thử nghiệm ghim (W2)

- **Trạng thái:** đã duyệt (17/11/2026, bản 2)
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P9, P10 — **Cổng:** chuẩn bị G6

Lịch sử soạn: bản 1 và bản 2 trình trong chat 17/11/2026; Codex soát bản 1; bản 2 sửa theo các điểm đó. File này là bản 2 ghép đầy đủ. Quyết định của Minh ghi ở `LOG.md` phiên 1.

## Mục tiêu

Kế hoạch [giai đoạn 2 §8.1, §8.2](../../docs/techstack/KE-HOACH-GIAI-DOAN-2.md) W2. DECISIONS 17/11 chọn phương án B: `main` của nhóm cộng các commit quan sát của PR #17.

Đây là task **cài đặt và kiểm dữ liệu**. Đầu ra là một phiên bản FlashTicket ghim, dùng xuyên W3–W7, và bằng chứng nó sinh các tín hiệu RCA cần trên các đường thực sự chạy. Task không trả lời về hiệu quả của M1; việc đó thuộc W3. Câu kết luận giới hạn ở "đạt các yêu cầu đã kiểm trên các đường thực sự chạy", không ghi "đủ R-01…R-10".

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Giải thích khác cần loại | Phép kiểm và bằng chứng | Phần còn mở |
|---|---|---|---|
| Gỡ xung đột có làm đổi logic nghiệp vụ của `main` không? | Lấy nhầm phía khi gỡ xung đột | `git diff 640dbaf..rca/exp-2026-11` chỉ được chạm các nhóm được giữ từ PR (mục Các bước, bước 1); đoạn nào khác phải liệt kê kèm lý do. `mvnw verify` của 7 service đạt; Booking, Event chạy thêm với `-P rca-test`. | Q2: đoạn `RefundServiceImpl` cần Tuấn xem. |
| Bản mới có sinh các tín hiệu bắt buộc không? | Bộ kiểm R cũ đạt mà vẫn thiếu (đã chỉ ra ở R-03, R-04, R-06); kịch bản tải không đi qua mọi đường | Bộ kiểm mới `tests/signals/` của repo lab đọc qua API Tempo/Loki/Prometheus (danh sách bên dưới), chạy trên lượt mua vé 10 phút cộng bước kiểm riêng cho User. | Đường không chạy trong lượt kiểm thì ghi là chưa kiểm, không ghi là đạt. |
| Đã biết chắc đang chạy bản nào chưa? | Image hoặc nhãn cũ còn sót | Chuỗi commit → digest → container, kiến trúc `arm64`; `service.version` khớp commit; ghim commit repo lab đã triển khai. | — |
| `main` đổi gì so với bản 3? | — | Ghi chênh lệch giữa **hai bản thực chạy**: merge cuối, image, cấu hình, schema. `6b21ed55...640dbaf` là 7/46 commit; `main` có 2 migration PostgreSQL (`event-image-roles`, `event-venue-details`). | Hành vi đổi bao nhiêu thì W3 đo. |

**Tín hiệu bắt buộc.** Ngưỡng khai trước khi chạy.

- Span SERVER có `http.route` ở gateway và các service trên luồng mua vé; span CLIENT gateway → service.
- Span DB CLIENT tới `event_db`, `booking_db`, `payment_db`, `ticket_db`.
- **User và Mongo:** kịch bản k6 không gọi route nào của User, nên thêm bước kiểm riêng, không nằm trong hỗn hợp tải: `GET /api/v1/me` bằng tài khoản thử, nối tới span của User và span Mongo.
- Span Redis ở booking và gateway.
- **RabbitMQ:** khai trước các cặp phát → nhận cần thấy, lấy từ `definitions.json` và code listener, ghi file trước khi chạy; kiểm từng cặp span PRODUCER/CONSUMER nối đúng bản tin.
- **Luồng chính:** một đơn `COMPLETED` có đúng một vé, lần theo `correlationId` qua các service.
- **Log:** JSON đủ trường B16. Ngưỡng **95% theo từng service** có điểm ghi log bắt buộc. Mẫu số gồm mọi dòng log ở các bước đã khai, kể cả dòng thiếu ID. Tử số chỉ đếm dòng có cặp `(traceId, spanId)` khớp đúng một span. Điểm bắt buộc mà không có log thì ghi "chưa đủ bằng chứng".
- **Metric:** JVM, HTTP server, pool DB, queue RabbitMQ, `docker_stats` từng container, `httpcheck`.
- **Tải 1 giờ:** mức tải ×1 như tải chuẩn T-063; tiêu chí giao dịch khai trước theo số của lượt L1. Đếm OOM và restart theo từng container. Đo bộ đếm rớt và lỗi xuất ở **cả hai** Collector (agent và gateway). Mất mẫu hoặc bộ đếm bị reset thì ghi "chưa xác định".

## Đầu vào

- Repo FlashTicket: `origin/main` ghim tại `640dbaf`, nhánh `origin/rca/quan-sat-log` tại `bb84d64`.
- Repo lab sau T-066.
- Script build cũ `app-host/scripts/build-t062.sh` (repo lab).
- `D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md`.

## Đầu ra

- **Repo FlashTicket:** nhánh mới `rca/exp-2026-11` = `640dbaf` + merge `rca/quan-sat-log`, đã gỡ xung đột, đã push. **Không mở PR vào `main`, không merge `main`.**
- **Repo lab:**
  - `app-host/scripts/build.sh` nhận revision làm tham số;
  - `app-host/overrides/*.yml`: file phủ lên `deploy/app/*.yml` của nhóm, thay cho bản chép `services/`;
  - `observability/collector/agent-compose.yaml` triển khai từ repo;
  - `tests/signals/check_purchase_journey.py` và file khai trước các cặp RabbitMQ.
- **`results/T-067/`:**
  - `go-xung-dot.md`: từng file trong 10 file xung đột, chọn phía nào, vì sao;
  - `build-manifest.json`: commit → image → digest → arch → profile, số lớp `RcaFaults` trong từng jar;
  - `compose-hieu-luc/`: cấu hình hiệu lực của từng service;
  - `kiem-tin-hieu.json` và `.md`;
  - `tai-1-gio.md`;
  - `thay-doi-main.md`;
  - `thay-doi-may.md`: mọi thay đổi trên máy, hash trước/sau, cách hoàn tác.

## Phạm vi ghi

Ngoài `LOG.md` của task này và dòng T-067 trong `docs/STATE.md`:

- Repo FlashTicket: **chỉ nhánh mới `rca/exp-2026-11`**, push lên origin.
- Repo lab: `app-host/`, `observability/collector/`, `tests/`. Commit và push theo luật cứng 11.
- `results/T-067/`.
- **exp-app:**
  - worktree build mới trong `/opt/flash-ticket-build`; image mới;
  - `pg_dump` và `mongodump` DB hiện tại vào `/srv/rca-lab/backups/`;
  - dựng lại DB theo Q3, chạy migration của `main`, nạp fixture;
  - chuyển container sang image mới bằng cấu hình hiệu lực;
  - giá trị giả cho biến bắt buộc của Payment ở `/etc/rca-lab`;
  - chuyển Collector agent sang compose của repo lab.
  - Giữ image `arm64-t062-6b21ed55` và `compose.json` cũ để hoàn tác.

## Các bước

1. **Tạo nhánh, merge, gỡ 10 file xung đột** (7 Dockerfile, `OrderServiceImpl`, `PromotionServiceImpl`, `RefundServiceImpl`). Quy tắc theo lời Minh: **mọi đoạn logic lấy theo `main`**. Phần quan sát của PR chỉ được chèn lại ở dạng gọi telemetry quanh điểm xử lý của `main`, không đổi luồng. Dockerfile lấy `main` làm gốc, chỉ thêm các dòng của PR: tải jar agent có checksum, entrypoint, biến môi trường. **Được giữ từ PR:** `src/rca-test` và profile trong pom, cấu hình log B16, agent trong image, test quan sát. Thay đổi `deploy/*` của PR **không** mang theo. Kiểm: `go-xung-dot.md` và diff so với `640dbaf`.
2. Chạy `mvnw verify` cho 7 service trên exp-app (ARM); Booking, Event thêm `-P rca-test`. Kiểm: test đạt.
3. Build image. Booking và Event build với `-P rca-test` như T-062; 5 service còn lại build thường. Kiểm: `build-manifest.json`; jar build thường không chứa `RcaFaults`.
4. Viết file phủ. Với mỗi service, dựng cấu hình hiệu lực bằng `docker compose -f <file nhóm> -f <file phủ> config`, lưu vào `results/T-067/compose-hieu-luc/`; triển khai từ file đã dựng. Payment: tắt `ngrok` bằng `profiles: ["disabled"]`; giữ mock VNPay của lab. **Chỉ một agent:** `OTEL_AGENT_ENABLED=true`, bỏ mount jar cũ và `JAVA_TOOL_OPTIONS -javaagent`. Kiểm: cấu hình hiệu lực có `logging.options.labels` chứa `com.docker.compose.service`; so với `compose-t062` đang chạy, chỉ khác image và các biến chủ đích đổi.
5. Dump DB (`pg_dump`, `mongodump`, cỡ 0,8 GB [ước lượng]) vào `/srv/rca-lab/backups/`. Đây là đường lùi dữ liệu duy nhất cho một bước không quay lại được.
6. Triển khai trong khung giờ riêng, sau tuyến một ca của T-066. Dựng lại DB, chạy migration, nạp fixture. Chuyển Collector agent sang compose của repo lab. Kiểm: health mọi service, đăng ký Eureka đủ, Collector nhận đúng `service.name`. **Hoàn tác:** khôi phục bản dump cùng image và compose cũ; thử hoàn tác ít nhất một lần.
7. Khai trước file cặp RabbitMQ và tiêu chí tải; rồi chạy bộ kiểm tín hiệu trên lượt mua vé 10 phút cộng bước `GET /api/v1/me`.
8. Tải 1 giờ.
9. Ghi `thay-doi-main.md` để W3 dùng.

## Kiểm đúng đắn

- Tín hiệu kiểm bằng bộ kiểm mới đọc trực tiếp từ kho; bộ kiểm R cũ chỉ để chẩn đoán.
- Ngưỡng và cặp RabbitMQ khai trước khi xem kết quả; đổi sau khi xem phải ghi là sửa sau.
- Tách lỗi build hoặc hạ tầng khỏi thiếu tín hiệu.
- **Không kiểm được trong task này:** chất lượng RCA trên bản mới (W3).

## Tiêu chí xong

1. Nhánh `rca/exp-2026-11` đã push; diff so với `640dbaf` chỉ chạm các nhóm được giữ, đoạn khác có lý do.
2. Test đạt.
3. Có chuỗi commit → digest → container, `arm64`, commit repo lab.
4. Đạt danh sách tín hiệu bắt buộc trên các đường đã chạy; đường chưa chạy ghi rõ.
5. Tải 1 giờ đạt tiêu chí khai trước; không OOM, không restart; bộ đếm rớt của hai Collector bằng 0 hoặc ghi "chưa xác định" kèm lý do.
6. `thay-doi-main.md` đủ.
7. Hoàn tác đã thử được ít nhất một lần.
8. Q2: Tuấn đã xem đoạn `RefundServiceImpl` trước khi nghiệm thu nhánh.

## Không làm

- Merge PR #17 vào `main`.
- Deploy lên máy 84.
- Bản K8s.
- Phép hồi quy V082 trên bản mới (W3).
- Luật cảnh báo (W4).

## Chi phí ước lượng

- Build và test 7 service trên ARM khoảng 1–2 giờ máy [ước lượng]; tải 1 giờ; dump DB vài phút. Hai việc dài cỡ 1 giờ nên báo trước theo luật cứng 8 và 21.
- **Khi gặp lỗi:**
  - Build hỏng ở một service: chỉ build lại service đó.
  - Tải hỏng ở 10%, 50% hay 99%: ghi là lỗi hạ tầng hoặc lỗi hệ thống, sửa, rồi chạy lại cả lượt 1 giờ. Đây không phải lượt thực nghiệm, nên chạy lại rẻ hơn phân tích một lượt dở dang.

## Rủi ro và điều chưa chắc

- Dựng lại DB làm mất dữ liệu đơn hàng thử cũ trên exp-app. Dữ liệu đó không phải bằng chứng; gói ca đã lưu riêng. Có bản dump để lùi.
- Gỡ xung đột ở `RefundServiceImpl` đụng logic nghiệp vụ (Q2).
- Nhóm đổi `main` tiếp sau khi đã ghim: bản ghim giữ nguyên, chỉ báo cho Minh.
- Sidecar `ngrok` của Payment có thể bị service khác phụ thuộc [chưa kiểm]; kiểm ở bước 4.

## Prompt bàn giao

Ở `LOG.md` của T-066 (một prompt chung cho cả hai SPEC).
