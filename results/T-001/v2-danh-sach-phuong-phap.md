# T-001 — Danh sách phương pháp cho P1 (bản 2, đề xuất chờ Minh chốt)

Ngày: 02/10/2026. Người làm: Claude, phiên 2 (làm lại toàn bộ theo yêu cầu của Minh). Bản phiên 1 giữ ở `v1-danh-sach-phuong-phap.md`.
Chưa chạy phương pháp nào, chưa dựng môi trường, không tải dữ liệu (SPEC "Không làm").

## 0. Cách đọc

- **Đã kiểm code**: đã đọc code ở revision ghi ở mục 9. Dẫn dạng `repo:file:dòng`.
- **Theo bài**: đã đọc văn bản bài trên arXiv HTML (tải bằng curl, tìm bằng grep). Chưa đối chiếu bản PDF in. Dẫn dạng "bài X, văn bản dòng N" (dòng của file text trích từ HTML, lưu ở scratchpad, không ở repo).
- **Theo K1**: lấy từ `docs/knowledge/K1-phuong-phap-rca.md`; K1 tự ghi là chưa kiểm lại.
- **Theo T-002**: lấy từ `results/T-002/the-rcaeval.md`. T-002 **chưa phản biện**; chỉ dùng để ghi điều kiện, không dùng để chọn dataset.
- **Chưa kiểm**: không có nguồn trong phiên này.
- Viết tắt repo: `RE` = RCAEval; `BR` = BARO gốc; `SR` = Simple-RCA; `EA` = Eadro; `MR` = MicroRCA; `MK` = MicroRank gốc; `TR` = TraceRCA gốc; `DT` = DeepTraLog; `GD` = GDN. Revision ở mục 9.

### Khác gì so với bản 1

Bản 1 dựa một phần vào công cụ tóm tắt web và grep. Bản 2 đọc lại code gốc của từng phương pháp và văn bản bài. Các thay đổi chịu lực:

1. **SimpleRCA không phải một phương pháp duy nhất.** Bài mô tả luật đếm cảnh báo. Nhưng ở nhánh `rcaeval` của repo tác giả, tên `simplerca` được gán cho `NezhaRCA`, tức BARO cộng phiếu trace/log chỉ cho top-3 của BARO (mục 3a, dòng 3). Con số 0,80 trên RE2-TT chưa biết sinh từ phiên bản nào.
2. **Không có đường chạy công bố cho TraceRCA, MicroRank, PDiagnose của RCAEval**, ở cả nhánh `main` lẫn ba nhánh bài báo (mục 1).
3. **Thêm bảng đường nhãn (mục 4)**: tìm thêm được đường nhãn ở MicroRCA gốc, Eadro gốc, GDN gốc, SimpleRCA, và runner RCAEval.
4. **Eadro gốc không chạy được nếu không sửa** (lỗi gọi hàm), và chia train/test bằng xáo ngẫu nhiên.
5. **DeepTraLog bị hạ xuống phương án C**: repo không có code dựng đồ thị từ dữ liệu thô, và theo T-002 log RCAEval không có trace ID.
6. Sửa lại nhận định của bản 1 về "B có vẻ đã chốt RCAEval" (Minh nêu): chi phí của mọi phương án ở mục 8 tính khi dữ liệu đã ở dạng RCAEval; với dataset khác, phương án nào cũng cần thêm adapter đọc dữ liệu.

## 1. Phương pháp có trong RCAEval (đã kiểm code)

Đã kiểm nhánh `main` (`259ea41`, khớp MRP) và ba nhánh bài báo `www25` (bài RCAEval), `fse26` (bài TORAI), `ase24`. Danh sách đăng ký: `RE:RCAEval/e2e/__init__.py:44-72`, `RE:main.py:47-82`.

