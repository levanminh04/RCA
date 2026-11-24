**CHƯA PHÁT ĐƯỢC E6 qua đêm theo nháp 3. Đề nghị tiếp tục phản biện, giữ S5 chưa mở.**

Có ba điểm chặn lượt ghi. Lệnh GET Event vẫn đi qua bộ giới hạn tốc độ dùng Redis. Công thức sức chứa trong nháp khác mục A3 Minh đã duyệt. Bước 3 chưa có câu SQL thuận và nghịch để kiểm trên các cột thật. Cả ba là vấn đề của **kế hoạch phát**. Tôi không thấy bằng chứng E6 đã chạy hoặc đã làm đổi dữ liệu.

### 1. Các điểm ảnh hưởng quyết định phát

**CHẶN 1 — GET Event ở bước 3 có thể tác động Redis.** Claude đã bỏ đúng GET `availability` của Booking. Tuy nhiên, nháp giữ `GET /api/v1/events/{id}` **qua gateway**. Ở FlashTicket `36a3725`, đường `/api/v1/events/**` đi qua `RequestRateLimiter`, dùng bean `redisRateLimiter`. Controller Event đọc PostgreSQL trong giao dịch chỉ đọc, nhưng bộ lọc chạy trước controller. Trên chính bản ghim, kết quả T-067 ghi `#/span/redis~1api-gateway/ket_qua = "dat"` và `#/span/redis~1api-gateway/so_trace_mau = 5`. Số này xác nhận gateway đã dùng Redis trong lượt T-067. Căn cứ cho đường GET cụ thể là cấu hình định tuyến. **Sửa tối thiểu:** bỏ GET Event khỏi E6. Bước 3 đã dùng SQL đọc lại để nhận phần PostgreSQL. Mặt trái chỉ là mất một đối chiếu công khai cho hai trường ngày diễn. [Nháp 3, bước 3](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-3.md:50) · [Route Event](/D:/Project/flash-ticket-platform/infrastructure/api-gateway/src/main/resources/application.yaml:94) · [Bean dùng Redis](/D:/Project/flash-ticket-platform/infrastructure/api-gateway/src/main/java/com/flashticket/api_gateway/routing/GatewayRouteConfiguration.java:19) · [Bằng chứng T-067](/D:/RCA-flashticket/results/T-067/kiem-tin-hieu/kiem-tin-hieu-lan1.json:56)

**CHẶN 2 — Ngân sách vé đúng, giá trị định ghi chưa đúng quyết định A3.** Với phương án A, dùng lại ba đối chứng và giữ tải 1.800 giây, tôi tính được `12×648 + 12×1.944 + 3×1.512 = 35.640`, khớp `du-toan-4.json#/phuong_an/0/K0_don_ca_dot_bao_thu`. Mục 15 Minh duyệt lấy `purchased + 53.460`, rồi làm tròn lên nghìn. Nháp 3 thêm `max(sức chứa hiện tại, …)`. Ngay với ví dụ `purchased = 44.000`, A3 cho **98.000**, nháp cho **100.000**. Con số 44.000 là ví dụ, chưa phải số đọc trên máy. Việc giữ sức chứa cũ từng nằm ở mục *Khác* và trong đề xuất của CX-32. LOG lượt 10 cho điều phối quyền phát có điều kiện, vẫn giữ phạm vi các dòng và giá trị đã duyệt. **Đề nghị:** dùng nguyên công thức A3 khi trình bước 1. Nếu Minh muốn giảm số dòng phải ghi, giữ 100.000 là phương án hợp lý để duyệt riêng khi đã biết `purchased`. [Mục 15 đã duyệt](/D:/RCA-flashticket/results/T-070/cho-duyet-2026-11-23-chieu.md:38) · [Hai phương án A3](/D:/RCA-flashticket/results/T-074/cau-hoi-minh-5.md:23) · [Ví dụ nháp 3](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-3.md:41) · [Dự toán](/D:/RCA-flashticket/results/T-074/du-toan-4.json)

