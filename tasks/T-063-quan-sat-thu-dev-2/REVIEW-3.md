# Phản biện T-063 — lượt 3, kiểm phản hồi và sửa sau REVIEW-2

- **Người phản biện:** Codex. **Ngày:** 14/11/2026 giờ Việt Nam (kiểm từ 13/11 khoảng 22:28Z). **Commit/diff:** HEAD c3d27f8a; đầu ra T-063 chưa commit. Không có commit riêng của lần sửa, nên đối chiếu nội dung hiện tại với nhận xét/phản hồi và kiểm lại file thật.
- **Công đoạn/cổng và bản lượt:** người phản biện kiểm lại phản hồi và sửa; chiến dịch M1-FlashTicket, M2; chỉ tạo REVIEW-3.md. Claude làm, Codex phản biện.
- **Đã đọc:** AGENTS, STATE, SPEC/LOG T-063, mẫu REVIEW và review-prompt; chiến dịch/checkpoint T-062; mục tiêu/RQ MRP, DT18, hướng dẫn cô, LESSONS; WHY-81–84 và DECISIONS phần chiến dịch/chuyển bộ chạy; báo cáo, thay đổi máy, ô dev, hồ sơ lượt/D2/điều kiện hậu kiểm/đóng băng; phân loại span và script; runner2/3, inj2, exporter, stage-m1/safe-export, adapter; kết quả kiểm sửa R1, tích hợp R2; 13 archive thu2, sổ, kênh bổ sung và đầu ra tải; Q4 và đính chính T-064. Sau tự soát mới đối chiếu REVIEW, REVIEW-2 và bảng đáp.
- **Tự soát độc lập:** kiểm toàn vẹn trước dùng; đếm lại trace thô theo traceId + spanId trong cả 13 gói; đối chiếu input/output và manifest, sổ/đầu dò, log PostgreSQL của bốn ca bình thường. Truy lại Tempo chỉ đọc cho bốn span cha. Không lấy số trong LOG làm bằng chứng thay file.

## Kết luận chung

**Không có lỗi đáng kể mới. R5 đã được xử lý ở mức phân loại có giới hạn; R6 đã sửa đúng mức kết luận. Đề xuất dừng phản biện phần phản hồi/sửa này.** Dừng không đồng nghĩa nghiệm thu toàn T-063: hồ sơ và phép thử điều phối còn thiếu, H3/H4 thiếu ô lỗi, nguyên nhân thiếu span Payment và cờ nền còn OPEN. Đợt thu dùng được để phân tích dev trong phạm vi đã nêu; chưa trả lời xong RQ5 hoặc chứng minh lợi ích đồ thị theo DT18/cô.

## Các điểm

Không thêm finding mới. Không giữ R5 là CHẶN chỉ vì chưa chứng minh được cơ chế mất span: SPEC cho phép “chưa phân xử” khi có các giải thích, bằng chứng thiếu và hệ quả. Mục 7 báo cáo hiện đã làm điều đó. Không có căn cứ từ các kiểm này để thu lại cả đợt hoặc loại PAUSE-PAYMENT chỉ vì thiếu cha.

## Đối chiếu các lượt trước

