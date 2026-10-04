# TraceRCA — biến thể rút gọn trong RCAEval

Đây là hồ sơ của hàm `tracerca()` trong RCAEval. Hàm chấm **operation (thao tác)** từ độ trễ span, không tái lập toàn bộ TraceRCA gốc. Revision nằm trong mục 9 của `results/T-001/danh-sach-phuong-phap.md`; code đối chiếu là `D:/RCA-ext/src/RCAEval/RCAEval/e2e/tracerca.py`. Nguồn gốc được đọc ở clone TraceRCA của T-001, chưa chạy bộ dữ liệu của bài gốc.

## 1. Bài toán và đầu vào

Cho bảng span và mốc sự cố \(\tau\), tìm operation có nhiều span chậm sau mốc so với trạng thái trước mốc. Một operation là cặp service và method. Hàm ghép `serviceName + '_' + methodName`; method thiếu được thay bằng `operationName` (`tracerca.py:48–49`). Mốc phải cùng đơn vị với `startTime + duration`; dòng đổi mốc từ giây sang micro giây đã bị comment (`:51`).

Hàm thực sự đọc `serviceName`, `methodName`, `operationName`, `startTime`, `duration`. Bộ đọc chung của T-007/T-015 nhận thêm `traceID`, `spanID`, `parentSpanID`, nhưng **hàm này không dùng ba cột đó**. Nó không đếm trace độc nhất. Đầu ra là danh sách operation có điểm hữu hạn; đổi thành thứ hạng service phải có quy tắc gộp riêng.

Không cần nhãn nguyên nhân để học. Cần đoạn trước mốc được coi là bình thường và có đủ mẫu cho mỗi operation xuất hiện sau mốc. Đây là xếp hạng với mốc biết trước. Nó chưa cung cấp luật báo động hệ thống hay tự tìm \(\tau\).

## 2. Từng bước xử lý và công thức

Gọi \(d_i\) là duration của span \(i\), tính bằng micro giây. Thời điểm kết thúc là \(e_i=startTime_i+d_i\). Hàm chia **span**, không chia trace:

\[
B=\{i:e_i<\tau\},\qquad C=\{i:e_i\ge\tau\}.
\]

Với mỗi operation \(o\), lấy duration của span trong \(B_o\). Tính trung bình và độ lệch chuẩn mẫu, đổi sang mili giây rồi làm tròn hai chữ số:

\[
\mu_o=round\!\left(\frac{\sum_{i\in B_o}d_i}{1000|B_o|},2\right),\quad
\sigma_o=round\!\left(\frac{\sqrt{\sum_{i\in B_o}(d_i-\bar d_o)^2/(|B_o|-1)}}{1000},2\right).
\]

`get_operation_slo()` dùng `pandas.std()`, tức `ddof=1`; đây là độ lệch chuẩn, dù docstring gọi nhầm là variance (phương sai) (`:20–38`). Span sau mốc bất thường khi

\[
b_i=\mathbf1[d_i/1000\ge\mu_{o(i)}+3\sigma_{o(i)}].
\]

Gọi \(n_o\) là số span sau mốc của operation \(o\), \(a_o\) là số span bất thường của nó, và \(A=\sum_o a_o\). Code tính:

\[
support_o=s_o=\frac{a_o}{A},\qquad
confidence_o=c_o=\frac{a_o}{n_o},\qquad
J_o=\frac{2s_oc_o}{s_o+c_o}.
\]

Đó là harmonic mean (trung bình điều hòa), không phải Jaccard similarity (độ giống Jaccard), dù biến tên `ji`. Khi \(a_o>0\), công thức rút gọn thành \(J_o=2a_o/(A+n_o)\). Một operation có nhiều span bất thường, và ít span bình thường của chính nó, nhận điểm cao (`:73,77,82`). Không có lan truyền điểm giữa operation.

Nếu \(a_o=0\) và \(A>0\), code tính \(0/0\) ở công thức \(J_o\), sinh NaN. Nếu \(A=0\), support của mọi operation là NaN. Code sắp tất cả điểm giảm dần **trước**, rồi mới bỏ NaN (`:86–93`). Bỏ NaN sau sắp không sửa được những so sánh đã bị NaN phá.

