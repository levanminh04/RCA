"""Verify the proposal revision and publish T038 metadata only."""
from pathlib import Path
import ast, difflib, hashlib, json, re, time, msvcrt
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
PKG=RUN/'package'
OUT=ROOT/'results/T-038'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return Path(p).relative_to(ROOT).as_posix()

started=time.perf_counter()
checks=[]
def check(name,ok):
    checks.append({'name':name,'ok':bool(ok)})
    if not ok:raise AssertionError(name)

# T038 root manifest necessarily changes when this proposal is indexed. Its input
# baseline is the exact archived manifest, not the new root manifest's own hash.
state_inputs=load(PKG/'input-state.json')
state_inputs['T-038']['original_path']='results/T-038/manifest.json'
state_inputs['T-038']['path']=rel(RUN/'before-manifest.json')
state_inputs['T-038']['validation_rule']='Verify archived baseline hash; current root must retain model005/comparison002 and R1 pin. Package/document metadata may change during this approved update.'
save(PKG/'input-state.json',state_inputs)

# Correct a global-looking historical field: builder SMTP is now implemented elsewhere.
p=OUT/'hoan-tat-trong-quyen.json'
d=load(p)
d.pop('shared_SMTP_fix_applied',None)
d['proposed_comparator_change_applied']=False
d['common_pin_converged']=False
d['criteria'][1]['status']='AWAITING_T038_SMTP_ADOPTION_AND_V2_COMPARATOR_COMMON_PIN_APPROVAL'
save(p,d)

baseline=load(RUN/'baseline.json')
excepted={'tasks/T-038-p5b-trainticket/LOG.md','docs/STATE.md'}
protected=[(p,v) for p,v in baseline.items() if p not in excepted]
check('protected source/shared/other task baseline unchanged',all((ROOT/p).is_file() and sha(ROOT/p)==v['sha256'] for p,v in protected))
old=load(RUN/'before-manifest.json')
allowed={'goi-sua-SMTP.md','ban-giao.md','hoan-tat-trong-quyen.md','hoan-tat-trong-quyen.json','de-nghi-tiep-theo.md','kha-thi.json','LICH-SU.md','prompt-claude-smtp.txt',
         'runs/hoan-tat-trong-quyen-001/smtp/plan.md','runs/hoan-tat-trong-quyen-001/smtp/plan.json',
         'runs/hoan-tat-trong-quyen-001/smtp/package-manifest.json','runs/hoan-tat-trong-quyen-001/smtp/package-verification.json'}
allowed={'results/T-038/'+p for p in allowed}
changed=[]
for row in old['files']:
    p=ROOT/row['path']
    check('historical path exists:'+row['path'],p.is_file())
    if sha(p)!=row['sha256']:changed.append(row['path'])
check('only authorized derived proposal files changed',set(changed)<=allowed)
check('T038 model/comparisons/source analysis are byte unchanged',all(x in allowed for x in changed))

# V1 package preserved byte-for-byte against the original root manifest.
prefix='results/T-038/runs/hoan-tat-trong-quyen-001/smtp/'
prior=[r for r in old['files'] if r['path'].startswith(prefix)]
check('original whole V1 package preserved',all(sha(RUN/'before/package-v1'/r['path'][len(prefix):])==r['sha256'] for r in prior))
check('T037/T039 real full-model preview 29 passed',load(PKG/'kiem-preview-001/checks.json')['all_ok'] and len(load(PKG/'kiem-preview-001/checks.json')['checks'])==29)
hashes=load(PKG/'candidate-code-hashes.json')
check('builder/init reused unchanged; only comparator proposed',all(sha(ROOT/r['source'])==r['base_sha256'] and sha(PKG/'experimental_copy'/Path(r['source']).name)==r['candidate_sha256'] and r['changed']==(Path(r['source']).name=='compare.py') for r in hashes))
patch=(PKG/'proposed-shared-code.patch').read_text(encoding='utf-8')
expected=''.join(difflib.unified_diff((ROOT/'src/do_thi_tinh/compare.py').read_text(encoding='utf-8').splitlines(True),
    (PKG/'experimental_copy/compare.py').read_text(encoding='utf-8').splitlines(True),fromfile='a/src/do_thi_tinh/compare.py',tofile='b/src/do_thi_tinh/compare.py'))
check('exact patch against current comparator',patch==expected)
for p in PKG.rglob('*.json'):load(p)
for p in RUN.rglob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
check('new package JSON and all new-run Python AST',True)
plan=load(PKG/'plan.json')
check('full actual replay scopes 1069/132 plus T037',plan['regression']['T038']==1069 and plan['regression']['T039']==132 and 'full' in plan['regression']['T037'])
check('proposed run paths unoccupied',all(not (ROOT/p).exists() for p in plan['proposed_writes']['new_run_output_scopes']))
docs=load(PKG/'docs-before-after.json')
for d in docs['replacements']:
    if 'before_sha256' in d:check('exact document before hash:'+d['path'],sha(ROOT/d['path'])==d['before_sha256'])
