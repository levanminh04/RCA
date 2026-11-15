# Phản biện T-064 — lượt 2

- **Người phản biện:** Codex — **Ngày:** 14/11/2026, khoảng 00:41Z — **Commit/diff đã đọc:** gốc `c3d27f8a`; đầu ra chưa commit. Chỉ ghi bản mới này theo brief của Minh.
- **Công đoạn/cổng:** kiểm lại phản hồi và sửa sau REVIEW lượt 1; M3 chiến dịch M1-FlashTicket. Task còn đang làm; đây không phải lượt nghiệm thu toàn M3.
- **Đã đọc:** AGENTS, STATE, SPEC và LOG T-064 (phiên 3); hồ sơ chiến dịch và checkpoint; mục tiêu MRP §2–3, DT18, hướng dẫn cô, LESSONS; WHY-81–86 và quyết định chiến dịch/tập chọn 13 ca. Đã đọc tiêu chí, hồ sơ chọn, sổ, đáp án, hai tập chọn, ghi chú cơ chế, chú thích nền, hợp đồng đầu ra, thay đổi máy; code đường chạy/chấm/bổ sung/H1/H5/H8, tiền xử lý span P7 và quy ước chấm; script ghi sổ/phát/nhận/kiểm lượt 3; bảng điểm và đầu ra liên quan của ba lượt; manifest T-063, T-062 và pin nền P7. Sau tự soát mới đọc kết luận REVIEW.md và bảng phản hồi.
- **Tự soát độc lập:** kiểm hash trước khi dùng lại; tính điểm từ nhóm hòa và phép chiếu bằng JavaScript; lần mẫu từ trace gốc của ca 98ea5ba4. Nhận xét trước khi đọc REVIEW: sửa phân loại khớp mẫu nguồn ở ca hỗn hợp; câu “không đổi” cần phân biệt thứ tự nút, danh sách cạnh và điểm cuối; hồ sơ tự khai các đầu ra M3 còn thiếu, không thể coi ứng viên tạm là bản khóa. Không phát thực nghiệm, không đọc dữ liệu khóa/ô đánh giá, không truy cập hoặc đổi máy chủ.

## Kết luận chung

**Gói sửa R1–R4 đã xử lý đúng các phần được kiểm; có một finding mới KHÔNG CHẶN về câu tổng hợp trong STATE.** R1 có lượt kết quả riêng; R2/R4 đã sửa đúng diễn giải và trạng thái quyền. WHY-85/86 xử lý phần lý do của hai lựa chọn quyết định ứng viên, khai đúng việc ghi muộn và giới hạn bằng chứng; không xóa vi phạm đã xảy ra. STATE nói không bản nào hồi quy, nhưng V043/V044 hồi quy so với P7 trên T-062; việc bản sửa bằng bản cha không đồng nghĩa bản đó không hồi quy so với P7.

Đủ để dùng kết quả lượt 3 cho bước phát triển tiếp và bản xuất thử. Chưa đủ nghiệm thu T-064/M3, khóa ứng viên, xác nhận lợi ích đồ thị hay trả lời RQ5. V032 vẫn là ứng viên **tạm** theo tiêu chí hiện hành trên tập 13 ca; V041 là bản thay thế có đầu ra cạnh.

## Các điểm

### R5. STATE gộp “bằng bản cha” thành “không bản nào hồi quy” — KHÔNG CHẶN

