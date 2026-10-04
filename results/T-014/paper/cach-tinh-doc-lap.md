# Tính lại điểm RHT và DA

`independent_scores.py` không import CIRCA, RCAEval hay sklearn. Nó dùng mảng đã chụp ở biên scorer, tính OLS bằng `scipy.linalg.lstsq`, rồi tự tính phần dư, z-score, confidence và DA. Mỗi node được so riêng với ngưỡng `atol=1e-7, rtol=1e-7`. Sai số tuyệt đối và tương đối của từng giá trị đều được lưu. Điểm rất lớn không bị cắt hoặc làm tròn để được PASS.

Giới hạn: đây là kiểm độc lập ở phép tính điểm. Snapshot vẫn lấy parent order, train/test arrays và topological groups từ runner. Nó có thể che một lỗi cùng có trong khâu dựng parents, preprocessing hoặc resampling. Phải kiểm riêng các mảng từ raw metric timestamps và graph edges. PASS của script này không tự chứng minh boundary không rò nhãn, graph đúng hay cửa sổ nạp đúng.

## OLS và RHT

Với X là ma trận parents ở 111 mẫu train, y là metric được chấm, đặt trung bình từng cột là x̄ và trung bình y là ȳ. Tính Xc=X−x̄, yc=y−ȳ. `lstsq(Xc,yc,cond=max(Xc.shape)·eps64)` cho β̂; b̂=ȳ−x̄ᵀβ̂. Đây là phép giải least squares có intercept tương ứng nhánh dense của sklearn 1.6.0. Không dùng normal equation vì bình phương condition number có thể làm sai hệ kém điều kiện. Khi không có effective parents, residual chính là y. Nếu hồi quy ném ValueError, script ghi nhánh dự phòng trực tiếp thay vì gọi đó là thành công OLS.

RCAEval dựng X bằng transpose của parent series. Với tau=0, thứ tự bộ nhớ là F; sklearn `copy_X` giữ thứ tự K. Snapshot có thể ghi `x_memory_order` là C hoặc F theo mảng thật. Nếu thiếu trường này, script dùng F theo source, ghi rõ đây là default. Nó không thử hai thứ tự rồi lấy thứ tự khớp điểm hơn. Thứ tự parents vẫn phải lấy đúng từ lần gọi scorer, vì đổi thứ tự khi covariance gần suy biến có thể đổi sai số floating point.

Residual train là e=y−Xβ̂−b̂. Để khớp StandardScaler, script tính mean μ và population variance ddof=0 bằng corrected two-pass:

\[
\mu=\frac{1}{n}\sum e_t,\quad c_t=e_t-\mu,\quad
v=\frac{\sum c_t^2-(\sum c_t)^2/n}{n}.
\]

Với ε là machine epsilon float64, StandardScaler nhận biết near-constant khi:

\[
v\le n\varepsilon v+(n\mu\varepsilon)^2.
\]

Trường hợp đó scale=1; trường hợp khác scale=√v. Đây không phải một sàn tùy chọn như 1e-6. Nếu residual gần 0 nhưng v vẫn trên bound, scale có thể rất nhỏ và score có thể rất lớn. Điều đó cần soi rank, residual và condition number; không tự đồng nhất score lớn với bằng chứng root cause mạnh. Parent thiếu, model misspecification, nội suy hoặc rounding là các giải thích khả thi khác.

Ở 10 mẫu test, z=(e−μ)/scale, s=max|z|. Confidence c=erf(s/√2)=1−2Φ(−s). Script tính erf trực tiếp bằng thư viện chuẩn; đây là một biến đổi Gaussian của s, không phải xác suất service là root. RHT chính dùng s, không dùng c.

Nguồn thuật toán đã đọc: RCAEval `graph_heads/rht.py:118–124,133–147,213–227`; môi trường py312-pin, sklearn `linear_model/_base.py:681–682`, `utils/extmath.py:1095–1142`, `preprocessing/_data.py:69–82`. Phiên bản và hash nguồn chính ở `source-manifest.json`; cách dựng môi trường thuộc báo cáo môi trường chính của T-014.

## DA

DA nhận scores gốc và graph. Đặt θ=3. Nó duyệt các generation ngược từ lá lên. Tại node i, thu mọi score của child; nếu child j có s_j<θ, còn thu evidence mà j đã tích lũy. Nó không thay score child bằng score đã cộng DA trong bước thu này.

\[
D_i=\{s_j:j\in Ch(i)\}\cup\bigcup_{j\in Ch(i):s_j<\theta}D_j,
\qquad s'_i=s_i+\mathbf 1[s_i\ge\theta]\max(D_i\cup\{0\}).
\]

Key xếp giảm dần là `(s′,−generation,s)`. Trong DAG, key generation ưu tiên ancestor khi điểm hòa. Trong SCC, code vẫn duyệt set của generation; một child cùng SCC có thể chưa có evidence tại lúc được đọc. Script ghi mọi trường hợp đó ở `DA_unresolved_child_evidence`. Capture thứ tự graph group trước khi DAScorer tạo lại set chưa chắc đủ: cần thứ tự `sorted_nodes` thực tế hoặc instrumentation tương đương. Không thử hoán vị theo kết quả mong muốn.

Một kiểm giả đủ nhỏ để tính tay: a→b→c có scores4,1,9. θ=3 nên b thu9 nhưng giữ điểm1. a thu score b=1 và evidence9 đi xuyên b; a thành13. Đây là fixture thuật toán, không phải kết quả RE2-TT.

Một SCC fixture chứng minh thứ tự có hệ quả: d→b; a↔b; a→c, scores d=5,a=1,b=1,c=10. Cùng generation {a,b}, nếu a được xử lý trước b thì d thành15; nếu b trước a thì d thành6. Đây là hành vi code khi graph cyclic, không phải bằng chứng thực nghiệm rằng CIRCA sai trên Train Ticket. Các khả năng graph SCC và missing-meta forwarding phải kiểm riêng trước khi diễn giải DA theo giả định DAG.

Nguồn: RCAEval `graph_heads/rht.py:254–287`; CIRCA gốc `circa/alg/ci/__init__.py:126–160`. Lớp có threshold default0; cấu hình canonical RHT+DA dùng3 ở `circa/experiment/comparison/models.py:629–634`.

## Chạy và đọc đầu ra

Lệnh: `python results/T-014/paper/independent_scores.py snapshot.json --out results/T-014/paper/<ten-phep-kiem> --compare`. Chỉ dùng snapshot của ca đã được SPEC chọn; không chọn lại ca vì score hoặc lỗi numerical.

`comparison.json` giữ toàn bộ hệ số, intercept, rank/singular values của OLS, residuals, normal parameters, test z, RHT/DA, sai số từng node. `comparison.csv` giúp soi từng thành phần. Exit0 chỉ khi có node, có phép so, không exception và mọi phép so đều trong tolerance. Tệp kết quả vẫn được giữ khi exit1.

`--self-test` kiểm variance, cột hằng, OLS chính xác, DA trên DAG và SCC fixture nói trên. Self-test không thay so snapshot thật. Đầu ra đã chạy được lưu ở `independent-self-test.json`.
