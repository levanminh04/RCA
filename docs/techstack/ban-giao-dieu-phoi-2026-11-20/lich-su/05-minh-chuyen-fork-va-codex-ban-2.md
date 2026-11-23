# Minh chuyển: báo cáo phiên fork T-069 và phản biện Codex cho kế hoạch bản 2

> Nguyên văn, trích bằng script từ `debcb98c-9a36-447f-b07c-8820bd290ab4.jsonl` (dòng 995). Không biên tập.

phản hồi của codex như sau, bạn đọc và cho phản biện, đề xuất các phần chạy song song được, sử dụng tính tăng multi-sessions của claude để làm nhé, 1 phiên điều phối, phần nào cần tuần tự thì tuần tự, tận dụng thời gian tối đa có thể nhưng tính đúng đắn vẫn ưu tiên cao nhất, lên plan chi tiết luôn bây giờ, bạn hãy thực hiện review và soi lại plan 1 lần nữa để tránh có vấn đề gì bỏ sót rồi sau đó mới tổng hợp thông tin với codex, phản biện :
dưới đây là phản biện của codex và đề xuất của phiên phản biện t69 từ claude, cần bạn tổng hợp thông tin thành 1 plan duy nhất để tránh 2 phiên mâu thuật
"

Cấu hình ba biến thể trong bản chụp khớp manifest-3. Chạy 9 lần (3 biến thể × 3 gói) trên exp-obs, chạy nền.

Cả 9 lần chạy: bỏ H8s1 (V061), bỏ H8a (V066) hay chỉ giữ H8a (V060) đều cho cùng thực thể đứng đầu như V082 và P7. Kéo đầu ra về và chấm hạng gốc.

Bước bỏ từng thành phần đã xong: trên cả 3 gói, V082 cho cùng hạng và cùng điểm quyết định như các gói khác, nên không thành phần nào của V082 gây ra việc đổi hạng. Tiếp theo tôi sẽ kiểm tra độ phủ 17 cặp và lập lại bảng bản 2.

Bước sửa script dừng ở `assert` nên `bang_theo_o_2.py` vẫn là bản chép của bản 1, và lần chạy kế tiếp đã ghi đè các file đầu ra; vì đầu vào giống nhau nên tôi sẽ kiểm lại ngay bằng `SHA256SUMS`.

Các file bị ghi đè **trùng byte** với manifest (6/6 OK), không mất dữ liệu. Sẽ ghi sự cố này vào LOG. Sửa lại bước tạo bản 2 cho đúng chuỗi trong code.

Bản 2 cho cùng bảng và tổng; D4 tính trên mọi ca đã thu vẫn = không. Toàn bộ 318 file cũ trong `SHA256SUMS` vẫn khớp. Giờ viết `dinh-chinh-1.md`.

Kiểm số "span mồ côi tăng ở 15/17" và "số span giảm 3–10%" trước khi để trong đính chính.

Cách đọc file văn bản của tôi sai cột; tính lại thẳng từ JSON đầu ra.

Đính chính đã xong. Ghi DECISIONS và WHY: xem định dạng và số mục cuối hiện có.

DECISIONS và WHY-102 đã ghi. Giữ nguyên `SHA256SUMS` (318 file, bản đã ghim) và lập `SHA256SUMS-2` cho toàn bộ thư mục sau đính chính.

Ghi LOG phiên 3 (kèm prompt Codex kiểm lại) và cập nhật dòng STATE.

Đã sửa xong theo đề xuất được duyệt. Kết quả mới quan trọng nhất là phép bỏ từng thành phần: V061, V066 và V060 cho đúng hạng và đúng điểm quyết định như P7 và V082 trên cả 3 gói. Booking ở CPU-BOOK-1 vẫn hạng 3 ở cả lượt chính và lượt lặp, Event ở HTTP5-EVENT vẫn hạng 2. Như vậy H5b, H8s1, H8a không gây ra và cũng không sửa được việc đổi hạng; nó nằm ở lõi chung.

