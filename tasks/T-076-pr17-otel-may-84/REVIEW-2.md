# Phản biện T-076 — lượt 2

- **Người phản biện:** Codex. **Ngày:** 26/11/2026. **Người làm:** Claude.
- **Công đoạn:** kiểm lại phản hồi và SPEC bản 2, P9/P10 ngoài G0–G4. Minh cho ghi đúng bản `REVIEW-2.md`. SPEC vẫn chờ Minh duyệt.
- **Đã đọc:** AGENTS của RCA và lab, STATE, hai bản SPEC, LOG, REVIEW và bảng phản hồi. Đối chiếu DT18, hướng dẫn của cô, MRP P9/P10, WHY-08/09/89, quyết định triển khai 16–19/11, LESSONS và T-070 §12. Mã nguồn ở FlashTicket `f178870`, PR `bb84d64`, lab `c1da15f` và RCA `25550d2a5`. Bằng chứng Q4 thuộc lab `85ace52`.
- **Tự soát độc lập:** kiểm SPEC bản 2 và đường CD, Collector, kho, bộ kiểm tín hiệu trước khi đọc bảng đáp của Claude. Repo RCA ở `672391b9b`. Bản 1 lưu đúng SHA-256 của bản đã phản biện. Bản 2 kiểm trong lượt này có SHA-256 `7da4b872fb9d59540b2a9c575f2b7355d66a9c45bd7dd38a0f00c15f42f690d9`.

## Kết luận chung

Bản 2 đã sửa hướng tách đầu vào RCA, chọn phạm vi log, đường Secret, CI B16 và kiến trúc build. **Đề nghị tiếp tục phản biện trước khi duyệt triển khai.** Còn bốn điểm có hệ quả cụ thể ở bước bật/hoàn tác, quy nguồn trace, lọc trước khi xuất và nghiệm thu Grafana. Vẫn giữ đúng một PR và thao tác máy 84 qua CD. Task thực hiện một phần P9a và chuẩn bị tích hợp cho P10. DT18-NV2/NV3 và hướng dẫn của cô còn cần bằng chứng từ thực nghiệm và demo đồ thị, phát hiện, xếp hạng. Bản 2 đã nêu đúng giới hạn cho máy 84.

## Các điểm

### N1. Restart ghi đè đích rollback trước merge — CHẶN

- **Ở đâu:** SPEC bước 8–9, C5, Q7/Q9 và mô tả hoàn tác trong PR.
- **Sai gì:** Xác nhận digest trước merge đủ cho lần rollback ngay sau merge. Sau một `restart` thành công, digest đó không còn là đích mà action hiện tại chấp nhận. Ngoài ra, bước 9 cho phép nhóm `k8s`, trong khi nhóm này lớn hơn tập bảy workload cấu hình agent.
- **Bằng chứng:** Tại `f178870`, `.github/workflows/_deploy-service.yml:192–205` lấy image hiện chạy cho `recreate`. `deploy/scripts/deploy-k8s-service.sh:170–190,261–271` tạo revision mới cho recreate, ghi `previous` bằng `current` cũ khi thành công, và rollback chỉ chấp nhận image của revision trong `previous`. Phản ví dụ từ code: A là image trước merge, B là image mới. Sau merge, `previous=A`. Sau bật và restart thành công, `current=B+bật`, `previous=B+tắt`. Gọi rollback digest A sẽ bị từ chối với `ROLLBACK_CONFIG_NOT_FOUND`. Lỗi rollout ngay trong lần bật vẫn có thể được CD tự phục hồi về B+tắt. Mặt khác, rollback áp lại cả snapshot Secret (`apply_revision`, dòng 46–50). Sau một lần restart để tắt, `previous` có thể là B+bật kèm header. `.github/scripts/plan-deploy.sh:19–28` chọn mọi mục K8s. Registry tại cùng commit có 10/10 mục là K8s, gồm Discovery, Keycloak và frontend.
- **Bước và quyết định chịu ảnh hưởng:** mâu thuẫn thiết kế, chặn duyệt workflow bật/hoàn tác như đang viết. Không có bằng chứng đã phát một CD như vậy. Mốc cần bảo vệ là lúc chuyển từ B+tắt sang B+bật.
- **Đề xuất sửa:** giữ hai pha hiện có, nhưng chốt theo từng service và bỏ lựa chọn nhóm `k8s`. Trong cửa sổ agent tắt, dùng kiểm nền đã có để quyết có giữ image B hay quay về A khi CD vẫn cho phép. Khi đã bật, hoàn tác agent về B+tắt bằng cập nhật đủ Secret và restart. Nếu dùng snapshot, kiểm nó thực sự ở trạng thái tắt và đồng bộ lại Secret GitHub trước lần restart tiếp. Nếu Minh cần quay về A cả sau khi đã bật, người vận hành phải chỉ ra tuyến CD được phép và còn khả dụng cho A trước bước 9. Nếu chưa có, ghi rõ giới hạn và để Minh quyết chấp nhận hoặc giữ agent tắt. Chọn cách này giữ CD hiện hữu. Thêm cơ chế lưu/chọn revision xa hơn chỉ đáng xét nếu Minh yêu cầu năng lực đó.

