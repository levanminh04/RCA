# T-039 — Xét lại khả thi sau khi có nguồn, 16/10/2026

**Đã thu xong đúng danh sách Minh duyệt. Giữ toàn phạm vi T-039 và pin T-036. Chưa đủ căn cứ cam kết hoàn thành toàn SPEC trong một phiên.** Chưa lập bản ghi/mapping, dựng/đối chiếu hoặc nhận inventory đầy đủ. Các điểm dưới đây là bằng chứng từ nguồn để đánh giá lượng việc, không là kết luận nguyên nhân chênh lệch dataset.

## Quyền và đầu vào hiện hành

Minh trả lời nguyên văn: “Duyệt đúng danh sách”; “Giữ toàn phạm vi T-039 để xem lại khả thi sau khi có nguồn”; “Giữ pin, ghi rõ chứng cứ tại T-039”. Lưu ở authorization-20261016.json và LOG Phiên 2. Không tự tách task, sửa SPEC hoặc sửa registry chung.

`runs/thu-nguon-001/acquisition.json`: 223 file nguồn và sáu response metadata; payload thực **37.524.834 byte**, bằng đề xuất. Trong đó source file **37.102.637 byte**. Toàn file khớp byte/Git blob; SHA256 được lưu theo file. Lượt thu hết **37,985 giây**, là wall time của lượt thực, không phải benchmark độc quyền. Peak RAM lượt thu chưa đo, không bịa lại. Không có lỗi tải, retry hoặc raw telemetry đã lấy.

Kiểm độc lập sau thu tại `runs/khao-sat-nguon-001/integrity.json`: **229/229** nguồn/metadata khớp. Tree đề xuất vẫn là 274 entry, 219 blob; lấy 215, loại đúng bốn log thô. Không tải dependency, image hoặc upstream khác. Registry task `nguon.json` giữ bằng chứng commit→tree mới; không đổi byte/pin T-036. Revision ứng dụng→dataset/image/deployment vẫn OPEN.

## Điều nguồn thật cho thấy phải phân xử

Các đường dẫn ngắn dưới đây thuộc `sources/augmented-ob-94a01ba4/`. Parent đã đọc trực tiếp các đoạn chính bên dưới; hai nhánh hỗ trợ chỉ đọc đã kiểm hash trước dùng. Đây không là phản biện chính thức.

| Quan sát FACT trong snapshot ứng viên | Bằng chứng | Công việc không được rút gọn và giới hạn |
|---|---|---|
| Hai script chọn biến thể MySQL/Redis khác nhau, có hoặc không exporter | `kubernetes-manifests/start_demo_with_istio.sh:3–4`, `start_with_istio_exporter.sh:3–4`; các YAML mysql/redis tương ứng | Phải giữ điều kiện deployment; không hợp tất cả YAML thành một runtime. Có 30 declaration nhưng 26 khóa kind+name riêng, theo declarations.json; đây chưa là inventory cuối |
| adservice truy cập MySQL, ngoài RPC | `src/adservice/src/main/java/hipstershop/AdService.java:227–279`; SQL ở `hack/init_mysql.sql` | Giữ DB logic/instance/owner và nhánh truy vấn/fallback, không áp kiến trúc upstream Google thay code này |
| Cart chọn Redis hoặc LocalCartStore theo cấu hình | `src/cartservice/src/Startup.cs:32–46`, `services/CartService.cs:34–48`; health→Ping trong `HealthCheckService.cs:33–38` | Dependency injection, startup/health và nghiệp vụ có điều kiện khác nhau; package instrumentation chưa chứng minh span thực được tạo |
| Generated không hoàn toàn đồng nhất với proto chung | `pb/demo.proto:208–210,227–228`; recommendation `demo_pb2_grpc.py:475–489` có AdsService; email `demo_pb2_grpc.py:444–452` có CreateOrder | Phải phân biệt khai báo, binding và đăng ký handler thật. Không bỏ generated, không biến binding không đăng ký thành service đang phục vụ |
| Tên thao tác không thể lấy đơn thuần từ RPC | AdService.java `:120–123,172–175,194–197,228–231` đổi tên Span.current(); checkout `main.go` tạo span nội bộ; frontend `main.go:209–212` bọc HTTP handler | Cần lần caller/callee và instrumentation theo owner. Chưa có mapping operation đã xác minh hoặc kết luận telemetry mất thông tin |
| Context và nhánh lỗi ảnh hưởng đường quan sát | Checkout `main.go` trong convertCurrency dùng context.TODO; các handler trả sớm khi lỗi. Email `email_server.py:161–185` chọn dummy | Phải giữ khả năng nhánh và kiểm các match/mismatch tương ứng. Chưa nối revision dataset thì chưa nhận là nguyên nhân ca Nezha cụ thể |
| Có NodeName ở code và spec.nodeName ở YAML | Checkout `main.go:69–94`; adservice.yaml `:56–59`, shippingservice.yaml `:52–55` | Xác nhận nguồn env của deployment ứng viên; chưa nối qua collector/export tới cột Node của dataset. Không xác nhận host hoặc gán metric Node* |
| Build/image vẫn thiếu chuỗi nối dataset | `hack/make-docker-images.sh:24–39`, `make-release-artifacts.sh:63–85`; image tag ở YAML; Dockerfile checkout còn COPY log.csv | Phải truy tác động source ngoài/phiên bản, không lấy tag làm digest. Không cần build image trong task; không mở log bị loại để khép coverage |

