# T-031 — Khóa cấu hình P3 theo phép kiểm không dùng nhãn

Ngày 06/10/2026. Người làm: Claude. Luật khóa khai trước ở `results/T-022/giao-thuc-v2.md` §6.5 (CIRCA, D5, WHY-30) và §6.6 (TORAI, D4, WHY-29). Không lượt evaluator nào chạy trên đầu ra thật trong T-031 (SPEC mục Không làm); khóa ghi trước mọi lượt evaluator. Mọi lượt dùng mã `src/p3` hash `8d4cc8196c87…` (đầy đủ: `moi-truong.json`, `src_p3_sau_sua_1`).

## 1. CIRCA kiến trúc — khóa **OLS** (đổi từ SVR ngày 06/10/2026, Q-80)

**Khóa hiện hành:** "CIRCA kiến trúc, OLS+RHT+DA, cấu hình P3"; SVR(sigmoid) báo làm cấu hình phụ. Minh duyệt (Q-80, WHY-30 ghi chú T-031, giao thức §6.5) sau chẩn đoán không dùng nhãn ở cuối mục này; chưa lượt evaluator nào chạy. Lượt OLS (`runs/circa-ols-h0-001`, 241,5 s, 0 lỗi runner): 30/30 ca OK cả hai biến thể; route 4.079 `no_effective_parents`, 4.526 `linear_regression`, 0 `value_error_fallback`; 0 z không hữu hạn; `current` = t+299 ở 30/30. Độ nhạy builder OLS (`do-nhay-builder.json`; bản SVR ở `do-nhay-builder-svr.json`): hash seed 1 / 2 đổi cạnh 24/30, cạnh gọi 0/30, thứ tự nút DA 24/30, thứ hạng thực thể DA 23/30 và 12/30. Bước 5 với OLS (`kiem-ca-that.json`, lượt `kiem-ca-that-003`): `current` 30/30, cửa sổ bình thường OK, hoán vị cột và dòng giống hệt.

**Lỗi làm tròn (Q-82, WHY-36, giao thức §6.5):** chỉ dùng bản OLS gốc, không biến thể sửa. Ca có ít nhất một nút điểm RHT > 1e10 là "ca lỗi làm tròn"; với hash seed 0, 1, 2 cùng 11 ca (`kiem-11-ca-hashseed.json`): `dev-03d4910932`, `dev-3ae0a6c15a`, `dev-4e68956051`, `dev-4f8a844308`, `dev-7f1b6b071d`, `dev-98bc73c499`, `dev-a505ab3f65`, `dev-a5cabe5fa7`, `dev-b8bd0abf60`, `dev-ba831dbeb8`, `dev-f9a8e05ed7` (nguồn `chan-doan-diem-lon.json`, cột `diem_ols`; không dùng nhãn). Bảng CIRCA báo trên 30 ca, kèm riêng 19 ca còn lại. Biến thể V∞ đã thử và bỏ (`runs/circa-vinf-001`, `k-vinf.json`; code đã gỡ, hash `src/p3` về `8d4cc8196c87…`).

Phần dưới là bản khóa SVR ban đầu (giữ làm lịch sử):

### 1a. Khóa ban đầu SVR(sigmoid)

Ghi lúc 06/10/2026 ≈10:50 (giờ máy), ngay sau khi có K-SVR3, trước lượt độ nhạy builder.

**Tên trong bảng:** "CIRCA kiến trúc, SVR(sigmoid)+RHT+DA, cấu hình P3". Báo kèm RHT-only cùng lượt.

**Luật (§6.5):** SVR nếu qua cả K-SVR1–4, không thì OLS.

| Phép kiểm | Điều kiện | Kết quả | Nguồn |
|---|---|---|---|
| K-SVR1 | `ANMRegressor(regressor=SVR(kernel="sigmoid"))`, tham số khác mặc định sklearn 1.6.0, qua lớp RCAEval `RHTScorer(regressor=…)` | Đạt: chỉ `kernel` khác mặc định (`rbf` → `sigmoid`); `cham_svr` gọi lớp RCAEval; trùng `CIRCA/circa/experiment/comparison/models.py:583–586` | `k-svr.json` → `K_SVR1` |
| K-SVR2 | 30/30 ca không ném lỗi, mọi z hữu hạn, không nút có cha hiệu lực rơi `value_error_fallback` | Đạt: 30/30 ca OK ở cả hai biến thể; route gộp 4.079 `no_effective_parents`, 4.526 `svr_regression`, 0 `value_error_fallback`; 0 z không hữu hạn; stderr mọi lượt rỗng | `k-svr.json` → `K_SVR2`, `ca`; `runs/circa-svr-h0-lan1-001/` |
| K-SVR3 | Chạy hai lần, đầu ra giống hệt | Đạt: 30/30 ca bản ghi giống hệt ở cả hai biến thể (so hash bản ghi trừ `run_id`, `opaque_id`, `cost`, `input_sha256`) | `k-svr.json` → `K_SVR3`, `K_SVR3_ca`; `runs/circa-svr-h0-lan2-001/` |
| K-SVR4 | Tổng 30 ca ≤ 3 giờ trên laptop (Q-40) | Đạt: 221,9 s (lượt 1), 212,0 s (lượt 2) | `k-svr.json` → `K_SVR4` |

