# Gói thay đổi đối chiếu SMTP và hợp nhất phiên bản — V2

Ngày 16/10/2026. **CANDIDATE, chờ Minh duyệt áp dụng.** Lượt này chỉ cập nhật hồ sơ T-038. Không sửa shared, SPEC, WHY/DECISIONS hoặc chuyển pin. Bản V1 đã giữ nguyên tại `../before/package-v1/`. File máy đọc: `plan.json`; bằng chứng phiên bản/hash: `input-state.json`; bản sửa tài liệu: `docs-before-after.json`.

## Trạng thái đã kiểm trên artifact hiện tại

| Nhánh | Hiện trạng | Điều không được suy ra |
|---|---|---|
| T-036 | Hợp đồng R1 và snapshot `results/T-036/runs/kiem-r1-after-002/code/` là mốc lịch sử; root manifest giữ nguyên. | Live code hôm nay không còn đồng nhất R1 do delta T-037 đã được duyệt. Đây không phải manifest hỏng. |
| T-037 | **Đã hỗ trợ SMTP và dựng mô hình đầy đủ theo thiết kế có điều kiện.** Minh đã cho sửa SMTP, kiểm lại và tiếp tục T-037, giữ T-038/T-039 nguyên pin. `runs/graph-003/` có model/graph/snapshot; `result.json#/passed`=1598, `/failed`=0. Builder nhận SMTP ở hai loại gọi; type thực tế SMTP còn chưa phân kiểu. Comparator vẫn là quy tắc cấu trúc R1. | Chưa nghiệm thu; chưa có runtime proof, chưa chuyển hai nhánh khác. Không gọi lựa chọn so cấu trúc đã được ghi giới hạn là lỗi triển khai T-037. |
| T-038 | Model005 và **1069 graph dev** đã đối chiếu dưới snapshot R1. Quan hệ SMTP có nguồn vẫn chưa đưa vào model hiện hành. | Quyền cập nhật gói này chưa cho đổi code/model/pin. Lineage/runtime nguồn TT vẫn có điều kiện. |
| T-039 | **Đã có model, mapping và bộ đối chiếu đầy đủ 132 graph dev**, run `thuc-thi-snapshot-004`. `execute_pinned.py` nhập trực tiếp snapshot T-036 gốc theo quyền Minh, không nhập live src. | Chưa nghiệm thu; inventory toàn deployment, runtime/Node/alias còn OPEN. Không còn tình huống “chưa có converter để hồi quy”. |

Nguồn trạng thái: manifest từng task được hash trong `input-state.json`; quyền T-037 tại `results/T-037/runs/tiep-smtp-001/authorization.txt`, hợp đồng tại `results/T-037/hop-dong-smtp.md`; kết quả T-039 tại `results/T-039/doi-chieu/tong-hop.json`, run verification và cost. Hash toàn268/5324/842artifact T037/T038/T039 đã kiểm trước dùng. Số1069 lấy `results/T-038/doi-chieu/index.json`; số132 lấy `results/T-039/runs/thuc-thi-snapshot-004/cost.json#/graph_count`.

## Chính xác điều xin Minh quyết

**Việc đã có:** biểu diễn `channel=smtp` trên `gọi-đồng-bộ` và `gọi-chưa-phân-kiểu`, `messaging=null`, không tạo broker/người nhận giả. Giữ builder T-037 đã kiểm, không xin thêm enum từ đầu. Snapshot/hợp đồng mới sẽ tiếp nhận delta có quyền này cùng thay đổi comparator nếu Minh chọn.

**Thay đổi mới đề xuất:** comparator nhận call `channel` tùy chọn (http/rpc/internal/smtp). Với SMTP tường minh, cả khóa `endpoints` và `typed` giữ marker `['smtp', null]`; HTTP/RPC hoặc trace không channel không có marker này. Vì vậy same-owner SMTP không còn khớp với HTTP/RPC/trace thiếu channel. Typed vẫn loại type chưa biết. Không suy channel từ static, không sửa graph T-035; adapter P9 muốn phát channel cần nguồn và quyền riêng.

Đây là **đổi nghĩa phép đối chiếu**, kể cả view endpoints, rồi **chuyển ba nhánh sang cùng manifest mới**; không thể duyệt dưới tên “chỉ bổ sung SMTP”. `kiem-preview-001/comparison-before-after.json` lưu đầu vào và hai kết quả: cùng synthetic SMTP static/trace thiếu channel, giao endpoints hiện tại là1, ứng viên là0. Chênh này là hệ quả thiết kế chủ ý, chưa là bằng chứng lợi ích RCA hay lỗi kết quả lịch sử.

