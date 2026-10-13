"""Chốt LOG/STATE và kiểm phạm vi; laptop chỉ xử lý metadata bàn giao."""
import ast
import difflib
import hashlib
import json
import tarfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[3]
home = root / 'results/T-033'
task = root / 'tasks/T-033-g2-nguyen-nhan-phat-hien'
opening = home / 'runs/session2-open-001'
checkpoint = home / 'runs/checkpoint-session2-001'
run = home / 'runs/checkpoint-session2-final'
run.mkdir(exist_ok=False)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for name in ['snapshot.json', 'metadata.tar.gz']:
    assert sha(checkpoint / name) == (checkpoint / (name + '.sha256')).read_text().split()[0]
with tarfile.open(checkpoint / 'metadata.tar.gz', 'r:gz') as archive:
    for member in archive.getmembers():
        destination = (checkpoint / member.name).resolve()
        assert checkpoint.resolve() in destination.parents
        assert not member.issym() and not member.islnk()
    archive.extractall(checkpoint, filter='data')
metadata = checkpoint / 'metadata'
snapshot = json.loads((checkpoint / 'snapshot.json').read_text(encoding='utf-8'))
assert snapshot['nsigma_fixed_units_verified'] == 60
assert snapshot['statuses']['bocpd-factorial-first-001']['status'] == 'PASS'
assert snapshot['statuses']['bocpd-factorial-rest-001']['status'] in ['RUNNING', 'PASS']
assert not snapshot['task_complete'] and not snapshot['research_questions_closed']
for verification in snapshot['completed_manifests_verified'].values():
    for relative, info in verification['files'].items():
        path = metadata / relative
        if path.is_file():
            assert path.stat().st_size == info['bytes'] and sha(path) == info['sha256']
audit = metadata / 'runs/core-audit-002/verification.json'
assert sha(audit) == snapshot['core_audit_sha256']
audit_doc = json.loads(audit.read_text(encoding='utf-8'))
assert audit_doc['status'] == 'PASS' and audit_doc['core_records'] == 120
assert audit_doc['nsigma_records'] == audit_doc['bocpd_full_PP_records'] == 60
assert sha(home / 'runs/prepare-001/inputs/source.json') == audit_doc['source_sha256']

# Không sửa SPEC/WHY trong phiên này. Nếu chat khác nối WHY thì giữ nguyên.
assert (task / 'SPEC.md').read_bytes() == (opening / 'SPEC.md.before').read_bytes()
assert (root / 'docs/WHY.md').read_bytes().startswith((opening / 'WHY.md.before').read_bytes())
assert (task / 'LOG.md').read_bytes().startswith((opening / 'LOG.md.before').read_bytes())
assert (root / 'AGENTS.md').read_bytes() == (home / 'runs/prepare-001/AGENTS.md.before').read_bytes()
script_ast = {}
for path in (home / 'scripts').glob('*.py'):
    ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    script_ast[path.name] = True
deployed = {}
for name in ['bocpd_factorial.py', 'nsigma_frozen.py', 'factorial_matrices.py',
             'supplement_job.sh', 'factorial_first.sh', 'factorial_rest.sh',
             'audit_core_fast.py', 'capture_session2.py']:
    assert sha(home / 'scripts' / name) == snapshot['scripts'][name], name
    deployed[name] = snapshot['scripts'][name]

# Đọc STATE ngay trước khi ghi; chỉ thay ô Trạng thái của dòng T-033.
state = root / 'docs/STATE.md'
state_before = state.read_bytes()
(run / 'STATE.md.before-close').write_bytes(state_before)
lines = state_before.splitlines(keepends=True)
indexes = [i for i, line in enumerate(lines) if line.startswith(b'| T-033 |')]
assert len(indexes) == 1
i = indexes[0]
parts = lines[i].decode('utf-8').split('|')
parts[6] = ' Đang thực hiện: lõi N-Sigma/BOCPD đã kiểm PASS; nền cố định 60/60 PASS; FP/PF ca đầu đạt, 29 ca mới chạy nền ổn định; checkpoint LOG phiên 2. Chưa độ trễ/kênh/đối chứng hoặc kết luận cơ chế '
lines[i] = '|'.join(parts).encode('utf-8')
state.write_bytes(b''.join(lines))
assert [l for l in state_before.splitlines(keepends=True) if not l.startswith(b'| T-033 |')] == [l for l in state.read_bytes().splitlines(keepends=True) if not l.startswith(b'| T-033 |')]