Code tám Nezha bổ sung đã được đọc ngữ nghĩa: INSTALL/STATUS hướng dẫn artifact và cách chạy, log.py cấu hình logger, log_parsing.py phân pod/service, pattern_miner.py nhận event graph. Không thấy producer Source/Target/Weight hoặc Node trong **tám file này**; không suy từ đó rằng mọi nguồn khác đều không có. Code analysis T-008 đã đọc cũng là consumer CSV, chưa nối pipeline export. Cần code tạo metadata/export schema hoặc nguồn tác giả; owner tác giả Nezha, Minh quyết nguồn được đọc. Độc lập nguồn phụ và nghĩa host vẫn OPEN; không mở Weight/Node values để bù.

JAR được kiểm ZIP directory/manifest, không chạy/giải nén ra đĩa: Java agent có 14.650 entry, tổng giải nén 60.714.062 byte, entry lớn nhất 2.714.596 byte; manifest ghi OpenTelemetry Java agent 1.5.3. Wrapper có 54 entry. Bằng chứng ở `runs/khao-sat-nguon-001/jar-metadata.json`. Đây là metadata binary đã ghim, không xác nhận agent nào đã chạy trong dataset.

## Khối lượng và phần còn thiếu

`source-profile.json` đo **36.920 dòng UTF-8, 1.415.067 byte văn bản, 20 file binary** trong 223 file nguồn đã lấy. Đếm gồm generated/lock/asset; không coi từng dòng đều cần cùng độ sâu hoặc đọc UTF-8 là đã khảo sát ngữ nghĩa. Profile ghi rõ từng file chỉ decoded-for-size hay binary identity; không gắn cờ coverage đạt từ phép đếm này.

Phạm vi đọc hỗ trợ: một nhánh đọc ngữ nghĩa 34 văn bản trong docs/hack/kubernetes/pb/Nezha; ba PNG docs chỉ hash. Nhánh backend kiểm 78 file thuộc sáu service, đọc code/config/build chính, scan generated/lock/wrapper có mục đích; file test code chỉ hash. Root đọc checkout main, frontend main/rpc, loadgenerator, Dockerfile/genproto và các đoạn product/shipping/handler để lần câu hỏi. Các lượt scan, đếm/hash hoặc xem trích đoạn không được nâng thành coverage semantic toàn file. Chưa hoàn tất đối chiếu mọi entry/loại trừ với inventory và quan hệ.

**Đánh giá sau nguồn:** các rút gọn “cây + proto”, “mọi YAML là một deployment”, “generated là bản sao” đều bị phản ví dụ nguồn bác bỏ. Vì vậy chưa có căn cứ hạ dự toán cũ xuống một phiên bằng các rút gọn ấy. Bản ghi, alias/owner, oracle, xử lý nhánh và generated, đối chiếu toàn 132 graph, phân tích nhóm cùng match và bàn giao còn phải làm đầy đủ. Không tự quyết đây là bất khả thi; kết luận hiện tại là **chưa chứng minh khả thi một phiên**.

Phần còn lại CANDIDATE **6–10,5 giờ công, chưa đo**: coverage/nguồn gián tiếp còn lại 1–2 giờ; bản ghi/mapping 2–3; oracle/dựng/đối chiếu 0,5–1; phân tích nhóm 1,5–3; tự kiểm/bàn giao 1–1,5. Chưa gồm phản biện/chờ nguồn tác giả. Ước lượng dựa trên các phụ thuộc vừa thấy, không phải thời gian máy hoặc giới hạn cắt nhiệm vụ.

Máy: đã biết source input và graph hiện hành nhỏ; vẫn chưa có pilot có bản ghi hợp lệ để đo toàn pipeline T-039. Dự toán RAM/giờ máy/tổng mọi lượt trong de-xuat-tai.json còn CANDIDATE. Mới dùng một lượt thu; giữ đủ run và intermediate, JAR chưa giải nén ra đĩa. Không đo chi phí cùng việc nặng khác hoặc dừng tiến trình phiên khác. Chưa tự cấp quyền lượt >1 giờ.

## Điều cần Minh quyết sau lựa chọn giữ nguyên task

Không sửa SPEC hoặc tự tạo task nhận phần còn lại. Nếu tiếp tục giữ toàn T-039 mà thực hiện qua nhiều phiên, cần Minh **duyệt rõ ngoại lệ một phiên**; câu “giữ toàn phạm vi để xem lại khả thi sau khi có nguồn” chưa là ngoại lệ này. Nếu Minh chọn tách sau bằng chứng mới, impact map trong de-xuat-tach.md vẫn chỉ là đề xuất, phải trình SPEC cụ thể trước ghi. Cả hai cách đều giữ toàn nghĩa vụ nghiên cứu; không yêu cầu giảm phân tích hoặc bỏ nhóm.

AGENTS §5 quy định: “Một task là một phần việc có đầu ra rõ, làm xong trong một phiên.” Lời giao cũng yêu cầu chưa đủ căn cứ thì trình cách tách và ảnh hưởng, không tự chia hoặc giảm độ sâu. Đây là lý do dừng phần dựng/đối chiếu phụ thuộc để Minh quyết; không phải thiếu quyền tải nữa.

Ba lựa chọn Minh đã trả lời được lưu nguyên văn trong LOG/authorization. Nội dung đề nghị lưu DECISIONS riêng ở `de-nghi-ghi-quyet-dinh.md`; chưa ghi file chung. Chưa đóng T-039/P5b/RQ3/RQ5/G3, chưa có số khớp cấu trúc hoặc bằng chứng lợi ích RCA.
