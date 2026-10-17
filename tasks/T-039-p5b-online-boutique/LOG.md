# Nhật ký T-039

Chỉ nối thêm. Phân biệt quyền tạo tài liệu, duyệt triển khai và quyền tải nguồn.

## Phiên 1 — 15/10/2026 — Codex — LeVanMinh — vai trò: người làm tài liệu đề xuất

**Mở phiên:** đọc AGENTS, STATE, mẫu SPEC/LOG, nguồn DT18/cô, MRP phần chi phối, LESSONS, WHY/DECISIONS và phương án P5b/đầu ra T-036 hiện hành. Chưa có SPEC/LOG T-039 trước lượt ghi. Kiểm hash kết quả T-036 và nguồn registry trước dùng đều khớp; không làm lại phần công cụ đã nghiệm thu.

**Công đoạn/mục tiêu:** tạo SPEC ở trạng thái ĐỀ XUẤT/CHỜ PHẢN BIỆN theo quyền chuẩn bị; Online Boutique/Nezha: truy revision/lineage, coverage snapshot, đối chiếu miền dev-adapter, nguồn phụ và Node/host còn OPEN. Phục vụ DT18-NV2/NV3, cô bước 1, MRP P5 và đầu vào RQ3/RQ5/P6/P9. Chưa có kết quả khảo sát của task.

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
6. Lệnh cuối lượt chuẩn bị: py -3 -X utf8 -B - (Python inline kiểm toàn diff/phạm vi chín file, append-only, template/prompt/pin và nguồn bảo vệ, in kết quả trong chat). Lệnh đọc tiếp: Get-Content -LiteralPath 'tasks/T-039-p5b-online-boutique/SPEC.md' -Raw.

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


## Phiên 2 — 15/10/2026 — Codex — LEVANMINH — vai trò: người làm T-039

**Phân loại:** EXECUTE có điều kiện. Tự rà từ nguồn gốc trước lịch sử phản biện; kiểm khả thi một phiên và trình tải mới trước phần phụ thuộc. Claude phản biện kết quả. Quyền chỉ results/T-039/, nối LOG này và đúng dòng T-039 của STATE. Không sửa SPEC hoặc nguồn quyết định.

**Nguyên lời Minh giao:**

Tôi giao bạn triển khai T-039 theo SPEC hiện hành, sau khi tự rà SPEC, kiểm khả năng hoàn thành trong một phiên và trình phần tải nguồn cần duyệt. Tôi đã đồng ý dừng lượt phản biện ba SPEC T-037/T-038/T-039. Đây là quyền triển khai có điều kiện; chưa duyệt tải repository hoặc nguồn mới.

Làm việc tại D:/RCA-flashticket.
Task: tasks/T-039-p5b-online-boutique/SPEC.md.
Bạn là Codex người làm. Claude phản biện kết quả. Tự rà không thay phản biện chính thức.

Trước triển khai:
1. Đọc AGENTS.md, docs/STATE.md, toàn bộ SPEC và mục cuối LOG T-039. Đọc trực tiếp DT18, hướng dẫn của cô, MRP phần RQ3/RQ5/P5/P6/P9/G3, LESSONS, WHY/DECISIONS liên quan và phương án P5b gốc trong LOG T-036 Phiên 1.
2. Tự rà như lần đầu từ nguồn/code/đầu ra thật; lập nhận xét trước khi mở kết luận phản biện hoặc phản hồi cũ. Đọc nguyên văn Prompt chung + Soát SPEC + G3 trong docs/review-prompt.md làm tiêu chí tự rà. Quyền người làm theo lời giao này và SPEC.
3. Kiểm hash trước dùng. Cùng pin T-036 được SPEC liệt kê, current_run runs/kiem-r1-after-002; snapshot code ở results/T-036/runs/kiem-r1-after-002/code/, code-hashes.json tại thư mục run. Kiểm mã hiện hành khớp snapshot. Không tự đổi pin hoặc sửa hash khi nguồn lệch.
4. Phân xử khả năng xong một phiên cho truy lineage/coverage, bản ghi/mapping, dựng/đối chiếu, phân tích, tự kiểm và bàn giao. Tách giờ công/giờ máy/RAM/byte tải/tổng đĩa cho mọi lượt cần giữ. Dự toán chưa đo phải ghi rõ. Không vừa một phiên hoặc chưa đủ căn cứ thì trình cách tách và ảnh hưởng, không giảm độ sâu hoặc tự chia task.
5. Trình sớm phần tải nguồn cần duyệt. Dùng đúng nguồn Nezha đã xác minh theo results/T-003/runs/final-review-003/artifact-manifest.json, nguồn results/T-008/sources/ và registry T-036. IntelligentDDS/Augmented-OnlineBoutique là repository ứng viên; chưa được coi là revision ứng dụng sinh dataset. Phân biệt tree object, commit code Nezha, ứng dụng, dataset, image và deployment. Không tự thay bằng upstream hoặc bản mới nhất.

Đề xuất tải phải có nguồn/URL, revision và mức xác minh, cây snapshot hoặc metadata dùng xác định danh sách, từng nhóm tệp/đối tượng, lý do cần, phần loại trừ và ảnh hưởng, byte mạng, dung lượng giải nén/tổng lưu và đường dẫn ghi. Có thể tra metadata công khai theo quyền chỉ đọc để lập đề xuất; chưa clone, tải snapshot/code hoặc ghi nguồn mới trước khi Minh duyệt. Thiếu revision/byte thì nêu bằng chứng cần, không bịa số. Ngoài scope hoặc cần data/README.md thì trình quyền ghi riêng.

Có lỗi cần sửa SPEC, mâu thuẫn nguồn/quyền, pin lệch hoặc phạm vi không khả thi thì dừng phần phụ thuộc; trình bằng chứng, hậu quả và sửa tối thiểu theo file. Không tự sửa SPEC. Tự rà đạt thì tiếp tục phần đủ nguồn trong quyền, không hỏi lại quyền đã có. Trong lúc chờ tải, làm phần độc lập đã có nguồn hợp lệ.

Phạm vi ghi: results/T-039/, nối tasks/T-039-p5b-online-boutique/LOG.md và chỉ dòng T-039 trong docs/STATE.md. Ghi nguyên lời giao, ngày/thiết bị/vai trò, kết quả tự rà và khả thi vào LOG. Trạng thái ĐỀ XUẤT là mốc trước lời giao; không tự sửa SPEC. Không ghi REVIEW, DECISIONS, WHY, src/, T-035/T-036, platform hoặc task khác. Quyết định cần lưu chính thức thì trình nội dung/phạm vi riêng.

Thực hiện đủ SPEC. Kiểm inventory theo toàn cây snapshot định danh, xét nguồn gián tiếp/config/template/build/schema/mã sinh và phần loại trừ. Không lấy phần đã tải hoặc service có trace làm toàn inventory. Không áp quy ước FT/TT sang OB.

