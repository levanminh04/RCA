# V8 — Checklist và đọc nhanh phương pháp

EXECUTE evidence-only. Hợp sáu bảng: 42 hàng; header audit riêng. Không chọn phương pháp, dataset hay protocol. Danh sách đã chốt là T001 §8 theo Q37/Q38; SPOT không dùng, GDN chỉ detector. T013 dùng bản sau R1/N1–3.

Checklist đầy đủ từng variant/detector: `method-checklist.csv`; nguồn cơ chế, defaults, paper/code, giả định, tính tay và ledger đều giữ riêng.

## BARO

Học trung vị và IQR của từng metric trên đoạn bình thường. Bản DataFrame xếp bằng max độ lệch có dấu ở hậu sự cố; giảm mạnh có thể thành điểm âm. Bài viết trị tuyệt đối. Nhánh dict lại lấy abs(max(post)-median), quartile theo chỉ số, nên cũng không đồng nhất. Không dùng đồ thị. N-Sigma RCA thay robust scale bằng mean/std dân số; detector N-Sigma là thuật toán khác. Cần mốc ngoài. Hai cửa sổ bình thường và lỗi quyết định tập cột sau bỏ hằng. Các ca T013 là kiểm cơ chế/tái lập, không chọn cửa sổ P3.

Nguồn ghim/hồ sơ: `results/T-013/ho-so-baro.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## BOCPD

Bộ phát hiện điểm đổi giữ phân phối runlength và dùng mô hình Student-t đa biến với hazard1/50, kappa1, nu=d+1. Wrapper tìm điểm đổi từ bước nhảy mode runlength. Đầu ra là chỉ số hàng, không timestamp. Code minmax toàn đầu vào nên nhìn tương lai; cắt quanh injection không hợp tự phát hiện. Ma trận T×T làm chi phí tăng theo bình phương chiều dài, còn phép toán covariance phụ thuộc số cột. Chưa có bảo đảm lượng bình thường tối thiểu hoặc calibration chung.

Nguồn ghim/hồ sơ: `results/T-013/ho-so-bocpd.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## N-Sigma

RCA: StandardScaler ddof0 trên nền, lấy max có dấu ở hậu và gộp metric về service. Detector BR: bắt đầu từ index100, nền expanding quá khứ, std mẫu ddof1 và so abs deviation>3std; trả timestamps theo cột có thể trùng và chưa sắp. Đây là hai vai trò riêng. Đã kiểm phép tính hai ca và các edge cases, chưa chứng minh false alarms trên regime bình thường độc lập.

Nguồn ghim/hồ sơ: `results/T-013/ho-so-nsigma-phat-hien.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## CIRCA

PC học quan hệ metric từ chính bảng ca; kiến trúc dựng quan hệ T/S/L/E từ call graph normal hoặc cấu hình. RHT dự báo metric bằng các cha rồi chuẩn hóa phần dư và lấy max trị tuyệt đối. DA truyền evidence từ con; threshold3 không cắt output ranking. T014 tham chiếu linear RHT interval1s khác bản empirical SVR sigmoid+DA và CaseData default1min. PC có SCC/cạnh hai chiều và lỗi wrapper có thể trả thứ tự cột. Mỗi nguồn graph/scorer/mapping là một biến thể riêng, không cô lập nguồn graph chỉ bằng so hai bảng điểm. Cần mốc ngoài, không detector sự cố.

Nguồn ghim/hồ sơ: `results/T-014/ho-so-circa-pc.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## MicroRank

Chia trace thành hai nhóm, dựng call graph operation và quan hệ trace-operation. PageRank đồng bộ hai vector25vòng với d=.85 alpha=.01, chuẩn hóa theo max từng phía; trọng số operation nhân mean của vector. Trọng số đi vào bốn ô spectrum và Dstar2=ef²/(ep+nf). Code gốc khác công thức prior cộng của bài, khác định nghĩa trace kind và detector/partition. RCAEval dùng span μ+3σ, có nhóm chồng và đặt lại cạnh; bản T015 sửa đầu vào giữ PageRank/spectrum. Gốc dùng handling-time trừ tổng con, chưa xử lý hợp khoảng con song song. Thiếu service trong trace thì không tự thêm root. Các fixture và ca đã chạy có số học độc lập.

Nguồn ghim/hồ sơ: `results/T-015/ho-so-microrank.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## TraceRCA

Bản gốc dùng reference latency/status của lời gọi và kết hợp support/confidence qua trace; bản RCAEval không tương đương cả pipeline. RE lấy operation anomalous theo μ+3σ rồi tính support/confidence, không PageRank. Khác MicroRank thêm vai trò detector và độ dài đầu ra nên không quy chênh lệch riêng cho graph. Cần reference cho từng operation hiện tại; thiếu/NaN không được thay bằng thứ tự cột.

Nguồn ghim/hồ sơ: `results/T-015/tracerca-rcaeval.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## Detector trace

Span μ+3σ của RE dùng inclusive duration, std mẫu và tối thiểu2span nền/operation. Luật MicroRank gốc học μ/std handling-time, alarm so root latency với tổng count(μ+1.5σ), báo khi>8trace; partition RCA lại μ+σ+50ms. Gốc code query60s nhưng bài30s. Thiếu root kind, instance và xử lý span cắt biên không cho phép tuyên bố đã cài đủ detector gốc.

