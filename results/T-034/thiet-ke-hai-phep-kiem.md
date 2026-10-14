# T-034 — Thiết kế hai phép phân xử E1 và E2

Viết ngày 13/10/2026, 12:35 (+07), **trước khi chạy bất kỳ nhánh đổi nào**. Người viết: Claude (người làm T-034). Quyền: lời Minh ngày 13/10/2026 đưa hai phép vào T-034 (nguyên lời trong `tasks/T-034-g2-goi-trinh/SPEC.md`); lý do lựa chọn ở `docs/WHY.md`, mục “Bổ sung WHY-51”. File này cụ thể hóa hai phép đã duyệt, không phải một vòng xin duyệt mới. Mọi cập nhật về sau chỉ là mục nối ở cuối, có thời điểm.

Hai phép đều là **chẩn đoán trên dev đã nhìn**. Chúng không thay số, cấu hình hay cách chấm của baseline đã khóa; không chọn phương pháp cho P5/P6; không đo lan vật lý.

Điều tôi đã biết trước khi viết (để người đọc tự đánh giá mức độc lập của dự đoán): toàn bộ bản đối chiếu đính chính ngày 13/10, bảng 13 cặp ở hai ngưỡng của mã tác giả, bảng `pattern_candidate` (kích thước pattern tốt nhất của frontend ở bảy ca Nezha-OB), và `zero-lineage-summary-001.json` (hai dòng dõi bị về 0, kết quả với normalizer giữ cố định). Tôi chưa thấy bất kỳ kết quả nào của hai nhánh đổi dưới đây.

---

## E1 — Quy tắc pattern của TraceRCA

### 1. Câu hỏi

Trong bản TraceRCA cài theo lời văn của bài (phép T-O của T-032), một dịch vụ nhận điểm lớn nhất qua **mọi** tập dịch vụ (pattern) được giữ có chứa nó, kể cả tập nhiều dịch vụ. Việc cho điểm qua tập nhiều dịch vụ có góp phần đưa dịch vụ gọi (caller) hoặc `frontend` lên trên dịch vụ gốc (root) không, hay chênh lệch quan sát được chủ yếu đến từ các bước khác?

### 2. Điều đã đọc và xác minh trước can thiệp

Nguồn: bài Li và cộng sự, IWQoS 2021, Mục III-B và III-C (bản PDF cùng mã băm `771c24d0…` với bản T-032 đã đọc; đọc lại bản chữ trích bằng `pdftotext`, không chép vào repo); mã tác giả đã ghim `author-tracerca/source/run_localization_association_rule_mining_20210516.py` (commit `b9087c72…`); bản cài theo lời văn `results/T-032/scripts/tracerca_original_ranking_v1.py`.

| Điểm | Lời văn của bài | Mã tác giả (dòng) | Bản cài theo lời văn |
|---|---|---|---|
| Tập được chấm | Mọi tập nghi ngờ chứa dịch vụ; ví dụ của bài nêu cả tập hai dịch vụ lẫn tập một dịch vụ (III-C) | Chỉ tập một dịch vụ: `if len(pattern) > 1: continue` (365–366) | Mọi tập được giữ |
| Điểm dịch vụ | Lớn nhất của (chỉ số Jaccard của tập × điểm trong tập) | Như bài, nhưng chỉ trên tập một dịch vụ (368–377) | Như bài |
| Điểm trong tập | Trị tuyệt đối của hiệu số trace có lời gọi bất thường đi vào và đi ra, trong các trace chứa tập | `in_out_diff`, `np.abs(_target - _source)` (338–348) | Như bài |
| Chọn tập | k = 100 tập có chỉ số Jaccard cao nhất; không nói về hòa | 100 **mức điểm** khác nhau cao nhất, rồi cắt 1.000 pattern đầu (357–362) | 100 tập đầu, giữ mọi tập hòa ở vị trí thứ 100 |
| Dịch vụ không có tập | Không nói | Điểm mặc định −1 (363) | Không có điểm; khi xếp hạng tính 0, hòa nhau ở cuối |
| Hòa giữa dịch vụ | Không nói | Sắp theo (điểm, −kích thước pattern); thứ tự trong nhóm hòa theo tập hợp Python | Ghi hạng tốt nhất và xấu nhất |

**Đã xác minh:** ở điểm “tập nào được chấm”, bản cài theo lời văn **khớp lời văn của bài**; mã tác giả mới là bên lệch khỏi lời văn (chỉ chấm tập một dịch vụ). Vì vậy không có căn cứ gọi quy tắc “chấm qua mọi tập” là lỗi cài bài.

**Chưa thể quy là lỗi của bên nào:** vì sao mã tác giả chỉ chấm tập một dịch vụ (lịch sử kho mã chưa đọc; tên file có ngày 16/05/2021, gần ngày công bố); cách xử lý hòa ở vị trí thứ 100 và mức mặc định cho dịch vụ không có tập, vì bài không nói. Hai pipeline còn khác ở cách dựng lời gọi, chọn đặc trưng, chuẩn nền và gắn cờ; E1 **không** đụng tới các bước đó.

### 3. Phạm vi khai trước

Nguồn danh sách: `results/T-032/runs/bo-sung-toan-dien-20261012-001/closure-ledger-review-001.json#/h6_pair_audit/pairs`. Lấy đủ 13 cặp thuộc 11 ca, không bỏ cặp nào.

| # | Dataset | Ca | Root | Caller trong cặp | Quan hệ cũ ở `to_p` |
|---|---|---|---|---|---|
| 1 | RE2-TT | dev-12a1a88069 | ts-order-service | ts-seat-service | root dưới |
| 2 | RE2-TT | dev-db293894ab | ts-travel-service | ts-seat-service | root dưới |
| 3 | RE2-TT | dev-f36d0647d5 | ts-order-service | ts-seat-service | root dưới |
| 4 | RE2-TT | dev-f36d0647d5 | ts-order-service | ts-travel-service | hòa |
| 5 | Nezha-OB | dev-14701a3bbb | shippingservice | frontend | root dưới |
| 6 | Nezha-OB | dev-3e27669440 | adservice | frontend | root dưới |
| 7 | Nezha-OB | dev-515c5f2190 | recommendationservice | frontend | root dưới |
| 8 | Nezha-OB | dev-5467884de4 | recommendationservice | frontend | root dưới |
| 9 | Nezha-OB | dev-63c30faf34 | recommendationservice | frontend | root dưới |
| 10 | Nezha-OB | dev-6c9afc9822 | emailservice | frontend | root dưới |
| 11 | Nezha-OB | dev-6c9afc9822 | emailservice | checkoutservice | hòa |
| 12 | Nezha-OB | dev-7d3c2fe6d1 | shippingservice | frontend | root dưới |
| 13 | Nezha-OB | dev-95e164235f | paymentservice | checkoutservice | không có quan hệ (NO_USEFUL_FEATURE) |

