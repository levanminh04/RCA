# SimpleRCA — hồ sơ kỹ thuật M4 cho G1

Đã cài độc lập mô tả §3.1.2 và kiểm trên 30 ca dev RE2-TT được phép. Đây là **SimpleRCA (M4, quy ước T-017)**; bài không khóa đủ cấu hình để gọi bản này là chương trình sinh bảng 2. Mọi quy ước quan trọng dưới đây **(quy ước triển khai T017, xem docs/WHY.md WHY-17; chưa chốt P3)**. Không phải quyết định chọn baseline hoặc độ dài cửa sổ P3.

Nguồn chính: [PDF FSE26](https://yifanyang6.github.io/assets/pdf/papers/fang2026rethinking-fse.pdf), §3.1.2 trang 5; [arXiv v2](https://arxiv.org/pdf/2510.04711v2), trang 4. Đã đọc PDF đầy đủ và xem bảng 2/3 bằng ảnh; URL/hash/revision ở `sources/` và `inventory-files.csv`. Code tác giả đối chiếu ba revision T001, không dùng làm code bản cài.

## 1. Bài toán và đầu vào

SimpleRCA là heuristic (luật kinh nghiệm) xếp hạng service theo số cảnh báo metric, trace và log. Bài dùng nó để khảo sát dataset. Thuật toán không tự chứng minh nguyên nhân nhân quả, không học từ nhãn root, không cung cấp detector sự cố trực tuyến đã hiệu chỉnh.

Bản này nhận hai cửa sổ số đo normal và incident. Adapter biết trước mốc t từ metadata, chia `[t−300,t)` và `[t,t+300)`; lõi chỉ nhận các mảng đã chia. Đầu vào gồm metric time series (chuỗi thời gian), trace span duration theo service và thông điệp log theo service. Thiếu log vẫn chạy, nhưng không diễn giải phiếu log0 là đã quan sát không có lỗi. Service/entity quan sát ở một trong hai cửa sổ vẫn là ứng viên, kể cả chỉ có log normal; ERROR trong normal không tạo phiếu log. Adapter truyền riêng observed_services đã chuẩn hóa; DB giữ riêng khi chưa có alias kiến trúc. Danh sách ứng viên không suy từ nhãn bị tiêm.

Metadata thời gian phải đúng đơn vị, ba nguồn phải có service identity (định danh) khớp hoặc alias tường minh. Minimum normal2 finite/metric,1 span/phía chỉ là điều kiện tính toán; chưa chứng minh đủ mẫu để ước lượng normal ổn định. Lõi có thể dùng một modality còn đủ dữ liệu, nhưng không coi điểm partial-modality là ngang điều kiện với đủ ba nguồn. Adapter RCAEval `prepare` vẫn yêu cầu bảng `metrics.time` để chia cửa sổ; dữ liệu thuần log/trace ở hệ khác phải cung cấp maps đã chia cho lõi hoặc adapter tương ứng, không truyền None vào bảng metrics.

## 2. Từng bước và công thức

Gọi C là tập entity quan sát; J_s là các kênh metric của s; N_j và A_j là tập điểm hữu hạn normal/incident. Không ffill, không đọc thời điểm từ tên ca. Bỏ NaN/inf có đếm số bỏ; duration âm là lỗi. Alias gộp hai service metric, alias chain/cycle và cột trùng là lỗi đầu vào.

**Bước 1 — baseline metric.** Với n_j=|N_j|≥2:

\[
\mu_j=\frac1{n_j}\sum_{x\in N_j}x,\qquad
\sigma_j=\sqrt{\frac1{n_j}\sum_{x\in N_j}(x-\mu_j)^2},\qquad
\theta_j=\mu_j+3\sigma_j.
\]

Đếm cảnh báo từng giá trị: \(a_j=\sum_{x\in A_j}\mathbf1[x>\theta_j]\), rồi \(M_s=\sum_{j\in J_s}a_j\). Không trị tuyệt đối; giảm giá trị không phát cảnh báo upper-tail. Std0 không thêm epsilon. Nếu thiếu normal hoặc incident, kênh unavailable, không chế tạo baseline. Mean/std này nhạy ngoại lệ, dù bài dùng từ robust (bền vững) khi nêu threshold.

Biến thể P95 thay θ_j bằng Q_0.95(N_j); biến thể channels thay a_j bằng 1[a_j>0]. Hai cách đếm là lựa chọn khác nhau vì bài chưa định nghĩa tổng hợp qua thời gian. Events làm điểm tăng theo độ dài, tần suất và số kênh; score lớn có thể do triệu chứng kéo dài hoặc nhiều kênh tương quan, không chỉ do nguyên nhân mạnh.

**Bước 2 — trace.** Gộp span durations theo s trong mỗi cửa sổ, tính \(q_s^N=Q_{0.95}(D_s^N)\), \(q_s^A=Q_{0.95}(D_s^A)\). Phiếu \(T_s=\mathbf1[q_s^A>3q_s^N]\). Quantile tuyến tính: vị trí h=(n−1)p, nội suy hai phần tử đã sắp xếp cạnh h. Cả hai phía cùng đơn vị nên không cần đổi đơn vị vật lý. Gộp span theo service chưa được chứng minh tương đương end-to-end service latency khi có nhiều operation; đây là giới hạn diễn giải. Không dùng parentSpanId hoặc status để tính phiếu.

**Bước 3 — log.** \(e_s=\sum_{\ell\in L_s^A}\mathbf1[\ell\text{ chứa ERROR hoặc FAIL hoặc EXCEPTION}]\), không phân biệt hoa/thường, một count/dòng. \(L_s=\mathbf1[e_s>\lambda]\), mặc định λ=0. Bài nêu ngưỡng predefined nhưng không cho số; 0 là quy ước tối thiểu của task, chưa là spike detector (bộ phát hiện tăng đột ngột) đã hiệu chỉnh. Từ ghép như failure hoặc thông điệp lỗi nền cũng có thể khớp. Không cần normal log cho quy tắc fixed này.

**Bước 4 — fusion (gộp điểm) và ranking.** \(S_s=M_s+T_s+L_s\). Sắp score giảm dần; score bằng nhau trả tie group, tên lexical chỉ để hiển thị. Không có trọng số modality hoặc propagation. Tất cả điểm0 thì abstain (không có ứng viên có bằng chứng); mọi channel không đủ quan sát thì báo lỗi. Điểm dương là cảnh báo kinh nghiệm, không là kiểm định ý nghĩa nguyên nhân.

**Bước 5 — chấm riêng sau xếp hạng.** Ghi JSON diagnosis xong mới lấy root từ tên ca ở runner. Nếu root thuộc nhóm hòa kích thước m sau o ứng viên: Hit@k kỳ vọng =max(0,min(m,k−o))/m, MRR kỳ vọng =Σ_(r=o+1)^(o+m)(1/r)/m. Báo thêm optimistic/pessimistic. Nhãn không được phản hồi vào chọn cột/ngưỡng/window.

## 3. Đồ thị dùng ở đâu theo K1 §3

| Vai trò | Mô tả §3.1.2 và M4 T017 |
|---|---|
| Topology/triển khai | Không nhận đồ thị |
| Ngữ cảnh feature detector | Không dùng cạnh hay láng giềng |
| Đối tượng chấm bất thường | Không chấm graph; chấm từng kênh/service |
| Lan truyền điểm | Không lan truyền |
| Giả định causal/conditional | Không có causal graph |
| Xếp hạng nguyên nhân | Cộng cảnh báo rồi sắp score, không graph ranking |

Trace có provenance cấu trúc, nhưng M4 chỉ đọc serviceName/startTime/duration, không parent-child. Code CLI orig có nhánh dùng parent duration khi span ít; đó là thông tin cấu trúc còn lại của **code tác giả**, không hiện diện trong bản M4. Vì vậy không gán mọi chương trình mang tên SimpleRCA cùng phạm vi “không đồ thị”.

## 4. Tham số mặc định, file:dòng

| Tham số | Giá trị | Nơi thực hiện |
|---|---|---|
| Metric rule, σ | sigma,3 | `src/simplerca/core.py:14`; `src/simplerca/core.py:15` |
| Quantile metric/trace | 0,95; tuyến tính | `src/simplerca/core.py:16`; `src/simplerca/core.py:17`; `src/simplerca/core.py:81` |
| Trace factor | 3 | `src/simplerca/core.py:18` |
| Log threshold/keywords | 0; ERROR/FAIL/EXCEPTION | `src/simplerca/core.py:19`; `src/simplerca/core.py:22` |
| Metric aggregation | events | `src/simplerca/core.py:20` |
| Minimum normal metric | 2 finite | `src/simplerca/core.py:21` |
| Std denominator | ddof0 | `src/simplerca/core.py:67` |
| Window | half300s mỗi phía | `src/simplerca/adapter.py:30` |
| Alias | giữ tên mặc định, mapping tường minh | `src/simplerca/adapter.py:21` |
| Hòa/abstain | lexical hiển thị; tie group; allzero | `src/simplerca/core.py:103`; `src/simplerca/core.py:109` |

Tham số nháp WHY chưa duyệt không trở thành mặc định nghiên cứu chính thức. Cấu hình đầy đủ từng lượt ở JSON; environment ghim trong `requirements.lock`.

## 5. Chỗ code khác bài

Đối chiếu chi tiết và file:dòng ở `doi-chieu-code.md`; hash/revision ở manifests. Ba CLI mặc định đăng ký NezhaRCA. Orig dùng max metric so1,19P95 và ngưỡng tuyệt đối CPU/mem80, traceP90>100ms/top5, log ratio nonINFO/INFOdrop rồi cộng điểm theo hạng với weight metric1,2. Rcaeval thay metric bằng BARO RobustScaler/max z, traceP90 ratio1,2 và success-drop, log dựa level/has_error, combiner giới hạn theo top metric. RE3-SS còn đổi nhánh tiền xử lý và chọn cột; không chỉ một cờ. Lớp SimpleRCA riêng chưa đăng ký dùng6sigma/weight100/50/20 và DataAdapter đọc nhãn.

M4 ở đây làm theo công thức §2 thay các luật đó. Window, std denominator, unit đếm alert, log threshold, quantile interpolation, missing handling và tie đều là khoảng trống bài; lý do/phương án/ảnh hưởng có nháp WHY. Không xác nhận code sinh bảng2 chỉ từ tên class. Trùng số có thể là ngẫu nhiên hoặc khác protocol; lệch số có thể do code, telemetry, preprocessing, window, tie hoặc subset.

Đã kiểm license trước sử dụng: Git trees ba revision không có LICENSE/COPYING; không chép implementation vào src. Hai zip code Zenodo17105974 và artifact FSE mới được kiểm riêng license/inventory. Snapshot chỉ dùng đối chiếu, bản cài tự viết. Artifact FSE mới có code giống orig nhưng kết quả từng ca đã lọc không có dev RE2-TT.

## 6. Giả định và điều kiện thất bại tác giả nêu

Bài §3.1.2 giả định các triệu chứng đủ lớn để vượt luật đơn giản, normal trước sự cố dùng làm baseline, và service nhiều cảnh báo là ứng viên root. Đây là heuristic, không có chứng minh causal.

Trong §3.2.3 FSE trang8–9, tác giả mô tả TypeI chỉ root có triệu chứng rõ, TypeII triệu chứng không rõ gây khó chẩn đoán. §6.2.3 trang17 nói thiết kế threshold-count hiệu quả với tín hiệu rõ, cục bộ nhưng kém với lỗi mạng/tinh tế khi root không là thành phần ồn nhất. Đây là kết luận tác giả trên benchmark mới, không phải phép kiểm P4 của T017. §6.2.4 trang18–19 bàn các thất bại do telemetry thiếu/không đầy đủ, mô hình hóa và chi phí; không suy rằng tất cả lỗi của các model áp cho SimpleRCA. ArXivv2 §3.1.2 có câu nói các luật basic và công cụ đánh giá dataset, không định vị RCA thực dụng; hai câu này đã bỏ trong bản FSE. Không trình bày chúng thành nguyên văn FSE.

Những vấn đề **task tự kiểm** phải tách khỏi lời tác giả: hai normal-control thực vẫn phát điểm dương; thiếu log; đếm events ưu tiên persistent/many-channel symptoms. Đây là kiểm đúng đắn trong P1, không phải phân tích hạn chế toàn dataset P4. Giả thuyết nguyên nhân khác của false alerts: normal biến động hoặc drift, std thấp, tương quan chuỗi, số kênh lớn, hoặc cửa sổ nominal normal có sự cố chưa ghi nhận. Task không phân xử các giả thuyết đó và không chỉnh ngưỡng theo nhãn.

## 7. Ví dụ tính tay

Ca chọn bằng thứ tự từ điển allowlist **trước kết quả**: re2tt_ts-auth-service_cpu_1. Không có log. Tính độc lập cả 369 metric và 68 entity (gồm DB giữ riêng); 2226 mục so đều đạt, counts/scores/ranks bằng tuyệt đối, floats tolerance1e−10 tương đối/tuyệt đối. Chi tiết số, từng bước và lý do root đứng hạng1 ở `vi-du-tinh-tay.md`, `vi-du-metric.csv`, `vi-du-score.csv`, `runs/example-comparison-v2.json`. Không dùng nhãn để chọn kênh CPU.

## 8. Đường nhãn có thể lọt vào

| Đường | Xử lý T017 và giới hạn |
|---|---|
| Tên ca/path chứa root/fault | Runner chỉ cho phép để chọn nguồn allowlist và đánh giá sau ghi diagnosis; không truyền vào lõi |
| Inject time | Adapter dùng để chia window chế độ biết mốc; không được gọi đây là tự phát hiện |
| Fault_info/labels của author adapter | Không import hoặc gọi; lớp riêng có đường đọc, CLI orig dùng adapter khác |
| Chọn SLI/kênh theo root/fault | Không làm; giữ mọi kênh hợp lệ |
| Alias theo đáp án | Alias chỉ từ schema/kiến trúc; dev không dùng alias suy đoán |
| Type labels | Không tính Type hoặc dùng Type làm feature/candidate |
| Chọn cấu hình theo Hit@1 | Khóa trước dev, sensitivity giữ riêng, không chọn winner |

Tên service trong telemetry cần cho đơn vị xếp hạng; điều này không đồng nghĩa được truyền tên ca có ground truth. Nhãn evaluation vẫn cần để đo đúng/sai, nhưng không quay ngược vào diagnosis.

## 9. Yêu cầu trên dataset khác và dữ kiện G1

CSV `yeu-cau-dau-vao.csv` ghi primary, biến thể và từng bộ cảnh báo, đúng16cột Minh yêu cầu. Dataset khác cần: baseline normal, incident interval từ bên ngoài; timestamp đúng đơn vị và đồng bộ; numeric channels gắn entity; trace durations cùng đơn vị và định danh service; log message và định danh service; alias kiến trúc nếu tên khác. Nếu không có modality, báo thiếu và giữ condition chạy riêng. Service không quan sát không được thêm từ nhãn. Cần thống nhất đơn vị entity/application service và mapping DB trước so sánh cross-method, không tự gộp tên.

Không cần đồ thị, train labels hoặc GPU; không có fit model. Chi phí thuật toán gồm scan metric/log, quantile theo service và sort ranking; phụ thuộc số mẫu/cột/spans/logs, thời gian I/O. Chưa đo cost chính thức vì laptop chạy nhiều phiên. Không ngoại suy elapsed sang dataset khác.

Điểm dev: Hit@1=0.833333 (25/30), Hit@3/5=0.966667, MRR=0.891111, nguồn `runs/final-summary.json` và `diem-dev.csv`. Bảng2 công bố RE2-TT0,80 trên90ca (`so-cong-bo.csv`). **Chưa tái lập số công bố**:60ca bị khóa, không có kết quả tác giả cho30dev ở nguồn đã kiểm, code/config sinh bảng chưa xác định. Không lấy chênh số làm bằng chứng tốt hơn hay tái lập thành công.

Luật TypeI/II và tỷ lệ nguyên PDF nằm riêng `type-i-ii.md`/`ty-le-type-cong-bo.csv`. Nó cần nhãn injection/root và còn OPEN về threshold/aggregation; không phải output SimpleRCA, không tự tính trên dataset mới.

## Cập nhật N1/N2 — 04/10/2026

Minh đã duyệt sửa. Runner và bộ lọc artifact dùng manifest 30 ca cố định; runner kiểm exact-set và danh tính resolve trước tạo run/đọc nguồn. `prepare` trả NamedTuple PreparedInputs: normal_metrics, incident_metrics, normal_traces, incident_traces, incident_logs, metric_services, observed_services. Metadata ví dụ normalized giữ observed_services, không có message log normal. Cửa sổ đếm log lỗi vẫn chỉ incident; service chỉ normal có score0.

Run-dev-005 khớp 30 diagnosis và toàn bộ output phụ với run004; điểm công bố trong hồ sơ không đổi. Kiểm mới 25 unittest/13 self-test/2.458 so ví dụ có chứng cứ tại `runs/fix-n1n2-001/verification.json` và `kiem-dung-dan.md`. File kết quả và inventory cũ giữ làm snapshot bàn giao; không gọi đây là tái lập full90 hoặc detector đã hiệu chỉnh.
