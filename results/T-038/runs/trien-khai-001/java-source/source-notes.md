# Khảo sát Java nguồn Train Ticket v1.0.0

Đây là phần việc hỗ trợ người làm T-038. Không phải phản biện chính thức. Nguồn là snapshot tham khảo có điều kiện đã được Minh duyệt tải. Các nhận định dưới đây không xác nhận snapshot sinh RE2-TT, không xác nhận hệ đang chạy và không chọn P6.

## Phạm vi và đầu ra

`extract_java.py` đọc danh sách tệp từ đề xuất tải đã duyệt. Trước khi giải mã nội dung từng tệp, chương trình kiểm số byte và Git blob theo cây đã định danh. Bảng `verified-inputs.json` lưu thêm SHA256. Không chạy code ứng dụng, Maven hoặc test nguồn; không mở telemetry hoặc dữ liệu khóa.

`source-facts.json#/file_index` bao phủ mọi tệp Java trong cây: 635 tệp. Trong đó có 401 tệp main thuộc module Maven hiện hành, 103 tệp test nguồn và 131 tệp main lịch sử trong old-docs. 156 tệp Java dưới old-docs gồm cả main và test; không được cộng 156 vào 635 lần nữa. Tệp test nguồn ở đây là mã unit test của ứng dụng, không phải tập đánh giá RCA bị khóa.

Các số và mẫu số hiện hành nằm ở `source-facts.json#/summary`. Có 42 module được root pom khai báo; 41 module có lớp SpringBootApplication và một module dùng chung. Bản ghi nguồn giữ riêng handler HTTP, phương thức Java service/repository, HTTP callsite, lời gọi repository, listener/publisher, cấu hình và thao tác hỗ trợ. Chỉ mục phương thức Java dùng chữ ký nguồn, không tự chuyển thành tên span lúc chạy.

## Bằng chứng đã lần theo

- HTTP: `TravelServiceImpl.java` của ts-travel-service, dòng 51–53, trả `http://` cộng tên service. Dòng 346–351 lấy ts-basic-service và gọi POST `/api/v1/basicservice/basic/travels`. `TravelApplication.java` dòng 30–33 khai báo bean RestTemplate có LoadBalanced. Field DiscoveryClient được inject không tự là lời gọi discovery. Có một lời gọi thực `discoveryClient.getInstances("ts-auth-service")` ở `UserServiceImpl.java` dòng 86; bản ghi này được giữ riêng trong `support_calls`.
- Dữ liệu: `ConfigRepository.java` khai báo CrudRepository và ba phương thức tại dòng 11–35. Các callsite repository lưu biến, kiểu khai báo/import, phương thức gọi và caller Java. URL JDBC tại `ts-config-service/src/main/resources/application.yml` dòng 9 là bằng chứng cấu hình riêng. Không dùng tên phương thức repository làm tên truy vấn/span lúc chạy.
- Messaging: notification `RabbitReceive.java` dòng 51 khai báo listener theo `Queues.queueName`; `notification/config/Queues.java` dòng 10 định nghĩa email. food `RabbitSend.java` dòng 21 có lời gọi AmqpTemplate hai đối số; `foodsearch/config/Queues.java` dòng 10 định nghĩa food_delivery. Exchange/routing mặc định là diễn giải API phụ thuộc; source không tự chứng minh broker/binding lúc chạy hoặc bản tin được nhận. Không nối trực tiếp producer với consumer chỉ vì cùng literal.
- Nền và hỗ trợ: `support_calls` lưu MailService.sender.send, Travel.executorService.submit, User.discoveryClient.getInstances và WaitOrder.pollThread.start. `background` và `pattern_index` giữ thêm annotation, executor và mẫu từ khóa. ThreadPoolTaskExecutor được khai báo trong inside-payment; annotation Async không tự chứng minh một caller thật đi qua proxy. Quét token hiện hành không thấy các tên API FeignClient, WebClient, HttpClient, ManagedChannel, RedisTemplate hoặc MongoTemplate đã liệt kê; đây là kết quả quét các mẫu này, không phải chứng minh mọi cơ chế động/thư viện ngoài đều vắng mặt.

## Chênh lệch ngay trong snapshot tham khảo

