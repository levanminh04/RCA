# Chỉ đạo của Claude (điều phối) cho Codex

Đọc file này mỗi lần cập nhật `CHECKPOINT.md` và trước mỗi chặng. Mục nào chưa xử lý thì làm theo, rồi ghi một dòng vào `LOG-dem.md`: "đã xử lý STEER #n". Không sửa file này (chỉ Claude ghi).

## STEER #1 — 20:10Z — rà `prepare-app.py` và `build-arm.sh`

Claude đã đối chiếu với repo FlashTicket, **không cần sửa**:
- `KEYCLOAK_AUDIENCE=flash-ticket-api` khớp giá trị mặc định trong `application.yaml` của event, ticket, user, payment.
- Client `user-management` có trong realm; tài khoản MongoDB `user_admin` khớp `deploy/mongodb/compose.yaml`; key-ring `{"keys": {"v1": <base64>}}` khớp `QrTokens.java` (`Base64.getDecoder`).
- `build-arm.sh`: worktree đúng commit, nhãn `revision` đúng, Keycloak chạy `mvn clean verify` (có test), các service khác `-DskipTests`.

Yêu cầu thêm cho tài liệu `huong-dan-trien-khai.md`:
1. Ghi rõ build bỏ test cho 7 service Spring (khác CI của nhóm).
2. `KC_HOSTNAME=http://10.0.0.158:8080` là địa chỉ nội bộ: token chỉ hợp lệ khi gọi Keycloak qua địa chỉ này. Khi hướng dẫn Minh dùng đường hầm SSH để đăng nhập hoặc lấy token từ laptop, phải nêu điều này (ví dụ lấy token bằng lệnh chạy trên `exp-app`, không qua `localhost` của laptop).
3. Liệt kê **tên** các biến env đã sinh (từ `env-inventory.json`), không có giá trị.

## STEER #2 — 20:30Z — kiểm chặng 4 chưa đủ: thiếu span Redis và RabbitMQ

Claude kiểm Tempo trên `exp-obs` (1 giờ gần nhất):
- Có: span `db.system="postgresql"` (booking, event, payment, ticket, keycloak); span server có `http.route`; span client có `server.address`. Prometheus và Loki có đủ 8 service.
- **Không có:** span Redis (`db.system`/`db.system.name` = redis: 0 trace), span RabbitMQ (`messaging.system` != nil: 0; `kind=producer|consumer`: 0).

Yêu cầu:
1. Không ghi chặng 4 là "đạt" khi chưa có span Redis và RabbitMQ (TECHSTACK §4.1 "Cách kiểm" đòi cả ba loại span).
2. Phân xử nguyên nhân, theo thứ tự rẻ trước: (a) lưu lượng thử có đi qua Redis và RabbitMQ chưa (đếm lệnh Redis bằng `INFO commandstats`, đếm message ở RabbitMQ management API trước và sau một luồng); (b) nếu có lưu lượng mà không có span: xem log khởi động agent, danh sách instrumentation (Lettuce, Spring RabbitMQ / RabbitMQ client) có bị tắt hay không tương thích Spring Boot 4.1.1; (c) chỉ khi (a) không đi qua thì tạo luồng nghiệp vụ có đi qua (ví dụ giữ chỗ, tạo đơn) với dữ liệu thử tối thiểu.
3. Ghi kết quả phân xử (cả trường hợp không xác định được) vào `kiem-agent.md` trong `out/`, kèm câu truy vấn TraceQL và số đếm. Đây là yêu cầu R-01, R-04 của `inputs/yeu-cau-quan-sat-p9.md`.

## STEER #3 — 20:45Z — rà `kiem-agent.md`: đạt yêu cầu; sắp thứ tự phần còn lại

Claude đọc `kiem-agent.md`: cách phân xử đúng (đếm trước/sau, tách FACT/OPEN, không gọi 403 là UP). Giữ Redis ở OPEN như đã ghi; **không dành thêm quá 15 phút** cho Redis trong đêm (ghi giả thuyết và phép kiểm cần làm sau vào mục OPEN).

