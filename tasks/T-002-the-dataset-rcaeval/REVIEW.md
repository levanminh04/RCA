# Phản biện T-002

- **Người phản biện:** Claude — **Ngày:** 03/10/2026 — **Commit/diff đã đọc:** base `38d3c1b` (theo `handoff-manifest.json`). `git diff` chỉ có `docs/STATE.md` và `docs/DECISIONS.md`. Dòng T-002 của STATE khớp `state-update.json`. Q-37/Q-38 và dòng T-001 thuộc T-001, không tính cho T-002. Kết quả chưa track được đọc trực tiếp. 93 artifact khớp hash ghi trong `verification/run-003/checks.json`.
- **Đã đọc:** SPEC, LOG; `mau-the-dataset.md`, `the-rcaeval.md`, `public-sources.md`; năm script; `local-inspection/run-002/` (manifest, cases, schemas, summary, case-summary, graph-degrees, all-service-positions, symptom-channel-bands, symptom-entity-rates, probe-case-summary, probe-cell-summary); `public-metadata/run-002/` (source-manifest, count-summary, root-fault-cells, verification, run.json, hf-tree, `sources/` gồm hf-README, github-README, paper-v2); `verification/run-001` và `run-003`; handoff-manifest, state-update, requirements.txt; DT18, advisor-2026-09-23, MRP §2–§4 và P2, WHY-03/04, DECISIONS Q-21/Q-31/Q-33, LESSONS, K2, một phần K3 về RCAEval.
- **Đã chạy (chỉ đọc):** tính lại từ CSV/JSON đã lưu. Đọc thêm vài file trong `data/rcaeval/` để kiểm cách ghi span gốc, ID trong log, cột workload, log lỗi của RE3-TT. Không mở `data/locked/`, không đọc archive, không ghi file nào khác.

## Kết luận chung

Số trong ba tài liệu khớp artifact. Tử/mẫu parent, khóa cùng trace, đếm RE3, phạm vi regex log và mức OPEN của RE3-OB đều đúng. Thẻ không chọn dataset và không gọi tín hiệu ngoài root là lan truyền.

Có một lỗi chặn: phần rò nhãn bỏ sót việc chính cửa sổ telemetry được cắt đối xứng quanh mốc tiêm. Bốn điểm không chặn đều là thiếu sót diễn giải, sửa bằng dữ liệu đã lưu hoặc vài câu.

## Các điểm

### R1. Biên cửa sổ file làm lộ mốc tiêm; thẻ không nêu — CHẶN

- **Ở đâu:** `the-rcaeval.md`, mục 5 và 8 của RE2-TT, RE2-OB, RE3-TT ("Mốc tiêm dùng để mô tả hai chế độ, không làm đầu vào bộ tự phát hiện"; "inject_time là nhãn biên"). Thêm dòng "Phát hiện theo thời gian" của bảng khả năng chấm, và danh sách "Nhãn ở đâu" ở mục 8 của `mau-the-dataset.md`. Bước SPEC: 2 và 5. Đầu ra MRP P2: kiểm rò nhãn và bảng "task nào chấm được".
- **Sai gì:** thẻ coi mốc tiêm chỉ nằm trong `inject_time.txt`. Thực ra cả ba file telemetry đều được cắt đúng từ mốc tiêm −720 s đến +720 s (RE2), hoặc ±900 s (RE3-TT). Bộ phát hiện nhận nguyên file sẽ biết lỗi bắt đầu ở giữa file. Đây là đầu vào suy ra từ nhãn (AGENTS luật cứng 6). Vì vậy câu "có thể chấm injection-regime" mạnh hơn bằng chứng.
- **Bằng chứng:**
  - `cases.json`: ở 32/32 ca mục tiêu, `metric_time_min − inject_time` = −720 (RE3-TT: −900) và `metric_time_max − inject_time` = +720 (+900).
  - `summary.json`: `normal_rows` 720–720 (RE3-TT 900) và `post_rows` 721–721 (901) ở mọi ca.
  - Biên trace (`epoch_min/max`) và biên log lệch biên metric không quá 1 s, ở mọi ca có trace/log.
  - Hai mẫu Sock Shop cũng ±720. Chỉ RE1-OB khác: mốc tiêm nằm ngoài file.
  - `hf-README.md`: index có cột `normal_timesteps`, `faulty_timesteps`; ví dụ mẫu dùng inject_time để chia normal/faulty.
