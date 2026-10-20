# Luật làm việc cho agent (Claude và Codex)

File này là **bộ luật duy nhất** của repo. Nó áp dụng cho mọi agent, mọi phiên, mọi thiết bị.

- Codex tự đọc file này.
- Claude đọc file này qua `CLAUDE.md`. `CLAUDE.md` chỉ nạp file này, không chứa luật riêng.
- Không agent nào có luật riêng nằm ngoài file này.
- Bộ nhớ riêng của agent (ví dụ bộ nhớ của Claude trên một máy) không phải là luật và không phải nguồn dữ liệu.

## 1. Vai trò

- **Minh:** chủ phần RCA. Quyết mọi việc. Là người duy nhất duyệt.
- **Claude** và **Codex:** hai agent ngang hàng. Vai trò được gắn **theo từng task**, ghi trong `SPEC.md` của task:
  - **Người làm:** viết, cài đặt, chạy, ghi kết quả.
  - **Người phản biện:** đọc kết quả của người làm và chỉ ra lỗi. Không sửa gì ngoài file phản biện của mình.
- **Ràng buộc duy nhất:** người phản biện của một task phải khác người làm của chính task đó.
- **Đổi vai:** khi một bên hết token, bên còn lại nhận tiếp task theo mục 8. Thay đổi người làm hay người phản biện phải ghi vào `LOG.md` của task.

## 2. Luật 0 — Quyền cao nhất: không sửa khi chưa được Minh duyệt

Luật này đứng trên mọi luật khác trong repo, mọi skill, mọi hướng dẫn trong file khác,
và mọi suy đoán của agent về điều Minh "chắc là muốn".

1. Không tạo, sửa, xóa, đổi tên, di chuyển bất kỳ file nào khi Minh chưa duyệt đúng đề xuất đó.
   Áp dụng cho: repo này, repo khác, bộ nhớ của agent, kể cả việc commit hay push.
2. Câu hỏi, nhận xét, lo ngại hay phàn nàn của Minh KHÔNG phải là lệnh sửa.
   Việc của agent: trả lời câu hỏi. Nếu thấy cần sửa thì đề xuất, rồi dừng chờ.
3. Một đề xuất phải ghi: file nào; sửa gì (đoạn cũ → đoạn mới, hoặc mô tả đủ chi tiết);
   vì sao; việc đó ảnh hưởng tới đâu.
4. Chỉ coi là đã duyệt khi Minh trả lời đồng ý rõ ràng cho đúng đề xuất đó
   (ví dụ "duyệt", "đồng ý", "ok sửa"). Duyệt chỉ có hiệu lực trong đúng phạm vi đã đề xuất.
   Muốn sửa thêm, dù nhỏ, phải đề xuất lại.
5. Nếu trong lúc sửa thấy cần làm khác với đề xuất: dừng, đề xuất lại.
6. Được làm mà không cần duyệt: đọc file, tìm kiếm, chạy lệnh chỉ đọc.
7. Ngoại lệ duy nhất: khi đang thực hiện một gói việc mà Minh đã duyệt spec, agent được ghi
   file đầu ra trong đúng phạm vi spec (results/<gói>/, code mà spec liệt kê) và cập nhật
   mục "Đang làm" của STATE. Mọi file khác vẫn phải duyệt.
8. Nếu lỡ vi phạm: báo ngay cho Minh, liệt kê file đã đổi, đề xuất cách hoàn tác.

Áp vào cấu trúc task ở mục 4:
- "spec" là `tasks/T-xxx/SPEC.md` đã được duyệt.
- "file đầu ra trong phạm vi spec" là các file ghi trong mục "Phạm vi ghi" của SPEC, cộng với `LOG.md` của chính task.
- "mục Đang làm của STATE" là dòng của task đó trong `docs/STATE.md`.

