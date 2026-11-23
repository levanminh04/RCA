# Claude: kế hoạch bản 2 (trình lại, không đợi đêm)

> Nguyên văn, trích bằng script từ `debcb98c-9a36-447f-b07c-8820bd290ab4.jsonl` (dòng 970). Không biên tập.

## Trả lời các câu hỏi

**"Đầu đêm và cuối đêm không cùng điều kiện" nghĩa là gì?** Mỗi giờ tải ×1 thêm khoảng 1.300 đơn vào DB (đo ở T-069: 648 đơn mỗi 30 phút). Đơn đã xong, đã hủy hay hết hạn đều nằm lại trong bảng, vé đã phát cũng vậy. Có hai worker chạy nền liên tục và quét toàn bộ các bảng này:
- **Booking `OrderExpiryWorker`:** chạy mỗi 5 giây, tìm đơn hết hạn. `EXPLAIN` cho thấy câu này quét tuần tự cả `tbl_orders`.
- **Ticket `TicketJobs`:** chạy mỗi 1 giây, đếm và lấy việc giao vé. Nó quét tuần tự `tbl_ticket_deliveries` và `tbl_issuances`; tới nay đã có ~7 triệu lượt quét, đọc ~93 tỉ dòng.

Bảng càng lớn thì hai câu này càng chậm và PostgreSQL càng tốn CPU. Vì vậy, chạy tải 12 giờ liền thì giờ thứ 12 có DB lớn hơn khoảng 40% so với giờ đầu, nền "nặng" dần lên. Ngưỡng chọn ở đầu lượt có thể bị vượt ở cuối lượt chỉ vì trôi, không phải vì có lỗi.

**"Trước mỗi đêm nền", có mấy đêm?** Kế hoạch §8.2 cho W4 hai khoảng nền: khoảng 1 để chọn ngưỡng, khoảng 2 để đo báo động giả trên dữ liệu chưa dùng khi chọn. Chữ "đêm" chỉ là cách gọi cũ. **Minh nói đúng: mọi thứ chạy trên server, nên không cần đợi đêm**, chạy ngay ban ngày được. Hai khoảng có thể là hai nửa của một lượt liên tục.

**Có nên thử tải tối đa (hệ thống chịu được bao nhiêu)?** Tôi đề xuất **có, nhưng dạng ngắn và đặt sau khoảng nền**, không nằm trên đường găng. Lý do:
- Ở T-069, mức ×3 đã làm áp lực CPU máy lên 27–30%, trên máy chỉ có 2 vCPU. Biết hệ thống bão hòa ở đâu giúp chọn mức tải cho nền và W7, để không vô tình đo hệ thống quá tải thay vì đo lỗi.
- Đây cũng là dữ liệu cho NV1 (đánh giá hiệu năng), hiện chưa ai phụ trách.

Mặt trái:
- Tải cao làm DB phình nhanh, nên cần chụp DB trước và khôi phục sau.
- Có thể làm sập service (hết bộ nhớ).
- Bộ tải chỉ có 20 phiên người mua cố định, nên ở mức cao có thể vướng giới hạn của tài khoản thay vì giới hạn hệ thống. Phải kiểm điều này khi soạn SPEC.

Cách làm đề xuất: tăng bậc ×1, ×2, ×3, ×4, ×6, mỗi bậc 10 phút, tổng khoảng 1 giờ; dừng ở bậc đầu tiên có lỗi hệ thống hoặc p95 vượt mức khai trước.

## Kế hoạch trình lại (bắt đầu ngay, ~02:00Z = 9h sáng 20/11)

**Bước 0 — Minh quyết ngay (~15 phút):**
1. Dời mốc ngày sự kiện ở `ticket_db`/`payment_db` thêm +14 ngày, cùng cách đã làm ở T-069. Hạn chót là 22:16Z hôm nay.
2. Chụp dump DB hiện tại làm **mốc tham chiếu** cho mọi lượt dài sau này (W4, kiểm W5, thử tải, W7).
3. Hồ sơ tải cho nền:
   - (a) chỉ ×1 đều;
   - (b) ×1 có thêm vài đợt flash ×3 hợp lệ. **Tôi đề xuất (b)**, vì W7 có ô FLASH; nếu luật chưa từng gặp flash hợp lệ thì sẽ báo nhầm ở các ô đó.
4. Có làm thử tải tối đa không.
5. Commit T-069 và gửi Codex hai prompt: soát kết quả T-069, và soát kế hoạch này (dưới).

