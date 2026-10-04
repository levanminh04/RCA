# Hồ sơ kỹ thuật: GDN (Graph Deviation Network)

T-018, người làm Claude, ngày 04/10/2026. Bộ phát hiện bất thường đa biến dùng đồ thị học được (Q-30, Q-37).

**Nguồn.** Bài: Deng & Hooi, "Graph Neural Network-Based Anomaly Detection in Multivariate Time Series", AAAI'21; đọc bản arXiv 2106.06947v1 (PDF, SHA-256 ở `nguon-tai.md`). Dẫn bài dạng "bài, dòng N" là dòng của file văn bản trích bằng `pdftotext -layout` (`D:\RCA-ext\work\T-018\nguon\gdn.txt`). Code: `d-ailin/GDN` revision `9853899` (T-001 mục 9). Dẫn code dạng `file:dòng`; mọi dòng dẫn được in lại bằng `scripts/kiem_dan_dong.py` (đầu ra `runs/kiem-dan-dong.txt`).

**Phạm vi.** Hồ sơ giải thích cơ chế và kiểm tính chất không cần nhãn. Hồ sơ **không** đánh giá GDN phát hiện tốt hay dở trên dataset nào (việc của P3).

## 0. Tóm tắt cho người đọc nhanh

- GDN học, từ dữ liệu bình thường, cách dự báo giá trị mỗi metric ở giây t từ 5 giây trước đó của chính nó và của vài metric "giống nó". "Giống" được học: mỗi metric có một vector embedding; đồ thị nối mỗi metric với k metric có embedding gần nhất (cosine).
- Khi chạy, metric nào bị dự báo sai nhiều hơn mức sai thường lệ của chính nó thì có điểm lệch cao. Điểm của cả hệ ở giây t là điểm lệch lớn nhất qua mọi metric, làm trơn 4 giây. Vượt ngưỡng thì báo bất thường. Ngưỡng là điểm lớn nhất từng thấy trên tập kiểm định (dữ liệu bình thường).
- Đồ thị ở đây là **đồ thị tương quan giữa các metric**, học từ dữ liệu. Nó **không** phải đồ thị gọi giữa các service. GDN không xếp hạng nguyên nhân gốc; nó cho thời điểm bất thường và metric lệch nhất.
- Code mặc định (`run.sh`) chọn ngưỡng tốt nhất **theo nhãn test** (`report='best'`), và ở mọi chế độ đều chuẩn hóa điểm test bằng trung vị/IQR **của chính tập test**. Hai chỗ này làm số của code không phải số "phát hiện trực tuyến". Mục 8 nêu cách chạy hợp lệ ở chế độ b.
- Trên RE2-TT, vướng lớn nhất là **lệch mức giữa các lượt chạy**: chuẩn hóa min-max học trên 12 phút của vài ca, cột hằng chia cho 1, nên ở ca khác nhiều metric (nhất là mem) nằm xa khoảng học. Trên dữ liệu **bình thường** giữ ngoài, mô hình học 1 ca báo động 24–31 % số tick, 5 ca khoảng 10–11 %, 10 ca khoảng 5 % (1 lượt, 1 seed); nếu chuẩn hóa điểm theo tập kiểm định (cách hợp lệ ở chế độ b) thì 94–100 % với 1–5 ca, 45 % với 10 ca. Mô hình 10 ca lại không báo động tick nào trên ca R-ca, kể cả sau mốc tiêm. Mục 9.2, 9.4.
- Code tính đúng như hồ sơ mô tả: bản numpy độc lập khớp code ở mọi dự báo (lệch ≤ 6·10⁻⁶), mọi điểm và mọi quyết định báo động trên 1436 tick. Học lại cho trọng số trùng hệt T-005; dữ liệu test không ảnh hưởng việc học. Với 1 ca học, đổi seed làm tập tick báo động đổi mạnh (Jaccard 0,18–0,58). Mục 7, 9.4.
- Các lựa chọn của task dùng trong kết quả chẩn đoán (bộ cột L\*, điền cột thiếu, chuẩn hóa điểm theo tập kiểm định) chưa có mục WHY (chờ WHY, xem `de-xuat-tai-lieu-chung.md` E1).

## 1. Bài toán và đầu vào

**Theo bài.** Đầu vào là chuỗi thời gian đa biến s(t) ∈ R^N của N cảm biến. Dữ liệu học giả định chỉ gồm dữ liệu bình thường (bài, dòng 154–169). Đầu ra là nhãn nhị phân a(t) ∈ {0, 1} cho mỗi tick test (dòng 181–186). Bài còn dùng điểm lệch từng cảm biến để khoanh cảm biến lệch (RQ4, dòng 455–457), nhưng không định nghĩa một thứ hạng nguyên nhân có đánh giá.

**Theo code.**
- Ba file trong `./data/<dataset>/`: `train.csv`, `test.csv` (cột đầu là chỉ số, các cột là metric; `test.csv` phải có cột `attack`), `list.txt` (tên metric, mỗi dòng một tên) (`main.py:44-45`, `util/net_struct.py:4-10`).
- Cột `attack` của tập học bị bỏ (`main.py:49-50`). Cột `attack` của test là nhãn, chỉ dùng ở bước chấm F1 (`main.py:156`, `evaluate.py:118-124`, `141-144`).
- `list.txt` cố định tập nút. Dữ liệu được đọc theo đúng tên trong `list.txt` (`util/preprocess.py:67-83`). Nếu test thiếu một tên, code chỉ in "not exist in data" rồi bỏ qua (`util/preprocess.py:74`), số hàng dữ liệu nhỏ hơn số nút của mô hình, và lượt chạy hỏng hoặc lệch cột. Vì vậy GDN cần **một bộ cột cố định và đủ ở mọi file**.
- Tiền xử lý mẫu của tác giả cho SWaT (`scripts/process_swat.py`): chuẩn hóa min-max học trên tập học rồi áp cho test (`scripts/process_swat.py:8-14`), lấy trung vị mỗi 10 điểm (`scripts/process_swat.py:77`), bỏ 2160 điểm đầu tập học (`scripts/process_swat.py:86`). Bài ghi lấy mẫu 10 s bằng trung vị và bỏ 2160 điểm đầu (dòng 339–345), nhưng **nhãn** của khối 10 s theo bài là nhãn xuất hiện nhiều nhất (dòng 342–343), còn script lấy max (`np.max` trong hàm `downsample` của `scripts/process_swat.py`): khối có 1/10 điểm tấn công thành 1 theo code, 0 theo bài. Script còn điền ô thiếu của test bằng trung bình của cả tập test (`scripts/process_swat.py:50`). T-018 không dùng script này (dùng ffill rồi điền 0), nên không số nào của task bị ảnh hưởng (REVIEW R1).

**Đơn vị đầu ra.** Tick thời gian (một tick = một dòng dữ liệu). Không có đầu ra mức service.

## 2. Từng bước xử lý và công thức

Ký hiệu: N metric; w = độ dài cửa sổ; d = chiều embedding; k = số láng giềng; s_i(t) là giá trị metric i ở tick t (đã chuẩn hóa min-max).

