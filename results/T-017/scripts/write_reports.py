"""Build explanatory tables and reports from preserved outputs, never labels for diagnosis."""
import csv,json,re,shutil
from pathlib import Path
O=Path('D:/RCA-flashticket/results/T-017');R=Path('D:/RCA-flashticket');W=Path('D:/RCA-ext/work/T-017')
s=json.loads((O/'runs/final-summary.json').read_text())
result=json.loads((O/'runs/run-dev-004/re2tt_ts-auth-service_cpu_1.json').read_text())
comparison=json.loads((O/'runs/example-comparison-v2.json').read_text())
supp=json.loads((O/'runs/supplement-001/summary.json').read_text())
def write(name,text): (O/name).write_text(text.strip()+'\n',encoding='utf-8')
def line(file,needle):
    return next(i for i,x in enumerate((R/file).read_text().splitlines(),1) if needle in x)
def loc(file,needle):return f'`{file}:{line(file,needle)}`'
core='src/simplerca/core.py';adapter='src/simplerca/adapter.py'
write('ho-so-simplerca.md',fr'''
# SimpleRCA — hồ sơ kỹ thuật M4 cho G1

Đã cài độc lập mô tả §3.1.2 và kiểm trên {s['cases']} ca dev RE2-TT được phép. Đây là **SimpleRCA (M4, quy ước T-017)**; bài không khóa đủ cấu hình để gọi bản này là chương trình sinh bảng 2. Mọi quy ước quan trọng dưới đây **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**. Không phải quyết định chọn baseline hoặc độ dài cửa sổ P3.

Nguồn chính: [PDF FSE26](https://yifanyang6.github.io/assets/pdf/papers/fang2026rethinking-fse.pdf), §3.1.2 trang 5; [arXiv v2](https://arxiv.org/pdf/2510.04711v2), trang 4. Đã đọc PDF đầy đủ và xem bảng 2/3 bằng ảnh; URL/hash/revision ở `sources/` và `inventory-files.csv`. Code tác giả đối chiếu ba revision T001, không dùng làm code bản cài.

## 1. Bài toán và đầu vào

SimpleRCA là heuristic (luật kinh nghiệm) xếp hạng service theo số cảnh báo metric, trace và log. Bài dùng nó để khảo sát dataset. Thuật toán không tự chứng minh nguyên nhân nhân quả, không học từ nhãn root, không cung cấp detector sự cố trực tuyến đã hiệu chỉnh.

Bản này nhận hai cửa sổ số đo normal và incident. Adapter biết trước mốc t từ metadata, chia `[t−300,t)` và `[t,t+300)`; lõi chỉ nhận các mảng đã chia. Đầu vào gồm metric time series (chuỗi thời gian), trace span duration theo service và thông điệp log theo service. Thiếu log vẫn chạy, nhưng không diễn giải phiếu log0 là đã quan sát không có lỗi. Service/entity chỉ xuất hiện trong một modality vẫn là ứng viên; DB giữ riêng khi chưa có alias kiến trúc. Danh sách ứng viên không suy từ nhãn bị tiêm.

Metadata thời gian phải đúng đơn vị, ba nguồn phải có service identity (định danh) khớp hoặc alias tường minh. Minimum normal2 finite/metric,1 span/phía chỉ là điều kiện tính toán; chưa chứng minh đủ mẫu để ước lượng normal ổn định. Lõi có thể dùng một modality còn đủ dữ liệu, nhưng không coi điểm partial-modality là ngang điều kiện với đủ ba nguồn. Adapter RCAEval `prepare` vẫn yêu cầu bảng `metrics.time` để chia cửa sổ; dữ liệu thuần log/trace ở hệ khác phải cung cấp maps đã chia cho lõi hoặc adapter tương ứng, không truyền None vào bảng metrics.

## 2. Từng bước và công thức

Gọi C là tập entity quan sát; J_s là các kênh metric của s; N_j và A_j là tập điểm hữu hạn normal/incident. Không ffill, không đọc thời điểm từ tên ca. Bỏ NaN/inf có đếm số bỏ; duration âm là lỗi. Alias gộp hai service metric, alias chain/cycle và cột trùng là lỗi đầu vào.

**Bước 1 — baseline metric.** Với n_j=|N_j|≥2:

\[
\mu_j=\frac1{{n_j}}\sum_{{x\in N_j}}x,\qquad
\sigma_j=\sqrt{{\frac1{{n_j}}\sum_{{x\in N_j}}(x-\mu_j)^2}},\qquad
\theta_j=\mu_j+3\sigma_j.
\]

Đếm cảnh báo từng giá trị: \(a_j=\sum_{{x\in A_j}}\mathbf1[x>\theta_j]\), rồi \(M_s=\sum_{{j\in J_s}}a_j\). Không trị tuyệt đối; giảm giá trị không phát cảnh báo upper-tail. Std0 không thêm epsilon. Nếu thiếu normal hoặc incident, kênh unavailable, không chế tạo baseline. Mean/std này nhạy ngoại lệ, dù bài dùng từ robust (bền vững) khi nêu threshold.

Biến thể P95 thay θ_j bằng Q_0.95(N_j); biến thể channels thay a_j bằng 1[a_j>0]. Hai cách đếm là lựa chọn khác nhau vì bài chưa định nghĩa tổng hợp qua thời gian. Events làm điểm tăng theo độ dài, tần suất và số kênh; score lớn có thể do triệu chứng kéo dài hoặc nhiều kênh tương quan, không chỉ do nguyên nhân mạnh.

**Bước 2 — trace.** Gộp span durations theo s trong mỗi cửa sổ, tính \(q_s^N=Q_{{0.95}}(D_s^N)\), \(q_s^A=Q_{{0.95}}(D_s^A)\). Phiếu \(T_s=\mathbf1[q_s^A>3q_s^N]\). Quantile tuyến tính: vị trí h=(n−1)p, nội suy hai phần tử đã sắp xếp cạnh h. Cả hai phía cùng đơn vị nên không cần đổi đơn vị vật lý. Gộp span theo service chưa được chứng minh tương đương end-to-end service latency khi có nhiều operation; đây là giới hạn diễn giải. Không dùng parentSpanId hoặc status để tính phiếu.

**Bước 3 — log.** \(e_s=\sum_{{\ell\in L_s^A}}\mathbf1[\ell\text{{ chứa ERROR hoặc FAIL hoặc EXCEPTION}}]\), không phân biệt hoa/thường, một count/dòng. \(L_s=\mathbf1[e_s>\lambda]\), mặc định λ=0. Bài nêu ngưỡng predefined nhưng không cho số; 0 là quy ước tối thiểu của task, chưa là spike detector (bộ phát hiện tăng đột ngột) đã hiệu chỉnh. Từ ghép như failure hoặc thông điệp lỗi nền cũng có thể khớp. Không cần normal log cho quy tắc fixed này.

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
| Metric rule, σ | sigma,3 | {loc(core,"metric_rule: str")}; {loc(core,"sigma: float")} |
| Quantile metric/trace | 0,95; tuyến tính | {loc(core,"metric_quantile: float")}; {loc(core,"trace_quantile: float")}; {loc(core,"qn=float")} |
| Trace factor | 3 | {loc(core,"trace_factor: float")} |
| Log threshold/keywords | 0; ERROR/FAIL/EXCEPTION | {loc(core,"log_threshold: int")}; {loc(core,"keywords: tuple")} |
| Metric aggregation | events | {loc(core,"metric_aggregation: str")} |
| Minimum normal metric | 2 finite | {loc(core,"min_normal_metric: int")} |
| Std denominator | ddof0 | {loc(core,"std(ddof=0)")} |
| Window | half300s mỗi phía | {loc(adapter,"def prepare")} |
| Alias | giữ tên mặc định, mapping tường minh | {loc(adapter,"def canonical_service")} |
| Hòa/abstain | lexical hiển thị; tie group; allzero | {loc(core,"ranks=sorted")}; {loc(core,"status='abstain'")} |

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

Ca chọn bằng thứ tự từ điển allowlist **trước kết quả**: re2tt_ts-auth-service_cpu_1. Không có log. Tính độc lập cả {s['example_metrics']} metric và {s['example_services']} entity (gồm DB giữ riêng); {comparison['checks']} mục so đều đạt, counts/scores/ranks bằng tuyệt đối, floats tolerance1e−10 tương đối/tuyệt đối. Chi tiết số, từng bước và lý do root đứng hạng1 ở `vi-du-tinh-tay.md`, `vi-du-metric.csv`, `vi-du-score.csv`, `runs/example-comparison-v2.json`. Không dùng nhãn để chọn kênh CPU.

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

Điểm dev: Hit@1={s['hit1_fractional']:.6f} ({s['hit1_sum']:g}/{s['cases']}), Hit@3/5={s['hit3_fractional']:.6f}, MRR={s['mrr_fractional']:.6f}, nguồn `runs/final-summary.json` và `diem-dev.csv`. Bảng2 công bố RE2-TT0,80 trên90ca (`so-cong-bo.csv`). **Chưa tái lập số công bố**:60ca bị khóa, không có kết quả tác giả cho30dev ở nguồn đã kiểm, code/config sinh bảng chưa xác định. Không lấy chênh số làm bằng chứng tốt hơn hay tái lập thành công.

Luật TypeI/II và tỷ lệ nguyên PDF nằm riêng `type-i-ii.md`/`ty-le-type-cong-bo.csv`. Nó cần nhãn injection/root và còn OPEN về threshold/aggregation; không phải output SimpleRCA, không tự tính trên dataset mới.
''')
metric_rows=list(csv.DictReader((O/'vi-du-metric.csv').open()))
table='\n'.join('| '+ ' | '.join([x['metric'].removeprefix('ts-auth-service_'),f"{float(x['mean']):.9g}",f"{float(x['std0']):.9g}",f"{float(x['threshold']):.9g}",x['normal_finite'],x['incident_finite'],x['alert_count']])+' |' for x in metric_rows)
tr=result['traces']['ts-auth-service']
scores=list(csv.DictReader((O/'vi-du-score.csv').open()))
top='\n'.join(f"| {x['thu_tu_hien_thi']} | {x['service']} | {x['metric']} | {x['trace']} | {x['log']} | {x['score']} |" for x in scores[:8])
sens=json.loads((O/'runs/run-dev-004/sensitivity.json').read_text())
sens_table='\n'.join(f"| {x['name']} | {x['scores']['ts-auth-service']['score']} | {x['scores']['ts-auth-service']['metric']} | {x['scores']['ts-auth-service']['trace']} | {x['scores']['ts-auth-service']['log']} |" for x in sens)
write('vi-du-tinh-tay.md',fr'''
# Ví dụ tính tay và tính độc lập

Ca chọn trước khi xem kết quả bằng rule SPEC: tên đầu thứ tự từ điển trong allowlist30dev, **re2tt_ts-auth-service_cpu_1**. Metadata/mốc và hash nguồn ở run004 summary, `sources/injection-manifest.json`; normalized inputs tại `D:/RCA-ext/work/T-017/example-input-run-dev-004/`. Bản normalized cũ được giữ riêng. Quy ước M4 **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**.

## 1. Chia cửa sổ và tính mọi ứng viên

Adapter chia normal[t−300,t), incident[t,t+300), không dùng root để chọn cột. Tính {s['example_metrics']} kênh của {s['example_services']} entity, gồm DB chưa gộp. Script `scripts/independent_example.py` đọc normalized CSV, tự viết mean/std/count/percentile/fusion/tie, **không import hoặc gọi lõi/adapter chính**. 12 nhóm self-test known-answer độc lập kiểm trước phép so. Phép so này kiểm score engine, không tự chứng minh adapter raw→CSV; schema/boundary/alias có kiểm riêng.

## 2. Các phép tính metric

Để người đọc thấy phép cộng, bảng dưới chỉ trình bày một entity; phần tính độc lập trước đó đã làm mọi entity. Nhãn root chỉ dùng sau khi JSON thứ hạng đã được ghi. Mỗi θ=μ+3σ, mỗi điểm x>θ được1 cảnh báo; equality không tính. Bảng làm tròn để đọc, số fullprecision ở `vi-du-metric.csv`.

| Kênh | μ | σ(ddof0) | θ | Normal finite | Incident finite | Count vượt θ |
|---|---:|---:|---:|---:|---:|---:|
{table}

Ví dụ CPU: θ={result['metrics']['ts-auth-service_cpu']['mean']:.9f}+3×{result['metrics']['ts-auth-service_cpu']['std']:.9f}={result['metrics']['ts-auth-service_cpu']['threshold']:.9f}; đếm {result['metrics']['ts-auth-service_cpu']['count']} điểm trên ngưỡng. CPU/diskio có3 điểm incident thiếu; không ffill và không coi thiếu là0. Tổng metric = {'+'.join(x['alert_count'] for x in metric_rows)}={s['example_root_score']['metric']}. Không lọc latency/mem/socket dù tên ca nói CPU.

## 3. Trace, log và điểm cuối

Trace entity này có {tr['n_normal']} span normal, {tr['n_incident']} incident. P95normal={tr['p95_normal']:g}, P95incident={tr['p95_incident']:g}, threshold3×normal={tr['threshold']:g}. P95incident<threshold nên phiếu trace0. Đơn vị vật lý OPEN; so cùng nguồn không cần đổi đơn vị. Đây là gộp span durations theo entity, chưa chứng minh service-latency end-to-end.

Ca không có logs.parquet. Log status=unavailable, đóng góp0 để cộng phần còn quan sát; không khẳng định error count0. Điểm cuối S={s['example_root_score']['metric']}+0+0={s['example_root_score']['score']}.

| Hạng hiển thị | Entity | Metric | Trace | Log đóng góp | Score |
|---|---|---:|---:|---:|---:|
{top}

Nguồn mọi ô: `vi-du-score.csv`, JSON diagnosis run004 và `runs/independent-example-v2.json`. Sau khi ranking cố định, evaluator đọc root=ts-auth-service: root đứng1 vì score1440 cao nhất, không có hòa ở đầu. Đây là giải thích **cơ chế xếp hạng**, không chứng minh CPU hay service này là nguyên nhân bằng causal inference. Các nguyên nhân khác của điểm cao gồm mức tiêm mạnh, persistence, nhiều kênh tương quan và baseline ít biến động; task chưa phân xử chúng.

## 4. Khớp độc lập và biến thể đã khóa

`runs/example-comparison-v2.json`: {comparison['checks']} so sánh đạt; count/score/ranking bằng tuyệt đối. Float dùng tolerance1e−10 tương đối hoặc tuyệt đối, max absolute error={comparison['max_absolute_float_error']:.12g}; không nói mọi absolute error nhỏ hơn1e−10. Sai khác làm tròn thống kê không đổi count/vote/score.

| Biến thể | Score entity ví dụ | Metric | Trace | Log |
|---|---:|---:|---:|---:|
{sens_table}

Nguồn `runs/run-dev-004/sensitivity.json`; không chọn winner theo accuracy. Ngưỡng log1/10 trên ca thiếu log không phân xử được log rule. Vì vậy kiểm thêm ca thứ hai có log, rule chọn cũng theo allowlist: {supp['case']}. Ngưỡng0/1/10 đều có một entity nhận phiếu log, score/ranking không đổi; keyword count được tính lại độc lập bằng substring ba từ rồi so từng entity (`runs/supplement-001/summary.json`). Không ngoại suy ổn định này cho ca/dataset khác.
''')
normal_table='\n'.join(f"| {x['case']} | {x['max_score']} | {x['positive_services']} | Không đạt |" for x in s['normal_controls'])
write('kiem-dung-dan.md',fr'''
# Kiểm đúng đắn — T017

Các phép kiểm xác nhận từng điều kiện cụ thể, không đồng nhất “không lỗi” với “chạy đúng”. Mọi số cuối lấy run-dev-004 (`runs/final-summary.json`);001–003 giữ nguyên lịch sử và không dùng làm số cuối. Quy ước M4 **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**.

## Kiểm đạt

| Phép kiểm | Kết quả và bằng chứng |
|---|---|
| Known-answer tổng hợp |16 unittest đạt; metric2+trace1+log1=4, strict threshold, missing/empty, tie, absent entity, std0, alias collision/cycle, boundary/units, negative duration |
| Script độc lập |12 nhóm self-test đạt;2226 mục so ví dụ đạt, mọi count/score/rank bằng tuyệt đối (`example-comparison-v2.json`) |
| Lặp lại |Hai ca đầu allowlist, JSON bằng tuyệt đối (run004 summary/repeat) |
| Đảo thứ tự cột |Hai ca đầu, output/tie groups bằng tuyệt đối; tổng hợp cũng đạt |
| Không fallback/không rỗng/tổng điểm |30/30 đạt;0 ranking trùng thứ tự entity từ cột metric; không dùng fallback (`final-summary.json`) |
| Hòa |Giữ tie group, fractional Hit và bounds; lexical chỉ display (test_ties_and_unobserved) |
| Missing log |cpu_1 unavailable, giữ ca; synthetic phân biệt None và bảng rỗng |
| Input guard |30ca/89file resolve đúng nguồn;2ca ngoài guard và file resolve ra ngoài bị chặn trước đọc (`supplement-001/guard-check.json`). File escape tổng hợp dùng mock resolve, không tạo symlink thật; các file thật không trỏ ngoài |
| Alias |Giữ tên DB, alias trace/log tường minh về metric hoạt động; collision metric/cycle/cột trùng lỗi; ca thứ hai baseline sau guard changes bằng run004 |
| Log sensitivity thực |Ngưỡng0/1/10 có1entity nhận phiếu, độc lập count từng entity đạt; không chọn cấu hình (`supplement-001`) |
| Provenance |30mốc metadata hash khớp manifest T002,70Git blob khớp, PDF bảng2/3 xem ảnh; số công bố tra trước dev |

Metric name parser tách underscore cuối theo schema RCAEval; chưa hỗ trợ suffix metric có underscore tùy ý. Trace và log timestamp range guards kiểm đúng đơn vị. Duration vật lý chưa xác nhận nhưng ratio cùng nguồn không cần đổi. Kiểm guard và alias sau run004 không làm đổi computation với aliases=None; baseline ca thứ hai xác nhận điều đó.

## Normal/normal: kết quả không đạt abstention trên dữ liệu thực

Synthetic hai cửa sổ constant bình thường trả abstain đúng. Hai ca thực dùng normal[t−450,t−300) và normal[t−300,t−150), hoàn toàn trước mốc inject đã biết, vẫn trả heuristic_alerts:

| Ca | Score lớn nhất | Entity điểm dương | Abstention |
|---|---:|---:|---|
{normal_table}

Nguồn `runs/run-dev-004/*-normal-control.json` và `final-summary.json`. Đây là phép kiểm đã làm và không đạt; không ghi “chưa kiểm”, không điều chỉnh threshold để làm đẹp. Điểm dương không được gọi là tìm ra nguyên nhân có ý nghĩa trong hai cửa sổ này. Các nguyên nhân khả thi khác: baseline/window khác phân bố, std thấp, drift, tương quan thời gian, nhiều phép vượt ngưỡng, hoặc nominal normal có bất thường chưa có nhãn. Không phân tích định lượng toàn dataset (P4) trong task này.

## Tái lập và số công bố

Bảng2 nguyên số ở `so-cong-bo.csv` tra trước chạy. RE2-TT công bố Top1=0,80 trên90ca. Bản M4 này trên30dev có Hit1={s['hit1_fractional']:.6f}, Hit3/5={s['hit3_fractional']:.6f}, MRR={s['mrr_fractional']:.6f}; mỗi ca/bounds có `diem-dev.csv`. Không gọi đây là tái lập trọn hoặc bằng chứng vượt tác giả.60ca đang khóa, source artifact được kiểm không cung cấp output30dev, code/config/window/tie sinh bảng2 chưa xác định. So paper vs dev trực tiếp trộn denominator/protocol/implementation.

Zenodo17105974: hai zip code có inventory/license/hash, không telemetry mới. FSE artifact mới dùng lại từ T012: code21file giống orig; hai parquet kết quả áp predicate allowlist trước đọc/trả giá trị,0devrows. Đã làm kiểm được phép; không ghi “chờ quyền” để bỏ lọc kết quả (`doi-chieu-code.md` §8).

Table3 có mâu thuẫn Eadro-SN I+II hiển thị0,94 nhưng cộtI&II0,96; giữ cả hai theo PDF, chưa tự sửa hoặc tính Type trên dữ liệu mới. Chi tiết `type-i-ii.md`.

## Lượt hỏng, sửa lỗi và thời gian

run001 ca thứ hai thiếu metadata nguồn dự kiến; run002 thiếu local metadata. Lấy30file mốc đúng nguồn/hash đã ghi T002 (tổng300byte), giữ failed JSON/progress. So trung gian phát regex pod làm gộp DB thànhts; bỏ suy đoán tên, thêm regression test, chạy lại30 ở004 lý do(c). Không đổi ngưỡng theo kết quả. Cột registry được dựng lại từ từng run/check, giữ registry thô lịch sử.

Mọi lượt có progress và elapsed ngay từ đầu. Laptop đang chạy nhiều phiên nên không số thời gian chính thức, không so5,99s của tác giả. Môi trường ghi phiên bản phụ đầy đủ; lệnh dựng tại `moi-truong.md`. Không EC2, không lượt>1giờ, không tải dataset mới.

## Chưa kiểm thật sự và hệ quả

| Việc | Lý do | Giả định và khi sai | Cách kiểm/đầu vào cần |
|---|---|---|---|
| Tái lập90RE2-TT |60khóa và chưa có đúngcode/config |Không giả định30 đại diện90; sai nếu chọn dev thiên lệch |ChốtG1, quyềnG3 và chương trình/outputs tác giả |
| So từng ca tác giả |Predicate ở nguồn đã có trả0devrow |Nguồn khác có thể có outputs chưa thấy |Tác giả cung cấp đúng30dev, lọc trước đọc |
| Type exact executable |Bài thiếu rule aggregation/threshold/“stronger” |Không mặc địnhví dụ2× là cấu hình dùng mọi dataset |Code/count/config gốc; không tự tính dataset mới |
| Cost chính thức/quy mô khác |8phiên cùng máy; P3 không thuộc task |Elapsed này không đại diện chạy đơn hoặc hệ lớn hơn |Máy rảnh, protocol G1/P3; không EC2 tại T017 |
| Đơn vị duration, service-latency semantic |Schema chỉ biết cùng nguồn; không đủ physical documentation |Nếu normal/incident khác đơn vị hoặc operation mix thay thì ratio sai nghĩa |Metadata rawcollector; đếm ratio không giải quyết latency semantics |
| Tổng quát hóa failure mechanisms |P4/giao thức dataset chưa chốt |Điểm dương không đồng nghĩa causalroot hoặc calibration |Thực nghiệmP4 sau G1, không tự thiết kế đồ thị |

Không có việc rẻ trong giới hạn đã nêu bị để “chờ quyền”. Bảng tiêu chí `tieu-chi-xong.csv` phân biệt đã hoàn thành công việc với hạn chế kết luận.
''')
# Preserve raw register; rebuild a precise derived register including repeats/control/variants.
old=O/'ca-da-chay-lich-su.csv'
if not old.exists(): shutil.copy2(O/'ca-da-chay.csv',old)
records=[]
for d in sorted((O/'runs').glob('run-dev-*')):
    summary=json.loads((d/'summary.json').read_text())
    for row in summary:
        case=row['case'];p=R/'data/rcaeval'/case
        files=[p/x for x in ('metrics.parquet','traces.parquet','logs.parquet') if (p/x).exists()]
        purpose=f"{d.name}: primary"+('; failed before diagnosis' if row['status']=='failed' else '')
        records.append([case,';'.join(map(str,files)),'SimpleRCA (M4)',purpose,'c: rerun sau bằng chứng mapping sai' if d.name=='run-dev-004' else 'b: bản cài/config mới'])
        for key in ('repeat','permuted','normal-control'):
            if (d/f'{case}-{key}.json').exists():records.append([case,';'.join(map(str,files)),'SimpleRCA (M4)',f'{d.name}: {key}','a: kiểm lặp lại' if key=='repeat' else 'b: đầu vào/window hoán đổi để kiểm'])
    if (d/'sensitivity.json').exists():
        case=summary[0]['case'];files=records[0][1]
        for x in json.loads((d/'sensitivity.json').read_text()):records.append([case,files,'SimpleRCA (M4) '+x['name'],f'{d.name}: sensitivity đã khóa','b: cấu hình/cửa sổ mới'])
