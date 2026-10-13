"""Mở checkpoint bàn giao đã được Minh yêu cầu; không đổi phương pháp."""
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[3]
home = root / 'results/T-033'
run = home / 'runs/handoff-open-001'
run.mkdir(exist_ok=False)
files = ['AGENTS.md', 'docs/STATE.md', 'docs/WHY.md', 'docs/DECISIONS.md',
         'docs/review-prompt.md', 'tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md',
         'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md']
baseline = {}
for name in files:
    content = (root / name).read_bytes()
    destination = run / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    baseline[name] = {'sha256': hashlib.sha256(content).hexdigest(), 'bytes': len(content)}
(run / 'baseline.json').write_text(json.dumps(baseline, indent=2), encoding='utf-8')
now = datetime.now(timezone(timedelta(hours=7))).isoformat()
entry = f'''

## Phiên 3 — {now} — Codex — laptop Windows 11 và EC2 T-033 — chốt bàn giao

- Minh duyệt SPEC ngày 09/10/2026. Minh yêu cầu: "hãy chốt mới nhất cho tôi để claude có thể kiểm tra toàn vẹn". Intent EXECUTE: chốt checkpoint, nhận đầu ra hiện có, kiểm tính toàn vẹn, cập nhật LOG/dòng T-033 STATE và soạn prompt. Đây không phải lời duyệt sửa guard hoặc chạy chặng nghiên cứu tiếp theo.
- Codex vẫn là người làm, Claude vẫn là người phản biện. Không tự mở phiên Claude hoặc gửi prompt; Minh chuyển thủ công. Prompt sẽ cho quyền chỉ đọc/trả lời trong chat khi chưa có quyền ghi bản REVIEW cụ thể.
- Đã đối chiếu checkpoint cũ: snapshot phiên 2 chỉ tới 09:35 ngày 10/10 +07, LOG đóng lúc 09:41 còn ghi FP/PF đang chạy. EC2 `bocpd-factorial-rest-001/status.json` hiện PASS, đủ 30 ca gồm ca pilot tái dùng; kết thúc 10:27:24 ngày 10/10 +07, exit 0, không còn worker. Cần nhận snapshot/manifest cuối và ghi trạng thái mới để không phụ thuộc chat.
- Vấn đề guard còn OPEN: SPEC mục Chi phí dự trù 4–12 giờ máy và nói "Đây không là timeout". Code guard dùng thời gian lịch liên tục từ lần tính đầu, bao gồm khoảng nghỉ. Mốc 11:46 ngày 10/10 do Codex cài; không được trình bày như thời hạn Minh đã chốt hoặc bằng chứng dùng hết giờ xử lý. Đề xuất chuyển sang tổng thời gian các lượt xử lý, giữ trần 12 giờ/4 GiB, chưa được Minh duyệt; chưa sửa code/nguồn/SPEC. Chi phí EC2 bật kể cả lúc nghỉ cũng chưa có đo đạc AWS độc lập. Chặng nghiên cứu mới phụ thuộc việc giải quyết cách tính ngân sách này.
- Phạm vi phiên: `results/T-033/`, LOG chỉ nối, duy nhất dòng T-033 STATE; EC2 chỉ `~/rca/T-033/`. SPEC/WHY/DECISIONS/code dữ liệu nguồn giữ nguyên. Không test/locked/heldout, không vùng kết quả T-032, không commit/push, không bật/tắt EC2.
'''
with (root / files[-1]).open('ab') as handle:
    handle.write(entry.encode('utf-8'))
print('PASS handoff opening; baseline saved; LOG append only')