**CHẶN 3 — Chưa thể xác nhận đường ghi và hoàn tác bằng lệnh thật.** Bước 1 có điểm dừng hợp lệ để lấy danh sách thật và trình SQL. Bước 3 hiện chỉ ghi `SELECT … FOR UPDATE`, “UPDATE theo khóa” và kiểm số dòng. Một `UPDATE` trúng một dòng vẫn có thể bỏ sót một trường JSON, ghi sai kiểu, hoặc ghi đè giá trị đã đổi trong lúc chờ duyệt. Tiền lệ E1 có SQL chạy thật cho Ticket và Payment, gồm điều kiện giá trị cũ và kiểm `ROW_COUNT`. Script đó chỉ đồng bộ ngày của hai bảng. Nó chưa thực hiện phần Event, Booking hay hoàn tác E6. [Nháp 3, bước 1–3](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-3.md:48) · [Script E1](/D:/RCA-flashticket/results/T-071/e1/sua_ngay.sh:15)

| DB | Những gì đối chiếu được trên schema và hiện vật E1 |
|---|---|
| Event | `tbl_events` dùng khóa `id`. Năm cột đích là `sale_ends_at`, `starts_at`, `ends_at`, `checkin_starts_at`, `checkin_ends_at`. Cần gán các ngày liên thuộc trong cùng một `UPDATE` để thỏa `CHECK` ngày check-in bằng ngày diễn. Sức chứa loại vé nằm ở `tbl_ticket_types.configured_quantity`, theo `id` loại vé và `event_id`. `purchase_limit` là giới hạn mua. |
| Booking | `tbl_event_sales_snapshots` có cả `sale_ends_at` và `configuration_snapshot`. Ba khóa `saleEndsAt`, `eventStartsAt`, `eventEndsAt` là **số** giây epoch có phần lẻ. `ticketTypes[*].configuredQuantity` là **chuỗi**, phải chọn phần tử theo `ticketTypeId`. Bản sao tồn kho là `tbl_ticket_type_inventory.configured_capacity`. `held` và `purchased` dùng để kiểm và tính đích. |
| Ticket | `tbl_event_access_snapshots` có `event_starts_at`, `event_ends_at`, theo `event_id`. JSON giao dịch mua lịch sử thuộc phạm vi loại trừ của §3. |
| Payment | `tbl_event_finance_snapshots.event_ends_at` là bản sao cấu hình đã thấy. `tbl_event_payouts` cũng có `event_ends_at`. Dòng cuối `sau.jsonl` là **kết quả đếm bằng 0 ở E1**. Bước 1 cần đếm lại cho đúng sự kiện. Nếu nay có dòng payout, trình lại phạm vi trước khi ghi. |

Ba giá trị JSON đích, tính từ UTC ở §4, lần lượt là `1798668991.402736`, `1798755391.402736`, `1798841791.402736`. Kiểm hậu trạng thái cần đọc cả đường dẫn và kiểu JSON. So chuỗi hiển thị có thể bỏ qua việc số đã bị ghi thành chuỗi. [Các dòng gốc E1](/D:/RCA-flashticket/results/T-071/e1/sau.jsonl) · [Đối chiếu sức chứa E1](/D:/RCA-flashticket/results/T-071/e1/suc-chua.json) · [Ràng buộc Event](/D:/Project/flash-ticket-platform/docs/architecture/data/postgres/10-event.sql:35) · [Ràng buộc Payment](/D:/Project/flash-ticket-platform/docs/architecture/data/postgres/30-payment.sql:111)

**Sửa tối thiểu cho điểm 3:** dùng ngay điểm dừng đã có ở bước 1. Trình **cặp SQL ghi và đảo** cho cùng danh sách khóa, cột, đường dẫn JSON và kiểu. Trong giao dịch ghi, so giá trị vừa khóa với giá trị bước 1 đã duyệt. Nếu khác thì dừng trước `UPDATE`. Lưu được giá trị cũ và đích theo từng lần thử trước `COMMIT`. Khi đảo JSON, chỉ đảo trường E6 đã đổi nếu trường ấy còn bằng đích. Đảo cả tài liệu JSON có thể làm mất thay đổi hợp lệ ở trường khác. Chưa cần chạy thử trên máy để sửa phần thiết kế này.

