"""Publish all three current views only after every approved full replay passes."""
from pathlib import Path
from collections import defaultdict,Counter
import json,hashlib,shutil,gzip,copy,re,sys,time,msvcrt,ast
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent
PKG=ROOT/'results/T-038/runs/cap-nhat-goi-smtp-001/package'
PLAN=json.loads((PKG/'plan.json').read_text(encoding='utf-8-sig'))
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def text(p,s):Path(p).write_text(s,encoding='utf-8')
def append(p,s):
 with Path(p).open('a',encoding='utf-8') as f:f.write(s)
def rel(p):return Path(p).relative_to(ROOT).as_posix()
dirs={t:ROOT/f'results/{t}/runs/doi-chieu-smtp-001' for t in ['T-037','T-038','T-039']}
checks={'T-037':dirs['T-037']/'checks/full-model-001/result.json','T-038':dirs['T-038']/'checks/full1069-002/summary.json','T-039':dirs['T-039']/'checks/full132-001/summary.json'}
res={t:load(p) for t,p in checks.items()}
assert res['T-037']['all_pass'] and res['T-037']['passed']==1598
assert res['T-038']['all_pass'] and res['T-038']['graph_count']==1069
assert res['T-039']['all_pass'] and res['T-039']['graph_count']==132
pin=load(dirs['T-038']/'pin.json');assert all(load(d/'pin.json')==pin for d in dirs.values())
assert sha(ROOT/pin['manifest'])==pin['manifest_sha256']
for name,digest in pin['code_hashes'].items():assert sha(ROOT/'src/do_thi_tinh'/name)==digest
save(RUN/'pin.json',pin)
# Full FT model and all non-SMTP fixture results are identical. Preserve the
# protocol-dependent legacy fixture and record its intentional before/after.
fd=dirs['T-037'];ftcheck=fd/'checks/full-model-001';priorft=ROOT/'results/T-037/runs/graph-003'
for name in ['entity.json','operation.json','projection.json','fixture-compare-two-queues.json','fixture-compare-missing-address.json','fixture-compare-missing-operation.json','fixture-trace-graphs.json']:
 assert load(ftcheck/name)==load(priorft/name),name
priorunknown=load(priorft/'fixture-compare-unknown.json');newunknown=load(ftcheck/'fixture-compare-unknown.json')
assert priorunknown['views']['endpoints']['numerator']==1 and newunknown['views']['endpoints']['numerator']==0
assert priorunknown['views']['typed']==newunknown['views']['typed']
save(fd/'diff.json',dict(all_pass=True,full_model_projection_and_non_SMTP_fixtures_exact_equal=True,passed=1598,
 unknown_SMTP_missing_trace_channel=dict(before_intersection=1,after_intersection=0,typed_unchanged=True,original_fixture=rel(priorft/'fixture-compare-unknown.json'),new_fixture=rel(ftcheck/'fixture-compare-unknown.json'))))
oldhash=load(RUN/'before-hashes.json')
allowed=set(PLAN['proposed_writes']['permission_and_pin_documents']+PLAN['proposed_writes']['modify_shared_exact_patch']+PLAN['proposed_writes']['modify_shared_docs']+sum(PLAN['proposed_writes']['current_outputs_after_all_adoption_pass'].values(),[]))
assert all(sha(ROOT/p)==v['sha256'] for p,v in oldhash.items() if p not in allowed),'unapproved mutation before publishing'
# Model/graph updates occur only when semantic content actually changes.
for t,d in dirs.items():
 base=ROOT/'results'/t
 for name in ['ban-ghi.json','nguon.json','mapping.json','do-thi/thuc-the.json','do-thi/thao-tac.json']:
  staged=d/name
  if t=='T-037':
   staged=d/'checks/full-model-001'/({'do-thi/thuc-the.json':'entity.json','do-thi/thao-tac.json':'operation.json'}.get(name,name))
  target=base/name
  if staged.is_file() and (not target.exists() or load(staged)!=load(target)):
   assert rel(target) in allowed;shutil.copyfile(staged,target)

