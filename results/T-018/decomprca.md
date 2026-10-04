# Đọc bài DecompRCA: "Where Root Cause Analysis Fails: A Retrieval-Reranking Decomposition"

T-018, người làm Claude, ngày 04/10/2026. MRP P1 yêu cầu đọc bài này (MRP dòng 143).

**Nguồn.** arXiv 2609.36686v1 (29/09/2026), PDF 659 472 B (SHA-256 ở `nguon-tai.md`). Repo `cruiseresearchgroup/DecompRCA` commit `f99d2172ad3b…` (29/09/2026, "Camera-ready release" ngay trước đó). Dẫn bài dạng "PDF dòng N" là dòng của `D:\RCA-ext\work\T-018\nguon\decomprca.txt` (`pdftotext -layout`). Dẫn repo dạng `file:dòng`. Tác giả: Muhammad, **Luan Pham** (tác giả RCAEval, BARO, TORAI), Barrière, Shetty, Pulga, Salim (UNSW, Baker Hughes) (PDF dòng 4–9).

**Phạm vi.** Chỉ đọc bài và code. Không cài pipeline, không gọi LLM, không chạy baseline (prompt Đợt 1). Hai phép tính phụ không chạy phương pháp nào: Retrieval@K của bộ chọn ngẫu nhiên trên RE1-OB/RE1-SS (`runs/b9-retrieval-ngau-nhien.json`) và đếm cột (LOG).

## 1. Bài làm gì

Mọi phương pháp RCA ngầm có hai giai đoạn: **truy hồi** (retrieval) tạo một tập ứng viên C, và **xếp lại** (reranking) sắp thứ tự C. Độ đo top@k gộp hai giai đoạn. Bài tách chúng (PDF dòng 58–70, 413–433):

- Retrieval@K = tỷ lệ ca có nguyên nhân gốc nằm trong C, |C| ≤ K.
- Rerank@k = trong các ca đó, tỷ lệ nguyên nhân gốc đứng trong k vị trí đầu.
- top@k = Retrieval@K × Rerank@k. 1 − Retrieval@K là lỗi truy hồi; Retrieval@K − top@k là lỗi xếp lại.
- Với phương pháp chỉ trả một thứ hạng, lấy C = K phần tử đầu, nên Retrieval@K = top@K và Rerank@k = top@k / top@K (PDF dòng 427–431).

Bài dùng phép tách này để "kiểm toán" bốn bộ dữ liệu: ba bộ hệ thống vật lý (WADI n=14, SWaT n=36, HVAC n=48; "lỗi lan truyền") và RCAEval **RE1** (OB, SS, TT, mỗi bộ n=125; "lỗi trực tiếp") (PDF dòng 366–373, 1025–1038).

Rồi bài dựng một pipeline hai giai đoạn để chứng minh hai lỗi sửa độc lập được (PDF dòng 323–360, 857–956):
1. **Bộ truy hồi đa tín hiệu**, ngân sách K chia đều ba tín hiệu (5+5+5 khi K=15), lấy hợp đã bỏ trùng:
   - độ lớn lệch mag(s_i) = max_{t∈F} z^rob_i(t), RobustScaler học trên cửa sổ nền (có dấu, như BARO của RCAEval);
   - khởi phát sớm ons(s_i) = −t_i, t_i = tick đầu tiên trong cửa sổ lỗi có |(x − μ_B)/σ_B| ≥ 1,5;
   - đổi trạng thái rời rạc stc(s_i): metric có ≤ 5 giá trị khác nhau mà mode cửa sổ lỗi khác mode cửa sổ nền, xếp theo lúc đổi đầu tiên.
2. **Bộ xếp lại LLM**: một lần gọi `gpt-oss-120b` (T = 1, 3 lượt, không seed) với mỗi ứng viên một dòng bằng chứng (z-score, độ trễ khởi phát, trung bình trước/sau); tùy chọn thêm một tài liệu mô tả hệ thống (DK).

Mọi phương pháp dùng cùng mốc phát hiện t_det. Với RCAEval, t_det **là mốc tiêm** (PDF dòng 979–981), tức chế độ a của MRP P3.

## 2. Kết quả chính (số lấy từ PDF)