- **Phản bác đã xét:**
  - Với RCA biết trước cửa sổ (RQ3b), mốc tiêm được cho một cách hợp lệ, nên không có rò mới.
  - Thẻ chỉ cho chấm phát hiện "khi giao thức P7 ghi rõ", và K2 §1 cũng giới hạn phần phát hiện.
  - Nhưng không chỗ nào nêu rò qua biên file, nên giao thức P7 không biết cần xử lý điều này.
  - Với 60 ca khóa và phần còn lại của toàn kho, việc cắt đối xứng chưa kiểm.
- **Hậu quả:** lỗi đã xảy ra là mục rò nhãn còn thiếu. Nguy cơ là ở G1/P7: RQ3a (P/R/F1 phát hiện) có thể bị chấm trên nguyên file, trong khi file đã chứa vị trí lỗi. DT18 có yêu cầu "phát hiện dấu hiệu bất thường".
- **Đề xuất sửa:** thêm vào mục 8 của ba thẻ có mẫu, và vào dòng "Phát hiện theo thời gian":
  - FACT trên mẫu: số ca, độ dài ±720/±900 s, cả ba nguồn tín hiệu.
  - CANDIDATE — chưa kiểm cho phần chưa đọc.
  - Ghi rõ đây là rò mà giao thức phát hiện phải xử lý; cách xử lý do P7/G1 quyết.

  Thêm "biên cửa sổ file" vào danh sách "Nhãn ở đâu" của mẫu thẻ. Không cần chạy lại.

### R2. Dòng "Tất cả metric" chủ yếu phản ánh kênh mem, vốn đã lệch trước tiêm — KHÔNG CHẶN

- **Ở đâu:** `the-rcaeval.md` mục 6 của RE2-TT và RE3-TT; dòng 7 bảng tiêu chí; mục 4 phần "Phép tính chung". Bước SPEC: 4.
- **Sai gì:** thẻ giải thích tỷ lệ cao bằng một danh sách ngang nhau: OR nhiều kênh, flat band, mẫu ít, drift. Dữ liệu đã lưu cho thấy một loại kênh (mem) chiếm phần lớn. Kênh này đã vượt band nhiều ngay trong đoạn đối chứng trước tiêm. LESSONS QT5 yêu cầu dừng tìm nguyên nhân khi một nhóm kênh chiếm gần hết. Ngược lại, flat band góp rất ít.
- **Bằng chứng:** tôi tính lại từ `symptom-channel-bands.csv`, cho service ngoài root theo heuristic tên, trung bình theo ca, q = .995.
  - RE2-TT, kênh mem: đối chứng 27,4%, sau tiêm 57,5%. Mức kỳ vọng là 0,5% nếu tham chiếu và đối chứng cùng phân phối, tức cao gấp khoảng 55 lần.
  - RE2-TT, các kênh khác: đối chứng ≤ 5,4%, sau tiêm ≤ 19,1% (latency-90 là 19,1%).
  - Dòng "Tất cả metric" của thẻ là 33,70% → 67,59%. Mem đã chiếm phần lớn con số này.
  - Mem sau tiêm cao ở cả 10 ô, kể cả lỗi mạng: auth×delay 35%, travel×loss 72%. Riêng auth không có cạnh trace nào.
  - Kênh có flat band (mọi kênh, RE2-TT): đối chứng 1,4%, sau tiêm 4,4%.
  - RE3-TT, kênh mem: 25,9% → 52,6% ở q = .95, nhưng 0,0% → 0,2% ở q = .995. Điều này giải thích phần lớn mức "rất nhạy ngưỡng" mà thẻ nêu.
  - RE2-OB khác hai bộ trên: cpu, latency và workload đều lên 67–82% sau tiêm. Mem không phải nguồn chính ở RE2-OB.