# Build all current TT descriptive statistics from new per-graph outputs.
t='T-038';d=dirs[t];base=ROOT/'results'/t;summary=res[t]
grouped=defaultdict(list);union=defaultdict(set);full=[];exclusions={};chains=[]
oldanalysis=load(d/'before/results/T-038/phan-tich-chenh-lech.json')
chainkeys={canon(x['key']) for x in oldanalysis['chain_examples']}
for row in summary['rows']:
 family=Path(row['input']).stem.split('-')[0]
 for vn,counts in row['views'].items():
  counts['static_fraction']=counts['intersection']/counts['S'] if counts['S'] else None
  counts['trace_fraction']=counts['intersection']/counts['T'] if counts['T'] else None
  grouped[(row['level'],family,vn)].append(counts)
 if family!='full':continue
 p=ROOT/row['output'];assert sha(p)==row['output_sha256'];result=json.loads(gzip.decompress(p.read_bytes()))
 full.append({k:row[k] for k in ['input','output','level','views']})
 for vn,v in result['views'].items():
  for cat in ['S','T','intersection','static_only','trace_only']:union[(row['level'],vn,cat)].update(map(canon,v[cat]))
  for side,items in v['exclusions'].items():
   for x in items:exclusions.setdefault((row['level'],vn,side,x['reason']),dict(output=row['output'],exclusion=x))
  if row['level']=='entity' and vn=='endpoints':
   for cat in ['intersection','static_only','trace_only']:
    for key in v[cat]:
     if canon(key) in chainkeys or key[3]==['smtp',None]:
      chains.append(dict(input=row['input'],output=row['output'],key=key,category=cat,static_members=[x for x in v['members']['static'] if x['key']==key],trace_members=[x for x in v['members']['trace'] if x['key']==key]))
family_stats=[]
for (level,family,vn),values in sorted(grouped.items()):
 s={}
 for k in ['S','T','intersection','static_only','trace_only','static_fraction','trace_fraction']:
  distinct=sorted({v[k] for v in values if v[k] is not None});s[k]=dict(min=min(distinct) if distinct else None,max=max(distinct) if distinct else None,null_count=sum(v[k] is None for v in values),distinct=distinct)
 family_stats.append(dict(level=level,family=family,view=vn,graph_count=len(values),values=s))
analysis=copy.deepcopy(oldanalysis);doc=load(base/'ban-ghi.json')
analysis.update(comparison_run='doi-chieu-smtp-001',numerical_source=rel(d/'summary.json'),family_stats=family_stats,full_graphs=full,
 full_union=[dict(level=k[0],view=k[1],category=k[2],keys=[json.loads(x) for x in sorted(v)]) for k,v in sorted(union.items())],
 exclusions=[dict(level=k[0],view=k[1],side=k[2],reason=k[3],**v) for k,v in sorted(exclusions.items())],chain_examples=chains,
 numerical_comparison_unchanged=False,SMTP_V2_diff=rel(d/'diff.json'),historical_analysis=rel(d/'before/results/T-038/phan-tich-chenh-lech.json'),
 non_SMTP_comparator_only_exact_unchanged_graphs=1069)
analysis['source_counts']['relations']=len(doc['relations']);analysis['source_counts']['entity_graph_edges']=len(load(base/'do-thi/thuc-the.json')['edges'])
save(d/'analysis-current.json',analysis);save(base/'phan-tich-chenh-lech.json',analysis)
save(d/'summary.json',summary)
save(base/'doi-chieu/index.json',dict(current_run='doi-chieu-smtp-001',summary=rel(d/'summary.json'),graph_count=1069,outputs=[x['output'] for x in summary['rows']],pin_file=rel(d/'pin.json'),historical_current_run='doi-chieu-dev-002'))
oldmd=(d/'before/results/T-038/phan-tich-chenh-lech.md').read_text(encoding='utf-8-sig')
prefix='''# Kết quả hiện hành T-038 theo SMTP V2

Đã so đủ1069graph dev bằng cùng pin V2 với T037/T039. Số mới lấy từ runs/doi-chieu-smtp-001/checks/full1069-002/summary.json và phan-tich-chenh-lech.json. Mỗi graph được replay R1 khớp nguyên kết quả đã lưu; comparator mới trên model cũ cũng bằng nguyên kết quả cũ. Delta SMTP tăng đúng một key S/static-only ở endpoints mỗi graph, tăng một loại trừ unknown_type phía static ở typed; tập đủ điều kiện typed, T, giao và phía trace giữ nguyên. Mẫu số static endpoints tăng1 nên tỷ lệ phía static phải đọc bản thống kê mới, không dùng bảng cũ.

Quan hệ mới dùng source MailService/config có provenance, giữ gọi-chưa-phân-kiểu và giới hạn authority/TLS/delivery/runtime. Record ID SMTP:mail-send:proposed-only giữ từ oracle được duyệt để truy cùng dòng preview; hậu tố lịch sử không còn là trạng thái áp dụng, trạng thái thật nằm manifest/pin. Không suy source-only là runtime không gửi hoặc telemetry lỗi. Delta đã kiểm tách khỏi comparator, không đổi mapping/nhãn để tăng giao.

Các chuỗi nguồn và giải thích cạnh tranh khôngSMTP của phân tích trước giữ giá trị trong phạm vi có điều kiện. Bản đầy đủ trước chuyển nằm runs/doi-chieu-smtp-001/before/results/T-038/phan-tich-chenh-lech.md; các bảng số trong bản ấy là R1 lịch sử. File JSON hiện hành đã dựng lại toàn family/full/union/exclusion/member chains từ output mới. Lineage/runtime, phần PDF lịch sử và nguồn dynamic vẫn OPEN, chưa trả lời lợi ích RCA/RQ3/RQ5/P6/G3.

## Phân tích R1 giữ để đối chiếu lịch sử (không dùng số này thay kết quả V2)

'''
text(base/'phan-tich-chenh-lech.md',prefix+oldmd)

