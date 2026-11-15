# T-063 — CPU-BOOK: lan chậm do tranh CPU hay do phụ thuộc? (12/11/2026 21:48Z, Claude)

Câu hỏi SPEC T-063: "CPU-BOOK lan chậm do tranh CPU hay do phụ thuộc?" → quyết định cường độ ô CPU (giảm là ứng viên, không chốt trước).

## 1. Quan sát trên ca T-062 `bf17acbf` (E1, 2 luồng đốt, 600 s, tải đọc 5 req/s)

Nguồn: `cpu-container.json` (từ `results/T-062/ca/_metric-bo-sung/`, `cpu_container.py`); `results/T-062/ca/bf17acbf/outputs/bf17acbf/method-output-1.json`.

- CPU trung bình (lõi) N = [t−300, t) → L1 = [t, t+150): Booking 0,006 → 0,969 (chạm quota 1,0). Mọi container khác **không đổi** (vd. Event 0,0078 → 0,0076; Postgres 0,0172 → 0,0173; RabbitMQ 0,131 → 0,129). Máy: 0,38 → 1,37 lõi bận trên 2 lõi (còn ~0,63 lõi rảnh trung bình).
- M1 P7 gắn cờ `tu_sinh` cho 7 thành phần (gồm Event, Payment, Ticket, Keycloak, Gateway, Discovery). Ở Event, tỷ lệ lời gọi vượt phân vị 95 của nền tăng mạnh ở thao tác SQL không liên quan Booking: `SELECT event_schema.tbl_event_images` r_A = 0,66 (nền 0,049), `tbl_ticket_types` 0,67, `event_db` 0,54. Job nền Ticket (`TicketJobs.publish` 0,28) và SQL Payment (`tbl_payment_attempts` 0,61) cũng tăng.
- Xác nhận can thiệp D2 (`results/T-062/tiem-loi/d2-xac-nhan-a2a95419.md`): Booking `nr_throttled` +1266 trong 150 s (≈ 84% chu kỳ), `cpu.pressure some avg10` 52%; p50 Event −2 ms (p50 không đổi).

→ Quan sát: service khác chậm ở **đuôi phân phối** trong khi CPU trung bình 10 s của chúng không đổi. Hai giải thích: H-phụ-thuộc (chậm lan qua lời gọi tới Booking) và H-cụm (Booking chiếm cả hai lõi theo cụm trong mỗi chu kỳ CFS 100 ms rồi bị throttle, các tiến trình khác chờ CPU). H-phụ-thuộc không giải thích được SQL của Event chậm (đường Event → Postgres không gọi Booking).

## 2. Phép thử phân xử (21:42–21:47Z, `exp-app`, không tải k6)

Script: [`thu_cuong_do.py`](thu_cuong_do.py) (cùng cơ chế đốt với `~/inj.py`), đầu ra thô [`thu-cuong-do-lan1.jsonl`](thu-cuong-do-lan1.jsonl). Đo 10 lần/s: HTTP `GET /api/v1/events?size=1` qua Gateway (Gateway → Event → Postgres, không qua Booking) và RTT Postgres trực tiếp (SSLRequest); áp lực CPU máy `/proc/pressure/cpu` (some); cgroup Booking.

| Pha (60 s, trừ ghi chú) | Booking dùng (lõi) | Chu kỳ bị throttle | Máy bận (lõi/2) | PSI some (ms/s) | HTTP p50 / p90 / p99 (ms) | PG p90 / p99 (ms) |
|---|---|---|---|---|---|---|
| nền 1 | 0,003 | 0 | 0,53 | 101 | 9,5 / 14,0 / 22,3 | 2,2 / 4,6 |
| **2 luồng** | 0,954 | **0,839** | 1,44 | **640** | 9,8 / **24,0** / **69,0** | 3,3 / 7,7 |
| nghỉ (25 s) | 0,004 | 0 | 0,47 | 89 | 9,0 / 12,2 / 15,6 | 2,0 / 9,6 |
| **1 luồng** | 0,957 | 0,033 | 1,44 | 206 | 10,7 / 17,0 / 26,4 | 3,2 / 7,0 |
| nghỉ (25 s) | 0,003 | 0 | 0,47 | 85 | 8,8 / 12,4 / 17,5 | 2,1 / 3,3 |
| nền 2 (40 s) | 0,003 | 0 | 0,53 | 97 | 9,0 / 12,9 / 23,5 | 2,1 / 3,4 |