### N2. Tempo chung vẫn có thể làm bộ kiểm tín hiệu exp-app nhận nhầm trace — CHẶN

- **Ở đâu:** SPEC C4, bước 7, bước 10 và tiêu chí 3.
- **Sai gì:** Tách Prometheus và file capture giải quyết đường vào hai stage RCA. C4 nói về dashboard nhưng bỏ sót một đường đọc Tempo dùng để nghiệm thu exp-app. Bước 10 còn gọi đích danh phép kiểm Q4 theo đường đó.
- **Bằng chứng:** Lab `c1da15f:tests/signals/check_purchase_journey.py:41–54,105–123,179–183` gọi Tempo `/api/search` rồi đọc từng trace. Truy vấn mẫu nhận span theo tên service/kind/route hoặc DB/queue, có giới hạn kết quả và thiếu selector môi trường. Nếu 84 sinh trace cho cùng tên service, mẫu 84 có thể thỏa điều kiện hoặc chiếm chỗ của mẫu exp. Phần kiểm theo đúng ID đơn vẫn chặt hơn, nhưng các mục kiểm độ phủ độc lập có thể cho kết luận nhầm. Q4 đã dùng chính chương trình này. Diff `85ace52..c1da15f` của bộ kiểm và gateway rỗng. Ngược lại, panel bản đồ hệ thống cũ dùng `serviceMap` nối datasource Prometheus thực nghiệm, và hai stage RCA hiện không đọc Tempo. Các đường đó chưa cho thấy bị trộn bởi thiết kế mới.
- **Bước và quyết định chịu ảnh hưởng:** chặn tuyên bố tách hoàn toàn các phép kiểm thực nghiệm dùng chung Tempo, và chặn dùng Q4 cũ không lọc để nghiệm thu pha 4. Việc tách đường dữ liệu RCA chính đã được xử lý ở mức thiết kế. Quy nguồn trace trên Tempo còn OPEN đến lúc có mẫu 84 và exp trong cùng cửa sổ.
- **Đề xuất sửa:** giữ Tempo chung cho lần đầu nếu muốn ít thay đổi. Gắn và kiểm nhãn nguồn ở hai receiver. Ràng buộc `exp` ở truy vấn Tempo dùng làm bằng chứng thực nghiệm, gồm bộ kiểm Q4 nếu dùng lại, và `production` ở truy vấn dashboard chạy thật. Nếu chưa sửa quyền/phạm vi cho bộ kiểm, hoãn phần nghiệm thu đó và giới hạn câu về cách ly ở Prometheus, capture, stage và luật. Khi duyệt phép trộn ở bước 7, dùng dấu tổng hợp có đối chứng dương từ đúng Prometheus chạy thật, vì chuỗi đã aggregate trong `prometheus.json` có thể mất nhãn môi trường. Hai stage đọc Prometheus thật từ tuyến thực nghiệm, dùng `RCA_M1_ROOT` thử riêng và mã mờ mới. `stage_b.py --prom-tu-file` chỉ phù hợp hồi quy ca cũ. Tách thêm Tempo tránh phụ thuộc vào selector và chia tải kho tốt hơn, nhưng tăng tài nguyên và cấu hình. Chưa cần làm nếu các truy vấn còn dùng đã được khoanh đúng và theo dõi tải kho chung.