## 3. Đồ thị được dùng ở đâu

Theo các vai trò ở K1 §3, bản RCAEval không dùng đồ thị để biểu diễn topology, tạo đặc trưng, chấm bất thường, lan truyền điểm, biểu diễn nhân quả hay xếp hạng. Nó chỉ nhóm span theo tên operation và tính duration. `parentSpanID` không vào phép tính; span mất cha hoặc nhiều root không làm đổi trực tiếp điểm, nhưng mất span vẫn làm đổi các số đếm.

Vì vậy, so MicroRank với biến thể này chưa tách được tác dụng riêng của PageRank. Hai bên còn khác đơn vị bằng chứng, luật chia trace, trọng số và giới hạn đầu ra. T-001 §3a dòng MicroRank/TraceRCA đã nêu giới hạn này.

## 4. Mặc định và nguồn file:dòng

| Tham số/quy ước | Mặc định thực tế | Nguồn |
|---|---|---|
| Đơn vị duration | micro giây; chia 1000 thành ms | `tracerca.py:34–35,61` |
| Độ lệch chuẩn | mẫu, `ddof=1` | `:35`; mặc định pandas được kiểm qua phép tính độc lập |
| Làm tròn mean/std | 2 chữ số sau dấu phẩy | `:34–35` |
| Luật bất thường | một phía, `duration >= μ+3σ` | `:61` |
| Điểm | trung bình điều hòa support/confidence | `:73,77,82` |
| Tie (hòa điểm) | giữ thứ tự xuất hiện operation ở span sau mốc | `:66,86`; `sorted` ổn định |
| Điểm NaN | bỏ sau sắp | `:90–93` |
| Số operation trả về | mọi operation có điểm không-NaN; không `top_max+6` | `:88–97` |
| Cửa sổ | hàm không cắt; T-007/T-015 tham chiếu ±600 s | `results/T-007/scripts/chay_e2.py:100–102`; WHY-16 |

`dataset` và `kwargs` được nhận nhưng không đổi luật hay tham số trong thân hàm (`:45–97`). ±600 s là quy ước bộ đọc, không phải tham số nội tại hoặc cấu hình tác giả baseline trace đã được xác minh. Cửa sổ P3 vẫn cần Minh chốt.

Gọi \(S\) là số span và \(M\) là số operation. Code RCAEval lọc toàn bảng cho từng operation ở cả thống kê reference và support/confidence, nên chi phí là \(O(MS)+O(M\log M)\), gồm bước sắp điểm (`tracerca.py:32–35,72–77,86`). Script độc lập dùng dictionary để tích lũy mỗi span một lần, rồi sắp operation, nên có chi phí kỳ vọng \(O(S)+O(M\log M)\) (`scripts/check_tracerca.py:100–155`). Lọc hữu hạn trước sắp không tự làm code raw (nguyên trạng) thành tuyến tính; phải phân biệt adapter chỉ sửa output với triển khai thống kê độc lập.

## 5. Chỗ khác TraceRCA gốc và lỗi NaN

TraceRCA gốc có quy trình chọn đặc trưng theo cặp gọi source–target, phát hiện invocation (lần gọi), ghép invocation thành tập service của trace, rồi khai phá frequent itemsets (tập mục thường gặp). Bản RCAEval chỉ giữ duration và hai tỷ lệ theo **span**.

Ở revision gốc đang kiểm:

