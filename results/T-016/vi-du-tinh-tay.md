# Ví dụ tính tay TORAI và lõi RCD trên một ca

T-016, S12. Số liệu từ `runs/s12-tinh-tay-goc.json`, `runs/s12-tinh-tay-sua.json`, bảng tóm tắt `runs/s12-tom-tat-goc.md`, `runs/s12-tom-tat-sua.md`, ví dụ chi-square `runs/s12-vi-du-chi2.txt`.

## 1. Chọn ca và cách kiểm

- **Luật chọn (ghi trong SPEC trước khi chạy):** torai-OB, code chính thức RCAEval, cửa sổ 10 (lệnh `docs/TORAI.md`), seed 0; ca đầu tiên theo thứ tự `sorted()` mà `main.py` dùng, có ít nhất một cụm từ 2 service. Ca đầu tiên `checkoutservice_cpu/1` thỏa (cụm `{cartservice, shippingservice}`), nên được chọn. Luật không dùng nhãn.
- **Script độc lập** `scripts/tinh_tay.py`: tự viết lại SeverityScorer, gộp service, BIC, điểm cụm, ghép dữ liệu trong cụm, rời rạc hóa K-means 1 chiều, phép kiểm chi-square, Ψ-PC cục bộ, vòng α, cách xếp theo p-value, hai pha của RCD, nhánh dự phòng. Không gọi hàm của TORAI, RCD, RCAEval, causal-learn, không gọi `KBinsDiscretizer`/`KMeans`. Chỉ gọi `GaussianMixture` của scikit-learn (thư viện) với đúng tham số, rồi tự tính lại log-likelihood và BIC từ tham số đã khớp.
- **Kiểm bản K-means tự viết** trên 2 995 cột thử ngẫu nhiên: 0 cột lệch tâm, 0 cột lệch mã bin so với scikit-learn 1.2.2 (`runs/s12-kiem-kmeans.txt`). Hai chi tiết phải chép đúng mới khớp: cụm rỗng sau khi dời điểm giữ "tổng" (bằng 0 trên dữ liệu đã trừ trung bình) làm tâm; tâm tính bằng tổng × (1/trọng số).
- **So với lượt chính thức cùng seed** (harness có thu giá trị trung gian, `D:\RCA-ext\work\T-016\s12-ct-torai`, `…-torai_sua`):

| Mục | Bản gốc | Bản sửa |
|---|---|---|
| Danh sách ứng viên, vectơ mức nghiêm trọng | trùng tuyệt đối | trùng tuyệt đối |
| BIC 14 giá trị (sklearn) | trùng tuyệt đối | trùng tuyệt đối |
| BIC tự tính so với sklearn | lệch tương đối ≤ 7,3e-16 | ≤ 7,3e-16 |
| Nhãn cụm, điểm cụm, danh sách `aa` | trùng | trùng |
| Số lần chạy Ψ-PC trong 3 cụm ≥ 2 service | 50, 28, 0 — trùng | 24, 34, 43 — trùng |
| Cột, dữ liệu đã rời rạc, hàng xóm F mỗi lần | trùng ở mọi lần | trùng ở mọi lần |
| p-value ở hàng F-node | lệch tương đối ≤ 1,3e-15 | ≤ 7,9e-15 |
| Thứ hạng RCD mỗi cụm, nhánh dự phòng | trùng | trùng |
| Thứ hạng cuối | giống hệt | giống hệt |

## 2. Bước 1 — Mức nghiêm trọng

Cửa sổ 10: metric 300 + 300 dòng, giảm còn 20 + 20; logts 20 + 20; tracets 20 + 20. Điểm lớn nhất mỗi nguồn (`ρ = max |x − μ| / σ`):
- metric (45 chuỗi): `checkoutservice_cpu` 264,9; `checkoutservice_mem` 29,58; `recommendationservice_cpu` 12,5; …
- log (30 chuỗi): `frontend_19` 2,96; `frontend_20` 2,559; `checkoutservice_21` 2,559; …
- trace_lat (17 chuỗi): `shippingservice_GetQuote` 10,48; `cartservice_AddItem` 8,947; `traceservice_Export` 8,947; …
- trace_err: 0 chuỗi (mọi cột hằng trong cửa sổ nên bị bỏ).

Chuẩn hóa trong từng nguồn rồi gộp theo service (metric, trace cộng; log lấy max):

