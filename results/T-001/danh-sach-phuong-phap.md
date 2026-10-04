# T-001 — Danh sách phương pháp cho P1 (bản 4: sửa theo phản biện; danh sách chốt theo Q-37, Q-38)

Ngày: 02/10/2026. Người làm: Claude, phiên 2 (làm lại toàn bộ theo yêu cầu của Minh).
- Bản 1: `v1-danh-sach-phuong-phap.md`. Bản 2 (ba phương án A/B/C): `v2-danh-sach-phuong-phap.md`. Bản 3 (trước phản biện): `v3-danh-sach-phuong-phap.md`.
- Bản 4 sửa theo `tasks/T-001-danh-sach-phuong-phap/REVIEW.md` (R1–R4, N1–N5). Minh duyệt ngày 03/10/2026: "duyệt đề xuất".
- **Danh sách đã chốt ở mục 8.** Minh chốt ngày 02/10/2026: "tôi chốt là làm gọn lại nhé" (Q-37), rồi chốt thêm: bỏ SPOT, CIRCA chạy cả hai biến thể đồ thị, RCD thành biến thể đối chứng của TORAI, tách task đo thời gian chạy.
- **Không giả định dataset.** Dataset chưa chốt; việc chọn thuộc P2, Minh duyệt ở G1 (MRP §4, Q-31). File này chỉ ghi mỗi phương pháp *cần* dữ liệu gì. Dữ kiện về RCAEval chỉ là dữ kiện về một ứng viên của P2, không dùng để chọn dataset (Minh duyệt sửa ngày 03/10/2026).
- Chưa chạy phương pháp nào, chưa dựng môi trường, không tải dữ liệu (SPEC "Không làm"). Riêng hai file code nhỏ của artifact Zenodo (2 MB) đã được tải vào scratchpad để đọc.

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

### Khác gì so với bản 2

1. **Bỏ lập luận "có mốc cho ba ví dụ của cô".** Ba ví dụ (PageRank, subgraph, GNN) thuộc bước 2: phương pháp đồ thị của nhóm. Chúng không phải danh sách baseline và không bắt buộc (DECISIONS Q-24; `docs/reference/sources/advisor-2026-09-23.md:17`). Con số 8–12 và yêu cầu "phủ đủ các họ" là ước lượng và tiêu chí của MRP (`docs/MRP.md:132`), không phải yêu cầu của cô. Cô nhấn chiều sâu: "chưa sâu kỹ thuật của từng phương pháp" (`advisor-2026-09-23.md:26`).
2. **Danh sách gọn được chốt** (mục 8). MicroRCA và Eadro chuyển sang dự phòng.
3. **SimpleRCA chỉ còn bản cài lại theo mô tả bài.** Biến thể "BARO + phiếu" bỏ khỏi danh sách, vì gọi nó là SimpleRCA dễ gây hiểu nhầm. Thêm bốn dữ kiện mới (mục 3a, dòng 3).
4. **Đã kiểm thêm, chỉ đọc:** gói cho Python 3.8 trên Windows đều có wheel; dữ kiện về RCAEval (một ứng viên của P2): không có metric host, không kèm chuỗi log/trace mà TORAI cần (mục 8.3).
5. **Thêm phân loại mức code M1–M4** (mục 8.2).
6. Sửa tên nhánh: commit `1be3911` của Simple-RCA là nhánh mặc định `orig`, không phải `master`.

### Khác gì so với bản 3

Sửa theo phản biện (REVIEW.md). Không đổi danh sách đã chốt.

1. **CIRCA bản RCAEval chỉ chấm bằng RHT, không có DA** (R1). Hai biến thể đồ thị chưa chắc dùng cùng cách chấm; chọn RHT hay RHT + DA để mở cho hồ sơ P1. Ghi các giả định định dạng của hàm (N1).
2. **MicroRank bản RCAEval có hai sai lệch ở phần dựng đầu vào** và chỉ trả tối đa 11 operation (R2, N2). Bỏ câu "cùng luật phát hiện, chỉ khác bước xếp hạng" của cặp MicroRank–TraceRCA.
3. **TORAI và RCD khác nhiều bước**, không chỉ bước gom cụm (R3). Thêm điểm giảm mẫu và ghép theo chỉ số, chưa kiểm bằng chạy.
4. **GDN và BOCPD:** thêm đường chuẩn hóa bằng dữ liệu tương lai của GDN (R4) và cách chấm BOCPD không chuẩn của BARO gốc (N5).
5. **CIRCA hai biến thể** chỉ là gợi ý cho RQ3d, không phải bằng chứng (N3). Luật gán T/S/L/E định nghĩa theo schema từng dataset (N1).
6. **SimpleRCA:** liệt kê tham số bài để ngỏ; thêm dòng Q-33 cho lập luận "dataset có quá dễ không" (N4).

## 1. Phương pháp có trong RCAEval (đã kiểm code)

Đã kiểm nhánh `main` (`259ea41`, khớp MRP) và ba nhánh bài báo `www25` (bài RCAEval), `fse26` (bài TORAI), `ase24`. Danh sách đăng ký: `RE:RCAEval/e2e/__init__.py:44-72`, `RE:main.py:47-82`.

