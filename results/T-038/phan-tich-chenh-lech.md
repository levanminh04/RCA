# Đối chiếu hiện hành T-038 sau tiếp nhận R1

Người làm đã kiểm nguồn rồi sửa chính thức. Chờ người phản biện kiểm bản sửa và Minh quyết; chưa nghiệm thu task. Nguồn số: `results/T-038/runs/sua-r1-20261017-001/checks/full1069-002/summary.json#/rows`, `phan-tich-chenh-lech.json#/family_stats` và `results/T-038/runs/sua-r1-20261017-001/model-checks.json`.

Mô hình có 110 thực thể, 993 thao tác, 513 relation, 50 binding và 139 signal. Có 170 cạnh thực thể, 343 cạnh thao tác; phép chiếu 122 cạnh và phần chỉ có ở mức thực thể 48 cạnh. Từng nhóm giữ locator và điều kiện nguồn, không xác nhận quan hệ đã chạy trong dataset.

R1 là lỗi trích/lập bản ghi: cấu hình → bản ghi từng bỏ Skywalking→Elasticsearch, Alertsnitch→MySQL, Nacos→MySQL và webhook Alertmanager→Alertsnitch. Nguồn gốc đủ để ghi quan hệ cấu hình có điều kiện; chưa đủ để nói runtime hoạt động. Ba cạnh đầu là dữ liệu; webhook giữ gọi-chưa-phân-kiểu/http, không tự nâng thành đồng bộ. Bằng chứng: `results/T-038/runs/sua-r1-20261017-001/source-checks.json#/checks`, `accepted-delta.json` trong cùng run; từng cạnh→record_ids→provenance→locator đi vào members của output.

So với bản SMTP V2 trước sửa: 979 graph entity thêm 4 S/static-only ở endpoints, 3 S/static-only ở typed và 1 unknown exclusion typed. Mẫu số tĩnh tăng tương ứng; tỷ lệ phải đọc lại. T/giao/trace_only, members và exclusions phía trace giữ nguyên. 90 output operation giữ nguyên cấu trúc/tập/số, chỉ đồng bộ mô tả SMTP; JSON graph operation có thêm 4 record/operation exclusion nhưng cạnh không đổi. Root phép chiếu cũ thiếu SMTP đã được thay: 121→122; entity-only44→48. So với phép chiếu V2 đúng trong run cũ, projection122 không đổi. Một mô tả entity.role SMTP được đổi từ ghi chú unsupported lịch sử sang hỗ trợ V2 có điều kiện; chỉ metadata node đổi, không đổi ID/type/provenance hay phép tính. inventory-index trước còn đếm508 relation, nên bản đồng bộ513 gồm4 R1 và1 SMTP đã bị bỏ khỏi chỉ mục. Xem metadata-correction.json và inventory-index-delta.json trong run sửa. Bảng delta từng graph: `results/T-038/runs/sua-r1-20261017-001/checks/full1069-002/delta.json#/rows`.

| Mức/miền/view | Graph | S | T | Giao | Riêng tĩnh | Riêng trace |
|---|---:|---:|---:|---:|---:|---:|
| entity/A/endpoints | 30 | 164 | 16–49 | 15–44 | 120–149 | 1–5 |
| entity/A/typed | 30 | 162 | 0 | 0 | 162 | 0 |
| entity/N/endpoints | 30 | 164 | 16–49 | 15–44 | 120–149 | 1–5 |
| entity/N/typed | 30 | 162 | 0 | 0 | 162 | 0 |
| entity/full/endpoints | 30 | 164 | 16–49 | 15–44 | 120–149 | 1–5 |
| entity/full/typed | 30 | 162 | 0 | 0 | 162 | 0 |
| entity/s300/endpoints | 150 | 164 | 16–49 | 15–44 | 120–149 | 1–5 |
| entity/s300/typed | 150 | 162 | 0 | 0 | 162 | 0 |
| entity/s60/endpoints | 739 | 164 | 0–49 | 0–44 | 120–164 | 0–5 |
| entity/s60/typed | 739 | 162 | 0 | 0 | 162 | 0 |
| operation/A/endpoints | 30 | 341 | 0 | 0 | 341 | 0 |
| operation/A/typed | 30 | 340 | 0 | 0 | 340 | 0 |
| operation/N/endpoints | 30 | 341 | 0 | 0 | 341 | 0 |
| operation/N/typed | 30 | 340 | 0 | 0 | 340 | 0 |
| operation/full/endpoints | 30 | 341 | 0 | 0 | 341 | 0 |
| operation/full/typed | 30 | 340 | 0 | 0 | 340 | 0 |

