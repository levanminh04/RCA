# T-072 — p95 payment/ticket từ E2 sang E4: trôi hay dao động đuôi? Rủi ro báo động giả cho E5 và demo

23/11/2026. Điều phối giao 01:42Z. Chỉ dùng dữ liệu đã xuất, không truy vấn Prometheus, không SSH (S4 đang mở cho T-073). Không đổi ngưỡng hay quy tắc đã khóa.

- Script: `troi_p95.py` → `troi-p95-e2-e4.json`; `troi_p95_rui_ro.py` → `troi-p95-rui-ro.json`. sha256: `SHA256SUMS-troi-p95`.
- Hash đầu vào trước khi dùng: `results/T-071/e2` 13/13, `e3` 7/7, `e4` 14/14 khớp `SHA256SUMS`. Bản giải nén `ra` của E2 377/377 và E4 424/424 khớp `ra-SHA256SUMS`. Bản chuyển `e2/xuat`, `e4/xuat`, `e2/phut.json`, `e4/phut.json` khớp `SHA256SUMS-e2-nguong` và `SHA256SUMS-e4`. Bốn mục lệch trong `SHA256SUMS-e2-nguong` là file đề xuất commit đã sửa hợp lệ ở lượt 8, không phải dữ liệu.
- Nguồn chính: counter bucket thô của histogram gateway (`tho/gw-bucket`, mỗi 10 s, mọi chuỗi nhãn) cho từng lượt, và chuỗi `tin-hieu/t072-p95-*` (bước 10 s).

## 1. Phân bố thời gian request theo lượt (toàn bộ request trong [StartedAt, FinishedAt])

Bảng chỉ lấy lượt ×1. Lượt flash có tỷ lệ chậm cao hơn ở cả E2 lẫn E4 vì tải ×3.

| | E2 (5 lượt ×1, 20/11 15:03–22:14Z) | E4 (7 lượt ×1, 22/11 10:13–17:56Z) |
|---|---|---|
| payment, request / 5 phút | 71,9–72,0 | 71,9–72,0 |
| payment p50 (s) | 0,0317–0,0340 | 0,0307–0,0332 |
| payment p95 cả lượt (s) | 0,062–0,075 | 0,056–0,074 |
| payment tỷ lệ > 0,1 s | 1,04–2,55% (tb 1,70%) | 1,04–1,97% (tb 1,67%) |
| payment tỷ lệ > 0,25 s | 0–0,35% | 0–0,35% |
| ticket, request / 5 phút | 71,7–71,9 | 71,7–71,9 |
| ticket p50 (s) | 0,0091–0,0097 | 0,0090–0,0094 |
| ticket p95 cả lượt (s) | 0,024–0,034 | 0,025–0,034 |
| ticket tỷ lệ > 0,1 s | 0,23–0,93% (tb 0,64%) | 0,12–1,28% (tb 0,58%) |

Thứ tự lượt E4, theo tỷ lệ ticket > 0,1 s: 0,12 → 0,35 → 0,46 → 0,81 → **1,28** → 0,58 → 0,46%. Tăng tới lượt 06 rồi giảm, không đơn điệu. Payment không có xu hướng theo thứ tự lượt ở cả hai khoảng. Booking và event (≈ 690–720 request / 5 phút) cũng ổn định.

**Quan sát:** ở mức cả lượt, payment E4 không chậm hơn E2: trung vị còn hơi thấp hơn, tỷ lệ request chậm như nhau. Ticket có trung bình E4 ≈ E2, nhưng tỷ lệ chậm giữa các lượt E4 dao động rộng hơn.

## 2. Đỉnh p95 duy trì 60 s trong phút khỏe ×1 đến từ đâu

