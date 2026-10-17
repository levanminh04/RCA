# Nhật ký T-038

Chỉ nối thêm. Phân biệt quyền tạo tài liệu, duyệt triển khai và quyền tải nguồn.

## Phiên 1 — 15/10/2026 — Codex — LeVanMinh — vai trò: người làm tài liệu đề xuất

**Mở phiên:** đọc AGENTS, STATE, mẫu SPEC/LOG, nguồn DT18/cô, MRP phần chi phối, LESSONS, WHY/DECISIONS và phương án P5b/đầu ra T-036 hiện hành. Chưa có SPEC/LOG T-038 trước lượt ghi. Kiểm hash kết quả T-036 và nguồn registry trước dùng đều khớp; không làm lại phần công cụ đã nghiệm thu.

**Công đoạn/mục tiêu:** tạo SPEC ở trạng thái ĐỀ XUẤT/CHỜ PHẢN BIỆN theo quyền chuẩn bị; Train Ticket: truy revision và độ đủ snapshot nguồn, graph tĩnh/mapping, đối chiếu RE2-TT dev và phân xử chênh lệch. Phục vụ DT18-NV2/NV3, cô bước 1, MRP P5 và đầu vào RQ3/RQ5/P6/P9. Chưa có kết quả khảo sát của task.

**Nguồn quyết định:** Q-159–Q-163 trong docs/DECISIONS.md; nguyên văn quyền chuẩn bị, danh sách chín file và ba bổ sung được lưu tại tasks/T-037-p5b-flashticket/LOG.md Phiên 1. Lượt này chỉ soạn tài liệu, không ghi “Minh đã duyệt triển khai SPEC”.

**Diễn biến:**
- Đối chiếu phạm vi gốc trong LOG T-036 Phiên 1 và bàn giao, giữ nghĩa vụ các nhánh và giới hạn thiết kế/runtime/lợi ích.
- Ghi Q-159–Q-163 và bổ sung WHY-53 trước SPEC/LOG; không gọi các chi tiết đề xuất hoặc dự toán là thiết kế/số đã xác minh.
- Soạn SPEC theo template, nêu câu hỏi/phép phân xử/phần thiếu/tiêu chí, prospective write scope và điều kiện duyệt triển khai.
- Bổ sung kiểm độ đủ nguồn/loại trừ, dự toán chưa đo/tổng mọi run/RAM pilot và pin/song song/STATE tuần tự theo lời Minh.
- Chuẩn bị prompt nguyên văn để Minh chuyển cho Codex phiên sạch soát cả ba SPEC. Các nhánh hỗ trợ đọc/soạn trong lượt này không là lượt phản biện chính thức.
- Sau SPEC/LOG, cập nhật STATE theo bản mới nhất, lần lượt từng dòng T-037/T-038/T-039, trạng thái chờ phản biện; không tạo T-040 hoặc chạy task.

**Quyết định của Minh trong phiên:** quyền tạo tài liệu và ba bổ sung theo Q-159–Q-163; không duyệt triển khai/tải nguồn. Ngoại lệ Codex phiên sạch chỉ cho soát ba SPEC; người làm vẫn Codex, phân công P5 còn lại không tự đổi. Không có lựa chọn phương pháp P6 hoặc xác nhận giả thuyết mới.

**Tự soát:** tách nguồn thiết kế/code, runtime và hiệu quả; không lấy whitelist đuôi file làm bằng chứng inventory đầy đủ, không lấy revision code RCA/tree làm deployment, không đưa nhãn vào builder/comparator. SPEC nêu các đầu vào/nguồn còn OPEN, yêu cầu trình bổ sung và rủi ro vượt một phiên. Đây là tự soát tài liệu, chưa có kết luận phản biện chính thức hoặc kiểm thực nghiệm của task.

**Kết thúc phiên:**
1. Đã tạo SPEC/LOG đề xuất; phạm vi nghiên cứu vẫn đầy đủ như phương án gốc, các nghĩa vụ còn thiếu và quyết định phụ thuộc được giữ rõ. Chưa trả lời xong RQ3/RQ5/P5b hoặc đủ căn cứ khóa G3.
2. Gói ghi đúng chín file Minh duyệt: docs/DECISIONS.md, WHY.md, STATE.md; SPEC.md/LOG.md T-037/T-038/T-039. Mỗi LOG là nhật ký chuẩn bị của chính task; không sửa code, kết quả, T-036 hoặc repo platform.
3. Kiểm chuẩn bị: nguồn/manifests trước dùng khớp; soát mục template, trạng thái/quyền, pin T-036 giống nhau, ba bổ sung, prompt nguyên văn, đường dẫn và phạm vi. Kiểm cuối sau ghi bằng lệnh inline đọc file/hash/diff; kết quả báo trong chat. Không tải, khảo sát ứng dụng, chạy checker/đối chiếu, mở dữ liệu khóa hoặc commit/push.
4. Còn OPEN: revision/tập nguồn/byte cần tải TT/OB, độ đủ snapshot và phần loại trừ, mapping/lineage/runtime, giờ công/máy/RAM/tổng lưu và tính khả thi một phiên. Thiếu đúng bằng chứng/owner/ảnh hưởng ở SPEC; các câu khoa học chưa được soát thực nghiệm trong lượt chuẩn bị. Đề xuất tiếp tục bằng lượt soát SPEC, không tự triển khai hoặc tự mở vòng mới. Nội dung nên vào báo cáo sau có bằng chứng: nguồn mô hình, địa chỉ tín hiệu, độ khớp có điều kiện và giới hạn quan sát.
5. Bước tiếp chính xác: Minh chuyển prompt dưới cho Codex phiên sạch để soát ba SPEC trong repo. Chỉ đọc/trả lời chat; sau phản biện, Minh quyết sửa/tách/duyệt triển khai từng task. Tải cần nguồn/revision/tệp/byte và quyền riêng. Không gọi checker tạo run hoặc mở source mới ở phiên soát SPEC.
6. Lệnh cuối lượt chuẩn bị: py -3 -X utf8 -B - (Python inline kiểm toàn diff/phạm vi chín file, append-only, template/prompt/pin và nguồn bảo vệ, in kết quả trong chat). Lệnh đọc tiếp: Get-Content -LiteralPath 'tasks/T-038-p5b-trainticket/SPEC.md' -Raw.

