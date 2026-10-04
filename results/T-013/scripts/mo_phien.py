from pathlib import Path
import datetime, json, subprocess, hashlib

ROOT = Path('D:/RCA-flashticket')
OUT = ROOT / 'results/T-013'
TASK = ROOT / 'tasks/T-013-ho-so-baro'
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
prompt = Path('C:/Users/84583/.codex/attachments/2f6c5735-a241-4299-bd8c-25d4034a97de/Pasted text.txt').read_text(encoding='utf-8-sig')
task = '<task>' + prompt.split('<task>', 1)[1].split('</task>', 1)[0] + '</task>'
head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
log = TASK/'LOG.md'
assert not log.exists(), 'LOG đã có; không ghi đè'
log.write_text(f'# Nhật ký T-013\n\n## Phiên 1 — 04/10/2026 — Codex — Windows 11, laptop Minh — vai trò: người làm\n\n**Mở phiên ({now}):** đã đọc các nguồn bắt buộc và tự duyệt SPEC theo ủy quyền. Không có SPEC/LOG/đầu ra T-013 trước phiên. HEAD git: `{head}`. Hai source HEAD đúng yêu cầu; git status repo ban đầu sạch. STATE chưa có T-013; prompt hiện hành giao T-013 rõ, chỉ thêm dòng T-013.\n\n**Quyết định của Minh trong phiên:**\n- Minh ủy quyền tự duyệt SPEC theo prompt Đợt 1 ngày 04/10/2026\n- Chưa ghi vào DECISIONS vì ngoài phạm vi; sẽ có nháp trong de-xuat-tai-lieu-chung.md.\n\n**Khối task nguyên văn:**\n\n```text\n{task}\n```\n\n**Tự phản biện SPEC trước chạy:** bổ sung dict/DataFrame, timestamp-vs-index của anomalies, std ddof, service max và hòa điểm; không biến phép thử normal-normal thành yêu cầu code phải biết từ chối RCA. Quy tắc ca được khóa trước kết quả. Mốc A tập chỉ tái dùng, không gọi ví dụ một ca là tái lập số toàn bài. Hai subagent chỉ đọc độc lập, root giữ LOG/STATE.\n\n**Diễn biến:**\n- {now} — bước 0/1: đọc luật, mốc công bố trước chạy, xác minh hai HEAD; SPEC đã ghi trong phạm vi tự duyệt.\n',encoding='utf-8')
manifest={'started':now,'head':head,'code':{},'authorization':'prompt Đợt 1 04/10/2026','status_initial':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True)}
for name in ['baro','RCAEval']:
    p=Path('D:/RCA-ext/src')/name
    manifest['code'][name]={'path':str(p),'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=p,text=True).strip(),'status':subprocess.check_output(['git','status','--short'],cwd=p,text=True)}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
state=ROOT/'docs/STATE.md'
with state.open('r+b') as f:
    old=f.read()
    assert b'| T-013 |' not in old
    lines=old.splitlines(keepends=True)
    last=max(i for i,line in enumerate(lines) if line.startswith(b'| T-'))
    offset=sum(map(len,lines[:last+1]))
    nl=b'\r\n' if lines[last].endswith(b'\r\n') else b'\n'
    row='| T-013 | Hồ sơ BARO và bộ phát hiện | P1 | Codex | Claude | đang làm (04/10/2026) | `tasks/T-013-ho-so-baro/` |'.encode()+nl
    f.seek(0); assert f.read()==old
    f.seek(offset); f.write(row+old[offset:]); f.truncate()
assert state.read_bytes()==old[:offset]+row+old[offset:]
print('Session opened; exactly one STATE row inserted.')
