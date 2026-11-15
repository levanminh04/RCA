# Báo cáo sáng — T-058, lượt đêm 10/11/2026 UTC

FlashTicket và kho quan sát đang chạy trên hai Oracle ARM. API cuối lượt đã qua; chưa hoàn tất thanh toán thật. Có trace/log/metric và hai gói M1 chạy lặp được. **C1 còn thiếu Redis; C3 gặp OOM cgroup; ca pause thiếu kênh để chấm chính event-service.** Đây là kiểm khả thi, không phải đánh giá hiệu quả hay câu trả lời RQ5.

## 1. Kết quả theo chặng

| Phần | Kết quả và bằng chứng |
|---|---|
| Máy/mạng | Hai Ubuntu24.04.5 aarch64, mỗi máy Linux báo2CPU; Docker29.9.3/Compose5.7.0. Chrony đồng bộ, không swap. Firewall cho subnet nội bộ đã lưu; chưa reboot để thử. Web chỉ bind loopback/IP nội bộ. `environment-app.json`, `environment-obs.json` |
| Build | Tám image `ft-local/*:arm64-<commit8>`, đúng worktree/commit/image runtime trong revisions. Bỏ frontend. Bảy Spring build **bỏ test**; Keycloak SPI `clean verify` có test. Không CI/push. `manifest-digest.json`, `build-manifest.json` |
| Dữ liệu/API | Env, secret, realm và QR ring sinh mới trên exp-app; không lấy từ máy khác. Bốn hạ tầng healthy; fresh PostgreSQL init riêng đủ12/15/13/7bảng. Seed SQL một event, hai loại vé và snapshot. API catalog/detail/availability200, order/replay201 cùngorder, paymentURLgiả200, cancel200. `smoke-api-final.json`, `verify-app-final.json` |
| Quan sát | LGTM0.40 dùng trước rồi dừng, giữ volume. Kho ghim riêng Collector0.165, Prometheus3.16, Loki3.7.9, Tempo3.1.1, Grafana13.3 đang chạy. Grafana proxy trả trace18span, log và metric8JVM; dashboardđãtạo, chưa kiểm bố cục bằng trình duyệt. `grafana-evidence.json`, `image-pins-*.json` |
| M1 | Python3.12 + freezeT044;39pin P7/P3 khớp. Không sửa lõi P7; adapter mới chỉ ởout và bảnOracle. Hai gói v2 có hash và output lặp, không có trường nhãn/mãca/ledger trongAPI. `rca-ban-dau.md`, `rca-ban-dau/`, `m1-feasibility-details.json` |

Gateway/Keycloak/Grafana lần lượt ở `10.0.0.158:8081`, `10.0.0.158:8080`, `10.0.0.215:3000`. Xem từ laptop qua SSH tunnel trong [hướng dẫn](huong-dan-trien-khai.md). Issuer vẫn là `http://10.0.0.158:8080/realms/flash-ticket`; lấy token trên exp-app. Bí mật chỉ xem trực tiếp file trên máy; tài liệu không chứa giá trị.

Gateway/payment health trả403 theo chính sách. Không gọi đó là UP: sáu client Eureka UP và API nghiệp vụ là bằng chứng tương ứng. VM app còn35GiB đĩa, obs còn122GiB tại snapshot cuối; RAM Linux báo11925/10919MiB, khác máy8GiB trong SPEC.

## 2. Trả lời C1–C4

**C1 — đạt một phần.** Agent2.33.1 chạy cùng các JVM/Boot4.1.1, có HTTPCLIENT/SERVER, JDBC/Mongo và ví dụ log nối span. RedisGET/SET tăng thật nhưng không có span Redis; hai rawpackv2 vẫn chỉ thấy DBsystem PostgreSQL/Mongo. Rabbit phải dùng đúng API hủy event synthetic mới sinh1PRODUCER+3CONSUMER cùng trace/parent; luồng đặt vé dừng thanh toán trước đó chưa publish. Queue/vhost và độ phủ log/route còn thiếu. Không quy lỗi chung cho Boot hoặc đổi starter trong đêm. Xem `kiem-agent.md`.

