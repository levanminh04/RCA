"""Kiểm complete diff/tập file, bảo toàn phạm vi và ghi manifest cuối."""
import ast,json,hashlib,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
from run import ROOT,OUT,read,write,selector,pd
from do_thi.builder import Prepared,op_id
sys.stdout.reconfigure(encoding='utf-8')

base=read(OUT/'runs/buoc0-001/truoc-phien.json')
current={p.relative_to(ROOT).as_posix():selector.sha256_file(p) for folder in ['src','docs','tasks']
         for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
allowed={'docs/STATE.md','tasks/T-035-p5-do-thi-tu-trace/LOG.md'}
outside=[p for p,h in base['files'].items() if p not in allowed and not p.startswith('src/do_thi/') and current.get(p)!=h]
new=[p for p in current if p not in base['files'] and not p.startswith('src/do_thi/')]
assert not outside and not new,('outside_scope',outside,new)
govern=read(OUT/'runs/buoc0-001/input-verification.json')['governing_hashes']
assert all(selector.sha256_file(ROOT/p)==h for p,h in govern.items())
log=(ROOT/'tasks/T-035-p5-do-thi-tu-trace/LOG.md').read_bytes()
pos=log.index('\n\n## Phiên 6 —'.encode('utf-8'))
assert hashlib.sha256(log[:pos]).hexdigest()==base['files']['tasks/T-035-p5-do-thi-tu-trace/LOG.md'],'log_not_append_only'

# Dựng lại đúng dòng trạng thái đầu phiên; mọi byte còn lại phải giữ.
state=ROOT/'docs/STATE.md';text=state.read_text('utf-8');lines=text.splitlines(keepends=True)
original=' Đã tạo SPEC và sửa tài liệu theo duyệt (14/10/2026, Q-150, Q-151); chưa triển khai. Khảo sát operation ngay trên mọi ca dev; Node qua bộ đọc bổ sung chỉ dev, nghĩa thiếu giữ OPEN. Minh giao phiên Codex mới tự rà một lần rồi triển khai nếu không có vấn đề (Q-153); prompt triển khai tại LOG Phiên 5. Giữ Claude phản biện kết quả. T-036 nhận nguồn kiến trúc, gồm nguồn tĩnh FlashTicket; chưa có SPEC riêng, soạn sau đặc tả v1 của T-035. '
for i,line in enumerate(lines):
    if line.startswith('| T-035 |'):
        pieces=line.split('|');pieces[6]=original;lines[i]='|'.join(pieces)
candidate=''.join(lines);ending=None
for sep in ['\n','\r\n']:
    raw=candidate.replace('\n',sep).encode('utf-8')
    if hashlib.sha256(raw).hexdigest()==base['files']['docs/STATE.md']:ending=sep;break
assert ending is not None,'state_more_than_one_row_changed'
state.write_bytes(text.replace('\n',ending).encode('utf-8'))

fixture=read(OUT/'fixture/inputs.json');expected_depth={'F1':{'a':0,'b':0,'c':0},'F8':{'a':0,'b':0,'a2':0},'F9':{'a':0,'inner':1,'inner2':2}}
write(OUT/'runs/kiem-cuoi-001/vocabulary-expected.json',expected_depth)
depth_results=[]
for c in fixture:
    if c['name'] not in expected_depth:continue
    v=Prepared(pd.DataFrame(c['spans']),{},c['universe']).vocabulary()
    actual={o['operation']:o['max_internal_depth'] for o in v['operations']}
    assert actual==expected_depth[c['name']]
    depth_results.append({'name':c['name'],'expected':expected_depth[c['name']],'actual':actual,'pass':True})
write(OUT/'runs/kiem-cuoi-001/vocabulary-regression.json',{'checks':depth_results,'pass':True})

manual=[]
for ds,oid in [('RE2-TT','dev-b8bd0abf60'),('Nezha-OB','dev-607751ac0a')]:
    c=read(OUT/'runs/pilot-002/cases'/ds/f'{oid}.json')
    e=read(OUT/'do-thi'/ds/oid/'thuc-the/full.json');o=read(OUT/'do-thi'/ds/oid/'thao-tac/full.json')
    ee={(z['source'],z['target']) for z in e['edges']};oo={(z['source'],z['target']) for z in o['edges']}
    for ti,t in enumerate(c['manual_trace_witness']):
        seen={r['spanID']:r for r in t['first_rows']};pairs=[]
        for child in t['first_rows']:
            parent=seen.get(child['parentSpanID'])
            if parent is None:continue
            op_pair=(op_id(parent['serviceName'],parent['operationName']),op_id(child['serviceName'],child['operationName']))
            assert op_pair in oo
            cross=parent['serviceName']!=child['serviceName']
            if cross:assert (parent['serviceName'],child['serviceName']) in ee
            pairs.append({'parent_span':parent['spanID'],'child_span':child['spanID'],'cross_entity':cross,'operation_edge_found':True,'entity_edge_required':cross})
        manual.append({'dataset':ds,'opaque_id':oid,'witness_pointer':f'#/manual_trace_witness/{ti}','pairs':pairs})
write(OUT/'runs/kiem-cuoi-001/manual-pair-check.json',{'traces':manual,'pass':True})

json_count=0
for p in OUT.rglob('*.json'):
    json.loads(p.read_text('utf-8-sig'));json_count+=1
for p in list((ROOT/'src/do_thi').glob('*.py'))+list((OUT/'scripts').glob('*.py'))+list((OUT/'fixture').glob('*.py')):
    ast.parse(p.read_text('utf-8'))

status_before=base['git_status'];status_after=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True)
delta=sorted(set(status_after.splitlines())-set(status_before.splitlines()))
assert all(any(p in r for p in ['results/T-035','src/do_thi','tasks/T-035','docs/STATE.md']) for r in delta),('git_outside_delta',delta)
diff=subprocess.run(['git','diff','--check','--','src/do_thi','results/T-035','tasks/T-035-p5-do-thi-tu-trace/LOG.md','docs/STATE.md'],cwd=ROOT,capture_output=True,text=True)
assert diff.returncode==0,diff.stdout+diff.stderr
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['head'],'commit_changed'

