# Nhật ký T-036

Chỉ nối thêm. Codex người làm; Claude phản biện chính thức.

## Phiên 1 — 15/10/2026 — Codex — LEVANMINH — vai trò: người làm

**Mở phiên:** đọc AGENTS, STATE, template và kiểm thư mục task. Chưa có T-036, chưa có đầu ra triển khai. Phiên này ghi tài liệu từ phương án đã được Minh duyệt và bàn giao phiên sạch; không triển khai code.

**Quyết định của Minh trong phiên:**
- Trước đó Minh đồng ý phương án chia P5b thành T-036–T-040; lựa chọn độ sâu là “thực thể đầy đủ; thao tác khi có bằng chứng”.
- Nguyên văn lời duyệt hiện tại: “duyệt spec 36 , sau đó tạo 1 prompt cho phiên codex mới hoàn toàn, yêu cầu triển khai task, tuy nhiên trước khi làm yêu cầu codex đọc và phản biện spec trước, nêu có phần chưa ổn thì dừng lại yêu cầu sửa spec rồi mới làm tiếp”. Đã ghi Q-157 trong docs/DECISIONS.md.
- Phạm vi ghi chuẩn bị theo bảng file phương án: SPEC/LOG T-036, DECISIONS, WHY và trạng thái liên quan trong STATE. Không tạo task sau hoặc đầu ra thực thi.

**Diễn biến:**
- Đọc phương án đính kèm, xác nhận chưa có SPEC T-036 trên đĩa; ghi phần hợp đồng chung thành SPEC. Lưu nguyên văn phần nội dung phương án bên dưới để phiên sạch đối chiếu, không coi đây là kết quả tự soát độc lập.
- Ghi quyết định trước, lý do WHY-53, SPEC/LOG và dòng trạng thái T-036. Ghi hai prompt riêng: Codex triển khai có điều kiện tự soát, Claude soát SPEC chỉ đọc.

**Kết thúc phiên:**
1. Đã ghi SPEC và bàn giao; chưa có kết quả khoa học/công cụ T-036. Chưa trả lời toàn P5b/RQ3/RQ5.
2. File thay đổi: docs/DECISIONS.md, docs/WHY.md, docs/STATE.md, tasks/T-036-p5b-hop-dong-chung/SPEC.md, tasks/T-036-p5b-hop-dong-chung/LOG.md. Giữ nguyên thay đổi có sẵn.
3. Kiểm chuẩn bị: task chưa tồn tại, mã quyết định/lý do không trùng; nguồn prompt lấy trực tiếp từ mẫu. Kiểm sau ghi sẽ nối riêng, không coi kiểm tài liệu là tự soát triển khai đã đạt.
4. Còn OPEN: phiên sạch tự soát SPEC, độ đủ biểu diễn của hợp đồng, revision dataset–ứng dụng và telemetry FT. Chưa chọn P6, nghiệm thu T-035/T-036 hay duyệt task sau. Không có kết luận phản biện chính thức T-036; tiếp tục bước tự soát theo yêu cầu Minh.
5. Bước tiếp: mở phiên Codex mới tại D:/RCA-flashticket; đọc SPEC, AGENTS/STATE và nguồn gốc; dùng prompt dưới. Cần sửa SPEC thì dừng, trình Minh. Không cần bật EC2/tải repo ở bước này.
6. Lệnh cuối bước ghi: Python inline tạo tài liệu được duyệt và kiểm diff phần thay đổi của phiên; không chạy builder hoặc thực nghiệm.

## Prompt Codex mới — tự soát trước, không có vấn đề mới triển khai

```text
Bạn là Codex trong phiên mới hoàn toàn tại D:/RCA-flashticket. Minh yêu cầu triển khai T-036, nhưng trước khi làm phải đọc và tự phản biện SPEC từ nguồn như lần đầu. Không dựa vào nhận xét thuận lợi hoặc lịch sử chat để mặc định SPEC đúng.

Đọc AGENTS.md, docs/STATE.md, tasks/T-036-p5b-hop-dong-chung/SPEC.md và phần mở/kết thúc phiên hiện hành của LOG.md để xác định quyền. Lời duyệt và phương án gốc đã lưu trong LOG; docs/DECISIONS.md ghi quyết định. Codex vẫn là người làm, Claude là người phản biện chính thức. Tự soát lần này không thay phản biện Claude.

Trước triển khai, đọc trực tiếp nguồn DT18/cô, MRP, LESSONS, WHY/DECISIONS liên quan và các đầu vào SPEC liệt kê; với repo hệ thống đọc luật và skill bắt buộc, chỉ đọc nguồn hiện hành. Đọc đầu ra/code gốc và lập nhận xét độc lập trước khi mở kết luận các lượt rà soát/phản biện cũ. Dùng nguyên văn Prompt chung, khối Soát SPEC và khối G3 trong docs/review-prompt.md làm tiêu chí tự soát; quyền của bạn theo SPEC và yêu cầu triển khai này, không lấy quyền chỉ đọc của prompt Claude trong LOG để thay vai trò.

Kiểm mục tiêu nguồn, độ đầy đủ phạm vi, phụ thuộc, quyền ghi, bằng chứng phân xử, tiêu chí xong, chi phí và tính nhất quán hợp đồng. Kiểm hash đầu ra cũ theo manifest trước khi dùng. Đừng chỉ kiểm đủ mục hoặc cho rằng Minh duyệt tức thiết kế đã đúng.

Nếu phát hiện phần chưa ổn cần sửa SPEC, hoặc mâu thuẫn nguồn/quyền/phụ thuộc ảnh hưởng triển khai: DỪNG triển khai. Nêu vị trí, bằng chứng, hậu quả, CHẶN/KHÔNG CHẶN và sửa tối thiểu theo file; trình Minh duyệt sửa SPEC rồi mới làm tiếp. Không tự sửa SPEC, đổi thiết kế, giảm phạm vi hay tự xử lý finding như một lệnh sửa. OPEN thuộc task sau không tự là lỗi SPEC; nêu đúng phụ thuộc và bằng chứng thiếu.

Nếu không có vấn đề cần sửa SPEC: báo rõ kết quả tự soát, ghi vào LOG, rồi tiếp tục triển khai ngay theo SPEC đã duyệt, không xin lại quyền đã có. Chỉ ghi results/T-036/, bốn file src/do_thi_tinh/ được SPEC liệt kê, nối LOG T-036 và cập nhật đúng dòng T-036 trong STATE. Khóa SPEC; mọi thay đổi ngoài phạm vi phải trình Minh.

Thực hiện đủ bước và kiểm đúng đắn của SPEC; giữ mọi lượt kể cả lỗi. Không làm T-037–040, không sửa T-035/platform, không mở test/heldout/repo lưu trữ, không tải repo/dataset, bật EC2, commit/push hoặc tự mở/gửi chat. Không tự dùng subagent. Nếu có thao tác tốn kém hoặc phải mở rộng phạm vi thì báo trước đúng AGENTS.

Cuối phiên kiểm toàn bộ diff và file đã đổi, đối chiếu kết quả với câu hỏi nguồn; ghi LOG đầy đủ bước tiếp/lệnh cuối, trạng thái và phần OPEN. Soạn prompt Claude soát kết quả (hoặc soát SPEC nếu bị chặn) bằng nguyên văn mẫu hiện hành để Minh chuyển thủ công. Không tự đóng task, chốt P6 hoặc mở G3/test.
```

