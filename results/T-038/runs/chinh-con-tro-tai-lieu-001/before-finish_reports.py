"""Tạo tài liệu bàn giao từ kết quả đã khóa; chỉ ghi phạm vi T038."""
from collections import Counter
from copy import deepcopy
import datetime as dt
import json
from pathlib import Path
from engine import ROOT, OUT, REV, load, save, checksum, canon


def write(name, content):
    (OUT / name).write_text(content.strip() + '\n', encoding='utf-8')


def main():
    base = OUT / 'runs/trien-khai-001'
    coverage = load(base / 'coverage/coverage-final.json')
    follow = load(base / 'java-source/binary-followup.json')
    final = load(base / 'java-source/followup-final.json')
    refinements = {r['path']:r for r in follow['recommendations'] if r.get('proposed_status') == 'excluded'}
    refinements.update({r['path']:r for r in final['results'] if r.get('proposed_status') == 'excluded'})
    assert len(refinements) == 24
    for row in coverage['files']:
        if row['path'] in refinements:
            assert row['status'] == 'open'
            row.update(status='excluded', read_depth=refinements[row['path']]['read_depth'],
                       reason=refinements[row['path']]['reason'], refinement=refinements[row['path']])
    counts = dict(Counter(r['status'] for r in coverage['files']))
    assert counts == {'read':2758, 'excluded':42, 'open':27}
    acquired = load(OUT / 'runs/tai-nguon-001/manifest.json')
    assert acquired['ok'] and acquired['file_count'] == 2827
    for row in acquired['files']:
        # Hash-only cả nhóm hạn chế. Không parse/hiển thị raw sample hay index lỗi.
        assert checksum(ROOT / row['path']) == row['sha256']
    prior = load(base / 'before-nguon.json')
    lineage = deepcopy(prior['lineage'])
    lineage[2].update(state='FACT', meaning='Gói tham khảo có điều kiện đã được Minh duyệt tải; đủ blob/tree. Chưa xác minh nguồn sinh RE2-TT.', evidence='results/T-038/runs/tai-nguon-001/manifest.json')
    coverage.update(statuses=counts, groups={g:dict(Counter(x['status'] for x in coverage['files'] if x['group']==g)) for g in sorted({x['group'] for x in coverage['files']})},
        verified_blob_count=2827, integrity_depth='Acquisition and final hash-only verification of every blob, including protected samples. Not content permission.',
        refinement_sources=['runs/trien-khai-001/java-source/binary-followup.json','runs/trien-khai-001/java-source/followup-final.json'],
        lineage=lineage, semantic_source_inventory_complete=False,
        read_caution='read = declared depth, often full lexical scan/pattern index; not full semantic proof. Excluded includes quarantined samples, not just proven irrelevant assets.',
        source_registry='results/T-038/nguon.json', unresolved_inputs=load(base/'coverage/facts.json')['external_sources'],
        open_details=[x for x in final['results'] if x.get('proposed_status') == 'open'],
        incident_metadata='results/T-038/runs/trien-khai-001/coverage/incident.json',
        incident_effect='Historical sample/image/workbook access violated no-raw instruction; contaminated indexes quarantined, not used by facts/model/mapping. No RE2 raw/test/heldout opened.')
    save(OUT / 'bao-phu-nguon.json', coverage)
    summary = load(OUT / 'runs/doi-chieu-dev-002/summary.json')
    previous = load(OUT / 'runs/doi-chieu-dev-001/summary.json')
    assert summary['graph_count'] == 1069 and not summary['errors']
    assert [r['output_sha256'] for r in summary['rows']] == [r['output_sha256'] for r in previous['rows']]
    save(OUT/'runs/doi-chieu-dev-002/cross-run-equivalence.json',dict(ok=True,graph_count=1069,
        comparison='SHA of all lossless JSON gzip outputs identical between 004 and 005 source models; added signals do not enter edge comparison.',
        first='doi-chieu-dev-001',last='doi-chieu-dev-002',different_edge_results=0))
    assembly = load(OUT / 'runs/lap-ban-ghi-005/result.json')
    analysis = load(OUT/'phan-tich-chenh-lech.json')
    mapping = load(OUT/'mapping-summary.json')
    write('bao-phu-nguon.md', '''# Nguồn Train Ticket và độ đủ

Đạt một phần. Đã nhận đủ cây release v1.0.0 được Minh duyệt: 3.921 mục, gồm 1.094 thư mục và 2.827 blob. Revision/tree/hash nằm trong manifest tải; không lấy HEAD. Không có gitlink; 8 symlink giữ nội dung literal, không tạo link thật. Đối chiếu byte/hash mọi blob đạt. Nguồn số: `runs/tai-nguon-001/manifest.json#/file_count`, `#/materialized_blob_bytes`; `bao-phu-nguon.json#/files`.

Phân hoạch cuối: 2.758 blob đã đọc ở độ sâu ghi riêng, 42 loại khỏi chuỗi bằng chứng, 27 OPEN (`bao-phu-nguon.json#/statuses`). “Đã đọc” gồm quét toàn văn/từ khóa, đọc cấu trúc container hoặc đọc thủ công theo nguồn; không có nghĩa mọi hành vi được phân xử. Nhóm loại có cả mẫu bị hạn chế và ảnh đã cách ly, không phải tất cả đều đã chứng minh không liên quan. Toàn cây đã kiểm khác với inventory ngữ nghĩa đầy đủ.

Đã lần root POM → 42 module (41 ứng dụng Java, một thư viện), cấu hình tên → controller/service/repository/client/worker → HTTP, data và messaging. Có nguồn Python/Go/Node, UI/nginx, Docker/build và 617 khai báo resource K8s theo profile. Không gộp các profile thành một deployment đã chạy. V1 quickstart mặc định MySQL/Nacos/RabbitMQ; Skywalking/Elasticsearch là profile tracing; Prometheus/Grafana là monitoring. Mongo/Jaeger lịch sử không trở thành runtime v1 chỉ vì còn nằm trong cây. Bằng chứng: `runs/trien-khai-001/coverage/facts.json` và `java-source/source-facts.json`.

24 loại trừ bổ sung có căn cứ nội dung/tham chiếu: font, icon/logo/avatar fallback, Gradle local state, Unicode bitfields, Maven wrapper và huy hiệu bài báo. Bằng chứng nằm trong `java-source/{binary-followup,followup-final}.json`, không chỉ dựa vào tên/đuôi. Còn 27 OPEN: 24 ảnh chưa phân loại chắc có telemetry hay không, một swap ở vị trí Helm template, một PDF lịch sử mới đọc metadata và một archive instrumentation mới đọc một phần. Mỗi mục có input/tool/quyền thiếu, ảnh hưởng và ước tính phút ở `bao-phu-nguon.json#/open_details`. Không đọc thêm nội dung có thể là telemetry để đóng bảng.

Archive chứa hai artifact instrumentation và 161 Java source nhúng đã đọc an toàn; khác namespace/nội dung với thư viện loose lịch sử. Các POM hiện hành không có direct reference đã tìm thấy; chưa chứng minh transitive/profile/image activation. Không dùng hook span-name trong archive để xác nhận tên thao tác RE2-TT. Thư viện ngoài repo, image digest/build provenance, wiki build và workload repo chưa nằm trong gói được duyệt. Config/template chưa render chỉ là khai báo có điều kiện; script sinh Secret có bất nhất cú pháp đã lưu, không nhận output giả định là deployment thật.

Chuỗi sáu trục ở `bao-phu-nguon.json#/lineage`: revision code RCAEval và snapshot dataset đã được phân biệt với commit ứng dụng tham khảo. Paper nối tới repo không ghim bản thu. Instrumentation, image và deployment sinh RE2-TT vẫn OPEN. Tag/image name hoặc độ giống graph không đủ nối chuỗi này. Owner cần cung cấp là chủ nguồn RCAEval, qua Minh: application commit, image digest/build metadata, agent/version/config, manifest/namespace/runtime config và thời gian thu. Chưa có chúng, mọi JSON so sánh giữ `conditional_reference=true`.

Sự cố đã báo ngay: nhánh hỗ trợ đọc nhầm 15 mẫu telemetry lịch sử công khai, XML của debugging workbook và một ảnh Jaeger UI. Root không đọc index lỗi; các bản lỗi được giữ, cách ly khỏi facts/graph/mapping/kết luận và tạo index sạch. Metadata sự cố ở `coverage/incident.json`. Không mở RE2 raw, data/locked, test hoặc heldout. Việc cách ly không hoàn tác lần đã đọc và không làm tuyên bố tuân thủ cả phiên trở lại hợp lệ.

Kết luận: có mô hình nguồn tham khảo và bảng thiếu cụ thể; chưa nhận inventory đầy đủ hoặc độ phủ instrumentation. Phần thiếu vẫn thuộc nghĩa vụ nghiên cứu, chưa bị loại vì ngoài SPEC. Xem `de-nghi-tiep-theo.md` cho đầu vào, owner, phép phân xử và phạm vi cần Minh quyết.
''')
    table = ['| Mức/miền | Graph | S | T | Giao | Riêng tĩnh | Riêng trace |','|---|---:|---:|---:|---:|---:|---:|']
    for r in analysis['family_stats']:
        if r['view'] != 'endpoints': continue
        def interval(k):
            v=r['values'][k]; return str(v['min']) if v['min']==v['max'] else f"{v['min']}–{v['max']}"
        table.append('| '+r['level']+'/'+r['family']+' | '+str(r['graph_count'])+' | '+' | '.join(interval(k) for k in ['S','T','intersection','static_only','trace_only'])+' |')
    write('phan-tich-chenh-lech.md', '''# Đối chiếu nguồn và graph dev RE2-TT

Đã so mọi graph hiện hành được giao, trên nguồn tham khảo có điều kiện. Số và từng thành viên nằm trong `runs/doi-chieu-dev-002/summary.json#/rows`, JSON gzip theo `doi-chieu/index.json` và `phan-tich-chenh-lech.json`. Bảng sau là min–max từng graph, không phải số cạnh độc nhất gộp qua ca.

'''+ '\n'.join(table) + '''

30 dev ID là mã mờ để điều phối, không đi vào phép tính khóa cạnh. Chọn đúng prefix manifest T035, không trộn lịch sử. Có 979 graph thực thể và 90 graph thao tác; full/N/A ở cả hai mức, 739 cửa sổ 60 giây và 150 cửa sổ 300 giây ở mức thực thể. Giữ interval/miền gốc; không mở lại telemetry để dựng cửa sổ khác. Nguồn số: `summary.json#/graph_family_counts`.

S là khóa tĩnh đủ điều kiện, T là khóa trace đủ điều kiện sau mapping; giao và hai phần riêng được tính bằng tập có hướng. Mỗi khóa giữ members với chỉ số/cạnh gốc/provenance riêng hai nguồn; exclusions phân hoạch phần không vào khóa. Không dùng inventory hoặc nút quan sát làm mẫu số cạnh. Typed T rỗng ở toàn bộ 1.069 graph vì kiểu trace còn unknown, hoặc đầu mút thao tác chưa đủ mapping. Trace fraction là null khi mẫu số rỗng, không là 0% coverage. 19 cửa sổ s60 có T endpoints rỗng, cũng giữ null. Các trường min/max/null_count đầy đủ ở `phan-tich-chenh-lech.json#/family_stats`.

## Đầu mút khớp không xác nhận transport hoặc phiên bản

Ví dụ admin-basic-info → config: mã nguồn có các callsite HTTP GET/POST/PUT/DELETE; bản ghi giữ từng điều kiện và provenance, graph thực thể gộp thành cặp có hướng. Mapping identity dựa khai báo component, không dựa nhãn. Cạnh trace cùng cặp giữ `gọi-chưa-phân-kiểu`; vì thế endpoints có thể giao nhưng typed bị loại. Chuỗi nguồn → record_ids → edge → members → tập nằm tại `phan-tich-chenh-lech.json#/chain_examples`, lọc cặp này; locator nguồn đi kèm từng member. Bước so typed giữ thiếu thông tin thay vì lấy HTTP nguồn lấp unknown trace. Không xác nhận HTTP/RPC transport của runtime hoặc instrumentation coverage từ endpoint match.

## Năm cặp riêng trace và đối chiếu nguồn tương ứng

Hợp của full endpoints có đúng năm cặp riêng trace: food→station, seat→travel, seat→travel2, travel→order, travel2→order-other (`phan-tich-chenh-lech.json#/full_union`, entity/endpoints/trace_only). Từng trường hợp, số graph chứa và witnesses gốc còn trong `edge-groups.json` và members; không cộng số xuất hiện qua cửa sổ thành số nguyên nhân.

Đã đọc toàn 38 Java file hiện hành của bốn module và helper liên quan. Không tìm được direct call cho năm cặp trong corpus đó. Control dương cùng cách gọi: food gọi travel và station-food; travel/travel2 gọi seat; seat gọi order hoặc order-other theo nhánh G/D. Chain travel→seat→order có controller/service và callsite đúng dòng; không co thành direct travel→order, không đảo chiều thành seat→travel. Biến stationResult trong food nhận body từ travel, tên biến không tạo endpoint station. Nguồn và line ở `coverage/mismatch-source-followup.json#/pairs`; chuỗi so sánh ở JSON phân tích.

Quan sát này hỗ trợ việc nguồn tham khảo không cung cấp direct edge tương ứng trong phần đã kiểm. Chưa phân xử source revision khác, alias/config override, dependency động, thiếu phân tích tĩnh, cấu trúc span hoặc instrumentation runtime. Không gọi absence nguồn là lỗi collector hoặc khẳng định runtime không có call. Cần application/image/instrumentation/deployment của bản thu và callsite/span attributes trước khi phân xử các giải thích đó.

## Khác tên và khác họ cấu hình

Hai tên observed `ts-food-map-service` và `ts-ticketinfo-service` không có identity đã xác minh trong inventory hiện hành nên giữ unmapped; không đổi thành station-food/basic theo chức năng giống nhau. Các tên thao tác kiểu `find ts.*`, `getMore`, `update`, và `find ts-auth-mongo.user` là chuỗi đã lưu, không tự chứng minh database implementation. V1 nguồn dùng JDBC/MySQL/Nacos, các sơ đồ/nguồn Mongo lịch sử thuộc profile khác. Đây là dấu hiệu cần kiểm lineage, chưa xác nhận nguyên nhân riêng của từng mismatch. Mapping và ghi chú đầy đủ ở `mapping.json`, `mapping-summary.json`, `runs/doi-chieu-dev-002/mapping-notes.json`.

## Vì sao mức thao tác chưa so được T

54 tên thao tác toàn miền có descriptor HTTP cùng owner khớp chính xác về cấu trúc; 16 mơ hồ, 35 candidate chưa verified và 49 unmapped. Đây là status của 154 tên khác nhau, không phải tỷ lệ cạnh. T035 đặt ID bằng (serviceName, operationName), tại `src/do_thi/builder.py:177–181`; generic GET trong cùng owner không giữ callsite/URL để chọn giữa nhiều source method. Các method repository chỉ là candidate; không biết agent đã tạo span ấy thế nào. Cụ thể chuỗi input operationName → ID T035 → mapping nhiều/chưa xác minh → exclusion đầu mút → không tạo khóa T đã được lưu trong `phan-tich-chenh-lech.json#/exclusions`. Trong 90 graph thao tác, mọi cạnh bị loại ở ít nhất một đầu mút; do đó T đủ điều kiện rỗng, không có nghĩa không có lời gọi.

Đây là hạn chế địa chỉ của graph đầu vào và quan hệ mapping hiện tại. Chưa chứng minh trường URI/kind/callsite đã từng có trước conversion hay collector làm mất: đặc tả T035 §2 chỉ cam kết lõi, p3 thêm kind=null/attributes={}/links=[]; raw không được mở ở task này. Muốn phân xử cần schema/instrumentation tại phiên bản thu hoặc trung gian được duyệt có URI/callsite/span-kind; không được tự dùng endpoint nguồn tạo runtime_name. Runtime_name của các operation nguồn vẫn OPEN. Đối chiếu dương exact owner+HTTP descriptor và phản ví dụ generic GET/sai owner/concrete ID nằm trong oracle và fixture result.

## Cửa sổ, nhánh và phần riêng tĩnh

Nguồn là hợp các lời gọi khai báo có điều kiện, không path-sensitive reachability hay workload. Bởi vậy không gán mọi static_only là mất telemetry. `edge-groups.json` giữ ví dụ cùng cặp khớp full nhưng vắng ở s60 cùng dev ID; điều này xác nhận membership thay theo miền, chưa nói vì không chạy nhánh, không quan sát, hay xử lý biên. Muốn phân xử cần workload/version và trung gian đã thu trong quyền. Thành phần source-only và DB default chưa được runtime xác nhận cũng có thể tạo phần riêng tĩnh; không cộng các nhóm chồng lấn thành tỷ lệ nguyên nhân.

## Lỗi literal nguồn và giới hạn hợp đồng

Rebook.updateOrder dùng PUT, khớp handler PUT của order/order-other. Cùng helper/owner, deleteOrder lại POST lên đường dẫn orderId trong khi handler khai DELETE. PollThread POST `/api/v1/contactservice/preserve`, khác handler `/api/v1/preserveservice/preserve`. Giữ nguyên literal và candidate, không sửa nguồn để tạo match; entity match có thể che bất nhất method/path. Đây là bất nhất source snapshot, chưa chứng minh bug của RE2. Mã/line trước→sau đã lưu tại `runs/doi-chieu-dev-002/source-chain-snippets.json`.

Messaging giữ queue/routing key khai báo, broker quickstart có điều kiện, broker_scope/exchange chưa xác minh nên bị loại theo hợp đồng; không nối producer→consumer chỉ từ tên queue. DB logical schema khác endpoint instance và owner; source default/env override không là physical deployment. Shared signal chỉ gắn entity một lần theo nguồn, operation=null, không nhân thành tín hiệu quan sát mỗi operation. Java logger và Java-agent env là khai báo; chưa có output schema/correlation, ba module nonJava có env Java-agent chưa chứng minh agent hoạt động.

SMTP có cấu hình smtp.163.com:465 và MailService.sender.send; enum T036 không nhận channel này. Đã lưu phản ví dụ thật, giữ external entity và ngừng riêng relation SMTP, không ép thành HTTP/RPC/broker. Đó là thiếu biểu diễn ở giao thức nguồn, khác thiếu dữ liệu hay lỗi adapter. Toàn mô hình chưa đủ quan hệ. Archive/libraries/config chưa render và nguồn OPEN có thể bổ sung quan hệ khác; không gọi coverage đầy đủ.

## Hàm ý nghiên cứu

Đồ thị được dùng để chuẩn hóa địa chỉ, chiếu operation→entity, tạo khóa có hướng và tính giao/phần riêng; chưa tính anomaly score, tập ứng viên hay rank. Kết quả hỗ trợ đầu vào kiến trúc/địa chỉ và yêu cầu quan sát cho DT18 bước khảo sát, RQ3/RQ5. Chưa chứng minh lợi ích RCA, cơ chế của lỗi baseline, nên chưa chọn P6 hay đóng G3. Bảng input/owner/phép phân xử/P6/P9 nằm ở `ban-giao.md` và `de-nghi-tiep-theo.md`.
''')
    write('kiem-dung-dan.md', f'''# Tự kiểm T-038

Pin chung T036 giữ nguyên bản sau R1, manifest/current_run theo SPEC; kiểm đủ artifact và cả code hiện hành so với snapshot. T035 chọn đúng manifest prefix và allowlist dev, không dùng graph lịch sử. Preflight và các lượt lỗi được giữ. Nguồn: `runs/kiem-dau-vao-002`, `runs/mien-graph-002`, `runs/metadata-de-xuat-001`, `runs/tai-nguon-001`.

Oracle literal độc lập được ghi trước mã riêng ở `fixtures/oracle.json`: entity/operation, projection, entity-only, mapping cùng owner/descriptor, generic verb, sai owner, concrete ID, tập/mẫu số null. Không gọi oracle supplemental là pre-code. Phép SMTP là counterexample sau khi đọc nguồn. Lượt cuối đạt {summary['fixture_checks_passed']}/{summary['fixture_checks_total']} checks (`runs/doi-chieu-dev-002/fixture-result.json#/checks`). Scanner Java có oracle thủ công viết sau extraction, không phải oracle trước mã; kiểm 32/32 và audit assembly004 14/14 chỉ bảo vệ phạm vi đã nêu, không chứng minh parser đầy đủ.

Từng graph kiểm độc lập S/T/giao/phần riêng từ quy tắc khóa của input unknown hiện có; kiểm members/exclusions là phân hoạch chỉ số, mỗi original đúng input, mẫu số rỗng=null, interval/input không đổi. Chạy cùng input lần hai và đảo thứ tự hợp lệ lần ba; đạt trên 1.069 graph. Giữ verification/hash từng phép lặp, lưu full kết quả chính lossless JSON gzip và roundtrip; không ghi full bản lặp giống hệt chỉ để nhân đĩa. Khi khác đã thiết kế giữ full sai. Nguồn: `runs/doi-chieu-dev-002/self-checks.json` và runner snapshot. Typed/operation rỗng được diễn giải là không đủ điều kiện so, không là absence/coverage.

Assembly005: {assembly['entities']} entity, {assembly['operations']} operation, {assembly['relations']} relation, {assembly['bindings']} binding, {assembly['signals']} signal; {assembly['unresolved']} unresolved records. Hai graph có {assembly['entity_edges']} cạnh entity và {assembly['operation_edges']} cạnh operation. Inventory/bản ghi không bị cắt theo observed nodes. 139 signal gồm 94 log, 42 trace, 3 metric; chỉ là địa chỉ/kết nối khai báo nguồn. `runs/lap-ban-ghi-005/result.json` và `phan-tich-chenh-lech.json#/source_counts` là nguồn số.

Source HTTP giữ tất cả 160 alternative của 146 callsite, chín empty initialization OPEN; không âm thầm pruning nhánh. Target operation chỉ nhận khi literal không dynamic và descriptor method/path khớp duy nhất; 71 trường hợp candidate-only vẫn OPEN. Có 273 repository callsite; không tạo DB operation giả. So supplemental signal không đổi cạnh: toàn bộ 1.069 SHA JSON gzip giữa full001/model004 và full002/model005 giống nhau (`cross-run-equivalence.json`).

Các lượt hỏng còn nguyên: preflight001 sai đường dẫn snapshot; graph-scope001 duplicated prefix; assembly001 schema fact; assembly003 target dynamic đã giảm ở004; pilot001 đưa sai level mapping, pilot002 RAM API trả 0 không hợp lệ, không dùng số đó; scanner sửa newline và history riêng; coverage incident được giữ/cách ly. Counterexample SMTP thử đầu thiếu field messaging bị schema từ chối, bản sửa đủ field mới xác nhận relation_type; cả hai giữ dưới runs. Không nâng một run chạy không lỗi thành xác minh runtime hoặc inventory đầy đủ.

Không có số công bố tương ứng cho bộ đọc này; đối chiếu nguồn, oracle, trung gian và set độc lập thay vì dựng baseline giả. Không chạy baseline/RCA/test/P6, không bật EC2 hoặc dùng GPU. Kiểm cuối về AST/JSON chọn lọc/hash/diff/append-only và quyền ghi nằm tại `runs/ket-phien-002/final-verification.json` sau khi finalizer chạy. Bản cuối manifest phủ cả nguồn/history; raw samples và index lỗi chỉ được hash, không parse lại để kiểm JSON.
''')
    write('ban-giao.md', '''# Bàn giao T-038 cho Minh và Claude

Đạt một phần, chờ phản biện kết quả; chưa đề nghị nghiệm thu đầy đủ. Minh yêu cầu không tách và đã duyệt gói tải; đã làm trong cùng phiên, không tạo task/SPEC mới. Full dev comparison đã xong trên bản nguồn có điều kiện. Các tiêu chí còn phụ thuộc SMTP/coverage/lineage được nêu cụ thể, không biến thiếu nguồn thành thu hẹp mục tiêu.

Điểm vào: `bao-phu-nguon.md/json` (toàn cây, lineage, phần OPEN), `nguon.json` (registry), `ban-ghi.json`, `inventory-index.json`, `mapping.json`, `mapping-summary.json`, `do-thi/`, `doi-chieu/index.json`, `phan-tich-chenh-lech.md/json`, `kiem-dung-dan.md`, `kha-thi.json`, `manifest.json`. Bản chụp assembly cuối là runs/lap-ban-ghi-005; comparer cuối là runs/doi-chieu-dev-002; giữ mọi lượt trước. Hash/revision tập trung ở manifests và registry.

| Bên nhận | Thông tin cung cấp được | Phần thiếu/điều kiện và phép phân xử |
|---|---|---|
| T-040 | Inventory/operations và quan hệ có provenance; toàn graph/cửa sổ, tập/members/exclusions, nhóm chênh lệch source→key→set | Không cộng các cờ thành tỷ lệ nguyên nhân; tổng hợp ba nhánh phải cùng pin, giữ revision conditional; chưa đủ inventory ngữ nghĩa |
| P6, RQ3/RQ5 | Entity/operation khác địa chỉ, data/broker/worker/shared signals, cấu trúc nguồn ngoài trace; đồ thị đã có vai trò tính toán tập | Chưa chọn mức/thuật toán/tín hiệu; cần bằng chứng dev cho thiết kế và đối chứng tương đương, chưa có lợi ích RCA từ phép giao |
| P9 FlashTicket | Cần owner/component ID ổn định; endpoint method+route và client callsite; kind/transport; logical DB và physical instance riêng; broker namespace/exchange/routing/queue; trace/span correlation cho log và địa chỉ scrape/resource của metric | Đây là yêu cầu quan sát rút ra từ thiếu địa chỉ hiện có, không chứng minh collector sửa được lịch sử. Cần kiểm schema/runtime FT với baseline quan sát trong task được duyệt; không sửa FT ở đây |
| Chủ dữ liệu qua Minh | App commit/image digest/build metadata; instrumentation version/config; deployment manifest/env/namespace/time scope; workload và schema capture | Dùng để phân xử revision, alias, nhánh/workload, telemetry và conversion; chưa có thì quan hệ nguồn chỉ tham khảo |

SMTP relation dừng riêng vì T036 không biểu diễn được, external entity còn trong inventory; phản ví dụ ở fixtures/smtp-counterexample.json. Không fork nghĩa chung cho TT. 27 blob OPEN và nguồn ngoài chưa được phép lấy có danh sách/input/owner/ước tính ở coverage và de-nghi-tiep-theo.md. Không cần chạy lại graph chỉ để làm đẹp coverage; phép bổ sung phải giải quyết đúng câu hỏi còn thiếu.

Sự cố đọc telemetry mẫu công khai của nhánh hỗ trợ đã được báo ngay và ghi trong LOG/coverage incident. Đã giữ bản lỗi, không dùng cho facts/model/mapping/kết luận; không có RE2 raw/test/heldout/data khóa được mở. Reviewer cần kiểm phạm vi phụ thuộc từ artifacts thực, không dựa lời khẳng định của người làm.

Tiếp theo chính xác: Minh chuyển `prompt-claude.txt` cho Claude để soát kết quả. Chưa có quyền ghi REVIEW thì Claude chỉ đọc/trả lời chat; Minh quyết phạm vi review riêng. Root không tự gửi. Minh quyết hướng xử lý phần thiếu sau xem đề xuất cụ thể. Không commit/push nếu chưa được yêu cầu. Commit đề nghị sau duyệt: `T-038: khảo sát nguồn Train Ticket và đối chiếu dev có điều kiện` (chỉ file T038/LOG và dòng STATE hợp lệ).
''')
    write('de-nghi-tiep-theo.md', '''# Phần cần Minh quyết sau kết quả T-038

Chưa thực hiện các đề nghị sau. Không tách task trong phiên này, không sửa SPEC, nguồn chung hoặc tài liệu quyết định. Các mục này là CANDIDATE/OPEN, không phải quyết định thiết kế.

1. **SMTP:** nguồn thật có sender.send và host:465, nhưng shared enum từ chối. Phương án tối thiểu trước mắt là giữ external entity + unsupported relation ngoài graph, kết luận đạt một phần như hiện tại. Nếu cần đưa quan hệ này vào graph, phải duyệt thiết kế sửa chung: biểu diễn channel smtp và trạng thái kiểu gọi chưa biết, quy tắc khóa/so/chiếu giữ transport không giả HTTP/RPC. Phạm vi dự kiến: src/do_thi_tinh/build.py, hợp đồng/README, oracle/fixtures/check và manifest/LOG của một lượt shared được duyệt; rà compare.py nếu khóa transport hiện hành không đủ. Cần quyết rõ type/semantics trước sửa, không mở lại hay ghi T036 chỉ vì counterexample. Ảnh hưởng: pin mới cho T037–039, kiểm tương thích và tái lập ba nhánh; chưa dự toán đủ lượt vì chưa được duyệt thiết kế. Không đề nghị chỉ thêm enum cho chạy qua.

2. **Lineage:** xin chủ nguồn qua Minh cung cấp app commit/image digest/build metadata, agent revision/config, deployment/namespace/env/time scope và workload/capture schema. Không có URL/revision/byte cụ thể của tài liệu chưa tồn tại trong quyền nên không đề nghị tải mù. Kiểm metadata nhỏ dự kiến vài phút sau nhận; tổng byte/RAM/chờ người chưa biết. Đây là phần thiếu để phân xử runtime, không phải thêm graph/RCA experiment. Không dùng graph giống nhau để chọn version.

3. **Coverage:** 27 mục OPEN được liệt kê riêng từng file ở bao-phu-nguon.json#/open_details. Cần owner xác nhận/sanitized nội dung 24 ảnh và PDF lịch sử trước xem để giữ giới hạn không đọc telemetry; swap cần version/loader/package member manifest của Helm, archive cần activation/đối chiếu library profile/image. Ước tính từng mục là dự toán, chưa đo; không đề nghị bỏ nghĩa vụ vì file ngoài parser. Đã đọc an toàn Java/POM nhúng; nếu cần đọc phần còn lại phải nêu đúng member/input và giữ guard raw telemetry. Nguồn library ngoài repo/wiki/workload/images chưa có package được duyệt; đề nghị sau khi biết đúng revision/từng nhóm/byte, không tự tải.

4. **Ghi quyết định chính thức:** có thể đề nghị Minh duyệt thêm vào docs/DECISIONS.md đúng lời: “không tách, làm trong 1 phiên , duyệt gói tải”, kèm tham chiếu LOG T038 và danh sách tải đã trình. Hiện chỉ ghi nguyên lời trong LOG theo quyền task, chưa sửa DECISIONS/WHY. Việc duyệt tải không xác minh phiên bản sinh dataset, không nghiệm thu task hoặc mở test.

Không có quyền cho lượt chạy dài hơn một giờ, tải thêm, EC2, test, baseline, P6/T040, commit/push hoặc gửi chat. Những gì vẫn làm được trong quyền đã được kiểm trước bàn giao; phần còn thiếu có input/owner/câu hỏi phụ thuộc thay cho kết luận ép kín.
''')
    summaries=[]
    for path in sorted((OUT/'runs').glob('doi-chieu-*/summary.json')):
        obj=load(path); summaries.append(dict(run=obj['run'], graphs=obj['graph_count'],elapsed_seconds=obj['elapsed_progress_seconds'],
            peak_working_set_bytes=obj['peak_working_set_bytes'], ram_valid='pilot-002' not in obj['run'],
            compressed_output_bytes=obj['compressed_output_bytes']))
    save(OUT/'kha-thi.json',dict(task='T-038',status='executed in same approved session; full comparisons done, source/SMTP/lineage partial',
        download={k:acquired[k] for k in ['file_count','unique_blobs','payload_received_bytes','metadata_received_bytes','materialized_blob_bytes','elapsed_acquisition_seconds','http_headers_tls_bytes','metadata_and_allocation_overhead_bytes']},
        full_and_pilot_runs=summaries,
        measured_known_machine_elapsed_seconds=sum(x['elapsed_seconds'] for x in summaries)+acquired['elapsed_acquisition_seconds'],
        elapsed_sum_condition='Sum of recorded acquisition/comparison durations only; excludes extraction, coverage, report, checks and unmeasured failed invocations. Not total labor/wait/isolated benchmark.',
        total_labor_hours=None,total_labor_reason='No continuous labor timer; 4–6h historical proposal is not a measurement.',
        failed_runs_preserved=True, all_runs_storage='final manifest records every retained file/byte, including failed/repeated runs, source and intermediates; filesystem allocation and future reviews unknown',
        Q40=dict(limit_seconds=10800,scope='per RCA method/dataset; comparisons are not an RCA method',full_comparison_seconds=[x['elapsed_seconds'] for x in summaries if x['run'].startswith('doi-chieu-dev')],limit_exceeded=False),
        projected_future_cost='No new compute/download planned without specific missing-input proposal; no >1h single run performed.',
        disk_and_checks_evidence='runs/ket-phien-002/final-verification.json and manifest.json',unknown=['headers/TLS','allocation blocks/NTFS metadata','whole labor/wait','unmeasured extraction/check elapsed/peak','future source package byte sizes']))
    # Neutral handoff, verbatim template blocks except prescribed placeholders.
    import re
    template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')
    def block(heading):
        return re.search(re.escape(heading)+r'\s+```text\n(.*?)\n```',template,re.S)[1]
    common=block('## Prompt chung')
    replacements={
        '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>':'T-038, tasks/T-038-p5b-trainticket/SPEC.md và LOG.md',
        '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>':'soát kết quả',
        '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>':'P5, chuẩn bị G3',
        '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>':'Codex người làm; Claude người phản biện kết quả',
        '<danh sách đường dẫn và git diff từ commit gốc nếu có>':'tasks/T-038-p5b-trainticket/SPEC.md, LOG.md; docs/MRP.md và các nguồn trực tiếp chi phối được SPEC liệt kê',
        '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>':'chưa có bản phản biện kết quả T-038',
        '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>':'results/T-038/manifest.json, ban-ghi.json, nguon.json, bao-phu-nguon.md/json, mapping.json, do-thi/, doi-chieu/index.json, phan-tich-chenh-lech.md/json, kiem-dung-dan.md, ban-giao.md; snapshot T-036 theo SPEC; Windows Python 3.12, py -3 -X utf8 -B; scripts/runs trong results/T-038/',
        '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>':'chỉ đọc và trả lời trong chat; Minh chưa cấp quyền ghi REVIEW cho lượt này'}
    for old,new in replacements.items():
        assert common.count(old)==1
        common=common.replace(old,new)
    prompt=common+'\n\n'+block('### Soát kết quả')+'\n\n'+block('### G3 — Khóa thiết kế trước khi mở test')+'\n'
    (OUT/'prompt-claude.txt').write_text(prompt,encoding='utf-8')
    save(OUT/'runs/trien-khai-001/report-inputs.json',dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        source_coverage_counts=counts,report_comparison_run=summary['run'],source_model_run='lap-ban-ghi-005',
        raw_or_contaminated_content_used=False,script='results/T-038/finish_reports.py'))
    print(canon(dict(status='reports written',coverage_counts=counts,comparison_run=summary['run'],prompt_chars=len(prompt))))


if __name__=='__main__':
    main()
