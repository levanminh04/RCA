# Gói sửa SMTP chung — đề xuất cụ thể, chưa áp dụng

Ngày 16/10/2026. Người làm T-038: Codex; trợ lý này không là phản biện chính thức. Minh đã cho làm phần T-038 trong quyền và trình gói SMTP. Chưa có quyền sửa shared, chuyển pin, mở lại T-036 hoặc ghi WHY/DECISIONS. Toàn bộ file trong thư mục này là vật liệu xét duyệt; `experimental_copy/` không được ba nhánh dùng thay pin.

## Vấn đề đã xác nhận và phạm vi nguồn

T-036 từ chối `channel=smtp` với cả `gọi-đồng-bộ` lẫn `gọi-chưa-phân-kiểu`. Phản ví dụ T-038 tại `fixtures/smtp-counterexample.json`, `runs/kiem-smtp-001/result.json`; T-037 tại `counterexample-smtp.json`, `runs/smtp-002/result.json`. Hash kiểm trước dùng nằm trong `input-verification.json`; không đọc kết luận REVIEW. Đã ghi tự soát độc lập trong `tu-soat-truoc-T037.md` trước đọc đề xuất T-037.

Train Ticket v1.0.0: `ts-notification-service/src/main/java/notification/service/MailService.java:L22-L23,L30-L46` khai JavaMailSender và gọi `send(message)`. `application.yml:L12-L14,L19-L25` khai host/port và cờ SSL/STARTTLS; không cần chép credential. `RabbitReceive.java:L78-L90` gọi MailService rồi ghi kết quả, không chứng minh thư đến hộp người nhận. Source registry và revision nằm tại `results/T-038/nguon.json`. Nguồn là tham khảo có điều kiện vì chưa nối được build/instrumentation sinh RE2-TT.

FlashTicket: T-037 đã ghim B13/B14, yêu cầu Ticket→SMTP và outcome có thể chưa rõ khi timeout. T-037 đề xuất channel SMTP nhưng chưa chọn loại gọi hay quy tắc comparator. Gói này thống nhất nhu cầu đó; không đổi SMTP thành HTTP/RPC/internal, không tạo broker hoặc email queue giả.

