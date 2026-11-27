# Phản biện T-076

- **Người phản biện:** Codex. **Ngày:** 26/11/2026. **Bản:** SPEC đề xuất, SHA-256 trong biên bản kiểm bên dưới.
- **Công đoạn và quyền ghi:** soát SPEC, P9/P10 ngoài G0–G4. Minh cho ghi bản đầu `tasks/T-076-pr17-otel-may-84/REVIEW.md`. Người làm là Claude.
- **Đã đọc:** AGENTS của RCA và lab, STATE, SPEC, phiên cuối LOG, DT18 §2, hướng dẫn của cô, MRP P9/P10, WHY-08/09/89, DECISIONS 16–19/11 và LESSONS liên quan. FlashTicket `main=f178870`, PR #17 `bb84d64`, nhánh ghim `36a3725`. Lab ở `85ace52` và `c1da15f`. Hồ sơ T-067, T-070 §12 và Q4.
- **Tự soát độc lập:** đọc pipeline Collector → kho → gói ca/cảnh báo, workflow và script CD → manifest → pod, rồi đối chiếu LOG. Kết quả lượt này dựa trên thiết kế, mã nguồn và hồ sơ đã lưu.

## Kết luận chung

Đề nghị **chưa duyệt SPEC hiện tại**. Giữ mục tiêu làm lại chính PR #17 và cấu hình máy 84 qua CD. Có sáu điểm chặn từng quyết định cụ thể và một điểm hồ sơ. Task bao phủ một phần P9a và việc chuẩn bị tích hợp cho P10. Bằng chứng nghiệm thu cần xác nhận tuyến thu và ảnh hưởng vận hành. Ánh xạ ba tín hiệu lên đồ thị, chất lượng phát hiện/xếp hạng và demo RCA vẫn thuộc bước đánh giá của DT18-NV2/NV3 và hướng dẫn của cô.

## Các điểm

### R1. Metric có thể lẫn trước khi bộ đóng gói đọc được nhãn — CHẶN