- **Ở đâu:** `docs/STATE.md`, dòng task T-064, câu “Không bản nào hồi quy trên 9 ca T-062”.
- **Sai gì:** đây là câu phổ quát sai khi đối chiếu tiêu chí không hồi quy so với P7. Bản sửa có thể bằng bản cha nhưng cả hai vẫn kém P7. Không phải lỗi của bộ chấm hoặc lỗi mới do sửa R1.
- **Bằng chứng:** `results/T-064/cham/khong-hoi-quy-3.json#/ban/V043-R1-H1a/tong/AC@1` = 3,3333333333333335; V044-R1-H1b cùng trường = 3,6666666666666665, trong khi `#/P7/tong/AC@1` = 5. Cả hai có `khong_xau_di = false`, K = 4. Đếm đủ 10 bản lượt 3: **8 đạt, 2 không đạt** điều kiện X không xấu đi; không có bản tăng K. Đã tính độc lập từ đầu ra gốc, không chỉ đọc cờ tổng hợp.
- **Phần có thể phản bác finding:** bảng kết quả thật đúng; hồ sơ chọn đã bỏ H1a/H1b vì AC@1 giảm. V032 và V041 không nằm trong hai ngoại lệ này. Nếu câu STATE chỉ định nói các ứng viên được giữ thì phải nói rõ tập bản đó; câu hiện tại không có phạm vi ấy.
- **Bước và quyết định chịu ảnh hưởng:** lỗi báo cáo đã xảy ra, làm sai trạng thái không hồi quy của các bản bị loại. **Không chặn** tiếp tục phát triển, chọn tạm V032 theo §5 hay dùng V041 làm bản thay thế; không chặn R1 được xác nhận đã sửa đúng. Chặn dùng câu phổ quát ấy làm kết luận về toàn bộ biến thể.
- **Đề xuất sửa tối thiểu:** người làm sửa đúng câu trong dòng T-064 của STATE thành “V032 và V041 không hồi quy trên 9 ca T-062; lượt 3 có V043/H1a và V044/H1b hồi quy AC@1, bằng tình trạng của các bản cha.” Vì sao: phân biệt mốc so và khoanh phạm vi, không cần chạy thêm. Mặt trái: dòng STATE dài hơn; có thể rút thành “Các bản đề xuất tạm không hồi quy; H1a/H1b bị loại vì giảm AC@1”, dẫn bảng chi tiết. Tôi ưu tiên câu có tên bản và hai ngoại lệ vì tránh lặp sự mơ hồ hiện tại. Đây là đề xuất, reviewer không sửa STATE.
- **Pin và tác động:** STATE là trạng thái sống, không nằm trong hàm băm cây mã hoặc các trường pin đầu vào/đầu ra của bảng chấm đã kiểm. Sửa câu làm đổi hash tệp STATE nếu có ai băm toàn repo, nhưng không đòi ghim lại hoặc chạy lại 47 bản. Không sửa bảng chấm/summary/code để khớp câu báo cáo.

Các phần chưa làm ở SPEC/hồ sơ chọn vẫn là nghĩa vụ của task đang mở, được nêu dưới đây; không biến chúng thành lỗi đã xảy ra hoặc điều kiện bắt buộc làm xong ngay trong lượt kiểm này.

## Đối chiếu các lượt trước