| Mốc lỗi | Kết luận theo luật 21 |
|---|---|
| **10%** | **KHÔNG CHẶN** về hoàn tác DB. Bước 0–2 chưa ghi dữ liệu nghiệp vụ. Giữ dump hoặc nhật ký dở theo quy định giữ lượt hỏng. |
| **50%** | **CHẶN ghi** tới khi có cặp SQL trên. Khi mất kết nối lúc commit, phải xác định giao dịch cũ đã kết thúc, đọc lại dưới khóa và so với nhật ký lần thử. Nếu cũ bằng đích ngay từ đầu thì đây là trường không cần đổi. Đếm số dòng trúng khóa không phân biệt được trường hợp này. |
| **99%** | Gặp giá trị thứ ba hoặc mất bằng chứng về dòng đã sửa, **dừng và giữ máy ở điều phối** là đúng. Nếu đọc lại chỉ thấy giá trị cũ/đích, dùng cùng đường đảo có điều kiện sau quyết định của Minh. Nếu DB và mốc đã xác nhận, lỗi băm hoặc đọc image ở bước 7 chỉ cần làm lại hiện vật thiếu. Bỏ `pg_restore` toàn DB là đúng. Worker Payment có lịch chạy kể cả khi k6 đã dừng. |

[Đường xử lý lỗi trong nháp](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-3.md:61) · [Worker Payment](/D:/Project/flash-ticket-platform/services/payment-service/src/main/java/com/flashticket/payment_service/worker/PaymentWorker.java:109)

### 2. Bước 0, chi phí và phạm vi kết luận

**Bước 0 — KHÔNG CHẶN về phương án kiểm chỉ đọc.** Nháp đã bỏ `inj3.py verify`. Code ghim tạo thư mục ngay khi nạp module và có nhánh gỡ pause, xóa deadline. Kiểm trực tiếp tiến trình, deadline/pid, lease, toxic và cờ `Paused` tránh được hai tác động này. Trên máy tải, cần phân biệt container đang chạy với container `Exited` được giữ lại. Trên exp-obs, cần phân biệt `flash-ticket-t073-webhook` với `flash-ticket-t072-bo-nhan` được phép còn chạy, dù cùng project Compose. Hồ sơ bàn giao ghi exp-app ở `407b4f5`, exp-obs ở `1bb40ca`, S4 đã đóng. Đề nghị so **cả hai HEAD** với bàn giao và dùng danh sách tiến trình toàn máy có đối số. Một cây Git sạch vẫn có thể ở sai revision. Lỗi đọc lease, Docker hoặc danh sách tiến trình phải trả về “chưa kiểm được”. Không có bằng chứng trạng thái máy hiện thời trong lượt chỉ đọc laptop này. [Bước 0](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-3.md:47) · [Code `verify`](/D:/Project/flashticket-rca-lab/faults/injectors/docker/inj3.py:309) · [Sổ đóng S4](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LICH-MAY.md:41) · [Trạng thái bàn giao](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/TRANG-THAI.json)

**Tạo ca và phạm vi dữ liệu.** Nhánh K0 đã bỏ runner, tải và bộ tiêm. Nếu đọc đủ trạng thái bước 0 và dừng khi bộ điều phối W5 còn chạy, tôi không thấy đường phát ca RCA trong các bước SQL/dump. Không thấy lệnh E6 cần MongoDB. Redis còn đường gián tiếp ở GET gateway nêu trên. Bốn DB nghiệp vụ được nêu ở §3. Tiền lệ `moc-db.json#/dump` của E1 còn có `keycloak_db`, nên hồ sơ E6 cần ghi đích danh tập DB đã dump. Một mốc gồm các dump riêng chỉ chứng minh trạng thái PostgreSQL trong phạm vi các đại lượng đã đọc trước/sau. [Phạm vi E6](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-3.md:27) · [Mốc E1](/D:/RCA-flashticket/results/T-071/e1/moc-db.json)

