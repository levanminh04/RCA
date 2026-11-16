# Kế hoạch giai đoạn 2: dữ liệu FlashTicket đủ và giàu, rồi ổn định phương pháp

- **Trạng thái:** Minh duyệt ghi file (chat 11/11/2026: "Duyệt, ghi file"). Duyệt kế hoạch không cấp quyền sửa repo FlashTicket, chạy lượt dài hay mở dữ liệu khóa; mỗi việc đó vẫn cần duyệt riêng.
- **Bổ sung 11/11/2026:** Minh duyệt ghi (chat 11/11: "duyệt ghi theo đề xuất, G2 giao diện đổi thành minh làm, tôi muons là theo phương án A trước, B thử sau nếu A không ổn"): nhánh G sản phẩm demo (§7), định nghĩa danh mục lỗi sớm (chặng 1c), quy tắc log mới (§4e), trạng thái §4a, sửa câu về cổng Keycloak (chặng 2, §5).
- **Người soạn:** Claude, 11/11/2026.
- **Đọc cùng:** `PLAN-TRIEN-KHAI.md` (kế hoạch gốc, §6.2 cho B4–B8), `TECHSTACK-NGHIEN-CUU.md`, `results/T-058/so-khac-phuc.md` (sổ khắc phục), `results/T-058/may-chu-va-truy-cap.md` (máy và cách vào).

## 0. Vì sao có kế hoạch này

Lượt đêm 10–11/11 (T-058) cho thấy hệ thống chạy được trên hai máy Oracle ARM và M1 chạy được trên dữ liệu FlashTicket, nhưng dữ liệu chưa đủ và M1 chưa dùng hết dữ liệu:

- Trace thiếu span Redis (đã sửa tạm), thiếu vhost (đã sửa tạm) và tên queue của RabbitMQ (chưa sửa).
- Log nghèo: payment, ticket, user hầu như không ghi log trong request; định dạng log mỗi service một kiểu; log hạ tầng chưa thu.
- M1 bỏ thuộc tính span (DB, cache, broker không thành nút), chỉ nhận 7 kênh metric, và loại thành phần gốc khi nó "chết im".
- Giới hạn bộ nhớ của nhóm không đủ khi gắn agent.

Chi tiết từng điểm ở `results/T-058/so-khac-phuc.md` (KP-01 đến KP-14), `kiem-span-redis.md`, `kiem-rabbitmq-va-log.md`.

## 1. Nguyên tắc

1. Không vội. Mỗi chặng có điều kiện vào, điều kiện ra và cách kiểm.
2. Dữ liệu đủ trước, phương pháp sau: thiếu dữ liệu thì phương pháp nào cũng không bù được.
3. Hai máy hiện tại (`exp-app`, `exp-obs`) là môi trường thử nghiệm; thư mục và tên tạm thời được chấp nhận tới chặng 5.
4. Mọi lỗi, chỗ thiếu và cách sửa ghi vào sổ khắc phục; điểm nào thành bài học chung thì đề xuất đưa vào `docs/LESSONS.md`.
5. Phần định nghĩa thí nghiệm (kịch bản tải, mức tải, danh mục lỗi) làm chuẩn ngay từ đầu, vì đổi giữa chừng thì kết quả các đợt không so được với nhau.

## 2. Hai mức phát hiện (nhắc lại MRP §2.3, M-38)

| Mức | Câu hỏi | Ai làm | Hiện trạng 11/11 |
|---|---|---|---|
| Hệ thống | Có sự cố hay không, lúc nào | Luật cảnh báo Grafana | Chưa dựng (0 luật) |
| Thành phần | Thành phần nào bất thường tự sinh, thành phần nào kế thừa | M1, có dùng đồ thị | Có trong M1; đã đánh giá trên dữ liệu công khai ở P7(a), G4 đã duyệt |

Nhánh "đồ thị tham gia quyết định báo động" vẫn hoãn (M-20). Không mở task riêng trên dữ liệu công khai lúc này; nếu cô yêu cầu thì mở sau chặng 3, dùng luật Grafana làm đối chứng.

## 3. Các chặng

