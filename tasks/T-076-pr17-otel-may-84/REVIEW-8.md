# Phản biện T-076 — Kiểm bản sửa REVIEW-6 trước merge PR #17

- **Người phản biện** Codex. **Người làm** Claude. Ngày 28/11/2026.
- **Công đoạn** Bước 5 Phần A, SPEC bản 6, P9/P10, ngoài G0–G4. Đầu soát `cd21f17`, toàn PR `f0a5d30..cd21f17`, bản sửa `cd21f17^..cd21f17`. REVIEW-7 thuộc lượt soát runbook riêng.
- **Nguồn** AGENTS, STATE, SPEC, LOG, mẫu REVIEW, DT18 §2, hướng dẫn cô §1–3, MRP P9/P10, WHY-09/89/111, DECISIONS về môi trường và W2, LESSONS QT16–19. Đối chiếu B16 §3–6, schema log, bảng file, mô tả PR, cấu hình CD/CI, README các lượt kiểm cục bộ, log Maven/K8s và mã tại đầu soát.
- **Tự soát độc lập** Đọc nguồn, bản sửa và đầu ra gốc trước bảng phản hồi. Lần theo giao dịch Payment tới ACK/NACK, điều kiện ghi outbox, MDC tới phản hồi tạo đơn, script CD tới con trỏ sau phát và đường phục hồi khi lỗi. Sau đó mới đối chiếu REVIEW đến REVIEW-6 và diễn tiến duyệt trong LOG. Khi tiếp tục sau gián đoạn, đã kiểm lại đầu PR và nguồn Phần A. Thay đổi runbook bước A2 thuộc việc riêng của T-070.

## Kết luận chung

**Đề nghị Minh giữ PR ở draft.** CI đã đạt trên đúng đầu đã đẩy. Bản sửa đã nối được mã tạm với mã đơn và sửa kết cục khi dời lịch outbox mất hiệu lực. Trước khi chốt bước 5 còn một đường ACK/NACK ghi sai kết cục và hai chỉ dẫn CD sai trong mô tả PR.

## Các điểm

### R1. Kênh Spring đóng sau commit vẫn có thể ghi lỗi giao dịch — CHẶN kết luận C4 về ngữ nghĩa listener Payment

