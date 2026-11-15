# Nhật ký T-065

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ.

---

## Phiên 0 — 13/11/2026 — Claude — laptop Minh — vai trò: người soạn SPEC (phiên điều phối T-062)

- Minh duyệt SPEC ngày 13/11/2026 (chat: "tổng thể đề xuất đã ổn … tạo ghi đầy đủ tài liệu …"; nguyên lời ở `docs/DECISIONS.md` mục chiến dịch M1-FlashTicket). SPEC ghi 12/11 ~19:20Z.
- Chưa làm bước nào của task. Bối cảnh và quyền: `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md`. Trạng thái sống: `tasks/T-062-dem-chang-1-4/CHECKPOINT-CHIEN-DICH.md`.
- Bước tiếp theo chính xác: theo mục "Các bước" của SPEC và danh sách việc trong checkpoint.
- Người làm của task này là Codex; các mục LOG tiếp theo do Codex ghi (hoặc phiên điều phối chép từ báo cáo của Codex, ghi rõ nguồn).

## Phiên 1 — 12/11/2026 22:15Z — Codex — laptop Minh — người làm T-065

- Nhận brief L3 G-a/G-b trên P7, chuẩn bị chiều bản cho T-064. Quyền theo SPEC đã duyệt/bổ sung và brief. Chỉ ghi results/T-065 và nối LOG này; không ghi STATE theo brief hẹp hơn.
- Đọc các nguồn bắt buộc; nguồn mục tiêu DT18/cô, MRP, LESSONS, WHY liên quan và DECISIONS điều phối. Bản 6 dùng làm mốc; không chạy lại 123 link cũ chỉ để xác nhận lỗi đã sửa.
- Đã kiểm ba hash bộ sinh/dashboard bản 6 với manifest T-062: khớp. Chưa sửa máy. SSH exp-obs dùng được; hash compose hiện đã đổi bởi T-063, giữ nguyên.
- Python ghim không khởi chạy được; CUA báo browser access host unavailable. Ghi chi tiết và phần phụ thuộc ở results/T-065/CHECKPOINT.md. Tiếp tục phần JSON/API độc lập bằng JavaScript, không lách sandbox.


## Kết thúc lượt L3 — 2026-11-12T22:51:12.291Z — Codex, người làm

1. Đã làm: dựng định dạng 0.3 có chiều bản P7, dữ liệu/chỉ mục, hai dashboard mới; bảng/đồ thị thao tác và link Tempo/Loki/Prometheus. Không chạy lại M1. G-a/G-b mới có bằng chứng dữ liệu/API, chưa hoàn thành kiểm browser; G-c chưa có đầu vào bản cuối.
2. File: chỉ results/T-065/ (tập đầy đủ ở manifest.json) và nối LOG này. Không ghi docs/STATE, src, task/results khác. Đã tạo 175 file dữ liệu và hai dashboard mới trên exp-obs, chỉ ghi đè file do L3 tạo khi hoàn thiện.
3. Kiểm: 72 mục nguồn còn khớp hash cuối lượt; 9 ca/18 bản ghi qua schema, 1.197 thao tác, 92 kênh op có cờ, 1.183 cặp cạnh. Tất cả số mẫu/trạng thái/cờ/e và trung gian span khớp nguồn. 2.638 URL nguồn giải mã một lần. API bản bàn giao api-panels-6.json: 189 request/1.440 target không lỗi, 18 trang ca và 153 cặp ca/service khớp. Kiểm thêm 9 API mẫu ba kho, 4 link Loki có cờ và 9 link tương quan trace; không gọi là bấm thật. Tám file máy cũ giữ hash, 177 file mới khớp local; dashboard cũ vẫn version 6/6. Restart riêng Grafana hai lần, không có tunnel/browser riêng còn mở.
4. OPEN: browser host không khả dụng, thiếu bấm thật/ảnh/render theo SPEC. Hai panel diễn giải rỗng động thử ba lần chưa đạt (lượt 3/nhanh 4/5); đã dừng cách thử theo §5a và rút phần lỗi, giữ lượt lỗi; bản bàn giao còn hướng dẫn text/mô tả điều kiện. Đề xuất Claude kiểm biểu thức/request đã lưu rồi quyết cách khác (xuất trạng thái truy vấn thành JSON từ lớp API/bộ xuất), chưa triển khai. G-c chờ chỉ mục T-064 và kiểm ứng viên cuối. Không thêm/đổi quyết định nghiên cứu; chưa trả lời xong RQ5 hay nghiệm thu T-065. Chi tiết bằng chứng/giới hạn trong kiem/001/BAO-CAO.md.

- Tự kiểm đã phát hiện và sửa nhầm enum CLIENT thành message; fixture kiểm CLIENT/PRODUCER/CONSUMER đã đạt. Không dùng lượt nhầm làm bằng chứng có message. Giữ cả các lượt lỗi schema/JSONata và phép kiểm chưa đạt.
- Chênh cách thực thi: dùng .mjs thay dung-dashboard.py do Python ghim không khởi chạy trong sandbox. Browser Use không có host; không vòng sandbox.
- Bước tiếp chính xác: Claude đọc results/T-065/CHECKPOINT.md, kiem/001/BAO-CAO.md, prompt-ban-giao.md; kiểm độc lập nguồn/đầu ra. Cấp môi trường browser phù hợp rồi kiểm ít nhất ba ca × ba kho, điều hướng và phát lại; quyết cách xử lý diễn giải rỗng. Theo dõi results/T-064/ban-xuat/chi-muc-ban.json để tích hợp G-c. Điều phối cập nhật dòng T-065 trong STATE theo phạm vi của mình.
- Lệnh kiểm API bản bàn giao: Get-Content -Raw -Encoding UTF8 results/T-065/api-obs.py | ssh <các tùy chọn khóa/known_hosts trong brief L3> ubuntu@213.35.116.128 "python3 - verify"; kết quả ở kiem/001/api-panels-6.json. Lệnh đối chiếu: import results/T-065/doi-chieu-api.mjs rồi verifyApi("api-panels-6.json","api-links-2.json") trong Node.
- Lệnh shell cuối trước mục này: Get-Content -Raw -Encoding UTF8 results/T-065/api-obs.py | ssh ... ubuntu@213.35.116.128 "python3 - inventory" (lưu codex/api-inventory-cuoi.json). Kiểm hash nguồn cuối bằng Node ở kiem/001/kiem-nguon-cuoi.json.
- Đề xuất commit khi điều phối/Minh duyệt phạm vi một phần: feat(t065): thêm giao diện theo bản và lớp thao tác P7. Chưa commit/push.

### Prompt bàn giao cho Claude — chép mẫu hiện hành

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065 — tasks/T-065-giao-dien-grafana/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: T-065, nhánh giao diện FlashTicket; G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện theo SPEC.
- Tài liệu gốc: AGENTS.md; tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md và BOI-CANH.md; results/T-064/hop-dong-dau-ra.md.
- Phản biện và phản hồi trước: Chưa có bản phản biện chính thức T-065. Mốc hồi quy: tasks/T-062-dem-chang-1-4/REVIEW-G1-5.md và results/T-062/codex/g1-that-2/BAO-CAO.md.
- Code và kết quả liên quan: results/T-065/README.md, manifest.json, kiem/001/BAO-CAO.md, CHECKPOINT.md; results/T-062/giao-dien/, results/T-062/ca/, results/T-062/ket-qua/ và results/T-061/ chỉ đọc. Môi trường/lệnh trong README và LOG T-065.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; quyền ghi lượt phản biện do phiên điều phối xác định riêng.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## Mở phiên L4 — 2026-11-14T01:25:20.735Z — Codex — laptop Minh — người làm T-065

- EXECUTE theo brief L4 được điều phối giao trong quyền chiến dịch. Phạm vi results/T-065/ và chỉ nối LOG này. Không ghi docs/src/T-064.
- Kiểm 66 đầu ra T-064 khớp chỉ mục; kiểm toàn bộ 221 file L3 trong manifest không lệch. Không chạy lại M1.
- Thử duy nhất cua.getState(): browsers=[], Browsers: Error: The browser access host is unavailable. Dừng bấm thật; không nhập mật khẩu hay tìm đường khác.


## Kết phiên L4 — 2026-11-14T02:00:34.116Z — Codex, người làm, laptop Minh

1. Đã làm: tích hợp chiều bản p7/V032/V041 cho cùng 22 ca; hạng/cờ/cạnh từ đúng đầu ra. Xuất trạng thái API sẵn cho panel rỗng; đọc raw trace dev để phân loại và dựng route metric có nguồn. Giữ dashboard bản 6/L3. Không chạy lại M1. Chi tiết/giới hạn: results/T-065/kiem/002/BAO-CAO.md.
2. File đổi: chỉ results/T-065/ (mã L4, dữ liệu đầy đủ/phép chiếu, hai dashboard, schema 0.4, kiểm 002, checkpoint, README/XONG/manifest/prompt và biên bản máy) và nối LOG này. Không ghi docs/STATE, src, T-064 hoặc task khác. Tập cụ thể ở manifest.json; manifest L3 giữ codex/manifest-L3.json.
3. Kiểm: 66 đầu ra nguồn khớp trước/sau; 66 cặp với 1.121 dòng thực thể, 1.538 cờ, 19.892 đơn vị, 456 cạnh, 14.955 thao tác khớp nguồn, giữ số nguyên ns. 33.002 URL giải mã một lần; schema 66/66, phép chiếu 1.188/1.188; hồi quy 9 ca P7 khớp L3. Raw dev: 13 hash, 2.535.887 span, 196 dòng thao tác message. API cuối 132 trang/2.442 target khớp hạng/cờ/cạnh/thao tác/link/biến/trạng thái. 54 mẫu ba kho × sáu ca × ba bản có dữ liệu. Snapshot 1.870 truy vấn: 639 có dữ liệu, 1.231 rỗng, 0 lỗi. 185 file máy cũ giữ hash, 2.822 file mới khớp; không chủ động restart. Giữ lỗi tự kiểm màu LOW_SUPPORT, lỗi GNU tar và lỗi API khi Docker OOM/restart 01:39:46Z. Giảm dữ liệu đọc lặp, giữ slot, kiểm lại đạt; không tăng RAM/config.
4. Còn mở: toàn task một phần vì browser host unavailable sau một lần cua.getState; chưa bấm thật/ảnh/render/href. P2 của REVIEW.md đạt phần API bằng trạng thái sẵn, chưa kiểm nhìn thấy trên browser. P3 đã có kiểm raw message; span link vẫn chưa hỗ trợ. Hai hash cấp bản P7 null theo chỉ mục, không suy giá trị. Folder Grafana vẫn RCA; thư mục dữ liệu mới, chưa tự đổi provider; câu hỏi phân biệt hai nghĩa thư mục chưa có trả lời. G-c đã kiểm ba bản hiện hành, không khóa M1-FT hay tự nghiệm thu. Giao diện đóng góp DT18 nhưng không trả lời xong RQ5, không đổi quyết định nghiên cứu.

- Bước tiếp chính xác: Claude đọc results/T-065/kiem/002/BAO-CAO.md, CHECKPOINT.md, README-L4.md và prompt-ban-giao.md; kiểm độc lập theo prompt. Sau đó kiểm luồng thật trong phiên có browser host/Grafana đã đăng nhập, ít nhất ba ca và ba kho; giữ ảnh, không nhập mật khẩu thay Minh. Không cần chạy lại M1/snapshot/kiểm dữ liệu hợp lệ. Nếu cần folder Grafana riêng thì trình thay đổi provider cụ thể; không sửa trong quyền L3. Điều phối cập nhật STATE.
- Lệnh API cuối: Get-Content -Raw -Encoding UTF8 results/T-065/l4-api.py | ssh -i D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts -o StrictHostKeyChecking=yes ubuntu@213.35.116.128 "python3 - links"; kết quả api-links-3.json. Kiểm đầy đủ cùng lệnh thay links bằng verify, kết quả api-panels-3.json; đối chiếu bằng l4-kiem.mjs::verifyApiL4.
- Lệnh shell cuối trước mục này: SSH đọc Docker events quanh 01:39Z và journalctl -k lọc OOM; đầu ra codex/l4-docker-events.jsonl và l4-kernel-oom.txt. Tiếp theo chỉ chốt manifest/đối chiếu file cục bộ, không thay máy.
- Đề xuất commit sau khi Minh duyệt: feat(t065): thêm chọn bản M1 cùng ca và trạng thái truy vấn Grafana. Chưa commit/push/merge.

### Prompt bàn giao Claude — nguyên mẫu hiện hành

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065 — tasks/T-065-giao-dien-grafana/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: T-065, nhánh giao diện chiến dịch M1-FlashTicket; G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện theo SPEC.
- Tài liệu gốc: AGENTS.md; tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md; results/T-064/hop-dong-dau-ra.md và ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md; LOG.md của T-065.
- Code và kết quả liên quan: results/T-065/README-L4.md, manifest.json, l4-*.mjs, l4-api.py, grafana-l4/, du-lieu-l4/, kiem/002/, CHECKPOINT.md, thay-doi-may.md; môi trường và lệnh trong README-L4.md.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat. Quyền ghi bản phản biện mới do phiên điều phối xác định riêng theo quyền chiến dịch.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## Mở phiên L5 — 2026-11-14T04:07:16.9818632Z — Codex — laptop Minh — người làm T-065

- Phân loại EXECUTE theo brief L5 Minh giao trong Codex app. Phạm vi: folder Grafana, kiểm Chrome thật, sửa giao diện trong T-065 và bàn giao; không ghi STATE, không commit/push. Quyền folder đã đối chiếu DECISIONS 14/11/2026. Claude phản biện/điều phối.



## L5 — 2026-11-14T05:39:29.835Z — Codex, laptop Minh, người làm

1. Đã xếp Grafana vào cây lồng và thêm mục lục. Sửa bảng metadata và lời diễn giải panel rỗng. Phủ rộng trên Chrome đủ 66 cặp. Kiểm sâu chốt 39 liên kết, 16 thao tác và 8 service. Tiếp nhận sau gián đoạn và đối chiếu phần đã lưu.
2. File đổi nằm trong results/T-065/ và mục nối LOG này. Trên máy đổi file provider, vị trí 6 dashboard, thêm mục lục và sửa 2 JSON L4. Xóa RCA cũ đã kiểm rỗng. Không ghi STATE.
3. Kiểm 7 UID bằng API, 4 hash lưu trữ, 66 PNG, 66 đối chiếu DOM/URL và 27 bản ghi máy. 14 Loki rỗng khớp API. 10 quan sát rỗng chưa phân xử.
4. L5 một phần. Điều cần Minh là gắn @Chrome cho đúng chat. Phần còn lại và thông tin tiếp nhận ở BAN-GIAO-L5.md. T-065 hỗ trợ giao diện DT18, RQ5 vẫn phụ thuộc thực nghiệm.

Bước tiếp mở tab L5 217960284, đọc kết quả Prometheus ở 217960455 nếu còn, rồi chạy L5Deep.init()/advance(). Nếu tab Explore mất, mở lại riêng bước đang dở trên dashboard. Lệnh cuối dự kiến là node results/T-065/l5-tong-hop.mjs manifest.

### Prompt độc lập cho Claude

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, L5. tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L5-brief.md.
- Công đoạn: soát kết quả.
- Gói/cổng: Chiến dịch M1-FlashTicket, phần tích hợp giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm T-065. Claude phản biện và điều phối.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, tasks/T-065-giao-dien-grafana/LOG.md, results/T-065/codex/L5-brief.md, results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md và tasks/T-065-giao-dien-grafana/LOG.md.
- Code và kết quả liên quan: results/T-065/BAN-GIAO-L5.md, results/T-065/manifest.json, results/T-065/CHECKPOINT.md, results/T-065/kiem/003-trinh-duyet/BAO-CAO.md, results/T-065/thay-doi-may.md và các script l5-*.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ nhận xét trong chat và ghi file phản biện nếu Minh duyệt đúng vị trí theo tasks/T-065-giao-dien-grafana/SPEC.md.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## L5 — 2026-11-14T07:02:49.3542647Z — Codex, laptop Minh, người làm — nối sau cập nhật Codex

1. Chrome hoạt động lại sau cập nhật Codex. Phủ rộng đạt 66/66 trang, 22 ca mỗi bản và đủ 66 PNG. Mẫu sâu đã đi qua 13/18 cặp, ghi 27/36 service, 52/72 thao tác và 9 lần đổi bản giữ ca, service, cửa sổ. Đã lưu 122/162 kết quả Explore gồm 52 Tempo, 44 Loki và 26 Prometheus. Trong đó 121 kết quả đã chốt phần đọc Chrome. Còn 40 liên kết chưa bấm và một lượt Loki cần đọc lại editor.
2. Ghi bằng chứng, báo cáo và checkpoint trong results/T-065, chỉ ghi thêm LOG này. Không đổi thêm trên exp-obs hay ghi STATE.
3. Kiểm số khóa và ảnh đã lưu. Phát lại T-062 V041/2e2a5541 đạt 6/6 đối chiếu. Cây Grafana đã có bằng chứng 7 UID và 4 hash lưu trữ.
4. Hạn mức sắp hết, L5 một phần. UI-03 chưa triển khai. Mười panel e8661e0a chưa phân xử. Còn bản M1-FT cuối theo SPEC.

Tab L5 217960473 ở V032-H5b/4af494a5, payment-service, Channel.waitForConfirms (oe819fc37fe58d0462c15). Nhật ký #1587 xác nhận đã chọn thao tác. Cửa sổ UTC [2026-11-13T07:50:38.000Z, 2026-11-13T08:00:38.000Z). sau-tien-do.json ghi pair=13, service=0, op=0, link=0, stage=op, pending=null. Không có tab Explore đang chờ hoặc tiến trình kiểm nền. Tiếp đọc panel 24/25, sau đó bấm Tempo và Loki của thao tác này.

Lệnh máy cuối `& results/T-065/l5-may.ps1 -Nhom 'L5 V032-H5b 4af494a5 dev-2'`. Lệnh chốt manifest `node results/T-065/l5-tong-hop.mjs manifest`.

### Prompt độc lập cho Claude

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, L5. tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L5-brief.md.
- Công đoạn: soát kết quả.
- Gói/cổng: Chiến dịch M1-FlashTicket, phần tích hợp giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm T-065. Claude phản biện và điều phối.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, tasks/T-065-giao-dien-grafana/LOG.md, results/T-065/codex/L5-brief.md, results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md và tasks/T-065-giao-dien-grafana/LOG.md.
- Code và kết quả liên quan: results/T-065/BAN-GIAO-L5.md, results/T-065/manifest.json, results/T-065/CHECKPOINT.md, results/T-065/kiem/003-trinh-duyet/BAO-CAO.md, results/T-065/thay-doi-may.md và các script l5-*.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ nhận xét trong chat và ghi file phản biện nếu Minh duyệt đúng vị trí theo tasks/T-065-giao-dien-grafana/SPEC.md.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## L5 — 2026-11-14T07:07:44.183Z — Codex, laptop Minh, người làm — tiếp sau khi hạn mức hồi

- Minh yêu cầu hoàn thiện phần còn lại. Kiểm hash 7 tệp điểm tiếp nhận đạt. Tiếp pair=13, giữ 66 trang và 122 kết quả Explore.


## L5 — 2026-11-14T07:21:59.176Z — Codex, laptop Minh, người làm — kết thúc phần độc lập của lượt nối

1. Đã sửa nguồn l4-dashboard.mjs và triển khai hai JSON L4 lúc 07:15Z. Bảng chi tiết/phát lại dùng hai cột xuống dòng, nhãn snapshot có ánh xạ, thêm chú giải màu, sửa lời diễn giải ô thiếu giá trị.
2. File trong results/T-065 gồm nguồn dựng, hai JSON và bản trước để hoàn tác, script l5-ui-kiem/deploy, phản hồi API, báo cáo, checkpoint, bàn giao, status và manifest. Chỉ nối LOG T-065. Trên exp-obs chỉ cập nhật hai file L4 trong folder hiện hành, backup vào thư mục dữ liệu T-065. Hash/lệnh/hoàn tác ở thay-doi-may.md.
3. 12/12 slot API kiểm trên T-062/dev qua ba bản đạt. Hai hash máy khớp file cục bộ và API đã nạp version 5/4. Giữ bốn JSON lưu trữ và bảy UID. Bổ sung Loki 2e2a5541 Booking, HTTP 200/0 dòng, cả 24 lượt Loki rỗng đều có đối chứng. 66 trang và 122 liên kết trước đó còn đủ file PNG, 121 liên kết đủ kiểm editor.
4. Chưa hoàn thành kiểm Chrome. Browser runtime báo quyền của chat không khả dụng, đã hỏi Minh gắn @Chrome. Skill computer-use mở được tab mới riêng tới Grafana, thấy bản V032/ca4af494a5/servicePayment/opChannel.waitForConfirms. Công cụ dừng theo chính sách xác định URL. Đã dừng thao tác UI, ghi lỗi trong ket-noi-chrome-0707.json. Còn 40 liên kết, một editor cần đọc lại, ảnh graph, phát lại dev và kiểm UI sau sửa. Mười panel rỗng loại iii còn thiếu Query Inspector. G-c vẫn phụ thuộc bản M1-FT cuối. L5 không kết luận lợi ích RCA hay hoàn thành RQ5.

Bước tiếp chính xác: Minh gửi @Chrome, kiểm STOP và l5-may.ps1, tạo instance L5Browser/L5Deep mới, reload tab L5 đúng URL trong BAN-GIAO-L5.md. Đọc panel 24/25 rồi tiếp pair13/service0/op0/link0/stage=op. Không lặp các phép kiểm có bằng chứng. Lệnh chốt lượt là node results/T-065/l5-tong-hop.mjs manifest, rồi đọc hash của các tệp bàn giao để kiểm nhất quán.

### Prompt độc lập cho Claude

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, L5. tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L5-brief.md.
- Công đoạn: soát kết quả.
- Gói/cổng: Chiến dịch M1-FlashTicket, phần tích hợp giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm T-065. Claude phản biện và điều phối.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, tasks/T-065-giao-dien-grafana/LOG.md, results/T-065/codex/L5-brief.md, results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md và tasks/T-065-giao-dien-grafana/LOG.md.
- Code và kết quả liên quan: results/T-065/BAN-GIAO-L5.md, results/T-065/manifest.json, results/T-065/CHECKPOINT.md, results/T-065/kiem/003-trinh-duyet/BAO-CAO.md, results/T-065/thay-doi-may.md và các script l5-*.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ nhận xét trong chat và ghi file phản biện nếu Minh duyệt đúng vị trí theo tasks/T-065-giao-dien-grafana/SPEC.md.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.



## L5 — 2026-11-14T07:42:50.924Z — Codex, laptop Minh, người làm — thử kết nối sau khi Minh gắn lại Chrome

- Đã thử ba đường khởi tạo gồm reset Node và đúng plugin. Cùng lỗi local browser access. Giữ mọi dữ liệu và trạng thái pair13. Không đổi máy hay nguồn dashboard trong lượt này. Cần thử tag từ tin nhắn thường. Lệnh kiểm chỉ đọc: Node REPL setupBrowserRuntime, browsers.list. Đã ghi CHECKPOINT và status. Manifest được cập nhật hash đúng các tệp ghi thêm.

