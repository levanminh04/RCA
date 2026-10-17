# Đặc tả đồ thị phụ thuộc v2.1 — T-035

V0 được viết trước bộ dựng đầu tiên. V2.1 bổ sung chính sách lỗi đầu vào theo Q-155; bản v2 giữ tại runs/sua-hop-dong-001/before/results/T-035/dac-ta-do-thi.md. V2 sửa hợp đồng messaging theo Q-154; thiết kế và đáp án bổ sung được ghi trước mã sửa. Bản v1 được giữ tại runs/sua-n1-001/before/results/T-035/dac-ta-do-thi.md. Đầu ra mô tả của P5; không là lựa chọn phương pháp P6. Căn cứ: DT18-NV2, bước 1 của cô, MRP P5, SPEC T-035, WHY-52; nhu cầu hệ thống theo B13 §5 và B16 §1, §3–5, §7.

## 1. Mô hình và địa chỉ

Đồ thị có hướng, có kiểu, cho phép chu trình. Cạnh gộp theo (nguồn, đích, kiểu, nguồn bằng chứng, destination legacy nếu có); cạnh messaging còn giữ khóa địa chỉ gồm broker, broker_scope, exchange, routing_key, queue. Message ID, identity scope và attempt không là khóa cạnh/nút hay địa chỉ metric. Đếm sự kiện làm chứng riêng với số cạnh. Giữ tối đa hai witness xác định bằng khóa trace/span để kiểm lại; không lưu bảng theo span. Các witness chỉ là con trỏ về dữ liệu nguồn, không là tên nút.

Thực thể có địa chỉ ổn định. Kiểu: service, gateway, database, cache, broker, identity-provider, external, host. Kiểu chỉ nhận từ metadata đã xác nhận hoặc thuộc tính có nghĩa đã kiểm; thiếu thì unknown. Không đoán database từ hậu tố tên. Universe là inventory riêng; nút quan sát và trạng thái độ phủ được giữ riêng. Thực thể ngoài alias được giữ nguyên tên, đánh dấu ngoài inventory, không gộp bằng regex.

Thao tác có khóa cặp (thực thể chủ quản, operationName gốc). Dùng JSON của cặp làm ID để tránh va chạm dấu phân cách. Giữ thao tác gốc, nội bộ và thao tác không gọi thực thể khác. Không tạo tên thao tác từ ID đơn/trace/span. Không chuẩn hóa tên theo kết quả khảo sát; tên thiếu giữ null và đánh dấu thiếu tên. Quan hệ thuộc-về là quan hệ địa chỉ, không là lời gọi.

Thành phần endpoint không có span vẫn là thực thể, giữ trong danh sách component_context của mức thao tác. Không tạo thao tác giả. Phép chiếu giữ component_context và thay mỗi đầu mút thao tác bằng thực thể chủ quản; đầu mút thành phần được giữ nguyên. Loại mọi cạnh span-parent, kể cả giữa hai thao tác khác chủ quản, cùng cạnh nội bộ và quan hệ thuộc-về khỏi tập cạnh phụ thuộc thực thể. Các cạnh phụ thuộc còn lại có hai đầu thực thể khác nhau được giữ khi chiếu, gồm cạnh thao tác→thành phần hoặc thành phần→thao tác sau đổi đầu mút. So trên cùng tập quan sát; inventory không cộng vào tập nút quan sát.

Nguồn bằng chứng: trace (quan hệ span/thuộc tính), dataset-other (nguồn khác của dataset), static (kiến trúc), inferred (quan hệ suy ra có witness). Bộ dựng T-035 chỉ tạo trace/inferred; T-036 nhận static. Không tự coi cạnh phụ thuộc là cạnh nhân quả.

## 2. Định dạng span và chính sách lỗi

Các cột lõi: traceID, spanID, parentSpanID, serviceName, operationName, startTime, duration; hai cột cuối là số nguyên microsecond. Nezha ưu tiên _start_ns/_end_ns để giữ nanosecond. Bộ chuyển từ p3 thêm kind=null, attributes={}, links=[]; không bịa trường nguồn không có.

