# T-022 — Nháp mục WHY (chưa ghi vào `docs/WHY.md`)

Ngày 05/10/2026. Người soạn: Claude. Chưa ghi nguồn chung: ghi vào `docs/WHY.md` cần Minh duyệt riêng nội dung và phạm vi (SPEC "Phạm vi ghi"). Nháp chưa được ghi không đủ điều kiện dùng lựa chọn trong số khoa học P3.

Mã mục để trống (`WHY-<mã>`), vì T-023 có thể đề xuất mục WHY cùng lúc; người ghi cấp mã khi Minh duyệt. Mỗi mục theo mẫu của `docs/WHY.md`: chọn → vì sao → phương án đã xét → bằng chứng → kết luận phụ thuộc.

Phần A là các quyết định Minh đã có (Q-64–Q-67, Q-72): chỉ ghi lý do, không mở lại. Phần B là ghi chú cho WHY-19. Phần C là các lựa chọn còn mở trong `lua-chon-can-duyet.md`; văn bản C viết theo đề xuất của tôi và phải sửa theo đúng điều Minh quyết trước khi ghi.

---

## A. Quyết định đã có

### A1. `WHY-<mã>`. Cửa sổ dữ liệu P3 — Đã quyết (Q-64)

- **Chọn:** đoạn sự cố 300 s sau mốc; đoạn bình thường tối đa 300 s trước mốc và không chồng lần tiêm trước. Nezha: chỉ áp cho metric; trace/log Nezha chỉ dùng cho xếp hạng biết trước cửa sổ. Eadro: dữ liệu bình thường lấy từ phiên no-fault (chưa kiểm; kiểm ở T-023). Áp như nhau cho mọi phương pháp trên cùng dataset (MRP P3 "cùng cửa sổ dữ liệu").
- **Vì sao:** độ dài cửa sổ quyết bộ nào có đủ dữ liệu bình thường cho từng ca, nên phải chốt cùng gói dataset ở G1 (gói A phụ thuộc vào nó). RE2-TT có 720 s trước mốc; Nezha khoảng 482–521 s giữa hai lần tiêm và không biết lỗi kết thúc lúc nào; Eadro không có đoạn bình thường trước tiêm trong phiên. 300 s trước mốc có sẵn ở RE2-TT; ở Nezha nằm trong khoảng giữa hai lần tiêm, nhưng có chồng phần đuôi của lỗi trước hay không còn tùy thời lượng lỗi chưa biết. Trên lưới 1 s, 300 + 300 s trùng `--length 10` của RCAEval, cấu hình T-006 đã tái lập được Bảng 3 bài BARO cho RobustScorer và N-Sigma (lệch ≤ 0,004 mỗi ô).
- **Phương án đã xét:** dời quyết định xuống đầu P3 (phải sửa MRP §4 và Q-54, trong khi gói dataset đã phụ thuộc); ±600 s (`--length 20`, cấu hình so mốc bài TORAI của MicroRank/TraceRCA, WHY-16) — không có đủ dữ liệu bình thường ở Nezha; toàn bản ghi ±720 s — chỉ có ở RE2, không áp được cho bộ khác.
- **Giới hạn:** T-013 cho thấy trên 25 ca fse-ob DELAY, đổi 300 → 360 dòng nền làm Avg@5 BARO giảm 0,224 (`results/T-013/cua-so-va-che-do-b.md` §1); kết quả nhạy với độ dài nền. Không chọn cửa sổ theo phân tích đó. MicroRank khớp mốc ở ±600 s, lệch 2/21 ô ở ±300 s (T-007), nên số MicroRank, TraceRCA P3 không so trực tiếp với Bảng 2 bài TORAI. Mốc tiêm là đầu vào hợp lệ chỉ ở chế độ (a) (A3).
- **Bằng chứng:** `results/T-021/goi-g1.md` §6 câu 2; `results/T-006/kiem-dung-dan.md:45`; `results/T-007/kiem-dung-dan.md` tóm tắt; `results/T-022/runs/allowlist-001/kiem-allowlist.json` (30/30 ca RE2-TT dev có mốc ở giây 720).
- **Kết luận phụ thuộc:** mọi số P3 chế độ (a) và cửa sổ RCA sau báo động ở chế độ (b); WHY-19 (ghi chú phần B).