Đơn vị là **cặp**; hai cặp chung một ca không phải hai mẫu độc lập. Cặp “root dưới” là điều kiện có hiện tượng (10 cặp); cặp “hòa” (2 cặp) và cặp 13 là điều kiện đối chứng về trạng thái.

**Cấu hình.** Pipeline tạo ra hiện tượng cũ có ba nhánh đã lưu trong `cases.json`:

- `to_p`: thời lượng span phía gọi, cờ lời gọi ở 1 lần độ lệch chuẩn. **Nhánh chính**: quan hệ cũ 0/4 và 0/8 định nghĩa ở đây.
- `to_p3`: như `to_p`, cờ ở 3 lần độ lệch chuẩn. Nhánh thứ hai.
- `to_c`: thời lượng span phía được gọi, 1 lần độ lệch chuẩn. Báo **phụ**: cùng trung gian, không dùng để đếm kết luận chính.

SPEC viết “các cấu hình ngưỡng 1 và 3 đã có”. Ở pipeline này đó là ngưỡng gắn cờ (1 và 3 lần độ lệch chuẩn). Ở mã tác giả, “ngưỡng 1 và 3” là ngưỡng **chọn đặc trưng**, một tham số khác. Số mã tác giả (ngưỡng chọn đặc trưng 1 và 3, đơn vị ms; nguồn Full008 qua ledger) được đặt ở cột riêng để đối chiếu. **Không** lấy chênh giữa hai pipeline làm tác động của quy tắc pattern.

Không mở rộng sang 41 ca còn lại của 52 ca dev.

### 4. Giữ nguyên, và đúng một yếu tố bị đổi

**Giữ nguyên, do chính mã nguồn tính:** bảng span của ca; cách dựng lời gọi; nền theo cặp dịch vụ; phép chọn đặc trưng; cờ lời gọi; trace bất thường; bảng kiểu trace (tập dịch vụ, tập có lời gọi bất thường đi vào, tập có lời gọi bất thường đi ra, bất thường hay không, số trace); khai phá tập phổ biến (support ≥ 10%); chỉ số Jaccard dạng phân số; tập được giữ `top` (100 tập đầu, giữ hòa ở vị trí cuối); công thức điểm trong tập; tập dịch vụ ứng viên (mọi dịch vụ có span); quy tắc thiếu điểm (tính 0 khi xếp hạng) và quy tắc hòa (hạng tốt nhất, xấu nhất).

Cách làm: gọi hàm `one_case` nguyên trạng của mã nguồn (nhập module ở chế độ chỉ đọc, `-B`). Thay `score_services` bằng một hàm bọc chỉ ghi lại đối số (`patterns`, `n_services`) rồi gọi hàm gốc. Nhờ đó nhánh đổi nhận **đúng** bảng kiểu trace mà hàm gốc nhận.

**Yếu tố duy nhất bị đổi:** trong vòng tính điểm, chỉ các tập trong `top` có đúng một dịch vụ được đóng góp điểm.

- Nhánh A (`all`, như nguồn): điểm(s) = max trên mọi tập T ∈ `top`, s ∈ T, của J(T) × |n_vào(s, T) − n_ra(s, T)|.
- Nhánh B (`singleton`): điểm(s) = J({s}) × |n_vào(s, {s}) − n_ra(s, {s})| nếu {s} ∈ `top`; nếu không thì **không có điểm**.

Không khai phá lại, không tuyển thêm, không bù tập một dịch vụ bị loại khỏi `top`. Dịch vụ không còn tập nào được ghi trạng thái riêng **“mất bằng chứng”**; khi xếp hạng nó nhận 0 theo quy tắc thiếu điểm của pipeline, nhưng 0 này không được đọc là “dịch vụ bình thường”. Phân biệt với điểm 0 có tập (hiệu vào − ra bằng 0).

Số học: phân số chính xác (`fractions.Fraction`) như nguồn; không có dung sai.

### 5. Kiểm tương đương trước khi diễn giải

1. **Nguồn và môi trường:** mã băm `tracerca_original_ranking_v1.py`, ba module nó nhập, `cases.json`, `summary.json` trên EC2 phải trùng bản ghim (`manifest-review-001.json#/source_pins`, `old-files-before.json`). Cùng trình thông dịch, biến môi trường và `PYTHONPATH` với lượt gốc (`runs/tracerca-original-ranking-001-launch/run.sh`).
2. **Bản giữ nguyên (sham):** chạy `one_case` gốc, dựng lại đúng các trường mà `main()` gốc ghi cho từng ca và từng nhánh, so với `cases.json` cũ. Mọi trường phải **bằng tuyệt đối**: trạng thái, số trace, số tập, hạng root, thực thể đứng đầu, pattern tốt nhất, quan hệ với caller, và cả các trường số thực. Dung sai khai trước: 0. Lệch thì tìm nguyên nhân và sửa bản cài của T-034, giữ lượt lỗi; không nới dung sai.
3. **Bản instrument, nhánh A:** điểm mọi dịch vụ và pattern tốt nhất phải trùng hàm gốc từng phân số; tập `top` dựng lại phải trùng về số tập, J lớn nhất, J nhỏ nhất.
4. **Ví dụ nhỏ tính tay** (ví dụ Hình 2 của bài, đã có trong fixture gốc): nhánh A cho A = 3, C = D = E = 4/3, B = 0, F không có tập; nhánh B cho A = 9/5, C = D = 4/3, E = 1, B = 0, F không có tập. Hai giá trị đổi (A và E) là do tập {A, B} và {A, B, E} có J cao hơn tập một dịch vụ.
5. **Tính lại độc lập:** một bản cài thứ hai chỉ dùng tập hợp Python trên bảng kiểu trace (không dùng mặt nạ bit, không dùng NumPy) tính lại J, n_vào, n_ra và điểm hai nhánh cho mọi dịch vụ ở mọi ca và nhánh; phải trùng từng phân số.
6. **Bất biến của nhánh B:** `top` của B là đúng `top` của A (cùng danh sách); tập ứng viên như nhau; điểm B(s) ≤ điểm A(s) với mọi s (vì B lấy max trên tập con). Vi phạm là lỗi cài.

Chưa đạt mục 1–6 thì không diễn giải nhánh B.

### 6. Đại lượng lưu

Theo ca và nhánh: bảng kiểu trace; số tập phổ biến; mọi tập trong `top` kèm thành viên, J (tử, mẫu), số trace bất thường chứa tập, số trace chứa tập; với từng dịch vụ: điểm A, pattern quyết định điểm A (thành viên, J, n_vào, n_ra), tập {s} có trong tập phổ biến không, có trong `top` không, điểm B, trạng thái bằng chứng ở mỗi nhánh; hạng (tốt nhất, xấu nhất) ở hai nhánh; thực thể đứng đầu; với từng cặp đã khai: điểm root và caller, quan hệ ở A và B, loại thay đổi.

