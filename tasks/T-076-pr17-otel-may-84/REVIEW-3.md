# Phản biện T-076 — SPEC bản 4

- **Người phản biện:** Codex. **Ngày:** 27/11/2026. **Người làm:** Claude.
- **Công đoạn và quyền ghi:** soát SPEC bản 4, P9/P10, ngoài G0–G4. Minh cho ghi riêng `tasks/T-076-pr17-otel-may-84/REVIEW-3.md`.
- **Đã đọc:** AGENTS, STATE, ba bản SPEC trước và SPEC bản 4, LOG T-076, bảng file PR, hồ sơ kiểm cục bộ, T-067 LOG phần dựng/hoàn tác, T-070 §10 và §12, hồ sơ Q4, cấu hình W4/W5, nháp W7 của T-074, DT18 §2, hướng dẫn của cô, MRP P9/P10, B16 §2–8, WHY và quyết định liên quan. Đối chiếu hai bản phản biện và các bảng đáp sau khi tự soát.
- **Mã nguồn và tính toàn vẹn:** RCA HEAD `672391b9b`, FlashTicket refs cục bộ `f178870` / `bb84d64` / `36a3725d`, nhánh dựng lại `ae5a870`, lab `c1da15f`. SHA-256 của SPEC bản 4 là `996e7f2e10ef3eafcc4502dadfa4107bebc3cd0de6cca8761adb5bf2d07ef353`. Bản 3 khớp dấu hash ghi trong LOG phiên 5. Kiểm đủ 12/12 mục trong `results/T-070/don/q4/SHA256SUMS`. Không tìm thấy manifest cho đầu ra T-076 đang có. Các đếm trên file thô T-076 dưới đây mô tả nội dung đang lưu.
- **Tự soát độc lập:** lần đường CD → Secret → pod, Compose → tải → ba tín hiệu → luật → bộ nhận → RCA → Grafana. Kiểm cấu hình và file kết quả gốc, sau đó kiểm các phản hồi cũ. Đọc exp-app và exp-obs qua wrapper được phép.

## Kết luận chung

Giữ hướng H1 + H4 và dùng chính PR #17. **Chưa duyệt nguyên SPEC bản 4**. Phần A còn thiếu điều kiện trước merge để bảo đảm các pod lên với agent tắt và xử lý được rollout hỏng. Phần B còn vướng quyền bật tuyến RCA trực tuyến và tiêu chí diễn tập chưa phân biệt được sự cố do tiêm với cảnh báo lúc đổi bản. Tách quyết định dựng bản demo khỏi quyết định khóa môi trường W7.

Phần A hỗ trợ P9a qua log B16 và chuẩn bị cấu hình trace/metric. Phần B là lát cắt tích hợp của P10 và DT18-NV2/NV3 trên exp-app. Một diễn tập đạt sẽ xác nhận đường đi và giao diện cho một ca. Đánh giá chất lượng phát hiện, vùng ảnh hưởng, xếp hạng, nhiều mức tải của NV1/P10 và hoàn tất P9b vẫn cần các gói tương ứng. Hướng dẫn của cô yêu cầu phần phát hiện và chẩn đoán thấy được trong demo. MRP P10 còn nêu phần giải thích LLM, hiện tích hợp W8 đang hoãn theo DECISIONS 23/11. Một lượt ở T-076 có thể dùng làm lượt đầu của W9a nếu khớp kịch bản. Kế hoạch W9a §8 vẫn nêu hai lượt diễn tập và phát lại offline.

## Các điểm

### R1. Công tắc mặc định tắt chưa bảo đảm tắt khi CD triển khai — CHẶN

- **Ở đâu:** SPEC C2, C4, bước 5–7, tiêu chí xong 2 và §Mở rộng.
- **Sai gì:** SPEC suy từ mặc định của entrypoint sang trạng thái thật của pod sau merge. Việc giữ `OTEL_AGENT_ENABLED` trong file mẫu tạo đúng đường để Secret hiện có bật agent ngay khi CD có image mới.
- **Bằng chứng:** FlashTicket `ae5a870:.github/workflows/cd.yml:3–5` chạy khi đẩy main. `_deploy-service.yml:163,205–207` lấy `ENV_<SVC>` của GitHub, ghi lại dotenv. `deploy/scripts/deploy-k8s-service.sh:198–221` chấp nhận khóa có tên trong file mẫu và có giá trị. Các Deployment có `envFrom` Secret. `services/booking-service/docker-entrypoint.sh:16–26` dùng `-javaagent` nếu là `true`. File mẫu để trống chỉ quy định khóa tùy chọn. Log phiên 4 báo pod của bản cũ chưa chạy agent. Image bản cũ chưa có agent nên tình trạng đó không phân xử được khóa trong Secret CD đang thiếu, false hay true. Bản thử `agent/tat-agent/{traces,metrics}.jsonl` đều 0 byte trong phép kiểm cục bộ. Đó là đối chứng hợp lệ cho cấu hình tắt của lượt thử.
- **Bước và quyết định chịu ảnh hưởng:** chặn merge ở bước 6 và xác nhận H1. Khi khóa đã là true, image mới có thể khởi động agent, dò gửi tới Service chưa triển khai và tăng tải JVM. Khi giá trị có mặt nhưng sai định dạng, entrypoint thoát 64. Chưa có bằng chứng hai tình huống này xảy ra trên 84.
- **Đề xuất sửa:** chuyển việc xác định người giữ `ENV_<SVC>` lên trước merge. Người giữ xác nhận các workload CD sẽ triển khai có khóa thiếu hoặc `false`, chỉ báo kết luận, giữ nguyên các khóa khác và dùng tuyến CD của nhóm. Đọc plan CD cho diff thực sự sẽ merge. Dùng bước 4 kiểm file mẫu → Secret → env container với dữ liệu giả, gồm đường tắt và đường bật. Sau merge đối chiếu status đã rollout đúng revision và trạng thái tắt. Giữ công tắc bây giờ giúp mở rộng bằng cấu hình sau này, đổi lại cần xác nhận từ người giữ Secret. Nếu Minh muốn cưỡng chế tắt bằng mã trong bản A thì lần mở rộng phải sửa thêm manifest hoặc entrypoint. Tôi đề xuất giữ công tắc và hoãn merge nếu người giữ chưa xác nhận được.