Các thuộc tính mở rộng của hợp đồng nội bộ (cần adapter xác minh nghĩa trước khi điền): entity.type; peer.entity/peer.type cho HTTP endpoint; db.entity/db.type cho database/cache; các trường messaging tại §7; host.id và host.identity_verified. Link có traceID/spanID, semantics=message_creation và semantics_verified=true mới được xét là nối tạo–xử lý bản tin. Đây là hợp đồng nội bộ để fixture kiểm, không tự là tên thuộc tính OTel hoặc yêu cầu đã ban hành cho FlashTicket.

Khóa span = (traceID,spanID), không chỉ spanID. ID rỗng/thiếu, thời gian âm/không nguyên, end<start: từ chối đầu vào, giữ run lỗi. Khóa trùng giống toàn nội dung lõi và mở rộng: bỏ bản lặp khỏi cấu trúc, đếm raw/unique/duplicate riêng. Khóa trùng khác nội dung: dừng, không chọn bản đầu tùy tiện. Parent sentinel rỗng, null, 0, -1, chuỗi toàn số 0 là span gốc. Mọi span unique hợp lệ thuộc đúng một nhóm: gốc, có cha tìm được trong khoảng, mồ côi. Parent nằm ngoài khoảng vẫn là mồ côi trong khoảng; không lấy tương lai/ngoài biên để nối.

Khoảng [lo,hi) nhận span start>=lo và end<hi; end=hi bị loại theo giao thức p3. Khoảng rỗng trả đồ thị rỗng, inventory giữ riêng. Toàn file RE2-TT = toàn bảng span của đúng ca dev. Toàn miền Nezha = toàn tập adapter trả trong [t−300,t+300), không đại diện cả file nguồn. N/A chia quanh mốc ở runner, không ở bộ dựng. N gọi đồ thị tham chiếu trước mốc, không khẳng định nền khỏe. Ảnh chụp RE2 neo min(start), bước 60/300 giây, có cả cửa sổ đuôi và rỗng; chỉ mức thực thể. Lưới có thể trùng mốc; P6 nhận giới hạn này. Không tạo ảnh chụp Nezha.

## 3. Quan hệ và sự kiện bằng chứng

Lời gọi quan sát chưa phân kiểu từ cha–con là cặp span tìm được cha trong cùng khoảng, khác thực thể, không thuộc gọi đồng bộ và không có PRODUCER/CONSUMER ở hai đầu. Hướng là chủ quản cha→chủ quản con; chưa xác nhận là span phía gọi/phía được gọi thật. Một cặp không mặc nhiên là một request mạng. C2 đếm số span trong trace, sự bao thời gian và kiểm tay; thiếu instrumentation thì giữ giả định. Cặp cùng thực thể được giữ ở mức thao tác và đếm nội bộ riêng.

- span-parent: cặp span cha–con tìm được trong cùng khoảng, có ít nhất một đầu mang kind PRODUCER hoặc CONSUMER. Giữ ở mức thao tác dưới dạng quan hệ cha–con đã gộp theo thao tác cùng witness; không khẳng định đây là lời gọi hay quan hệ trao đổi bản tin và không thay thế cây span gốc. Không chiếu span-parent thành cạnh phụ thuộc thực thể, dù hai thao tác khác chủ quản. Các cạnh messaging có bằng chứng riêng vẫn được dựng và chiếu theo §7.
- gọi-đồng-bộ: cặp CLIENT→SERVER với nghĩa kind do adapter xác minh; hoặc CLIENT có peer.entity/peer.type tường minh khi không có SERVER quan sát. Không suy kind từ tên thao tác.
- gọi-chưa-phân-kiểu: các cặp cha–con còn lại sau khi loại gọi đồng bộ và span-parent; không gán quan hệ cha–con có PRODUCER/CONSUMER thành lời gọi chỉ vì hai đầu khác thực thể.
- dữ-liệu: thao tác phía service→database/cache từ db.entity/db.type tường minh. Không suy ownership từ tên.
- thông-điệp: PRODUCER→broker, broker→CONSUMER khi có địa chỉ broker. Địa chỉ phát và queue nhận tách riêng. Link tạo bản tin có nghĩa xác minh trỏ đúng PRODUCER được nối khi các trường cùng hiện diện không mâu thuẫn; không đòi địa chỉ phát bằng queue. Nếu không có link xác minh, message_id chỉ được nối trong cùng broker/broker_scope/identity_scope được xác minh và chỉ có một nguồn tạo quan sát trong miền. Chính sách thiếu/mâu thuẫn và địa chỉ metric ở §7. CorrelationId giao dịch không được dùng. Retry/lần giao lại/lần xử lý là các sự kiện witness riêng, không là các nút thao tác mới.
- triển-khai: thực thể→host khi host.id có host.identity_verified=true. Cùng tên Node ổn định chưa đủ. Chỉ fixture dùng xác nhận giả đã khai; Node Nezha mặc định OPEN.

