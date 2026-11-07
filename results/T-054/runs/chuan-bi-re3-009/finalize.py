"""Checkpoint a preparation result, preserving historical artifacts and source code."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
LOG = ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md'
STATE = ROOT/'docs/STATE.md'


def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


checkpoint = json.loads((RUN/'checkpoint.json').read_text(encoding='utf-8'))
before = {k.replace('\\', '/'): v for k, v in checkpoint['before'].items()}
log_key = str(LOG.relative_to(ROOT)).replace('\\', '/')
assert hashlib.sha256(LOG.read_bytes()[:before[log_key]['bytes']]).hexdigest() == before[log_key]['sha256']
assert pin(STATE) == before['docs/STATE.md']
assert pin(ROOT/'tasks/T-054-khoa-g3-chay-p7-a/SPEC.md') == before['tasks/T-054-khoa-g3-chay-p7-a/SPEC.md']
checkpoint['retained_failures'].append({'step': 'first finalize009', 'error': 'KeyError docs/STATE.md',
                                        'cause': 'Windows backslash keys in before snapshot',
                                        'mutation_before_failure': 'none',
                                        'resolution': 'normalize dictionary keys to forward slashes'})
(RUN/'before-state.md').write_bytes(STATE.read_bytes())

# Bind the upstream code actually inspected to the existing pinned revision.
upstream = Path('D:/RCA-ext/src/RCAEval')
revision = '259ea4167160256a74ad30004aa3d96a998c846e'
assert subprocess.check_output(['git', '-C', str(upstream), 'rev-parse', 'HEAD']).decode().strip() == revision
sources = json.loads((RUN/'source-pins.json').read_text(encoding='utf-8'))
sources['upstream'] = []
for rel in ['RCAEval/io/time_series.py', 'RCAEval/e2e/tracerca.py', 'RCAEval/utility/__init__.py']:
    blob = subprocess.check_output(['git', '-C', str(upstream), 'show', revision+':'+rel])
    working = (upstream/rel).read_bytes()
    assert working.replace(b'\r\n', b'\n') == blob.replace(b'\r\n', b'\n')
    sources['upstream'].append({'repository': str(upstream), 'revision': revision, 'path': rel,
                                **pin(upstream/rel), 'matches_git_blob_after_EOL': True})
save(RUN/'source-pins.json', sources)

template = (ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')


def block(heading):
    part = template.split(heading, 1)[1]
    return re.search(r'```text\n(.*?)\n```', part, re.S).group(1)


common = block('## Prompt chung')
replacements = {
    '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>': 'T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; results/T-054/runs/chuan-bi-re3-009/bao-cao.md',
    '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>': 'soát kết quả',
    '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>': 'P7(a), chuẩn bị G3',
    '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>': 'Codex người làm; Claude người phản biện',
    '<danh sách đường dẫn và git diff từ commit gốc nếu có>': 'AGENTS.md; SPEC/LOG T-054; docs/STATE.md, MRP.md, WHY.md, DECISIONS.md, LESSONS.md; các nguồn đề tài dưới đây',
    '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>': 'Các lượt được LOG T-054 dẫn theo thời gian',
    '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>': 'results/T-054/manifest-chuan-bi-re3-009.json; results/T-054/runs/chuan-bi-re3-009/; source-pins.json; D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B',
    '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>': 'Chỉ đọc và trả lời trong chat; không sửa file, không chạy phương pháp, không mở dữ liệu khóa, không SSH/sync, không commit/push',
}
for old, new in replacements.items():
    assert old in common
    common = common.replace(old, new)
prompt = common+'\n\n'+block('### Soát kết quả')+'\n\n'+block('### G3 — Khóa thiết kế trước khi mở test')+'\n'
(RUN/'prompt-claude.txt').write_text(prompt, encoding='utf-8')

end = '''

### Kết thúc checkpoint009 — chuẩn bị RE3 còn điều kiện

Đã phân tích lại đủ 5 schema metric/30ca từ 90footer đã lưu, không lấy lại footer hoặc mở data page. Inventory-schema ghi 12 owner chung/28 owner hợp; 2ca có tên namespace ngoài nhóm chung; chưa xác nhận dữ liệu thêm có tín hiệu hoặc là lỗi dataset. Đã phân biệt đơn vị mã hóa với cadence/r; metrics.time có nguồn khai giây, trace us là suy luận từ Jaeger/code, log unit/r/inventory vẫn thiếu nguồn RE3. Không dùng T039 Nezha làm deployment RE3.

Đã lập 8 dòng khả năng hỗ trợ theo code/schema, chưa tuyên bố hỗ trợ trên ca thật. 27 kiểm tổng hợp PASS: biên/đơn vị/parent-key/suffix; tái hiện ts-* làm rỗng metric cả5schema trong adapter TORAI TT. Hai literal dataset của BARO/TraceRCA không tự chứng minh lỗi số; đã thu hẹp nhận định003 bằng phân tích code. Không đổi hay mở lại kết quả task cũ. RQ3/RQ5 chưa được phân xử bằng RE3 vì chưa mở held-out; kết quả này chỉ phục vụ hợp đồng trước G3.

Đã trình bản vá H2 chính xác9filecode+SPEC/WHY/DECISIONS tại bao-cao009; chưa cài. Câu hỏi duyệt được gửi cho Minh, chưa coi là đã trả lời. Profile đơn vị/U/alias/r bắt buộc, thiếu thì chặn trước method; duyệt cài không tự chốt giả định chưa kiểm hoặc mở dữ liệu. H1 còn cần tài liệu exporter/deployment hoặc quyết định rõ về giả định chưa kiểm. Cloud vẫn tạm dừng riêng theo Minh, main/G3 chưa được mở.

File thay đổi lượt009: output runs/chuan-bi-re3-009/, manifest-chuan-bi-re3-009.json; LOG nối thêm và đúng dòng T054 STATE. Không sửa core, SPEC, WHY, DECISIONS, dữ liệu hay pin008; chưa commit/push. Hai phép kiểm bootstrap hash lịch sử dừng vì LOG/STATE đã cập nhật hợp lệ; đã đổi sang pin output bất biến dùng lại. urllib GitHub gặp lỗi chứng chỉ; PowerShell dùng trust Windows đọc metadata được. Một lệnh writer inline lớn bị policy từ chối không nêu lý do cụ thể; chuyển sang file script tường minh, không đổi quyền hoặc tắt xác thực.

Bước tiếp chính xác: đọc bao-cao009 mục Bản vá H2 và time-and-observation-contract.json; nhận quyết định Minh. Chỉ sau duyệt exact patch mới cài9filecode và các nguồn được nêu, kiểm synthetic/default rồi tạo checkpoint mới, không ghi đè009. Nếu chưa có nguồn unit/U/r thì giữ OPEN và chặn phần thực thi; không xem thử telemetry để chốt. Không SSH/sync khi AWS còn tạm dừng. Lệnh cuối: python -X utf8 -B results/T-054/runs/chuan-bi-re3-009/finalize.py rồi kiểm manifest009, hash protected008 và git diff --check trong phạm vi. Đề xuất commit khi Minh yêu cầu: “Chuẩn bị hợp đồng RE3, phân xử inventory và adapter trước G3”; chưa commit.

### Prompt Claude — checkpoint009

```text
'''+prompt+'```\n'
with LOG.open('a', encoding='utf-8', newline='') as f:
    f.write(end)
old = next(x for x in STATE.read_bytes().splitlines(keepends=True) if x.startswith(b'- **T-054'))
new = ('- **T-054 — checkpoint009: tiếp tục chuẩn bị RE3; cloud tạm dừng theo Minh.** Codex làm, Claude phản biện. OB đã cài/kiểm ở008;009 có inventory/schema, hợp đồng thời gian, bảng hỗ trợ và27kiểm tổng hợp. H1 units/r/U/alias còn thiếu nguồn; bản vá H2 cụ thể chờ Minh duyệt. Chưa mở telemetry RE3/G3/main. [009](../results/T-054/runs/chuan-bi-re3-009/bao-cao.md), [AWS](../results/T-054/runs/cai-ob-source-native-008/aws-loss-report.md), [LOG](../tasks/T-054-khoa-g3-chay-p7-a/LOG.md).\r\n').encode('utf-8')
STATE.write_bytes(STATE.read_bytes().replace(old, new, 1))
checkpoint.update(status='STATIC_RE3_PREPARATION_CHECKPOINTED_H1_OPEN_H2_PATCH_PENDING_APPROVAL',
                  finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  synthetic_checks_passed=27, next='Await exact H2 patch approval; obtain missing exporter/deployment declarations; no telemetry or cloud',
                  formal_review_completed=False)
save(RUN/'checkpoint.json', checkpoint)

# Full immutable008 output and source-code pins must still match.
previous = json.loads((ROOT/'results/T-054/manifest-cai-ob-source-native-008.json').read_text(encoding='utf-8'))
for rel, expected in previous['outputs'].items():
    if rel == 'docs/STATE.md':
        b = (RUN/'before-state.md').read_bytes()
        assert {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()} == expected
    elif rel == 'tasks/T-054-khoa-g3-chay-p7-a/LOG.md':
        assert hashlib.sha256(LOG.read_bytes()[:expected['bytes']]).hexdigest() == expected['sha256']
    else:
        assert pin(ROOT/rel) == expected, rel
for rel, expected in sources['files'].items():
    assert pin(ROOT/rel) == expected, rel
before_state = (RUN/'before-state.md').read_bytes()
assert STATE.read_bytes().replace(new, old, 1) == before_state
subprocess.run(['git', 'diff', '--check', '--', 'docs/STATE.md', str(LOG.relative_to(ROOT))], cwd=ROOT, check=True)
save(RUN/'validation.json', {
    'previous008_outputs_unchanged': len(previous['outputs']),
    'production_source_files_unchanged': len(sources['files']),
    'LOG_pre009_prefix_preserved': True, 'STATE_only_T054_line_changed': True,
    'synthetic_checks_PASS': 27, 'diff_check': 'PASS', 'RE3_telemetry_opened': False,
    'main_started': False, 'cloud_paused': True,
    'source_decisions_added': False, 'H1_complete': False, 'H2_implemented': False})
outputs = {str(p.relative_to(ROOT)).replace('\\', '/'): pin(p) for p in sorted(RUN.rglob('*')) if p.is_file()}
save(ROOT/'results/T-054/manifest-chuan-bi-re3-009.json', {
    'schema': 'T054-RE3-PREPARATION-009', 'status': checkpoint['status'],
    'outputs': outputs, 'previous_manifest': pin(ROOT/'results/T-054/manifest-cai-ob-source-native-008.json'),
    'mutable_checkpoint': {str(LOG.relative_to(ROOT)): pin(LOG), 'docs/STATE.md': pin(STATE)},
    'RE3_telemetry_opened': False, 'H2_implemented': False, 'main_started': False,
    'approval_question_pending': True, 'worker': 'Codex', 'reviewer': 'Claude'})
print(json.dumps({'checkpoint': '009', 'outputs': len(outputs), 'checks': 'PASS',
                  'H1': 'OPEN sources', 'H2': 'concrete patch awaiting approval', 'telemetry': False}))