| | Đỉnh S (s) | S / ngưỡng | Request trong 5 phút tại đỉnh | Request > 0,1 s trong 5 phút đó |
|---|---|---|---|---|
| payment E2 | 0,1225 (21:45Z, lượt 08) | 0,67 | 72 | 4 |
| payment E4 | 0,1544 (10:56Z, lượt 01) | 0,84 | 73 | 5 |
| ticket E2 | 0,0612 (16:24Z, lượt 02) | 0,55 | 72 | 3 |
| ticket E4 | 0,0938 (14:58Z, lượt 06) | 0,84 | 72 | 3 |

Với khoảng 72 request trong cửa sổ, p95 là request chậm thứ 4 tính từ trên xuống. Vì vậy chỉ 3–5 request chậm cũng đủ đẩy p95 lên gần mốc bucket 0,1 s.

- **Tần suất vượt:** S > 0,7 × ngưỡng xảy ra ở E4 tại 6 bước (1 đợt) với payment và 16 bước (2 đợt) với ticket; ở E2 là 0. S > 0,84 × ngưỡng: 0 bước ở cả hai khoảng.
- **Thời điểm vượt 0,7 × ngưỡng của ticket ở E4:** 11/16 bước nằm trong 10 phút đầu lượt. Lúc đầu lượt cửa sổ còn ít request nên p95 dao động mạnh hơn. E3 cho thấy cùng cơ chế: booking lên 0,0931 s (95% ngưỡng) ở điểm đầu lượt, nhưng không giữ đủ 60 s.
- **Độ phân tán của số request > 0,1 s trong cửa sổ 5 phút rời nhau** (phương sai / trung bình): payment 0,79 (E2) và 0,84 (E4); ticket 1,12 (E2) và 1,29 (E4). Payment không dồn cụm. Ticket dồn cụm nhẹ ở E4.

## 3. Phân xử hai giải thích

| Giải thích | Dự đoán nếu đúng | Dữ liệu | Kết luận |
|---|---|---|---|
| Trôi do DB tích lũy | Cả phân bố dịch lên: p50, tỷ lệ > 0,1 s và > 0,25 s tăng; tăng theo thứ tự lượt và từ E2 sang E4 | Payment: không tăng ở mức nào. Ticket: trung bình không tăng, không đơn điệu theo lượt | **Không được dữ liệu hỗ trợ** ở mức cả lượt. Không loại trừ được trôi nhỏ hơn độ phân giải (bucket 0,025–0,1 s) hoặc trôi chỉ ở một vài truy vấn DB |
| Dao động đuôi do ít request | Đỉnh S do vài request chậm trong cửa sổ khoảng 72 request; phân bố cả lượt không đổi; đỉnh lớn hơn khi số cửa sổ quan sát nhiều hơn | Đỉnh tương ứng 3–5 request chậm; số request chậm mỗi cửa sổ gần Poisson; E4 có 2.293 bước khỏe so với 2.129 ở E2 | **Phù hợp** (giải thích ứng viên chính) |
| (Khác) Tỷ lệ request chậm của ticket thay đổi theo lượt, nguyên nhân chưa rõ | Một vài lượt có tỷ lệ chậm cao hơn hẳn | Lượt E4-06: 1,28%, so với trung bình 0,6% | Có quan sát; **nguyên nhân chưa biết** (tranh chấp CPU trên exp-app, GC, DB, mạng: chưa phân xử) |

**Phép đo phân xử còn thiếu:**
1. Độ trễ truy vấn DB theo service của ticket và payment, lấy từ span DB trong Tempo hoặc metric `db_client_*`, so giữa E2 và E4 và giữa các lượt E4. Truy vấn nhẹ theo khúc ngoài S4, khoảng 30–60 phút công.
2. CPU, GC, throttle của ticket-service trong lượt E4-06 so với lượt khác. Chuỗi có sẵn trong Prometheus; cần truy vấn ngoài S4.
3. Một khoảng khỏe ×1 dài hơn (≥ 6 giờ) sau E5 để xem tỷ lệ chậm của ticket có tăng theo thời gian không. Tốn vài giờ máy; thuộc quyết định của Minh.

