# Đối chiếu nguồn và graph dev RE2-TT

Đã so mọi graph hiện hành được giao, trên nguồn tham khảo có điều kiện. Số và từng thành viên nằm trong `runs/doi-chieu-dev-002/summary.json#/rows`, JSON gzip theo `doi-chieu/index.json` và `phan-tich-chenh-lech.json`. Bảng sau là min–max từng graph, không phải số cạnh độc nhất gộp qua ca.

| Mức/miền | Graph | S | T | Giao | Riêng tĩnh | Riêng trace |
|---|---:|---:|---:|---:|---:|---:|
| entity/A | 30 | 159 | 16–49 | 15–44 | 115–144 | 1–5 |
| entity/N | 30 | 159 | 16–49 | 15–44 | 115–144 | 1–5 |
| entity/full | 30 | 159 | 16–49 | 15–44 | 115–144 | 1–5 |
| entity/s300 | 150 | 159 | 16–49 | 15–44 | 115–144 | 1–5 |
| entity/s60 | 739 | 159 | 0–49 | 0–44 | 115–159 | 0–5 |
| operation/A | 30 | 340 | 0 | 0 | 340 | 0 |
| operation/N | 30 | 340 | 0 | 0 | 340 | 0 |
| operation/full | 30 | 340 | 0 | 0 | 340 | 0 |

30 dev ID là mã mờ để điều phối, không đi vào phép tính khóa cạnh. Chọn đúng prefix manifest T035, không trộn lịch sử. Có 979 graph thực thể và 90 graph thao tác; full/N/A ở cả hai mức, 739 cửa sổ 60 giây và 150 cửa sổ 300 giây ở mức thực thể. Giữ interval/miền gốc; không mở lại telemetry để dựng cửa sổ khác. Nguồn số: `summary.json#/graph_family_counts`.

S là khóa tĩnh đủ điều kiện, T là khóa trace đủ điều kiện sau mapping; giao và hai phần riêng được tính bằng tập có hướng. Mỗi khóa giữ members với chỉ số/cạnh gốc/provenance riêng hai nguồn; exclusions phân hoạch phần không vào khóa. Không dùng inventory hoặc nút quan sát làm mẫu số cạnh. Typed T rỗng ở toàn bộ 1.069 graph vì kiểu trace còn unknown, hoặc đầu mút thao tác chưa đủ mapping. Trace fraction là null khi mẫu số rỗng, không là 0% coverage. 19 cửa sổ s60 có T endpoints rỗng, cũng giữ null. Các trường min/max/null_count đầy đủ ở `phan-tich-chenh-lech.json#/family_stats`.

## Đầu mút khớp không xác nhận transport hoặc phiên bản

Ví dụ admin-basic-info → config: mã nguồn có các callsite HTTP GET/POST/PUT/DELETE; bản ghi giữ từng điều kiện và provenance, graph thực thể gộp thành cặp có hướng. Mapping identity dựa khai báo component, không dựa nhãn. Cạnh trace cùng cặp giữ `gọi-chưa-phân-kiểu`; vì thế endpoints có thể giao nhưng typed bị loại. Chuỗi nguồn → record_ids → edge → members → tập nằm tại `phan-tich-chenh-lech.json#/chain_examples`, lọc cặp này; locator nguồn đi kèm từng member. Bước so typed giữ thiếu thông tin thay vì lấy HTTP nguồn lấp unknown trace. Không xác nhận HTTP/RPC transport của runtime hoặc instrumentation coverage từ endpoint match.

## Năm cặp riêng trace và đối chiếu nguồn tương ứng

Hợp của full endpoints có đúng năm cặp riêng trace: food→station, seat→travel, seat→travel2, travel→order, travel2→order-other (`phan-tich-chenh-lech.json#/full_union`, entity/endpoints/trace_only). Từng trường hợp, số graph chứa và witnesses gốc còn trong `edge-groups.json` và members; không cộng số xuất hiện qua cửa sổ thành số nguyên nhân.

Đã đọc toàn 38 Java file hiện hành của bốn module và helper liên quan. Không tìm được direct call cho năm cặp trong corpus đó. Control dương cùng cách gọi: food gọi travel và station-food; travel/travel2 gọi seat; seat gọi order hoặc order-other theo nhánh G/D. Chain travel→seat→order có controller/service và callsite đúng dòng; không co thành direct travel→order, không đảo chiều thành seat→travel. Biến stationResult trong food nhận body từ travel, tên biến không tạo endpoint station. Nguồn và line ở `runs/trien-khai-001/coverage/mismatch-source-followup.json#/pairs`; chuỗi so sánh ở JSON phân tích.