| Nội dung | Số | PDF dòng |
|---|---|---|
| Retrieval@15 chỉ dùng độ lớn: hệ vật lý | 0,35–0,64 | 93–95, 387–389 |
| Retrieval@15 chỉ dùng độ lớn: RE1-OB / SS / TT | 1,00 / 1,00 / 0,98 | 393–395 |
| Retrieval@5 chỉ dùng độ lớn: RE1-OB / SS / TT | 0,98 / 1,00 / 0,91 | 393–395 |
| BARO top@1: RE1-OB / SS / TT | 0,784 / 0,856 / 0,560 | 527 |
| CIRCA (PC) top@1: RE1-OB / SS / TT | 0,536 / 0,632 / 0,320 | 530 |
| PageRank (PC) top@1: RE1-OB / SS / TT | 0,112 / 0,136 / 0,008 | 532 |
| LLM không DK top@1: RE1-OB / SS / TT | 0,875 / 0,872 / 0,653 | 537 |
| Lỗi xếp lại của LLM trên RE1-TT (Retrieval@15 − top@1) | 0,26 | 472 |
| Đổi t_det ±1–2 phút: thay đổi Retrieval@15 tối đa trên RCAEval | 3,2 điểm % | 1453–1463 |
| Đồ thị học từ dữ liệu bình thường nhiều ngày: không hơn đồ thị từng ca | CIRCA RE1-OB 0,632 (global FCI) so với BARO 0,784 | 1479–1511 |

Kết luận tác giả: trên hệ vật lý, cả hai lỗi cùng lớn; trên microservice, truy hồi gần như xong và lỗi nằm ở xếp lại; trong các thiết lập chính (đầu-cuối, tập ứng viên của bộ truy hồi, đồ thị học từ dữ liệu bình thường nhiều ngày), phương pháp đồ thị (PC/FCI + PageRank/RandomWalk/CIRCA) không rõ ràng hơn baseline thống kê tốt nhất (PDF dòng 540–556, 625–632). Ngoại lệ do chính bài nêu: với tập ứng viên rút ngẫu nhiên có chứa nguyên nhân (dùng nhãn để bảo đảm), CIRCA-FCI trên SWaT đạt top@1 0,400, hơn BARO 0,286 và LLM 0,362 (PDF dòng 1274–1278; `method/experiments/controlled_pools.py:61-107`). Thiết lập đó dùng nhãn nên không phải bằng chứng đồ thị thắng khi vận hành thật, nhưng cho thấy thành phần tập ứng viên làm đổi kết luận (REVIEW R2).

Hạn chế tác giả tự nêu (PDF dòng 633–637): bộ lỗi lan truyền nhỏ và chỉ ở hệ nước/tòa nhà; lợi ích trên hệ vật lý cần t_det sai dưới 5 phút; **tham số bộ truy hồi chỉnh trên chính các bộ dữ liệu này**; DK chưa được nạp thích ứng; LLM không tất định.

## 3. Bảng kiểm khẳng định (PDF và repo)

