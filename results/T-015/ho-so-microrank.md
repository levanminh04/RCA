# Hồ sơ kỹ thuật MicroRank

Task T-015, P1, G1. Hồ sơ này trả lời RQ1 và nhận xét của cô về chiều sâu kỹ thuật. Các lựa chọn cho P3 là **CANDIDATE**, chưa phải quyết định của Minh. Số thực nghiệm chỉ được dẫn từ file chạy; số bài báo có nguồn riêng.

Nguồn trực tiếp đã đọc: bài *MicroRank: End-to-End Latency Issue Localization with Extended Spectrum Analysis in Microservice Environments*, WWW'21; code tác giả `IntelligentDDS/MicroRank` đúng revision T-001 §9; `RCAEval/e2e/microrank.py` đúng revision T-001 §9. Ký hiệu **MR** dưới đây là file trong clone MicroRank gốc; **RE** là file `RCAEval/e2e/microrank.py`. Revision, hash và đường dẫn thật nằm trong manifest của T-015. Bản text toàn văn: `sources/microrank-paper.txt`; ảnh đã kiểm công thức và bảng: `runs/independent-math/paper-pages/`.

## 1. Bài toán và đầu vào

MicroRank xếp hạng service instance (bản chạy cụ thể của dịch vụ) có khả năng gây ra **latency issue**, tức sự cố làm tăng thời gian đáp ứng. Đơn vị tính ban đầu là operation (thao tác) của một instance. Bài §3.1 và §4.1 chia trace (vết thực thi của một yêu cầu) thành bình thường và bất thường, sau đó kết hợp hai nguồn bằng chứng để xếp hạng. Đây không phải mô hình suy ra nguyên nhân vật lý, cũng không tự tạo nhãn vùng ảnh hưởng.

Code gốc cần mỗi span (một thao tác có khoảng thời gian) có `traceID`, `spanID`, `operationName`, `duration`, `startTime`, `references[0].spanID`, `process.serviceName`, các `tags` cho `span.kind` và tên pod/instance. Nó đọc Jaeger qua Elasticsearch, sắp theo trace rồi thời gian (`MR:preprocess_data.py:28–65`). Timestamp truy vấn là millisecond; duration span là microsecond. Ngưỡng và độ trễ đem so được chia 1.000 để thành millisecond (`MR:preprocess_data.py:249–254`; `MR:anormaly_detector.py:56,95`). Nhầm hai đơn vị làm đổi hoàn toàn phân nhóm.

Bản RCAEval nhận bảng span. Nó tạo khóa `serviceName + '_' + methodName`, dùng `operationName` khi `methodName` thiếu (`RE:649–650`). Đây là **service-operation**, khác instance-operation của gốc. Hai service có cùng method vẫn khác nút. Một service có nhiều method thì có nhiều nút. Nối chuỗi bằng `_` có thể va chạm nếu chính các thành phần chứa dấu này; adapter phải kiểm khóa, không được suy service bằng cách cắt tùy tiện.

Metrics và log không tham gia điểm MicroRank. Chúng có thể dùng độc lập để kiểm inventory (danh sách service có quan sát) hoặc giải thích sau xếp hạng, nhưng không được chọn ứng viên bằng nhãn gốc. Cả bài và code không cần nhãn lỗi để học ngưỡng; chúng cần một đoạn trace được coi là bình thường. Gốc khuyến nghị đoạn dài, ví dụ một giờ ở bài §4.2 và `MR:anormaly_detector.py:7–11`; đây không phải bảo đảm một giờ luôn đủ cho mọi operation.

Phân biệt ba bản để tránh gọi nhầm kết quả:

| Tên | Phân nhóm trace | Đồ thị/điểm | Mức tái lập |
|---|---|---|---|
| MicroRank gốc | So độ trễ trace với tổng ngưỡng theo số operation; code phân nhóm dùng μ+σ và cộng 50 ms | Tích lũy cạnh từ các trace thuộc từng nhóm; PageRank và weighted spectrum (phổ có trọng số) | Đối chiếu code gốc; cần kind, root, self-time và instance để chạy trọn |
| MicroRank RCAEval | μ+3σ theo từng span; số trace hai nhóm có thể chồng; đồ thị trước/sau mốc khác tập được đếm | Có lỗi đặt lại danh sách cạnh | T-007 tái lập số của chính bản này |
| **MicroRank-RCAEval sửa đầu vào** (`microrank_rcaeval_fixed_span`) | Giữ detector μ+3σ nhưng mỗi trace thuộc đúng một nhóm; dùng cùng tập trace cho graph và count | Tích lũy cạnh; giữ hàm PageRank/spectrum chính thức | Biến thể sửa adapter; không đồng nhất với toàn bộ MicroRank gốc |

Đoạn μ+3σ và luật gốc được mô tả riêng trong `ho-so-phat-hien-trace.md`. Thiếu `span.kind` không cho phép tự gán mọi span mất cha là root thật hoặc gọi kết quả fixed-span là detector gốc.

## 2. Từng bước xử lý và công thức

### 2.1. Học mức bình thường và phân nhóm

Gọi $h_s$ là handling time (thời gian tự xử lý) của span $s$. Code gốc tính bằng duration cha trừ duration các con trực tiếp đã xuất hiện, rồi lấy trung bình và độ lệch chuẩn theo operation. Nhánh thông thường loại trace khi thiếu tham chiếu/cha trong lúc học hoặc khi duration root sau phép trừ con vượt 1 giây (`MR:preprocess_data.py:143–150,177–225,249–254`). Riêng span đầu của trace mới, nhánh non-frontend có `references=[]` không gán `parentId`, nhưng vẫn đọc nó ở dòng 218: có thể gây `UnboundLocalError` nếu chưa gán trước đó, hoặc đọc parent của trace trước nếu biến đã tồn tại (`:210–221`). Vì vậy thiếu references không luôn chỉ làm loại baseline. AST nguồn và phản ví dụ trạng thái binding độc lập nằm trong `runs/review-response/toy-source-checks.json`; lượt gọi AST gốc tái hiện lỗi được giữ trong LOG phiên 2/N2. Do code trừ tổng duration con, không lấy độ dài hợp các khoảng con, không được gọi đây là self-time đã xử lý đúng mọi trường hợp song song. Đây là điểm cần kiểm trên hệ khác, không tự sửa công thức để số đẹp hơn.

Theo bài §4.2, ngưỡng trace $t$ là

\[
 L_{\mathrm{expected}}(t)=\sum_o c_{to}(\mu_o+1.5\sigma_o),
 \qquad a(t)=\mathbf 1\{L_t>L_{\mathrm{expected}}(t)\},
\]