Bản ghi và mapping phải có provenance, owner/scope/điều kiện. Viết oracle độc lập trước biến đổi riêng; dùng T-036 đã ghim. Chọn graph Nezha-OB dev hiện hành theo manifest T-035, không lấy graph lịch sử trong runs/. So toàn graph/cửa sổ được giao ở hai mức và các ảnh chụp có sẵn; không tự tạo cửa sổ mới. Giữ miền dev-adapter, interval, endpoints/typed, members/exclusions, tập giao/phần riêng và mẫu số N/A.

Truy lineage nguồn phụ bằng code/tài liệu trong quyền. Metadata cùng pipeline chưa là bằng chứng độc lập; metadata mức ngày chỉ dùng phạm vi mô tả đã cho phép, không chọn P6. Không mở Weight, chuỗi số hoặc Node/log/metric/trace thô để khảo sát thêm. Không suy host từ tên Node hoặc tính ổn định tên; thiếu nguồn nghĩa định danh thì giữ OPEN.

Lần theo nhóm chênh lệch quan trọng và match tương ứng; xét revision/alias/miền/nhánh/nguồn/telemetry/chuyển đổi. Mapping không tối ưu theo tỷ lệ khớp và không nhận nhãn. Revision chưa nối được phải hiện ngay trong JSON/báo cáo dưới dạng đối chiếu tham khảo có điều kiện.

T-037/T-038 chạy song song và giữ cùng pin T-036. Cần đổi hợp đồng chung thì dừng phần phụ thuộc, trình phản ví dụ và ảnh hưởng cả ba nhánh; không tự sửa hoặc fork nghĩa chung. STATE cập nhật tuần tự, đọc bản mới nhất trước sửa đúng dòng task; nếu không bảo đảm được thì trình dòng cần cập nhật để Minh điều phối. Không đo chi phí cùng việc nặng khác hoặc dừng tiến trình phiên khác. Thao tác tốn kém theo AGENTS phải báo chi phí và chờ duyệt.

Giữ mọi lượt kể cả lỗi/lặp, trung gian, lệnh và môi trường. Không mở test/heldout/archive, chạy baseline/RCA, chọn P6, làm T-040, bật EC2, commit/push hoặc tự mở/gửi chat.

Cuối phiên kiểm toàn diff/phạm vi/manifest, phân biệt đạt task với mức trả lời mục tiêu nguồn. Nối LOG đủ báo cáo, OPEN, bước tiếp/lệnh cuối; cập nhật đúng dòng STATE. Soạn prompt Claude nguyên văn Prompt chung + Soát kết quả + G3 hiện hành; nếu dừng vì cần sửa SPEC thì dùng Soát SPEC. Minh chuyển thủ công. Không tự nghiệm thu hoặc đóng task/G3.

**Mở phiên:** đã đọc AGENTS, STATE, toàn SPEC và mục cuối LOG. Trạng thái ĐỀ XUẤT là mốc cũ theo lời giao; đang tự rà và kiểm nguồn, chưa tải nguồn/code hoặc chạy dựng/đối chiếu. Một nhánh hỗ trợ chỉ đọc kiểm hash và inventory graph; không là phản biện chính thức, không ghi file.


### Tự rà độc lập và kết thúc tiền kiểm — 16/10/2026

**Tự rà trước lịch sử:** đã đọc trực tiếp DT18/cô, MRP RQ3/RQ5/P5/P6/P9/G3, LESSONS, WHY-52/53, quyết định liên quan, mẫu SPEC, nguyên văn Prompt chung/Soát SPEC/G3 và phương án P5b gốc LOG T-036 Phiên 1. Đọc nguồn/code/manifest thật, ghi nhận xét độc lập vào results/T-039/tu-ra-va-kha-thi.md trước khi đọc REVIEW và mốc đóng T-036. Không mở kết luận soát SPEC T-039 cũ hoặc tự mở vòng phản biện. Nhánh hỗ trợ chỉ kiểm hash/inventory, không ghi file hoặc giữ vai trò phản biện chính thức.

**Diễn biến/đầu ra:** kiểm cục bộ bằng preflight.py tien-kiem-001 đạt; lưu pin từng artifact, mã hiện hành so snapshot, Git blob T-008, canonical graph list và interval. Metadata công khai chỉ được đọc trong bộ nhớ để lập đề xuất, không lưu raw response/code mới. Bảng đề xuất có toàn cây với action đọc/loại trừ, từng URL/blob/byte và nhóm nguồn, không được gọi là inventory ứng dụng đã khảo sát. Quan sát máy là capacity snapshot, không đo hiệu năng cùng việc nặng khác. Không chạy build/compare/RCA, không đọc raw telemetry/Weight/Node values/test/heldout/archive.

**Nhận xét độc lập:** pin/hash T-036 đạt; miền graph hiện hành đã xác định. Registry gọi revision Nezha là tree object, API Git commits chứng minh là commit với tree canonical có cùng thành viên snapshot. Chặn suy luận từ loại object cũ; không có mismatch nội dung và không đổi pin. Revision ứng dụng/dataset/image/deployment, độc lập nguồn phụ và nghĩa host vẫn OPEN. Chưa có căn cứ cam kết toàn SPEC một phiên; dự toán phân rã, phương án tách và ảnh hưởng từng file ở các đề xuất. Không tự sửa SPEC hoặc giảm tiêu chí. Đây là tự rà người làm, chưa là REVIEW chính thức hoặc nhiệm thu.

**Quyết định của Minh trong phiên:** nguyên lời giao ở đầu Phiên 2; triển khai có điều kiện và quyền ghi đúng scope. Chưa có quyết định tải nguồn, sửa registry/pin, tách task hoặc chọn P6. Trình lưu chính thức nguyên ý sau khi Minh quyết, không ghi DECISIONS/WHY bằng quyền này.

