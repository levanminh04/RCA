| Ca (mã mờ) | Ô lỗi | Đáp án T-059 (tập chấp nhận) | M1: kết luận | M1: hạng 1 | Hạng tốt nhất của đáp án | Vai trò M1 gán cho đáp án |
|---|---|---|---|---|---|---|
| `00eaea92` | FLASH-HEALTHY | root = null (tải tăng khỏe) (root = null) | CAUSE_FOUND (OK) | payment-service | — | — |
| `1ad3afeb` | EVENT-DB-LAT | event-service → event_db (data) (event-service, event_db) | CAUSE_FOUND (OK) | event-service | #1 | event-service: nghi là nguồn, event_db: bình thường |
| `2e2a5541` | SLOW-BOOK | booking-service (booking-service) | CAUSE_FOUND (OK) | booking-service | #1 | booking-service: nghi là nguồn |
| `6c1a9fd8` | BINH-THUONG | root = null (ca bình thường) (root = null) | CAUSE_FOUND (OK) | event-service | — | — |
| `a5539fba` | BINH-THUONG | root = null (ca bình thường) (root = null) | CAUSE_FOUND (OK) | keycloak | — | — |
| `a89954d1` | HTTP5-EVENT | event-service (event-service) | CAUSE_FOUND (OK) | event-service | #1 | event-service: nghi là nguồn |
| `bf17acbf` | CPU-BOOK | booking-service (booking-service) | CAUSE_FOUND (OK) | booking-service | #1 | booking-service: nghi là nguồn |
| `e8661e0a` | BINH-THUONG | root = null (ca bình thường) (root = null) | CAUSE_FOUND (OK) | event-service | — | — |
| `f728fce2` | NET-GW-BOOK | api-gateway → booking-service (http) (api-gateway, booking-service) | CAUSE_FOUND (OK) | booking-service | #1 | api-gateway: bị kéo theo, booking-service: nghi là nguồn |

Ca có lỗi: 5; đáp án ở hạng 1: 5/5; trong top 3: 5/5. Ca không tiêm lỗi mới (3 bình thường có lỗi nền tickets 500 + FLASH chưa xác nhận khỏe, có 429 ở Gateway): 4; M1 kết luận CAUSE_FOUND: 4/4 — chưa phải tỷ lệ báo động giả trên ca khỏe (T-059: chưa có ngưỡng khỏe).
Nguồn: `ket-qua/phat-lai/bang-cham.json` (sha256 manifest kết quả trước ghép `8f9cf01368fc6823…`). n = 1 mỗi ô — chỉ là lượt phát triển đầu, không đủ để kết luận hiệu quả.
