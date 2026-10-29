# Nhật ký T-042

Chỉ người làm ghi file này. Chỉ ghi thêm, không sửa mục cũ. Codex là người làm; Claude là người phản biện chính thức.

---

## Phiên 1 — 23/10/2026 — Codex — Windows 11, máy local — vai trò: người làm

**Mở phiên:** đã đọc AGENTS, STATE, mẫu SPEC và nguồn trực tiếp trước khi soạn đề xuất trong chat. Chưa có thư mục T-042 trước lượt tạo. Phiên này lưu SPEC được duyệt và bàn giao; không triển khai nghiên cứu.

**Công đoạn và mục tiêu nguồn:** tạo hồ sơ task đối chiếu baseline Nezha-OB với số công bố, thuộc P3–P4; chuẩn bị căn cứ cho P6/P7. Minh cho phép phiên Codex mới tự soát trước rồi triển khai nếu không có điểm bất hợp lý. Đây chưa phải xác nhận nguyên nhân chênh lệch hoặc tự soát khoa học của phiên triển khai.

**Quyết định của Minh trong phiên:**
- “Dùng T-042 cho đối chiếu; đổi tham chiếu hạ tầng ở lượt được duyệt sau”.
- “duyệt tạo spec, sau đó tạo 1 prompt cho phiên codex mới. yêu cầu phiên này tự soát spec trước, nếu có điểm bất hợp lý thì dừng, nếu không thì triển khai task luôn.”
- Minh duyệt SPEC ngày 23/10/2026. Đã nối lời duyệt và phạm vi vào D:/RCA-flashticket/docs/DECISIONS.md, Q-189. Tự soát của Codex không thay phản biện chính thức của Claude. SPEC đã lưu thì khóa; không tự sửa khi thấy bất hợp lý.
- Tham chiếu T-042 hạ tầng trong D:/RCA-flashticket/docs/KE-HOACH-GIAI-DOAN-TOI.md chưa đổi. Chờ lượt duyệt riêng, không tự cấp số khác. Nên thông báo cho Claude nếu đang dùng kế hoạch; chưa gửi tin.

**Diễn biến:**
- Sau khi hai nhánh đọc nguồn T-026 và SimpleRCA trả kết quả, người làm tích hợp vào bản đề xuất trong chat; các nhận định nguồn vẫn phải kiểm trên file thật trước sử dụng. Các trợ lý cùng Codex không phải phản biện chính thức.
- Lượt tạo đã kiểm danh sách task, quyền ghi, mẫu và nguồn quyết định; lưu dấu vết trạng thái ban đầu để kiểm phần thay đổi của lượt này. Kho đã có nhiều thay đổi sẵn, không coi chúng là sản phẩm T-042.
- Nối Q-189; tạo SPEC từ bản được duyệt, chỉ cập nhật phần hành chính theo lời Minh: trạng thái, quyền có điều kiện và nơi đặt prompt. Không thay thiết kế khoa học, chi phí hay phạm vi phép kiểm.
- Tạo LOG và hai prompt: prompt triển khai cho phiên Codex mới; prompt Claude soát SPEC theo mẫu để Minh tùy chọn chuyển.
- Chưa ghi WHY, chưa tạo results/T-042, chưa chạy thực nghiệm, chưa tải nguồn, chưa mở test/dữ liệu khóa và chưa commit/push.

**Checkpoint khi ngữ cảnh được nén:** đang hoàn tất đúng lượt tạo hồ sơ, không bắt đầu nghiên cứu. SPEC và Q-189 đã có; LOG đang lưu checkpoint và bàn giao; dòng STATE sẽ đồng bộ rồi kiểm đủ bốn file. Sau khi kiểm xong, Minh mở phiên Codex mới bằng prompt bên dưới. Phiên mới phải kiểm nguồn, hash, hợp đồng và tính hợp lý từ đầu theo yêu cầu tự soát; không coi việc kiểm tài liệu bàn giao ở đây là tự soát đã đạt.

**Tự soát và phản biện:** lượt này chỉ kiểm tính nhất quán hồ sơ được lưu. Chưa có phản biện chính thức của Claude. Chưa có kết quả T-042; các giả thuyết vẫn CANDIDATE/OPEN như SPEC. Không biến duyệt thử thành xác nhận giả thuyết.

**Phạm vi lượt tạo:** đúng bốn file: SPEC.md và LOG.md của task; nối DECISIONS.md; dòng T-042 trong STATE.md và bỏ câu “Không còn task đang mở” đã hết hiệu lực khi thêm task. WHY và kế hoạch hạ tầng giữ nguyên. Không sửa code hoặc kết quả cũ.

**Bước tiếp theo chính xác:**
1. Phiên Codex mới đọc D:/RCA-flashticket/AGENTS.md, docs/STATE.md, SPEC.md và mục cuối LOG.md của task; kiểm Q-189 và nguồn trực tiếp trong SPEC.
2. Tự soát trước mọi cài đặt/thực nghiệm. Có điểm bất hợp lý thì dừng triển khai, nối LOG bằng chứng/hậu quả/đề xuất sửa và báo Minh; không sửa SPEC. Không có thì ghi kết quả tự soát vào LOG và triển khai ngay trong phạm vi đã duyệt.
3. Sau tự soát đạt, nối đúng nội dung WHY được SPEC cho phép trước khi dùng lựa chọn trong kết quả; tiến hành phần A trước phần B. Lệnh bộ bọc mới chỉ ghi sau khi cài và kiểm; chưa có lệnh thực nghiệm T-042 để chạy trong lượt tạo.
4. Kiểm lại file thật và manifest; dùng lại đầu ra hợp lệ. Không mở test, tải thêm, tự mở rộng phạm vi hay commit/push. Kết thúc triển khai thì cập nhật STATE chờ phản biện và soạn prompt Claude theo công đoạn thực tế.

## Prompt phiên Codex mới

```text
Tôi là Minh. Tôi giao Codex tiếp tục T-042 tại D:/RCA-flashticket với vai trò người làm; Claude là người phản biện.

Tôi đã duyệt tạo SPEC và cho phép phiên này tự soát trước: nếu có điểm bất hợp lý thì dừng báo tôi; nếu không có thì triển khai task luôn trong phạm vi đã duyệt. Không cần hỏi lại quyền chạy sau khi tự soát đạt. Quyết định được lưu tại D:/RCA-flashticket/docs/DECISIONS.md, Q-189. Đây không phải quyền tự sửa SPEC.

Đọc theo thứ tự:
1. D:/RCA-flashticket/AGENTS.md và D:/RCA-flashticket/docs/STATE.md.
2. D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md và mục cuối LOG.md cùng thư mục.
3. Các nguồn trực tiếp chi phối được SPEC liệt kê: DT18, hướng dẫn của cô, MRP P3/P4/P7, WHY, DECISIONS, LESSONS; sau đó bài, code, manifest và kết quả thật. Không dùng tóm tắt trong chat/LOG hoặc nhận định khảo sát thay cho bằng chứng.

Tự soát với tư cách người làm trước khi viết code hay chạy thực nghiệm: mục tiêu nguồn có được bao phủ đúng không; giả thuyết và phép kiểm có phân xử được không; code/revision/giấy phép/đầu vào có đúng không; nguồn và manifest có hợp lệ không; quyền dev/test, phạm vi ghi, phụ thuộc, chi phí và tiêu chí xong có mâu thuẫn hoặc thiếu sót không. Không mặc định SPEC đúng vì tôi đã duyệt.

Nếu phát hiện điểm bất hợp lý, dừng triển khai; ghi bằng chứng, hậu quả và đề xuất sửa cụ thể theo file vào LOG và báo trong chat để tôi quyết. Không tự sửa SPEC hoặc lách bằng một nhánh chạy khác. OPEN đã được mô tả đúng không tự là lỗi; nhưng phải kiểm cách giới hạn đó ảnh hưởng câu hỏi nguồn.

Nếu không phát hiện điểm bất hợp lý, ghi kết quả tự soát vào LOG rồi triển khai ngay các bước trong SPEC. Ghi mục WHY đã được duyệt trước khi dùng lựa chọn trong kết quả; kiểm nguồn và dùng lại đầu ra hợp lệ, không làm lại các lượt đã đủ bằng chứng. Lưu tiến độ, mọi lượt kể cả lượt hỏng, kiểm trung gian và kết luận theo từng giả thuyết. Chỉ ghi trong phạm vi SPEC; giữ nguyên code/kết quả cũ và các thay đổi không thuộc task.

Chỉ dùng Nezha-OB dev được allowlist cho phép. Không mở test/giữ ngoài, không tải thêm, không sửa code dùng chung, không tự mở rộng task hoặc vượt ngân sách; không commit/push. Nếu cần vượt phạm vi thì dừng và trình tôi.

T-042 đã dành cho đối chiếu. Các tham chiếu T-042 hạ tầng trong D:/RCA-flashticket/docs/KE-HOACH-GIAI-DOAN-TOI.md chưa được sửa; không lấy chúng làm quyền chạy hạ tầng hoặc tự đổi mã. Không tự gửi tin cho Claude.

Tự soát này không thay phản biện chính thức của Claude. Khi xong, kiểm toàn bộ diff và file set, báo bốn mục theo AGENTS §7, ghi LOG đủ bàn giao, cập nhật dòng T-042 trong STATE thành chờ phản biện và soạn prompt cho Claude theo mẫu. Không tự nghiệm thu hoặc đóng task.
```

## Prompt Claude

