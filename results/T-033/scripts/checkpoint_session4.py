"""Documentation/integrity checkpoint only; no research calculations or EC2 writes."""
from __future__ import annotations

import ast
import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TASK = ROOT / 'tasks/T-033-g2-nguyen-nhan-phat-hien'
OUT = ROOT / 'results/T-033/runs/session4-checkpoint-001'
OLD = ROOT / 'results/T-033/runs/checkpoint-handoff-001'

DECISIONS = '''1. DUYỆT: ngân sách thời gian tính bằng tổng giờ xử lý cộng dồn của các lượt, gồm lượt hỏng và lượt kiểm, trần 12 giờ; bỏ mốc lịch 11:46 ngày 10/10. Chỉ sửa đúng phần guard trong script; giữ bản cũ; kiểm hash hai đầu; ghi cách tính và số giờ đã dùng vào LOG trước khi khởi lượt mới.
2. DUYỆT: xóa đúng một file ~/rca/T-033/runs/checkpoint-handoff-001/artifacts.tar trên EC2, sau khi tự kiểm lại bản laptop khớp artifact-inventory.json. Trần 4 GiB tính trên đầu ra tại EC2. Không xóa gì khác. Ghi dung lượng trước và sau vào LOG.
Hai lời duyệt này không mở rộng sang việc khác.'''


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return {'sha256': h.hexdigest(), 'bytes': path.stat().st_size}


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def append_log(text):
    with (TASK / 'LOG.md').open('a', encoding='utf-8', newline='') as f:
        f.write(text)


def main():
    OUT.mkdir(exist_ok=False)
    now = datetime.now().astimezone().isoformat()
    append_log(f'''\n\n## Phiên 4 — {now} — Codex — laptop Windows 11 — Người làm T-033

- Minh duyệt SPEC ngày 09/10/2026. Intent EXECUTE: tiếp chặng tính EC2 độ trễ/kênh và khóa nhóm theo SPEC; chưa viết kết luận cơ chế/tổng hợp. Codex là người làm, Claude là người phản biện.
- Đã đọc AGENTS, STATE, toàn bộ SPEC, LOG phiên 3 và README checkpoint từ repo. Phiên mới không dùng lịch sử chat làm bằng chứng. Các phần MRP RQ2/P4, DT18-NV2/NV3, hướng dẫn cô §1, LESSONS và WHY-41 còn phải đọc trực tiếp trước diễn giải.

### Quyết định của Minh trong phiên — lời duyệt ngày 10/10/2026, Minh cung cấp lại trong phiên mới

{DECISIONS}

- Hai lời duyệt trên đã có hiệu lực trong phạm vi đã nêu. Chưa ghi docs/DECISIONS.md; trình dòng lưu chính thức trong chat và chờ Minh duyệt. Không sửa SPEC/WHY hoặc quy tắc khoa học.

### Checkpoint ngay khi ngữ cảnh bị nén — {now}

- Theo AGENTS §5a.2 và yêu cầu Minh: chốt trạng thái ở results/T-033/runs/session4-checkpoint-001/, đề nghị mở phiên mới; chưa khởi lượt nghiên cứu mới.
- Chưa sửa guard, chưa tính đủ ledger giờ xử lý, chưa xóa archive EC2, chưa SSH trong phiên này. Snapshot EC2 checkpoint-handoff-001 là lịch sử ngày 10/10, không được gọi là trạng thái EC2 vừa kiểm.
- Hai trợ lý hỗ trợ tự soát chỉ đọc script, không phải phản biện Claude chính thức. Báo cáo trợ lý là đầu vào kiểm của người làm; fixture và mọi tính nghiên cứu vẫn phải chạy EC2.
''')
    dump(OUT / 'checkpoint.json', {
        'at': now, 'reason': 'CONTEXT_COMPACTED', 'task_complete': False,
        'intent': 'EXECUTE', 'worker_started_this_session': False,
        'guard_edited': False, 'archive_deleted': False,
        'cumulative_budget_accounting': 'NOT_DONE',
        'remote_state': 'NOT_REFRESHED_THIS_SESSION',
        'research_questions': 'OPEN; no mechanism conclusions',
        'decisions': DECISIONS,
        'decision_register_write': 'AWAITING_MINH_APPROVAL',
        'source_checkpoint': 'results/T-033/runs/checkpoint-handoff-001',
    })
    source_manifest = {}
    duplicate_keys = {}
    for name in ('nsigma_delay.py', 'bocpd_delay.py', 'channel_context.py'):
        p = ROOT / 'results/T-033/scripts' / name
        source_manifest[name] = digest(p)
        tree = ast.parse(p.read_text(encoding='utf-8'), filename=name)
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                seen = {}
                for key in node.keys:
                    if isinstance(key, ast.Constant) and isinstance(key.value, str):
                        if key.value in seen:
                            found.append({'key': key.value, 'first_line': seen[key.value],
                                          'duplicate_line': key.lineno})
                        seen[key.value] = key.lineno
        duplicate_keys[name] = found
    dump(OUT / 'script-reading-evidence.json', {
        'scripts': source_manifest, 'ast_parse': 'PASS',
        'duplicate_literal_dictionary_keys': duplicate_keys,
        'ec2_fixture_run': False, 'script_edits': False,
    })
    print(json.dumps({'checkpoint_opened': str(OUT), 'duplicate_keys': duplicate_keys}, ensure_ascii=False))


if __name__ == '__main__':
    main()