**Đề xuất commit, chưa thực hiện:** docs: draft P5b specs for FlashTicket, Train Ticket and Online Boutique. Chỉ commit/push khi Minh yêu cầu hoặc duyệt riêng.

## Prompt bàn giao — Codex phiên sạch soát ba SPEC (Minh chuyển thủ công)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: gói ba SPEC T-037/T-038/T-039; D:/RCA-flashticket/tasks/T-037-p5b-flashticket/SPEC.md; D:/RCA-flashticket/tasks/T-038-p5b-trainticket/SPEC.md; D:/RCA-flashticket/tasks/T-039-p5b-online-boutique/SPEC.md.
- Công đoạn: soát SPEC.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm. Claude theo phân công P5; riêng lượt soát ba SPEC này, Codex phiên sạch độc lập phản biện theo ngoại lệ Minh chỉ định. Ngoại lệ chỉ cho công đoạn SPEC, không tự mở rộng sang phản biện kết quả hoặc đổi vai trò khác.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; SPEC.md và LOG.md của ba task nêu trên; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; phương án P5b trong LOG T-036 Phiên 1; nguồn đầu vào được từng SPEC liệt kê.
- Phản biện và phản hồi trước: chưa có REVIEW của ba task. Lịch sử nguồn phụ thuộc ở tasks/T-036-p5b-hop-dong-chung/LOG.md, REVIEW.md và results/T-036/runs/; chỉ đọc kết luận lịch sử sau tự soát phần gốc.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-036/{manifest.json,hop-dong.md,nguon.json,ban-giao.md}; src/do_thi_tinh/README.md và code; snapshot results/T-036/runs/kiem-r1-after-002/code/ và code-hashes.json; results/T-035/manifest.json và nguồn/schema/graph hiện hành được SPEC liệt kê; Windows/PowerShell, Python theo README. Nguồn FlashTicket chỉ đọc ở D:/Project/flash-ticket-platform theo AGENTS và skill bắt buộc.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, SPEC, LOG, STATE, DECISIONS, WHY, code hoặc kết quả; chưa triển khai hoặc tải nguồn. Ba SPEC đang ở trạng thái ĐỀ XUẤT/CHỜ PHẢN BIỆN; quyền chuẩn bị tài liệu không là quyền chạy các bước triển khai.

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

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


### Bổ sung tự kiểm cuối Phiên 1 — 15/10/2026

Kiểm hình thức lần đầu báo ba cờ ở cùng điều kiện chuỗi: harness chỉ tìm “chưa duyệt triển khai/tải nguồn”, trong khi LOG ghi “không duyệt triển khai/tải nguồn”. Đã đọc đối chiếu SPEC/LOG và xác nhận quyền vẫn chỉ chuẩn bị; sửa phép kiểm để nhận cả hai cách diễn đạt, không sửa tài liệu để làm phép kiểm đạt. Kết quả lần kiểm lỗi được giữ bằng mô tả này vì gói chỉ cho chín file, không tạo thư mục run.

Các nhánh hỗ trợ đã đọc nguồn và tự kiểm tài liệu; không là lượt phản biện chính thức. Prompt của lượt chuẩn bị vẫn là khối nguyên văn ở trên. Lệnh kiểm sau cùng tiếp tục chỉ đọc template/prompt/pin/hash/diff và toàn phạm vi chín file; chưa triển khai/tải/commit/push.


## Phiên 2 — 15/10/2026 — Codex — LEVANMINH — vai trò: người làm

**Mở phiên / phân loại:** EXECUTE có điều kiện theo lời giao dưới. Codex người làm; Claude phản biện kết quả. Tự rà không thay phản biện chính thức. Nhãn ĐỀ XUẤT trong SPEC/STATE/LOG trước lời giao là mốc lịch sử, không sửa SPEC. Phạm vi được giao: results/T-038/, nối LOG này và chỉ dòng T-038 trong STATE. Quyền tải nguồn mới còn phải duyệt riêng.

**Nguyên lời giao của Minh:**