### 7. Bảng diễn giải khai trước

Với mỗi cặp “root dưới” ở nhánh A:

| Kết quả ở nhánh B | Kết luận được phép |
|---|---|
| Root lên trên caller, cả hai đều còn tập một dịch vụ được chấm | Ở cặp này, cho điểm qua tập nhiều dịch vụ là bước làm caller đứng trên root **trong pipeline này**. Tác động riêng của quy tắc pattern được xác lập ở mức can thiệp cho cặp đó |
| Caller vẫn trên root, cả hai còn tập | Loại giải thích “thừa hưởng J của tập nhiều dịch vụ” cho cặp này trong phạm vi đã thử; chênh với mã tác giả phải đến từ bước khác (dựng lời gọi, chọn đặc trưng, gắn cờ, cách chọn tập) |
| Quan hệ đổi nhưng một bên mất bằng chứng | Ghi “đổi do mất bằng chứng”; không tính là root được định vị, không tính là loại giải thích |
| Hòa mới hoặc hòa mất | Báo riêng là thay đổi về hòa |
| Điểm đổi nhưng hạng tương đối không đổi | Báo tác động lên điểm, không lên hạng |

Tổng hợp: báo số cặp theo từng dòng trên, tách RE2-TT và Nezha-OB, tách `to_p` và `to_p3`. Kết luận về “bước Y” chỉ trong phép đổi đã cô lập:

- Nếu phần lớn cặp có hiện tượng đổi chiều mà không do mất bằng chứng: quy tắc pattern là một bước gây chênh đã xác nhận ở mức can thiệp cho các cặp đó. Điều này vẫn **không** nói mã tác giả “đúng hơn”, không nói về chờ hay lan vật lý, không nói phương pháp nào tốt hơn.
- Nếu phần lớn không đổi: giải thích ứng viên của bản đính chính (6/7 ca frontend lấy điểm từ tập 2–3 dịch vụ) không đủ; ghi “đã loại trong phạm vi đã thử”, bước gây chênh giữa hai pipeline còn mở và nằm ở các bước E1 không đụng tới.
- Kết quả lẫn lộn: nêu điều kiện tách hai nhóm (ví dụ mức chênh J giữa tập một dịch vụ và tập tốt nhất, hoặc n_ra của frontend).

Dự đoán của tôi, ghi để đối chiếu, không phải tiêu chí: tôi không chắc chiều. Ở ví dụ đã thấy (dev-63c30faf34), frontend lấy J = 0,937 từ tập hai dịch vụ với n_ra = 563, root có 0,937 × 534. Tập {frontend} chứa gần như mọi trace nên J của nó thấp hơn, nhưng n_ra tính trên nhiều trace hơn. Hai tác dụng ngược chiều, nên kết quả có thể khác nhau theo ca. Ở ba ca RE2-TT, root không có tập nào trong `top` (`root_best` rỗng), nên tôi dự đoán root vẫn không có điểm ở nhánh B và các cặp RE2-TT sẽ rơi vào dòng “mất bằng chứng” hoặc không đổi.

### 8. Máy, lệnh, chi phí

- **Máy:** EC2 từng chạy T-032 (`ubuntu@3.26.62.217`), vì bảng span đã phát lại và môi trường nằm ở đó. Chỉ ghi dưới `/home/ubuntu/rca/T-034/`. Nguồn T-032, T-031 và môi trường T-025 chỉ đọc.
- **Môi trường:** `/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8`; `PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 PYTHONHASHSEED=0`; `PYTHONPATH=/home/ubuntu/rca/T-034/e1:/home/ubuntu/rca/T-032/scripts:/home/ubuntu/rca/T-032/repo/src:/home/ubuntu/rca/T-025/src/RCAEval`; `TMPDIR` và cache đặt dưới T-034. Một tiến trình, không song song.
- **Chi phí đã biết:** lượt gốc mất 1,2–11,4 giây mỗi ca cho 11 ca này (`cases.json#/cases/*/wall_s`), cộng lại khoảng 41 giây. Số tập phổ biến lớn nhất là 1.815, nên không có rủi ro bùng nổ pattern ở các ca đã khai. **Dự toán (chưa đo cho code mới):** dưới 5 phút máy cho sham cộng hai nhánh và tính lại độc lập; đầu ra dưới 20 MiB. Ghi thời gian từng ca và RSS đỉnh.
- **Đưa về:** `results/T-034/runs/e1-<lượt>/`, kiểm mã băm hai đầu.

---

## E2 — BOCPD đầy đủ trong miền log trên hai ca underflow

### 1. Câu hỏi

Ở hai ca `dev-3ae0a6c15a` và `dev-ba831dbeb8`, bản BOCPD gốc làm tròn khối lượng posterior của một số dòng dõi (run length) về đúng 0 (underflow). Nếu tính posterior và chuẩn hóa hoàn toàn trong miền log, posterior đầy đủ, trạng thái có xác suất cao nhất (MAP) và điểm đổi (CP) có khác bản gốc không?

Kết quả cũ (`zero-lineage-summary-001.json`) chỉ phục hồi vài dòng dõi với normalizer của bản gốc giữ cố định, tại hai điểm đối chiếu FF/PF (chỉ số 411 và 522). Nó chưa trả lời cho cả chuỗi.

### 2. Phạm vi khai trước

Bốn chuỗi, không thêm, không bớt:

| Chuỗi | Ca | Nhánh | T | d | Nguồn (cùng mã băm ở laptop và EC2 T-033) |
|---|---|---|---|---|---|
| 1 | dev-3ae0a6c15a | FF (đầu vào full) | 1.441 | 36 | `runs/bocpd-rest-001/dev-3ae0a6c15a--full.npz` (`9a56942a…`) |
| 2 | dev-3ae0a6c15a | PF (tiền tố, mặt nạ cột của tiền tố, thang full) | 720 | 30 | `runs/bocpd-factorial-rest-001/dev-3ae0a6c15a--PF.npz` (`6b9f9e8d…`) |
| 3 | dev-ba831dbeb8 | FF | 1.441 | 36 | `runs/bocpd-rest-001/dev-ba831dbeb8--full.npz` (`09df5f3f…`) |
| 4 | dev-ba831dbeb8 | PF | 720 | 30 | `runs/bocpd-factorial-rest-001/dev-ba831dbeb8--PF.npz` (`1bfc5a9a…`) |

Đầu vào lấy từ chính NPZ nguồn: `X` (đã tiền xử lý, đúng thứ tự cột `columns`), `times`. Không đọc lại metric thô, không tiền xử lý lại. Nhãn (mốc tiêm, root) không vào phép tính; chỉ dùng sau cùng để đặt chỉ số 720 làm mốc đọc.

### 3. Giữ nguyên, và đúng một yếu tố bị đổi

