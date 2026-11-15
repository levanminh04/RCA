# T-063 — Kết quả D2 bản 2 (xác nhận can thiệp), tag `d2b-2a7f481a`, 13/11/2026 02:23–03:00Z

Tải hành trình mua vé (L1), cấu hình sau bảo trì lượt 1. Mỗi ô 150 s, đầu dò độc lập không gọi HTTP của app (`inj2.py probe`) + Prometheus đúng khoảng. Script: [`phan_tich_d2b.py`](phan_tich_d2b.py) → [`d2b-d2b-2a7f481a-danh-gia.json`](d2b-d2b-2a7f481a-danh-gia.json); truy vấn bổ sung phía Gateway/consumer/liveness với **nền sạch** đầu lượt (02:23:30–02:25:20Z; nền ngay trước từng ô bị nhiễm do `rate[1m]` của ô trước).

| Ô | Kết quả | Bằng chứng (nền → lỗi) |
|---|---|---|
| EVENT-DB-LAT | **ĐẠT** | toxic `event-jdbc` 30 ms; PG SSLRequest qua proxy 33,2 ms (trực tiếp 1,3); pool used Event 0 → 1,9 |
| REDIS-BOOK | **ĐẠT** | toxic 200 ms; PING Redis qua proxy 202 ms; p50 server Booking 9,9 → 255 ms (Booking dùng Redis trên đường mua — ở T-062 tải đọc thì không, nên ô này từng bị bỏ) |
| NET-GW-BOOK | **ĐẠT** | toxic 300 ms; p50 `http_client_request_duration` Gateway→:18082 22 → 333 ms |
| HTTP5-EVENT | **ĐẠT** | 5xx Event 0 → 1,03 req/s; audit `http.error.executed` tăng |
| CPU-BOOK-1 | **ĐẠT** | 1 luồng đốt; Booking throttle 0 → 15,5% chu kỳ; `nr_throttled` +171 trong 95 s |
| CPU-BOOK-2 | **ĐẠT** | 2 luồng; throttle → 72%; `nr_throttled` +804 |
| PAUSE-PAYMENT | **ĐẠT** (can thiệp + đầu dò) | `Paused=true`; `httpcheck_error` (:8083) = 1, thời gian liveness 18 ms → 29.376 ms (hết thời gian chờ); mẫu JVM Payment 3 → 1 / 30 s. Kênh `live-down` bản 2 (theo `httpcheck_status`) **không** phản ánh (trạng thái cũ giữ khi request treo) → sửa kênh (bản 3) |
| CONSUMER-BOOK-SLOW | **CHƯA ĐẠT** | toxic latency 200 ms có mặt nhưng không tồn queue: ack Booking 0,35 → 0,48/s, unacked ~0,2, ready 0, p50 span CONSUMER không tăng. Trễ đường truyền không giới hạn thông lượng ở nhịp message thấp. → đổi sang toxic `bandwidth` (giới hạn thông lượng) và xác nhận lại |
| POOL-EVENT | **KHÔNG THỬ ĐƯỢC** | pool used/pending Event = 0 suốt pha. Nguyên nhân trong mã: `services/event-service/src/rca-test/.../RcaFaults.java` `poll()` có `!"event_service".equals("booking_service")` → `pool.hold` chỉ chạy ở Booking (POOL-BOOK là ô **đánh giá**). Làm được cần sửa `src/rca-test` (ngoài đường dẫn đã ghi rõ trong quyền) → loại khỏi đợt thu; H3 chỉ phân xử gián tiếp (tín hiệu pool ở EVENT-DB-LAT, CPU-BOOK) — ghi giới hạn |

Ô dùng cho đợt thu: 7 ô đạt ở trên + FLASH-HEALTHY, HTTP5-EVENT-FLASH (cùng hook HTTP5-EVENT đã đạt; chờ L1 có `-BuocTai`) + BINH-THUONG; CONSUMER-BOOK-SLOW chỉ vào nếu xác nhận lại đạt.

## Đính chính 03:25Z — tải D2 hết sớm; nguyên nhân 503/504 của pilot L1