# OB all results are exactly equal; preserve original analysis as a named historical section.
t='T-039';d=dirs[t];base=ROOT/'results'/t
save(d/'summary.json',res[t]);save(base/'doi-chieu/tong-hop.json',res[t])
oldmd=(d/'before/results/T-039/phan-tich-chenh-lech.md').read_text(encoding='utf-8-sig')
text(base/'phan-tich-chenh-lech.md','# Kết quả hiện hành T-039 theo SMTP V2\n\nĐã replay132/132graph dưới snapshot R1 và comparator V2; mỗi kết quả mới bằng nguyên kết quả cũ, gồm sets/members/exclusions/mẫu số/interval. Model và mapping giữ nguyên; lặp/đảo/input bất biến đạt. Nguồn số và output hiện hành ở runs/doi-chieu-smtp-001/checks/full132-001/summary.json, diff.json và pin.json. Phân tích nguồn dưới đây được giữ, số không đổi do bằng nhau toàn artifact; các đường dẫn run004 là bằng chứng lịch sử, đầu ra mới theo summary hiện hành. Inventory toàn deployment/runtime/Node/alias vẫn OPEN, chưa nghiệm thu/P6/G3.\n\n'+oldmd)

limits='Runtime/build/instrumentation/deployment lineage, authority/port/TLS/delivery và các OPEN nguồn giữ nguyên. Chưa xác nhận lợi ích RCA/RQ3/RQ5, chọn P6, nghiệm thu task hoặc mở G3/test.'
template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
def block(h):return re.search(r'```text\n(.*?)\n```',template.split(h,1)[1],re.S).group(1)
def prompt(task):
 common=block('## Prompt chung');values=[task+' và results/'+task+'/runs/doi-chieu-smtp-001/','soát kết quả','P5, chuẩn bị G3','Codex người làm; Claude phản biện kết quả',
  'AGENTS.md; SPEC/LOG của T036–T039; docs/MRP.md, WHY.md, DECISIONS.md; results/T-038/runs/cap-nhat-goi-smtp-001/package/plan.json; results/T-036/runs/doi-chieu-smtp-001/authorization.json',
  'Liệt kê các bản REVIEW của từng task được Minh cho phép khi đọc thư mục; không có bản phản biện chính thức riêng của lượt triển khai V2',
  'src/do_thi_tinh/; results/T-036/runs/doi-chieu-smtp-001/manifest.json; results/'+task+'/manifest.json và runs/doi-chieu-smtp-001/{pin.json,checks,diff.json}; Windows Python3.12, -X utf8 -B; môi trường D:/RCA-ext/envs/py312-pin/Scripts/python.exe cho checker có pandas',
  'chỉ đọc và trả lời trong chat; chưa được Minh cho ghi REVIEW hoặc sửa file trong lượt phản biện này']
 matches=list(re.finditer(r'<[^>]+>',common));assert len(matches)==len(values)
 for m,v in reversed(list(zip(matches,values))):common=common[:m.start()]+v+common[m.end():]
 return common+'\n\n'+block('### Soát kết quả')+'\n\n'+block('### G3 —')+'\n'