**B1. Cửa sổ trượt.** x_i(t) = [s_i(t−w), …, s_i(t−1)] ∈ R^w; đích là s_i(t) (bài Eq. 4, dòng 235–242; `datasets/TimeDataset.py:44-49`). Tập học lấy cửa sổ với bước `slide_stride`; tập test luôn bước 1 (`TimeDataset.py:44`). Vì vậy w tick đầu của mỗi file không có dự báo.

**B2. Embedding.** Mỗi metric i có v_i ∈ R^d, khởi tạo ngẫu nhiên (`models/GDN.py:95`, `119`), học cùng mô hình (bài dòng 137–143).

**B3. Học cấu trúc đồ thị.** e_ji = v_iᵀv_j / (‖v_i‖·‖v_j‖); A_ji = 1{j ∈ TopK_k({e_ki : k ∈ C_i})} (bài Eq. 2–3, dòng 194–200). Không có thông tin trước thì C_i = mọi nút trừ i (Eq. 1, dòng 188–191). Code: `GDN.py:150-157` tính cos trên **toàn bộ** nút, kể cả i; cạnh hướng j → i (`GDN.py:161-163`). Đồ thị tính từ embedding đã `detach` (`GDN.py:145`), nên không có gradient đi qua bước chọn top-k; embedding chỉ được học qua attention (B4) và lớp ra (B5).

**B4. Dự báo bằng attention.** Với S_i = N(i) ∪ {i}:
- g_i(t) = v_i ⊕ W x_i(t), W ∈ R^{d×w} (Eq. 6, dòng 268);
- π(i, j) = LeakyReLU(aᵀ(g_i ⊕ g_j)) (Eq. 7, dòng 270; độ dốc âm 0,2 ở `models/graph_layer.py:13`, `109`);
- α_ij = exp π(i, j) / Σ_{k∈S_i} exp π(i, k) (Eq. 8, dòng 272–274; `graph_layer.py:110`);
- z_i(t) = ReLU(α_ii W x_i + Σ_{j∈N(i)} α_ij W x_j) (Eq. 5, dòng 255–257).
- Code: W không có bias (`graph_layer.py:25`); a tách thành bốn vector att_i, att_j, att_em_i, att_em_j (`graph_layer.py:27-30`, `100-103`), tương đương aᵀ(g_i ⊕ g_j); bỏ vòng tự thân rồi thêm lại (`graph_layer.py:61-62`); cộng bias sau khi gộp (`graph_layer.py:73-74`); rồi **BatchNorm** và ReLU (`GDN.py:77-79`).

**B5. Lớp ra.** ŝ(t) = f_θ([v_1 ∘ z_1(t), …, v_N ∘ z_N(t)]) (Eq. 9, dòng 217–224). Code: nhân từng phần tử với embedding (`GDN.py:176`), BatchNorm + ReLU (`GDN.py:179`), Dropout 0,2 (`GDN.py:114`, `182`), rồi một lớp tuyến tính d → 1 **dùng chung cho mọi nút** (`GDN.py:183`, `OutLayer` ở `GDN.py:27-56` với `out_layer_num=1`).

**B6. Hàm mất mát và học.** L = (1/(T−w)) Σ_t ‖ŝ(t) − s(t)‖² (Eq. 10, dòng 230–234; code chia thêm cho N: `train.py:20-21`, `F.mse_loss(..., 'mean')`). Adam lr 1e-3 (`train.py:31`).

**B7. Tập kiểm định và chọn epoch.** Lấy một khối **liền** 20 % số cửa sổ học (`run.sh`: `val_ratio=0.2`), vị trí đầu khối chọn ngẫu nhiên bằng `random.randrange` (`main.py:128-148`). Sau mỗi epoch, nếu val loss nhỏ hơn mức tốt nhất thì lưu mô hình (`train.py:93-96`); 15 epoch không cải thiện thì dừng (`train.py:49`, `102-103`). Epoch được chọn **chỉ bằng val loss trên dữ liệu học**; `train()` nhận `test_dataloader` nhưng không dùng (`train.py:27-112`). R1 kiểm thực nghiệm điều này (mục 7.1).

**B8. Điểm lệch.** Err_i(t) = |s_i(t) − ŝ_i(t)| (Eq. 11, dòng 251); a_i(t) = (Err_i(t) − μ̃_i)/σ̃_i với μ̃_i, σ̃_i là trung vị và IQR "theo thời gian" (Eq. 12, dòng 259–263). Bài không nói trung vị/IQR lấy trên tập nào. Code: a_i(t) = (Err_i(t) − med_i)/(|IQR_i| + 0,01), với med_i, IQR_i tính trên **toàn bộ tập test** (`evaluate.py:48-60`; `util/data.py:75-82`). Tham số `val_res` truyền vào `get_err_scores` không được dùng (`evaluate.py:49-52`).

**B9. Gộp và làm trơn.** Bài: A(t) = max_i a_i(t) (Eq. 13, dòng 268–274), rồi trung bình trượt (SMA) không nêu độ dài (dòng 279–284). Code làm trơn **từng metric trước**, rồi mới lấy max: ã_i(t) = mean(a_i(t−3), …, a_i(t)) với t ≥ 3, ã_i(t) = 0 với t < 3 (`evaluate.py:62-65`); A(t) = max_i ã_i(t) (`evaluate.py:102-107`, `topk=1`). Max của trung bình khác trung bình của max: chỗ code khác bài.

**B10. Ngưỡng.** Bài: τ = max của điểm đã làm trơn trên tập kiểm định (dòng 286–291, 341–350). Code `report='val'`: τ = max_{i,t} ã_i^val(t), với điểm kiểm định chuẩn hóa bằng trung vị/IQR **của chính tập kiểm định** (`evaluate.py:21`, `109`); báo bất thường khi A(t) > τ (`evaluate.py:112`). Code `report='best'` (mặc định của `main.py:216` và `run.sh`): thử 400 ngưỡng theo phân vị của A(t) trên test, giữ ngưỡng cho **F1 cao nhất theo nhãn test** (`evaluate.py:129-158`; `util/data.py:28-47`).

## 3. Đồ thị dùng ở đâu (theo các vai trò ở K1 §3)

| Vai trò (K1 §3) | GDN có không | Ở đâu |
|---|---|---|
| Biểu diễn topology hoặc quan hệ triển khai | Không | Đồ thị không lấy từ kiến trúc hay trace |
| Cung cấp ngữ cảnh feature cho detector | **Có** | Dự báo metric i dùng cửa sổ của các láng giềng học được (B3–B5). Đây là chỗ duy nhất đồ thị tham gia |
| Làm chính đối tượng cần chấm bất thường | Không | Chấm từng metric, không chấm đồ thị |
| Lan truyền điểm nghi vấn | Không | Điểm không lan trên đồ thị |
| Biểu diễn giả định causal/conditional | Không (một phần) | Láng giềng là metric có embedding giống nhau, không phải quan hệ nhân quả. Bài chỉ nói "có xu hướng liên quan" (dòng 145–148) |
| Xếp hạng ứng viên nguyên nhân | Không | Không có bước xếp hạng; chỉ có metric lệch nhất ở mỗi tick |

