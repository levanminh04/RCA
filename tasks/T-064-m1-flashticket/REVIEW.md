# Phản biện T-064 — lượt 1

- **Người phản biện:** Codex — **Ngày:** 14/11/2026 — **Commit/diff đã đọc:** gốc `c3d27f8a`; code và đầu ra T-064 chưa commit. Đối tượng chính là `results/T-064/ho-so-chon.md`, bản nháp 1 ghi 13/11 22:40Z. Không xét đây là hồ sơ nghiệm thu task.
- **Công đoạn/cổng và bản lượt:** soát kết quả giữa chừng, M3 chiến dịch M1-FlashTicket; chỉ ghi bản mới `tasks/T-064-m1-flashticket/REVIEW.md` theo brief của Minh. Không sửa LOG, STATE, code, kết quả hay máy chủ.
- **Đã đọc:** AGENTS; STATE; SPEC và LOG T-064; hồ sơ chiến dịch và checkpoint T-062; mục tiêu MRP, DT18, hướng dẫn cô, LESSONS; WHY-81–84 và quyết định chiến dịch ngày 13/11. Đã đọc tiêu chí, hồ sơ chọn, sổ biến thể, đáp án, hai tập chọn, ghi chú cơ chế, sổ thay đổi máy, hợp đồng đầu ra; code `src/m1_ft/`, các đường liên quan trong `src/m1/` và `src/p3/danh_gia.py`; script chấm/giữ-bỏ/kiểm/nhận/phát lượt; bảng điểm hai lượt và không hồi quy; manifest T-063/T-062 và đầu ra gốc liên quan. Đọc trace thật của ca `98ea5ba4` để kiểm loại cạnh; đối chiếu trung gian các ca sai và ca đúng.
- **Tự soát độc lập:** đọc nguồn, bộ chấm và đầu ra gốc trước khi lập findings. Không có REVIEW trước của T-064 để lấy làm kết luận. Dùng JavaScript qua `mcp__node_repl.js` để kiểm hash và tính độc lập trên JSON. Không chạy lô phương pháp mới, không đọc `data/locked/`, không dùng ô đánh giá.

## Kết luận chung

Bốn bảng điểm dev và hai bảng không hồi quy khớp đầu ra đã lưu trong dung sai tiêu chí; chưa thấy sai số tổng hợp làm đổi hai bản đứng đầu được hồ sơ nêu. Có ba điểm chặn **các phần kết luận/đề xuất tương ứng**: H1 trộn sai loại cạnh, gọi phép bỏ H1c là bỏ quan hệ, và thiếu hồ sơ WHY cho những lựa chọn quyết định ứng viên. Các phần chưa làm đã khai ở mục 7 không tự là lỗi của lượt giữa chừng; hiện chưa đủ nghiệm thu M3, khóa ứng viên hoặc trả lời RQ5.

## Các điểm

### R1. H1 gộp message vào HTTP trước khi tính điểm cạnh — CHẶN

- **Ở đâu:** `src/m1_ft/thanh_phan/h1_canh.py:82–87`, hàm `CanhDuLieu.ra`; `src/m1/span.py:164–174`; đầu ra H1a/H1b/H1c.
- **Sai gì:** `mau_canh` gộp theo cặp chủ `(a,b)`, không phân loại giao thức. H1 nhận kết quả này rồi gán toàn bộ `loai = "http"`. Nhưng trace tải mua vé có cả quan hệ PRODUCER → CONSUMER. Một cặp còn chứa đồng thời HTTP và message, nên đây là lỗi dữ liệu đi vào phép tính, không chỉ sai nhãn hiển thị.
- **Bằng chứng:** ca đã khớp SHA trong `results/T-063/thu2/ca/98ea5ba4.tgz`:
  - `outputs/98ea5ba4/method-input.json` có 162.228 span. Ghép đủ thông tin loại cho 162.228 span từ `cases/98ea5ba4/raw-traces.jsonl`.
  - Lặp đúng điều kiện span bọc của `span.chuan_bi` cho tuyến Payment → Booking: **72 mẫu CLIENT → SERVER và 144 mẫu PRODUCER → CONSUMER**, tất cả ở N. H1 xuất một cạnh `http` với `n_N = 216`, `n_A = 0`.
  - Booking → Payment có **144 mẫu PRODUCER → CONSUMER**, nhưng được xuất `http`, `n_N = 144`. Payment → Ticket và Ticket → Payment mỗi tuyến **72 mẫu message**, cũng được xuất `http`.
  - Ví dụ nguồn: `PaymentWorker.publishOutbox` → `business.ex publish` (kind 4, scope RabbitMQ) → `booking.accept-payment.v1 process` (kind 5, scope Spring Rabbit, queue `booking.accept-payment.q`). Phụ lục A ghi phép đếm đã chạy và kết quả.
  - Đối chiếu đầu ra: `results/T-064/cham/dau-ra-dev2/V028-H1c+H8s1/98ea5ba4/method-output-1.json#/extra/m1_ft/canh_xep_hang`, lọc theo `nguon`, `dich`, `loai`; các mẫu số trên khớp. Định nghĩa PRODUCER/CONSUMER tách khỏi CLIENT/SERVER ở [OpenTelemetry SpanKind](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind).
