"""Chốt dòng trạng thái và kiểm diff phiên; không chạy phương pháp trên laptop."""
import ast
import difflib
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

root = Path(__file__).resolve().parents[3]
task = root / 'tasks/T-033-g2-nguyen-nhan-phat-hien'
home = root / 'results/T-033'
old = home / 'runs/prepare-001'
run = home / 'runs/checkpoint-session1-final'
run.mkdir(exist_ok=False)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

snapshot_path=home/'runs/checkpoint-session1-002/remote-snapshot.json'
snapshot=json.loads(snapshot_path.read_text(encoding='utf-8'))
assert snapshot['statuses']['nsigma-first-001']['status']=='PASS'
assert snapshot['statuses']['nsigma-rest-001']['status']=='PASS'
assert snapshot['statuses']['bocpd-first-002']['status']=='PASS'
assert snapshot['statuses']['bocpd-rest-001']['status']=='RUNNING'
ns_records=[(oid,branch,rec) for name in ['nsigma-first-001','nsigma-rest-001']
            for oid,case in snapshot['statuses'][name]['cases'].items()
            for branch,rec in case.items()]
assert len(ns_records)==60 and all(rec['status']=='PASS' and all(rec['checks'].values()) for _,_,rec in ns_records)
assert sha(snapshot_path)==(snapshot_path.parent/'remote-snapshot.sha256').read_text().split()[0]

# Nguồn trạng thái được đọc ngay trước ghi; bảo toàn mọi byte ngoài dòng T-033.
state=root/'docs/STATE.md'
before=state.read_bytes()
(run/'STATE.md.before-close').write_bytes(before)
lines=before.splitlines(keepends=True)
indexes=[i for i,line in enumerate(lines) if line.startswith(b'| T-033 |')]
assert len(indexes)==1
i=indexes[0]
parts=lines[i].decode('utf-8').split('|')
parts[6]=' Đang thực hiện: N-Sigma lõi 60/60 PASS; BOCPD full/FF/PP ca đầu đạt, 29 ca còn lại chạy nền ổn định trên EC2; checkpoint LOG phiên 1. Chưa FP/PF, nền cố định hoặc kết luận cơ chế '
lines[i]='|'.join(parts).encode('utf-8')
state.write_bytes(b''.join(lines))
assert [line for line in before.splitlines(keepends=True) if not line.startswith(b'| T-033 |')]==[line for line in state.read_bytes().splitlines(keepends=True) if not line.startswith(b'| T-033 |')]

spec=task/'SPEC.md'
before=spec.read_bytes()
(run/'SPEC.md.before-close').write_bytes(before)
lines=before.splitlines(keepends=True)
prefix='- **Trạng thái:**'.encode('utf-8')
indexes=[i for i,line in enumerate(lines) if line.startswith(prefix)]
assert len(indexes)==1
i=indexes[0]
ending=b'\r\n' if lines[i].endswith(b'\r\n') else b'\n'
lines[i]=('- **Trạng thái:** Minh duyệt SPEC và thực hiện ngày 09/10/2026 (Q-91, Q-92; lời duyệt "ĐÃ CHỐT"); SPEC đã khóa. Đang thực hiện các chặng được duyệt; tiến độ ở dòng T-033 STATE và LOG.').encode('utf-8')+ending
spec.write_bytes(b''.join(lines))
assert [line for line in (old/'SPEC.md.before').read_bytes().splitlines(keepends=True) if not line.startswith(prefix)]==[line for line in spec.read_bytes().splitlines(keepends=True) if not line.startswith(prefix)]
why=root/'docs/WHY.md'
oldwhy=(old/'WHY.md.before').read_bytes()
assert why.read_bytes().startswith(oldwhy)
appendix=spec.read_text(encoding='utf-8').split('## Phụ lục — dự thảo WHY-41\n',1)[1].split('\n## Prompt bàn giao',1)[0].strip()
suffix=why.read_bytes()[len(oldwhy):].decode('utf-8')
expected='\n\n## WHY-41. Lần theo cơ chế phát hiện — Đã quyết (Minh duyệt SPEC T-033 ngày 09/10/2026)\n\n'+appendix+'\n'
assert suffix==expected
assert (root/'AGENTS.md').read_bytes()==(old/'AGENTS.md.before').read_bytes()