prompt=(OUT/'prompt-claude-smtp.txt').read_text(encoding='utf-8-sig')
template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
def block(heading):
    section=template.split(heading,1)[1]
    return re.search(r'```text\n(.*?)\n```',section,re.S).group(1)
common=block('## Prompt chung')
# Everything after the last information placeholder must be exact, untouched.
tail=common.split('<quyền',1)[-1] if '<quyền' in common else common
fixed=common[common.index('Không sửa ngoài phạm vi trên'):]
check('handoff verbatim common fixed block',fixed in prompt)
check('handoff verbatim Soat SPEC and G3 blocks',block('### Soát SPEC') in prompt and block('### G3 —') in prompt)
check('handoff points current V2', 'runs/cap-nhat-goi-smtp-001/package' in prompt and 'runs/hoan-tat-trong-quyen-001/smtp' not in prompt)

log=ROOT/'tasks/T-038-p5b-trainticket/LOG.md'
beforelog=(RUN/'LOG-before.md').read_bytes()
check('LOG append only before report',log.read_bytes().startswith(beforelog))
report='''
### Kết thúc cập nhật gói SMTP V2 — 16/10/2026 — Codex người làm

1. Đã làm: đối chiếu source/code/manifest hiện tại và cập nhật trọn gói duyệt. FACT: T037 đã hỗ trợ SMTP/full model theo delta Minh duyệt, T039 đã có comparer132graph dùng snapshot gốc. Đề xuất V2 đổi comparator (cả endpoints) và common pin; builder giữ nguyên T037. Dự kiến hồi quy đủ T037/fullfixture,1069TT,132OB; dự trù37phút máy/600MB chưa đo. Giữ V1 nguyên byte và sửa điểm vào cũ dẫn V2. Chưa có quyết định khoa học hoặc áp dụng mới.
2. File đổi: trong results/T-038 chỉ package V2, plan.md/json và metadata đánh dấu V1 lịch sử, goi-sua-SMTP, bàn giao/hoàn tất/đề nghị/khả thi/lịch sử/prompt/manifest. Nối LOG này và chỉ dòng T038 STATE. Không sửa shared, các SPEC, WHY/DECISIONS hay đầu ra T036/T037/T039; không commit/push.
3. Kiểm:29/29 preview đạt (oracle trước candidate, rebuild full mô hình T037/T039 và frozen TT, phản ví dụ đổi semantics). Kiểm hash toàn baseline trước dùng, kiểm bất biến protected source/other-task và mọi5324artifact T038 cũ ngoài đúng12file derived đã khai báo; model005,1069so và phân tích số không đổi. Kiểm patch chỉ comparator, builder hiện hành byte-identical; JSON/AST, bản lưu V1 nguyên byte, draft before hash, prompt nguyên mẫu và full replay scopes. Chi tiết máy đọc tại runs/cap-nhat-goi-smtp-001/verification.json và package/package-verification.json; manifest chỉ finalize sau các assertion đạt.
4. Chưa chắc/cần Minh quyết: gói V2 chưa áp dụng; preview không là1069/132replay hay adoption. Chọn comparator theo protocol hoặc giữ so cấu trúc hiện tại và việc chuyển cả ba pin cần Minh duyệt gói cụ thể. T038 thiếu relation SMTP trong model hiện hành; các runtime/source/authority/TLS/delivery OPEN vẫn giữ, chưa trả lời lợi ích RCA/RQ3/RQ5/G3. Cần provenance build/image/instrumentation/deployment/trace channel để phân xử runtime. Không lấy task đủ file thay bằng chứng ấy. Đề nghị bàn giao gói cho Claude đọc độc lập nếu Minh chọn, chưa tự gửi hay cấp quyền REVIEW.

Nguồn quyết định trong phiên: Minh yêu cầu cập nhật gói SMTP theo trạng thái mới trước duyệt; quyền này chỉ cập nhật hồ sơ T038. Dự thảo ghi DECISIONS/WHY về lựa chọn common pin nằm trong docs-before-after.json, chưa ghi nguồn chính thức khi chưa có lời duyệt áp dụng.
Bước tiếp chính xác: Minh đọc results/T-038/runs/cap-nhat-goi-smtp-001/package/plan.md, plan.json, docs-before-after.json và patch. Nếu duyệt áp dụng V2, trước mutation kiểm lại input-state.json trên source thật và giữ nguyên các pin lịch sử, rồi thực hiện theo hồi quy/phạm vi đã duyệt. Không gọi engine.py cũ để nhập live như R1. Không có tiến trình cần chờ.
Lệnh cuối lượt: `py -3 -X utf8 -B results/T-038/runs/cap-nhat-goi-smtp-001/finalize_update.py`.
Đề nghị commit sau khi Minh cho phép riêng: `T-038: cập nhật gói đối chiếu SMTP và hợp nhất phiên bản theo trạng thái hiện hành`.

Prompt bàn giao trung tính để Minh chuyển thủ công (chưa có quyền ghi REVIEW):
```text
'''+prompt+'\n```\n'
if '### Kết thúc cập nhật gói SMTP V2' not in log.read_text(encoding='utf-8-sig'):
    with log.open('a',encoding='utf-8') as f:f.write(report)