Prompt này chỉ dùng nếu Minh chọn gửi Claude soát SPEC. Không phải yêu cầu phải chờ Claude trước quyền triển khai có điều kiện của phiên Codex mới. Chưa có quyền ghi REVIEW; lượt soát này chỉ trả lời chat.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-042; D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md.
- Công đoạn: soát SPEC.
- Gói/cổng: P3–P4, trọng tâm G2.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md và LOG.md cùng thư mục; D:/RCA-flashticket/docs/KHAO-SAT-SAU-K1-K6.md; các nguồn trực tiếp liệt kê trong SPEC; bản mới chưa commit, không có diff từ commit gốc của task.
- Phản biện và phản hồi trước: không có.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-008/, results/T-017/, results/T-026/, results/T-034/ và các nguồn được SPEC dẫn trong cùng repo; revision và manifest tại mục Đầu vào của SPEC; chưa có code hoặc kết quả thực nghiệm T-042.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; không tạo/sửa/xóa file, không chạy thực nghiệm hoặc tải thêm.

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

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và quy tắc đơn giản trên cùng đồ thị dùng khi đánh giá tác dụng của việc dùng quan hệ; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```

## Kết thúc phiên 1 — tạo hồ sơ và bàn giao

1. **Đã làm gì:** lưu SPEC được Minh duyệt; ghi Q-189 và đồng bộ dòng T-042; soạn prompt phiên Codex mới tự soát rồi triển khai có điều kiện, cùng prompt Claude soát SPEC theo mẫu. Đã ghi checkpoint khi ngữ cảnh nén.
2. **File đã thay đổi:** D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md; LOG.md cùng thư mục; D:/RCA-flashticket/docs/DECISIONS.md; D:/RCA-flashticket/docs/STATE.md. Chỉ bốn file thuộc lượt này. Chưa ghi WHY, chưa sửa kế hoạch hạ tầng.
3. **Kiểm tra đã chạy và kết quả:** kiểm toàn bộ nội dung SPEC và LOG; SPEC đủ đề mục mẫu, giữ nội dung khoa học bản đã duyệt. Kiểm theo byte xác nhận phần DECISIONS trước lượt này giữ nguyên, chỉ nối Q-189; hoàn nguyên trong bộ nhớ đúng thay đổi STATE cho hash trùng bản đầu lượt. AGENTS, WHY, kế hoạch hạ tầng và mẫu review không đổi. Hai prompt trong LOG khớp bản đã soạn; prompt Claude lấy nguyên văn ba khối mẫu, chỉ điền thông tin trung tính. Thư mục task chỉ có SPEC/LOG, chưa có results/T-042. Kiểm khoảng trắng và git diff --check đạt; trạng thái Git ngoài bốn file có cùng dấu vết với đầu lượt. Kiểm này không xác nhận nội dung các thay đổi có sẵn hoặc thay cho kiểm manifest nghiên cứu ở phiên sau.
   - Các thao tác kiểm chỉ đọc từng gặp đầu ra trạng thái quá dài bị cắt và lỗi mã hóa stdout; đã đổi sang kết quả tổng hợp và xử lý Unicode, kiểm lại thành công. Không phát sinh đầu ra thực nghiệm hoặc file tạm.
4. **Điều chưa chắc hoặc cần Minh quyết:** hồ sơ task và bàn giao đã có; câu hỏi vì sao baseline thấp vẫn chưa được T-042 trả lời. Chưa có tự soát khoa học của phiên triển khai hoặc phản biện chính thức của Claude. Code/config sinh bảng công bố, tác động từng quy ước và mức tương đương dữ liệu còn cần kiểm theo SPEC; các quyết định P6/P7 phụ thuộc phần đó. Mã T-042 đã thuộc đối chiếu; bốn tham chiếu hạ tầng trong kế hoạch còn chờ lượt sửa được duyệt riêng. Nên báo Claude để tránh nhầm mã nếu đang dùng kế hoạch; chưa gửi và không cần Claude duyệt lại quyết định mã. Không tự đóng task hoặc mở test.
5. **Bước tiếp theo chính xác:** Minh mở phiên Codex mới tại D:/RCA-flashticket, dán mục “Prompt phiên Codex mới” ở trên. Phiên mới đọc AGENTS, STATE, SPEC, mục cuối LOG và nguồn trực tiếp; tự soát với vai trò người làm. Có điểm bất hợp lý thì dừng, trình bằng chứng và đề xuất; không có thì ghi WHY trong phạm vi và triển khai phần A rồi B. Không cần chờ Claude soát SPEC để thực hiện quyền có điều kiện. Prompt Claude trong LOG dành cho Minh tùy chọn chuyển, không tự gửi.
6. **Lệnh cuối cùng của lượt kiểm hồ sơ:** `git diff --check -- docs/STATE.md docs/DECISIONS.md`, chạy tại D:/RCA-flashticket; kết quả không báo lỗi. Lệnh này kiểm định dạng tài liệu, không chạy nghiên cứu.

**Đề xuất nội dung commit khi Minh yêu cầu:** `docs: add T-042 baseline comparison spec and conditional handoff`. Chưa commit/push.



---

## Phiên 2 — 24/10/2026 — Codex — Windows 11, máy local — vai trò: người làm

**Mở phiên:** Minh giao tiếp tục T-042 theo Q-189: tự soát trước, có bất hợp lý thì dừng trình; không có thì triển khai ngay trong SPEC. Đây không phải quyền sửa SPEC. Claude giữ vai trò phản biện chính thức; chưa gửi tin hoặc mở lượt phản biện.

**Phân loại:** EXECUTE có điều kiện. FACT: STATE, SPEC và LOG thống nhất vai trò và trạng thái chưa chạy; Q-189 đã lưu lời duyệt. USER_CONFIRMED: chỉ Nezha-OB dev allowlist; không tải thêm, sửa code dùng chung, mở test/giữ ngoài hoặc commit/push. Các giả thuyết nguyên nhân vẫn CANDIDATE/OPEN trước kiểm.

**Thao tác đầu phiên:** đã đọc AGENTS, STATE, toàn bộ SPEC và mục cuối LOG, DT18, hướng dẫn giảng viên và các phần MRP trực tiếp chi phối. Đã lưu dấu vết trạng thái Git và hash sáu file quản trị/task trong bộ nhớ để đối chiếu cuối lượt; repo có sẵn thay đổi ngoài task, giữ nguyên. Chưa có results/T-042. Đang đọc WHY/DECISIONS/LESSONS và kiểm nguồn thật trước code/thực nghiệm. Một trợ lý Codex chỉ đọc provenance/code SimpleRCA, không ghi file, không thay phản biện Claude. Không có quyết định nghiên cứu mới trong lời giao cần nối DECISIONS.

### Tự soát trước triển khai — đạt trong phạm vi SPEC

**Kết luận người làm:** chưa phát hiện bất hợp lý chặn triển khai T-042 trong phạm vi được duyệt. Không sửa SPEC. Nguồn DT18-NV3, hướng dẫn cô §1 và MRP RQ1/RQ2/P3/P4/P7 đòi kiểm độ lệch và chuỗi cơ chế; SPEC bao phủ đối chiếu hiện có và phép phân xử M4, đồng thời yêu cầu bàn giao pipeline tác giả chưa định danh. Phần đó còn OPEN và chặn tuyên bố tái lập bảng/chọn baseline P7 theo số công bố; không bị coi là đã hoàn thành bởi 2×2.

**Bằng chứng tự soát trực tiếp:**
- Q-189/STATE/SPEC/LOG thống nhất quyền có điều kiện, vai trò và phạm vi; chỉ dòng T-042 của STATE được cập nhật. Chỉ nối đúng mục WHY đã duyệt, không có quyền sửa SPEC/src/data/kết quả cũ. Không có quyền phản biện chính thức mới cho Claude.
- T-026: 36 file cấu hình/allowlist/nhãn/bảng chấm/code cần dùng khớp source_hashes/handoff; 11 source code ngoài repo khớp external-code-manifest; 154/154 nguồn dev (1.041.219.665 byte) và 248/248 bản ghi chấm khớp hash. Lượt hash toàn nguồn/bản ghi mất 9,293 giây, chỉ đọc byte để hash, không đưa giá trị telemetry ra ngoài bộ đọc cửa sổ. 22 ca và nguồn đúng kích thước, không mở test.
- T-008: 16/16 nguồn trong run-001/manifest khớp. Đã đọc trực tiếp PDF Nezha trang 8–9: service-level AS@k, 56 fault OB và Table 3; không lấy published-reference làm thay thân bài.
- T-034: ban-do-g2.json, bang-baseline.json, goi-g2.md, hai-phep-kiem.json khớp manifest-cuoi-007. 14 nguồn T-032/T-034 được dẫn trực tiếp cho phần cần dùng cũng khớp. Không dùng cham-a.md T-026 làm nguồn số vì bản sau sửa có lịch sử riêng.
- Trợ lý Codex chỉ đọc kiểm SimpleRCA: 74/74 file download-manifest, sáu tài liệu inventory, 37/37 file artifact khớp; 21/21 vendor file giống orig. Ba entrypoint là NezhaRCA; orig Python>=3.13/sáu parquet, fusion/luật metric/trace khác M4 và fallback dùng parent-child. Ba tree không có LICENSE/COPYING; chỉ đọc, không sao chép. Root đã đọc trực tiếp FSE §3.1.2 và Table 2. Chỗ ngưỡng/đơn vị alert chưa khóa cho phép phép phân xử 2×2, không xác nhận program sinh 0,91.
- Trợ lý Codex chỉ đọc kiểm MicroRank: official.py khớp PROVENANCE; core manifest, micro-analysis summary/script và 88 observed của 22 ca × 4 nhánh khớp chuỗi hash. Không thiếu nguồn EC2 trong chuỗi đó. Clone đầy đủ ở scratchpad trong PROVENANCE không còn; chỉ đối chiếu phần lõi được trích và bằng chứng đã lưu, không nhận là đã kiểm trực tiếp toàn preprocessing/entrypoint MicroRank tác giả hoặc chương trình Table 3. Giới hạn toàn pipeline đã thuộc phần OPEN/bàn giao của SPEC.
- Môi trường nguồn hiện có D:/RCA-ext/envs/T-014-main/Scripts/python.exe: Python 3.12.10; numpy 1.26.4, pandas 2.2.3, psutil 6.1.1. Dùng -B; không cài/tải. Config M4 có sẵn sigma/P95 và events/channels; giữ nguyên trace/log/tập ứng viên/cửa sổ. Chưa chạy phương pháp. Các tổng hợp cũ thiếu ngưỡng/phiếu đầy đủ cho 2×2 nên cần thu đúng trung gian trong lượt cho phép; sẽ dùng lại bảng/chains hợp lệ, không chạy lại MicroRank.
- Dự toán SPEC 20–60 phút máy, RAM<2GB/đĩa<300MB còn là chưa kiểm; pilot không nhãn trước lô. Không có lý do dự kiến vượt một giờ cho một lượt. Không chạy công việc nặng song song khi đo.

**Lỗi lệnh chỉ đọc:** một lệnh đọc JSON dùng encoding mặc định gặp UnicodeDecodeError; đã đọc lại UTF-8 thành công. Một tìm kiếm glob PowerShell trỏ tên không tồn tại; đã đọc đúng manifest bằng đường dẫn thật. Không phát sinh lượt thực nghiệm hoặc file ngoài LOG.

**Bước tiếp:** nối WHY-54 đúng nội dung SPEC, lập nguồn/kế hoạch trước chạy, cài bộ bọc trong results/T-042/scripts và kiểm fixture/đầu vào trước evaluator. Mọi phát hiện cần patch ngoài quyền hoặc thay SPEC sẽ dừng nhánh và trình Minh; không âm thầm chữa trong bộ bọc.

### Nguồn, bộ bọc và pilot không nhãn

- Đã nối WHY-54 đúng nội dung được duyệt trước khi dùng lựa chọn. Bộ kiểm nguồn tạo nguon.json và ke-hoach-chay.json trước mọi lượt phương pháp; không tải thêm. Dữ liệu chỉ hash theo allowlist, không trả raw.
- Đã xác minh khả năng dùng lại SimpleRCA: hai summary T-032 khớp nguồn nhưng chỉ có root/above-root; full capture cũ ở EC2 không có local. Vì thiếu ngưỡng/count/vote/full ranking, phát lại S0 trong đúng quyền SPEC; không lấy lại EC2. Summary S1 được giữ làm kiểm đối chiếu lịch sử.
- Bộ bọc mới nằm đúng results/T-042/scripts. Fixture 22/22 đạt: selector trước I/O, timestamp/biên/ns-us, mapping165, hàng lặp, NaN/thiếu/zero/rỗng, công thức, hòa, hoán vị và locator không vào core. Lượt fixture: runs/fixtures-001/checks.json.
- Pilot không nhãn chọn ca nhỏ nhất theo tổng byte nguồn, không theo nhãn: runs/pilot-001. Bốn nhánh hoàn tất; S0 khớp nguyên trạng thái/điểm/tập ứng viên/hạng/nhóm hòa T-026; tính độc lập ngưỡng/count/vote/score đạt. Audit CSV cửa sổ độc lập đạt; không lưu payload. Có kiểm hoán vị trên dữ liệu pilot thật và đối chứng N1–N2 thật: metric ordinal 2/3; trace/log chia tại trung điểm thời gian N, không xác nhận N sạch.
- Chi phí pilot: cost.json ghi 5,679 giây, RSS đo tại biên ca 221,148 MiB (có thể bỏ đỉnh ngắn); chiếu tuyến tính 22 ca 124,940 giây. Đây chưa là cận trên. Không dự kiến vượt ngân sách; triển khai đủ 22 ca, dùng lại bốn diagnosis pilot đã ghi và kiểm hash. Nhãn chưa được evaluator đọc; chưa chọn nhánh thắng.

**Lệnh tiếp:** D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B results/T-042/scripts/chay_dev.py full full-001. Lượt này ghi mọi ca/nhánh ngay sau khi hoàn tất và tiến độ; gặp lỗi nguồn/khớp/invariant thì dừng giữ lượt hỏng.

**Bảo toàn phiên bản code trong lúc chạy:** trong khi worker full-001 đã import các hàm kiểm, người làm nối hàm evaluator vào kiem_doc_lap.py. Không đổi các hàm arithmetic/window_audit/rank_metrics đã chạy. Để không mất provenance theo hash đầu lượt, đã dựng lại đúng byte phiên bản trước phần nối và lưu runs/full-001/source-kiem_doc_lap-at-start.py; hash khớp config.json của lượt và pilot. Không cần phát lại lượt hợp lệ vì worker dùng module đã nạp và phần phép tính không đổi. Một lệnh kiểm snapshot đầu tiên dùng khóa POSIX trong bảng đường dẫn Windows gặp KeyError; đã sửa cách đọc khóa và kiểm hash thành công. Giữ nguyên config/lịch sử, không cập nhật hash cũ thành hash mới.

### Chốt đầu ra trước evaluator

Full-001 hoàn tất và chốt diagnosis-list.json lúc 2026-10-23T18:09:50Z (24/10/2026 giờ Việt Nam). Đủ 88 bản ghi = 22 ca × 4 nhánh, gồm 4 bản ghi pilot được dùng lại theo hash. Cả 22 S0 khớp trạng thái/score/candidate/order/tie T-026, 22 audit đầu vào độc lập và 88 tính phiếu độc lập đều đạt. Tổng wall full 161,136 giây, RSS lấy mẫu lớn nhất 329,781 MiB; pilot 5,679 giây riêng, không cộng chi phí pilot thêm vào từng bản ghi dùng lại. Chưa đọc giá trị nhãn trong evaluator T-042. Từ mốc này không thay/chọn lại diagnosis vì số chấm. Bước sau chỉ nối nhãn dev sau kiểm lại toàn bộ hash, chấm P3 và tính độc lập, đối chiếu S1 lịch sử.

### Phân tích sau khi nối nhãn và tự kiểm đầu ra

- Evaluator đọc đủ 88 diagnosis đã chốt và kiểm hash rồi mới nối nhãn dev. P3 và phép tính độc lập khớp 88/88; S0/S1 khớp 44 khoảng hạng root lịch sử. Có đủ 22 ca, 13 ô, trạng thái/ứng viên/hòa và hiệu ứng ghép cặp. Kết quả tại runs/evaluate-001/summary.json.
- S0/S1/S2/S3 Hit@1 lần lượt 0,318182 / 0,242424 / 0,181818 / 0,204545; MRR 0,537542 / 0,500295 / 0,417776 / 0,409994. Không chọn nhánh thắng hoặc đổi baseline. Báo tăng/giữ/giảm từng ca và từng ô, gồm ca đúng bị hỏng. Cận cohort41/56 chỉ có điều kiện; không mở test.
- Tổng hợp trực tiếp ngưỡng/count cho 3.630 kênh–ca: P95 thấp hơn3.030, bằng600, không cao hơn; count tăng1.202, giữ2.428; metric events1.201→3.058. Trace/log giữ nguyên. Đã đọc chuỗi root–competitor cho ca cải thiện và ca hỏng, gồm cặp trong cùng ô. Bằng chứng ở runs/reuse-audit-001/m4-mechanism.json và diagnosis từng ca.
- Kiểm tái lập chuỗi MicroRank: manifest-review→manifest-final→core/script/summary→88 observed,352 metadata,22 case analysis;465 mục khớp. Dùng lại, không chạy MicroRank. Đã đọc cả cặp đúng/sai sau cùng can thiệp trong cùng ô, không dựng main Hit1 đúng vốn không có. Phân biệt can thiệp repo với program Table3 chưa định danh.
- Đã tạo doi-chieu.md, phan-xu.json, bao-cao.md. Khảo sát A.3 cần thu hẹp vì T-032/G2 đã có phân xử một phần; không sửa khảo sát hoặc G2. Các hạn chế dữ liệu không bị dùng làm nguyên nhân gap khi thiếu phép matched-program/release. RQ2 và quyết định baselineP7 vẫn OPEN; không xác nhận lợi ích đồ thị.
- Trợ lý Codex kiểm đọc 88hash,22ca/13ô, các ví dụ và nguồn MicroRank; không thấy lỗi khoa học mới, phát hiện dấu | chưa escape làm lệch bảng13ô. Người làm đã sửa sang dấu × trong báo cáo và kiểm cấu trúc cột. Lệnh sửa đầu tiên dừng trước ghi vì regex đếm12/13 (frontend không có hậu tố service); đã sửa regex, đủ13. Không có lượt phương pháp hỏng hoặc phải bỏ; mọi lỗi lệnh đọc/kiểm và phiên bản code đều giữ trong LOG.
- Sau khi phương pháp đã chốt, bổ sung hàm tổng hợp nguồn vào doi_chieu.py; đã giữ bản source-doi_chieu-at-start.py ở full-001. Các hàm source helper đã dùng không đổi. Cả hai snapshot nguồn đầu lượt sẽ được kiểm theo config.json cuối phiên; không sửa hash cấu hình cũ.

**Đang kết thúc:** kiểm toàn bộ file set/diff, prefix LOG/WHY, source code baseline và con trỏ; tạo manifest cuối; đồng bộ đúng dòng T-042 thành chờ phản biện và soạn prompt Claude nguyên mẫu. Chưa có phản biện Claude hoặc nghiệm thu Minh; không commit/push.


## Kết thúc phiên 2 — 24/10/2026 — chờ phản biện

1. **Đã làm gì:** tự soát theo nguồn trực tiếp trước triển khai, không thấy bất hợp lý chặn SPEC; ghi WHY-54 đúng nội dung đã duyệt; kiểm nguồn, đối chiếu bài–code–repo; chạy đủ 2×2 M4 trên dev, dùng lại pilot và chuỗi MicroRank/S1 hợp lệ. Viết phân xử từng giả thuyết, báo cáo theo ca/ô, tác động G2/P6/P7/P9 và hợp đồng/bằng chứng thiếu của phần nối tiếp. Tự soát nội bộ Codex không thay phản biện Claude.
2. **File thay đổi:** tạo đúng đầu ra trong results/T-042/ (danh sách đầy đủ và hash tại manifest.json); chỉ nối LOG T-042, nối WHY-54 trong docs/WHY.md và đổi đúng dòng T-042 trong docs/STATE.md thành chờ phản biện. SPEC/DECISIONS/AGENTS giữ nguyên; không sửa kế hoạch hạ tầng, code dùng chung hoặc kết quả cũ. Kiểm prefix và trạng thái Git ngoài phạm vi không đổi; các thay đổi có sẵn không bị lấy làm sản phẩm task.
3. **Kiểm tra và kết quả:** nguồn hiện có khớp; fixture22, input audit22, arithmetic88, S0 exact22, P3/độc lập88, khoảng hạng lịch sử44 đều đạt. Chuỗi MicroRank465 file khớp, không chạy lại. Đã kiểm đủ bảng13ô/22ca, sửa dấu tách cột Markdown, kiểm source snapshot theo hash đầu lượt, JSON strict, syntax, con trỏ/đường dẫn và diff/file set. Nguồn baseline/code/bản ghi cũ vẫn khớp. Không có lượt phương pháp hỏng; các lỗi lệnh chỉ đọc/kiểm được ghi trong phiên này.
4. **Điều chưa chắc hoặc cần Minh quyết:** T-042 đạt phần đối chiếu hiện có và phép phân xử M4 đã giao; hai quy ước có tác động tính toán nhưng các biến thể không sửa gap chung, nên không chọn baseline mới. Chưa xác nhận code/config/preprocessing/cohort/evaluator tạo bảng công bố; RQ2, cơ chế vật lý, lợi ích đồ thị, baseline P7 và G3 vẫn OPEN. Phần pipeline tác giả cần nguồn cụ thể và task/ngân sách riêng như báo cáo §7; thiếu local capture M4 đã xử lý bằng replay được phép, thiếu whole clone MicroRank được giữ đúng giới hạn. Không nghiệm thu/đóng task, không mở test/giữ ngoài, tải thêm, lấy EC2, gửi Claude hoặc commit/push. Nội dung cần đưa vào tài liệu chính thức khi Minh quyết: cách diễn đạt lại khảo sát A.3 và phạm vi G2-H08, lựa chọn comparator P7, yêu cầu nguồn tác giả và quan sát FlashTicket; chưa tự sửa các tài liệu đó.

**Giới hạn kiểm chi phí:** thời gian và RSS lượt phương pháp có trong cost.json; RSS là lấy mẫu ở biên ca, không là cận đỉnh. Các lượt chỉ kiểm nguồn/evaluator có metadata riêng và trường chưa đo ghi null, không suy thành0. Không có bằng chứng vượt ngân sách. Việc thiếu measurement đỉnh không được dùng để giảm dự toán gói nối tiếp.

**Hai lỗi kiểm cuối đã phân xử:** một lệnh cuối so DECISIONS báo không khớp do người làm gõ sai hằng hash trong lệnh, không phải file đổi; đã lấy tự động giá trị đầu phiên và xác nhận hash thực giữ nguyên. Một lệnh in mẫu prompt thiếu cấu hình stdout UTF-8 bị lỗi mã hóa, đã đọc lại thành công. Các lệnh không sửa file khoa học. Không cập nhật manifest nguồn để hợp thức hóa mismatch.

**Bước tiếp theo chính xác:** Minh đọc D:/RCA-flashticket/results/T-042/bao-cao.md, phan-xu.json, doi-chieu.md và manifest.json; chọn chuyển prompt Claude bên dưới để soát kết quả. Claude đọc nguồn theo mẫu và quyền hiện được giao; chưa được ghi REVIEW trong prompt này. Người làm chờ lượt phản biện/Minh quyết; không tự mở vòng hoặc gửi tin. Nếu tiếp trên máy khác, dựng nguồn/môi trường theo manifest và data/README, kiểm hash rồi đọc kết quả đã có; không chạy lại lượt hợp lệ chỉ vì đổi phiên.

**Lệnh cuối của lượt kiểm kết thúc:** Python -B qua stdin tại D:/RCA-flashticket để kiểm JSON/Markdown/source versions/prefix/scope, nối mục kết thúc và prompt này, tạo và kiểm manifest; trong lệnh gọi git diff --check -- docs/STATE.md docs/WHY.md tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md results/T-042. Lệnh tái xem chỉ đọc: Get-Content -LiteralPath results/T-042/bao-cao.md -Encoding utf8; xem invocation/cost từng run. Các CLI phương pháp đã chạy được ghi ở các mục trước, không có lệnh chạy tiếp cần tự thực hiện.

**Đề xuất nội dung commit khi Minh yêu cầu:** research: compare Nezha-OB baselines and audit M4 conventions (T-042). Chưa commit/push.

## Prompt Claude — soát kết quả T-042

Minh chọn chuyển prompt này. Chỉ quyền được nêu dưới đây có hiệu lực; chưa tự gửi hoặc mở phản biện.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-042; D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P3–P4, trọng tâm G2.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md và LOG.md cùng thư mục; D:/RCA-flashticket/results/T-042/doi-chieu.md, phan-xu.json, bao-cao.md, nguon.json, ke-hoach-chay.json, manifest.json; bản task chưa commit, không có commit gốc riêng.
- Phản biện và phản hồi trước: không có phản biện chính thức trước.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-042/scripts/ và runs/; source/manifest tại nguon.json, runs/reuse-audit-001/micro-source-checks.json và manifest.json; các nguồn T-008/T-017/T-026/T-032/T-034 được SPEC dẫn; code src/p3/, src/simplerca/, src/microrank/ trong cùng repo; môi trường D:/RCA-ext/envs/T-014-main/Scripts/python.exe, dùng -B; lệnh đã chạy trong LOG và invocation từng lượt.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chưa có quyền ghi bản phản biện hoặc sửa file trong lượt này.

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

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và quy tắc đơn giản trên cùng đồ thị dùng khi đánh giá tác dụng của việc dùng quan hệ; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.

```

