# Phản biện T-076 — Kiểm bản sửa trước merge PR #17

- **Người phản biện** Codex. **Người làm** Claude. Ngày 28/11/2026. Bước 5 Phần A, SPEC bản 6, P9/P10, ngoài G0–G4.
- **Bản đã đọc** Toàn PR `4d57225..f40b849`, riêng bản sửa `f40b849^..f40b849`. Đối chiếu với `2a275b5..f29073f` và với thay đổi của nhóm `4d57225..f0a5d30`. Các dòng mã bên dưới thuộc đầu PR trừ khi ghi rõ.
- **Tự soát độc lập** Đọc AGENTS, STATE, SPEC, DT18, hướng dẫn cô, MRP P9/P10, WHY, DECISIONS, LESSONS, B16 và schema. Kiểm mã, cấu hình, bảng file, mô tả PR, README từng lượt, log gốc và CI. Lần theo ACK/NACK, cách lưu outbox, correlation khi trả HTTP, đường phát và hoàn tác trước khi đối chiếu kết luận/phản hồi trong REVIEW đến REVIEW-5. Đọc phần duyệt, đính chính và bàn giao của LOG để kiểm quyền và diễn tiến.

## Kết luận chung

**Đề nghị Minh giữ PR ở draft và tiếp tục phản biện có mục tiêu.** CI trên đầu đã đẩy xanh. Bản sửa khắc phục fixture Booking, kết cục callback VNPay chưa rõ, cấu hình Discovery và việc Event ghi span cha khi agent tắt. Main đã tiến thêm một PR đổi chính sách số pod và script CD. Hướng dẫn hoàn tác còn thiếu một nhánh của Payment. Log cũng còn những đường ghi sai hoặc mất liên kết ngay khi agent tắt.

Bước 5 cung cấp bằng chứng tích hợp cục bộ cho P9a. Tiêu chí 1 của SPEC còn phần cập nhật theo main, Minh đọc và quyết định merge. Tiêu chí 2–4 cần lần triển khai/diễn tập đã định ở bước sau. Với tiêu chí 5, file mở rộng đã có và có lượt soát riêng. Chưa thể kết luận về tác động khi chạy thật, độ phủ ba tín hiệu, độ đúng xếp hạng hay RQ5 từ lượt này.

## Các điểm

### R1. CI xanh thuộc nền trước thay đổi số pod — CHẶN kết luận PR đã sẵn sàng trên main mới nhất

