# T-001 — Danh sách phương pháp cho P1 (đề xuất, chờ Minh duyệt ở G1)

Ngày: 02/10/2026. Người làm: Claude. Chưa chạy phương pháp nào, chưa dựng môi trường (SPEC "Không làm").

## 0. Cách đọc file này

- **Đã kiểm code**: đã đọc file code ở revision ghi trong bảng nguồn (mục 5). Dẫn dạng `file:dòng`.
- **Theo bài**: lấy từ trang arXiv HTML hoặc README, đọc qua công cụ tóm tắt web. **Chưa đối chiếu bản in.** Chỉ dùng làm thông tin, không làm căn cứ chọn.
- **Theo K1**: lấy từ `docs/knowledge/K1-phuong-phap-rca.md`, ghi rõ "chưa kiểm lại".
- **Chưa kiểm**: không có nguồn trong phiên này; ghi giả định nếu có.
- Viết tắt repo code: `RE:` = RCAEval `phamquiluan/RCAEval` @ `259ea41`; `BR:` = `phamquiluan/baro` @ `e35f4ec`; `SR:` = `LGU-SE-Internal/Simple-RCA` @ `1be3911`; `EA:` = `BEbillionaireUSD/Eadro` nhánh `main`; `MR:` = `elastisys/MicroRCA` nhánh `master`. Hash đầy đủ ở mục 5.

## 1. Bước 1 — Các phương pháp có trong RCAEval (đọc code thật)

Danh sách đăng ký: `RE:RCAEval/e2e/__init__.py:44-72` (Python 3.12) và `RE:main.py:47-82`. README liệt kê 17 baseline (`RE:README.md:236`).

