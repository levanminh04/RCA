# CIRCA: sửa kiểm journal DA và thứ tự chốt manifest — CHƯA DUYỆT

Codex là người làm T-032; Claude là người phản biện. Đây là đề xuất sửa bộ kiểm trong một bản mới, chưa áp dụng. Không sửa phương pháp, adapter, môi trường, SPEC, code dùng chung hoặc WHY-42. CIRCA vẫn khớp tuyệt đối; không dùng ngoại lệ MicroRank.

## Chỗ sai và bằng chứng đã kiểm

**FACT — lỗi kiểm journal.** `runs/circa-nodeview-transport-002/verified/runs/circa-nodeview-fixture-001/check.json#/error` ghi `actual DA groups not observed`; traceback trỏ `replay_circa_v3.py:444`. Bộ kiểm đang yêu cầu đúng một mục `topological_groups_after_native_cache`. Trong khi đó, `capture_circa_v2.py#CircaCapture._line` ghi mục này ở line event của dòng `for index, nodes in enumerate(sorted_nodes):`.

Nguồn `RCAEval.graph_heads.rht.DAScorer.score` đã đọc trực tiếp từ `D:/RCA-ext/src/RCAEval/RCAEval/graph_heads/rht.py`, kiểm SHA256 khớp `runs/circa-source-001/source-closure.json#/files/RCAEval.graph_heads.rht/sha256`. Hàm tạo `sorted_nodes` trước vòng lặp, không có `break` ở vòng gán index. Header được ghé lại sau mỗi nhóm và một lần khi vòng lặp kết thúc. Với G nhóm và một lần trả về hoàn chỉnh, dự đoán cần kiểm là G+1 snapshot, không phải một snapshot. Việc này phản ánh line event của vòng lặp; không phản ánh việc native tự tính topology nhiều lần.

**FACT — journal thực tế.** Trong `runs/circa-nodeview-transport-002/verified/runs/circa-nodeview-fixture-001/adapter_extension_tables/capture/calls/0029-da.json`, `/outcome` là `return`, `/exceptions` rỗng, `/journal` có hai snapshot nhóm giống hệt nhau, mỗi snapshot giữ một nhóm theo thứ tự caller_cpu, root_cpu. Xen giữa hai snapshot là hai lượt gán index 0. Sau đó có hai lượt descendant, hai child-map và hai adjustment. `/exit/sorted_nodes` giữ đúng một nhóm ấy. Bộ kiểm đã nhầm số lần ghi header với số lần tính nhóm. Chưa có bằng chứng lệch số học CIRCA.

**FACT — NodeView đã qua kiểm riêng, toàn bộ fixture chưa đạt.** File `serializer_nodeview/check.json#/passed` của cùng lượt là true, nhưng check chung vẫn FAIL trước khi hoàn tất tất cả fixture. `circa-nodeview-fixture-001-monitor/status.json#/elapsed_s` ghi 10,570103352889419 giây. Không dùng thời gian này làm dự toán đủ fixture hoặc pilot; chưa chạy pilot thật.

**FACT — lỗi thứ tự chốt manifest.** Trong `replay_circa_v3.py#main`, nhánh lỗi tạo `artifact_manifest` và ghi check trước khi nối dòng FAILED vào `progress.jsonl`. Trong `#one`, nhánh hoàn tất cũng ghi manifest trước khi nối FINISHED. Vì thế một log còn được ghi sau khi đã chốt hash; nhánh pilot PASS cũng sẽ gặp lỗi này khi kiểm lại artifact. Đây là lỗi toàn vẹn đầu ra, phải sửa trước pilot; không được chữa bằng bỏ log khỏi manifest.

Closed transport hiện có `runs/circa-nodeview-transport-002/{check.json,two-end-check.json,file-inventory.json}`: 77 tệp khớp hash hai đầu theo byte hiện tại. Receipt ghi rõ `original_full_manifest_pass=false` và `intermediates_eligible=false`. Manifest trong check cũ chỉ lệch `progress.jsonl`: hash phần tiền tố được kiểm khớp, phần nối là sự kiện FAILED đã được code ghi sau manifest. Việc xác nhận transport giúp đọc lỗi; không biến lượt hỏng thành kết quả nghiên cứu hợp lệ. Đã kiểm lại độc lập đủ 77 tệp trước viết đề xuất này.

