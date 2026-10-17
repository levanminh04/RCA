# Kết quả hiện hành T-039 theo SMTP V2

Đã replay132/132graph dưới snapshot R1 và comparator V2; mỗi kết quả mới bằng nguyên kết quả cũ, gồm sets/members/exclusions/mẫu số/interval. Model và mapping giữ nguyên; lặp/đảo/input bất biến đạt. Nguồn số và output hiện hành ở runs/doi-chieu-smtp-001/checks/full132-001/summary.json, diff.json và pin.json. Phân tích nguồn dưới đây được giữ, số không đổi do bằng nhau toàn artifact; các đường dẫn run004 là bằng chứng lịch sử, đầu ra mới theo summary hiện hành. Inventory toàn deployment/runtime/Node/alias vẫn OPEN, chưa nghiệm thu/P6/G3.

# Phân tích chênh lệch nguồn và graph T-039

Đã đối chiếu đủ 132 graph Nezha-OB dev đã lưu. Đây là **đối chiếu tham khảo có điều kiện**: chưa xác minh snapshot ứng dụng/build/image/deployment đã sinh dataset. Không gọi graph tĩnh là sự thật runtime. Phần nguồn toàn deployment đạt một phần; phần dựng/so sánh và kiểm trong miền giao đã triển khai.

Bằng chứng máy đọc: `runs/phan-tich-002/source-to-difference.json`. `/cells` giữ từng graph/cửa sổ/interval/mẫu số; `/chains` giữ 93 khóa của hai mức, source record/provenance, member gốc và mọi cửa sổ khớp/chênh; `/excluded_edge_groups` giữ 53 nhóm raw edge bị loại, mapping từng đầu và vị trí trong mọi graph. `/groups` nối các khóa quan trọng với trường hợp khớp và giải thích cạnh tranh. Đây là số nhóm biểu diễn, không là tỷ lệ nguyên nhân. Từng graph đầy đủ nằm ở đường dẫn `output` trong mỗi cell.

| Mức | Cửa sổ | Số graph | Cạnh trace gốc | Đủ điều kiện so đầu mút | Bị loại bởi mapping |
|---|---|---:|---:|---:|---:|
| entity | A | 2 | 11 | 11 | 0 |
| entity | A | 20 | 13 | 13 | 0 |
| entity | N | 22 | 13 | 13 | 0 |
| entity | full | 22 | 13 | 13 | 0 |
| operation | A | 2 | 52 | 10 | 42 |
| operation | A | 1 | 62 | 9 | 53 |
| operation | A | 19 | 63 | 10 | 53 |
| operation | N | 22 | 63 | 10 | 53 |
| operation | full | 22 | 63 | 10 | 53 |

Nguồn số: `/cells`. Phép so đầu mút (endpoints) bỏ kiểu; phép so có kiểu (typed) giữ kiểu và loại unknown. Ở cả 132 graph, mẫu số trace của typed bằng0 nên tỷ lệ phía trace là null/N/A. Đây là chưa đủ điều kiện xác minh kiểu, không phải chứng cứ cạnh trace sai kiểu.

## G1. Lời gọi giữa service và phần vắng theo cửa sổ

**Quan sát:** 64/66 graph entity có 13 khóa trace đủ điều kiện và cả13 đều có trong22 khóa tĩnh; hai cửa sổ A còn11. Hai ca opaque `dev-55f99f3e0a` và `dev-b0f8b2e3ac` thiếu checkout→email/payment trong A nhưng có trong N/full của chính ca ấy. checkout→currency là static-only ở cả66 graph. Xem `/cells` và `/groups/0/mismatch_keys`, `matched_counterparts` trỏ `/chains/*/id`.

**Chuỗi nguồn và đối chiếu:** checkout/main.go:178–239 có luồng chuẩn bị/charge/ship/empty/email; 453–473 có lời gọi Convert. Bản ghi `go:co:rpc:CurrencyService/Convert` giữ cạnh tĩnh với điều kiện, dựng thành khóa checkout→currency và không tìm trong T. Các cạnh checkout→cart/shipping/productcatalog có code/config cùng owner và khớp làm đối chiếu. Convert tạo span có ctx nhưng RPC tại471 dùng `context.TODO()`. Đây là khác biệt nguồn có thể làm mất ngữ cảnh truyền sang lời gọi so với việc dùng ctx; chưa chứng minh code này đã chạy hoặc đây là nguyên nhân duy nhất của cạnh thiếu trong dataset.

