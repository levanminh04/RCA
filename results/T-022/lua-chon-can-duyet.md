# T-022 — Các lựa chọn giao thức P3 cần Minh quyết

Ngày 05/10/2026. Người soạn: Claude (người làm T-022). Trạng thái cả file: **CANDIDATE, chờ Minh quyết**. Chưa lựa chọn nào được dùng trong số khoa học. Lựa chọn chỉ có hiệu lực khi Minh quyết và mục WHY tương ứng được ghi vào `docs/WHY.md` (luật cứng 3; SPEC bước 4).

Cách đọc mỗi mục: đã quyết gì (nếu có) → câu hỏi → phương án → đề xuất → vì sao → bằng chứng → khi nào đề xuất sai → kết luận phụ thuộc. Không phương án nào được chọn theo chênh accuracy; chưa chạy phương pháp nào trên 30 ca dev trong task này.

Ký hiệu: `t` là mốc chia (mốc tiêm ở chế độ (a), thời điểm báo động ở chế độ (b)). "N" là đoạn bình thường, "A" là đoạn sự cố. Thực thể (entity) là tiền tố trước dấu `_` đầu tiên của tên cột metric, ví dụ `ts-auth-service`, `ts-auth-mongo`.

Tóm tắt cho Minh: mục 0 là tổ chức task. Mục 1–12 là giao thức. Mục 13 là cách chọn ca pilot. Câu hỏi gom ở cuối file (mục 14).

---

## 0. Tổ chức task: tách hay cho T-022 kéo dài hai phiên

- **Vì sao phải hỏi:** bước 3–4 của SPEC chỉ được làm sau khi Minh quyết các mục dưới và WHY đã ghi. Vậy T-022 không thể xong trong một phiên (AGENTS §5, §5a.4). REVIEW nháp R3 đã nêu; SPEC ghi "Chưa quyết tách task".
- **Phương án A — giữ T-022, hai phiên.** Phiên 1 (phiên này): bước 0–2. Phiên 2, sau khi Minh quyết và ghi WHY: bước 3–5. Một lượt phản biện Codex ở cuối. Không cần SPEC mới.
- **Phương án B — tách.** T-022 dừng ở bước 2: giao thức, allowlist, bảng bằng chứng, nháp WHY. Codex phản biện giao thức trước khi cài. Task mới (mã T-030, vì T-024–T-029 đã dành trong PLAN) làm bước 3–5 với SPEC chép phần bước 3–5 của SPEC T-022.
- **Đề xuất: B.** Giao thức là thứ mọi task T-024–T-027 sẽ dùng. Phản biện độc lập trước khi đóng nó vào code và pilot thì sửa rẻ hơn. Code không phụ thuộc lựa chọn còn tranh cãi (selector, hàm độ đo với fixture) có thể bắt đầu ngay trong T-030 khi SPEC T-030 được duyệt, song song với phản biện.
- **Khi nào B sai:** nếu Minh muốn quyết thẳng mà không chờ phản biện, B chỉ thêm một vòng chờ; khi đó A rẻ hơn.
- **Phụ thuộc:** lịch PLAN §4 ("Đêm chuẩn bị"), dòng phụ thuộc "T-022 hoàn tất" của T-024/T-025.

---

## 1. Chế độ (a): cắt cửa sổ Q-64 trên từng nguồn

- **Đã quyết (Q-64):** sau mốc 300 s; trước mốc tối đa 300 s, không chồng lần tiêm trước. Không mở lại độ dài.
- **Câu hỏi:** biên đóng hay mở; áp cho metric, trace, log, chuỗi 15 s của TORAI thế nào; ai chia N/A bên trong.
- **Đề xuất:**
  1. Theo timestamp, nửa mở: N = [t−300 s, t), A = [t, t+300 s). Trên lưới metric 1 s của RE2-TT, đây đúng là 300 + 300 dòng, trùng `main.py` RCAEval với `--length 10` (`main.py:314–315`: `time < t` lấy 300 dòng cuối, `time ≥ t` lấy 300 dòng đầu).
  2. Metric theo cột `time`; span theo `startTime` (µs → s) nằm trong [t−300, t+300); log theo `timestamp`. Chuỗi 15 s của TORAI: 20 dòng mỗi phía theo `time < t`, như `main.py:381–394`. Lưới 15 s của dữ liệu tác giả không thẳng hàng với mốc (ca auth_cpu_1: bin chứa mốc bắt đầu 10 s trước mốc và bị tính vào N); giữ như code, ghi lại.
  3. Bên trong cửa sổ, mỗi phương pháp chia N/A theo đúng code đã kiểm ở P1 (ví dụ RCAEval tracerca/microrank chia span theo thời điểm kết thúc; CIRCA RHT dùng train [t−120, t−10] và 10 điểm cuối làm test, `rht.py:361–365`, `data.py:175–176`). Adapter chỉ quyết dữ liệu nào được đưa vào.
  4. Thiếu dữ liệu: ghi số dòng và số giây thực của N, A. Không kéo dài cửa sổ để bù.
  5. "Không chồng lần tiêm trước": mỗi ca RE2-TT là một bản ghi riêng, mốc ở giây 720 (30/30 ca, `runs/allowlist-001/kiem-allowlist.json`). Kiểm được trong file, không kiểm được với lịch tiêm của 60 ca test vì mốc của chúng nằm trong `data/locked/`.