**Báo cáo kết thúc:**
1. Đã hoàn tất tiền kiểm và phần độc lập có nguồn hợp lệ: quyền/nguồn, pin/hash, graph inventory, đọc API/code analysis liên quan, đề xuất tải/chi phí/tách và bàn giao. Chưa đạt đầu ra khảo sát/bản ghi/mapping/graph/đối chiếu/phân tích của toàn SPEC. Chưa trả lời RQ3/RQ5 hoặc đóng P5b/G3.
2. File ghi: results/T-039/ (tất cả path trong manifest); chỉ nối LOG này; chỉ dòng T-039 trong STATE. Không sửa SPEC, REVIEW, DECISIONS, WHY, src hoặc T-035/T-036/platform/task khác. Giữ toàn thay đổi có sẵn; không commit/push.
3. Kiểm: toàn 187 artifact T-036, code-hashes/snapshot/current code, nguồn T-008 theo manifest cuối T-003, Git blob nguồn và toàn 132 graph hiện hành khớp; canonical path khớp. JSON input-verification/graph-inventory là bằng chứng số. Không chạy pilot hoặc thí nghiệm ứng dụng. Kiểm cuối manifest/protected hash/prefix LOG/dòng STATE/prompt/số đề xuất bằng finalize_preflight.py verify; kết quả ở final-verification.json.
4. OPEN/bị ảnh hưởng: phạm vi một phiên, tải nguồn cụ thể, cách xử lý mô tả loại object; chưa nối deployment, chưa chứng minh coverage/alias/nguồn phụ/Node. Owner nguồn thiếu: tác giả Nezha/application deployment cho build/image/export schema; Minh quyết cấp nguồn/tách; người làm khảo sát/đối chiếu sau duyệt. T-040/P6/P9 không được nhận số khớp hoặc kết luận thiếu telemetry từ tiền kiểm này. Nội dung nên vào báo cáo: loại object/revision, điều kiện đối chiếu, miền adapter, coverage nguồn và giới hạn độc lập.
5. Bước tiếp chính xác: Minh đọc results/T-039/tu-ra-va-kha-thi.md, de-xuat-tach.md, de-xuat-tai.md/json; quyết tải, tổ chức task và cách xử lý metadata chung. Chưa chạy tải từ đề xuất. Sau duyệt phạm vi cụ thể, lập/sửa SPEC theo quyền riêng nếu chọn tách; nếu chỉ duyệt tải thì chỉ thu nguồn đúng danh sách, không tự sửa task/pin. Muốn tiếp từ pin cũ: kiểm lại results/T-036/manifest.json và code snapshot trước phần phụ thuộc; dừng khi lệch. Lệnh đọc: Get-Content -Raw -LiteralPath 'results/T-039/de-xuat-tai.md'.
6. Lệnh cuối dự kiến của lượt này và bước kiểm cuối: py -3 -X utf8 -B results/T-039/finalize_preflight.py verify. Lệnh có ghi kết quả chỉ trong results/T-039; không gọi preflight trên tên run cũ. Sau kiểm chỉ báo lại, không mutation khác trong repo.

**Đề xuất commit, chưa thực hiện:** docs: record T-039 preflight and source acquisition proposal. Không commit/push khi chưa có Minh duyệt riêng.

### Prompt Claude — soát đề xuất SPEC (Minh chọn chuyển thủ công)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-039; tasks/T-039-p5b-online-boutique/SPEC.md; đề xuất tại results/T-039/de-xuat-tach.md và de-xuat-tai.md/json.
- Công đoạn: soát SPEC.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude phản biện kết quả theo lời giao hiện hành. Claude nhận lượt soát đề xuất SPEC này nếu Minh chuyển prompt.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; SPEC.md và LOG.md T-039; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md; LOG T-036 phần phương án gốc; results/T-039/tu-ra-va-kha-thi.md, de-xuat-tach.md, de-xuat-tai.md/json. Bản trước và diff tại results/T-039/runs/tien-kiem-001/.
- Phản biện và phản hồi trước: Không có bản REVIEW trong thư mục T-039 tại lúc soạn prompt; lịch sử lời giao và tài liệu ở LOG T-039. Với đầu vào T-036, lịch sử trong LOG và REVIEW.md của T-036.
- Code và kết quả liên quan: results/T-036/manifest.json, current_run runs/kiem-r1-after-002, code/ và code-hashes.json tại run; src/do_thi_tinh/README.md và code; results/T-035/manifest.json; results/T-003/runs/final-review-003/artifact-manifest.json và nguồn T-008 theo SPEC. Kết quả tiền kiểm tại results/T-039/manifest.json và runs/tien-kiem-001/. Windows/PowerShell; Python -X utf8 -B. Đọc preflight.py trước khi cân nhắc chạy vì script tạo run; lượt soát này không tự cấp quyền tạo run.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC hoặc kết quả từ prompt này; không tải nguồn mới, sửa pin hoặc chạy thực nghiệm.

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

### Minh trả lời sau tiền kiểm — 16/10/2026

Ba câu trả lời nguyên văn: (1) “Duyệt đúng danh sách”; (2) “Giữ toàn phạm vi T-039 để xem lại khả thi sau khi có nguồn”; (3) “Giữ pin, ghi rõ chứng cứ tại T-039”. Câu hỏi, proposal và hash ràng buộc ở results/T-039/authorization-20261016.json. Quyền tải đúng danh sách/metadata/path của de-xuat-tai.json, không sửa SPEC hoặc registry/pin T-036. Tiếp tục thu nguồn, kiểm byte/Git blob/SHA256, rồi xem lại khả thi; chưa tự chia task hoặc dựng/đối chiếu khi chưa phân xử điều kiện một phiên. Chưa có quyền ghi DECISIONS/WHY; trình nguyên ý để lưu chính thức riêng.

Tiền kiểm trước thu đã chốt và kiểm đạt: finalize_preflight.py verify, manifest 25 file, 14 nguồn bảo vệ nguyên vẹn, LOG nối và STATE chỉ đúng dòng task. Manifest này được snapshot trong run thu trước cập nhật tiếp. Nội dung “chưa duyệt” trong báo cáo tiền kiểm/proposal là mốc trước ba câu trả lời này. Bắt đầu run thu-nguon-001; mọi request/lỗi/lượt và môi trường được giữ trong phạm vi T-039.

### Checkpoint sau thu nguồn và xét lại khả thi — 16/10/2026

**Quyết định hiện hành:** giữ nguyên ba câu trả lời Minh đã nối ở trên. Đã dùng quyền tải đúng danh sách; giữ toàn phạm vi T-039, không tự sửa SPEC/tách hoặc đổi pin. Đính chính loại object ghi trong registry riêng results/T-039/nguon.json; registry chung không đổi. Việc ghi DECISIONS cần quyền riêng, nội dung đề nghị ở de-nghi-ghi-quyet-dinh.md.

**Diễn biến:** chạy acquire_sources.py thu-nguon-001; thu xong 223 file nguồn/sáu metadata, tất cả size/Git blob khớp, payload 37.524.834 byte, không lỗi. Không tải bốn log thô hoặc nguồn ngoài; không clone/cài gói/build/image. Sau đó post_acquisition_audit.py khao-sat-nguon-001 kiểm lại 229 hash và lưu profile/declaration/JAR metadata; không chạy code nguồn hoặc dựng graph. Hai nhánh hỗ trợ chỉ đọc source trong phạm vi phân công, không phản biện chính thức; root đối chiếu đoạn nguồn quan trọng trước ghi báo cáo.