| Hàm | File | Họ | Đã kiểm trên code |
|---|---|---|---|
| `baro` | `RE:RCAEval/e2e/baro.py:19-60` | Thống kê trên metric | Chỉ là bước xếp hạng: RobustScaler học trên đoạn trước `inject_time`, điểm = max z sau đó (`baro.py:22-24, 49-51`). Không có BOCPD (BOCPD ở `BR`, mục 2). |
| `mmbaro`, `mmnsigma` | `RE:RCAEval/e2e/baro.py:178`, `:71` | Thống kê đa nguồn | Thêm chuỗi đếm log và chuỗi trace; chuỗi trace chỉ dùng cho OB, TT (`baro.py:63-68`). |
| `nsigma` | `RE:RCAEval/e2e/__init__.py:109-148` | Thống kê trên metric | Như `baro` nhưng StandardScaler (`__init__.py:137`). |
| `e_diagnosis` | `RE:RCAEval/e2e/__init__.py:154-201` | Thống kê | Gọi PyRCA. |
| `circa`, `mmcirca` | `RE:RCAEval/e2e/circa.py:18-43`, `:45` | Nhân quả + đồ thị | Đồ thị học bằng PC trên toàn cửa sổ (`circa.py:31-33`, `RE:graph_construction/pc.py:12-21`), **không phải đồ thị kiến trúc** như bài gốc (K1 §C.6). Chấm bằng RHT với `detect_time=inject_time`, `current=inject_time+300` (`RE:graph_heads/rht.py:362, 365`). **Chỉ có RHT, không có DA** (Descendant Adjustment, chỉnh điểm theo nút con cháu): `RHTScorer` là scorer duy nhất được gọi (`rht.py:345, 365`); lớp `DAScorer` có trong file (`:232`) nhưng không được gọi. CIRCA gốc có cả cấu hình RHT và RHT + DA (`CIRCA:circa/experiment/comparison/models.py:596-635`). Vậy bản này khác bài ở hai thành phần: đồ thị và DA. Giả định định dạng: lấy mẫu 1 giây (`rht.py:362`); tên cột dạng `service_metric`, cột khác dạng bị bỏ im lặng (`:350-358`); lỗi thì wrapper `@rca` trả thứ tự cột (`RE:RCAEval/e2e/__init__.py:22-35`). SLI chọn ngẫu nhiên (`:349`) nhưng RHT không đọc. |
| `rcd`, `mmrcd` | `RE:RCAEval/e2e/rcd.py:449-462` | Nhân quả | Chia normal/anomal theo `inject_time`. Cần Python 3.8 riêng (`RE:main.py:133-134`). |
| `torai` | `RE:RCAEval/e2e/torai.py:69` | Đa nguồn, nhân quả, không dùng đồ thị gọi | Cắt theo `inject_time` (`torai.py:84-112`). Import từ `rcd` nên cần môi trường Python 3.8. Có tham số `service`, `fault_type`, `case` trong chữ ký nhưng thân hàm không đọc (các chỗ có chữ "service" là biến cục bộ `service_list`, `service_ranks` từ dòng 238); runner không truyền (`RE:main.py:408-417`). |
| `tracerca` | `RE:RCAEval/e2e/tracerca.py:45-95` | Trace, không đồ thị | **Bản rút gọn**: span bất thường nếu `duration ≥ mean + 3·std` của operation (`tracerca.py:61`); xếp hạng theo trung bình điều hòa của support và confidence (`:64-84`). Khác xa bản gốc (mục 2). |
| `microrank` | `RE:RCAEval/e2e/microrank.py:646-711` | Trace + PageRank | Luật span `mean + 3·std` (`microrank.py:666-667`) **chỉ đổi hai số đếm trace** (`:697-698`): đồ thị "bình thường" dựng từ mọi span trước mốc tiêm (`:673`), đồ thị "bất thường" từ mọi span sau mốc (`:684`). Bản gốc dựng đồ thị và đếm trên cùng hai tập trace (`MK:online_rca.py:212-242`). Dòng `:626` so tên operation với khóa traceID nên luôn đúng; cạnh operation–operation bị đặt lại ở mọi span (bản gốc tích lũy cạnh: `MK:preprocess_data.py:436-462`). Cạnh này vào PageRank với hệ số 0,01 (`:20, 28-30`); tác động lên thứ hạng **chưa kiểm** (cần chạy, thuộc hồ sơ P1). PageRank `d=0.85` (`:20`); phổ `dstar2` (`:702`). Chỉ trả tối đa 11 operation, ở mức operation (`:443, 699`; bản gốc cũng vậy: `MK:online_rca.py:149, 239`). |
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
| SimpleRCA | `LGU-SE-Internal/Simple-RCA` (submodule của `OperationsPAI/rca-algo-contrib`) | Không có LICENSE | Nhiều nhánh, không nhánh nào khớp mô tả bài; xem mục 3a dòng 3. |
| Eadro | `BEbillionaireUSD/Eadro` | Không có LICENSE | `main.py:89-90` gọi `chunkDataset(train_chunks, node_num)` nhưng hàm khởi tạo đòi thêm `edges` (`main.py:5`) → **không chạy được nếu không sửa**. Chia train/test bằng `np.random.shuffle` trên chunk (`preprocess/align.py:131-138`), không theo thời gian; nhãn chunk = service gốc nếu chunk trùng khoảng lỗi (`align.py:18-31`). Chọn checkpoint theo HR@1 trên test (`base.py:102-105`). Tự lùi về CPU (`main.py:62-67`). Bài SimpleRCA cũng nhận xét độ chính xác cao của Eadro "chủ yếu do trùng mẫu giữa tập train và test" (bài SimpleRCA, văn bản dòng 611). |
| MicroRCA | `elastisys/MicroRCA` | Không có LICENSE | Là script chạy trên file CSV đặt tên theo `faults_name` (`MicroRCA.py:53-70`). Cần: độ trễ theo cạnh gọi nguồn/đích (`:53, 57`), file đồ thị service–host `_mpg.csv` (`:70`), metric container `ctn_*` và host `node_*` (`:112, 127`). BIRCH `threshold=0.045`, làm trơn 12 điểm (`:16, 276`); `alpha=0.55` (`:275`); PageRank `alpha=0.85` (`:255`). Dùng `iteritems` đã bị pandas 2 bỏ (`:25`). Đường nhãn: xem mục 4. Ví dụ: RCAEval, một ứng viên của P2, không có metric host hay quan hệ service–host (mục 8.3). |
| MicroRank (gốc) | `IntelligentDDS/MicroRank` | MIT | Báo động hệ thống khi số trace vượt `μ+1.5σ` lớn hơn 8 (`MK:anormaly_detector.py:62, 70`); chia trace bình thường/bất thường bằng `μ+σ` cộng 50 ms (`:93-102`). Phổ mặc định `dstar2` (`MK:online_rca.py:242`), không phải Ochiai như K1 ghi. Đọc trace từ Elasticsearch (`MK:preprocess_data.py:9-14`). |
| TraceRCA (gốc) | `NetManAIOps/TraceRCA` | Không có LICENSE | Quy trình nhiều bước qua Makefile: chọn đặc trưng theo từng cặp gọi (`TR:run_selecting_features.py:52-80`), phát hiện 3σ trên các đặc trưng đã chọn (`TR:run_anomaly_detection_invo.py:38-59`), khai phá luật kết hợp (`SUPPORT=0.1`, `K=100`, `TR:Makefile:22-25`). Nhãn service gốc chỉ dùng ở bước chấm (`TR:run_localization_collect.py:79-80`). Bản RCAEval chỉ giữ ý tưởng support/confidence. |
| PDiagnose | Không có | — | Bài RCAEval và bài TORAI đều ghi "source code is unavailable" và tự cài (bài RCAEval, văn bản dòng 488; bài TORAI, dòng 249). |
| DeepTraLog | `FudanSELab/DeepTraLog` | Không có LICENSE | Chỉ có mô hình và dữ liệu đồ thị đã dựng sẵn (`DT:model/dataset.py:64-74` đọc JSON đồ thị). **Không có code dựng đồ thị trace–log từ dữ liệu thô** và không có code tạo embedding sự kiện. Tự lùi về CPU (`DT:model/main.py:40`). |
| GDN | `d-ailin/GDN` | MIT | Mặc định `report='best'` (`GD:main.py:216`, `run.sh`): chọn ngưỡng tối đa F1 **trên nhãn test** (`GD:evaluate.py:141-144`). Chế độ `val` dùng ngưỡng = điểm cao nhất trên dữ liệu bình thường (`GD:evaluate.py:109`), khớp bài về cách đặt ngưỡng; điểm kiểm định chuẩn hóa bằng thống kê của chính tập kiểm định, điểm test bằng thống kê của tập test (`GD:evaluate.py:20-21, 52`; bổ sung theo T-018). Thiết bị chọn được (`GD:main.py:208`). |
| SPOT/DSPOT | Repo gốc `Amossys-team/SPOT` trả 404 | `ads-evt` (PyPI 0.0.4): GNU GPLv3 | `limjcst/ads-evt` nói là bọc nguyên bản và có test so khớp. Một bản sao khác nằm ở `RE:RCAEval/e2e/microcause.py:2095`, nhưng không được gọi (`:2190` bị comment). |
| CIRCA (gốc) | `NetManAIOps/CIRCA` | BSD-3-Clause | Có lớp `StructuralGraph` (`circa/graph/structural.py:169`) để chạy với đồ thị cấu trúc. Bài PRISM nói đã dựng và công bố đồ thị phụ thuộc cho các hệ trong RCAEval (bài PRISM, văn bản dòng 254); chưa kiểm tải được. |
| RCD (gốc) | `azamikram/rcd` | MIT | Hướng dẫn viết cho Ubuntu, Python 3.8, phải vá thư viện bằng symlink (`README.md:5-41`). Trên Windows: mọi gói ghim đều có wheel cp38 (mục 8.3); `RE:script/link.sh` dùng đường dẫn Linux, phải chép tay 5 file vá. Chưa cài thử. |