- `run_invo_encoding.py:31–48,90–99` đọc danh sách trace từ pickle và ghi **pickle DataFrame invocation**, không phải CSV hay bảng `duration_self`. Mặc định `ENABLE_ALL_FEATURES=False` và `FEATURE_NAMES=['latency','http_status']` (`trainticket_config.py:1–13`). Cột mặc định gồm source, target, timestamp bắt đầu/kết thúc, trace_id, trace_label, latency, http_status và biên trace. Encoder bỏ invocation source=target (`run_invo_encoding.py:52–55`), đổi HTTP status thành nhóm hàng trăm (`:87`), và kiểm tên source/target thuộc inventory service (`:94–97`). Do đó đơn vị xếp hạng cuối là **service**, không phải operation/interface. Nhánh mặc định giữ nguyên latency/timestamp (`:79–87`); module nguồn `data.trainticket.download` được import ở `:11` nhưng không có trong clone. Đơn vị raw của nhánh này **chưa kiểm**, không tự suy từ schema RE2.
- `run_selecting_features.py:38–44,67–83` chọn đặc trưng bằng độ lệch chuẩn hóa giữa phân phối hiện tại và lịch sử; code thực gọi `stderr_criteria`, không gọi dòng `fisher_criteria` đã comment. Tham số CLI `--fisher` có default **1** (`:51`); chạy entrypoint Makefile lại truyền **3** qua `FISHER=3` (`Makefile:24,109–110`). Đây là ngưỡng chọn feature, khác ngưỡng detector `SIGMA=1`; tên tham số không đổi phép kiểm thành Fisher. Vì ngưỡng này có thể đổi tập feature, phải ghi rõ entrypoint khi tái lập pipeline gốc.
- `run_anomaly_detection_invo.py:38–60` xét độ lệch **hai phía** theo từng đặc trưng/cặp gọi. Hàm tên `anomaly_detection_3sigma`, nhưng hệ số thực là biến `threshold`; mặc định bằng **1**, và `Makefile:23` đặt `SIGMA=1`. Không thể gọi mặc định này là ngưỡng 3σ chỉ từ tên hàm. Reference dùng std dân số, có sàn 0,1 (`run_anomaly_detection_prepare_model.py:52–59`). Khi cache thiếu cặp/feature, detector lấy mean/std từ **current**, thay vì dừng vì thiếu reference (`run_anomaly_detection_invo.py:47–55`); đây là một thay đổi nghĩa phải kiểm khi chuyển dataset. Cột localization nhận là `predict`, được chép từ `Ours-predict` (`:116–118`).
- `run_localization_association_rule_mining_20210516.py:163–180` tạo tập source/target trong từng trace và cờ bất thường là max của các invocation. `:127–145` khai phá tập với `min_support_rate=0.1` và tính confidence theo trace; không có ngưỡng `min_confidence` tường minh ở đường này.
- Điểm tập mặc định là \(1/(1/\max(s,10^{-4})+1/\max(c,10^{-4})-1)\), tức Jaccard; sau đó nhân chênh số trace bất thường đi vào/đi ra service (`:294–299,338–377`). Code cuối chỉ dùng pattern một phần tử (`:365–366`), và `k=100` là số mức điểm chọn, không phải top-100 service (`:357–362`).
- File có tùy chọn PRFL/PageRank, nhưng đường `main()` truyền `enable_PRFL=False` (`:66–74`). Đọc có PageRank trong file không chứng minh lượt mặc định dùng nó. Bản RCAEval không có các bước trên.
- `main()` loại `gateway` khỏi pattern được xét (`:72`). Nó còn gọi `inject_noise(...,0)` (`:61–62`); dù tỷ lệ truyền vào là 0, hàm vẫn hạ cờ invocation với xác suất 1% trong các trace đang bất thường, dùng seed 2021 (`:23–34`). Đây là thay đổi ngẫu nhiên có seed trong code, không được gọi lượt mặc định là hoàn toàn giữ nguyên cờ detector.
- Builder chung `run_anomaly_detection_prepare_model.py:15–35` còn đọc NPZ trace labels để huấn luyện RF/MLP cho các baseline phụ, trước khi tạo cache reference invocation ở `:52–59`. Core TraceRCA localization không đọc nhãn nguyên nhân. Tuy vậy, chạy nguyên builder chung vẫn cần trace labels; không thể mô tả toàn pipeline là không cần mọi loại nhãn.

**Phân loại NaN:** tác giả RCAEval ghi rõ ý định “ignore ji nan” ở `tracerca.py:90`; loại operation không có bằng chứng bất thường là chủ ý có dấu vết. Đặt bước loại sau `sorted` là **lỗi triển khai thứ tự**, vì kết quả không còn giảm dần theo chính điểm đã tính. Không có dấu vết trong hàm cho thấy tác giả muốn dùng NaN để tạo thứ hạng khác.

