# Hai lượt 10 phút — source cuối

Lượt A: `l1r20261112v2a`, 2026-11-12T22:52:05.622954116Z -> 2026-11-12T23:02:06.129989495Z. Lượt B: `l1r20261112v2b`, 2026-11-12T23:03:06.018617541Z -> 2026-11-12T23:13:06.517007501Z. Cùng source, cấu hình, rate 12 hành trình/10 s và mix 70/20/5/5; mỗi lượt tạo phiên PKCE mới trước cửa sổ. Snapshot/hash ở thư mục từng lượt. SHA256 source/config A = B = current.

| Chỉ số | A | B |
|---|---:|---:|
| journey_started | 720 | 720 |
| journey_finished | 720 | 720 |
| purchase finished | 144 | 144 |
| journey_failed | 0 | 0 |
| dropped_iterations | 0 | 0 |
| HTTP 401 | 0 | 0 |
| token_refresh_success | 41 | 42 |
| token_refresh_failure | 0 | 0 |

Gateway đếm độc lập từ log B16 trong khoảng start-utc tới container FinishedAt, nhận completed/failed/rejected/cancelled. Bảng dưới dùng routeId thực của gateway. Refresh Keycloak và mock checkout không qua gateway; callback mock đi trực tiếp payment.

| Route gateway | k6 A | Gateway A | k6 B | Gateway B | Chênh tuyệt đối A–B | Tương đối so với A |
|---|---:|---:|---:|---:|---:|---:|
| booking | 1369 | 1369 | 1364 | 1364 | 5 | 0.365% |
| event | 1440 | 1440 | 1440 | 1440 | 0 | 0.000% |
| payment | 144 | 144 | 144 | 144 | 0 | 0.000% |
| ticket | 144 | 144 | 144 | 144 | 0 | 0.000% |

Theo endpoint: log gateway không ghi template path. Các số gateway dưới đây được nối theo requestId; với Event dùng correlationId khi duy nhất. Kiểm routeId và status sau nối; không tự đặt traceparent. Số k6 lấy từ counter route_responses, đối chiếu thêm JSON/CSV và console request log.

Trong các analysis v2 tạo sớm, trường tên cũ `requestTraceUniqueCount` đếm ID response duy nhất; không phải số trace. Các bản sau gọi đúng là `requestIdentityUniqueCount`. Số span/trace lấy từ bằng chứng Tempo riêng.

| Endpoint | k6 A | Gateway nối A | k6 B | Gateway nối B | Chênh tuyệt đối A–B | Tương đối so với A |
|---|---:|---:|---:|---:|---:|---:|
| GET /api/v1/events | 720 | 720 | 720 | 720 | 0 | 0.000% |
| GET /api/v1/events/{id} | 720 | 720 | 720 | 720 | 0 | 0.000% |
| GET /api/v1/events/{id}/availability | 720 | 720 | 720 | 720 | 0 | 0.000% |
| GET /api/v1/orders/{id} | 397 | 397 | 392 | 392 | 5 | 1.259% |
| GET /api/v1/orders/{id}/tickets | 144 | 144 | 144 | 144 | 0 | 0.000% |
| POST /api/v1/orders | 216 | 216 | 216 | 216 | 0 | 0.000% |
| POST /api/v1/orders/{id}/cancel | 36 | 36 | 36 | 36 | 0 | 0.000% |
| POST /api/v1/payments | 144 | 144 | 144 | 144 | 0 | 0.000% |

Tương đối = |B−A|/A × 100%; A = 0 ghi N/A. Tổng gateway A 3097, B 3092; chênh tuyệt đối 5 (0.161%). Nhịp theo 600 s lịch: 5.1617 và 5.1533 req/s. Không dùng thời gian nhận file làm thời gian tải.

Gateway missing A/B: 0/0; status/route mismatches: 0/0; duplicate IDs: 0/0; extra requests: 0/0.

Các đơn hai lượt có 0 orderId trùng; từng hành trình tạo đơn mới. Khác biệt ở số poll có thể phát sinh do chờ trạng thái bất đồng bộ; bảng chỉ ghi quan sát, chưa quy toàn bộ chênh lệch cho một cơ chế. Các lượt này không tự chứng minh khả năng mở rộng hoặc chất lượng RCA.

**Không tự đặt ngưỡng đạt độ lặp.** Claude đánh giá các chênh lệch theo quyền điều phối; L1 bàn giao số và bằng chứng. Nguồn: `out/l1r20261112v2a/analysis.json`, `out/l1r20261112v2b/analysis.json`, `gateway.jsonl`, `raw.json`, `raw.csv`, `container.log`, `summary.json`, `routes.csv` và manifest mỗi lượt. `lap-2-luot.json` lưu các bảng máy đọc được.

V1 và lượt dừng giữ riêng: `l1p20261112a`, `l1r20261112a`, `l1r20261112b`. Không dùng chúng thay xác nhận source cuối; xem `SU-CO-TRACEPARENT.md`.