Theo K1 §D.2, GDN thuộc mẫu C (GNN dự báo bình thường → phần dư). Theo MRP §2.3, GDN là "graph-based anomaly detection" **theo nghĩa hẹp** (đồ thị đi vào điểm bất thường), nhưng đồ thị là đồ thị tương quan học được, không phải đồ thị phụ thuộc giữa dịch vụ mà DT18 yêu cầu. Muốn dùng đồ thị gọi, phải thay bước B3 bằng tập ứng viên C_i từ kiến trúc; bài cho phép (dòng 176–181) nhưng code ở revision này không cài (mục 5, dòng 10).

## 4. Tham số mặc định

`run.sh` là cấu hình tác giả dùng trong README; `main.py` có mặc định khác. T-005, T-006 và task này dùng `run.sh` (nhánh `cpu`).

| Tham số | `run.sh` | Mặc định `main.py` | Bài (WADI / SWaT) | Ý nghĩa |
|---|---|---|---|---|
| seed | 5 (`run.sh:4`) | 0 (`main.py:209`) | — | Vị trí khối kiểm định, khởi tạo, xáo batch |
| batch | 32 (`run.sh:5`) | 128 (`main.py:201`) | — | |
| w (`slide_win`) | 5 (`run.sh:6`) | 15 (`main.py:203`) | 5 (dòng 385–386) | Độ dài cửa sổ |
| d (`dim`) | 64 (`run.sh:7`) | 64 (`main.py:204`) | 128 / 64 (dòng 382–384) | Chiều embedding và W |
| `out_layer_num` | 1 (`run.sh:8`) | 1 (`main.py:211`) | "stacked fully-connected" (dòng 220–221) | Số lớp của f_θ |
| `slide_stride` (học) | 1 (`run.sh:9`) | 5 (`main.py:205`) | — | |
| k (`topk`) | 5 (`run.sh:10`) | 20 (`main.py:215`) | 30 / 15 (dòng 383) | Số láng giềng (code tính cả chính nút, mục 5) |
| `out_layer_inter_dim` | 128 (`run.sh:11`) | 256 (`main.py:212`) | 128 / 64 "hidden layers" (dòng 383–384) | **Không dùng** khi `out_layer_num=1` (`GDN.py:33-36`) |
| `val_ratio` | 0,2 (`run.sh:12`) | 0,1 (`main.py:214`) | — | |
| `decay` | 0 (`run.sh:13`) | 0 (`main.py:213`) | — | weight decay |
| epoch tối đa | 30 (`run.sh:19`) | 100 (`main.py:202`) | 50 (dòng 381) | |
| patience | 15 (`train.py:49`) | 15 | 10 (dòng 381–382) | |
| Adam | lr 1e-3, β = (0,9; 0,999) mặc định torch (`train.py:31`) | | lr 1e-3, β = (0,9; 0,99) (dòng 380–381) | |
| `report` | `best` (`run.sh:20`) | `best` (`main.py:216`) | ngưỡng = max trên tập kiểm định (dòng 286–291) | |
| ε trong mẫu số | 0,01 (`evaluate.py:58`) | | không có | |
| làm trơn | 4 tick, gồm tick hiện tại (`evaluate.py:63-65`) | | SMA, không nêu độ dài | |
| Dropout lớp ra | 0,2 (`GDN.py:114`) | | không nêu | |

## 5. Chỗ code khác bài

| # | Bài | Code | Hệ quả |
|---|---|---|---|
| 1 | C_i loại chính nút i (Eq. 1, dòng 188–191) | TopK trên mọi nút; cos(i, i) = 1 nên i hầu như luôn nằm trong TopK, rồi vòng tự thân bị bỏ và thêm lại (`GDN.py:150-157`; `graph_layer.py:61-62`) | Mỗi nút thực chất có k − 1 láng giềng khác nó (với k = 5: 4). Đo ở mục 7.3 |
| 2 | z_i = ReLU(tổng có trọng số) (Eq. 5) | Cộng bias, BatchNorm rồi ReLU (`graph_layer.py:73-74`; `GDN.py:77-79`) | Khác kiến trúc; ảnh hưởng chưa đo |
| 3 | f_θ: các lớp kết nối đầy đủ, đầu ra N chiều (dòng 217–221); lớp ẩn 128/64 (dòng 383–384) | BatchNorm + ReLU + Dropout rồi một lớp tuyến tính d → 1 dùng chung cho mọi nút; `out_layer_inter_dim` không được dùng với `out_layer_num=1` (`GDN.py:27-56`, `176-183`) | Mô hình nhỏ hơn mô tả; mỗi nút chỉ khác nhau qua embedding |
| 4 | Trung vị/IQR "theo thời gian", không nêu tập (dòng 259–263) | Tính trên toàn bộ tập test (`evaluate.py:52`) | Điểm của tick t phụ thuộc dữ liệu sau t (mục 6, mục 8) |
| 5 | Không có ε | Mẫu số |IQR| + 0,01 (`evaluate.py:58`) | Metric có lỗi gần hằng được nhân tới 100 lần (mục 9) |
| 6 | Max qua cảm biến rồi SMA (dòng 268–284) | SMA từng metric rồi max (`evaluate.py:62-65`, `102-107`) | Thứ tự khác; với max của trung bình, một metric phải lệch liền vài tick mới cao |
| 7 | Ngưỡng = max trên tập kiểm định (dòng 286–291, 341–350) | Mặc định `report='best'`: ngưỡng tối đa F1 theo nhãn test (`main.py:216`, `run.sh:20`, `evaluate.py:141-144`) | Số mặc định của code là cận trên, không phải số phát hiện |
| 8 | Adam β2 = 0,99; tối đa 50 epoch; patience 10; k = 15 (SWaT) | β2 = 0,999; 30 epoch; patience 15; k = 5 (`train.py:31`, `49`; `run.sh`) | Cấu hình `run.sh` là cho MSL mẫu, không phải cấu hình của bảng trong bài |
| 9 | Không nói cách chọn tập kiểm định | Khối liền 20 % cửa sổ học, vị trí ngẫu nhiên theo seed (`main.py:128-148`) | Ngưỡng phụ thuộc seed; tập kiểm định cùng giai đoạn với tập học |
| 11 | Nhãn khối 10 s là nhãn phổ biến nhất (dòng 342–343) | `scripts/process_swat.py` lấy max nhãn trong khối | Khi tái lập bảng bài, P/R/F1 có thể đổi ở biên sự cố và sự cố ngắn (REVIEW R1) |
| 10 | Có thể đưa thông tin trước vào C_i (dòng 176–184) | Không cài: đồ thị đầy đủ `get_fc_graph_struc` chỉ dùng để dựng chỉ số batch; forward luôn tính TopK trên mọi nút; `get_prior_graph_struc` không được gọi (`main.py:52-58`; `GDN.py:134-166`; `util/net_struct.py:30`) | Muốn ràng buộc láng giềng theo đồ thị gọi phải sửa code |

## 6. Giả định và điều kiện thất bại do tác giả nêu