ast_checks={}
for p in (home/'scripts').glob('*.py'):
    ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    ast_checks[p.name]=True

status=snapshot['statuses']['bocpd-rest-001']
bo_valid=[oid for oid,case in status['cases'].items() if case.get('full',{}).get('status')=='PASS' and case.get('PP',{}).get('status')=='PASS' and case.get('FF',{}).get('m_prefix_match') is True and case.get('FF',{}).get('cp_prefix_match') is True]
now=datetime.now(timezone(timedelta(hours=7))).isoformat()
log=task/'LOG.md'
log_before=log.read_bytes()
(run/'LOG.md.before-close').write_bytes(log_before)
end=f'''

### Kết thúc phiên 1 — {now}

1. Đã làm: khóa nguồn/nhóm ban đầu, nối WHY-41 theo phụ lục duyệt; preflight dev/env/index đạt; N-Sigma native 60/60 đầu ra đạt; BOCPD ca đầu full/FF/PP đạt và lô còn lại chạy nền. Snapshot mới: `results/T-033/runs/checkpoint-session1-002/remote-snapshot.json` → `/statuses`, `/completed_case_branches`, `/resources`, `/scripts`. Tại snapshot, lô còn lại đã hoàn tất full/FF/PP cho {len(bo_valid)} ca: {', '.join(bo_valid) or 'chưa có'}; PID {status['pid']}, status {status['status']}. Snapshot cũ vẫn giữ. Chưa xong task.
2. File thay đổi trong phiên: `results/T-033/` (scripts, source/flags đóng gói, manifest, khóa nhóm, snapshot); tạo và nối `tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md`; chỉ dòng trạng thái `SPEC.md`; chỉ dòng T-033 `docs/STATE.md`; chỉ nối WHY-41 vào `docs/WHY.md`. EC2 chỉ ghi `~/rca/T-033/`. Không sửa DECISIONS hay nguồn/code/data cũ, không test/locked/heldout, không commit/push, không bật/tắt EC2. Không đọc/ghi vùng kết quả T-032.
3. Kiểm: hash nguồn cũ và allowlist/dev; N-Sigma toàn cờ/time/columns/hợp native; fixture không nhãn và phép tính tay; BOCPD full/PP source exact, ca đầu same-input native, FF m/CP từng ca hợp lệ; trung gian posterior/normalizer/theta. Lượt metadata lỗi giữ nguyên, recheck chỉ schema khôi phục contract. Snapshot hai đầu cùng hash. Tự kiểm diff lưu `results/T-033/runs/checkpoint-session1-final/scope-verification.json` và `own-diff.txt`: SPEC ngoài dòng status không đổi; lần đóng chỉ dòng T-033 STATE đổi, bảo toàn T-032; WHY prefix và phụ lục chính xác; AGENTS giữ nguyên; AST mọi script đạt. Chưa có kết luận nghiên cứu từ việc khớp nguồn.
4. OPEN và việc Minh cần làm: cần các nhánh bổ sung, độ trễ/kênh, tính tay/đối chứng và tổng hợp để phân xử cơ chế RQ2/P4; chưa chọn thiết kế P6 hay đóng G2. Ngân sách còn lại phải đo lại trước các nhánh mới; lô đang chạy có guard dừng lỗi/budget. EC2 còn cần bật; Minh có thể tắt laptop cho lô lõi hiện tại, ước lượng xong lô 05:30–08:30 ngày 10/10 +07, chưa phải hoàn tất T-033. Theo AGENTS §5a.2, đề nghị Minh mở phiên Codex mới khi quay lại, tiếp cùng task sau checkpoint; giữ vai trò, không gửi phản biện khi task chưa xong.

Lệnh cuối cùng đã chạy: Python `-B -X utf8 results/T-033/scripts/finish_session1.py` trên laptop để chốt trạng thái/LOG và kiểm phạm vi. Lệnh EC2 cuối: snapshot-only `checkpoint_remote.py --name checkpoint-session1-002`, sau đó chép snapshot+hash về; worker nền không đổi. Bước tiếp theo chính xác: đọc LOG checkpoint trên; SSH kiểm `bocpd-rest-001/status.json`, stdout/stderr/exit, PID từ status và `~/rca/T-033/trang-thai.txt`; kiểm hash manifest của đơn vị đã hoàn tất trước dùng. Không khởi trùng/làm lại ca PASS. Sau khi lõi liên quan đã khớp, tiếp các chặng SPEC và cập nhật dự toán; nếu STOPPED hoặc dự toán vượt giới hạn thì dừng phần phụ thuộc và trình Minh.

Prompt Minh mở phiên Codex tiếp (tiếp thực hiện, chưa là prompt phản biện):

> Đọc AGENTS.md, làm tiếp T-033 trong STATE. Minh đã duyệt thực hiện 09/10/2026 theo lời "ĐÃ CHỐT", phạm vi/ngân sách và ràng buộc trong LOG phiên 1. Đọc toàn SPEC và mục cuối LOG T-033. EC2 3.107.246.249 có lô bocpd-rest-001 đang chạy nền, không khởi trùng hoặc chạy lại đơn vị PASS. Kiểm PID/status/progress, hash nguồn và manifest trước dùng; tiếp phần còn thiếu đúng các chặng, ưu tiên tính đúng. Giữ các giới hạn ghi song song T-032, không test/locked/heldout, không commit/push, không bật/tắt EC2. Nếu lỗi khoa học hay vượt dự toán, checkpoint và trình Minh. Khi task xong mới soạn prompt Claude theo mẫu.
'''
with log.open('ab') as f: f.write(end.encode('utf-8'))
assert log.read_bytes().startswith(log_before)