---

## Tiếp tục phiên 2 — 24/10/2026 — Codex — Windows local — người làm

**Lời Minh:** “duyệt làm luôn trong phiên này, làm cho đến khi không phân xử được nữa thì thôi”. Đã ghi Q-190. Đây là duyệt phần nối tiếp vừa trình, không phải lời xác nhận nguyên nhân hoặc quyền mở test. Giữ Claude là người phản biện; chưa tự gửi tin.

**Phạm vi và tác động:** tiếp tục xác định code/config/preprocessing, dựng bộ bọc dev an toàn rồi so cùng đầu vào/thay từng khác biệt. Ghi bổ sung theo lượt mới trong results/T-042/runs/; không ghi đè164file kết quả đã có hoặc sửa src/SPEC/kế hoạch/tác vụ khác. Nối LOG/WHY/DECISIONS, chỉ đổi dòng T-042 STATE. Quyền mới giải quyết ranh giới chỉ bàn giao phần pipeline ở SPEC cũ; giữ SPEC như hồ sơ đã khóa, ghi lời duyệt và kế hoạch thực tế ở đây. Chưa có nhu cầu tải/cài; codeZIP local đã ghim có thể còn nguồn chưa khai thác. Không tự coi thiếu clone ở scratchpad là không thể phân xử.

