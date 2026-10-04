# T-007 — Kiểm đúng đắn trên EC2: MicroRank, TraceRCA, BOCPD

Ngày 03/10/2026, hai phiên. Người làm: Claude. Máy: EC2 m7i-flex.large, Ubuntu 24.04 (`moi-truong-ec2.md`).

Mục đích: biết ba phương pháp chạy đúng hay không trước khi dùng số của chúng (LESSONS SL24, Q-41), bằng cách chạy lại trên dữ liệu có số công bố và so từng ô. Task này không trả lời câu hỏi nghiên cứu, không chọn dataset.

Mọi đường dẫn dưới đây tính từ `results/T-007/`. Khối chạy nằm ở `runs/<bộ thư viện>/<khối>.tar.gz`.

## Tóm tắt

| Phương pháp | Mốc (loại) | Cấu hình | Ô lệch > 0,02 | Kết luận theo tiêu chí |
|---|---|---|---|---|
| MicroRank | Bảng 2 bài TORAI, dòng Trace (B) | ±600 s, cấu hình so mốc chính thức (mục 1.3) | 0/21 (lệch lớn nhất 0,003) | **khớp** |
| MicroRank | như trên | ±300 s (SPEC) | 2/21 | lệch |
| TraceRCA | Bảng 2 bài TORAI, dòng Trace (B) | ±600 s, cấu hình so mốc chính thức | 3/21 (mỗi ô 1 ca; AVERAGE khớp) | lệch |
| TraceRCA | như trên | ±300 s (SPEC) | 7/21 | lệch |
| BOCPD | README BARO (A) | lệnh tác giả | 0/3 | **khớp** |
| BOCPD | Bảng 2 bài BARO (B) | lệnh tác giả | 2/3 | lệch (tác giả tự ghi số tái lập cao hơn bài) |

Các phát hiện chính:
1. **BOCPD chạy đúng như tác giả.** 100/100 ca có danh sách điểm đổi giống hệt kết quả tác giả lưu sẵn trong dataset; P/R/F1 trùng README.
2. **MicroRank khớp mốc ở cấu hình ±600 s** (21/21 ô, lệch lớn nhất 0,003). Ở ±300 s (SPEC) lệch 2 ô LOSS, do 3 ca LOSS đổi hạng giữa hai cửa sổ.
3. **MicroRank (bản RCAEval) xếp hạng gần như theo lưu lượng.** Thứ tự điểm theo sát số trace đi qua thao tác (tương quan hạng 0,75–0,97). 87/90 ca (±300 s) và 82/90 ca (±600 s) có cùng 4 service đầu, bất kể lỗi. Bộ số của bài ở 5/6 loại lỗi (0,00 / 0,40 / 0,36) đúng là bộ số của một thứ hạng cố định như vậy.
4. **TraceRCA lệch 3/21 ô ở ±600 s** (mỗi ô 1 ca, AVERAGE khớp) và 7/21 ô ở ±300 s. Nguyên nhân đã chứng minh có tác động: kết quả đổi theo thứ tự dòng span. Code sắp xếp với khóa NaN; 79/90 ca có thứ hạng không giảm dần theo điểm. Chỉ đổi thứ tự dòng (cùng tập span) đã làm hạng đáp án đổi ở 22/90 ca, một ô đổi tới 0,2.
5. **Bản thư viện không đổi kết quả.** `py312-pin` và `py312` giống hệt ở mọi ca và mọi ô của ba phương pháp.
6. **R1 (REVIEW T-002)** đúng trên dữ liệu BOCPD; phạm vi ảnh hưởng ở mục 5.

Loại B nghĩa là cách chạy của tác giả không công bố đủ để chạy lại y hệt (ở đây: bộ đọc trace). Với loại B, lệch không có nghĩa là sai; mỗi mục nêu các nguyên nhân khả thi (Q-33) và cái nào đã kiểm.

## 1. Cách làm chung

### 1.1 Tiêu chí và cách chấm

- **Tiêu chí khớp** (chốt trong SPEC trước khi chạy): phương pháp tất định, mỗi ô lệch ≤ 0,02. Không chỉnh tham số để cho khớp.
- **Chấm** (MicroRank, TraceRCA) như `main.py` RCAEval: thứ hạng thao tác đổi về service bằng `x.split("_")[0]`, bỏ trùng; `RCAEval.benchmark.evaluation.Evaluator` theo từng loại lỗi. AVERAGE là trung bình 6 loại lỗi (tính lại từ bảng của bài: khớp cả 6 ô AVERAGE). Tên ca chỉ dùng để chấm (`scripts/cham.py`).
- **Kiểm chính script chấm:** chạy `cham.py` trên đầu ra `main.py` của T-006 (TORAI trên torai-OB, 3 lượt): khớp 18/18 ô Avg@5 mà `main.py` in ra.
- **Mốc** trích bằng máy từ HTML arXiv 2604.13522v1, Bảng 2 (`moc-torai-bang2-trace.json`, `scripts/trich_moc.py`).

### 1.2 Dữ liệu và cách chạy