- **Phản bác đã xét:**
  - Thẻ không gọi mức tăng này là lan truyền, và CANDIDATE đã liệt kê drift.
  - CSV chỉ có số đếm, không có hướng thay đổi, nên chưa chứng minh được mem trôi theo thời gian.
  - Vì vậy đây là lỗi diễn giải, không phải lỗi số.
- **Hậu quả:**
  - Ở G1, con số khoảng 68% dễ bị đọc là tín hiệu lan cho tiêu chí 7.
  - Phép so đối chứng/sau tiêm còn thiên về chênh dương với mọi kênh trôi, vì đoạn sau tiêm nằm xa đoạn tham chiếu hơn.
  - Latency-90 cũng có đối chứng 5,4%, gấp khoảng 10 lần mức kỳ vọng, nên cũng cần cảnh báo nhưng nhẹ hơn.
- **Đề xuất sửa:** thêm một đoạn ngắn lấy từ CSV sẵn có: tỷ lệ theo loại kênh, và nêu mem là thành phần chính của dòng "Tất cả metric" ở RE2-TT/RE3-TT. Ghi rằng dòng này không đủ làm bằng chứng cho tiêu chí 7. Không cần chạy lại.

### R3. Sáu ca đồ thị nhỏ tập trung ở hai service gốc; bảng bậc gộp che điều này — KHÔNG CHẶN

- **Ở đâu:** `the-rcaeval.md` RE2-TT mục 3 (bảng bậc; đoạn "3 cấu trúc"); dòng 5 bảng tiêu chí. Bước SPEC: 3.
- **Sai gì:**
  - Bảng bậc tính trên cả 30 ca, không tính trong các ca mà service đó là root.
  - Cả 6 ca đồ thị nhỏ đều thuộc ô có root là order hoặc travel.
  - Khi order là root, nó ở vị trí (1,1) trong 4/6 ca của nó. Bảng hiện tại lại cho cảm giác order chủ yếu ở (5,1).
  - Lời giải thích "workload/độ phủ đo" của thẻ đúng nhưng chung chung, không nêu sự trùng này. Đây là gộp số trước khi tách theo ô (LESSONS QT15).
- **Bằng chứng:**
  - `cases.json`: đồ thị 20 nút/20 cạnh ở order×disk lặp 2–3, order×loss lặp 2–3, travel×disk lặp 3. Đồ thị 21/21 ở travel×disk lặp 2. Lần lặp 1 của ba ô này đều là 27/55.
  - `graph-degrees.csv`, lọc `is_root`, cửa sổ trước tiêm: order (1,1) ở 4 ca, (5,1) ở 2 ca. Travel (2,3) ở 2 ca, (4,5) ở 4 ca. Auth, route, train không đổi.
  - Bảy node vắng trong đồ thị nhỏ: preserve, preserve-other, seat, security, user, contacts, payment.
  - Tôi rà nhanh 4 file metric, chỉ đoạn trước tiêm. Ở order×disk lặp 2, không có các cột `_workload` của preserve, seat, security, user, contacts. Ở travel×disk lặp 3, các cột này bằng 0. Ở lặp 1 của hai ô đó, chúng có giá trị (seat khoảng 8,5).
  - Workload của order: 0,40 ở order×disk lặp 2, so với 5,35 ở lặp 1.
  - Như vậy luồng đặt vé có vẻ không chạy trong các lần lặp đó, không chỉ là thiếu trace. Tôi mới rà 4 ca, chưa kiểm cả 6.
- **Phản bác đã xét:**
  - Thẻ đã cho thấy đồ thị trước tiêm trùng toàn cửa sổ, nên khác biệt không do tiêm lỗi; và đã nêu workload như một khả năng.
  - Nhưng việc các lần lặp trong cùng một ô có workload và đồ thị khác nhau là thông tin G1 cần.
  - Nó liên quan tiêu chí 5, và tiền đề "ba lần lặp của một ô gần như giống nhau" của WHY-04.