| Hàm | File | Họ | Ghi chú đã kiểm trên code |
|---|---|---|---|
| `baro` | `RE:RCAEval/e2e/baro.py:19-60` | Thống kê trên metric | **Chỉ là bước xếp hạng**: RobustScaler học trên đoạn trước `inject_time`, điểm = max z sau `inject_time` (`baro.py:22-24, 49-51`). **Không có BOCPD** trong nhánh `main` (BOCPD chỉ còn ở `RE:legacy/eval.py:126-375`, đọc file JSON kết quả có sẵn). |
| `mmbaro`, `mmnsigma` | `RE:RCAEval/e2e/baro.py:178`, `:71` | Thống kê đa nguồn | Thêm chuỗi đếm log và chuỗi trace (lỗi, độ trễ); trace chỉ dùng với OB, TT (`baro.py:63-68`). |
| `nsigma` | `RE:RCAEval/e2e/__init__.py:109-148` | Thống kê trên metric | Như `baro` nhưng dùng StandardScaler (`__init__.py:137`). |
| `e_diagnosis` | `RE:RCAEval/e2e/__init__.py:154-201` | Thống kê (kiểm định hai mẫu) | Gọi PyRCA. |
| `circa`, `mmcirca` | `RE:RCAEval/e2e/circa.py:18-43`, `:45` | Nhân quả + đồ thị | **Khác bài**: đồ thị học bằng PC từ metric (`circa.py:33`, `pc_default`), không phải đồ thị kiến trúc như bài gốc (K1 §C.6, chưa kiểm lại). Chấm bằng `rht` (`RE:RCAEval/graph_heads/rht.py:290`). |
| `rcd`, `mmrcd` | `RE:RCAEval/e2e/rcd.py:449-462`, `mmrcd.py` | Nhân quả | Chia normal/anomal theo `inject_time` (`rcd.py:461-462`). Cần môi trường Python 3.8 riêng (`RE:main.py:133-134`, `RE:docs/SETUP.md:39`). |
| `torai` | `RE:RCAEval/e2e/torai.py:69` | Đa nguồn + nhân quả, không dùng đồ thị gọi | Cắt theo `inject_time` (`torai.py:84-112`). Import từ `rcd` (`torai.py` đầu file) nên cũng cần môi trường RCD. Hàm có tham số `service`, `fault_type`, `case` nhưng thân hàm không đọc chúng (các chỗ khớp chữ "service" là biến cục bộ `service_list`, `service_ranks`, từ dòng 238); runner không truyền chúng (`RE:main.py:408-417`). |
| `tracerca` | `RE:RCAEval/e2e/tracerca.py:45-95` | Dựa trên trace | **Bản cài lại đơn giản**: span bất thường nếu `duration ≥ mean+3·std` của operation trên đoạn bình thường (`tracerca.py:61`); xếp hạng theo trung bình điều hòa của support và confidence (`:64-84`). |
| `microrank` | `RE:RCAEval/e2e/microrank.py:646-711` | Trace + PageRank | Phát hiện cũng theo span `mean+3·std` (`microrank.py:666-667`), khác bài (`μ+1.5σ` theo trace, K1 §C.3, chưa kiểm lại). PageRank `d=0.85` (`:20`), rồi phổ (spectrum). |
| `pdiagnose` | `RE:RCAEval/e2e/pdiagnose.py:49-61` | Đa nguồn | **Không chạy được như phương pháp**: chỉ có `main()` đọc đường dẫn cứng `./data/mm-ob/checkoutservice_cpu/1/...`; không đăng ký trong `__init__.py:44-72` hay `main.py:47-82`. |
| `microcause` | `RE:RCAEval/e2e/microcause.py:2178` | Nhân quả + random walk | **Cần SLI** suy từ tên ca (`microcause.py:2187`; SLI chọn ở `RE:main.py:340-363` từ `service` lấy từ tên thư mục, `main.py:283`). Có bản sao SPOT/DSPOT (`microcause.py:2095-2113`) nhưng không gọi (`:2190` bị comment). |
| `easyrca` | `RE:RCAEval/e2e/easyrca.py:2178` | Nhân quả | Cần SLI như trên (`easyrca.py:2187`). |
| `cloudranger` | `RE:RCAEval/e2e/cloudranger.py:154-179` | Tương quan + random walk | Cần SLI (`cloudranger.py:163`). |
| `run` | `RE:RCAEval/e2e/run.py` | Nhân quả, học sâu (torch) | |
| `causalrca` | `RE:RCAEval/e2e/causalrca.py` | Nhân quả, học sâu (torch) | |
| `mscred` | `RE:RCAEval/e2e/mscred.py` | Phát hiện bằng học sâu (torch) | |
| `causalai` | `RE:RCAEval/e2e/causalai.py:14` | Nhân quả | Không có trong danh sách `main.py:47-82`. |
| `pc_pagerank`, `cmlp_pagerank`, `ntlr_pagerank`, `fci_/ges_/granger_/lingam_pagerank`, `*_randomwalk`, `micro_diag` | `RE:RCAEval/e2e/pc_pagerank.py`, `pc_randomwalk.py`, `lingam_pagerank.py`, ... | Đồ thị nhân quả học từ metric + PageRank/random walk | Họ "đồ thị học + lan truyền". |
| `eventadl` | `RE:RCAEval/e2e/eventadl.py:129` | Log sự kiện kiểu CloudTrail | Khác loại dữ liệu; không áp vào bài toán metric/log/trace. |
| `ht` | `RE:RCAEval/e2e/__init__.py:204` | Nhân quả (PyRCA) | Chỉ nhập khi chạy Python 3.8 (`RE:main.py:85-86`). |

**Phát hiện về runner (ảnh hưởng P3, đã kiểm code):**
- `RE:main.py:204-208, 286` chỉ đọc `data.csv` hoặc `simple_metrics.csv`; nhánh đa nguồn đọc thêm `logts.csv`, `tracets_*.csv` (`main.py:368-400`). **Không có nhánh nào đọc `traces.csv`.** Vậy `tracerca`, `microrank` không chạy được qua `main.py` như hiện tại; cần adapter riêng. Giả định "RCAEval đã chạy sẵn được TraceRCA, MicroRank" là **sai ở HEAD này**.
- `tracerca`, `microrank` nhận `inject_time` theo micro giây (dòng đổi đơn vị bị comment: `tracerca.py:51`, `microrank.py:652`).
- `RE:main.py:283` lấy `service` gốc từ tên thư mục ca rồi chọn SLI theo nó (`main.py:340-363`). Đúng như MRP P2 đã ghi. Ảnh hưởng tới `microcause`, `easyrca`, `cloudranger`.

