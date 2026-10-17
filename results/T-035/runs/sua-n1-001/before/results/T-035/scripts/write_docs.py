import sys,json
from pathlib import Path
from run import ROOT,OUT,read

def save(name,text):
    with (OUT/name).open('x',encoding='utf-8') as f:f.write(text)
s=read(OUT/'thong-ke-do-thi.json');v=read(OUT/'tu-vung-thao-tac.json');n=read(OUT/'cot-node-nezha.json');l=read(OUT/'do-phu-theo-nhan.json')
a=s['datasets']['RE2-TT'];b=s['datasets']['Nezha-OB']
k3=s['K3'];seeds=[read(OUT/'runs'/p/'result.json') for p in ['seed-001-h1','seed-002-h2']]
assert all(x['pass'] for x in seeds) and l['G2_H19_match']

save('thong-ke-do-thi.md',f'''# Đồ thị phụ thuộc từ trace dev — T-035

T-035 đã tạo mô hình chung, bộ dựng và khảo sát hai mức trên toàn bộ dev được duyệt. Đây là kết quả mô tả của P5. Chưa xác nhận đồ thị hoặc mức thao tác giúp chẩn đoán; chưa chọn thiết kế P6, chưa hoàn tất P5/G3.

## 1. Miền dữ liệu và định nghĩa

RE2-TT: toàn bảng span của đúng ca dev. Nezha-OB: toàn tập adapter trả trong cửa sổ dev [t−300,t+300), không là cả file nguồn. N/A chỉ nhận span được bao trọn trong khoảng, cha cũng phải ở trong khoảng; span bắc qua biên không được lấy cha ở ngoài để nối. N là đồ thị tham chiếu trước mốc, chưa có bằng chứng nền khỏe. Đây là mô tả chế độ biết trước cửa sổ; không dùng các đồ thị N/A này làm đầu vào tự phát hiện.

Ảnh chụp RE2 neo **min start của bảng span**, giữ phần lẻ microsecond; lưới 60/300 giây cố định theo neo ấy, end < biên phải. Không đồng nhất neo này với neo theo timestamp metric/giây nguyên của khảo sát cũ. Cảnh báo trong SPEC về biên trùng mốc ở lưới cũ vẫn là việc P6 phải xét; lưới của T-035 không được tạo bằng mốc tiêm. Mức thao tác chỉ lưu full/N/A. Nezha không có ảnh chụp. Nguồn: `thong-ke-do-thi.json#/window_definition`, các graph `interval_ns`.

Đồ thị khác nhau khi tập nút/cạnh khác, bỏ count, witness và timestamp khỏi fingerprint. Độ phủ inventory khác số nút có span. Mọi cạnh dev hiện là gọi-chưa-phân-kiểu: hướng từ owner span cha sang owner span con; chưa xác nhận quan hệ mạng đồng bộ.

## 2. C3–C4: cấu trúc và độ phủ

| Miền | RE2-TT | Nezha-OB |
|---|---:|---:|
| Số ca | {a['cases']} | {b['cases']} |
| Span trong full được phép | {a['span_total']:,} | {b['span_total']:,} |
| Cấu trúc thực thể full | {a['full_entity_shapes']} | {b['full_entity_shapes']} |
| Cấu trúc thao tác full | {a['full_operation_shapes']} | {b['full_operation_shapes']} |
| Ca N/A đổi cấu trúc thực thể | {a['N_A_entity_changed']} | {b['N_A_entity_changed']} |
| Ca N/A đổi cấu trúc thao tác | {a['N_A_operation_changed']} | {b['N_A_operation_changed']} |

Nguồn từng ô: `thong-ke-do-thi.json#/datasets/RE2-TT` và `#/datasets/Nezha-OB`, trường cùng tên. Từng ca/cửa sổ: `#/cases/<i>/windows/<tên>`. Theo ô: `do-phu-theo-nhan.json#/cells`; chỉ ghép nhãn sau khi graph và thống kê không nhãn đã ghi. Một ô không là mẫu hình của toàn dataset.

Ảnh chụp 60 giây: {a['snapshot_shapes']['60']['windows']} khoảng, {a['snapshot_shapes']['60']['distinct']} cấu trúc khác nhau, {a['snapshot_shapes']['60']['empty_windows']} khoảng rỗng. 300 giây: {a['snapshot_shapes']['300']['windows']} khoảng, {a['snapshot_shapes']['300']['distinct']} cấu trúc, {a['snapshot_shapes']['300']['empty_windows']} khoảng rỗng. Nguồn: `#/datasets/RE2-TT/snapshot_shapes`. Vì vậy gần hằng ở full/N/A không đồng nghĩa hằng ở cửa sổ ngắn. Khác biệt có thể do số lời gọi và quy tắc cắt, chưa là thay kiến trúc hoặc do lỗi.

Mọi thực thể U có trạng thái has_edge, span_without_edge hoặc not_observed ở `#/cases/<i>/windows/<tên>/coverage`. Tập ngoài U ghi riêng tại outside_inventory. Đây là độ phủ quan sát của bộ dựng; không có mẫu số số request/span thật đã sinh. Không có cạnh không chứng minh không phụ thuộc; có thể không được gọi, thiếu instrumentation, mất span hoặc cửa sổ ngắn.

K3 tái lập đúng toàn bộ ca RE2-TT và tổng {k3['totals'][0]:,} span; {k3['totals'][1]:,}/{k3['totals'][2]:,} tham chiếu cha resolve. Phân bố nút/cạnh: {k3['node_edge_distribution']}. Nguồn: `runs/kiem-cuoi-001/K3.json#/rows`, `#/totals`, `#/node_edge_distribution`. Các tập nút/cạnh cũng so chính xác với T-002, không chỉ số đếm. Có ba cấu trúc như T-002. Câu hai cấu trúc trong K2 chưa có quy trình/đầu ra gốc ở nguồn được phép để xác định vì sao khác; không sửa K2 hoặc dùng câu ấy thay kết quả hiện tại. Phần chưa biết này không làm mất phép tái lập T-002.

## 3. C1–C2: cạnh nào có bằng chứng

| Loại | RE2-TT | Nezha-OB | Căn cứ |
|---|---|---|---|
| Gọi chưa phân kiểu | Dựng được | Dựng được | trace/span/parent + owner, K1/K4 |
| Gọi đồng bộ xác nhận | Chưa phân xử | Chưa phân xử | Không có kind/định nghĩa đầy đủ của span phía gọi–phía nhận trong export |
| Dữ liệu đến DB/cache | Không dựng được từ export hiện có | Không dựng được từ export hiện có | Tên query không cho endpoint/ownership đã xác minh |
| Thông điệp qua broker/nối bản tin | Không dựng được | Không dựng được | Không có broker/destination/link/message identity đủ nghĩa |
| Triển khai lên máy | Không dựng được | Chưa phân xử Node; chưa dựng cạnh đã xác nhận | Thiếu mapping host có nguồn xác nhận |

Ba trạng thái nói về khả năng dựng từ bằng chứng hiện có, không là khẳng định các quan hệ không tồn tại. Tên thao tác chứa query/database/RPC là gợi ý mô tả, không được biến thành kiểu cạnh hoặc ownership bằng regex. Nguồn từ vựng: `tu-vung-thao-tac.json#/cases`; schema/provenance từng ca: `thong-ke-do-thi.json#/cases/<i>/provenance`. Kiểu quan hệ đã kiểm trên fixture, không là kết quả quan sát thật của hai dataset.

Một lời gọi cấu trúc là cặp span cha–con khác owner resolve được; mỗi sự kiện có hai span làm chứng, khác với số request mạng thật. RE2 có {a['cross_parent_contains']:,}/{a['cross_parent_events']:,} cặp được bao thời gian; Nezha {b['cross_parent_contains']:,}/{b['cross_parent_events']:,}. Nguồn: `#/datasets/<dataset>/cross_parent_contains`, cross_parent_events. Không bao thời gian có thể do clock, bất đồng bộ hoặc semantics instrumentation; phép đếm không phân xử các giải thích này. Histogram số span mỗi trace ở `runs/bo-sung-001/summary.json#/cases/<i>/span_count_per_trace`; không gọi số ấy là số span mỗi request mạng.

Kiểm tay hai trace mỗi dataset tại `kiem-dung-dan.md` hỗ trợ cách giữ quan hệ; không xác nhận kiểu vật lý trên mọi ca. UV-1/UV-2 còn cần semantics phía gọi, thời gian và cây span gốc. Đồ thị thao tác không thay cây/thời gian từng lần thực thi.

## 4. C7–C8: mức thao tác

| Thuộc tính full | RE2-TT | Nezha-OB |
|---|---:|---:|
| Khóa entity+operation khác nhau trên dev | {v['datasets']['RE2-TT']['distinct_entity_operations']} | {v['datasets']['Nezha-OB']['distinct_entity_operations']} |
| Khóa có ở mọi ca | {v['datasets']['RE2-TT']['operations_present_all_cases']} | {v['datasets']['Nezha-OB']['operations_present_all_cases']} |
| Khóa chỉ có ở một ca | {len(v['datasets']['RE2-TT']['operations_one_case'])} | {len(v['datasets']['Nezha-OB']['operations_one_case'])} |
| Tên giống ID theo luật đã khai | {len(v['datasets']['RE2-TT']['candidate_id_names'])} | {len(v['datasets']['Nezha-OB']['candidate_id_names'])} |
| Khóa chỉ tên HTTP method | {len(v['datasets']['RE2-TT']['only_http_method'])} | {len(v['datasets']['Nezha-OB']['only_http_method'])} |
| Tên dùng ở nhiều thực thể | {len(v['datasets']['RE2-TT']['names_multiple_entities'])} | {len(v['datasets']['Nezha-OB']['names_multiple_entities'])} |
| Số chữ ký con lớn nhất cho một thao tác/ca | {v['datasets']['RE2-TT']['max_child_signature_count']} | {v['datasets']['Nezha-OB']['max_child_signature_count']} |
| Độ sâu nội bộ lớn nhất | {v['datasets']['RE2-TT']['max_internal_depth']} | {v['datasets']['Nezha-OB']['max_internal_depth']} |

Nguồn: `tu-vung-thao-tac.json#/datasets/<dataset>`; presence và từng cửa sổ ở `#/cases`. Luật giống ID chỉ là phép mô tả, không chứng minh tên ổn định về nghĩa; không tự chuẩn hóa. Tên HTTP chung có thể gộp nhiều đích. Nhiều chữ ký con có thể do nhánh/tải đầu vào hợp lệ, không tự là lỗi đặt tên.

**Dựng được tới đâu:** có cấu trúc thao tác trên mọi ca/full/N/A và phép chiếu nhất quán. Phần mất cha vẫn bị thiếu quan hệ, không được bù hoặc loại ca khó. Tên Nezha có mặt nhất quán giữa các ca dev; ở RE2 có nhóm chỉ xuất hiện một ca và nhóm HTTP chung, cần kiểm nghĩa với instrumentation/phiên bản nguồn trước khi P6 coi tên là địa chỉ thao tác riêng. Không kết luận mọi thao tác đều được quan sát đầy đủ.

**Có phân biệt hơn mức thực thể không:** có. Cặp cha–con nội bộ được giữ: {a['same_entity_events']:,} sự kiện RE2, {b['same_entity_events']:,} sự kiện Nezha. Nguồn: `thong-ke-do-thi.json#/datasets/<dataset>/same_entity_events`. RE2 có sáu cấu trúc thao tác so với ba thực thể; chiếu đúng tập thực thể/cạnh ở mọi khoảng đã kiểm. Cạnh thực thể có nhiều cặp thao tác được báo theo ca tại `#/datasets/<dataset>/operation_pairs_per_entity_edge`. Không suy lợi ích chẩn đoán từ các số này.

**Còn thiếu:** nghĩa ổn định của tên, kind và endpoint, cây/thời gian mỗi span, xử lý span thiếu, log nối đúng scope và metric thao tác thực. P6 cần so hai mức trên cùng bằng chứng, cửa sổ, tập ứng viên và ngân sách chọn; giữ metric toàn service là bối cảnh chung. Chưa chọn mức nào.

## 5. C4/K8, C6 và C9

K8 tái lập 8 ca không có cạnh gọi đi vào root và 7 ca có cạnh quá thưa; 37 ca có ít nhất một cặp đi vào đủ 20 lời gọi mỗi phía. Nguồn: `do-phu-theo-nhan.json#/totals`, `#/rows`, định nghĩa từ T-032 call_slow_table_v1.py MIN_CALLS. Đếm trên F, chia theo end của span cha; khác với N/A containment của ảnh đồ thị, không ép hai quy tắc cho cùng số đếm. Nhóm D5 tái lập 949/1.293 trace A mất cha; chi tiết scope ở `#/rows` của dev-746fd74313.

Node: có {len(n['distinct_Node'])} giá trị, từng pod có một giá trị ổn định trên các cửa sổ đã đọc; service có thể có nhiều pod/Node ở hai ngày. Giá trị dạng IP và tính ổn định chưa xác nhận host. Nguồn và phần thiếu ở `cot-node-nezha.md`, JSON; không dựng cạnh triển khai đã xác nhận.

K6 so hai chiều trace với metadata mức ngày; nguồn sinh/tính độc lập chưa xác nhận. Không đọc Weight/chuỗi số, không dùng các cặp đó bổ sung cạnh hoặc chọn P6. C9 ở `thong-tin-theo-quan-he.md` phủ mọi quan hệ, đối chiếu B16 và nêu trường/khóa còn thiếu. Chưa ban hành yêu cầu P9a, chưa sửa FlashTicket.

## 6. Tiêu chí xong và bàn giao

| Tiêu chí SPEC | Trạng thái | Bằng chứng/giới hạn |
|---|---|---|
| 1. Mô hình chung đủ nút/cạnh | Đạt | dac-ta-do-thi.md; fixture; thành phần thiếu dev vẫn có trong mô hình |
| 2. C1 theo loại cạnh/dataset | Đạt | Mục 3; từ vựng/provenance; trạng thái không dựng/chưa phân xử được giữ |
| 3. C2 và giả định | Đạt trong phạm vi mô tả | Cặp cấu trúc; containment/histogram/kiểm tay; kiểu mạng OPEN |
| 4. C3 theo ca | Đạt | JSON mọi ca/cửa sổ và theo ô; full khác cửa sổ ngắn |
| 5. C4, mọi inventory, K8 | Đạt | Coverage từng thực thể và đối chiếu 8+7; không quy nguyên nhân thiếu |
| 6. K1–K7 và F1–F11 | Đạt | kiem-dung-dan.md; K6 chỉ là kiểm mô tả, không đối chiếu độc lập đã xác nhận |
| 7. C6 nghĩa Node hoặc OPEN | Đạt với OPEN | Cần mã collector/export hoặc định nghĩa cột cụ thể |
| 8. C7–C8 ba câu | Đạt | Mục 4; chưa chứng minh lợi ích, nghĩa tên HTTP chung còn thiếu |
| 9. C9 đầy đủ | Đạt | Bảng quan hệ, lý do và nơi nhận; runtime FlashTicket chưa kiểm |
| 10. Bộ dựng không nhận nhãn | Đạt | Chữ ký API, fixture từ chối nhãn; runner/report tách barrier |

Kết quả task đã hoàn tất để chờ Claude phản biện và Minh nghiệm thu. Chưa tự nghiệm thu/đóng task, RQ3, P5 hoặc G3. C1–C9 trả lời khả năng dựng và giữ thông tin; không trả lời đồ thị khắc phục hạn chế RCA hay không.

T-036 nhận mô hình v1, graph/coverage và metadata K6: dựng inventory/cạnh tĩnh có revision cho Train Ticket, Online Boutique và FlashTicket; đối chiếu hai nguồn. P6 nhận bảng C5 và các giới hạn C2/C7 để chọn tín hiệu/cơ chế/mức; không suy lợi ích từ số cấu trúc. P9a nhận bảng thông tin để Minh duyệt từng yêu cầu. P9b cấp trace thật chuẩn hóa; phép so với nguồn tĩnh FlashTicket phải được giao trong SPEC tương ứng.

Chi phí lượt đầy đủ: {s['cost']['full_run_seconds']/60:.2f} phút, RAM đỉnh {s['cost']['peak_rss_bytes']/1024**3:.2f} GiB. Nguồn `thong-ke-do-thi.json#/cost`; thời gian từng ca/bước/cửa sổ và lượt dừng hiệu năng ở runs/. Giữ mọi lượt; không tải, không dùng EC2, không mở test/heldout. Mọi hash nằm trong manifest. Prompt Claude trong LOG Phiên 6 và prompt-claude-soat-ket-qua.txt; Minh chuyển thủ công.
''')