với $c_{to}$ là số lần operation $o$ xuất hiện trong trace $t$. Bài §4.1 và code dùng chiều $L_t>L_{\mathrm{expected}}$. Câu ngay sau công thức (1) của bài lại viết chiều ngược; hồ sơ giữ chiều có căn cứ nhất quán, ghi lỗi văn bản này thay vì âm thầm chép theo.

Code gốc có **hai luật**: detector hệ thống dùng 1,5σ và báo khi hơn 8 trace bất thường (`MR:anormaly_detector.py:61–73`); hàm chia nhóm RCA dùng

\[
a_{\mathrm{partition}}(t)=\mathbf1\left\{L_t>\sum_oc_{to}(\mu_o+\sigma_o)+50\ \mathrm{ms}\right\}
\]

(`MR:anormaly_detector.py:93–105,120–131`). Không được thay luật thứ hai bằng "chỉ cần một span vượt 3σ" rồi gọi đó là ngữ nghĩa đầy đủ của gốc. Phân nhóm gốc là hai tập rời nhau $T_f$ và $T_p$; các span quan sát được trong cửa sổ của mỗi trace đi vào graph của đúng nhóm đó (`MR:online_rca.py:209–232`).

Chia ở mức trace không tự khôi phục trace đầy đủ. `get_span()` chỉ lấy span có `startTimeMillis` trong cửa sổ (`MR:preprocess_data.py:49–53`). Trace cắt ngang biên có thể thiếu cha, con hoặc root; không được bổ sung span bên ngoài cửa sổ rồi vẫn gọi là cùng đầu vào. Bản sửa T-015 cũng chỉ phân nhóm các span phía sau mốc đang quan sát. Khi cùng trace có span trước và sau mốc, nhóm RCA không chứa phần trước mốc đã dùng học ngưỡng; phải ghi quy tắc đó và đếm trace cắt biên riêng.

### 2.2. Dựng hai đồ thị

Với mỗi nhóm $g\in\{f,p\}$, dựng:

- $O_g$: tập operation xuất hiện trong các trace của nhóm;
- $E_g\subseteq O_g\times O_g$: cạnh gọi cha→con; bỏ trùng cùng cặp;
- $X^g_{ot}=1$: trace $t$ có ít nhất một span của operation $o$;
- $m_t$: số span/operation occurrence trong trace, gồm các operation lặp.

Code gốc tích lũy cạnh ở `MR:preprocess_data.py:436–462`. Mất cha thì span vẫn tạo nút và incidence (quan hệ xuất hiện trace-operation), nhưng cạnh không resolve được bị bỏ (`:455–458`). Một operation không có cạnh gọi vẫn được xếp hạng nếu có incidence với trace. Một service không xuất hiện trong trace không có nút nào; MicroRank không tự thêm service đó từ metric.

Tên biến lịch sử dễ gây hiểu nhầm: `operation_trace` có khóa là **trace** và giá trị là operation; `trace_operation` có khóa là **operation** và giá trị là trace (`MR:pagerank.py:97–110`).

### 2.3. Ma trận và ưu tiên trace

Với $M=|O_g|$, $N=|T_g|$, ba ma trận có **cột là nguồn**, hàng là đích:

\[
A_{jo}=\frac{\mathbf1\{(o,j)\in E_g\}}{\deg^+_g(o)},\quad
B_{ot}=\frac{X^g_{ot}}{\sum_j X^g_{jt}},\quad
C_{to}=\frac{X^g_{ot}}{\sum_r X^g_{or}}.
\]

Cột không có cạnh của $A$ để bằng 0; $B,C$ chỉ có operation/trace có incidence nên mẫu số dương. Matrix gốc dùng `float32` (`MR:pagerank.py:74–79`). Không bỏ quantization (lượng tử hóa số thực) này khi yêu cầu khớp điểm code đến sai số rất nhỏ.

Trace kind (loại trace) trong **code** là nhóm các trace có cột $B_{:t}$ bằng nhau: cùng tập operation duy nhất, bất kể thứ tự gọi hoặc số lần gọi. Gọi $k_t$ là số trace trong loại đó; $K=\sum_t1/k_t$; $S=\sum_t1/m_t$. Ưu tiên trace bình thường là

\[
u^p_t=\frac{1/k_t}{K}.
\]

Ưu tiên trace bất thường **đúng biểu thức code** là

\[
u^f_t=\frac{0.5}{S\left(0.5\,k_t/K+1/m_t\right)}.
\]

Nguồn: `MR:pagerank.py:112–140`. Prior bất thường của code không được chuẩn hóa tổng thành1; không gọi nó là phân phối xác suất. Công thức này không phải công thức (7) trong bài. Bài dùng hỗn hợp cộng $\varphi(1/n_t)/\sum1/n +(1-\varphi)(1/k_t)/\sum1/k$, mặc định $\varphi=0.5$. Vì vậy phải ghi đang kiểm biểu thức code, không gọi tính lại code là đã xác nhận ưu tiên trace của bài.

### 2.4. PageRank ở hai phía

Mỗi nhóm có vector operation $s^{(q)}$ và vector trace $r^{(q)}$. Khởi tạo mọi phần tử bằng $1/(M+N)$. Ở vòng $q$, dùng đồng thời hai vector của vòng trước:

\[
\tilde s^{(q)}=d\left(B r^{(q-1)}+\alpha A s^{(q-1)}\right),\qquad
\tilde r^{(q)}=d C s^{(q-1)}+(1-d)u,
\]
\[
s^{(q)}=\tilde s^{(q)}/\max_o\tilde s^{(q)}_o,\qquad
r^{(q)}=\tilde r^{(q)}/\max_t\tilde r^{(q)}_t.
\]

Code chạy đúng 25 vòng, $d=0.85$, $\alpha=0.01$, không có ngưỡng dừng hội tụ (`MR:pagerank.py:172–192`). $B,C$ truyền trọng số qua coverage; $A$ bổ sung quan hệ gọi. Đây không phải `networkx.pagerank` chuẩn: vector được chia theo **max từng phía** ở mỗi vòng, không chuẩn hóa tổng bằng 1; ma trận khối không được chuẩn hóa lại sau thêm $\alpha A$.

Sau đó code trả trọng số

\[
w^g_o=s^{(25)}_o\frac{\sum_j s^{(25)}_j}{M}.
\]

Do $0\le s_o\le1$, trọng số không vượt 1 nếu cập nhật hợp lệ. Nó không phải xác suất lỗi. Bài §4.4.4 không mô tả phép nhân thêm trung bình này. Code còn đếm $N^g_o=\sum_t\mathbf1\{B_{ot}\ne0\}$, tức số trace **duy nhất** đi qua operation (`MR:pagerank.py:148–163`).

### 2.5. Weighted spectrum và Dstar2

