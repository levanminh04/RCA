# Phản biện T-076 — SPEC bản 5

- **Người phản biện:** Codex. **Ngày:** 27/11/2026. **Người làm:** Claude.
- **Công đoạn và quyền ghi:** kiểm lại phản hồi và sửa, P9/P10 ngoài G0–G4. Minh cho ghi riêng `tasks/T-076-pr17-otel-may-84/REVIEW-4.md`.
- **Đã đọc:** AGENTS, STATE, SPEC bản 3–5, LOG, bảng file, kết quả kiểm cục bộ, Q4 của T-070, tài liệu triển khai và tiêu chí khóa E5 của T-073, DT18, hướng dẫn của cô, MRP P9/P10, B16, WHY/DECISIONS/LESSONS liên quan. Đọc REVIEW 1–3 và các bảng đáp sau khi đã tự soát nguồn và đường chạy.
- **Bản đã soát:** SPEC bản 5 SHA-256 `d88cfbbf14b71f19ce0eee28c1c3ebc6462b4f2022b1d8ebae8d0b3d105d475d`. Bản 4 trùng hash đã soát ở REVIEW-3. Bản 3 trùng hash ghi ở LOG. Repo RCA HEAD `672391b9b`. FlashTicket refs cục bộ `f178870` / `bb84d64` / `36a3725d`, nhánh dựng lại `ae5a870` còn là bản 3. Lab `c1da15f`.
- **Tự soát độc lập:** lần đường CD → revision → pod, rồi k6 → tín hiệu Q4 → luật → webhook → bộ gom → đầu vào V082 → G1/Grafana. Đối chiếu văn bản với code ở revision đang có, đọc trạng thái exp-app và exp-obs. Dùng hash để kiểm nguồn E5 và Q4 trước khi đối chiếu tiêu chí.

## Kết luận chung

Giữ H1 + H4. Bản 5 xử lý được nguy cơ Secret bật agent và tách quyết định W7 khỏi bản demo. Còn ba điểm chặn theo bước: xác minh đích rollback trước merge, cấp đúng phạm vi và viết đường dựng/hoàn tác cho bước 9–10, khóa tiêu chí quy ca demo cho lần tiêm. Đề nghị tiếp tục một lượt đáp. Có thể duyệt riêng phần chuẩn bị PR nếu Minh muốn làm song song, trước khi duyệt bước merge hoặc diễn tập.

Phần A triển khai lát cắt log B16 và chuẩn bị cấu hình trace/metric cho P9a. Phần B áp dụng RCA trên exp-app và trình diễn phát hiện, đồ thị con, xếp hạng cho P10 và DT18-NV2/NV3. RQ về độ nhạy, báo động giả, độ đúng vùng, đánh giá nhiều mức tải của NV1 và đường đọc API đầy đủ của P9b vẫn thuộc phần việc tương ứng. MRP P10 còn nêu giải thích bằng LLM. DECISIONS 23/11 hoãn W8. Một lượt đạt có thể dùng cho W9a trong giới hạn lát cắt này, còn số lượt diễn tập và phần trình bày cuối theo kế hoạch W9a.

## Các điểm

### R1. Digest đang chạy chưa chứng minh CD có thể quay lại revision đó — CHẶN