**Giữ nguyên:** X, thứ tự cột, thời gian; prior của từng nhánh theo mã gốc (`MultivariateT(dims=d)`: dof = d + 1, κ = 1, μ = 0, scale = I); hazard hằng 1/50 (`constant_hazard(50, ·)`); phép cập nhật trạng thái `update_theta` của lớp gốc, gọi nguyên trạng, cùng thứ tự (tính mật độ dự báo → cập nhật posterior → cập nhật tham số); quy ước chỉ số m[i] = argmax R[:, i+1]; quy tắc CP: i ≥ 1 và |m[i] − m[i−1]| > 1 (`src/p3/adapters/phat_hien.py::diem_doi_tu_R`); hòa của argmax lấy chỉ số nhỏ nhất như NumPy.

**Yếu tố duy nhất bị đổi:** miền số học của posterior.

- Bản gốc: R tuyến tính, `R[1:t+2] = R[0:t+1]·pdf·(1−H)`, `R[0] = Σ R·pdf·H`, chia cho tổng.
- Bản miền log: `logR[1:t+2] = logR[0:t+1] + logpdf + log(1−H)`, `logR[0] = logsumexp(logR + logpdf + log H)`, trừ `logsumexp` của cả cột, ở **mọi** bước.

**Mật độ dự báo.** Bản gốc gọi `scipy.stats.multivariate_t.pdf(x, df, loc, shape)` với `shape = inv(κ·(dof−d+1)/(κ+1) · scale)`. Trong SciPy 1.14.1, `pdf` là `exp` của `logpdf`. Bản miền log gọi `multivariate_t.logpdf` với **đúng các đối số đó**, dựng bằng đúng các biểu thức của mã gốc, và không lấy `exp`. Vậy đây là log-density của cùng phân phối dự báo, tính ổn định; không lấy log của một PDF đã về 0.

Không thêm sàn, jitter, cắt run length, hay bất kỳ sửa mô hình nào. Không dùng normalizer của bản gốc.

### 4. Kiểm tương đương trước khi diễn giải

Dung sai dưới đây khai trước khi thấy kết quả nhánh đổi.

1. **Nguồn:** mã băm bốn NPZ; `_bocpd.py` phải là `4a57fde3…` (BARO `e35f4ec`, bản T-033 đã ghim trong `runs/prepare-001/inputs/source.json`); cùng trình thông dịch và thư viện với lượt gốc (Python 3.12.3, NumPy 1.26.4, SciPy 1.14.1 ở `/home/ubuntu/rca/T-025/envs/main`).
2. **Native sham:** chạy `online_changepoint_detection` gốc với lớp gốc, không bọc, trên X của từng chuỗi. Bắt buộc: `m` và `CP_flags` **trùng tuyệt đối** bản lưu; mọi phần tử R có giá trị lưu ≥ 1e-290 lệch tương đối ≤ 1e-9. Báo thêm tỷ lệ phần tử trùng từng bit. Không đạt thì không dùng chuỗi đó.
3. **Fixture F1, không underflow** (dữ liệu tổng hợp, T = 60, d = 3, có một lần đổi mức vừa phải): điều kiện hợp lệ của fixture là mọi trạng thái đạt được có R gốc > 1e-290. Bắt buộc: `exp(logpdf)` trùng `pdf` gốc từng bit, hoặc lệch tương đối ≤ 1e-12 thì ghi rõ; |logR_log − log R_gốc| ≤ 1e-9 ở mọi trạng thái đạt được; MAP ở mọi bước và tập CP trùng tuyệt đối; |logsumexp của mỗi cột| ≤ 1e-12; mọi giá trị của trạng thái đạt được hữu hạn; tham số (dof, κ, μ, scale) sau cùng trùng từng bit với một đối tượng gốc chạy riêng.
4. **F1 so với tham chiếu độ chính xác cao** (mpmath, 50 chữ số; bản cài độc lập của cùng mô hình: cập nhật tham số, ma trận nghịch đảo, định thức và hàm gamma đều tính trong mpmath, đệ quy tuyến tính): |logR_log − log R_tc| ≤ 1e-7; MAP và CP trùng ở mọi bước mà hai trạng thái đầu của tham chiếu cách nhau hơn 1e-6 (đơn vị log).
5. **Fixture F2, có underflow thật trong bản gốc** (cùng mô hình, T ≈ 80, d = 2, hai lần nhảy mức rất lớn): điều kiện hợp lệ là bản gốc có ít nhất một trạng thái bằng đúng 0 trong khi tham chiếu dương. Bắt buộc: bản miền log hữu hạn ở mọi trạng thái đạt được; |logR_log − log R_tc| ≤ 1e-6 + 1e-9·|log R_tc|; MAP và CP trùng tham chiếu (ngoài các bước hai trạng thái đầu cách nhau dưới 1e-6).
6. **Fixture F3, đối chứng dương cho phép toán** (bảng mật độ dự báo đặt sẵn, không dùng mô hình): một dòng dõi bị đẩy xuống dưới ngưỡng biểu diễn rồi sau đó có mật độ vượt trội. Theo số học chính xác nó phải thành MAP; bản gốc đã làm tròn nó về 0 nên không thể. Bắt buộc: bản gốc **khác** tham chiếu về MAP và CP ở ít nhất một bước; bản miền log **trùng** tham chiếu ở mọi bước; |logR_log − log R_tc| ≤ 1e-9 + 1e-12·|log R_tc|. Fixture này cho biết phép so có đủ khả năng phát hiện khi underflow thật sự đổi MAP.
7. **Chỉ số và thứ tự:** ở F1, `diem_doi_tu_R` gọi trực tiếp trên `exp(logR)` phải cho cùng m và CP với quy tắc áp trên logR.

Căn cứ của dung sai: sai số làm tròn của float64 trong miền log cỡ 1e-16 nhân độ lớn giá trị mỗi bước, cộng dồn qua tối đa 1.441 bước cho cỡ 1e-11; chọn 1e-9 có dư hai bậc. Tham chiếu mpmath khác float64 ở chuỗi nghịch đảo ma trận của mã gốc, nên dung sai nới tới 1e-7 và 1e-6. MAP, hòa và CP luôn báo riêng; posterior gần nhau không đủ để cho qua.

Lỗi của bản cài mới thì sửa trong T-034, giữ lượt lỗi, không gọi là kết quả khoa học.

### 5. So sánh toàn chuỗi và đại lượng lưu

Với mỗi chuỗi, so bản gốc (lấy từ native sham đã khớp bản lưu) với bản miền log ở **mọi** cột t = 1…T:

