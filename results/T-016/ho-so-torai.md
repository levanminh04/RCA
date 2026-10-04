# Hồ sơ kỹ thuật TORAI (kèm lõi RCD và biến thể RCD)

T-016, gói P1, cổng G1. Người làm: Claude. Ngày 04/10/2026.
Trả lời nhận xét của cô: "chưa sâu kỹ thuật của từng phương pháp". Đọc file này để hiểu TORAI và RCD mà không cần đọc code.

## 0. Cách đọc

- **Nguồn và revision** (theo `results/T-001/danh-sach-phuong-phap.md` mục 9):
  - Code chính thức: RCAEval `259ea4167160256a74ad30004aa3d96a998c846e` (viết tắt `RE`). `RCAEval/e2e/torai.py` và `rcd.py` giống hệt nhánh `fse26` của bài TORAI (kiểm bằng `git diff`, LOG phiên 1).
  - RCD gốc: `azamikram/rcd` `373882c6982db7a999ec1ff99ea54c644a48b409` (viết tắt `RCDg`).
  - Bài TORAI: arXiv `2604.13522v1` (FSE'26), dẫn theo mục (§) và bảng. Bài RCD: Ikram và cộng sự, NeurIPS'22, bản chính và phụ lục trên proceedings.neurips.cc.
- Dẫn code dạng `RE:đường/dẫn:dòng`. "Bài" là văn bản bài báo; "code" là RCAEval `259ea41`.
- Số liệu lấy từ file trong `results/T-016/` (đường dẫn ghi tại chỗ). Kết quả có ngẫu nhiên ghi kèm số seed.
- "Chưa kiểm" nghĩa là chưa có bằng chứng trong task này.
- Thuật ngữ: *severity* (mức nghiêm trọng), *cluster* (cụm), *chunk* (khối biến), *CI test* (phép kiểm độc lập có điều kiện), *intervention* (can thiệp), *F-node* (nút can thiệp), *fallback* (nhánh dự phòng).

## 1. Bài toán và đầu vào

**Bài toán.** Một sự cố đã được phát hiện ở thời điểm `t̂_A`. TORAI xếp hạng các service theo khả năng là nguyên nhân gốc (coarse-grained, mức service). Bài còn mô tả bước xếp chỉ báo (fine-grained) nhưng code không có bước đó (mục 5, khác biệt C1).

**Đầu vào theo bài (§2, §3.1).** Với mỗi service `s_i`, ba nhóm chuỗi thời gian:
- metric `𝒳ℳ_i` (bốn "tín hiệu vàng": traffic, saturation, latency, errors);
- log: số lần xuất hiện của từng mẫu log (Drain) trong mỗi khoảng thời gian, `𝒳ℒ_i`;
- trace: với từng operation, tần suất theo độ trễ và mã trạng thái, `𝒳𝒯𝒞_i`. Service không có trace (blind spot) thì thiếu nhóm này.
Dữ liệu chia tại `t̂_A`: đoạn bình thường `[t0, t̂_A)` và đoạn lỗi `[t̂_A, t̂_A + T)`. **`t̂_A` đến từ một bộ phát hiện bên ngoài**; TORAI không tự phát hiện.

**Đầu vào trong code** (`RE:main.py:268-417`, `RE:RCAEval/e2e/torai.py:69-77`):

| Bảng | Chu kỳ | Tên cột | Cửa sổ `main.py` với `--length L` |
|---|---|---|---|
| `metric` (`simple_metrics.csv`) | 1 s | `<service>_<loại>`, ví dụ `cartservice_cpu`, `cartservice_latency` | `L·30` dòng trước mốc + `L·30` dòng từ mốc (`main.py:314-315`) |
| `logts` (`logts.csv`) | 15 s | `<service>_<số mẫu>`, ví dụ `cartservice_13` | `L·2` dòng trước + `L·2` dòng từ mốc (`main.py:381-384`) |
| `tracets_err`, `tracets_lat` | 15 s | `<service>_<method>`, ví dụ `cartservice_GetCart` | như logts (`main.py:386-394`) |

- Mốc là `inject_time.txt` (thời điểm tiêm lỗi, không phải `t̂_A` do bộ phát hiện đưa ra). Tức RCAEval chạy TORAI ở **chế độ biết trước thời điểm** (MRP P3, chế độ a).
- `main.py` bỏ mọi cột `*_latency-50` (`:297`), đổi `*_latency-90` thành `*_latency`; với torai-TT chỉ giữ cột metric bắt đầu bằng `ts-` (`:299-302`); thay vô cực bằng NaN, `ffill`, điền 0 (`:305-309`).
- Cách dựng `logts`, `tracets` từ log/trace thô: `dung-logts-tracets.md`.

## 2. Từng bước xử lý, công thức

Ký hiệu: chuỗi `x^(i,j)` là chuỗi thứ `j` của service `i`; `N` = đoạn bình thường, `A` = đoạn lỗi.

### Bước 0 — Giảm mẫu metric (chỉ có trong code)

`metric = metric.iloc[::15]` (`RE:torai.py:81`, chú thích "the metric is sampled every second, resample for 15s"). Đây là lấy 1 dòng mỗi 15 dòng, không lấy trung bình. Mục đích: metric cùng chu kỳ 15 s với logts. Bài không nêu bước này (mục 5, C2).

### Bước 1 — SeverityScorer (bài §3.2; code `RE:torai.py:84-182`)

Với mỗi chuỗi, học trung bình `μ` và độ lệch chuẩn `σ` trên đoạn bình thường, rồi lấy độ lệch lớn nhất trong đoạn lỗi:

  `ρ(i,j) = max_{t ∈ A} |x_t(i,j) − μ(i,j)| / σ(i,j)`

- Code dùng `StandardScaler` (độ lệch chuẩn tổng thể, ddof = 0; nếu `σ = 0` thì thang = 1, tức `ρ = max |x_t − μ|`) (`:126-129`).
- Metric: trước đó `preprocess` bỏ cột `time`, bỏ cột hằng (riêng từng đoạn N, A), đổi `*_mem` sang MB, rồi chỉ giữ cột có ở cả hai đoạn (`:84-90`).
- Log: bỏ cột hằng trên cả cửa sổ trước khi chia (`:93-95`); bỏ chuỗi nếu đoạn bình thường rỗng (`:140-141`).
- Trace lỗi: `ffill`, điền 0, bỏ cột hằng; **đoạn bình thường bỏ 2 điểm cuối** (`:155`); nếu `μ = 0` và `σ² = 0` thì `ρ ← ρ·10⁹` (`:162-163`). Trace độ trễ: không bỏ điểm, không nhân (`:170-182`).
- **Chuẩn hóa trong từng nguồn** (code, không có trong bài): `ρ̃(i,j) = ρ(i,j) / Σ_{i',j'} ρ(i',j')` trên mọi chuỗi cùng nguồn (`:132, 149, 166, 181`).

Gộp về service (bài §3.2; code `:184-213`):
- metric, trace: cộng, `ρ_m(i) = Σ_j ρ̃_m(i,j)` (`fine2coarse_addup`);
- log: lấy max theo service, `ρ_l(i) = max_j ρ̃_l(i,j)`, rồi chuẩn hóa lại trên các service (`fine2coarse_highest`, `:196-208`);
- trace: code giữ **hai** cột riêng `trace_lat`, `trace_err` (bài gộp thành một `ρ_tc`); đổi tên `frontendservice` → `frontend` cho trace (`:225-226`).
- Service lấy bằng **tiền tố trước dấu `_`** của tên cột (`i.split("_")[0]`). Nguồn thiếu → điền 0 (`:236`; bài §3.2 cũng điền 0).

Kết quả: mỗi service một vectơ 4 chiều `v_i = [ρ_m, ρ_l, ρ_lat, ρ_err]` (bài: 3 chiều).

### Bước 2 — SymptomCluster: gom cụm bằng GMM (bài §3.3; code `:238-274`)

- Thử mọi số cụm `k = 1..n` (n = số service ứng viên). Mỗi `k` khớp một Gaussian Mixture Model (GMM) hiệp phương sai đầy đủ, `max_iter = 50`, `random_state = 0` (`:243-249`).
- Chọn `k*` có BIC nhỏ nhất: `BIC(k) = −2·ln L̂ + p·ln n`, với `p = k·d(d+1)/2 + k·d + (k−1)`, `d = 4` (`:250-253`).
- Khớp lại với `k*`, gán **cứng** mỗi service vào một cụm (`predict`, `:256-262`). Bài nói GMM cho phép gán mềm để một service vào nhiều cụm (§3.3); code không làm (C4).
- Điểm service `y_i = mean(v_i)` (trung bình 4 thành phần, `:263`). Điểm cụm = trung bình `y_i` trong cụm (`:265-272`). Xếp cụm giảm dần (`:274`).

### Bước 3 — CausalRanker: chạy lõi RCD trong từng cụm (bài §3.4; code `:276-334`, `:22-66`)

- Cụm 1 service: đặt thẳng vào thứ hạng, không chạy RCD (`:283-286`).
- Cụm ≥ 2 service:
  1. Xếp trước theo `y_i` giảm dần (danh sách `aa`, `:289-292`).
  2. Lấy mọi cột metric và log có tên **bắt đầu bằng** tên một service trong cụm (`str.startswith`, `:295-300`). Trace được truyền vào nhưng `_rcd_multimodal` **không dùng** (C5).
  3. `_rcd_multimodal` (`:22-66`): giảm mẫu metric **lần nữa** `iloc[::15]` (`:29`; C3 — lỗi, xem `giam-mau-hai-lan.md`); chia N/A; `preprocess`; ghép metric với logts bằng `pd.concat(axis=1)` **theo chỉ số dòng** (`:47-48`); bỏ cột trùng, điền 0, bỏ cột hằng, ghép thêm cột F-node; gọi `run_multi_phase(γ = 5, localized = True, bins = 5)` (`:65`).
  4. RCD trả một danh sách cột theo thứ tự nghi ngờ. Đổi về service bằng tiền tố, bỏ trùng (`:322-328`).
  5. **Nhánh dự phòng** (code, không có trong bài): nếu danh sách service từ RCD không dài đúng bằng số service của cụm, bỏ kết quả RCD và dùng thứ tự `aa` (mức nghiêm trọng) (`:330-334`).

### Bước 4 — RankAggregation (bài §3.5, Thuật toán 1; code `:276-340`)

Nối các cụm theo thứ tự điểm cụm; trong cụm theo thứ tự của bước 3. Đầu ra code: `["<service>_A", ...]` (`:336-340`).

### Bước 5 — FineGrainer (bài §3.6): **code không có**

Bài: với mỗi chỉ báo, học trung vị `med` và khoảng tứ phân vị `IQR` trên đoạn bình thường, `γ = max_{t∈A} |x_t − med| / IQR`, xếp chỉ báo theo `γ`. Code RCAEval chỉ trả service (C1).

### Lõi RCD (dùng ở bước 3, và là biến thể RCD)

**Ý tưởng (bài RCD §4).** Coi sự cố là một *can thiệp mềm* (soft intervention) lên biến gốc `R`: cơ chế sinh `P(R | Pa_R)` đổi giữa lúc bình thường và lúc lỗi. Thêm một biến nhị phân F (F-node): F = 0 với dòng bình thường, F = 1 với dòng lỗi. Ghép hai đoạn thành một bảng. Khi đó `X ⊥ F | Pa_X` đúng với mọi biến không bị can thiệp. Biến gốc là hàng xóm còn lại của F sau khi chạy PC (Ψ-PC). Định lý 1 của bài: với phép kiểm CI hoàn hảo, đủ nhân quả (không biến ẩn) và giả định trung thành mở rộng, thuật toán trả đúng biến gốc.

**Các bước trong code** (`RE:RCAEval/e2e/rcd.py`; patch causal-learn `RE:lib/causallearn/utils/PCUtils/SkeletonDiscovery.py:152-210`):

1. **Rời rạc hóa** (`rcd.py:231-236, 278-289`): ghép N và A, mỗi cột chia thành tối đa `bins = 5` khoảng bằng K-means 1 chiều (`KBinsDiscretizer(strategy="kmeans")`, tâm khởi tạo đều trên `[min, max]`). Khoảng rộng ≤ 1e-8 bị bỏ, nên số bin thực có thể < 5; cột hằng thành 1 bin. Sau đó mỗi cột mã hóa lại thành `0..c−1` theo giá trị có mặt.
2. **Phép kiểm CI chi-square** (`rcd.py:21`, causal-learn `chisq`): với bảng đếm `n_{s,x,y}` theo cấu hình `s` của tập điều kiện `S`,
   `χ² = Σ_s Σ_{x,y} (n_{sxy} − n_{sx·} n_{s·y} / n_{s··})² / (n_{sx·} n_{s·y} / n_{s··})`,
   bậc tự do `df = Σ_s (r_s − 1)(c_s − 1)` (chỉ đếm hàng/cột có kỳ vọng khác 0), `p = P(χ²_df > χ²)`; nếu `df = 0` thì `p = 1`.
3. **Ψ-PC cục bộ** (`SkeletonDiscovery.py:152-210`; bài RCD "Localized Learning"): bắt đầu từ đồ thị đầy đủ; **chỉ kiểm cạnh nối F với từng biến y**. Ở độ sâu `d`: duyệt các hàng xóm của F theo thứ tự hoán vị ngẫu nhiên (`:183`); với mỗi `y`, thử mọi tập `S` gồm `d` biến vừa kề `y` vừa kề F; nếu `p > α` thì bỏ cạnh F–y (`:193-204`); ngược lại ghi `p` vào danh sách p-value của `y` (`:205-206`). Tăng `d` cho tới khi bậc lớn nhất − 1 ≤ `d` (`:180`).
4. **Vòng α** (`rcd.py:121-208`): chạy Ψ-PC với `α = α0, α0 + 0,1, …` (< 1). Lần nào F có hàng xóm mới thì thêm vào danh sách, xếp nhóm mới theo p-value (bước 5). Dừng khi đủ `min_nodes` nút. α lớn nghĩa là khó kết luận "độc lập" hơn, nên giữ nhiều hàng xóm hơn.
5. **Xếp trong một lần** (`rcd.py:211-222`): lặp lấy nút có danh sách p-value **lớn nhất** (so như danh sách Python: so phần tử đầu, hòa thì so phần tử sau) đẩy xuống cuối. Kết quả: nút có p-value nhỏ nhất (phụ thuộc F mạnh nhất) đứng đầu. Bài RCD (phụ lục, Thuật toán 3) viết `argmax(max(P))`; code so cả danh sách (C10).
6. **Phân cấp (hai pha)** (`rcd.py:307-446`):
   - Pha 1: hoán vị ngẫu nhiên các cột (`np.random.permutation`, `:309`), chia thành khối `γ = 5` cột (`:310-315`); chạy Ψ-PC trên từng khối với `α0 = 0,01` (`LOCAL_ALPHA`, `:302`), dừng ở hàng xóm đầu tiên (`min_nodes = 1`); hợp các hàng xóm. Lặp lại trên tập hợp cho tới khi còn ≤ γ biến hoặc không giảm được nữa (`:428`).
   - Pha 2: chạy Ψ-PC một lần trên tập còn lại với `α0 = 0,001` (`START_ALPHA`, `:23`), cố xếp mọi biến (`min_nodes = số cột`, `:165-167`). Có thể trả **ít hơn** số biến nếu tới α gần 1 vẫn còn biến độc lập với F.
   - Ràng buộc `assert min_nodes < số dòng` (`:168`): nhiều biến hơn số dòng thì lỗi.

## 3. Đồ thị dùng ở đâu (theo vai trò ở K1 §3)

| Vai trò (K1 §3) | TORAI | Ghi chú |
|---|---|---|
| Biểu diễn topology / triển khai | **Không.** TORAI cố ý không dựng đồ thị gọi (bài §1, §2.3) | Đây là luận điểm chính của bài: tránh "blind spot" của trace |
| Ngữ cảnh feature cho bộ phát hiện | Không. Không có bộ phát hiện bên trong; `t̂_A` từ ngoài | |
| Đối tượng chấm bất thường | Không. SeverityScorer chấm từng chuỗi riêng | |
| Lan truyền điểm nghi vấn | Không | |
| Giả định nhân quả / có điều kiện | **Có, trong cụm.** Đồ thị nhân quả (chỉ khung kề quanh F-node) học từ chính dữ liệu của ca, nút là chuỗi thời gian (metric, mẫu log) | Pattern E ở K1 §D.2. Chỉ học cạnh kề F (bản cục bộ), không học cạnh giữa hai chuỗi |
| Xếp hạng ứng viên | **Có, gián tiếp.** Thứ tự trong cụm lấy từ p-value của cạnh F–nút | Chỉ khi không rơi nhánh dự phòng |

Kết luận cho câu hỏi "đồ thị phát hiện bất thường ở đâu" (WHY-02): ở TORAI, đồ thị không tham gia phát hiện, không lan truyền, không dùng quan hệ gọi. Nó chỉ là một khung nhân quả cục bộ dùng để sắp lại trong cụm. Ở cấu hình chạy chính thức, bước này hầu như không đổi thứ hạng (mục 5, C3 và `giam-mau-hai-lan.md`).

## 4. Tham số mặc định (code RCAEval `259ea41`)

| Tham số | Giá trị | Nơi | Ghi chú |
|---|---|---|---|
| Cửa sổ `--length` | mặc định 20 (`main.py:122`); lệnh của TORAI dùng 10 (`docs/TORAI.md`) | `main.py:122, 314-315, 381` | L phút = `L·30` giây mỗi phía; quyết định cửa sổ P3 chờ G1 (Q-54) |
| Giảm mẫu metric | 1/15 dòng, hai lần | `torai.py:81`, `:29` | lần hai là lỗi (C3) |
| Thang chuẩn hóa | `StandardScaler` | `torai.py:70` | có thể đổi qua `kwargs["scaler_function"]`; `main.py` không đổi |
| Bỏ 2 điểm cuối trace lỗi | `[:-2]` | `torai.py:155` | |
| Nhân khi `μ=σ²=0` | 1e9 | `torai.py:162-163` | chỉ trace lỗi |
| GMM | `covariance_type="full"`, `max_iter=50`, `random_state=0`, `k = 1..n` | `torai.py:243-261` | |
| Điểm service | trung bình 4 thành phần | `torai.py:263` | |
| RCD trong TORAI | `gamma=5`, `localized=True`, `bins=5` | `torai.py:22`, gọi ở `:65` | |
| `dk_select_useful` | `False` | `torai.py:33-34, 86-87`; `main.py:414` | bài RCD bỏ metric có độ lệch chuẩn < 1; RCAEval mặc định không |
| CI test | chi-square | `rcd.py:21` | |
| α pha 2, bước, trần | 0,001; 0,1; 1 | `rcd.py:23-25` | |
| α pha 1 | 0,01 | `rcd.py:302` | |
| γ | 5 | `rcd.py:303, 453` | |
| Seed | không đặt (`seed=None`) | `rcd.py:458, 486-487`; `rcd.py:294` có `# np.random.seed(0)` bị tắt | TORAI không có tham số seed |
| RCD gốc | `SEED=420`, `BINS=None`, `LOCAL_ALPHA=0.01`, `DEFAULT_GAMMA=5`, cục bộ chỉ khi `--local` | `RCDg:rcd.py:13-23, 115-119, 128-129` | gốc luôn đặt seed 420 |

## 5. Chỗ code khác bài

| # | Bài nói | Code làm | Bằng chứng | Ảnh hưởng (đo trong task, hoặc chưa kiểm) |
|---|---|---|---|---|
| C1 | Có FineGrainer xếp chỉ báo (§3.6, Bảng 5–7) | Không có; chỉ trả service | `torai.py:336-340` | Không tái lập được Bảng 5–7 bằng code này |
| C2 | Không nêu chu kỳ; §3.1 chỉ nói "bins the occurrence of log templates" | Metric 1 s giảm còn 1/15 dòng (lấy mẫu, không trung bình); logts/tracets 15 s | `torai.py:80-81`; `RE:docs/TORAI.md` mục Data Format | Chu kỳ 15 s chỉ có trong tài liệu RCAEval, không có trong bài (đã tìm trong văn bản HTML) |
| C3 | CausalRanker phân tích chuỗi đa nguồn của các service trong cụm (§3.4, Hình 3 có CPU, ErrLog, TraceLat) | Giảm mẫu metric lần hai trong cụm; ghép metric–log theo chỉ số dòng. Cửa sổ 10: **0 cột metric** vào RCD ở 90/90 ca OB, 90/90 SS, 30/30 TT; mỗi nửa thêm 1 dòng giả toàn 0 | `torai.py:29, 47-48`; `runs/s4-soi-dau-vao-*.jsonl`; `runs/s12-tinh-tay-goc.json` | Xem `giam-mau-hai-lan.md` |
| C4 | GMM gán mềm, một service có thể ở nhiều cụm (§3.3) | Gán cứng (`predict`) | `torai.py:262` | Chưa kiểm |
| C5 | CausalRanker dùng cả trace (Hình 3) | `_rcd_multimodal` nhận `tracets_*` nhưng không dùng | `torai.py:25-26, 312-321` | Chưa kiểm (không sửa trong task này, xem SPEC "Bản sửa") |
| C6 | Vectơ 3 chiều `[ρm, ρl, ρtc]` (§3.2) | 4 chiều (`trace_lat`, `trace_err` tách riêng), mỗi nguồn chuẩn hóa theo tổng | `torai.py:132, 149, 166, 181, 228-236` | Đổi trọng số giữa các nguồn; chưa kiểm |
| C7 | Không có | Nhánh dự phòng về thứ tự mức nghiêm trọng khi RCD không xếp đủ service của cụm | `torai.py:330-334` | Gốc, cửa sổ 10: 176/184 cụm OB, 171/173 cụm SS rơi nhánh này (`cham/s7-tong-hop.json`) |
| C8 | Ứng viên là "service" | Ứng viên là tiền tố tên cột: gồm cả `redis`, `frontend-external` (chỉ có metric), `health`, `traceservice` (chỉ có trace); lấy cột cụm bằng `startswith` nên `frontend` kéo theo `frontend-external_*` (OB), SS có 19–21 va chạm mỗi ca | `torai.py:185, 200, 295-310`; `runs/s4-soi-dau-vao-*.jsonl` | Ứng viên OB 14 thay vì 11 service; với SS, cột `*-db_*` lọt vào cụm làm danh sách service từ RCD không khớp cụm → dễ rơi nhánh dự phòng (chưa đo riêng) |
| C9 | `t̂_A` từ bộ phát hiện (§2) | `inject_time.txt` | `main.py:311-312` | Chế độ biết trước thời điểm; không đo được độ nhạy với `t̂_A` lệch |
| C10 | RCD xếp theo `argmax(max(P))` (phụ lục bài RCD, Thuật toán 3) | So cả danh sách p-value như list Python | `rcd.py:216-217` | Khác khi thứ tự theo danh sách p-value (so phần tử đầu, hòa thì phần tử sau) khác thứ tự theo max của danh sách. Ví dụ trong ca tính tay, α = 0,91: `cartservice_13` [0,5177; 0,5835; …], `shippingservice_16` [0,5698; …] — so danh sách chọn `shippingservice_16`, so max chọn `cartservice_13` (`runs/s12-tinh-tay-goc.json`; sửa theo REVIEW R5). Tác động tới đầu ra chưa đo |
| C11 | RCD bỏ metric có độ lệch chuẩn < 1 (phụ lục bài RCD, "Implementation and Test-bed Setup") | Chỉ bỏ cột hằng | `rcd.py:449-484`; `main.py:414` | Chưa kiểm |
| C12 | RCD gốc đặt seed 420 | RCAEval không đặt seed | `RCDg:rcd.py:13, 117`; `rcd.py:458` | Kết quả RCD, TORAI không lặp lại giữa các lần (xem `ngau-nhien.md`) |

Vì sao C4, C5, C6, C10, C11 "chưa kiểm": đo ảnh hưởng của chúng phải chạy một biến thể khác code tác giả (gán mềm, thêm trace vào RCD, đổi trọng số nguồn, đổi cách xếp, lọc cột theo độ lệch chuẩn). Đó là thay đổi phương pháp, nằm trong "Không làm" của SPEC; chỉ lỗi C3 được sửa. Giả định khi coi chúng là khác biệt nhỏ: nhánh dự phòng (C7) đã quyết định thứ hạng ở đa số cụm, nên đổi bên trong RCD ít ảnh hưởng điểm. Giả định sai nếu một thay đổi làm RCD xếp đủ service của cụm thường xuyên hơn. P4 kiểm được nếu cần.

## 6. Giả định và điều kiện thất bại do chính tác giả nêu

**TORAI (bài):**
- Chỉ báo của nguyên nhân gốc phải đổi phân phối rõ sau sự cố (§5 "Threats to Validity").
- Khi nguyên nhân gốc không có triệu chứng mạnh (ví dụ lỗi mã chỉ biểu hiện ở service phía dưới), TORAI xếp các service bị ảnh hưởng lên đầu, không xếp đúng gốc (§3.5).
- Thời điểm `t̂_A` có thể lệch; dùng trung vị/IQR (FineGrainer) để chịu được (§3.6, Hình 4). SeverityScorer vẫn dùng trung bình/độ lệch chuẩn nên không có tính chịu lệch này.
- Kết luận phụ thuộc loại lỗi, hệ thống, công cụ tiêm (§5).
- Cụm mức nghiêm trọng cao nhất có thể chỉ có 1 service trong khi gốc ở cụm thứ hai; vì vậy chạy CausalRanker cho mọi cụm (§3.5).

**RCD (bài NeurIPS'22):**
- Cần phép kiểm CI hoàn hảo, đủ nhân quả (không biến ẩn gây nhiễu) và trung thành mở rộng (Định lý 1).
- Biến ẩn làm sai: sự cố B thật, top-1 của RCD không thuộc service lỗi; tác giả cho rằng do biến ẩn và để lại cho sau (§6).
- Nguyên nhân nằm ngoài hệ quan sát: RCD chỉ chỉ ra service bị ảnh hưởng trực tiếp (§6, sự cố C).
- Cần đủ mẫu: Ψ-PC kém vì ít mẫu bình thường (§6 Sock Shop); phụ lục đo độ hiệu quả theo số mẫu lỗi.
- Bản vanilla sound nhưng không complete; có thể có dương tính giả (phụ lục).

## 7. Ví dụ tính tay (tóm tắt; chi tiết ở `vi-du-tinh-tay.md`)

Ca `torai-OB/checkoutservice_cpu/1`, cửa sổ 10, seed 0, chọn theo luật trong SPEC trước khi chạy. Script độc lập `scripts/tinh_tay.py` khớp code chính thức ở mọi bước: vectơ mức nghiêm trọng và BIC trùng tuyệt đối; mọi lần Ψ-PC (50 + 28 lần ở bản gốc) trùng cột, dữ liệu rời rạc, hàng xóm F; p-value lệch tương đối ≤ 1,3e-15; thứ hạng cuối giống hệt (`runs/s12-tinh-tay-goc.json`, `runs/s12-tinh-tay-sua.json`).

Vì sao service gốc đứng hạng 1 (đọc nhãn sau khi đã có thứ hạng): `checkoutservice_cpu` có `ρ = 264,9`, chiếm 0,709 tổng điểm metric; `checkoutservice` thành một cụm riêng với điểm cao nhất (0,2205). RCD không cần chạy cho cụm này. RCD có chạy cho cụm `{cartservice, shippingservice}` nhưng chỉ thấy cột log, và F-node chỉ có hàng xóm khi α ≥ 0,61 (p ≈ 0,52–0,57): không có bằng chứng phụ thuộc, RCD xếp gần như ngẫu nhiên.

## 8. Đường nhãn có thể lọt vào phương pháp

| # | Đường | Có lọt không | Bằng chứng |
|---|---|---|---|
| N1 | Tham số `service`, `fault_type`, `case` trong chữ ký `torai()` | Không: thân hàm không đọc; harness và `main.py` không truyền | `torai.py:69`; T-001 mục 4; harness truyền `sli=None` |
| N2 | `sli` suy từ tên service gốc (`main.py:340-365`) | Không: `torai`, `rcd` không đọc `sli` | T-006 mục 2.4 |
| N3 | Mốc tiêm `inject_time` dùng để chia N/A | Có, nhưng hợp lệ ở chế độ (a) "biết trước thời điểm". Ở chế độ (b) phải thay bằng `t̂_A` của bộ phát hiện | `main.py:311-315` |
| N4 | Biên file cắt đối xứng ±720 s quanh mốc tiêm | Không ảnh hưởng chế độ (a); ở chế độ (b) lộ vị trí lỗi | REVIEW T-002 R1; T-006 mục 2.3 |
| N5 | `tracets_lat` của bản Figshare dùng ngưỡng mean + 3σ tính trên **toàn file** (gồm cả sau mốc tiêm) | Không phải nhãn, nhưng là **dữ liệu tương lai**: ngưỡng của đoạn bình thường đã "thấy" đoạn lỗi | `dung-logts-tracets.md` mục 3 |
| N6 | Tên thư mục ca → tên file kết quả | Chỉ để chấm | harness, `main.py:283-286` |
| N7 | Chọn cửa sổ theo số công bố | Rủi ro thiết kế theo kết quả, không phải nhãn trong phương pháp. Cửa sổ P3 chốt ở G1 (Q-54) | T-006 mục 11.1 |

Phép thử giả (hai cửa sổ đều bình thường) và hoán vị cột: `kiem-khong-nhan.md`.

## 9. Yêu cầu đầu vào khi chạy trên dataset khác

Bảng đầy đủ: `yeu-cau-dau-vao.csv`. Tóm tắt:
- **Bắt buộc:** metric theo service (tên cột `<service>_<loại>`, 1 dòng/giây vì code giảm mẫu 1/15 để ra 15 s) và `logts` (15 s/dòng, tên `<service>_<id>`). `torai()` đọc `data["logts"]` trực tiếp (`:73`), không có log thì lỗi; muốn chạy không log phải truyền bảng chỉ có cột `time` (suy từ code, chưa kiểm bằng chạy: mọi ca trong task đều có log).
- **Tùy chọn:** `tracets_err`, `tracets_lat` (15 s/dòng, tên `<service>_<method>`).
- **Mốc sự cố:** bắt buộc (`inject_time` hoặc `t̂_A`).
- **Dữ liệu bình thường:** cửa sổ L phút cần `L/2` phút trước mốc (cửa sổ 10: 5 phút; 20 dòng 15 s).
- **Tên service:** không chứa `_`; không là tiền tố của tên service khác (C8). Với dataset có `-db` hay tên lồng nhau (Sock Shop), ứng viên và cột cụm bị trộn.
- **Không cần:** đồ thị gọi, nhãn để học, trace_id trong log.
- **Phải tự dựng:** `logts` (Drain + đếm theo 15 s), `tracets` (đặc tả ở `dung-logts-tracets.md`). Từ parquet RCAEval chỉ dựng lại chính xác được `tracets`, không dựng lại chính xác được `logts` bản Figshare.

## 10. Biến thể RCD

RCD (bản RCAEval, `RE:rcd.py:449-493`) là biến thể đối chứng của TORAI (Q-38). Nó dùng chung lõi `run_multi_phase` nhưng khác TORAI ở nhiều bước cùng lúc, nên chênh lệch điểm giữa hai bên **không quy riêng cho một bước nào**:

| Bước | TORAI | RCD |
|---|---|---|
| Nguồn tín hiệu | metric + log (+ trace cho SeverityScorer) | chỉ metric (`mmrcd` mới đa nguồn) |
| Giảm mẫu | 1/15, rồi 1/15 nữa trong cụm | không giảm (1 dòng/giây; cửa sổ 10 = 300 + 300 dòng) |
| Gom cụm | GMM + BIC trên vectơ mức nghiêm trọng | không |
| Tập biến vào Ψ-PC | cột của các service trong một cụm | mọi cột metric không hằng ở cả hai đoạn (cửa sổ 10: tối đa 45–53 cột ở OB, 52–68 ở SS, 272–301 ở TT; `runs/s4-soi-dau-vao-*-len10.jsonl`) |
| Đơn vị xếp | service (`<service>_A`) | metric (`<service>_<loại>`); chấm ở mức service bằng tiền tố, bỏ trùng (`main.py:560-572`) |
| Độ dài đầu ra | mọi ứng viên (nhờ nhánh dự phòng) | chỉ các metric RCD tìm được (T-006: 1–23 phần tử); service gốc không có trong danh sách thì tính trượt |
| Seed | không | không (`seed=None`) |

Hệ quả cho P3, P4 (chưa kiểm): RCD không xếp đủ ứng viên, nên AC@5, Avg@5 của RCD phụ thuộc độ dài đầu ra chứ không chỉ chất lượng xếp. Muốn so "có cụm và không cụm" thì cần một biến thể chỉ khác bước gom cụm (ví dụ chạy lõi RCD trên mọi cột metric + log của toàn hệ, giảm mẫu như TORAI). Task này không làm biến thể đó (SPEC "Không làm").

Kết quả RCD trong task: `diem-mo-t006.md` (torai-OB cửa sổ 20, Linux), `quy-mo-tt.md` (Train Ticket).