### A2. `WHY-<mã>`. Báo Retrieval@K và Rerank@1 — Đã quyết (Q-65)

- **Chọn:** với mọi phương pháp RCA, báo thêm Retrieval@K (service gốc nằm trong K thực thể đầu) và Rerank@1 = AC@1 / Retrieval@K, K ∈ {5, 10}, bằng `Evaluator.retrieval_service` và `rerank_service` của RCAEval `259ea41` (`RCAEval/benchmark/evaluation.py:162–210`).
- **Vì sao:** Hit@k gộp hai kiểu hỏng: không tìm ra nguyên nhân, và tìm ra nhưng xếp sai. Tách hai phần cho P4 biết tìm cơ chế ở bước nào (bài DecompRCA). Tính từ thứ hạng đã có, không tốn chạy thêm.
- **Phương án đã xét:** định nghĩa theo K metric của Bảng 1 DecompRCA — với hệ ít service, bộ chọn ngẫu nhiên 15 metric đã trúng 0,82–0,90 (RE1-OB, RE1-SS), nên mức trần chủ yếu do cấu trúc; không báo (mất phép tách).
- **Giới hạn:** Retrieval@K = AC@K và Rerank@1 = AC@1/AC@K theo định nghĩa; đây là cách trình bày khác của cùng thứ hạng, không phải bằng chứng độc lập. Hàm RCAEval không xử lý hòa và `main.py` bỏ ca lỗi khỏi mẫu (`main.py:552–553`); bộ chấm P3 nạp ca lỗi dưới dạng danh sách rỗng và phá hòa theo tên (C9).
- **Bằng chứng:** `results/T-018/decomprca.md` mục 3–4; `results/T-018/runs/b9-retrieval-ngau-nhien.json`; `results/T-021/goi-g1.md` §6 câu 3.
- **Kết luận phụ thuộc:** phân loại hạn chế ở P4 (lỗi truy hồi hay lỗi xếp lại).

### A3. `WHY-<mã>`. Mốc tiêm ở chế độ (a) và ngân sách nhãn — Đã quyết (Q-66)

- **Chọn:** ở chế độ (a), mốc tiêm là thông tin vận hành biết trước, được đưa cho phương pháp qua adapter chế độ (a). Chỉ service gốc và loại lỗi là nhãn chấm. Ngân sách nhãn root của mọi baseline bằng 0: không học, không chọn cấu hình, không chọn ca bằng nhãn root. Kết quả chế độ (a) luôn báo cạnh chế độ (b).
- **Vì sao:** trong RCAEval, bản code P1 đã kiểm, mọi baseline tầng 1 nhận mốc tiêm (`main.py:311–315`); bài BARO báo riêng các dòng `[t_inject]`; RCAEval chạy TORAI bằng mốc tiêm thay `t̂_A` (`results/T-016/ho-so-torai.md` C9). Bỏ chế độ (a) thì không so được với số công bố và không tái lập được. Riêng MicroRank bài gốc là pipeline online có bộ phát hiện trace riêng; bản P3 là bản RCAEval sửa đầu vào, nhận mốc tiêm. MRP §4 nói nhãn test chỉ để chấm; xếp mốc vào "thông tin vận hành" làm rõ đầu vào này hợp lệ ở đâu (chỉ chế độ a). Không baseline nào trong Q-38 học từ nhãn root.
- **Phương án đã xét:** bỏ chế độ (a) trên test, chỉ chạy chế độ (b) — mất phép so với bài gốc và tách lỗi phát hiện khỏi lỗi xếp hạng.
- **Giới hạn:** kết quả chế độ (a) dễ hơn thực tế vì biết đúng lúc lỗi bắt đầu. Mốc tiêm không phải lúc biểu hiện (onset); độ trễ ở chế độ (b) là "độ trễ từ lúc tiêm" (MRP P7). Mốc chỉ vào adapter chế độ (a); ở chế độ (b) mọi đường suy ra mốc (tên ca, đường dẫn, file nhãn, cắt quanh mốc) bị cấm (luật cứng 6).
- **Bằng chứng:** `results/T-021/goi-g1.md` §6 câu 4; MRP §4, P3; `results/T-013/ho-so-baro.md` §1, §8.
- **Kết luận phụ thuộc:** cách đọc mọi số chế độ (a); phân biệt nhãn chấm với đầu vào phương pháp trong mọi adapter P3.