**Kết quả sau nguồn:** có biến thể deployment cùng tên, Cart Redis/local, adservice MySQL, generated không đồng nhất proto chung và tên span nội bộ; không thể rút gọn thành cây+proto. Chưa có producer metadata hoặc cầu nối NodeName→Node dataset trong phần nguồn đã đọc; chưa xác minh app/image/deployment sinh dataset. Profile UTF-8/ZIP không đồng nghĩa semantic coverage. Báo cáo có locator/phần đã đọc/chưa đọc và owner bằng chứng thiếu. Không lập mapping, tối ưu alias hoặc quy nguyên nhân cho ca dataset từ các ví dụ này.

**Kết thúc lượt/checkpoint:**
1. Đã hoàn tất đúng thu nguồn được duyệt và phần kiểm/đọc để xét lại khả thi; đầu vào đã sẵn cho khảo sát tiếp. Chưa đạt toàn tiêu chí bản ghi/graph/đối chiếu/phân tích của SPEC; chưa trả lời RQ3/RQ5/G3 hoặc đóng P5b. Điều kiện một phiên chưa có căn cứ xác nhận; dự toán còn lại CANDIDATE 6–10,5 giờ công, không giảm kiểm. Minh chưa duyệt ngoại lệ nhiều phiên; giữ toàn task không tự là ngoại lệ. Trình quyết định cách tiếp tục, không tự chia task.
2. File ghi chỉ results/T-039/, nối LOG này và dòng T-039 của STATE. Manifest cuối liệt kê toàn file; bản trước/nguồn đã thu/lượt kiểm được giữ. Không sửa SPEC, src, WHY/DECISIONS/REVIEW hoặc T-035/T-036/platform/task khác; không commit/push.
3. Kiểm: tiền kiểm 187 artifact T-036 và 132 graph hiện hành khớp; thu nguồn size/blob/SHA256 đạt; kiểm sau thu 229/229; tổng declaration và profile có JSON; kiểm cuối scope/hash/prefix/prompt/manifest ở runs/ket-sau-tai-001/final-verification.json. Giờ thu thực không là benchmark độc quyền; peak RAM lượt thu chưa đo, không suy lại. Chưa chạy pilot toàn pipeline hoặc tự kiểm graph/mapping chưa tồn tại.
4. OPEN và quyết định phụ thuộc: khả thi một phiên/cách tiếp tục do Minh; semantic coverage/owner/alias/generated/nhánh do người làm phải hoàn thành; deployment/image/producer metadata/export schema do tác giả/nguồn có provenance, Minh quyết quyền bổ sung nếu cần. T-040/P6/P9 chưa được nhận graph hoặc kết luận thiếu telemetry/host từ gói này. Formal report chỉ dùng provenance/miền/giới hạn đã kiểm, không số khớp hoặc lợi ích RCA.
5. Bước tiếp chính xác: đọc results/T-039/bao-cao-sau-tai.md và ban-giao.md; Minh quyết ngoại lệ giữ task qua nhiều phiên hoặc tách với SPEC cụ thể. Nếu được tiếp, kiểm toàn manifest T-039 và các pin input trước dùng; hoàn tất coverage nguồn trước bản ghi, viết oracle literal trước code riêng rồi dựng/đối chiếu theo SPEC nguyên phạm vi. Không cần tải lại nguồn đã hợp lệ. Lệnh đọc: Get-Content -Raw -LiteralPath 'results/T-039/bao-cao-sau-tai.md'.
6. Lệnh cuối sau cập nhật dòng STATE và kiểm toàn diff: py -3 -X utf8 -B results/T-039/finalize_after_acquisition.py verify. Không ghi thêm sau kiểm; nếu cần sửa, phải kiểm lại và giữ lịch sử. Đề xuất commit chưa thực hiện: docs: record T-039 approved sources and feasibility checkpoint.

### Prompt Claude sau thu — Minh chọn gửi hoặc dừng

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-039; tasks/T-039-p5b-online-boutique/SPEC.md; đề xuất tại results/T-039/de-xuat-tach.md; tài liệu hiện hành tại bao-cao-sau-tai.md, authorization-20261016.json và LOG Phiên 2.
- Công đoạn: soát SPEC.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude phản biện kết quả theo lời giao hiện hành. Claude nhận lượt soát đề xuất SPEC này nếu Minh chuyển prompt.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; SPEC.md và LOG.md T-039; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md; LOG T-036 phần phương án gốc; results/T-039/tu-ra-va-kha-thi.md, bao-cao-sau-tai.md, authorization-20261016.json, de-xuat-tach.md, de-xuat-tai.md/json. Bản trước và diff tại results/T-039/runs/tien-kiem-001/.
- Phản biện và phản hồi trước: Không có bản REVIEW trong thư mục T-039 tại lúc soạn prompt; lịch sử lời giao và tài liệu ở LOG T-039. Với đầu vào T-036, lịch sử trong LOG và REVIEW.md của T-036.
- Code và kết quả liên quan: results/T-036/manifest.json, current_run runs/kiem-r1-after-002, code/ và code-hashes.json tại run; src/do_thi_tinh/README.md và code; results/T-035/manifest.json; results/T-003/runs/final-review-003/artifact-manifest.json và nguồn T-008 theo SPEC. Kết quả tại results/T-039/manifest.json, nguon.json, runs/tien-kiem-001/, runs/thu-nguon-001/, runs/khao-sat-nguon-001/ và sources/ theo acquisition.json. Windows/PowerShell; Python -X utf8 -B. Đọc preflight.py trước khi cân nhắc chạy vì script tạo run; lượt soát này không tự cấp quyền tạo run.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC hoặc kết quả từ prompt này; không tải nguồn mới, sửa pin hoặc chạy thực nghiệm.

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

## Phiên 3 — 16/10/2026 — Codex — LEVANMINH — vai trò: người làm T-039

**Nguyên lời Minh:** “làm trong 1 phiên, triển khai luôn giúp tôi nếu không còn vướng mắc nào”. Phân loại EXECUTE: tiếp tục toàn SPEC hiện hành trong phiên, không tự tách hoặc sửa SPEC. Quyền ghi T-039 giữ nguyên. Điều kiện khả thi trước đó là dự toán chưa đo, không phải lỗi khoa học đã chứng minh; sau kiểm nguồn/pin không có mismatch thì thực hiện phần có nguồn hợp lệ. Các OPEN revision/coverage/lineage giữ theo SPEC và báo đúng mức đạt, không suy thành đã xác nhận hoặc bỏ nghĩa vụ. Không xin lại quyền tải đã có; không tải nguồn ngoài danh sách.

**Mở phiên:** đọc lại AGENTS/STATE/toàn SPEC và LOG cuối; kiểm toàn manifest T-039 278/278 và T-036 187/187 khớp; current_run/pin đúng. Giữ toàn nguồn/lượt cũ. Hai nhánh hỗ trợ lập fragment source/backend và Go có provenance/coverage trong parts/; không là phản biện chính thức, không ghi REVIEW/LOG/STATE. Root soát lại, viết oracle trước mã riêng, dựng/đối chiếu và phân tích. Claude phản biện kết quả theo phân công. Nguồn metadata riêng Nezha được Minh duyệt trước; pin shared giữ nguyên.