Nút là service/component và operation có nguồn; cạnh SMTP hướng client→mail-server external, không tới hộp người nhận. Type phụ thuộc bằng chứng chờ của client, không suy từ tên mail hoặc delivery về sau. TT delta giữ `gọi-chưa-phân-kiểu`, operation nguồn và `runtime_name=null` khi chưa nối instrumentation. Port/host/cờ TLS, branch/retry/outcome giữ trong context/provenance; marker null không xác minh authority/port/TLS/delivery. Không thêm schema địa chỉ tổng quát. Projection, ownership, entity-only, binding/signal và shared metric giữ nghĩa cũ. Phép tính dùng cạnh là chuẩn hóa khóa, chiếu và các tập so; chưa có scoring/ranking RCA.

## Code và tài liệu cũ → mới

- **build.py và __init__.py:** dùng nguyên byte baseline T-037 graph003 hiện hành; không nằm trong patch sửa shared. Snapshot mới vẫn phải chứa chúng và hash đúng.
- **compare.py:** patch chính xác `proposed-shared-code.patch`, từ comparator hiện hành sang optional call channel/marker SMTP. Không thay API export hoặc HTTP/RPC legacy ngoài phân tách SMTP đã nêu.
- **README shared:** bản đầy đủ dự kiến `README.shared-proposed.md`; phân biệt R1 lịch sử, delta SMTP T037 và pin mới sau PASS.
- **Hợp đồng T036 mới trong run:** diễn giải call channel đã có, optional trace field, SMTP key cả hai view, unknown/missing channel/exclusions/denominators và giới hạn địa chỉ. Giữ `results/T-036/hop-dong.md` và root manifest lịch sử.
- **SPEC ba nhánh:** nối phụ lục version/adoption, giữ nguyên đoạn pin gốc như lịch sử và ngoại lệ T037/T039 đã có; không thay lời duyệt cũ. Hash/created_utc pin mới chỉ điền từ manifest thực sau kiểm. Các đoạn trước/sau và phụ lục T036 có ở `docs-before-after.json`.
- **WHY/DECISIONS:** dự thảo ghi lựa chọn đổi comparator, phương án giữ quy tắc cấu trúc hiện tại và tác động phiên bản; nguyên lời duyệt/date/mã chưa có thì để OPEN. Không ghi đề xuất thành quyết định.

## Phạm vi ghi xin duyệt và tác động

Danh sách chính xác ở `plan.json#/proposed_writes`; mọi phạm vi dưới đây chỉ có hiệu lực **sau Minh duyệt gói V2**, không suy từ quyền T038 hiện tại.

| File/phạm vi | Việc dự kiến |
|---|---|
| `src/do_thi_tinh/compare.py`, `README.md` | Áp đúng patch và README preview; builder dùng lại nguyên trạng. |
| `results/T-036/runs/doi-chieu-smtp-001/` | Hồ sơ sửa mới: before/oracle/hợp đồng/code snapshot/hash, check runner, mọi lần chạy/kết quả/chi phí, manifest pin và bàn giao/prompt. Không ghi root manifest T036. |
| `tasks/T-036-p5b-hop-dong-chung/SPEC.md` và LOG | Nối phụ lục sửa được duyệt và LOG thực; T036 gốc đã đóng vẫn là lịch sử. |
| `tasks/T-037-p5b-flashticket/SPEC.md`, `tasks/T-038-p5b-trainticket/SPEC.md`, `tasks/T-039-p5b-online-boutique/SPEC.md` và LOG tương ứng | Nối phụ lục quyền/pin mới và tiến trình thực tế; giữ delta T037, direct-snapshot T039 và pin cũ cho output cũ. |
| `docs/WHY.md`, `docs/DECISIONS.md` | Chỉ nối lý do/version và nguyên quyết định thực sau duyệt; nội dung dự thảo xem before→after. |
| `docs/STATE.md` | Chỉ dòng T036–T039, cập nhật tuần tự bản mới nhất; không tự nghiệm thu hoặc đổi G3. |
| `results/T-037/runs/doi-chieu-smtp-001/` | Pin loader/runner mới; snapshot full model/graph003/registry/fixture, dựng và so đầy đủ fixture hiện có với hai comparator, giữ tập/members/loại trừ/mẫu số và diff. Không thay counterexample/rejection oracle lịch sử. |
| `results/T-038/runs/doi-chieu-smtp-001/` | Pin loader/engine/compare runner mới, delta SMTP có nguồn, rebuild hai mức và so đủ1069 graph; per-graph output/diff nằm trong run mới. |
| `results/T-039/runs/doi-chieu-smtp-001/` | Pin loader và `execute_common.py` tiếp nhận từ **execute_pinned.py đã có**; rebuild full model, replay **đủ132 graph**, output/diff từng graph trong run mới. Không kiểm smoke thay replay. |
| Bản hiện hành của T037/T038/T039 liệt kê trong plan.json | Sau cả ba nhánh PASS mới cập nhật model/graph/mapping/registry khi có delta, chỉ mục/phân tích/kiểm/bàn giao/prompt/manifest với pin mới. Giữ byte trước trong before/ và mọi output cũ nguyên pin. Coverage/source không tự tăng do đổi comparator. Nếu thất bại giữ trạng thái chuyển chưa xong, không đánh tráo pin. |

