# Mẫu thẻ dataset

Mẫu chung cho mọi ứng viên của MRP §4/P2. Giữ cùng thứ tự các mục khi so ở G1. Chi phí ghi riêng; dữ liệu đã có hay code baseline đã có không chứng minh khả năng phân xử. Thẻ này mô tả bằng chứng, không chọn dataset, không đặt thêm cổng.

Ô chưa có bằng chứng ghi **OPEN — chưa kiểm**, lý do, đầu vào và người cần giải quyết. Một ca mẫu chỉ cho biết ca mẫu đó; không suy rộng thành toàn bộ dataset.

## 1. Danh tính, nguồn và phạm vi đã kiểm

| Mục | Nội dung cần điền |
|---|---|
| Tên dataset, hệ thống, biến thể | `<tên; hệ; phiên bản>` |
| Tác giả, năm, công cụ tiêm lỗi, stack thu thập | `<nguồn từng thông tin>` |
| Nguồn chính | `<bài báo; README; kho dữ liệu công khai>` |
| Revision và ngày truy cập | `<đường dẫn manifest ghi revision; ngày>` |
| Giấy phép dữ liệu và code | `<tên; link/file; phạm vi cho phép dùng; phân biệt hai giấy phép>` |
| Tổng số ca và nguồn đếm | `<metadata công khai hay đếm file; cách nhận diện một ca>` |
| Ca đã có, ca được phép đọc, ca thực sự kiểm | `<ba số riêng; danh sách mẫu trong manifest>` |
| Phần chỉ kiểm metadata/schema/nhãn | `<phần nào; phần nào chưa đọc telemetry (dữ liệu đo)>` |
| Kết quả gốc và cách chạy lại | `<script; lệnh; file kết quả; thời gian chạy>` |

Trạng thái của các phát biểu:

- **FACT:** quan sát có nguồn; ghi rõ trên mẫu hay toàn bộ, metadata hay dữ liệu đo.
- **USER_CONFIRMED:** Minh xác nhận; trích ý và mã/đường dẫn quyết định trong repo.
- **CANDIDATE:** giả thuyết hoặc đề xuất chưa kiểm; ghi giả định và trường hợp sai.
- **DECIDED:** Minh đã duyệt lựa chọn cụ thể; dẫn nguồn quyết định. Không dùng cho suy luận của agent.
- **OPEN:** chưa biết; ghi vì sao và đầu vào/người cần để giải quyết.

Mỗi nhận định từ kết quả có nguyên nhân khả thi khác ngay cạnh nó, theo Q-33. Kết quả đếm là FACT trong phạm vi đếm; ý nghĩa khoa học của số đếm có thể vẫn là CANDIDATE hoặc OPEN.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí MRP §4 | Kết quả và trạng thái | Phạm vi, nguồn bằng chứng | Nguyên nhân khả thi khác / giới hạn diễn giải |
|---|---|---|---|
| 1. Công khai, tải được, giấy phép cho phép dùng | `OPEN — chưa kiểm` | `<link; revision; kiểm tải mẫu; giấy phép dữ liệu>` | `<công khai không đồng nghĩa có giấy phép; tình trạng truy cập ở ngày kiểm>` |
| 2. Nhãn thành phần gốc và thời điểm lỗi | `OPEN — chưa kiểm` | `<trường nhãn; độ phủ; injection hay onset>` | `<tiêm lỗi không chứng minh triệu chứng bắt đầu ngay>` |
| 3. Trace có liên kết span cha–con | `OPEN — chưa kiểm` | `<schema; độ phủ và mẫu số ở mục 4>` | `<thiếu cha có thể do lấy mẫu, cắt cửa sổ hoặc mất span>` |
| 4. Metric; log nếu có | `OPEN — chưa kiểm` | `<schema; số ca có; chất lượng từng nguồn>` | `<file có mặt không đồng nghĩa nội dung dùng được>` |
| 5. Nhiều service gốc ở nhiều vị trí đồ thị | `OPEN — chưa kiểm` | `<đếm nhãn; bậc raw từng node; phạm vi đồ thị>` | `<vị trí có thể trùng với danh tính service và loại lỗi>` |
| 6. Lỗi tài nguyên, mạng, mã nguồn | `OPEN — chưa kiểm` | `<tên nhãn gốc; nhóm theo tài liệu nguồn; bảng theo ô>` | `<nhãn loại lỗi không chứng minh biểu hiện ở mọi nguồn tín hiệu>` |
| 7. Triệu chứng ở service ngoài service gốc | `OPEN — chưa kiểm` | `<ước lượng nhiều ngưỡng từ đoạn bình thường ở mục 6>` | `<tải chung, nhiễu hoặc lỗi đo cũng tạo bất thường cùng lúc>` |
| 8. Dữ liệu bình thường đủ để học ngưỡng | `OPEN — chưa kiểm` | `<độ dài; số điểm; nguồn và nguy cơ nhiễm lỗi>` | `<đoạn trước tiêm chưa chắc sạch hoặc đại diện tải vận hành>` |
| 9. Ít nhất một bộ độc lập trong bộ dataset chọn | `OPEN — chưa kiểm` | `<tác giả; công cụ lỗi; stack; quan hệ với các ứng viên>` | `<khác tên hệ không chứng minh độc lập; chỉ kết luận khi đủ thẻ>` |

