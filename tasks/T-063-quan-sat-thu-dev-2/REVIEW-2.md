# Phản biện T-063 — lượt 2, sau đợt thu chính dev bản 2

- **Người phản biện:** Codex. **Ngày:** 14/11/2026 giờ Việt Nam; kiểm 13/11 khoảng 19:40–19:51Z. **Commit:** HEAD c3d27f8a; đầu ra chưa commit.
- **Công đoạn/cổng:** soát kết quả, M2 chiến dịch M1-FlashTicket. Claude làm; chỉ được tạo REVIEW-2.md.
- **Đã đọc:** AGENTS, STATE, SPEC/LOG T-063; chiến dịch/checkpoint; mục tiêu/RQ MRP, DT18, hướng dẫn cô, LESSONS; DECISIONS phần chiến dịch và chuyển bộ chạy; WHY-81–84; báo cáo, bảng tín hiệu, thay đổi máy, B16 bản 2 và B16 nguồn; lịch/hồ sơ lượt/đóng băng, runner2/3, inj2, exporter, hậu kiểm; gói thật thu2; phân tích span/CPU/ca nền, kiểm R/tích hợp; adapter/span và code đọc tín hiệu M1-FT liên quan.
- **Tự soát độc lập:** kiểm hash trước dùng; lần tải → sổ/đầu dò → dữ liệu thô → adapter → input/output P7. Sau tự soát mới đọc REVIEW.md và phản hồi. Đã nhận bổ sung 19:43–19:44Z của Claude về span mới; không giữ nhận xét “chưa chạy script” của bản báo cáo trước đó.

## Kết luận chung

**Đợt thu đã hoàn thành và có thể tiếp tục phân tích dev trong phạm vi đã kiểm. Chưa nghiệm thu toàn T-063.** R1–R4 đã được xử lý đúng mức cần cho lượt thu; không thấy căn cứ thu lại toàn đợt. R5 chặn nghiệm thu phần phân loại trace đầy đủ; R6 cần thu hẹp một kết luận cơ chế. H3/H4 vẫn thiếu ô lỗi và hồ sơ còn đầu ra chưa hoàn thiện. Đây chưa là bằng chứng hiệu quả đồ thị hay trả lời xong RQ5.

## Các điểm

### R5. Chưa phân biệt các nguồn span thiếu cha trên tải mới — CHẶN nghiệm thu phần phân loại trace