## 2. Bước 2 — Phương pháp ngoài RCAEval: code chính thức và giấy phép

Giấy phép kiểm qua GitHub API (`/repos/<repo>` và danh sách file gốc) ngày 02/10/2026. "Không có LICENSE" = repo không có file giấy phép; về pháp lý là giữ mọi quyền. Dùng để tái lập trong nghiên cứu thường được chấp nhận, nhưng **không được chép code vào repo này**. Đây là nhận định chưa kiểm với nhà trường.

| Phương pháp | Repo | Giấy phép | Ghi chú |
|---|---|---|---|
| BARO (đầy đủ, có BOCPD) | `phamquiluan/baro` | MIT | `BR:baro/anomaly_detection.py:77` (`bocpd`, hazard hằng 50 ở `:144`), `:7` (`nsigma`, k=3), `BR:baro/_bocpd.py`. |
| SimpleRCA | `LGU-SE-Internal/Simple-RCA` (submodule của `OperationsPAI/rca-algo-contrib`) | Không có LICENSE | `SR:src/simplerca/main.py:37`. Nhánh `rcaeval` (`5fd1f7f`) có thêm `baro.py`, `time_series.py`; chưa kiểm có adapter RE2 hay không. **Đường nhãn:** adapter đọc nhãn loại lỗi (`SR:src/simplerca/adapter.py:41-46`) và truyền `fault_type` vào hàm (`adapter.py:122-126`); hàm `simplerca` không dùng nó (`main.py:37` là chỗ duy nhất có chữ này). Adapter lấy cửa sổ sự cố từ `fault_start_time`, `fault_end_time` (`adapter.py:49-51`). Adapter của nhóm phải bỏ cả hai đầu vào này. |
| Eadro | `BEbillionaireUSD/Eadro` | Không có LICENSE | Chọn checkpoint theo HR@1 trên tập test (`EA:codes/base.py:102-105`), đúng như MRP P3 ghi. Có cờ `--gpu`, tự lùi về CPU (`EA:codes/main.py:62-67`). |
| MicroRCA | `elastisys/MicroRCA` | Không có LICENSE | BIRCH `ad_threshold=0.045`, `alpha=0.55`, PageRank `alpha=0.85` (`MR:MicroRCA.py:37, 255, 275-276`). Cần đồ thị service–host (`MR:MicroRCA.py:65`); RCAEval có quan hệ service–host không thì **chưa kiểm** (việc của P2). |
| MicroRank (gốc) | `IntelligentDDS/MicroRank` | MIT | Dùng để so với bản cài lại của RCAEval. |
| TraceRCA (gốc) | `NetManAIOps/TraceRCA` | Không có LICENSE | Có các script phát hiện và khai phá luật kết hợp; cấu hình cho TrainTicket (`trainticket_config.py`). Chưa đọc chi tiết. |
| PDiagnose | Không tìm thấy (`NetManAIOps/PDiagnose` trả 404). | — | Chỉ có script hỏng trong RCAEval (mục 1). |
| DeepTraLog | `FudanSELab/DeepTraLog` | Không có LICENSE | `model/main.py`, `model/model.py`. Chạy trên CPU được không: **chưa kiểm**. |
| GDN | `d-ailin/GDN` | MIT | Thiết bị cấu hình được (`main.py:55-56`). Thời gian chạy CPU: **chưa kiểm**. |
| SPOT/DSPOT | Không tìm thấy repo của tác giả (`Amossys-team/SPOT` trả 404). | Bản sao trong `RE:RCAEval/e2e/microcause.py:2095` (LICENSE-MicroCause, Apache 2.0) | Nguồn gốc bản sao: **chưa kiểm**. |
| CIRCA (gốc) | `NetManAIOps/CIRCA` | BSD-3-Clause | Cần để chạy đúng biến thể đồ thị kiến trúc. |
| RCD (gốc) | `azamikram/rcd` | MIT | |
| DéjàVu | `NetManAIOps/DejaVu` | MIT | Không có trong ứng viên MRP; xem mục 4. |

## 3. Bước 3 — Bảng ứng viên

Cột "Biết trước thời điểm?" = phương pháp có cần mốc sự cố từ bên ngoài không. "Nhãn để học?" = có cần nhãn nguyên nhân hoặc nhãn bất thường để huấn luyện không (khác với nhãn chỉ để chấm).

