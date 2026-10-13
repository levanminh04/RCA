"""Mở phiên đã được Minh duyệt; không tính toán nghiên cứu."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[3]
task = root / 'tasks/T-033-g2-nguyen-nhan-phat-hien'
run = root / 'results/T-033/runs/prepare-001'
run.mkdir(parents=True, exist_ok=False)
paths = ['AGENTS.md', 'docs/STATE.md', 'docs/WHY.md',
         'tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md']
before = {}
for name in paths:
    b = (root / name).read_bytes()
    before[name] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    (run / (Path(name).name + '.before')).write_bytes(b)
(run / 'before.json').write_text(json.dumps(before, indent=2), encoding='utf-8')
spec = task / 'SPEC.md'
b = spec.read_bytes()
lines = b.splitlines(keepends=True)
hits = [i for i, line in enumerate(lines) if line.startswith('- **Trạng thái:**'.encode())]
assert len(hits) == 1
i = hits[0]
ending = b'\r\n' if lines[i].endswith(b'\r\n') else b'\n'
lines[i] = ('- **Trạng thái:** Minh duyệt SPEC và thực hiện ngày 09/10/2026 (Q-91, Q-92; lời duyệt "ĐÃ CHỐT"); SPEC đã khóa. Đang chuẩn bị nguồn/môi trường theo các chặng được duyệt.').encode() + ending
spec.write_bytes(b''.join(lines))
# Đọc lại file chung ngay trước mỗi thao tác; chỉ thay đúng dòng T-033.
state = root / 'docs/STATE.md'
b = state.read_bytes()
lines = b.splitlines(keepends=True)
hits = [i for i, line in enumerate(lines) if line.startswith(b'| T-033 |')]
assert len(hits) == 1
i = hits[0]
parts = lines[i].decode().split('|')
parts[6] = ' Đang thực hiện theo Minh duyệt 09/10: chuẩn bị nguồn/hash/EC2; chưa chạy nghiên cứu '
lines[i] = '|'.join(parts).encode()
state.write_bytes(b''.join(lines))
# Nội dung phụ lục chép nguyên văn; không tạo/sửa WHY-40.
why = root / 'docs/WHY.md'
b = why.read_bytes()
assert b'## WHY-41.' not in b
text = spec.read_text(encoding='utf-8')
appendix = text.split('## Phụ lục — dự thảo WHY-41\n', 1)[1].split('\n## Prompt bàn giao', 1)[0].strip()
addition = '\n\n## WHY-41. Lần theo cơ chế phát hiện — Đã quyết (Minh duyệt SPEC T-033 ngày 09/10/2026)\n\n' + appendix + '\n'
with why.open('ab') as f:
    f.write(addition.encode())
log = task / 'LOG.md'
assert not log.exists()
log.write_text('''# LOG T-033 — Lần theo cơ chế phát hiện

## Phiên 1 — 09/10/2026 — Codex — laptop Windows 11 và EC2 T-033 — Người làm

- Minh duyệt SPEC ngày 09/10/2026.
- Intent: EXECUTE. USER_CONFIRMED: Minh nói "ĐÃ CHỐT", duyệt SPEC trên file, thứ tự lõi → nhánh bổ sung, ngân sách 4–12 giờ máy và tối đa 4 GiB mới; chạy nền/qua đêm trên EC2 3.107.246.249 với keys.pem. Vượt dự toán phải checkpoint, dừng và trình Minh. Không test/locked/heldout, không commit/push hoặc bật/tắt EC2.
- Phạm vi: results/T-033/, LOG chỉ nối, dòng T-033 STATE, trạng thái SPEC T-033, WHY-41 nguyên phụ lục, EC2 ~/rca/T-033/. Không đọc/ghi results/T-032/ hoặc ~/rca/T-032/. Phiên T-032 chịu trách nhiệm DECISIONS lời duyệt chung; phiên này không ghi DECISIONS.
- Đã đọc AGENTS, STATE, toàn SPEC. Chưa có LOG hoặc results T-033; không có đầu ra cần làm lại. STATE/SPEC còn trạng thái trước duyệt; cập nhật đúng dòng được Minh cho phép. Đọc MRP RQ2/P4, DT18-NV2/NV3, hướng dẫn cô §1, LESSONS và WHY-34/35/39/40; không coi số cờ là cơ chế hoặc proxy là onset thật.
- Nối WHY-41 nguyên văn phụ lục trước dùng lựa chọn. Bảo toàn byte ngoài dòng SPEC/STATE và prefix WHY; baseline tại results/T-033/runs/prepare-001/.
- Một trợ lý chỉ đọc hỗ trợ tìm contract N-Sigma; không phải reviewer chính thức, không ghi hoặc chạy phương pháp. Claude vẫn là reviewer do Minh chuyển thủ công.
- Kết nối đầu: sandbox chặn SSH; thử ngoài sandbox được duyệt tự động nhưng strict host checking báo chưa có khóa host mặc định. Không sửa known_hosts của Minh. Key đã xác định D:/RCA-ext/keys/keys.pem; sẽ lưu khóa host TOFU mới chỉ trong run T-033 với accept-new trước SSH. Không tắt kiểm host key.
- CẦN GIỮ LAPTOP MỞ: chưa kiểm môi trường, hash và ca đầu; chưa có run ổn định. Các ca/bước chưa chạy. Chưa có kết luận nghiên cứu.
''', encoding='utf-8')
after = {}
for name in paths:
    q = root / name
    bb = q.read_bytes()
    after[name] = {'sha256': hashlib.sha256(bb).hexdigest(), 'bytes': len(bb)}
spec_before = (run / 'SPEC.md.before').read_bytes().splitlines(keepends=True)
spec_after = spec.read_bytes().splitlines(keepends=True)
assert [x for x in spec_before if not x.startswith('- **Trạng thái:**'.encode())] == [x for x in spec_after if not x.startswith('- **Trạng thái:**'.encode())]
state_before = (run / 'STATE.md.before').read_bytes().splitlines(keepends=True)
state_after = state.read_bytes().splitlines(keepends=True)
assert [x for x in state_before if not x.startswith(b'| T-033 |')] == [x for x in state_after if not x.startswith(b'| T-033 |')]
assert why.read_bytes().startswith((run / 'WHY.md.before').read_bytes())
(run / 'open-session-verification.json').write_text(json.dumps({'status': 'PASS', 'after': after, 'spec_only_status': True, 'state_only_T033': True, 'why_append_only': True, 'appendix_exact': True}, indent=2), encoding='utf-8')
print('PASS: mở LOG, đúng dòng SPEC/STATE và nối nguyên WHY-41.')