Ba callsite không tìm được handler đích tương thích trong phần Java hiện hành. Bản ghi tương ứng và mọi alternative nằm trong `source-facts.json#/relations`:

1. `inside_payment/async/AsyncTask.java` dòng 27 gọi GET `rest-service-external:16100/greet`. Không có handler Java thuộc module này trong cây module hiện hành. Cần đối chiếu coverage deployment/nguồn khác trước khi kết luận thiếu nguồn hoặc đường gọi không hoạt động.
2. `rebook/service/RebookServiceImpl.java` dòng 358–374 chọn order/order-other và dùng POST cho đường có orderId. `OrderController.java` dòng 142 và `OrderOtherController.java` dòng 139 khai báo DELETE trên các đường tương ứng. Cặp đối chiếu cùng điều kiện: updateOrder của Rebook dòng 339–355 dùng PUT và các controller có PutMapping tương ứng. Điều này xác nhận khác biệt method trong snapshot nguồn; chưa xác nhận lỗi đã xảy ra trong RE2-TT.
3. `waitorder/utils/PollThread.java` dòng 43 chọn ts-preserve-service, dòng 54 truyền URL vào doPreserve, dòng 75–80 POST `/api/v1/contactservice/preserve`. `preserve/controller/PreserveController.java` dòng 18 và 32 khai báo `/api/v1/preserveservice` cộng `/preserve`. Không sửa literal để ép khớp. Chuỗi thread start được chỉ ra ở WaitListOrderServiceImpl dòng 162–170; branch/runtime reachability vẫn là câu hỏi khác.

Các URL alternative giữ nguyên mọi phép gán nguồn trong phương thức. Chín alternative rỗng xuất phát từ khởi tạo biến; extractor không chứng minh phân tích luồng đủ để loại chúng. Không coi số alternative là số lời gọi hay số service đã được gọi thực tế. `target_handler_candidates` chỉ là ứng viên tương thích method/path theo nguồn, chưa xác nhận tên operation do instrumentation tạo.

## Kiểm tra và giới hạn

`manual-oracle.json` được viết sau mã và các lượt nháp đầu, từ đoạn nguồn đã đọc tay và kiểm hash. Không nhận đó là oracle có trước mã. `checks.json` kiểm literal mẫu độc lập, sáu route Config, Travel batch, messaging, PollThread, repository/datasource và bean; đối chiếu danh sách Java với plan; đối chiếu số và thành viên 146 HTTP callsite bằng scanner độc lập; đối chiếu annotation handler bằng scanner riêng. Bản hiện hành có 32/32 kiểm đạt. Kết quả này kiểm tính đúng của các phép trích được nêu, không xác nhận toàn bộ hành vi Java hoặc mọi nhánh runtime.

Một lượt kiểm đầu báo lệch locator do scanner kiểm phụ thay comment nhiều dòng bằng khoảng trắng và làm mất newline. Đã giữ kết quả lỗi tại `check-history`, sửa scanner bảo toàn newline và kiểm lại đạt. Một lệnh đọc tay thử đường `notification/service/MailServiceImpl.java` không có trong snapshot; sau đó dùng đúng `MailService.java`. Không có tải hoặc sửa nguồn ứng dụng do phần việc này.

Parser từ vựng có cân bằng ngoặc, bỏ comment và giữ offset. Nó không phải javac, không suy kiểu toàn chương trình, không chạy reflection/DI/profile, không mở rộng code sinh ngoài cây hoặc thư viện Maven ngoài. Named inner class được lập chỉ mục; anonymous/local class và overload động không được nhận là đã phân giải đầy đủ. Phép thay đối số cùng lớp chỉ áp dụng khi một khai báo tên phương thức và các callsite nguồn tường minh đủ để theo; không nhận đó là call graph toàn chương trình.

Kết quả dùng được để chuẩn hóa bản ghi nguồn theo hợp đồng T-036 và so có điều kiện. Độ đủ snapshot ngoài phần Java, mapping tên runtime, lineage dataset, deployment và phép giải thích chênh lệch với graph dev do người làm T-038 tổng hợp; không lấy các kiểm ở đây thay bằng chứng đó.