Với operation có ở cả hai nhóm:

\[
e_f(o)=w^f_o N^f_o,\quad n_f(o)=w^f_o(|T_f|-N^f_o),
\]
\[
e_p(o)=w^p_o N^p_o,\quad n_p(o)=w^p_o(|T_p|-N^p_o).
\]

Đây là bốn ô spectrum: có/không xuất hiện × trace bất thường/bình thường. Mỗi ô đếm của operation được nhân với cùng trọng số $w_o$ ở phía tương ứng. PageRank của trace ảnh hưởng gián tiếp tới $w_o$ qua coverage; code không cộng riêng trọng số của từng trace vào ô spectrum. Dstar2 là

\[
\operatorname{susp}(o)=\frac{e_f(o)^2}{e_p(o)+n_f(o)}.
\]

Nguồn code: `MR:online_rca.py:49–86`; công thức spectrum: bài (8); Dstar2: bài Bảng 3. Operation phủ nhiều trace bất thường, ít trace bình thường có xu hướng điểm cao. Nhưng cùng độ phủ vẫn có thể khác điểm do PageRank/call graph, trace kind, scope và phép chuẩn hóa; không quy điểm hoàn toàn cho lưu lượng.

Nhánh thiếu nhóm của code phải được nói riêng. Nếu operation chỉ có ở bất thường, $e_p=n_p=10^{-7}$. Nếu chỉ có ở bình thường, $e_f=n_f=10^{-7}$, $e_p=(1+w^p_o)N^p_o$, $n_p=|T_p|-N^p_o$ (`MR:online_rca.py:62–76`). Nhánh này khác quy tắc bài "đặt PageRank phía thiếu bằng 0,0001". Không đổi nó trong bản sửa hai sai lệch; nếu muốn đổi thì là biến thể khác, cần lý do.

Cuối cùng sắp operation giảm dần điểm, lấy `top_max + 6`; lời gọi mặc định `top_max=5` nên tối đa 11 operation (`MR:online_rca.py:148–153,239–242`; `RE:442–445,699`). Service ranking (thứ hạng dịch vụ) chỉ hình thành sau một bước ánh xạ operation→service rồi bỏ trùng. 11 operation không đồng nghĩa 11 service, cũng không suy ra một trần Hit@5 cố định.

## 3. Đồ thị dùng ở đâu

Đối chiếu vai trò K1 §3 với code, không coi K1 là bằng chứng gốc:

| Vai trò | Có/không và cơ chế |
|---|---|
| Biểu diễn topology (cấu trúc quan hệ) | Có: $A$ là quan hệ gọi operation quan sát từ cha–con span; $B,C$ là quan hệ coverage giữa operation và trace |
| Ngữ cảnh feature cho detector | Trong RCAEval span3σ: không. Trong gốc: quan hệ cha–con dùng khi học handling/self-time cho μ,σ; vì vậy phát biểu tuyệt đối "không quan hệ nào tham gia detector" quá mạnh |
| Đối tượng cần chấm bất thường | Không chấm một graph/subgraph là bất thường; luật trước đó chấm trace |
| Lan truyền điểm nghi vấn | Có: hai cập nhật $B r+\alpha A s$ và $C s$ |
| Giả định causal/conditional (nhân quả/có điều kiện) | Quan hệ gọi là phụ thuộc thực thi quan sát, không là đồ thị nhân quả học được hay bằng chứng can thiệp |
| Xếp hạng ứng viên | Có gián tiếp: PageRank làm trọng số spectrum; Dstar2 tạo thứ hạng cuối |

PageRank nằm **sau detector** ở pipeline bài Hình 5 và code `MR:online_rca.py:156–242`. PageRank không quyết định span/trace có bất thường hay không. Nhưng luật gốc có bước học self-time dựa vào cha–con. Phải phân biệt nguồn quan hệ đó với vai trò đồ thị PageRank để mô tả đúng phát hiện.

## 4. Tham số mặc định và điều kiện chạy

| Tham số/quy ước | Giá trị code gốc | File:dòng | Khác RCAEval/ý nghĩa |
|---|---|---|---|
| `d` | 0,85 | `MR:pagerank.py:172` | hệ số lan truyền, không ngưỡng phát hiện |
| `alpha` | 0,01 | `MR:pagerank.py:172` | trọng số call graph; không tự kết luận tác động nhỏ chỉ từ giá trị nhỏ |
| Iteration | 25 | `MR:pagerank.py:173–179` | số vòng cố định; README khuyên tăng trên hệ lớn |
| Hội tụ | Không có ε dừng | `MR:pagerank.py:179–192` | 25 vòng không chứng minh hội tụ |
| Ưu tiên operation | Không teleport trực tiếp vào operation | `MR:pagerank.py:180–184` | ưu tiên chỉ đi vào trace qua (u) |
| Ưu tiên trace | coefficient 0,5 trong biểu thức code | `MR:pagerank.py:139–140` | khác hỗn hợp cộng φ=0,5 của bài (7) |
| SLO chuẩn hóa | mean/std dân số, chia 1.000, làm tròn 4 chữ số | `MR:preprocess_data.py:249–254` | RE dùng duration trọn span, std mẫu pandas, làm tròn 2 chữ số (`RE:562–563`) |
| Root latency | Tổng duration các `frontend` span `kind=server` trong trace | `MR:preprocess_data.py:311–327` | không tùy tiện dùng max duration của root mất cha |
| Detector hệ thống | Σcount(μ+1,5σ), hơn 8 trace | `MR:anormaly_detector.py:61–73` | comment tỷ lệ1% không khớp điều kiện thật |
| Partition RCA | Σcount(μ+σ)+50ms | `MR:anormaly_detector.py:99–102` | RE là μ+3σ theo span (`RE:666–670`) |
| Cửa sổ detector code | 60 giây, lùi hiện tại 1 phút | `MR:online_rca.py:158–163` | bài §4.1 là 30 giây |
| Cửa sổ RCA code | detect_time−5s đến +55s | `MR:online_rca.py:165–167` | không phải ±300s hoặc ±600s |
| Sau báo động | ngủ 240s rồi vòng ngoài ngủ 60s | `MR:online_rca.py:245–246` | bài §4.2 nói flush 5 phút |
| Spectrum | `dstar2` | `MR:online_rca.py:242` | không đổi công thức theo root rank |
| `top_max` | 5, nhưng trả tối đa 11 operation | `MR:online_rca.py:148–153,239` | phải ghi cả output trọn và output cắt |
| Span window ES | startTimeMillis∈[start,end] | `MR:preprocess_data.py:49–53` | adapter T-007 dùng startTime∈[lo,hi); khác quy tắc biên |
| Hash seed | Không khóa trong tác giả | graph list/set trong RE `636–641` | adapter khóa thứ tự nút/tie; vẫn kiểm hai tiến trình seed0/1 |