verification={'status':'PASS','json_files_valid':json_count,'outside_scope_changes':outside,'outside_scope_new_files':new,
    'log_append_only':True,'state_only_T035_row':True,'src_p3_unchanged':True,'src_circa_unchanged':True,
    'governing_hashes_unchanged':True,'HEAD_unchanged':True,'git_diff_check':True,'git_status_delta':delta,
    'tracked_scope_diff':subprocess.check_output(['git','diff','--','docs/STATE.md'],cwd=ROOT,text=True),
    'current_log_sha256':selector.sha256_file(ROOT/'tasks/T-035-p5-do-thi-tu-trace/LOG.md'),
    'current_state_sha256':selector.sha256_file(state),
    'pending_doc_sync':'STATE Task đang mở retains pre-execution sentence outside authorized row; proposal recorded in LOG, awaiting Minh.',
    'source_p3_hashes':{p:h for p,h in current.items() if p.startswith('src/p3/')},
    'manual_pair_check':'manual-pair-check.json','vocabulary_regression':'vocabulary-regression.json'}
write(OUT/'runs/kiem-cuoi-001/final-verification.json',verification)

artifacts=[]
for folder in [OUT,ROOT/'src/do_thi']:
    for p in sorted(folder.rglob('*')):
        if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts:
            artifacts.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':selector.sha256_file(p)})
bytes_total=sum(x['bytes'] for x in artifacts)
assert bytes_total<300*1024*1024,'output_budget'
write(OUT/'manifest.json',{'task':'T-035','created_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base['head'],
    'files':artifacts,'artifact_count':len(artifacts),'total_bytes':bytes_total,
    'source_verification':'runs/buoc0-001/input-verification.json','final_verification':'runs/kiem-cuoi-001/final-verification.json',
    'scope':['results/T-035/','src/do_thi/','tasks/T-035-p5-do-thi-tu-trace/LOG.md:append','docs/STATE.md:T-035 row'],
    'LOG_STATE_not_artifacts':'Append-only LOG and STATE row hashes recorded separately in final-verification; manifest excludes itself.',
    'scientific_decisions_added':[],'task_state':'awaiting_official_review','open_test_heldout':False,'commit_push':False,
    'flash_ticket_source':{'commit':'98d5ad5546244e5e7e29b41dbef92d454f50a7ac','path':'D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md',
                           'sha256':selector.sha256_file(Path('D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md'))}})
print(json.dumps({'status':'PASS','artifacts':len(artifacts),'output_MiB':round(bytes_total/1024**2,2),'json_valid':json_count,
                  'outside_scope_changes':[],'log_append_only':True,'state_only_T035_row':True,'commit_push':False},ensure_ascii=False))
