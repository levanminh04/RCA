"""Tích hợp phần bổ sung đã kiểm; không đổi model/graph/pin chung."""
from collections import Counter
import datetime as dt
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'results/T-038'
RUN=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,t:p.write_text(t.strip()+'\n',encoding='utf-8')


def main():
    coverage=load(RUN/'before-bao-phu-nguon.json')
    extra=load(RUN/'coverage/findings.json')
    assert extra['all_checks_ok'] and len(extra['records'])==27
    old_open={x['path'] for x in coverage['files'] if x['status']=='open'}
    assert {x['path'] for x in extra['records']}==old_open
    records={x['path']:x for x in extra['records']}
    for r in coverage['files']:
        if r['path'] in records:
            f=records[r['path']]
            reason=f.get('reason',f.get('visual_observation'))
            assert reason, f['path']
            r.update(status=f['proposed_status'],read_depth=f['read_depth'],reason=reason,
                inventory_impact=f.get('inventory_relation_effect'),refinement=f)
    counts=dict(Counter(r['status'] for r in coverage['files']))
    assert counts=={'read':2783,'excluded':43,'open':1}
    coverage.update(statuses=counts,
        read_depths=dict(Counter(r['read_depth'] for r in coverage['files'])),
        groups={g:dict(Counter(r['status'] for r in coverage['files'] if r['group']==g)) for g in sorted({r['group'] for r in coverage['files']})},
        open_details=[r for r in extra['records'] if r['proposed_status']=='open'],
        latest_refinement='runs/hoan-tat-trong-quyen-001/coverage/findings.json',
        old_open_roles_partitioned=True,remaining_content_open_blocks_declared_current_inventory=False,
        semantic_source_inventory_complete=False,content_scope_complete=False,
        current_module_build_inventory_checked=True,
        completeness_caution='All snapshot paths have evidence-based roles/status. Current declared modules/build/config have been surveyed. This is not proof of arbitrary runtime behavior, transitive/image activation or all historical PDF content.',
        lineage_resolution='runs/hoan-tat-trong-quyen-001/lineage-resolution.json')
    save(OUT/'bao-phu-nguon.json',coverage)
    write(OUT/'bao-phu-nguon.md', '''# Nguồn Train Ticket và độ đủ — bản bổ sung hiện hành

Đã xử lý hết phần khảo sát trong quyền. Snapshot nguồn có 3.921 mục: 1.094 thư mục và 2.827 blob-path; 2.712 Git blob duy nhất. Từng path được kiểm byte/hash; 8 symlink giữ literal, không tạo link. Revision/tree/hash ở `runs/tai-nguon-001/manifest.json`, không dùng HEAD. “Đủ cây” khác “đọc mọi nội dung” và khác “xác minh runtime”.

Bảng hiện hành: **2.783 read, 43 excluded, 1 open**, tổng 2.827 (`bao-phu-nguon.json#/statuses`). Read ghi độ sâu riêng, gồm đọc toàn văn/lexical, đọc cấu trúc và đọc hình; không hứa đã phân xử mọi hành vi. Excluded có cả nhóm cách ly do giới hạn raw telemetry; không đồng nghĩa mọi file đã chứng minh vô can bằng nội dung. Semantic/content completeness và runtime lineage vẫn false.

Đã rà lại toàn 27 mục OPEN cũ, không dùng “chưa phân loại ảnh” làm lý do tự dừng. 24 ảnh được đối chiếu README/HTML/code và xem an toàn: UI đặt vé/admin, Selenium config, browser icon, wireframe, splash/theme và avatar fixture. Ảnh không tạo cạnh service chỉ từ nhãn giao diện. Archive instrumentation được đọc Java/POM/manifest/spring.factories và class/container metadata an toàn, không chạy bytecode. Swap MySQL chart được loại có điều kiện bằng quy tắc loader chính thức ở hai baseline Helm do README nêu; không có .helmignore không làm dotfile tự thành template. Bằng chứng từng mục, 134 đầu vào được kiểm và 43/43 checks ở `runs/hoan-tat-trong-quyen-001/coverage/findings.json`; đọc diễn giải ở `coverage/report.md` trong cùng run.

Chỉ body PDF `old-docs/Json2Shiviz/document/ReadMe.pdf` chưa mở: metadata sáu trang/mười ảnh chưa tách được hướng dẫn khỏi mẫu log đang bị cấm. Code/build/regular-expression cạnh tài liệu đã xác định vai trò converter offline lịch sử. Root POM 42 module, 43 POM hiện hành và build references không đưa converter này vào declared-current application build. Vì vậy PDF không chặn phân hoạch inventory module hiện hành. Phần thiếu chỉ hạn chế kết luận phụ thuộc nội dung/schema/naming lịch sử; nếu cần, phải có vùng/trang an toàn hoặc bản đã bỏ mẫu từ chủ nguồn, hay quyền xem mẫu tương ứng. Không thiếu công cụ đọc PDF và không cần tải/build mới để phân loại vai trò này.

Nguồn hiện hành đã lần Maven module → config tên/URL → controller/service/repository/client/worker, cùng Python/Go/Node/UI/nginx, build/template/deployment. Có 617 khai báo resource K8s theo profile trong facts; không gộp thành một deployment đã chạy. V1 quickstart dùng MySQL/Nacos/RabbitMQ; tracing Skywalking/Elasticsearch và monitoring Prometheus/Grafana là cấu hình có điều kiện. Nguồn Mongo/Jaeger lịch sử giữ vai trò lịch sử. Hạn chế template/generator/dynamic/env/external dependencies được nêu đúng phần trong facts và phân tích; chưa render hoặc chạy application bằng quyền này.

Archive có hai artifact monitoring và 161 Java source an toàn đã xét. Namespace/source khác bản loose lịch sử; không lấy sự hiện diện của JAR làm agent đã active. Current POM/profile/build references không khai trực tiếp thư viện đó; resolved transitive dependencies, image build và actual agent config chưa có. Phần này hạn chế runtime naming/lineage; không tự thêm Zipkin endpoint vào graph hiện hành từ một library default lịch sử.

Đã tra thêm metadata primary: repo benchmark ở pin đang dùng và hai branch công bố ASE24/WWW25, metadata catalogue Zenodo/Figshare và các locator paper/README đã lưu. Có 11 request API, nhận 125.582 byte metadata; hai URL commit dùng tên branch trả 404 được giữ, followup resolve SHA qua branch list thành công. Không lấy blob code/image/telemetry từ các API này. Không tìm được liên kết app commit→image→agent→deployment tại các nguồn/locator đã kiểm; việc tìm có giới hạn không chứng minh nó không tồn tại trên internet. Receipt, SHA và phạm vi âm tính ở `runs/hoan-tat-trong-quyen-001/lineage-resolution.json`. Thiếu lineage chỉ giới hạn so sánh tham khảo theo SPEC, không là lý do dừng các bước độc lập.

Metadata commit release nguồn đã duyệt ghi việc xóa ticketinfo, tách food-map, chuyển MySQL và đổi cấu hình Skywalking; con trỏ ở `release-refactor-metadata.json` trong run bổ sung. Đây là chứng cứ về reconstruction của nguồn tham khảo, không phải alias hay phiên bản RE2 được xác minh. Không chọn revision theo tỷ lệ khớp graph.

Sự cố lịch sử giữ nguyên: nhánh hỗ trợ từng đọc nhầm 15 mẫu telemetry công khai, XML debugging workbook và ảnh Jaeger; đã báo, giữ bản lỗi và cách ly khỏi facts/model/mapping/kết luận. Root không dùng index lỗi. Không mở RE2 raw/test/heldout/data khóa. Finalizer chỉ hash nguồn và index cách ly, không parse lại. Chi tiết ở `runs/trien-khai-001/coverage/incident.json`; việc làm sạch không hoàn tác lần đã đọc.

Kết luận hiện hành: toàn path đã được phân hoạch vai trò; inventory module/build khai báo hiện hành được khảo sát, song không nhận inventory ngữ nghĩa/runtime đầy đủ. Kết quả mô tả có điều kiện vẫn dùng được đúng phạm vi. SMTP là phần biểu diễn chung đang chờ duyệt gói sửa cụ thể; không bỏ nó khỏi nghĩa vụ P5b.
''')
    analysis=load(RUN/'before-phan-tich-chenh-lech.json')
    analysis.update(source_flag_resolution='runs/hoan-tat-trong-quyen-001/source-flag-resolution.json',
        source_flag_statement='151 overlapping tracking records; 9 empty-initializer flags closed by manual if/else control-flow evidence, 142 remaining rows are source conditions/candidates or examined external/literal discrepancies, not 142 undone tasks.',
        release_refactor_evidence='runs/hoan-tat-trong-quyen-001/release-refactor-metadata.json',
        latest_lineage_metadata='runs/hoan-tat-trong-quyen-001/lineage-resolution.json',
        numerical_comparison_unchanged=True)
    save(OUT/'phan-tich-chenh-lech.json',analysis)
    text=(RUN/'before-phan-tich-chenh-lech.md').read_text(encoding='utf-8')
    text=text.replace('Archive/libraries/config chưa render và nguồn OPEN có thể bổ sung quan hệ khác; không gọi coverage đầy đủ.',
        'Archive/libraries/config chưa render còn giới hạn về activation/runtime; rà bổ sung đã phân loại toàn bộ27 mục cũ, chỉ body PDF converter lịch sử chưa mở. PDF không chặn declared-current module inventory, nhưng không nhận toàn nội dung/semantics đã đầy đủ.')
    text+='''

## Bổ sung sau yêu cầu làm hết phần trong quyền

Chín cờ `http_target_unresolved_alternative` trước đây không còn là đích chưa biết của source. Đã đọc từng đoạn: URL khởi tạo rỗng, sau đó cả hai nhánh if/else gán URL trước call. Nếu condition/assignment ném exception thì không tới call; nếu tới call bình thường thì không còn giá trị rỗng. Đây là overapproximation của extractor lexical, không phải thiếu telemetry. Oracle đọc tay, source hash/line và chín chuỗi đầy đủ ở `runs/hoan-tat-trong-quyen-001/{manual-branch-oracle.json,source-flag-resolution.json}`. Không sửa source hay tự chứng minh nhánh đã chạy. Các alternative không rỗng đã có trong model005, nên đóng cờ không đổi graph/mapping/kết quả.

Đã phân loại toàn151 tracking row:9 closed initializer,71 candidate target operation,67 branch/value conditions và4 external/literal discrepancies đã đọc nguồn. Chúng chồng lấn, không là151 ca lỗi hay tỷ lệ nguyên nhân. Candidate dynamic URL giữ nguyên vì source pattern không chứng minh giá trị URL/routing runtime; bốn no-handler đã có external implementation thiếu hoặc source method/path bất nhất. Giữ chúng có điều kiện là kết quả khảo sát, không tự biến thành nghĩa vụ chạy runtime không được giao.

Metadata reconstruction nguồn đã duyệt ghi xóa ticketinfo, tách food-map, migration MySQL và Skywalking (`runs/hoan-tat-trong-quyen-001/release-refactor-metadata.json`). Điều này củng cố khác biệt source/profile đã quan sát; chưa nối được nguồn thu RE2 nên không dùng làm alias hoặc nguyên nhân xác nhận cho năm cặp riêng trace. Tra metadata tiếp có phạm vi/receipt ở lineage-resolution.json; kết quả so vẫn conditional. Không cần chạy lại1069 graph vì mọi input model/graph/mapping và numerical output giữ nguyên hash.
'''
    write(OUT/'phan-tich-chenh-lech.md',text)
    correctness=(RUN/'before-kiem-dung-dan.md').read_text(encoding='utf-8')
    correctness=correctness.replace('chín empty initialization OPEN','chín empty initialization đã được đóng bằng bằng chứng if/else ở lượt bổ sung')
    correctness+='''

Kiểm bổ sung hiện hành ở `runs/hoan-tat-trong-quyen-001/`: coverage43/43 trên27 mục cũ; source-flag resolution đóng9initializer và phân loại đủ151 tracking row; metadata receipts giữ cả404 và followup thành công. Model005/graph/mapping và1069 output không đổi, dùng lại kiểm hợp lệ theo hash. Bản thử SMTP26/26 chỉ chạy code copy ở `smtp/experimental_copy/`, chưa là hợp đồng/pin đang dùng. Oracle SMTP thử riêng có chronology trước candidate code. Kiểm cuối lượt bổ sung và manifest sẽ ghi riêng, không ghi đè bản kiểm28/28 trước. Source semantics/content/runtime completeness vẫn không được nâng thành true.
'''
    write(OUT/'kiem-dung-dan.md',correctness)
    package=RUN/'smtp/plan.json'
    assert package.exists(), 'Wait for complete concrete SMTP package before handoff'
    smtp=load(package)
    preview=load(RUN/'smtp/kiem-preview-001/checks.json')
    assert preview['all_ok'] and len(preview['checks'])==26
    write(OUT/'goi-sua-SMTP.md', '''# Xin duyệt gói sửa SMTP chung

Gói cụ thể đã chuẩn bị, chưa áp dụng: [thiết kế, danh sách file, ảnh hưởng và chi phí](runs/hoan-tat-trong-quyen-001/smtp/plan.md); [danh sách máy đọc](runs/hoan-tat-trong-quyen-001/smtp/plan.json); [patch chính xác](runs/hoan-tat-trong-quyen-001/smtp/proposed-shared-code.patch); [oracle trước code](runs/hoan-tat-trong-quyen-001/smtp/oracle-before-code.json); [26 kiểm bản thử](runs/hoan-tat-trong-quyen-001/smtp/kiem-preview-001/checks.json).

Đề nghị thêm channel SMTP cho chặng sender→mail-server, không dựng broker/người nhận và không coi accepted send là delivered. Giữ type theo bằng chứng riêng; Train Ticket mới có interface/config nên dùng gọi-chưa-phân-kiểu. Comparator tách miền SMTP để không nhận khớp với HTTP/RPC hoặc trace thiếu protocol. Host/port/TLS literal giữ theo nguồn/context; phép so chưa xác nhận authority/TLS/delivery. Các lựa chọn đối lập và điều kiện thất bại được nêu trong plan; đây là đề xuất kỹ thuật cần Minh duyệt, không phải quyết định đã có.

Patch dùng chung sửa build.py/compare.py và README, bổ sung hồ sơ hợp đồng/kiểm/pin trong run T036 mới, phụ lục SPEC/LOG T036, WHY/DECISIONS và chuyển cùng pin ở ba SPEC/LOG T037–039. Tiếp nhận ba nhánh theo output thật hiện có; T038 replay đủ1069 graph, T037/T039 không được nhận smoke là hoàn thành task. Giữ các root/run/hợp đồng lịch sử và graph T035. Bảng trong plan ghi đúng từng file/phạm vi, đoạn cũ→mới, runner nhận pin mới tường minh và quy tắc lưu input/output mới; không dùng HEAD hay fork nghĩa riêng.

Bản thử copy đạt26/26, gồm hồi quy build legacy; không thay việc chạy bộ kiểm chung và tiếp nhận pin sau khi duyệt. Dự toán CANDIDATE:31 phút máy,550MB output mới có dự trù một lần sửa/chạy lạiTT; RAM dự trù0,5GiB choTT, shared peak chưa đo. Không tải source/image hay bậtEC2. Dự toán không là phép đo pin mới và không bao giờ là quyền hoàn thành toànT037/T039. Nếu vượt phạm vi/chi phí phải trình lại.

Minh cần duyệt đúng gói/filelist và quyền chuyển pin có điều kiện các kiểm đạt. Nguồn yêu cầu quyền riêng: lời giao T038 và SPEC cấm ghi src/, T036 hoặc task khác; AGENTS Luật0 yêu cầu Minh duyệt đúng đề xuất. Vì vậy quyền “làm tiếp T038” chỉ đủ chuẩn bị bản này, chưa đủ áp dụng shared patch.
''')
    matrix=dict(task='T-038',intent='EXECUTE',authorized_execution_complete=True,full_task_accepted=False,
        shared_SMTP_fix_applied=False,current_pin_unchanged=True,
        source_counts=counts,source_content_open_blocks_declared_current_inventory=False,
        research_questions_closed=False,numerical_comparison_reused_after_hash_verification=True,
        current_model='runs/lap-ban-ghi-005',current_comparison='runs/doi-chieu-dev-002',
        criteria=[
          dict(id=1,status='MET_WITH_EXPLICIT_SCOPE_LIMITS',evidence=['bao-phu-nguon.json','runs/hoan-tat-trong-quyen-001/coverage/findings.json','runs/hoan-tat-trong-quyen-001/lineage-resolution.json'],limits='Content PDF historical and runtime/semantic completeness not asserted; conditional source comparison is permitted.'),
          dict(id=2,status='AWAITING_APPROVAL_SHARED_SMTP',evidence=['fixtures/smtp-counterexample.json','goi-sua-SMTP.md'],limits='Current graph lacks SMTP relation; package tested in experimental copy only. No complete relation representation claim.'),
          dict(id=3,status='MET_1069_ALL_DEV_GRAPHS',evidence=['doi-chieu/index.json','runs/doi-chieu-dev-002/self-checks.json'],limits='Typed/operation T empty means ineligible mapping/type, not no traffic.'),
          dict(id=4,status='MET_DESCRIPTIVE_AND_SOURCE_MECHANISMS',evidence=['phan-tich-chenh-lech.md','runs/hoan-tat-trong-quyen-001/source-flag-resolution.json'],limits='Actual runtime mismatch cause remains unresolved without build/instrumentation evidence; not a P6 choice.'),
          dict(id=5,status='HANDOFF_AND_APPROVAL_PACKAGE_READY',evidence=['ban-giao.md','goi-sua-SMTP.md','prompt-claude.txt'],limits='Minh chooses shared change/review/acceptance; no automatic closure or test access.' )],
        next_authorization_needed=dict(action='Apply exact shared SMTP package and adopt common new pin',proposal='goi-sua-SMTP.md'),
        other_open_limits=['historical PDF body under sample guard','runtime image/deployment/instrumentation lineage','dynamic runtime activation/URL values'],
        no_undone_authorized_analysis_left=True)
    save(OUT/'hoan-tat-trong-quyen.json',matrix)
    write(OUT/'hoan-tat-trong-quyen.md', '''# Mức hoàn tất T-038 sau lượt làm tiếp

Đã hoàn tất phần triển khai và tự kiểm đang được phép; không còn dừng ở nhãn OPEN chung. Chưa nhận toàn task đủ biểu diễn/nghiệm thu: **phần áp dụng sửa SMTP chung còn chờ Minh duyệt gói cụ thể**. Bản ghi, graph và phép so hiện hành vẫn giữ pin T-036 v1 đã giao.

| Tiêu chí SPEC | Kết quả và bằng chứng |
|---|---|
| Snapshot/coverage/lineage | Đủ cây/hash; 2.783 read, 43 excluded, 1 body PDF open. Đã rà hết 27 mục cũ. PDF offline không chặn module inventory hiện hành. Không nhận semantic/runtime completeness. Metadata đã truy tiếp và kết luận có điều kiện. |
| Quan hệ/địa chỉ/biểu diễn | Nguồn và hai graph đã kiểm; 9 cờ initializer đã đóng bằng source. SMTP có counterexample, patch preview và 26 checks; chưa áp dụng shared nên chưa nhận đủ mọi relation. |
| Toàn graph/cửa sổ dev | Đủ 1.069, cùng pin/mapping/input; tập/members/exclusions/mẫu số/interval/lặp/đảo hợp lệ. Dùng lại output theo hash, không chạy lại khi không cần thiết. |
| Chênh lệch và cơ chế | Có mismatch/match và chuỗi code→record→mapping→key→set; đã phân loại đủ 151 tracking row. Không quy nguyên nhân runtime hoặc chọn P6 từ absence nguồn. |
| Bàn giao | Có đầu vào T-040/P6/P9, giới hạn nguồn riêng và gói SMTP/filelist/chi phí để Minh duyệt; prompt chuẩn để chuyển thủ công. |

Các giới hạn về runtime lineage, input dynamic và nội dung PDF không biến thành yêu cầu mở raw hoặc dừng phép so tham khảo đã được SPEC cho phép. Chúng chỉ giới hạn kết luận tương ứng. Gói SMTP là thay đổi ngoài quyền T-038; không thể tự áp dụng bằng cách đổi enum riêng hoặc bỏ quan hệ đó cho task có vẻ xong.

Xem chi tiết từng tiêu chí và con trỏ tại `hoan-tat-trong-quyen.json`. Bước cần Minh quyết hiện tại là `goi-sua-SMTP.md`; không cần giao lại phần T-038 đã được làm.
''')
    write(OUT/'ban-giao.md', '''# Bàn giao T-038 — phần trong quyền đã hoàn tất

Đã xử lý hết phần đang có quyền: rà 27 mục nguồn cũ, đọc source đóng 9 cờ OPEN sai, truy thêm metadata lineage và chuẩn bị gói sửa SMTP cụ thể. **Chưa đủ nghiệm thu toàn T-038 vì SMTP trong hợp đồng chung chưa được duyệt/áp dụng.** Xem `hoan-tat-trong-quyen.md/json` để phân biệt tiêu chí đạt, phần chờ quyền và giới hạn kết luận.

Điểm vào hiện hành: `bao-phu-nguon.md/json`, `ban-ghi.json`, `nguon.json`, `inventory-index.json`, `mapping.json`, `do-thi/`, `doi-chieu/index.json`, `phan-tich-chenh-lech.md/json`, `kiem-dung-dan.md`, `kha-thi.json`, `hoan-tat-trong-quyen.md/json`, `goi-sua-SMTP.md`, `manifest.json`. Model005 và 1.069 kết quả ở doi-chieu-dev-002 giữ nguyên; bổ sung mới ở runs/hoan-tat-trong-quyen-001. Giữ mọi bản trước; không chạy lại output hợp lệ khi input không đổi.

| Bên nhận | Đầu vào và điều kiện |
|---|---|
| T-040 | Nguồn/inventory/operations và relation có provenance, toàn graph/cửa sổ và từng tập/members/exclusions. Source comparison conditional; 9 initializer flag là overapproximation của extractor đã kiểm, không phải mất telemetry. Không cộng các cờ chồng lấn thành tỷ lệ nguyên nhân. |
| P6/RQ3/RQ5 | Địa chỉ hai mức, source relation và signal declarations, nguồn thêm ngoài trace. Graph mới dùng tính khóa/chiếu/tập; chưa có điểm RCA, bằng chứng lợi ích hoặc thiết kế P6 đã chọn. |
| P9 FlashTicket | Owner/component ID, endpoint method/route/client callsite, kind/protocol; DB logical/physical riêng; broker namespace/exchange/routing/queue; log trace/span correlation và metric resource/scrape target. SMTP cần tách configured/observed TLS, attempt và outcome của chặng gửi; không nhận accepted là recipient delivery. Đây là yêu cầu quan sát, không chứng minh collector sửa lịch sử chưa ghi. |
| Chủ dữ liệu qua Minh | App commit/image build digest, actual agent/config, deployment/namespace/env/time và workload/capture schema nếu muốn phân xử runtime. Metadata primary đã kiểm không cung cấp nối chuỗi này; không dùng graph giống nhau để chọn version. |

Coverage hiện là 2.783 read, 43 excluded, 1 PDF body open. PDF là manual converter offline ngoài current declared build, nên không chặn module inventory. Không tuyên bố đọc body hoặc semantic/runtime đầy đủ. Archive đã rõ source/entrypoints; actual activation vẫn cần manifest/dependencies/image. Các giới hạn giữ đúng phạm vi kết luận, không thay cho việc làm còn có thể thực hiện.

SMTP: `goi-sua-SMTP.md` dẫn patch, code copy, oracle, 26 checks, filelist, ảnh hưởng và chi phí. Chưa sửa src/shared, T-036 hay SPEC khác, chưa chuyển pin. Minh duyệt gói thì mới áp dụng, kiểm chung và tiếp nhận pin ba nhánh. Dự toán 31 phút máy/550 MB output là CANDIDATE, không là số đã đo. Không nghiệm thu T-037/T-039 qua kiểm tiếp nhận.

Sự cố telemetry mẫu lịch sử đã được báo và giữ trong incident/LOG; index lỗi cách ly, không dùng cho facts/model/mapping/kết luận. Không mở raw RE2/test/heldout/data khóa. Kiểm cuối chỉ hash nhóm đó. Không thể hoàn tác việc đã đọc trong lượt cũ.

Bước tiếp: Minh xem gói SMTP để duyệt chính xác phạm vi chung. Prompt soát kết quả ở prompt-claude.txt và LOG; prompt gói SMTP ở prompt-claude-smtp.txt, đều theo nguyên mẫu để Minh chuyển thủ công. Chưa có quyền ghi REVIEW thì Claude chỉ đọc/trả lời chat. Không tự gửi chat, nghiệm thu, đóng G3, commit/push. Commit đề nghị sau Minh duyệt: `T-038: hoàn tất khảo sát trong quyền và trình gói SMTP chung`.
''')
    write(OUT/'de-nghi-tiep-theo.md', '''# Việc cần Minh quyết sau khi hoàn tất phần trong quyền

**Đề nghị hành động hiện tại:** duyệt hoặc bác gói SMTP tại `goi-sua-SMTP.md`. Gói đã có patch/sourcecopy/oracle/checks/filelist và ảnhhưởng ba nhánh; chưa áp dụng. Không còn đề nghị Minh duyệt lại việc khảo sátT038 hoặc phân loại cả27tệpcũ.

Các phần khác là giới hạn cho kết luận mạnh hơn: nếu muốn xác nhận runtime RE2 thì cần application/image/instrumentation/deployment identity từ chủ nguồn; nếu muốn dùng body PDF converter lịch sử thì cần vùngtrangan toàn/bản bỏmẫu hoặc quyềnxemmẫu cụthể. Chúng không ngăn phépso thamkhảo và phânhoạchinventory currentdeclaredbuild đã được làm.

Quyếtđịnh chínhthức cần lưu trong DECISIONS vẫn phải được Minhduyệt phạmvi riêng; draft của góiSMTP nêu đúng nội dung chờ duyệt, không ghi đề xuất thànhquyếtđịnh. Không tựsửa WHY/DECISIONS/SPEC/src bằng quyềnT038; không commit/push/test/EC2.
''')
    history=(RUN/'before-LICH-SU.md').read_text(encoding='utf-8')
    history+='''

Lượt hiện hành bổ sung là `runs/hoan-tat-trong-quyen-001/`: before-* giữ các rootreport cũ, coveragefindings thay phân hoạch27OPEN thành1bodyPDFopen; sourceflagresolution đóng9initializer vàgiữ141? Không: tổng trackingrow gốc151,9closed và142rowcóđiềukiện/đãgiảithích. XemJSON làmnguồn số. Model005 vàdoi-chieu-dev-002 vẫncurrent, SMTPexperimental_copy chỉ đểduyệt khôngactive. Không chạy finish_reports.py cũ đểghiđè rootreportbổsung; nó táitạo báo cáo ởmốc27OPENtrước lượt này. Finalmanifest hiệnhành ghi current_completion_run vàproposal.
'''
    history=history.replace('vàgiữ141? Không: tổng trackingrow gốc151','; tổng trackingrow gốc151')
    write(OUT/'LICH-SU.md',history)
    cost=load(RUN/'before-kha-thi.json')
    metadata=load(RUN/'lineage-resolution.json')
    cost.update(status='authorized source/comparison work completed; shared SMTP proposal ready, not applied',
        supplemental_metadata=dict(requests=metadata['metadata_request_count'],received_bytes=metadata['metadata_received_bytes'],headers_TLS_unknown=True,web_lookup_bytes_unknown=True,request_receipts='runs/hoan-tat-trong-quyen-001/lineage/requests.json and lineage-branch-followup/requests.json'),
        supplemental_coverage=dict(checks=43,paths_reclassified=27,elapsed_helper_seconds_not_total_labor=extra['summary']['elapsed_seconds']),
        SMTP_preview=dict(checks=26,elapsed_seconds=preview['elapsed_seconds'],RAM_measured=False,active_pin_changed=False),
        proposed_shared_future_cost=dict(candidate_only=True,machine_minutes=31,output_bytes_approx=550000000,TT_RAM_GiB=0.5,network_source_download_bytes=0,scope='shared checks + TT1069 replay with one rerun allowance + existing-output/fixture adoption FT/OB; not full FT/OB completion'),
        all_runs_storage='final manifest including all prior and supplemental source/metadata/history/preview, allocation/headers unknown')
    save(OUT/'kha-thi.json',cost)
    save(RUN/'integration-result.json',dict(ok=True,counts=counts,model_graph_mapping_numerical_changes=False,authorized_work_completed=True,task_acceptance_or_shared_change=False,coverage_findings_sha256=sha(RUN/'coverage/findings.json'),source_flag_resolution_sha256=sha(RUN/'source-flag-resolution.json'),SMTP_plan_sha256=sha(package),created_utc=dt.datetime.now(dt.timezone.utc).isoformat()))
    print(json.dumps(dict(ok=True,counts=counts,model_unchanged=True,SMTP_applied=False),ensure_ascii=False))


if __name__=='__main__':main()
