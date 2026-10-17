# T-038 — P5b: nguồn tĩnh Train Ticket và đối chiếu RE2-TT dev

- **Trạng thái:** ĐỀ XUẤT / CHỜ PHẢN BIỆN SPEC. Minh duyệt ghi tài liệu chuẩn bị ngày 15/10/2026; chưa duyệt triển khai, tải nguồn hoặc chạy khảo sát.
- **Người làm:** Codex.
- **Người phản biện:** Claude theo phân công P5; riêng lượt soát ba SPEC T-037–039 là Codex phiên sạch độc lập theo ngoại lệ Minh chỉ định. Ngoại lệ chỉ ở công đoạn SPEC, chưa cho ghi REVIEW và không tự áp sang phản biện kết quả.
- **Thuộc gói MRP:** P5 — **Cổng:** chuẩn bị G3; chưa là quyền mở test.
- **Nguồn quyền:** Q-159–Q-163; nguyên lời Minh lưu tại LOG T-037 Phiên 1. Các bước triển khai và phạm vi kết quả dưới đây là đề xuất chờ Minh duyệt.

## Mục tiêu

Khảo sát kiến trúc, cấu hình và code Train Ticket trong snapshot được xác định; lập inventory thực thể đầy đủ trong snapshot đã kiểm, chủ động khảo sát thao tác có bằng chứng và đối chiếu hai chiều với graph RE2-TT dev T-035. Phục vụ DT18-NV2/NV3, bước 1 và chuỗi nghiên cứu của cô, MRP P5 và đầu vào RQ3/RQ5/P6/P9.

Đây là khảo sát nguồn và phân xử chênh lệch có điều kiện. Phân biệt code RCAEval, revision dataset, ứng dụng, instrumentation và deployment; repo chính thức, HEAD mới hoặc image tag không tự chứng minh nguồn sinh dataset. Kết quả nguồn khác revision chỉ được nhận làm tham khảo có điều kiện ngay trong JSON/báo cáo, chưa là độ phủ instrumentation hay lợi ích RCA.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Lựa chọn/giải thích khác | Phép phân xử và bằng chứng | Hỗ trợ, bác bỏ hoặc chưa phân xử | Phần thiếu và quyết định phụ thuộc |
|---|---|---|---|---|
| Inventory/quan hệ có đủ snapshot? DT18-NV2/P5 | Chỉ service có trace hoặc vài loại file có thể bỏ module/config/mã sinh/quan hệ | Toàn cây snapshot → bảng đọc/loại trừ → nguồn → bản ghi/graph | Chỉ nhận đầy đủ khi coverage nguồn bảo vệ được; thiếu phần có thể chứa quan hệ bác bỏ tuyên bố đầy đủ | Trình nguồn bổ sung; ảnh hưởng inventory và giải thích thiếu cạnh |
| Snapshot nào liên hệ RE2-TT? DT18-NV3/P5 | Code RCA, dataset, ứng dụng và deployment có thể khác | Nguồn RCAEval → tài liệu thu/build/image/instrumentation/deployment → snapshot | Có chuỗi xác minh mới verified; graph giống hoặc repo đúng tên chưa đủ | Owner cung cấp manifest/image/code thu; chưa nối được thì so tham khảo có điều kiện |
| Tĩnh và trace khớp ở đâu? hợp đồng T-036 | Đầu mút, kiểu, transport và địa chỉ là các mức xác minh khác nhau | Graph dev/miền/interval → mapping nguồn → khóa → tập/members/mẫu số | Unknown không thành sync; mơ hồ/thiếu địa chỉ không thành match | Giữ phần chưa so được theo từng mức; T-040/P6 nhận giới hạn |
| Chênh lệch do bước nào? P5/AGENTS | Revision/alias/miền/nhánh/nguồn/telemetry/chuyển đổi | Lần chuỗi đầu vào → xử lý → trung gian → đầu ra, đối chiếu mismatch và match tương ứng | Chỉ xác nhận giải thích có bằng chứng phân xử; không đủ thì OPEN | Nêu đúng phần phải đọc/thu/chạy, chi phí và quyết định phụ thuộc |
| P6/P9 nhận gì? RQ3/RQ5 | Cạnh/địa chỉ tĩnh khác quan sát thật hoặc lợi ích | Bảng thông tin có thể cung cấp, nơi ghi và trường còn thiếu | Có đầu vào cụ thể, chưa chọn thuật toán/mức/tín hiệu | T-040 tổng hợp; P9 kiểm schema/runtime, P6/P7/P10 đánh giá thiết kế |

