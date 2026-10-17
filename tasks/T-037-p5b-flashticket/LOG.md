# Nhật ký T-037

Chỉ nối thêm. Phân biệt quyền tạo tài liệu, duyệt triển khai và quyền tải nguồn.

## Phiên 1 — 15/10/2026 — Codex — LeVanMinh — vai trò: người làm tài liệu đề xuất

**Mở phiên:** đọc AGENTS, STATE, mẫu SPEC/LOG, nguồn DT18/cô, MRP phần chi phối, LESSONS, WHY/DECISIONS và phương án P5b/đầu ra T-036 hiện hành. Chưa có SPEC/LOG T-037 trước lượt ghi. Kiểm hash kết quả T-036 và nguồn registry trước dùng đều khớp; không làm lại phần công cụ đã nghiệm thu.

**Công đoạn/mục tiêu:** tạo SPEC ở trạng thái ĐỀ XUẤT/CHỜ PHẢN BIỆN theo quyền chuẩn bị; FlashTicket đầy đủ theo nguồn thiết kế B11–B16; coverage quan hệ/thao tác/địa chỉ, hợp đồng runtime và phần chưa quan sát. Phục vụ DT18-NV2/NV3, cô bước 1, MRP P5 và đầu vào RQ3/RQ5/P6/P9. Chưa có kết quả khảo sát của task.

**Nguyên văn quyền chuẩn bị Minh gửi trong phiên:**

```text
Tôi duyệt ghi gói ba SPEC T-037, T-038, T-039 đã trình, ở trạng thái ĐỀ XUẤT/CHỜ PHẢN BIỆN. Đây là quyền ghi tài liệu chuẩn bị, chưa duyệt triển khai hoặc tải nguồn.
Làm việc tại D:/RCA-flashticket. Đọc AGENTS.md, STATE và nguồn hiện hành trước khi ghi. Giữ nguyên thay đổi có sẵn của người khác.
Phạm vi duyệt gồm đúng chín file đã đề xuất:
- docs/DECISIONS.md
- docs/WHY.md
- docs/STATE.md
- tasks/T-037-p5b-flashticket/SPEC.md
- tasks/T-037-p5b-flashticket/LOG.md
- tasks/T-038-p5b-trainticket/SPEC.md
- tasks/T-038-p5b-trainticket/LOG.md
- tasks/T-039-p5b-online-boutique/SPEC.md
- tasks/T-039-p5b-online-boutique/LOG.md
Ghi nội dung ba SPEC đã trình, bổ sung rõ:
1. Nguồn tải chọn lọc phải được kiểm đủ cho phạm vi khảo sát. Liệt kê phần loại trừ và ảnh hưởng; thiếu nguồn cần thiết thì trình bổ sung, không gọi phần đã tải là inventory toàn snapshot.
2. Giờ công, thời gian máy và dung lượng là dự toán chưa đo. Nêu dung lượng có bao gồm mọi lượt chạy hay chưa; RAM còn chưa đo, cần đo ở lượt thử. Không giảm kiểm để vừa dự toán.
3. Ba task có thể triển khai song song sau khi từng SPEC được Minh duyệt triển khai. Ghim cùng phiên bản hợp đồng/code T-036; mỗi task chỉ ghi phạm vi riêng. Nếu cần đổi hợp đồng chung thì dừng phần phụ thuộc và trình Minh. Cập nhật STATE tuần tự, đọc lại bản mới nhất trước khi sửa đúng dòng task.
Ghi nguồn quyết định trước, rồi SPEC/LOG và STATE. Ngoại lệ Codex phiên sạch phản biện ba SPEC được ghi đúng phạm vi Minh đã yêu cầu; không tự
```

Thông điệp được cung cấp kết thúc tại cụm “không tự”. Không tự khôi phục phần chưa có; giới hạn tự mở/gửi phiên trong SPEC/prompt được dẫn từ AGENTS §9. Các yêu cầu đã đủ rõ để ghi đúng chín file tài liệu, không dùng phần thiếu làm quyền triển khai.


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
6. Lệnh cuối lượt chuẩn bị: py -3 -X utf8 -B - (Python inline kiểm toàn diff/phạm vi chín file, append-only, template/prompt/pin và nguồn bảo vệ, in kết quả trong chat). Lệnh đọc tiếp: Get-Content -LiteralPath 'tasks/T-037-p5b-flashticket/SPEC.md' -Raw.

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

Tự đọc lại câu về phép chiếu và đối chiếu hợp đồng/code T-036 cho thấy cách viết có thể gây hiểu nhầm. Đã làm rõ trong SPEC: giữ nội bộ/span-parent ở records/lớp thao tác, không chiếu thành cạnh phụ thuộc thực thể, báo riêng entity-only/thiếu operation. Đây là sửa cách diễn đạt trong bản đề xuất để khớp hợp đồng đã ghim, không đổi thiết kế hoặc sửa theo một vòng phản biện chính thức.

Các nhánh hỗ trợ đã đọc nguồn và tự kiểm tài liệu; không là lượt phản biện chính thức. Prompt của lượt chuẩn bị vẫn là khối nguyên văn ở trên. Lệnh kiểm sau cùng tiếp tục chỉ đọc template/prompt/pin/hash/diff và toàn phạm vi chín file; chưa triển khai/tải/commit/push.

## Phiên 2 — 15/10/2026 — Codex — LeVanMinh (Windows 11) — vai trò: người làm

**Mở phiên:** EXECUTE có điều kiện theo nguyên văn dưới đây. Claude phản biện kết quả. Tự rà của người làm không thay phản biện chính thức. Trạng thái ĐỀ XUẤT trong SPEC/STATE là lịch sử trước lời giao; không sửa SPEC. Chỉ ghi results/T-037/, nối LOG này và đúng dòng T-037 trong STATE. Giữ thay đổi của các phiên khác.

**Nguyên văn lời giao của Minh:**