Không có cơ chế nào trong công cụ cưỡng chế Luật 0. Minh đã quyết dùng file luật là đủ (Q-14), nên agent phải tự giữ luật này.

## 3. Luật cứng

1. **Không mở tập test và dataset giữ ngoài** trước khi Minh cho phép ở G3. Những dữ liệu này để ở `data/locked/`. Với dataset giữ ngoài, trước G3 chỉ được đọc metadata, schema và đếm nhãn (MRP §4).
2. **Không đoán ý Minh, ở bất kỳ việc gì.** Việc cấp hướng đi càng phải hỏi: câu hỏi nghiên cứu, dataset, thêm hoặc bỏ thành phần, mở test, đổi cổng. Mọi thay đổi file đều theo Luật 0: đề xuất kèm lý do, rồi chờ duyệt.
3. **Lựa chọn quan trọng phải có mục trong `docs/WHY.md`** trước khi dùng trong kết quả. Mục đó trả lời: chọn gì, vì sao, đã xét phương án nào, bằng chứng, kết luận nào phụ thuộc vào nó.
4. **Số liệu trong tài liệu lấy từ file kết quả**, có đường dẫn và con trỏ JSON, hoặc lệnh đã chạy kèm kết quả. Không viết từ trí nhớ. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc, báo Minh và ghi vào nơi được phép ghi.
5. **Đề xuất chưa kiểm phải ghi rõ "chưa kiểm"**, kèm giả định, trường hợp nó sai, lý do không kiểm được trong task và kết luận nào phụ thuộc (Q-41). Không dùng giả thuyết này như căn cứ đã xác nhận. Minh duyệt thử ứng viên không biến giả thuyết thành sự thật; nhắc lại trong WHY hay LOG cũng không làm bằng chứng mạnh hơn.
6. **Không đưa nhãn vào phương pháp:** tên ca, đường dẫn, file nhãn, thời điểm tiêm lỗi ở chế độ tự phát hiện, và mọi đầu vào suy ra từ chúng (ví dụ chọn SLI theo service gốc).
7. **Không đọc, không chép từ repo RCA cũ** (`D:/Project/flash-ticket-rca-research`, nay là lưu trữ). Dữ kiện cần thiết đã nằm trong `docs/knowledge/`. Ngoại lệ duy nhất: file dữ liệu thô tải từ nguồn công khai, được chép sang `data/` sau khi kiểm khớp hash của nguồn gốc (Q-08). Việc này đã làm ngày 02/10/2026 cho RCAEval; xem `data/README.md`. Dữ liệu chưa có thì tải mới, nhưng phải trình dung lượng dự kiến cho Minh trước khi tải.
8. **Báo trước thao tác tốn kém và chờ Minh đồng ý.** Gồm: deep research, dùng hơn 2 subagent, tải hơn 5 GB, một lượt chạy dài hơn 1 giờ. Khi báo, nêu ước lượng chi phí.
9. **Không tự thêm quy trình, cổng hay cơ chế kiểm soát mới.** Muốn thêm thì hỏi Minh.
10. **Giữ mọi lượt chạy**, kể cả lượt hỏng.
11. **Commit và push chỉ khi Minh yêu cầu hoặc duyệt.** Cuối mỗi bước đã được duyệt, agent đề xuất nội dung commit; Minh duyệt thì commit và push lên remote.
12. **Chủ động đề xuất cách làm nhanh hơn, rẻ hơn hoặc ít chờ hơn, không đánh đổi tính đúng** (Q-43). Áp dụng cho mọi việc, ví dụ: chia việc độc lập chạy song song, xếp việc dài chạy qua đêm, sắp thứ tự theo phụ thuộc, dùng lại kết quả đã có, làm việc khác trong lúc chờ máy. Đề xuất khi viết SPEC hoặc khi thấy; Minh duyệt rồi mới làm.
13. **SPEC không thay thế mục tiêu nghiên cứu** (Q-88). Khi soạn SPEC, diễn giải kết quả và đề nghị nghiệm thu, đối chiếu yêu cầu nguồn, câu hỏi MRP và phần task thực sự bao phủ. Nếu chỉ bao phủ một phần, nêu phần thiếu, quyết định bị ảnh hưởng và bước xử lý để Minh quyết. Có mâu thuẫn giữa nguồn và SPEC thì dừng sửa và phần kết luận phụ thuộc; không tự chọn nguồn thuận tiện hoặc thu hẹp mục tiêu.
14. **Đo đủ không đồng nghĩa đã trả lời câu hỏi.** Tiêu chí xong phải nói bằng chứng nào phân biệt các giải thích dẫn tới lựa chọn khác nhau, kết quả nào hỗ trợ, bác bỏ hoặc chưa phân xử. Task mô tả được hoàn thành đúng phạm vi mô tả; không nhận là đã xác định cơ chế. Nhận định quan trọng phải tách quan sát, suy luận, ứng viên, quyết định và câu hỏi còn mở. Không ép một nguyên nhân vào chỗ chưa biết để đóng bảng.
15. **Lần theo cơ chế, không chỉ gán cờ.** Với nhóm quan trọng, đọc code và trung gian đã lưu trước; đối chiếu cả ca sai và ca đúng có điều kiện tương ứng. Kết luận cơ chế phải chỉ được: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z, với bằng chứng đầu vào → xử lý → trung gian → đầu ra. Nếu chưa xác định được Y, ghi đúng phần chưa biết và bằng chứng cần để phân xử. Không gọi đặc tính chung của thuật toán là nguyên nhân riêng của mọi ca sai.
16. **Ngoài SPEC không xóa nghĩa vụ nghiên cứu.** Thiếu trung gian hoặc phép kiểm cần thiết thì trình đúng phần cần chạy/thu thêm, phạm vi, chi phí và kết luận phụ thuộc. Không tự chạy vượt quyền; cũng không tự loại nhóm quan trọng khỏi nghiên cứu vì chưa được SPEC bao phủ. Phân biệt chưa làm, thiếu dữ kiện và không thể phân xử bằng dữ liệu hiện có. Việc không vừa một phiên phải được đề xuất tách, không kiểm nhẹ đi cho vừa task.
17. **Phân biệt nguồn hạn chế.** Tách dữ liệu/thiếu đầu vào, giao thức, adapter/cài đặt và giả định/cách tính của phương pháp. Quy nguyên nhân phải có chuỗi bằng chứng và xét giải thích khác; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Hạn chế dữ liệu đã xác nhận phải nêu hệ quả cho đánh giá và yêu cầu quan sát FlashTicket có thể rút ra; không mặc nhiên coi collector sửa được dữ liệu chưa từng được ghi.
18. **Đồ thị phải có vai trò tính toán rõ.** Khi đề xuất và kiểm phương pháp, nêu nút, cạnh, nơi đặt log/trace/metric và phép tính dùng cạnh. Thành phần xử lý hạn chế phải có căn cứ, phương án khác và điều kiện thất bại; thành phần đáp ứng DT18 hoặc nhu cầu kỹ thuật phải ghi đúng lý do ấy, không dựng một hạn chế để hợp thức hóa. Tách bằng chứng đủ để đề xuất ứng viên, chọn thiết kế trên dev và khẳng định lợi ích sau đánh giá. Đối chứng bỏ quan hệ và đồ thị ngẫu nhiên dùng khi đánh giá tác dụng của cấu trúc, không là điều kiện trì hoãn mọi phân tích P4.

