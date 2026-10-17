# Phản biện T-037

- **Người phản biện:** Codex, phiên sạch độc lập được Minh chỉ định thay Claude — **Ngày:** 16/10/2026.
- **Công đoạn/cổng và bản lượt:** soát kết quả toàn T-037; P5, chuẩn bị G3; REVIEW.md. Chưa có file REVIEW kết quả T-037 trước lượt này.
- **Phạm vi đối chiếu:** nguồn thiết kế đã ghim; bản ghi và graph hiện hành; manifest trước V2 với bản hiện hành; snapshot R1 và mã chung hiện hành. Không chọn HEAD thay nội dung nguồn hoặc pin.
- **Đã đọc:** AGENTS.md; STATE; toàn SPEC và các mục LOG liên quan T-037; MRP phần RQ3/RQ5/P5/P6/P9/G3; DT18, hướng dẫn của cô, LESSONS, WHY-52/53 và quyết định liên quan; registry, coverage, bản ghi, địa chỉ tín hiệu, hợp đồng runtime, oracle/fixture, các đầu ra T-037 và code do_thi/do_thi_tinh. Nguồn platform được đối chiếu chỉ đọc theo AGENTS.md và skill govern-capstone-work; dùng B11-C/B12/B13/B14/B16, sơ đồ và định nghĩa dữ liệu được ghim. Lịch sử công cụ và REVIEW T-036 được đọc sau khi tự soát đầu ra gốc.
- **Tự soát độc lập:** đọc nguồn, code và kết quả thật trước kết luận phản biện/phản hồi lịch sử; tính lại trong bộ nhớ. Không dùng subagent hoặc tạo run trong lượt phản biện.

## Kết luận chung

Không phát hiện lỗi đáng kể còn chưa xử lý trong mô hình thiết kế FlashTicket và tiếp nhận SMTP V2 của T-037. Đầu ra đáp ứng phần mô hình nguồn thiết kế và bàn giao có điều kiện của các tiêu chí SPEC; phục vụ DT18-NV2, bước 1 của cô và MRP P5. Đây chưa là xác nhận runtime, lợi ích RCA, lựa chọn P6 hoặc hoàn tất toàn P5b/RQ3/RQ5/G3.

Minh đã đồng ý dừng phản biện, nghiệm thu và đóng T-037 ngày 16/10/2026. Quyết định và ngoại lệ phân công được ghi riêng ở docs/DECISIONS.md; mốc đóng ở LOG Phiên 4 và dòng T-037 trong STATE. SPEC, manifest và kết quả giữ snapshot trước nghiệm thu; những câu chờ Claude hoặc chưa nghiệm thu trong snapshot lịch sử không thay quyết định đóng hiện hành.

## Quyền và ngoại lệ phân công

Lời giao phản biện của Minh ghi: “Minh chỉ định Codex phiên mới hoàn toàn này làm người phản biện chính thức kết quả thay Claude.” Task được chỉ định là T-037. Đây là ngoại lệ phản biện **kết quả**, khác ngoại lệ soát ba SPEC trước đó; Codex phiên triển khai vẫn là người làm, phiên này không chuyển sang vai trò người làm.

Sau báo cáo chỉ đọc, Minh yêu cầu nguyên văn: “Đồng ý dừng phản biện, nghiệm thu và đóng T-037 giúp tôi. Lưu bản phản biện và ghi nhận ngoại lệ phân công, giữ nguyên các OPEN, chưa commit/push.” Minh tiếp tục xác nhận “Duyệt đúng bốn file” sau khi trình gói REVIEW.md, DECISIONS.md, LOG.md T-037 và đúng dòng T-037 trong STATE.md. Quyền này cho ghi nhận đóng và ngoại lệ; không sửa luật, phân công lịch sử của SPEC, code, kết quả hoặc task khác.

## Các điểm

