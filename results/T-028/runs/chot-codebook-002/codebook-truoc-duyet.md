# Codebook T-028 — phân tích hạn chế xếp hạng chế độ (a)

Bản trình Minh duyệt, ngày 07/10/2026. Đây là tiêu chí khai trước bằng chứng mới; chưa có kết quả phân loại hoặc phép đo tập trung P4. Codex làm, Claude phản biện kết quả. SPEC đã được Minh duyệt trong LOG ngày 07/10/2026. Sau khi chốt, thay đổi tiêu chí phải trình Minh và giữ bản/kết quả cũ (SPEC bước 4).

## 1. Câu hỏi, đơn vị và nguồn

Phân tích vì sao ca dev xếp sai theo các dấu hiệu kiểm được. Dữ liệu quan sát chỉ hỗ trợ cơ chế ứng viên. Chỉ membership và luật trả về cho biết rào cản trực tiếp của pipeline; chúng cũng chưa giải thích vì sao rào cản xuất hiện.

- Bảng chính: RE2-TT `cohorts.dev30` trong `results/T-024/cham-a.json`; Nezha-OB `tables.main` trong `results/T-026/cham-a.json`. Sáu phương pháp: `baro`, `simplerca`, `microrank_full`, `tracerca`, `circa_ols_da`, `torai_B`. Tập ca và seed lấy đúng bảng nguồn, không chọn lại theo kết quả.
- Đơn vị đếm là ca × phương pháp × dataset. Với k ∈ {1,5}, ca sai là `status=OK` và Hit@k kỳ vọng đã lưu < 1, không thêm tolerance. Ca đúng là OK và Hit@k=1. Non-OK báo theo trạng thái, không gán cơ chế xếp hạng. Tổng mức trượt Σ(1−Hit) giữ non-OK có Hit=0, khác số ca sai OK. Nguồn quy tắc: giao thức T-022 §8, WHY-28; số trích ở `runs/danh-sach-001/step1.json`.
- CIRCA dev19: chỉ dòng phụ có điều kiện, tái dùng đặc trưng dev30; giữ danh sách loại theo Q-82/WHY-36. Không thay bảng chính hoặc tính các phương pháp khác trên dev19.
- Nezha A/B/trace_guard: chỉ giữ dấu đổi status/Hit đã trích. Thiếu ca ở B là `not_in_cohort`. Không tính đặc trưng, đồ thị hoặc gán cơ chế cho ba view này.
- Nhãn dev: `results/T-022/nhan-dev.json`, `results/T-026/nhan-dev.json`. Ô/loại lỗi/vị trí lấy nguyên trường nhãn và các CSV T-021 trong SPEC; không suy từ tên đường dẫn. Nhóm vị trí là `nhom_vi_tri_p75` đã có, không tính lại từ graph N. Vị trí Nezha T-021 dùng phút chồng ±60 s quanh tiêm, hub còn OPEN; chỉ là nhóm cấu trúc tham chiếu, không là vị trí nhân quả (giao thức §8.9; `results/T-021/vi-tri-root.csv`).
- Bản ghi đầu ra gốc do manifest T-024/T-026 chỉ tới là nguồn O, R, khóa, hòa, seed, trạng thái và diagnostics. Giữ mọi entity sau mapping, gồm service/component/DB; không lọc theo hậu tố tên hoặc theo U (WHY-26, giao thức §8.1). “Service” trong phần tín hiệu/trace là đơn vị native theo schema, không là bộ lọc tập ứng viên. Mỗi thống kê lưu đường dẫn + JSON pointer; hash ở manifest, không rải trong báo cáo. Không dùng bảng phụ ngoài CIRCA dev19 và các view Nezha nêu trên để chọn tiêu chí.

## 2. Dòng dữ liệu và giá trị thiếu

Bước 3 chỉ đọc dev bằng guard: `src/p3/selector.py` với allowlist T-022; `src/p3/nezha.py` với allowlist T-026, `view=main`, guard=0. Không gọi runner/worker, `adapters.*.chay`, `diagnose`, GMM, RCD, PC, Drain hoặc hồi quy. Không mở test/data/locked. Python dùng `-B` và không ghi bytecode.

Tính thống kê cho **mọi service/kênh** trước, không chọn root/service theo nhãn. Ghi file đặc trưng chưa nối nhãn rồi mới đọc/nối root, fault, cell và vị trí để tạo `ca-sai.json`. Bước 1 đã dùng nhãn để chấm/chép số; file đó không được truyền vào hàm tính đặc trưng. Mốc t là thông tin hợp lệ của chế độ (a), không nghiên cứu chế độ tự phát hiện ở đây. Locator/mã mờ chỉ định danh và provenance, không dùng làm đặc trưng.

