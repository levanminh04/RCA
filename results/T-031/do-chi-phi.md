# T-031 — Đo chi phí và chiếu cho 30 ca dev RE2-TT

Ngày 06/10/2026. Người làm: Claude. Laptop i5-1240P (16 luồng: 4 lõi P, 8 lõi E), RAM 15,7 GB, trống 2,1–3,8 GB trong lúc đo. Mọi lượt chạy tuần tự qua runner P3, giới hạn 3.600 s mỗi lượt (SPEC). Mã `src/p3` hash `8d4cc8196c87…` (`moi-truong.json`). Số trong file này lấy từ `chieu-chi-phi.json` (script `scripts/chieu_chi_phi.py`, cấu hình `work/cfg-chieu.json`) và `runs/<lượt>/tom-tat.json`. `chieu-chi-phi.json` là bản tổng hợp trước OLS/EC2, giữ làm lịch sử; số OLS và EC2 đọc trực tiếp từ `tom-tat.json`. Không có số accuracy nào.

**Trạng thái (cập nhật 06/10 chiều):** TORAI chạy đủ trên EC2 (Q-79); MicroRank đi tiếp (lời Minh); CIRCA khóa OLS (Q-80); BOCPD ở T-025 chạy trên EC2 không trần 20 giờ (Q-79). Mục 8 là việc chờ Minh lúc viết lần đầu, nay đã quyết.

## 1. Ca pilot (§12)

Luật khai trước ở LOG 10:20: sắp theo bộ yếu tố sau tiền xử lý, thứ tự từ điển; nhỏ nhất, trung vị dưới (vị trí 15/30), lớn nhất; hòa thì mã mờ nhỏ hơn. Không dùng nhãn. Bảng yếu tố 30 ca: `runs/yeu-to-002/yeu-to.json`; ca chọn: `ca-pilot.json`.

| Phương pháp | Yếu tố (thứ tự so) | Nhỏ nhất | Trung vị dưới | Lớn nhất |
|---|---|---|---|---|
| BOCPD | d = số cột sau chọn Q-67, bỏ cột hằng trên cả bản ghi | `dev-20acb4402d` (22) | `dev-3defe3d34b` (30) | `dev-4f8a844308` (39) |
| N-Sigma | số cột tập BOCPD đưa vào N-Sigma (D9 không bỏ cột hằng) | `dev-1e6d61b5ec` (25) | `dev-03d4910932` (34) | `dev-b8bd0abf60` (48) |
| N-Sigma đối chứng | mọi cột | `dev-1e6d61b5ec` (340) | `dev-14372e1209` (363) | `dev-b8bd0abf60` (375) |
| BARO | số cột còn ở cả hai nửa | `dev-260d332c8d` (264) | `dev-12a1a88069` (284) | `dev-16597725c1` (288) |
| SimpleRCA | (span, dòng log, cột metric) trong cửa sổ | `dev-260d332c8d` (51.863; 24.388; 345) | `dev-ba831dbeb8` (330.580; 116.396; 368) | `dev-b8bd0abf60` (644.791; 108.403; 375) |
| MicroRank, TraceRCA | (span sau lọc §5.2, operation) | `dev-260d332c8d` (51.863; 74) | `dev-ba831dbeb8` (330.580; 152) | `dev-b8bd0abf60` (644.791; 152) |
| CIRCA | (nút, cạnh, cha lớn nhất) của đồ thị từ N, hash seed 0 | `dev-260d332c8d` (273; 220; 8) | `dev-03d4910932` (290; 356; 15) | `dev-7f1b6b071d` (301; 499; 73) |
| TORAI A | số cột metric + `logts` + `tracets` vào `torai` | `dev-8017c6dc70` (516) | `dev-7f1b6b071d` (816) | `dev-12a1a88069` (966) |
| TORAI B | số cột metric + `logts` + `tracets` vào `torai` | `dev-1e6d61b5ec` (549) | `dev-57546fd87b` (1.015) | `dev-4f8a844308` (1.260) |