### R2. C4 thiếu tiêu chí và hành động cho bản production agent tắt — CHẶN

- **Ở đâu:** SPEC C2/C4, bước 6–7, Q7 và §Rủi ro.
- **Sai gì:** C4 chỉ kể log/nhận diện host là thay đổi có tác động. C2 giữ cả cấu hình ngoài Java agent. Một lần đo bộ nhớ cũ theo pod chưa đủ làm đối chứng 10%, và bản 4 bỏ điều kiện xử lý khi theo dõi thấy regression sau một rollout đã thành công.
- **Bằng chứng:** `git grep -n SPRING_AUTOCONFIGURE_EXCLUDE ae5a870 -- deploy/k8s` tìm thấy cấu hình loại Lettuce observation ở Gateway, Booking và Assistant. `ae5a870:deploy/k8s/booking-service/configmap.yaml:40` là biến Spring Boot đọc độc lập với nhánh Java agent trong entrypoint. Có thể cấu hình này dư vì service vốn chưa dùng auto-configuration đó. Cũng có thể nó thay đổi nguồn observation của service. Pod Ready không phân xử hai trường hợp. LOG phiên 4 lúc 05:07Z ghi Booking 654 và 411 MiB, Payment 689 và 368 MiB ở hai replica, có rollout đồng thời; chênh giữa các replica cùng service đã vượt ngưỡng đề xuất. Bản 3 C5 và bước 8 từng ghi nền, kiểm client và đích về bản A trong giai đoạn agent tắt. `deploy-k8s-service.sh:170–175,261–271` chỉ hoàn tác nếu digest khớp revision `previous`, mục này có thể đổi sau một CD thành công khác. Tự phục hồi khi rollout fail không xử lý trường hợp pod Ready nhưng chức năng suy giảm sau đó.
- **Bước và quyết định chịu ảnh hưởng:** chặn duyệt Q7 như tiêu chí ảnh hưởng và chặn merge nếu chưa có phương án xử lý khi luồng thật suy giảm. Không quy mức dùng RAM khác nhau cho riêng agent hoặc riêng PR.
- **Đề xuất sửa:** trong C2 liệt kê các cấu hình ảnh hưởng ngay khi agent tắt. Với loại Lettuce, ưu tiên chỉ áp khi bật agent, hoặc giữ nếu người làm chứng minh không đổi hành vi cần giữ của từng service trong cấu hình thật. Trong cửa sổ rollout đã có, chốt lại nền sát thời điểm merge, cùng luồng/tải, định nghĩa cách so theo workload khi replica đổi và báo riêng thiếu mẫu. Ghép mức RAM với kiểm chức năng ngắn đã khai trên tuyến hệ thống được phép, dùng số liệu đọc sẵn nếu đủ. Nếu chỉ có số liệu pod, giới hạn kết luận ở rollout và tài nguyên quan sát được. Trước merge xác định người bấm và revision/digest về được, ghi tiêu chí dừng và xác nhận khi nào đường đó hết hiệu lực. Cách này giữ CD hiện hữu và khoảng theo dõi 60 phút. Nếu thiếu quan sát phía client hoặc thiếu đích quay lại, trình Minh chấp nhận phạm vi hẹp hơn hoặc dời merge.

### R3. Bước 9–10 cần ghi trên tuyến hiện bị khóa quyền — CHẶN