Tên run đều đã kiểm chưa tồn tại khi trình V2. Nếu có nhánh thay đổi trước khi áp dụng, kiểm lại input-state, báo chênh và cập nhật đề xuất; không áp patch lên baseline khác. Không có quyền sửa T035, nguồn ứng dụng, repo platform, raw/test/heldout, dependency hay môi trường; không tải thêm, commit/push hoặc gửi agent.

## Tiếp nhận runner và hồi quy đầy đủ

1. Kiểm hash tất cả baseline/manifest, giữ pin cũ. Chép oracle literal trước sửa; dùng snapshot độc lập để so R1, T037 đã SMTP và candidate, không gọi live hiện tại là R1. Chạy lại toàn checker T036/R1 và SMTP regression T037 trong run mới, giữ mọi lỗi.
2. Loader mới nhận đường dẫn/SHA/created_utc manifest mới tường minh, kiểm hash từng module snapshot và live rồi import namespace riêng; không HEAD/fallback R1. ROOT/input/output root tường minh. `T038/engine.py:pinned_api` hardcode R1/live hash nên giữ lịch sử, tạo runner mới; chỉ sửa SPEC không đổi runner là chưa đủ.
3. T037 dùng full model/registry `graph-003`, snapshot `input-code-hashes.json`, `runner.py`, `assemble-complete.py`, oracle/fixtures đã có, không giả định thiếu converter. So nguyên model không delta, cả hai mức/projection/entity-only/shared signals và mọi fixture; phân tách thay đổi comparator chủ ý khỏi bất biến builder. Không biến fixture thành runtime trace thật.
4. T038 đóng băng1069 input/mapping/context; lưu baseline R1, candidate cùng model cũ, rồi candidate với delta SMTP để **tách ảnh hưởng comparator khỏi thêm quan hệ**. So từng tập S/T/giao/hiệu/members/exclusions/mẫu số, hai mức/full/N/A/s60/s300; kiểm nguồn/unknown/unmapped, lặp/đảo và input bất biến. Không bỏ cạnh thiếu trace để tăng giao.
5. T039 runner hiện tại nhập `results/T-036/runs/kiem-r1-after-002/code`; giữ file đó, tạo `execute_common.py` từ logic thực với pin_loader. Dựng lại model hiện có và replay132 graph cùng mapping/context, so từng tập/members/exclusions/mẫu số. Không biến “không có SMTP được ghi” thành lý do bỏ hồi quy hoặc đóng source/runtime OPEN.
6. Xuất diff riêng từng tác động; phần không SMTP phải bằng baseline nếu không có hệ quả thiết kế đã khai báo. Mọi khác biệt ngoài dự kiến phải lần theo đầu vào→mapping→key→set; không sửa oracle để PASS. Tiếp nhận cả ba đầy đủ mới publish các bản hiện hành theo cùng pin. Mỗi output mang pin của lượt sinh ra nó; chuyển hiện hành không viết lại lịch sử. Kiểm complete diff/phạm vi/LOG append-only/STATE đúng dòng/prompt chuẩn, rồi Minh quyết riêng nghiệm thu.

