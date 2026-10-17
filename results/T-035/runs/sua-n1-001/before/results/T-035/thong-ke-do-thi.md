# Đồ thị phụ thuộc từ trace dev — T-035

T-035 đã tạo mô hình chung, bộ dựng và khảo sát hai mức trên toàn bộ dev được duyệt. Đây là kết quả mô tả của P5. Chưa xác nhận đồ thị hoặc mức thao tác giúp chẩn đoán; chưa chọn thiết kế P6, chưa hoàn tất P5/G3.

## 1. Miền dữ liệu và định nghĩa

RE2-TT: toàn bảng span của đúng ca dev. Nezha-OB: toàn tập adapter trả trong cửa sổ dev [t−300,t+300), không là cả file nguồn. N/A chỉ nhận span được bao trọn trong khoảng, cha cũng phải ở trong khoảng; span bắc qua biên không được lấy cha ở ngoài để nối. N là đồ thị tham chiếu trước mốc, chưa có bằng chứng nền khỏe. Đây là mô tả chế độ biết trước cửa sổ; không dùng các đồ thị N/A này làm đầu vào tự phát hiện.

Ảnh chụp RE2 neo **min start của bảng span**, giữ phần lẻ microsecond; lưới 60/300 giây cố định theo neo ấy, end < biên phải. Không đồng nhất neo này với neo theo timestamp metric/giây nguyên của khảo sát cũ. Cảnh báo trong SPEC về biên trùng mốc ở lưới cũ vẫn là việc P6 phải xét; lưới của T-035 không được tạo bằng mốc tiêm. Mức thao tác chỉ lưu full/N/A. Nezha không có ảnh chụp. Nguồn: `thong-ke-do-thi.json#/window_definition`, các graph `interval_ns`.

Đồ thị khác nhau khi tập nút/cạnh khác, bỏ count, witness và timestamp khỏi fingerprint. Độ phủ inventory khác số nút có span. Mọi cạnh dev hiện là gọi-chưa-phân-kiểu: hướng từ owner span cha sang owner span con; chưa xác nhận quan hệ mạng đồng bộ.

## 2. C3–C4: cấu trúc và độ phủ

| Miền | RE2-TT | Nezha-OB |
|---|---:|---:|
| Số ca | 30 | 22 |
| Span trong full được phép | 22,834,238 | 1,421,887 |
| Cấu trúc thực thể full | 3 | 1 |
| Cấu trúc thao tác full | 6 | 1 |
| Ca N/A đổi cấu trúc thực thể | 0 | 2 |
| Ca N/A đổi cấu trúc thao tác | 4 | 3 |

Nguồn từng ô: `thong-ke-do-thi.json#/datasets/RE2-TT` và `#/datasets/Nezha-OB`, trường cùng tên. Từng ca/cửa sổ: `#/cases/<i>/windows/<tên>`. Theo ô: `do-phu-theo-nhan.json#/cells`; chỉ ghép nhãn sau khi graph và thống kê không nhãn đã ghi. Một ô không là mẫu hình của toàn dataset.

Ảnh chụp 60 giây: 739 khoảng, 84 cấu trúc khác nhau, 17 khoảng rỗng. 300 giây: 150 khoảng, 4 cấu trúc, 0 khoảng rỗng. Nguồn: `#/datasets/RE2-TT/snapshot_shapes`. Vì vậy gần hằng ở full/N/A không đồng nghĩa hằng ở cửa sổ ngắn. Khác biệt có thể do số lời gọi và quy tắc cắt, chưa là thay kiến trúc hoặc do lỗi.

Mọi thực thể U có trạng thái has_edge, span_without_edge hoặc not_observed ở `#/cases/<i>/windows/<tên>/coverage`. Tập ngoài U ghi riêng tại outside_inventory. Đây là độ phủ quan sát của bộ dựng; không có mẫu số số request/span thật đã sinh. Không có cạnh không chứng minh không phụ thuộc; có thể không được gọi, thiếu instrumentation, mất span hoặc cửa sổ ngắn.

