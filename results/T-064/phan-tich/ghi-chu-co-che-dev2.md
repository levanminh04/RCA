# T-064 — Ghi chú cơ chế trên tập chọn dev bản 2 (bản làm việc, ghi trong lúc lô chạy)

Mỗi mục tách: quan sát (có đường dẫn) → suy luận → trạng thái. Chưa kết luận giữ/bỏ khi lô chưa đủ 27 bản.

## Q1. Booking bị cờ ở ca không lỗi (P7) — 13/11 ~14:35Z

- **Quan sát.** Nguồn `results/T-064/cham/dau-ra-dev2/P7/<mã>/method-output-1.json#/extra/kenh_co`.
  - P7 trả `CAUSE_FOUND` ở 4/5 ca không lỗi; Booking hạng 1 ở cả 4.
  - 3 ca BINH-THUONG (eb48d6b3, 729604d2, f20b0ca5): Booking có 1–2 cờ, đều là đơn vị thao tác DB đơn lẻ, lớp `khong_lan`. Ví dụ: `Session.persist IdempotencyRequest`, `Session.merge PurchaseLimit`, `UPDATE tbl_purchase_limits`, `SELECT tbl_outbox_messages`. `s` lớn nhất 5,7–83.
  - FLASH-HEALTHY (fb1cf0e9): 29 cờ ở Booking, gồm `workload`, latency p50/p90, cạnh Gateway→Booking. Tải ×3 là điều kiện H7 nhắm tới.
  - Ca lỗi Booking: REDIS-BOOK 7 cờ, NET-GW-BOOK 5 cờ, CPU-BOOK-1 51 cờ, CPU-BOOK-2 62 cờ; `s` lớn nhất 535–1.352, có metric hoặc cạnh.
- **Suy luận (chưa kiểm).** Cờ nền ở BINH-THUONG có thể là dịch phân vị nhỏ của thao tác DB dưới tải mua vé. Đây là đối tượng của H8 (sàn 1 ms) và H6a. Cần đọc `don_vi_phan_vi` từng cờ (h, l, r_N/r_A) để biết độ dịch tuyệt đối.
- **Hệ quả cho chấm.** Ca lỗi Booking đúng hạng không chỉ nhờ "Booking luôn bị cờ": độ mạnh và độ rộng tín hiệu tách rõ hai nhóm. Nhưng chưa có phép phân xử định lượng (vd. biên của khóa xếp hạng).

## Q2. Bản gộp làm mất cờ cạnh đúng ở EVENT-DB-LAT — 13/11 ~15:00Z

- **Quan sát.** `V027-GOP-H8s1/4af494a5/method-output-1.json#/extra/m1_ft/canh_xep_hang`:
  - cạnh event-service → event_db (data): `co_truoc_dinh_vi = 1`, `diem = 0,952`, sau định vị `dinh_vi = phia_goi`, `co = 0`, hạng 20 (nhóm cuối).
  - `chu_thich/H1c-canh-chung/bang_chung_rieng/event-service` = `jvm-cpu`, `pool-used`, `pool-wait`. Đây là kênh do H2/H3 thêm.
  - Sơ bộ trên tập B: cạnh đúng top 3 ở 0/3 ô cạnh với V026 và V027.
- **Suy luận.** Bước định vị (H1b, dùng trong H1c) coi kênh tài nguyên của bên gọi là bằng chứng lỗi riêng của bên gọi, nên bỏ cờ cạnh. Với DB chậm, pool-used/pool-wait tăng là **hệ quả** (connection bị giữ lâu hơn), không phải nguyên nhân tại event-service.
  - Điều kiện: H2/H3 bật cùng H1c.
  - Bước: định vị `phia_goi`.
  - Thông tin bị đánh giá sai: kênh pool/JVM của bên gọi.
- **Trạng thái.** Chưa đối chiếu V014 (H1c riêng, không H2/H3) và V021/V022 (gộp bỏ H2/H3). Hai bản này sẽ phân xử khi lô xong.

### Q2 — bổ sung 13/11 ~16:10Z (sơ bộ, tập B, 10/27 bản)