### Prompt độc lập cho Claude

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, L5. tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L5-brief.md.
- Công đoạn: soát kết quả.
- Gói/cổng: Chiến dịch M1-FlashTicket, phần tích hợp giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm T-065. Claude phản biện và điều phối.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, tasks/T-065-giao-dien-grafana/LOG.md, results/T-065/codex/L5-brief.md, results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md và tasks/T-065-giao-dien-grafana/LOG.md.
- Code và kết quả liên quan: results/T-065/BAN-GIAO-L5.md, results/T-065/manifest.json, results/T-065/CHECKPOINT.md, results/T-065/kiem/003-trinh-duyet/BAO-CAO.md, results/T-065/thay-doi-may.md và các script l5-*.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ nhận xét trong chat và ghi file phản biện nếu Minh duyệt đúng vị trí theo tasks/T-065-giao-dien-grafana/SPEC.md.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.



## L5 — 2026-11-14T07:48:35.193Z — Codex, laptop Minh, người làm — thử tag Chrome trực tiếp

- Runtime tiếp tục báo local browser access. Computer Use đọc được URL Grafana nhưng dừng trước thao tác tìm bảng theo chính sách xác định URL. Dừng UI. Không phát sửa trên máy. Một lần đọc stats và runner3 đã lưu. Giữ checkpoint pair13. Tệp tiếp nhận cho chat mới là results/T-065/codex/L5-prompt-tiep-nhan.md, kết nối mới chưa kiểm.

### Prompt độc lập cho Claude

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, L5. tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L5-brief.md.
- Công đoạn: soát kết quả.
- Gói/cổng: Chiến dịch M1-FlashTicket, phần tích hợp giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm T-065. Claude phản biện và điều phối.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, tasks/T-065-giao-dien-grafana/LOG.md, results/T-065/codex/L5-brief.md, results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md và tasks/T-065-giao-dien-grafana/LOG.md.
- Code và kết quả liên quan: results/T-065/BAN-GIAO-L5.md, results/T-065/manifest.json, results/T-065/CHECKPOINT.md, results/T-065/kiem/003-trinh-duyet/BAO-CAO.md, results/T-065/thay-doi-may.md và các script l5-*.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ nhận xét trong chat và ghi file phản biện nếu Minh duyệt đúng vị trí theo tasks/T-065-giao-dien-grafana/SPEC.md.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.



## L5 — 2026-11-14T07:52:26.027Z — Codex, laptop Minh, người làm — tiếp nhận chat mới có @Chrome

- Minh yêu cầu hoàn thiện brief trong quyền đã cấp. Claude giữ vai trò phản biện. Đã đọc AGENTS, STATE, SPEC và bàn giao tại results/T-065/. Giữ dữ liệu và ảnh cũ. Đã kiểm 5283 hash manifest, không lệch. Tiếp pair13, kiểm STOP/máy rồi khởi tạo instance mới.


## L5 — 2026-11-14T08:33:29.546Z — Codex, laptop Minh, người làm — checkpoint theo yêu cầu Minh

1. Tiếp nhận chat mới có Chrome CUA, kiểm5283 hash và66 nguồn không lệch. Hoàn tất mẫu sâu162link/72op/36service/18cặp/12đổi bản; editor Loki đọc lại đạt. Rà36 graph,giữ2ảnh đủ,bổ sung34 và54khung;34đối chiếu SVG đạt,hợp ảnh không thiếu node. Chốt LOW_SUPPORT→chi tiết tab mới7/7.
2. File đổi chỉ results/T-065/ và nối LOG này. Script mới l5-cua-adapter.mjs,l5-graph-qa.mjs,l5-checkpoint-chat-moi.mjs. Báo cáo/checkpoint/prompt/manifest và tạo tác ảnh/DOM/JSON của lượt; bản báo cáo cũ giữ riêng. Máy chủ không đổi9hash. Mở tunnel local riêng sau mất listener;session30562/PID24712 giữ cho tiếp nhận. Không ghiSTATE haynguồn M1,không commit/push.
3. Kết quả tổng hợp từ tien-do.json và kiem-chot-checkpoint-chat-moi.json.24Loki rỗng đều có API;177panel loại(i),10lịch sử loại(iii). Máy cuốiSTOP=false,runner3=0,restart0,359.9MiB/768MiB. Kiểm cú pháp/diff/tập file vàmanifest thực hiện ngay sau mục này.
4. Task một phần,không thêm/đổi quyết định nghiên cứu. G-a thiếuChromeUI04/phát lại/Inspector;G-b đạt luồngmẫu,giới hạnspanlink vàràkhac còn ghi rõ;G-c chờbảncuối. DT18 được bổ sung bằng chứnggiao diện;không đóngRQ5 haykhẳng địnhlợi íchRCA. Minh yêu cầucheckpoint vìusage;đề nghị tiếp đúngphầnthiếu,không chấpnhậncheckpoint như nghiệmthu.

Bước tiếp/lệnh/tab theo CHECKPOINT mục 2026-11-14T08:33:29.546Z,BAN-GIAO-L5.md vàcodex/L5-prompt-tiep-nhan.md. Lệnh cuối đã chạy:node results/T-065/l5-tong-hop.mjs. Lệnh chốt sẽ chạy:node results/T-065/l5-tong-hop.mjs manifest. Đề xuất commit khiMinh duyệt riêng: test(t065): hoàn tất mẫu sâu Chrome và lưu graph QA L5;chưa commit/push.

### Prompt độc lập cho Claude

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, L5; tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L5-brief.md.
- Công đoạn: soát kết quả.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện và điều phối.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, LOG.md; results/T-065/codex/L5-brief.md; results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md và LOG.md.
- Code và kết quả liên quan: results/T-065/BAN-GIAO-L5.md, CHECKPOINT.md, manifest.json, kiem/003-trinh-duyet/, các script l5-* và grafana-l4/.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và nhận xét trong chat; ghi file phản biện khi Minh cho phép đúng vị trí theo SPEC.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


- QA ảnh cuối: Ảnh ui04-low-support-detail.png đọc được tên/trạng thái và các dòng chính nhưng cắt dòng Giới hạn metric cuối bảng; DOM đã lưu đủ 9 dòng. Lượt tiếp cần ảnh View panel24 hoặc cuộn đến dòng cuối, không cần kiểm lại dữ liệu thao tác.


### Kiểm tra chốt checkpoint

- Ba script mới qua node --check (exit 0). git diff --check exit 0. Không thiếu file, PNG cũ không đổi. Khôi phục mảng cũ để so hash xác nhận giữ đủ 122 link, 52 thao tác, 27 service và 9 đổi bản; chỉ bổ sung bằng chứng đọc lại editor. CHECKPOINT/journal/may.jsonl giữ nguyên tiền tố cũ. Có đủ 54 PNG graph được dẫn. Chi tiết ở kiem/003-trinh-duyet/kiem-tap-file-chat-moi.json.
- L5 một phần theo yêu cầu Minh. Phần UI04/phát lại/Inspector và ảnh dòng cuối panel24 ở prompt tiếp nhận. Tunnel local riêng session30562/PID24712 giữ cho tiếp nhận; không có tiến trình kiểm nền.
- Lệnh chốt cuối của lượt: node results/T-065/l5-tong-hop.mjs manifest. Không commit/push.

### Prompt bàn giao cuối cho Claude — bản chuẩn

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, L5; tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L5-brief.md.
- Công đoạn: soát kết quả.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện và điều phối.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, LOG.md; results/T-065/codex/L5-brief.md; results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md và LOG.md.
- Code và kết quả liên quan: results/T-065/BAN-GIAO-L5.md, CHECKPOINT.md, manifest.json, kiem/003-trinh-duyet/, các script l5-* và grafana-l4/.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và nhận xét trong chat; ghi file phản biện khi Minh cho phép đúng vị trí theo SPEC.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## L5 — 2026-11-14T08:39:22.346Z — Codex, laptop Minh, người làm — usage hồi, tiếp UI04

- Minh yêu cầu tiếp tục. Giữ Claude phản biện; không đổi quyền. Đọc checkpoint/bàn giao/prompt cuối; kiểm hash đúng phần sẽ dùng đạt. Tunnel PID24712 còn listener. Dùng lại66trang/162link/36graph; chỉ kiểm phần UI04/phát lại/Inspector và ràkhac còn thiếu.


## L5 — 2026-11-14T08:46:18.857Z — Codex, laptop Minh, người làm — rà khac xong, Chrome bị chặn

1. Đọc lại prompt/checkpoint sau ngắt. Thử ba đường Chrome rồi dừng UI vì cùng lỗi trước truy cập trang. Rà 1.997 dòng khac/131 tên, 491 span ví dụ từ hai raw khớp hash, phủ 131/131. Lần theo raw → kind → nhãn khac. Không sửa nhãn/M1. Dùng lại mẫu 66 trang/162 link/36 graph.
2. File mới/đổi chỉ results/T-065 và nối LOG: script audit, kết quả, biên bản kết nối, báo cáo/checkpoint/status, hai prompt và manifest. Không đổi máy chủ, src/docs/T-064/STATE. Không commit/push.
3. Cú pháp script audit đạt; hai raw hash khớp, ba check audit đạt. Máy STOP=false, runner3=0, 310.9MiB/768MiB, restart0. Kiểm cú pháp/diff/hash cuối thực hiện ngay sau phần chốt. Mẫu UI cũ không đổi trong lượt.
4. P3 đạt phần rà; G-a và các mục UI-04 bị kết nối chặn, G-c chờ bản cuối. T-065 thêm bằng chứng giao diện DT18, không khẳng định lợi ích RCA hoặc đóng RQ5. Không thêm/đổi quyết định nghiên cứu. Đề nghị tiếp phần thiếu khi Chrome hoạt động, không thay bằng API hoặc coi brief đã xong.

Bước tiếp: đọc BAN-GIAO-L5/CHECKPOINT mục 2026-11-14T08:46:18.857Z, thử kết nối @Chrome, kiểm máy, rồi chỉ làm UI-04/phát lại/Inspector. Lệnh cuối đã chạy: node results/T-065/l5-khac-audit.mjs. Lệnh chốt cuối: node results/T-065/l5-tong-hop.mjs manifest. Tunnel PID24712/session30562 giữ; không job kiểm nền. Đề xuất commit khi có duyệt riêng: test(t065): bổ sung audit khac và bàn giao L5; chưa commit/push.

### Prompt độc lập cho Claude

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, L5; tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L5-brief.md.
- Công đoạn: soát kết quả.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện và điều phối.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, LOG.md; results/T-065/codex/L5-brief.md; results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md và LOG.md.
- Code và kết quả liên quan: results/T-065/BAN-GIAO-L5.md, CHECKPOINT.md, manifest.json, kiem/003-trinh-duyet/, l5-khac-audit.mjs, các script l5-* và grafana-l4/.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và nhận xét trong chat; ghi file phản biện khi Minh cho phép đúng vị trí theo SPEC.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## L5 — 2026-11-14T08:53:39.900438+00:00 — Codex, laptop Minh, người làm — tiếp UI04 bằng Chrome mới

Đã đọc AGENTS, brief/prompt, SPEC, cuối LOG/CHECKPOINT, bàn giao và nguồn yêu cầu. Minh giao tiếp phần còn lại, không ghi STATE/src/docs/T-064, không commit/push. Chrome tab 217961015 kết nối thành công sau sửa kiểu ID số thành chuỗi; không dùng binding cũ. Listener 13000 vẫn PID24712. Kiểm 5.963 hash: chín hồ sơ lệch đã giải thích bằng script chốt audit, bản sao và tiền tố append-only; 66 nguồn T-064 đều khớp. Giữ manifest cũ ở codex/manifest-L5-truoc-UI04-suite.json. Chỉ tiếp UI04/phát lại/Inspector, không làm lại mẫu, graph hay audit.


### 2026-11-14T08:59:04.338078+00:00 — UI04/phát lại và sửa header UI05

Ảnh cuối panel24 đạt, dev19b chỉ hiện giới hạn. Gặp và giữ lượt header phát lại có thời gian rỗng lúc biến ẩn tải; sửa trong quyền L5 đúng l4-dashboard.mjs và content panel1 hai JSON L4, triển khai hai file có backup/hash. Không đổi query/targets hoặc dữ liệu. Bảng2e2a11dòng đã đọc/chụp toàn bộ ở View panel7; đường về chính giữ ngữ cảnh. Ảnh/table chưa dựng đủ được giữ làm lượt lỗi; không tính đạt. Tiếp10Inspector và panel28/31–35.


### 2026-11-14T09:06:17.566951+00:00 — UI06

UI06: đối chứng hiện tại cùng p7/e8661e0a/event-service/panel31: hard navigation numeric URL tạo request from/to NaN và step8760h; ISO cùng instant tạo from1794444870000/to1794445469999, step15s và40dòng/chuỗi. DOM/ảnh inspector-ui05-* giữ nguyên. Không suy nguyên nhân10quan sát lịch sử. Sửa nguồn và hai JSON L4: default time, header, biến ẩn và thời gian danh sách dùng ISO UTC; mọi panel live targets và panel7/24 targets không đổi. Deploy qua stdin SSH, không restart; hash/backup tại ui06-plan.json, ui06-deploy.jsonl và grafana-l5/ui06. Hoàn tác dùng /opt/flash-ticket-obs/rca-ket-qua/t065-l4-001/rollback/l5-ui06/ về vị trí ghi trong manifest deploy; source local có bản sao trước. Numeric bookmark cũ chưa được biến thành hợp lệ; cần ISO URL hoặc chọn ca sau bản sửa.
Tiếp10Inspector trên URL ISO; không kiểm lại66trang/162link/36graph, không đọc raw hoặc audit lại.


## L5 — 2026-11-14T09:26:52.372474+00:00 — Codex, laptop Minh, người làm — kết lượt UI06

1. Đã làm: phần Chrome còn lại đủ bằng chứng; Inspector10/10 đúngquery/window HTTP200, T06211dòng/dev1giới hạn/snapshot5dòng, ảnh cuối24. Sửa lỗi thời gian UI05/UI06 trong quyền; giữ toàn bộ lượt cũ. Dùng lại66trang/162link/36graph/auditkhac, không chạy lại M1/raw.
2. File đổi chỉ results/T-065 và nối LOG này. Trên exp-obs chỉ hai JSON L4, backup/hash trong ui05/06-plan/deploy; provider/compose/dashboard lưu trữ không đổi, không restart. Không ghi STATE/docs/src/T-064 hoặc commit/push.
3. Kiểm: 13 điều kiện ui06-kiem-cuoi.json đạt; nguồn dựng hai dashboard khớp, chín file máy đúng kỳ vọng, healthok. Contact sheet mười Inspector đã xem. Kiểm toàn vẹn/diff/tập file và manifest chốt nối ngay sau mục này.
4. Task: phần L5 hiện hành tự kiểm xong; T-065 còn G-c cần bản M1-FT đề xuất cuối, chưa nghiệm thu. Câu hỏi nguồn: bổ sung minh họa DT18; không xác nhận lợi ích RCA hoặc đóng RQ5. Mười quan sát lịch sử thiếu request/response đúng giờ, còn các giải thích tải/tham số/hiển thị; giữ loại(iii), không chạy hiện tại để quy nguyên nhân quá khứ. Đề xuất Claude kiểm độc lập rồi điều phối cung cấp chỉ mục/hash bản cuối; không tự chọn V032/V041. URL số cũ cần ISO/chọn ca; đã ghi README-L4. Không có quyết định nghiên cứu mới.

Bước tiếp chính xác: đọc BAN-GIAO-L5.md, kiem/003-trinh-duyet/ui06-kiem-cuoi.json, manifest.json; kiểm hash rồi phản biện bằng prompt dưới. Khi có bản M1-FT cuối, đối chiếu SPEC/G-c và chỉ kiểm phần tích hợp chịu ảnh hưởng. Không tự chạy lại mẫu đã đạt. Tab217961015/tunnelPID24712giữ, không job nền. Lệnh cuối trước báo cáo: py -3 -X utf8 results/T-065/l5-ui06-validate.py (đạt). Lệnh chốt tiếp: node results/T-065/l5-tong-hop.mjs manifest, sau kiểm tập file. Nội dung commit có thể đề xuất riêng khi Minh yêu cầu: fix(t065): giữ cửa sổ ISO và bổ sung bằng chứng UI L5; lượt này không commit/push.

### Prompt độc lập cho Claude

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, L5; tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L5-brief.md.
- Công đoạn: soát kết quả.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện và điều phối.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, LOG.md; results/T-065/codex/L5-brief.md; results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md và LOG.md.
- Code và kết quả liên quan: results/T-065/BAN-GIAO-L5.md, CHECKPOINT.md, manifest.json, kiem/003-trinh-duyet/, grafana-l4/, l4-dashboard.mjs, các script l5-*; môi trường Windows, Chrome và exp-obs theo brief.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và nhận xét trong chat; ghi file phản biện khi Minh cho phép đúng vị trí theo SPEC.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


### 2026-11-14T09:29:41.440771+00:00 — kiểm diff/tập file trước manifest

Đã kiểm5.984filemốc,khôngmấtfile;18filekếtquảđãcó đổi đúng danh sách; mọiảnh/graph/dữliệu/auditcũngoàidanh sách giữhash.66nguồnT064khớp;diff/statusfileđãtheodõi ngoài phạm vi giữnguyên;LOGappend-only. Đã đọc hết thayđổi nghĩa của haiJSON(20đườngdẫn)vàhunknguồn,khôngđổi livequery/targets7/24. Cúpháp5JS/6Pythonđạt,promptClaudeđúngnguyênmẫu. ui06-integrity.json vàui06-final-checks.json lưu bằngchứng. Lệnhcuốiđãchạy: kiểm cúpháp/template trongPowerShell/Python; bướcchốt: node results/T-065/l5-tong-hop.mjs manifest rồi kiểmchecksumchỉđọc.


### 2026-11-14T09:30:24.115378+00:00 — guard manifest và cách xử lý

Lệnh chốt manifest lần đầu bị guard từ chối trước khi ghi, vì README-L4.md chưa nằm trong allowedModified của bộ chốt cũ. README này nằm trong phạm vi results/T-065 được cấp và chỉ thêm cách dùng URL ISO đã kiểm. Đã thêm đúng README-L4.md vào tập được phép, không nới quyền cho dữ liệu nguồn. Lượt lỗi giữ ở ui06-manifest-guard.json; bản manifest trước lượt vẫn giữ nguyên. Kiểm tập file trước đó xác nhận 5.984 file mốc không mất; 18 file kết quả đã có thay đổi đúng quyền; 66 đầu ra nguồn khớp. Tiếp chốt và kiểm hash, không chạy lại thực nghiệm.


### 2026-11-14T09:31:27.100580+00:00 — checksum chốt đạt

Đã chốt và kiểm manifest: 6256/6256 hash khớp, LOG khớp, không file thiếu hoặc file mới chưa giải thích. Lệnh đã chạy: node results/T-065/l5-tong-hop.mjs manifest và phép kiểm checksum chỉ đọc. Sau khi nối biên bản này, dựng lại manifest để ghim chính LOG/checkpoint/biên nhận mới rồi kiểm checksum cuối trong chat. Không còn thao tác Chrome đang dở; G-c chờ bản M1-FT đề xuất cuối. Toàn bộ đầu ra cũ được giữ.
Bước tiếp: Claude đọc prompt-ban-giao.md để kiểm độc lập; khi điều phối cấp bản cuối và hash hợp lệ mới tiếp G-c. Không chạy lại mẫu cũ.


## L6 — 2026-11-14T10:50:46.878Z — Codex CLI, Windows laptop Minh, người làm — mở lượt đáp REVIEW-2

Phân loại EXECUTE, chỉ đáp phản biện. Minh cấp trong brief 14/11/2026: điền bảng Phản hồi của người làm của REVIEW-2, nối LOG, ghi file phụ results/T-065 nếu cần; không sửa STATE/docs/dashboard/máy chủ, không truy cập Chrome/exp-obs/exp-app, không commit. Không gọi agent khác. Đọc AGENTS, STATE, SPEC, mục cuối LOG, DT18, hướng dẫn cô, MRP và quyết định/lý do/bài học trực tiếp chi phối. STATE còn L3; brief hiện tại chỉ rõ tiếp L5 thành L6, nên không tự cập nhật STATE.

Trước ghi: kiểm manifest L5 bằng PowerShell Get-FileHash: 6.257/6.257 file khớp, không thiếu/lệch; LOG khớp task_log; 66/66 đầu ra trong chỉ mục T-064 khớp. Manifest L5 giữ nguyên. LOG bị ghim; nối L6 sẽ đổi hash toàn file có chủ đích, giữ nguyên tiền tố L5 để kiểm với task_log cũ. Chưa mở nội dung hoặc kết luận REVIEW/REVIEW-2; chỉ lấy bytes/hash REVIEW-2 làm mốc bảo vệ phần reviewer. Phần tự soát độc lập sẽ được ghi ngay dưới trước khi đọc các kết luận.

### L6 — 2026-11-14T10:53:15.725Z — tự soát độc lập, TRƯỚC khi mở kết luận phản biện

- FACT: đối chiếu lại đủ 66 bản xuất với 66 nguồn đã khớp hash. Khớp entity_ranking, cờ, đơn vị, vùng, cạnh, metadata và nhóm tie_group+1; không thấy trường đáp án bị cấm trong bản chính. Đếm trực tiếp: 1.121 thực thể, 1.538 cờ, 19.892 đơn vị, 456 cạnh xếp hạng, 14.955 thao tác, 33.002 URL. Không có LOW_SUPPORT sai màu tím trong 66 bản xuất. Số sẽ lưu ở codex/L6-dap-review2.json#/checks. Không gọi verifyL4 vì hàm đó ghi đè kết quả L4.
- FACT: đếm trực tiếp bằng chứng Chrome cũ: 66 trang (22/bản), 18 cặp bản/ca, 36 service, 72 thao tác, 162 liên kết (72 Tempo, 54 Loki, 36 Prometheus), 36 graph, 12 đổi bản; không thiếu PNG được các bản ghi trỏ tới. Chỉ đây là phạm vi mẫu sâu đã lưu, không là kiểm hết mọi thao tác/mọi truy vấn sau UI06. Tự soát lần này không bấm trình duyệt.
- FACT: đọc đường xuất l4-xuat.mjs và l4-dashboard.mjs: hạng/cờ lấy từ nguồn, đồ thị thao tác là quan hệ span cha–con quan sát; phát lại ghép đáp án riêng, không chấm lại. Chỉ mục ghi V032 đề xuất tạm, V041 thay thế, hai hash cấp bản P7 null. G-c vẫn cần bản đề xuất cuối; không coi đó là lỗi khoa học hay kết luận ứng viên đã khóa.
- FACT: panel-rong.json là nhật ký phát hiện thô (586 bản ghi); kết quả đã đối chiếu ở doi-chieu-rong-snapshot.json còn 187 panel (177 loại i, 10 loại iii), không lấy hai tập làm cùng đại lượng. Mười quan sát lịch sử thiếu request/response đúng giờ; các giải thích còn lại là tham số/tải/hiển thị. Chỉ log/network/ảnh đúng giờ cũ mới phân xử được; chạy lại hiện tại không tái tạo bằng chứng lịch sử. Giữ giới hạn này, không quy lỗi dữ liệu/M1.
- FACT: mã dashboard hiện tại khớp hash nguồn trong biên nhận tái dựng; hai bản dựng cuối đã lưu khớp cấu trúc với hai JSON hiện hành. Không tuyên bố đã chạy lại generator. Thử dựng trong bộ nhớ bị môi trường chặn sinh code từ chuỗi; một phép đối chiếu đầu lỗi do chưa import util, đã sửa cách gọi chỉ trong bộ nhớ và chạy được. Không file kết quả cũ bị ghi lại.
- CANDIDATE cần chú ý khi tiếp nhận: l5-ui06-validate.py cuối hàm ghi ui06-kiem-cuoi.json, dù docstring nói kiểm bằng chứng đã lưu. File đích bị manifest ghim. L6 không chạy script ấy hoặc l5-tong-hop.mjs; dùng kiểm chỉ đọc, không đổi hash biên nhận cũ. Chưa quy đây là finding tính đúng của đầu ra L5 vì L5 có quyền ghi và các hash hiện khớp.
- Kết luận tự soát trước review: chưa phát hiện thêm lỗi đáng kể trong các giá trị xuất và ranh giới kết luận đã kiểm ở trên. DT18-NV3 được hỗ trợ ở phần giao diện minh họa; bằng chứng UI không xác nhận hiệu quả RCA hoặc đóng RQ5. Còn phải kiểm từng ý REVIEW-2 bằng file thật; chưa đọc kết luận REVIEW/REVIEW-2.