```text
Tôi giao bạn triển khai T-038 theo SPEC hiện hành, sau khi tự rà SPEC, kiểm khả năng hoàn thành trong một phiên và trình phần tải nguồn cần duyệt. Tôi đã đồng ý dừng lượt phản biện ba SPEC T-037/T-038/T-039. Đây là quyền triển khai có điều kiện; chưa duyệt tải repository hoặc nguồn mới.

Làm việc tại D:/RCA-flashticket.
Task: tasks/T-038-p5b-trainticket/SPEC.md.
Bạn là Codex người làm. Claude phản biện kết quả. Lượt tự rà không thay phản biện chính thức.

Trước triển khai:
1. Đọc AGENTS.md, docs/STATE.md, toàn bộ SPEC và mục cuối LOG T-038. Đọc trực tiếp DT18, hướng dẫn của cô, MRP phần RQ3/RQ5/P5/P6/P9/G3, LESSONS, WHY/DECISIONS liên quan và phương án P5b gốc trong LOG T-036 Phiên 1.
2. Tự rà từ nguồn như lần đầu. Đọc nguồn/code/đầu ra gốc, lập nhận xét trước khi mở kết luận phản biện hoặc phản hồi cũ. Đọc nguyên văn Prompt chung + Soát SPEC + G3 trong docs/review-prompt.md làm tiêu chí tự rà. Bạn giữ quyền người làm theo lời giao này và SPEC.
3. Kiểm hash các đầu vào cũ theo manifest phù hợp. Pin T-036 là bản được SPEC liệt kê, current_run runs/kiem-r1-after-002; snapshot code ở results/T-036/runs/kiem-r1-after-002/code/, code-hashes.json tại thư mục run. Mã hiện hành phải khớp pin. Không tự đổi phiên bản hoặc cập nhật hash khi nguồn lệch.
4. Đánh giá khả năng xong một phiên cho toàn chuỗi truy nguồn/coverage, lập bản ghi, dựng/đối chiếu, phân tích nhóm chênh lệch, tự kiểm và bàn giao. Tách giờ công, giờ máy, RAM, byte tải và tổng lưu mọi lượt. Chưa đo ghi chưa đo. Nếu quá rộng hoặc chưa thể phân xử tính khả thi, trình cách tách và ảnh hưởng; không giảm kiểm hoặc tự chia task.
5. Ưu tiên trình sớm đề xuất tải nguồn. Bắt đầu từ nguồn RCAEval đã lưu và xác minh hash theo results/T-002/handoff-manifest.json cùng registry T-036. FudanSELab/train-ticket chỉ là repository ứng viên. Phân biệt revision code RCAEval, dataset, ứng dụng, instrumentation, image và deployment; không chọn revision theo mức khớp graph.

Đề xuất tải phải nêu nguồn/URL, revision và mức xác minh, cây snapshot hoặc metadata dùng lập danh sách, từng nhóm tệp/đối tượng, lý do cần, phần loại trừ và ảnh hưởng, byte mạng, dung lượng giải nén/tổng đĩa và đường dẫn lưu. Có thể tra metadata công khai theo quyền chỉ đọc để lập đề xuất; chưa clone, tải snapshot/code hoặc ghi nguồn mới trước khi Minh duyệt. Chưa xác định được revision hay byte thì nói rõ bằng chứng thiếu, không bịa số. data/README.md hoặc nơi ghi ngoài scope phải được duyệt riêng.

Nếu có lỗi cần sửa SPEC, xung đột nguồn/quyền, pin lệch hoặc phạm vi không khả thi: dừng phần phụ thuộc, trình bằng chứng và sửa tối thiểu theo file. Không tự sửa SPEC. Nếu tự rà đạt thì tiếp tục phần triển khai đủ nguồn trong quyền, không xin lại quyền đã có. Chờ duyệt tải chỉ dừng phần cần nguồn đó.

Phạm vi ghi: results/T-038/, nối tasks/T-038-p5b-trainticket/LOG.md và chỉ dòng T-038 trong docs/STATE.md. Ghi nguyên lời giao, ngày/thiết bị/vai trò, kết quả tự rà và kế hoạch khả thi vào LOG. Nhãn ĐỀ XUẤT trong tài liệu là mốc trước lời giao; không tự sửa SPEC. Không ghi REVIEW, DECISIONS, WHY, src/, T-035/T-036 hoặc task khác. Quyết định cần lưu chính thức thì trình nội dung/phạm vi riêng.

Thực hiện đủ SPEC. Kiểm inventory từ toàn cây snapshot được định danh, không chỉ phần tải hoặc service thấy trong trace. Xét config/deployment/build/template/schema/interface/mã sinh/nguồn ngoài có thể chứa quan hệ. Thiếu nguồn cần thiết thì trình bổ sung và giữ kết luận đầy đủ OPEN.

Lập bản ghi/operation/quan hệ/địa chỉ có provenance. Viết oracle độc lập cho biến đổi riêng; dùng T-036 đã ghim. Mapping phải có nguồn, giữ owner/scope; không dùng nhãn hoặc tối ưu tỷ lệ khớp để chọn mapping.

Chọn graph RE2-TT dev hiện hành từ manifest T-035, không gom graph trong runs/. So toàn bộ graph/cửa sổ được giao ở hai mức, gồm full/N/A và các ảnh chụp có sẵn; không dựng cửa sổ mới hoặc đọc lại trace thô. Báo endpoints/typed riêng, unknown, unmapped/ambiguous/unverified, members/exclusions, giao/phần riêng và mẫu số N/A.

Lần theo nhóm chênh lệch quan trọng và match tương ứng. Xét revision, alias, miền/cửa sổ, nhánh chưa chạy, nguồn tĩnh thiếu, telemetry thiếu và lỗi chuyển đổi. Thiếu chuỗi revision thì kết quả phải ghi đối chiếu tham khảo có điều kiện; không tự quy mismatch cho instrumentation.

T-037/T-039 chạy song song, dùng chung pin T-036. Cần đổi hợp đồng chung thì dừng phần phụ thuộc và trình ảnh hưởng cả ba nhánh; không tự sửa hoặc fork nghĩa chung. STATE cập nhật tuần tự, đọc bản mới nhất trước sửa đúng dòng task; không bảo đảm được thì trình dòng cần cập nhật cho Minh điều phối. Không đo chi phí cùng việc nặng khác hoặc dừng tiến trình phiên khác. Thao tác tốn kém theo AGENTS cần báo trước và chờ duyệt.

Giữ mọi lượt lỗi/lặp, trung gian, lệnh và môi trường. Không mở test/heldout/raw telemetry/archive, chạy baseline/RCA, chọn P6, làm T-040, bật EC2, commit/push hoặc tự mở/gửi chat.

Cuối phiên kiểm diff/phạm vi/manifest và mức trả lời mục tiêu nguồn. Nối LOG đủ báo cáo, OPEN, bước tiếp/lệnh cuối; cập nhật đúng dòng STATE. Soạn prompt Claude nguyên văn Prompt chung + Soát kết quả + G3 hiện hành; nếu bị chặn vì cần sửa SPEC thì dùng Soát SPEC. Minh chuyển thủ công. Không tự nghiệm thu hoặc đóng task/G3.
```

