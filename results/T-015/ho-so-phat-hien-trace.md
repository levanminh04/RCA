# Hồ sơ hai luật phát hiện trace

Cần phân biệt **span detector (bộ phát hiện span)** của RCAEval với **trace detector (bộ phát hiện trace)** trong MicroRank gốc. Cả hai dùng mean/std nhưng chấm các đại lượng khác nhau. PageRank chạy ở bước RCA sau detector; nó không làm cho các luật này thành bộ phát hiện đồ thị.

Nguồn: `RCAEval/e2e/tracerca.py`, `RCAEval/e2e/microrank.py` ở clone `D:/RCA-ext/src/RCAEval`; MicroRank gốc `anormaly_detector.py`, `preprocess_data.py`, `online_rca.py` ở clone T-001. Revision được ghim tại T-001 §9. Bài WWW'21 được đọc qua `results/T-015/sources/microrank-paper.txt`, có mốc `[PAGE n]`; không dùng K1 chưa kiểm làm bằng chứng chính.

## A. Luật μ+3σ theo span của RCAEval

### 1. Bài toán và đầu vào

Tìm span có **inclusive duration (thời lượng gồm thời gian chờ thao tác con)** lớn hơn reference của chính operation. Cần `serviceName`, `methodName`, `operationName`, `startTime`, `duration`, và mốc chia reference/current \(\tau\). Không cần `parentSpanID`, trace root hoặc nhãn nguyên nhân. Duration phải là micro giây; ngưỡng được tính bằng mili giây.

Định danh operation là đầu vào bắt buộc: phải biết service và method, dùng operationName khi method thiếu. Vì μ/σ được tra theo khóa này, duration đơn lẻ chưa đủ chạy luật. Adapter T-015 yêu cầu startTime, duration và mốc chia là số hữu hạn; duration không âm. Dữ liệu vi phạm phải báo lỗi trước khi chia cửa sổ, không được coi là bình thường hoặc tạo evidence (bằng chứng). Đây là guard của adapter, không phải guard sẵn có của hàm RCAEval (`src/microrank/__init__.py:35–37`; `scripts/check_tracerca.py:88–91,108–120`).

Hàm biết mốc chia, không tự tìm một incident onset (thời điểm bắt đầu sự cố). Nó trả cờ theo span. TraceRCA RCAEval dùng các cờ này trực tiếp trong số đếm span. MicroRank RCAEval cũ chỉ dùng cờ để lấy hai số trace, còn đồ thị dựng trên toàn span trước/sau mốc (`microrank.py:666–698`); không được mô tả hai pipeline như cùng detector rồi chỉ khác xếp hạng.

### 2. Từng bước và công thức

Operation \(o=(service,method)\); method thiếu được thay bằng operationName. Baseline là span kết thúc trước \(\tau\). Với duration \(d_i\) tính bằng micro giây:

\[
\mu_o=round(mean(d_i)/1000,2),\quad
\sigma_o=round(std_{ddof=1}(d_i)/1000,2),\quad
b_i=\mathbf1[d_i/1000\ge\mu_o+3\sigma_o].
\]

Hệ số 3, phép so `>=`, std mẫu và làm tròn hai số là code thực (`tracerca.py:34–35,53–61`; `microrank.py:562–563,654–667`). Reference/current chia theo **thời điểm kết thúc span**. Bộ đọc T-007 cắt cửa sổ theo **thời điểm bắt đầu span**, nên một trace hoặc span kéo dài qua biên có thể bị cắt không đồng nhất.

Nếu muốn gộp thành trace bất thường bằng “ít nhất một span bất thường”, đó là quy tắc adapter của T-015, không phải một luật báo động hệ thống được hàm này trả về. Tập bình thường phải là phần bù của cùng tập trace hiện tại; chỉ lấy unique traceID của các span bình thường sẽ gây nhóm chồng nhau.

### 3. Vai trò đồ thị theo K1 §3

