"""Final handoff, append-only LOG, one STATE row, bounded owned diff and manifest."""
from datetime import datetime,timezone
import difflib
import hashlib
import json
import msvcrt
from pathlib import Path
import re
import subprocess

ROOT=Path('D:/RCA-flashticket');BASE=ROOT/'results/T-037';RUN=BASE/'runs/ket-phien-002'
LOG=ROOT/'tasks/T-037-p5b-flashticket/LOG.md';STATE=ROOT/'docs/STATE.md'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write(p,v):p.write_text(v,encoding='utf-8')
RUN.mkdir(parents=True,exist_ok=False)
run=load(BASE/'runs/graph-003/result.json');smtp=load(BASE/'runs/smtp-regression-001/result.json');assert run['all_pass'] and smtp['all_pass']
template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
def block(a,b):return template.split(a,1)[1].split(b,1)[0].split('```text\n',1)[1].split('\n```',1)[0]
common=block('## Prompt chung','## Khối công đoạn');stage=block('### Soát kết quả','### Người làm đáp phản biện');gate=block('### G3 — Khóa thiết kế trước khi mở test','### G4 — Kết quả')
values=[
 'T-037; D:/RCA-flashticket/tasks/T-037-p5b-flashticket/SPEC.md và LOG.md',
 'soát kết quả', 'P5; chuẩn bị G3', 'Codex người làm, Claude người phản biện chính thức kết quả',
 'AGENTS.md; docs/STATE.md; SPEC/LOG T-037; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; results/T-037/nguon.json cùng các nguồn và snapshot được liệt kê; nguồn platform theo luật và skill govern-capstone-work',
 'Chưa có bản phản biện kết quả T-037. Lịch sử chuẩn bị/triển khai và quyền sửa tại tasks/T-037-p5b-flashticket/LOG.md. T-036 có REVIEW.md và LOG.md trong tasks/T-036-p5b-hop-dong-chung/',
 'results/T-037/manifest.json, ban-ghi.json, bao-phu-nguon.md/json, do-thi/, dia-chi-tin-hieu.json, hop-dong-runtime.md, hop-dong-smtp.md, kiem-dung-dan.md, ban-giao.md và runs/; oracle/fixtures tại các file manifest liệt kê. Pin nền T-036 runs/kiem-r1-after-002/code và code-hashes.json; mã T-037 thực dùng tại runs/graph-003/code. Diff tại runs/ket-phien-002/changes.diff. Windows11, Python3.12 môi trường D:/RCA-ext/envs/py312-pin; lệnh build-check.py hoặc smtp-check.py chỉ khi Minh giao chạy trong phạm vi kết quả T-037; không chạy checker T036 ghi vào T036',
 'Chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC, code, kết quả hoặc nguồn chung. Minh chuyển prompt thủ công'
]
assert len(re.findall(r'<[^>]+>',common))==len(values)
filled=common
for token,value in zip(re.findall(r'<[^>]+>',common),values):filled=filled.replace(token,value,1)
prompt=filled+'\n\n'+stage+'\n\n'+gate+'\n';write(BASE/'prompt-claude.txt',prompt)

# Take a fresh locked read; no stale STATE version is written.
with STATE.open('r+b') as f:
 msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
 try:
  f.seek(0);old=f.read();lines=old.decode('utf-8-sig').splitlines(keepends=True);indices=[i for i,l in enumerate(lines) if l.startswith('| T-037 |')];assert len(indices)==1;i=indices[0]
  nl='\r\n' if lines[i].endswith('\r\n') else '\n';prior=lines[i]
  lines[i]='| T-037 | P5b: FlashTicket đầy đủ theo thiết kế | P5 (G3) | Codex | Claude (kết quả) | Chờ Claude phản biện kết quả (16/10/2026). Đã sửa/kiểm SMTP và dựng mô hình thiết kế có điều kiện; nguồn/coverage/graph/fixture/bàn giao ở results/T-037/, current_run graph-003. T038/T039 giữ pin gốc; T037 ghi pin nền + delta SMTP theo Minh giao. Runtime/queue/scope và RQ3/RQ5/G3 còn OPEN; chưa nghiệm thu. Prompt ở results/T-037/prompt-claude.txt và LOG Phiên3. | `tasks/T-037-p5b-flashticket/` |'+nl
  final=''.join(lines).encode('utf-8');final=(b'\xef\xbb\xbf'+final) if old.startswith(b'\xef\xbb\xbf') else final
  (RUN/'state-immediately-before.md').write_bytes(old);f.seek(0);f.write(final);f.truncate();f.flush()
  dump(RUN/'state-update.json',dict(old_line=prior.strip(),new_line=lines[i].strip(),only_T037_row_changed=[x for x in old.decode('utf-8-sig').splitlines() if not x.startswith('| T-037 |')]==[x for x in final.decode('utf-8-sig').splitlines() if not x.startswith('| T-037 |')]))
 finally:f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)