| Chặng | Ngày (dự kiến) | Việc | Xong khi | Ai làm |
|---|---|---|---|---|
| **0. Khép phần khả thi T-058** | 11–12/11 | Minh chỉ định người phản biện T-058; quyết commit (đề xuất: gói dữ liệu thô 126 MB để ngoài git, giữ mã băm); quyết máy AWS cũ (dùng làm máy tải hoặc Stop) | T-058 đóng phần khả thi, có phản biện | Minh, Claude |
| **1a. Đủ dữ liệu, phía cấu hình** | 12–19/11 | Thu log hạ tầng (PostgreSQL, MongoDB, Redis, RabbitMQ) qua Collector tại chỗ; thêm `hostId`; viết **bộ kiểm chất lượng dữ liệu tự động** chấm R-01–R-10 (`results/T-040/yeu-cau-quan-sat-p9.md`) sau mỗi thay đổi | Bộ kiểm chạy được, báo đúng các chỗ thiếu đã biết | Claude (không sửa code FlashTicket) |
| **1b. Đủ dữ liệu, phía code** | 12–19/11, song song 1a | Nhóm hệ thống làm các mục ở §4; merge xong thì dựng lại `exp-app` từ image đa kiến trúc do CD build | Bộ kiểm báo đủ span HTTP, DB, Redis, RabbitMQ (có tên queue); log nối span ở mọi service; không OOM | Nhóm hệ thống (Minh làm hoặc giao) |
| **1c. Định nghĩa danh mục lỗi** | 12–15/11, song song 1a | Từ 11 kịch bản ở `docs/KE-HOACH-GIAI-DOAN-TOI.md` D.9, chốt bảng vị trí × họ lỗi. Mỗi ô ghi: cách tiêm; phần code hoặc cấu hình phải có (cờ lỗi, chuỗi kết nối qua Toxiproxy, mock VNPay); dấu hiệu mong đợi trên metric, log, trace; ô thuộc đợt phát triển hay đánh giá (phụ thuộc điểm M7). Chỉ định nghĩa, chưa chạy. Làm sớm vì bảng này quyết định nhóm phải viết code gì (việc 2i) | Minh duyệt bảng; nhóm biết phải làm gì cho việc 2i | Claude soạn, Minh duyệt |
| **2. Máy tải chuẩn** | 13–19/11, song song chặng 1 | Máy AWS `3.24.8.49`: ghim phiên bản k6, đồng bộ giờ; kịch bản và mức tải lưu trong repo RCA; Security List và `iptables` của `exp-app` chỉ mở cổng gateway 8081 và Keycloak 8080 cho `3.24.8.49/32`. Kịch bản tải bắt buộc có đăng nhập và đặt vé; mở cổng chưa đủ để đăng nhập, xem §5 | Một kịch bản cố định chạy lặp 2 lần cho lưu lượng giống nhau (đếm ở gateway) | Claude |
| **3. Danh mục lỗi và phát hiện (T-059)** | 18–26/11 | Dựng bộ tiêm theo danh mục đã định nghĩa ở chặng 1c; Toxiproxy, Pumba, cờ lỗi; sổ tiêm lỗi (PLAN §5); nguồn quan sát độc lập cho "service chết im" (KP-10); luật cảnh báo Grafana, ngưỡng chọn trên dữ liệu bình thường; chạy nền qua đêm | Mỗi họ lỗi chạy được và có mốc trong sổ; luật Grafana không báo động giả trên đêm nền | Claude, nhóm (cờ lỗi) |
| **4. Đợt phát triển M1** | 25/11–4/12 | Chạy M1 và baseline trên dữ liệu phát triển. Thử cho M1 dùng thông tin giàu hơn: DB, cache, broker thành nút từ thuộc tính span; thêm kênh JVM, pool kết nối, queue. Mỗi thay đổi là một thành phần có đối chứng bỏ nó; tiêu chí chọn khai trước | Chọn xong phiên bản M1 cho FlashTicket theo tiêu chí khai trước | Claude, phản biện |
| **5. Khóa và chuẩn hóa** | khoảng 4/12 | Đặt lại thư mục và tên trên máy và trong repo cho khoa học, dễ đọc; khóa bản FlashTicket, bản M1, kịch bản tải bằng commit và mã băm; dựng lại từ máy trống bằng script để chứng minh tái lập | Dựng lại từ máy trống chạy đúng như bản khóa | Claude |
| **6. Đánh giá, demo, viết** | 5–30/12 | Như `PLAN-TRIEN-KHAI.md` §6.2 (B6–B8) | Hồ sơ G6 duyệt; quyển nộp 30/12 | Claude, Minh |