## 3. Bảng ứng viên

"Biết trước thời điểm?" = có cần mốc sự cố từ bên ngoài. "Nhãn để học?" = có cần nhãn nguyên nhân hay nhãn bất thường để huấn luyện (khác với nhãn chỉ để chấm).

### 3a. Phương pháp RCA (đủ 11 ứng viên của MRP P1)

| # | Phương pháp | Họ | Bài toán | Đầu vào | Biết trước thời điểm? | Nhãn để học? | Code, giấy phép, CPU | Bài gần đây dùng (mục 6) | Quyết định (bản 3) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **BARO** | Thống kê trên metric | Phát hiện (BOCPD) + xếp hạng | Metric | Bản RE: có. Bản BR: BOCPD tự tìm mốc | Không | RE + BR, MIT, CPU | RCAEval, TORAI, SimpleRCA, DecompRCA, PRISM | **Chọn.** Mạnh, rẻ, có mặt ở cả 5 bài. Chạy hai chế độ: biết trước thời điểm (bản RE) và tự phát hiện (BOCPD, bản BR). |
| 2 | **N-Sigma** | Thống kê trên metric | Xếp hạng (bản BR: cả phát hiện) | Metric | Có (`RE:__init__.py:110-112`) | Không | RE + BR, MIT, CPU | Detector baseline trong bài BARO (K1 §C.4) | **Biến thể đối chứng của BARO, không viết hồ sơ riêng.** Chỉ khác bộ chuẩn hóa (`__init__.py:137` so với `baro.py:49`). |
| 3 | **SimpleRCA** | Luật đơn giản, đa nguồn | Xếp hạng | Metric, log, trace + dữ liệu bình thường | Bài: so với dữ liệu bình thường trong cửa sổ sự cố; cách cắt cửa sổ bài không nêu (chưa kiểm). CLI mặc định `orig` đọc sáu bảng normal/abnormal đã chia sẵn (`SR:src/simplerca/nezha_adapter.py:26-42`); chưa xác minh cách tạo cửa sổ đó độc lập với nhãn. Lớp SimpleRCA riêng mới lấy đầu/cuối cửa sổ lỗi từ nhãn (`SR:src/simplerca/adapter.py:49-51`) | Không | Không có code khớp bài (mức M4, mục 8.2). SR không có LICENSE. CPU | Chính bài FSE'26 | **Chọn, chỉ bản nhóm cài lại theo mô tả bài** (bài SimpleRCA, văn bản dòng 228-234): metric vượt 3σ hoặc P95 lịch sử; trace P95 gấp ~3 lần lúc bình thường; số dòng log chứa từ khóa lỗi vượt một ngưỡng; xếp service theo số cảnh báo. **Bài để ngỏ tham số:** 3σ hay P95; bội số trace (bài ghi "ví dụ 3x"); ngưỡng số dòng log lỗi ("định trước", không nêu giá trị); cách cắt cửa sổ. Đây là lựa chọn của nhóm, phải có mục WHY và chốt trước khi xem kết quả dev (luật cứng 3). Tên dùng trong báo cáo: "SimpleRCA (cài lại theo mô tả bài)". Vì sao chọn: là phép thử "dataset có quá dễ không" và baseline không đồ thị mạnh (LESSONS QT7). **Không nhánh code nào của tác giả khớp mô tả bài:** (1) CLI mặc định `orig` đăng ký `NezhaRCA` (`SR:main.py:11`): metric CPU/mem max > 1,19×P95 normal và >80 (`nezha_rca.py:105-162`); trace P90 tuyệt đối >100ms (`:215-258`); top5 mỗi modality cộng điểm theo hạng5-i, trọng số metric1,2 và trace/log1 (`:69-93`). Lớp SimpleRCA riêng không được CLI đăng ký vẫn có metric6σ và trọng số100/50/20 (`src/simplerca/main.py:304-381`); đó là đường code khác, chưa xác định đường nào sinh bảng2; (2) nhánh `rcaeval`: tên `simplerca` gán cho `NezhaRCA` (`main.py:12`). Hàm `baro()` ở đây trùng logic `RE:baro.py` (đã so diff). Điểm service = max điểm metric, chỉ lấy top-5 (`nezha_rca.py:49, 66-90`); phiếu trace/log chỉ cộng cho top-3 của BARO (`:133, 151, 158`). Hệ quả: service gốc ngoài top-3 của BARO không thể lên Top@1, ngoài top-5 thì không có trong kết quả; (3) nhánh `rcaeval_re3_ss` bật `dk_select_useful=True` riêng cho dataset `rcaeval_re3_ss` (`nezha_rca.py:54`). Ngoài cờ, `time_series.py:101` đổi kiểm hậu tố `ss` thành `sock-shop`, làm tên `rcaeval_re3_ss` đi qua chuỗi drop_constant/convert_mem và các bước lọc khi bật dk_select_useful (`:103-110`); chưa định lượng ảnh hưởng lên accuracy. Artifact Zenodo 17105974 không chứa code SimpleRCA. → Chưa biết bảng 2 (RE2-TT 0,80) sinh từ code nào. Biến thể (2) **không có trong danh sách**. Nếu cần thử tái lập con số 0,80, gọi đúng tên "BARO + phiếu trace/log (code nhánh `rcaeval`)" và chỉ dùng như một phép kiểm. |
| 4 | **RCD** | Nhân quả | Xếp hạng metric | Metric (đa nguồn: `mmrcd`) | Có (`RE:rcd.py:461-462`) | Không (cần chia normal/anomal) | RE + gốc, MIT, CPU; Python 3.8 | RCAEval, TORAI, DecompRCA | **Biến thể đối chứng của TORAI, không có hồ sơ riêng** (Minh duyệt 02/10). TORAI và RCD dùng chung lõi nhân quả `run_multi_phase` (`RE:torai.py:12-16, 312`) nhưng **khác nhiều bước**: gom cụm, nguồn tín hiệu, giảm mẫu, cách ra thứ hạng cuối (mục 3a dòng 9; mục 8.1). Chênh lệch giữa hai bên không quy riêng cho một bước. |
| 5 | **CIRCA** | Nhân quả + đồ thị | Xếp hạng metric | Metric + đồ thị + mốc phát hiện | Có (`RE:rht.py:362`) | Không | RE (BSD-3) + gốc (BSD-3), CPU; thời gian chạy PC trên hàng trăm metric: chưa kiểm | RCAEval, TORAI, DecompRCA | **Chọn.** Là phương pháp duy nhất trong danh sách mà đồ thị đi vào phép tính điểm (parent set; K1 §D.2 mẫu E). **Chạy cả hai biến thể đồ thị** (Minh duyệt 02/10): PC (bản RCAEval, chỉ RHT) và kiến trúc (đồ thị gọi + luật gán metric vào T/S/L/E định nghĩa theo schema từng dataset; mục 8.1). Dùng RHT hay RHT + DA: để mở cho hồ sơ P1. |
| 6 | **MicroRank** | Trace + PageRank | Phát hiện trace + xếp hạng operation | Trace | Có (`RE:microrank.py:654-658`) | Không | RE (MIT) + MK (MIT), CPU; cần tự viết adapter đọc trace (mục 1) | RCAEval, TORAI, SimpleRCA | **Chọn.** Đại diện họ dựa trên trace và lan truyền trên đồ thị: PageRank chạy trên đồ thị dựng từ trace. Code RE chỉ giống MK ở hàm PageRank và công thức phổ `dstar2`; phần dựng đầu vào có hai sai lệch (mục 1). Sửa bản RE hay dùng hàm của bản gốc qua adapter: để mở cho hồ sơ P1. Cả hai bản chỉ trả tối đa 11 operation; MRR, NDCG cần thứ hạng đầy đủ ở mức service. |
| 7 | **TraceRCA** | Trace, không đồ thị | Phát hiện span + xếp hạng | Trace | Có (`RE:tracerca.py:53-54`) | Không | RE (MIT, bản rút gọn), CPU; cùng adapter trace với MicroRank. Bản TR gốc không có LICENSE, cần dữ liệu dạng riêng | RCAEval, TORAI | **Biến thể đối chứng của MicroRank, không viết hồ sơ riêng.** Dùng bản RE, ghi rõ "bản rút gọn của RCAEval". Vai trò: đối chứng không dùng PageRank cho MicroRank. Hai bản RE dùng cùng công thức `μ+3σ` (`tracerca.py:61`, `microrank.py:667`) nhưng **vai trò khác nhau**: ở TraceRCA luật quyết định span nào bất thường; ở MicroRank RE nó không quyết định trace nào vào đồ thị (mục 1). TraceRCA RE trả đủ danh sách, MicroRank tối đa 11 operation. Vì vậy chênh lệch giữa hai bên không quy riêng cho PageRank, cho tới khi hồ sơ P1 thống nhất tập trace và đầu ra. Không dùng làm đại diện cho TraceRCA gốc. |
| 8 | **MicroRCA** | Lan truyền trên đồ thị (PPR trên đồ thị con bất thường) | Phát hiện cạnh (BIRCH) + xếp hạng service | Độ trễ cạnh gọi, metric container và host, đồ thị service–host | Không; BIRCH chạy trên cả chuỗi của lần chạy | Không | MR, **không có LICENSE**, CPU; phải cài lại vì code là script gắn với file CSV riêng | SimpleRCA | **Không chọn; dự phòng.** Lý do: (a) ưu tiên chiều sâu (Q-37); (b) code không có LICENSE, là script gắn với file CSV riêng, phải cài lại; (c) script gốc dùng nhãn (L5, L6). Yêu cầu dữ liệu nếu dùng lại: độ trễ theo cạnh gọi, metric container và metric host, quan hệ service–host; P2 ghi dataset nào có. Dùng lại nếu P4 cần prior work cho "đồ thị con bất thường". |
| 9 | **TORAI** | Đa nguồn, nhân quả, không đồ thị gọi | Xếp hạng service và chỉ báo | Metric, log, trace dưới dạng chuỗi thời gian | Có (`RE:torai.py:84`; bài: cần `t_A` từ bộ phát hiện ngoài) | Không | RE, MIT, CPU; Python 3.8 | Chính bài FSE'26 | **Chọn.** Đối chứng trực tiếp cho câu hỏi "có cần đồ thị gọi không". Hồ sơ giải thích cả lõi RCD (RCD là biến thể đối chứng). **Đã kiểm ở T-016:** TORAI giảm mẫu metric còn 1/15 hai lần (`RE:torai.py:29, 81, 295`) và ghép metric với chuỗi log theo chỉ số dòng (`:47-48`). Với `--length 10` (`RE:docs/TORAI.md:51`) và dữ liệu 1 điểm/giây, nửa lỗi chỉ còn 1 dòng metric nên mọi cột metric bị bỏ vì hằng; lõi RCD chỉ nhận cột log, mỗi nửa thêm 1 dòng giả toàn 0 do ghép theo chỉ số (đã kiểm ở T-016, `results/T-016/giam-mau-hai-lan.md`). Lõi RCD chỉ sắp lại trong cụm có ≥2 service, không đủ thì lùi về thứ tự mức nghiêm trọng (`:283-335`). `torai.py` ở nhánh `fse26` giống nhánh `main`. Kiểm bằng chạy một ca ở hồ sơ P1, vì T-001 không chạy phương pháp (SPEC "Không làm"). Rủi ro: cùng nhóm tác giả với RCAEval (mục 7). Cần chuỗi thời gian log và trace dựng từ log/trace thô; RCAEval không kèm code dựng (ví dụ về RCAEval ở mục 8.3). |
| 10 | **Eadro** | Học có đồ thị (GAT), có giám sát | Phát hiện cửa sổ + xếp hạng service | Log, KPI, trace + đồ thị gọi lịch sử | Không (phân loại cửa sổ) | **Có**: nhãn cửa sổ + service gốc | EA, **không có LICENSE**; code không chạy được nếu không sửa; torch + dgl; CPU được, thời gian chưa kiểm | SimpleRCA | **Không chọn; dự phòng.** Có giám sát nên không xếp chung bảng với phương pháp không giám sát. Code lỗi (`main.py:89-90`); chia ngẫu nhiên và chọn checkpoint trên test (L7); cần môi trường riêng (Python 3.8, torch 1.12.1, dgl 0.9.1, tick 0.7.0.1: đều có wheel Windows, chưa cài thử). Dùng lại nếu P4 cần prior work cho "GNN dùng trong RCA". |
| 11 | **PDiagnose** | Đa nguồn, luật bỏ phiếu | Xếp hạng | Metric, log, trace | Có | Không | Không có code gốc; RE có script sai cửa sổ log (mục 1) | RCAEval, TORAI (cả hai tự cài) | **Không chọn.** Không có code gốc, nên kết quả chỉ phản ánh bản cài lại của người cài. Vai trò "luật bỏ phiếu đa nguồn" đã có SimpleRCA. |

