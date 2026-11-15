# Môi trường kiểm khả thi T-058

Lượt đêm 10/11/2026 UTC. Codex thực hiện; Claude điều phối bằng `STEER.md`. Hướng dẫn lệnh, giải thích tham số và cách xem từ laptop nằm ở `huong-dan-trien-khai.md`.

| Máy | SSH công khai | Địa chỉ nội bộ | Kiến trúc và hệ điều hành | RAM Linux báo ban đầu | Ổ gốc |
|---|---|---|---|---|---|
| exp-app | ubuntu@129.221.208.47 | 10.0.0.158 | aarch64, Ubuntu 24.04.5 | 11925 MiB | khoảng 48 GiB usable |
| exp-obs | ubuntu@213.35.116.128 | 10.0.0.215 | aarch64, Ubuntu 24.04.5 | 10919 MiB | khoảng 135 GiB usable |

Hai Oracle A1 cùng subnet `10.0.0.0/24`. Giá trị RAM là số hệ điều hành báo, khác mô tả danh nghĩa và khác máy 8 GiB trong SPEC cũ. Không dùng kết quả đêm nay để khẳng định máy 8 GiB đủ. Số CPU Linux và trạng thái cuối lượt nằm trong `environment-app.json`, `environment-obs.json` khi thu xong.

Docker Engine 29.9.3, Compose 5.7.0. `chrony` đồng bộ giờ; không có swap. Luật INPUT cho subnet nội bộ được lưu bằng `netfilter-persistent`; chưa reboot để kiểm nạp lại. Không đổi Security List Oracle.

## 1. Ứng dụng và dữ liệu

Clone công khai trên `exp-app`: `/opt/flash-ticket-src`. Mỗi service có worktree riêng dưới `/opt/flash-ticket-build`, checkout đúng commit đầy đủ trong `inputs/revisions.json`. Tám image cục bộ `ft-local/<service>:arm64-<8 ký tự commit>`; bỏ frontend. Bảy service Spring build bằng wrapper với `-DskipTests`; **không chạy test**. Keycloak SPI dùng Maven `clean verify`, có chạy test. Chi tiết commit, image ID, ARM và digest nằm trong manifest.

Ứng dụng dùng bản compose của nhóm chép vào `/opt/flash-ticket-app/compose`. Bản thêm mount agent ở `compose-exp`; không sửa repo. Gateway nghe `10.0.0.158:8081`; Keycloak nghe `10.0.0.158:8080`. Sáu Spring service còn lại chỉ nghe loopback. Keycloak dùng bridge; các Spring service dùng host network. Eureka có sáu client UP, cộng discovery và Keycloak là tám JVM.

Hạ tầng nằm ở `/opt/flash-ticket-infra`: PostgreSQL 16.15, Redis 7.4.11-alpine, RabbitMQ 4.3.6-management, MongoDB 7.0. Chỉ publish loopback. Dữ liệu sinh mới; dùng DDL và realm của repo. Lỗi quyền executable của init PostgreSQL và hai reader SQL bị thiếu đã được sửa ở bản triển khai. Đã kiểm riêng init từ volume trống: bốn business DB có 12/15/13/7 bảng. Log lỗi ban đầu vẫn giữ.

Env, tài khoản thử, client secret và QR ring sinh mới trên `exp-app`. File env mode 600; QR ring owner 10001, mode 440. Tài liệu chỉ ghi tên biến. Giá trị sinh ngẫu nhiên trên máy, xem file tương ứng ở `/opt/flash-ticket-app/env/` trên `exp-app`; QR ring ở `secrets/ticket-qr/key-ring.json`. `.env` gốc nằm trong clone trên Oracle. Không có bí mật được chủ động chép vào gói bàn giao.

Issuer dùng thống nhất `http://10.0.0.158:8080/realms/flash-ticket`. Lấy token bằng script chạy trên `exp-app`; không đổi issuer thành localhost của laptop. Luồng smoke đã qua catalog/detail/availability, tạo đơn, replay idempotency, tạo URL thanh toán giả và hủy hold. Luồng dừng trước thanh toán thật. Không có ngrok, VNPay thật hay email thật. Seed event/ticket snapshot bằng SQL tối thiểu được lưu cùng script và UUID trong `seed-fixture.json`.

## 2. Quan sát

Agent Java 2.33.1 gắn vào cả tám JVM. `JAVA_TOOL_OPTIONS` giữ `-XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC`. Head sampler `parentbased_always_on`; không tail sampling. Spring xuất OTLP HTTP/protobuf tới `127.0.0.1:4318`; Keycloak bridge tới `10.0.0.158:4318`. Collector tại chỗ contrib 0.165.0 dùng host network; có file queue và file capture. Receiver log chỉ đọc tám container ứng dụng; công cụ tải/tiêm lỗi không được đưa vào Loki.