- **Ở đâu:** results/T-063/bao-cao.md §3, §5–6; span-goc/phan-loai-dev2.json; câu hỏi span gốc và tiêu chí cơ chế của SPEC.
- **Thiếu gì:** bản mới đã chạy đủ script, nhưng chỉ báo trung bình mồ côi 1,0/ca và để việc lần tiếp ở nhóm CLIENT khác. Chưa giải thích 13 span thiếu cha hoặc ghi các giải thích/bằng chứng thiếu cho từng nhóm. Đây là phần phân loại dữ liệu của T-063, không đòi làm đánh giá phương pháp thuộc T-064. Các nhóm thực tế có căn cứ khác nhau.
- **Bằng chứng độc lập:** đếm lại raw-traces.jsonl trong cả 13 archive, dùng traceId+spanId để tìm cha trên toàn gói; khớp bảng phân loại mới 13/13. Có 11 span Payment ở 46aab4be, một span Event ở 5fb8208f và một span Event ở f20b0ca5. Con trỏ phan-loai-dev2.json: #/46aab4be/theo_service_nhom/payment-service|mo_coi và hai khóa event-service|mo_coi tương ứng; chi tiết tại #/<mã>/chi_tiet, nhom=mo_coi.
- **Lần tới nguồn:** hai span Event là JDBC trên HikariPool-1:connection-adder. GET Tempo chỉ đọc tìm thấy cha, nhưng cha kết thúc khoảng t−1.483 s và t−2.871 s, ngoài cửa sổ đóng gói ±600 s. Không phải mất bản ghi cha trong chính cửa sổ ấy. Luồng nền giữ context cũ là ứng viên, chưa xác nhận cơ chế truyền context. Với Payment, Tempo tìm thấy hai span cha mà gói không có; chúng bắt đầu/kết thúc gần t−2,4 s, nằm trong cửa sổ đóng gói. “Cha ngoài cửa sổ” không giải thích được nhóm Payment. Dữ kiện tái kiểm ở phụ lục A.
- **Payment còn OPEN vì sao:** span có thể đến kho sau stage, hoặc đường capture/xuất/đóng gói bỏ bản ghi. Chưa xác định bước làm thiếu. File capture 13:14Z được manifest dẫn tới hiện không còn trên máy, nên không thể so trực tiếp tiền tố đó trong lượt này. Không có căn cứ chọn một nguyên nhân. Cần đối chiếu snapshot/capture nếu còn bản khác, cấu hình và log exporter quanh pause/stage; nếu không còn, ghi không thể xác định bước mất bằng dữ liệu đã lưu. Phân tích chỉ đọc này dự kiến phút đến vài chục phút, chưa đo; không cần thu lại tải để phân loại phần hiện có.
- **Phần có thể bác bỏ finding:** báo cáo tự nhận đạt một phần; số đếm mới đúng. Không cáo buộc số sai hoặc toàn đợt hỏng. Tuy nhiên “chưa lần” chưa thay được phân xử/giới hạn SPEC yêu cầu, nhất là khi có thể tách nhóm từ dữ kiện sẵn có.
- **Bước/quyết định chịu ảnh hưởng:** chặn nghiệm thu trọn câu hỏi span gốc và kết luận đã xử lý hết thiếu context trên tải mua vé. Không chặn phân tích độc lập ca khác, không tự động buộc loại PAUSE-PAYMENT. Chưa đo tác động riêng của 11 span tới điểm/hạng; không gọi đó là nguyên nhân hạng sai P7.
- **Sửa tối thiểu đề xuất:** thêm phân loại hai nhóm Event/Payment và hệ quả vào phân tích span/báo cáo; giữ giới hạn Payment nếu không phân xử được. Lần nhóm CLIENT khác từ dữ liệu đã có: 3.595/8.245 gốc CLIENT khác là basic.ack Booking trên luồng RabbitListenerEndpointContainer. Nhóm này đã được nhận diện ở pilot tải mua vé trong kiem-r/BAO-CAO.md. Không cần thu thêm để biết nhóm chính đó; không coi toàn bộ phần tăng là mất context. Với nhóm còn lại, ghi căn cứ hoặc phần thiếu cụ thể.

### R6. “Đã loại autovacuum và checkpoint” vượt bằng chứng — KHÔNG CHẶN dữ liệu thu