```text
Tôi giao bạn triển khai T-037 theo SPEC hiện hành, sau khi tự rà SPEC và kiểm khả năng hoàn thành trong một phiên. Tôi đã đồng ý dừng lượt phản biện ba SPEC T-037/T-038/T-039. Đây là quyền triển khai có điều kiện trong phạm vi dưới đây; chưa duyệt tải nguồn mới.

Làm việc tại D:/RCA-flashticket.\
Task: tasks/T-037-p5b-flashticket/SPEC.md.\
Bạn là Codex người làm. Claude phản biện kết quả. Lượt tự rà này không thay phản biện chính thức.

Trước triển khai:

1. Đọc AGENTS.md, docs/STATE.md, toàn bộ SPEC và mục cuối LOG của T-037. Đọc trực tiếp DT18, hướng dẫn của cô, MRP phần RQ3/RQ5/P5/P6/P9/G3, LESSONS, WHY/DECISIONS liên quan và phương án P5b gốc trong LOG T-036 Phiên 1.
2. Tự rà từ nguồn như lần đầu. Đọc nguồn/code/đầu ra gốc và lập nhận xét trước khi mở kết luận phản biện hoặc phản hồi cũ. Đọc nguyên văn Prompt chung + khối Soát SPEC + khối G3 trong docs/review-prompt.md làm tiêu chí tự rà. Quyền của bạn theo lời giao triển khai này và SPEC, không lấy quyền chỉ đọc của prompt reviewer để thay vai trò.
3. Kiểm manifest và hash đầu vào trước dùng. Pin chung là T-036 được SPEC liệt kê, current_run runs/kiem-r1-after-002; snapshot code tại results/T-036/runs/kiem-r1-after-002/code/, code-hashes.json tại thư mục run. Kiểm mã hiện hành khớp snapshot. Không tự đổi pin hoặc cập nhật hash để hợp thức hóa nguồn lệch.
4. Đối chiếu toàn phạm vi với khả năng xong trong một phiên: đọc nguồn, coverage, dựng graph, oracle, tự kiểm, phân xử và bàn giao. Tách giờ công, giờ máy, RAM và tổng đĩa cho mọi lượt cần giữ. Dự toán chưa đo phải ghi đúng trạng thái. Nếu không vừa một phiên hoặc chưa đủ căn cứ phân xử, trình phương án tách và ảnh hưởng; không tự tách mã task hay giảm tiêu chí.
5. Nguồn FlashTicket chỉ đọc ở D:/Project/flash-ticket-platform. Đọc AGENTS.md, skill .agents/skills/govern-capstone-work/SKILL.md và nguồn bắt buộc trước khảo sát. Đọc các nguồn thiết kế được SPEC giao, ghim revision/hash/dirty state. Không đọc hệ thống cũ hoặc RCA archive. Nếu phát sinh nguồn cần tải, trình nguồn/revision/tệp hoặc nhóm tệp, lý do, phần loại trừ, byte tải, dung lượng giải nén/tổng lưu và đường dẫn ghi; chờ Minh duyệt đúng phần đó.

Nếu tự rà phát hiện lỗi cần sửa SPEC, mâu thuẫn nguồn/quyền hoặc phụ thuộc chặn: dừng phần phụ thuộc; báo vị trí, bằng chứng, hậu quả và đề xuất sửa theo file để Minh quyết. Không tự sửa SPEC. Nếu không có vấn đề và phạm vi khả thi, báo kết quả tự rà rồi tiếp tục triển khai ngay, không hỏi lại quyền đã có. Khi chờ duyệt nguồn, tiếp tục phần độc lập đủ nguồn và nằm trong quyền.

Phạm vi ghi: results/T-037/, nối tasks/T-037-p5b-flashticket/LOG.md và chỉ dòng T-037 trong docs/STATE.md. Ghi nguyên văn lời giao, ngày, thiết bị, vai trò và kết quả tự rà vào LOG. Trạng thái ĐỀ XUẤT trong tài liệu là mốc trước lời giao này; không tự sửa SPEC. Không ghi REVIEW, DECISIONS, WHY, src/, T-035/T-036, repo platform hoặc task khác. Quyết định cần ghi sổ chính thức thì trình nội dung và phạm vi riêng.

Quyết định cần ghi sổ chính thức thì trình nội dung và phạm vi riêng.

Thực hiện đủ SPEC. Inventory phải được kiểm coverage theo toàn phạm vi nguồn ghim; thao tác chỉ lập khi có bằng chứng. Rà đủ HTTP/RPC, DB logic và instance chung, cache, messaging/queue/fan-out/retry, outbox/inbox, callback/query, scheduler, Saga/bù trừ/terminal fence, delivery/check-in, role-grant/projection và hỗ trợ/vận hành. Giữ provenance, owner, điều kiện và địa chỉ tín hiệu. Tên thao tác thiết kế chưa là tên runtime.

Viết oracle độc lập trước phần chuyển đổi riêng. Dùng công cụ T-036 đã ghim; kiểm bản ghi → ID/type/address → graph/phép chiếu/binding/signal. Không tạo operation giả, không nhân metric chung thành bằng chứng độc lập, không nối message/callback từ correlation. Hợp đồng thiếu biểu diễn thì giữ phản ví dụ, dừng phần phụ thuộc và trình ảnh hưởng cả ba nhánh. Không sửa hoặc fork nghĩa hợp đồng chung.

T-038/T-039 có thể chạy song song. Giữ thay đổi của các phiên khác. STATE phải cập nhật tuần tự, đọc lại bản mới nhất ngay trước sửa đúng dòng task; nếu không bảo đảm được thì trình dòng cần cập nhật để Minh điều phối. Đo thời gian/RAM khi không có việc nặng khác chạy đồng thời; không tự dừng tiến trình phiên khác. Thao tác tốn kém theo AGENTS phải báo chi phí và chờ duyệt.

Giữ mọi lượt kể cả lỗi, trung gian, lệnh, môi trường và thời gian. Không mở test/heldout/telemetry thô, chọn P6, làm T-040, bật EC2, commit/push hoặc tự mở/gửi chat.

Cuối phiên kiểm toàn diff và đúng phạm vi; báo phần đạt, câu hỏi nguồn đã trả lời, OPEN và quyết định phụ thuộc. Nối LOG đủ bước tiếp/lệnh cuối, cập nhật đúng dòng STATE. Soạn prompt Claude bằng nguyên văn Prompt chung + khối Soát kết quả + G3 hiện hành; nếu dừng vì cần sửa SPEC thì dùng khối Soát SPEC. Minh chuyển thủ công. Không tự nghiệm thu hoặc đóng task/G3.
```

**Nhận xét độc lập trước lịch sử phản biện:** Đã đọc luật, SPEC/LOG, Prompt chung + Soát SPEC + G3 nguyên văn; DT18/cô, MRP RQ3/RQ5/P5/P6/P9/G3, LESSONS, WHY-52/53, quyết định trực tiếp và phương án gốc P5b. Nhóm hỗ trợ chỉ thu thập nguồn/kiểm hash, không là review chính thức. Đọc platform AGENTS và skill govern-capstone-work đầy đủ cùng reference authority/gates, DT18 và roles trước khảo sát. Phân loại phần mô hình là CANDIDATE từ thiết kế; quyền triển khai là USER_CONFIRMED; tên/span/queue/instance runtime và hiệu quả RCA là OPEN.