**Đã làm:**
- `results/T-069/dinh-chinh-1.md`: đính chính đủ R1–R7, file gốc giữ nguyên.
  - Kết luận W3 viết lại: một ô tụt vượt ngưỡng và tái lập; D1–D5 không kích hoạt; Minh quyết.
  - Đếm lại kích thước bảng đúng thời điểm từng ca: 4,8× ở CPU-BOOK-1 lượt chính, 7,2× ở lượt lặp, 6,2× ở HTTP5-EVENT (không phải ~10×).
  - "DB là nguyên nhân gốc" hạ xuống ứng viên. Các giải thích còn lại: code đường mua vé đổi, tranh chấp CPU, dao động mẫu đuôi.
  - Nêu giới hạn của phép tính lại z: chỉ đúng với kênh SQL lá.
- Độ phủ đủ 17 cặp, đếm lại từ JSON: số kênh chấm hợp lệ đổi ở 14/17 cặp, span mồ côi tăng ở 16/17.
- `bang_theo_o_2.py` sửa logic D4: bảng và tổng trùng bản 1, D4 vẫn = không.
- Ghi mục T-069 vào `docs/DECISIONS.md` (gồm quyết định B, thu lại 3 ô, phạm vi ghi thực tế); thêm WHY-102 về hai tầng tiêu chí; cập nhật LOG phiên 3 kèm prompt cho Codex kiểm lại, và dòng T-069 trong STATE.
- **Một sự cố trong lúc sửa:** lần tạo bản 2 đầu tiên lỗi giữa chừng, và lệnh kế tiếp ghi đè 6 file đầu ra của bản 1. Kiểm ngay: cả 6 trùng byte với manifest, không mất gì. Đã ghi vào LOG và đính chính. `SHA256SUMS` cũ (318 file) vẫn khớp; `SHA256SUMS-2` phủ 348 file.

**Kế hoạch tiếp theo:**
1. **Quyết W3, đang chặn W4/W5.** Đề xuất: chấp nhận ô tụt CPU-BOOK-1 làm ngoại lệ có ghi rõ, và dùng V082 cho demo.
   - Lý do: P7 và mọi biến thể đều tụt y hệt, nên không bản thay thế nào làm tốt hơn; D1–D5 không kích hoạt.
   - Mặt trái: khi ép CPU Booking, demo có thể xếp Ticket hoặc Keycloak trên Booking.
2. **Dời mốc sự kiện ở `ticket_db`, `payment_db` thêm +14 ngày,** cùng cách đã làm (dump trước, kiểm khớp 1 dòng). Phải xong trước 20/11 22:16Z; quá giờ đó, hai service này coi sự kiện đã kết thúc, có thể sinh payout hoặc đổi check-in và làm hỏng đêm nền W4. Mất khoảng 15 phút.
3. **Soạn SPEC W4** (luật cảnh báo, đêm nền) ngay. exp-app đang rảnh, nên nếu SPEC được duyệt hôm nay thì đêm nền 1 có thể chạy đêm nay. Trong SPEC thêm hai việc trước mỗi lượt dài: kiểm hạn bán của sự kiện, và ghi số dòng các bảng chính. Song song đó soạn SPEC W5 ở phiên khác; W5 chỉ dùng dữ liệu đã thu.
4. **Kiểm soát trạng thái DB cho W6–W7:** chụp một bản dump làm mốc chuẩn và khôi phục trước mỗi đợt đánh giá. Đưa vào SPEC W6, không làm riêng bây giờ.
5. **Phép tách DB với code** (cùng image, khôi phục DB nhỏ, thu 2 ô, ~1 giờ 30 phút): đề xuất **không làm bây giờ**. Chỉ cần nếu một quyết định ở W6 đòi tách riêng DB khỏi code.
6. **Ghi cho thiết kế W6:** điểm yếu "chấm theo một mẫu max trên kênh gộp" của lõi là ứng viên chưa kiểm. Có thể thử đơn vị theo từng câu lệnh, hoặc thay max bằng phân vị cao, trên dữ liệu dev. Không sửa gì trong T-069.
7. **Báo nhóm FlashTicket:** worker hết hạn đơn và worker giao vé đang quét tuần tự bảng lớn, kéo CPU PostgreSQL lên. Đây là vấn đề hiệu năng thật, liên quan NV1. Minh gửi, hoặc tôi soạn nội dung để Minh gửi.
8. **Commit repo RCA:** gồm `tasks/T-069-v082-ban-ghim/`, `results/T-069/` (bỏ 3 file `raw.json` 60–78 MB; bản gốc và hash còn trên exp-obs), `docs/DECISIONS.md`, `docs/WHY.md`. `docs/STATE.md` đang lẫn thay đổi chưa commit của phiên T-066/T-067/T-068, nên Minh chọn có đưa vào hay không.
9. **Codex kiểm lại:** prompt ở cuối LOG; Minh điền phạm vi ghi.