cross_entity_parent_events đếm mọi cặp span cha–con khác chủ quản tìm được trong cùng khoảng, gồm cả span-parent. Đây là số sự kiện quan hệ cha–con thô, không đồng nghĩa số cạnh hoặc tổng event_count của các cạnh phụ thuộc thực thể sau chiếu. Ví dụ một cặp khác chủ quản có đầu PRODUCER và thiếu bằng chứng messaging có thể cho số đếm này bằng 1 nhưng không tạo cạnh phụ thuộc thực thể; hai nút quan sát vẫn được giữ.

Callback trace mới được giữ như thao tác gốc tại service; CLIENT span phía gọi external tạo service→external. Không bịa external→callback từ correlation/timestamp. Nếu nguồn thật cung cấp bằng chứng gọi vào thì adapter mới thêm span/quan hệ phù hợp. Scheduler là thao tác gốc không có cạnh gọi vào. Outbox gồm thao tác ghi dữ liệu và thao tác publisher; không ghép hai trace bằng correlation. Saga/bù trừ là tên thao tác ổn định và quan hệ quan sát thực; chiều bù trừ không tự đảo cạnh hoặc xác lập nhân quả nghiệp vụ.

## 4. Log, trace, metric và đường dùng cạnh

Trace/spans địa chỉ bằng khóa trace/span→(entity,operation); cây span và thời gian từng lần thực thi phải đọc từ đầu vào gốc khi P6 cần. Đồ thị thao tác không thay cây này.

Log nối theo trace/span hợp lệ; thiếu khóa thì entity+timestamp, chỉ lên mức thực thể; operation tường minh và ổn định mới gắn thao tác. Metric entity/instance/host gắn đúng scope. Metric của cả service là bối cảnh dùng chung, không sao thành bằng chứng độc lập của mọi thao tác. Broker queue metric địa chỉ (broker,broker_scope,queue), chỉ khi đủ ba phần; exchange/routing, message ID và destination legacy không thay địa chỉ queue. Đối tác ngoài chỉ có telemetry phía client. Node chưa xác định host thì không gắn chuỗi metric host vào service.

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


## 6. V1 và thay đổi so với bản trước chạy

Giữ mô hình, scope, cutoff, projection và giới hạn kết luận đã khai ở v0. Sentinel `root` được thêm vào code trước pilot theo nguồn Nezha/T-032; chú giải ở cuối v0 được nối trong pilot-001. Phần chính v0 và đáp án fixture được ghi trước bộ dựng. Không coi chú giải nối sau là bản được ghi trước toàn bộ pilot.

Tối ưu witness bằng mảng chỉ mục và depth bằng memoization; đây là thay cách tính, giữ cùng ngữ nghĩa. Graph hợp lệ pilot cũ khớp từng byte bản mới. Không đổi width, chuẩn hóa tên thao tác, đưa Node thành host hoặc bổ sung cạnh từ metadata mức ngày.

V1 nhận kết quả mô tả: dữ liệu dev dựng cạnh gọi chưa phân kiểu; tên SQL không tự cho ownership/endpoint; Node vẫn OPEN. Mức thao tác giữ thêm nội bộ và phân biệt cặp thao tác; không giữ cây/thời gian từng lần thực thi. Danh mục inventory ở graph thực thể là context chung cho hai mức, không được tính thành thao tác giả.