K3 tái lập đúng toàn bộ ca RE2-TT và tổng 22,834,238 span; 22,437,039/22,639,789 tham chiếu cha resolve. Phân bố nút/cạnh: {'20/20': 5, '21/21': 1, '27/55': 24}. Nguồn: `runs/kiem-cuoi-001/K3.json#/rows`, `#/totals`, `#/node_edge_distribution`. Các tập nút/cạnh cũng so chính xác với T-002, không chỉ số đếm. Có ba cấu trúc như T-002. Câu hai cấu trúc trong K2 chưa có quy trình/đầu ra gốc ở nguồn được phép để xác định vì sao khác; không sửa K2 hoặc dùng câu ấy thay kết quả hiện tại. Phần chưa biết này không làm mất phép tái lập T-002.

## 3. C1–C2: cạnh nào có bằng chứng

| Loại | RE2-TT | Nezha-OB | Căn cứ |
|---|---|---|---|
| Gọi chưa phân kiểu | Dựng được | Dựng được | trace/span/parent + owner, K1/K4 |
| Gọi đồng bộ xác nhận | Chưa phân xử | Chưa phân xử | Không có kind/định nghĩa đầy đủ của span phía gọi–phía nhận trong export |
| Dữ liệu đến DB/cache | Không dựng được từ export hiện có | Không dựng được từ export hiện có | Tên query không cho endpoint/ownership đã xác minh |
| Thông điệp qua broker/nối bản tin | Không dựng được | Không dựng được | Không có broker/destination/link/message identity đủ nghĩa |
| Triển khai lên máy | Không dựng được | Chưa phân xử Node; chưa dựng cạnh đã xác nhận | Thiếu mapping host có nguồn xác nhận |

Ba trạng thái nói về khả năng dựng từ bằng chứng hiện có, không là khẳng định các quan hệ không tồn tại. Tên thao tác chứa query/database/RPC là gợi ý mô tả, không được biến thành kiểu cạnh hoặc ownership bằng regex. Nguồn từ vựng: `tu-vung-thao-tac.json#/cases`; schema/provenance từng ca: `thong-ke-do-thi.json#/cases/<i>/provenance`. Kiểu quan hệ đã kiểm trên fixture, không là kết quả quan sát thật của hai dataset.

Một lời gọi cấu trúc là cặp span cha–con khác owner resolve được; mỗi sự kiện có hai span làm chứng, khác với số request mạng thật. RE2 có 3,405,669/3,957,045 cặp được bao thời gian; Nezha 334,129/338,829. Nguồn: `#/datasets/<dataset>/cross_parent_contains`, cross_parent_events. Không bao thời gian có thể do clock, bất đồng bộ hoặc semantics instrumentation; phép đếm không phân xử các giải thích này. Histogram số span mỗi trace ở `runs/bo-sung-001/summary.json#/cases/<i>/span_count_per_trace`; không gọi số ấy là số span mỗi request mạng.

Kiểm tay hai trace mỗi dataset tại `kiem-dung-dan.md` hỗ trợ cách giữ quan hệ; không xác nhận kiểu vật lý trên mọi ca. UV-1/UV-2 còn cần semantics phía gọi, thời gian và cây span gốc. Đồ thị thao tác không thay cây/thời gian từng lần thực thi.

## 4. C7–C8: mức thao tác

| Thuộc tính full | RE2-TT | Nezha-OB |
|---|---:|---:|
| Khóa entity+operation khác nhau trên dev | 154 | 55 |
| Khóa có ở mọi ca | 74 | 55 |
| Khóa chỉ có ở một ca | 2 | 0 |
| Tên giống ID theo luật đã khai | 0 | 0 |
| Khóa chỉ tên HTTP method | 23 | 0 |
| Tên dùng ở nhiều thực thể | 11 | 9 |
| Số chữ ký con lớn nhất cho một thao tác/ca | 12 | 9 |
| Độ sâu nội bộ lớn nhất | 2 | 3 |

Nguồn: `tu-vung-thao-tac.json#/datasets/<dataset>`; presence và từng cửa sổ ở `#/cases`. Luật giống ID chỉ là phép mô tả, không chứng minh tên ổn định về nghĩa; không tự chuẩn hóa. Tên HTTP chung có thể gộp nhiều đích. Nhiều chữ ký con có thể do nhánh/tải đầu vào hợp lệ, không tự là lỗi đặt tên.