**Diễn biến đầu phiên:** đọc AGENTS, STATE, toàn SPEC/LOG T-038; nguồn DT18/cô, MRP RQ3/RQ5/P5/P6/P9/G3, LESSONS, WHY-52/53, DECISIONS liên quan và phương án P5b gốc LOG T-036 Phiên 1. Dùng Prompt chung + Soát SPEC + G3 nguyên văn để tự rà. Chưa mở kết luận REVIEW/phản hồi cũ; các kiểm cơ học đọc pin/manifest/selector do hai nhánh hỗ trợ người làm thực hiện chỉ đọc, không là phản biện hay chat độc lập.

**Đã kiểm:** pin T-036 hiện hành khớp, 187 artifacts và code snapshot khớp. Nguồn công khai RCAEval đã lưu khớp T-002/registry. Selector root T-035 cho 1.069 graph RE2-TT dev; không gom runs. Kết quả máy lưu runs/kiem-dau-vao-002/input-verification.json. Lượt 001 lỗi đường dẫn snapshot do runner dùng cấu trúc thư mục thay tên file; không phải pin lệch. Giữ script và kết quả lỗi ở runs/kiem-dau-vao-001/. Đã sửa runner trong phạm vi rồi chạy tên mới.

**Sự cố truy metadata:** hai URL GitHub /commits/<sha> trả kèm patch (response lần lượt 894830 và 29131 byte), dù phần trích ra chỉ là commit/date/tree/message. Không lưu body/patch và không dùng patch làm bằng chứng nguồn; đã báo Minh trong chat. Từ đây chỉ dùng /git/commits/<sha> và /git/trees/<sha> cho metadata. Chưa clone, lấy snapshot ứng dụng, cài gói hay ghi nguồn mới. Các metadata công khai khác chỉ tra trong bộ nhớ để lập đề xuất.

**Còn đang làm:** lập nhận xét tự rà độc lập và đề xuất nguồn/tính khả thi toàn chuỗi. Chưa dựng inventory/graph tĩnh/mapping hoặc đối chiếu vì chưa có nguồn ứng dụng trong quyền; chưa xác minh application/instrumentation/image/deployment sinh RE2-TT.


### Tự rà độc lập, truy nguồn và kết thúc Phiên 2 — 16/10/2026

Nhận xét độc lập đã ghi `results/T-038/tu-ra-spec.md` trước khi mở REVIEW và mốc đóng T-036. Sau đối chiếu, không thấy phụ thuộc mới yêu cầu đổi pin/hợp đồng; không mở lại task đã đóng. Lượt này không đọc kết luận phản biện T-038 cũ; trên đĩa chưa có REVIEW T-038. Việc Minh đã dừng soát ba SPEC không thay tự rà hay phản biện kết quả.

**Kết quả tự rà:** phạm vi mô hình/đối chiếu phù hợp DT18/cô/MRP và WHY-52/53. Chưa có lỗi cần sửa nghĩa hợp đồng. Tuy nhiên, chưa phân xử được tính khả thi toàn chuỗi trong một phiên, nên dừng phần triển khai phụ thuộc đó và trình tách; không báo tự rà đạt toàn điều kiện. Đề xuất đầy đủ ở `results/T-038/de-xuat-nguon-va-tach.md`; chưa sửa SPEC.

**Truy nguồn:** nguồn RCAEval đã lưu có paper dẫn repository không ghim app revision. Tách code RCAEval, dataset, ứng dụng, instrumentation, image và deployment trong `nguon.json`. Chuỗi ứng dụng–dataset còn OPEN. Metadata v1.0.0 được khảo sát để lập một gói nguồn tham khảo CANDIDATE, chưa chọn/tải/đọc ứng dụng. Git tree có 3.921 mục, 2.827 blob và 29.074.015 byte payload; từng URL/path/mode/blob ID/byte ở `runs/metadata-de-xuat-001/de-xuat-tai.json`. Metadata body chỉ tra trong bộ nhớ; file kế hoạch là danh sách đề xuất dẫn xuất. Kiểm lại tree object đều khớp, không thay hash để hợp thức hóa. Phần tải source/metadata sau duyệt, byte network header/TLS/retry, allocation/metadata/giải nén nội bộ và tổng lưu mọi run vẫn OPEN.

