# T-067 — Tải 1 giờ trên bản ghim (bước 8)

Bản: `rca/exp-2026-11` = `36a3725d…` (image `arm64-t067-36a3725d`). Lượt k6 `t067-tai-1gio-001`: 18/11/2026 07:57:34–08:57:36Z,
×1 như tải chuẩn T-063 (12 hành trình/10 s, hỗn hợp 70/20/5/5), bộ điều khiển `tai_linux.py` (lab `8dccb34`).
Tiêu chí khai trước và commit trước khi chạy: lab `862b208` `tests/signals/tieu-chi.json#/buoc_8`.

| Tiêu chí (khai trước) | Ngưỡng | Kết quả | Nguồn |
|---|---|---|---|
| Tỷ lệ hành trình hỏng | ≤ 0,5% | 0 / 4321 (không có mẫu `journey_failed`) | `k6/t067-tai-1gio-001/summary.json#/metrics/journey_failed` |
| Hành trình xong / bắt đầu | ≥ 99% | 4321 / 4321 = 100% | `#/metrics/journey_finished`, `#/metrics/journey_started` |
| `dropped_iterations` | 0 | 0 (không có mẫu) | `#/metrics/dropped_iterations` |
| p95 `http_req_duration{expected_response:true}` | ≤ 1000 ms | 339,6 ms (p99 591,6 ms) | `#/metrics/http_req_duration{expected_response:true}` |
| Request lỗi | (báo) | 0 / 19.824 | `#/metrics/http_req_failed` |
| Đơn COMPLETED đúng số vé | mọi đơn | 864 đơn, tổng số lượng 864, tổng vé 864, lệch 0 | `tai-1-gio/don-db.json` (psql trên exp-app sau lượt) |
| OOM, restart (14 container exp-app) | 0 | 0 OOM, 0 restart, `StartedAt` không đổi | `tai-1-gio/container-truoc.json` (07:56:38Z), `container-sau.json` (08:58:17Z) |
| Bộ đếm rớt/lỗi Collector agent (exp-app) | tăng 0 | 0; uptime không reset, 360 mẫu/3600 s | `tai-1-gio/collector.json#/collector/agent` |
| Bộ đếm rớt/lỗi Collector gateway (exp-obs) | tăng 0 | 0; uptime không reset, 360 mẫu/3600 s | `tai-1-gio/collector.json#/collector/gateway` |
| Container k6 | — | exit 0, không OOM; 12 file nhận về khớp hash | `tai_linux receive` (LOG) |

Theo dõi giữa lượt (mỗi 10 phút, 08:09–08:49Z): luôn 0 restart, 0 OOM, mọi container đang chạy.

**Kết luận:** đạt mọi tiêu chí đã khai cho tải ×1 trong 1 giờ.

**Giới hạn của phép đo:**
- ~~Bộ đếm Collector: các họ `exporter_send_failed_*`, `enqueue_failed_*`, `processor_dropped_*` không có chuỗi; chưa phân xử.~~ **Bổ sung sau phản biện nội bộ (18/11, Minh duyệt; không đổi tiêu chí), `tai-1-gio/collector-2.json` (`tai_kiem.py` bản 2):**
  - `processor_dropped_*` **không tồn tại** ở Collector 0.165 (đọc endpoint `:8888` của agent). Bản 1 của `tai_kiem.py` dùng sai tên. Đo lại bằng `processor_incoming_items` − `outgoing_items`: mọi processor của cả hai Collector chênh 0, trừ `filter/health` của agent bỏ 2.521 span `/actuator/health*` theo thiết kế (≈ 7 đích dò × 360 lần/giờ).
  - `send_failed_*`, `enqueue_failed_*` chỉ được tạo ở lần lỗi đầu (trước đây gateway từng có chuỗi `send_failed_log_records`), nên không có chuỗi nghĩa là chưa lỗi.
  - Đối chiếu đầu–cuối trong cửa sổ: agent gửi 1.136.825 span và 95.468 dòng log qua `otlp`; gateway nhận đúng 1.136.825 span và 95.468 dòng; chênh 0.
  - Kết luận "bộ đếm rớt bằng 0" giữ nguyên, nay có bằng chứng trực tiếp. `collector.json` (bản 1) giữ nguyên.
- Trạng thái đơn trong lượt: EXPIRED 168, CANCELLED 216, PENDING_PAYMENT 48, khớp hỗn hợp có nhánh bỏ dở và hủy. Số khớp hỗn hợp: COMPLETED 864 = 20% × 4321; CANCELLED 216 = 5% (hủy); EXPIRED 168 + PENDING_PAYMENT 48 = 216 = 5% (bỏ dở). 48 đơn PENDING_PAYMENT là đơn bỏ dở gần cuối lượt chưa hết hạn lúc truy vấn [suy luận từ số đếm; chưa kiểm thời điểm hết hạn].
- Không so với bản 3; W3 đo.