- **Ở đâu:** results/T-063/bao-cao.md §3, dòng ca bình thường; nguồn dẫn results/T-064/phan-tich/ghi-chu-co-che-dev2.md Q4.
- **Sai gì:** Q4 nói hai ứng viên “không được ủng hộ” bởi phép đếm hiện có; báo cáo nâng thành “đã loại”. Sự có mặt ở cả ca có cờ và ca không cờ không loại được ảnh hưởng phụ thuộc thời điểm, bảng, thời lượng hoặc I/O. Đây là lỗi mức kết luận, không phải lỗi thu.
- **Bằng chứng:** đếm lại log PostgreSQL trong method-input.json của bốn archive đã kiểm hash. Checkpoint complete N/A đều 1/1. Tổng vacuum/analyze N→A: eb48d6b3 5/18→5/21; f20b0ca5 2/13→2/14; 729604d2 3/20→5/15; 83073ed1 5/14→3/19. Đây là toàn instance; Q4 còn tách DB/bảng. Cả hai cách đếm chưa đối chiếu mức vượt ngưỡng theo thời gian với thời lượng/I/O từng hoạt động. Nguồn: outputs/<mã>/method-input.json phần tử [2], entity=postgresql-shared-instance, chia N/A theo [5].
- **Phần phản bác đã xét:** vắng autovacuum event_db trong eb48d6b3 chống giả thuyết autovacuum trực tiếp trên DB đó. Nhưng instance dùng chung, nên chưa loại ảnh hưởng gián tiếp. Q4 đúng khi không suy vắng log chờ khóa thành không có khóa. TD-06 đã ghi bật log_lock_waits; nên đối chiếu cấu hình thực và giới hạn thời gian ghi log trước khi nói không biết đã bật chưa.
- **Bước/quyết định chịu ảnh hưởng:** không được coi hai cơ chế đã bị bác bỏ khi chọn giải thích hoặc thiết kế H6/H8. Không yêu cầu chứng minh nhân quả xong trong T-063; không chặn dùng dev hay nhánh độc lập.
- **Sửa tối thiểu đề xuất:** ghi “phép đối chiếu hiện có chưa phân biệt được; chưa đủ căn cứ quy nguyên nhân hoặc loại hai ứng viên”. Nếu lựa chọn thiết kế phụ thuộc nguyên nhân này, đối chiếu mốc cờ với log đã lưu trước; dự kiến vài phút đến vài chục phút, chưa đo. Thiếu I/O/khóa ngắn thì nêu giới hạn và quyết định phụ thuộc. Không cần chạy lại baseline hoặc thu cả đợt.

## Đối chiếu các lượt trước

| Điểm và phản hồi lượt 1 | Đánh giá độc lập |
|---|---|
| R1 dọn lỗi vẫn phát ô sau | **Đúng; sửa phù hợp cho lượt thu.** runner2/3 truyền cleanup-error; verify trước chu kỳ, không sạch thì dừng. inj2 có hẹn giờ toxic/pause. Mô phỏng chay/kiem-sua-R1/mo-phong.txt: một cycle-begin rồi run-abort-dirty; thử hết hạn có verify sạch. Code khớp pin bản 2. Sổ chính không có cycle-error/dirty; không có bằng chứng lan lỗi. Không suy mọi sự cố đều đã thử. |
| R2 thiếu tích hợp cuối | **Đúng; đã bổ sung phần cần cho lượt thu.** kt57fcd7 sau TD-09 có P7 OK, lặp trùng, chống thư mục trùng và xuất/nhận bản 3. Lượt ngắn runner3 kiểm vận chuyển mới; lượt chính có đủ archive/hash. Chốt thư mục trùng chưa tự là kiểm nhánh M1 lỗi rồi stage mã mới; không ca chính nào cần nhánh này. Không giữ điểm chặn cũ chỉ vì chưa có lỗi thật. |
| R3 đầu dò không tự phân loại | **Đúng; chọn hậu kiểm hợp lệ.** Điều kiện khai khoảng 07:30Z sau phát nhưng trước đọc dữ liệu chính theo hồ sơ; không gọi là khóa trước phát. Đếm audit/k6/sổ khớp kết quả lưu. Giữ 12/13 ban đầu và 13/13 sau sửa; dùng tập sửa làm chính vẫn chờ Minh. |
| R4 điều kiện CPU chưa đủ | **Đúng; phản hồi giữ giới hạn phù hợp.** Không đổi cường độ theo số đẹp. PSI máy avg60 ở t−240/t+60/t+330: CPU-BOOK-1 12,32/22,89/28,69%; CPU-BOOK-2 14,92/48,77/68,58%. Đây là ba mốc, không là trung bình pha; chưa xác nhận CPU-BOOK-1 “PSI tăng ≤×2”. Hai ca hợp lệ về số luồng/throttle, chưa là hai cơ chế cô lập. Nguồn: thu2/tiem-loi/so-thu2.jsonl, probe.psi_cpu_may theo opaque_id/phase. |