save('cot-node-nezha.md',f'''# Cột Node của Nezha-OB

**Kết luận: OPEN về nghĩa host.** Chưa dựng cạnh triển khai đã xác nhận. Có {len(n['distinct_Node'])} giá trị Node và {len(n['pod_to_nodes_all_dev'])} pod gốc trên các cửa sổ dev. Mỗi pod gắn một giá trị trong phần đã đọc; productcatalogservice có hai pod ở hai ngày. Tính ổn định và tên dạng IP chỉ hỗ trợ tính nhất quán, không xác nhận nguồn định danh host. Nguồn số: `cot-node-nezha.json#/distinct_Node`, `#/pod_to_nodes_all_dev`, `#/cases`.

Reader dùng lại selection/hash/path guard của p3, lọc timestamp theo [t−300,t+300) trước khi xuất PodName/Node, đối chiếu Timestamp với TimeUnixNano và alias tường minh. Không sửa p3; không xuất Log, Node* numeric series hoặc dữ liệu ngoài dev. Thống kê từng phút ở `#/cases/<i>/per_minute` và tên cột Node* ở metric_Node_headers; không dùng chúng làm bằng chứng host riêng.

Đã đọc README, paper và mã phân tích đã tải; inventory mã dưới data/nezha không có mã thu bổ sung. Bài Nezha trang 8 mô tả Kubernetes và Node Exporter; không chỉ rõ cột Node của log được export từ khóa nào, hoặc những giá trị này có scope nào. README và mã analysis không cung cấp mapping host cụ thể. Nguồn trực tiếp và phần thiếu: `#/source_review`, `#/missing`. Không suy rằng dataset hoàn toàn không có quan hệ dịch vụ–máy; chỉ chưa đủ căn cứ nhận mapping này là host.

Để phân xử: cần mã collector/export định nghĩa cột, hoặc mô tả schema liên kết Node với hostId thật. Minh có thể giao nguồn bổ sung theo phạm vi riêng; không tải trong task. P9a cần hợp đồng service/instance/host + thời gian ownership; B16 §4 và §7 đã nêu nhu cầu nhưng runtime chưa kiểm. Không tự sửa câu G2, không gán chuỗi Node* cho service.
''')