- MicroRank, TraceRCA: 90 ca RE2-OB (5 service gốc × 6 loại lỗi × 3 lần), file `traces.parquet` và `inject_time.txt`. Mốc của Bảng 2 đo trên torai-OB. Đã kiểm: torai-OB và RE2-OB trùng cả 90 tên ca và 90 mốc tiêm (0 ca lệch). torai-OB chỉ có chuỗi trace đã gộp 15 s, nên phải dùng span thô của RE2-OB.
- RCAEval không có code đọc trace (`main.py` chỉ đọc file metric). Dùng bộ đọc của T-005: lấy span có `startTime` trong [mốc − w, mốc + w), gọi `microrank(data, mốc_µs)`, `tracerca(data, mốc_µs)` của RCAEval `259ea41`, không sửa code (`scripts/chay_e2.py`).
- BOCPD: `fse-ob` (Zenodo 11046533), 100 ca. Script bọc mỏng gọi đúng `reproduce_bocpd("fse-ob")` của BARO `e35f4ec`, như `python main.py --dataset OnlineBoutique --anomaly-detection`; chỉ ghi thêm kết quả từng ca (`scripts/chay_e3_bocpd.py`; Minh duyệt).
- Bộ thư viện: số chính thức từ `py312-pin` (X1 của T-006 chốt bộ này, `results/T-006/x1-chot-moi-truong.md`). `py312` chạy song song làm bằng chứng (mục 6).

### 1.3 Cấu hình cửa sổ: vì sao ±600 s là cấu hình so mốc chính thức

SPEC đặt w = 300 s (`--length 10`), lấy theo lệnh trong `docs/TORAI.md` của RCAEval. Lệnh đó là lệnh chạy **chính TORAI**, không phải các baseline. Bằng chứng về cấu hình tác giả dùng cho baseline trong bài TORAI:

1. `main.py` RCAEval đổi mặc định `--length` từ 10 thành 20 ở commit `61326e5` ngày 27/12/2024 (đã kiểm bằng `git show` trên clone `259ea41`). Bài TORAI ra năm 2026.
2. T-006 chạy BARO bằng `main.py --length 20` trên torai-SS: trùng đến 2 chữ số **mọi ô** T1, T3, A5 dòng BARO Bảng 3 bài TORAI (`results/T-006/runs/soi-baro-torai-ss-length20.tar.gz`; LOG T-006). T-007 đã tự đối chiếu `results/T-006/cham/soi-baro-torai-ss-length20.txt` với mốc trong `results/T-006/scripts/moc.py`: 21/21 ô trùng khi làm tròn 2 chữ số.
3. Với `--length 20`, `main.py` cắt cả chuỗi trace gộp (`tracets`) của TORAI thành 40 điểm × 15 s mỗi phía, tức ±600 s.

Vì vậy cấu hình so mốc chính thức là **w = 600 s**. Cả ba bằng chứng đều có trước khi chạy biến thể ±600 s (LOG T-007 phiên 2, mục "Quyết định của Minh trong phiên 2"); kết quả của biến thể không dùng để chọn. Độ mạnh của bằng chứng: **gián tiếp** với MicroRank, TraceRCA. Tác giả không công bố code trace, nên việc họ dùng cùng cửa sổ với các baseline metric là suy luận. Minh duyệt chạy cấu hình này ngày 03/10 (phiên 2), với điều kiện chọn cấu hình theo bằng chứng về cấu hình tác giả, không theo cấu hình nào khớp hơn. Báo cả hai cấu hình. Lựa chọn ghi ở `docs/WHY.md` WHY-16.

## 2. MicroRank

Nguồn: `cham/so-moc-py312-pin.json` (±300 s), `cham/so-moc-py312-pin-microrank-L20.json` (±600 s); giá trị trung gian `cham/thong-ke.json`. Mọi lượt: 90/90 ca chạy không lỗi.

### 2.1 Cấu hình ±600 s (so mốc chính thức)

Nguồn: `runs/py312-pin/microrank-L20.tar.gz`. 0/21 ô lệch quá 0,02; kết luận theo tiêu chí: **khớp**.

| Loại lỗi | AC@1 mốc | AC@1 mình | lệch | AC@3 mốc | AC@3 mình | lệch | Avg@5 mốc | Avg@5 mình | lệch |
|---|---|---|---|---|---|---|---|---|---|
| CPU | 0,00 | 0,000 | +0,000 | 0,40 | 0,400 | +0,000 | 0,36 | 0,360 | +0,000 |
| MEM | 0,00 | 0,000 | +0,000 | 0,40 | 0,400 | +0,000 | 0,36 | 0,360 | +0,000 |
| DISK | 0,00 | 0,000 | +0,000 | 0,40 | 0,400 | +0,000 | 0,36 | 0,360 | +0,000 |
| SOCKET | 0,00 | 0,000 | +0,000 | 0,40 | 0,400 | +0,000 | 0,36 | 0,360 | +0,000 |
| DELAY | 0,00 | 0,000 | +0,000 | 0,40 | 0,400 | +0,000 | 0,36 | 0,360 | +0,000 |
| LOSS | 0,00 | 0,000 | +0,000 | 0,27 | 0,267 | -0,003 | 0,19 | 0,187 | -0,003 |
| AVERAGE | 0,00 | 0,000 | +0,000 | 0,38 | 0,378 | -0,002 | 0,33 | 0,331 | +0,001 |

