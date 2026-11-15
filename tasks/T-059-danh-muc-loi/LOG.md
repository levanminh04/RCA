# Nhật ký T-059

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối.

Minh duyệt SPEC ngày 11/11/2026 (chat: "t59 codex làm, t61 claude làm, ... nếu không có bất đồng quản điểm thì duyệt ghi"). SPEC do Claude ghi theo lời duyệt, sau hai lượt phản biện SPEC của Codex và một lượt đáp của Claude trong chat.

## Phiên 1 — 11/11/2026 — Codex — Windows — Người làm

- Mở phiên theo lệnh triển khai đã duyệt của Minh. Đã đọc AGENTS, STATE, toàn bộ SPEC và mục cuối LOG. Kiểm Git: T-059 có SPEC và LOG, chưa có `results/T-059`; giữ nguyên thay đổi có trước và phần T-061 do Claude làm.
- Tự rà trước khi lập bảng: DT18-NV1/NV2/NV3 và hướng dẫn cô yêu cầu áp dụng sau thực nghiệm công khai, kiểm cả phát hiện và chẩn đoán khi tải đổi. RQ5/D.9/B1.9 cần bảng khai trước để chia ô và tạo nhãn độc lập. Việc 2i cần biết tuyến nào phải qua proxy, hook nằm ở đâu và điều kiện nào mới giao được cho B4. SPEC câu 1–2, 7 bao phủ vị trí, cơ chế và bằng chứng can thiệp; câu 3–4 nối R-01–R-10/KP với yêu cầu code; câu 5–6 khai nhãn, pha và chia theo ô. Phần phải đo sau là tác động, khả năng phân biệt của RCA, thời gian cảnh báo/hồi phục, chất lượng dữ liệu và kết quả ba bản B1.9. Tiêu chí Minh duyệt còn ở bước bàn giao.
- Đối chiếu văn bản: chặng 1c trong kế hoạch còn ghi “Claude soạn” và “phụ thuộc điểm M7”. SPEC đã duyệt và lệnh Minh 11/11 giao Codex thực hiện, dùng mặc định chia theo ô của MRP §4/WHY-04/D.9. M7 là ngoại lệ OPEN. Các đoạn đầu của D.9 về pool/mất DB phải đọc cùng đoạn ngay dưới bảng yêu cầu tách pool, DB và đường mạng. Không thấy xung đột buộc sửa SPEC. Triển khai các phần đủ căn cứ ngay trong phiên.
- Toàn vẹn: R-01–R-10 khớp SHA-256 và byte theo T-040 /files. Manifest lượt đêm T-058 khớp 203/203 mục, gồm hai mục giữ tại thư mục out của lượt gốc. Sổ KP cập nhật ngoài snapshot đã băm được đọc để tra cứu. Kết luận dùng bằng chứng đã băm, mã hoặc kiểm trực tiếp; phần KP chưa đối chứng tại T-059 giữ giới hạn bằng chứng. Dùng SSH đã ghim chỉ đọc hai máy Oracle; nối ID image đang chạy với build manifest và mở từng commit tại repo FlashTicket.

### Kết quả và tự kiểm

