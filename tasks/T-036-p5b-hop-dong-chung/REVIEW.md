# Phản biện T-036

- **Người phản biện:** Codex, phiên độc lập được Minh chỉ định thay Claude — **Ngày:** 15/10/2026.
- **Công đoạn/cổng và bản lượt:** soát kết quả toàn bộ T-036; P5, chuẩn bị G3; REVIEW.md.
- **Vai trò và quyền:** Minh cho phép ngoại lệ hai phiên Codex giữ vai trò người làm/người phản biện. Lượt phản biện ban đầu chỉ đọc và trả lời chat. Sau báo cáo đó, Minh nói “đóng task giúp tôi”, duyệt gói đã trình gồm REVIEW.md, DECISIONS.md, nối LOG.md và đúng dòng T-036 trong STATE.md. Việc ghi nhận đóng task không đổi vai trò, không phải một lượt tự phản biện của người làm và không sửa phân công lịch sử trong SPEC.
- **Diff đã đọc:** results/T-036/runs/ket-phien-001/changes.diff; results/T-036/runs/sua-r1-001/changes.diff; đối chiếu code hiện hành và các bản trước.
- **Đã đọc:** AGENTS.md; STATE; SPEC T-036; MRP phần mục tiêu/RQ3/RQ5/P5–P7/P9/G3; DT18; hướng dẫn của cô; LESSONS; WHY-52/53 và quyết định liên quan; toàn bộ code do_thi_tinh; hợp đồng, registry, fixture, các đầu ra được dẫn dưới đây; hợp đồng/code liên quan của T-035; các nguồn trong registry. Nguồn thiết kế FlashTicket B11-C/B12/B13/B14/B16 được đọc theo luật và skill govern-capstone-work của repo hệ thống, chỉ dùng làm nguồn thiết kế.
- **Tự soát độc lập:** nguồn và đầu ra gốc/code được soát trước khi đối chiếu các kết luận lịch sử trong LOG và lượt sửa. Hai nhánh hỗ trợ kỹ thuật/nguồn chỉ đọc cung cấp đầu vào cho người phản biện; không là các vòng phản biện chính thức riêng.

## Kết luận chung

Không phát hiện lỗi đáng kể còn chưa xử lý trong hợp đồng và công cụ chung T-036. Trong phạm vi đã kiểm, đầu ra đáp ứng các tiêu chí xong của SPEC và cung cấp phần biểu diễn/đối chiếu có điều kiện của P5. Đề xuất dừng phản biện và nghiệm thu phần công cụ; chưa hoàn thành toàn P5b/RQ3/RQ5/G3, chưa xác nhận runtime hoặc lợi ích RCA.

**Trạng thái sau phản biện:** Minh đã yêu cầu đóng T-036 bằng lời “đóng task giúp tôi”. Quyết định được ghi ở docs/DECISIONS.md, Q-158; LOG Phiên 4 và dòng T-036 trong STATE là mốc đóng. SPEC, manifest và báo cáo triển khai giữ nguyên snapshot trước nghiệm thu, không dùng các câu chờ phản biện trong snapshot đó thay cho trạng thái hiện hành.

## Các điểm

Không có finding CHẶN hoặc KHÔNG CHẶN mới cần xử lý. Không tạo finding chỉ vì thiếu kết quả thuộc các task tiếp theo.

## Đối chiếu các lượt trước

**R1 về khóa địa chỉ consume: đúng và đã sửa.** Comparator trước sửa dùng thêm exchange/routing trong khóa chặng nhận, nên hai phía cùng broker/scope/queue nhưng khác độ chi tiết địa chỉ nguồn phát có thể không giao nhau. Bản hiện hành chỉ lấy trường cần cho từng vai trò và giữ địa chỉ đầy đủ trong graph/members.