- **Hậu quả:** phân tích "kết quả theo vị trí service gốc" (RQ1) trên RE2-TT sẽ bị lẫn với khác biệt workload ở hai service gốc.
- **Đề xuất sửa:**
  - Thêm danh sách 6 ca, và bậc của root trong chính các ca của nó (từ cột `is_root` của `graph-degrees.csv`).
  - Ghi FACT về bảy node vắng.
  - Ghi CANDIDATE — chưa kiểm: workload của các lần lặp này khác nhau, kèm lời giải thích khác.
  - Thêm vào mục 10 một dòng OPEN: định nghĩa lá/giữa/hub cần Minh quyết (WHY) trước khi dòng 5 trả lời được câu "nhiều vị trí" của MRP §4. Không sửa K2.

### R4. Trace RE2-OB thiếu ba service dù có metric/log; chưa nêu nguy cơ cho RE3-OB — KHÔNG CHẶN

- **Ở đâu:** `the-rcaeval.md` RE2-OB mục 3–4; RE3-OB mục 3 (bảng bậc) và mục 10. Bước SPEC: 2–3.
- **Sai gì:**
  - Thẻ RE2-OB ghi 5 root đều có trong graph, và "không coi 7 node mẫu là toàn kiến trúc".
  - Nhưng thẻ không nêu FACT cụ thể: cartservice, shippingservice, adservice (và redis) có metric và log nhưng không có span nào trong cùng ca.
  - Vì vậy bậc ra 4 của checkout là bậc trong phần được trace, không phải bậc trong hệ.
  - RE3-OB có 12/30 ca mà root là adservice (9 ca) hoặc cartservice (3 ca). Thẻ RE3-OB chỉ ghi "OPEN, không có mẫu".
- **Bằng chứng:**
  - `cases.json`, re2ob: node trace gồm checkout, currency, email, frontendservice, payment, productcatalog, recommendation.
  - `schemas.json`: có cột `adservice_*`, `cartservice_*`, `shippingservice_*`, kể cả latency-90.
  - Log mẫu (tôi đọc `container_name`): 11 tên, gồm adservice, cartservice, shippingservice, redis.
  - Bài v2 §3.1: Online Boutique có 12 service.
  - `count-summary.json`, RE3-OB: adservice 9, cartservice 3.
- **Phản bác đã xét:** thẻ cố ý không suy từ RE2-OB sang RE3-OB, và điều đó đúng. Vì vậy chỉ nên ghi đây là nguy cơ, không ghi thành FACT.
- **Hậu quả:** ở G1, RE3-OB dễ được hiểu là có 4 root ở 4 vị trí đồ thị (tiêu chí 5) và có đủ trace (tiêu chí 3). Bằng chứng gần nhất hiện có lại nghiêng về chiều ngược lại.
- **Đề xuất sửa:**
  - Thêm FACT về các service vắng trong trace vào RE2-OB mục 3–4.
  - Thêm vào RE3-OB mục 3 và 10 một dòng CANDIDATE — chưa kiểm: root ad/cart có thể không có node trace; giả định là RE3-OB dùng cùng cách gắn bộ đo; sai nếu RE3-OB gắn bộ đo khác.

### R5. Đối chiếu nguồn bỏ sót hai khẳng định về nhãn chỉ báo và kênh trace của RE3 — KHÔNG CHẶN

- **Ở đâu:** `public-sources.md`, mục "Nội dung tài liệu"; `the-rcaeval.md`, bảng khả năng chấm; RE3-TT dòng 6 bảng tiêu chí và mục 4. Bước SPEC: 3 và 5.
- **Sai gì:**
  - (a) Bài v2 §3 nói mỗi ca có "root cause indicator" (chỉ báo gốc). §3.2 định nghĩa nó theo loại lỗi: CPU hog → metric CPU; DELAY → latency; lỗi mã nguồn → stack trace trong log hoặc response code. Tree ở revision không có file chỉ báo nào cho bốn bộ; `root_cause.txt` chỉ có ở 8 ca RE3-SS. Thẻ kết luận đúng là không chấm được operation/code line. Nhưng thẻ không ghi khẳng định trái chiều này của nguồn, và không ghi rằng chỉ báo của RE2, theo bài, thực chất suy ra từ tên thư mục.
  - (b) HF card, README và bài đều nói RE3 hỗ trợ chẩn đoán qua "response codes in traces". Ở mẫu RE3-TT, `statusCode` rỗng ở mọi span. Thẻ chỉ ghi "0 / 0" trong bảng, không nối với tiêu chí 6. MRP §4 coi lỗi mã nguồn quan trọng chính vì nó có thể hiện ở log/trace.