Quan sát này hỗ trợ việc nguồn tham khảo không cung cấp direct edge tương ứng trong phần đã kiểm. Chưa phân xử source revision khác, alias/config override, dependency động, thiếu phân tích tĩnh, cấu trúc span hoặc instrumentation runtime. Không gọi absence nguồn là lỗi collector hoặc khẳng định runtime không có call. Cần application/image/instrumentation/deployment của bản thu và callsite/span attributes trước khi phân xử các giải thích đó.

## Khác tên và khác họ cấu hình

Hai tên observed `ts-food-map-service` và `ts-ticketinfo-service` không có identity đã xác minh trong inventory hiện hành nên giữ unmapped; không đổi thành station-food/basic theo chức năng giống nhau. Các tên thao tác kiểu `find ts.*`, `getMore`, `update`, và `find ts-auth-mongo.user` là chuỗi đã lưu, không tự chứng minh database implementation. V1 nguồn dùng JDBC/MySQL/Nacos, các sơ đồ/nguồn Mongo lịch sử thuộc profile khác. Đây là dấu hiệu cần kiểm lineage, chưa xác nhận nguyên nhân riêng của từng mismatch. Mapping và ghi chú đầy đủ ở `mapping.json`, `mapping-summary.json`, `runs/doi-chieu-dev-002/mapping-notes.json`.

## Vì sao mức thao tác chưa so được T

54 tên thao tác toàn miền có descriptor HTTP cùng owner khớp chính xác về cấu trúc; 16 mơ hồ, 35 candidate chưa verified và 49 unmapped. Đây là status của 154 tên khác nhau, không phải tỷ lệ cạnh. T035 đặt ID bằng (serviceName, operationName), tại `src/do_thi/builder.py:177–181`; generic GET trong cùng owner không giữ callsite/URL để chọn giữa nhiều source method. Các method repository chỉ là candidate; không biết agent đã tạo span ấy thế nào. Cụ thể chuỗi input operationName → ID T035 → mapping nhiều/chưa xác minh → exclusion đầu mút → không tạo khóa T đã được lưu trong `phan-tich-chenh-lech.json#/exclusions`. Trong 90 graph thao tác, mọi cạnh bị loại ở ít nhất một đầu mút; do đó T đủ điều kiện rỗng, không có nghĩa không có lời gọi.

Đây là hạn chế địa chỉ của graph đầu vào và quan hệ mapping hiện tại. Chưa chứng minh trường URI/kind/callsite đã từng có trước conversion hay collector làm mất: đặc tả T035 §2 chỉ cam kết lõi, p3 thêm kind=null/attributes={}/links=[]; raw không được mở ở task này. Muốn phân xử cần schema/instrumentation tại phiên bản thu hoặc trung gian được duyệt có URI/callsite/span-kind; không được tự dùng endpoint nguồn tạo runtime_name. Runtime_name của các operation nguồn vẫn OPEN. Đối chiếu dương exact owner+HTTP descriptor và phản ví dụ generic GET/sai owner/concrete ID nằm trong oracle và fixture result.

## Cửa sổ, nhánh và phần riêng tĩnh

Nguồn là hợp các lời gọi khai báo có điều kiện, không path-sensitive reachability hay workload. Bởi vậy không gán mọi static_only là mất telemetry. `edge-groups.json` giữ ví dụ cùng cặp khớp full nhưng vắng ở s60 cùng dev ID; điều này xác nhận membership thay theo miền, chưa nói vì không chạy nhánh, không quan sát, hay xử lý biên. Muốn phân xử cần workload/version và trung gian đã thu trong quyền. Thành phần source-only và DB default chưa được runtime xác nhận cũng có thể tạo phần riêng tĩnh; không cộng các nhóm chồng lấn thành tỷ lệ nguyên nhân.

## Lỗi literal nguồn và giới hạn hợp đồng

