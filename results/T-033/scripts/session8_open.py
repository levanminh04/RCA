"""Laptop metadata/hash/transport only. Research stays on the pinned EC2."""
import pathlib,json,hashlib,datetime,shutil,ast
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT=ROOT/'results/T-033/runs/session8-open-001'
OUT.mkdir(exist_ok=False)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
for name in ['session7-storage-checkpoint-001','session7-storage-approval-checkpoint-001']:
 base=ROOT/'results/T-033/runs'/name
 entries=read(base/'manifest.json')['files'];bad=[]
 for rel,m in entries.items():
  p=ROOT/rel
  if rel=='tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md' and name=='session7-storage-checkpoint-001':
   p=ROOT/'results/T-033/runs/session7-storage-approval-checkpoint-001/LOG.md.before'
  if rel=='docs/STATE.md' and name=='session7-storage-checkpoint-001':
   p=ROOT/'results/T-033/runs/session7-storage-approval-checkpoint-001/STATE.md.before'
  if p.stat().st_size!=m['bytes'] or sha(p)!=m['sha256']:bad.append(rel)
 assert not bad,(name,bad)
 checks.append({'manifest':str((base/'manifest.json').relative_to(ROOT)),'files':len(entries),'status':'PASS'})
for name in ['checkpoint-handoff-001','session6-compute-checkpoint-001']:
 base=ROOT/'results/T-033/runs'/name
 entries=read(base/'artifact-inventory.json');entries=entries.get('files',entries)
 if isinstance(entries,list):entries={v.get('path',v.get('relative_path')):v for v in entries}
 bad=[]
 for rel,m in entries.items():
  p=base/'artifacts'/rel
  if p.stat().st_size!=m['bytes'] or sha(p)!=m['sha256']:bad.append(rel)
 assert not bad,(name,bad)
 checks.append({'inventory':str((base/'artifact-inventory.json').relative_to(ROOT)),'files':len(entries),'status':'PASS'})
# Historical manifest pins are checked against preserved snapshots, never live appends.
base=ROOT/'results/T-033/runs/session6-compute-checkpoint-001'
entries=read(base/'manifest.json')['files']
for rel,m in entries.items():
 p=(ROOT/'results/T-033/runs/session7-open-001'/(pathlib.Path(rel).name+'.before')) if rel in ['docs/STATE.md','tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'] else ROOT/rel
 assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],rel
checks.append({'manifest':str((base/'manifest.json').relative_to(ROOT)),'files':len(entries),'status':'PASS'})
protected=['AGENTS.md','docs/DECISIONS.md','docs/WHY.md','docs/MRP.md','docs/LESSONS.md','docs/review-prompt.md','tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md']
log=ROOT/'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md';state=ROOT/'docs/STATE.md'
shutil.copyfile(log,OUT/'LOG.md.before');shutil.copyfile(state,OUT/'STATE.md.before')
write(OUT/'baseline.json',{'protected':{r:{'sha256':sha(ROOT/r),'bytes':(ROOT/r).stat().st_size} for r in protected},'old_t033_files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in (ROOT/'results/T-033').rglob('*') if p.is_file() and not p.is_relative_to(OUT)}})
write(OUT/'integrity.json',{'status':'PASS','checks':checks})
stamp=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
with log.open('a',encoding='utf-8',newline='\n') as f:
 f.write('\n\n## Phiên 8 — '+stamp+' — Codex — laptop Windows 11 và EC2 T-033 — Người làm\n\n- EXECUTE theo SPEC, tiếp lời duyệt 5GiB/bản trích v2/pilot rồi rest; không xin lại. Codex làm, Claude phản biện. Đã đọc AGENTS/STATE/SPEC/LOG/checkpoint cuối, kiểm manifest/hash trước dùng. Giữ mọi run lỗi, không chạy lại detector PASS, không xóa thêm. Một trợ lý chỉ đọc soát mã trích, không là phản biện chính thức.\n- Ledger nối nguyên snapshot cuối phiên7 và timer mới; mọi EC2 mới có đo. Phạm vi results/T-033/, LOG nối, chỉ dòng T-033 STATE và EC2 ~/rca/T-033/. Không sửa nguồn/môi trường/phương pháp/SPEC/WHY/DECISIONS, không test/locked/heldout/commit/push.\n')
# Preserve old controller; only transport snapshot paths change.
s=(ROOT/'results/T-033/scripts/session7_control.py').read_text(encoding='utf-8-sig')
s=s.replace("runs/session7-open-001'","runs/session8-open-001'").replace("runs/session6-final-budget-001/ledger.json'","runs/session7-storage-approval-checkpoint-001/ledger.json'")
(ROOT/'results/T-033/scripts/session8_control.py').write_text(s,encoding='utf-8',newline='\n')
inp=read(ROOT/'results/T-033/runs/session7-open-001/extract-input.json')
for n in ['points-lock.json','coverage-matching.json']:
 p=ROOT/'results/T-033/runs/session7-open-001'/n
 inp['pins']['runs/session7-manual-001/'+n]={'sha256':sha(p),'bytes':p.stat().st_size}
inp.update(storage_extension_authorized=True,approved_storage_limit_bytes=5*2**30,run_name='session7-manual-pilot-001',selected_case_ids=['dev-03d4910932'])
write(OUT/'pilot-input.json',inp)
rest=dict(inp);rest['run_name']='session7-manual-rest-001';rest['selected_case_ids']=sorted({x['opaque_id'] for x in inp['locator']['core']}-{'dev-03d4910932'})
assert len(rest['selected_case_ids'])==29
write(OUT/'rest-input.json',rest)
ast.parse(s);ast.parse((ROOT/'results/T-033/scripts/session7_extract_v2.py').read_text())
print(json.dumps({'status':'PASS','checks':checks,'pilot':inp['selected_case_ids'],'rest_count':29,'ledger_base':'session7-storage-approval-checkpoint-001/ledger.json'}))
