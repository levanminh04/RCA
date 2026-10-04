"""Verify the full handoff and refresh its exhaustive, final file manifest."""
import csv,hashlib,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[3];OUT=ROOT/'results/T-015';TASK=ROOT/'tasks/T-015-ho-so-microrank'
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
scientific=j(OUT/'runs/final-scientific-audit.json');assert scientific['all_passed']
reference=j(OUT/'runs/ob-reference-audit/summary.json');assert reference['all_passed'] and len(reference['cases'])==90
assert reference['baseline_ranker_not_rerun']
required=['ho-so-microrank.md','ho-so-phat-hien-trace.md','tracerca-rcaeval.md','vi-du-tinh-tay.md','yeu-cau-dau-vao.csv','ca-da-chay.csv','dinh-chinh-task-cu.md','de-xuat-tai-lieu-chung.md','bao-cao-cuoi.md','tieu-chi-xong.csv','manifest-ban-giao.json']
assert all((OUT/p).is_file() and (OUT/p).stat().st_size for p in required)
log=(TASK/'LOG.md').read_text(encoding='utf-8-sig')
assert 'Minh ủy quyền tự duyệt SPEC theo prompt Đợt 1 ngày 04/10/2026' in log
assert '<task>' in log and '</task>' in log
for section in ['A. Đã làm','B. File đã thay đổi','C. Kiểm tra đã chạy','D. VẤN ĐỀ Ở TASK CŨ','E. Chỗ lệch khỏi SPEC','F. Đề xuất cho tài liệu chung','G. Phần chưa kiểm','H. Cần Minh quyết']:assert section in log and section in (OUT/'bao-cao-cuoi.md').read_text(encoding='utf-8')
template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
common=template.split('## Prompt chung',1)[1].split('```text',1)[1].split('```',1)[0].strip('\r\n')
g1=template.split('**G1 — phương pháp, dataset, cách chia:**',1)[1].split('```text',1)[1].split('```',1)[0].strip('\r\n')
prompt=log.split('## Prompt phản biện cho Claude — vai trò Minh đã đồng ý',1)[1].split('```text',1)[1].split('```',1)[0].strip('\r\n')
assert prompt.endswith('\n\n'+g1)
filled_common=prompt[:-len('\n\n'+g1)]
placeholder=re.search(r'các file đầu ra: (.*),\nvà kết quả',filled_common,re.S).group(1)
expected=common.replace('<T-xxx-tên>','T-015-ho-so-microrank').replace('<T-xxx>','T-015').replace('<danh sách>',placeholder).replace('<commit gốc>','93f13d4c4a966428177e2acc287d96bc89303e92')
assert filled_common==expected,'review prompt fixed text changed'
assert log.rstrip().endswith(g1+'\n```'),'review prompt must be the end of LOG'
state=(ROOT/'docs/STATE.md').read_text(encoding='utf-8-sig')
line=next(v for v in state.splitlines() if v.startswith('| T-015 |'))
assert '| chờ phản biện (04/10/2026) |' in line
last_state=json.loads((OUT/'runs/state-changes.jsonl').read_text(encoding='utf-8').splitlines()[-1])
assert last_state['outside_t015_bytes_identical'] and last_state['new_line']==line
json_checked=[]
for p in sorted(OUT.rglob('*.json')):
    # Historical failures and NaN audit artifacts are intentionally retained;
    # numeric validity is enforced separately on the selected valid outputs.
    v=j(p);json_checked.append(str(p.relative_to(ROOT)));del v
all_owned=[]
for folder in [OUT,ROOT/'src/microrank',TASK,pathlib.Path('D:/RCA-ext/work/T-015')]:
    for p in sorted(folder.rglob('*')):
        if p.is_file():all_owned.append(p)
checkfile=OUT/'runs/final-handoff-check.json'
result={'all_passed':True,'required_files':required,'scientific_audit_passed':True,'reference_slo_and_counts_exact_cases':90,
        'review_common_verbatim_except_neutral_placeholders':True,'G1_verbatim':True,'review_prompt_at_log_end':True,
        'state_row':line,'state_other_bytes_preserved_when_updated':True,'json_artifact_count':len(json_checked),
        'json_artifacts_checked':json_checked,'method_not_rerun':True,'outside_scope_not_mutated_by_this_script':True}
save(checkfile,result)
manifest_path=OUT/'manifest-ban-giao.json';manifest=j(manifest_path)
all_owned=sorted(set(all_owned+[checkfile]),key=lambda p:str(p))
entries=[]
for p in all_owned:
    if p==manifest_path:
        entries.append({'path':str(p.resolve()).replace('\\','/'),'host':'laptop','bytes':None,'sha256':None,'note':'Self manifest; no recursive hash'})
    else:entries.append({'path':str(p.resolve()).replace('\\','/'),'host':'laptop','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
manifest['local_files']=entries
manifest['mutable_files_hashed_before_final_handoff']=[]
manifest['all_local_files_hashed_after_log_and_state_finalized']=True
manifest['local_paths_exact']=True
save(manifest_path,manifest)
assert {e['path'] for e in manifest['local_files']}=={str(p.resolve()).replace('\\','/') for p in all_owned}
assert all(e['path'].startswith('/home/ubuntu/rca/T-015/') for e in manifest['remote_files'])
print(json.dumps({'status':'pass','local_files':len(entries),'remote_paths':len(manifest['remote_files']),'json_artifacts':len(json_checked),'review_template_exact':True,'state_only_T015_changed':True}))
