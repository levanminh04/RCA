# Phản biện T-076 — PR #17 trước merge

- **Người phản biện:** Codex. **Người làm:** Claude. **Ngày:** 27/11/2026.
- **Công đoạn:** bước 5 Phần A, soát kết quả theo SPEC bản 6. P9/P10, ngoài G0–G4. Lượt 5. Hai đầu diff FlashTicket là `6b77144..2a275b5`.
- **Nguồn:** AGENTS, STATE, SPEC, mục cuối LOG T-076, bảng file, mô tả PR, ba README kiểm cục bộ và đầu ra tương ứng. Đã đối chiếu B16 §3–7, DT18-NV1–NV3, hướng dẫn cô ngày tiếp nhận 23/09, MRP P9/P10, WHY-89, DECISIONS về repo lab và pin thử nghiệm, LESSONS QT5/QT18/QT19. Bốn bản phản biện trước và bảng đáp được dùng để đối chiếu sau khi tự soát nguồn.
- **Tự soát độc lập:** đọc diff, luồng CD, mã gateway/Booking/Payment/Ticket/Event, cấu hình quan sát, đầu ra Booking và CI trên đúng đầu PR. Diễn giải dưới đây phân biệt hành vi chứng minh được bằng mã, phép đo trên laptop và trạng thái chưa đọc trên máy 84.

## Kết luận chung

**Đề nghị giữ PR ở draft và tiếp tục phản biện trước merge.** CI đạt và cấu hình tắt agent đúng trên bảy Deployment. Tuy nhiên, đổi phương thức nhận RabbitMQ làm hỏng hai đường kiểm tích hợp hiện hữu. Kế hoạch triển khai cũng bỏ sót điều kiện cùng digest khi replica đang bật. Một số sự kiện B16 sai kết cục hoặc mất liên kết ngay khi agent tắt. Đây là các vấn đề của chính đầu ra bước 5.

## Các điểm

### R1. Kiểm tích hợp Booking vẫn gắn vào phương thức cũ — CHẶN nghiệm thu PR

`SalesConfigurationListener.java:21–31` chuyển `@RabbitListener` sang phương thức nhận cả envelope và bản tin thô. `BookingPersistenceIT.java:890,906` vẫn lấy phương thức một tham số rồi gọi `getAnnotation(RabbitListener.class).ackMode()`. `EventCancellationListener` và phép kiểm ở dòng 8806, 8944 có cùng lỗi. Đọc bằng `javap -v -classpath services/booking-service/target/classes` trên hai lớp xác nhận annotation chỉ ở phương thức có hậu tố `Delivery`. Khi tới hai lệnh đọc annotation, giá trị là null. Đây là lỗi xác định được ở test theo mã và bytecode. Lượt này không ghi nhận một lần chạy toàn bộ suite bị lỗi.

Ba điểm dựng endpoint khác trong cùng file (4748, 5187, 6721) cũng gọi hàm cũ và đi vòng qua phần bọc mới, dù chúng tự đặt AUTO. CI thường và profile `rca-test` xanh phù hợp với bằng chứng này vì Failsafe cho `BookingPersistenceIT` nằm ở profile `integration` (pom Booking, dòng 293–302). Phép kiểm queue giả trong `ObservabilityTests` gọi trực tiếp lớp telemetry.

**Sửa tối thiểu đề xuất:** cho các fixture broker trỏ vào đúng chữ ký được Spring đăng ký. Giữ phép kiểm ACK sau commit, giao lại và đưa vào hàng đợi lỗi. Chạy lại các ca tích hợp bị tác động trên PostgreSQL/RabbitMQ thử của Booking sau khi Minh duyệt. Chỉ bỏ assertion annotation sẽ làm test xanh trong khi vẫn bỏ qua đầu vào production.

### R2. Reader có thể chặn phát image mới trước cả bước rollback — CHẶN quyết định merge tự triển khai

`deploy/scripts/deploy-k8s-service.sh:393–408,467–494` yêu cầu revision Booking chỉ dùng writer có **cùng digest** với image ứng viên khi bật reader. Khi chuyển từ reader đang hoạt động sang writer, script cũng so hai revision. Event có kiểm tương ứng tại 523–545, 640–662. Ticket có tại 737–750, 837–861. Các kiểm này chạy **trước** `apply_revision` ở dòng 867. README K8s dòng 77–78, 87, 96 cũng yêu cầu baseline writer cùng image. Fixture Booking trong `.github/scripts/test-k8s-deploy.py:663–675` thay digest và yêu cầu CD từ chối. Đây là hành vi đúng của CD.

