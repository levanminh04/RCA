**HAI SCRIPT DÙNG ĐƯỢC / CHƯA: CHƯA để xác nhận đủ điều kiện phát pha ghi E6.** `b1c-yen.sh` đạt phần kiểm yên của CX-45 khi người trực truyền số phút không tải đã xác nhận. `b0.sh` đã xử lý các phản ví dụ về tiến trình và crontab của CX-41/41b, nhưng vẫn có thể giấu một timer lạ và cắt mất thông tin quyết định lease còn hiệu lực. Tôi tái hiện được cả hai trên laptop bằng chính `b0.sh`.

### Các điểm ảnh hưởng quyết định phát

| Mức và người xử lý | Bằng chứng | Hậu quả và sửa tối thiểu |
|---|---|---|
| **CHẶN bước 0 · lỗi nhỏ Codex** | Tôi cho `systemctl list-timers` giả trả `night-load.timer night-load.service`, sắp chạy sau một phút. `b0.sh` in `(khong timer khop)`, trả **0**. Dòng 122 chỉ giữ tên khớp `rca\|t06\|t07\|m1\|tai`. Nháp 4 yêu cầu người trực xét **timer lạ**. [Bộ lọc](/D:/RCA-flashticket/results/T-074/e6/v3/b0.sh:121) · [Tiêu chí bước 0](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-4.md:35) | Người trực không thấy lịch sắp chạy dù đã đọc hết stdout. In nguyên danh sách timer trên app và obs, giữ xử lý lỗi `systemctl`. Mặt trái là đầu ra dài hơn. Không cần đặt danh sách timer được phép mới. |
| **CHẶN xác nhận lease từ đầu ra bước 0 · lỗi nhỏ Codex** | Tôi chạy hai đầu vào JSON có cùng UUID, cùng hạn còn 120 giây, lần lượt mang `action=off` và `action=pool.hold`, `value=1`. Kích thước lần lượt 424 và 430 byte. Cả hai lượt trả **0**, phần lease in ra **giống hệt**, thiếu cả `action` lẫn `expiresAt`. `printf '%.300s'` cắt trước hai trường. Mã hook ở `36a3725` đọc JSON tới 16.384 byte và xét hai trường đó. [Chỗ cắt](/D:/RCA-flashticket/results/T-074/e6/v3/b0.sh:116) · [Mã đọc lease](/D:/Project/flash-ticket-platform/services/event-service/src/rca-test/java/com/flashticket/event_service/testing/RcaFaults.java:81) | Với hai đầu vào này, người trực không phân biệt được tắt hook với lease còn hạn. Hai lease trong mốc app cũ ngắn và đọc được, nên chưa có bằng chứng lần đọc cũ đã che một lease hoạt động. Sửa nhỏ nhất là in đầy đủ nội dung đã đọc thành công. |
| **CHẶN dùng nguyên lệnh nháp 6 · cần Claude** | Nháp ghi `bash v3/b0.sh` và `bash v3/b1c-yen.sh`. Lệnh đầu mặc định `app`, chỉ nhánh `obs` mới thu máy tải. Với số đo sạch, lệnh thứ hai thiếu `--phut-khong-tai N` trả **2**. CX-45r nêu đúng cả hai. Hơn nữa, bộ thử cố ý mong mã **0** khi đã in tiến trình cấm hoặc cron lạ. [Nháp 6](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-6.md:24) · [Bộ thử bước 0](/D:/RCA-flashticket/results/T-074/e6/v3/thu-codex/chay-thu.sh) | Trong bản nháp kế tiếp, ghi `bash v3/b0.sh app` trên exp-app, `bash v3/b0.sh obs` trên exp-obs, rồi người trực đối chiếu nội dung. Mỗi lần kiểm yên trước/sau dump, truyền `--phut-khong-tai N` từ mốc thực tế. Giữ ý nghĩa mã 0 của `b0` là **thu thập thành công**. |
| **CHẶN phát DB đầu nếu mốc mua đã trôi · cần Claude** | Tôi cho chính `b1c-yen.sh` đọc `held=0 purchased=41706`, các số bận bằng 0, không tải 10 phút. Kết quả `YEN`, mã **0**, đúng tiêu chí yên. Nhưng SQL thuận B đã ghim đòi `purchased=41705`. `chay.sh kiem CU` đối chiếu `purchased` với **mốc vừa truyền**. Nháp lại cho ghi Event trước khi chạy thử SQL Booking trên DB nháp. [Điều kiện SQL B](/D:/RCA-flashticket/results/T-074/e6/v2/sql/B/thuan-booking.sql:28) · [Phép so với mốc](/D:/RCA-flashticket/results/T-074/e6/v3/chay.sh:167) · [Thứ tự DB](/D:/RCA-flashticket/results/T-074/e6-spec-nhap-6.md:22) | Nếu mốc mới là 41.706 và các điều kiện khác đạt, Event có thể đã ghi trước khi lượt thử Booking phát hiện điều kiện chắc chắn trượt. Chưa có bằng chứng mốc thật đã trôi. Đề nghị Claude ghi ngay ở bước 0 điều kiện phát **SQL B đã khóa**: đối chiếu `purchased` vừa đọc với 41.705 trước DB đầu. Lệch thì dừng trước Event, trình Minh. Giữ nguyên nghĩa `YEN` và SQL B. |

