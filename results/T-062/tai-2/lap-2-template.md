# Hai lượt 10 phút — source cuối

Lượt A: `l1r20261112v2a`, @TIME_A@. Lượt B: `l1r20261112v2b`, @TIME_B@. Cùng source, cấu hình, rate 12 hành trình/10 s và mix 70/20/5/5; mỗi lượt tạo phiên PKCE mới trước cửa sổ. Snapshot/hash ở thư mục từng lượt. @INPUT_CHECK@.

| Chỉ số | A | B |
|---|---:|---:|
@SUMMARY@

Gateway đếm độc lập từ log B16 trong khoảng start-utc tới container FinishedAt, nhận completed/failed/rejected/cancelled. Bảng dưới dùng routeId thực của gateway. Refresh Keycloak và mock checkout không qua gateway; callback mock đi trực tiếp payment.

| Route gateway | k6 A | Gateway A | k6 B | Gateway B | Chênh tuyệt đối A–B | Tương đối so với A |
|---|---:|---:|---:|---:|---:|---:|
@GATEWAY_TABLE@

Theo endpoint: log gateway không ghi template path. Các số gateway dưới đây được nối theo requestId; với Event dùng correlationId khi duy nhất. Kiểm routeId và status sau nối; không tự đặt traceparent. Số k6 lấy từ counter route_responses, đối chiếu thêm JSON/CSV và console request log.

Trong các analysis v2 tạo sớm, trường tên cũ `requestTraceUniqueCount` đếm ID response duy nhất; không phải số trace. Các bản sau gọi đúng là `requestIdentityUniqueCount`. Số span/trace lấy từ bằng chứng Tempo riêng.

| Endpoint | k6 A | Gateway nối A | k6 B | Gateway nối B | Chênh tuyệt đối A–B | Tương đối so với A |
|---|---:|---:|---:|---:|---:|---:|
@ROUTE_TABLE@

Tương đối = |B−A|/A × 100%; A = 0 ghi N/A. Tổng gateway A @TOTAL_A@, B @TOTAL_B@; chênh tuyệt đối @TOTAL_DIFF@ (@TOTAL_REL@). Nhịp theo 600 s lịch: @RATE_A@ và @RATE_B@ req/s. Không dùng thời gian nhận file làm thời gian tải.

@MATCH_CHECK@

Các đơn hai lượt có @ORDER_OVERLAP@ orderId trùng; từng hành trình tạo đơn mới. Khác biệt ở số poll có thể phát sinh do chờ trạng thái bất đồng bộ; bảng chỉ ghi quan sát, chưa quy toàn bộ chênh lệch cho một cơ chế. Các lượt này không tự chứng minh khả năng mở rộng hoặc chất lượng RCA.

**Không tự đặt ngưỡng đạt độ lặp.** Claude đánh giá các chênh lệch theo quyền điều phối; L1 bàn giao số và bằng chứng. Nguồn: `out/l1r20261112v2a/analysis.json`, `out/l1r20261112v2b/analysis.json`, `gateway.jsonl`, `raw.json`, `raw.csv`, `container.log`, `summary.json`, `routes.csv` và manifest mỗi lượt. `lap-2-luot.json` lưu các bảng máy đọc được.

V1 và lượt dừng giữ riêng: `l1p20261112a`, `l1r20261112a`, `l1r20261112b`. Không dùng chúng thay xác nhận source cuối; xem `SU-CO-TRACEPARENT.md`.