PR dựng lại image của ba service này. Nếu reader đang bật hoặc cấu hình phát hành yêu cầu bật reader, baseline gắn với image cũ không thỏa cho digest mới. Kể cả đổi flag cùng lúc đổi image cũng có thể bị chặn. Chỉ biết `current`, `previous`, `writer-baseline` tồn tại như mục Hoàn tác trong mô tả PR chưa xác nhận điều kiện phát. File baseline có thể còn sau khi tắt reader. Matrix CD có `fail-fast: false`, nên một service bị từ chối vẫn có thể để cụm chạy lẫn các phiên bản. PR revert cũng phải qua CD.

**OPEN ở bước 6:** chưa biết trạng thái reader hiện hành và dự kiến phát của từng service. Nếu đang writer-only và tiếp tục writer-only thì điều kiện trên không chặn đường đổi image thông thường. Đề nghị Minh lấy xác nhận trạng thái flag từ người giữ cấu hình, không lấy giá trị Secret, và đối chiếu revision/digest trong lần đọc C4 đã duyệt. Nếu reader đang bật, hẹn nhóm về writer trên digest hiện tại trước, phát image mới writer-only, rồi để nhóm quyết thời điểm bật lại reader với baseline mới. Chi phí là thêm lượt CD và một khoảng dùng writer. Nếu nhóm chưa có lịch hoặc không xác nhận được, dời merge. Không đề xuất nới guard.

### R3. Gateway và Booking không nối được log tạo đơn bằng mã giao dịch — CHẶN kết luận B16 cho luồng mua vé

B16 §3 quy định từ khi tạo được đơn, trả `X-Correlation-Id = orderId` và nối correlation tạm với đơn. Với request mới mang mã A, gateway chuyển A vào Booking. `CorrelationFilter.java:21–39` của Booking đưa A vào ngữ cảnh log MDC. Khi reserve thành công, `OrderServiceImpl.java:2034–2039` và `BusinessTelemetry.java:14–26` ghi cả `orderId` và `correlationId` bằng mã đơn B. Giá trị cấu trúc B thắng giá trị A trong MDC (`LogFields.java:65–78`). `OrderController.java:73–79` chỉ trả Location và body. Gateway vì thế trả và ghi A theo nhánh dự phòng (`CorrelationIdFilter.java:51–58,100–111`). Không có dòng chuyển A → B trong đường này. Hai phía còn sinh `requestId` riêng. Một phần thiếu ở controller đã có trên main, nhưng log mới của PR không thực hiện liên kết mà B16 yêu cầu.

Cũng có sai lệch mới với request lỗi tới Booking trực tiếp khi thiếu header hợp lệ. Filter tạo A. `GlobalExceptionHandler.java:92–102,123–133` sinh B, thấy MDC đã có A nên log dùng A, còn header và body gửi về B. Khi gateway đã gửi UUID hợp lệ, hai bên dùng cùng UUID cho nhánh lỗi này.

**Đề xuất:** dùng chung mã đã chuẩn hóa cho phản hồi lỗi và MDC. Khi tạo đơn thành công, trả B và ghi liên kết với mã tạm ở bước biết chắc orderId. Kiểm một lần tạo đơn và một lỗi không có header qua entry point tương ứng, so header/body/log. Không suy ra giao dịch lưu đơn sai từ lỗi liên kết này.

### R4. Callback VNPay chưa rõ kết quả được ghi SUCCESS — CHẶN kết luận đúng nghĩa log thanh toán

`CinemaVNPayServiceTest.java:230–239` có ca chữ ký hợp lệ, phản hồi có mã 07, trạng thái chưa phân xử. `PaymentService.java:205–257` lưu `UNKNOWN`, để `finishedAt=null`, trả ACK giao thức `RspCode=00`, rồi log qua `BusinessTelemetry.committed` mà không truyền outcome riêng. `BusinessTelemetry.java:28–35` của Payment chỉ nhận trạng thái `FAILED` làm thất bại, còn lại mặc định `SUCCESS`. Do đó bản ghi có thể mang `stateAfter=UNKNOWN, outcome=SUCCESS`. Cùng đường đó, `stateAfter=FAILED` lại làm outcome thành FAILED dù callback cũng đã được xác thực. Diễn giải “SUCCESS chỉ nghĩa là nhận được callback” không giải thích được cả hai nhánh. B16 §4 và WHY-89 phân biệt hai giá trị này khi đọc log.

**Đề xuất:** cho sự kiện kết quả thanh toán ánh xạ rõ `SUCCEEDED / FAILED / UNKNOWN` sang ba outcome tương ứng. Nếu cần biểu diễn đã nhận callback, giữ thông tin đó ở mã lý do hoặc sự kiện xác thực riêng. Kiểm bản ghi của ca không rõ đã có cùng một ca thành công và một ca thất bại. Giữ nguyên quyết định tiền, trạng thái DB và ACK VNPay.

### R5. Listener gom từ chối và giao lại vào FAILED — CHẶN kết luận C4 về ngữ nghĩa RabbitMQ