- Tập học chỉ có dữ liệu bình thường (dòng 167–169). Sai khi đoạn "bình thường" có sự cố hoặc khởi động; tác giả bỏ 2160 điểm đầu vì hệ mất 5–6 giờ mới ổn định (dòng 343–345).
- Bất thường có thể chỉ ảnh hưởng một nhóm nhỏ cảm biến, nên dùng max (dòng 268–270).
- Thay đổi đột ngột thường bị dự báo sai cả khi bình thường, nên phải làm trơn (dòng 279–284).
- Ngưỡng max trên tập kiểm định được chọn "để tránh thêm siêu tham số"; tác giả nêu EVT là cách khác (dòng 286–291).
- Hạn chế tự nêu: hướng tiếp theo là kiến trúc khác và **học trực tuyến** để thực tế hơn (dòng 466–470). Bài chỉ thử trên hai hệ xử lý nước (SWaT, WADI), dữ liệu cảm biến lấy mẫu 10 giây.
- Tác giả **không** nêu: dữ liệu microservice, cột thay đổi giữa các lần chạy, metric thiếu, độ nhạy theo w hay k.

## 7. Ví dụ tính tay (một bước chấm điểm trên một ca đã thấy)

### 7.1 Mô hình dùng để tính: lặp lại T-005 (R1)

- Dữ liệu: dựng lại bằng script độc lập (`scripts/chuan_bi_gdn.py`), **trùng từng byte** với `train.csv`, `test.csv`, `list.txt` của T-005 (`runs/b3-chuan-bi.json`, SHA-256). Học trên 720 dòng trước mốc của 5 ca, 333 cột; test là toàn ca `re2tt_ts-route-service_socket_1` (1441 dòng, 1436 cửa sổ). Ca chọn theo quy tắc R-ca của SPEC (T-005 chọn theo kích thước file).
- Học theo `run.sh` (seed 5, luồng mặc định 12), nhưng truyền `test_dataloader=None` vào `train()`.
- Kết quả lặp (`runs/r1-re2tt5-seed5.log`, LOG): loss epoch 0–28 trùng từng chữ số với T-005 (`results/T-005/runs/do-gdn_hoc-full-lan1.log`). Lượt bị giới hạn 1 giờ dừng ở epoch 29/30 vì máy bận; mô hình tốt nhất đã lưu có **SHA-256 nội dung tensor trùng hệt** mô hình của T-005. Vì T-005 truyền loader test thật còn R1 truyền `None` mà mô hình như nhau, **dữ liệu test không ảnh hưởng việc học và chọn epoch** (đường G5 kiểm bằng thực nghiệm). Phần chấm chạy lại bằng `--chi-cham` (`runs/r1s-re2tt5-cham.log`).

### 7.2 Tính lại độc lập và đối chiếu với code

`scripts/tinh_tay_gdn.py` cài lại B1–B10 bằng numpy theo công thức ở đầu file script; không import module nào của GDN, torch chỉ để nạp trọng số. Kết quả so với đầu ra của code chính thức (`runs/r1s-re2tt5-cham-tinh-tay.json`):

| So sánh | Kết quả | Dung sai (SPEC) |
|---|---|---|
| Dự báo ŝ, 1436 tick × 333 cột test | lệch tối đa 6,0·10⁻⁶ | ≤ 1·10⁻⁵ |
| Dự báo ŝ, 719 cửa sổ kiểm định | lệch tối đa 4,9·10⁻⁷ | ≤ 1·10⁻⁵ |
| Điểm đã làm trơn ã_i(t), test | lệch tối đa 3,3·10⁻⁴; 0 ô vượt dung sai | 1·10⁻³ + 1·10⁻⁵·|a| |
| Ngưỡng τ | 63,832934 (tay) / 63,832916 (code) | — |
| Cột đứng đầu A(t) | trùng ở 1436/1436 tick | — |
| Quyết định báo động | trùng ở 1436/1436 tick (88 báo động) | — |

Lệch còn lại do code tính trong float32, bản tay trong float64. Ba phép kiểm thêm, cùng script:
- **Top-k gồm chính nút:** 333/333 nút có chính nó trong TopK; mỗi nút có đúng 4 láng giềng khác nó (mục 5 dòng 1).
- **Hoán vị nút** (hoán vị cùng lúc hàng embedding và cột đầu vào): dự báo đổi chỗ tương ứng, lệch tối đa 7,1·10⁻¹⁵. Mô hình đã học không phụ thuộc thứ tự cột.
- **Đảo thứ tự cột trong CSV** (giữ `list.txt`), chấm bằng code chính thức: `test_scores`, `normal_scores`, `test_pred`, `val_pred` trùng SHA-256 (`runs/r1b-daocot-cham.log`, LOG).

### 7.3 Một bước chấm điểm, tính bằng số

Hai tick chọn theo quy tắc R-tick của SPEC (`runs/r1s-re2tt5-cham-tinh-tay.json`, mục `giai_thich`).

**t\* = tick 12 (dòng 17 của file), tick có A(t) lớn nhất.** Cột đứng đầu: `ts-consign-service_diskio`.
1. Cửa sổ đầu vào (đã chuẩn hóa) của chính nó: [0,426; 0,426; 0,426; 0,366; 0,366] — nằm trong khoảng học [0, 1].
2. Láng giềng (B3): TopK theo cos = {chính nó 1,0; `ts-order-mongo_socket` 0,358; `ts-route-service_diskio` 0,349; `ts-price-service_socket` 0,348; `ts-order-mongo_diskio` 0,346}.
3. Attention (B4): α = 1,00 vào `ts-route-service_diskio`, ≈ 0 cho mọi láng giềng còn lại và cho chính nó. Lý do: `ts-route-service_diskio` vừa nhảy từ 0,48 lên **53,84** lần khoảng học ở dòng 13 (khoảng học là [0, 1]); h_j = W x_j lớn nên π(i, j) lấn át, softmax dồn hết vào nó.
4. Dự báo ŝ = 26,28; thực tế s = 0,366; Err = 25,91.
5. Chuẩn hóa (code): trung vị lỗi của cột trên cả file test 0,149, IQR 0,104 → a(t−3..t) = [492,6; 560,8; 418,0; 225,5]; ã = 424,2.
6. A(t\*) = 424,2 > τ = 63,8 → **báo động**. Theo biến thể b (trung vị 0,128, IQR 0,116 của tập kiểm định): ã = 385,8, vẫn báo động.

Cơ chế: một metric của láng giềng ra xa khoảng học làm hỏng dự báo của metric khác. Cột bị "báo" (consign diskio) không lệch; cột lệch thật là route diskio. Attention chỉ ra đúng nguồn (bài nói attention giúp giải thích, dòng 437–451).

**t0 = tick 100 (dòng 105).** Cột đứng đầu `ts-assurance-mongo_cpu`: α = 0,62 cho chính nó, còn lại 0,03–0,18; dự báo 0,535, thực 0,411, Err = 0,123; trung vị lỗi 0,013, IQR 0,020 → ã = 8,54 < τ = 63,8 → không báo động. Lỗi tuyệt đối chỉ 0,12 khoảng học nhưng điểm đã là 8,5 vì IQR của cột nhỏ: thang điểm của từng cột do IQR lỗi của chính nó quyết định.