Nguồn ghim/hồ sơ: `results/T-015/ho-so-phat-hien-trace.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## TORAI

Code tính max|z| của metric/log/trace, chuẩn hóa theo tổng từng nguồn, gom service thành vector4chiều. GMM thử k1..n chọn BIC, gán cứng và xếp cụm bằng mean severity. RCD trong cụm thêm F=normal/fault và dùng kiểm CI để xếp biến, nhưng fallback severity khi không xếp đủ service. Gốc metric stride15 hai lần; bản sửa bỏ lần hai và ghép theo vị trí. Code thiếu FineGrainer, không đưa trace vào RCD và khác gán mềm bài. TORAI không tự phát hiện; nhãn root không fit nhưng regime boundary bắt buộc. Seed theo ca, chưa chốt windowP3.

Nguồn ghim/hồ sơ: `results/T-016/ho-so-torai.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## RCD

Ghép normal/fault và F-node, rời rạc hóa kmeans tối đa5bin, Ψ-PC chỉ kiểm cạnh kềF bằng chi-square. Pha1 hoán vị và nhóm5biến với alpha.01; pha2 alpha.001 tăng.1 tới<1. Xếp p-value theo list Python khác max(P) trong bài. RE không đặt seed; gốc420. RCD đối chứng metric không gom cụm/không giảm mẫu nên khác TORAI nhiều bước. Đòi causal sufficiency/faithfulness và đủ mẫu; output có thể thiếu biến và root, denominator phải giữ.

Nguồn ghim/hồ sơ: `results/T-016/ho-so-torai.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## SimpleRCA (M4 theo mô tả bài)

Bản độc lập theo mô tả, không code tác giả. Metric mỗi point>mean+3std0 là một alert; trace mỗi service một phiếu nếu P95incident>3P95normal; log substringERROR/FAIL/EXCEPTION một count/dòng và phiếu nếu count>0. Cộng phiếu về service, giữ tie groups và zero-score abstain. Events/channels, P95, trace factor2/4, log thresholds và half600 là các quy ước/biến thể riêng; không chọn bằng accuracy. Giữ observed-service union kể cả normal-only log score0. Rules này chưa là detector streaming đã calibration. TypeI/II của bài là luật phân loại riêng, không accuracy SimpleRCA.

Nguồn ghim/hồ sơ: `results/T-017/ho-so-simplerca.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## GDN (d-ailin/GDN@9853899)

Detector dự báo metric từ cửa sổ5tick và top-k neighbors học bằng embedding, rồi chuẩn hóa residual theo median/IQR và smoothing4tick; anomaly hệ thống=max metric score. Không xếp root. Default reportbest chọn threshold theo nhãn test; reportval bỏ đường đó nhưng score vẫn dùng thống kê test tương lai. T018 cố định317cột dev và dùng thống kê validation; normal held-aside trong dev vẫn báo45–100%tick. Học normal dùng injection của dev để lấy720point/ca;1/5/10ca là12/60/120phút1s, không bảo đảm đủ. Window5ticks không nghĩa5giá trị độc lập vì cột lặp.

Nguồn ghim/hồ sơ: `results/T-018/ho-so-gdn.md`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.

## Kiểm sâu khóa bằng seed trước đọc

MicroRank T015 và TORAI T016 đã khóa ở LOG T020. `deep-source-audit.md` ghi đối chiếu nguồn gốc; `runs/` giữ phép tính lại. MicroRank replay fixture không mở telemetry. TORAI kiểm arithmetic từ kết quả đã chạy, không gọi pipeline/CI mới; giới hạn không tái chạy toàn Psi-PC.

## Từng biến thể và từng bộ phát hiện

Mỗi đoạn sau giữ đúng biến thể của bảng nguồn. Các quy ước chưa kiểm nằm nguyên văn trong CSV; đoạn đọc nhanh không thay hồ sơ đầy đủ.

### BARO — BR DataFrame RobustScorer

Đầu vào: metric numeric. Đơn vị: metric; gộp service bằng max/dedup. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không. Mốc: cần điểm tách; injection chỉ chế độ a hoặc detector hợp lệ. Nền tối thiểu: nền/hậu >=2 và metric không hằng mỗi nửa để còn candidate; đủ thống kê chưa tác giả bảo đảm. Defaults: RobustScaler median IQR25-75; dk=False; max signed. Adapter dataset mới: chua_kiem. Nguồn: results/T-013/yeu-cau-dau-vao.csv:2 và method-checklist.csv.

### BARO — RE DataFrame baro

Đầu vào: metric numeric. Đơn vị: metric; main service dedup và bỏ -db. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không. Mốc: cần điểm tách; injection chế độa. Nền tối thiểu: >=2 mỗi nửa để không bị bỏ hằng; nửa rỗng lỗi. Defaults: dataset=None không preprocess; dk=False; signed max. Adapter dataset mới: chua_kiem. Nguồn: results/T-013/yeu-cau-dau-vao.csv:3 và method-checklist.csv.

### BARO — BR dict fast path

Đầu vào: dict metric -> [timestamp,value]. Đơn vị: metric; scores trả trực tiếp. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không. Mốc: inject_time bắt buộc. Nền tối thiểu: >=4 mẫu trước; >=1 mẫu sau; codebỏ metric thiếu. Defaults: upper median; quartile index; abs(max-med); IQR0->1. Adapter dataset mới: chua_kiem. Nguồn: results/T-013/yeu-cau-dau-vao.csv:4 và method-checklist.csv.

### N-Sigma — BR/RE RCA

