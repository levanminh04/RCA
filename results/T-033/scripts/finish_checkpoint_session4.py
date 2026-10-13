"""Close the interrupted session with documents and integrity checks only."""
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-033/runs/session4-checkpoint-001'
OLD = ROOT / 'results/T-033/runs/checkpoint-handoff-001'
TASK = ROOT / 'tasks/T-033-g2-nguyen-nhan-phat-hien'


def sha_bytes(data):
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    now = datetime.now().astimezone().isoformat()
    integrity = json.loads((OUT / 'integrity-verification.json').read_text(encoding='utf-8'))
    remote = json.loads((OUT / 'remote-status.json').read_text(encoding='utf-8'))
    scripts = json.loads((OUT / 'script-reading-evidence.json').read_text(encoding='utf-8'))
    historical = json.loads((OLD / 'handoff-manifest.json').read_text(encoding='utf-8'))
    assert integrity['status'] == 'PASS' and integrity['checked_files'] == 825
    assert remote['worker_candidates'] == [] and remote['archive_deleted'] is False
    unchanged_scripts = {}
    for name, expected in scripts['scripts'].items():
        actual = sha_bytes((ROOT / 'results/T-033/scripts' / name).read_bytes())
        assert actual == expected, name
        unchanged_scripts[name] = actual
    log_path = TASK / 'LOG.md'
    expected_log = historical['external-documents']['tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md']
    old_prefix = log_path.read_bytes()[:expected_log['bytes']]
    assert sha_bytes(old_prefix) == expected_log, 'Historical LOG prefix changed'
    checkpoint = json.loads((OUT / 'checkpoint.json').read_text(encoding='utf-8'))
    checkpoint.update({'closed_at': now, 'remote_state': 'READ_ONLY_REFRESHED',
        'remote_status_file': 'remote-status.json', 'local_integrity': 'PASS_825_OF_825',
        'local_integrity_file': 'integrity-verification.json',
        'source_script_edits': False, 'next_session_required': True,
        'current_phase': 'PRE_RUN_SCRIPT_READING_INCOMPLETE',
        'pending': ['cumulative budget ledger and guard correction',
                    'authorized archive deletion after fresh integrity check',
                    'independent full script review and channel metadata fix',
                    'EC2 pilot fixtures/validation/time/RAM/storage',
                    'delay/channel rest and updated group/control lock',
                    'manual reading and synthesis in later session']})
    dump(OUT / 'checkpoint.json', checkpoint)
    (OUT / 'README.md').write_text(f'''# T-033 — Checkpoint phiên 4

Chốt {now}. Codex người làm, Claude phản biện. Phiên dừng do ngữ cảnh nén theo AGENTS §5a.2 và lời Minh. **Chưa khởi chặng tính mới, task chưa hoàn tất.**

## Bằng chứng và trạng thái mới

- `checkpoint.json`: hai lời duyệt nguyên văn, việc đã/chưa làm. Lời duyệt tổng 12 giờ xử lý và xóa đúng archive đã có hiệu lực; chưa sửa guard/ledger hoặc xóa archive. Chưa có quyền ghi hai dòng vào DECISIONS.
- `integrity-verification.json`: tự kiểm laptop PASS 825/825 file, byte và SHA khớp inventory; không thiếu/thừa. Metadata lịch sử bất biến trong handoff-manifest khớp. External-documents lịch sử không được coi là pin của docs hiện tại đang có sửa được duyệt của phiên khác.
- `remote-status.json`: SSH chỉ đọc lúc {remote['at']}; không worker/tmux T-033. EC2 T-033 du {remote['du'].strip()}; archive {remote['archive_bytes']} byte còn nguyên. Không EC2 writes, không khởi worker, không xóa. Dung lượng trước/sau xóa chưa có vì chưa xóa.
- `script-reading-evidence.json`: ba script parse AST đạt; dict status lặp trong channel_context.py được người làm kiểm. `script-reading-notes.md` phân biệt chứng cứ người làm với báo cáo trợ lý chưa kiểm EC2. Ba script không đổi trong phiên.
- `scope-verification.json`: kiểm LOG chỉ nối, SPEC giữ hash lịch sử, chỉ dòng T-033 STATE đổi, script nghiên cứu không đổi. `manifest.json` khóa file checkpoint.

## Mức đạt và phần thiếu

Checkpoint-handoff-001 giữ nguyên bộ lõi/bổ sung và toàn bộ lượt lỗi; locator có core/FF/factorial/fixed. Hash bản nhận đạt không thay kiểm số/intermediates mới, không xác nhận cơ chế. `output-presence.json` lịch sử vẫn mô tả đầu ra cấp gốc; phiên 4 không tạo đầu ra nghiên cứu mới.

Chưa: ledger tổng mọi lượt hỏng/kiểm; sửa guard; xóa archive; tự đọc đủ ba script và sửa lỗi metadata kênh; fixture/pilot/rest độ trễ/kênh; khóa nhóm/đối chứng sau phân rã; đọc tay; tổng hợp. RQ2/P4/P6/G2 vẫn OPEN. Không có bằng chứng mới phân xử cơ chế/tín hiệu/onset.

Trần 4 GiB hiện chỉ tính đầu ra EC2 theo lời Minh. Không dùng combined storage trong README cũ làm trần hiện tại. Không dùng subtotal wall có status trong snapshot để mặc nhiên cấp giờ còn lại; phải dựng ledger đủ trước run mới.

## Bước tiếp chính xác

Minh mở phiên Codex mới với `prompt-next-session.md`; đó là prompt nối việc, không phải phản biện Claude. Đọc bản gốc và các notes trước hành động. Việc tiếp ngay vẫn là chuẩn bị/kiểm script và chặng tính EC2; **chưa chuyển sang đọc tay + tổng hợp**. Khi chặng tính đạt mới soạn prompt đó. Prompt Claude chính thức chỉ khi task hoàn tất.

Lệnh đọc trước ở laptop:

```powershell
Get-Content -LiteralPath results/T-033/scripts/nsigma_delay.py -Encoding UTF8
Get-Content -LiteralPath results/T-033/scripts/bocpd_delay.py -Encoding UTF8
Get-Content -LiteralPath results/T-033/scripts/channel_context.py -Encoding UTF8
```

Lệnh EC2 chỉ đọc trước sửa/chạy, rồi kiểm hash theo inventory/source/manifest và môi trường pin:

```powershell
ssh -i D:/RCA-ext/keys/keys.pem -o UserKnownHostsFile=D:/RCA-flashticket/results/T-033/runs/prepare-001/known_hosts -o StrictHostKeyChecking=yes -o BatchMode=yes ubuntu@3.107.246.249 'tail -n 20 ~/rca/T-033/trang-thai.txt'
```

Không gọi CLI delay hiện tại để chạy toàn lô: cần tự xác nhận/hoàn thiện pilot/rest, provenance/lifecycle và guard trong phạm vi đã duyệt, giữ bản cũ và hash hai đầu. Lệnh tính pilot chính xác chỉ ghi sau sửa/kiểm script đạt, không đoán CLI chưa có. Python EC2 pin `/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8`; native `/home/ubuntu/rca/T-025/src/baro`; adapter `/home/ubuntu/rca/T-025/repo/src/p3/`. Dữ liệu chỉ allowlist trong inputs/source.json đã hash.

## EC2 và Minh cần làm

Không có lượt chạy nền hiện tại; Minh có thể tắt laptop sau chốt. EC2 vẫn cần cho phần tính còn lại; giữ bật để phiên mới tiếp, agent không bật/tắt EC2. Chưa thông báo worker “đã ổn định” vì chưa có pilot mới. Khi kiểm pilot phiên sau phải báo CẦN GIỮ LAPTOP MỞ theo yêu cầu Minh.

Hai lời duyệt đã ghi nguyên văn LOG. Đề xuất nối nguyên văn thành hai dòng mới trong docs/DECISIONS.md, ngày 10/10/2026, nguồn lời Minh trong phiên 4; mã lấy từ file sau khi đọc lại lúc có quyền ghi. Phạm vi chỉ lưu quyết định, không thêm quyền/SPEC. Chờ Minh duyệt ghi sổ theo Luật 0; không chờ duyệt lại các việc đã được phép.
''', encoding='utf-8')
    closing = f'''

### Kết thúc phiên 4 — checkpoint khi ngữ cảnh nén — {now}

1. Đã làm: đọc toàn SPEC/LOG phiên 3 và README gốc; ghi dòng mở phiên và nguyên hai lời duyệt ngày 10/10. Tự kiểm SHA/byte laptop 825/825 PASS; kiểm chỉ đọc EC2 không worker/tmux, archive còn nguyên. Lưu tự soát trợ lý và tự xác nhận lỗi dict status trùng trong script kênh. Không thực hiện chặng tính mới.
2. File thay đổi: thêm scripts/checkpoint_session4.py và finish_checkpoint_session4.py, checkpoint session4-checkpoint-001 trong results/T-033/; LOG chỉ nối; chỉ dòng T-033 STATE. Không sửa ba script nghiên cứu/guard, SPEC, WHY, DECISIONS, nguồn code/dữ liệu; không EC2 writes/xóa, không test/locked/heldout/vùng T-032, không commit/push/bật/tắt EC2.
3. Kiểm: integrity-verification.json PASS 825 file/{integrity['bytes']} byte, metadata bất biến trong handoff-manifest khớp; local SHA mất {integrity['wall_s']:.3f} giây, chỉ kiểm điều khiển. AST ba script PASS; duplicate status tại 229/246 xác nhận. SSH metadata hoàn thành trong 4.182 giây đo từ client, gồm kết nối; không dùng số này làm thời gian tính nghiên cứu EC2. remote-status.json ghi du/archive/disk. LOG lịch sử khớp hash prefix, SPEC khớp pin, script giữ hash, STATE chỉ dòng T-033. Không recompute số/intermediates nghiên cứu trong phiên này.
4. OPEN: task chưa xong; chưa có kết luận cơ chế/RQ2/P4/P6/G2. Còn thiếu ledger đủ giờ xử lý, sửa guard, xóa archive đúng quyền, người làm tự đọc đủ ba script, fixture/pilot kiểm schema/time/CP/flags/intermediates/RAM/bytes, rest độ trễ/kênh, khóa nhóm/đối chứng, đọc tay/tổng hợp. Lỗi metadata kênh phải sửa trước pilot; báo cáo trợ lý chưa thay kiểm EC2. Đọc trực tiếp MRP/DT18/advisor/LESSONS/WHY-41 trước diễn giải. Không bỏ câu hỏi cơ chế vì mới khớp hash.

EC2: vừa kiểm chỉ đọc {remote['at']}, không worker/tmux T-033; archive còn nguyên. Minh có thể tắt laptop sau checkpoint. EC2 còn cần cho chặng tính đã duyệt, giữ bật để nối phiên; agent không bật/tắt máy. Không báo lượt mới ổn định vì chưa có pilot. Phiên sau khi kiểm pilot phải giữ laptop theo yêu cầu Minh.

Bước tiếp chính xác: mở phiên Codex mới và copy results/T-033/runs/session4-checkpoint-001/prompt-next-session.md. Đọc README/checkpoint/integrity/remote-status/evidence/notes và ba script; SSH chỉ đọc `tail -n 20 ~/rca/T-033/trang-thai.txt` bằng key/known_hosts và pin trong README; dựng ledger đủ trước sửa guard/khởi run. Tự kiểm lại inventory rồi chỉ xóa archive được duyệt, ghi byte trước/sau. Đừng chạy CLI delay toàn lô hiện có trước hoàn thiện pilot/rest và fixture. Chặng tính chưa đạt nên chưa chuyển đọc tay+tổng hợp hay soạn phản biện chính thức.

Lệnh cuối phiên: `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -X utf8 results/T-033/scripts/finish_checkpoint_session4.py` trên laptop — chốt tài liệu và tự kiểm phạm vi/hash; không tính nghiên cứu. Lệnh EC2 cuối: Python pin nhận script metadata qua SSH stdin, chỉ đọc ps/tmux/du/stat/df; nguyên kết quả ở remote-status.json. Lượt SSH trước đó lỗi cú pháp PowerShell trước kết nối, không chạy EC2, đã sửa cách truyền stdin cho lượt chỉ đọc; không có lượt detector lỗi mới.

Đề xuất ghi DECISIONS, chờ Minh duyệt riêng việc lưu sổ theo Luật 0: nối hai dòng mới ngày 10/10/2026, giữ nguyên nội dung hai mục DUYỆT trong “Quyết định của Minh trong phiên”, nguồn Minh cung cấp trong phiên 4. Không tự gán mã đang được phiên T-032 dùng; đọc lại file lấy mã khi có quyền nối. Lời duyệt thực hiện đã có, việc lưu DECISIONS chưa được duyệt.

Prompt phiên kế tiếp nằm ở results/T-033/runs/session4-checkpoint-001/prompt-next-session.md, Minh chuyển thủ công. Không phải prompt phản biện Claude; không tự mở hay gửi vòng review.
'''
    with log_path.open('a', encoding='utf-8', newline='') as f:
        f.write(closing)
    state_path = ROOT / 'docs/STATE.md'
    # Read the shared live file immediately before the narrowly authorized edit.
    state_before = state_path.read_bytes()
    text = state_before.decode('utf-8')
    rows = [line for line in text.splitlines(keepends=True) if line.startswith('| T-033 |')]
    assert len(rows) == 1
    old_row = rows[0]
    cells = old_row.rstrip('\r\n').split('|')
    assert len(cells) == 9
    cells[6] = ' Đang thực hiện (phiên 4, 11/10): tự kiểm bản nhận 825/825 file đạt; EC2 không worker. Minh đã duyệt guard tổng 12 giờ xử lý và xóa đúng archive; chưa thực hiện. Chốt session4-checkpoint-001 do ngữ cảnh nén; chưa chạy độ trễ/kênh, chưa khóa nhóm mới/đọc tay/tổng hợp. Mở phiên Codex mới theo prompt checkpoint '
    newline = '\r\n' if old_row.endswith('\r\n') else '\n'
    new_row = '|'.join(cells) + newline
    state_after = text.replace(old_row, new_row, 1).encode('utf-8')
    assert state_after.replace(new_row.encode('utf-8'), b'', 1) == state_before.replace(old_row.encode('utf-8'), b'', 1)
    assert state_path.read_bytes() == state_before, 'STATE changed concurrently; retry narrow edit from a fresh read'
    (OUT / 'STATE.md.before-session4-close').write_bytes(state_before)
    state_path.write_bytes(state_after)
    spec_expected = historical['external-documents']['tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md']
    assert sha_bytes((TASK / 'SPEC.md').read_bytes()) == spec_expected
    assert sha_bytes(log_path.read_bytes()[:expected_log['bytes']]) == expected_log
    scope = {'status': 'PASS', 'log_historical_prefix_unchanged': True,
             'state_only_T033_row_changed': True, 'state_before': sha_bytes(state_before),
             'state_after': sha_bytes(state_after), 'spec_unchanged': True,
             'research_scripts_unchanged': unchanged_scripts, 'ec2_writes': False,
             'source_of_truth_new_decisions': 'USER_CONFIRMED; verbatim LOG, DECISIONS write awaits approval'}
    dump(OUT / 'scope-verification.json', scope)
    diff = subprocess.run(['git', 'diff', '--', 'results/T-033/',
        'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md', 'docs/STATE.md'], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
    (OUT / 'scoped-worktree-diff.txt').write_bytes(diff)
    manifest = {p.relative_to(OUT).as_posix(): sha_bytes(p.read_bytes())
                for p in OUT.rglob('*') if p.is_file() and p.name != 'manifest.json'}
    manifest['session_scripts'] = {name: sha_bytes((ROOT / 'results/T-033/scripts' / name).read_bytes())
         for name in ('checkpoint_session4.py', 'finish_checkpoint_session4.py')}
    dump(OUT / 'manifest.json', manifest)
    # Read back all written metadata and complete scope diff; no data calculations.
    for p in OUT.glob('*.json'):
        json.loads(p.read_text(encoding='utf-8'))
    assert b'| T-033 |' in diff
    print(json.dumps({'checkpoint': str(OUT), 'status': 'PASS',
       'artifact_files_verified': integrity['checked_files'], 'no_new_research_run': True,
       'guard_unchanged': True, 'archive_not_deleted': True,
       'session_changed_files': ['results/T-033/scripts/checkpoint_session4.py',
          'results/T-033/scripts/finish_checkpoint_session4.py',
          'results/T-033/runs/session4-checkpoint-001/*',
          'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md (append)',
          'docs/STATE.md (T-033 row only)']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
