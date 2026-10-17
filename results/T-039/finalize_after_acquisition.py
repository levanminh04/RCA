"""Chốt checkpoint sau thu; không nghiệm thu hoặc triển khai phần chưa qua khả thi."""
from pathlib import Path
import ast
import datetime as dt
import difflib
import hashlib
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/T-039'
RUN = BASE / 'runs/ket-sau-tai-001'


def digest(p):
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if sys.argv[1] == 'prepare':
    RUN.mkdir(parents=True, exist_ok=False)
    for name in ['manifest.json', 'ban-giao.md', 'kiem-dung-dan.md']:
        shutil.copyfile(BASE / name, RUN / ('truoc-ket-' + name))
    # Giữ các khối chuẩn; chỉ thay thông tin trung tính tại các trường điền.
    prompt = (BASE / 'prompt-claude-soat-spec.txt').read_text(encoding='utf-8')
    prompt = prompt.replace(
        'đề xuất tại results/T-039/de-xuat-tach.md và de-xuat-tai.md/json',
        'đề xuất tại results/T-039/de-xuat-tach.md; tài liệu hiện hành tại bao-cao-sau-tai.md, authorization-20261016.json và LOG Phiên 2')
    prompt = prompt.replace('results/T-039/tu-ra-va-kha-thi.md, de-xuat-tach.md, de-xuat-tai.md/json.',
        'results/T-039/tu-ra-va-kha-thi.md, bao-cao-sau-tai.md, authorization-20261016.json, de-xuat-tach.md, de-xuat-tai.md/json.')
    prompt = prompt.replace('Kết quả tiền kiểm tại results/T-039/manifest.json và runs/tien-kiem-001/.',
        'Kết quả tại results/T-039/manifest.json, nguon.json, runs/tien-kiem-001/, runs/thu-nguon-001/, runs/khao-sat-nguon-001/ và sources/ theo acquisition.json.')
    (BASE / 'prompt-claude-sau-tai.txt').write_text(prompt, encoding='utf-8')
    (BASE / 'ban-giao.md').write_text('''# Bàn giao T-039 sau thu nguồn — 16/10/2026

**Task chưa hoàn tất.** Đã tự rà, kiểm pin/input, thu đúng nguồn Minh duyệt và xét lại khả thi. Minh giữ toàn phạm vi T-039; chưa có ngoại lệ thực hiện qua nhiều phiên hoặc quyết định tách. Không lập bản ghi/mapping/graph/đối chiếu, không nghiệm thu hoặc đóng G3.

Đọc `bao-cao-sau-tai.md` trước; nguyên lời Minh ở LOG Phiên 2 và `authorization-20261016.json`. Bản tự rà/proposal trước duyệt tải giữ nguyên mốc lịch sử, không còn là hiện trạng quyền tải. Bản bàn giao trước thu được giữ tại `runs/ket-sau-tai-001/truoc-ket-ban-giao.md`.

Nguồn đã đủ đúng danh sách, hash byte/Git blob/SHA256 đạt. Danh sách/capture ở `runs/thu-nguon-001/acquisition.json`; kiểm lại và profile ở `runs/khao-sat-nguon-001/`. Profile chỉ đếm/scan, chưa là semantic coverage. Registry `nguon.json` ghi đính chính commit→tree riêng tại T-039 theo Minh; pin và registry T-036 nguyên byte.

Còn phải làm đủ SPEC: coverage từng phần của toàn cây và nguồn gián tiếp; bản ghi/owner/provenance/điều kiện; oracle riêng trước code; mapping từ nguồn; dựng/chiếu/đối chiếu mọi graph hiện hành ở hai mức và hai views; lần theo nhóm mismatch và match tương ứng; tự kiểm/chi phí/bàn giao P6/P9. Generated/đăng ký handler, hai biến thể deployment và backend Cart phải được phân biệt. Revision ứng dụng→dataset/image/deployment, producer metadata và nghĩa Node/host vẫn OPEN. Không dùng nguồn cùng pipeline như xác nhận độc lập.

Bước tiếp phụ thuộc Minh: cho phép giữ task qua nhiều phiên, hoặc chọn tách và duyệt SPEC cụ thể trước sửa. Chọn giữ toàn phạm vi để xem lại khả thi sau nguồn chưa tự là ngoại lệ AGENTS §5. Không giảm phân tích để vừa một phiên; không tự chia mã task. Các nguồn tải đã được duyệt không cần xin lại.

Lệnh đọc tiếp: `Get-Content -Raw -LiteralPath 'results/T-039/bao-cao-sau-tai.md'`. Trước dùng số/source, kiểm manifest T-039 và pin T-036/T-035 từ input-verification.json. Không chạy lại script thu/prepare trên run cũ. Chưa cài gói, chạy code ứng dụng, baseline/RCA, mở dữ liệu khóa hoặc commit/push.

Prompt chung + Soát SPEC + G3 trung tính ở `prompt-claude-sau-tai.txt` và cuối LOG; Minh chọn gửi hay dừng, không tự mở lượt review mới. Đề nghị lưu nguyên ba quyết định đã nhận vào DECISIONS theo `de-nghi-ghi-quyet-dinh.md`; chưa có quyền sửa file chung. Nội dung formal report hiện chỉ là provenance, miền và các giới hạn, chưa phải độ khớp hoặc lợi ích RCA.
''', encoding='utf-8')
    with (BASE / 'kiem-dung-dan.md').open('a', encoding='utf-8') as f:
        f.write('''

## Kiểm sau thu theo Minh duyệt — 16/10/2026

`runs/thu-nguon-001/acquisition.json`: 223 file nguồn, sáu metadata; 37.524.834 byte payload thực; tất cả Git blob/byte khớp, không có lỗi. `runs/khao-sat-nguon-001/integrity.json`: 229/229 SHA256/byte khớp sau thu. Declaration count và JAR metadata được kiểm độc lập để xét khối lượng; không là semantic inventory hoặc runtime evidence. Không có graph/mapping T-039 đã dựng.

Đã đối chiếu các ví dụ nguồn chính về biến thể deployment, dependency MySQL/Redis có điều kiện, generated khác proto/registration và NodeName chưa nối Node dataset. Các số và locator ở bao-cao-sau-tai.md, không nhận phát biểu của nhánh hỗ trợ là quyết định hoặc bằng chứng coverage toàn snapshot.

Kiểm cuối checkpoint: `py -3 -X utf8 -B results/T-039/finalize_after_acquisition.py verify`. Kiểm nguồn đã thu, proposal đã duyệt, pin/SPEC/nguồn bảo vệ, LOG append-only, STATE chỉ dòng task, prompt nguyên văn và manifest toàn file. Kết quả ở runs/ket-sau-tai-001/final-verification.json. Không chạy lại script preflight cũ sau thu vì điều kiện no-sources của nó là mốc trước cấp quyền tải.
''')
    log = ROOT / 'tasks/T-039-p5b-online-boutique/LOG.md'
    with log.open('a', encoding='utf-8', newline='') as f:
        f.write('''

### Checkpoint sau thu nguồn và xét lại khả thi — 16/10/2026

**Quyết định hiện hành:** giữ nguyên ba câu trả lời Minh đã nối ở trên. Đã dùng quyền tải đúng danh sách; giữ toàn phạm vi T-039, không tự sửa SPEC/tách hoặc đổi pin. Đính chính loại object ghi trong registry riêng results/T-039/nguon.json; registry chung không đổi. Việc ghi DECISIONS cần quyền riêng, nội dung đề nghị ở de-nghi-ghi-quyet-dinh.md.

**Diễn biến:** chạy acquire_sources.py thu-nguon-001; thu xong 223 file nguồn/sáu metadata, tất cả size/Git blob khớp, payload 37.524.834 byte, không lỗi. Không tải bốn log thô hoặc nguồn ngoài; không clone/cài gói/build/image. Sau đó post_acquisition_audit.py khao-sat-nguon-001 kiểm lại 229 hash và lưu profile/declaration/JAR metadata; không chạy code nguồn hoặc dựng graph. Hai nhánh hỗ trợ chỉ đọc source trong phạm vi phân công, không phản biện chính thức; root đối chiếu đoạn nguồn quan trọng trước ghi báo cáo.

**Kết quả sau nguồn:** có biến thể deployment cùng tên, Cart Redis/local, adservice MySQL, generated không đồng nhất proto chung và tên span nội bộ; không thể rút gọn thành cây+proto. Chưa có producer metadata hoặc cầu nối NodeName→Node dataset trong phần nguồn đã đọc; chưa xác minh app/image/deployment sinh dataset. Profile UTF-8/ZIP không đồng nghĩa semantic coverage. Báo cáo có locator/phần đã đọc/chưa đọc và owner bằng chứng thiếu. Không lập mapping, tối ưu alias hoặc quy nguyên nhân cho ca dataset từ các ví dụ này.

**Kết thúc lượt/checkpoint:**
1. Đã hoàn tất đúng thu nguồn được duyệt và phần kiểm/đọc để xét lại khả thi; đầu vào đã sẵn cho khảo sát tiếp. Chưa đạt toàn tiêu chí bản ghi/graph/đối chiếu/phân tích của SPEC; chưa trả lời RQ3/RQ5/G3 hoặc đóng P5b. Điều kiện một phiên chưa có căn cứ xác nhận; dự toán còn lại CANDIDATE 6–10,5 giờ công, không giảm kiểm. Minh chưa duyệt ngoại lệ nhiều phiên; giữ toàn task không tự là ngoại lệ. Trình quyết định cách tiếp tục, không tự chia task.
2. File ghi chỉ results/T-039/, nối LOG này và dòng T-039 của STATE. Manifest cuối liệt kê toàn file; bản trước/nguồn đã thu/lượt kiểm được giữ. Không sửa SPEC, src, WHY/DECISIONS/REVIEW hoặc T-035/T-036/platform/task khác; không commit/push.
3. Kiểm: tiền kiểm 187 artifact T-036 và 132 graph hiện hành khớp; thu nguồn size/blob/SHA256 đạt; kiểm sau thu 229/229; tổng declaration và profile có JSON; kiểm cuối scope/hash/prefix/prompt/manifest ở runs/ket-sau-tai-001/final-verification.json. Giờ thu thực không là benchmark độc quyền; peak RAM lượt thu chưa đo, không suy lại. Chưa chạy pilot toàn pipeline hoặc tự kiểm graph/mapping chưa tồn tại.
4. OPEN và quyết định phụ thuộc: khả thi một phiên/cách tiếp tục do Minh; semantic coverage/owner/alias/generated/nhánh do người làm phải hoàn thành; deployment/image/producer metadata/export schema do tác giả/nguồn có provenance, Minh quyết quyền bổ sung nếu cần. T-040/P6/P9 chưa được nhận graph hoặc kết luận thiếu telemetry/host từ gói này. Formal report chỉ dùng provenance/miền/giới hạn đã kiểm, không số khớp hoặc lợi ích RCA.
5. Bước tiếp chính xác: đọc results/T-039/bao-cao-sau-tai.md và ban-giao.md; Minh quyết ngoại lệ giữ task qua nhiều phiên hoặc tách với SPEC cụ thể. Nếu được tiếp, kiểm toàn manifest T-039 và các pin input trước dùng; hoàn tất coverage nguồn trước bản ghi, viết oracle literal trước code riêng rồi dựng/đối chiếu theo SPEC nguyên phạm vi. Không cần tải lại nguồn đã hợp lệ. Lệnh đọc: Get-Content -Raw -LiteralPath 'results/T-039/bao-cao-sau-tai.md'.
6. Lệnh cuối sau cập nhật dòng STATE và kiểm toàn diff: py -3 -X utf8 -B results/T-039/finalize_after_acquisition.py verify. Không ghi thêm sau kiểm; nếu cần sửa, phải kiểm lại và giữ lịch sử. Đề xuất commit chưa thực hiện: docs: record T-039 approved sources and feasibility checkpoint.

### Prompt Claude sau thu — Minh chọn gửi hoặc dừng

```text
''')
        f.write(prompt)
        f.write('```\n')
    print('Prepared post-acquisition checkpoint and neutral handoff; SPEC/pin unchanged.')
