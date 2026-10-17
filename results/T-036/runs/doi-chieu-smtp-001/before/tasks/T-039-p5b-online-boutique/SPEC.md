# T-039 — P5b: nguồn tĩnh Online Boutique và đối chiếu Nezha-OB dev

- **Trạng thái:** ĐỀ XUẤT / CHỜ PHẢN BIỆN SPEC. Minh duyệt ghi tài liệu chuẩn bị ngày 15/10/2026; chưa duyệt triển khai, tải nguồn hoặc chạy khảo sát.
- **Người làm:** Codex.
- **Người phản biện:** Claude theo phân công P5; riêng lượt soát ba SPEC T-037–039 là Codex phiên sạch độc lập theo ngoại lệ Minh chỉ định. Ngoại lệ chỉ ở công đoạn SPEC, chưa cho ghi REVIEW và không tự áp sang phản biện kết quả.
- **Thuộc gói MRP:** P5 — **Cổng:** chuẩn bị G3; chưa là quyền mở test.
- **Nguồn quyền:** Q-159–Q-163; nguyên lời Minh lưu tại LOG T-037 Phiên 1. Các bước triển khai và phạm vi kết quả dưới đây là đề xuất chờ Minh duyệt.

## Mục tiêu

Khảo sát nguồn kiến trúc, cấu hình và code Online Boutique có căn cứ liên hệ với Nezha-OB; lập inventory đầy đủ trong snapshot nguồn đã kiểm, thao tác khi có bằng chứng, quan hệ/địa chỉ tín hiệu và đối chiếu hai chiều với graph Nezha-OB dev T-035. Phục vụ DT18-NV2/NV3, bước 1 và chuỗi nghiên cứu của cô, MRP P5, đầu vào RQ3/RQ5/P6/P9.

Đây là khảo sát nguồn, biểu diễn và phân xử chênh lệch, chưa chọn P6 hoặc đánh giá lợi ích RCA. Phân biệt revision code Nezha, tree object, ứng dụng, dataset, image và deployment; một nguồn phụ của dataset chưa tự là nguồn tĩnh độc lập. Miền Nezha toàn tập trong task là miền dev-adapter đã lưu, không cả ngày hoặc toàn file nguồn. Node chưa được chứng minh là host không được gắn metric host.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Lựa chọn/giải thích khác | Phép phân xử và bằng chứng | Hỗ trợ, bác bỏ hoặc chưa phân xử | Phần thiếu và quyết định phụ thuộc |
|---|---|---|---|---|
| Snapshot ứng dụng nào liên hệ Nezha-OB? DT18-NV3/P5 | Code Nezha/tree/ứng dụng/image/deployment có thể khác | Nguồn đã lưu → tài liệu/mã thu/build/deploy → snapshot | Chuỗi xác minh mới verified; tên repo/graph giống chưa đủ | Nguồn ứng dụng/deployment thiếu giữ OPEN, đối chiếu có điều kiện |
| Nguồn chọn lọc có đủ inventory? DT18-NV2/P5 | Chỉ loại file hoặc service có trace có thể bỏ config/template/mã sinh | Toàn cây snapshot → nhóm nguồn/loại trừ → định danh/quan hệ → bản ghi | Có coverage mới nhận đầy đủ; chưa đọc phần có thể liên quan không tự là không liên quan | Trình bổ sung; ảnh hưởng inventory và giải thích cạnh riêng |
| Tĩnh và trace khớp ở đâu và vì sao khác? hợp đồng T-036 | Revision/alias/miền/nhánh/nguồn/telemetry/chuyển đổi | Từng graph/interval dev → mapping → khóa → tập/members; đọc match và mismatch tương ứng | Tách quan sát, suy luận, ứng viên, quyết định và OPEN; không quy mọi thiếu cạnh cho telemetry | Bằng chứng cần đọc/thu/chạy và chi phí phải trình, ảnh hưởng T-040/P6/P9 |
| Nguồn phụ có độc lập không? MRP P5/P7 | Metadata có thể suy từ cùng trace hoặc pipeline | Truy tài liệu/code tạo nguồn, đầu vào, revision, miền thời gian | Có lineage mới xác định mức độc lập; hai file khác nhau chưa đủ | Metadata ngày chỉ mô tả theo quyền hiện hành; không dùng chọn P6 |
| Node/địa chỉ tín hiệu có nghĩa gì? DT18-NV2/P9 | Node có thể chưa là host; tên ổn định chưa đủ | Schema/mã/tài liệu thu và output dev đã được phép → entity/instance/host/scope | Chỉ xác nhận host khi có nguồn nghĩa định danh; thiếu giữ OPEN | P9 cần trường/khóa/owner/thời gian áp dụng; không suy từ tên |