### L6 — 2026-11-14T11:00:14.554Z — điểm N1 tự tìm khi đối chiếu R2 trên file gốc

N1 — KHÔNG CHẶN riêng bản UI06; chặn dùng ba quan sát trace cũ làm bằng chứng đúng cửa sổ. Đếm đủ panel34 trong 66 trang đã lưu: 660 thời điểm Start time đọc được; 30 thời điểm ở ba trang e8661e0a (P7/V032/V041) ngoài cửa sổ. Ba file 021-trang-p7-e8661e0a.json, 043-trang-V032-H5b-e8661e0a.json, 065-trang-V041-R1-H1c_H5b_H8s1-e8661e0a.json đều trỏ /panel_checks/panels/19/text trong kiem/003-trinh-duyet. Cửa sổ nguồn là 2026-11-12T00:54:30Z–01:04:30Z; dòng trace lại ở 14/11 khoảng 04:27/04:37/04:52Z. 630 thời điểm còn lại của 63 trang nằm trong cửa sổ tương ứng. Đây là lỗi hiển thị thời gian đã quan sát trong lịch sử, không chỉ là panel rỗng và không thay số M1.

Xét phần có thể bác finding: nguồn sau UI06 hiện có 10/10 dòng P7 ở ui06-p7-live-panels.json#/panels/34, 10/10 dòng V041 ở ui06-V041-live-panels.json#/panels/34 và 10/10 dòng V032 trong phần Trace của ui06-inspector-04-V032-event-p31-dom.txt đúng cửa sổ; không nói lỗi còn hiện hành. Thiếu request/response đúng giờ cũ nên chưa phân biệt request sai thời gian do URL số với khung dữ liệu cũ hoặc tham số/datasource fallback. Giao diện dùng UTC; lệch hai ngày không được giải thích bằng múi giờ. Chỉ dùng log/network đúng lúc cũ nếu đã lưu để quy cơ chế; không thể tạo lại bằng chạy mới. Đề xuất thêm giới hạn lịch sử này vào báo cáo/bàn giao sau khi Minh duyệt, giữ mọi file cũ. Không cần chạy lại 66 trang; phần còn cần bấm thật sau UI06 thuộc R1. Bằng chứng chi tiết sẽ ở codex/L6-dap-review2.json#/checks.

### L6 — kết luận đáp REVIEW-2 và đề xuất, chưa sửa đầu ra L5

**Vai trò:** Codex người làm. Claude vẫn là người phản biện. Các ý dưới đây là phản hồi và đề xuất, không là quyết định của Minh.

- **R1 — đúng, CHẶN nghiệm thu G-b trên UI06.** Đếm độc lập 10 khác biệt cấu trúc mỗi JSON. Hai biến thời gian đổi sang ISO; data link ở panel 4/22/23 của trang chính và panel 4 của phát lại dùng chính chúng. Đọc đủ 91 hành động sau 09:06Z, không có bấm những data link ấy. Các thao tác đổi service/bản bằng ô chọn, bấm danh sách ca và header không thay phép kiểm đường nội suy biến trong liên kết. Giới hạn câu G-b của bàn giao L5: phần hạng/cờ/đồ thị cũ còn hợp lệ, nhưng luồng điều hướng bị ảnh hưởng chưa được kiểm lại. Không có bằng chứng rằng liên kết hiện đang hỏng; đây là thiếu bằng chứng nghiệm thu. Xem `codex/L6-dap-review2.json#/checks`, mục `R1_ui06_structure_and_time_variable_consumers`.
- **R2 — đúng, KHÔNG CHẶN.** Đếm lại khớp 36/36 URL số của e8661e0a, 0 ISO; 21 ca khác: 67 URL số trên 1.665 hành động, 1.598 ISO. Đây là hành động, không phải 1.701 phép đo độc lập. Đã đọc cả 67 DOM tương ứng: 66 file chỉ có `Loading Grafana`, file còn lại chỉ có vỏ trang; không có panel sống để làm đối chứng URL số vẫn trả dữ liệu đúng. Có căn cứ ghi numeric URL là ứng viên giải thích lịch sử, chưa đủ quy cơ chế. Giữ 10 quan sát rỗng loại (iii). Bổ sung N1 cho phần không rỗng, không thu hẹp nghiên cứu về chỉ kiểm panel rỗng. Xem các mục `R2_*` trong file kiểm L6.
- **R3 — đúng, KHÔNG CHẶN.** File thô có 586 bản ghi (154 i, 432 iii), gồm 18 trùng khóa. 568 khóa sau gộp tách thành 381 false positive và 187 panel thực cần đối chiếu (177 i, 10 iii). Số tổng hợp đúng; thiếu chỉ dẫn rõ nguồn phân loại hiện hành. Không xóa hoặc sửa file thô.
- **R4 — đúng một phần, KHÔNG CHẶN.** FACT đã xóa folder rỗng: `folder-rca-xoa.json#/contents/data` và `#/children/data` đều rỗng, `#/delete/http` là 200 lúc 04:16:03Z. Brief L5 §2 ghi rõ “nếu sau khi chuyển đã rỗng thì được xóa”. Cũng phải xét DECISIONS mục “Bổ sung quyền điều phối chiến dịch nhiều ngày, 13/11/2026”: Minh giao “toàn quyền điều phối và triển khai”, các việc trong gói không chờ duyệt lại; mục folder 14/11 giao Claude chọn cách sắp xếp và dẫn tới brief. Câu ghi nhận quyền máy liệt kê rõ provider/chuyển file nhưng không ghi DELETE. Có hai cách hiểu: (a) xóa folder rỗng là phần triển khai cách sắp xếp được giao; (b) danh sách thao tác trong ghi nhận quyền máy là giới hạn đóng. Không tự chọn một cách làm DECIDED. Finding đã xét brief nhưng chưa xét đủ quyền giao ngày 13/11; vì vậy chưa đủ căn cứ khẳng định chắc vượt quyền. Minh phân xử. Đề xuất giữ trạng thái hiện tại và xác nhận phạm vi của việc đã làm; không tạo lại folder chỉ để sửa hồ sơ. Mặt trái: cần nói rõ văn bản cho phép ở thời điểm làm. Phương án khác là tạo lại nhưng UID có thể đổi và không khôi phục danh tính cũ; phải được Minh cho phép, không làm trong L6.
- **N1 — KHÔNG CHẶN riêng UI06.** Chi tiết ở mục vừa ghi trước bảng phản hồi: 30/660 Start time đọc được trong 3/66 trang lịch sử sai cửa sổ, đều e8661e0a; 630 dòng của 63 trang còn lại đúng cửa sổ. Sau UI06, 10 dòng mỗi bản của ba bản đều đúng cửa sổ trong bằng chứng đã lưu. Chặn dùng ba panel trace cũ làm bằng chứng query đúng; không biến lỗi lịch sử này thành kết luận bản hiện hành còn hỏng. Không quy nguyên nhân vật lý, dữ liệu hay phương pháp M1 từ DOM.

**Đối chiếu P1–P4 của lượt 1:** P1 đúng ở thời điểm L3, đã bổ sung phần lớn bằng chứng L5 nhưng R1 còn hở. P2 đã có snapshot riêng; phân loại rỗng vẫn không là chứng minh nguyên nhân. P3 đã có message và audit nhóm khac, vẫn giữ giới hạn ví dụ/scope và span link chưa hỗ trợ; không cần đọc lại raw. P4 không có bằng chứng lỗi do dùng JS; nguồn hiện tại khớp hash trong biên nhận tái dựng, hai bản dựng đã lưu khớp cấu trúc với JSON hiện hành. L6 không gọi generator và không báo là đã tái dựng mới. Không điền REVIEW.md vì lượt này chỉ được điền REVIEW-2.

#### Phần còn mở, bằng chứng cần và đề xuất cho Minh

1. **R1:** thiếu bấm thật sau UI06 trên đường data link, vì lượt này bị giới hạn file cục bộ và không có Chrome/quyền máy. Đề xuất một lượt kiểm ngắn, dự kiến 30–45 phút nếu Chrome/Grafana hoạt động như L5; đây là ước lượng chưa kiểm, không hứa thời gian. Dùng ba ca đã có dữ liệu: P7/1ad3afeb, V032/e8661e0a và V041/eb48d6b3; phủ cả tải đọc/dev và đủ ba bản. Mẫu cụ thể (service đầu bảng, thao tác có cờ và cửa sổ) ở `#/proposed_R1_samples` của file kiểm L6. Bấm panel 4 → panel 22 → data link của node panel 23 ở mỗi ca (9 bấm); thêm một bấm panel 4 từ trang phát lại vì cùng dùng hai biến đã đổi. Panel 4 phải giữ bản/ca/cửa sổ và chọn đúng service; op có thể được query chọn lại khi đổi service. Panel 22/23 phải chọn đúng op. Lưu URL đích, DOM/ảnh, from/to ISO bằng biên nguồn, request của một panel sống tại đích có from/to hữu hạn và đúng biên; không chỉ thử URL trực tiếp hoặc ô chọn. Thêm kiểm Start time panel34 trên các trang này để tránh coi “có dữ liệu” là đúng cửa sổ. Không chạy lại M1, 66 trang, 162 link hay API toàn bộ. Mặt trái: đây vẫn là kiểm mẫu, không phủ mọi thao tác; đã có hồi quy dữ liệu/API để giữ phần không đổi. Chỉ API hoặc chấp nhận giới hạn không thay tiêu chí bấm thật; giữ trạng thái một phần là phương án nếu chưa cho chạy. Trước lượt nặng phải kiểm STOP/runner3/bộ nhớ tại thời điểm chạy theo brief L5; không suy máy hiện rảnh từ mốc 10:35Z cũ. Nếu phát hiện cần sửa dashboard, dừng phần sửa và trình đúng thay đổi; đề xuất này chỉ là kiểm.
2. **R2/N1:** dữ kiện lưu được đã cho biết URL và lỗi hiển thị lịch sử; chưa có request/response và trạng thái khung đúng thời điểm để phân xử numeric URL tạo tham số sai, khung dữ liệu cũ, tải/biến hoặc fallback. Đã phân tích 67 DOM, không có đối chứng panel sống ở trạng thái URL số. Chủ bằng chứng là hồ sơ L5; chạy mới không tái tạo request quá khứ. Đề xuất ghi các quan sát cùng ứng viên và giữ cơ chế lịch sử OPEN, không thêm thực nghiệm. Chi phí bổ sung bằng chứng hiện có đã thực hiện trong L6; việc ghi đính chính khoảng 10–15 phút, chưa kiểm. Quyết định phụ thuộc là cách diễn giải lỗi UI lịch sử, không phải chọn M1 hoặc nghiệm thu kết quả khoa học.
3. **R4:** Minh xác nhận cách hiểu quyền giao, rồi mới đề xuất ghi đúng lời Minh vào DECISIONS. Khuyến nghị giữ folder đã xóa, không hoàn tác; lợi ích là không sinh thêm thay đổi máy/UID chỉ để làm đẹp hồ sơ. Chưa có xác nhận thì giữ bất đồng về phạm vi quyền, không ghi vi phạm hay hợp thức hóa thành FACT. Đây là quyết định quy trình, không đổi hạng/cờ.
4. **G-c:** nguồn T-064 đang ghi “Chỉ mục thử”, V032 là đề xuất tạm, V041 là thay thế. Thiếu xác nhận bản đề xuất cuối, chỉ mục/hash và kiểm phần tích hợp chịu ảnh hưởng. Chủ đầu vào là Claude điều phối T-064; không tự nâng bản tạm hoặc yêu cầu Minh chọn thuật toán thay điều phối. Đề xuất tiếp nhận đúng bản cuối khi điều phối cấp, chỉ kiểm dữ liệu/luồng bị đổi; khối lượng/chi phí chưa thể chốt khi chưa biết bản và delta. Giữ G-c một phần. T-065 hỗ trợ DT18-NV3 ở phần minh họa, không xác nhận hiệu quả RCA hoặc đóng RQ5.

#### Impact map — đề xuất sửa gom theo file, CHƯA ĐƯỢC THỰC HIỆN

| File/phạm vi xin xử lý ở lượt sau | Thay đổi cụ thể và lý do | Ảnh hưởng |
|---|---|---|
| `results/T-065/kiem/003-trinh-duyet/BAO-CAO.md` | Nối đính chính: G-b còn R1 sau UI06; chỉ rõ file thô/file phân loại hiện hành; bổ sung đếm R2 và 67 DOM, N1 và phản chứng sau UI06; giữ loại (iii) và giới hạn cơ chế | Sửa phạm vi kết luận UI, không đổi số M1 hay xóa lịch sử |
| `results/T-065/BAN-GIAO-L5.md` | Nối đính chính G-b một phần vì data link chưa bấm lại; dẫn tới R2/R3/N1 và nguồn phân loại; bỏ khả năng hiểu “phần Chrome còn lại đã kiểm” là đủ mọi luồng chịu UI06 | Bàn giao khớp bằng chứng; không sửa nội dung reviewer |
| `results/T-065/kiem/004-dieu-huong-ui06/` (mới) | Chỉ ghi nhật ký bấm, đối chiếu, ảnh, báo cáo và manifest của 10 bấm nêu trên; không sửa dashboard hoặc nguồn phương pháp | Bổ sung đúng phần thiếu R1; giữ 003 và manifest L5 làm lịch sử |
| `results/T-065/thay-doi-may.md` | Chỉ thêm nguồn quyền/diễn giải theo quyết định R4 của Minh sau khi có, không đổi lệnh/giờ/receipt đã ghi | Làm rõ quyền, không phát lệnh máy |
| `docs/DECISIONS.md` | Chỉ ghi đúng quyết định mới của Minh về phạm vi xóa RCA rỗng; chưa có lời Minh nên chưa soạn thành quyết định đã duyệt | Nguồn sự thật phải có trước phần diễn giải phụ thuộc |
| `results/T-065/codex/manifest-L7.json` (mới), LOG T-065 và bảng phản hồi lượt liên quan nếu được cấp | Lưu trạng thái trước/sau và ngoại lệ của đính chính; nối kết quả kiểm/phản hồi | Không ghi đè manifest L5, không thay hash cũ để che lệch |

Báo cáo/bàn giao/thay-doi-may hiện đều bị ghim ở `manifest.json#/files`; mọi sửa trên ba file sẽ đổi hash của chúng và làm mốc L5 lệch nếu kiểm như trạng thái hiện hành. Phải giữ manifest/byte trước và dùng manifest mới cho lượt được duyệt, không chạy bộ chốt cũ để ghi đè mốc lịch sử. Không thấy cần đổi nguồn, ngưỡng, hạng, schema hay code phương pháp. Gói đề xuất trên có hơn ba file nên cần Minh duyệt đúng impact map theo Global Working Agreement; Luật 0 cũng chưa cho sửa báo cáo/code chỉ từ finding. Quyền L6 hiện tại chỉ đủ phản hồi/LOG/file phụ, nên chưa sửa các file đề xuất. Có thể chỉ duyệt R1 và đính chính R2/R3/N1 trước; R4 phụ thuộc cách Minh phân xử.

#### Báo cáo L6 trước kiểm chốt

1. **Đã làm:** tự soát gốc và ghi LOG trước khi đọc REVIEW/REVIEW-2; kiểm từng R1–R4; phân tích ngoại tuyến 67 lượt URL số; phát hiện N1 và xét bằng chứng sau sửa; điền đúng bảng REVIEW-2, để trống Minh quyết. Soạn đề xuất và prompt trung tính, không tự gửi agent.
2. **File thay đổi dự kiến chốt:** `tasks/T-065-giao-dien-grafana/REVIEW-2.md` chỉ các hàng phản hồi; LOG này chỉ nối; file phụ mới `results/T-065/codex/L6-dap-review2.json`. Không sửa STATE/docs/dashboard/máy chủ hoặc kết quả L5, không commit.
3. **Kiểm:** đầu lượt 6.257/6.257 hash L5 và 66/66 nguồn khớp, LOG khớp; 66 bản xuất khớp giá trị gốc; đếm mẫu UI khớp; kiểm diff UI06, 91 hành động, 67 DOM, 66 panel trace và 30 dòng sau UI06 như các mục trên. Giữ các lỗi công cụ: py/rg không có trong PATH sandbox; node.exe bị từ chối khởi chạy; lượt Node REPL hash toàn bộ timeout/reset nên dùng PowerShell để kiểm đủ; lần dựng trong bộ nhớ bị chặn code generation, không coi là tái dựng thành công; một phép đối chiếu đầu thiếu import util rồi đã chạy được. Không chạy script kiểm cũ vì một số script ghi đè biên nhận. Kiểm chốt toàn vẹn và bảo vệ phần reviewer sẽ nối ngay sau.
4. **Còn lại:** R1 chưa có bằng chứng bấm sau sửa; R4 còn cách hiểu quyền cần Minh quyết; cơ chế lịch sử R2/N1 OPEN có lý do và phần thiếu ở trên; G-c chờ đầu vào bản cuối. Không thêm/chuyển trạng thái quyết định nghiên cứu. Đề xuất tiếp tục lượt kiểm hẹp R1; chưa đề xuất dừng phản biện G-a/G-b khi điểm chặn chưa xử lý. Sau khi R1 đạt và phản hồi được kiểm, có thể đề nghị dừng lượt này; không tự nghiệm thu, đóng task hoặc RQ5.

Lệnh tính toán cuối trước mục này: Node REPL đối chiếu phần Trace của `ui06-inspector-04-V032-event-p31-dom.txt` với cửa sổ nguồn (10/10 dòng đúng), so hash đã ghim của các file đề xuất. Bước chốt chính xác: kiểm lại `manifest.json#/files` bằng PowerShell Get-FileHash; so tiền tố LOG với `#/task_log`; so tiền tố REVIEW-2 trước bảng phản hồi; kiểm năm hàng Minh quyết trống, prompt khớp mẫu và tập file. Bước sau bàn giao: Claude dùng prompt dưới để kiểm phản hồi/đề xuất trên file; chưa có quyền ghi review mới thì trả lời trong chat. Lượt Chrome R1 chỉ làm khi Minh cấp lại môi trường/quyền tương ứng.

Nội dung commit có thể trình riêng sau: `docs(t065): ghi phản hồi REVIEW-2 và bằng chứng ngoại tuyến L6`. L6 không commit hoặc push.


### Prompt bàn giao cho Claude — kiểm lại phản hồi và đề xuất L6

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, lượt đáp L6 cho đầu ra L5; tasks/T-065-giao-dien-grafana/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md (mục L6, gồm phản hồi và đề xuất theo file); results/T-065/codex/L5-brief.md; results/T-064/ban-xuat/chi-muc-ban.json; docs/DECISIONS.md.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md; results/T-065/BAN-GIAO-L5.md; tasks/T-065-giao-dien-grafana/REVIEW-2.md (bảng Phản hồi của người làm L6).
- Code và kết quả liên quan: results/T-065/codex/L6-dap-review2.json; results/T-065/manifest.json; BAN-GIAO-L5.md, CHECKPOINT.md, thay-doi-may.md, kiem/003-trinh-duyet/, grafana-l4/, grafana-l5/, l4-dashboard.mjs và các script l5-* trong results/T-065; môi trường lượt này là Codex CLI sandbox, chỉ kiểm file đã lưu.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc file cục bộ và trả lời trong chat; chưa có quyền ghi bản phản biện lượt mới; không truy cập Chrome, exp-obs hoặc exp-app.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

### L6 — kiểm chốt và kết lượt, 14/11/2026

1. Đã hoàn thành lượt đáp REVIEW-2 trong quyền: R1/R2/R3 đúng, R4 đúng một phần; thêm N1 về panel trace lịch sử sai cửa sổ. Đã soạn prompt chuẩn để Minh chuyển Claude, chưa tự gửi.
2. Tập file cuối đúng ba file: bảng cuối REVIEW-2, LOG chỉ nối và `results/T-065/codex/L6-dap-review2.json`. Không có sửa báo cáo/code/dashboard hoặc thao tác máy chủ. Không cập nhật STATE theo giới hạn của brief L6.
3. Kiểm chốt PowerShell hoàn tất 11:07:45Z: 6.257/6.257 file cũ khớp, không thiếu/lệch; tiền tố LOG 154.243 byte khớp task_log của manifest L5; 66/66 nguồn khớp. Kiểm diff theo byte: 29.694 byte của REVIEW-2 trước hàng R1 giữ nguyên; chỉ điền bốn hàng và thêm N1, năm ô Minh quyết trống. Prompt lấy nguyên khối chung/công đoạn/cổng hiện hành. Git diff --check không báo lỗi; ba file đang untracked nên phép kiểm byte/hash là căn cứ đầy đủ hơn git diff. Manifest L5 giữ nguyên; nối LOG làm hash toàn LOG đổi có chủ đích, mốc cũ được kiểm theo tiền tố và hash mới nằm trong file kiểm L6.
4. Chưa nghiệm thu G-b vì R1; R4 còn bất đồng về diễn giải quyền giao; cơ chế R2/N1 và G-c còn mở đúng phần thiếu đã nêu. Không đổi quyết định nghiên cứu. Đề xuất tiếp tục kiểm hẹp R1 khi Minh cấp Chrome/quyền tương ứng; gói sửa báo cáo và R4 trong impact map vẫn chỉ là đề xuất. Lượt đáp L6 đã xong, không coi đó là xong T-065/RQ5.