- V022 (gộp bỏ H3): cạnh đúng ở REDIS-BOOK và NET-GW-BOOK lên hạng 2, nên bảng cạnh từ 0 lên 2/3. EVENT-DB-LAT vẫn hạng 29,5.
- Ủng hộ suy luận Q2 cho Booking: kênh pool (H3) của bên gọi kéo định vị về `phia_goi`. EVENT-DB-LAT còn H2 (`jvm-cpu`) là ứng viên; chờ V021 (gộp bỏ H2) và V014 (H1c riêng).
- Mọi bản gộp có K = 5/5 (P7 = 4/5). Chưa biết kênh nào gây cờ ở ca nền; chờ V012 (H2), V013 (H3), V017 (H4), V018 (H5).
- Sơ bộ một thành phần: V002 (H8s1) K 4 → 3, nút giữ; V003 (H6a) không đổi; V004 (H6a + H8s1) như V002.
- 16:20Z, V021 (gộp bỏ H2): cạnh EVENT-DB-LAT vẫn mất. `bang_chung_rieng/event-service` = `pool-used`, `pool-wait`, chỉ từ H3. Kết hợp với V022: một kênh tài nguyên của bên gọi, đứng một mình (H2 hoặc H3), đã đủ làm định vị ra `phia_goi`. V021 có K = 3/5, các bản gộp khác 5/5, nên H2 góp 2 ca nền bị cờ (chưa xem từng ca).

## Q3. PAUSE-PAYMENT: đáp án vắng ở P7, hạng 4 với H5 — 13/11 ~18:45Z

- **Quan sát.** P7 `46aab4be/method-output-1.json`:
  - `diagnostics/NO_VALID_CHANNEL = ["payment-service"]`; 16/17 thực thể quan sát được xếp hạng, Payment bị loại.
  - V018-H5: Payment trở lại danh sách, cờ `live-down` và `live-ms`, khóa `[2, 1.0, 0.693, 1, 1.0]`, hạng 4 (nhóm 3).
  - Ba thực thể đứng trên Payment: Booking, Gateway, User có `s` hàng trăm.
  - V015 (không có H5) giống P7.
- **Cơ chế.**
  - Điều kiện: thành phần bị pause cả pha lỗi.
  - P7: mọi kênh của Payment mất mẫu ở A, nên bước loại thực thể không có kênh hợp lệ bỏ Payment, mất thông tin "thành phần chết".
  - H5: khôi phục thông tin này bằng nguồn sống/chết độc lập. Nhưng độ lớn của kênh nhị phân (e ≤ 1) không so được với độ trễ của bên phụ thuộc, nên Payment xếp sau các thành phần chịu hậu quả.
- **Ứng viên sửa (chưa kiểm):** khi `live-down` = 1 suốt A, coi là bằng chứng tuyệt đối, xếp trên như `STOPPED`/`NEW_OP` của E4. Thiết kế này chọn sau khi đã xem ca này, nên phải khai là thiết kế trên dữ liệu đã xem; chỉ có 1 ô PAUSE trong tập chọn.

## Q4. Ca không lỗi còn bị cờ dưới V015 — 13/11 ~18:45Z

- **FLASH-HEALTHY (fb1cf0e9), 53 cờ.** Tỉ lệ đuôi độ trễ (`r_len`) của nhiều thao tác tăng dưới tải ×3:
  - Event: `SELECT tbl_event_sectors` 0,049 → 0,118; `Transaction.commit` 0,040 → 0,090.
  - Ticket: `SELECT ticket_db` 0,040 → 0,093.
  - Keycloak: job `DELETE OUTBOX_ENTRY` 0,047 → 0,157.
  - H7c bỏ workload của 5 service, chia log theo ρ ≈ 2,2–2,7, nhưng không chạm độ trễ thao tác.
  - Suy luận: độ trễ tăng vì tải là thay đổi thật của hệ thống, không phải nhiễu đo. Chưa phân xử được câu hỏi "ca FLASH khỏe có nên trả NO_INTRINSIC_ANOMALY khi độ trễ thật tăng không". Đây là câu hỏi định nghĩa cho Minh và hướng dẫn của cô (DT18: suy giảm do tải ngoài).
- **BINH-THUONG eb48d6b3:** 1 cờ, `op|event-service|event_db`, `r_len` 0,044 → 0,062, n ≈ 2.700, h ≈ 1,33 ms.
- **BINH-THUONG f20b0ca5:** 2 cờ: `UPDATE tbl_purchase_limits` 0,037 → 0,100 (n ≈ 214); `SELECT tbl_order_payment_snapshots` 0,045 → 0,073.
  - Suy luận (chưa kiểm): dịch nhỏ của thao tác DB dưới tải mua vé. Ứng viên: autovacuum (đã có log autovacuum, TD-06), checkpoint Postgres, khóa hàng `tbl_purchase_limits` khi cùng user mua liên tiếp.
  - Phân xử bằng: đối chiếu mốc cờ với log autovacuum/checkpoint của Postgres trong gói ca, và với số hành trình cùng user trong cửa sổ.