## Đầu vào

- AGENTS.md, docs/STATE.md; docs/MRP.md §3 (RQ3/RQ5), P5/P6/P9 và G3; docs/LESSONS.md; WHY-52/53 và các quyết định trực tiếp liên quan trong docs/DECISIONS.md.
- docs/reference/sources/DT18-de-tai-va-nhiem-vu.md §2–3 và docs/reference/sources/advisor-2026-09-23.md §1; phương án P5b gốc tại LOG T-036 Phiên 1; tasks/_MAU/SPEC.md và docs/review-prompt.md.
- T-036 đã nghiệm thu theo Q-158: results/T-036/{manifest.json,hop-dong.md,nguon.json,ban-giao.md}, REVIEW và mốc đóng trong LOG T-036; src/do_thi_tinh/README.md và code. Kiểm hash trước dùng; lệch thì dừng phần phụ thuộc, không tự cập nhật hash để hợp thức hóa nguồn.
- results/T-002/handoff-manifest.json và các nguồn RCAEval được registry T-036 liệt kê, sau xác minh hash; không dùng thẻ cũ lệch manifest. Repository FudanSELab/train-ticket là điểm bắt đầu ứng viên đã ghi, chưa là revision ứng dụng sinh RE2-TT.
- results/T-035/{manifest.json,dac-ta-do-thi.md,thong-tin-theo-quan-he.md} và graph dưới results/T-035/do-thi/RE2-TT/ thuộc manifest/allowlist dev hiện hành. Kiểm selector chỉ lấy bản hiện hành được giao; không suy nghiệm thu T-035 từ việc dùng đầu vào.
- Nguồn ứng dụng/deployment/instrumentation mới còn OPEN, chỉ tải sau đề xuất cụ thể được Minh duyệt. Không đọc lại trace thô/test/heldout/data khóa hoặc archive RCA.
- Python/môi trường theo README T-036/T-035; -X utf8 -B, không cài môi trường hoặc sinh bytecode ngoài quyền.

### Ghim chung và song song

Cả T-037/T-038/T-039 dùng cùng snapshot hợp đồng nguồn tĩnh v1 sau sửa R1: results/T-036/manifest.json, created_utc 2026-10-15T13:45:08.305188+00:00, current_run runs/kiem-r1-after-002. Code tham chiếu là snapshot ở results/T-036/runs/kiem-r1-after-002/code/ và code-hashes.json; hợp đồng/registry được manifest T-036 phủ. Hash nằm trong manifest, không dùng HEAD thay nội dung file. Khi triển khai, lưu pin đầu vào của task vào manifest riêng và kiểm code hiện hành so với snapshot này. Không tự chuyển sang phiên bản khác nếu nguồn thay đổi.

Ba task chỉ được triển khai song song sau khi **từng SPEC được Minh duyệt triển khai**. Mỗi nhánh chỉ ghi phạm vi riêng. Nếu cần đổi hợp đồng/code chung, dừng phần phụ thuộc và trình Minh về phản ví dụ, phạm vi sửa và ảnh hưởng ba nhánh; không tự fork một nghĩa cạnh hoặc alias chung để chạy tiếp.

Cập nhật STATE thực hiện tuần tự: đọc lại bản mới nhất ngay trước ghi, chỉ thay đúng dòng task; nếu file đổi trong lúc chuẩn bị thì đọc lại và áp vào bản mới, không ghi đè nhánh khác. Quyền chuẩn bị không là quyền tự mở/gửi chat.

### Độ đủ nguồn tải chọn lọc

Chưa chốt revision, whitelist đuôi file, danh sách tải, vị trí lưu hoặc số byte. Trước tải phải trình Minh nguồn/revision/từng nhóm tệp/đối tượng/dung lượng; quyền ghi tài liệu hay duyệt triển khai không tự thay quyền tải nguồn cụ thể.

Phạm vi “inventory toàn snapshot” phải được kiểm từ **toàn cây của snapshot đã định danh**, không chỉ cây tệp đã tải. Bảng nguồn phải phân hoạch phần đã đọc/loại trừ/chưa lấy/chưa rõ; mỗi phần bị loại có lý do, bằng chứng và ảnh hưởng đến inventory/quan hệ. Tên/đuôi file tự nó không chứng minh không liên quan.