Không tổng hợp thành điểm tự đặt. Nếu không có trace, ghi rõ khả năng nghiên cứu kịch bản đồ thị từ kiến trúc là **CANDIDATE — chưa kiểm**; không coi đó là tương đương trace.

## 3. Nhãn, số ca và khả năng phân xử

| Thành phần gốc | Nhãn loại lỗi gốc | Nhóm tài nguyên/mạng/mã nguồn theo nguồn | Số ca, số lần lặp | Nguồn và phạm vi đếm |
|---|---|---|---|---|
| `<điền>` | `<giữ nhãn gốc>` | `<nhóm hoặc OPEN; không đoán từ tên>` | `<số>` | `<metadata công khai; file kết quả>` |

Tổng hợp số thành phần gốc khác nhau, số loại lỗi, số ô (thành phần gốc × loại lỗi), số lần lặp của mỗi ô, ô thiếu và nhãn không phân tích được. Tách đếm toàn kho công khai khỏi phần dữ liệu đo đã kiểm. Nếu nguồn công bố và đếm thực tế lệch nhau, giữ cả hai và nêu nguyên nhân còn khả thi.

| Thành phần gốc | Có mặt trong đồ thị mẫu? | Bậc vào, bậc ra raw | Đồ thị/ca nào cho số này | Giới hạn và giải thích khác |
|---|---|---|---|---|
| `<node>` | `<có/không/chưa kiểm>` | `<hai số; quy ước hướng cạnh>` | `<file cạnh; file kết quả>` | `<node thiếu có thể do instrumentation/lấy mẫu; không mặc định cô lập>` |

Ghi cách dựng cạnh (span nào tạo cạnh, hướng cạnh, phạm vi thời gian), số node/cạnh, số đồ thị khác nhau trên phần đã kiểm nếu có. Báo bậc raw để mô tả vị trí; không tự chọn ngưỡng hay định nghĩa hub (nút trung tâm). Nếu dùng từ lá/giữa/hub từ nguồn, dẫn định nghĩa của nguồn và ghi rõ đó chưa phải lựa chọn phương pháp của nhóm. Không suy topology toàn bộ từ một ca.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

| Nguồn | Có trong bao nhiêu ca đã kiểm? | Định dạng, trường, đơn vị, thời gian | Chất lượng đã đo | Phạm vi / giải thích khác |
|---|---|---|---|---|
| Trace (dấu vết lời gọi) | `<tử số/mẫu số>` | `<trace ID; span ID; parent ID; service; start; duration; status; operation>` | `<rỗng, trùng ID, liên kết cha; bảng bên dưới>` | `<schema mẫu không bảo đảm biến thể khác giống nhau>` |
| Metric (số đo) | `<tử số/mẫu số>` | `<tên cột; service; đơn vị; nhịp lấy mẫu; timestamp>` | `<NaN; hằng số; khoảng trống; độ dài; mapping service>` | `<số đo hằng có thể bình thường hoặc không được thu>` |
| Log (nhật ký) | `<tử số/mẫu số>` | `<timestamp; service; level; message; cấu trúc payload>` | `<rỗng; trace_id cột riêng; trace ID trong nội dung>` | `<không có cột trace_id chưa chứng minh payload không chứa ID>` |

Liên kết span cha–con:

| Phép đếm | Kết quả | Cách tính và nguồn |
|---|---|---|
| Tổng span | `<số>` | `<file kết quả>` |
| Span không có parent ID, root theo quy ước nguồn | `<số>` | `<null/rỗng/sentinel cụ thể>` |
| Span có parent ID cần resolve (tìm được cha) | `<mẫu số>` | `<không gộp root vào mẫu số>` |
| Span tìm được cha duy nhất | `<tử số>` | `<khóa ghép, ví dụ trace ID + span ID; không chỉ span ID>` |
| Span không tìm được cha / cha không duy nhất | `<hai số>` | `<phân biệt mất cha và ID trùng>` |
| Tỷ lệ resolve | `<tử số/mẫu số; %>` | `<giữ cả hai số; mẫu số bằng 0 thì không xác định>` |