### Q4 — bổ sung 13/11 ~19:35Z: đối chiếu log Postgres (phiên 2)

- **Phép kiểm.** Đếm trong `cases/<mã>/raw-logs.jsonl` (gói `results/T-063/thu2/ca/<mã>.tgz`) các dòng `automatic vacuum/analyze of table` và `checkpoint complete` của `postgresql-shared-instance`, tách cửa sổ N [t−300, t) và A [t, t+300). So hai ca bị cờ (eb48d6b3, f20b0ca5) với hai ca BINH-THUONG không bị cờ dưới V015 (729604d2, 83073ed1).
- **Quan sát.**
  - Autovacuum/analyze có ở cả N và A của cả bốn ca, số lượng cùng cỡ: mỗi cửa sổ 5–9 lần analyze và 1–4 lần vacuum trên `booking_db`, 5–8 lần analyze trên `ticket_db`. `tbl_purchase_limits` được analyze 2–3 lần ở mỗi cửa sổ của cả bốn ca.
  - Checkpoint chạy gần như liên tục ở cả bốn ca: mỗi cửa sổ một lần `checkpoint complete`, `total` 232–270 s trên chu kỳ 300 s.
  - `event_db` không có dòng autovacuum nào trong hai cửa sổ của eb48d6b3, ca có cờ `op|event-service|event_db`.
  - Không có dòng `still waiting` hay `deadlock` trong bốn ca.
- **Suy luận.** Autovacuum và checkpoint không phân biệt ca bị cờ với ca không bị cờ, nên hai ứng viên này **không được ủng hộ**. Khóa hàng **chưa phân xử được**: không có dòng chờ khóa, nhưng chưa kiểm `log_lock_waits` có bật không; nếu tắt thì vắng dòng không nói gì.
- **Giải thích còn lại (chưa kiểm).** Dao động ngẫu nhiên của tỉ lệ đuôi khi chấm khoảng 300 đơn vị span mỗi ca. Phân xử cần chạy lặp ca BINH-THUONG (chiến dịch để sau) hoặc phép dời mốc t trên cùng gói (tiêu chí §7).
- **Trạng thái.** Hai cờ nền còn lại của V015 ở ca BINH-THUONG: nguyên nhân chưa xác định.

## Q5. HTTP5-EVENT-FLASH (98ea5ba4): Keycloak đứng trên Event — 13/11 ~19:36Z

- **Quan sát.** `V015-H1c+H7c+H8s1/98ea5ba4/method-output-1.json` (P7 cho cùng thứ tự nút):
  - Keycloak hạng 1 nhờ đúng một đơn vị: `op|keycloak|SELECT keycloak_db.OFFLINE_USER_SESSION`, s = 962; n_N = 711, n_A = 1.370; tỉ lệ đuôi 0,048 → 0,168; p = 0,003.
  - Event (gốc) hạng 2: `op|event-service|GET /api/v1/events/{id}` s = 124,8. Kênh `error` và `log_loi` của Event có cờ thô nhưng F_I = 0; ở ô HTTP5-EVENT không tải tăng (e9c9679b) hai kênh này có F_I = 1.
  - Cùng đơn vị Keycloak ở ca BINH-THUONG 83073ed1: n_N = 709, n_A = 1.346; tỉ lệ đuôi 0,045 → 0,139; p = 0,37, không có cờ. Ở FLASH-HEALTHY fb1cf0e9 chiều ngược lại: n_N = 1.360, n_A = 725.
  - ρ của Keycloak theo H7 là 1,43–1,55 ở cả ba ca, kể cả ca không tải tăng.
  - Hạng kỳ vọng 2,5 (không phải 2) ở V015: cạnh `keycloak → keycloak_db` (e = 0,039, `rieng_canh`) đứng hạng 2 trong danh sách chung, phép chiếu của tiêu chí cho `keycloak_db` cùng hạng 2 với Event.