- **Ở đâu:** SPEC C4, Q7–Q8, bước 6–7 và phần Phạm vi ghi.
- **Sai gì:** Bước 6 ghi digest và người bấm nhưng chưa xác nhận mỗi service có snapshot tương thích của revision hiện tại để trở thành `previous`. Ghi thời điểm merge chưa ràng buộc hết khoảng từ nền đo đến lúc thực sự rollout. C4 cũng đặt ngưỡng RAM mà chỉ nói dừng khi crash/OOM hoặc kiểm GET lỗi.
- **Bằng chứng:** FlashTicket `ae5a870:deploy/scripts/deploy-k8s-service.sh:170–175` yêu cầu `previous` tồn tại và digest đúng image của snapshot đó. Dòng 261–270 cập nhật `current` và chỉ ghi `previous` nếu có revision cũ. Dòng 285–295 khai đường không có revision trước và chỉ dẫn riêng cho Assistant. `.github/workflows/_deploy-service.yml:134–136` tuần tự theo service, không giữ riêng slot A trong toàn cửa sổ quan sát. Luồng CD còn verify và publish trước deploy. Với CD thành công ngay trước hoặc sau rollout PR, digest ghi trước có thể khác snapshot sẽ dùng để quay lại. Docker image đang chạy và snapshot CD là hai nguồn bằng chứng khác nhau. LOG máy 84 phiên 4 đủ để biết các replica khác nhau và đang có rollout, chưa có chỉ mục snapshot cho từng service.
- **Bước và quyết định chịu ảnh hưởng:** chặn bước 6 nếu dùng câu “có thể quay lại bằng CD” làm căn cứ merge. Rủi ro cụ thể là pod Ready nhưng kiểm chức năng trượt khi bản cần quay lại đã không còn là `previous`, hoặc không có snapshot ban đầu. Chưa quan sát tình huống này xảy ra. Ngưỡng Q7 còn là đề xuất vận hành. Một ảnh `kubectl top` và vài GET chỉ cho mức RAM và chức năng quan sát được ở những mẫu đó.
- **Đề xuất sửa:** trước merge, Minh hoặc người vận hành xác nhận readonly `current` của CD, snapshot tương ứng và image cho mỗi service trong plan CD từ diff sắp merge. Chỉ ghi revision/digest và trạng thái, không đọc Secret. Điều phối với nhóm để giữ đích trong khoảng theo dõi. Khi cần quay lại, đối chiếu `previous` một lần nữa. Nếu không bảo toàn đích, ưu tiên dời merge. Phương án khác là Minh duyệt riêng đường phục hồi khẩn khi CD không về được, gồm ngoại lệ nếu phải revert bằng PR khác. Chốt thêm Q7 là ngưỡng phải dừng/trình hay chỉ để báo, cách xử lý thiếu mẫu và khoảng đo thực tế theo từng rollout. Q8 khai trước cùng GET và điều kiện đạt (mã trạng thái, phần hợp đồng cần đúng), giữ giới hạn không suy thành đã kiểm toàn bộ giao dịch hoặc p95 dưới tải.

### R2. Bước 9 vẫn cần ghi trên obs, và đường phục hồi bước 10 còn trỏ vào bản lab cũ — CHẶN

- **Ở đâu:** SPEC Phạm vi ghi, bước 8–10, C5/C6, tiêu chí xong 3–4.
- **Sai gì:** Bản 5 đã thêm quyền vận hành, nhưng dòng obs chỉ liệt kê thay đổi tuyến RCA trực tuyến và giới hạn tới bước 10. Bước 9 yêu cầu Q4 vốn phát tải từ obs và ghi trạng thái tại đó. Bước 10 dẫn `trien-khai-e5.md` §5 để hoàn tác, trong khi đó là runbook gắn commit và đường dẫn trước đợt dọn. Chưa có cặp thao tác áp/hoàn tác đúng trên `c1da15f`.
- **Bằng chứng:** `results/T-070/don/q4/README.md` ghi lệnh Q4 phát qua `tai_linux.py start` trên obs. Lab `c1da15f:load/controller/tai_linux.py:52–54,182–186,189–221,242–270` ghi `tai-linux-events.jsonl`, buộc làm mới token khi start, có thể khôi phục mock/tunnel, ghi hồ sơ lượt trên máy tải. Đường này có thể đi thẳng, khác đường `chuoi_tai` đang chờ REVIEW-5. `results/T-073/trien-khai-e5.md` §5 hoàn tác bằng H `1bb40ca` ở `/opt/rca-lab` và trả nguồn `t065-l11-001`. Lab hiện dùng `/opt/flashticket-rca`, `rca/online/README.md` ghi G1 ra `online-<lượt>`, còn dashboard ở commit hiện hành đọc URL `public/rca/dev`. `observability/grafana/build_dashboards.py` hỗ trợ sinh dashboard theo nguồn `online-…`. Lệnh đọc `ssh.sh obs` cho HEAD `c1da15f`, mount `/srv/flashticket-rca/rca/results` vào `/usr/share/grafana/public/rca`, chỉ thấy Grafana và bộ nhận T-072 trong nhóm được kiểm. Hai file STOP kiểm được đều vắng. T-070 chưa có REVIEW-5.
- **Bước và quyết định chịu ảnh hưởng:** chặn khởi động Q4 bước 9 nếu chưa cấp quyền ghi chính xác, và chặn bước 10 nếu chưa có điều kiện T-070 và cách nối trở lại tuyến hiện hành. Thiếu nguồn dashboard, RCA có thể ghi G1 đúng nhưng UI vẫn đọc `dev`. Đổi checkout về H cũ có thể mất cải chính sau dọn hoặc ảnh hưởng bộ nhận nhẹ. Đây là mâu thuẫn đường vận hành, chưa có lượt mới thất bại.
- **Đề xuất sửa:** Q4 bước 9 ghi đúng lựa chọn chạy thẳng qua `tai_linux.py` như Q4 cũ, và xin quyền cho nhật ký/trạng thái obs, đầu ra, token pool, khôi phục mock/tunnel nếu xảy ra và dữ liệu đơn trên DB thử. Nếu dùng `chuoi_tai`, đặt điều kiện kiểm và kết luận T-070 trước lần dùng đầu tiên. Với bước 10, trình diff hoặc thao tác qua cơ chế Grafana hiện hành để thêm integration vào đúng contact point, nối bộ `online-<lượt>` mà G1 ghi, rồi khôi phục nguồn ban đầu và gỡ riêng integration/receiver T-073 trên `c1da15f`. Giữ `t072-bo-nhan` và luật hiện hành. Trước tiêm, kiểm đích spool từ cả đường Grafana và đích đọc đúng bộ của dashboard như mục đích S4-6/S4-9. Tận dụng thứ tự E5, không áp checkout H cũ. Nếu chưa được Minh cấp quyền cho các thao tác trên, có thể chuẩn bị cấu hình hoặc dùng phát lại để trình bày, với tiêu chí live còn mở.