**Tự kiểm hiện có:** `oracle-before-code.json` ghi24case literal và5case hồi quy trước candidate; `kiem-preview-001/checks.json` **29/29 đạt**. Có rebuild exact-equal legacy T036, frozen T038, **full model T037 hiện tại và T039 hiện tại**, và phản ví dụ thay semantics. `candidate-code-hashes.json` cho biết builder không sửa. Đây chưa phải full1069/132 comparator replay, chưa phải adoption/common manifest; phần ấy chờ quyền chung vì thay giao thức và bản dùng ba nhánh. Không có SMTP thật/network hoặc evidence delivery.

## Phương án, câu hỏi nguồn và giới hạn

- **Giữ comparator cấu trúc hiện tại + tiếp nhận builder SMTP:** là phương án ít thay đổi, hợp lệ nếu ghi rõ chỉ so cấu trúc. Đây là baseline T037 đã có, không phải unsupported. Chưa phân biệt hai protocol cùng owner; Minh có thể chọn phương án này thay marker và phải cập nhật gói trước áp dụng.
- **Marker SMTP đề xuất:** phân biệt chặng SMTP trong phép so; trace thiếu protocol sẽ có thêm thiếu bằng chứng tương ứng, không chứng minh cạnh nguồn sai hoặc runtime không gửi. Có thể làm giảm giao khi telemetry thiếu channel. Đây là giả định thiết kế để thử, chưa là chọn phương pháp P6.
- **Schema transport/authority/port/TLS tổng quát:** phân biệt sâu hơn nhưng cần telemetry/adapter/chuẩn hóa có nguồn và quyền riêng; marker hiện tại không trả lời câu hỏi ấy. Đổi taxonomy mail/broker không có căn cứ cho cạnh gửi hiện tại.

Đáp ứng DT18-NV2, MRP P5 và bước1 của cô ở biểu diễn quan hệ/địa chỉ có nguồn và so hai nguồn; không xác nhận cơ chế phát hiện/ranking, RQ3/RQ5, lợi ích đồ thị, G3 hay mở test. Runtime lineage TT/OB, hiệu lực thư viện/TLS/delivery, phạm vi deployment và alias vẫn OPEN. Để phân xử runtime cần image/build/instrumentation/deployment và trace channel có provenance từ chủ nguồn qua Minh; không thể lấy fixture hoặc cờ thiếu dữ liệu thay bằng chứng. Nếu cần authority/port/TLS, trình schema/thu thêm tương ứng trước kết luận. Mapping sai mail-server/channel do suy đoán/type tự nâng hoặc accepted=delivered là điều kiện thất bại, phải dừng kết luận phụ thuộc.

## Chi phí cập nhật

**Dự toán CANDIDATE chưa đo:37 phút máy, khoảng600MB output**, chạy tuần tự trong một phiên, không tải nguồn. Gồm shared2phút/50MB, T03710/150, T03810/150, T0395/100, dự phòng một lượtTT10/150. Không dùng dự toán V1 31phút/550MB vì chưa gồm hồi quy đầy đủ FT/OB. RAMTT dự trù0.5GiB; các peak khác chưa đo, không cộng peak. Thời gian soạn/đọc và mọi lỗi chưa biết không phải benchmark; nếu một lượt dự kiến >1giờ hoặc phát sinh phạm vi/tải khác thì báo Minh đúng luật hiện hành.

Số đã đo chỉ để tham khảo: TT pin cũ `kha-thi.json#/full_and_pilot_runs` ~4–6phút cho1069; OB run004 `cost.json`132graph,3.669giây, peak71557120bytes, **isolated_benchmark=false**, không ngoại suy sang full regression. Preview29 chỉ đo trong `checks.json#/elapsed_seconds`, không đo peak riêng. Kế hoạch37phút là dự trù tác vụ/kiểm/phân tích, không suy từ phép nhân thời gianOB. Giữ mọi lượt và cập nhật số thực sau chạy.

## Tiêu chí gói được áp dụng xong sau duyệt

Hợp đồng/README/WHY/DECISIONS/SPEC đúng nghĩa comparator mới; patch chỉ compare và builder giữ byte T037; toàn T036/R1/SMTP và full model/fixture T037,1069TT,132OB có artifact so tập/members/loại trừ/mẫu số, input/ordering/hash/projection/mapping; tách delta TT và comparator. Pin manifest mới tồn tại/được hash và cả ba runner dùng đúng nó, output cũ nguyên pin. Trạng thái OPEN khoa học giữ đúng nguồn, Minh quyết nghiệm thu riêng. Nếu chỉ preview đạt thì gói vẫn **chưa áp dụng**.