Lệnh tính toán đầy đủ cuối: PowerShell Get-FileHash trên `manifest.json#/files`, kiểm tiền tố LOG và chỉ mục 66 nguồn. Phép kiểm cuối sau khi ghi mục này: Node REPL đọc lại ba file, kiểm tiền tố/ô Minh quyết/prompt và đối chiếu hash LOG/REVIEW-2 trong file kiểm L6; không ghi kết quả cũ. Bước tiếp chính xác: Claude đọc SPEC, đầu ra gốc, LOG mục L6 và `codex/L6-dap-review2.json`, sau đó REVIEW-2; dùng “Prompt bàn giao cho Claude — kiểm lại phản hồi và đề xuất L6” ngay trên. Chưa có quyền ghi lượt phản biện mới thì trả lời trong chat. Không có job hoặc thao tác UI/máy đang chờ từ L6.


## L7 — 2026-11-14T11:58:33.214Z — Codex, laptop Minh, người làm — checkpoint

1. Đã bấm bốn đường liên kết UI06 trên ba mẫu. Đủ 12/12 luồng đã bấm; 11/12 có bằng chứng Inspector đạt. Lần bấm 19 từ panel 23 V041 đã tới đúng service, thao tác và cửa sổ. Minh yêu cầu lưu checkpoint trước khi đọc Inspector.
2. Ghi trong results/T-065/kiem/004-r1-ui06/, results/T-065/codex/L7-trang-thai.json, bản lưu manifest cũ, manifest hiện hành và mục LOG này. Giữ 003, dashboard, REVIEW-2 và STATE. Ổ D: từng báo ENOSPC. Tôi lưu bằng chứng tạm trong bộ nhớ rồi ghi khi ổ có chỗ, không xóa file để giải phóng dung lượng.
3. Ba đầu ra mẫu khớp SHA-256 của chỉ mục T-064. Hai dashboard trên exp-obs khớp bản UI06. Đã kiểm biên request và dữ liệu sống theo doi-chieu-dich.json. 72/72 Start time đọc được từ ba trang đích nằm trong cửa sổ. Panel 23 V032 hiện ID lúc tải, đối chứng panel 24 và đọc lại cùng URL hiện đúng payment_db. Không đề xuất sửa link từ hiện tượng này. Ngay trước panel 23 V041, Grafana dùng 431,6 MiB, dưới mức 600 MiB Minh cấp. Sau bấm dùng 424,5 MiB. RestartCount vẫn 0 và StartedAt giữ nguyên; hai số đo ở may.jsonl.
4. R1 còn mở đúng bằng chứng Query Inspector cho lần bấm 19. G-c chờ chỉ mục và hash bản M1-FT cuối của T-064. Lượt này kiểm giao diện minh họa DT18. Kết luận RQ5 còn phụ thuộc thực nghiệm FlashTicket.

Bước tiếp: đọc results/T-065/kiem/004-r1-ui06/checkpoint-v041-p23.json, giữ tab Chrome 217961091 tại View panel 31, đọc Query Inspector cho cùng đích. Dùng menu panel → Inspect → Data → Query → Refresh → Expand all. Đối chiếu query, UTC, mã trả về và điểm. Nối một dòng bằng chứng cho lần 19, cập nhật báo cáo/trạng thái, nối LOG và dựng lại manifest. Bảo toàn giới hạn tải đã ghi. Prompt dưới đây để Minh chuyển Claude sau khi chốt dữ liệu hoặc khi muốn kiểm checkpoint.

Lệnh chốt: Node.js chạy từ PowerShell stdin để đối chiếu tập file và SHA-256 với codex/manifest-L7-truoc.json, dựng và kiểm manifest hiện hành, kiểm tiền tố LOG; git diff --check. Nội dung commit nếu Minh duyệt riêng: docs(t065): lưu kiểm liên kết R1 sau UI06.

### Prompt cho Claude — kiểm lại phản hồi và sửa L7

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, L7, tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L7-brief.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, tasks/T-065-giao-dien-grafana/LOG.md, results/T-065/codex/L7-brief.md, results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, tasks/T-065-giao-dien-grafana/REVIEW-2.md, results/T-065/codex/L6-dap-review2.json và mục L6 trong LOG.
- Code và kết quả liên quan: results/T-065/grafana-l5/ui06/, results/T-065/kiem/004-r1-ui06/, results/T-065/manifest.json và mục L7 trong LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi tasks/T-065-giao-dien-grafana/REVIEW-3.md.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## L7 tiếp nhận — 2026-11-14T12:12:25.1316013Z — Codex, laptop Minh, người làm

Tiếp nhận checkpoint L7 theo chỉ thị Minh ngày 14/11/2026. Minh xác nhận Chrome giữ nguyên. Chỉ ghi results/T-065/ và nối LOG; giữ vai trò Codex làm, Claude phản biện. Đã kiểm 6.301 checksum và LOG khớp manifest tiếp nhận; giữ bản manifest trước tại codex/manifest-L7-tiep-nhan-truoc.json. Hai STOP chưa bật. Tab 217961091 đúng View panel 31, booking-service, OrderExpiryWorker.expireDueOrders và cửa sổ checkpoint. Chỉ thu tiếp Inspector của lần bấm 19, không bấm graph thêm; giờ bấm cũ tiếp tục null. Không chạy lại phần đã đạt. Phạm vi tác động: thêm request/response/ảnh và kiểm toàn vẹn trong kiem/004-r1-ui06/, cập nhật đối chiếu, báo cáo và trạng thái L7, dựng manifest hiện hành, nối LOG và prompt. Quyền này đã được Minh cấp trong yêu cầu tiếp nhận.


### L7 tiếp nhận — kết lượt 14/11/2026

1. Đã hoàn thành phần Inspector còn thiếu của lần bấm 19 trên đúng tab hiện có, không bấm lại panel 23. Đối chiếu đủ 12/12 luồng mẫu: đúng service/operation/cửa sổ và panel sống có dữ liệu. Lần 19: request from 22:18:33.000Z đến 22:28:32.999Z ngày 11/11, nguồn phương pháp nửa mở kết thúc 22:28:33.000Z; mã 200, hai chuỗi × 41 điểm. Cây DOM, bản trích xuất đủ mảng số và hai ảnh mới nằm trong kiem/004-r1-ui06/. Giờ bấm cũ giữ null; nối dòng 20 lỗi thu và dòng 21 bằng chứng qua doi_chieu_lan_bam=19.
2. File đã đổi trong results/T-065/: BAO-CAO.md, doi-chieu-dich.json, nối nhat-ky-bam.jsonl và may.jsonl, trạng thái L7; thêm bằng chứng, script chốt, biên bản tiếp nhận/toàn vẹn và bản lưu manifest trước phiên; dựng manifest hiện hành. LOG chỉ nối mục này. Giữ nguyên REVIEW-2, SPEC, docs/STATE và các hồ sơ docs; không sửa dashboard/provisioning/dữ liệu hay file máy chủ, không commit/push. Tập file chính xác sẽ ở kiem/004-r1-ui06/kiem-cuoi-tiep-nhan.json và manifest.json.
3. Manifest tiếp nhận 6.301/6.301 checksum khớp; giữ 6.257 mục cũ so manifest trước L7. Nguồn T-064 lần 19 khớp hash chỉ mục; đơn vị ns và biên N/A đã đối chiếu. Lỗi Unexpected error đầu phiên đi cùng tunnel local đã mất (không listener 13000, PID cũ không còn). Giữ cây lỗi và biên bản; khôi phục tunnel theo brief rồi Refresh cùng Inspector trả dữ liệu. Không có Docker restart/OOM từ checkpoint, StartedAt giữ nguyên; số đo sau Inspector 377,1 MiB/768 MiB lúc 12:19:14Z. Hai STOP chưa bật; không can thiệp lô M1 đang chạy. API ảnh timeout khi tab chưa ở trước; đã đưa đúng tab Grafana ra trước bằng phím Ctrl+3 rồi thu hai ảnh, không phát truy vấn mới. Script chốt lần đầu dừng do window nguồn là object ns, chưa ghi đầu ra; đã đọc đúng schema và kiểm biên ns trước lần chốt thành công. Các lỗi thu giữ trong hồ sơ, không dùng làm kết quả khoa học.
4. R1 đã đủ bằng chứng mẫu theo phạm vi được Minh duyệt; đề nghị Claude kiểm lại, Minh quyết chấp nhận. Không tự nghiệm thu G-b hay đóng T-065. Không phát hiện lỗi liên kết trong mẫu nên không đề xuất sửa dashboard. G-c còn OPEN vì chưa có bản M1-FT đề xuất cuối và chỉ mục/hash bàn giao từ T-064; tiếp nhận nguồn ấy rồi kiểm phần G-c theo SPEC/quyền tương ứng. L7 chỉ trả lời luồng hiển thị sau UI06, không trả lời xong RQ5. Các bất đồng/đề xuất còn lại của L6 giữ nguyên để kiểm lại, không sửa ngoài R1. Không thêm hay đổi quyết định nghiên cứu.

Bước tiếp chính xác: Claude đọc AGENTS.md, SPEC và nguồn gốc được nêu trong prompt; kiểm checksum bằng `py -3 -X utf8 results/T-065/codex/l7-tiep-nhan-chot.py verify`; tự soát đầu ra gốc rồi đọc phản hồi L6/L7 và REVIEW-2. Dùng prompt dưới đây; REVIEW-3 chỉ ghi khi Minh cấp quyền. T-065 tiếp phần G-c sau khi T-064 bàn giao bản đề xuất cuối. Không có thao tác Chrome hay job kiểm còn dở. Tab 217961091 ở Query Inspector cùng đích; tunnel mới PID 43220, exec session 46123, 127.0.0.1:13000 → exp-obs 10.0.0.215:3000. Trước dùng tiếp, kiểm listener/PID và hai STOP; không tự dừng tunnel khác.

Lệnh cuối trước ghi mục này: `py -3 results/T-065/codex/l7-tiep-nhan-chot.py evidence` (thành công sau khi kiểm schema ns), sau đó SSH chỉ đọc đo máy/Docker events và kiểm chỉ mục đối chiếu. Lệnh chốt cuối của lượt: `py -3 -X utf8 results/T-065/codex/l7-tiep-nhan-chot.py seal`, rồi `py -3 -X utf8 results/T-065/codex/l7-tiep-nhan-chot.py verify` và `git diff --check`; kết quả máy đọc ở kiem-cuoi-tiep-nhan.json/manifest. Nội dung commit đề xuất nếu Minh duyệt riêng: `docs(t065): hoàn tất bằng chứng R1 sau UI06`.

### Prompt cho Claude — kiểm lại phản hồi L6 và L7 đã chốt

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065; tasks/T-065-giao-dien-grafana/SPEC.md; results/T-065/codex/L7-brief.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, tasks/T-065-giao-dien-grafana/LOG.md, results/T-065/codex/L7-brief.md, results/T-064/ban-xuat/chi-muc-ban.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, tasks/T-065-giao-dien-grafana/REVIEW-2.md, results/T-065/codex/L6-dap-review2.json, mục L6 và L7 trong LOG T-065.
- Code và kết quả liên quan: results/T-065/grafana-l5/ui06/, results/T-065/kiem/004-r1-ui06/, results/T-065/codex/L7-trang-thai.json, results/T-065/manifest.json, results/T-065/codex/manifest-L7-truoc.json, results/T-065/codex/manifest-L7-tiep-nhan-truoc.json.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi tasks/T-065-giao-dien-grafana/REVIEW-3.md; khi được Minh cấp thì chỉ ghi đúng bản lượt mới ấy.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## L8 — 2026-11-14T16:40:37.0199601Z — Codex CLI, laptop Minh, người làm — mở kiểm G-c cuối

Phân loại EXECUTE. Tiếp nhận brief L8 do Minh giao, quyền SPEC bổ sung và DECISIONS điều phối chiến dịch. Codex làm, Claude phản biện. Phạm vi tác động đã giao: results/T-065/ (nguồn chụp, bộ xuất/dashboard mới, kiểm 005, checkpoint/XONG/manifest/thay-doi-may/prompt) và chỉ nối LOG này; exp-obs chỉ thư mục kết quả mới t065-l8-001 và file dashboard mới, restart riêng Grafana nếu cần. Giữ bản G-c thử, không sửa STATE/docs/SPEC/REVIEW/T-064/src. Đã kiểm 6311 mục manifest, LOG và 83 đầu ra nguồn khớp. Chỉ mục bản 2 có ba bản × 28 ca; một slot P7 lỗi chạy không dựng hạng. Chưa thêm/đổi quyết định nghiên cứu.

Dùng lại dữ liệu L4 đã băm cho 22 ca; chỉ dựng thêm sáu ca dev3 trên exp-obs từ nguồn hiện có, không chạy M1 hay chấm. Các lệnh xử lý/API chia thành bước ngắn, dự kiến mỗi lượt dưới một giờ. Nếu công việc kéo dài: lỗi ở 10% giữ nguyên nguồn/hồ sơ tiếp nhận, chỉ chạy lại bước xuất lỗi (vài phút); ở 50% giữ từng ca xuất đã xong, chỉ bổ sung ca lỗi và slot phụ thuộc (vài phút); ở 99% giữ dashboard/dữ liệu đã kiểm, chỉ tiếp slot API hoặc hồ sơ còn thiếu (vài phút), không chạy lại M1/raw toàn bộ. Lỗi nguồn/hash chặn phần phụ thuộc; giữ mọi lượt hỏng. STOP local/remote kiểm trước mỗi bước. Không có lượt tính toán hơn một giờ được phát.


### L8 — kết lượt 2026-11-14T16:53:19.615Z — dừng tại mâu thuẫn nguồn

1. Đã kiểm tiếp nhận: 6.311 checksum manifest cũ và LOG khớp; 83 đầu ra nguồn khớp SHA byte; chỉ mục bản 2 đúng ba bản × 28 ca. Chuẩn bị nguồn chụp/bản nháp bộ xuất, nhưng guard metadata dừng trước ghi dữ liệu/dashboard. Tự đọc code và tính lại cho thấy trường cấu hình của chỉ mục V082 là hash byte file, còn 28 đầu ra là hash JSON chuẩn hóa theo src/m1_ft/chay.py. Đây là FACT về quy ước băm; chưa có bằng chứng sai cấu hình chạy hoặc sai hạng. Chi tiết từng ca/con trỏ/hash nằm trong kiem/005-gc-cuoi/chan-hash-cau-hinh.json.
2. File đổi: results/T-065/ (nguồn chụp nguon-l8, bản nháp codex/l8-xuat.py, script tiếp nhận/chốt l8-local.ps1, payload/lượt lỗi, kiểm 005, XONG/checkpoint/thay-doi-may/manifest/prompt và bản lưu trước) và chỉ nối LOG này. Không sửa nguồn T-064, src, docs, STATE, SPEC hoặc REVIEW; không commit/push. Tập file cụ thể do kiem/005-gc-cuoi/kiem-cuoi.json và manifest chốt liệt kê. Trên exp-obs chỉ tạo thư mục mới t065-l8-001 và đặt nguồn/script/inventory; chưa tạo provisioning/dashboard mới, không restart.
3. Kiểm chạy: nguồn và manifest tiếp nhận như mục 1; cấu hình chuẩn hóa tính lại khớp metadata của cả 28 đầu ra V082; V071 không lệch hai trường metadata với chỉ mục. 3.019 file có trước trên máy giữ hash, StartedAt Grafana không đổi; hai STOP chưa bật khi kiểm máy. Xác nhận đủ nguồn trace/log/metric sáu ca dev3 nhưng chưa xử lý raw/liên kết. Bản nháp Python chỉ được kiểm cú pháp/guard, chưa kiểm chức năng xuất/dashboard/API. L8 chưa kiểm Chrome. Lượt export hỏng và lỗi môi trường được giữ; không tính là kết quả khoa học. Bản trước XONG/prompt giữ byte; CHECKPOINT/thay-doi-may chỉ nối.
4. G-c chưa đạt. Chặn việc xuất/hiển thị hash và kiểm dashboard cuối cho tới khi T-064 thống nhất quy ước. Đề xuất Claude điều phối sửa trường cau_hinh_sha256 của chỉ mục/hồ sơ theo sha_cau_hinh đã dùng trong kết quả, giữ hash byte file trong trường có tên riêng nếu cần; không sửa method-output hay chạy lại M1 vì chưa thấy nội dung cấu hình khác nhau. Phương án khác: Minh cho T-065 hiển thị hai loại hash bằng nhãn phân biệt sau khi hợp đồng nói rõ; mặt trái là tiếp tục hai quy ước. Đã hỏi Minh trong chat, chưa nhận trả lời khi chốt; không tự chọn. L6/L7 vẫn chờ Claude kiểm lại; giữ các phản hồi/bất đồng cũ. Task một phần, không nghiệm thu và không trả lời xong RQ5. Không thêm/đổi quyết định nghiên cứu.

Bước tiếp chính xác: đọc báo cáo kiem/005-gc-cuoi/BAO-CAO.md và nguồn T-064 được điều phối bàn giao lại; xác nhận ý nghĩa hash và hash chỉ mục mới, giữ bản chụp lỗi cũ. Sau khi nguồn thống nhất mới sửa bộ xuất nháp trong quyền, kiểm dữ liệu/API theo brief L8, rồi liệt kê phần Chrome cần app. Không chạy lại init hoặc M1. L8 không còn job nền, tab hay tunnel mới.

Lệnh cuối trước mục này: SSH chỉ đọc gọi inventory() của script L8, so may-truoc với may-sau-chan (3.019 file cũ không đổi), rồi kiểm độc lập canonical hash tại Node REPL và kiểm bản lưu/prefix. Lệnh chốt sau mục này: `& ./results/T-065/codex/l8-local.ps1 -Action seal`, rồi `-Action verify` và `git diff --check`; kết quả ghi kiem-cuoi.json/manifest. Nội dung commit đề xuất nếu Minh duyệt riêng: `docs(t065): lưu checkpoint G-c cuối và mâu thuẫn hash cấu hình V082`. Chưa commit/push.

### Prompt cho Claude — kiểm lại L6, L7 và L8

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065; tasks/T-065-giao-dien-grafana/SPEC.md; lượt L8 theo brief kiểm G-c cuối do Minh giao.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: AGENTS.md; tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md; results/T-064/hop-dong-dau-ra.md; results/T-064/ban-xuat/chi-muc-ban.json; results/T-064/cau-hinh-de-xuat.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, REVIEW-2.md; results/T-065/codex/L6-dap-review2.json; các mục L6, L7 và L8 trong LOG T-065.
- Code và kết quả liên quan: results/T-065/grafana-l5/ui06/; results/T-065/kiem/004-r1-ui06/; results/T-065/kiem/005-gc-cuoi/; results/T-065/codex/l8-local.ps1; results/T-065/codex/l8-xuat.py; results/T-065/nguon-l8/; results/T-065/manifest.json; results/T-065/codex/manifest-L8-truoc.json; kết quả kiểm checksum bằng PowerShell: & ./results/T-065/codex/l8-local.ps1 -Action verify.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ trả lời trong chat nếu chưa được Minh hoặc điều phối theo quyền chiến dịch cấp quyền ghi bản phản biện mới. Khi có quyền, liệt kê thư mục task để chọn đúng bản lượt mới; không sửa REVIEW cũ, LOG, STATE hoặc nguồn T-064 trong vai trò phản biện T-065.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## L8b — 2026-11-14T17:01:24.249Z — Codex CLI, laptop Minh, người làm — tiếp sau đính chính nguồn

Phân loại EXECUTE. Minh giao tiếp brief L8 sau khi điều phối sửa nguồn T-064. Đã đọc chỉ mục/bộ dựng/hồ sơ cấu hình/sổ đính chính và tự kiểm 83 đầu ra đúng SHA, 56/56 metadata M1-FT khớp chỉ mục mới; hash cấu hình chuẩn hóa và hash byte file đúng quy ước. Đường dẫn/SHA đầu ra không đổi so L8; không có lượt chạy lại M1. Giữ hồ sơ L8 làm lịch sử. Phạm vi tác động được giao: chỉ results/T-065/ và nối LOG này; trên exp-obs thư mục mới t065-l8b-001 và hai file dashboard UID t065-l8b-rca/t065-l8b-phat-lai. Giữ dữ liệu/dashboard G-c thử và mọi file máy có trước. Không sửa STATE/docs/SPEC/REVIEW/src/T-064.

Dùng lại 22 ca và template đã băm; chỉ dựng lớp bằng chứng sáu ca dev3 từ nguồn hiện có tại exp-obs, không tải raw về laptop. Mỗi lệnh xuất/API dự kiến dưới một giờ, lưu ca/slot độc lập. Lỗi ở 10%: giữ nguồn và ca đã xuất, sửa bước xuất lỗi, tiếp ca thiếu (vài phút); 50%: giữ ca/slot xong và snapshot đã kiểm, chỉ tiếp ca lỗi/phụ thuộc (vài phút); 99%: giữ dữ liệu/dashboard đạt, chỉ tiếp slot API hoặc hồ sơ còn thiếu (vài phút), không chạy lại M1/raw toàn bộ. Lỗi nguồn/hash dừng phần phụ thuộc; giữ lượt hỏng. Kiểm STOP local/remote trước từng bước. Phần đọc raw/Infinity chạy trên exp-obs để giảm chuyển dữ liệu; laptop nhận/chấm đối chiếu và chốt hồ sơ.

- L8b bước 2 2026-11-14T17:11:30.799Z: xuất và kiểm đủ 84 slot, schema 84/84, 48.927 URL; hồi quy 9 ca P7 T-062 đạt. Dữ kiện chi tiết tại kiem/006-gc-cuoi/kiem-xuat.json. Tiếp deploy UID mới và API; giữ mọi hồ sơ L8.

- L8b bước 3 2026-11-14T17:28:12.403Z: API đủ 18 trang đạt, 33 mẫu liên kết có dữ liệu từ 12 request mới; 20 live query có 15 dữ liệu/5 rỗng/0 lỗi. Giữ lỗi biến service và sửa projection; kiểm lại 84 slot đạt. Nhận/kiểm 2.477 file, không nhận raw; 3.019 file máy có trước và 91 file L8 giữ hash, không restart. Tiếp chốt hồ sơ; UI mới chưa kiểm.


### L8b — kết lượt 2026-11-14T17:33:34.406Z — G-c bản cuối đạt dữ liệu/API, UI mới chưa kiểm

