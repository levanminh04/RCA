"""Checkpoint approval after context compression; local documents/hash only."""
from pathlib import Path
import datetime, hashlib, json, difflib

root = Path.cwd()
out = root / 'results/T-033/runs/session7-storage-approval-checkpoint-001'
old = root / 'results/T-033/runs/session7-storage-checkpoint-001'
log = root / 'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'
state = root / 'docs/STATE.md'
sha = lambda b: hashlib.sha256(b).hexdigest()
def save(name, value):
    (out/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

assert not (out/'checkpoint.json').exists(), 'Preserve existing checkpoint; do not overwrite'
previous = json.loads((old/'manifest.json').read_text(encoding='utf-8'))
for rel, entry in previous['files'].items():
    b = (root/rel).read_bytes()
    assert len(b) == entry['bytes'] and sha(b) == entry['sha256'], rel

protected_names = ['AGENTS.md', 'tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md',
    'docs/DECISIONS.md', 'docs/WHY.md', 'docs/MRP.md', 'docs/LESSONS.md',
    'docs/review-prompt.md']
protected = {p: sha((root/p).read_bytes()) for p in protected_names}
log_before = log.read_bytes()
state_before = state.read_bytes()  # Read immediately before modifying only T-033.
(out/'LOG.md.before').write_bytes(log_before)
(out/'STATE.md.before').write_bytes(state_before)
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
ledger_bytes = (old/'ledger.json').read_bytes()
ledger = json.loads(ledger_bytes)
(out/'ledger.json').write_bytes(ledger_bytes)

checkpoint = {
    'at': now, 'task': 'T-033', 'worker': 'Codex', 'reviewer': 'Claude',
    'status': 'APPROVAL_RECORDED_CONTEXT_CHECKPOINT', 'task_complete': False,
    'reason': 'Context compressed; AGENTS section 5a.2 requires immediate checkpoint and new session',
    'approval': {'user_exact': 'duyệt', 'proposal': str((old/'README.md').relative_to(root)).replace('\\','/'),
        'approved_storage_limit_bytes': 5*1024**3,
        'scope': ['Keep every old and failed output', 'Use preserved session7_extract_v2.py projection/post_indices/exact byte guard/lossless new gzip',
            'One-case pilot and verify before rest excluding pilot; no detector rerun',
            'New T-033 outputs, append LOG, only T-033 STATE row, EC2 ~/rca/T-033/',
            'Continue original manual reading and synthesis after validated extraction'],
        'time_budget_changed': False, 'formal_decision_record_added': False},
    'prior_manifest_check': {'status':'PASS','files':len(previous['files'])},
    'new_ec2_commands': 0, 'new_ec2_charged_s': 0,
    'charged_new_processing_s': ledger['new_processing_charged_s'],
    'remaining_approved_processing_s': ledger['remaining_approved_s'],
    'ledger_source': {'path':str((old/'ledger.json').relative_to(root)).replace('\\','/'), 'sha256':sha(ledger_bytes)},
    'last_ec2_observation_is_historical': True,
    'last_ec2_observation': json.loads((old/'checkpoint.json').read_text(encoding='utf-8'))['ec2'],
    'correction_executed': False,
    'draft': {'path':'results/T-033/scripts/session7_extract_v2.py',
        'sha256':sha((root/'results/T-033/scripts/session7_extract_v2.py').read_bytes()),
        'validation':'Static only; pilot/rest/readback not yet run'},
    'next': 'New session reads governing sources and both session7 checkpoints, verifies hashes, creates/pins fresh cumulative ledger and timed source/process/hash EC2 check; builds exact pilot input, verifies pilot, then rest; continues full SPEC manual reading/synthesis.'
}
save('checkpoint.json', checkpoint)
readme = f'''# T-033 — Lời duyệt và checkpoint do ngữ cảnh nén

Minh trả lời nguyên văn **“duyệt”** cho đề xuất tại `../session7-storage-checkpoint-001/README.md`: nâng riêng trần đầu ra EC2 T-033 lên **5 GiB**, dùng bản sửa trích v2, một ca pilot có kiểm trước phần còn lại và tiếp nguyên SPEC. Giữ mọi file cũ/lỗi; không chạy lại detector PASS. Không đổi ngân sách thời gian, SPEC, DECISIONS, WHY hoặc nguồn cũ. Lời duyệt này không cần xin lại ở phiên tiếp.

Ngữ cảnh đã nén. Đã checkpoint theo AGENTS §5a.2; chưa SSH hoặc chạy bản sửa sau lời duyệt. Task và phần đọc tay/tổng hợp vẫn chưa hoàn tất. Codex người làm; Claude phản biện chính thức. Chưa soạn prompt phản biện vì task chưa xong.

Hash checkpoint trước đạt {len(previous['files'])}/{len(previous['files'])} trước ghi. `ledger.json` là bản sao nguyên byte của ledger cuối phiên 7: charged mới {ledger['new_processing_charged_s']} giây, còn {ledger['remaining_approved_s']} giây. Không có timer/charge EC2 mới. Hạch toán cũ 8 giờ là dự phòng chưa kiểm, actual cũ OPEN. Trạng thái không worker là quan sát lịch sử, cần kiểm mới có đo trước dùng EC2.

Bước tiếp chính xác: đọc AGENTS, STATE, toàn SPEC T-033 và LOG cuối; checkpoint này cùng README/checkpoint/ledger/scope/manifest của session7-storage-checkpoint-001; session7-open-001/points-lock.json, coverage-matching.json, lock-receive-verification.json; scripts/session7_control.py, session7_extract.py, session7_extract_v2.py và draft-static-check-final.json. Kiểm hash trước dùng. Dựng/pin snapshot ledger nối từ ledger cuối và mọi timer sau đó, kiểm process/source/hash mới có đo. Tự soát wrapper/input quyền 5GiB, explicit ca pilot, post_indices/time/cột/shape/scalar/NaN/flags và exact byte guard. Pilot đạt rồi rest loại pilot. CLI launch chưa hoàn thiện; không dùng lệnh suy đoán. Mã bản sửa chưa có PASS EC2.

Trước diễn giải phải đọc trực tiếp MRP RQ2/P4, DT18 NV2/NV3, advisor §1, toàn LESSONS, WHY-41 và các nguồn/checkpoint đã yêu cầu trong LOG. Dùng kết quả PASS theo hash; giữ 64 nhóm và 210 đường ca/khóa điểm. Lần theo đầu vào → xử lý → thống kê/phân phối → cờ/CP → chấm với điểm/ca đối chứng và giải thích cạnh tranh. Thiếu bằng chứng thì OPEN cùng phép kiểm, chi phí, quyết định phụ thuộc. Không tự đổi SPEC/tham số/tiêu chí hoặc chạy vượt quyền.

Minh cần mở phiên mới và dán: “Đọc AGENTS.md, tiếp T-033 trong STATE. Đọc checkpoint session7-storage-approval-checkpoint-001 và checkpoint phiên 7 theo LOG, kiểm hash trước dùng. Đề xuất trần EC2 5GiB và sửa trích tại README phiên 7 đã được tôi duyệt; không xin lại. Codex làm, Claude phản biện. Tiếp pilot/kiểm/rest rồi đọc tay và tổng hợp nguyên SPEC; mọi xử lý EC2 mới phải có ledger/timer, không chạy lại detector PASS, không xóa thêm. Ngữ cảnh nén thì checkpoint ngay.”

Lệnh cuối laptop: Python pin `-B -X utf8 results/T-033/runs/session7-storage-approval-checkpoint-001/checkpoint-writer.py`. Chỉ tài liệu/hash/diff. Lệnh EC2 cuối vẫn là receive-locks lịch sử ghi trong checkpoint trước.
'''
(out/'README.md').write_text(readme, encoding='utf-8')
entry = f'''\n\n### Bổ sung cuối phiên 7 — {now} — lưu lời duyệt; checkpoint ngay do ngữ cảnh nén

Quyết định của Minh trong lượt: trả lời nguyên văn “duyệt” cho đúng đề xuất tại results/T-033/runs/session7-storage-checkpoint-001/README.md. Được nâng riêng trần đầu ra EC2 T-033 lên 5GiB, dùng bản trích v2/post_indices/exact byte guard/gzip mới không mất dữ liệu, kiểm một ca pilot rồi rest loại pilot và tiếp nguyên SPEC. Giữ mọi bản cũ/lỗi; không chạy lại detector PASS. Không thay trần thời gian hoặc ghi quyết định mới vào DECISIONS/WHY/SPEC.

1. Đã làm: đọc lại AGENTS/STATE/nguồn checkpoint; kiểm manifest trước; lưu lời duyệt và checkpoint theo AGENTS §5a.2 vì ngữ cảnh nén. Chưa thực hiện EC2 mới hoặc chạy v2.
2. File đổi: chỉ thư mục mới results/T-033/runs/session7-storage-approval-checkpoint-001/, LOG nối mục này và duy nhất dòng T-033 STATE. Không sửa nguồn cũ hoặc file ngoài phạm vi.
3. Kiểm: manifest checkpoint trước PASS {len(previous['files'])}/{len(previous['files'])}; ledger sao nguyên byte; kiểm prefix LOG, mọi dòng STATE khác và hash tài liệu bảo vệ; diff/scope/manifest mới ở checkpoint này. Không có timer/charge EC2 mới. Charged mới {ledger['new_processing_charged_s']} giây, còn {ledger['remaining_approved_s']} giây; actual cũ OPEN.
4. OPEN: bản sửa mới chỉ đạt static, chưa pilot/rest/readback. Đọc tay/tổng hợp/RQ2/P4/G2 và phần nguyên nhân vật lý/onset chưa hoàn tất; không chờ duyệt lại storage/time. EC2 không worker là bằng chứng lịch sử phiên 7, chưa kiểm mới trong lượt này. Minh cần mở phiên mới theo README; không bật/tắt EC2. Chưa có prompt Claude vì toàn task chưa xong.

Bước tiếp chính xác: đọc README/checkpoint.json/ledger.json/scope-verification.json/manifest.json ở checkpoint mới, rồi checkpoint storage cũ và các khóa/script theo README. Kiểm hash; dựng input explicit pilot và snapshot ledger mới; trước EC2 phải kiểm process/source/hash có đo; pilot đạt mới rest không trùng; tiếp đọc tay/tổng hợp đủ SPEC và trực tiếp nguồn MRP/DT18/advisor/LESSONS/WHY-41. Không bịa CLI chưa hoàn thiện.
Lệnh cuối laptop: C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B -X utf8 results/T-033/runs/session7-storage-approval-checkpoint-001/checkpoint-writer.py (chỉ tài liệu/hash/diff). Lệnh EC2 cuối giữ nguyên session7_control.py remote-readonly session7-receive-locks-001 results/T-033/scripts/session7_receive_locks.py, chưa có EC2 mới sau lời duyệt.
'''
with log.open('ab') as f: f.write(entry.encode('utf-8'))
lines = state_before.decode('utf-8').splitlines(keepends=True)
indices = [i for i,s in enumerate(lines) if s.startswith('| T-033 |')]
assert len(indices)==1
i = indices[0]
cells = lines[i].rstrip('\r\n').split('|')
assert len(cells)==9
cells[6] = ' Đang thực hiện (phiên 7, 11/10): Minh đã duyệt trần đầu ra EC2 5GiB và bản trích v2/pilot/rest; checkpoint ngay vì ngữ cảnh nén. Chưa chạy v2/EC2 mới, giữ mọi lượt lỗi, không rerun PASS. Đọc tay/tổng hợp/RQ2/G2 còn OPEN; mở phiên mới từ session7-storage-approval-checkpoint-001, ledger cuối ở đó; kiểm process/source/hash có đo trước dùng EC2 '
newline = '\r\n' if lines[i].endswith('\r\n') else '\n'
lines[i] = '|'.join(cells)+newline
state.write_bytes(''.join(lines).encode('utf-8'))

assert log.read_bytes().startswith(log_before)
state_after = state.read_bytes()
assert [s for s in state_before.decode('utf-8').splitlines() if not s.startswith('| T-033 |')] == [s for s in state_after.decode('utf-8').splitlines() if not s.startswith('| T-033 |')]
assert {p:sha((root/p).read_bytes()) for p in protected_names} == protected
diff = ''.join(difflib.unified_diff(state_before.decode('utf-8').splitlines(True),state_after.decode('utf-8').splitlines(True),fromfile='STATE.before',tofile='STATE.after'))
diff += ''.join(difflib.unified_diff(log_before.decode('utf-8').splitlines(True),log.read_text(encoding='utf-8').splitlines(True),fromfile='LOG.before',tofile='LOG.after'))
(out/'approved-docs.diff').write_text(diff, encoding='utf-8')
save('scope-verification.json', {'status':'PASS','old_manifest_files_verified':len(previous['files']),
    'log_prefix_unchanged':True,'state_other_rows_unchanged':True,
    'protected_files_before_after':protected,'ec2_used':False,
    'prior_ledger_copy_hash':sha(ledger_bytes)})
paths = sorted(p for p in out.iterdir() if p.is_file() and p.name!='manifest.json')+[log,state]
manifest = {'status':'PASS','path_basis':'repository root','self_excluded':True,'files':{}}
for p in paths:
    b=p.read_bytes(); manifest['files'][p.relative_to(root).as_posix()]={'sha256':sha(b),'bytes':len(b)}
save('manifest.json',manifest)
for rel,v in manifest['files'].items():
    b=(root/rel).read_bytes(); assert sha(b)==v['sha256'] and len(b)==v['bytes']
print(json.dumps({'status':'PASS','manifest_files':len(manifest['files']),'ec2_new_commands':0,
    'approved_storage_limit_bytes':5*1024**3,'checkpoint':out.relative_to(root).as_posix()},ensure_ascii=False))
