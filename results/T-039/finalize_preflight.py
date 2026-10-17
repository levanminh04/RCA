"""Bàn giao/kiểm tiền kiểm T-039; không thực hiện đề xuất đang chờ duyệt."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/T-039'
RUN = BASE / 'runs/tien-kiem-001'


def write(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    b = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(b),
            'sha256': hashlib.sha256(b).hexdigest()}


def block(text, heading):
    section = text.split(heading + '\n', 1)[1]
    return re.search(r'```text\n(.*?)\n```', section, re.S).group(1)


template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8-sig')
common = block(template, '## Prompt chung')
replacements = {
    '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>':
        'T-039; tasks/T-039-p5b-online-boutique/SPEC.md; đề xuất tại results/T-039/de-xuat-tach.md và de-xuat-tai.md/json',
    '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>': 'soát SPEC',
    '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>': 'P5; chuẩn bị G3',
    '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>':
        'Codex người làm; Claude phản biện kết quả theo lời giao hiện hành. Claude nhận lượt soát đề xuất SPEC này nếu Minh chuyển prompt',
    '<danh sách đường dẫn và git diff từ commit gốc nếu có>':
        'AGENTS.md; docs/STATE.md; SPEC.md và LOG.md T-039; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md; LOG T-036 phần phương án gốc; results/T-039/tu-ra-va-kha-thi.md, de-xuat-tach.md, de-xuat-tai.md/json. Bản trước và diff tại results/T-039/runs/tien-kiem-001/',
    '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>':
        'Không có bản REVIEW trong thư mục T-039 tại lúc soạn prompt; lịch sử lời giao và tài liệu ở LOG T-039. Với đầu vào T-036, lịch sử trong LOG và REVIEW.md của T-036',
    '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>':
        'results/T-036/manifest.json, current_run runs/kiem-r1-after-002, code/ và code-hashes.json tại run; src/do_thi_tinh/README.md và code; results/T-035/manifest.json; results/T-003/runs/final-review-003/artifact-manifest.json và nguồn T-008 theo SPEC. Kết quả tiền kiểm tại results/T-039/manifest.json và runs/tien-kiem-001/. Windows/PowerShell; Python -X utf8 -B. Đọc preflight.py trước khi cân nhắc chạy vì script tạo run; lượt soát này không tự cấp quyền tạo run',
    '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>':
        'chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC hoặc kết quả từ prompt này; không tải nguồn mới, sửa pin hoặc chạy thực nghiệm',
}
for old, new in replacements.items():
    assert old in common, old
    common = common.replace(old, new)
assert not re.search(r'<[^>]+>', common)
prompt = '\n\n'.join([common, block(template, '### Soát SPEC'),
                       block(template, '### G3 — Khóa thiết kế trước khi mở test')]) + '\n'
prompt_path = BASE / 'prompt-claude-soat-spec.txt'
if sys.argv[1] == 'prepare':
    assert not prompt_path.exists()
    prompt_path.write_text(prompt, encoding='utf-8')
    log_path = ROOT / 'tasks/T-039-p5b-online-boutique/LOG.md'
    with log_path.open('a', encoding='utf-8', newline='') as f:
        f.write('''

### Tự rà độc lập và kết thúc tiền kiểm — 16/10/2026

**Tự rà trước lịch sử:** đã đọc trực tiếp DT18/cô, MRP RQ3/RQ5/P5/P6/P9/G3, LESSONS, WHY-52/53, quyết định liên quan, mẫu SPEC, nguyên văn Prompt chung/Soát SPEC/G3 và phương án P5b gốc LOG T-036 Phiên 1. Đọc nguồn/code/manifest thật, ghi nhận xét độc lập vào results/T-039/tu-ra-va-kha-thi.md trước khi đọc REVIEW và mốc đóng T-036. Không mở kết luận soát SPEC T-039 cũ hoặc tự mở vòng phản biện. Nhánh hỗ trợ chỉ kiểm hash/inventory, không ghi file hoặc giữ vai trò phản biện chính thức.

**Diễn biến/đầu ra:** kiểm cục bộ bằng preflight.py tien-kiem-001 đạt; lưu pin từng artifact, mã hiện hành so snapshot, Git blob T-008, canonical graph list và interval. Metadata công khai chỉ được đọc trong bộ nhớ để lập đề xuất, không lưu raw response/code mới. Bảng đề xuất có toàn cây với action đọc/loại trừ, từng URL/blob/byte và nhóm nguồn, không được gọi là inventory ứng dụng đã khảo sát. Quan sát máy là capacity snapshot, không đo hiệu năng cùng việc nặng khác. Không chạy build/compare/RCA, không đọc raw telemetry/Weight/Node values/test/heldout/archive.

**Nhận xét độc lập:** pin/hash T-036 đạt; miền graph hiện hành đã xác định. Registry gọi revision Nezha là tree object, API Git commits chứng minh là commit với tree canonical có cùng thành viên snapshot. Chặn suy luận từ loại object cũ; không có mismatch nội dung và không đổi pin. Revision ứng dụng/dataset/image/deployment, độc lập nguồn phụ và nghĩa host vẫn OPEN. Chưa có căn cứ cam kết toàn SPEC một phiên; dự toán phân rã, phương án tách và ảnh hưởng từng file ở các đề xuất. Không tự sửa SPEC hoặc giảm tiêu chí. Đây là tự rà người làm, chưa là REVIEW chính thức hoặc nhiệm thu.

**Quyết định của Minh trong phiên:** nguyên lời giao ở đầu Phiên 2; triển khai có điều kiện và quyền ghi đúng scope. Chưa có quyết định tải nguồn, sửa registry/pin, tách task hoặc chọn P6. Trình lưu chính thức nguyên ý sau khi Minh quyết, không ghi DECISIONS/WHY bằng quyền này.

**Báo cáo kết thúc:**
1. Đã hoàn tất tiền kiểm và phần độc lập có nguồn hợp lệ: quyền/nguồn, pin/hash, graph inventory, đọc API/code analysis liên quan, đề xuất tải/chi phí/tách và bàn giao. Chưa đạt đầu ra khảo sát/bản ghi/mapping/graph/đối chiếu/phân tích của toàn SPEC. Chưa trả lời RQ3/RQ5 hoặc đóng P5b/G3.
2. File ghi: results/T-039/ (tất cả path trong manifest); chỉ nối LOG này; chỉ dòng T-039 trong STATE. Không sửa SPEC, REVIEW, DECISIONS, WHY, src hoặc T-035/T-036/platform/task khác. Giữ toàn thay đổi có sẵn; không commit/push.
3. Kiểm: toàn 187 artifact T-036, code-hashes/snapshot/current code, nguồn T-008 theo manifest cuối T-003, Git blob nguồn và toàn 132 graph hiện hành khớp; canonical path khớp. JSON input-verification/graph-inventory là bằng chứng số. Không chạy pilot hoặc thí nghiệm ứng dụng. Kiểm cuối manifest/protected hash/prefix LOG/dòng STATE/prompt/số đề xuất bằng finalize_preflight.py verify; kết quả ở final-verification.json.
4. OPEN/bị ảnh hưởng: phạm vi một phiên, tải nguồn cụ thể, cách xử lý mô tả loại object; chưa nối deployment, chưa chứng minh coverage/alias/nguồn phụ/Node. Owner nguồn thiếu: tác giả Nezha/application deployment cho build/image/export schema; Minh quyết cấp nguồn/tách; người làm khảo sát/đối chiếu sau duyệt. T-040/P6/P9 không được nhận số khớp hoặc kết luận thiếu telemetry từ tiền kiểm này. Nội dung nên vào báo cáo: loại object/revision, điều kiện đối chiếu, miền adapter, coverage nguồn và giới hạn độc lập.
5. Bước tiếp chính xác: Minh đọc results/T-039/tu-ra-va-kha-thi.md, de-xuat-tach.md, de-xuat-tai.md/json; quyết tải, tổ chức task và cách xử lý metadata chung. Chưa chạy tải từ đề xuất. Sau duyệt phạm vi cụ thể, lập/sửa SPEC theo quyền riêng nếu chọn tách; nếu chỉ duyệt tải thì chỉ thu nguồn đúng danh sách, không tự sửa task/pin. Muốn tiếp từ pin cũ: kiểm lại results/T-036/manifest.json và code snapshot trước phần phụ thuộc; dừng khi lệch. Lệnh đọc: Get-Content -Raw -LiteralPath 'results/T-039/de-xuat-tai.md'.
6. Lệnh cuối dự kiến của lượt này và bước kiểm cuối: py -3 -X utf8 -B results/T-039/finalize_preflight.py verify. Lệnh có ghi kết quả chỉ trong results/T-039; không gọi preflight trên tên run cũ. Sau kiểm chỉ báo lại, không mutation khác trong repo.

**Đề xuất commit, chưa thực hiện:** docs: record T-039 preflight and source acquisition proposal. Không commit/push khi chưa có Minh duyệt riêng.

### Prompt Claude — soát đề xuất SPEC (Minh chọn chuyển thủ công)

```text
''')
        f.write(prompt)
        f.write('```\n')
    print('Prepared neutral prompt and appended LOG; no source acquisition or SPEC change.')
elif sys.argv[1] == 'verify':
    protected = json.loads((RUN / 'protected-before.json').read_text(encoding='utf-8'))
    assert all(digest(ROOT / p['path']) == p for p in protected)
    assert prompt_path.read_text(encoding='utf-8') == prompt
    before_log = (RUN / 'LOG-before.md').read_bytes()
    after_log = (ROOT / 'tasks/T-039-p5b-online-boutique/LOG.md').read_bytes()
    assert after_log.startswith(before_log)
    assert after_log.count(prompt.encode('utf-8')) == 1
    before_state = (RUN / 'STATE-before-our-write.md').read_bytes()
    after_state = (ROOT / 'docs/STATE.md').read_bytes()
    old_lines, new_lines = before_state.splitlines(keepends=True), after_state.splitlines(keepends=True)
    assert len(old_lines) == len(new_lines)
    changed = [(i + 1, a, b) for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
    assert len(changed) == 1 and changed[0][1].startswith(b'| T-039 |') and changed[0][2].startswith(b'| T-039 |')
    proposal = json.loads((BASE / 'de-xuat-tai.json').read_text(encoding='utf-8'))
    selected = [e for e in proposal['whole_tree_proposal'] if e['action'] == 'proposed_fetch']
    excluded = [e for e in proposal['whole_tree_proposal'] if e['action'] == 'exclude_no_fetch']
    assert len(proposal['whole_tree_proposal']) == 274 and len(selected) == 215 and len(excluded) == 4
    assert sum(e['size'] for e in selected) == proposal['ob_selection']['source_payload_bytes']
    assert sum(e['size'] for e in excluded) == proposal['ob_selection']['excluded_payload_bytes']
    assert sum(e['size'] for e in proposal['nezha_selection']['files']) == proposal['nezha_selection']['expected_payload_bytes']
    assert sum(e['observed_body_bytes'] for e in proposal['metadata_to_fetch_after_approval']) == 422197
    assert proposal['costs']['proposed_body_payload_bytes'] == 37524834
    assert not (BASE / 'sources').exists()
    import difflib
    diff = ''.join(difflib.unified_diff(before_state.decode('utf-8-sig').splitlines(True),
                    after_state.decode('utf-8-sig').splitlines(True), fromfile='before/STATE.md', tofile='after/STATE.md'))
    diff += ''.join(difflib.unified_diff(before_log.decode('utf-8-sig').splitlines(True),
                    after_log.decode('utf-8-sig').splitlines(True), fromfile='before/LOG.md', tofile='after/LOG.md'))
    (RUN / 'changes.diff').write_text(diff, encoding='utf-8')
    write('results/T-039/runs/tien-kiem-001/final-verification.json', {
        'all_ok': True, 'protected_files_unchanged': len(protected), 'log_append_only': True,
        'state_only_task_row': True, 'neutral_prompt_matches_template': True,
        'proposal_sum_checks': True, 'no_new_sources_saved': True,
        'log': digest(ROOT / 'tasks/T-039-p5b-online-boutique/LOG.md'),
        'state': digest(ROOT / 'docs/STATE.md'), 'last_command': 'py -3 -X utf8 -B results/T-039/finalize_preflight.py verify'})
    files = [digest(p) for p in sorted(BASE.rglob('*')) if p.is_file() and p != BASE / 'manifest.json']
    write('results/T-039/manifest.json', {'task': 'T-039',
        'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'status': 'PRECHECK_ONLY_AWAITING_MINH_DECISION', 'current_run': 'runs/tien-kiem-001',
        'shared_pin_changed': False, 'decisions_added': [], 'count': len(files), 'files': files,
        'excludes': 'manifest itself; LOG and STATE hashes are in final-verification.json',
        'science_status': 'No application inventory/mapping/build/comparison completed; RQ3/RQ5/G3 OPEN'})
    assert all(digest(ROOT / e['path']) == e for e in files)
    print(json.dumps({'all_ok': True, 'manifest_count': len(files), 'protected_unchanged': len(protected),
                      'state_row': changed[0][0], 'no_new_source_saved': True}))
else:
    raise ValueError('use prepare or verify')