Hai lỗi ở `b0` kế thừa cách hiển thị của v2. Brief yêu cầu giữ các phần còn lại trừ khi chúng có cùng loại lỗi. Ở đây, dữ liệu có trong đầu vào nhưng mất trước khi tới người trực, cùng hậu quả với việc cắt crontab ở dòng 3. Phiên này chỉ có quyền phản biện. Nếu hai bên đồng thuận, hai sửa nhỏ thuộc quy tắc Codex ngày 24/11. `b0.sh`, bộ thử và ghi chú đã ghim trong `thu-codex/SHA256SUMS`. Nháp 6 đã ghim trong `SHA256SUMS-10`. Bản sửa cần giữ các bản và manifest cũ. [Brief CX-45](/D:/RCA-flashticket/results/T-070/codex/CX-45-brief.md) · [Manifest Codex](/D:/RCA-flashticket/results/T-074/e6/v3/thu-codex/SHA256SUMS) · [Manifest Claude](/D:/RCA-flashticket/results/T-074/SHA256SUMS-10)

### Đối chiếu các lượt trước

| Điểm | Đánh giá độc lập |
|---|---|
| **CX-39/39b về số đơn, outbox và bước 0 cũ. CX-41/41b về `GROUP BY`, psql, RabbitMQ và thiếu bảng** | **Đúng với bản cũ. Đã sửa trên đường gọi v3.** SQL nhóm theo `lifecycle_state`. Đầu ra đòi đủ sáu trạng thái, đúng một cặp `held/purchased`, bốn số outbox và ít nhất một hàng đợi đọc được. Trong bộ thử chạy lại, lỗi truy vấn đơn trả 3, lỗi RabbitMQ trả 1 kèm `LOI_THU_THAP`, thiếu bảng Ticket trả 3. Hàng đợi đầu tiên có tin vẫn được tính khi đầu ra không có tiêu đề. [Script kiểm yên](/D:/RCA-flashticket/results/T-074/e6/v3/b1c-yen.sh:21) · [Đầu ra giả lập](/D:/RCA-flashticket/results/T-074/e6/v3/thu-codex/luot-3.out) |
| **CX-41/41b về `k6 --quiet run`, `runner4.py --output /tmp/grep.log`, cron dòng 5, lỗi thu thập** | **Đúng với v2. Đã sửa các phản ví dụ nêu tên.** Hai tiến trình hiện trên app, obs và máy tải giả lập. Cron dòng 5 hiện ở ba máy. Lỗi `ps`, Docker, SSH giả hoặc crontab làm script trả khác 0 và chỉ ra bước lỗi. Tiến trình cấm và cron lạ vẫn cần người trực quyết định từ nội dung. [Bộ thử](/D:/RCA-flashticket/results/T-074/e6/v3/thu-codex/chay-thu.sh) · [Đầu ra ba máy](/D:/RCA-flashticket/results/T-074/e6/v3/thu-codex/luot-3.out:343) |
| **CX-39 #1 về khóa JSON Booking và cam kết so mọi phiên bản** | **Đúng với lỗi gốc, sửa đúng một phần theo nghĩa rộng.** Thuận B hiện so JSONB có xét `NULL`, đếm đúng phần tử vé và dùng `jsonb_set(..., false)`. Điều kiện inventory vẫn chỉ so tập trường ghi trong SQL. Minh đã duyệt giữ nguyên SQL B. [SQL thuận Booking](/D:/RCA-flashticket/results/T-074/e6/v2/sql/B/thuan-booking.sql:15) |
| **CX-39 #2–3 và CX-41b về chạy nghịch tiếp, đảo nhầm, DB lặp, mất log** | **Đúng trên đường cũ.** V2 đã dừng tuần tự ở lỗi đầu trong T07/T08. Quyết định 24/11 bỏ SQL nghịch. V3 giới hạn một DB mỗi lượt ghi, từ chối DB lặp ở `kiem` và có khóa thư mục. Các ca lưu T41–T43 xác nhận nhánh từ chối. Việc phục hồi dump thật thuộc phần Claude. [Bộ chạy v3](/D:/RCA-flashticket/results/T-074/e6/v3/chay.sh:37) · [T41–T43](/D:/RCA-flashticket/results/T-074/e6/v3/thu/chay_thu.out:59) |
| **CX-39 #4, CX-41/41b về kết cục COMMIT và đích B trộn CU/DICH** | **Đúng với v2.** Danh sách đã ghim giữ sức chứa ở `CU`. V3 so đầu/đích theo từng trường và chờ phiên cũ khi kết cục chưa rõ. Các ca T21–T24 đã lưu tách lỗi trước COMMIT, sau COMMIT, thiếu dấu và trạng thái lẫn. Đây là bằng chứng giả lập về đường phục hồi của Claude. [Đích B](/D:/RCA-flashticket/results/T-074/e6/v2/sql/B/truong.txt) · [Phân loại v3](/D:/RCA-flashticket/results/T-074/e6/v3/chay.sh:176) · [Kết quả đã ghim](/D:/RCA-flashticket/results/T-074/e6/v3/thu/chay_thu.out) |
| **CX-39 #5, CX-41/41b về tên trường, `purchased`, thiếu `truong.txt`** | **Đúng với v2.** V3 kiểm manifest và khả năng đọc danh sách trước khi chạy, so tên theo nghĩa đen, đòi đúng số dòng và so `purchased` với mốc. T18–T20 và T31–T37 đã lưu thể hiện các trường hợp từ chối. Mốc vừa đọc khác hằng số trong SQL thuận là vấn đề riêng nêu ở trên. [Đọc danh sách](/D:/RCA-flashticket/results/T-074/e6/v3/chay.sh:63) · [Các ca kiểm](/D:/RCA-flashticket/results/T-074/e6/v3/thu/chay_thu.out) |
| **CX-45r về 36/36, hash, phạm vi ghi và khả năng dùng hai script** | **Đúng** về số ca, hash, các sửa đã giao và lỗi cách gọi trong nháp 6. **Đúng một phần** về khả năng dùng cả hai cho bước phát. Bộ thử cũ không phân biệt được hai cặp đầu vào timer và lease ở trên. Nhật ký thao tác CX-45/CX-45r cho thấy các lần sửa và chuyển hướng đầu ra vào hai script cùng `thu-codex/`. Không thấy bằng chứng Codex ghi sang phần Claude. [Báo cáo CX-45r](/D:/RCA-flashticket/results/T-070/codex/CX-45r-tin-cuoi.md) |