### R3. C6 mới dùng một phần tiêu chí E5 để nhận đúng ca — CHẶN

- **Ở đâu:** SPEC C6, Q6, bước 10 và tiêu chí xong 4.
- **Sai gì:** C6 dùng điều kiện “cảnh báo của sự cố có `startsAt` sau lúc tiêm”. Điều kiện này không có biên cuối, có thể dựa vào một cảnh báo thành viên của sự cố đã mở, và chưa buộc đối chiếu `t̂` của sự cố được RCA thực sự dùng. Ghi đồ thị con và bảng hạng của ca đúng là tiến bộ. Mốc 25 phút có nguồn nhưng phải tính tới lúc mở được ca trên Grafana.
- **Bằng chứng:** `results/T-073/khai-truoc-e5.json#/tieu_chi/ket_qua_chuc_nang` khóa một sự cố lớp `he-thong` với `t̂ ∈ [mốc tiêm, mốc tiêm + 600 s)`, `t_loi_bang_t_hat = true` và `v082.trung_sha = true`. `#/N` phân biệt thời điểm hiện và mở được ca trên UI với giờ ghi G1. `#/ca_nghiem_thu/muc_tai` ghi tải chạy ít nhất 600 s trước khi tiêm. `c1da15f:rca/online/incidents.py:138–144,183–207` gom nhiều cảnh báo cùng lớp và có thể gộp sau khi khoảng cháy trước đã kết thúc. Tình huống phản ví dụ là luật cũ đã về bình thường nhưng một alert mới trong khoảng gom nhập vào sự cố cũ. Alert mới qua được phép so riêng `startsAt`, trong khi t̂ của sự cố vẫn là của ca cũ. Một alert sau khi gỡ pause cũng qua điều kiện “sau lúc tiêm”. G1 kiểm t̂ so với cửa sổ lõi tại `g1_b.py:152–157`. Q4 đã kiểm hash cho thấy alarm đầu lượt có thể là mất mẫu hoặc p95 lúc khởi động.
- **Bước và quyết định chịu ảnh hưởng:** chặn tuyên bố “đã diễn tập trọn vòng theo ca tiêm này” và “đạt theo đích W5”. C6 đã tách cảnh báo quan sát, dùng ID ca và đề xuất nền. Phần còn thiếu trên có thể làm báo đạt nhầm dù đã thấy một ca mới trên UI. Kết quả mới chưa có.
- **Đề xuất sửa:** tái dùng phần chức năng đã khai của E5 cho demo nếu Minh duyệt Q6. Khai thời gian pause và cửa sổ phát hiện hữu hạn, tối thiểu 600 s nền liên tục có dữ liệu phù hợp với cửa sổ gói, và cách tránh gom với sự cố cũ mà vẫn giữ dữ liệu. Dùng t̂ của đúng sự cố hệ thống để chấm, kiểm hai cờ đã có và đích UI trong 25 phút. Nếu thiếu phủ, báo riêng phủ của đầu vào V082 theo WHY-111, không nâng thành hỏng tuyến khi chức năng đạt. Đồng bộ thời gian tải, thời gian tiêm/gỡ và chờ kết quả để dự toán không vượt trần đã duyệt. Lấy nhãn tiêm chỉ để đối chiếu sau lượt. Cho phép phát lại làm dự phòng. Nếu Minh chỉ cần một ca bất kỳ hiện lên từ đường live, đổi chữ tiêu chí để giới hạn kết luận tới đường truyền và hiển thị, không dùng nó làm bằng chứng tái hiện ca PAUSE-PAYMENT.