costs={t:(dict(elapsed_seconds=res[t]['seconds'],peak_process_rss_bytes=res[t]['peak_working_set_bytes'])) if t=='T-037' else load(dirs[t]/('checks/full1069-002/cost.json' if t=='T-038' else 'checks/full132-001/cost.json')) for t in dirs}
for t,d in dirs.items():
 base=ROOT/'results'/t
 detail=('1598/1598 kiểm full model/fixture; graph/binding/signal/nguồn giữ nguyên. Unknown SMTP + trace thiếu channel đổi endpoint numerator1→0 đúng oracle trước chạy.' if t=='T-037' else '1069/1069graph; baseline R1 và comparator-only bằng nguyên output cũ; delta SMTP tách riêng, endpoints thêm1S/static-only và typed thêm1unknown exclusion, trace/giao giữ nguyên.' if t=='T-038' else '132/132graph; R1 replay và V2 đều bằng nguyên output cũ gồm tập/members/loại trừ/mẫu số; source/mapping/model giữ nguyên.')
 report='# Bàn giao '+t+' — tiếp nhận SMTP V2\n\nMinh duyệt triển khai gói theo Q-164 ngày16/10/2026; code/pin chung đã tiếp nhận sau đủ kiểm ba nhánh. Chờ Claude phản biện kết quả; chưa tự nghiệm thu.\n\n'+detail+'\n\nPin hiện hành là pin.json trong runs/doi-chieu-smtp-001/, manifest chung results/T-036/runs/doi-chieu-smtp-001/manifest.json. Loader kiểm exact path/SHA/created_utc và code live+snapshot; không HEAD/fallback R1. Mọi kết quả cũ, script/oracle/snapshot lịch sử giữ nguyên. Root report/model/index được giữ byte trước ở before/; không gán pin mới cho output cũ. Kế hoạch V2 ban đầu và các báo cáo “chờ duyệt” trước lượt này là tài liệu lịch sử; trạng thái hiện hành theo manifest và bàn giao này.\n\n'+limits+'\n\nBằng chứng: checks/ trong run, diff.json và manifest; báo cáo chung tại results/T-036/runs/doi-chieu-smtp-001/ban-giao.md. Chi phí thực theo cost.json trong run; không là benchmark cô lập, không suy từ thời gian tổng thành giờ công. Không tải nguồn/SMTP thật/test/heldout/commit/push. T040/P6/P9 nhận thêm semantics protocol đã ghi; telemetry channel cần nguồn riêng, không suy từ static.\n\nBước tiếp: Minh chuyển prompt-claude.txt để Claude soát độc lập nếu muốn. Không tự gửi; chỉ Minh nghiệm thu/đóng task.\n'
 text(base/'ban-giao.md',report);text(d/'ban-giao.md',report);save(d/'cost.json',costs[t])
 pr=prompt(t);text(base/'prompt-claude.txt',pr);text(d/'prompt-claude.txt',pr)
 oldcheck=(d/f'before/results/{t}/kiem-dung-dan.md').read_text(encoding='utf-8-sig')
 text(base/'kiem-dung-dan.md','# Tự kiểm hiện hành theo pin SMTP V2\n\n'+detail+'\n\nKiểm chung221R1 +100SMTPbaseline +29V2; toàn1598FT/1069TT/132OB đạt trước chuyển. Từng tập/members/loại trừ/mẫu số, hash/input/lặp/đảo và builder/projection có bằng chứng trong run mới. Giữ mọi lượt lỗi điều phối và phép kiểm, không đổi đáp án để PASS. '+limits+'\n\n## Báo cáo trước chuyển giữ làm lịch sử\n\n'+oldcheck)
 if t=='T-038':
  p=base/'kha-thi.json';v=load(d/'before/results/T-038/kha-thi.json')
  v['status']='SMTP_V2_APPLIED_ALL_THREE_BRANCHES_PASS_AWAITING_REVIEW'
  v['SMTP_V2_implementation']={'status':'APPLIED_COMMON_PIN_ALL_BRANCHES_PASS','cost':costs[t],'network_bytes':0,'measured_process_not_isolated':True,'historical_estimate':{'minutes':37,'output_bytes':600000000},'pin_file':rel(d/'pin.json')}
  v['SMTP_current_state']={'T037_SMTP_representation_implemented':True,'T037_full_model_exists':True,'T039_full_comparator_exists':True,'T038_active_model_SMTP_adopted':True,'proposed_comparator_change_applied':True,'common_pin_converged':True}
  save(p,v)