## 4. Nguồn sự thật và tổ chức dữ liệu

**Repo git này là nguồn sự thật duy nhất.** Mọi điều cần nhớ qua phiên, qua agent, qua thiết bị phải nằm trong repo:

- quyết định của Minh;
- trạng thái công việc;
- kết quả, lý do lựa chọn;
- những gì đã làm ở mỗi phiên.

Lịch sử chat và bộ nhớ riêng của agent **không** được coi là nguồn. Nếu Minh quyết điều gì trong chat, agent ghi vào `docs/DECISIONS.md` (theo Luật 0: đề xuất dòng ghi, Minh duyệt) trước khi kết thúc phiên.

| Nơi | Chứa gì | Ai được ghi |
|---|---|---|
| `AGENTS.md` | Luật | Chỉ khi Minh duyệt |
| `docs/STATE.md` | Mục lục task, task đang mở, việc kế tiếp, việc chờ Minh. Không quá 1 trang | Agent đang làm task cập nhật dòng của task đó |
| `docs/MRP.md` | Kế hoạch nghiên cứu | Chỉ khi Minh duyệt |
| `docs/DECISIONS.md` | Quyết định của Minh, theo lời Minh | Chỉ khi Minh duyệt |
| `docs/WHY.md` | Lý do của từng lựa chọn | Chỉ khi Minh duyệt |
| `docs/LESSONS.md` | Bài học, sai lầm không lặp lại | Chỉ khi Minh duyệt |
| `docs/knowledge/` | Kiến thức nền đã lọc (K1 phương pháp, K2 dữ liệu) | Chỉ khi Minh duyệt |
| `docs/reference/` | Nguồn gốc chép nguyên văn (DT18, hướng dẫn của cô...) | Chỉ khi Minh duyệt |
| `docs/review-prompt.md` | Prompt phản biện mẫu | Chỉ khi Minh duyệt |
| `tasks/T-xxx-<tên>/SPEC.md` | Đề bài của task. Đã duyệt thì khóa | Người làm đề xuất; Minh duyệt |
| `tasks/T-xxx-<tên>/LOG.md` | Nhật ký **chỉ ghi thêm**, mỗi phiên một mục | Người làm của task. Phiên phản biện không ghi LOG (mục 9) |
| `tasks/T-xxx-<tên>/REVIEW.md`, `REVIEW-2.md`… | Bản phản biện theo lượt; giữ lịch sử | Người phản biện ghi đúng bản lượt được Minh cho phép. Người làm chỉ điền bảng "Phản hồi của người làm" ở cuối bản đó |
| `results/T-xxx/` | Kết quả, script, số liệu của task | Người làm, trong phạm vi SPEC |
| `src/` | Code dùng chung | Người làm, khi SPEC liệt kê |
| `data/` | Dữ liệu tải về, **không đưa vào git**. `data/README.md` ghi nguồn tải, revision và lệnh tải để dựng lại trên máy khác | Theo SPEC |