Trong Payment, năm phương thức `*Delivery` chỉ đặt SUCCESS sau khi hàm con trả về. Năm nhánh `basicNack(tag,false,true)` tại `PaymentMessageListener.java:51,81,110,139,169` yêu cầu giao lại rồi ném lỗi. `RabbitTelemetry.close()` vì thế phát mặc định `FAILED/MESSAGE_PROCESSING_FAILED`. Lỗi hợp đồng đưa sang `MessageConversionException` cũng nhận cùng cặp trường. Trong Booking, ví dụ `SalesConfigurationListener.java:21–51`, dữ liệu không hợp lệ đi qua `AmqpRejectAndDontRequeueException` nhưng log đóng scope cũng phát FAILED. Ticket làm được điều phân biệt này ngay trên luồng thật tại `TicketBusinessListeners.java:66–88`. Việc khôi phục MDC trong `finally` và ACK sau service trả về là đúng, chúng không sửa giá trị outcome.

**Đề xuất:** ghi RETRY sau NACK yêu cầu giao lại thành công, REJECTED khi quyết định từ chối đã biết. Tách trường hợp lệnh broker thất bại và chưa rõ kết cục. Giữ cơ chế ném exception, số lần ACK/NACK và chính sách hàng đợi hiện có. Dùng listener thật để so đồng thời lệnh broker, log và MDC sau khi thoát. Không có bằng chứng mất bản tin trên máy 84.

### R6. Discovery gắn log production vào host giả — CHẶN tiêu chí định danh C4 nếu áp cho Discovery

Hai danh sách bảy service khác nhau đúng một thành viên. Discovery thuộc danh sách B16 và được CD build lại. Assistant có cấu hình K8s cho agent nhưng nằm ngoài hợp đồng log. `deploy/k8s/discovery-server/statefulset.yaml:46–63` lấy tên pod, IP, UID và ConfigMap. Cả hai manifest Discovery thiếu `HOST_ID` và `ENVIRONMENT`. `infrastructure/discovery-server/docker-entrypoint.sh:6–8` xuất `local-test` và `local`. `LogFields.java:92–96` dùng chính hai giá trị đó. Vậy ngay nếu pod chạy khỏe, log Discovery theo manifest vẫn sai host và môi trường. README đã ghi Discovery chưa có cấu hình agent. Giới hạn ấy không giải quyết việc log B16 vẫn chạy. Discovery hiện mặc định tắt agent và StatefulSet không nạp Secret của service.

**Đề xuất:** Minh duyệt bổ sung đúng metadata `HOST_ID=spec.nodeName` và `ENVIRONMENT=production` cho Discovery, hoặc ghi rõ ngoại lệ của C4 và hệ quả khi lọc log theo host/môi trường. Nếu muốn cam kết “tắt cứng” cho cả tám image, chốt riêng cờ false trong StatefulSet. Không cần thêm đường xuất dữ liệu để sửa định danh.

### R7. Event có thể ghi mã span cha vào trường span hiện tại — CHẶN kết luận P9a về nối log–trace cho đường này

Với request có `traceparent` hợp lệ khi agent tắt, `event_service/web/CorrelationFilter.java:46–50` chép mã span phía gửi vào MDC `spanId`. `EventLogCustomizer.java:78–85` ưu tiên `span_id`, nhưng khi vắng khóa này lại chấp nhận `spanId` chỉ theo độ dài và mẫu hex. Khi đó log Event chỉ vào span bên gọi. Phần chép header đã tồn tại ở main. PR viết lại bộ xuất, tiếp tục nhận trường này, trong khi comment nói ưu tiên span đang hoạt động. Ca thử đồng thời gán hai khóa khác nhau chưa bao phủ trường hợp chỉ có span cha. ConfigMap Event còn đặt tên khóa agent là `spanId`; giả lập hai khóa trong test không chứng minh thứ tự ghi thực tế khi bật agent.

**Đề xuất:** giữ trace context để truyền tiếp, chỉ xuất `spanId` hiện tại khi xác định được span thực thi. Kiểm nhánh chỉ có header và nhánh có span hiện hành khác span cha. Chưa có căn cứ định lượng số liên kết sai hoặc tác động lên hạng RCA.

### R8. Bản ghi outbox gán nguyên nhân ở broker cho lỗi ngoài broker — KHÔNG CHẶN giao dịch, chặn dùng reasonCode để quy nguyên nhân