Đầu vào: metric numeric. Đơn vị: metric -> service max/dedup. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không. Mốc: cần điểm tách, chế độa hoặc detector hợp lệ. Nền tối thiểu: >=2 mỗi nửa còn cột biến thiên; không có ngưỡng đủ statistically bảo đảm. Defaults: StandardScaler ddof0; max signed; không k. Adapter dataset mới: chua_kiem. Nguồn: results/T-013/yeu-cau-dau-vao.csv:5 và method-checklist.csv.

### BOCPD — BR bocpd wrapper

Đầu vào: metric latency/error numeric; khôngmatch thì fallbackmọicột. Đơn vị: không xếp hạng; cps chỉsố dòng. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không. Mốc: raw không cần; tái lập reproduce cắt quanhinjection. Nền tối thiểu: không warmup khai báo; cần T>=2 có cột khônghằng; đủ nền normal chưa bảo đảm. Defaults: hazard1/50; nu=d+1 kappa1 mu0 S=I; |diff mode|>1. Adapter dataset mới: chua_kiem. Nguồn: results/T-013/yeu-cau-dau-vao.csv:6 và method-checklist.csv.

### N-Sigma — BR nsigma detector

Đầu vào: time và mọi metric numeric. Đơn vị: khôngrank; listtimestamp theo metric; cótrùng. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không. Mốc: raw không; runnerw300 có injection. Nền tối thiểu: T>=101 mặc định; mỗi mean/std cần >=2 mẫu hợp lệ; representativenormal OPEN. Defaults: k3 startsfrom100; past expanding; std ddof1; abs >3std. Adapter dataset mới: chua_kiem. Nguồn: results/T-013/yeu-cau-dau-vao.csv:7 và method-checklist.csv.

### CIRCA — PC-RHT RCAEval

Đầu vào: metrics numeric. Đơn vị: metric; service dedup là adapter. Vai trò đồ thị: graph cung cấp cha cho hồi quy RHT; DA dùng evidence con; PC là graph học từ metric, architecture là graph từ mapping/call relations; yêu cầu graph: tự học PC trên cả bảng. Mốc: có; inject_time trong tái lập. Nền tối thiểu: 111 điểm resample train theo lookup120 detect10 interval1s; chua_kiem: mức bảo đảm thống kê tối thiểu phổ quát. Defaults: PC alpha0.05 FisherZ stableTrue uc_rule0 uc_priority2 depth không cap; RHT linear tau0 max use_confidenceFalse interval1s current=mốc+300s. Adapter dataset mới: chua_kiem. Nguồn: results/T-014/yeu-cau-dau-vao.csv:2 và method-checklist.csv.

### CIRCA — Kiến trúc-RHT tham chiếu T014

Đầu vào: metrics numeric và service call graph normal; mapping T/S/L/E. Đơn vị: metric; service dedup là adapter. Vai trò đồ thị: graph cung cấp cha cho hồi quy RHT; DA dùng evidence con; PC là graph học từ metric, architecture là graph từ mapping/call relations; yêu cầu graph: có; graph metric từ call graph và mapping. Mốc: có; để chọn normal và RHT. Nền tối thiểu: 111 điểm resample theo cấu hình tham chiếu1s; chua_kiem: mức bảo đảm thống kê phổ quát. Defaults: T→S/L/E; S→L/E; L→E; callerT→calleeT; calleeL/E→callerL/E; calleeE→ancestorE; RHT linear tau0 max interval1s lookup120 detect10. Adapter dataset mới: chua_kiem. Nguồn: results/T-014/yeu-cau-dau-vao.csv:3 và method-checklist.csv.

### CIRCA — Kiến trúc-RHT+DA kiểm cơ chế

Đầu vào: metrics numeric và graph metric có hướng. Đơn vị: metric. Vai trò đồ thị: graph cung cấp cha cho hồi quy RHT; DA dùng evidence con; PC là graph học từ metric, architecture là graph từ mapping/call relations; yêu cầu graph: có; DA interpretation cần DAG. Mốc: có; RHT nhận mốc ngoài. Nền tối thiểu: theo RHT cấu hình chọn; chua_kiem: mức bảo đảm normal phổ quát. Defaults: RHT theo dòng tham chiếu; DAScorer threshold3 aggregator max; key scoreAdjusted -generation rawScore. Adapter dataset mới: chua_kiem. Nguồn: results/T-014/yeu-cau-dau-vao.csv:4 và method-checklist.csv.

### CIRCA — PC-RHT+DA kiểm SCC

Đầu vào: metrics numeric. Đơn vị: metric. Vai trò đồ thị: graph cung cấp cha cho hồi quy RHT; DA dùng evidence con; PC là graph học từ metric, architecture là graph từ mapping/call relations; yêu cầu graph: tự học PC rồi convert cạnh; undirected thành hai hướng. Mốc: có. Nền tối thiểu: theo RHT111 điểm trong cấu hình1s; chua_kiem: độ đủ normal. Defaults: PC/RHT theo dòng PC; DA threshold3 max; SCC topological generations. Adapter dataset mới: chua_kiem. Nguồn: results/T-014/yeu-cau-dau-vao.csv:5 và method-checklist.csv.

### CIRCA — Kiến trúc empirical SVR+RHT+DA; CaseData gốc