| Hàm | File | Họ | Đã kiểm trên code |
|---|---|---|---|
| `baro` | `RE:RCAEval/e2e/baro.py:19-60` | Thống kê trên metric | Chỉ là bước xếp hạng: RobustScaler học trên đoạn trước `inject_time`, điểm = max z sau đó (`baro.py:22-24, 49-51`). Không có BOCPD (BOCPD ở `BR`, mục 2). |
| `mmbaro`, `mmnsigma` | `RE:RCAEval/e2e/baro.py:178`, `:71` | Thống kê đa nguồn | Thêm chuỗi đếm log và chuỗi trace; chuỗi trace chỉ dùng cho OB, TT (`baro.py:63-68`). |
| `nsigma` | `RE:RCAEval/e2e/__init__.py:109-148` | Thống kê trên metric | Như `baro` nhưng StandardScaler (`__init__.py:137`). |
| `e_diagnosis` | `RE:RCAEval/e2e/__init__.py:154-201` | Thống kê | Gọi PyRCA. |
| `circa`, `mmcirca` | `RE:RCAEval/e2e/circa.py:18-43`, `:45` | Nhân quả + đồ thị | Đồ thị học bằng PC trên toàn cửa sổ (`circa.py:31-33`, `RE:graph_construction/pc.py:12-21`), **không phải đồ thị kiến trúc** như bài gốc (K1 §C.6). Chấm bằng RHT với `detect_time=inject_time`, `current=inject_time+300` (`RE:graph_heads/rht.py:362, 365`). |
| `rcd`, `mmrcd` | `RE:RCAEval/e2e/rcd.py:449-462` | Nhân quả | Chia normal/anomal theo `inject_time`. Cần Python 3.8 riêng (`RE:main.py:133-134`). |
| `torai` | `RE:RCAEval/e2e/torai.py:69` | Đa nguồn, nhân quả, không dùng đồ thị gọi | Cắt theo `inject_time` (`torai.py:84-112`). Import từ `rcd` nên cần môi trường Python 3.8. Có tham số `service`, `fault_type`, `case` trong chữ ký nhưng thân hàm không đọc (các chỗ có chữ "service" là biến cục bộ `service_list`, `service_ranks` từ dòng 238); runner không truyền (`RE:main.py:408-417`). |
| `tracerca` | `RE:RCAEval/e2e/tracerca.py:45-95` | Trace, không đồ thị | **Bản rút gọn**: span bất thường nếu `duration ≥ mean + 3·std` của operation (`tracerca.py:61`); xếp hạng theo trung bình điều hòa của support và confidence (`:64-84`). Khác xa bản gốc (mục 2). |
| `microrank` | `RE:RCAEval/e2e/microrank.py:646-711` | Trace + PageRank | Phát hiện cùng luật span `mean + 3·std` (`microrank.py:666-667`); PageRank `d=0.85` (`:20`); phổ `dstar2` (`:702`). Khác bản gốc ở bước phát hiện (mục 2). |
| `pdiagnose.py` | `RE:RCAEval/e2e/pdiagnose.py:49-125` | Đa nguồn, luật bỏ phiếu | **Không phải hàm phương pháp**: chỉ có `main()` đọc đường dẫn cứng (`:55-62`); không có hàm `pdiagnose` ở bất kỳ commit nào (`git log --all -S "def pdiagnose"` không trả kết quả). Nội dung: đếm điểm metric vượt 3σ, đếm log chứa "error/fail", đếm span vượt 3σ, cộng theo service. Phần log đếm trên **toàn bộ** dữ liệu, không tách trước/sau sự cố (`:89-92`). |
| `microcause`, `easyrca`, `cloudranger` | `RE:RCAEval/e2e/microcause.py:2178`, `easyrca.py:2178`, `cloudranger.py:154` | Nhân quả / tương quan + random walk | Cần SLI; runner chọn SLI từ tên service gốc lấy từ tên thư mục ca (`RE:main.py:283, 340-363`). Xem mục 4. |
| `run`, `causalrca`, `mscred` | `RE:RCAEval/e2e/run.py`, `causalrca.py`, `mscred.py` | Học sâu (torch) | |
| `pc_pagerank` và các biến thể `*_pagerank`, `*_randomwalk`, `micro_diag` | `RE:RCAEval/e2e/pc_pagerank.py:13`, `pc_randomwalk.py`, `lingam_pagerank.py` | Đồ thị nhân quả học từ metric + PageRank / random walk | Chạy được qua `main.py`. |
| `causalai`, `ht`, `eventadl` | `RE:RCAEval/e2e/causalai.py:14`, `__init__.py:204`, `eventadl.py:129` | Khác | `causalai` không có trong `main.py`; `ht` chỉ nhập ở Python 3.8; `eventadl` dùng log sự kiện kiểu CloudTrail. |

**Runner (đã kiểm code):**
- `RE:main.py:204-208, 289` chỉ đọc `data.csv` hoặc `simple_metrics.csv`. Nhánh đa nguồn đọc thêm `logts.csv`, `tracets_*.csv` (`main.py:368-400`). **Không có chỗ nào đọc `traces.csv`.** Kiểm cả nhánh `www25`, `fse26`: `git grep "traces.csv\|tracerca(\|microrank("` không ra lời gọi nào. Notebook `docs/multi-source-rca-demo.ipynb` đọc `traces.csv` nhưng chỉ gọi `mmbaro`.
- Hệ quả: TraceRCA, MicroRank, PDiagnose mà hai bài RCAEval và TORAI báo kết quả **không có code chạy được công bố**. Bài TORAI ghi đã dùng "publicly available implementation" cho MicroRank và TraceRCA (bài TORAI, văn bản dòng 249), nhưng không rõ là bản nào.
- `tracerca`, `microrank` so `startTime + duration` với `inject_time` cùng đơn vị (dòng đổi sang micro giây bị comment: `tracerca.py:51`, `microrank.py:652`). Theo T-002, đơn vị `duration` của RE2 còn OPEN.
- `RE:main.py:311-315`: đọc `inject_time.txt`, cắt `length/2` phút trước và sau mốc đó. Cửa sổ dữ liệu luôn được cắt quanh mốc tiêm lỗi (xem mục 4).

## 2. Code gốc ngoài RCAEval (đã kiểm code)

Giấy phép kiểm qua GitHub API và danh sách file gốc, ngày 02/10/2026. "Không có LICENSE" nghĩa là repo không có file giấy phép, mặc định giữ mọi quyền. Đọc để tái lập thường được chấp nhận trong nghiên cứu, nhưng không chép code vào repo này. Nhận định này **chưa kiểm** với nhà trường.