### 7.4 Giải thích kết quả bằng nhãn (chỉ sau khi đã có kết quả)

Nhãn của ca: service gốc `ts-route-service` (lỗi socket), mốc tiêm ở dòng 720, tức tick 715 (`runs/tai-moc-tiem.json`). Số lấy từ `runs/b5-giai-thich-ca.json`.

- t\* (tick 12) nằm **703 s trước mốc tiêm**. Đây là báo động sai theo giả định "trước mốc là bình thường". Nguyên nhân là `ts-route-service_diskio` ở đầu file nằm xa khoảng học (lệch mức giữa các lượt chạy, mục 9.2), không phải sự cố. Việc metric này thuộc đúng service gốc là trùng hợp có thể có, nhưng xảy ra 12 phút trước khi tiêm nên không phải triệu chứng của lỗi được tiêm.
- 88 tick báo động: 47 trước mốc, 41 từ mốc. Báo động đầu tiên sau mốc ở 65 s. Ở 41 tick sau mốc, cột đứng đầu **không lần nào** thuộc service gốc; nhiều nhất là `ts-seat-service_error` (28 tick) và `ts-ticketinfo-service_mem` (13). Tại tick có A lớn nhất sau mốc, cột tốt nhất của service gốc đứng thứ 43.
- Trung vị A(t) trước và sau mốc gần bằng nhau (7,7 so với 8,4).
- Biến thể b báo động 712/715 tick trước mốc và 721/721 tick sau: không phân biệt được gì, vì cả file nằm xa khoảng học.

Cách đọc đúng mức: trên ca này, mô hình học trên 5 ca không tách được trước và sau mốc tiêm; tín hiệu sau mốc nó bắt được nằm ở service khác (lỗi của seat-service, có thể là triệu chứng lan, **chưa kiểm**). Nguyên nhân khả thi khác (Q-33): (a) lỗi socket ở route-service có thể không hiện mạnh ở metric (đoạn sau mốc của các phương pháp khác chưa xem ở task này); (b) một ca không phải mẫu hình (QT15); (c) cấu hình 333 cột của T-005 và w = 5 có thể không phải cấu hình tốt cho dữ liệu này. Hồ sơ không kết luận GDN tốt hay dở trên RE2-TT (việc của P3).

## 8. Đường nhãn hoặc dữ liệu test có thể lọt vào, và cách chạy hợp lệ ở chế độ b

### 8.1 Các đường

| # | Ở đâu | Cái gì lọt vào | Mức | Cách chặn |
|---|---|---|---|---|
| G1 | `report='best'`, mặc định của `main.py:216` và `run.sh:20`; `evaluate.py:129-158`; `util/data.py:28-47` | **Nhãn test**: thử 400 ngưỡng theo phân vị của A(t) trên test, giữ ngưỡng có F1 cao nhất theo nhãn | Nhãn | Dùng `report='val'`. Số F1 của `report='best'` chỉ là cận trên (T-006 mục 9 ghi F1 0,878 trên MSL theo cách này) |
| G2 | `evaluate.py:52` (cả `report='val'` và `'best'`) | **Dữ liệu test tương lai**: trung vị và IQR lỗi của từng metric tính trên toàn tập test. Điểm ở tick t phụ thuộc mọi tick sau t, kể cả đoạn sự cố | Dữ liệu tương lai, không phải nhãn | Lấy trung vị/IQR từ tập kiểm định (R-chuẩn-hóa-b). T-001 L8 đã nêu |
| G3 | `evaluate.py:21`, `109` | Ngưỡng τ tính từ điểm kiểm định chuẩn hóa bằng **chính** trung vị/IQR của tập kiểm định, còn điểm test chuẩn hóa bằng trung vị/IQR của tập test. Hai thang khác nhau | Không phải nhãn; làm ngưỡng phụ thuộc thành phần của file test | R-chuẩn-hóa-b đưa cả hai về thang của tập kiểm định |
| G4 | Biên file RCAEval | Mốc tiêm nằm đúng giữa file: 30/30 ca dev, 720 dòng trước và 721 dòng từ mốc (`runs/tai-moc-tiem.json`; T-002). Với G2, nửa sau file luôn là đoạn sự cố, nên trung vị/IQR của file chứa thông tin về vị trí sự cố | Mốc tiêm (nhãn thời gian) lộ gián tiếp | Chấm theo luồng, chuẩn hóa cố định từ tập kiểm định; không cắt cửa sổ quanh mốc tiêm |
| G5 | Chọn epoch: `train.py:89-103` | Không có: epoch chọn theo val loss của dữ liệu học; `test_dataloader` truyền vào nhưng không dùng | Không | R1 kiểm thực nghiệm (mục 7.1) |
| G6 | Bộ chuẩn hóa min-max | Học trên tập học (`scripts/process_swat.py:8-14`; T-005 `chuan_bi_dau_vao.py` cũng vậy) | Không | — |
| G7 | Bộ cột `list.txt` của T-005 | Giao 5 ca học **và ca test** (`results/T-005/scripts/chuan_bi_dau_vao.py:122`). Dùng thông tin của ca test (siêu dữ liệu, không phải nhãn) | Siêu dữ liệu test | Chế độ b: chốt bộ cột chỉ từ dữ liệu học; mục 9.1 |
| G8 | Lấy dữ liệu học | Đoạn "bình thường" của ca học cắt bằng mốc tiêm của chính các ca đó (T-005, task này) | **Nhãn dev dùng để học** | Hợp lệ nếu G1 ghi rõ là nhãn dùng để học (MRP §4); không bao giờ dùng mốc tiêm của ca test |
| G10 | Script mẫu `scripts/process_swat.py:50` | Ô thiếu của test điền bằng trung bình cả tập test: giá trị ở quá khứ có thể dùng dữ liệu tương lai | Dữ liệu tương lai (nếu test có ô thiếu) | Điền bằng thống kê tập học hoặc ffill; T-018 dùng ffill rồi 0 (REVIEW R1) |
| G9 | Tập kiểm định | Khối liền nằm giữa dữ liệu học, cửa sổ ở hai mép khối chồng 4/5 điểm với cửa sổ học (bước 1). Val loss và τ hơi lạc quan | Không phải nhãn | Ghi nhận; ảnh hưởng đo gián tiếp ở phép kiểm "bình thường vs bình thường" |

### 8.2 Cách chạy hợp lệ ở chế độ b (không dùng mốc tiêm của ca được chấm)