Đầu vào: metrics numeric và service call graph normal; mapping T/S/L/E. Đơn vị: metric; service dedup là adapter. Vai trò đồ thị: graph cung cấp cha cho hồi quy RHT; DA dùng evidence con; PC là graph học từ metric, architecture là graph từ mapping/call relations; yêu cầu graph: có; graph metric từ call graph và mapping. Mốc: có; để chọn normal và RHT. Nền tối thiểu: CaseData default interval1min lookup120 detect10:111 điểm train trước mốc; chua_kiem: cấu hình sampling/window thực tế sinh toàn bảngOracle chưa tái lập. Defaults: SVR kernel sigmoid mặc địnhsklearn C1 epsilon.1 gamma scale; RHT tau0 max use_confidenceFalse; DA threshold3; CaseData default interval1min lookup120 detect10 current=mốc+300s. Adapter dataset mới: chua_kiem. Nguồn: results/T-014/yeu-cau-dau-vao.csv:6 và method-checklist.csv.

### CIRCA — PC backend R/pcalg audit MEM25; linearRHT

Đầu vào: metrics numeric. Đơn vị: metric; service dedup là adapter. Vai trò đồ thị: graph cung cấp cha cho hồi quy RHT; DA dùng evidence con; PC là graph học từ metric, architecture là graph từ mapping/call relations; yêu cầu graph: tự học PC bằng causal.R/pcalg, giữ graph node cô lập; graph cached cho factorial scorer. Mốc: có; inject_time trong tái lập. Nền tối thiểu: 111 điểm resample train theo lookup120 detect10 interval1s; chua_kiem: mức bảo đảm thống kê tối thiểu phổ quát. Defaults: R4.4.2 pcalg2.7-12 CI gauss alpha.05 m.maxInf numCores1; LinearRegression; tau0 max confidenceFalse interval1s lookup120 detect10 current=mốc+300s; không DA. Adapter dataset mới: chua_kiem. Nguồn: results/T-014/yeu-cau-dau-vao.csv:7 và method-checklist.csv.

### CIRCA — PC backend R/pcalg audit MEM25; SVR_sigmoidRHT

Đầu vào: metrics numeric. Đơn vị: metric; service dedup là adapter. Vai trò đồ thị: graph cung cấp cha cho hồi quy RHT; DA dùng evidence con; PC là graph học từ metric, architecture là graph từ mapping/call relations; yêu cầu graph: tự học PC bằng causal.R/pcalg, giữ graph node cô lập; graph cached cho factorial scorer. Mốc: có; inject_time trong tái lập. Nền tối thiểu: 111 điểm resample train theo lookup120 detect10 interval1s; chua_kiem: mức bảo đảm thống kê tối thiểu phổ quát. Defaults: R4.4.2 pcalg2.7-12 CI gauss alpha.05 m.maxInf numCores1; SVR sigmoid C1 epsilon.1 gamma scale; tau0 max confidenceFalse interval1s lookup120 detect10 current=mốc+300s; không DA. Adapter dataset mới: chua_kiem. Nguồn: results/T-014/yeu-cau-dau-vao.csv:8 và method-checklist.csv.

### CIRCA — PC backend R/pcalg audit MEM25; linearRHT+DA3

Đầu vào: metrics numeric. Đơn vị: metric; service dedup là adapter. Vai trò đồ thị: graph cung cấp cha cho hồi quy RHT; DA dùng evidence con; PC là graph học từ metric, architecture là graph từ mapping/call relations; yêu cầu graph: tự học PC bằng causal.R/pcalg, giữ graph node cô lập; graph cached cho factorial scorer. Mốc: có; inject_time trong tái lập. Nền tối thiểu: 111 điểm resample train theo lookup120 detect10 interval1s; chua_kiem: mức bảo đảm thống kê tối thiểu phổ quát. Defaults: R4.4.2 pcalg2.7-12 CI gauss alpha.05 m.maxInf numCores1; LinearRegression; tau0 max confidenceFalse interval1s lookup120 detect10 current=mốc+300s; DA threshold3. Adapter dataset mới: chua_kiem. Nguồn: results/T-014/yeu-cau-dau-vao.csv:9 và method-checklist.csv.

### CIRCA — PC backend R/pcalg audit MEM25; SVR_sigmoidRHT+DA3

Đầu vào: metrics numeric. Đơn vị: metric; service dedup là adapter. Vai trò đồ thị: graph cung cấp cha cho hồi quy RHT; DA dùng evidence con; PC là graph học từ metric, architecture là graph từ mapping/call relations; yêu cầu graph: tự học PC bằng causal.R/pcalg, giữ graph node cô lập; graph cached cho factorial scorer. Mốc: có; inject_time trong tái lập. Nền tối thiểu: 111 điểm resample train theo lookup120 detect10 interval1s; chua_kiem: mức bảo đảm thống kê tối thiểu phổ quát. Defaults: R4.4.2 pcalg2.7-12 CI gauss alpha.05 m.maxInf numCores1; SVR sigmoid C1 epsilon.1 gamma scale; tau0 max confidenceFalse interval1s lookup120 detect10 current=mốc+300s; DA threshold3. Adapter dataset mới: chua_kiem. Nguồn: results/T-014/yeu-cau-dau-vao.csv:10 và method-checklist.csv.

### MicroRank — gốc efd85e8

Đầu vào: trace Jaeger có duration; parent; span.kind; pod; root frontend-server. Đơn vị: instance-operation; mapping instance riêng. Vai trò đồ thị: call/coverage graph lan truyền PageRank rồi weighted spectrum; không phải detector graph/subgraph; yêu cầu graph: có: call graph và bipartite operation-trace; parent còn dùng học self-time. Mốc: không cần inject cho alarm gốc; chế độ biết mốc phải khai báo. Nền tối thiểu: không có số tối thiểu bảo đảm; tác giả khuyên history dài ví dụ1h; mỗi operation cần baseline hợp lệ. Defaults: alarm μ+1.5σ và >8 trace; partition μ+σ+50ms; d=.85 alpha=.01 25 vòng; Dstar2 top_max=5 trả11. Adapter dataset mới: chua_kiem. Nguồn: results/T-015/yeu-cau-dau-vao.csv:2 và method-checklist.csv.