| service | metric | log | trace_lat | trace_err | trung bình `y` | cụm |
|---|---|---|---|---|---|---|
| checkoutservice | 0,7087 | 0,1211 | 0,0524 | 0 | **0,2205** | 1 |
| cartservice | 0,0275 | 0,1110 | 0,2450 | 0 | 0,0959 | 0 |
| shippingservice | 0,0374 | 0,1110 | 0,2005 | 0 | 0,0872 | 0 |
| currencyservice | 0,0259 | 0,1126 | 0,0768 | 0 | 0,0538 | 2 |
| frontend | 0,0276 | 0,1401 | 0,0368 | 0 | 0,0511 | 2 |
| emailservice | 0,0348 | 0,1110 | 0,0349 | 0 | 0,0452 | 2 |
| traceservice | 0 | 0 | 0,1563 | 0 | 0,0391 | 3 |
| recommendationservice | 0,0505 | 0,0751 | 0,0268 | 0 | 0,0381 | 2 |
| paymentservice | 0,0210 | 0,1110 | 0,0175 | 0 | 0,0374 | 2 |
| adservice | 0,0212 | 0,1072 | 0,0204 | 0 | 0,0372 | 2 |
| health | 0 | 0 | 0,0762 | 0 | 0,0190 | 3 |
| productcatalogservice | 0,0168 | 0 | 0,0563 | 0 | 0,0183 | 3 |
| redis | 0,0244 | 0 | 0 | 0 | 0,0061 | 3 |
| frontend-external | 0,0044 | 0 | 0 | 0 | 0,0011 | 3 |

14 ứng viên, trong đó `traceservice`, `health` (chỉ từ trace), `redis`, `frontend-external` (chỉ từ metric) không phải service ứng dụng (khác biệt C8 ở hồ sơ).

## 3. Bước 2 — Gom cụm

BIC theo số cụm k (sklearn và tự tính trùng tới 3 chữ số thập phân ở mọi k): k = 1: −216,393; 2: −270,031; 3: −261,795; **4: −282,826 (nhỏ nhất)**; 5: −255,919; … 14: −45,291. Chọn k = 4.

Cụm và điểm cụm (trung bình `y`), xếp giảm dần:
1. cụm 1 `{checkoutservice}`: 0,2205 → 1 service, không chạy RCD.
2. cụm 0 `{cartservice, shippingservice}`: 0,0915 → chạy RCD.
3. cụm 2 `{currencyservice, frontend, emailservice, recommendationservice, paymentservice, adservice}`: chạy RCD.
4. cụm 3 `{traceservice, health, productcatalogservice, redis, frontend-external}`: chạy RCD.

## 4. Bước 3 — RCD trong cụm `{cartservice, shippingservice}` (bản gốc)

**Dữ liệu vào RCD.** Lấy 10 cột metric (cpu, mem, socket, workload, latency của mỗi service) và 8 cột log có tiền tố `cartservice`/`shippingservice`. Metric bị giảm mẫu lần hai còn 3 dòng: 2 dòng normal (chỉ số 0, 225), 1 dòng anomal (chỉ số 450). Nửa anomal 1 dòng nên mọi cột metric là hằng và bị bỏ: **0 cột metric**. Ghép với logts (chỉ số 0…19 và 20…39) bằng `concat` theo chỉ số: nửa normal có chỉ số `[0, 225, 1, …, 19]`, nửa anomal `[450, 20, …, 39]`. Dòng 225 và 450 không có log → điền 0: mỗi nửa thêm **1 dòng giả toàn 0**. Kết quả: 21 + 21 dòng, 8 cột log.

**Rời rạc hóa một cột** (`cartservice_13`, `runs/s12-vi-du-chi2.txt`):
- giá trị normal: 19, **0**, 21, 19, 22, 38, 20, 19, 20, 19, 17, 19, 20, 25, 24, 24, 29, 13, 13, 24, 20 (số 0 là dòng giả);
- giá trị anomal: **0**, 24, 26, 23, 21, 20, 20, 22, 20, 21, 23, 23, 21, 19, 20, 17, 20, 18, 24, 19, 20;
- tâm khởi tạo đều trên [0, 38]: 3,8; 11,4; 19; 26,6; 34,2 → tâm K-means: 0; 13; 19,731; 24,455; 38 → biên bin: 0; 6,5; 16,365; 22,093; 31,227; 38.
- Hai dòng giả tạo riêng một bin (tâm 0). Tức lỗi ghép dòng làm thay đổi cả cách chia bin.
- Số bin thực tế (edge case E1), đếm trên mọi cột ở mọi lần Ψ-PC của ca này: bản gốc 5 bin ở 306 lần-cột, 4 bin ở 10; bản sửa 5 bin ở 400, 2 bin ở 15, 0 bin ở 3 (mọi biên bị bỏ vì khoảng ≤ 1e-8, cột thành một mã duy nhất). Kết quả khớp code chính thức ở cả các trường hợp này (`runs/s12-tinh-tay-*.json`, trường `so_bin`).

