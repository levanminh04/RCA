# Phản biện T-076 — Kiểm lại bản sửa REVIEW-8 trước merge PR #17

- **Người phản biện** Codex. **Người làm** Claude. **Ngày** 28/11/2026. Bước 5 Phần A, SPEC bản 6, P9/P10 ngoài G0–G4.
- **Bản đã soát** `f0a5d30..e19fc53` là toàn PR. `cd21f17..e19fc53` là bản sửa REVIEW-8. Hồ sơ RCA tại `6fb207132`. Chỉ ghi bản lượt 10. Lượt 9 dành cho runbook.
- **Nguồn** AGENTS, STATE, SPEC, LOG, bảng file, mô tả PR, README các lượt kiểm, log Maven, B16 và K8s. Đối chiếu DT18 §2, hướng dẫn cô §1–3, MRP P9/P10, WHY-09/89, DECISIONS, LESSONS QT12/16–19, B16 §3–8, schema log, mã FlashTicket và CI của PR.
- **Tự soát độc lập** Đọc SPEC, diff, bản mô tả và đầu ra gốc trước các bảng đáp. Lần theo lệnh trên kênh RabbitMQ, mã giao dịch từ outbox tới JSON, điều kiện reader, con trỏ và nhánh phục hồi trong CD. Kiểm cả listener Ticket dùng cùng kiểu xác nhận thủ công. Sau đó đối chiếu từng ý cũ với bản sửa, LOG và kết quả của đúng ca thử.

## Kết luận chung

**Đề nghị giữ PR ở draft và tiếp tục phản biện đúng hai điểm dưới đây.** Payment đã sửa đúng kết cục ACK/NACK và mã giao dịch của outbox. Mô tả đã tách đúng hai nhóm cấu hình reader. CI bắt buộc đạt trên đầu PR. Còn một log Ticket sai nghĩa ngay trong phép thử đã lưu và hai đường dừng sớm của CD chưa được nói rõ cho người quyết định hoàn tác. Bước 5 chưa đủ để nghiệm thu T-076 hay kết luận hệ thống đã chạy ổn định trên máy 84.

## Các điểm

### R1. Ticket ghi lỗi xử lý bản tin khi nghiệp vụ đã trả về và ACK mới là bước hỏng — CHẶN kết luận C4 về ngữ nghĩa listener Ticket