- Số trạng thái đạt được có R gốc bằng đúng 0; số trạng thái dưới ngưỡng chuẩn hóa (0 < R < 2,2e-308); cột và hàng đầu tiên xuất hiện mỗi loại.
- **Khối lượng bị mất:** log của tổng xác suất (theo bản miền log) nằm ở các trạng thái mà bản gốc đã cho bằng 0; giá trị lớn nhất theo cột và cột đạt.
- **Chênh posterior:** max |logR_log − log R_gốc| trên các trạng thái có R gốc ≥ 1e-290; khoảng cách biến thiên toàn phần ½·Σ|R_gốc − exp(logR_log)| theo cột, giá trị lớn nhất.
- **Khoảng cách hai trạng thái đầu** (log) theo cột ở cả hai bản; giá trị nhỏ nhất và cột đạt.
- **m, CP, timestamp:** vị trí khác đầu tiên của m; tập CP ở hai bản; CP thêm, CP mất kèm timestamp; báo động đầu trước và sau chỉ số 720.
- **Phân loại mỗi chỗ m khác:** (a) do underflow, khi trạng thái MAP của bản miền log có R gốc bằng 0 hoặc dưới ngưỡng chuẩn hóa; (b) do làm tròn hoặc hòa sát, khi cả hai trạng thái có R gốc bình thường và cách nhau dưới 1e-9; (c) khác, phải tìm nguyên nhân trước khi diễn giải.
- **Đối chiếu với kết quả cũ:** tại (chỉ số 411, cha 225) và (522, cha 204) cùng các điểm về 0 đầu tiên (371, 385), so logR_log với giá trị “normalizer giữ cố định” đã lưu. Hai cách tính chỉ khác nhau ở khối lượng đã mất khỏi normalizer, nên kỳ vọng lệch không quá 1e-6; lệch hơn thì phải giải thích.

Lưu: tóm tắt JSON theo chuỗi; một NPZ gọn chứa m và CP của ba bản (lưu, sham, log), các chuỗi theo cột nêu trên, năm trạng thái đầu của mỗi cột ở hai bản, và nguyên cột logR tại các chỉ số cần giải thích. **Không** lưu ma trận logR đầy đủ (16,6 MB mỗi chuỗi full); ai cần có thể tái tạo bằng script trong vài phút.

### 6. Bảng diễn giải khai trước

| Kết quả | Kết luận được phép |
|---|---|
| m và CP trùng ở cả bốn chuỗi; khối lượng mất rất nhỏ | Underflow không làm đổi MAP hay CP **trên bốn chuỗi đã kiểm**. Giải thích “underflow gây ra khác biệt FF/PF” được loại cho hai ca này trên toàn chuỗi. Không suy ra cho 28 ca còn lại hay cho cấu hình khác |
| m khác ở vài bước, CP trùng | Nêu bước, phân loại (a)/(b)/(c); tác động dừng ở đường MAP, không tới cờ |
| CP khác | Nêu timestamp thêm và mất, phân loại, và báo động đầu có đổi không. Hệ quả: số CP cũ của hai ca này có phần do số học; ghi vào K3 và §8. Bảng baseline đã khóa **không** bị sửa |
| Sham hoặc fixture không đạt | Không diễn giải; sửa và chạy lại, giữ lượt lỗi |

Trong mọi trường hợp: không suy ra bộ phát hiện tốt hơn hay kém hơn từ số CP; không dùng kết quả để chọn xử lý số học cho P6, chỉ để ghi căn cứ ở K5.

Dự đoán của tôi, ghi để đối chiếu, không phải tiêu chí: m và CP sẽ trùng. Lý do: dòng dõi bị về 0 đã mất hơn 700 đơn vị log so với dòng dõi dẫn đầu, và kết quả với normalizer giữ cố định cho thấy tại hai điểm đã kiểm nó còn cách MAP hơn 600 đơn vị log. Dự đoán này có thể sai ở phần chuỗi chưa ai kiểm, nhất là sau mốc.

### 7. Máy, lệnh, chi phí

- **Máy:** EC2 từng chạy T-033 (`ubuntu@3.107.246.249`). Lý do đổi so với ý “laptop có đủ nguồn”: bốn NPZ có sẵn tại chỗ với cùng mã băm, đây là máy và môi trường đã tạo bản gốc nên sham dễ khớp nhất, và laptop chỉ còn khoảng 2,5 GB RAM trống (đo 12:34). Đo trước khi chạy: 2 CPU, load 0,0, MemAvailable 7.481.065.472 byte, đĩa trống 1.319.153.664 byte. Không cần chuyển dữ liệu; chỉ chuyển script (vài chục KB). Đầu ra dự kiến dưới 30 MiB, không tạo môi trường mới.
- **Fixture:** chạy trên laptop khi viết code (nhanh, không cần dữ liệu), rồi chạy lại trên EC2 trong đúng môi trường của lượt thật; kết quả EC2 mới là bản dùng.
- **Môi trường EC2:** `/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8`; `PYTHONPATH=/home/ubuntu/rca/T-025/src/baro:/home/ubuntu/rca/T-025/repo/src`; `PYTHONDONTWRITEBYTECODE=1`; `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1` (ghi lại; ma trận 36×36 không được lợi từ nhiều luồng và hai tiến trình chạy cùng lúc trên 2 CPU); `TMPDIR` và cache dưới `/home/ubuntu/rca/T-034/`. Chỉ ghi dưới `/home/ubuntu/rca/T-034/`.
- **Chia việc:** hai tiến trình song song, mỗi tiến trình một ca (PF trước làm pilot, rồi FF). Mỗi chuỗi: sham rồi miền log.
- **Chi phí đã biết:** bản gốc có quan sát mất 314 giây (FF, dev-3ae0a6c15a) và 64 giây (PF) trên chính máy này (`dev-3ae0a6c15a--full.json#/wall_s`, `--PF.json#/wall_s`); RSS đỉnh khoảng 400 MB. **Dự toán (chưa đo cho code mới):** mỗi chuỗi tốn khoảng hai lần thời gian gốc (một lượt sham, một lượt log); mỗi ca khoảng (64 + 314) × 2 ≈ 13 phút máy; hai ca song song nên chờ thực tế khoảng 15–20 phút, tổng thời gian máy khoảng 26 phút. Không có lượt nào dự kiến quá 1 giờ. Cập nhật sau pilot PF.
- **Tiến độ:** ghi ra file mỗi 100 bước: bước, thời gian đã chạy, RSS.
- **Đưa về:** `results/T-034/runs/e2-<lượt>/`, kiểm mã băm hai đầu.

---

## Giới hạn chung

- Cả hai phép dùng 11 và 2 ca dev đã nhìn, chọn vì chúng có hiện tượng. Kết quả không ước lượng tần suất trên toàn dev và không nói gì về test.
- E1 kiểm một bước trong **một** pipeline (bản cài theo lời văn). Nó không biến bản đó thành baseline và không tái lập bài gốc: pipeline chỉ có một đặc trưng (độ trễ) và nền ngắn.
- E2 kiểm số học của **bản cài BARO** trên đầu vào đã tiền xử lý nhìn trước; nó không nói gì về chất lượng phát hiện, onset thật hay báo động sai trong vận hành.