Phụ thuộc: chặng 1b quyết định thời điểm xong chặng 1; chặng 1c không phụ thuộc 1a, 1b; chặng 2 không phụ thuộc chặng 1; chặng 3 cần chặng 1 và 2; chặng 4 cần chặng 3; chặng 5 cần chặng 4. Nhánh G (§7) chạy song song với các chặng.

## 4. Việc gửi nhóm hệ thống

**a) CD chạy được trên ARM.** Trong `.github/workflows/_deploy-service.yml`: thêm bước `docker/setup-qemu-action` trước buildx; đổi `platforms: linux/amd64` thành `linux/amd64,linux/arm64`; giữ `provenance: false`. Image nền Temurin 21 (digest đang ghim) và Keycloak 26.8.0 đã có bản `arm64` (đã kiểm qua registry). Bước `kc.sh build` của Keycloak chạy qua giả lập sẽ chậm hơn (chưa đo). Frontend gắn cứng URL theo môi trường; muốn dùng ở môi trường khác thì build theo môi trường hoặc chuyển sang cấu hình lúc chạy.
**Trạng thái 11/11:** nhóm đang làm, chưa xong (Minh, chat 11/11). Trong lúc chờ, `exp-app` tiếp tục chạy image ARM tự build từ đúng commit của máy 84 (KP-01).

**b) Bộ nhớ khi có agent.** booking-service bị OOM ở 512 MiB; payment 95%, discovery 90% giới hạn. Nâng `mem_limit` khi bật agent; lưu ý `MaxRAMPercentage=50` làm heap tăng theo giới hạn.

**c) Biến env.** `SPRING_AUTOCONFIGURE_EXCLUDE=org.springframework.boot.data.redis.autoconfigure.observation.LettuceObservationAutoConfiguration` cho booking-service, api-gateway (có span Redis). `OTEL_INSTRUMENTATION_RABBITMQ_EXPERIMENTAL_SPAN_ATTRIBUTES=true` cho event, booking, payment, ticket (có vhost). Đưa jar agent vào image và bật bằng env (TECHSTACK §4.1).

**d) Khởi tạo PostgreSQL.** Thêm quyền thực thi cho `deploy/postgres/00-business-databases.sh`; bổ sung hai file SQL reader mà compose đang trỏ tới nhưng không có trong repo.

**e) Log, thống nhất ngay từ đầu.** B16 §4 đã có chuẩn log v1. Hiện mỗi service làm một kiểu (booking dùng trường mặc định `level`, `logger_name`; event dùng bộ tùy biến riêng; ticket, payment, user dùng danh sách trường của B16). Bốn quy tắc chung:
1. Một khối cấu hình log giống hệt nhau cho mọi service: cùng danh sách trường, cùng tên trường (`severity`, `timestamp`, `stackTrace`); tốt nhất đặt trong một file dùng chung.
2. **Gateway** ghi một dòng cho mọi request (hiện chỉ ghi khi 4xx, 5xx; KP-15). **Service nghiệp vụ** ghi một dòng ở mỗi điểm quyết định nghiệp vụ (B16 §5), mỗi message xử lý xong và mỗi lỗi. Không bắt service nghiệp vụ ghi thêm một dòng cho mọi request thành công, vì span của request đã có thời gian và mã trạng thái; log cần mang thứ span không có: `reasonCode`, `stateBefore`, `stateAfter`, `outcome`. Quy tắc này thay quy tắc cũ "mỗi request ở mọi service một dòng" (11/11), vì quy tắc cũ nặng và trùng với span. Tình trạng từng service: `VIEC-CHO-QUYET-VA-LAM.md` §3.
3. Hạn chế log framework: `com.flashticket` mức INFO; `org.springframework`, `org.hibernate`, `com.netflix`, `io.lettuce`, `org.apache` mức WARN.
4. Một phép kiểm tự động trong CI: chạy service, bắt vài dòng log, so với một JSON Schema viết từ B16 §4.

Thêm: Keycloak bật log JSON (chưa kiểm tên tùy chọn của bản 26.8.0); thêm `hostId` (B16 bắt buộc khi chạy thật).

**f) Tên queue trong span.** Gắn thuộc tính tên queue trong listener, hoặc thêm cầu nối Micrometer Tracing để observation của Spring AMQP sinh span có thông tin listener.

## 5. Máy tải (chặng 2): các điểm đã cân nhắc