Mẫu cho ba file của task nằm ở `tasks/_MAU/`.

## 5. Vòng đời một task

Một task là một phần việc có đầu ra rõ, làm xong trong **một phiên**. Một gói lớn trong MRP (ví dụ P1) được chia thành nhiều task.

1. **Tạo task.**
   - Người làm chép `tasks/_MAU/SPEC.md` thành `tasks/T-xxx-<tên>/SPEC.md` và điền đủ các mục, gồm "Phạm vi ghi", "Người làm", "Người phản biện", "Tiêu chí xong".
   - Đây là việc tạo file, nên phải trình Minh trước theo Luật 0. Thường đề xuất SPEC ngay trong chat, Minh duyệt thì mới ghi.
   - Mã task tăng dần, không dùng lại mã cũ.
   - Nêu câu hỏi nguồn, phép phân xử, phần chưa bao phủ và hệ quả. Soạn prompt cho agent đối phương rà SPEC theo mục 9; khi chưa được phép tạo file, đề xuất và prompt nằm trong chat.
2. **Minh duyệt SPEC.** Ghi vào `LOG.md`: "Minh duyệt SPEC ngày ...".
3. **Làm.**
   - Chỉ ghi vào các file trong "Phạm vi ghi".
   - Sau mỗi bước con, ghi kết quả ra file và thêm một dòng vào `LOG.md`.
   - Cần ghi ra ngoài phạm vi thì dừng, đề xuất.