| Phương pháp | Repo | Giấy phép | Đã kiểm trên code |
|---|---|---|---|
| BARO (đầy đủ) | `phamquiluan/baro` | MIT | BOCPD chỉ chạy trên cột latency/error (`BR:baro/anomaly_detection.py:94-97`); chuẩn hóa min–max trên **cả cửa sổ**, kể cả phần sau sự cố (`:120-127`), tức không thuần trực tuyến; hazard hằng 50 (`:144`). N-Sigma k=3, từ điểm 100 (`:7`). Khi chấm phát hiện, cửa sổ được cắt 300 điểm trước và 300 điểm sau mốc tiêm (`BR:baro/reproducibility.py:133-137`). |
| SimpleRCA | `LGU-SE-Internal/Simple-RCA` (submodule của `OperationsPAI/rca-algo-contrib`) | Không có LICENSE | Hai phiên bản, xem mục 3a dòng 3. |
| Eadro | `BEbillionaireUSD/Eadro` | Không có LICENSE | `main.py:89-90` gọi `chunkDataset(train_chunks, node_num)` nhưng hàm khởi tạo đòi thêm `edges` (`main.py:5`) → **không chạy được nếu không sửa**. Chia train/test bằng `np.random.shuffle` trên chunk (`preprocess/align.py:131-138`), không theo thời gian; nhãn chunk = service gốc nếu chunk trùng khoảng lỗi (`align.py:18-31`). Chọn checkpoint theo HR@1 trên test (`base.py:102-105`). Tự lùi về CPU (`main.py:62-67`). Bài SimpleRCA cũng nhận xét độ chính xác cao của Eadro "chủ yếu do trùng mẫu giữa tập train và test" (bài SimpleRCA, văn bản dòng 611). |
| MicroRCA | `elastisys/MicroRCA` | Không có LICENSE | Là script chạy trên file CSV đặt tên theo `faults_name` (`MicroRCA.py:53-70`). Cần: độ trễ theo cạnh gọi nguồn/đích (`:53, 57`), file đồ thị service–host `_mpg.csv` (`:70`), metric container `ctn_*` và host `node_*` (`:112, 127`). BIRCH `threshold=0.045`, làm trơn 12 điểm (`:16, 276`); `alpha=0.55` (`:275`); PageRank `alpha=0.85` (`:255`). Dùng `iteritems` đã bị pandas 2 bỏ (`:25`). Đường nhãn: xem mục 4. |
| MicroRank (gốc) | `IntelligentDDS/MicroRank` | MIT | Báo động hệ thống khi số trace vượt `μ+1.5σ` lớn hơn 8 (`MK:anormaly_detector.py:62, 70`); chia trace bình thường/bất thường bằng `μ+σ` cộng 50 ms (`:93-102`). Phổ mặc định `dstar2` (`MK:online_rca.py:242`), không phải Ochiai như K1 ghi. Đọc trace từ Elasticsearch (`MK:preprocess_data.py:9-14`). |
| TraceRCA (gốc) | `NetManAIOps/TraceRCA` | Không có LICENSE | Quy trình nhiều bước qua Makefile: chọn đặc trưng theo từng cặp gọi (`TR:run_selecting_features.py:52-80`), phát hiện 3σ trên các đặc trưng đã chọn (`TR:run_anomaly_detection_invo.py:38-59`), khai phá luật kết hợp (`SUPPORT=0.1`, `K=100`, `TR:Makefile:22-25`). Nhãn service gốc chỉ dùng ở bước chấm (`TR:run_localization_collect.py:79-80`). Bản RCAEval chỉ giữ ý tưởng support/confidence. |
| PDiagnose | Không có | — | Bài RCAEval và bài TORAI đều ghi "source code is unavailable" và tự cài (bài RCAEval, văn bản dòng 488; bài TORAI, dòng 249). |
| DeepTraLog | `FudanSELab/DeepTraLog` | Không có LICENSE | Chỉ có mô hình và dữ liệu đồ thị đã dựng sẵn (`DT:model/dataset.py:64-74` đọc JSON đồ thị). **Không có code dựng đồ thị trace–log từ dữ liệu thô** và không có code tạo embedding sự kiện. Tự lùi về CPU (`DT:model/main.py:40`). |
| GDN | `d-ailin/GDN` | MIT | Mặc định `report='best'` (`GD:main.py:216`, `run.sh`): chọn ngưỡng tối đa F1 **trên nhãn test** (`GD:evaluate.py:141-144`). Chế độ `val` dùng ngưỡng = điểm cao nhất trên dữ liệu bình thường (`GD:evaluate.py:109`), khớp bài. Thiết bị chọn được (`GD:main.py:208`). |
| SPOT/DSPOT | Repo gốc `Amossys-team/SPOT` trả 404 | `ads-evt` (PyPI 0.0.4): GNU GPLv3 | `limjcst/ads-evt` nói là bọc nguyên bản và có test so khớp. Một bản sao khác nằm ở `RE:RCAEval/e2e/microcause.py:2095`, nhưng không được gọi (`:2190` bị comment). |
| CIRCA (gốc) | `NetManAIOps/CIRCA` | BSD-3-Clause | Có lớp `StructuralGraph` (`circa/graph/structural.py:169`) để chạy với đồ thị cấu trúc. Bài PRISM nói đã dựng và công bố đồ thị phụ thuộc cho các hệ trong RCAEval (bài PRISM, văn bản dòng 254); chưa kiểm tải được. |
| RCD (gốc) | `azamikram/rcd` | MIT | Hướng dẫn viết cho Ubuntu, Python 3.8, phải vá thư viện bằng symlink (`README.md:5-41`). Chạy trên Windows: chưa kiểm. |

## 3. Bảng ứng viên

"Biết trước thời điểm?" = có cần mốc sự cố từ bên ngoài. "Nhãn để học?" = có cần nhãn nguyên nhân hay nhãn bất thường để huấn luyện (khác với nhãn chỉ để chấm).

### 3a. Phương pháp RCA (đủ 11 ứng viên của MRP P1)