- **Ở đâu:** SPEC §Phạm vi ghi, Phần B, C6, bước 8–10 và tiêu chí xong 3–4.
- **Sai gì:** SPEC giới hạn exp-app vào build/đổi service, ghi “Obs: không ghi thêm” và bỏ máy tải khỏi phạm vi ghi. Đường chạy Q4, nền ×1 và diễn tập cần cả máy tải và obs. Điều kiện “qua T-070 REVIEW-5” hữu ích nhưng chưa cấp các thao tác này. Bước 8 cũng gọi `hieu_luc.py` là chỉ đọc trong khi script tạo file cấu hình và `so-sanh.json`.
- **Bằng chứng:** Đọc 27/11 qua `ssh.sh obs`, lab `c1da15f`, `docker ps` có Grafana và `flash-ticket-t072-bo-nhan`, không có container `t073-webhook` đang chạy. LOG T-073 mục hoàn tác và `results/T-073/trien-khai-e5.md` §5 ghi gỡ integration T-073 và trả dashboard về ca cũ. `c1da15f:rca/online/README.md` yêu cầu tạo spool, bật webhook, nối contact point, chạy bộ điều phối và chọn đầu ra mới. `load/controller/tai_linux.py:136–146,182,189–221,242–270` kiểm STOP/bảo trì, tạo token pool và ghi đầu ra trên máy tải, ghi nhật ký/trạng thái obs. Quan sát lúc đọc: STOP và hai marker bảo trì đều vắng. Điều này chỉ nói guard lúc đọc chưa bị các file ấy chặn. `test-environment/scripts/hieu_luc.py` gọi `os.makedirs` và `open(...,'wb')`. `docs/STATE.md` dòng T-070 và prompt kiểm lại vẫn để riêng đường tải chuỗi và bật RCA sau sửa.
- **Bước và quyết định chịu ảnh hưởng:** chặn Q5 theo lịch “ngay sau merge” nếu bao gồm vận hành bước 9–10, chặn tiêu chí demo. Kiểm mã, build độc lập và soát cấu hình có thể chuẩn bị trước trong quyền tương ứng. Tạo cấu hình hiệu lực, phát tải, tiêm lỗi và bật tuyến online cần phạm vi thực thi rõ.
- **Đề xuất sửa:** giữ REVIEW-5 và kết luận của Minh về hai đường vận hành làm điều kiện dùng đúng đường tương ứng. Ở bước 8 dùng diff đọc trước, chỉ định thư mục đầu ra khi dựng cấu hình. Nêu đúng nơi cần ghi cho lượt demo riêng: điều khiển tải và đầu ra trên máy tải, dấu vết tiêm/gỡ trên exp-app, spool/bộ điều phối/contact point và nguồn dashboard trên obs, cùng đường hoàn tác. Nếu nhóm khác nhận khâu bật lại, ghi người chịu trách nhiệm và bằng chứng tuyến đã sẵn sàng trước khi tiêm. Ưu tiên dùng gói vận hành hiện có sau khi đối chiếu `c1da15f` và đường mới. Phát lại offline có thể làm phương án trình bày dự phòng, cần ghi tiêu chí live còn mở. Chi phí chuẩn bị chính là quyền vận hành và một lần xác nhận đường nhận. Không cần chạy lại E5 chỉ để bật dịch vụ.

### R4. Tiêu chí diễn tập có thể đếm nhầm một sự cố đã có — CHẶN

- **Ở đâu:** SPEC C5, C6, bước 9–10, tiêu chí xong 3–4 và Q6.
- **Sai gì:** Bản 4 nêu so p95 từng route và “diễn tập một vòng đạt” nhưng chưa định nghĩa trạng thái đầu, cửa sổ dữ liệu, ca mới cần thấy trên dashboard, hoặc giới hạn thời gian. Nhìn một số p95 thấp hoặc thấy Grafana hiện một ca chưa phân biệt được luật đủ mẫu, đợt khởi động lại, ca lưu sẵn và lỗi vừa tiêm. “Đồ thị dịch vụ” cũng có thể chỉ là sơ đồ tổng thể.
- **Bằng chứng:** Hồ sơ Q4 đã kiểm 12 hash. `q4/README.md` mục 1 ghi luật mất mẫu Gateway cháy từ lúc dời dịch vụ tới đầu lượt mua vé. Mục 2 ghi bốn luật p95 cháy trong phần đầu lượt rồi tự hết. WHY-105–110 và `c1da15f:observability/grafana/provisioning/alerting/rules.yaml` giải thích cửa sổ 5 phút, số request tối thiểu, thời gian duy trì và nhánh mất tín hiệu. Lưới/route thiếu mẫu có thể im dù chưa đủ căn cứ. T-073 dùng `startsAt` làm t̂, cửa sổ ±600 s và thời gian chờ F. `results/T-073/khai-truoc-e5.json` đã định nghĩa đích thời gian cho lát cắt E5 cũ. `rca/online/README.md` phân biệt phát lại dev và chạy từ webhook.
- **Bước và quyết định chịu ảnh hưởng:** chặn tiêu chí “demo đạt” và chọn lại ngưỡng chỉ từ một lần so p95. Khởi động lạnh, đổi phân bố độ trễ và lỗi đường thu đều còn là giải thích khả thi. Q4 đo đường tín hiệu, hồi quy trên hai gói dev cũ đo tính lặp lại đầu vào cũ, diễn tập đo tích hợp trên bản mới.
- **Đề xuất sửa:** trước tiêm, dùng lượt nền dự kiến để xác nhận đủ mẫu, ổn định theo trạng thái luật thật, có dữ liệu tiền sự cố cho cửa sổ online và không còn sự cố lớp hệ thống cũ chen vào. Ưu tiên khai trước đích thời gian theo hợp đồng W5 đang dùng nếu Minh chấp nhận cho demo, kiểm ID và t̂ của ca mới xuyên suốt webhook → G1 → dashboard, thấy đồ thị con/vùng nghi ngờ và danh sách hạng có bằng chứng của ca đó. Ghi nhận cảnh báo lớp quan sát riêng. Sổ tiêm chỉ dùng sau chạy để đối chiếu, giữ mốc vào RCA từ `startsAt`. Nếu luật im do thiếu mẫu, kiểm đường thu hoặc kéo dài nền trong thời lượng đã duyệt trước khi cân nhắc hiệu chỉnh. Nếu nền khỏe có đủ mẫu vẫn cháy, trình T-072 xét ngưỡng cho demo. Dùng hai phép kiểm dự kiến và một kịch bản đã có để tiết kiệm thời gian, giữ cửa thoát nếu toàn vòng vượt ước lượng. Một ca đã biết chỉ chứng minh đường tích hợp. Kết luận về tỷ lệ báo động giả, độ nhạy và độ đúng vùng còn cần W7 hoặc bằng chứng đánh giá đã khai riêng.