### Checkpoint tiếp tục và pin lệch — 16/10/2026

Minh yêu cầu tiếp tục checkpoint, kiểm subagent và không suy giảm đầu ra. Hai subagent trước dừng usage, chưa ghi fragment; đã tiếp tục chúng với phạm vi nguồn riêng. Kiểm nguồn 229/229 còn khớp. Phát hiện build.py hiện hành thêm smtp so snapshot pin; manifest T036 chưa đổi. Bằng chứng byte/diff ở results/T-039/runs/pin-lech-001/. Dừng build/compare/validate phụ thuộc; không đổi pin/hash, không rollback hay dừng tiến trình khác. Chỉ tiếp nguồn/fragment/coverage độc lập và trình Minh cách xử lý. Các JSON fragment mới chưa được gọi đã kiểm hợp đồng.


Tự kiểm nguồn checkpoint lần đầu dừng vì locator common istio L3–28 vượt file 27 dòng. Đã đọc file và sửa thành L3–27, giữ bản trước/lượt lỗi tại runs/cho-pin-001/. Không phải lỗi builder; builder chưa chạy. Kiểm lại bằng chế độ resume, không ghi đè snapshot trước.


### Kết thúc checkpoint chờ pin — 16/10/2026

**Quyết định Minh:** nguyên văn “Chờ gói chung và duyệt lại pin”, trả lời câu hỏi xử lý build.py lệch snapshot. Giữ toàn SPEC, không dùng snapshot cũ để dựng/đối chiếu; không sửa/hash lại mã chung hoặc tự chuyển pin.

1. Đã tiếp checkpoint mới nhất; hai subagent trước hết usage chưa ghi fragment đã chạy lại, hoàn tất fragment nguồn/coverage. Root lưu oracle trước transform, phần nguồn chung, registry và phân hoạch toàn tree; kiểm refs/source hash. Chưa hoàn tất T-039: mapping/build/project/compare/phân tích chưa chạy; semantic coverage/merge chưa nghiệm thu. Câu hỏi nguồn chỉ có bản ghi có điều kiện, chưa có độ khớp hoặc lợi ích RCA; RQ3/RQ5/P5b/G3 còn OPEN.
2. Chỉ ghi results/T-039/, nối LOG này và đúng dòng T-039 trong STATE. Không sửa SPEC/WHY/DECISIONS/REVIEW/src/T-035/T-036/platform/task khác. Exact shared-code mismatch lưu ở pin-lech-001; không quy người sửa hoặc quyền duyệt của nhánh khác khi không có bằng chứng.
3. Kiểm nguồn 229 file/metadata còn khớp; fragments chỉ JSON/ID/ref/locator/provenance và oracle-before-transform snapshot; không schema builder validation. Cây phân hoạch đủ, tách read/scan/hash/excluded. Kiểm cuối source set/manifest/phạm vi/prefix/prompt và mismatch expected ở runs/cho-pin-001/final-verification.json; không chạy pilot hoặc thực nghiệm. Source counters và file list ở source-checkpoint.json/manifest. Giờ/RAM máy toàn pipeline vẫn chưa đo; không dùng chi phí scan làm số pipeline.
4. CHẶN hiện tại là mã chung không khớp pin; Minh đã chọn chờ pin mới, owner quyết pin là Minh/gói chung. Phần nguồn còn OPEN gồm deployment/image, instrumentation alias, collector/Node/nguồn phụ và external source; không coi thiếu source là nguyên nhân telemetry. Nơi nhận T-040/P6/P9 và đầu vào cụ thể ở ban-giao.md. Không giảm yêu cầu hoặc tự nghiệm thu đầu ra để xử lý thiếu token/usage.

**Bước tiếp chính xác:** Minh duyệt gói chung và pin; kiểm manifest/code snapshot/current đã đồng nhất rồi rà ảnh hưởng/ghi pin T039 đúng quyền. Sau đó root soát/merge source fragments, oracle, mapping có owner/provenance, dựng/chiếu/đối chiếu toàn graph theo SPEC, lần nhóm chênh lệch và match tương ứng. Lệnh đọc: Get-Content -Raw -LiteralPath 'results/T-039/ban-giao.md'. Không tự mở/gửi chat hay dùng code changed trước Minh duyệt pin.

**Lệnh cuối dự kiến:** py -3 -X utf8 -B results/T-039/checkpoint_sources.py verify. Chỉ kiểm/chốt checkpoint; không chạy shared code. **Đề xuất commit, chưa làm:** docs: checkpoint T-039 source records pending shared contract pin. Chỉ commit/push khi Minh yêu cầu/duyệt riêng.

### Prompt Claude — checkpoint kết quả (Minh chọn gửi hoặc dừng)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-039; tasks/T-039-p5b-online-boutique/SPEC.md; checkpoint results/T-039/runs/cho-pin-001/.
- Công đoạn: soát kết quả.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude phản biện chính thức kết quả.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; SPEC và LOG T-039; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; DT18 và advisor-2026-09-23.md trong docs/reference/sources/; results/T-039/nguon.json, bao-phu-nguon.json và parts/. Diff/bản trước tại runs/trien-khai-001/, pin-lech-001/ và cho-pin-001/.
- Phản biện và phản hồi trước: Không có REVIEW T-039; lịch sử quyền và checkpoint ở LOG Phiên 2–3. Lịch sử T-036 theo LOG/REVIEW của T-036.
- Code và kết quả liên quan: results/T-039/manifest.json; runs/thu-nguon-001/acquisition.json; fixtures/oracle.json; source fragments/coverage trong parts/; results/T-036/manifest.json pin runs/kiem-r1-after-002 và code-hashes.json tại run; metadata nguồn đã thu theo registry. Windows/PowerShell, Python -X utf8 -B; checkpoint_sources.py chỉ tạo checkpoint trong T-039, chưa được tự cấp quyền chạy lại hoặc dựng graph bởi prompt này.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; không ghi REVIEW/LOG/STATE hoặc sửa nguồn/kết quả/pin; không chạy builder/compare/experiment ngoài quyền Minh cấp riêng.

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


Kiểm cuối checkpoint lần đầu báo prompt không khớp khi so byte newline LF với LOG ghi CRLF. Đối chiếu nội dung sau chuẩn hóa newline khớp đúng một lần; sửa checker đọc newline chuẩn, không sửa prompt/LOG để làm kiểm đạt. Lượt lỗi giữ verify-failure-001.json; chưa chạy builder.

