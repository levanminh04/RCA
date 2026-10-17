# Đặc tả đồ thị phụ thuộc v0 — T-035

Viết trước khi chạy bộ dựng. Đầu ra mô tả của P5; không là lựa chọn phương pháp P6. Căn cứ: DT18-NV2, bước 1 của cô, MRP P5, SPEC T-035, WHY-52; nhu cầu hệ thống theo B16 §1, §3–5, §7.

## 1. Mô hình và địa chỉ

Đồ thị có hướng, có kiểu, cho phép chu trình. Mỗi cạnh gộp theo (nguồn, đích, kiểu, nguồn bằng chứng, đích messaging nếu có). Đếm sự kiện làm chứng riêng với số cạnh. Giữ tối đa hai witness xác định bằng khóa trace/span để kiểm lại; không lưu bảng theo span. Các witness chỉ là con trỏ về dữ liệu dev, không là tên nút.

Thực thể có địa chỉ ổn định. Kiểu: service, gateway, database, cache, broker, identity-provider, external, host. Kiểu chỉ nhận từ metadata đã xác nhận hoặc thuộc tính có nghĩa đã kiểm; thiếu thì unknown. Không đoán database từ hậu tố tên. Universe là inventory riêng; nút quan sát và trạng thái độ phủ được giữ riêng. Thực thể ngoài alias được giữ nguyên tên, đánh dấu ngoài inventory, không gộp bằng regex.

Thao tác có khóa cặp (thực thể chủ quản, operationName gốc). Dùng JSON của cặp làm ID để tránh va chạm dấu phân cách. Giữ thao tác gốc, nội bộ và thao tác không gọi thực thể khác. Không tạo tên thao tác từ ID đơn/trace/span. Không chuẩn hóa tên theo kết quả khảo sát; tên thiếu giữ null và đánh dấu thiếu tên. Quan hệ thuộc-về là quan hệ địa chỉ, không là lời gọi.

Thành phần endpoint không có span vẫn là thực thể, giữ trong danh sách component_context của mức thao tác. Không tạo thao tác giả. Phép chiếu giữ component_context; chiếu mọi cạnh giữa hai thao tác khác chủ quản thành cạnh thực thể, giữ cạnh thao tác→thành phần hoặc thành phần→thao tác; bỏ cạnh nội bộ và thuộc-về khỏi tập cạnh phụ thuộc thực thể. So trên cùng tập quan sát; inventory không cộng vào tập nút quan sát.

Nguồn bằng chứng: trace (quan hệ span/thuộc tính), dataset-other (nguồn khác của dataset), static (kiến trúc), inferred (quan hệ suy ra có witness). Bộ dựng T-035 chỉ tạo trace/inferred; T-036 nhận static. Không tự coi cạnh phụ thuộc là cạnh nhân quả.

## 2. Định dạng span và chính sách lỗi

Các cột lõi: traceID, spanID, parentSpanID, serviceName, operationName, startTime, duration; hai cột cuối là số nguyên microsecond. Nezha ưu tiên _start_ns/_end_ns để giữ nanosecond. Bộ chuyển từ p3 thêm kind=null, attributes={}, links=[]; không bịa trường nguồn không có.

Các thuộc tính mở rộng của hợp đồng nội bộ (cần adapter xác minh nghĩa trước khi điền): entity.type; peer.entity/peer.type cho HTTP endpoint; db.entity/db.type cho database/cache; messaging.broker, messaging.destination, messaging.message_id, messaging.attempt; host.id và host.identity_verified. Link có traceID/spanID, semantics=message_creation và semantics_verified=true mới được nhận là nối tạo–xử lý bản tin. Đây là hợp đồng nội bộ để fixture kiểm, không tự là tên thuộc tính OTel hoặc yêu cầu đã ban hành cho FlashTicket.