Đề xuất, chờ G1 và mục WHY (chờ WHY, xem `de-xuat-tai-lieu-chung.md`):
1. **Bộ cột** chốt từ dữ liệu học trước khi thấy ca test. Ca test thiếu cột thì điền trung vị tập học và ghi số cột đã điền; cột thừa bỏ (mục 9.1).
2. **Dữ liệu học** là dữ liệu bình thường không thuộc ca được chấm: đoạn trước mốc tiêm của các ca dev (nhãn dev dùng để học, G8), hoặc bản ghi bình thường riêng nếu dataset có.
3. **Chuẩn hóa đầu vào** học trên tập học. Cột hằng trong tập học phải xử lý trước (mục 9.2), không để chia cho 1.
4. **Học** theo `run.sh`, seed cố định; epoch chọn theo val loss (code đã đúng).
5. **Chuẩn hóa điểm lệch** bằng trung vị/IQR của tập kiểm định, giữ cố định (R-chuẩn-hóa-b). Đây là thay đổi duy nhất so với code ở phần chấm.
6. **Ngưỡng** τ = max điểm đã làm trơn trên tập kiểm định (`report='val'`), giữ cố định.
7. **Chấm theo luồng** trên toàn file test, tick nào cũng chỉ dùng 5 tick trước nó và 3 điểm lệch trước nó. Không cắt cửa sổ quanh mốc tiêm. 8 tick đầu file không thể báo động (5 tick không có dự báo, 3 tick làm trơn bằng 0; `TimeDataset.py:44`, `evaluate.py:62-65`).
8. Mốc tiêm của ca test chỉ dùng ở bước chấm (P3).

GDN không học lại khi chạy (bài nêu học trực tuyến là việc tương lai, dòng 466–470). Hệ chạy càng lâu sau lúc học, ngưỡng cố định càng dễ lệch.

## 9. Yêu cầu đầu vào khi chạy trên dataset khác

### 9.1 Bộ cột cố định

GDN có một nút cho mỗi tên trong `list.txt`; embedding v_i gắn với chỉ số nút (mục 1). Mô hình học xong không nhận thêm hay bớt cột.

**Trên RE2-TT (30 ca dev; `cot-re2tt/tom-tat.json`, `cot-re2tt/cot-khong-du-30-ca.csv`):**
- 340–375 cột thô mỗi ca; sau làm sạch như T-005 (bỏ `*_latency-50`, đổi `*_latency-90`) còn 318–347.
- Giao 30 ca (L\*) có 317 cột; hợp có 354; 37 cột không có ở đủ 30 ca.
- 37 cột đó gồm: 23 cột `*_error` (có ở 2–20 ca), 12 cột latency/workload của 6 service (vắng ở đúng 4 ca, cả 4 có gốc `ts-order-service`), 2 cột `istio-init` (có ở 1 ca).
- Chỉ 2 cột error có ở đủ 30 ca (`ts-admin-travel-service_error`, `ts-ui-dashboard_error`); cả hai hằng ở đoạn trước mốc trong 21–28/30 ca (`cot-re2tt/cot.csv`).

**Ba cách xử lý và hệ quả:**

| Cách | Làm gì | Hệ quả |
|---|---|---|
| A. Giao theo ca học và ca test (T-005) | `list.txt` = giao các ca học và ca được chấm | Bộ cột phụ thuộc ca được chấm (G7); mỗi ca test cần một mô hình riêng; không hợp lệ ở chế độ b |
| B. Giao cố định trên dữ liệu dev (L\*) | Chốt một lần từ siêu dữ liệu dev; ca thiếu cột thì điền | Một mô hình cho mọi ca. Mất gần hết cột error (23/25 cột error không vào L\*; `cot-re2tt/loai.csv`), nên GDN gần như không thấy tín hiệu lỗi; điều này quan trọng với lỗi mã nguồn (MRP §4 tiêu chí 6). Ca test có thể thiếu cột của L\* |
| C. Hợp cố định, điền giá trị khi vắng | Chốt hợp 354 cột; vắng thì điền 0 hoặc trung vị | Cột vắng ở ca học thành cột hằng (mục 9.2). Cột error vắng có nghĩa "không có lỗi", điền 0 là đúng nghĩa, nhưng việc có/vắng cột tương quan với service gốc (`dinh-chinh-task-cu.md` D1) |

Đề xuất (chờ WHY, xem `de-xuat-tai-lieu-chung.md`): cách B cho bộ cột trạng thái (cpu, mem, diskio, socket, workload, latency), và xử lý riêng cột error theo cách C với 0 = không có lỗi. Chưa kiểm cách này làm đổi kết quả thế nào.

### 9.2 Cột hằng trong tập học, và lệch mức giữa các lượt chạy

**Cơ chế.** Đầu vào được chuẩn hóa min-max theo tập học (như `scripts/process_swat.py:8-14`). Cột hằng trong tập học có khoảng 0; T-005 và `MinMaxScaler` thay khoảng 0 bằng 1, nên ở dữ liệu mới cột đó mang nguyên đơn vị thô (byte bộ nhớ, số kết nối). Rộng hơn: cột có khoảng học rất hẹp (bộ nhớ gần như không đổi trong 12 phút) thì một chênh nhỏ theo đơn vị thô ở lượt chạy khác cũng thành hàng nghìn lần khoảng học.

**Đo trên dữ liệu (không cần mô hình;** `runs/b3-chuan-bi.json`, `runs/b6-lech-phan-bo.json`):

| Tập học (bộ cột L\*) | Cột hằng trong tập học | Ô của 19 đoạn giữ ngoài nằm ngoài [−1, 2] | Riêng cột mem | Giá trị tuyệt đối lớn nhất |
|---|---|---|---|---|
| 1 ca (720 dòng) | 39 | 23,1 % | 89,1 % | 6,0·10^8 |
| 5 ca (3600 dòng) | 27 | 4,9 % | 14,2 % | 7718 |
| 10 ca (7200 dòng) | 16 | 0,6 % | 1,1 % | 7332 |

Khoảng [−1, 2] nghĩa là lệch không quá một lần khoảng học về mỗi phía. Cùng chiều với số ca học: mức của metric (nhất là mem, latency) khác nhau giữa các lượt chạy hệ thống, mà 12 phút một ca không phủ được.

**Hệ quả trên điểm GDN** (mô hình học trên 1 ca, `runs/b6b7-phan-tich.json`, lượt `l1-lstar-n1-seed5`): trên 19 đoạn **bình thường** giữ ngoài (3,77 giờ), cách chuẩn hóa của code báo động ở 23,6 % số tick (143 đợt, khoảng 38 đợt mỗi giờ, cả 19 đoạn); biến thể b báo động ở 99,6 % số tick; A(t) lớn nhất tới khoảng 10^11. Bỏ các cột hằng trong tập học khỏi phép lấy max (chẩn đoán) **không** đổi kết quả (99,6 %): cột hằng làm đầu vào của láng giềng phình to, nên dự báo của các cột khác cũng hỏng; và cột không hằng nhưng có khoảng hẹp cũng lệch. Vì sao cách của code ít báo động hơn: nó chuẩn hóa theo chính đoạn được chấm (G2), nên lệch mức kéo dài cả đoạn bị "hấp thụ" vào trung vị/IQR của đoạn. Đó không phải ưu điểm: cũng chính cơ chế đó hấp thụ một sự cố kéo dài.