`TicketOutboxPublisher.java:82–89,115–145` gom trường hợp schema đã lưu sai, lỗi đọc dữ liệu và lỗi DB ghi sau broker confirm vào cùng catch runtime rồi xuất `BROKER_UNAVAILABLE`. Payment cũng có thể đã nhận ACK và qua kiểm returned rồi mới lỗi tại `markPublished` (`PaymentWorker.java:72–99`), nhưng log lại báo `BROKER_DELIVERY_UNCONFIRMED` nếu nhánh dời lịch chạy xong. Phân loại nội bộ trong catch có phần kế thừa main. PR đưa nó ra log RCA như lý do của kết cục. Lỗi sau confirm không chứng minh broker mất kết nối. Thêm nữa, `retryCount` lấy số **lần thử**, nên ngay lần đầu thành công cũng có thể ghi 1 (`OutboxMessage.java:36`, `MessagingServiceImpl.java:60`, Ticket `TicketOutboxPublisher.java:149,174`, `TicketDeliveryWorker.java:161,187`).

**Đề xuất:** ghi mã trung tính nếu chưa biết nguyên nhân, hoặc phân biệt theo bước thực sự thất bại. Đổi số lần thử sang số lần thử lại khi ghi `retryCount`. Các sửa này chỉ cần đổi telemetry, giữ lịch retry và điều kiện cập nhật DB.

### R9. Hai giới hạn của hồ sơ kiểm sau rebase — KHÔNG CHẶN riêng, cần ghi đúng mức bằng chứng

- `results/T-076/kiem-cuc-bo/README.md` §2 và `agent/build-image.sh:4` nói CI GitHub chạy dòng `ADD` tải agent gốc. Local dùng COPY sau khi kiểm checksum. Trong run PR, job Maven Booking bỏ qua `Upload JAR for the image build`. Workflow CI không gọi publish. Phép kiểm rollout dùng Dockerfile fixture tự sinh (`test-k8s-rollout-hooks.py:158–174`). Digest asset upstream tại tag v2.33.1 khớp pin trong Dockerfile. Điều còn thiếu là bằng chứng BuildKit chạy dòng ADD từ môi trường CD. Đề nghị đính chính câu về CI, không yêu cầu chạy lại Maven hay coi release asset bị sai.
- LOG dòng 600–603 ghi Minh duyệt cả `test-ticket-replica.sh` nếu chạy được local. README sau rebase nói bỏ vì ngoài CI và PR không sửa code replica. Fixture có hỗ trợ Git Bash/Windows và cần Docker, PostgreSQL, RabbitMQ, Maven. Kết quả `TicketPostgresIT` kiểm một đường khác. Không có log thử hoặc điều kiện cụ thể làm fixture không chạy được. Đề nghị người làm đối chiếu khả năng chạy trong môi trường được phép rồi hoàn thành phần đã duyệt hoặc trình Minh chấp nhận bỏ với phạm vi rõ. Không dùng fixture này thay bằng chứng về trạng thái reader thật ở R2. Reviewer không phát fixture vì nó tạo file và container.

## Đối chiếu các lượt trước

Đánh giá dưới đây áp cho nhận xét tại bản SPEC lúc đó và phản hồi của Claude. “Đúng” ở một thiết kế lịch sử không có nghĩa là hạ tầng đó đã được dựng.