## Hậu quả

CIRCA đang bị chặn bởi bộ kiểm trung gian và toàn vẹn artifact, chưa phải bởi tính toán native. Không bỏ phép kiểm journal, không lấy một snapshot thuận tiện để bỏ các snapshot khác, không bỏ progress khỏi hash. Sửa NodeView đã được duyệt không cấp quyền sửa hai chỗ mới này, nên dừng phần phụ thuộc và trình Minh. Các phân tích BARO/SimpleRCA độc lập vẫn tiếp tục.

Đây là hai lỗi khác nhau qua hai lượt fixture: lượt đầu serializer NodeView, lượt sau kiểm DA journal. Chưa phải ba lần thử cùng một chỗ. Không vì vậy tự chạy lượt sửa tiếp; proposal này vẫn cần Minh duyệt.

## Sửa tối thiểu được đề xuất sau duyệt

Chỉ tạo `scripts/replay_circa_v4.py` từ v3. Giữ nguyên `capture_circa_v2.py`, toàn bộ pin helper/source/package, dữ liệu, native, adapter, ngưỡng, công thức, bảng, thứ hạng và tiêu chí exact. Các thay đổi của v4 phải được full diff và so AST trước chuyển.

1. **Journal DA hoàn chỉnh:** thay yêu cầu `len(group_entries)==1` bằng phép kiểm có cấu trúc. Với call trả về hoàn chỉnh, lấy G từ các nhóm đã ghi, yêu cầu đúng G+1 header; so exact toàn bộ snapshot với nhau và với `/exit/sorted_nodes` sau giải mã kiểu set-iteration đã ghi, giữ nguyên thứ tự nhóm và node. Không sort hoặc deduplicate. Kiểm toàn bộ chronology: header nhóm i → đúng các index_visit của nhóm i, mỗi index bằng i → header kế tiếp; sau header cuối chỉ có các cặp descendant_visit/child-map theo chiều đảo nhóm của nguồn, rồi adjustment theo thứ tự `scores.items()` đã ghi tại entry. Không chấp nhận bước thừa, thiếu, lặp hoặc đảo bước. Giữ mọi phép kiểm child-map, propagation, score, index, khóa DA, bảng, mảng và native/full-return đã có.
2. **Empty và exception:** graph rỗng được score_graph trả sớm, không gọi DA, vẫn theo nhánh đã có. Native DA với G=0 và scores rỗng phải ghi đúng một header rỗng, không có visit/map/adjustment và trả dict rỗng. `sorted_nodes` có nhóm rỗng vẫn tính nhóm đó vào G. Exception trước loop không được áp công thức G+1 hay chứng nhận completed DA: giữ exception/path, từ chối dùng journal ấy như traversal hoàn chỉnh. Nhánh ERROR của score_graph đã có giữ nguyên trạng thái và giới hạn bằng chứng từng phần; không dùng exception để bỏ kiểm ở call hoàn tất.
3. **Chốt đầu ra:** mọi `source-checks.json` và sự kiện terminal FINISHED/FAILED thuộc run phải được ghi xong trước khi tính manifest cuối. Soát cả `one`, `fixtures`, xử lý lỗi của `main` và `finally`; không được có file do wrapper còn ghi sau manifest cuối. Giữ đầy đủ progress và mọi stdout/stderr/source-checks; không thêm ngoại lệ loại progress ra khỏi manifest, không sửa lịch sử. Các check phải khai chính xác file tự loại để tránh tự tham chiếu; nếu ghi failure-after-check thì giữ check cũ và khai rõ file failure hiện tại được loại, không che lỗi bằng một check PASS cũ.
4. **Posthoc audit trước fresh fixture:** thêm đường CLI chỉ đọc capture fixture cũ đã đóng băng, ràng buộc bằng manifest transport hiện tại và SHA256 được truyền từ bên gọi. Kiểm source/package/helper, mọi byte/artifact/capture table/array và join journal bằng verifier v4; không gọi native, không sửa capture/check/progress cũ. Ghi kết quả audit mới. Audit PASS chỉ chứng minh bộ kiểm hiểu đúng snapshot đã lưu; không tái tạo được native–observed comparison của lượt fixture đã dừng và không cấp eligibility nghiên cứu cho lượt cũ. Audit lỗi thì dừng toàn lượt, không tới fresh fixture.
5. **Fresh fixture đầy đủ:** giữ nguyên 18 fixture gốc và fixture NodeView, thêm ba fixture native DA nhỏ (empty G, SCC/cycle với tail, exception trước loop bằng scores=None) và một fixture toàn vẹn manifest có hai nhánh terminal PASS/FAIL. Fixture `da_order` cũ phải chứng minh đã thực sự qua ít nhất hai nhóm. Các fixture mới so original–observed exact, nonmutation/hook, cùng kiểm journal; exception fixture phải chứng minh chính exception native được giữ và không bị nhận như completed DA. Fixture manifest xác nhận terminal log/source checks nằm trong hash cuối, cùng phép phá hash trên bản sao để chứng minh không bỏ qua thay đổi sau chốt. Tổng 23 fixture gồm 19 giữ nguyên và 4 mới; mỗi fixture là kiểm bộ ghi/kiểm, không là bằng chứng cơ chế nghiên cứu.