- **Phần có thể phản bác finding:** P7 cũng dùng helper này và H1 đã bổ sung cạnh service → broker. Điều đó không làm helper trở thành bộ phân loại HTTP; cạnh tới broker không tách 144 mẫu message khỏi 72 mẫu HTTP đã bị gộp. Chưa có bằng chứng lỗi này làm sai ba cạnh đáp án hoặc làm đổi bản đứng đầu; không suy số điểm hiện tại phải đổi.
- **Bước và quyết định chịu ảnh hưởng:** lỗi đã xảy ra trong đọc → nhóm mẫu → tính điểm → xuất cạnh. Chặn xác nhận H1 có đồ thị đúng loại và việc dùng nguyên đầu ra cạnh đó làm bản đề xuất/giao diện cuối. Điểm nút thuần P7/H8 không phụ thuộc H1 vẫn dùng được trong phạm vi đã kiểm. Lỗi kiểu cạnh còn làm yếu diễn giải các bản H1 bị loại.
- **Đề xuất sửa tối thiểu:** tách mẫu theo loại đã xác minh **trước** khi gộp/chấm ở nhánh H1; giữ riêng quan hệ message và HTTP, hoặc khai loại chưa xác định nếu chưa có căn cứ. Không sửa `src/m1/`. Giữ nguyên lượt cũ; người làm khoanh các đầu ra H1 và kết luận bị ảnh hưởng, trình phần tính lại cần thiết. Ưu tiên dùng đầu vào đã lưu, không thu lại dữ liệu chỉ vì sửa phân nhóm. Không đổi tiêu chí chấm.
- **Pin và tác động:** `h1_canh.py` nằm trong `sha_ma_nguon()` của cả gói, đã được sổ biến thể và summary ghim cho hai lượt. Sửa file làm đổi hash cây mã; không ghi đè kết quả/sổ cũ hoặc báo kết quả sửa là kết quả ban đầu. Những cấu hình không bật H1 cần xét tương đương để dùng lại, không mặc định chạy lại cả 37 bản. Phản biện này chưa chạy bản sửa nên chưa có chi phí thực đo cho phần tính lại.

### R2. V002–V028 không phải đối chứng bỏ quan hệ; H1c không phải điều kiện để phương pháp dùng đồ thị — CHẶN

- **Ở đâu:** `results/T-064/ho-so-chon.md:89` và `:141`, mục 4 và 8.
- **Sai gì:** hồ sơ vừa gọi V002 so với V028 là đối chứng “bỏ quan hệ”, vừa nói V028 “cần” cho mục tiêu đồ thị có vai trò tính toán. Hai câu gộp việc **thêm đầu ra cạnh H1c** với việc **dùng quan hệ trong phương pháp**.
- **Bằng chứng:**
  - Cấu hình `bien-the/V002-H8s1/cau-hinh.json` chỉ thêm sàn H8; nó không tắt E1/E2/E5 của P7. Đầu vào thật ca `98ea5ba4` trong gói đã băm có `inputs[6].bat_tat = {E1: "U", E2: "C", E5: true, E6: "a", ...}`.
  - V002 ở ca này vẫn có **18 quan hệ**, **12 đơn vị `canh|...`** và **52 bản ghi kế thừa**: `.../V002-H8s1/98ea5ba4/method-output-1.json#/extra/canh`, `/extra/don_vi_phan_vi`, `/inherited_by`. Lệnh đếm toàn ba mảng đã chạy qua Node.
  - `src/m1/chuoi.py:342–355` dùng quan hệ để tính mẫu độc quyền và bằng chứng cạnh; `:585–594` dùng E5 và `F_I` trước xếp hạng. Đây cũng là vai trò đã ghi ở WHY-72/74, không do H1c tạo ra.
  - Trung gian ca `4af494a5` còn cho một đường tính cụ thể: P7 coi hai kênh latency-50/90 của Event là kế thừa theo đường Event → Keycloak, gắn với `OutboxDrainerTask.run`; sau H8 bỏ cờ thao tác này, `F_I` của hai kênh Event đổi **0 → 1**, điểm lớn nhất của Event đổi khoảng **650,55 → 988,12**. Nguồn: hai output P7 và V002 của ca đó, `/inherited_by`, `/extra/kenh_co` và `/entity_ranking`. Điều này xác nhận quan hệ vẫn tham gia tính trong V002; chưa cô lập lợi ích riêng của quan hệ.
  - Kiểm đủ 13 ca: thứ tự `(entity, tie_group)` của V002 và V028 trùng **13/13**, đúng với việc H1c là hậu xử lý `ra`. Kết quả này chỉ phân xử phần tăng thêm của H1c trên nền P7 đang dùng đồ thị.