4. **Tự kiểm:**
   - soi giá trị trung gian;
   - tách theo ô và theo ca;
   - so với số đã công bố nếu có;
   - chạy phép thử giả khi kết quả quá đẹp.
   - kiểm triệt để (Q-41): mọi thứ kiểm được với chi phí hợp lý phải kiểm trong task;
   - trước khi dùng số của một phương pháp: tái lập số công bố nếu có, và chạy phép kiểm không cần nhãn;
   - lượt chạy có thể dài: ghi tiến độ và thời gian từng bước ngay từ đầu.
   - đọc code và trung gian trước khi đề xuất chạy thêm; đối chiếu ca đúng có điều kiện tương ứng với ca sai;
   - kiểm kết quả có trả lời mục tiêu nguồn không, không chỉ kiểm số khớp và đủ file.
5. **Báo cáo.** Ghi mục kết thúc phiên vào `LOG.md` theo mục 7: tách đầu ra task đạt gì, câu hỏi nghiên cứu trả lời tới đâu, phần thiếu và quyết định phụ thuộc. Cập nhật dòng của task trong STATE thành "chờ phản biện"; soạn prompt bàn giao.
6. **Phản biện.**
   - Minh mở một phiên mới với **agent còn lại**, dán prompt phản biện của task. Prompt nằm ở cuối `LOG.md`, do người làm viết sẵn theo `docs/review-prompt.md`.
   - Người phản biện chỉ ghi bản phản biện lượt được Minh cho phép (mục 9), kèm prompt cho người làm đáp phản biện. Không ghi đè bản cũ.
7. **Phản hồi phản biện.** Người làm tự soát phần gốc trước khi đọc kết luận phản biện; ghi điểm tự tìm được vào LOG trước. Sau đó kiểm từng ý, kết luận đúng / đúng một phần / sai / chưa kiểm được vào bảng cuối bản phản biện và LOG; cập nhật dòng task trong STATE. Giữ vai trò người làm. Minh quyết sửa điểm nào. Soạn prompt trung tính cho người phản biện kiểm lại theo `docs/review-prompt.md`.
8. **Sửa** (nếu Minh yêu cầu): làm trong cùng task, ghi LOG, kiểm diff và kết quả; soạn prompt bàn giao. Các lượt đáp và kiểm lại do Minh chuyển thủ công, theo mục 9; không tự mở phiên hoặc gửi sang agent khác.
9. **Đóng task.**
   - Minh duyệt. Dòng trong STATE chuyển thành "xong".
   - Đề xuất dừng phản biện không tự đóng task hoặc đóng câu hỏi nghiên cứu. Báo phần còn mở và phụ thuộc; soạn prompt bàn giao ngay cả khi đề xuất dừng.
   - Agent đề xuất commit, Minh duyệt thì commit và push.

### 5a. Task khó, phiên dài

1. Thử cùng một chỗ 3 lần không được: dừng, ghi cái đã thử và kết quả vào nơi được phép ghi, đề xuất tách task hoặc đổi cách làm. Một điểm bất đồng lặp ba lần không có tiến triển thì trình nguyên bất đồng và bằng chứng cho Minh; không tạo thêm lý lẽ để làm mất bất đồng. Không đặt giới hạn ba lượt cho mọi cuộc phản biện.
2. Thấy ngữ cảnh đã bị nén, hoặc tự thấy mình lặp việc: ghi checkpoint ngay trong phạm vi được phép, rồi đề nghị Minh mở phiên mới. Người làm ghi LOG; người phản biện ghi bản phản biện của mình; phiên chỉ đọc báo trong chat.
3. Câu hỏi cho Minh gom vào một lượt ở đầu phiên. Người làm ghi câu trả lời vào mục "Quyết định của Minh trong phiên" của LOG khi có quyền; người phản biện ghi trong bản phản biện của mình; phiên chỉ đọc nêu trong chat. Quyết định cần lưu chính thức được trình ghi DECISIONS theo Luật 0.
4. Task dự kiến không xong trong một phiên: đề xuất tách ngay khi viết SPEC.