with LOG.open('a',encoding='utf-8') as f:
 f.write(f'''\n\n### Kết thúc Phiên 3 — 16/10/2026 — Codex người làm — LeVanMinh

1. Đã sửa hỗ trợ SMTP theo Minh giao, kiểm đạt100/100 và regression221/221,312graph/156projection; giữ nguyên nội dung221check records và10artifact cũ. Tiếp tục T037: đọc/ghim34nguồn (5tài liệu chính,10diagram,4README,10baseline definitions,5nguồn quản trị),652đơnvị nguồn; lưu32thực thể/65tên thao tác/115quan hệ nguồn thành72cạnh thực thể/55cạnh thao tác/17cạnh chiếu,14binding/153địa chỉ tín hiệu. Full graph/fixture kiểm đạt{run['passed']}/{run['passed']} ở runs/graph-003/result.json. Số kiểm nhiều gồm references; không coi nó là bằng chứng mọi lập luận khoa học hoặc runtime đã đúng. Source quote/schema đã kiểm riêng, raw arrow OPEN được giữ.
2. File thay đổi đúng phần đã giao: src/do_thi_tinh/build.py chỉ2guardthêmsmtp; results/T037/ (graph, nguồn/coverage/bản ghi/địa chỉ/hợp đồng bổ sung/runtime/kiểm/bàn giao/manifest và mọi run); LOG chỉ nối thêm và đúng dòngT037 trong STATE. Không sửa T036snapshot/manifest, T038/T039SPEC/pin/code/kết quả; không sửa SPEC T037/REVIEW/WHY/DECISIONS hoặc platform. Mã actual không giả khớp pin cũ: T037 ghi rõ nền + deltaSMTP đã duyệt, snapshot ở graph-003/code. Bản trước và runlỗi giữ nguyên.
3. Tất cả phép kiểm hiện hành đạt. Máy: SMTP+regression {smtp['seconds']:.3f}s, peakchild {smtp['original_regression']['peak_working_set_bytes']}byte; graphhiệnhành {run['seconds']:.3f}s, peak {run['peak_working_set_bytes']}byte. Tổngđĩa/cácfilehash tại manifest, gồm lượt lỗi/lặp/bản trước. Giờcông là dự toán, không lấy walltime qua ngắt usage làm thời gian làm liên tục. Kiểmcuối bằng verify-complete.py đối chiếu toànowned diff/phạmvi/hash/pin/LOGprefix/STATErow/prompt; kết quảởruns/ket-phien-002/final-verification.json. Không tải/giải nén/EC2/commit/push/mởtest/heldout/telemetry thô hoặc tự gửichat.
4. Đạt phần mô hình nguồnthiếtkế và bàn giao cóđiềukiện để chờClaude phảnbiện; không tự nghiệmthu. Câu nguồn được trả lời: giữowner/DBlogic-instance/quan hệ có type/address/operationname thiết kế vàSMTP; mọi khoảngtrốngquantrọng có nguồnowner/input. Chưa xácnhậnruntime, nhánh đãchạy, tínhiệuđủ hoặc lợiíchRCA. OPEN7nhóm tại bao-phu-nguon.json#/open_items; P9cần config/build/export/names/queue/scope/clock/permissions, P6cần thiết kế/phép dùngcạnh/binding trên dev, T040cần tổnghợp khácpin theo quyềnriêng; RQ3/RQ5/G3 giữmở. Không có quyếtđịnhnghiêncứumới hoặc giảmtiêuchí. QuyếtđịnhSMTP/giữnguyên2nhánh cần ghi sổchínhthức được trìnhnộidung/phạmvi ởban-giao.md, chưa ghi ngoài quyền.

**Bước tiếp chính xác:** Minh chuyển promptClaude dưới đây (hoặc results/T037/prompt-claude.txt) để soát kết quả trên nguồn/đầu ra thật. Chưa có quyền ghi REVIEW; reviewer mặc định chỉđọc/trảlờichat, Minh quyết phạmvi lượtghi. Không chạy lại graph hoặc đổi pin hai nhánh khi chưa có lý do/quyền. Đọc results/T037/manifest.json và kiểm hash trước dùng; xem bao-phu-nguon.json, do-thi/, hop-dong-runtime.md và ban-giao.md. Finding là đầu vào, Minh quyết sửa.

**Lệnh cuối của lượt:** & 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B results/T-037/verify-complete.py. Lệnh chỉ kiểm toàn artifact/phạmvi và ghi báo cáo cuối trong T037, không thựcnghiệmmới. **Đềxuất nội dungcommit, chưa thực hiện:** `feat: support SMTP in sourced graphs and model FlashTicket design`. Chỉ commit/push khi Minhduyệt riêng.

**Prompt Claude — Soát kết quả + G3, Minh chuyển thủ công:**\n\n```text\n{prompt}```\n''')