## Đầu vào

- AGENTS.md, docs/STATE.md; docs/MRP.md §3 (RQ3/RQ5), P5/P6/P9 và G3; docs/LESSONS.md; WHY-52/53 và các quyết định trực tiếp liên quan trong docs/DECISIONS.md.
- docs/reference/sources/DT18-de-tai-va-nhiem-vu.md §2–3 và docs/reference/sources/advisor-2026-09-23.md §1; phương án P5b gốc tại LOG T-036 Phiên 1; tasks/_MAU/SPEC.md và docs/review-prompt.md.
- T-036 đã nghiệm thu theo Q-158: results/T-036/{manifest.json,hop-dong.md,nguon.json,ban-giao.md}, REVIEW và mốc đóng trong LOG T-036; src/do_thi_tinh/README.md và code. Kiểm hash trước dùng; lệch thì dừng phần phụ thuộc, không tự cập nhật hash để hợp thức hóa nguồn.
- Nguồn Nezha đã lưu mà results/T-003/runs/final-review-003/artifact-manifest.json và registry T-036 liệt kê; nguồn ở results/T-008/sources/ theo manifest. Chỉ dùng đúng artifact đã xác minh, không dùng thẻ cũ lệch hash.
- IntelligentDDS/Augmented-OnlineBoutique là repository ứng viên từ registry T-036, chưa chứng minh revision ứng dụng sinh dataset. Không tự thay bằng upstream hoặc bản mới nhất; revision/danh sách nguồn/byte/vị trí tải còn OPEN và phải trình trước lấy mới.
- results/T-035/{manifest.json,dac-ta-do-thi.md,thong-tin-theo-quan-he.md,cot-node-nezha.json,cot-node-nezha.md} khi manifest phủ, cùng graph dưới results/T-035/do-thi/Nezha-OB/ thuộc allowlist dev hiện hành. Không gom graph lịch sử. Việc dùng không tự nghiệm thu T-035.
- Nguồn phụ mức ngày chỉ dùng nội dung metadata/Source–Target đã được cho phép và lưu; không mở Weight hoặc chuỗi số, Node/log/metric/trace thô để khảo sát thêm bằng quyền task này. Muốn thu thêm phải trình phạm vi riêng. Không đọc test/heldout/data khóa/archive.
- Môi trường Python theo README T-036/T-035; -X utf8 -B, không sinh bytecode ngoài phạm vi hoặc cài gói mới từ quyền này.

### Ghim chung và song song

Cả T-037/T-038/T-039 dùng cùng snapshot hợp đồng nguồn tĩnh v1 sau sửa R1: results/T-036/manifest.json, created_utc 2026-10-15T13:45:08.305188+00:00, current_run runs/kiem-r1-after-002. Code tham chiếu là snapshot ở results/T-036/runs/kiem-r1-after-002/code/ và code-hashes.json; hợp đồng/registry được manifest T-036 phủ. Hash nằm trong manifest, không dùng HEAD thay nội dung file. Khi triển khai, lưu pin đầu vào của task vào manifest riêng và kiểm code hiện hành so với snapshot này. Không tự chuyển sang phiên bản khác nếu nguồn thay đổi.

Ba task chỉ được triển khai song song sau khi **từng SPEC được Minh duyệt triển khai**. Mỗi nhánh chỉ ghi phạm vi riêng. Nếu cần đổi hợp đồng/code chung, dừng phần phụ thuộc và trình Minh về phản ví dụ, phạm vi sửa và ảnh hưởng ba nhánh; không tự fork một nghĩa cạnh hoặc alias chung để chạy tiếp.

Cập nhật STATE thực hiện tuần tự: đọc lại bản mới nhất ngay trước ghi, chỉ thay đúng dòng task; nếu file đổi trong lúc chuẩn bị thì đọc lại và áp vào bản mới, không ghi đè nhánh khác. Quyền chuẩn bị không là quyền tự mở/gửi chat.

### Độ đủ nguồn tải chọn lọc

Chưa chốt revision, whitelist đuôi file, danh sách tải, vị trí lưu hoặc số byte. Trước tải phải trình Minh nguồn/revision/từng nhóm tệp/đối tượng/dung lượng; quyền ghi tài liệu hay duyệt triển khai không tự thay quyền tải nguồn cụ thể.