| # | Khẳng định | PDF | Repo | Kết luận | Bằng chứng |
|---|---|---|---|---|---|
| K1 | Đăng ở NeurIPS 2026, Evaluations & Datasets | dòng 52 | README dòng đầu | **Khớp** | Trang arXiv ghi "Accepted at NeurIPS 2026 (Evaluations & Datasets Track)". MRP dòng 143 ghi đúng |
| K2 | RCAEval dùng là **RE1** (OB, SS, TT), 125 ca mỗi bộ, chỉ metric | 366–370, 1025–1031 | `method/datasets/rcaeval_dataset.py:28` (`SUITES` chỉ RE1) | **Khớp** | Không dùng RE2, không dùng trace/log |
| K3 | RE1-OB, SS, TT có 95, 63, 241 cột metric | 1031 | — | **Khớp** với OB, SS (đếm hợp các ca); TT chưa kiểm (không có dữ liệu RE1-TT) | Hợp cột 125 ca: OB 95, SS 63; mỗi ca chỉ 49–59 (OB), 57–63 (SS) cột (`runs/b9-retrieval-ngau-nhien.json`, khóa `hop_cot_tho_cac_ca`, `so_cot_tho_moi_ca_min_max`) |
| K4 | Cửa sổ 600 dòng mỗi phía "như RCAEval (--length 20)"; thực tế 360/361 dòng phần lớn ca | 1026–1030 | `rcaeval_dataset.py:40-41, 208-221` | **Khớp** | — |
| K5 | "Lặp lại chính xác tiền xử lý của `main-ase.py` (ASE'24)" | 1032–1035 | `rcaeval_dataset.py:45-74` | **Khớp một phần** | Bước cột khớp: bỏ cột hằng từng cửa sổ, giữ giao, mem → MB, giữ cả `_latency-50` và `_latency-90` (`main-ase.py` chỉ bỏ `_lat_50`/`_lat_99` của sock-shop, mà RE1-SS dùng tên `_latency-50`, nên không bỏ gì). Cửa sổ thì không: `main-ase.py` ở commit `fb8f20a` mặc định `--length 10` = 300 dòng mỗi phía (`main-ase.py:166-168`), còn loader dùng 600 như `main.py` hiện tại. Với RE1-SS (721 dòng/ca) hai cách gần như cùng dữ liệu; với 50 ca RE1-OB có 600 dòng trước mốc thì khác. Ảnh hưởng tới số: chưa kiểm |
| K6 | Bỏ `_latency-50`, đổi `_latency-90` như `main.py` mới làm BARO "0,57 trên Sock Shop (so với 0,95 công bố)" | 1033–1035 | chú thích `rcaeval_dataset.py:48-52` | **Chưa kiểm; có bằng chứng ngược một phần** | T-006 chạy BARO với đúng tiền xử lý kiểu `main.py` trên `fse-ss` (trùng 100/125 ca RE1-SS, T-006 mục 2.2): Avg@5 0,952 (cửa sổ 10), 0,960 (cửa sổ 20); AC@1 0,840 / 0,850 (`results/T-006/cham/bang-so-sanh.md:283-305`). Không thấy mức 0,57. Nguyên nhân khả thi khác: con số 0,57 là độ đo khác, gồm 25 ca disk, hoặc một biến thể `main.py` khác. Không chạy lại vì prompt cấm chạy benchmark ở phần này |
| K7 | top@k = Retrieval@K × Rerank@k | 423–425 | `method/evaluation/metrics.py:10-19, 71-75, 120-147` | **Khớp** | Khi truyền tập ứng viên riêng, "trúng" đòi nguyên nhân vừa ở k đầu vừa trong C, nên đẳng thức luôn đúng theo định nghĩa |
| K8 | Retrieval@K áp cho mọi thứ hạng, K là cỡ tập ứng viên | 427–433 | `method/runners/compute_retrieval_recall_cumulative.py:56-74, 135-137` | **Khớp, nhưng K có hai đơn vị** | Bảng 1 với RCAEval: K là số **metric**; trúng nếu bất kỳ metric nào của service gốc nằm trong K metric. RCAEval `Evaluator.retrieval_service` (cài theo bài này): K là số **service** trong thứ hạng mức service (`RCAEval/benchmark/evaluation.py:178-184`; `main.py:460-467` ghi "K is a retrieval depth, not the candidate pool size"). Hai con số cùng tên không so trực tiếp được |
| K9 | Microservice: "truy hồi gần như đã giải (98–100 %)" | 25–26, 93–95, 439–441 | — | **Số đúng, cách đọc cần sửa** | Bộ chọn ngẫu nhiên 15 metric, quy về service như K8, đạt Retrieval@15 = 0,816 (RE1-OB), 0,901 (RE1-SS); ở K=5: 0,392 / 0,500 (`runs/b9-retrieval-ngau-nhien.json`). Để tính số này, script đã đọc toàn bộ số đo và mốc tiêm RE1 (bỏ cột hằng theo từng cửa sổ như loader của bài), vượt phạm vi “chỉ đọc tên cột” của SPEC, nằm trong giới hạn của prompt; Minh duyệt giữ số ngày 04/10 (REVIEW R5; SPEC thay đổi mục 10). RE1-OB trung vị 13 service, 54 metric/ca; service gốc trung vị 5 metric. Vậy ở K=15 phần lớn mức 0,98–1,00 là do cấu trúc (ít service, mỗi service nhiều metric), không phải do bộ truy hồi giỏi. Ở K=5 độ lớn lệch (0,98 / 1,00) hơn ngẫu nhiên rõ. RE1-TT chưa kiểm |
| K10 | Định nghĩa ba tín hiệu và cách chia ngân sách | 868–889 | `method/algorithms/rca/candidate_selection.py:18-43, 46-77, 80-109, 112-125` | **Khớp** | — |
| K11 | LLM: `gpt-oss-120b` qua Groq, T = 1,0, 3 lượt, `max_tokens` 4096, không seed | 406–409, 948–956 | `method/runners/run_llm_balanced.py:265-273`; `method/runners/_common.py:270` | **Khớp**; số LLM **chưa kiểm** | Repo không phát hành phản hồi LLM đã lưu (README, mục "LLM rows"), nên chỉ tái lập được bằng API trả phí; trong phạm vi task không chạy |
| K12 | "Mọi baseline dùng tham số mặc định công bố [RCAEval]"; "cài đặt baseline kế thừa từ RCAEval" | 403–404, 972–973 | `method/algorithms/rca/rcd.py:5`, `epsilon_diagnosis.py:5` (PyRCA); `circa.py:22-28` (CIRCA gốc NetManAIOps, RHT + DA) | **Lệch câu chữ** | Chỉ BARO chạy qua RCAEval (`baro.py:19-28`). RCD, ε-Diagnosis dùng PyRCA; CIRCA dùng bản gốc có thêm DA. Phụ lục C (PDF 1050–1084) ghi đúng điều này; câu ở §6.2 và Phụ lục A thì không. Hệ quả: số RCD, CIRCA của bài **không** cùng cài đặt với RCAEval, TORAI, hay T-006 |
| K13 | Tài liệu DK "không bao giờ chỉnh theo kết quả lỗi trên tập test", không mã hóa nguyên nhân gốc | 957–968 | `method/prompts/rcaeval/TrainTicket_Context_Light.md` | **Chưa kiểm được là có rò hay không** | Sơ đồ "Request Topology (Key Paths)" của tài liệu Train Ticket có đủ 5 service gốc của RE1-TT (auth, order, route, train, travel; danh sách lấy từ `results/T-002/public-metadata/run-001/hf-tree.json`), trong 16/43 service ứng dụng tài liệu liệt kê. Nếu 16 service được chọn ngẫu nhiên, xác suất chứa đủ 5 là C(16,5)/C(43,5) ≈ 0,0045. Giải thích khác hợp lý: RCAEval chọn service trung tâm để tiêm lỗi, và mô tả "đường chính" tự nhiên gồm service trung tâm. Kiểm soát ẩn danh (Bảng 14) kiểm việc nhớ tên, không kiểm điều này. Hệ quả: so "LLM có DK" với baseline phải tính tới khả năng DK mang thông tin trước về vị trí lỗi |
| K14 | Bộ lọc của baseline đồ thị (gần hằng ≥ 95 %, tương quan ≥ 0,9999) không loại nguyên nhân gốc ở RCAEval | 1065–1070 | `method/algorithms/cd/per_scenario.py:58, 76, 165, 184` | **Khớp phần code**; số ca loại chưa kiểm | — |
| K15 | Đổi t_det ±1, ±2 phút trên RCAEval | 1431–1463 | `method/experiments/tdet_sensitivity.py:42-43` | **Khớp phần code** | Kết quả chưa kiểm (cần chạy) |