Lý do yếu tố đầu là khối lượng đầu vào lớn nhất phương pháp xử lý: §12 không nói cách gộp nhiều yếu tố (chi tiết thực thi, trình Minh ở mục 8).

## 2. Số đo từng bước (giây mỗi lượt; khoảng min–max)

Nguồn: `cost.buoc_s` trong bản ghi §13 (`runs/<lượt>/luot/*/ban-ghi-*.json`), tổng hợp từ `tom-tat.json`.

| Phương pháp (lượt) | Số lượt | Đọc | Cắt | Phương pháp | Wall | RSS đỉnh (MB) |
|---|---|---|---|---|---|---|
| MicroRank (`microrank-30-001`) | 30 | 0,7–1,8 | 0,0–0,3 | 1,1–6,3 | 2,1–8,7 | 253–1.642 |
| CIRCA SVR, hash seed 0 (`circa-svr-h0-lan1-001`) | 30 | 0,8–2,2 | 0,0–0,4 | 3,4–8,8 | 4,6–11,9 | 329–1.446 |
| BARO (`pilot-baro-001`) | 3 | 0,7–1,0 | ≈ 0 | 9,8–19,1 | 11,5–21,1 | 375–383 |
| SimpleRCA (`pilot-simplerca-001`) | 3 | 2,4–4,9 | 0,1–0,7 | 1,0–5,7 | 3,9–11,8 | 289–1.517 |
| TraceRCA (`pilot-tracerca-001`) | 3 | 1,5–4,2 | 0,0–0,6 | 21,1–52,2 | 23,8–59,1 | 508–1.813 |
| N-Sigma tập BOCPD (`pilot-nsigma-001`) | 3 | 0,6–1,9 | — | 4,4–11,5 | 5,4–13,9 | 134–136 |
| N-Sigma mọi cột (`pilot-nsigma-doi-chung-001`) | 3 | 0,6 | — | 97,9–107,2 | 98,9–108,3 | 137–140 |
| TORAI B (`torai-B-001`, dừng ở 16/90; laptop, lịch sử) | 16 | chuẩn bị: đọc 2,2–6,0; dựng bảng (Drain) 1,1–11,6 | 0,1–0,5 | `torai` 20,1–66,5 | 25,0–87,5 | 281–1.345 |
| CIRCA OLS, hash seed 0, laptop (`circa-ols-h0-001`) | 30 | 0,8–4,3 | 0,0–0,5 | 3,2–11,9 | 4,4–17,0 | 330–1.446 |
| TORAI B, EC2 (`torai-B-ec2-001`) | 90 | chuẩn bị 0,6–3,8 | — | `torai` 8,8–17,8 | 12,1–23,7 | 295–1.536 |
| TORAI A, EC2 (`torai-A-ec2-001`) | 90 | — | — | `torai` 8,2–18,2 | 10,9–20,8 | 175–178 |
| BOCPD tiền tố (mục 4) | 4 | đọc + tiền xử lý 1,6–5,3 | — | 38,7–183,8 | 41,9–186,9 | 182–184 |

## 3. Tổng đo thật trên 30 ca

| Phương pháp | Tổng wall 30 ca | Ghi chú | Nguồn |
|---|---|---|---|
| MicroRank, hash seed 0 | 158,5 s | 26 OK, 4 ERROR tính trượt (lời Minh 13:30, LOG T-031) | `dem-loi-microrank.json` |
| CIRCA OLS+RHT+DA (khóa, Q-80), hash seed 0 / 1 / 2 | 241,5 / 167,9 / 179,7 s | `runs/circa-ols-h{0,1,2}-001` | `do-nhay-builder.json` |
| CIRCA SVR(sigmoid)+RHT+DA (cấu hình phụ), hash seed 0 | 221,9 s (lượt 1); 212,0 s (lượt 2) | hai biến thể cùng một lượt | `k-svr.json` → `K_SVR4` |
| CIRCA **SVR**, hash seed 1 / 2 | 230,6 s / 224,1 s | độ nhạy builder | `do-nhay-builder-svr.json` |
| TORAI B (khóa), 3 seed, EC2 | 1.635 s (90 lượt, 12,1–23,7 s/lượt) | laptop dừng ở 16/90 (752 s) | `runs/torai-B-ec2-001/`, `runs/torai-B-001/` |
| TORAI A, 3 seed, EC2 | 1.274 s (90 lượt) | | `runs/torai-A-ec2-001/` |

