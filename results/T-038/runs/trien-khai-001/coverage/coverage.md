# Bao phủ nguồn T-038 — nhánh hỗ trợ người làm

Đã phân hoạch toàn Git tree được duyệt: 3.921 mục, gồm 1.094 thư mục và 2.827 blob. Đây là kiểm bao phủ nguồn và độ sâu đã đọc; chưa là khẳng định inventory/quan hệ ngữ nghĩa đầy đủ. Revision ứng dụng sinh RE2-TT còn OPEN.

Nguồn số: `coverage-final.json#/statuses`, `/groups`, `/files`, `/directories`; plan được ghim trong `plan_sha256`; hash nguồn ở acquisition manifest và registry riêng. Không tải thêm nguồn, chạy ứng dụng, giải nén archive ra đĩa hoặc đọc dữ liệu khóa.

## Phân hoạch hiện hành

| Nhóm | read | excluded | open |
|---|---:|---:|---:|
| application-java | 401 | 0 | 0 |
| application-nonjava | 26 | 0 | 1 |
| application-resources-and-build | 156 | 0 | 5 |
| application-tests | 79 | 0 | 1 |
| deployment | 69 | 0 | 1 |
| historical-documentation | 191 | 17 | 4 |
| root-build-and-project | 20 | 0 | 0 |
| root-images | 12 | 1 | 13 |
| ui-dashboard | 112 | 0 | 25 |
| vendored-node-dependencies | 1692 | 0 | 1 |

`read` phải đọc cùng `read_depth`: decode/index toàn văn khác phân xử thủ công; archive Office XML khác đọc hình/mũi tên; Git symlink literal khác chạy target. Không tự loại theo đuôi. Không có mục not-retrieved sau khi tải xong. 17 mục lịch sử trong lượt sạch không mở lại, chỉ acquisition metadata; đây là 15 text telemetry mẫu, một ảnh phụ thuộc mẫu và workbook kết quả nghiên cứu.

## Nội dung đã lần nguồn

- Entry point ngoài Java: Flask/gunicorn avatar, Web.go news, Express ticket-office, Tornado voucher, Nginx UI. `facts.json` giữ handler, điều kiện HTTP, MySQL và env override. Khối Mongo của Go bị comment; không là cạnh hiện hành. Ticket-office đọc PORT env nhưng không truyền vào createConnection.
- Root README → Makefile → hack/deploy → quickstart charts/templates. Nacos/MySQL/RabbitMQ ở quickstart; tracing tùy chọn là Skywalking/Elasticsearch; monitoring tùy chọn là Prometheus/Grafana và các exporter/alert components. Profile Jaeger/EFK/Istio/PVC và root Docker Compose giữ riêng, không hợp thành một deployment.
- Hai template app có 46 Deployment; svc.yaml có 44 Kubernetes Service. Thiếu Service riêng của food-delivery và wait-order không chứng minh hai ứng dụng không tồn tại. Generator chưa chạy; các điều kiện script và namespace giữ OPEN.
- RabbitMQ chain giữ release → chart ConfigMap rabbitmq_host → envFrom từng deployment → spring.rabbitmq.host. Broker logical `rabbitmq:quickstart`, scope null; localhost default từng module không bị gộp thành một instance. Queue/email/food_delivery và vai trò khai báo được giữ với source locator; không tự nhận exchange/binding/message instance.
- Notification có JavaMailSender và cấu hình SMTP external. SMTP không có channel thích hợp trong T036 hiện hành: giữ external/address trong inventory, relation phản ví dụ ngoài graph, không ép thành HTTP/RPC.
- 11 sơ đồ API dưới image/train-ticket-draws-* đã xem trực tiếp; một số dùng ticketinfo/food-map và tên cũ khác v1.0.0. Không lấy tên tài liệu thay code. Root xem image/2.png; phạm vi quan sát được ghi rõ observer.

## Phần chưa phân xử và hệ quả

- Archive `myproject.zip` chỉ liệt kê 22 entry trong bộ nhớ: hai bộ artifact monitoring core/Zipkin với JAR lồng. Không đọc nội dung JAR lồng, không suy bằng hash nguồn unpacked. Năm wrapper JAR chỉ kiểm namespace/member Maven; chưa đọc bytecode. Office DOCX/PPTX đọc XML text; ảnh/quan hệ đồ họa nhúng chưa render. PDF, font, asset UI, swap/cache binary còn ghi đúng độ sâu trong bảng từng file. Chưa có cơ sở tuyên bố mọi binary không ảnh hưởng.
- Nguồn ngoài được dẫn cụ thể ở `external-references.json` và `facts.json#/external_sources`: image/base image chưa có digest, Maven/Go/Python/npm dependencies, Wiki build guide và workload repo. Chưa tải hoặc thực thi. Tree không có gitlink và không tìm thấy LFS pointer trong content index sạch; không biến điều đó thành chứng minh image đầy đủ.
- Ticket-office khai mysql ^2.18.1 nhưng cây vendor không có node_modules/mysql; Dockerfile copy vendor và npm install bị comment. Đây là lệch khai báo/cây nguồn; chưa chạy source hoặc kiểm base image, nên runtime dependency còn OPEN.
- Chưa xác minh app/image/instrumentation/deployment sinh RE2-TT. Đầu ra chỉ hỗ trợ inventory/đối chiếu nguồn có điều kiện, không quy mismatch cho telemetry, không chứng minh lợi ích RCA hoặc mở test.

## Sự cố và kiểm

Lượt screening đầu đã decode nhầm 15 text telemetry mẫu công khai trong old-docs và XML workbook kết quả nghiên cứu. Khi phân loại tài liệu, image/jaeger.png hiện ra là screenshot trace UI; không lấy dữ liệu ảnh vào facts/model. Đã báo root ngay để báo Minh. `incident.json` ghi path/thao tác/output/ảnh hưởng, không sao nội dung mẫu. Giữ các output lỗi `coverage.json`, `content-index.json`, `archive-structures.json`; không dùng chúng để lập model. Index sạch có tên riêng, không mở lại nhóm mẫu; facts/part chỉ đọc source runtime/config/deployment với hash trước đọc. Không được tuyên bố cả phiên chưa đọc telemetry thô.

`verification.json` kiểm đủ 3.921 entry, không lặp path, index sạch loại toàn nhóm mẫu và part-schema build ghim đạt. Các lỗi chọn locator đã ghi, rồi lấy chính xác metadata.name từ YAML; part hiện hành trỏ đúng Skywalking L38–49. Không commit/push.

## Bàn giao

- Root dùng `part-document.json`, `part-registry.json` và `part-validation.json` để merge; endpoint references cần dedup role/provenance với nhánh Java.
- `facts.json` giữ chuỗi broker, nguồn ngoài, 617 tài nguyên K8s theo profile, giới hạn/SMTP và điều kiện; không coi mọi ConfigMap là node RCA.
- `coverage-final.json` là bảng từng path hiện hành. Chưa có quyền/nguồn để xác nhận binary/ảnh nhúng hoặc dependency ngoài; ảnh hưởng tuyên bố đầy đủ và lời giải thích mismatch. Root giữ nghĩa vụ này trong báo cáo/bàn giao, trình đúng nguồn/phép kiểm bổ sung nếu cần.