SMTP có phiên trao đổi command/reply; mail server chấp nhận mail có thể giao hoặc chuyển tiếp về sau. Vì vậy thời gian một lời gọi gửi tới mail server khác thời gian tới hộp người nhận. Xem [RFC 5321 §4.3 và §6.1](https://www.rfc-editor.org/rfc/rfc5321.html#section-6.1). Port 465 được dùng cho submission qua TLS, nhưng số port/cấu hình không chứng minh phiên ứng dụng đã thương lượng TLS thành công. Xem [RFC 8314 §3.3 và §7.3](https://www.rfc-editor.org/rfc/rfc8314.html#section-3.3). Đọc tài liệu chuẩn qua web, không tải source/dependency mới, không chạy SMTP/network client.

## Thiết kế xin duyệt

1. Giữ sáu relation type hiện hành. Thêm `smtp` vào channel dành cho hai loại gọi; `messaging` bắt buộc null. Cạnh hướng **service/operation gửi → mail-server external**, đại diện một chặng SMTP cấu hình/thiết kế có nguồn. Không là cạnh tới người nhận, thành công delivery hoặc trao đổi broker.
2. Type giữ riêng với protocol. Chỉ chọn `gọi-đồng-bộ` khi có bằng chứng cho chặng client→mail-server và nghĩa chờ của chặng ấy. Nếu mới có interface/config/ý định gửi thì dùng `gọi-chưa-phân-kiểu`. Delta TT đề xuất dùng **chưa phân kiểu**. Synthetic kiểm cả hai loại không là bằng chứng TT chạy đồng bộ. Async job gọi SMTP không biến mọi chặng bên trong thành async; dialogue SMTP không tự chứng minh implementation Java chặn thread.
3. `runtime_name=null` cho tên thiết kế chưa nối instrumentation. Operation TT đã có khai báo `java:notification.service.MailService#sendEmail(Mail mail,String template)`; không tạo một operation trên mail server. T-037 giữ tên thiết kế theo nguồn, không lấy tên TT làm quy ước FT. Nếu không có operation nguồn thì entity-only vẫn hợp lệ và được báo loại trừ ở mức operation.
4. Giữ host/port/cờ TLS/điều kiện branch/retry/outcome trong `context` và locator nguồn. Không thêm trường địa chỉ mới vào schema tối thiểu. Logical external entity và identity mapping chỉ khi có nguồn; không alias theo suffix/port, không gộp provider thiếu scope. Khóa gộp vẫn hai đầu + type + channel + messaging null, giữ mọi context/provenance/record ID. Hai port cùng logical mail-server có thể gộp cấu trúc nhưng cả hai literal vẫn truy được. **Match này không xác nhận authority, port, TLS hay recipient delivery.** Nếu P9 cần so riêng authority/port/TLS, phải trình schema/telemetry thực tế trước khi dùng ở mức đó.
5. Thêm call `channel` tùy chọn vào **consumer comparator**, chỉ chấp nhận http/rpc/internal/smtp với hai call type. Graph T-035 nguyên bản không đổi và chưa có trường này; comparator đọc nguyên bản hoặc phần mở rộng tường minh. Không điền channel vào graph legacy hoặc suy từ static. P9 adapter muốn phát trường mới cần SPEC/nguồn riêng, không nằm trong gói sửa này.
6. Với SMTP đã biết, khóa cả `endpoints` lẫn `typed` giữ marker `['smtp', null]` trong vị trí address. Null là không có địa chỉ structured ở chiều này, **không phải** địa chỉ SMTP đã được xác minh. Hai phía có SMTP tường minh mới cùng marker. HTTP/RPC hoặc trace thiếu transport có marker null, không khớp SMTP. Typed vẫn loại `gọi-chưa-phân-kiểu` với `unknown_type`; không nâng type từ nguồn tĩnh. Các members giữ nguyên edge gốc/channel/context. Các HTTP/RPC legacy vẫn gộp theo contract v1; gói này không tuyên bố toàn bộ typed key xác minh transport.
7. Cách tách miền SMTP ở endpoints phải ghi rõ trong hợp đồng; tên endpoints vì thế nghĩa đầu mút kèm các miền protocol/role cần bảo toàn (messaging đã có ngoại lệ tương ứng). Đây là lựa chọn kỹ thuật ứng viên để tránh coi cùng owner là bằng chứng cùng chặng SMTP; không phải DT18 bắt buộc cách đặt khóa này. Mẫu số SMTP gồm đúng các khóa đủ điều kiện; không xóa cạnh chỉ vì trace không có SMTP.
8. Projection, mapping ownership, entity-only exclusions, bindings, signals và queue metric giữ nghĩa hiện hành. Không nhân shared metric theo mỗi operation/SMTP edge; không thêm số sự kiện nguồn tĩnh. Graph chỉ cung cấp quan hệ và phép tính tập, chưa chấm bất thường/xếp hạng RCA.

## Cũ → mới ở code và tài liệu

Patch code chính xác: `proposed-shared-code.patch`. Các copy byte đã sửa ở `experimental_copy/{build.py,compare.py}`; hash base/candidate ở `candidate-code-hashes.json`. `__init__.py` copy chỉ phục vụ import thử, không cần sửa shared.

- `build.py` CHANNELS và guard call: http/rpc/internal → thêm smtp. Không sửa relation type hoặc messaging rules.
- `compare.py` danh sách field trace được nhận → thêm channel tùy chọn; nếu có thì kiểm call protocol/type. Khóa address non-messaging luôn null → chỉ SMTP dùng marker riêng. Không thay graph đầu vào hoặc tự đoán protocol.
- README shared: liên kết tài liệu hợp đồng v1 ở root → mô tả pin v1 lịch sử cùng bản bổ sung SMTP mới, giới hạn transport và lệnh kiểm mới. Không đổi API exports.
- Hợp đồng mới trong run T-036: §2 thêm channel SMTP và nghĩa chặng; §4 mô tả key marker, unknown, protocol optional và mẫu số; §5 ghi consumer extension khác original T-035 và không so authority/TLS/delivery. Bản `results/T-036/hop-dong.md` nghiệm thu cũ giữ nguyên.

## File xin quyền sửa, thêm và tác động

Danh sách máy đọc ở `plan.json#/proposed_writes`. Đây là **gói xin duyệt**, chưa phải quyền đã có.

| File/phạm vi | Thay đổi và vì sao |
|---|---|
| `src/do_thi_tinh/build.py`, `compare.py` | Áp đúng patch sau tự soát/duyệt, nhận và so SMTP có nghĩa rõ. Không fork riêng cho TT/FT. |
| `src/do_thi_tinh/README.md` | Dẫn bản sửa, mô tả consumer trace extension và giới hạn. |
| `results/T-036/runs/sua-smtp-001/` | Thêm hồ sơ sửa kỹ thuật mới: before/code + source hash; oracle/input/expected trước code; patch/code snapshot; hợp đồng/registry/check runner; mọi pilot/lỗi/lặp/kết quả/tài nguyên; manifest và bàn giao/prompt. Không ghi đè run cũ. Tên này phải kiểm chưa tồn tại; nếu đã tồn tại, không ghi đè và trình đúng tên thay trước mutation. |
| `tasks/T-036-p5b-hop-dong-chung/SPEC.md` | **Nối phụ lục sửa kỹ thuật SMTP**, ghi quyền cụ thể ở bảng này và tiêu chí hồi quy; không sửa lịch sử duyệt gốc. T-036 đã đóng nên phải được Minh cho mở phần sửa rõ ràng. |
| `tasks/T-036-p5b-hop-dong-chung/LOG.md` | Chỉ nối: lời duyệt, vai trò, oracle→patch→kiểm, pin mới, chi phí/lượt lỗi/điểm thiếu/bàn giao. |
| `docs/WHY.md` | Nối lý do đã duyệt: chặng SMTP khác delivery; lựa chọn/alternatives/nguồn/failure/giới hạn. Dự thảo dưới đây, không tự cấp mã. |
| `docs/DECISIONS.md` | Nối nguyên quyết định của Minh về sửa shared và chuyển pin sau đủ kiểm; không ghi lời đề xuất thành quyết định đã có. Mã để Minh/nguồn sổ cấp khi duyệt. |
| `tasks/T-037-p5b-flashticket/SPEC.md`, `tasks/T-038-p5b-trainticket/SPEC.md`, `tasks/T-039-p5b-online-boutique/SPEC.md` | Chỉ thay đoạn ghim chung: v1 R1 → pin SMTP chung sau khi run mới PASS; giữ tham chiếu pin cũ cho đầu ra lịch sử. Giá trị hash/created_utc phải lấy manifest mới đã tạo, chưa biết không điền giả. Không đổi mục tiêu/tiêu chí. |
| `tasks/T-037-p5b-flashticket/LOG.md`, `tasks/T-038-p5b-trainticket/LOG.md`, `tasks/T-039-p5b-online-boutique/LOG.md` | Nối thông báo chuyển pin có quyền, input snapshots, phân biệt đầu ra cũ/mới, kiểm tương thích. Không tự hoàn thành task khác. |
| `docs/STATE.md` | Chỉ bốn dòng T036–T039, cập nhật tuần tự trên bản mới nhất; ghi sửa/kiểm/pin, không đổi cổng/nghiệm thu/OPEN khoa học khác. |
| `results/T-037/runs/tiep-nhan-smtp-001/` | Snapshot phần T037 hiện có; viết oracle semantics SMTP **mới** trước converter/check mới; giữ nguyên counterexample và mọi đáp án lịch sử. Kiểm representation/projection/entity-only/shared signal theo nguồn. Đây là tiếp nhận hợp đồng, không tự nhận khảo sát/full model T037 đã hoàn tất. |
| `results/T-038/runs/tiep-nhan-smtp-001/` | Delta TT có nguồn, bản ghi/registry/graph/mapping snapshot và runner mới, so đủ1069 graph ở `doi-chieu/doi-chieu-smtp-001/` mới; kiểm tập/loại trừ/mẫu số/input/lặp/đảo, phân tích ảnh hưởng. Không ghi đè outputs lịch sử. |
| `results/T-038/doi-chieu/doi-chieu-smtp-001/` | Output JSON nén mới từng graph/cửa sổ để tái lập và kiểm ảnh hưởng khôngSMTP. |
| `results/T-038/ban-ghi.json`, `nguon.json`, `mapping.json`, `do-thi/thuc-the.json`, `do-thi/thao-tac.json`, `doi-chieu/index.json`, `phan-tich-chenh-lech.md`, `phan-tich-chenh-lech.json`, `kiem-dung-dan.md`, `kha-thi.json`, `ban-giao.md`, `prompt-claude.txt`, `manifest.json` | Sau khi kết quả mới đạt kiểm, trỏ/cập nhật bản hiện hành theo pin mới, delta và số đo thực. Giữ byte bản trước trong `runs/tiep-nhan-smtp-001/before/`; không thay kết quả cũ thành dùng pin mới. Coverage nguồn không tự thay đổi do thêm SMTP. |
| `results/T-039/runs/tiep-nhan-smtp-001/` | Kiểm pin/schema/fixture và input hiện có; nếu chưa có model thì báo đúng chưa có numerical replay. Không tạo giả số hồi quy và không làm thay toàn task T039. |

Gói không sửa root manifest/báo cáo/fixture/run lịch sử của T-036, không sửa T-035, nguồn ứng dụng hay repo platform. Manifest mới đặt trong **run mới**, là pin mới tường minh; manifest T-036 cũ ở root giữ nguyên giá trị lịch sử. Shared source live sẽ đổi hash nên không còn khớp manifest cũ ở vị trí live; replayer pin cũ phải dùng snapshot `kiem-r1-after-002/code/`. Ba nhánh không được tự chuyển từng phần hoặc dùng HEAD. Nếu giữ quyền T038 hiện tại thì chỉ có hồ sơ đề xuất, mọi kết quả chính vẫn pin v1.

**Đổi SPEC/pin chưa đủ để đổi runner.** `results/T-038/engine.py:pinned_api()` hiện hardcode snapshot R1 và kiểm live hash R1; `compare_dev.py` import hàm ấy. Gói không sửa hai script gốc. Trong `runs/tiep-nhan-smtp-001/` phải tạo `pin.json`, `pin_loader.py`, `engine_smtp.py`, `compare_dev_smtp.py`: pin.json chứa đường dẫn/SHA/created_utc manifest SMTP đã duyệt; loader kiểm manifest đúng giá trị ấy, mỗi module live và snapshot cùng SHA trong manifest rồi mới import snapshot dưới namespace mới. Engine/compare mới truyền pin tường minh, đường ROOT giải quyết theo repo thực (không giữ parents[2] sai sau khi chuyển file sâu), output/run root cấu hình tường minh, không fallback HEAD/R1. Fixture SMTP cũ vốn kiểm rejection phải giữ lịch sử và được thay bằng fixture semantics mới ở runner mới; không chạy old rejection oracle làm expected của pin mới. Mọi input/output/hash bao gồm pin.json được lưu trong manifest tiếp nhận. Hai script gốc và snapshot cũ tiếp tục mô tả lượt legacy; nếu live đã đổi thì replayer legacy phải dùng snapshot mà không tuyên bố live vẫn khớp R1.

T037 hiện có `check-counterexample.py`/snapshot checker phản ví dụ, chưa có full-model converter hoàn tất; tạo checker tiếp nhận mới cùng loader, không sửa counterexample/runner cũ. T039 hiện mới có preflight/acquisition/audit và nguồn; chưa có model/comparer để giả định đổi constant đã đủ. Tạo pin/loader fixture tiếp nhận; converter tương lai phải nhận pin mới tường minh trong quyền T039 tương ứng. Đây là dữ kiện trên artifacts đang có, không yêu cầu hoàn thành hai task ngoài lời giao T038.

Tên run T036/T037/T039 ở bảng là đề nghị cụ thể; kiểm tồn tại chỉ đọc trước khi xin duyệt. Không mở task/chat mới, không gửi agent đối phương, không commit/push. Việc soạn prompt chuẩn để Minh chuyển thuộc hồ sơ run sau sửa; không lấy đồng thuận agent thay quyết định Minh.

## Oracle, bản thử và tiêu chí nhận sửa

`oracle-before-code.json` là expected literal ghi trước copy code đề xuất. `kiem-preview-001/checks.json` có26 kiểm đạt trong bản thử:24 case từ oracle và2 rebuild legacy exact-equal. Xem môi trường/thời gian máy ở file đó, không suy runtime/delivery từ synthetic. `kiem-preview-001/proposed-T038-delta.json` và `proposed-T038-edge-preview.json` cho thấy đúng cạnh dự kiến thêm; chưa đưa vào ban-ghi/graph/so sánh hiện hành. Kiểm đó chưa thay toàn bộ hồi quy T036/R1 hay1069 phép so pin mới; hai phần này được liệt kê rõ trong quyền xin chạy sau duyệt.

Tiêu chí sau khi duyệt sửa chung:

1. Lưu oracle trước code áp dụng; tái lập phản ví dụ T037/TT dưới pin cũ (rejection) và pin mới (giữ SMTP). Không sửa input hoặc đáp án chỉ để PASS.
2. Dựng hai mức, project và entity-only đúng literal; không tạo broker/recipient/runtime-name. Type unknown vẫn bị loại typed; trace không protocol không khớp SMTP. SMTP phải không khớp HTTP/RPC ở cùng đầu mút trong cả hai view; HTTP/RPC legacy giữ kết quả cũ.
3. Khớp SMTP tường minh chỉ xác nhận owner/endpoints+SMTP, không xác nhận address/port/TLS/mail content/delivery. Context khác không mất provenance; shared metric vẫn một địa chỉ. Mapping owner/conflict/unverified và missing transport phải phân biệt được.
4. Chạy lại toàn kiểm T036 v1+R1 và oracle mới vào run mới, so tập/members/exclusions/mẫu số, không chỉ đếm PASS. Old fixture và frozen TT build phải bằng đầu ra v1 ở phần chưa thêm SMTP. T038 so đủ graph dev dưới pin mới; typed/unknown/unmapped không đổi nghĩa để tăng giao.
5. T037/T039 tiếp nhận pin đúng phạm vi đã có, giữ trạng thái thiếu scientific output. Không gọi kiểm smoke của một fixture là hoàn thành hai task. Mỗi nhánh có manifest tiếp nhận và không sử dụng pin lẫn nhau.
6. Diff đầy đủ xác nhận đúng filelist, giữ mọi lượt, old snapshots unchanged, registry đúng hash, LOG append-only/STATE đúng dòng, hợp đồng/prompt/WHY/DECISIONS/SPEC thống nhất. Minh quyết nghiệm thu sửa và ba task riêng.

## Phương án đối lập và khi đề xuất sai

- **Chỉ thêm enum SMTP, giữ comparator v1:** ít code hơn và đúng capture, nhưng SMTP/HTTP/RPC cùng type+đầu mút vẫn có thể khớp; chưa đáp ứng nhu cầu phân biệt chặng protocol. Có thể chọn nếu Minh chấp nhận phép so chỉ cấu trúc với giới hạn rõ; gói khuyến nghị marker để không nhận false protocol agreement.
- **Thêm type mail hoặc coi mail là broker messaging:** tách typed nhưng thay taxonomy, có thể đánh đồng giao mail về sau với chặng client→server, đòi broker/scope/queue mà nguồn không có. Không chọn.
- **Trường transport/authority/port/TLS tổng quát mọi protocol:** nhiều thông tin hơn và phù hợp khi P9 đã có telemetry; đổi schema/key/adapter rộng, chưa có input thật để khóa chuẩn hóa. Gói tối thiểu không tuyên bố đã làm việc này. Failure: nếu nghiên cứu cần phân biệt server port/TLS mà chỉ dùng logical endpoint key thì proposal chưa đủ, phải trình extension trước kết luận ấy.
- **Giữ unsupported:** bảo toàn pin và là trạng thái hợp lệ trước duyệt, nhưng không hoàn thành biểu diễn SMTP và không loại delivery khỏi nghĩa vụ P5b.

Điều kiện thất bại: nguồn mapping nhầm mail-server; một channel thêm bởi adapter chưa có bằng chứng; effective library không dùng SMTP; implementation async nhưng tự gán sync; merge logical endpoint bị hiểu thành cùng authority; accepted send được báo thành delivered. Khi đó giữ OPEN đúng phần phụ thuộc và chỉ bổ sung input/đổi schema sau đề xuất cụ thể. Không quy mọi mismatch cho instrumentation hoặc dataset.

## Chi phí và phần còn chưa biết

Đo preview26 kiểm: `kiem-preview-001/checks.json#/elapsed_seconds`; không đo peak riêng lượt này. Input legacy T038 rebuild chỉ là build, chưa chạy lại1069 so trong preview. Nguồn số nền: `results/T-038/kha-thi.json#/full_and_pilot_runs` có hai lượt1069 graph, khoảng4–6 phút/lượt, peak khoảng231MB, mỗi lượt JSON nén73,862,554 bytes. Đây là số đã đo của cấu hình cũ, **không phải** số cam kết pin mới.

Dự toán CANDIDATE để duyệt gói: shared checks1 phút/50MB output; T03810 phút/0.5GiB RAM/150MB output cho một lượt mới gồm graph/trung gian+so, cộng một lượt chạy lại nếu sửa lỗi thêm10 phút/150MB; T037/T039 tiếp nhận các đầu ra hiện có và fixture mỗi nhánh5 phút/100MB. Tổng phần máy dự kiến dưới31 phút, output dự trù550MB (mọi lượt theo dự toán giữ lại), chưa gồm toàn công đọc/review, shared peak chưa đo, NTFS allocation hoặc lượt lỗi ngoài dự toán. **RAM là peak toàn process của từng lượt/ước lượng maximum, không cộng các peak thành tổng RAM và không đo lượt nặng đồng thời.** Không tải byte mạng mới, không giải nén gói mới, không EC2/GPU. Không suy giờ công hoặc chi phí hoàn tất toàn T037/T039 từ smoke. Nếu cần chạy >1 giờ/lượt, nguồn ngoài hoặc phần việc chưa liệt kê thì báo và chờ theo AGENTS, không chạy bằng dự toán này.

P6 chưa chọn tín hiệu/mức/cơ chế; P9 nhận yêu cầu ghi protocol/peer/port/TLS configured và observed riêng, attempt/outcome/timeout của chặng SMTP tại sender/adapter, không giao collector phục hồi thông tin chưa ghi. Recipient delivery cần nguồn/bằng chứng riêng nếu về sau đánh giá, không đưa vào cạnh chặng này. RQ3/RQ5/G3 và quyền mở test không thay đổi.

## Dự thảo WHY/DECISIONS chờ duyệt

WHY: “Bổ sung channel SMTP cho chặng client/operation→mail-server, giữ type theo bằng chứng riêng. Tách SMTP trong khóa so để không lấy khớp đầu mút HTTP/RPC hoặc trace thiếu protocol làm khớp SMTP. Giữ context/provenance về host/port/TLS nhưng chưa so authority/TLS/delivery. Căn cứ là nguồn FT/TT và nhu cầu biểu diễn DT18/P5; không phải hạn chế hay lợi ích RCA đã chứng minh. Đã xét chỉ thêm enum, type mail/broker, transport schema tổng quát và giữ unsupported. Bản thử tổng hợp kiểm được semantics cục bộ; full hồi quy/common-pin adoption chờ duyệt. Kết luận phụ thuộc: đủ biểu diễn chặng SMTP, tổng hợp P5b và đầu vào P9, không chọn P6.”

DECISIONS chỉ ghi **sau khi Minh đồng ý** gói và từ nguyên lời đồng ý: cho sửa danh sách file ở bảng; cho nối phụ lục T036, chạy kiểm và chuyển đồng bộ ba SPEC sang manifest SMTP mới **nếu toàn tiêu chí kỹ thuật đạt**; giữ đầu ra/pin cũ lịch sử. Đây chưa phải quyết định Minh đã có trong phiên T038.