Không có đồ thị ở phép chấm này. Cạnh gọi không tham gia tạo ngưỡng hoặc cờ. Dữ liệu có trace ID không tự làm một phép tính trở thành detector đồ thị. Mất cha/nhiều root không gây lỗi lookup ở luật span; thiếu span hoặc mất mẫu vẫn thay đổi phân phối reference/current.

### 4. Mặc định, kèm file:dòng

| Mục | Mặc định | Nguồn |
|---|---|---|
| Khóa operation | service + `_` + method, fallback operationName | `tracerca.py:48–49` |
| Reference | `startTime+duration < inject_time` | `:53` |
| Đổi đơn vị | duration/1000 → ms | `:34–35,61` |
| Mean/std | làm tròn 2; std mẫu ddof=1 | `:34–35` |
| Ngưỡng | μ+3σ, dùng `>=` | `:61` |
| Ngưỡng báo động hệ thống | không có trong hàm | `:45–98` |
| Cửa sổ | do bộ đọc chọn; T-015 tham chiếu ±600 s | `results/T-007/scripts/chay_e2.py:100–102`; WHY-16 |

Gọi \(S\) là số span và \(M\) là số operation. Code RCAEval lọc lại bảng span cho từng operation để tính mean/std, nên riêng bước reference tốn \(O(MS)\) (`tracerca.py:32–35`; `microrank.py:560–563`). Groupby (nhóm theo operation) hoặc dictionary (bảng tra) gom mẫu/tính cờ trong \(O(S)\) kỳ vọng; `sort=True` của groupby T-015 còn sắp \(M\) khóa, thêm \(O(M\log M)\) (`src/microrank/__init__.py:52–61`; `scripts/check_tracerca.py:97–141`). Đây là chi phí riêng detector, chưa bao gồm sắp span, dựng đồ thị và PageRank của cả pipeline.

### 5. Khác bài và code gốc

Đây là inclusive duration của từng span. MicroRank gốc dùng **operation handling time (thời gian xử lý riêng của thao tác)** và số lần operation xuất hiện trong trace để dự báo end-to-end latency (độ trễ đầu đến cuối). Vì vậy không thể gọi μ+3σ theo span là detector MicroRank gốc.

TraceRCA gốc cũng khác: detector invocation của source–target, nhiều đặc trưng, so hai phía; tên hàm chứa `3sigma` nhưng hệ số mặc định thực là 1 (`run_anomaly_detection_invo.py:14,38–60,72`; `Makefile:23`). Không đồng nhất tên phương pháp với một giá trị ngưỡng chưa đọc code.

### 6. Giả định và điều kiện thất bại

RCAEval không nêu riêng một bộ giả định trong hàm. Các điều kiện code cần và phép kiểm đã làm được ghi rõ:

- Mọi operation sau mốc phải có reference. Không có reference gây KeyError; một mẫu reference cho std NaN. Script kiểm độc lập báo trạng thái đầu vào, không điền ngưỡng bằng nhãn.
- Với reference hằng, σ=0 và `>=` làm span đúng bằng mean cũng bất thường. Toy đã xác nhận trong `runs/tracerca-audit/seed0/toy-checks.json`.
- Baseline phải thật sự đại diện bình thường. Thay workload, tốc độ sampling hoặc composition operation có thể gây báo giả; đây là điều kiện suy từ công thức, không tuyên bố tác giả đã kiểm mọi tình huống.
- Không có cờ bất thường thì không được trả một thứ hạng dự phòng rồi diễn giải thành nguyên nhân có nghĩa.

### 7. Ví dụ tính tay và kiểm độc lập

Ba span reference 90,100,110 ms cho μ=100 ms, σ mẫu=10 ms, ngưỡng 130 ms. Span hiện tại 120 ms bình thường; 140 ms bất thường. Script tự tính mean/std/cờ bằng số duration, không gọi hàm tác giả trong phép tính. Đường đối chiếu riêng xác nhận mọi điểm TraceRCA hữu hạn khớp code chính thức với sai số 0 (`seed0/toy-checks.json`).

