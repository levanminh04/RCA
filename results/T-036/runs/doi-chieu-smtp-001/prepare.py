from pathlib import Path
import json,hashlib,shutil,difflib,re,sys
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
PKG=ROOT/'results/T-038/runs/cap-nhat-goi-smtp-001/package'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def text(p,s):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8') as f:f.write(s)
def append(p,s):
 with Path(p).open('a',encoding='utf-8') as f:f.write(s)
approval='Duyệt gói SMTP V2, triển khai và kiểm đầy đủ cả ba nhánh theo kế hoạch, làm trong một phiên, giữ nguyên kết quả cũ và không dừng sớm.'
plan=load(PKG/'plan.json'); drafts=load(PKG/'docs-before-after.json')
for k,v in load(PKG/'input-state.json').items():assert sha(ROOT/v.get('path',k))==v['sha256'],k
for row in load(PKG/'package-manifest.json')['files']:assert sha(PKG/row['path'])==row['sha256']
for row in drafts['replacements']:
 if 'before_sha256' in row:assert sha(ROOT/row['path'])==row['before_sha256'],row['path']
baselines={};manifeststats={}
for task in ['T-036','T-037','T-038','T-039']:
 p=ROOT/f'results/{task}/manifest.json';m=load(p);n=0
 for row in m['files']:
  q=ROOT/row['path']
  # T036 accepted shared live hash predates the authorized T037 builder delta.
  if task=='T-036' and not row['path'].startswith('results/T-036/'):continue
  assert q.is_file() and sha(q)==row['sha256'],row['path']
  baselines[row['path']]={'sha256':row['sha256'],'bytes':q.stat().st_size};n+=1
 baselines[p.relative_to(ROOT).as_posix()]={'sha256':sha(p),'bytes':p.stat().st_size}
 manifeststats[task]=n
paths=plan['proposed_writes']['permission_and_pin_documents']+plan['proposed_writes']['modify_shared_exact_patch']+plan['proposed_writes']['modify_shared_docs']+['src/do_thi_tinh/build.py','src/do_thi_tinh/__init__.py','AGENTS.md','docs/MRP.md','docs/LESSONS.md','docs/review-prompt.md']
paths+=sum(plan['proposed_writes']['current_outputs_after_all_adoption_pass'].values(),[])
paths+=['results/T-036/manifest.json','results/T-036/hop-dong.md','results/T-035/manifest.json']
for path in sorted(set(paths)):
 p=ROOT/path;target=RUN/'before'/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
 baselines[path]={'sha256':sha(p),'bytes':p.stat().st_size}
save(RUN/'before-hashes.json',baselines)
save(RUN/'authorization.json',dict(intent='EXECUTE',approval_exact=approval,approved_plan=str(PKG/'plan.json'),plan_sha256=sha(PKG/'plan.json'),created_utc=datetime.now(timezone.utc).isoformat(),manifest_verified_counts=manifeststats,scope=plan['proposed_writes'],no_commit_push_test=True))
for task in ['T-037','T-038','T-039']:
 dest=ROOT/f'results/{task}/runs/doi-chieu-smtp-001';dest.mkdir(exist_ok=False)
 for path in plan['proposed_writes']['current_outputs_after_all_adoption_pass'][task]:
  p=ROOT/path;q=dest/'before'/path;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 shutil.copyfile(RUN/'authorization.json',dest/'authorization.json')
for t in ['T-036','T-037','T-038','T-039']:
 dirname=next(p for p in plan['proposed_writes']['permission_and_pin_documents'] if p.startswith('tasks/'+t) and p.endswith('/LOG.md'))
 append(ROOT/dirname,'\n\n### Triển khai gói SMTP V2 — 16/10/2026 — Codex — LEVANMINH — người làm\n\nMinh duyệt nguyên lời: “'+approval+'”\nPhạm vi đúng plan.json V2 và before→after đã duyệt. Làm tuần tự cùng phiên, giữ tất cả output/pin cũ; không tự nghiệm thu, không mở test/heldout, commit/push hoặc gửi agent. Đã kiểm hash manifest/code và lưu before; tiến độ/kết quả mới trong results/'+t+'/runs/doi-chieu-smtp-001/.\n')
decision=ROOT/'docs/DECISIONS.md';numbers=[int(x) for x in re.findall(r'\| Q-(\d+) \|',decision.read_text(encoding='utf-8-sig'))];qid='Q-'+str(max(numbers)+1)
append(decision,'\n| '+qid+' | 16/10/2026 | “'+approval+'” | Phạm vi đúng gói V2 results/T-038/runs/cap-nhat-goi-smtp-001/package/plan.json: đổi comparator SMTP, giữ builder T037, hồi quy full T037/1069TT/132OB, chuyển pin chung sau toàn kiểm đạt; ghi WHY/SPEC/LOG/STATE và outputs hiện hành đúng filelist, giữ lịch sử. Không tự nghiệm thu/G3/test/commit/push. |\n')
for row in drafts['replacements']:
 if row['path']=='docs/WHY.md':append(ROOT/row['path'],row['after_append'].replace('Chọn (sau Minh duyệt):','Chọn theo Minh duyệt '+qid+' ngày16/10/2026:'))
 elif row['path'].endswith('/SPEC.md'):
  append(ROOT/row['path'],row['after_append'].replace('(chỉ nối sau Minh duyệt)','(Minh duyệt '+qid+' ngày16/10/2026)').replace('Nguyên lời và ngày Minh duyệt lấy từ quyết định thực;','Nguyên lời Minh duyệt tại '+qid+' và authorization.json;'))