status = snapshot['statuses']['bocpd-factorial-rest-001']
now = datetime.now(timezone(timedelta(hours=7))).isoformat()
progress_command = "ssh -i D:/RCA-ext/keys/keys.pem -o UserKnownHostsFile=D:/RCA-flashticket/results/T-033/runs/prepare-001/known_hosts -o StrictHostKeyChecking=yes -o BatchMode=yes ubuntu@3.107.246.249 'tail -n 20 ~/rca/T-033/trang-thai.txt'"
channel_exists = (home / 'scripts/channel_context.py').is_file()
log = task / 'LOG.md'
log_before = log.read_bytes()
(run / 'LOG.md.before-close').write_bytes(log_before)
entry = f'''

### Kết thúc phiên 2 — {now}

1. Đã làm: kiểm lõi bằng `core-audit-002`, PASS 120 record; chạy và kiểm FP/PF ca đầu theo native cùng đầu vào; chạy nền cố định đủ 60 đơn vị, mọi kiểm độc lập từ Series gốc đạt. Snapshot EC2 lúc {snapshot['utc']} tại `results/T-033/runs/checkpoint-session2-001/snapshot.json` → `/statuses`, `/completed_manifests_verified`, `/live_completed_cases`, `/resources`. FP/PF rest còn {status['status']}, PID {status['pid']}; snapshot kiểm hash hai nhánh của {len(snapshot['live_completed_cases'])} ca mới: {', '.join(snapshot['live_completed_cases'])}. Lô tự tiếp đúng danh sách nguồn; đây không phải hoàn tất T-033.
2. File thay đổi trong phiên: script và checkpoint/metadata trong `results/T-033/`; chỉ nối `tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md`; chỉ ô trạng thái dòng T-033 của `docs/STATE.md`. SPEC và WHY không được sửa trong phiên 2. EC2 chỉ ghi `~/rca/T-033/`; nguồn code/data/env cũ chỉ đọc. Không ghi DECISIONS, không đọc/ghi vùng kết quả T-032, không test/locked/heldout, không commit/push, không bật/tắt EC2. Script `bocpd_delay.py` và `nsigma_delay.py` chưa được chạy; channel_context.py có trên laptop: {channel_exists}, chưa được người làm kiểm đầy đủ hoặc chạy.
3. Kiểm: nguồn/manifest/trung gian lõi PASS; FP/PF ca đầu khớp native R/m/CP/time và ma trận; nền cố định khớp mean/std/count/flags/margin từ Series dtype gốc, mọi cột/ca. Hash toàn manifest của hai lô fixed và pilot FP/PF đạt. Snapshot và archive metadata hai đầu cùng hash; JSON đã nhận được kiểm theo manifest, NPZ được kiểm tại EC2 và không tải về trong checkpoint này. AST script đạt; script đã triển khai khớp laptop/EC2; tự kiểm phạm vi và diff lưu `results/T-033/runs/checkpoint-session2-final/`. Run audit chậm 001 vẫn được giữ; audit 002 chỉ sửa việc giải nén lặp, không đổi tiêu chí. Auto-review từ chối một lệnh khởi khi pilot chưa chốt; đã giải quyết bằng pilot PASS, hash và dự toán trước khởi rest, không còn chặn quyền này.
4. OPEN và việc Minh cần làm: task chưa hoàn tất. Cần độ trễ/mật độ/chuỗi cờ, đối chiếu kênh, khóa nhóm bổ sung, đọc tay có đối chứng và phân xử cơ chế. Chưa đóng RQ2/P4/G2 hoặc chọn P6. Duration trace giữ raw, đơn vị còn OPEN theo nguồn; số traceID quan sát không tự là số request độc lập. Không dùng PASS của driver làm kết luận vật lý. EC2 còn cần bật; lô FP/PF hiện đã ổn định để Minh tắt laptop. Ước lượng xong lô 10:30–11:00 ngày 10/10 +07, không bảo đảm xong toàn task. Guard 12 giờ toàn lịch dừng tại 11:46:29 ngày 10/10 +07 và giới hạn 4 GiB vẫn giữ. Snapshot ghi dung lượng mới {snapshot['resources']['new_bytes']} byte, RAM khả dụng {snapshot['resources']['ram_available_bytes']} byte và đĩa trống {snapshot['resources']['disk_free_bytes']} byte; đây là nguồn số tại thời điểm snapshot. Nếu phần còn thiếu vượt dự toán thì checkpoint, dừng phần phụ thuộc và trình Minh.

EC2 T-033 ĐÃ ỔN ĐỊNH — Minh có thể tắt laptop

Đang chạy `bocpd-factorial-rest-001`, tmux `t033-fac-rest`, socket `/home/ubuntu/rca/T-033/tmux.sock`. Ca đầu đã đạt kiểm nguồn/điểm đổi/native và trung gian; tốc độ/RAM/dung lượng được đo trước khởi phần còn lại; lỗi hoặc budget tự dừng và ghi lại. Khi mở lại phiên, agent kiểm status/exit/PID, stdout/stderr và hash manifest trước dùng, không khởi trùng; sau đó tiếp chặng còn thiếu theo SPEC. Minh giữ EC2 bật cho tới khi agent báo không còn cần máy.

Lệnh Minh xem tiến độ:

```powershell
{progress_command}
```

Nguồn vận hành: `~/rca/T-033/runs/bocpd-factorial-rest-001/status.json` (PID hiện hành); `progress.txt`, `stdout.txt`, `stderr.txt` trong run; outer `.out`, `.err`, `.shell.pid`, `.exit` dưới `runs/`. Lệnh khởi đã dùng `bash ~/rca/T-033/scripts/factorial_rest.sh` trong tmux; không chạy lại lệnh khởi khi worker còn sống. Pilot và fixed có status PASS cùng manifest trong thư mục run của chúng.

Bước tiếp theo chính xác: đọc AGENTS, STATE, toàn SPEC, LOG phiên 2 và snapshot/metadata nêu trên. SSH xem progress bằng lệnh trên; kiểm `bocpd-factorial-rest-001/status.json`, `.exit`, stderr và PID lấy từ status. Nếu PASS, kiểm toàn manifest và đọc con trỏ `reused_record` cho ca pilot; NPZ của ca tái dùng nằm trong pilot, không giả định nằm trong rest. Nếu STOPPED/BUDGET_STOP hoặc không đủ dự toán, đọc lỗi, dừng phần phụ thuộc và trình Minh. Không chạy lại core, pilot, fixed hoặc ca đã PASS. Script delay/kênh còn phải được kiểm nguồn và cài/run trên EC2, laptop không tính nghiên cứu. Đọc CLI và nguồn của `bocpd_delay.py`, `nsigma_delay.py`, `channel_context.py`; lấy anchors từ `factorial_first.sh`/snapshot trước triển khai. Tiếp các chặng, khóa lựa chọn trước diễn giải, giữ câu hỏi chưa phân xử là OPEN. Nếu thấy thiết kế SPEC không phân xử được hoặc sai với code/data, báo vị trí, bằng chứng, hậu quả và đề xuất, không tự đổi SPEC/phép làm.

Lệnh cuối đã chạy để chốt phiên: Python `-B -X utf8 results/T-033/scripts/finish_session2.py` trên laptop (chỉ metadata, AST và cập nhật LOG/STATE). Lệnh EC2 cuối của checkpoint: Python `capture_session2.py` chỉ đọc trạng thái/kiểm hash, ghi snapshot mới; sau đó scp snapshot+archive metadata+hash về. Không thay worker đang chạy.

Theo AGENTS §5a.2: "Thấy ngữ cảnh đã bị nén ... ghi checkpoint ngay ... rồi đề nghị Minh mở phiên mới." Ngữ cảnh phiên đã nén; đề nghị Minh mở phiên Codex mới để tiếp cùng task từ checkpoint. Prompt tiếp thực hiện dưới đây; chưa phải prompt phản biện Claude vì task còn thiếu kết quả.

> Đọc AGENTS.md, check tiến độ và tiếp T-033 trong STATE theo SPEC đã được Minh duyệt thực hiện ngày 09/10/2026, lời "ĐÃ CHỐT". Đọc toàn SPEC và LOG phiên 2/kết thúc phiên 2. Lõi và N-Sigma nền cố định đã PASS; EC2 3.107.246.249 còn lô bocpd-factorial-rest-001 chạy tmux độc lập. Kiểm PID/status/exit/progress và hash nguồn/manifest, không khởi trùng hoặc chạy lại đơn vị PASS; theo con trỏ provenance cho ca pilot tái dùng. Tiếp các chặng còn thiếu đúng SPEC, ưu tiên tính đúng, dừng phần phụ thuộc và trình Minh khi thiết kế không ổn hoặc vượt dự toán. Guard hiện giữ mốc 11:46:29 ngày 10/10 +07 và tối đa 4 GiB mới; không tự đổi. Giữ phạm vi ghi T-033 và ràng buộc chạy song song T-032; không test/locked/heldout, không commit/push, không bật/tắt EC2. Laptop chỉ điều khiển/tài liệu/metadata, tính nghiên cứu trên EC2. Khi task hoàn tất mới soạn prompt Claude theo docs/review-prompt.md: Prompt chung + Soát kết quả + G2.
'''
with log.open('ab') as f:
    f.write(entry.encode('utf-8'))