**Một phép kiểm chi-square** (F ⊥ `cartservice_13`, tập điều kiện rỗng):

| | bin 0 | bin 1 | bin 2 | bin 3 | bin 4 |
|---|---|---|---|---|---|
| F = 0 (normal) | 1 | 2 | 12 | 5 | 1 |
| F = 1 (anomal) | 1 | 0 | 14 | 6 | 0 |
| kỳ vọng mỗi hàng | 1 | 1 | 13 | 5,5 | 0,5 |

χ² = 3,245; df = (2 − 1)(5 − 1) = 4; p = 0,5177. Với α = 0,01 (pha 1): p > α nên kết luận độc lập, bỏ cạnh F–`cartservice_13`.

**Vòng α và kết quả.**
- Pha 1, mức 1: hoán vị 8 cột, chia khối [5 cột, 3 cột]. Ở khối đầu, mọi phép kiểm có p từ 0,5177 tới 0,8156; F không còn hàng xóm nào cho tới α = 0,61. Ở α = 0,61, `shippingservice_15`, `cartservice_13`, `shippingservice_16` có p < α nên được giữ; kiểm có điều kiện bỏ tiếp `shippingservice_16` (p = 1, df = 0: hai chuỗi log `shippingservice_15`, `_16` đếm giống hệt nhau).
- Hai mức của pha 1 rồi pha 2; tổng 50 lần chạy Ψ-PC. RCD trả `[cartservice_13, shippingservice_16, shippingservice_15, shippingservice_26]` → service `[cartservice, shippingservice]`, đủ 2 service nên **không** rơi nhánh dự phòng.
- Đọc kết quả: nút được nhận là hàng xóm của F chỉ khi α ≥ 0,61, tức khi p ≈ 0,52–0,57. Không có bằng chứng phụ thuộc nào giữa F và các chuỗi này. Thứ tự RCD đưa ra ở đây là thứ tự của những p-value không có ý nghĩa thống kê.

Cụm 2: 28 lần Ψ-PC; RCD trả ít service hơn cụm → nhánh dự phòng (thứ tự mức nghiêm trọng). Cụm 3: không cột log nào, 0 cột metric → RCD nhận bảng rỗng, trả danh sách rỗng → nhánh dự phòng.

## 5. Bước 4 — Thứ hạng cuối và vì sao service gốc đứng hạng đó

Thứ hạng: `checkoutservice, cartservice, shippingservice, currencyservice, frontend, emailservice, recommendationservice, paymentservice, adservice, traceservice, health, productcatalogservice, redis, frontend-external`.

**Mở nhãn sau khi đã có thứ hạng:** ca `checkoutservice_cpu/1`, service gốc `checkoutservice`, lỗi CPU. Service gốc đứng hạng 1 vì:
- `checkoutservice_cpu` lệch 264,9 độ lệch chuẩn so với lúc bình thường, chiếm 70,9 % tổng điểm metric của mọi service;
- vì vậy vectơ của `checkoutservice` tách hẳn khỏi các service khác, GMM xếp nó thành cụm riêng có điểm cụm cao nhất;
- RCD không tham gia vào vị trí này (cụm 1 service).
Tức trên ca này, TORAI đúng nhờ SeverityScorer và GMM; lõi nhân quả không đóng góp.

## 6. Bản sửa, cùng ca

- Cụm `{cartservice, shippingservice}`: RCD nhận 20 + 20 dòng, 16 cột (8 metric + 8 log), 0 dòng giả. F có hàng xóm từ α = 0,21 (`cartservice_latency`, `cartservice_mem`); RCD trả `[cartservice_mem, cartservice_latency, shippingservice_16]` → đủ 2 service.
- Ba cụm chạy 24, 34, 43 lần Ψ-PC (gốc: 50, 28, 0).
- Thứ hạng cuối **giống hệt** bản gốc, vì service gốc đã nằm ở cụm 1 service và thứ tự trong các cụm còn lại không đổi.
- Ca này không đủ để nói bản sửa tốt hơn hay kém hơn. Ảnh hưởng trên toàn dataset: `giam-mau-hai-lan.md`.