- **Phương án khác:** (i) cắt theo số dòng như `main.py` — trùng kết quả trên RE2-TT nhưng sai nghĩa khi dữ liệu có lỗ hoặc nhịp khác 1 s (Nezha, Eadro); (ii) A đóng [t, t+300] (301 dòng) — lệch 1 dòng so RCAEval L10; (iii) adapter chia N/A thay phương pháp — đổi phần khoa học của tác giả (MRP §6.4).
- **Vì sao:** Q-64 nói bằng giây, không bằng dòng; nửa mở cho đúng 300 + 300 dòng như cấu hình RCAEval đã tái lập ở T-006 (L10). Giữ cách chia nội bộ của tác giả là mặc định prior work.
- **Sai khi:** một phương pháp cần dữ liệu ngoài cửa sổ (ví dụ CIRCA bản gốc 1 phút lấy 120 phút lịch sử) — khi đó cửa sổ Q-64 không đủ ý nghĩa thời gian của bài; phải ghi là cấu hình RCAEval, không phải bài.
- **Phụ thuộc:** mọi số chế độ (a) ở T-024, T-026, T-027.

---

## 2. Nguồn đầu vào của TORAI

- **Đã quyết:** WHY-19 chọn bản sửa hai chỗ; ít nhất 3 seed (WHY-20). Chưa quyết nguồn `logts`, `tracets`.
- **Sự thật:** T-016 chạy TORAI trên `torai-TT` (CSV tác giả, Figshare). Metric trùng RE2 ở 30/30 ca dev (`results/T-016/runs/s10-cung-ca.json`). `logts` không dựng lại được từ parquet RE2 (tốt nhất 50,2 % ô, `results/T-016/dung-logts-tracets.md` §4). `tracets_lat` của tác giả dùng ngưỡng μ+3σ trên toàn file, gồm sau mốc (§3). Ca `re2tt_ts-auth-service_cpu_1`: parquet RE2 không có log, nhưng `logts.csv` tác giả có 223.924 lượt log (LOG phiên 1, 20:25).
- **Phương án A — dữ liệu tác giả (torai-TT).** Đúng đầu vào bài/code dùng; đã kiểm ở T-016.
- **Phương án B — tự dựng từ parquet RE2** theo đặc tả T-016 §5 (Drain chế độ B ngưỡng 0,4; tracets theo §3, ngưỡng học trên N). Cùng nguồn với các phương pháp khác và với Nezha/Eadro sau này; nhưng là đầu vào khác tác giả, logts chỉ khớp ≤ 50,2 %.
- **Phương án C — A làm chính, B làm phép kiểm độ nhạy** trên một phần ca.
- **Đề xuất: A.** Prior work là mặc định (MRP §6.4); B đổi đầu vào của phương pháp, cần WHY riêng và chưa kiểm. Ghi giới hạn: (1) TORAI và các phương pháp đọc parquet nhận bằng chứng log khác nhau ở ít nhất 1 ca; (2) ngưỡng `tracets_lat` của tác giả dùng dữ liệu sau mốc — ở chế độ (a) không phải rò nhãn nhưng là dữ liệu ngoài N; (3) trên Nezha/Eadro (T-026/T-027) buộc phải dựng như B, nên so TORAI giữa dataset phải ghi khác nguồn đầu vào.
- **Sai khi:** Minh ưu tiên "cùng nguồn dữ liệu cho mọi phương pháp" hơn "đúng đầu vào tác giả". Khi đó chọn B, chấp nhận TORAI trên RE2 là "TORAI với logts nhóm tự dựng".
- **Phụ thuộc:** mọi số TORAI P3; so TORAI với SimpleRCA (cùng dùng log); TORAI ở chế độ (b) nếu có.