Các bảng số/câu trả lời C1–C9 và tiêu chí xong ở thong-ke-do-thi.md/JSON; kiểm ở kiem-dung-dan.md; C6 ở cot-node-nezha; C9 ở thong-tin-theo-quan-he. Chưa chọn P6 hoặc nghiệm thu P5. T-036 nhận phiên bản hiện tại sau kiểm để soạn SPEC nguồn tĩnh riêng; P9 nhận hợp đồng dữ liệu theo phạm vi Minh duyệt.

## 7. V2: địa chỉ và bằng chứng messaging

Trường tùy chọn trong attributes: `messaging.broker` là ID thực thể ổn định; `messaging.broker_scope` là namespace triển khai/vhost; `messaging.exchange` và `messaging.routing_key` là địa chỉ phát; `messaging.queue` là queue nhận; `messaging.identity_scope` là namespace của message ID, với `messaging.identity_scope_verified=true` khi adapter đã kiểm nghĩa; `messaging.message_id` là định danh bản tin, `messaging.attempt` là lần giao/xử lý. Exchange/routing chấp nhận chuỗi rỗng có nghĩa (default exchange), khác None là thiếu. Địa chỉ khác khi có phải là chuỗi không rỗng; cờ verified phải là boolean. Cờ này không khẳng định duy nhất nguồn phát quan sát.

`messaging.destination` v1 được giữ nguyên như địa chỉ chưa tách nghĩa. Không tự suy queue, exchange hay identity scope từ đó; chỉ ID + destination không đủ để nối. Dữ liệu cũ có link xác minh vẫn có thể nối, nhưng thiếu queue/scope thì không có địa chỉ metric hoàn chỉnh.

Cạnh thông điệp có đối tượng `messaging` với broker, broker_scope, exchange, routing_key, queue (trường thiếu là null), cùng `queue_metric_address`. Cạnh phát không có queue/metric queue. Cạnh nhận lấy địa chỉ phía nhận. Cạnh logic giữ địa chỉ phía nhận và bổ sung exchange/routing từ phía phát nếu phía nhận thiếu. Khi broker, broker_scope, queue đều có, metric address là mảng ba giá trị đó; thiếu thì null. Phép gộp, fingerprint và phép chiếu giữ toàn bộ địa chỉ; hai queue cùng service/thao tác vẫn là hai cạnh. Metric có cùng địa chỉ trên nhiều cạnh là một chuỗi bối cảnh dùng chung, không nhân thành các quan sát độc lập.

Link xác minh phải trỏ nguồn PRODUCER trong miền đang dựng. So broker, broker_scope, exchange, routing_key, identity_scope, message_id khi cả hai phía có trường đó; queue và destination legacy không cần bằng nhau. Có link xác minh thì không dùng ID fallback; từng link hợp lệ được giữ, từng link thiếu nguồn/sai kind/mâu thuẫn bị báo. Batch có một phần nối được chưa là batch đầy đủ. Link không xác minh hoặc sai semantics không phải bằng chứng; vẫn có thể xét ID độc lập.

ID fallback yêu cầu cả hai phía có broker, broker_scope, identity_scope, identity_scope_verified=true, message_id. Tìm theo (broker,broker_scope,identity_scope,message_id); không có hoặc nhiều PRODUCER trong miền thì không nối. Một nguồn thì còn kiểm mâu thuẫn các trường cùng hiện diện như nhánh link. Không đọc span ngoài miền để nối hoặc chọn nguồn. Retry có nhiều nguồn cùng ID mà thiếu link xác minh vẫn là đa nghĩa.

`unresolved_messages` đếm consumer không có cạnh logic. `messaging_diagnostics` ở cả hai mức báo count và tối đa hai witness (traceID,spanID) theo nguyên nhân: link_source_unavailable, link_source_not_producer, link_scope_conflict, identity_unverified, identity_no_source, identity_ambiguous, identity_scope_conflict, queue_address_incomplete. Thiếu địa chỉ metric đếm một lần mỗi consumer, không đếm producer hoặc đếm lại cạnh logic. Một consumer có thể có nhiều vấn đề; không cộng cờ thành tỷ lệ nguyên nhân. Cạnh không messaging và graph dev không messaging giữ schema cũ.

