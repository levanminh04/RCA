# Lineage nguồn Online Boutique / Nezha — T-039

Đây là khảo sát nguồn phục vụ tích hợp của người làm, không phải phản biện chính thức. Hash đầu vào được kiểm theo checkpoint `results/T-039/manifest.json`, acquisition và manifest nguồn T-008. Chi tiết hashes, phạm vi scan và bằng chứng ở `backend-source-audit.json`. Không mở dataset/nhãn/giá trị chuỗi, không tải thêm, không chạy ứng dụng hoặc bộ dựng.

## 1. Liên hệ dự án chưa là build lineage

README Augmented-OB:3–6 nêu việc thêm OpenTelemetry, TraceID/SpanID và liên hệ nghiên cứu Nezha. README Nezha đã lưu:86–95 nêu họ dữ liệu Online Boutique. Đây là liên hệ mức dự án/bài báo. Metadata `sources/metadata/ob-commits.json` định danh snapshot ứng dụng, commit ngày 17/08/2023; `nezha-commit.json` định danh commit Nezha ngày 20/05/2025. Revision code, tree, image, deployment và collection revision là các đối tượng khác nhau. Ngày commit về sau không tự chứng minh hay bác bỏ ancestry nội dung đã chạy trước đó.

YAML dùng image tag và `imagePullPolicy: Always`; trong scope đã đọc chưa có digest/build manifest liên hệ dataset. Snapshot ghim hợp lệ là nguồn capability có điều kiện, chưa xác nhận snapshot sinh dataset. Giữ OPEN; owner là tác giả nguồn/triển khai, Minh quyết yêu cầu đúng digest/build/effective manifest/collection version.

## 2. Logical database → configured mysql endpoint

Chuỗi `addatabase`: `src/adservice/src/main/java/hipstershop/AdService.java:237–257` ghép JDBC URL bằng MYSQL_ADDR và tên DB addatabase, đọc aditems; `kubernetes-manifests/adservice.yaml:42–43` đặt mysql:3306; `mysql.yaml:1–11` khai Service mysql ở namespace hipster/port3306/selector app=mysql; deployment tương ứng ở14–35.

Chuỗi `Productdb`: `src/productcatalogservice/server.go:188–203` ghép DSN MYSQL_ADDR và /Productdb; `productcatalogservice.yaml:46–47` dùng cùng mysql:3306. Các chuỗi này đủ ghi logical DB→configured endpoint binding có điều kiện đúng manifest. Không gộp DB logic với instance hoặc suy physical host. Provenance nên có code URL/DSN, YAML MYSQL_ADDR và Service, không chỉ script SQL.

`hack/init_mysql.sql:1–15,91–129` khai database/table nhưng script tồn tại không chứng minh đã chạy. YAML dùng hostPath/image; actual initialization, image digest và process/placement của môi trường dataset còn OPEN. Source binding không là xác nhận triển khai runtime.

## 3. Exporter và collector là các chặng khác nhau

`mysql_exporter.yaml:49–55` khai sidecar mysqld-exporter, image và DATA_SOURCE_NAME tới 127.0.0.1:3306; Service expose 9104 tại9–16. Đây là capability cấu hình đọc instance mysql ở exporter variant, chưa xác minh implementation/query/series đã chạy. `redis_exporter.yaml:53–56,78–80` có image/port 9121, chưa khai Redis target; không dùng default dependency chưa đọc để suy cạnh target. `start_with_istio_exporter.sh:3–4` chọn manifests exporter, script mặc định `start_demo_with_istio.sh:3–4` chọn manifests khác. Không nhận mọi variant cùng hoạt động.

Ad dùng OTEL_EXPORTER_OTLP_ENDPOINT và OTEL_SERVICE_NAME (`adservice.yaml:48–51`); cart dùng OTEL_EXPORTER_OTLP_ENDPOINT và SERVICE_NAME (`cartservice.yaml:48–51`, Startup.cs:58–65). JS/Python dùng COLLECTOR_ADDR/SERVICE_NAME. Signal address phải giữ đúng biến. Endpoint OTLP của ứng dụng chưa cho receiver/processor/exporter config tạo CSV. Không biến exporter→DB, app→collector và series dataset thành một lineage đã xác nhận chỉ vì tên giống.