save(RUN/'decision.json',{'id':qid,'approval_exact':approval})
# Freeze new literal oracles before applying shared comparator.
shutil.copyfile(PKG/'oracle-before-code.json',RUN/'oracle.json')
save(RUN/'adoption-oracle.json',{'T036_R1_checks_unchanged':True,'builder_identical_to_T037':True,'T037_unknown_smtp_missing_trace_channel_endpoint_numerator':0,'T037_typed_unknown_denominator':0,'T038_graphs':1069,'T039_graphs':132,'non_SMTP_unchanged':True,'T038_comparator_only_before_delta_unchanged':True,'trace_inputs_unchanged':True})
src=ROOT/'src/do_thi_tinh/compare.py';candidate=PKG/'experimental_copy/compare.py'
patch=''.join(difflib.unified_diff(src.read_text(encoding='utf-8').splitlines(True),candidate.read_text(encoding='utf-8').splitlines(True),fromfile='a/src/do_thi_tinh/compare.py',tofile='b/src/do_thi_tinh/compare.py'))
assert patch==(PKG/'proposed-shared-code.patch').read_text(encoding='utf-8')
shutil.copyfile(candidate,src);shutil.copyfile(PKG/'README.shared-proposed.md',ROOT/'src/do_thi_tinh/README.md')
for name in ['__init__.py','build.py','compare.py']:
 p=ROOT/'src/do_thi_tinh'/name;q=RUN/'code'/name;q.parent.mkdir(exist_ok=True);shutil.copyfile(p,q)
save(RUN/'code-hashes.json',{name:sha(RUN/'code'/name) for name in ['__init__.py','build.py','compare.py']})
contract=(ROOT/'results/T-036/hop-dong.md').read_text(encoding='utf-8-sig')
text(RUN/'hop-dong.md',contract+'\n\n## Bổ sung V2 được Minh duyệt '+qid+' — 16/10/2026\n\nBuilder tiếp nhận nguyên delta SMTP T037: smtp hợp lệ với gọi-đồng-bộ/gọi-chưa-phân-kiểu; messaging=null. Chặng client→mail-server không là delivery tới người nhận. Type theo bằng chứng riêng, không tự nâng unknown.\n\nComparator nhận channel tùy chọn http/rpc/internal/smtp chỉ với hai loại gọi. Cả endpoints/typed giữ address marker [smtp,null] cho SMTP tường minh. Trace thiếu channel, HTTP/RPC không khớp key SMTP; không suy từ static, không bỏ cạnh SMTP khỏi mẫu số vì trace thiếu protocol. Typed loại unknown như cũ. HTTP/RPC legacy không phân biệt protocol sâu hơn. T035 gốc không đổi; P9 adapter extension cần nguồn/quyền riêng.\n\nMarker null không là authority/port/TLS verified. Context/provenance vẫn giữ literal host/port/configured TLS/outcome. Không suy runtime, broker, operation giả hay accepted=delivered. Projection/ownership/entity-only/shared signal giữ nghĩa cũ; graph dùng chuẩn hóa/chiếu/tập so, chưa scoring RCA.\n\nHợp đồng này và snapshot code được pin bởi manifest run mới; root T036 manifest/hợp đồng và mọi output R1/T037 cũ là lịch sử. Pin mới chỉ publish sau kiểm shared, ba nhánh tiếp nhận sau full replay. Giữ các giới hạn nguồn/runtime, chưa nghiệm thu task/G3/test/commit.\n')
shutil.copyfile(ROOT/'results/T-036/nguon.json',RUN/'nguon.json')
# Adapt original T036 checker by output/root path only; logic/oracles unchanged.
original=(ROOT/'results/T-036/check.py').read_text(encoding='utf-8-sig')
adapted=original.replace('ROOT = Path(__file__).resolve().parents[2]','ROOT = Path('+repr(str(ROOT))+')',1).replace("out = ROOT / 'results/T-036/runs' / sys.argv[1]",'out = Path('+repr(str(RUN/'checks/t036-r1-001'))+')',1)
(RUN/'checks').mkdir()
text(RUN/'check_regression.py',adapted)
text(RUN/'checker-adaptation.diff',''.join(difflib.unified_diff(original.splitlines(True),adapted.splitlines(True))))
print(json.dumps({'ready':True,'decision':qid,'verified_counts':manifeststats,'builder_unchanged':sha(ROOT/'src/do_thi_tinh/build.py')==sha(RUN/'before/src/do_thi_tinh/build.py')},ensure_ascii=False))