**Giới hạn đi kèm (không đổi khóa):**
- Route ghi theo cách của `src/circa_kien_truc/scoring.py:44–57`: khớp lại hồi quy riêng và bắt `ValueError` ở `fit`/`predict`. Lỗi trong bước z-score của residual (cũng nằm trong `try` của RHT, `rht.py:118–124`) không được route bắt riêng; stderr rỗng ở 30 lượt cho thấy RHT không ghi cảnh báo dự phòng nào.
- Qua K-SVR chỉ nói "SVR chạy đúng cấu hình, đủ ngân sách, lặp lại được". Không nói SVR mạnh hơn OLS (WHY-30); không có số accuracy nào được xem.
- 300 s trace trước mốc dựng đồ thị; số nút, cạnh từng ca trong `k-svr.json` → `ca`.
- Độ nhạy builder (sau khóa, mô hình đã khóa; `do-nhay-builder.json`): so với hash seed 0, hash seed 1 và 2 mỗi cái đổi cạnh đồ thị metric ở 24/30 ca, không đổi cạnh gọi ca nào, đổi thứ tự nút DA ở 24/30 ca; đổi thứ hạng thực thể DA ở 22/30 (seed 1) và 7/30 (seed 2). Seed khóa vẫn 0; không chọn seed theo kết quả.

**Chẩn đoán thêm, ghi sau khi khóa, không đổi khóa (trình Minh):**
- SVR(sigmoid) gần như không hồi quy ở đa số nút có cha (`chan-doan-svr.json`, 3 ca pilot CIRCA): std(dự đoán)/std(y train) < 0,01 ở 89/114, 103/157, 105/154 nút; trung vị 2e-13–5e-12; vài nút phình tới 54–94 lần. Điểm RHT của SVR gần z-score không hồi quy (Spearman 0,84–0,97; top-10 nút trùng 9–10/10). Code CIRCA gốc cũng không chuẩn hóa dữ liệu trước hồi quy (`CIRCA/circa/alg/ci/anm.py:21–31`; `circa/model/data_loader.py:69–110`), nên đây là hành vi của cấu hình đúng bài trên metric RE2-TT, không phải lỗi cài. K-SVR1–4 không được thiết kế để thấy điều này. Hệ quả cho P4: với SVR, cạnh đồ thị ít tác động lên điểm RHT; tác động đồ thị còn lại chủ yếu qua DA.
- 13 nút ở 13/30 ca có điểm RHT > 1e6 (`chan-doan-diem-lon.json`). 11/13 là nút có y train chỉ 2 giá trị khác nhau ở mức sai số dấu phẩy động (std ≈ 1e-16): residual train std ≈ 2e-17 nên z ≈ 7,7e15–6,9e17; OLS cho cùng hiện tượng (8,7e15–7,0e17), z-score không hồi quy cùng nút chỉ 0,2–9,3. 2/13 là lệch thật (1,1e6–1,2e6 ở cả SVR, OLS, z-score). Đây là hành vi z-score residual của RHT gốc (`RCAEval/graph_heads/rht.py:22–28`); nút đó đứng đầu danh sách CIRCA ở 11 ca bất kể lỗi.

## 2. TORAI — khóa **nguồn B** (tự dựng từ parquet RE2)

Ghi lúc 06/10/2026 ≈14:35 (giờ máy), ngay sau khi có K-B3 đủ 90 lượt; trước mọi lượt evaluator.

**Luật (§6.6, D4, WHY-29):** B làm dòng chính khi đạt K-B1, K-B2, K-B3; không thì A. Cả A và B đều đã chạy và giữ.

| Phép kiểm | Kết quả | Nguồn |
|---|---|---|
| K-B1 | Đạt (T-030): `tracets_err` 99,95 %, `tracets_lat` 99,39 % ô theo tên cột, gộp 30 ca | `results/T-030/k-b1.json` |
| K-B2 | Đạt 30/30 ca: tổng `logts` B mỗi service = số dòng log của service trong cửa sổ | `k-b.json` → `K_B2` |
| K-B3 | Đạt 90/90 lượt (30 ca × seed 0, 1, 2) OK, không lỗi runner, `key_check` pass 90/90 | `k-b.json` → `K_B3`; `runs/torai-B-ec2-001/` |

**Ghi kèm (không phải cổng):**
- Chạy trên EC2 theo lời Minh (LOG 13:45); laptop dừng ở 16/90 (`runs/torai-B-001`). Ở 16 lượt trùng, thứ tự và bản ghi §13 của EC2 giống hệt laptop (16/16). Hash tệp bảng CSV khác ở cả 16 (chưa kiểm trực tiếp vì CSV đã xóa; giải thích khả dĩ: ký tự xuống dòng Windows/Linux, vì nội dung đưa vào TORAI cho bản ghi giống hệt).
- Tỉ lệ cụm nhiều service rơi nhánh dự phòng `y_train`: gộp 302/342 = 0,88; từng lượt 0,25–1,0. Nghĩa là thứ tự trong cụm phần lớn theo mức nghiêm trọng, không theo RCD (như SL36).
- Thứ tự giữa 3 seed: B giống nhau ở cả 3 seed ở 18/30 ca, 2 thứ tự khác nhau ở 9 ca, 3 ở 3 ca; A: 26, 3, 1.
- Nguồn A (`runs/torai-A-ec2-001`): 90/90 OK. Thứ tự A khác B ở 30/30 ca (seed 0). Lệch lưới A 0–14 s (`runs/lech-luoi-a-002`).
- Danh sách TORAI chỉ có 3–5 nhóm hòa cấp cụm cho 68 thực thể ở ca kiểm (§11.9); cách tính hòa theo §8.4.