**Chi phí — KHÔNG CHẶN riêng, cần sửa số trước khi điều phối xếp lịch.** Cộng sáu dòng §8 được **75–155 phút**, tức **1 giờ 15 đến 2 giờ 35**, chưa gồm chờ Minh ở bước 1, bàn giao bước 8 và điều tra khi gặp giá trị thứ ba. Cận trên làm tròn một chữ số là **2,6 giờ**. Hàng lỗi 10% cho phép chờ yên 30 phút nhưng lại ghi cả lượt làm lại “≤ 30 phút”. Nếu còn phải dump và đọc lại thì cận ấy thiếu thời gian. Khoảng 20–40 phút cho đảo theo dòng vẫn là ước lượng. Khi tới điểm chờ mà chưa có quyết định đúng phạm vi, phương án khả thi qua đêm là dừng trước ghi. [Bảng lỗi](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-3.md:65) · [Các hạng mục thời gian](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-3.md:78)

**Pilot W7 — KHÔNG CHẶN E6, cần thu hẹp câu “xác nhận”.** Một lượt mua thành công trước hạn cũ 02/12 phù hợp với **cả hai** cấu hình hạn bán. Tương tự, khi cả hai mức sức chứa đều còn vé, mua được một vé không phân biệt chúng. Code Booking so thời điểm quyết định với `saleEndsAt`. Pilot có thể xác nhận hành trình mua hoạt động tại thời điểm thử. Muốn kết luận dịch vụ thấy đúng giá trị mới, cần trường trả về hoặc bằng chứng ứng dụng phân biệt được hai giá trị, trong quyền của W7. Đề nghị giữ kết luận E6 ở mức đọc lại PostgreSQL. [Giới hạn của nháp](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-3.md:88) · [Điều kiện bán của Booking](/D:/Project/flash-ticket-platform/services/booking-service/src/main/java/com/flashticket/booking_service/service/impl/OrderServiceImpl.java:1957)

### 3. Đối chiếu phản hồi của người làm

| Điểm | Kết luận sau kiểm |
|---|---|
| CX-32 #1, quyền và bước 0 | **Đúng.** Đã sửa phần gọi `verify`, bổ sung các phép đọc và điểm dừng W5. Trạng thái sống chỉ xác nhận được khi chủ S5 thực hiện bước 0. |
| CX-32 #2, A3/B1/B2 | **Đúng về ngân sách, đúng một phần về bản sửa.** `35.640` khớp. Phép `max` vẫn cần quyết định riêng. |
| CX-32 #3, GET | **Đúng một phần.** Bỏ GET Booking và nhận DB bằng SQL là đúng. Cả reviewer trước lẫn người làm đã bỏ sót bộ giới hạn tốc độ trên tuyến GET Event. |
| CX-32 #4, hoàn tác | **Đúng về nguyên tắc, xử lý một phần.** Đã bỏ restore cả DB và có điểm dừng khi không biết trạng thái. Chưa có cặp lệnh khả kiểm ở bước 1–3. |
| CX-32, D13 | **Đúng.** W-1 đã ghi lần đầu rời Normal có thể vào thẳng Alerting, cùng điều kiện về phiên bản, khoảng nhìn lùi và giờ đánh giá. Vẫn là đề xuất khi khóa W7. |
| CX-32, BARO | **Đúng.** Ở `259ea41`, API tính điểm, sắp ổn định rồi trả tên và hạng. Có thể dựng lại điểm để kiểm; đầu ra API chỉ cho đối chiếu hạng. |
| CX-32, độ trôi K0 | **Đúng.** Cân bằng số lần xuất hiện theo khối vẫn cho phép hai ô lần lượt đứng đầu và cuối ở cả ba khối. W-3 thu hẹp kết luận đúng mức. |
| CX-32b M1, khóa image | **Đúng, đã sửa ở thiết kế.** `.Image` của container rồi `docker image inspect` ID đó xác định được image chạy, kể cả khi `RepoDigests` rỗng. |
| CX-32b M2, SimpleRCA | **Đúng.** `prepare` dùng chung `boundary` để cắt N và A. W-4 giữ trạng thái chưa hỗ trợ D13 cho tới khi wrapper giữ A gốc và cắt riêng N′. |
| CX-32b, dự toán E6 cũ | **Đúng về hiệu lực.** §8 đã chỉ rõ thay `#/viec_them/E6` vốn tính cả chu kỳ đã bỏ. Phép cộng của bảng mới còn lệch như trên. |