Không mở lại task tải đã kiểm. Kiểm thêm summary cả đợt: dropped_iterations=0 và ExitCode=0 ở 13/13. Mất mạng laptop trước lượt chính được tách đúng khỏi kết quả phương pháp.

## Tuân thủ quy trình và mức đạt

- Chỉ tạo REVIEW-2.md. Không LOG/STATE, sửa code/kết quả, commit, gọi agent khác; không đọc dữ liệu khóa, repo lưu trữ, env hoặc nội dung khóa. SSH chỉ GET API/đọc file. Windows OpenSSH từ chối ACL khóa; dùng SSH của Git với cùng khóa/known_hosts, không sửa quyền hay sao chép khóa.
- Quyền chiến dịch bổ sung trong DECISIONS cho Claude điều phối/gọi phản biện; không áp yêu cầu chuyển thủ công cũ thành vi phạm. Hook services/event-service/src/rca-test ngoài danh sách đường dẫn được sửa; báo cáo hiện đã trình đúng phần cần Minh cho phép.
- Revision và thay ô có WHY-83/84; không phải yêu cầu thuật toán của DT18/cô. Không thấy nhãn can thiệp lọt vào input P7 đã kiểm; sổ/audit ở phía xác nhận/chấm. Đây là chế độ biết mốc sự cố, không phải kiểm detector tự phát hiện.
- **Đạt:** thu xong, băm và P7 từng ca; quan sát bổ sung có thật. **Chưa đạt trọn:** phân xử/khai giới hạn span mới theo R5; lần thật “hết hạn → chờ → tự gọi lại”; manifest toàn T-063 và o-dev-bo-sung.json. Báo cáo đã khai các đầu ra thiếu, không biến chúng thành lỗi khoa học khác.
- H3/H4 có metric nhưng chưa có ô cạn pool/consumer tụt sau; pool-pending và queue-ready bằng 0 ở mọi mẫu đã lưu. Không dùng bộ này kết luận hai hướng vô ích; không buộc xong T-064 mới nhận phần thu hợp lệ.
- B16 bản 2 vẫn là đề xuất, không là chuẩn đã duyệt hay triển khai đủ. Đối chiếu B16 nguồn và một số tài liệu chính thức; chưa xác nhận lại toàn bộ trang dẫn. [OTel Java agent 3.0 preview](https://opentelemetry.io/blog/2026/java-agent-3.0-preview/) hỗ trợ rủi ro đổi semconv/instrumentation; [Loki retention](https://grafana.com/docs/loki/latest/operations/storage/retention/) hỗ trợ yêu cầu cấu hình retention. Không biến đề xuất K3s thành lỗi dữ liệu Docker hiện tại.

## Điều đã kiểm và thấy đúng

| Kiểm chỉ đọc | Kết quả |
|---|---|
| thu2/SHA256SUMS | 214/214 khớp; sha256sum -c và đếm độc lập bằng Node crypto |
| Manifest trong archive | 65/65 file cases/<mã>/manifest.json khai khớp byte/hash |
| Input/output P7 | 13/13 input khớp summary.input_sha256; 26 output khớp output_sha256, hai bản/ca trùng byte; status OK, 39 pin/ca |
| Pin code/đóng băng | 12/12 laptop_file_sha256 bản 2; 39/39 source pin; local stage-m1/run-m1/safe-export khớp pin. Không khẳng định kiểm lại mọi cấu hình máy hiện tại |
| Sổ | 127/127 seq/prev_sha256 đúng; SHA trên dòng UTF-8 trước, bỏ newline |
| Audit/k6 | HTTP5 có 720/2.161 audit trong lỗi, mỗi ô 20 khe 30 s, không có trước/sau; k6 tương ứng 720/2.161 hành trình lỗi |
| Payment | Hai probe paused true; hồi running false; live-down :8083 có 20 mẫu nền 0 và 20 mẫu sau t bằng 1. Nguồn: thu2/ca/46aab4be/prometheus-bo-sung.json, bundles[channel=live-down], http_url chứa :8083 |
| Raw trace | 13/13 khớp phan-loai-dev2.json; CONSUMER gốc 0; 13 mồ côi như R5 |
| CPU cũ | Sáu dòng pha cpu-book/thu-cuong-do-lan1.jsonl khớp CPU/throttle/PSI/p99 báo cáo. Cụm CFS vẫn là suy luận chưa đo trực tiếp; không mở rộng sang mọi tải |

**Kênh bổ sung:** 13 gói ×24 bundle, không lỗi khúc. threads-blocked rỗng 13/13; truy vấn kho hiện tại cũng chỉ có runnable/timed_waiting/waiting. throttle-ratio hữu hạn ở Booking 533/533 mẫu; 5.845/5.845 mẫu của 11 thực thể còn lại NaN. Adapter đổi số không hữu hạn thành thiếu, không là bằng chứng “không throttle”. samples luôn 1 vì count by(service_name) bên ngoài count_over_time đếm số chuỗi, không giữ số mẫu bên trong. dong-goi/README.md đã khai không dùng; H5 hiện đọc live-down/live-ms, nên không thêm finding chặn cho kênh chưa dùng. Ngữ nghĩa [count](https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators) và [count_over_time](https://prometheus.io/docs/prometheus/latest/querying/functions/#aggregation_over_time) đối chiếu Prometheus. Có chuỗi không đồng nghĩa có giá trị hữu hạn có nghĩa.

## Phụ lục A — Dữ kiện truy span cha

Gói: results/T-063/thu2/ca/<mã>.tgz, cases/<mã>/raw-traces.jsonl. Lệnh chỉ đọc trên exp-obs: Python urllib.request.urlopen('http://127.0.0.1:3200/api/traces/'+traceId, timeout=20), duyệt batches → scopeSpans → spans; đổi ID base64 Tempo thành hex, lọc spanId. Kết quả GET được lưu trong bảng làm bằng chứng lượt này.

| Ca | traceId; spanId cha | Cha trên Tempo; thời gian so với t |
|---|---|---|
| 46aab4be | 1a2ad69c7d138b90a49f0baa0cb8e40b; 203105619fac9a5a | booking.order-completed.v1 process, −2,385→−2,351 s |
| 46aab4be | cùng trace trên; c8e902dd99d2f695 | InboxMessageRepository.save, −2,358→−2,357 s |
| 5fb8208f | 619d4a771c6ceaac3b8b40f20a2cc1f2; d02cb8a1de7329fe | GET /api/v1/events/{id}, −1.483,127→−1.483,111 s |
| f20b0ca5 | 68a7da36cbeb614d3c80e0f1b3416e6b; bc57ab78297952a2 | OutboxWorker.relay, −2.870,558→−2.870,547 s |

Child Payment gần t−2,4 s; child Event ở t−64,530 và t−37,480 s. Kiểm tồn tại /opt/flash-ticket-obs/pinned/data/capture/traces-2026-11-13T13-14-02.009-size.jsonl → không còn. Không suy từ một file rằng mọi capture đều mất.

**Tác động hash:** runner2/3, inj2, exporter, lịch/tải ghim trong dong-bang-2.json; stage/run/safe-export ghim T-058. Không sửa chúng hay ghi đè archive/manifest cũ để xử lý finding. R5/R6 chủ yếu thêm phân tích/báo cáo; đổi bao-cao.md đổi hash báo cáo, không đổi 214 mục thu2/SHA256SUMS. Sửa hook H3 đổi image/revision và đóng băng mới; giữ riêng ca mới/cầu so sánh, không sửa pin đợt đã thu. Chưa có manifest toàn T-063 để âm thầm cập nhật cho khớp.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** tự soát nguồn, code, dữ liệu thật, mọi archive; đọc phản hồi sau đó; truy cha Tempo để tách loại thiếu cha.
2. **File thay đổi:** chỉ tasks/T-063-quan-sat-thu-dev-2/REVIEW-2.md. Không thêm/sửa quyết định, không commit.
3. **Kiểm:** các bảng trên; không chạy thực nghiệm mới. Chưa xác nhận bước làm thiếu span Payment, giới hạn R5 giữ nguyên.
4. **Bất đồng/câu hỏi mở và đề xuất để Minh quyết:**
   - **Nghiệm thu:** nhận phần thu đã kiểm, chưa nghiệm thu toàn task; Claude đáp R5/R6 và hoàn thiện đầu ra trong quyền. Bỏ/thu lại toàn bộ 13 ca chưa có lợi ích chứng minh. Mặt trái của tiếp tục là phần cơ chế còn mở, phải giới hạn kết luận phụ thuộc.
   - **PAUSE-PAYMENT:** đề xuất Minh chấp nhận tập 13 theo sửa điều kiện kỹ thuật: D2 đã khai Paused=true, probe/liveness xác nhận độc lập với điểm M1. Giữ tập 12 và khai sửa sau dữ liệu. Mặt trái: tập chính có sửa sau; phương án 12 chính/13 bổ sung giữ điều kiện nguyên bản nhưng thiếu ô trực tiếp duy nhất của H5 trong tập chính. Đây chưa là Minh duyệt.
   - **FLASH-HEALTHY:** giữ nhãn “không tiêm lỗi” và K đã khai; báo tách thêm bốn BINH-THUONG và một tăng tải. Không đổi đáp án/bỏ ca vì phương pháp gắn cờ hoặc độ trễ tăng. Tỉ lệ vượt phân vị chưa tự chứng minh suy giảm có ý nghĩa thực hành. Đổi tiêu chí sau xem phải được Minh quyết và báo bổ sung. Mặt trái của giữ là K đo cả phản ứng với tải; phân tầng làm rõ điều đó.
   - **H3:** đồng ý xin sửa đúng hook thử Event, build/thu bổ sung với đối chứng phù hợp. Đổi image là mặt trái, không gộp thẳng cohort cũ. Chấp nhận thiếu ô là phương án khác nhưng kết luận về H3 OPEN. H4 còn quyền chuẩn bị tải/thu bổ sung; Claude rà code/kết quả và báo chi phí trước phát theo luật hiện hành. Reviewer không phát thực nghiệm thay.
   - **Lưu dữ liệu:** giữ đủ gói hiện có; khi commit đề xuất kho artifact bền do Minh chỉ định, git giữ manifest/code/báo cáo. Đánh đổi: thêm nơi sao lưu/quyền; phương án khác git LFS. Chưa upload, đổi ignore hay xóa file. Chưa chọn nơi lưu không chặn phân tích cục bộ.

**Đề xuất tiếp tục bằng lượt người làm đáp R5/R6 và phản biện các đề xuất trên.** R1/R2 trước thu không còn phản đối chưa xử lý. Không áp số lượt cố định, không chạy lại chỉ để có số mới. Minh quyết sửa/chấp nhận giới hạn/dừng; dừng không tự nghiệm thu, khóa thiết kế hoặc mở test. Chưa có phản hồi cho hai finding mới nên chưa gọi là bất đồng hai bên đã xác lập.

## Prompt bàn giao cho người làm

Nguyên văn Prompt chung + Người làm đáp phản biện, chỉ điền metadata. Mẫu không có khối cổng M2 giai đoạn 2; không tự ghép G3/G4. Theo mẫu, người làm kiểm cả các đề xuất chờ Minh trong bản này.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-063, tasks/T-063-quan-sat-thu-dev-2/, kết quả sau đợt thu chính dev bản 2 và các đề xuất trong REVIEW-2.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: chiến dịch M1-FlashTicket, mốc M2 theo tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md mục 7; giai đoạn 2 không có khối cổng riêng trong mẫu.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện theo SPEC T-063.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; SPEC.md và LOG.md T-063; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md và CHECKPOINT-CHIEN-DICH.md; results/T-063/bao-cao.md, quan-sat/thay-doi-may.md, o-dev-bo-sung.md, dong-bang.md; docs/WHY.md và DECISIONS.md; commit gốc c3d27f8a, đầu ra chưa commit.
- Phản biện và phản hồi trước: tasks/T-063-quan-sat-thu-dev-2/REVIEW.md và bảng phản hồi; REVIEW-2.md.
- Code và kết quả liên quan: results/T-063/thu2/ (SHA256SUMS, ca/, chay/, tiem-loi/, audit/, tai-out/); results/T-063/span-goc/, cpu-book/, ca-nen/, chay/, dong-goi/, kiem-r/, kiem-tich-hop/; results/T-064/phan-tich/ghi-chu-co-che-dev2.md; src/m1/ và src/m1_ft/; exp-app/exp-obs chỉ đọc qua SSH với khóa/known_hosts như results/T-063/chay/runner2.py, không chạy tải, tiêm lỗi hoặc đổi cấu hình.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat theo prompt này; prompt không tự cấp quyền. Nếu Minh hoặc quyền chiến dịch hiện hành đã cho phép ghi phản hồi: chỉ bảng Phản hồi của người làm cuối REVIEW-2.md và nối LOG.md T-063; giữ nguyên nhận xét/prompt reviewer. Sửa kết quả/code theo đúng quyền hiện hành.

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

Chỉ điền bảng này và LOG khi có quyền; giữ nguyên nhận xét/prompt; thêm N1, N2… cho tự soát. Để trống cột Minh quyết.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R5 | Đúng; chặn nghiệm thu phần phân loại trace | Đếm lại `span-goc/phan-loai-dev2.json`: 13 span mồ côi (Payment 11 ở 46aab4be; Event 1 ở 5fb8208f, 1 ở f20b0ca5); gốc CLIENT khác 8.245, trong đó Booking `basic.ack` 3.595 — khớp số của người phản biện. Chưa tự truy lại Tempo cho bốn span cha ở phụ lục A. Đã thêm mục 7 vào `results/T-063/bao-cao.md`: tách hai nhóm, giữ nhóm Payment là chưa xác định bước làm thiếu, nêu hai giải thích và bằng chứng cần. Còn thiếu: nhóm `PUT`/`GET` 260 mỗi service chưa kiểm đích; chưa đo ảnh hưởng của 11 span tới điểm M1 ở ca PAUSE-PAYMENT | |
| R6 | Đúng; không chặn | Báo cáo ghi "đã loại" trong khi ghi chú Q4 chỉ nói "không được ủng hộ". Đã sửa câu ở mục 3 thành "chưa phân biệt được, chưa đủ căn cứ quy nguyên nhân hoặc loại". Về khóa: TD-06 ghi đã bật `log_lock_waits`; Q4 của T-064 viết "chưa kiểm có bật không" là thiếu sót của người làm, đã ghi bổ sung ở Q4 và mục 7 báo cáo (chờ khóa ngắn hơn `deadlock_timeout` vẫn không được ghi) | |
| N1 | Tự tìm, KHÔNG CHẶN — nay đã có bằng chứng | Chuỗi hash sổ: người phản biện kiểm 127/127 | |
| N2 | Tự tìm, KHÔNG CHẶN | Chưa có lần "hết hạn → chờ → tự gọi lại" chạy trọn trên Codex thật; người phản biện cũng ghi chưa đạt trọn | |
| N4 | Tự tìm, KHÔNG CHẶN — nay đã có bằng chứng | P7 13/13 OK, 26 đầu ra trùng byte theo cặp: người phản biện kiểm | |