Bằng chứng:
- src/do_thi_tinh/compare.py: phần normalized chọn required và address theo channel; hop-dong.md §3 phân biệt khớp chặng nhận với xác nhận routing/binding/bản tin.
- fixtures/r1.json và runs/kiem-r1-after-002/r1-regression.json#/cases giữ các trường hợp hai mức/hai phép so, queue/scope khác, địa chỉ thiếu và thành viên gốc.
- runs/kiem-r1-before-002/result.json#/failed là 22; hai bản sau sửa tại runs/kiem-r1-after-001 và runs/kiem-r1-after-002 có #/passed = 221 và #/failed = 0.
- Tái lập độc lập trong bộ nhớ bằng Python -X utf8 -B: nạp comparator bản trước ở runs/sua-r1-001/before/src/do_thi_tinh/compare.py, so cùng một consume có địa chỉ nguồn phát bổ sung với cạnh T-035 đã lưu. Cả endpoints và typed: bản trước (numerator, static_denominator, trace_denominator) = (0,1,1); bản hiện hành = (1,1,1).
- Khớp consume không chứng minh exchange/routing, binding hay bản tin runtime. Các phần đó không bị nâng thành bằng chứng đã xác nhận. Không còn phản đối chưa xử lý đối với R1 trong phạm vi đã kiểm.

Các nhận xét tự soát trong LOG về DB logic/instance, ngoại lệ span-parent, alias/miền/revision và giới hạn fixture phù hợp nguồn và code hiện hành. Không có file REVIEW chính thức trước bản này để mặc nhiên kế thừa kết luận.

## Tuân thủ quy trình

- Quyền triển khai theo SPEC/Q-157 và quyền sửa R1 được lưu tại runs/sua-r1-001/authorization.txt; chưa thấy thay đổi ngoài phạm vi qua các diff và bản trước được lưu.
- Đối chiếu bản trước với hiện hành: LOG chỉ nối thêm; STATE chỉ đổi dòng T-036; SPEC và nguồn bảo vệ khớp hash preflight. Oracle gốc và các lượt lỗi được giữ.
- Trước sử dụng đã kiểm hash: 187 mục manifest T-036, 15 nguồn registry và ba manifest phụ thuộc khớp. Các graph dev đọc trong bộ kiểm được kiểm hash theo manifest T-035.
- Phiên phản biện không sửa code/kết quả, không tạo run trên đĩa, không mở trace thô/test/dataset khóa, không tải nguồn, không commit/push.
- Bốn file ghi nhận đóng là ngoại lệ được Minh duyệt trực tiếp sau báo cáo phản biện. Không suy quyền này thành quyền sửa SPEC, WHY, kết quả, code hoặc task sau.

## Điều đã kiểm và thấy đúng