Tự rà chưa thấy lỗi cần sửa SPEC/hợp đồng để bắt đầu. B11-C §1 và chú thích sơ đồ giao endpoint/topic/sequence cho B13/B14; vì vậy mũi tên TKT→BKG ở sơ đồ không được dùng làm chứng cứ lời gọi trực tiếp. Giữ đối chiếu mức trách nhiệm trong coverage; đường bù trừ cụ thể theo hợp đồng là Payment→Booking. Alias Gateway ở sơ đồ B14 là cổng thanh toán theo create/IPN/refund, không tự gộp với API Gateway. Các câu DRAFT trong lịch sử không nâng realm/stack thành runtime đã kiểm.

**Pin:** results/T-037/runs/tu-ra-001/preflight.json: pin đúng created_utc/current_run; T-036 187/187 entries và T-035 5.667/5.667 entries khớp hash/bytes; mã hiện hành khớp snapshot. Không đổi pin/hash. Kết quả hash là FACT; thời gian preflight không là benchmark do có thu thập nguồn chỉ đọc đồng thời. Không dùng các entry lịch sử ngoài input thực của T-037 để tự chặn task.

**Khả thi một phiên, dự toán chưa đo:** phạm vi năm nguồn chính 2.237 dòng/192.902 byte và 10 sơ đồ dẫn trực tiếp 743 dòng/23.050 byte. B12 chủ yếu là từ điển storage, không phải 467 operation; coverage phải giữ từng vùng và ánh xạ đúng datastore, không tạo operation từ tên cột. Tổng giờ công 5–8 giờ gồm nguồn/coverage 2–3, bản ghi/oracle 1,5–2,5, graph/tự kiểm/phân xử 1–1,5 và bàn giao 0,5–1. Hai phần hỗ trợ độc lập giảm thời gian chờ, không là reviewer. Giờ máy dự toán 5–15 phút, mỗi lượt dưới 5 phút; peak RAM dự toán dưới 0,5 GiB; cần đo pilot khi không có việc nặng khác. Dự toán kết quả tối đa 200 MB cho 10 lượt gồm lượt lỗi/chạy lại/bản cần giữ; không sao 374 MB graph T-035/T-036 vào từng run. Dữ liệu vào đã có trên đĩa; không tải/giải nén. Đây là ước lượng CANDIDATE, sai nếu nguồn phát sinh quan hệ/biểu diễn chưa giải được; khi đó dừng phần phụ thuộc và trình, không giảm tiêu chí.

**Tiến độ:** đã lưu preflight và oracle literal results/T-037/oracle.json trước phần chuyển đổi riêng. Bước tiếp: lập bản ghi có nguồn + coverage; chỉ gọi build/project/compare từ snapshot đã ghim bằng runner T-037. Không chạy checker T-036 vì checker đó ghi thư mục của T-036. Chưa mở kết luận REVIEW cũ tại thời điểm ghi nhận xét này.

**Lệnh đầu đã chạy:** Get-Content luật/STATE/SPEC/LOG và nguồn; py -3 -X utf8 -B results/T-037/preflight.py. Một lệnh đọc gộp gọi nhầm docs/WHY.md/DECISIONS.md ở cwd platform báo không có file; đã đọc đúng bản RCA, không tạo file hay dùng bản khác thay thế. Một số lượt output bị cắt đã đọc lại phần cần; không coi output bị cắt là đã đọc đủ.

### Tiếp tục qua 16/10/2026 — chặn biểu diễn SMTP

Đã mở REVIEW/mốc đóng T-036 sau khi lưu nhận xét độc lập. Phản biện công cụ cũ không nêu SMTP, không thay phản ví dụ nguồn mới. B13 L199, B14 L82 và B14-03 L9–12 xác định Ticket gửi SMTP. Hợp đồng T-036 §2 và build.py L10–11/L161–169 chỉ nhận channel gọi http/rpc/internal; không có SMTP. Dừng graph/phép chiếu và mọi kết luận đầy đủ phụ thuộc; không sửa/fork T-036, không chuyển SMTP thành HTTP/RPC/internal. Hai nhánh nguồn tiếp tục lưu đúng phần độc lập, không chạy converter.

Tự phát hiện lỗi oracle ban đầu: oracle.json#/http_edges/5 xếp Ticket→SMTP vào HTTP, trái nguồn. Bản đó giữ nguyên lịch sử và bị vô hiệu cho dựng graph đầy đủ; counterexample-smtp.json ghi oracle đúng trước runner phản ví dụ. Chưa có converter T-037 hoặc graph được sửa để theo oracle sai.

Lượt smtp-001 chạy hai build calls rồi lỗi ở thao tác đo RAM bằng Windows API (ctypes chưa khai argtypes), không phải lỗi khác của T-036. Giữ input/registry/oracle, failure.txt và code-used.py; sửa riêng phép đo trong runner T-037 và chạy tên mới, không ghi đè lượt lỗi. Trước chạy đã lấy mẫu CPU 1 giây: không process vượt 0,25 CPU-second; helper chỉ đọc/ghi JSON nhẹ. Không dừng tiến trình phiên khác.

Đính chính chép lời giao ở trên: giữa đoạn “Không ghi REVIEW...” và “Thực hiện đủ SPEC” có thêm một đoạn lặp “Quyết định cần ghi sổ chính thức thì trình nội dung và phạm vi riêng.” do chép lặp của agent. Đoạn lặp không thuộc một yêu cầu riêng của Minh, không thêm quyền; nguyên câu đã nằm đúng trong đoạn phạm vi ghi trước đó. Giữ lịch sử append-only của LOG và ghi rõ lỗi chép này.


### Bản chép chuẩn lời giao — thay bản chép có đoạn lặp, giữ nguyên lịch sử

