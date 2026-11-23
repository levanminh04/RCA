# Claude: trả lời "prompt Codex, W4/W5 song song, nền" — kế hoạch bản 1

> Nguyên văn, trích bằng script từ `debcb98c-9a36-447f-b07c-8820bd290ab4.jsonl` (dòng 966). Không biên tập.

## 1. Prompt cho Codex của T-069

Có, nằm ở cuối LOG: [LOG.md:303](tasks/T-069-v082-ban-ghim/LOG.md:303), mục "Prompt cho Codex — soát kết quả T-069". Prompt này gồm Prompt chung và khối "Soát kết quả"; Minh chỉ cần điền dòng "Phạm vi ghi". Prompt ở [LOG.md:183](tasks/T-069-v082-ban-ghim/LOG.md:183) là bản soát điểm chặn sự kiện hết hạn bán; việc đó đã xử lý xong, không cần gửi.

## 2. "Nền" có phải là để im không có request?

**Không.** Nền là hệ thống chạy bình thường, có tải thật, chỉ không tiêm lỗi. Để im không dùng được vì:
- Không có request thì không có số liệu lỗi hay p95 theo route. Luật cảnh báo sẽ không bao giờ kêu, nên đo báo động giả ra 0 một cách vô nghĩa, và ngưỡng chọn trên đó không dùng được khi có tải.
- Grafana cũng gần như trống, chỉ còn liveness và metric máy.
- Cảnh báo phải được hiệu chỉnh đúng trong điều kiện sẽ gặp khi demo và đánh giá, tức là khi có người mua vé.

Vì vậy cần bắn tải nhiều giờ, cùng kịch bản hành trình mua vé và cùng mức ×1 như khi tiêm lỗi. Có hai lựa chọn để Minh quyết khi duyệt SPEC W4:
- Có thêm vài đợt flash ×3 hợp lệ trong đêm không, để luật không báo nhầm khi bán vé chớp nhoáng.
- Có thêm một khúc ngắn không tải, để kiểm luật không báo "không có dữ liệu".

**Hệ quả quan trọng từ T-069:** tải ×1 tạo khoảng 1.300 đơn mỗi giờ (đo được 648 đơn mỗi 30 phút). Một đêm 8 giờ thêm khoảng 10.000 đơn, tức bảng đơn tăng ~28%. Các worker quét tuần tự sẽ chậm dần và PostgreSQL tốn CPU dần trong đêm, nên đầu đêm và cuối đêm không cùng điều kiện. Vì vậy trước mỗi đêm nền phải khôi phục DB về một mốc chuẩn, và ghi số dòng các bảng theo giờ.

## 3. Đề xuất: làm W4 và W5, chia song song

**Tài nguyên chỉ dùng được một lượt tại một thời điểm:**
- exp-app: hệ thống được đo.
- Máy tải: chỉ cho một container k6.
- Prometheus trên exp-obs: truy vấn nặng có thể làm nó khởi động lại và mất dữ liệu.

Mọi việc viết code, phân tích hay soạn hồ sơ đều chạy song song được.

**Đường găng (quyết định tổng thời gian):**
1. Minh duyệt: dời mốc ngày ở Ticket và Payment, chọn mốc DB chuẩn. Việc dời mốc nên làm **trước 20/11 22:16Z**, vì sau giờ đó hai service này coi sự kiện đã kết thúc.
2. Dời mốc, chụp dump DB chuẩn, khôi phục.
3. **Đêm nền 1** (chỉ thu dữ liệu, có thể chạy ngay đêm nay). Đêm 1 không cần luật viết xong, vì ngưỡng chọn sau trên dữ liệu đã lưu.
4. Chọn và chốt ngưỡng.
5. Khôi phục DB, nạp luật vào Grafana.
6. **Đêm nền 2** (luật chạy thật, đo báo động giả, webhook thật).
7. Kiểm W5 từ đầu tới cuối (tiêm một lỗi vào ban ngày).
8. W9a (kịch bản demo).

**Song song ngay từ bây giờ, mỗi việc một phiên và một SPEC riêng:**

| Phiên | Việc | Cần exp-app? | Phụ thuộc |
|---|---|---|---|
| A (hạ tầng) | Dời mốc Ticket/Payment, dump DB chuẩn và khôi phục, SPEC đo đêm nền, phát đêm 1 | Có | Minh duyệt mục 1–2 |
| B (W4) | Viết luật `provisioning/alerting`, khai trước quy tắc gom cảnh báo, script chấm lại luật trên dữ liệu đã lưu | Không | Ngưỡng cần dữ liệu đêm 1 |
| C (W5) | Bộ xuất chung theo cửa sổ bất kỳ (gồm R9), hợp đồng G1 0.3 mang t̂, bộ điều phối nhận webhook, chạy thử trên ca đã có | Không | Thống nhất định dạng webhook với B ngay từ đầu; **không chạy truy vấn Prometheus nặng trong khung đêm nền** |
| D (W6) | Thiết kế đánh giá: khóa bản, D14, ma trận ô, baseline; runner W7 đóng gói đầu vào không phụ thuộc đầu ra M1 (lỗi RECREATE-PAY của T-069); đưa vào kiểm soát DB và điểm yếu chấm z | Không | Không |
| E (W8) | LLM tối thiểu | Không | Minh chọn mức P8 |
| F | Viết quyển; báo nhóm FlashTicket về truy vấn quét tuần tự; dọn tồn đọng (Codex T-066/T-068/T-069, commit) | Không | Không |

