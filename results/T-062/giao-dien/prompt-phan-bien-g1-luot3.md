Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-062, bước G1 (giao diện G2 trên Grafana exp-obs); tasks/T-062-dem-chang-1-4/SPEC.md (dòng G1). Đề bài G1 và yêu cầu của Minh dán nguyên văn ở cuối prompt.
- Công đoạn: kiểm lại phản hồi và sửa (lượt 3; người làm đã đáp lượt 2 và đưa phương án cuối F1′, F2′, F3, F4, F5; CHƯA sửa code).
- Gói/cổng: T-062 lượt chạy chặng 1–4, bước G1 (dashboard G2). Cổng nghiên cứu gần nhất đã duyệt: G4.
- Người làm và người phản biện chính thức: Người làm G1: Claude (phiên giao diện). Phản biện lượt G1: Codex theo yêu cầu của Minh trong chat 12/11/2026.
- Tài liệu gốc: AGENTS.md; tasks/T-062-dem-chang-1-4/SPEC.md, BOI-CANH.md, LOG.md, CHECKPOINT.md; results/T-061/dinh-dang-ket-qua-rca.md; results/T-059/danh-muc-loi.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md. Commit gốc c3d27f8a; results/T-062/giao-dien/ chưa commit.
- Phản biện và phản hồi trước: tasks/T-062-dem-chang-1-4/REVIEW-G1.md (lượt 1) và REVIEW-G1-2.md (lượt 2), mỗi bản có bảng phản hồi của người làm ở cuối; results/T-062/giao-dien/phan-hoi-g1.md (§1 tự soát, §2 phương án lượt 1, §3 phản hồi lượt 2 và phương án cuối).
- Code và kết quả liên quan: results/T-062/giao-dien/ (dung-dashboard.py, chi-muc-phat-lai.py, chi-muc-chinh.py, grafana/dashboards/*.json, thay-doi.md, XONG.md); results/T-062/e2.py; results/T-062/ket-qua/. Bản triển khai: exp-obs:/opt/flash-ticket-obs/pinned/provisioning/dashboards/ (hash trong thay-doi.md). Sinh lại dashboard: cd results/T-062/giao-dien && py -3 -B dung-dashboard.py.
- Phạm vi ghi được Minh cho phép trong lượt này: bạn KHÔNG tự ghi file nào. Lượt này chạy bằng `codex exec -o tasks/T-062-dem-chang-1-4/REVIEW-G1-3.md`; câu trả lời cuối của bạn được lưu nguyên văn thành bản lượt 3, nên viết theo khung tasks/_MAU/REVIEW.md, giữ bảng "Phản hồi của người làm" trống ở cuối. Được chạy lệnh chỉ đọc, kể cả SSH chỉ đọc tới exp-obs như lượt 1. Không thay đổi exp-obs, exp-app, máy tải; không chạm máy 84; không đọc grafana.env, file mật khẩu, sổ tiêm lỗi.

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

=== VIỆC CẦN CHỐT TRONG LƯỢT NÀY ===
Theo yêu cầu của Minh (nguyên văn bên dưới), người làm chỉ sửa khi hai bên không còn bất đồng. Với từng điểm còn mở của lượt 2 (R3, điều kiện F1/F2) và từng phương án cuối F1′, F2′, F3, F4, F5 trong results/T-062/giao-dien/phan-hoi-g1.md §3, ghi rõ: đồng ý / đồng ý có điều kiện (nêu điều kiện cụ thể) / không đồng ý (nêu lý do và phương án thay). Cuối bản, ghi một danh sách "ĐÃ CHỐT, được sửa" và một danh sách "CÒN BẤT ĐỒNG" (mỗi mục kèm phương án sửa của từng bên).

=== YÊU CẦU CỦA MINH CHO LƯỢT PHẢN BIỆN NÀY (chat 12/11/2026, nguyên văn) ===
“tôi cho phép bạn sử dụng codex để làm và phản biện cần thiết, vì tôi đan treo máy nên hãy tận dụng codex tối đa, tuân thủ các rule của dự án, nếu 2 bên có bất đồng thì ghi nhận bất đồng và phương án sửa sau khi 2 bên đã chốt, nếu 2 bên không còn bất đồng nào thì mới duyệt sửa, yêu cầu codex kiểm về tính đúng đắn, mức độ ảnh hưởng, có ảnh hưởng đến kế hoạch dài hạn và có ảnh hưởng đến production, main, demo trên máy 84 hay không , codex hết usage thì dừng chờ khi usage khôi phục”
Theo đó, mỗi điểm ghi thêm: mức độ ảnh hưởng; có ảnh hưởng tới kế hoạch dài hạn (docs/techstack/, MRP) không; có ảnh hưởng tới production, nhánh main hoặc demo trên máy 84 không. Trong mục kết luận, trả lời riêng ba câu này cho toàn bộ đầu ra G1.

=== ĐỀ BÀI G1 (nguyên văn, phiên điều phối giao) ===
Repo `D:\RCA-flashticket` là đồ án RCA (tìm nguyên nhân gốc sự cố) của Minh trên hệ FlashTicket. Task T-062 là lượt chạy qua đêm Minh đã duyệt (xem `tasks/T-062-dem-chang-1-4/SPEC.md`). Phiên điều phối Claude giữ máy `exp-app` (FlashTicket, bộ tiêm lỗi), Codex giữ máy tải k6. Phiên này là phiên giao diện G1, người duy nhất được thay đổi Grafana trên `exp-obs` đêm nay. Kết quả M1 thật của T-062 sẽ đổ dần vào `/opt/flash-ticket-obs/rca-ket-qua/` (định dạng 0.2 của T-061, kèm file chỉ mục danh sách sự cố) do phiên điều phối đẩy lên; hiện chưa có, nên dựng giao diện trên dữ liệu mẫu T-061 trước. Minh muốn sáng dậy có giao diện đầy đủ, trực quan, dễ dùng, nhãn dễ hiểu (ghét nhãn khó hiểu như "không cờ").

Task:
Bạn là phiên giao diện G1 của T-062. Đọc trước: `AGENTS.md`; `tasks/T-062-dem-chang-1-4/SPEC.md` (mục "Luật cứng của lượt", bảng máy, bước G1); `tasks/T-062-dem-chang-1-4/BOI-CANH.md` (mục "Lớp thao tác và LLM" có quy ước nhãn); `results/T-061/dinh-dang-ket-qua-rca.md`; `results/T-061/exp-obs/README.md` (Infinity 4.1.6 đã cài, nguồn `infinity-rca`, cách vào Grafana và dashboard thử "T-061 thử Infinity"); `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` nhánh G (G2).

Mục tiêu: dashboard G2 trên Grafana `exp-obs` (provisioning trong `pinned/provisioning/dashboards/` của stack quan sát) để Minh thử RCA:
1. Trang chính: danh sách sự cố (từ file chỉ mục trong `rca-ket-qua/`), chọn một sự cố bằng biến dashboard.
2. Đồ thị dịch vụ (Node graph): nhãn dễ hiểu, kích thước nút cố định. Đỏ "#hạng / nghi là nguồn", cam "#hạng / bị kéo theo", xám "(trống) / bình thường", tím "? / thiếu dữ liệu". Mã lớp M1 và điểm `e` chỉ trong chi tiết.
3. Bảng hạng service, bảng bằng chứng của service đã chọn, và liên kết Explore sang Tempo/Loki/Prometheus đúng cửa sổ thời gian của sự cố.
4. Lớp thao tác (hướng 1 trong BOI-CANH: cạnh cha–con quan sát được, panel thao tác theo service đã chọn) nếu kịp.
5. Trang phát lại có đáp án tách riêng (đọc thư mục `.../rca-ket-qua/phat-lai/`); trang chính không bao giờ hiện đáp án.
Dữ liệu: nếu chưa có kết quả T-062, dùng dữ liệu mẫu T-061 (chép bản sao vào một thư mục con mẫu, không sửa file cũ) và thiết kế sao cho file mới thả vào là hiện. Ghi rõ định dạng file chỉ mục bạn đọc vào `results/T-062/giao-dien/dinh-dang-chi-muc.md` để phiên điều phối sinh đúng; nếu T-061 đã định nghĩa chỉ mục thì theo đó.

Quyền và giới hạn: chỉ được thay đổi Grafana `exp-obs` (provisioning dashboards, thư mục `rca-ket-qua` mẫu/phát lại) và ghi trong `results/T-062/giao-dien/`. Không đụng `exp-app`, máy tải, Prometheus/Loki/Tempo/collector, repo FlashTicket, `src/`, `docs/`, `results/T-0xx/` khác. `docker compose` trên exp-obs phải có `-p flash-ticket-obs-pinned`; sửa provisioning gắn bind mount phải `docker restart` Grafana; Node graph cần 10–20 s để bố cục. Trên exp-obs có thư mục `/opt/rca-tai` và có thể có container `rca-tai-*` (k6 dự phòng của Codex): không đụng. Mọi thay đổi trên máy ghi vào `results/T-062/giao-dien/thay-doi.md` (lệnh, giờ UTC). Không in mật khẩu. Nếu tồn tại `D:/RCA-overnight/STOP` thì dừng.

Xong khi: Minh mở được qua đường hầm SSH, đổi ca được, các panel trên chạy; có ảnh chụp (`results/T-062/giao-dien/anh/`) và `results/T-062/giao-dien/XONG.md` gồm: cách mở (lệnh đường hầm, URL, tên dashboard), panel nào làm/chưa làm, định dạng chỉ mục, giới hạn đã biết. Dòng đầu XONG.md: `G1 XONG` hoặc `G1 XONG MỘT PHẦN`.

=== YÊU CẦU BỔ SUNG (nguyên văn, phiên điều phối gửi sau khi có ca thật đầu tiên) ===
Đã có kết quả M1 thật đầu tiên của T-062 trên exp-obs: kiểm lại dashboard G2 với dữ liệu thật. Phiên điều phối đã đẩy `rca-ket-qua/a5539fba.json` và `rca-ket-qua/chi-muc/danh-sach-su-co.json` (bằng `results/T-062/e2.py`, chỉ mục cùng trường T-061). Một ca mới sẽ được đẩy khoảng mỗi 31 phút tới ~01:20Z (tổng 9 ca), qua `results/T-062/chay/theo-doi-e2.sh`. Bản phát lại (`phat-lai/`) chỉ đẩy khi hết đợt; khối `phat_lai` có thêm `o_loi`, `root_khai_truoc`, `tap_chap_nhan`, `hang_trong_tap`, `hang_tot_nhat` ngoài các trường T-061 (`thanh_phan_tiem` = phần tử đầu tập chấp nhận, `ho_loi` có kèm root). Việc nhờ: trên bản thử Grafana của bạn, xem ca a5539fba có hiển thị đúng không (danh sách, đồ thị, hạng, bằng chứng, liên kết Explore đúng cửa sổ 2026-11-11 20:44:36–20:54:36Z ± nền), sửa dashboard nếu cần, chụp ảnh mới vào `results/T-062/giao-dien/anh/` và cập nhật `XONG.md`. Phạm vi ghi như cũ (chỉ Grafana exp-obs và `results/T-062/giao-dien/`); không đụng `rca-ket-qua/` chính (phiên điều phối ghi).
