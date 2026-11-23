# T-072 — Báo động giả trên E4 (luật sống) và so với R5

23/11/2026. Quy tắc đã khóa trước khi xem dữ liệu: gom `T072-gom-3` (`quy-tac-gom.json`), ngưỡng `nguong.json` (`c8f44854…`, `T072-chon-nguong-2` trên E2), R5 ≤ 1 sự cố / 6 giờ khỏe ×1 (Minh 20/11). Máy đọc: `bang-bao-dong-gia.json`; chi tiết `e4/`. Không đổi ngưỡng hay quy tắc sau khi xem E4.

## Kết quả

| Lớp phút (T-071, độc lập tín hiệu luật) | Phút | Sự cố hệ thống | Sự cố quan sát |
|---|---|---|---|
| khỏe ×1 | **383** | **0** | 0 |
| flash (chỉ mô tả) | 38 | 0 | 0 |
| biên | 43 | 0 | 0 |

- **Mẫu số:** 383 phút khỏe ×1 (`results/T-071/e4/phan-loai-phut.json`, 9 lượt, cửa sổ 10:13–17:57Z 22/11) ∩ phút Grafana đã đánh giá. Grafana đánh giá đủ mọi phút 10:00–18:09Z (490/490 phút, 66 truy vấn/phút = 6 tick × 11 luật, 32.340/32.340 ok), không khởi động lại kể từ 06:05:55Z → **0 phút bị loại**, mẫu số 383 ≥ 360. Cửa sổ nằm trọn sau giờ hiệu lực E4 (06:06:00Z). Phút có cờ lấn cửa sổ vẫn tính (quy tắc chính); bỏ chúng còn 338 phút, tử số vẫn 0.
- **Tỷ lệ:** 0 / (383/360) = **0 sự cố / 6 giờ khỏe ×1**; khoảng tin cậy Poisson 95%: [0; 3,47] / 6 giờ.
- **So R5: đạt** theo phép so đã khai (0 ≤ 1, mẫu số ≥ 360).

## Ba nguồn đối chiếu (đều 0)

| Nguồn | Kết quả | File |
|---|---|---|
| Bộ chấm offline trên chuỗi E4 do T-071 xuất (`cham_offline.py`, ngưỡng thật) | 0 khoảng cháy, 0 sự cố ở mọi lớp; 9 lượt, 0 khúc lỗi; 21.862 điểm chồng giữa file lượt, 0 lệch; lưới pha …0 s trùng tick Grafana | `e4/cham-offline.json` |
| Lịch sử trạng thái Grafana (`grafana.db` chỉ đọc) | 0 chuyển trạng thái của 11 luật từ commit G, kể cả Pending (đọc 19:07Z và 19:22Z) | `e4/k1-kiem.txt`, `e4/k2-grafana-luc-cham.txt` |
| Webhook (bộ nhận `t072-bo-nhan`) | 0 tin mới; file giữ nguyên 9 dòng của E3 (sha256 `b6f0de26…`) | như trên |

## Giải thích khác cho "0 sự cố" đã xét (`e4/giai-thich-khac.json`)

| Giải thích | Kiểm | Kết luận |
|---|---|---|
| Grafana không đánh giá luật | 66 truy vấn/phút ở mọi phút, tất cả ok; không khởi động lại | bác bỏ |
| Biểu thức không có dữ liệu (luôn NoData → OK) | p95 4 route: có điểm ở 100% bước khỏe ×1 và flash; liveness: 8 đích, 100% bước, giá trị 0; `mat-do` = 8 mọi bước; `mat-gw` 9,4–9,5 s | bác bỏ cho p95, liveness, mất quan sát |
| Luật lỗi im vì NoData | Luật lỗi không có điểm vì **không có 5xx nào** (`phu/5xx-*` = 0 ở mọi bước, 4 route); đúng thiết kế (≥ 3 lỗi 5xx) | 0 cảnh báo lỗi là đúng, nhưng luật lỗi **không được thử thách** ở E4 |
| Gai ngắn bị `for` che | Không bước thô nào vượt ngưỡng ở bất kỳ luật nào | không có gai để che |

## E4 hỗ trợ R5 tới đâu, và không chứng minh gì

- Hỗ trợ: trên 383 phút khỏe ×1 dưới tải ×1 thực, ngưỡng chọn từ E2 không gây báo động giả; đạt R5 theo phép so đã khai. Độ tin thấp: 0 sự cố trong 6,4 giờ không loại được tỷ lệ thật tới 3,47 / 6 giờ (đã nêu khi trình R5).
- **Không** chứng minh luật nhạy với lỗi thật: độ nhạy thuộc E5 và W6–W7. Bảy luật vẫn **chưa kiểm dương** trên dữ liệu thật: `t072-p95-booking`, `t072-p95-event`, `t072-p95-ticket`, `t072-loi-booking`, `t072-loi-ticket`, `t072-mat-do`, `t072-mat-gw`.
- Không nói gì về tải khác ×1 ngoài 38 phút flash (mô tả: 0 sự cố).

## Khoảng cách tới ngưỡng (quan sát, không dùng để chỉnh ngưỡng)

| Route | Max p95 duy trì 60 s, khỏe ×1 E4 (s) | Ngưỡng | Tỷ lệ với ngưỡng | So với M của E2 |
|---|---|---|---|---|
| booking | 0,0466 | 0,098 | 0,48 | 0,98 |
| event | 0,0447 | 0,097 | 0,46 | 0,97 |
| payment | 0,1544 | 0,184 | **0,84** | **1,26** |
| ticket | 0,0938 | 0,112 | **0,84** | **1,53** |

Với payment và ticket, giá trị lớn nhất ở E4 vượt M của E2 (26% và 53%), còn cách ngưỡng khoảng 16%. Hai giải thích chưa phân xử:
1. **Trôi:** DB tích lũy; E4 bắt đầu (10:13Z 22/11) khoảng 36 giờ sau khi E2 kết thúc (22:15Z 20/11).
2. **Dao động đuôi:** hai route này chỉ có ≈ 70 request / 5 phút, và E4 dài hơn E2 (9 lượt so với 8).

Cần thêm số liệu để phân xử: phân bố p95 theo thời gian trong lượt và giữa các lượt E2/E4, cùng chuỗi trôi của T-071. Nếu là trôi, các khoảng đo sau (E5, demo) có nguy cơ báo động giả ở payment và ticket. Ngưỡng **không** được sửa bằng E4; nếu sửa thì phải ghi "sửa sau" và kiểm trên một khoảng mới.
