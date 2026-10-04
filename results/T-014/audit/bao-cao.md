# Kiểm độc lập CIRCA và các task cũ

Thực hiện ngày 04/10/2026. Chỉ ghi `results/T-014/audit/`; không sửa tài liệu hay đầu ra của task cũ. Laptop có phiên khác đang chạy, nên thời gian trong log chỉ là số chẩn đoán, không phải phép đo thời gian chính thức.

## 1. Phép kiểm đã triển khai

Script `check_original.py` dùng Python của môi trường `py312-pin` đã có, không cài thêm gói. CIRCA gốc được import trực tiếp từ clone của T-014; không sao chép hay sửa scorer của tác giả. Đối chiếu RHT (regression-based hypothesis testing, kiểm định bằng phần dư hồi quy) của CIRCA gốc với lớp RHT và hàm `rht()` của RCAEval.

Ca được cố định trước khi chạy: `fse-ob/cartservice_cpu/1` và `fse-ob/cartservice_mem/1`, lấy lần lặp đầu của hai cấu hình CPU/MEM của cartservice. Không chọn theo kết quả mới. Chỉ runner biết đường dẫn; scorer nhận metric, đồ thị, mốc và SLI (service level indicator, chỉ báo chất lượng dịch vụ) độc lập với nhãn. SLI ở đây là nút đầu, RHT không đọc giá trị này. Không dùng nhãn khi dựng đồ thị hay tính điểm.

Dữ liệu được chuẩn bị như T-006 `chay_fse.py --length 10`, rồi tiền xử lý bằng RCAEval. PC (Peter–Clark, học đồ thị qua kiểm định độc lập) dùng `pc_default` nguyên trạng. Giữ đúng cách chuyển cạnh của `rht()` rồi đưa cùng đồ thị vào hai scorer. Một cấu hình phụ chỉ thêm lại các nút cô lập để kiểm tập ứng viên; không dùng cấu hình này thay kết quả RCAEval. Chạy lại scorer gốc trên cùng đồ thị để kiểm tính lặp lại. Registry ở `cases.csv` ghi từng cấu hình và lý do a/b.

Số lấy từ `cartservice_cpu_1_comparison.json`, `cartservice_mem_1_comparison.json`:

| Ca | Metric không hằng đưa vào PC | Metric được chấm | Cạnh có hướng sau chuyển đổi | Metric cô lập bị mất | Sai khác lớn nhất giữa scorer gốc và RCAEval |
|---|---:|---:|---:|---|---:|
| CPU/1 | 45 | 44 | 86 | `main_cpu` | 0 |
| MEM/1 | 47 | 46 | 77 | `adservice_error` | 0 |

- Hai lần scorer gốc cho cùng điểm từng metric. Hàm `rht()` và lớp `RHTScorer` cũng cho cùng điểm từng metric.
- Cả hai đồ thị có chu trình. Không gọi chúng là directed acyclic graph (DAG, đồ thị có hướng không chu trình).
- Tập ứng viên mới khớp JSON cũ của T-006. Thứ hạng cũ giảm dần theo điểm mới, kể cả các nhóm hòa.
- Khi giữ lại nút cô lập, scorer gốc tính được `main_cpu=2.164937935933773` và `adservice_error=0`; nguồn là `original_isolate_scores` trong hai JSON. Không có nhãn đi vào phép tính này.
- Đây là bằng chứng tại hai ca, không chứng minh toàn bộ dataset tương đương. Điểm không khác trên cùng đồ thị loại trừ được giả thuyết khác biệt scorer ở hai ca; nó không loại trừ khác biệt nguồn đồ thị, cửa sổ, chuẩn bị dữ liệu hoặc phiên bản PC tác giả đã dùng.

## 2. Đường CIRCA-PC bỏ ứng viên cô lập

`RCAEval/graph_heads/rht.py:308–343` tạo danh sách `nodes`, nhưng chỉ gọi `graph.add_edge`, không thêm tất cả nút vào đồ thị. `RCAEval/classes/data.py:223` lấy `graph.nodes` làm tập cần tải. Vì vậy metric PC không có cạnh bị loại trước chấm điểm. Code gốc `circa/graph/common.py:66–68` thêm nút trước khi thêm cạnh.