- **Ở đâu:** SPEC C4, bước 6–7, phạm vi ghi lab và tiêu chí xong 3.
- **Sai gì:** Hai bộ đóng gói lấy trace/log từ file capture và lấy metric trực tiếp qua Prometheus. Tách file capture hay lọc nhãn trong dashboard không tách được metric đã bị gộp từ trước. Một span thử đơn lẻ cũng không kích thích được điều kiện của các luật p95/5xx.
- **Bằng chứng:** Lab `c1da15f:rca/lib/stage_m1.py:81` và `rca/online/stage_b.py:149–163` đều gọi `collect_metrics` khi thu thật. Bản khóa trong `rca/method.lock` trỏ `25550d2a5:src/m1/adapter_flashticket.py`. Ở đó, `TOTAL_RATE` gộp theo `service_name` và histogram gộp theo `le,service_name`. Ví dụ cùng `api-gateway` ở hai môi trường, lưu lượng đã cộng chung và histogram đã mất nhãn môi trường trước khi thành `prometheus.json`. Lab `gateway.yaml:115–153` còn đưa trace qua các connector sinh metric như `span_metrics` và `service_graph`. Prometheus đã được cấu hình đưa thuộc tính môi trường lên nhãn khi có, nhưng selector phải đặt **trước** từng phép gộp. Collector exp-app gắn `deployment.environment=exp` ở cả ba tín hiệu. Luật `rules.yaml:31` có điều kiện tối thiểu 30 request và `:577` lấy mẫu mới nhất. Dữ liệu chạy thật có thể vừa gây báo sai, vừa che tình trạng mất metric exp-app. [Quy ước nhãn OTLP của Prometheus](https://prometheus.io/docs/guides/opentelemetry/)
- **Bước và quyết định chịu ảnh hưởng:** lỗ hổng thiết kế chặn xác nhận C4 và bật xuất thật ở bước 8. Hồi quy hai ca V082 chứng minh lõi xử lý cùng đầu vào. Phát lại dev với `--prom-tu-file` đi tắt qua đường truy vấn đang chịu rủi ro.
- **Đề xuất sửa:** ưu tiên phân luồng ngay từ receiver riêng của 84. Chỉ receiver nội bộ vào file vòng thực nghiệm, và đường metric mà hai stage/luật đọc chỉ thấy exp-app. Nếu dùng chung Prometheus, lọc dương `exp` trên từng selector nguồn trước aggregate, kể cả tử số/mẫu số, và xác nhận label có trên metric sinh qua connector. Đặt phần tách ở lớp thu, giữ bản chụp phương pháp. SPEC cần chỉ rõ tuyến được chọn, file cần đổi, và thử cửa sổ trộn cho cả hai stage: trace/log có dấu phân biệt, metric 84 đủ để thay đổi truy vấn nếu lọc sai, metric exp vẫn vào gói và luật vẫn nhận đúng tín hiệu exp. Dùng chung kho giảm tài nguyên nhưng còn chia tải. Kho metric riêng giảm rủi ro lẫn, đổi lại tốn thêm cấu hình và tài nguyên. Ghi commit lab mới và hiệu ứng lên luật T-072 để phân biệt với baseline cũ, giữ UID và nghĩa luật. Nếu chưa tách được metric đầu vào thì giữ agent 84 chưa xuất dữ liệu.

### R2. CD chưa chuyển được cấu hình xác thực đến mọi workload — CHẶN

- **Ở đâu:** SPEC C3, bước 3, 6, 8 và Q4.
- **Sai gì:** Gắn token vào `ENV_<SVC>` mới đi đến file dotenv trên máy. SPEC chưa nêu cách token qua bộ lọc CD, Discovery lấy token thế nào, và nguồn nào thực hiện kiểm dương khi cổng chỉ mở cho 84.
- **Bằng chứng:** FlashTicket `f178870:.github/workflows/_deploy-service.yml:200–219` ghi dotenv và chuyển bộ manifest. `deploy/scripts/deploy-k8s-service.sh:180–236` chỉ đưa khóa được khai trong `deploy/k8s/examples/<service>.secret.env.example` vào Secret và bỏ hẳn nhánh sinh Secret cho `discovery-server`. `deploy/k8s/discovery-server/statefulset.yaml` chỉ có `configMapRef`. Thêm token GitHub không tự khắc phục hai chỗ này. Vòng apply manifest liệt kê các tên cố định, nên một file CA ConfigMap rời cần được nối vào tuyến thực thi. IP công khai OCI được ánh xạ tới IP riêng trên VNIC. Tên/IP mà client gọi phải khớp SAN của chứng chỉ, còn listener cần bind vào địa chỉ cục bộ hợp lệ. Bước 6 dùng máy tải để kiểm dương nhưng thiết kế chỉ cho IP egress 84. Kiểm từ máy tải có thể bị chặn trước TLS và không phân xử được lỗi token. [Cấu hình exporter OTLP](https://opentelemetry.io/docs/specs/otel/protocol/exporter/) · [Gán IP công khai trên OCI](https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/reserved-public-ip-assign.htm)
- **Bước và quyết định chịu ảnh hưởng:** thiếu đường thực thi chặn Q4 và triển khai bước 8. Q4 chưa được duyệt. Không có bằng chứng một pod đã gửi sai token.
- **Đề xuất sửa:** giữ TLS + bearer + giới hạn egress nếu xác nhận được IP. Chốt HTTPS, protocol tương thích Java agent 2.x, SAN, đường mount CA từ manifest CD thực sự apply, và đường truyền biến header từ secret vào từng loại workload. Dùng một giá trị giả để kiểm luồng Secret trước. Xác nhận người giữ bản đầy đủ của `ENV_<SVC>` trước bước 8 vì CD ghi thay toàn bộ dotenv. Chọn rõ thêm đường Secret cho Discovery hay tạm để Discovery tắt và khai độ phủ. Mở thêm đường Secret giữ độ phủ nhưng chạm script CD chung. `detect-changes.sh` hiện coi thay script deploy chung là recreate cho các workload K8s. Nếu chọn cách đó, bước 1 phải khai tập rollout thực tế và tránh kéo các workload ngoài phạm vi như Keycloak vào thay đổi ngoài ý muốn. Dùng CD do Minh duyệt để kiểm từ nguồn được phép và dành máy tải làm đối chứng bị chặn, hoặc khai trước một tuyến kiểm thử khác cùng cấu hình TLS/token. Quy định rõ hậu quả nếu egress đổi hoặc không xác minh được: giữ xuất thật tắt tới khi định tuyến đã kiểm. [Cấu hình Java agent và protocol mặc định](https://opentelemetry.io/docs/languages/java/configuration/)

### R3. Tuyến máy 84 đi thẳng tới gateway bỏ qua lớp lọc dữ liệu đang dùng — CHẶN

- **Ở đâu:** SPEC C2, C3, mục Không lộ bí mật, bước 3–6 và Q1.
- **Sai gì:** SPEC kiểm token và khóa riêng trong Git, cùng hình dạng log sau khi đến Loki. B16 §6 yêu cầu loại trường nhạy cảm trước khi ghi/xuất, dùng sentinel giả và kiểm điểm nhận. TLS xác thực được tuyến vận chuyển. Nó vẫn vận chuyển trường đã thu nhầm.
- **Bằng chứng:** Agent exp-app chạy `filter/health` và `transform/sanitize` trong pipeline trace của `observability/collector/agent-docker-host.yaml:161–182,225–234` để bỏ query URL trước khi xuất. Gateway `gateway.yaml:115–153` hiện đưa trace/log tới Tempo/Loki sau memory limiter và batch, không có các processor đó. PR `bb84d64` có test stdout B16 với sentinel, và entrypoint Booking cưỡng bức `OTEL_LOGS_EXPORTER=none`. Mở OTLP log là đường xuất khác. Q4 kiểm đúng 13 trường cho đường filelog exp-app, đọc từ `results/T-070/don/q4/kiem-tin-hieu.json#/log/booking-service/du_truong_B16` khi đối chiếu dòng tổng hợp. Điều này chưa chứng minh schema hay tính sạch của OTLP log trực tiếp. Chưa có quan sát xác nhận rò rỉ thật.
- **Bước và quyết định chịu ảnh hưởng:** chặn bật trace thật và quyết định mặc định Q1(a). Nếu appender xuất body/MDC khác stdout đã làm sạch, trường B16 có thể mất và dữ liệu nhạy cảm có thể nằm trong kho trung tâm.
- **Đề xuất sửa:** ưu tiên Q1(c) cho lần bật đầu nếu Q1(a) chưa có bằng chứng từ bản chạy tương đương. Chốt tập thuộc tính trace/metric được xuất của agent, dùng lớp lọc Collector làm dự phòng, chạy một đường tổng hợp có sentinel giả và kiểm bản ghi thực nhận trước khi chuyển endpoint thật. Nếu log là yêu cầu của lần bật đầu, dùng đường OTLP chỉ sau khi cùng mẫu cho đủ trường bắt buộc theo schema, nối đúng trace/span ở vị trí đã khai, không lộ sentinel và không thu trùng. Nếu appender không giữ được schema, phương án (b) giữ log JSON stdout nhưng thêm vận hành DaemonSet. Q1(c) ít thay đổi nhất và còn thiếu log trên 84, do đó không nghiệm thu đủ ba tín hiệu của 84 hay dùng H8 ở đó. Nhu cầu tích hợp ba tín hiệu cho thực nghiệm tiếp tục dựa trên exp-app và được nghiệm thu riêng.

### R4. Tiêu chí lên máy 84 bỏ p95 đã hứa, điều kiện hoàn tác chưa đủ — CHẶN

- **Ở đâu:** SPEC C5, bước 4, 8–9, tiêu chí xong 4 và rủi ro dung lượng.
- **Sai gì:** C5 yêu cầu p95 không xấu quá ngưỡng khai trước. Bước 9 và tiêu chí 4 chỉ yêu cầu Ready, không OOM/restart và có tín hiệu. Một pod ổn định vẫn có thể phục vụ chậm hoặc tăng lỗi. Giả định quay lại bằng digest cũng cần kiểm điều kiện của CD trước khi bật.
- **Bằng chứng:** Ở `f178870`, Booking giới hạn 768 MiB tại `deploy/k8s/booking-service/deployment.yaml:45`. CD có chế độ rollback từng service. `deploy/scripts/deploy-k8s-service.sh:170–175` đòi có revision `previous` và digest đúng revision đó, rồi phục hồi manifest đã lưu. Dockerfile `main` vẫn khởi chạy Java trực tiếp. Build một service chỉ cho bằng chứng của image được chọn. p95 Q4 là từ exp-app ở tải thử, không phải nền máy 84. Gateway lab dùng chung memory limiter và vùng ghi vòng hiện hữu. Nếu nối 84 vào chung công suất, disk 44% ở bản kiểm kê trước đợt dọn không cho biết tốc độ tăng hoặc số tín hiệu bị rơi dưới tải chạy thật.
- **Bước và quyết định chịu ảnh hưởng:** chặn quyết định merge có bật agent và kết luận không ảnh hưởng hệ thống. Mức overhead và lưu lượng thật còn OPEN. Hai khả năng phù hợp với hiện trạng là agent vừa ngân sách tài nguyên, hoặc rollout khỏe nhưng ứng dụng/Collector chậm hay rơi tín hiệu do tải bổ sung.
- **Đề xuất sửa:** ghi vào bước 9/tiêu chí 4 nguồn đo, cửa sổ nền cùng luồng, p95 và tỷ lệ lỗi, giới hạn/điều kiện dừng được Minh duyệt trước. Nếu thiếu nền 84, dùng một kiểm hành trình ngắn tương ứng qua tuyến hệ thống đã được duyệt trước/sau và ghi giới hạn về tải. Bước 4 nên dùng kiểm khởi động có agent đại diện cho Booking và Assistant nếu Q2(a), cùng build hai kiến trúc trong CD hiện hữu. Chốt lấy mẫu và giới hạn nhận cho 84 ban đầu, theo dõi exporter drop/queue và tuổi mẫu thực nghiệm trong đúng giờ theo dõi đã dự kiến. Trước merge xác nhận cách lấy revision/digest có thể quay lại bằng CD và ai bấm. Ưu tiên hoàn tác CD từ bản trước sẵn có để đáp ứng một PR, không dựa vào mở thêm PR khẩn. Nếu chưa có tuyến quay lại qua CD, chọn triển khai bản agent mặc định tắt và trình cách bật qua CD hiện hữu, hoặc lùi merge đến khi đủ điều kiện. Chi phí chính là cửa sổ theo dõi đã có, smoke test ngắn và đọc thông tin revision qua người vận hành/CD được phép. Số đo overhead thật vẫn chỉ có sau rollout.

### R5. Ghép kiểm B16 cũ nguyên trạng sẽ xung đột với Assistant chỉ có agent — CHẶN

- **Ở đâu:** SPEC C1, C6, bước 2–4 và Q2.
- **Sai gì:** Kế hoạch giữ CI kiểm B16, đồng thời thêm agent cho Assistant mà chưa làm log B16. SPEC chưa chỉ ra cách ghép để CI vẫn có nghĩa và không vỡ ở đường mới.
- **Bằng chứng:** PR `bb84d64:.github/workflows/_maven-verify.yml:94` gọi verifier vô điều kiện với `target/b16-log-samples.jsonl`. Verifier mở file ngay và lỗi nếu file trống. `git grep -n b16-log-samples bb84d64 -- ':!*.yml'` tìm bảy writer trong bảy service có log B16, không có Assistant/Keycloak. Ở `f178870`, `ci.yml` chạy workflow dùng chung cho Maven được chọn, Assistant dùng lệnh `mvn` theo registry và có đoạn nạp môi trường MVC ngoại tuyến trong workflow. Khi thêm Dockerfile/entrypoint cho Assistant, service vào matrix. Nếu giữ cả rule `deploy/observability/*` của PR cũ, rule cũng chọn Assistant vì chỉ loại Keycloak và frontend.
- **Bước và quyết định chịu ảnh hưởng:** mâu thuẫn khi chuyển nguyên hunk CI. Chặn kỳ vọng CI xanh với Q2(a). Đây là thất bại suy được từ đường mã nếu ghép theo cách đó, chưa phải một lượt CI đã thất bại.
- **Đề xuất sửa:** giữ bước validate bắt buộc cho tập service B16 định danh rõ và cho các thay đổi schema/verifier chạy lại đúng tập đó. Giữ setup trợ giúp Maven/Assistant của main. Local dùng lệnh từ registry, không dùng `mvnw` cho mọi service. Chọn Q2(a) nếu cần trace Assistant ngay. Đổi lại log Assistant vẫn ngoài B16. Q2(b) mở thêm schema/test, còn Q2(c) bỏ luôn độ phủ Assistant. Dùng phân nhánh theo service có hợp đồng B16, tránh coi file mẫu vắng là pass cho service vốn bắt buộc có.

### R6. Lý do bỏ build đa kiến trúc sai, có nguy cơ bỏ nhầm hunk còn dùng — CHẶN

- **Ở đâu:** SPEC C1, bước 1–4, Q3 và pha 4.
- **Sai gì:** Q3 ghi “CD của main build amd64”. CD hiện đã xuất hai kiến trúc. Hunk còn lại của PR ở workflow build gắn `SERVICE_VERSION`, có mục đích khác.
- **Bằng chứng:** `git show f178870:.github/workflows/_deploy-service.yml` dòng 79–82, 118 cài QEMU arm64 và build `linux/amd64,linux/arm64`. `git diff f178870...bb84d64 -- .github/workflows/_deploy-service.yml` cho thấy hunk thêm `SERVICE_VERSION=github.sha`, trong khi Dockerfile PR mặc định `local-dev`. OCI label revision trong main không tự cấp giá trị `service.version` cho telemetry. `test-environment/scripts/build.sh` lab truyền build arg này và tự build bảy Spring service ARM. Dockerfile Keycloak trong PR có thay đổi bật native tracing. Agent exp-app có receiver riêng `otlp/keycloak`. SPEC cho phép cân nhắc bỏ hunk Keycloak ngoài phạm vi 84, nhưng pha 4 không thể mặc định tuyến đó vẫn hoạt động.
- **Bước và quyết định chịu ảnh hưởng:** chặn duyệt Q3 theo lý do hiện tại và tuyên bố nhận diện bản build đúng B16. Mục pha 4 chỉ phụ thuộc nếu Minh duyệt ghim lại.
- **Đề xuất sửa:** bỏ phần đa kiến trúc thừa của PR theo bảng từng hunk, giữ hai platform ở CD main và giữ cách truyền revision cho service có telemetry. Kiểm `service.version` bằng revision của image, tránh nhận `local-dev` là đạt. Dùng lại image dual-arch của CD nếu tương đương. Bản exp-app có profile `rca-test` riêng thì dùng build ARM đang có. Khi xét pha 4, kiểm trước các phụ thuộc Compose/Keycloak trong bảng C1. Nếu chưa quyết giữ tuyến Keycloak cho exp-app, ghi rõ tín hiệu phụ thuộc và hoãn phần nghiệm thu bị ảnh hưởng. Chốt `origin/main` và đầu PR thật ở thời điểm dựng/đẩy, dùng lease khớp head đã soát để giữ cập nhật của nhóm.

### R7. Căn cứ triển khai lab và quyền ghi cần ghi đúng — KHÔNG CHẶN

- **Ở đâu:** SPEC Đầu vào, Phạm vi ghi, bước 5–7 và Q5.
- **Sai gì:** `85ace52` là pin của Q4, còn `main` lab hiện là `c1da15f`. Mục quyền máy obs trỏ bước 5 (phản biện) thay vì 6–7. Q5 có đề xuất ngoại lệ đúng hướng, nhưng §12 hiện quy định chỉ đọc và danh sách phạm vi ghi của SPEC chưa nêu rõ mục ghi ngoại lệ cùng thời điểm có hiệu lực.
- **Bằng chứng:** `git -C D:/Project/flashticket-rca-lab ls-remote origin refs/heads/main` trả `c1da15f`. Diff hai commit có thay đổi launcher/build và đường RCA trực tuyến. Diff riêng gateway, Collector app, Prometheus, hai stage và luật cảnh báo không đổi. `AGENTS.md:251`, SPEC dòng 76–87 và bước 5–7. Q4 README phân biệt commit chạy và các đính chính. Không thấy bằng chứng đã thực thi ngoại lệ.
- **Bước và quyết định chịu ảnh hưởng:** không chặn kiểm kê chỉ đọc. Trước khi thi hành phải có Q5 được Minh duyệt, căn cứ chạy mới và quyền đúng cho bước 6–7. Giữ hồ sơ lịch sử đúng pin để tái lập.
- **Đề xuất sửa:** ghi `85ace52` cho bằng chứng Q4, dựng thay đổi trên lab main đã xác nhận, chỉnh tham chiếu bước 6–7. Khi Minh duyệt Q5, ghi đúng ngoại lệ ở §12 trước khi ghi repo hệ thống. Nêu file và phạm vi theo bảng C1 trước thay đổi lớn, cùng quyền đẩy nhánh PR. Ghi các yêu cầu/điểm Minh quyết mới vào DECISIONS và lý do tuyến cách ly/xuất thật vào WHY sau khi được duyệt nội dung, trước khi viện làm căn cứ kết quả. Hoãn Q6 để tránh gộp đổi bản thử nghiệm vào triển khai 84.

## Đối chiếu các lượt trước

Đây là lượt phản biện đầu của T-076. Các đính chính Q4 dùng làm nguồn cho hiện trạng cũ.

## Tuân thủ quy trình

STATE và LOG cùng ghi SPEC đang chờ duyệt. Yêu cầu một PR và bật agent qua CD là USER_CONFIRMED. Q1–Q6 vẫn là đề xuất. Bản soát này có quyền ghi đúng một file. Không thấy đầu ra triển khai T-076 trong phạm vi đã kiểm. Nhãn `exp`/môi trường là thông tin nguồn thu, khác nhãn ca lỗi. Hai stage hiện nhận mã mờ và mốc theo chế độ, và kiểm định này chưa thay mốc, nhãn, tập ca hay lõi xếp hạng. Bản chụp phương pháp đã ghim; thay đổi pipeline hoặc luật cần ghi commit lab để tái lập và không dùng kết quả cũ như bằng chứng cho rollout mới.

## Điều đã kiểm và thấy đúng

- Dựng lại ngay nhánh PR #17 phù hợp yêu cầu một PR. `gh pr view 17` xác nhận OPEN/CONFLICTING. `git rev-list --left-right --count f178870...bb84d64` cho 92/10. `git diff --stat f178870...bb84d64` cho 124 file, +5.028/−214. Đầu nhánh main lấy từ API nhánh và khớp `f178870`. Tập 13 file xung đột là số ghi trong SPEC. Lượt này xác nhận trạng thái CONFLICTING qua GitHub, chưa tính lại danh sách từng file. [PR #17](https://github.com/levanminh04/flash-ticket-platform/pull/17)
- `git rev-list --count 640dbaf..f178870` và đếm `git diff --name-only 640dbaf f178870` cho 52 commit và 171 file. Registry main có cả Assistant và K8s. Nhánh build và nhánh recreate đều có trong CD. Kiểm pod và đăng ký Eureka đã có, dùng được cho phần rollout của SPEC.
- SHA-256 khớp manifest cho `T-067/kiem-tin-hieu.md`, `T-067/kiem-tin-hieu/kiem-tin-hieu-lan1.json`, `T-070/don/q4/README.md`, `T-070/don/q4/kiem-tin-hieu.json`, `T-070/kiem-ke/README.md`, `T-070/kiem-ke/m1-ban-chup.tsv`. Dòng adapter trong bảng kiểm kê khớp `rca/method.lock`. Hai JSON tín hiệu có `#/log/booking-service/du_truong_B16 = 936`. Kết quả xác nhận đường thu trên bản ghim exp-app ở cửa sổ đã đo.
- WHY-08/09 giải thích giữ lõi RCA chung và vì sao phải đo đủ trường/loại span từ phía instrumentation. WHY-89 giải thích vai trò `outcome` của H8. Các căn cứ này ủng hộ tách tại đường thu và kiểm schema. Lựa chọn đường OTLP log, tách metric và tỷ lệ lấy mẫu cho 84 vẫn cần bằng chứng riêng.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. Đã soát SPEC theo DT18, MRP, B16 và đường thực thi tại các revision nêu trên.
2. Chỉ thêm `tasks/T-076-pr17-otel-may-84/REVIEW.md`. Repo RCA khi đọc ở `672391b9b`. SHA-256 của SPEC được soát là `b3bb3583b0434c0d8465dcb6b5f31fea840263b2a505e96f73f71195d3d1b336`.
3. Kiểm metadata PR/main qua GitHub, đọc diff Git, lần qua CD và nguồn thu/thành phần đọc dữ liệu. Kiểm sáu file đối chiếu theo manifest, sáu file khớp. Không mở dữ liệu khóa, không vào máy 84, không chạy thực nghiệm hay commit.
4. **Đề nghị tiếp tục một lượt đáp phản biện trước khi duyệt SPEC.** Giữ mục tiêu một PR và CD. Ưu tiên giữ log 84 tắt nếu tuyến OTLP chưa qua kiểm B16, chỉ mở trace/metric sau khi xác nhận cách ly và đường Secret, giữ dual-arch vốn có của main và quyền quyết pha 4 riêng. Bằng chứng còn thiếu là IP egress và đường pod thực nhận token, kiểm đối chứng hai nguồn theo cả ba tín hiệu, độ sạch/độ phủ của dữ liệu nhận được, nền và đường hoàn tác của rollout. Mỗi mục có cách thu và hệ quả nếu còn thiếu trong R1–R7. Minh quyết đề xuất sửa và phạm vi từng bước. Chưa có bất đồng từ người làm.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/SPEC.md (bản đề xuất).
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P9, P10, công việc tích hợp ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude là người làm, Codex là người phản biện.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/SPEC.md, results/T-070/don/KE-HOACH-DON.md §12, DT18, hướng dẫn của cô và MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, chưa có phản hồi.
- Code và kết quả liên quan: D:/Project/flash-ticket-platform (main f178870, PR #17 bb84d64, nhánh ghim 36a3725), D:/Project/flashticket-rca-lab (85ace52 và c1da15f), results/T-067/SHA256SUMS, results/T-070/don/q4/SHA256SUMS. Các nguồn này dùng ở chế độ chỉ đọc.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi Minh cấp quyền ghi rõ trong lượt đáp.

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

Người làm điền bảng khi được Minh cấp quyền. Để trống cột Minh quyết.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN | RCA `25550d2a5:src/m1/adapter_flashticket.py:24–36`: `sum by(service_name)`, `sum by(le,service_name)`, không lọc môi trường, nằm trong bản đã khóa. Gateway còn ghi trace vào file `capture` (`gateway.yaml:114–153`). Bản 2 (Minh duyệt viết 26/11): tách ở lớp thu bằng `collector-production` + `prometheus-production` riêng, không đi qua gateway/`capture`; không sửa `stage_*`, luật, bản phương pháp. Kiểm cửa sổ trộn cho hai bộ đóng gói và luật ở bước 7. Mặt trái: thêm 2 container (obs còn ~10 GB RAM). | |
| R2 | Đúng; CHẶN | `deploy-k8s-service.sh:196–236` @`f178870`: chỉ khóa khai trong file mẫu vào Secret; `discovery-server` không có Secret. Bản 2: khóa token và `OTEL_AGENT_ENABLED` vào mục `# Optional` của 7 file mẫu; CA công khai qua ConfigMap, entrypoint ghi ra `/tmp` (pod không đặt `readOnlyRootFilesystem`); không sửa script CD chung; discovery chưa bật (khai phủ); kiểm lọc khóa bằng dotenv giả ở bước 4; HTTPS OTLP/HTTP, SAN = IP công khai obs, nghe IP nội bộ; kiểm từ nguồn được phép tạm, máy tải làm đối chứng bị chặn. Header/CA qua biến môi trường **chưa kiểm**. `ENV_<SVC>` ghi thay toàn bộ → Q9. | |
| R3 | Đúng; CHẶN | `gateway.yaml` chỉ `memory_limiter`, `batch`; agent exp-app có `filter/health`, `transform/sanitize` (`agent-docker-host.yaml:161–182,225–234`). Bản 2: Collector riêng có lớp lọc tương đương, kiểm sentinel/query URL ở bước 6; Q1 đổi đề xuất sang (c) — lần đầu không gửi log máy 84. | |
| R4 | Đúng; CHẶN | C5 bản 1 có p95 nhưng bước 9/tiêu chí 4 bỏ mất. `cd.yml:6–18` có `restart`, `rollback`; `rollback` cần `previous` (`deploy-k8s-service.sh:171–175`). Bản 2: merge với agent tắt; bật/tắt bằng `ENV_<SVC>` + CD `restart` (không cần PR thứ hai); ngưỡng Q7 khai trước (p95 phía client từ kiểm hành trình ngắn, lỗi, OOM/restart, rơi dữ liệu exporter, tuổi mẫu thực nghiệm); kiểm khả năng `rollback` trước merge; tỷ lệ lấy mẫu Q8. Kiểm hành trình ngắn không đại diện tải thật (ghi giới hạn). | |
| R5 | Đúng; CHẶN | `_maven-verify.yml:94` @`bb84d64`: B16 chạy cho mọi service trừ keycloak. Bản 2: kiểm theo danh sách service có hợp đồng B16, thiếu file mẫu ở service trong danh sách = lỗi; Assistant (a) ngoài danh sách; giữ cách main cài Maven/registry. | |
| R6 | Đúng; CHẶN | Lỗi của người làm: `_deploy-service.yml:79–82,118` @`f178870` đã build `linux/amd64,linux/arm64`. Bản 2: Q3 sửa lý do; giữ hunk `SERVICE_VERSION`; kiểm `service.version` = revision; Keycloak tracing xét trong bảng C1, pha 4 kiểm phụ thuộc trước; `--force-with-lease`. | |
| R7 | Đúng; KHÔNG CHẶN | Lab main `c1da15f`; quyền obs trỏ bước 6–7; Q5 ghi trước khi ghi repo FlashTicket. Bản 2 đã sửa ba chỗ. | |