### A4. `WHY-<mã>`. Tập cột BOCPD và chạy qua đêm — Đã quyết (Q-67, Q-72)

- **Chọn:** BOCPD dùng **tập cột** theo cấu hình tác giả `reproduce_bocpd`: tên chứa `latency-50` hoặc `_error`, bỏ `queue-master` và `rabbitmq_` (BARO `e35f4ec`, `baro/reproducibility.py:139–145`). Q-67 chỉ chọn tập cột, không chọn cách cắt 300 + 300 quanh mốc tiêm của hàm đó. Đo lại thời gian đầu P3. Q-72: BOCPD chế độ (b) trên RE2-TT dev được chạy qua đêm trên EC2 ở T-025, tối đa 20 giờ, đầu vào không chọn theo mốc tiêm, ghi tiến độ từng ca, giữ lượt hỏng; kết luận chi phí ghi cho bản cài BARO, không cho thuật toán BOCPD.
- **Vì sao:** đây là quy ước tác giả dùng khi báo kết quả phát hiện. Hàm `bocpd()` tự chọn mọi cột chứa `latency` (cả `latency-90`) và `_error`; ở T-005 nó chọn 76 cột (60 không hằng) và mất 1.440 s cho 600 điểm, toàn ca 1.441 điểm không xong trong 1 giờ. Chi phí xấp xỉ O(T²d³) (`results/T-013/ho-so-bocpd.md` §9), nên giảm số cột d là cách theo đúng tác giả để giảm chi phí. Q-40 giới hạn 3 giờ cho toàn ca một dataset; Q-72 là ngoại lệ riêng cho BOCPD.
- **Phương án đã xét:** báo "không chạy đủ trong ngân sách" (áp cho CIRCA-PC ở Q-67); chạy một mẫu ca; cắt quanh mốc như `reproduce_bocpd` (cấm ở chế độ b, luật cứng 6); giữ 76 cột của `bocpd()`.
- **Giới hạn:** trên RE2-TT dev, tập cột này có 25–48 cột thô/ca; số cột `_error` 3–20/ca và thay đổi theo ca (`results/T-022/cot-bocpd-dev.csv`); sự có mặt cột `_error` tương quan với service gốc (`results/T-018/dinh-chinh-task-cu.md` D1) — với bộ phát hiện chạy từng ca, điều này không thành đường học nhãn, nhưng là dữ liệu tương lai trong file (C4). Chi phí trên 1.441 điểm với tập cột này **chưa đo**; ngoại suy từ cấu hình cũ (≈ 69 giờ/30 ca) không áp cho cấu hình này.
- **Bằng chứng:** `results/T-005/do-kha-thi.md` bảng 2b; `results/T-013/trung-gian/chi-phi-va-sentinel.json`; `results/T-021/goi-g1.md` §6 câu 5; DECISIONS Q-67, Q-72.
- **Kết luận phụ thuộc:** mọi số phát hiện BOCPD P3; lịch và chi phí T-025.

---

## B. Ghi chú bổ sung cho WHY-19

- **File đích:** `docs/WHY.md`, WHY-19, dòng "Giới hạn".
- **Đoạn cũ (giữ nguyên):** "Cửa sổ P3 chưa chốt (Q-54)."
- **Thêm ngay sau câu đó:** "Ghi chú 05/10/2026: cửa sổ P3 đã chốt ở Q-64 (300 s sau mốc, tối đa 300 s trước mốc), xem `WHY-<mã cửa sổ>`. Trên lưới 1 s, cửa sổ này trùng `--length 10` của lệnh chính TORAI, cấu hình mà bằng chứng ở mục này đã dùng (Avg@5 TT dev 10). Câu trước là trạng thái lúc ghi WHY-19 (04/10/2026), giữ để thấy lịch sử."
- **Vì sao:** WHY-19 còn ghi trạng thái cũ; người đọc có thể hiểu là cửa sổ vẫn mở. Giữ câu cũ để không xóa lịch sử.
- **Kết luận phụ thuộc:** không đổi lựa chọn bản TORAI; chỉ cập nhật trạng thái.

---

## C. Lựa chọn còn mở — viết theo đề xuất, sửa theo quyết định của Minh trước khi ghi