## 4. Chiếu 30 ca cho phương pháp chạy pilot — **chưa kiểm**

Cách chiếu khai trước (LOG 10:42): wall mỗi lượt nội suy tuyến tính từng đoạn theo yếu tố đầu qua 3 ca pilot; cộng trên 30 ca. Nguồn: `chieu-chi-phi.json` → `pilot_chieu`.

| Phương pháp | Chiếu 30 ca | Cận thô 30 × min / 30 × max | Lượt dài nhất đo được |
|---|---|---|---|
| BARO | 437 s | 346 / 634 s | 21,1 s |
| SimpleRCA | 277 s | 117 / 353 s | 11,8 s |
| TraceRCA | 1.402 s | 715 / 1.772 s | 59,1 s |
| N-Sigma tập BOCPD | 216 s | 162 / 416 s | 13,9 s |
| N-Sigma mọi cột | 3.084 s | 2.967 / 3.249 s | 108,3 s |

**Giả định:** wall đơn điệu theo yếu tố đầu, nội suy được giữa 3 điểm. **Sai khi:** chi phí phụ thuộc yếu tố khác (ví dụ BARO: thời gian không tăng theo số cột ở 3 ca đo, 21,1 → 13,8 → 11,5 s); hoặc tốc độ máy dao động. Hai nguồn dao động đã thấy: (a) lượt đầu mỗi đợt chậm hơn do khởi động lạnh (cùng ca N-Sigma `dev-1e6d61b5ec`: 13,9 s ở lượt đầu đợt, 4,9 s ở đợt sau); lượt đầu luôn là ca có mã mờ nhỏ nhất trong danh sách, nên đầu nhỏ của nội suy có thể lệch lên; (b) tốc độ máy đổi ≈ 3 lần giữa chừng một lượt (mục 5). Không đo lại được trong task (SPEC cố định số lượt pilot).

## 5. BOCPD: đo trên tiền tố, chiếu 1.441 điểm và 30 ca — **chưa kiểm**, của laptop

Đo theo Q-77 và SPEC bước 6: tiền xử lý §7.2 trên cả bản ghi (giữ d của ca), lấy T điểm đầu, gọi `online_changepoint_detection` như §7.2; không tính điểm đổi, không dùng đầu ra ngoài thời gian và RSS. Nguồn: `runs/bocpd-tien-to-dev-20acb4402d-001/`, `runs/bocpd-tien-to-dev-4f8a844308-001/`, `chieu-chi-phi.json` → `bocpd`.

| Ca | d | T | Thời gian gọi | ms/lần gọi pdf | RSS đỉnh |
|---|---|---|---|---|---|
| nhỏ nhất `dev-20acb4402d` | 22 | 300 | 96,1 s | 2,13 | 183 MB |
| | | 600 | 183,8 s | 1,02 | 184 MB |
| lớn nhất `dev-4f8a844308` | 39 | 150 | 38,7 s | 3,42 | 182 MB |
| | | 300 | 146,0 s | 3,23 | 184 MB |

**Chiếu theo công thức khai trước:**
- p = log₂(t(2T)/t(T)): ca nhỏ 0,93; ca lớn 1,92.
- 1.441 điểm một ca: ca nhỏ 1.060 s (T²) hoặc 417 s (T^p); ca lớn 3.368 s (T²) hoặc 2.949 s (T^p).
- c = t(300)/300²: ca nhỏ 1,068e-3; ca lớn 1,622e-3; q = 0,73.
- **30 ca: 34,7 giờ (d², T²); 23,1 giờ (d^q, T²).** Thứ yếu, nhân (1441/300)^(p−2): 6,5 / 30,4 giờ (d²; p ca nhỏ / ca lớn), 4,3 / 20,2 giờ (d^q).
- Phân bố d ở 30 ca: 22–39, tổng 896 (`runs/yeu-to-002/yeu-to.json`). Số cột thô 25–48 mà ngoại suy T-030 dùng lớn hơn d thật.