### MicroRank — RCAEval 259ea41

Đầu vào: span duration và relation parent cùng operation. Đơn vị: service-operation; output top11 operation. Vai trò đồ thị: call/coverage graph lan truyền PageRank rồi weighted spectrum; không phải detector graph/subgraph; yêu cầu graph: có: graph trước/sau mốc và bipartite; lỗi reset cạnh. Mốc: có: inject_time μs được caller cấp. Nền tối thiểu: ≥2 span trước mốc/operation để std mẫu có nghĩa; thực tế không guard đầy đủ. Defaults: span μ+3σ với >=; std ddof1; ms round2; d=.85 alpha=.01 25vòng; Dstar2. Adapter dataset mới: chua_kiem. Nguồn: results/T-015/yeu-cau-dau-vao.csv:3 và method-checklist.csv.

### MicroRank — MicroRank-RCAEval sửa đầu vào

Đầu vào: span duration và parent, cùng khóa service-method. Đơn vị: service-operation; top11 và full riêng; service mapping từ bảng. Vai trò đồ thị: call/coverage graph lan truyền PageRank rồi weighted spectrum; không phải detector graph/subgraph; yêu cầu graph: có: hai graph từ hai tập trace rời; bipartite incidence. Mốc: có: incident_time_us; không gọi tự phát hiện. Nền tối thiểu: ≥2 span kết thúc trước mốc mỗi operation xuất hiện sau mốc; baseline μ/std ms round2. Defaults: giữ detector span3σ; normal là phần bù; gốc d=.85 alpha=.01 25vòng Dstar2; seed0; canonical trace/op. Adapter dataset mới: chua_kiem. Nguồn: results/T-015/yeu-cau-dau-vao.csv:4 và method-checklist.csv.

### TraceRCA — gốc b9087c7

Đầu vào: invocation source-target, trace_id, latency, http_status; cache reference và feature được chọn. Đơn vị: service source/target; pattern singleton; không phải operation/interface. Vai trò đồ thị: support/confidence theo coverage, không PageRank; invocation relations của gốc khác RE; yêu cầu graph: không graph propagation ở main enable_PRFL=False; tập source-target và chiều gọi tham gia điểm. Mốc: window/history do caller chọn; core không đọc inject_time. Nền tối thiểu: cache mean/std từng source-target-feature; std dân số có sàn .1; cache thiếu tự học từ current; chua_kiem: số mẫu/history tối thiểu tác giả bảo đảm. Defaults: threshold=1σ hai phía; chọn feature stderr_criteria: CLI --fisher default1, Makefile truyền3; support=.1; không ngưỡng min_confidence tường minh; k=100 mức điểm; PRFL=False; loại gateway; main noise=0 vẫn hạ cờ ngẫu nhiên1% trong trace abnormal với seed2021. Adapter dataset mới: chua_kiem. Nguồn: results/T-015/yeu-cau-dau-vao.csv:5 và method-checklist.csv.

### TraceRCA — RCAEval + adapter hữu hạn

Đầu vào: span duration theo service-operation. Đơn vị: service-operation; service bỏ trùng sau sorting. Vai trò đồ thị: support/confidence theo coverage, không PageRank; invocation relations của gốc khác RE; yêu cầu graph: không; grouping service-operation không là graph detector. Mốc: có: inject_time μs; before END<marker/current END>=marker. Nền tối thiểu: ≥2 span reference mỗi current operation để std mẫu; missing/NaN baseline phải báo lỗi. Defaults: ngưỡng μ+3σ >=; μ/std ms round2 ddof1; score2a/(A+n); finite trước sort; tie tên operation. Adapter dataset mới: chua_kiem. Nguồn: results/T-015/yeu-cau-dau-vao.csv:6 và method-checklist.csv.

### Detector trace — span μ+3σ RCAEval

Đầu vào: duration inclusive; timestamp chọn reference/current; định danh operation service+method bắt buộc, fallback operationName. Đơn vị: flag span; trace abnormal iff có ít nhất1 flagged span trong biến thể sửa. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không trong detector; đồ thị dùng sau. Mốc: có trong adapter RCAEval; standalone cần reference/current cấp độc lập. Nền tối thiểu: ≥2 span/operation; std0 vẫn >=mu dễ báo; chưa bảo đảm normal sạch. Defaults: μ/std mẫu ddof1 round2ms; duration>=μ+3σ; no-anomaly explicit. Adapter dataset mới: chua_kiem. Nguồn: results/T-015/yeu-cau-dau-vao.csv:7 và method-checklist.csv.

### Detector trace — MicroRank gốc alarm và partition

Đầu vào: root request duration; số operation; μ/std self-handling. Đơn vị: alarm cấp hệ và normal/anomaly cấp trace. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: parent dùng tính handling baseline; PageRank sau detection. Mốc: alarm gốc không inject; cần normal history; known-window là chế độ khác. Nền tối thiểu: tác giả khuyên dài ví dụ1h; mỗi operation có mean/std; alarm cần >8 trace vượt ngưỡng. Defaults: alarm E=Σc(μ+1.5σ), D>E và count>8; partition E=Σc(μ+σ)+50ms; std dân số round4. Adapter dataset mới: chua_kiem. Nguồn: results/T-015/yeu-cau-dau-vao.csv:8 và method-checklist.csv.