- **Bằng chứng:**
  - `paper-v2.html` §3 và §3.2, các đoạn về "root cause indicator".
  - `hf-tree.json`: 8 file `root_cause.txt`, tất cả ở re3ss.
  - `summary.json` re3tt: `status_nonnull` = 0 trên 183.623 span.
  - `hf-README.md`: câu "response codes in traces".
  - Tôi rà nhanh log mẫu RE3-TT bằng regex `Exception|\tat |ERROR`: 109 dòng, 0 trước tiêm, 109 sau tiêm. Trong đó 106 dòng ở service khác root (travel 42, admin-travel 36, travel2 26…), 3 dòng ở route. Đây là rà thô trên một ca, chỉ để cho thấy kênh log đáng ghi rõ; không phải kết quả thay thẻ.
- **Phản bác đã xét:** thẻ đã ghi "Không thấy lệch metric cũng chưa loại trừ biểu hiện ở log/trace". Vì vậy đây là thiếu đối chiếu nguồn, không phải kết luận sai.
- **Hậu quả:** G1 có thể đánh giá tiêu chí 6–7 của RE3 chỉ qua probe metric (RE3-TT 9,10% sau tiêm ở q = .995). Trong khi đó, trên mẫu, kênh trạng thái của trace trống, và nguồn chỉ ra log là nơi chính để thấy lỗi mã nguồn.
- **Đề xuất sửa:** thêm vài dòng FACT/OPEN vào `public-sources.md`, và vào RE3-TT dòng 6 cùng mục 4:
  - nguồn khẳng định gì, và revision thực có gì;
  - trace status trống trên mẫu;
  - tín hiệu log của RE3: OPEN — chưa kiểm.

  Không yêu cầu làm probe log trong T-002.

## Điều đã kiểm và thấy đúng

- **Phạm vi ghi:** file mới của T-002 chỉ nằm trong `results/T-002/`, `requirements.txt` và LOG. STATE chỉ đổi dòng T-002. Không thấy file nào ngoài phạm vi.
- **Dữ liệu khóa:** không mở `data/locked/`. Cả 100 input trong manifest đều thuộc `data/rcaeval/`, và `safe_file` chặn "locked". Mốc tiêm của 29 ca dev lấy từ HF ở đúng revision đã ghim, có sha256, thay vì đọc `cases.parquet` bị khóa.
- **Ghi chú quy trình, không ảnh hưởng số liệu:** LOG không ghi việc trình Minh dung lượng trước khi tải 29 file đó (290 byte), theo Q-21 / luật cứng 7. Minh xét.
- **Liên kết span cha–con:**
  - Span gốc là `parentSpanID` null. Tôi kiểm trực tiếp trên mẫu OB và RE3-TT: số null bằng số root trong thẻ; không có giá trị rỗng hay "0"; không span nào tự trỏ về chính nó.
  - Khóa là (traceID, parentSpanID) trong cùng file. Mẫu số không gồm span gốc. Số key trùng là 0.
  - Ba bảng trace khớp `summary.json`. Lần kiểm hỏng `verification/run-001` được giữ, và nguyên nhân (NaN) đúng như LOG.