### R4. Chữ “không đổi hành vi app” rộng hơn diff và phép kiểm — KHÔNG CHẶN

- **Ở đâu:** SPEC C4, mục Kiểm đúng đắn, Q8.
- **Bằng chứng và hệ quả:** Loại `SPRING_AUTOCONFIGURE_EXCLUDE` xử lý thay đổi auto-configuration đã nêu ở lượt trước. Diff `f178870..ae5a870` còn đổi filter gateway/Booking, wrapper RabbitMQ và annotation validation. Ví dụ `PaymentMessageListener.onPaymentDecisionDelivery` bọc listener thật, gọi ACK trên nhánh thành công, ghi outcome và khôi phục MDC qua `RabbitTelemetry.close`. Nhánh lỗi có ném ngoại lệ, nên lượt đọc này không thấy bằng chứng lỗi bị ghi thành ACK thành công ở đoạn đó. Mã chạy khi agent tắt vẫn có thêm xử lý. C4 đã giới hạn kết luận vận hành, nhưng kiểm diff ConfigMap chỉ xác nhận bỏ biến cấu hình đó, chưa chứng minh mọi hành vi ứng dụng tương đương. `verify` thường và kiểm B16 cục bộ của bản 3 cũng có phạm vi hữu hạn.
- **Đề xuất sửa:** sửa bất biến thành agent tắt và cấu hình Spring đã nêu không áp ở Phần A. Ghi phần thay đổi instrumentation chạy thật và giới hạn kiểm Q8. Giữ lượt soát PR bước 5 để đánh giá diff mới, gồm ngữ nghĩa outcome, MDC và đường giao dịch đã có test. Chưa phát hiện lỗi nghiệp vụ cụ thể ở phần này.

## Đối chiếu các lượt trước

