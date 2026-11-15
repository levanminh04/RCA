# Kiểm độ nhạy mốc ±30 s — phân tích (phiên C, T-064 SPEC bước 6, §7)

Ghi 14/11/2026 ~06:45Z. Vai trò: **kiểm độ nhạy, không dùng để chọn** (sổ V052–V059, `vai_tro: do_nhay_moc`). Kết quả dùng trong hồ sơ chọn phải chờ WHY-(a) (`../de-xuat-WHY.md`).

## 1. Đã chạy gì

- **Bản:** P7, V032-H5b (đề xuất tạm), V041 (thay thế có cạnh); mỗi bản với d ∈ {−30, +30} (V052–V057).
- **Ca:** 13 ca dev bản 2 và 9 ca T-062.
- **Hai bản phụ khai trước:** V058 (P7, dựng lại đầu vào với d = 0, để kiểm cài đặt) và V059 (P7, d = −300, phép thử giả).
- **Máy:** `exp-obs`, mã nguồn `goc-10` (`05273b2e…`), 05:20:47–06:34Z.
- **Kiểm lô** (`../cham/kiem-lo-doi-moc.json`):
  - đủ 176/176 cặp; mọi cặp `status OK`, hai lần chạy trùng SHA;
  - V058: `method-input.json` dựng lại trùng byte bản đã lưu ở 22/22 ca, và đầu ra trùng byte P7 ở 22/22 ca. Vậy đường dựng lại tái lập đúng P7; mọi khác biệt ở d ≠ 0 là do mốc.
  - Gói metric bổ sung quanh t': 0 lệch ở 252.125 điểm chung (`kiem-bo-sung-doi-t.json`).
- **Chấm:** `../cham_phien_c.py`, cùng đáp án khai trước và bộ chấm của T-064. Kết quả ở `../cham/doi-moc.json`; bảng theo ô ở `bang-o.md`; chi tiết kênh của mọi ca đổi ở `co-che-tu-dong.md`.

## 2. Quan sát (số từ `../cham/doi-moc.json`)

Tập 13 ca, cột là AC@1 / AC@3 / tổng hạng cắt / K:

| Bản | d = 0 | d = −30 | d = +30 |
|---|---|---|---|
| P7 | 5 / 7 / 15 / 4 | 5 / 8 / 12 / 5 | 5 / 7 / 16 / 5 |
| V032 | 6 / 8 / 10 / 4 | 6 / 8 / 10 / 5 | 5 / 8 / 13 / 5 |
| V041 | 6 / 8 / 11 / 3 (cạnh 3/3) | 6 / 7 / 12,5 / 3 (cạnh 3/3) | 4 / 7 / 16 / 3 (cạnh 2/3) |

9 ca T-062, AC@1 / tổng hạng cắt / K: P7 5 / 5 / 4 → (−30) 5 / 5 / 4, (+30) 3 / 8 / 4. V032 giống P7. V041 5 / 5 / 1 → (−30) 5 / 5 / 2, (+30) 4 / 6 / 1.

Phép thử giả d = −300 (phía A = [t−300, t), trước mốc): AC@1 của P7 rơi từ 5 xuống 1 (dev bản 2) và từ 5 xuống 1,06 (T-062). Vậy phép kiểm có sức phân biệt. Hai ca còn "đúng" là trùng hợp do tín hiệu nền trước t, không phải tín hiệu lỗi: 5fb8208f có EVALSHA của api-gateway với khởi phát −300 s, mà api-gateway thuộc tập chấp nhận của cạnh NET-GW-BOOK.

Theo ô (bảng ở `bang-o.md`):
- **Không đổi ở cả 6 phép dời:** CPU-BOOK-1, NET-GW-BOOK (dev), FLASH-HEALTHY (K = 1), SLOW-BOOK, CPU-BOOK (T-062); EVENT-DB-LAT (T-062) đổi chỉ ở hạng cạnh của V041 +30 (2 → 3).
- **Đổi ở mọi bản:**
  - HTTP5-EVENT e9c9679b: 1 → 2 ở cả ±30.
  - HTTP5-EVENT-FLASH 98ea5ba4: 2 → 1 ở −30, 2 → 3 ở +30.
  - BINH-THUONG 83073ed1: `NO_INTRINSIC_ANOMALY` → `CAUSE_FOUND` ở ±30 (P7, V032) và ở −30 (V041).