- So với ±300 s: hạng đáp án đổi ở đúng 3 ca, đều là LOSS và đều thành trượt: `recommendationservice_loss_2` (4 → trượt), `recommendationservice_loss_3` (4 → trượt), `productcatalogservice_loss_2` (3 → trượt) (`cham/thong-ke.json`, `so_sanh`). 3 ca này tạo ra toàn bộ khác biệt ở cột LOSS.
- Thứ hạng vẫn gần như cố định: 82/90 ca có cùng 4 service đầu như ở ±300 s.
- Cấu hình ±600 s được chọn ở mục 1.3 trước khi có kết quả này. Việc khớp 21/21 ô là bằng chứng phù hợp thêm, không phải căn cứ chọn.

### 2.2 Cấu hình ±300 s (SPEC)

2/21 ô lệch quá 0,02 (in đậm); kết luận theo tiêu chí: lệch.

| Loại lỗi | AC@1 mốc | AC@1 mình | lệch | AC@3 mốc | AC@3 mình | lệch | Avg@5 mốc | Avg@5 mình | lệch |
|---|---|---|---|---|---|---|---|---|---|
| CPU | 0,00 | 0,000 | +0,000 | 0,40 | 0,400 | +0,000 | 0,36 | 0,360 | +0,000 |
| MEM | 0,00 | 0,000 | +0,000 | 0,40 | 0,400 | +0,000 | 0,36 | 0,360 | +0,000 |
| DISK | 0,00 | 0,000 | +0,000 | 0,40 | 0,400 | +0,000 | 0,36 | 0,360 | +0,000 |
| SOCKET | 0,00 | 0,000 | +0,000 | 0,40 | 0,400 | +0,000 | 0,36 | 0,360 | +0,000 |
| DELAY | 0,00 | 0,000 | +0,000 | 0,40 | 0,400 | +0,000 | 0,36 | 0,360 | +0,000 |
| LOSS | 0,00 | 0,000 | +0,000 | 0,27 | 0,333 | **+0,063** | 0,19 | 0,280 | **+0,090** |
| AVERAGE | 0,00 | 0,000 | +0,000 | 0,38 | 0,389 | +0,009 | 0,33 | 0,347 | +0,017 |

### 2.3 Giá trị trung gian (QT5)

Đo trên lượt ±300 s; ở ±600 s mẫu thứ hạng tương tự (mục 2.1).

- **Thứ hạng gần như cố định** (`cham/thong-ke.json`, `thu_hang["py312-pin/microrank"]`):
  - 87/90 ca có cùng 4 service đầu: frontendservice, currencyservice, productcatalogservice, recommendationservice. 3 ca còn lại đều là LOSS.
  - frontendservice đứng đầu ở 90/90 ca. Thứ hạng chỉ chứa 4 service này; checkoutservice và emailservice không bao giờ xuất hiện.
  - Một thứ hạng cố định như vậy cho đúng AC@1 0, AC@3 0,40, Avg@5 0,36. Tính tay: currencyservice hạng 2 cho Avg@5 0,8; productcatalogservice hạng 3 cho 0,6; recommendationservice hạng 4 cho 0,4; hai service còn lại 0; trung bình 0,36.
- **Chỉ trả 11 thao tác** ở mọi ca. Hàm phổ `calculate_spectrum_without_delay_list` trả `top_max + 6` thao tác, với `top_max = 5`. Giới hạn này chỉ cắt số thao tác, không tự cố định số service.
- **Trần AC@5 của các thứ hạng thu được:** checkoutservice và emailservice vắng ở mọi thứ hạng, nên 36/90 ca chắc chắn trượt; AC@5 tối đa 0,6 cho tập thứ hạng này. Thực tế AC@5 là 52/90 ở ±300 s và 49/90 ở ±600 s (`cham/py312-pin-microrank.json`, `cham/py312-pin-microrank-L20.json`).
- **Soi bên trong** (`scripts/trung_gian_microrank.py`, 6 ca; `runs/py312-pin/microrank-trung-gian.tar.gz`; `cham/thong-ke.json`, `trung_gian_microrank`). Script bọc hai hàm nội bộ, không đổi kết quả (6/6 ca giống lượt chính).
  - Đồ thị "bất thường" chứa **mọi** trace sau mốc: số trace của đồ thị bằng số trace sau mốc ở 6/6 ca (ví dụ 3584 = 3584).
  - `nf < 0` ở 1–14 trên 37 thao tác mỗi ca.
  - Tương quan hạng (Spearman) giữa điểm Dstar2 và số trace sau mốc đi qua thao tác: 0,957; 0,969; 0,820; 0,940; 0,932; 0,750.