Toy hai cửa sổ bình thường có reference 9,10,11 ms và current 10,11 ms trả `NO_ANOMALY`, ranking rỗng. Toy reference hằng 10,10 ms/current 10 ms cho báo giả theo code gốc; giữ kết quả đó để phân biệt “không lỗi khi chạy” với “phát hiện đúng”. Toy ngưỡng đúng bằng 130 ms xác nhận phép so `>=`; đổi parent thành mất cha/nhiều root và ghép traceID không đổi điểm span. Các phép kiểm thêm ở `runs/tracerca-audit/toy-extra/toy-checks.json`.

Ca TT cố định `re2tt_ts-auth-service_cpu_1` có 5036 span bị flag trong 483.077 span sau mốc, theo reference 474.132 span; mọi 96 điểm TraceRCA hữu hạn/56NaN khớp code chính thức với sai số 0. Operation login của auth có reference 842 span: μ 144,79 ms, σ 54,22 ms, ngưỡng 307,45 ms; 412/831 span sau mốc bị flag. Điểm/chỉ số này lấy từ `seed0/tt-operation-scores.csv`, `tt-summary.json`.

Cùng 5036 cờ span đó, biến thể **MicroRank-RCAEval sửa đầu vào** gộp thành 1403 trace bất thường và 1326 trace bình thường trong 2729 trace sau mốc; không giao nhau. Đó là kết quả khác đơn vị so số đếm span của TraceRCA, vì mỗi trace chỉ cần ít nhất một span bị flag. Tính độc lập mean/std/cờ/partition và cả bốn quan hệ đồ thị khớp snapshot ở 19 phép so; nguồn `runs/tt-independent-inputs/auth/comparison.json`, snapshot `runs/tt-local/example.json`. Phép so không dùng root label. Tuy vậy, phép so audit root/missing lúc đầu cùng dùng danh sách token thiếu `<NA>`, nên PASS không xác nhận đúng nghĩa null. Census scalar sau đó chứng minh pandas.NA có `str='<NA>'`, không phải None (`runs/tracerca-audit/parent-null-scalar-audit.json`). Đính metadata riêng trên runtime pin xác nhận: nhóm normal có 1326 root/0 missing; anomaly có 1403 root/0 missing. Cả bốn quan hệ graph mỗi phía khớp chính xác snapshot gốc, nên đầu vào PageRank/spectrum và điểm không đổi (`runs/root-audit-correction/auth/audit-correction.json`). Giữ snapshot cũ để kiểm lỗi audit; đây không phải đổi root policy sang detector gốc frontend/server.

Phép kiểm đầu có 2818 span bị flag trên 242.829 span current và 104 operation hữu hạn, nhưng chỉ lọc start trước tiêm. Census tìm thấy 11 span kết thúc tại/sau tiêm, trong đó 4 span bị flag. Giữ nguyên lượt đầu ở `seed0/tt-two-normal-windows.json`. Control nghiêm loại 11 span, không đổi reference, rồi tính lại số đếm/điểm độc lập: **2814 span bị flag trên 242.818 span current và 102 operation hữu hạn**, mọi span kết thúc trước tiêm (`normal-boundary/strict-two-normal-windows.json`, `strict-normal-boundary-audit.json`).

Đây là **báo giả theo giả định đoạn trước tiêm không có sự cố khác**, không được diễn giải ranking thành root cause của lỗi tiêm. Các nguyên nhân khả thi gồm đuôi độ trễ, baseline thay đổi, làm tròn/σ nhỏ, rule `>=` hoặc sự cố trước tiêm chưa gắn nhãn; task chưa tách từng nguyên nhân bằng số liệu. Muốn gọi detector dùng được cho tự phát hiện phải có quy tắc calibration (hiệu chỉnh ngưỡng) và đánh giá báo giả được Minh chốt; hiện vẫn CANDIDATE **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**.

Biến thể MicroRank sửa đầu vào trên đúng control nghiêm có cùng 2814 cờ span, tạo 570 trace bất thường và 863 trace bình thường trong 1433 trace current, rồi trả 11 operation (`runs/tt-local/auth/two-normal-summary.json`). Phép kiểm vì vậy chưa đạt yêu cầu ngữ nghĩa “hai cửa sổ bình thường không tìm ra nguyên nhân có nghĩa”; phải giữ trạng thái **báo giả của pipeline dùng luật span**, dù PageRank/spectrum chạy không lỗi và các nhóm không giao nhau. Sửa cạnh/partition không tự hiệu chỉnh detector.