Phạm vi “inventory toàn snapshot” phải được kiểm từ **toàn cây của snapshot đã định danh**, không chỉ cây tệp đã tải. Bảng nguồn phải phân hoạch phần đã đọc/loại trừ/chưa lấy/chưa rõ; mỗi phần bị loại có lý do, bằng chứng và ảnh hưởng đến inventory/quan hệ. Tên/đuôi file tự nó không chứng minh không liên quan.

Rà cấu hình runtime/deployment, build/template, schema/interface, mã sinh và đầu vào sinh mã, client/handler/binding, wrapper, submodule/LFS hoặc nguồn ngoài repo khi chúng có thể tạo định danh/quan hệ. Không mặc định tải/generated đầy đủ hoặc bỏ mọi generated; phải xác định quan hệ nằm ở đâu và đầu vào nào cần đọc. Nếu phần bị loại có thể ảnh hưởng nhưng chưa đủ quyền/nguồn để xét, trình bổ sung đúng phần đó và giữ kết luận đầy đủ OPEN. Không gọi “toàn phần đã tải” là “toàn snapshot”; không dùng thiếu nguồn để tự thu hẹp nghĩa vụ khảo sát.

## Đầu ra

Sau duyệt triển khai, trong results/T-039/:
- nguon.json và bao-phu-nguon.md/json: revision/hash/locator/điều kiện, chuỗi Nezha–ứng dụng–deployment, tree toàn snapshot, nhóm nguồn đọc/loại trừ/chưa lấy cùng ảnh hưởng, nguồn cần bổ sung.
- ban-ghi.json, mapping.json và do-thi/: inventory/operations/relations/bindings/signals có provenance, alias có scope/owner, graph hai mức và phép chiếu/phần entity-only.
- doi-chieu/: JSON từng graph/cửa sổ dev hiện hành, hai mức và views endpoints/typed, interval/miền, tập/members/exclusions/mẫu số, trạng thái revision có điều kiện.
- phan-tich-chenh-lech.md cùng bảng bằng chứng: nhóm quan trọng, chuỗi nguồn → xử lý → trung gian → đầu ra và trường hợp khớp tương ứng; giải thích hỗ trợ/bác bỏ/chưa phân xử, lineage nguồn phụ và Node/host OPEN.
- kiem-dung-dan.md, manifest.json, fixtures/ và runs/: oracle riêng độc lập, code/lệnh/môi trường, input/trung gian/output, tiến độ/giờ/RAM/đĩa và mọi lượt kể cả lỗi/lặp.
- ban-giao.md: phần đã bao phủ, thông tin mất/chưa có, owner/đầu vào/phép kiểm bổ sung, chi phí và quyết định T-040/P6/P9 phụ thuộc.

Số liệu phải dẫn file/con trỏ JSON hoặc lệnh/kết quả đã lưu. Không nhận metadata cả ngày hoặc một nguồn cùng pipeline là xác nhận độc lập độ phủ trace.

## Phạm vi ghi

**Hiện tại chỉ chuẩn bị tài liệu trong chín file Minh duyệt.** Sau khi Minh duyệt triển khai: results/T-039/, nối LOG T-039 và đúng dòng T-039 trong STATE. Nguồn tải/vị trí lưu cần đề xuất riêng; nếu ngoài phạm vi hoặc cần data/README.md thì trình trước ghi. Không sửa src/, T-035/T-036, WHY/DECISIONS, nền tảng FT hoặc task khác bằng quyền này.

## Các bước