Trong T-015, ±600s là cấu hình tham chiếu của T-007 theo WHY-16; ±300s là kiểm độ nhạy được định trước trong SPEC. Bằng chứng cửa sổ baseline trace của tác giả TORAI là gián tiếp. Hai cấu hình này không tự thành cửa sổ P3; Q-54 để việc đó ở tổng hợp G1.

## 5. Chỗ code khác bài, và hai sai lệch RCAEval

### 5.1. Bài và code gốc

1. **Detector và partition khác nhau.** Bài dùng μ+1,5σ; code detector hệ thống tương ứng, nhưng code chia nhóm RCA dùng μ+σ+50ms. Không diễn giải hai luật là một.
2. **Định nghĩa loại trace bị giản lược.** Bài §4.3 nói cùng coverage tree (cây các operation và quan hệ gọi). Code so cột (B), tức cùng tập operation; hai trace cùng operation nhưng cấu trúc gọi khác vẫn một loại.
3. **Prior bất thường khác.** Công thức (7) là cộng hai nghịch đảo đã chuẩn hóa. Code dùng nghịch đảo của biểu thức hỗn hợp ở §2.3. Hai công thức không tương đương đại số. Phản ví dụ không nhãn có hai trace với2 và4 operation duy nhất, mỗi loại xuất hiện1lần: prior bài lần lượt7/12 và5/12, prior code8/9 và4/3 (`runs/independent-math/prior-expression-check.json`). Khi cùng kind count, biểu thức code ưu tiên scope lớn hơn, ngược key insight "scope nhỏ giúp thu hẹp nguyên nhân" của bài. Đây là khác biệt đại số, chưa xác định là lỗi viết nhầm hay một prototype khác bài; tác động tới ranking từng ca còn phải soi, không tự sửa prior trong bản sửa hai sai lệch.
4. **Damping trong bài tự không nhất quán.** Phương trình (3) dùng $(1-d)Av+du$, còn (4) dùng $dAv+(1-d)u$. Code theo (4) trước phép chuẩn hóa max.
5. **Khởi tạo/chuẩn hóa.** Bài §4.4.4 ghi riêng 1/M và 1/N; code khởi tạo1/(M+N), chuẩn hóa max mỗi phía mỗi vòng rồi nhân trung bình vector operation. Không mặc nhiên thay code bằng PageRank chuẩn.
6. **Spectrum phía thiếu.** Bài đặt F/P phía thiếu bằng0,0001; code đặt trực tiếp ô spectrum1e−7, cộng thêm1 vào weight trong nhánh chỉ bình thường.
7. **Cửa sổ.** Bài30s và flush5min; code detector60s, RCA−5/+55s, ngủ240+60s. Vì vậy số WWW'21 chỉ là mốc của giao thức tác giả, không phải mốc khớp bắt buộc của adapter RE2.
8. **Công thức spectrum mặc định.** Bài §5.2 dùng Ochiai mặc định trong thực nghiệm; code `MR:online_rca.py:242` gọi Dstar2. Các bảng bài có cả hai. Ví dụ và bản sửa giữ Dstar2 theo đúng lời gọi code, không chọn sau khi xem điểm. Mốc Dstar2 đã tra trước run; không gán R@2=66% của Ochiai ở datasetB cho Dstar2 (54%). K1 ghi Ochiai/66% là đúng trong ngữ cảnh bài, nhưng không chứng minh đó là lời gọi của revision code đang chạy.

### 5.2. Hai sai lệch RCAEval phải sửa

**Đặt lại cạnh.** `RE:626–627` kiểm `op not in operation_trace`, nhưng từ điển đó có khóa là traceID. Điều kiện gần như luôn đúng; `operation_operation[op]` bị đặt thành `[]` ở mỗi span. Kết quả thường chỉ giữ các con của lần xuất hiện cuối cùng của operation. Gốc kiểm `operation_name not in operation_operation` và tích lũy mọi cạnh của các trace trong nhóm (`MR:preprocess_data.py:436–462`). Sửa tích lũy giúp call graph phản ánh các lần gọi đã thấy thay vì span cuối. Hash order, mất cha, cửa sổ bị cắt và spanID trùng vẫn có thể làm graph khác; không quy mọi khác biệt thứ hạng cho riêng hai dòng đó.

**Nhóm trace chồng và lệch graph-count.** RCAEval tách từng span trước/sau mốc theo `startTime+duration`; sau đó lấy traceID có span dưới/ngang-trên3σ ở phía sau mốc (`RE:654–670`). Một trace có cả span bình thường và bất thường xuất hiện trong cả hai tập. Ngoài ra, graph bình thường dựng từ `normal_df` trước mốc, graph bất thường từ toàn `anomal_df` sau mốc, nhưng total counts là hai tập trace vừa phân theo ngưỡng (`RE:672–702`). Vì vậy $|T_g|-N^g_o$ có thể âm: spectrum không còn cùng một bảng đếm nhất quán.

Bản **MicroRank-RCAEval sửa đầu vào** (`microrank_rcaeval_fixed_span`) sửa hai điểm: tích lũy cạnh theo trace; chỉ chia **một lần ở mức trace**, rồi graph/count dùng đúng trace của nhóm đó. Nó giữ μ+3σ để không tự suy trường kind/root mà parquet không có. Đây là bản sửa giao thức rõ tên; luật phân nhóm μ+3σ vẫn khác `trace_list_partition` gốc. Bản full-original còn cần đầu vào và kiểm riêng. Không dùng số tốt hơn để che khác biệt này.

## 6. Giả định và điều kiện thất bại do tác giả nêu

Bài §5.5 nêu: (a) không định vị được lỗi không làm lệch latency; (b) chất lượng tracing ảnh hưởng độ chính xác, mất quá nhiều trace làm suy giảm; (c) instrumentation có overhead; (d) đây là reactive approach (phản ứng sau khi sự cố xảy ra), chậm hơn cách dự báo chủ động. README mục Notices nêu thêm: detector không phù hợp mọi hệ và có thể thay; hệ lớn cần nhiều vòng PageRank hơn; intermittent failures (lỗi chập chờn) và broken traces (trace đứt) có thể giảm độ chính xác.

Các giả thuyết riêng phải tách khỏi lời tác giả: trừ tổng duration con có thể sai khi xử lý song song; bỏ trace thiếu root/cha có thể làm baseline lệch; window ngắn thiếu operation có thể gây ngưỡng không đủ; top-11 operation có thể giảm coverage service; chỉ latency có thể không thấy lỗi trả nhanh. Cơ chế toán/code cho thấy các đường này khả thi, nhưng chưa đo được tần suất hoặc mức tác hại tổng quát trong P1. Không gọi chúng là kết quả P4.