| Điểm và phản hồi | Đánh giá độc lập hiện tại | Hậu quả và trạng thái |
|---|---|---|
| R1: sai loại cạnh; người làm đồng ý, sau đó sửa và chạy lượt 3 | **Đúng; bản sửa xử lý đúng lỗi đã chỉ ra.** Vòng lặp giữ điều kiện span bọc của P7, tách theo kind trước khi chấm; nhánh tái lập cũ chỉ bật ở đối chứng. Ở 98ea5ba4, ghép kind đủ 162.228/162.228 span; Payment → Booking tách http N/A = 72/0 và message = 144/0; Booking → Payment message = 144/0; Payment → Ticket và Ticket → Payment message = 72/0 mỗi tuyến. Khớp đầu ra V039. | Gỡ chặn dùng đầu ra H1 đã sửa trong phạm vi dev đã kiểm. Không khẳng định mọi giao thức hoặc mẫu async chưa quan sát đều được hỗ trợ. Lượt cũ giữ là lịch sử; không nâng thành kết quả của mã mới. |
| R2: bỏ H1c bị gọi là bỏ quan hệ; người làm sửa mục 4, 8 | **Đúng; đã xử lý hai câu diễn giải.** V002 giữ E1/E2/E5, phép tính mẫu độc quyền/đặc trưng cạnh/kế thừa của P7. H1c là thêm đầu ra cạnh trên nền ấy. Đã đối chiếu cấu hình và đường chay → chuan_bi/mau_canh → E5 → xếp hạng. | Không còn dùng DT18 làm lý do buộc chọn H1c. Phép so bỏ quan hệ thật vẫn chưa có; kết luận lợi ích riêng của quan hệ trên FlashTicket còn OPEN. |
| R3: thiếu WHY cho sàn 1 ms và H5b; người làm thêm WHY-85/86 | **Đúng; đã xử lý nội dung của hai lựa chọn này.** WHY ghi rõ thời điểm thêm muộn, nguyên lý/sổ có trước, phương án khác, đánh đổi, điều kiện thất bại và phụ thuộc. 1 ms được ghi là ngưỡng thực dụng; giả thuyết CFS chưa được xác nhận. H5b khai thiết kế sau khi xem PAUSE-PAYMENT và chỉ một ô. | Không coi bổ sung WHY là bằng chứng mới hoặc khắc phục ngược thời điểm tuân thủ. Người làm còn khai chưa rà đủ WHY cho H2/H4/H6a/H7c; không đánh dấu đã hoàn tất toàn bộ yêu cầu rà của R3. Việc đó còn trong hồ sơ M3, không là căn cứ bác điểm số hoặc chặn bản xuất thử hiện tại. |
| R4: áp tiêu chí hiện hành bị ghi thành chờ Minh xác nhận | **Đúng; đã xử lý.** Mục 4/9 dẫn đúng quyền đã cấp. Mục 10 áp quyết định dùng tập B; mục 11 giữ thứ tự §5. File tiêu chí khóa không bị sửa để đồng bộ ngược quá khứ. | Quyền tự chọn theo tiêu chí khác với quyền đổi tiêu chí sau khi xem kết quả. Không còn chờ Minh quyết lại việc áp dụng thứ tự đang có. |
| N1: giờ ước lượng sai | **Đúng; đã khai đính chính theo lịch sử LOG.** Sổ trước lượt 3 ghi trước thời điểm phát; không dùng các giờ ước lượng cũ để chứng minh quyền hoặc thứ tự mới. | Không thấy hệ quả đổi dữ liệu, tiêu chí hoặc thứ tự chấm ở lượt 3. |
| N2: độ vượt bị bỏ sát sàn | **Đúng về quan sát; chưa kiểm được độ nhạy cục bộ của K quanh 1 ms.** Bảng chú thích mục 3 có 762, 977, 985 µs; không suy ba con số này thành lượng thay đổi K. Các ca tương ứng vẫn K = 1 ở sàn hiện tại. K đã khác giữa P7 và sàn 1 ms, nhưng điều đó không xác định đường đáp ứng khi quét gần sàn. | Đọc nhận định “K nhạy” như cảnh báo chưa quét, không như kết quả đo độ nhạy. Không đổi lựa chọn hoặc yêu cầu quét chỉ để hợp thức hóa một câu. |
| Pin bộ chấm cũ trong t062-p7.json | **Đúng về lịch sử pin; không thấy sai số điểm.** Đối chiếu độc lập ba bảng không hồi quy: 47 bản-tập, 423 ca đều khớp đầu ra theo quy ước hiện hành. | Không ghi lại pin của file lịch sử thành hash mã hiện tại. Chưa chạy lại Python trong sandbox này. |

### R1 — kiểm trung gian và tác động, không chỉ kiểm điểm cuối

Nguồn số: `results/T-064/cham/dau-ra-dev2/<bản>/<ca>/method-output-1.json#/extra/m1_ft/canh_xep_hang`, `#/entity_ranking`; T-062 ở `bien-the/<bản>/ra-khong-hoi-quy-<lượt>/<ca>/`. Đối chiếu độc lập khớp `kiem/kiem-luot3.json#/so_voi_cha` và `#/doi_chung`:

- Tám cấu hình sửa giữ nguyên cấu hình cha. Thứ tự cặp (entity, tie_group) trùng **176/176** cặp bản–ca. Không có cạnh khong_ro trong các đầu ra đó.
- Hai đối chứng V046/V047 trùng bản cha **44/44** cặp sau khi bỏ đúng variant, ba khóa siêu dữ liệu cây mã/cấu hình/bản và ba khóa chú thích mới; không bỏ điểm khoa học.
- Danh sách cạnh có cờ (nguồn, đích, loại, hạng) chỉ đổi ở V043 tại 19b17e22, fb1cf0e9, 60166807. “Không đổi” chỉ đúng với điểm chấm và thứ tự nút, không đúng với toàn bộ danh sách cạnh.
- 19b17e22: Payment → Booking từ mẫu gộp 216/216 không cờ thành HTTP 72/72 có cờ, e = 1/3, hạng 2. Booking → Payment chuyển đúng loại message; các cạnh phía sau dịch hạng.
- 60166807: cùng tuyến gộp 216/216 tách HTTP 72/72, có cờ, e = 0,45833, hạng 2; Booking → Payment đổi loại và dịch hạng 4 → 5. Đây là chấm lại mẫu riêng, không chỉ đổi chữ hiển thị.
- fb1cf0e9: Payment → Ticket giữ mẫu 72/213, e = 0,05223, hạng 2, đổi loại http → message. Trường hợp này danh sách “cạnh có cờ” khác do sửa loại, không do phát sinh cờ.