### TORAI — goc: RCAEval 259ea41 RCAEval/e2e/torai.py (giống nhánh fse26)

Đầu vào: metric theo service; chuỗi đếm mẫu log logts (torai.py:73 đọc trực tiếp, thiếu thì lỗi; không có log phải truyền bảng chỉ có cột time). Đơn vị: service = tiền tố trước '_' của mọi cột metric, log, trace (gồm cả redis, frontend-external, health, traceservice, *-mongo; OB 14, SS 15, TT 68 ứng viên); đầu ra dài bằng số ứng viên. Vai trò đồ thị: không call graph; khung nhân quả cục bộ quanh F trong cụm, chỉ khi không fallback; yêu cầu graph: không. Mốc: có: inject_time hoặc t̂_A từ bộ phát hiện ngoài (chế độ biết trước thời điểm). Nền tối thiểu: L/2 phút trước mốc với cửa sổ L (cửa sổ 10: 5 phút = 300 dòng metric, 20 dòng logts). Defaults: --length 10 (docs/TORAI.md; main.py mặc định 20); giảm mẫu iloc[::15] hai lần (torai.py:81, 29); StandardScaler; trace_err bỏ 2 điểm cuối normal, x1e9 khi mean=var=0; GMM full, max_iter 50, random_state 0, k=1..n theo BIC; RCD gamma 5, localized, bins 5, chi-square, alpha pha1 0,01 / pha2 0,001 bước 0,1; không seed. Adapter dataset mới: chua_kiem. Nguồn: results/T-016/yeu-cau-dau-vao.csv:2 và method-checklist.csv.

### TORAI — sua: src/torai/torai_sua.py (bỏ giảm mẫu lần 2 + ghép theo vị trí)

Đầu vào: như bản gốc. Đơn vị: service (như bản gốc). Vai trò đồ thị: không call graph; khung nhân quả cục bộ quanh F trong cụm, chỉ khi không fallback; yêu cầu graph: không. Mốc: có (như bản gốc). Nền tối thiểu: như bản gốc. Defaults: như bản gốc trừ: giảm mẫu metric một lần; metric và logts ghép theo vị trí trong từng nửa, cắt về độ dài chung. Adapter dataset mới: chua_kiem. Nguồn: results/T-016/yeu-cau-dau-vao.csv:3 và method-checklist.csv.

### RCD — RCAEval 259ea41 RCAEval/e2e/rcd.py (biến thể đối chứng của TORAI, Q-38)

Đầu vào: metric. Đơn vị: metric; chấm ở mức service bằng tiền tố, bỏ '-db', bỏ trùng (main.py:560-572); đầu ra chỉ 1–25 metric nên service gốc có thể vắng mặt. Vai trò đồ thị: khung nhân quả cục bộ quanh F-node dùng CI; không call graph; yêu cầu graph: không (tự học khung kề quanh F-node từ dữ liệu ca). Mốc: có (chia normal/lỗi). Nền tối thiểu: L/2 phút trước mốc; số dòng phải lớn hơn số biến ở pha 2 (assert rcd.py:168). Defaults: gamma 5, localized True, bins 5 (K-means), chi-square, alpha pha1 0,01 / pha2 0,001 bước 0,1 tới < 1, dk_select_useful False, seed None (RCD gốc: seed 420, bỏ metric sd < 1). Adapter dataset mới: chua_kiem. Nguồn: results/T-016/yeu-cau-dau-vao.csv:4 và method-checklist.csv.

### RCD — gốc azamikram/rcd 373882c (chỉ đọc, không chạy trên dataset)

Đầu vào: metric dạng normal.csv, anomalous.csv. Đơn vị: metric, top-k (--k). Vai trò đồ thị: khung nhân quả cục bộ quanh F-node dùng CI; không call graph; yêu cầu graph: không. Mốc: có (tách hai file). Nền tối thiểu: chua_kiem: bài dùng 5 phút bình thường (Sock Shop), 2 ngày (sự cố thật). Defaults: SEED 420, BINS None (synthetic rời rạc sẵn), LOCAL_ALPHA 0,01, gamma 5, localized chỉ khi --local. Adapter dataset mới: chua_kiem. Nguồn: results/T-016/yeu-cau-dau-vao.csv:5 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — primary events sigma log0 half300

Đầu vào: ít nhất một modality khả dụng; bản đủ ba nguồn cần metric+trace+log. Đơn vị: service/entity quan sát ở hai cửa sổ (union; normal-only log score0; lỗi log chỉ incident); DB giữ riêng khi chưa có alias kiến trúc; tie groups; lexical chỉ hiển thị; allzero abstain. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: metric >=2 finite/channel; trace >=1 duration/service; log fixed threshold không cần normal. Đây là tối thiểu toán học; chưa đủ hiệu chỉnh statistical false alerts. Defaults: metric mean+3std0; events; P95linear trace>3x; log substr ERROR/FAIL/EXCEPTION count>0; window half300s. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:2 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — metric P95

Đầu vào: ít nhất một modality khả dụng; bản đủ ba nguồn cần metric+trace+log. Đơn vị: service/entity quan sát ở hai cửa sổ (union; normal-only log score0; lỗi log chỉ incident); DB giữ riêng khi chưa có alias kiến trúc; tie groups; lexical chỉ hiển thị; allzero abstain. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: metric >=2 finite/channel; trace >=1 duration/service; log fixed threshold không cần normal. Đây là tối thiểu toán học; chưa đủ hiệu chỉnh statistical false alerts. Defaults: đổi metric threshold=historical P95linear; còn lại primary. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:3 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — metric channels