**Chẩn đoán (tiến độ trong lượt, đã khai trước):** chi phí mỗi lần gọi pdf không đổi theo vị trí trong chuỗi ở cả 4 lượt khi máy chạy đều: lượt T = 600 ca nhỏ 0,9–1,5 ms ở mọi khoảng bước; hai lượt ca lớn 3,0–3,6 ms. Riêng lượt T = 300 ca nhỏ: 3,2 ms/lần ở ≈ 190 bước đầu (≈ 60 s), rồi 0,9–1,5 ms. Cùng dữ liệu, cùng ca, lượt T = 600 chạy nhanh ngay từ đầu, nên chỗ chậm là của máy, không của thuật toán. Hệ quả: p = 0,93 của ca nhỏ, c_nhỏ, q = 0,73 và các tổng neo theo c_nhỏ đều bị nhiễm đoạn chậm. Nguyên nhân máy chậm: chưa kiểm (giả thuyết: tiến trình chạy trên lõi E của i5-1240P, hoặc tải nền).

**Khoảng hợp lý trên laptop (thay số tham khảo cũ; REVIEW T-031 phiên 2, TR4) — chưa kiểm:** ≈ 8–35 giờ cho 30 ca. Hai giả thuyết dữ liệu chưa tách được: H1, chi phí ∝ d² (neo theo lượt chạy đều, ≈ 16,7 giờ); H2, chi phí gần như không phụ thuộc d (≈ 0,95 ms × 1441·1442/2 × 30 ≈ 8,2 giờ ở tốc độ nhanh). Số mũ d = 2,02 chỉ đúng nếu H1 đúng. Số chiếu chính khai trước (34,7 / 23,1 giờ) giữ nguyên ở trên.

**Giả định của mọi phép chiếu BOCPD:** chi phí mỗi lần gọi không đổi theo vị trí (đã thấy trong lượt tới T = 600; chưa kiểm ở 600–1.441); tốc độ máy như lúc đo. **Sai khi:** máy chạy chậm hơn (đã thấy dao động ≈ 3 lần); phần sau 600 bước đắt hơn (ví dụ do bộ nhớ: mảng `scale` T × d × d). Đây là số laptop; tốc độ EC2 chưa đo (EC2 của T-007: 2 vCPU = 1 lõi × 2 luồng, Xeon Platinum 8488C, `results/T-007/moi-truong-ec2.md:11`). Q-79 đã bỏ trần 20 giờ của Q-72 cho BOCPD trên EC2.

## 6. Đề xuất giới hạn `TIMEOUT` mỗi lượt cho T-024, T-025 (N3) — đề xuất, chờ Minh

- **T-024 (chế độ a, laptop):** giữ 3.600 s cho mọi phương pháp, như T-031. Lượt dài nhất đo được: TORAI B 87,5 s, TraceRCA 59,1 s; gấp ≥ 40 lần, đủ chịu dao động ≈ 3 lần của máy. Không chỉnh theo từng phương pháp để khỏi chọn sau khi thấy thời gian.
- **T-025, ranker ở t̂ (BARO, CIRCA, TORAI) và N-Sigma:** 3.600 s, cùng lý do (N-Sigma mọi cột 108 s).
- **T-025, BOCPD (một lượt = một ca đủ 1.441 điểm):** SPEC T-025 đo trước một ca trên máy chạy (ca nhỏ nhất, d = 22), chiếu ca lớn nhất (d = 39) theo d², rồi khai `TIMEOUT` = 3 × số chiếu đó trước khi chạy cả 30 ca. Hệ số 3 lấy từ dao động tốc độ đã thấy. Trên laptop số này sẽ ≈ 3 × 3.368 s ≈ 2,8 giờ (chưa kiểm). TIMEOUT tính trên máy chạy thật (EC2), không dùng số laptop.