1. **Đã làm.** Hoàn thành bản định nghĩa chặng 1c cho 11 kịch bản D.9. Có 17 ô lỗi và một đối chứng khỏe. Phân bổ đề xuất gồm 5 ô lỗi phát triển, 12 ô lỗi đánh giá, cùng hai hồ sơ của đối chứng khỏe tách theo đợt. Tách pool Booking, mất booking_db tại đích và trễ đường JDBC. Hai thao tác VNPay refund/query cùng một vị trí Payment→VNPay; tạo URL và nhận IPN thuộc đường khác. Đã đọc bản 2i theo luồng người triển khai: file/điểm móc, thao tác, cấu hình, đầu dò và kết quả chấp nhận cho từng mục A–E.
2. **Tập file.** Thêm ba tệp `results/T-059/{danh-muc-loi.md,danh-muc-loi.json,yeu-cau-code-nhom.md}`, nối LOG này, cập nhật đúng dòng T-059 trong STATE. SPEC giữ nguyên. Lần cập nhật STATE đọc lại bản mới nhất và đối chiếu mọi dòng còn lại bằng byte. Không ghi repo hệ thống hoặc máy thí nghiệm.
3. **Kiểm.** R-01–R-10 khớp manifest T-040. 203/203 đầu ra manifest lượt đêm T-058 khớp byte/SHA-256, hai mục khớp ở thư mục out gốc. `docker inspect` đối chiếu 8 image ID trên exp-app với build manifest và đọc Git blob theo commit từng service. `curl` GET Prometheus `/api/v1/status/config`, `/api/v1/targets`, `/api/v1/rules`: scrape 10s, self up, evaluation mặc định 1m, chưa có rule Prometheus. `query_range` trong 360s bước 5s dùng `timestamp()` trên các chuỗi JVM/docker stats, đếm 37 mốc nguồn/chuỗi đại diện, cách khoảng 10s. Grafana API provisioning GET trả 401 khi không có auth. Kiểm filelog include với LogPath trên 5 service thấy khớp ở thời điểm đọc. Python so từng ô/nhãn/trạng thái/điều kiện giữa MD và JSON, kiểm đủ 11 kịch bản, 18 dòng, khóa chia không trùng và root null duy nhất, 39 dẫn chiếu Git đúng path/dòng, và đủ ô trong giao việc 2i. Khi kiểm phát hiện một khoảng dòng compose dài hơn file một dòng; đã sửa cả hai bản và chạy lại. Đã đọc toàn bộ phần thêm và đối chiếu diff của từng file. Lệnh kiểm cuối: `git diff --check -- docs/STATE.md`, `git diff --unified=0 -- docs/STATE.md` và `git status --short --untracked-files=all -- docs/STATE.md tasks/T-059-danh-muc-loi results/T-059`.
4. **Còn OPEN và hệ quả.** Chưa có phép xác nhận can thiệp trong T-059. 2i cần làm cấu hình proxy, hook, mock và tải; cần chứng minh riêng tuyến JDBC/Redis, DB đích cô lập, fixture thanh toán–phát vé–hoàn tiền, terminal FAILED có bù trừ, mạng/CPU cô lập trên ARM, liveness độc lập và độ phủ log/trace/metric ở tải dự kiến. B4 cần đầu dò, sổ, nền, luật cảnh báo và ngưỡng tải khỏe. Pha 10+10+10 phút là ứng viên dựa trên cadence đo được và cửa sổ M1; thời lượng thực phụ thuộc luật Grafana, độ trễ có tác động, hồi phục và drain. T-059 chưa cho số ô hữu hiệu, kết quả RQ5, chi phí phát triển hoặc nghiệm thu B4. M7 vẫn OPEN.

### Bước tiếp theo

Minh chuyển prompt bên dưới cho Claude. Claude đọc AGENTS, SPEC, các nguồn gốc và ba đầu ra để phản biện độc lập. Khi xử lý phản biện, người làm đọc nguồn/đầu ra trước, kiểm từng ý theo AGENTS §9. Sau khi Minh duyệt bảng và giao 2i, B4 đối chiếu revision/digest của bản thử, bằng chứng baseline đúng tuyến và các điều kiện xác nhận từng ô. Các điểm cần đưa vào quyển khi có dữ liệu gồm cách chia theo vị trí, vùng ảnh hưởng endpoint, phạm vi cạnh/nút, ảnh hưởng tài nguyên chung và điều kiện phân biệt tải tăng khỏe với suy giảm thật.

Nội dung commit đề xuất khi Minh yêu cầu sau phản biện: `docs(T-059): define FlashTicket fault catalog and 2i requirements`.