Thiết kế trước code ở runs/sua-n1-001/design.md; inputs và oracle trước code ở fixture_inputs.json, fixture_expected.json trong cùng lượt. fixture_design.md giải thích từng tình huống và cách kiểm. Kết quả kiểm và hồi quy được ghi sau chạy trong cùng lượt; xem kiem-dung-dan.md. Bản v2 sửa mâu thuẫn hợp đồng v1, không tuyên bố routing/instrumentation FlashTicket thật đã kiểm hoặc lợi ích RCA đã xác nhận.

## 8. V2.1: dữ liệu thiếu, miền ID và chính sách từ chối

Tên thao tác thiếu được chuẩn hóa thành null trước tạo khóa, không phụ thuộc dtype float64, object hoặc nullable string của pandas. Không thay tên có giá trị hoặc tạo thao tác từ mã lần thực thi. missing_operation đếm số span thiếu tên, thao tác của cùng entity/tên null dùng cùng khóa.

ID thao tác giữ định dạng JSON cặp; tập ID này được giữ chỗ trên toàn bảng Prepared. ID thực thể quan sát sau alias hoặc endpoint thực (database/cache, peer, broker, host) không được trùng ID thao tác. Vi phạm từ chối identifier_collision trước xuất đồ thị; project cũng kiểm giao giữa khóa belongs_to với chủ quản/component_context trước chiếu. Inventory-only nằm ngoài tập quan sát nên không gây va chạm. Đây là giới hạn đầu vào tường minh của định dạng hiện tại; cần hỗ trợ ID va chạm thì phải thiết kế namespace riêng, không âm thầm đổi đích hoặc bỏ cạnh.

Mọi cột thời gian có mặt phải là số nguyên hữu hạn, không âm, thuộc [0, 2**63−1] trước ép int64. Số object/chuỗi được kiểm chính xác, không đổi qua float làm tròn số lớn. Khi một đầu thời gian phải đổi từ microsecond, kiểm giá trị hoặc tổng startTime+duration không vượt floor((2**63−1)/1000) trước nhân 1000 hoặc cộng. Ưu tiên _start_ns/_end_ns từng cột khi có; phép đổi us không được dùng thì không bắt buộc thực hiện nó, nhưng cột us vẫn phải hợp lệ trong int64. Sau chọn nguồn, end phải không nhỏ hơn start. Vi phạm từ chối invalid_time, không wrap/clamp hoặc bỏ span. Quy tắc cửa sổ không đổi.

Gộp kiểu từ inventory, entity.type và endpoint theo một quy tắc: unknown với kiểu đã biết nhận kiểu đã biết; kiểu đã biết với unknown giữ kiểu đã biết; hai kiểu đã biết giống nhau giữ nguyên; khác nhau từ chối conflicting_entity_type. Áp dụng cả inventory của endpoint chưa có span. Không coi thứ tự dòng là bằng chứng xác định kiểu.

Thiết kế và đáp án literal trước mã ở runs/sua-hop-dong-001/design.md, oracle.py và receipt oracle-before-code.json; kết quả kiểm/hồi quy được ghi sau chạy. Bản này xử lý hợp đồng kỹ thuật, chưa xác nhận nghĩa vật lý cạnh, runtime FlashTicket hoặc lợi ích RCA.

## 9. Đính chính văn bản v2.1 — span-parent (15/10/2026)

Theo Q-156, mục 1 và 3 được làm rõ để khớp chính sách đã cài và ngoại lệ đã ghi ở K5. Không đổi code, phép dựng/chiếu hoặc số dev. Bản trước và kiểm sau sửa được giữ tại runs/dong-bo-span-parent-001/. Việc đồng bộ này chưa là nghiệm thu toàn bộ hợp đồng, xác nhận nghĩa instrumentation hay lợi ích RCA.