## 4. Hệ quả cho P3 (giao thức, tập ứng viên, độ đo)

Đây là đề xuất cho P3, chưa phải quyết định. Lựa chọn nào dùng trong kết quả phải có mục WHY trước (chờ WHY, xem `de-xuat-tai-lieu-chung.md`).

1. **Báo thêm Retrieval@K và Rerank@1 bên cạnh MRR, Hit@k.** Rẻ: tính được từ thứ hạng đã có, cho mọi phương pháp. Nói được phương pháp hỏng ở "không tìm ra" hay "tìm ra nhưng xếp sai". RCAEval `259ea41` đã có sẵn (`main.py --report-decomposition K`; `Evaluator.retrieval_service`, `rerank_service`). Phải chốt **đơn vị của K** (service, như RCAEval) và ghi rõ, vì Bảng 1 của bài dùng K metric (K8). Kèm mức ngẫu nhiên, tính trên **tập ứng viên thực dùng** của từng phương pháp hoặc tập chung đã chốt. Không dùng `--report-chance` của RCAEval làm căn cứ cho mọi phương pháp: nó đếm cột sau tiền xử lý trên cửa sổ ghép (`main.py:320-330`), còn BARO tiền xử lý hai cửa sổ riêng rồi lấy giao, nên cột hằng trước mốc mà đổi sau mốc được đếm nhưng không được xếp (REVIEW R4).
2. **Tập ứng viên phải cố định và giống nhau giữa các phương pháp.** Bài cho thấy chỉ đổi tập ứng viên (15 so với toàn bộ) đã đổi thứ tự LLM và baseline (Bảng 4, PDF dòng 583–605). Bảng 4 là đối chứng có dùng nhãn (chèn nguyên nhân vào tập khi bộ truy hồi bỏ sót), đo bước xếp lại có kiểm soát, không phải giao thức P3 không nhãn. PageRank, RandomWalk chỉ xếp các nút có trong đồ thị học được; nguyên nhân không có trong thứ hạng tính là trượt (PDF 1097–1098). MRP P3 đã yêu cầu "cùng tập ứng viên"; cần thêm: phương pháp trả thứ hạng thiếu ứng viên thì ghi riêng số ca thiếu, không lấp bằng thứ tự cột (cùng tinh thần MRP P3 về ca lỗi).
3. **Mức đánh giá service phải chốt quy tắc quy đổi** metric → service (bài: phần trước `_`, gộp `-db` vào service chủ, `compute_retrieval_recall_cumulative.py:56-57`). RE2-TT có pod `ts-*-mongo`; quy tắc gộp phải ghi rõ cho từng dataset.
4. **Cửa sổ và tiền xử lý làm đổi số.** Bài dùng 600 dòng mỗi phía, giữ cả hai phân vị độ trễ, và nói tiền xử lý này cần để tái lập BARO của RCAEval (K5, K6). T-006 đã thấy cửa sổ đổi kết quả (Q-54). Hai lựa chọn này phải chốt ở G1 cùng độ dài cửa sổ.
5. **So số với bài phải cùng cài đặt.** RCD, ε-Diagnosis (PyRCA), CIRCA (bản gốc có DA) của bài khác cài đặt RCAEval (K12). Số của bài chỉ là mốc so hợp lệ cho BARO.
6. **Chế độ b.** Bài cho thấy trên microservice, lệch t_det ±2 phút đổi Retrieval@15 tối đa 3,2 điểm %, trên hệ vật lý ±5 phút đổi tới 27 điểm % (PDF 1453–1463). P3 chế độ b nên báo độ nhạy của RCA theo độ trễ của bộ phát hiện (BOCPD, N-Sigma, GDN), vì "bộ phát hiện quyết định nền truy hồi" (PDF dòng 104–105, 488–491).
7. Bài **không** đặt ra quy tắc nào về dùng nhãn khác MRP; DK là đầu vào bên ngoài, phải coi như một nguồn thông tin trước cần kiểm (K13) nếu P8 dùng LLM với tài liệu hệ thống.