### Prompt phản biện để Minh chuyển cho Claude

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-059, `tasks/T-059-danh-muc-loi/SPEC.md`.
- Công đoạn: soát kết quả.
- Gói/cổng: P10, chặng 1c, chưa có cổng riêng.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: `docs/KE-HOACH-GIAI-DOAN-TOI.md` D.1/D.9/D.11, `docs/techstack/PLAN-TRIEN-KHAI.md` §5/§7, `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` chặng 1c, `docs/techstack/VIEC-CHO-QUYET-VA-LAM.md`, `tasks/T-043-thiet-ke-rca-m1/SPEC.md` B1.9, `results/T-040/yeu-cau-quan-sat-p9.md`, `results/T-058/so-khac-phuc.md`. RCA HEAD `c3d27f8a8f8bf38a5bbad65522d2f6aff7189cb4`, xem `git status`, `git diff -- docs/STATE.md` và các tệp mới của task.
- Phản biện và phản hồi trước: hai lượt soát SPEC và lượt đáp trong chat 11/11/2026, ghi nguồn ở SPEC/LOG. Chưa có phản biện kết quả.
- Code và kết quả liên quan: `results/T-059/danh-muc-loi.md`, `results/T-059/danh-muc-loi.json`, `results/T-059/yeu-cau-code-nhom.md`; `results/T-040/manifest.json`, `results/T-058/dem-2026-11-10/artifacts-sha256.json` và `build-manifest.json`. Repo FlashTicket `D:/Project/flash-ticket-platform`, checkout `1d40c97076db402d3e0d529a3b48523d37837240`, revision triển khai theo build manifest và bảng mã.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa duyệt riêng đường dẫn bản phản biện.

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
```

## Phiên 2 — 11/11/2026 — Codex — Windows — Người làm

- Mở lượt sửa sau khi đọc AGENTS, STATE, SPEC, LOG và hai nội dung Minh chuyển. Minh duyệt sửa có điều kiện nếu hai bên hết bất đồng. Đồng ý với Claude lượt 2 về gói danh mục mức service. Claude rút phản đối D9-04 vì chỉ Ticket nhận `ticket.issue.v1`. Bổ sung điểm thiếu trong lần đáp trước về ngưỡng backend, nhóm cảnh báo 429, phạm vi tải chung và chữ STATE trong mục 9 của mẫu prompt mới.
- **Quyết định đã ghi.** D.9 và WHY-80: Event→event_db phát triển, Booking→booking_db đánh giá. Proxy Event giữ trong mọi ô/pha, đêm nền và đối chứng. POOL-EVENT là CANDIDATE riêng; TICKET-PAUSE chỉ đánh giá. Nhãn root chiếu từ vị trí tiêm và kết quả xác nhận; giữ riêng đáp án telemetry có thể phân biệt. Khai hỗn hợp chung, ưu tiên luồng đặc thù nhịp thấp. Nếu cần hồ sơ riêng thì ghép đối chứng cùng lịch và báo giới hạn rò rỉ. Quota giữ có điều kiện, ngưỡng backend bằng số phải khóa trước lượt chấm, mọi cảnh báo ở ca bị giới hạn vẫn xuất báo cáo riêng. So hai mức tải trong một tập ô đánh giá khai trước, tính thêm lượt vào dự toán.
- **File.** Nối `docs/DECISIONS.md`, `docs/WHY.md`; đồng bộ hai dòng, chú thích nhãn và chú thích dự toán ở D.9 trong `docs/KE-HOACH-GIAI-DOAN-TOI.md`. Sửa ba đầu ra trong `results/T-059/`; nối LOG và cập nhật riêng dòng T-059 trong STATE. SPEC và đầu ra T-061 ở ngoài gói sửa.
- **Tự kiểm.** R-01–R-10 và 203 mục manifest T-058 khớp SHA-256 và byte. MD/JSON khớp 11 kịch bản, 18 ô lỗi (6 phát triển, 12 đánh giá), 1 đối chứng khỏe, 1 ứng viên pool ngoài bảng chia, 40 dẫn chiếu file/dòng Git theo revision. Kiểm mỗi ô có điều kiện xác nhận độc lập, khả năng phân biệt để OPEN, và yêu cầu 2i tương ứng. Rà diff và tập file. Lệnh kiểm bàn giao: `git diff --check -- docs/DECISIONS.md docs/WHY.md docs/KE-HOACH-GIAI-DOAN-TOI.md docs/STATE.md` và `git status --short --untracked-files=all -- docs/STATE.md tasks/T-059-danh-muc-loi results/T-059`.
- **OPEN.** Quyền ghi này áp cho bản định nghĩa mức service. P59-1 là đề xuất riêng về chấm mức thao tác. Vị trí trong code, span ứng viên và nhãn thao tác cần phân biệt. Cạnh client quan sát được không tự xác định root ở thao tác. Chưa khóa schema nhãn thao tác. B4 còn cần xác nhận image/config quota, ngưỡng và khoảng đo backend, fixture và lịch tải, mức tải và số lượt, hiệu lực và quan sát từng can thiệp. M7 còn OPEN. Chưa nghiệm thu bảng hoặc B4.
- **Bước tiếp theo.** Minh có thể chuyển prompt để Claude kiểm bản đã ghi, rồi duyệt bảng mức service. Sau đó dùng bản giao việc 2i và các điều kiện B4 trong danh mục. Đề xuất nội dung commit nếu Minh yêu cầu sau kiểm: `docs(T-059): refine fault split and workload controls after review`.

### Prompt để Minh chuyển Claude kiểm bản sửa T-059

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-059, `tasks/T-059-danh-muc-loi/SPEC.md`.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P10, chặng 1c, chưa có cổng riêng.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: `docs/KE-HOACH-GIAI-DOAN-TOI.md` D.1/D.9/D.11, `docs/techstack/PLAN-TRIEN-KHAI.md` §5/§7, `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` chặng 1c, `tasks/T-043-thiet-ke-rca-m1/SPEC.md` B1.9, `docs/DECISIONS.md` và `docs/WHY.md`. RCA HEAD `c3d27f8a8f8bf38a5bbad65522d2f6aff7189cb4`, xem diff các file docs và tệp mới trong task.
- Phản biện và phản hồi trước: phản biện Claude lượt 1, phản hồi Codex, kiểm lại Claude lượt 2 và lời duyệt sửa của Minh trong chat. Minh chuyển kèm nếu cần.
- Code và kết quả liên quan: `results/T-059/danh-muc-loi.md`, `danh-muc-loi.json`, `yeu-cau-code-nhom.md`, `results/T-040/manifest.json`, `results/T-058/dem-2026-11-10/artifacts-sha256.json` và `build-manifest.json`. FlashTicket `D:/Project/flash-ticket-platform`, checkout `1d40c97076db402d3e0d529a3b48523d37837240`, mã theo bảng revision. Gateway theo BOM của `infrastructure/api-gateway/pom.xml` ở revision triển khai.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat nếu Minh chưa duyệt riêng đường dẫn bản phản biện.

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
```

