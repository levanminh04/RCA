# Thiết kế sửa hợp đồng messaging — trước sửa code

Quyền: Q-154, ngày 15/10/2026. Đây là sửa hợp đồng biểu diễn T-035; không chọn phương pháp P6, không sửa SPEC hay hệ FlashTicket. Bằng chứng cần phân xử là fixture có địa chỉ phát khác queue nhận và phép chiếu giữ riêng queue. Chạy lại dev chỉ kiểm hồi quy.

## Trường nội bộ

Adapter phải xác minh nghĩa trước khi điền. Các trường tùy chọn: `messaging.broker` (ID thực thể broker ổn định), `messaging.broker_scope` (phạm vi triển khai/vhost/namespace), `messaging.exchange`, `messaging.routing_key`, `messaging.queue`, `messaging.identity_scope`, `messaging.identity_scope_verified`, `messaging.message_id`. Chuỗi exchange/routing rỗng có nghĩa (ví dụ default exchange); None là thiếu. Các địa chỉ khác phải là chuỗi không rỗng khi hiện diện. Identity scope là namespace được xác minh của ID bản tin, không phải queue; cờ verified chỉ xác nhận nghĩa namespace, không chứng minh nguồn tạo quan sát là duy nhất.

Giữ `messaging.destination` cũ như địa chỉ chưa tách nghĩa. Không suy exchange/queue/identity scope từ nó. Không dùng nó để ép hai phía bằng nhau. Fixture cũ dùng link xác minh vẫn có thể nối; chỉ message ID + destination không còn đủ để nối. Thiếu queue/scope thì báo thiếu địa chỉ metric, không bịa giá trị.

## Cạnh và địa chỉ metric

Cạnh thông điệp thêm `messaging` gồm đúng broker, broker_scope, exchange, routing_key, queue; không chứa ID bản tin, identity scope hoặc attempt. Cạnh phát lấy phía phát, queue=None; cạnh nhận lấy phía nhận. Cạnh logic lấy phía nhận, bổ sung exchange/routing từ nguồn phát chỉ khi phía nhận thiếu. `queue_metric_address` là [broker,broker_scope,queue] khi đầy đủ; nếu thiếu thì None. Cạnh phát không nhận queue metric. Giữ destination legacy riêng. Các trường messaging cùng tham gia khóa gộp, fingerprint và phép chiếu hai mức. Queue của hai cạnh không nhập nhau chỉ vì cùng service/operation. Retry giữ count/witness riêng trên cùng cạnh, không tạo nút theo ID hay attempt. Nguồn span gốc vẫn cần để lấy mọi lần thực thi.

Không thêm trường vào cạnh không phải messaging; đồ thị dev không có messaging dự kiến giữ nguyên từng byte. Đây là dự đoán phải kiểm, chưa là kết quả.

## Nối bản tin

1. Chỉ nhận link semantics=message_creation, semantics_verified=true. Nguồn phải là PRODUCER trong cùng miền quan sát. So mọi cặp thông tin cùng hiện diện: broker, broker_scope, exchange, routing_key, identity_scope, message_id. Queue và destination legacy không cần bằng nhau. Không có message ID vẫn nối được bằng link đủ nghĩa. Thông tin thiếu không bị coi là mâu thuẫn; không lấy span ngoài cửa sổ để nối.
2. Có link được khai xác minh thì chỉ dùng các link hợp lệ; báo riêng link thiếu nguồn, sai kind hoặc mâu thuẫn. Không dùng ID fallback để che một link xác minh không hợp lệ. Nếu một consumer có nhiều link, giữ phần có bằng chứng; báo phần chưa nối. Không biến phần nối được thành khẳng định batch đã đầy đủ.
3. Không có link xác minh thì được xét message ID. Hai phía phải có broker, broker_scope, identity_scope, identity_scope_verified=true và message_id. Tìm đúng bốn khóa (broker,broker_scope,identity_scope,message_id), chỉ nhận một PRODUCER trong miền. Kiểm tiếp các trường cùng hiện diện như nhánh link. Không có nguồn/đa nghĩa/mâu thuẫn thì unresolved. Không dùng correlation, timestamp gần hoặc nhãn để ghép.
4. `unresolved_messages` đếm consumer không có cạnh logic. `messaging_diagnostics` báo nguyên nhân với count và tối đa hai witness trace/span mỗi nguyên nhân, gồm link_source_unavailable, link_source_not_producer, link_scope_conflict, identity_unverified, identity_no_source, identity_ambiguous, identity_scope_conflict, queue_address_incomplete. Một consumer có thể có nhiều vấn đề; không cộng chúng thành tỷ lệ nguyên nhân. Không có messaging thì giữ schema dev cũ.

## Phép kiểm và kết luận được phép

Đáp án fixture do trợ lý triển khai lập từ literal trước code, oracle không dùng helper định danh cạnh của builder. Kiểm exact cạnh hai mức, count, witness, queue metric và phép chiếu; đối chứng nguồn/đích thiếu, mâu thuẫn, ID khác scope, nhiều nguồn, correlation, retry và biên thời gian. Phát lại fixture cũ. Chạy lại toàn bộ dev theo allowlist, cửa sổ, inventory và adapter cũ; giữ lượt mới và so graph, vocabulary, stats/coverage/checks với bản cũ. Không tái sinh hay ghi đè các graph cũ.

Fixture đạt chỉ xác nhận bộ dựng theo hợp đồng này. Không xác nhận instrumentation FlashTicket, delivery routing thật, semantics nguồn chưa biết, hiệu quả RCA hoặc Node là host. P9 cần dữ liệu thật và adapter đã xác minh. T-036 nhận v2 sau kiểm; không tự nghiệm thu P5/G3.
