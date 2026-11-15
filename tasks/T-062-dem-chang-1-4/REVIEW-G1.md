# Phản biện T-062 — G1

- **Người phản biện:** Codex — **Ngày:** 12/11/2026.
- **Công đoạn:** soát kết quả G1, giao diện G2 trên Grafana `exp-obs`; cổng nghiên cứu gần nhất G4.
- **Bản lượt:** câu trả lời này, theo đường dẫn đích `tasks/T-062-dem-chang-1-4/REVIEW-G1.md` được prompt chỉ định. Tôi không tự ghi file.
- **Commit/diff:** mốc `c3d27f8a`; đầu ra G1 chưa được Git theo dõi.
- **Đã đọc:** AGENTS, STATE, SPEC/BOI-CANH/LOG/CHECKPOINT/PROMPT-DIEU-PHOI của T-062; nguồn DT18 và hướng dẫn của cô; phần liên quan trong MRP/WHY/DECISIONS/LESSONS và kế hoạch giai đoạn 2; định dạng T-061; code, JSON dashboard, chỉ mục, báo cáo, nhật ký triển khai và ảnh G1; code E2.
- **Tự soát độc lập:** đọc nguồn và code gốc, kiểm manifest, đối chiếu bản triển khai và dữ liệu thật trước khi kết luận. Chưa có lượt phản biện trước.

## Kết luận chung

**G1 đạt một phần; chưa nên nghiệm thu trang phát lại T-062 là biểu diễn đúng đáp án.** Có một mâu thuẫn thiết kế cần xử lý ở cách gọi đáp án cạnh, và một lỗi số liệu nhỏ trong mô tả đồ thị. Phần xem trực tiếp trên Grafana thật vẫn chưa được xác minh; `XONG.md` đã khai đúng giới hạn này.

Ba câu trả lời theo yêu cầu của Minh:

1. **Tính đúng và mức ảnh hưởng:** trang chính, dữ liệu M1 và hạng không bị hai điểm dưới làm thay đổi. R1 ảnh hưởng cách người xem hiểu vị trí tiêm và kết quả phát lại; R2 ảnh hưởng mô tả mức quan sát của đồ thị.
2. **Kế hoạch dài hạn:** cần giữ đúng phân biệt root cạnh và tập chấp nhận đã duyệt ở T-059. Hai điểm này không đòi đổi MRP, thuật toán M1 hoặc hướng triển khai Grafana.
3. **Production, main và demo máy 84:** không thấy đường tác động trực tiếp từ thay đổi G1 đã kiểm. Dashboard nằm trên `exp-obs`; hash compose và datasources vẫn khớp bản sau T-061. Tôi không truy cập máy 84, không sửa hoặc push nhánh nào. Kết luận này chỉ bao phủ G1, không xác nhận các bước khác của T-062.

## Các điểm

### R1. Trang phát lại gọi một đầu cạnh là “thành phần bị tiêm” — CHẶN nghiệm thu phần đáp án T-062

- **Ở đâu:** [dung-dashboard.py:267](/D:/RCA-flashticket/results/T-062/giao-dien/dung-dashboard.py:267), dòng 302 và 350; [chi-muc-phat-lai.py:36](/D:/RCA-flashticket/results/T-062/giao-dien/chi-muc-phat-lai.py:36).
- **Sai gì:** giao diện coi `phat_lai.thanh_phan_tiem` là đáp án duy nhất. Với T-062, trường này chỉ là phần tử đầu của tập chấp nhận, không nhất thiết là vị trí tiêm thật.

**Bằng chứng:**

- [e2.py:125](/D:/RCA-flashticket/results/T-062/e2.py:125) gán `thanh_phan_tiem = accept[0]`, đồng thời giữ riêng `root_khai_truoc`, `tap_chap_nhan`, `hang_trong_tap`, `hang_tot_nhat`.
- T-059 quy định root của ô tiêm trên tuyến là **cạnh có hướng và loại**. Chẳng hạn `EVENT-DB-LAT`: root là `event-service → event_db (data)`; tập chấp nhận mức nút gồm hai đầu cạnh.
- Dashboard lại đánh dấu đầu tiên bằng “◆ ĐÁP ÁN”, gọi nó là “thành phần bị tiêm”, và ghi “không phải” ở các nút khác. Chỉ mục cũng lấy vai trò/hạng của riêng đầu tiên dưới tên “M1 xếp đáp án là”.

