# T-032 — Thiết kế phép đổi tất định, bản 003 (cách thực hiện K-2 và M-D trên laptop; lõi quan sát CIRCA)

Viết ngày 11/10/2026 (02:40 +07), trước khi chạy K-2 và M-D. Người viết: Claude. Bản 001 và 002 giữ nguyên. Định nghĩa của K-2 (bản 001 mục 8) và M-D (bản 001 mục 4) **không đổi**; bản này chỉ chốt cách thực hiện trên laptop và các đại lượng đọc thêm. Quy tắc chung ở mục 3 của bản 001 áp dụng y nguyên.

## 1. Điều tôi đã thấy trước khi viết

- Toàn bộ `ket-qua-phien-9.md`: kết quả A′, M-C1, T-D, B-1, B-2, S-1, K-1, phân rã SimpleRCA và TORAI B.
- Riêng với M-D: tôi đã biết kết quả T-D trên TraceRCA (cùng định nghĩa thời lượng chưa phủ): 18/22 cặp caller vẫn đứng trên root. Định nghĩa M-D được khóa ở bản 001 trước khi có kết quả này và không được sửa ở đây.
- Riêng với K-2: tôi đã biết kết quả K-1 (so hai bản ghi đóng băng có và không có DA) và đã chạy một ca thử `dev-a5cabe5fa7` trên EC2 để kiểm công cụ; nhánh sham của ca đó lệch bản đóng băng ở bit cuối nên không dùng. Chẩn đoán giá trị cực lớn của T-031 (`results/T-031/chan-doan-diem-lon.json`): nút `ts-admin-travel-service_latency` có y train chỉ gồm 2 giá trị khác nhau, độ lệch chuẩn cỡ 1e-16, phần dư cỡ 1e-17.

## 2. CIRCA trên laptop: sham, nhánh quan sát, K-2

Căn cứ nơi chạy: Minh cho phát lại CIRCA trên laptop (Q-130, Q-131 mục 2). Bản đóng băng CIRCA sinh trên laptop (`results/T-031/runs/circa-ols-h0-001`).

Mỗi ca ba nhánh, mỗi nhánh một tiến trình riêng, cùng môi trường như `src/p3/runner.py` đặt cho worker (PYTHONPATH theo thứ tự của runner, `PYTHONHASHSEED=0`, cờ `-B -W ignore`, không đặt biến số luồng):

1. **sham:** đường native nguyên vẹn `p3.worker.main` → `p3.adapters.circa.chay` → `circa_kien_truc.scoring.score_graph`; bản ghi dựng bằng `p3.runner._ket_thuc`.
2. **obs (quan sát, không phải phép đổi):** như sham, thêm một lớp bọc quanh `circa_kien_truc.scoring.score_graph` chỉ để giữ lại giá trị trả về đầy đủ của hàm (đồ thị metric có hướng, thứ tự duyệt DA, và với từng nút: cha, train/test của y và x, hệ số, phần dư, mean/var/scale của phần dư, z, điểm DA và `child_score`). Lớp bọc gọi hàm gốc với đúng đối số và trả đúng giá trị gốc.
3. **k2:** bọc `p3.adapters.circa.do_thi` để bỏ mọi cạnh của đồ thị trả về, giữ nguyên tập nút. Đây là bước duy nhất bị đổi (bản 001 mục 8).

**Điều kiện dùng:** hai bản ghi `ols+rht_da` và `ols+rht` của nhánh sham và của nhánh obs phải trùng bản đóng băng ở mọi trường trừ `run_id` và `cost`, số thực so theo biểu diễn hex, không dung sai. Chạy sham cho đủ 30 ca trước. Có ca lệch thì dừng toàn bộ CIRCA và báo Minh; không chạy K-2. Nhánh obs lệch ở ca nào thì trung gian của ca đó không dùng và cũng dừng để báo.

**Đại lượng đọc từ nhánh obs (mô tả, nối nhãn sau):**

- Với mỗi nút có |điểm RHT| > 1e10 (mốc báo riêng của Q-82): số giá trị khác nhau của y train, độ lệch chuẩn y train, scale của phần dư, số cha, đường hồi quy. Mục đích: xác nhận nguồn số học trên chính lượt OLS đã khóa, vì chẩn đoán T-031 làm trên lượt SVR.
- Với mỗi nút có thành phần đầu của khóa DA > 1e10: điểm RHT của chính nó có > 1e10 không, hay nó nhận qua `child_score`. Mục đích: kiểm suy luận của K-1 rằng giá trị cực lớn đi từ hậu duệ lên tổ tiên. Suy luận đó bị bác nếu có nút mang khóa DA cực lớn mà cả điểm riêng lẫn `child_score` đều không cực lớn.
- Hướng cạnh thật giữa các nút của root, của thực thể đứng trên root và của nút cực lớn.