**Kiểm đầu lượt:** đọc lại AGENTS/STATE/SPEC/LOG và nguồn chi phối DT18/cô/MRP/LESSONS/WHY/DECISIONS. Manifest T-042 trước bổ sung có163file, tất cả khớp; chính manifest và sáu file quản trị/task được giữ hash đầu lượt trong bộ nhớ để kiểm phạm vi. Hai trợ lý Codex chỉ đọc lần source SimpleRCA và MicroRank; không ghi, không chạy method hoặc thay phản biện Claude. Không quá hai trợ lý.

**Mục tiêu và điều kiện dừng khoa học:** không chỉ chạy thêm để gần0,91. Với mỗi phép phải xác định được đầu vào/phần xử lý khác nhau, dự đoán, kết quả ủng hộ/bác bỏ và thiếu nguồn gì. Dừng nhánh khi bằng chứng cần thiết không có sau khi đã lần nguồn local hợp lệ, hoặc dữ liệu hiện có không phân biệt được các giải thích; ghi chính xác nguồn cần lấy và quyết định phụ thuộc. Không dùng hết phạm vi cũ hay số kém làm bằng chứng không thể phân xử.

**Kế hoạch trước code/thực nghiệm:** (1) kiểm nguồnZIP/code/loader/evaluator còn có; (2) lập hợp đồng source→schema→unit→N/A và hàng rào dev; (3) dùng lại trung gian nếu đủ; (4) chỉ chạy phép có hợp đồng nhận diện được, fixture và pilot không nhãn trước, ghi từng lượt/chi phí; (5) nối nhãn sau diagnosis và phân tích đủ ca/ô, so ca đúng/sai; (6) báo cáo bổ sung và prompt Claude. Dự toán chưa kiểm: đọc/cài/kiểm trong một phiên, máy ưu tiên lượt dưới1giờ, không EC2/GPU; chưa coi 5s/ca bài là ngân sách. Không tải thêm hiện tại. Nếu cần môi trường/nguồn mới, đánh giá kích thước và quyền cụ thể trước thao tác.