**Phần có thể phản bác finding:** `ho_loi` và `nhan_xet` của E2 vẫn chứa root cạnh và thông tin tập chấp nhận. `XONG.md` cũng đã khai chưa hiện đầy đủ tập này. Vì vậy đây không phải mất toàn bộ đáp án. Tuy nhiên, các nhãn khẳng định trên đồ thị và bảng vẫn mâu thuẫn với nghĩa của dữ liệu nguồn.

- **Bước và quyết định chịu ảnh hưởng:** mâu thuẫn thiết kế đã có trong code; chưa xác nhận biểu hiện trên bản phát lại thật vì tại lúc kiểm thư mục phát lại T-062 chưa có. Chặn kết luận rằng trang phát lại diễn đạt đúng vị trí tiêm và kết quả định vị cạnh. Không chặn dùng trang chính để xem dự đoán.
- **Mức ảnh hưởng:** trung bình, tập trung ở diễn giải phát lại. Không làm đổi hạng hay file kết quả M1.
- **Ảnh hưởng dài hạn:** cần giữ phân biệt root cạnh, tập chấp nhận mức nút và kết quả định vị cạnh của T-059; không cần đổi thiết kế nghiên cứu.
- **Production/main/máy 84:** không có tác động trực tiếp từ lỗi hiển thị này.

**Đề xuất sửa tối thiểu:** với bản T-062, hiện root khai trước bằng chữ; ghi rõ hai đầu thuộc “tập chấp nhận mức nút”, không gọi riêng đầu tiên là vị trí bị tiêm và không loại đầu còn lại bằng “không phải”. Nếu hiện hạng, phân biệt hạng từng đầu với hạng tốt nhất trong tập. Giữ cách đọc cũ cho mẫu T-061 không có các trường mới.

Phương án này tận dụng dữ liệu E2 đã có và không thêm cạnh giả vào đồ thị M1. Mặt trái là cần cập nhật hợp đồng chỉ mục và các chỗ hiển thị liên quan. Phương án nhỏ hơn là tạm bỏ dấu đáp án trên nút đối với root cạnh, chỉ hiện root/tập chấp nhận bằng chữ.

### R2. Mô tả đồ thị ghi cố định 10 nút không có cạnh — KHÔNG CHẶN

- **Ở đâu:** [dung-dashboard.py:336](/D:/RCA-flashticket/results/T-062/giao-dien/dung-dashboard.py:336).
- **Sai gì:** mô tả panel khẳng định “10 thành phần hạ tầng … không có cạnh”, lấy từ hai mẫu T-061 nhưng áp dụng cho cả dữ liệu mới.

**Bằng chứng:** lệnh đếm độc lập lấy tập `nut[].id` trừ các đầu `canh[].nguon/dich` cho kết quả:

- Hai mẫu gốc T-061: mỗi mẫu có **10** nút không có cạnh.
- Chín ca T-062 hiện có: mỗi ca có **9** nút không có cạnh.
- Ca `a5539fba` đã có cạnh từ Booking/Event/Payment/Ticket tới Keycloak. Panel độ phủ và ảnh 11 hiển thị đúng **9**, trái với mô tả cố định.

- **Bước và quyết định chịu ảnh hưởng:** lỗi mô tả đã xảy ra; làm sai thông tin về mức quan sát của đồ thị. Không đổi đồ thị, hạng hoặc bằng chứng.
- **Mức ảnh hưởng:** thấp. Không chặn sử dụng dashboard.
- **Ảnh hưởng dài hạn:** chỉ cần bỏ việc khái quát số của mẫu cũ thành hạn chế cố định.
- **Production/main/máy 84:** không có tác động trực tiếp.

**Đề xuất sửa tối thiểu:** bỏ số 10 khỏi mô tả, dẫn người xem tới số đếm trong panel độ phủ. Cách này đủ sửa lỗi và ít phụ thuộc hơn việc duy trì thêm một phép đếm trong mô tả.