## 6. Bắt đầu một phiên

Mọi phiên, của cả hai agent, mở đầu giống nhau:

1. Đọc file này.
2. Đọc `docs/STATE.md`: task nào đang mở, ai làm, ai phản biện, đang ở bước nào.
3. Đọc `SPEC.md` của task đang mở, và **mục cuối** của `LOG.md`.
4. Chỉ đọc thêm khi cần:
   - `docs/LESSONS.md` khi thiết kế, chọn tham số, diễn giải kết quả;
   - `docs/MRP.md` khi cần phạm vi hay câu hỏi nghiên cứu;
   - `docs/WHY.md`, `docs/DECISIONS.md` khi cần lý do hay quyết định.
   Khi soạn SPEC, diễn giải hoặc phản biện kết quả, phải đọc phần mục tiêu MRP, DT18 và hướng dẫn của cô trực tiếp chi phối công việc, cùng LESSONS và các lý do/quyết định liên quan. Không chỉ dựa trên SPEC hoặc tóm tắt của LOG.
5. Kiểm các file đầu ra mà LOG nói đã có: chúng có thật không, có hợp lệ không. Không làm lại bước đã có đầu ra hợp lệ.
6. Phiên của người làm: thêm vào `LOG.md` một dòng mở phiên: ngày, agent, thiết bị, vai trò trong task. Phiên phản biện bỏ bước này (mục 9).

Câu mồi chuẩn Minh dán khi mở phiên: **"Đọc AGENTS.md, làm tiếp task đang mở trong STATE."**

Nếu STATE và LOG mâu thuẫn nhau, hoặc việc Minh giao lệch STATE: dừng, hỏi Minh.

Minh hỏi một câu ngắn thì trả lời ngắn từ các file trên, không mở nghiên cứu sâu.

## 7. Kết thúc mỗi lượt và mỗi phiên

**Cuối mỗi lượt trả lời có làm việc**, agent báo ngắn bốn mục:

1. Đã làm gì.
2. File đã thay đổi. Nếu chỉ đọc thì nói rõ: không sửa file nào.
3. Kiểm tra đã chạy và kết quả.
4. Điều chưa chắc hoặc cần Minh quyết.

Trong mục 4, phân biệt: task đã đạt gì; câu hỏi nguồn đã trả lời gì; bất đồng và câu hỏi mở nào còn lại; thiếu đúng bằng chứng gì; quyết định hoặc bước tiếp theo bị ảnh hưởng. Không báo "không còn tồn đọng" hoặc "đủ căn cứ" nếu mới kiểm số và phạm vi.

Sau mọi lượt trình SPEC, hoàn thành task, phản biện, đáp phản biện hoặc kiểm sửa, **bất kỳ agent nào cũng phải soạn prompt** để Minh copy sang agent đối phương, theo mục 9. Vẫn soạn khi đề xuất dừng. Người làm đặt prompt trong mục LOG mới khi có quyền ghi; người phản biện đặt trong bản phản biện của mình; chưa có quyền ghi file thì đưa trong chat. Minh chọn gửi hay dừng; agent không tự gửi.

**Cuối mỗi phiên của người làm**, agent chép báo cáo đó vào `LOG.md` của task, cộng thêm:

- bước tiếp theo chính xác: lệnh cần chạy, file cần đọc;
- lệnh cuối cùng đã chạy.

Rồi cập nhật dòng của task trong STATE.

Phiên phản biện không ghi LOG hay STATE. Những gì nó đã đọc và đã kiểm nằm trong `REVIEW.md` (mục 9).