**Phân xử:** chênh A với N/full được xác nhận ở tập đã lưu; identity entity có nguồn và chuyển đổi T039 không làm rơi khóa. Nhánh request/lỗi, sampling/telemetry, revision/deployment và xử lý trước T035 vẫn chưa phân xử. N/full có cạnh không chứng minh A đã thực thi cùng nhánh. Cần liên kết source→image→deploy→export cùng quan sát lời gọi/ngữ cảnh trong quyền riêng trước quy nguyên nhân vật lý.

## G2. Phụ thuộc dữ liệu khác cạnh giữa service

**Quan sát:** ad→mysql/addatabase, productcatalog→mysql/Productdb và cart→redis-cart chỉ có phía tĩnh ở entity. Source có URL/DSN/Redis calls, nhưng graph thao tác giữ SQL span thuộc owner ứng dụng. Ba tên `SELECT addatabase.aditems`, `sql.conn.query`, `sql.rows` chưa có candidate mapping được chứng minh; không biến SQL span thành DB entity. Chuỗi đầy đủ ở `/groups/1` và `/excluded_edge_groups`.

**Chuỗi:** AdService.java:237–257 → record `backend:ad-mysql-read` → operation createAdsMap→DB logic → chiếu ad→DB; server.go:188–214/238–298 → DSN/query → records Productdb → productcatalog→DB. MYSQL_ADDR và mysql Service nối hai DB logic với một instance cấu hình, không thành hai host. Cart Startup chọn Redis khi REDIS_ADDR có giá trị, ngược lại LocalCartStore; RedisCartStore giữ calls/health/startup. Script SQL tồn tại chưa chứng minh đã provision. Chi tiết DB binding/source locator ở `runs/doc-nguon-002/lineage.md`.

**Đối chiếu khớp:** frontend→productcatalog và frontend→cart vẫn khớp entity; ParseCatalog→ReadCatalog khớp thao tác với literal span rõ. Như vậy không có căn cứ gọi mọi data static-only là lỗi telemetry chung. Nguồn chứng minh khả năng phụ thuộc dữ liệu, còn graph hiện hành chưa cung cấp định danh thành phần DB/cache độc lập qua mapping này. Revision, nhánh, source thư viện, thuộc tính đầu vào adapter và export vẫn OPEN. P9 cần DB/cache attributes, namespace endpoint và logical DB→instance→host có hiệu lực thời gian; collector không khôi phục dữ liệu chưa từng ghi.

## G3. Hàm và span không có cùng ranh giới

**Quan sát:** AdImpl/getAds có `@WithSpan` và literal updateName nên map vào canonical GetAds. Hai cạnh canonical GetAds→getAdsByCategory/getRandomAds khớp trong phần đủ điều kiện. Các cạnh helper→createAdsMap và createAdsMap→DB là static-only. Không có node createAdsMap trong union operation đã giao; vẫn giữ operation nguồn vì đây là khảo sát capability, không giới hạn inventory theo observed nodes.

**Cơ chế trong nguồn:** AdService.java:169–173 và190–197 gọi createAdsMap trước khi đổi tên current span sang category/random. createAdsMap:227–231 không có @WithSpan và chỉ `Span.current().updateName(...)`, không tạo span riêng. Với hành vi đúng như nguồn và instrumentation này, tên tạm createAdsMap có thể bị lần updateName sau ghi đè. Vì vậy call graph hàm có helper riêng không bắt buộc tạo span-parent helper riêng, ngay cả khi không mất telemetry. Raw trace giữ category/random→SQL; những cạnh ấy bị loại do SQL mapping, không được lén nhận thành match DB.