**Phát hiện nguồn ban đầu:** ZIP code rcabench-platform-feat-fse26.zip đã nằm local theo download-manifest T-017, có make_nezha.py. Chưa đọc source này ở lượt trước. Sẽ kiểmhash rồi đọc đúng các member sourcecode; không giải nén dữ liệu hoặc chạy loader toàn tập. Một lần đọc đoán tên simple_rca.py không tồn tại, đã dùng inventory thật thay; không tạo file.

**Checkpoint nối tiếp:** đã lập kế hoạch prospective continuation-001/plan.json và nối WHY-54 trước code/chạy. Ngữ cảnh đã được nén; trạng thái khôi phục từ file thật: ba file quản trị/LOG đã nối Q-190 và dòng T-042 đang làm bổ sung;164file cũ giữ nguyên, chưa có thực nghiệm bổ sung. Tiếp tục theo quyền Minh yêu cầu cùng phiên; nếu phải chuyển máy/phiên, đọc kế hoạch này và output mới, không lặp lượt hợp lệ.

**Tiến độ bổ sung:** fixture Simple10/10 và pilot6nhánh một ca đạt; full dùng lại pilot, đang hoàn thành132diagnosis. Source-contract-001 hỏng vì assertion phụ trợ nói quá rộng toànZIP không có tênpaired; scan thật cho thấy reader RCABench khác có. Đã giữ source-at-start/failure, đọc đúng đường Nezha converter/caller và chạy source-contract-002 đạt: thiếu sáu pairedfiles làm adapter gốc trả sáu DataFrame rỗng và ranks[]. Không diễn giải lỗi kiểm này thành lỗi method. Micro fixture8 đạt; pilot-001 hỏng ở kiểm ordering phụ trợ quá chặt, giữ nguyên và sửa kiểm multiplicity ở lượt002, không sửa method. Đang chạy22dev và dùng lại pilot. Nhãn chỉ nối ở evaluation sau freeze các worker; việc đọc schema nhãn ở tiến trình điều phối không truyền vào method hoặc dùng chọn cấu hình.

**Checkpoint Q-190:** hai trợ lý dừng do giới hạn usage; root nhận lại toàn bộ file thật. Probe full22 và histogram22 đã hoàn tất, giữ outputs. Worker Micro full-002 được root dừng để giữ ngân sách đĩa; giữ nguyên mọi file, không xóa/nén thay cũ; full-003 dùng driver_v4 chỉ nén output mới và dùng lại10ca đã đủ3record. Tiếp tục chạy cùng phiên theo lời Minh; không coi giới hạn usage của trợ lý là giới hạn khoa học.


### Kết thúc phần nối tiếp Q-190 — 24/10/2026 — Codex người làm

1. **Đã làm:** tiếp tục theo lời Minh, không dừng ở2×2. Đọc code converter/caller/evaluator đã ghim; kiểm kernel AST không sửa trên22dev; so đơn vị trace, thời gian log/metric, severity, graph/count/formula/prior và cây kind. Dùng lại các trung gian đủ hash và pilot/case hợp lệ. Main.py literal đúng15/22, projection TimeStamp16/22; physicalns5/22; không nhận nhánh tốt hơn là baseline đã chọn. NezhaRCA partial và severity contracts tách rõ. Micro nguyên kernel RCAEval có spectrum không hợp lệ22/22; đổi riêng graph/formula/prior không cứu sham Top1. Có chuỗi trung gian và ca đúng/sai cùng ô, không gán mọi sai cho một cơ chế. Đã lập báo cáo nguồn/mức kết luận tại bao-cao-bo-sung.md và phan-xu-bo-sung.json trong continuation-001.

2. **File thay đổi:** chỉ thêm results/T-042/runs/continuation-001/ (scripts/config/fixture/diagnosis/intermediate/evaluation/report/hash/cost/prompt); nối WHY-54, DECISIONS Q-190 và LOG này; chỉ đổi dòng T-042 trong STATE. SPEC và164file T-042 trước bổ sung giữ nguyên; toàn bộ src, data, kết quả/task khác và tham chiếu hạ tầng không sửa. Q-190 chỉ duyệt thực hiện phần nối tiếp, không quyết chọn phương pháp hoặc nghiệm thu. Không commit/push, tải/cài, mở test/giữ ngoài, ghi ngoài hệ thống hoặc gửi Claude. Hai trợ lý nội bộ hỗ trợ người làm, không thay phản biện chính thức; root tiếp quản khi trợ lý hết usage.

3. **Kiểm:** fixture Simple10, graph/spectrum8, Eq7 toy, contract11 và histogram8 đạt; source/revision/AST hash kiểm trước dùng; raw payload không lưu. Có132Simple,198level,110TimeStamp,242Micro và132prior records (gồm replay/control; không là số quan sát độc lập). Micro evaluator đối chiếu242 vàprior132 với P3; kiểm cuối308native API ordinal ranks đối chiếu P3 đạt, tách khỏi kỳ vọng score ties. Đọc lại đầy đủ JSON/gzip/source scripts, frozen-list hashes và163output cũ đạt; kiểm code chung theo29pin gốc đạt; template prompt common/stage/G2 giữ nguyên ngoài metadata. git diff --check đạt. File set và hash trong manifest bổ sung; không sửa manifest cũ để che control hashes đã đổi theo quyền mới.

   **Lượt hỏng/dừng giữ đầy đủ:** source-contract-001 assertion scanner quá rộng, đã đọc lại đường Nezha và kiểm002; Micro pilot-001 đòi list order không cần cho ranker thay bằng Counter multiplicity; full-001 kiểm bit quá chặt, giữ audit và dùng16ULP AND16eps không floor, giữ service order/tie/max-op exact; full-002 dừng worker vì lưu lượng đĩa rồi tiếp bằng gzip cho output mới; full-003 hai operation không phải max trong cùng shippingservice đổi thứ tự2ULP, ghi đủ vị trí/score tại full-004, service ranking không đổi. Final-verify-001 dùng tie_group sai khi chấm native API; giữ source/failure rồi002 dùng ordinal key rõ ràng, không đổi diagnosis. Một lệnh đọc JSON thiếu encoding và một lệnh tìm wildcard trên PowerShell hỏng; đọc lại đúng UTF-8/thư mục, không ảnh hưởng số. Cost/clock/RSS có giới hạn nêu ở cost-and-runs.json: contracts RSS null; full-002 bị dừng nên không có CPU/peak/cost cuối. Không gọi null là0. Kết quả nặng giữ nguyên; tổng byte thực trong manifest, không xóa/nén thay file cũ.

4. **Câu hỏi nguồn và điều còn mở:** đã xác nhận những khác biệt có tác động, không phải thiếu mọi bằng chứng. Không thể định danh tiếp pipeline lịch sử sinh0.91/Table3 chỉ từ nguồn local và22dev: thiếu exact revision/entrypoint/config/cohort, normal inputs/conversion bridge, per-case predictions và script tổng hợp. Normal ngoài allowlist không được mở. Có thể nghĩ thêm tổ hợp/đổi thuật toán, nhưng không cung cấp provenance để chọn giữa các chương trình tác giả khả dĩ; không coi nó là bắt buộc chạy thêm chỉ để khớp số. Severity thật thiếu ở112587lượt dòng vẫn unknown; không bịa INFO hoặc suy keyword thành level. Kết quả dev chưa xác nhận lợi ích phương pháp đồ thị hoặc tổng quát hóa; P6/P7/G3 và lựa chọn baseline phụ thuộc nguồn/thiết kế/đánh giá được giao tiếp. Dừng thực nghiệm phần nối tiếp ở giới hạn nhận diện này; chưa nghiệm thu/đóng task hay câu hỏi nghiên cứu. Claude chưa phản biện; Minh quyết tiếp nhận giới hạn, yêu cầu nguồn hoặc giao bước sau.

**Bước tiếp theo chính xác:** Minh đọc results/T-042/runs/continuation-001/bao-cao-bo-sung.md, phan-xu-bo-sung.json và manifest.json cùng báo cáo/manifest gốc. Nếu chuyển phiên, giữ SOURCE/Python theo config/pins; xác minh manifest và đọc diagnoses đã có trước, không chạy lại lượt hợp lệ. Claude nhận prompt trung tính bên dưới để tự đọc nguồn gốc và kiểm kết quả; chưa được ghi REVIEW nếu Minh chưa cấp quyền. Người làm chờ Minh/Claude, không tự nghiệm thu hoặc gửi tin. Không có lệnh method còn cần tự chạy.