### R5. Q5 gộp quyết định demo với chọn môi trường thực nghiệm W7 — CHẶN

- **Ở đâu:** SPEC C5, Q5, bước 8–9 và tiêu chí xong 3. “Hệ” ở đây là cấu hình FlashTicket và các thành phần ghim dùng để đo.
- **Sai gì:** Q5 đề xuất W7 khi mở lại dùng ngay bản mới và khai lại phần ghim. Trong cùng hàng, căn cứ chỉ là kiểm tín hiệu, nền ngắn và phát lại dữ liệu cũ. C5 đã cảnh báo đúng rằng kết quả cũ không so trực tiếp với bản mới. Điều còn thiếu là điều kiện để Minh chọn bản W7 sau khi biết hệ quả lên ngưỡng, fixture và đầu vào đánh giá.
- **Bằng chứng:** `results/T-074/w7-spec-nhap-2.md` mục Câu hỏi và R3 phân biệt RQ3a/RQ5/D14, ngưỡng W4, source và điều kiện ghim riêng. `docs/STATE.md` ghi E6 dừng, W7 hoãn. Trên exp-app, đọc bằng `ssh.sh app` thấy Payment dùng image `arm64-t067-36a3725d`, Keycloak dùng image ghim riêng `arm64-776d9c9e` và Collector ở image lab hiện hành. `git diff 36a3725 ae5a870 -- deploy/app` cho thấy 7 file Spring chỉ Payment đổi, nhưng toàn bộ diff với bản cũ còn có thay đổi code và Keycloak. `test-environment/scripts/build.sh` dựng 7 Spring service, vì vậy pin của demo phải ghi cả phần runtime giữ từ môi trường cũ. WHY-08 giải thích dùng chung lõi. Lõi trùng byte trên cùng dữ liệu cũ không đo ổn định của detector hoặc tín hiệu đưa vào lõi ở bản mới.
- **Bước và quyết định chịu ảnh hưởng:** chặn vế đổi đối tượng W7 của Q5. Không chặn duyệt chuẩn bị bản demo khi đủ điều kiện R3. Có thể lên bản demo mới và chọn cùng runtime cho W7 sau đó, hoặc giữ bộ cũ làm W7 khi ưu tiên kế thừa ngưỡng/nền và thiết kế đã khai. Hai hướng khác nhau về diễn giải và chi phí chuyển. Hướng H1 + H4 trong LOG mới xác nhận việc dựng exp-app vì demo.
- **Đề xuất sửa:** tách Q5 thành duyệt thời điểm dựng demo và để lựa chọn pin W7 khi Minh mở lại W6/W7. Tôi đề xuất dựng demo, ghi commit, digest, Compose hiệu lực, phần Keycloak/collector/hạ tầng giữ lại và đích hoàn tác. Khi chọn W7, đối chiếu cái nào trong fixture, ngưỡng, luật, collector và nguồn đầu dò còn tương đương. Dùng lại bằng chứng Q4/replay đúng mục đích, chỉ đề xuất phần dev cần thêm cho khác biệt đã xác định. Giữ nguyên E2/E4, Q4 và kết quả T-069/T-073 theo pin gốc. Nếu muốn chuyển W7, cần cập nhật và duyệt đúng hồ sơ W6/W7 trước khi khóa, kèm thay đổi vân tay đầu vào và hệ quả đo. Chưa định lượng chi phí phần dev mới vì chưa chọn pin và chưa biết cấu hình hiệu lực của bản merge.

### R6. Mô tả mở rộng bỏ sót bản sao nội dung exception — KHÔNG CHẶN