for t in ['T-036','T-037','T-038','T-039']:
 spec=next(ROOT/p for p in PLAN['proposed_writes']['permission_and_pin_documents'] if p.startswith('tasks/'+t) and p.endswith('/SPEC.md'))
 append(spec,'\n### Tiếp nhận V2 đã kiểm — 16/10/2026\n\nPhụ lục V2 ở trên đã được triển khai theo Q-164. Manifest chung: results/T-036/runs/doi-chieu-smtp-001/manifest.json; created_utc thực: '+pin['created_utc']+'. Đường dẫn/SHA/created_utc và module hashes chính xác nằm pin.json của cả T037/T038/T039 trong runs/doi-chieu-smtp-001/. Loader kiểm các giá trị này trước import. Cả ba đã đạt toàn hồi quy trước đổi bản hiện hành; kết quả cũ vẫn dùng pin đã sinh chúng. Các chữ OPEN/pending của phụ lục trước là mốc trước kiểm, metadata hiện hành theo pin.json và bàn giao, không suy nghiệm thu task/G3/test/commit.\n')
 if t=='T-036':pr=prompt(t)
 else:pr=(dirs[t]/'prompt-claude.txt').read_text(encoding='utf-8')
 log=Path(str(spec).replace('SPEC.md','LOG.md'))
 append(log,'\n### Kết thúc triển khai V2 trong cùng phiên — 16/10/2026 — Codex người làm\n\n1. Đã làm: áp đúng comparator/README, builder T037 không đổi; ghi quyết định/lý do trước dùng, chạy đủ221R1/100SMTPbaseline/29V2/1598FT/1069TT/132OB, rồi tiếp nhận chung cả ba. ỞTT, tách comparator khỏi delta; thêm đúng1key endpoints phía static và1typed unknown exclusion, T/giao giữ nguyên; ởOB toàn output bằng cũ; FT unknown SMTP không khớp trace thiếu channel theo oracle mới.\n2. File đổi: đúng plan.json V2: shared compare/README, bốn SPEC/LOG chỉ nối, WHY/DECISIONS chỉ nối, bốn dòng STATE, các bản hiện hành ba nhánh liệt kê và bốn run mới. before giữ mọi byte trước sửa; giữ mọi output/script/fixture/run cũ, kể cả lỗi điều phối. Không sửa nguồn/raw/T035/data khóa hoặc commit/push.\n3. Kiểm: full models, source/hash/pin, oracle/independent edges/projection/entity-only/shared signal; mọi graph so tập/members/loại trừ/mẫu số/interval, lặp/đảo/input bất biến. Kết quả chi tiết ở checks/, diff.json, completion.json và final-verification.json của gói chung; manifest finalized sau assertion. Chi phí thực per-process nằm cost.json từng run; tổng bytes gồm mọi lượt được thống kê chung, không là giờ công hay benchmark cô lập. Lượt TTfull1069-001 đã giữ failure: checker ban đầu đòi typed exclusion bằng nhau sau thêm unknown SMTP; đã sửa đúng kiểm phân hoạch theo oracle, không đổi model/comparator/đáp án đủ điều kiện. Các lỗi adapter cũ giữ trong preparation-attempts.json.\n4. Điều chưa chắc/cần Minh quyết: triển khai V2 và tiếp nhận kỹ thuật đã đạt, chờ phản biện và Minh nghiệm thu riêng. '+limits+' Không lấy match/mismatch hoặc synthetic làm bằng chứng nguyên nhân runtime. Phân xử cần build/image/instrumentation/deployment/trace channel có nguồn từ chủ dữ liệu qua Minh; P9 muốn authority/TLS cần schema/telemetry riêng.\n\nBước tiếp chính xác: đọc results/T-036/runs/doi-chieu-smtp-001/ban-giao.md và final-verification.json; Minh chuyển prompt dưới đây cho Claude nếu chọn, chưa cấp quyền ghi REVIEW. Lệnh cuối: `py -3 -X utf8 -B results/T-036/runs/doi-chieu-smtp-001/complete_adoption.py`. Không có tiến trình cần chờ sau hoàn tất.\nCommit đề nghị khi Minh cho phép riêng: `P5b: áp dụng đối chiếu SMTP V2 và tiếp nhận pin chung FT TT OB`.\n\nPrompt trung tính để Minh chuyển thủ công:\n```text\n'+pr+'\n```\n')