**Đại lượng của K-2 (khai trước, như bản 001 mục 3.5 và mục 8):** với từng nút, điểm RHT native so với điểm khi không có cạnh; hạng root (rank_min, rank_max) ở ba bảng `native_rht`, `native_da`, `k2_rht`; tập thực thể đứng trên root; margin. Báo riêng nhóm ca có nút vượt 1e10 và nhóm còn lại (Q-82). Khi đồ thị không có cạnh, bước DA không có hậu duệ để cộng; ghi lại hai bảng k2 có cùng thứ tự thực thể hay không, không diễn giải thêm.

**K-2 phân xử được gì:** tác dụng của riêng bước "hồi quy nút theo các nút cha" lên điểm RHT và hạng root. Không phân xử tác dụng của DA (đó là K-1), không phân xử chất lượng của đồ thị gọi.

## 3. M-D trên laptop

Căn cứ nơi chạy: Q-130, Q-131 mục 2. Bước PageRank dùng float32 và BLAS, chỉ laptop tái lập bản đóng băng từng bit (WHY-43).

**Cách thực hiện, không sửa file mã nguồn nào:**

- Lấy mã nguồn của hàm `microrank.microrank` đang nạp (`src/microrank/__init__.py`, hash kiểm theo nguồn T-026) và thay đúng ba chuỗi, mỗi chuỗi phải xuất hiện đúng một lần:
  1. `df=data[COLS].copy()` → thêm một cột `u` do script tính trước từ chính `data[COLS]`;
  2. `before.groupby('operation',sort=True).duration.agg(` → dùng cột `u`;
  3. `after['abnormal']=after.duration/1000 >=` → dùng cột `u`.
  Mọi dòng khác, gồm phép chia trước/sau mốc theo `startTime+duration` gốc, kiểm hợp lệ, sắp xếp, đồ thị, PageRank, spectrum, là mã native không đổi. Hàm đã thay được gán vào `microrank.microrank` để adapter gọi; phần còn lại đi đúng đường worker và dựng bản ghi native.
- **sham:** cột `u` = `duration`. Bản ghi phải trùng bản đóng băng từng bit ở cả 52 ca (48 OK, 4 ERROR). Sham lệch ở ca nào thì M-D của ca đó vô hiệu; lệch thì dừng và báo.
- **md:** cột `u` = thời lượng chưa được span con trực tiếp phủ, tính bằng hàm `uncovered` của `scripts/tracerca_core_and_td_v1.py` (nạp nguyên hàm từ file đó, cùng 8 trường hợp tự dựng chạy lại trước). Con tìm theo `parentSpanID == spanID` trong cùng `traceID`, trên toàn bộ bảng span mà hàm nhận. Định danh span lặp không dùng làm cha. Đơn vị micro giây, số nguyên.
- Bốn ca nguồn ERROR: chạy như mọi ca; trạng thái của nhánh md được ghi đúng như xảy ra, không ép.

**Đại lượng (khai trước, bản 001 mục 3.5 và mục 4):** hạng root, tập thực thể đứng trên root, margin từng thực thể ở native và md; số span mang cờ và số trace nhóm A ở hai nhánh; với từng cặp (caller của root, root): còn đứng trên root hay không. Quan hệ gọi lấy từ `runs/caller-root-phien9-001/caller-root.json` đã có, không định nghĩa lại.

**Dự đoán đối lập:** giữ nguyên bản 001 (H-con, H-phần-chưa-phủ). Ghi thêm: M-D đổi phân hoạch A/N nên cả đếm phủ lẫn trọng số đổi theo; kết quả là tác động tổng của việc đổi đại lượng cờ, không so trực tiếp từng cặp với T-D.

## 4. Nơi chạy, canh RAM, chi phí

- Laptop, mỗi lúc một tiến trình con. Trước mỗi tiến trình con: chờ tới khi RAM trống ≥ 1,25 × RAM đỉnh của ca trong bản đóng băng + 6,5% tổng RAM (mốc 95% của Minh cộng 1,5% đệm). Trong lúc chạy lấy mẫu mỗi giây; RAM hệ thống đạt 95% thì giết tiến trình con, ghi sự kiện, quay lại chờ; cùng một tiến trình con bị giết 3 lần thì dừng cả lượt. Mốc 95% không đổi. Tiến trình con bị giết không để lại bản ghi nào được dùng; thư mục của nó giữ nguyên.
- Mỗi tiến trình con tối đa 600 s. Tổng chờ RAM tối đa 6 giờ.
- Ước lượng chưa đo: CIRCA 90 tiến trình con, bản đóng băng cộng 241 s cho 30 ca nên khoảng 20–30 phút; M-D 104 tiến trình con, khoảng 30–50 phút. Mỗi lượt dưới 1 giờ tính toán, không kể thời gian chờ RAM.