`git merge-base origin/main f40b849` trả `4d57225`. API `git/ref/heads/main` và `commits/main` đều trả `f0a5d30`. Run 46098406525 ghi `head_sha=f40b849`, `pull_requests[0].base.sha=4d57225`. Trường base trong bản ghi PR đọc được cũng còn ghi nền cũ. Đầu nhánh main và nền của lượt CI trả lời hai câu hỏi khác nhau. Việc rebase/push trước đó đã làm đúng trên nền được duyệt lúc ấy. [CI đã kiểm](https://github.com/levanminh04/flash-ticket-platform/actions/runs/46098406525) · [Thay đổi của nhóm](https://github.com/levanminh04/flash-ticket-platform/pull/59)

`git diff --stat 4d57225 f0a5d30` liệt kê sáu file, gồm HPA Booking/Payment/User, script CD, fixture và README K8s. Bản mới chấp nhận cấu hình writer một pod, kiểm số node theo profile, giữ điều kiện riêng cho reader. README K8s ở main mới ghi lần quan sát lúc 04:06 UTC và giới hạn phục hồi snapshot hai pod. Đây là bằng chứng có thời điểm của nhóm. Số pod, revision và sức chứa tại giờ merge vẫn cần nền C4. Giao của hai danh sách đường dẫn thay đổi so với `4d57225` có 0 file. Dù có thể hợp nhất sạch về văn bản, CD vẫn sẽ chạy theo profile khác lượt kiểm trước.

**Đề xuất.** Minh cho Claude cập nhật chính PR #17 trên đầu main hiện hành, giữ chính sách pod của nhóm, so lại phần K8s/CD thực sự đổi và lấy CI của cặp đầu mới. Dùng lại bằng chứng Java còn tương đương. Cách này tốn một lượt CI, tránh việc lấy CI cũ làm bằng chứng cho rollout mới. Có thể dùng CI của commit tích hợp có hai parent đã xác minh nếu Minh chấp nhận cách đáp ứng yêu cầu “trên main mới nhất”. Bước này chưa được phát trong lượt phản biện.

### R2. Mục hoàn tác bỏ Payment và nhầm thời điểm của con trỏ — CHẶN quyết định merge tự triển khai

`results/T-076/mo-ta-pr17.md` mục “Hoàn tác” và body thật của PR đều liệt kê bốn service có guard reader, nhưng chỉ kể Booking, Event, Ticket ở ngoại lệ `writer-baseline`. Trên chính nền đã soát, `deploy/scripts/deploy-k8s-service.sh:26–29` khởi tạo biến `previous` bằng **current trước lần phát**. Dòng 1050–1073 kiểm/ghi baseline ở nhánh Payment, rồi thay biến bằng giá trị **của target** nếu có. Dòng 1082–1086 mới ghi con trỏ sau triển khai. Main tiếp theo vẫn có nhánh Payment này ở dòng 1088. `previous` đọc trước phát là đích của lần rollback lúc đó. Nó không tự là đích sau khi phát PR. Cũng không thể suy từ sự tồn tại của file baseline trên revision cũ rằng revision mới sẽ có file ấy.

**Hậu quả và giới hạn.** Nếu current là B, previous cũ là A, target writer-only bình thường và không có override, sau phát thành công đích có thể là B. Với target có baseline hợp lệ, đích có thể theo baseline. Dòng “đối chiếu lại khi cần” ở C4 giảm rủi ro bấm nhầm nhưng không giúp Minh biết trước đích dự kiến hoặc việc quay lại có trả về profile hai pod. Chưa quan sát lỗi CD trên máy 84. README main mới cung cấp dấu mốc reader OFF cho Booking/Payment, chưa xác nhận cấu hình lần phát sắp tới của cả bốn service.

**Đề xuất.** Chỉnh riêng mục hoàn tác trong mô tả PR và hướng dẫn dùng ở C4. Tách current trước phát, baseline/override áp dụng cho revision đích, previous thực sau phát và digest/profile cần khôi phục. Bao gồm Payment và nhánh Discovery `compatible-previous` khi thực sự có migration. Dùng lần đọc C4 đã duyệt và xác nhận của người giữ cấu hình về reader đang chạy **và** reader dự kiến của Booking/Event/Ticket/Payment. Không cần đọc Secret. Nếu phải đổi từ reader về writer, nhóm xác nhận cách làm hợp lệ theo profile đang dùng trên cùng digest. Nếu chưa biết đích hoặc nguồn lực cần để về profile cũ, đề xuất dời merge. Chi phí chủ yếu là phối hợp nhóm hoặc một lần CD nếu thực sự phải đổi chế độ. PR revert cũng phải đi qua CD.

### R3. Lỗi kênh RabbitMQ trong Payment có thể bị ghi thành lỗi giao dịch — CHẶN kết luận R5 đã xử lý đúng nhánh ACK/NACK

Ở `PaymentMessageListener.java:30–69`, khi giao dịch thành công, hàm trong gọi `basicAck` **sau** khối xử lý nghiệp vụ. Hàm bọc phân `IOException` vào `UNKNOWN/BROKER_COMMAND_FAILED`, còn `RuntimeException` vào `RETRY/TRANSACTION_UNAVAILABLE`. Cả năm entry point có cùng cách phân loại. Khi kênh đóng trước ACK, chính lệnh ACK có thể ném `AlreadyClosedException`. Khi đó giao dịch đã commit và mã chưa hề gọi NACK, nhưng log vẫn nói lỗi giao dịch đang thử lại. Lỗi kênh xảy ra trong lúc NACK cũng đi nhầm nhánh nếu là ngoại lệ này.

**Bằng chứng riêng.** Classpath Surefire của Payment ghi `amqp-client-5.30.0` và `spring-rabbit-4.1.1`. Trong client đúng phiên bản, `ChannelN.basicAck/basicNack → transmit → ensureIsOpen`; khi đóng, client ném `AlreadyClosedException → ShutdownSignalException → RuntimeException`. Proxy kênh của Spring có đường ném lại `getTargetException()`. `ListenerTelemetryTests.java:110–122` giả lập **IOException** khi NACK. Test ấy đạt và không phân xử được nhánh trên. Đây là phản ví dụ theo mã, chưa phải sự cố đã quan sát. WHY-89 phân loại UNKNOWN khác RETRY, nên nhầm trường này ảnh hưởng cách diễn giải log. Chưa đo tác động lên hạng RCA. [Client RabbitMQ 5.30.0](https://github.com/rabbitmq/rabbitmq-java-client/blob/v5.30.0/src/main/java/com/rabbitmq/client/impl/AMQChannel.java) · [Proxy kênh Spring AMQP 4.1.1](https://github.com/spring-projects/spring-amqp/blob/v4.1.1/spring-rabbit/src/main/java/org/springframework/amqp/rabbit/connection/CachingConnectionFactory.java)

**Đề xuất.** Phân loại theo bước đã thực hiện. Chỉ ghi RETRY sau khi gửi NACK yêu cầu giao lại và lời gọi trả về. Lỗi trong lệnh ACK/NACK ghi UNKNOWN rồi ném lại nguyên lỗi. Giữ số lần gửi và thứ tự commit/ACK. Một ca ACK ném ngoại lệ kênh sau commit ở fixture listener sẽ phân biệt hai cách. Chỉ bổ sung một kiểu ngoại lệ vào catch ngoài ít sửa hơn nhưng vẫn suy bước thất bại từ kiểu lỗi.

### R4. Trả được mã đơn nhưng chưa bảo đảm nối mã tạm với mã đơn — CHẶN riêng kết luận đủ B16 §3 cho tạo đơn

Với mã tạm A và orderId B, `OrderController` trả B. Gateway chọn giá trị cuối hợp lệ ở `beforeCommit` và ghi correlation hiệu lực B khi kết thúc. Nhánh lỗi Booking dùng MDC đã chuẩn hóa cho header, body và log. Hai sửa này đúng. Khi đặt chỗ mới, `OrderServiceImpl.java:2037` gọi `BusinessTelemetry.committed`; `BusinessTelemetry.java:17–18` ghi cả `orderId` và `correlationId` bằng B. `CorrelationFilter.java` đặt A và một requestId riêng rồi trả lại MDC cũ ở finally. Mã tạo đơn không phát sự kiện chứa cặp A/B. Đường trả order đã có do idempotency cũng có thể return trước sự kiện reserve.

Phản bác của Claude đúng **có điều kiện**. Nếu Booking đã ghi một dòng có A và cùng requestId với dòng reserve thì nối được qua hai dòng. Gắn MDC không tự sinh dòng này. Gateway và Booking tạo requestId riêng. Trên đường thành công im lặng trước reserve, cả dòng kết thúc gateway lẫn dòng reserve đều mang B. Người có B truy được đơn. Người chỉ có A từ bước trước chưa có liên kết B16 §3 hứa. Không có căn cứ để nói mọi đơn đều đứt chuỗi.

**Đề xuất.** Ở bước trả thành công đã biết B, khi A khác B, ghi một sự kiện nối bằng hai trường sẵn có `correlationId=A`, `orderId=B`; giữ B trên phản hồi và sự kiện nghiệp vụ. Sự kiện mô tả việc nối mã cũng dùng được cho lần trả lại đơn cũ mà không ghi nhầm là vừa reserve. Một request thành công kiểm dòng nối và header phân xử trực tiếp. Nếu Minh chấp nhận hoãn thì ghi rõ mức phủ này trước khi dùng chuỗi theo mã tạm.

### R5. Outbox vẫn có thể báo đã lên lịch thử lại dù không cập nhật dòng nào — KHÔNG CHẶN giao dịch, chặn diễn giải log retry

`MessagingServiceImpl.java:79–85` của Payment trả về bình thường khi bản tin đã published hoặc số lần claim khác. `PaymentWorker.java:88–104` vẫn ghi `RETRY`. Ở Ticket, `TicketOutboxPublisher.java:135–152` bỏ qua số hàng của lệnh dời lịch có điều kiện theo attempts và published_at, rồi chọn RETRY chỉ vì biến failure có giá trị. Ví dụ worker cũ nhận được lỗi gửi sau khi worker mới đã đánh dấu published. Lệnh dời lịch không tác động, nhưng dòng của worker cũ báo RETRY. Nhánh Ticket xử lý thành công đã kiểm số hàng và có mã `LEASE_CHANGED`; đây là đối chứng trong chính file. Phía Payment, `BROKER_CONFIRMED` vẫn đúng khi đã nhận confirm. Riêng nhánh lỗi **sau confirm**, reason đã sửa thành `PUBLISH_FAILED` nhưng chuỗi message luôn là “Outbox delivery unconfirmed”.

**Đề xuất.** Để telemetry nhận biết dời lịch có hiệu lực qua kết quả cập nhật hoặc cờ trả về. Với claim đã hết hiệu lực, dùng kết cục trung tính cho lần xử lý này. Chỉnh message Payment theo bước đã biết. Giữ điều kiện DB, mã lưu DB và thời gian dời lịch. Lợi ích là phân biệt được lỗi gửi với một worker đã mất quyền cập nhật; đổi kiểu trả về nội bộ sẽ cần kiểm caller/mock. Nếu chỉ cần thể hiện ý định dời lịch, Minh có thể chọn mô tả hẹp hơn cho sự kiện và hoãn xác nhận việc đã lên lịch. Chưa có số ca mất lease từ môi trường chạy thật.

## Đối chiếu các lượt trước

| REVIEW-5 | Đánh giá phản hồi tại đầu đã sửa |
|---|---|
| R1 | **Đúng, đã xử lý.** Năm fixture đổi sang phương thức `*Delivery(Envelope, Message)`. Log Booking integration ghi 157 ca BookingPersistenceIT đạt trong 173 ca Failsafe. Các assertion về ACK và delivery còn đó. |
| R2 | **Đúng một phần.** Guard cùng image là điều kiện triển khai, writer-only sang writer-only có thể hợp lệ. Tình trạng tại giờ merge thuộc bước 6. Hướng dẫn rollback hiện tại vẫn thiếu Payment và thời điểm con trỏ, xem R2 lượt này. |
| R3 | **Đúng một phần.** Header và nhánh lỗi đã sửa. Lập luận dựa vào requestId cần có dòng trước reserve; xem R4. Không có bằng chứng ngăn được việc tạo đơn. |
| R4 | **Đúng, đã xử lý.** Nhánh UNKNOWN có trong switch. Test callback hiện có bao gồm mã 07; test telemetry kiểm ba trạng thái. Đếm JSON có eventName bằng `payment.callback-confirmed` trong log Payment sau rebase cho bốn dòng UNKNOWN/UNKNOWN, năm SUCCEEDED/SUCCESS và một FAILED/FAILED (stateAfter/outcome). Đây là dữ liệu thử cục bộ. |
| R5 | **Đúng một phần.** Booking phân biệt ngoại lệ reject tường minh với lỗi cần requeue. Payment giữ ném lỗi, các ca hợp đồng sai, NACK thành công và IOException được phân biệt. Ngoại lệ kênh không kiểm tra tại compile time còn bị gán RETRY. AUTO của Booking và giới hạn giao lại của broker cũng không chứng minh từng bản tin cuối cùng được phát lại. |
| R6 | **Đúng, đã xử lý ở manifest.** Đã đối chiếu ConfigMap và StatefulSet Discovery, thấy production, nodeName và công tắc false. Giá trị trên pod thuộc bước 7. |
| R7 | **Đúng một phần theo điều kiện.** Khi chỉ có traceparent và spanId của bên gửi, customizer loại span cha; khi có span_id hợp lệ thì ưu tiên khóa này. Test Event tách hai trường hợp. Để xác nhận khi bật agent thật cần ghép một log Event với span nhận của chính Event, có thể dùng lượt kiểm tín hiệu bước 9 thay vì chạy thêm ở bước 5. |
| R8 | **Đúng với sai lệch ban đầu.** Ticket tách lỗi dữ liệu/DB khỏi AmqpException ở log. Payment nhớ trạng thái confirm. Các vị trí sửa dùng attempt trừ một có chặn dưới ở 0. Mã DB/lịch retry được giữ. Mặt còn thiếu của diễn giải retry và chuỗi message ở R5 lượt này. |
| R9a | **Đúng.** README gốc đã đính chính cách build local bằng COPY và giới hạn CI. Chú thích lịch sử ở đầu `agent/build-image.sh` vẫn nói CI chạy ADD. Phạm vi duyệt mục 9 nêu README. Khi trích kết quả dùng README đã đính chính; lần build CD mới phân xử việc tải asset tại đó. |
| R9b | **Đúng, đã thực hiện trong phạm vi local.** Giữ các lần hỏng. Bản sao fixture đổi user và điều kiện chờ RabbitMQ, thể hiện ở diff hai dòng. Ca IT đạt 25/25. Lệnh verify cả bộ dưới env replica có bốn lỗi trùng bốn tên test cấu hình trong đối chứng main. Kết quả này hỗ trợ giải thích lỗi môi trường bộ thử; không xác nhận recipe nguyên bản đạt hay xác nhận reader thật. |
| N1 | **Đúng, đã sửa theo duyệt.** Bảy ConfigMap bỏ hai khóa tùy chỉnh của agent. Kiểm Event agent bật còn như R7. |
| N2 | **Đúng về đính chính.** LOG ghi bổ sung lúc 14:30Z; TSV kiểm sau rebase hỗ trợ thứ tự. Hai giờ thay thế là xấp xỉ theo người làm, không dùng để đo thời lượng. |

Các điểm của lượt thiết kế được xét theo phiên bản khi nêu. Bảng dưới ghi tác động còn hiệu lực ở bước 5.

| Lượt | Đối chiếu từng điểm và phản hồi |
|---|---|
| 1 | **R1 đúng** — truy vấn M1 cộng theo service, nguồn metric dùng chung có thể lẫn; H1 đã loại đường xuất này. **R2 đúng** — danh sách khóa được CD đưa vào Secret và Discovery dùng ConfigMap làm thay đổi cách đưa credential; Phần A không triển khai tuyến CA/token. **R3 đúng** — kiểm sau bộ lọc không bảo đảm dữ liệu trước khi xuất; query thử vẫn còn email/phone. **R4 đúng một phần về mức đã khép** — Q7/Q8 có nền và hành động, phần rollback xem R2. **R5 đúng** — danh sách B16 loại Assistant, workflow vẫn yêu cầu mẫu với service trong danh sách. **R6 đúng** — workflow build giữ hai kiến trúc và thêm SHA. **R7 đúng** — SPEC tách commit lab và quyền vận hành, hoạt động thật chờ Phần B. |
| 2 | **N1 đúng** — `previous` có thể đổi sau phát; Q10 ghi phương án revert. **N2 đúng** — truy vấn Tempo của lab `c1da15f:tests/signals/check_purchase_journey.py:107–119` lọc service/route; H1 hoãn đường production dùng chung. **N3 đúng** — đối chứng bật đã lưu ở `ban-6/bat-ghi-de/phan-tich.txt` cho thấy query chỉ che theo tên, exemplar bằng 0 trong lượt thử. **N4 đúng** — serviceMap của datasource Tempo trỏ Prometheus cấu hình sẵn; Phần A chưa thêm datasource. |
| 3 | **R1 đúng** — công tắc cứng hiện có trên bảy Deployment và một StatefulSet. **R2 đúng** — C4 có nền, Q7/Q8 và hành động cho bản agent tắt. **R3 đúng** — bước 9 và 10 ghi các thao tác obs khác nhau và quyền tương ứng. **R4 đúng** — C6 loại sự cố hệ thống đang mở và yêu cầu đúng ca/cửa sổ. **R5 đúng** — C5 chỉ chọn bản demo, W7 chờ quyết định riêng. **R6 đúng** — README nhánh mục mở rộng có cả exception.message và exception.stacktrace. **R7 đúng** — bước 8 đã tính cấu hình Compose, ngrok, tag cũ và giới hạn phục hồi DB. Hai việc sau liên quan phạm vi thiết kế, chưa có nghiệm thu triển khai. |
| 4 | **R1 đúng một phần về cách xử lý** — đọc con trỏ và digest cần thiết, còn phải xét target và profile, xem R1–R2 lượt này. **R2 đúng** — SPEC tách Q4 chạy từ obs và runbook cho bước 10, không dùng lại nguyên checkout cũ. **R3 đúng** — C6 dẫn đúng tiêu chí E5, đúng ca, cửa sổ, cờ và hạn mở dashboard. **R4 đúng** — mã Java B16 chạy ngay cả lúc agent tắt; CI/schema không quyết định ngữ nghĩa, như phản ví dụ ACK và outbox ở trên. |

## Tuân thủ quy trình

SPEC bản 6 và STATE giao đúng vai trò. LOG phiên 6 ghi đề xuất 1–9, Minh duyệt sửa gồm N1, sau đó duyệt rebase/push trên nền `4d57225`. LOG công khai việc người làm đã thấy tóm tắt trước khi tự soát. Không lấy sự đồng ý của hai bên làm bằng chứng. Diff bản sửa có 28 file; phạm vi mã, fixture và manifest tương ứng các mục đã duyệt. Không thấy bằng chứng sửa ngoài quyền trong diff này. Lượt soát runbook là việc khác đã được ghi riêng ở cuối LOG.

Hướng dẫn Minh đọc “44 file Java ngoài test” của bước 5 thuộc diff cũ. Đếm đường dẫn `/src/main/.*\.java$` bằng `git diff --name-only 4d57225 f40b849` được **46**. So với tập đường dẫn cũ tăng đúng `GlobalExceptionHandler.java` và `OrderController.java`. Khi bàn giao Minh đọc, dùng danh sách của revision sắp merge để không bỏ hai đầu vào HTTP vừa sửa.

DT18-NV1/NV2, hướng dẫn của cô và MRP yêu cầu hệ giao dịch và tín hiệu phục vụ đồ thị. H1/H4, công tắc tắt trên K8s và tiêu chí demo là quyết định của Minh. WHY-08 chi phối dùng chung lõi; WHY-89 giải thích vì sao nhầm outcome có thể đổi cách mã hóa một dòng log. Diff là phần sinh tín hiệu, không thay đặc trưng, bộ ứng viên, xếp hạng hoặc đối chứng đồ thị. Không thấy nhãn sự cố được đưa vào phương pháp từ các sửa đang xét. Không có lựa chọn thuật toán mới cần đưa vào WHY. Chữ ghi quyết định T-076 vào DECISIONS vẫn chờ Minh theo LOG. Không mở quyết định nghiên cứu hay thay tiêu chí C6 sau khi xem kết quả.

## Điều đã kiểm và thấy đúng

- **Revision và toàn vẹn.** `git range-diff 6b77144..f29073f 4d57225..f40b849` cho bảy commit tương đương và một commit chỉ đổi ngữ cảnh ở Payment .env.example. `git diff --shortstat 4d57225 f40b849` cho 138 file. `git diff --check` trên cặp này sạch. Worktree ở đúng đầu PR, không có thay đổi tracked. Trong repo RCA, SHA-256 SPEC bản 6 khớp tiền tố LOG. `git diff HEAD --name-only -- results/T-076/kiem-cuc-bo tasks/T-076-pr17-otel-may-84` rỗng trước khi tạo bản này, 50 file lượt `sua-review-5/` có trong Git. T-076 không có SHA256SUMS chung. Q4 có 12/12 hash khớp; hai file khai trước E5 và triển khai E5 khớp tiền tố ở LOG T-073. Không sửa đầu ra được ghim. Rà SPEC, bảng file và manifest/plan đã theo dõi: mã FlashTicket nhận dạng bằng commit; các đường dẫn trùng tên trong manifest Train Ticket là nguồn khác. Sửa PR sẽ đổi commit/blob và có thể đổi digest image. Q4/E5 và log kết quả cục bộ giữ theo revision gốc.
- **CI và PR.** `gh pr checks 17` trả HTTP 401 trong phiên này. Đọc được qua REST công khai `gh api -H 'Authorization:' repos/levanminh04/flash-ticket-platform/commits/f40b849/check-runs?per_page=100`. Đếm `.check_runs[].conclusion` cho **14 success, 1 skipped** (Frontend). Required, tám job Maven và bước routing trong job Deploy scripts đạt. Body thực khớp `mo-ta-pr17.md` sau bỏ tiêu đề riêng và chuẩn hóa xuống dòng. [Run đã kiểm](https://github.com/levanminh04/flash-ticket-platform/actions/runs/46098406525)
- **Đầu ra cục bộ.** Dưới `results/T-076/kiem-cuc-bo/sua-review-5/`, lọc dòng tổng `Tests run: …, Failures: …, Errors: …, Skipped: …` trong `verify/log/*verify.log`. Payment 144, Event 179, Ticket 229, Booking 457; profile RCA Event 187, Booking 466; Booking integration 457 + 173. Payment sau rebase trong `main-4d57225/verify/log/payment-service-verify.log` là 153 + 57. Các tổng vừa nêu đều có ba bộ đếm cuối bằng 0. Tệp `*-b16.log` của bốn service sửa ghi PASS trên hai mẫu/service. Các lỗi fixture Ticket và đối chứng bốn ca được báo riêng ở R9b.
- **Manifest và dữ liệu thô.** Kiểm công tắc false và `HOST_ID=spec.nodeName` trong bảy Deployment và StatefulSet Discovery. So với main ghim, `git diff --name-only 4d57225 f40b849 -- deploy/k8s/examples` rỗng. `main-4d57225/log/{kiem-manifest.txt,k8s-tom-tat.txt}` ghi giá trị môi trường và kết quả bốn script. Lọc JSON ở `tat-secret-true/booking.log`, nhóm theo version/environment/host/eventName/outcome: 135 dòng cùng revision `f29073f`, production, node-thu, runtime.log, UNKNOWN. Hai file OTLP cạnh đó đều 0 byte. Đây là log runtime của lượt thử agent tắt, không có ca mua vé để suy ra liên kết A/B. Chính sách rollout, độ phủ span trên pod và hành trình thật vẫn cần dữ liệu bước 6–9.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. Đã kiểm độc lập bước 5, đối chiếu từng điểm và phản hồi, CI, diff, bytecode/phần mã thư viện liên quan và đầu ra đã lưu.
2. Chỉ ghi `tasks/T-076-pr17-otel-may-84/REVIEW-6.md`. Không chạy thử mới, vào máy 84/exp-app/obs, mở dữ liệu khóa, gửi bình luận hay commit.
3. CI và các kiểm build hỗ trợ bản sửa trên nền đã ghim. Phản ví dụ ở R3–R5 là hành vi theo mã trong điều kiện nêu rõ. Không có phép đo tần suất production hoặc mức đổi thứ hạng.
4. **Đề nghị tiếp tục.** Minh cho Claude đáp R1–R5 và trình phạm vi sửa tối thiểu. Ưu tiên cập nhật nền và hướng dẫn CD, sửa cách nhận loại lỗi kênh, rồi quyết phạm vi nối mã và diễn giải retry. Có thể gộp các sửa được Minh chọn vào cùng lần CI để giảm chờ. Chấp nhận giới hạn telemetry sẽ giảm công sửa, nhưng phải thu hẹp kết luận B16 tương ứng. Xác nhận reader, baseline, profile, giờ merge và Q7/Q8 thuộc bước 6 và nhóm vận hành. Lần quan sát thật thuộc bước 7. Chất lượng phương pháp trên FlashTicket cần đánh giá ở P10/W7 theo quyết định riêng. Chỉ đưa bằng chứng tích hợp đúng revision vào báo cáo đồ án.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6).
- Công đoạn: người làm đáp phản biện REVIEW-6, bước 5 Phần A trước merge PR #17.
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4, không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}, results/T-076/{bang-file-pr17.md,mo-ta-pr17.md,kiem-cuc-bo/}, B16 và deploy/observability/log.schema.json ở repo FlashTicket, DT18, hướng dẫn của cô và MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md, REVIEW-5.md, REVIEW-6.md và các bảng phản hồi tương ứng.
- Code và kết quả liên quan: D:/Project/flash-ticket-platform, worktree D:/Project/ft-pr17-dung-lai; PR #17, git diff 4d57225 f40b849, git show f40b849, git diff 2a275b5 f29073f và git diff 4d57225 f0a5d30; CI của PR và results/T-076/kiem-cuc-bo/sua-review-5/.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat theo quyền hiện có. Không vào máy 84, exp-app, obs. Không dùng subagent.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.
```

## Phản hồi của người làm (người làm điền sau)

Người làm chỉ điền bảng này khi Minh cho phép. Thêm N1, N2… cho điểm tự tìm. Để trống cột Minh quyết.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN | `git fetch` 28/11: main `f0a5d30` (PR #59 `86f5030`, tạm một Pod). `git diff --stat 4d57225 f0a5d30`: 6 file (HPA Booking/Payment/User, `deploy-k8s-service.sh`, `test-k8s-deploy.py`, README K8s), không trùng file PR. `git merge-tree` sạch, nhưng CI và bộ kiểm K8s của PR chạy trên `4d57225`. Sửa: rebase lên `f0a5d30`, chạy lại bộ kiểm K8s (gồm test mới của main) và service có code đổi, CI trên đầu mới. | |
| R2 | Đúng; CHẶN | `deploy-k8s-service.sh` (PR @`f40b849`) dòng 26–29 đặt `previous` = `current` trước phát; dòng 523 (Booking) và 1081 (Payment) thay bằng `writer-baseline` **của revision đích** nếu có; dòng 1082–1086 ghi file `previous` sau phát. Mục "Hoàn tác" ghi đích = `previous` đọc trước merge và bỏ Payment: sai. Thêm (người làm tìm khi kiểm): trên main `f0a5d30`, `writer_revision`/`payment_writer_revision` đòi HPA 2/2, nên revision một Pod không làm baseline cho reader được. Sửa: viết lại mục Hoàn tác trong `results/T-076/mo-ta-pr17.md` (body PR cập nhật khi Minh duyệt push). | |
| R3 | Đúng; CHẶN kết luận R5 lượt trước | `PaymentMessageListener.java` (5 hàm bọc): `basicAck` sau commit ném `AlreadyClosedException` (`ShutdownSignalException` ⊂ `RuntimeException`) → nhánh `RETRY/TRANSACTION_UNAVAILABLE`, sai bước. `basicNack` ném lỗi này trong catch cũng rơi vào RETRY. Test cũ chỉ giả `IOException`. Sửa tối thiểu: bắt `ShutdownSignalException` trước `RuntimeException` → `UNKNOWN/BROKER_COMMAND_FAILED`; test ACK ném lỗi kênh. Mặt trái: vẫn suy bước từ kiểu lỗi; nghiệp vụ Payment gửi qua `RabbitTemplate` nên lỗi kênh ở đó đã được Spring đổi thành `AmqpException`, không trùng nhánh này. Cách theo bước (Codex) chắc hơn nhưng đổi chữ ký 5 hàm trong. | |
| R4 | Đúng; CHẶN riêng B16 §3 tạo đơn | B16 §3 dòng 34: "Request trước khi có đơn dùng correlation tạm và log liên kết khi tạo thành công". `CorrelationFilter` đặt A; `OrderController` trả B; không dòng nào có cả A và B. Sửa: khi trả thành công và A ≠ B, ghi sự kiện `order.correlation-linked` (`correlationId`=A, `orderId`=B, `outcome`=SUCCESS); schema để `eventName` tự do. Test controller kiểm dòng nối. | |
| R5 | Đúng; KHÔNG CHẶN | Ticket `TicketOutboxPublisher.java`: kết quả `jdbc.update` dời lịch bị bỏ, `RETRY` chỉ dựa vào `failure`. Payment `MessagingServiceImpl.rescheduleOutbox` `return` im lặng khi lease đổi; `PaymentWorker` vẫn ghi `RETRY`, message luôn "Outbox delivery unconfirmed". Sửa: dời lịch không tác động → `UNKNOWN/LEASE_CHANGED`; `rescheduleOutbox` trả boolean; message theo bước. Giữ điều kiện DB, mã lưu DB, thời gian dời. | |