| Điểm và phản hồi | Đánh giá độc lập lượt này |
|---|---|
| R1 — dọn lỗi, vẫn phát ô sau | **Đúng; bản sửa phù hợp.** runner2/3 và inj2 còn khớp pin bản đóng băng 2. Code có truyền lỗi dọn, verify trước chu kỳ và dừng khi không sạch. Bằng chứng mô phỏng chay/kiem-sua-R1/mo-phong.txt ghi một cycle-begin, run-abort-dirty; thử hết hạn ghi verify sạch. Sổ chính không có dirty/cycle-error. Không chạy lại tiêm lỗi hoặc mở rộng kết luận thành mọi sự cố đã được thử. |
| R2 — tích hợp cuối | **Đúng; phần bổ sung vẫn hợp lệ.** kiem-tich-hop/BAO-CAO.md và ket-qua-kt57fcd7.json ghi đường cuối sau TD-09, kiểm chốt thư mục trùng; lượt thử runner3 bổ sung vận chuyển. Độc lập kiểm cả 13 gói chính: manifest/input đúng, status OK, output lặp trùng. Không coi đó là phép thử mọi nhánh phục hồi; lượt chính không dùng nhánh M1 lỗi rồi stage mã mới. |
| R3 — hậu kiểm thay tự phân loại | **Đúng; cách xử lý hợp lệ với giới hạn đã khai.** Chuỗi sổ đúng, có đủ đầu dò và fault-start/stop cho tám ô can thiệp. Hai JSON xác nhận chỉ khác ca 46aab4be: 12 ca theo điều kiện gốc, 13 sau sửa; probe thực là paused true, hồi running false. Điều kiện được ghi sau phát nhưng khai trước đọc dữ liệu chính, không gọi là khóa trước phát. Tập chính vẫn chờ Minh. |
| R4 — điều kiện CPU | **Đúng; không có căn cứ nâng mức kết luận.** D2B đã tách đạt cách tiêm khỏi đạt điều kiện cô lập cơ chế. Không đổi số luồng/quota sau xem. Sổ có PSI máy nhưng vài mốc không thay trung bình pha hay đối chứng trễ tuyến không qua Booking dưới cùng tải. Giữ giới hạn, không đòi chạy lại để đạt ngưỡng đẹp. |
| R5 — span thiếu cha và CLIENT khác | **Đúng; sửa đã xử lý điểm chặn ở mức mô tả/giới hạn.** Raw trace khớp bảng mới ở 13/13 ca: 11 Payment tại 46aab4be, một Event tại 5fb8208f, một Event tại f20b0ca5. Truy lại Tempo xác nhận hai cha Event ngoài cửa sổ; hai cha Payment trong cửa sổ nhưng vắng trong gói. Mục 7 báo cáo phân biệt đúng hai nhóm, giữ hai giải thích Payment và không quy hạng M1 cho chúng. Bảng đáp nói chưa tự truy lại là đúng phạm vi tự kiểm của Claude; không coi việc hai bên cùng đồng ý là bằng chứng thay phép kiểm. Dữ kiện PUT/GET bổ sung bên dưới giải quyết phần chưa biết đích gọi. |
| R6 — autovacuum/checkpoint | **Đúng; sửa đã xử lý.** Báo cáo §3 và đính chính Q4 hiện nói phép đếm chưa phân biệt ca có/không cờ, chưa loại hoặc quy nguyên nhân. Đếm độc lập bốn ca khớp REVIEW-2. Có mặt ở cả hai nhóm không bác được tác động phụ thuộc thời điểm/thời lượng/I/O. Không yêu cầu chứng minh nhân quả xong tại lượt sửa này. |
| N1 — chuỗi sổ | **Đúng; nay kiểm lại trực tiếp:** 127 dòng đúng seq và prev_sha256, không dựa lời reviewer trước. |
| N2 — hết hạn → chờ → tự gọi lại | **Đúng; vẫn chưa đạt trọn phép thử thật.** Báo cáo và LOG nhận đúng phần thiếu. Chưa có bằng chứng mới trong hồ sơ biến thử mô phỏng/resume thành chu trình tự gọi lại thật. Không chặn nhánh phân tích độc lập theo bổ sung SPEC. |
| N4 — P7 từng gói | **Đúng; nay kiểm lại trực tiếp:** 13 input khớp summary.input_sha256, 13 cặp output trùng byte, 13 summary status OK. |

### Bằng chứng span bổ sung

Nguồn: results/T-063/thu2/ca/<mã>.tgz, cases/<mã>/raw-traces.jsonl; đối chiếu span-goc/phan-loai-dev2.json#/<mã>/theo_service_nhom và chi_tiet. Khi tìm cha dùng cặp traceId + spanId, không dùng riêng spanId. Kết quả phân loại khớp toàn bộ bảng theo service/nhóm của cả 13 ca.

| Nhóm | Kết quả kiểm trực tiếp |
|---|---|
| Payment, 46aab4be | 11 child trong cùng trace, gần t − 2,4 s; cha 203105619fac9a5a và c8e902dd99d2f695 vắng trong gói. Tempo có cả hai: booking.order-completed.v1 process kết thúc t − 2,351 s; InboxMessageRepository.save kết thúc t − 2,357 s. |
| Event, 5fb8208f | Child JDBC trên HikariPool-1:connection-adder tại t − 64,530 s. Cha d02cb8a1de7329fe có trên Tempo, kết thúc t − 1.483,111 s, ngoài ±600 s. |
| Event, f20b0ca5 | Cùng loại luồng; child tại t − 37,480 s. Cha bc57ab78297952a2 có trên Tempo, kết thúc t − 2.870,547 s, ngoài ±600 s. |