- 200 ms giữa Sydney và Singapore không vào dữ liệu RCA: span bắt đầu khi gateway trong mạng Oracle nhận request. Số đo phía k6 có 200 ms nền, phải trừ nếu dùng làm nhãn "mức ảnh hưởng". Độ dao động đo được: p95 221 ms so với tối thiểu 200 ms (120 lần kết nối).
- Lưu lượng ra khỏi AWS (ước lượng, chưa đo): khoảng 270 MB mỗi giờ ở 50 request/giây, khoảng 16 GB cho 60 giờ chiến dịch, dưới 100 GB miễn phí mỗi tháng. Phản hồi vào AWS miễn phí; Oracle miễn phí 10 TB chiều ra mỗi tháng.
- Chuẩn ngay phần định nghĩa thí nghiệm (kịch bản, lịch đến cố định, phiên bản k6, định dạng kết quả); phần dựng máy giữ đơn giản.
- **Đăng nhập trong kịch bản tải** (đã kiểm realm và cấu hình; cách làm chưa kiểm):
  - Realm `flash-ticket` của nhóm: token sống 300 giây; phiên đăng nhập hết khi rỗi 30 phút, tối đa 10 giờ; có refresh token. Một chu kỳ sự cố dài khoảng 30 phút, lượt nền chạy qua đêm (`PLAN-TRIEN-KHAI.md` §6.2, §7), nên kịch bản phải làm mới token; lượt dài hơn 10 giờ phải đăng nhập lại. Không làm mới thì từ phút thứ 5 mọi request bị 401, tạo một "sự cố" giả trong dữ liệu.
  - Client `frontend` chỉ cho luồng trình duyệt (PKCE), không cho gửi thẳng mật khẩu; `KC_HOSTNAME` ghim `10.0.0.158`, nên trang đăng nhập chuyển hướng về địa chỉ nội bộ. Lượt đêm đã lấy token theo luồng PKCE bằng `results/T-058/dem-2026-11-10/auth.py`, chạy trên `exp-app`.
  - Hướng làm (chưa kiểm): k6 đăng nhập trước cho một nhóm người mua ở pha khởi động, làm mới token định kỳ, giữ một ít lượt đăng nhập trong lúc chạy để Keycloak cũng có tải. Realm hiện chỉ có 1 tài khoản người mua; số tài khoản cần tạo chọn ở chặng 2.

## 6. Điểm chờ Minh quyết

1. Người phản biện T-058.
2. Commit kết quả lượt đêm, có đưa gói thô 126 MB vào git không.
3. Máy AWS `3.24.8.49`: dùng làm máy tải (chặng 2) hay Stop.
4. Gửi danh sách §4 cho nhóm hệ thống; ai làm từng mục.
5. Đưa các mục tổng quát của sổ khắc phục vào `docs/LESSONS.md`.
6. Các điểm M1–M9 ở `VIEC-CHO-QUYET-VA-LAM.md` §1. M6 (nơi đặt giao diện) đã quyết 11/11, xem §7.

## 7. Nhánh G: sản phẩm demo

**Vì sao thêm.** Các chặng 0–5 chỉ lo dữ liệu và M1. Các nguồn còn đòi phần sản phẩm:

| Nguồn | Yêu cầu |
|---|---|
| DT18 | Sản phẩm cuối có giao diện minh họa kết quả phân tích |
| MRP P10, Q-28 | Demo: báo sự cố → đồ thị con bất thường → danh sách nguyên nhân → LLM giải thích; phần phát hiện được demo ngang phần RCA |
| `docs/KE-HOACH-GIAI-DOAN-TOI.md` D.1 tầng 1 | Chuỗi thu thập → cảnh báo → chẩn đoán → giao diện chạy trên FlashTicket |
| Bước 5 của cô, P8 | LLM diễn giải nguyên nhân; P8 hoãn từ 09/11 |

**Quyết định của Minh (chat 11/11):** G2 do Minh làm. Làm phương án A trước: Grafana, panel Node graph đọc kết quả RCA. Phương án B (trang riêng của RCA) chỉ thử nếu A không ổn. Thế nào là "A không ổn": Minh quyết khi xem bản A đầu tiên. Đề xuất để Minh xét: một màn hình không hiện được cùng lúc đồ thị tô màu, bảng xếp hạng và liên kết sang bằng chứng (trace, log, metric).