Rebook.updateOrder dùng PUT, khớp handler PUT của order/order-other. Cùng helper/owner, deleteOrder lại POST lên đường dẫn orderId trong khi handler khai DELETE. PollThread POST `/api/v1/contactservice/preserve`, khác handler `/api/v1/preserveservice/preserve`. Giữ nguyên literal và candidate, không sửa nguồn để tạo match; entity match có thể che bất nhất method/path. Đây là bất nhất source snapshot, chưa chứng minh bug của RE2. Mã/line trước→sau đã lưu tại `runs/doi-chieu-dev-002/source-chain-snippets.json`.

Messaging giữ queue/routing key khai báo, broker quickstart có điều kiện, broker_scope/exchange chưa xác minh nên bị loại theo hợp đồng; không nối producer→consumer chỉ từ tên queue. DB logical schema khác endpoint instance và owner; source default/env override không là physical deployment. Shared signal chỉ gắn entity một lần theo nguồn, operation=null, không nhân thành tín hiệu quan sát mỗi operation. Java logger và Java-agent env là khai báo; chưa có output schema/correlation, ba module nonJava có env Java-agent chưa chứng minh agent hoạt động.

SMTP có cấu hình smtp.163.com:465 và MailService.sender.send; enum T036 không nhận channel này. Đã lưu phản ví dụ thật, giữ external entity và ngừng riêng relation SMTP, không ép thành HTTP/RPC/broker. Đó là thiếu biểu diễn ở giao thức nguồn, khác thiếu dữ liệu hay lỗi adapter. Toàn mô hình chưa đủ quan hệ. Archive/libraries/config chưa render còn giới hạn về activation/runtime; rà bổ sung đã phân loại toàn bộ27 mục cũ, chỉ body PDF converter lịch sử chưa mở. PDF không chặn declared-current module inventory, nhưng không nhận toàn nội dung/semantics đã đầy đủ.

## Hàm ý nghiên cứu

Đồ thị được dùng để chuẩn hóa địa chỉ, chiếu operation→entity, tạo khóa có hướng và tính giao/phần riêng; chưa tính anomaly score, tập ứng viên hay rank. Kết quả hỗ trợ đầu vào kiến trúc/địa chỉ và yêu cầu quan sát cho DT18 bước khảo sát, RQ3/RQ5. Chưa chứng minh lợi ích RCA, cơ chế của lỗi baseline, nên chưa chọn P6 hay đóng G3. Bảng input/owner/phép phân xử/P6/P9 nằm ở `ban-giao.md` và `de-nghi-tiep-theo.md`.


## Bổ sung sau yêu cầu làm hết phần trong quyền

Chín cờ `http_target_unresolved_alternative` trước đây không còn là đích chưa biết của source. Đã đọc từng đoạn: URL khởi tạo rỗng, sau đó cả hai nhánh if/else gán URL trước call. Nếu condition/assignment ném exception thì không tới call; nếu tới call bình thường thì không còn giá trị rỗng. Đây là overapproximation của extractor lexical, không phải thiếu telemetry. Oracle đọc tay, source hash/line và chín chuỗi đầy đủ ở `runs/hoan-tat-trong-quyen-001/{manual-branch-oracle.json,source-flag-resolution.json}`. Không sửa source hay tự chứng minh nhánh đã chạy. Các alternative không rỗng đã có trong model005, nên đóng cờ không đổi graph/mapping/kết quả.

Đã phân loại toàn151 tracking row:9 closed initializer,71 candidate target operation,67 branch/value conditions và4 external/literal discrepancies đã đọc nguồn. Chúng chồng lấn, không là151 ca lỗi hay tỷ lệ nguyên nhân. Candidate dynamic URL giữ nguyên vì source pattern không chứng minh giá trị URL/routing runtime; bốn no-handler đã có external implementation thiếu hoặc source method/path bất nhất. Giữ chúng có điều kiện là kết quả khảo sát, không tự biến thành nghĩa vụ chạy runtime không được giao.

Metadata reconstruction nguồn đã duyệt ghi xóa ticketinfo, tách food-map, migration MySQL và Skywalking (`runs/hoan-tat-trong-quyen-001/release-refactor-metadata.json`). Điều này củng cố khác biệt source/profile đã quan sát; chưa nối được nguồn thu RE2 nên không dùng làm alias hoặc nguyên nhân xác nhận cho năm cặp riêng trace. Tra metadata tiếp có phạm vi/receipt ở lineage-resolution.json; kết quả so vẫn conditional. Không cần chạy lại1069 graph vì mọi input model/graph/mapping và numerical output giữ nguyên hash.
