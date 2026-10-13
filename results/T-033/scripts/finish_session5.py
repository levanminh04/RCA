"""T-033 session 5: documentation/hash checkpoint, no research calculation."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OPEN = ROOT / 'results/T-033/runs/session5-open-001'
OUT = ROOT / 'results/T-033/runs/session5-checkpoint-001'
TASK = ROOT / 'tasks/T-033-g2-nguyen-nhan-phat-hien'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    OUT.mkdir(exist_ok=False)
    now = datetime.now(timezone(timedelta(hours=7))).isoformat()
    command = [
        'ssh', '-i', 'D:/RCA-ext/keys/keys.pem',
        '-o', 'UserKnownHostsFile=D:/RCA-flashticket/results/T-033/runs/prepare-001/known_hosts',
        '-o', 'StrictHostKeyChecking=yes', '-o', 'BatchMode=yes',
        'ubuntu@3.107.246.249',
        'PYTHONDONTWRITEBYTECODE=1 /home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 -',
    ]
    code = """import os,time,json,psutil,subprocess,shutil
from pathlib import Path
from datetime import datetime,timezone
t0=time.perf_counter();h=Path.home()/'rca/T-033';workers=[]
for p in psutil.process_iter(['pid','cmdline']):
 try:
  c=p.info['cmdline'] or []
  if p.pid!=os.getpid() and any('T-033' in a for a in c) and any(a.endswith('.py') or a.endswith('.sh') for a in c):workers.append(p.info)
 except (psutil.NoSuchProcess,psutil.AccessDenied):pass
