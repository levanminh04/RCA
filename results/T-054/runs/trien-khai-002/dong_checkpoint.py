"""Đóng gói checkpoint công cụ; không chạy thực nghiệm hoặc nâng quyền."""
import hashlib
import json
import re
import shutil
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-002'


def pin(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def save(path, value):
    if path.exists():
        raise RuntimeError('Không ghi đè: ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')


source = json.loads((OUT / 'source-manifest.json').read_bytes())
source['previous_source_manifest'] = pin(OUT / 'source-manifest.json')
source['own_scripts'] = {p.relative_to(ROOT).as_posix(): pin(p) for p in sorted((OUT / 'scripts').glob('*.py'))}
source['status'] = 'CURRENT_CODE_CHECKPOINT_NOT_G3'
source['decision_source'] = pin(OUT / 'manifest-quyet-dinh-001.json')
source['authority'] = pin(RUN / 'quyen-minh.txt')
source['candidate_documents_stale'] = ['protocol.json', 'matrix.json', 'pilot-plan.json', 'ho-so-g3.md']
save(RUN / 'source-current.json', source)

freeze = OUT / 'runs/freeze-cong-cu-004'
freeze.mkdir(exist_ok=False)
old = json.loads((OUT / 'runs/freeze-cong-cu-003/files.json').read_bytes())
files = {}
for relative in old['files']:
    src = ROOT / relative
    dst = freeze / 'code' / relative
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    raw = dst.read_bytes()
    files[relative] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                       'git_blob_from_exact_bytes': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}
save(freeze / 'files.json', {'files': files, 'HEAD_is_not_working_tree': True,
     'contains_private_labels': False, 'contains_telemetry': False,
     'status': 'CODE_CHECKPOINT_NOT_G3_FREEZE',
     'historical_candidate_metadata': ['results/T-054/protocol.json', 'results/T-054/matrix.json'],
     'current_code_manifest': pin(RUN / 'source-current.json')})
with tarfile.open(freeze / 'code.tar.gz', 'w:gz') as tar:
    for relative in files:
        tar.add(freeze / 'code' / relative, arcname=relative, recursive=False)
save(freeze / 'package.json', {'status': 'CODE_CHECKPOINT_NOT_G3_FREEZE', 'test_allowed': False,
     'archive': pin(freeze / 'code.tar.gz'), 'files_manifest': pin(freeze / 'files.json'),
     'note': 'Protocol/matrix là ứng viên lịch sử; không dùng gói để phát test hoặc nhận đã hoàn tất công cụ.'})

state = ROOT / 'docs/STATE.md'
before_state = state.read_bytes()
(RUN / 'STATE-before.txt').write_bytes(before_state)
text = before_state.decode('utf-8')
old_line, = [line for line in text.splitlines() if line.startswith('- **T-054 —')]
new_line = ('- **T-054 — Khóa G3(a), chạy/báo cáo P7(a): đang hoàn thiện công cụ, chưa xong pha 1.** '
            'Codex làm, Claude phản biện. Checkpoint 002 đã kiểm điều phối/phục hồi, phụ thuộc C-d3, '
            'TORAI A tự sinh và gate A4; chưa pilot thật/SSH/G3/test. Minh giữ A bảng phụ, nguồn cấp sau; '
            'cho tăng thời gian, chưa chốt trần số/quy tắc cạn trần. Còn plan nguồn thật, phân loại lỗi, '
            'parity và dự toán pilot. [LOG phiên 3](../tasks/T-054-khoa-g3-chay-p7-a/LOG.md), '
            '[báo cáo 002](../results/T-054/reports/tu-soat-002/bao-cao.md).')
assert text.count(old_line) == 1
state.write_bytes(text.replace(old_line, new_line).encode('utf-8'))

template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8-sig')


def block(title):
    part = template[template.index(title):]
    return part.split('```text', 1)[1].split('```', 1)[0].strip()