Bảng là min–max từng graph, không phải hợp độc nhất. Có 979 entity, 90 operation, 739 cửa sổ s60 và 150 s300; 30 full/N/A mỗi mức. Các interval và tập graph giữ nguyên. S/T là khóa cạnh đủ điều kiện, không là số inventory. Mẫu số T rỗng giữ null; typed T rỗng không phải không có traffic. Members và exclusions phân hoạch từng chỉ số cạnh; không cộng chúng thành tỷ lệ nguyên nhân.

## Đầu mút khớp không xác nhận transport hoặc phiên bản

Ví dụ admin-basic-info → config: mã nguồn có các callsite HTTP GET/POST/PUT/DELETE; bản ghi giữ từng điều kiện và provenance, graph thực thể gộp thành cặp có hướng. Mapping identity dựa khai báo component, không dựa nhãn. Cạnh trace cùng cặp giữ `gọi-chưa-phân-kiểu`; vì thế endpoints có thể giao nhưng typed bị loại. Chuỗi nguồn → record_ids → edge → members → tập nằm tại `phan-tich-chenh-lech.json#/chain_examples`, lọc cặp này; locator nguồn đi kèm từng member. Bước so typed giữ thiếu thông tin thay vì lấy HTTP nguồn lấp unknown trace. Không xác nhận HTTP/RPC transport của runtime hoặc instrumentation coverage từ endpoint match.

## Năm cặp riêng trace và đối chiếu nguồn tương ứng

Hợp của full endpoints có đúng năm cặp riêng trace: food→station, seat→travel, seat→travel2, travel→order, travel2→order-other (`phan-tich-chenh-lech.json#/full_union`, entity/endpoints/trace_only). Từng trường hợp, số graph chứa và witnesses gốc còn trong `runs/doi-chieu-dev-002/edge-groups.json` và members; không cộng số xuất hiện qua cửa sổ thành số nguyên nhân.

Đã đọc toàn 38 Java file hiện hành của bốn module và helper liên quan. Không tìm được direct call cho năm cặp trong corpus đó. Control dương cùng cách gọi: food gọi travel và station-food; travel/travel2 gọi seat; seat gọi order hoặc order-other theo nhánh G/D. Chain travel→seat→order có controller/service và callsite đúng dòng; không co thành direct travel→order, không đảo chiều thành seat→travel. Biến stationResult trong food nhận body từ travel, tên biến không tạo endpoint station. Nguồn và line ở `runs/trien-khai-001/coverage/mismatch-source-followup.json#/pairs`; chuỗi so sánh ở JSON phân tích.

Quan sát này hỗ trợ việc nguồn tham khảo không cung cấp direct edge tương ứng trong phần đã kiểm. Chưa phân xử source revision khác, alias/config override, dependency động, thiếu phân tích tĩnh, cấu trúc span hoặc instrumentation runtime. Không gọi absence nguồn là lỗi collector hoặc khẳng định runtime không có call. Cần application/image/instrumentation/deployment của bản thu và callsite/span attributes trước khi phân xử các giải thích đó.

## Khác tên và khác họ cấu hình

Hai tên observed `ts-food-map-service` và `ts-ticketinfo-service` không có identity đã xác minh trong inventory hiện hành nên giữ unmapped; không đổi thành station-food/basic theo chức năng giống nhau. Các tên thao tác kiểu `find ts.*`, `getMore`, `update`, và `find ts-auth-mongo.user` là chuỗi đã lưu, không tự chứng minh database implementation. V1 nguồn dùng JDBC/MySQL/Nacos, các sơ đồ/nguồn Mongo lịch sử thuộc profile khác. Đây là dấu hiệu cần kiểm lineage, chưa xác nhận nguyên nhân riêng của từng mismatch. Mapping và ghi chú đầy đủ ở `mapping.json`, `mapping-summary.json`, `runs/doi-chieu-dev-002/mapping-notes.json`.

## Vì sao mức thao tác chưa so được T

54 tên thao tác toàn miền có descriptor HTTP cùng owner khớp chính xác về cấu trúc; 16 mơ hồ, 35 candidate chưa verified và 49 unmapped. Đây là status của 154 tên khác nhau, không phải tỷ lệ cạnh. T035 đặt ID bằng (serviceName, operationName), tại `src/do_thi/builder.py:177–181`; generic GET trong cùng owner không giữ callsite/URL để chọn giữa nhiều source method. Các method repository chỉ là candidate; không biết agent đã tạo span ấy thế nào. Cụ thể chuỗi input operationName → ID T035 → mapping nhiều/chưa xác minh → exclusion đầu mút → không tạo khóa T đã được lưu trong `phan-tich-chenh-lech.json#/exclusions`. Trong 90 graph thao tác, mọi cạnh bị loại ở ít nhất một đầu mút; do đó T đủ điều kiện rỗng, không có nghĩa không có lời gọi.

