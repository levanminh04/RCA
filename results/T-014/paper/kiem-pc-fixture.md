# Kiểm PC nhỏ: cơ chế và các nhánh lỗi

Nguồn kết quả là `pc-fixtures-002/fixture-results.json`, từng JSON theo fixture, `wrapper-results.json`, `uninstrumented-check.json` và `independent/comparison.json`. Script: `pc_fixtures.py`. Dữ liệu chỉ là tín hiệu giả, không đọc ca RCA, dataset mới hay nhãn. Seed20261004, 2000 mẫu, năm biến. Các inputs có thể dựng lại từ script và lưu ở NPZ; hash ở từng record.

Ước lượng trước chạy120 giây. Lượt002 ghi start/end từng PC call và wrapper trong `progress.jsonl`; toàn khối từ02:17:33.829745 tới02:17:43.212017 UTC. Thời gian chỉ là diagnostic vì laptop có phiên khác; không dùng làm chi phí chính thức hoặc suy thời gian Train Ticket. Không chạy lại PC Train Ticket trong nhánh này.

## Dữ liệu giả và depth

Chain: x₀=u₀, x₁=0.8x₀+u₁, x₂=0.8x₁+u₂, x₃=0.8x₂+u₃; x₄=u₄ độc lập. Collider: x₀=u₀, x₁=u₁, x₂=0.8x₀+0.8x₁+u₂, x₃=0.7x₂+u₃, x₄=u₄. Mọi u là Normal(0,1) từ cùng seed đã chốt trước kết quả.

Default gọi causal-learn PC nguyên trạng. Prefix0/1 là function compile trong bộ nhớ từ source skeleton, chỉ đổi điều kiện while thành `original_condition and depth<cap`; biến depth bắt đầu−1 và tăng trước CI. Vì vậy cap0 chạy đúng lượt depth0; cap1 chạy depth0 và1. Không sửa file thư viện. Dùng recorder để lưu mọi CI và condition size; recorder được kiểm riêng bằng default không instrumentation trên cả hai mô hình, cho cùng matrix.

| Fixture | Alpha | Default edges / max | Prefix0 edges / max | Prefix1 edges / max |
|---|---:|---:|---:|---:|
| chain | .01 | 3 / 1 | 6 / 0 | 3 / 1 |
| chain | .05 | 3 / 1 | 6 / 0 | 3 / 1 |
| chain | .1 | 3 / 1 | 6 / 0 | 3 / 1 |
| collider | .01 | 3 / 2 | 5 / 0 | 3 / 1 |
| collider | .05 | 3 / 2 | 5 / 0 | 3 / 1 |
| collider | .1 | 3 / 2 | 5 / 0 | 3 / 1 |

`max` là condition size lớn nhất thực sự được gọi, không phải default có maxdepth đó. Default không có cap. Prefix1 cho cùng final matrix ở hai mô hình này không chứng minh nó tương đương default nói chung: collider default còn thực hiện39 CI so với36 ở prefix1. Chain3 edges chưa được định hướng; collider xác định x₀→x₂←x₁ và x₂→x₃. Đảo cột bằng hoán vị [4,2,0,3,1] giữ đúng labeled endpoints của cả hai default alpha.05; không chỉ so edge count.

Các alpha chưa đổi graph ở hai quan hệ mạnh này. Có thể do p-values không nằm gần các ngưỡng, không phải bằng chứng PC không nhạy alpha. Phép kiểm boundary bổ sung dưới đây tách điều đó.

## Alpha boundary được dựng bằng công thức

Nguồn: `pc-alpha-boundary/config-before-run.json` và `results.json`; script `pc_alpha_boundary.py`. Trước lời gọi PC, dựng ba biến bằng QR của dữ liệu centered, rồi đặt correlation r=tanh(Φ⁻¹(1−0.03/2)/√(2000−3)). Nhờ đó Fisher-Z cho p≈0.03 giữa hai biến; biến còn lại trực giao. Đây là kiểm ý nghĩa threshold, không chọn dữ liệu hoặc cấu hình theo RCA score/accuracy.

Thư viện cho p=0.029999999999999805. Alpha.01 xóa cạnh; alpha.05/.1 giữ một cạnh. Cả ba khớp luật p>alpha→remove. Tăng alpha làm khó chấp nhận độc lập hơn đối với cùng p-value. Vì PC thay neighbors và tập điều kiện theo các lượt, kết quả này không chứng minh số cạnh toàn graph luôn đơn điệu theo alpha trên dữ liệu bất kỳ.

## Hằng, singular, rỗng và wrapper

| Trường hợp | Kết quả thật | Kết luận được phép |
|---|---|---|
| Constant đưa trực tiếp vào PC | graph có7 edges;66/102 CI trả p=NaN; correlation nonfinite | Không exception không đủ hợp lệ. NaN>alpha là False nên có thể giữ cạnh. Pipeline có preprocessing phải được xét riêng. |
| Constant qua CIRCA preprocessing | cột hằng bị loại; wrapped/unwrapped cùng ranking4 metric, stderr rỗng | Preprocessing xử lý full-table constant này, không chứng minh mọi covariance singular đã được xử lý. |
| Duplicate columns | raw/unwrapped ValueError: correlation matrix singular | Cột trùng không hằng vẫn làm Fisher-Z không nghịch đảo được. |
| Duplicate qua wrapper | ranks đúng thứ tự năm cột; stderr báo fallback | Phải loại fallback khỏi kết luận xếp hạng nhân quả. Nó không phải RHT tìm được năm ứng viên đúng. |
| Orthogonal five variables | PC0 edges; wrapped/unwrapped ranks=[]; không exception/fallback | Graph/scorer mất hết candidate. Không được ghi “chạy được” chỉ từ exit hoặc không có traceback. |
| RuntimeError cố ý và đảo cột | wrapper trả thứ tự cột tương ứng; stderr minh bạch | Chứng minh fingerprint fallback; không dùng kết quả này để chấm RCA. |