Làm rõ kiểm cuối: protected-before.json của lượt triển khai là ảnh byte live lúc mở run, không phải pin đã duyệt. build.py đã có thể đổi đồng thời khi chụp ảnh ấy. Hash chuẩn để kiểm pin luôn lấy manifest/code-hashes/snapshot T036; expected chuẩn và current actual giữ ở pin-lech-001/evidence.json. Kiểm cuối ghi riêng hai tham chiếu, không sửa ảnh cũ hoặc hợp thức hóa hash live. Lệnh chốt cuối: py -3 -X utf8 -B results/T-039/checkpoint_sources.py verify-2; giữ bản kiểm/manifest trước làm rõ.
## Phiên 4 — 16/10/2026 — Codex — LEVANMINH — vai trò: người làm T-039

**Nguyên lời Minh:** “duyệt đề xuất, triển khai t39 ngay để chuyển sang phản biện, không ảnh hưởng đến 38 37 nhé”. Đề xuất đã duyệt là T-039 dùng trực tiếp snapshot T-036 cũ đã ghim, giữ nguyên current shared đang sửa, phạm vi ghi results/T-039/, nối LOG này và đúng dòng T-039 STATE. Đây thay lựa chọn chờ trước đó; không thay hash pin nội dung hoặc sửa SPEC/common code/T-037/T-038. Nạp snapshot nguyên byte từ results/T-036/runs/kiem-r1-after-002/code/, kiểm theo code-hashes trước import; không dùng src live. Tiếp đủ SPEC, không bỏ mapping/analysis/checks để chuyển review.

**Mở phiên:** đọc AGENTS/STATE/SPEC/LOG cuối/bàn giao; kiểm manifest T039 318/318 khớp và bốn snapshot code theo code-hashes khớp. Hai nhánh hỗ trợ nguồn/lineage và mapping-source riêng; không review chính thức, không ghi shared/task khác. Root kiểm/merge, chạy oracle độc lập, dựng/đối chiếu132graph rồi phân tích/tự kiểm/bàn giao. Giữ nguyên dữ liệu/graph trace và mọi lịch sử. Không tải thêm/source ngoài, mở test/raw/Weight/Nodevalues, EC2, commit/push.
**Checkpoint tiếp tục theo lời Minh:** “TIẾP TỤC TỪ CHECK POINT MỚI NHẤT GIÚP TÔI, CÁC SUBAGENT ĐANG CHẠY GIỜ NẾU CÓ, ĐẢM BẢO KẾT QUẢ ĐẦU RA KHÔNG SUY GIẢM”. Hai subagent dừng do hạn mức sau khi đã lưu audit nguồn/lineage/mapping; root tiếp quản phân tích, không bỏ tiêu chí. Canonical thuc-thi-snapshot-004 đã PASS132/132; graph23entity/22edge và68operation/71edge; bản ghi82relation/2logical bindings/53signals, nguồn theo scope đã tải. Đã giữ source audit, oracle, set/members/exclusions, input hash và lịch sử run. Phân tích root tại runs/phan-tich-002:93key chains/53nhóm raw edge bị loại/132ô/7nhóm giải thích. Chưa chốt báo cáo/manifest/STATE ở checkpoint này. Source deployment completeness vẫn OPEN, không đổi thành xác nhận runtime.


### Kết thúc triển khai trong quyền — chuyển Claude phản biện kết quả

**Quyết định của Minh trong phiên:** quyền tải exact list/giữ toàn T039/giữ pin và chứng cứ commit-tree đã nằm ở các mục trước; Phiên4 ghi nguyên lời duyệt snapshot cũ và lời tiếp tục. Chưa ghi DECISIONS/WHY vì lời giao cấm; đề xuất chép quyết định chính thức đúng file/nội dung/lý do/ảnh hưởng ở results/T-039/de-nghi-ghi-quyet-dinh.md, chờ Minh duyệt riêng. Không chọn thiết kế nghiên cứu mới hoặc thay pin nội dung.

1. **Đã làm:** hoàn tất phần triển khai nguồn tham chiếu, mapping, dựng/chiếu và đối chiếu132graph/22opaqueID×2mức×full/N/A hiện hành. Tĩnh23entity/22edge và68operation/71edge,82relation/2logical-instance binding/53signal declarations; numbers từ doi-chieu/tong-hop.json#/record_counts và #/static_counts. Mapping10entity verified,20operation literal verified/32candidate unverified/3SQL unmapped. Kiểm và phân tích7nhóm có match tương ứng, nguồn→record→key→mapping→set,93key chains và53nhóm rawedge exclusions trong runs/phan-tich-002. Báo cáo đọc bằng tiếng Việt tại phan-tich-chenh-lech.md; source audit/lineage và bao-phu-nguon.md tách đọc/scan/excluded toàn274tree entries. Đầu ra sẵn để Claude phản biện, không tự nghiệm thu task.
2. **File thay đổi:** chỉ results/T-039/ (bản ghi/mapping/graph132comparison, nguồn registry/coverage đã khảo sát, báo cáo/script/fixtures/runs/manifest/prompt), nối LOG này và chỉ dòng T039 STATE. Không sửa SPEC/src/T035/T036/T037/T038/WHY/DECISIONS/REVIEW/platform. Nguồn tải còn nguyên; không tải thêm hoặc mở test/raw/Weight/Node values. Git diff toàn repo có thay đổi cũ/phiên khác; không rollback hoặc nhận các thay đổi đó là của T039. Protected observations của lượt004 cho build/compare và manifest T036/T037/T038 đều không đổi; kết quả chốt cuối ở ket-thuc-001/verification.json.
3. **Kiểm đã chạy:** thuc-thi-snapshot-004/verification.json PASS132; oracle literal giữ từ trước transform, owner conflict/unverified/empty denominator/projection; độc lập khóa/tập/giao/hiệu/members/exclusions/mẫu số; permutation và không đổi input; interval và conditional_reference nguyên; canonical allowlist và hash132graph/T035,228registry refs và snapshot4file đã kiểm. Typed trace denominator0/null do unknown, không lấp kiểu từ kiến trúc. Exact archive004 đã giữ; kiểm cuối kiểm archive bằng byte, JSON/provenance/prompt mẫu/hash/LOG append-only/STATEonlyrow rồi lập manifest. Pilot/cost/process input/memory theo run; lượt004 khoảng3,669s/71.557.120byte peak process, không benchmark cô lập hoặc đo giờ công toàn task. Lượt trước/failure giữ nguyên:001 ngắt trước oracle,002 mapping_target do điều phối nhầm level,003 PASS nhưng bindingduplicate/candidate metadata sửa ở004; analysis001 locatorfile không có được từ chối,002 sửa đúng source. Root đã lưu rõ135comparison lịch sử tái dựng là RECONSTRUCTED_NOT_ORIGINAL_BYTES vì runner đầu chỉ ghi canonical, không giả chúng là byte gốc. Không sửa shared để vượt lỗi. Chi phí/tổng byte giữ mọi lượt nằm trong manifest/cost và receipt.
4. **Còn mở và mức trả lời câu nguồn:** cây snapshot được phân hoạch đủ; inventory toàn deployment và ngữ nghĩa runtime chỉ đạt một phần. Chưa có app→build→image digest→deploy→dataset, selected instrumentation naming/Health binding, collector producer Source/Target/Node, tính độc lập metadata ngày hoặc nghĩa host của Node. Source code cho thấy context.TODO và current-span rename, nhưng chưa quy chúng là nguyên nhân dataset. Graph so ở miền dev-adapter có điều kiện, full không cả ngày; tỷ lệ1 phía T chỉ trên cạnh đủ mapping, không telemetrycoverage. T040/P6/P9 nhận đúng evidence/input/owner/cost/limits trong ban-giao.md và de-xuat-bo-sung-nguon.md; chưa thực hiện gói sau. Chưa chọn P6, xác nhận lợi ích RCA, đóng RQ3/RQ5/P5/G3 hoặc mở test. Minh/Claude cần đánh giá phần mô tả đã triển khai và giới hạn nguồn; nguồn mới phải có exactlist/revision/byte được duyệt trước lấy.