1. Đã tích hợp chỉ mục bản 2 đã sửa vào ba bản × 28 ca, hai UID t065-l8b-rca/t065-l8b-phat-lai. Trang ca có trạng thái bản/chạy, hash cấu hình chuẩn hóa, hash byte file cấu hình, mã nguồn/đầu ra, cửa sổ. Hạng/cờ/cạnh lấy nguyên nguồn; V082 hiện không có đầu ra cạnh. P7/ebd5ef38 hiện lỗi chạy/đường dẫn lỗi, bảng kết quả rỗng. Sáu ca dev3 có liên kết trace/log/metric từ nguồn đã băm; log là ngữ cảnh service, span link vẫn chưa hỗ trợ. Không chạy/chấm M1; không có quyết định nghiên cứu mới.
2. File đổi: chỉ results/T-065 (nguon-l8b, may-l8b, grafana-l8b, schema0.5, mã/script/bản nhận L8b, kiểm006, README/XONG/checkpoint/thay-doi-may/manifest/prompt và các bản lưu trước) và chỉ nối LOG này. Manifest giữ trước tại codex/manifest-L8b-truoc.json; tập file cuối nằm kiem/006-gc-cuoi/kiem-cuoi.json. Trên exp-obs chỉ thư mục t065-l8b-001 và hai file provisioning mới; giữ các bản thử và hồ sơ chặn L8. Không ghi STATE/docs/SPEC/REVIEW/src/T-064, không commit/push.
3. Kiểm: 83 SHA đầu ra và 56 metadata M1-FT khớp nguồn mới. Đủ 84 slot, schema84; 1.410 dòng thực thể, 1.652 cờ, 26.266 đơn vị, 600 cạnh xếp hạng, 19.971 dòng thao tác theo slot; ns nguyên và thứ tự/tie/source giữ đúng. 48.927 URL đúng một lần; 9 ca P7 T-062 hồi quy đạt. API18 trang/315target-biến đạt. Liên kết33mẫu có dữ liệu từ12request mới; request trùng dùng lại có giờ gốc. Snapshot20query:15 dữ liệu/5rỗng/0lỗi; panel28 khớp. Gói nhận21.195.332byte nén, SHA hai đầu và2.477file khớp, không tải raw. 3.019file máy trước và91file L8 giữ hash; Grafana tự nạp, không restart. Toàn bộ số/con trỏ tại kiem/006-gc-cuoi/tom-tat.json và báo cáo. Rà JSON dashboard:74/44 thay đổi tương ứng chính/phát lại; bố cục chỉ tăng6h metadata và dịch phần sau, target sống giữ nguyên (dashboard-diff.json).
4. G-c đạt phần dữ liệu/API, UI mới chưa kiểm bấm/ảnh trong lượt CLI. Bước app cụ thể ở codex/L8b-app-brief.md và chín URL ISO trong kiem/006-gc-cuoi/mau-UI-con-lai.json. Đề xuất kiểm UI mới rồi Minh quyết nghiệm thu; Claude kiểm lại phần L6/L7/L8/L8b theo prompt gộp. L6/L7 còn chờ kiểm lại; không tự kết luận các bất đồng cũ đã đóng. T-065 còn một phần, RQ5 cần bằng chứng nghiên cứu T-064/P10; giao diện trả lời được phần truy vết/hiển thị đầu ra cuối. Với query rỗng, chưa phân xử không phát sinh chuỗi/nhãn-query khác/retention; cần dữ liệu cùng giờ để quy nguyên nhân. Không suy collector hỏng từ raw có hoặc query rỗng.

Lỗi giữ trong hồ sơ: Node REPL đầu kiểm nguồn lỗi cú pháp trước tác động; SCP pin vào thư mục kiểm mới do root sở hữu bị chặn, đã dùng thư mục gốc mới; API lượt1 bắt biến service trả mảng một phần tử. Đã sửa bằng projection object ma/ten, giữ request/response và backup hai dashboard trước sửa, không dựng lại raw/M1. API lượt2 và kiểm84slot sau sửa đạt. Các lỗi này không là kết quả khoa học.

Bước tiếp chính xác: Claude đọc README-L8b.md, báo cáo kiểm006 và nguồn, kiểm hash bằng & ./results/T-065/codex/l8b-local.ps1 -Action verify; tự soát rồi đọc REVIEW-2/phản hồi L6 và bằng chứng L7/L8/L8b. Phần app dùng URL ISO/brief, kiểm STOP/listener trước; không chạy lại M1/raw/API đã đạt khi nguồn/targets giữ nguyên. Không có tab/tunnel hay tiến trình kiểm mới còn dở; các lô M1 là của điều phối, L8b không can thiệp.

Lệnh cuối trước chốt: SSH l8b-dong-goi.py (kiểm máy/tạo gói), SCP/tar nhận và kiểm2.477file; tiếp Node kiểm diff dashboard và mẫu prompt, git diff --check (đạt). Lệnh chốt sau mục này: & ./results/T-065/codex/l8b-local.ps1 -Action seal rồi -Action verify. Nội dung commit đề xuất nếu Minh duyệt riêng: feat(t065): tích hợp G-c bản V082 cuối và giữ lịch sử. Chưa commit/push.

### Prompt cho Claude — kiểm lại L6, L7, L8 và L8b

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065; tasks/T-065-giao-dien-grafana/SPEC.md; results/T-065/codex/L8-brief.md và L8b-brief.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: AGENTS.md; tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md; results/T-064/hop-dong-dau-ra.md; results/T-064/ban-xuat/chi-muc-ban.json; results/T-064/cau-hinh-de-xuat.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, REVIEW-2.md; results/T-065/codex/L6-dap-review2.json; các mục L6, L7, L8, L8b trong LOG T-065.
- Code và kết quả liên quan: results/T-065/grafana-l5/ui06/; kiem/004-r1-ui06/; kiem/005-gc-cuoi/; kiem/006-gc-cuoi/; grafana-l8b/; may-l8b/; dinh-dang/0.5/; nguon-l8b/; codex/l8b-xuat.py, l8b-kiem.py, l8b-dong-goi.py, l8b-local.ps1; README-L8b.md; manifest.json; codex/manifest-L8b-truoc.json; các đường dẫn tương đối trong mục này thuộc results/T-065. Lệnh kiểm checksum: & ./results/T-065/codex/l8b-local.ps1 -Action verify.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ trả lời trong chat nếu chưa được Minh hoặc điều phối theo quyền chiến dịch cấp quyền ghi bản phản biện mới. Khi có quyền, liệt kê thư mục task để chọn đúng bản lượt mới; không sửa REVIEW cũ, LOG, STATE hoặc nguồn T-064 trong vai trò phản biện T-065.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


### L8b — 2026-11-14T17:39:45.360Z — bổ sung chốt tệp điều phối

Seal lần đầu dừng trước ghi manifest: codex/L8-trang-thai.json đã được bộ gọi đổi sang trạng thái tiến trình lúc16:55:52Z, trước L8b. Tên trạng thái kết quả bị trùng tên tệp của bộ gọi. Đã tái dựng bản kết quả cũ và kiểm SHA/byte đúng pin trước, lưu codex/L8-ket-qua-lich-su.json; kết quả L8b lưu codex/L8b-ket-qua.json. Giữ nguyên tệp điều phối hiện có trong bước xử lý, không ghim tên trang-thai do bộ gọi quản lý. Biên bản kiem/006-gc-cuoi/doi-chieu-tep-dieu-phoi.json. Không ảnh hưởng dữ liệu/dashboard/số; không có quyết định nghiên cứu mới. Các kết quả/bước UI còn thiếu và prompt gộp ở mục ngay trước giữ hiệu lực. Lệnh cuối: đọc trạng thái/mtime và đối chiếu nội dung lịch sử với hash; tiếp l8b-local.ps1 seal/verify.

### Prompt cho Claude — bản gộp sau chốt tệp điều phối

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065; tasks/T-065-giao-dien-grafana/SPEC.md; results/T-065/codex/L8-brief.md và L8b-brief.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: AGENTS.md; tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md; results/T-064/hop-dong-dau-ra.md; results/T-064/ban-xuat/chi-muc-ban.json; results/T-064/cau-hinh-de-xuat.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, REVIEW-2.md; results/T-065/codex/L6-dap-review2.json; các mục L6, L7, L8, L8b trong LOG T-065.
- Code và kết quả liên quan: results/T-065/grafana-l5/ui06/; kiem/004-r1-ui06/; kiem/005-gc-cuoi/; kiem/006-gc-cuoi/; grafana-l8b/; may-l8b/; dinh-dang/0.5/; nguon-l8b/; codex/l8b-xuat.py, l8b-kiem.py, l8b-dong-goi.py, l8b-local.ps1; README-L8b.md; manifest.json; codex/manifest-L8b-truoc.json; các đường dẫn tương đối trong mục này thuộc results/T-065. Lệnh kiểm checksum: & ./results/T-065/codex/l8b-local.ps1 -Action verify.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ trả lời trong chat nếu chưa được Minh hoặc điều phối theo quyền chiến dịch cấp quyền ghi bản phản biện mới. Khi có quyền, liệt kê thư mục task để chọn đúng bản lượt mới; không sửa REVIEW cũ, LOG, STATE hoặc nguồn T-064 trong vai trò phản biện T-065.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## L8c — 2026-11-14T22:53:09Z — Codex, người làm, Windows/Chrome

1. Đã kiểm hai UID G-c bản cuối trong tab riêng. Đổi bản, chọn ca/service/thao tác thật, đến ba kho quan sát và kiểm lớp phát lại. Lưu checkpoint mỗi tổ hợp. G-c đạt các phép kiểm trên mẫu L8c.
2. Ghi `results/T-065/kiem/007-gc-chrome/`, nối `CHECKPOINT.md` và mục LOG này, cập nhật `XONG.md`, `prompt-ban-giao.md` và `manifest.json`. Giữ manifest, XONG và prompt trước lượt trong `results/T-065/codex/`. Tập tệp chính xác ở manifest.
3. Mốc L8b đạt 9.022 checksum và LOG, 10 pin nguồn mẫu và 2 hash dashboard khớp. Tại Chrome: 18/18 trang khớp bản/ca/window và trạng thái, 9/9 bảng mẫu khớp các dòng đã dựng, 9/9 đích Explore khớp datasource/query/window và HTTP 200. Lưu 29 ảnh, gồm ảnh đích của cả ba kho mỗi ca. Nguồn số và kết quả theo từng đối tượng ở `results/T-065/kiem/007-gc-chrome/doi-chieu.json` và `BAO-CAO.md`. STOP vắng tại các lần kiểm ranh giới. Không chạy lại M1/raw/bộ API L8b. Không mở test.
4. DOM có thể giữ metadata cũ khi panel phát lại ngoài khung, hàng hiện đúng sau khi đưa vào khung trong phép tái hiện. Loki T-062 rỗng tại giờ kiểm, nguyên nhân OPEN. Bước tiếp là Claude đọc và kiểm độc lập L6–L8c, sau đó Minh quyết nghiệm thu. RQ5/P10 và lựa chọn thiết kế tiếp tục theo nguồn nghiên cứu. Không thêm quyết định cần ghi DECISIONS. Nội dung commit đề xuất khi Minh yêu cầu: “Lưu kiểm Chrome G-c T-065”. Chưa commit hoặc push.

Lệnh kiểm nguồn cuối là SSH chỉ đọc STOP và SHA hai file `t065-l8b-*.json` trên exp-obs. Listener còn ở 127.0.0.1:13000, PID 25432. Tiếp theo chạy `& ./results/T-065/codex/l8b-local.ps1 -Action verify`, đọc `results/T-065/kiem/007-gc-chrome/doi-chieu.json` và dùng prompt dưới.

### Prompt cho Claude

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065; tasks/T-065-giao-dien-grafana/SPEC.md; results/T-065/codex/L8-brief.md, L8b-brief.md và L8b-app-brief.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: AGENTS.md; tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md; results/T-064/hop-dong-dau-ra.md, ban-xuat/chi-muc-ban.json và cau-hinh-de-xuat.json.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md và REVIEW-2.md; results/T-065/codex/L6-dap-review2.json; các mục L6, L7, L8, L8b và L8c trong LOG T-065.
- Code và kết quả liên quan: results/T-065/grafana-l5/ui06/, kiem/004-r1-ui06/, kiem/005-gc-cuoi/, kiem/006-gc-cuoi/, kiem/007-gc-chrome/, grafana-l8b/, may-l8b/, dinh-dang/0.5/, nguon-l8b/, codex/l8b-xuat.py, codex/l8b-kiem.py, codex/l8b-dong-goi.py, codex/l8b-local.ps1, README-L8b.md, XONG.md, manifest.json và codex/manifest-L8c-truoc.json; các đường dẫn rút gọn trong mục này thuộc results/T-065. Lệnh kiểm checksum là & ./results/T-065/codex/l8b-local.ps1 -Action verify.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ trả lời trong chat nếu chưa được Minh cấp quyền ghi bản phản biện mới. Khi được cấp quyền, ghi đúng bản lượt mới do Minh cho phép.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.


## L9 — 2026-11-15 — Codex, Windows laptop Minh, người làm — đáp REVIEW-3

### Mở lượt và quyền

- Phân loại EXECUTE: đáp phản biện; không đổi vai. Minh cấp đúng bảng “Phản hồi của người làm” cuối REVIEW-3 và một mục LOG mới trong brief L9 ngày 15/11/2026. Không có quyền sửa đầu ra/dashboard/mục lục/folder, STATE, SPEC, docs hoặc manifest; không commit/push.
- Đã đọc AGENTS, STATE, toàn SPEC và mục L8c cuối LOG; nguồn trực tiếp DT18/cô, MRP (mục tiêu, RQ5/P9/P10), LESSONS, quyết định chiến dịch/folder/bản cuối và WHY liên quan. STATE vẫn là mốc cũ; lượt này theo brief mới, không suy STATE là nghiệm thu hay tự cập nhật ngoài quyền. Không mở dữ liệu khóa hoặc thực nghiệm mới.
- Trước ghi, lệnh `& ([ScriptBlock]::Create((Get-Content -Raw -Encoding UTF8 results/T-065/codex/l8b-local.ps1))) -Action verify` đạt: `VERIFIED: 9175 checksums and task LOG; status=dat_g_c_chrome_mau_L8c`. LOG trước lượt đúng 284.157 byte theo `results/T-065/manifest.json#/task_log`. REVIEW-3 không bị ghim trong manifest này. Nối LOG làm đổi hash toàn file có chủ ý trong quyền; giữ manifest cũ và kiểm tiền tố LOG, không sửa pin lịch sử.
- Đọc nguồn/đầu ra gốc trước. Chưa mở kết luận REVIEW, REVIEW-2, REVIEW-3. Nhận xét tự soát sẽ ghi tiếp trong chính mục L9 trước khi mở các kết luận đó.

### Tự soát độc lập — ghi TRƯỚC khi mở kết luận các bản phản biện

- **FACT — đầu ra và truy vết:** đọc đường xuất/kiểm L8b, hợp đồng T-064, chỉ mục bản cuối, cấu hình đề xuất và hồ sơ chọn (phần bản cuối/giới hạn). Đối chiếu độc lập bằng Node REPL, chỉ đọc: kiểm SHA byte nguồn hiện tại và snapshot cho 83 đầu ra; 84 slot gồm một slot P7 lỗi chạy. Giữ số nguyên vượt giới hạn Number bằng reviver `context.source` → BigInt, nên đối chiếu biên ns không bị làm tròn. Cả 84 slot khớp hạng/thứ tự/tie_group, cờ, đơn vị, vùng, cạnh, metadata và phép chiếu thao tác đã kiểm; 0 sai khác trong các phép đối chiếu này. Tổng đếm lại khớp `results/T-065/may-l8b/kiem/kiem-xuat.json#/cases`, `/totals`, `/urls_decoded_once`: 1.410 dòng thực thể; 1.652 cờ; 26.266 đơn vị; 600 cạnh; 19.971 thao tác; 48.927 URL. URL đã đối chiếu datasource, query sau giải mã một lần và cửa sổ bao gồm kết thúc tại cận trên −1 ms. Không thấy khóa đáp án bị cấm trong 84 bản chính. V082 không có đầu ra cạnh; không tự suy cạnh/xếp lại. P7/ebd5ef38 có LOI_CHAY, không dựng hạng/cờ/thao tác.
- **FACT — bản UI cuối:** hash và byte hai JSON `grafana-l8b/t065-l8b-*.json` khớp `may-l8b/kiem/may-sau.json#/new_dashboards`. Không còn tham chiếu UID L4 trong hai JSON này. Bằng chứng lưu `kiem/007-gc-chrome/doi-chieu.json` có 18 trang, 9 tổ hợp bảng, 9 đích Explore; đủ 29 ảnh và các tệp trang/request-response/ảnh được dẫn tồn tại. Đây là kiểm hồ sơ đã lưu, không phải bấm lại hay xác nhận mọi hàng của bảng ảo đều hiển thị. L8c đã tách số hàng DOM và tổng nguồn.
- **N1 tự tìm — CANDIDATE, CHẶN tuyên bố đường vào “hiện hành” đã đồng bộ:** `kiem/003-trinh-duyet/folder-plan.json#/dashboard/panels/0/options/content` còn dẫn `/d/t065-l4-rca`, `/d/t065-l4-phat-lai`, ghi V032/V041 và 22 ca là hiện hành. `may-l8b/kiem/may-truoc.json#/files` ghim mục lục và hai file L4 ở thư mục hiện hành; `may-sau.json#/old_files_changed` rỗng. Hai dashboard L8b chỉ thêm vào thư mục hiện hành. Như vậy hồ sơ nguồn hỗ trợ lỗi đường vào/lưu trữ bị lạc mốc; chưa có phép GET live L9 nên không khẳng định đây là ảnh chụp máy hiện giờ. Sửa tối thiểu dự kiến: mục lục trỏ tới hai UID L8b và ghi 28 ca cùng đúng trạng thái p7/V082/V071; chuyển đúng hai dashboard L4 sang lưu trữ, giữ UID và byte JSON. Không sửa trong L9; cần đối chiếu phạm vi quyền mới và hash trước khi trình thực thi.
- **OPEN có giới hạn:** Loki T-062 rỗng và metadata ngoài khung nhìn là quan sát trong hồ sơ L8c. Chưa có log/request đúng thời điểm đủ để chọn giữa các giải thích lưu giữ/nhãn/tham số/tải/hiển thị. Không quy là lỗi dữ liệu hoặc M1. Đánh giá lại từng điểm sau khi đọc reviewer; chỉ đề xuất bổ sung bằng chứng khi có quyết định phụ thuộc cụ thể. Không dùng việc UI đúng để xác nhận hiệu quả phương pháp hay đóng RQ5/P10.
- Chưa thấy lỗi số xuất mới trong phần đã đối chiếu. Chưa mở kết luận REVIEW/REVIEW-2/REVIEW-3 tới thời điểm nối đoạn này. Các quan sát trên không tự nghiệm thu task hoặc gỡ phản đối chưa đọc.

### Đáp REVIEW-3 sau tự soát

- **S1 — Đúng — CHẶN nghiệm thu G-c và trình diễn bản cuối qua điểm bắt đầu.** Đọc lại mục lục ghim tại grafana-l5/t065-l5-muc-luc.json; nội dung không có hai UID L8b, V082/V071 hoặc 28 ca. may-l8b/kiem/may-truoc.json ghim mục lục và hai L4; may-sau.json ghi 0 file cũ đổi và đặt hai L8b cùng folder hiện hành. Hai dashboard L8b riêng khớp nguồn, nên lỗi thuộc đường vào/lưu trữ, không thuộc số xuất. N1 tự soát L9 trùng vấn đề này. L8 chỉ cho thêm mới; không tự sửa. Đề xuất mục lục mới trỏ L8b, V082 đề xuất cuối Minh chọn và V071 thay thế; chuyển đúng hai L4 sang lưu trữ giữ UID/byte. File, hash dự kiến, hoàn tác và chi phí ở LOG L9.
- **S2 — Đúng một phần — KHÔNG CHẶN.** Nhãn “không có đầu ra cạnh” đúng ở 28/28 slot V082; chưa có bằng chứng người xem thực sự hiểu sai. Thiếu lời giải thích có thể gây nhầm khi demo. Hash cây mã src/m1 + src/m1_ft khớp bản V082; chuoi.py dùng E1 ở mau_thao_tac, E2 ở mau_canh/gan_canh, E5 ở phan_loai; H1c không bật không đồng nghĩa tắt E1/E2/E5. Đề xuất chỉ thêm description panel 5 của JSON RCA, dẫn hồ sơ chọn §15 và nói graph thao tác là truy vết; không sửa 28 bản xuất hoặc phương pháp. Nguồn sửa lưu riêng grafana-l10, giữ JSON L8b lịch sử; chi tiết/hash ở LOG.
- **S3 — Đúng một phần — KHÔNG CHẶN.** Tự đếm L5: 6 query booking thuần rỗng, 6 query payment có dữ liệu cùng window. Nhưng snapshot L4 panel 35 có thêm regex error/exception/warn, nên không phải cùng query ở cả ba mốc. L9 đã kiểm raw-logs.jsonl theo manifest ca 00eaea92: 14.280 logRecords, 7.400 trong cửa sổ, payment 885, booking 0 theo resource service.name. Điều này thu hẹp vắng dữ liệu ghi nhận; không chứng minh ứng dụng không phát log và không loại mọi khả năng retention/nhãn/định tuyến theo stream. Chưa có stdout/Collector/Loki đúng thời điểm để tách các giải thích. Đề xuất nối đính chính vào báo cáo L8c; giữ nguyên nguyên nhân OPEN, không sửa kho quan sát. Lệnh/count, giới hạn, hash dự kiến và chi phí ở LOG L9.
- **S4 — Đúng — KHÔNG CHẶN; gói đính chính chưa được duyệt thực hiện.** Hash BAO-CAO L5 và BAN-GIAO-L5 khớp manifest L7-truoc và manifest hiện hành; không được tự áp dụng góp ý. Đếm lại R2 khớp 36 URL số của e8661e0a, 67/1.665 lượt số của 21 ca khác; R3 khớp 586 bản ghi, 568 khóa, 381 false positive, 187 panel (177 i, 10 iii). R1/L7 có 12/12 luồng với Inspector HTTP 200; phản hồi N1 lịch sử vẫn có giới hạn cơ chế. Đề xuất nối cùng đính chính vào hai tài liệu, giữ câu/file thô và lưu manifest trước khi ghim lượt mới. Không sửa trong L9.
- **N1 (L9) — Tự soát trước review — CHẶN, cùng phạm vi S1; không tính thành lỗi thứ hai.** Nguồn độc lập trước khi đọc kết luận: folder-plan.json#/dashboard/panels/0/options/content, may-truoc.json#/files và may-sau.json#/old_files_changed. Kết luận chỉ cho mốc hồ sơ L8b/L8c; chưa GET live ở L9. Đề xuất và quyền chờ như S1. N1 của L6 là lỗi thời gian lịch sử khác, không gộp với N1 này.
- **N2 (L9) — Tự kiểm sau đọc review — KHÔNG CHẶN; sai đơn vị đếm trong nhận định G-c của REVIEW-3.** 726 là số thao tác, không phải số phần tử lien_ket: 295 + 303 + 128 thao tác ở 86dea661/ebd5ef38/00eaea92. Số liên kết tương ứng 601 + 609 + 269 = 1.479; đối chiếu đầy đủ id và mảng lien_ket giữa V082/V071 đều trùng. Chín lần Explore L8c đều ở V071 đúng như reviewer nêu. Kết luận dùng lại bằng chứng vẫn đứng; đề nghị reviewer dùng đúng đại lượng trong lượt sau. Người làm không sửa nhận xét của reviewer.

### Kiểm riêng các lượt trước