### 8. Đường nhãn

Mốc inject dùng để cắt cửa sổ/chọn reference. Đây là thông tin oracle (biết trước) nếu chuyển sang tự phát hiện. Tên ca, root service, fault type, chọn SLI theo root không thuộc đầu vào. Chọn ngưỡng/cửa sổ sau khi nhìn test cũng là đường rò thông tin. Script chỉ giải thích root sau khi đã lưu thứ hạng.

### 9. Dataset khác

Cần timestamp/duration cùng micro giây, đồng hồ tương thích, service–method định danh ổn định, reference cho mọi operation, ít nhất hai mẫu để std mẫu xác định. Adapter phải reject (báo lỗi và dừng) startTime/duration/mốc không hữu hạn hoặc duration âm; script TraceRCA độc lập còn kiểm tổng startTime+duration hữu hạn trước so biên (`scripts/check_tracerca.py:108–120`). Code nguyên không có những guard này. Code không định nghĩa lượng reference tối thiểu đủ về thống kê. Không cần parent/root để chạy luật, nhưng phải biết duration là inclusive hay exclusive và lấy mẫu có đổi không. Luật gộp span thành trace/incident, minimum alarm count (số bằng chứng báo động tối thiểu) và xử lý baseline hằng chưa được tác giả RCAEval cung cấp; mọi lựa chọn mới là CANDIDATE **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**.

Kiểm sau phản hồi có 10 toy guard adapter, 9 toy TraceRCA độc lập và 8 toy duration root; tất cả input sai đều bị chặn, toy hữu hạn khớp bản trước guard chính xác (`runs/review-response/guard-tests.json`). Quét đúng nguồn của 90 ca OB và 3 ca TT dev đã chạy cho 0 dòng thời gian sai ở cả raw và cửa sổ ±600 s; hash nguồn khớp bản đã dùng (`runs/review-response/ec2-second/input-time-audit/summary.json`). Đây là kiểm miền đầu vào, không chạy lại phương pháp, không xác nhận độ chính xác detector và không kiểm full schema gốc.

## B. Detector của MicroRank gốc

### 1. Bài toán và đầu vào

Detector so **độ trễ toàn trace** với tổng thời gian xử lý dự kiến của các operation mà trace thực sự đi qua. Vì request làm nhiều việc có thể chậm một cách bình thường, reference phụ thuộc số lần mỗi operation xuất hiện, không chỉ một ngưỡng latency chung.

Code gốc đọc Jaeger trong Elasticsearch: traceID, spanID, operationName, duration, serviceName, references và tag `span.kind` (`preprocess_data.py:28–89,101–114,131–225,275–329`). Root đặc biệt là **service tên `frontend` và tag `span.kind=server`**, không phải mọi span có parent trống (`:177–190,207–221,311–327`). RE2 parquet có 11 trường ở schema đã kiểm của T-002; adapter RCAEval chọn tám cột trace và không có tag này. Không tự suy root policy từ tên service gốc.

### 2. Từng bước và công thức

**Reference.** Code xử lý các trace theo thứ tự traceID/startTime. Với mỗi span, duration riêng được tính bằng duration ban đầu trừ duration các span con trực tiếp đã gặp. Với \(h_s\) là thời gian xử lý này:

\[
\mu_o=round(mean(h_s:o(s)=o)/1000,4),\qquad
\sigma_o=round(std_{ddof=0}(h_s:o(s)=o)/1000,4).
\]

