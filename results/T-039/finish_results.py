"""Render T039 evidence reports, then finalize after LOG/STATE edits.
Only writes T039. No network, shared imports, raw inputs or task status changes.
"""
import sys
sys.dont_write_bytecode=True
import copy
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
B=ROOT/'results/T-039'
FINAL=B/'runs/ket-thuc-001'

def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def path(p):return Path(p).relative_to(ROOT).as_posix()
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def md(p,x):Path(p).write_text(x.strip()+'\n',encoding='utf-8')

def reports():
    FINAL.mkdir(exist_ok=False)
    for name in ['nguon.json','bao-phu-nguon.json','ban-giao.md','kiem-dung-dan.md','de-nghi-ghi-quyet-dinh.md']:
        p=FINAL/'before'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((B/name).read_bytes())
    for p in [ROOT/'docs/STATE.md',ROOT/'tasks/T-039-p5b-online-boutique/LOG.md']:
        (FINAL/('before-'+p.name)).write_bytes(p.read_bytes())
    summary=read(B/'doi-chieu/tong-hop.json');doc=read(B/'ban-ghi.json');mapping=read(B/'mapping.json')
    reg=read(B/'nguon.json');reg['status']='STATIC_REFERENCE_IMPLEMENTED_WITH_OPEN_DEPLOYMENT_AND_LIBRARY_LINEAGE'
    reg['execution']=dict(pin='results/T-036/runs/kiem-r1-after-002/code/',current_shared_used=False,user_override='LOG T039 Phiên4; dùng snapshot cũ đã ghim, không chờ shared SMTP',run='runs/thuc-thi-snapshot-004',conditional_reference=True)
    reg['lineage_audit']='runs/doc-nguon-002/lineage.md'
    reg['interpretation']='Source identity verified, dataset deployment link OPEN. Registry metadata correction does not change T036.'
    write(B/'nguon.json',reg)
    cov=read(B/'bao-phu-nguon.json')
    cov['completeness']=dict(tree_partition_complete=True,all_runtime_or_external_sources_complete=False,semantic_coverage_fully_verified=False,builder_and_comparison_validated=True,claim='Phân hoạch đủ toàn snapshot; đọc/scan/excluded được tách. Inventory tham chiếu nguồn đã khảo sát, chưa xác nhận đầy đủ deployment/library runtime.',remaining=['exact deployed image/source/instrumentation/collector lineage','external library span naming','unread raw logs excluded by approval; not needed as static source','see source audit for read depth per group'])
    cov['final_audit']=dict(source='runs/doc-nguon-002/backend-source-audit.json',lineage='runs/doc-nguon-002/lineage.md',report='runs/doc-nguon-002/bao-phu-lineage.md',corrections='runs/thuc-thi-snapshot-004/merge-audit.json',inventory_independent_of_observed_nodes=True)
    write(B/'bao-phu-nguon.json',cov)
    n=summary['record_counts'];m=summary['mapping_counts'];cost=read(B/'runs/thuc-thi-snapshot-004/cost.json')
    tables=[]
    for level in ['entity','operation']:
        for window in ['full','N','A']:
            rows=[r for r in summary['rows'] if r['level']==level and r['window']==window]
            counts=Counter((r['views']['endpoints']['numerator'],r['views']['endpoints']['static_denominator'],r['views']['endpoints']['trace_denominator']) for r in rows)
            for (num,sd,td),count in sorted(counts.items()):tables.append(f'| {level} | {window} | {count} | {num}/{sd} | {num}/{td} |')
    md(B/'bao-phu-nguon.md',f'''# Bao phủ nguồn T-039

Đã kiểm cây snapshot ứng dụng, không lấy tập service có trace làm inventory. Toàn cây có {cov['entry_count']} entry, gồm {cov['blob_count']} blob và 55 tree; phân hoạch từng path nằm ở `bao-phu-nguon.json#/rows`, số theo trạng thái ở `#/counts`. Snapshot/pin/hash nằm trong registry và manifest.

215 blob ứng dụng đã tải; bốn `log.csv` thô bị loại đúng danh sách Minh duyệt. Bốn file ấy là dữ liệu vận hành, không dùng làm nguồn tĩnh; Dockerfile có COPY chúng nên chưa nhận tái lập build image. Cùng nguồn Nezha bổ sung và metadata, acquisition giữ 229 file, payload 37.524.834 byte (`runs/thu-nguon-001/acquisition.json`). Không mở log, test/heldout hoặc giá trị Node/Weight.

Đã xét source/config/deployment, build/template, proto/mã sinh, stash/test source, dependency/JAR manifest, tài sản trình duyệt và hình kiến trúc. `read`, `scan`, `hash` và `excluded` có nghĩa khác nhau. Chiều sâu của từng nhóm, nguồn ngoài và hệ quả ở `runs/doc-nguon-002/bao-phu-lineage.md`, `backend-source-audit.json`, `parts/*-coverage.json`. Không coi scan đủ thư viện là đã xác minh runtime. Không thấy LFS pointer/gitlink trong snapshot đã định danh.

Kết quả tham chiếu có {n['entities']} entity, {n['operations']} operation, {n['relations']} relation, {n['resource_bindings']} binding logic–instance và {n['signals']} khai báo địa chỉ tín hiệu (`doi-chieu/tong-hop.json#/record_counts`). Đây là khai báo nguồn, không phải số luồng telemetry độc lập. Binding trùng Productdb được hợp provenance; metric exporter ở instance không được nhân sang hai DB logic. `fonts.gstatic.com` giữ như resource hint trong inventory; preconnect không được biến thành cạnh HTTP. Exporter variant và browser scope giữ riêng trong context.

Độ đầy đủ inventory deployment vẫn **OPEN**: chưa có source→build→image digest→deployment→dataset, thư viện runtime và collector/export CSV. Nguồn khả dụng đã cho phép dựng/so graph tham chiếu; chưa đủ nhận toàn deployment hoặc quy thiếu cạnh cho telemetry. Phần mục tiêu nguồn đạt một phần, không tự thu hẹp nghĩa inventory để gọi xong. Đầu vào cần bổ sung, owner, chi phí và quyết định phụ thuộc ở `ban-giao.md` và `de-xuat-bo-sung-nguon.md`.

Các lỗi địa chỉ ad/cart, resource hint và thiếu configured exporter edge đã được sửa trong bản ghi hợp nhất, giữ fragments gốc và audit. Source notes cũng giữ README khác code (MySQL/local currency), generated proto khác registered service, email dummy, health/dependency, Node và nguồn phụ. Chưa dùng các khác biệt này làm nguyên nhân dataset.
''')
    md(B/'kiem-dung-dan.md',f'''# Tự kiểm T-039

Lượt chuẩn: `runs/thuc-thi-snapshot-004/verification.json` — PASS. Dùng nguyên snapshot T036 đã ghim; các module thực nạp đều từ thư mục snapshot. Không dùng live `src` có SMTP, không đổi pin/spec hay mã task khác. Quyền ngoại lệ nằm trong LOG Phiên4.

- Oracle literal đã có trước code biến đổi: `fixtures/oracle.json`, bản trước transform tại `runs/trien-khai-001/oracle-before-transform.json`. Kiểm giao/phần riêng hai phía, typed unknown, mẫu số0→null, mapping chưa verified, owner conflict và projection/entity-only. Kết quả thật: `runs/thuc-thi-snapshot-004/oracle-result.json`.
- Đủ {summary['graph_count']} graph theo canonical allowlist T035 và hash manifest, không lấy runs lịch sử hay dựng cửa sổ mới. API chỉ nhận graph/bản ghi/mapping/context; tên ca, root, loại lỗi, đường dẫn điều phối và mốc tiêm không là input phương pháp.
- Tính lại độc lập từng khóa từ cạnh đầu vào, giao/phần riêng, mẫu số/tỷ lệ; kiểm members trỏ đúng original, eligible/excluded phân hoạch đủ và không trùng. Bảo toàn interval, conditional_reference và miền dev-adapter trên tất cả graph.
- Build sau đảo thứ tự bản ghi cho đầu ra bằng nhau; compare sau đảo mapping cho đầu ra bằng nhau; deep-copy đối chiếu xác nhận không đổi đầu vào. Kiểm chiếu là tập con graph entity và báo entity-only trong `projection-check.json`. Phép so endpoints không xác minh HTTP/RPC; typed không được lấp unknown bằng kiến trúc.
- Mỗi nguồn registry được hash lại; graph input được kiểm theo manifest T035, snapshot4file theo code-hashes/T036. Kiểm JSON/provenance/phạm vi/prompt/manifest cuối ở `runs/ket-thuc-001/verification.json`.

Số lần và chi phí: acquisition và các run chuẩn bị giữ nguyên; execution001 bị root ngắt ở quan sát hash task khác trước oracle; execution002 oracle/build đạt nhưng compare entity nhận nhầm mapping operation nên bị từ chối `mapping_target`; execution003 đạt toàn bộ; execution004 sửa hợp binding/candidate provenance và đo lại. Không sửa hợp đồng chung để bỏ lỗi. Những thay đổi này chỉ ở orchestration T039.

Runner đầu ghi output canonical chưa lưu bản riêng theo attempt. Inputs/failures vẫn có; 135 comparison lịch sử được tái dựng và **ghi rõ RECONSTRUCTED_NOT_ORIGINAL_BYTES** tại `runs/khoi-phuc-lich-su-001/receipt.json`, không giả là byte original. Lượt004 có archive byte đầu ra thật trong `runs/thuc-thi-snapshot-004/outputs/`; runner hiện lưu cả per-run outputs cho các lượt sau.

Lượt004 elapsed {cost['elapsed_seconds']:.3f}s, peak working set tiến trình {cost['peak_process_rss_bytes']:,} byte; input graph {cost['input_graph_bytes']:,} byte. Đây là quan sát chi phí tiến trình, không benchmark máy cô lập hoặc giờ công toàn task (`cost.json`). Trước lượt này có quan sát CPU workload ngắn, không dừng tiến trình khác (`runs/quan-sat-chi-phi-001/workloads.json`). Pilot/giờ từng graph có trong run và tổng hợp; không ngoại suy hoặc đề xuất EC2. Peak lượt003 không đo được do kiểu handle Windows; không thay null bằng0. Tổng byte thực lưu cuối, gồm failed/replayed/history, nằm ở manifest. Giờ công toàn task không đo liên tục, vẫn OPEN; không dùng thời gian compute để xác nhận dự toán công.

Không có số công bố tương ứng với bộ biến đổi bản ghi; oracle/nguồn/trung gian là căn cứ kiểm. Các kiểm này chứng minh hành vi triển khai trong miền giao, chưa chứng minh ứng dụng đã triển khai, telemetry đầy đủ hoặc lợi ích RCA.
''')
    md(B/'ban-giao.md',f'''# Bàn giao T-039 cho phản biện

Đã triển khai dựng/đối chiếu trên toàn {summary['graph_count']} graph Nezha-OB dev đã lưu, bằng snapshot T036 cũ đã ghim mà Minh duyệt dùng trực tiếp. T037/T038 và mã chung không được sửa. Phản biện chính thức: Claude; chưa nghiệm thu task/P5/G3. Phần xác nhận đầy đủ nguồn deployment chỉ đạt một phần vì lineage ngoài snapshot còn OPEN.

Đọc `nguon.json`, `bao-phu-nguon.md/json`, `ban-ghi.json`, `mapping.json`, `do-thi/`, `doi-chieu/tong-hop.json`, `phan-tich-chenh-lech.md`, `kiem-dung-dan.md`; manifest dẫn mọi file/hash. Mọi comparison có `conditional_reference=true`, domain dev-adapter và interval gốc. full có interval null là union miền adapter được phép, không cả ngày. N/A là tên cửa sổ theo giao thức, không tự chứng minh sạch/lỗi.

| Mức | Cửa sổ | Số graph | Giao/S endpoints | Giao/T eligible endpoints |
|---|---|---:|---:|---:|
{chr(10).join(tables)}

Nguồn: `doi-chieu/tong-hop.json#/rows/*/views/endpoints`; từng row có input/output/interval. Có {m['entity:verified']} entity mapping đã xác minh định danh nguồn; thao tác {m['operation:verified']} literal verified, {m['operation:unverified']} candidate chưa verified, {m['operation:unmapped']} SQL chưa có candidate (`#/mapping_counts`). Fraction1 trên eligible T không là đầy đủ trace. Typed có mẫu số trace0/null vì unknown; không kết luận sai kiểu. Chi tiết chuỗi evidence và từng nhóm/ca ở báo cáo chênh lệch.

Graph ở đây tham gia chuẩn hóa khóa, phép chiếu, giao và hiệu tập. Entity nodes là service/component/data/external có nguồn, operation giữ owner. Bindings tách DB logic với mysql instance; signals là địa chỉ log/trace/metric và điều kiện, chưa có giá trị đo hoặc host binding. Chưa có detector, score, lan truyền hoặc thứ hạng. Đạt phần mô hình/nguồn tham chiếu của DT18-NV2/NV3 và bước1 của cô; chưa trả lời hiệu quả cơ chế RQ3 hay toàn RQ5.

| Nơi nhận/owner | Đầu vào hoặc phép phân xử còn thiếu | Hệ quả và chi phí |
|---|---|---|
| T040 / Minh giao task | Registry, coverage, source→record→set, exclusions và các OPEN của cả ba nhánh; giữ pin nền và ngoại lệ rõ | Tổng hợp tính dùng được; chưa làm T040 bằng quyền T039. Công đọc/chốt chưa đo |
| Dataset/deployment authors; Minh duyệt thu | Commit app/build, image digest, rendered deploy và cấu hình collector/export CSV | Phân xử revision/alias/telemetry/Node; chưa có URL/revision/byte nên chưa tải. Chi phí thu chưa xác định; phải trình danh sách trước |
| P6 / Minh chốt SPEC | Literal verified20, candidate32 và SQL3; ví dụ match/mismatch cùng điều kiện | Cần xác minh tên/thời gian/availability khi chọn thao tác, giữ unknown và tập ứng viên; không tối ưu mapping theo tỷ lệ. Chưa có quyền chạy experiment mới |
| P9a/P9b / Minh và nhóm quan sát | Service/instance/pod namespace+UID, host ID có nghĩa, mapping hiệu lực theo thời gian; span kind/DB/messaging attributes; log trace/span IDs; source→export→schema | NodeName trong ứng dụng chưa chứng minh cột Node của dataset. Cần schema/collector+fixture join, không chỉ ổn định tên. Collector không khôi phục dữ liệu chưa ghi |
| Nguồn phụ / dataset authors | Producer Source/Target/Node, đầu vào/khóa/thời gian và sampling | Không dùng metadata ngày như đối chứng độc lập hoặc chọn P6; code đã đọc là consumer chưa xác định producer. Thu metadata/code mới phải duyệt riêng |

`de-xuat-bo-sung-nguon.md` tách phần có thể xử lý bằng source mới và phần cần chủ nguồn, giả định/điều kiện sai, owner và kết luận phụ thuộc. Không phải cổng mới hoặc yêu cầu tự chạy vượt SPEC. Còn nghi vấn revision/alias/domain/branch/static/telemetry được ghi theo từng nhóm; chưa có bằng chứng quy nguyên nhân vật lý của graph thiếu.

Lệnh tái lập sau khi Minh giao quyền chạy: `py -3 -X utf8 -B results/T-039/execute_pinned.py <ten-run-moi-chua-co>`; không import live src. Lệnh đọc/kiểm rẻ: `py -3 -X utf8 -B results/T-039/finish_results.py verify <ten-kiem-moi>` (chỉ tạo kết quả kiểm trong T039). Prompt trung tính cho Claude ở `prompt-claude.txt`, Minh chuyển thủ công. Chưa commit/push. Đề xuất commit sau nghiệm thu: `research: implement pinned T039 Online Boutique source graph comparison`.
''')
    md(B/'de-xuat-bo-sung-nguon.md','''# Phần nguồn chưa đủ và đề xuất bổ sung

Chưa duyệt tải mới; không tải trong lượt này. Đề xuất dưới đây phục vụ phần mục tiêu còn thiếu, không chặn phản biện kết quả tham chiếu đã có.

1. **App→dataset revision (OPEN).** Cần tác giả cung cấp commit ứng dụng, build provenance, digest image, rendered manifest đang thu và thời gian thu. Nguồn hiện có chỉ trỏ repository ứng viên, tag ảnh không chứng minh digest. Giả định cùng repo cùng dataset có thể sai vì build/branch/deploy khác. Không đủ nguồn trong snapshot để phân xử. Quyết định phụ thuộc: diễn giải cạnh riêng như thiếu telemetry hoặc runtime ground truth. URL/revision/byte chưa có; Minh/tác giả xác định trước đề xuất tải exact list. Chi phí máy nhỏ nếu chỉ metadata nhưng dung lượng chưa đo, giờ truy tác giả chưa biết.
2. **Instrumentation aliases (OPEN).** Source đã có dependencies/version và một Java agent binary; chưa có chuỗi library thực sự chạy→CSV span naming. Đề xuất chỉ lấy exact dependency implementation cần cho các candidate32 và SQL3 sau xác minh build; không lấy cả upstream mới nhất. Thư viện có thể đổi prefix, SQL naming, context và generated method coverage. Cần lập từng file/revision/byte từ metadata trước tải; chi phí đọc/kiểm chưa đo. Chưa có căn cứ tự biến chúng thành alias verified.
3. **Collector và metadata producer (OPEN).** Cần code/config/schema xuất Source/Target/Node, provenance input, cửa sổ áp dụng và resource identity. Bảy file Python đã khảo sát chưa chỉ ra writer này; không suy nó không tồn tại ở toàn Nezha. Hai CSV khác nhau có thể cùng telemetry. Chủ nguồn: tác giả dataset/deployment; Minh duyệt thu. Chưa có revision/URL/byte, không tạo giá trị hoặc mở daily Weight/Node để đóng mục. Phụ thuộc: độc lập nguồn phụ, host metrics, mapping hiệu lực theo thời gian của P9.
4. **Deployment ngoài snapshot (OPEN).** Istio injection/rendered manifest được script tham chiếu nhưng nguồn tương ứng thiếu; MySQL init có SQL nhưng chưa chứng minh provision. Cần exact config/version/digest/initialization logs hoặc manifest từ chủ deploy, không mở raw trong quyền hiện hành. Phụ thuộc: inventory toàn deployment và metric shared instance. Chi phí chưa đo; phải trình phạm vi cụ thể trước thực hiện.

Những gì có thể kiểm rẻ bằng nguồn đang có đã được ghi trong source audit, merge và phân tích. Các phần trên không được dùng như sự thật đã xác nhận để kết luận về lợi ích graph hoặc chọn P6. Nếu không thu được, giữ giới hạn so tham chiếu và thiết kế phép đánh giá có thể phân xử trong gói Minh giao; không tự nhận inventory runtime đầy đủ.
''')
    md(B/'de-nghi-ghi-quyet-dinh.md','''# Đề nghị ghi sổ chính thức — chưa ghi DECISIONS

Quyền task cấm ghi DECISIONS/WHY; các quyết định đã có trong LOG theo quyền người làm. Đề nghị Minh duyệt riêng file `docs/DECISIONS.md`, thêm mục mới theo mã kế tiếp chưa dùng, giữ nguyên mục cũ:

- Minh duyệt danh sách tải theo `results/T-039/de-xuat-tai.json`; giữ toàn phạm vi T039 một phiên và giữ pin nguồn Nezha, ghi chứng cứ commit/tree ở T039.
- Minh duyệt T039 dùng trực tiếp snapshot T036 đã ghim tại `runs/kiem-r1-after-002/code/`, giữ nguyên mã chung và T037/T038; lựa chọn này thay lựa chọn chờ gói chung trước đó. Không thay pin nội dung, SPEC, quyền mở test hoặc quyền commit.

Nguồn nguyên lời, thời điểm/quyền trong LOG T039 Phiên2–4 và authorization. Đây là đề xuất chép quyết định của Minh, không là quyết định khoa học mới. Ảnh hưởng: tái lập T039 và phân biệt pin nền với live shared khi tổng hợp. Chưa tự cấp số Q mới hoặc viết sổ.
''')
    prompt_source=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
    def block(section):
        return re.search(r'```text\n(.*?)\n```',prompt_source.split(section,1)[1],re.S)[1]
    prompt=block('## Prompt chung')
    substitutions={
      '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>':'T-039; tasks/T-039-p5b-online-boutique/SPEC.md; results/T-039/',
      '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>':'soát kết quả',
      '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>':'P5; chuẩn bị G3',
      '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>':'Codex người làm; Claude phản biện chính thức kết quả',
      '<danh sách đường dẫn và git diff từ commit gốc nếu có>':'AGENTS.md; docs/STATE.md; SPEC/LOG T039; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; nguồn DT18 và advisor trong docs/reference/sources/; nguồn và đầu ra tại results/T-039/. Bản trước tại runs/cho-pin-001/, thuc-thi-snapshot-004/before/ và ket-thuc-001/before/',
      '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>':'Chưa có REVIEW T039; lịch sử tự rà/quyền/checkpoint trong LOG T039',
      '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>':'results/T-039/manifest.json, ban-giao.md, kiem-dung-dan.md, execute_pinned.py; snapshot results/T-036/runs/kiem-r1-after-002/code/ và code-hashes.json; source registry/coverage, fixtures, runs và graph T035 canonical theo manifest. Python3.12, -X utf8 -B; lệnh tái lập/kiểm ghi tại ban-giao.md, chỉ chạy trong quyền Minh giao',
      '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>':'chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW/LOG/STATE hoặc sửa kết quả/pin; Minh có thể giao riêng bản REVIEW theo AGENTS'
    }
    for a,b in substitutions.items():prompt=prompt.replace(a,b)
    prompt+='\n\n'+block('### Soát kết quả')+'\n\n'+block('### G3 — Khóa thiết kế trước khi mở test')+'\n'
    assert not re.search(r'<[^>]+>',prompt)
    md(B/'prompt-claude.txt',prompt)
    write(FINAL/'report-data.json',dict(summary=summary['record_counts'],mapping=summary['mapping_counts'],counts_by_cell=tables,coverage_counts=cov['counts'],cost=cost,prompt_template_sha256=sha(ROOT/'docs/review-prompt.md')))
    print('reports written; append LOG/only T039 STATE row, then finalize')