| Bước | Việc | Ai | Khi | Cần có trước |
|---|---|---|---|---|
| G1 | Định dạng kết quả RCA bản 0: một JSON gồm sự cố, nút và cạnh, vai trò từng nút (nghi là nguồn, bị kéo theo, bình thường, thiếu dữ liệu), xếp hạng, vùng nghi ngờ, bằng chứng, liên kết sang trace, log, metric. Trường của nút và cạnh theo đúng trường panel Node graph cần (`docs/DE-XUAT-HUONG-GRAFANA-RCA.md` §7.2, tài liệu tham khảo theo Q-188). Kèm dữ liệu mẫu từ 2 ca của lượt đêm (`method-output-1.json` có vai trò của 17 thực thể và các cạnh) | Claude | 12–14/11 | Không |
| G2 | Giao diện theo phương án A: dashboard Grafana gồm danh sách sự cố → Node graph tô màu → bảng xếp hạng và bằng chứng → ô giải thích (để trống tới G4). Bố cục tham khảo `DE-XUAT-HUONG-GRAFANA-RCA.md` §7.6. Cách cấp dữ liệu cho panel chọn ở G1: plugin Infinity đọc JSON (chưa cài trên `exp-obs`, kiểm 11/11; cài là thay đổi trên máy, cần Minh duyệt) hoặc nguồn PostgreSQL có sẵn trong Grafana | Minh | Từ 14/11 | G1 |
| G3 | Dịch vụ RCA trực tuyến: nhận cảnh báo Grafana → gom thành sự cố → chạy M1 → ghi kết quả theo định dạng G1 → cấp cho giao diện | Claude | Cùng chặng 3 | G1; luật cảnh báo của chặng 3 |
| G4 | LLM giải thích dựa trên gói bằng chứng (P8) | Claude | Sau chặng 4, theo điểm M8 | M8 |
| G5 | Kịch bản demo có script, chế độ phát lại offline, video, diễn tập | Claude, Minh | Chặng 6 | G2, G3 |

Cả hai phương án dùng chung định dạng G1, nên chuyển sang B không mất việc đã làm ở G1, G3.

## 8. Cập nhật 17/11/2026: kế hoạch bản 3 (nhánh demo trước, nhánh đánh giá sau)

- **Trạng thái:** Minh duyệt ghi (chat 17/11/2026: "duyệt theo đề xuất , ghi kế hoạch"; DECISIONS mục "Hoãn D16; chế độ (b) trên FlashTicket; nén T-032; kế hoạch bản 3"). Bản này qua hai lượt Codex phản biện và hai bản đáp của Claude trong chat. Duyệt kế hoạch không thay duyệt SPEC từng gói, lượt chạy dài, sửa repo nhóm hay mở dữ liệu khóa.
- **Thay cho** các ngày của §3 chặng 3–6 và §7 G3–G5. Phần §0–§7 giữ làm lịch sử.

### 8.1 Đã chốt

| Việc | Chốt | Nguồn |
|---|---|---|
| Nền tảng | Oracle cho exp-app, exp-obs; máy tải ở AWS | DECISIONS 16/11 |
| Repo vận hành | `flashticket-rca-lab`; phiên bản là commit; dữ liệu ngoài git | DECISIONS 16/11 |
| Triển khai | Docker Compose trước; bản K8s sau demo, ghi là giới hạn của quyển | DECISIONS 16/11 |
| D16 | Hoãn; không chặn khóa bản và chế độ (b) trên FlashTicket; kết quả (b) ghi giới hạn | DECISIONS 17/11 |
| Bản FlashTicket thử nghiệm | `main` của nhóm + commit quan sát của PR #17, tự build, `OTEL_AGENT_ENABLED=true`; ghim một bản dùng xuyên W3–W7 | DECISIONS 17/11 |
| M7 | Giữ chia theo ô (vị trí × họ lỗi); ngoại lệ phải trình riêng | DECISIONS 11/11 (T-059) |

### 8.2 Nhánh demo (ưu tiên)

