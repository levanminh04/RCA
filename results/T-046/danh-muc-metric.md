# T-046 Phần M — Danh mục metric tiêu biểu (M1–M2, bản ứng viên)

- **Trạng thái:** ứng viên, **chưa kiểm** tác dụng lên RCA. Viết ngày 01/11/2026, trước khi tính bất kỳ số nào riêng cho danh mục. Phép kiểm không nhãn (M3) nằm ở `danh-muc-metric-m3-sua2.json` (bản trước: `danh-muc-metric-m3.json`).
- Danh mục được viết sau khi đã xem A/A và C-e của dev cho cổng (tỷ lệ qua giả theo loại kênh).
- **Không thay WHY-59.** WHY-59 (Q-209) quyết giữ mọi cột metric, và đã bác "chỉ giữ P90" theo WHY-27. Muốn dùng danh mục trong M1 (M4) hay so với toàn bộ metric ở T-047 (M5) thì Minh phải quyết lại WHY-59. Trước đó phải khai đủ mục tiêu phép so, cấu hình K, ngân sách chọn, ngưỡng `verdict` và điều kiện giữ phản ứng (phản biện lượt 1 của Codex, R3).
- **Phạm vi:** đây là danh mục cho **chẩn đoán**, không phải cho cảnh báo.
  - Cảnh báo dùng tín hiệu triệu chứng: golden signals, SLO.
  - Chẩn đoán cần thêm tín hiệu phía nguyên nhân theo từng thành phần: USE và bão hòa riêng theo loại.
  - Không lấy giới hạn chuỗi của bản sao lên Grafana Cloud làm giới hạn đầu vào RCA.

## 1. Nguyên tắc

1. **Theo loại nút**, mỗi loại một bộ tín hiệu cố định:
   - service: RED (tốc độ request, lỗi, thời gian);
   - tài nguyên của tiến trình hay container: USE (mức dùng, bão hòa, lỗi);
   - kho dữ liệu, broker, máy: tín hiệu bão hòa riêng.
   - Nguồn: Google SRE book, chương "Monitoring Distributed Systems" (bốn golden signals); B. Gregg, "The USE Method"; T. Wilkie, "The RED Method"; OpenTelemetry semantic conventions (HTTP, database, messaging metrics).
2. **Một tín hiệu một kênh tiêu chuẩn.** Bỏ biến thể đo cùng đại lượng, vì khóa xếp hạng của E4 đếm số kênh và cộng điểm.
   - cpu theo lõi và theo %: giữ %.
   - mem theo MiB và theo %: giữ %.
   - Nhiều phân vị độ trễ: giữ P90.
3. **Ưu tiên phía chính thành phần.** Độ trễ phía server phản ánh chính service. Độ trễ phía client là tổng hợp lời gọi đi trên mọi đích, nên không phải tín hiệu của một cạnh. Thông tin cạnh lấy từ trace (E2). (Sau M3: giữ một kênh client P90 như tín hiệu riêng, vì không trùng phía server; xem mục 3.)
4. **Không bỏ tín hiệu phía nguyên nhân** chỉ vì nó ồn. Lỗi tiêm của RE2-TT gồm cpu, mem, disk, socket, delay, loss. Kênh ồn xử lý ở cổng hoặc ở cách biến đổi, không xử lý bằng cách bỏ.
5. **Không chọn theo MRR dev.** Danh mục định từ nguyên tắc trên; tác dụng đo sau bằng luật C, theo đúng điều kiện ở phần trạng thái.

## 2. Danh mục theo loại nút

| Loại nút | Tín hiệu | Kênh tiêu chuẩn | RE2-TT | Nezha-OB | FlashTicket (B16 §5; tên kênh cần kiểm ở phiên bản dùng) |
|---|---|---|---|---|---|
| Service | Rate | request/giây | `workload` | `PodWorkload-Ops` | `http.server.request.duration` (đếm) qua Micrometer/OTel |
| Service | Errors | tỷ lệ lỗi hoặc tỷ lệ thành công | `error` | `PodSuccessRate-pct`; `FrontSuccessRate-pct` (frontend) | đếm 5xx/lỗi theo route mẫu |
| Service | Duration | P90 phía server | `latency-90` | `PodServerLatencyP90-s` | histogram duration, P90 |
| Tiến trình/container | CPU, mức dùng | % | `cpu` | `CpuUsageRate-pct` | CPU container |
| Tiến trình/container | CPU, bão hòa | throttling | không có | không có | **thiếu**: cần CPU throttling của container |
| Tiến trình/container | Bộ nhớ | % hoặc working set so với giới hạn | `mem` | `MemoryUsageRate-pct` | RAM container; heap JVM, GC pause: **chưa có trong B16** |
| Tiến trình/container | Đĩa I/O | thông lượng hoặc số syscall | `diskio` | `SyscallRead`, `SyscallWrite` | disk (B16 hạ tầng) |
| Service | Duration gọi đi | P90 phía client (sửa sau M3) | không có | `PodClientLatencyP90-s` | duration của HTTP client theo đích logic |
| Tiến trình/container | Mạng | byte vào/ra; kết nối | `socket` | `NetworkReceiveBytes`, `NetworkTransmitBytes` | **thiếu** mạng theo container |
| Tiến trình/container | Lỗi | restart, OOM | không có | không có | restart/OOM (B16) |
| Kho dữ liệu, cache | Bão hòa, thời gian | pool kết nối đang dùng/chờ; thời gian truy vấn | không có | không có | connection pool, lock wait, transaction duration (B16) |
| Broker | Bão hòa | hàng đợi ready/unacked, tuổi | không có | không có | queue ready/unacked, backlog/age (B16) |
| Máy | USE máy | CPU, RAM, disk, mạng của host | không có | không có | CPU/RAM/disk host (B16); **thiếu** mạng host |
| Hạ tầng quan sát | Mất dữ liệu | collector dropped/export failure | không có | không có | có (B16). Dùng cho trạng thái quan sát (B1.3b), không phải kênh chấm |