## 5. Hệ quả cho P4 (giả thuyết, đều **chưa kiểm**)

| # | Giả thuyết | Giả định | Sai khi | Việc kiểm được nó |
|---|---|---|---|---|
| H1 | Trên RE2-TT dev, ca BARO xếp sai phần lớn là **lỗi xếp lại**: service gốc nằm trong 5 service đầu nhưng không đứng đầu | RE2-TT giống RE1 ở chỗ lỗi hiện rõ tại service gốc | Lỗi mạng (delay, loss) lan sang service gọi mạnh hơn tại gốc | P3: tính Retrieval@5, Rerank@1 theo service, tách theo loại lỗi và theo service gốc |
| H2 | Ở chế độ a, lỗi truy hồi của phương pháp thống kê tập trung ở vài ô (service gốc × loại lỗi), không đều | Mỗi ô có cơ chế hiện tín hiệu khác nhau | Lỗi truy hồi rải đều mọi ô | P3/P4: bảng Retrieval@K theo ô (QT15) |
| H3 | Ở CIRCA-PC, một phần lỗi là truy hồi tại bước tiền xử lý: cột của service gốc bị bỏ vì hằng/gần hằng hoặc trùng tuyến tính | Bài thấy điều này ở hệ vật lý (1/14, 2/36, 12/48 ca), không thấy ở RE1 | RE2-TT có ít cột hằng ở service gốc | Đếm số ca cột của service gốc còn sau tiền xử lý của CIRCA; đối chiếu `cot-re2tt/cot.csv` (cột error hằng ở mọi ca) |
| H4 | Ở chế độ b, bộ phát hiện trễ vài phút làm giảm truy hồi chủ yếu ở lỗi lan truyền | Bài: microservice bền với ±2 phút | Trễ của bộ phát hiện RE2-TT dưới 2 phút | P3: đo trễ phát hiện; chạy RCA với t_det lệch như bài |
| H5 | Nếu RE2-TT thuộc "chế độ lỗi trực tiếp" (service gốc là service lệch nhất), đồ thị khó giúp xếp hạng hơn thống kê | Phát biểu của bài cho RE1 chuyển sang RE2 | RE2-TT có nhiều ca triệu chứng lan (MRP tiêu chí 7) | P2/G1 đếm tiêu chí 7; P4 đếm tỷ lệ ca service gốc có điểm độ lớn cao nhất |
| H6 | Phần "LLM hơn baseline" trên microservice đến một phần từ thông tin trước về service trung tâm | K13 | Kiểm soát với tài liệu DK bỏ sơ đồ đường chính vẫn cho cùng mức | P8 (nếu dùng LLM): so tài liệu có và không có sơ đồ đường chính |