---

## 3. Tập ứng viên, ánh xạ về thực thể, coverage

- **Câu hỏi:** chấm ở mức nào; universe gồm gì; phương pháp không có bằng chứng cho một thực thể thì sao.
- **Sự thật:** metric RE2-TT dev có 68 thực thể `ts-*` (gồm 26 DB mongo/mysql và `ts-ui-dashboard`), cộng `istio-init` ở 1 ca. Trace chỉ phủ 27 thực thể trong cửa sổ ±600 s ở 3 ca T-015 (`results/T-015/bang-ung-vien-tt.csv`); 27 ca còn lại chưa đếm. Cả 5 service gốc đều là `ts-*-service`.
- **Đề xuất:**
  1. Chấm ở mức thực thể (service hoặc thành phần như DB). Ánh xạ: metric → tiền tố trước `_` đầu tiên (như `main.py:560`); trace → `serviceName` của span (không cắt chuỗi `service_operation`, T-015 §1); TORAI → `<service>_A`. Bỏ trùng giữ lần xuất hiện đầu (điểm cao nhất).
  2. Universe đánh giá cố định U = 68 thực thể `ts-*`, chốt từ metadata 30 ca dev, không từ nhãn. Dùng cho coverage và mức ngẫu nhiên. Danh sách xếp hạng của phương pháp được chấm nguyên trạng; thực thể ngoài U (ví dụ `istio-init`) giữ chỗ trong danh sách và được ghi riêng.
  3. Báo thêm tập quan sát được của chính phương pháp (n_obs), như RCAEval tính `n_candidates` sau tiền xử lý (`main.py:322–329`).
  4. Phương pháp không có bằng chứng cho một thực thể thì không xếp thực thể đó. Không điền ngẫu nhiên phần còn thiếu.
  5. **SLI:** không phương pháp tầng 1 nào cần SLI. `main.py` RCAEval suy SLI từ tên service gốc (`main.py:340–365`), tức từ nhãn; P3 không dùng đường này. Adapter truyền `sli=None`; riêng `src/circa_kien_truc/scoring.py:39` đặt SLI là nút đầu theo thứ tự tên (RHT không dùng SLI để chấm). TORAI có tham số `service`, `fault_type`, `case` trong chữ ký; adapter không truyền (luôn `None`).
  6. File U: `results/T-022/mappings/universe-re2tt-dev.json` (68 = 41 `-service` + 26 DB + `ts-ui-dashboard`; có ở cả 30 ca; `istio-init` ngoài U, 1 ca), lập bằng `scripts/lap_universe.py`, lượt `runs/universe-001/`.
- **Phương án khác:** (i) chỉ các `-service` (bỏ DB, dashboard) — lệch RCAEval và TORAI (68 ứng viên, `results/T-016/quy-mo-tt.md` §2), làm mức ngẫu nhiên khác; (ii) gộp DB vào service chủ — cần ánh xạ sở hữu chưa có nguồn; (iii) điền phần thiếu bằng thứ tự ngẫu nhiên — cho phương pháp điểm nhờ may.
- **Sai khi:** cô hoặc Minh coi DB là một phần của service. Khi đó cần bảng sở hữu DB→service lấy từ kiến trúc, không từ nhãn.
- **Phụ thuộc:** mọi độ đo xếp hạng; trần coverage của MicroRank, TraceRCA (chỉ thấy ≤ 27 thực thể).

---

## 4. Bộ cột metric

- **Sự thật:** bộ cột khác giữa các ca và tương quan với service gốc (`results/T-018/dinh-chinh-task-cu.md` D1). Rủi ro trực tiếp là với phương pháp học xuyên ca. Mọi phương pháp metric tầng 1 (BARO, CIRCA, TORAI, SimpleRCA) và hai bộ phát hiện chạy riêng từng ca.
- **Đề xuất:** dùng bộ cột có trong file của ca, như code tác giả và `main.py`. Không bỏ cột `_error`. Không điền giá trị cho cột vắng. Ghi số cột và danh sách cột vắng so với hợp 30 ca vào audit phía evaluator, để P4 kiểm tương quan với nhãn; không đưa dấu vắng vào phương pháp.
- **Phương án khác:** (i) hợp cố định, cột vắng = NaN/0 — với phương pháp có bước bỏ cột hằng thì gần như tương đương đề xuất (cột toàn 0 bị bỏ), thêm việc mà không đổi đầu vào thực; (ii) giao cố định L\* (317 cột, T-018) — bỏ 23/25 cột error, lệch tác giả, mất tín hiệu lỗi.
- **Vì sao:** phương pháp chạy từng ca không học được quy luật "cột nào vắng thì root ở đâu" giữa các ca. Bỏ cột error sẽ làm yếu baseline (QT7).
- **Sai khi:** một phương pháp dùng số cột hoặc sự có mặt cột làm đặc trưng (ví dụ đếm số alert theo cột như SimpleRCA "events" — WHY-17 đã ghi điểm tăng theo số cột). Kiểm ở P4 bằng audit cột vắng.
- **Phụ thuộc:** BARO, CIRCA, TORAI, SimpleRCA, BOCPD, N-Sigma phát hiện.