Ghi phép ghép kiểm trong một file, một ca hay liên file. Với tỷ lệ tổng, ghi cộng số đếm hay trung bình theo ca. Liên kết tồn tại không chứng minh quan hệ nhân quả. Ghi giới hạn status/error, loại span, database/message queue nếu schema không cho biết.

Log: tách **có cột trace_id**, **cột có giá trị**, **chuỗi giống trace ID trong payload**, và **ID ghép được với trace**. Nếu chỉ kiểm schema hoặc tìm mẫu chuỗi, phần ghép ID còn OPEN. Có log không đồng nghĩa ánh xạ được log lên node/cạnh.

## 5. Dữ liệu bình thường và mốc thời gian

| Mục | Kết quả, nguồn | Giới hạn / nguyên nhân khả thi khác |
|---|---|---|
| Mốc lỗi có sẵn | `<injection (tiêm lỗi), onset (bắt đầu biểu hiện), hay loại chưa rõ; đơn vị/timezone>` | `<độ trễ tiêm → triệu chứng; clock lệch>` |
| Thời gian trước/sau mốc theo ca và nguồn tín hiệu | `<min/max; file theo ca>` | `<cửa sổ file có thể khác cửa sổ lỗi thật>` |
| Đoạn dùng tạm làm dữ liệu bình thường | `<quy tắc; độ dài; số điểm theo ca/kênh>` | `<khởi động, lỗi trước đó, tải biến đổi có thể gây contamination (nhiễm lỗi)>` |
| Dữ liệu bình thường riêng có nhãn | `<có/không/OPEN; nguồn>` | `<không tự gọi mọi đoạn trước tiêm là nhãn bình thường>` |
| Khả năng học ngưỡng | `<FACT về độ dài; CANDIDATE về đủ; OPEN nếu chưa kiểm>` | `<phụ thuộc phương pháp, nhịp lấy mẫu và mức ổn định>` |

Nếu chỉ có injection timestamp, nhãn thời gian chỉ hỗ trợ đánh giá theo khoảng tiêm trong điều kiện ghi rõ. Không gọi đó là ground truth (nhãn chuẩn) của bất thường quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

Với dữ liệu được phép đọc: mô tả kênh metric, mapping service, đoạn bình thường, công thức/ngưỡng thử, xử lý hằng số và dữ liệu thiếu. Đây là khảo sát dataset, chưa phải chọn ngưỡng RCA. Không tạo nhãn lan chính thức cho từng ca.

| Ngưỡng thử từ dữ liệu bình thường | Số ca hợp lệ / số ca đã xét | Bằng chứng bất thường ngoài service gốc | Kết quả theo ô | Giải thích khác / giới hạn |
|---|---|---|---|---|
| `<ngưỡng 1>` | `<hai số>` | `<số đếm/tỷ lệ; chỉ định nghĩa tạm và file kết quả>` | `<đường dẫn bảng>` | `<tải chung; kênh nhiễu; ít mẫu; bias do metric được thu>` |
| `<ngưỡng 2>` | `<hai số>` | `<như trên>` | `<đường dẫn bảng>` | `<như trên>` |
| `<ngưỡng 3>` | `<hai số>` | `<như trên>` | `<đường dẫn bảng>` | `<như trên>` |

Nêu độ nhạy theo ngưỡng, ca/kênh không tính được và lý do. Bất thường đồng thời chưa chứng minh lan truyền nhân quả. Không thấy bằng chứng ở metric chưa chứng minh không lan ở log/trace. Với dataset giữ ngoài trước G3: **OPEN — chưa kiểm**, vì chỉ được đọc metadata/schema/đếm nhãn; không làm phép ước lượng này.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task đánh giá | Nhãn cần | Nhãn thực có và độ phủ | Chấm được đến đâu? | Giới hạn / giải thích khác |
|---|---|---|---|---|
| Xếp hạng nguyên nhân gốc | `<thành phần gốc theo ca; đơn hay đa nguyên nhân>` | `<nguồn>` | `<MRR/Hit@k; NDCG tùy nhãn; OPEN khi thiếu>` | `<nhãn service không chấm chi tiết operation/span>` |
| Phát hiện bất thường theo thời gian | `<nhãn bất thường quan sát được theo đơn vị đánh giá>` | `<onset/interval thật, chỉ injection, hoặc không có>` | `<phân biệt đánh giá theo khoảng tiêm với theo bất thường thật>` | `<injection không chứng minh onset; thiếu nhãn kết thúc>` |
| Vùng ảnh hưởng | `<tập thành phần thật bị ảnh hưởng theo ca>` | `<nguồn hoặc không có>` | `<chấm được/không chấm được/OPEN>` | `<service gốc không thay thế nhãn vùng; ước lượng mục 6 không phải nhãn>` |
| Bất thường theo trace, nếu dataset có | `<nhãn từng trace>` | `<nguồn hoặc không có>` | `<đơn vị trace; không mặc định chuyển sang cửa sổ/service>` | `<nhãn trace không tự suy ra nguyên nhân gốc>` |