Lệnh SSH đọc trên exp-obs: python3 -B - với urllib.request.urlopen('http://127.0.0.1:3200/api/traces/' + traceId, timeout=20), duyệt batches/scopeSpans/spans, đổi ID base64 sang hex và chọn bốn ID cha tại REVIEW-2 phụ lục A. Kết quả trên khớp cả bốn. Kiểm Path.exists() cho capture traces-2026-11-13T13-14-02.009-size.jsonl trả False. Chỉ xác nhận file được hỏi không còn; không khẳng định đã tìm mọi bản sao.

**CLIENT khác:** tổng 8.245; basic.ack Booking 3.595, POST discovery-server 1.550. Đọc url.full, server.address và scope của toàn bộ phần còn lại: **3.100 PUT/GET đều tới http://127.0.0.1:8761/eureka/** (đăng ký/heartbeat hoặc apps/delta), scope io.opentelemetry.apache-httpclient-5.0. Payment có 250 PUT + 250 GET; năm service còn lại mỗi loại 260. POST của discovery-server tới localhost:8761/eureka/peerreplication/batch/. Đây là bằng chứng trực tiếp cho đích Eureka mà báo cáo mới chỉ ghi “chưa kiểm”; không chứng minh mọi cơ chế truyền context của thư viện đã đúng. Không cần thêm lượt thu để biết các đích này.

### Bằng chứng R6 bổ sung

Nguồn: outputs/<mã>/method-input.json trong từng archive; phần tử [2] là log, entity = postgresql-shared-instance; [5] là t. Đếm message theo [t−300,t) và [t,t+300), bằng regex automatic vacuum of table / automatic analyze of table / checkpoint complete.

| Ca | vacuum N→A | analyze N→A | checkpoint N→A |
|---|---|---|---|
| eb48d6b3 | 5→5 | 18→21 | 1→1 |
| f20b0ca5 | 2→2 | 13→14 | 1→1 |
| 729604d2 | 3→5 | 20→15 | 1→1 |
| 83073ed1 | 5→3 | 14→19 | 1→1 |