```text
Tôi giao bạn triển khai T-037 theo SPEC hiện hành, sau khi tự rà SPEC và kiểm khả năng hoàn thành trong một phiên. Tôi đã đồng ý dừng lượt phản biện ba SPEC T-037/T-038/T-039. Đây là quyền triển khai có điều kiện trong phạm vi dưới đây; chưa duyệt tải nguồn mới.

Làm việc tại D:/RCA-flashticket.\
Task: tasks/T-037-p5b-flashticket/SPEC.md.\
Bạn là Codex người làm. Claude phản biện kết quả. Lượt tự rà này không thay phản biện chính thức.

Trước triển khai:

1. Đọc AGENTS.md, docs/STATE.md, toàn bộ SPEC và mục cuối LOG của T-037. Đọc trực tiếp DT18, hướng dẫn của cô, MRP phần RQ3/RQ5/P5/P6/P9/G3, LESSONS, WHY/DECISIONS liên quan và phương án P5b gốc trong LOG T-036 Phiên 1.
2. Tự rà từ nguồn như lần đầu. Đọc nguồn/code/đầu ra gốc và lập nhận xét trước khi mở kết luận phản biện hoặc phản hồi cũ. Đọc nguyên văn Prompt chung + khối Soát SPEC + khối G3 trong docs/review-prompt.md làm tiêu chí tự rà. Quyền của bạn theo lời giao triển khai này và SPEC, không lấy quyền chỉ đọc của prompt reviewer để thay vai trò.
3. Kiểm manifest và hash đầu vào trước dùng. Pin chung là T-036 được SPEC liệt kê, current_run runs/kiem-r1-after-002; snapshot code tại results/T-036/runs/kiem-r1-after-002/code/, code-hashes.json tại thư mục run. Kiểm mã hiện hành khớp snapshot. Không tự đổi pin hoặc cập nhật hash để hợp thức hóa nguồn lệch.
4. Đối chiếu toàn phạm vi với khả năng xong trong một phiên: đọc nguồn, coverage, dựng graph, oracle, tự kiểm, phân xử và bàn giao. Tách giờ công, giờ máy, RAM và tổng đĩa cho mọi lượt cần giữ. Dự toán chưa đo phải ghi đúng trạng thái. Nếu không vừa một phiên hoặc chưa đủ căn cứ phân xử, trình phương án tách và ảnh hưởng; không tự tách mã task hay giảm tiêu chí.
5. Nguồn FlashTicket chỉ đọc ở D:/Project/flash-ticket-platform. Đọc AGENTS.md, skill .agents/skills/govern-capstone-work/SKILL.md và nguồn bắt buộc trước khảo sát. Đọc các nguồn thiết kế được SPEC giao, ghim revision/hash/dirty state. Không đọc hệ thống cũ hoặc RCA archive. Nếu phát sinh nguồn cần tải, trình nguồn/revision/tệp hoặc nhóm tệp, lý do, phần loại trừ, byte tải, dung lượng giải nén/tổng lưu và đường dẫn ghi; chờ Minh duyệt đúng phần đó.

Nếu tự rà phát hiện lỗi cần sửa SPEC, mâu thuẫn nguồn/quyền hoặc phụ thuộc chặn: dừng phần phụ thuộc; báo vị trí, bằng chứng, hậu quả và đề xuất sửa theo file để Minh quyết. Không tự sửa SPEC. Nếu không có vấn đề và phạm vi khả thi, báo kết quả tự rà rồi tiếp tục triển khai ngay, không hỏi lại quyền đã có. Khi chờ duyệt nguồn, tiếp tục phần độc lập đủ nguồn và nằm trong quyền.

Phạm vi ghi: results/T-037/, nối tasks/T-037-p5b-flashticket/LOG.md và chỉ dòng T-037 trong docs/STATE.md. Ghi nguyên văn lời giao, ngày, thiết bị, vai trò và kết quả tự rà vào LOG. Trạng thái ĐỀ XUẤT trong tài liệu là mốc trước lời giao này; không tự sửa SPEC. Không ghi REVIEW, DECISIONS, WHY, src/, T-035/T-036, repo platform hoặc task khác. Quyết định cần ghi sổ chính thức thì trình nội dung và phạm vi riêng.

Thực hiện đủ SPEC. Inventory phải được kiểm coverage theo toàn phạm vi nguồn ghim; thao tác chỉ lập khi có bằng chứng. Rà đủ HTTP/RPC, DB logic và instance chung, cache, messaging/queue/fan-out/retry, outbox/inbox, callback/query, scheduler, Saga/bù trừ/terminal fence, delivery/check-in, role-grant/projection và hỗ trợ/vận hành. Giữ provenance, owner, điều kiện và địa chỉ tín hiệu. Tên thao tác thiết kế chưa là tên runtime.

Viết oracle độc lập trước phần chuyển đổi riêng. Dùng công cụ T-036 đã ghim; kiểm bản ghi → ID/type/address → graph/phép chiếu/binding/signal. Không tạo operation giả, không nhân metric chung thành bằng chứng độc lập, không nối message/callback từ correlation. Hợp đồng thiếu biểu diễn thì giữ phản ví dụ, dừng phần phụ thuộc và trình ảnh hưởng cả ba nhánh. Không sửa hoặc fork nghĩa hợp đồng chung.

T-038/T-039 có thể chạy song song. Giữ thay đổi của các phiên khác. STATE phải cập nhật tuần tự, đọc lại bản mới nhất ngay trước sửa đúng dòng task; nếu không bảo đảm được thì trình dòng cần cập nhật để Minh điều phối. Đo thời gian/RAM khi không có việc nặng khác chạy đồng thời; không tự dừng tiến trình phiên khác. Thao tác tốn kém theo AGENTS phải báo chi phí và chờ duyệt.

Giữ mọi lượt kể cả lỗi, trung gian, lệnh, môi trường và thời gian. Không mở test/heldout/telemetry thô, chọn P6, làm T-040, bật EC2, commit/push hoặc tự mở/gửi chat.

Cuối phiên kiểm toàn diff và đúng phạm vi; báo phần đạt, câu hỏi nguồn đã trả lời, OPEN và quyết định phụ thuộc. Nối LOG đủ bước tiếp/lệnh cuối, cập nhật đúng dòng STATE. Soạn prompt Claude bằng nguyên văn Prompt chung + khối Soát kết quả + G3 hiện hành; nếu dừng vì cần sửa SPEC thì dùng khối Soát SPEC. Minh chuyển thủ công. Không tự nghiệm thu hoặc đóng task/G3.
```


### Kết thúc phiên — 16/10/2026 — dừng phần phụ thuộc, chưa hoàn thành T037