Phép kiểm thực trên hai ca ở §1 xác nhận hiện tượng. Fixture trong `synthetic.json` xác nhận thêm: PC toàn ma trận 0 trả `ranks=[]`; một đồ thị có cạnh giữa a/b và c cô lập chỉ còn a/b. Không có exception hay nhánh trả thứ tự cột ở trường hợp PC rỗng. Do đó kiểm chỉ có exception và nhánh dự phòng không đủ để xác nhận tập ứng viên hợp lệ.

Không kết luận hiện tượng này giải thích lệch MEM=0,148 trên fse. Hai ca không phải toàn bộ ô MEM, và hai nút cô lập vừa tìm không phải service nhãn gốc. Muốn quy nguyên nhân cho ô cần đúng cấu hình tác giả hoặc phép so có đồ thị/candidate được kiểm soát, nằm trong việc tiếp theo nếu ngân sách cho phép.

## 3. Mốc công bố và các nguyên nhân lệch còn lại

Đã tra nguồn trước lượt chạy mới:

- [BARO](https://arxiv.org/html/2405.09330), §4.4: thay call graph (đồ thị gọi) của CIRCA bằng PC. §4.8.2: alpha mặc định 0,05. Bảng 3 CIRCA[t_inject], fse-ob: CPU 0,90, MEM 0,74, DELAY 0,90, LOSS 0,55, AVG 0,77; fse-ss: 0,97/0,98/0,98/0,88/0,95. Các số trong `results/T-006/scripts/moc.py` khớp bảng đang công bố.
- [TORAI](https://arxiv.org/html/2604.13522v1), §4.4 mô tả CIRCA dùng call graph; §4.8.2 về dữ liệu **real-world** nói CIRCA học PC trên mọi time series. Câu sau không xác định chắc cấu hình Bảng 2–4 trên dataset public. Do đó nguồn đồ thị của các bảng này vẫn OPEN. Không suy câu mô tả call graph thành bằng chứng tác giả đã chạy biến thể kiến trúc.
- Bảng 8 TORAI ghi CIRCA Train Ticket 312,77 giây/ca. Quy 30 ca thành 9.383,1 giây, khoảng 2,61 giờ. Đây chỉ là ước lượng tổng từ máy và giao thức tác giả, không dự đoán đáng tin cho ca RE2-TT hiện tại; T-005 đã có ca vượt một giờ.

Code PC gốc có khác biệt có thể ảnh hưởng kết quả: `circa/graph/r/causal.R:11–14` dùng `pcalg::pc`, `skel.method="stable.fast"`, `maj.rule=TRUE`, `solve.confl=TRUE`; RCAEval `graph_construction/pc.py:12–21` dùng mặc định causal-learn. Chúng không chỉ khác ngôn ngữ hay phiên bản: quy tắc collider (nút va chạm) và xử lý xung đột định hướng có thể khác. Đã chạy `causal.R` nguyên trạng bằng runtime riêng; kết quả ở §3.1 và §5.

Fixture `direction.json` dùng chính `causallearn.GeneralGraph.add_directed_edge(a,b)` và bắt `MemoryGraph` mà hàm `rht()` chính thức nhận. Ma trận có `adj[a,b]=-1`, `adj[b,a]=1`, nhưng cạnh cuối là b→a. Vì vậy đường chuyển cạnh của RCAEval đảo chiều cả cạnh PC đã có hướng; không chỉ đổi cạnh vô hướng thành hai chiều. Đây là lỗi ngữ nghĩa đồ thị có chứng cứ trực tiếp. Nó làm đổi tập parents (cha) dùng hồi quy. Chưa thể quy toàn bộ chênh ô công bố cho lỗi này, vì graph/cửa sổ/backend công bố chưa xác định.

RHT của RCAEval có context khác mức mô tả thường hiểu từ `--length`: `lookup_window=120`, `detect_window=10`, interval một giây, train_window=111 (`classes/data.py:157–177`; `rht.py:361–365`). Tập tải là từ mốc−120 đến mốc+300; học dùng 111 điểm đầu, kiểm dùng 10 điểm cuối. Cửa sổ 10/20 phút làm đổi dữ liệu học PC; không đồng nghĩa RHT học 300/600 điểm. Endpoint ở mốc+300 còn có thể được nội suy từ điểm cuối khi input chỉ tới mốc+299. T-006 chưa lưu intermediate values (giá trị trung gian) đủ để phân xử mọi hiệu ứng này ở ô MEM.

Các giả thuyết cần phân biệt:

| Giả thuyết | Trạng thái trong nhánh này | Phạm vi bằng chứng |
|---|---|---|
| RHT bị chép sai từ CIRCA gốc | Không thấy khác ở hai ca | Max diff 0 với cùng đồ thị/context; chưa kiểm mọi ca |
| Node cô lập bị bỏ khỏi candidate | Đã xác nhận | Hai ca thật + fixture PC rỗng |
| Khác PC R/causal-learn, collider, conflict rule | Đã kiểm có tác động trên hai ca và một ô MEM | Backend đổi graph; target đồng thời giữ node và sửa ngữ nghĩa chiều, chưa tách riêng mọi yếu tố |
| Chiều PC bị đảo ở RCAEval | Đã xác nhận | Actual GeneralGraph + actual rht capture; sửa chiều trên MEM/1 đổi hạng service 2→1 |
| Linear/SVR và RHT/DA khác cấu hình | Đã kiểm riêng scorer trên MEM25 | Cùng Rgraph/candidate/window, các cấu hình cho số khác nhưng đều không khớp mốc |
| Bài dùng lưới alpha thay alpha 0,05 | Chưa có căn cứ | BARO ghi default 0,05; không được dò theo accuracy |
| Bài dùng graph kiến trúc | OPEN cho bảng public TORAI | Mô tả chưa đủ xác nhận cấu hình bảng |
| Windows/Linux hoặc phần mềm | OPEN | Hai scorer cùng Windows khớp; không thay được kiểm PC trên R/Linux |
| Cửa sổ/preprocess khác | OPEN cho cấu hình công bố chính xác | T-006 đã thử length10/20; RHT và PC dùng cửa sổ khác nhau |

### 3.1. Kiểm backend, chiều và cấu hình scorer

Hai ca cố định có output ở `r-comparison-summary.json`. Trên full600 điểm như input PC của T-006, R-pcalg nguyên trạng cho 119 cạnh ở CPU/1 và 90 cạnh ở MEM/1; causal-learn sau chuyển ngữ nghĩa đúng cho 86 và 77. Số cạnh khác là 57/53. Giữ tất cả node trong các cấu hình so này. Hạng cartservice ở MEM/1 là 2 với đường RCAEval thật, 1 khi sửa chiều và 1 với Rgraph. Đây là hai ca được chọn trước chạy, không suy thành kết luận toàn ô.

Sau bằng chứng này, SPEC mở kiểm targeted (kiểm đúng một ô) 25 ca MEM fse-ob trước chạy ô đó. Không benchmark toàn 100 ca, không mở dữ liệu mới. Dùng R-pcalg trên cùng input600 đã chuẩn bị, alpha=0,05, m.max=Inf, numCores=1; RHT gốc dùng context111/10 điểm, interval1s, current=mốc+300. Giữ tất cả node; graph R có cạnh đúng chiều theo ma trận R. `cartservice_mem/1` dùng lại graph đã có sau assert input giống hệt. Chấm service bằng bỏ trùng giữ thứ tự, như `cham.py` T-006. Điểm và thứ hạng được ghi trước khi runner đọc service nhãn để chấm.

Nguồn: `mem-target-summary.json`, `mem-prior-config-summary.json`. Đây là số chẩn đoán protocol, không dùng để chọn biến thể hay đổi cấu hình mặc định.

| Cấu hình trên ô MEM fse-ob (25 ca) | AC@1 | AC@3 | Avg@5 | So với mốc BARO 0,74 |
|---|---:|---:|---:|---:|
| RCAEval T-006, dùng lại kết quả | 0,68 | 0,92 | 0,888 | +0,148 |
| Rgraph + linear RHT | 0,60 | 0,96 | 0,864 | +0,124 |
| Cùng Rgraph + SVR(sigmoid) RHT | 0,80 | 1,00 | 0,960 | +0,220 |
| Cùng Rgraph + linear RHT+DA (threshold3) | 0,76 | 0,84 | 0,856 | +0,116 |
| Cùng Rgraph + SVR(sigmoid) RHT+DA (threshold3) | 0,60 | 0,92 | 0,864 | +0,124 |

SVR và DA được lấy từ prior work (công trình trước): config cuối artifact `source/updated-config/params-oracle-run.json` dùng structural/SVR/tau_max0; code pin `models.py:580–586` tạo SVR(kernel="sigmoid"), và `:630` đặt DA threshold3. Artifact cập nhật có revision khác pin của task; chỉ dùng như nguồn cấu hình, không gọi nó là cùng code pin hoặc bằng chứng lệnh đã sinh bảng BARO. Các biến thể này được thêm vào SPEC trước lượt thử chúng, và đều được giữ. Không có cấu hình nào khớp mốc0,74; không có căn cứ chọn cấu hình gần nhất để thay số cũ.

Đổi Rgraph, chiều và tập ứng viên cùng lúc làm Avg@5 giảm0,024. Vì ba yếu tố đổi cùng nhau, số này không phải tác động riêng của pcalg hoặc riêng đảo chiều. Linear→SVR và thêm DA được tách trên cùng graph/candidate/window, nên tác động của scorer trong bảng có căn cứ. Chúng chưa giải thích đủ ô lệch0,148.

Giới hạn: đây là gọi `causal.R` gốc và scorer gốc có kiểm soát; không phải chạy toàn factory/loader experiment gốc. Factory gốc học PC từ `CaseData.load_data`, trong khi target cố ý cho PC full600 để giữ input PC như RCAEval. Không có lệnh/bản code sinh bảng BARO trong repo BARO pin của T-001; tìm code chỉ thấy nhắc CIRCA trong docs thời gian. Nhánh RCAEval `ase24` vẫn dùng linear RHT, không DA, cùng cách đảo chiều, nhưng tên nhánh chưa chứng minh nó sinh bảng BARO. Vì vậy cấu hình công bố còn OPEN; thiếu lệnh tác giả là lý do cụ thể, không phải thiếu quyền cài R.

Kiểm lặp/hoán vị PC R trên hai ca: ma trận giống từng phần tử khi chạy lại và khi đảo thứ tự cột rồi map về thứ tự cũ (`pcalg-repeat.csv`). SVR lặp trên ca MEM đầu cũng maxdiff0. Tính độc lập DA từ graph/rawscore, theo đúng hash tuple và cách duyệt SCC của code, khớp mọi điểm trên 25×2 cấu hình DA (`verification.json`). 25×4 variant đều có điểm hữu hạn và ranking không rỗng. Ranking linear không trùng thứ tự cột. Công thức Avg@5 độc lập cũng khớp mọi số bảng. Không thấy exception/regression fallback trong lượt target thành công.

Fixture DA có chu trình ở `da-cycle.json` cho một điều kiện thất bại thêm. Cùng a→b→c, c→b và rawscore a=4,b=1,c=4, threshold3, sáu hashseed cho điểm c=5 hoặc8. Đồ thị DAG đối chứng a→b→c cho cùng điểm mọi seed. Vì trong một SCC (strongly connected component, thành phần liên thông mạnh), `child_scores` của child có thể đã có hoặc chưa có theo thứ tự set, DA thay đổi cả điểm, không chỉ thứ tự hòa. Đây là kiểm giả không dữ liệu/nhãn. Không suy nó giải thích ô MEM25 hay mọi đồ thị kiến trúc. Nó là lý do cơ chế để thận trọng với DA trên PC có chu trình; không chọn RHT-only từ điểm cao hơn.

Lượt PC target150,02s; scorer linear21,234s; ba cấu hình scorer bổ sung18,594s theo log. Đây là thời gian chẩn đoán trên laptop dùng chung, không phải số chi phí chính thức. Tổng thấp hơn budget15phút/dataset của nhánh. Giữ cả lượt prior đầu hỏng do networkx2.5 thiếu `topological_generations`; đổi sang môi trường T-014-main đã có networkx2.8.8, không sửa môi trường chỉ đọc. Mọi điểm linear recompute trong môi trường mới khớp số trước đó trên25ca. Kiểm độc lập DA lần đầu không khớp vì script dùng hash của chuỗi tên và cách duyệt SCC khác code; lượt2 giữ cùng hash tuple/thứ tự set của code và khớp từng điểm. Cả hai log kiểm giữ nguyên; không che khác biệt biểu diễn khi có SCC.

## 4. Vấn đề ở task cũ — để reviewer kiểm

### N1 — T-001 diễn đạt sai xử lý tên cột

- File: `results/T-001/danh-sach-phuong-phap.md:60`.
- Cũ: `tên cột dạng service_metric, cột khác dạng bị bỏ im lặng`.
- Sai gì: tên không có dấu `_` không bị bỏ; `rht.py:308` truy cập token thứ hai rồi ném `IndexError`. Wrapper có thể trả thứ tự cột. Tên có nhiều dấu `_` bị cắt hai token, tạo đường chập nút/bỏ dữ liệu khác.
- Bằng chứng: `synthetic.json` ghi lỗi `IndexError: list index out of range` khi gọi `rht()` trực tiếp với cột `cpu`. Code `e2e/__init__.py:22–35` thể hiện nhánh dự phòng.
- Ảnh hưởng: yêu cầu định dạng đầu vào và phép kiểm nhánh dự phòng. Không suy thành lỗi điểm T-006 vì hai ca vừa chạy dùng tên tương thích.
- Đã triển khai: fixture trên scorer chính thức; lưu lỗi thật. Không sửa T-001.
- Đề xuất mới: `tên cột phải tách được đúng service_metric; cột không có '_' làm hàm lỗi và wrapper có thể trả thứ tự cột. Tên có nhiều '_' bị cắt hai token, có thể chập nút hoặc thiếu dữ liệu; adapter phải kiểm tính tương thích trước gọi.`

### N2 — T-006 nói rộng hơn phạm vi kiểm hashseed

- File: `results/T-006/kiem-dung-dan.md:186,216`.
- Cũ: `Thứ tự nút do hash: không đổi top 5` và `top 5 giữ nguyên ở 6 seed, nên Avg@5 không đổi`.
- Sai gì: script `results/T-006/scripts/soi_circa_hashseed.py:khac[:4]` chỉ kiểm bốn ca trong 15 ca có ranking khác. Log `runs/25-soi-circa-hashseed.log` xác nhận bốn ca. Hai lượt chính thức trên 90 ca có cùng điểm từng ô, nhưng đó là bằng chứng khác, không chứng minh mọi seed giữ top5 ở cả 90 ca.
- Ảnh hưởng: phạm vi kết luận tính tất định; không làm thay đổi các số đã chấm của hai lượt chính thức.
- Đã triển khai: kiểm script và log thật; tái lập điểm không nhãn trên hai ca ở §1. Không đổi seed hay benchmark thêm cả dataset.
- Đề xuất mới: `Ở bốn ca được kiểm với sáu hashseed, top5 giữ nguyên. Hai lượt chính thức trên 90 ca cho cùng điểm từng ô. Chưa kiểm mọi hashseed trên tất cả ca; không suy kết quả bốn ca thành bảo đảm tất định toàn dataset.`

### N3 — T-001/T-006 thiếu thông tin tập ứng viên thật của CIRCA-PC

- Nơi cần bổ sung: `results/T-001/danh-sach-phuong-phap.md:60`, `results/T-006/kiem-dung-dan.md:160–168`.
- Thiếu gì: mô tả không cho biết metric PC cô lập bị loại khỏi candidate, đồ thị rỗng có thể trả ranking rỗng dù không có exception. Không khẳng định các con số T-006 sai chỉ vì thiếu mô tả.
- Bằng chứng và triển khai: §1–2 và ba fixture/JSON. Tại CPU/1 và MEM/1, candidate cũ đúng là subset sau loại cô lập.
- Ảnh hưởng: đơn vị/tập xếp hạng và kết luận đầu vào. Khi đổi nguồn đồ thị cần báo cả số metric vào PC, node graph và metric scored; không coi graph khác là chỉ đổi parents nếu candidate cũng khác.
- Đề xuất bổ sung nguyên văn: `CIRCA-PC RCAEval chỉ thêm cạnh khi dựng MemoryGraph; metric không có cạnh PC không được chấm. PC rỗng có thể cho ranking rỗng mà không ném lỗi. Tập metric sau preprocess và tập ứng viên được chấm có thể khác nhau; lưu cả hai để diễn giải kết quả.`

### N4 — Các hồ sơ cũ thiếu lỗi đảo chiều cạnh PC có hướng

- File: `results/T-001/danh-sach-phuong-phap.md:60`; `results/T-006/kiem-dung-dan.md:160–166` mô tả PC+RHT nhưng không báo ngữ nghĩa chiều bị đổi.
- Sai/thiếu gì: `rht.py:318–343` rồi `graph.reverse()` làm cạnh GeneralGraph a→b thành b→a. Do RHT hồi quy trên parents, đây là đổi mô hình chấm điểm, không chỉ đổi cách hiển thị graph.
- Bằng chứng: `check_direction.py`, `direction.json`; actual GeneralGraph ma trận[-1,1], actual graph nhận cạnh ngược. Trên MEM/1, cấu hình sửa chiều nhưng giữ node làm hạng service2→1 (`r-comparison-summary.json`).
- Ảnh hưởng: mô tả code khác bài và khả năng diễn giải cha/con; không sửa số T-006 và không gọi lỗi này là nguyên nhân đủ của ô0,148.
- Đã triển khai: fixture actual API; so graph/scorer không nhãn trên hai ca; target MEM25 thêm nguồn graph R gốc, lưu mọi variant. Không sửa file task cũ.
- Đề xuất thêm: `Đường chuyển adjacency của rht đảo chiều cạnh PC đã có hướng so với GeneralGraph của causal-learn. RHT thật dùng parents của graph sau đảo chiều. Tách lỗi ngữ nghĩa này khỏi việc cạnh vô hướng thành hai chiều và khỏi sai khác backend PC; chưa quy toàn bộ chênh số công bố cho nó.`

### N5 — “Chỉ khác graph/DA” là mô tả thiếu cấu hình paper

- File: `results/T-001/danh-sach-phuong-phap.md:60` (`khác bài ở hai thành phần: đồ thị và DA`); `results/T-005/do-kha-thi.md:61` (`chỉ khác bước dựng đồ thị`).
- Thiếu gì: default lớp RHT là linear, nhưng prior-work real/Oracle config của CIRCA dùng SVR(sigmoid); structural canonical còn dùng DA. Khi gọi biến thể “như bài gốc”, không được suy chỉ thay graph mà các thành phần còn lại tương đương.
- Bằng chứng: config whitelist cuối artifact ở `source/updated-config/params-oracle-run.json`; factory pin `models.py:580–586,630`; lớp default `alg/ci/anm.py:18–20`. Nguồn bài/hồ sơ riêng của T-014 xác định SVR+DA trên real/Oracle. Artifact cập nhật khác revision pin, nên giữ ranh giới nguồn.
- Ảnh hưởng: yêu cầu đầu vào, lựa chọn RHT/RHT+DA và diễn giải so hai biến thể; không phủ nhận có thể dựng một adaptation kiến trúc dùng chung linearRHT nếu ghi rõ đó là lựa chọn của task.
- Đã triển khai: cùng25Rgraph kiểm riêng linear/SVR/DA, lưu từng điểm/params/rank; không chọn từ điểm. So samegraph hai ca đã xác nhận scorer linear gốc và RE khớp.
- Đề xuất đoạn mới: `CIRCA-PC RCAEval dùng causal-learn và linear RHT, không DA. Bản structural theo real/Oracle prior work dùng SVR(sigmoid)+DA(threshold3); đổi graph đơn thuần tạo adaptation dùng chung scorer nhưng chưa phải cùng cấu hình paper. Hồ sơ cần ghi thêm cửa sổ, xử lý node cô lập và ngữ nghĩa chiều cạnh.`

## 5. R/pcalg: đã dựng và chạy không-admin

Kiểm ban đầu không thấy R/7z trên PATH hay các thư mục Program Files thường gặp. Theo [R Windows FAQ](https://cran.r-project.org/bin/windows/base/rw-FAQ.html), thiếu admin không chứng minh R không cài được. Đã giải nén installer R bằng innoextract1.9 chính thức vào work/T-014, không chạy installer; không registry/shortcut. R4.4.2 + pcalg2.7-12 + graph/RBGL và dependencies dùng binary ghim, thư mục library/tmp/cache ở task. Nguồn/hash/byte và lệnh dựng trong `moi-truong-r.md`, `r-downloads.json`, `r-packages-installed.csv`, `external-files.csv`. Cảnh báo locale/build-R giữ nguyên; chúng không làm lượt PC lỗi.

Lượt metadata đầu Bioconductor trả HTTP403, đã giữ `r-packages-setup.log`; lượt sau dùng mirror Posit trong danh sách official và chạy thành công. Tổng tải mạng đã biết131.175.732B gồm runtime/công cụ/gói/metadata và ba file Figshare, dưới1GB. Không tải dataset mới. Không cài admin/toolchain.

Figshare ba payload chỉ được mở archive directory và extract whitelist code/config/README; không đọc `cache.zip` hay kết quả từng ca/rawdata Oracle/synthetic. Vì vậy không có lệnh chạy trên dataset mới hoặc dùng label artifact để chọn cấu hình. Artifact cập nhật và supplementary được giữ với MD5 khớp metadata nguồn.

## 6. Bàn giao nhánh

Danh sách file repo của nhánh ở `output-files.csv`; mọi file ngoài repo do nhánh tạo dưới downloads/tools/R/R-library/audit-r được liệt kê từng file kèm hash/byte trong `external-files.csv`. Registry `cases.csv` cần gộp vào `results/T-014/ca-da-chay.csv` của nhánh chính. Không SSH, không commit/push, không sửa file task cũ hay tài liệu chung. Dùng môi trường T-014-main của nhánh chính để DA chạy; không sửa nó.

Coverage (phạm vi soi task cũ) ở `coverage-task-cu.csv`: census tài liệu Markdown top-level T000–T012, đọc sâu CIRCA T001/T005/T006, các script chấm/runner/fallback/hashseed liên quan, code pin gốc và nguồn paper. T004 không có task/results trong repo lúc kiểm. T000 đầu ra ở docs/knowledge và tài liệu luật, không có results/T000. Đã đọc REVIEW T003 R1 và phần đánh giá lại; áp dụng bài học bằng làm mọi kiểm rẻ được phép, dựng R thật và không trình việc còn chưa làm thành “chờ quyền”. Không tự gọi đây là audit mọi artifact/dataset/phương pháp của T000–T012.

Điều còn OPEN: code/lệnh tạo bảng BARO/TORAI public và phiên bản PC tác giả thật; tác động riêng từng backend/chiều/candidate trên toàn dataset; full experiment factory gốc và môi trường2022. Đã làm các kiểm rẻ trong scope để phân biệt scorer/graph/cấu hình, nhưng không dò cửa sổ/alpha/regressor theo điểm. Không có đủ input nguồn để gán nguyên nhân duy nhất cho phần chênh còn lại. Khi có code/lệnh tác giả, sẽ kiểm được giả định “protocol giống target full600 + context111/10”; nếu input/factory khác thì giả định đó sai. Nguồn chưa biết này không cho phép coi số T006 đã sai, cũng không cho phép gọi đã tái lập số công bố.

## 7. Bổ sung phân xử chiều và coverage trên đồ thị đã lưu

Không học lại PC. Cố định trước điểm ba thay đổi trên25R-pcalg graph MEM: bỏ isolate; đảo chiều và giữ isolate; đảo chiều và bỏ isolate. Baseline forward/keep dùng lại. Cửa sổ, linear RHT và bộ dữ liệu giữ nguyên. Nhãn chỉ đọc sau khi lưu các điểm/thứ hạng. Script `isolate_graph_factors.py`; phép đếm độc lập `verify_saved_factors.py` không import scorer.

| Hướng Rgraph | Giữ isolate | Avg5 |
|---|---|---:|
| Chiều gốc của R | có | 0,864 |
| Chiều gốc của R | không | 0,864 |
| Đảo chiều | có | 0,896 |
| Đảo chiều | không | 0,896 |

Nguồn: `graph-factor-summary.json`, điểm/rank từngca ở `graph-factors/`, kiểm100configuration ở `graph-factor-verification.json`.75lượt scorer mới mất11,906s (chẩn đoán trên laptop dùng chung). Việc bỏisolate giữ nguyên điểm các ứng viên còn lại trong tolerance. Vì vậy trên đúng cácRgraph/cửa sổ này, đảo chiều đổiAvg5+.032; bỏisolate không giải thích lệchaggregate. Không suy đó là tác động tương tự trên mọicausal-learn graph, hoặc rằng isolate không ảnh hưởng ở ca khác. Các sourcegraph/parents khác có thể đổi cả candidate và hiệu quả hồi quy.

Rgraph đảo chiều cho.896, trong khi T006 reused.888; cảhai vẫn cao hơn mốc.740. Sai chiều đã có chứng cứcode và ảnh hưởng, nhưng sửa chiều không tái lập sốpaper. Giao thức côngbố, backend/rules và window/preprocess vẫn có thể giải thích phần lệch còn lại. Không chọn cấu hình từ điểm cao hay gầnpaper.