- **P1:** đúng ở lượt 1; bằng chứng L5 và L7 đã bổ sung phần thiếu của G-a/G-b. **R1:** đủ căn cứ đề nghị gỡ điểm chặn này: `kiem/004-r1-ui06/doi-chieu-dich.json#/luong` có 12 luồng, đối chiếu mỗi `lan_bam_chot` với `/lan_bam`: đủ 12 bản ghi, 12 HTTP 200, toàn bộ trường `/kiem` của 12 bản ghi đúng. Lần 19 có `/query_inspector/request_response_file` và `/query_inspector/extracted_file`, không còn là checkpoint thiếu Inspector. Không tự nghiệm thu task.
- **P2/R2:** snapshot có ghi giờ và không suy nguyên nhân, đáp ứng phần diễn giải đã kiểm; 10 quan sát lịch sử vẫn OPEN. L9 đếm lại `kiem/003-trinh-duyet/nhat-ky-bam.jsonl`, lọc `utc < 2026-11-14T08:50:00Z` và URL `/d/t065-l4-rca`: e8661e0a 36 số/0 ISO; 21 ca khác 67 số/1.598 ISO trong 1.665 lượt. Phân tích 67 DOM hợp lệ ở `codex/L6-dap-review2.json#/checks` (theo name `R2_offline_67_other_numeric_observations`) chưa có request/response/panel sống để phân xử. Các giải thích còn lại: điều hướng/biến cửa sổ, trạng thái tải, hiển thị hoặc nhánh dự phòng. Cần bằng chứng đúng giờ cũ; gói hiện tại không có, chạy hiện tại không thay được. Không chặn kết quả UI06/L8c đã được kiểm.
- **P3:** không thấy phản đối còn lại về phân loại `khac`; hồ sơ `khac-audit.md`, `khac-audit.json` đã được manifest ghim. Việc phân loại hiển thị không tự chứng minh chất lượng tín hiệu hay RCA. **P4:** dùng JavaScript không gây lỗi đã xác lập; L8b dùng Python, L9 chỉ đọc/đối chiếu, không tự chạy lại generator. `l8b-kiem.py` có nhánh ghi kết quả; không gọi script ấy trong lượt chỉ đọc đầu ra.
- **R3:** tự đếm lại `panel-rong.json`: 586 dòng, khóa `(ban,ca,service,panel)` có 568, tức 18 trùng. `doi-chieu-rong-snapshot.json`: 187 panel, gồm 177 i và 10 iii, cộng 381 false positive = 568. Phản hồi L6 đúng; đính chính chỉ dẫn chưa được duyệt làm.
- **R4:** biên nhận `folder-rca-xoa.json` có danh sách dashboard và folder con rỗng, DELETE 200. Hai nguồn quyền 13/11 (điều phối/triển khai) và 14/11 (provider/chuyển file, dẫn brief) cho phép hai cách diễn giải. Reviewer đã rút kết luận chắc chắn vượt quyền. Đề xuất Minh xác nhận giữ trạng thái folder rỗng đã xóa; không hoàn tác chỉ để tạo UID mới. Mặt trái: quyền xóa chưa được ghi rõ. Phương án khác là Minh yêu cầu tạo lại và chấp nhận UID mới. Chưa có quyết định; không ghi DECISIONS hoặc tạo lại.
- **N1 của L6:** phản hồi lịch sử vẫn đúng theo các file nguồn đã ghim và bảng L6. Không dùng ba trang e8661e0a làm bằng chứng truy vấn đúng lúc cũ; bằng chứng sau UI06 đúng cửa sổ. Cơ chế cũ chưa phân xử vì thiếu request/response đúng thời điểm. N1 này khác N1 tự soát L9.

### S3 — lệnh chỉ đọc và mức phân xử mới

Đã đọc `results/T-062/ca/00eaea92/cases/00eaea92/manifest.json`, đối chiếu SHA và số byte `raw-logs.jsonl` trước khi dùng. File 54.905.842 byte khớp pin. Đếm lần lượt từng batch `resourceLogs`, từng `scopeLogs`, từng `logRecords`; lấy service từ `resource.attributes[service.name]`, thời gian `BigInt(timeUnixNano ?? observedTimeUnixNano)`, lọc cận dưới bao gồm/cận trên loại trừ theo `method_window_seconds`. Không mở raw trace hay dữ liệu khóa.

Kết quả lệnh Node REPL đã chạy: `batches=1198, resource_groups=7626, total_records=14280, in_window=7400, missing_timestamp=0`. Trong cửa sổ: `api-gateway=5909, payment-service=885, ticket-service=590, keycloak=16, booking-service=0`; tổng bốn service có bản ghi là 7.400. Ngoài lọc cửa sổ cũng không có resource mang tên booking-service. Danh sách khóa service resource chỉ có `service.name`, `service.instance.id`; không có khóa service trong log.attributes ở các bản ghi trong cửa sổ. Đây là đếm resource đã lưu, không chứng minh ứng dụng không phát log hoặc không có một alias chưa ghi nhận.

Đối chiếu query thật: snapshot L4 `kiem/002/api-snapshot.json#/00eaea92~1booking-service/queries` (panel 35) có regex lỗi/cảnh báo; sáu booking L5 và Loki L8c là selector thuần. Sáu payment L5 gồm ba selector thuần, ba selector + lọc traceId. Do đó không thể gọi mọi mốc là cùng truy vấn; chỉ kết luận sự vắng riêng của booking trong capture và các truy vấn đã nêu. Các giải thích còn lại là không phát tại ứng dụng, thu nhận/định tuyến không ghi, nhãn hoặc lưu giữ khác theo stream. Gói hiện có không chứa stdout, log Collector và cấu hình/nhãn/lưu giữ Loki đủ đúng thời điểm để chọn giữa chúng. Đối chiếu các nguồn ấy nếu đã được lưu mới phân xử được; rà vài phút nếu có, chưa xác lập rằng chúng tồn tại và không tự truy cập máy trong L9. Không đề xuất chạy lại ca hoặc sửa Collector để khép OPEN. Hệ quả: khi trình bày đánh giá đầu vào phải nêu coverage log đã quan sát; nguyên nhân gốc của thiếu log vẫn OPEN, không thay hạng/cờ hay biến dữ liệu sống thành kết quả khoa học.

### Đề xuất sửa gom theo file — CHƯA được duyệt thực thi

Đề xuất một gói ngắn xử lý S1, kèm S2/S3/S4 nếu Minh đồng ý. Ưu tiên S1 vì chặn đường vào trình diễn. S2 chỉ thêm lời giải thích; S3/S4 nối tài liệu để người đọc không phải dựng lại lịch sử. Không chạy lại M1, raw, 84 slot hay toàn bộ bộ UI. Chi phí **chưa kiểm**: S1 khoảng 10–20 phút nếu SSH/Chrome sẵn; thêm S2/S3/S4 và chốt hồ sơ khoảng 15–20 phút. Kết nối hoặc provisioning chậm có thể tăng thời gian; không hứa ETA. Không dùng subagent.

**Bản đồ tác động, cần Minh cấp quyền riêng trước mọi thao tác dưới đây:**

| Điểm | File/thao tác dự kiến | Tác động, kiểm cần có và hoàn tác |
|---|---|---|
| S1 | Nguồn phát hành mới `results/T-065/grafana-l10/t065-l5-muc-luc.json`; thay đúng file máy `/opt/flash-ticket-obs/pinned/provisioning/dashboards/RCA FlashTicket/0 · Bắt đầu tại đây/t065-l5-muc-luc.json` bằng nguồn mới. Giữ file local L5 cũ. | Chỉ đổi panel văn bản: hai UID L8b, 28 ca × 3 bản, V082 đề xuất cuối Minh chọn/V071 thay thế; L4 ghi lưu trữ. Giữ UID mục lục. GET hash live trước khi ghi phải bằng pin trước; khác thì dừng phần phụ thuộc và trình lại. Hoàn tác bằng byte mục lục cũ đã lưu. |
| S1 | Trên exp-obs, chuyển đúng `t065-l4-rca.json` và `t065-l4-phat-lai.json` từ `RCA FlashTicket/1 · Kết quả hiện hành/` sang `RCA FlashTicket/9 · Lưu trữ/L4 · Bộ bản tạm · 14-11/` dưới thư mục provisioning dashboards. | Không sửa UID/byte JSON; không đổi provider hoặc dữ liệu t065-l4-001. Kiểm UID/folder bằng API và bấm từ mục lục tới hai UID L8b; một ảnh mục lục. Hoàn tác chuyển hai file về vị trí cũ nếu trạng thái vẫn đúng hash của lượt. Cần kiểm không có file đích trước khi chuyển; không ghi đè. |
| S2 | Nguồn phát hành mới `results/T-065/grafana-l10/t065-l8b-rca.json`; thay đúng file máy `…/RCA FlashTicket/1 · Kết quả hiện hành/t065-l8b-rca.json`. Giữ JSON L8b local. | Chỉ thêm `description` của panel 5 theo câu dưới. Giữ targets, variables, time, links, UID và dữ liệu. Kiểm diff ngữ nghĩa đúng một trường, GET loaded JSON. Hoàn tác byte JSON RCA trước sửa. Không cần đổi bản phát lại hay 28 file dữ liệu. Không chạy đường deploy L8b vì guard của nó đòi file mới chưa tồn tại. |
| S3 | Nối đúng khối S3 dưới vào `results/T-065/kiem/007-gc-chrome/BAO-CAO.md`. | Bổ sung bằng chứng raw và phân biệt query; giữ câu cũ như lịch sử, không nhận đã xác định cơ chế. File đã ghim nên hash đổi. Hoàn tác từ bản lưu nguyên byte trước gói, chỉ khi chưa có thay đổi khác. |
| S4 | Nối đúng khối S4 dưới vào `results/T-065/kiem/003-trinh-duyet/BAO-CAO.md` và `results/T-065/BAN-GIAO-L5.md`. | Cập nhật R1/L7, chỉ nguồn R2/R3/N1 và bản cuối; giữ mọi câu cũ, dữ liệu thô và REVIEW. Hai hash đổi; giữ bản lưu nguyên byte. Không coi bản lịch sử là báo cáo hiện hành. |
| Hồ sơ của gói sửa | Chỉ thêm đầu ra thực thi trong `results/T-065/kiem/008-dinh-chinh/` (biên nhận, sao lưu file cần thay, kiểm folder/hash/JSON và ảnh); thêm hai nguồn JSON `grafana-l10/` nêu trên; lưu manifest hiện hành nguyên byte ở `codex/manifest-L10-truoc.json`; sau bằng chứng mới, nối CHECKPOINT.md/thay-doi-may.md, cập nhật XONG.md/prompt-ban-giao.md/manifest.json và một mục LOG T-065 của gói sửa. Không sửa STATE, SPEC, docs, nguồn T-064 hoặc code M1. | Đây là hồ sơ bắt buộc của chính thay đổi dự kiến, chưa được quyền ghi trong L9. Trước khi ghi kiểm tất cả pin liên quan. Manifest trước giữ nguyên như lịch sử; manifest mới ghim đúng báo cáo/ảnh/nguồn mới và LOG sau lượt, không tự ghi nghiệm thu. Hash sau của ảnh/biên nhận/manifest/LOG phụ thuộc kết quả thực thi chưa xảy ra nên **chưa có**; không điền hash giả. Nếu không được cấp phạm vi này thì chỉ trình đề xuất, không sửa. |

Phương án khác đã xét: chỉ cho người xem một URL L8b trực tiếp và giữ mục lục cũ — rẻ hơn nhưng không xử lý S1. Chỉ giữ đính chính trong LOG/REVIEW — giữ hash báo cáo cũ nhưng người đọc riêng các báo cáo không thấy cập nhật. Sửa l8b-xuat.py hoặc toàn bộ dữ liệu xuất để giải thích S2 — rộng hơn nhu cầu và làm đổi pin mã tạo L8b; không chọn. Bản sửa nguồn JSON giữ riêng để không biến lịch sử L8b thành nguồn đã sửa.

Các hash trước dưới đây đã kiểm từ hồ sơ local đã ghim, **không là xác nhận hash máy hiện giờ**. Hash sau chỉ là giá trị ứng viên tính trong bộ nhớ, không là biên nhận đã sửa. Gói thực thi phải đối chiếu pin live ngay trước thao tác. JSON ứng viên lấy nguyên object nguồn, chỉ đổi trường nêu rõ, xuất bằng `JSON.stringify(object) + "\n"` (UTF-8, không BOM). Khối nối tài liệu = hai LF + nguyên văn khối dưới + một LF cuối, giữ nguyên byte trước đó.

| Mục | File/byte cần kiểm | SHA-256 trước | SHA-256 sau DỰ KIẾN | Byte sau |
|---|---|---|---|---|
| S1 | `grafana-l5/t065-l5-muc-luc.json` → nguồn phát hành mới `grafana-l10/t065-l5-muc-luc.json` | `2e2e42419a9f47bfb17c24a390273ab796118849b90a17647874710e7641c2db` | `c5170208559d62b12aa9428f7b988acf056eed215e4fa6f0b371a678937ef74f` | 3101 |
| S2 | `grafana-l8b/t065-l8b-rca.json` → nguồn phát hành mới `grafana-l10/t065-l8b-rca.json` | `12acad7d9cb80c57546df322e3c73f291c0d769ba3520240b36473d552be4ac1` | `98821bf0a4e95053f38c2d71af9c89c72058ae3301a587b56a4c9b1fb01bb1ef` | 36665 |
| S3 | `kiem/007-gc-chrome/BAO-CAO.md` (chỉ nối) | `6355b69ebcc4cf1d6c807d53f2b45cd3934e5d4569a40d5c4ede54b4352c797a` | `69cbc7fcd84d0da1173fdd5537d121a7631c696a94380b44630536a1a82f9688` | 7049 |
| S4a | `kiem/003-trinh-duyet/BAO-CAO.md` (chỉ nối) | `5e196236e9a72461b6e9bcd1a07b296b7519977cef2ffcce11db550f7222fec0` | `2aabb2b39ed50944efba4d8cc56d72631e6803523a442fac9bd4f1ab505f35c3` | 18584 |
| S4b | `BAN-GIAO-L5.md` (chỉ nối) | `c5ec446f9330dcb25a509989a9c7b65a9af892b7520de06ce725227d370e1058` | `eca5883775e3fac5e022ac77635ab7de5ca89046b0d89ccb412dfc84b267e835` | 6751 |
| S1 chuyển chỗ | `t065-l4-rca.json` | `27140f7a6526fd9c68cb7f45ef79e92e06ec4efe1fe9b892093dbfc523fa61fb` | `27140f7a6526fd9c68cb7f45ef79e92e06ec4efe1fe9b892093dbfc523fa61fb` | 62178 |
| S1 chuyển chỗ | `t065-l4-phat-lai.json` | `be98e32cb80417af0ae426df2a1be6ad39534f0f7dfbd4be49e62d26333589f9` | `be98e32cb80417af0ae426df2a1be6ad39534f0f7dfbd4be49e62d26333589f9` | 26183 |

**Nội dung panel mục lục S1 dự kiến** (chỉ thay `panels[0].options.content`, giữ các trường khác):

```text
## Chọn nơi bắt đầu

- **[Mục lục RCA](/d/t065-l5-muc-luc)** — Điểm bắt đầu. Bộ bản hiện hành: p7 (khoa_P7), V082-V066+H8a (de_xuat), V071-V041+H8a (thay_the). Số ca: 28 ca × 3 bản (9 T-062 + 13 dev2 + 6 dev3). Nguồn giao diện: T-065 / L8b, kiểm Chrome L8c; cập nhật 15/11/2026.

- **[RCA — bản đề xuất cuối V082](/d/t065-l8b-rca)** — Chọn bản → ca → service → thao tác → bằng chứng. V082 là đề xuất cuối Minh chọn ngày 14/11/2026; V071 là bản thay thế có đầu ra cạnh. Số ca: 28 ca mỗi bản. **Hiện hành**; việc chọn bản không thay nghiệm thu T-064/T-065.

- **[Phát lại có đáp án — T-062](/d/t065-l8b-phat-lai)** — Lớp đáp án riêng cho 9 ca T-062; 19 ca dev chỉ hiện giới hạn chưa cấp đáp án. Cùng ba bản và 28 ca. **Hiện hành**.

- **[L4 — RCA bộ bản tạm](/d/t065-l4-rca)** — p7, V032-H5b, V041-R1-H1c+H5b+H8s1; 22 ca mỗi bản (9 T-062 + 13 dev2). **Lưu trữ — bộ bản tạm L4**, không là bản đề xuất cuối.

- **[L4 — phát lại bộ bản tạm](/d/t065-l4-phat-lai)** — Cùng ba bản tạm; 9 ca T-062 có lớp đáp án riêng, 13 ca dev2 có giới hạn. **Lưu trữ — bộ bản tạm L4**.

- **[L3 — sự cố và thao tác M1](/d/t065-rca)** — Mốc hồi quy giao diện lớp thao tác. Bản: P7 khóa. Số ca: 9 ca T-062. Nguồn giao diện: T-065 / L3; ngày 13/11/2026; **lưu trữ**.

- **[L3 — phát lại có đáp án](/d/t065-phat-lai)** — Mốc hồi quy trang phát lại. Bản: P7 khóa. Số ca: 9 ca T-062. Nguồn giao diện: T-065 / L3; ngày 13/11/2026; **lưu trữ**.

- **[G2 bản 6 — xem sự cố](/d/rca-g2)** — Mốc hồi quy dashboard G2. Bản: P7 khóa. Số ca: 9 ca T-062. Nguồn giao diện: T-062 / G1 bản 6; ngày 12/11/2026; **lưu trữ**.

- **[G2 bản 6 — phát lại có đáp án](/d/rca-g2-phat-lai)** — Mốc hồi quy phát lại G2. Bản: P7 khóa. Số ca: 9 ca T-062. Nguồn giao diện: T-062 / G1 bản 6; ngày 12/11/2026; **lưu trữ**.

### Trạng thái và giới hạn

P7 đã khóa. V082 là đề xuất cuối Minh chọn; V071 là bản thay thế có đầu ra cạnh. Không suy việc chọn bản là nghiệm thu task hoặc bằng chứng hiệu quả phương pháp.

Hai hash cấp bản P7 là null trong chỉ mục T-064; không suy hash từ file đầu ra. Trang chính và mục lục không chứa đáp án. Span link message chưa hỗ trợ.

Nguồn bản và ca: results/T-064/ban-xuat/chi-muc-ban.json. Cửa sổ trang ca: [t−300,t+300).
```

**Description panel 5 S2 dự kiến** (thêm trường, không sửa target):

```text
V082 không xuất bảng xếp hạng cạnh. Phương pháp vẫn dùng quan hệ qua E1 (tách thời lượng thao tác theo span con), E2 (gán bằng chứng cạnh) và E5 (tách tự sinh/kế thừa). Đồ thị thao tác ở panel 23 chỉ truy vết quan hệ span quan sát được. Nguồn: results/T-064/ho-so-chon.md §15; src/m1/chuoi.py.
```

**Khối nối S3 dự kiến:**

```markdown
## Đính chính L9 — Loki T-062, bổ sung bằng chứng đã lưu

L4 (`../002/api-snapshot.json`, khóa `00eaea92/booking-service`, panel 35) dùng `{service_name="booking-service"} |~ "(?i)error|exception|warn"`; query này khác query thuần `{service_name="booking-service"}` của sáu lượt L5 và L8c. Không coi ba mốc là cùng query. L5 ghi sáu lượt booking rỗng và sáu lượt payment có dữ liệu trong cùng cửa sổ; ba lượt payment dùng selector thuần, ba lượt thêm bộ lọc traceId. Nguồn: `../003-trinh-duyet/kiem-lien-ket-that.json` (lọc ca 00eaea92, kho loki).

L9 kiểm hash và số byte `results/T-062/ca/00eaea92/cases/00eaea92/raw-logs.jsonl` theo `manifest.json` cùng thư mục trước khi đếm: 1.198 batch, 14.280 logRecords; 7.400 bản ghi có timeUnixNano trong [1794442999000000000,1794443599000000000), gồm 885 payment-service và 0 booking-service theo resource.attributes[service.name]. Không có timestamp thiếu. Nguồn lệnh chỉ đọc và kết quả đầy đủ: LOG T-065 mục L9, phần S3.

Bằng chứng này không phù hợp với giải thích toàn bộ cửa sổ đã bị xóa đồng loạt ở mọi service tại các lượt L5. Nó chưa xác định vì sao booking vắng trong gói capture và trong Loki: ứng dụng không phát, thu nhận/định tuyến không ghi, nhãn hoặc lưu giữ theo stream còn là các giải thích. Cần stdout hoặc nhật ký Collector và cấu hình/nhãn/lưu giữ Loki đúng thời điểm cũ để phân xử; gói hiện có không chứa chuỗi bằng chứng đó. Truy vấn lại bây giờ không tái tạo lịch sử. Giữ nguyên nguyên nhân OPEN; không từ đây kết luận lỗi dữ liệu/M1 hoặc cần sửa Collector. Điều này chỉ ảnh hưởng lời giải thích dữ liệu sống, không thay hạng, cờ hay phép kiểm điều hướng đã đạt.
```

**Khối nối S4 dự kiến, dùng nguyên văn cho cả hai file:**

```markdown
## Đính chính sau L5 — bằng chứng L6/L7 và bản G-c cuối

Đoạn này bổ sung lịch sử, giữ nguyên nội dung và hồ sơ L5 trước đó. Nguồn: LOG T-065 mục L6–L9; `results/T-065/codex/L6-dap-review2.json#/checks`; `results/T-065/kiem/004-r1-ui06/doi-chieu-dich.json`.

- R1: L5 chưa đủ bằng chứng bấm các data link sau UI06. L7 đã bổ sung 12/12 luồng gồm panel 4/22/23 trang chính và panel 4 phát lại trên ba mẫu; có request/response Inspector, kể cả lần bấm 19. Không coi bằng chứng cũ trước UI06 thay cho lượt kiểm này.
- R2: trước 08:50Z, e8661e0a có 36/36 URL số; 21 ca khác có 67 URL số trong 1.665 lượt. Các DOM của 67 lượt chỉ Loading/vỏ trang, không là đối chứng panel sống. URL số là ứng viên, chưa xác nhận nguyên nhân 10 quan sát lịch sử loại (iii); vẫn thiếu request/response đúng giờ cũ.
- R3: `results/T-065/kiem/003-trinh-duyet/panel-rong.json` là 586 bản ghi thô; sau gộp còn 568 khóa, trong đó 381 false positive và 187 panel (177 loại i, 10 loại iii) ở `results/T-065/kiem/003-trinh-duyet/doi-chieu-rong-snapshot.json`. Dùng file đối chiếu làm nguồn phân loại; giữ file thô.
- N1 của L6: ba trang e8661e0a có 30/660 Start time hiển thị ngoài cửa sổ; không dùng các panel đó chứng minh truy vấn lịch sử đúng. Bằng chứng sau UI06 của ba bản đúng cửa sổ; chưa xác định được cơ chế quá khứ khi thiếu request đúng giờ.