Không có finding CHẶN hoặc KHÔNG CHẶN mới cần xử lý. Không biến công việc runtime hoặc thực nghiệm của gói sau thành lỗi hiện tại, cũng không coi việc nghiệm thu mô hình là đã hoàn tất các nghĩa vụ đó.

## Đối chiếu các lượt trước

Không có REVIEW kết quả T-037 trước bản này. Các điểm tự soát trong LOG và lịch sử hợp đồng được kiểm sau nhận xét độc lập:

- **SMTP bị thiếu trong hợp đồng nền và oracle ban đầu xếp SMTP vào HTTP: đúng, đã xử lý trong đầu ra hiện hành.** B13 §6, B14 §6 và B14-03 nêu Ticket gửi SMTP ngoài transaction. Bản ghi hiện hành giữ Ticket→SMTP với channel smtp, type gọi-chưa-phân-kiểu; không giả thành HTTP, không có broker giả và runtime_name vẫn null. Bản oracle sai và các lượt lỗi còn được giữ. Bổ sung builder và comparator có quyền riêng; nội dung sửa đúng delta đã duyệt.
- **R1 về khóa consume: đúng và đã sửa ở hợp đồng chung.** Code hiện hành so chặng nhận bằng broker/scope/queue, giữ exchange/routing trong thành viên gốc. Fixture hai queue tính lại cho cả endpoints và typed: numerator=2, static_denominator=3, trace_denominator=2. Khớp chặng nhận không được diễn giải thành xác minh routing/binding hoặc bản tin runtime. Không mở lại T-036 đã đóng.
- **Lý do thiếu mapping operation của fixture consume nằm ở target: đúng.** Tính lại fixture hiện hành cho hai exclusion unmapped:target, không giao nhau và không tạo operation giả. Việc sửa oracle v3 không đổi chính sách mapping hoặc dữ liệu fixture để theo điểm.
- **Callback, scheduler, correlation, fan-out và retry:** các giới hạn đã khai phù hợp đầu vào fixture và code. Tính lại sáu fixture trace trùng graph đã lưu; correlation không tự nối message/callback, scheduler không có caller giả. Đây là bằng chứng hợp đồng tổng hợp, không chứng minh FT runtime đã sinh dữ liệu tương đương.

Bằng chứng hiện hành: results/T-037/runs/doi-chieu-smtp-001/checks/full-model-001/{fixture-trace-graphs.json,fixture-compare-two-queues.json,fixture-compare-missing-operation.json,fixture-compare-missing-address.json,fixture-compare-unknown.json}; oracle-v3.json và các bản lịch sử trong manifest.

## Tuân thủ quy trình

- Quyền triển khai, bổ sung SMTP và V2 được đối chiếu với authorization, LOG, DECISIONS và plan đã duyệt; không suy quyền từ việc công cụ cũ được nghiệm thu.
- Trước dùng đã kiểm hash manifest T-037, pin chung V2, đầu vào T-035 và registry nguồn. Pin V2 cùng nhau ở FT/TT/OB; snapshot và mã live khớp pin hiện hành.
- Manifest R1 lịch sử có checksum của build.py, compare.py, README.md khác mã live sau các bổ sung đã được duyệt. Đã đối chiếu đúng snapshot R1: nội dung cũ còn khớp; delta builder chỉ thêm smtp tại hai guard, delta comparator nhận optional call channel và marker SMTP. Đây là khác phiên bản có nguồn quyền, không thay checksum cũ để hợp thức hóa mã mới.
- So manifest T-037 trước V2 với hiện hành: không mất tệp; chỉ ba báo cáo/bàn giao/prompt hiện hành đổi trong danh sách payload cũ được so. Bản ghi, nguồn và hai graph giữ nguyên byte; builder không đổi trong V2. SPEC/LOG và WHY/DECISIONS trước gói V2 được nối thêm theo quyền.
- Lượt phản biện chỉ đọc không ghi file, không thực nghiệm mới, không đọc dữ liệu khóa/telemetry thô, không tải nguồn, không bật EC2 hoặc commit/push.
- Lượt lưu và đóng chỉ ghi đúng bốn file Minh duyệt. LOG chỉ nối mốc đóng/ngoại lệ theo quyền cụ thể của lượt này; người phản biện không nhận vai trò người làm. Giữ mọi OPEN và các bản trước.