Trên `exp-obs`, LGTM 0.40.0 đã dùng để có smoke sớm, sau đó dừng và giữ volume. Kho hiện tại gồm Collector 0.165.0, Prometheus 3.16.0, Loki 3.7.9, Tempo 3.1.1 và Grafana 13.3.0. Image ghim digest trong compose cuối. Grafana nghe `10.0.0.215:3000`; Collector nghe `10.0.0.215:4317/4318`; API backend publish loopback. Trên laptop chỉ mở tunnel loopback tới Grafana/gateway.

Trace/log/metric đã truy vấn được qua proxy Grafana; có dashboard `t058-flashticket`. HTTP/JDBC/Mongo và RabbitMQ fan-out có bằng chứng mẫu. Redis còn thiếu span dù lệnh thật có chạy. Chưa phủ đủ R-01–R-10; xem `kiem-agent.md`, `kiem-telemetry.md`. Bố cục dashboard chưa kiểm bằng trình duyệt.

Prometheus đặt retention 48h. Thời gian giữ thực tế Loki/Tempo chưa xác minh; `reject_old_samples_max_age` của Loki không phải retention. File capture xoay theo dung lượng. Cần kiểm dung lượng dài hạn trước khi dùng làm nền nhiều ngày.

## 3. Phép đo và M1

Theo STEER #3, C3 rút còn 20:45–21:15Z rảnh và 21:15–21:45Z tải đọc 1 request/giây. Lấy mẫu mỗi 15 giây, không gây lỗi trong giờ đo. Đây là phép đo rút ngắn; không thay SPEC 1 giờ + 1 giờ. Raw samples và kết quả tổng hợp đã nhận trong các file `resources-30m-*`, `so-do-tai-nguyen.json`.

Kết quả C3: cả hai pha có OOM cgroup booking 512 MiB, lúc 21:04:18Z và 21:40:18Z. Dữ liệu vẫn giữ; không coi là nền sạch. Sau C3, theo STEER #4, compose-exp đổi booking/payment/event lên 1 GiB, discovery 768 MiB, Keycloak 1536 MiB. Đây là lệch giới hạn so với compose gốc; giữ các cờ JVM 50% và UTC. API phục hồi 21:50:53Z; theo dõi mới dùng counter cgroup và RSS đúng tiến trình Java. Xem `kiem-bo-nho.md`. Không có đối chứng cùng máy không agent để định lượng overhead.

M1 dùng Python 3.12 trên `exp-obs`, dependencies T-044 có freeze constraints. 39 file `src/m1`, `src/p3` khớp SHA của T-054 main013-v2. Không sửa code P7; chỉ thêm `adapter_flashticket.py`. Inventory giữ 32 thực thể T-037, kể cả thực thể chưa thấy; không thu hẹp theo service bị pause. Host thiết kế không tự đồng nhất với Oracle.

Bản đầu lấy trace/log từ file OTLP do Collector ghi song song khi xuất tới Tempo/Loki; metric lấy qua Prometheus API. Các API kho và proxy Grafana đã được kiểm bằng mẫu riêng. Chưa có bộ đọc đầy đủ Tempo/Loki API, chưa chứng minh từng record mirror đều đã được kho lưu. Vì vậy phần này chỉ kiểm chuyển đổi và chạy M1 trên telemetry thu được; chưa hoàn thành toàn bộ đường đọc kho của P9b.

Kế hoạch đầu lúc21:15Z ở `m1-execution-plan.json` dự kiến một cửa sổ bình thường và một pause, mỗi input chạy lặp hai lần. C4 SPEC yêu cầu3lỗi+1bình thường; phạm vi đêm nay hẹp hơn theo STEER. User `rca` không đọc được sổ của user `ledger`; chỉ `t` và tín hiệu/metadata được phép đi vào API bảy tham số. Gói thực chạy v2, hash và diagnostics đã nhận ở `rca-ban-dau/`.

Plan trên giữ làm v1 và hai ca v1 đã hủy theo STEER #4. Plan v2 ở `m1-execution-plan-v2.json`, khóa 21:52:40Z sau khi thấy OOM và trước đầu ra M1: chờ ổn định 10 phút, cửa sổ bình thường mới 22:01–22:11Z, pause event-service không trước 22:17Z nếu nền đã đạt. Không pause booking. Tải v1 giữ tới22:15; v2 nối tiếp tới22:35, file riêng. Kết quả phải phân biệt cấu hình bộ nhớ trước và sau sửa.

V2 đã chạy xong: normal và ca pause đều có output lặp cùng SHA, 39 pin nguồn khớp, graph 7 nút/8 cạnh. Ca pause không đủ kênh hợp lệ cho event-service nên chỉ trả hạng 16/17 thực thể quan sát. Event unpause22:22:28Z, catalog/detail trở lại200 ở22:23:00/01Z. Availability đi booking và không bị ảnh hưởng; giả định “cả ba đường tới event” trong plan đã được đính chính riêng, không sửa bản khóa. Xem `rca-ban-dau.md`, `load-impact-detail.json`.

Đây là cài đặt và kiểm khả thi. Không có kết luận về độ chính xác thứ hạng hoặc RQ5. Repo RCA/FlashTicket trên laptop chỉ được đọc; không GitHub CI/push, không truy cập máy 84/AWS.