---

## Mục nối 1 — 13/10/2026, 12:49 (+07): đổi dữ liệu của fixture F2, trước khi chạy bốn chuỗi thật

Bản thiết kế ghi F2 là “T ≈ 80, d = 2, hai lần nhảy mức rất lớn”. Lượt thử trên laptop (`runs/e2-fixtures-laptop-001-fail/fixtures.json`) cho F1 và F3 đạt, F2 **không đạt điều kiện hợp lệ**: bản gốc không có trạng thái nào bằng 0, khối lượng nhỏ nhất của tham chiếu chỉ tới e^−126. Mọi phép so khác của F2 trong lượt đó vẫn đạt. Đây là lỗi thiết kế fixture, không phải lỗi phép tính: phân phối dự báo Student-t có đuôi nặng, một lần nhảy chỉ phạt cỡ −(df + d)/2 · log(1 + z²/df), nên với df khoảng 30 không thể xuống dưới ngưỡng biểu diễn.

Thay đổi: F2 dùng 200 điểm ở mức 0, rồi 15 điểm ở mức 40 và 15 điểm ở mức −40 (d = 2, độ lệch chuẩn 0,01, cùng seed 20261013), tức T = 230. Bậc tự do tại lần nhảy đầu khi đó khoảng 200. Thử ba cấu hình trung gian (nhảy theo cấp số nhân tới 1,4e5; d = 3–8 với đoạn 20–45 điểm) đều bị loại: cái đầu làm mã gốc báo `LinAlgError` vì ma trận suy biến, các cái sau không tạo underflow. Lượt `runs/e2-fixtures-laptop-002/fixtures.json` với dữ liệu mới: F1, F2, F3 đều đạt; F2 có 2.335 trạng thái bằng đúng 0 và 195 trạng thái dưới chuẩn hóa ở bản gốc, bản miền log lệch tham chiếu tối đa 5,4e-10.

Không đổi: phép tính miền log, dung sai, các fixture F1 và F3, phạm vi bốn chuỗi, bảng diễn giải. Thay đổi này xảy ra trước khi có bất kỳ kết quả nào của bốn chuỗi thật.

Ghi nhận thêm từ F2, không phải kết quả khoa học: ở fixture có underflow thật này, bản gốc vẫn cho cùng MAP và CP với tham chiếu. Chỉ F3 (bảng mật độ đặt sẵn) mới làm underflow đổi MAP. Điều đó phù hợp với nhận xét rằng dòng dõi bị về 0 thường đã thua rất xa; nó không thay cho việc kiểm trên bốn chuỗi thật.

Kết quả E1 lượt 001 đã có trước mục nối này (chạy 12:41, sau khi bản thiết kế được ghim trên EC2 với mã băm `749090a5…`); mục nối này không đụng tới phần E1.

---

## Mục nối 2 — 13/10/2026, 13:03 (+07): lệch ở sham của E2 lượt 001, phép kiểm tất định và phép đo theo lịch sử dòng dõi

**Đã thấy gì khi viết mục này.** Lượt `e2-001` trên EC2 T-033: hai chuỗi PF đã xong; hai chuỗi FF đã xong phần sham, đang chạy phần miền log. Tôi đã thấy: (1) sham của cả bốn chuỗi trùng `m` và `CP_flags` với bản lưu; (2) R của sham **không** trùng bản lưu từng bit (55–87% phần tử trùng); (3) lệch tương đối lớn nhất trên phần tử ≥ 1e-290 là 4,3e-11 (3ae-PF), 7,0e-11 (3ae-FF), 8,9e-11 (ba83-FF) và **2,1e-9 (ba83-PF)**; (4) ở hai chuỗi PF, bản miền log cho `m` và CP trùng bản gốc; (5) ở ba83-PF, chênh |log R_gốc − logR_log| lớn nhất trên phần tử ≥ 1e-290 là 0,21, trong khi khoảng cách biến thiên toàn phần lớn nhất chỉ 3,7e-13.

**Hệ quả theo đúng tiêu chí đã khai.** Chuỗi ba83-PF **không đạt** tiêu chí sham “lệch tương đối ≤ 1e-9” (2,1e-9). Tôi không nới dung sai. Lượt `e2-001` được giữ nguyên; kết quả của nó chưa dùng để kết luận.

**Giả thuyết về nguyên nhân, phải kiểm trước khi chạy lại:**

1. *Vì sao sham không trùng bản lưu từng bit trên cùng máy, cùng môi trường.* Lượt gốc của T-033 không đặt biến luồng BLAS (`scripts/bocpd_job.sh`); lượt `e2-001` đặt `OPENBLAS_NUM_THREADS=1`. Số luồng có thể đổi thứ tự cộng trong phép nghịch đảo ma trận, làm density lệch ở bit cuối. Kiểm bằng chế độ `determinism` của `e2_bocpd_log_v2.py`: chạy lại vòng lặp gốc trên một chuỗi PF, một lần không đặt biến luồng, một lần đặt 1 luồng; so density và R với bản lưu từng bit.
2. *Vì sao lệch nhỏ ở density thành lệch 1e-9 đến 0,21 ở vài trạng thái.* Một dòng dõi có khối lượng tụt xuống vùng dưới chuẩn hóa (dưới 2,2e-308) chỉ còn vài bit có nghĩa; nếu sau đó nó lớn lên lại trên 1e-290 thì mang theo sai số làm tròn lớn. Đây là một dạng khác của cùng hiện tượng underflow (mất độ chính xác dần, trước khi về hẳn 0). Bản thiết kế đã bỏ sót trường hợp này: căn cứ dung sai 1e-9 giả định sai số chỉ cộng dồn đều.

**Thay đổi, khai trước khi chạy lại (lượt `e2-002`):**

