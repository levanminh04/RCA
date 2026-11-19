# T-067 — Bản 3 và bản ghim `rca/exp-2026-11` khác nhau ở đâu (cho W3)

So **hai bản thực chạy** trên exp-app: bản 3 (đang chạy tới T-067, image `arm64-t062-6b21ed55`) và bản ghim T-067
(image `arm64-t067-36a3725d`). Mục đích: W3 biết hành vi nào có thể đổi trước khi đo M1 trên bản mới.
Đây là liệt kê thay đổi, **không đo** ảnh hưởng (W3 đo).

Lập 18/11/2026; mục 5–6 điền sau bước 6 (triển khai 07:19:40Z).

## 1. Commit

| | Bản 3 | Bản ghim |
|---|---|---|
| Commit chạy | `6b21ed55ecfe…` (nhánh `rca/quan-sat-log` sau merge `main` 12/11) | `36a3725d9b20…` = merge `640dbaf` (`main` ghim 17/11) + `bb84d64` |
| Nguồn logic | `main` tới 12/11 | `main` tới `640dbaf` (+17 commit first-parent, 24 commit không phải merge) |
| Quan sát (B16, agent, telemetry) | PR #17 bản `f7e6207` | như bản 3, gỡ xung đột theo `go-xung-dot.md` |

Lệnh: `git log --oneline --first-parent 6b21ed55..640dbaf` (17 dòng), `git log --no-merges 6b21ed55..640dbaf` (24).

## 2. Mã nghiệp vụ đổi theo service (`git diff --shortstat 6b21ed55 36a3725 -- <svc>/src/main`)

| Service | Đổi | Commit chính của nhóm |
|---|---|---|
| event-service | 24 file, +824/−222 | API Venue, cập nhật luồng organizer, seatmap, ảnh event (`image_role`), `categoryId` (TuyenPV2004, 13–15/11) |
| booking-service | 18 file, +229/−62 | tên sự kiện trong đơn (`OrderViewAssembler`, truy vấn trang đơn mới), đọc snapshot cũ (sondimid, 13–16/11) |
| payment-service | 5 file, +78/−129 | **hoàn tiền chỉ ghi DB** (`782e557`, Quốc Tuấn 14/11; bỏ gọi VNPay refund/query); xóa biến VNPay không dùng; **đường lỗi Payment → Booking** (`40b5acd`, K3s): lời gọi POST lấy snapshot mua hàng của Booking nay bắt `IllegalStateException` (LoadBalancer không có instance) và ném `PaymentException(BOOKING_UNAVAILABLE)`, không retry POST |
| user-service | 7 file, +94/−13 | giới hạn ảnh, `branding-max-bytes` |
| api-gateway | 2 file, +7/−3 | thêm route ảnh nền seat-map, `/api/v1/admin/venues` |
| ticket-service | 2 file, +6 | sửa 404 tra vé |
| discovery-server | 0 | — |

Thay đổi có thể chạm luồng mua vé đang dùng trong tải: Booking (trang đơn, tên sự kiện, `OrderViewAssembler`), Event (chi tiết sự kiện có thêm trường), Payment (hoàn tiền; **đường lỗi khi gọi Booking lấy snapshot mua hàng** — mã lỗi trả về khi Booking không có instance đổi; có thể chạm các ô lỗi phía Booking của W3). *(Đính chính 19/11, phản biện R4: bản trước ghi "luồng thanh toán không đổi theo diff" là sai.)*

## 3. Cấu hình trong mã (`application.yaml`, `pom.xml`)

- Booking: tiền tố khóa cache Redis đơn của người mua `…buyer-orders:v1:` → `…:v2:` (mặc định; env có thể ghi đè). Hệ quả: cache nguội sau triển khai.
- Payment: thêm `payment.booking.discovery-enabled` (mặc định `false` → dùng `BOOKING_SERVICE_URL`), thêm `spring-cloud-starter-loadbalancer`.
- Event: bỏ `booking-base-url`; thêm `spring-cloud-starter-loadbalancer`, `imageio-webp`.
- User: `max-file-size` 2MB → 5MB, thêm `imageio-webp`.
- Gateway: thêm 2 route (mục 2).
- Cấu hình chạy (env, giới hạn tài nguyên, thư mục tiêm lỗi): **không đổi** — cấu hình hiệu lực chỉ khác `image` và `SERVICE_VERSION` (`compose-hieu-luc/so-sanh.json`).

## 4. Image