- **Log:** không có cột trace/span ID. Tôi rà thêm chuỗi hex 16/32 ký tự trong message của mẫu OB và RE3-TT: 0 dòng, 0 khớp ID trace. Thẻ nói đúng phạm vi: regex không chứng minh ghép theo request, và việc ghép còn OPEN.
- **Số đếm:**
  - RE2-TT và RE2-OB: 90 ca, 5 root, 6 lỗi, 30/30 ô, lặp 3.
  - RE3-TT: 30 ca, 2 root, 4 lỗi, 8/8 ô, lặp 3–6 (route×f3 = 6; auth×f1–f3 = 4).
  - RE3-OB: 30 ca, 4 root, 5 lỗi, 10/20 ô, lặp 3.
  - Tất cả khớp `root-fault-cells.csv` và tree. Thẻ không biến lưới RE3 thành lưới đều. Chỗ lệch f5 của HF card và "3–5 lần" của bài được ghi đúng, không sửa nguồn.
- **So với K2:** tôi tái lập được: travel×disk lặp 2 có thêm `ts-payment-service` và cạnh từ inside-payment sang payment. Thẻ giữ bằng chứng, nêu các lý do chưa chắc, không sửa K2.
- **Probe triệu chứng:**
  - `metric_excursions` chỉ nhận (frame, boundary). Root được gắn sau, và không dùng để chọn SLI.
  - Có đủ ba giá trị q, đoạn đối chứng là 1/3 cuối trước tiêm, flat band được lưu riêng, rate không xác định bị bỏ khỏi trung bình.
  - Bảng mục 6 của ba thẻ khớp `probe-case-summary.csv` (tôi tính lại). Số của paymentservice RE2-OB khớp CSV.
  - Thẻ không gọi mức tăng ngoài root là lan truyền nhân quả hay nhãn vùng. Bảng chấm ghi vùng ảnh hưởng chưa chấm được.
  - Probe chỉ dùng để mô tả, nên việc không thêm mục WHY là chấp nhận được.