Rà cấu hình runtime/deployment, build/template, schema/interface, mã sinh và đầu vào sinh mã, client/handler/binding, wrapper, submodule/LFS hoặc nguồn ngoài repo khi chúng có thể tạo định danh/quan hệ. Không mặc định tải/generated đầy đủ hoặc bỏ mọi generated; phải xác định quan hệ nằm ở đâu và đầu vào nào cần đọc. Nếu phần bị loại có thể ảnh hưởng nhưng chưa đủ quyền/nguồn để xét, trình bổ sung đúng phần đó và giữ kết luận đầy đủ OPEN. Không gọi “toàn phần đã tải” là “toàn snapshot”; không dùng thiếu nguồn để tự thu hẹp nghĩa vụ khảo sát.

## Đầu ra

Sau duyệt triển khai, trong results/T-038/:
- nguon.json và bao-phu-nguon.md/json: nguồn/revision/hash/điều kiện, chuỗi dataset–ứng dụng–deployment; tree toàn snapshot, nhóm tệp đã đọc/loại trừ/chưa lấy, ảnh hưởng và đề nghị bổ sung.
- ban-ghi.json: inventory/operations/relations/resource_bindings/signals theo T-036; mỗi phần có locator/owner/điều kiện. Không lấy nút trace làm inventory nguồn.
- mapping.json và do-thi/: mapping có nguồn, hai graph tĩnh, phép chiếu và phần entity-only.
- doi-chieu/: JSON từng graph/cửa sổ dev, cả hai mức đủ điều kiện, views endpoints/typed, members/exclusions/tập/mẫu số và cờ revision có điều kiện.
- phan-tich-chenh-lech.md và bảng bằng chứng: từng nhóm quan trọng, trường hợp so tương ứng, giải thích hỗ trợ/bác bỏ/OPEN; phân biệt nguồn thiếu, giao thức, adapter/cài đặt và giả định phép so.
- kiem-dung-dan.md, manifest.json, fixtures/ và runs/: oracle độc lập cho biến đổi riêng, code/lệnh/môi trường, input/trung gian/output, thời gian/RAM/đĩa và mọi lượt lỗi/lặp.
- ban-giao.md: phần đã biết, thông tin mất/chưa có, owner/đầu vào/phép kiểm bổ sung, chi phí và ảnh hưởng T-040/P6/P9.

Số liệu phải dẫn file/con trỏ JSON hoặc lệnh/kết quả đã lưu. Dự toán không được trình bày như số đã đo.

## Phạm vi ghi

**Quyền hiện tại chỉ chuẩn bị tài liệu trong chín file đã duyệt.** Sau khi Minh duyệt triển khai: results/T-038/, nối LOG T-038 và đúng dòng T-038 trong STATE. Nguồn tải/vị trí lưu cần đề xuất riêng; nếu ngoài phạm vi này hoặc cần data/README.md thì trình mở rộng trước ghi. Không sửa src/, T-035/T-036, WHY/DECISIONS hoặc task khác bằng quyền task này.

## Các bước