Chi tiết phương án, bằng chứng và trường hợp sai ở `results/T-022/lua-chon-can-duyet.md` (mục ghi trong ngoặc). Dưới đây là văn bản sẽ ghi nếu Minh chọn đúng đề xuất.

### C1. Cắt cửa sổ chế độ (a) trên từng nguồn (mục 1)

- **Chọn:** theo timestamp, nửa mở: N = [t−300 s, t), A = [t, t+300 s); metric theo `time`, span theo `startTime`, log theo `timestamp`, chuỗi 15 s TORAI 20 dòng mỗi phía. Bên trong cửa sổ, mỗi phương pháp chia N/A theo code tác giả đã kiểm ở P1. Thiếu dữ liệu thì ghi độ dài thực, không kéo dài cửa sổ.
- **Vì sao:** Q-64 tính bằng giây; nửa mở cho đúng 300 + 300 dòng như RCAEval `--length 10` trên lưới 1 s; giữ cách chia nội bộ là giữ phần khoa học của tác giả (MRP §6.4).
- **Phương án đã xét:** cắt theo số dòng (sai nghĩa khi có lỗ dữ liệu hay nhịp khác 1 s); đoạn A đóng 301 dòng; adapter tự chia N/A thay phương pháp.
- **Kết luận phụ thuộc:** mọi số chế độ (a).

### C2. Nguồn đầu vào TORAI trên RE2-TT (mục 2)

- **Chọn:** dùng `logts.csv`, `tracets_err.csv`, `tracets_lat.csv` của tác giả (torai-TT, Figshare); metric của torai-TT trùng parquet RE2 ở 30/30 ca dev.
- **Vì sao:** đúng đầu vào tác giả dùng; `logts` không dựng lại được từ parquet RE2 (tốt nhất 50,2 % ô); hành vi bản sửa đã kiểm trên đúng dữ liệu này (T-016).
- **Phương án đã xét:** tự dựng từ parquet (đổi đầu vào phương pháp, chưa kiểm); dùng cả hai làm phép kiểm độ nhạy.
- **Giới hạn:** `tracets_lat` của tác giả dùng ngưỡng trên toàn file (dữ liệu sau mốc); ca `re2tt_ts-auth-service_cpu_1` có log ở torai-TT nhưng không có trong parquet RE2, nên TORAI và SimpleRCA nhận bằng chứng log khác nhau ở ca này; ở Nezha/Eadro phải tự dựng, nên so TORAI giữa dataset có khác nguồn đầu vào.
- **Kết luận phụ thuộc:** mọi số TORAI P3.

### C3. Tập ứng viên và ánh xạ thực thể (mục 3)

- **Chọn:** chấm ở mức thực thể; universe U = 68 thực thể `ts-*` của RE2-TT chốt từ metadata dev (gồm DB và `ts-ui-dashboard`); chấm danh sách của phương pháp nguyên trạng sau ánh xạ và bỏ trùng; không điền thực thể thiếu; báo coverage theo U và tập quan sát của phương pháp.
- **Vì sao:** DT18 coi nút là "dịch vụ hoặc thành phần hệ thống"; RCAEval và TORAI xếp cả DB; điền phần thiếu cho phương pháp điểm nhờ may.
- **Phương án đã xét:** chỉ `-service`; gộp DB vào service chủ (chưa có bảng sở hữu); điền ngẫu nhiên phần thiếu.
- **Kết luận phụ thuộc:** mọi độ đo xếp hạng; trần coverage phương pháp trace.

### C4. Bộ cột metric (mục 4)

- **Chọn:** mỗi ca dùng cột có trong file của ca, như code tác giả; không bỏ cột `_error`; không điền cột vắng. Ghi audit cột vắng ở phía evaluator, không đưa vào phương pháp.
- **Vì sao:** mọi phương pháp metric tầng 1 và hai bộ phát hiện chạy riêng từng ca, nên không học được quy luật cột vắng giữa các ca; bỏ cột error làm yếu baseline.
- **Phương án đã xét:** hợp cố định (gần tương đương sau bước bỏ cột hằng); giao cố định L\* (bỏ 23/25 cột error).
- **Giới hạn:** sự có mặt cột tương quan với root (T-018 D1); phương pháp đếm alert theo cột có thể bị ảnh hưởng — kiểm ở P4.
- **Kết luận phụ thuộc:** BARO, CIRCA, TORAI, SimpleRCA, BOCPD, N-Sigma.

