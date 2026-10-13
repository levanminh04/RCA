"""Mở phiên tiếp đã duyệt; chỉ cập nhật nhật ký và snapshot phạm vi."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json
import hashlib

root=Path(__file__).resolve().parents[3]
run=root/'results/T-033/runs/session2-open-001'
run.mkdir(exist_ok=False)
names=['docs/STATE.md','docs/WHY.md','tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md','tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md']
before={}
for name in names:
    data=(root/name).read_bytes()
    (run/(Path(name).name+'.before')).write_bytes(data)
    before[name]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
(run/'before.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
now=datetime.now(timezone(timedelta(hours=7))).isoformat()
entry=f'''

## Phiên 2 — {now} — Codex — laptop Windows 11 và EC2 T-033 — Người làm

- Minh duyệt SPEC ngày 09/10/2026. Minh yêu cầu kiểm tiến độ và tiếp thực hiện theo cùng phạm vi/ngân sách; intent EXECUTE. Claude vẫn là người phản biện chính thức. Hai trợ lý nội bộ hỗ trợ cài đúng script frozen và factorial, không tự mở vòng phản biện.
- Đã đọc lại AGENTS, STATE, toàn SPEC và checkpoint LOG phiên 1. Lời duyệt trong yêu cầu hiện hành và dòng T-033 là nguồn quyền thực hiện; các câu chờ duyệt cũ ngoài dòng trạng thái được giữ nguyên theo phạm vi Minh cho phép.
- EC2 live check 09:05 ngày 10/10 +07: `bocpd-rest-001/status.json` PASS, 29 ca đủ full và PP; exit0, không còn PID28484; kết thúc 03:35:37 +07, thời gian lô 11.209,136 giây. Progress ở ~/rca/T-033/trang-thai.txt. Kết quả này là trạng thái driver, đang kiểm hash/manifest/intermediate trước dùng và trước nhánh mới. Chưa khởi trùng, chưa đọc locked/test/heldout hoặc T-032.
- Unified exec mặc định lỗi setup refresh ngay lúc khởi process; exec ngoài sandbox được duyệt tự động và chạy được. Không cài môi trường mới, không đổi package. Source code/data cũ EC2 tiếp tục chỉ đọc.
- CẦN GIỮ LAPTOP MỞ: đang kiểm lõi và chuẩn bị ca đầu FP/PF/nền cố định; dự kiến cần khoảng 20–40 phút để chuẩn bị và kiểm ca đầu, ước lượng có thể đổi theo lỗi/chiều. Mốc báo lại khi ca đầu các nhánh đạt và đo đủ runtime/RAM/disk.
'''
log=root/names[-1]
old=log.read_bytes()
with log.open('ab') as f: f.write(entry.encode('utf-8'))
assert log.read_bytes().startswith(old)
print('PASS session 2 opening; LOG append only')
