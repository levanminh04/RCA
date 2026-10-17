"""Kiểm/chốt source checkpoint khi Minh yêu cầu chờ pin; không nhập shared code."""
from pathlib import Path
from collections import Counter
import datetime as dt
import difflib
import hashlib
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/T-039'
RUN = BASE / 'runs/cho-pin-001'


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def save(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(p):
    data = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


if sys.argv[1] in {'prepare', 'resume'}:
    RUN.mkdir(parents=True, exist_ok=sys.argv[1] == 'resume')
    for name in ['manifest.json', 'nguon.json', 'bao-phu-nguon.json', 'ban-giao.md', 'kiem-dung-dan.md']:
        if not (RUN / ('before-' + name)).exists():
            shutil.copyfile(BASE / name, RUN / ('before-' + name))
    if not (RUN / 'LOG-before-close.md').exists():
        shutil.copyfile(ROOT / 'tasks/T-039-p5b-online-boutique/LOG.md', RUN / 'LOG-before-close.md')
    save(RUN / 'decision.json', {'user_date': '2026-10-16',
        'user_verbatim': 'Chờ gói chung và duyệt lại pin',
        'question': 'Mã chung hiện thêm smtp, manifest/pin T-036 vẫn bản cũ; dùng snapshot cũ hoặc chờ gói chung?',
        'chosen_action': 'WAIT_SHARED_PACKAGE_AND_MINH_APPROVAL_OF_NEW_PIN',
        'shared_code_modified_by_this_task': False, 'build_compare_project_run': False,
        'source_only_work_completed': True})
    registry = read(BASE / 'nguon.json')
    receipts = read(BASE / 'runs/thu-nguon-001/acquisition.json')
    source_index = {}
    for receipt in receipts['files']:
        p = ROOT / receipt['path']
        assert digest(p) == {k: receipt[k] for k in ['path', 'bytes', 'sha256']}
        if '/augmented-ob-94a01ba4/' in receipt['path']:
            prefix, revision = 'OB:', '94a01ba4c7c79e0c0b2c9da073ba081fcedc4bf1'
        else:
            prefix, revision = 'NEZHA:', 'd8140101fdb4e7dfb60d3ef9f64706f382b68470'
        source_id = prefix + receipt['source_path']
        source_index[source_id] = {'id': source_id, 'kind': 'application-source' if prefix == 'OB:' else 'analysis-source',
            'revision': revision, 'sha256': receipt['sha256'], 'path': receipt['path'],
            'condition': 'candidate source revision; not proof of dataset build/image/deployment',
            'dataset_link': 'OPEN', 'url': receipt['url']}
    ids = {r['id'] for r in registry['sources']}
    registry['sources'] += [r for ident, r in sorted(source_index.items()) if ident not in ids]
    registry['status'] = 'SOURCE_REGISTRY_DRAFT_GRAPH_EXECUTION_WAITING_NEW_PIN'
    registry['builder_validation'] = 'NOT_RUN'
    registry['current_shared_code_matches_old_pin'] = False
    registry['pin_decision'] = 'runs/cho-pin-001/decision.json'
    save(BASE / 'nguon.json', registry)
    summaries = []
    for part in ['common', 'backend', 'go']:
        doc = read(BASE / 'parts' / (part + '.json'))
        assert doc['scope'] == {'system': 'Nezha-OB', 'revision': '94a01ba4c7c79e0c0b2c9da073ba081fcedc4bf1'}
        entities = {r['id'] for r in doc['entities']}
        operations = {(r['entity'], r['name']) for r in doc['operations']}
        checked = 0
        for group in ['entities', 'operations', 'relations', 'signals', 'resource_bindings']:
            for row in doc[group]:
                assert row['provenance']
                for evidence in row['provenance']:
                    source = source_index[evidence['source_id']]
                    assert evidence['locator'].strip() and evidence['condition'].strip()
                    # Locator range bounded where numeric; semantic correctness is not inferred by this check.
                    try:
                        text = (ROOT / source['path']).read_text(encoding='utf-8')
                        maximum = len(text.splitlines())
                        nums = [int(n) for n in re.findall(r'(?:\bL|[–-]L?)(\d+)', evidence['locator'])]
                        assert all(1 <= n <= maximum for n in nums), (source['path'], evidence['locator'], maximum)
                    except UnicodeDecodeError:
                        pass
                    checked += 1
        for row in doc['relations']:
            for endpoint in [row['source'], row['target']]:
                assert endpoint['entity'] in entities
                assert endpoint['operation'] is None or (endpoint['entity'], endpoint['operation']) in operations
        summaries.append({'part': part, 'counts': {k: len(doc[k]) for k in ['entities','operations','relations','resource_bindings','signals']},
                          'provenance_reference_checks': checked, 'json_and_reference_checks': 'PASS',
                          'builder_schema_validation': 'NOT_RUN', 'merged_graph': False})
    coverage = read(BASE / 'bao-phu-nguon.json')
    specialists = []
    for name in ['backend', 'go']:
        v = read(BASE / 'parts' / (name + '-coverage.json'))
        specialists += [(name, row) for row in v['files']]
    bypath = {}
    for name, row in specialists:
        bypath.setdefault(row['path'], []).append({'reviewer_support_part': name,
             'inspection': row.get('status', row.get('inspection')), 'reason': row.get('reason', row.get('impact'))})
    for row in coverage['rows']:
        local = row.get('path_local')
        row['specialist_inspection'] = bypath.get(local, [])
        if row['status'] == 'read_application_source':
            row['status'] = 'source_screened_with_specialist_scope' if local in bypath else 'structural_scan_only'
            row['reason'] = 'reference scan saved; specialist scope is explicit per file; no claim beyond recorded inspection'
        if row['status'] == 'read_test_source_structure':
            row['status'] = 'test_source_scan_only'
            row['reason'] = 'source reference scan only; exclusion from runtime based on build entrypoints, not dataset test access'
    coverage['counts'] = dict(Counter(r['status'] for r in coverage['rows']))
    coverage['completeness']['semantic_coverage_fully_verified'] = False
    coverage['completeness']['builder_and_comparison_validated'] = False
    coverage['completeness']['pending'] = ['root complete source review/merge', 'pin approval', 'independent oracle execution',
                                          'mapping/build/projection/comparison/analysis']
    save(BASE / 'bao-phu-nguon.json', coverage)
    save(RUN / 'source-checkpoint.json', {'parts': summaries,
        'counts_not_additive': 'overlapping entities and operations across fragments; not merged inventory totals',
        'whole_tree_partition': {'entries': coverage['entry_count'], 'blobs': coverage['blob_count'], 'counts': coverage['counts']},
        'sources_in_registry_added': len(source_index), 'shared_api_imported': False,
        'oracle_status': 'written_before_transform; not run', 'current_run': 'runs/trien-khai-001',
        'machine_benchmark': False, 'graph_or_mapping_outputs': False})
    # Exact current standard blocks; only metadata placeholders are filled.
    template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8-sig')
    def block(heading):
        return re.search(r'```text\n(.*?)\n```', template.split(heading + '\n',1)[1], re.S).group(1)
    common = block('## Prompt chung')
    replacements = [
       'T-039; tasks/T-039-p5b-online-boutique/SPEC.md; checkpoint results/T-039/runs/cho-pin-001/',
       'soát kết quả', 'P5; chuẩn bị G3', 'Codex người làm; Claude phản biện chính thức kết quả',
       'AGENTS.md; docs/STATE.md; SPEC và LOG T-039; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; DT18 và advisor-2026-09-23.md trong docs/reference/sources/; results/T-039/nguon.json, bao-phu-nguon.json và parts/. Diff/bản trước tại runs/trien-khai-001/, pin-lech-001/ và cho-pin-001/',
       'Không có REVIEW T-039; lịch sử quyền và checkpoint ở LOG Phiên 2–3. Lịch sử T-036 theo LOG/REVIEW của T-036',
       'results/T-039/manifest.json; runs/thu-nguon-001/acquisition.json; fixtures/oracle.json; source fragments/coverage trong parts/; results/T-036/manifest.json pin runs/kiem-r1-after-002 và code-hashes.json tại run; metadata nguồn đã thu theo registry. Windows/PowerShell, Python -X utf8 -B; checkpoint_sources.py chỉ tạo checkpoint trong T-039, chưa được tự cấp quyền chạy lại hoặc dựng graph bởi prompt này',
       'chỉ đọc và trả lời trong chat; không ghi REVIEW/LOG/STATE hoặc sửa nguồn/kết quả/pin; không chạy builder/compare/experiment ngoài quyền Minh cấp riêng',
    ]
    placeholders = re.findall(r'<[^>]+>', common)
    assert len(placeholders) == len(replacements)
    for marker,value in zip(placeholders,replacements):
        common = common.replace(marker,value)
    prompt = '\n\n'.join([common,block('### Soát kết quả'),block('### G3 — Khóa thiết kế trước khi mở test')])+'\n'
    (BASE/'prompt-claude-checkpoint.txt').write_text(prompt,encoding='utf-8')
    (BASE/'ban-giao.md').write_text('''# T-039 — checkpoint chờ pin chung, 16/10/2026

**Chưa hoàn tất task.** Minh chọn “Chờ gói chung và duyệt lại pin” sau khi current build.py thêm smtp còn manifest T-036 vẫn pin cũ. Không tự dùng snapshot cũ thay mã hiện hành, đổi pin/hash, rollback hoặc gửi chat cho nhánh khác. Bằng chứng exact bytes/diff ở runs/pin-lech-001/.

Đã làm tiếp phần nguồn độc lập: parts/common.json, backend.json, go.json và hai coverage chuyên biệt; registry nguon.json, phân hoạch toàn cây bao-phu-nguon.json, oracle literal fixtures/oracle.json viết trước code chuyển đổi riêng. JSON/ref/locator/hash đã kiểm; **chưa import bộ dựng hoặc xác nhận schema/build/compare**. Source fragments có overlap nên không cộng tổng thành inventory cuối. Standalone client/example giữ trong source_examples ngoài document backend, tránh gán caller cho server.

Nguồn đã thu vẫn đúng scope và hash; không có tải thêm hoặc mở raw telemetry/Weight/Node values/test/heldout/archive. Ba ảnh docs đã xem; SVG/CSS/template được kiểm reference theo browser scope. Binary JAR chỉ metadata/manifest; không decompile/chạy. Coverage tách semantic review/scan/hash-only/excluded, không biến reference scan thành semantic proof. Tập cây được phân hoạch đủ 274 entry/219 blob; bốn log thô vẫn excluded-unread; external build/image/collector/Istio/library/source lineage còn OPEN.

**Bước tiếp chính xác:** sau Minh duyệt gói chung và pin mới, kiểm manifest/code-hashes/snapshot/current code đã đồng nhất; đối chiếu ảnh hưởng đến ba nhánh và xin quyền cập nhật pin/registry task theo gói duyệt. Không tự coi shared code thay đổi là pin mới đã được duyệt. Khi được phép chạy: root rà/merge fragments bằng identity+union provenance, giải duplicate/runtime_name/ownership, hoàn tất source coverage; viết mapping có nguồn, chạy oracle trước transform; dựng/chiếu/đối chiếu toàn graph hiện hành/interval/dev-adapter ở hai mức; kiểm và phân tích mismatch cùng match tương ứng. Không có graph/mapping T-039 đã kiểm để dùng tiếp.

Đầu ra hợp lệ trước đó: pin/graph inventory tiền kiểm và acquisition/metadata theo manifest các run. Đầu ra mới là nguồn/bản ghi nháp có điều kiện. Các bước còn lại giữ nguyên toàn SPEC, không giảm kiểm vì một phiên hoặc do subagent dừng usage. Claude phản biện chính thức; prompt nguyên văn Prompt chung + Soát kết quả + G3 ở prompt-claude-checkpoint.txt và LOG Phiên 3 để Minh chọn chuyển thủ công.

Nguồn thiếu/owner: tác giả triển khai cần image digest/build/revision/manifest thu; collector/export schema cần nối NodeName→Node và producer Source/Target; source instrumentation chính xác cần xác minh runtime alias trước mapping. Minh quyết nguồn/phiên bản bổ sung, không tự tải bằng quyền đã có. T-040/P6/P9 chưa nhận được kết quả độ khớp hoặc bằng chứng telemetry thiếu; RQ3/RQ5/P5b/G3 còn OPEN. Nội dung nên ghi chính thức về lựa chọn chờ pin được trình trong de-nghi-ghi-quyet-dinh.md, chưa sửa DECISIONS/WHY.
''',encoding='utf-8')
    with (BASE/'kiem-dung-dan.md').open('a',encoding='utf-8') as f:
        f.write('\n\n## Checkpoint nguồn chờ pin — 16/10/2026\n\nPhát hiện current build.py lệch snapshot, giữ exact evidence và dừng dependency. Minh chọn chờ gói chung/duyệt lại pin. Không nhập build/project/compare để kiểm fragment. Chỉ kiểm JSON, ID/refs/provenance/locator source và source hash; kết quả ở runs/cho-pin-001/source-checkpoint.json. Root chưa nhận source fragment đã validated contract hoặc semantic coverage toàn snapshot. Oracle literal đã có trước biến đổi, chưa chạy; không bịa kết quả oracle. Checkpoint cuối kiểm manifest/scope/append-only/STATE/prompt/expected mismatch; trạng thái blocked_dependency, không all-task-pass.\n')
    with (ROOT/'tasks/T-039-p5b-online-boutique/LOG.md').open('a',encoding='utf-8') as f:
        f.write('''

### Kết thúc checkpoint chờ pin — 16/10/2026

**Quyết định Minh:** nguyên văn “Chờ gói chung và duyệt lại pin”, trả lời câu hỏi xử lý build.py lệch snapshot. Giữ toàn SPEC, không dùng snapshot cũ để dựng/đối chiếu; không sửa/hash lại mã chung hoặc tự chuyển pin.

1. Đã tiếp checkpoint mới nhất; hai subagent trước hết usage chưa ghi fragment đã chạy lại, hoàn tất fragment nguồn/coverage. Root lưu oracle trước transform, phần nguồn chung, registry và phân hoạch toàn tree; kiểm refs/source hash. Chưa hoàn tất T-039: mapping/build/project/compare/phân tích chưa chạy; semantic coverage/merge chưa nghiệm thu. Câu hỏi nguồn chỉ có bản ghi có điều kiện, chưa có độ khớp hoặc lợi ích RCA; RQ3/RQ5/P5b/G3 còn OPEN.
2. Chỉ ghi results/T-039/, nối LOG này và đúng dòng T-039 trong STATE. Không sửa SPEC/WHY/DECISIONS/REVIEW/src/T-035/T-036/platform/task khác. Exact shared-code mismatch lưu ở pin-lech-001; không quy người sửa hoặc quyền duyệt của nhánh khác khi không có bằng chứng.
3. Kiểm nguồn 229 file/metadata còn khớp; fragments chỉ JSON/ID/ref/locator/provenance và oracle-before-transform snapshot; không schema builder validation. Cây phân hoạch đủ, tách read/scan/hash/excluded. Kiểm cuối source set/manifest/phạm vi/prefix/prompt và mismatch expected ở runs/cho-pin-001/final-verification.json; không chạy pilot hoặc thực nghiệm. Source counters và file list ở source-checkpoint.json/manifest. Giờ/RAM máy toàn pipeline vẫn chưa đo; không dùng chi phí scan làm số pipeline.
4. CHẶN hiện tại là mã chung không khớp pin; Minh đã chọn chờ pin mới, owner quyết pin là Minh/gói chung. Phần nguồn còn OPEN gồm deployment/image, instrumentation alias, collector/Node/nguồn phụ và external source; không coi thiếu source là nguyên nhân telemetry. Nơi nhận T-040/P6/P9 và đầu vào cụ thể ở ban-giao.md. Không giảm yêu cầu hoặc tự nghiệm thu đầu ra để xử lý thiếu token/usage.

**Bước tiếp chính xác:** Minh duyệt gói chung và pin; kiểm manifest/code snapshot/current đã đồng nhất rồi rà ảnh hưởng/ghi pin T039 đúng quyền. Sau đó root soát/merge source fragments, oracle, mapping có owner/provenance, dựng/chiếu/đối chiếu toàn graph theo SPEC, lần nhóm chênh lệch và match tương ứng. Lệnh đọc: Get-Content -Raw -LiteralPath 'results/T-039/ban-giao.md'. Không tự mở/gửi chat hay dùng code changed trước Minh duyệt pin.

**Lệnh cuối dự kiến:** py -3 -X utf8 -B results/T-039/checkpoint_sources.py verify. Chỉ kiểm/chốt checkpoint; không chạy shared code. **Đề xuất commit, chưa làm:** docs: checkpoint T-039 source records pending shared contract pin. Chỉ commit/push khi Minh yêu cầu/duyệt riêng.

### Prompt Claude — checkpoint kết quả (Minh chọn gửi hoặc dừng)

```text
''')
        f.write(prompt+'```\n')
    with (BASE/'de-nghi-ghi-quyet-dinh.md').open('a',encoding='utf-8') as f:
        f.write('\n\nBổ sung nguyên ý Minh ngày 16/10/2026, chưa ghi file chung: sau khi source chung lệch pin do thêm smtp, Minh chọn “Chờ gói chung và duyệt lại pin”. T-039 dừng dựng/đối chiếu phụ thuộc, không tự dùng snapshot cũ hoặc chuyển pin. Lời yêu cầu tiếp tục checkpoint/giữ chất lượng và kết quả nguồn độc lập lưu LOG Phiên 3; không suy thành quyền sửa shared hoặc DECISIONS.\n')
    print('Source-only checkpoint prepared; shared dependency remains stopped.')
elif sys.argv[1] in {'verify', 'verify-2'}:
    assert RUN.is_dir()
    if sys.argv[1] == 'verify-2':
        assert not (RUN/'final-verification-before-pin-label.json').exists()
        shutil.copyfile(RUN/'final-verification.json', RUN/'final-verification-before-pin-label.json')
        shutil.copyfile(BASE/'manifest.json', RUN/'manifest-before-pin-label.json')
    else:
        assert not (RUN/'final-verification.json').exists()
    a=read(BASE/'runs/thu-nguon-001/acquisition.json')
    sources=a['files']+a['metadata']
    for r in sources:
        assert digest(ROOT/r['path']) == {k:r[k] for k in ['path','bytes','sha256']}
    protected=read(BASE/'runs/trien-khai-001/protected-before.json')
    states=[]
    for r in protected:
        actual=digest(ROOT/r['path'])['sha256'];states.append({'path':r['path'],'expected':r['sha256'],'actual':actual,'same':actual==r['sha256']})
    mismatch=[r for r in states if not r['same']]
    assert [r['path'] for r in mismatch]==['src/do_thi_tinh/build.py'], mismatch
    evidence=read(BASE/'runs/pin-lech-001/evidence.json')
    assert mismatch[0]['actual']==evidence['actual_sha256']
    before=(RUN/'STATE-before-our-write.md').read_bytes();after=(ROOT/'docs/STATE.md').read_bytes()
    lines1,lines2=before.splitlines(keepends=True),after.splitlines(keepends=True)
    assert len(lines1)==len(lines2)
    changed=[(x,y) for x,y in zip(lines1,lines2) if x!=y]
    assert len(changed)==1 and all(x.startswith(b'| T-039 |') for x in changed[0])
    log=(ROOT/'tasks/T-039-p5b-online-boutique/LOG.md').read_bytes()
    assert log.startswith((RUN/'LOG-before-close.md').read_bytes())
    prompt=(BASE/'prompt-claude-checkpoint.txt').read_text(encoding='utf-8')
    assert log.decode('utf-8').replace('\r\n','\n').count(prompt)==1
    template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
    for heading in ['### Soát kết quả','### G3 — Khóa thiết kế trước khi mở test']:
        block=re.search(r'```text\n(.*?)\n```',template.split(heading+'\n',1)[1],re.S).group(1)
        assert block in prompt
    common=re.search(r'```text\n(.*?)\n```',template.split('## Prompt chung\n',1)[1],re.S).group(1)
    assert common.split('Không sửa ngoài phạm vi trên,',1)[1] in prompt
    for p in BASE.rglob('*.json'):
        read(p)
    save(RUN/'final-verification.json',{'checkpoint_checks_pass':True,'task_complete':False,
        'dependency_state':'WAIT_SHARED_PACKAGE_AND_MINH_APPROVAL_OF_NEW_PIN',
        'shared_pin_mismatch_expected_and_preserved':mismatch,
        'protected_hash_reference':'execution-opening live-byte observation, NOT approved T036 pin; shared file may already have been edited concurrently when captured',
        'approved_shared_pin_check':{'path':evidence['path'], 'expected_by_pinned_manifest':evidence['expected_sha256'],
          'current_actual':evidence['actual_sha256'], 'same':False, 'source':'runs/pin-lech-001/evidence.json; T036 code-hashes.json'},
        'protected_inputs':states,
        'sources_verified':len(sources),'log_append_only':True,'state_only_task_row':True,
        'prompt_standard_preserved':True,'shared_builder_imported_or_run':False,
        'log':digest(ROOT/'tasks/T-039-p5b-online-boutique/LOG.md'),'state':digest(ROOT/'docs/STATE.md'),
        'last_command':'py -3 -X utf8 -B results/T-039/checkpoint_sources.py verify'})
    diff=''.join(difflib.unified_diff(before.decode('utf-8-sig').splitlines(True),after.decode('utf-8-sig').splitlines(True),fromfile='before-write/STATE.md',tofile='after/STATE.md'))
    diff+=''.join(difflib.unified_diff((RUN/'LOG-before-close.md').read_text(encoding='utf-8-sig').splitlines(True),log.decode('utf-8-sig').splitlines(True),fromfile='before-close/LOG.md',tofile='after/LOG.md'))
    (RUN/'changes.diff').write_text(diff,encoding='utf-8')
    files=[digest(p) for p in sorted(BASE.rglob('*')) if p.is_file() and p!=BASE/'manifest.json']
    save(BASE/'manifest.json',{'task':'T-039','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
       'status':'SOURCE_CHECKPOINT_WAITING_SHARED_PACKAGE_AND_APPROVED_PIN','current_run':'runs/cho-pin-001',
       'source_execution_run':'runs/trien-khai-001','shared_pin_changed':False,'spec_changed':False,
       'task_complete':False,'graph_mapping_comparison_completed':False,'count':len(files),'files':files,
       'excludes':'manifest itself; LOG/STATE hashes in final-verification.json',
       'open':['approved common pin','source semantic coverage/merge','mapping/oracle/build/compare/analysis','deployment/auxiliary-source/host lineage']})
    assert all(digest(ROOT/r['path'])==r for r in files)
    print(json.dumps({'checkpoint_checks_pass':True,'task_complete':False,'files':len(files),'sources':len(sources),'dependency':'waiting_approved_pin'}))
else:
    raise ValueError('prepare or verify')