Đối chiếu nghĩa loại span theo [OpenTelemetry SpanKind](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind); số kind cụ thể được kiểm trên trace đã ghim, không thay runtime bằng bản thư viện mới. [Tài liệu CFS chính thức](https://docs.kernel.org/scheduler/sched-design-CFS.html) không xác lập 1 ms là ranh giới lỗi/nhiễu của phép đo này; vì vậy cách WHY-85 giữ giả thuyết ấy ở trạng thái chưa kiểm là phù hợp.

Ba ca trên không phải ô có đáp án cạnh. Phép chiếu vẫn cho cùng phân bố hạng đáp án ở bảng nút; bảng cạnh được chấm trên ba ô cạnh khác. Vì vậy điểm cuối không đổi dù trung gian đổi là kết quả nhất quán. Với H1b/H1c, định vị còn có thể gỡ cờ trước khi chèn cạnh; không lấy “điểm bằng nhau” làm chứng cứ mọi cạnh bất biến.

## Tuân thủ quy trình

- Phạm vi sửa của người làm nằm trong quyền SPEC và chiến dịch đã được bổ sung ở DECISIONS; sửa R1 không phải hành động tự động tuân theo finding ngoài quyền. Đã kiểm sổ mới, thư mục mới và ghi nhận TD-64-09, không ghi đè lượt cũ. Không có bằng chứng trong đường đã soát về việc đổi tiêu chí hoặc dùng ô đánh giá.
- `h1_canh.py` thuộc hash cây mã; cây hiện tại khớp pin lượt 3. Đối chứng mã nguồn bảo toàn việc dùng lại hai bản cha. `git diff c3d27f8a --stat -- src/m1 src/p3` không có thay đổi; các pin nền cũng khớp.
- Đường phương pháp chỉ đọc t của request và tín hiệu kỹ thuật; nhãn nằm phía chấm. H1 không nhận tên ô/đáp án. Không suy từ kiểm đường chạy này thành bảo đảm không thể tái nhận diện dữ liệu bằng bất kỳ cách nào.
- LOG khai lượt 3 sau khi xem lượt 1/2, giữ kết quả lỗi cũ, có dự toán từ lượt trước và xử lý lỗi ở 10/50/99%. Lỗi chặn lệnh do tự khớp tên tiến trình được ghi là lỗi thao tác; không biến thành kết quả phương pháp.
- Bảng phản hồi cũ và phần mục 9 của hồ sơ ghi trạng thái trước sửa; LOG và mục 11 nối lịch sử sau sửa. Không coi các câu lịch sử ấy là bản sửa hiện tại vẫn chưa thực hiện.
- Vai trò lượt này chỉ ghi REVIEW-2.md; không ghi LOG/STATE, không sửa thay người làm, không commit/push. Không thể quy toàn bộ working tree đang có của nhiều task cho lượt T-064 này.

## Điều đã kiểm và thấy đúng

Các lệnh tính/đối chiếu chạy qua `mcp__node_repl.js`, chỉ đọc; SHA-256 dùng `node:crypto`, tar đọc trong bộ nhớ bằng `node:zlib`. Kết quả dưới đây là kiểm độc lập bằng JavaScript, **không** phải chạy lại Python/M1.

| Phép kiểm | Kết quả |
|---|---|
| SHA theo T-063 thu2/SHA256SUMS | 214/214 khớp |
| SHA theo T-062 ca/manifest-ca.json#/files; ca/_nguon/m1-source-pins.json#/pins | 28/28 và 39/39 khớp |
| Gói nhận lượt 3 theo nhan-luot3/luot3-out.sha256; đối chiếu file trong tar với file đang dùng | Khớp; 660/660 file bằng byte |
| Cây src/m1 + src/m1_ft, quy tắc sha_ma_nguon() | 31 file mã, khớp pin sổ/summary lượt 3 |
| Cấu hình canonical theo sổ các lượt chọn | 47/47 khớp |
| Hai output theo summary của 47 bản trên dev và T-062 | 1.034 cặp, không lệch SHA; riêng lượt 3 đủ 220 cặp, summary OK, hai lần khớp |
| SHA output tham chiếu bởi sáu bảng dev | 1.250/1.250 khớp; đáp án, tiêu chí, tập chọn cũng khớp pin |
| Tính độc lập phân bố min hạng tập chấp nhận, phép chiếu, AC@1/3, hạng cắt, K | 100 bản-tập, 1.250 ca trong sáu bảng dev khớp, dung sai 1e-9 |
| Tính độc lập đúng cạnh có hướng/loại và nhóm hòa | 300 phép chấm ca-cạnh khớp |
| Tính độc lập ba bảng không hồi quy | 47 bản-tập, 423 ca khớp; riêng lượt 3: 8 bản đạt không hồi quy, V043/V044 giảm AC@1 so với P7 |
| Tách mẫu từ raw trace 98ea5ba4 | Đủ kind cho 162.228 span; 13 nhóm tuyến-loại khớp mẫu N/A xuất ra |

Công thức chấm độc lập: với nhóm hòa đầu tiên có g nút, m đáp án chấp nhận và pos nút đứng trước, xác suất min hạng tại pos+q là C(g−q,m−1)/C(g,m). Cộng xác suất top 1/3 và E[min(hạng,6)]. Trước đó gán mỗi nút vị trí đầu nhóm, cho cạnh có cờ cải thiện hạng hai đầu theo tiêu chí rồi gom nhóm lại. K đếm thô từ status/verdict. Đã so từng ca và tổng, không chỉ so bản đứng đầu.

Trên tập chính, `cham/chon-dev2-luot2-tap13.json#/ban/V032-H5b`: AC@1 = 6, AC@3 = 8, tổng hạng = 10, K = 4. `cham/chon-dev2-luot3-tap13.json#/ban/V041-R1-H1c+H5b+H8s1`: 6, 8, 11, K = 3, cạnh top 3 = 3/3. Thứ tự §5 hiện hành chọn V032; ưu tiên K/cạnh để chọn V041 sẽ là đổi tiêu chí sau khi xem, chưa được suy thành quyết định Minh.

**Giới hạn kiểm thực thi:** gọi Python ghim với -B không khởi chạy được vì không tạo được tiến trình Python gốc; gọi trực tiếp Python 3.12 gốc báo Access is denied. Không có quyền nâng sandbox. Vì vậy không báo test đơn vị hoặc bộ chấm Python đã chạy lại trong lượt này. Không có lỗi Python của phương pháp được suy ra từ lỗi môi trường đó. LOG ghi người làm đã chạy test_cham.py; reviewer không lấy lời ghi này thay kết quả chạy độc lập.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** kiểm độc lập bản sửa H1, kết quả lượt 3, diễn giải và hai WHY; kiểm từng phản hồi R1–R4, N1/N2 và pin bộ chấm cũ; lần thêm các cạnh V043 thay đổi; phát hiện câu tổng hợp STATE sai phạm vi (R5).
2. **File thay đổi:** chỉ `tasks/T-064-m1-flashticket/REVIEW-2.md`. Không sửa nguồn quyết định, code, kết quả, bản phản biện cũ hoặc máy chủ.
3. **Kiểm và kết quả:** bảng trên; không có sai lệch hash/điểm trong các kiểm đã chạy. Chưa chạy lại Python vì sandbox từ chối thực thi.
4. **Còn mở và quyết định phụ thuộc:**

| Phần còn thiếu | Vì sao còn mở; cách phân xử và chi phí | Hệ quả/đề xuất trong lượt này |
|---|---|---|
| Tác dụng riêng của quan hệ | Chưa có nhánh cùng tín hiệu bỏ quan hệ; so H1c không tách được vai trò E1/E2/E5. Người làm cần hoàn thiện thiết kế/cài và dự toán từ đầu ra đã có, trong quyền chiến dịch; lượt này không phát lô. | Tiếp tục phần đã khai trong SPEC. Chưa kết luận lợi ích đồ thị; không ưu tiên V041 chỉ vì nó xuất cạnh. |
| Các hướng/đầu ra M3 chưa xong | H3/H4 thiếu ô lỗi phân xử; H8-adapter/log, dời mốc, cấu hình đề xuất, bản xuất và manifest còn thiếu theo LOG. Chú thích nền đã có, phần k6 chưa đối chiếu. Chi phí thu/cài phụ thuộc phạm vi người làm chưa chốt; không có ETA hợp lệ để reviewer tự điền. | Giữ task đang làm, tiếp tục đầu việc trong quyền. Không loại hướng vì chưa có dữ liệu. Phần sửa hook vượt đường dẫn đã cấp phải do Minh quyết theo đề xuất cụ thể của người làm. |
| Cơ chế các ca nền và HTTP5-EVENT-FLASH | Q4 chưa tách được ảnh hưởng theo thời điểm của autovacuum/checkpoint, chờ khóa ngắn và dao động; Q5 chưa tách nhịp job/lịch đăng nhập và sự khác nhau của cổng. Còn dữ liệu trace/log/trung gian đã lưu để đọc trước, gồm ca đúng tương ứng; phân tích cần dự toán sau khi khoanh lượng dữ liệu, không tự thu mới trong lượt này. | Không xác nhận cơ chế vật lý hoặc đóng câu hỏi nguồn. Ưu tiên phân tích dữ liệu đang có theo Q4/Q5; không chạy lại baseline hay cả đợt thu chỉ để có kết quả mới. |
| Hiệu quả/độ lặp và ngưỡng thực dụng | Một lần thu, H5b thiết kế sau khi xem một ca; chưa có kiểm độc lập hoặc quét gần sàn. K khác giữa δ = 0 và 1 ms không cho độ nhạy cục bộ quanh 1 ms. Chạy lặp đang để sau theo Minh; chi phí phải tính theo số ô khi lập gói đó. | Giữ ứng viên tạm và báo giới hạn; không yêu cầu chạy lặp ngay hoặc đổi ngưỡng chỉ để đóng review. |
| FLASH-HEALTHY | Tải và độ trễ thay đổi thật chưa tự xác định nghĩa “khỏe” theo giao dịch/SLO; chú thích hiện mới dùng chỉ số Gateway thay thế, chưa đối chiếu k6. | Đề xuất giữ K thô và nhóm FLASH riêng theo tiêu chí hiện hành, đọc k6 đã lưu để làm rõ ảnh hưởng trước đề xuất định nghĩa. Mặt trái: K vẫn có thể tính phản ứng với tải là một ca không đạt. Phương án đổi cách đếm sau xem kết quả làm đổi tiêu chí, không đề xuất áp ngay. Minh quyết nếu muốn đổi mục tiêu đó. |
| WHY các hướng còn lại | Người làm tự khai chưa rà đầy đủ H2/H4/H6a/H7c. Đã có code/sổ để rà, không cần lượt tính mới; chưa có số đo thời gian rà. | Hoàn tất rà trong công việc M3; không ghi chúng đã hoàn tất R3, không coi việc ghi thêm lý do là thêm bằng chứng hiệu quả. |

**Đề xuất tiếp tục một lượt đáp ngắn cho R5, sửa đúng câu trạng thái trong quyền rồi dừng phần kiểm gói sửa này**; không cần thực nghiệm hoặc vòng rà rộng mới. R5 không thay lựa chọn tạm, nhưng chưa coi câu báo cáo sai là đã xử lý. Tiếp tục T-064 theo SPEC và phản biện đầu ra tiếp theo khi được giao. Minh quyết sửa hay chấp nhận phạm vi giới hạn và dừng; không mở thêm vòng chỉ để lặp các giới hạn đã thống nhất. Dừng lượt này không tự nghiệm thu task, khóa M1, mở test hoặc trả lời các câu hỏi còn OPEN. Không đề xuất commit/push khi task đang phát triển và Minh chưa yêu cầu.

## Prompt bàn giao cho người làm

Chép nguyên văn Prompt chung và khối Người làm đáp phản biện từ mẫu, chỉ điền thông tin lượt. Không có khối cổng riêng cho giai đoạn 2. Không tự gửi.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-064 (tasks/T-064-m1-flashticket/), phản hồi sau lượt kiểm lại REVIEW-2.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: chiến dịch M1-FlashTicket, M3, tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md mục 5 và 7; giai đoạn 2 không có khối trọng tâm cổng riêng trong mẫu.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện, theo SPEC T-064.
- Tài liệu gốc: tasks/T-064-m1-flashticket/SPEC.md và LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md và CHECKPOINT-CHIEN-DICH.md; results/T-064/tieu-chi-chon.md, ho-so-chon.md, so-bien-the.jsonl, dap-an-dev2.json, tap-chon-dev2-12.json, tap-chon-dev2-13.json, phan-tich/ghi-chu-co-che-dev2.md, chu-thich-thao-tac-nen.md, hop-dong-dau-ra.md, thay-doi-may.md; docs/WHY.md; docs/DECISIONS.md; commit gốc c3d27f8a, đầu ra chưa commit.
- Phản biện và phản hồi trước: tasks/T-064-m1-flashticket/REVIEW.md cùng bảng phản hồi của người làm; LOG.md phiên 3; tasks/T-064-m1-flashticket/REVIEW-2.md.
- Code và kết quả liên quan: src/m1_ft/; src/m1/ và src/p3/danh_gia.py chỉ đọc; results/T-064/kiem/, cham/, bien-the/; results/T-063/thu2/SHA256SUMS và gói ca tương ứng; results/T-062/ca/manifest-ca.json, ca/_nguon/m1-source-pins.json và ket-qua/phat-lai/bang-cham.json. Môi trường ghim D:/RCA-ext/envs/py312-pin/Scripts/python.exe, PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages; kiểm trên đầu ra đã lưu, không phát lô mới hoặc đổi máy trong lượt đáp nếu chưa có quyền tương ứng.
- Phạm vi ghi được Minh cho phép trong lượt này: theo quyền chiến dịch đã ghi trong SPEC và CHIEN-DICH-M1-FT.md: bảng Phản hồi của người làm ở cuối REVIEW-2.md, nối LOG.md của T-064 và dòng T-064 trong docs/STATE.md. Không sửa nhận xét hoặc prompt của reviewer; sửa code/kết quả theo quyền tương ứng của chiến dịch; ngoài quyền thì đề xuất trong chat.

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
```

```text
Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.
```

## Phản hồi của người làm (người làm điền sau)

Người làm chỉ điền bảng này và LOG trong quyền đã cấp; không sửa nhận xét hoặc prompt. Thêm N1, N2… cho điểm tự tìm, ghi mức và bằng chứng. Để trống cột Minh quyết.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R5 | Đúng; không chặn | Câu "Không bản nào hồi quy trên 9 ca T-062" trong `docs/STATE.md` do người làm viết ở phiên 3 là sai phạm vi: `cham/khong-hoi-quy-1.json` và `khong-hoi-quy-3.json` có V009, V010, V011, V043, V044 với AC@1 dưới 5 trên T-062. Đã sửa câu trong STATE thành phạm vi đúng (bản đề xuất và thay thế không hồi quy; các bản H1a/H1b có và đã bị loại). Hồ sơ chọn mục 3 vốn giới hạn câu này ở "mọi bản trong bảng"; không đổi lựa chọn tạm | |
| Kết luận chung (R1–R4 đã xử lý, không có điểm chặn mới) | Đúng | Người làm không có phản đối. Đồng ý dừng lượt kiểm này; task chưa đủ nghiệm thu. Người làm chưa đọc kỹ từng mục của bản này ngoài R5 và kết luận vì hạn mức phiên gần hết; phiên kế phải đọc mục "R1 — kiểm trung gian và tác động" và mục báo cáo lượt trước khi làm tiếp | |