**Bước 1 — phiên A, hạ tầng (~30–45 phút):** dời mốc, dump DB, soạn SPEC đo nền, kiểm bộ tải chạy được nhiều giờ. Bộ tải mới chỉ được kiểm tới 1 giờ ở T-067; chưa biết token Keycloak có hết hạn trong lượt 12 giờ không. Nếu không chạy liền được thì nối nhiều lượt 1 giờ.

**Bước 2 — exp-app, nền liên tục ~12 giờ (~03:00Z → ~15:00Z):** khai trước hai nửa.
- **Nửa 1 (6 giờ):** chọn ngưỡng.
- **Nửa 2 (6 giờ):** đo báo động giả, luật chạy thật.
- Mỗi giờ ghi số dòng các bảng, CPU PostgreSQL và p95 theo route, để **đo xem trôi có đáng kể với các chỉ số cảnh báo không.**
- Không khôi phục DB giữa hai nửa: hệ thống thật cũng tích dữ liệu theo thời gian, và luật cần chịu được điều đó. Nếu số đo cho thấy trôi làm lệch ngưỡng, sẽ trình lại phương án khôi phục giữa hai nửa (mất ~15 phút bảo trì, cần dừng service).

**Bước 3 — sau khoảng nền:**
- Kiểm W5 từ đầu tới cuối: tiêm một lỗi, Grafana tự hiện kết quả RCA. Cần máy tải rảnh, nên không trùng bước 2.
- Thử tải tối đa nếu duyệt (~1 giờ, khôi phục DB trước và sau).
- Sau đó là W9a.

**Song song ngay từ bây giờ, mỗi việc một phiên và một SPEC:**

| Phiên | Việc | Mốc cần đạt |
|---|---|---|
| A | Hạ tầng (bước 1–2) | Phát nền trước ~03:00Z |
| B (W4) | Viết luật Grafana, khai trước quy tắc gom cảnh báo, script chọn ngưỡng trên dữ liệu đã lưu | Luật sẵn trước khi bắt đầu nửa 2 (~09:00Z); nạp luật vào Grafana không ảnh hưởng ứng dụng |
| C (W5) | Bộ xuất theo cửa sổ bất kỳ, G1 0.3, bộ điều phối webhook, chạy thử trên ca đã có | Thống nhất định dạng webhook với B ngay đầu; không truy vấn Prometheus nặng trong lúc nền chạy (có thể làm Prometheus khởi động lại và mất dữ liệu nền) |
| D (W6) | Thiết kế đánh giá; đưa vào các phát hiện T-069 (kiểm soát DB, điểm yếu chấm z, đóng gói đầu vào không phụ thuộc P7) | Không phụ thuộc |
| E (W8) | LLM | Khi Minh chọn mức P8 |
| F | Quyển, báo nhóm FlashTicket về các truy vấn quét tuần tự, tồn đọng | Không phụ thuộc |

**Phụ thuộc cứng:**
- exp-app và máy tải chỉ phục vụ một lượt: nền, kiểm W5 và thử tải phải xếp nối tiếp nhau.
- Ngưỡng W4 cần dữ liệu nửa 1.
- Kiểm W5 cần cả luật W4 lẫn dịch vụ W5.
- Hạn bán của sự kiện kéo tới 02/12: đủ cho W4, nhưng phải kiểm lại trước W7.

**Nếu mọi thứ suôn sẻ:** W4 xong khoảng 15–16Z hôm nay. W5 xong khi phiên C sẵn sàng, tức là phụ thuộc tốc độ viết code chứ không phụ thuộc máy.

Tôi chưa sửa file nào trong lượt này.