- Bản ghi → owner/ID/kiểu/địa chỉ → cạnh/chiếu → tập/mẫu số có trung gian và đáp án literal; unknown không thành sync; địa chỉ bắt buộc thiếu bị loại cả khi hai phía cùng thiếu.
- Mapping operation đòi owner nhất quán; cạnh nội bộ sau alias ở mức entity bị loại có lý do. Inventory không tự thành observed_nodes hoặc tập ứng viên RCA.
- Hai DB logic giữ riêng, một instance PG chung và binding có nguồn; metric chung không nhân thành bằng chứng operation. Phần mapping tương đương chưa có ở trace được bàn giao rõ.
- Publish/consume/logical-message phân biệt vai trò; nhiều queue cùng consumer giữ riêng; không tự nối bản tin chỉ từ broker/correlation. Khớp HTTP/RPC trong typed chỉ xác nhận mức kiểu mà T-035 biểu diễn, chưa xác nhận transport.
- API không nhận nhãn để chọn quan hệ; phép tính này dùng cạnh để chuẩn hóa khóa và tính giao/phần riêng, chưa tính điểm bất thường hoặc xếp hạng RCA.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** soát toàn task từ nguồn/đầu ra thật, đối chiếu tiêu chí SPEC và mục tiêu nguồn; sau đó kiểm lịch sử R1 và quyền sửa.
2. **File thay đổi:** lượt phản biện ban đầu không sửa file. Lượt Minh duyệt đóng lưu bản này, nối DECISIONS/LOG và chỉ đổi dòng T-036 trong STATE; không thay code, kết quả hoặc quyết định khoa học.
3. **Kiểm và kết quả:** phát lại checker trong bộ nhớ, giữ nguyên phần tính/kiểm và vô hiệu hóa mkdir, snapshot/progress/save ra đĩa: 221/221 đạt, tương thích 312 graph và khớp 156 cặp chiếu. Đối chiếu đầu ra sau chuẩn hóa JSON với bản lưu hiện hành đều khớp ở các đầu ra được so. Số lưu tại results/T-036/runs/kiem-r1-after-002/result.json, các con trỏ #/passed, #/failed, #/compatibility_graph_count, #/trace_projection_pair_count. Lượt inline chỉ đọc không tạo artifact run; lệnh R1 và kết quả được mô tả ở trên. Git status sau lượt chỉ đọc giữ nguyên; manifest không lệch.
4. **Bất đồng/phần thiếu:** không còn phản đối có bằng chứng ảnh hưởng nghiệm thu công cụ trong phạm vi đã kiểm. T-037–040 còn khảo sát/đối chiếu đầy đủ ba hệ và tổng hợp; T-038/039 còn truy revision sinh dữ liệu; P9 còn runtime, telemetry và mapping tài nguyên; P6/P7/P10 còn chọn/đánh giá phương pháp và lợi ích. Nơi nhận, đầu vào thiếu và quyết định phụ thuộc ở results/T-036/ban-giao.md §2–3. T-035 không tự được nghiệm thu bởi việc đóng T-036.

**Đề xuất dừng phản biện:** không còn lỗi đáng kể cần xử lý ở phần công cụ. Minh đã quyết đóng T-036; không mở thêm vòng phản biện hoặc task từ prompt dưới. Nội dung nên vào báo cáo đồ án: phân biệt thiết kế/quan sát/lợi ích, DB logic/instance, địa chỉ messaging/metric shared và mẫu số cấu trúc có điều kiện.

## Prompt bàn giao cho người làm

Prompt được lưu để giữ nghĩa vụ bàn giao của lượt phản biện. Minh chọn sử dụng; bản này không tự cho phép mở lại task đã đóng.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-036; D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/SPEC.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex ở các phiên triển khai và sửa là người làm; Codex trong phiên độc lập là người phản biện chính thức theo ngoại lệ Minh chỉ định. SPEC/LOG/STATE giữ phân công lịch sử. Phiên nhận prompt này giữ vai trò người làm.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; tasks/T-036-p5b-hop-dong-chung/SPEC.md và LOG.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; results/T-036/nguon.json và các nguồn được registry liệt kê.
- Phản biện và phản hồi trước: lịch sử tại tasks/T-036-p5b-hop-dong-chung/LOG.md và results/T-036/runs/; bản phản biện chính thức tại tasks/T-036-p5b-hop-dong-chung/REVIEW.md.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-036/manifest.json; hop-dong.md; nguon.json; fixtures/; runs/; kiem-dung-dan.md; ban-giao.md; src/do_thi_tinh/README.md và code; results/T-035/manifest.json và các đầu vào SPEC liệt kê. Diff tại results/T-036/runs/ket-phien-001/changes.diff và results/T-036/runs/sua-r1-001/changes.diff. Windows/PowerShell; Python theo README.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC, DECISIONS, code hoặc kết quả. Không thực hiện quyền triển khai từ SPEC trong lượt đáp này.

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

## Phản hồi của người làm (người làm điền sau)

Giữ trống; không dựng một lượt đáp phản biện chưa diễn ra. Minh đã nghiệm thu trực tiếp; người phản biện không điền thay người làm hoặc cột Minh quyết.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