Service không có cạnh không đồng nghĩa không xếp hạng: nếu operation có trong trace thì $B,C$ vẫn truyền trọng số. Service vắng trace mới không có node/score. Với tập ca $\mathcal D$ và tập service ứng viên thực $C_i$, trần coverage là

\[
\operatorname{Hit@k}\le\frac1{|\mathcal D|}\sum_{i\in\mathcal D}\mathbf1\{r_i\in C_i\},
\]

với $r_i$ là nhãn gốc, **chỉ đọc sau lưu ranking**. Nếu cắt top-11 operation trước mapping, dùng tập $C_i^{11}$ để nêu trần của output đã cắt. Không coi trần đó là thuộc tính chung của MicroRank, và không suy nó từ số operation đơn thuần. Census TT phân biệt vắng trace, không có cạnh liên service, không có cạnh operation nào, và rơi khỏi danh sách cắt. Trên ca auth đã chọn, auth không có cạnh liên service nhưng vẫn ở hạng service 9 của danh sách đầy đủ; nó có hai cạnh operation nội bộ. Operation assurance không có cạnh ở cả hai nhóm vẫn được chấm và ở hạng operation 152. Không có service vắng mọi cạnh operation trong riêng ca này; toy không cạnh kiểm điều kiện đó riêng. Service có metric nhưng vắng trace không được thêm vào output. Nguồn: `runs/tt-local/auth/primary-summary.json`, `runs/tt-independent-math/auth/spectrum-scores.csv`, `runs/independent-math/toy-isolated/`.

## 7. Ví dụ tính độc lập trên ca dev Train Ticket

SPEC chọn trước `re2tt_ts-auth-service_cpu_1`; ca dự phòng cố định là `re2tt_ts-route-service_mem_1` khi ca đầu không đủ evidence. Cách chọn này không nhìn root rank. Script `scripts/independent_math.py` đọc graph snapshot của adapter, tự dựng $A,B,C,u$, chạy 25 cập nhật operation/trace, tính trọng số, bốn ô spectrum và Dstar2. Nó không import hoặc gọi hàm tác giả.

Kết quả phải khớp mọi operation weight, trace count, mọi ô spectrum và score của hàm PageRank/spectrum chính thức, với sai số tuyệt đối và tương đối không quá1e−10. Chứng nhận này có điều kiện: graph snapshot là đầu vào của cả hai, nên tự nó không kiểm độc lập chất lượng partition/graph builder. Các phép kiểm toy và census phải kiểm phần đó riêng. Hai vector không được gọi là đã hội tụ chỉ vì đủ25 vòng; file `*-iterations.csv` ghi thay đổi max của từng vòng.

Ví dụ TT đã hoàn thành trong `vi-du-tinh-tay.md`: graph bình thường có 146 operation/191 cạnh/1.326 trace; graph bất thường có 152 operation/199 cạnh/1.403 trace. `scripts/independent_inputs.py` dựng lại ngưỡng, partition và bốn quan hệ graph từ raw span; 19 phép đối chiếu ban đầu đạt (`runs/tt-independent-inputs/auth/comparison.json`). Tái tính độc lập có 4.383 phép so prior, operation PPV, weight/count/spectrum/score đều sai số tuyệt đối và tương đối bằng 0 (`runs/tt-independent-math/auth/summary.json`). Lỗi nhận token null `<NA>` trong audit gốc của T-015 được phát hiện sau đó; nó đổi cách đếm root/missing-parent, không đổi graph hoặc điểm. Vì cả hai builder cùng thiếu token này, 19 PASS không tự chứng minh ngữ nghĩa null đúng. Audit raw sửa cho root bình thường/bất thường1.326/1.403 và missing-parent0/0; bốn quan hệ graph mỗi phía khớp tuyệt đối (`runs/root-audit-correction/auth/audit-correction.json`). Probe quan sát biến trả về của `official.pageRank` không sửa source:2.729 trace PPV và298 operation PPV khớp0 (`runs/tt-trace-vector-probe/auth/summary.json`). 298 operation là kiểm lặp, không cộng thành số giá trị khác nhau.

Operation `ts-station-service_find ts.station` có điểm 75,29594619687462 và hạng 1. Chỉ sau lưu ranking mới đọc nhãn: service gốc auth có operation tốt nhất ở hạng 26, điểm 19,925789676987726; service auth ở hạng 9 trong danh sách đầy đủ và bị loại khỏi 11 operation trả về. Auth có PageRank operation bằng 1 ở cả hai phía, nhưng ep+nf lớn hơn station: PageRank cao không tự bảo đảm Dstar2 cao. Mọi ô, từng bước ma trận/prior và phép thay số nằm trong ví dụ, lấy từ file kết quả.

Phải nối bước chia nhóm với các ô phổ trên. Gọi $D_s=\mathrm{duration}_s/1000$ (ms); luật của biến thể là $a(t)=\mathbf1\{\exists s\in t:\ D_s\ge\mu_{o(s)}+3\sigma_{o(s)}\}$. Thêm span tạo thêm cơ hội bị cờ; nếu các cờ độc lập và cùng xác suất $p$ thì $P(a(t)=1)=1-(1-p)^{m_t}$. Đây chỉ là minh họa cơ chế, vì span thật có thể tương quan và operation có phân phối khác nhau. Tái đếm từ ba snapshot cho thấy nhóm bất thường có trace dài hơn rõ rệt:

| Ca dev | Trung vị span normal / anomaly | Trung bình span normal / anomaly | Trace ≥100 span normal / anomaly |
|---|---:|---:|---|
| auth CPU | 5 / 179 | 54,22 / 293,08 | 348/1.326 (26,24%) / 903/1.403 (64,36%) |
| route mem | 5 / 179 | 10,40 / 213,19 | 7/1.038 (0,67%) / 1.047/1.277 (81,99%) |
| route socket | 5 / 179 | 5,77 / 424,44 | 2/1.130 (0,18%) / 1.167/1.435 (81,32%) |

Nguồn: `runs/review-response/trace-length-stats.csv`, dựng lại bằng `scripts/check_review_diagnostics.py` từ đúng ba `example.json`, không chạy lại phương pháp. Ở auth, 903 trace dài bất thường và 903 trace chứa operation station chỉ bằng số lượng; giao là 866, mỗi tập có 37 trace riêng. Hợp mọi operation auth có 439 trace bất thường, không giao 903 trace dài quan sát. Vì vậy sự liên hệ giữa độ dài, loại trace và grouping đi vào coverage của spectrum trước khi chấm điểm. Dstar2 không trực tiếp dùng độ dài; prior bất thường của code cũng tăng theo $m_t$ khi giữ $k_t$ cố định (§2.3). Chưa có ablation để kết luận độ dài chi phối điểm hơn nguyên nhân lỗi, hoặc quy riêng auth hạng 9 cho đồ thị. Workload drift (thay đổi thành phần tải), thiếu span/instrumentation, ngưỡng theo operation và tài nguyên dùng chung còn là khả năng khác chưa kiểm. Vắng operation auth trong trace quan sát không đủ để loại mọi ảnh hưởng gián tiếp của auth. Đây là giới hạn của CANDIDATE, không là kết luận P4.