---

## 5. CIRCA kiến trúc

- **Đã quyết:** tầng 1 dùng CIRCA đồ thị kiến trúc (Q-62). Chưa quyết scorer, mô hình, coverage, nguồn đồ thị.
- **Đề xuất:**
  1. **Scorer:** RHT + DA (ngưỡng 3), hồi quy tuyến tính (LinearRegression, mặc định `ci/anm.py:19`). Báo kèm RHT-only (rẻ, cùng lượt) để so với cách RCAEval chấm.
  2. **Ứng viên:** giữ metric cô lập như ứng viên không cha (adapter T-014), báo coverage gốc của code (ví dụ ca minh họa 124/272) riêng.
  3. **Nguồn đồ thị gọi:** span trong N = [t−300, t), cả hai đầu cạnh. T-014 dùng toàn bộ trace trước mốc (720 s); Q-64 giới hạn 300 s.
  4. **Schema và bỏ cột hằng:** trên dữ liệu cửa sổ N∪A như RCAEval. Ở chế độ (a), RCA chạy sau t+300 nên mọi dữ liệu này đã có sẵn.
  5. **Cửa sổ nội bộ RHT:** giữ train [t−120, t−10], test 10 điểm cuối (RCAEval 1 s).
- **Phương án khác:** (i) RHT-only tuyến tính làm chính (T-014 tham chiếu; khớp RCAEval CIRCA-PC) — nhưng CIRCA theo bài là RHT+DA; (ii) SVR(sigmoid) + RHT + DA như thực nghiệm bài — chưa kiểm ở T-014; (iii) coverage gốc — mất metric im lặng; (iv) đồ thị từ trace N∪A — có thể chứa cạnh do sự cố gây ra.
- **Vì sao:** DA là thành phần của phương pháp trong bài; RHT+DA tuyến tính đã được tính lại độc lập ở T-014 (`paper/compare-example-architecture/comparison.json`); metric graph là DAG ở 30/30 ca nên DA tất định trên đồ thị đó (T-014 hồ sơ §7).
- **Sai khi:** call/meta graph có chu trình ở 24/30 ca (T-014) làm cạnh metric phụ thuộc thứ tự SCC; nếu kiểm ở bước 3 thấy DA đổi theo hash seed thì phải báo, không chọn seed. 300 s trace có thể thiếu cạnh ít lưu lượng so với 720 s: ghi số cạnh.
- **Phụ thuộc:** mọi số CIRCA P3 và mọi nhận định "đồ thị kiến trúc giúp/không giúp" ở P4.

---

## 6. MicroRank-RCAEval sửa đầu vào

- **Đã quyết:** dùng bản sửa (Q-62). Không dùng số T-007 làm đích (SPEC).
- **Đề xuất:**
  1. Cửa sổ Q-64 (±300 s), khác ±600 s T-015 đã kiểm; ghi rõ.
  2. **Xếp đầy đủ** mọi operation có điểm, không cắt top-11. Báo thêm danh sách cắt top-11 (`top_max=5`) để đối chiếu code.
  3. Operation → service theo `serviceName` của span; điểm service = điểm operation cao nhất.
  4. Bản sao span: giữ bản sao trùng hoàn toàn; ID trùng khác nội dung → ERROR (chính sách T-015 §9.2).
  5. Operation không có span trong N: không có ngưỡng nên không bị cờ (như RCAEval, so sánh với NaN là sai); đếm và ghi.
  6. Không có trace bất thường → NO_EVIDENCE; không có trace bình thường → ERROR.
  7. Service vắng trace: không xếp; tính vào coverage.