- **Phần có thể phản bác finding:** hồ sơ đã giới hạn “không rút lợi ích đồ thị nói chung” và phân biệt điểm nút với phép chiếu. Phần ấy đúng. Nhưng câu gọi đối chứng và lý do buộc có H1c vẫn sai, có thể khiến Minh chọn bản khác vì tưởng V002 không đáp ứng DT18.
- **Bước và quyết định chịu ảnh hưởng:** lỗi diễn giải đã xảy ra, chặn dùng cặp này để kết luận tác dụng của bỏ quan hệ hoặc lấy DT18/luật 18 làm lý do bắt buộc chọn V028. Không chặn báo đây là phép thêm/bỏ H1c hay giữ bản có đầu ra cạnh làm lựa chọn phục vụ giao diện.
- **Đề xuất sửa tối thiểu:** đổi tên phép so thành “thêm/bỏ H1c trên nền P7 có quan hệ”; nêu rõ các phép tính đồ thị V002 vẫn giữ. Lý do giữ bản thay thế V028 là đầu ra cạnh và nhu cầu giao diện, cùng đánh đổi đã đo. Đối chứng bỏ quan hệ theo câu hỏi trong SPEC còn chưa được phép so này bao phủ; ghi phần thiếu và quyết định phụ thuộc. Không yêu cầu chạy đối chứng mới trong lượt phản biện này hoặc bắt đồ thị phải thắng mới được chọn ứng viên.
- **Pin và tác động:** sửa diễn giải trong hồ sơ không làm đổi code hay đầu ra hai lượt. Không sửa tiêu chí đã khóa để ưu tiên bản có H1c sau khi xem điểm.

### R3. Những lựa chọn quyết định ứng viên chưa có WHY; lý do vật lý của sàn chưa được xác nhận — CHẶN