### 3a. Phương pháp RCA (ứng viên trong MRP P1)

| # | Phương pháp | Họ | Bài toán | Đầu vào | Biết trước thời điểm? | Nhãn để học? | Code, giấy phép, CPU | Bài gần đây dùng làm baseline | Đề xuất |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **BARO** | Thống kê trên metric | Phát hiện (BOCPD) + xếp hạng | Metric | Bản RCAEval: có (`RE:baro.py:22-24`). Bản gốc: không, BOCPD tìm mốc (`BR:anomaly_detection.py:77`) | Không | RE + BR, MIT, CPU (chỉ numpy/sklearn) | RCAEval, TORAI, SimpleRCA, DecompRCA, PRISM (theo bài) | **Chọn.** Mạnh, rẻ, được gần như mọi bài gần đây dùng. Chạy cả hai chế độ: có mốc (RCAEval) và tự phát hiện (BR). |
| 2 | **N-Sigma** | Thống kê trên metric | Xếp hạng (và phát hiện, bản BR) | Metric | Có (`RE:__init__.py:110-112`) | Không | RE + BR, MIT, CPU | Detector baseline của BARO (K1 §C.4, chưa kiểm lại) | **Chọn.** Gần như miễn phí; là đối chứng của BARO (chỉ khác bộ chuẩn hóa, `__init__.py:137` vs `baro.py:49`). |
| 3 | **SimpleRCA** | Luật đơn giản, đa nguồn | Xếp hạng theo số cảnh báo | Metric, log, trace + dữ liệu bình thường | Có: cả đầu và cuối cửa sổ sự cố, lấy từ file nhãn (`SR:adapter.py:49-51`) | Không | SR, **không có LICENSE**, CPU (pandas) | Chính bài FSE'26 đề xuất nó | **Chọn.** Bài FSE'26 báo top-1 0,80 trên RE2-TT so với BARO 0,67 (theo bài, chưa đối chiếu bản in). Nếu đúng, đây là baseline "không đồ thị" mạnh nhất phải vượt (LESSONS QT7). Cần viết adapter; đọc code để cài lại, không chép. |
| 4 | **RCD** | Nhân quả | Xếp hạng | Metric (đa nguồn ở `mmrcd`) | Có (`RE:rcd.py:461-462`) | Không (cần chia normal/anomal) | RE + gốc, MIT, CPU; cần Python 3.8 | RCAEval, TORAI, DecompRCA, SimpleRCA (repo `rca-algo-contrib`) | **Chọn.** Đại diện nhân quả học từ dữ liệu, dùng rộng. |
| 5 | **CIRCA** | Nhân quả + đồ thị cấu trúc | Xếp hạng | Metric + đồ thị + mốc phát hiện | Có (`RE:circa.py:35`) | Không | RE (BSD-3) + gốc (BSD-3), CPU | RCAEval, TORAI, DecompRCA | **Chọn.** Là phương pháp duy nhất trong danh sách mà đồ thị đi vào phép tính điểm bất thường (parent set, K1 §D.2 mẫu E). Lưu ý: bản RCAEval dùng đồ thị PC, không phải đồ thị kiến trúc. Biến thể nào chạy chốt ở hồ sơ P1. |
| 6 | **MicroRank** | Trace + PageRank | Phát hiện trace + xếp hạng operation | Trace | Có (`RE:microrank.py:654-658`) | Không | RE (MIT) + gốc (MIT), CPU; **không chạy được qua `main.py`** (mục 1) | RCAEval, TORAI, SimpleRCA (theo bài) | **Chọn.** Trực tiếp là ví dụ PageRank của cô. Bản RCAEval khác bài ở ngưỡng phát hiện. |
| 7 | **TraceRCA** | Dựa trên trace, không đồ thị | Phát hiện span + xếp hạng | Trace | Có (`RE:tracerca.py:53-54`) | Không | RE (MIT, bản cài lại) + gốc (không có LICENSE), CPU; không chạy qua `main.py` | RCAEval, TORAI (theo bài) | **Chọn.** Bản RCAEval có cùng bước phát hiện với MicroRank (mean+3·std, `tracerca.py:61` vs `microrank.py:667`). Cặp này cho phép so "trace có PageRank" với "trace không PageRank" khi giữ nguyên bộ phát hiện. |
| 8 | **MicroRCA** | Lan truyền trên đồ thị (PPR) | Phát hiện cạnh (BIRCH) + xếp hạng service | Độ trễ cuộc gọi + metric container/host + đồ thị | Không, BIRCH tự phát hiện trên cửa sổ dữ liệu (`MR:MicroRCA.py:19-37`); cách cắt cửa sổ: chưa kiểm | Không | MR, **không có LICENSE**, CPU (sklearn, networkx) | SimpleRCA (theo bài); MonitorRank-style baseline trong K1 | **Chọn có điều kiện.** Đại diện thuần "lan truyền trên đồ thị" và là ví dụ PageRank thứ hai của cô. Điều kiện: dataset có độ trễ theo cạnh gọi và quan hệ service–host (P2 kiểm). Nếu không có, ghi lý do và dùng PC-PageRank (mục 4) thay vai trò lan truyền. |
| 9 | **TORAI** | Đa nguồn, nhân quả, không dùng đồ thị gọi | Xếp hạng service và chỉ báo | Metric, log, trace (chuỗi thời gian) | Có (`RE:torai.py:84`; bài: cần `t_A` từ bộ phát hiện ngoài) | Không | RE, MIT, CPU; cần môi trường RCD | Chính bài FSE'26 | **Chọn.** Đối chứng "đa nguồn không đồ thị gọi"; trực tiếp hỏi đồ thị gọi có cần không. Rủi ro: cùng nhóm tác giả với RCAEval, kết quả công bố trên chính RCAEval (xem mục 6). |
| 10 | **Eadro** | Học có đồ thị (GAT), có giám sát | Phát hiện cửa sổ + xếp hạng service | Log, KPI, trace + đồ thị gọi lịch sử | Không (phân loại cửa sổ) | **Có**: nhãn cửa sổ bất thường + service gốc | EA, **không có LICENSE**, CPU được (`EA:main.py:62-67`), thời gian chưa kiểm | SimpleRCA (theo bài, và repo `rca-algo-contrib`) | **Chọn có điều kiện.** Đại diện duy nhất của họ "học có đồ thị" cho RCA. Điều kiện: (a) đổi chọn checkpoint sang dev (`EA:base.py:102-105`); (b) không xếp chung bảng với phương pháp không giám sát mà không ghi rõ (MRP §4); (c) đủ ca có nhãn trên dev; nếu không đủ thì báo "không chạy được công bằng". |
| 11 | **PDiagnose** | Đa nguồn | Xếp hạng | Metric, log, trace | Có (`RE:pdiagnose.py:61-70`) | Không | Không có code chạy được (mục 1, 2) | RCAEval, TORAI (theo bài) | **Không chọn.** Không có code chạy được; tự cài theo bài là cài lại một phương pháp, dễ lặp LESSONS SL7. Họ đa nguồn đã có SimpleRCA, TORAI, mmBARO. |