- **Phương án khác:** (i) giữ top-11 như code — MRR, NDCG cần vị trí ngoài 11 operation; 11 operation có thể ít hơn 5 service; (ii) operation mới coi là bất thường — đổi detector, chưa có nguồn.
- **Vì sao:** `top_max` là tham số định dạng đầu ra, không thuộc công thức điểm (T-015 §2.5). Đầy đủ cho phép tính mọi độ đo trên cùng danh sách.
- **Sai khi:** Minh muốn so trực tiếp với cách RCAEval báo (top-11). Khi đó báo cả hai, chọn một làm chính.
- **Phụ thuộc:** số MicroRank P3; trần coverage.

---

## 7. TraceRCA bản lọc hữu hạn

- **Đã quyết:** dùng bản lọc hữu hạn (Q-62).
- **Đề xuất:** bỏ điểm NaN/inf trước khi sắp; operation có support 0 là "không có bằng chứng", không xếp; hòa giữ điểm bằng nhau để evaluator xử lý (mục 9), thứ tự hiển thị theo tên operation; tổng span bất thường bằng 0 → NO_EVIDENCE; thiếu baseline của operation ghi riêng; service = `serviceName`, điểm service = max operation.
- **Phương án khác:** gán điểm 0 cho support 0 và xếp cuối (thêm ứng viên hòa ở đáy); giữ nguyên bug sort (chỉ để tái dựng T-007).
- **Vì sao:** NaN không có thứ tự; sort rồi lọc làm thứ hạng phụ thuộc thứ tự dòng (T-007: đổi thứ tự dòng làm đổi hạng đáp án ở 22/90 ca). "Không có bằng chứng" khác "xếp cuối".
- **Sai khi:** zero-support chiếm phần lớn service; khi đó Retrieval@all thấp do quy ước, phải báo.
- **Phụ thuộc:** số TraceRCA P3; tác động NaN + hòa được báo gộp, không quy cho một lỗi (SPEC).

---

## 8. Trạng thái lỗi và bản ghi mỗi lượt

- **Đề xuất:** mỗi (ca, phương pháp, cấu hình, seed) một bản ghi gồm trạng thái `OK`, `NO_EVIDENCE`, `ERROR`, `UNSUPPORTED`, `TIMEOUT`; danh sách xếp hạng kèm điểm; đếm nhánh dự phòng (TORAI); cờ "thứ hạng trùng thứ tự cột". Mọi trạng thái khác `OK` vẫn ở mẫu số và tính trượt (hạng ∞). Báo số ca theo trạng thái cạnh mỗi bảng.
- **Phương án khác:** bỏ ca lỗi khỏi mẫu như `main.py:552–553` — làm số đẹp hơn thật; MRP P3 cấm.
- **Phụ thuộc:** mọi bảng P3.

---

## 9. Cách chấm xếp hạng

- **Đã quyết:** MRR, NDCG@5, Hit@1/3/5 (MRP P7), AC@k và Avg@5 (để so RCAEval), Retrieval@K và Rerank@1 với K = 5, 10 bằng hàm RCAEval (Q-65); bootstrap theo ô (MRP P7).
- **Đề xuất:**
  1. **Hòa:** nhóm các thực thể cùng điểm (so bằng đúng giá trị float của phương pháp). Hit, RR, DCG tính kỳ vọng khi thứ tự trong nhóm là ngẫu nhiên đều; báo kèm cận lạc quan/bi quan (như T-017, WHY-17). Phương pháp chỉ trả thứ tự (TORAI) coi là không hòa.
  2. **Hàm RCAEval** (AC@k, Avg@5, Retrieval@5/10, Rerank@1): nạp danh sách đã phá hòa theo tên thực thể, ghi rõ "theo định nghĩa RCAEval, hòa phá theo tên". Ca không phải `OK` nạp danh sách rỗng để giữ ở mẫu số.
  3. Root vắng khỏi danh sách: Hit = 0, RR = 0, DCG = 0.
  4. Ghi rõ trùng nghĩa: Hit@k = AC@k ở mức thực thể với một root; Retrieval@K = AC@K; Rerank@1 = AC@1 / AC@K; NDCG@5 là hàm của hạng. Không trình bày như bằng chứng độc lập (WHY-06).
  5. **Bootstrap:** lấy lại 10 ô dev có hoàn lại, mỗi ô mang cả 3 ca; B = 10.000; seed 20261005; khoảng phân vị 95 %. Phương pháp nhiều seed: trung bình theo seed của từng ca trước khi bootstrap; báo khoảng giữa các seed riêng.
  6. Báo theo loại lỗi, theo ô, theo nhóm vị trí root (cột `nhom_vi_tri_p75` của T-021), và từng ca.