Với các điểm kế thừa CX-29/29b, #1–2 đúng về lỗi của bản cũ. #3 đã sửa công thức giao khoảng, tại `t̂=t+900` giao bằng 0. #4 còn phụ thuộc miền hỗ trợ D13. #5 đúng một phần vì yêu cầu niêm đầu vào đã có; nhánh runner bỏ gói khi `fault_ok=False` là lỗi thực thi cụ thể. #6 đúng về mất tên thực thể ở wrapper. #7 đúng vì đầu dò sạch sau tự gỡ tương thích với cả “đã tiêm” và “chưa tiêm”. Các bổ sung về pilot mặc định ×1, bộ đốt ghim Booking và dự toán khi kéo dài tải tác động tới W7. B2 đã chọn giữ thời lượng tải. Các điểm này không đòi chạy một ca RCA ở E6. [Thiết kế W7 bản 5](/D:/RCA-flashticket/results/T-074/thiet-ke-w6-5.md:29) · [Các điểm W-1 đến W-6](/D:/RCA-flashticket/results/T-074/con-mo-w6.md) · [Miền D13 gốc](/D:/RCA-flashticket/tasks/T-043-thiet-ke-rca-m1/SPEC.md:329) · [SimpleRCA](/D:/RCA-flashticket/src/simplerca/adapter.py:55) · [BARO](/D:/RCA-ext/src/RCAEval/RCAEval/e2e/baro.py:49)

**Quy trình — KHÔNG CHẶN riêng.** LOG phiên 6 ghi mở phiên, rồi đọc CX-32/32b lúc 17:43Z. Trước mốc đó không có mục ghi nhận xét tự tìm được của phiên 6 theo §5.7. Chứng cứ xác nhận **thiếu bản ghi tự soát trước phản hồi**. Không đủ để suy ra Claude đã hoặc chưa suy nghĩ gì ngoài LOG. Hệ quả cụ thể là bảng “10 điểm đều đúng; không bất đồng” không cung cấp bằng chứng kiểm độc lập cho đường qua gateway hay phép `max`. Phần diff T-074 quan sát được gồm tài liệu dưới `results/T-074/`, LOG nối thêm và dòng T-074 trong STATE, phù hợp phạm vi thiết kế. [LOG phiên 6](/D:/RCA-flashticket/tasks/T-074-w6-thiet-ke-danh-gia/LOG.md:520) · [Phạm vi SPEC](/D:/RCA-flashticket/tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md)

### 4. Báo cáo cuối lượt