- **Ở đâu:** SPEC C2, Q2–Q4, §Mở rộng sang máy 84 và tiêu chí xong 5.
- **Sai gì:** Bản 4 đã thừa nhận bộ lọc tên query chỉ là lớp đầu. Bảng mở rộng chỉ nêu bỏ `exception.message` ở phần xử lý event exception. Dữ liệu lưu cho thấy `exception.stacktrace` cũng có thể chứa cùng thông điệp. B16 §6 yêu cầu whitelist trước khi ghi/xuất. Cần nói rõ phạm vi giữa Java agent và Collector trong cụm, cả nơi ghi và gửi đi.
- **Bằng chứng:** Đọc dòng JSON trong `results/T-076/kiem-cuc-bo/agent/loc-nguon-1/traces.jsonl`, đi qua các span event tên `exception` và đếm không in giá trị: 82 event có stacktrace, 12 có message khác rỗng, cả 12 chứa chính message đó trong stacktrace. Cùng cách đếm danh sách `exemplars` không rỗng trong `metrics.jsonl` cho 29 ở `mac-dinh` và 0 ở `loc-nguon-1`. Mẫu có nội dung giả. `c1da15f:observability/collector/agent-docker-host.yaml` xóa `url.query` và cắt query ở `url.full`/`http.url`/`http.target`. Cấu hình đó chưa phải bằng chứng đã lọc stacktrace. Snapshot Booking cục bộ 381,3 → 499 MiB trong hai `tom-tat.tsv` chỉ cho biết chênh dưới cấu hình và tải đã thử. K3s đối với Payment/Event, đường CD cho image dựng sẵn, phân luồng Tempo và Grafana đều chưa có bằng chứng của lần bật.
- **Bước và quyết định chịu ảnh hưởng:** không chặn việc đặt endpoint ứng viên khi có điều kiện khóa R1. Chưa đủ để cam kết cấu hình hiện tại đáp ứng B16 khi bật hoặc việc mở rộng chắc chắn chỉ cần thay số RAM/IP. Thiếu bằng chứng payload và công suất thật sẽ chặn quyết định bật 84 ở gói sau.
- **Đề xuất sửa:** trong C2 và file mở rộng, ghi danh sách chặn và tắt exemplar là hai lớp giảm dữ liệu. Ghi kiểm whitelist ở phía nguồn của tuyến định bật, gồm span event và bản ghi/export đầu tiên. Nếu Minh chấp nhận Collector trong cùng cụm làm biên lọc trước khi ghi/xuất ra ngoài, cần nói rõ phần raw mà receiver có thể nhận, phương án kiểm soát tuyến nội bộ và cách ngăn raw đi vào file/kho. Loại hoặc lọc cả stacktrace theo bằng chứng. Nếu B16 vẫn được hiểu là ngay trước khi rời tiến trình Java, cần hạn chế instrumentation hoặc giải pháp lọc ở Java trước khi bật. Ưu tiên giữ tắt và dùng bộ kiểm sentinel giả hiện có ở gói sau. Đường Collector/CD mới, phân luồng Prometheus/capture, các truy vấn Tempo và datasource Grafana vẫn là phụ thuộc mở của đúng gói đó. Không dùng số +118 MiB làm dự báo cho mọi service.

### R7. Chốt cấu hình dựng và phương án quay lui trong bước 8 — KHÔNG CHẶN

- **Ở đâu:** SPEC C3, bước 4, 8–9, gói kết quả cục bộ và bảng file đã duyệt.
- **Sai gì:** Một số chỉ dẫn của bản 3 còn rơi vào đường dựng bản 4. Cần giữ vết thay đổi trước khi áp scope mới. Đồng thời “chặn build” của C3 cần ghi chính xác nó chặn pha nào.
- **Bằng chứng:** `git diff 36a3725 ae5a870 -- deploy/app/payment-service.yml` cho thấy bản mới bỏ service ngrok. File phủ lab `test-environment/overrides/payment-service.yml` vẫn khai `ngrok: profiles: [disabled]` và `hieu_luc.py` vẫn đòi `--ngrok-env`. Phép `docker compose … config` chỉ dùng YAML giả qua stdin với CLI 2.38.2 cho thấy mặc định bỏ service đó, bật profile `disabled` báo thiếu image/build. Không có bằng chứng Compose mặc định đã hỏng. `build.sh` mode `verify` hoặc `all` có `set -e` và chạy `verify -P rca-test`. Mode `build` dùng `package -DskipTests`. `verify/tien-do.tsv` và `verify/log/booking-service-rca-test-verify.log` ghi Booking profile thoát 1, 453 test, 67 error. `RcaFaultsWebConfigTests` tạo class với bean giả bằng tay nên chưa đủ bảo đảm interceptor được nối thật khi khởi tạo ứng dụng. Bảng file phần K8s còn ghi CA và header theo bản 3, trong khi bước 3 bản 4 sẽ bỏ hai thứ đó. Tại exp-app, đường Compose Payment đang dùng là `/opt/flashticket/compose/payment-service.yml`. `deploy.sh` có mode hoàn tác theo bộ file Compose và tag cũ, không hoàn tác dữ liệu nghiệp vụ phát sinh từ lượt mua.
- **Bước và quyết định chịu ảnh hưởng:** sửa lối mô tả trong Q1 và chốt cách thực thi bước 8 trước khi dừng service. Ngrok là cấu hình cũ cần khai cách xử lý, chưa phải blocker khởi động đã xảy ra. Phạm vi nhận xét `C1 đã chốt` vẫn đúng cho bảng 124 file gốc; deltas mới cần ghi thêm để lượt review PR biết điều gì đã được duyệt.
- **Đề xuất sửa:** giữ Q1 để vượt qua verify profile, sửa hẹp trong src/rca-test. Dùng verify đủ profile và phép kiểm thật mà bước 4 dự kiến để thấy hook vẫn hoạt động khi có bean, jar production vắng lớp thử. Kịch bản `PAUSE-PAYMENT` dùng Docker, nên có thể chạy dù hook Booking hỏng. Chốt mode build, đọc kết quả verify, và dùng bước 8 kiểm hai bộ Compose hiệu lực, tag còn tồn tại, khác biệt nơi đặt ngrok/mock VNPay, dự toán và các bước hoàn tác service. Đối chiếu ngày còn bán của fixture với lịch demo, vì T-070 §12 ghi có hạn bán. Đối chiếu schema/realm/fixture thực dùng và ghi rõ việc triển khai đổi dữ liệu hay chỉ đổi image. LOG T-067 từng ghi áp migration tại chỗ và chuẩn bị hoàn tác dữ liệu. Nếu bản mới cần thay schema hoặc snapshot dữ liệu, trình riêng quyền và thời gian. Lượt k6 mua vé cũng ghi đơn vào DB thử, nên ghi rõ hoàn tác image có giới hạn nào. Lưu diff bản 4 bổ sung cho bảng file cũ, giữ số và bằng chứng bản 3. Dùng lượt 4 hiện có với Collector HTTP đúng tên, bỏ bootstrap TLS/token cứng của `chay-agent.sh` bản 3 trong lượt mới theo quyền được duyệt. Nếu cần đổi file lab, ghim commit mới và xét lại bước nào phụ thuộc. Mốc gián đoạn trong T-070 chỉ là mốc cơ sở. LOG T-067 còn có lượt build ARM cũ để tham chiếu. Dùng lại hồ sơ đó và đo phần thay đổi trong lượt build dự kiến, rồi cập nhật dự toán gián đoạn bước 8. Nếu một lượt có thể vượt một giờ, trình chi phí và cách giữ phần đã xong theo AGENTS §3.21.