"

"

**Đề xuất Minh duyệt việc soạn SPEC song song cho W4, W5 và W6. Chưa nên duyệt phát lượt nền 12 giờ theo lịch bản 2.** Chạy ban ngày là hợp lý. Điểm chặn nằm ở cách tạo tải, thời điểm khóa luật cảnh báo và cách xác định giờ khỏe để tính báo động giả. Ba điểm này đều có thể xử lý mà không phải chạy lại T-069.

### Các điểm phản biện

| Mức | Bước bị ảnh hưởng | Bằng chứng, hậu quả và sửa tối thiểu |
|---|---|---|
| **CHẶN phát lượt W4 như mô tả** | A có tạo được 12 giờ tải liên tục với nhiều đợt flash hay không | Ở bản lab `407b4f5`, cả `tai_linux.py` và kịch bản k6 đều giới hạn **3.600 giây mỗi lượt**. Mỗi lượt chỉ có tải đều hoặc **một lần tăng bậc**, giữ mức cao đến hết lượt. Mỗi lần `start` còn kiểm máy rảnh và cấp phiên đăng nhập mới. Vì vậy, nối các lượt một giờ là **phương án thực thi ngay từ đầu**, có khoảng chuyển lượt. Đề xuất ghi lịch từng lượt, thời gian có tải thực, khoảng chuyển và cách xử lý cảnh báo tại biên. Với lỗi ở 10%, 50%, 99%, giữ nguyên đoạn hợp lệ và kết quả lỗi, chỉ bù phần thiếu nếu còn đáp ứng thiết kế. Thời gian bù một lượt tải tối đa một giờ, cộng khởi động và kiểm tra. Nếu cần tính liên tục tuyệt đối thì phải trình thay đổi bộ tải riêng. [Bộ điều khiển](D:/Project/flashticket-rca-lab/load/controller/tai_linux.py:225) · [Giới hạn tham số](D:/Project/flashticket-rca-lab/load/controller/tai_linux.py:340) · [Kịch bản k6](D:/Project/flashticket-rca-lab/load/scenarios/purchase-journey.js:18) |
| **CHẶN chấm nửa 2 và cam kết giờ xong W4** | B dùng hết nửa 1 để chọn ngưỡng, đồng thời muốn bắt đầu chấm trực tuyến ngay đầu nửa 2 | Sau mẫu cuối của nửa 1 vẫn còn thời gian tính ngưỡng, nạp bản luật đã chọn và xác nhận Grafana đang đánh giá. SPEC cần khai trước **mức báo giả chấp nhận được, đơn vị sự cố sau gom, số giờ khỏe làm mẫu số** và cách ghi nhận mất dữ liệu. Ghi giờ luật thực sự có hiệu lực rồi mới tính nửa 2. Kiểm đường gửi–nhận webhook bằng một tín hiệu dương có kiểm soát ngoài khoảng chấm. Nếu thấy trôi ở nửa 2 rồi đổi ngưỡng hoặc khôi phục DB, giữ kết quả đầu và dùng khoảng mới để kiểm phương án sửa. Bản 2 chưa đủ căn cứ cho mốc “W4 xong 15–16Z”. [Tiêu chí W4](D:/RCA-flashticket/docs/techstack/KE-HOACH-GIAI-DOAN-2.md:139) · [Độ đo phát hiện](D:/RCA-flashticket/docs/techstack/KE-HOACH-GIAI-DOAN-2.md:151) |
| **CHẶN kết luận “báo động giả khi flash” nếu chỉ dựa vào việc không tiêm lỗi** | Chọn hồ sơ nền và phân loại cảnh báo | **Mình chọn (b)**, giữ cùng hỗn hợp hành trình, khai trước lịch ×1 và flash ở cả hai khoảng, báo kết quả riêng theo mức tải. Có bằng chứng để chọn ứng viên này. Ca `124242f0` đã chạy 10 phút ×1 rồi 20 phút ×3, hoàn tất **5.042/5.042 hành trình**, tỷ lệ HTTP lỗi bằng 0. Tuy vậy, mỗi đợt mới vẫn cần bằng chứng sức khỏe độc lập từ tải thực đến backend, hành trình hoàn tất, lượt k6 bỏ và phản hồi 429. Khai cách phân loại trước khi xem cảnh báo. Nếu tải thực sự làm dịch vụ suy giảm, giữ cảnh báo và thời lượng ở nhóm đó. Nếu không, hệ càng phát hiện quá tải tốt lại càng bị chấm nhiều báo giả. [Cấu hình ca, `/stepSeconds`](D:/RCA-flashticket/results/T-069/thu/t069-chinh/tai-out/t3-124242f0/run.json) · [Kết quả, `/metrics/journey_finished/count`](D:/RCA-flashticket/results/T-069/thu/t069-chinh/tai-out/t3-124242f0/summary.json) · [Quyết định về tải và quota](D:/RCA-flashticket/docs/DECISIONS.md:539) · [Tiêu chí flash khỏe](D:/RCA-flashticket/tasks/T-059-danh-muc-loi/SPEC.md:32) |
| **CHẶN nghiệm thu W5 theo câu “Grafana tự hiện kết quả”** | C có thể làm song song, nhưng tiêu chí cuối chưa phân biệt được kết quả mới với ca phát lại | Bộ đóng gói hiện hành nhận `--t` và ghi `mode: a`. Một ca cũ hiển thị đúng chỉ kiểm được một phần đường chạy. Đề xuất B và C chốt ngay bản ghi cảnh báo chứa **mốc báo động `t̂`, luật và tín hiệu kích hoạt**, cùng giờ nhận webhook lưu riêng. Ca nghiệm thu phải cho thấy lõi thực nhận dữ liệu trong `[t̂−300, t̂)` và `[t̂, t̂+300)`, với liveness theo lần dò mới nhất. Đo thời gian trên dev rồi khai **N phút trước khi tiêm**. Nếu không có cảnh báo, thiếu dữ liệu hoặc xử lý lỗi, ghi riêng từng trường hợp. W4 có thể kiểm giao nhận webhook bằng bộ nhận nhẹ trong khi C hoàn thiện RCA. [Hợp đồng D3](D:/RCA-flashticket/tasks/T-043-thiet-ke-rca-m1/SPEC.md:324) · [Bộ đóng gói hiện tại](D:/Project/flashticket-rca-lab/campaigns/runner/stage_m1.py:85) · [Tiêu chí W5](D:/RCA-flashticket/docs/techstack/KE-HOACH-GIAI-DOAN-2.md:140) |
| **CHẶN riêng phép “thử tải tối đa” đã đề xuất** | Các bậc ×4 và ×6, cách suy ra sức chịu tải | Bộ điều khiển chỉ nhận hệ số **1 đến 3**. Số 27–30% ở ca khỏe ×3 là **PSI `some avg60`**, tỷ lệ thời gian có tác vụ phải chờ CPU. Nó không cho biết máy đã dùng 27–30% công suất hay còn dư bao nhiêu. Đề xuất hoãn lượt này khỏi đường dẫn tới W9a. Nếu Minh giao NV1, soạn SPEC riêng, xác định tải yêu cầu, tải đạt được, giới hạn người mua và tiêu chí suy giảm. Nếu bộ phát hết khả năng trước ứng dụng, kết luận chỉ là mức tải hệ đã phục vụ được. Một lượt tăng bậc cũng chỉ bao phủ một phần NV1. [Giới hạn bộ điều khiển](D:/Project/flashticket-rca-lab/load/controller/tai_linux.py:342) · [Số đo PSI, dòng `BINH-THUONG-X3; moi`](D:/RCA-flashticket/results/T-069/phan-tich/psi.txt) · [Nhiệm vụ DT18-NV1](D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md:13) |