- **Cơ chế** (đọc `RCAEval/e2e/microrank.py` và đối chiếu giá trị trên):
  - Trong `microrank()`, đồ thị bất thường dựng từ mọi span sau mốc. Vì vậy `ef = w·(số trace qua thao tác)` đếm cả trace bình thường. Còn `nf = w·(số trace bất thường − số trace qua thao tác)` âm ở thao tác đông.
  - Kết quả: điểm lớn ở thao tác có nhiều trace, tức thứ hạng đi theo lưu lượng.
  - Vòng chạy `online_anomaly_detect_RCA` trong cùng file, là bản chuyển từ vòng chạy MicroRank gốc, làm khác: chia trace của cùng một cửa sổ thành hai tập rời nhau rồi mới dựng hai đồ thị.
- **Đối chiếu code MicroRank gốc** (`IntelligentDDS/MicroRank` revision `efd85e8`, `preprocess_data.py`, `online_rca.py`; phát hiện bởi phản biện R2, người làm đã kiểm lại). `microrank()` bản RCAEval còn hai sai lệch so với bản gốc:
  1. **Cạnh gọi bị đặt lại ở mỗi span.** `get_pagerank_graph` kiểm `if op not in operation_trace` (từ điển khóa traceID), nên `operation_operation[op] = []` chạy ở mọi span. Mỗi thao tác chỉ còn cạnh của span cuối. Bản gốc kiểm `operation_name not in operation_operation` và tích lũy cạnh. Cạnh đi vào PageRank qua `alpha · p_ss` với `alpha = 0,01`.
  2. **Hai nhóm trace chồng nhau.** Bản RCAEval lấy traceID từ hai nhóm *span* sau mốc (dưới / trên ngưỡng), nên một trace có thể ở cả hai nhóm. Ít nhất 5 060 + 727 − 5 088 = 699 trace ở cả hai nhóm tại `checkoutservice_cpu_1`; cả 6 ca đã soi đều có chồng (`cham/thong-ke.json`). Bản gốc chia ở mức trace (`trace_list_partition`) rồi dùng cùng hai tập cho đồ thị và số đếm.
  - **Chưa đo** hai sai lệch này làm đổi điểm bao nhiêu, và chưa biết chúng có phải nguyên nhân chính của thứ hạng gần cố định không.
- Kết luận ở mục này là về **bản RCAEval** trong cấu hình đã chạy; không xác nhận cơ chế MicroRank gốc.

### 2.4 Nguyên nhân khả thi của các ô lệch, và cái đã kiểm

| Nguyên nhân khả thi | Kiểm | Kết quả |
|---|---|---|
| Bản thư viện | chạy `py312` | không phải: 90/90 file giống `py312-pin` |
| Thứ tự chạy, hash seed của Python | chạy lại 6 ca trong tiến trình mới (Python dùng hash seed ngẫu nhiên mặc định; không ghi giá trị) | không phải: 6/6 file giống |
| Thứ tự dòng span (bộ đọc khác cho thứ tự khác) | xáo thứ tự dòng, 90 ca (`runs/py312-pin/microrank-tron.tar.gz`) | không phải: 44/90 file khác (thứ tự trong nhóm hòa), nhưng thứ hạng service giống 90/90, điểm không đổi |
| Độ dài cửa sổ (tập span) | chạy ±600 s (mục 2.1) | **là nguyên nhân**: ±600 s cho 0/21 ô lệch; 2 ô LOSS ở ±300 s đến từ 3 ca LOSS đổi hạng giữa hai cửa sổ |
| Bộ đọc của tác giả lọc span khác (không phải theo cửa sổ) | không kiểm được | tác giả không công bố code trace |
| Script chấm | so với `main.py` | không phải: 18/18 ô khớp |

LOSS là loại lỗi duy nhất có ca thoát khỏi thứ hạng cố định. 3 ca đó (`currencyservice_loss_1`, `productcatalogservice_loss_1`, `recommendationservice_loss_1`) đều có lưu lượng giảm sau mốc: tỉ lệ span trước/sau mốc trong cửa sổ là 1,84; 2,81; 1,49, trong khi 82/90 ca có tỉ lệ ≤ 1,3 (`cham/thong-ke.json`). Thứ hạng theo lưu lượng nên nhạy với việc lưu lượng giảm, và vì thế nhạy với tập span đưa vào.

## 3. TraceRCA

Nguồn: `cham/so-moc-py312-pin.json` (±300 s), `cham/so-moc-py312-pin-tracerca-L20.json` (±600 s); phân tích sắp xếp `cham/sap-xep-tracerca-py312-pin.json` (trên ±300 s). Mọi lượt: 90/90 ca chạy không lỗi.

### 3.1 Cấu hình ±600 s (so mốc chính thức)

Nguồn: `runs/py312-pin/tracerca-L20.tar.gz`, `cham/so-moc-py312-pin-tracerca-L20.json`. 3/21 ô lệch quá 0,02 (in đậm); kết luận theo tiêu chí: lệch.