| # | Phương pháp | Họ | Bài toán | Đầu vào | Biết trước thời điểm? | Nhãn để học? | Code, giấy phép, CPU | Bài gần đây dùng (mục 6) | Đề xuất |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **BARO** | Thống kê trên metric | Phát hiện (BOCPD) + xếp hạng | Metric | Bản RE: có. Bản BR: BOCPD tự tìm mốc | Không | RE + BR, MIT, CPU | RCAEval, TORAI, SimpleRCA, DecompRCA, PRISM | **Chọn.** Mạnh, rẻ, có mặt ở cả 5 bài. Chạy cả hai chế độ. |
| 2 | **N-Sigma** | Thống kê trên metric | Xếp hạng (bản BR: cả phát hiện) | Metric | Có (`RE:__init__.py:110-112`) | Không | RE + BR, MIT, CPU | Detector baseline trong bài BARO (K1 §C.4) | **Chọn.** Gần như miễn phí. Là đối chứng của BARO: chỉ khác bộ chuẩn hóa (`__init__.py:137` so với `baro.py:49`). |
| 3 | **SimpleRCA** | Luật đơn giản, đa nguồn | Xếp hạng | Metric, log, trace + dữ liệu bình thường | Có. Nhánh master: lấy đầu và cuối cửa sổ lỗi từ file nhãn (`SR:src/simplerca/adapter.py:49-51`). Nhánh `rcaeval`: lấy `inject_time` (`nezha_adapter.py:31`) | Không | SR, **không có LICENSE**, CPU | Chính bài FSE'26 | **Chọn, cài lại cả hai biến thể** (không chép code): (i) **theo bài**: đếm cảnh báo; metric vượt 3σ hoặc P95 lịch sử, trace P95 gấp ~3 lần bình thường, log có từ khóa lỗi (bài SimpleRCA, văn bản dòng 228-234); (ii) **theo code nhánh `rcaeval`**: tên `simplerca` được gán cho `NezhaRCA` (`main.py:12`). Nó lấy top-5 của BARO (`nezha_rca.py:49`), rồi cộng phiếu trace/log **chỉ cho các service đã nằm trong top-3 của BARO** (`nezha_rca.py:133, 151, 158`). Biến thể (ii) không độc lập với BARO. Chưa biết bảng 2 của bài (RE2-TT 0,80) sinh từ biến thể nào. Vì sao chọn: là baseline "không đồ thị" mạnh nhất được công bố trên RCAEval (LESSONS QT7). |
| 4 | **RCD** | Nhân quả | Xếp hạng metric | Metric (đa nguồn: `mmrcd`) | Có (`RE:rcd.py:461-462`) | Không (cần chia normal/anomal) | RE + gốc, MIT, CPU; Python 3.8 | RCAEval, TORAI, DecompRCA | **Chọn.** Đại diện nhân quả học từ dữ liệu, dùng rộng. |
| 5 | **CIRCA** | Nhân quả + đồ thị | Xếp hạng metric | Metric + đồ thị + mốc phát hiện | Có (`RE:rht.py:362`) | Không | RE (BSD-3) + gốc (BSD-3), CPU; thời gian chạy PC trên hàng trăm metric: chưa kiểm | RCAEval, TORAI, DecompRCA | **Chọn.** Là phương pháp duy nhất trong danh sách mà đồ thị đi vào phép tính điểm (parent set; K1 §D.2 mẫu E). Biến thể đồ thị (PC hay kiến trúc) để Minh quyết (mục 8). |
| 6 | **MicroRank** | Trace + PageRank | Phát hiện trace + xếp hạng operation | Trace | Có (`RE:microrank.py:654-658`) | Không | RE (MIT) + MK (MIT), CPU; cần tự viết adapter đọc trace (mục 1) | RCAEval, TORAI, SimpleRCA | **Chọn.** Là ví dụ PageRank của cô, chạy trên đồ thị dựng từ trace. Dùng code RE (phần PageRank + phổ giống MK, cùng `dstar2`), thêm biến thể dùng luật phát hiện của MK (`μ+σ+50 ms`). |
| 7 | **TraceRCA** | Trace, không đồ thị | Phát hiện span + xếp hạng | Trace | Có (`RE:tracerca.py:53-54`) | Không | RE (MIT, bản rút gọn), CPU; cùng adapter trace với MicroRank. Bản TR gốc không có LICENSE, cần dữ liệu dạng riêng | RCAEval, TORAI | **Chọn bản RE, ghi rõ "bản rút gọn của RCAEval".** Vai trò: bản RE dùng **cùng luật phát hiện** với MicroRank bản RE (`tracerca.py:61` và `microrank.py:667`). Hai phương pháp này tạo cặp so sánh: giữ nguyên bộ phát hiện, chỉ khác bước xếp hạng (có hoặc không có PageRank). Không dùng làm đại diện cho TraceRCA gốc. |
| 8 | **MicroRCA** | Lan truyền trên đồ thị (PPR trên đồ thị con bất thường) | Phát hiện cạnh (BIRCH) + xếp hạng service | Độ trễ cạnh gọi, metric container và host, đồ thị service–host | Không; BIRCH chạy trên cả chuỗi của lần chạy | Không | MR, **không có LICENSE**, CPU; phải cài lại vì code là script gắn với file CSV riêng | SimpleRCA | **Chọn có điều kiện.** Là phương pháp có sẵn duy nhất trong danh sách khớp hai ví dụ của cô cùng lúc: đồ thị con bất thường và PageRank. Điều kiện: (a) dựng được độ trễ cạnh gọi từ trace (trace RCAEval có parentSpanID theo T-002; chưa kiểm cách dựng); (b) có metric host. Nếu không có host thì chạy biến thể chỉ có service và ghi là lệch bài. (c) Bỏ hai đường nhãn trong script gốc (mục 4). |
| 9 | **TORAI** | Đa nguồn, nhân quả, không đồ thị gọi | Xếp hạng service và chỉ báo | Metric, log, trace dưới dạng chuỗi thời gian | Có (`RE:torai.py:84`; bài: cần `t_A` từ bộ phát hiện ngoài) | Không | RE, MIT, CPU; Python 3.8 | Chính bài FSE'26 | **Chọn.** Đối chứng trực tiếp cho câu hỏi "có cần đồ thị gọi không". Rủi ro: cùng nhóm tác giả với RCAEval (mục 7). |
| 10 | **Eadro** | Học có đồ thị (GAT), có giám sát | Phát hiện cửa sổ + xếp hạng service | Log, KPI, trace + đồ thị gọi lịch sử | Không (phân loại cửa sổ) | **Có**: nhãn cửa sổ + service gốc | EA, **không có LICENSE**; code không chạy được nếu không sửa; torch + dgl; CPU được, thời gian chưa kiểm | SimpleRCA | **Chọn có điều kiện.** Đại diện duy nhất của họ "GNN cho RCA". Điều kiện: (a) sửa lỗi `main.py:89-90`; (b) chia train/dev/test theo ô, chọn checkpoint trên dev; (c) đủ ca có nhãn trên dev (phụ thuộc P2); (d) báo trong bảng riêng, không xếp chung với phương pháp không giám sát (MRP §4). Không đạt (c) thì báo "không chạy được công bằng". |
| 11 | **PDiagnose** | Đa nguồn, luật bỏ phiếu | Xếp hạng | Metric, log, trace | Có | Không | Không có code gốc; RE có script sai cửa sổ log (mục 1) | RCAEval, TORAI (cả hai tự cài) | **Không chọn ở A.** Không có code gốc, nên kết quả chỉ phản ánh bản cài lại của người cài. Vai trò "luật bỏ phiếu đa nguồn" đã có SimpleRCA (i). Đưa vào phương án C. |