### C5. CIRCA kiến trúc (mục 5)

- **Chọn:** RHT + DA (θ = 3), LinearRegression; báo kèm RHT-only; giữ metric cô lập làm ứng viên không cha; đồ thị gọi từ span trong N; schema và bỏ cột hằng trên N∪A như RCAEval; giữ cửa sổ nội bộ RHT của RCAEval (train [t−120, t−10], test 10 điểm cuối).
- **Vì sao:** CIRCA theo bài là RHT + DA; bản tuyến tính đã tính lại độc lập ở T-014; metric graph là DAG ở 30/30 ca; giữ metric cô lập tránh mất ứng viên im lặng; ở chế độ (a) RCA chạy sau t+300 nên dữ liệu N∪A đã có.
- **Phương án đã xét:** RHT-only làm chính (khớp RCAEval CIRCA-PC); SVR(sigmoid) + RHT + DA (chưa kiểm); coverage gốc; đồ thị từ trace N∪A.
- **Giới hạn:** call/meta graph có chu trình ở 24/30 ca; 300 s trace có thể thiếu cạnh so với 720 s; cửa sổ RHT 1 s khác ý nghĩa thời gian của bài (1 phút).
- **Kết luận phụ thuộc:** mọi số CIRCA P3 và nhận định về đồ thị kiến trúc ở P4.

### C6. MicroRank-RCAEval sửa đầu vào (mục 6)

- **Chọn:** cửa sổ Q-64; xếp đầy đủ mọi operation có điểm (báo kèm top-11); service theo `serviceName`, điểm service = max operation; giữ bản sao trùng, ID trùng khác nội dung → ERROR; operation không có span trong N thì không bị cờ (ghi số); không có trace bất thường → NO_EVIDENCE; service vắng trace không xếp.
- **Vì sao:** `top_max` là tham số định dạng, không thuộc công thức điểm; MRR, NDCG cần đủ thứ hạng.
- **Phương án đã xét:** top-11 như code; coi operation mới là bất thường.
- **Kết luận phụ thuộc:** số MicroRank P3.

### C7. TraceRCA bản lọc hữu hạn (mục 7)

- **Chọn:** lọc NaN/inf trước khi sắp; support 0 là không có bằng chứng, không xếp; hòa giữ nguyên điểm để evaluator xử lý; tổng span bất thường 0 → NO_EVIDENCE; điểm service = max operation.
- **Vì sao:** NaN không có thứ tự; sort rồi lọc làm thứ hạng phụ thuộc thứ tự dòng (T-007: hạng đáp án đổi ở 22/90 ca khi chỉ đổi thứ tự dòng).
- **Phương án đã xét:** support 0 xếp cuối với điểm 0; giữ bug (chỉ để tái dựng T-007).
- **Kết luận phụ thuộc:** số TraceRCA P3; tác động NaN và hòa báo gộp.

### C8. Trạng thái lỗi (mục 8)

- **Chọn:** trạng thái `OK`, `NO_EVIDENCE`, `ERROR`, `UNSUPPORTED`, `TIMEOUT` cho mỗi lượt; mọi trạng thái khác `OK` ở mẫu số và tính trượt; báo số ca theo trạng thái.
- **Vì sao:** MRP P3 cấm chấm thứ tự cột như dự đoán thật và cấm bỏ ca lỗi khỏi mẫu; `main.py` RCAEval bỏ ca lỗi.
- **Kết luận phụ thuộc:** mọi bảng P3.

### C9. Cách chấm xếp hạng (mục 9)

- **Chọn:** hòa theo nhóm điểm bằng nhau, tính kỳ vọng Hit/RR/DCG khi thứ tự trong nhóm ngẫu nhiên, kèm cận lạc quan/bi quan; hàm RCAEval nạp danh sách phá hòa theo tên và danh sách rỗng cho ca không `OK`; root vắng → 0; bootstrap theo 10 ô dev, B = 10.000, seed 20261005, khoảng phân vị 95 %; nhiều seed thì trung bình theo ca trước khi bootstrap; báo theo lỗi, ô, nhóm vị trí và từng ca.
- **Vì sao:** không biến thứ tự cột hay tên thành bằng chứng (MRP P3); ba lần lặp của một ô gần như giống nhau nên phải lấy mẫu theo ô (WHY-04, MRP P7).
- **Phương án đã xét:** phá hòa theo thứ tự cột; bootstrap theo ca.
- **Giới hạn:** 10 ô cho khoảng tin cậy rộng; các độ đo trùng nghĩa (Hit@k = AC@k, Retrieval@K = AC@K, NDCG@5 là hàm của hạng) không phải bằng chứng độc lập.
- **Kết luận phụ thuộc:** mọi bảng xếp hạng P3, P7.