**Bằng chứng đã xảy ra trong test.** Trong `services/ticket-service/.../TicketListenerTests.java:115–123`, ca `acknowledgementFailurePropagatesWithoutSecondNackAfterCommit` cho dịch vụ trả về, đặt `IOException` tại ACK, kiểm thứ tự và xác nhận không có lệnh thứ hai. XML Surefire của chính ca đó chứa `ticket.message.processed / FAILED / MESSAGE_PROCESSING_FAILED`. Bản ghi đã lưu trong repo cũng cho đúng ba trường ấy. [Log Maven, dòng 189](../../results/T-076/kiem-cuc-bo/sua-review-6/verify/log/ticket-service-verify.log#L189) · [Ca kiểm trên đầu PR](https://github.com/levanminh04/flash-ticket-platform/blob/e19fc53/services/ticket-service/src/test/java/com/flashticket/ticket_service/TicketListenerTests.java#L115)

**Cơ chế.** `TicketBusinessListeners.consume` dùng chung cho access, cancellation và issue. Hàm gọi `transaction.accept(decoded)` ở dòng 71. ACK ở dòng 86 và chỉ sau khi ACK trả về mới đặt SUCCESS. Nếu ACK ném lỗi, khối tự đóng ghi giá trị mặc định của `RabbitTelemetry`. Dòng 76–82 có cùng đường rơi về mặc định nếu chính lệnh reject hoặc NACK ném lỗi. Nhánh ACK đã có bản ghi thật từ ca thử. Hai nhánh còn lại là hệ quả đọc mã. Ở ca đối chứng, NACK yêu cầu giao lại trả về bình thường, log ghi `RETRY/TRANSACTION_UNAVAILABLE`. [Listener Ticket](https://github.com/levanminh04/flash-ticket-platform/blob/e19fc53/services/ticket-service/src/main/java/com/flashticket/ticket_service/messaging/TicketBusinessListeners.java#L64) · [Giá trị mặc định và dòng xuất](https://github.com/levanminh04/flash-ticket-platform/blob/e19fc53/services/ticket-service/src/main/java/com/flashticket/ticket_service/observability/RabbitTelemetry.java#L15)

**Hệ quả.** Người trực có thể quy lỗi cho bước xử lý vé khi bước chưa xác định được kết quả là lệnh gửi tới broker. Test xanh là hợp lý vì nó kiểm thứ tự và ngoại lệ. Nó chưa kiểm nội dung log của ca đó. Phần sửa Payment đáp đúng phạm vi Minh duyệt. Lỗi Ticket có từ phần khác của PR. WHY-89 gom cả FAILED và UNKNOWN vào nhóm lỗi, nên riêng đổi hai giá trị này không làm đổi phân nhóm đó. Chưa có số đo ảnh hưởng tới xếp hạng hoặc bằng chứng sự cố thật trên 84.

**Sửa tối thiểu đề nghị Minh duyệt.** Trong `TicketBusinessListeners.java`, ngay trước từng lệnh ACK/NACK/reject, đặt kết cục dự phòng `UNKNOWN/BROKER_COMMAND_FAILED`. Giữ kết cục cụ thể ngay sau khi lệnh trả về. Cách này giữ ngoại lệ gốc, số lần và thứ tự gọi, không cần đưa proxy của Payment sang Ticket. Trong `TicketListenerTests.java`, bổ sung kiểm sự kiện phát ra vào ca ACK đã có và kiểm hai nhánh lệnh còn lại ở cùng fixture. Chỉ sửa mô tả PR sẽ ít việc hơn nhưng để nguyên bản ghi sai ở đầu ra. Thay mã/test sẽ đổi đầu PR và cần CI của đầu mới.

### R2. CD có thể dừng giữa chuyển đổi mà chưa đi vào nhánh phục hồi — KHÔNG CHẶN mã PR, còn thiếu căn cứ dùng hướng dẫn C4 trên đường chuyển đổi cũ

**Ở đâu.** Mục Hoàn tác đã bỏ lời hứa khôi phục vô điều kiện. Ba trường hợp đã viết đều có cơ sở. Tuy nhiên, phần hướng dẫn tại dòng 67–71 chưa cho người trực biết một lần kiểm lỗi *bên trong* bước kết thúc chuyển đổi có thể thoát hẳn trước nhánh phục hồi. [Mô tả PR trong hồ sơ](../../results/T-076/mo-ta-pr17.md#L67)

- Khi áp và kiểm revision đích đạt, script gọi `finish`. Hàm này kiểm lại peers, có thể tạo bản nền rồi xóa Deployment cũ trước khi ghi `migration-finished`. Nếu `finish` lỗi, script thoát với `DISCOVERY_MIGRATION_FINALIZE_FAILED` trước khi ghi `current/previous` hoặc gọi `restore`. Workload có thể đã đổi dù con trỏ còn cũ. [Điểm thoát của CD](https://github.com/levanminh04/flash-ticket-platform/blob/e19fc53/deploy/scripts/deploy-k8s-service.sh#L1090) · [Thứ tự trong finish](https://github.com/levanminh04/flash-ticket-platform/blob/e19fc53/deploy/scripts/migrate-k8s-discovery.py#L192)
- Khi áp/kiểm lỗi và có `bridge-drained.json`, script gọi `unbridge` để đưa ứng dụng cũ trở lại phục vụ. Nếu lệnh lỗi, `LEGACY_APPLICATION_UNDRAIN_FAILED` kết thúc script trước cả lần thử áp lại revision trước. [Điểm thoát trước restore](https://github.com/levanminh04/flash-ticket-platform/blob/e19fc53/deploy/scripts/deploy-k8s-service.sh#L1106)

**Phạm vi và phản chứng.** Đây là hai đường có thật trong code gốc của main. Chưa có bằng chứng chúng xảy ra trên 84. Câu yêu cầu đọc thông báo và workload thật ở dòng 71 là đúng và giảm nguy cơ thao tác nhầm. Khi lần phát không đi qua chuyển đổi legacy, hai đường này không phải lý do hoãn merge. Các fixture lưu riêng kết quả phục hồi thành công và kết thúc chuyển đổi thành công. Chúng không chứng minh hai thao tác luôn thành công trong cùng một lượt.

**Sửa tối thiểu đề nghị Minh duyệt.** Thêm vào `results/T-076/mo-ta-pr17.md` một câu cho hai mã dừng trên: kiểm workload đang phục vụ và các con trỏ trước khi chọn đích, vì CD có thể chưa thử khôi phục. Đồng bộ đúng câu đó vào body PR khi Minh cho phép. Đổi tài liệu không đổi đầu PR hay kết quả CI. Chờ xác nhận cụm đã hết chuyển đổi cũng có thể loại rủi ro cho riêng lần phát này, nhưng để hướng dẫn chung thiếu thông tin. Không cần đổi script CD của nhóm.

## Đối chiếu các lượt trước

### REVIEW-8 và phản hồi của Claude

| Điểm | Đánh giá độc lập tại đầu PR |
|---|---|
| R1, kết cục Payment | **Đúng, đã xử lý** cho các đường được nêu. Dùng `git grep -n` tại `e19fc53` trên `PaymentMessageListener.java`, đếm từng mẫu `@RabbitListener`, `track(channel)`, `basicAck(` và `basicNack(`, kết quả lần lượt 5, 5, 5, 5. Proxy lưu lỗi tại chính lệnh, tháo `InvocationTargetException` và ném lỗi gốc. NACK trả về bình thường mới đánh dấu đã yêu cầu giao lại. `failed()` ưu tiên lỗi kênh. Các test phân biệt cùng kiểu `IllegalStateException` ở bước nghiệp vụ và ở lệnh kênh. Điều này khớp nhánh xử lý kênh đóng của [Spring Rabbit 4.1.1](https://github.com/spring-projects/spring-amqp/blob/v4.1.1/spring-rabbit/src/main/java/org/springframework/amqp/rabbit/connection/CachingConnectionFactory.java#L1133) và chữ ký ACK/NACK của [RabbitMQ Java 5.30.0](https://github.com/rabbitmq/rabbitmq-java-client/blob/v5.30.0/src/main/java/com/rabbitmq/client/Channel.java#L698). |
| R2, profile reader | **Đúng, đã xử lý trong mô tả.** So các hàm kiểm writer ở `deploy-k8s-service.sh:424,559,773,968`, các guard tại 636/764 và fixture K8s lưu trong `sua-review-6/verify/k8s-py3/test-k8s-deploy.py.log`. Booking/Payment cần nền hai pod cho reader. Event/Ticket kiểm profile một pod và điều kiện tương thích riêng. Body công khai có đoạn HPA 1/1. Trạng thái reader đang chạy và định phát thuộc bước 6. |
| R3, phục hồi | **Đúng về lỗi cũ. Phản hồi và bản sửa đúng với ba trường hợp đã nêu, còn thiếu ngoại lệ ở R2 lượt này.** CD kiểm điều kiện trước khi áp, có thể phục hồi Deployment cũ khi đang chuyển Discovery, và chỉ in `RESTORED_PREVIOUS` sau khi áp lẫn kiểm lại đều đạt. Người làm đã thêm bước đối chiếu workload thật. Trang PR có các mã kết quả đã bổ sung. |
| R4, correlation của outbox Payment | **Đúng, đã xử lý.** `OutboxMessage.java:33,64` lấy correlation từ envelope và ghi cột bắt buộc. `PaymentWorker` lấy lại từ entity ở cả đường broker xác nhận và đường lỗi. `LogFields` chấp nhận trường này. Hai bản ghi thực trong log Payment của lượt sửa, một RETRY và một UNKNOWN, có đủ messageId và correlationId. Test dùng hai UUID riêng. Với nhánh thành công, bằng chứng ở lần soát này là đường mã. BROKER_CONFIRMED chỉ xác nhận broker đã nhận. |

### Các lượt trước REVIEW-8

Các đánh giá dưới đây xét ý kiến tại thời điểm nêu và phần còn hiệu lực ở bước 5. Điều kiện chạy ở Phần B giữ theo SPEC và lượt runbook riêng.

| Lượt | Điểm và căn cứ đối chiếu |
|---|---|
| REVIEW | **R1 đúng** về lẫn metric khi gộp nguồn. C2 hiện tắt agent trên 84. **R2 đúng** về CD chọn khóa theo mẫu Secret. Diff mẫu Secret rỗng. **R3 đúng** về lọc trước xuất theo B16 §6. **R4 đúng** về nền và đích phục hồi. C4/Q7/Q8 khai rõ GET và bộ nhớ. **R5 đúng**, workflow Maven đọc danh sách B16 ngoài Assistant. **R6 đúng**, workflow build giữ hai kiến trúc và build-arg phiên bản. **R7 đúng** về quyền, SPEC bản 6 chia phần ghi theo repo và bước. |
| REVIEW-2 | **N1 đúng**, lần phát thành công có thể thay `previous`. **N2 đúng có điều kiện** khi nhiều môi trường cùng xuất trace vào Tempo. H1 hiện tắt nguồn 84. **N3 đúng**, file `ban-6/bat-ghi-de/phan-tich.txt` còn sentinel email trên trace khi q đã che. **N4 đúng ở thiết kế cũ**, nạp datasource khác thuộc lúc thực hiện mở rộng. |
| REVIEW-3 | **R1 đúng**, tám manifest hiện khai tắt ở `env`. **R2 đúng**, C4 khai trước nền, GET, điều kiện dừng. **R3 đúng** về quyền cho obs/máy tải ở bước 9–10. **R4 đúng**, C6 đòi sự cố mới, đúng lớp và cửa sổ. **R5 đúng**, C5 tách bản demo khỏi lựa chọn W7. **R6 đúng**, phần mở rộng xét cả message và stacktrace. **R7 đúng**, bước 8 yêu cầu kiểm bản ghim, dữ liệu và đích hoàn tác. Đây là các sửa thiết kế. |
| REVIEW-4 | **R1 đúng**, rollback cần revision và image khớp. **R2 đúng**, SPEC §Phạm vi ghi và bước 9–10 đã ghi quyền, thao tác và đường hoàn tác. **R3 đúng**, C6 nối ca từ mốc phát hiện tới trang ca. **R4 đúng**, diff cho thấy mã Java vẫn chạy dù agent tắt. |
| REVIEW-5 R1–R5 | **R1 đúng**, fixture Booking đã gọi hàm Delivery. **R2 đúng về guard**, quyết định merge còn phụ thuộc người giữ cấu hình. **R3 đúng về thiếu liên kết ban đầu**, ý phản bác việc suy rộng thành lỗi mọi giao dịch là hợp lý. Đầu này có dòng nối mã tạm với orderId và trả mã đơn. **R4 đúng**, callback UNKNOWN được Payment giữ UNKNOWN sau commit. **R5 đúng trong phạm vi Booking/Payment đã nêu**, đã phân biệt hợp đồng sai, giao lại và lỗi kênh Payment. Mở rộng kết luận sang Ticket gặp phản ví dụ R1 ở trên. |
| REVIEW-5 R6–R9, N1–N2 | **R6 đúng**, Discovery dùng StatefulSet và hostId từ node. **R7 đúng một phần**, Event loại span cha khi thiếu span hiện hành. Việc nối với trace thật khi bật agent còn thuộc bước 9. **R8 đúng**, Ticket tách lỗi dữ liệu/DB khỏi lỗi broker trong lý do ghi log, Payment phân biệt trước/sau confirm. **R9a đúng**, kiểm build tại laptop từng dùng COPY, CI của PR chưa chạy dòng ADD của CD. **R9b đúng**, lượt test replica riêng có sửa fixture, LOG giữ lỗi của lượt ban đầu. **N1 đúng**, cấu hình MDC tùy chỉnh đã bỏ. **N2 đúng** về việc LOG có đính chính giờ, không dùng mốc xấp xỉ để tính thời lượng. |
| REVIEW-6 | **R1 đúng tại lúc nêu**, nay đầu GitHub đã trên main yêu cầu và Required đạt. **R2 đúng**, mô tả đã có Payment, tách current trước phát và previous sau phát. Giới hạn phục hồi ở R2 lượt này. **R3 đúng**, bắt riêng lỗi kênh theo kiểu ngoại lệ ở bản trước chưa đủ. Bản hiện tại phân xử theo bước. **R4 đúng**, controller tạo đơn ghi liên kết A/B khi cần. **R5 đúng** cho dời lịch, Payment kiểm boolean từ DB và Ticket kiểm số dòng UPDATE. Một worker Payment thấy broker confirm vẫn có thể mất lease trước khi ghi published_at. |

## Tuân thủ quy trình

LOG phiên 7 dòng 1295–1300 ghi rõ Claude đã đọc kết luận REVIEW-8 rồi mới tự kiểm. Đây là lệch §5.7 có ảnh hưởng tới cách dùng bằng chứng. Sự đồng ý R1–R4 của Claude không phải lần phát hiện độc lập thứ hai. Các test, bản ghi Ticket và đường CD ở trên cho phép đánh giá trực tiếp. LOG ghi Minh duyệt sửa, rồi duyệt push riêng. Commit cuối chạm đúng ba file chạy và hai file test của Payment. Mô tả vận hành ở hồ sơ RCA và body PR. Không thấy thay đổi ngoài phạm vi của bản sửa đó. STATE ghi đúng đầu chờ phản biện. Quyết định T-076 chờ Minh duyệt chữ đưa vào DECISIONS như STATE đã ghi.

Đã tìm tên các file đề nghị sửa trong manifest, danh sách SHA256, fingerprint và plan JSON được Git theo dõi ở hai repo, ngoài dữ liệu khóa. Không thấy ghim riêng cho các file đó. Đầu PR là mốc ghim cho mã. Trong hồ sơ bước 4, các file `kiem-manifest.txt` là kết quả kiểm manifest K8s. Với log dùng làm bằng chứng, so Git blob theo bộ lọc của repo bằng `git hash-object --path=<file> -- <file>` với `git rev-parse 6fb207132:<file>`. Khớp 8/8 gồm năm file của `sua-review-8/`, log Ticket nêu ở R1, bảng file và mô tả PR. `git diff 6fb207132 -- results/T-076/kiem-cuc-bo results/T-076/mo-ta-pr17.md results/T-076/bang-file-pr17.md` rỗng.

## Điều đã kiểm và thấy đúng

- `git ls-remote … refs/heads/main refs/pull/17/head` trả `f0a5d30` và `e19fc53`. `git rev-parse e19fc53^` trả `cd21f17`. `git diff --check f0a5d30 e19fc53` sạch. Đếm `git diff --name-only f0a5d30 e19fc53 -- ':(glob)**/src/main/**/*.java'` được 48 đường dẫn Java cho Minh đọc ở đầu này.
- GitHub Checks gắn đúng head SHA. Workflow CI có 13 job thành công, gồm tám job Maven và job tổng hợp Required. Job Frontend được bỏ qua. Đếm trên 14 mục job của cùng run trong sidebar Checks, ghép biểu tượng trạng thái **trước** liên kết của từng job. Truy vấn GraphQL trực tiếp trong phiên trả 401, REST trả 403 do hạn mức. Đã đọc trang Checks trực tiếp qua HTTPS và kiểm đầu PR qua Git. [GitHub Checks của PR](https://github.com/levanminh04/flash-ticket-platform/pull/17/checks) · [Lượt CI đã kiểm](https://github.com/levanminh04/flash-ticket-platform/actions/runs/46141549282) · [Required](https://github.com/levanminh04/flash-ticket-platform/actions/runs/46141549282/job/140969203375)
- `sua-review-8/verify/log/payment-service-verify.log` có `Tests run: 159` và `Tests run: 57`, cả hai 0 failure/error/skipped. Hai lớp liên quan có 8 và 2 test, đều nằm trong bộ vừa nêu. `payment-service-b16.log` ghi PASS cho 2 record mẫu. Số 2 ở dòng chuẩn bị của `verify/tien-do.tsv` là lần thăm dò sẵn sàng trong script. Hai dòng verify và B16 đều có mã thoát 0. LOG báo bốn failure khi áp test lên mã cũ. Không có log thô riêng của lượt đối chứng đó trong thư mục sửa, nên chỉ dùng kết quả trên mã mới và sự khác biệt có thể lần theo từ diff làm căn cứ độc lập.
- DT18 và cô đặt mục tiêu thu tín hiệu và áp dụng phương pháp lên hệ thống bán vé. H1/H4, cách vận hành reader và tiêu chí demo do Minh quyết theo SPEC. WHY-09 giải thích vì sao cần chuẩn quan sát sớm. WHY-89 giải thích cách dùng outcome. Bước này không đưa bộ nhãn, ca lỗi, điểm bất thường, bộ ứng viên hay hàm xếp hạng vào mã sửa. Không có lựa chọn phương pháp mới cần hợp thức hóa bằng WHY, cũng chưa có phép so sánh hiệu quả RCA. C2 tắt agent đã kiểm tĩnh trong 8 manifest và giữ file mẫu Secret theo main.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. Đã kiểm bản sửa REVIEW-8, CI và các đường xử lý có ảnh hưởng tới C4. Phần Payment và profile reader đạt trong phạm vi nêu ở bảng đối chiếu.
2. Chỉ tạo `tasks/T-076-pr17-otel-may-84/REVIEW-10.md`. Không commit, bình luận PR, truy cập các máy hay chạy thực nghiệm.
3. Bằng chứng quyết định là ca ACK Ticket đã lưu, log Payment, mã CD của đúng revision và trạng thái CI. Chưa có bằng chứng lỗi Ticket hoặc lỗi chuyển đổi đã xảy ra trên máy 84.
4. **Đề nghị Minh cho Claude đáp R1 và R2, ưu tiên sửa Ticket và bổ sung câu hướng dẫn CD.** Giữ nguyên kết quả các lượt cũ. Nếu Minh chấp nhận giới hạn R1, cần ghi rõ phạm vi ngữ nghĩa log chưa đạt. R2 có thể không áp cho lần phát nếu cụm đã qua chuyển đổi. Việc xác nhận reader hiện tại/dự định và đích rollback cần người giữ cấu hình cùng số liệu chỉ đọc ở bước 6 đã duyệt. Chi phí là lượt xác nhận và đọc trạng thái CD trước merge. Khi ấy mới phân biệt được cấu hình tương thích với trường hợp CD sẽ từ chối. Tiêu chí 1 còn phần Minh đọc và merge, tiêu chí 2 cần theo dõi 60 phút ở bước 7, tiêu chí 3–4 cần bản dựng và diễn tập theo bước 8–10. Tiêu chí 5 thuộc lượt runbook riêng. Chưa lấy các phần này làm kết quả P10.

## Prompt bàn giao cho người làm

Minh chọn gửi hoặc dừng. Phạm vi mặc định của lượt đáp là trong chat.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6).
- Công đoạn: người làm đáp REVIEW-10 về bước 5 Phần A, PR #17 trước merge, gồm đánh giá các đề xuất trong bản phản biện.
- Gói/cổng: P9/P10, tích hợp ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude là người làm, Codex là người phản biện.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}, results/T-076/{bang-file-pr17.md,mo-ta-pr17.md,kiem-cuc-bo/}, docs/architecture/B16-observability-baseline.md và deploy/observability/log.schema.json trong repo FlashTicket, git diff f0a5d30 e19fc53.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md đến REVIEW-6.md, REVIEW-8.md và REVIEW-10.md. REVIEW-7 và lượt dành cho REVIEW-9 thuộc runbook riêng.
- Code và kết quả liên quan: D:/Project/flash-ticket-platform, worktree D:/Project/ft-pr17-dung-lai tại e19fc53, sửa trên cd21f17, PR #17 https://github.com/levanminh04/flash-ticket-platform/pull/17, results/T-076/kiem-cuc-bo/sua-review-6/ và sua-review-8/. Chỉ đọc. Không vào máy 84, exp-app, obs. Không dùng subagent.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi Minh cấp quyền ghi cụ thể cho lượt đáp.

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

Người làm chỉ điền bảng này và LOG trong quyền được duyệt; không sửa nhận xét hay prompt của người phản biện. Thêm N1, N2… cho điểm tự tìm được, nêu CHẶN/KHÔNG CHẶN và bằng chứng. Để trống cột Minh quyết. Prompt của lượt đáp nằm trong mục LOG mới hoặc chat.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN | `TicketBusinessListeners.consume` (`e19fc53`): `basicAck` lỗi → `RabbitTelemetry` giữ mặc định `FAILED/MESSAGE_PROCESSING_FAILED`; dòng 189 `sua-review-6/verify/log/ticket-service-verify.log` ghi đúng `"outcome":"FAILED","reasonCode":"MESSAGE_PROCESSING_FAILED"` cho ca ACK lỗi. Reject/NACK lỗi cũng rơi về mặc định. Sửa (`e086fdc`): đặt `UNKNOWN/BROKER_COMMAND_FAILED` ngay trước mỗi lệnh kênh, kết cục cụ thể sau khi lệnh trả về; không đổi lệnh, thứ tự, ngoại lệ. Test: ca ACK lỗi có sẵn thêm kiểm log, thêm ca reject lỗi, NACK lỗi; hai ca reject/NACK thành công kiểm `REJECTED`/`RETRY`. Ba ca lỗi trượt trên mã `e19fc53`. | |
| R2 | Đúng; KHÔNG CHẶN | `deploy-k8s-service.sh` dòng 1092 (`finish` → `DISCOVERY_MIGRATION_FINALIZE_FAILED`) và 1109 (`unbridge` → `LEGACY_APPLICATION_UNDRAIN_FAILED`) thoát trước nhánh khôi phục. Sửa `mo-ta-pr17.md` mục Hoàn tác: thêm hai mã này và bước kiểm workload, con trỏ. Body PR đồng bộ khi Minh duyệt push. | |
| N1 | Người làm tự tìm khi kiểm R1; KHÔNG CHẶN; mã có sẵn trên main, PR không đụng | `user-service` `IdentityConsumer.receive` (mã main `e0c0dfb`): ghi `REJECTED`/`RETRY` **trước** `basicReject`/`basicNack`; `basicAck` lỗi thì không có dòng quyết định nào. Minh duyệt sửa cùng lượt ("Duyệt, cả user-service"). Sửa (`e086fdc`): `brokerCommand()` chạy lệnh, lỗi → `UNKNOWN/BROKER_COMMAND_FAILED` rồi ném lại; quyết định ghi sau khi lệnh trả về. Test 4 ca mới (ACK, NACK, reject lỗi; thành công); ba ca lỗi trượt trên mã `e19fc53`. | |