## 3. Kết luận (tách quan sát / suy luận / chưa kiểm)

- **Quan sát.** Ở cùng lượng CPU Booking tiêu thụ (0,954 vs 0,957 lõi) và cùng mức bận máy (1,44 lõi), 2 luồng cho áp lực CPU máy gấp ~3 lần và p99 của đường không qua Booking gấp ~2,6 lần so với 1 luồng; 1 luồng vẫn làm đuôi tăng nhẹ (p90 +21%, p99 +19% so với nền 1).
- **Suy luận (cơ chế, mức đã kiểm).** Trong điều kiện quota 1 lõi + 2 luồng bận trên máy 2 lõi, bộ lập lịch CFS cho Booking chạy trên **cả hai lõi** trong phần đầu mỗi chu kỳ 100 ms tới khi hết quota rồi throttle (84% chu kỳ bị throttle). Trong các cụm đó mọi tiến trình khác (Postgres, Event…) phải chờ CPU → trễ đuôi tăng ở service không phụ thuộc Booking, trong khi CPU trung bình của chúng không đổi. Đây là **nhiễu hàng xóm qua CPU của máy**, không phải lan qua lời gọi. Bằng chứng: đầu vào (số luồng) → xử lý (throttle, PSI) → trung gian (trễ đường không qua Booking) → đầu ra (cờ M1 lan mọi service). H-phụ-thuộc bị loại cho các thao tác không gọi Booking.
- **Hệ quả cho đánh giá.** Ở CPU-BOOK 2 luồng, các cờ ở service khác là **triệu chứng thật** của tranh CPU máy, không phải lỗi phát hiện của M1; đáp án gốc (Booking) không đổi. Ô này đo khả năng M1 phân biệt "nguồn chiếm CPU" với "nạn nhân chờ CPU" — chính là việc của H2 (kênh JVM/cgroup: throttling chỉ có ở Booking).
- **Chưa kiểm.** (a) n = 1 lượt mỗi pha, không tải k6 (chỉ 10 req/s thăm dò); dưới tải mua vé mức ảnh hưởng có thể khác. (b) Chưa đo trực tiếp phân bố "hai lõi bận cùng lúc" theo ms (cần `perf sched` hoặc `schedstat`); cơ chế cụm là suy luận từ throttle + PSI, chưa quan sát trực tiếp. (c) Throttling theo container trên Prometheus mới có từ 21:39Z (TD-03), không áp được cho 9 ca cũ.

## 4. Đề xuất cho ô dev (đưa vào `o-dev-bo-sung.md`; quyết định ghi WHY khi chốt danh mục)

- Giữ **hai cường độ là hai ô dev khác nhau**, không thay ô này bằng ô kia: `CPU-BOOK-1` (1 luồng: bão hòa quota cục bộ, ít nhiễu máy) và `CPU-BOOK-2` (2 luồng, = cường độ T-062: nhiễu hàng xóm). Lý do: hai cơ chế khác nhau, mỗi cái kiểm một điều kiện thất bại khác của M1/H2; chọn một cường độ "cho M1 dễ" là chỉnh theo đáp án.
- Đầu dò xác nhận: `nr_throttled`/`throttled_usec` của cgroup Booking (đã có trong `inj.py probe`) + metric mới `container_cpu_throttling_data_*` trên Prometheus.