### C10. Chế độ (b): phạm vi và chuỗi đầu vào (mục 10)

- **Chọn:** phát hiện hồi cứu trên bản ghi đã chọn vì có sự cố; bộ phát hiện nhận cả bản ghi 1.441 điểm một lần, không khởi động lại; giữ tiền xử lý tác giả và khai báo look-ahead của BOCPD (min–max, bỏ cột hằng trên toàn chuỗi); bỏ sentinel ở chỉ số T và ghi số lần bỏ; warm-up theo mặc định code.
- **Vì sao:** mốc RE2-TT luôn ở giây 720, nên mọi lịch chia đoạn theo vị trí trong file đều gắn với mốc; cả bản ghi là cách ít lựa chọn nhất. Tiền xử lý nhân quả là biến thể mới không có câu hỏi P3 nào đòi. Sentinel là lỗi biên của code, giữ nó làm mọi ca có một báo động sau mốc.
- **Phương án đã xét:** đoạn 600 điểm bước 300 (rẻ hơn khoảng một phần ba, vẫn gắn với mốc, thêm biên khởi động lại); tiền xử lý nhân quả; nối các ca.
- **Giới hạn:** không đo được cảnh báo online hay báo động sai trong vận hành liên tục; dữ liệu bình thường chỉ 720 s/ca.
- **Kết luận phụ thuộc:** mọi số phát hiện P3; RCA chế độ (b).

### C11. Chế độ (b): cột N-Sigma, episode, chấm phát hiện, ghép ranker (mục 11)

- **Chọn:** N-Sigma dùng cùng tập cột với BOCPD (Minh quyết, tôi không chắc); episode: báo động đầu mở episode, báo động trong 300 s sau thuộc episode đó; nhãn phát hiện: bất thường = [t_tiêm, cuối file], bình thường = trước đó (bài BARO); độ đo theo episode, theo ca, theo cửa sổ 60 s từ đầu file (không point-adjust), FP/giờ bình thường, độ trễ từ lúc tiêm; chế độ (b) chạy BARO, CIRCA kiến trúc, TORAI với cả hai bộ phát hiện; chỉ episode đầu kích hoạt RCA, cửa sổ RCA theo Q-64 quanh thời điểm báo động.
- **Vì sao:** cùng đầu vào thì so được hai bộ phát hiện; thời gian trơ 300 s khớp cửa sổ sau mốc và "flush 5 phút" của MicroRank; bài BARO ghép từng phương pháp RCA với từng bộ phát hiện (`RCA_method[Anomaly_Detector]`, arXiv 2405.09330v1 Bảng 3) và dùng điểm đổi đầu tiên cho RCA; bài TORAI giả định mốc từ bộ phát hiện ngoài.
- **Phương án đã xét:** N-Sigma mọi cột; gộp báo động cách ≤ 5 điểm (`find_anomalies`); mỗi episode một RCA; ghép mọi ranker với mọi bộ phát hiện.
- **Giới hạn:** thời lượng lỗi RE2 không được công bố; giả định lỗi kéo dài tới cuối file chưa kiểm.
- **Kết luận phụ thuộc:** bảng phát hiện P3; RCA chế độ (b); chi phí T-025.

### C12. Seed và tham số (mục 12)

- **Chọn:** TORAI seed {0, 1, 2} đặt theo ca; phương pháp tất định chạy một lần và kiểm lặp lại/hoán vị trên một phần ca; MicroRank `PYTHONHASHSEED=0`, kiểm thêm 1; mọi tham số giữ mặc định tác giả; không chỉnh bằng nhãn dev.
- **Vì sao:** WHY-20; ngân sách nhãn root bằng 0 (Q-66).
- **Kết luận phụ thuộc:** tính tái lập của mọi số P3.