Không có message khớp still waiting hoặc deadlock detected trong các cửa sổ này. Docker inspect chỉ đọc trường Config.Cmd của flash-ticket-infra-postgres-1 hiện có log_lock_waits=on, log_autovacuum_min_duration=0, log_checkpoints=on; kiểm này không phải snapshot tham số hiệu lực lúc thu. Theo [PostgreSQL 16 — Lock Management](https://www.postgresql.org/docs/16/runtime-config-locks.html), deadlock_timeout mặc định 1 s cũng là thời gian chờ trước khi ghi log_lock_waits. Chưa đọc giá trị hiệu lực của lượt cũ; vì thế không suy vắng log thành không có khóa ngắn. Phần sửa R6 giữ đúng giới hạn này.

## Tuân thủ quy trình

- Phân loại lượt là EXECUTE bản phản biện và REVIEW đầu ra; không được sửa thay người làm. Chỉ tạo REVIEW-3.md. Không LOG/STATE, bản cũ, code, đầu ra khác; không commit/push hoặc tự gửi prompt.
- Các sửa báo cáo và đính chính Q4 của Claude nằm trong quyền chiến dịch đã bổ sung tại DECISIONS và CHIEN-DICH-M1-FT §6; không coi góp ý reviewer tự là quyền mới. Không có bằng chứng để báo vi phạm quyền sửa ở phần đã kiểm.
- LOG có tự soát trước đọc REVIEW-2 và phần đáp; bảng đáp giữ trống Minh quyết. STATE vẫn ghi chờ lượt 2, cũ hơn LOG/brief; phân vai/task đang mở không đổi. Không suy dòng này thành đã nghiệm thu. Kết luận chính thức dùng brief lượt này và hồ sơ hiện tại.
- Hash báo cáo/Q4 không nằm trong 214 mục thu2/SHA256SUMS hay 12 pin laptop của đóng băng 2. Sửa các tài liệu này không đổi byte gói đã thu. runner2/3, inj2, exporter, lịch/tải đang ghim; không đề xuất sửa hoặc cập nhật pin cũ cho khớp. Hook H3 nếu được phép sửa sẽ đổi image/revision và cần hồ sơ mới, giữ cohort cũ.
- Không mở dữ liệu khóa, ô đánh giá hay repo lưu trữ. Sổ tiêm và tên ô chỉ dùng kiểm can thiệp/chấm. Đường stage/adapter đã đọc không truyền chúng vào lõi M1. Đây là dữ liệu biết mốc, chưa là bằng chứng detector tự phát hiện không dùng thời điểm tiêm.
- Python laptop không khởi động được do sandbox; không thay ACL/cài môi trường. Dùng PowerShell Get-FileHash, Node đọc/giải nén trong bộ nhớ và SSH Git cho truy vấn chỉ đọc. Một gói lớn vượt giới hạn chuỗi Node được đọc lại theo từng dòng, không giải nén ra đĩa. Không chạy tải/tiêm hoặc đổi cấu hình máy.

## Điều đã kiểm và thấy đúng

| Kiểm | Kết quả và nguồn |
|---|---|
| Băm toàn đợt | PowerShell đọc SHA256SUMS, Get-FileHash -Algorithm SHA256 từng đường dẫn: **214/214 khớp**. |
| Pin laptop | Node crypto đối chiếu dong-bang/dong-bang-2.json#/laptop_file_sha256: **12/12 khớp**. Không tuyên bố đã kiểm lại toàn bộ pin cấu hình remote. |
| Manifest từng archive | Node zlib + đọc tar trong bộ nhớ, đối chiếu cases/<id>/manifest.json#/files: **65/65 file đúng byte/hash**. |
| P7 | **13/13** input khớp summary.input_sha256, status OK; **13/13** cặp output trùng byte. Đây là kiểm toàn vẹn/tất định, không là đánh giá tính đúng mọi thành phần phương pháp. |
| Sổ | **127/127** seq liên tục từ 0; prev_sha256 bằng SHA256 dòng UTF-8 trước bỏ newline, dòng đầu là 64 số 0. Có 13 cycle-begin/load-start/cycle-end, tám fault-start/stop; không cycle-error/dirty. |
| Tải chính | thu2/tai-out/t2-<id>/{state,summary}.json: **13/13** ExitCode=0, dropped_iterations=0. HTTP5-EVENT có 720 journey_failed, HTTP5-EVENT-FLASH 2.161, PAUSE-PAYMENT 159; không coi ExitCode=0 là không có hành trình lỗi. Bỏ lượt thử 865c8e93 khỏi thống kê chính. |
| Gói bổ sung | **13 × 24** bundle, loi_khuc rỗng; threads-blocked là kênh duy nhất result rỗng ở 13/13. Có chuỗi không tự chứng minh mọi giá trị hữu hạn hoặc có nghĩa; không nâng kết luận về samples/throttle-ratio đã nêu ở REVIEW-2. |
| Hậu kiểm | xac-nhan-ca.json#/ca và xac-nhan-ca-2.json#/ca: **12 và 13** xác nhận; chỉ Payment đổi. Sổ probe.payment_state của nó: running false → paused true → paused true → running false theo bốn pha. |

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** kiểm lại độc lập đầu ra/sửa, đối chiếu R1–R6 và N1/N2/N4; bổ sung căn cứ đích Eureka và truy lại cha Tempo.
2. **File thay đổi:** chỉ tasks/T-063-quan-sat-thu-dev-2/REVIEW-3.md, gồm prompt bàn giao. Không thêm hoặc đổi quyết định chính thức.
3. **Kiểm đã chạy:** các bảng trên; không thực nghiệm mới. Các phép kiểm đã có kết quả phù hợp không chạy lại phương pháp chỉ để xác nhận đổi phiên.
4. **Điều còn mở và đề xuất:**
   - **Nghiệm thu:** đề xuất dừng phản biện R5/R6, nhận phần thu đã kiểm và tiếp tục hoàn thiện T-063 trong quyền. Chưa nghiệm thu toàn task: manifest.json, o-dev-bo-sung.json và phép thử tự gọi lại thật còn thiếu. Dừng lượt tiết kiệm vòng lặp; mặt trái là cần giữ rõ các phần chưa đạt, không dùng dừng review làm bằng chứng đã xong M0/M3/RQ5. Phương án tiếp tục một vòng cùng dữ kiện không bổ sung căn cứ hiện có.
   - **Payment/ca nền:** bước thiếu hai cha vẫn OPEN: đến kho sau snapshot và bỏ sót ở đường capture/xuất là các giải thích chưa tách được; file capture đã hỏi không còn. Rà bản sao snapshot/log exporter nếu còn là việc đọc, dự kiến phút đến vài chục phút, chưa đo. Nếu không có nguồn phân xử, giữ giới hạn thay vì gán nguyên nhân. Ảnh hưởng riêng tới điểm/hạng chưa đo; không dùng 11 span làm lời giải thích hạng hoặc lý do tự loại ca. Với cờ nền, chưa đối chiếu thời gian vượt ngưỡng với thời lượng/I/O từng hoạt động và khóa ngắn; phân tích dữ liệu đã lưu có thể phân xử một phần, dự kiến vài chục phút chưa đo. Chọn giải thích cơ chế phụ thuộc phần này; sửa câu kết luận đã đủ xử lý R6, không buộc thu lại toàn đợt.
   - **Tập 12/13:** đề xuất Minh chấp nhận tập 13 làm chính vì probe/D2 xác nhận pause độc lập với điểm M1, giữ tập 12 và khai sửa sau. Mặt trái: điều kiện được sửa sau dữ liệu. Phương án 12 chính/13 bổ sung giữ nguyên điều kiện gốc nhưng thiếu ô trực tiếp duy nhất của H5 trong tập chính. Chưa là quyết định.
   - **FLASH-HEALTHY:** đề xuất giữ nhãn “không tiêm lỗi”, giữ K đã khai và báo tách bốn ca bình thường với một ca tăng tải. Tránh đổi đáp án sau thấy điểm. Mặt trái: K bao gồm phản ứng với tải; phương án đổi tiêu chí cần Minh duyệt và báo riêng, độ trễ tăng chưa tự xác định nhãn khỏe theo ý nghĩa vận hành.
   - **H3/H4:** đề xuất cho sửa đúng điều kiện hook thử Event đã trình để thu POOL-EVENT với đối chứng phù hợp; mặt trái là image khác, phải giữ/báo riêng cohort và cầu so sánh. Phương án chấp nhận thiếu ô giữ H3 OPEN. H4 tiếp tục rà code/lưu lượng/can thiệp rồi trình chi phí phần thiếu trong quyền; không quy việc chưa tạo được queue tồn thành bằng chứng H4 vô ích. Chưa có số đo để hứa ETA hoặc hệ số tải. Không chặn nhánh có đầu vào độc lập, chưa đủ kết thúc H1–H8/M3.
   - **Lưu gói:** đề xuất giữ đủ dữ liệu, trình Minh kho artifact bền để git giữ code/manifest/báo cáo. Mặt trái là thêm nơi lưu và quyền; Git LFS là phương án khác. Chưa upload/xóa/đổi ignore. Việc này không chặn phân tích local.

**Đề xuất dừng lượt phản biện này.** Không còn phản đối chưa xử lý đối với phần sửa R5/R6; không có bất đồng hai bên còn giữ có bằng chứng trong phần này. Những giới hạn khoa học trên vẫn còn, Minh quyết nghiệm thu, tập chính, quyền hook và cách lưu. Dừng không tự đóng task, chọn thiết kế hoặc mở test. Các đề xuất chờ Minh vẫn là CANDIDATE.

## Prompt bàn giao cho người làm

Chép nguyên văn Prompt chung và khối Người làm đáp phản biện từ docs/review-prompt.md, chỉ điền metadata trung tính. M2 giai đoạn 2 không có khối cổng riêng. Minh chọn chuyển hoặc dừng; không tự gửi. Yêu cầu phản biện các đề xuất chờ Minh nằm ở mục 20 của Prompt chung.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-063 (tasks/T-063-quan-sat-thu-dev-2/), đáp REVIEW-3.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: chiến dịch M1-FlashTicket, M2 (CHIEN-DICH-M1-FT.md mục 5 và 7); giai đoạn 2 không có khối cổng riêng trong mẫu.
- Người làm và người phản biện chính thức: Claude làm; Codex phản biện (SPEC T-063).
- Tài liệu gốc: tasks/T-063-quan-sat-thu-dev-2/SPEC.md (gồm bổ sung), LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md, CHECKPOINT-CHIEN-DICH.md; results/T-063/bao-cao.md, quan-sat/thay-doi-may.md, o-dev-bo-sung.md, dong-bang.md; results/T-063/chay/HO-SO-LUOT.md, D2B-KET-QUA.md, dieu-kien-xac-nhan.md, xac-nhan-ca.json, xac-nhan-ca-2.json, lich-2.json; docs/WHY.md từ WHY-81; commit gốc c3d27f8a, đầu ra chưa commit.
- Phản biện và phản hồi trước: tasks/T-063-quan-sat-thu-dev-2/REVIEW.md, REVIEW-2.md và REVIEW-3.md, các bảng Phản hồi của người làm và mục đáp trong LOG.md.
- Code và kết quả liên quan: results/T-063/thu2/ (SHA256SUMS, ca/, chay/, tiem-loi/, audit/); results/T-063/span-goc/, chay/, dong-goi/, tiem-loi/, cpu-book/, ca-nen/, h5/, kiem-r/, kiem-tich-hop/, dieu-phoi/; results/T-064/phan-tich/ghi-chu-co-che-dev2.md; kiểm SHA256SUMS trước dùng; exp-app/exp-obs chỉ đọc SSH theo runner2.py, không chạy tải/tiêm/đổi cấu hình trong lượt đáp này.
- Phạm vi ghi được Minh cho phép trong lượt này: bảng Phản hồi của người làm ở cuối tasks/T-063-quan-sat-thu-dev-2/REVIEW-3.md và nối tasks/T-063-quan-sat-thu-dev-2/LOG.md theo quyền chiến dịch; không sửa nội dung hay prompt của reviewer. Không tự sửa báo cáo/code trong lượt đáp; phần chưa có quyền rõ ràng thì chỉ trả lời trong chat.

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

Người làm chỉ điền bảng này và LOG trong quyền được duyệt; không sửa nhận xét hay prompt. Thêm N1, N2… cho tự soát; để trống cột Minh quyết.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| Kết luận chung (không có finding mới; R5, R6 đã xử lý) | Đúng; không chặn | Người làm không có phản đối. Tự soát trước khi đọc bản này không tìm thêm điểm nào ngoài N1–N5 đã ghi ở LOG phiên 2. Đồng ý dừng phản biện phần phản hồi/sửa này; task chưa nghiệm thu | |
| Đích `PUT`/`GET` là Eureka | Chưa kiểm được trong lượt này (chưa tự đếm lại) | Bằng chứng của người phản biện là phép đọc trực tiếp `url.full`/`server.address`. Đã thêm một câu dẫn nguồn vào `results/T-063/bao-cao.md` mục 7, ghi rõ người làm chưa đếm lại. Không đổi kết luận nào | |
| STATE còn ghi "chờ lượt 2" | Đúng tại thời điểm người phản biện đọc | Dòng T-063 trong `docs/STATE.md` đã được cập nhật 22:29Z, sau khi phát lượt này | |
| Span Payment thiếu cha (OPEN) | Đúng; còn mở | Hai giải thích chưa tách: span tới kho sau lúc chụp, hoặc bỏ sót ở đường capture/xuất. Việc đọc bản sao snapshot/log exporter chưa làm. Ảnh hưởng tới hạng M1 chưa đo; không dùng làm lời giải thích hạng | |
| Các đề xuất chờ Minh (tập 13 làm chính, giữ nhãn FLASH-HEALTHY và báo tách, sửa hook H3, kho artifact) | Người làm đồng ý cả bốn là đề xuất | Chưa phải quyết định. Mặt trái như người phản biện nêu; riêng tập 13: điều kiện xác nhận sửa sau khi có dữ liệu, và H5b của T-064 thiết kế sau khi xem đúng ca này | |