**C2 — từng yêu cầu còn một phần/chưa kiểm.** `kiem-telemetry.md` đối chiếu đủR-01–R-10, có bằng chứng và phần thiếu. Chưa có ánh xạ đủ65thao tác,12cạnh dữ liệu/14binding, queue/vhost, tỷ lệ log-span toàn cửa sổ hoặc đối chiếu mỗi request với span gateway. Revision mô hình T-037 chưa được chứng minh khớp runtime mới.

**C3 — cấu hình cgroup cũ không ổn định.** Theo STEER#3, đo rút30phút rảnh+30phút tải1rps, giữ241mẫu/máy. Booking chạm cgroup512MiB, kernel giết lúc21:04:18Z và21:40:18Z; cả hai pha có sự cố không nhãn. Host vẫn còn RAM. `State.OOMKilled=false` sau restart không chứng minh khôngOOM; journal và delta restart xác nhận cả hai.

| Máy/pha | CPU trung bình | RAM available nhỏ nhất | Tăng dữ liệu quan sát GB/giờ |
|---|---:|---:|---:|
| app/rảnh |20,44%|59,01%|0,1207|
| app/tải |21,23%|58,63%|0,1573|
| obs/rảnh |3,26%|86,50%|0,8442|
| obs/tải |3,25%|86,55%|0,8612|

GB/giờ ngoại suy từ30phút, gồm capture/queue/backend; chưa phải retention ổn định. Các chuỗi receiver_refused đầy đủ có delta0 ở hai Collector; send_failed/enqueue_failed không xuất chuỗi trong mẫu. Không suy drop SDK=0. Xem `so-do-tai-nguyen.json`, `unplanned-oom.json`, `kiem-bo-nho.md`.

Theo STEER#4, sau C3 đã tăng riêng compose-exp: booking/payment/event1024MiB, discovery768MiB, Keycloak1536MiB; giữ các cờ JVM50% vàUTC. API phục hồi21:50:53Z. Monitor sau sửa có159mẫu từ21:52:44 tới22:32:37, cgroupOOMkill/restart0, đúng một lần eventpaused có chủ đích. Chưa có A/B cùng máy khôngagent hoặc C3 đủ1h+1h sau sửa; không định lượng overhead riêng của agent hay kết luận máy8GiB đủ.

**C4 — đường chạy thực thi được, còn thiếu đầu vào ở ca pause.** Planv1 giữ nguyên nhưng hủy hai ca sau OOM; không chạy M1v1. Planv2 khóa21:52:40 sau quan sát OOM, trước đầu raM1. Sau khoảng chờ606/606HTTP200 và normal22:01–22:11 có600/600HTTP200, pauseevent300,258giây rồi phục hồi. Không pausebooking.

| Casev2 | Span | Metric rows gói rộng | Log | Quan sát/trả hạng | Graphnút/cạnh | Lặp cùngSHA |
|---|---:|---:|---:|---:|---:|---|
| Normal |32138|4617|23|17/17|7/8|Có|
| Pauseevent |26643|4505|234|17/16|7/8|Có|

Cả hai `status=OK`, E2dựphòng0. Trong nửaA của ca pause, event có0span,0mẫu CPU/RAM mới; RED chỉ3mẫu hữu hạn, dưới ngưỡng5. Nó nằm trong `NO_VALID_CHANNEL`, không được trả hạng. Không điền0/forward-fill hoặc đổi ngưỡng để ép có điểm. Chưa đủ3lỗi+1normal của SPEC; không coi chạy thành công là chẩn đoán đúng.

