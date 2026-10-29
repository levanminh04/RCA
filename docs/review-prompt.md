# Prompt đánh giá độc lập và bàn giao

Dùng sau mọi lượt trình SPEC, báo cáo kết quả, phản biện, người làm đáp phản biện hoặc kiểm sửa (Q-88). Người phản biện chính thức phải khác người làm. Các lượt không tự đổi vai trò.

## Cách dùng

1. Chép nguyên văn **Prompt chung** + đúng một **Khối công đoạn** + **Khối trọng tâm cổng** hiện có. Không bỏ câu mạnh hoặc thay bằng danh sách kiểm riêng.
2. Chỉ điền chỗ <...> bằng thông tin trung tính: task/đề xuất, công đoạn, vai trò, đường dẫn, revision, manifest, môi trường/lệnh chạy và quyền ghi đã được Minh duyệt. Không thêm kết luận, số của người làm, gợi ý chỗ có lỗi/an toàn, mã quyết định/bài học cụ thể hoặc giới hạn khoa học riêng (Q-44).
3. Người làm ghi prompt vào mục LOG mới khi có quyền; người phản biện ghi trong bản phản biện lượt của mình, trước bảng phản hồi; chưa có quyền ghi thì đưa trong chat. Không thay prompt cũ.
4. Minh copy sang phiên của agent đối phương. Agent không tự mở phiên hay gửi sang agent khác. SPEC chưa được duyệt tạo file được trình và soát trong chat.
5. Sau mỗi lượt vẫn soạn prompt, kể cả đề xuất dừng. Bất kỳ bên nào có thể đề xuất dừng; Minh quyết. Không che bất đồng bên kia còn giữ. Đồng thuận không thay bằng chứng; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Người phản biện chỉ ghi đúng một bản lượt được Minh cho phép. Liệt kê thư mục trước khi chọn tên bản mới; REVIEW.md nếu chưa có, REVIEW-2.md… cho lượt sau, không ghi đè lịch sử. Người làm chỉ điền bảng phản hồi của bản liên quan và LOG trong quyền được duyệt; không sửa nhận xét hay prompt của người phản biện.

## Cách chạy

**Codex phản biện:** mở phiên tương tác trong D:\RCA-flashticket rồi dán prompt; hoặc dùng CLI chỉ đọc và lưu câu trả lời vào đúng file đã được Minh cho phép:

```
codex exec -s read-only -C D:\RCA-flashticket -o tasks\T-xxx-<tên>\<bản-phản-biện-đã-duyệt>.md "<dán prompt>"
```

Nếu chỉ được trả lời trong chat, không dùng tùy chọn lưu file. Với người làm đáp phản biện, dùng phiên tương tác và quyền ghi bảng phản hồi/LOG đã duyệt.

**Claude:** mở phiên mới trong D:\RCA-flashticket rồi dán prompt. Quyền ghi do prompt đã được Minh duyệt xác định, không mặc nhiên cấp quyền sửa.

## Prompt chung

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: <mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>.
- Công đoạn: <soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>.
- Gói/cổng: <gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>.
- Người làm và người phản biện chính thức: <tên theo SPEC; ngoài task thì ghi vai trò dự kiến>.
- Tài liệu gốc: <danh sách đường dẫn và git diff từ commit gốc nếu có>.
- Phản biện và phản hồi trước: <đường dẫn theo thứ tự thời gian; không có thì ghi không có>.
- Code và kết quả liên quan: <đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>.
- Phạm vi ghi được Minh cho phép trong lượt này: <chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>.

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
```

## Khối công đoạn

Chép đúng một khối; không tự sửa các câu kiểm.

### Soát SPEC

```text
Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.
```

### Soát kết quả

```text
Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.
```

### Người làm đáp phản biện

```text
Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.
```

### Kiểm lại phản hồi và sửa

```text
Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.
```

## Khối trọng tâm cổng

### G0 — MRP

```text
Đọc thêm docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
1. Chuỗi gói việc P1–P10 có đi đúng chuỗi cô yêu cầu không
   (hiểu sâu phương pháp → nhiều dataset → hạn chế → 5 bước đồ thị → tích hợp sản phẩm)?
2. Có bước nào cô yêu cầu mà MRP bỏ sót hoặc hiểu sai không?
3. Cách hiểu "graph-based anomaly detection" ở MRP §2.3 có hợp lý không? Có cách hiểu nào tốt hơn không?
4. Câu hỏi nghiên cứu nào không trả lời được bằng dữ liệu dự kiến?
5. Có lựa chọn nào lặp lại một sai lầm trong LESSONS không? Có lựa chọn nào thiếu câu trả lời "tại sao" không?
```

### G1 — Phương pháp, dataset, cách chia

```text
Danh sách phương pháp có phủ đủ các họ không; hồ sơ kỹ thuật có đúng với bài và code gốc không
(kiểm ngẫu nhiên ít nhất 2 phương pháp); dataset đã chọn có phân xử được RQ1, RQ3 không;
cách chia dev/test có lộ đáp án không; có đường nào để nhãn lọt vào phương pháp không.
```

### G2 — Baseline và phân tích hạn chế

```text
Kiểm chuỗi đầu vào → xử lý → trung gian → đầu ra ở các nhóm quan trọng. Đọc code và trung gian đã lưu trước, đối chiếu ca sai với ca đúng có điều kiện tương ứng. Thiếu trung gian thì nêu đúng phần cần chạy/thu thêm, chi phí và quyết định phụ thuộc; không tự chạy ngoài quyền hoặc bỏ câu hỏi bằng “ngoài SPEC”.
Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Nếu chưa xác định Y, giữ đúng quan sát, giải thích khác và bằng chứng thiếu.
Phân biệt dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu xác nhận có hệ quả đánh giá và yêu cầu quan sát FlashTicket có thể rút ra không?
Đầu ra có nêu: hạn chế đã xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/phép tính; quan hệ có thể bổ sung thông tin gì; câu chưa trả lời và bằng chứng còn thiếu? Căn cứ nào đủ đề xuất ứng viên, căn cứ nào đủ lựa chọn thiết kế?
Không bắt mọi task P4 làm xong đối chứng của phương pháp mới. Đối chứng bỏ quan hệ và quy tắc đơn giản trên cùng đồ thị dùng khi đánh giá tác dụng của việc dùng quan hệ; không là điều kiện trì hoãn mọi phân tích hạn chế baseline.
```

### G3 — Khóa thiết kế trước khi mở test

```text
Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

### G4 — Kết quả

```text
Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```
