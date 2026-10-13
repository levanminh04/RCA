"""Metadata/hash and authorized session opening only; no research computation."""
import pathlib,json,hashlib,datetime,shutil
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT=ROOT/'results/T-033/runs/session9-open-001'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def meta(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
logrel='tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'
for name in ['session8-compute-evidence-checkpoint-001','session7-storage-approval-checkpoint-001','session7-storage-checkpoint-001','session6-compute-checkpoint-001']:
 base=ROOT/'results/T-033/runs'/name; entries=read(base/'manifest.json')['files'];bad=[]
 for rel,m in entries.items():
  p=ROOT/rel
  if rel in [logrel,'docs/STATE.md']:
   snap={'session8-compute-evidence-checkpoint-001':('session8-compute-evidence-checkpoint-001','after'),
    'session7-storage-approval-checkpoint-001':('session8-open-001','before'),
    'session7-storage-checkpoint-001':('session7-storage-approval-checkpoint-001','before'),
    'session6-compute-checkpoint-001':('session7-open-001','before')}[name]
   p=ROOT/'results/T-033/runs'/snap[0]/(pathlib.Path(rel).name+'.'+snap[1])
  if not p.is_file() or meta(p)!=m:bad.append(rel)
 checks.append({'source':str((base/'manifest.json').relative_to(ROOT)),'files':len(entries),'mismatches':bad})
 assert not bad,(name,bad)
for name in ['checkpoint-handoff-001','session6-compute-checkpoint-001','session8-extraction-001','session8-evidence-receive-001','session8-stats-receive-001']:
 base=ROOT/'results/T-033/runs'/name;entries=read(base/'artifact-inventory.json');entries=entries.get('files',entries)
 if isinstance(entries,list):entries={v.get('path',v.get('relative_path')):v for v in entries}
 bad=[]
 for rel,m in entries.items():
  p=base/'artifacts'/rel
  if not p.is_file() or meta(p)!={'bytes':m['bytes'],'sha256':m['sha256']}:bad.append(rel)
 checks.append({'source':str((base/'artifact-inventory.json').relative_to(ROOT)),'files':len(entries),'mismatches':bad})
 assert not bad,(name,bad)
OUT.mkdir(exist_ok=False)
protected=['AGENTS.md','docs/DECISIONS.md','docs/WHY.md','docs/MRP.md','docs/LESSONS.md','docs/review-prompt.md','tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md']
shutil.copyfile(ROOT/logrel,OUT/'LOG.md.before');shutil.copyfile(ROOT/'docs/STATE.md',OUT/'STATE.md.before')
write(OUT/'baseline.json',{'protected':{r:meta(ROOT/r) for r in protected},'old_t033_files':{str(p.relative_to(ROOT)):meta(p) for p in (ROOT/'results/T-033').rglob('*') if p.is_file() and not p.is_relative_to(OUT)}})
write(OUT/'integrity.json',{'status':'PASS','checks':checks,'historical_LOG_STATE_snapshots':True})
stamp=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
with (ROOT/logrel).open('a',encoding='utf-8',newline='\n') as f:
 f.write('\n\n## Phiên 9 — '+stamp+' — Codex — laptop Windows 11 và EC2 T-033 — Người làm\n\n- EXECUTE theo yêu cầu đính kèm của Minh và SPEC đã duyệt; Codex làm, Claude phản biện. Tiếp đọc tay/tổng hợp toàn task; giữ trần 5GiB và 4h xử lý mới, không xin lại. Kiểm manifest/inventory nguồn theo snapshot LOG/STATE lịch sử PASS. Không rerun detector PASS, không đổi khóa/tiêu chí/tham số, không xóa thêm.\n- Chỉ ghi lượt mới results/T-033/, LOG nối, duy nhất dòng T-033 STATE và EC2 ~/rca/T-033/. Ledger base session8-compute-evidence-checkpoint-001/ledger.json; chỉ cộng timer phiên9. Mọi EC2 mới phải kiểm process/source/hash có đo trước xử lý. Theo chỉ dẫn riêng mới của Minh: nén thì checkpoint vẹn toàn rồi tiếp trong cùng phiên; các điều kiện dừng vì hash/quyền/trần giữ nguyên. Không mở/gửi phản biện chính thức hoặc commit/push.\n')
s=(ROOT/'results/T-033/scripts/session8_control.py').read_text(encoding='utf-8-sig')
s=s.replace("runs/session8-open-001'","runs/session9-open-001'").replace("runs/session7-storage-approval-checkpoint-001/ledger.json'","runs/session8-compute-evidence-checkpoint-001/ledger.json'")
(ROOT/'results/T-033/scripts/session9_control.py').write_text(s,encoding='utf-8',newline='\n')
print(json.dumps({'status':'PASS','checks':checks},ensure_ascii=False))