## Prompt cho Codex phản biện kế hoạch (thay bản trước)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: đề xuất thứ tự và song song hóa W4, W5 (cùng W6, W8, quyển, việc tồn đọng) sau T-069, bản 2, đang trong chat; nguyên văn:
  "Bắt đầu ngay ~02:00Z 20/11, không đợi đêm (mọi phần chạy trên server). Bước 0 Minh quyết: dời mốc ngày sự kiện ở ticket_db/payment_db +14 ngày trước 20/11 22:16Z; dump DB hiện tại làm mốc tham chiếu cho mọi lượt dài sau; hồ sơ tải nền (a) ×1 đều hoặc (b) ×1 có vài đợt flash ×3 hợp lệ, người làm đề xuất (b) vì W7 có ô FLASH; có thử tải tối đa không; commit T-069, gửi Codex. Bước 1 phiên A (~30–45 phút): dời mốc, dump, SPEC đo nền, kiểm bộ tải chạy nhiều giờ (mới kiểm tới 1 giờ ở T-067; nếu không thì nối các lượt 1 giờ). Bước 2 exp-app nền liên tục ~12 giờ (~03:00Z–15:00Z), hai nửa khai trước: nửa 1 (6 giờ) chọn ngưỡng, nửa 2 (6 giờ) đo báo động giả với luật chạy thật; mỗi giờ ghi số dòng bảng DB, CPU PostgreSQL, p95 theo route để đo trôi; không khôi phục DB giữa hai nửa, nếu trôi làm lệch ngưỡng thì trình lại phương án khôi phục (~15 phút bảo trì). Lý do đo trôi: tải ×1 tạo ~1.300 đơn/giờ; worker Booking OrderExpiryWorker (mỗi 5 s) và Ticket TicketJobs (mỗi 1 s) quét tuần tự tbl_orders, tbl_ticket_deliveries, tbl_issuances nên chậm dần và PostgreSQL tốn CPU dần (T-069). Bước 3 sau nền: kiểm W5 từ đầu tới cuối (tiêm một lỗi, Grafana tự hiện kết quả), thử tải tối đa nếu duyệt (bậc ×1, ×2, ×3, ×4, ×6, mỗi bậc 10 phút, dừng ở bậc đầu có lỗi hệ thống hoặc p95 vượt mức khai trước, khôi phục DB trước và sau, kiểm giới hạn 20 phiên người mua), rồi W9a. Song song ngay: B W4 viết luật, quy tắc gom, script chọn ngưỡng trên dữ liệu đã lưu, luật sẵn trước nửa 2; C W5 bộ xuất theo cửa sổ bất kỳ, G1 0.3, bộ điều phối webhook, thống nhất định dạng webhook với B, không truy vấn Prometheus nặng khi nền chạy; D W6 thiết kế, đưa phát hiện T-069 (kiểm soát DB, điểm yếu chấm z, đóng gói đầu vào không phụ thuộc P7); E W8 khi Minh chọn mức P8; F quyển, báo nhóm FlashTicket truy vấn quét tuần tự, tồn đọng. Phụ thuộc cứng: exp-app và máy tải một lượt tại một thời điểm (nền, kiểm W5, thử tải nối tiếp); ngưỡng cần dữ liệu nửa 1; kiểm W5 cần luật W4 và dịch vụ W5; hạn bán sự kiện tới 02/12, kiểm lại trước W7. Nền = có tải bình thường không tiêm lỗi; để im không dùng được."
- Công đoạn: soát SPEC.
- Gói/cổng: kế hoạch giai đoạn 2 §8 (W4, W5; liên quan W6, W8, W9a), chuẩn bị G6.
- Người làm và người phản biện chính thức: người soạn đề xuất Claude; người phản biện dự kiến Codex.
- Tài liệu gốc: docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2–8.5; docs/STATE.md; tasks/T-069-v082-ban-ghim/SPEC.md, LOG.md; results/T-069/phan-tich-nguyen-nhan.md, results/T-069/phan-tich/kiem-db.txt, results/T-069/phan-tich/psi.txt, results/T-069/phan-tich/cpu-container-nen.txt, results/T-069/thu/t069-chinh/tai-create-order.json, results/T-069/sua-su-kien/; tasks/T-066-repo-lab-dung-lai-may/LOG.md, tasks/T-067-ban-flashticket-ghim/LOG.md, tasks/T-068-don-grafana/LOG.md.
- Phản biện và phản hồi trước: không có.
- Code và kết quả liên quan: repo lab D:/Project/flashticket-rca-lab commit 407b4f5 (campaigns/runner/, load/controller/, observability/grafana/, faults/); repo FlashTicket D:/Project/flash-ticket-platform revision 36a3725d (services/booking-service OrderExpiryWorker, OrderRepository; services/ticket-service TicketJobs); máy exp-app, exp-obs, máy tải theo inventory/ của repo lab, khóa và cách gọi ở AGENTS.md mục 12 (chỉ đọc nếu Minh cho phép).
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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
```

```text
Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.
```

`docs/review-prompt.md` chưa có khối trọng tâm cho cổng G6, nên prompt không có khối cổng.