CLI mới có thể gộp **audit → fresh fixture** trong cùng một job để giữ đúng trần chung 600 giây/50 MiB. Chỉ thêm nhánh điều phối và output audit/fixture trong script v4; không đổi logic native_child, source_for, closure/import, make_job, reconstruct hoặc compare_records. `one` chỉ đổi thứ tự chốt terminal/source-checks/manifest nêu ở mục 3. Nếu phát hiện kiểu dữ liệu, frame, công thức hoặc lỗi khác ngoài phạm vi trên, fail-stop và trình lại; không mở rộng sửa trong v4.

## Thứ tự chạy và phạm vi file

Sau Minh duyệt và full diff/source/hash hai đầu đạt:

- Đo lại tổng dung lượng mới gồm local + remote + archive/temp/lượt hỏng so trần 8 GiB, RAM khả dụng, đĩa và process. Mỗi lúc một việc nặng EC2; không làm song song native trên laptop.
- Chạy nền một job audit capture cũ rồi fresh full fixture. Tổng job tối đa **600 giây/50 MiB mới**; lỗi dừng, không retry, giữ run/PID/progress/stdout/stderr/status. Audit và đủ 23 fixture phải PASS; kiểm hash lại toàn artifact sau job đã đóng. Lệch manifest hoặc kiểm khác vẫn dừng.
- Chỉ sau điều kiện trên mới một pilot RE2-TT `dev-03d4910932`, OLS/a/h0, cặp `ols+rht_da` và `ols+rht` nguồn trong cùng job; tối đa **600 giây/150 MiB mới**, source/native–observed/frozen đều exact. Kiểm manifest terminal sau job đóng. Lệch số học thì dừng và trình chẩn đoán CIRCA laptop riêng với phạm vi/chi phí; không dùng tolerance MicroRank. Không cohort CIRCA hay A′.
- Sau pilot trình đo thực tế và dự toán trước ca tiếp; giữ yêu cầu báo CẦN GIỮ LAPTOP MỞ cho ca đầu chưa ổn định.

File đề xuất cho phép tạo:

| File/thư mục | Nội dung |
|---|---|
| `results/T-032/scripts/replay_circa_v4.py` | Sửa verifier DA, finalization; CLI posthoc audit và fixture thêm đúng mục trên |
| `results/T-032/runs/circa-da-journal-audit-fixture-001/` | Audit mới và fresh fixture, source/check/manifest/progress; không sửa run cũ |
| Thư mục monitor/launcher cùng tên dưới `runs/` | Nohup, PID, status, stdout/stderr, đo tài nguyên |
| `results/T-032/runs/circa-re2-first-001/` và monitor/launcher | Một pilot exact nếu đủ điều kiện; đường này phải còn mới, nếu đã tồn tại thì dừng trình tên lượt mới |
| Receipt mới dưới `results/T-032/runs/circa-source-001/` | Inventory, full diff/AST, source/helper pin, danh sách chuyển và hash hai đầu |
| Trên EC2: các đường tương ứng chỉ trong `~/rca/T-032/` | Không ghi task khác/code/môi trường dùng chung |
| LOG và dòng T-032 của STATE | LOG chỉ nối; STATE đọc lại ngay trước sửa đúng dòng task |
| DECISIONS: đúng dòng Q-103 bên dưới | Chỉ sau Minh duyệt, đọc lại file ngay trước nối |