Đây là std quần thể `numpy.std`, khác std mẫu của RCAEval (`preprocess_data.py:169–225,235–254`). Khi có references nhưng cha chưa có trong bộ nhớ, code đánh dấu trace baseline bị loại; reference cũng bị loại nếu thời gian xử lý root sau phép trừ vượt 1.000.000 micro giây (`:143–150,185–194`). Nhánh thiếu references ở span đầu của trace mới còn có lỗi `parentId` chưa gán hoặc giữ từ span cũ (`:210–218`; xem §B.6–B.7), nên không chỉ có hành vi loại trace. Phép trừ tổng con không phải phép hợp khoảng thời gian; với con chạy song song nó có thể cho self-time âm. Đây là hành vi code cần kiểm, không tự gọi mọi số âm là thời gian xử lý vật lý đúng.

Khóa operation của detector gốc là `serviceName + '_' + operationName.split('/')[-1]` (`preprocess_data.py:106–110,164–167,286–289`). Prefix service tách hai service cùng tên thao tác, nhưng hai đường dẫn trong cùng service có segment cuối giống nhau có thể bị gộp; đường dẫn kết thúc bằng `/` cho suffix rỗng. Không tự thay bằng key method đầy đủ rồi gọi đó là preprocessing nguyên trạng.

**Độ trễ quan sát.** \(c_{to}\) là số span của operation \(o\) trong trace \(t\). \(D_t\) là tổng inclusive duration của các span frontend-server trong trace, chia 1000 sang ms (`:292–327`). Nếu có nhiều span loại root này, code **cộng** duration, không lấy max hay critical path (đường quyết định độ trễ).

**Báo động hệ thống.**

\[
E_t^{alarm}=\sum_o c_{to}(\mu_o+1.5\sigma_o),\quad
b_t^{alarm}=\mathbf1[D_t>E_t^{alarm}],\quad
alarm=\mathbf1[\sum_t b_t^{alarm}>8].
\]

Mọi phép so đều nghiêm `>` (`anormaly_detector.py:44–75`). Không có điều kiện tỷ lệ >1% trong nhánh chạy thực; câu ở docstring `:39` không phải code quyết định.

**Chia trace để RCA.** Sau báo động, code dùng luật khác:

\[
E_t^{partition}=\sum_o c_{to}(\mu_o+\sigma_o),\qquad
b_t^{partition}=\mathbf1[D_t>E_t^{partition}+50\text{ ms}].
\]

`trace_list_partition()` đưa mỗi trace vào đúng một nhóm (`anormaly_detector.py:93–133`). Vòng RCA chỉ chạy PageRank khi cả nhóm bình thường và bất thường đều không rỗng (`online_rca.py:220–232`). Vì hai ngưỡng khác nhau, hệ thống có thể báo động nhưng không có trace bất thường theo luật partition; không được coi đó là cùng một ngưỡng.

### 3. Vai trò đồ thị theo K1 §3

Quan hệ cha–con cung cấp ngữ cảnh để loại thời gian con khỏi reference của cha. Công thức detector dùng số lần operation, mean/std và root latency; nó không dùng PageRank, điểm lan truyền hoặc đồ thị làm đối tượng anomaly score. Sau partition, quan hệ gọi và trace coverage (trace đi qua operation nào) mới vào hai PageRank ở RCA. Bài §4.2–4.3 cũng tách hai bước (`microrank-paper.txt:292–306`).

### 4. Mặc định, kèm file:dòng

| Mục | Mặc định thực của code gốc | Nguồn |
|---|---|---|
| Đơn vị truy vấn | timestamp mili giây | `preprocess_data.py:21–22,50–53` |
| Đơn vị span | duration micro giây → chia1000 ra ms | `anormaly_detector.py:56,95`; `preprocess_data.py:250–254` |
| Khóa operation detector | service + `_` + segment cuối của operationName | `preprocess_data.py:106–110,164–167,286–289` |
| Reference std/làm tròn | `ddof=0`, 4 chữ số | `preprocess_data.py:250–254` |
| Root | `frontend` AND `span.kind=server` | `:177,207,311,326` |
| Reference mặc định trong script online | 1 phút hard-code | `online_rca.py:33–41` |
| Khuyến nghị normal history | ví dụ1h trong bài; docstring muốn >1h | bài §4.2 `microrank-paper.txt:294–300`; `anormaly_detector.py:11` |
| Cửa sổ báo động | 60s, trễ thời gian hiện tại1 phút | `online_rca.py:158–163` |
| Alarm multiplier/count | 1,5; hơn 8 trace | `anormaly_detector.py:62–70` |
| Partition | μ+σ mỗi operation, cộng 50 ms toàn trace | `:93–102` |
| Cửa sổ RCA | detect_time −5 s đến +55 s | `online_rca.py:165–167` |
| Nghỉ sau RCA | sleep 240 s rồi sleep 60 s | `:245–246` |