Đây là hạn chế địa chỉ của graph đầu vào và quan hệ mapping hiện tại. Chưa chứng minh trường URI/kind/callsite đã từng có trước conversion hay collector làm mất: đặc tả T035 §2 chỉ cam kết lõi, p3 thêm kind=null/attributes={}/links=[]; raw RE2 không được mở để phân xử trong phép này. Muốn phân xử cần schema/instrumentation tại phiên bản thu hoặc trung gian được duyệt có URI/callsite/span-kind; không được tự dùng endpoint nguồn tạo runtime_name. Runtime_name của các operation nguồn vẫn OPEN. Đối chiếu dương exact owner+HTTP descriptor và phản ví dụ generic GET/sai owner/concrete ID nằm trong oracle và fixture result.

## Cửa sổ, nhánh và phần riêng tĩnh

Nguồn là hợp các lời gọi khai báo có điều kiện, không path-sensitive reachability hay workload. Bởi vậy không gán mọi static_only là mất telemetry. `runs/doi-chieu-dev-002/edge-groups.json` giữ ví dụ cùng cặp khớp full nhưng vắng ở s60 cùng dev ID; điều này xác nhận membership thay theo miền, chưa nói vì không chạy nhánh, không quan sát, hay xử lý biên. Muốn phân xử cần workload/version và trung gian đã thu trong quyền. Thành phần source-only và DB default chưa được runtime xác nhận cũng có thể tạo phần riêng tĩnh; không cộng các nhóm chồng lấn thành tỷ lệ nguyên nhân.

## Lỗi literal nguồn và giới hạn hợp đồng

Rebook.updateOrder dùng PUT, khớp handler PUT của order/order-other. Cùng helper/owner, deleteOrder lại POST lên đường dẫn orderId trong khi handler khai DELETE. PollThread POST `/api/v1/contactservice/preserve`, khác handler `/api/v1/preserveservice/preserve`. Giữ nguyên literal và candidate, không sửa nguồn để tạo match; entity match có thể che bất nhất method/path. Đây là bất nhất source snapshot, chưa chứng minh bug của RE2. Mã/line trước→sau đã lưu tại `runs/doi-chieu-dev-002/source-chain-snippets.json`.

Messaging giữ queue/routing key khai báo, broker quickstart có điều kiện, broker_scope/exchange chưa xác minh nên bị loại theo hợp đồng; không nối producer→consumer chỉ từ tên queue. DB logical schema khác endpoint instance và owner; source default/env override không là physical deployment. Shared signal chỉ gắn entity một lần theo nguồn, operation=null, không nhân thành tín hiệu quan sát mỗi operation. Java logger và Java-agent env là khai báo; chưa có output schema/correlation, ba module nonJava có env Java-agent chưa chứng minh agent hoạt động.

SMTP đã biểu diễn theo pin V2; record giữ kiểu chưa phân loại, không suy authority/TLS/delivery hoặc runtime. Hậu tố proposed-only trong ID SMTP là định danh lịch sử được giữ để truy provenance; trạng thái áp dụng nằm ở manifest hiện hành. Bốn dependency cấu hình bổ sung cũng chỉ là khả năng có điều kiện trong snapshot. Không biến nguồn tĩnh thành graph runtime đã xác minh.

## Phần còn mở và vai trò tính toán

Đã kiểm các địa chỉ còn lại từ nguồn hiện có tại `results/T-038/runs/sua-r1-20261017-001/source-audit.json#/further_source_addresses`. UI→OAP và Prometheus→Alertmanager thiếu protocol đã xác minh; discovery/scrape thiếu binding/owner, Grafana chưa có datasource address trong file. Hợp đồng đang ghim không nhận call channel unknown. Không dùng port/image/role để lấp; thay hợp đồng hoặc lấy semantics image/client cần quyền riêng. Điều này giới hạn kết luận đầy đủ cấu hình, không phủ nhận bốn quan hệ đã có bằng chứng.

Đồ thị dùng nút thực thể/thao tác, cạnh gọi/thông điệp/dữ liệu và provenance để chiếu, tạo khóa có hướng, tính giao/phần riêng. Signal log/trace/metric là địa chỉ khai báo gắn entity/operation theo nguồn; chưa tính anomaly score, vùng ảnh hưởng hoặc rank. Phần này phục vụ DT18-NV2/NV3 và bước1 của cô; chưa chọn P6 hoặc xác nhận lợi ích RCA.

Coverage toàn cây là bookkeeping, không là toàn semantics. Revision ứng dụng→image→instrumentation→deployment→RE2, body PDF lịch sử, dynamic override/binding/runtime đều còn OPEN. Các chuỗi nguồn/match/mismatch không chịu R1 được dùng lại sau kiểm hash, xem các đường dẫn gốc ở trên. Không chạy lại RCA, mở raw/test/heldout/archive hoặc tải nguồn.