common = block('## Prompt chung')
values = [
    'T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md',
    'soát kết quả',
    'P6/G3(a), chuẩn bị P7(a)',
    'Codex làm; Claude phản biện',
    'tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; các nguồn trực tiếp được dẫn trong SPEC',
    'results/T-054/runs/soan-spec-001/nguon-phan-bien-001.txt, nguon-phan-bien-002.txt, phan-hoi-002.md',
    'results/T-054/scripts/; manifest-trien-khai-002.json; runs/trien-khai-002/source-current.json; runbook.md; các nguồn/code được dẫn trong các manifest',
    'chỉ đọc và trả lời trong chat; chưa cấp file phản biện mới',
]
matches = re.findall(r'<[^>]+>', common)
assert len(matches) == len(values)
for old_value, new_value in zip(matches, values):
    common = common.replace(old_value, new_value, 1)
prompt = '\n\n'.join([common, block('### Soát kết quả'), block('### G3 — Khóa thiết kế trước khi mở test')])
assert not re.search(r'<[^>]+>', prompt)
(RUN / 'prompt-claude.txt').write_text(prompt + '\n', encoding='utf-8')

log = ROOT / 'tasks/T-054-khoa-g3-chay-p7-a/LOG.md'
ending = '''

### Kết thúc phiên 3 — checkpoint 002, chưa hoàn tất pha 1

1. Đã làm: tiếp tục tự soát nguồn và code, sửa lỗi journal/trần thời gian/DRAIN/PID Windows; nối phụ thuộc main→C-d3 bất biến; prep/run A trên dữ liệu tự sinh; gate đủ cohort/seed trước nhãn; lập đề xuất pilot. Báo cáo chi tiết: `results/T-054/reports/tu-soat-002/bao-cao.md`. Giữ đúng giới hạn nhận xét nguồn từ báo cáo 001; không nhận là review chính thức hoặc soát mù mới.
2. File đổi: chín script T-054, LOG chỉ nối, đúng dòng T-054 STATE; thêm đầu ra dưới results/T-054/runs/trien-khai-002, reports/tu-soat-002, freeze-cong-cu-004 và manifest-trien-khai-002. Không sửa SPEC/src/sổ hoặc file lịch sử; các thay đổi có sẵn ngoài T-054 được giữ. Danh mục đầy đủ và pin nằm trong manifest mới. Freeze004 là 107 file đúng byte; protocol/matrix bên trong là ứng viên lịch sử, không là cấu hình đã khóa.
3. Kiểm: queue-fixtures-004 25 PASS; regression-transport-002 60 PASS; TORAI A thật bằng Python 3.8 trên dữ liệu tự sinh đủ seed 0/1/2, prep khớp byte; a4-guard tám phản ví dụ không đọc nhãn; regression-report 28 slot/89 dòng/bốn vùng/hai vị trí N PASS. Không cộng các lượt lặp thành tổng độc lập. Giữ các lượt lỗi, gồm queue-fixtures-003 và regression-transport-001. Kiểm đóng gói/phạm vi sẽ lưu tại runs/trien-khai-002/validation.json; sau đó pin toàn bộ đầu ra vào manifest, kiểm lại chỉ đọc bằng lệnh cuối bên dưới.
4. Chưa chắc/cần Minh: chưa có pilot thật, ETA hoặc bằng chứng parity mới, chưa khóa G3/test. Thiếu plan thực từ nguồn gốc độc lập, binding nguồn/nhãn, grant materialize/pilot/SSH/sync, nguồn A, môi trường, chính sách lỗi/timeout/cạn trần/độ nhạy; chưa có scheduler nhiều worker và số đo đủ. Giữ A bảng phụ đã USER_CONFIRMED; grant nguồn sau. Cho tăng thời gian đã USER_CONFIRMED nhưng chưa có số. Đề xuất pilot 3 giờ trôi/tối đa 9 giờ-máy trong pilot-proposal.json là CANDIDATE CHƯA KIỂM, không phải quyền/ETA. Chưa xin phát lô khi nguồn/môi trường chưa hoàn chỉnh. Chưa nghiệm thu task hoặc trả lời hiệu quả độc lập RQ3b/d và các câu hỏi nguồn còn mở.

Minh nhắn tiếp trong lượt: “KHI NÀO XONG BƯỚC PILOT VÀ ƯỚC LƯỢNG ,CHUẨN BỊ SANG CHẠY CHÍNH THÌ BÁO TÔI NHÉ, SẮP HẾT USAGE”; sau đó “VẬY SAU BƯỚC NÀY BÁO CÁO LẠI TÔI LUÔN”. Ghi yêu cầu báo sau bước hiện tại và báo mốc xong pilot/dự toán trước chạy chính; không nhận các câu này là đã khóa G3, duyệt trần bằng số hay mở nguồn/test/SSH. Không lập automation hoặc tự mở chat.

Ngữ cảnh đã nén: đã ghi checkpoint ngay theo AGENTS §5a.2 và đề nghị mở phiên mới. Phiên tiếp nhận đọc manifest mới, kiểm pin source-current thay own_scripts cũ; không chạy generator lap_ho_so.build_documents vì vẫn mang giả định A OPEN. Root protocol/matrix/source-manifest/pilot-plan/ho-so-g3 từ checkpoint001 chưa đồng bộ; phải cập nhật generator/hồ sơ từ nguồn quyết định trước dùng. Giữ mọi lịch sử.

Bước tiếp chính xác:
- Đọc AGENTS, dòng T-054 STATE, SPEC, mục cuối LOG và reports/tu-soat-002/bao-cao.md. Kiểm manifest-trien-khai-002 cùng validation.json và source-current.json.
- Đọc results/T-052/giao-thuc-p7-a-003.json mục C_e, nguồn P3/G1 và metadata dev gốc trước khi nối plan thật; không đọc raw test/A. Bản đồ độc lập phải có nguồn gốc, không hai bản tự sinh cùng dữ kiện.
- Hoàn thiện phần công cụ còn thiếu: finalization lỗi đủ chứng cứ, plan/source binding, C-e support, generator/hồ sơ hiện hành, scheduler và phép đo được SPEC yêu cầu. Không tự chọn chính sách khoa học.
- Khi có plan cụ thể, trình đúng gói pilot/nguồn/máy/thời gian và grant còn thiếu theo SPEC §7; sau pilot báo Minh số đo/dự toán và điều kiện còn thiếu trước chạy chính. Không dùng cap đề nghị làm ETA.

Đề xuất sổ chính thức chưa ghi: docs/DECISIONS.md nối “Minh cho tăng thời gian thực hiện T-054, mức cụ thể cần dự toán; giữ TORAI A ở bảng phụ ngoài A4, cấp quyền nguồn riêng sau.” Cần Minh duyệt đúng dòng/phạm vi trước ghi. Chưa có quyết định mới về cơ chế phương pháp.

Lệnh cuối dự kiến và được chạy để chốt checkpoint: `& 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe' -X utf8 -B 'results/T-054/runs/trien-khai-002/kiem_checkpoint.py' --manifest 'results/T-054/manifest-trien-khai-002.json'`. Bản thân lệnh này chỉ đọc. Không chạy lại validator checkpoint001 vì pin của nó đã thành lịch sử.

Prompt trung tính để Minh chọn chuyển sang Claude (chưa tự gửi, chưa đề nghị nghiệm thu; chưa có quyền ghi REVIEW mới):

```text
'''
with log.open('ab') as stream:
    stream.write((ending + prompt + '\n```\n').encode('utf-8'))
print(json.dumps({'freeze_files': len(files), 'LOG_appended': True, 'STATE_task_row_only': True,
                  'scientific_pilot_run': False, 'test_opened': False}))