assert log.read_bytes().startswith(log_before)
diff = []
for label, before, after in [
        ('STATE close', state_before, state.read_bytes()),
        ('LOG session 2', (opening / 'LOG.md.before').read_bytes(), log.read_bytes())]:
    diff.extend(difflib.unified_diff(before.decode('utf-8').splitlines(True),
                                    after.decode('utf-8').splitlines(True),
                                    fromfile=label + ' before', tofile=label + ' after'))
(run / 'own-diff.txt').write_text(''.join(diff), encoding='utf-8')
inventory = {str(path.relative_to(root)).replace('\\', '/'):
             {'sha256': sha(path), 'bytes': path.stat().st_size}
             for path in home.rglob('*') if path.is_file() and run not in path.parents}
result = {'status': 'PASS', 'utc': now, 'SPEC_unchanged_session2': True,
          'WHY_prefix_preserved_no_write_session2': True, 'AGENTS_unchanged': True,
          'STATE_close_only_T033': True, 'LOG_append_only': True,
          'script_AST': script_ast, 'deployed_scripts_hash_match': deployed,
          'core_records_verified': 120, 'nsigma_fixed_units_verified': 60,
          'factorial_status': status['status'], 'factorial_pid_at_snapshot': status['pid'],
          'factorial_new_cases_verified': snapshot['live_completed_cases'],
          'snapshot_sha256': sha(checkpoint / 'snapshot.json'),
          'task_complete': False, 'research_questions_closed': False,
          'result_file_inventory': inventory,
          'documentation_sha256': {str(p.relative_to(root)).replace('\\', '/'): sha(p)
                                   for p in [state, log, task / 'SPEC.md']}}
(run / 'scope-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: result[k] for k in ['status', 'core_records_verified',
                  'nsigma_fixed_units_verified', 'factorial_status',
                  'factorial_new_cases_verified', 'task_complete']}))