Các khoảng ±300/±600 s của RCAEval không thay thế cửa sổ online gốc. Hash seed không có trong công thức detector; thứ tự span lại ảnh hưởng preprocessing khi cha phải có trước con. Không chỉ thay hash seed rồi coi như đã kiểm mọi nguồn bất định.

### 5. Chỗ code khác bài

Bài §4.2 dùng \(\sum c_o(\mu_o+1.5\sigma_o)\), normal history ví dụ 1 h, sliding window 30 s và chỉ một trace anomal đã kích hoạt; §4.3 nói partition theo cùng Equation1. Code dùng window 60 s, alarm>8, và partition μ+σ+50 ms. Ghi rõ cả hai thay vì chọn một bản theo kết quả tốt hơn.

Văn bản §4.2 có câu “expected > real” mới coi anomal (`microrank-paper.txt:313–314`), ngược overview “real > expected” (`:229–232`) và code (`anormaly_detector.py:64`). Câu này là mâu thuẫn nội tại của nguồn; khi diễn giải cách chạy, dùng phép so **real > expected đã xác minh ở code** và nêu mâu thuẫn, không âm thầm đảo code. Không có căn cứ từ một câu lỗi để gọi trace nhanh là latency anomaly.

### 6. Giả định và điều kiện thất bại do tác giả nêu

Bài nói rõ phương pháp nhắm bất thường biểu hiện qua **latency deviations (độ trễ thay đổi)**; phụ thuộc chất lượng tracing, mất quá nhiều trace làm độ chính xác giảm; việc instrument trace có overhead; cách làm phản ứng sau khi latency issue đã xảy ra (`microrank-paper.txt:417–421,698–707`). Bài cho phép cập nhật normal mean/std khi xuất hiện một chuỗi báo giả (`:299–300`), tức baseline cố định không được xem là bất biến trong mọi workload. Tác giả không đánh giá detector trên dữ liệu production C vì thiếu danh sách fault đầy đủ (`:597–607`).

Các rủi ro **suy từ code**, không gán thành phát biểu của tác giả:

- Có references nhưng mất cha hoặc con xuất hiện trước cha làm trace baseline bị loại. Riêng span đầu của trace mới không phải frontend-server và có references rỗng: `if parentId in temp` nằm ngoài nhánh gán parentId (`preprocess_data.py:210–218`). Nếu chưa từng gán biến, pipeline có thể crash bằng `UnboundLocalError`; nếu đã gán từ span trước, code dùng parentId cũ. Không khẳng định mọi references rỗng đều crash. Nhiều root frontend-server được cộng duration; nhiều root từ service khác không được nhận tự động.
- Trace bị cắt theo startTime không đảm bảo đủ cha/con/root. Reference được lọc và current được đếm theo luật khác nhau; caller phải ghi số trace bị bỏ.
- Khi chuyển trace, current không có root bị `pop`; trace cuối chưa có bước hậu kiểm tương tự (`preprocess_data.py:315–329`). Không giả định mọi output operation_count đều có D>0 chỉ vì trace trước đã bị lọc.
- Trừ tổng con song song có thể cho self-time âm. Operation mới hoặc operation mất hết reference có thể tạo NaN/lookup lỗi. Một phép so với NaN không phát hiện được vấn đề đầu vào.
- Duration root không hữu hạn không được code gốc chặn trước phép so: NaN có thể bị coi là trace bình thường. Adapter công thức T-015 yêu cầu duration root hữu hạn và không âm trước alarm/partition (`src/microrank/detectors.py:8–13,25–38`); không gán guard này cho tác giả.
- Số alarm>8 phụ thuộc throughput và độ dài cửa sổ. Tỷ lệ anomaly giống nhau có thể báo hoặc không báo khi số request khác nhau.