Khóa span = (traceID,spanID), không chỉ spanID. ID rỗng/thiếu, thời gian âm/không nguyên, end<start: từ chối đầu vào, giữ run lỗi. Khóa trùng giống toàn nội dung lõi và mở rộng: bỏ bản lặp khỏi cấu trúc, đếm raw/unique/duplicate riêng. Khóa trùng khác nội dung: dừng, không chọn bản đầu tùy tiện. Parent sentinel rỗng, null, 0, -1, chuỗi toàn số 0 là span gốc. Mọi span unique hợp lệ thuộc đúng một nhóm: gốc, có cha tìm được trong khoảng, mồ côi. Parent nằm ngoài khoảng vẫn là mồ côi trong khoảng; không lấy tương lai/ngoài biên để nối.

Khoảng [lo,hi) nhận span start>=lo và end<hi; end=hi bị loại theo giao thức p3. Khoảng rỗng trả đồ thị rỗng, inventory giữ riêng. Toàn file RE2-TT = toàn bảng span của đúng ca dev. Toàn miền Nezha = toàn tập adapter trả trong [t−300,t+300), không đại diện cả file nguồn. N/A chia quanh mốc ở runner, không ở bộ dựng. N gọi đồ thị tham chiếu trước mốc, không khẳng định nền khỏe. Ảnh chụp RE2 neo min(start), bước 60/300 giây, có cả cửa sổ đuôi và rỗng; chỉ mức thực thể. Lưới có thể trùng mốc; P6 nhận giới hạn này. Không tạo ảnh chụp Nezha.

## 3. Quan hệ và sự kiện bằng chứng

Lời gọi quan sát chưa phân kiểu là cặp span cha–con resolve được, khác thực thể. Hướng là chủ quản cha→chủ quản con; chưa xác nhận là span phía gọi/phía được gọi thật. Một cặp không mặc nhiên là một request mạng. C2 đếm số span trong trace, sự bao thời gian và kiểm tay; thiếu instrumentation thì giữ giả định. Cặp cùng thực thể được giữ ở mức thao tác và đếm nội bộ riêng.

- gọi-đồng-bộ: cặp CLIENT→SERVER với nghĩa kind do adapter xác minh; hoặc CLIENT có peer.entity/peer.type tường minh khi không có SERVER quan sát. Không suy kind từ tên thao tác.
- gọi-chưa-phân-kiểu: cặp còn lại; không biến PRODUCER/CONSUMER thành gọi đồng bộ.
- dữ-liệu: thao tác phía service→database/cache từ db.entity/db.type tường minh. Không suy ownership từ tên.
- thông-điệp: PRODUCER→broker, broker→CONSUMER khi có địa chỉ broker; destination là scope riêng, không trộn hàng đợi. Cạnh logic producer→consumer chỉ khi link tạo bản tin có nghĩa xác minh trỏ đúng PRODUCER, cùng broker/destination; hoặc message_id khớp trong cùng broker/destination và chỉ có một nguồn tạo xác định. Thiếu/đa nghĩa thì không nối logic, đếm unresolved. CorrelationId giao dịch không được dùng. Retry/lần giao lại/lần xử lý là các sự kiện witness riêng, không là các nút thao tác mới.
- triển-khai: thực thể→host khi host.id có host.identity_verified=true. Cùng tên Node ổn định chưa đủ. Chỉ fixture dùng xác nhận giả đã khai; Node Nezha mặc định OPEN.

Callback trace mới được giữ như thao tác gốc tại service; CLIENT span phía gọi external tạo service→external. Không bịa external→callback từ correlation/timestamp. Nếu nguồn thật cung cấp bằng chứng gọi vào thì adapter mới thêm span/quan hệ phù hợp. Scheduler là thao tác gốc không có cạnh gọi vào. Outbox gồm thao tác ghi dữ liệu và thao tác publisher; không ghép hai trace bằng correlation. Saga/bù trừ là tên thao tác ổn định và quan hệ quan sát thực; chiều bù trừ không tự đảo cạnh hoặc xác lập nhân quả nghiệp vụ.