append(ROOT/'docs/WHY.md','\n**Bằng chứng triển khai V2 sau lựa chọn đã duyệt:** toàn hồi quy và ba nhánh đã được chạy trong cùng phiên; xem results/T-036/runs/doi-chieu-smtp-001/completion.json và final-verification.json. Comparator-only TT/OB giữ nguyên kết quả cũ; TT thêm SMTP có đúng phần thay theo oracle, FT thiếu channel tách khỏi SMTP. Đây xác nhận hợp đồng/tiếp nhận trong miền dữ liệu đã kiểm, không là lợi ích RCA hoặc runtime proof. Giữ mọi OPEN nêu trong lý do và bàn giao.\n')

# Update only the four authorized STATE rows under exclusive lock.
state=ROOT/'docs/STATE.md'
with state.open('r+b') as f:
 msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
 try:
  raw=f.read();s=raw.decode('utf-8-sig');ls=s.splitlines(keepends=True)
  for t in ['T-036','T-037','T-038','T-039']:
   i=next(i for i,x in enumerate(ls) if x.startswith('| '+t+' |'));cells=ls[i].split('|')
   if t=='T-036':status=' Gốc đã đóng15/10 theo Q-158; gói kỹ thuật SMTP V2 Minh duyệt Q-164 đã triển khai/kiểm16/10. Chung221R1/100SMTPbaseline/29V2 đạt; FT1598/TT1069/OB132 đã tiếp nhận cùng manifest mới. Bàn giao results/T-036/runs/doi-chieu-smtp-001/. Chờ phản biện sửa, chưa tự nghiệm thu sửa/G3 hoặc commit/push. '
   elif t=='T-037':status=' SMTP V2 đã tiếp nhận16/10 theo Q-164; toàn1598fullmodel/fixture đạt, builder/model giữ nguyên; comparator tách SMTP khỏi trace thiếu channel. Cùng pin T036 run doi-chieu-smtp-001 với TT/OB sau đủ hồi quy. Chờ Claude phản biện kết quả, chưa nghiệm thu; runtime/queue/scope/RQ3/RQ5/G3 OPEN. Bàn giao/prompt results/T-037/ và LOG hiện hành. '
   elif t=='T-038':status=' SMTP V2 đã triển khai16/10 theo Q-164: thêm relation có nguồn, kiểm đủ1069graph; replay R1/comparator-only bằng cũ, delta endpoints +1static-only và typed +1unknown exclusion, trace/giao giữ nguyên. Đã tiếp nhận pin chung sau FT/OB đạt; giữ output cũ. Chờ Claude phản biện kết quả, chưa nghiệm thu/P6/G3/test. Lineage/runtime OPEN. Bàn giao/prompt results/T-038/ và LOG hiện hành. '
   else:status=' SMTP V2 đã tiếp nhận16/10 theo Q-164: full132graph replay R1/V2 bằng nguyên output cũ; model/mapping/source giữ nguyên. Cùng pin mới với FT/TT sau toàn kiểm đạt, legacy snapshot/runner giữ lịch sử. Chờ Claude phản biện kết quả; inventory toàn deployment/runtime/Node/alias OPEN, chưa nghiệm thu/P6/G3/test. Bàn giao/prompt results/T-039/ và LOG hiện hành. '
   cells[6]=status;ls[i]='|'.join(cells)
  result=''.join(ls).encode('utf-8');result=(b'\xef\xbb\xbf'+result) if raw.startswith(b'\xef\xbb\xbf') else result
  f.seek(0);f.write(result);f.truncate();f.flush()
 finally:f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)