### 3b. Bộ phát hiện bất thường (Q-30)

| # | Bộ phát hiện | Họ | Đơn vị | Đầu vào | Nhãn để học? | Code, giấy phép | Quyết định (bản 3) |
|---|---|---|---|---|---|---|---|
| D1 | **BOCPD** (BARO) | Điểm thay đổi Bayes | Thời điểm | Cột latency/error | Không | `BR:anomaly_detection.py:77-151`, MIT | **Chọn.** Cho BARO chế độ tự phát hiện. Phải sửa hai chỗ để không dùng dữ liệu tương lai và nhãn: chuẩn hóa chỉ trên phần đã thấy; chạy trên cửa sổ trượt, không cắt quanh mốc tiêm. Cách BARO gốc chấm BOCPD không chuẩn: một ca là TP nếu có bất kỳ điểm thay đổi nào, là FP nếu điểm đầu tiên trước điểm 300 (`BR:baro/reproducibility.py:168-181`). Số P/R/F1 BOCPD đã công bố không so được với cách chấm của MRP P3. |
| D2 | **N-Sigma** | Thống kê | Thời điểm | Metric | Không | `BR:anomaly_detection.py:7-35`, MIT | **Chọn.** Bộ phát hiện đơn giản nhất. |
| D3 | **SPOT/DSPOT** | Cực trị (EVT) | Thời điểm | Chuỗi đơn biến | Không | `ads-evt` (GPLv3) | **Không dùng** (Minh duyệt 02/10); dự phòng nếu P4 cho thấy cách đặt ngưỡng của N-Sigma là nguồn lỗi chính. Đại diện ngưỡng EVT; ARMOR cũng dùng POT (K1 §C.12). Dùng `ads-evt` vì có test so với bản gốc. Không chép code GPL vào repo. |
| D4 | **Luật trace** | Thống kê trên trace | Span hoặc trace | Trace | Không | `RE:tracerca.py:61` (`μ+3σ` theo span); `MK:anormaly_detector.py:62, 93-102` (theo trace) | **Đi kèm MicroRank/TraceRCA**, không tốn thêm. Chấm riêng phần phát hiện. |
| D5 | **GDN** | GNN trên đồ thị học được, dự báo | Thời điểm + chuỗi lệch | Chuỗi metric | Không (học trên dữ liệu bình thường) | `GD`, MIT; CPU chưa kiểm | **Chọn** (Q-37; Minh xem lại và giữ ngày 03/10). Task đo kiểm khả thi; không đạt thì ghi lý do theo WHY-10. Đại diện duy nhất của GNN trong danh sách, có code đầy đủ. Bắt buộc dùng `report='val'`, và chuẩn hóa điểm lỗi bằng thống kê lấy từ dữ liệu trước thời điểm chấm: code gốc chuẩn hóa điểm test bằng trung vị/IQR của cả tập test (`GD:evaluate.py:16-21, 48-60`; `GD:util/data.py:75-82`). Điều kiện: đủ dữ liệu bình thường để học (MRP §4 tiêu chí 8, phụ thuộc P2). Rủi ro: bài chỉ đánh giá trên dữ liệu cảm biến (K1 §C.11). |
| D6 | BIRCH | Phân cụm | Cạnh gọi | Độ trễ cạnh | Không | `MR:MicroRCA.py:19-46` | Không (MicroRCA không chọn). |
| D7 | Đầu nhị phân Eadro | GNN có giám sát | Cửa sổ | Đa nguồn | Có | `EA` | Không (Eadro không chọn). |
| D8 | **DeepTraLog** | Đồ thị trace–log + GGNN | Trace | Span + log gắn vào span | Không (một lớp) | `DT`, không có LICENSE; **thiếu code dựng đồ thị** | **Không chọn.** Đại diện duy nhất của mẫu "đồ thị là đối tượng bị chấm" (K1 §D.2 mẫu D). Nhưng phải tự viết bộ dựng đồ thị và embedding, và cần log có trace ID; P2 ghi dataset nào có. |