## Phiên 3 — 11/11/2026 — Codex — Windows — Người làm

- **Quyền và kết luận.** Minh cho phép ghi nếu phần Claude đề xuất chỉ bổ sung cho chấm mức thao tác, M1 xếp hạng service không cần và hai bên không còn bất đồng. Đối chiếu đề xuất P59-1 đã sửa với SPEC T-059, điểm cách ly PLAN §5 và `src/m1/chuoi.py::chay`. Codex đồng ý với Claude: ứng viên ở phía bộ chấm, không là đầu vào M1 hoặc điều kiện cho hiển thị hướng 1. M1 vẫn sử dụng tín hiệu thao tác đo từ telemetry trong phép tính mức service. Lời duyệt ghi ứng viên không phải quyết định thực hiện hướng 2.
- **Đã bổ sung.** `results/T-059/danh-muc-loi.md` và `results/T-059/danh-muc-loi.json` thêm P59-1. Ghi bốn hook HTTP và hook terminal `TicketService.issue` ở CANDIDATE, chờ B4 ánh xạ span. Với Saga, xác minh lệnh phát vé và phân biệt span listener với span nghiệp vụ. Lỗi tuyến giữ root cạnh. Cgroup, pause, DB đích và pool không định nghĩa thao tác gốc theo cách đặt ô. POOL-EVENT là ứng viên ngoài bảng chia. FLASH-HEALTHY là đối chứng, áp dụng root null khi xác nhận khỏe.
- **Tự kiểm.** Bỏ phần P59-1 khỏi MD/JSON thu đúng nội dung cũ, cả byte và cấu trúc JSON. So đủ 19 dòng cùng POOL-EVENT riêng, ứng viên đều chưa có nhãn xác minh. Kiểm chữ ký đầu vào M1 và tìm dẫn chiếu danh mục trong code M1/adapter. Không cần chạy lại M1 cho thay đổi tài liệu. Kiểm diff, tập file và mục prompt. Ba file ghi trong lượt là hai bản danh mục và LOG này. T-061 C/D là gói sửa hợp đồng giao diện riêng; không xử lý trong quyền ghi P59-1.
- **OPEN và bước tiếp.** Nếu Minh chọn chấm mức thao tác, B4 dùng bằng chứng độc lập nối hook với request/message, xác minh span theo revision và khóa quy tắc nhãn trước lượt chấm. Trạng thái duyệt bảng T-059 vẫn là chờ Claude kiểm bản ghi và Minh duyệt. Minh có thể chuyển prompt dưới đây để Claude kiểm cả bản mức service và P59-1. Lệnh cuối kiểm: `git diff --check` trên tài liệu liên quan và `git status --short --untracked-files=all -- results/T-059 tasks/T-059-danh-muc-loi`. Nội dung commit đề xuất nếu Minh yêu cầu sau kiểm: `docs(T-059): record optional operation scoring candidates`.

### Prompt để Minh chuyển Claude kiểm phần P59-1 đã ghi

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-059, `tasks/T-059-danh-muc-loi/SPEC.md`, bản sửa mức service và phần P59-1 trong danh mục.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P10, chặng 1c, chưa có cổng riêng.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: `docs/KE-HOACH-GIAI-DOAN-TOI.md` D.9/D.11, `docs/techstack/PLAN-TRIEN-KHAI.md` §5, `tasks/T-043-thiet-ke-rca-m1/SPEC.md` B1.9, SPEC/LOG T-059. Xem Git diff các tài liệu và nội dung các tệp mới của task.
- Phản biện và phản hồi trước: phản biện và đáp các lượt trước theo LOG; Claude sửa P59-1 và lời duyệt có điều kiện của Minh trong chat do Minh chuyển kèm.
- Code và kết quả liên quan: `results/T-059/danh-muc-loi.md`, `danh-muc-loi.json`, `yeu-cau-code-nhom.md`, `src/m1/chuoi.py`, `src/m1/hop_dong.py`. Revision FlashTicket theo bảng mã và `results/T-058/dem-2026-11-10/build-manifest.json`.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat nếu Minh chưa duyệt riêng đường dẫn bản phản biện.

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
```