**Bước tiếp chính xác:** Minh copy prompt bên dưới (cũng ở results/T-039/prompt-claude.txt) sang Claude để phản biện kết quả; chưa có quyền ghi REVIEW thì trả lời chat. Đọc ban-giao.md, manifest và đầu ra thật; không chỉ LOG. Lệnh kiểm hash rẻ nếu được Minh giao: py -3 -X utf8 -B results/T-039/finish_results.py verify <ten-kiem-moi>. Tái lập runner cần tênrunmới và quyền chạy: py -3 -X utf8 -B results/T-039/execute_pinned.py <ten-run-moi>. Không tự đổi sang live src.

**Lệnh chốt cuối lượt này:** py -3 -X utf8 -B results/T-039/finish_results.py finalize. File kết quả dự kiến runs/ket-thuc-001/verification.json và manifest.json; có lỗi phải giữ lỗi/báo trước kết luận. **Đề xuất commit sau Minh duyệt riêng, chưa làm:** research: implement pinned T039 Online Boutique source graph comparison. Không push/commit bằng quyền triển khai.

### Prompt Claude — soát kết quả (Minh chuyển thủ công)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-039; tasks/T-039-p5b-online-boutique/SPEC.md; results/T-039/.
- Công đoạn: soát kết quả.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude phản biện chính thức kết quả.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; SPEC/LOG T039; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; nguồn DT18 và advisor trong docs/reference/sources/; nguồn và đầu ra tại results/T-039/. Bản trước tại runs/cho-pin-001/, thuc-thi-snapshot-004/before/ và ket-thuc-001/before/.
- Phản biện và phản hồi trước: Chưa có REVIEW T039; lịch sử tự rà/quyền/checkpoint trong LOG T039.
- Code và kết quả liên quan: results/T-039/manifest.json, ban-giao.md, kiem-dung-dan.md, execute_pinned.py; snapshot results/T-036/runs/kiem-r1-after-002/code/ và code-hashes.json; source registry/coverage, fixtures, runs và graph T035 canonical theo manifest. Python3.12, -X utf8 -B; lệnh tái lập/kiểm ghi tại ban-giao.md, chỉ chạy trong quyền Minh giao.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW/LOG/STATE hoặc sửa kết quả/pin; Minh có thể giao riêng bản REVIEW theo AGENTS.

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


### Triển khai gói SMTP V2 — 16/10/2026 — Codex — LEVANMINH — người làm

Minh duyệt nguyên lời: “Duyệt gói SMTP V2, triển khai và kiểm đầy đủ cả ba nhánh theo kế hoạch, làm trong một phiên, giữ nguyên kết quả cũ và không dừng sớm.”
Phạm vi đúng plan.json V2 và before→after đã duyệt. Làm tuần tự cùng phiên, giữ tất cả output/pin cũ; không tự nghiệm thu, không mở test/heldout, commit/push hoặc gửi agent. Đã kiểm hash manifest/code và lưu before; tiến độ/kết quả mới trong results/T-039/runs/doi-chieu-smtp-001/.

### Kết thúc triển khai V2 trong cùng phiên — 16/10/2026 — Codex người làm

1. Đã làm: áp đúng comparator/README, builder T037 không đổi; ghi quyết định/lý do trước dùng, chạy đủ221R1/100SMTPbaseline/29V2/1598FT/1069TT/132OB, rồi tiếp nhận chung cả ba. ỞTT, tách comparator khỏi delta; thêm đúng1key endpoints phía static và1typed unknown exclusion, T/giao giữ nguyên; ởOB toàn output bằng cũ; FT unknown SMTP không khớp trace thiếu channel theo oracle mới.
2. File đổi: đúng plan.json V2: shared compare/README, bốn SPEC/LOG chỉ nối, WHY/DECISIONS chỉ nối, bốn dòng STATE, các bản hiện hành ba nhánh liệt kê và bốn run mới. before giữ mọi byte trước sửa; giữ mọi output/script/fixture/run cũ, kể cả lỗi điều phối. Không sửa nguồn/raw/T035/data khóa hoặc commit/push.
3. Kiểm: full models, source/hash/pin, oracle/independent edges/projection/entity-only/shared signal; mọi graph so tập/members/loại trừ/mẫu số/interval, lặp/đảo/input bất biến. Kết quả chi tiết ở checks/, diff.json, completion.json và final-verification.json của gói chung; manifest finalized sau assertion. Chi phí thực per-process nằm cost.json từng run; tổng bytes gồm mọi lượt được thống kê chung, không là giờ công hay benchmark cô lập. Lượt TTfull1069-001 đã giữ failure: checker ban đầu đòi typed exclusion bằng nhau sau thêm unknown SMTP; đã sửa đúng kiểm phân hoạch theo oracle, không đổi model/comparator/đáp án đủ điều kiện. Các lỗi adapter cũ giữ trong preparation-attempts.json.
4. Điều chưa chắc/cần Minh quyết: triển khai V2 và tiếp nhận kỹ thuật đã đạt, chờ phản biện và Minh nghiệm thu riêng. Runtime/build/instrumentation/deployment lineage, authority/port/TLS/delivery và các OPEN nguồn giữ nguyên. Chưa xác nhận lợi ích RCA/RQ3/RQ5, chọn P6, nghiệm thu task hoặc mở G3/test. Không lấy match/mismatch hoặc synthetic làm bằng chứng nguyên nhân runtime. Phân xử cần build/image/instrumentation/deployment/trace channel có nguồn từ chủ dữ liệu qua Minh; P9 muốn authority/TLS cần schema/telemetry riêng.

Bước tiếp chính xác: đọc results/T-036/runs/doi-chieu-smtp-001/ban-giao.md và final-verification.json; Minh chuyển prompt dưới đây cho Claude nếu chọn, chưa cấp quyền ghi REVIEW. Lệnh cuối: `py -3 -X utf8 -B results/T-036/runs/doi-chieu-smtp-001/complete_adoption.py`. Không có tiến trình cần chờ sau hoàn tất.
Commit đề nghị khi Minh cho phép riêng: `P5b: áp dụng đối chiếu SMTP V2 và tiếp nhận pin chung FT TT OB`.