**Phạm vi trace:** 1.069 graph từ đúng prefix root hiện hành của manifest T-035: 979 entity, 90 operation. Mỗi mức đủ full/N/A; entity còn 150 s300 và 739 s60. Allowlist/opaque ID, miền whole_dev_trace_table và interval đã kiểm, không mở raw. Tất cả cạnh đầu vào là gọi-chưa-phân-kiểu; đó là đặc tính đã lưu, không được tự suy kiểu hay bỏ view typed. Chi tiết/locator ở `runs/mien-graph-002/graph-scope.json`. Không tính số khớp khi chưa có nguồn/mapping.

**Lỗi kiểm được giữ:** preflight 001 tìm nhầm cấu trúc thư mục snapshot; graph scope 001 thêm trùng tiền tố dev. Hai lỗi runner đã sửa trong quyền, mỗi lượt sau tên mới; code cũ và JSON lỗi giữ trong thư mục lượt cũ. Không có nguồn hash lệch. Sự cố API commit trả kèm patch và cách chuyển endpoint đã ghi ở đầu phiên; không lưu/dùng patch. Không xóa lượt hoặc dừng tiến trình phiên khác.

**Khả thi và cách làm nhanh hơn:** reuse graph/manifest T-035 và công cụ T-036 đã pin, không đọc lại trace. Tải toàn Git tree ứng viên có payload nhỏ giúp tránh bỏ file theo đuôi và nhiều lượt xin bổ sung, nhưng không tự bảo đảm coverage toàn hệ hoặc đúng deployment. Đề xuất tách A truy nguồn/coverage trước; B giữ nguyên nghĩa vụ bản ghi/oracle/dựng/mapping/toàn graph/hai mức/hai view/mismatch+match/kiểm/bàn giao, cần SPEC riêng sau khi A cho phạm vi thực. Chưa tự tạo task/gán mã hoặc nhận A thay toàn P5b. Giờ công A 2–4 là CANDIDATE chưa đo, phần còn lại/máy/RAM/tổng lưu còn OPEN; công thức cộng pilot, ba lượt chính/tự kiểm và mọi lỗi/lặp ở `kha-thi.json`. Không dùng dự toán lịch sử 4–6 giờ làm trần giảm kiểm. Chưa đo cost cùng việc nặng khác; chưa làm pilot để ngoại suy khi thiếu nguồn. Tổng phần máy theo Q-40 và điều kiện báo trước vẫn chưa phân xử.

**Quyết định Minh trong phiên:** chỉ lời giao nguyên văn ở trên là quyền hiện hành. Chưa có quyết định duyệt gói tải, chọn snapshot tham khảo hoặc tách task. Đề xuất nội dung lưu chính thức lời giao và phạm vi riêng docs/DECISIONS.md ở mục 6 của đề xuất; chưa ghi DECISIONS/WHY.

**Báo cáo bốn mục:**
1. Đã tự rà từ nguồn và code/đầu ra gốc, kiểm pin/hash/selector/miền, lập danh sách nguồn tải và phương án tách. Đây là tiến độ trước triển khai, chưa hoàn thành tiêu chí T-038. Câu hỏi nguồn mới xác định được giới hạn lineage/đầu vào; chưa trả lời inventory đầy đủ, độ khớp hoặc cơ chế chênh lệch, lợi ích RQ3/RQ5/P5b/G3.
2. File thay đổi: chỉ `results/T-038/`, nối LOG này và đúng dòng T-038 trong `docs/STATE.md`. STATE đọc bản mới nhất và giữ exclusive access khi ghi, lưu immediate-before/after trong `runs/ket-phien-001/`; không sửa mục tổng hợp hoặc dòng task khác. SPEC, REVIEW, DECISIONS, WHY, src/, T-035/T-036 và task khác giữ nguyên theo phạm vi phiên. Không tải snapshot/code ứng dụng hoặc ghi nguồn mới, không mở test/heldout/raw/archive, không chạy baseline/RCA/P6/T-040/EC2, không commit/push hoặc tự mở/gửi chat. Ngoại lệ API đã nhận kèm patch trong bộ nhớ được khai riêng, không che bằng câu không tải.
3. Kiểm: 187 artifacts T-036/pin/snapshot code và nguồn RCAEval T-002 khớp; 1.069 graph và selector/allowlist/interval/type đạt; metadata tree object khớp. Lượt lỗi và lượt đạt đều giữ. Kiểm cuối append-only/diff/phạm vi/prompt/JSON/manifest sẽ được ghi bổ sung dưới đây bằng finalize.py; không coi các kiểm này là kiểm đúng đắn của graph tĩnh hoặc câu trả lời khoa học chưa làm.
4. Cần Minh quyết: duyệt hay không gói nguồn tham khảo, cách tách/phạm vi sửa SPEC và quyền ghi quyết định chính thức. Chủ nguồn RCAEval/Minh còn cần cung cấp build/image/instrumentation/deployment sinh dataset để nâng khỏi đối chiếu có điều kiện. T-040/P6/P9 còn thiếu mô hình, địa chỉ và phân tích nguồn TT; chưa chọn thiết kế hoặc quy lỗi instrumentation. Không có bất đồng phản biện T-038 có file để xử lý trong lượt này. Prompt dưới để Minh chọn chuyển, không tự mở lại vòng soát cả ba SPEC.