- **Phương án khác:** bootstrap theo ca (bỏ qua tương quan trong ô); phá hòa theo thứ tự cột như code gốc (biến thứ tự cột thành bằng chứng, MRP P3 cấm).
- **Sai khi:** 10 ô quá ít cho khoảng tin cậy ổn định — báo khoảng rộng, không thu hẹp bằng bootstrap theo ca.
- **Phụ thuộc:** mọi bảng xếp hạng P3, P7.

---

## 10. Chế độ (b): phạm vi, chuỗi đầu vào bộ phát hiện, trạng thái

- **Đã quyết:** Q-67 chọn tập cột BOCPD theo `reproduce_bocpd` (chỉ tập cột, không cách cắt 300+300 quanh mốc). Q-72 cho BOCPD chạy EC2 qua đêm ở T-025 (≤ 20 giờ), đầu vào không chọn theo mốc tiêm.
- **Câu hỏi:** hồi cứu hay online; chuỗi nào đưa vào bộ phát hiện; tiền xử lý dùng tương lai xử lý ra sao.
- **Sự thật quan trọng:** mọi ca RE2-TT được cắt quanh lỗi, mốc luôn ở giây 720 của file 1.441 giây. Vì vậy **mọi lịch chia đoạn theo vị trí trong file đều tương đương một lịch theo mốc tiêm** trên dataset này. "Đoạn chọn bằng lịch độc lập lỗi" không còn độc lập thật.
- **Đề xuất:**
  1. Gọi đúng tên: **phát hiện hồi cứu trên bản ghi đã chọn vì có sự cố**, không gọi là giám sát online (T-013 `cua-so-va-che-do-b.md` §3).
  2. **Chuỗi đầu vào: cả bản ghi 1.441 điểm**, một lần, không khởi động lại, không mang trạng thái giữa ca, không lịch sử trước đầu file.
  3. Tiền xử lý **giữ đúng code tác giả**: BOCPD bỏ cột hằng, ffill, điền 0, min–max trên toàn chuỗi (`reproducibility.py:147–154`); N-Sigma dùng mean/std quá khứ mở rộng. Khai báo look-ahead của BOCPD (min–max, bỏ cột hằng dùng cả chuỗi). Không thêm biến thể nhân quả.
  4. Bộ phát hiện chỉ nhận bảng metric (cột `time` + các cột đã chọn). Không nhận mốc tiêm, root, loại lỗi, tên hoặc đường dẫn ca.
  5. Bỏ điểm đổi "sentinel" ở chỉ số T (ngoài dữ liệu, lỗi biên `_bocpd.py:196,225`); đếm và ghi số lần bỏ. Nếu giữ, mọi ca đều có một "báo động" sau mốc, làm recall giả bằng 1.
  6. Warm-up: giữ mặc định code (N-Sigma `startsfrom=100`; BOCPD không có). Báo động trong 100 điểm đầu vẫn tính, báo thêm riêng để chẩn đoán.
  7. Nhịp báo động: mỗi điểm 1 s đều được đánh giá, như code; không lấy mẫu thưa. Thống kê được dùng tại điểm i: N-Sigma dùng mean/std của mọi điểm trước i (nhân quả); BOCPD dùng posterior tới i nhưng dữ liệu đã được chuẩn hóa bằng min–max toàn chuỗi (look-ahead khai báo).
- **Phương án khác:** (i) đoạn 600 điểm bước 300 từ đầu file — rẻ hơn khoảng một phần ba theo phép tính O(T²) (3 × 600² + 541² so với 1.441², chưa đo) nhưng, như nói trên, lịch này vẫn gắn với mốc; thêm biên khởi động lại; SPEC cấm chia đoạn để làm đẹp chi phí; (ii) tiền xử lý nhân quả (min–max mở rộng) — biến thể mới cần WHY và kiểm, không có câu hỏi P3 nào đòi; (iii) nối các ca thành một dòng giả — SPEC cấm.
- **Sai khi:** chi phí BOCPD trên 1.441 điểm vượt 20 giờ cho 30 ca (Q-72). Khi đó dừng theo Q-72, giữ ca đã xong, trình Minh; không tự cắt đoạn.
- **Phụ thuộc:** mọi số phát hiện P3 (T-025); RCA chế độ (b).

---

## 11. Chế độ (b): tập cột N-Sigma, gộp episode, chấm phát hiện, RCA sau báo động