## 4. Đường nhãn và dữ liệu tương lai đã thấy trong code (đã kiểm)

Phục vụ luật cứng 6 và câu hỏi G1 "có đường nào để nhãn lọt vào phương pháp". Mỗi dòng ghi cách chặn trong adapter của nhóm.

| # | Ở đâu | Cái gì lọt vào | Cách chặn |
|---|---|---|---|
| L1 | `RE:main.py:283, 340-363` | Tên service gốc lấy từ tên thư mục ca → chọn SLI → MicroCause, EasyRCA, CloudRanger dùng SLI khi xếp hạng | Không dùng ba phương pháp này; nếu dùng, chọn SLI từ cấu hình cố định (ví dụ cổng vào) |
| L2 | `RE:main.py:311-315` | Cửa sổ dữ liệu cắt đối xứng quanh mốc tiêm lỗi | Chế độ (a) "biết trước thời điểm": hợp lệ, và phải ghi rõ. Chế độ (b): cắt cửa sổ độc lập với nhãn |
| L3 | `BR:reproducibility.py:133-137, 168-181`; `BR:anomaly_detection.py:120-127` | Khi chấm BOCPD, cửa sổ cắt quanh mốc tiêm; chuẩn hóa dùng cả phần tương lai; cách chấm đã công bố tính TP cho mọi ca có điểm thay đổi | Cửa sổ trượt; chuẩn hóa theo phần đã quan sát; chấm theo cửa sổ thời gian (MRP P3) |
| L4 | `SR:src/simplerca/adapter.py:41-51, 120-126` | DataAdapter của lớp SimpleRCA riêng, không phải adapter CLI orig: đọc fault_type và truyền vào hàm (hàm không dùng); fault_start/end chia cửa sổ lỗi | Cài lại không có tham số `fault_type`; cửa sổ theo chế độ (a)/(b) như mọi phương pháp |
| L5 | `MR:MicroRCA.py:297-298` | Ngưỡng BIRCH đổi theo service gốc và loại lỗi (`payment`, `shipping` dùng 0.02) | Một ngưỡng cố định cho mọi ca, chọn trên dev |
| L6 | `MR:MicroRCA.py:327` | Danh sách ứng viên lọc theo các service bị tiêm lỗi (`targets`) | Ứng viên = mọi service quan sát được |
| L7 | `EA:base.py:102-105`; `EA:preprocess/align.py:131-138` | Chọn checkpoint trên test; chia ngẫu nhiên nên các chunk liền nhau của cùng một lần lỗi nằm cả ở train lẫn test | Chia theo ô (MRP §4); checkpoint chọn trên dev |
| L8 | `GD:main.py:216`; `GD:evaluate.py:16-21, 48-60, 141-144` | Ngưỡng phát hiện chọn theo F1 trên nhãn test; điểm test chuẩn hóa bằng trung vị/IQR của cả tập test (dữ liệu đo tương lai, không phải nhãn) | Dùng `report='val'`; thống kê chuẩn hóa lấy từ dữ liệu trước thời điểm chấm, giữ cố định hoặc chỉ cập nhật bằng quá khứ |
| L9 | Bài PRISM, văn bản dòng 253 | Với phương pháp có ngưỡng, bài báo báo kết quả tốt nhất qua nhiều ngưỡng | Không dùng số của bài làm mốc so sánh |