Output schema còn có khác biệt: `circa` thành công trả `node_names` gồm time, nhưng adj chỉ có metric. Fixture constant-preprocessed có adj4×4/node_names5; empty có adj5×5/node_names6. Consumer phải dùng identity của pc_input để align graph. Chưa có bằng chứng consumer task cũ nào đã dùng sai field này.

## Scorer độc lập và DA cyclic

Snapshot từ chain default alpha.05 giữ conversion của RCAEval, bao gồm final reverse. Có4 scored nodes vì biến độc lập không có cạnh bị bỏ. Independent script so32 thành phần RHT/residual/confidence/DA, PASS; max absolute error2.220446049250313e−16. Snapshot từ dữ liệu giả này không thay ví dụ tính tay RE2-TT. Nó kiểm scorer trên PC graph cyclic nhỏ trong phạm vi numerical semantics.

Nhánh audit đã chạy code chính thức trên SCC fixture bằng hashseed0–5 (`../audit/da-cycle.json`): DAG giữ một vector; cycle có hai vectors. Với a→b, b↔c và scores4,1,4, DA score c bằng8 hoặc5. Đây là khác điểm số, không chỉ tie. Đường vòng có thể đưa score c về evidence của chính c. Các giải thích của tác giả cho DA dựa DAG; một method call không lỗi không chữa được giả định đó.

## Nguồn default và giới hạn kết luận

T-014-main đọc lại causal-learn từ py312-pin. Default: alpha.05, fisherz, stable=True, uc_rule0, uc_priority2 (`causallearn/search/ConstraintBased/PC.py:22–26`). Skeleton không cap depth; điều kiện dừng theo max_degree (`utils/PCUtils/SkeletonDiscovery.py:61–65`). Fisher-Z nghịch đảo correlation, clip r, tính T/p (`utils/cit.py:138–171`). Các version/hash và file:dòng được ghi trong `source-manifest.json`.

Fixture kiểm được wiring, CI thresholds, empty/singular/constant/fallback, column permutation và tính điểm nhỏ. Nó không kiểm feasibility của default RE2-TT273 metrics, graph/rank đầy đủ, điều kiện depth cao, độ nhạy alpha của Train Ticket, normal/normal của PC mặc định, số công bố hoặc độ lặp lại/permutation ở quy mô đó. Các phần này chỉ được kết luận từ lượt EC2/default/capped của main và phải giữ tên cấu hình khác nhau.

## Lượt hỏng được giữ

Lượt001 có lỗi deepcopy trong recorder của T-014, gây RecursionError sau skeleton và KeyError khi chưa có matrix. Không dùng nó làm bằng chứng lỗi PC. Đã giữ NPZ, từng JSON, progress và console; giải thích ở `pc-fixtures-001/loi-bo-ghi.md`. Lượt002 sửa recorder nhưng giữ cùng seed/input/config. Default không recorder cho cùng matrix ở chain và collider, nên không chỉ dựa lời khẳng định “đã sửa”.

## Kiểm constructors của meta types

Theo yêu cầu tách lỗi cấu hình, `check_set_construction.py` kiểm seeds0–5 trên Python của T-014-main; kết quả ở `set-construction-comparison.json`. Cặp `set('TSLE')` và `set(['T','S','L','E'])` có cùng membership và cùng iteration order ở cả sáu seed. Các effects SLE/LE/E/T cũng giữ cùng order giữa constructor trực tiếp và nhánh list/intersection types. Đây chỉ loại trừ đúng constructor pair đã hỏi; không chứng minh hai skeleton/graphs tương đương hay xác định seed của graph cũ chưa ghi provenance.

## Kiểm bổ sung cơ chế định hướng nhạy thứ tự

Sau lượt PC đảo cột trên ca Train Ticket, skeleton giữ nguyên nhưng667cặp endpoint và258/270điểm đổi. Lần chạy này cũng đổihost/compiler nên không quy riêng mọi khác biệt cho cột. Fixture mới trên cùng máy chỉ đổi nodeorder, giữ chaina-b-c-d và separating sets theo tên giống nhau, đã đổi hướng cạnhb-c. Rule tính tay độc lập khớp hàm chính thức.

`stable=True` trong SkeletonDiscovery chỉ gom xóa cạnh cuối lượtdepth. PC mặc định dùng`uc_priority=2`: ưu tiên collider đã địnhhướng. UCSepset duyệt triple theo chỉsốnode, vì vậy xungđột có thể được xử lý khác khi đổi chỉsố. Fixture dùng separating sets giả được ghi rõ, không códataset/nhãn vàkhông phải replay sepsets của caTT. Nguồn: orientation-order-fixture.json; check_orientation_order.py; causal-learn0.1.3.8 PC.py25–26/111–116, UCSepset.py40–42/95–111, GraphClass.py92–107. Đây là điều kiện thực thi cần báo choG1, không đổi uc_priority để lấy điểm cao hay để làm kiểm đạt.