# Full owned text diff, with unchanged prior runs represented by the prior manifest.
before=BASE/'runs/tiep-smtp-001/before'
changed=[];parts=[]
for p in sorted(BASE.rglob('*')):
 if not p.is_file() or p.name in ['manifest.json','changes.diff','final-verification.json']:continue
 rel=p.relative_to(ROOT).as_posix();oldfile=before/rel
 if oldfile.is_file():
  original=oldfile.read_bytes()
  if original==p.read_bytes():continue
 elif p.is_relative_to(BASE/'runs') and not any(x in p.parts for x in ['tiep-smtp-001','smtp-regression-001','assemble-001','assemble-002','graph-001','graph-002','graph-003','ket-phien-002']):continue
 else:original=b''
 if p==RUN/'changes.diff':continue
 # Prior giant status/diff snapshots are integrity entries, not recursively inserted diffs.
 if p.name.endswith('.diff') or p.name in ['status-before.txt','status-final.json','preflight.json']:
  changed.append(dict(path=rel,kind='retained_metadata',sha256=sha(p),bytes=p.stat().st_size));continue
 try:
  lines=p.read_text(encoding='utf-8-sig').splitlines(keepends=True);oldlines=original.decode('utf-8-sig').splitlines(keepends=True)
 except UnicodeError:
  changed.append(dict(path=rel,kind='binary',sha256=sha(p),bytes=p.stat().st_size));continue
 parts+=list(difflib.unified_diff(oldlines,lines,fromfile='before/'+rel if original else '/dev/null',tofile=rel))
 changed.append(dict(path=rel,kind='text_diff',sha256=sha(p),bytes=p.stat().st_size))
for rel in ['src/do_thi_tinh/build.py','tasks/T-037-p5b-flashticket/LOG.md','docs/STATE.md']:
 p=ROOT/rel;q=before/rel
 oldlines=(RUN/'state-immediately-before.md').read_text(encoding='utf-8-sig').splitlines(keepends=True) if rel=='docs/STATE.md' else q.read_text(encoding='utf-8-sig').splitlines(keepends=True)
 parts+=list(difflib.unified_diff(oldlines,p.read_text(encoding='utf-8-sig').splitlines(keepends=True),fromfile='before/'+rel,tofile=rel))
 changed.append(dict(path=rel,kind='text_diff',sha256=sha(p),bytes=p.stat().st_size))
write(RUN/'changes.diff',''.join(parts));dump(RUN/'owned-file-set.json',changed)
dump(RUN/'prompt-check.json',dict(stage_exact=stage in prompt,gate_exact=gate in prompt,common_placeholder_count=len(values),fixed_text_preserved=True))
old=load(before/'results/T-037/manifest.json')
manifest=dict(task='T-037',created_utc=datetime.now(timezone.utc).isoformat(),state='AWAITING_CLAUDE_REVIEW_NOT_ACCEPTED',current_run='runs/graph-003',smtp_regression_run='runs/smtp-regression-001',
 source_registry='nguon.json',records='ban-ghi.json',coverage='bao-phu-nguon.json',runtime_contract='hop-dong-runtime.md',
 base_contract=dict(task='T-036',current_run='runs/kiem-r1-after-002',manifest_sha256=sha(ROOT/'results/T-036/manifest.json'),code_hashes='results/T-036/runs/kiem-r1-after-002/code-hashes.json'),
 approved_addendum='hop-dong-smtp.md',actual_code_snapshot='runs/graph-003/code',old_T037_manifest='runs/tiep-smtp-001/before/results/T-037/manifest.json',
 authorization='runs/tiep-smtp-001/authorization.txt',stats=run['stats'],tests_or_heldout_opened=False,downloads_bytes=0,unpacked_bytes=0,runtime_verified=False,rca_benefit_verified=False,
 sibling_pins_changed=False,oracle='oracle-v3.json',oracle_history=['oracle.json initial invalid SMTP grouping retained','oracle-v2.json full independent source requirements before converter','oracle-v3.json correct fixture missing-mapping target'],
 retained_runs=[p.name for p in sorted((BASE/'runs').iterdir()) if p.is_dir()],
 validation='runs/ket-phien-002/final-verification.json',prompt='prompt-claude.txt',files=[])
dump(BASE/'manifest.json',manifest)
print(json.dumps(dict(state=manifest['state'],current_run=manifest['current_run'],owned_entries=len(changed),diff_bytes=(RUN/'changes.diff').stat().st_size),ensure_ascii=False))