## 6. Hệ quả cho việc chọn dataset ở G1

1. **RE1 không thỏa MRP tiêu chí 3** (không có trace) và bài chỉ dùng metric. Số của bài trên RE1-TT không làm mốc cho phương pháp dùng trace. Bài cũng không dùng RE2, RE3, Nezha, Eadro, LEMMA.
2. **Bằng chứng về "phân xử được".** Bài đặt RCAEval RE1 vào chế độ lỗi trực tiếp: ở K=5, độ lớn lệch đã truy hồi 0,91–1,00 (PDF 393–395). Nếu RE2-TT cũng vậy, nó yếu cho câu "đồ thị giúp khi nào" ở bước xếp hạng (WHY-03, MRP tiêu chí 7). Đây là lý do để G1 **đếm tiêu chí 7 trên dev trước khi chọn**, không phải lý do loại RE2-TT (chưa kiểm trên RE2).
3. **Mức "truy hồi dễ" một phần do cấu trúc.** Với 11–13 service, bộ ngẫu nhiên 15 metric đã truy hồi 0,82–0,90 (K9). Dataset nhiều service phân xử truy hồi tốt hơn dataset ít service; RE2-TT có 68 pod có cột cpu ở cả 30 ca dev (`cot-re2tt/loai.csv`). Đây là thêm một lý do ưu tiên hệ cỡ Train Ticket (cùng hướng LESSONS SL33).
4. **Bộ lỗi lan truyền của bài là hệ vật lý** (WADI, SWaT, HVAC). Ngoài miền DT18 và OT đã bỏ khỏi khảo sát (Q-47). Không phải ứng viên. Dataset có lan truyền cung cấp các ca truy hồi khó để kiểm vai trò đồ thị; phép tách truy hồi/xếp lại vẫn tính được trên dataset lỗi trực tiếp (RE1-TT: lỗi truy hồi 0,09, lỗi xếp lại 0,26; PDF dòng 472). FlashTicket (P10) có thể cung cấp ca lan truyền (REVIEW R3).
5. **Số service gốc.** RE1-TT và RE2-TT cùng 5 service gốc (auth, order, route, train, travel; `hf-tree.json` của T-002; LESSONS ST1). Kết luận của bài trên RE1-TT không khái quát được sang vị trí khác trong đồ thị (WHY-03).

## 7. Liên hệ với GDN và các bộ phát hiện (Q-30)

- Bài nói bộ phát hiện quyết định nền truy hồi (PDF dòng 104–105). GDN cho điểm lệch từng metric ã_i(t) (`ho-so-gdn.md` mục 2). Thứ tự metric theo ã_i tại tick báo động là một **bộ truy hồi** đánh giá được bằng Retrieval@K mức service. Bài GDN gọi đây là khả năng khoanh cảm biến (RQ4) nhưng không đo. Đề xuất cho P3 (**chưa kiểm**): báo Retrieval@K của thứ tự metric GDN tại tick báo động đầu tiên, cùng định nghĩa K như mục 4.1. Sai khi tick báo động đầu tiên là báo động sai (trước sự cố) — khi đó thứ tự metric không liên quan sự cố.
- Tín hiệu "khởi phát sớm" của bài và độ trễ phát hiện của GDN đo cùng một thứ: thời điểm lệch. Lỗi GDN chuẩn hóa theo trung vị/IQR của cả file test (`ho-so-gdn.md` mục 5 dòng 4) làm thời điểm vượt ngưỡng phụ thuộc dữ liệu sau đó.

## 8. Giới hạn của việc đọc này

- Không tái lập số nào của bài. Số LLM cần API trả phí và không có phản hồi lưu sẵn (K11). Số baseline cần dữ liệu RE1-TT và WADI/SWaT (cần xin) và chạy hàng giờ (README "Runtime").
- K6, K13 chỉ là nghi vấn có bằng chứng một phần; không kết luận bài sai.
- Đọc bản v1 trên arXiv; bản hội nghị có thể khác.