Phản ví dụ độc lập: input `(low,0.2),(undefined,NaN),(high,0.9)` cho raw ranking `low,high`; lọc hữu hạn trước cho `high,low`. Phản ví dụ, code và kết quả nằm ở `results/T-015/runs/tracerca-audit/seed0/toy-checks.json`.

Tái dựng chỉ từ điểm T-007 đã lưu, không chạy lại baseline OB, cho 90/90 thứ hạng gốc và 90/90 thứ hạng xáo khớp; 90 ca có NaN, 79 ca không giảm dần. Adapter CANDIDATE lọc hữu hạn trước và phá hòa bằng tên operation ổn định: kết quả gốc/xáo khớp 90/90; đổi thứ hạng operation ở 88 ca, thứ hạng service ở 38 ca, vị trí service gốc ở 14 ca. **14 gồm cả sửa NaN và đổi quy tắc hòa**, nên không đối chiếu trực tiếp với 13 của T-007 khi chỉ bỏ NaN trước và giữ hòa theo thứ tự cũ. Mỗi ca và số tổng ở `seed0/t007-tung-ca.csv`, `seed0/t007-audit.json`.

Nguyên nhân khả thi khác đã phân biệt: hòa điểm cũng gây phụ thuộc thứ tự; sai số thống kê có thể đổi ngưỡng; adapter gộp service có thể đổi vị trí; cửa sổ có thể đổi tập span. Audit trên **cùng điểm đã lưu** chứng minh riêng lỗi sắp và quy tắc hòa đủ làm đổi thứ hạng. Nó không quy các khác biệt giữa bài, dataset và bộ đọc cho lỗi NaN.

Adapter đề xuất giữ bản raw cho tái lập; với bản đã sửa, dùng `stable_finite_ranks()` trong `scripts/check_tracerca.py`. Giữ \(A=0\) thành `NO_ANOMALY` và danh sách rỗng. Không biến \(0/0\) thành điểm 0 rồi thêm ứng viên một cách âm thầm. Không đổi công thức để lấy điểm chấm cao hơn. Đây là CANDIDATE **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**.

## 6. Giả định và điều kiện thất bại

Hàm RCAEval không có mục văn bản giải thích giả định hoặc giới hạn riêng của tác giả. Không gán cho tác giả các giả thuyết mới. Các điều kiện **đọc được từ code**, đã kiểm bằng toy, gồm:

- Operation mới sau mốc không có reference: lookup `normal_slo[op]` gây lỗi (`:59–60`). Một span reference cho std NaN; cờ `>=NaN` là False. Adapter kiểm độc lập báo `INVALID_BASELINE`, không gọi đó là bình thường.
- Hàm raw không kiểm startTime, duration hoặc mốc chia hữu hạn trước so biên. Adapter T-015 phải reject (báo lỗi và dừng) timestamp/mốc/duration không hữu hạn và duration âm; `independent_spans()` còn kiểm thời điểm kết thúc hữu hạn trước hai predicate `<`/`>=` (`scripts/check_tracerca.py:88–91,108–120`). Đây là guard adapter mới, không phải hành vi sẵn có của tác giả. Chín toy guard TraceRCA độc lập bị chặn đúng và toy hữu hạn khớp bản trước guard (`runs/review-response/guard-tests.json`). Quét đúng 90 nguồn OB và 3 TT dev đã dùng cho 0 dòng thời gian sai ở raw/cửa sổ, hash đều khớp (`runs/review-response/ec2-second/input-time-audit/summary.json`); không chạy lại ranker hay suy số cũ sai từ toy nonfinite.
- Reference hằng có \(\sigma=0\). Vì dùng `>=`, span hiện tại đúng bằng mean cũng bị gọi bất thường. Toy hai span 10 ms trước mốc và một span 10 ms sau mốc đã xác nhận. Đây là báo giả của detector, không được sửa bằng cách sắp thứ hạng.
- Thiếu span/mất mẫu làm đổi \(a_o,n_o,A\). Không có giả định “phải có cây trace hoàn chỉnh” để chạy hàm này, nhưng không đồng nghĩa score còn đại diện đúng cho workload.
- Service vắng span sau mốc không vào danh sách operation. Service có span nhưng không có span bất thường cũng không xuất hiện sau bước bỏ NaN. Service không có cạnh vẫn có thể là ứng viên vì bản này không đọc cạnh.