1. Đã tự rà nguồn/pin và khảo sát nguồn độc lập; lưu 24 nguồn/snapshot, 347 đơn vị coverage dự thảo và bản ghi một phần ({'entities': 32, 'operations': 60, 'relations': 79, 'resource_bindings': 14, 'signals': 58}). Chặn SMTP được tái lập2/2 ở runs/smtp-002/result.json. Không có graph/phép chiếu toàn phạm vi được dựng, không gọi task đạt. Năm nguồn/diagram/readme được đọc; content DDL/schema/realm dẫn xuất chỉ metadata, source closure chưa hoàn tất.
2. Phạm vi thay đổi: results/T-037/, LOG này chỉ nối thêm, đúng dòng T037 trong STATE. Không sửa SPEC/REVIEW/WHY/DECISIONS/src/T035/T036/platform/task khác. Oracle HTTP/SMTP ban đầu sai được giữ và vô hiệu, lượt đo lỗi được giữ. Bản chép chuẩn lời giao ở trên sửa lỗi chép lặp bằng cách nối thêm. Không tải, mở test/heldout/telemetry, chọn P6/làm T040/EC2, commit/push hoặc tự gửi chat.
3. Kiểm input/snapshot/common code trước và cuối đều khớp; partial-record checks 24/24, không thay kiểm graph. CPU sample không việc nặng khác; memory32.768.000byte và thời gian hai build calls chỉ cho phản ví dụ nhỏ. Full cost dự toán chưa đo còn điều kiện; không dùng sample để nhận khả thi full task khi contract đang chặn. Kiểm diff/phạm vi cuối bằng verify-final.py sau ghi, xem runs/ket-phien-001/final-verification.json.
4. Phần nguồn đã trả lời: B12 giữ DB logic/instance chung; thao tác là tên thiết kế; B13/B14 đòi SMTP và pin hiện hành không nhận transport này. Chưa trả lời lợi ích RCA/RQ3/RQ5, chưa nhận full coverage/model hoặc G3. OPEN cần Minh quyết gói sửa chung/pin cho ba nhánh theo ban-giao.md; queue/scope/runtime names/deployment/telemetry và đầy đủ fixture còn phải xác minh. Không tự mở lại T036 đã đóng, không tự nghiệm thu T037. Đây là phần hỗ trợ mô hình/P9, không là cơ chế đã xác nhận.

**Bước tiếp chính xác:** Minh xem results/T-037/ban-giao.md mục phạm vi sửa và kiem-dung-dan.md. Chờ duyệt gói xử lý hợp đồng/pin chung; không chạy graph từ bản ghi hiện tại. Sau quyền phù hợp, viết oracle đúng đầy đủ trước converter, đọc/ghim nguồn dẫn xuất cần thiết, hoàn tất coverage từng requirement→record→ID/type/address→graph/chiếu/binding/signal và fixture runtime tổng hợp; chạy dưới tên run mới. Không tự đổi SPEC/pin hoặc giảm tiêu chí. Quyết định triển khai có điều kiện cần lưu DECISIONS được trình nguyên ý trong ban-giao.md, chưa ghi do ngoài quyền.

**Lệnh cuối dự kiến/được giao chạy trong phiên:** py -3 -X utf8 -B results/T-037/verify-final.py. Lệnh đó chỉ kiểm artifact/diff/hash/prefix/phạm vi. Đề xuất commit sau khi Minh giải quyết chặn và duyệt: `docs: preserve T-037 design survey and SMTP contract counterexample`; chưa commit/push.

**Prompt Claude — soát kết quả một phần (Minh chuyển thủ công):**

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-037; D:/RCA-flashticket/tasks/T-037-p5b-flashticket/SPEC.md và LOG.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm, Claude người phản biện chính thức kết quả.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; tasks/T-037-p5b-flashticket/SPEC.md và LOG.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; results/T-037/nguon.json và các nguồn/snapshot được liệt kê.
- Phản biện và phản hồi trước: Không có REVIEW kết quả T-037; lời giao và lịch sử chuẩn bị tại LOG Phiên1–2; T-036 có tasks/T-036-p5b-hop-dong-chung/REVIEW.md và LOG.md.
- Code và kết quả liên quan: results/T-037/manifest.json, ban-ghi.json, bao-phu-nguon.md/json, kiem-dung-dan.md, ban-giao.md, hop-dong-runtime.md, counterexample-smtp.json, oracle.json và runs/; pin T-036 runs/kiem-r1-after-002/code/ cùng code-hashes.json, manifest.json và đầu vào SPEC; Windows11/Python3.12; py -3 -X utf8 -B results/T-037/check-counterexample.py <tên run mới> chỉ khi được Minh giao chạy; không chạy checker T036 vào thư mục T036.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC, kết quả, code hoặc nguồn chung. Minh chuyển prompt thủ công.

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


## Phiên 3 — 16/10/2026 — Codex — LeVanMinh (Windows 11) — người làm

**Nguyên văn lời Minh mới:** “Vậy sửa hỗ trợ SMTP và kiểm lại, giữ nguyên T-038/T-039 đang chạy. Sau khi kiểm đạt thì tiếp tục T-037, không tự đổi pin của hai nhánh kia.” Trước đó Minh duyệt mục1 hỗ trợ SMTP; câu hỏi về kiểm/đồng bộ không là quyền sửa hai SPEC. Phạm vi thực hiện: sửa src/do_thi_tinh/build.py thêm channel smtp cho quan hệ gọi; lưu oracle/kiểm/hồi quy/snapshot hợp đồng bổ sung và đầu ra trong results/T-037/, nối LOG này và chỉ dòng T037 trong STATE. Không sửa T036 snapshot/manifest hoặc T038/T039. T037 dùng pin gốc cộng bổ sung SMTP đã duyệt, không giả vờ bản sửa khớp hash pin cũ.

**Mở phiên/tự rà:** đọc lại AGENTS, STATE, SPEC/LOG T037 và các nguồn chi phối; kiểm manifest T036/T037, code hiện hành và nguồn platform trước dùng tại runs/tiep-smtp-001/preflight.json. Giữ các output đã hợp lệ, chỉ bổ sung phần thiếu. Nguồn thiết kế FORMATION/CANDIDATE; DT18/cô và MRP vẫn yêu cầu mapping đủ3tínhiệu, không xác nhận runtime/lợi ích hoặc chọn P6. Hai phần hỗ trợ thu nguồn/soạn phép kiểm trong phạm vi riêng, không là reviewer chính thức. Không tải nguồn, không mở test/heldout/telemetry thật.