### “Đầu đêm và cuối đêm không cùng điều kiện” đúng đến đâu?

**Đã đo được:** bốn ca ×1 không tiêm trong lượt chính đều có 648 lần tạo đơn thành công trong 30 phút. Ở thời điểm kiểm DB, `tbl_orders` có 37.477 dòng. Với truy vấn tìm đơn hết hạn, `EXPLAIN` cho kế hoạch quét tuần tự. Hai bảng Ticket cũng có số lượt quét tuần tự tích lũy lớn. [Số đơn, ví dụ `/1e5debb6/201`](D:/RCA-flashticket/results/T-069/thu/t069-chinh/tai-create-order.json) · [Số dòng, `EXPLAIN` và thống kê từng bảng](D:/RCA-flashticket/results/T-069/phan-tich/kiem-db.txt)

**Chưa kiểm:** lấy `648 × 2 × 12` cho 15.552 đơn, tương đương khoảng 41,5% **số dòng của riêng `tbl_orders` tại mốc đã đo**, nếu giữ ×1, cùng tỷ lệ thành công và các dòng còn lại trong bảng. Con số ấy chưa cho biết dung lượng toàn DB, p95 của từng route hay số cảnh báo ở giờ thứ 12. Thống kê Ticket cũng cộng dồn theo bảng, chưa tách riêng từng câu SQL của worker. Đề xuất giữ DB tích lũy qua hai khoảng nếu câu hỏi W4 là luật có chịu được vận hành kéo dài hay không. So p95 và cảnh báo ở **cùng mức tải** đầu–cuối, đồng thời giữ chuỗi lỗi, p95 và liveness ở đúng nhịp luật đánh giá. Số ghi mỗi giờ giúp giải thích xu hướng nhưng không dựng lại được một cảnh báo chỉ kéo dài vài phút. [Phân tích T-069, mục 4](D:/RCA-flashticket/results/T-069/phan-tich-nguyen-nhan.md) · [CPU PostgreSQL ở các khoảng nền](D:/RCA-flashticket/results/T-069/phan-tich/cpu-container-nen.txt)