Chưa kiểm toàn văn bài TraceRCA gốc trong subtask này; không dùng các điều kiện suy từ RCAEval để tuyên bố tác giả TraceRCA gốc nêu chúng. Hồ sơ này không xác nhận tái lập TraceRCA gốc.

## 7. Ví dụ tính độc lập

Toy đã được ghi trước phần giải thích nhãn: operation `svc_a` có duration reference 90,100,110 ms, nên \(\mu=100\), \(\sigma=10\), ngưỡng 130 ms. Hai span sau mốc 120,140 ms cho \(a_a=1,n_a=2\). Operation `svc_b` có reference 50,60,70 ms, và span sau mốc 60 ms, nên \(a_b=0,n_b=1\). Tổng \(A=1\).

Vậy \(s_a=1,c_a=1/2,J_a=2/3\). Với `svc_b`, \(s_b=c_b=0\), code sinh NaN và không đưa nó vào kết quả. Tính độc lập không gọi hàm tác giả; lời gọi code chính thức chỉ ở đường đối chiếu riêng. Mọi điểm hữu hạn khớp, sai số tuyệt đối và tương đối đều 0; kết quả lưu `seed0/toy-checks.json`.

Ví dụ Train Ticket cố định trước xem kết quả là `re2tt_ts-auth-service_cpu_1`, cửa sổ tham chiếu ±600 s. Có 957.209 span trong cửa sổ: 474.132 span reference, 483.077 span sau mốc; tổng span bất thường \(A=5036\). Tính độc lập khớp code chính thức trên **96 điểm hữu hạn và 56 NaN**, sai số tuyệt đối/tương đối 0. Mọi số lấy từ `runs/tracerca-audit/seed0/tt-summary.json`, `tt-operation-scores.csv`.

Để xem phép tính không chọn theo nhãn, lấy operation hữu hạn đầu tiên theo thứ tự tên: `ts-admin-basic-info-service_GET`. Reference có 205 mẫu, μ=6,86 ms, σ=1,28 ms; ngưỡng=10,70 ms. Sau mốc có 190 span,3 span vượt ngưỡng. Vậy \(s=3/5036\), \(c=3/190\), \(J=6/(5036+190)=0.001148105625717566\).

Sau khi lưu ranking mới dùng nhãn để giải thích root: `ts-auth-service_POST /api/v1/users/login` có μ=144,79 ms, σ=54,22 ms; ngưỡng 307,45 ms. Trong 831 span sau mốc có 412 span bất thường, nên \(J=824/(5036+831)=0.1404465655360491\), lớn hơn mọi operation khác. Hai operation tiếp theo có điểm 0,03607937462417318 và0,03382157123834887, đều thuộc ts-basic-service. Vì vậy auth đứng đầu khi gộp service bằng lần xuất hiện đầu trong ranking. Đó là cơ chế từ tỷ lệ span chậm, không phải bằng chứng lan truyền đồ thị hay xác nhận nhân quả của loại lỗi CPU. Hòa điểm, sampling và thay workload vẫn là các giải thích khả thi cho thứ hạng thấp hơn của những service khác.

Đảo cột giữ cả raw ranking và điểm. Đảo dòng giữ **mọi điểm**, nhưng raw ranking đổi vì NaN/tie; adapter canonical giữ ranking. Phép kiểm đầu lấy span có start trước mốc, chia tại \(\tau-300\)s, có 2818 span bị flag và 104 operation hữu hạn. Kiểm biên sau đó thấy **11 span kết thúc tại/sau mốc tiêm**, trong đó 4 span bị flag. Vì vậy lượt đầu chưa phải cửa sổ quan sát hoàn toàn trước tiêm; giữ nguyên hai file cũ để kiểm lại (`tt-two-normal-windows.json`, `tt-summary.json`).