### 3b. Bộ phát hiện bất thường (Q-30)

| # | Bộ phát hiện | Họ | Đơn vị phát hiện | Đầu vào | Nhãn để học? | Code, giấy phép, CPU | Bài gần đây dùng | Đề xuất |
|---|---|---|---|---|---|---|---|---|
| D1 | **BOCPD** (trong BARO) | Thống kê, điểm thay đổi | Thời điểm | Metric (độ trễ, lỗi) | Không | `BR:anomaly_detection.py:77`, MIT, CPU | BARO | **Chọn.** Cho chế độ "tự phát hiện" của BARO. |
| D2 | **N-Sigma** | Thống kê | Thời điểm | Metric | Không | `BR:anomaly_detection.py:7`, MIT, CPU | Detector baseline trong BARO (K1, chưa kiểm lại) | **Chọn.** Baseline phát hiện đơn giản nhất. |
| D3 | **SPOT/DSPOT** | Thống kê cực trị (EVT) | Thời điểm | Chuỗi đơn biến | Không | Bản sao `RE:microcause.py:2095`, Apache 2.0 (theo LICENSE-MicroCause), CPU | Detector baseline trong BARO (K1, chưa kiểm lại); ARMOR dùng POT (K1 §C.12) | **Chọn.** Đại diện ngưỡng EVT; nguồn gốc bản sao chưa kiểm. |
| D4 | Ngưỡng trace mean+3·std (MicroRank/TraceRCA bản RCAEval) | Thống kê trên trace | Span | Trace | Không | `RE:tracerca.py:61`, MIT | Đi kèm hai phương pháp trên | **Chọn**, không tốn thêm: chấm riêng như một bộ phát hiện. |
| D5 | BIRCH (MicroRCA) | Phân cụm | Cạnh gọi | Độ trễ cạnh | Không | `MR:MicroRCA.py:19-37` | Detector baseline trong BARO (K1, chưa kiểm lại) | Đi theo MicroRCA (chọn có điều kiện). |
| D6 | **GDN** | Đồ thị học + GNN, dự báo | Thời điểm + chuỗi lệch | Chuỗi metric | Không (học trên dữ liệu bình thường) | `d-ailin/GDN`, MIT; CPU chưa kiểm | DecompRCA dùng WADI/SWaT là dữ liệu gốc của GDN (theo README) | **Chọn.** Đại diện "GNN-based anomaly detection" trên metric, ví dụ thứ ba của cô. Rủi ro: chưa đánh giá trên microservice (K1 §C.11, chưa kiểm lại). |
| D7 | **DeepTraLog** | Đồ thị trace + GGNN | Trace | Span + log gắn vào span | Không (một lớp) | `FudanSELab/DeepTraLog`, **không có LICENSE**; CPU chưa kiểm | Chưa thấy trong 4 bài đã xem | **Chọn có điều kiện.** Đại diện duy nhất "đồ thị là đối tượng bị chấm" (K1 §D.2 mẫu D). Điều kiện: dataset có log gắn trace_id và có nhãn bất thường theo trace hoặc dùng nhãn theo khoảng tiêm lỗi (P2 kiểm). |
| D8 | Đầu nhị phân của Eadro | GNN có giám sát | Cửa sổ | Đa nguồn | Có | EA | — | Đi theo Eadro. |

