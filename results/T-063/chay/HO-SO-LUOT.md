# T-063 — Hồ sơ lượt thu chính dev bản 2 (luật 21) — bản chốt 13/11/2026 03:45Z (lịch `lich-2.json` sha256 `9bc6a329…`)

**Lượt:** `runner2.py thu --lich results/T-063/chay/lich-2.json` trên laptop; 13 chu kỳ × 30 phút (nền 10 / lỗi 10 / hồi phục 10) ≈ 6,5 giờ máy; M1 P7 chạy nền tuần tự trên `exp-obs` (~10 s/ca + đóng gói ~2–4 phút/ca). Tiền điều kiện: D2 bản 2 xác nhận từng ô; L1b báo độ bền tunnel/mock và đổi bậc tải; hồ sơ đóng băng ghi đủ; `D:/RCA-overnight/STOP` không tồn tại.

| Lỗi xảy ra ở | Loại lỗi | Phạm vi chặn | Xử lý | Chạy lại gì | Mất thêm |
|---|---|---|---|---|---|
| 10% (chu kỳ 2) | tiêm không lên (lệnh start lỗi) | chỉ ô đó | `fault-start-failed`/`m1-skipped`, chạy tiếp | ô đó, cuối lượt hoặc lượt bù | 30 phút |
| bất kỳ | start chạy nhưng đầu dò không xác nhận | chỉ ca đó | runner **không** tự phân loại (REVIEW R3): ca vẫn `m1-queued`; **hậu kiểm** trên sổ (`inj2 probe` t+60/t+330) theo điều kiện của `D2B-KET-QUA.md`, ghi xác nhận từng mã mờ vào `results/T-063/chay/xac-nhan-ca.json` **trước** khi T-064 khai tập chọn; ca không xác nhận ra khỏi tập chọn (tiêu chí T-064 mục 1) | ô đó ở lượt bù | 30 phút |
| bất kỳ | dọn can thiệp không xác nhận sạch (`verify`/`cleanup`) | cả máy | `bao_dam_sach` ghi `dirty`, thử dọn 1 lần, không được thì `run-abort-dirty` và dừng lượt (REVIEW R1); toxic và pause không tự hết hạn — chỉ `verify` gỡ pause quá hạn | các chu kỳ còn lại sau khi dọn tay | thời gian dọn + 30 phút/ô |
| 10% | tải không khởi động 2 lần / tunnel chết | cả lượt | dừng lượt, giữ ca đã thu; sửa đường tải (L1) | các chu kỳ còn lại | sửa + 30 phút/ô còn lại |
| 50% (chu kỳ 7) | M1/stage lỗi một ca | ca đó | runner stage lại cùng t với mã mới (1 lần), giữ thư mục cũ | không thu lại | ~3 phút |
| 50% | `exp-obs` ngừng nhận (Prometheus/Tempo khởi động lại) | các ca có cửa sổ chồng khoảng mất | ghi khoảng mất; ca bị ảnh hưởng đánh dấu, thu bù | chỉ ô có cửa sổ chồng | 30 phút/ô |
| 99% (chu kỳ 13) | bất kỳ | ô cuối | như trên | ô cuối | 30 phút |
| bất kỳ | phát hiện lỗi phương pháp (M1/adapter) | không chặn thu | dữ liệu thô vẫn giữ; M1 chạy lại sau trên gói đã lưu | không thu lại | ~10 s/ca |
| bất kỳ | sai code tính toán bộ đóng gói | các ca đã đóng gói | đóng gói lại từ Tempo/Loki/Prometheus (retention 30d, Tempo 14d) | không thu lại nếu còn trong retention | phút/ca |

Thêm quy tắc phân loại hoặc quyết định của Minh không buộc thu lại ca đã xong (dữ liệu thô giữ; phương pháp chạy lại trên gói). Điều kiện suy biến đã quét ở D2 (`D2B-KET-QUA.md`): POOL-EVENT không thử được, CONSUMER-BOOK-SLOW không xác nhận được (loại); PAUSE-PAYMENT làm mất mọi tín hiệu Payment (đầu dò httpcheck bắt được); CPU-BOOK-2 nhiễu toàn máy (đã đo); tải D2 hết sớm (đã sửa thời lượng). Kiểm `dropped_iterations` của k6 mỗi chu kỳ (REVIEW-PL2 R4).

## Phụ lục 13/11/2026 ~06:15Z — bộ chạy chuyển lên `exp-obs` (`runner3.py`)

Minh quyết (DECISIONS "Chạy bộ điều phối đợt thu trên `exp-obs`"). Lượt chính chạy bằng `runner3.py thu --lich lich-2.json` trên `exp-obs`, thư mục `~/rca-dieu-phoi`. Bản này sinh từ `runner2.py` bằng `results/T-063/chay/tao_runner3.py` và chỉ đổi phần vận chuyển:
- M1 và đóng gói chạy cục bộ.
- SSH tới `exp-app` bằng khóa trong `~/rca-dieu-phoi/keys`.
- Tải chạy qua `results/T-062/tai-2/tai_linux.py` (L1d, phản biện `tasks/T-062-dem-chang-1-4/REVIEW-PL2-2.md`).
- STOP ở `~/rca-dieu-phoi/STOP`.

Logic chu kỳ, đầu dò, `bao_dam_sach`, thử lại và stage lại khi M1 lỗi giữ nguyên. Hash ở hồ sơ đóng băng bản 2. Bảng lỗi trên vẫn áp dụng, thêm ba dòng:

| Lỗi xảy ra ở | Loại lỗi | Phạm vi chặn | Xử lý | Chạy lại gì | Mất thêm |
|---|---|---|---|---|---|
| bất kỳ | mạng laptop mất | không chặn | bộ chạy không phụ thuộc laptop: chạy trong session riêng (`setsid`), stdin `/dev/null`. Đã kiểm khi ngắt SSH laptop giữa lượt thử | không | 0 |
| bất kỳ | `exp-obs` khởi động lại / tiến trình bộ chạy chết | chu kỳ đang chạy | các lỗi tự hết: toxic/pause qua `_het_han` +5 s, hook có lease, CPU có timeout. k6 chạy hết `--seconds` rồi tự dừng. Chu kỳ dở không có M1, dữ liệu thô giữ. Phát lại `runner3` với lịch các chu kỳ còn lại sau khi máy tải trống (`tai_linux` từ chối nếu còn container `rca-tai-`) | chu kỳ dở + các chu kỳ còn lại | ≤ 30 phút + phần còn lại |
| hậu kiểm | đầu dò audit đếm 2000 dòng đuôi `executions.jsonl`, đã bão hòa (lượt thử: 2000 `http.error.executed` ở cả t−240) | không chặn | xác nhận ô hook (HTTP5-*) bằng file audit **đầy đủ** lọc theo `timestamp` trong [t, t+600], cùng tỉ lệ 5xx của Event. Lượt thử: 2.159 lần trong 05:54–06:04Z, lần cuối 06:04:16Z = lúc dừng. Sau đợt thu, chép `executions.jsonl` của Event/Booking về repo trước khi hậu kiểm | không | phút |

Lượt thử một chu kỳ `HTTP5-EVENT-FLASH` (lịch `results/T-063/chay/thu-ngan/lich-thu-ngan.json`, thư mục `~/rca-dieu-phoi/thu-ngan`, mã mờ `865c8e93`) **không phải ca RCA**, không vào tập chọn. Kết quả ở `results/T-063/chay/thu-ngan/`.