## 4. Producer Source/Target/Node chưa tìm ở đúng scope

Đã đọc các đường consumer/producer liên quan và scan toàn AST/literal bảy Python file ghim: T-008 `data_integrate.py`, `alarm.py`, `main.py`, `pattern_ranker.py`; supplement `log.py`, `log_parsing.py`, `pattern_miner.py`. Không thấy literal Source/Target/Node/NodeName, collector/exporter hoặc writer tạo daily relation/Node metadata trong đúng scope ấy. `data_integrate.py:483–488` đọc trace/log CSV; 426–466 tạo EventGraph từ sự kiện/parent span; 535–551 tính support và trả object. Writer tại `alarm.py:66–81` ghi threshold, không phải producer daily Source–Target.

Đây không chứng minh producer vắng ở toàn repository, image hay hệ thu. Tree metadata giúp định danh source paths, không thay đọc body/nguồn ngoài chưa có. Các giải thích còn cạnh tranh: metadata suy từ cùng trace/span; từ service mesh/collector khác; từ cấu hình triển khai; hoặc một pipeline/revision chưa có trong audited scope. Chưa phân xử thì không dùng metadata như đối chứng độc lập độ phủ trace. Cần producer code/config, input schema, revision và time/aggregation policy. Owner: tác giả Nezha/collector, Minh quyết nguồn bổ sung.

## 5. NodeName source chưa chứng minh cột Node là host

YAML lấy NODE_NAME từ spec.nodeName; ad/JS/cart đặt NodeName vào tag/attribute, Python vào Resource. Đây là nghĩa trường nguồn trong manifest ứng viên. Consumer Nezha đọc PodName/OperationName/SpanID/ParentID (`data_integrate.py:239–263,483–488`), chưa cho transform sang dataset Node nào, namespace nào và hiệu lực thời gian nào. Node dataset giữ OPEN; không tạo host hoặc metric-host binding từ tên. P9 cần exporter field mapping, service/pod/instance/host identity và validity interval.

## 6. Metric không tự độc lập

`alarm.py:84–148` tính NetworkP90 từ trace parent/pod span, 276–279 đưa vào metric list. Đây là FACT về consumer code, chưa xác minh mọi metric file đã qua đường này. Nó đủ bác suy luận chung rằng tên network metric luôn đến sensor độc lập. Exporter mysql/Redis trong source cũng chưa xác nhận series/schema của dataset. Phần này ảnh hưởng P6 khi chọn tín hiệu, P9 khi phân biệt quan sát đã ghi với điều collector mới có thể ghi.

## 7. Thao tác và giới hạn thư viện

Recommendation actual outgoing ListProducts tại server:71, channel/stub:99–105 đã có trong backend. Email main cố định dummy; cloud-mail constructor và non-dummy start raise nên không thêm active external-mail edge. Client/example được bảo toàn trong backend-coverage.source_examples, không là server process ownership. Watch trong class email/recommendation là source-declared candidate; Health binding của dependency chưa đọc nên chưa kết luận active hoặc absent.

JAR được xem ZIP manifest/mục lục class, không phân tích hết bytecode/agent filter/final span name hoặc chạy. External dependency code/image chưa tải. Generated Python đã scan descriptor/URI/registration và có mismatch proto, chưa là đọc mọi serializer field hoặc runtime library semantics. Không gọi đây complete instrumentation coverage. Input/owner/chi phí và quyết định P6/P9 phụ thuộc ở `backend-source-audit.json#/open_items`. Nguồn ngoài cần đề xuất đúng file/revision/dung lượng riêng; báo cáo không cho quyền tải, chạy thực nghiệm hoặc mở test.