| Loại lỗi | AC@1 mốc | AC@1 mình | lệch | AC@3 mốc | AC@3 mình | lệch | Avg@5 mốc | Avg@5 mình | lệch |
|---|---|---|---|---|---|---|---|---|---|
| CPU | 0,07 | 0,067 | -0,003 | 0,80 | 0,800 | +0,000 | 0,69 | 0,693 | +0,003 |
| MEM | 0,00 | 0,000 | +0,000 | 0,53 | 0,533 | +0,003 | 0,57 | 0,573 | +0,003 |
| DISK | 0,20 | 0,200 | +0,000 | 0,80 | 0,733 | **-0,067** | 0,72 | 0,693 | **-0,027** |
| SOCKET | 0,07 | 0,133 | **+0,063** | 0,73 | 0,733 | +0,003 | 0,67 | 0,680 | +0,010 |
| DELAY | 0,20 | 0,200 | +0,000 | 0,53 | 0,533 | +0,003 | 0,57 | 0,560 | -0,010 |
| LOSS | 0,07 | 0,067 | -0,003 | 0,53 | 0,533 | +0,003 | 0,49 | 0,507 | +0,017 |
| AVERAGE | 0,10 | 0,111 | +0,011 | 0,65 | 0,644 | -0,006 | 0,62 | 0,618 | -0,002 |

Mỗi ô lệch tương ứng đúng 1 ca trên 15. Cột AVERAGE trong ngưỡng ở cả 3 chỉ số.

### 3.2 Cấu hình ±300 s (SPEC)

7/21 ô lệch quá 0,02 (in đậm); kết luận theo tiêu chí: lệch.

| Loại lỗi | AC@1 mốc | AC@1 mình | lệch | AC@3 mốc | AC@3 mình | lệch | Avg@5 mốc | Avg@5 mình | lệch |
|---|---|---|---|---|---|---|---|---|---|
| CPU | 0,07 | 0,067 | -0,003 | 0,80 | 0,800 | +0,000 | 0,69 | 0,707 | +0,017 |
| MEM | 0,00 | 0,000 | +0,000 | 0,53 | 0,533 | +0,003 | 0,57 | 0,573 | +0,003 |
| DISK | 0,20 | 0,133 | **-0,067** | 0,80 | 0,733 | **-0,067** | 0,72 | 0,680 | **-0,040** |
| SOCKET | 0,07 | 0,133 | **+0,063** | 0,73 | 0,867 | **+0,137** | 0,67 | 0,680 | +0,010 |
| DELAY | 0,20 | 0,200 | +0,000 | 0,53 | 0,533 | +0,003 | 0,57 | 0,560 | -0,010 |
| LOSS | 0,07 | 0,133 | **+0,063** | 0,53 | 0,467 | **-0,063** | 0,49 | 0,493 | +0,003 |
| AVERAGE | 0,10 | 0,111 | +0,011 | 0,65 | 0,656 | +0,006 | 0,62 | 0,616 | -0,004 |

Một ca trên 15 tương ứng 0,067 ở AC@k. Các ô lệch tương ứng 1–2 ca, theo cả hai chiều.

### 3.3 Giá trị trung gian

- Trả 26–36 thao tác mỗi ca. Service đứng đầu: frontendservice 72/90 ca, checkoutservice 17/90, recommendationservice 1/90 (`cham/thong-ke.json`).
- Tên thao tác ghép từ `serviceName`, tức service phát ra span. Span phía gọi (ví dụ `checkoutservice_GetProduct`) đứng trước service bị lỗi, nên hạng của đáp án thường là 2–4. Phù hợp AC@1 thấp trong bài (0,10).

### 3.4 Kết quả phụ thuộc thứ tự dòng span

- **Phát hiện.** Xáo thứ tự dòng (cùng tập span, seed 1) làm 90/90 file khác lượt chính. Hạng đáp án đổi ở 22/90 ca (`runs/py312-pin/tracerca-tron.tar.gz`; `cham/thong-ke.json`).
- **Cơ chế, đã kiểm** (`scripts/hoa_diem_tracerca.py`, `scripts/phan_tich_sap_xep_tracerca.py`; `runs/py312-pin/tracerca-hoa3.tar.gz`; `cham/sap-xep-tracerca-py312-pin.json`):
  - `ji = 2·s·c/(s+c)` bằng NaN với thao tác không có span bất thường (0/0). 90/90 ca có NaN, 1–11 thao tác mỗi ca.
  - `tracerca.py` gọi `sorted(..., reverse=True)` trên cả khóa NaN, rồi mới bỏ NaN. So sánh với NaN luôn sai, nên kết quả không còn giảm dần: **79/90 ca có thứ hạng không giảm dần theo ji**. Thứ hạng vì vậy phụ thuộc thứ tự xuất hiện của thao tác, tức thứ tự dòng.
  - Áp đúng phép sắp này lên danh sách điểm đã ghi dựng lại thứ hạng ở 90/90 ca, cả thứ tự gốc lẫn thứ tự xáo.
  - Điểm ji giống hệt giữa hai thứ tự ở 90/90 ca, tức không do sai số làm tròn.
  - Ngoài NaN còn có hòa điểm: 44/90 ca có nhóm hòa chạm top 10 (`runs/py312-pin/tracerca-hoa.tar.gz`).
- **Ảnh hưởng tới điểm** (±300 s; in đậm: lệch mốc quá 0,02):