**Chi phí còn lại — dự toán chưa đo:** 3–5 giờ công gồm coverage/đọc nguồn dẫn xuất, bản ghi/oracle/graph/fixtures và bàn giao; máy2–10phút, peakRAM dưới512MiB; tổng output cả lịch sử+lỗi/10lượt dự kiến dưới200MB. Đo sau khi không việc nặng khác; không suy giờ công từ giờ máy, không chạy quá1giờ hoặc thay tiêu chí cho vừa thời gian. Phần SMTP kiểm đạt mới chạy chuyển đổi T037. Bản đồ ảnh hưởng: source build.py; dẫn xuất trong T037; không đổi quyết định P6/khóa G3, không ghi DECISIONS/WHY từ quyền cũ. Nội dung sổ chính thức cần trình riêng cuối phiên; quyền SMTP mới được lưu nguyên văn ở đây và authorization run.

### Checkpoint tiếp tục — 16/10/2026

Minh yêu cầu “TIẾP TỤC TỪ CHECK POINT MỚI NHẤT GIÚP TÔI, CÁC SUBAGENT ĐANG CHẠY GIỜ NẾU CÓ, ĐẢM BẢO KẾT QUẢ ĐẦU RA KHÔNG SUY GIẢM”. Hai helper từng errored usage. Helper kiểm đã lưu oracle/runner nên người làm đọc lại và chạy; helper nguồn được tiếp tục, ghi xong đúng2file rồi ngừng ghi. Không đổi vai trò hoặc tiêu chí. Lệnh ghi quá dài của helper trước đó bị CreateProcess từ chối trước tạo file; đã chia lượt ghi nhỏ, không mất/lược coverage.

SMTP đã đạt100/100, regression221/221/312graph/156projection; outputs cũ so toàn nội dung giữ nguyên. Run results/T037/runs/smtp-regression-001, không ghi T036. Bản build.py sửa đúng2guard smtp theo oracle trước checker. Snapshot/manifestT036, pinSPEC38/39 giữ nguyên. T037 ghi pin nền + delta đã duyệt; không cập nhật hash để giả vờ current khớp nền.

Đọc/crosscheck thêm bảy SQL definitions, Mongo schema/bootstrap và realm candidate local; không chạy database/Keycloak hoặc xem dữ liệu thật. Assembly2 có34nguồn,652đơnvị nguồn,32entities/65ops/115relations/14bindings/153signals. Các số chưa là runtime/coverage hiệu quả. Địa chỉ là schema/design; runtime names null. Đã sửa locator cache L52→L47 đúng source trong bản tích hợp, giữ bản partial trước đó.

Graph-001 có1594đạt/1lỗi harness: kiểm “mọi exclusion phải missing address” quên rằng data relations ngoài miền messaging được loại đúng outside_relation_domain. Đã giữ run/code/input, sửa kiểm chỉ xét messaging; graph-002 đạt1595/1595. Không sửa T036/comparator theo lỗi kiểm này. fixtures-runtime.json v1 có sender fan-out là Payment nên có một cùng-owner; chưa chạy converter, đã giữ v1 và tạo v2 đúng Event→3consumer trước graph run. Oracle-v2 có trường lý do missing mapping chưa khớp đầu target của fixtureconsume; viết oracle-v3 đúng unmapped:target và để checker đọc literal này, không đổi chính sách mapping hay fixture để khớp output. Lịch sử v1/v2/v3 và mọi run được giữ.

Tiếp theo: hoàn thiện coverage/ledger cùng kết quả graph; kiểm lại nguồn gốc và phạm vi đầy đủ; xuất graph/bàn giao/prompt/manifest cuối. Không gọi số kiểmthamchiếu là bằng chứng mọi lập luận nguồn đã đúng hoặc đồ thị có ích choRCA.


### Kết thúc Phiên 3 — 16/10/2026 — Codex người làm — LeVanMinh

1. Đã sửa hỗ trợ SMTP theo Minh giao, kiểm đạt100/100 và regression221/221,312graph/156projection; giữ nguyên nội dung221check records và10artifact cũ. Tiếp tục T037: đọc/ghim34nguồn (5tài liệu chính,10diagram,4README,10baseline definitions,5nguồn quản trị),652đơnvị nguồn; lưu32thực thể/65tên thao tác/115quan hệ nguồn thành72cạnh thực thể/55cạnh thao tác/17cạnh chiếu,14binding/153địa chỉ tín hiệu. Full graph/fixture kiểm đạt1598/1598 ở runs/graph-003/result.json. Số kiểm nhiều gồm references; không coi nó là bằng chứng mọi lập luận khoa học hoặc runtime đã đúng. Source quote/schema đã kiểm riêng, raw arrow OPEN được giữ.
2. File thay đổi đúng phần đã giao: src/do_thi_tinh/build.py chỉ2guardthêmsmtp; results/T037/ (graph, nguồn/coverage/bản ghi/địa chỉ/hợp đồng bổ sung/runtime/kiểm/bàn giao/manifest và mọi run); LOG chỉ nối thêm và đúng dòngT037 trong STATE. Không sửa T036snapshot/manifest, T038/T039SPEC/pin/code/kết quả; không sửa SPEC T037/REVIEW/WHY/DECISIONS hoặc platform. Mã actual không giả khớp pin cũ: T037 ghi rõ nền + deltaSMTP đã duyệt, snapshot ở graph-003/code. Bản trước và runlỗi giữ nguyên.
3. Tất cả phép kiểm hiện hành đạt. Máy: SMTP+regression 27.669s, peakchild 115253248byte; graphhiệnhành 1.252s, peak 81518592byte. Tổngđĩa/cácfilehash tại manifest, gồm lượt lỗi/lặp/bản trước. Giờcông là dự toán, không lấy walltime qua ngắt usage làm thời gian làm liên tục. Kiểmcuối bằng verify-complete.py đối chiếu toànowned diff/phạmvi/hash/pin/LOGprefix/STATErow/prompt; kết quảởruns/ket-phien-002/final-verification.json. Không tải/giải nén/EC2/commit/push/mởtest/heldout/telemetry thô hoặc tự gửichat.
4. Đạt phần mô hình nguồnthiếtkế và bàn giao cóđiềukiện để chờClaude phảnbiện; không tự nghiệmthu. Câu nguồn được trả lời: giữowner/DBlogic-instance/quan hệ có type/address/operationname thiết kế vàSMTP; mọi khoảngtrốngquantrọng có nguồnowner/input. Chưa xácnhậnruntime, nhánh đãchạy, tínhiệuđủ hoặc lợiíchRCA. OPEN7nhóm tại bao-phu-nguon.json#/open_items; P9cần config/build/export/names/queue/scope/clock/permissions, P6cần thiết kế/phép dùngcạnh/binding trên dev, T040cần tổnghợp khácpin theo quyềnriêng; RQ3/RQ5/G3 giữmở. Không có quyếtđịnhnghiêncứumới hoặc giảmtiêuchí. QuyếtđịnhSMTP/giữnguyên2nhánh cần ghi sổchínhthức được trìnhnộidung/phạmvi ởban-giao.md, chưa ghi ngoài quyền.