Đầu vào: ít nhất một modality khả dụng; bản đủ ba nguồn cần metric+trace+log. Đơn vị: service/entity quan sát ở hai cửa sổ (union; normal-only log score0; lỗi log chỉ incident); DB giữ riêng khi chưa có alias kiến trúc; tie groups; lexical chỉ hiển thị; allzero abstain. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: metric >=2 finite/channel; trace >=1 duration/service; log fixed threshold không cần normal. Đây là tối thiểu toán học; chưa đủ hiệu chỉnh statistical false alerts. Defaults: mỗi metric có bất kỳ vượt ngưỡng chỉ1phiếu; còn lại primary. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:4 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — log threshold1

Đầu vào: ít nhất một modality khả dụng; bản đủ ba nguồn cần metric+trace+log. Đơn vị: service/entity quan sát ở hai cửa sổ (union; normal-only log score0; lỗi log chỉ incident); DB giữ riêng khi chưa có alias kiến trúc; tie groups; lexical chỉ hiển thị; allzero abstain. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: metric >=2 finite/channel; trace >=1 duration/service; log fixed threshold không cần normal. Đây là tối thiểu toán học; chưa đủ hiệu chỉnh statistical false alerts. Defaults: log count>1; còn lại primary. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:5 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — log threshold10

Đầu vào: ít nhất một modality khả dụng; bản đủ ba nguồn cần metric+trace+log. Đơn vị: service/entity quan sát ở hai cửa sổ (union; normal-only log score0; lỗi log chỉ incident); DB giữ riêng khi chưa có alias kiến trúc; tie groups; lexical chỉ hiển thị; allzero abstain. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: metric >=2 finite/channel; trace >=1 duration/service; log fixed threshold không cần normal. Đây là tối thiểu toán học; chưa đủ hiệu chỉnh statistical false alerts. Defaults: log count>10; còn lại primary. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:6 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — trace factor2

Đầu vào: ít nhất một modality khả dụng; bản đủ ba nguồn cần metric+trace+log. Đơn vị: service/entity quan sát ở hai cửa sổ (union; normal-only log score0; lỗi log chỉ incident); DB giữ riêng khi chưa có alias kiến trúc; tie groups; lexical chỉ hiển thị; allzero abstain. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: metric >=2 finite/channel; trace >=1 duration/service; log fixed threshold không cần normal. Đây là tối thiểu toán học; chưa đủ hiệu chỉnh statistical false alerts. Defaults: trace P95 incident>2x normal; còn lại primary. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:7 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — trace factor4

Đầu vào: ít nhất một modality khả dụng; bản đủ ba nguồn cần metric+trace+log. Đơn vị: service/entity quan sát ở hai cửa sổ (union; normal-only log score0; lỗi log chỉ incident); DB giữ riêng khi chưa có alias kiến trúc; tie groups; lexical chỉ hiển thị; allzero abstain. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: metric >=2 finite/channel; trace >=1 duration/service; log fixed threshold không cần normal. Đây là tối thiểu toán học; chưa đủ hiệu chỉnh statistical false alerts. Defaults: trace P95 incident>4x normal; còn lại primary. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:8 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — window half600

Đầu vào: ít nhất một modality khả dụng; bản đủ ba nguồn cần metric+trace+log. Đơn vị: service/entity quan sát ở hai cửa sổ (union; normal-only log score0; lỗi log chỉ incident); DB giữ riêng khi chưa có alias kiến trúc; tie groups; lexical chỉ hiển thị; allzero abstain. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: metric >=2 finite/channel; trace >=1 duration/service; log fixed threshold không cần normal. Đây là tối thiểu toán học; chưa đủ hiệu chỉnh statistical false alerts. Defaults: normal[t-600,t),incident[t,t+600); còn lại primary. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:9 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — metric rule

Đầu vào: metric time+service_metric. Đơn vị: alert/channel hoặc service; không riêng root ranking. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: >=2 finite historical points/channel. Defaults: mean+3std0 hoặc P95; mỗi point>threshold alert. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:10 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — trace rule

Đầu vào: trace service+duration hai cửa sổ. Đơn vị: alert/channel hoặc service; không riêng root ranking. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: >=1 span mỗi service mỗi cửa sổ. Defaults: P95linear; factor3; strict>. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:11 và method-checklist.csv.

### SimpleRCA (M4 theo mô tả bài) — log rule

Đầu vào: log service+message cửa sổ incident. Đơn vị: alert/channel hoặc service; không riêng root ranking. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không; không dùng parentSpanID hoặc statusCode. Mốc: adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t. Nền tối thiểu: không cho fixed threshold; baseline không được dùng để hiệu chỉnh spike. Defaults: ERROR/FAIL/EXCEPTION case-insensitive substring; một count/dòng; count>0. Adapter dataset mới: chua_kiem. Nguồn: results/T-017/yeu-cau-dau-vao.csv:12 và method-checklist.csv.

### GDN (d-ailin/GDN@9853899) — code mặc định (run.sh, report='best')