Mục LOG phải đủ để **một agent khác, trên một máy khác, không có lịch sử chat**, làm tiếp được ngay.

## 8. Đổi agent giữa chừng (hết token, hết usage)

- Agent sắp hết lượt thì ưu tiên ghi mục kết thúc phiên vào `LOG.md` (mục 7) trước mọi việc khác.
- Agent nhận tiếp làm theo mục 6, rồi ghi vào LOG: "Tiếp nhận từ <agent> ngày ...; vai trò mới: ...".
- Nếu agent nhận tiếp đang là người phản biện của task:
  - nó trở thành người làm;
  - task cần một người phản biện mới khác nó.
  - Thường thì người làm cũ làm phản biện khi có token trở lại. Ghi thay đổi này vào LOG và SPEC; sửa SPEC phải được Minh duyệt.
- Nếu mục cuối của LOG không đủ để làm tiếp (ví dụ phiên trước bị cắt ngang):
  - dựng lại trạng thái từ `git status`, `git diff` và các file trong `results/T-xxx/`;
  - ghi rõ vào LOG những gì dựng lại được và những gì không chắc.

## 9. Phản biện

- Prompt mẫu và cách chạy cho từng agent: `docs/review-prompt.md`.
- Mọi prompt bàn giao chép nguyên văn "Prompt chung", đúng khối công đoạn và khối trọng tâm cổng hiện có trong `docs/review-prompt.md`. Bất kỳ bên nào soạn cũng chỉ điền thông tin trung tính; không thêm kết luận, số, gợi ý finding, mã quyết định/bài học cụ thể hoặc giới hạn khoa học riêng (Q-44, Q-88). Phạm vi ghi là thông tin quyền hạn, không là lý do thu hẹp câu hỏi cần đánh giá.
- Giữ vai trò chính thức qua các lượt. Người làm kiểm và đáp ý kiến của người phản biện, không trở thành người phản biện chính thức của task mình. Với đề xuất ngoài task, ghi vai trò dự kiến và phạm vi Minh cho phép; chưa có quyền ghi thì đánh giá trong chat.
- Tự soát yêu cầu và đầu ra gốc trước khi đọc kết luận các lượt trước. Sau đó kiểm từng điểm, kể cả phần có thể bác bỏ finding; không mặc nhiên đồng ý với bên nào.
- Người phản biện chỉ báo lỗi ảnh hưởng tới:
  - tính đúng của lập luận, phương pháp hoặc kết quả;
  - độ khớp với DT18 và hướng dẫn của cô.
  Kiểm cả tuân thủ quy trình có ảnh hưởng cụ thể: quyền ghi, duyệt phạm vi, nguồn quyết định, tự kiểm, LOG/bàn giao và trạng thái kết luận. Kiểm đạt SPEC và đạt phần mục tiêu nguồn, không chỉ đủ file hoặc khớp số. Không coi công việc hợp lệ của gói sau là lỗi hiện tại; nêu phần phụ thuộc còn thiếu.
