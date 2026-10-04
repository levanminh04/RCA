# Phản biện T-018

- **Người phản biện:** Codex — **Ngày:** 04/10/2026 — **Commit/diff đã đọc:** không có commit gốc hoặc diff của task; phản biện danh sách file Minh giao, không dùng git diff.
- **Đã đọc:** `AGENTS.md`, `docs/STATE.md`, SPEC và toàn LOG T-018, `tasks/_MAU/REVIEW.md`; toàn bộ văn bản, CSV, JSON, log và script trong `results/T-018/`; bài GDN và DecompRCA qua bản văn bản trích từ hai PDF, kiểm hash PDF/text theo `nguon-tai.md`; dữ liệu GDN đã dựng, trọng số và mảng trong `D:/RCA-ext/work/T-018/gdn/`; các file mốc tiêm trong `nguon/rcaeval-inject/`. Đối chiếu code GDN, các đường loader/retriever/graph/reranker/evaluation/controlled-pool của DecompRCA và RCAEval đúng revision Minh giao. Đọc thêm `docs/MRP.md`, `WHY.md`, `DECISIONS.md`, `LESSONS.md`, hai nguồn DT18/hướng dẫn cô, danh sách T-001, các đầu vào T-005/T-006 và thẻ dataset liên quan.
- **Nguồn chính thức:** [GDN v1](https://arxiv.org/abs/2106.06947v1), [DecompRCA v1](https://arxiv.org/abs/2609.36686v1). Revision code/hash nguồn theo manifest của task. Số dòng PDF dưới đây tính bằng ký tự xuống dòng trong các file `gdn.txt`, `decomprca.txt`, như script dẫn dòng của task.

## Kết luận chung

Không phát hiện lỗi làm sai các số chính, phép tính tay hoặc quyết định báo động GDN đã lưu; không có finding CHẶN. Có sáu điểm KHÔNG CHẶN cần sửa hoặc Minh quyết trước khi dùng hồ sơ làm căn cứ cho G1/P3/P4. Hồ sơ có đủ cấu trúc đầu ra của SPEC, nhưng phần đối chiếu tiền xử lý và một số hệ quả DecompRCA chưa chính xác hoàn toàn.

## Các điểm

### R1. Bỏ sót khác biệt về đáp án và điền ô thiếu của preprocessing GDN — KHÔNG CHẶN

- **Ở đâu:** B1; `results/T-018/ho-so-gdn.md:27`, mục 5 và bảng đường nhãn mục 8.1.
- **Sai gì:** câu “Bài ghi cùng các bước” chưa đúng về cách gộp nhãn khi giảm mẫu. Hồ sơ cũng chưa nêu đường dùng dữ liệu test tương lai trong script tiền xử lý mẫu.
- **Bằng chứng:** bài `gdn.txt:341–343` lấy nhãn phổ biến nhất trong khối 10 giây. Code `D:/RCA-ext/src/GDN/scripts/process_swat.py:30–32` lấy max nhãn. Khối nhãn `[1,0,0,0,0,0,0,0,0,0]` thành 1 theo code, 0 theo bài. Cùng file, dòng 50 điền NaN bằng trung bình của toàn tập test.
- **Hậu quả:** cách gộp nhãn có thể đổi Precision, Recall, F1 tại biên sự cố hoặc sự cố ngắn khi tái lập bảng bài. Nếu test có NaN, điểm ở quá khứ có thể dùng giá trị tương lai ngay từ đầu vào.
- **Đã xét đoạn phản bác:** task chưa benchmark SWaT/WADI và T-018 dùng ffill/0, không dùng script mẫu này. Vì vậy đây là thiếu sót của hồ sơ kỹ thuật, không phải rò nhãn hoặc số sai đã xảy ra trong các lượt T-018.
- **Đề xuất sửa:** sửa câu “cùng các bước”; bổ sung khác biệt gộp nhãn vào mục 5 và đường `test.mean()` có điều kiện vào mục 8.1. Không cần chạy benchmark mới.

### R2. Kết luận “không lúc nào” bỏ sót ngoại lệ đồ thị của chính bài — KHÔNG CHẶN

- **Ở đâu:** B9; `results/T-018/decomprca.md:44`; cách dẫn Bảng 4 tại dòng 73.
- **Sai gì:** kết luận đồ thị không lúc nào hơn baseline thống kê được viết rộng hơn các thiết lập chính của bài.
- **Bằng chứng:** `decomprca.txt:1274–1278` nêu đối chứng pool ngẫu nhiên chứa nguyên nhân: trên SWaT, CIRCA-FCI top@1 = 0,400, BARO = 0,286, LLM = 0,362. Bài tự gọi đây là một thiết lập đồ thị thắng baseline thống kê tốt nhất. `method/experiments/controlled_pools.py:61–107` dùng nhãn để chọn/thêm metric gốc; đây là oracle-controlled pool (tập ứng viên có đáp án được bảo đảm bằng nhãn).
- **Hậu quả:** nếu dùng câu phổ quát này ở P4/G1, có thể bỏ cơ chế đồ thị dù bài có phản ví dụ và cho thấy thành phần pool ảnh hưởng kết luận. Bảng 4 đo xếp lại có kiểm soát, không phải giao thức P3 không nhãn.
- **Đã xét đoạn phản bác:** các đoạn PDF 540–556, 625–632 hỗ trợ kết luận trên các thiết lập chính, gồm end-to-end, pool của retriever và đồ thị global. Ngoại lệ pool ngẫu nhiên có dùng nhãn cũng không chứng minh đồ thị thắng trong vận hành thực tế. Hai giới hạn này cần cùng được giữ.
- **Đề xuất sửa:** giới hạn câu dòng 44 vào các thiết lập chính; thêm ngoại lệ trên và ghi rõ Bảng 4 là đối chứng có dùng nhãn để bảo đảm gốc trong pool.

### R3. Lan truyền không phải điều kiện cần để tách hai loại lỗi — KHÔNG CHẶN

- **Ở đâu:** B9/G1; `results/T-018/decomprca.md:96`.
- **Sai gì:** câu “chỉ có bộ dữ liệu có lan truyền thật mới tách được lỗi truy hồi khỏi lỗi xếp lại” sai về điều kiện áp dụng phép tách.
- **Bằng chứng:** ngay dòng 13–16 của hồ sơ và PDF 413–433 định nghĩa phép tách cho mọi thứ hạng. Với pipeline đa tín hiệu trên RE1-TT, bài báo Retrieval@15 = 0,912 và top@1 = 0,653 (PDF 472): lỗi truy hồi = 0,088; lỗi xếp lại = 0,259. Bài xếp RE1 vào nhóm lỗi trực tiếp, vẫn tách được cả hai.
- **Hậu quả:** G1 có thể đánh giá sai khả năng phân xử của dataset lỗi trực tiếp cho RQ1/P4. Khả năng tính phép tách khác khả năng kiểm giá trị của cấu trúc đồ thị.
- **Đã xét đoạn phản bác:** dòng 94 nói không loại RE2-TT và H1 còn dự đoán lỗi xếp lại trên RE2-TT. Các đoạn này hợp lý nhưng không giới hạn mệnh đề “chỉ” ở dòng 96.
- **Đề xuất sửa:** thay bằng: “Dataset có lan truyền cung cấp các ca truy hồi khó để kiểm vai trò đồ thị; phép tách truy hồi/xếp lại vẫn tính được trên dataset lỗi trực tiếp.”

### R4. `--report-chance` không bảo đảm đúng tập ứng viên thực dùng — KHÔNG CHẶN

- **Ở đâu:** B9, đề xuất P3; `results/T-018/decomprca.md:72`.
- **Sai gì:** hồ sơ nói mức ngẫu nhiên của flag này được tính trên “đúng số ứng viên sau tiền xử lý”, nhưng bộ đếm và phương pháp có thể dùng các tập khác nhau.
- **Bằng chứng:** RCAEval `main.py:325–329` đếm cột sau preprocessing trên cửa sổ ghép. BARO `RCAEval/e2e/baro.py:23–41` tiền xử lý riêng hai cửa sổ rồi giữ giao; `RCAEval/io/time_series.py:4–5` bỏ cột hằng. Phản ví dụ: cột `s_x` có pre = `[0,0]`, post = `[1,2]`. Bộ đếm trên chuỗi ghép giữ nó, BARO loại nó vì hằng ở pre. Nếu đây là metric duy nhất của service s, cả số ứng viên service cũng khác.
- **Hậu quả:** chance/lift của P3 có thể bị tính trên tập mà phương pháp không xếp hạng. Mức đó không tự giải thích được phần kết quả do cấu trúc tập ứng viên.
- **Đã xét đoạn phản bác:** dòng 73 đề xuất một tập chung cho P3. Đây vẫn là đề xuất, không làm bộ đếm của code hiện tại thành đúng với mọi phương pháp. Chú thích trong code chính thức cũng không thay thế việc kiểm đường xử lý thực tế.
- **Đề xuất sửa:** bỏ bảo đảm trên; ghi mức ngẫu nhiên phải theo tập ứng viên thực dùng hoặc tập chung đã chốt. Không dùng flag như căn cứ đúng cho mọi phương pháp nếu chưa khớp tập đó.

### R5. B9 đã đọc số đo RE1 ngoài giới hạn đọc của SPEC — KHÔNG CHẶN

- **Ở đâu:** B9; `tasks/T-018-ho-so-gdn-decomprca/SPEC.md:29,99`; `results/T-018/scripts/retrieval_ngau_nhien.py:51–58`.
- **Sai gì:** SPEC chỉ cho đọc tên cột/tên ca RE1-OB và RE1-SS. Script đã đọc toàn CSV và mốc tiêm, tách pre/post, rồi dùng giá trị để loại cột hằng.
- **Bằng chứng:** dòng 51 đọc `inject_time.txt`; dòng 52 gọi `pd.read_csv(f)` không giới hạn header; dòng 56–58 lọc cửa sổ theo mốc và giữ giao cột. LOG ghi đã chạy script; `b9-retrieval-ngau-nhien.json` có kết quả trên 125 ca mỗi bộ. Không có mục mở rộng quyền đọc này trong phần thay đổi SPEC.
- **Hậu quả:** các số ngẫu nhiên 0,816/0,901 là kết quả phụ thuộc số đo và mốc tiêm, không phải phép tính chỉ từ schema được cho phép. Nguồn gốc/phạm vi được duyệt của bằng chứng dùng tại K9 và E2 bị mô tả thiếu.
- **Đã xét đoạn phản bác:** đây không phải chạy RCA, không có bằng chứng mở dữ liệu khóa, và nhãn chỉ dùng để tính mức ngẫu nhiên. Các điều đó không làm thao tác đọc trở thành chỉ đọc tên cột.
- **Đề xuất sửa:** ghi rõ độ lệch này vào báo cáo task và trình Minh quyết có chấp nhận dùng các kết quả đã có không. Chưa coi chúng là bằng chứng nằm đúng phạm vi SPEC. Không tái chạy để sửa việc đã xảy ra.

### R6. Lựa chọn đã dùng trong kết quả chưa có mục WHY trước khi dùng — KHÔNG CHẶN

- **Ở đâu:** B3/B5–B7; `results/T-018/ho-so-gdn.md:17`; `de-xuat-tai-lieu-chung.md:5–22`; `docs/WHY.md`.
- **Sai gì:** L*, điền trung vị khi thiếu cột và chuẩn hóa lỗi bằng thống kê val đã được dùng trong kết quả chẩn đoán, nhưng WHY mới nằm ở đề xuất E1 chờ duyệt. AGENTS luật cứng 3 yêu cầu mục WHY trước khi dùng lựa chọn quan trọng trong kết quả.
- **Bằng chứng:** hồ sơ tự ghi các lựa chọn này chưa có WHY. Các bảng B3/B6/B7 và kết quả biến thể b đã sử dụng chúng. WHY hiện có chưa chứa mục GDN tương ứng.
- **Hậu quả:** phần lý do chính thức của kết quả biến thể còn thiếu; chưa thể chuyển các lựa chọn này thành cấu hình P3 đã chốt.
- **Đã xét đoạn phản bác:** SPEC đã ghi quy tắc chọn trước và lý do, nên không có căn cứ nói lựa chọn được tối ưu sau khi nhìn kết quả. E1 cũng được ghi đúng là đề xuất; đây không làm số đã tính sai. Phạm vi ghi cấm sửa WHY giải thích vì sao người làm chỉ đề xuất, nhưng không đáp ứng điều kiện phải có WHY trước khi dùng.
- **Đề xuất sửa:** Minh quyết phần lý do cho các lựa chọn đã dùng, ghi đúng thời điểm vào WHY qua phạm vi được duyệt. Tách rõ lý do của phép chẩn đoán T-018 khỏi cấu hình P3 còn mở; không ghi như đã quyết trước thực nghiệm. Không cần tính lại số chỉ để hoàn thiện lý do.

## Điều đã kiểm và thấy đúng

- **Tiêu chí xong:** đủ hồ sơ 7 mục, đường nhãn, chế độ b và yêu cầu đầu vào; có bảng tính tay, R1, bình thường giữ ngoài, cỡ học/seed/hoán vị; đủ các đầu ra và LOG kết thúc/prompt/STATE. CSV đầu vào có 5 dòng, đúng 16 cột, không ô rỗng. CSV ca có 190 dòng, 30 ca; cả 30 thuộc dev được phép. Tiêu chí đối chiếu bài–code còn thiếu phần ở R1; các hệ quả B9 có sai sót R2–R4.
- **Tính lại chỉ đọc:** nạp mô hình đã lưu, tính lại toàn bộ 1436 × 333 dự báo test và 719 cửa sổ val bằng numpy, không học lại. Lệch dự báo tối đa 6,0228e-6 và 4,8849e-7; lệch điểm tối đa 3,3465e-4; 0 ô vượt dung sai; 0 argmax khác; 0 quyết định báo động khác. Ngưỡng tay 63,83293362535, code 63,83291628443. Khớp file tính tay và Tiêu chí xong 2.
- **Các lượt:** tính lại số tick, đợt và đoạn báo động của 8 cấu hình hoàn tất, cả cách code và biến thể b; khớp `b6b7-phan-tich.json`. Jaccard khớp. Hàm Spearman không xử lý ties bằng hạng trung bình; chênh khoảng 0,003 trở xuống, không đổi kết luận về seed nên không thành finding riêng.
- **Tái lập và nguồn:** nội dung tensor R1 trùng T-005; GDN source đúng revision và sạch. Hash/kích thước hai PDF và hai bản text khớp manifest. 30 file mốc tiêm khớp oid nguồn đã lưu. Mọi JSON hợp lệ; lượt R1 hỏng có log exit 124, các lượt hoàn tất có exit 0. Không học lại hoặc chạy benchmark mới.
- **Đường nhãn GDN:** nhãn test không vào feature/loss/chọn epoch. Mốc dev dùng cắt normal học và đoạn kiểm bình thường đã được khai. `attack` giả toàn 0 không được dùng tối ưu F1. R1 có dùng schema của ca được chấm, L* dùng schema toàn 30 dev; SPEC đã giới hạn ý nghĩa hai phép kiểm, không gọi đây là kết quả test độc lập.
- **Đồ thị:** embedding → top-k → attention → dự báo → lỗi chuẩn hóa → max/ngưỡng khớp code. GDN dùng đồ thị metric học được, không phải đồ thị phụ thuộc service. DecompRCA pipeline thường không gửi nhãn gốc/tên ca vào LLM; t_det của RE1 là mốc tiêm, đúng chế độ a. DK có mô tả quan hệ hệ thống; lợi ích của DK không chứng minh không dùng thông tin cấu trúc. Đối chứng không đồ thị trong MRP/WHY-07 đã nêu đúng: nếu còn self-time hoặc hồi quy theo cha, chỉ được kết luận về bước đã bỏ. T-018 chưa thực hiện phép so đồ thị/không đồ thị mới.
- **Phân loại nguồn và quyết định:** DT18 yêu cầu các đầu ra và đồ thị phụ thuộc; ví dụ thuật toán/dataset của cô không phải danh sách phải cài. Q-38 đã duyệt danh sách gọn: thống kê, nhân quả, trace/lan truyền, đa nguồn và detector học đồ thị có đại diện. Không yêu cầu T-018 bổ sung phương pháp học RCA có giám sát đã không được chọn. E1–E6 và H1–H6 vẫn được ghi là đề xuất/giả thuyết, chưa phải quyết định của Minh.
- **Dataset/RQ:** chưa chốt dataset thí nghiệm, chia dev/test hoặc cửa sổ P3; không coi đây là thiếu việc của T-018. RE2-TT đơn lẻ không tách được vị trí khỏi danh tính 5 service gốc hoặc khái quát sang topology khác; WHY-03 đã giới hạn đúng. Bộ Bank chỉ được bảo toàn, chất lượng/tiêu chí 7 vẫn OPEN tới G3. Chưa đủ căn cứ xác nhận toàn bộ tập cuối phân xử được RQ1/RQ3. Phép chia học/normal giữ ngoài của T-018 chỉ là chẩn đoán trên dev, không phải cách chia test G1.
- **Phạm vi ghi:** các đích ghi của script được kiểm nằm trong `results/T-018/` hoặc `D:/RCA-ext/work/T-018/`; LOG khai chỉ sửa dòng T-018 của STATE. Không thấy bằng chứng ghi ngoài phạm vi từ các file được giao. Vì không có diff task, không chứng nhận được lịch sử mọi thay đổi ngoài danh sách. R5 là vượt phạm vi đọc, không phải ghi.
- **Giới hạn phản biện:** không đọc `data/locked/`, không mở telemetry Bank, không tái chạy script B9 hoặc phương pháp trên dataset mới. Không xác nhận số LLM hay benchmark SWaT/WADI chưa tái lập. K6/K13 của DecompRCA đã có giả thuyết đối lập và trạng thái chưa kiểm; không nâng chúng thành lỗi đã xảy ra.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng | `process_swat.py` gộp nhãn bằng max (dòng 30–32 tính từ đầu hàm `downsample`), bài ghi "nhãn phổ biến nhất" (`gdn.txt:342–343`); khối 1/10 nhãn 1 thành 1 theo code, 0 theo bài. `test.fillna(test.mean())` (dòng 50) dùng trung bình cả tập test. Câu "Bài ghi cùng các bước" ở `ho-so-gdn.md:27` sai. Phạm vi hẹp: không ảnh hưởng số nào của T-018 (T-018 dùng ffill/0, không dùng script này) | Duyệt sửa (04/10) |
| R2 | Đúng | `decomprca.txt:1274–1278`: pool ngẫu nhiên chứa nguyên nhân, CIRCA-FCI 0,400 > BARO 0,286 trên SWaT, bài tự gọi là "the one setup where a graph method beats". Câu ở `decomprca.md:44` rộng hơn bài. Đồng ý ghi rõ pool đó và Bảng 4 dùng nhãn để bảo đảm gốc trong pool | Duyệt sửa (04/10) |
| R3 | Đúng | Mâu thuẫn với chính định nghĩa ở `decomprca.md` mục 1; RE1-TT (lỗi trực tiếp) vẫn tách được: lỗi truy hồi 0,09, lỗi xếp lại 0,26 (PDF 472). Đồng ý câu thay của reviewer | Duyệt sửa (04/10) |
| R4 | Đúng | `main.py:325` đếm sau `preprocess` trên cửa sổ ghép; BARO tiền xử lý hai cửa sổ riêng rồi lấy giao, nên cột hằng ở pre mà đổi ở post bị đếm nhưng không được xếp. Chú thích trong code nói "the set the method actually ranked" là chưa đúng với BARO. Tôi đã chép chú thích đó mà không kiểm đường xử lý — đúng lỗi QT2/SL24. Mức chênh thực tế trên RCAEval chưa đo | Duyệt sửa (04/10) |
| R5 | Đúng | SPEC dòng 29, 99 chỉ cho đọc tên cột và tên ca RE1; `retrieval_ngau_nhien.py` đọc toàn CSV, mốc tiêm và giá trị để bỏ cột hằng. Prompt Đợt 1 cho phép chạy phương pháp trên RE1-OB/SS nên không vượt giới hạn của prompt, nhưng vượt SPEC tôi tự viết và không ghi vào "Thay đổi trong lúc làm". Đề xuất: ghi độ lệch vào SPEC/LOG, Minh quyết có dùng số 0,816/0,901 không. Nếu không dùng: bản chỉ-tên-cột tính được bằng hợp/từng ca không bỏ cột hằng, nhưng sẽ khác định nghĩa của DecompRCA | Duyệt sửa (04/10) |
| R6 | Đúng một phần | Đúng là AGENTS luật cứng 3 chưa thỏa. Nhưng `<gioi_han>` của prompt cấm người làm ghi WHY và quy định cách xử lý là ghi "(chờ WHY…)" tại chỗ dùng — task đã làm vậy (`ho-so-gdn.md:17`, mục 8.2, 9.1). Điểm còn thiếu thật: E1 viết như "chọn" cấu hình P3, trong khi kết quả cho thấy cấu hình đó chưa đạt (trùng tự soát S2). Đề xuất: WHY chỉ ghi lý do của phép chẩn đoán T-018; E1 đổi thành ứng viên, không chốt P3 | Duyệt sửa (04/10) |
| N1 (tự tìm, KHÔNG CHẶN) | — | `ho-so-gdn.md` mục 9.5 gọi Eadro "ứng viên tốt nhất cho GDN" chỉ dựa vào thẻ T-009; độ dài, bộ cột, độ sạch phiên bình thường chưa kiểm. Đề xuất hạ thành "ứng viên cần kiểm" | Duyệt sửa (04/10) |
| N2 (tự tìm, KHÔNG CHẶN) | — | Mục 0 và 9.4 nêu "10 ca khoảng 5 %" trên 1 lượt, 1 seed; cần thêm "1 lượt, 1 seed" để không đọc như mức ổn định | Duyệt sửa (04/10) |