Trong `PaymentMessageListener.java:31–71`, service đã trả về sau commit. Nếu lệnh xác nhận `basicAck` ném `AlreadyClosedException` của RabbitMQ, bản mới ghi đúng `UNKNOWN/BROKER_COMMAND_FAILED`. Nhưng lệnh ACK có thể dừng ngay ở proxy kênh của Spring, trước khi tới client RabbitMQ. Trong Spring Rabbit 4.1.1, khi kênh đích đã đóng, proxy có nhánh ném `IllegalStateException` cho ACK/NACK và nhánh `AmqpException` cho kênh publisher callback đã đóng. Cả hai đi vào `catch (RuntimeException)` của Payment. Dòng log khi đó là `RETRY/TRANSACTION_UNAVAILABLE` mặc dù ở đường ACK giao dịch đã commit và listener chưa gọi NACK. Khi chính lệnh NACK ném một trong hai lỗi đó, việc yêu cầu giao lại cũng chưa được xác nhận. [Proxy Spring đúng phiên bản](https://raw.githubusercontent.com/spring-projects/spring-amqp/v4.1.1/spring-rabbit/src/main/java/org/springframework/amqp/rabbit/connection/CachingConnectionFactory.java) · [Đường gọi listener](https://raw.githubusercontent.com/spring-projects/spring-amqp/v4.1.1/spring-rabbit/src/main/java/org/springframework/amqp/rabbit/listener/SimpleMessageListenerContainer.java) · [Kiểm kênh của RabbitMQ 5.30.0](https://raw.githubusercontent.com/rabbitmq/rabbitmq-java-client/v5.30.0/src/main/java/com/rabbitmq/client/impl/AMQChannel.java)

**Bằng chứng phân xử.** Classpath của `TEST-*ListenerTelemetryTests.xml` trong `services/payment-service/target/surefire-reports/` có `spring-rabbit-4.1.1.jar` và `amqp-client-5.30.0.jar`. Đọc bytecode bằng `javap -p -c` thấy `SimpleMessageListenerContainer` lấy kênh từ consumer rồi truyền vào `executeListener`. Ở `CachingConnectionFactory$CachedChannelInvocationHandler.invoke`, các nhánh nêu trên tạo ngoại lệ và có đường ném lại `getTargetException()`. Đếm trong lớp listener ở đầu PR cho 5 annotation `@RabbitListener`, 5 catch mới, 5 điểm ghi RETRY, 5 lệnh ACK và 5 lệnh NACK. Hai test mới ở `ListenerTelemetryTests.java:131–176` ném ngoại lệ client trên mock `Channel`. Test dòng 74 lại dùng chính `IllegalStateException` cho xử lý nghiệp vụ thất bại và NACK thành công. Hai tình huống cần kết cục khác nhau dù cùng kiểu ngoại lệ. Lập luận về `RabbitTemplate` trong phản hồi của Claude áp cho đường gửi trong nghiệp vụ. Ở đây listener gọi trực tiếp phương thức trên `Channel`.

**Hệ quả và đề xuất.** Đây là lỗi phân nhánh xác định từ mã, chưa có số lần xảy ra trên cụm. WHY-89 xếp UNKNOWN và RETRY vào hai nhóm khác nhau, nên cách đọc tín hiệu có thể đổi. Chưa có phép đo ảnh hưởng lên hạng RCA. Đề nghị ghi kết cục ngay theo bước gửi lệnh ở năm đường xử lý. NACK yêu cầu giao lại trả về thành công mới ghi RETRY. Khi chính ACK/NACK ném lỗi, ghi UNKNOWN và ném lại nguyên lỗi. Giữ thứ tự commit, số lệnh, tham số và cách xử lý hợp đồng sai. Phép kiểm nhỏ nhất dùng cùng `IllegalStateException` ở hai vị trí trong fixture Payment. Sửa theo bước nhiều dòng hơn mở rộng danh sách catch, nhưng bắt rộng ở lớp ngoài sẽ làm sai cả ca lỗi nghiệp vụ đã NACK thành công.

### R2. Hướng dẫn áp điều kiện hai pod cho cả Event và Ticket — CHẶN dùng mục Hoàn tác để quyết merge

`results/T-076/mo-ta-pr17.md:52` liệt kê Booking, Event, Ticket và Payment rồi kết luận bản nền cho reader phải có hai pod. Body trên GitHub khớp văn bản này. Với Booking và Payment, Claude đọc đúng. `deploy/scripts/deploy-k8s-service.sh:441,463–468,975,1036–1038` ràng buộc hai pod khi dùng bản nền cho reader. Với Event, dòng 636 đòi HPA 1/1, dòng 585 và 684 đối chiếu bản writer cùng cấu hình và image. Với Ticket, dòng 764 đòi 1/1, dòng 778 kiểm profile cả hai revision và dòng 781 so image.

Có đối chứng dương trong `.github/scripts/test-k8s-deploy.py`. Event thiết lập writer một pod ở dòng 1197–1202, bật reader thành công và kiểm con trỏ ở 1249–1252. Ticket thực hiện hai bước tương ứng ở 1347–1353 và 1450–1453. Log có sẵn `sua-review-6/verify/k8s-py3/test-k8s-deploy.py.log`, dòng 4–7, ghi nhận các fixture theo từng service. Chúng kiểm điều kiện CD. Chúng không cung cấp trạng thái reader trên máy 84.

**Hệ quả và đề xuất.** Nhóm có thể loại một revision phục hồi hợp lệ, hoặc chuẩn bị hai pod cho một cấu hình mà CD từ chối. Sửa câu ở dòng 52 theo hai nhóm dịch vụ, giữ điều kiện tương thích và cùng image. Ở bước 6, dùng xác nhận của người giữ cấu hình cho **cả trạng thái đang chạy lẫn trạng thái định phát**. Một con trỏ writer-baseline có thể còn sau khi đã tắt reader. Phương án bỏ hoàn toàn số pod ngắn hơn nhưng thiếu thông tin khi đối chiếu đích rollback. Lỗi ở hướng dẫn, chưa có bằng chứng rollout nào thất bại vì nó.

### R3. Mô tả hứa CD tự phục hồi về cùng đích khi phát lỗi — CHẶN căn cứ hoàn tác của C4

`mo-ta-pr17.md:54–62` đã sửa đúng thời điểm đọc `previous` và thêm Payment. Nhưng dòng 61 nói “Phát lỗi giữa chừng: CD tự khôi phục về cùng đích này.” Có ba trường hợp phân biệt được trong `deploy/scripts/deploy-k8s-service.sh`:

| Thời điểm | Hành vi của CD |
|---|---|
| Kiểm cấu hình reader thất bại trước `apply_revision` | Script có thể dừng trước khi áp workload mới. Chưa có lần phục hồi workload để báo thành công. |
| Discovery đang chuyển từ Deployment cũ, bước áp/kiểm lỗi trước khi kết thúc migration | Dòng 1111–1117 gọi `restore` trên bản sao legacy. `migrate-k8s-discovery.py:222–227` đọc `legacy-deployment.json` và cần pod legacy còn đó. Nếu thành công thì phục hồi legacy. `compatible-previous` dùng trên đường hoàn tất migration, dòng 1090–1094 và `finish` dòng 192–218. Hai đích có thể khác hẳn workload và image. |
| Lỗi áp/kiểm thông thường | Dòng 1119–1142 chỉ *thử* phục hồi khi có đích khác target. Cả áp và kiểm lại phải thành công mới in `RESTORED_PREVIOUS`. Có nhánh `RESTORE_FAILED` và nhánh thiếu đích. Lỗi finalize tại dòng 1092 cũng có đường dừng riêng. |

Log fixture `sua-review-6/verify/k8s-py3/test-k8s-discovery.py.log` có cả phục hồi legacy và hoàn tất migration. Hai dấu vết thuộc những ca thử khác nhau. Có thể cụm đã xong migration từ trước, khi đó nhánh legacy không áp cho lần phát này. Ngay cả khi ấy, nhánh phục hồi thông thường vẫn có điều kiện thành công.

**Hệ quả và đề xuất.** Khi một lần phát lỗi, người trực có thể nhận nhầm workload đang phục vụ hoặc coi một lần thử phục hồi là thành công. Đề nghị sửa đúng đoạn hướng dẫn và body PR, mô tả trường hợp dừng trước áp, đích legacy khi đang migration, và trạng thái CD sau lần thử phục hồi. Giữ bước đọc lại image/profile trước khi Minh bấm rollback. Sửa mô tả đủ cho lỗi này. Sửa script CD sẽ đổi hành vi của nhóm ngoài phạm vi PR.

### R4. Log kết quả phát outbox Payment bỏ mã giao dịch đã có — KHÔNG CHẶN logic dời lịch, giới hạn phép truy theo B16

B16 §3–4 yêu cầu publisher khôi phục correlation từ bản tin và ghi mã khi đã gắn giao dịch. `MessagingServiceImpl.enqueue` lưu envelope trong transaction. `OutboxMessage.java:33,64–65` lưu `envelope.correlationId()` vào cột bắt buộc. Worker chạy theo lịch, nhận entity từ `claimOutbox`. Hai dòng `payment.outbox.result` ở `PaymentWorker.java:80–86,96–110` ghi messageId nhưng bỏ correlationId của dòng đang xử lý. `LogFields` cho phép trường này nhưng chỉ đọc MDC và trường được truyền, nên không tự khôi phục nó từ entity. Đối chứng ở `TicketOutboxPublisher.java:161–162` ghi cả hai. Hai dòng RETRY/UNKNOWN của fixture trong `sua-review-6/verify/log/payment-service-verify.log` có messageId và thiếu correlationId. Fixture dùng mock nên bằng chứng về **sự sẵn có của mã trong bản ghi thật** đến từ entity và hàm enqueue.

Với đường gửi thành công, có thể đối chiếu messageId với log consumer nếu có đủ hai đầu. Với lần gửi lỗi trước khi tới consumer, đường nối đó không được bảo đảm. `CorrelationData(messageId)` dùng cho broker confirm. Payload vẫn giữ mã giao dịch. Lỗi chỉ giới hạn việc tìm chính dòng kết quả của worker bằng correlationId.

**Đề xuất.** Trong hai dòng log, lấy correlationId từ entity hiện tại. Dùng fixture hiện có với hai UUID khác nhau để xác nhận giữ đúng vai trò của mỗi mã. Không cần đổi envelope, DB, AMQP hay dựa vào MDC dùng chung cho cả lô. Nếu Minh hoãn, ghi giới hạn này khi mô tả mức phủ B16. R5 của REVIEW-6 về cập nhật lịch vẫn đã xử lý.

## Đối chiếu các lượt trước

| REVIEW-6 | Phán định về phản hồi và bản sửa |
|---|---|
| R1 — đầu PR và CI | **Đúng, đã xử lý.** `git merge-base f0a5d30 cd21f17` trả đầu main đã nêu. `git range-diff 4d57225..f40b849 f0a5d30..cd21f17` cho 8 dấu bằng và 1 commit mới. REST xác nhận PR mở ở draft, đúng head/base. Run 46127267478 có cùng head/base, completed/success. Danh sách check trên head có 14 success, 1 skipped (Frontend). “Chưa push” mô tả mốc trước dòng 1206 của LOG. [CI của đầu đã soát](https://github.com/levanminh04/flash-ticket-platform/actions/runs/46127267478) |
| R2 — đích hoàn tác | **Đúng một phần.** Dòng 26–29 và 534/702/901/1088 của CD xác nhận C0 và các override writer của revision đích. Mục mới đã kể Payment và Discovery. Phần tổng quát hóa profile và phần khôi phục khi lỗi còn R2–R3 ở trên. |
| R3 — kênh đã đóng | **Đúng một phần.** Hai mock mới phân biệt được bản cũ và mới với ngoại lệ RabbitMQ. Proxy Spring còn phản ví dụ R1. |
| R4 — liên kết mã tạm | **Đúng, đã xử lý cho tạo đơn.** Filter Booking xác thực hoặc cấp mã tạm A trong MDC. Sau khi service trả OrderView, controller gọi `correlationLinked` trước khi trả header B. Khi A khác B, sự kiện có `correlationId=A, orderId=B`, các khóa đều qua danh sách cho phép. Cùng đường controller khi trả lại đơn cũ do idempotency. `OrderControllerTests.java:436–490` kiểm cặp A/B trên sự kiện và B trên header. Không cần một dòng trước reserve để suy ra A. |
| R5 — lease và retry | **Đúng, đã xử lý cho lần dời lịch.** Payment khóa dòng, trả false khi đã published hoặc attempt đã đổi. Worker chọn UNKNOWN khi false, RETRY khi true, chọn lời log theo broker đã confirm hay chưa. Ticket dùng số hàng UPDATE cho cả nhánh thành công và nhánh dời lịch. Test Payment dùng hai kết quả boolean. Test Postgres của Ticket đổi attempt trong lúc worker chờ confirm. Điều kiện ghi DB, mã lưu lỗi và lịch giữ theo diff. Riêng SUCCESS/BROKER_CONFIRMED của Payment chứng minh broker xác nhận, không chứng minh chính worker cũ vừa đổi published_at nếu `markPublished` trả sớm. |

Các điểm cũ dưới đây được xét theo thiết kế và quyền có hiệu lực lúc đó. “Đúng về thiết kế” chỉ có nghĩa SPEC bản 6 đã xử lý yêu cầu ở mức kế hoạch.

| Lượt | Đối chiếu từng điểm theo bằng chứng còn hiệu lực |
|---|---|
| REVIEW | **R1 đúng** về nguy cơ lẫn metric ở thiết kế cũ. Bản 6 tắt agent phía 84. **R2 đúng** về bộ lọc khóa của CD. Diff mẫu Secret hiện rỗng. **R3 đúng** về biên lọc. Kết quả thô của lượt bật thử còn email trong query. **R4 đúng** về nền và hoàn tác. C4/Q7/Q8 đã thay phép thử p95 bằng phạm vi rollout/GET được Minh duyệt. **R5 đúng**. Workflow Maven tra danh sách B16 và kiểm file mẫu, Assistant ngoài danh sách. **R6 đúng**. Workflow build giữ amd64/arm64 và truyền SERVICE_VERSION. **R7 đúng về quyền trong thiết kế mới**. SPEC §Phạm vi ghi chia quyền máy và repo theo bước. |
| REVIEW-2 | **N1 đúng**. Con trỏ previous phụ thuộc lần phát. C4 và R3 lượt này phân biệt các thời điểm. **N2 đúng có điều kiện** khi dùng chung Tempo. H1 chưa xuất từ 84. **N3 đúng**. Dấu email xuất hiện trong `ban-6/bat-ghi-de/phan-tich.txt` dù q đã che. **N4 đúng về kế hoạch cũ**. Nạp datasource mới thuộc đường mở rộng khi thật sự dùng nguồn production. |
| REVIEW-3 | **R1 đúng**. Công tắc nằm trong env tường minh ở manifest. **R2 đúng về thiết kế**. C4 giữ nền/GET và điều kiện dừng. **R3 đúng**. Quyền obs và máy tải của bước 9–10 đã ghi ở SPEC bản 6. **R4 đúng**. C6 đòi sự cố mới, đúng lớp và cửa sổ. **R5 đúng**. C5 để lựa chọn W7 cho lượt sau. **R6 đúng**. SPEC giữ cả message và stacktrace trong việc cần lọc. **R7 đúng về thiết kế**. Bước 8 yêu cầu kiểm cấu hình hiệu lực, tag, fixture và giới hạn hoàn tác dữ liệu. Các câu về vận hành Phần B vẫn cần kết quả của gói đó. |
| REVIEW-4 | **R1 đúng** về điều kiện đọc revision/digest, có thêm phân nhánh hiện tại ở R2–R3. **R2 đúng** về quyền ghi Q4 và tuyến hoàn tác bước 10, thể hiện ở SPEC §Phạm vi ghi. **R3 đúng**. C6 dẫn tiêu chí E5 và liên kết đúng ca từ t̂ tới dashboard. **R4 đúng**. C4 liệt kê log/filter/listener vẫn chạy khi agent tắt. |
| REVIEW-5 R1–R4 | **R1 đúng**. Fixture Booking gọi entry point Delivery. Log integration có 157 BookingPersistenceIT trong 173 ca integration. **R2 đúng về guard**. Tình trạng reader thực tế còn thuộc C4. **R3 đúng một phần ở lần đáp đầu, nay đã khép với tạo đơn** theo REVIEW-6 R4. **R4 đúng**. Đọc JSON `payment.callback-confirmed` trong log Payment mới thấy 4 UNKNOWN/UNKNOWN, 5 SUCCEEDED/SUCCESS, 1 FAILED/FAILED (stateAfter/outcome). |
| REVIEW-5 R5–R8 | **R5 đúng một phần**. Nhánh từ chối và NACK thành công phân biệt được, còn R1 của lượt này. **R6 đúng** ở manifest StatefulSet và ConfigMap Discovery. **R7 đúng một phần**. `EventLogCustomizer` loại span cha khi thiếu span_id, giữ ưu tiên span hiện hành. Muốn khẳng định Event khi bật agent, ghép log với span nhận ở lần kiểm tín hiệu bước 9 đã dự kiến. **R8 đúng** về lỗi đã nêu. Ticket phân biệt lỗi dữ liệu/DB, Payment nhớ confirm và đếm retry từ lần thứ hai. Phần dời lịch được phân xử ở REVIEW-6 R5. |
| REVIEW-5 R9, N1–N2 | **R9a đúng**. README đã đính chính build local thay ADD bằng COPY. Dòng ADD thật phụ thuộc lần build CD. **R9b đúng có giới hạn**. `sua-review-5/log/ticket-replica-run-it.log` ghi 25 ca đạt với fixture đã điều chỉnh. Log verify cả bộ có 4 failure và log đối chứng cấu hình main có 4 failure. **N1 đúng**. Quét configmap của 8 workload có agent ở đầu PR cho 0 khóa MDC tùy chỉnh. **N2 đúng về đính chính**. LOG dòng 605 trở đi ghi lại mốc 27/11. Các mốc xấp xỉ này không dùng để tính thời lượng. |

## Tuân thủ quy trình

- LOG phiên 7 ghi Minh duyệt ghi phản hồi và sửa R1–R5. Dòng 1206 ghi duyệt push riêng. Commit cuối có 11 file Java về listener, correlation, outbox và test. Mô tả PR trên GitHub khớp bản ở repo sau khi bỏ tiêu đề riêng và chuẩn hóa xuống dòng. Không có bằng chứng rằng Claude tự phát hành trước khi được duyệt.
- LOG phiên 7 tự ghi lệch §5.7: Claude đã đọc kết luận của REVIEW-6 trước khi tự soát. Vì vậy bảng nhận đúng R1–R5 không phải lần phát hiện độc lập thứ hai. Phản ví dụ proxy và profile Event/Ticket cho thấy hậu quả cụ thể nếu dùng sự đồng ý đó thay cho kiểm mã.
- Khi bàn giao Minh đọc, dùng danh sách `git diff --name-only f0a5d30 cd21f17 -- ':(glob)**/src/main/**/*.java'`. Đếm được **48** đường dẫn, so với **46** ở đầu trước sửa theo cùng quy tắc. Hai đường thêm là interface và implementation `MessagingService` của Payment. Số 44 trong bước 5 là mốc của diff cũ. Dùng lệnh trên tại đầu cần duyệt là đủ, không cần sửa lại SPEC đã khóa.
- DT18 và cô yêu cầu thu tín hiệu và áp dụng phương pháp sau nghiên cứu. H1/H4, số pod, công tắc agent, hợp đồng log và ngưỡng demo là những lựa chọn kỹ thuật hoặc quyết định của Minh. WHY-09 giải thích nhu cầu nhận telemetry sớm, WHY-89 giải thích cách đọc outcome. Chúng không chứng minh thay đổi collector hoặc log làm hạng RCA tốt hơn. Không thấy điểm mới chọn cơ chế RCA, chọn ngưỡng theo kết quả hay đưa nhãn tiêm vào tính điểm trong bản sửa. Chữ quyết định T-076 ở DECISIONS còn chờ Minh như STATE ghi. Căn cứ quyền thực hiện ở đây là SPEC và mục duyệt trong LOG.
- Các file đề xuất chạm ở R1–R4 thuộc mã nguồn/test theo Git và bản mô tả PR. Tìm tên trong manifest, JSON plan và fingerprint được theo dõi của hai repo không thấy bản ghim riêng cho các file đó. Sửa Java/test sẽ đổi đầu PR và cần CI của đầu mới. Sửa nguồn mô tả và đồng bộ body chỉ đổi tài liệu. Đề xuất giữ kết quả ở `sua-review-6/` gắn với đầu đã kiểm.

## Điều đã kiểm và thấy đúng

- **Toàn vẹn.** SHA-256 của SPEC khớp tiền tố sau duyệt trong LOG. Khi tiếp tục, dùng `git ls-tree -r 75e239c2a` trên thư mục task, `results/T-076/kiem-cuc-bo`, bảng file, mô tả PR, AGENTS và mẫu prompt. So từng blob với `git hash-object --stdin-paths` được 217/217 khớp. Hai file `kiem-manifest.txt` là kết quả kiểm manifest K8s. Lượt này dùng cây Git để đối chiếu nội dung đã lưu. `git diff --check f0a5d30 cd21f17` sạch.
- **Kiểm cục bộ đã lưu.** Trong `results/T-076/kiem-cuc-bo/sua-review-6/verify/log/`, lọc dòng tổng `[INFO] Tests run:` kết thúc bằng số skipped. Payment verify 157 + 57, Ticket verify 229, Booking verify 457, Booking rca-test 466, Booking integration 457 + 173, TicketPostgresIT 23. Các tổng này có failures/errors/skipped bằng 0. Ba `*-b16.log` đều PASS với hai mẫu/service. Các mẫu kiểm schema; ý nghĩa nghiệp vụ được đối chiếu riêng ở trên.
- **Hạ tầng và CI.** Lượt K8s đầu có 3 log báo thiếu module yaml. Lượt sau ghi 4 mã thoát 0 trong `verify/k8s-py3/tien-do.tsv`. CI được đọc qua REST công khai bằng `gh api -H 'Authorization:'`, với `pulls/17`, `actions/runs/46127267478` và `commits/cd21f17/check-runs?per_page=100`. Các nguồn này xác nhận CI đúng revision và không cung cấp kết quả triển khai lên máy 84.
- **Cấu hình thực thi.** Quét các Deployment/StatefulSet có `OTEL_AGENT_ENABLED` được 8 workload đặt false trong env, có host từ spec.nodeName và production trong ConfigMap. Danh sách B16 gồm 7 service. Diff `deploy/k8s/examples/` so với main rỗng. Các quan sát này đủ để đọc cấu hình nguồn của Phần A.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. Đã kiểm độc lập bản sửa và phân xử phản hồi REVIEW-6. R1, R4 và R5 của **REVIEW-6** đã xử lý trong phạm vi nêu ở bảng. R2 và R3 của **REVIEW-6** mới đúng một phần.
2. File duy nhất của lượt là `tasks/T-076-pr17-otel-may-84/REVIEW-8.md`. Lượt này chỉ đọc hai repo và GitHub ngoài việc tạo bản phản biện này. Không chạy Maven, Docker, thực nghiệm RCA hoặc truy cập các máy triển khai.
3. CI đúng cặp revision đã xanh. Mã proxy Spring, fixture CD, log gốc, hợp đồng B16 và điều kiện ghi DB là căn cứ cho bốn điểm trên.
4. **Đề nghị tiếp tục phản biện có mục tiêu và giữ draft.** Đề nghị Minh duyệt cho Claude xử lý R1, hiệu chỉnh hai câu vận hành R2–R3 và bổ sung trường có sẵn ở R4 trong cùng lượt. Mặt trái là có một đầu Java mới cần CI. Nếu hoãn R4, ghi giới hạn truy theo mã giao dịch. Có thể chấp nhận giới hạn phân loại R1 thay cho sửa nếu Minh quyết rõ, nhưng khi ấy chưa thể nghiệm thu lời khẳng định về kênh đóng. Việc sửa tài liệu R2–R3 chỉ cần đối chiếu script và fixture sẵn có.

**Phần còn mở.** Tại giờ merge, nhóm giữ cấu hình mới phân xử được reader thực tế và dự định ở từng service. Minh dùng xác nhận đó cùng nền C4, revision, digest và sức chứa để quyết định phát hay dời. Chi phí là lần phối hợp và đọc C4 đã định, có thể có một lượt CD của nhóm nếu thực sự phải về writer trước. Tiêu chí 1 còn Minh đọc và merge. Tiêu chí 2 thuộc 60 phút theo dõi ở bước 7. Tiêu chí 3–4 cần bản ghim, tín hiệu và diễn tập trên exp-app ở bước 8–10. Tiêu chí 5 có hồ sơ mở rộng với lượt soát riêng. Các kết quả triển khai, mức phủ ba tín hiệu và hiệu quả phát hiện/xếp hạng chưa thể suy từ CI hay từ lượt này.

## Prompt bàn giao cho người làm

Minh chọn gửi prompt hoặc dừng. Quyền ghi trả lời REVIEW-8 chưa được cấp.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/SPEC.md bản 6.
- Công đoạn: người làm đáp phản biện REVIEW-8, bước 5 Phần A của PR #17.
- Gói/cổng: P9/P10, tích hợp ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}, results/T-076/{bang-file-pr17.md,mo-ta-pr17.md}, results/T-076/kiem-cuc-bo/ và README từng lượt, B16 và deploy/observability/log.schema.json trong repo FlashTicket, git diff f0a5d30 cd21f17.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md, REVIEW-5.md, REVIEW-6.md và REVIEW-8.md trong cùng thư mục. REVIEW-7.md dành cho runbook riêng.
- Code và kết quả liên quan: D:/Project/flash-ticket-platform và worktree D:/Project/ft-pr17-dung-lai tại cd21f17, git show cd21f17, git range-diff 4d57225..f40b849 f0a5d30..cd21f17, PR #17, CI 46127267478, results/T-076/kiem-cuc-bo/{sua-review-5,sua-review-6}/. Chỉ đọc. Không vào máy 84, exp-app, obs. Không dùng subagent. Phần T-070 và runbook bước A2 thuộc lượt riêng.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, gồm đối chiếu các đề xuất trong REVIEW-8. Chỉ ghi bảng phản hồi, LOG hoặc STATE nếu Minh duyệt rõ phạm vi ở lượt đáp.

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

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN | `spring-rabbit-4.1.1.jar`, lớp `CachingConnectionFactory$CachedChannelInvocationHandler` có chuỗi `Channel closed; cannot ack/nack` (đọc bằng `strings`): proxy Spring ném `IllegalStateException` trước khi tới client RabbitMQ, rơi vào `catch (RuntimeException)` → `RETRY`. Bản sửa REVIEW-6 R3 của người làm bắt theo kiểu lỗi (`ShutdownSignalException`) nên chưa đủ; lập luận về `RabbitTemplate` chỉ áp cho đường gửi, không cho lệnh gọi thẳng trên `Channel`. Sửa: `RabbitTelemetry.track(channel)` bọc `Channel` (proxy JDK) ghi lại bước: `basicAck`/`basicNack` ném lỗi → `UNKNOWN/BROKER_COMMAND_FAILED`; `basicNack(requeue=true)` trả về bình thường → `RETRY/TRANSACTION_UNAVAILABLE`; còn lại giữ `FAILED`. Năm hàm bọc gọi hàm trong với `telemetry.track(channel)`; không đổi chữ ký hàm trong (test tích hợp gọi trực tiếp), lệnh, tham số, thứ tự. Test mới: `IllegalStateException("Channel closed; cannot ack/nack")` ở ACK sau commit và ở NACK → `UNKNOWN`; test cũ cùng `IllegalStateException` ở bước nghiệp vụ + NACK thành công → `RETRY`. Hai test mới trượt trên mã `cd21f17`. | |
| R2 | Đúng; CHẶN | `deploy-k8s-service.sh` dòng 636 (Event) và 764 (Ticket) đòi HPA 1/1; điều kiện bản nền 2 Pod chỉ ở Booking/Payment. Sửa câu điều kiện trước merge trong `mo-ta-pr17.md` theo hai nhóm, thêm xác nhận trạng thái reader đang chạy và định phát. | |
| R3 | Đúng; CHẶN | Dòng 1111–1142: `RESTORED_LEGACY_DISCOVERY`/`DISCOVERY_RESTORE_FAILED`, `RESTORED_PREVIOUS` chỉ khi áp và kiểm lại đạt, `RESTORE_FAILED`, `NO_PREVIOUS_K8S_REVISION`; lỗi kiểm cấu hình có thể dừng trước khi áp. Sửa dòng "CD tự khôi phục" thành ba trường hợp và bước đọc workload thật. | |
| R4 | Đúng; KHÔNG CHẶN | `PaymentWorker` hai dòng `payment.outbox.result` không có `correlationId`; entity có `getCorrelationId()`. Sửa: thêm trường từ entity; test dùng hai UUID khác nhau cho `messageId` và `correlationId` (trượt trên `cd21f17`). | |