| Lượt, điểm | Đánh giá và bằng chứng riêng |
|---|---|
| 1 R1 | Đúng. Adapter `src/m1/adapter_flashticket.py:24–36` cộng các series theo service; gateway lab có file capture. Bản 6 tắt xuất từ 84. Chỉ kết luận không có đường trộn mới do agent trong cấu hình này. |
| 1 R2 | Đúng về hạn chế CD. Danh sách cho phép khi dựng Secret nằm trong `deploy-k8s-service.sh:309–345`; Discovery dùng ConfigMap. CA/token từng pod đã rút khỏi Phần A. R6 là vấn đề định danh riêng. |
| 1 R3 | Đúng. Ở lab `c1da15f` lớp lọc nằm trong `agent-docker-host.yaml`; gateway có capture. Việc giảm dữ liệu trong agent vẫn chưa bao phủ query tùy ý, xem đối chứng bên dưới. |
| 1 R4 | Đúng cho bản 1. Bản 6 có Q7/Q8 và lịch quan sát 60 phút cho agent tắt. Giới hạn p95 đã khai. Nhận định đường lui đủ sau rebase chỉ đúng một phần, xem R2. |
| 1 R5 | Đúng, đã sửa điểm CI. Workflow cũ ở `bb84d64` chỉ loại Keycloak, bản mới kiểm theo danh sách và Assistant nằm ngoài. |
| 1 R6 | Đúng, đã sửa. `f178870:_deploy-service.yml` đã có hai kiến trúc; diff giữ chúng, đưa SHA vào build arg. Khả năng build hai kiến trúc trong CD khác với đã build trong run PR. |
| 1 R7 | Đúng về pin và quyền lab. Bản 6 chỉ dùng lab theo commit và duyệt riêng phần vận hành; lượt này không kiểm máy. |
| 2 N1 | Đúng. CD đọc `previous` rồi so digest; con trỏ có thể đổi khi phát tiếp. Q10 dự phòng đã được duyệt. Cùng digest còn là tiền điều kiện phát mới theo R2. |
| 2 N2 | Đúng. `check_purchase_journey.py:107–119` trên lab lọc service/route, không lọc environment. Bản 6 hoãn ghép tuyến 84, nên không có yêu cầu chạy phép trộn ở bước 5. |
| 2 N3 | Đúng. Ba span thử còn email/phone ở query khi chỉ che danh sách. Kiểm sau Collector không thay bằng chứng trước bộ lọc. |
| 2 N4 | Đúng cho thiết kế hai datasource. Provisioning lab còn `serviceMap.datasourceUid=prometheus`. Bản 6 chưa thêm datasource 84, nên không cần reload trong Phần A. |
| 3 R1 | Đúng trong phạm vi bảy Deployment. Đã kiểm giá trị cứng và đối chứng Booking. Discovery thuộc StatefulSet và dùng mặc định image. |
| 3 R2 | Đúng. Q7/Q8 đã có ngưỡng, hành động và giới hạn GET. Diff ConfigMap không thêm biến loại Spring; không suy từ đó ra code Java giữ nguyên ngữ nghĩa. |
| 3 R3 | Đúng. Q4 xác nhận điều khiển tải từ obs. Bản 6 cấp phạm vi riêng cho bước 9/10, yêu cầu runbook mới và quyết định T-070. |
| 3 R4 | Đúng. C6 hiện xét sự cố đang mở và cửa sổ t̂ theo E5, khắc phục khả năng nhận nhầm sự cố cũ ở thiết kế. |
| 3 R5 | Đúng. C5 và Q5 chỉ ghim bản demo; không đưa ra lựa chọn W7. |
| 3 R6 | Đúng. README nhánh mục mở rộng yêu cầu xử lý cả message và stacktrace của exception; giá trị này chưa được kiểm trên tuyến production tương lai. |
| 3 R7 | Đúng. Bước 8 nêu ngrok, bản Compose hiệu lực, fixture, image cũ và giới hạn phục hồi dữ liệu. Đây là chuẩn bị của Phần B. |
| 4 R1 | Đúng với revision trước rebase. Bản 6 và LOG bổ sung con trỏ cần đọc. Phản hồi chỉ giải quyết một phần trên main mới vì guard cùng digest chạy trước lúc apply (R2). |
| 4 R2 | Đúng. Q4 và `trien-khai-e5.md` cho thấy hai tuyến khác nhau. Bản 6 đã ghi phạm vi obs bước 9 và runbook theo lab hiện hành cho bước 10. |
| 4 R3 | Đúng. Đối chiếu C6 trực tiếp với `results/T-073/khai-truoc-e5.json#/tieu_chi/ket_qua_chuc_nang` và `#/N`: đúng cửa sổ, mã ca, cờ kiểm, đích dashboard và hạn. Kết quả trên bản demo mới còn phụ thuộc lượt chạy. |
| 4 R4 | Đúng. SPEC ghi rõ B16 chạy khi agent tắt; R1, R3–R8 xác định phần mà test cấu trúc log và GET không phân xử được. |

## Tuân thủ quy trình

SPEC bản 6 và dòng T-076 trong STATE khớp vai trò. LOG ghi Minh duyệt lại bốn việc sau khi main tiến, trước push có lease. Danh sách thay đổi của PR nằm trên nhánh đã nêu; không có diff vào `deploy/app`, mẫu Secret hay script CD K8s chung. LOG có nhắc script tương đối `scratchpad/go-xung-dot.py` nhưng không ghi thư mục gốc. Diff Git không xác định được vị trí file tạm hoặc toàn bộ ghi ngoài Git. Không lấy điều đó làm bằng chứng có vi phạm. Phần kiểm fixture Ticket đã duyệt còn hở ở R9.

DT18 và hướng dẫn của cô đặt yêu cầu quan sát và tích hợp. H1/H4, Q1–Q10 là quyết định của Minh trong SPEC đã duyệt. Không có lựa chọn thuật toán, đầu vào nhãn, bộ xếp hạng hay đối chứng đồ thị mới trong diff. WHY-89 giúp thấy hậu quả của việc đồng nhất kết cục; không dùng nó để khẳng định V082 thay đổi thứ hạng. Chữ ghi quyết định T-076 trong DECISIONS vẫn chờ Minh như LOG đã nêu.

Đề xuất sửa ở trên áp cho **commit kế tiếp** của PR. Đã rà các mốc `SPEC`, bảng file, các manifest Q4/T-067 và các đầu vào khóa E5. Code của hệ thống được nhận diện bằng commit. Sửa source, manifest K8s hay fixture Java sẽ đổi Git blob/đầu PR và có thể đổi digest image. Lưu kết quả kế tiếp theo revision mới, giữ bằng chứng của đầu hiện tại và các pin cũ. Không đề xuất sửa hồi tố file kết quả đã ghim.