## Điều đã kiểm và thấy đúng

Số lưu hiện hành ở results/T-037/runs/doi-chieu-smtp-001/checks/full-model-001/result.json: #/all_pass=true, #/passed=1598, #/failed=0. Đây là số của lượt triển khai đã lưu; lượt phản biện không tuyên bố chạy lại toàn checker có ghi file.

Các kiểm độc lập đã chạy bằng Python inline -X utf8 -B, chỉ đọc và tính trong bộ nhớ:

1. Hash/bytes: 312 payload T-037, 71 payload pin V2, 5.667 mục T-035 và 34 nguồn live/snapshot khớp manifest tương ứng. Khi chuẩn bị lưu bản này, kiểm lại 312 và 71 mục vẫn khớp.
2. Gọi API thuần build/project trên ban-ghi.json và nguon.json, so toàn JSON với graph hiện hành và run V2; đều bằng nhau, input không đổi. Gộp cạnh độc lập theo đầu mút/type/channel/messaging và tập record_ids cũng khớp.
3. Kết quả tính lại trùng #/stats: 32 thực thể, 65 tên thao tác thiết kế, 115 quan hệ nguồn, 72 cạnh thực thể, 55 cạnh thao tác, 17 cạnh chiếu, 14 binding, 153 địa chỉ tín hiệu; 23 signal dùng chung. Inventory không tự thành observed nodes hoặc tập ứng viên P6.
4. Tính lại sáu trace_cases từ fixtures-runtime-v2.json bằng T-035 và bốn fixture compare bằng V2: mọi JSON trùng bản lưu, input giữ nguyên. Kiểm độc lập các tập S/T/giao/phần riêng, thành viên, exclusion và mẫu số đều nhất quán. Unknown SMTP với trace thiếu channel không khớp endpoints; typed loại unknown ở cả phía.
5. Đối chiếu 239 original_source_text trong bao-phu-nguon.json#/units với đúng dòng snapshot: không sai lệch. Đối chiếu tên bảng SQL với dictionary B12: đủ 47, phân theo owner 12/15/13/7. Nguồn số kiểm tương ứng ở runs/assemble-002/semantic-source-audit.json và coverage-resolution.json.
6. Kiểm 652 đơn vị coverage: các record/entity được dẫn tồn tại; mục OPEN có owner và required_input. Toàn bộ 65 operation và signal_ids trong dia-chi-tin-hieu.json khớp bản ghi; chỉ mục signal dùng chung khớp. Tham chiếu hợp lệ và số đếm không tự thay bằng chứng nghĩa từ nguồn.

Nút/cạnh, địa chỉ log/trace/metric, DB logic khác instance và tài nguyên dùng chung được giữ rõ. P5 dùng cạnh để gộp, chiếu và đối chiếu cấu trúc; chưa có điểm bất thường hoặc xếp hạng trong T-037. Chưa có baseline/đối chứng hiệu quả RCA của T-037 để diễn giải như một kết quả RQ3.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** phản biện độc lập từ nguồn/đầu ra thật, sau đó đối chiếu lịch sử; lưu bản này và ghi nhận nghiệm thu/đóng theo Minh duyệt.
2. **File thay đổi:** tạo tasks/T-037-p5b-flashticket/REVIEW.md; nối docs/DECISIONS.md và LOG.md T-037; chỉ đổi dòng T-037 trong docs/STATE.md. Không sửa SPEC, code, kết quả hoặc OPEN.
3. **Kiểm và kết quả:** các kiểm độc lập được liệt kê ở trên đều khớp. Lượt lưu kiểm diff/phạm vi bốn file, tính nối thêm, đúng dòng STATE, prompt nguyên văn và hash kết quả được bảo vệ; kết quả kiểm sau ghi báo trong chat. Không tạo run để ghi nhận việc đóng.
4. **Bất đồng/phần thiếu:** không còn phản đối có bằng chứng ảnh hưởng nghiệm thu phần mô hình thiết kế/SMTP V2 đã kiểm. Bảy nhóm OPEN tại bao-phu-nguon.json#/open_items giữ nguyên: queue/scope; operation runtime; deployment/resource; config/identity; pipeline; quyền/UI/retention; thiết kế và đánh giá RCA. Chủ nguồn/service/nhóm nền tảng và P9 cần cung cấp build/image/config/export, mapping và telemetry thực. T-040 nhận tổng hợp; P6 cần phép dùng cạnh/binding và bằng chứng dev; P7/P10 còn đánh giá lợi ích. RQ3/RQ5/G3 chưa đóng, test chưa được mở.