**Bước tiếp chính xác:** Minh chuyển promptClaude dưới đây (hoặc results/T037/prompt-claude.txt) để soát kết quả trên nguồn/đầu ra thật. Chưa có quyền ghi REVIEW; reviewer mặc định chỉđọc/trảlờichat, Minh quyết phạmvi lượtghi. Không chạy lại graph hoặc đổi pin hai nhánh khi chưa có lý do/quyền. Đọc results/T037/manifest.json và kiểm hash trước dùng; xem bao-phu-nguon.json, do-thi/, hop-dong-runtime.md và ban-giao.md. Finding là đầu vào, Minh quyết sửa.

**Lệnh cuối của lượt:** & 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B results/T-037/verify-complete.py. Lệnh chỉ kiểm toàn artifact/phạmvi và ghi báo cáo cuối trong T037, không thựcnghiệmmới. **Đềxuất nội dungcommit, chưa thực hiện:** `feat: support SMTP in sourced graphs and model FlashTicket design`. Chỉ commit/push khi Minhduyệt riêng.

**Prompt Claude — Soát kết quả + G3, Minh chuyển thủ công:**

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-037; D:/RCA-flashticket/tasks/T-037-p5b-flashticket/SPEC.md và LOG.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm, Claude người phản biện chính thức kết quả.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; SPEC/LOG T-037; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; results/T-037/nguon.json cùng các nguồn và snapshot được liệt kê; nguồn platform theo luật và skill govern-capstone-work.
- Phản biện và phản hồi trước: Chưa có bản phản biện kết quả T-037. Lịch sử chuẩn bị/triển khai và quyền sửa tại tasks/T-037-p5b-flashticket/LOG.md. T-036 có REVIEW.md và LOG.md trong tasks/T-036-p5b-hop-dong-chung/.
- Code và kết quả liên quan: results/T-037/manifest.json, ban-ghi.json, bao-phu-nguon.md/json, do-thi/, dia-chi-tin-hieu.json, hop-dong-runtime.md, hop-dong-smtp.md, kiem-dung-dan.md, ban-giao.md và runs/; oracle/fixtures tại các file manifest liệt kê. Pin nền T-036 runs/kiem-r1-after-002/code và code-hashes.json; mã T-037 thực dùng tại runs/graph-003/code. Diff tại runs/ket-phien-002/changes.diff. Windows11, Python3.12 môi trường D:/RCA-ext/envs/py312-pin; lệnh build-check.py hoặc smtp-check.py chỉ khi Minh giao chạy trong phạm vi kết quả T-037; không chạy checker T036 ghi vào T036.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC, code, kết quả hoặc nguồn chung. Minh chuyển prompt thủ công.

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

### Tự kiểm cuối — phân biệt manifest nền với mã shared đã duyệt sửa