| Loại lỗi | Chỉ số | Mốc | Lượt chính | Thứ tự xáo | Bỏ NaN trước (thứ tự gốc) | Bỏ NaN trước (thứ tự xáo) |
|---|---|---|---|---|---|---|
| CPU | AC@1 | 0,07 | 0,067 | 0,067 | 0,067 | 0,067 |
| CPU | AC@3 | 0,80 | 0,800 | 0,800 | **0,733** | **0,733** |
| CPU | Avg@5 | 0,69 | 0,707 | 0,693 | 0,680 | 0,680 |
| MEM | AC@1 | 0,00 | 0,000 | 0,000 | 0,000 | 0,000 |
| MEM | AC@3 | 0,53 | 0,533 | **0,467** | **0,400** | **0,400** |
| MEM | Avg@5 | 0,57 | 0,573 | **0,533** | 0,560 | 0,560 |
| DISK | AC@1 | 0,20 | **0,133** | **0,333** | 0,200 | 0,200 |
| DISK | AC@3 | 0,80 | **0,733** | **0,733** | **0,733** | **0,733** |
| DISK | Avg@5 | 0,72 | **0,680** | 0,720 | **0,680** | **0,680** |
| SOCKET | AC@1 | 0,07 | **0,133** | **0,133** | **0,133** | **0,133** |
| SOCKET | AC@3 | 0,73 | **0,867** | **0,867** | **0,800** | **0,800** |
| SOCKET | Avg@5 | 0,67 | 0,680 | 0,680 | 0,667 | 0,667 |
| DELAY | AC@1 | 0,20 | 0,200 | **0,267** | 0,200 | 0,200 |
| DELAY | AC@3 | 0,53 | 0,533 | 0,533 | **0,467** | **0,467** |
| DELAY | Avg@5 | 0,57 | 0,560 | **0,600** | 0,560 | 0,560 |
| LOSS | AC@1 | 0,07 | **0,133** | **0,133** | **0,133** | **0,200** |
| LOSS | AC@3 | 0,53 | **0,467** | **0,600** | **0,400** | **0,400** |
| LOSS | Avg@5 | 0,49 | 0,493 | **0,533** | 0,480 | 0,493 |
| AVERAGE | AC@1 | 0,10 | 0,111 | **0,156** | **0,122** | **0,133** |
| AVERAGE | AC@3 | 0,65 | 0,656 | 0,667 | **0,589** | **0,589** |
| AVERAGE | Avg@5 | 0,62 | 0,616 | 0,627 | 0,604 | 0,607 |

Số ô lệch mốc quá 0,02: lượt chính 7/21; thứ tự xáo 12/21; bỏ NaN trước 11/21 ở cả hai thứ tự. Riêng việc đổi thứ tự dòng đã làm một ô dao động tới 0,2 (DISK AC@1 0,133 → 0,333; LOSS AC@3 0,467 → 0,600), lớn hơn mọi độ lệch so với mốc. Cột "bỏ NaN trước" chỉ để đo ảnh hưởng của lỗi sắp xếp, không phải đề xuất sửa code.

### 3.5 Nguyên nhân khả thi của các ô lệch, và cái đã kiểm

| Nguyên nhân khả thi | Kiểm | Kết quả |
|---|---|---|
| Bản thư viện | chạy `py312` | không phải: 90/90 file giống |
| Hash seed, tiến trình | chạy lại 6 ca trong tiến trình mới (hash seed ngẫu nhiên mặc định; không ghi giá trị) | không phải: 6/6 file giống |
| Thứ tự dòng span của bộ đọc | xáo, phân tích sắp xếp (mục 3.4) | **có tác động đã chứng minh**: đổi thứ tự làm điểm đổi cùng cỡ hoặc lớn hơn độ lệch so với mốc. Không biết thứ tự của bộ đọc tác giả, nên không tái tạo được đúng số của bài |
| Độ dài cửa sổ | chạy ±600 s (mục 3.1) | **có tác động**: số ô lệch giảm từ 7/21 (±300 s) xuống 3/21 (±600 s). 3 ô còn lại mỗi ô 1 ca, nhỏ hơn biên độ mà thứ tự dòng gây ra (tới 3 ca một ô, đo ở ±300 s; chưa đo lại ở ±600 s) |
| Script chấm | so với `main.py` | không phải: 18/18 ô khớp |

## 4. BOCPD

Nguồn: `runs/py312-pin/bocpd.tar.gz` (`bocpd/chay.log`, `bocpd/tien-do.jsonl`); `cham/thong-ke.json` (`bocpd`).

| Chỉ số | README BARO (A) | Bảng 2 bài BARO (B) | Mình (`py312-pin`) | Lệch với README | Lệch với bài |
|---|---|---|---|---|---|
| Precision | 0,76 | 0,69 | 0,7634 | +0,003 | **+0,073** |
| Recall | 1,00 | 1 | 1,0000 | 0,000 | 0,000 |
| F1 | 0,87 | 0,82 | 0,8658 | −0,004 | **+0,046** |