**Phân xử:** nguồn chỉ ra bước thay đổi thông tin tên; graph đã lưu có mẫu hình tương thích và trường hợp GetAds→category/random khớp. Chưa nối agent/build/deploy nên đây là ứng viên giải thích dataset, chưa xác nhận nguyên nhân dataset. Nhánh, nguồn thư viện/agent, revision và export còn mở. Không dùng một đặc tính chung của thuật toán để quy cho mọi ca sai. P6 cần xác định mức thao tác phù hợp với tín hiệu thực ghi, không coi mỗi hàm là một span.

## G4. Mapping có nguồn và mẫu số sau loại trừ

**Quan sát:** union55 operation có20 literal verified,32 candidate chưa verified và3 SQL chưa có candidate. Phần lớn graph có63 raw edge nhưng chỉ10 đủ điều kiện endpoints; hai A có52 raw edge và10 đủ điều kiện; một A có62 raw edge và9 đủ điều kiện. Tất cả vẫn có output, members và exclusions. Tỷ lệ giao/T=1 chỉ trên phần đủ điều kiện, không là “trace phủ đủ100%”.

**Chuỗi:** recommendation_server.py:63–84/98–105 và demo_pb2_grpc.py:143–158 chứng minh local client ListProducts thuộc recommendationservice gọi productcatalogservice. Bản ghi đã thêm đúng local owner; generated RPC path chưa xác minh tên span thư viện nên candidate slash-prefix vẫn unverified. Tương tự sáu candidate slash/grpc-prefix có bảng thủ công theo scope/owner, không tự strip prefix. Những tên RPC trùng chữ nhưng không có literal span cũng chưa verified. So sánh loại edge ngay tại đầu mapping không đủ chứng cứ; không phải edge đã vắng khỏi dữ liệu.

**Đối chiếu:** shipping CreateQuoteFromCount→CreateQuoteFromFloat tại main.go:285–301 và checkout Prepare...→GetUserCart có literal và khớp. Ad handler literal được map riêng, không gộp cả span GetAds chưa verified với AdImpl. Oracle owner conflict đã kiểm từ chối nhầm chủ. Không tạo SQL fake operation để tăng khớp. Muốn nâng candidate cần exact library/version được build, naming path/filter và runtime link; generated URI một mình chưa đủ. Revision và alias ngoài literal vẫn OPEN, conversion T039 đã kiểm độc lập.

## G5. Phạm vi browser, tải và exporter

**Quan sát:** loadgenerator→frontend, web-client→frontend và hai stylesheet browser→stackpath/fonts.googleapis chỉ có phía tĩnh. mysqld-exporter→mysql thuộc variant exporter. gstatic chỉ là preconnect hint, giữ trong inventory nhưng đã loại cạnh HTTP suy sai lúc tự rà. Nguồn và key/members ở `/groups/4`.

**Chuỗi:** locustfile.py task/request → sáu record hợp vào một khóa loadgen→frontend; header.html:26–30 → hai request stylesheet từ browser, không là frontend server egress; mysql_exporter.yaml:38–55 → DATA_SOURCE_NAME loopback → record data exporter→mysql. start_with_istio_exporter và start_demo_with_istio:3–4 chọn variant khác nhau, không nhận chúng cùng chạy. Script/template/code nguồn đủ giữ khả năng với điều kiện; chưa xác nhận profile tải/browser/variant thực dùng.

**Đối chiếu:** frontend→ad/shipping là RPC app khớp trong cùng tập graph nhưng khác scope quan sát. Vì vậy static-only của browser/exporter không tự là collector thiếu RPC nội bộ. Revision, nhánh/browser fetch, deployment, collector scope và nguồn ngoài còn mở. Redis exporter chưa khai target trong config đã đọc nên không suy target từ default thư viện. Những gì thiếu đã nêu đúng input/owner ở bàn giao; không bỏ inventory vì source ngoài miền trace.

## G6. Một cạnh thao tác chỉ vắng ở một ô A