**Lệnh method/kiểm chính đã thực hiện:** dùng D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B tại D:/RCA-flashticket:
- results/T-042/runs/continuation-001/simple_runner.py fixtures simple-fixtures-001; pilot simple-pilot-001; full simple-full-001.
- source_audit.py; evaluate_simple.py; level_runner.py0/1/2 với PYTHONHASHSEED tương ứng; time_projection.py; evaluate_extra.py.
- micro/driver.py vàdriver_v2.py fixture/cached/pilot/full; driver_v3.py full full-002; driver_v4.py full full-003; driver_v5.py full full-004 vàevaluate evaluate-001, PYTHONHASHSEED=0. Invocation/source snapshots từng run ghi đúngversion.
- micro/prior.py fixtures prior-fixtures-001; prior_v2.py pilot prior-pilot-002; full prior-full-002; evaluate prior-evaluate-002, PYTHONHASHSEED=0. Tất cả từ graph đã lưu, không rawrerun.
- finish_report.py; verify_final.py (lượt002 đạt); finalize_handoff.py. Lệnh cuối cần hoàn tất là kiểm seal bằng final_seal_check.py sau khi manifest/handoff được tạo; script chỉ đọc. Các lệnh lỗi, stdout/stderr/failure và checkpoints giữ ở đúngrun.

**Đề xuất nội dung commit khi Minh yêu cầu:** research: discriminate Nezha-OB baseline source and input contracts (T-042). Chưa commit/push.

### Prompt Claude — soát kết quả T-042 sau phần nối tiếp

Minh chọn chuyển; chưa tự gửi. Prompt được chép nguyên văn ba khối hiện hành, chỉ điền metadata.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-042; D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P3–P4, trọng tâm G2.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md và LOG.md; D:/RCA-flashticket/docs/DECISIONS.md, WHY.md; D:/RCA-flashticket/results/T-042/bao-cao.md, doi-chieu.md, phan-xu.json, nguon.json, ke-hoach-chay.json, manifest.json; D:/RCA-flashticket/results/T-042/runs/continuation-001/bao-cao-bo-sung.md, phan-xu-bo-sung.json, manifest.json; bản chưa commit, không có commit gốc riêng.
- Phản biện và phản hồi trước: không có phản biện chính thức trước.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-042/scripts/ và runs/; D:/RCA-flashticket/results/T-042/runs/continuation-001/plan.json, supplementary-plan.json, cost-and-runs.json, micro-mechanism-chains.json, final-verify-002/checks.json và các diagnosis-list/diagnoses-frozen; src/p3/, src/simplerca/, src/microrank/; nguồn/revision/pin tại nguon.json, source-pins/source-checks/config/invocation từng lượt và manifest; môi trường D:/RCA-ext/envs/T-014-main/Scripts/python.exe, dùng -B, lệnh thực tế và hướng dẫn tại LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chưa có quyền ghi bản phản biện hoặc sửa file trong lượt này.

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

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và quy tắc đơn giản trên cùng đồ thị dùng khi đánh giá tác dụng của việc dùng quan hệ; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```


## Phiên 24/10/2026 — Codex, LEVANMINH, người làm T-042 — bổ sung normal N (Q-191)

### Quyết định của Minh trong phiên

Minh: “DUYỆT LÀM NGAY BÂY GIỜ”, duyệt đúng gói đã trình sau đáp phản biện: sửa SPEC bổ sung normal N, ghi DECISIONS/WHY/LOG/STATE và đầu ra normal-source-001; thử N-only trên22dev và kiểm đầu–cuối N. Giữ A300, code/kết quả cũ, khóa test/giữ ngoài, không commit/push/gửi Claude. Đã lưu Q-191 trước dùng lựa chọn. Không sửa Q-189 trùng mã của công việc khác.

### Tự soát trước chạy

Đọc AGENTS/STATE, SPEC và mục cuối LOG; đối chiếu DT18/cô, MRP RQ1/RQ2/P3/P4/P7, WHY/DECISIONS/LESSONS và source/manifest thật. Đã có lượt phản biện Claude trong chat và đáp phản biện chỉ đọc; chưa có file REVIEW được Minh duyệt ghi. Nhận thiếu sót phải trình phép đổi N trước khi dừng; không nhận suy luận N/A đã được xác nhận là nguyên nhân. Main chia Duration/1000, NezhaRCA/1e6; không gán nhầm hệ quả100s cho main. MRR TT công bố0.85, không0.80. Đính chính và phản hồi đầy đủ sẽ nằm trong đầu ra bổ sung.

Phạm vi mới đủ kiểm tác động nguồn N trên A cố định; chưa phân xử riêng sạch/số mẫu/độ dài, chưa nối kín historical pipeline. Hai miền normal được allowlist, chỉ timestamp-scanning trước lọc; không mở telemetry ngoài miền. N ngày23 có thể sau ca dev; không dịch timestamp hoặc để MicroRank tự chia nhầm. Một phút có thể thiếu mẫu; phải ghi unavailable/fallback/error, không tạo dữ liệu. Các giới hạn này đã được trình và được Minh duyệt, không tự là lỗi SPEC mới. Code/giấy phép/môi trường dùng lại nội bộ như lượt trước, không vendoring/phát hành.

Bản đồ ảnh hưởng đã được Minh duyệt: SPEC/DECISIONS/WHY là nguồn quyền và lý do; normal-source-001 là đầu ra mới; LOG/đúng dòng STATE là tiến độ. Đã chụp byte/hash mọi1284file kết quả T042 cũ và9control trước thay đổi tại before.json/before/. Giữ nguyên các thay đổi không thuộc task. Hai trợ lý nội bộ chỉ đọc code/metadata độc lập, không phải phản biện Claude.

Lỗi thao tác chuẩn bị: hai lần đọc nhầm tên core.py không tồn tại (đã tìm đúng inventory); một patch header SPEC có anchor dư không tồn tại nên bị từ chối toàn bộ, sau đó sửa đúng một dòng. Không đổi file/đầu ra khoa học trong các lần lỗi. Không dùng kết quả hỏng làm bằng chứng.

**Tiếp theo:** kiểm hash nguồn/kết quả, tạo allowlist và kế hoạch cụ thể, reader fixture, đếm mẫu normal trước method. Giữ mọi lượt và chi phí ngay từ đầu.

### Tiến độ bổ sung Q-191, trước chấm nhãn

- prepare-001:1282output khoa học cũ khớp manifest;26file normal (41.268.767byte) khớp inventory/hash. allowlist và plan được ghi trước method. Các control hash cũ không được tự cập nhật; bản trước giữ trong before/.
- fixtures-001:2kiểm adapter Micro explicit N/A đạt, gồm N nằm sau A mà không dịch thời gian.
- pilot-001:ca nhỏ nhất dev-27252dca60; M4 cũ và main M0 cũ replay khớp chính xác, explicit Micro chia N/A khớp toàn kết quả core gốc; N mới chạy3method được. Normal ngày23 có165kênh mỗi kênh1mẫu hữu hạn; lưu audit và mọi output trước đọc nhãn.
- full-001:đang chạy, dùng lại pilot đúng hash/script; normal ngày22 cũng165kênh×1mẫu. M4 metric sẽ unavailable đúng min2, không fill; main pool fallback giữ đúng code. Từngca/F2/audit/method_s/stdout/stderr ghi ngay từ đầu. Chưa chấm/đọc nhãn ở lượt này. Không xem một phút normal là nền sạch hoặc nhiều mẫu.
- Bước tiếp:đợi full-001 freeze66record rồi mới chạy evaluate.py; đọc score/intermediate theo từngca vàô. Lệnh đang chạy: Python -B results/T-042/runs/normal-source-001/run.py full full-001, PYTHONHASHSEED=0.

### Sau freeze và chấm Q-191

full-001 hoàn tất66record, reuse3pilot,261giây full; cả22Micro cóstatusok, không kích hoạt nhánh no_anomalous/no_normal/missingwindow. Trợ lý đọc code nêu wrapper sẽ dừng nếu các trạng thái ấy xuất hiện; đây là giới hạn nhánh chưa dùng, không mấtca hiện tại. Không tổng quát runner ngoài22inputđãduyệt; giữ sourceđúnghashđãchạy.

evaluate-001 hỏng vì khóa root trùng với trường root trong chuỗi; giữ source/failure. evaluate-002 hỏng khi bảng trace không có emailservice do không có A trace; giữ source/failure. evaluate-003 dùng get rõ trường thiếu, đạt toàn66record và chấm P3/độc lập. Không chạy lại method, không đổi diagnosis hoặc mẫu số. Đã sửa native Micro baseline theo thứ tự full operation API lưu trong scores trước chấm, tách khỏi thứ tự hiển thị hòa.

Tự kiểm F2 phát hiện5channel–case gần hằng có standardized delta vượt cận số họcsqrt5 do mean/variance làm tròn. Không dùng các số này làm cơ chế. Ghi WHY trước tính lại riêng thống kê F2 bằng hữu tỷ trên binary64 cùng đầu vào; không rerun method, không floor/epsilon hoặc mở thêm telemetry ngoài dev. Kết quả cũ giữ nguyên; báo cáo dùng F2-stable-001 sau kiểmcounts/timestamp/minmax.

### Kết thúc gói bổ sung Q-191 — bàn giao chờ phản biện

1. **Đã làm:** đã hoàn tất đúng gói N-only + F2 được Minh duyệt. Nguồn/hash/allowlist/plan trước method, normal60s chỉ có1mẫu mỗi165kênh/ngày, trace/log giữ capture19–28giây thực. Giữ A300 và source clock P3; Micro nhận N/A explicit, không shift thời gian.66diagnosis mới trên22dev freeze trước nhãn, dùng lại đối chứng cũ/pilot. Báo cáo hiện hành và đính chính/đáp F1–F3 tại results/T-042/runs/normal-source-001/bao-cao.md; phân xử từng giả thuyết tại phan-xu.json, toàn ô/ca tại evaluate-003/evaluation.json và tables.md.

   Kết quả chính P3 kỳ vọng hòa: M4 Hit1 0,318182→0,367424, MRR0,537542→0,555250; MAIN Hit1 0,681818→0,500000, MRR0,782147→0,684222; Micro Hit1 0→0, MRR0,170139→0,163059. Native tương ứng7→6,15→12,0→0 trên22. M4 chấm20OK+2NO_EVIDENCE, không loại ca rỗng. Chuỗi xác nhận: M4 usablemetric165→0 mỗi ca; MAIN440poolCPU/network fallback sangA và0alert, latency5giá trị khác metric tại1mốc vẫn chạy; Micro nhóm trace đổi22/22nhưngroot không lên1. Không suy một cờ thành nguyên nhân mọi ca; đã đối chiếu cả đúng/sai cùng ô và lưu mọi trung gian. N này không khôi phục kết quả chung; không chứng minh nền cũ nhiễm lỗi hay normal mới sạch.

   F2 cùng3630kênh–ca, tính hữu tỷ cho thống kê sau phát hiện5tỷ số gần hằng vượt cận do làm tròn. F2-stable-001 counts/timestamp/minmax khớp toàn bộ, cận đạt; không đổi method/score.3042tỷ số xác định,588không xác định; medianabs1,093941 vàP901,866629. Dấu delta chỉ mô tả, không tự là biến động vật lý; tên field normalized_lastbit_changes chỉ đếm số tỷ số đổi, không hàm ý chỉ bit cuối. Chưa phân xử nguyên nhân hồi phục; 7cặp dev kề không là toàn lịch tiêm.

2. **File thay đổi:** đúng5control được duyệt: SPEC T-042 (header và phụ lụcQ-191), nối DECISIONS Q-191, WHY-54 và LOG này; chỉ dòng T-042 STATE thành chờ phản biện. Mọi đầu ra mới nằm trong results/T-042/runs/normal-source-001/; file-set/diff/hash cuối tại manifest.json và control-diff.patch.1284file T042 cũ, các control không thuộc lượt và src giữ nguyên. Không sửa mã hạ tầng/tham chiếu kế hoạch hoặc Q-189 trùng mã của công việc khác. Không commit/push, mở test/giữ ngoài, tải/cài hoặc gửi Claude.

3. **Kiểm:** verification-001/checks.json PASS:170JSON/gzip tại mốc kiểm đọc được;66record+baseline hash, tổng P3/độc lập, F2stable, source snapshots, pin T034 và2nguồn công bố,1284kết quả cũ và control ngoài quyền không đổi; git diff --check đạt. Đã đọc toàn báo cáo, từng ô/ca và trung gian. Hai trợ lý nội bộ chỉ đọc code/output, kiểm độc lập component/fusion/spectrum66record và F2, không là Claude hoặc phản biện chính thức. Method full261giây, pilot12giây, F2stable6giây; peak sampled RSS~456MiB, không là đỉnh liên tục. Tổng byte thực tại manifest, dưới20MB. F2stable không capture stdout/stderr riêng, giữ progress/summary/exit0; không giả null là0.

   Giữ evaluate-001/002 hỏng (khóa root trùng, thiếu trace emailservice hợp lệ), source/failure đầy đủ; evaluate-003 đạt. Không rerun method. Một patch bổ sung báo cáo bị từ chối vì hunk ngược thứ tự; không file đổi ở lượt đó, đã cập nhật theo đúng dòng. Giới hạn wrapper Micro: trạng thái core khôngok nhưng không thiếu baseline sẽ dừng lô; không kích hoạt ở22input này (tất cảok), không tuyên bố runner đã xử lý mọi input khả dĩ.

4. **Câu hỏi nguồn và phần cần Minh quyết:** gói đã duyệt đã có đủ đầu ra và kiểm, chưa nghiệm thu. RQ1/P3 vàRQ2/P4 có thêm chuỗi tác động N→mất phiếu/fallback/nhóm trace→rank ở điều kiện kiểm; chưa xác định độc nhất nguyên nhân chênh công bố, sạch/nhiễm normal hoặc lịch sử chương trình. Exact normal_metric/bridge/revision/config/cohort/per-case prediction/aggregation vẫn OPEN. Phần A theo converter chưa chạy: cần nguồn đúng lần tiêm kế toàn lịch và quyền miền mới nếu giao test/giữ ngoài; không tự lấy ca dev kế làm mốc và không chạy vượt Q-191. Phép N cũng thay nguồn/độ dài/số mẫu/phủ cùng nhau, không tách riêng “sạch”. Không nói đã hết phép phân xử; bước A/source-history cần giao riêng. P6/P7/baseline/G3 và hiệu quả đồ thị vẫn phụ thuộc. Đề xuất tiếp tục Claude kiểm độc lập lượt bổ sung; Minh quyết nghiệm thu, nguồn/miền tiếp theo hoặc chấp nhận giới hạn.

**Bước tiếp theo chính xác:** đọc bao-cao.md, phan-xu.json, evaluate-003/evaluation.json, mechanism-summary.json, F2-stable-001/summary.json và manifest trong normal-source-001. Dùng D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B, PYTHONHASHSEED=0 nếu cần kiểm. Trước dùng output, chạy verify.py seal chỉ đọc; không chạy lại method hợp lệ. Prompt Claude nguyên mẫu nằm ngay dưới và prompt-claude.txt; Minh chuyển thủ công. Người làm không tự đóng task.

**Lệnh đã chạy:** run.py prepare prepare-001; fixtures fixtures-001; pilot pilot-001; full full-001; evaluate.py (hỏng001), evaluate.py evaluate-002 (hỏng), evaluate.py evaluate-003 (đạt); f2_stable.py; report.py; verify.py check. Tất cả script ở results/T-042/runs/normal-source-001/, Python hiện có -B; hashseed0 ở method. Các lượt method có stdout/stderr, invocation và source-at-start. Sau report.py có hai chỉnh phần giải thích bằng chứng/F2 trong bao-cao.md, không đổi số JSON. Lệnh cuối phiên: D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B results/T-042/runs/normal-source-001/verify.py seal (chỉ đọc sau manifest; PASS thể hiện trên tool output). Không có method còn cần chạy tự động trong gói này.

**Đề xuất nội dung commit khi Minh yêu cầu:** research: test Nezha-OB normal-source contrast and document baseline limits (T-042). Chưa commit/push.

### Prompt Claude — kiểm lại phản hồi và bổ sung T-042

Minh chọn chuyển hoặc dừng; chưa tự gửi. Chép nguyên văn common + công đoạn kiểm lại + G2, chỉ điền metadata.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-042; D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P3–P4, trọng tâm G2.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md và LOG.md; D:/RCA-flashticket/docs/DECISIONS.md, WHY.md; D:/RCA-flashticket/results/T-042/bao-cao.md, doi-chieu.md, phan-xu.json, nguon.json, ke-hoach-chay.json, manifest.json; D:/RCA-flashticket/results/T-042/runs/continuation-001/bao-cao-bo-sung.md, phan-xu-bo-sung.json, manifest.json; D:/RCA-flashticket/results/T-042/runs/normal-source-001/bao-cao.md, phan-xu.json, source-contract.json, plan.json, manifest.json, verification-001/checks.json; bản chưa commit, không có commit gốc riêng.
- Phản biện và phản hồi trước: phản biện Claude ngày 24/10/2026 lưu nguyên văn tại D:/RCA-flashticket/results/T-042/runs/normal-source-001/phan-bien-trong-chat.txt; phản hồi Codex trong chat do Minh chuyển; bản ghi phản hồi và bổ sung tại D:/RCA-flashticket/results/T-042/runs/normal-source-001/bao-cao.md và LOG T-042.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-042/scripts/ và runs/; D:/RCA-flashticket/results/T-042/runs/normal-source-001/run.py, evaluate.py, f2_stable.py, evaluate-003/, F2-stable-001/, mechanism-summary.json, cost-and-runs.json, before.json; D:/RCA-flashticket/src/p3/, src/simplerca/, src/microrank/; nguồn ngoài repo theo pin tại D:/RCA-flashticket/results/T-017/sources/download-manifest.json; môi trường D:/RCA-ext/envs/T-014-main/Scripts/python.exe, dùng -B; lệnh và hướng dẫn tại LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chưa có quyền ghi bản phản biện, sửa file hoặc chạy thực nghiệm mới.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và quy tắc đơn giản trên cùng đồ thị dùng khi đánh giá tác dụng của việc dùng quan hệ; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```