- **Từng ca:** 100/100 ca có danh sách điểm đổi giống hệt `naive_bocpd.json` tác giả lưu sẵn trong dataset. Đây là phép so mạnh hơn P/R/F1: cùng đầu vào, cùng đầu ra ở mọi ca.
- **Lệch với bài:** README tác giả ghi số tái lập "a bit better than the numbers presented in the paper (Table 2)". Vì 100/100 ca trùng kết quả tác giả lưu, độ lệch với bài không đến từ môi trường hay cách chạy của mình. Bài dùng lượt chạy nào thì không kiểm được, vì không có dữ liệu của lượt đó.
- **Cách tác giả tính** (`baro/reproducibility.py`, `reproduce_bocpd`):
  - Ca có ít nhất một điểm đổi là TP. Recall = 1 vì ca nào cũng có điểm đổi.
  - Ca có điểm đổi đầu tiên trước điểm 300 của cửa sổ (trước mốc tiêm) là FP. Ở đây có 31 FP: cpu 10, loss 10, delay 9, mem 2.

## 5. Phạm vi ảnh hưởng của R1 (REVIEW T-002) tới phép kiểm BOCPD

R1 nêu: file telemetry RCAEval được cắt đối xứng quanh mốc tiêm, nên chỉ cần nhìn biên file là biết mốc tiêm. Kiểm trên đúng dữ liệu T-007 (`scripts/bien_file.py`, `runs/bien-file.tar.gz`):
- `fse-ob` (dữ liệu BOCPD): 100/100 ca có `time` từ mốc −360 s đến mốc +360 s, 360 dòng trước mốc và 361 dòng từ mốc. Mốc tiêm nằm đúng giữa file.
- RE2-OB (dữ liệu MicroRank, TraceRCA): `startTime` bắt đầu ở mốc −720 s ở 90/90 ca. Kết thúc ở +720 s ở 87 ca; 3 ca kết thúc sớm (mục 7).

Phạm vi ảnh hưởng:
1. **Không đổi kết luận "khớp" của phép kiểm BOCPD.** `reproduce_bocpd` vốn nhận mốc tiêm trực tiếp: nó cắt 300 điểm trước và 300 điểm sau mốc rồi mới chạy BOCPD, và chấm FP bằng vị trí 300. Phép kiểm này hỏi "code có ra đúng điểm đổi như tác giả không"; mốc tiêm là đầu vào hợp lệ của câu hỏi đó. Rò qua biên file không thêm thông tin nào ngoài mốc tiêm đã được cho.
2. **Số P/R/F1 ở đây không phải số phát hiện tự động.** Cửa sổ 600 điểm đặt mốc tiêm đúng ở điểm 300. Bỏ bước cắt mà chạy trên nguyên file `fse-ob` cũng không hết rò: theo R1, mốc vẫn nằm giữa file (điểm 360 trên 721). Vì vậy không dùng các số này, hay cách cắt này, cho chế độ tự phát hiện ở P3 (luật cứng 6). Cách xử lý biên file do giao thức P7/G1 quyết (như R1 đề xuất).
3. **MicroRank, TraceRCA** chạy ở chế độ biết mốc tiêm (mốc được truyền vào hàm). Cửa sổ ±300 s và ±600 s nằm trong file, nên biên file không thêm thông tin. R1 không ảnh hưởng hai phép kiểm này.

## 6. Khác biệt giữa `py312-pin` và `py312`

Các gói chính: pandas 2.2.3 / 3.0.6, scipy 1.14.1 / 1.17.1, scikit-learn 1.6.0 / 1.7.2, causal-learn 0.1.3.8 / 0.1.4.8; numpy 1.26.4 ở cả hai (`moi-truong-ec2.md`). So từng ca và từng ô (`cham/thong-ke.json`, `so_sanh`; `cham/so-moc-py312*.json`):

| Phương pháp | So từng ca | So từng ô với mốc |
|---|---|---|
| MicroRank | 90/90 file kết quả giống từng byte | 21/21 ô bằng nhau (0 ô khác) |
| TraceRCA | 90/90 file giống từng byte | 21/21 ô bằng nhau |
| BOCPD | 100/100 ca cùng danh sách điểm đổi | P, R, F1 bằng nhau (0,7634 / 1,0000 / 0,8658) |

Kết luận: trên dữ liệu này, bản thư viện không đổi kết quả của ba phương pháp. Biến thể ±600 s chỉ chạy bằng `py312-pin`.

## 7. Phép kiểm không cần nhãn