# Common final handoff and verification before root manifest publication.
completion={'status':'IMPLEMENTED_ALL_THREE_ADOPTED_AWAITING_REVIEW_NOT_ACCEPTED','pin':pin,'checks':{'T036_R1':221,'historical_SMTP':100,'V2_SMTP':29,'T037':1598,'T038':1069,'T039':132},'results':{t:rel(p) for t,p in checks.items()},'costs':costs,'all_old_outputs_retained':True,'tests_heldout_opened':False,'commit_push':False,'limits':limits}
save(RUN/'completion.json',completion)
text(RUN/'ban-giao.md','# SMTP V2 đã triển khai và kiểm đủ ba nhánh\n\nMinh duyệt Q-164. Shared221R1/100SMTPbaseline/29V2, FT1598, TT1069, OB132 đều đạt. Cả ba dùng cùng pin.json, manifest/code chung cố định trong run này; completion.json lưu pointer kết quả và số thực. Kết quả hiện hành mới chuyển sau đủ ba nhánh. Snapshot/hợp đồng/manifest T036 gốc và mọi output cũ giữ nguyên.\n\nTT comparator-only khớp toàn kết quả cũ; delta thêm một cạnh SMTP mỗi mức, một key S/static-only endpoints và một unknown exclusion typed mỗi graph. Không đổi trace/mapping/giao hoặc đủ điều kiện typed. OB bằng nguyên toàn132output cũ. FT source/model không đổi; unknown SMTP với trace thiếu channel endpoint numerator1→0 đúng oracle.\n\n'+limits+'\n\nCác lượt lỗi adapter/TTchecker giữ nguyên trong checks/ và preparation-attempts.json; không thay shared hoặc oracle để PASS. Báo cáo số thực theo cost.json từng nhánh và completion.json, không benchmark cô lập hoặc suy giờ công. Không tải thêm, khôngSMTPnetwork/test/commit/push. Chờ Claude soát và Minh nghiệm thu riêng. Prompt chuẩn ở prompt-claude.txt để Minh chuyển thủ công.\n')
text(RUN/'prompt-claude.txt',prompt('T-036'))
changed=[p for p,v in oldhash.items() if sha(ROOT/p)!=v['sha256']]
assert set(changed)<=allowed,set(changed)-allowed
appendonly=[p for p in PLAN['proposed_writes']['permission_and_pin_documents'] if p!='docs/STATE.md']
for p in appendonly:assert (ROOT/p).read_bytes().startswith((RUN/'before'/p).read_bytes()),p
def without_rows(s):return ''.join(x for x in s.splitlines(keepends=True) if not any(x.startswith('| '+t+' |') for t in ['T-036','T-037','T-038','T-039']))
assert without_rows((RUN/'before/docs/STATE.md').read_text(encoding='utf-8-sig'))==without_rows(state.read_text(encoding='utf-8-sig'))
assert sha(ROOT/'results/T-036/manifest.json')==oldhash['results/T-036/manifest.json']['sha256']
assert sha(ROOT/'src/do_thi_tinh/build.py')==oldhash['src/do_thi_tinh/build.py']['sha256']
for t,d in dirs.items():
 assert load(d/'pin.json')==pin
 pr=(d/'prompt-claude.txt').read_text(encoding='utf-8');assert block('### Soát kết quả') in pr and block('### G3 —') in pr and block('## Prompt chung').split('Không sửa ngoài phạm vi trên')[1] in pr
