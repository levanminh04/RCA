# T-063 thu3 — Điều kiện hậu kiểm can thiệp từng ca (khai trước khi phát đợt thu chính)

**Ghi lúc:** 14/11/2026 ~05:52Z (bản nháp), chốt lúc ghi dòng "Chốt" ở cuối file, **trước** khi phát `runner4.py thu --lich lich-3.json`. **Chưa xem dữ liệu của lượt chính** (lượt chính chưa phát). Dữ liệu đã xem: chạy thử cường độ pool (`do/thu-pool*.jsonl`), chạy thử toxic H4 (`do/thu-h4b*.jsonl`), chạy thử `runner4` một chu kỳ rút ngắn (`thu3-thu-ngan`, không phải ca RCA).

Khuôn theo `results/T-063/chay/dieu-kien-xac-nhan.md` (đợt 2). Script: `results/T-063/thu3/scripts/xac_nhan_ca_3.py` (sinh bằng `scripts/tao_xac_nhan_ca_3.py` từ `chay/xac_nhan_ca.py`; diff 87 dòng). Không dùng điểm M1. Nhãn và kết quả nằm phía chấm. Nguồn đầu dò độc lập với M1: đầu dò `inj3.py` trên `exp-app` (toxiproxy API, `rabbitmqctl`, cgroup, docker inspect, audit hook), file audit đầy đủ, Prometheus `exp-obs` (chỉ kênh pool cho POOL-EVENT, như đợt 2 dùng httpcheck cho PAUSE). M1 không đọc sổ, audit hay đầu dò.

## Cửa sổ

Mỗi chu kỳ có `S` (mốc tải) và `t = S + 600`. Nền N = [t − 570, t − 30]; lỗi L = [t + 30, t + 570]; sau = [t + 610, t + 1170]. Prometheus `query_range` bước 15 s.

## Điều kiện chung (mọi ca)

- C0: sổ `so-thu3.jsonl` có `cycle-begin`, `load-start`, `cycle-end`; không có `cycle-error` hay `dirty` của mã đó. Ô có lỗi: có `fault-start` (không phải `fault-start-failed`) và `fault-stop`.
- C1: k6 của chu kỳ `ExitCode = 0`; **C1-bậc**: `run.json.multiplier` bằng `multiplier` ghi ở `cycle-begin` (1 hoặc 3). Ghi `dropped_iterations`, `journey_failed`, `token_refresh_failure`; các số này không làm điều kiện loại.

## Điều kiện riêng

Chuỗi so khớp đã đối chiếu với đầu ra thật của đầu dò trong chạy thử: `toxics` là dict `proxy → ["t063:{'rate': 1}"]` (rỗng = `[]`); `payment_state` = `"running false"`; `burn_procs` = `"0"`; `rabbit_booking.ready_tong`, `.unacked_tong` là số nguyên; audit Event có trường `operation`, `timestamp`.

| Ô | Xác nhận khi (tất cả đúng) |
|---|---|
| POOL-EVENT | audit đầy đủ `event-service/audit/executions.jsonl`: có `pool.hold.started` trong [t, t + 605]; không có dòng `pool.*` trong [t − 600, t) và (t + 605, t + 1200]. Prometheus `max(db_client_connections_usage{service_name="event-service",state="used"})`: tb(L) ≥ 4,5; tb(N) ≤ 3; tb(sau) ≤ 3. `max(db_client_connections_pending_requests{service_name="event-service"})`: max(L) ≥ 1; tb(N) < 0,5 |
| CONSUMER-BOOK-SLOW-X3 | đầu dò t+60 và t+330 có toxic trên `booking-amqp`; hoi+60 không còn toxic nào; tồn queue Booking (ready + unacked, `booking.*.q`) ở t+330 ≥ 10; ở hoi+60 ≤ 2; C1-bậc = 3 |
| EVENT-DB-LAT | như đợt 2: t+60 và t+330 có toxic trên `event-jdbc`; `pg_sslrequest_ms.proxy_event` ≥ 20 ở cả hai; hoi+60 không còn toxic |
| RECREATE-PAY | đầu dò `payment_container` (`Id StartedAt RestartCount`): Id ở t+60 khác Id ở t−240, và Id ở t+60 = t+330 = hoi+60 (đổi đúng một lần); `StartedAt` của container mới trong [t, t + 60]; `payment_state` = `running false` ở t+330 và hoi+60; Prometheus `max(httpcheck_error{http_url=~".*:8083.*"})` trong [t + 180, t + 570] bằng 0 (đã phục hồi) |
| BINH-THUONG, BINH-THUONG-X3 | mọi đầu dò: không toxic, `burn_procs` = 0, `payment_state` = `running false`; audit Event không có `http.error.executed` và không có `pool.*` trong [t − 600, t + 1200]; BINH-THUONG-X3 thêm C1-bậc = 3 |

Ghi thêm, không làm điều kiện: max `httpcheck_error` :8083 trong [t, t + 120] của RECREATE-PAY (hụt liveness lúc JVM khởi động); ID kết nối AMQP của Booking ở t+60/t+330/hoi+60 (rớt kết nối thì ghi), tồn queue Booking ở mọi đầu dò của ca không lỗi, `pool_used`/`pending` trung bình.

## Đầu ra