## Đối chiếu các lượt trước

| Điểm | Kết luận sau kiểm độc lập |
|---|---|
| REVIEW R1 | **Đúng.** Adapter ở bản chụp cộng theo `service_name` và đường capture gateway dùng chung. Bản 3 có thiết kế tách. Bản 4 giữ nguồn exp cho demo vì chưa gửi từ 84. Gói bật sau vẫn cần tách metric/capture tại đầu vào. |
| REVIEW R2 | **Đúng.** CD lọc khóa theo file mẫu và bỏ Discovery. Bản 3 xử lý đường cho bảy workload và ghi phạm vi Discovery. Bản 4 chuyển token tới Collector, vấn đề token trong từng pod lùi. Kiểm lại chính tuyến Secret còn lại mới thấy cửa bật sớm ở R1 lượt này. |
| REVIEW R3 | **Đúng.** So `gateway.yaml` với pipeline exp-app xác nhận thiếu processor tại gateway mặc định. Giữ OTLP log tắt loại được phần log trên 84 trong hướng này. Dữ liệu raw cho thấy vẫn cần kiểm whitelist và stacktrace khi chuyển sang bật trace, xem R6. |
| REVIEW R4 | **Đúng.** Bản 3 thêm tiêu chí phía client, ngưỡng và đích hoàn tác theo hai giai đoạn. Bản 4 chưa có lần bật thật, nhưng giới hạn kiểm ảnh hưởng của lần đổi image và đích về A vẫn còn giá trị. R2 lượt này đối chiếu đường `previous` ở HEAD. |
| REVIEW R5 | **Đúng, đã sửa trong code.** `b16-services.txt` và workflow tại `ae5a870` giới hạn B16 đúng bảy tên, Assistant có verify riêng. Đếm mã thoát cục bộ 8 verify thường và 7 B16 đều 0. CI GitHub còn cần kết quả ở bước 5. |
| REVIEW R6 | **Đúng, đã sửa phần CD.** Workflow giữ amd64/arm64 và truyền `SERVICE_VERSION`, build lab ARM truyền commit riêng. Keycloak đang chạy bản ghim riêng qua phép đọc exp-app. Vì vậy phạm vi B là 7 image Spring mới và phần phụ thuộc giữ riêng. |
| REVIEW R7 | **Đúng.** Q4 dùng lab `85ace52`, lab hiện hành là `c1da15f`. RCA AGENTS §12 có ngoại lệ đúng nhánh, có căn cứ trong bản 3 Q5 và LOG, vẫn yêu cầu Minh duyệt push. Bản 4 đổi pha, dòng STATE hiện còn trỏ IP trước bước 6 và người giữ Secret trước bước 9 như bản cũ. Cần sửa riêng khi Minh duyệt cập nhật. |
| REVIEW-2 N1 | **Đúng.** `deploy-k8s-service.sh` ghi đè một `previous` sau deploy/restart thành công. Bản 3 xử lý theo một service; bản 4 không làm lần restart bật. Cần giữ điều kiện rollback cho chuyển đổi agent tắt và ghi lại giới hạn khi mở rộng. |
| REVIEW-2 N2 | **Đúng.** `tests/signals/check_purchase_journey.py` tìm theo service/span/dấu tài nguyên, giới hạn kết quả, thiếu selector môi trường ở revision hiện tại. Đếm 200 trace Q4 của người làm chỉ là mẫu cũ. Bản 4 bỏ nguồn 84, nên chưa có xung đột hai nguồn trong lần demo. Cần đưa điều kiện lọc theo nguồn vào gói dùng Tempo chung sau này. |
| REVIEW-2 N3 | **Đúng, đã kiểm thêm với dữ liệu giả.** Kết quả raw phân biệt bộ lọc ở Java với bộ lọc sau khi nhận. Bản 4 hoãn bật đúng với phạm vi dữ liệu hiện còn. R6 giới hạn chữ “chỉ thêm” khi chuẩn bị pha sau, không đặt quy trình triển khai mới cho pha này. |
| REVIEW-2 N4 | **Đúng.** Theo Compose và provisioning tại `c1da15f`, thêm dashboard/Prometheus chưa tự xác nhận Grafana đang truy nguồn mới. Đầu ra Grafana cho production đã chuyển sang gói sau. Dashboard online exp-app cần được nối lại theo R3. |

## Tuân thủ quy trình