## 4. Rủi ro báo động giả

Đây là ước lượng mô hình, mức **suy luận** (`troi-p95-rui-ro.json`). Giả định: 72 request / 5 phút, request chậm độc lập, mọi request chậm rơi trong bucket 0,1–0,25 s.

| Route | Ngưỡng | Request > 0,1 s tối thiểu trong 5 phút để p95 > ngưỡng | Kỳ vọng số cửa sổ vượt / 6 giờ (72 cửa sổ) theo tỷ lệ chậm: tb E2 / tb E4 / lượt xấu nhất |
|---|---|---|---|
| payment | 0,184 | **9** | 0,0004 / 0,0004 / 0,009 |
| ticket | 0,112 | **4** | 0,09 / 0,07 / **≈ 1,0** |

- **Payment:** rủi ro báo động giả do dao động đuôi ở tải ×1 rất nhỏ. Còn một đường khác: ≥ 4 request > 0,25 s trong một cửa sổ, kỳ vọng khoảng 0,008 / 6 giờ ở tỷ lệ 0,35%.
- **Ticket là điểm yếu:** chỉ 4 request chậm trong 5 phút (≈ 5,5% của 72) là đủ vượt ngưỡng. Ở tỷ lệ chậm trung bình, kỳ vọng < 0,1 / 6 giờ, khớp với 0 sự cố quan sát ở E2 và E4. Nếu tỷ lệ chậm như lượt E4-06 (1,28%) kéo dài, kỳ vọng tăng lên khoảng 1 / 6 giờ, chạm ngưỡng R5. Ticket dồn cụm nhẹ (chỉ số 1,29), nên mô hình Poisson có thể **đánh giá thấp** rủi ro. Mức rủi ro này **chưa kiểm** bằng dữ liệu độc lập.
- **E5, ô `PAUSE-PAYMENT`:** trong lúc lỗi, cảnh báo payment là đúng chứ không phải báo động giả. Lưu lượng ticket tụt về 0, chặn 30 request làm luật ticket im. Rủi ro báo động giả của W4 ở E5 nằm ở các đoạn khỏe quanh ca và ở ticket khi lưu lượng phục hồi: các cửa sổ đầu có ít request, p95 dao động mạnh (cơ chế ở mục 2). Vì vậy một cảnh báo ticket ngay sau khi phục hồi không đủ để coi là sự cố mới. Bộ gom (ghép trong 300 s) giảm việc đếm trùng nhưng không loại được trường hợp này.
- **Demo:** rủi ro lớn nhất ở các phút đầu sau khi bật tải (cửa sổ ít request) và với ticket. Biện pháp vận hành có thể đề xuất mà **không** đổi ngưỡng đã khóa: chạy tải ít nhất 5 phút trước khi bắt đầu phần trình bày phát hiện. Đây là đề xuất, chưa kiểm; Minh hoặc điều phối quyết.

## 5. Kết luận đúng mức bằng chứng

- **Quan sát:** đỉnh p95 duy trì của payment và ticket ở E4 cao hơn E2 (0,84 so với 0,67 và 0,55 của ngưỡng). Phân bố thời gian request cả lượt thì không tăng.
- **Suy luận (ứng viên chính):** đỉnh cao hơn là dao động đuôi do số request nhỏ, cộng với tỷ lệ request chậm của ticket thay đổi giữa các lượt. Trôi do DB tích lũy không được dữ liệu ở độ phân giải này hỗ trợ, nhưng chưa bị loại trừ.
- **Rủi ro:** payment thấp. Ticket chấp nhận được ở tỷ lệ chậm trung bình, nhưng nhạy với các lượt có tỷ lệ chậm cao; ước lượng là mô hình, chưa kiểm.
- **Không làm:** không đổi ngưỡng, không đổi quy tắc. Muốn thay đổi thì phải ghi "sửa sau" và kiểm trên một khoảng mới (`thong-nhat.md` §1.3).