## 7. Đề xuất phạm vi và lịch T-024, T-025 — đề xuất, chờ Minh

- **T-024 (chấm chế độ a, 30 ca dev, laptop):** chạy BARO (≈ 7 phút), SimpleRCA (≈ 5 phút), TraceRCA (≈ 23 phút), rồi evaluator trên mọi bản ghi. Dùng lại bản ghi 30 ca của T-031 khi hash `src/p3` không đổi: CIRCA (`runs/circa-ols-h0-001`, OLS đã khóa; SVR `runs/circa-svr-h0-lan1-001` làm cấu hình phụ), TORAI (`runs/torai-B-ec2-001`, `runs/torai-A-ec2-001`), MicroRank (`runs/microrank-30-001`; 4 ca ERROR tính trượt). Không chạy lại phương pháp đã có bản ghi hợp lệ. CIRCA báo trên 30 ca và riêng 19 ca không lỗi làm tròn (Q-82; 11 ca giống nhau ở hash seed 0, 1, 2, `kiem-11-ca-hashseed.json`). Thời gian máy mới ≈ 35–40 phút (chưa kiểm).
- **T-025 (chế độ b) — lịch đề xuất, chưa kiểm:**
  1. Trên EC2, đo một lượt tiền tố T = 300 cho ca nhỏ (d = 22) và ca lớn (d = 39) (vài phút đến ≈ 10 phút): có tốc độ EC2 và tách được H1/H2 (mục 5).
  2. Chiếu lại 30 ca; khai `TIMEOUT` = 3 × chiếu ca lớn (mục 6).
  3. Chạy BOCPD 30 ca tuần tự trong tmux; Minh theo dõi và có thể dừng (Q-79).
  4. Song song: laptop chạy T-024 và N-Sigma tập BOCPD, mọi cột (≈ 4 và ≈ 51 phút trên laptop, chưa kiểm).
  5. Ranker ở t̂ với hai bộ phát hiện, sau khi BOCPD xong.
- **Đề xuất nhanh hơn (luật cứng 12), chưa kiểm:** 30 ca BOCPD độc lập nhau; chạy song song nhiều tiến trình (mỗi tiến trình ≈ 200–300 MB RAM) trên máy nhiều lõi rút ngắn thời gian chờ gần theo số lõi. Máy EC2 của T-007 chỉ có 1 lõi vật lý nên lợi ít; laptop có 16 luồng nhưng lõi E chậm hơn. Đổi lại: Q-40 ghi "chạy tuần tự", và số đo thời gian từng ca sẽ nhiễu hơn (SL30). Cần Minh quyết.

## 8. Việc chờ Minh

**Đã quyết hết** (giữ làm lịch sử): (1) lời Minh 13:30 (LOG T-031); (2), (3) Q-79; (4) lời Minh "tôi duyệt mục 4".

1. **MicroRank D6:** 4/30 ca `ERROR` (operation mới sau mốc, mỗi ca đúng 1 operation). Nhánh đã dừng sau bước 2. Minh quyết bước tiếp cho MicroRank.
2. **TORAI > 1 giờ:** cho chạy tiếp lượt B (74 lượt còn lại, ≈ 55–60 phút) và lượt A (90 lượt, chưa đo, có thể ≈ 1 giờ). Chưa có thì K-B3, khóa nguồn TORAI, pilot và kiểm bước 5 của TORAI còn thiếu.
3. **BOCPD vượt Q-72 theo phép chiếu chính** (34,7 / 23,1 giờ trên laptop; số tham khảo ≈ 16,7 giờ; chiếu nhiễm đoạn máy chậm). Minh quyết: xem lại Q-72, đo lại tiền tố, hay đo một ca trên EC2 ở T-025 trước.
4. Chi tiết thực thi chọn trong task (trình để xác nhận): luật gộp nhiều yếu tố chọn ca pilot (mục 1); yếu tố N-Sigma là số cột tập BOCPD (§12 ghi "như BOCPD").