- **Chỉ ở +30:**
  - EVENT-DB-LAT 4af494a5: 2 → 1 với P7, V032.
  - PAUSE-PAYMENT 46aab4be: 1 → 3 với V032, V041 (P7 vẫn không có đáp án trong thứ hạng).
  - T-062: HTTP5-EVENT a89954d1 1 → 2, NET-GW-BOOK f728fce2 1 → 3 (P7, V032).
  - V041: REDIS-BOOK 1 → 2,5 (cạnh 2 → 30,5); CPU-BOOK-2 2,5 → 1.

## 3. Cơ chế đã xác nhận trên trung gian (luật 15)

**C1 — ngưỡng N bị lẫn lỗi khi dời +30.** Điều kiện: lỗi khởi phát trong [t, t+30). Bước E4 (`h` = phân vị 0,95 của N × 1,05) tính trên N = [t−270, t+30), nên N chứa 30 s mẫu lỗi (10% thời gian N, vượt 1 − q_hi = 5% khi tần suất đều). Ngưỡng nhảy vào phân bố lỗi; tỷ lệ vượt ở A giảm; e giảm hoặc mất cờ.
- Đầu vào → trung gian → đầu ra, ca f728fce2 (NET-GW-BOOK, P7): đơn vị `canh|api-gateway|booking-service` có `h` = 1.951,95 µs và `r_len_A` = 1,0 ở d = 0 (e = 1.027,9, có cờ). Ở d = +30: `h` = 316.531,7 µs, `r_len_A` = 0, `F_raw_len` = 0. Mất cờ cạnh E2 làm booking từ hạng 1 xuống 3.
- Cùng chiều ở các ca khác: điểm của đơn vị lỗi giảm khoảng một nửa (a89954d1 `GET /api/v1/events/{id}` 664 → 342; e9c9679b 85,2 → 50,1; 4af494a5 `Transaction.commit` 651 → 339). Đơn vị nền khởi phát sau t+30 giữ nguyên điểm và vượt lên, ví dụ keycloak `OFFLINE_USER_SESSION` khởi phát +120 s ở a89954d1.
- Ca đối chiếu cùng điều kiện, theo chiều ngược: 4af494a5 "tốt lên" ở +30 cũng vì C1. Đối thủ của đáp án (payment `InboxMessageRepository.findById`, e = 996, khởi phát +10 s) mất cờ, còn các đơn vị của event-service chỉ giảm điểm. Đây không phải bằng chứng bản bền với mốc.

**C2 — H5b mất điều kiện (i) khi dời +30.** PAUSE-PAYMENT: liveness payment hụt từ mẫu `tu` = t+15 s (`chu_thich.H5-liveness.chet_im` của V032 d = 0). Ở t' = t+30, mẫu t+15 thuộc N, nên điều kiện "phản hồi ở mọi mẫu trước t" sai, `chet_im` rỗng (V056), và thứ hạng về như P7 (booking hạng 1). Ở d = −30 điều kiện vẫn thỏa (`tu` = t+15 > t−30). Đây là tính chất thiết kế của H5b (WHY-86): bản chỉ nhận thành phần "chết" **sau** mốc.

**C3 — thang IQR của `nhanh_z` trên chuỗi phẳng, dời −30.** P7 bật `nhanh_z`: e = max|A − med_N| / IQR_N. Ca e9c9679b, kênh `workload` của api-gateway có N gần phẳng (5,24–5,30 req/s, 20 điểm). IQR_N bằng 0,04 ở d = 0 và 0,025 ở d = −30; min A bằng 2,50 trong cả hai trường hợp. Do đó z_xuống tăng từ 69,25 lên 110,6, đúng giá trị trong đầu ra (`don_vi_phan_vi`), và vượt điểm của event-service (82,4). Hạng 1 chuyển sang api-gateway. Tính lại bằng `numpy` trên `prometheus.json` của ca cho đúng hai số này.

## 4. Ứng viên chưa kiểm (luật cứng 5)