Thời gian còn lại tới 23:15Z khoảng 2,5 giờ. Thứ tự đề xuất, chạy song song khi được:
1. **Đo tài nguyên (C3) chạy nền ngay:** 30 phút rảnh rồi 30 phút tải nhẹ cố định (thay cho 1 giờ + 1 giờ của SPEC; ghi rõ là rút ngắn và vì sao). Ghi RAM, CPU từng container và từng máy, drop của cả hai Collector, GB/giờ ở kho. Không gây lỗi trong 60 phút này.
2. **Trong lúc đo:** viết bộ đọc `out/src/m1/adapter_flashticket.py` từ dữ liệu thật trong Tempo/Loki/Prometheus và dựng môi trường M1 trên `exp-obs`.
3. **Sau khi đo xong:** một lỗi thử (`docker pause` một service trong khoảng 5 phút, tải nhẹ vẫn chạy), ghi mốc vào `out/so-tiem-loi.jsonl`; đóng gói cửa sổ trước–trong–sau; chạy M1. Thêm một cửa sổ không lỗi làm phép thử giả nếu kịp.
4. Từ 23:15Z: tài liệu và `bao-cao-sang.md` như PROMPT.

## STEER #4 — 21:46Z — OOM của booking-service: không tiêm lỗi vào booking lúc này

Codex đã phát hiện đúng: booking (cgroup 512 MiB, giới hạn lấy từ compose của nhóm) bị kernel giết vì hết bộ nhớ lúc 21:04:18 và 21:40:18, Docker khởi động lại 2 lần. Hệ quả:

1. **Không chạy lần tạm dừng booking sau 21:50Z** như kế hoạch đã khóa. Booking đang tự sập theo chu kỳ, nên đây là sự cố không có nhãn; tiêm thêm lỗi vào nó sẽ trộn hai nguyên nhân.
2. **Ghi lại, không xóa:** cửa sổ đo rảnh (20:45–21:15) và tải (21:15–21:45) đều chứa một lần OOM; cửa sổ bình thường t=21:35Z kết thúc 18 giây trước OOM 21:40:18. Báo các cửa sổ này là "có sự cố không nhãn", không dùng làm nền sạch hay phép thử giả.
3. **Phân xử nguyên nhân (rẻ trước):** RSS và heap của booking theo thời gian từ sampler; so với lúc chưa gắn agent (máy 84 chạy cùng giới hạn 512 MiB mà không có agent). Kiểm các service khác còn bao nhiêu khoảng trống so với `mem_limit`. Ghi vào `out/` như một phát hiện C3 (chi phí bộ nhớ của agent), kèm số.
4. **Sửa tối thiểu để đêm nay có cửa sổ sạch:** trong bản compose riêng của `exp-app`, nâng `mem_limit` của booking (và service nào khác sát giới hạn) lên mức đủ dư, ví dụ 768 MiB; ghi rõ đây là **lệch cấu hình so với máy 84**, lý do và số đo. Không sửa file trong repo.
5. **Kế hoạch đã khóa lúc 21:15Z giữ nguyên làm bản 1.** Viết bản 2 với dấu thời gian mới, ghi "sửa sau khi thấy OOM, trước khi có đầu ra M1" (quy tắc 16 của prompt mẫu). Gợi ý thứ tự: khởi động lại, chờ ổn định 10 phút, cửa sổ bình thường mới, rồi một lần tạm dừng 5 phút (service do bạn chọn và ghi vào sổ), rồi chạy M1. Từ 23:15Z vẫn dừng việc mới.

Số đo của Claude lúc 21:47Z (`docker stats`): booking 486/512 MiB (95%), **payment 488/512 MiB (95%)**, **discovery 346/384 MiB (90%)**, event 412/512 MiB (81%), keycloak 609/768 MiB (79%); gateway, ticket, user dưới 55%. Payment và discovery cũng sát giới hạn, nên xét cùng lúc với booking ở mục 4. Không có job tạm dừng nào đang hẹn giờ trên `exp-app`.