Ghi khả năng so phương pháp có giám sát và không giám sát theo ngân sách nhãn. Số đủ để huấn luyện, chuyển sang hệ khác và baseline nào chạy được là OPEN nếu chưa kiểm; không suy từ số ca tổng.

## 8. Rò nhãn và thông tin phục vụ G1

- Nhãn ở đâu: tên ca/thư mục, đường dẫn, file nhãn, mốc tiêm và biên cửa sổ telemetry. Phần nào phục vụ đếm/chấm, phần nào là telemetry; có thể suy mốc tiêm từ vị trí trong file sau khi bỏ tên ca/file nhãn không?
- Nếu thấy biên đối xứng quanh injection: ghi số ca/nguồn đã kiểm, độ lệch timestamp đầu/cuối và phần chưa đọc. Biên hàng quan sát chưa chứng minh cơ chế exporter; injection chưa là onset triệu chứng. Nêu nguy cơ cho giao thức tự phát hiện, phân biệt với trường hợp detector đã khai thác rò được kiểm chứng. Không mặc định mọi dataset rò hoặc tự chốt cách cắt/chấm mới.
- Nếu có runner công khai dùng nhãn để chọn SLI (chỉ báo chất lượng dịch vụ) hoặc đầu vào khác: ghi file/dòng và phạm vi đã kiểm. Adapter chưa có thì ghi OPEN; không khẳng định đã loại rò nhãn.
- Cách chia theo ô và dataset giữ ngoài: dẫn phương án đã có, trạng thái CANDIDATE/DECIDED và nguồn WHY-04/quyết định. Thẻ không tự chốt cách chia.
- Ghi rõ nhãn để học, nhãn dev để chọn cấu hình/checkpoint và nhãn chỉ để chấm khi có phương án. Nhãn test chỉ để chấm theo MRP; không đưa tên ca, đường dẫn hay đầu vào suy từ nhãn vào phương pháp.
- Bộ độc lập: ghi tác giả/công cụ tiêm/stack để so với mọi thẻ ở G1. Độc lập toàn bộ còn OPEN khi chưa đủ nguồn.

## 9. Kích thước và chi phí — tách khỏi khả năng phân xử

| Mục | Đã đo hay ước lượng? | Giá trị, đơn vị, nguồn | Điều chưa kiểm |
|---|---|---|---|
| Dung lượng tải nén / kích thước file công khai | `<FACT/ước lượng>` | `<byte/GB; metadata revision>` | `<metadata thiếu>` |
| Dung lượng giải nén / đang có trên máy | `<phân biệt>` | `<nguồn>` | `<không suy bằng dung lượng nén>` |
| RAM và thời gian đọc mẫu | `<FACT hoặc OPEN>` | `<môi trường; ca mẫu; file kết quả>` | `<không suy chi phí toàn bộ từ một mẫu>` |
| Chi phí tải và viết adapter | `<CANDIDATE — chưa kiểm nếu dự kiến>` | `<ước lượng riêng; giả định>` | `<định dạng khác; thiếu mapping>` |

## 10. Những điều còn mở

| Vấn đề | Vì sao chưa kiểm? | Đầu vào cần | Người/bước dự kiến giải quyết | Kết luận phụ thuộc |
|---|---|---|---|---|
| `<OPEN>` | `<lý do cụ thể>` | `<file/schema/nguồn/Minh quyết>` | `<G1/G3/task sau theo kế hoạch sẵn có>` | `<RQ hoặc tiêu chí bị giới hạn>` |

Kết thúc bằng phạm vi bằng chứng đã có, điều chưa phân xử được và các nguyên nhân khả thi khác. Không kết luận dataset thắng/thua ứng viên khác khi chưa đủ bảng chung, không chọn dataset thay Minh.