## Điều đã kiểm và thấy đúng

| Kiểm chỉ đọc | Kết quả và phạm vi |
|---|---|
| `gh pr view 17`, `gh pr checks 17`, `gh run view 46013069317` và API các job | PR draft, MERGEABLE, base/head khớp yêu cầu. Run kết thúc success ở lần 1. Required, tám job Maven, CodeQL, Dependency Review và Deploy scripts đạt. Frontend skipped. Job Deploy scripts có bước routing fixtures đạt, giải quyết thiếu `jq` local. Nội dung body khớp bản local sau bỏ tiêu đề Markdown và chuẩn hóa xuống dòng. [CI đã kiểm](https://github.com/levanminh04/flash-ticket-platform/actions/runs/46013069317) |
| `git diff --name-only 6b77144 2a275b5`, `git diff --check` | 129 file, trong đó 44 Java thuộc `src/main`; diff sạch lỗi khoảng trắng. Diff DTO có 12 khai báo danh sách bỏ annotation thừa phía ngoài và giữ `@Valid` trên phần tử. Đường hoàn tiền mới ghi `DB_ONLY` trong transaction hiện có. |
| Log Maven cuối trong `results/T-076/kiem-cuc-bo/ban-6-main-6b77144/verify/log/` | Lấy dòng tổng cuối của mỗi `*-verify.log`: User 70, Event 178, Ticket 229, Booking 453. Profile RCA Event 186 và Booking 462. TicketPostgresIT 22. Các dòng này đều ghi 0 failure, error và skipped. Bốn log B16 sau rebase mỗi log PASS 2 record. Mở danh mục ZIP của JAR Booking production hiện có: 0 đường dẫn chứa RcaFaults. |
| Phân tích YAML và JSON thực | Bảy Deployment đích có `env.OTEL_AGENT_ENABLED="false"`, `HOST_ID=spec.nodeName`. Bảy ConfigMap có environment production và 29 tên che khác nhau mỗi cái. JSON Schema của PR chấp nhận 135/135 dòng JSON tách từ `ban-6-main-6b77144/tat-secret-true/booking.log`; cả 135 mang đúng commit, `node-thu`, production. Cũng cả 135 là `runtime.log/UNKNOWN`, vì vậy mẫu này không xác nhận kết cục mua vé. Hai file OTLP ở lượt tắt đều 0 byte. Đây là mô phỏng Compose có request thử. |
| Đối chứng bật đã lưu, `ban-6/bat-ghi-de/{traces,metrics}.jsonl` | Duyệt các object có key `url.query`: ba query thử che `q`, `vnp_SecureHash`, `vnp_TxnRef`, còn nguyên giá trị thử email/phone. Tổng độ dài các mảng exemplars trong metrics bằng 0. Các tên khác được xác nhận qua cấu hình, không gọi là đã thử động cả 29. Đường gửi này dùng image trước rebase. |
| Toàn vẹn và tái sử dụng | Hash SPEC hiện tại và năm bản cũ khớp tiền tố ghi ở LOG. Kiểm lại 12/12 mục `results/T-070/don/q4/SHA256SUMS`. Hai file khai trước/triển khai E5 khớp mốc LOG T-073. `git diff --quiet d46f3ae 2a275b5` trên bốn service dùng lại, các Dockerfile và entrypoint trả 0. T-076 không có danh sách checksum của toàn gói; số local mô tả file đang lưu. SHA-256 của JAR agent công bố tại release khớp pin Dockerfile Booking. [Release OTel v2.33.1](https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/tag/v2.33.1) |

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. Đã soát bước 5 trên mã, bytecode, cấu hình, log và CI thật. Bằng chứng hiện có xác nhận build Maven và cơ chế tắt agent trong phạm vi đã kiểm.
2. File duy nhất của lượt này là `tasks/T-076-pr17-otel-may-84/REVIEW-5.md`. Không ghi lên PR, không vào máy 84/exp-app/obs, không chạy thực nghiệm.
3. Phép đọc bytecode, dữ liệu thô và script CD cho thấy các sai lệch ở trên vẫn tồn tại dù Required xanh. Hiện chưa có kết quả triển khai 60 phút, tín hiệu sau đổi bản, diễn tập C6 hay hồ sơ mở rộng cuối task. Các tiêu chí 2–5 của SPEC thuộc các bước sau.
4. **Đề nghị Minh giữ draft, chuyển Claude đáp các điểm và trình gói sửa theo file, trước khi chọn giờ merge.** Phần CD có thể chuẩn bị song song bằng cách xác nhận reader với nhóm. Chấp nhận merge ngay sẽ tiết kiệm một lượt sửa nhưng để lại test hỏng, log không đáng tin trên những nhánh đã nêu và rủi ro triển khai dở. Minh quyết phạm vi sửa và các giới hạn chấp nhận. Hiện chưa có phản hồi của Claude cho lượt này. Khi viết báo cáo đồ án, chỉ dùng các phép kiểm đã làm làm bằng chứng tích hợp cục bộ; đánh giá dưới tải, chất lượng chẩn đoán và hiệu quả đồ thị cần bằng chứng riêng.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6).
- Công đoạn: người làm đáp phản biện, bước 5 Phần A.
- Gói/cổng: P9/P10, tích hợp ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude người làm, Codex người phản biện.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}, results/T-076/bang-file-pr17.md, results/T-076/mo-ta-pr17.md, results/T-076/kiem-cuc-bo/ và các README của từng lượt, B16 trong repo FlashTicket, DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md, REVIEW-5.md (cùng thư mục).
- Code và kết quả liên quan: D:/Project/ft-pr17-dung-lai, git diff 6b77144 2a275b5, nhánh cũ bb84d64, PR #17 và CI trên levanminh04/flash-ticket-platform; chỉ đọc, không vào máy 84, exp-app, obs, không dùng subagent.
- Phạm vi ghi được Minh cho phép trong lượt này: khi Minh chuyển prompt, theo đúng quyền Minh cấp cho lượt đáp; nếu chưa cho phép ghi rõ ràng thì chỉ trả lời trong chat.

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
| R1 | Đúng; CHẶN nghiệm thu PR | Xác nhận bằng mã: `SalesConfigurationListener` có `@RabbitListener` ở `handleSalesConfiguredEventDelivery(Envelope, Message)`; `BookingPersistenceIT.java:888–906` lấy `getMethod("handleSalesConfiguredEvent", Envelope.class)` rồi `getAnnotation(RabbitListener.class).ackMode()` → null → NPE; dòng 8806/8944 cùng kiểu với `EventCancellationListener`. 4748, 5187 (`AcceptPaymentListener`), 6721 (`BookingIssuanceResultListener`) dựng endpoint vào hàm trong, bỏ qua phần bọc telemetry. Profile `integration` (pom 293–302) không chạy trong CI, nên CI xanh không mâu thuẫn. Lỗi do PR (diff 6b77144..2a275b5 thêm 11 dòng vào listener, không sửa IT). Chưa chạy profile `integration`. Sửa: trỏ fixture vào hàm `*Delivery` (truyền cả `Message`), giữ assertion ACK/requeue/DLQ; chạy lại các ca IT bị tác động. | |
| R2 | Đúng về cơ chế; điều kiện chặn merge (OPEN), không phải lỗi nội dung PR | Đọc `deploy-k8s-service.sh:393–494`: khi Secret revision bật reader, `writer_revision(baseline, target)` đòi baseline cùng image với target; khi tắt reader mà bản đang chạy bật reader, `writer_revision(target, active)` cũng đòi cùng image. Image mới của PR không thỏa trong cả hai nhánh → `BOOKING_WRITER_REVISION_REQUIRED` trước `apply_revision`; Event, Ticket tương tự. Writer-only cả trước và sau thì không vướng. Cờ nằm trong Secret, không đọc được theo luật; sự tồn tại `writer-baseline` không phân xử được (file cũng ghi ở nhánh chuyển về writer). Đề xuất: Minh hỏi nhóm trạng thái reader của ba service trên 84 trước C4; nếu đang bật thì nhóm về writer trên digest hiện tại trước merge. Nếu nhóm không xác nhận được thì dời merge. Đồng ý không nới guard. | |
| R3 | Đúng một phần; KHÔNG CHẶN merge, chặn câu "đủ B16 cho luồng mua vé" | Đúng: không có dòng nào chứa cả mã tạm A và mã đơn B; header trả về không phải orderId (controller main); nhánh lỗi khi gọi Booking trực tiếp thiếu header lệch A/B. Nói quá: vẫn nối được A → B qua `requestId` của Booking — `CorrelationFilter` đặt MDC `requestId`, `LogFields.ALLOWED` gồm `requestId`, dòng `reserve` (correlationId = B) và các dòng trước cùng request (A) chung `requestId`. Gateway và Booking khác `requestId`, nối gateway → Booking qua A. Sửa đề xuất: trả `X-Correlation-Id` = orderId khi tạo đơn; `GlobalExceptionHandler` dùng cùng mã cho MDC và phản hồi. Chưa kiểm gateway giữ header do Booking trả về hay không. | |
| R4 | Đúng; CHẶN câu đúng nghĩa log thanh toán | `PaymentService.java:239–256` lưu `UNKNOWN` rồi gọi `BusinessTelemetry.committed(..., previousState, UNKNOWN, "CALLBACK_VERIFIED")`; `BusinessTelemetry.java:28–31` chỉ coi `FAILED` là thất bại, còn lại `SUCCESS`. `stateAfter` vẫn đúng `UNKNOWN`. Schema `log.schema.json` có `UNKNOWN`. Sửa: `stateAfter=UNKNOWN` → `outcome=UNKNOWN`, thêm test ca mã 07. Không đổi tiền, DB, ACK VNPay. | |
| R5 | Đúng; CHẶN câu ngữ nghĩa RabbitMQ | `PaymentMessageListener.java:51…` `basicNack(tag,false,true)` rồi ném lỗi → `RabbitTelemetry` mặc định `FAILED/MESSAGE_PROCESSING_FAILED`; `ContractValidationException` → `MessageConversionException` cũng FAILED. Booking `AmqpRejectAndDontRequeueException` cũng FAILED. Schema có `RETRY`, `REJECTED`; Ticket `TicketBusinessListeners.java:77,82` dùng đúng. Sửa: RETRY sau NACK requeue, REJECTED khi từ chối đã biết; giữ ném lỗi, ACK/NACK, chính sách hàng đợi. | |
| R6 | Đúng; lỗi người làm bỏ sót; CHẶN tiêu chí định danh C4 cho Discovery | Discovery có trong `b16-services.txt`; `statefulset.yaml` không có `HOST_ID`, `ENVIRONMENT`; entrypoint mặc định `local`, `local-test`; `LogFields.java:94–95` dùng hai giá trị đó. Bước 3 chỉ sửa 7 Deployment. Sửa: thêm `ENVIRONMENT: production` vào ConfigMap Discovery, `HOST_ID` = `spec.nodeName` và `OTEL_AGENT_ENABLED: "false"` vào `env:` StatefulSet; chạy `test-k8s-discovery.py`. | |
| R7 | Đúng một phần; CHẶN câu nối log–trace cho Event | Agent tắt: đúng — `CorrelationFilter.java:46–50` (mã main) chép span bên gọi vào MDC `spanId`; `EventLogCustomizer` (PR) xuất nó thành `spanId`. Agent bật: chưa kiểm thứ tự ghi. Gốc rộng hơn, xem N1: ConfigMap đặt khóa MDC của agent là `spanId`, nên ưu tiên `span_id` trong customizer không áp. Sửa: customizer bỏ `spanId` khi trùng đoạn span trong MDC `traceparent`; cùng N1. | |
| R8 | Đúng; KHÔNG CHẶN | `TicketOutboxPublisher.java:115–116` gom `RuntimeException` (gồm lỗi schema/JSON ở 82–84 và lỗi DB sau confirm) thành `BROKER_UNAVAILABLE`; `retryCount` = `message.attempt()` nên lần đầu là 1, trong khi tên trường chỉ số lần thử lại (B16 bảng trường, dòng 62, chỉ ghi "số không âm"). Payment tương tự. Sửa chỉ log: mã trung tính cho lỗi không thuộc broker, `retryCount = attempt − 1`; giữ `last_error_code` trong DB và lịch retry. | |
| R9 | Đúng cả hai; KHÔNG CHẶN; R9b là lỗi quy trình của người làm | R9a: CI không build image; dòng `ADD` chỉ chạy ở CD sau merge. Checksum khớp release. Nếu tải lỗi, CD dừng ở build, bản cũ vẫn chạy. Sửa câu trong `results/T-076/kiem-cuc-bo/README.md`. R9b: Minh duyệt chạy `test-ticket-replica.sh` "nếu chạy được local"; người làm bỏ mà không trình lại. 28/11 Docker laptop tắt nên chưa chạy; `TESTING.md` của nhóm ghi lệnh "chưa kiểm runtime". Chạy trong vòng sửa (cần Docker). | |
| N1 | Người làm tự tìm; KHÔNG CHẶN merge (agent tắt), chặn câu nối log–trace khi bật agent ở 84 | 7 ConfigMap có `OTEL_INSTRUMENTATION_COMMON_LOGGING_TRACE_ID_KEY: traceId`, `…SPAN_ID_KEY: spanId` (commit `46b38a8`, theo SPEC C2). Lab trên exp-app không đặt hai khóa này nên agent dùng `trace_id`/`span_id`, đúng thứ customizer ưu tiên. Ở 84 khi bật agent, ưu tiên đó mất tác dụng; ở Event va với span bên gọi (R7). Sửa: bỏ 2 dòng ở 7 ConfigMap (lệch SPEC C2, cần Minh duyệt). | |
| N2 | Người làm tự tìm; KHÔNG CHẶN, đã đính chính | Hai mốc LOG "14:00Z", "14:20Z" ngày 27/11 sai giờ (thực tế khoảng 13:30Z, 13:45Z); đã ghi dòng đính chính trong LOG 14:30Z. | |