**Dựng được tới đâu:** có cấu trúc thao tác trên mọi ca/full/N/A và phép chiếu nhất quán. Phần mất cha vẫn bị thiếu quan hệ, không được bù hoặc loại ca khó. Tên Nezha có mặt nhất quán giữa các ca dev; ở RE2 có nhóm chỉ xuất hiện một ca và nhóm HTTP chung, cần kiểm nghĩa với instrumentation/phiên bản nguồn trước khi P6 coi tên là địa chỉ thao tác riêng. Không kết luận mọi thao tác đều được quan sát đầy đủ.

**Có phân biệt hơn mức thực thể không:** có. Cặp cha–con nội bộ được giữ: 18,479,994 sự kiện RE2, 1,044,674 sự kiện Nezha. Nguồn: `thong-ke-do-thi.json#/datasets/<dataset>/same_entity_events`. RE2 có sáu cấu trúc thao tác so với ba thực thể; chiếu đúng tập thực thể/cạnh ở mọi khoảng đã kiểm. Cạnh thực thể có nhiều cặp thao tác được báo theo ca tại `#/datasets/<dataset>/operation_pairs_per_entity_edge`. Không suy lợi ích chẩn đoán từ các số này.

**Còn thiếu:** nghĩa ổn định của tên, kind và endpoint, cây/thời gian mỗi span, xử lý span thiếu, log nối đúng scope và metric thao tác thực. P6 cần so hai mức trên cùng bằng chứng, cửa sổ, tập ứng viên và ngân sách chọn; giữ metric toàn service là bối cảnh chung. Chưa chọn mức nào.

## 5. C4/K8, C6 và C9

K8 tái lập 8 ca không có cạnh gọi đi vào root và 7 ca có cạnh quá thưa; 37 ca có ít nhất một cặp đi vào đủ 20 lời gọi mỗi phía. Nguồn: `do-phu-theo-nhan.json#/totals`, `#/rows`, định nghĩa từ T-032 call_slow_table_v1.py MIN_CALLS. Đếm trên F, chia theo end của span cha; khác với N/A containment của ảnh đồ thị, không ép hai quy tắc cho cùng số đếm. Nhóm D5 tái lập 949/1.293 trace A mất cha; chi tiết scope ở `#/rows` của dev-746fd74313.

Node: có 8 giá trị, từng pod có một giá trị ổn định trên các cửa sổ đã đọc; service có thể có nhiều pod/Node ở hai ngày. Giá trị dạng IP và tính ổn định chưa xác nhận host. Nguồn và phần thiếu ở `cot-node-nezha.md`, JSON; không dựng cạnh triển khai đã xác nhận.

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

Chi phí lượt đầy đủ: 18.14 phút, RAM đỉnh 2.25 GiB. Nguồn `thong-ke-do-thi.json#/cost`; thời gian từng ca/bước/cửa sổ và lượt dừng hiệu năng ở runs/. Giữ mọi lượt; không tải, không dùng EC2, không mở test/heldout. Mọi hash nằm trong manifest. Prompt Claude trong LOG Phiên 6 và prompt-claude-soat-ket-qua.txt; Minh chuyển thủ công.

## Nhóm thao tác chỉ một phía và cấu trúc theo ô

Nezha-OB: 0 ca có thao tác chỉ ở A; 2 ca có thao tác chỉ ở N. Danh sách riêng từng ca/tên tại `tu-vung-thao-tac.json#/datasets/Nezha-OB/A_only_by_case` và `N_only_by_case`; theo cửa sổ tại `#/cases`. Không bỏ nhóm chỉ sau mốc, không tạo nền giả.

RE2-TT: 4 ca có thao tác chỉ ở A; 0 ca có thao tác chỉ ở N. Danh sách riêng từng ca/tên tại `tu-vung-thao-tac.json#/datasets/RE2-TT/A_only_by_case` và `N_only_by_case`; theo cửa sổ tại `#/cases`. Không bỏ nhóm chỉ sau mốc, không tạo nền giả.

C3 theo ô gồm full, đổi N/A và ảnh chụp tại `do-phu-theo-nhan.json#/cells`. Các nhóm này chỉ là báo cáo sau ghép nhãn, không là đầu vào bộ dựng hoặc căn cứ đã chọn mức P6. Bản trước bổ sung được giữ ở runs/report-001-before-final-groups.