### Thứ tự đề xuất cho Minh

1. **Cho soạn SPEC A/B/C/D song song.** A và B thống nhất lịch tải, tiêu chí giờ khỏe và mốc bàn giao trước khi A phát nền. B có thể dùng ngay bốn ca ×1, một ca ×3 đều, một ca flash của T-069 và lượt ×1 một giờ của T-067 để thử cách tính. Đây là cách giảm thời gian chuẩn bị. Khoảng chấm trực tuyến vẫn cần được giữ riêng. D tiếp tục thiết kế W6, gồm D14 và việc đóng gói đầu vào độc lập với đầu ra P7. [Lượt tải T-067](D:/RCA-flashticket/results/T-067/tai-1-gio.md) · [Thiết kế W6](D:/RCA-flashticket/docs/techstack/KE-HOACH-GIAI-DOAN-2.md:146)
2. **Đồng bộ hai bản sao ngày sự kiện là hợp lý, nhưng tách việc này khỏi hạn phát W4.** Hạn bán đã ghi ở Event/Booking là **05:16 ngày 03/12 giờ Việt Nam**. Mốc cũ ở Ticket/Payment là **05:16 ngày 21/11 giờ Việt Nam**, chi phối cửa sổ check-in và điều kiện đối soát. Kịch bản mua hiện hành không gọi hai thao tác đó. Đề xuất duyệt riêng đúng các trường và bản ghi cần đồng bộ, lưu giá trị cũ, rồi chụp mốc tham chiếu khi các bản sao đã khớp. Nếu muốn **khôi phục** cho một lượt sau, SPEC cần nói cách xử lý đơn đang dở, hàng đợi và trạng thái mock tại mốc chụp. Chưa có phép đo cho cam kết khôi phục trong 15 phút. [Bản ghi trước](D:/RCA-flashticket/results/T-069/sua-su-kien/truoc.jsonl) · [Bản ghi sau](D:/RCA-flashticket/results/T-069/sua-su-kien/sau.jsonl) · [Điều kiện check-in](D:/Project/flash-ticket-platform/services/ticket-service/src/main/java/com/flashticket/ticket_service/application/TicketService.java:575) · [Điều kiện đối soát](D:/Project/flash-ticket-platform/services/payment-service/src/main/java/com/flashticket/payment_service/service/impl/FinanceServiceImpl.java:195)
3. **Xếp lượt dùng máy theo thứ tự nền W4 → kiểm W5 → diễn tập W9a khi W8 tối thiểu đã sẵn.** Có thể chuẩn bị kịch bản và phần phát lại trước. Đề xuất chọn W8 ở mức demo trước, vì §8.2 đã xác định đầu ra tối thiểu là giải thích có dẫn chứng và gợi ý xử lý. Phần đánh giá sâu của LLM vẫn do Minh quyết. Người viết quyển có thể làm các chương đã có kết quả. Phần báo nhóm FlashTicket nên trình Minh dưới dạng bản nháp có số đo và giới hạn quy nguyên nhân. [W8 và W9a](D:/RCA-flashticket/docs/techstack/KE-HOACH-GIAI-DOAN-2.md:141)