def verify(name):
    dest=B/'runs'/name;dest.mkdir(exist_ok=False)
    manifest=read(B/'manifest.json');errors=[]
    for f in manifest['files']:
        p=ROOT/f['path']
        if not p.is_file() or sha(p)!=f['sha256']:errors.append(f['path'])
    write(dest/'verification.json',dict(status='PASS' if not errors else 'FAIL',checked=len(manifest['files']),mismatches=errors,manifest_sha256=sha(B/'manifest.json')))
    print(len(manifest['files']), 'hash checks', 'PASS' if not errors else errors)

def finalize():
    assert FINAL.exists()
    # Validate all final comparison paths against canonical input and literal.
    summary=read(B/'doi-chieu/tong-hop.json');registry=read(B/'nguon.json');doc=read(B/'ban-ghi.json')
    provenance=0;sourceids={x['id'] for x in registry['sources']}
    for k in ['entities','operations','relations','resource_bindings','signals']:
        for row in doc[k]:
            assert row['provenance']
            for p in row['provenance']:
                assert p['source_id'] in sourceids and p['locator'] and p['condition'];provenance+=1
    for source in registry['sources']:
        assert sha(ROOT/source['path'])==source['sha256']
    for row in summary['rows']:
        result=read(ROOT/row['output'])
        assert result['interval_ns']==row['interval_ns'] and result['conditional_reference']
        assert result['context']['domain']=='dev-adapter'
        for view,stats in row['views'].items():
            assert all(result['views'][view][k]==v for k,v in stats.items())
        archived=B/'runs/thuc-thi-snapshot-004/outputs'/Path(row['output']).relative_to('results/T-039')
        assert sha(ROOT/row['output'])==sha(archived),'canonical output differs from exact run004 archive'
    for name in ['ban-ghi.json','mapping.json','do-thi/thuc-the.json','do-thi/thao-tac.json','do-thi/chieu-thuc-the.json','doi-chieu/tong-hop.json']:
        assert sha(B/name)==sha(B/'runs/thuc-thi-snapshot-004/outputs'/name)
    evidence=read(B/'runs/phan-tich-002/source-to-difference.json')
    assert len(evidence['cells'])==132 and len(evidence['chains'])==93
    assert len(evidence['groups'])==7 and len(evidence['excluded_edge_groups'])==53
    for g in evidence['groups']:
        assert set(g['competing'])=={'revision','alias','domain_window','branch','incomplete_static_source','missing_telemetry','conversion_error'}
        assert g['matched_counterparts']
    # Unmodified literal oracle still agrees byte-for-byte with before-transform copy.
    assert sha(B/'fixtures/oracle.json')==sha(B/'runs/trien-khai-001/oracle-before-transform.json')
    before=(FINAL/'before-LOG.md').read_bytes();after=(ROOT/'tasks/T-039-p5b-online-boutique/LOG.md').read_bytes()
    assert after.startswith(before)
    state_before=(FINAL/'before-STATE.md').read_text(encoding='utf-8-sig');state_after=(ROOT/'docs/STATE.md').read_text(encoding='utf-8-sig')
    erase=lambda text:re.sub(r'^\| T-039 \|[^\n]*','T039_ROW',text,flags=re.M)
    assert erase(state_before)==erase(state_after),'unrelated STATE change; do not overwrite other session'
    prompt=(B/'prompt-claude.txt').read_text(encoding='utf-8')
    assert prompt.strip() in after.decode('utf-8-sig').replace('\r\n','\n')
    template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
    block=lambda section:re.search(r'```text\n(.*?)\n```',template.split(section,1)[1],re.S)[1]
    assert prompt.strip().endswith(block('### Soát kết quả')+'\n\n'+block('### G3 — Khóa thiết kế trước khi mở test'))
    general=block('## Prompt chung')
    literal_parts=re.split(r'<[^>]+>',general)
    cursor=0
    for part in literal_parts:
        ix=prompt.find(part,cursor);assert ix>=cursor,'prompt template literal differs';cursor=ix+len(part)
    protected=read(B/'runs/thuc-thi-snapshot-004/protected-after.json')
    observed=[dict(path=p,before=d,current=sha(ROOT/p),unchanged=sha(ROOT/p)==d) for p,d in protected.items()]
    jsoncount=0
    for p in B.rglob('*.json'):
        read(p);jsoncount+=1
    write(FINAL/'verification.json',dict(status='PASS',graph_count=len(summary['rows']),provenance_references=provenance,registry_hashes=True,json_files_parsed=jsoncount,exact_run004_archives=True,independent_oracle_unchanged=True,analysis_chains=93,analysis_groups=7,log_append_only=True,only_T039_STATE_row_changed=True,prompt_in_LOG=True,prompt_template_literals=True,protected=observed,interpretation='Snapshot pin unchanged. Concurrent files are observed only; no mutation of shared/T037/T038 is authorized or performed.',source_scope='whole snapshot partition; deployment completeness OPEN'))
    files=[]
    for p in sorted(B.rglob('*')):
        if p.is_file() and p!=B/'manifest.json':files.append(dict(path=path(p),bytes=p.stat().st_size,sha256=sha(p)))
    write(B/'manifest.json',dict(task='T-039',created_utc=datetime.now(timezone.utc).isoformat(),status='IMPLEMENTED_REFERENCE_WAITING_CLAUDE_REVIEW',current_run='runs/thuc-thi-snapshot-004',finalization_run='runs/ket-thuc-001',task_accepted=False,graph_mapping_comparison_completed=True,source_deployment_completeness='OPEN_PARTIAL',shared_pin_changed=False,shared_code_used='original pinned snapshot, not current src',pin=dict(manifest='results/T-036/manifest.json',sha256=sha(ROOT/'results/T-036/manifest.json'),code_hashes=read(ROOT/'results/T-036/runs/kiem-r1-after-002/code-hashes.json')),input_graph_count=len(summary['rows']),log_sha256=sha(ROOT/'tasks/T-039-p5b-online-boutique/LOG.md'),state_T039_row=re.search(r'^\| T-039 \|[^\n]*',state_after,re.M)[0],count=len(files),total_payload_bytes_excluding_manifest=sum(x['bytes'] for x in files),files=files))
    # Read back every written hash; no verifier artifact outside this manifest.
    m=read(B/'manifest.json');assert all(sha(ROOT/f['path'])==f['sha256'] for f in m['files'])
    print(json.dumps(dict(status='PASS',files=len(files),bytes=m['total_payload_bytes_excluding_manifest'],graphs=len(summary['rows']),protected_unchanged=all(x['unchanged'] for x in observed)),ensure_ascii=False))

if __name__=='__main__':
    if sys.argv[1]=='reports':reports()
    elif sys.argv[1]=='finalize':finalize()
    elif sys.argv[1]=='verify':verify(sys.argv[2])