- Vai trò khớp SPEC và STATE. LOG ghi Minh duyệt bản 3, duyệt bảng file, rồi duyệt hai thay đổi về `HOST_ID` và tạo CA/chứng chỉ. Bản 4 ghi đúng trạng thái đề xuất sau quyết định viết theo H1 + H4. Không thấy bằng chứng đã triển khai theo bản 4. Dòng STATE còn sót hai chỗ trỏ bước bản 3 nêu trên. `KE-HOACH-DON.md` §12 cũng còn mô tả bật 84 theo task này. Đề nghị trình đồng bộ sau khi SPEC và quyết định nguồn được duyệt.
- Bản 4 có lý do sơ bộ cho Collector trong cụm, bỏ CA/token tại pod và dùng một PR. WHY-08/09/89 giải thích lõi dùng chung và các tín hiệu phải giữ, WHY-105–111 giải thích detector/cửa sổ/độ phủ hiện tại. Chưa thấy mục WHY cho cách chọn đích chuyển tiếp, điều kiện chọn pin W7 hay ngưỡng 10% bản 4. Các mục còn là đề xuất. Sau khi Minh quyết, trình ghi DECISIONS/WHY với phương án khác, điều kiện thất bại và bằng chứng theo Luật 0, trước khi dùng làm kết luận. Không lấy các số đã thấy để biến ngưỡng Q7 thành phép so đã được kiểm độc lập.
- Cơ chế RCA hiện hành giữ mốc từ webhook `startsAt`. Bộ điều phối sinh cửa sổ, stage ghép trace/log dạng đã chuẩn hóa với metric Prometheus, lõi ghim tạo bằng chứng bất thường và hạng V082, G1 đưa kết quả ra dashboard. `deployment.environment` và `service.version` định tuyến/định phiên bản, không phải nhãn lỗi. `PAUSE-PAYMENT` thuộc trình điều phối kịch bản, không mở thêm dữ liệu hay nhãn vào stage/lõi. T-076 không thay đường xếp hạng, đầu vào nhãn hoặc đối chứng quan hệ. Chưa có lượt trên bản 4 để xác nhận pipeline runtime có đúng độ phủ sau khi đổi bản.
- Bằng chứng ghim Q4 không bị dùng làm nghiệm thu cho revision mới. Giữ nguyên manifest Q4 và kết quả gốc. Kiểm read-only `git diff --check f178870 ae5a870` sạch. Chưa thấy SPEC bản 4 yêu cầu sửa lõi hoặc file chấm lịch sử. Phản biện không ghi LOG/STATE.

## Điều đã kiểm và thấy đúng