Bản G-c cuối p7/V082/V071 thuộc lượt L8b/L8c, không phải bộ bản tạm L4 của báo cáo này. Xem `results/T-065/kiem/006-gc-cuoi/BAO-CAO.md`, `results/T-065/kiem/007-gc-chrome/BAO-CAO.md` và phản hồi L9. Không tự nghiệm thu task, đóng RQ5/P10 hoặc mở test.
```

### Đề nghị và phần cần Minh quyết

- Đề xuất cấp gói S1 và gộp S2/S3/S4 như bản đồ tác động trên. Chưa sửa bất kỳ phần nào của gói; đây là đề xuất cần duyệt, không là quyền đã có. S1 vẫn CHẶN nghiệm thu G-c/trình diễn qua điểm bắt đầu, dù đường xem hai dashboard L8b đã đạt trên mẫu.
- Đề xuất giữ trạng thái folder RCA rỗng đã xóa ở R4; Minh phân xử phạm vi quyền. Chưa có lời quyết mới để ghi DECISIONS. Không tự ghi quyết định nghiên cứu mới.
- Đề xuất Claude kiểm lại phản hồi L9 và các đề xuất này trong một lượt ngắn; sau S1 được duyệt sửa và kiểm phần chịu ảnh hưởng thì đề xuất dừng nếu không còn phản đối ảnh hưởng tính đúng. Không đòi kiểm lại 84 slot hoặc chạy thí nghiệm để xác nhận sửa văn bản/folder. S2/S3/N2 có phần phản bác cụ thể, cần đối chiếu, không mặc định hai bên đã đồng ý.
- T-065 chỉ đáp ứng phần minh họa/truy vết của DT18-NV3 trong phạm vi đã kiểm. Hiệu quả phương pháp, kiểm độc lập ngoài dev và RQ5/P10 theo hồ sơ nghiên cứu; task giao diện và đồng thuận phản biện không thay bằng chứng đó. Nếu đầu ra/chỉ mục/hash bản cuối thay thì chỉ cập nhật phần chịu ảnh hưởng theo quyền mới, không tự khóa hoặc nghiệm thu T-064. Không mở test.

### Báo cáo cuối lượt L9

1. Đã tự soát và ghi nhận xét trước review; kiểm S1–S4, đối chiếu P1–P4/R1–R4/N1 L6 và bổ sung N1/N2 L9. Kiểm nguyên vẹn và đối chiếu 84 slot; đếm log được phép để thu hẹp S3; chuẩn bị đề xuất cụ thể có hash dự kiến, hoàn tác và chi phí.
2. Chỉ đổi bảng cuối REVIEW-3 và nối trong mục LOG L9 này. Giữ nội dung/prompt reviewer, các bản lượt cũ và mọi đầu ra. Không sửa STATE hoặc manifest.
3. Kiểm trước ghi đạt 9.175 checksum + LOG. Đối chiếu 83 SHA nguồn hiện tại/snapshot và 84 slot: không sai khác ở các trường đã kiểm; các tổng khớp `may-l8b/kiem/kiem-xuat.json`. Hash cây mã V082 và ba tệp nguồn T-064 (`ho-so-chon.md`, `cau-hinh-de-xuat.json`, `ban-xuat/chi-muc-ban.json`) khớp manifest tương ứng. Kiểm bảng/LOG và tập file sẽ ghi chốt sau prompt dưới.
4. L9 hoàn tất phần đáp phản biện, chưa sửa S1–S4 hoặc nghiệm thu T-065. S1 chặn đường vào; R4 cần Minh phân xử quyền; nguyên nhân thiếu log booking và 10 quan sát lịch sử còn OPEN vì thiếu chứng cứ đúng thời điểm; số/đơn vị đếm N2 cần reviewer đối chiếu. Câu hỏi nghiên cứu không tự đóng.

Bước tiếp chính xác: Claude đọc nguồn gốc rồi kiểm bảng phản hồi REVIEW-3 và mục L9 này, chỉ trả lời chat tới khi có quyền bản phản biện mới. Nếu Minh duyệt gói sửa, người làm đọc lại hash/byte dự kiến và kiểm pin live trước khi thay file; triển khai theo từng dòng bản đồ tác động rồi kiểm mục lục/folder và JSON chịu ảnh hưởng. Không chạy `l8b-local.ps1 -Action seal` để ghi lại mốc cũ. Sau L9, `-Action verify` nguyên trạng sẽ báo LOG vì LOG được nối trong quyền; phải kiểm `files` và tiền tố LOG dài `manifest.json#/task_log/bytes`, không diễn giải đây là mất toàn vẹn nội dung cũ.

Lệnh cuối trước chốt: Node REPL đối chiếu 12 luồng R1 với bản ghi bấm chốt, đếm lại R3 theo khóa và tính hash đề xuất hoàn toàn trong bộ nhớ. Kiểm chốt và lệnh cuối thực tế ghi nối sau prompt, trong cùng mục L9. Nội dung commit có thể trình riêng khi Minh yêu cầu: `docs(t065): đáp REVIEW-3 và trình gói sửa đường vào bản cuối`. Chưa commit/push.

### Prompt bàn giao cho Claude — kiểm lại phản hồi và đề xuất L9

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, lượt L9 đáp REVIEW-3 và đề xuất sửa trong tasks/T-065-giao-dien-grafana/LOG.md; tasks/T-065-giao-dien-grafana/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện.
- Tài liệu gốc: AGENTS.md; tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md; results/T-065/codex/L8-brief.md, L8b-brief.md, L8b-app-brief.md; results/T-064/hop-dong-dau-ra.md, ban-xuat/chi-muc-ban.json, cau-hinh-de-xuat.json và ho-so-chon.md; docs/DECISIONS.md.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, REVIEW-2.md và REVIEW-3.md (gồm bảng phản hồi L9); results/T-065/codex/L6-dap-review2.json; các mục L6–L9 của LOG T-065.
- Code và kết quả liên quan: results/T-065/grafana-l5/, grafana-l8b/, may-l8b/, nguon-l8b/, kiem/002/, kiem/003-trinh-duyet/, kiem/004-r1-ui06/, kiem/006-gc-cuoi/, kiem/007-gc-chrome/, codex/l8b-xuat.py, codex/l8b-kiem.py, codex/l8b-local.ps1, manifest.json; results/T-062/ca/00eaea92/cases/00eaea92/manifest.json và raw-logs.jsonl; src/m1/chuoi.py, e2.py, e5.py và src/m1_ft/chay.py. Môi trường PowerShell/Node REPL. Manifest L8c ghim phần LOG theo số byte ở task_log; L9 chỉ nối LOG, kiểm files và tiền tố LOG theo pin đó. Đề xuất sửa và các nội dung/hash dự kiến nằm trong LOG L9, chưa có file triển khai mới.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ trả lời trong chat. Chỉ ghi bản phản biện lượt mới nếu Minh hoặc điều phối cấp chính xác tên file và quyền ghi riêng. Không ghi LOG/STATE, không sửa REVIEW cũ, bảng phản hồi, dashboard hoặc kết quả.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

### Kiểm chốt L9 và lệnh cuối

- Node REPL kiểm lại 9.175 file theo SHA-256 và số byte trong `manifest.json#/files`: 9.175 khớp, 0 thiếu/lệch; `manifest.json` nguyên byte. Kiểm 10 file nguồn/quy định/REVIEW cũ đã giữ mốc: không đổi. Không dùng kết quả `-Action verify` của toàn LOG sau nối như thể LOG chưa thay đổi.
- LOG giữ nguyên tiền tố 284.157 byte và hash theo `#/task_log`; toàn phần thêm trước dòng chốt này bằng đúng mục mở, tự soát, báo cáo và prompt L9 đã chuẩn bị. REVIEW-3 giữ nguyên 28.217 byte trước các hàng phản hồi và 1 byte sau bảng; chỉ thay 4 hàng trống bằng 6 hàng phản hồi. Sáu ô Minh quyết đều trống. Prompt chung (trừ thông tin trung tính), khối Kiểm lại phản hồi và sửa và khối G4 khớp mẫu. Phần thêm không có dòng thừa khoảng trắng cuối.
- `git diff --check -- tasks/T-065-giao-dien-grafana/LOG.md tasks/T-065-giao-dien-grafana/REVIEW-3.md` trả 0. Git đang coi hai thư mục task/kết quả là untracked, nên phép này không thay kiểm buffer/prefix đầy đủ ở trên. Có cảnh báo không đọc được file ignore ở cấu hình người dùng; không đổi cấu hình để khắc phục.
- Tập file thay đổi của chính L9: chỉ `tasks/T-065-giao-dien-grafana/REVIEW-3.md` (hàng phản hồi) và `tasks/T-065-giao-dien-grafana/LOG.md` (mục L9). Các hash dự kiến là tính trong bộ nhớ; chưa tạo grafana-l10, gói đính chính, biên nhận hoặc thay file trên exp-obs. Không có quyết định nghiên cứu được thêm/đổi, không cập nhật STATE, không commit/push.
- Lệnh cuối thực tế: Node REPL đọc lại hai file, so toàn bộ REVIEW-3 với bản ghép chỉ đổi hàng, so toàn bộ phần LOG nối với các khối L9 dự kiến, xác nhận tiền tố LOG theo manifest, kiểm các file nguồn đã giữ mốc và lấy dòng bàn giao; chỉ in kết quả, không ghi file. Bước tiếp và phạm vi Claude theo prompt ngay trên; S1 và gói sửa vẫn chờ quyền riêng.


## L10 — 2026-11-15T03:38:26.738Z — Codex, Windows laptop Minh, người làm — sửa S1 REVIEW-3

### Mở lượt và quyền

- EXECUTE theo brief L10 và quyết định Minh ngày 15/11/2026 “Duyệt cả ba”, đã ghi ở docs/DECISIONS.md mục sửa R9/R10/S1. Trong T-065 chỉ S1 được duyệt; S2/S3/S4 chưa duyệt, không áp dụng. Giữ vai trò người làm; Claude phản biện.
- Đã đọc AGENTS, STATE (mốc lịch sử), SPEC, REVIEW-3 phần S1/bảng phản hồi, gói L9 và CHECKPOINT cuối. Brief này cấp phạm vi cụ thể; không cập nhật STATE/SPEC/docs hoặc T-064. Nguồn DT18/cô và mục tiêu MRP được đọc trực tiếp để giới hạn kết luận giao diện.
- Kiểm trước sửa: toàn bộ 9.175 file trong manifest L8c khớp SHA-256/số byte; tiền tố LOG lịch sử khớp pin. Nội dung mục lục ứng viên lấy nguyên văn khối S1 L9, đúng hash/byte dự kiến, chỉ đổi panels[0].options.content. STOP local/home vắng. Chưa ghi máy; chờ đối chiếu hash live của ba file và đích chuyển.
- Môi trường CLI không có py/rg trên PATH; dùng Node/PowerShell và SSH Python3 hiện có. Các lệnh đọc thử thất bại không thay file hoặc môi trường. Không chạy lại M1/bộ xuất/API dữ liệu/UI L8b–L8c.

### Hash live trước sửa

- GET qua SSH và API tại 2026-11-15T03:39:53.555734+00:00: ba file mục lục/L4 khớp pin L9; hai file đích lưu trữ chưa tồn tại. Hai L8b giữ đúng pin. Biên nhận, toàn bộ hash provisioning/compose và folders/search ở results/T-065/kiem/008-s1/may-truoc-001.json; ba file gốc đã lưu nguyên byte ở ban-truoc/. Không in hoặc ghi khóa/mật khẩu.

### Triển khai và tự kiểm S1

- Áp dụng đúng ba file tại 2026-11-15T03:40:17.251389+00:00: mục lục mới; chuyển hai L4 bằng tạo đích không ghi đè rồi bỏ vị trí cũ, giữ inode/UID/byte. Ghi nhận từng thao tác ở kiem/008-s1/ap-dung-001.jsonl.
- API tại 2026-11-15T03:40:27.638204+00:00 đã nạp đúng nội dung mục lục, cả năm UID trả 200; search/folders xác nhận L4 trong nhánh 9 · Lưu trữ/L4 · Bộ bản tạm · 14-11, chỉ hai L8b trong Hiện hành. Liên kết mục lục trỏ đúng hai UID L8b và đích API tồn tại; chưa bấm hai link bằng trình duyệt trong L10. Hash đúng bảng L9. Toàn bộ file provisioning/compose ngoài ba file cho phép giữ hash; Grafana không restart. Chi tiết hash-truoc-sau.json và doi-chieu.json.
- Đã đọc skill computer-use và tài liệu kèm. Chrome native có cửa sổ; browser access host của unified-computer-use không khả dụng. Không tác động UI native. API render đã thử, trả HTTP 500 “Rendering failed.” (render-001.json). Không chụp được ảnh; giữ nghĩa vụ ảnh để Minh chạy app. Không cài renderer hoặc đổi cấu hình ngoài gói.

### Báo cáo cuối lượt L10

1. **Đã làm:** triển khai đúng S1 L9, kiểm hash live trước/sau, vị trí đích vắng, nội dung và folders/search qua API. Mục lục nguồn chỉ đổi một trường; hai L4 giữ UID/byte; hai L8b ở Hiện hành. Không có quyết định nghiên cứu mới.
2. **File đổi:** nguồn mới grafana-l10/t065-l5-muc-luc.json; bằng chứng/lệnh/byte trước ở kiem/008-s1/; bản manifest trước codex/manifest-L10-truoc.json; cập nhật XONG/prompt-ban-giao/manifest; nối CHECKPOINT/thay-doi-may/LOG và thêm đúng một hàng S1 (sửa) trong bảng cuối REVIEW-3, để trống Minh quyết. Ngoài exp-obs chỉ ba file cho phép, không đổi nguồn khác. Tập file chính xác sẽ được ghim trong kiem/008-s1/kiem-cuoi.json và manifest lượt này.
3. **Kiểm:** trước sửa 9.175 pin local khớp; hash live của ba file đúng pin L9. Sau sửa toàn bộ hash/UID/folder và liên kết mục lục qua API đạt; mười file máy khác trong inventory giữ hash; không restart. Byte hoàn tác đã lưu và khớp pin, lệnh hoàn tác chỉ rà code, chưa chạy. Đã thử browser access và API render, giữ cả bằng chứng lỗi. Kiểm diff đầy đủ theo buffer/prefix và kiểm pin local cuối lượt ghi bên dưới.
4. **Còn thiếu:** ảnh Mục lục và bằng chứng bấm từ Mục lục trong L10 chưa làm. Browser access host không khả dụng; render HTTP 500 “Rendering failed.” Minh mở app, vào /d/t065-l5-muc-luc, chụp ảnh và kiểm hai link hiện hành. Đề xuất giữ triển khai hiện tại để lấy ảnh, không cài renderer ngoài gói; mặt trái là S1 chưa có bằng chứng ảnh để xác nhận hoàn tất. Phương án hoàn tác chỉ dùng nếu Minh yêu cầu và pin còn khớp. S2/S3/S4 chưa duyệt, không sửa. L10 chỉ đáp ứng phần đường vào/lưu trữ của G-c, không bổ sung căn cứ hiệu quả M1, không khép RQ5/P10; T-064/T-065 chưa được nghiệm thu từ lượt này.

**Bước tiếp chính xác:** Minh mở app tại /d/t065-l5-muc-luc để chụp ảnh và kiểm hai UID L8b; Claude đọc source/đầu ra trong prompt dưới, kiểm lại trong chat khi chưa có quyền ghi REVIEW mới. Lệnh tái kiểm API chỉ đọc: `& ([ScriptBlock]::Create((Get-Content -Raw -Encoding UTF8 results/T-065/kiem/008-s1/s1-ssh.ps1))) -Action after -OutputName may-sau-002.json` (lượt mới, không ghi đè). Đọc `kiem/008-s1/BAO-CAO.md`, `doi-chieu.json`, `hash-truoc-sau.json`, `HOAN-TAC.md`, manifest hiện hành và bản trước. Phạm vi chạy thêm/lưu ảnh hoặc REVIEW mới do Minh/điều phối cấp, không tự mở lượt khác.

**Đề xuất commit sau khi Minh quyết:** `T-065: đồng bộ mục lục L8b và lưu trữ L4 theo S1`. Chưa commit/push.

### Prompt cho Claude kiểm lại — Minh chọn chuyển thủ công

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, tasks/T-065-giao-dien-grafana/; lượt L10 theo gói L9.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket; nhánh giao diện Grafana G-c sau G4.
- Người làm và người phản biện chính thức: Codex là người làm; Claude là người phản biện theo SPEC.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md; LOG.md mục L9–L10; docs/DECISIONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; revision c3d27f8a8f8b, đầu ra T-065 chưa commit.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, REVIEW-2.md, REVIEW-3.md; phản hồi của người làm trong REVIEW-3 và LOG L9–L10.
- Code và kết quả liên quan: results/T-065/grafana-l5/; grafana-l10/; grafana-l8b/; kiem/008-s1/; XONG.md; CHECKPOINT.md; thay-doi-may.md; manifest.json và codex/manifest-L10-truoc.json. Máy exp-obs theo hướng dẫn repo; lệnh và môi trường ở kiem/008-s1/s1-ssh.ps1, s1-may.py và HOAN-TAC.md.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; lượt này chưa có quyền ghi bản REVIEW mới.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

### Kiểm chốt L10 và tiếp nhận

- Rà đầy đủ diff bằng buffer: LOG giữ nguyên tiền tố trước L10; REVIEW-3 chỉ chèn đúng một hàng mới và khôi phục được nguyên byte trước khi bỏ hàng ấy, ô Minh quyết trống. CHECKPOINT/thay-doi-may chỉ nối. Prompt chung chỉ điền tám trường trung tính; khối Kiểm lại phản hồi và sửa và khối G4 giữ nguyên văn.
- Rà 9.175 pin cũ: 9.171 nguyên byte, chỉ bốn file hồ sơ được phép đổi (CHECKPOINT, XONG, thay-doi-may, prompt-ban-giao); không thiếu file. Các nguồn L5/L8b/báo cáo S2–S4, AGENTS, SPEC, STATE và mẫu prompt giữ hash. Nguồn grafana-l10 chỉ có mục lục; nội dung và hash đúng gói L9. Manifest trước giữ nguyên byte.
- Làm rõ mục báo cáo: **trên exp-obs** chỉ ba file dashboard được phép; local theo tập file trong kiem/008-s1/kiem-cuoi.json. Ảnh Mục lục và kiểm hai link đã thuộc quyền L10, không cần duyệt lại; chỉ quyền tạo bản REVIEW mới chưa được cấp trong prompt.
- Lệnh shell cuối đã chạy: `git diff --check -- results/T-065 tasks/T-065-giao-dien-grafana/LOG.md tasks/T-065-giao-dien-grafana/REVIEW-3.md`, exit 0. Vì các thư mục đầu ra/task là untracked ở mốc này, kết quả đó không thay cho kiểm diff/pin đầy đủ ở trên.
- Lệnh cuối của lượt: Node REPL ghim tập file ở kiem/008-s1/kiem-cuoi.json, cập nhật manifest sau LOG này, rồi chỉ đọc/kiểm SHA-256 và số byte của toàn bộ manifest, LOG và REVIEW-3. Không commit/push hoặc ghi ngoài phạm vi. Bước tiếp vẫn là ảnh trên app và Claude kiểm độc lập theo prompt trên; trạng thái S1 còn ảnh, không tự nghiệm thu task.


## L11 — 2026-11-15T05:02:43.501Z — mở phiên, cập nhật chỉ mục xuất bản 3

Codex, người làm T-065; Windows laptop điều khiển exp-obs. Quyền theo brief L11 của Minh 15/11/2026 04:55Z. Đã đọc AGENTS, STATE, SPEC, LOG cuối, CHECKPOINT, L8b/L10/ảnh Minh, chỉ mục bản 2/3, hồ sơ chọn §17, WHY-99 và nguồn đề tài/MRP/LESSONS. 9.197 pin T-065 và LOG khớp; chỉ mục bản 3 đúng pin, 83 đầu ra khớp, chỉ hai slot ebd5ef38 đổi. Nguồn kiểm ở kiem/010-chi-muc-3/tiep-nhan.json; giữ manifest trước tại codex/manifest-L11-truoc.json. STOP local/home và remote vắng tại ranh giới đầu.

Phương án trong quyền: thư mục dữ liệu mới t065-l11-001, sao byte dữ liệu L8b rồi dựng lại đúng hai slot từ đầu ra mới; 82 slot giữ byte. Giữ hai UID hiện hành, chỉ đổi đường dữ liệu và chữ chỉ mục bản 2 → bản 3; Mục lục giữ vì đích UID không đổi. GET/live hash trước phải khớp pin, lưu byte trước và guard hoàn tác. Không chạy/chấm M1 hay xuất raw lại. File ghi: kiem/010-chi-muc-3/, dữ liệu/dashboard mới trong results/T-065, XONG/CHECKPOINT/manifest/prompt, nối LOG; trên exp-obs đúng thư mục dữ liệu mới và hai file dashboard đã nêu. Không ghi STATE/docs/SPEC/REVIEW/T-064.


### L11 — 2026-11-15T05:07:45.695Z — kết thúc lượt tại mâu thuẫn nguồn

1. Đã kiểm chỉ mục bản 3 đúng pin; 83 đầu ra bản 3 và 83 bản 2 khớp; chỉ hai slot ebd5ef38 đổi. 9.197 pin T-065/LOG trước phiên khớp. Kiểm chỉ đọc máy: 2.233 file dữ liệu/nguồn cũ khớp; hai dashboard/Mục lục đúng pin L10, GET API HTTP 200; byte trước đã lưu.
2. File đổi chỉ trong results/T-065 và nối LOG: báo cáo/bằng chứng/byte trước ở kiem/010-chi-muc-3/, XONG/CHECKPOINT/prompt/manifest và bản manifest trước. Không ghi máy, STATE/docs/SPEC/REVIEW/T-064. Danh sách chốt tại kiem/010-chi-muc-3/kiem-cuoi.json.
3. Phát hiện mỗi slot mới giảm 65 → 64 cờ, bỏ đúng payment-service_live-down; 64 cờ còn lại giữ toàn bộ trường; thứ tự entity/tie_group và verdict giữ. Bằng chứng doi-chieu-co.json. Brief L11 và T-064 ho-so-chon §17 nói cờ không đổi, nên dừng phần xuất/triển khai theo yêu cầu nguồn. Chưa có API/UI bản 3; không lấy API bản 2 làm kiểm bản 3.
4. Đã hỏi Minh; chưa có trả lời lúc chốt. Đề xuất xuất đúng nguồn bản 3 với 64 cờ, giữ dữ liệu L8b; thay đúng hai dashboard hiện hành, giữ Mục lục. Phương án khác và ảnh hưởng nêu trong BAO-CAO. T-065 chưa nghiệm thu; G-c truy vết bản mới còn thiếu, không có kết luận hiệu quả phương pháp/RQ5/P10 mới. Nội dung cần T-064 trình đính chính: câu cờ hiển thị không đổi trong §17; L11 không được sửa file ấy.