Trace/log adapter lấy từ mirrorOTLP của Collector, metric từ PrometheusAPI; chưa là bộ đọc đầy đủ Tempo/LokiAPI. Cần review độ phủ/kênh thiếu và đường đọc kho trước hoàn tấtP9b.

## 3. Tác động lỗi và điều đã sửa trong diễn giải

Pause xác nhận22:17:28.010777Z; unpause22:22:28.268351Z. Theo nhóm bắt đầu request so với mốc xác nhận:300request trong pause gồm100HTTP200,133HTTP503,67HTTP504. Catalog/detail phục hồi ở request22:23:00/22:23:01Z; availability đi booking và luôn200 trong pause.

Planv2 đã ghi sai giả định cả ba endpoint tới event-service. Giữ file khóa, ghi đính chính ở `m1-plan-v2-deviations.json`; không đổi workload/t/thuật toán. Một504 trong nhóm trước xác nhận bắt đầu sau lệnh pause nhưng trước xác nhận khoảng10ms; `load-impact-detail.json` giữ khoảng mốc, không gán thành lỗi nền. Năm phút trước lệnh yêu cầu có300/300HTTP200. Tổng4800request gồm lỗiOOM/recreate trước đó, không gán toàn bộ397phản hồi lỗi cho pause.

## 4. Bàn giao và phần chờ quyết

Lệnh/cấu hình/cách dùng MobaXterm: `huong-dan-trien-khai.md`; cấu hình công khai và hash trong `public-*-config.tgz`, `config-public/`. Gói không có env, realm chứa bí mật hoặc QR ring. Chưa dựng lại toàn bộ hai VM từ số0 bằng bản script cuối.

Đề xuất chuyển tiếp: review adapter và xử lý thiếu kênh khi servicepaused; probeLettuce cùng phiên bản để phân xử Redis; sửa initPostgreSQL/two readerSQL vào repo sau duyệt; chốt binding/thao tác/queue và retention; chạy C3 đủ thời lượng cùng phép so agent có kiểm soát. Các lựa chọn, mặt trái và bằng chứng cần thêm ở `CAN-MINH-QUYET.md`. Không tự sửa repo chính hay đóng task.

Ghi nhận tuân thủ: một lần đọc README seed lịch sử đã làm mật khẩu mẫu cũ xuất hiện trong tooloutput. Không dùng/chép giá trị đó; các log sau đọc qua redactor. Không có giá trị bí mật mới trong gói bàn giao. Không truy cập84/AWS, không ghiGitHub hoặc hai repo laptop. `prompt-ban-giao-Claude.md` là prompt bàn giao nguyên mẫu, chưa tự gửi sang agent khác.

Các job đo/tải/tiêm lỗi/M1 đã dừng; event không còn paused, timer phục hồi đã dừng. Tunnel của Codex đã đóng22:50:40Z sau kiểm cuối HTTP200. Minh tạo tunnel mới theo hướng dẫn; các container Oracle giữ chạy. `self-check.json` có17kiểm nhất quán đạt, không thay chấp nhận khoa học C1–C4. Checkpoint/DONE chốt giờ dừng lượt; không có kết luận hiệu quảM1/RQ5.

Gitstatus cuối cho thấy repo RCA có thay đổi tracked ở DECISIONS/STATE; không khẳng định repo sạch hoặc suy nguồn thay đổi từ snapshot cuối. Lượt này chỉ đọc hai repo,39pin nguồn P7 tại laptop vẫn khớp. Danh sách file bàn giao/hash ở `artifacts-sha256.json`; LOG và CHECKPOINT là nhật ký vận hành.

Ghi nh?n v?n h?nh: checkpoint cu?i ch?m nh?p h?n15ph?t (t?22:32Z t?i l?n c?p nh?t cu?i) khi ho?n thi?n t?i li?u. ?? c?p nh?t ??y ?? v? gi? LOG; kh?ng s?a m?c ho?c d? li?u ?? che ph?n ch?m.