**Outbox tại `36a3725` đúng ở cả bốn dịch vụ.** Tôi đối chiếu DDL, bước thêm tiền tố `tbl_`, ánh xạ dịch vụ và đường ghi mốc gửi. Bốn truy vấn dùng lần lượt `event_schema`, `booking_schema`, `ticket_schema`, `payment_schema`, cùng bảng `tbl_outbox_messages` và điều kiện `published_at IS NULL`. Điều kiện này đếm cả bản tin đang chờ thử lại. DDL Booking xác nhận sáu giá trị `lifecycle_state`. Tài liệu vòng đời tại cùng commit xác nhận `ISSUANCE_FAILED` là trạng thái cuối. [Bốn câu gọi thực](/D:/RCA-flashticket/results/T-074/e6/v3/b1c-yen.sh:52) · [Các đường dẫn DDL và entity](/D:/RCA-flashticket/results/T-074/e6/v3/thu-codex/GHI-CHU.md:7) · [Quy tắc đổi tên bảng](/D:/Project/flash-ticket-platform/services/99-table-prefix.sql:32)

### Báo cáo cuối lượt

1. **Đã làm.** Tự soát nguồn, diff v2→v3, hai script, bộ thử, nháp E6 và mã FlashTicket trước khi đối chiếu các kết luận CX-39/39b, CX-41/41b và CX-45r. Hai script kiểm điều kiện vận hành trước E6. Chúng không nhận nhãn sự cố, tính điểm bất thường hay chọn cơ chế đồ thị. Tôi không thấy lựa chọn phương pháp mới phải ghi WHY trong phần sửa này. Tiêu chí của toàn bộ T-074 và kết quả P9/P10 chưa thể nghiệm thu từ hai script. [SPEC T-074](/D:/RCA-flashticket/tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md) · [MRP P9/P10](/D:/RCA-flashticket/docs/MRP.md:289)
2. **File thay đổi.** Tôi không sửa file nào, không ghi LOG/STATE, không commit. Các ca bổ sung chỉ chạy trong bộ nhớ và in ra stdout. Không SSH, kết nối DB, mở dữ liệu khóa hay dùng agent con.
3. **Kiểm đã chạy.** `bash results/T-074/e6/v3/thu-codex/chay-thu.sh` trả **0**, cả hai `bash -n` đạt, **36/36** ca đạt. `Get-FileHash` khớp **9/9** mục manifest CX-45, **44/44** mục v2 và **7/7** mục manifest phần Claude phiên 10. Đã kiểm hash nguồn E6 cũ và các tệp mốc E1 dùng để đối chiếu. Kết quả của ba phép thử bổ sung nằm ở bảng đầu. Lượt này không chạy lại bộ phục hồi của Claude. [Kết quả gốc để đối chiếu](/D:/RCA-flashticket/results/T-074/e6/v3/thu-codex/luot-3.out:751)
4. **Đề nghị Minh.** **Tiếp tục một lượt đáp hẹp, giữ S5 chưa phát ghi.** Đề nghị Claude phản hồi hai lỗi mất thông tin, sửa cách gọi trong nháp kế tiếp và đặt phép đối chiếu `purchased` trước Event. Sau đồng thuận, Codex có thể sửa nhỏ phần hiển thị và ca hồi quy trên laptop. Cách khác là người trực đọc riêng timer và lease trên máy. Cách đó làm bằng chứng bước 0 nằm ngoài đầu ra `b0.sh`. Chưa cần quyết lại biến thể B. Nếu số mua thật lệch hằng số đã khóa, khi ấy mới cần Minh quyết cách xử lý. Hiện không có số đọc mới trên máy để khẳng định lệch hay khớp. Có thể phân xử ngay trong bước đọc S5 vốn đã dự kiến, trước lần ghi đầu tiên.