Bước tiếp chính xác: chờ Minh giải quyết; đọc results/T-065/kiem/010-chi-muc-3/BAO-CAO.md và doi-chieu-co.json; kiểm STOP local/home/remote, nguồn và hash live lại trước ghi. Lệnh máy cuối: python3 -B - qua SSH, inventory chỉ đọc, lưu may-truoc-001.json. Lệnh chốt cuối lượt: kiểm checksum bằng node_repl, kiểm prefix LOG/CHECKPOINT, kiểm tập file mới và git diff --check; bằng chứng kiem-cuoi.json. Không có job nền/tunnel/browser mới cần tiếp nhận.

#### Prompt cho Claude — L11

# Prompt bàn giao Claude — T-065 L11

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, tasks/T-065-giao-dien-grafana/; lượt L11 theo brief 15/11/2026.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket; nhánh giao diện Grafana G-c sau G4.
- Người làm và người phản biện chính thức: Codex là người làm; Claude là người phản biện theo SPEC.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md; LOG.md mục L11; docs/DECISIONS.md; results/T-064/ban-xuat/chi-muc-ban.json và chi-muc-ban-2.json; results/T-064/ho-so-chon.md; docs/WHY.md.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, REVIEW-2.md, REVIEW-3.md; phản hồi người làm trong REVIEW-3 và LOG L9–L11.
- Code và kết quả liên quan: results/T-065/kiem/010-chi-muc-3/; results/T-065/kiem/006-gc-cuoi/; kiem/008-s1/; kiem/009-s1-anh-minh/; XONG.md; CHECKPOINT.md; manifest.json; codex/manifest-L11-truoc.json; môi trường exp-obs và lệnh SSH theo hướng dẫn repo.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; chưa có quyền ghi bản REVIEW mới.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```



## L11b — 2026-11-15T05:11:16.391Z — tiếp nhận đính chính và triển khai bản 3

Codex, người làm T-065, Windows điều khiển exp-obs. Minh chuyển đính chính L11b: phạm vi không đổi, dùng đúng đầu ra bản 3 gồm 64 cờ; bổ sung câu nguồn Mục lục theo T1 và kiểm cờ/khóa/chữ H5b theo T2 REVIEW-4. Đã đọc đính chính cuối hồ sơ T-064 §17 và LOG 05:00Z. Tự soát L11 đã xác định cờ/khóa đổi trước khi đọc REVIEW-4. Không ghi REVIEW-4 theo phạm vi lượt này. 9.218 pin T-065/LOG khớp; nguồn bản 3 đúng pin và 83 đầu ra khớp, chỉ hai slot đổi. Bản manifest L11 giữ ở codex/manifest-L11b-truoc.json; mọi hồ sơ dừng giữ trong kiem/010-chi-muc-3 và bản BAO-CAO-L11.md.

Tác động: dữ liệu mới t065-l11-001, dựng lại hai slot/projection; 82 slot giữ byte. Hai dashboard hiện hành giữ UID, chỉ đổi đường dữ liệu và chữ chỉ mục; Mục lục chỉ đổi câu nguồn/phiên bản cập nhật. Trước ghi GET/pin live và lưu byte; dữ liệu L8b không đổi; hướng dẫn hoàn tác có guard. Không chạy/chấm M1 hoặc raw, không sửa T-064/STATE/SPEC/docs/REVIEW; ghim ảnh 009 đã có từ manifest L11.


### L11b — 2026-11-15T05:16:02.094Z — xuất dữ liệu đạt, chưa đổi dashboard

Đã tạo riêng /opt/flash-ticket-obs/rca-ket-qua/t065-l11-001. Trước ghi kiểm 2.233 pin dữ liệu/nguồn L8b và toàn bộ provisioning/compose; GET ba UID khớp file/pin. Dữ liệu 84/84 slot qua kiểm ngữ nghĩa và schema 0.5: 1.410 dòng hạng, 1.650 cờ, 26.266 đơn vị, 600 cạnh, 19.971 thao tác; 48.717 URL đúng giải mã/query/window. Hai ebd5ef38 đúng nguồn R9: 64 cờ, khóa payment [2,4511.154929577465,1.7998955013230344,30,12625.943468737061], H5 chết im rỗng. 82 slot còn lại giữ byte từng ca/vue/phát lại/service; dữ liệu L8b giữ hash. Không chạy raw/M1/chấm; chín P7 T-062 hồi quy đạt. Biên nhận local l11b/stage-001.txt; chi tiết máy kiem/kiem-xuat.json, kiem-schema.json, doi-chieu-byte.json. Tiếp: đổi đúng ba file đã ghim bằng script deploy, rồi API; cách hoàn tác đã lưu l11b/HOAN-TAC.md.


### L11b — 2026-11-15T05:18:23.786Z — triển khai/API đạt, ảnh bị giới hạn công cụ

Đã đổi đúng hai file L8b hiện hành và Mục lục, giữ UID, lưu byte rollback và hash trước/sau. Grafana tự nạp (ready lần 2), không restart. 18/18 trang API (3 bản × 3 ca × 2 trang) khớp metadata/hạng/cờ/cạnh/cửa sổ/biến; hai truy vấn audit khóa qua cùng URL Infinity khớp chính xác từng phần tử khóa nguồn. Bảng hạng hiện hành không có cột khóa; kiểm khóa qua truy vấn audit đọc, không tự thêm cột UI. Không đổi file provisioning khác, compose, provider hay datasource. 82 slot vẫn giữ byte và dữ liệu L8b còn đúng pin. Chi tiết verify-001.txt và biên nhận máy sẽ nhận về may-l11/.

Đã đọc skill computer-use và thử CUA: browser access host unavailable; cửa sổ Chrome có nhưng getApp bị từ chối “Computer Use was not approved to use Google Chrome”. Không có input/UI/screenshot mới, không thử lách quyền hay cài renderer. Biên nhận l11b/trinh-duyet-001.json; ảnh cần Minh chụp sẽ ghi l11b/ANH-CAN-CHUP.md. Không có thao tác UI, tunnel hoặc job API còn dở. Tiếp đóng gói/nhận/kiểm và chốt hồ sơ; không chạy lại M1/raw/chấm.


### L11b — 2026-11-15T05:24:33.664Z — bàn giao dữ liệu/API, ảnh còn thiếu

1. Đã xuất và triển khai chỉ mục bản 3 theo đính chính; giữ UID và dữ liệu L8b, thay đúng hai dashboard và nội dung Mục lục. Hai slot cập nhật cả cờ (64), khóa và nguồn H5b rỗng; 82 slot giữ byte. Không có quyết định nghiên cứu mới.
2. File đổi trong results/T-065: may-l11/, grafana-l11/, kiem/010-chi-muc-3/l11b/, BAO-CAO, XONG/CHECKPOINT/prompt/thay-doi-may/manifest; nối LOG này. Giữ bản trước ở codex/manifest-L11b-truoc.json và l11b/ban-truoc/. Tập file chốt tại l11b/kiem-cuoi.json. Trên máy chỉ thư mục dữ liệu mới và ba file dashboard đã duyệt. Không ghi STATE/docs/SPEC/REVIEW/T-064.
3. Kiểm ngữ nghĩa/schema 84/84, hồi quy 9 P7 T-062; API 18/18 và hai audit khóa qua Infinity đạt. 83 nguồn bản 3 đúng pin; 2.404 file nhận từ máy đúng SHA; 82 slot khác giữ byte và 2.233 file dữ liệu/nguồn L8b giữ pin. Chỉ ba file máy đổi, GET trước/sau khớp, không restart. Lượt rà chữ H5 đầu quá rộng bắt tên bản lưu trữ; đã giữ kết quả và kiểm lại đúng ngữ cảnh, không đổi dữ liệu theo guard sai.
4. Dữ liệu/API đã đạt; chưa có ảnh/bấm UI bản 3 do browser access host unavailable và công cụ từ chối quyền Chrome. Không dùng ảnh bản 2 để xác nhận bản 3. URL/phần cần Minh chụp ở l11b/ANH-CAN-CHUP.md; ảnh 009 đã ghim. Chờ Claude kiểm và Minh quyết nghiệm thu, không khép T-064/RQ5/P10. S2–S4 và OPEN trước giữ nguyên. Không còn bất đồng nguồn đang xin giải quyết; đính chính L11b đã giải quyết điểm dừng.

Bước tiếp chính xác: đọc results/T-065/kiem/010-chi-muc-3/BAO-CAO.md và l11b/ANH-CAN-CHUP.md; Claude kiểm theo prompt dưới, Minh chụp/duyệt. Nếu cần đọc máy: SSH pin host theo results/T-058/dem-2026-11-10/remote.ps1, GET ba UID qua cơ chế không in credential. Hoàn tác chỉ khi Minh yêu cầu, theo l11b/HOAN-TAC.md; giữ mọi kết quả. Lệnh máy cuối đã chạy: python3 -B - đóng gói trong t065-l11-001; sau đó SCP nhận l11-ban-giao-001.tgz, tar giải vào may-l11 và Node kiểm 2.404 pin. Lệnh cuối chốt hồ sơ: git diff --check cho đường dẫn được phép và node_repl kiểm checksum/prefix/prompt/tập file; kết quả ở l11b/kiem-cuoi.json và manifest. Không job/tunnel/UI mới cần tiếp nhận. Đề xuất commit khi Minh duyệt: “T-065: xuất và hiển thị chỉ mục bản 3, giữ lịch sử L8b”; chưa commit/push.

#### Prompt cho Claude — L11/L11b

# Prompt bàn giao Claude — T-065 L11/L11b

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, tasks/T-065-giao-dien-grafana/; lượt L11 và L11b theo brief và đính chính 15/11/2026.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket; nhánh giao diện Grafana G-c sau G4.
- Người làm và người phản biện chính thức: Codex là người làm; Claude là người phản biện theo SPEC.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md; docs/DECISIONS.md; results/T-064/ban-xuat/chi-muc-ban.json và chi-muc-ban-2.json; results/T-064/ho-so-chon.md; docs/WHY.md; nguồn DT18 và hướng dẫn cô trong docs/reference/sources/.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md; phản hồi người làm trong REVIEW-3 và LOG L9–L11b.
- Code và kết quả liên quan: results/T-065/kiem/010-chi-muc-3/; may-l11/; grafana-l11/; kiem/009-s1-anh-minh/; XONG.md; CHECKPOINT.md; thay-doi-may.md; manifest.json và codex/manifest-L11b-truoc.json. Máy exp-obs theo hướng dẫn repo; nguồn thực thi kiem/010-chi-muc-3/l11b/l11-may.py và HOAN-TAC.md; các lệnh SSH đã chạy trong LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; chưa được cấp quyền ghi bản REVIEW mới.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```



## L12 — 2026-11-15T06:19:31.742Z — tiếp nhận S2/S4/U2 và chốt hồ sơ theo M4

Codex, Windows laptop điều khiển exp-obs, vai trò người làm T-065; Claude phản biện. Intent EXECUTE: brief L12 15/11/2026 06:15Z là quyền thực hiện trong results/T-065, nối LOG và đúng dashboard hiện hành cần S2; không ghi STATE/docs/SPEC/REVIEW/T-064. Minh đã quyết tại docs/DECISIONS.md mục “M4 chiến dịch M1-FlashTicket: trả lời 9 câu hỏi”. Không thêm quyết định.

Tự soát nguồn/đầu ra trước khi mở REVIEW-5: 11649 pin manifest hiện hành và LOG khớp; ho-so-chon T-064 khớp manifest-3. Panel 5 “Trạng thái đầu ra cạnh” tồn tại ở cả RCA và phát lại, object giống nhau: true. Vì brief L12 cho phép cả trang phát lại nếu cùng panel, áp S2 cho hai dashboard; phần dẫn panel 23 trong lời giải thích phát lại phải chỉ rõ ở trang chính. Chỉ thêm description, không đổi targets/truy vấn/UID/variables/time/links hay dữ liệu. S4 lấy nguyên khối L9, chỉ nối hai file; U2 chỉ nối đính chính nguồn brief điều phối. Ảnh U1 đã có, 5 ảnh và GHI-CHU khớp SHA256SUMS; giới hạn nhận dạng URL ảnh đầu giữ theo GHI-CHU. Pin dashboard L9 đã cũ; dùng bản sau L11b, kiểm GET live trước khi ghi, lưu byte trước/sau/cách hoàn tác.

Bản đồ tác động: hai nguồn JSON mới grafana-l12 và hai file provisioning hiện hành cho S2; nối BAO-CAO L5/BAN-GIAO-L5 cho S4; nối BAO-CAO chỉ mục 3 cho U2; báo cáo L12, XONG/CHECKPOINT/thay-doi-may/prompt/manifest và hồ sơ kiểm/byte trước trong kiem/012-s2-s4-u2. Giữ manifest trước ở codex/manifest-L12-truoc.json. Phạm vi này đúng brief L12 đã duyệt. Không chạy lại M1/raw/chấm hoặc bộ API 84 slot. STOP local vắng. Lệnh SSH chỉ đọc đầu từ Node trả kết nối port 22 Permission denied, chưa thao tác máy; đang thử tuyến exec_command đã có.

### L12 — 2026-11-15T06:22:25.415Z — tự soát/ảnh và tài liệu

Đã đọc REVIEW-5 sau khi ghi tự soát: U2 đúng, đối chiếu brief L11b xác nhận điều phối soạn; nối một dòng nguồn đúng, giữ câu cũ. S4 nối nguyên văn khối L9 vào hai báo cáo, prefix nguyên byte và hash khối nối khớp nhau. Đã xem cả năm ảnh U1: bản/ca, chỉ mục 3, nguồn/hash đầu ra và cửa sổ khớp hồ sơ đã ghim; ảnh đầu có URL phát lại nhưng breadcrumb/nội dung trang chính, giữ chưa phân xử theo GHI-CHU, không suy đã bấm điều hướng. Ảnh không có bảng đủ 64 cờ; số này vẫn dựa bằng chứng dữ liệu/API L11b, không gán cho ảnh. Chưa có quyết định nghiên cứu mới. GET live trước xác nhận cả hai dashboard đúng pin sau L11b và panel/query khớp byte nguồn; STOP remote vắng, không restart. Nguồn S2 mới đã dựng, mỗi dashboard diff đúng một trường description; chưa ghi máy.

### L12 — 2026-11-15T06:24:43.578Z — ghi S2 xong, dừng kiểm nạp sau ba quan sát

Script s2-may.py apply đã GET/pin lại hai dashboard trước ghi, chỉ đổi description và ghi đúng hai file hiện hành; biên nhận wrote có hash trước/sau. Ba quan sát nạp sau đó đều chưa khớp file nên script dừng assertion, không tự restart hoặc đổi cách triển khai. Transcript giữ ở kiem/012-s2-s4-u2/ap-dung-001.jsonl. Chỉ đọc chẩn đoán tiếp để biết trường không khớp; chưa chốt nghiệm thu/G-c theo lần nạp này. Nếu cần thao tác khác brief, dừng và trình điều phối.

### L12 — 2026-11-15T06:26:42.306Z — GET sau đã khớp, không thêm ghi máy

Quan sát chỉ đọc lúc 2026-11-15T06:24:48.609905+00:00 xác nhận cả hai description đã được Grafana tự nạp, file đúng pin sau và GET khớp; diff GET trước/sau chỉ description và version. Lượt apply hết ba quan sát trước khi thấy nạp; không thử ghi lần nữa hoặc restart. Giữ thất bại này trong transcript, không gọi lượt ấy đạt. Không xác định thời điểm nạp chính xác hay cơ chế chậm. Inventory 13 file cho thấy chỉ đúng hai dashboard đổi; compose/provider/datasource/dashboard khác và thời gian khởi động/restart_count giữ. Đối chiếu đầy đủ tại kiem/012-s2-s4-u2/doi-chieu.json. Bước tiếp chốt hồ sơ theo M4 đã duyệt và điều kiện ảnh đã lưu; không cần thao tác máy khác.

### L12 — 2026-11-15T06:34:30.430Z — kết thúc task theo quyết định M4

1. **Đã làm gì.** Hoàn tất S2: description panel 5 ở RCA và phát lại giải thích V082 vẫn dùng quan hệ E1/E2/E5 bên trong lõi P7; không đổi target/query. S4 nối nguyên văn khối L9; U2 nối một dòng đính chính nguồn brief L11b là điều phối soạn, Minh chuyển. R4 ghi USER_CONFIRMED hồi tố theo M4, không thêm thao tác folder; S3 giữ OPEN. Ảnh S1 đã có và U1 đủ năm ảnh được kiểm/xem/ghim. Điều kiện lưu ảnh đã đáp ứng: ghi nhận T-065 nghiệm thu theo M4 của Minh, G-a/G-b/G-c đạt trong phạm vi bằng chứng và giới hạn đã khai. Không có quyết định nghiên cứu mới.
2. **File thay đổi.** Trong results/T-065: BAN-GIAO-L5.md; kiem/003-trinh-duyet/BAO-CAO.md; kiem/010-chi-muc-3/BAO-CAO.md chỉ nối; XONG.md và prompt-ban-giao.md cập nhật; CHECKPOINT.md/thay-doi-may.md chỉ nối; manifest.json ghim lại sau cùng, bản trước nguyên byte codex/manifest-L12-truoc.json. Mới: grafana-l12/ (hai nguồn) và kiem/012-s2-s4-u2/ (byte trước, script qua stdin, biên nhận trước/sau/lượt lỗi, kiểm/diff, báo cáo, hoàn tác). Ảnh/ghi chú/checksum 011 là đầu vào điều phối đã lưu, L12 chỉ thêm pin, không sửa byte. Nối LOG này. Trên máy chỉ hai dashboard hiện hành, đường dẫn/pin trong noi-dung-va-diff.json. Không ghi STATE/docs/SPEC/REVIEW/T-064/src; không commit/push.
3. **Kiểm và kết quả.** Trước làm: 11649 pin và LOG khớp, nguồn T-064 khớp manifest-3; checksum ảnh U1 đạt. Hai nguồn S2 diff đúng description; GET live trước đúng pin L11b. Apply ghi đúng hai file nhưng kiểm nạp ba quan sát thất bại, giữ transcript; đã dừng ghi/checkpoint. Quan sát chỉ đọc 2026-11-15T06:24:48.609905+00:00 GET khớp hai file, diff GET chỉ description/version. Inventory 13 file chỉ hai dashboard đổi, máy không restart. S4 hash sau đúng dự kiến L9; các file chỉ nối/LOG giữ prefix; prompt đúng mẫu và module kiểm manifest import được. Đã so diff bảy file local, 15 file nguồn/phạm vi cấm giữ hash; git diff --check đạt nhưng T-065/LOG chưa được theo dõi git nên phép so byte/diff no-index mới là bằng chứng chính. Tập file chi tiết ở kiem-cuoi.json/manifest.json. Sau mục này chỉ băm/chốt manifest và chạy kiểm checksum chỉ đọc; không dùng kiểm API làm ảnh/bấm thật.
4. **Điều chưa chắc, câu hỏi nguồn và bước phụ thuộc.** Task đạt phần giao diện minh họa/truy vết DT18-NV3; chưa trả lời hiệu quả độc lập phương pháp, không đóng RQ5/P10. S3 chưa phân xử ứng dụng không phát/thu nhận-định tuyến/nhãn/lưu giữ log, thiếu đúng nguồn ứng dụng/Collector/cấu hình Loki lịch sử; chưa xác lập những nguồn này có được lưu. Cơ chế mười quan sát (iii)/Start time cũ thiếu request/response và dựng hình đúng giờ; query hiện tại không tái tạo lịch sử. URL/nội dung ảnh U1 đầu khác nhau, giữ OPEN; ảnh không có bảng đủ 64 cờ hoặc chuỗi bấm, số/đích dựa dữ liệu/API L11b. P7 hash null đúng nguồn, dev chưa cấp đáp án ở phát lại, span link message chưa hỗ trợ, bookmark số cũ giữ giới hạn. Không còn bất đồng tính đúng đang xin phân xử ở gói L12; các OPEN có bằng chứng thiếu cụ thể trong BAO-CAO L12, không bị nghiệm thu hoặc dừng phản biện biến thành kết luận cơ chế. Đề xuất giữ OPEN và dừng phản biện theo M4 đã quyết; không chạy thêm để cố khép lịch sử. Không cần Minh quyết thêm để hoàn thành L12. Commit/push vẫn chưa được cấp quyền cho lượt này.

**Bước tiếp chính xác cho điều phối:** đọc results/T-065/XONG.md; results/T-065/kiem/012-s2-s4-u2/BAO-CAO.md, doi-chieu.json và kiem-cuoi.json. Điều phối cập nhật STATE theo quyền riêng. Có thể đọc bằng Get-Content -Raw -Encoding UTF8. Kiểm pin chỉ đọc bằng Node REPL: const m = await import('file:///D:/RCA-flashticket/results/T-065/kiem/012-s2-s4-u2/kiem-manifest.mjs'); await m.kiemManifest(). Không chạy lại M1/raw/chấm hay kiểm rộng phần đã đủ. Nếu Minh yêu cầu hoàn tác, đọc HOAN-TAC.md rồi kiểm STOP/pin trước; rollback chưa chạy.

**Lệnh máy cuối đã chạy:** Get-Content -Raw -Encoding UTF8 results/T-065/kiem/012-s2-s4-u2/doc-sau.py | ssh (host/identity/known_hosts đã ghim như HOAN-TAC.md) 'sudo -n python3 -B -'; kết quả doc-sau-001.json. Không có job, tunnel hoặc thao tác UI mới đang dở. **Lệnh kiểm cuối phải chạy sau khi chốt manifest:** import module kiem-manifest.mjs và await kiemManifest() chỉ đọc như trên; kết quả cuối trả trong phiên. Hồ sơ/byte giữ để tiếp nhận trên máy khác không cần lịch sử chat.

**Đề xuất nội dung commit khi Minh duyệt:** “T-065: chốt M4, bổ sung S2/S4/U2 và ghim ảnh S1/U1”. Chưa commit/push.

#### Prompt cho Claude — L12 (để Minh chọn gửi hoặc dừng)

# Prompt bàn giao Claude — T-065 L12

Để Minh chọn copy khi cần; không tự mở vòng phản biện sau quyết định M4.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, tasks/T-065-giao-dien-grafana/; lượt L12 theo brief ngày 15/11/2026.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Chiến dịch M1-FlashTicket; nhánh giao diện Grafana sau G4.
- Người làm và người phản biện chính thức: Codex là người làm; Claude là người phản biện theo SPEC.
- Tài liệu gốc: AGENTS.md; tasks/T-065-giao-dien-grafana/SPEC.md và LOG.md; results/T-065/codex/L12-brief.md; docs/DECISIONS.md; results/T-064/ho-so-chon.md; docs/WHY.md; nguồn DT18 và hướng dẫn cô trong docs/reference/sources/.
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md, REVIEW-5.md; phản hồi trong LOG T-065.
- Code và kết quả liên quan: results/T-065/kiem/012-s2-s4-u2/; grafana-l12/; kiem/009-s1-anh-minh/; kiem/011-u1-anh-minh/; XONG.md; CHECKPOINT.md; thay-doi-may.md; manifest.json và codex/manifest-L12-truoc.json. Hướng dẫn lệnh máy trong HOAN-TAC.md và LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; chưa được cấp quyền ghi bản REVIEW mới.

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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