| Điểm | Kết luận đối với phản hồi và bản 5 |
|---|---|
| REVIEW-3 R1 | **Đúng, đã xử lý ở thiết kế.** `env` có ưu tiên trên `envFrom` theo Pod API Kubernetes. Trả file mẫu Secret về main loại đường đưa công tắc từ `ENV_<SVC>`. Bước 4 phải kiểm tất cả manifest đưa vào rollout. Discovery dùng StatefulSet riêng, không có công tắc từ mẫu Secret trong thiết kế hiện tại. Chưa có manifest bản 5 đã render. Bật sau sẽ cần PR cấu hình theo service, là mặt trái so với bật bằng Secret. |
| REVIEW-3 R2 | **Đúng một phần về mức khép.** Đã bỏ biến Spring và thu hẹp kết luận của C4. Q7/Q8 thêm nền và smoke test. Xác minh snapshot/`previous` chưa có, tiêu chí RAM trượt chưa có hành động. Xem R1 và R4. |
| REVIEW-3 R3 | **Đúng một phần về mức khép.** `hieu_luc.py` đã có đích ghi riêng. Phạm vi mới gọi tên obs, máy tải, spool và nguồn dashboard. Vẫn cần quyền thực tế của Q4 bước 9 và đường phục hồi theo layout đang chạy. Xem R2. |
| REVIEW-3 R4 | **Đúng một phần về mức khép.** Đã có ID ca, đích dashboard, nền, đồ thị con và N. So với khóa E5 còn thiếu biên cuối và quy sự cố theo t̂ của ca đã gom. Xem R3. |
| REVIEW-3 R5 | **Đúng, đã xử lý.** Q5 chỉ chọn bản demo, ghi pin và thành phần giữ lại. W7 chờ mở W6/W7. Hồi quy trên dữ liệu cũ chỉ kiểm tính lặp lại. |
| REVIEW-3 R6 | **Đúng, đã xử lý ở hồ sơ mở rộng.** Bản 5 gọi tên cả hai trường exception và giữ biên lọc là OPEN. Không cần chứng minh biên trong pha agent tắt. Gói bật mới cần sentinel và số đo từng service. |
| REVIEW-3 R7 | **Đúng, đã bổ sung bước 8.** Ngrok, fixture, schema/realm, thời hạn bán, dữ liệu phát sinh, mode build và hoàn tác được nêu. `verify/all` và `build` có đường khác nhau. Kết quả của phiên tới mới quyết quyền đổi schema/fixture. |
| REVIEW R1 | **Đúng nếu bật 84 và dùng chung tuyến.** Bộ chuyển đổi Prometheus gộp theo service và capture gateway có thể trộn nguồn. Bản 5 không đưa 84 vào tuyến. Thiết kế tách Prometheus/capture tiếp tục có căn cứ cho pha sau. |
| REVIEW R2 | **Đúng với thiết kế token trong pod.** CD chỉ nhận khóa có tên trong mẫu, Discovery dùng ConfigMap riêng. Bản 5 đưa token vào Collector pha sau, khép phụ thuộc Secret token cho merge lần này. Quyền triển khai Collector và kết nối xác thực giữ OPEN. |
| REVIEW R3 | **Đúng với đường cũ.** Gateway hiện không có lớp xử lý query giống agent Collector exp-app. Có TLS không loại trường nhạy cảm. Bản 5 giữ 84 tắt, lọc tại biên được Minh chọn vẫn là điều kiện trước lần bật. |
| REVIEW R4 | **Đúng nhưng chỉ xử lý một phần trên phạm vi mới.** Overhead khi bật 84 không thuộc bản 5. Rủi ro đổi image và khôi phục snapshot còn ở C4. |
| REVIEW R5 | **Đúng, đã xử lý ở nhánh dựng lại.** `b16-services.txt` tách Assistant khỏi bảy service B16. Kết quả CI GitHub của bản 5 còn là đầu ra bước 5. |
| REVIEW R6 | **Đúng, đã xử lý về cấu hình.** CD vẫn amd64/arm64, có `SERVICE_VERSION`. Phần Keycloak giữ ghim riêng có bằng chứng hiện trạng ở exp-app. |
| REVIEW R7 | **Đúng về pin và ngoại lệ.** Q4 ở `85ace52`, lab hiện hành ở `c1da15f`. Ngoại lệ AGENTS chỉ đúng nhánh PR. Quyền obs mới xem R2 lượt này. |
| REVIEW-2 N1 | **Đúng.** `previous` thay đổi theo deploy/restart thành công. Tắt cứng dời thao tác bật sang PR cấu hình. Điều kiện snapshot trước merge vẫn cần sửa theo R1. |
| REVIEW-2 N2 | **Đúng, áp khi có hai nguồn.** TraceQL tín hiệu ở lab hiện chưa khoanh `exp` trên toàn bộ truy vấn. Mục Mở rộng đã nhắc lọc `exp`. Bản 5 chưa đưa dữ liệu 84 vào kho. |
| REVIEW-2 N3 | **Đúng, để mở lần bật.** B16 §6 phân biệt whitelist trước ghi/xuất với lớp Collector dự phòng. Xóa message không tự xóa bản sao trong stacktrace. Bản 5 đã nêu điều kiện. |
| REVIEW-2 N4 | **Đúng, phần datasource production hoãn.** Nếu bật 84 sau này, cần xác nhận datasource mới đã nạp và đọc đúng kho. Cùng lúc, bước 10 của bản 5 vẫn phải nối UI demo vào đúng bộ G1 hiện hành. |