| | Bản 3 | Bản ghim |
|---|---|---|
| Ảnh gốc JRE | `eclipse-temurin:21-jre-alpine@sha256:ac05c3c4…` (digest của PR) | `…@sha256:b48e02e0…` (digest của `main`) + `curl`, `jq` |
| Agent | OpenTelemetry Java agent 2.33.1, checksum `e43a270d…` | như cũ |
| Booking, Event | `-P rca-test` | `-P rca-test`; hook `pool.hold` của Event (`e557307`, ô POOL-EVENT) — xem bảng nền bên dưới |
| ID image | xem `build-manifest` T-062 | `build/build-manifest-dem-lai.json` |

**Nền so sánh của Event phụ thuộc nhóm ca** *(đính chính 19/11, phản biện R4)*:

| Nền | Image Event | Hook `pool.hold` so với bản ghim | Bằng chứng |
|---|---|---|---|
| Bản 3 đang chạy ngay trước W2 (sau khi Minh hoàn tác Event) | `arm64-t062-6b21ed55` | bản ghim **có thêm** hook: `git diff --shortstat 6b21ed55 36a3725 -- services/event-service/src/rca-test` = 2 file, +36/−2 | `docs/DECISIONS.md` (hoàn tác Event), `trien-khai/` |
| Các ca **thu bù 3** của T-063 | `arm64-t063h3-76b34d5e` | **không khác**: `git diff e557307 36a3725 -- services/event-service/src/rca-test` rỗng | `results/T-063/dong-bang/dong-bang-3.json` (container Event), `docs/WHY.md` (lý do image riêng) |

W3 ghép ca từ nhóm nào thì so với nền của nhóm đó; không quy khác biệt ở ô POOL-EVENT cho hook khi so với thu bù 3.

## 5. Schema DB

Áp tại chỗ (phương án A, Minh chọn 18/11), giữ dữ liệu, Keycloak và sự kiện của tải chuẩn:

| Migration của `main` | Trên DB bản 3 | Sau T-067 |
|---|---|---|
| `2026-11-04-payment-refund-settlement-columns.sql` | đã có | không đổi |
| `2026-11-13-event-image-roles.sql` | chưa | áp 06:58:29Z và lại 07:13:01Z (sau thử hoàn tác): thêm `tbl_event_images.image_role` (mặc định `GALLERY`), bỏ ràng buộc duy nhất `(event_id, display_order)`, thêm `event_image_role_check`, `event_image_role_order_key`; `UPDATE 0` (bảng ảnh rỗng) |
| `2026-11-15-event-venue-details.sql` | chưa | thêm `tbl_venues.description`, `image_url`, `google_maps_url` |

Không đổi: `booking_db`, `payment_db`, `ticket_db`, `keycloak_db`, Mongo `user_db`. Dữ liệu cũ (14.182 đơn COMPLETED, 4 sự kiện) giữ nguyên. Điểm lùi: `/srv/rca-lab/backups/t067-20261118/`.

## 6. Container và Collector

| | Bản 3 | Bản ghim |
|---|---|---|
| Cấu hình | `/opt/flash-ticket-app/compose-t062/*.yml` | `/opt/flash-ticket-build/t067-compose/hieu-luc/*.yml` (= `deploy/app` của `main` + file phủ lab `99eeca0`) |
| Env | `env-t062/` | như cũ (`env_file: !override`) |
| Khác biệt hiệu lực | — | chỉ `image`, `SERVICE_VERSION` (`compose-hieu-luc/so-sanh.json`) |
| Payment | không có `ngrok` | `ngrok` của `main` tắt bằng profile |
| Collector agent | `/opt/flash-ticket-app/collector/compose.json` + `config.json` | `/opt/rca-lab/observability/collector/agent-compose.yaml` (checkout `5a39028`, blob = `main` lab); cấu hình ≡ bản cũ sau khi thay IP; dữ liệu `/srv/rca-lab/collector-agent` (hàng đợi chép từ bản cũ) |
| Chuỗi container | — | `trien-khai/chuoi-container.json` |

## 7. Điều W3 cần biết khi so với bản 3

- Mọi số đo của bản 3 (T-062…T-066) chạy trên image khác ảnh gốc JRE và code nghiệp vụ khác (mục 2). Hook `pool.hold` của Event: bản ghim có thêm so với nền `6b21ed55`, nhưng giống nền thu bù 3 (`76b34d5e`) — xem bảng nền ở mục 4. Bản ghim không phải bản 3 cộng quan sát.
- Cache đơn của Booking nguội ngay sau triển khai (tiền tố `v2`).
- Đo trên bản ghim (18/11): tải ×1 10 phút 721/721 hành trình xong, p95 562 ms (`kiem-tin-hieu.md`); tải 1 giờ ở `tai-1-gio.md`. Chưa so định lượng với bản 3; W3 đo.