Giữ tất cả bản v1–v3, capture cũ/v2 và mọi lượt hỏng. Không test, data/locked, dataset giữ ngoài, T-033, archive repo, commit/push. Chưa tạo v4 hoặc thực hiện proposal này.

## Chi phí, cách khác và phần chưa kiểm

Giờ máy tối đa 20 phút và 200 MiB mới cho hai chặng; đây là trần, không dự toán dựa trên đủ fixture/pilot đã đo. Lượt mới vừa dừng 10,57 giây không đại diện việc sẽ chạy tiếp. RAM dự trù fixture/audit 1 GiB, pilot 3 GiB là **chưa kiểm**; phải đo thực tế với job guard, không xem peak polling của lượt lỗi ngắn là cận trên. Nếu available/đĩa/global budget không đủ hoặc cần vượt trần, checkpoint và trình Minh, không chạy thêm hoặc giảm kiểm. Công sửa/soát dự trù 1–2 giờ, chưa đo.

Đã xét chỉ lấy header đầu hoặc bỏ điều kiện số lượng: nhanh nhưng che thiếu/lặp/thay đổi journal, không chọn. Đã xét đổi capture để chỉ ghi header một lần: bỏ mất chronology nguồn, thêm thay đổi observer không cần thiết, không chọn. Đã xét bỏ progress khỏi manifest: né lỗi toàn vẹn, không chọn. Đã xét chạy pilot ngay vì NodeView riêng PASS: thiếu đầy đủ fixture và hash terminal, không chọn. Dùng audit snapshot đã lưu trước giúp phát hiện lỗi verifier mà không chạy lại native; vẫn phải fresh fixture exact trước pilot.

Giả thuyết G+1 có thể sai nếu line-event semantics của interpreter khác hoặc nguồn native có đường thoát loop khác. Pin nguồn hiện tại loại việc tự thay code; các fixture G=0, nhiều nhóm, cycle và pre-loop exception kiểm trực tiếp điều kiện này trên EC2 đã duyệt. Nếu không đúng, dừng và trình, không biến thành ngưỡng gần đúng. Kết luận cơ chế CIRCA, caller/root và lợi ích quan hệ vẫn OPEN cho tới lõi valid và phần phân tích được thực hiện.

**WHY:** không đề xuất sửa WHY-42 hoặc thêm ngoại lệ nghiên cứu. Thay đổi này sửa cách đối chiếu một journal và chốt hash để thực hiện lại tiêu chí exact đã duyệt; không chọn cách chấm, ngưỡng, ca hoặc cơ chế mới. Lý do và phương án nằm trong proposal/LOG và quyết định Q-103. Nếu việc sửa dẫn tới lựa chọn khoa học mới, dừng trình đoạn WHY riêng trước khi dùng kết quả.

## Dòng DECISIONS xin Minh duyệt, chưa nối

| Q-103 | 10/10/2026 | Minh duyệt đúng results/T-032/de-xuat-circa-da-journal-002.md: chỉ tạo replay_circa_v4, giữ capture v2/helper/source/package/native/adapter và exact; kiểm DA header G+1 trên call hoàn tất, mọi snapshot/chronology/index/traversal/score/key exact, phân biệt empty và pre-loop exception; sửa terminal/source-checks ghi trước manifest cuối ở cả success/failure, giữ progress trong hash; posthoc audit capture fixture hỏng chỉ đọc theo closed transport hash, không cấp eligibility cho lượt cũ, đạt mới fresh đủ 19 fixture cũ và 4 mới, gộp audit/fixture ≤600 giây/50 MiB; đạt nguồn/hash/full fixture mới một pilot RE2 dev-03d4910932 OLS/a/h0 cặp DA/RHT ≤600 giây/150 MiB; chưa cohort, lỗi dừng không retry, drift số phải trình chẩn đoán CIRCA laptop riêng, không tolerance MicroRank; giữ mọi bản/lượt cũ, một việc nặng EC2, đo RAM/đĩa/tổng mới ≤8 GiB trước chạy, chỉ T-032/LOG/dòng STATE và receipt mới, không SPEC/WHY-42/code chung/test/locked/T-033/commit/push; cho nối đúng dòng này sau đọc lại DECISIONS. | Lời duyệt Minh; results/T-032/de-xuat-circa-da-journal-002.md |