**Kiểm toàn vẹn và phạm vi lượt này.** Mình đã soát **kế hoạch bản 2** trong chat, đọc code ở hai revision được chỉ định và kiểm đủ **318/318 file T-069** khớp danh sách hiện tại. Có một đính chính cụ thể trước khi chốt hồ sơ: LOG bước 9 ghi mã danh sách `410d9923…`, còn file cuối có mã `cec9b3f1…`. Mình đã tái tạo đúng tiền tố cũ bằng cách giữ nguyên 317 mục còn lại và tính riêng `thay-doi-may.md` đến hết M11. Bản cuối thêm M12, M13 và dòng kiểm DB chỉ đọc. Đề xuất Claude trình nối một dòng đính chính vào LOG trong lượt soát kết quả T-069. Chênh lệch này đã giải thích được, không cần thu lại dữ liệu. **Không sửa file nào, không commit, không truy cập máy chủ và không chạy thực nghiệm.** [LOG bước 9](D:/RCA-flashticket/tasks/T-069-v082-ban-ghim/LOG.md:287) · [Danh sách cuối](D:/RCA-flashticket/results/T-069/SHA256SUMS) · [Ba dòng bổ sung](D:/RCA-flashticket/results/T-069/thay-doi-may.md:19)

**Đề xuất tiếp tục một lượt Claude đáp phản biện trong chat.** Quyết định còn chờ Minh là hồ sơ tải (b), phạm vi đồng bộ và chụp DB, cùng việc hoãn thử sức tải khỏi lịch demo. Phần còn thiếu để duyệt chạy là lịch tải thực thi được, tiêu chí báo giả, thời điểm khóa luật và hợp đồng nghiệm thu W5. Lượt này không thay cho lượt phản biện kết quả T-069 đang chờ trong STATE.