### 7. Ví dụ tính tay và kiểm độc lập

Toy gồm operation A có μ=10ms,σ=1ms; B có μ=20ms,σ=2ms. Mỗi trace có A một lần, B một lần, root duration 35.000 micro giây=35ms.

\[
E^{alarm}=(10+1.5\cdot1)+(20+1.5\cdot2)=34.5\text{ ms}.
\]

Có 9 trace 35 ms, mỗi trace vượt 34,5 ms ; 9>8 nên báo động. Nhưng ngưỡng partition là \((10+1)+(20+2)+50=83\)ms. Cả 9 trace đều thuộc nhóm bình thường theo partition. Vòng RCA sẽ không xếp hạng khi nhóm anomal rỗng. Ví dụ cho thấy cần phân biệt alarm và partition, không suy báo động đồng nghĩa RCA có đủ hai nhóm.

Script tính độc lập hai công thức, rồi so với các hàm chính thức được lấy bằng AST (chỉ nạp hàm, không kết nối Elasticsearch/không chạy code top-level). Kết quả khớp, lưu `results/T-015/runs/tracerca-audit/seed0/toy-checks.json`. Phép kiểm này xác nhận **công thức trên operation_count/SLO**, không xác nhận chuyển schema RE2 thành self-time/root gốc.

Toy riêng lấy nguyên `get_operation_slo` bằng AST: trace t1 có một span frontend-server, rồi trace t2 bắt đầu bằng span service khác với `references=[]`. Lời gọi tái hiện `UnboundLocalError` ở parentId, không phải chỉ bỏ t2. Kết quả toy được ghi trước khi đọc REVIEW và tái kiểm ở `tasks/T-015-ho-so-microrank/LOG.md`, mục tự soát S2/N2 của phiên2. Chưa dùng toy này để suy lỗi đã xảy ra trên các ca RE2: T-015 chưa chạy toàn preprocessing gốc trên RE2.

### 8. Đường nhãn

Detector gốc tự dùng đồng hồ hiện tại và normal history, không cần mốc inject. Đoạn normal history mà người thực nghiệm chọn bằng nhãn vẫn có thể tạo rò thông tin. Root policy frontend/server là schema code gốc, không phải nhãn service gây lỗi. Tự đổi root policy theo service gốc của mỗi ca, chọn operation hoặc SLI theo root label, hoặc dùng inject để kích hoạt rồi gọi là tự phát hiện đều sai giao thức.

### 9. Dataset khác và đề xuất P3

Để chạy **đúng detector gốc**, cần schema Jaeger hoặc adapter bảo toàn tag client/server, root request latency, quan hệ cha–con đầy đủ và thứ tự, duration micro giây, operation count và normal handling-time reference. Phải kiểm nhánh references rỗng nêu ở §B.6 trước khi chuyển schema; chỉ điền một root marker chưa giải quyết lỗi này. Adapter công thức phải từ chối duration root không hữu hạn/âm, thay vì để NaN vào nhóm bình thường. Schema RE2 đã kiểm thiếu `span.kind`; không được tự coi mọi parent trống là frontend-server rồi ghi “MicroRank gốc”. Muốn áp dụng phải có mapping schema do Minh chốt và phép kiểm độc lập.

T-015 kiểm grouping/đồ thị như gốc nhưng giữ detector span của RCAEval. Tên Minh đã duyệt là **MicroRank-RCAEval sửa đầu vào**; mô tả kỹ thuật đi kèm là sửa grouping/graph, giữ detector span μ+3σ. Nó không thay thế hồ sơ detector gốc. Bản faithful MicroRank gốc là ưu tiên theo QT2 khi đầu vào đáp ứng; lựa chọn bản dùng P3 phải dựa trên ngữ nghĩa/đầu vào, không chọn bản chấm điểm cao hơn. Mapping detector, luật root và dùng detector span là CANDIDATE **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**.