### N3. Phép kiểm hiện chỉ chứng minh lọc sau khi payload rời máy 84 — CHẶN

- **Ở đâu:** SPEC C3/C3b, bước 4, 6 và 9, tiêu chí 2, Q4.
- **Sai gì:** Bản 2 đặt lớp lọc ở `collector-production` trên obs rồi kiểm bản ghi đã qua lọc. Kết quả đó không phân xử được agent đã loại trường cấm trước lúc xuất hay payload thô vượt Internet rồi mới bị loại.
- **Bằng chứng:** B16 §6 trong `bb84d64:docs/architecture/B16-observability-baseline.md` yêu cầu whitelist trước khi ghi/xuất, với Collector là lớp dự phòng. Trên exp-app, `agent-docker-host.yaml:161–182,225–234` chạy processor xóa query trước exporter đi máy khác. Thiết kế mới có TLS và bỏ log 84. Hai lựa chọn đó giảm rủi ro đường truyền và log, còn trace có thuộc tính URL và cấu hình thu header/parameter riêng. Ví dụ agent để một query nhạy cảm trong `url.full`, Collector xóa sau khi nhận, sentinel trong kho vẫn vắng. Tài liệu instrumentation chính thức cũng cho thấy sanitization/capture phụ thuộc loại thuộc tính và cấu hình. Chưa có bằng chứng rò rỉ, hay payload raw của 84 đã được kiểm. [URL semantic conventions](https://opentelemetry.io/docs/specs/semconv/url/) · [HTTP instrumentation configuration](https://opentelemetry.io/docs/zero-code/java/agent/instrumentation/http/)
- **Bước và quyết định chịu ảnh hưởng:** chặn bật xuất trace thật ở bước 9 và chữ “dữ liệu gửi đi sạch”. Kiểm TLS, token và bản ghi trong Tempo giữ giá trị cho phần chúng đo.
- **Đề xuất sửa:** giữ Q1(c). Ngay trong smoke test Java agent ở bước 4, chọn cấu hình phía nguồn cho các trường bị cấm theo B16, dùng HTTP/DB mẫu có dữ liệu giả và kiểm payload OTLP **trước** processor Collector, đồng thời yêu cầu còn span/metric hữu ích. Bước 6 giữ phép kiểm sau lọc. Ưu tiên cấu hình agent có sẵn nếu kết quả chứng minh đạt. Nếu agent chưa lọc được các trường bị cấm trên đường định bật, hạn chế instrumentation đó hoặc giữ xuất trace tắt đến khi Minh duyệt tuyến lọc phía nguồn. Thêm Collector tại cluster chỉ là phương án sau khi cấu hình agent không đáp ứng. Chi phí kiểm đầu tiên nằm trong smoke test đã có.

### N4. Chưa có bước nạp datasource mới vào Grafana đang chạy — CHẶN

- **Ở đâu:** SPEC Đầu ra, quyền obs, bước 6–7 và tiêu chí xong.
- **Sai gì:** SPEC hứa hiện trace/metric chạy thật trên Grafana và không dừng thành phần cũ. Phần thao tác chỉ bật hai container mới, còn tiêu chí chỉ kiểm kho nhận. Dashboard mới hiện trong danh sách vẫn có thể không truy vấn được datasource mới.
- **Bằng chứng:** Lab `c1da15f:observability/compose.yaml` mount riêng các thư mục provisioning và dashboard vào Grafana. `provisioning/dashboards/providers.yaml` cho file provider quét định kỳ, còn việc nạp datasource qua provisioning có đường reload riêng. Datasource Tempo `tempo` hiện nối `serviceMap.datasourceUid: prometheus` của thực nghiệm. Nếu dùng nguyên liên kết này trong dashboard chạy thật, map vẫn đọc metric thực nghiệm. Lệnh chỉ đọc `docker ps` trên obs xác nhận Grafana hiện đang chạy. Thêm service Compose hoặc file YAML không tự là chứng cứ Grafana đã nạp và panel đọc đúng UID. [Grafana Admin API, reload provisioning](https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/api-legacy/admin/) · [Provision Tempo data source](https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/provision/)
- **Bước và quyết định chịu ảnh hưởng:** chặn nghiệm thu đầu ra Grafana theo mục tiêu. Việc hai kho nhận dữ liệu có thể kiểm riêng ngay cả khi datasource chưa nạp.
- **Đề xuất sửa:** ghi bước người vận hành được Minh duyệt reload riêng datasource provisioning với quyền hiện có, rồi mở dashboard và thấy metric 84 cùng trace đã lọc nguồn. Nếu dùng service map, chỉ tới Prometheus chạy thật, hoặc bỏ panel đó khỏi lát cắt đầu khi chưa cần. Giữ UID/datasource/luật cũ. Nếu không có quyền reload, Minh chọn một cửa sổ restart Grafana có ảnh hưởng cảnh báo, hoặc dời phần dashboard và ghi tiêu chí chưa đạt. Ưu tiên reload riêng vì không cần dừng Grafana hay dựng bản thứ hai. Không cần sửa rule cho việc thêm datasource.

## Đối chiếu các lượt trước

| Điểm cũ | Kết luận về phản hồi và bản sửa |
|---|---|
| R1 | **Đúng, đã sửa thiết kế cho đường RCA chính.** Stage đọc file capture/Prometheus cũ. Receiver mới không dẫn vào các nguồn đó. Cần giữ đối chứng dương/âm và phần quy nguồn Tempo ở N2. |
| R2 | **Đúng, đường thực thi đề xuất có căn cứ.** CD lọc theo mẫu và `# Optional`, pod có môi trường từ Secret. Đưa CA qua ConfigMap tránh thêm loại manifest ngoài danh sách CD. Giữ Discovery tắt có ghi thiếu phủ. Header, CA/SAN và egress thật còn OPEN. Bước 4 phân xử được cấu hình exporter với dữ liệu giả, còn bước 6 và CD được phép mới kiểm tuyến mạng. Thiếu bản đầy đủ `ENV_<SVC>` thì giữ agent tắt. |
| R3 | **Đúng một phần về mức khép finding.** Giữ log 84 tắt và bổ sung lọc ở obs xử lý phần Loki và bản ghi sau nhận. Việc kiểm payload trước khi gửi còn thiếu, xem N3. |
| R4 | **Đúng một phần về mức khép finding.** Q7 đã đưa p95, lỗi và trạng thái pod vào tiêu chí. Merge agent tắt tạo nền thích hợp để so tác động của việc bật agent trên cùng image B. Phương án hoàn tác còn N1. Ghi tuổi mẫu exp và counter từ chối/lỗi theo cửa sổ so có lưu lượng, thay vì đòi giá trị tuổi mẫu “không đổi” theo từng lần lấy mẫu hoặc dùng tổng tích lũy. Với 10% sampling, khi một service ít lưu lượng, thiếu trace có thể do chưa được lấy mẫu hoặc exporter chưa chạy. Dùng metric/telemetry nhận theo service và một hành trình biết có chạm service trong giờ theo dõi, ghi thiếu phủ nếu vẫn chưa phân biệt. Kiểm GET ngắn chỉ cho kết luận dưới tải/luồng đã đo. |
| R5 | **Đúng, đã sửa ở SPEC.** Danh sách cụ thể tách Assistant chỉ có agent khỏi bảy service có file mẫu, thiếu mẫu đúng phạm vi vẫn lỗi. CI GitHub thật còn ở bước 4. Giữ được vai trò của kiểm B16 trong cả workflow CI và workflow build CD dùng lại. |
| R6 | **Đúng, đã sửa ở SPEC.** Main giữ hai platform, hunk truyền revision được giữ theo C1 và có kiểm `service.version`. Keycloak native tracing là phụ thuộc của pha 4 và được đưa vào bảng C1. |
| R7 | **Đúng về pin lab, mốc obs và thứ tự Q5.** Còn lệch nhỏ trong quyền ghi Secret. Mục Phạm vi ghi trỏ bước 8, thao tác thực ở bước 9. Sửa tham chiếu trước khi ban quyền từng bước. Không dùng lại khuyến nghị mở gateway chung trong T-070 §12 làm lệnh triển khai. Dẫn về C4 T-076 đã được duyệt khi có quyền cập nhật hồ sơ. |

## Tuân thủ quy trình

LOG phiên 2 ghi Minh duyệt **viết** bản 2 và điền bảng đáp. SPEC/STATE vẫn ghi chờ duyệt triển khai. Hash `SPEC.ban-1.md` khớp bản soát trước. So với diff đã kiểm cuối lượt 1, phần phản biện và prompt cũ của `REVIEW.md` nguyên vẹn, thay đổi ở bảng đáp. LOG có khai người làm đã thấy tóm tắt trước khi tự soát nên lượt đáp đó không được tính là tự soát độc lập. Lượt này đối chiếu lại bằng mã nguồn. Chưa thấy đầu ra thực thi T-076. Các lựa chọn về phân luồng, lọc xuất, lấy mẫu và ngưỡng vẫn là đề xuất. Sau khi Minh quyết, ghi vào DECISIONS/WHY trong phạm vi được duyệt trước khi viện làm căn cứ kết quả. Label nhập tuyến là thông tin môi trường, không là nhãn lỗi hay mốc tiêm. Lõi và method lock không cần đổi cho đề xuất này.

## Điều đã kiểm và thấy đúng

- `Get-FileHash -Algorithm SHA256` khớp manifest cho hai file tín hiệu T-067, hai file Q4 (README và JSON) và bảng `T-070/kiem-ke/m1-ban-chup.tsv`. Đây là bằng chứng của exp-app tại cửa sổ đã ghi, dùng để xác định tuyến và phép kiểm đang có.
- Kiểm obs chỉ đọc qua wrapper cho HEAD `c1da15f`, `free -m` báo `available=10249 MiB`, `df -h /srv/flashticket-rca` báo dùng 45%. Đây là ảnh chụp lúc kiểm, không thay số cũ và không suy ra sức chứa dưới tải 84. Không đọc env hay bí mật.
- Mô hình merge agent tắt rồi bật bằng CD giúp tách tác động đổi image khỏi tác động bật agent nếu ghi đúng nền và giới hạn hoàn tác. Việc ghi rõ thiếu log/Discovery phù hợp phạm vi đề xuất, không làm thành kết luận đã phủ đủ B16 trên 84.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. Kiểm độc lập hai bản SPEC, đối chiếu R1–R7 và truy đường thực thi của các sửa đổi.
2. Chỉ thêm `tasks/T-076-pr17-otel-may-84/REVIEW-2.md`.
3. Đã kiểm diff, mã nguồn theo revision, hash năm file theo manifest và tình trạng obs bằng lệnh chỉ đọc. Không vào 84, không chạy thực nghiệm, không mở dữ liệu khóa, không commit.
4. **Đề nghị tiếp tục lượt đáp, chưa duyệt bước bật agent.** Chọn cách giữ một PR, restart từng service và phân biệt mốc hoàn tác A/B. Ưu tiên Tempo chung có lọc đúng truy vấn, kiểm phía nguồn ngay trong smoke test, và reload riêng datasource Grafana. Q1(c), Q2(a), dual-arch của main và tách Prometheus đã có lý do. Q7/Q8 chờ Minh chọn và khai phạm vi đo. Q9/IP cần người vận hành xác nhận trước phần phụ thuộc. Giữ Q6 duyệt riêng. Bằng chứng còn thiếu và tác động cụ thể nêu trong N1–N4. Chưa có phản hồi của người làm về các điểm mới.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/SPEC.md (bản 2 đề xuất).
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P9, P10, việc tích hợp ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude là người làm, Codex là người phản biện.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,SPEC.ban-1.md,LOG.md}, results/T-070/don/KE-HOACH-DON.md §12, DT18, hướng dẫn của cô và MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md và bảng phản hồi cuối file, sau đó tasks/T-076-pr17-otel-may-84/REVIEW-2.md.
- Code và kết quả liên quan: D:/Project/flash-ticket-platform (f178870, bb84d64, 36a3725), D:/Project/flashticket-rca-lab (c1da15f), repo RCA (25550d2a5:src/m1/adapter_flashticket.py), results/T-070/don/q4/SHA256SUMS. Các nguồn này dùng ở chế độ chỉ đọc.
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
| N1 | Đúng; CHẶN | `f178870:deploy/scripts/deploy-k8s-service.sh:170–175,261–271`: chỉ một `previous`, ghi lại sau mỗi `deploy`/`restart` thành công; `rollback` đòi digest đúng image của `previous`. `plan-deploy.sh:19–28`: nhóm `k8s` = 10 service. Bản 3 (Minh duyệt viết 26/11): bật/tắt từng service; quyết giữ B hay `rollback` về A trong pha agent tắt (bước 8); sau khi bật chỉ tắt bằng bỏ khóa + `restart`, không dùng `rollback`; `ENV_<SVC>` đầy đủ trước mỗi `restart`; giới hạn không về A sau khi bật thành Q10 để Minh chấp nhận hoặc đòi đường CD khác. | |
| N2 | Đúng; CHẶN | Lab `c1da15f:tests/signals/check_purchase_journey.py:41–54`: TraceQL không lọc môi trường. Kiểm Tempo (SSH, chỉ đọc) cửa sổ Q4: `booking-service` 200/200 trace có `deployment.environment="exp"`, 0 trace khác (giới hạn 200). Bản 3: giữ Tempo chung; bộ kiểm tín hiệu lọc `exp` (thêm vào phạm vi ghi lab); dashboard chạy thật lọc `production`; bước 7 thêm đối chứng dương ở `prometheus-production`/Tempo, hai stage chạy truy vấn Prometheus thật (`RCA_M1_ROOT` thử, mã mờ mới), bộ kiểm tín hiệu trên cửa sổ trộn. | |
| N3 | Đúng; CHẶN | B16 §6 yêu cầu lọc trước khi xuất; bản 2 chỉ kiểm sau Collector obs. Bản 3: bước 4 kiểm payload thô của agent trước mọi processor (collector cục bộ không processor), sentinel ở query URL/header/body/tham số DB, chọn cấu hình agent; không đạt thì tắt instrumentation hoặc giữ agent tắt; Collector obs là dự phòng; tiêu chí 2 đổi theo. Cấu hình agent cụ thể **chưa kiểm**. | |
| N4 | Đúng; CHẶN | Lab `compose.yaml:77–78` mount provisioning; `datasources.yaml:30–31` `serviceMap` → `prometheus`. Bản 3: C7 — datasource `prometheus-production`, `tempo-production` (`serviceMap` → `prometheus-production`), reload bằng `POST /api/admin/provisioning/datasources/reload`, kiểm danh sách/health, dashboard cũ không đổi; reload lỗi → Minh chọn restart Grafana hoặc dời. | |