- **Ở đâu:** `docs/WHY.md` hiện kết thúc ở WHY-84; `src/m1_ft/thanh_phan/h8_san.py:11–14`; `h4_h5.py:119–170`; hồ sơ chọn mục 3–4.
- **Sai gì:** ít nhất sàn **1 ms** của H8 và quy tắc H5b **chết im 60 s → đưa lên nhóm đầu** đã dùng trong kết quả và đề xuất chọn, nhưng không có mục WHY. Docstring, LOG và sổ biến thể có giải thích, song không thay nghĩa vụ ghi lựa chọn quan trọng vào nguồn này **trước** khi dùng kết quả. Quyền tự quyết chiến dịch cấp quyền chọn và ghi WHY, không miễn nghĩa vụ đó.
- **Bằng chứng:**
  - Rà toàn `docs/WHY.md`: các mục từ WHY-81 chỉ gồm nơi chạy, H1c, thay ô thu và revision thu; không có mục cho H8/H5b. Tìm các chuỗi `H5b`, `H8s1`, `H8-san`, `1 ms`, `sàn độ lớn`, rồi đọc bốn mục cuối.
  - Hồ sơ chọn V002 trên A vì H8 làm K **4 → 3**; cùng lúc CPU-BOOK-2 tụt hạng **1 → 2**. Nguồn: `cham/chon-dev2-luot1-tap12.json#/ban/{P7,V002-H8s1}`, `/ca/60166807`; `.../V002-H8s1/60166807/method-output-1.json#/extra/m1_ft/chu_thich/H8-san/don_vi_bo_co` cho hai độ vượt bị bỏ khoảng **411 và 506 µs**. Vì vậy đây là lựa chọn ảnh hưởng trực tiếp chất lượng, không phải chi tiết trình bày.
  - Trên B, V032 đứng đầu vì H5b đưa PAUSE-PAYMENT lên hạng **1**; đầu ra cũ H5 cho hạng **4**: `cham/chon-dev2-luot2-tap13.json#/ban/{V032-H5b,V036-KC-V018}/ca/46aab4be`.
  - Lý do hiện tại của H8 nói dịch nhỏ hơn hạt lập lịch CFS “không phân biệt được với nhiễu lập lịch”. [Tài liệu CFS chính thức](https://docs.kernel.org/scheduler/sched-design-CFS.html) mô tả granularity nhằm hạn chế chuyển tác vụ và accounting theo ns; nó không xác lập sàn 1 ms để phân biệt lỗi với nhiễu của phép đo này. Không có số đo trong hồ sơ xác nhận suy diễn đó trên máy thu. Đây là **suy luận chưa kiểm**, không phải định luật để hợp thức hóa ngưỡng.
- **Phần có thể phản bác finding:** H8/H5b đều có nguyên lý, điều kiện thất bại và khai lịch sử xem dev; H8 cũng đã thừa nhận bỏ mất lỗi thật nhỏ. Những điều đó có ích và không bị phủ nhận. Việc chưa có WHY không chứng minh tác giả chọn ngưỡng theo nhãn, cũng không làm sai phép cộng điểm. Tuy nhiên hồ sơ chưa đủ nguồn lý do cho hai lựa chọn đang quyết định ứng viên; chép nguyên lời biện minh CFS vào WHY sẽ chưa giải quyết phần căn cứ.
- **Bước và quyết định chịu ảnh hưởng:** thiếu sót đã xảy ra trước bước chọn. Chặn coi hồ sơ lý do lựa chọn là hoàn chỉnh để chốt đề xuất M3. Không chặn giữ nguyên kết quả mô tả và tiếp tục phần công việc độc lập.
- **Đề xuất sửa tối thiểu:** thêm mục WHY ở cuối theo quyền chiến dịch, ghi **thời điểm bổ sung thực**, truy vết nguyên lý đã ghi trước trong code/sổ, phương án khác, điều kiện thất bại và các quyết định phụ thuộc. Rà cả các lựa chọn quan trọng H1–H8 khác cùng nghĩa vụ này. Với H8, đề xuất giữ 1 ms ở trạng thái ngưỡng thực dụng của ứng viên dev, công khai giả thuyết CFS chưa kiểm và đánh đổi đã thấy; không tuyên bố đã xác định nguồn nhiễu. Phương án đổi/lựa thêm ngưỡng là thiết kế tiếp trên dev, cần khai đúng lịch sử và phạm vi; không cần chạy thêm chỉ để vá một câu biện minh.
- **Pin và tác động:** WHY là tài liệu sống, không thuộc cây hash code T-064. Chỉ thêm WHY không đổi kết quả lịch sử. Sửa docstring trong `h8_san.py` cũng làm đổi hash cây mã vì hàm băm đọc cả byte tệp; phải giữ pin cũ và ghi tác động, không tự băm lại lượt cũ như thể chạy bằng mã mới.

### R4. Hồ sơ bỏ sót quyết định đã cho áp dụng tiêu chí chọn — KHÔNG CHẶN

- **Ở đâu:** `results/T-064/ho-so-chon.md:84`; checkpoint 22:29Z; `docs/DECISIONS.md:573–586`.
- **Sai gì:** hồ sơ nói chưa thấy xác nhận thứ tự §5 và tiếp tục đưa xác nhận này vào phần chờ Minh, nhưng DECISIONS đã ghi cho Claude “áp dụng tiêu chí chọn đã trình tại `results/T-064/tieu-chi-chon.md`, tự chọn biến thể, tổ hợp và ứng viên theo tiêu chí ấy”. Bổ sung SPEC cũng yêu cầu tự chọn trong quyền, không chờ Minh chọn thay.
- **Bằng chứng:** mục “Bổ sung quyền điều phối chiến dịch nhiều ngày, 13/11/2026”, đặc biệt dòng 579. Hồ sơ chiến dịch mục 9 còn nói bốn điểm từng chờ đã được xử lý và chỉ hỏi phần vượt quyền. Câu cũ trong tiêu chí là lịch sử trước bổ sung, không phải quyết định mới hủy quyền đã cấp.
- **Phần có thể phản bác finding:** nếu muốn đổi tiêu chí để ưu tiên K hoặc đầu ra cạnh sau khi thấy điểm, vẫn phải trình Minh. Minh cũng vẫn quyết xem xét ứng viên cuối. Finding chỉ phản đối việc gọi **áp dụng tiêu chí đang có** là thiếu xác nhận.
- **Bước và quyết định chịu ảnh hưởng:** sai trạng thái nguồn quyết định; có thể gây chờ hoặc đưa lựa chọn đã được giao tự quyết về Minh dưới một lý do không đúng. Không đổi các số đã chấm, không tự phê duyệt tập B hay thay tiêu chí.
- **Đề xuất sửa tối thiểu:** trong báo cáo/checkpoint lượt tiếp, dẫn đúng quyền đã cấp, giữ thứ tự §5 hiện hành. Nếu đề nghị chọn khác thứ tự đó, ghi rõ đây là đề nghị đổi sau khi xem kết quả, có lý do và mặt trái. Không sửa tại chỗ file tiêu chí đang khóa chỉ để xóa câu lịch sử. Tập B và định nghĩa FLASH-HEALTHY là các câu hỏi khác.
- **Pin và tác động:** sửa trạng thái trong báo cáo/checkpoint không đổi đầu ra tính toán; sửa tiêu chí sẽ làm lệch `tieu_chi_sha256` được bốn bảng điểm ghim, nên không làm việc ấy để “đồng bộ” quá khứ.

## Đối chiếu các lượt trước

Chưa có phản biện chính thức trước của T-064. Hồ sơ chỉ ghi tiêu chí từng được góp ý trong chat; không có đủ nguyên văn các lượt đó ở tập nguồn này để đánh giá từng ý. Không suy từ việc tiêu chí đã qua góp ý rằng cách cài hoặc toàn bộ diễn giải đã được xác nhận. Đây không phải lượt mở lại T-063 hay các task đã đóng.

## Tuân thủ quy trình

- Vai trò đúng SPEC: Claude làm, Codex phản biện. Brief cho phép đúng file này. Không có sửa thay người làm, commit, truy cập máy hoặc phát thực nghiệm.
- Tiêu chí khớp pin ở cả bốn bảng điểm; 37 cấu hình khớp giá trị băm canonical trong sổ; sổ có 104 dòng, gồm 27 và 10 bản đăng ký chọn. Lượt 2 có khai đã xem lượt 1 và ca thử trên tập chọn. Không có căn cứ cáo buộc đổi tiêu chí ngầm.
- Chỉ thấy nhãn trong nhánh chấm. Phương pháp nhận đầu vào kỹ thuật, cấu hình và mốc `t` của chế độ a; code đọc request chỉ lấy `t`. Tên ô và đáp án không được truyền vào đường tính đã đọc. Đây là kiểm đường chạy liên quan, không phải chứng minh mọi byte của tất cả gói không thể mang thông tin nhãn.
- Không thấy thay đổi `src/m1/`, `src/p3/` so với commit gốc ở diff đã kiểm; 39 pin nền P7 khớp. Các thay đổi tài liệu đang có thuộc nhiều task; không quy toàn bộ working tree cho T-064. Thiếu WHY có ảnh hưởng cụ thể được ghi ở R3.
- STATE đang ở mốc cũ hơn LOG/hồ sơ. Brief hiện tại đã chỉ rõ review kết quả giữa chừng và bản nháp; không dựa vào STATE cũ để phủ nhận đầu ra đã tồn tại hoặc tự cập nhật nó.

## Điều đã kiểm và thấy đúng

| Phép kiểm đã chạy qua Node, chỉ đọc | Kết quả |
|---|---|
| SHA theo `results/T-063/thu2/SHA256SUMS` | 214/214 khớp |
| SHA theo `results/T-062/ca/manifest-ca.json#/files` | 28/28 khớp |
| `results/T-062/ca/_nguon/m1-source-pins.json#/pins` | 39/39 khớp |
| Nguồn xác nhận hai tập chọn và hai nguồn đáp án | Khớp giá trị băm khai trong JSON |
| SHA của hai output so với `summary.json#/output_sha256` | Dev: 481/481 cặp; không hồi quy: 333/333 cặp; không lệch, hai output bằng byte, summary OK |
| SHA đầu ra mà bốn bảng dev dẫn | 975/975 tham chiếu khớp; tiêu chí, đáp án và tập chọn cũng khớp pin |
| Gói nhận lượt 2 so `kiem/nhan-luot2/luot2-out.sha256` | Khớp |
| Tính độc lập min hạng tập chấp nhận dưới hoán vị đều, phép chiếu, AC@1/3, hạng cắt, K | Khớp cả 78 bản-tập trong bốn bảng dev với dung sai 1e-9; đây là tính đối chiếu bằng JS, không phải chạy lại Python |
| Tính độc lập bảng cạnh từ danh sách cạnh đã xuất | 234 phép chấm ca-cạnh khớp bảng dev; không chứng minh danh sách đầu vào đúng loại (R1) |
| Tính độc lập từ P7 gốc T-062 rồi chấm 37 × 9 đầu ra không hồi quy | Mốc P7: AC@1 = 5, AC@3 = 5, tổng hạng = 5, K = 4; 333/333 ca biến thể khớp bảng đã lưu |
| V035/V036/V037 so V015/V018/V019, bỏ đúng metadata đã khai | Mỗi cặp trùng 13/13 dev và 9/9 T-062 |
| Cấu hình đang có và sổ trước chấm | 37/37 hash cấu hình khớp; cây mã hiện tại khớp giá trị lượt 2 |
| Rà ca tụt hơn 2 bậc trong các phép GIỮ thêm-riêng/bỏ-khỏi-gộp lượt 1 và các phép lượt 2 | Không có phép được GIỮ nào vi phạm trên dữ liệu đã chấm |

**Giới hạn tái chạy:** venv ghim không khởi động được vì Python nền tại hồ sơ người dùng bị sandbox trả `Access is denied`; `py` cũng không có trong PATH. Không chạy được `test_cham.py` hoặc nguyên script Python chấm trong lượt này. Không tự sửa venv hoặc chạy trên môi trường khác rồi gọi đó là tái lập môi trường ghim.

**Pin bộ chấm lịch sử:** `cham/t062-p7.json#/cham_py_sha256` lệch `src/m1_ft/cham.py` hiện tại. Đã dừng dùng riêng tổng hợp ấy, báo Minh trong lượt và kiểm lại từ P7 gốc có manifest: số từng ca, hash output và tổng đều khớp. LOG cho thấy bộ chấm có được bổ sung sau bước chấm P7 đầu; chưa khôi phục byte bộ chấm lịch sử để xác minh chính hash đó. Vì vậy dùng phép tính độc lập trên nguồn đã băm cho đối chiếu không hồi quy, không nhận là đã tái chạy đúng revision bộ chấm lịch sử. Không có bằng chứng số P7 bị sai và không yêu cầu chạy lại phương pháp chỉ vì pin lịch sử này.

Các bảng chính V002/V028/V034 và mức phạt do phép chiếu khớp file thật. Giữ cách báo hiện tại là hệ quả quy ước chấm, không tự biến chênh 1,0 thành suy giảm thứ tự nút. Không có căn cứ chọn lại ngưỡng hoặc đổi quy tắc chấm từ phép kiểm này.

## Phụ lục A — phép đếm loại cạnh đã chạy

Đọc gói `98ea5ba4.tgz` đã kiểm SHA trong bộ nhớ bằng `node:zlib`, duyệt header tar; không giải nén ra repo. Parse `method-input.json`, lập map `(traceID, spanID)` và thông tin phụ từ raw trace. Sau đó chạy lõi đếm dưới đây qua `mcp__node_repl.js` (`inp` là đầu vào, `phu` là map kind đã ghép đủ). Đây là phép kiểm dữ liệu đã lưu, không chạy M1 mới.

```javascript
const spans = new Map(inp[0].map(s => [s.traceID + '|' + s.spanID, s]));
const children = new Map();
for (const s of inp[0]) {
  const pk = s.traceID + '|' + s.parentSpanID;
  if (!spans.has(pk)) continue;
  if (!children.has(pk)) children.set(pk, []);
  children.get(pk).push(s);
}
const counts = {};
for (const s of inp[0]) {
  const key = s.traceID + '|' + s.spanID;
  const cs = children.get(key) || [];
  const par = spans.get(s.traceID + '|' + s.parentSpanID);
  if (cs.length !== 1 || cs[0].owner === s.owner || !par || par.owner !== s.owner) continue;
  const a = inp[4][s.owner] || s.owner;
  const b = inp[4][cs[0].owner] || cs[0].owner;
  const kind = phu.get(key).kind + '->' + phu.get(cs[0].traceID + '|' + cs[0].spanID).kind;
  const side = s.start_us + s.duration_us < inp[5] * 1e6 ? 'N' : 'A';
  counts[a + '|' + b] ??= {};
  counts[a + '|' + b][kind] ??= {N: 0, A: 0};
  counts[a + '|' + b][kind][side]++;
}
```

Kết quả tuyến liên quan:

| Tuyến | CLIENT → SERVER N/A | PRODUCER → CONSUMER N/A | H1 xuất loại và mẫu số |
|---|---:|---:|---|
| Payment → Booking | 72/0 | 144/0 | http, 216/0 |
| Booking → Payment | 0/0 | 144/0 | http, 144/0 |
| Payment → Ticket | 0/0 | 72/0 | http, 72/0 |
| Ticket → Payment | 0/0 | 72/0 | http, 72/0 |

Đếm này xác nhận lỗi trên một ca đủ phản ví dụ; chưa ước lượng tỷ lệ lỗi loại cạnh của toàn tập. Không lấy một ca làm tỷ lệ phổ quát.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** soát hai lượt chọn và hồ sơ nháp từ code, manifest, JSON và trace gốc. Tách kiểm đúng số khỏi kiểm ý nghĩa phương pháp/đồ thị và quyền quyết định.
2. **File đã thay đổi:** chỉ `tasks/T-064-m1-flashticket/REVIEW.md`. Không thêm quyết định cho Minh, không đổi code/kết quả/tiêu chí, không commit. Các đề xuất sửa ở trên chưa được thực hiện.
3. **Kiểm đã chạy:** bảng kiểm ở trên. Không chạy được Python ghim; phép đối chiếu JS có giới hạn đã khai. Không chạy thực nghiệm mới hoặc đổi máy.
4. **Bất đồng/câu hỏi mở và đề xuất:**
   - **Đề xuất tiếp tục phản biện** qua một lượt Claude đáp R1–R4 trước khi dùng hồ sơ để chốt M3. R1–R3 còn ảnh hưởng phần đề xuất; chưa có phản hồi người làm để nói đã thống nhất. Chưa cần mở thêm lô thực nghiệm trong lượt đáp; trước hết khoanh ảnh hưởng trên dữ liệu đã có và trình sửa tối thiểu.
   - **Tập A/B:** đề xuất chấp nhận sửa điều kiện Docker để B là tập dev có PAUSE, vì nguồn đầu dò và định nghĩa cờ đã chỉ ra lỗi chép; giữ A nguyên để báo độ nhạy, khai sửa sau. Mặt trái: sửa điều kiện sau xem dữ liệu và H5b đã được thiết kế trên ca ấy, nên không có bằng chứng độc lập cho H5b. Phương án chỉ A giữ quy tắc cũ nguyên vẹn nhưng loại một can thiệp đã có bằng chứng. Đây là đề xuất, Minh chưa quyết; không tự đổi tập chọn.
   - **FLASH-HEALTHY:** đề xuất giữ K đếm thô và báo nhóm FLASH riêng đúng tiêu chí hiện hành. Muốn thay định nghĩa khỏe cần căn cứ ảnh hưởng giao dịch và quyết định riêng; độ trễ tăng đơn lẻ chưa phân xử được nhiễu, tải có chấp nhận được hay sự cố thật. Chú thích nền/dời mốc và số giao dịch đã lưu là phần cần hoàn thiện trong task; chạy lặp là phần chiến dịch để sau. Không tự gán lại nhãn để giảm K.
   - **Ứng viên:** đề xuất giữ kết quả thứ tự §5 là kết quả tạm theo từng tập, không đổi thứ tự để H1c thắng. Với A, V002 đang đứng đầu; nếu Minh nhận B thì V032 đang đứng đầu. Việc triển khai ứng viên cuối còn phụ thuộc R1–R3, các hướng chưa hoàn tất và đầu ra còn thiếu. Bản có cạnh có thể là lựa chọn giao diện, không phải điều kiện cứu tính đồ thị của P7. Mặt trái của thứ tự đang có là K đứng sau xếp hạng; phương án ưu tiên K là đổi tiêu chí sau khi xem và phải khai như vậy.
   - **Cơ chế và phạm vi nguồn:** phần mềm đã giải thích được một số đổi cờ/đổi hạng (đặc biệt CPU-BOOK-2, PAUSE và định vị cạnh bị tài nguyên lấn). Các nguồn nhịp Keycloak, cờ nền và vai trò tải vẫn còn giả thuyết khác. Q5 có thể lần thêm trên raw trace và code G3 đã lưu; chưa có chi phí thực đo, chưa có lý do đòi thu lại toàn bộ. H3/H4 thiếu ô phân xử, H8-adapter/H8-log, phép dời mốc, xuất ứng viên và manifest còn là công việc của M3, không được coi là đã hoàn thành bởi lượt review này. Chưa kết luận hiệu quả độc lập, lợi ích đồ thị tổng thể hoặc RQ5.

Minh quyết sửa, chấp nhận giới hạn hoặc gửi tiếp. Dừng phản biện về sau không tự nghiệm thu task, khóa M1, mở test hay duyệt giả thuyết. Nội dung cần đưa vào tài liệu chính thức khi được phép là phân loại cạnh, phạm vi đối chứng, lý do thiết kế và trạng thái quyết định; không chỉ giữ trong chat.

## Prompt bàn giao cho người làm

Prompt dưới chép nguyên văn mẫu hiện hành, điền thông tin trung tính; không tự gửi. Quyền sửa kết quả không được mở rộng bởi bản phản biện này.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-064 (tasks/T-064-m1-flashticket/), hai lượt chọn trên dev bản 2 và results/T-064/ho-so-chon.md bản nháp 1.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: chiến dịch M1-FlashTicket, M3; giai đoạn 2 không có khối trọng tâm cổng riêng trong mẫu hiện hành.
- Người làm và người phản biện chính thức: Claude là người làm; Codex là người phản biện chính thức theo SPEC T-064.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; tasks/T-064-m1-flashticket/SPEC.md và LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md và CHECKPOINT-CHIEN-DICH.md; results/T-064/tieu-chi-chon.md, ho-so-chon.md, so-bien-the.jsonl, dap-an-dev2.json, tap-chon-dev2-12.json, tap-chon-dev2-13.json, phan-tich/ghi-chu-co-che-dev2.md, thay-doi-may.md, hop-dong-dau-ra.md; docs/WHY.md và docs/DECISIONS.md; commit gốc c3d27f8a và đầu ra chưa commit.
- Phản biện và phản hồi trước: tasks/T-064-m1-flashticket/REVIEW.md (lượt 1); chưa có phản hồi chính thức của người làm.
- Code và kết quả liên quan: src/m1_ft/; src/m1/ và src/p3/danh_gia.py chỉ đọc; results/T-064/bien-the/, cham/, kiem/; results/T-063/thu2/SHA256SUMS, results/T-063/chay/xac-nhan-ca.json, xac-nhan-ca-2.json và dieu-kien-xac-nhan.md; results/T-062/ca/manifest-ca.json; results/T-059/danh-muc-loi.json. Môi trường ghim D:/RCA-ext/envs/py312-pin/Scripts/python.exe, PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages. Chỉ chạy lại bộ chấm và test đơn vị trên đầu ra đã lưu khi môi trường cho phép, ghi đầu ra thử vào thư mục tạm ngoài repo; không phát lô biến thể mới, không đổi máy, không đọc dữ liệu khóa hoặc ô đánh giá trong lượt đáp.
- Phạm vi ghi được Minh cho phép trong lượt này: đối chiếu quyền Minh đã cấp cho người làm trong chiến dịch và yêu cầu lượt đáp. Phần phản hồi theo vai trò là bảng “Phản hồi của người làm” cuối tasks/T-064-m1-flashticket/REVIEW.md, LOG.md cùng task và dòng T-064 trong docs/STATE.md khi quyền hiện hành cho phép. Không sửa nhận xét hay prompt của reviewer; bản phản biện không tự cấp quyền sửa code, kết quả, SPEC hoặc tiêu chí theo finding. Nếu chưa có quyền ghi rõ ràng cho lượt đáp thì chỉ trả lời trong chat.

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
```

## Phản hồi của người làm (người làm điền sau)

Người làm chỉ điền bảng này và LOG trong quyền được duyệt; không sửa nhận xét hay prompt của người phản biện. Thêm N1, N2… cho điểm tự tìm được, nêu CHẶN/KHÔNG CHẶN và bằng chứng. Để trống cột Minh quyết. Prompt của lượt đáp nằm trong mục LOG mới hoặc chat.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; chặn việc dùng đầu ra cạnh của H1 làm bản đề xuất hoặc giao diện cuối | Kiểm lại trên file: `V028-H1c+H8s1/98ea5ba4/method-output-1.json#/extra/m1_ft/canh_xep_hang` có Payment → Booking `http` 216/0, Booking → Payment 144/0, Payment → Ticket 72/0, Ticket → Payment 72/0 — khớp số người phản biện. Code `h1_canh.py` gán loại `http` cho mọi cặp từ `mau_canh`. Người làm chưa tự đếm lại kind trong raw trace. Khoanh phạm vi (đếm trên V028, 22 ca): 4 cạnh sai loại ở 13/13 ca dev bản 2, 0 ở T-062; không cạnh nào có cờ. Chưa biết tách mẫu có sinh cờ mới không. Chưa sửa mã; kế hoạch sửa và phạm vi bản bị ảnh hưởng ở `results/T-064/ho-so-chon.md` mục 9 | |
| R2 | Đúng; chặn hai câu diễn giải | Người làm gọi sai tên phép so. V002 chỉ thêm sàn H8, không tắt quan hệ của P7. Đã sửa mục 4 và 8 của hồ sơ: phép so là thêm/bỏ H1c trên nền P7 có quan hệ; lý do giữ V028 là đầu ra cạnh cho giao diện. Phần thiếu: đối chứng bỏ quan hệ mà SPEC hỏi chưa chạy trong T-064; kết luận về tác dụng của quan hệ còn mở | |
| R3 | Đúng; chặn coi hồ sơ lý do là hoàn chỉnh | `docs/WHY.md` dừng ở WHY-84, không có mục cho H8 sàn và H5b (grep 0 kết quả) dù cả hai đã dùng trong kết quả — người làm vi phạm luật cứng 3. Đã thêm WHY-85 và WHY-86 ở cuối, ghi rõ là ghi muộn và dẫn nguyên lý có trước trong docstring/sổ. Đồng ý lý do CFS là suy luận chưa kiểm: WHY-85 ghi 1 ms là ngưỡng thực dụng. Chưa rà đủ các lựa chọn H2, H4, H6a, H7c (các hướng này không vào bản đề xuất); chưa sửa docstring để không đổi hash mã | |
| R4 | Đúng; không chặn | DECISIONS dòng 579 đã giao áp dụng tiêu chí. Người làm đọc câu lịch sử trong file tiêu chí thành việc còn chờ. Đã sửa hồ sơ mục 4 và mục 9: bản đề xuất theo §5 là V002 (tập A), V032 nếu Minh nhận tập B. Không sửa file tiêu chí đang khóa | |
| N1 | Tự tìm; không chặn | Mốc giờ 22:27Z, 22:30Z, 22:35Z trong LOG phiên 3 và 22:40Z ở đầu hồ sơ là ước lượng sai; đã ghi dòng đính chính trong LOG theo giờ file thật | |
| N2 | Tự tìm; không chặn, ảnh hưởng độ chắc của K | Độ vượt lớn nhất bị sàn 1 ms bỏ ở ba ca không lỗi là 762–985 µs, sát sàn; K nhạy với δ, chưa quét δ khác (`results/T-064/chu-thich-thao-tac-nen.md` mục 3) | |
| Pin bộ chấm `t062-p7.json` lệch `cham.py` hiện tại | Đúng; không chặn | `cham.py` được bổ sung (chiếu cạnh, chấm cạnh) sau bước chấm P7 đầu, như LOG phiên 1 ghi. Người phản biện đã tính lại độc lập từ đầu ra gốc và khớp. Người làm chưa chấm lại file này bằng `cham.py` hiện tại | |