Không thấy đường nhãn ở: `torai` (tham số có nhưng không đọc), TraceRCA gốc (nhãn chỉ ở bước chấm), `baro`/`nsigma`/`rcd`/`circa` của RCAEval ngoài L2.

## 5. Phương pháp trong RCAEval hoặc K1 nhưng không có trong ứng viên MRP

| Phương pháp | Lý do | Thuộc phương án |
|---|---|---|
| MicroCause, EasyRCA, CloudRanger | Cần SLI (L1). Họ nhân quả đã có RCD, CIRCA | Không |
| PC-PageRank (và `*_pagerank`, `*_randomwalk`) | Chạy sẵn qua `main.py`. DecompRCA và PRISM dùng làm baseline. PageRank chạy trên đồ thị nhân quả học từ metric, không phải đồ thị gọi | B (thay MicroRCA), C |
| mmBARO, mmRCD, mmCIRCA | Biến thể đa nguồn của 1, 4, 5; gần như miễn phí; không tính vào số đếm | A, B, C |
| CausalRCA | Nhân quả học sâu; bài TORAI và SimpleRCA dùng; chạy qua `main.py` (cần torch) | C |
| Nezha | Đa nguồn, khác nhóm tác giả; bài SimpleRCA dùng. Bài TORAI ghi Nezha cần trace ID trong từng dòng log (bài TORAI, văn bản dòng 249); P2 ghi dataset nào có | C, có điều kiện dữ liệu |
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

Nguồn từng cột: bài RCAEval, văn bản dòng 488; bài TORAI, dòng 230; bài SimpleRCA, dòng 861-865; bài DecompRCA, dòng 493-500; bài PRISM, dòng 200-252. N-Sigma, SimpleRCA và TORAI không có cột vì chúng là phương pháp của chính các bài. DecompRCA dùng RCD, ε-Diagnosis của PyRCA và CIRCA gốc (RHT + DA), không phải bản RCAEval; chỉ BARO chạy qua RCAEval (bổ sung theo T-018, `results/T-018/decomprca.md` K12).

## 7. Nhận định dựa trên kết quả đã công bố, và nguyên nhân khả thi khác (Q-33)

| Nhận định | Nguyên nhân khả thi khác |
|---|---|
| SimpleRCA đạt Top@1 0,80 trên RE2-TT, BARO 0,67 (bài SimpleRCA, bảng 2) → SimpleRCA là baseline mạnh | (a) Số của BARO lấy từ bài gốc, không chạy lại (bài SimpleRCA, văn bản dòng 607), nên hai số có thể khác giao thức. (b) Nếu số sinh từ code nhánh `rcaeval` thì "SimpleRCA" ở đó = BARO cộng phiếu, và phần hơn có thể chỉ do xếp lại trong top-3 của BARO. Nếu sinh từ nhánh `rcaeval_re3_ss` thì có cấu hình riêng cho RE3-SS. Không có code nào khớp mô tả bài (mục 3a, dòng 3). (c) RE2-TT có 5 service gốc và đồ thị gần như không đổi (LESSONS ST3). (d) Luật có thể đã được chỉnh trên chính các benchmark này. → Chỉ dùng để chọn SimpleRCA làm ứng viên, không dùng để kết luận. |
| BARO, RCD, CIRCA xuất hiện ở hầu hết bài → "baseline chuẩn" | Có thể vì chúng sẵn trong RCAEval. RCAEval, TORAI, DecompRCA, PRISM có chung tác giả Luan Pham, nên tần suất không độc lập. |
| TORAI hơn chín baseline | Benchmark của chính nhóm tác giả; chế độ biết trước `t_A`; ba baseline trace không có code chạy công bố (mục 1); baseline cần SLI có thể đã nhận SLI từ nhãn (L1); `torai.py` nhánh `fse26` giống nhánh `main`, nên nếu bài chạy code này thì hiện tượng giảm mẫu và ghép theo chỉ số (mục 3a dòng 9) nằm trong số đã công bố. |
| SimpleRCA đo được "dataset có quá dễ không", vì bài xếp 0,86 số ca vào Type I+II | Tỷ lệ Type do luật phân loại riêng của tác giả, xét metric liên quan lỗi hoặc số log lỗi so với ngưỡng (PDF FSE §3.2.3, trang8–9). Riêng nhận xét RE3-OB, tác giả nói chỉ đếm error entries; không khái quát sang mọi dataset. Tỷ lệ này không do SimpleRCA. Điểm của bản cài lại còn phụ thuộc tham số nhóm chọn (mục 3a dòng 3) và chế độ biết trước thời điểm. |
| Eadro mạnh trong bài gốc | Chia ngẫu nhiên và chọn checkpoint trên test (L7). Bài SimpleRCA cũng nêu chuyện trùng mẫu train/test. |
| MicroRCA đạt Precision@1 khoảng 89% (K1 §C.2) | Ngưỡng chỉnh theo service gốc, ứng viên lọc theo service bị tiêm (L5, L6). |
| GDN F1 0,81 trên SWaT (K1 §C.11) | Bài ghi ngưỡng = max điểm trên tập kiểm định (tương ứng `report='val'`), nhưng code chuẩn hóa điểm test bằng trung vị/IQR của cả tập test ở mọi chế độ (L8), và không có log hay dữ liệu để biết bảng sinh từ chế độ nào (bổ sung theo T-018, `results/T-018/ho-so-gdn.md` mục 8.1; Minh duyệt 04/10). |

## 8. Danh sách đã chốt (Minh, 02/10/2026)

Hai lần chốt:
- **Q-37**: "tôi chốt là làm gọn lại nhé".
- **Sau đó** (**Q-38**): bỏ SPOT; CIRCA chạy cả hai biến thể đồ thị; RCD thành biến thể đối chứng của TORAI; lượt đo môi trường và thời gian chạy tách thành task riêng.

Danh sách này ít hơn mức "ước lượng 8–12 phương pháp RCA" ở MRP P1 (`docs/MRP.md:132`) và SPEC (`SPEC.md:10`). Đây là quyết định của Minh.

Mức code M1–M4 định nghĩa ở mục 8.2. "Biến thể đối chứng" là phương pháp gần như giống phương pháp chính, chỉ khác đúng một bước. Chạy cả hai thì biết riêng bước đó có tác dụng không. N-Sigma đúng nghĩa này. TraceRCA và RCD khác phương pháp chính nhiều bước; với hai cặp này, chênh lệch không quy riêng cho một bước (bảng biến thể ở dưới). Biến thể không có hồ sơ riêng; hồ sơ của phương pháp chính có thêm một đoạn "biến thể khác ở bước X".

### 8.1. Danh sách

**Phương pháp RCA có hồ sơ đầy đủ (5):**