### 3b. Bộ phát hiện bất thường (Q-30)

| # | Bộ phát hiện | Họ | Đơn vị | Đầu vào | Nhãn để học? | Code, giấy phép | Đề xuất |
|---|---|---|---|---|---|---|---|
| D1 | **BOCPD** (BARO) | Điểm thay đổi Bayes | Thời điểm | Cột latency/error | Không | `BR:anomaly_detection.py:77-151`, MIT | **Chọn.** Cho BARO chế độ tự phát hiện. Phải sửa hai chỗ để không dùng dữ liệu tương lai và nhãn: chuẩn hóa chỉ trên phần đã thấy; chạy trên cửa sổ trượt, không cắt quanh mốc tiêm. |
| D2 | **N-Sigma** | Thống kê | Thời điểm | Metric | Không | `BR:anomaly_detection.py:7-35`, MIT | **Chọn.** Bộ phát hiện đơn giản nhất. |
| D3 | **SPOT/DSPOT** | Cực trị (EVT) | Thời điểm | Chuỗi đơn biến | Không | `ads-evt` (GPLv3) | **Chọn.** Đại diện ngưỡng EVT; ARMOR cũng dùng POT (K1 §C.12). Dùng `ads-evt` vì có test so với bản gốc. Không chép code GPL vào repo. |
| D4 | **Luật trace** | Thống kê trên trace | Span hoặc trace | Trace | Không | `RE:tracerca.py:61` (`μ+3σ` theo span); `MK:anormaly_detector.py:62, 93-102` (theo trace) | **Chọn**, đi kèm MicroRank/TraceRCA, không tốn thêm. Chấm riêng phần phát hiện. |
| D5 | **GDN** | GNN trên đồ thị học được, dự báo | Thời điểm + chuỗi lệch | Chuỗi metric | Không (học trên dữ liệu bình thường) | `GD`, MIT; CPU chưa kiểm | **Chọn.** Đại diện "GNN-based anomaly detection" (ví dụ thứ ba của cô) có code đầy đủ. Bắt buộc dùng `report='val'`. Điều kiện: đủ dữ liệu bình thường để học (MRP §4 tiêu chí 8, phụ thuộc P2). Rủi ro: bài chỉ đánh giá trên dữ liệu cảm biến (K1 §C.11). |
| D6 | BIRCH | Phân cụm | Cạnh gọi | Độ trễ cạnh | Không | `MR:MicroRCA.py:19-46` | Đi theo MicroRCA. |
| D7 | Đầu nhị phân Eadro | GNN có giám sát | Cửa sổ | Đa nguồn | Có | `EA` | Đi theo Eadro. |
| D8 | **DeepTraLog** | Đồ thị trace–log + GGNN | Trace | Span + log gắn vào span | Không (một lớp) | `DT`, không có LICENSE; **thiếu code dựng đồ thị** | **Không chọn ở A; đưa vào C có điều kiện.** Là đại diện duy nhất của mẫu "đồ thị là đối tượng bị chấm" (K1 §D.2 mẫu D). Nhưng phải tự viết bộ dựng đồ thị và embedding, và cần log có trace ID. Theo T-002, log RCAEval không có trace ID. Chỉ khả thi nếu P2 chọn dataset có liên kết log–trace. |

## 4. Đường nhãn và dữ liệu tương lai đã thấy trong code (đã kiểm)

Phục vụ luật cứng 6 và câu hỏi G1 "có đường nào để nhãn lọt vào phương pháp". Mỗi dòng ghi cách chặn trong adapter của nhóm.

| # | Ở đâu | Cái gì lọt vào | Cách chặn |
|---|---|---|---|
| L1 | `RE:main.py:283, 340-363` | Tên service gốc lấy từ tên thư mục ca → chọn SLI → MicroCause, EasyRCA, CloudRanger dùng SLI khi xếp hạng | Không dùng ba phương pháp này; nếu dùng, chọn SLI từ cấu hình cố định (ví dụ cổng vào) |
| L2 | `RE:main.py:311-315` | Cửa sổ dữ liệu cắt đối xứng quanh mốc tiêm lỗi | Chế độ (a) "biết trước thời điểm": hợp lệ, và phải ghi rõ. Chế độ (b): cắt cửa sổ độc lập với nhãn |
| L3 | `BR:reproducibility.py:133-137`; `BR:anomaly_detection.py:120-127` | Khi chấm BOCPD, cửa sổ cắt quanh mốc tiêm; chuẩn hóa dùng cả phần tương lai | Cửa sổ trượt; chuẩn hóa theo phần đã quan sát |
| L4 | `SR:adapter.py:41-51, 120-126` | Adapter đọc nhãn loại lỗi và truyền vào hàm (hàm không dùng); lấy cửa sổ lỗi từ file nhãn | Cài lại không có tham số `fault_type`; cửa sổ theo chế độ (a)/(b) như mọi phương pháp |
| L5 | `MR:MicroRCA.py:297-298` | Ngưỡng BIRCH đổi theo service gốc và loại lỗi (`payment`, `shipping` dùng 0.02) | Một ngưỡng cố định cho mọi ca, chọn trên dev |
| L6 | `MR:MicroRCA.py:327` | Danh sách ứng viên lọc theo các service bị tiêm lỗi (`targets`) | Ứng viên = mọi service quan sát được |
| L7 | `EA:base.py:102-105`; `EA:preprocess/align.py:131-138` | Chọn checkpoint trên test; chia ngẫu nhiên nên các chunk liền nhau của cùng một lần lỗi nằm cả ở train lẫn test | Chia theo ô (MRP §4); checkpoint chọn trên dev |
| L8 | `GD:main.py:216`; `GD:evaluate.py:141-144` | Ngưỡng phát hiện chọn theo F1 trên nhãn test | Dùng `report='val'` |
| L9 | Bài PRISM, văn bản dòng 253 | Với phương pháp có ngưỡng, bài báo báo kết quả tốt nhất qua nhiều ngưỡng | Không dùng số của bài làm mốc so sánh |