**Nguyên nhân khả thi khác (Q-33):** (a) đoạn trước mốc tiêm không thật sự bình thường (khởi động, tải đổi), (b) mô hình học quá khớp với 1 ca (val loss 0,026 trên chính ca học), (c) w = 5 quá ngắn so với nhịp cập nhật (mục 9.3). (a) không kiểm được vì không có nhãn "bình thường" độc lập (T-002 mục 5). (b) và lệch mức chỉ tách được một phần: R1 học trên 5 ca vẫn báo động 11,2 % tick bình thường giữ ngoài (93,7 % với biến thể b), nên quá khớp một ca không giải thích hết; nhưng so sánh này lẫn khác biệt bộ cột (mục 9.4). (c) **chưa kiểm** (độ nhạy theo w thuộc P3).

Đề xuất (chờ WHY, xem `de-xuat-tai-lieu-chung.md`; **chưa kiểm**): chuẩn hóa đầu vào bằng thống kê bền (trung vị/IQR) học trên nhiều lượt chạy, hoặc chuẩn hóa theo từng lượt bằng đoạn đầu của chính luồng đang chạy (cần một đoạn khởi động không chấm). Cả hai thay đổi phần tiền xử lý, không đổi lõi GDN. Cách thứ hai có rủi ro riêng với RCAEval: file luôn có 12 phút trước mốc tiêm (G4), nên "đoạn đầu luồng là bình thường" đúng nhờ cách cắt file, tức gián tiếp dùng mốc tiêm; chỉ hợp lệ nếu độ dài đoạn khởi động chốt trước và ngắn hơn hẳn 12 phút, và phải ghi rõ giả định này.

### 9.3 Nhịp cập nhật thật của metric và độ dài cửa sổ w

RE2-TT có một dòng mỗi giây, bước thời gian luôn đúng 1 s (30/30 ca, `cot-re2tt/tom-tat.json`). Nhưng giá trị không đổi mỗi giây. Đo trên đoạn trước mốc của 30 ca (`cot-re2tt/loai.csv`; trung vị qua cột và ca):

| Loại | Số cột trong L\* | Tỷ lệ bước 1 s có đổi giá trị | Độ dài đoạn giá trị lặp (s) |
|---|---|---|---|
| cpu | 68 | 0,26 | 1 (xen các đoạn phẳng dài, ví dụ 16 s liền ở `ts-order-service_cpu`) |
| diskio | 67 | 0,25 | 1 (như cpu) |
| latency | 22 | 0,15 | 5 |
| workload | 22 | 0,14 | 6,5 |
| mem | 68 | 0,04 | 18 |
| socket | 68 | 0,01 | 36,75 |
| error | 2 | 0 | 720 (hằng) |

170/317 cột của L\* có đoạn lặp trung vị từ 5 s trở lên. Với w = 5, phần lớn cửa sổ của các cột này chỉ chứa một hoặc hai giá trị khác nhau. Hệ quả (lý luận, **chưa kiểm** bằng thực nghiệm đổi w): mô hình dễ học "lặp lại giá trị cuối"; lỗi dự báo tập trung ở các tick giá trị nhảy, và các tick nhảy là chuyện bình thường của cách thu dữ liệu, không phải bất thường. Làm trơn 4 tick (B9) chỉ giảm một phần. Bài lấy mẫu SWaT/WADI 10 s bằng trung vị (dòng 339–342), tức mỗi tick đã là một giá trị mới. Cách tương ứng cho RE2-TT là lấy mẫu lại theo nhịp thật (5–15 s) trước khi chạy GDN; khi đó 720 dòng bình thường mỗi ca chỉ còn 48–144 tick. Lựa chọn này thuộc P3 (chờ WHY).

**Lệch thời gian giữa các cột (E5).** Không có chuẩn để đo lệch đồng hồ giữa nguồn metric container và nguồn latency/workload; **chưa kiểm**, vì dữ liệu chỉ có một cột `time` chung đã căn sẵn. Nếu latency trễ hơn cpu vài giây, cửa sổ 5 s có thể không chứa nguyên nhân của giá trị cần dự báo, làm dự báo chéo cột kém hơn; không làm hỏng việc chạy. Ô thiếu ở đầu file: trung vị 0 ở mọi loại (`cot-re2tt/loai.csv`), tổng 67 000 ô thiếu trên 30 ca (`cot-re2tt/tom-tat.json`), được ffill rồi điền 0 (E11).

### 9.4 Cần bao nhiêu dữ liệu bình thường

**Bài:** SWaT 47 515 tick, WADI 118 795 tick học, mỗi tick 10 s (bài dòng 279–283, 339–342), tức khoảng 5,5 và 13,7 ngày bình thường, 51 và 127 cột. **RE2-TT:** 720 tick mỗi ca (12 phút), 317 cột (L\*). Gộp cả 30 ca dev được tối đa 21 600 tick (6 giờ), nhưng là 30 lượt chạy rời, không liên tục.

**Đo trong task** (19 đoạn bình thường giữ ngoài, 3,77 giờ; `runs/b6b7-phan-tich.json`):

| Mô hình | Tập học | τ | Tick báo động (cách code) | Đợt báo động / giờ | Đoạn có báo động | Tick báo động (biến thể b) |
|---|---|---|---|---|---|---|
| l1 | 1 ca, L\*, seed 5 | 39,70 | 23,6 % | 37,9 | 19/19 | 99,6 % |
| l2 | 1 ca, L\*, seed 1 | 59,17 | 24,5 % | 53,0 | 19/19 | 99,6 % |
| l3 | 1 ca, L\*, seed 2 | 36,79 | 30,7 % | 53,0 | 19/19 | 99,6 % |
| l4 | 1 ca, L\*, seed 5, `list.txt` hoán vị | 37,45 | 25,0 % | 53,3 | 18/19 | 99,6 % |
| l5 | 5 ca, L\*, seed 5 | 48,32 | 10,8 % | 13,3 | 18/19 | 99,6 % |
| l6 | 5 ca, L\*, seed 1 | 55,08 | 10,3 % | 12,5 | 17/19 | 99,6 % |
| R1 | 5 ca, 333 cột (T-005), seed 5 | 63,83 | 11,2 % | 16,2 | 18/19 | 93,7 % |
| l7 | 10 ca, L\*, seed 5 | 49,53 | 4,95 % | 5,0 | 9/19 | 45,2 % |

Trên dữ liệu bình thường, mô hình học 1 hoặc 5 ca báo động ở hơn một phần mười số tick; học 10 ca còn 4,95 % (5 đợt mỗi giờ, 9/19 đoạn). Với biến thể b, 10 ca vẫn báo động 45 % số tick. Nhiều ca học hơn thì ít báo động hơn, cùng chiều với chẩn đoán lệch mức ở mục 9.2 (ô ngoài khoảng học: 23 % → 4,9 % → 0,6 % khi 1 → 5 → 10 ca). **Seed và thứ tự cột** (cùng file; so A(t) và tập tick báo động trên ca R-ca giữa các lượt 1 ca):
- Ba seed (5, 1, 2): τ từ 36,8 đến 59,2; Jaccard của tập tick báo động 0,18–0,58; tương quan hạng (Spearman) của A(t) 0,11–0,62. Tức với 1 ca học, **tick nào bị báo động phụ thuộc mạnh vào seed**.
- Hoán vị `list.txt`, giữ seed 5: Jaccard 0,87, Spearman 0,61. Thứ tự cột khi học đổi kết quả ít hơn đổi seed, vì seed giữ nguyên vị trí khối kiểm định và thứ tự xáo batch; chỉ khởi tạo gắn với chỉ số nút là đổi.
- Mô hình đã học thì không phụ thuộc thứ tự cột (mục 7.2). Hai seed ở cỡ 5 ca (l5 seed 5, l6 seed 1): τ 48,3 và 55,1; báo động sai trên đoạn giữ ngoài 10,8 % và 10,3 %; trên R-ca Jaccard 0,62, Pearson A 0,98, Spearman 0,45. Nhiều dữ liệu học hơn thì ít phụ thuộc seed hơn, nhưng chỉ có hai seed nên chưa đo được khoảng dao động.