Vòng 25 còn max thay đổi operation/trace 0,598831/0,347665 phía bình thường, 0,539508/0,550659 phía bất thường (`*-iterations.csv`). Probe trên cùng snapshot auth dùng số vòng **25/26/50/100/101 cố định trước kiểm**: 25 khớp mọi score đã lưu, sai số tuyệt đối và tương đối 0; 26/50/100 đổi top 11; 101 giữ top 11 nhưng đổi thứ hạng đầy đủ. Ngay 100/101 vẫn còn thay đổi operation lớn, nên chưa có bằng chứng hội tụ. Nguồn: `runs/review-response/iteration-probe.json`. Giữ 25 để khớp code đã chọn; không chọn số vòng theo root rank hoặc theo điểm tốt hơn. Đây là độ nhạy của một snapshot, không là tần suất trên dataset.

Control nghiêm với hai cửa sổ kết thúc trước mốc tiêm thật vẫn có 2.814/242.818 span bị cờ (1,16%) và 570/1.433 trace bất thường (39,78%), trả 11 operation. Ca auth có lỗi có 5.036/483.077 span bị cờ (1,04%) và 1.403/2.729 trace bất thường (51,41%). Nguồn hai tỷ lệ cạnh nhau: `runs/review-response/trace-length-stats.csv`; nguồn control gốc: `runs/tt-local/auth/two-normal-summary.json`. Đây là false alarm trên control, không phải nguyên nhân có nghĩa. Baseline control khác độ dài và thành phần, nên không dùng chênh tỷ lệ này đo hiệu quả phân biệt sự cố. Chưa đo false alarm, mức ảnh hưởng của độ dài hoặc hội tụ tổng quát trên dataset trong P1.

Phép kiểm trước khối OB đầy đủ đã hoàn thành: snapshot pilot `runs/pilot/re2ob_checkoutservice_cpu_1.json` được tái tính độc lập; 327 so sánh weight/count/spectrum/score có sai số tuyệt đối và tương đối0. File `runs/independent-math/ob-pilot-rerun/summary.json` ghi kết quả; 9 file trung gian/kết quả của lượt đầu và chạy lại giống từng byte (`ob-pilot-repeat-check.json`). Lượt đầu chỉ lỗi in tên tiếng Việt ở console Windows sau khi toàn bộ artifact đã ghi; giữ `ob-pilot/console-failure.json`, sửa output console và chạy lại đích mới. Đây là kiểm lõi số học trên graph pilot, chưa thay cho ví dụ TT hoặc kiểm tất cả ca.

Mốc WWW'21 đã tra **trước chạy T-015** trong `runs/independent-math/published-before-run.json`. Dstar2 của MicroRank trên datasetA có R@1/3/5=94/96/96%; datasetB có hai gốc nên báo R@2/3/5=54/68/72%; datasetC=100/100/100% (bài Bảng4–6, trang9). Đây là các dataset/giao thức khác RE2. Trong giới hạn task không có dữ liệu thô của các dataset tác giả để tái lập toàn bảng; thiếu phép tái lập đó làm yếu kết luận về tái lập **bài gốc**, không cản kiểm chính xác công thức code. Bảng7 thời gian PageRank5,5s là overhead tác giả trên cấu hình riêng, không là thời gian chính thức của laptop/EC2 đang chia sẻ.

## 8. Đường nhãn có thể lọt vào phương pháp

Mốc tiêm lỗi đi vào cửa sổ và phép chia trước/sau của RCAEval. Nó là đầu vào hợp lệ khi chạy **biết trước thời điểm**, không hợp lệ để gọi là tự phát hiện. Tên thư mục có service gốc/loại lỗi chỉ được lớp I/O dùng tìm file/lưu file; không truyền vào lõi, chọn root, chọn operation, chọn SLI hoặc threshold. Chấm và giải thích root rank là các bước sau khi điểm/ranking đã lưu.

Các đường rủi ro khác: loại service không có trace bằng cách biết danh sách root; tự chọn ingress từ root bị tiêm; học ngưỡng trên toàn ca gồm đoạn lỗi; chọn window/top_max/iterations sau khi thấy root rank; chọn biến thể vì Hit@k cao hơn; dùng tên ca quyết định cách repair span. Adapter phải xuất record cấu hình và trạng thái lỗi, không biến output rỗng thành thứ tự cột. Nhãn không được dùng giải thích rằng một graph thiếu cạnh là đúng.

## 9. Yêu cầu khi chạy trên dataset khác và đề xuất P3

Dataset mới phải xác minh: duration/start unit; startTime, duration và mốc cửa sổ đều hữu hạn, duration không âm; parent có cùng trace; dữ liệu bình thường đủ phủ operation; root latency và kind; instance/pod nếu muốn xếp instance; trace không bị cắt nhiều ở window; stable operation identity; ID trùng phải cùng nội dung quan sát, bản sao giữ số lần xuất hiện; ID trùng khác nội dung bị từ chối; ánh xạ operation→service; cách xử lý ngưỡng thiếu và nhóm rỗng. Adapter từ chối thời gian NaN/Inf trước split/ngưỡng (`src/microrank/__init__.py:35–37`); root duration đưa vào hai luật gốc cũng phải hữu hạn không âm (`src/microrank/detectors.py:9–13`), vì NaN có thể làm phép so trả False rồi bị coi là bình thường. Điểm cuối hữu hạn không chứng minh đầu vào hợp lệ: trước sửa guard, toy span+Inf vẫn có thể tạo score hữu hạn. Sau sửa, 27 kiểm guard/toy đều đạt; input hợp lệ giữ kết quả chính xác (`runs/review-response/guard-tests.json`). Quét thời gian nguồn và cửa sổ của 90 OB + 3 TT đã chạy cho 0 dòng thời gian sai, hash nguồn đều khớp (`runs/review-response/ec2-second/input-time-audit/summary.json`); không chạy lại ranker, không gán toy thành số cũ sai. Operation vắng baseline không thể được lấp threshold bằng service nhãn. Một trace có nhiều root cần quy tắc latency phù hợp hệ; gốc chỉ cộng các frontend-server span, không định nghĩa chung cho mọi root. Service không trace không thể được MicroRank tự chấm; thêm điểm từ metric là phương pháp khác, không repair thuần giao thức.