## Đối chiếu các lượt trước

Không có bản phản biện hoặc phản hồi trước.

## Tuân thủ quy trình

- Giữ vai trò phản biện; chỉ chạy thao tác đọc. Không ghi LOG/STATE, sửa dashboard, chạy M1, đọc sổ tiêm hoặc mở dữ liệu khóa.
- Bản dashboard triển khai khớp repo và các tiền tố hash trong `thay-doi.md`. Không phát hiện sai khác cần dừng sử dụng.
- Giới hạn “chưa xem trên Grafana thật” được báo trung thực bằng `G1 XONG MỘT PHẦN`.
- Các manifest ca/kết quả T-062 đã kiểm không ghim file G1. JSON triển khai có hash trong nhật ký; sửa chúng sẽ cần sinh lại và ghi nhận hash triển khai mới.
- Chưa có bằng chứng đủ để kết luận G1 sửa ngoài phạm vi. Tôi không kiểm toán toàn bộ hoạt động của các phiên khác.

## Điều đã kiểm và thấy đúng

- Hai dashboard sinh trong bộ nhớ trùng cấu trúc JSON đã lưu; bốn script Python phân tích cú pháp thành công.
- Ba file provisioning trên `exp-obs` khớp byte bản local. Log xác nhận nạp dashboard sau lần triển khai cuối.
- Manifest ca: **28/28** mục khớp hash và kích thước. Manifest kết quả: **9/9** file khớp. Chỉ mục chín ca khớp hash, mã, mốc và số lượng thực thể; các file chính không có khối `phat_lai`.
- Sáu file mẫu trên máy thật khớp bản G1 local; các bản sao tương ứng khớp nguồn T-061. Hai mẫu gốc đạt kiểm manifest T-061.
- Trang chính không chứa bốn mẫu truy cập đáp án mà bộ sinh cấm.
- Với `a5539fba`, cửa sổ **20:45:04–20:55:04 UTC** khớp `request.json` và cửa sổ M1 đã kiểm manifest. Không có căn cứ buộc dashboard dùng mốc 20:44:36 trong tin giao việc.
- Code và ảnh đã lưu phù hợp với quy ước màu, hạng, kích thước nút cố định và bằng chứng Keycloak. Ảnh Explore thể hiện truy vấn tương ứng.
- Lớp thao tác được ghi rõ là dữ liệu từ kho quan sát, không nhận là đầu ra xếp hạng thao tác của M1. Phần thiếu đồ thị thao tác và LLM đã được khai.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** phản biện độc lập code, nguồn, dữ liệu, ảnh và bản triển khai G1.
2. **File thay đổi:** không sửa file nào; không commit, push hoặc thay đổi máy từ xa.
3. **Kiểm đã chạy:** kiểm cú pháp, tái sinh dashboard trong bộ nhớ, hash/manifest, chỉ mục, cạnh và cửa sổ thời gian; các kết quả nêu trên đạt. API dashboard thật trả `401`; công cụ trình duyệt không có phiên khả dụng, nên chưa kiểm tương tác thật.
4. **Còn mở và đề xuất:** đề xuất người làm đáp R1/R2 trước khi sửa. Chưa có phản hồi nên chưa thể gọi là hai bên đã thống nhất. Đề xuất tiếp tục phản biện tập trung vào hai điểm này; giữ trạng thái nghiệm thu một phần.

Phần tương tác trên Grafana thật còn thiếu bằng chứng đổi ca, mở menu và Explore trong phiên đã đăng nhập. Hash và log nạp thành công chưa phân xử được giữa “chạy đúng” và “còn lỗi chỉ xuất hiện khi dùng nguồn/phiên thật”. Một lượt kiểm ngắn trên Grafana đã đăng nhập, không cần chạy lại M1, sẽ giải quyết phần này.