Nezha xử lý payload trên RAM; không lưu chuỗi giá trị, span, log, ID span, nội dung log hay danh sách cạnh. Chỉ ghi thống kê ca × service × kênh, số dòng/giới hạn thời gian, ánh xạ schema và manifest nguồn. Quan hệ gọi với root được rút trên RAM thành cờ/số đếm/khoảng cách theo service sau nối nhãn. Xác suất top-k theo service và số trùng cặp ca là thống kê tổng hợp, không là dữ liệu đo thô. Không cần tạo payload tạm.

Mỗi đặc trưng có `value`, `availability` và `reason`; giá trị thiếu dùng JSON null, biểu diễn N/A trong bảng. Các lý do: `unsupported`, `non_OK`, `missing_channel`, `insufficient_N`, `empty_A`, `ambiguous_mapping`, `nonfinite`, `intermediate_not_saved_requires_rerun`, `no_reference_in_N`, `invalid_ranking_invariant`, `no_eligible_pair`. Không gộp thiếu với 0. Service không có cạnh quan sát được là giá trị 0 khi graph dựng được; graph không dựng được là N/A. Kênh log có mặt nhưng không có dòng A của service là đếm 0 theo luật native; không đồng nghĩa thiếu kênh.

## 3. Cửa sổ, ánh xạ và thống kê tín hiệu

`N/A` trong công thức là normal/anomalous (bình thường/bất thường), còn N/A trong bảng giá trị là không áp dụng/không đủ dữ liệu. Các thống kê dưới đây là bằng chứng phân tích, không chạy lại bộ xếp hạng.

### 3.1 Cửa sổ đúng với đầu vào đã dùng

RE2-TT cắt metric `time∈[t−300,t+300)`, log `timestamp∈[t−300,t+300)`; span phải start≥t−300 và end<t+300. Không kéo dữ liệu ngoài cửa sổ vào bằng ffill. Tái dùng helper cắt/tiền xử lý thuần dữ liệu trong `src/p3/cua_so.py`, không gọi phương pháp. Giữ đơn vị gốc; thời gian span µs, metric/log giây. Nguồn: giao thức §5/§6; WHY-22.

| Phương pháp | Chia N/A và tiền xử lý của bằng chứng native |
|---|---|
| BARO | Metric theo time<t; nguồn khóa đã lưu sau bỏ `time.1`/latency-50, inf→NaN, ffill rồi 0 trên cửa sổ, đổi latency-90→latency và preprocess riêng N/A. Không fit lại RobustScaler; dùng khóa signed max robust-z đã lưu. |
| SimpleRCA | Metric thô bỏ time/time.1, chỉ lấy hữu hạn; N/A theo time. Span theo start<t; không gán span qua mốc vào A theo end. Log A theo timestamp≥t, message thiếu thành chuỗi rỗng. Không ffill metric. |
| MicroRank full | Span đã cắt outer; N=end<t, A=end≥t. Operation=serviceName+'_'+methodName sau fill methodName bằng operationName. Luật ID/operation và baseline của `src/microrank/__init__.py`; không gọi PageRank hoặc hàm xếp hạng. |
| TraceRCA | Outer và end-split như MicroRank; mapping operation như adapter. Không gọi TraceRCA để tính lại ji. Giữ ji hữu hạn/diagnostics đã lưu; thống kê span tính độc lập. |
| CIRCA OLS+RHT+DA | Graph native N có start≥t−300,end<t. Train metric 111 điểm [t−120,t−10], test 10 điểm cuối tới current (điểm thật cuối A), tiền xử lý theo adapter/giao thức §6.5. Chỉ đọc score RHT, khóa DA, parents/route đã lưu; không dựng lại nội suy hoặc fit hồi quy. |
| TORAI B | Giữ đúng nguồn B, 20 bin 15 s mỗi phía và tiền xử lý đã lưu theo giao thức §6.6/WHY-29. Dùng blocks, nhánh cluster và diagnostics từng seed đã lưu. Không dựng lại logts, GMM, RCD hoặc severity cần fit. |

Nezha: `doc_cua_so` lấy outer window Q-63; main guard=0. BARO nhận thứ tự 5N+5A từng nguồn với marker front_service, không giả các nguồn đồng thời; khóa đã lưu đã qua preprocessing. SimpleRCA nhận `metric_arrays.normal/anomalous` riêng từng kênh, không dùng marker chung để chia lại; trace chia start ns, log chia timestamp ns. MicroRank/TraceRCA chia end ns, kiểm membership ns→µs đúng wrapper. Giữ hàng lặp theo đầu vào phương pháp. CIRCA/TORAI UNSUPPORTED: không đo bằng chứng native hoặc suy root không có tín hiệu. Nguồn: WHY-37, Q-85, `src/p3/nezha.py`, `src/p3/adapters/nezha.py`.