So trên cùng bộ cột L\* (l1 so với l5), học 5 ca giảm tỷ lệ tick báo động sai từ 23,6 % xuống 10,8 %; R1 (bộ 333 cột của T-005, đoạn giữ ngoài phải điền 0–16 cột, `runs/b3-chuan-bi.json`) cho mức tương tự (11,2 %). Biến thể b không giảm (99,6 % ở cả 1 và 5 ca): so với IQR lỗi trên tập kiểm định, lỗi ở ca khác lớn hơn nhiều bậc.

**Kết luận cho câu "cần bao nhiêu":** 12 phút của một lượt chạy không đủ; 5 lượt (1 giờ) vẫn báo động sai khoảng 10 % số tick; 10 lượt (2 giờ) giảm còn khoảng 5 % (1 lượt, 1 seed), cùng chiều với chẩn đoán lệch mức (mục 9.2). Chưa cấu hình nào đạt mức dùng được khi chạy liên tục (5 đợt báo động sai mỗi giờ). Chỉ một seed ở cỡ 10 ca. Một quan sát ngược chiều cần ghi (dùng nhãn sau khi có kết quả): mô hình 10 ca **không báo động tick nào** trên ca R-ca, kể cả 721 s sau mốc tiêm (A lớn nhất 27,9 < τ = 49,5; `runs/l7-lstar-n10-seed5.log`). Giảm báo động sai có thể đi kèm mất khả năng phát hiện; đo đánh đổi này là việc của P3 (một ca không phải mẫu hình, QT15). Yếu tố quyết định không chỉ là số tick mà là **số lượt chạy khác nhau** (độ đa dạng mức). Nếu dataset có bản ghi bình thường liên tục nhiều giờ (như SWaT/WADI) thì yêu cầu này dễ đạt hơn.

### 9.5 Dataset nào chạy được GDN

Điều kiện rút từ mục 9.1–9.4: (1) có metric dạng chuỗi thời gian; (2) bộ cột cố định được giữa các file (hoặc chốt được từ dữ liệu học); (3) có dữ liệu bình thường **không thuộc ca được chấm**, đủ nhiều lượt chạy để phủ mức của metric; (4) biết đoạn nào là bình thường mà không cần mốc tiêm của ca được chấm. Bảng dưới chỉ đọc từ thẻ dataset của T-002, T-008–T-012 và `results/T-003/bang-tieu-chi.md`; **không chạy GDN trên dataset nào ngoài 30 ca dev RE2-TT** (giới hạn của task, MRP §4).

| Dataset | (1) Metric | (2) Bộ cột | (3) Bình thường | Kết luận cho GDN | Nguồn |
|---|---|---|---|---|---|
| RCAEval RE2-TT | Có, 1 dòng/s; nhịp thật 1–37 s | Khác nhau giữa ca; giao 317 / hợp 354 ở 30 ca dev | 12 phút trước mốc mỗi ca; không có bản ghi bình thường riêng | **Chạy được** với bộ cột cố định và học trên đoạn trước mốc của nhiều ca dev; 1 ca không đủ (9.2). Phải xử lý lệch mức và cột hằng | mục 9.1–9.4; `results/T-002/the-rcaeval.md` |
| RCAEval RE2-OB, RE2-SS, RE3 | Có (T-002: 72 cột OB mẫu, 316 cột RE3-TT mẫu) | chua_kiem: chỉ đọc 1 ca mỗi bộ | 12–15 phút trước mốc mỗi ca | Như RE2-TT, cùng giới hạn; RE2-SS mẫu không có trace nhưng GDN không cần trace | `results/T-002/the-rcaeval.md` mục 5 |
| Nezha OB/TT | Có metric tài nguyên | chua_kiem | Thẻ ghi metric của `construct_data` trùng file với dữ liệu lỗi; cửa sổ bình thường chặt không đủ chia tham chiếu/đối chứng | **Chưa chạy được sạch**: không có đoạn bình thường đáng tin để học | `results/T-008/the-dataset.md:22, 54-61` |
| Eadro TT/SN | Có metric thật | chua_kiem | Có phiên không lỗi riêng (SN 3, TT 2 có nhãn); độ sạch tải chưa bảo đảm | **Ứng viên cần kiểm**: theo thẻ có phiên bình thường riêng, không phải cắt bằng mốc tiêm; độ dài phiên, bộ cột và độ sạch chưa kiểm, nên chưa so được với bộ khác | `results/T-009/the-dataset.md:20, 91-93` |
| DeepTraLog TT | **Không** có metric tài nguyên riêng | — | 10 ZIP trace bình thường | **Không chạy được** nguyên dạng; phải tự dựng chuỗi metric từ span (thêm lựa chọn chưa có WHY) | `results/T-010/the-dataset.md:18, 116-122` |
| LEMMA-RCA (mẫu) | Có KPI | chua_kiem | Mốc bình thường chưa xác minh; Cloud có 24 giờ trước lỗi nhưng không có nhãn khỏe | **Chưa đủ căn cứ**: không xác định được đoạn bình thường | `results/T-011/the-dataset.md:22, 37-41, 76, 89` |
| FSE fault-propagation (T-012) | Có | chua_kiem | Khoảng 240 s trước tiêm mỗi ca | Rất ngắn; giống RE2-TT nhưng ít hơn 3 lần | `results/T-012/the-dataset.md:22, 46-48` |
| AnoMod | Có | chua_kiem | Một capture bình thường mỗi hệ | Có thể học trên capture bình thường; ít lượt chạy nên lệch mức như 9.2 là rủi ro (chua_kiem) | `results/T-012/the-dataset.md:92, 105-107` |
| OpenRCA Bank (bảo toàn) | Theo nguồn có metric | Không được xem trước G3 | Không được xem trước G3 | Không kết luận trước G3 (WHY-13) | WHY-13 |

Kết luận ngắn: GDN chỉ "chạy được" theo nghĩa phép kiểm không cần nhãn trên RE2-TT; còn phát hiện có tốt không là việc của P3. Dataset có **bản ghi bình thường riêng, nhiều lượt** hợp với GDN hơn (Eadro có thể thuộc loại này theo thẻ, chưa kiểm) dataset chỉ có vài phút trước mốc tiêm mỗi ca.