save('kiem-dung-dan.md',f'''# Kiểm đúng đắn T-035

| Phép kiểm | Kết quả | Bằng chứng |
|---|---|---|
| K1 phân hoạch, khóa và loại bằng chứng | Đạt mọi ca/cửa sổ | thong-ke-do-thi.json#/cases/<i>/checks; stats và graph witness; raw/unique/duplicate tách riêng |
| K2 lặp/seed | Đạt | Mọi khoảng dựng hai lần trong day-du-001; fixture seed0/1/2 khớp; seed-001-h1 và seed-002-h2 khớp hai ca pilot thật, mọi khoảng ở các ca ấy |
| K3 RE2-TT | Đạt từng ca, tập và tổng | runs/kiem-cuoi-001/K3.json; 27/55×24, 20/20×5, 21/21×1; K2 hai cấu trúc cũ chưa rõ quy trình đếm |
| K4 service_calls | Đạt | Cùng frame/khoảng, cutoff sau mọi start; checks/independent từng ca/cửa sổ. Không so các frame có quy tắc cắt khác |
| K5 phép chiếu | Đạt | Tập nút/cạnh thực thể bằng phép chiếu ở {sum(len(c['checks']) for c in s['cases'])} khoảng; loại cạnh nội bộ/span-parent, giữ endpoint context/inventory riêng |
| K6 Nezha metadata | Đã kiểm đầy đủ hai chiều | runs/kiem-cuoi-001/K6.json; nguồn sinh/tính độc lập OPEN; không đọc Weight hoặc chuỗi số |
| K7 fixture | Đạt F1–F11 và nhánh lỗi | fixture/inputs.json, expected.json viết trước bộ dựng; fixture-001 tới fixture-004, 18 nhánh; expected-error đúng loại |
| K8 kiểm tay và nhãn | Đạt trong phạm vi mô tả | Bên dưới; do-phu-theo-nhan.json#/totals khớp 8/7; D5 949/1293 |

Hai lần giống nhau được kiểm trên mọi cửa sổ, không chỉ fingerprint. Seed khác được kiểm trên hai dataset thật ở hai ca pilot và mọi fixture. Kiểm toàn bộ ca dưới mọi seed không được khai là đã làm; mã dùng sort tường minh, không dựa thứ tự set để xuất. K4 dùng bản cài độc lập đã có, không gọi CIRCA/scoring hoặc RCA.

## Kiểm tay từ dòng span tới hai mức

**RE2-TT, ca pilot:** witness nguồn tại `runs/pilot-002/cases/RE2-TT/dev-b8bd0abf60.json#/manual_trace_witness`.

- Trace mẫu 0: span gốc POST refresh của order, span con OrderRepository.findByAccountId, rồi find/getMore ts.orders đều thuộc order. Hai cặp nội bộ giữ ở thao tác; không tạo order→database chỉ từ chữ trong tên. Mẫu có nhiều span và phần cha không hiện trong đoạn witness, nên không gọi nó là một request mạng đầy đủ. Graph giữ orphan của toàn phạm vi, không điền cha giả.
- Trace mẫu 1: POST login của auth→UserRepository.findByUsername→find ts-auth-mongo.user, lặp ở hai lần thực thi. Cả năm span cùng thực thể; mức thực thể auth không có cạnh gọi khác owner, mức thao tác giữ login→repository→query. Không bịa nút database từ tên query. Đây là phân biệt cấu trúc mà gộp thực thể không giữ; chưa là hiệu quả RCA.

**Nezha-OB, ca pilot:** nguồn `runs/pilot-002/cases/Nezha-OB/dev-607751ac0a.json#/manual_trace_witness`.

- Trace mẫu 0 có bảy span: frontend root, frontend GetProduct/AddItem; ProductCatalog GetProduct là con của frontend GetProduct, Cart AddItem là con của frontend AddItem; sql.conn.query/sql.rows thuộc ProductCatalog. Mức thực thể có frontend→productcatalogservice và frontend→cartservice. Mức thao tác giữ tên của cả hai phía cùng owner và các cặp nội bộ. Hai span cùng tên GetProduct không gộp vì owner khác. Thời gian hai cặp phù hợp quan hệ bao ở mẫu này; thiếu kind trong CSV nên không nâng thành gọi-đồng-bộ xác nhận.
- Trace mẫu 1 có 68 span, nhiều lời gọi frontend tới GetProduct và PlaceOrder. Cạnh thao tác gộp theo tên/owner, giữ event_count; các lần thực thi không thành nút mới. Cần cây span gốc nếu P6 dùng thứ tự hoặc chồng lấn; graph gộp không giữ đủ chúng.

Đã đối chiếu các cặp có cả hai dòng witness với tập cạnh thực thể/thao tác full của đúng ca. Mẫu không đủ phân xử mọi trường hợp ngoài đoạn witness; K1/K4/K5 kiểm toàn tập, còn nghĩa instrumentation vẫn OPEN. C2 không gọi quan hệ phụ thuộc là quan hệ nhân quả.

## D5 và so nhãn riêng

`do-phu-theo-nhan.json#/rows` của dev-746fd74313 ghi 1.293 trace A và 949 trace mất cha, cả start/end split ở miền F và cha trong A. Tái lập số G2-H19. Không loại ca này khỏi graph/số ca; mồ côi chỉ là trạng thái quan sát.

Root không được gọi = không có cặp cha–con khác owner đi vào root trên F. Quá thưa = có cặp đi vào nhưng không cặp nào đủ 20 trước và 20 sau theo end của span cha (code T-032 call_slow_table_v1.py MIN_CALLS). Tái lập 8 không đi vào, 7 thưa, 37 đủ; `runs/bo-sung-001` lưu count mọi cặp trước ghép root. Không gán thiếu cạnh cho dataset/instrumentation chỉ từ một cờ, không dùng nhóm này chọn thiết kế.

## Tự kiểm và giới hạn

362 hash đầu vào cũ đạt trước chạy, theo manifest phù hợp ở `runs/buoc0-001/input-verification.json`. Pilot-001 giữ phần dừng hiệu năng; mọi graph hợp lệ khớp từng byte pilot-002. Không sửa p3/CIRCA/task cũ/FlashTicket, không tải/EC2/test/heldout. Kiểm file set, source hash và complete diff sau cùng ở runs/kiem-cuoi-001; manifest cuối không lấy hash mới làm xác minh đầu ra cũ.

Đã trả lời khả năng dựng/giữ cấu trúc, chưa xác nhận cơ chế hoặc lợi ích RCA. Node host, nghĩa vật lý cạnh, nguồn sinh metadata mức ngày, nguyên nhân vắng cạnh, quy trình đếm hai graph cũ trong K2 và trace FlashTicket thật còn OPEN theo báo cáo. Không tự đóng RQ3/P5/G3 hoặc chọn P6.
''')