**Bước tiếp chính xác:** đọc đề xuất, danh sách blob đã pin, `nguon.json`, `kha-thi.json` và câu trả lời Minh. Chỉ tải sau quyền đúng gói; chỉ sửa SPEC/WHY/DECISIONS theo phạm vi được duyệt riêng. Trước dùng đầu vào, kiểm pin/manifest; nếu cần chạy lại vì đầu vào thay đổi, dùng tên run mới: `py -3 -X utf8 -B results/T-038/preflight.py <ten-run-moi>`. Không chạy lại kiểm rộng khi đầu vào chưa đổi. Chưa có downloader được viết/chạy.

**Lệnh kết phiên:** `py -3 -X utf8 -B results/T-038/finalize.py`; lệnh này chỉ kiểm, giữ diff/phạm vi, nối kết quả kiểm LOG và tạo manifest đầu ra T-038. Kết quả thực tế ghi ngay dưới sau khi chạy.

**Đề xuất commit, chưa thực hiện:** `docs: record T-038 preflight and source proposal`. Chỉ commit/push sau Minh yêu cầu/duyệt riêng.

**Nội dung formal report:** phân biệt nguồn thiết kế/code với quan sát, lineage revision, coverage nguồn và mẫu số; chưa đưa tỷ lệ khớp hoặc cơ chế thiếu cạnh khi chưa có kết quả.

### Prompt Claude — Minh chuyển thủ công

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-038; D:/RCA-flashticket/tasks/T-038-p5b-trainticket/SPEC.md; đề xuất tại D:/RCA-flashticket/results/T-038/de-xuat-nguon-va-tach.md.
- Công đoạn: soát SPEC.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude phản biện kết quả theo phân công hiện hành.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/review-prompt.md; SPEC/LOG T-038; phương án P5b tại LOG T-036 Phiên 1; các đầu vào SPEC liệt kê.
- Phản biện và phản hồi trước: Không có REVIEW T-038 trên đĩa. Tự rà người làm tại results/T-038/tu-ra-spec.md; lịch sử nguồn phụ thuộc tại tasks/T-036-p5b-hop-dong-chung/REVIEW.md và LOG.md.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-038/manifest.json và các file được phủ; results/T-036/manifest.json, runs/kiem-r1-after-002/code/ và code-hashes.json; src/do_thi_tinh/README.md; results/T-035/manifest.json; results/T-002/handoff-manifest.json; Windows/PowerShell, Python 3.12 -X utf8 -B.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; chưa được ghi REVIEW hoặc sửa file, tải nguồn hay chạy thực nghiệm mới. Minh quyết phạm vi ghi riêng nếu chuyển lượt này.

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

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


**Bổ sung kiểm cuối Phiên 2 — 16/10/2026:** finalize.py kiểm append-only LOG, diff STATE chỉ dòng T-038, nguồn bảo vệ/pin hiện hành, phân hoạch/byte đề xuất, prompt nguyên văn, mọi JSON và cú pháp Python, không sinh bytecode: đạt. Giữ các lượt lỗi và toàn bộ file kết quả, ghi diff và manifest riêng T-038; không đổi SPEC/quyết định khoa học hoặc tự nghiệm thu. Lệnh cuối đã chạy: `py -3 -X utf8 -B results/T-038/finalize.py`. Bước tiếp vẫn chờ Minh quyết đúng các nội dung ở đề xuất; không tự tải hoặc mở phần B.


### Tiếp tục Phiên 2 — 16/10/2026 — Codex — LEVANMINH — người làm

Minh trả lời nguyên văn: “không tách, làm trong 1 phiên , duyệt gói tải”. Giữ toàn bộ SPEC, không tách task, không sửa SPEC/WHY/DECISIONS. Duyệt gói tải đã trình tại de-xuat-nguon-va-tach.md mục 2–3 và danh sách blob đã ghim. Lời duyệt không xác minh revision sinh dataset; kết quả dùng nguồn này giữ điều kiện tham khảo. Đã kiểm manifest đầu ra trước tiếp tục, giữ bản trước dưới runs/trien-khai-001/. Tiếp tục triển khai đủ bước theo quyền đã có; chỉ ghi results/T-038/, nối LOG và đúng dòng STATE.


**Sự cố coverage, báo ngay trong chat 16/10:** nhánh hỗ trợ đã decode/index nhầm 15 tệp telemetry mẫu công khai trong old-docs/Json2Shiviz, trái giới hạn không đọc raw telemetry của lời giao. Không mở data/, RE2 raw/test/heldout. Root chưa đọc content-index lỗi. Đã yêu cầu giữ lượt lỗi, ghi incident danh sách path/output, không dùng mẫu trong facts/graph/mapping/kết luận, và tạo index sạch chỉ kiểm integrity nhóm mẫu. Không tự xóa hoặc ghi đè bản lỗi; không thể hoàn tác việc đã đọc. Đề xuất khắc phục bằng cách loại nội dung đó khỏi chuỗi bằng chứng và giữ kiểm tra nguồn độc lập. Tiếp tục phần không phụ thuộc.