Không thấy đường nhãn ở: `torai` (tham số có nhưng không đọc), TraceRCA gốc (nhãn chỉ ở bước chấm), `baro`/`nsigma`/`rcd`/`circa` của RCAEval ngoài L2.

## 5. Phương pháp trong RCAEval hoặc K1 nhưng không có trong ứng viên MRP

| Phương pháp | Lý do | Thuộc phương án |
|---|---|---|
| MicroCause, EasyRCA, CloudRanger | Cần SLI (L1). Họ nhân quả đã có RCD, CIRCA | Không |
| PC-PageRank (và `*_pagerank`, `*_randomwalk`) | Chạy sẵn qua `main.py`. DecompRCA và PRISM dùng làm baseline. PageRank chạy trên đồ thị nhân quả học từ metric, không phải đồ thị gọi | B (thay MicroRCA), C |
| mmBARO, mmRCD, mmCIRCA | Biến thể đa nguồn của 1, 4, 5; gần như miễn phí; không tính vào số đếm | A, B, C |
| CausalRCA | Nhân quả học sâu; bài TORAI và SimpleRCA dùng; chạy qua `main.py` (cần torch) | C |
| Nezha | Đa nguồn, khác nhóm tác giả; bài SimpleRCA dùng. Bài TORAI ghi Nezha cần trace ID trong từng dòng log (bài TORAI, văn bản dòng 249); theo T-002 log RCAEval không có | C, có điều kiện dữ liệu |
| ε-Diagnosis, RUN, MSCRED, HT, causalai, EventADL | Họ đã có đại diện rẻ hơn, hoặc khác loại dữ liệu | Không |
| DéjàVu | Có giám sát theo từng hệ, cho lỗi lặp lại (K1 §C.9); Eadro đã đại diện họ này | Không |
| ARMOR | Code chỉ trên Zenodo (K1 §A.2), chưa kiểm tải được | Không (ứng viên nếu P4 cho thấy thiếu dữ liệu quan sát là hạn chế chính) |
| DiagFusion, ART, MicroDig, ShapleyIQ, MicroHECL | Bài SimpleRCA dùng trên benchmark mới của họ; chưa kiểm code | Không |

## 6. Bài gần đây dùng phương pháp nào làm baseline (đã đọc văn bản bài)

| Phương pháp | RCAEval (WWW'25 Companion) | TORAI (FSE'26) | SimpleRCA (FSE'26) | DecompRCA (NeurIPS'26 E&D) | PRISM (bản thảo 01/2026) |
|---|---|---|---|---|---|
| BARO | ✓ | ✓ | ✓ | ✓ | ✓ |
| RCD | ✓ | ✓ | | ✓ | |
| CIRCA | ✓ | ✓ | | ✓ | |
| MicroRank | ✓ | ✓ | ✓ | | |
| TraceRCA | ✓ | ✓ | | | |
| PDiagnose | ✓ (tự cài) | ✓ (tự cài) | | | |
| MicroRCA | | | ✓ | | |
| Eadro | | | ✓ | | |
| CausalRCA | ✓ | ✓ | ✓ | | |
| MicroCause | ✓ | ✓ | | | |
| PC-PageRank / PageRank / RandomWalk | | | | ✓ | ✓ |
| ε-Diagnosis | ✓ | | | ✓ | |
| Nezha | | | ✓ | | |

Nguồn từng cột: bài RCAEval, văn bản dòng 488; bài TORAI, dòng 230; bài SimpleRCA, dòng 861-865; bài DecompRCA, dòng 493-500; bài PRISM, dòng 200-252. N-Sigma, SimpleRCA và TORAI không có cột vì chúng là phương pháp của chính các bài.

## 7. Nhận định dựa trên kết quả đã công bố, và nguyên nhân khả thi khác (Q-33)

| Nhận định | Nguyên nhân khả thi khác |
|---|---|
| SimpleRCA đạt Top@1 0,80 trên RE2-TT, BARO 0,67 (bài SimpleRCA, bảng 2) → SimpleRCA là baseline mạnh | (a) Số của BARO lấy từ bài gốc, không chạy lại (bài SimpleRCA, văn bản dòng 607), nên hai số có thể khác giao thức. (b) Nếu số sinh từ biến thể (ii) thì SimpleRCA = BARO cộng phiếu; phần hơn có thể chỉ do xếp lại trong top-3 của BARO. (c) RE2-TT có 5 service gốc và đồ thị gần như không đổi (LESSONS ST3). (d) Luật có thể đã được chỉnh trên chính các benchmark này. → Chỉ dùng để chọn SimpleRCA làm ứng viên, không dùng để kết luận. |
| BARO, RCD, CIRCA xuất hiện ở hầu hết bài → "baseline chuẩn" | Có thể vì chúng sẵn trong RCAEval. RCAEval, TORAI, DecompRCA, PRISM có chung tác giả Luan Pham, nên tần suất không độc lập. |
| TORAI hơn chín baseline | Benchmark của chính nhóm tác giả; chế độ biết trước `t_A`; ba baseline trace không có code chạy công bố (mục 1); baseline cần SLI có thể đã nhận SLI từ nhãn (L1). |
| Eadro mạnh trong bài gốc | Chia ngẫu nhiên và chọn checkpoint trên test (L7). Bài SimpleRCA cũng nêu chuyện trùng mẫu train/test. |
| MicroRCA đạt Precision@1 khoảng 89% (K1 §C.2) | Ngưỡng chỉnh theo service gốc, ứng viên lọc theo service bị tiêm (L5, L6). |
| GDN F1 0,81 trên SWaT (K1 §C.11) | Chế độ mặc định chọn ngưỡng trên nhãn test (L8). Chưa kiểm bảng của bài dùng chế độ nào. |