| Phép kiểm | Kết quả | Nguồn |
|---|---|---|
| Thứ hạng không rỗng, không lỗi | MicroRank 11 thao tác mỗi ca, TraceRCA 26–36; 0 ca rỗng, 0 ca lỗi ở mọi lượt | `cham/thong-ke.json` |
| Chạy lại 6 ca mỗi phương pháp, tiến trình mới | 12/12 file giống từng byte, ở cả hai bộ | `runs/<bộ>/{microrank,tracerca}-lai.tar.gz` |
| BOCPD so với kết quả tác giả lưu | 100/100 ca giống hệt, ở cả hai bộ | `runs/<bộ>/bocpd.tar.gz` |
| Hai bộ thư viện | giống hệt (mục 6) | `cham/thong-ke.json` |
| Xáo thứ tự span | MicroRank: điểm không đổi; TraceRCA: đổi (mục 3.4) | `runs/py312-pin/*-tron.tar.gz` |
| Giá trị trung gian | mục 2.3, 3.3, 3.4 | như trên |
| Kiểm hồi quy `chay_e2.py` sau khi thêm tùy chọn | 6/6 file TraceRCA giống lượt chính | `runs/py312-pin/tracerca-hoi-quy.tar.gz` |
| Cửa sổ, dữ liệu | cửa sổ ±300 s có 78 805–173 073 span, ±600 s có 165 561–344 204 span; tỉ lệ span trước/sau mốc (±300 s) 0,96–6,27, > 1,3 ở 8 ca | `cham/thong-ke.json` |

Ca đáng chú ý: `checkoutservice_cpu_2` có trace kết thúc ở mốc +39 s. Cửa sổ ±300 s chỉ có 10 846 span sau mốc, so với 67 959 trước mốc (`runs/bien-file.tar.gz`). Ca này được chấm như mọi ca; không loại ca nào.

## 8. Lượt chạy, kể cả lượt hỏng

- Lượt chính, chạy lại, BOCPD: `runs/py312-pin/`, `runs/py312/`.
- Phép kiểm thêm (`py312-pin`): `microrank-trung-gian`, `microrank-tron`, `tracerca-tron`, `tracerca-hoa`, `tracerca-hoa2`, `tracerca-hoa3`, `tracerca-hoi-quy`, `tracerca-L20`, `microrank-L20`. Kiểm biên file: `runs/bien-file.tar.gz`.
- Lượt hỏng: `runs/py312-pin/microrank-trung-gian-hong1.tar.gz`, do lỗi import trong script của tôi; đã sửa và chạy lại.
- Dựng máy và lượt thử: `runs/e0/`, `runs/e1/`, `runs/thu/`; log tổng `runs/*.log`.
- Lỗi ghi log trong script bash của tôi: dòng "mã thoát" ở các log tổng phiên 1 luôn in 0. Mọi khối đã kiểm độc lập (đủ ca, 0 Traceback); đã sửa script.

## 9. Không kiểm được trong task, và hệ quả

- **Bộ đọc trace của tác giả không công bố.** Hệ quả: với TraceRCA chỉ kết luận được "lệch 3/21 ô, nguyên nhân khả thi là thứ tự dòng của bộ đọc". Thứ tự này đã được chứng minh đủ làm đổi số cỡ độ lệch, nên không tái tạo được đúng số của bài. Với MicroRank, ±600 s khớp 21/21 ô, nhưng việc bộ đọc của tác giả cho cùng tập span chỉ là suy ra từ kết quả khớp.
- **Tác động của hai sai lệch MicroRank bản RCAEval so với bản gốc** (mục 2.3) chưa đo. Hệ quả: chưa biết thứ hạng gần cố định do sai lệch này hay do bản chất phương pháp trên dữ liệu OB.
- **Cấu hình cửa sổ của tác giả cho baseline trace** chỉ có bằng chứng gián tiếp (mục 1.3, WHY-16).
- **BOCPD theo cách tác giả cắt cửa sổ quanh mốc tiêm.** Hệ quả: chỉ chứng tỏ code BOCPD chạy đúng như tác giả; không nói gì về chế độ tự phát hiện (mục 5).
- **Không tái lập trên Train Ticket** (RE2-TT có ca khóa). Hệ quả: tính đúng trên dữ liệu cỡ Train Ticket chưa kiểm trực tiếp.
- **Thời gian** ở đây không phải số đo (máy dùng chung, có lúc chạy song song); đo chính thức thuộc T-008.

## 10. Hệ quả cho việc dùng số của ba phương pháp

Chỉ nêu sự kiện; quyết định thuộc Minh và các gói sau.
- **MicroRank (bản RCAEval):** khớp số của bài TORAI trong cấu hình ±600 s đã chạy; không xác nhận cơ chế MicroRank gốc. Số đó phản ánh một thứ hạng gần như cố định, không phản ánh khả năng tìm service gốc; bản RCAEval còn hai sai lệch so với bản gốc (mục 2.3).
- **Cửa sổ:** số của hai phương pháp trace đổi theo độ dài cửa sổ (±300 s hay ±600 s). T-007 dùng ±600 s làm cấu hình tham chiếu theo bằng chứng gián tiếp (mục 1.3, WHY-16); cửa sổ tác giả dùng cho baseline trace chưa xác minh.
- **TraceRCA (bản RCAEval):** kết quả phụ thuộc thứ tự dòng span do sắp xếp với NaN. Dùng số của nó thì phải cố định và ghi lại thứ tự đọc, và biết rằng một ô có thể dao động tới 0,2 chỉ vì thứ tự.
- **BOCPD:** code chạy đúng như tác giả. Cách tái lập của tác giả dùng mốc tiêm trong đầu vào, không dùng được cho tự phát hiện.