v0=(OUT/'dac-ta-do-thi-v0.md').read_text('utf-8')
save('dac-ta-do-thi.md',v0.replace('# Đặc tả đồ thị phụ thuộc v0 — T-035','# Đặc tả đồ thị phụ thuộc v1 — T-035',1)+'''

## 6. V1 và thay đổi so với bản trước chạy

Giữ mô hình, scope, cutoff, projection và giới hạn kết luận đã khai ở v0. Sentinel `root` được thêm vào code trước pilot theo nguồn Nezha/T-032; chú giải ở cuối v0 được nối trong pilot-001. Phần chính v0 và đáp án fixture được ghi trước bộ dựng. Không coi chú giải nối sau là bản được ghi trước toàn bộ pilot.

Tối ưu witness bằng mảng chỉ mục và depth bằng memoization; đây là thay cách tính, giữ cùng ngữ nghĩa. Graph hợp lệ pilot cũ khớp từng byte bản mới. Không đổi width, chuẩn hóa tên thao tác, đưa Node thành host hoặc bổ sung cạnh từ metadata mức ngày.

V1 nhận kết quả mô tả: dữ liệu dev dựng cạnh gọi chưa phân kiểu; tên SQL không tự cho ownership/endpoint; Node vẫn OPEN. Mức thao tác giữ thêm nội bộ và phân biệt cặp thao tác; không giữ cây/thời gian từng lần thực thi. Danh mục inventory ở graph thực thể là context chung cho hai mức, không được tính thành thao tác giả.

Các bảng số/câu trả lời C1–C9 và tiêu chí xong ở thong-ke-do-thi.md/JSON; kiểm ở kiem-dung-dan.md; C6 ở cot-node-nezha; C9 ở thong-tin-theo-quan-he. Chưa chọn P6 hoặc nghiệm thu P5. T-036 nhận đặc tả này để soạn SPEC nguồn tĩnh riêng; P9 nhận hợp đồng dữ liệu theo phạm vi Minh duyệt.
''')
print('Wrote v1 and complete reports')