Đầu vào: metric đa biến, mọi cột cùng nhịp tick. Đơn vị: không xếp hạng; đầu ra là cờ bất thường mỗi tick và điểm lệch từng metric. Vai trò đồ thị: graph tương quan học từ embedding cung cấp neighbor features cho dự báo; không root ranking; yêu cầu graph: không cần đầu vào đồ thị; tự học đồ thị tương quan top-k từ embedding (GDN.py:150-163). Code không nhận đồ thị trước (ho-so mục 5 dòng 10). Mốc: không khi chạy; nhưng chọn ngưỡng bằng nhãn test. Nền tối thiểu: như biến thể report='val'. Defaults: run.sh: seed 5, batch 32, w=5, dim 64, topk 5 (kể cả chính nút), out_layer_num 1, val_ratio 0.2, epoch 30, patience 15 (train.py:49), Adam lr 1e-3, epsilon 0.01, làm trơn 4 tick. Adapter dataset mới: chua_kiem. Nguồn: results/T-018/yeu-cau-dau-vao.csv:2 và method-checklist.csv.

### GDN (d-ailin/GDN@9853899) — code, report='val' (ngưỡng như bài)

Đầu vào: metric đa biến, mọi cột cùng nhịp tick. Đơn vị: không xếp hạng; đầu ra là cờ bất thường mỗi tick và điểm lệch từng metric. Vai trò đồ thị: graph tương quan học từ embedding cung cấp neighbor features cho dự báo; không root ranking; yêu cầu graph: không cần đầu vào đồ thị; tự học đồ thị tương quan top-k từ embedding (GDN.py:150-163). Code không nhận đồ thị trước (ho-so mục 5 dòng 10). Mốc: không. Nền tối thiểu: bài: 47 515 tick (SWaT) / 118 795 (WADI) ở 10 s. RE2-TT: không đủ ở 1 ca (720 tick: 23,6–30,7 % tick bình thường giữ ngoài bị báo động, 4 lượt) ở 5 ca (3600 tick: 10,3–11,2 %, 3 lượt); 10 ca (7200 tick): 4,95 %, 1 lượt; ho-so 9.4. Defaults: run.sh: seed 5, batch 32, w=5, dim 64, topk 5 (kể cả chính nút), out_layer_num 1, val_ratio 0.2, epoch 30, patience 15 (train.py:49), Adam lr 1e-3, epsilon 0.01, làm trơn 4 tick. Adapter dataset mới: chua_kiem. Nguồn: results/T-018/yeu-cau-dau-vao.csv:3 và method-checklist.csv.

### GDN (d-ailin/GDN@9853899) — đề xuất chế độ b (bộ cột cố định, chuẩn hóa và ngưỡng từ tập kiểm định; ho-so 8.2)

Đầu vào: metric đa biến, mọi cột cùng nhịp tick. Đơn vị: không xếp hạng; đầu ra là cờ bất thường mỗi tick và điểm lệch từng metric. Vai trò đồ thị: graph tương quan học từ embedding cung cấp neighbor features cho dự báo; không root ranking; yêu cầu graph: không cần đầu vào đồ thị; tự học đồ thị tương quan top-k từ embedding (GDN.py:150-163). Code không nhận đồ thị trước (ho-so mục 5 dòng 10). Mốc: không với ca được chấm. Nền tối thiểu: chua_kiem: số ca tối thiểu chưa xác định (10 ca vẫn 45 % tick bình thường giữ ngoài bị báo động với biến thể b); với RE2-TT tỷ lệ ô bình thường mới nằm ngoài khoảng học: 23 % (1 ca), 4,9 % (5 ca), 0,6 % (10 ca) (runs/b6-lech-phan-bo.json); cần xử lý cột hằng và lệch mức trước. Defaults: run.sh: seed 5, batch 32, w=5, dim 64, topk 5 (kể cả chính nút), out_layer_num 1, val_ratio 0.2, epoch 30, patience 15 (train.py:49), Adam lr 1e-3, epsilon 0.01, làm trơn 4 tick. Adapter dataset mới: chua_kiem. Nguồn: results/T-018/yeu-cau-dau-vao.csv:4 và method-checklist.csv.

### DecompRCA — bộ truy hồi đa tín hiệu (đã đọc, không chạy) — K=15 chia 5+5+5 (mag/ons/stc)

Đầu vào: metric đa biến. Đơn vị: metric; chấm quy về service (bỏ -db). Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không. Mốc: có: t_det (RCAEval: mốc tiêm). Nền tối thiểu: cửa sổ nền của chính ca: 360–600 dòng 1 s ở RE1. Defaults: K=15; z_low 1,5; rời rạc khi <= 5 giá trị; tol 1e-2 (candidate_selection.py). Adapter dataset mới: chua_kiem. Nguồn: results/T-018/yeu-cau-dau-vao.csv:5 và method-checklist.csv.

### DecompRCA — bộ xếp lại LLM (đã đọc, không chạy) — gpt-oss-120b, T=1, 3 lượt; có/không tài liệu DK

Đầu vào: bản ghi bằng chứng từng ứng viên (z-score, độ trễ khởi phát, trung bình trước/sau). Đơn vị: metric, chấm quy về service. Vai trò đồ thị: không graph hoặc không áp dụng trong rule thống kê này; yêu cầu graph: không (DK có thể mô tả đường gọi bằng lời). Mốc: có (qua bộ truy hồi). Nền tối thiểu: như bộ truy hồi. Defaults: max_tokens 4096, không seed (run_llm_balanced.py:265-273; _common.py:270). Adapter dataset mới: chua_kiem. Nguồn: results/T-018/yeu-cau-dau-vao.csv:6 và method-checklist.csv.
