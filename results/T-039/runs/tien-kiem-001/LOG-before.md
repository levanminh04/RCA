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