- **Vị trí root:** thẻ ghi rõ OB và RE3-TT chỉ có 1 ca, và không suy ra topology toàn kho. RE3-OB để OPEN có lý do, đúng SPEC.
- **Thời gian:** ba nguồn tín hiệu khớp nhau trong khoảng 1 s ở mọi ca, đúng như câu "startTimeMillis/1000 khớp epoch metric/log".
- **Q-31 và mẫu thẻ:** thẻ không chọn dataset, không so RCAEval hơn hay kém, và ghi tiêu chí 9 không đạt trong họ RCAEval. Mẫu thẻ không thiên về RCAEval: có ô cho dataset không có trace và cho nhãn theo từng trace.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng một phần — CHẶN phần cảnh báo trước khi chốt giao thức tự phát hiện | Tính lại cases.json: 32/32 ca mục tiêu có metric ±720 s (RE2) hoặc ±900 s (RE3-TT) quanh injection. Thiếu cảnh báo rằng biên telemetry tiết lộ vị trí nhãn tiêm. Đính chính: trace lệch biên metric dưới 1 s, log tối đa 2 s ở RE2-OB, không phải mọi nguồn ≤1 s. Biên hàng quan sát chưa chứng minh cơ chế exporter; điểm giữa là injection, chưa phải onset triệu chứng. Thẻ đã nêu tên ca và nhãn biên, không khẳng định nhãn chỉ ở inject_time.txt; câu chấm injection-regime có điều kiện P7 vẫn hợp lệ nếu xử lý nguy cơ này. Chưa có detector bị chứng minh khai thác rò. Đề xuất bổ sung FACT đúng phạm vi và cảnh báo vào mẫu/thẻ/bảng chấm; phần chưa đọc OPEN. Tự chọn cách cắt hoặc bỏ khả năng chấm phát hiện sẽ vượt bằng chứng và phạm vi. Chi tiết ở LOG phiên tự soát 03/10. | |
| R2 | Đúng một phần — KHÔNG CHẶN | Tính lại cùng nhóm ngoài root từ CSV: RE2-TT q=.995 mem 27,427%→57,548%, OR 33,699%→67,589%; các kênh khác thấp hơn. RE3-TT mem lớn ở q=.95 (25,883%→52,636%), nhưng q=.995 chỉ 0%→0,208%, nên không gọi mem là chính ở mọi ngưỡng. Thẻ đã nêu drift/OR/band0 và không kết luận lan; thiếu phân rã cụ thể, không sai số. Mức 0,5% là danh nghĩa cho một kênh dưới giả định phù hợp, không phải kỳ vọng OR hay chứng minh drift. Cùng phạm vi OR ngoài root, cận OR flat là 0,327–0,418% control và 1,030–1,266% post; số flat của reviewer dùng phạm vi khác, không trực tiếp phân rã dòng OR. Chưa có giao các kênh nên không biết đóng góp riêng khi bỏ mem. Đề xuất bổ sung số theo kênh/q và giới hạn tiêu chí 7. Bỏ mem hoặc đổi ngưỡng chỉ để giảm tỷ lệ có thể loại cả tín hiệu lỗi tài nguyên thật. | |
| R3 | Đúng một phần — KHÔNG CHẶN | Bảng trên 30 graph đúng số và mẫu số; thiếu bậc ở chính ca service là root để diễn giải RQ1. cases.json/graph-degrees.csv xác nhận order (1,1) 4/6, (5,1) 2/6; travel (2,3) 2/6, (4,5) 4/6. Bảy node vắng ở 5 ca 20/20; travel×disk lặp 2 còn payment, chỉ vắng 6 node. Đã đọc lại bốn file metric của reviewer: order_workload trước tiêm 5,351 ở order×disk 1 và 0,400 ở lặp 2; các cột preserve/seat/security/user/contacts thiếu ở order×disk 2, bằng 0 ở travel×disk 3, còn lặp 1 có giá trị (seat 8,496/8,519). Khác biệt số đo là FACT; «luồng đặt vé không chạy» vẫn CANDIDATE vì thiếu/zero metric còn có thể do exporter/instrumentation. Đề xuất bổ sung tách theo root/ca và số node đúng; raw bậc đã đủ mô tả, không cần chốt hub mới trong T-002. Chia lại dev/test hay sửa WHY-04 từ bốn mẫu sẽ vượt phạm vi. | |
| R4 | Đúng một phần — KHÔNG CHẶN | cases.json/schemas.json/rates và log.entities xác nhận ad/cart/shipping/redis có metric/log nhưng vắng graph mẫu RE2-OB; ba service có latency-90. Bậc checkout là bậc quan sát, điều này thẻ đã giới hạn; thiếu tên node và hệ quả ánh xạ cụ thể là có thật. RE3-OB có ad 9, cart 3 ca, nhưng chưa có telemetry: không đủ coi thiếu trace là FACT, hoặc coi tiêu chí 3/5 đã đạt. Các ô hiện tại đã ghi OPEN có lý do, đúng SPEC. Đề xuất thêm FACT về độ phủ RE2-OB; nếu ghi nguy cơ RE3-OB phải nêu giả định instrumentation tương tự và điều kiện sai khi exporter/workload/phiên bản khác. Dùng mẫu RE2-OB để loại RE3-OB có thể loại nhầm bộ; không tải mới hay chọn dataset. | |
| R5 | Đúng một phần — KHÔNG CHẶN | Paper v2 §3/§3.2 mô tả root cause indicator; tree có 8 root_cause.txt, đều RE3-SS, không có file tên này trong bốn bộ. Đây chưa là bằng chứng thiếu mọi dạng nhãn chỉ báo. RE3-TT status_nonnull=0/183.623; paper §3.4 nói response code khi có sẵn, nên không bác bỏ toàn RE3. Tính lại regex trên raw log cho đúng 109 hàng (0 pre, 109 post; 106 ngoài root, 3 root). Cả 3 hàng root là INFO khởi động: IOException/ServletException trong chữ ký hàm và ExceptionTranslationFilter trong tên lớp, không phải lỗi đã xác minh. 106 hàng ngoài root gồm 53 hàng có từ ERROR và 53 bản ghi stack/exception; số hàng không là số sự cố độc lập hay nhãn lan. Đề xuất đối chiếu lời nguồn/file thực có, giới hạn status và việc đã rà log nhưng chưa xác lập nhãn chỉ báo/vùng. Không suy fault→metric hoặc regex→ground truth; không coi log là kênh chính của toàn bộ RE3 từ một ca. | |