## Phiên 24/10/2026 — Codex, LEVANMINH, người làm — dừng điều tra OB theo Q-192

### Quyết định của Minh trong phiên

Minh: “Dừng tìm nguyên nhân lệch OB và chấp nhận giới hạn”. Đã lưu nguyên lời quyết định tại docs/DECISIONS.md, Q-192. Đây là quyết định dừng điều tra thêm, có hiệu lực thay phần tiếp tục tìm nguyên nhân trước đây; không tự suy thành nghiệm thu hoặc đóng T-042. Không còn lượt tìm nguyên nhân cần tự chạy, không tự trình/chạy tiếp nhánh A hoặc xin nguồn tác giả trong phạm vi này. Các giới hạn và nguyên nhân chưa phân xử tiếp tục OPEN, đã được Minh chấp nhận làm giới hạn của hồ sơ hiện tại.

### Báo cáo bốn mục

1. **Đã làm:** dừng tìm nguyên nhân lệch OB, ghi quyết định và bàn giao theo giới hạn hiện có. Không nghiên cứu hoặc chạy thực nghiệm mới. Kết quả và mức kết luận ở các báo cáo T-042 giữ nguyên; không nhận đã xác định duy nhất do dataset/code, normal sạch/nhiễm hoặc pipeline sinh số công bố.
2. **File thay đổi:** chỉ nối docs/DECISIONS.md và LOG này; chỉ cập nhật dòng T-042 docs/STATE.md. Giữ nguyên SPEC/WHY, toàn bộ code, kết quả/manifest và các thay đổi không thuộc lượt. Không commit/push/gửi Claude.
3. **Kiểm:** trước ghi, hash toàn bộ file/control của gói normal-source-001 khớp manifest. Sau ghi, kiểm đúng ba file, append-only DECISIONS/LOG và chỉ dòng T-042 STATE; toàn bộ file kết quả trong manifest vẫn nguyên hash; git diff --check đạt. Không kiểm lại phương pháp hoặc mở dữ liệu.
4. **Giới hạn và trạng thái:** chấp nhận phần nguyên nhân chưa phân xử, khác giao thức/cài đặt/độ phủ đầu vào và nguồn lịch sử còn thiếu như đã báo. Việc dừng không xác nhận hay bác bỏ mọi ứng viên nguyên nhân, không chứng minh không thể phân xử tiếp. T-042 vẫn chờ phản biện hồ sơ hiện có, chưa nghiệm thu/đóng; Minh chọn có chuyển Claude hay không. Các quyết định baseline/P6/P7/G3 không được tự bổ sung từ lời dừng này.