**Những điểm phụ thuộc dễ bị bỏ sót:**
- Đêm nền và kiểm W5 từ đầu tới cuối không được trùng giờ, vì dùng chung exp-app và máy tải.
- Nạp luật vào Grafana phải làm trước đêm 2, không làm giữa đêm.
- Hạn bán của sự kiện kéo tới 02/12: đủ cho W4, nhưng phải kiểm lại trước W7.
- Kiểm W5 từ đầu tới cuối cần cả luật W4 đang chạy lẫn dịch vụ W5.
- Bước "đo thời gian trên dev rồi khai N phút" của W5 chỉ làm được khi luồng W5 đã chạy.
- Chọn mốc DB ảnh hưởng cả ngưỡng W4 lẫn W6–W7, nên phải chốt một mốc dùng chung.

**Cách rút thêm một ngày:** thu đêm 1 và đêm 2 liên tiếp, rồi chấm luật bằng cách chạy lại trên dữ liệu đã lưu, không chạy luật thật. Mặt trái: mất bằng chứng cảnh báo và webhook chạy thật, và cách chạy lại phải mô phỏng đúng `for:` cùng chu kỳ đánh giá của Grafana. Tôi nghiêng về giữ đêm 2 chạy thật, vì phần lớn thời gian đã được che bởi việc viết luật song song trong đêm 1.

Tôi chưa sửa file nào trong lượt này. Minh duyệt thì tôi soạn SPEC cho phiên A trước, vì phiên A nằm trên đường găng và có hạn 22:16Z.

## 4. Prompt cho Codex phản biện kế hoạch này

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: đề xuất thứ tự và song song hóa W4, W5 (cùng W6, W8, quyển, việc tồn đọng) sau T-069, đang trong chat; nguyên văn:
  "Tài nguyên tuần tự: exp-app (hệ thống được đo), máy tải (một container k6), Prometheus exp-obs (truy vấn nặng có thể làm khởi động lại). Đường găng: (1) Minh duyệt dời mốc ngày sự kiện ở ticket_db/payment_db (+14 ngày, trước 20/11 22:16Z) và mốc DB chuẩn → (2) dời mốc, dump DB chuẩn, khôi phục → (3) đêm nền 1 chỉ thu dữ liệu, tải hành trình mua vé ×1 nhiều giờ (không cần luật viết xong) → (4) chọn và chốt ngưỡng → (5) khôi phục DB, nạp luật Grafana → (6) đêm nền 2 luật chạy thật, đo báo động giả, webhook thật → (7) kiểm W5 từ đầu tới cuối ban ngày → (8) W9a. Song song ngay: phiên A hạ tầng (bước 1–3, 5–6); phiên B W4 viết luật provisioning/alerting, khai trước quy tắc gom, script chấm lại luật trên dữ liệu đã lưu; phiên C W5 bộ xuất chung theo cửa sổ bất kỳ, G1 0.3 mang t̂, bộ điều phối webhook, chạy thử trên ca đã có, không truy vấn Prometheus nặng trong khung đêm nền, thống nhất định dạng webhook với B; phiên D W6 thiết kế (khóa bản, D14, ma trận ô, baseline, runner W7 đóng gói đầu vào không phụ thuộc đầu ra M1, kiểm soát trạng thái DB, điểm yếu chấm z một mẫu max); phiên E W8 khi Minh chọn mức P8; phiên F quyển, báo nhóm FlashTicket truy vấn quét tuần tự, tồn đọng. Nền = có tải bình thường không tiêm lỗi; để im không dùng được. Tải ×1 tạo ~1.300 đơn/giờ nên khôi phục DB về mốc chuẩn trước mỗi đêm và ghi số dòng bảng theo giờ. Phương án rút một ngày: thu hai đêm liên tiếp và chấm luật bằng chạy lại trên dữ liệu đã lưu (mặt trái: mất bằng chứng chạy thật, phải mô phỏng for và chu kỳ đánh giá); người làm nghiêng về giữ đêm 2 chạy thật."
- Công đoạn: soát SPEC.
- Gói/cổng: kế hoạch giai đoạn 2 §8 (W4, W5; liên quan W6, W8, W9a), chuẩn bị G6.
- Người làm và người phản biện chính thức: người soạn đề xuất Claude; người phản biện dự kiến Codex.
- Tài liệu gốc: docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2–8.5; docs/STATE.md; tasks/T-069-v082-ban-ghim/SPEC.md, LOG.md; results/T-069/phan-tich-nguyen-nhan.md, results/T-069/phan-tich/kiem-db.txt, results/T-069/thu/t069-chinh/tai-create-order.json, results/T-069/sua-su-kien/; tasks/T-066-repo-lab-dung-lai-may/LOG.md, tasks/T-067-ban-flashticket-ghim/LOG.md, tasks/T-068-don-grafana/LOG.md.
- Phản biện và phản hồi trước: không có.
- Code và kết quả liên quan: repo lab D:/Project/flashticket-rca-lab commit 407b4f5 (campaigns/runner/, load/controller/, observability/grafana/, faults/); máy exp-app, exp-obs, máy tải theo inventory/ của repo lab, khóa và cách gọi ở AGENTS.md mục 12 (chỉ đọc nếu Minh cho phép).
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