for x in supp['variants']:
    case=supp['case'];p=R/'data/rcaeval'/case
    records.append([case,';'.join(str(p/x) for x in ('metrics.parquet','traces.parquet','logs.parquet')),'SimpleRCA (M4) log'+str(x['threshold']),'supplement-001: baseline/độc lập keyword count/sensitivity','b: kiểm ngưỡng đã khóa trên ca có log'])
records.append(['synthetic known-answer','src/simplerca/tests/test_core.py;results/T-017/scripts/independent_example.py','SimpleRCA M4 / bộ tính độc lập','16tests và12nhóm kiểm tự tạo','b: implementation mới, đáp án biết trước'])
for version,folder in [('v1','example-input'),('v2','example-input-run-dev-004')]:
    records.append(['re2tt_ts-auth-service_cpu_1',str(W/folder),'SimpleRCA M4 bộ tính độc lập',f'independent-example-{version}: so mọi score/rank/count','b: code độc lập mới' if version=='v1' else 'c: sửa mapping database của đầu vào normalized'])
with (O/'ca-da-chay.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(['ca','file_nguon','phuong_phap','muc_dich','ly_do']);w.writerows(records)
criteria=[
['1','Hoàn thành','16tests;12selftests;guard/path/alias/checks','synthetic và supplement-001; normal-control thực không đạt abstention được báo'],
['2','Hoàn thành','9mục hồ sơ; ví dụ độc lập2226check','ho-so-simplerca.md;vi-du-tinh-tay.md;example-comparison-v2.json'],
['3','Hoàn thành','PDF20/23trang;ảnhbảng2/3;Type và tỷ lệ riêng','sources/pdf-manifest.json;type-i-ii.md;CSV literal'],
['4','Hoàn thành trong giới hạn','3revision/70blob/license/Zenodo và FSEartifact','doi-chieu-code.md;code/config sinh0,80 cònOPEN'],
['5','Hoàn thành kiểm dev','30dev,repeat/permutation2case;normal-control báo kết quả bất lợi','run-dev-004;ca-da-chay.csv;không mở locked'],
['6','Hoàn thành','4file bắt buộc,16cột đúngprompt,11rows;nhápWHY;audit T000–012 liên quan','CSV/input_requirements.py;dinh-chinh-task-cu.md;không tái thực nghiệm mọi task'],
['7','Hoàn thành khi bàn giao','inventory/LOG6ý/A–H/prompt/STATE và phạm vi','handoff-check.json;state-edit-check.json;phần chưa kiểm ởkiem-dung-dan.md']]
with (O/'tieu-chi-xong.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(['tieu_chi','trang_thai','bang_chung','ghi_chu']);w.writerows(criteria)
pdf=json.loads((O/'sources/pdf-manifest.json').read_text())
for x in pdf:
    pages=[6,7] if x['name']=='arxiv-v2' else [7,8]
    x['table_images']=[str(W/f"{x['name']}-page-{p}.png") for p in pages]
    assert all(Path(p).exists() for p in x['table_images'])
    x['source_url']='https://arxiv.org/pdf/2510.04711v2' if x['name']=='arxiv-v2' else 'https://yifanyang6.github.io/assets/pdf/papers/fang2026rethinking-fse.pdf'
(O/'sources/pdf-manifest.json').write_text(json.dumps(pdf,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'reports':3,'case_registry_rows':len(records),'criteria':len(criteria),'supplement_baseline_exact':supp['baseline_matches_run004']},ensure_ascii=False))