1. Đọc nguồn/quyền/trạng thái và kiểm pin/manifest. Chưa duyệt triển khai thì chỉ soát tài liệu. Trước triển khai phân xử khả năng một phiên, trình tách nếu quá rộng.
2. Lần lineage từ nguồn Nezha đã lưu tới ứng dụng, instrumentation/image/deployment. Phân biệt tree object và commit/build thật; thiếu nguồn mới thì trình đề xuất revision/tệp/byte trước tải.
3. Kiểm tree toàn snapshot, phần loại trừ và nguồn gián tiếp theo mục Độ đủ nguồn; thiếu phần có thể chứa định danh/quan hệ thì trình bổ sung. Không để tập file đã tải tự quyết định nghĩa inventory toàn snapshot.
4. Lập bản ghi bằng nguồn, chủ động khảo sát thao tác/quan hệ ở mọi phần liên quan thay vì chỉ service có trace. Giữ owner/tên gốc/điều kiện; không gán kiến trúc/messaging/DB của FT hoặc TT vào OB.
5. Viết oracle cho mapping/chuyển đổi riêng trước code, dựng bằng T-036. Kiểm ID/type/address/owner/chiếu/provenance; cần đổi hợp đồng chung thì lưu phản ví dụ và dừng phần phụ thuộc để trình.
6. Mapping bằng bằng chứng, không tối ưu tỷ lệ khớp; so toàn graph/cửa sổ dev hiện hành ở hai mức. Giữ interval/miền dev-adapter, báo các phần chưa đủ điều kiện so.
7. Truy code/tài liệu tạo metadata phụ theo quyền, xác định lineage và phạm vi thời gian. Nếu từ cùng telemetry thì khai phụ thuộc, không dùng như đối chứng độc lập; metadata ngày không dùng chọn P6.
8. Phân tích nhóm chênh lệch quan trọng và match tương ứng; xét revision/alias/miền/nhánh/nguồn/telemetry/chuyển đổi trước quy nguyên nhân. Node/host chỉ xác nhận từ nghĩa thu được dẫn nguồn; thiếu thì OPEN.
9. Đo pilot sau có quyền, tính tổng chi phí; kiểm nguồn/coverage/diff/phạm vi/manifest/kết luận, bàn giao và ghi LOG/dòng STATE/prompt. Minh quyết nghiệm thu.

## Kiểm đúng đắn

Mỗi entity/operation/relation/binding/signal phải truy về revision/locator/điều kiện; inventory khác observed nodes và tập ứng viên RCA. Bản ghi nguồn được lập từ yêu cầu/kiến trúc/cấu hình/code, không giới hạn theo những tên đã thấy trong trace. Không dùng root, loại lỗi, tên/đường dẫn ca hoặc mốc tiêm để chọn quan hệ; điều phối báo cáo tách khỏi API.

Dùng build/compare/project T-036; không sửa graph trace hoặc lấy kiến trúc lấp kiểu unknown. Mapping tường minh có nguồn kể cả identity, giữ scope/tên gốc và owner operation, ambiguity/unverified/unmapped có lý do. So endpoints khác so typed; HTTP/RPC gộp theo kiểu mà T-035 giữ chưa xác nhận transport. Messaging dùng khóa vai trò; nhiều queue cùng consumer giữ riêng, consume match chưa xác nhận exchange/routing/binding/bản tin. DB logic/instance và shared metric không được gộp/nhân sai.

So cả mức entity/operation trên toàn graph hiện hành được manifest/allowlist giao: full/N/A và ảnh chụp 60/300 giây có sẵn. Không gom graph lịch sử hoặc mở trace thô để dựng lại. Giữ interval/miền nguyên bản, tập S/T/giao/phần riêng hai phía, members, exclusions và mẫu số rỗng N/A. Mức thao tác thiếu mapping vẫn báo phần chưa so được, không tạo operation giả để đủ kết quả.

Chênh lệch cần xét revision, alias, miền/cửa sổ, nhánh chưa chạy, nguồn tĩnh thiếu, telemetry thiếu và lỗi chuyển đổi. Lần theo nguồn → bản ghi → chuẩn hóa → mapping → cạnh → tập; xem cả mismatch và match có điều kiện tương ứng. Chỉ quy giải thích khi chuỗi bằng chứng phân biệt được phương án khác; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân. Đồ thị tham gia phép tính khóa/giao/phần riêng, chưa tạo điểm bất thường hoặc thứ hạng.

Đối chiếu nguồn phụ với code sinh và quyền dùng metadata, không dùng sự khác nhau của hai file làm bằng chứng độc lập. “Toàn miền” Nezha là tập span adapter trả trong cửa sổ dev theo giao thức, không cả ngày; N/A không tự là nhãn nền khỏe hoặc lỗi. Không suy host từ Node* hoặc đo thêm giá trị Node bằng quyền này.

Kiểm độc lập các tập/thành viên/mẫu số, bảo toàn nguồn, tính xác định khi đảo thứ tự hợp lệ và input không đổi. Coverage nguồn phải xét phần bị loại có thể ảnh hưởng. Không có số công bố tương ứng cho công cụ chuyển bản ghi; dùng nguồn/oracle/trung gian, không tạo baseline giả hoặc thực nghiệm RCA.

## Tiêu chí xong

