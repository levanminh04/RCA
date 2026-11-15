# T-063 — Điều kiện hậu kiểm can thiệp từng ca (khai trước khi xem dữ liệu đợt thu chính)

**Ghi lúc:** 13/11/2026 ~07:30Z. Đợt thu chính phát 07:13Z. Khi ghi file này, chưa đọc đầu dò, metric hay audit của bất kỳ chu kỳ nào trong lượt chính; dữ liệu duy nhất đã xem là lượt thử `865c8e93`.

**Nguồn yêu cầu:**
- `tasks/T-063-quan-sat-thu-dev-2/REVIEW.md` R3: hậu kiểm, ghi từng mã mờ trước khi T-064 khai tập chọn.
- `results/T-064/tieu-chi-chon.md` dòng 14: ca có can thiệp không được đầu dò xác nhận thì không vào tập chọn.
- Bằng chứng từng ô theo `D2B-KET-QUA.md`.

**Mục đích:** chỉ xác nhận can thiệp đã xảy ra đúng chỗ, đúng khoảng. Không dùng điểm M1. Nhãn và kết quả nằm phía chấm, không đưa vào phương pháp.

## Cửa sổ

Mỗi chu kỳ có `S` (mốc tải) và `t = S + 600` (mốc lỗi). Các cửa sổ:
- nền N = [t − 570, t − 30];
- lỗi L = [t + 30, t + 570];
- sau = [t + 610, t + 1170].

Prometheus dùng `query_range` bước 15 s.

## Điều kiện chung (mọi ca)

- C0: sổ có `cycle-begin`, `load-start`, `cycle-end`; không có `cycle-error` hay `dirty` của mã đó. Với ô có lỗi: có `fault-start` (không phải `fault-start-failed`) và `fault-stop`.
- C1: k6 của chu kỳ có `ExitCode = 0`. Ghi `dropped_iterations`, `journey_failed`, `token_refresh_failure` để báo cáo; các số này không làm điều kiện loại.

## Điều kiện riêng

| Ô | Xác nhận khi (tất cả đúng) |
|---|---|
| EVENT-DB-LAT | đầu dò t+60 và t+330 có toxic trên `event-jdbc`; `pg_sslrequest_ms.proxy_event` ≥ 20 ở cả hai; đầu dò hoi+60 không còn toxic |
| REDIS-BOOK | t+60 và t+330 có toxic trên `booking-redis`; `redis_ping_ms.proxy` ≥ 150 ở cả hai; hoi+60 không còn toxic |
| NET-GW-BOOK | t+60 và t+330 có toxic trên `gateway-booking-http`; p50 `http_client_request_duration_seconds` của `api-gateway` tới `127.0.0.1:18082`: tb(L) − tb(N) ≥ 200 ms; hoi+60 không còn toxic |
| HTTP5-EVENT, HTTP5-EVENT-FLASH | file audit **đầy đủ** `event-service/audit/executions.jsonl`, `operation = http.error.executed`, đúng `targetId` của ô: có trong [t, t+605]; phủ ≥ 90% các khe 30 s của [t, t+600]; không có trong [t − 600, t) và (t + 605, t + 1200]. Không dùng số đếm đuôi 2000 dòng của đầu dò (đã bão hòa, `HO-SO-LUOT.md` phụ lục) |
| CPU-BOOK-1 / CPU-BOOK-2 | `burn_procs` = 1 / 2 ở t+60 và t+330; `cgroup_booking.nr_throttled` tăng từ t+60 tới t+330; `burn_procs` = 0 ở hoi+60 |
| PAUSE-PAYMENT | `payment_state` = `running true` ở t+60 và t+330; `running false` ở hoi+60; max `httpcheck_error{http_url=~".*:8083.*"}` trong L ≥ 1 và trong N bằng 0 hoặc vắng |
| BINH-THUONG, FLASH-HEALTHY | mọi đầu dò: không toxic, `burn_procs` = 0, `payment_state` = `running false`; audit không có `http.error.executed` trong [t − 600, t + 1200] |

Ghi thêm cho FLASH-HEALTHY và HTTP5-EVENT-FLASH (không làm điều kiện): số hành trình bắt đầu sau t chia trước t, lấy từ k6 `raw.json`. Số kỳ vọng ~3.

## Đầu ra

`results/T-063/chay/xac-nhan-ca.json`: mỗi mã mờ một mục, gồm ô, `xac_nhan` true/false, từng điều kiện kèm số đo, và lý do khi false.

Lỗi hạ tầng (thiếu dữ liệu đầu dò, Prometheus mất mẫu) ghi `khong_du_du_lieu`, tách khỏi "không xác nhận". Ca thiếu dữ liệu không vào tập chọn. Lượt bù cho ca đó do Minh quyết.

Script: `results/T-063/chay/xac_nhan_ca.py`.

## Sửa sau 1 — 13/11/2026 ~14:20Z (SAU KHI xem đầu dò; chờ Minh xác nhận)

- **Thấy gì:** lượt chạy theo điều kiện khai trước cho kết quả `results/T-063/chay/xac-nhan-ca.json`: 12/13 xác nhận. PAUSE-PAYMENT (`46aab4be`) trượt đúng một điều kiện, `paused_t60_t330`. Đầu dò ghi `payment_state = "paused true"` ở t+60 và t+330, `running false` ở t−240 và hoi+60. httpcheck :8083 max = 1 trong lỗi và vắng ở nền; 159 hành trình lỗi.
- **Vì sao sai:** đầu dò in `{{.State.Status}} {{.State.Paused}}`. Khi bị pause, Docker báo Status = `paused`. Điều kiện khai trước viết `running true` là lỗi chép của Claude. Nguồn mà điều kiện dẫn, `D2B-KET-QUA.md`, ghi "`Paused=true`".
- **Sửa:** pause được xác nhận khi cờ Paused (từ cuối chuỗi) là `true` ở t+60 và t+330. Các điều kiện khác của ô giữ nguyên. Chạy bằng cờ `--sua-sau-1` → `results/T-063/chay/xac-nhan-ca-2.json`.
- **Giữ cả hai kết quả.** Chấm T-064 báo tập 12 ca (theo điều kiện khai trước) và tập 13 ca (theo sửa sau 1). Minh quyết dùng tập nào.

**Minh nhận "Sửa sau 1" (13/11/2026 ~23:19Z):** "Đồng ý, dùng 13 ca". Kết quả hậu kiểm dùng: `xac-nhan-ca-2.json`. Ghi tại `docs/DECISIONS.md`, mục "Tập chọn dev bản 2: nhận "Sửa sau 1", dùng 13 ca".
