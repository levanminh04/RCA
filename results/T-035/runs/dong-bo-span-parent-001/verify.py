"""Verify the approved documentation-only correction and publish its manifest."""
from pathlib import Path
from datetime import datetime, timezone
import difflib
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
REL = RUN.relative_to(ROOT).as_posix()
sys.path.insert(0, str(ROOT / 'src'))
import pandas as pd
from do_thi.builder import build, project


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, stderr=subprocess.DEVNULL)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def create(path, data):
    raw = data if isinstance(data, bytes) else data.encode('utf-8')
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_bytes() == raw, f'Do not overwrite {path}'
        return
    with path.open('xb') as stream:
        stream.write(raw)


def dump(path, value):
    create(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


pre = read(RUN / 'preflight.json')
allowed = set(pre['write_files'])
previous = read(RUN / 'before/results/T-035/manifest.json')
model_rel = 'results/T-035/dac-ta-do-thi.md'
log_rel = 'tasks/T-035-p5-do-thi-tu-trace/LOG.md'

# Literal examples target both sides of the messaging-kind condition and controls.
examples = [
    ('producer_child', 'B', 'INTERNAL', 'PRODUCER', 'span-parent', 0),
    ('consumer_parent', 'B', 'CONSUMER', 'INTERNAL', 'span-parent', 0),
    ('producer_parent', 'B', 'PRODUCER', 'INTERNAL', 'span-parent', 0),
    ('ordinary_cross_owner', 'B', 'INTERNAL', 'INTERNAL', 'gọi-chưa-phân-kiểu', 1),
    ('client_server', 'B', 'CLIENT', 'SERVER', 'gọi-đồng-bộ', 1),
    ('consumer_same_owner', 'A', 'CONSUMER', 'INTERNAL', 'span-parent', 0),
]
replays = []
for name, owner, parent_kind, child_kind, edge_type, entity_count in examples:
    frame = pd.DataFrame([
        dict(traceID='T', spanID='p', parentSpanID='', serviceName='A', operationName='root', startTime=0, duration=10, kind=parent_kind),
        dict(traceID='T', spanID='c', parentSpanID='p', serviceName=owner, operationName='publish', startTime=1, duration=2, kind=child_kind),
    ])
    entity, operation = build(frame, None, {}, {'A': 'service', 'B': 'service'})
    assert {n['id'] for n in entity['nodes']} == {'A', owner}
    assert len(operation['edges']) == 1
    edge = operation['edges'][0]
    assert edge['source'] == '["A","root"]'
    assert edge['target'] == ('["A","publish"]' if owner == 'A' else '["B","publish"]')
    assert edge['type'] == edge_type
    assert len(entity['edges']) == entity_count
    if entity_count:
        assert [(e['source'], e['target'], e['type']) for e in entity['edges']] == [('A', 'B', edge_type)]
    assert entity['stats']['cross_entity_parent_events'] == int(owner != 'A')
    nodes, projected = project(operation)
    assert nodes == {'A', owner} and len(projected) == entity_count
    replays.append({
        'name': name, 'pass': True,
        'expected_operation_edge': edge_type, 'expected_entity_edges': entity_count,
        'entity_nodes': sorted(nodes), 'entity_edges': entity['edges'],
        'operation_edges': operation['edges'],
        'cross_entity_parent_events': entity['stats']['cross_entity_parent_events'],
    })
dump(RUN / 'replay.json', {'mode': 'in_memory', 'builder_unchanged': True, 'pass': len(replays), 'cases': replays})

model = (ROOT / model_rel).read_text(encoding='utf-8')
assert 'Loại mọi cạnh span-parent, kể cả giữa hai thao tác khác chủ quản' in model
assert '- span-parent: cặp span cha–con tìm được trong cùng khoảng' in model
assert 'không thay thế cây span gốc' in model
assert '- gọi-chưa-phân-kiểu: các cặp cha–con còn lại sau khi loại gọi đồng bộ và span-parent' in model
assert 'cross_entity_parent_events đếm mọi cặp span cha–con khác chủ quản' in model
assert 'chiếu mọi cạnh giữa hai thao tác khác chủ quản thành cạnh thực thể' not in model
assert '- gọi-chưa-phân-kiểu: cặp còn lại;' not in model
for name, old_hash in pre['source_hashes'].items():
    assert sha((ROOT / name).read_bytes()) == old_hash, name

# Check the generated prompts against the exact present template.
template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8')
fence = '`' * 3
def block(heading):
    return template[template.index(heading):].split(fence + 'text', 1)[1].split(fence, 1)[0].strip('\n')
base_common = block('## Prompt chung')
stage = block('### Soát kết quả')
gate = block('### G3 — Khóa thiết kế trước khi mở test')
prompt_receipt = read(RUN / 'prompt-template-check.json')
prompt_data = {}
for filename in ['prompt-codex-sach-soat-t035.txt', 'prompt-claude-soat-ket-qua.txt']:
    raw = (RUN / filename).read_bytes()
    prompt = raw.decode('utf-8')
    assert sha(raw) == prompt_receipt['prompt_files'][filename]
    assert stage in prompt and gate in prompt
    common = prompt[prompt.index('Bạn thực hiện một lượt đánh giá độc lập'):].split('\n\nCông đoạn: soát kết quả.')[0]
    old_lines, actual_lines = base_common.splitlines(), common.splitlines()
    assert len(old_lines) == len(actual_lines)
    for old, actual in zip(old_lines, actual_lines):
        if re.search(r'<[^>]+>', old):
            assert actual.startswith(old.split('<', 1)[0]) and not re.search(r'<[^>]+>', actual)
        else:
            assert old == actual, (old, actual)
    metadata = common.split('Thông tin lượt này:', 1)[1].split('\n\nKhông sửa ngoài', 1)[0]
    for forbidden in ['span-parent', 'Q-156', '5641', '129/129', 'N1 —', 'đã đạt', 'không còn lỗi']:
        assert forbidden not in metadata, (filename, forbidden)
    assert 'chỉ đọc và trả lời trong chat' in metadata
    prompt_data[filename] = prompt

# The original artifact contents are preserved except the approved specification.
changed_old_artifacts = []
for entry in previous['files']:
    path = ROOT / entry['path']
    assert path.is_file(), str(path)
    if sha(path.read_bytes()) != entry['sha256']:
        changed_old_artifacts.append(entry['path'])
assert changed_old_artifacts == [model_rel], changed_old_artifacts

# Final report and both prompts are appended to this worker's LOG.
log = (ROOT / log_rel).read_bytes()
old_log = (RUN / 'before' / log_rel).read_bytes()
assert log.startswith(old_log)
marker = '**Kết thúc Phiên 9 — đồng bộ văn bản:**'
if marker not in log.decode('utf-8'):
    ending = f'''
{marker}

1. **Đã làm:** làm rõ span-parent ở mục 1/3 của đặc tả v2.1: điều kiện tạo, phạm vi giữ quan hệ đã gộp ở mức thao tác, ngoại lệ phép chiếu kể cả khác chủ quản; thu hẹp gọi chưa phân kiểu; giải thích số đếm cặp cha–con khác chủ quản. Không đổi hành vi bộ dựng. Quyết định Q-156 và lý do đã ghi trước sửa đặc tả.
2. **File:** đúng sáu file ngoài thư mục lượt trong preflight.json: đặc tả, WHY, DECISIONS, LOG, dòng T-035 trong STATE, manifest; đầu ra mới chỉ dưới {REL}/. Giữ mọi bản trước và mọi lượt; không sửa SPEC/code/baseline/FlashTicket, không mở test hoặc commit/push.
3. **Kiểm:** mọi artifact ở manifest trước khớp trước sửa; sau sửa chỉ đặc tả được đổi trong tập artifact cũ. Sáu trường hợp nhỏ trong replay.json khớp đích literal/cạnh/phép chiếu và cross_entity_parent_events. Hash code/báo cáo kiểm/script sinh tài liệu/SPEC/luật giữ nguyên. Kiểm văn bản không còn hai câu quy tắc quá rộng; prompt chép nguyên văn khối chung/công đoạn/G3, chỉ điền metadata trung tính. Không chạy lại dev. Kiểm diff/phạm vi, nối thêm và manifest ở verify.py/final-verification.json.
4. **Mức trả lời nguồn / còn mở:** xử lý mâu thuẫn văn bản đã trình; không tự xác nhận toàn task không còn lỗi hoặc đã đầy đủ quan sát. Kết quả dev đã kiểm được giữ, chưa thêm bằng chứng RCA mới. Nghĩa vật lý cạnh, Node=host, nguồn metadata ngày, kiến trúc tĩnh, trace FlashTicket thật và hiệu quả thiết kế tiếp tục theo các nơi nhận T-036/P6/P9; chưa chọn P6 hoặc đóng T-035/P5/G3/RQ3. Chờ Codex sạch soát toàn task như lần đầu, sau đó phản biện chính thức/Minh quyết.

**Quyết định Minh trong phiên:** lời duyệt nguyên văn và quyền ở Q-156/minh-duyet.txt. Không có quyết định mới về phương pháp hoặc hiệu quả RCA.

**Lượt kiểm dừng được giữ:** apply_docs-attempt-001.py dừng trước preflight và trước sửa tài liệu vì băm nội dung toàn bộ file tracked ngoài T-035 tốn I/O không cần thiết. attempt-001-status.json ghi trạng thái. Bản áp dụng dùng manifest T-035, hash nguồn trực tiếp, tập đường dẫn git và diff ngoài phạm vi để bảo toàn thay đổi có trước; không tạo cổng hay quy trình mới.

**Bước tiếp theo chính xác:** Minh mở phiên Codex mới tại D:/RCA-flashticket và dán nguyên file prompt-codex-sach-soat-t035.txt trong lượt này. Chỉ dán prompt, không dán thêm danh sách finding/kết luận để định hướng. Phiên mới đọc AGENTS, nguồn, SPEC, hợp đồng, code và dữ liệu gốc được phép, ghi nhận xét độc lập trong chat rồi mới đối chiếu lịch sử. Đây là tự soát của người làm; Claude vẫn phản biện chính thức. Không tự mở/gửi phiên. Prompt Claude bên dưới để Minh chọn chuyển thủ công.

**Lệnh cuối / tái lập phép kiểm:** & 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B {REL}/verify.py. Không chạy lại apply_docs.py hoặc lượt dev cũ. Các bản trước ở before/, bản sau ở after/, diff ở changes.diff, phép phát lại ở replay.json, biên nhận kết thúc ở final-verification.json. Đầu ra hợp lệ dùng lại; không tạo run mới chỉ vì đổi máy.

**Đề xuất commit, chưa thực hiện:** docs: clarify span-parent projection in T-035; chỉ phạm vi đã duyệt của lượt này, giữ mọi thay đổi có trước. Commit/push chờ Minh duyệt riêng.

### Prompt Codex sạch — soát toàn bộ T-035

```text
{prompt_data['prompt-codex-sach-soat-t035.txt'].rstrip()}
```

### Prompt Claude — soát kết quả

```text
{prompt_data['prompt-claude-soat-ket-qua.txt'].rstrip()}
```
'''
    nl = '\r\n' if b'\r\n' in log else '\n'
    with (ROOT / log_rel).open('ab') as stream:
        stream.write((nl + ending.replace('\n', nl)).encode('utf-8'))

# Preserve the user's other tracked changes and untracked file set.
head = git('rev-parse', 'HEAD').decode().strip()
assert head == pre['head_before']
outside_diff = git('diff', '--no-ext-diff', 'HEAD', '--', '.', *[':(exclude)' + name for name in allowed])
assert sha(outside_diff) == pre['outside_tracked_diff_sha256']
tracked = [x.decode('utf-8') for x in git('ls-files', '-z').split(b'\0') if x]
assert tracked == pre['tracked_paths']
untracked = [x.decode('utf-8') for x in git('ls-files', '--others', '--exclude-standard', '-z').split(b'\0') if x]
outside_untracked = sorted(name for name in untracked if name not in allowed and not name.startswith(REL + '/'))
assert outside_untracked == pre['outside_untracked_paths']
for name in ['docs/WHY.md', 'docs/DECISIONS.md', log_rel]:
    assert (ROOT / name).read_bytes().startswith((RUN / 'before' / name).read_bytes()), name
old_state = (RUN / 'before/docs/STATE.md').read_bytes()
new_state = (ROOT / 'docs/STATE.md').read_bytes()
old_row = next(x for x in old_state.splitlines() if x.startswith(b'| T-035 |'))
new_row = next(x for x in new_state.splitlines() if x.startswith(b'| T-035 |'))
assert new_state.replace(new_row, old_row, 1) == old_state
assert b'Q-156' in new_row
check = subprocess.run(['git', 'diff', '--check', '--', *sorted(allowed)], cwd=ROOT, capture_output=True)
new_errors = set(check.stdout.decode('utf-8', errors='replace').splitlines()) - set(pre['git_diff_check_before'].splitlines())
assert not new_errors, sorted(new_errors)

diffs = []
for name in pre['write_files']:
    if name.endswith('/manifest.json'):
        continue
    before = (RUN / 'before' / name).read_bytes()
    after = (ROOT / name).read_bytes()
    create(RUN / 'after' / name, after)
    diffs.extend(difflib.unified_diff(before.decode('utf-8').splitlines(keepends=True), after.decode('utf-8').splitlines(keepends=True), fromfile='before/' + name, tofile='after/' + name))
create(RUN / 'changes.diff', ''.join(diffs))
verification = {
    'status': 'PASS', 'task': 'T-035', 'decision': 'Q-156',
    'mode': 'documentation_only', 'builder_and_dev_outputs_unchanged': True,
    'old_artifacts_checked': len(previous['files']),
    'changed_old_artifacts': changed_old_artifacts,
    'in_memory_examples_passed': len(replays),
    'outside_tracked_diff_preserved': True, 'outside_untracked_paths_preserved': True,
    'append_only': ['docs/WHY.md', 'docs/DECISIONS.md', log_rel],
    'state_only_T035_row': True, 'head_unchanged': head,
    'source_hashes': pre['source_hashes'],
    'document_hashes': {name: sha((ROOT / name).read_bytes()) for name in pre['write_files'] if not name.endswith('/manifest.json')},
    'prompt_template_verbatim': True, 'prompt_scope': 'read_only_chat',
    'full_dev_rerun': False, 'open_test_heldout': False,
    'commit_push': False, 'threads_created_or_messaged': False,
    'formal_reviewer': 'Claude', 'task_accepted_or_closed': False,
    'previous_full_verification': previous.get('final_verification'),
}
dump(RUN / 'final-verification.json', verification)

# No circular manifest reference: the manifest does not include itself.
files = []
for directory in [ROOT / 'results/T-035', ROOT / 'src/do_thi']:
    for path in sorted(directory.rglob('*')):
        if not path.is_file() or path == ROOT / 'results/T-035/manifest.json':
            continue
        if '__pycache__' in path.parts or path.suffix == '.pyc':
            continue
        raw = path.read_bytes()
        if path.suffix == '.json':
            json.loads(raw.decode('utf-8-sig'))
        files.append({'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)})
files.sort(key=lambda item: item['path'])
manifest = dict(previous)
manifest.update({
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'files': files, 'artifact_count': len(files), 'total_bytes': sum(x['bytes'] for x in files),
    'scope': pre['write_files'] + [REL + '/'],
    'final_verification': REL.removeprefix('results/T-035/') + '/final-verification.json',
    'previous_full_verification': previous.get('final_verification'),
    'previous_manifest': REL.removeprefix('results/T-035/') + '/before/results/T-035/manifest.json',
    'task_state': 'awaiting_fresh_codex_self_audit_and_official_review',
    'pending_doc_sync': False, 'open_test_heldout': False, 'commit_push': False,
    'documentation_decisions_added': ['Q-156'],
    'scientific_decisions_added': [],
})
(ROOT / 'results/T-035/manifest.json').write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
for entry in files:
    assert sha((ROOT / entry['path']).read_bytes()) == entry['sha256'], entry['path']
assert git('rev-parse', 'HEAD').decode().strip() == pre['head_before']
print(json.dumps({'status': 'PASS', 'artifacts': len(files), 'in_memory_examples': len(replays), 'code_and_dev_unchanged': True, 'prompt': REL + '/prompt-codex-sach-soat-t035.txt'}, ensure_ascii=False))