1. Registry, snapshot và chuỗi ứng dụng/dataset/deployment được ghi đúng mức xác minh; revision còn OPEN thể hiện ngay trong kết quả.
2. Inventory/quan hệ truy về nguồn, coverage toàn snapshot và loại trừ được kiểm. Thiếu nguồn cần thiết phải báo đạt một phần/trình bổ sung, không tự nhận đầy đủ.
3. Graph/mapping/đối chiếu hai chiều trên toàn graph/cửa sổ dev được giao có trung gian, tập/members/mẫu số/ngoài miền đúng; lỗi chặn chưa xử lý không được gọi đạt.
4. Nhóm chênh lệch quan trọng đã được lần theo, có giải thích cạnh tranh và match tương ứng; OPEN nêu đúng chứng cứ/owner/phép bổ sung và quyết định phụ thuộc.
5. Miền dev-adapter, lineage/độc lập nguồn phụ và Node/host được diễn giải đúng. Không dùng metadata ngày hoặc nghĩa host chưa xác minh chọn P6.
6. Bàn giao cụ thể cho T-040/P6/P9; kiểm/manifest/LOG/prompt đủ. Chưa xác nhận telemetry đầy đủ, lợi ích RCA, chọn P6, đóng P5b/RQ3/RQ5/G3 hoặc mở test.

## Không làm

Không triển khai/tải từ quyền tạo tài liệu, không mở telemetry thô/test/heldout/archive, dựng cửa sổ Nezha mới hoặc coi adapter là cả ngày. Không tự tải repo/upstream mới, đọc Weight/Node values, sửa shared code/trace/kiến trúc FT, chạy baseline/RCA, bật EC2, commit/push hoặc mở/gửi chat. Không làm thay T-040 hoặc kiểm runtime FT; các nghĩa vụ đó giữ rõ để task sau nhận.

## Chi phí ước lượng

Dự toán lịch sử OB/Nezha **3–5 giờ công** là CANDIDATE chưa đo, chưa gồm phản biện/chờ nguồn; không là trần giảm kiểm hoặc cam kết một phiên. Truy lineage và phân xử nhóm có thể lâu hơn phần tính.

Giờ máy, peak RAM, byte tải và tổng đĩa còn OPEN; **chưa có dự toán bao phủ mọi lượt chạy**. Khi trình tải phải nêu byte mạng/giải nén/cây nguồn; tổng đĩa và máy cần tính mọi graph/cửa sổ, pilot/tự kiểm/lượt lỗi/lặp/snapshot/trung gian cần giữ, tách khoản đã tính/chưa tính. RAM chưa đo, phải đo lượt thử sau có quyền cùng kích thước input và cách ngoại suy; không đo cùng việc nặng khác. Dùng laptop theo phương án gốc, chưa có căn cứ EC2/GPU.

So tổng máy với ngân sách Q-40 ở phần liên quan; thao tác thuộc luật cứng 8 phải báo trước. **Đề xuất trước duyệt triển khai:** nếu phạm vi triệt để vượt một phiên, Minh quyết tách truy nguồn/coverage/lineage và dựng/đối chiếu/phân tích, không tự chia mã task hoặc giảm tiêu chí để vừa dự toán.

## Rủi ro và điều chưa chắc

Chưa kiểm Augmented-OB đúng ứng dụng/deployment sinh Nezha-OB, độ đủ nguồn tải chọn lọc, nguồn phụ độc lập, tên/owner operation ổn định, Node có nghĩa host và hợp đồng T-036 giữ hết nhu cầu OB. Các giả định có thể sai khi config/mã sinh/nguồn ngoài bị bỏ, metadata suy từ cùng trace, tên đồng dạng sai scope hoặc snapshot không khớp. Chưa đo chi phí một phiên/RAM/tổng lượt/đĩa. Các phần này chưa được khảo sát trong lượt chuẩn bị vì chưa có quyền đọc/tải/chạy mở rộng; ảnh hưởng nhận định đầy đủ, giải thích chênh lệch, chọn thiết kế và yêu cầu P9. T-036 được nghiệm thu chưa xác nhận các giả định này.

## Prompt bàn giao

Prompt soát **cả ba SPEC** được chép nguyên văn từ Prompt chung + khối Soát SPEC + khối G3 của docs/review-prompt.md tại LOG.md Phiên 1 của từng task. Chỉ điền thông tin trung tính. Minh chuyển thủ công cho Codex phiên sạch theo ngoại lệ đã chỉ định; phiên đó chỉ đọc/trả lời chat, chưa được ghi REVIEW, sửa tài liệu, triển khai hoặc tải nguồn. Không tự mở/gửi phiên.