elif sys.argv[1] == 'verify':
    assert RUN.is_dir() and not (RUN / 'final-verification.json').exists()
    protected = json.loads((BASE / 'runs/tien-kiem-001/protected-before.json').read_text(encoding='utf-8'))
    assert all(digest(ROOT / r['path']) == r for r in protected)
    auth = json.loads((BASE / 'authorization-20261016.json').read_text(encoding='utf-8'))
    assert digest(BASE / 'de-xuat-tai.json')['sha256'] == auth['approved_proposal_sha256']
    a = json.loads((BASE / 'runs/thu-nguon-001/acquisition.json').read_text(encoding='utf-8'))
    expected_sources = {e['path'] for e in a['files'] + a['metadata']}
    actual_sources = {p.relative_to(ROOT).as_posix() for p in (BASE / 'sources').rglob('*') if p.is_file()}
    assert expected_sources == actual_sources and len(actual_sources) == 229
    for e in a['files'] + a['metadata']:
        assert digest(ROOT / e['path']) == {k: e[k] for k in ['path', 'bytes', 'sha256']}
    assert not any(p.endswith('/log.csv') for p in actual_sources)
    for p in BASE.rglob('*.json'):
        json.loads(p.read_text(encoding='utf-8-sig'))
    for p in BASE.glob('*.py'):
        ast.parse(p.read_text(encoding='utf-8'))
    old_log = (BASE / 'runs/tien-kiem-001/LOG-before.md').read_bytes()
    log_path = ROOT / 'tasks/T-039-p5b-online-boutique/LOG.md'
    assert log_path.read_bytes().startswith(old_log)
    old_state = (RUN / 'STATE-before-our-write.md').read_bytes()
    state_path = ROOT / 'docs/STATE.md'
    new_state = state_path.read_bytes()
    before, after = old_state.splitlines(keepends=True), new_state.splitlines(keepends=True)
    assert len(before) == len(after)
    changes = [(x, y) for x, y in zip(before, after) if x != y]
    assert len(changes) == 1 and all(x.startswith(b'| T-039 |') for x in changes[0])
    template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8-sig')
    prompt = (BASE / 'prompt-claude-sau-tai.txt').read_text(encoding='utf-8')
    blocks = lambda t: re.findall(r'```text\n(.*?)\n```', t, re.S)
    for header in ['### Soát SPEC', '### G3 — Khóa thiết kế trước khi mở test']:
        b = blocks(template.split(header + '\n', 1)[1])[0]
        assert b in prompt
    common = blocks(template.split('## Prompt chung\n', 1)[1])[0]
    common_literal = common.split('\nKhông sửa ngoài phạm vi trên,', 1)[1]
    assert '\nKhông sửa ngoài phạm vi trên,' + common_literal in prompt
    assert log_path.read_text(encoding='utf-8').count(prompt) == 1
    diffs = ''.join(difflib.unified_diff(old_state.decode('utf-8-sig').splitlines(True),
             new_state.decode('utf-8-sig').splitlines(True), fromfile='before-current-write/STATE.md', tofile='after/STATE.md'))
    diffs += ''.join(difflib.unified_diff(old_log.decode('utf-8-sig').splitlines(True),
             log_path.read_text(encoding='utf-8-sig').splitlines(True), fromfile='before-session/LOG.md', tofile='after/LOG.md'))
    (RUN / 'changes.diff').write_text(diffs, encoding='utf-8')
    save(RUN / 'final-verification.json', {'all_ok': True, 'protected_files_unchanged': len(protected),
        'approved_sources_verified': len(expected_sources), 'source_set_exact': True,
        'log_append_only': True, 'state_only_task_row': True, 'prompt_template_preserved': True,
        'python_parse_only': True, 'new_decision_file_writes': False,
        'log': digest(log_path), 'state': digest(state_path),
        'last_command': 'py -3 -X utf8 -B results/T-039/finalize_after_acquisition.py verify'})
    files = [digest(p) for p in sorted(BASE.rglob('*')) if p.is_file() and p != BASE / 'manifest.json']
    save(BASE / 'manifest.json', {'task': 'T-039', 'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'status': 'APPROVED_SOURCES_ACQUIRED_FULL_TASK_NOT_COMPLETED',
        'current_run': 'runs/ket-sau-tai-001', 'acquisition_run': 'runs/thu-nguon-001',
        'source_audit_run': 'runs/khao-sat-nguon-001', 'shared_pin_changed': False,
        'spec_changed': False, 'count': len(files), 'files': files,
        'excludes': 'manifest itself; LOG/STATE hashes in final-verification.json',
        'open': ['one-session feasibility/Minh decision', 'semantic source coverage',
                 'records/oracle/mapping/build/compare/analysis', 'dataset deployment lineage',
                 'auxiliary source independence', 'dataset Node host semantics'],
        'decisions_received': auth['user_answers'], 'formal_decisions_register_changed': False})
    assert all(digest(ROOT / e['path']) == e for e in files)
    print(json.dumps({'all_ok': True, 'manifest_files': len(files),
          'source_files_verified': len(expected_sources), 'protected_unchanged': len(protected),
          'task_complete': False, 'disk_bytes_manifest_files': sum(e['bytes'] for e in files)}))
else:
    raise ValueError('prepare or verify')