### Prompt bàn giao cho Claude

Minh có thể chuyển phần nhận xét trên cùng prompt dưới đây. Mẫu repo có khối G0–G4. Tôi dùng khối G3 cho phần khóa trước đánh giá, theo bàn giao T-074. Cổng của task vẫn là chuẩn bị G6. [Mẫu bàn giao](/D:/RCA-flashticket/docs/review-prompt.md:27)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074 E6, bản sửa CX-45 trong results/T-074/e6/v3/.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P9/P10, W6 → E6, chuẩn bị W7 và G6.
- Người làm và người phản biện chính thức: Claude là người làm T-074, Codex là người phản biện. Phần sửa CX-45 do một phiên Codex thực hiện theo phân công 24/11.
- Tài liệu gốc: tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md và LOG.md; docs/DECISIONS.md phần 24/11; tasks/T-070-dieu-phoi-giai-doan-2/LOG.md và HOP-DONG.md; results/T-074/e6-spec-nhap-3.md, e6-spec-nhap-4.md, e6-spec-nhap-5.md, e6-spec-nhap-6.md; results/T-070/codex/CX-45-brief.md và CX-45r-brief.md.
- Phản biện và phản hồi trước: results/T-070/codex/CX-39-tin-cuoi.md, CX-39b-tin-cuoi.md, CX-41-tin-cuoi.md, CX-41b-tin-cuoi.md, CX-45r-tin-cuoi.md; bản kiểm độc lập CX-45b cùng các đề xuất do Minh chuyển kèm trong chat.
- Code và kết quả liên quan: results/T-074/e6/v2/, results/T-074/e6/v3/, results/T-071/e1/; SHA256SUMS ở v2 và v3/thu-codex, results/T-074/SHA256SUMS-10; D:/Project/flash-ticket-platform tại 36a3725, chỉ đọc. Bộ thử laptop: bash results/T-074/e6/v3/thu-codex/chay-thu.sh.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chỉ đọc trên laptop, không SSH, không dùng subagent.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```