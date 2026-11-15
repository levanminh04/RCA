"""Copy the governing review prompt literally; fill only neutral run metadata."""
from pathlib import Path
import re

root=Path(__file__).resolve().parent
source=Path('D:/RCA-flashticket/docs/review-prompt.md').read_text(encoding='utf8')
common=re.search(r'## Prompt chung\s+```text\n(.*?)\n```',source,re.S)[1]
stage=re.search(r'### Soát kết quả\s+```text\n(.*?)\n```',source,re.S)[1]
fill={
'<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>':'T-058; D:/RCA-ext/overnight-T058/inputs/SPEC.md; phạm vi lượt đêm ở AGENTS.md, PROMPT.md, out/STEER.md.',
'<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>':'soát kết quả.',
'<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>':'P9b và chuẩn bị P10; không có cổng riêng, đầu ra phục vụ G6 theo SPEC T-058.',
'<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>':'Lượt đêm: Codex là người làm, Claude điều phối/giám sát theo AGENTS.md và PROMPT.md. Người phản biện chính thức cho kết quả lượt này chờ Minh chỉ định; không tự đổi vai trò.',
'<danh sách đường dẫn và git diff từ commit gốc nếu có>':'D:/RCA-ext/overnight-T058/AGENTS.md, PROMPT.md, inputs/AGENTS-repo-RCA.md, inputs/ban-giao-chay-dem.md, inputs/thay-doi-ha-tang-2026-11-11.md, inputs/SPEC.md, inputs/revisions.json, inputs/TECHSTACK-NGHIEN-CUU.md, inputs/PLAN-TRIEN-KHAI.md, inputs/LESSONS.md, inputs/yeu-cau-quan-sat-p9.md; chỉ đạo out/STEER.md. Hai repo nguồn laptop chỉ đọc; không có commit hoặc diff triển khai trong repo.',
'<đường dẫn theo thứ tự thời gian; không có thì ghi không có>':'Chỉ đạo điều phối trong out/STEER.md; chưa có bản phản biện chính thức của kết quả lượt đêm trong out/.',
'<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>':'D:/RCA-ext/overnight-T058/out/: bao-cao-sang.md, moi-truong.md, manifest-digest.json, huong-dan-trien-khai.md, kiem-agent.md, kiem-telemetry.md, kiem-bo-nho.md, so-do-tai-nguyen.json, rca-ban-dau.md, rca-ban-dau/, m1-execution-plan.json, m1-execution-plan-v2.json, m1-source-pins.json, src/m1/adapter_flashticket.py, stage-m1.py, run-m1.py, LOG-dem.md, CHECKPOINT.md, CAN-MINH-QUYET.md. Quyền máy và khóa nêu trong AGENTS.md của thư mục lượt đêm.',
'<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>':'Prompt này chỉ đề nghị đọc và trả lời trong chat; không cấp quyền ghi mới, không chạy thực nghiệm mới. Claude vẫn có kênh điều phối out/STEER.md theo quyền lượt đêm đã có.'}
for old,new in fill.items():
    if old not in common: raise SystemExit('Template placeholder changed')
    common=common.replace(old,new)
intro=('# Prompt bàn giao kết quả lượt đêm\n\n'
       'Nguồn mẫu: `D:/RCA-flashticket/docs/review-prompt.md`. Chép nguyên Prompt chung và khối Soát kết quả, chỉ điền metadata trung tính. '
       'T-058 không có cổng riêng; mẫu hiện tại chưa có khối G6, nên không tự đặt thêm khối cổng hoặc dùng cổng khác.\n\n')
(root/'prompt-ban-giao-Claude.md').write_text(intro+'```text\n'+common+'\n\n'+stage+'\n```\n',encoding='utf8')
print('Created literal handoff prompt; no message sent to another agent')
