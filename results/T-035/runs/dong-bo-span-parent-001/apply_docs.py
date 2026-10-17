"""Apply Minh's approved documentation correction; preserve the prior release."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
REL = RUN.relative_to(ROOT).as_posix()
FILES = [
    'results/T-035/dac-ta-do-thi.md',
    'docs/WHY.md',
    'docs/DECISIONS.md',
    'tasks/T-035-p5-do-thi-tu-trace/LOG.md',
    'docs/STATE.md',
    'results/T-035/manifest.json',
]
APPROVAL = 'duyệt sửa trong phiên này luôn, sau khi sửa, tạo 1 prompt cho phiên codex sạch mới review lại 035 1 lần nữa , phiên này review lại như lần đầu không neo theo những phần đã có tránh anchor'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def create(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data if isinstance(data, bytes) else data.encode('utf-8'))


def dump(path, value):
    create(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def append(rel, text):
    path = ROOT / rel
    raw = path.read_bytes()
    nl = '\r\n' if b'\r\n' in raw else '\n'
    with path.open('ab') as stream:
        stream.write((nl + text.replace('\r\n', '\n').replace('\n', nl)).encode('utf-8'))


def replace_line(text, prefix, replacement):
    found = [line for line in text.splitlines() if line.startswith(prefix)]
    assert len(found) == 1, (prefix, len(found))
    return text.replace(found[0], replacement, 1)


assert (ROOT / 'AGENTS.md').is_file(), ROOT
assert not (RUN / 'preflight.json').exists(), 'This run must not overwrite a previous attempt'
manifest = json.loads((ROOT / FILES[-1]).read_text(encoding='utf-8'))
for entry in manifest['files']:
    path = ROOT / entry['path']
    assert path.is_file() and sha(path.read_bytes()) == entry['sha256'], entry['path']
print(json.dumps({'stage': 'manifest_verified', 'files': len(manifest['files'])}), flush=True)

tracked = [x.decode('utf-8') for x in git('ls-files', '-z').split(b'\0') if x]
untracked = [x.decode('utf-8') for x in git('ls-files', '--others', '--exclude-standard', '-z').split(b'\0') if x]
outside_untracked = sorted(name for name in untracked if name not in FILES and not name.startswith(REL + '/'))
outside_diff = git('diff', '--no-ext-diff', 'HEAD', '--', '.', *[':(exclude)' + name for name in FILES])
for name in FILES:
    create(RUN / 'before' / name, (ROOT / name).read_bytes())
create(RUN / 'git-diff-before.patch', git('diff', '--no-ext-diff', 'HEAD', '--'))
create(RUN / 'git-status-before.txt', git('status', '--porcelain=v1', '--untracked-files=normal'))
baseline_check = subprocess.run(['git', 'diff', '--check', '--', *FILES], cwd=ROOT, capture_output=True)
dump(RUN / 'preflight.json', {
    'intent': 'EXECUTE', 'date_local': '2026-10-15',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'device': os.environ.get('COMPUTERNAME', 'Windows'),
    'approval': APPROVAL, 'decision': 'Q-156',
    'base_commit': manifest['base_commit'], 'head_before': git('rev-parse', 'HEAD').decode().strip(),
    'write_files': FILES, 'write_directory': REL + '/',
    'previous_artifacts_verified': len(manifest['files']),
    'previous_manifest_sha256': sha((ROOT / FILES[-1]).read_bytes()),
    'tracked_paths': tracked, 'outside_untracked_paths': outside_untracked,
    'outside_tracked_diff_sha256': sha(outside_diff),
    'git_diff_check_before': baseline_check.stdout.decode('utf-8', errors='replace'),
    'source_hashes': {name: sha((ROOT / name).read_bytes()) for name in [
        'AGENTS.md', 'docs/review-prompt.md', 'tasks/T-035-p5-do-thi-tu-trace/SPEC.md',
        'src/do_thi/builder.py', 'results/T-035/kiem-dung-dan.md',
        'results/T-035/scripts/write_docs.py',
    ]},
})
create(RUN / 'minh-duyet.txt', APPROVAL + '\n')
create(RUN / 'de-xuat-da-duyet.md', '''# Phạm vi đã được Minh duyệt — 15/10/2026

Đồng bộ văn bản với chính sách span-parent hiện có; không sửa code hoặc kết quả dev.

1. Mục 1 của đặc tả: ngoại lệ span-parent khi chiếu, kể cả hai thao tác khác chủ quản.
2. Mục 3: định nghĩa span-parent, điều kiện tạo, phạm vi giữ ở mức thao tác, không thay cây span gốc.
3. Thu hẹp gọi-chưa-phân-kiểu thành các cặp không thuộc gọi đồng bộ và span-parent.
4. Giải thích cross_entity_parent_events đếm cặp span khác chủ quản, bao gồm span-parent.
5. WHY nối lý do; DECISIONS ghi lời duyệt; LOG nối nhật ký và prompt; STATE chỉ dòng T-035.
6. Giữ bản trước sửa, diff và phép kiểm dưới thư mục lượt này; cập nhật manifest.

Phiên Codex sạch tiếp theo đọc nguồn và đầu ra gốc như lần đầu, ghi nhận xét độc lập trước lịch sử.
Codex vẫn là người làm, Claude phản biện chính thức. Chỉ soạn prompt, không tự mở hoặc gửi phiên.
''')

# Record the human decision before updating its dependent artifacts.
decisions = (ROOT / 'docs/DECISIONS.md').read_text(encoding='utf-8')
assert not re.search(r'\| Q-156 \|', decisions)
append('docs/DECISIONS.md', f'\n| Q-156 | 15/10/2026 | “{APPROVAL}” | Minh duyệt gói đồng bộ văn bản T-035 đã trình: làm rõ span-parent, ngoại lệ phép chiếu và phạm vi gọi chưa phân kiểu/số đếm; nối WHY, DECISIONS, LOG, chỉ dòng T-035 trong STATE; giữ bản trước sửa và cập nhật manifest. Phạm vi tại {REL}/de-xuat-da-duyet.md và preflight.json. Không sửa code hoặc chạy lại dev. Sau sửa soạn prompt Codex sạch soát toàn T-035 như lần đầu, đọc nguồn/đầu ra trước lịch sử; giữ Codex người làm, Claude phản biện chính thức. Chưa nghiệm thu, không mở test hoặc commit/push. |\n')
append('docs/WHY.md', '''
### Bổ sung WHY-52 — Làm rõ span-parent và ngoại lệ phép chiếu (15/10/2026, Q-156)

- **Chọn:** ghi đúng chính sách đã cài: cặp span cha–con tìm được trong cùng khoảng, có ít nhất một đầu PRODUCER/CONSUMER, được lưu dạng span-parent ở mức thao tác; không chiếu loại quan hệ này thành cạnh phụ thuộc thực thể. Cạnh messaging cần bằng chứng riêng theo hợp đồng. cross_entity_parent_events vẫn đếm các cặp khác chủ quản thuộc nhóm này.
- **Vì sao:** DT18-NV2/MRP P5 yêu cầu nút và cạnh có nghĩa rõ. Quan hệ cha–con của span có kind messaging chưa đủ tự xác nhận lời gọi hoặc nối bản tin. Code dựng/chiếu và bảng K5 đã có ngoại lệ, nhưng đặc tả mục 1 và câu “cặp còn lại” ở mục 3 chưa nêu nó. Đây là đồng bộ hợp đồng kỹ thuật với hành vi hiện có, không là phát hiện hạn chế RCA hoặc thay phương pháp P6.
- **Phương án đã xét:** thêm cạnh gọi cho mọi cặp loại này sẽ đổi cách diễn giải khi chưa có bằng chứng về quan hệ; chỉ dựa bảng K5 để giải thích không sửa được mâu thuẫn trong đặc tả hình thức. Chọn làm rõ định nghĩa, phép chiếu và số đếm, giữ bộ dựng.
- **Bằng chứng và giới hạn:** src/do_thi/builder.py tạo span-parent khi một đầu là PRODUCER/CONSUMER, bỏ loại này ở bước gộp thực thể và project; kiem-dung-dan.md/K5 đã ghi ngoại lệ. Phản ví dụ nhỏ đã tái lập trong bộ nhớ trước duyệt. Phép kiểm sau sửa sẽ lưu trong runs/dong-bo-span-parent-001/; không dùng việc được duyệt làm bằng chứng đã kiểm xong. span-parent là quan hệ đã gộp theo thao tác cùng witness, không giữ đầy đủ cây/thời gian từng lần thực thi.
- **Kết luận phụ thuộc:** độ nhất quán đặc tả/bộ dựng và bàn giao T-036/P9. Không khẳng định nguyên nhân vật lý, đầy đủ quan sát messaging runtime, lợi ích đồ thị hoặc đã đóng task/P5/G3/RQ3.
''')
append('tasks/T-035-p5-do-thi-tu-trace/LOG.md', f'''
## Phiên 9 — 15/10/2026 — Codex — {os.environ.get('COMPUTERNAME', 'Windows')} — Người làm

**Mở phiên / quyền:** EXECUTE theo lời Minh đã lưu nguyên văn tại Q-156; đồng bộ văn bản span-parent trong đúng phạm vi preflight.json và de-xuat-da-duyet.md của {REL}/. Không đổi vai trò. Prompt cho Codex sạch phải soát toàn task từ nguồn trước lịch sử.

**Trước sửa:** mọi artifact của manifest đầu phiên đã kiểm khớp; tập file, hash nguồn và bản trước sáu file được giữ trong lượt này. Ghi quyết định rồi WHY trước sửa đặc tả. Phản hồi của người làm đối với nhận xét Minh chuyển: đúng; mâu thuẫn nằm giữa câu chiếu/cặp còn lại trong đặc tả với ngoại lệ trong code và K5. Chưa có căn cứ từ nhận xét này để thêm cạnh gọi. Bước tiếp: sửa bốn nội dung văn bản đã trình, kiểm các trường hợp nhỏ và tính bất biến của code/kết quả, soạn hai prompt từ mẫu hiện hành.
''')

model_path = ROOT / 'results/T-035/dac-ta-do-thi.md'
raw = model_path.read_bytes()
nl = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8')
text = replace_line(text, 'Thành phần endpoint không có span', 'Thành phần endpoint không có span vẫn là thực thể, giữ trong danh sách component_context của mức thao tác. Không tạo thao tác giả. Phép chiếu giữ component_context và thay mỗi đầu mút thao tác bằng thực thể chủ quản; đầu mút thành phần được giữ nguyên. Loại mọi cạnh span-parent, kể cả giữa hai thao tác khác chủ quản, cùng cạnh nội bộ và quan hệ thuộc-về khỏi tập cạnh phụ thuộc thực thể. Các cạnh phụ thuộc còn lại có hai đầu thực thể khác nhau được giữ khi chiếu, gồm cạnh thao tác→thành phần hoặc thành phần→thao tác sau đổi đầu mút. So trên cùng tập quan sát; inventory không cộng vào tập nút quan sát.')
text = replace_line(text, 'Lời gọi quan sát chưa phân kiểu là', 'Lời gọi quan sát chưa phân kiểu từ cha–con là cặp span tìm được cha trong cùng khoảng, khác thực thể, không thuộc gọi đồng bộ và không có PRODUCER/CONSUMER ở hai đầu. Hướng là chủ quản cha→chủ quản con; chưa xác nhận là span phía gọi/phía được gọi thật. Một cặp không mặc nhiên là một request mạng. C2 đếm số span trong trace, sự bao thời gian và kiểm tay; thiếu instrumentation thì giữ giả định. Cặp cùng thực thể được giữ ở mức thao tác và đếm nội bộ riêng.')
needle = '- gọi-đồng-bộ:'
assert text.count(needle) == 1
text = text.replace(needle, '- span-parent: cặp span cha–con tìm được trong cùng khoảng, có ít nhất một đầu mang kind PRODUCER hoặc CONSUMER. Giữ ở mức thao tác dưới dạng quan hệ cha–con đã gộp theo thao tác cùng witness; không khẳng định đây là lời gọi hay quan hệ trao đổi bản tin và không thay thế cây span gốc. Không chiếu span-parent thành cạnh phụ thuộc thực thể, dù hai thao tác khác chủ quản. Các cạnh messaging có bằng chứng riêng vẫn được dựng và chiếu theo §7.' + nl + needle, 1)
text = replace_line(text, '- gọi-chưa-phân-kiểu:', '- gọi-chưa-phân-kiểu: các cặp cha–con còn lại sau khi loại gọi đồng bộ và span-parent; không gán quan hệ cha–con có PRODUCER/CONSUMER thành lời gọi chỉ vì hai đầu khác thực thể.')
needle = 'Callback trace mới được giữ'
assert text.count(needle) == 1
text = text.replace(needle, 'cross_entity_parent_events đếm mọi cặp span cha–con khác chủ quản tìm được trong cùng khoảng, gồm cả span-parent. Đây là số sự kiện quan hệ cha–con thô, không đồng nghĩa số cạnh hoặc tổng event_count của các cạnh phụ thuộc thực thể sau chiếu. Ví dụ một cặp khác chủ quản có đầu PRODUCER và thiếu bằng chứng messaging có thể cho số đếm này bằng 1 nhưng không tạo cạnh phụ thuộc thực thể; hai nút quan sát vẫn được giữ.' + nl + nl + needle, 1)
text += (nl + '## 9. Đính chính văn bản v2.1 — span-parent (15/10/2026)' + nl + nl + 'Theo Q-156, mục 1 và 3 được làm rõ để khớp chính sách đã cài và ngoại lệ đã ghi ở K5. Không đổi code, phép dựng/chiếu hoặc số dev. Bản trước và kiểm sau sửa được giữ tại runs/dong-bo-span-parent-001/. Việc đồng bộ này chưa là nghiệm thu toàn bộ hợp đồng, xác nhận nghĩa instrumentation hay lợi ích RCA.' + nl)
model_path.write_bytes(text.encode('utf-8'))

state_path = ROOT / 'docs/STATE.md'
state = state_path.read_bytes().decode('utf-8')
old_rows = [line for line in state.splitlines() if line.startswith('| T-035 |')]
assert len(old_rows) == 1
new_row = '| T-035 | P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace | P5 (G3) | Codex | Claude | Đã đồng bộ văn bản span-parent với bộ dựng theo Q-156 (15/10/2026); giữ kết quả dev đã kiểm. Chờ phiên Codex sạch tự soát toàn task từ nguồn như lần đầu, rồi phản biện chính thức/nghiệm thu. Prompt hiện hành tại results/T-035/runs/dong-bo-span-parent-001/, LOG Phiên 9. Chưa chọn P6/đóng task. | `tasks/T-035-p5-do-thi-tu-trace/` |'
state_path.write_bytes(state.replace(old_rows[0], new_row, 1).encode('utf-8'))

# Copy exact template blocks; only neutral metadata replaces placeholders.
template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8')
fence = '`' * 3
def block(heading):
    return template[template.index(heading):].split(fence + 'text', 1)[1].split(fence, 1)[0].strip('\n')
common = block('## Prompt chung')
stage = block('### Soát kết quả')
gate = block('### G3 — Khóa thiết kế trước khi mở test')
replacement = {
    '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>': 'T-035 — P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace; D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md',
    '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>': 'soát kết quả',
    '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>': 'P5; G2 đã duyệt, G3 là cổng kế tiếp',
    '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>': 'Codex người làm; Claude người phản biện chính thức theo SPEC. Phiên Codex sạch là lượt tự soát độc lập về ngữ cảnh do Minh yêu cầu, không đổi vai trò chính thức',
    '<danh sách đường dẫn và git diff từ commit gốc nếu có>': 'D:/RCA-flashticket/AGENTS.md; D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md; D:/RCA-flashticket/docs/MRP.md, D:/RCA-flashticket/docs/WHY.md, D:/RCA-flashticket/docs/DECISIONS.md, D:/RCA-flashticket/docs/LESSONS.md, D:/RCA-flashticket/docs/review-prompt.md; D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md. D:/Project/flash-ticket-platform/docs/architecture/B13-api-and-event-contracts.md và B16-observability-baseline.md chỉ đọc. Commit gốc theo manifest hiện hành; kiểm git status và đọc trực tiếp các tệp chưa theo dõi; đối chiếu diff lịch sử sau nhận xét độc lập',
    '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>': 'D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/LOG.md và bản phản biện nếu có sau khi liệt kê thư mục task; lịch sử ở D:/RCA-flashticket/results/T-035/runs/ và nội dung Minh cung cấp. Đọc nhận xét, kết luận, phản hồi, prompt cũ và bản trước sửa sau khi đã ghi nhận xét độc lập trong chat',
    '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>': 'D:/RCA-flashticket/src/do_thi/, D:/RCA-flashticket/src/p3/, D:/RCA-flashticket/src/circa_kien_truc/builder.py; D:/RCA-flashticket/results/T-035/dac-ta-do-thi.md, manifest.json và code, graph/JSON, fixture, báo cáo, các run theo manifest. Các nguồn upstream và allowlist dev theo SPEC và input-verification được manifest chỉ tới. Hướng dẫn D:/RCA-flashticket/src/do_thi/README.md, environment của lượt đầy đủ trong manifest; Windows/PowerShell; Python D:/RCA-ext/envs/py312-pin/Scripts/python.exe -X utf8 -B. Kiểm hash trước dùng đầu ra cũ',
    '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>': 'chỉ đọc và trả lời trong chat; không ghi REVIEW, LOG, STATE, SPEC, code hoặc kết quả, không commit/push. Không mở test/heldout/data/locked hoặc repo RCA lưu trữ. Dữ liệu dev chỉ qua allowlist/adapter và phạm vi SPEC; phép phát lại rẻ chỉ trong bộ nhớ, không chạy script có ghi hoặc thực nghiệm mới',
}
for key, value in replacement.items():
    assert common.count(key) == 1, key
    common = common.replace(key, value)
assert not re.search(r'<[^>]+>', common)
body = common + '\n\n' + stage + '\n\n' + gate + '\n'
prefix = '''Minh yêu cầu phiên Codex sạch đánh giá toàn bộ T-035 như lần đầu. Đây là lượt tự soát độc lập về ngữ cảnh; Codex vẫn là người làm, Claude vẫn là người phản biện chính thức.

Thứ tự riêng theo lời Minh: đọc yêu cầu nguồn, SPEC, hợp đồng hiện hành, code và bằng chứng đầu vào/trung gian/đầu ra trước. Dùng STATE và quyết định để xác định vai trò, quyền và yêu cầu; không lấy trạng thái hoàn thành làm kết luận. Chưa đọc nhận xét/kết luận trong LOG, REVIEW, báo cáo tự kiểm/tổng kết, bản trước sửa, diff lịch sử hoặc prompt cũ. Ghi danh sách nhận xét độc lập trong chat rồi mới đối chiếu lịch sử và báo cáo. Soát toàn task, không chỉ phần vừa sửa; không nhận danh sách finding cũ để định hướng tìm kiếm, không mặc định phải có lỗi hoặc ấn định số lỗi. Thứ tự này áp dụng trước hướng dẫn đọc lịch sử thông thường, theo yêu cầu trực tiếp của Minh.

'''
create(RUN / 'prompt-codex-sach-soat-t035.txt', prefix + body)
claude_common = common.replace(replacement['<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>'], 'Codex người làm; Claude người phản biện chính thức theo SPEC')
create(RUN / 'prompt-claude-soat-ket-qua.txt', claude_common + '\n\n' + stage + '\n\n' + gate + '\n')
dump(RUN / 'prompt-template-check.json', {
    'template_sha256': sha((ROOT / 'docs/review-prompt.md').read_bytes()),
    'stage_copied_verbatim': stage in body, 'gate_copied_verbatim': gate in body,
    'common_replacements_only': True,
    'prompt_files': {name: sha((RUN / name).read_bytes()) for name in ['prompt-codex-sach-soat-t035.txt', 'prompt-claude-soat-ket-qua.txt']},
    'no_finding_list_or_result_counts_in_metadata': True,
    'scope': 'read_only_chat', 'threads_created_or_messaged': False,
})
print(json.dumps({'status': 'DOCUMENTS_APPLIED', 'decision': 'Q-156', 'previous_artifacts_verified': len(manifest['files']), 'next': REL + '/verify.py'}, ensure_ascii=False))
