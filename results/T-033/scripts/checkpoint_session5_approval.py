"""Persist Minh's approved 8h + 4h accounting and stop after context compression.

Document/hash operations only. Does not connect to EC2 or execute research.
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib
import json
import re
import difflib

ROOT = Path('D:/RCA-flashticket')
OUT = ROOT / 'results/T-033/runs/session5-approval-checkpoint-001'
LOG = ROOT / 'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'
DECISIONS = ROOT / 'docs/DECISIONS.md'
STATE = ROOT / 'docs/STATE.md'
OLD_LEDGER = ROOT / 'results/T-033/runs/session5-budget-001/ledger.json'
LAST_COMMAND = ('D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -X utf8 '
                'results/T-033/scripts/checkpoint_session5_approval.py')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if OUT.exists():
    raise SystemExit('Checkpoint exists; read it, do not repeat append operations.')
at = datetime.now(timezone(timedelta(hours=7))).isoformat()
dec_before = DECISIONS.read_bytes()
log_before = LOG.read_bytes()
state_before = STATE.read_bytes()
ledger_before = OLD_LEDGER.read_bytes()
assert sha(ledger_before) == '680ddbbd8cca8e6adeeda82381baefb8a3329d8bf45ab67c9d64a1ef48da2b42'
old_ledger = json.loads(ledger_before)
previous_checkpoint = json.loads((ROOT / 'results/T-033/runs/session5-checkpoint-001/checkpoint.json').read_text(encoding='utf-8'))
assert previous_checkpoint['new_research_run_started'] is False
assert old_ledger['accounting_valid_for_next_run'] is False
codes = [int(n) for n in re.findall(rb'\| Q-(\d+) \|', dec_before)]
code = f'Q-{max(codes) + 1}'
assert code == 'Q-132', 'Decision register changed; inspect before appending.'

protected = [
    ROOT / 'AGENTS.md',
    ROOT / 'tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md',
    ROOT / 'docs/WHY.md', ROOT / 'docs/MRP.md', ROOT / 'docs/LESSONS.md',
    ROOT / 'docs/review-prompt.md', OLD_LEDGER,
    ROOT / 'results/T-033/scripts/nsigma_delay.py',
    ROOT / 'results/T-033/scripts/bocpd_delay.py',
    ROOT / 'results/T-033/scripts/channel_context.py',
    ROOT / 'results/T-033/scripts/bocpd_core.py',
]
protected_before = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in protected}
OUT.mkdir(parents=True, exist_ok=False)
for name, data in [('DECISIONS.md.before', dec_before), ('LOG.md.before', log_before), ('STATE.md.before', state_before)]:
    (OUT / name).write_bytes(data)

approval = {
    'at_recorded': at,
    'task': 'T-033',
    'decision': code,
    'classification': 'USER_CONFIRMED',
    'user_reply_verbatim': 'duyệt',
    'approved_proposal': (
        'Hạch toán chặng cũ là 8 giờ, dành tối đa 4 giờ xử lý cho phần tiếp theo, '
        'đồng thời cho lưu quyết định vào DECISIONS. 8 giờ là mức hạch toán dự phòng, '
        'chưa kiểm; không phải số đo thực tế.'
    ),
    'approved_prior_processing_s': 28800,
    'approved_max_new_processing_s': 14400,
    'accounting_total_cap_s': 43200,
    'historical_actual_processing_s': None,
    'historical_actual_status': 'OPEN; cannot be fully reconstructed from retained timing evidence',
    'scope': 'Accounting resolution and recording this decision only; existing SPEC/run approvals remain in effect',
    'research_permission_expanded': False,
    'no_new_ec2_processing_since_approval_in_this_supplement': True,
}
save_json(OUT / 'approval.json', approval)
accounting = {
    'at': at, 'task': 'T-033', 'status': 'APPROVED_ACCOUNTING_BASELINE',
    'decision': code, 'source_sha256': old_ledger['source_sha256'],
    'budget_compute_s': 43200,
    'accounting_valid_for_next_run': True,
    'approved_total_processing_s': 28800,
    'approved_prior_processing_s': 28800,
    'approved_max_new_processing_s': 14400,
    'new_processing_charged_s': 0,
    'remaining_approved_s': 14400,
    'remaining_basis': 'Administrative allocation at approval; not a measured residual from actual historical processing',
    'historical_actual_processing_s': None, 'unknown_time_s': None,
    'historical_actual_status': 'OPEN',
    'represented_marker_s': old_ledger['represented_marker_s'],
    'represented_markers_and_available_timers_s': old_ledger['represented_markers_and_available_timers_s'],
    'historical_ledger': 'results/T-033/runs/session5-budget-001/ledger.json',
    'historical_ledger_sha256': sha(ledger_before),
    'historical_delta': 'results/T-033/runs/session5-checkpoint-001/ledger-delta.json',
    'open': old_ledger['open'],
    'next_run_requirements': [
        'Time every EC2 processing run/check after approval, including failed runs; sum charged wall across separate runs',
        'Do not use calendar elapsed time or only completed-status subtotals as total processing',
        'Create and pin a fresh per-run ledger snapshot containing 28800 plus all subsequent processing charges',
        'Update only the approved guard path/hash to the approved accounting snapshot; preserve old script/ledger versions and verify both ends',
        'Current staged guards still pin the old incomplete ledger; this document does not launch or validate a pilot',
    ],
}
save_json(OUT / 'approved-accounting.json', accounting)

decision_row = (
    f'\n| {code} | 11/10/2026 | T-033: Minh duyệt hạch toán chặng cũ là 8 giờ, '
    'dành tối đa 4 giờ xử lý cho phần tiếp theo trong trần hạch toán 12 giờ, '
    'và lưu quyết định này vào DECISIONS. 8 giờ là mức hạch toán dự phòng, chưa kiểm; '
    'không phải số đo thực tế. Thời gian thực tế cũ không tái dựng đầy đủ vẫn OPEN. '
    'Các lượt xử lý mới, gồm lượt hỏng và kiểm, phải cộng dồn trong phần tối đa 4 giờ; '
    'không mở rộng phạm vi SPEC hay quyền khác. | Minh trả lời nguyên văn "duyệt" '
    'cho đề xuất hạch toán 8 giờ cũ + tối đa 4 giờ mới và lưu DECISIONS, chat ngày '
    '11/10/2026; LOG T-033 bổ sung phiên 5; '
    'results/T-033/runs/session5-approval-checkpoint-001/approval.json |\n'
)
# Decision source of truth first, before derived LOG/STATE/checkpoint references.
assert DECISIONS.read_bytes() == dec_before
with DECISIONS.open('ab') as f:
    f.write(decision_row.encode('utf-8'))

prompt = '''Đọc AGENTS.md, tiếp T-033 trong STATE. Codex là người làm, Claude là người phản biện. Phiên mới chỉ dùng repo; ghi dòng mở phiên vào LOG.

Đọc toàn SPEC T-033, LOG phiên 3, 4, 5 và bổ sung cuối phiên 5; checkpoint-handoff-001/README.md, snapshot.json, artifact-locator.json, output-presence.json; session4-checkpoint-001/README.md, checkpoint.json, integrity-verification.json, remote-status.json, script-reading-evidence.json, script-reading-notes.md; session5-open-001/ các bằng chứng mới; session5-budget-001/ledger.json; session5-checkpoint-001/; và checkpoint mới session5-approval-checkpoint-001/README.md, checkpoint.json, approval.json, approved-accounting.json, scope-verification.json, manifest.json. Đọc trực tiếp MRP RQ2/P4, DT18 NV2/NV3, advisor §1, LESSONS và WHY-41 trước diễn giải.

Q-128/Q-129 đã có trong DECISIONS. Minh đã duyệt Q-132 ngày 11/10/2026: hạch toán chặng cũ 8 giờ, tối đa 4 giờ xử lý mới, cho lưu quyết định; đã ghi DECISIONS và LOG. Đây là mức quản lý ngân sách dự phòng, chưa kiểm, không phải số đo thực tế. Thời gian cũ không tái dựng vẫn OPEN nhưng không còn chờ duyệt hạch toán. Giữ ledger lịch sử nguyên trạng; dùng approved-accounting.json làm căn cứ dựng snapshot ledger mới trước từng run. Mọi lượt xử lý EC2 sau lời duyệt, gồm hỏng và kiểm, phải được đo và cộng trong tối đa 4 giờ mới; không lấy lịch hoặc subtotal status làm ngân sách đủ.

Phiên 5 dừng vì ngữ cảnh bị nén theo AGENTS §5a.2. Không có nghiên cứu/fixture/pilot mới. Laptop 825 file và raw EC2 89 file đã tự kiểm hash PASS; archive duy nhất được duyệt đã xóa, byte trước/sau nằm trong archive-deletion-001.json, không xóa gì nữa. Key metadata status_code đã sửa tối thiểu, bản cũ giữ/hash hai đầu. Guard đã bỏ mốc lịch và kiểm ledger thiếu PASS; staged guard vẫn pin ledger cũ chưa đầy đủ nên phải cập nhật đúng guard sang ledger mới, giữ bản cũ/hash hai đầu và kiểm đường accounting hợp lệ trước chạy. Các trợ lý trước chỉ tự soát chỉ đọc; không thay tự kiểm Codex hay phản biện Claude.

Làm tiếp chặng tính đã duyệt: tự kiểm process/hash/source mới, không khởi trùng. Hoàn thiện điều phối/pilot-rest/provenance/fixture theo SPEC sau đọc đủ nsigma_delay.py, bocpd_delay.py, channel_context.py và native; không thay tham số/tiêu chí/SPEC. Giữ các bản cũ trong thư mục lượt mới. Laptop chỉ điều khiển/tài liệu/nhận/kiểm hash; tính nghiên cứu dùng pin EC2. Mỗi script chạy ca đầu EC2; fixture/intermediates/source/time/flags/CP/schema và time/RAM/byte/ngân sách đạt mới chạy rest. Tái dùng đơn vị PASS theo nguồn hash. Lượt dài tmux/nohup độc lập SSH/laptop, progress/stdout/stderr/PID/status/lệnh xem ở LOG, tự dừng khi lỗi. Cập nhật khóa nhóm/đối chứng sau phân rã và trước diễn giải; giữ riêng input trùng, collapse hợp lệ, không kênh, lỗi và mẫu số từng loại.

Báo CẦN GIỮ LAPTOP MỞ khi kiểm pilot, kèm lý do/ước lượng/mốc báo lại. Chỉ báo EC2 T-033 ĐÃ ỔN ĐỊNH — Minh có thể tắt laptop sau pilot kiểm đạt và đo đủ tài nguyên/ngân sách/lỗi tự dừng; kèm run/ước lượng xong/lệnh tiến độ/việc tiếp khi mở lại. Không viết kết luận cơ chế hay báo cáo tổng hợp trong chặng tính. Thiết kế không phân xử được/hash hoặc CP lệch/sắp vượt trần thì checkpoint, dừng phần phụ thuộc và trình Minh; không tự đổi cách làm. Ngữ cảnh nén thì checkpoint ngay và đề nghị phiên mới.

Phạm vi ghi: results/T-033/, LOG chỉ nối, duy nhất dòng T-033 STATE (đọc ngay trước sửa), EC2 ~/rca/T-033/. Không ghi DECISIONS thêm ngoài quyết định đã lưu, nguồn cũ, SPEC, WHY, test/locked/heldout, T-032; không cài package, commit/push hoặc bật/tắt EC2. Cuối phiên LOG đủ AGENTS §7, last command/bước tiếp chính xác, STATE đúng dòng T-033, trạng thái EC2/việc Minh cần làm. Chỉ khi chặng tính đạt mới soạn prompt phiên tiếp đọc tay+tổng hợp; chỉ khi task hoàn tất mới soạn prompt Claude theo nguyên văn Common + Soát kết quả + G2 trong docs/review-prompt.md, không tự gửi/mở review.
'''
(OUT / 'prompt-next-session.md').write_text(prompt, encoding='utf-8')
checkpoint = {
    'at': at, 'reason': 'CONTEXT_COMPRESSED_AGENTS_5A_2',
    'task_complete': False, 'research_phase_complete': False,
    'official_roles': {'worker': 'Codex', 'reviewer': 'Claude'},
    'decision_registered': code,
    'budget_approval_pending': False,
    'accounting': '8h administrative old-phase charge plus at most 4h new processing; actual old processing remains OPEN',
    'approved_accounting': 'approved-accounting.json',
    'no_new_ec2_command_since_approval': True,
    'new_research_run_started': False, 'fixture_or_pilot_started': False,
    'prior_preparation_checkpoint': 'results/T-033/runs/session5-checkpoint-001/checkpoint.json',
    'last_ec2_evidence': 'results/T-033/runs/session5-checkpoint-001/remote-status.json',
    'last_ec2_observation_utc': '2026-10-11T00:32:01.999369+00:00',
    'ec2_at_last_observation': 'No T-033 worker or tmux session; archive removed. Must check fresh before launch.',
    'scripts_still_pin_incomplete_old_ledger': True,
    'pending': [
        'Fresh process/source/hash check with processing time measurement',
        'New ledger snapshot, approved guard path/hash update and valid-accounting verification',
        'Pilot/rest lifecycle, provenance, fixtures and full independent worker self-check for all three scripts',
        'One EC2 pilot per script, then resource/budget/source/time/flags/CP/schema/intermediate checks before rest',
        'Rest delay/channel processing using existing PASS units without rerun',
        'Updated factorial group/control lock with four distinct categories and their denominators',
        'Manual evidence reading and synthesis in a subsequent session after computation phase passes',
    ],
    'last_command': LAST_COMMAND,
    'next_step': 'Open a fresh Codex session with prompt-next-session.md; read governing sources, log session opening, inspect and hash checkpoint, then instrument fresh EC2 check and prepare approved ledger/guards before any pilot',
}
save_json(OUT / 'checkpoint.json', checkpoint)

log_addition = f'''

### Bổ sung phiên 5 — {at} — Minh duyệt hạch toán 8 giờ cũ + tối đa 4 giờ mới; checkpoint do ngữ cảnh nén

Quyết định của Minh trong lượt: Codex đề xuất “hạch toán chặng cũ là 8 giờ, dành tối đa 4 giờ xử lý cho phần tiếp theo, đồng thời cho lưu quyết định vào DECISIONS. 8 giờ là mức hạch toán dự phòng, chưa kiểm; không phải số đo thực tế.” Minh trả lời nguyên văn: “duyệt”. Đã nối {code} đúng quyền này vào docs/DECISIONS.md trước cập nhật tài liệu dẫn xuất. Lời duyệt không mở rộng nghiên cứu, quyền ghi hoặc tiêu chí. Phần chờ hạch toán trong mục kết thúc phiên 5 trước đó đã được giải quyết bởi {code}; thời gian thực tế lịch sử vẫn OPEN, không chuyển thành số đo 8 giờ.

1. Đã làm: lưu lời duyệt và baseline quản lý 28800 giây cũ, tối đa 14400 giây xử lý mới; giữ nguyên ledger lịch sử và delta. Ngữ cảnh vừa nén, checkpoint ngay theo AGENTS §5a.2; không tiếp chạy nghiên cứu trong phiên này. Không có lệnh EC2 mới từ sau lời duyệt. Guard staged còn pin ledger cũ thiếu; chưa gọi là sẵn sàng chạy. Không còn lời duyệt ngân sách đang chờ để tiếp chặng tính trong SPEC.
2. File thay đổi: nối duy nhất {code} vào docs/DECISIONS.md; LOG chỉ nối; duy nhất dòng T-033 trong docs/STATE.md; results/T-033/scripts/checkpoint_session5_approval.py và runs/session5-approval-checkpoint-001/. Không sửa ledger cũ, script detector/độ trễ/kênh, nguồn/native/adapter/env/raw, SPEC, WHY/MRP/LESSONS/AGENTS/review-prompt. Không đổi EC2, không xóa thêm, không commit/push.
3. Kiểm: ledger lịch sử khớp hash pin cũ; DECISIONS/LOG giữ nguyên prefix, STATE chỉ đổi dòng T-033; protected source/script/doc hashes giữ nguyên. Manifest checkpoint kiểm byte/hash mọi file mới; kết quả chi tiết trong scope-verification.json. Không kiểm fixture/pilot/rest hay đường guard ledger hợp lệ trong lượt này; tự kiểm cũ không thay kiểm ca đầu.
4. OPEN: tổng thời gian thực tế cũ không tái dựng đầy đủ, không thể chứng nhận bằng mức hạch toán 8 giờ. Đây đã là giới hạn được Minh chấp nhận về quản lý ngân sách, không chặn cấp tối đa 4 giờ mới. Mọi lượt xử lý mới, kể cả hỏng/kiểm, phải đo/cộng dồn trước mỗi launch. Chặng tính vẫn thiếu điều phối/fixtures/pilot-rest/provenance, ca đầu ba script và time/RAM/bytes/flags/CP/schema, các đơn vị rest và khóa nhóm mới. RQ2/P4/G2 chưa có bằng chứng mới để phân xử; cơ chế/đọc tay/tổng hợp chưa làm, không ghi task hoàn tất hay chờ phản biện.

EC2: bằng chứng cuối vẫn là session5-checkpoint-001/remote-status.json ở 2026-10-11T00:32:01.999369+00:00, không worker/tmux T-033, archive đã xóa. Lượt này không SSH và không khởi pilot/worker. Trước launch phải kiểm trạng thái mới; không tuyên bố lượt EC2 mới ổn định. Minh có thể đóng laptop giữa phiên vì Codex chưa khởi lượt xử lý mới; không yêu cầu bật/tắt EC2.

Bước tiếp chính xác: mở phiên Codex mới bằng results/T-033/runs/session5-approval-checkpoint-001/prompt-next-session.md. Đọc các nguồn/chặng/checkpoint đã liệt kê, ghi dòng mở phiên; kiểm manifest/hash. Dựng ledger snapshot mới từ approved-accounting.json ({code}) cộng timer của mọi lượt kiểm/xử lý từ sau duyệt; kiểm process/hash/source EC2 mới có đo thời gian; cập nhật đúng guard sang ledger mới, giữ bản cũ/hash hai đầu và kiểm đường accounting hợp lệ. Sau đó hoàn thiện và tự kiểm điều phối rồi chạy từng pilot đúng SPEC, đạt mới rest, không chạy lại PASS. CLI pilot chưa hoàn thiện/kiểm nên không bịa lệnh launch. Kết nối SSH chuẩn: key D:/RCA-ext/keys/keys.pem, known_hosts results/T-033/runs/prepare-001/known_hosts, BatchMode/StrictHostKeyChecking=yes, ubuntu@3.107.246.249; Python pin /home/ubuntu/rca/T-025/envs/main/bin/python, không cài package. Prompt này là nối chặng tính, không là prompt đọc tay+tổng hợp hay phản biện Claude.

Lệnh cuối lượt: `{LAST_COMMAND}` (chỉ tài liệu/hash/checkpoint laptop). Lệnh EC2 cuối không đổi: Python pin qua SSH stdin trong results/T-033/scripts/finish_session5.py kiểm process/tmux/byte/disk/archive; stdout/timer ở session5-checkpoint-001/remote-status.json và ledger-delta.json. Không còn việc cần Minh duyệt để thực hiện chặng tính hiện tại; việc Minh cần làm vì ngữ cảnh nén là mở phiên mới theo AGENTS §5a.2. Sau khi chặng tính đạt, phiên sau đọc tay/tổng hợp; prompt phản biện chính thức chỉ soạn khi task hoàn tất.
'''
assert LOG.read_bytes() == log_before
with LOG.open('ab') as f:
    f.write(log_addition.encode('utf-8'))

# Fresh STATE read immediately before changing only the T-033 row.
fresh_state = STATE.read_bytes()
assert fresh_state == state_before
state_lines = fresh_state.decode('utf-8').splitlines(keepends=True)
matches = [i for i, line in enumerate(state_lines) if line.startswith('| T-033 |')]
assert len(matches) == 1
i = matches[0]
cells = state_lines[i].rstrip('\r\n').split('|')
assert len(cells) == 9
cells[6] = (' Đang thực hiện (phiên 5, 11/10): chuẩn bị/hash/xóa archive/key status_code và guard ledger thiếu đạt; '
            f'{code} đã duyệt và lưu: hạch toán cũ 8h + tối đa 4h xử lý mới, thời gian thực tế cũ OPEN. '
            'Ngữ cảnh nén → checkpoint session5-approval-checkpoint-001, mở phiên mới; chưa pilot/rest độ trễ/kênh/khóa nhóm. '
            'Guard còn pin ledger cũ; không worker mới được khởi ')
old_row = state_lines[i]
ending = '\r\n' if old_row.endswith('\r\n') else '\n'
state_lines[i] = '|'.join(cells) + ending
STATE.write_bytes(''.join(state_lines).encode('utf-8'))

readme = f'''# T-033 — checkpoint bổ sung lời duyệt {code}

Ghi {at}, Codex là người làm, Claude là người phản biện. Phiên dừng vì ngữ cảnh nén (AGENTS §5a.2); không có nghiên cứu mới.

Minh đã duyệt hạch toán chặng cũ 8 giờ và tối đa 4 giờ xử lý mới, cho lưu DECISIONS. 8 giờ là mức quản lý dự phòng, chưa kiểm; không phải số đo. Thời gian thực tế cũ vẫn OPEN. Không còn chờ duyệt hạch toán trong phạm vi này.

`approval.json` giữ lời duyệt và đề xuất được duyệt. `approved-accounting.json` giữ baseline quản lý, nguồn ledger lịch sử và yêu cầu cộng mọi lượt mới kể cả hỏng/kiểm. Ledger lịch sử không đổi. Đây chưa là ledger staged được guard pin: phải tạo snapshot theo thời gian đã cộng và cập nhật đúng guard/hash trước launch.

`checkpoint.json` chứa trạng thái/việc còn lại. `scope-verification.json` kiểm phạm vi/prefix/hash. `manifest.json` kiểm byte/hash file checkpoint. `prompt-next-session.md` là prompt nối chặng tính cho phiên Codex mới; chưa là prompt tổng hợp hay phản biện chính thức.

Không có SSH mới trong bổ sung này. Bằng chứng EC2 cuối trong session5-checkpoint-001/remote-status.json, ở 2026-10-11T00:32:01.999369+00:00: không T-033 worker/tmux. Kiểm mới trước launch. Archive đã xóa đúng một file trong phiên 5, không xóa lại. Chưa pilot/fixture/rest/khóa nhóm.

Lệnh cuối: `{LAST_COMMAND}`. Bước tiếp: mở phiên mới với prompt, đọc nguồn/LOG/checkpoint, ghi mở phiên, kiểm hash rồi hoàn thiện ledger/guard/điều phối và ca đầu theo SPEC. Không cần xin lại duyệt cho việc trong SPEC đã duyệt.
'''
(OUT / 'README.md').write_text(readme, encoding='utf-8')

after_state_lines = STATE.read_bytes().decode('utf-8').splitlines(keepends=True)
before_state_lines = state_before.decode('utf-8').splitlines(keepends=True)
changed_rows = [n + 1 for n, (a, b) in enumerate(zip(before_state_lines, after_state_lines)) if a != b]
assert len(before_state_lines) == len(after_state_lines)
assert changed_rows == [i + 1]
assert DECISIONS.read_bytes() == dec_before + decision_row.encode('utf-8')
assert LOG.read_bytes() == log_before + log_addition.encode('utf-8')
assert sha(OLD_LEDGER.read_bytes()) == sha(ledger_before)
protected_after = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in protected}
assert protected_before == protected_after
doc_diff = ''.join(''.join(difflib.unified_diff(
    before.decode('utf-8').splitlines(keepends=True),
    path.read_bytes().decode('utf-8').splitlines(keepends=True),
    fromfile=str(path.relative_to(ROOT)) + ' (before)',
    tofile=str(path.relative_to(ROOT)) + ' (after)'))
    for path, before in [(DECISIONS, dec_before), (LOG, log_before), (STATE, state_before)])
(OUT / 'approved-docs.diff').write_text(doc_diff, encoding='utf-8')
verification = {
    'status': 'PASS', 'at': at,
    'decisions_exact_approved_append': True, 'decision_code': code,
    'log_prefix_unchanged': True, 'state_changed_rows': changed_rows,
    'state_changed_task': 'T-033', 'protected_hashes_unchanged': True,
    'protected_hashes': protected_after,
    'old_ledger_unchanged': True,
    'approved_accounting_s': {'old': 28800, 'new_max': 14400, 'cap': 43200},
    'historical_actual_remains_open': True,
    'new_ec2_processing_or_research': False,
    'script': {'path': str(Path(__file__).relative_to(ROOT)), 'sha256': sha(Path(__file__).read_bytes())},
    'new_checkpoint_files': sorted(p.name for p in OUT.iterdir() if p.is_file()),
}
save_json(OUT / 'scope-verification.json', verification)
files = [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
         for p in sorted(OUT.iterdir()) if p.is_file()]
manifest = {'at': at, 'task': 'T-033', 'files': files, 'self_excluded': 'manifest.json'}
save_json(OUT / 'manifest.json', manifest)
for item in files:
    path = OUT / item['path']
    assert path.stat().st_size == item['bytes'] and sha(path.read_bytes()) == item['sha256']
print(json.dumps({'status': 'PASS', 'decision': code, 'checkpoint': str(OUT),
                  'manifest_files_verified': len(files), 'state_row': i + 1,
                  'new_ec2_processing': False, 'new_research': False}, ensure_ascii=False))
print(doc_diff)