`results/T-063/thu3/xac-nhan-ca-3.json`: mỗi mã mờ một mục (ô, `xac_nhan`, từng điều kiện kèm số đo, lý do khi false). Lỗi hạ tầng (thiếu đầu dò, Prometheus mất mẫu, thiếu audit) ghi `khong_du_du_lieu`, tách khỏi "không xác nhận"; ca đó không vào tập chọn. Ca không đạt không vào tập chọn, ghi lý do. Nếu sai do chép điều kiện: khai "Sửa sau" riêng ở cuối file này, giữ cả hai kết quả, chờ Minh.

## Chốt — 14/11/2026 06:16Z

Đối chiếu với đầu ra thật trước khi chốt: `xac_nhan_ca_3.py` chạy trên chạy thử `runner4` (`thu3/thu-ngan/xac-nhan-thu.json`: ca thử `69845d29` CONSUMER-BOOK-SLOW-X3 xác nhận, mọi điều kiện đọc được, tồn t+60/t+330/hoi+60 = 5/616/0); định dạng `payment_container` lấy từ chạy thử RECREATE-PAY (`exp-app:~/t063/thu3/thu-recreate.jsonl`: `"<Id> <StartedAt> <RestartCount>"`); số pool lấy từ chạy thử cường độ (`do/thu-pool-prom.json`). Ngưỡng ở bảng trên không đổi sau các phép đối chiếu này. **Chưa xem dữ liệu của lượt chính** (chưa phát).

## Sửa sau — 14/11/2026 ~10:50Z (SAU KHI xem kết quả hậu kiểm lượt chính; chờ Minh xác nhận)

Phần trên giữ nguyên (bản đã băm khi đóng băng bản 3: sha256 `9dbdca16…`; mục này thêm sau). Kết quả theo bản chốt: `xac-nhan-ca-3.json` (script `scripts/xac_nhan_ca_3-ban-chot.py`, sha256 `3962e4b3…` = hash trong `dong-bang-3.json`): **4/6 xác nhận**. Kết quả theo hai sửa dưới: `xac-nhan-ca-3-sua-sau.json` (cờ `--sua-sau-1 --sua-sau-2`, cài bằng `scripts/va_sua_sau.py`; chạy không cờ cho kết quả trùng bản chốt ở mọi ca và mọi điều kiện): **6/6**.

- **Sửa sau 1 (sửa cài đặt, không đổi điều kiện).** Ca BINH-THUONG-X3 trượt `C0_chu_ky`. Điều kiện khai trước ghi "Ô có lỗi: có `fault-start` và `fault-stop`"; BINH-THUONG-X3 là ô không lỗi, sổ có đủ `cycle-begin`, `load-start`, `mark`, `cycle-end`, không `cycle-error`/`dirty`. Script chép từ đợt 2 chỉ coi BINH-THUONG, FLASH-HEALTHY là ô không lỗi trong C0 (quên thêm BINH-THUONG-X3 ở dòng này, dù đã thêm ở nhánh điều kiện riêng). Sửa: C0 dùng đúng bộ ô không lỗi. Các điều kiện khác của ca đều đạt ở cả hai lần chạy.
- **Sửa sau 2 (sửa điều kiện).** Ca RECREATE-PAY trượt `httpcheck_phuc_hoi_t180_t570`: `query_range` cho max = 1 trong [t + 180, t + 570]. Mẫu thô (`httpcheck_error{http_url=~".*:8083.*"}[600s]` tại t + 570) chỉ có ở t + 3, 13, 23, 33, 43 (connection refused); `httpcheck_status` 401 có mẫu liên tục trước và sau, hở đúng khoảng đó. Nguyên nhân trượt: chuỗi đẩy qua OTLP không có dấu stale, Prometheus giữ giá trị cuối 5 phút (lookback) nên `query_range` thấy 1 tới ~t + 343. Lỗi do tôi đặt điều kiện mà không tính lookback. Sửa: "phục hồi" = không có mẫu thô `httpcheck_error` nào trong [t + 180, t + 570]. Các điều kiện khác của ca (Id đổi đúng một lần, `StartedAt` = t + 5 s, payment chạy ở t+330 và hoi+60) đều đạt.
- **Đề xuất của người làm:** nhận cả hai sửa (6 ca). Lý do: sửa 1 không đổi nội dung điều kiện; sửa 2 dùng chính nguồn đầu dò đã khai, chỉ bỏ hiệu ứng lookback của truy vấn, và bằng chứng thô cho thấy payment phục hồi ở ~t + 53. Mặt trái: cả hai sửa làm sau khi xem kết quả; nếu Minh không nhận, BINH-THUONG-X3 và RECREATE-PAY ra khỏi tập chọn, H4 mất đối chứng cùng bậc tải. Phương án khác: thu lại hai ô này với điều kiện đã sửa khai trước (~1 giờ máy).

**Minh nhận "Sửa sau 1" và "Sửa sau 2" (14/11/2026 ~11:00Z):** "Nhận cả hai". Kết quả hậu kiểm dùng: `xac-nhan-ca-3-sua-sau.json` (6/6). Ghi tại `docs/DECISIONS.md`, mục "Thu bù 3 (T-063): nhận "Sửa sau 1" và "Sửa sau 2", 14/11/2026".