Chi phí code gốc đáng chú ý: ma trận $B,C$ dày tốn $O(MN)$ RAM; nhận diện kind bằng so cột từng cặp tốn $O(N^2M)$ ở trường hợp xấu nhất, ngoài 25 lần nhân ma trận-vector. Vì vậy quy mô Train Ticket phải kiểm trực tiếp; thời gian OB không đủ chứng minh TT khả thi. Ca TT auth có 957.209 span trong cửa sổ, method ghi 7,483s và thời gian bên trong worker 14,312s (`runs/tt-local/auth/primary-worker.log`); supervisor đo toàn tiến trình 14,653s (`run-ledger.csv` cùng thư mục). Đây là thời gian quan sát, không phải benchmark đối chiếu với 5,5s PageRank của bài. RSS được lấy mẫu theo heartbeat nên không tự là đỉnh RAM. Mốc chi phí công bố và đo task này phải tách; đo khi EC2/laptop có việc khác chỉ phản ánh chi phí quan sát.

**CANDIDATE cho P3:** dùng ngữ nghĩa code gốc khi dữ liệu đủ và đã kiểm; khi chỉ có schema span của RCAEval, dùng tên rõ **MicroRank-RCAEval sửa đầu vào** (`microrank_rcaeval_fixed_span`), cùng record detector/partition khác gốc, để tránh graph-count âm và mất cạnh. Giữ bản RCAEval cũ chỉ làm mốc tái lập T-007, không dùng sai lệch biết rõ làm cơ sở giải thích cơ chế. Lý do là QT2 và tính nhất quán của spectrum; không dựa vào bản nào cho điểm cao hơn. (chờ WHY, xem `de-xuat-tai-lieu-chung.md`.)

Phạm vi chạy TT là **3/30 ca dev** đã nêu, chưa kiểm 27 ca còn lại. Cap 1 GB tính cả sao chép là diễn giải bảo thủ của người làm, không phải Minh chốt thu 30→3. Đây là thu hẹp kế hoạch round-robin trong SPEC; census footer 30 ca không thay cho chạy phương pháp trên 30 ca. Bằng chứng cấu trúc/code và toy giữ node không cạnh vẫn có giá trị, nhưng các số coverage/rank/length chỉ thuộc ba ca. CANDIDATE chưa được kiểm mức phù hợp detector trên toàn dev; mở rộng phần đó do Minh quyết, không tự chuyển P1 thành benchmark P3 hay phân tích P4.

Điều này chưa tự chốt cửa sổ P3 hoặc quy tắc mapping/candidate; G1 phải quyết cùng điều kiện đầu vào, dataset và ngân sách. Minh đã duyệt gọi bản chạy là **MicroRank-RCAEval sửa đầu vào**, đồng thời yêu cầu đánh giá khả thi và chi phí suy kind/root/pod không nhãn để dùng detector/code gốc; không cài nhánh suy trong T-015. Vì vậy phần chạy này không chứng minh tái lập toàn bộ trace partition gốc. Quyết định lựa chọn P3 và xử lý đầu vào gốc thuộc G1.

### 9.1. Khả thi và chi phí suy kind, root, pod không dùng nhãn

**Phạm vi Minh duyệt:** chỉ đánh giá; không cài hoặc đưa trường suy vào phương pháp ở T-015. Footer của cả30 ca dev trong whitelist đã được kiểm riêng; tất cả cùng11 cột: `time`, `traceID`, `spanID`, `serviceName`, `methodName`, `operationName`, `parentSpanID`, `startTimeMillis`, `startTime`, `duration`, `statusCode`. Không ca nào có `span.kind` hay pod/instance. Nguồn: `runs/independent-math/tt-schema-assessment.json`, chỉ đọc metadata, không chạy phương pháp hoặc mở ca ngoài whitelist. Bảng dưới dựa trên yêu cầu thật của code gốc, không dựa vào tên service gốc của ca.

| Trường | Có thể suy từ11 cột không? | Chi phí và điều chưa đủ |
|---|---|---|
| Root cấu trúc | Có thể tìm span không có parent trong cùng trace bằng khóa `(traceID,spanID)`. Đây là root quan sát được | Một lượt dựng chỉ mục và một lượt resolve: $O(S)$ thời gian/RAM cho $S$ span. Parent không resolve có thể là true root, span cha bị lấy mẫu mất, hoặc cửa sổ cắt mất cha; bảng span không phân biệt được ba nguyên nhân |
| Root latency theo gốc | Cần thêm xác nhận ingress từ cấu hình/instrumentation độc lập nhãn | Gốc chỉ cộng span `frontend` và `kind=server`; dùng max duration hoặc tổng root cấu trúc là luật khác. Multi-root có thể là nhiều yêu cầu, async hoặc trace chưa đủ; số liệu latency suy không được bảo đảm bằng structural root |
| Span kind | Có thể gợi ý từ quan hệ caller/callee hoặc tên method, chưa xác minh | Áp luật tên cột/operation là chi phí tuyến tính thấp; thiếu gold kind khiến không đo được lỗi suy. CLIENT/SERVER thường cùng operation, có thể có INTERNAL/PRODUCER/CONSUMER; chỉ parent và tên không nhận diện duy nhất |
| Pod/instance | Không nhận diện duy nhất từ `serviceName` | Nhiều pod cùng service có thể sinh bảng span giống hệt khi field instance bị bỏ. Không thuật toán nào phục hồi chắc chắn danh tính mất mà không có metadata triển khai, host hoặc exporter. Gán pod=serviceName giảm đơn vị xếp hạng thành service, không tái lập instance của gốc |
| Handling/self-time | Có thể tính biểu thức duration−Σduration(con) bằng parent nếu trace đủ | Chi phí $O(S)$ nếu indexed. Nhưng trace thiếu cha/con và child spans song song làm biểu thức khác handling time thật; có thể âm. Không được sửa sang union các khoảng rồi gọi là code gốc nếu chưa quyết biến thể |

Về chạy phần mềm, có thể dựng cấu trúc Jaeger `_source/references/process/tags` từ bảng, nhưng việc điền `tags.kind` và `tags.name` là chỗ không có bằng chứng. Code gốc còn hard-code `frontend`, lọc root duration sau phép trừ con ở ngưỡng 1s, sắp trace/time, trừ duration con, dùng std dân số và làm tròn 4 số. Trong ca TT auth đã kiểm, inventory không có service tên `frontend`; giữ nguyên điều kiện frontend-server không tạo latency trace như gốc mong đợi (`runs/tt-local/auth/primary-summary.json`; `MR:preprocess_data.py:311–327`). Đổi ingress hoặc gán tag cần một quy tắc đã được xác minh. Chạy hết mà không lỗi sau khi điền các tag đoán không chứng minh đúng cơ chế.