- **Cấu hình luồng của lượt chạy lại:** nếu phép kiểm tất định cho thấy một cấu hình tái lập bản lưu từng bit thì dùng đúng cấu hình đó (khớp nguồn hơn; không chọn theo kết quả nhánh đổi). Nếu không cấu hình nào tái lập từng bit thì giữ 1 luồng và báo cả hai lần chạy.
- **Phép tính không đổi:** `log_run`, `LogLikelihood`, quy tắc m/CP, fixture và mọi dung sai đã khai giữ nguyên từng dòng (script v2 sinh từ v1 bằng `scripts/make_e2_v2.py`, chỉ thêm phần đo).
- **Phép đo thêm:** tách trạng thái vùng bình thường (R gốc ≥ 1e-290) thành hai nhóm theo lịch sử dòng dõi trong bản gốc: chưa từng xuống dưới 2,2e-308, và đã từng. Báo riêng sai số lớn nhất của từng nhóm, số trạng thái sai hơn 1e-9 và khối lượng lớn nhất của chúng.
- **Tiêu chí sham:** tiêu chí đã khai (`pass`) được giữ và báo nguyên. Báo thêm hai dòng riêng: phần bắt buộc theo SPEC (m và CP trùng tuyệt đối bản lưu) và tiêu chí R ≤ 1e-9 **chỉ trên dòng dõi chưa từng dưới chuẩn hóa**. Dòng thứ hai được đặt ra **sau khi đã thấy kết quả**, nên tôi ghi rõ nó là tiêu chí hậu nghiệm; việc dùng nó để coi một chuỗi là diễn giải được phải nêu trong báo cáo và để người phản biện, Minh xét. Nếu ngay cả dòng dõi chưa từng dưới chuẩn hóa cũng lệch quá 1e-9 thì chuỗi đó không diễn giải được.
- **Tiêu chí tương đương bản gốc ↔ miền log** cũng báo theo hai nhóm. Kỳ vọng nếu giả thuyết 2 đúng: nhóm chưa từng dưới chuẩn hóa lệch không quá 1e-9; nhóm đã từng có thể lệch lớn. Nếu nhóm thứ nhất lệch quá 1e-9 thì giả thuyết sai và phải tìm nguyên nhân khác trước khi diễn giải.

**Bảng diễn giải bổ sung:** nếu m và CP trùng nhưng có trạng thái của bản gốc sai hơn 1e-9 vì dòng dõi từng dưới chuẩn hóa, kết luận được phép là: underflow có làm sai posterior của bản gốc ở các trạng thái khối lượng rất nhỏ (nêu số trạng thái, mức sai và khối lượng lớn nhất), nhưng không đổi MAP hay CP trên chuỗi đã kiểm.

Không đổi: phạm vi bốn chuỗi, yếu tố bị đổi, bảng diễn giải chính, phần E1.

---

## Mục nối 3 — 13/10/2026, 13:13 (+07): kết quả lượt 001 và phép kiểm tất định; khai lượt `e2-002` trước khi chạy

**Đã thấy gì khi viết mục này.**

1. Lượt `e2-001` xong cả bốn chuỗi (`results/T-034/runs/e2-001/`, đã kiểm mã băm hai đầu). Ba chuỗi (3ae-PF, ba83-PF, ba83-FF) có `m` và CP của bản miền log trùng bản gốc. **Chuỗi 3ae-FF khác**: `m` khác ở 12 chỉ số liên tiếp (752–763); CP của bản gốc có 755, bản miền log có 752, 760, 764 thay vào; mọi CP khác trùng. Tại cột 753, 98% khối lượng của bản miền log nằm ở trạng thái mà bản gốc đã cho bằng 0 (dòng dõi bắt đầu ở chỉ số 240). Đây là điều **trái với dự đoán** tôi ghi ở mục E2.6.
2. Phép kiểm tất định (`runs/e2-determinism-001` trên EC2): không đặt biến luồng (OpenBLAS 2 luồng, đúng cấu hình lượt gốc của T-033) thì density 720/720 hàng và R trùng bản lưu **từng bit**, ở cả hai chuỗi PF; đặt 1 luồng thì density lệch từ bước 1 (ở chữ số thứ 15) và R chỉ trùng 55%, lặp lại cho đúng kết quả đó. Vậy giả thuyết 1 của Mục nối 2 đúng: lệch sham ở lượt 001 do tôi đặt `OPENBLAS_NUM_THREADS=1`, khác cấu hình nguồn.
3. Fixture của script v3 trên EC2, cấu hình luồng của nguồn (`runs/e2-fixtures-ec2-004-v3`): F1–F4 đạt. Hai lượt 002-v3 và 003-v3 không đạt F4 vì bản đầu của tham chiếu mở rộng lấy `exp` ở float64, mà ở F2 chính pdf float64 đã về 0; đã sửa thành `exp` ở độ chính xác mở rộng. Giữ cả hai lượt lỗi.

**Vì kết quả 3ae-FF khác thường, phải nghi bản cài trước khi tin.** Fixture F3 đã cho thấy bản miền log xử lý đúng trường hợp dòng dõi “chết” sống lại, nhưng trên bảng mật độ đặt sẵn. Thêm một tham chiếu độc lập **trên chính chuỗi thật**:

- **Tham chiếu số thực mở rộng.** Chạy đúng đệ quy tuyến tính của mã gốc (nhân, cộng, chia cho tổng; không có logsumexp) với R kiểu `np.longdouble` 80 bit, ngưỡng biểu diễn cỡ 1e-4931 thay cho 1e-308. Mật độ là `exp` (độ chính xác mở rộng) của cùng `logpdf`. Tham số và `update_theta` vẫn của lớp gốc. Tiêu chí khai trước: `m` và CP của tham chiếu **trùng tuyệt đối** bản miền log; |log R_mở rộng − logR_log| ≤ 1e-8 trên mọi trạng thái đạt được có logR ≥ −10.000. Không đạt thì chuỗi đó không diễn giải được và phải tìm nguyên nhân.
- Fixture F4 kiểm chính tham chiếu này bằng mpmath trên F2 và F3.

**Sửa một kỳ vọng sai của Mục nối 2.** Tôi đã viết rằng trạng thái có dòng dõi chưa từng dưới chuẩn hóa sẽ lệch không quá 1e-9 giữa bản gốc và bản miền log. Điều đó chỉ đúng khi khối lượng bị mất còn không đáng kể. Khi một dòng dõi đã bị bản gốc cho bằng 0 lại chiếm khối lượng lớn theo số học đúng, bản gốc chia cho một tổng thiếu phần đó, nên **mọi** trạng thái đều lệch. Phép đo sửa lại:

- “Trạng thái bị ảnh hưởng” = bằng 0 trong bản gốc, hoặc dưới chuẩn hóa, hoặc có dòng dõi từng dưới chuẩn hóa. Tính khối lượng của nhóm này theo bản miền log ở từng cột.
- Tiêu chí tương đương: trên các cột **trước** cột đầu tiên mà khối lượng đó vượt 1e-12, trạng thái sạch phải lệch không quá 1e-9. Sau cột đó, chênh lệch là hệ quả của underflow và được báo, không dùng làm phép kiểm bản cài.
- “Đoạn phân kỳ” = các cột liên tiếp có khoảng cách biến thiên toàn phần trên 1e-6. Một đoạn được coi là do underflow mở đầu khi ở cột đầu của nó, khối lượng của trạng thái bị ảnh hưởng chiếm từ một nửa khoảng cách đó trở lên.
- Phân loại chỗ `m` khác: (a) trực tiếp do underflow, khi trạng thái MAP của bản miền log là trạng thái bị ảnh hưởng; (a′) hệ quả trong đoạn phân kỳ do underflow mở đầu; (b) làm tròn hoặc hòa sát; (c) khác, phải tìm nguyên nhân.