## 4. Phương pháp có trong RCAEval hoặc K1 nhưng không nằm trong ứng viên MRP

Không đề xuất chọn. Liệt kê để Minh thấy phạm vi đã xét.

| Phương pháp | Lý do không chọn bây giờ |
|---|---|
| MicroCause, EasyRCA, CloudRanger | Cần SLI; runner RCAEval chọn SLI từ tên ca (`RE:main.py:283, 340-363`), tức nhãn lọt vào. Muốn dùng phải viết lại phần chọn SLI. Họ "nhân quả" đã có RCD, CIRCA. |
| RUN, CausalRCA, MSCRED | Học sâu (torch), họ nhân quả/phát hiện đã có đại diện rẻ hơn. CausalRCA được SimpleRCA và TORAI dùng (theo bài); nếu Minh muốn thêm một baseline nhân quả học sâu thì CausalRCA là ứng viên. |
| ε-Diagnosis | Họ thống kê đã có BARO, N-Sigma. DecompRCA dùng nó (theo README). |
| PC-PageRank và các biến thể `*_pagerank`, `*_randomwalk` | **Phương án dự phòng** cho vai trò "lan truyền trên đồ thị" nếu MicroRCA không chạy được trên dataset đã chọn. DecompRCA và PRISM dùng PageRank/PC-PageRank làm baseline (theo bài). |
| mmBARO, mmRCD, mmCIRCA | Biến thể đa nguồn của 1, 4, 5. Chạy được gần như miễn phí khi đã có bản gốc; đề xuất coi là **biến thể**, không tính vào số 8–12. |
| EventADL, HT, causalai | Khác loại dữ liệu (EventADL) hoặc không có trong runner Python 3.12. |
| DéjàVu | Có giám sát theo từng hệ, cho lỗi lặp lại (K1 §C.9, chưa kiểm lại); Eadro đã đại diện họ "học có đồ thị, có giám sát". |
| ARMOR | Code chỉ trên Zenodo (K1 §A.2); chưa kiểm tải được. Ứng viên nếu P4 cho thấy thiếu dữ liệu quan sát là hạn chế chính. |
| Nezha, DiagFusion, ART, MicroDig, ShapleyIQ, MicroHECL | Bài SimpleRCA dùng làm baseline (theo bài). Không có trong ứng viên MRP; chưa kiểm code. Nếu Minh muốn mở rộng, Nezha (đa nguồn, có repo trong `rca-algo-contrib`) là ứng viên đầu tiên. |