Loại đúng 11 span này không đổi reference ở trước \(\tau-300\)s. Trừ số đếm của chúng rồi tính lại công thức độc lập cho control nghiêm: **2814 span bị flag trong 242.818 span current**, 102 operation hữu hạn. Mọi span được giữ đều kết thúc trước tiêm. Kết quả ở `runs/tracerca-audit/normal-boundary/strict-two-normal-windows.json`; chứng cứ 11 span, ngưỡng và cờ ở `strict-normal-boundary-audit.json`. Đây là **báo giả theo giả định đoạn trước tiêm không có sự cố khác**, không phải nguyên nhân sự cố đã được tìm đúng. Baseline thay đổi, đuôi độ trễ, σ nhỏ/làm tròn và sự cố có sẵn chưa được gắn nhãn là các giải thích khả thi; task chưa tách chúng bằng số liệu. Không dùng top1 của ca lỗi để che control này.

Chạy lại cùng ca trong tiến trình riêng, `PYTHONHASHSEED=0` và `1`, cho mọi điểm, raw ranking, adapter ranking và số đếm hai cửa sổ bình thường giống nhau. Kết quả đối chiếu ở `runs/tracerca-audit/repeat-check.json`; giữ riêng cả `seed0/` và `seed1/`. Parquet chỉ đọc bằng runtime `py312` rồi chuyển CSV qua pipe trong bộ nhớ; tính điểm và lời gọi code chính thức dùng `py312-pin` với Python 3.12.10, pandas 2.2.3. Không cài hay sửa môi trường chung. Hash nguồn, code, artifact và revision nằm trong `runs/tracerca-audit/manifest-sources.json`.

## 8. Đường nhãn có thể lọt vào phương pháp

Mốc inject đi vào cửa sổ và phép chia reference/current. Điều này hợp lệ cho chế độ biết mốc, không hợp lệ khi gọi pipeline là tự phát hiện. Không chọn operation, service hay SLI theo service gốc. Bộ đọc biết tên ca để tìm file; tên ca và đáp án không được truyền vào hàm tính điểm. Script chỉ lấy nhãn từ tên ca **sau khi đã ghi ranking độc lập** để giải thích thứ hạng.

Tập baseline phải do giao thức xác định trước. Chọn đoạn “bình thường” dựa trên nhãn test hoặc lựa chọn cửa sổ sau khi xem điểm đều có thể làm rò thông tin. Case basename và root label không được dùng phá hòa.

## 9. Yêu cầu khi chạy trên dataset khác

Cần service/method có định danh nhất quán, duration và timestamp cùng micro giây, cùng đồng hồ, cùng phạm vi sampling, và reference bình thường cho mọi operation hiện tại. Định danh operation là bắt buộc để tra μ/σ. Adapter yêu cầu duration không âm, startTime/duration/mốc hữu hạn và kiểm thời điểm kết thúc trước phân nhóm; input sai phải báo lỗi thay vì xếp hạng. Có ít nhất hai span reference mới tính được std mẫu; code không nêu số mẫu đủ ổn định về thống kê. Cần kiểm key service–method không va chạm khi ghép dấu `_`.

Không cần call graph hoặc service inventory để chạy hàm. Tuy vậy, đánh giá trên toàn inventory phải giữ rõ service không có bằng chứng: bản gốc không tự xếp hạng chúng. Adapter gộp operation thành service, xử lý tie, missing reference, NaN và không-bất-thường phải được ghi trước khi dùng ở P3. Nếu P3 cần thứ hạng đầy đủ cho MRR/NDCG, việc nối thêm service vắng trace là một quy ước đánh giá riêng cần Minh quyết; không coi đó là đầu ra của TraceRCA.

Nếu dùng **TraceRCA gốc**, đầu vào khác hẳn hàm RCAEval: pickle invocation có source/target service, trace_id và feature; cache reference theo cặp/feature; danh sách feature được chọn; inventory/config cùng quy tắc chuẩn hóa tên. Default chỉ dùng latency và http_status; bật tài nguyên là một cấu hình khác. Phải xác minh đơn vị raw và phục hồi module encoder nguồn đang thiếu trước khi chuyển RE2. Builder chung cần thêm NPZ lịch sử với trace labels cho RF/MLP phụ; một adapter chỉ lấy nhánh TraceRCA phải ghi rõ không chạy các nhánh đó. Task này chưa chạy pipeline gốc, nên không suy chi phí hoặc khả năng tái lập từ phép kiểm RCAEval.