- **REDIS-BOOK của V041 ở +30 (cạnh 2 → 30,5): đã kiểm một phần** (`extra.m1_ft.canh_xep_hang`, cạnh booking-service → cache).
  - Ở d = 0: `diem` (e = r_A − r_N) = 0,954, `dinh_vi` = `rieng_canh`, có cờ.
  - Ở d = +30: vẫn có cờ trước bước định vị (`co_truoc_dinh_vi` = 1), nhưng `diem` = 0,0027. Hợp với C1: N lẫn lỗi, r_N tăng gần bằng r_A. Bước định vị chuyển sang `phia_dich` → mất cờ.
  - **Chưa kiểm:** lý do định vị đổi sang phía đích (cờ của cache hay cờ phía gọi thay đổi). Phép kiểm cần làm: đọc `dinh_vi` và cờ op SERVER/metric của hai đầu cạnh.
- **CPU-BOOK-2 của V041 (2,5 → 4 ở −30; 2,5 → 1 ở +30):** **chưa kiểm**.
- **83073ed1 đổi K ở ±30:** đơn vị span đơn lẻ có khởi phát đúng ở biên cửa sổ (ticket `SELECT ticket_db`, kp = −30 s khi d = −30; booking `Session.persist Order`, kp = +80 s khi d = +30). Ứng viên: kết luận `NO_INTRINSIC_ANOMALY` ở d = 0 nằm sát ngưỡng, đổi vài mẫu N/A là lật. **Chưa kiểm** p và ngưỡng của từng đơn vị.
- **98ea5ba4 tốt lên ở −30** (keycloak `OFFLINE_USER_SESSION`, khởi phát +0 s, mất vị trí đầu): **chưa kiểm** là C1 ngược chiều hay C3.

## 5. Suy luận và giới hạn

- **Kết quả xếp hạng nhạy với mốc ở mức 30 s,** nhất là khi dời muộn hơn mốc (+30). Trên tập 13 ca: AC@1 của V041 6 → 4; tổng hạng của P7 15 → 16, của V032 10 → 13. Trên 9 ca T-062: AC@1 của P7 và V032 5 → 3. Cơ chế chính (C1) là tính chất của phép chọn N/A theo mốc trong E4, không riêng thành phần nào của M1-FT.
- **Thứ tự giữa các bản trên tập 13 ca:**
  - V032 không kém P7 ở cả ba mốc: AC@1 6/6/5 so với 5/5/5; tổng hạng 10/10/13 so với 15/12/16.
  - V041 kém P7 về AC@1 ở +30 (4 so với 5).
  - Lợi thế riêng của V032 so với P7 ở PAUSE-PAYMENT mất ở +30 (C2).
  - K tăng 1 ở cả ba bản tại một ca không lỗi (83073ed1), nên kết luận về K = 4 hay 5 nhạy với mốc.
- **Hệ quả cho FlashTicket (luật 17):** mốc t trong chế độ (a) phải đặt **trước hoặc đúng** lúc lỗi khởi phát. Mốc muộn 30 s làm N lẫn lỗi. Một dịch vụ RCA trực tuyến (G3 giai đoạn 2) lấy t từ luật cảnh báo, vốn thường kích **sau** khởi phát, sẽ gặp đúng điều kiện +30. Đây là yêu cầu ghi lại cho thiết kế cảnh báo và mốc, **chưa kiểm** trên luật cảnh báo thật.
- **Không rút ra được:**
  - dao động giữa các lần thu (mỗi ô một lần thu);
  - độ nhạy với |d| khác 30;
  - phép dời có làm đổi lựa chọn V032 so với P7 theo §5 hay không, khi chưa áp đủ luật §5 lên các bản dời. Phép dời không phải biến thể để chọn; hồ sơ chọn quyết, sau WHY.

## 6. Câu hỏi mở

1. Có nên thêm phép kiểm d ∈ {−60, −15, +15} để biết ngưỡng lật ở các ô HTTP5-EVENT không? Ước khoảng 1 giờ máy cho 3 bản × 22 ca × 3 mốc.
2. Có nên thiết kế một biến thể bền với mốc muộn (ví dụ tách N = [t−300, t−δ)) không? Đây là thay đổi phương pháp, cần ghi sổ và WHY trước.
3. 83073ed1: cần đọc p, ngưỡng của từng đơn vị lật (mục 4).