| Phương pháp | Giúp trả lời câu hỏi gì | Mức code | Môi trường |
|---|---|---|---|
| BARO | Baseline thống kê mạnh, có mặt ở 5/5 bài gần đây (mục 6). Kèm BOCPD cho chế độ tự phát hiện | M1 | Python 3.12 |
| SimpleRCA (cài lại theo mô tả bài) | Dataset có quá dễ không. Bài SimpleRCA xếp 0,86 số ca của các benchmark cũ vào Type I+II; tỷ lệ này khác nhau giữa các dataset (bảng 3 của bài). Tỷ lệ này do luật phân loại riêng của bài, không phải do SimpleRCA (mục 7). Đồng thời là baseline không đồ thị cho RQ3 | M4 | Python 3.12 |
| CIRCA, **cả hai biến thể đồ thị** | Đồ thị đi thẳng vào phép tính điểm. Chênh lệch giữa hai biến thể chỉ là **gợi ý** về vai trò của nguồn đồ thị, chưa phải bằng chứng cho RQ3d: hai biến thể khác nhau nhiều thứ cùng lúc (PC học từ chính ca đó gồm cả đoạn sau sự cố; luật gán T/S/L/E; mật độ cạnh; DA). Đối chứng của RQ3d là đồ thị ngẫu nhiên giữ bậc (MRP §6) | PC chỉ RHT: M1. Thêm DA, hoặc đồ thị kiến trúc: M2 | Python 3.12 |
| MicroRank | Trace + PageRank trên đồ thị dựng từ trace. Bản RE có hai sai lệch ở phần dựng đầu vào (mục 1) | M2: cần sửa code RE hoặc adapter cho hàm gốc | Python 3.12 |
| TORAI | Đa nguồn, không dùng đồ thị gọi. Hồ sơ phải giải thích cả lõi RCD, vì TORAI gọi `run_multi_phase` của RCD trong từng cụm service (`RE:RCAEval/e2e/torai.py:12-16, 312`) | M2 | Python 3.8 |

**CIRCA hai biến thể** dự định dùng cùng cách chấm điểm, chỉ khác nguồn đồ thị. Bản PC hiện có chỉ chấm bằng RHT (hồi quy theo nút cha), không có DA (chỉnh theo nút con cháu). Dùng RHT hay RHT + DA: để mở cho hồ sơ P1. Nếu thêm DA: số CIRCA đã công bố là bản chỉ RHT; trên đồ thị PC, cạnh vô hướng thành hai cạnh ngược chiều (`RE:rht.py:318-323`), nên DA chưa chắc cho cùng cách chấm trên hai loại đồ thị (chưa kiểm; cần chạy, thuộc hồ sơ P1).
- **PC**: bản RCAEval, đồ thị học từ dữ liệu của chính ca đó (`RE:circa.py:33`).
- **Kiến trúc**: như bài gốc. Đồ thị gọi giữa service dựng từ trace. Mỗi metric gán vào Traffic/Saturation/Latency/Errors theo luật định nghĩa riêng cho schema của từng dataset (ví dụ với tên cột của RCAEval: workload→T; cpu, mem, socket, diskio→S; latency→L; error→E). Luật cạnh giữa các loại lấy theo cấu hình của CIRCA (`CIRCA:circa/graph/structural.py:169`; ví dụ `tests/alg/sgraph/index.yml`).
- Cả hai cách dựng đều không dùng nhãn.

**Biến thể đối chứng, không có hồ sơ riêng (3):**

| Biến thể | Của | Khác ở bước | Mức code |
|---|---|---|---|
| N-Sigma | BARO | Chuẩn hóa bằng trung bình/độ lệch chuẩn thay cho trung vị/IQR | M1 |
| TraceRCA bản RCAEval | MicroRank | Xếp hạng bằng support/confidence, không dùng PageRank. Khác thêm: vai trò của luật μ+3σ và độ dài đầu ra (mục 3a dòng 7) | M2 |
| RCD | TORAI | Dùng chung lõi nhân quả nhưng khác nhiều bước: không gom cụm, chỉ metric, không giảm mẫu, ra thứ hạng metric thay cho service (mục 3a dòng 9) | M1, Python 3.8 |

**Bộ phát hiện (Q-30):**
- BOCPD (M1): phải sửa chuẩn hóa và cách cắt cửa sổ (L3).
- N-Sigma (M1): phải chọn cột chạy.
- GDN (M2: phải chuyển dữ liệu, lấy phần giao cột, dùng `report='val'`). Minh giữ ngày 03/10; task đo kiểm khả thi.
- Luật trace (μ+3σ theo span, và luật của MicroRank gốc): đi kèm MicroRank.
- SPOT: **không dùng**.

**Phủ các họ của MRP P1** (tiêu chí của MRP, không phải yêu cầu của cô):

| Họ | Đại diện |
|---|---|
| Thống kê trên metric | BARO (+ N-Sigma) |
| Nhân quả | CIRCA, TORAI (+ RCD) |
| Dựa trên trace | MicroRank (+ TraceRCA bản RCAEval) |
| Lan truyền trên đồ thị | MicroRank (PageRank) |
| Đa nguồn | SimpleRCA, TORAI |
| Học có đồ thị | Chỉ có ở phần phát hiện (GDN). **Không có đại diện cho RCA.** Lý do: ứng viên duy nhất là Eadro, mà Eadro có giám sát, code lỗi, chia ngẫu nhiên và chọn checkpoint trên test (L7), chi phí môi trường cao. Giữ làm dự phòng |

**Dự phòng**, dùng lại nếu P4 cần:
- MicroRCA: prior work cho "đồ thị con bất thường"; cần dataset có metric host.
- Eadro: prior work cho "GNN dùng trong RCA".
- SPOT: nếu P4 cho thấy cách đặt ngưỡng của N-Sigma là nguồn lỗi chính.

**Chưa chọn:** mmBARO, mmRCD, mmCIRCA (mức M2, cần chuỗi log/trace như TORAI); PC-PageRank; PDiagnose; DeepTraLog.

### 8.2. Mức code của mọi ứng viên

| Mức | Nghĩa | Phương pháp |
|---|---|---|
| **M1** | Có code, giấy phép mở. Chỉ cần đọc file parquet thành bảng rồi gọi hàm | BARO, N-Sigma, RCD, CIRCA với đồ thị PC chỉ RHT (giả định định dạng ở mục 1), PC-PageRank, BOCPD |
| **M2** | Có code, giấy phép mở, nhưng thiếu dữ liệu đầu vào hoặc chưa có đường chạy. Phải viết thêm bộ đọc dữ liệu, hoặc dựng hay tải dữ liệu nó cần | MicroRank, TraceRCA bản RCAEval: hàm có sẵn, nhưng không có code nào đọc file trace và đưa vào hàm (mục 1); MicroRank còn phải sửa hai sai lệch ở phần dựng đầu vào. TORAI, mmBARO, mmRCD, mmCIRCA: cần chuỗi thời gian log và trace dựng từ log/trace thô; RCAEval không kèm code dựng. CIRCA với đồ thị kiến trúc: phải viết bộ dựng cấu hình đồ thị. CIRCA thêm DA: phải gọi thêm `DAScorer`. GDN: chỉ đọc định dạng CSV riêng, cần một bộ cột cố định, cần môi trường torch/PyG cũ. SPOT: `ads-evt`, GPLv3 |
| **M3** | Có code nhưng không có giấy phép, hoặc phải sửa mới chạy. Chỉ đọc rồi tự cài lại | MicroRCA, Eadro, TraceRCA gốc, DeepTraLog (thiếu cả bộ dựng đồ thị) |
| **M4** | Không có code khớp bài. Cài theo mô tả trong bài | SimpleRCA (mọi nhánh code của tác giả đều khác mô tả bài, mục 3a), PDiagnose (hai bài RCAEval và TORAI đều tự cài) |