diffs=[]
for name,b0,b1 in [
    ('SPEC.md',(old/'SPEC.md.before').read_bytes(),spec.read_bytes()),
    ('STATE.md: close-step',(run/'STATE.md.before-close').read_bytes(),state.read_bytes()),
    ('WHY.md',oldwhy,why.read_bytes()),
    ('LOG.md: close-step',log_before,log.read_bytes())]:
    diffs.extend(difflib.unified_diff(b0.decode('utf-8').splitlines(True),b1.decode('utf-8').splitlines(True),fromfile=name+' before',tofile=name+' after'))
(run/'own-diff.txt').write_text(''.join(diffs),encoding='utf-8')
file_set={str(p.relative_to(root)).replace('\\','/'):{'sha256':sha(p),'bytes':p.stat().st_size} for p in home.rglob('*') if p.is_file() and run not in p.parents}
for p in [spec,state,why,log]: file_set[str(p.relative_to(root)).replace('\\','/')]={'sha256':sha(p),'bytes':p.stat().st_size}
result={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
        'spec_only_status':True,'state_close_only_T033':True,'why_appendix_exact':True,
        'AGENTS_unchanged':True,'LOG_append_only':True,'script_AST':ast_checks,
        'core_nsigma_records_PASS':60,'bocpd_first_PASS':True,
        'bocpd_rest_status':status['status'],'bocpd_rest_completed_full_FF_PP':bo_valid,
        'snapshot_sha256':sha(snapshot_path),'changed_file_set':file_set,
        'research_questions_closed':False,'task_complete':False}
(run/'scope-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({key:result[key] for key in ['status','core_nsigma_records_PASS','bocpd_rest_status','bocpd_rest_completed_full_FF_PP','task_complete']},ensure_ascii=False))