Quy tắc ưu tiên của `env` và `envFrom` được kiểm trên tài liệu Container của Kubernetes. [Kubernetes Pod API](https://kubernetes.io/docs/reference/kubernetes-api/core/pod-v1/)

## Tuân thủ quy trình

- LOG ghi riêng việc Minh duyệt **viết** bản 5, theo sau trạng thái bản 4. SPEC và STATE cùng ghi bản 5 là đề xuất. LOG nói rõ lượt tự soát của người làm đã thấy tóm tắt trước nên không coi là độc lập. Hash bản 4 khớp bản REVIEW-3 đã soát. Nhánh dựng lại vẫn ở bản 3. Không thấy bằng chứng đã phát thử bản 5.
- STATE còn hai phụ thuộc của phương án cũ là IP 84 trước bước 6 và người giữ `ENV_<SVC>` trước bước 9. SPEC bản 5 và LOG không còn dùng các điều kiện ấy cho hai bước đó. T-070 §12 cũng còn trỏ việc bật 84 sang T-076. Báo sai lệch để Minh duyệt đồng bộ sau khi quyết SPEC, giữ nguyên hồ sơ ghim lần chạy. Không dùng hai dòng cũ làm lệnh triển khai.
- WHY-08/09/89 giải thích giữ lõi và tín hiệu. WHY-105–111 giải thích biểu thức luật, thời gian và độ phủ. Q7 là ngưỡng mới để Minh quyết, chưa thấy WHY cho ngưỡng này hoặc căn cứ rằng nó phân biệt regression với dao động nền. Đề nghị quyết và trình ghi WHY/DECISIONS trước khi dùng làm kết luận. Không sửa file nguồn trong lượt phản biện.

## Điều đã kiểm và thấy đúng

- Hash `khai-truoc-e5.json` và `trien-khai-e5.md` khớp các giá trị LOG T-073 ghi cho bản khóa và bản áp dụng. Q4 khớp 12/12 trong `SHA256SUMS`. Kiểm `git diff --check f178870 ae5a870` sạch. Đọc `verify/tien-do.tsv` xác nhận 8/8 verify thường, 7/7 B16 mã thoát 0, Booking profile lỗi. Số 67 lỗi ở log verify của bản 3. Không tìm thấy manifest cho gói T-076, nên các số mô tả file đang lưu.
- Hai máy được phép đọc đều cho lab `c1da15f`. Exp-app giữ image Payment `arm64-t067-36a3725d` và Keycloak `arm64-776d9c9e`. Đây là hiện trạng, không phải bằng chứng cho pin demo mới. `git ls-remote` gặp reset kết nối GitHub, nên chưa xác nhận được main/head PR mới nhất từ server. Giữ điều kiện kiểm lại base/head thật và dùng lease khớp đầu nhánh ở bước 5.
- Đường online lấy t̂ từ webhook, ghép tín hiệu quan sát trong cửa sổ, chạy bản chụp V082 ghim và sinh G1 theo ca. Sổ tiêm không tham gia vào đường này theo code và SPEC. Không đổi đặc trưng, lan theo cạnh, tập ứng viên hay xếp hạng. Không có phép đối chứng đồ thị mới trong lượt tích hợp này. Độ phủ và chất lượng chỉ có thể báo theo bằng chứng của lượt được phép chạy tiếp.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. Kiểm lại SPEC bản 5, đối chiếu cả phản hồi cũ và các phần thay đổi với đường vận hành.
2. Chỉ thêm `tasks/T-076-pr17-otel-may-84/REVIEW-4.md`.
3. Kiểm hash, diff, log kết quả cục bộ, code và trạng thái hai máy bằng lệnh đọc. Không vào máy 84, không chạy tải hoặc tiêm lỗi, không mở dữ liệu khóa, không commit.
4. **Đề nghị tiếp tục lượt đáp.** Giữ phương án agent tắt cứng. Trình xác nhận đích quay lui và hành động Q7 trước merge. Chốt đúng quyền Q4, đường bật/hoàn tác trên lab hiện hành và tiêu chí E5 dùng cho demo trước các bước tương ứng. Ưu tiên Q8 hẹp cùng GET đã khai, kiểm ngrok/fixture ở bước 8 rồi chỉ đổi dữ liệu khi Minh duyệt, và giữ W7 chờ mở lại. Giá trị production sau rollout, hiệu quả demo mới và tính phù hợp của biên lọc khi bật 84 vẫn mở. Chưa có phản hồi của người làm về các điểm lượt này.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/SPEC.md (bản 5, đề xuất).
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4, không có khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,SPEC.ban-4.md,SPEC.ban-3.md,LOG.md}, results/T-076/{bang-file-pr17.md,kiem-cuc-bo/README.md}, results/T-070/don/{KE-HOACH-DON.md,q4/README.md}, results/T-073/{khai-truoc-e5.json,trien-khai-e5.md}, DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/{REVIEW.md,REVIEW-2.md,REVIEW-3.md,REVIEW-4.md} và các bảng đáp hiện có.
- Code và kết quả liên quan: D:/Project/flash-ticket-platform (refs cục bộ f178870, bb84d64, 36a3725d), D:/Project/ft-pr17-dung-lai (ae5a870), D:/Project/flashticket-rca-lab (c1da15f), results/T-076/kiem-cuc-bo/, results/T-070/don/q4/SHA256SUMS. Chỉ đọc nguồn đã được Minh cho phép.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat khi chưa có quyền ghi riêng cho lượt đáp. Nếu Minh cấp quyền, ghi đúng phần được nêu.

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