1. Tự soát nguồn/tiêu chí/quyền, kiểm pin/manifest; chưa duyệt triển khai thì chỉ soát tài liệu. Trước triển khai nêu khả năng hoàn thành một phiên; nếu quá rộng trình tách, không tự thu hẹp.
2. Lần provenance từ nguồn RCAEval đã lưu; lập phương án truy revision và tải phần nguồn còn thiếu có danh sách/byte. Chỉ lấy sau đúng quyền; không chọn phiên bản theo mức khớp graph.
3. Kiểm toàn cây snapshot và phần nguồn bị loại theo mục Độ đủ nguồn. Nối module/build/deployment/config/code sinh với thực thể/quan hệ; thiếu nguồn cần thiết thì trình bổ sung, không gọi inventory đầy đủ.
4. Đọc nguồn lập inventory và quan hệ, chủ động khảo sát HTTP/RPC, DB/cache, messaging, nền/callback và thành phần hỗ trợ khi nguồn có. Giữ tên/owner/điều kiện; operation runtime_name chưa xác minh giữ OPEN.
5. Viết oracle biến đổi/mapping riêng trước mã; dựng bằng T-036 đã ghim. Kiểm ID/type/address/provenance/chiếu. Hợp đồng không giữ được nghĩa thì lưu phản ví dụ và dừng phần phụ thuộc, trình sửa chung.
6. Lập mapping có nguồn và so toàn bộ graph/cửa sổ RE2-TT dev hiện hành được giao; so hai chiều, hai view, báo cả phần không so được. Điều phối ca ngoài API, không chọn cạnh theo nhãn.
7. Lần theo nhóm chênh lệch quan trọng và match tương ứng; ưu tiên code/trung gian đã có. Thiếu chứng cứ phải trình đúng phần cần bổ sung và ảnh hưởng; không tự quy thiếu instrumentation.
8. Đo pilot/tiến độ sau có quyền; tính tổng máy/đĩa mọi bước và lượt dự kiến. Nếu thao tác tốn kém hoặc không vừa một phiên, trình cách tách/phạm vi trước khi làm phần vượt.
9. Soát nguồn/diff/manifest/mẫu số/kết luận và bàn giao. Ghi LOG/dòng STATE/prompt theo mẫu; Minh quyết nghiệm thu.

## Kiểm đúng đắn

Mỗi entity/operation/relation/binding/signal phải truy về revision/locator/điều kiện; inventory khác observed nodes và tập ứng viên RCA. Bản ghi nguồn được lập từ yêu cầu/kiến trúc/cấu hình/code, không giới hạn theo những tên đã thấy trong trace. Không dùng root, loại lỗi, tên/đường dẫn ca hoặc mốc tiêm để chọn quan hệ; điều phối báo cáo tách khỏi API.

Dùng build/compare/project T-036; không sửa graph trace hoặc lấy kiến trúc lấp kiểu unknown. Mapping tường minh có nguồn kể cả identity, giữ scope/tên gốc và owner operation, ambiguity/unverified/unmapped có lý do. So endpoints khác so typed; HTTP/RPC gộp theo kiểu mà T-035 giữ chưa xác nhận transport. Messaging dùng khóa vai trò; nhiều queue cùng consumer giữ riêng, consume match chưa xác nhận exchange/routing/binding/bản tin. DB logic/instance và shared metric không được gộp/nhân sai.

So cả mức entity/operation trên toàn graph hiện hành được manifest/allowlist giao: full/N/A và ảnh chụp 60/300 giây có sẵn. Không gom graph lịch sử hoặc mở trace thô để dựng lại. Giữ interval/miền nguyên bản, tập S/T/giao/phần riêng hai phía, members, exclusions và mẫu số rỗng N/A. Mức thao tác thiếu mapping vẫn báo phần chưa so được, không tạo operation giả để đủ kết quả.

Chênh lệch cần xét revision, alias, miền/cửa sổ, nhánh chưa chạy, nguồn tĩnh thiếu, telemetry thiếu và lỗi chuyển đổi. Lần theo nguồn → bản ghi → chuẩn hóa → mapping → cạnh → tập; xem cả mismatch và match có điều kiện tương ứng. Chỉ quy giải thích khi chuỗi bằng chứng phân biệt được phương án khác; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Đồ thị tham gia phép tính khóa/giao/phần riêng, chưa tạo điểm bất thường hoặc thứ hạng.

Kiểm độc lập danh sách tập và thành viên, tổng phân hoạch, mẫu số rỗng, tính xác định khi đảo thứ tự hợp lệ và input không đổi. Phần nguyên bản và provenance hai nguồn giữ riêng. Kiểm coverage nguồn trước dùng chữ “toàn”; chưa có số công bố cho công cụ đọc bản ghi này, kiểm bằng nguồn/oracle/trung gian thay vì tạo baseline giả. Không chạy lại baseline hoặc thí nghiệm RCA trong task.

## Tiêu chí xong

