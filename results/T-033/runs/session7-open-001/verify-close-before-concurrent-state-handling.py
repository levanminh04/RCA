"""Complete interrupted document/hash close; no EC2, no scientific processing."""
import ast,datetime,difflib,hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parents[3];O=R/'results/T-033/runs/session7-open-001';C=R/'results/T-033/runs/session7-storage-checkpoint-001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,j):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(j,f,ensure_ascii=False,indent=2);f.write('\n')
baseline=read(O/'baseline.json');protected={};concurrent={}
for rel,m in baseline.items():
    if rel in ('docs/STATE.md','tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'):continue
    p=R/rel
    if sha(p)==m['sha256'] and p.stat().st_size==m['bytes']:protected[rel]=m;continue
    assert rel in ('docs/DECISIONS.md','docs/WHY.md'), rel
    before=R/'results/T-033/runs/session6-open-001/before'/rel
    assert sha(before)==m['sha256'] and p.read_bytes().startswith(before.read_bytes())
    delta=p.read_bytes()[len(before.read_bytes()):].decode('utf-8')
    assert 'T-032' in delta and 'T-033' not in delta
    concurrent[rel]={'status':'CONCURRENT_APPEND_FOR_T032_OUTSIDE_THIS_WRITER','before':m,
        'current':{'sha256':sha(p),'bytes':p.stat().st_size},'old_prefix_unchanged':True,
        'scope_affected':'No change to T-033 decisions or WHY-41','append_text':delta}
write(C/'concurrent-source-appends.json',concurrent)
for n in ('checkpoint-handoff-001','session6-compute-checkpoint-001'):
    base=R/'results/T-033/runs'/n;iv=read(base/'artifact-inventory.json');iv=iv.get('files',iv)
    for rel,m in iv.items():
        p=base/'artifacts'/rel;assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes'],rel
for name in ('points-lock.json','coverage-matching.json'):
    p=O/name;m=read(O/'lock-receive-verification.json')['files'][name]
    assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes']
for p in (R/'results/T-033/scripts').glob('*session7*.py'):ast.parse(p.read_text(encoding='utf-8'))
v2=R/'results/T-033/scripts/session7_extract_v2.py'
assert read(C/'draft-static-check-final.json')['sha256']==sha(v2)
log=R/'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md';log0=(O/'LOG.md.before').read_bytes()
assert log.read_bytes().startswith(log0)
state=R/'docs/STATE.md';state0=(O/'STATE.md.before').read_bytes()
old=state0.decode('utf-8').splitlines();new=state.read_text(encoding='utf-8').splitlines()
assert len(old)==len(new)
changed=[i for i,(a,b) in enumerate(zip(old,new)) if a!=b]
assert len(changed)==1 and old[changed[0]].startswith('| T-033 |')
with log.open('ab') as f:
    f.write(('\nBổ sung kiểm đóng phiên: lần finish_session7.py đã nối báo cáo và đổi đúng dòng T-033 STATE rồi dừng kiểm khi thấy DECISIONS/WHY khác baseline. Đọc phần thay đổi trực tiếp: chỉ nối Q-133–135 và WHY-45 cho T-032 trong lúc phiên chạy, prefix nguồn đầu phiên/T-033/WHY-41 giữ nguyên. Codex không ghi hai file này. Bằng chứng concurrent-source-appends.json; không có xung đột nguồn T-033 và không tự áp quyền T-032. Đã giữ bản static check trước/sau bổ sung validation của draft.\nLệnh chốt laptop cuối thay dòng trước: C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B -X utf8 results/T-033/scripts/verify_close_session7.py — metadata/hash/diff và chỉ nối LOG; không EC2 hay nghiên cứu. Bước tiếp và việc Minh cần quyết giữ theo README.\n').encode('utf-8'))
diff=[]
for rel,b in [('docs/STATE.md',state0),('tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md',log0)]:
    diff.extend(difflib.unified_diff(b.decode('utf-8').splitlines(keepends=True),(R/rel).read_text(encoding='utf-8').splitlines(keepends=True),fromfile='before/'+rel,tofile=rel))
(C/'approved-docs.diff').write_text(''.join(diff),encoding='utf-8',newline='\n')
write(C/'scope-verification.json',{'status':'PASS','LOG_append_only':True,'STATE_only_task_changed':'T-033',
    'STATE_changed_line_1based':changed[0]+1,'protected_docs_unchanged':protected,
    'concurrent_source_appends':list(concurrent),'concurrent_source_detail':'concurrent-source-appends.json',
    'old_inventories_rehashed':1124,'locked_points_received_hash_verified':True,
    'no_detector_reexecuted':True,'no_research_resumed_after_STORAGE_STOP':True,
    'no_remote_write_after_STORAGE_STOP':True,'storage_violation_reported':True,'draft_unexecuted':True,
    'all_failed_outputs_preserved':True,'no_commit_push':True})
files={}
for p in (R/'results/T-033/scripts').glob('*session7*.py'):
    files[str(p.relative_to(R)).replace('\\','/')]= {'sha256':sha(p),'bytes':p.stat().st_size}
for p in (R/'results/T-033/runs').glob('session7-*'):
    if p.is_dir():
        for f in p.rglob('*'):
            if f.is_file() and f!=C/'manifest.json':files[str(f.relative_to(R)).replace('\\','/')]={'sha256':sha(f),'bytes':f.stat().st_size}
for p in (state,log):files[str(p.relative_to(R)).replace('\\','/')]={'sha256':sha(p),'bytes':p.stat().st_size}
write(C/'manifest.json',{'status':'PASS','path_basis':'repository root','self_excluded':True,'files':files})
for rel,m in files.items():assert sha(R/rel)==m['sha256'] and (R/rel).stat().st_size==m['bytes']
print('CHECKPOINT PASS',len(files),'files. Storage approval and manual synthesis remain OPEN.')