Người làm chỉ điền bảng trong phạm vi Minh duyệt. Giữ nguyên nhận xét và prompt. Để trống cột Minh quyết.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN | `deploy-k8s-service.sh:13,24,170–175,261–271,285–295` @nhánh: trạng thái ở `<app_root>/state/k8s/<svc>/` (`current`, `previous`, `<rev>/image`, `<rev>/secret-env.json`); `rollback` chỉ về `previous` khi digest khớp `image`; không có revision trước thì CD chỉ in hướng dẫn. Bản 6 (Minh duyệt viết 27/11): bước 6 đọc chỉ-đọc `current`/`previous`/`image` từng service trong plan CD (không đọc `secret-env.json`), service không có đích quay lại thì báo Minh trước merge, hẹn nhóm không triển khai 60 phút, đối chiếu lại `previous` khi cần quay lại; đường dự phòng PR revert khẩn cấp (Q10, ngoại lệ có chủ đích). Q7 thành "báo và trình", chỉ dừng khi crash/OOM hoặc GET trượt; Q8 khai trước 2–3 GET, mỗi cái 3 lần, điều kiện HTTP 200 và trường chính; giới hạn kết luận ghi rõ. | |
| R2 | Đúng; CHẶN | `results/T-070/don/q4/README.md`: Q4 chạy `tai_linux.py start` từ obs; `results/T-073/trien-khai-e5.md` §5 dùng `/opt/rca-lab`, `1bb40ca`, `t065-l11-001`. Bản 6: phạm vi ghi bước 9 (obs `/srv/flashticket-rca/load/`, token pool, mock/đường hầm, đầu ra máy tải, đơn trong DB thử), không dùng `chuoi_tai`; bước 10 theo runbook mới `results/T-076/exp-app/runbook-online.md` trên `c1da15f` (bộ nhận T-073, integration qua API Grafana có JSON trước/sau, bộ điều phối ghi `online-<lượt>`, dashboard sinh bằng `build_dashboards.py` có sao lưu; hoàn tác trả `dev`, gỡ integration, dừng bộ nhận; giữ `t072-bo-nhan` và luật; không checkout bản lab cũ), Minh duyệt runbook trước khi chạy; trước tiêm kiểm cả Grafana → spool và dashboard đọc đúng bộ. | |
| R3 | Đúng; CHẶN | `results/T-073/khai-truoc-e5.json#/tieu_chi/ket_qua_chuc_nang`, `#/N`, `#/ca_nghiem_thu`; `incidents.py:138–144,183–207` gom cảnh báo cùng lớp. Bản 6 C6 dùng lại nguyên tiêu chí E5: tải ≥ 600 s, tiêm `PAUSE-PAYMENT` `--seconds 600`, không có sự cố `he-thong` đang mở trước tiêm, t̂ ∈ [mốc tiêm, +600 s), `t_loi_bang_t_hat` và `trung_sha` đúng, **mở được** trang ca của đúng sự cố trong N = 25 phút từ t̂; bỏ sót/quá N ghi như E5; thiếu phủ báo riêng theo WHY-111; tổng thời lượng ≤ 1 giờ khai trong runbook. | |
| R4 | Đúng; KHÔNG CHẶN | Bản 6 C4 và mục Kiểm đúng đắn: đổi thành "agent tắt và biến Spring không áp ở Phần A"; liệt kê code B16 vẫn chạy thật (log JSON, filter correlation, bọc listener RabbitMQ, bỏ `@Valid` trùng ở 6 DTO); ngữ nghĩa outcome/MDC/ACK đánh giá ở lượt soát PR bước 5; giới hạn kết luận của Q8. | |