## Prompt Claude — soát SPEC (Minh chọn chuyển; không tự gửi)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-036; D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/SPEC.md.
- Công đoạn: soát SPEC.
- Gói/cổng: P5; G2 đã duyệt, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện chính thức.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/DECISIONS.md; docs/WHY.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; tasks/T-036-p5b-hop-dong-chung/SPEC.md và LOG.md; các nguồn đầu vào được SPEC liệt kê.
- Phản biện và phản hồi trước: chưa có phản biện chính thức T-036.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-035/manifest.json, dac-ta-do-thi.md, thong-tin-theo-quan-he.md; src/do_thi/README.md và code; manifest nguồn T-002/T-003 được SPEC liệt kê; Windows/PowerShell.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; không ghi REVIEW, SPEC, LOG, STATE, code hoặc kết quả.

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

## Phương án gốc Minh đính kèm khi duyệt — lưu lịch sử

Bản dưới là nguyên văn nội dung trước lời duyệt. Các câu “chưa duyệt/CANDIDATE” mô tả thời điểm đề xuất. Lời duyệt hiện hành ở đầu phiên và Q-157; phạm vi thực thi phiên tới chỉ T-036 theo SPEC, không toàn gói.

**Tôi đề xuất giữ trọn phạm vi P5b và chia thành năm task**, với FlashTicket được khảo sát đầy đủ từ thiết kế đã duyệt. Lựa chọn **“thực thể đầy đủ; thao tác khi có bằng chứng”** đã được Minh xác nhận; tôi không hỏi lại.

Đây là **phương án tổ chức và nội dung để lập SPEC**, chưa thay phạm vi T-036 trong repo, chưa cấp quyền triển khai. Codex giữ vai trò người làm; Claude phản biện chính thức.

**1. Phạm vi và câu hỏi P5b phải trả lời**

P5b phục vụ DT18-NV2, bước xây dựng đồ thị của cô và MRP P5; chuẩn bị đầu vào cho RQ3 và thử nghiệm FlashTicket ở RQ5. Nó cần trả lời:

| Câu hỏi | Bằng chứng phải có | Kết luận được phép |
|---|---|---|
| Mỗi hệ gồm những thực thể và quan hệ nào? | Danh mục có nguồn, phiên bản, vị trí trích dẫn và điều kiện áp dụng | Những quan hệ được thiết kế, cấu hình hoặc code xác định |
| Có thể biểu diễn các quan hệ đó bằng hợp đồng T-035 không? | Ánh xạ cụ thể và ví dụ kiểm có đáp án độc lập | Biểu diễn được tới đâu; thông tin nào còn mất hoặc chưa có địa chỉ |
| Đồ thị tĩnh và đồ thị trace khớp ở đâu? | Ánh xạ thực thể, miền so sánh, tập giao và phần khác biệt hai chiều | Mức khớp trong miền đã xác định |
| Chênh lệch đến từ đâu? | Lần theo nguồn → chuẩn hóa → ánh xạ → cạnh → kết quả so sánh | Giải thích đã xác minh, đã loại trừ hoặc còn OPEN |
| FlashTicket phải cung cấp gì để kiểm bằng runtime? | Bảng quan hệ/thao tác → trường cần → nguồn ghi → phép kiểm | Đầu vào cụ thể cho P9a/P9b và thử nghiệm sau này |

P5b chưa trả lời đồ thị giúp phát hiện hoặc xếp hạng tốt hơn hay không. Phần đó cần phương pháp và đánh giá ở P6/P7/P10.

**2. Phạm vi FlashTicket được giữ đầy đủ**

Nguồn trực tiếp là [B11-C](/D:/Project/flash-ticket-platform/docs/architecture/B11-C-target-architecture.md), [B12](/D:/Project/flash-ticket-platform/docs/architecture/B12-data-ownership-and-schema.md), [B13](/D:/Project/flash-ticket-platform/docs/architecture/B13-api-and-event-contracts.md), [B14](/D:/Project/flash-ticket-platform/docs/architecture/B14-main-flow-sequences.md) và [B16](/D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md).

| Phần phải khảo sát | Biểu diễn ở mức thực thể | Chi tiết thao tác và bằng chứng cần giữ |
|---|---|---|
| HTTP/RPC | Bên gọi → bên nhận; gateway, service, hệ ngoài theo nguồn | Endpoint/method, owner, điều kiện gọi; freeze, probe issuance, financial summary và các endpoint liên quan |
| Database/cache | Service → tài nguyên dữ liệu đúng owner và phạm vi | Thao tác đọc/ghi được nguồn chỉ rõ; database logic, instance dùng chung, địa chỉ metric và vị trí triển khai phân biệt |
| Producer/broker/consumer | Service phát → broker → service nhận | Vai trò phát/nhận, message type, exchange/routing key, consumer và queue; trường chưa có tên cụ thể giữ OPEN |
| Outbox/inbox | Quan hệ với datastore và broker của đúng service | Ghi transaction, relay, publisher confirm, consumer commit rồi ACK; không coi có bảng là đã có worker chạy đúng |
| Retry/redelivery/xử lý lặp | Giữ quan hệ gốc; không tạo service hoặc nút mới cho mỗi lần thử | Phân biệt logical message, publish attempt, delivery và processing; giữ điều kiện deduplication |
| Callback đối tác | Quan hệ vào Payment và quan hệ Payment gọi đối tác theo thiết kế | Xác minh callback, query/refund; trace callback mới không bị ghép giả vào trace trước |
| Scheduler/công việc nền | Thuộc service chủ quản; có thể không có bên gọi vào | Expiry/release, relay, refund/query, delivery, phục hồi role-grant/projection; khảo sát từ nguồn, không đợi trace |
| Saga/bù trừ | Các quan hệ HTTP/message/data thực sự được thiết kế | Các bước điều phối của Payment, phản hồi Booking/Ticket, terminal fence, hoàn và hội tụ; không tự đảo cạnh khi bù trừ |
| Thao tác nghiệp vụ/quan sát | Địa chỉ thực thể và nơi gắn tín hiệu | Toàn bộ nhóm thao tác B16 §5; ghi rõ thao tác nào có định danh thiết kế, tên span nào còn chờ instrumentation |
| Hạ tầng và thành phần hỗ trợ | Gateway, identity, config/discovery, host, kho quan sát, RCA và đối tác được nguồn xác định | Tách vai trò nghiệp vụ, vận hành và quan sát; inventory không tự trở thành tập ứng viên xếp hạng |

Hai điểm cần xử lý ngay trong thiết kế P5b:

- **Database logic khác instance vật lý.** B12 §2 xác định các database riêng nhưng dùng chung PostgreSQL instance. Phương án biểu diễn phải giữ cả ownership và tài nguyên dùng chung. Không gộp mất database; không tạo ảo nhiều instance độc lập. Mapping tài nguyên dùng chung phải được kiểm trước khi bàn giao cho P6.
- **Producer/consumer là vai trò.** Có thể biểu diễn đầy đủ cạnh ở mức thực thể mà không biến mọi thao tác thành nút. Thao tác có bằng chứng vẫn được ghi trong danh mục và lớp chi tiết; tên thao tác thiết kế không tự được coi là `operationName` của trace tương lai.