- **Đề xuất:**
  1. **Tập cột N-Sigma:** cùng tập cột với BOCPD (luật `reproduce_bocpd`: `latency-50` hoặc `_error`), để hai bộ phát hiện được so trên cùng đầu vào. Phương án khác: mọi cột (mặc định khi gọi `nsigma` trên cả bảng; T-005 chạy cách này, 59 s/ca) — nhiều cơ hội báo động hơn nên so không cùng đầu vào. **Đây là điểm tôi không chắc; Minh chọn.**
  2. **Báo động → episode:** episode bắt đầu ở báo động đầu tiên; mọi báo động trong 300 s sau đó thuộc episode này (thời gian trơ 300 s = cửa sổ sau mốc Q-64; MicroRank bài §4.2 "flush 5 phút" sau báo động). Báo động N-Sigma được sắp và bỏ trùng trước (hàm gốc trả danh sách chưa sắp, T-013).
  3. **Nhãn phát hiện (chỉ evaluator):** bất thường = [t_tiêm, cuối file]; bình thường = [đầu file, t_tiêm), theo định nghĩa bài BARO ("trong thời gian tiêm là bất thường, trước đó bình thường"). Giả định lỗi kéo dài tới cuối file: **chưa kiểm**, RE2 không công bố thời lượng lỗi.
  4. **Độ đo:** (i) theo episode: TP nếu episode bắt đầu trong đoạn bất thường; FP nếu trước; (ii) theo ca: tỉ lệ ca có ít nhất một episode TP; (iii) theo cửa sổ thời gian (MRP P3): cửa sổ 60 s tính từ đầu file (60 s là cửa sổ bộ phát hiện trong code MicroRank, `online_rca.py:158–163`; vì mốc ở giây 720 nên biên cửa sổ trùng mốc, đây là đặc điểm của RE2-TT, ghi lại), cửa sổ dự đoán dương nếu có báo động, không "point-adjust"; (iv) số episode FP trên mỗi giờ bình thường (mẫu số 30 × 720 s = 6 giờ); (v) độ trễ = đầu episode TP đầu tiên − t_tiêm, gọi là "độ trễ từ lúc tiêm" (MRP P7).
  5. **Ghép bộ phát hiện với ranker:** chỉ ghép những cặp có cơ sở prior work: bài BARO ghép từng phương pháp RCA với từng bộ phát hiện (`RCA[Detector]`, Bảng 3), gồm RobustScorer (BARO) và CIRCA; bài TORAI giả định mốc từ bộ phát hiện ngoài (§2). Đề xuất chế độ (b) chạy BARO, CIRCA kiến trúc, TORAI, mỗi cái với cả hai bộ phát hiện. MicroRank, TraceRCA (có bộ phát hiện trace riêng) và SimpleRCA không chạy chế độ (b) ở P3; ghi lý do. Riêng MicroRank bài gốc có bộ phát hiện online (μ+1,5σ, hơn 8 trace) nên thuộc nhóm "có bộ phát hiện" của MRP P3; nhưng bộ phát hiện đó cần `span.kind`, root frontend-server và pod mà RE2-TT không có (`results/T-015/ho-so-microrank.md` §9.1), còn bản RCAEval sửa cần mốc `t` để học ngưỡng. Chạy MicroRank chế độ (b) vì vậy cần suy các trường thiếu, là biến thể mới chưa có WHY — đề xuất không làm ở P3 và ghi giới hạn.
  6. **RCA sau báo động:** chỉ episode đầu tiên của ca kích hoạt RCA (như BARO dùng điểm đổi đầu tiên, `root_cause_analysis.py:285–291`). Cửa sổ RCA theo Q-64 quanh thời điểm báo động t̂: N = [t̂−300, t̂), A = [t̂, t̂+300), cắt ở biên file và ghi độ dài thực. Episode đầu là FP thì RCA vẫn chạy và vẫn chấm theo root của ca (đó là hành vi thật của pipeline).
- **Phương án khác:** gộp báo động cách nhau ≤ 5 điểm (`find_anomalies`, `anomaly_detection.py:68–73`) — tạo rất nhiều episode khi nhiều cột; mỗi episode chạy một RCA — chi phí T-025 = bộ phát hiện + số episode × ranker, chưa có số episode; ghép mọi ranker với mọi bộ phát hiện — tạo pipeline mới không có prior work.
- **Sai khi:** bộ phát hiện báo động rất sớm (trước mốc) ở hầu hết ca; khi đó RCA chế độ (b) chủ yếu đo RCA trên dữ liệu bình thường. Đó vẫn là kết quả cần báo, không đổi luật sau khi xem.
- **Phụ thuộc:** bảng phát hiện riêng (Q-30), RCA chế độ (b), chi phí T-025.

---

## 12. Seed, cấu hình, ngân sách nhãn