Adapter cho nhánh gốc còn phải xác định hành vi `references=[]` ở span đầu trace mới. Nhánh non-frontend của code học SLO có thể đọc `parentId` chưa gán hoặc còn từ trace trước (`MR:preprocess_data.py:210–221`; `runs/review-response/toy-source-checks.json`). Điền structural root không đủ để hứa chạy được detector gốc: cần policy references và kiểm riêng, cùng miền thời gian/root duration hữu hạn. T-015 chỉ đánh giá khả thi, chưa cài adapter suy schema hoặc sửa clone gốc.

Chi phí scan và viết bộ chuyển đổi là hữu hạn, thấp hơn bước PageRank dày về độ phức tạp. Payload trace của30 ca dev đã có tổng548.755.287 byte, 22.834.238 span theo footer; mỗi ca từ125.465 đến1.535.674 span. Không cần tải lại; chỉ đọc footer thì rẻ hơn full scan. Bước root cấu trúc vì vậy xử lý 22.834.238 hàng nếu quét toàn30ca. Chưa có số thời gian chính thức cho nhánh suy kind/pod: máy đang dùng chung, và nhánh đó chưa được cài theo phạm vi đánh giá của Minh. Số đọc metadata không phải thời gian chạy detector/code gốc. **Chi phí xác minh** mới là yếu tố quyết định: cần nguồn kind/instance thật hoặc metadata instrumentation, rồi kiểm lỗi suy trên dev; T-015 không được tải/đọc thêm ca TT ngoài whitelist. Thời gian scan trên máy dùng chung chỉ là quan sát, không là benchmark chính thức. Thiếu gold kind/pod làm yếu kết luận "dùng được code/detector gốc", dù census root cấu trúc làm được. Nguồn kích thước và schema: `runs/independent-math/tt-schema-assessment.json`.

Đề xuất G1: nếu source dataset có kind/instance thật thì viết adapter minh bạch và kiểm code gốc; nếu chỉ có11 cột, giữ **MicroRank-RCAEval sửa đầu vào** ở đơn vị service-operation. Phương án thứ ba là định nghĩa detector trên root/self-time suy, nhưng đó là biến thể khoa học mới, cần WHY và kiểm riêng, không là công việc đã triển khai. Không dùng root label để chọn ingress, method hoặc pod giả. (chờ WHY, xem `de-xuat-tai-lieu-chung.md`.)

## Biến thể TraceRCA bản RCAEval

TraceRCA trong RCAEval dùng span duration, reference gồm span kết thúc trước mốc và ngưỡng μ+3σ; nó không dùng đồ thị. Gọi $a_o$ là số span bất thường của operation $o$, $n_o$ là số span sau mốc của operation đó và $A$ là tổng span bất thường. Điểm là harmonic mean (trung bình điều hòa) của support $a_o/A$ và confidence $a_o/n_o$, rút gọn thành $2a_o/(A+n_o)$ khi $a_o>0$. Cách này khác Jaccard và khai phá theo trace của code TraceRCA gốc. Xem đối chiếu file:dòng và ví dụ độc lập trong `tracerca-rcaeval.md`.

Operation không có bằng chứng bất thường tạo NaN. Code có ý bỏ NaN, nhưng bỏ sau `sorted` làm hỏng thứ tự điểm. Artifact T-007 đã được tái dựng trong `runs/tracerca-audit/seed0/t007-audit.json`: 90 ca có NaN, 79 ca có ít nhất một cặp điểm hữu hạn tăng lên trong danh sách trả về. Adapter **CANDIDATE** phải lọc giá trị hữu hạn trước khi sắp, dùng tên operation cho tie ổn định, giữ trạng thái `NO_ANOMALY` với danh sách rỗng và coi thiếu baseline là lỗi đầu vào. (chờ WHY, xem `de-xuat-tai-lieu-chung.md`.)

Đây không phải ablation (loại riêng một thành phần) chỉ bỏ đồ thị của MicroRank: detector, spectrum, đơn vị tính điểm và giới hạn output cũng khác. Vì vậy chênh giữa hai phương pháp không xác định riêng lợi ích của call graph hoặc PageRank. Luật phát hiện và điều kiện chạy được trình bày trong `ho-so-phat-hien-trace.md`.


### 9.2. Kết quả đối chiếu từng ca và policy bản sao

`so-sanh-tung-ca.csv` có90hàng, dùng đúng mốc T-007 L20±600s đã lưu và90đầu ra hợp lệ của biến thể. Không có điểm trung bình để chọn bản. Mỗi hàng chứa hai danh sách operation/service, hạng root đọc sau prediction, counts, overlap và cơ chế graph-count. `runs/ob-comparison-check-final.json` kiểm hữu hạn/không âm, counts cùng nhóm và output không rỗng. Phép so là thay đổi kết hợp grouping, tích lũy cạnh, canonical ordering và parent lookup theo trace; chưa có ablation để gán riêng từng chênh lệch cho một sửa.

Hai ca recommendation_loss_1/_2 ban đầu bị guard từ chối. Chẩn đoán tất cả11cột cho48/99key trùng hoàn toàn, không conflict (`runs/duplicate-input-audit/summary.json`). Gốc dùng một lookup `temp[spanID]` nhưng append `pr_trace` mỗi doc (`MR:preprocess_data.py:398–449`). Bản sửa giữ mọi row trong detector/SLO RCAEval và occurrence prior; chỉ lookup cha dùng một identity. Đây không phải nói SLO gốc cũng giữ bản sao: preprocessing SLO gốc duyệt dict span duy nhất. Conflict measurement bị từ chối là guard bổ sung, khác last-wins của gốc. Toy duplicate so AST gốc đạt cả4relations; hai rerun độc lập8.328/9.345so sánh khớp0. Failure và bảng so ban đầu được giữ ở `runs/ob-block-3/` và `runs/so-sanh-tung-ca-before-duplicate-policy.csv`. Lý do sửa ghi trước ranking mới, theo cơ chế (chờ WHY, xem de-xuat-tai-lieu-chung.md).

`kiem-cua-so-ob.csv` so hai ca định trước ở±300/±600s; thay cửa sổ đổi số trace và điểm. T015 dùng±600s để đồng nhất T007 L20 và WHY16; kết quả này không chốt cửa sổ P3. `kiem-ung-vien-tt.md` và204dòng `bang-ung-vien-tt.csv` phân biệt inventory, trace, graph, rank đầy đủ và top11 trên3ca TT, không suy trần cho30ca.