Nếu hợp đồng T-035 chưa biểu diễn được một nhu cầu đã biết, P5b phải chỉ ra phản ví dụ, thông tin mất và đề xuất bổ sung tối thiểu. Không bỏ nhu cầu đó hoặc âm thầm sửa T-035.

**3. Phần làm được ngay và phần còn chờ**

| Làm được từ nguồn hiện có | Chưa thể xác nhận | Đầu vào cần và nơi nhận |
|---|---|---|
| Danh mục thực thể, owner/datastore và bố trí thiết kế FlashTicket | Process, endpoint và placement đang chạy thật | Build/revision, cấu hình triển khai và inventory runtime; nhóm hệ thống/P9 |
| Đồ thị quan hệ và danh mục thao tác từ B12/B13/B14/B16 | Những nhánh đã thực thi trong một request hoặc lượt chạy | Telemetry cùng workload và thời gian quan sát; P9b |
| Exchange/routing theo B13; consumer đích và yêu cầu queue riêng | Tên queue/vhost/binding thực, retry/dead-letter routing | Cấu hình broker và export tương ứng; nhóm hệ thống/P9a |
| Quy tắc nối message, callback, scheduler; ví dụ tổng hợp | Nghĩa link, namespace message ID, độ đầy đủ span thật | Phiên bản instrumentation, mẫu export và phép thử các biên; P9a/P9b |
| Địa chỉ dự kiến của log/trace/metric | Tỷ lệ nối được, sampling/drop, clock offset | Dữ liệu export và manifest lượt chạy; P9b |
| Đối chiếu TT/OB với đồ thị dev đã lưu | Revision hệ thống sinh dataset nếu nguồn chưa chứng minh | Manifest triển khai, image digest, cấu hình hoặc mã thu của tác giả |
| Kiểm bộ dựng và bộ so sánh | Lợi ích cho RCA | Thiết kế P6 và đánh giá tương ứng |

Với FlashTicket, **chưa có code ứng dụng mới theo xác nhận của Minh**. P5b dựng từ thiết kế; code cũ không là bằng chứng triển khai bản mới.

Với TT/OB:

- Train Ticket: bắt đầu từ nguồn RCAEval đã lưu và [repo Train Ticket chính thức](https://github.com/FudanSELab/train-ticket), lần theo release, manifest triển khai, image và instrumentation.
- Nezha-OB: xét [Augmented-OnlineBoutique của nhóm Nezha](https://github.com/IntelligentDDS/Augmented-OnlineBoutique), nguồn Nezha và phần cấu hình/code liên quan. Repo này công bố bổ sung instrumentation, nhưng điều đó chưa chứng minh commit cụ thể đã sinh dataset đang dùng.
- Revision dataset, revision code RCA và revision ứng dụng sinh dữ liệu là ba thứ khác nhau.
- Nếu chưa nối được revision: vẫn dựng đồ thị có nguồn của revision đã xác định, nhưng chỉ báo **đối chiếu tham khảo có điều kiện**. Không gọi chênh lệch là thiếu instrumentation của dataset.

Mỗi quan hệ giữ riêng bốn thông tin: **khả năng biểu diễn; bằng chứng thiết kế/code; quan sát runtime; bằng chứng lợi ích RCA**. Không dùng một nhãn chung để nâng cả bốn.

**4. Cách đối chiếu với T-035**

Đầu vào là [đặc tả v2.1](/D:/RCA-flashticket/results/T-035/dac-ta-do-thi.md), graph/JSON theo manifest và [bảng thông tin theo quan hệ](/D:/RCA-flashticket/results/T-035/thong-tin-theo-quan-he.md). Việc dùng các đầu vào này không đồng nghĩa T-035 đã nghiệm thu.

Quy tắc đề xuất:

1. **Giữ nguyên graph trace.** Đồ thị tĩnh và kết quả đối chiếu là đầu ra riêng; không thêm cạnh tĩnh vào T-035 để làm tăng độ phủ.
2. **Ánh xạ có bằng chứng.** Giữ tên gốc, định danh chuẩn, phạm vi và nguồn alias. Không gộp bằng hậu tố tên hoặc chọn mapping làm kết quả khớp hơn. Mapping mơ hồ giữ riêng.
3. **Tách miền so sánh.** Theo hệ, revision, loại quan hệ, mức đồ thị và từng ca/cửa sổ hiện có. “Toàn miền” Nezha vẫn là miền dev adapter đã cho phép; không mở rộng thành toàn ngày.
4. **So hai chiều.** Báo tập giao, chỉ có trong tĩnh, chỉ có trong trace; đồng thời báo phần chưa ánh xạ, chưa rõ kiểu và chưa đủ điều kiện so.
5. **Công bố mẫu số.** Với tập cạnh tĩnh đủ điều kiện \(S\) và cạnh trace đã ánh xạ đủ điều kiện \(T\), báo \(|S∩T|/|S|\) và \(|S∩T|/|T|\), kèm danh sách phần tử. Mẫu số rỗng là không áp dụng. Đây là tỷ lệ khớp cấu trúc, không phải precision/recall so với một ground truth hoàn chỉnh.
6. **So cấu trúc và so kiểu riêng.** Cạnh trace “gọi chưa phân kiểu” có thể khớp cặp đầu mút nhưng chưa xác nhận kiểu đồng bộ. Không dùng kiểu từ nguồn tĩnh để sửa nghĩa quan sát.
7. **Giữ địa chỉ messaging.** Không gộp mất queue; không ép exchange bằng queue; thiếu địa chỉ không được tự tính là khớp. Nguồn bằng chứng được giữ riêng dù phép đối chiếu cần so quan hệ từ hai loại nguồn.
8. **Mức thao tác chỉ so khi mapping xác minh được.** Giữ các thao tác thiết kế chưa có trace và thao tác trace chưa tìm thấy nguồn; không tạo thao tác giả để đạt phép chiếu.

Đối với mỗi nhóm chênh lệch quan trọng, kiểm các giải thích: khác revision, alias, miền/cửa sổ, nhánh chưa chạy, nguồn tĩnh thiếu, telemetry thiếu hoặc lỗi chuyển đổi. Đọc cả trường hợp khớp có điều kiện tương ứng. Không cộng các cờ chồng lấn thành tỷ lệ nguyên nhân.

Metadata quan hệ mức ngày của Nezha tiếp tục chỉ dùng trong phạm vi mô tả đã cho phép; chưa được đưa vào đồ thị dùng chọn thiết kế P6.

**5. Tổ chức công việc và khả năng song song**

Đề xuất mã dưới đây **chưa được chốt**. Việc chia này thay cách tổ chức phạm vi P5b đã giao cho T-036, nên cần Minh duyệt trước khi ghi vào repo.

| Task dự kiến | Đầu vào/phụ thuộc | Đầu ra chính | Song song và cách giữ nhất quán |
|---|---|---|---|
| **T-036 — Hợp đồng nguồn tĩnh và đối chiếu** | T-035 hiện hành; yêu cầu của cả ba hệ; B12–B16 | Quy tắc định danh/bằng chứng/mẫu số; danh mục nguồn; bộ dựng từ bản ghi quan hệ có nguồn và bộ đối chiếu; ví dụ kiểm | Làm trước. Phải dùng ví dụ HTTP, data, messaging và tài nguyên chung để tránh hợp đồng chỉ vừa TT/OB |
| **T-037 — FlashTicket theo thiết kế** | Hợp đồng T-036 đủ dùng; nguồn FlashTicket ghim phiên bản | Inventory, graph, thao tác, bảng bao phủ toàn bộ nhóm ở mục 2; hợp đồng kiểm với runtime | Có thể đọc nguồn cùng T-038/T-039; không tự đổi hợp đồng chung |
| **T-038 — Train Ticket** | Hợp đồng chung; nguồn/revision ứng viên; graph RE2-TT dev | Truy nguồn phiên bản, graph tĩnh, mapping, đối chiếu và phân tích chênh lệch | Độc lập với nội dung nghiệp vụ FT/OB; mọi alias/kiểu phải có nguồn riêng |
| **T-039 — Online Boutique** | Hợp đồng chung; Nezha/Augmented-OB; graph Nezha dev | Như T-038, thêm phân biệt nguồn phụ dataset và tính độc lập | Có thể cùng T-037/T-038; không lấy quy ước TT áp sang OB |
| **T-040 — Tổng hợp P5b và bàn giao** | Đầu ra đã kiểm của bốn task trên | Soát nhất quán ba hệ; báo cáo P5b; đầu vào P6/P9; danh sách bằng chứng còn thiếu | Làm sau. Kiểm lại cùng phiên bản hợp đồng, miền ID, phép chiếu và mẫu số |

T-036 chỉ làm công cụ chuyển **bản ghi quan hệ đã được đọc và dẫn nguồn** thành graph, không xây công cụ phân tích tĩnh tổng quát cho mọi ngôn ngữ.

**Song song có điều kiện:** ba nhánh hệ thống có thể đọc và lập bản ghi nguồn độc lập sau hợp đồng chung. Nếu một nhánh phát hiện nhu cầu đổi nghĩa cạnh hoặc định danh, dừng phần phụ thuộc để xử lý chung; không để mỗi nhánh dùng một nghĩa riêng. Ghi quyết định, sửa mã chung và tổng hợp làm tuần tự.

Phương án mặc định vẫn có thể thực hiện tuần tự bởi Codex. Chưa đề nghị tự mở chat hoặc sử dụng subagent.

**Ước lượng công sức — CANDIDATE, chưa đo:**

| Phần | Giờ công dự kiến |
|---|---:|
| Hợp đồng chung, mã chuyển đổi/đối chiếu và ví dụ kiểm | 2–4 |
| FlashTicket đầy đủ theo thiết kế | 4–6 |
| Train Ticket và truy nguồn phiên bản | 4–6 |
| Online Boutique và nguồn Nezha | 3–5 |
| Tổng hợp, tự kiểm và bàn giao | 2–3 |
| **Toàn gói** | **15–24** |

Ước lượng tăng so với lượt trước vì đã tính riêng việc đọc nguồn cho từng quan hệ, khảo sát thao tác, kiểm tài nguyên chung và phân xử chênh lệch. Chưa gồm phản biện hoặc chờ tác giả cung cấp bằng chứng.

Phần máy dự kiến nhẹ hơn đọc lại trace thô vì dùng graph T-035 đã lưu. Chưa đo nên chưa cam kết thời gian chạy. Không cần EC2/GPU trong phương án này. Dung lượng tải nguồn TT/OB còn OPEN; lập danh sách tệp và tổng byte theo revision trước khi xin tải, không duyệt tải trọn repo bằng một ước lượng tùy ý.

**6. Kiểm đúng đắn và tiêu chí xong**

Các phép kiểm phải bao gồm:

- Mỗi nút/cạnh truy được về nguồn và điều kiện áp dụng; không biến quan hệ thiết kế thành sự kiện đã chạy.
- Đáp án viết độc lập cho các trường hợp: alias mơ hồ, cạnh khác kiểu, nhiều queue cùng consumer, fan-out, retry, callback trace mới, scheduler không có caller, database dùng chung instance và cửa sổ rỗng.
- Giữ được phân biệt nguồn tĩnh/trace; không bịa `event_count` từ số dòng tài liệu.
- Phép chiếu thao tác giữ đúng phần có thể chiếu, không yêu cầu thao tác chưa có bằng chứng để làm graph thực thể đầy đủ.
- Mọi phần tử ngoài miền so sánh được báo cùng lý do; tổng các tập đối chiếu khớp danh sách thực.
- Bộ dựng/so sánh không dùng root, loại lỗi hoặc tên ca để chọn quan hệ. Nhãn chỉ phục vụ báo cáo riêng sau khi graph được tạo.
- Chạy lại cho kết quả xác định; giữ mọi lượt, kể cả lượt lỗi.

**P5b đạt khi:**

1. Cả ba hệ có danh mục nguồn, revision và trạng thái liên hệ với hệ mục tiêu/dataset.
2. FlashTicket có bảng đối chiếu tới từng quan hệ, thao tác và điểm quan sát thuộc các nhóm đã nêu; không dừng ở một vài ví dụ.
3. Mọi nhu cầu có nguồn được biểu diễn, hoặc có mô tả chính xác thông tin chưa biểu diễn được và cách xử lý cần trình Minh.
4. TT/OB có đối chiếu hai chiều trên các graph dev trong phạm vi; chưa xác minh revision thì giới hạn kết luận được thể hiện ngay trong kết quả.
5. Các nhóm chênh lệch quan trọng đã được lần theo bằng nguồn có thể đọc trong quyền được duyệt. Còn OPEN phải nêu đúng bằng chứng thiếu, người cung cấp và quyết định phụ thuộc.
6. P6/P9 nhận được đầu vào cụ thể, không chỉ một hình đồ thị hoặc danh sách “cần thêm trace”.
7. Kiểm nguồn, phép dựng, phép đối chiếu và tổng hợp đạt; lỗi chưa xử lý ảnh hưởng kết luận được giữ rõ.

Đạt các tiêu chí này cho phép nhận **mô hình tĩnh và mô tả độ khớp có điều kiện**. Nó chưa xác nhận runtime FlashTicket, cơ chế RCA hoặc quyền mở test.

**7. Đầu ra cho P6/P9 và thử nghiệm FlashTicket**

- **P6:** graph theo nguồn, inventory tách khỏi nút quan sát, địa chỉ tín hiệu, kiểu/chiều cạnh, thông tin mất khi gộp và các mapping còn OPEN. Mỗi thông tin nêu phép tính nào *có thể* nhận nó; không tự chọn mức operation, tín hiệu hoặc cơ chế.
- **P9a:** mỗi thiếu hụt ghi quan hệ cần hỗ trợ, trường/khóa cần có, nơi phải ghi — application instrumentation, broker/configuration, collector hay giao thức thực nghiệm — và phép kiểm. Collector không được coi là nơi tái tạo thông tin chưa từng ghi.
- **P9b:** hợp đồng chuẩn hóa và bộ ví dụ đầu vào/đầu ra; yêu cầu manifest build/deployment, namespace, sampling/drop và clock.
- **SPEC đối chiếu FlashTicket khi có runtime:** kiểm đường thành công, lỗi phát hành/bù trừ, publish lại, consumer lặp, callback/query, expiry, delivery lỗi và các đường phục hồi đã có trong thiết kế. Đây là phép kiểm quan sát các hành vi đã duyệt, không thêm nghiệp vụ.
- **P10:** dữ liệu đủ chứng minh workload/nhánh đã chạy, nhãn lỗi và giao thức đánh giá riêng. Các số khớp cấu trúc không thay kết quả thử nghiệm RCA.

**8. File dự kiến và nội dung cần ghi chính thức**

| Đường dẫn dự kiến | Nội dung/ảnh hưởng |
|---|---|
| `D:/RCA-flashticket/docs/DECISIONS.md` | Ghi nguyên ý lựa chọn của Minh; việc chia task chỉ ghi là đã quyết sau khi được duyệt |
| `D:/RCA-flashticket/docs/WHY.md` | Lý do độ sâu khảo sát; phân biệt thiết kế/runtime; quy tắc đối chiếu, tài nguyên chung và cách chia việc |
| `D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/{SPEC,LOG}.md` | Phạm vi task chung, câu hỏi, đầu ra, kiểm, quyền ghi |
| `D:/RCA-flashticket/tasks/T-037-p5b-flashticket/{SPEC,LOG}.md` | Toàn bộ phần FlashTicket trong phương án |
| `D:/RCA-flashticket/tasks/T-038-p5b-trainticket/{SPEC,LOG}.md` | Nguồn TT và đối chiếu RE2-TT |
| `D:/RCA-flashticket/tasks/T-039-p5b-online-boutique/{SPEC,LOG}.md` | Nguồn OB và đối chiếu Nezha |
| `D:/RCA-flashticket/tasks/T-040-p5b-tong-hop/{SPEC,LOG}.md` | Tổng hợp và bàn giao P6/P9 |
| `D:/RCA-flashticket/results/T-036/` | `hop-dong.md`, `nguon.json`, fixture, kiểm và manifest |
| `D:/RCA-flashticket/results/T-037/` | Inventory, quan hệ/thao tác có nguồn, graph FlashTicket, bao phủ yêu cầu và hợp đồng đối chiếu runtime |
| `D:/RCA-flashticket/results/T-038/`, `results/T-039/` | Nguồn, mapping, graph, JSON đối chiếu, báo cáo chênh lệch, kiểm và manifest từng hệ |
| `D:/RCA-flashticket/results/T-040/` | Báo cáo P5b, bàn giao P6/P9, kiểm tổng hợp và manifest |
| `D:/RCA-flashticket/src/do_thi_tinh/{__init__.py,build.py,compare.py,README.md}` | Bộ dựng/đối chiếu dùng chung; không sửa bộ dựng trace T-035 |
| `D:/RCA-flashticket/docs/STATE.md` | Thêm các dòng task theo cách chia được duyệt và cập nhật phần kế tiếp liên quan |

Các thư mục kết quả chứa `runs/` để giữ lịch sử; SPEC từng task phải liệt kê phạm vi của chính nó. Nguồn tải mới và việc cập nhật `data/README.md` sẽ nằm trong đề xuất tải có danh sách/dung lượng cụ thể.

**Nội dung quyết định đề nghị ghi, chưa ghi:**

> Minh chọn “thực thể đầy đủ; thao tác khi có bằng chứng”. P5b chủ động khảo sát thao tác và đường giao tiếp từ nguồn kiến trúc, hợp đồng, cấu hình, code hoặc trace có bằng chứng; không yêu cầu dựng toàn bộ đồ thị mọi hàm. Phạm vi FlashTicket bao gồm các quan hệ đồng bộ, bất đồng bộ, dữ liệu, công việc nền, callback, Saga/bù trừ và điểm quan sát đã được nguồn quy định. FlashTicket mới chưa có code ứng dụng; phần dựng từ thiết kế phải ghi đúng trạng thái. Lựa chọn này chưa quyết định cách chia task hoặc cho phép ngoại lệ quy tắc một phiên.

Cách chia năm task và các quy tắc kỹ thuật mới ở trên vẫn là **CANDIDATE**. Không có quyền ghi P5b từ các lần duyệt sửa T-035. Tôi cũng không đề xuất sửa kiến trúc/nghiệp vụ FlashTicket, MRP hoặc nguồn T-035 trong gói này.

**Tự rà:** phương án đã giữ đủ các nhóm Minh yêu cầu, tách việc làm ngay khỏi bằng chứng runtime, giữ nghĩa vụ TT/OB và không chọn trước P6. Điểm chưa chốt là cách chia task, phạm vi ghi tương ứng và các lựa chọn kỹ thuật cần được soát trong SPEC. Bằng chứng nối revision TT/OB với deployment sinh dataset vẫn OPEN.


## Bổ sung kiểm cuối Phiên 1 — 15/10/2026

Đã kiểm đủ các mục của template SPEC; Prompt chung giữ nguyên ngoài chỗ điền metadata, khối Soát SPEC và G3 khớp nguyên văn. Điều kiện dừng trước triển khai/sửa SPEC có trong cả SPEC và prompt. Đường dẫn nguồn/manifest liên quan tồn tại; không chạy lại hash toàn bộ kết quả T-035 trong lượt ghi tài liệu này. Đã xem diff đầy đủ phần thêm DECISIONS/WHY và sửa STATE của lượt, cùng toàn nội dung hai file mới; giữ thay đổi cũ. Dòng T-036 nằm trong bảng task. Chỉ năm file đã nêu thay đổi; chưa có results/T-036 hoặc src/do_thi_tinh. Kiểm tài liệu đạt, chưa thay lượt tự soát nguồn ở phiên sạch. Lệnh cuối: Python kiểm mục template, khối prompt, đường dẫn, phạm vi và nối kết quả này; bước tiếp vẫn là prompt Codex mới ở trên. Đề xuất nội dung commit sau khi Minh yêu cầu/duyệt: docs: ghi SPEC T-036 và bàn giao tự soát trước triển khai. Chưa commit/push.

## Phiên 2 — 15/10/2026 — Codex — LEVANMINH — vai trò: người làm

**Mở phiên / quyền:** EXECUTE theo yêu cầu hiện tại của Minh và SPEC đã duyệt. Tự soát từ nguồn trước triển khai; Codex giữ người làm, Claude phản biện chính thức. Không có REVIEW T-036 để đối chiếu; không lấy lời duyệt làm bằng chứng đúng khoa học.

**Nhận xét độc lập trước triển khai:**
- DT18-NV2/cô bước 1 và MRP P5 đòi gọi, message, dữ liệu, định danh tín hiệu và đối chiếu nguồn. SPEC bao phủ hợp đồng/công cụ; khảo sát đủ ba hệ thuộc T-037–040, lợi ích RCA thuộc P6/P7/P10. Không dùng fixture để trả lời thay các phần đó.
- B12 §2: database logic và PostgreSQL instance chung phải giữ hai định danh cùng mapping tài nguyên, không thêm cạnh gọi giữa các database. T-035 chưa có schema riêng cho mapping này; SPEC cho phép hợp đồng nguồn tĩnh riêng. Giữ mapping có nguồn bên cạnh graph, không âm thầm sửa graph trace hoặc coi mapping là cạnh đã quan sát. Đây là thông tin T-037/P6/P9 phải nhận.
- B13 §5.1–5.2/B16 §3–5: producer/consumer là vai trò; exchange/routing khác queue và namespace message ID. T-035 v2.1 giữ địa chỉ; comparator phải giữ địa chỉ khi bỏ provenance khỏi khóa so cấu trúc. Không nối bản tin từ correlation hoặc topology.
- Đọc code builder/project T-035: phép chiếu bỏ span-parent và cạnh cùng owner; component_context giữ endpoint không có operation. T-036 phải báo phần thao tác không thể chiếu, không tạo operation giả hoặc đồng nhất tên thiết kế với runtime.
- Alias/miền/revision có thể tạo chênh lệch giống thiếu telemetry. So cấu trúc và so kiểu phải riêng; unknown/thiếu địa chỉ giữ loại trừ có lý do. Không chọn alias tăng khớp. WHY-52/53 đã có căn cứ, phương án khác và giới hạn cho các lựa chọn này.
- Phụ thuộc: T-035 chưa nghiệm thu nhưng SPEC cho phép dùng bản ghim sau kiểm hash. Các graph dev và code/hợp đồng trực tiếp đã kiểm khớp manifest; nguồn TT/Nezha đã lưu được chọn cũng khớp. Không dùng thẻ cũ hoặc mở trace thô/test.
- Quyền/chi phí/tiêu chí: đường ghi cụ thể đủ để cài và kiểm; không cần tải/EC2/subagent/lượt >1 giờ. Oracle literal phải có trước code. Registry khởi đầu không được tự thành inventory đầy đủ hay xác minh revision dataset–ứng dụng.

**Kết luận tự soát:** chưa phát hiện lỗi đáng kể cần sửa SPEC hoặc chặn triển khai. Tiếp tục trong phạm vi đã duyệt. Khả năng biểu diễn và so sánh còn phải được fixture phân xử; tự soát không thay phản biện Claude hoặc nghiệm thu.

**Bản đồ tác động theo SPEC:** nguồn hợp đồng results/T-036/hop-dong.md trước; fixtures có oracle trước bốn file src/do_thi_tinh; chạy kiểm và báo cáo/manifest/bàn giao sau; chỉ nối LOG này và thay dòng T-036 trong STATE. Không thay SPEC/WHY/DECISIONS/T-035/platform. Giữ toàn bộ thay đổi có sẵn.

**Quyết định Minh trong phiên:** triển khai T-036 sau tự soát không có vấn đề; không có lựa chọn khoa học mới. Quyền này đã được ghi ở Q-157 và SPEC, không xin ghi thêm quyết định trùng.

**Tiến độ bước nguồn/hợp đồng/oracle:** registry 14 nguồn, kiểm 5.673 artifact được chọn từ manifest; kết quả và hash tại runs/chuan-bi-001/input-verification.json và preflight.json. Đọc B11-C/B12/B13/B14/B16 hiện hành, không dùng code cũ. Ghi hợp đồng và oracle literal trước implementation; biên nhận fixtures/oracle-before-code.json xác nhận chưa có build.py/compare.py. Nguồn công khai chỉ là điểm bắt đầu truy revision, chưa là deployment sinh dataset.

**Tiến độ cài/kiểm:** viết bốn file src/do_thi_tinh và checker trong phạm vi. runs/kiem-001 dừng ở bước chọn graph lịch sử vì selector rộng; mọi kiểm fixture đã chạy trước đó đạt, failure.json giữ exception. Sửa selector chỉ chọn results/T-035/do-thi/ hiện hành, không sửa graph/manifest đầu vào. runs/kiem-002 đạt các kiểm literal và tương thích. Tự đọc lại code phát hiện cần báo nút cô lập và loại cạnh nội bộ sau alias; bổ sung trong implementation, giữ SPEC. Bổ sung kiểm biên tương ứng trước lượt cuối, không thay oracle gốc để đạt.

**Hoàn tất implementation / tự soát:** bổ sung bảng mapping nút cô lập, loại cạnh nội bộ sau alias, phân biệt default exchange rỗng với thiếu, bảo toàn provenance/record membership và giữ source evidence khác runtime/RCA. Registry cập nhật revision cụ thể khi nguồn lưu chứng minh được; giữ 15 nguồn hiện hành, không nâng tree/code/dataset revision thành application deployment. Nguồn registry ban đầu giữ ở runs/chuan-bi-001/nguon-ban-dau.json. Kiểm tích hợp messaging dùng span tổng hợp qua T-035, không mở trace thô.

**Kết thúc Phiên 2:**
1. Đã tự soát SPEC độc lập từ nguồn, chưa phát hiện lỗi cần sửa SPEC; đã cài hợp đồng/registry, builder/comparator, oracle, kiểm, báo cáo và bàn giao. Đầu ra công cụ đạt các phản ví dụ đã kiểm; chưa có inventory/đối chiếu kiến trúc đủ ba hệ. T-036 chờ Claude phản biện, Minh nghiệm thu; tự soát không thay phản biện chính thức.
2. File thay đổi đúng quyền: results/T-036/; src/do_thi_tinh/__init__.py, build.py, compare.py, README.md; nối LOG này; chỉ dòng T-036 trong docs/STATE.md. SPEC không sửa. Giữ mọi thay đổi có sẵn. Không sửa T-035/platform/WHY/DECISIONS hoặc file task khác; không mở test, tải repo, bật EC2, dùng subagent, commit/push.
3. Kiểm: manifest đầu vào khớp; oracle literal có trước code; lượt cuối 151 kiểm đạt, 312 graph dev full/N/A đọc tương thích và 156 cặp chiếu khớp. Hai process seed khác cho trung gian giống từng byte; kết quả ở runs/kiem-004, kiem-005 và runs/ket-phien-001/determinism.json. Lượt cuối 8.754s, RAM peak working set 109.9MiB; số gốc trong result.json. Giữ lượt lỗi kiem-001 (selector graph lịch sử), các lượt sau và snapshot mã hai lượt cuối. Kiểm cuối diff/phạm vi/manifest ở runs/ket-phien-001/final-verification.json; không chạy lại baseline hoặc trace thô.
4. Câu nguồn: cung cấp biểu diễn và phép so có điều kiện cho P5, chưa trả lời RQ3/RQ5, toàn P5b hoặc cơ chế RCA. OPEN: deployment/runtime FT; revision ứng dụng sinh TT/OB; nghĩa host/metadata ngày; độ đầy đủ telemetry; lựa chọn/lợi ích P6. Binding DB→instance được giữ ngoài cạnh trace; T-035 chưa có trường tương đương. ban-giao.md nêu phản ví dụ, phương án adapter/mapping cần trình, owner và quyết định phụ thuộc. Không coi thiếu bằng chứng là không thể làm hoặc tự loại nhóm khỏi nghiên cứu.

**Quyết định/bất đồng:** không có phản biện chính thức T-036 trước phiên này, không có bất đồng với Claude được kết luận thay. Không thêm quyết định khoa học. Quyền triển khai đã được Q-157/SPEC ghi, không tự sửa sổ. Minh quyết nghiệm thu hoặc bước sửa sau phản biện. Nội dung nên vào báo cáo: phân biệt nguồn/quan sát, logical DB/instance, địa chỉ messaging/metric shared và mẫu số có điều kiện, cùng giới hạn fixture/runtime.

**Bước tiếp chính xác:** Minh mở phiên Claude mới tại D:/RCA-flashticket, copy results/T-036/prompt-claude.txt (cũng dưới đây). Claude đọc nguồn/đầu ra/code trước các kết luận, kiểm độc lập theo mẫu. Phạm vi mặc định của prompt chỉ đọc/trả lời chat; ghi REVIEW cần Minh cấp đúng file lượt. Không tự gửi hoặc tự mở phiên. T-037–040 cần SPEC riêng sau hợp đồng được xem xét; không triển khai từ quyền T-036.

**Lệnh cuối của phiên:** py -3 -X utf8 -B results/T-036/finalize.py (tổng hợp và kiểm diff/phạm vi/manifest); lệnh kiểm hành vi cuối: & 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B results/T-036/check.py kiem-005. Không chạy lại tên run cũ. Nếu phát hiện lỗi lúc tổng hợp, giữ kết quả lỗi và trình đúng phạm vi; không sửa SPEC.

**Đề xuất nội dung commit, chưa thực hiện:** feat: add sourced static graph contract and trace comparison for T-036. Minh yêu cầu không commit/push trong phiên này; không thực hiện.

### Prompt Claude — soát kết quả (Minh chuyển thủ công)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-036; D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện chính thức.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; tasks/T-036-p5b-hop-dong-chung/SPEC.md và LOG.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; nguồn và manifest tại results/T-036/nguon.json.
- Phản biện và phản hồi trước: không có bản phản biện chính thức T-036 trước lượt này.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-036/manifest.json; hop-dong.md; nguon.json; fixtures/; runs/; kiem-dung-dan.md; ban-giao.md; src/do_thi_tinh/README.md và code; results/T-035/manifest.json và các đầu vào SPEC liệt kê; Windows/PowerShell, Python theo README; diff phiên ở results/T-036/runs/ket-phien-001/changes.diff.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC, code hoặc kết quả.

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


## Phiên 3 — 15/10/2026 — Codex — LEVANMINH — sửa R1 theo Minh giao

**Mở phiên / quyền:** Minh duyệt: “Duyệt sửa R1 theo đề xuất trong phiên này. Sau khi sửa và kiểm lại, soạn prompt cho phiên Codex sạch phản biện chính thức toàn bộ T-036 như lần đầu, không neo theo kết luận cũ.” Vai trò lượt này là thực hiện sửa theo chỉ định hiện tại; lượt phản biện trước ở chat, chưa có REVIEW. Tự kiểm sửa không là phản biện chính thức mới. Phiên Codex sạch tiếp theo phản biện chính thức toàn bộ task theo ngoại lệ Minh đã chỉ định; không sửa SPEC/phân công lịch sử.

**Phạm vi và thứ tự:** giữ bản trước tại results/T-036/runs/sua-r1-001/before/; ghi oracle R1 và tái lập trước sửa; sửa khóa compare theo vai trò và mô tả hợp đồng; hồi quy checker, báo cáo/bàn giao/manifest, prompt mới và đúng dòng T-036 của STATE. Không sửa SPEC/WHY/DECISIONS/T-035/platform, không mở test, tải nguồn, dùng subagent hoặc commit/push. Hash 95 artifact, 15 nguồn và ba manifest phụ thuộc khớp trước sử dụng; preflight.json ghi chi tiết.

**Oracle và tái lập trước sửa:** fixtures/r1.json và receipt runs/sua-r1-001/oracle-before-fix*.json được ghi khi comparator còn khớp bản before/. Lượt kiem-r1-before-001 giữ exception mapping_target do harness đưa operation mapping vào mức entity; đã sửa harness theo mức, không sửa comparator hoặc oracle. Lượt kiem-r1-before-002 chạy đủ, bộ kiểm cũ đạt; 22 kiểm R1 không đạt ở giao/mẫu số/member của trường hợp khác độ chi tiết. Giữ mọi lượt. Sau đó sửa comparator chỉ chọn trường địa chỉ theo vai trò; graph nguồn/members nguyên bản giữ đầy đủ. Đồng bộ hợp đồng và literal khóa mong đợi trong checker; không đổi oracle ban đầu.


**Kết thúc Phiên 3 / kiểm sửa theo Minh duyệt:**
1. Đã sửa khóa đối chiếu theo vai trò, giữ địa chỉ đầy đủ trong nguồn/members; đồng bộ hợp đồng và tự kiểm hồi quy. R1 đạt trong các trường hợp đã kiểm; chưa là phản biện chính thức mới, chưa nghiệm thu toàn task. Không thêm quyết định khoa học.
2. File hiện hành sửa: src/do_thi_tinh/compare.py; results/T-036/check.py, hop-dong.md, kiem-dung-dan.md, ban-giao.md, manifest.json. Thêm fixtures/r1.json, các run mới, thư mục sửa có bản trước/oracle/diff/audit, prompt-codex-clean.txt; LOG chỉ nối và STATE chỉ dòng T-036. Không sửa SPEC/WHY/DECISIONS/T-035/platform hoặc oracle ban đầu. Giữ mọi lượt và thay đổi có sẵn.
3. Kiểm: hai lượt sau sửa đều 221/221 đạt, 0 lỗi; 312 graph và 156 cặp chiếu. 10 trung gian xác định giữa hai process; 7 đầu ra không chịu tác động khớp trước sửa. Trước sửa giữ một exception harness và lượt tái lập 22 kiểm R1 không đạt. Số/hash ở result.json, r1-regression.json, determinism-and-preservation.json và final-verification.json. Không chạy baseline hoặc trace thô/test.
4. Task có hợp đồng/công cụ và bằng chứng tự kiểm hiện hành; câu nguồn P5/RQ3/RQ5 chưa hoàn tất. Inventory/đối chiếu đầy đủ ba hệ, revision ứng dụng, runtime FT và lợi ích RCA vẫn cần các task đã bàn giao. Khớp consume không xác nhận routing/binding runtime. Minh quyết nghiệm thu sau phản biện toàn task; quyền sửa đã lưu nguyên văn authorization.txt. Không suy đồng thuận thành quyền G3/test.

**Bước tiếp chính xác:** Minh mở phiên Codex mới tại D:/RCA-flashticket và dán results/T-036/prompt-codex-clean.txt. Phiên đó là người phản biện chính thức độc lập theo chỉ định Minh, đọc toàn nguồn/code/đầu ra như lần đầu trước nhận xét lịch sử; chỉ trả lời chat, chưa có quyền ghi REVIEW. Không tự tạo/gửi phiên. Nội dung báo cáo cần giữ: phân biệt khóa lưu thông tin với khóa đo chặng theo vai trò và giới hạn của khớp consume.

**Lệnh kiểm hành vi cuối:** PYTHONHASHSEED=1 với D:/RCA-ext/envs/py312-pin/Scripts/python.exe -X utf8 -B results/T-036/check.py kiem-r1-after-002; đã chạy qua subprocess đặt biến cho process con. **Lệnh cuối của bước bàn giao:** py -3 -X utf8 -B results/T-036/runs/sua-r1-001/finalize-r1.py. Script có guard không ghi đè audit đã có; đọc audit và manifest trước tiếp tục, không chạy lại run cũ.

**Đề xuất commit, chưa thực hiện:** fix: compare messaging addresses by role in T-036. Chỉ commit/push khi Minh yêu cầu hoặc duyệt.

### Prompt Codex sạch — phản biện chính thức toàn bộ T-036 (Minh chuyển thủ công)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: toàn bộ T-036; D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/SPEC.md.
- Công đoạn: soát kết quả toàn bộ task trong một phiên Codex sạch.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: người làm là Codex ở các phiên triển khai và sửa T-036; người phản biện chính thức là Codex trong một phiên mới độc lập, thay Claude theo chỉ định trực tiếp của Minh. Minh đã cho phép ngoại lệ hai phiên Codex giữ hai vai trò này. SPEC/LOG/STATE còn giữ phân công lịch sử; chưa có quyền sửa SPEC hoặc các sổ phân công. Phiên nhận prompt này là người phản biện chính thức.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; D:/RCA-flashticket/docs/STATE.md; D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/SPEC.md và LOG.md; D:/RCA-flashticket/docs/MRP.md; D:/RCA-flashticket/docs/WHY.md; D:/RCA-flashticket/docs/DECISIONS.md; D:/RCA-flashticket/docs/LESSONS.md; D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md; D:/RCA-flashticket/results/T-036/nguon.json và các nguồn được registry liệt kê.
- Phản biện và phản hồi trước: lịch sử các phiên và các lượt của task tại D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/LOG.md và D:/RCA-flashticket/results/T-036/runs/; chưa có file REVIEW chính thức. Nhận xét và phản hồi lịch sử được đọc sau khi đã lập nhận xét độc lập từ nguồn và đầu ra gốc.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-036/manifest.json; hop-dong.md; nguon.json; fixtures/; runs/; kiem-dung-dan.md; ban-giao.md; D:/RCA-flashticket/src/do_thi_tinh/README.md và toàn bộ code; D:/RCA-flashticket/results/T-035/manifest.json và các đầu vào SPEC liệt kê. Diff các phiên tại D:/RCA-flashticket/results/T-036/runs/ket-phien-001/changes.diff và D:/RCA-flashticket/results/T-036/runs/sua-r1-001/changes.diff. Windows/PowerShell; môi trường Python và cách chạy theo README.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời bản phản biện chính thức trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC, DECISIONS, code hoặc kết quả. Không thực hiện quyền triển khai của người làm từ SPEC.

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


## Phiên 4 — 15/10/2026 — Codex — LEVANMINH — ghi nhận phản biện chính thức và đóng theo Minh duyệt

**Mở phiên / quyền:** trước đó phiên Codex sạch giữ vai trò người phản biện chính thức theo ngoại lệ Minh chỉ định; phản biện chỉ đọc được trả lời trong chat. Sau đề xuất nghiệm thu và gói ghi nhận đúng bốn file, Minh yêu cầu nguyên văn: “đóng task giúp tôi”. Đây là quyền ghi REVIEW.md, nối docs/DECISIONS.md, nối LOG này và chỉ đổi dòng T-036 trong docs/STATE.md để đóng task. Không chuyển sang vai trò người làm, không sửa SPEC/phân công lịch sử hoặc kết quả.

**Quyết định của Minh trong phiên:** “đóng task giúp tôi” (T-036), ghi nguyên ý ở Q-158. Phần phạm vi nghiệm thu và nghĩa vụ còn mở là mô tả của agent trong REVIEW và bàn giao, không gộp thành các quyết định nghiên cứu mới của Minh.

**Nguồn và kết quả phản biện đã lưu:** REVIEW.md ghi lượt soát toàn bộ task từ nguồn/đầu ra gốc trước lịch sử. Không phát hiện lỗi đáng kể còn chưa xử lý trong hợp đồng/công cụ chung. R1 đúng và đã sửa; bản hiện hành giữ địa chỉ đầy đủ trong members và chỉ so phần cần cho vai trò. Bộ kiểm phát lại trong bộ nhớ đạt 221/221, 312 graph tương thích, 156 cặp phép chiếu khớp; số lưu đối chiếu ở results/T-036/runs/kiem-r1-after-002/result.json#/passed, #/failed, #/compatibility_graph_count, #/trace_projection_pair_count. Chi tiết kiểm độc lập và giới hạn trong REVIEW. Không tạo run mới từ lượt chỉ đọc.

**Tiến độ ghi nhận:** kiểm lại 187 mục manifest T-036 trước sử dụng, đều khớp. Lưu bản phản biện chính thức có prompt theo mẫu và bảng phản hồi trống; ghi Q-158; nối mốc đóng này; dòng T-036 trong STATE chuyển xong. SPEC, manifest và báo cáo triển khai giữ snapshot trước nghiệm thu; hiện trạng theo Q-158/REVIEW/mục LOG này và dòng T-036. Phần mô tả chưa triển khai trong mục Task đang mở của STATE là mốc cũ, không là hiện trạng của T-036; ngoài dòng task không nằm trong quyền sửa lượt này.

**Kết thúc Phiên 4:**
1. Đã lưu phản biện chính thức và ghi nhận Minh nghiệm thu/đóng T-036 ở phạm vi hợp đồng/công cụ. Không còn lỗi đáng kể được phản biện giữ lại trong phạm vi đã kiểm; không dựng thêm lượt đáp hoặc tự chạy vòng phản biện.
2. File thay đổi đúng gói duyệt: thêm tasks/T-036-p5b-hop-dong-chung/REVIEW.md; nối docs/DECISIONS.md và LOG này; chỉ sửa dòng T-036 của docs/STATE.md. Không sửa code/kết quả/SPEC/WHY/task khác. Không commit/push.
3. Kiểm lượt đóng: đối chiếu toàn nội dung/diff bốn file, append-only DECISIONS/LOG, duy nhất dòng STATE, mẫu prompt và hash nguồn/kết quả bảo vệ. Kết quả kiểm sau ghi được báo trong chat; không chạy lại thực nghiệm hoặc tạo artifact ngoài bốn file.
4. T-036 đạt phần công cụ/SPEC, chưa hoàn tất toàn P5b hoặc trả lời RQ3/RQ5/G3. T-037–040 nhận inventory/đối chiếu đầy đủ ba hệ và tổng hợp; T-038/039 truy revision; P9 nhận runtime/telemetry/mapping DB→instance; P6/P7/P10 chọn/đánh giá thiết kế/lợi ích RCA. Đầu vào/owner/quyết định phụ thuộc giữ tại results/T-036/ban-giao.md §2–3. Không tự nghiệm thu T-035, chọn P6 hoặc mở test. Nội dung formal report cần giữ: phân biệt nguồn thiết kế, quan sát runtime và hiệu quả RCA, cùng địa chỉ/tài nguyên/mẫu số có điều kiện.

**Bước tiếp chính xác:** đọc docs/STATE.md dòng T-036, REVIEW.md và results/T-036/ban-giao.md §3 trước khi trình SPEC T-037–040; việc soạn/triển khai task mới cần Minh giao/duyệt riêng. Lệnh đọc: Get-Content -LiteralPath 'results/T-036/ban-giao.md' -Raw. Không tự mở lại T-036 từ prompt được lưu.

**Prompt bàn giao:** nguyên văn Prompt chung + khối Người làm đáp phản biện + khối G3 được lưu tại REVIEW.md trước bảng phản hồi. Prompt thuộc lượt phản biện; Minh chọn gửi hoặc dừng. Mốc đóng hiện tại không yêu cầu tự phát sinh một lượt đáp mới.

**Lệnh cuối của lượt đóng:** Python inline -X utf8 -B kiểm hash/prefix/diff/phạm vi bốn file và mẫu prompt, in kết quả trong chat; không tạo file kiểm riêng. **Đề xuất nội dung commit, chưa thực hiện:** docs: record T-036 review and acceptance. Chỉ commit/push khi Minh yêu cầu hoặc duyệt riêng.