**Tiến độ triển khai:** gói tải tai-nguon-001 đủ 2827 đường dẫn/2712 unique blob, không lỗi; 29.074.015 byte cây nguồn, payload nhận28.752.055 byte nhờ blob trùng, metadata1.088.474 byte, header/TLS chưa đo. Nguồn factual/code coverage tách profile và lineageOPEN. Assembler001 lỗi schema operation fact (giữ error/script),002/003đạt;004đã giữ targethandlerdynamic làcandidateOPEN, không chọn từshape. Sourcegraph110entity/993operation/508relation, chưa biểu diễnSMTPvà chưa nhận inventoryđầyđủ.

**Pilot:** pilot001 lỗi adapter đưa mappingoperation vàographentity, đãlọc theo level trong runner; pilot002 functionalđạt nhưng RAM0 doAPIbinding là sốkhônghợp lệ, không dùng; pilot003 đãsửa binding, functionalđạt, peak77131776byte,4graphbao gồm3phépcomparemỗi graph. Tấtcảgiữrunriêng. Dự toán máy/đĩa toàn1069graph từpilot ở runs/du-toan-tu-pilot.json; không thay phépđo full. Không thấy tiếntrìnhPythonkhác ở preflightpilot, không dừng việc phiênkhác. Các unknown/cost saiđượcgiữrõ.


**Checkpoint ngữ cảnh trong cùng Phiên 2:** đã nén ngữ cảnh; giữ yêu cầu Minh làm trong một phiên, không tách. Full run doi-chieu-dev-001 kết thúc thành công: 1069 graph, 337.953 giây operational elapsed, 73.862.554 byte JSON gzip, peak working set cuối lượt 230.506.496 byte (gồm bước tổng hợp). Các số từ stdout của runner; sẽ đối chiếu summary trước báo cáo. Pin T036 không đổi. Bước tiếp: đọc summary và supplement tín hiệu độc lập, merge nếu hợp lệ, kiểm/recompare khi đầu vào thay; phân tích cơ chế, coverage/lineage, chi phí thực, prompt đúng mẫu; final diff/manifest và chỉ cập nhật dòng T038. Lệnh cuối: đọc đuôi LOG và engine cùng poll session45799 (exit0). Không chạy lại bước tải hoặc dùng index coverage lỗi.


### Kết thúc triển khai trong cùng Phiên 2 — 16/10/2026 — Codex — người làm

**Quyết định của Minh trong phiên:** giữ nguyên lời duyệt “không tách, làm trong 1 phiên , duyệt gói tải”. Minh nhắc tiếp tục từ checkpoint mới nhất, giữ chất lượng đầu ra và kiểm subagent. Hai phần hỗ trợ đã hoàn tất, không còn lượt chạy nền cần tiếp quản; đều là trợ giúp người làm, không phải Claude phản biện. Không tạo task/SPEC mới, không sửa quyết định khoa học. Đề nghị ghi chính thức lời duyệt vào DECISIONS nằm trong de-nghi-tiep-theo.md, chưa ghi file đó vì ngoài quyền.

1. **Đã làm gì:** tải đúng gói source được duyệt; đủ 2827 blob/3921 tree entries, byte/hash đúng. Khảo sát code/config/build/deployment, thêm 135 khai báo signal vào model005 sau phần cơ sở. Model có 110 entity,993 operation,508 relation,50 resource binding,139 signal; còn151 unresolved. Hai graph có165/342 cạnh; projection operation có121 cạnh, entity-only44, phân hoạch đúng165. So đủ1069 graph dev của30 ID mờ:979 entity và90 operation, full/N/A cùng cửa sổ s60/s300 có sẵn. Giữ tất cả run lỗi/lặp và mọi JSON members/exclusions lossless gzip. Không mở RE2 raw/test/heldout/data khóa, không chạy baseline/RCA/P6/T040 hoặc source application/build. Toàn bộ kết quả conditional reference, chưa nối được app/instrumentation/image/deployment sinh dataset.
2. **File thay đổi:** chỉ results/T-038/ (nguồn tải, code riêng, bản ghi/mapping/graph/so sánh, coverage, báo cáo, fixtures, runs, manifest/prompt); nối LOG này và thay đúng dòng T038 trong STATE bằng lock/đọc bản mới nhất. Danh sách từng file/hash nằm trong manifest cuối. SPEC/src/shared/T035/T036/WHY/DECISIONS/AGENTS và thay đổi có sẵn được bảo vệ. Không commit/push. Bản trước các file root đã có được lưu; LICH-SU.md chỉ rõ đầu ra hiện hành và phần preflight hết hiệu lực.
3. **Kiểm đã chạy:** preflight pin và toàn187 artifact T036; code hiện hành so snapshot. Java checks32/32 và assembly004 audit14/14 trong phạm vi parser khai báo. Oracle riêng trước mã và supplemental SMTP phân biệt chronology; fixture cuối23/23. Mỗi graph có set/member/exclusion/denominator/null/interval/input-unchanged, repeat và reorder; đủ1069graph đều đạt. Full001:337.953s,230506496byte peak; full002 trên model005:260.109s,231550976byte peak; mỗi lượt73862554byte JSON gzip. Toàn SHA output hai lượt giống nhau; signal thêm không đổi cạnh. Đây là operational accounting, không benchmark cách ly. Pilot dự toán174s không dùng thay phép đo; chi phí extraction/labor/failures chưa có timer không được bịa thành tổng. Disk mọi run/source/intermediate sẽ được đo trong manifest cuối. Bảng từng ca/miền và min–max ở phan-tich-chenh-lech.json, không dùng trung bình để quy nguyên nhân.
4. **Đạt tới đâu và còn gì:** source inventory ngữ nghĩa chưa đủ:2758blob đã đọc theo độ sâu ghi riêng,42loại/cách ly,27OPEN. Có owner/input/tool/ước tính ở coverage, gồm ảnh chưa chắc an toàn, PDF, swapHelm và archiveinstrumentation. Năm cặp riêng trace đã có đối chiếu source direct/indirect/chiều và control dương; chưa quy được cho revision/collector. Op T đủ điều kiện rỗng vì mapping thiếu/mơ hồ; không là không có call. Nguồn→ID→mapping→exclusion→set đã lần cụ thể. SMTP có counterexample enum, dừng riêng relation và giữ external entity; chưa đổi hợp đồng chung. Đã cung cấp đầu vào T040/P6/P9, chưa chọn phương pháp hoặc chứng minh lợi ích RCA, chưa đóng RQ3/RQ5/G3. Task đạt một phần, chờ Claude soát kết quả và Minh quyết phần thiếu, không tự nghiệm thu.