- Mỗi điểm ghi: CHẶN hoặc KHÔNG CHẶN, chặn kết luận/quyết định nào, bằng chứng, hậu quả và sửa tối thiểu. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không yêu cầu thêm phép kiểm chỉ để "cho chắc" hoặc tự chạy vượt quyền.
- Người phản biện chỉ ghi đúng một bản lượt được Minh cho phép: `REVIEW.md` nếu chưa có, hoặc tên lượt mới lấy sau khi liệt kê thư mục; không ghi đè lịch sử, không ghi LOG/STATE. Bảng "Phản hồi của người làm" ở cuối bản đó do người làm điền, để trống cột "Minh quyết". Người làm không sửa nhận xét hay prompt của người phản biện; prompt đáp tiếp theo nằm trong LOG hoặc chat theo quyền ghi.
- Không có lỗi đáng kể thì nói thẳng là không có. Không cần tìm cho đủ số lượng.
- Góp ý của phản biện là đầu vào, không phải lệnh (LESSONS QT18). Minh quyết sửa gì.
- Sau mỗi lượt, báo các bất đồng có bằng chứng còn tồn tại, quyết định bị ảnh hưởng và câu hỏi mở. Bất kỳ bên nào không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt thì đề xuất dừng; không che bất đồng bên kia còn giữ. Minh quyết dừng, sửa, chạy bổ sung hoặc chấp nhận giới hạn. Có thể thống nhất giới hạn khi thiếu bằng chứng rồi đề xuất dừng; kết luận phụ thuộc vẫn OPEN.
- Mỗi lượt đều kèm prompt cho đối phương, kể cả khi đề xuất dừng. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, nghiệm thu task, cho phép mở test hay xác nhận giả thuyết. Không tự mở lại task đã đóng.

## 10. Văn phong

- Tiếng Việt, câu ngắn, nêu "tại sao".
- Hash và mã nằm trong manifest, không rải trong văn bản.
- Viết sao cho cô đọc hiểu mà không cần đọc repo.
- Thuật ngữ tiếng Anh giữ nguyên ở lần đầu, kèm nghĩa tiếng Việt.

## 11. Dấu hiệu đang đi sai, thấy thì dừng lại

- Đang sửa file mà Minh chưa duyệt, hoặc coi một câu hỏi của Minh là lệnh sửa.
- Đang tự viết thêm luật, phép kiểm, biên nhận thay vì trả lời một câu hỏi khoa học.
- Đang tự mở vòng review, tự gửi prompt sang agent khác hoặc tự sửa theo finding mà Minh chưa duyệt. Soạn prompt để Minh chuyển thủ công theo mục 9 là nghĩa vụ đã duyệt.
- Một con số vô lý được gọi là "giới hạn đã biết".
- Kết luận về đồ thị dựa trên một cấu hình hoặc một con số trung bình.
- Một giả thuyết khớp "đẹp" với tài liệu mà chưa xem số từng ô.
- Đang cài một phương pháp mà không có câu hỏi nào cần nó trả lời.
- Đang sửa thiết kế sau khi đã nhìn kết quả test.
- Đang đoán ý Minh.
- Dùng một kết quả làm căn cứ mà chưa nêu các nguyên nhân khả thi khác có thể giải thích nó.
- Dùng "chưa kiểm" như sự thật, hoặc coi task xong là câu hỏi nghiên cứu đã được trả lời.
- Bỏ nhóm quan trọng vì thiếu trung gian hoặc ngoài SPEC mà không trình phần bằng chứng cần bổ sung và quyết định phụ thuộc.
- Quy lỗi cho dataset chỉ từ cờ thiếu dữ liệu, hoặc chọn cơ chế đồ thị chỉ vì đã dẫn một mã hạn chế.
- STATE dài hơn một trang, hoặc LOG thiếu mục kết thúc phiên.

## 12. Môi trường và thiết bị

- Windows 11. Có PowerShell và Git Bash. Python 3.12 gọi bằng `py -3`. Codex CLI 0.130.0.
- Laptop i5-1240P, RAM 16 GB, không có GPU NVIDIA. Ổ D còn khoảng 65 GB (kiểm ngày 02/10/2026).
- Repo hệ thống FlashTicket: `D:/Project/flash-ticket-platform`. Chỉ đọc. Chuẩn quan sát ở `docs/architecture/B16-observability-baseline.md`.
- **Máy mới:**
  1. Clone repo từ remote.
  2. Dựng dữ liệu theo `data/README.md`.
  3. Dựng môi trường Python theo hướng dẫn trong repo (sẽ ghi ở đây khi có code đầu tiên).
  4. Đọc file này và STATE.

  Không cần gì từ máy cũ ngoài repo.