## 8. Đề xuất và ba phương án cho Minh chốt

### 8.1. Phương án

**A — Phủ đủ họ, có đại diện cho ba ví dụ của cô (đề xuất).**
- RCA (10): BARO, N-Sigma, SimpleRCA (hai biến thể), RCD, CIRCA, MicroRank, TraceRCA (bản RCAEval), TORAI, MicroRCA (có điều kiện), Eadro (có điều kiện). Chạy kèm mmBARO, mmRCD, mmCIRCA.
- Phát hiện: BOCPD, N-Sigma, SPOT, luật trace, GDN. BIRCH và đầu nhị phân Eadro đi theo phương pháp mẹ.

**B — Gọn: không học có giám sát, không cài lại phương pháp từ repo không có giấy phép.**
- RCA (9): BARO, N-Sigma, SimpleRCA (hai biến thể), RCD, CIRCA, MicroRank, TraceRCA (bản RCAEval), TORAI, PC-PageRank (thay vai trò lan truyền của MicroRCA). Chạy kèm biến thể mm*.
- Phát hiện: như A, trừ BIRCH và đầu Eadro.

**C — Mở rộng (14, vượt mức 8–12 của MRP).**
- RCA: A + PC-PageRank + CausalRCA + PDiagnose (sửa script RCAEval thành hàm, sửa cửa sổ log) + Nezha (có điều kiện dữ liệu). TraceRCA gốc chạy thêm như biến thể.
- Phát hiện: A + DeepTraLog (có điều kiện dữ liệu).

### 8.2. Phủ họ và ba ví dụ của cô

| Họ (MRP P1) hoặc ví dụ của cô | A | B | C |
|---|---|---|---|
| Thống kê trên metric | BARO, N-Sigma | như A | như A |
| Nhân quả | RCD, CIRCA | như A | + CausalRCA |
| Dựa trên trace | MicroRank, TraceRCA | như A | + TraceRCA gốc |
| Lan truyền trên đồ thị | MicroRank, MicroRCA* | MicroRank, PC-PageRank | MicroRank, MicroRCA*, PC-PageRank |
| Đa nguồn | SimpleRCA, TORAI, mm* | như A | + PDiagnose, Nezha* |
| Học có đồ thị (RCA) | Eadro* | **không có** | Eadro* |
| GNN cho phát hiện | GDN | GDN | GDN, DeepTraLog* |
| Ví dụ "PageRank" | MicroRank, MicroRCA* | MicroRank, PC-PageRank | đủ cả ba |
| Ví dụ "đồ thị con bất thường" | MicroRCA* | **không có đại diện có sẵn** | MicroRCA* |
| Ví dụ "GNN" | Eadro*, GDN | chỉ GDN (phát hiện) | Eadro*, GDN, DeepTraLog* |

`*` = có điều kiện. Ở A, họ "học có đồ thị (RCA)" và ví dụ "đồ thị con" **chỉ có đại diện có điều kiện**. Nếu P2 cho thấy điều kiện không đạt, A rút về B ở hai ô này, và báo cáo phải nêu lý do bằng bằng chứng.

### 8.3. Lợi và hại

Ước lượng chi phí dưới đây là ước lượng thô, **chưa kiểm**. Phần việc chung cho mọi phương án:
- adapter đọc trace cho MicroRank/TraceRCA;
- cài lại SimpleRCA (hai biến thể);
- bọc BOCPD, N-Sigma, SPOT chạy trên cửa sổ trượt;
- chuyển dữ liệu cho GDN;
- hai môi trường Python (3.12, và 3.8 cho RCD/TORAI).

Tất cả tính khi dữ liệu đã ở dạng RCAEval. Với dataset khác, mọi phương án đều cần thêm adapter đọc dữ liệu, nên khác biệt chi phí giữa A, B, C **không phải lý do để chọn dataset** (MRP §4, Q-31).

| | A | B | C |
|---|---|---|---|
| **Lợi** | Phủ đủ sáu họ của MRP, mỗi ví dụ của cô có một phương pháp đã công bố làm mốc. Có ba cặp đối chứng trong cùng họ: BARO/N-Sigma (bộ chuẩn hóa), MicroRank/TraceRCA (có/không PageRank, cùng bộ phát hiện), MicroRCA/PC-PageRank nếu cần (đồ thị gọi hay đồ thị học). Có một phương pháp có giám sát để hỏi "nhãn có giúp không" (RQ1, RQ2). Nằm trong mức 8–12 của MRP. | Rẻ nhất: không torch/dgl, không cài lại phương pháp từ repo không có giấy phép. Mọi phương pháp RCA đều không giám sát, nên xếp chung một bảng được. Ít rủi ro trễ tiến độ P1–P3. | Phủ rộng nhất. Có phương pháp khác nhóm tác giả RCAEval (Nezha, CausalRCA), giảm thiên vị một nhóm. Có đại diện cho mẫu "đồ thị là đối tượng bị chấm" (DeepTraLog). |
| **Hại** | Hai phương pháp có điều kiện tốn công nhất. Eadro: sửa lỗi, chia lại dữ liệu, tiền xử lý log (Drain + Hawkes), môi trường torch + dgl, cần đủ ca có nhãn. MicroRCA: cài lại từ code không có giấy phép, dựng độ trễ cạnh từ trace, có thể thiếu metric host. Nếu điều kiện không đạt thì tốn công mà vẫn rút về B. | Không có phương pháp đã công bố nào cho ví dụ "đồ thị con bất thường" và cho "GNN dùng trong RCA". Cô hỏi "đồ thị con / GNN thì prior work làm thế nào, hạn chế ở đâu" thì P4 không có số để trả lời. PC-PageRank chỉ thay được một phần MicroRCA, vì nó chạy trên đồ thị nhân quả học từ metric, không phải đồ thị gọi. Không có góc nhìn "có giám sát". | Vượt mức 8–12 của MRP. Ba phương pháp thêm có thể **không chạy được trên RCAEval**: DeepTraLog và Nezha cần log có trace ID, PDiagnose không có code gốc. Chi phí cao nhất, rủi ro trễ P1 lớn nhất. Nhiều phương pháp hơn không tự trả lời thêm câu hỏi nào nếu chưa có RQ cần chúng (LESSONS QT1). |
| **Rủi ro rò nhãn cần chặn** | L1–L8 | L1–L4 | L1–L8 + chưa kiểm cho Nezha, CausalRCA, DeepTraLog |
| **Phụ thuộc P2** | Có: điều kiện của MicroRCA, Eadro, GDN | Có: GDN | Nhiều nhất |