1. **Đã làm.** Đối chiếu quyết định R9, Q8/Q9, phương án C và mục 13–24 với nháp 2–3, E0/E1, code ghim và phản hồi phiên 6. Hồ sơ đã có các đầu ra thiết kế W6, dự toán và câu hỏi gom. Phần xin phát E6 còn ba điểm chặn trên. E6 chuẩn bị trạng thái hệ thống cho W7. DT18, hướng dẫn của cô và G6 vẫn cần bằng chứng đánh giá FlashTicket, đồ thị và chẩn đoán ở các gói tương ứng. E6 không đưa nhãn vào một đường xếp hạng. Lý do chọn K0 đã có ở hồ sơ WHY đề xuất, cùng phương án K2 và giới hạn về trôi. Mốc ghi WHY chính thức là trước thu W7.
2. **File.** Không sửa file nào. Không commit, không SSH, không dùng subagent, không mở dữ liệu khóa và không chạy thực nghiệm.
3. **Kiểm đã chạy.** `Get-FileHash` khớp **22/22 mục** trong sáu manifest T-074. Chín mục E0/E1 đã chọn khớp trong từng manifest T-071 được đối chiếu. Đã kiểm hash hiện vật tín hiệu gateway T-067, đọc code bằng `git show`/`git grep` tại `1bb40ca`, `36a3725`, `259ea41`, tính lại ngân sách vé, thời gian và epoch. Các kiểm này xác nhận bản thiết kế và căn cứ cục bộ. Trạng thái máy, `purchased`, SQL theo dòng thực và thời gian đảo thực tế chưa được đo.
4. **Điều cần Minh quyết.** Đề nghị **tiếp tục một lượt đáp hẹp của Claude, giữ S5 chưa mở**. Dùng nguyên A3 đã duyệt, bỏ GET gateway, và giữ điểm dừng duyệt cặp lệnh thuận/nghịch trước ghi. Cách này mất đối chiếu HTTP ở E6 và có thể cần Minh chốt danh sách vào hôm sau. Đổi lại, điều phối biết chính xác việc nào có thể hoàn tất qua đêm. Nếu Minh chọn giữ sức chứa hiện tại khi cao hơn đích, cần duyệt đúng thay đổi A3 đó. Nháp 3 và `con-mo-w6.md` đã ghim trong `SHA256SUMS-6`; nếu duyệt soạn bản sửa, đề nghị dùng bản kế tiếp và manifest riêng. Quyết định phát vẫn theo Q8 và điều kiện ở LOG lượt 10. [Điều kiện phát](/D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:378) · [Manifest bản 3](/D:/RCA-flashticket/results/T-074/SHA256SUMS-6)

### Prompt bàn giao cho Claude

Mẫu hiện có các khối G0–G4. Tôi giữ cách bàn giao đã ghi ở LOG phiên 6, dùng khối G3 cho phần kiểm thiết kế trước khóa. Cổng thực của task vẫn là **chuẩn bị G6**. Minh có thể chuyển bảng phản biện ở trên cùng prompt này. [Mẫu gốc](/D:/RCA-flashticket/docs/review-prompt.md:27)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074, tasks/T-074-w6-thiet-ke-danh-gia/, nháp SPEC bổ sung E6 ở results/T-074/e6-spec-nhap-3.md và phản hồi phiên 6.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P9/P10, W6 → E6, chuẩn bị W7 và G6. Mẫu hiện có dùng khối G3 như bàn giao phiên 6.
- Người làm và người phản biện chính thức: Claude là người làm T-074; Codex là người phản biện.
- Tài liệu gốc: tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md, LOG.md; docs/DECISIONS.md; tasks/T-070-dieu-phoi-giai-doan-2/LOG.md, LICH-MAY.md, HOP-DONG.md, TRANG-THAI.json; results/T-070/cho-duyet-2026-11-23-chieu.md.
- Phản biện và phản hồi trước: results/T-070/codex/CX-29-tin-cuoi.md, CX-29b-tin-cuoi.md, CX-32-tin-cuoi.md, CX-32b-tin-cuoi.md; LOG T-074 phiên 5–6; bản kiểm lại và các đề xuất của Codex do Minh chuyển kèm trong chat.
- Code và kết quả liên quan: results/T-074/ và SHA256SUMS đến SHA256SUMS-6; results/T-071/e0-trang-thai.md và e1/; results/T-067/kiem-tin-hieu/ và manifest; D:/Project/flashticket-rca-lab tại 1bb40ca, D:/Project/flash-ticket-platform tại 36a3725, D:/RCA-ext/src/RCAEval tại 259ea41.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chỉ đọc trên laptop, không SSH, không dùng subagent; đọc có chọn lọc.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```