- `git rev-parse` xác nhận ba ref cục bộ và HEAD worktree đã nêu. `Get-Content` đếm 124 dòng danh sách file, 13 dòng xung đột. Bảng đã duyệt chia 93 giữ, 17 sửa, 14 bỏ. Thử `gh pr view`, `gh api` và `git ls-remote` đều gặp reset kết nối GitHub. Chưa xác nhận tình trạng từ server trong lượt này. Bước 5 phải lấy lại base/head thật và dùng lease ghim đúng đầu đã soát trước push.
- Đã đọc bản thử Booking/Assistant và thời điểm verify ở file gốc. Tách lỗi Booking profile khỏi Maven thường và GitHub CI thông thường. Các kiểm B16 và cấu hình của bản thử chưa cho phép suy tải hoặc hành vi của 84. Số máy 84 lấy từ LOG phiên 4, chưa đo lại.
- Đã xác nhận exp-app, exp-obs dùng lab `c1da15f`. Hai lớp đầu ra là kiểm cấu hình/đường tín hiệu và diễn tập toàn vòng. Assistant chỉ agent và Keycloak/hạ tầng ghim riêng không ngăn lát cắt Q4 đặt mua trong ba tín hiệu đã đo. Không dùng phạm vi ấy để nói phủ tất cả workload.
- Chọn demo RCA không cần frontend là lát cắt hợp lý của P10 nếu người xem vẫn thấy hành trình mua, cảnh báo, đồ thị con của ca và hạng. Có thể mở rộng trình bày sau theo yêu cầu của Minh. Chưa đạt tiêu chí xong bản 4 vì đang soát kế hoạch và chưa có đầu ra bản này.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. Đã soát SPEC bản 4 và đối chiếu các phản hồi R1–R7, N1–N4 trên nguồn gốc và code.
2. Đầu ra duy nhất là `tasks/T-076-pr17-otel-may-84/REVIEW-3.md`.
3. Đã kiểm 12/12 hash Q4, mốc hash SPEC bản 3, diff, nhật ký Maven, JSONL, Compose với YAML giả và hai máy được phép bằng lệnh đọc. Không vào máy 84, không mở dữ liệu khóa, không chạy lượt tải hay tiêm lỗi, không commit.
4. **Đề nghị tiếp tục lượt đáp trước khi duyệt SPEC.** Q1 sửa hẹp và H1/H4 có căn cứ. Chốt cách bảo đảm tắt và xử lý regression sau rollout ở Phần A. Khoanh quyền thực thi và điều kiện đạt demo ở Phần B. Để pin W7 chờ W6/W7 mở lại và tách mốc demo. Việc chứng minh B16 khi mở xuất 84 còn phụ thuộc biên lọc Minh chấp nhận, kiểm raw, năng lực triển khai CD và tài nguyên dưới tải. Chưa có phản hồi của người làm về các điểm lượt này. Đề xuất và mặt trái cho từng quyết định ở R1–R7.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/SPEC.md (bản 4, đề xuất).
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P9/P10, tích hợp ngoài G0–G4, không có khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,SPEC.ban-3.md,LOG.md}, results/T-076/bang-file-pr17.md, results/T-076/kiem-cuc-bo/README.md, results/T-070/don/{KE-HOACH-DON.md,q4/README.md}, DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/{REVIEW.md,REVIEW-2.md,REVIEW-3.md}, gồm bảng đáp của hai lượt đầu.
- Code và kết quả liên quan: D:/Project/flash-ticket-platform (ref cục bộ f178870, PR #17 bb84d64, nhánh ghim 36a3725d), D:/Project/ft-pr17-dung-lai (ae5a870), D:/Project/flashticket-rca-lab (c1da15f), results/T-076/kiem-cuc-bo/, results/T-070/don/q4/SHA256SUMS, hồ sơ T-072/T-073/T-074.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi riêng cho lượt đáp. Nếu Minh cấp quyền, ghi đúng phần được Minh nêu.

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

Người làm chỉ điền bảng trong quyền đã được duyệt. Giữ nguyên nhận xét và prompt. Để trống cột Minh quyết.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN | `deployment.yaml:59–63` @nhánh: `envFrom` ConfigMap rồi Secret, Secret thắng; CD đưa vào Secret khóa có tên trong file mẫu (`deploy-k8s-service.sh:198–221`); giá trị hiện có của `ENV_<SVC>` không đọc được, và README cũ của PR từng hướng dẫn đặt `OTEL_AGENT_ENABLED=true`. Bản 5 (Minh duyệt viết 27/11) chọn khác đề xuất giữ công tắc trong Secret: **tắt cứng** `OTEL_AGENT_ENABLED: "false"` ở `env:` của 7 `deployment.yaml` (`env` thắng `envFrom`), file mẫu Secret không đổi so với main; bật sau này là sửa nhỏ trong cùng PR thêm Collector. Kiểm: render manifest (bước 4), log pod không có dòng khởi động agent (bước 7). Thứ tự `env` > `envFrom` là quy tắc K8s, không mô phỏng trên laptop. | |
| R2 | Đúng; CHẶN | Không service nào có starter OpenTelemetry/Micrometer tracing (`grep pom.xml`), nên `OTEL_*` chỉ agent đọc; `SPRING_AUTOCONFIGURE_EXCLUDE` thì Spring đọc. Bản 5: bỏ biến này khỏi Phần A (thêm ở giai đoạn sau); C4 có nền đo ≤ 30 phút trước merge, so theo service (trung bình mỗi bản, báo riêng khi số bản đổi), kiểm chức năng GET công khai (Q8), digest trước merge, `rollback` tới lần triển khai kế tiếp rồi revert bằng PR, người bấm Minh, tiêu chí dừng. Kết luận giới hạn ở rollout và tài nguyên quan sát được. | |
| R3 | Đúng; CHẶN | T-070 chưa có `REVIEW-5.md`. Bản 5: phạm vi ghi thêm máy tải (lượt k6), obs (bộ nhận T-073, bộ điều phối, contact point, nguồn dashboard, hoàn tác theo `trien-khai-e5.md` §5), exp-app (cấu hình hiệu lực vào thư mục mới, dấu vết tiêm, đổi ngày bán nếu Q9); bước 10 chỉ bắt đầu khi REVIEW-5 xong và Minh kết luận về tuyến chuỗi tải/RCA trực tuyến; `hieu_luc.py` không còn gọi là chỉ đọc. | |
| R4 | Đúng; CHẶN | `q4/README.md` mục 1–2: luật mất mẫu và 4 luật p95 cháy khi khởi động lại. Bản 5 C6: nền tới khi mọi luật bình thường và đủ mẫu, cảnh báo của sự cố có `startsAt` sau lúc tiêm, mã ca đi đủ webhook → G1 → dashboard trong N = 25 phút từ t̂ (`results/T-073/khai-truoc-e5.json`), trang ca có đồ thị con và danh sách hạng của chính ca đó, cảnh báo lớp quan sát ghi riêng, sổ tiêm đọc sau lượt; một ca chỉ chứng minh đường tích hợp; phương án phát lại offline dự phòng. | |
| R5 | Đúng; CHẶN | Bản 5: Q5 chỉ còn dựng bản demo sau bước 7; ghi bản ghim demo đủ (commit, digest, Compose hiệu lực, Keycloak `776d9c9e`, Collector lab, đích hoàn tác); chọn bản W7 để khi mở lại W6/W7; kết quả cũ giữ theo pin gốc. | |
| R6 | Đúng; KHÔNG CHẶN | Bản 5 mục Mở rộng: lọc `exception.message` và lọc/bỏ `exception.stacktrace`; hai lớp hiện có ghi là giảm dữ liệu; điều kiện OPEN gồm kiểm payload thô ở nguồn và bản ghi đầu tiên ra ngoài, câu hỏi Collector trong cụm có là biên lọc B16 §6 không, số RAM thật theo service, phí AWS. | |
| R7 | Đúng; KHÔNG CHẶN | Bản 5 bước 8 kiểm: ngrok trong file phủ lab, cấu hình hiệu lực vào thư mục mới, tag cũ, mock VNPay, schema/realm/fixture, ngày bán (hết 02/12/2026 22:16Z, Q9), mode `build.sh`, dự toán từ lượt T-067, hoàn tác và giới hạn (không hoàn tác đơn trong DB thử); C3 ghi đúng lỗi chặn `build.sh verify|all`; bảng file thêm mục "Chênh bản 5"; lượt kiểm cục bộ mới bỏ TLS/token. | |