# Sequential exclusive lock on the actual STATE file, reading the latest bytes.
state=ROOT/'docs/STATE.md'
with state.open('r+b') as f:
    msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
    try:
        data=f.read(); text=data.decode('utf-8-sig');lines=text.splitlines(keepends=True)
        matches=[i for i,s in enumerate(lines) if s.startswith('| T-038 |')]
        check('one current T038 row',len(matches)==1)
        i=matches[0];cells=lines[i].split('|')
        cells[6]=' Hoàn tất phần T038 trong quyền; gói SMTP V2 cập nhật16/10/2026 chờ Minh duyệt, chưa nghiệm thu toàn task. T037 đã hỗ trợ SMTP/full model; T039 đã đối chiếu132graph. V2 đề xuất đổi comparator và common pin, giữ builder T037, hồi quy full T037/1069TT/132OB; preview29đạt. Model005/1069so T038 và pin gốc không đổi; lineage/runtime OPEN, không chọn P6/mở test. Plan/filelist/diff/chi phí ở results/T-038/runs/cap-nhat-goi-smtp-001/package/; bàn giao/prompt và LOG hiện hành. '
        lines[i]='|'.join(cells)
        updated=''.join(lines).encode('utf-8')
        if data.startswith(b'\xef\xbb\xbf'):updated=b'\xef\xbb\xbf'+updated
        f.seek(0);f.write(updated);f.truncate();f.flush()
    finally:
        f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)
oldstate=(RUN/'STATE-before.md').read_text(encoding='utf-8-sig')
newstate=state.read_text(encoding='utf-8-sig')
striprow=lambda s:''.join(x for x in s.splitlines(keepends=True) if not x.startswith('| T-038 |'))
check('STATE only T038 row changed',striprow(oldstate)==striprow(newstate))
check('LOG remains append only',log.read_bytes().startswith(beforelog))

summary={'all_ok':True,'created_utc':datetime.now(timezone.utc).isoformat(),'protected_file_count':len(protected),'old_T038_file_count':len(old['files']),
    'changed_existing_T038_files':changed,'preserved_V1_files':len(prior),'preview_checks':29,
    'not_run':['full comparator replay1069/132','common pin adoption','real SMTP/network'],
    'elapsed_seconds':time.perf_counter()-started,'checks':checks}
save(RUN/'verification.json',summary)
save(PKG/'package-verification.json',{k:v for k,v in summary.items() if k!='checks'})
save(PKG/'package-manifest.json',{'status':'V2_CURRENT_APPROVAL_PACKAGE_ONLY','files':[{'path':p.relative_to(PKG).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
    for p in sorted(PKG.rglob('*')) if p.is_file() and p.name!='package-manifest.json']})

# Preserve all existing root-manifest metadata; the actual model and comparator pin stay R1.
m=load(RUN/'before-manifest.json')
m['created_utc']=datetime.now(timezone.utc).isoformat()
m['status']='T038 authorized outputs unchanged; V2 comparator/common-version proposal updated; not applied or accepted'
m['previous_manifest_before_SMTP_V2']='runs/cap-nhat-goi-smtp-001/before-manifest.json'
m['current_SMTP_proposal']='runs/cap-nhat-goi-smtp-001/package/plan.md'
m['current_SMTP_proposal_verification']='runs/cap-nhat-goi-smtp-001/verification.json'
m['last_external_LOG_sha256']=sha(log)
m['last_external_STATE_sha256']=sha(state)
m['excludes']='manifest self; external LOG/STATE verified in current SMTP proposal verification'
m['SMTP_proposal_state']={'T037_SMTP_builder_implemented':True,'T039_comparer_implemented':True,'preview_checks':29,'comparator_change_applied':False,'common_pin_converged':False}
previous={r['path']:r for r in old['files']}
files=[]
for p in sorted(OUT.rglob('*')):
    if not p.is_file() or p==OUT/'manifest.json':continue
    r=dict(previous.get(rel(p),{}));r.update(path=rel(p),bytes=p.stat().st_size,sha256=sha(p))
    if 'validation' not in r:r['validation']='proposal-update-artifact; source/sample copies hash only'
    files.append(r)
m['files']=files;m['file_count']=len(files);m['total_artifact_bytes_excluding_manifest']=sum(r['bytes'] for r in files)
save(OUT/'manifest.json',m)
check('published root manifest hashes exact',all(sha(ROOT/r['path'])==r['sha256'] for r in m['files']))
print(json.dumps({'all_ok':True,'checks':len(checks),'protected_files':len(protected),'changed_existing_files':changed,'manifest_files':len(files),'preview_checks':29},ensure_ascii=False))