## 4. Log, trace, metric và đường dùng cạnh

Trace/spans địa chỉ bằng khóa trace/span→(entity,operation); cây span và thời gian từng lần thực thi phải đọc từ đầu vào gốc khi P6 cần. Đồ thị thao tác không thay cây này.

Log nối theo trace/span hợp lệ; thiếu khóa thì entity+timestamp, chỉ lên mức thực thể; operation tường minh và ổn định mới gắn thao tác. Metric entity/instance/host gắn đúng scope. Metric của cả service là bối cảnh dùng chung, không sao thành bằng chứng độc lập của mọi thao tác. Broker queue metric địa chỉ (broker,destination); đối tác ngoài chỉ có telemetry phía client. Node chưa xác định host thì không gắn chuỗi metric host vào service.

| Ứng viên G2 | Phần tử có thể dùng | Phần còn cần đầu vào gốc; trạng thái |
|---|---|---|
| UV-1 | Cạnh có hướng, thao tác hai đầu | Kind và khoảng thời gian từng lời gọi; chưa chọn |
| UV-2 | Quan hệ cha–con của span | Cây span, khoảng thời gian, chồng lấn/song song; đồ thị gộp không đủ |
| UV-3 | Thao tác và cây từng request | Root span, membership, duration từng span; đồ thị thao tác không đủ |
| UV-4 | Tập thực thể cùng trace | Membership từng trace; không dùng cạnh |
| UV-5 | Cạnh đi vào/đi ra | Thời lượng có nghĩa phía gọi; chưa chọn |
| UV-6 | Nút thực thể/thao tác | Log và success rate; chưa có phép dùng cạnh |
| UV-7 | Quan hệ lan điểm | Quy tắc gộp/giá trị hợp lệ còn chọn ở P6 |
| UV-8 | Thực thể, cạnh kiến trúc→đồ thị metric | T-036 và cấu hình metric; không dựng đồ thị metric tại đây |
| UV-9 | Cửa sổ, provenance | Chuỗi thời gian, kiểm không nhìn tương lai; không dùng cạnh trực tiếp |

## 5. Kiểm và giới hạn khai trước

F1–F11 và đáp án tại fixture/expected.json được ghi trước mã bộ dựng. K1 phân hoạch và event count; K2 hai lượt/seed 0,1,2; K3 đối chiếu từng ca/T-002 và tổng; K4 service_calls trên cùng tập span, cutoff nằm sau mọi start; K5 chiếu hai mức; K6 cặp nguồn phụ Nezha (chỉ header/Source–Target); K7 fixture; K8 kiểm tay và ghép nhãn riêng sau ghi đồ thị. Bộ dựng chỉ nhận spans, interval, aliases, universe. Không nhận tên ca/đường dẫn/mốc/root/fault; cột nhãn bị từ chối.

Tên có chuỗi giống UUID, hex dài hoặc đoạn URL số được báo dạng ứng viên ID, không tự là tên sai. Chữ ký con là tập cặp entity/operation con trực tiếp của một span; báo số chữ ký cho mỗi operation. Độ sâu nội bộ là độ sâu chuỗi cha cùng thực thể, chu trình khóa span nếu có được đếm riêng, không lặp vô hạn. Thay đổi cấu trúc chỉ so tập nút/cạnh, không gồm count/witness/time.

Mọi số trong báo cáo lấy từ JSON kèm con trỏ. C1–C9 là mô tả/khả năng biểu diễn. Lợi ích chẩn đoán, nhân quả, nền khỏe, độ khớp kiến trúc và trace FlashTicket thật còn OPEN theo nơi nhận ở SPEC.

Làm rõ trước pilot: sentinel chuỗi `root` được nhận theo mã nguồn trace_coverage của T-032 và schema Nezha; không tính là span mất cha.