Ánh xạ metric về service theo mapping đã dùng trong adapter/bản ghi, trace theo serviceName, log theo container_name/schema mapping bộ đọc. SimpleRCA native dùng tiền tố trước dấu `_` cuối; P3 ánh xạ item về entity theo `thuc_the_metric` và lấy key lớn nhất nếu nhiều native item về cùng entity (`src/p3/ban_ghi.py:7–37`). Vì vậy tính tổng phiếu ở native service trước, rồi max theo entity khi đối chiếu score P3; không cộng lại các native service chung entity. Không tự thêm alias theo tên gần giống; thiếu hoặc nhiều nghĩa ghi N/A.

### 3.2 Đặc trưng theo phương pháp

Ghi cho tất cả service, rồi trích service root sau nối nhãn. Các ngưỡng native đã quyết không phải ngưỡng tự chọn của P4; độ nhạy ngưỡng ghi N/A, dẫn WHY/giao thức tương ứng.

| Phương pháp | Số cần lưu và cờ `local_nonpositive` |
|---|---|
| BARO | Khóa từng metric/service trong ranking/entity_ranking; score service là max khóa metric. Cờ đúng khi service có khóa hữu hạn ≤0. Chỉ nói “không lệch tăng theo score BARO”; không nói không bất thường. Không áp 3σ cho robust-z. |
| SimpleRCA | Mỗi metric: nN,nA hữu hạn, số thiếu, μN,σN ddof=0, θ=μN+3σN, số A>θ (strict >), tổng events theo service. Metric khả dụng khi nN≥2,nA≥1. Trace: nN,nA, P95 tuyến tính, phiếu `P95A>3·P95N`, khả dụng khi mỗi phía≥1. Log: số dòng A, số dòng khớp regex ERROR\|FAIL\|EXCEPTION không phân biệt hoa/thường (mỗi dòng tối đa một phiếu đếm), phiếu count>0. Tổng điểm là events metric + phiếu trace + phiếu log; so với score đã lưu, không chạy diagnose. Cờ dùng score service đã lưu =0, ghi kèm số kênh thiếu và phiếu thành phần; nó nghĩa không nhận phiếu dương, không chứng minh các kênh thiếu bình thường. |
| MicroRank full | Mỗi operation: số span N/A, μN và σN ddof=1 trong ms, **làm tròn cả hai 2 chữ số thập phân trước so**; số span A có duration_ms≥μ_round+3σ_round. Giữ riêng số trace A được xếp bất thường (ít nhất một span đạt ngưỡng), số trace bất thường chứa operation, và số span bất thường của operation. Số span là tổng số hàng theo operation, **giữ hàng lặp cùng ID/nội dung** như native; kiểm ID xung đột là lỗi, không chọn một hàng. Chỉ số trace dùng tập traceID trong RAM để tránh đếm một trace qua nhiều operation. Cờ đúng khi service có span A, mọi operation A của service có baseline hữu hạn ≥2 span, và tổng span A vượt ngưỡng bằng 0. Thiếu baseline/std NaN ghi N/A, không điền 0. Điểm native operation/service lấy bản ghi; dấu lệch duration không thay thế PageRank/điểm MicroRank. |
| TraceRCA | Cùng luật span end-split, ddof=1, ms/round2/**≥**; lưu số span A và abnormal từng operation/service, tổng abnormal A, ji hữu hạn đã lưu. Cờ như MicroRank, nhưng không tự sửa std NaN mà code gốc biến so sánh thành False; thiếu nền vẫn ghi N/A cho bằng chứng. Nếu root bị lọc vì ji không hữu hạn, chỉ mô tả dữ kiện lọc đã lưu; không tính lại thứ hạng. |
| CIRCA | Mỗi metric: rht_score, regression_route, parents count, regression_error từ diagnostics.nodes; key DA đầy đủ `(score,−index,z-score)` lấy ranking. Cờ đúng khi có ít nhất một metric service với RHT hữu hạn và **mọi metric native của service đều có score hữu hạn ≤3**. Thiếu metric/score ghi N/A. Ngưỡng 3 là θ native; RHT≤3 không nói raw metric không lệch, cũng không thay khóa DA bằng RHT. Lưu dấu ca lỗi Q-82 từ cohort đã khóa, không tìm cohort mới. |
| TORAI B | Mỗi seed: số cluster, block chứa service, key cluster, vị trí nhóm trong block, nhánh `don`/`rcd`/`du_phong` từ extra.nhanh_khoi và diagnostics. Severity vector chỉ đọc nếu được lưu và ánh xạ được; thiếu thì N/A với lý do cần chạy lại trung gian. Không định nghĩa local_nonpositive từ cluster key/nhánh dự phòng; cờ đó N/A vì khác nghĩa score cục bộ. |

Nếu phép cộng SimpleRCA không khớp score đã lưu hoặc cửa sổ/input hash không khớp bản ghi, đây là sai triển khai cần sửa theo SPEC bước 5; không đổi công thức để ép khớp. Log là tổng đếm, không lưu nội dung. Các quan sát âm/giảm không được gọi là không có lỗi.

Luật trace ≥ cộng làm tròn có thể đánh dấu span không thay đổi khi σN bằng hoặc làm tròn về 0; native flag dương không tự chứng minh phân phối đã đổi. Luật cụ thể đối chiếu `src/simplerca/core.py:63–100`, `src/simplerca/adapter.py:45–84`, `src/microrank/__init__.py:42–60`, `results/T-015/tracerca-rcaeval.md:15–44` và `src/p3/adapters/nezha.py`.

### 3.3 Proxy độ lệch span để diễn giải quan hệ gọi

Đặc trưng raw riêng, không dùng thay luật native: với mỗi service, tính P95 duration N/A (quantile tuyến tính) và số span mỗi phía; `latency_up_τ = P95A > τ·P95N`. Chính τ=3, độ nhạy τ=2 và 4. Lý do: mốc chính cùng thang tỉ lệ 3 của SimpleRCA, hai mốc bao quanh kiểm phụ thuộc vào lựa chọn này; chưa kiểm P4, không chọn theo độ phân biệt ca đúng/sai. So tích trực tiếp, không chia 0; thiếu một phía hoặc duration không hữu hạn/âm ghi N/A. Đây là span-duration, không phải end-to-end latency.

Chia theo start cho SimpleRCA; end cho MicroRank/TraceRCA. BARO/CIRCA/TORAI dùng end như bối cảnh trace (không là tín hiệu native của BARO/TORAI). Không dùng proxy này trong primary; báo nó cùng root/caller để xét cách giải thích “triệu chứng ở phía gọi”. Báo các số và cờ ở cả ba τ cho mọi ca đủ dữ liệu. Cadence/clock Nezha làm liên hệ này yếu, không sửa đồng hồ hoặc giả nền sạch.

## 4. Quan hệ gọi từ N của chính ca

Dựng graph phân tích `G_N`, cạnh caller→callee từ parent-child cùng trace, chỉ khi cả span cha/con trong N. Dùng N-start cho SimpleRCA, N-end cho MicroRank/TraceRCA; CIRCA theo N native end<t. BARO/TORAI dùng N-end làm bối cảnh, ghi rõ phương pháp không nhận graph này. Outer theo §3.1.

Định danh `(traceID,spanID)`. Với graph phân tích, hàng trùng có cùng service,parent,start,duration chỉ lấy một; ID trùng khác nội dung bỏ toàn key xung đột cùng các cạnh trỏ tới nó, báo số xung đột. Thống kê tín hiệu vẫn giữ chính sách hàng lặp của đầu vào native. Thiếu parent là orphan, không đoán cha. Bỏ self-loop service khỏi cạnh reachability, giữ service trong tập nút. Không nối theo thứ tự thời gian hoặc nhãn. Ghi số span/nút/cạnh hữu hiệu, orphan, duplicate/conflict và số service cô lập. Thiếu trường/mapping hoặc không còn span N hợp lệ sau xử lý xung đột thì graph N/A.

Sau nối root, mỗi service ghi: indegree/outdegree quan sát, có cạnh trực tiếp đến root, có đường đi dương đến root, shortest distance nếu có. Không có đường là False khi graph khả dụng; không phải bằng chứng không có phụ thuộc thật. Không gọi graph phân tích này là graph native MicroRank/graph nhân quả CIRCA.

Service `e` chắc chắn đứng trước root khi cả hai trong R và:

- BARO/SimpleRCA/MicroRank/TraceRCA/CIRCA: full key entity của e lớn hơn root theo tuple native, đúng số đã lưu; hòa bằng nhau chính xác. CIRCA không chỉ so score đầu.
- TORAI: block e có key lớn hơn block root; hoặc cùng block và nhóm nội khối e đứng trước nhóm root. Khác block cùng key hoặc cùng nhóm không đạt điều kiện chắc chắn trước. Không suy từ thứ tự hiển thị hoặc cận hạng.

Ghi số/tên service thỏa, loại direct/ancestor và khoảng cách; dùng per-service aggregate cho Nezha. Đây là liên hệ quan sát giữa quan hệ gọi và ưu tiên thứ hạng, chưa là nhãn “lan”.

## 5. Nhãn cơ chế và thứ tự gán

Cờ cơ sở được tính cho cả ca đúng/sai. Nhãn cơ chế chỉ gán cho ca OK sai tại k đang xét. Mỗi cờ giữ True/False/N/A và bằng chứng. Không có bằng chứng không được đổi thành False. Non-OK giữ exception/status, không gán vào “chưa phân loại” của xếp hạng.

| Mã | Nhãn và tiêu chí | Mức kết luận; cách phản bác/giải thích khác |
|---|---|---|
| M1 | **Root ngoài O:** root∉sets.observed_entities của bản ghi. | Rào cản quan sát trực tiếp của pipeline. Có thể do coverage kênh, cửa sổ, mapping hoặc preprocessing; không chứng minh service không phát lỗi. |
| M2 | **Root trong O nhưng ngoài R:** root∈O, root∉entity_ranking/blocks. | Rào cản trả về trực tiếp. Đối chiếu item/key, NaN/filter và diagnostics; có thể do lọc điểm hoặc thiếu bằng chứng. Chỉ đặt tên bộ lọc cụ thể nếu nguồn đã xác nhận. |
| M3 | **Hòa cắt biên top-k:** 0<Hit@k<1 từ phân phối chính xác đã chấm **của từng bản ghi/seed**. Không dùng Hit trung bình các seed để phát hiện hòa; seed thắng/thua khác nhau không tự là hòa. | Phân rã trực tiếp bất định do hòa, không là nguyên nhân độc lập. Hòa hoàn toàn sau k không thuộc nhãn này. |
| M4 | **CIRCA thuộc ca lỗi làm tròn đã xác nhận:** ca nằm trong danh sách loại dev19 Q-82/WHY-36. | Lỗi số học đã xác nhận ở cấp ca; chưa xác nhận nó gây từng thất bại của root/DA. Không gán cho phương pháp khác, không chạy bản sửa để phân xử. |
| M5 | **Caller/ancestor được ưu tiên trên root:** có e≠root với đường e→root trong G_N và e chắc chắn đứng trước root theo §4. | Cơ chế ứng viên phù hợp nhầm phía gọi; có thể do workload, hướng gọi khác hướng lan, lỗi nhiều nơi, điểm native hoặc coverage. Proxy §3.3 là bối cảnh, không điều kiện đổi nhóm. |
| M6 | **Không có bằng chứng cục bộ dương theo luật đã khai:** root có cờ local_nonpositive=True theo §3.2. | Cơ chế ứng viên phụ thuộc tín hiệu/phương pháp. Thiếu kênh, tăng tải, lỗi hiện ở giảm tín hiệu hoặc nhãn/clock không khớp đều có thể giải thích. Không gán TORAI bằng severity chưa lưu. |
| M0 | **Chưa phân loại:** ca sai OK không có M1–M6 True. | Giữ toàn cờ thiếu/False và lý do; không tạo nhóm mới sau khi nhìn phân bố. |

Primary (nhãn chính để trình bày) theo thứ tự cố định **M1 → M2 → M3 → M4 → M5 → M6 → M0**: rào cản tập trước, bất định hòa, lỗi đã xác nhận, rồi dấu hiệu ứng viên. Báo đa nhãn tất cả M1–M6 True; tổng đa nhãn có thể lớn hơn số ca. Primary không là kết luận nguyên nhân trội hoặc chuỗi nhân quả. TORAI giữ cờ từng seed: nhãn case True nếu ít nhất một seed OK sai tại k có cờ True; báo `n_seed_true/n_seed_OK_wrong`, `n_seed_NA`, `all/partial`. Nếu không seed True mà có seed thiếu thì cờ tổng N/A; còn lại False. Hit ca trung bình đúng quy tắc T-024, mẫu số vẫn ca; không gán cờ seed đúng thành lời giải thích seed sai. Quy tắc OR chỉ áp M1–M6; sau gộp, ca M0 khi không có M1–M6 True. Giữ seed chưa phân loại riêng, không OR M0 lên ca đã có cơ chế khác.

Không có ngưỡng mới cho membership, key, hòa, status, cohort Q-82; độ nhạy N/A. M3 và việc chỉ gán trên ca sai phụ thuộc định nghĩa Hit: đối chứng đúng/sai của nhãn này mang tính cấu trúc, không phải bằng chứng nhân quả. M4 cũng báo nền trong cả nhóm ca đúng, không chỉ nhóm sai.

## 6. Phép đo chung về tập trung và biến thiên đầu ra

Dùng cùng một phép đo cho mọi phương pháp, k∈{1,5}. Với bản ghi i (một seed), O_i là tập quan sát thực, R_i là tập thực thể trả về duy nhất sau mapping (gồm service/component/DB), L_i=|R_i|, m_i=min(k,L_i). Từ `khoi_tu_ban_ghi` + `phan_bo_hang` trong `src/p3/danh_gia.py`, lần lượt truyền từng entity để lấy `p_i,k(e)=P(rank_i(e)≤k)`, không cần nhãn root. TORAI dùng hoán vị nguyên khối + hòa nội khối đúng giao thức §8.4; không uniform trên khoảng min–max.

Cho hai bản ghi độc lập i,j:

```
D_k(i,j) = 2 Σ_e p_i,k(e) p_j,k(e) / (m_i+m_j)
D0_k(i,j) = 2 m_i m_j |O_i∩O_j| / (|O_i| |O_j| (m_i+m_j))
ΔD = D−D0
V = 1−D
```

D là độ trùng top-k kỳ vọng (Dice overlap). D0 là đối chứng giải tích: mỗi bên hoán vị đều **đúng O của mình**, độc lập, lấy đúng L của đầu ra thật. Không thay O bằng U hoặc tập service toàn dataset, không Monte Carlo. Báo D,D0,ΔD,V, không đặt ngưỡng “cao/thấp”, không kiểm p-value.

Điều kiện: mỗi bản ghi OK, 0<L≤|O| và R⊆O, service không lặp; m>0. Không đạt thì cặp N/A kèm nguyên nhân, không tự mở rộng O hoặc điền D=0. Danh sách ngắn dùng m, không pad bằng service giả. Non-OK/UNSUPPORTED không có phép đo này; vẫn báo trạng thái và mẫu số riêng.

Giữa hai ca: phương pháp một seed có một cặp; TORAI lấy trung bình đều các tổ hợp seed hợp lệ (tối đa chín), báo số hợp lệ/tổng và trạng thái thiếu, không điền 0 cho tổ hợp lỗi. Mỗi cặp ca chỉ đóng góp một giá trị. Không so hai seed của cùng ca như hai ca khác nhau.

- **Khác ô:** mỗi cặp ô không thứ tự có giá trị trung bình các cặp ca hợp lệ của hai ô; sau đó trung bình đều các cặp ô có giá trị. Báo cả bảng cặp ô, số cặp ca/seed hợp lệ và số thiếu.
- **Cùng ô:** trung bình các cặp ca khác nhau không thứ tự trong từng ô; sau đó trung bình đều các ô đủ cặp. Không trộn cùng ô với khác ô.
- **Biến thiên seed trong một ca:** TORAI dùng cùng D trên ba cặp seed không thứ tự, báo D0/ΔD/V và cặp hợp lệ. Phương pháp một seed ghi N/A, không coi là biến thiên bằng 0.

Hai phân phối hòa giống nhau vẫn có thể D<1 vì hai lần phá hòa độc lập. Vì vậy V gồm bất định hòa, không gọi riêng là phương sai thuật toán. Báo thêm p theo service và L/O để giải thích. D hoặc ΔD lớn chỉ mô tả đầu ra lặp lại trong điều kiện tập ứng viên; chưa chứng minh thuật toán bỏ qua dữ liệu ca hoặc nhầm nguyên nhân.

## 7. Audit schema và các bảng báo cáo

Dùng nguyên `raw_column_audit` T-024; không đọc thêm schema test, không chạy L*. Báo union_n, số cột hiện/vắng và tên cột vắng theo ca; nhóm ô lấy nhãn dev. Loại cột theo suffix chính xác: cpu, mem, diskio, socket, workload, error, latency-50, latency-90; suffix khác giữ nhóm `other` cùng tên nguyên gốc, time/time.1 báo riêng. Nhóm service theo mapping native, không suy root từ cột vắng.

Với mỗi ô và mỗi cột trong union, đếm hiện/vắng trên số ca ô; báo cạnh O, R, số item/kênh sau preprocessing của từng phương pháp. Liên hệ schema với root chỉ là bảng chéo hiện/vắng × root/ô trên dev; không classifier, không hoán vị nhãn, không suy tác động schema đã tách khỏi loại lỗi/root. Schema raw chung không có nghĩa phương pháp nhận cùng tín hiệu. Các kênh bị drop hoặc thiếu trung gian native giữ nguồn và N/A.

Báo riêng mỗi dataset × phương pháp × k, tiếp tục tách cell, fault/nhom_loi, nhom_vi_tri_p75:

- Tổng ca, OK đúng/sai, non-OK từng trạng thái; mức trượt kỳ vọng không cộng lẫn số ca.
- Nhãn primary và đa nhãn: số ca nhãn/tổng OK sai, đồng thời số ca nhãn/tổng cohort để thấy coverage. Nếu mẫu số 0 ghi N/A.
- Cờ cơ sở từng cơ chế: số True/số đủ dữ liệu trong nhóm OK đúng và OK sai, cùng số False/N/A. TORAI cờ cơ sở trên mọi seed OK có quy tắc any/all/partial như §5, còn nhãn cho ca sai chỉ dùng seed sai. Ca đúng/sai có thiếu nhóm ghi N/A và không có đối chứng. Không chọn nhóm theo chênh tỉ lệ, không thử ngưỡng mới.
- τ=2/3/4 của proxy: số True/đủ dữ liệu và N/A từng nhóm; cờ proxy không thay primary. Báo rõ nhóm nào đổi cờ dưới các mốc, không tự thêm ngưỡng “đổi lớn”.
- Các cơ chế có thể thay thế, bằng chứng đã kiểm/chưa kiểm và phép can thiệp nào phân xử được nhưng ngoài phạm vi. Không gộp số RE2/Nezha thành một độ chính xác chung.

Hồ sơ đối chiếu tác giả: `results/T-013/ho-so-baro.md`, `results/T-017/ho-so-simplerca.md`, `results/T-015/ho-so-microrank.md`, `results/T-015/tracerca-rcaeval.md`, `results/T-014/ho-so-circa-kien-truc.md`, `results/T-016/ho-so-torai.md`, K1. Chỉ dẫn hạn chế tác giả thật sự nêu; không quy quan sát P4 cho tác giả. Không kết luận đồ thị có ích/không hoặc đặt nhãn lan chính thức. RE2 ít root/graph gần hằng; Nezha cadence, clock/nền sạch còn OPEN; không suy tính đại diện cho test.

## 8. Kiểm triển khai và đọc tay theo SPEC

Không thêm lượt phương pháp. Bước 3 tính lại độc lập một đặc trưng mỗi loại (membership/keys-hòa; thống kê metric; span/log; graph; schema; D/D0) trên ba ca đủ dữ liệu đầu tiên theo mã mờ tăng dần **trong mỗi dataset**, không chọn theo root/Hit/giá trị. Đối với loại chỉ có RE2, dùng ba ca RE2; loại không có dữ liệu ở dataset đó ghi N/A, không giả đủ kiểm. Với D dùng ba cặp không thứ tự từ ba ca đầu đủ đầu ra; kiểm công thức/đối chứng bằng mã riêng. Đối với seed, giữ cả seed đã có trên ba ca chọn. So trung gian/count và sai khác số học; không dùng tolerance để thay hòa hay membership. Sửa lỗi mã theo công thức đã duyệt, giữ lượt hỏng.

Bước 5: mỗi dataset × phương pháp × nhãn cơ chế × k có ca thì chọn hai mã mờ đầu theo thứ tự tăng dần (hoặc tất cả nếu ít hơn); M0≤10 lấy tất cả, M0>10 lấy mười mã đầu trong mỗi nhóm dataset × phương pháp × k. Gộp ca trùng để đọc một lần nhưng giữ các k/nhãn cần kiểm; TORAI đọc mọi seed liên quan. Đọc đối chiếu bản ghi, thống kê và phần cửa sổ dev cần thiết trên RAM; không chép payload Nezha. Ghi giá trị, nguồn và khớp/không khớp tiêu chí, không chỉ ghi “pass”. M0 không sinh tiêu chí mới.

## 9. Văn bản WHY-38 đề nghị ghi nguyên văn sau duyệt

Phạm vi xin duyệt riêng: **chỉ thêm mục dưới đây ở cuối `docs/WHY.md`**, giữ nguyên mọi mục cũ; không sửa DECISIONS, giao thức, MRP hoặc SPEC. Tiêu đề “Đã quyết” chỉ có hiệu lực sau khi Minh duyệt đúng văn bản/phạm vi này. Minh duyệt codebook đơn thuần không mặc nhiên duyệt ghi WHY. Chưa ghi WHY trong phiên này.

--- BEGIN WHY-38 ---

## WHY-38. Codebook phân tích hạn chế xếp hạng chế độ (a) — Đã quyết (Minh duyệt codebook T-028 và nội dung mục này)

- **Chọn:** dùng `results/T-028/codebook.md` chốt trước lượt tính bằng chứng P4. Bảng chính là RE2-TT dev30 và Nezha-OB main, sáu phương pháp với trạng thái giữ nguyên. Ca sai OK xét riêng Hit@1/Hit@5 kỳ vọng theo hòa; mức trượt kỳ vọng và non-OK báo riêng. CIRCA dev19 chỉ dòng có điều kiện Q-82; các view Nezha độ nhạy chỉ đánh dấu status/Hit đã có. Không chạy lại phương pháp.
- **Vì sao:** RQ2 và yêu cầu của cô cần chỉ ra ca nào, phương pháp nào, dấu hiệu cơ chế nào. Khóa tiêu chí trước bằng chứng mới hạn chế chọn ngưỡng theo kết quả dev, nhưng không xóa được việc người làm đã thấy bảng T-024/T-026. Tính cho cả ca đúng tạo đối chứng liên hệ; nhãn nối sau thống kê không cần nhãn. Thiếu kênh/trung gian không được biến thành không có lỗi.
- **Tiêu chí:** giữ đa nhãn và primary theo thứ tự root ngoài O → root trong O ngoài R → hòa cắt biên top-k → ca lỗi làm tròn CIRCA đã xác nhận → caller/ancestor N chắc đứng trước root → không có bằng chứng cục bộ dương theo luật từng phương pháp → chưa phân loại. Primary chỉ để trình bày. Rào cản tập/hòa/lỗi số học được phân biệt với cơ chế ứng viên chưa kiểm nhân quả. TORAI giữ cờ từng seed, gộp theo ca và công khai any/all/partial; ngưỡng native/hòa không đổi. Proxy span-duration riêng dùng P95A>τ·P95N, τ chính 3, độ nhạy 2 và 4, không dùng để đổi primary.
- **Phép đo đầu ra:** dùng cùng Dice overlap kỳ vọng top-1/top-5 trên phân phối hạng chính xác, kể cả hòa khối TORAI; đối chứng giải tích là hoán vị đều độc lập trên đúng O từng ca, giữ chiều dài trả về. Báo D, D0, D−D0 và 1−D theo cặp ca, cân đều cặp ô/cùng ô riêng; seed trong ca báo riêng. Non-OK/đầu ra vi phạm điều kiện ghi N/A. 1−D gồm bất định hòa; sự tập trung không chứng minh bỏ qua dữ liệu ca. Audit schema dùng raw_column_audit T-024, chỉ bảng chéo dev, không chạy L* hoặc đưa dấu vắng vào phương pháp.
- **Phương án đã xét:** phân phối đều trên cận hạng làm sai hòa khối TORAI; so top-k hiển thị bỏ qua hòa; đối chứng trên U thay O làm lẫn coverage với hành vi xếp hạng; áp một z-score/ngưỡng chung không phản ánh tín hiệu native; gán một nguyên nhân duy nhất che đa cơ chế; đổi tiêu chí theo độ phân biệt sai/đúng gây chọn theo kết quả. Không chọn các phương án này. Không chạy can thiệp hoặc thành phần phương pháp để điền trung gian thiếu vì ngoài SPEC T-028.
- **Bằng chứng thiết kế:** giao thức V2 T-022 §5–§8, WHY-22–33/36–37 và bản ghi/chấm T-024/T-026 quy định cửa sổ, mapping, hòa/seed, O/R và hạn chế dữ liệu. SPEC T-028 bước 2–6 quy định chốt trước bằng chứng, đối chứng và giới hạn nhân quả. Codebook dẫn code native và hồ sơ P1 tương ứng. Đây là căn cứ thiết kế; hiệu quả phân loại và các liên hệ P4 chưa kiểm tại thời điểm chốt.
- **Kết luận phụ thuộc:** mọi nhóm ca sai và số ca theo cơ chế của T-028; liên hệ với loại lỗi/vị trí/caller, tín hiệu, schema; mọi số tập trung/biến thiên đầu ra P4. Không áp cho phát hiện/chế độ (b), test, dataset khác, nhãn lan chính thức hoặc kết luận giá trị đồ thị. Clock/nền sạch, coverage và tính đại diện còn OPEN theo nguồn; can thiệp nhân quả ngoài phạm vi.

--- END WHY-38 ---

## 10. Điểm dừng hiện tại

Chưa tính đặc trưng, D/D0 hoặc gán M0–M6. Sau dòng giờ “chốt codebook” trong LOG, dừng để Minh duyệt codebook và **đúng văn bản/phạm vi WHY-38 tại §9**. Chỉ sang bước 3 khi đã ghi lời duyệt và WHY-38 vào nguồn chung. Phiên mới bước 3–6 theo ngoại lệ hai phiên của T-028; nếu lượt tính dự kiến >1 giờ phải báo trước và chờ Minh đồng ý.