### 8.4. Khuyến nghị

**Chọn A, chốt hai phương pháp có điều kiện (MicroRCA, Eadro) sau khi có thẻ dataset (T-002, T-003).** Lý do: A là phương án duy nhất có prior work cho cả ba ví dụ của cô mà vẫn trong mức 8–12. Nếu điều kiện không đạt, A tự rút về B, và lý do được ghi bằng bằng chứng. Báo cáo "đã thử, không chạy được công bằng vì X" vẫn là một câu trả lời hợp lệ (MRP §3). B hợp lý nếu Minh ưu tiên tiến độ hơn độ phủ. C chỉ nên chọn nếu P2 chọn được dataset có liên kết log–trace.

Khuyến nghị này **chưa kiểm** ở hai giả định:
- Giả định 1: chi phí Eadro và MicroRCA nằm trong một task P1. Sai khi tiền xử lý Eadro hoặc dựng độ trễ cạnh tốn hơn dự kiến.
- Giả định 2: dev có đủ ca có nhãn để huấn luyện Eadro. Sai khi P2 chọn dataset nhỏ.

### 8.5. Cần Minh quyết

1. Chọn A, B hay C (hoặc sửa).
2. Có chấp nhận đọc code không có giấy phép (SimpleRCA, Eadro, MicroRCA, TraceRCA gốc, DeepTraLog) để cài lại, không chép vào repo không. Nếu không: A mất MicroRCA, Eadro, SimpleRCA. Riêng SimpleRCA (i) vẫn cài được theo mô tả trong bài.
3. CIRCA chạy biến thể nào: đồ thị PC (RCAEval), đồ thị kiến trúc (bài gốc; có thể dùng đồ thị PRISM công bố, chưa kiểm), hay cả hai. Đề xuất: cả hai. Phần chênh giữa hai biến thể là bằng chứng trực tiếp cho câu "đồ thị đúng có giúp không" (RQ3d).
4. SimpleRCA: chạy cả hai biến thể (đề xuất), hay chỉ một.

## 9. Nguồn và revision

| Nguồn | Revision / ngày truy cập |
|---|---|
| RCAEval `phamquiluan/RCAEval` | `main` `259ea4167160256a74ad30004aa3d96a998c846e`; `www25` `9d14687ce0644188f1f1a576fd3f57cd903af446`; `fse26` `eeadab4f797ed7a0012958fb86f0e4af621ddba6`; `ase24` `19e54db4bf3b04f0759acaf491c202c3a5142324` |
| BARO `phamquiluan/baro` | `e35f4ec1095e5cac891d52de9ad18a5b32a37ec8` |
| Simple-RCA `LGU-SE-Internal/Simple-RCA` | master `1be391178d872302dd17fcefa3d2cc4505ce4513` (commit mà `OperationsPAI/rca-algo-contrib` trỏ tới); nhánh `rcaeval` `5fd1f7fceab7aae92efe9e86500cfc004c0950d1` |
| Eadro `BEbillionaireUSD/Eadro` | `82ff9c9a7a58a9cd2b713aa78754a73c543a15db` |
| MicroRCA `elastisys/MicroRCA` | `de334b2815742a248225cf6e242840a9d5fedc9a` |
| MicroRank `IntelligentDDS/MicroRank` | `efd85e8e6f0fad30f6f8aaf0555e3324d8f5f982` |
| TraceRCA `NetManAIOps/TraceRCA` | `b9087c72d201fbb17d724114cd389de4854815ad` |
| DeepTraLog `FudanSELab/DeepTraLog` | `04376dcb99d4b0fd0c50850255c2c4f9ec9503c1` |
| GDN `d-ailin/GDN` | `9853899da860682669a134e4af315d036aab4eca` |
| CIRCA `NetManAIOps/CIRCA` | `0215e1880096aa02a305c697f1c23cac4600ebd2` |
| RCD `azamikram/rcd` | `373882c6982db7a999ec1ff99ea54c644a48b409` |
| SPOT | `limjcst/ads-evt`, PyPI `ads-evt` 0.0.4 (GPLv3); `Amossys-team/SPOT` 404 ngày 02/10/2026 |
| Bài RCAEval | arXiv 2412.17015, WWW'25 Companion |
| Bài TORAI | arXiv 2604.13522v1, FSE'26 |
| Bài SimpleRCA | arXiv 2510.04711, FSE'26 |
| Bài DecompRCA | arXiv 2609.36686 và README `cruiseresearchgroup/DecompRCA`, NeurIPS'26 E&D |
| Bài PRISM | arXiv 2601.21359v1, bản thảo, chưa thấy nơi đăng |

Giới hạn: văn bản bài lấy từ arXiv HTML. Tiêu đề cột của bảng bị mất khi chuyển sang text; cột đầu của bảng 2 bài SimpleRCA được suy là Top@1 từ câu ở văn bản dòng 610. Trước khi dùng số của bài làm căn cứ trong báo cáo, phải đối chiếu bản PDF.