Với danh sách đã chốt, không phương pháp nào phải dựa vào code không có giấy phép. SimpleRCA được cài theo mô tả bài; đọc code tác giả chỉ để đối chiếu.

### 8.3. Kiểm thêm ngày 02/10/2026 (chỉ đọc). Dữ kiện về RCAEval là về một ứng viên của P2, không dùng để chọn dataset

- **Metric host:** không có.
  - Cách kiểm: đọc tên cột metric của 35 ca local qua `results/T-002/local-inspection/run-002/schemas.json`, và tự đọc footer parquet của `data/rcaeval/re2tt_ts-auth-service_cpu_1/metrics.parquet`.
  - Kết quả: chỉ có cpu, mem, socket, diskio, workload, latency-50, latency-90, error theo service. RE2-TT có khoảng 340–375 metric mỗi ca; bộ cột khác nhau giữa các ca.
- **Môi trường:** máy có Python 3.9 và 3.12, chưa có 3.8. Mọi gói ghim của RCD/TORAI (`RE:requirements_rcd.lock`, `requirements_torai.lock`) đều có wheel `cp38-win_amd64` trên PyPI. GDN (torch 1.5.1+cpu, torch-scatter 2.0.4, torch-sparse 0.6.x) có wheel cp38 Windows trên kho của PyTorch và PyG. `RE:script/link.sh` vá thư viện bằng symlink theo đường dẫn Linux; trên Windows phải chép tay 5 file.
- **Dữ liệu cho TORAI:**
  - Bản Hugging Face đang có trong `data/` chỉ có `metrics`, `logs`, `traces` dạng parquet, không có `logts`/`tracets`.
  - RCAEval không có code dựng hai chuỗi này.
  - Bản đã xử lý cho RE2 có ở Figshare: TORAI 91 MB (article 31925976); RCAEval đầy đủ 4,46 GB (article 31048672).
  - Với dataset khác RCAEval, phải tự dựng.
- **Runner:** `RE:main.py:204-208` tìm `data.csv`/`simple_metrics.csv`, không đọc parquet. Mọi phương pháp gọi hàm trực tiếp qua adapter của nhóm.
- **BOCPD** giữ một ma trận (T+1)×(T+1) với T là số điểm trong cửa sổ (`BR:baro/_bocpd.py`, hàm `online_changepoint_detection`). Cửa sổ 24 phút ở 1 điểm/giây thì nhẹ; chuỗi dài nhiều giờ thì không chạy một lần được.
- **Chưa kiểm:** thời gian chạy trên CPU và cài thật môi trường. Việc này giao cho task đo riêng (Minh duyệt 02/10); SPEC chờ trình.

### 8.4. Còn mở

1. **Báo động sai trên mỗi giờ bình thường** (MRP P3, P7): giữ nguyên độ đo trong MRP; T-001 không quyết cách đo.
   - "Mỗi giờ" là một tỷ lệ: tổng số báo động sai chia cho tổng thời gian bình thường đã quan sát. Cộng nhiều đoạn ngắn vẫn tính được.
   - Ba hạn chế khi đoạn ngắn: phần khởi động hoặc học ngưỡng ăn bớt thời gian; ít giờ thì con số kém chắc chắn; không thấy biến động dài.
   - Có ý nghĩa đến đâu phụ thuộc dataset được chọn: P2 ghi lượng dữ liệu bình thường của từng dataset (tiêu chí 8, MRP §4); P3 quyết cách đo sau G1.
2. **SPEC task đo** môi trường và thời gian chạy: chờ trình. Minh đồng ý (03/10) dùng vài ca có sẵn trong `data/` (không đụng `data/locked/`) chỉ để đo thời gian. Việc này không phải chọn dataset.

### 8.5. Các phương án đã xét

Chi tiết ba phương án ở `v2-danh-sach-phuong-phap.md`, mục 8. Cột "Thuộc phương án" ở mục 5 của file này cũng chỉ về các phương án đó.

- **A** (10 RCA): không chọn.
  - Quá rộng so với yêu cầu chiều sâu của cô.
  - Hai phương pháp có điều kiện. Cả hai cần điều kiện dữ liệu hoặc nhãn mà P2 chưa kiểm.
  - Lý do chính của A là "có mốc cho ba ví dụ của cô"; lý do này đặt sai vai trò của ba ví dụ (Q-24).
- **B** (9 RCA): gần bản gọn. Khác ở chỗ B coi N-Sigma và TraceRCA là phương pháp có hồ sơ đầy đủ và có thêm PC-PageRank.
- **C** (14): vượt mức ước lượng. Nhiều phương pháp cần log có trace ID hoặc không có code gốc.
- **Bản gọn 6 RCA + 2 biến thể**: Minh chốt (Q-37), rồi sửa thành **5 RCA + 3 biến thể**, đưa RCD về làm biến thể của TORAI.
- **Giữ RCD, bỏ TORAI**: không chọn. Sẽ mất phương pháp đa nguồn có kết quả công bố tốt nhất trên RE2 trong 9 baseline của bài TORAI, tức mất một ứng viên "baseline mạnh nhất" cho RQ3.
- Cái giá chung của bản gọn: không có prior work cho "GNN dùng trong RCA" và "đồ thị con". Nếu sau P4 cần, dùng các phương pháp dự phòng.

## 9. Nguồn và revision

| Nguồn | Revision / ngày truy cập |
|---|---|
| RCAEval `phamquiluan/RCAEval` | `main` `259ea4167160256a74ad30004aa3d96a998c846e`; `www25` `9d14687ce0644188f1f1a576fd3f57cd903af446`; `fse26` `eeadab4f797ed7a0012958fb86f0e4af621ddba6`; `ase24` `19e54db4bf3b04f0759acaf491c202c3a5142324` |
| BARO `phamquiluan/baro` | `e35f4ec1095e5cac891d52de9ad18a5b32a37ec8` |
| Simple-RCA `LGU-SE-Internal/Simple-RCA` | nhánh mặc định `orig` `1be391178d872302dd17fcefa3d2cc4505ce4513` (commit mà `OperationsPAI/rca-algo-contrib` trỏ tới); nhánh `rcaeval` `5fd1f7fceab7aae92efe9e86500cfc004c0950d1`; nhánh `rcaeval_re3_ss` `7f7f2954f7c40d7705e0a4a4ebe17aed8978610d`. Artifact của bài: Zenodo 17105974 (hai zip code `rcabench-platform-feat-fse26.zip`, `rcabench-fse-26.zip`) |
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