**Quan sát:** `dev-27252dca60/operation/A` có9 khóa đủ điều kiện; PrepOrderItems→ConvertCurrency vắng tại đây, có trong N/full cùng ca và các graph còn lại. Cạnh PrepareOrderItemsAndShippingQuoteFromCart→ConvertCurrency vẫn là trường hợp khớp có cùng đích. Xem `/groups/5`, `/chains/*/occurrences` và `/cells` theo opaque ID; không lấy trung bình che ô khác.

**Chuỗi nguồn:** checkout/main.go:432–446 gọi ConvertCurrency cho từng item sau GetProduct thành công;302–306 đổi phí ship theo nhánh chuẩn bị. Cùng source, owner, literal mapping và phép chuẩn hóa cho kết quả khác giữa cửa sổ vì input edge-set khác, không vì đổi policy theo kết quả.

**Phân xử:** xác nhận được khác miền cửa sổ. Không xác nhận request có item, nhánh lỗi, sampling hoặc lời gọi đã chạy. Mapping là literal đã kiểm; chuyển đổi T039 bảo toàn cạnh/interval. Cần source revision và request/span sequence đúng quyền để phân biệt nhánh chưa chạy với telemetry/adapter thiếu. Không suy lỗi gốc từ tên ca, N/A hoặc số cạnh.

## G7. Kiểu unknown, nguồn phụ và Node

Typed loại unknown nên không đo được agreement về kiểu; endpoints vẫn giữ những cặp đủ mapping, ví dụ frontend→productcatalog. Không điền kiểu từ kiến trúc để tạo kết quả đẹp. Đây là hành vi hợp đồng đã kiểm bằng oracle và toàn graph, không là phát hiện runtime sai kiểu.

Bảy file Python Nezha đã đọc đường consumer/producer liên quan và scan AST/literal chưa chỉ ra producer CSV Source/Target/Node trong scope ấy. data_integrate.py đọc CSV rồi dựng EventGraph/support; writer đã thấy ở alarm.py là threshold, không phải metadata phụ đó. NetworkP90 trong alarm.py được suy từ trace: tên metric không chứng minh sensor độc lập. Không khẳng định toàn Nezha/deployment không có producer. Chi tiết exact source/hash/locator và các giải thích khác ở `runs/doc-nguon-002/backend-source-audit.json` và `lineage.md`.

YAML lấy NODE_NAME từ spec.nodeName và app ghi NodeName, nhưng chưa có schema/transform chứng minh cột Node dataset mang đúng host ID ấy. Không tạo host node hoặc gắn host metric từ tên ổn định. Metadata ngày có thể từ cùng trace, mesh/collector khác, cấu hình hoặc pipeline/revision chưa có; chưa phân xử tính độc lập hay miền thời gian. P9 cần producer/config/version, identity service–pod–instance–host và validity interval. Quyền T039 không mở Weight/Node values/telemetry thô để lấp chỗ thiếu.

## Phần trả lời được và phần nhận tiếp

Nguồn→bản ghi→khóa→mapping→tập đã có chuỗi bằng chứng và phép kiểm; nguồn chức năng có thể khác cấu trúc span, và mẫu số sau mapping nhỏ hơn graph gốc là hai điều đã phân biệt cụ thể. Giữ DB logic khác instance, inventory khác observed nodes và tín hiệu khai báo khác các kênh độc lập đã đo. Graph thực sự được dùng trong phép chiếu, chuẩn hóa khóa và giao/hiệu tập; chưa dùng tính bất thường hoặc xếp hạng.

Chưa xác nhận inventory toàn deployment, nguyên nhân vật lý của cạnh thiếu, đầy đủ telemetry hoặc lợi ích RCA. T040 nhận mô hình tham chiếu và các OPEN; P6 cần chọn mức/tín hiệu/cơ chế bằng bằng chứng dev riêng; P9 nhận yêu cầu identity/địa chỉ/lineage. Nguồn cần bổ sung, owner, chi phí chưa đo và quyết định phụ thuộc nằm ở `de-xuat-bo-sung-nguon.md`, `ban-giao.md`. Đây là hoàn thành phần triển khai trong quyền để phản biện, không tự nghiệm thu toàn mục tiêu nguồn hoặc đóng RQ3/RQ5/P5/G3.