Chưa có căn cứ từ G1 để kết luận thêm về hiệu quả RCA, lợi ích đồ thị hoặc hoàn thành RQ5. Những câu đó cần thực nghiệm và đánh giá ở các bước tương ứng.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-062, bước G1; tasks/T-062-dem-chang-1-4/SPEC.md, dòng G1 và đề bài trong results/T-062/giao-dien/prompt-phan-bien-g1.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: giao diện G2 của T-062; cổng nghiên cứu gần nhất đã duyệt G4.
- Người làm và người phản biện chính thức: người làm G1 Claude; Codex phản biện lượt G1 theo yêu cầu Minh.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; tasks/T-062-dem-chang-1-4/SPEC.md, BOI-CANH.md, LOG.md, CHECKPOINT.md; results/T-061/dinh-dang-ket-qua-rca.md; results/T-061/exp-obs/README.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md. Mốc Git c3d27f8a; đầu ra G1 chưa commit.
- Phản biện và phản hồi trước: bản phản biện G1 trong câu trả lời Codex ngày 12/11/2026, đường dẫn đích theo lệnh CLI là tasks/T-062-dem-chang-1-4/REVIEW-G1.md; chưa có phản hồi.
- Code và kết quả liên quan: results/T-062/giao-dien/; results/T-062/e2.py; results/T-062/ket-qua/manifest-ket-qua.json; results/T-062/ca/manifest-ca.json; results/T-059/danh-muc-loi.md. Bản triển khai tại exp-obs:/opt/flash-ticket-obs/pinned/provisioning/dashboards/; môi trường và hash triển khai ở results/T-062/giao-dien/thay-doi.md.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Không sửa code, dashboard, dữ liệu, tài liệu hoặc máy từ xa. Chưa có quyền ghi bảng phản hồi hay LOG trong lượt này.

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

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN phần đáp án của trang phát lại T-062 | Kiểm lại: `results/T-062/e2.py:125` gán `thanh_phan_tiem = accept[0]`; `results/T-059/danh-muc-loi.md` (dòng 25, 48, 89) giữ root ở cạnh có hướng và loại. Dashboard (`dung-dashboard.py:222,235,268,302,350`) và `chi-muc-phat-lai.py:36–45` gọi riêng phần tử đầu là "thành phần bị tiêm" và ghi "không phải" cho phần còn lại. `e2.py:147` gọi `chi-muc-phat-lai.py`, nên chỉ mục phát lại T-062 sẽ mang lỗi này. Trùng điểm tự soát N1. Đồng ý phương án sửa tối thiểu của reviewer; chi tiết F1–F2 ở `results/T-062/giao-dien/phan-hoi-g1.md` §2 | |
| R2 | Đúng; KHÔNG CHẶN | `dung-dashboard.py:336` ghi cứng "10 thành phần hạ tầng"; `a5539fba.json` `/do_phu/thuc_the_khong_co_canh` có 9 phần tử. Đồng ý bỏ số, dẫn tới dòng Độ phủ (F3) | |
| N1 | (tự tìm trước khi đọc phản biện) trùng R1; CHẶN phần đáp án trang phát lại | `phan-hoi-g1.md` §1 | |
| N2 | (tự tìm) KHÔNG CHẶN | Cột "Có hạng / quan sát" và dòng Độ phủ ghi 17/17 "có hạng", trong khi dashboard không hiện hạng cho 16 thành phần bình thường (M1 xếp chung hạng 2, khóa 0). Đề xuất F4: đổi chữ thành "M1 trả hạng" | |
| N3 | (tự tìm) KHÔNG CHẶN | Bằng chứng span DB của keycloak không có biểu đồ trong lớp thao tác (chỉ HTTP theo route). Không sửa lượt này; đã khai ở XONG §2a | |
| N4 | (tự tìm) KHÔNG CHẶN | `public/rca` không cần đăng nhập nên `phat-lai/` đọc được trong VCN; đã khai XONG §5.7; không sửa trong G1, việc của Minh quyết | |
| N5 | (tự tìm khi kiểm R1) KHÔNG CHẶN, cần reviewer xét | `e2.py:110–112` lấy `hang` của mọi nút trong tập, kể cả nút "bình thường" (vd. a5539fba: 16 nút bình thường cùng `hang` = 2). `hang_tot_nhat` vì vậy có thể là hạng của nhóm bình thường. Đây là cách chấm của phiên điều phối, ngoài phạm vi G1; dashboard sẽ hiện hạng kèm vai trò và số đồng hạng thay vì chỉ "#2" (F1) | |