1. Snapshot/phạm vi/chuỗi revision được công bố đúng trạng thái. Inventory đầy đủ phải có coverage toàn snapshot và phần loại trừ được kiểm; nếu thiếu nguồn cần thiết thì báo đạt một phần và trình bổ sung, không tự nghiệm thu đầy đủ.
2. Quan hệ/thao tác/địa chỉ có provenance, dựng/chiếu đúng hoặc có phản ví dụ và quyết định cần Minh xử lý; lỗi chặn chưa xử lý không được gọi đạt.
3. Toàn graph/cửa sổ RE2-TT dev được giao có so hai chiều, các tập/members/mẫu số/loại trừ kiểm được. Revision còn OPEN thể hiện ngay trong kết quả; không quy mismatch cho runtime nếu chưa có căn cứ.
4. Nhóm chênh lệch quan trọng đã lần theo bằng nguồn trong quyền, xét giải thích khác và match tương ứng; phần chưa phân xử chỉ rõ bằng chứng/owner/phép bổ sung và quyết định phụ thuộc.
5. Bàn giao cụ thể cho T-040/P6/P9; kiểm/manifest/LOG/prompt đủ. Kết quả cho phép nhận mô hình tĩnh và mô tả độ khớp có điều kiện; chưa trả lời lợi ích RCA, chọn P6, đóng P5b/RQ3/RQ5/G3 hoặc mở test.

## Không làm

Không triển khai hoặc tải từ việc duyệt tạo tài liệu. Không sửa shared code/graph trace/kiến trúc FT; không mở test/heldout/archive, đọc telemetry thô, bật EC2, commit/push hoặc tự mở/gửi chat. Không dựng mọi hàm, không tự áp quy ước/mapping của FT/OB sang TT và không làm thay tổng hợp T-040. Thiếu nguồn ngoài quyền phải trình, không xóa nghĩa vụ nghiên cứu.

## Chi phí ước lượng

Dự toán lịch sử **4–6 giờ công** cho TT và truy revision chỉ là CANDIDATE chưa đo, chưa gồm phản biện/chờ nguồn. Có thể lạc quan: đọc nguồn và phân xử theo nhóm thường khác thời gian máy; không cam kết xong một phiên hoặc dùng dự toán làm trần giảm kiểm.

Revision/danh sách nguồn/byte tải, thời gian toàn lượt tính, peak RAM và tổng lưu còn OPEN. **Chưa có dự toán bao phủ mọi lượt chạy**. Đề xuất tải phải tách byte mạng, giải nén/cây nguồn và tổng đĩa; tổng máy/đĩa cần cộng mọi graph/cửa sổ, pilot/tự kiểm/lượt lỗi/lặp lại/snapshot/trung gian cần giữ, ghi khoản đã tính/chưa tính. RAM chưa đo, phải đo ở lượt thử sau có quyền; khai input và cách ngoại suy, không đo cùng việc nặng khác. Dùng laptop theo kế hoạch gốc, chưa có căn cứ cần EC2/GPU.

So tổng máy với ngân sách Q-40 ở phần tính toán liên quan; hơn một giờ/lượt hoặc tải hơn 5 GB và chi phí khác theo AGENTS phải báo trước. **Đề xuất trước duyệt triển khai:** phân xử một phiên; nếu quá rộng, Minh quyết tách truy nguồn/coverage và dựng/đối chiếu/phân tích. Không tự tách mã task hoặc giảm tiêu chí để vừa dự toán.

## Rủi ro và điều chưa chắc

Chưa kiểm revision ứng dụng/deployment sinh RE2-TT; thiếu chuỗi build/instrumentation thì chỉ so tham khảo. Chưa kiểm nguồn chọn lọc đủ snapshot, độ ổn định tên/owner/mapping operation và độ đủ hợp đồng; config/mã sinh/nguồn ngoài có thể bác bỏ. Chưa kiểm chi phí một phiên/tổng run/RAM/đĩa. Phần chưa kiểm không thực hiện trong lượt chuẩn bị vì chưa có quyền khảo sát/tải/chạy; ảnh hưởng kết luận đầy đủ, quy giải thích chênh lệch và bước thiết kế P6/P9. Ghi đúng owner/nguồn cần, không lấy việc công cụ T-036 được nghiệm thu thay bằng chứng TT.

## Prompt bàn giao

Prompt soát **cả ba SPEC** được chép nguyên văn từ Prompt chung + khối Soát SPEC + khối G3 của docs/review-prompt.md tại LOG.md Phiên 1 của từng task. Chỉ điền thông tin trung tính. Minh chuyển thủ công cho Codex phiên sạch theo ngoại lệ đã chỉ định; phiên đó chỉ đọc/trả lời chat, chưa được ghi REVIEW, sửa tài liệu, triển khai hoặc tải nguồn. Không tự mở/gửi phiên.