**Sự cố và phạm vi ảnh hưởng:** coverage helper ban đầu đã decode15 mẫu telemetry lịch sử công khai, XML của old-docs/debugging.xlsx và xem image/jaeger.png. Trái giới hạn không đọc raw trong lời giao; đã báo ngay trong chat. Ba index lỗi giữ nguyên/cách ly, root không mở nội dung index lỗi, model/mapping/facts dựa code/config độc lập và rerun sạch. Không thể hoàn tác việc đã đọc, không tuyên bố tuân thủ toàn phiên. Incident danh sách path/output/dependencies ở runs/trien-khai-001/coverage/incident.json. Lượt cuối chỉ hash nguồn và index cách ly, không parse lại. Metadata GitHub commit endpoint lúc tiền duyệt từng trả patch ngoài dự kiến trong memory: không lưu/dùng, đã báo trước và chuyển git metadata endpoints; gói tải tiếp theo chỉ chạy sau Minh duyệt.

**Bước tiếp chính xác:** hoàn tất `py -3 -X utf8 -B results/T-038/finalize_implementation.py`, kiểm kết quả runs/ket-phien-002/final-verification.json và manifest. Minh chuyển prompt dưới đây cho Claude soát kết quả; chưa có quyền ghi REVIEW nên chỉ đọc/trả lời chat. Minh quyết các đề nghị SMTP/lineage/coverage trong de-nghi-tiep-theo.md; không tự sửa shared hay tải thêm. Commit đề nghị sau nghiệm thu và có quyền: `T-038: khảo sát nguồn Train Ticket và đối chiếu dev có điều kiện`. Lệnh cuối trước ghi mục này: kiểm projection bằng pinned build, đọc kết quả reports; lệnh cuối sau kiểm sẽ được nối ngay bên dưới.

**Prompt để Minh copy sang Claude (không tự gửi):**

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-038, tasks/T-038-p5b-trainticket/SPEC.md và LOG.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P5, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện kết quả.
- Tài liệu gốc: tasks/T-038-p5b-trainticket/SPEC.md, LOG.md; docs/MRP.md và các nguồn trực tiếp chi phối được SPEC liệt kê.
- Phản biện và phản hồi trước: chưa có bản phản biện kết quả T-038.
- Code và kết quả liên quan: results/T-038/manifest.json, ban-ghi.json, nguon.json, bao-phu-nguon.md/json, mapping.json, do-thi/, doi-chieu/index.json, phan-tich-chenh-lech.md/json, kiem-dung-dan.md, ban-giao.md; snapshot T-036 theo SPEC; Windows Python 3.12, py -3 -X utf8 -B; scripts/runs trong results/T-038/.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; Minh chưa cấp quyền ghi REVIEW cho lượt này.

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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


**Kiểm cuối triển khai:** finalize_implementation.py đạt toàn bộ kiểm pin/hash, rebuild/đếm bản ghi, đủ 1069 output và tập/mẫu số/interval, input bất biến, oracle/lặp/đảo, coverage partition, LOG append-only, STATE chỉ dòng T038 và prompt nguyên văn. Nguồn/mẫu/index cách ly chỉ hash, không parse lại. Giữ phần khoa học chưa đủ và mọi lượt lỗi. Lệnh cuối đã chạy: `py -3 -X utf8 -B results/T-038/finalize_implementation.py`. Bước tiếp: Minh chuyển prompt-claude.txt cho Claude soát kết quả và quyết phần thiếu; không tự chạy ngoài quyền hoặc nghiệm thu.


**Rà con trỏ tài liệu cuối:** chuẩn hóa các tham chiếu rút gọn coverage/java-source thành đúng runs/trien-khai-001/ trong báo cáo/LICH-SU và script tái tạo. Không đổi số, graph/mapping hoặc kết luận; toàn bộ artifact trước ngoài bốn file văn bản/mã tái tạo giữ hash. Bản trước và diff ở runs/chinh-con-tro-tai-lieu-001/. Kiểm cuối triển khai vẫn28/28đạt; manifest cập nhật theo đúng file đã đổi/thêm. Lệnh cuối: `py -3 -X utf8 -B results/T-038/fix_report_references.py`. Bước tiếp không đổi: Minh chuyển prompt cho Claude, quyết phần thiếu; không tự nghiệm thu/commit/push.