## 5. Nguồn

| Nguồn | Revision / ngày truy cập |
|---|---|
| RCAEval | `github.com/phamquiluan/RCAEval`, HEAD `259ea4167160256a74ad30004aa3d96a998c846e` (29/09/2026) |
| BARO | `github.com/phamquiluan/baro`, `e35f4ec1095e5cac891d52de9ad18a5b32a37ec8` |
| SimpleRCA | `github.com/LGU-SE-Internal/Simple-RCA`, `1be391178d872302dd17fcefa3d2cc4505ce4513` (commit mà `OperationsPAI/rca-algo-contrib` trỏ tới); nhánh `rcaeval` `5fd1f7fceab7aae92efe9e86500cfc004c0950d1` |
| Eadro, MicroRCA, TraceRCA, DeepTraLog, GDN, MicroRank, CIRCA, RCD, DejaVu | Nhánh mặc định, truy cập 02/10/2026; giấy phép theo GitHub API |
| Bài RCAEval | arXiv 2412.17015 (WWW'25 Companion). Danh sách 15 baseline theo trang HTML |
| Bài TORAI | arXiv 2604.13522 (FSE'26). Chín baseline: PDiagnose, HeMiRCA, CausalRCA, MicroCause, RCD, CIRCA, BARO, MicroRank, TraceRCA (theo trang HTML) |
| Bài SimpleRCA | arXiv 2510.04711 (FSE'26). 11 baseline: MicroRank, MicroRCA, MicroHECL, MicroDig, DiagFusion, Eadro, ART, ShapleyIQ, Nezha, CausalRCA, BARO; top-1 RE2-TT SimpleRCA 0,80, BARO 0,67 (theo trang HTML, **chưa đối chiếu bản in**) |
| Bài DecompRCA | `github.com/cruiseresearchgroup/DecompRCA` README (NeurIPS'26 E&D). Baseline: BARO, RCD, ε-Diagnosis, CIRCA, PageRank, RandomWalk; ghim RCAEval `fb8f20a` |
| Bài PRISM | arXiv 2601.21359 (bản thảo, chưa thấy nơi đăng). Baseline: BARO, ScoreOrdering, Cholesky, PC-PageRank, Counterfactual, RCLAgent, Traversal, SmoothTraversal (theo trang HTML) |

Giới hạn: danh sách baseline và số liệu của các bài đọc qua công cụ tóm tắt trang web, có thể sót hoặc sai tên. Trước khi dùng làm căn cứ ở báo cáo, phải đối chiếu bản PDF.

## 6. Nhận định dựa trên kết quả đã công bố, và nguyên nhân khả thi khác (Q-33)

| Nhận định | Nguyên nhân khả thi khác |
|---|---|
| SimpleRCA đạt top-1 0,80 trên RE2-TT, hơn BARO 0,67 (theo bài) → SimpleRCA là baseline mạnh. | (a) Hai số có thể không cùng giao thức (cửa sổ, tiền xử lý, tập ứng viên). (b) Luật của SimpleRCA có thể được chỉnh trên chính các benchmark này. (c) RE2-TT chỉ có 5 service gốc và đồ thị gần như không đổi (LESSONS ST3), nên một luật đơn giản dễ khớp. (d) Số đọc qua công cụ tóm tắt, chưa đối chiếu bản in. → Chỉ dùng để chọn SimpleRCA làm ứng viên, không dùng để kết luận nó mạnh. |
| BARO, RCD, CIRCA được dùng làm baseline ở hầu hết bài gần đây → "baseline chuẩn". | Có thể vì chúng sẵn trong RCAEval (dễ chạy), không vì chúng mạnh. RCAEval, TORAI, BARO, PRISM, DecompRCA có chung tác giả Luan Pham, nên tần suất xuất hiện không độc lập. |
| TORAI hơn chín baseline (theo bài). | Đánh giá trên benchmark của chính nhóm tác giả; chế độ biết trước `t_A`; các baseline chạy qua runner có thể nhận SLI từ nhãn (mục 1) hoặc rơi về thứ tự cột khi lỗi (`RE:e2e/__init__.py:22-35`; README ghi đã sửa lỗi rơi về thứ tự cột ở 09/2026). |
| Eadro tốt trong bài gốc (K1 §C.7). | Checkpoint chọn theo HR@1 trên test (`EA:base.py:102-105`) làm số lạc quan; chỉ hai benchmark tự thu. |
| Bộ phát hiện trace mean+3·std ở RCAEval "là MicroRank". | Đây là bản cài lại; bài gốc dùng ngưỡng khác (K1 §C.3, chưa kiểm lại). Kết quả bản RCAEval không đại diện cho MicroRank gốc. |

## 7. Đề xuất cho G1 (chờ Minh duyệt)

**Danh sách RCA đề xuất (10):** BARO, N-Sigma, SimpleRCA, RCD, CIRCA, MicroRank, TraceRCA, TORAI, và hai phương pháp có điều kiện: MicroRCA, Eadro. Biến thể đa nguồn mmBARO, mmRCD, mmCIRCA chạy kèm, không tính vào số.

**Bộ phát hiện đề xuất:** BOCPD, N-Sigma, SPOT, ngưỡng trace mean+3·std, GDN; DeepTraLog có điều kiện. BIRCH và đầu nhị phân Eadro đi theo phương pháp mẹ.

**Phủ các họ ở MRP P1:**

| Họ (MRP P1) | Đại diện |
|---|---|
| Thống kê trên metric | BARO, N-Sigma |
| Nhân quả | RCD, CIRCA (CIRCA cũng có đồ thị trong phép tính điểm) |
| Dựa trên trace | TraceRCA, MicroRank |
| Lan truyền trên đồ thị | MicroRank (PageRank), MicroRCA (PPR); dự phòng PC-PageRank |
| Đa nguồn | SimpleRCA, TORAI, mmBARO |
| Học có đồ thị | Eadro (RCA); GDN, DeepTraLog (phát hiện) |

Ba ví dụ của cô: PageRank → MicroRank, MicroRCA; đồ thị con → MicroRCA (đồ thị con bất thường); GNN → Eadro, GDN, DeepTraLog.

**Các phương án đã xét:**
- **A (đề xuất trên, 10 RCA).** Phủ đủ sáu họ, có đối chứng trong cùng họ (BARO/N-Sigma; MicroRank/TraceRCA). Chi phí: ba adapter tự viết (SimpleRCA, TraceRCA+MicroRank vì runner không đọc trace, MicroRCA) và hai môi trường Python (3.12 và 3.8).
- **B (chỉ dùng cái chạy được trong RCAEval, 7 RCA):** BARO, N-Sigma, RCD, CIRCA, TORAI, mmBARO, PC-PageRank. Rẻ nhất. Mất: baseline mạnh SimpleRCA; họ trace (vì runner không đọc trace); họ học có đồ thị. Không trả lời được nhận xét của cô về PageRank trên trace và GNN.
- **C (A + CausalRCA + Nezha, 12 RCA).** Phủ thêm nhân quả học sâu và một phương pháp đa nguồn khác nhóm tác giả. Thêm chi phí torch và adapter Nezha; chưa có câu hỏi nghiên cứu nào cần riêng hai phương pháp này (LESSONS QT1).

**Điều cần Minh quyết ở G1:**
1. Chọn A, B hay C (hoặc sửa).
2. Có chấp nhận dùng code không có giấy phép (SimpleRCA, Eadro, MicroRCA, DeepTraLog, TraceRCA gốc) chỉ để đọc và tái lập, không chép vào repo không.
3. CIRCA chạy biến thể nào: đồ thị PC (RCAEval) hay đồ thị kiến trúc (bài gốc), hay cả hai.
4. Điều kiện của MicroRCA, Eadro, DeepTraLog phụ thuộc kết quả P2 (dataset có gì). Đề xuất: chốt sau khi có thẻ dataset (T-002, T-003).