- Container tải của D2 (`rca-tai-d2b-2a7f481a`, `-Seconds 1800` cố định trong `runner2.py`) kết thúc ~02:53Z, trong khi D2 chạy tới 03:00Z. Nửa sau CPU-BOOK-2 (từ 02:53Z) và toàn bộ PAUSE-PAYMENT không có tải của D2. Lỗi của bộ chạy (Claude), đã sửa: thời lượng tải theo số ô.
- L1c (Codex) thấy máy tải trống và chạy pilot `l1maint20261113a` 02:56:05–03:01:07Z — đúng luật "không hai workload". 33 lỗi create-payment (19×504, 14×503) của pilot này nằm trong 02:56:34–02:58:24Z, trùng khoảng D2 pause Payment (02:55:49–02:58:20Z) → **nguyên nhân: ô PAUSE-PAYMENT của D2**, không phải lỗi sau bảo trì. Câu hỏi OPEN của L1 về 503/504 đóng bằng bằng chứng thời gian này.
- Ảnh hưởng tới kết luận D2: CPU-BOOK-2 (throttle đo trong cgroup, không phụ thuộc tải) và PAUSE-PAYMENT (trạng thái pause, httpcheck) vẫn xác nhận được; PAUSE-PAYMENT có tải pilot của L1 trong pha lỗi.

## Xác nhận lại, tag `d2b-43e42c6c` (03:21–03:32Z)

- **PAUSE-PAYMENT — ĐẠT trọn**: `Paused=true`; kênh `live-down` bản 3 (`max by(http_url)(httpcheck_error) or 0·…`) cho :8083 = 0 ở nền, **1,0** suốt pha lỗi; mẫu JVM Payment 3 → 1 / 30 s.
- **CONSUMER-BOOK-SLOW, lần 2 (toxic `bandwidth` 2 KB/s)** — CHƯA ĐẠT: ready Booking 0 → 0, unacked tb 0,33 (max 1), ack 0,37 → 0,48/s, p50 server Booking không đổi. Lưu lượng message của tải (~0,5 msg/s) nhỏ hơn mức giới hạn. Lần 3 (1 KB/s, mức nhỏ nhất của toxiproxy) đang chạy; không đạt thì loại ô, H4 chỉ phân xử gián tiếp (AGENTS §5a).
- **CONSUMER-BOOK-SLOW, lần 3 (bandwidth 1 KB/s, tag `d2b-8bea3d4a`)** — CHƯA ĐẠT: ready 0, unacked tb 0,33, ack 0,37 → 0,47/s, p50 Booking không đổi. **Dừng sau 3 lần (AGENTS §5a), loại ô khỏi đợt thu.** Đã thử: latency 200 ms, bandwidth 2 KB/s, bandwidth 1 KB/s. Nhận định (chưa kiểm): với ~0,5 message/s và prefetch mặc định của Spring AMQP, toxic trên kết nối không làm consumer tụt sau; muốn tạo tồn queue cần làm chậm khâu xử lý của consumer (hook trong `src/rca-test` — ngoài phạm vi đường dẫn đã ghi rõ) hoặc tăng lưu lượng message. Hệ quả: H4 chỉ phân xử gián tiếp; Booking vẫn nối AMQP qua proxy `booking-amqp` (không toxic = chuyển tiếp) để topology cố định trong đợt thu.

## Danh mục ô cho đợt thu dev bản 2 (chốt 03:42Z)

EVENT-DB-LAT, REDIS-BOOK, NET-GW-BOOK, HTTP5-EVENT, HTTP5-EVENT-FLASH, CPU-BOOK-1, CPU-BOOK-2, PAUSE-PAYMENT, FLASH-HEALTHY, BINH-THUONG ×4. Không vào: SLOW-BOOK (WHY-83), POOL-EVENT (không thử được), CONSUMER-BOOK-SLOW (không xác nhận được).

## Đính chính theo REVIEW T-063 R4 (03:58Z)

CPU-BOOK-1 và CPU-BOOK-2: **cách tiêm ĐẠT** (số luồng đốt đúng, throttle trong cgroup Booking tăng). **Điều kiện cô lập cơ chế khai trước chưa thỏa trọn**: CPU-BOOK-2 throttle 72% < ngưỡng khai 80% (`o-dev-bo-sung.md`); CPU-BOOK-1 chưa đo PSI CPU toàn máy (đầu dò chỉ có pressure cgroup Booking), và tải D2 hết sớm ở nửa sau CPU-BOOK-2. Giữ hai cường độ, **không** chỉnh luồng/quota theo số đã xem; không gọi CPU-BOOK-1 là đối chứng "ít nhiễu toàn máy" khi diễn giải M1 trước khi có PSI máy dưới tải mua vé.