| Gói | Việc | Xong khi |
|---|---|---|
| W0 | Nén T-032 tại chỗ; ghi kế hoạch này; viết `docs/READING-GUIDE.md` | — |
| W1 | Repo lab chạy được: chép đủ phụ thuộc runner (stage/run M1, safe-export, inj3, venv dựng lại); script đọc `inventory/`; code và cấu hình ở git, JSON và chỉ mục ca ở `/srv/rca-lab` (chuyển trên máy). Dựng lại exp-obs, máy tải từ repo, dùng lại volume cũ. Kiểm từ đầu tới cuối: tải → xuất gói → RCA → mở được ca phát lại; xong mới trình danh sách xóa. Đầu ra trên máy chỉ kéo khi cần giữ và chưa có bản tương đương hoặc không dựng lại được. Trước khi trình danh sách xóa, đối chiếu từng đầu vào lịch sử (gói bổ sung, gói R9, bản chụp mã) với bản trên laptop: có bản tương đương, chứng minh dựng lại được, hoặc kéo về (gói đầu vào M1 đã kéo 17/11, `D:/RCA-archive/exp-obs/m1ft-inputs`). Thời hạn giữ Tempo: đo tốc độ tăng rồi chọn | Luồng chạy trọn từ repo lab |
| W2 | Dựng bản thử nghiệm ghim (8.1): ghim revision `main` khi soạn SPEC (17/11 là `640dbaf`; danh sách xung đột kiểm lại trên đúng revision đó); gỡ xung đột trên nhánh riêng; build image arm64 và biến thể `-P rca-test` cho Booking, Event; file phủ lên `deploy/app/*.yml`; kiểm arm64 từng digest; chuỗi commit → digest → container. Nghiệm thu bằng danh sách tín hiệu bắt buộc theo luồng mua vé: span HTTP, DB, Redis, producer và consumer RabbitMQ có tên queue; log nối span bằng khóa `(traceId, spanId)` với độ phủ tối thiểu khai trước. Bộ kiểm R cũ (`results/T-062/kiem-du-lieu/kiem-r.py`) chỉ dùng chẩn đoán (R-03 không đòi Redis; R-04, R-06 có thể đạt khi thiếu) | Mua vé chạy trọn; đủ tín hiệu bắt buộc; không OOM sau 1 giờ tải |
| W3 | Phụ thuộc: cách tính "lần dò mới nhất" (WHY-99) đã tích hợp vào bộ xuất chung, dùng cùng ngữ nghĩa ở phía cũ và phía mới. V082 không hồi quy trên bản mới: khai trước cặp ca cũ–mới (ô, digest, tải, can thiệp, đầu dò, cửa sổ) và tiêu chí theo ô (hạng nút gốc, lỗi chạy, kết luận ca khỏe); chỉ kết luận cho ô ghép được; dùng lại đầu ra cũ khớp điều kiện | Bảng so theo ô; V082 tụt thì dừng, trình Minh |
| W4 | Luật cảnh báo Grafana bằng file (`provisioning/alerting/`): lỗi, p95 theo route ở gateway; liveness theo "lần dò mới nhất". Ngưỡng chọn trên đêm nền 1, đo báo động giả trên đêm nền 2. Khai trước quy tắc gom cảnh báo | Báo động giả dưới ngưỡng khai trước; webhook chạy |
| W5 | Dịch vụ RCA trực tuyến chế độ (b): bộ xuất chung tích hợp cách tính "lần dò mới nhất" (WHY-99) cho ca và cửa sổ bất kỳ; hợp đồng G1 bản 0.3 mang nguồn t̂; bộ điều phối ghi t̂, phép kiểm `t` lõi nhận = t̂; không sửa lõi M1 đã ghim; không đọc sổ tiêm; mốc theo D3, giữ riêng giờ nhận webhook; đo thời gian trên dev rồi mới khai N phút; kiểm dashboard hiện hành, lưu trữ và phát lại khi đổi nguồn JSON. Nghiệm thu theo D3: lưu riêng bản ghi cảnh báo và giờ nhận; xuất dữ liệu theo t̂ đủ cửa sổ tới t̂+300 (gói cũ quanh mốc tiêm không dùng được); kiểm dữ liệu thực sự vào lõi (cửa sổ, tín hiệu), không chỉ `t = t̂`; ghi riêng thiếu dữ liệu phủ, lỗi xử lý, ca bỏ sót. Nếu demo dùng stage đọc file ghi vòng của Collector, ghi giới hạn cửa sổ; đọc qua API Tempo/Loki/Prometheus (P9b) để OPEN | Tiêm một lỗi, Grafana tự hiện kết quả trong N phút đã khai |
| W8 | LLM tối thiểu: giải thích dẫn bằng chứng, gợi ý bước xử lý, được trả lời "không đủ bằng chứng". Mức đánh giá do Minh chọn | Chạy được trong demo |
| W9a | Kịch bản demo, video, phát lại offline, diễn tập 2 lần | Diễn tập không lỗi |

