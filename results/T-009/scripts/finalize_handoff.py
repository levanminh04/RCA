import hashlib,json,re
from pathlib import Path
base=Path('results/T-009');run=base/'runs/inspect-004';card=(base/'the-dataset.md').read_text(encoding='utf-8');links=[]
for m in re.finditer(r'\]\(([^)]+)\)',card):
    target=m.group(1)
    if '://' not in target:assert (base/target).exists(),target;links.append(target)
assert len(re.findall(r'^## [0-9]+\.',card,re.M))==20
p=run/'validation.json';v=json.loads(p.read_text(encoding='utf-8'));v.update(card_sections=20,all_card_local_links_exist=True,card_local_links=links);p.write_text(json.dumps(v,indent=2),encoding='utf-8')
log=Path('tasks/T-009-the-dataset-eadro/LOG.md');marker='## Kết thúc nhánh Eadro Q-47 — 03/10/2026 — Codex GPT-6.1 Sol high'
if marker not in log.read_text(encoding='utf-8'):
    with log.open('a',encoding='utf-8') as f:f.write('''

## Kết thúc nhánh Eadro Q-47 — 03/10/2026 — Codex GPT-6.1 Sol high, laptop Windows

1. Đã làm: kiểm toàn ZIP/nested hai hệ; 794 file cuối chỉ CSV/JSON, không PKL. SN-all/TT-all lặp raw/nhãn theo hash (330 member trùng), không cộng ca. 19 phiên raw duy nhất SN7/TT12, 117 nhãn tiêm SN36/TT81, mỗi ô một lần; paper72/162 giữ riêng. Kiểm parent scoped theo dòng và identity riêng: SN span trùng giống hệt, TT có identity xung đột. Kiểm đủ metric/log/time/normal, bậc root toàn file; clock trace/export chưa rõ nên bậc injection-window không diễn giải là cô lập. Probe metric3q từ normal reference/control độc lập: 56.070 dòng từng ca/kênh/q, giữ zero-band/refn/n/exceed, không OR, không nhãn lan/region, không RCA.
2. File thay đổi: scripts/inspect_files.py, summarize_files.py, verify_files.py, finalize_handoff.py; the-dataset.md (hai thẻ10mục), inspection-plan.md; runs/inspect-001/002 failure, inspect-003 complete ban đầu, inspect-004 kết quả cuối/validation/backup/file-list; LOG này. Không sửa SPEC/STATE/DECISIONS/WHY/data README/REVIEW; không Bank/locked, không commit/push. Lỗi parser TAR seekable và thứ tự member được giữ. Một phép kiểm link lỗi encoding cp1252 trước khi ghi kết quả, sửa explicit UTF-8 rồi đạt.
3. Kiểm: inspect-004 toàn archive168,156giây, CRC mọi ZIP member đạt. SHA256/MD5 ZIP khớp nguồn; hash330 cặp nested raw/label khớp ngoài. Independent parent balances/q monotonicity đạt; tính median/band/exceed trực tiếp từ hai CSV gốc×3q khớp. Card20mục và link cục bộ đạt. validation.json, independent-summary.json giữ số gốc. git diff --check không lỗi phạm vi nhánh; đọc các file untracked trực tiếp.
4. OPEN thật: license chưa có permission rõ; clock/history/export trace và SN nginx alias chưa có chứng minh; nhãn onset/vùng không có. TT normal20/4 trong TT-no-fault.txz đã đọc số đo nhưng không vào reference/control do không nhãn faults=[] riêng. G1/split do Minh quyết. Không còn chờ quyền telemetry; đủ bàn giao inspection đã duyệt cho Claude review gộp parent; không tự đóng task.

Bước tiếp: root đọc the-dataset.md và runs/inspect-004/{summary,independent-summary,validation,root-degree-whole-file}.json, symptom-metrics.json; ghép parent/prompt chung+G1 nguyên văn. Không chạy lại inspection hợp lệ. Lệnh kiểm cuối trước LOG: py -3 -B results/T-009/scripts/verify_files.py --run inspect-004 (PASS); finalize_handoff.py kiểm links/countcard/file-list. Rebuild card dùng summarize_files.py --run inspect-004, rồi verify_files.py/finalize_handoff.py. Các lựa chọn mô tả reference/control không phải quyết định detector/G1.
''')
files=[]
for p in sorted(base.rglob('*')):
    if not p.is_file() or p==run/'file-list.json':continue
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    files.append(dict(path=str(p.relative_to(base)).replace('\\','/'),bytes=p.stat().st_size,sha256=h.hexdigest()))
(run/'file-list.json').write_text(json.dumps(dict(task='T-009',current_files=files,log=str(log)),indent=2),encoding='utf-8');print('Eadro handoff/file-list PASS',len(files))