- **Đã quyết:** ngân sách nhãn root = 0 cho mọi baseline (Q-66); TORAI ít nhất 3 seed, đặt seed theo ca (WHY-19, WHY-20).
- **Đề xuất:** TORAI seed {0, 1, 2}, `np.random.seed(s)` ngay trước mỗi lời gọi; phương pháp tất định chạy một lần, kiểm lặp lại và hoán vị ở một phần ca; MicroRank khóa `PYTHONHASHSEED=0`, kiểm thêm 1. Mọi tham số giữ mặc định code tác giả (hazard 1/50, k = 3, startsfrom = 100, θ DA = 3, 25 vòng PageRank, d = 0,85). Không chỉnh tham số bằng nhãn dev.
- **Phụ thuộc:** tính tái lập; WHY-20.

---

## 13. Chọn ca pilot (bước 4)

- **Đề xuất:** với mỗi phương pháp, tối đa 3 ca theo yếu tố chi phí lấy từ metadata, không theo root, loại lỗi hay accuracy: phương pháp metric và bộ phát hiện — số cột d thực đưa vào (T = 1.441 hoặc 600 cố định): ca d nhỏ nhất, trung vị, lớn nhất theo `cot-bocpd-dev.csv` hoặc số cột metric; phương pháp trace — số span toàn file (`results/T-015/runs/independent-math/tt-schema-assessment.json`): nhỏ nhất, trung vị, lớn nhất. Hòa thì lấy mã mờ nhỏ hơn. Ghi ca nào phủ mức nào.
- **BOCPD:** đo trước một ca d trung vị trên laptop với giới hạn 1 giờ; nếu chạm giới hạn chỉ báo cận dưới (SPEC). Lượt nào dự kiến trên 1 giờ phải xin Minh (luật cứng 8).

---

## 14. Câu hỏi cho Minh (một lượt)

| # | Câu hỏi | Đề xuất của tôi | Mục |
|---|---|---|---|
| Q1 | Tách T-022 (B) hay cho hai phiên (A)? | B: tách, T-030 làm bước 3–5 | 0 |
| Q2 | Cửa sổ chế độ (a): nửa mở theo timestamp, giữ cách chia nội bộ của tác giả? | Đồng ý | 1 |
| Q3 | Nguồn đầu vào TORAI: dữ liệu tác giả (A), tự dựng (B), hay A + kiểm độ nhạy (C)? | A | 2 |
| Q4 | Universe U = 68 thực thể `ts-*` (gồm DB), chấm danh sách nguyên trạng, không điền phần thiếu? | Đồng ý | 3 |
| Q5 | Bộ cột: dùng cột có trong file, không bỏ `_error`, ghi audit cột vắng ở evaluator? | Đồng ý | 4 |
| Q6 | CIRCA: RHT+DA tuyến tính làm chính, kèm RHT-only; giữ metric cô lập; đồ thị từ trace trong N? | Đồng ý | 5 |
| Q7 | MicroRank: xếp đầy đủ làm chính, kèm top-11? | Đồng ý | 6 |
| Q8 | TraceRCA: support 0 là không có bằng chứng, không xếp? | Đồng ý | 7 |
| Q9 | Ca lỗi/không bằng chứng ở mẫu số, tính trượt? | Đồng ý | 8 |
| Q10 | Hòa tính kỳ vọng + cận; bootstrap theo ô B = 10.000? | Đồng ý | 9 |
| Q11 | Chế độ (b): hồi cứu, cả bản ghi 1.441 điểm, giữ tiền xử lý tác giả, bỏ sentinel? | Đồng ý | 10 |
| Q12 | Tập cột N-Sigma: cùng tập BOCPD hay mọi cột? | Cùng tập BOCPD (không chắc) | 11.1 |
| Q13 | Episode thời gian trơ 300 s; chấm theo episode, ca, cửa sổ 60 s, FA/giờ, độ trễ? | Đồng ý | 11.2–11.4 |
| Q14 | Chế độ (b) chỉ cho BARO, CIRCA, TORAI; RCA chỉ ở episode đầu? | Đồng ý | 11.5–11.6 |
| Q15 | Cho ghi các mục WHY theo `de-xuat-why.md` (gồm Q-64–Q-67 và ghi chú WHY-19)? | Duyệt từng mục | WHY |
| Q16 | `REVIEW.md` của task đang chứa phản biện gói tài liệu. Phản biện kết quả T-022 ghi vào đâu? | Codex ghi `REVIEW-ket-qua.md`; tôi điền bảng phản hồi của REVIEW cũ nếu Minh cho | — |