### 8.3 Nhánh đánh giá (lịch chờ dự toán)

- **W6 — khóa bản và thiết kế đánh giá.** Khóa digest FlashTicket, commit repo lab, sha256 bản M1, kịch bản và mức tải. D14 bắt buộc: P7 khóa chạy thẳng, V082 đầy đủ, V082 che từng nhóm thông tin kể cả phần dẫn xuất; cả hai chế độ. Ma trận ô chạy được trên bản mới. Dự toán giờ máy và quy tắc gói hợp lệ. R-07: mặc định chấm theo sự cố tiêm đã xác nhận trong cửa sổ khai trước và gọi là "độ trễ theo mốc tiêm"; chỉ khi Minh chọn kết luận theo thời điểm bắt đầu tác động mới thêm đầu dò dòng thời gian (chi phí tính trong W6). Baseline: SimpleRCA (M4, quy ước T-017), BARO RobustScorer là ứng viên; khóa danh sách và nhánh dự phòng của từng phép che trước khi thu; ở chế độ (b) BARO dùng cùng t̂. Runner cho W7: chụp và kiểm đầu vào từng ca lúc thu, đóng gói đầu vào không phụ thuộc đầu ra M1 (bỏ điều kiện `summary.json` của `safe-export.py`), chạy batch RCA và baseline sau khi cả đợt đã đóng; tuyến trực tuyến W5 tách riêng. Ghi WHY trước khi thu.
- **Độ đo theo đầu ra:**

| Đầu ra | Độ đo |
|---|---|
| Phát hiện | Precision, Recall, F1 theo cửa sổ; quy tắc ghép sự cố với cảnh báo, gộp báo trùng; ca bỏ sót; báo động giả mỗi giờ khỏe; độ trễ theo mốc đã chọn |
| Xếp hạng | MRR, NDCG@5, Hit@k, AC@k theo B1.9 (T-043 SPEC) và quy tắc nhãn T-059; khóa riêng ba bảng: điểm theo nhãn thật, điểm theo tập nút chấp nhận, bảng định vị cạnh (có hướng, có loại; `UNSUPPORTED` cho V082); giữ ca không có cảnh báo trong mẫu số của chế độ (b), báo thêm điểm trên nhóm có cảnh báo |
| Vùng ảnh hưởng | Precision, Recall, F1 khi có nhãn độc lập cùng cấp (đường đo mức endpoint của T-059); chưa đối chiếu được thì báo đồ thị con nghi ngờ, độ đúng OPEN |

- **W7 — đợt đánh giá.** Chỉ chốt lịch khi có dự toán và phương án lỗi ở 10%, 50%, 99% (luật 21). Thu trước, chạy RCA và baseline sau trên gói đã đóng; chấm sau khi đã băm đầu ra.
- **W9b — hồ sơ G6** (phản biện chéo bắt buộc) và quyển. Chương P1–P7 viết ngay, song song.

### 8.4 Thứ tự, song song, khi trễ

- W0 và W1 làm trước; chuẩn bị W2 song song W1. Trên exp-app, lượt kiểm đầu–cuối của W1 và lần dựng lại container của W2 ở hai khung giờ riêng. W3 sau W2 và sau khi tích hợp cách tính R9 vào bộ xuất chung. W4 sau W2; đêm nền W4 tách khỏi ca tiêm W3. W5 viết song song W4 trên dữ liệu đã có. W6 thiết kế song song W4–W5. Quyển viết song song từ 18/11.
- Sửa S1–S7 sau ba lượt Codex rà bản 3: Minh duyệt 17/11 ("Duyệt cả hai").
- Ngày cụ thể chờ ngày demo và bảo vệ (Minh chưa cho). Chưa có căn cứ đặt lịch W7.
- Khi trễ, cắt theo thứ tự: LLM về mức chỉ demo → số baseline → số lần lặp. Không cắt W3, D14.

### 8.5 Còn mở

- D16 (hoãn); R-07 cho độ trễ phát hiện; NV1 (đánh giá hiệu năng hệ thống) chưa có người phụ trách; ngày demo và bảo vệ; mức đánh giá LLM; K8s là giới hạn của quyển.