## 3. Ánh xạ: kênh bị bỏ khỏi danh mục và lý do

| Dataset | Kênh bỏ | Lý do (nguyên tắc) |
|---|---|---|
| RE2-TT | `latency-50` | Cùng tín hiệu Duration với `latency-90`; giữ P90 (nguyên tắc 2) |
| Nezha-OB | `CpuUsage-m` | Cùng đại lượng với `CpuUsageRate-pct` (nguyên tắc 2) |
| Nezha-OB | `MemoryUsage-Mi` | Cùng đại lượng với `MemoryUsageRate-pct` (nguyên tắc 2) |
| Nezha-OB | `PodServerLatencyP95-s`, `PodServerLatencyP99-s` | Biến thể phân vị (nguyên tắc 2) |
| Nezha-OB | `PodClientLatencyP95-s`, `PodClientLatencyP99-s` | Biến thể phân vị của độ trễ gọi đi (nguyên tắc 2). **Sửa 19:20 sau M3:** giữ `PodClientLatencyP90-s` như tín hiệu riêng "độ trễ gọi đi", vì tương quan với `PodServerLatencyP90-s` chỉ 0,44 (`danh-muc-metric-m3.json#/tuong_quan_kenh_bo_kenh_giu`); bản đầu bỏ cả ba theo nguyên tắc 3 |

- RE2-TT giữ 7/8 loại kênh; Nezha-OB giữ 11/17 (bản đầu 10/17, sửa sau M3). Số đơn vị metric hợp lệ mỗi cửa sổ thật, trung vị: RE2-TT 361 → 333; Nezha-OB 154 → 94, bản đầu 84 (`danh-muc-metric-m3-sua2.json#/so_don_vi_metric_that`).
- M3, mức trùng (Spearman): cpu m~% và mem Mi~% của Nezha-OB 1,0; server P95~P90 0,95, P99~P90 0,81; RE2-TT latency-50~90 0,91. Qua giả theo loại kênh ở A/A RE2-TT với G3: mem lên 0,368, latency 0,11–0,12, cpu 0,06–0,11 (`#/qua_cong_aa_theo_hau_to`); danh mục không giải quyết qua giả của kênh giữ lại. Đây là tỷ lệ qua cổng, không phải cờ: mem qua cổng nhiều nhưng gần như không tạo cờ (`bao-cao.md` mục 1).
- C-e theo loại kênh, RE2-TT: `danh-muc-metric-m3-sua2.json#/qua_cong_ce_G3_theo_hau_to_RE2`. Nezha-OB không có C-e.
- **M3 hoàn thành một phần:** độ phủ theo thành phần gốc cần nhãn, chưa làm; tác dụng lên RCA chưa kiểm (M4–M5).
- **Chưa kiểm:** P90 có phải phân vị tốt nhất cho chẩn đoán không (P99 nhạy với đuôi hơn nhưng ồn hơn). Bỏ độ trễ phía client có làm mất tín hiệu khi bên được gọi không có metric không (giả thuyết thứ ba của P4: thành phần gốc thiếu tín hiệu).

## 4. Chỗ thiếu ở FlashTicket (đề xuất cho yêu cầu quan sát P9a; chưa trình, chưa duyệt)

- CPU throttling của container: bão hòa CPU; mức dùng % không thấy khi chạm quota.
- Heap JVM và thời gian GC pause: bão hòa bộ nhớ của service Java; RAM container không phân biệt heap.
- Mạng theo container và theo host: lỗi tiêm mạng (delay, loss) cần tín hiệu phía mạng ngoài độ trễ.
- Đặt danh mục thành một yêu cầu R-11 khi lập P9a. T-040 đã đóng; không sửa tệp R-01–R-10.
