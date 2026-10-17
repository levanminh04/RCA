"""Begin the authorized SMTP repair and T037 continuation, preserving old artifacts."""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone

ROOT=Path('D:/RCA-flashticket');BASE=ROOT/'results/T-037';RUN=BASE/'runs/tiep-smtp-001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
RUN.mkdir(parents=True,exist_ok=False)
errors=[];checks=[]
for rel in ['results/T-036/manifest.json','results/T-037/manifest.json']:
 m=load(ROOT/rel)
 for e in m['files']:
  p=(ROOT/e['path']).resolve();assert p.is_relative_to(ROOT) and not p.is_relative_to(ROOT/'data')
  ok=p.is_file() and sha(p)==e['sha256'] and p.stat().st_size==e['bytes']
  checks.append({'path':e['path'],'matches':ok})
  if not ok:errors.append(e['path'])
 if rel.endswith('T-037/manifest.json'):
  for e in m['files']:
   p=ROOT/e['path']
   if p.parent==BASE:
    target=RUN/'before'/e['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
  p=ROOT/rel;target=RUN/'before'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
for rel in ['src/do_thi_tinh/build.py','src/do_thi_tinh/compare.py','src/do_thi_tinh/__init__.py','src/do_thi_tinh/README.md','tasks/T-037-p5b-flashticket/LOG.md','docs/STATE.md']:
 p=ROOT/rel;target=RUN/'before'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
guard=['AGENTS.md','docs/WHY.md','docs/DECISIONS.md','docs/LESSONS.md','docs/MRP.md','docs/review-prompt.md',
 'tasks/T-037-p5b-flashticket/SPEC.md','tasks/T-038-p5b-trainticket/SPEC.md','tasks/T-039-p5b-online-boutique/SPEC.md',
 'results/T-036/manifest.json','results/T-036/runs/kiem-r1-after-002/code-hashes.json']
registry=load(BASE/'nguon.json')
for s in registry['sources']:
 ok=sha(Path(s['path']))==s['sha256'];checks.append({'path':s['path'],'matches':ok})
 if not ok:errors.append(s['path'])
pin=load(ROOT/'results/T-036/runs/kiem-r1-after-002/code-hashes.json')
for rel,expected in pin.items():
 checks.append({'path':rel,'matches':sha(ROOT/rel)==expected})
 if sha(ROOT/rel)!=expected:errors.append(rel)
result={'client_date':'2026-10-16','utc':datetime.now(timezone.utc).isoformat(),'device':platform.node(),
 'intent':'EXECUTE','role':'Codex người làm, Claude phản biện kết quả',
 'authorization':'Vậy sửa hỗ trợ SMTP và kiểm lại, giữ nguyên T-038/T-039 đang chạy. Sau khi kiểm đạt thì tiếp tục T-037, không tự đổi pin của hai nhánh kia.',
 'all_checks':checks,'errors':errors,'protected':{rel:sha(ROOT/rel) for rel in guard},
 'old_manifest':'runs/tiep-smtp-001/before/results/T-037/manifest.json',
 'original_pin':load(ROOT/'results/T-036/manifest.json')['current_run'],
 'tracked_diff_before':subprocess.check_output(['git','-C',str(ROOT),'diff','HEAD','--binary'],stderr=subprocess.PIPE).decode('utf-8',errors='replace'),
 'budget_estimate_unmeasured':{'remaining_work_hours':[3,5],'machine_minutes':[2,10],'peak_ram_MiB':512,'total_output_MB_including_prior_and_ten_retained_runs':200,'download_bytes':0}}
dump(RUN/'preflight.json',result)
if errors:raise SystemExit('INPUT_DRIFT_STOP '+str(errors))
with (ROOT/'tasks/T-037-p5b-flashticket/LOG.md').open('a',encoding='utf-8') as f:
 f.write('''\n\n## Phiên 3 — 16/10/2026 — Codex — LeVanMinh (Windows 11) — người làm

**Nguyên văn lời Minh mới:** “Vậy sửa hỗ trợ SMTP và kiểm lại, giữ nguyên T-038/T-039 đang chạy. Sau khi kiểm đạt thì tiếp tục T-037, không tự đổi pin của hai nhánh kia.” Trước đó Minh duyệt mục1 hỗ trợ SMTP; câu hỏi về kiểm/đồng bộ không là quyền sửa hai SPEC. Phạm vi thực hiện: sửa src/do_thi_tinh/build.py thêm channel smtp cho quan hệ gọi; lưu oracle/kiểm/hồi quy/snapshot hợp đồng bổ sung và đầu ra trong results/T-037/, nối LOG này và chỉ dòng T037 trong STATE. Không sửa T036 snapshot/manifest hoặc T038/T039. T037 dùng pin gốc cộng bổ sung SMTP đã duyệt, không giả vờ bản sửa khớp hash pin cũ.

**Mở phiên/tự rà:** đọc lại AGENTS, STATE, SPEC/LOG T037 và các nguồn chi phối; kiểm manifest T036/T037, code hiện hành và nguồn platform trước dùng tại runs/tiep-smtp-001/preflight.json. Giữ các output đã hợp lệ, chỉ bổ sung phần thiếu. Nguồn thiết kế FORMATION/CANDIDATE; DT18/cô và MRP vẫn yêu cầu mapping đủ3tínhiệu, không xác nhận runtime/lợi ích hoặc chọn P6. Hai phần hỗ trợ thu nguồn/soạn phép kiểm trong phạm vi riêng, không là reviewer chính thức. Không tải nguồn, không mở test/heldout/telemetry thật.

**Chi phí còn lại — dự toán chưa đo:** 3–5 giờ công gồm coverage/đọc nguồn dẫn xuất, bản ghi/oracle/graph/fixtures và bàn giao; máy2–10phút, peakRAM dưới512MiB; tổng output cả lịch sử+lỗi/10lượt dự kiến dưới200MB. Đo sau khi không việc nặng khác; không suy giờ công từ giờ máy, không chạy quá1giờ hoặc thay tiêu chí cho vừa thời gian. Phần SMTP kiểm đạt mới chạy chuyển đổi T037. Bản đồ ảnh hưởng: source build.py; dẫn xuất trong T037; không đổi quyết định P6/khóa G3, không ghi DECISIONS/WHY từ quyền cũ. Nội dung sổ chính thức cần trình riêng cuối phiên; quyền SMTP mới được lưu nguyên văn ở đây và authorization run.
''')
(RUN/'authorization.txt').write_text(result['authorization']+'\n',encoding='utf-8')
print(json.dumps({'checks':len(checks),'errors':errors,'device':result['device'],'old_pin':result['original_pin']},ensure_ascii=False))