**Lượt `e2-002`:** script `e2_bocpd_log_v3.py` (`2206b495…`), bốn chuỗi như cũ, **không đặt biến luồng** (đúng cấu hình nguồn; chọn theo phép kiểm tất định, không theo kết quả nhánh đổi). Mỗi chuỗi: sham → miền log → tham chiếu mở rộng. Dự toán từ số đo của lượt 001 và phép kiểm tất định (2 luồng chậm hơn 1 luồng khoảng 1,45 lần khi hai tiến trình chạy cùng lúc): mỗi chuỗi PF khoảng 5 phút, mỗi chuỗi FF khoảng 28 phút; hai ca song song nên chờ khoảng 35 phút, tổng thời gian máy khoảng 66 phút. Không lượt nào quá 1 giờ.

**Kết quả nào được dùng.** Nếu sham của `e2-002` đạt tiêu chí đã khai ban đầu (kỳ vọng trùng từng bit) và tham chiếu mở rộng đạt, thì `e2-002` là lượt dùng để kết luận; `e2-001` giữ làm lượt đối chiếu ở cấu hình 1 luồng. Nếu hai lượt cho `m` hoặc CP của bản miền log khác nhau thì báo cả hai và không kết luận trước khi hiểu vì sao.

**Bảng diễn giải cho 3ae-FF, nếu được xác nhận** (dòng “CP khác” của mục E2.6): nêu timestamp thêm và mất, độ trễ từ mốc tiêm trước và sau, cửa sổ 60 giây nào đổi dấu, báo động đầu có đổi không. Phạm vi: một chuỗi của một ca; không suy cho 28 ca còn lại, không đổi bảng baseline, không nói bộ phát hiện tốt hơn hay kém hơn.

---

## Mục nối 4 — 13/10/2026, 13:32 (+07): dừng hai chuỗi FF của lượt `e2-002`, chạy lại tuần tự ở lượt `e2-003`

**Đã thấy gì khi viết mục này.** Hai chuỗi PF của `e2-002` đã xong: sham trùng bản lưu từng bit, tham chiếu mở rộng trùng bản miền log, `m` và CP trùng bản gốc. Hai chuỗi FF của `e2-002` **chưa cho kết quả nào của nhánh đổi**: cả hai còn ở bước sham khi bị dừng.

**Vì sao dừng.** Lượt `e2-002` chạy hai ca song song, mỗi tiến trình hai luồng OpenBLAS, trên máy hai CPU. Ở d = 36 cách này chậm khoảng mười lần: sham FF mới tới bước 500 sau 459 giây (lượt `e2-001`, một luồng: khoảng 45 giây). Dự phóng cả lượt trên 3 giờ, vượt ngưỡng 1 giờ của AGENTS 3.8 và dự toán của Mục nối 3 (dự toán đó sai vì suy từ chuỗi PF, d = 1). Tôi dừng hai tiến trình lúc 06:27:20Z và ghi `INTERRUPTED-FF.txt` trong thư mục khởi chạy. Đây là lỗi điều phối của tôi, không phải kết quả khoa học.

**Lượt `e2-003`.** Cùng script v3 (`2206b495…`), cùng đầu vào, cùng cấu hình luồng của nguồn (không đặt biến luồng). Khác duy nhất: hai chuỗi FF chạy **lần lượt**, mỗi lúc một tiến trình, đúng như lượt gốc của T-033. Số đo đầu lượt: sham tới bước 1.000 sau 152 giây. Nếu một chuỗi dự phóng vượt 1 giờ thì dừng và báo Minh.

**Không đổi:** phạm vi bốn chuỗi, yếu tố bị đổi, tiêu chí sham, tiêu chí tham chiếu mở rộng, bảng diễn giải, quy tắc chọn lượt dùng để kết luận. Lượt dùng để kết luận gồm PF của `e2-002` và FF của `e2-003` (cùng script, cùng cấu hình luồng); `e2-001` vẫn là lượt đối chiếu một luồng. Phần FF dở dang của `e2-002` giữ nguyên, không dùng.

---

## Mục nối 5 — 13/10/2026, 13:58 (+07): đính chính một câu của Mục nối 4

Ở Mục nối 4 tôi viết dự toán sai “vì suy từ chuỗi PF, d = 1”. Câu đó sai. Số đúng, lấy từ tóm tắt của các lượt: chuỗi PF có T = 720 và d = 30; chuỗi FF có T = 1441 và d = 36.

Điều đo được: khi hai tiến trình chạy cùng lúc, mỗi tiến trình hai luồng, chuỗi PF vẫn chạy gần như bình thường (bước giữ nguyên 89 giây ở lượt `e2-002`, so với 75 giây ở lượt `e2-001`), còn chuỗi FF chậm khoảng mười lần. Vì sao hai loại chuỗi khác nhau như vậy thì **chưa kiểm**; một khả năng là thư viện đại số chỉ dùng nhiều luồng từ một cỡ ma trận nào đó. Tôi không kiểm thêm vì nó không ảnh hưởng kết quả khoa học: bản giữ nguyên trùng bản lưu từng bit ở các chuỗi đã xong, và lượt `e2-003` chạy lần lượt đúng như lượt gốc.

Không đổi gì khác trong thiết kế.

---

## Mục nối 6 — 13/10/2026, 17:41 (+07): đính chính cách tổng hợp ở mục E1.7, sau phản biện

Viết sau khi đã có kết quả E1 và sau hai lượt phản biện của Codex (Minh duyệt sửa). Không đổi phép kiểm, không đổi số.

Mục E1.7 có hai tầng: bảng theo từng cặp, rồi ba câu tổng hợp. Câu tổng hợp thứ hai (“phần lớn không đổi thì ghi đã loại trong phạm vi đã thử”) đã bị tôi dùng để viết kết luận phủ định cho cả nhóm. Cách dùng đó sai: nó che dòng đầu của chính bảng theo cặp, là dòng áp cho cặp có đổi chiều mà cả hai bên còn bằng chứng.

Cách tổng hợp đúng, thay ba câu cũ: báo theo từng loại cặp và không gộp thành một câu “có” hoặc “không”.

- Cặp đảo chiều, cả hai còn tập được chấm: quy tắc là bước quyết định ở cặp đó, mức can thiệp.
- Cặp có điểm của dịch vụ gọi giảm nhưng chưa đảo chiều: quy tắc có tác động lên điểm; không đủ để giải thích thứ hạng ở cặp đó.
- Cặp giữ nguyên cả điểm lẫn quan hệ vì root không có tập được chấm: phép đổi đã chạy và hợp lệ; nó không đánh giá việc bổ sung tập cho root.

Thêm một giới hạn: cặp đảo chiều ở nhánh chính thuộc ca dev-63c30faf34, là ví dụ tôi đã ghi số ngay trong mục E1.7 trước khi chạy. Kết quả ở cặp đó vẫn là can thiệp, nhưng không phải xác nhận trên mẫu độc lập.