Prompt trung tính để Minh chuyển thủ công:
```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-039 và results/T-039/runs/doi-chieu-smtp-001/.
- Công đoạn: soát kết quả.
- Gói/cổng: P5, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude phản biện kết quả.
- Tài liệu gốc: AGENTS.md; SPEC/LOG của T036–T039; docs/MRP.md, WHY.md, DECISIONS.md; results/T-038/runs/cap-nhat-goi-smtp-001/package/plan.json; results/T-036/runs/doi-chieu-smtp-001/authorization.json.
- Phản biện và phản hồi trước: Liệt kê các bản REVIEW của từng task được Minh cho phép khi đọc thư mục; không có bản phản biện chính thức riêng của lượt triển khai V2.
- Code và kết quả liên quan: src/do_thi_tinh/; results/T-036/runs/doi-chieu-smtp-001/manifest.json; results/T-039/manifest.json và runs/doi-chieu-smtp-001/{pin.json,checks,diff.json}; Windows Python3.12, -X utf8 -B; môi trường D:/RCA-ext/envs/py312-pin/Scripts/python.exe cho checker có pandas.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa được Minh cho ghi REVIEW hoặc sửa file trong lượt phản biện này.

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


## Ghi nhận phản biện và đóng T-039 — 16/10/2026 — Codex — LEVANMINH

**Vai trò:** Codex phiên độc lập là người phản biện chính thức kết quả thay Claude theo ngoại lệ Minh chỉ định trong lời giao lượt đánh giá. Codex phiên triển khai vẫn là người làm. SPEC giữ nguyên phân công lịch sử; không đổi vai và không dựng một lượt người làm đáp chưa diễn ra.

**Quyền ghi nhận đóng:** sau báo cáo phản biện chỉ đọc, Minh nói nguyên văn: “Duyệt, chấp nhận giới hạn lịch sử và phần nguồn còn OPEN. Ghi nhận phản biện, ngoại lệ phân công và đóng T-039 giúp tôi; chưa duyệt G3 hay mở test.” Ngoại lệ ghi nhận hành chính này cho tạo REVIEW.md, nối DECISIONS/LOG và cập nhật dòng T-039 STATE; không áp quyền người làm hay tự sửa kết quả.

**Quyết định của Minh:** Q-165 tại docs/DECISIONS.md lưu nguyên lời duyệt. Minh chấp nhận R1 về đầu ra lịch sử chỉ còn bản tái dựng và phần nguồn còn OPEN; đóng T-039. Không suy từ việc đóng task thành đạt đầy đủ inventory deployment, xác nhận cơ chế runtime, lợi ích RCA, chọn P6, đóng RQ3/RQ5/P5/G3 hoặc mở test.

1. **Đã làm:** lưu bản phản biện chính thức REVIEW.md theo lượt đã đánh giá trong chat; ghi ngoại lệ phân công kết quả và mốc đóng. Kết quả tham chiếu hiện hành không có lỗi CHẶN mới; R1 KHÔNG CHẶN đã được Minh chấp nhận. Không mở vòng phản biện khác.
2. **File thay đổi:** tạo tasks/T-039-p5b-online-boutique/REVIEW.md; chỉ nối docs/DECISIONS.md và LOG.md này; chỉ thay dòng T-039 trong docs/STATE.md. SPEC, AGENTS/WHY/MRP/LESSONS/review-prompt, code, kết quả, nguồn và manifest giữ nguyên. Không nhận thay đổi có sẵn của workspace là của lượt này; không commit/push.
3. **Kiểm:** lượt phản biện trước đã tính lại độc lập trong bộ nhớ toàn 132 kết quả, khớp nội dung JSON/tập/members/exclusions/mẫu số/interval; hash các manifest và nguồn ghim đạt. Bằng chứng và con trỏ ở REVIEW.md. R1 giữ đúng 3+132 bản tái dựng theo receipt.json, không nhận là byte gốc. Lượt ghi nhận đóng chỉ kiểm bốn file, prefix append-only, đúng một dòng STATE, quyết định/ngoại lệ/giới hạn nhất quán, prompt từ mẫu và hash nguồn bảo vệ. Không chạy thực nghiệm hoặc ghi kết quả mới.
4. **Câu hỏi nguồn còn mở:** inventory toàn deployment mới đạt một phần. Thiếu app→build→image→deploy→dataset, exact library/span naming, producer/schema Source/Target/Node và nguồn datastore/exporter runtime. Owner là tác giả dataset/deployment/collector hoặc maintainer qua Minh; đầu vào/phần phụ thuộc ở de-xuat-bo-sung-nguon.md và REVIEW.md. T-040/P6/P9 nhận những nghĩa vụ này khi được Minh giao riêng. Không gán host từ Node, không gọi metadata là nguồn độc lập hoặc suy thiếu telemetry từ tỷ lệ mapping.

**Bước tiếp chính xác:** không còn công việc được giao trong T-039 sau quyết định đóng. Khi Minh giao bước tiếp theo, đọc docs/STATE.md và docs/DECISIONS.md, rồi REVIEW.md này cùng results/T-039/de-xuat-bo-sung-nguon.md; task sau cần SPEC/quyền tương ứng. Không chạy lại đầu ra hợp lệ hoặc tự mở lại T-039. Prompt bàn giao trung tính từ Prompt chung + Người làm đáp phản biện + G3 được lưu nguyên khối tại REVIEW.md, mục Prompt bàn giao cho người làm; Minh chọn gửi, agent không tự gửi.

**Lệnh cuối của lượt ghi nhận:** `py -3 -X utf8 -B -` — Python inline chỉ đọc kiểm diff/phạm vi bốn file, append-only, dòng STATE, prompt và hash; kết quả trong chat. Không tạo artifact kiểm mới.

**Đề xuất commit, chưa thực hiện:** `docs: record independent review and close T-039 with accepted limits`. Chỉ commit/push khi Minh yêu cầu hoặc duyệt riêng.

**Xác nhận kiểm cuối sau ghi:** PASS. Đúng bốn file; DECISIONS và LOG chỉ nối; STATE chỉ đổi dòng T-039; prompt giữ nguyên các khối mẫu. 13 nguồn bảo vệ không đổi, gồm SPEC/code/các manifest. Kiểm lại toàn 5.667+71+1.006 mục của ba manifest đều khớp; không đổi artifact khoa học. Quyết định Q-165, REVIEW và STATE thống nhất trạng thái đóng có giới hạn, chưa duyệt G3/mở test. Lệnh kiểm cuối: `py -3 -X utf8 -B -` (inline chỉ đọc; kết quả trong chat).