- **Suy luận.**
  - Số lần chạy và độ trễ của thao tác Keycloak này đổi giữa hai nửa cửa sổ **cả ở ca không lỗi**, nên cờ ở 98ea5ba4 không đặc hiệu cho lỗi đã tiêm. Đây là thao tác có nhịp riêng (đối tượng của H6); H6a không lọc được nó.
  - Khóa xếp hạng của P7 so `max s` trước, nên một đơn vị đơn lẻ s = 962 thắng gốc thật có s = 124,8.
- **Chưa biết.** Vì sao cùng mức dịch mà cổng cho p = 0,003 ở ca này và 0,37 ở ca nền; nhịp nào làm số lần chạy gấp đôi giữa hai nửa cửa sổ (job Keycloak, hay lịch đăng nhập của k6/đầu dò).
- **Bằng chứng cần.** (i) loại span gốc và tên luồng của thao tác này trong `raw-traces.jsonl`; (ii) số lần chạy theo từng phút trên cả chu kỳ 30 phút của vài ca; (iii) đọc cách tính p của cổng G3 cho hai ca.

## Q6. CPU-BOOK-2 (60166807): H8s1 đẩy Booking từ hạng 1 xuống 2 — 13/11 ~19:36Z

- **Quan sát.**
  - P7: Booking hạng 1, khóa `max s` = 1.325,5, 60 kênh có cờ, Σs = 12.913. Event hạng 2: `max s` = 782,2, 11 kênh, Σs = 3.286.
  - Hai đơn vị mạnh nhất của Booking là thao tác trong tiến trình, rất ngắn: `Session.persist …Reservation` (ngưỡng h = 45 µs, độ vượt trung bình 411 µs), `TicketTypeInventoryRepository.saveAll` (h = 43 µs, độ vượt 506 µs).
  - H8s1 (sàn 1 ms) bỏ 24 hướng có cờ, trong đó 15 của Booking, gồm hai đơn vị trên. `max s` của Booking còn 758,7 < 782,2 của Event. Booking vẫn có 45 kênh, Σs = 7.516, và `metric|booking-service_cpu`.
  - CPU-BOOK-1 (19b17e22): H8s1 bỏ 34 hướng nhưng đơn vị mạnh nhất của Booking (1.352) vượt sàn, hạng giữ.
  - Tỉ lệ độ vượt trung bình / ngưỡng h của các hướng bị H8s1 bỏ (`V002-H8s1/<mã>` × `don_vi_phan_vi`): bốn ca BINH-THUONG đều ≤ 0,8; CPU-BOOK-1 tới 4,9; CPU-BOOK-2 tới 11,7; FLASH-HEALTHY tới 11,4; EVENT-DB-LAT có một đơn vị Payment 7,9.
- **Cơ chế.** Điều kiện: tranh CPU làm thao tác vài chục µs chậm thêm 0,3–0,8 ms. Bước: sàn tuyệt đối 1 ms của H8s1. Thông tin mất: bằng chứng mạnh nhất của chính thành phần gốc. Khóa `max s` rồi đảo thứ tự với chênh 3%. Đây đúng là điều kiện thất bại đã ghi trước của H8-san (lỗi thật có độ vượt < δ).
- **Ứng viên sửa (chưa kiểm, chưa chạy).**
  - Sàn tương đối (chỉ bỏ cờ khi độ vượt < 1 ms **và** < h). Dự đoán từ số trên: giữ được Booking ở CPU-BOOK-2 và vẫn bỏ cờ nền ở BINH-THUONG, nhưng trả lại đơn vị Payment 7,9 ở EVENT-DB-LAT — đúng đơn vị mà việc bỏ nó đưa Event lên hạng 1. Vậy đây là đổi ca này lấy ca kia, không phải cải thiện rõ.
  - Khóa xếp hạng ít phụ thuộc một đơn vị đơn lẻ (ví dụ xét độ rộng trước). Đây là đổi lõi xếp hạng E6 của P7, chỉ có 7 ca lỗi để chọn; nguy cơ khớp quá cao.
- **Trạng thái.** Hai ca sai CPU-BOOK-2 (H8s1) và EVENT-DB-LAT (P7) cùng một gốc: một đơn vị thao tác rất ngắn quyết định `max s`. Chưa có thay đổi nào tách được hai ca mà có nguyên lý độc lập với đáp án.

### Q4 — đính chính 13/11 19:58Z (theo REVIEW-2 R6 của T-063)