for p in list(RUN.glob('*.py'))+[q for d in dirs.values() for q in d.glob('*.py')]:ast.parse(p.read_text(encoding='utf-8-sig'))
verification={'all_ok':True,'phase':'before root manifests publication','changed_existing_files':changed,'all_preexisting_paths_checked':len(oldhash),'append_only_verified':appendonly,'STATE_only_T036_T039_rows':True,'historical_outputs_unchanged_except_exact_approved_current_views':True,'builder_byte_unchanged':True,'three_pins_equal':True,'complete_results':completion['checks'],'full_diff_scope_verified':True}
save(RUN/'final-verification.json',verification)
for t,d in dirs.items():
 base=ROOT/'results'/t;old=load(d/f'before/results/{t}/manifest.json');m=copy.deepcopy(old)
 m['created_utc']=datetime.now(timezone.utc).isoformat();m['current_run']='runs/doi-chieu-smtp-001';m['common_pin']=pin
 m['status']='SMTP_V2_ALL_BRANCHES_ADOPTED_AWAITING_CLAUDE_REVIEW_NOT_ACCEPTED';m['state']=m['status'];m['task_accepted']=False
 m['historical_manifest_before_V2']=rel(d/f'before/results/{t}/manifest.json');m['validation']=rel(RUN/'final-verification.json');m['current_handoff']='ban-giao.md';m['current_prompt']='prompt-claude.txt'
 m['log_sha256']=sha(next(ROOT/p for p in PLAN['proposed_writes']['permission_and_pin_documents'] if p.startswith('tasks/'+t) and p.endswith('/LOG.md')))
 m['state_'+t.replace('-','')+'_row']=next(x for x in state.read_text(encoding='utf-8-sig').splitlines() if x.startswith('| '+t+' |'))
 if t=='T-037':
  m['historical_base_contract']=m['base_contract'];m['base_contract']=pin;m['historical_approved_addendum']=m['approved_addendum'];m['approved_addendum']=rel(RUN/'hop-dong.md');m['actual_code_snapshot']=rel(RUN/'code');m['actual_shared_code']={'src/do_thi_tinh/'+n:h for n,h in pin['code_hashes'].items()};m['sibling_pins_changed']=True;m['authorization']=rel(d/'authorization.json');m['stats']=res[t]['stats']
 elif t=='T-038':
  m['current_model']='runs/doi-chieu-smtp-001';m['historical_shared_T036_pin']=m['shared_T036_pin'];m['shared_T036_pin']=pin
  m['current_completion_report']='runs/doi-chieu-smtp-001/ban-giao.md';m['current_completion_verification']=rel(RUN/'final-verification.json');m['current_completion_run']='runs/doi-chieu-smtp-001'
  m['SMTP_proposal_state']={'T037_SMTP_builder_implemented':True,'T039_comparer_implemented':True,'comparator_change_applied':True,'T038_SMTP_relation_adopted':True,'common_pin_converged':True};m['current_SMTP_implementation']=rel(RUN/'completion.json');m['last_external_LOG_sha256']=m['log_sha256'];m['last_external_STATE_sha256']=sha(state)
 else:
  m['historical_pin']=m['pin'];m['pin']=pin;m['shared_pin_changed']=True;m['shared_code_used']='exact SMTP V2 manifest snapshot, validated live+snapshot; old direct-R1 runner unchanged history';m['finalization_run']='runs/doi-chieu-smtp-001'
 # Every run has an independent index of its files; the pin SHA remains stable.
 runfiles=[{'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(d.rglob('*')) if p.is_file() and p.name!='manifest.json']
 save(d/'manifest.json',dict(task=t,pin=pin,all_pass=True,files=runfiles))
 oldrows={r['path']:r for r in old['files']}
 files=[dict(oldrows.get(rel(p),{}),path=rel(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(base.rglob('*')) if p.is_file() and p!=base/'manifest.json']
 m['files']=files;m['file_count']=len(files);m['count']=len(files);m['total_payload_bytes_excluding_manifest']=sum(r['bytes'] for r in files);m['total_artifact_bytes_excluding_manifest']=m['total_payload_bytes_excluding_manifest'];m['total_payload_bytes']=m['total_payload_bytes_excluding_manifest']
 if t=='T-037':
  m['historical_output_accounting']={k:old[k] for k in ['total_output_bytes','file_count_including_manifest_and_final_report','payload_excludes'] if k in old}
  m.pop('total_output_bytes',None);m['file_count_including_manifest_and_final_report']=len(files)+1;m['payload_excludes']='Root manifest self only; every retained file under this task is included.'
 save(base/'manifest.json',m)
 for row in files:assert sha(ROOT/row['path'])==row['sha256']
# Record measured processing separately from preparation/labor and exact retained scope.
shared_costs={
 'T036_R1_seconds':load(RUN/'checks/t036-r1-001/result.json')['seconds'],
 'SMTP_baseline_including_its_child_R1_seconds':load(RUN/'checks/smtp-baseline-002/result.json')['seconds'],
 'V2_literal_seconds':load(RUN/'checks-smtp-v2-001/checks.json')['elapsed_seconds']}
costpaths=[RUN]+list(dirs.values())
save(RUN/'cost.json',{'shared_recorded_durations':shared_costs,'branch_costs':costs,
 'recorded_elapsed_sum_lower_bound_seconds':sum(shared_costs.values())+sum(v['elapsed_seconds'] for v in costs.values()),
 'condition':'Sum of measured distinct process/run intervals; excludes script preparation, reporting, unmeasured early adapter failures, waiting and labor. Not an isolated benchmark.',
 'retained_new_run_bytes_before_this_cost_and_common_artifact_manifest':{rel(d):sum(p.stat().st_size for p in d.rglob('*') if p.is_file()) for d in costpaths},
 'bytes_scope':'All retained attempts/before/snapshots/intermediates/new outputs in four approved run directories; logical bytes, excludes filesystem allocation metadata and subsequent index size.',
 'network_bytes':0,'new_download_bytes':0,'estimated_budget_historical_only':{'machine_minutes':37,'output_bytes_approx':600000000},'labor_hours':None,'other_unmeasured_costs':'OPEN, not silently zero'})
# Immutable common pin deliberately excludes later operational reports; index them separately.
save(RUN/'artifact-manifest.json',dict(immutable_pin_manifest_sha256=sha(RUN/'manifest.json'),files=[{'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(RUN.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
assert all(load(ROOT/f'results/{t}/manifest.json')['common_pin']==pin for t in dirs)
print(json.dumps({'all_ok':True,'checks':completion['checks'],'pins_converged':True,'old_outputs_preserved':True,'changed_existing_files':len(changed)},ensure_ascii=False))