t=subprocess.run(['tmux','-S',str(h/'tmux.sock'),'ls'],capture_output=True,text=True)
print(json.dumps({'at':datetime.now(timezone.utc).isoformat(),'worker_candidates':workers,'tmux_stdout':t.stdout,'tmux_stderr':t.stderr,'archive_exists':(h/'runs/checkpoint-handoff-001/artifacts.tar').exists(),'logical_bytes':sum(p.stat().st_size for p in h.rglob('*') if p.is_file()),'disk_free_bytes':shutil.disk_usage(h).free,'ec2_wall_s':time.perf_counter()-t0,'no_ec2_writes':True}))
"""
    p = subprocess.run(command, input=code.encode(), capture_output=True, timeout=30)
    (OUT / 'remote-status.stderr').write_bytes(p.stderr)
    assert p.returncode == 0, p.stderr.decode()
    remote = json.loads(p.stdout)
    assert not remote['worker_candidates'] and not remote['tmux_stdout']
    assert not remote['archive_exists']
    (OUT / 'remote-status.json').write_bytes(p.stdout)
    ledger_path = ROOT / 'results/T-033/runs/session5-budget-001/ledger.json'
    ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
    stage = json.loads((OPEN / 'guard-stage-001.json').read_text(encoding='utf-8'))
    dump(OUT / 'ledger-delta.json', {
        'status': 'INCOMPLETE', 'base_ledger': '../session5-budget-001/ledger.json',
        'base_sha256': sha(ledger_path),
        'new_available_timers': [
            {'source': '../session5-open-001/guard-stage-001.json', 'pointer': '/ec2_wall_s', 's': stage['ec2_wall_s']},
            {'source': 'remote-status.json', 'pointer': '/ec2_wall_s', 's': remote['ec2_wall_s']},
        ],
        'unknown_time_s': None, 'remaining_approved_s': None,
        'scope': 'Additional control timer scopes only; process initialization/exit outside timers remain uninstrumented. Do not modify pinned base ledger or allocate new hours.',
    })
    pending = [
        'Minh accounting decision or evidence for non-reconstructible processing time',
        'Complete pilot/rest selection, lifecycle, provenance and fixtures for delay scripts; verify staged guard in complete accounting path',
        'EC2 pilot for each of three scripts, then source/flags/CP/schema/intermediate/time/RAM/bytes verification before rest',
        'Remaining delay/channel units without rerunning PASS',
        'Updated factorial group/control lock and separate input duplicate/collapse/no-channel/error denominators',
        'Manual evidence reading and synthesis in subsequent session only after computation phase passes',
    ]
    dump(OUT / 'checkpoint.json', {
        'at': now, 'reason': 'INCOMPLETE_PROCESSING_TIME_ACCOUNTING',
        'task_complete': False, 'research_phase_complete': False,
        'official_roles': {'worker': 'Codex', 'reviewer': 'Claude'},
        'archive_deleted_only_authorized_path': True,
        'source_integrity': 'PASS local 825 files and EC2 89 raw files',
        'guard_change': 'Staged, old versions preserved, two-end SHA/AST and incomplete-ledger rejection PASS; complete-accounting execution not tested',
        'channel_metadata_change': 'Only second trace-summary status dictionary key changed to status_code',
        'represented_marker_s': ledger['represented_marker_s'],
        'represented_markers_and_available_timers_s': ledger['represented_markers_and_available_timers_s'],
        'remaining_approved_s': None, 'new_research_run_started': False,
        'fixture_or_pilot_started': False, 'mechanism_conclusions': 'OPEN, none added',
        'pending': pending, 'remote_status_file': 'remote-status.json',
        'decision_register': 'Q-128/Q-129 already registered at approved followup in session 4; unchanged this session',
    })
    next_text = '''Đọc AGENTS.md, tiếp T-033 trong STATE. Codex người làm, Claude người phản biện. Chỉ dùng repo; ghi dòng mở phiên LOG.

Đọc toàn SPEC, LOG phiên 3–5; checkpoint-handoff-001 và session4-checkpoint-001 theo danh mục LOG; session5-open-001/fresh-laptop-integrity.json, remote-readonly-001.json, timing-source-verification-001.json, archive-deletion-001.json, channel-status-fix.json, guard-stage-001.json, *.complete.diff, preclose-scope-verification.json; session5-budget-001/README.md và ledger.json; session5-checkpoint-001/README.md, checkpoint.json, ledger-delta.json, remote-status.json và scope-verification.json. Đọc trực tiếp MRP RQ2/P4, DT18 NV2/NV3, advisor §1, LESSONS và WHY-41 trước diễn giải.

Phiên 5 chưa có nghiên cứu mới. Archive được duyệt đã xóa sau tự kiểm laptop; không xóa gì khác. Q-128/Q-129 đã ghi đúng quyền từ cuối phiên 4, không ghi lại. Hai time guard mới pin ledger và cộng xử lý hiện hành; bản cũ còn giữ. Cả hai test từ chối ledger INCOMPLETE; đường guard với ledger đủ chưa kiểm. Metadata trace summary đã sửa status_code, field nguồn statusCode giữ nguyên; fixture kênh chưa chạy.

Chặn cấp giờ mới: ledger chỉ tái dựng khoảng marker/timer có bằng chứng. Thiếu shell setup/exit ngoài marker; process exit sau write cuối; imports trước mkdir của checkpoint/package; các SSH kiểm/hash rời phiên 1–4. Không coi subtotal là tổng đủ, không tính lịch/khoảng nghỉ làm ngân sách xử lý, không tự đặt reserve. Đọc câu trả lời mới của Minh về cách hạch toán hoặc nguồn timing; nếu chưa có, không khởi lượt mới. Giữ phần thiếu và ảnh hưởng OPEN. Thêm ledger delta và thời gian các lệnh mới trước cấp giờ. Không tự đánh dấu accounting_valid_for_next_run hoặc đoán approved_total_processing_s.

Sau khi ngân sách được giải quyết: kiểm process/hash/source mới, không khởi trùng. Bản EC2 staged: ~/rca/T-033/scripts/session5-guard-001/{bocpd_delay.py,channel_context.py,bocpd_core.py}; ledger ~/rca/T-033/runs/session5-budget-001/ledger.json. Local source scripts có hai guard/key đã sửa; nsigma_delay.py chưa đổi. Cần hoàn thiện pilot/rest, lifecycle/source pin/fixture theo SPEC trước CLI; không gọi toàn lô hiện có. Từng script ca đầu trên EC2 pin; fixture/intermediate/time/flags/CP/schema và tài nguyên đạt mới rest; giữ đơn vị PASS qua nguồn hash, không chạy lại. Chạy dài độc lập laptop/SSH, progress/stdout/stderr/PID/status/lệnh xem LOG và tự dừng lỗi. Không chọn tham số/tiêu chí mới.

Cập nhật khóa nhóm/đối chứng sau factorial và trước diễn giải theo SPEC, giữ input trùng/collapse hợp lệ/no-channel/error và mẫu số riêng. Chưa viết kết luận cơ chế/tổng hợp trong chặng tính. Phần chưa phân xử phải có đúng bằng chứng cần.

Chỉ ghi results/T-033/, LOG nối, duy nhất dòng T-033 STATE đọc ngay trước sửa, EC2 ~/rca/T-033/. Không SPEC/DECISIONS/WHY/nguồn cũ, test/locked/heldout/T-032, package install, commit/push/bật-tắt EC2. Laptop chỉ tài liệu/điều khiển/nhận/hash. Báo CẦN GIỮ LAPTOP MỞ khi pilot, nêu lý do/ước lượng/mốc báo lại. Chỉ báo EC2 T-033 ĐÃ ỔN ĐỊNH sau ca đầu kiểm đủ tài nguyên/ngân sách và lỗi tự dừng. Ngữ cảnh nén checkpoint và đề nghị phiên mới.

Cuối phiên LOG đủ AGENTS §7, last command/bước tiếp cụ thể, STATE chỉ dòng T-033, EC2 và việc Minh cần làm. Chỉ khi chặng tính đạt mới soạn prompt đọc tay+tổng hợp. Chỉ khi task hoàn tất mới soạn prompt phản biện Claude theo nguyên văn Common + Soát kết quả + G2; không tự gửi/mở review.
'''
    (OUT / 'prompt-next-session.md').write_text(next_text, encoding='utf-8')
    report = f'''

### Kết thúc phiên 5 — {now} — dừng phần cấp giờ vì ledger chưa đủ

1. Đã làm: dùng repo mở phiên và kiểm nguồn/checkpoint; tự đọc đủ ba script và native, MRP RQ2/P4, DT18 NV2/NV3, advisor §1, LESSONS và WHY-41. Q-128/Q-129 đã có hiệu lực và được ghi sổ từ bổ sung cuối phiên 4; không ghi lại. Tự kiểm mới laptop825 và raw EC2 89 file; xóa duy nhất archive được duyệt. Sửa key metadata status_code và đúng time guard hai script, giữ bản cũ/hash hai đầu. Dựng ledger mọi lượt tìm được, giữ phần thiếu OPEN. Không khởi nghiên cứu/fixture/pilot mới, không viết kết luận cơ chế.
2. File thay đổi: scripts/bocpd_delay.py và scripts/channel_context.py trong results/T-033/; scripts/finish_session5.py (tài liệu/checkpoint), runs/session5-open-001/, session5-budget-001/, session5-checkpoint-001/; LOG chỉ nối; duy nhất dòng T-033 STATE. EC2 chỉ thêm scripts/session5-001/, scripts/session5-guard-001/, runs/session5-budget-001/ và xóa đúng runs/checkpoint-handoff-001/artifacts.tar. Không đổi native/adapter/env/raw, SPEC, AGENTS, DECISIONS/WHY/MRP/LESSONS/review-prompt, T-032 hoặc test/locked/heldout; không commit/push/bật/tắt EC2.
3. Kiểm: laptop825/825 file, 1393611373 byte PASS theo inventory; native/source pin và 89/89 raw EC2, 656358942 byte PASS. Archive byte trước 2791021314 → sau 1395923714, giảm đúng1395097600 byte, không xóa khác. AST ngoài guard và key status_code giữ nguyên; hai hash local/EC2 và AST đạt; cả hai guard từ chối ledger thiếu đúng BUDGET_LEDGER_INCOMPLETE. Bằng chứng trong session5-open-001/*.json/*.diff; script nguyên guard cũ được giữ. Guard đường accounting đầy đủ/fixture/pilot/rest chưa kiểm, không gọi staged script sẵn sàng chạy toàn lô. Hash/byte tài liệu và LOG prefix/phạm vi kiểm trong scope-verification.json.
4. OPEN: represented_marker_s={ledger['represented_marker_s']}, khoảng 5,315301530 giờ, và timer điều khiển riêng không chứng minh tổng xử lý đầy đủ. Ledger còn thiếu setup/exit ngoài marker và SSH/hash rời phiên1–4; unknown_time_s và remaining_approved_s null. Last-write không là upper bound toàn process. Thiếu này chặn cấp giờ/run mới trong trần12h; đã hỏi Minh cung cấp timing hoặc quyết hạch toán, không tự đặt reserve. Có thêm timer guard/test và remote-status trong ledger-delta.json, chưa sửa ledger pin cũ. Chặng tính còn thiếu lifecycle/provenance/pilot-rest/fixtures, ba pilot/time-RAM-byte-schema-CP-flags, rest độ trễ/kênh và khóa nhóm mới. RQ2/P4/G2/P6 chưa được phân xử thêm; đọc tay/tổng hợp vẫn chưa bắt đầu. Không loại nghĩa vụ nghiên cứu vì chặn ngân sách; cần giải quyết ledger rồi làm đủ theo SPEC.

EC2: kiểm mới ở {remote['at']}, không worker/tmux T-033, archive không còn; byte hiện hành {remote['logical_bytes']}, disk free {remote['disk_free_bytes']}. Minh có thể tắt laptop trong lúc chờ vì không có pilot/worker mới; EC2 còn cần cho phần tính, agent không bật/tắt máy. Chưa báo EC2 lượt mới ổn định. Việc Minh cần làm: chốt hạch toán phần thời gian không tái dựng hoặc cung cấp timing còn thiếu.

Bước tiếp chính xác: đọc session5-budget-001/ledger.json#/open và session5-checkpoint-001/ledger-delta.json; kiểm câu trả lời Minh trước mọi cấp giờ. Chưa có trả lời thì chỉ đọc/kiểm điều khiển cần thiết, không chạy CLI. Sau giải quyết, kiểm SSH chỉ đọc `tail -n 20 ~/rca/T-033/trang-thai.txt` với key/known_hosts README, process và source/hash mới. Hoàn thiện điều phối/fixture đúng SPEC rồi mới chạy từng pilot; không chạy lại đơn vị PASS. Prompt nối cùng chặng ở session5-checkpoint-001/prompt-next-session.md; đây không là prompt đọc tay+tổng hợp hay phản biện Claude. Task chưa hoàn tất nên chưa soạn phản biện chính thức.

Lệnh cuối chốt: `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -X utf8 results/T-033/scripts/finish_session5.py` (tài liệu/hash/SSH metadata chỉ đọc). Lệnh EC2 cuối: Python pin qua SSH stdin kiểm process/tmux/byte/disk/archive; script nguyên văn nằm trong finish_session5.py, kết quả remote-status.json và timer trong ledger-delta.json. Lệnh pilot còn chưa được tạo/kiểm; không đoán hoặc dùng CLI toàn lô hiện có.
'''
    with (TASK / 'LOG.md').open('a', encoding='utf-8', newline='') as f:
        f.write(report)
    # Re-read the shared STATE immediately before modifying only T-033.
    state_path = ROOT / 'docs/STATE.md'
    state_before = state_path.read_bytes()
    (OUT / 'STATE.md.before-close').write_bytes(state_before)
    lines = state_before.splitlines(keepends=True)
    indexes = [i for i, line in enumerate(lines) if line.startswith(b'| T-033 |')]
    assert len(indexes) == 1
    i = indexes[0]
    parts = lines[i].decode().split('|')
    parts[6] = ' Đang thực hiện (phiên 5, 11/10): laptop825/raw89 hash đạt; đã xóa đúng archive và sửa key status_code/time guard, bản cũ giữ. Ledger khoảng marker 5,3153h còn thiếu thời gian, dừng cấp giờ mới/chờ Minh hạch toán; không worker/pilot mới. Checkpoint session5-checkpoint-001; độ trễ/kênh, khóa nhóm/đọc tay/tổng hợp còn chưa chạy '
    lines[i] = '|'.join(parts).encode()
    state_path.write_bytes(b''.join(lines))
    assert [v for v in state_before.splitlines(keepends=True) if not v.startswith(b'| T-033 |')] == [v for v in state_path.read_bytes().splitlines(keepends=True) if not v.startswith(b'| T-033 |')]
    assert (TASK / 'LOG.md').read_bytes().startswith((OPEN / 'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md').read_bytes())
    baseline = json.loads((OPEN / 'baseline.json').read_text(encoding='utf-8'))
    protected = ['AGENTS.md', 'docs/DECISIONS.md', 'docs/MRP.md', 'docs/LESSONS.md', 'docs/WHY.md', 'docs/review-prompt.md', 'tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md']
    protected_checks = {name: sha(ROOT / name) == baseline[name]['sha256'] for name in protected}
    assert all(protected_checks.values())
    dump(OUT / 'scope-verification.json', {'status': 'PASS', 'LOG_append_only': True, 'STATE_only_T033': True, 'protected_documents_unchanged': protected_checks, 'source_or_spec_changed': False, 'research_new_run_started': False})
    (OUT / 'README.md').write_text(f'''# T-033 — Checkpoint phiên 5

Chốt {now}. Codex người làm, Claude phản biện. Task/chặng tính chưa hoàn tất; không có run nghiên cứu mới. Dừng cấp giờ vì ledger chưa đủ, theo yêu cầu Minh về thời gian không tái dựng.

- Laptop825 và raw EC2 89 file hash/byte PASS. Đã xóa duy nhất archive được duyệt, byte trước/sau và SHA tại `../session5-open-001/archive-deletion-001.json`.
- Key trace summary status_code đã sửa tối thiểu. Hai time guard cộng dồn đã stage và hash hai đầu; kiểm EC2 từ chối ledger thiếu đạt. AST ngoài guard/key giữ nguyên; bản cũ trong `../session5-open-001/scripts/`. Đường guard hợp lệ/fixture/pilot còn chưa kiểm.
- `../session5-budget-001/ledger.json`: từng khoảng marker/timer, phần thiếu và owner. Khoảng marker không là tổng đủ hoặc upper bound mọi process. `remaining_approved_s` null. `ledger-delta.json`: timer mới sau ledger pin, cần hạch toán trước run sau.
- `remote-status.json`: không worker/tmux, archive không còn, byte/disk mới. Laptop có thể tắt trong lúc chờ; EC2 còn cần cho phần tính, agent không bật/tắt máy. Không gọi lượt mới ổn định.
- `checkpoint.json` và `prompt-next-session.md`: phần đã/chưa làm, nguồn/file/lệnh/phạm vi. Đây là nối chặng tính, chưa chuyển đọc tay+tổng hợp hay Claude review chính thức.
- `scope-verification.json`: LOG chỉ nối, STATE chỉ T-033, tài liệu nguồn giữ nguyên. Manifest khóa các file checkpoint này.

Cần Minh quyết cách hạch toán các đoạn xử lý không tái dựng hoặc bổ sung timing. Không tự đặt reserve, đánh dấu ledger đầy đủ hoặc cấp `12 − subtotal` giờ.
''', encoding='utf-8')
    dump(OUT / 'manifest.json', {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size} for p in OUT.iterdir() if p.is_file() and p.name != 'manifest.json'})
    print(json.dumps({'status': 'PASS', 'checkpoint': str(OUT), 'task_complete': False, 'remote_workers': remote['worker_candidates'], 'remaining_approved_s': None}, ensure_ascii=False))


if __name__ == '__main__':
    main()