<details>
<summary><strong>Prompt bàn giao cho Claude — người làm đáp phản biện</strong></summary>

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: đề xuất thứ tự và song song hóa W4, W5 cùng các việc liên quan sau T-069, bản 2 trong chat. Nguyên văn đề xuất được gửi soát:
  "Bắt đầu ngay ~02:00Z 20/11, không đợi đêm (mọi phần chạy trên server). Bước 0 Minh quyết: dời mốc ngày sự kiện ở ticket_db/payment_db +14 ngày trước 20/11 22:16Z; dump DB hiện tại làm mốc tham chiếu cho mọi lượt dài sau; hồ sơ tải nền (a) ×1 đều hoặc (b) ×1 có vài đợt flash ×3 hợp lệ, người làm đề xuất (b) vì W7 có ô FLASH; có thử tải tối đa không; commit T-069, gửi Codex. Bước 1 phiên A (~30–45 phút): dời mốc, dump, SPEC đo nền, kiểm bộ tải chạy nhiều giờ (mới kiểm tới 1 giờ ở T-067; nếu không thì nối các lượt 1 giờ). Bước 2 exp-app nền liên tục ~12 giờ (~03:00Z–15:00Z), hai nửa khai trước: nửa 1 (6 giờ) chọn ngưỡng, nửa 2 (6 giờ) đo báo động giả với luật chạy thật; mỗi giờ ghi số dòng bảng DB, CPU PostgreSQL, p95 theo route để đo trôi; không khôi phục DB giữa hai nửa, nếu trôi làm lệch ngưỡng thì trình lại phương án khôi phục (~15 phút bảo trì). Lý do đo trôi: tải ×1 tạo ~1.300 đơn/giờ; worker Booking OrderExpiryWorker (mỗi 5 s) và Ticket TicketJobs (mỗi 1 s) quét tuần tự tbl_orders, tbl_ticket_deliveries, tbl_issuances nên chậm dần và PostgreSQL tốn CPU dần (T-069). Bước 3 sau nền: kiểm W5 từ đầu tới cuối (tiêm một lỗi, Grafana tự hiện kết quả), thử tải tối đa nếu duyệt (bậc ×1, ×2, ×3, ×4, ×6, mỗi bậc 10 phút, dừng ở bậc đầu có lỗi hệ thống hoặc p95 vượt mức khai trước, khôi phục DB trước và sau, kiểm giới hạn 20 phiên người mua), rồi W9a. Song song ngay: B W4 viết luật, quy tắc gom, script chọn ngưỡng trên dữ liệu đã lưu, luật sẵn trước nửa 2; C W5 bộ xuất theo cửa sổ bất kỳ, G1 0.3, bộ điều phối webhook, thống nhất định dạng webhook với B, không truy vấn Prometheus nặng khi nền chạy; D W6 thiết kế, đưa phát hiện T-069 (kiểm soát DB, điểm yếu chấm z, đóng gói đầu vào không phụ thuộc P7); E W8 khi Minh chọn mức P8; F quyển, báo nhóm FlashTicket truy vấn quét tuần tự, tồn đọng. Phụ thuộc cứng: exp-app và máy tải một lượt tại một thời điểm (nền, kiểm W5, thử tải nối tiếp); ngưỡng cần dữ liệu nửa 1; kiểm W5 cần luật W4 và dịch vụ W5; hạn bán sự kiện tới 02/12, kiểm lại trước W7. Nền = có tải bình thường không tiêm lỗi; để im không dùng được."
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: kế hoạch giai đoạn 2 §8, chuẩn bị G6; đề xuất ngoài task.
- Người làm và người phản biện chính thức: ngoài task, người soạn Claude, người phản biện dự kiến Codex.
- Tài liệu gốc: docs/techstack/KE-HOACH-GIAI-DOAN-2.md, docs/techstack/PLAN-TRIEN-KHAI.md, docs/STATE.md, tasks/T-069-v082-ban-ghim/SPEC.md và LOG.md, SPEC và LOG của T-043, T-059, T-066, T-067, T-068 theo phần liên quan.
- Phản biện và phản hồi trước: một bản phản biện của Codex trong chat, Minh chuyển sau phần tự soát; chưa có phản hồi của người làm.
- Code và kết quả liên quan: results/T-069/ và SHA256SUMS, results/T-067/ và SHA256SUMS; D:/Project/flashticket-rca-lab commit 407b4f5; D:/Project/flash-ticket-platform revision 36a3725d.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm, LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
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

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm “cho chắc”.
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
```

</details>