**Dừng phản biện theo Minh quyết.** Nghiệm thu T-037 trong phạm vi mô hình thiết kế và bàn giao có điều kiện, không là bằng chứng runtime hay lợi ích RCA. Không tự sinh lượt đáp hoặc mở lại task từ prompt lưu dưới đây. Nội dung nên vào báo cáo: phạm vi nguồn thiết kế, logical DB/instance chung, điều kiện ghép message, địa chỉ tín hiệu và giới hạn xác minh runtime.

## Prompt bàn giao cho người làm

Prompt lưu để giữ nghĩa vụ bàn giao. Minh đã quyết đóng task; chỉ dùng khi Minh giao tiếp, không tự gửi hoặc tự mở lại task.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-037; D:/RCA-flashticket/tasks/T-037-p5b-flashticket/SPEC.md và LOG.md; kết quả D:/RCA-flashticket/results/T-037.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex phiên triển khai là người làm; Codex phiên sạch độc lập là người phản biện chính thức kết quả theo ngoại lệ Minh chỉ định. Phiên nhận prompt giữ vai trò người làm; phân công lịch sử trong SPEC giữ nguyên.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; SPEC.md và LOG.md của T-037, gồm phụ lục; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; results/T-037/nguon.json và các nguồn được dẫn. Repo D:/Project/flash-ticket-platform chỉ đọc theo AGENTS.md và skill govern-capstone-work tại đó.
- Phản biện và phản hồi trước: lịch sử tại tasks/T-037-p5b-flashticket/LOG.md và results/T-037/runs/; lịch sử hợp đồng tại tasks/T-036-p5b-hop-dong-chung/; bản phản biện kết quả T-037 tại tasks/T-037-p5b-flashticket/REVIEW.md.
- Code và kết quả liên quan: src/do_thi/, src/do_thi_tinh/; results/T-035/manifest.json; results/T-036/runs/doi-chieu-smtp-001/manifest.json và snapshot code được dẫn; results/T-037/manifest.json, runs/doi-chieu-smtp-001/pin.json, checks/, diff.json; results/T-038/runs/cap-nhat-goi-smtp-001/package/plan.json. Windows/Python 3.12; môi trường theo README và tài liệu task.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa có quyền sửa REVIEW, LOG, STATE, SPEC, quyết định, code hoặc kết quả trong lượt đáp. Không chạy script có ghi file, thực nghiệm mới, tải nguồn, bật EC2, mở dữ liệu khóa, dùng subagent hoặc tự mở/gửi chat. Có thể kiểm hash và tính lại độc lập trong bộ nhớ từ dữ liệu đã được phép đọc. Không dùng quyền triển khai cũ hoặc prompt này để tự mở lại task đã đóng.

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

Bảng để trống. Không có lượt đáp được tự mở từ việc lưu bản này; chỉ điền khi Minh giao trong phạm vi rõ ràng. Người làm không sửa nhận xét hoặc prompt của người phản biện.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|