- Câu "chưa kiểm `log_lock_waits` có bật không" ở trên thiếu: `results/T-063/quan-sat/thay-doi-may.md` TD-06 ghi đã bật `log_lock_waits=on` từ 12/11 23:29Z (chưa đọc lại cấu hình đang chạy). Dù bật, Postgres chỉ ghi lần chờ dài hơn `deadlock_timeout` (mặc định 1 s, chưa đọc giá trị thực). Vắng dòng chờ khóa vì thế chỉ loại chờ khóa dài, không loại chờ cỡ ms.
- Mức kết luận đúng cho autovacuum và checkpoint: phép đếm theo cửa sổ **chưa phân biệt được** ca bị cờ với ca không bị cờ. Chưa đối chiếu mốc vượt ngưỡng theo thời gian với thời lượng hay I/O của từng lần chạy, nên chưa loại được ảnh hưởng phụ thuộc thời điểm. Instance dùng chung, nên vắng autovacuum trên `event_db` chưa loại ảnh hưởng gián tiếp.

## Q7. BINH-THUONG-X3 (1e5a3dc5): V082 báo nhầm do một cờ CPU Payment — 15/11/2026 (REVIEW-4 R10; Minh duyệt "Duyệt cả ba")

- **Quan sát** (chỉ file đã có; `kiem/nhan-luot5/l5/dev3/d0/<bản>/<ca>/method-output-1.json`):
  - V082 ở 1e5a3dc5: `CAUSE_FOUND`, payment-service hạng 1. `#/extra/kenh_co` có đúng một cờ tự sinh (`F_I = 1`): `metric|payment-service_cpu`, s ≈ 2,765. Cờ `ticket-service_live-ms` có `F_I = 0` (không tự sinh, không tính).
  - `#/extra/don_vi_phan_vi` (ma `metric|payment-service_cpu`): n_N = n_A = 20; tỉ lệ đuôi lên N → A = 0 → 0,05 (một điểm trong 20 vượt ngưỡng h ≈ 0,0816); p_len ≈ 0,0040.
  - Đối chứng cùng bản 3, tải ×1 (7d1ee32f, tập độ nhạy): cũng `CAUSE_FOUND`, payment hạng 1, cờ tự sinh duy nhất `metric|payment-service_cpu` (s ≈ 3,608; đuôi lên 0 → 0,85, h ≈ 0,0426). P7, V032, V061 ở 7d1ee32f có thêm cờ `op|booking-service|Session.persist …Reservation` (bị H8s1 bỏ ở V082).
  - Cờ CPU Payment có ở 1e5a3dc5 dưới mọi bản đã chạy (P7, V032, V061, V071, V082); không do thành phần M1-FT nào sinh ra.
  - Tải: `results/T-063/thu3/xac-nhan-ca-3-sua-sau.json#/ca/1e5a3dc5/k6` multiplier 3, 6.481 journey, 0 lỗi, 0 drop; `#/ca/7d1ee32f/k6` multiplier 1, 2.161 journey, 0 lỗi. Tải ×3 kéo dài suốt chu kỳ (BAN-GIAO-B), khác FLASH-HEALTHY tăng tải tại t.
- **Đã lần được:** kênh CPU Payment → điểm đuôi trong A vượt ngưỡng (1 điểm ở 1e5a3dc5, 17 điểm ở 7d1ee32f) → p_len < ngưỡng → cờ tự sinh `F_I = 1` → payment có bằng chứng riêng → verdict `CAUSE_FOUND`. Không qua H5b (không có chết im), không qua sàn 1 ms (kênh metric).
- **Chưa phân xử — nguyên nhân CPU Payment đổi trong A.** Không gán cho tải ×3: ca ×1 cùng bản 3 cũng có cờ, mạnh hơn. Khả năng còn lại: (a) việc nền định kỳ của Payment rơi vào cửa sổ A (lịch job/outbox); (b) dao động CPU bình thường vượt ngưỡng chặt khi N rất ổn (đuôi N = 0); (c) hiệu ứng riêng của bản triển khai 3 (cùng đợt build/khởi động lại Event 14/11). Phân xử cần: chuỗi CPU gốc của Payment quanh t ở hai ca và ở các ô lỗi bản 3 trước t; mốc log job/outbox của Payment trong cửa sổ; đối chiếu latency N/A của Payment. Dữ liệu có trong gói ca trên exp-obs (`/opt/flash-ticket-rca/cases/<mã>`); chưa đọc trong lượt này (chỉ dùng file đã có theo phạm vi duyệt). Kết luận phụ thuộc: diễn giải K của V082 (1 trong 4 ca báo nhầm); không đổi K hay thứ tự chọn.