verify-complete lần đầu đạt76/77; cờ còn lại do phép kiểm đòi mọi187entryT036 vẫnkhớp, nhưng chính src/do_thi_tinh/build.py là một entry và đã được Minh duyệt sửa2guardSMTP. Không sửa manifest/pin cũ để làm số khớp. Giữ báo cáo/manifest/verifier lần đầu tại ket-phien-002/*attempt-001*. Phép kiểm cuối phân biệt186entry không đổi và đúng1delta build được duyệt; snapshot code nền + chính file manifest vẫn khớp hash cũ, current build phải khớp đúng2thayđổi và snapshotT037. Đây là sửa điều kiện kiểm cho phạm vi được duyệt, không đổi outputgraph hay hợpđồng ngoàiSMTP. T038/T039 vẫn giữpin và snapshot nền; bảnmanifest nền khi kiểm currentcode phải báo delta này chứ không gọi toàn187entrycurrentunchanged. Lệnh cuối tiếp tục verify-complete.py; xem báo cáo cuối cùng trước dùng.

### Biên nhận kiểm cuối Phiên 3

Kiểm toàn diff và phạm vi đạt 77/77. Đối chiếu manifest hiện hành có 268 entry đều khớp; tổng lưu thực 79.162.838 byte tại thời điểm kiểm, gồm mọi lượt lỗi, lượt lặp, snapshot và metadata. Tổng có thể đổi vài byte khi nối biên nhận này; manifest và báo cáo cuối được tính lại sau ghi. Không có thay đổi tracked ngoài phạm vi sở hữu. Pin/SPEC T038/T039 và snapshot/manifest T036 giữ nguyên; entry current build trong manifest nền được báo đúng là delta SMTP đã duyệt, không tự ghi lại hash nền.

Lệnh cuối thực hiện sau biên nhận: & 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B results/T-037/verify-complete.py. File kết quả cuối: results/T-037/runs/ket-phien-002/final-verification.json. Bàn giao, OPEN và prompt hiện hành ở các mục kết thúc Phiên3 phía trên; chỉ Minh chuyển prompt và quyết nghiệm thu.


### Triển khai gói SMTP V2 — 16/10/2026 — Codex — LEVANMINH — người làm

Minh duyệt nguyên lời: “Duyệt gói SMTP V2, triển khai và kiểm đầy đủ cả ba nhánh theo kế hoạch, làm trong một phiên, giữ nguyên kết quả cũ và không dừng sớm.”
Phạm vi đúng plan.json V2 và before→after đã duyệt. Làm tuần tự cùng phiên, giữ tất cả output/pin cũ; không tự nghiệm thu, không mở test/heldout, commit/push hoặc gửi agent. Đã kiểm hash manifest/code và lưu before; tiến độ/kết quả mới trong results/T-037/runs/doi-chieu-smtp-001/.

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
- Task hoặc đề xuất: T-037 và results/T-037/runs/doi-chieu-smtp-001/.
- Công đoạn: soát kết quả.
- Gói/cổng: P5, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude phản biện kết quả.
- Tài liệu gốc: AGENTS.md; SPEC/LOG của T036–T039; docs/MRP.md, WHY.md, DECISIONS.md; results/T-038/runs/cap-nhat-goi-smtp-001/package/plan.json; results/T-036/runs/doi-chieu-smtp-001/authorization.json.
- Phản biện và phản hồi trước: Liệt kê các bản REVIEW của từng task được Minh cho phép khi đọc thư mục; không có bản phản biện chính thức riêng của lượt triển khai V2.
- Code và kết quả liên quan: src/do_thi_tinh/; results/T-036/runs/doi-chieu-smtp-001/manifest.json; results/T-037/manifest.json và runs/doi-chieu-smtp-001/{pin.json,checks,diff.json}; Windows Python3.12, -X utf8 -B; môi trường D:/RCA-ext/envs/py312-pin/Scripts/python.exe cho checker có pandas.
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


## Phiên 4 — 16/10/2026 — Codex phiên sạch — LeVanMinh — người phản biện; ghi nhận ngoại lệ và đóng theo Minh duyệt

**Mở lượt ghi / vai trò:** lượt soát kết quả độc lập trước đó chỉ đọc và trả lời chat. Minh chỉ định Codex phiên sạch làm người phản biện chính thức kết quả thay Claude; Codex phiên triển khai vẫn là người làm. Đây là ngoại lệ ở công đoạn kết quả, khác ngoại lệ soát SPEC cũ. Ghi mốc này theo quyền đóng bốn file, không nhận vai trò người làm hoặc sửa phân công lịch sử trong SPEC.

**Quyết định của Minh trong phiên:** lời giao ban đầu ghi “Minh chỉ định Codex phiên mới hoàn toàn này làm người phản biện chính thức kết quả thay Claude.” Sau báo cáo, Minh yêu cầu nguyên văn: “Đồng ý dừng phản biện, nghiệm thu và đóng T-037 giúp tôi. Lưu bản phản biện và ghi nhận ngoại lệ phân công, giữ nguyên các OPEN, chưa commit/push.” Khi trình thêm nghĩa vụ ghi LOG, Minh xác nhận “Duyệt đúng bốn file”: tạo REVIEW.md, nối DECISIONS.md và LOG này, chỉ cập nhật dòng T-037 trong STATE. Ngoại lệ và quyết định đóng ghi riêng tại Q-166/Q-167; không bổ sung lựa chọn khoa học vào lời Minh.

**Nguồn và phản biện:** REVIEW.md lưu bản soát nguồn/đầu ra gốc trước lịch sử, code/pin/diff được đối chiếu, các kiểm độc lập, giới hạn và prompt chuẩn. Không phát hiện lỗi đáng kể còn chưa xử lý trong mô hình thiết kế FlashTicket và tiếp nhận SMTP V2. R1 và các lỗi oracle/harness lịch sử được kiểm lại, không kế thừa kết luận chỉ từ LOG. Không có REVIEW kết quả T-037 trước lượt lưu này.

**Kết thúc lượt ghi nhận đóng:**
1. Đã lưu bản phản biện, ghi ngoại lệ kết quả vào sổ quyết định và LOG, ghi Minh nghiệm thu/đóng T-037; STATE chuyển xong đúng dòng task. Phạm vi đạt: mô hình nguồn thiết kế và bàn giao có điều kiện của P5; không đóng toàn P5b hoặc RQ3/RQ5/G3.
2. File đổi đúng gói duyệt: tasks/T-037-p5b-flashticket/REVIEW.md; docs/DECISIONS.md; LOG này; chỉ dòng T-037 trong docs/STATE.md. SPEC, code, mọi kết quả/manifest, registry, coverage và các OPEN giữ nguyên. Các metadata chờ phản biện/hash LOG trước đóng trong manifest là snapshot triển khai lịch sử; mốc nghiệm thu hiện hành ở Q-167/REVIEW/mục này/STATE, không gán lại pin hoặc sửa output cũ.
3. Kiểm phản biện: hash, dựng/chiếu độc lập trong bộ nhớ, sáu fixture trace, bốn fixture đối chiếu, trích dẫn nguồn, SQL dictionary, coverage và địa chỉ tín hiệu khớp; chi tiết/lệnh/nguồn số ở REVIEW. Trước lưu kiểm lại 312 mục T-037 và 71 mục pin V2 vẫn khớp. Lượt ghi kiểm toàn diff/phạm vi, nối thêm, đúng dòng STATE, mẫu prompt và các đầu ra được bảo vệ; kết quả cuối báo trong chat. Không chạy lại checker có ghi file, không tạo run.
4. Không còn phản đối chưa xử lý ảnh hưởng phạm vi nghiệm thu đã nêu. Giữ bảy nhóm OPEN tại results/T-037/bao-phu-nguon.json#/open_items cùng owner/input/effect: queue/scope, runtime operation, deployment/resource, config/identity, pipeline, access/UI/retention và RCA. P9 cần build/image/config/export và telemetry thực; P6 cần phép dùng cạnh/binding và kiểm dev; T-040 tổng hợp/P7/P10 theo SPEC/quyền sau. Không xác nhận runtime hay lợi ích RCA, không chọn P6 hoặc mở test. Phần nên đưa vào báo cáo: nguồn mô hình, DB logic/instance chung, nghĩa messaging và giới hạn dữ liệu runtime.

**Bước tiếp chính xác:** đọc docs/DECISIONS.md Q-166/Q-167, dòng T-037 trong STATE, REVIEW.md và results/T-037/ban-giao.md trước khi trình việc tiếp. Lệnh đọc: Get-Content -LiteralPath 'tasks/T-037-p5b-flashticket/REVIEW.md' -Raw. T-037 đã đóng; không chạy lại graph hoặc mở lượt phản biện từ prompt lịch sử. Mọi phần tổng hợp/runtime/thiết kế còn thiếu theo nhiệm vụ và quyền riêng.

**Prompt bàn giao:** nguyên văn Prompt chung + Người làm đáp phản biện + G3 nằm trong REVIEW.md trước bảng phản hồi, giữ vai trò và mặc định chỉ đọc. Minh chọn dùng hoặc dừng; không tự gửi. Việc đóng không yêu cầu tự phát sinh lượt đáp.

**Lệnh cuối của lượt:** py -3 -X utf8 -B - (Python inline chỉ đọc, kiểm diff/phạm vi bốn file, nối thêm DECISIONS/LOG, đúng dòng STATE, prompt và hash kết quả; in trong chat). Không có tiến trình thực nghiệm cần chờ. Chưa commit/push theo Minh yêu cầu; nội dung commit dự kiến nếu được giao riêng: docs: record T-037 independent review and acceptance.