**Lưu ý hash sau quyết định:** manifest gói normal-source-001 giữ nguyên như mốc kết thúc thực nghiệm. Hash control DECISIONS/LOG/STATE từ mốc ấy sẽ khác do Q-192; đó là thay đổi hồ sơ có nguồn, không phải thay đổi kết quả. Không cập nhật manifest cũ để che khác biệt. Khi dùng lại số, kiểm phần files của manifest; không chạy verify.py seal nguyên gói rồi coi control mismatch có nguồn này là kết quả bị hỏng.

**Bước tiếp theo chính xác:** không có lệnh method cần chạy. Nếu Minh giao kiểm hồ sơ, đọc Q-192 và mục này trước, rồi báo cáo/phan-xu/manifest của results/T-042/runs/normal-source-001/. Prompt nguyên mẫu bên dưới chỉ được Minh chuyển thủ công; không tự gửi hoặc tái khởi động điều tra. Nếu Minh nghiệm thu/đóng task sau đó, ghi quyết định riêng và cập nhật trạng thái theo quyền mới.

**Lệnh cuối phiên:** lệnh Python -B chỉ kiểm hash các mục files trong results/T-042/runs/normal-source-001/manifest.json, đối chiếu phạm vi ba file và git diff --check; không chạy method hoặc đọc telemetry. Kết quả PASS thể hiện trong tool output của lượt này.

**Nội dung commit đề xuất nếu Minh yêu cầu:** docs: record accepted limits and stop OB discrepancy investigation (T-042). Chưa commit/push.

### Prompt bàn giao hiện có — Minh chọn chuyển hoặc dừng

Chép nguyên văn prompt đã chuẩn bị, chỉ metadata; quyết định hiện hành nằm tại DECISIONS và mục LOG mới. Không tự gửi.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-042; D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P3–P4, trọng tâm G2.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md và LOG.md; D:/RCA-flashticket/docs/DECISIONS.md, WHY.md; D:/RCA-flashticket/results/T-042/bao-cao.md, doi-chieu.md, phan-xu.json, nguon.json, ke-hoach-chay.json, manifest.json; D:/RCA-flashticket/results/T-042/runs/continuation-001/bao-cao-bo-sung.md, phan-xu-bo-sung.json, manifest.json; D:/RCA-flashticket/results/T-042/runs/normal-source-001/bao-cao.md, phan-xu.json, source-contract.json, plan.json, manifest.json, verification-001/checks.json; bản chưa commit, không có commit gốc riêng.
- Phản biện và phản hồi trước: phản biện Claude ngày 24/10/2026 lưu nguyên văn tại D:/RCA-flashticket/results/T-042/runs/normal-source-001/phan-bien-trong-chat.txt; phản hồi Codex trong chat do Minh chuyển; bản ghi phản hồi và bổ sung tại D:/RCA-flashticket/results/T-042/runs/normal-source-001/bao-cao.md và LOG T-042.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-042/scripts/ và runs/; D:/RCA-flashticket/results/T-042/runs/normal-source-001/run.py, evaluate.py, f2_stable.py, evaluate-003/, F2-stable-001/, mechanism-summary.json, cost-and-runs.json, before.json; D:/RCA-flashticket/src/p3/, src/simplerca/, src/microrank/; nguồn ngoài repo theo pin tại D:/RCA-flashticket/results/T-017/sources/download-manifest.json; môi trường D:/RCA-ext/envs/T-014-main/Scripts/python.exe, dùng -B; lệnh và hướng dẫn tại LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chưa có quyền ghi bản phản biện, sửa file hoặc chạy thực nghiệm mới.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và quy tắc đơn giản trên cùng đồ thị dùng khi đánh giá tác dụng của việc dùng quan hệ; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```


## Phiên 24/10/2026 — Codex, LEVANMINH, người làm — đóng T-042 theo Q-193

**Quyết định của Minh:** “đóng task.” Đã lưu Q-193 tại docs/DECISIONS.md. Minh đóng task với giới hạn đã chấp nhận theo Q-192; không ghi rằng Claude đã hoàn tất kiểm lượt bổ sung nếu chưa có bằng chứng.

1. **Đã làm:** đóng T-042 theo quyết định Minh; dừng điều tra OB như Q-192. Không chạy thêm hoặc thay kết luận khoa học.
2. **File thay đổi:** chỉ nối DECISIONS và LOG này; chỉ chuyển dòng T-042 trong STATE thành xong/đã đóng. Giữ SPEC/WHY/code/kết quả/manifest và thay đổi ngoài lượt.
3. **Kiểm:** hash toàn bộ file kết quả trong manifest gói normal-source-001 giữ nguyên; kiểm append-only hai file và chỉ dòng T-042 STATE thay đổi; git diff --check đạt. Không mở telemetry/test hoặc chạy phương pháp.
4. **Giới hạn còn lại:** task đã đóng theo quyết định Minh; phần nguyên nhân chưa phân xử và thiếu nguồn đã được chấp nhận, vẫn OPEN về khoa học. Không suy đóng task thành xác nhận nguyên nhân do dataset/code, chọn baseline, hiệu quả đồ thị hoặc quyền mở G3/test. Không tự mở lại task. Không còn việc T-042 được phép tự chạy.

**Bước tiếp theo:** không có lệnh thực nghiệm tiếp. Nếu cần tra cứu, đọc Q-192/Q-193 và mục đóng này, rồi báo cáo/phan-xu/manifest trong results/T-042/runs/normal-source-001/. Mọi nhiệm vụ mới chờ Minh giao; không tự chuyển tiếp Claude. Các control hash lịch sử đã khác theo Q-192/Q-193; giữ manifest cũ và kiểm phần files khi dùng lại số.

**Lệnh cuối:** Python -B kiểm hash phần files của manifest, đối chiếu đúng ba file thay đổi và git diff --check, kết quả PASS trong tool output; không chạy method.

**Nội dung commit đề xuất nếu Minh duyệt:** docs: close T-042 with accepted OB discrepancy limits. Chưa commit/push.

### Prompt lưu để Minh dùng nếu giao kiểm hồ sơ sau này

Task đã đóng; đây chỉ là prompt chuẩn được lưu theo mục7/9, không tự mở lượt phản biện hoặc tái khởi động task. Quyết định và trạng thái hiện hành phải đọc ở DECISIONS/STATE/LOG. Minh chọn có dùng hay không.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-042; D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P3–P4, trọng tâm G2.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md và LOG.md; D:/RCA-flashticket/docs/DECISIONS.md, WHY.md; D:/RCA-flashticket/results/T-042/bao-cao.md, doi-chieu.md, phan-xu.json, nguon.json, ke-hoach-chay.json, manifest.json; D:/RCA-flashticket/results/T-042/runs/continuation-001/bao-cao-bo-sung.md, phan-xu-bo-sung.json, manifest.json; D:/RCA-flashticket/results/T-042/runs/normal-source-001/bao-cao.md, phan-xu.json, source-contract.json, plan.json, manifest.json, verification-001/checks.json; bản chưa commit, không có commit gốc riêng.
- Phản biện và phản hồi trước: phản biện Claude ngày 24/10/2026 lưu nguyên văn tại D:/RCA-flashticket/results/T-042/runs/normal-source-001/phan-bien-trong-chat.txt; phản hồi Codex trong chat do Minh chuyển; bản ghi phản hồi và bổ sung tại D:/RCA-flashticket/results/T-042/runs/normal-source-001/bao-cao.md và LOG T-042.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-042/scripts/ và runs/; D:/RCA-flashticket/results/T-042/runs/normal-source-001/run.py, evaluate.py, f2_stable.py, evaluate-003/, F2-stable-001/, mechanism-summary.json, cost-and-runs.json, before.json; D:/RCA-flashticket/src/p3/, src/simplerca/, src/microrank/; nguồn ngoài repo theo pin tại D:/RCA-flashticket/results/T-017/sources/download-manifest.json; môi trường D:/RCA-ext/envs/T-014-main/Scripts/python.exe, dùng -B; lệnh và hướng dẫn tại LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chưa có quyền ghi bản phản biện, sửa file hoặc chạy thực nghiệm mới.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và quy tắc đơn giản trên cùng đồ thị dùng khi đánh giá tác dụng của việc dùng quan hệ; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```
