"""Laptop documentation, scope/diff/hash checkpoint only. Never starts EC2."""
import ast, datetime, difflib, hashlib, json, pathlib
R=pathlib.Path(__file__).resolve().parents[3]
O=R/'results/T-033/runs/session7-open-001'
C=R/'results/T-033/runs/session7-storage-checkpoint-001'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
checkpoint=read(C/'checkpoint.json');ledger=read(C/'ledger.json')
# Preserve the earlier draft check against its exact then-current source.
v2=R/'results/T-033/scripts/session7_extract_v2.py';final=v2.read_text(encoding='utf-8')
prior=final.replace("                assert np.array_equal(fz['columns'],a['columns']), 'Fixed/native column order drift'\n                assert len(postrow)<=1, 'Duplicate fixed post index'\n                if len(postrow):assert int(fz['times'][int(postrow[0])])==int(a['times'][i])\n",'')
prior=prior.replace("for oid in INPUT['selected_case_ids']],",'for oid in CASES],')
assert hashlib.sha256(prior.encode('utf-8')).hexdigest()==read(C/'draft-static-check.json')['sha256']
(O/'draft-before-postmap-validation.py').write_bytes(prior.encode('utf-8'))
ast.parse(final)
write(C/'draft-static-check-final.json',{'status':'PASS_STATIC_ONLY_NOT_EXECUTED',
    'script':str(v2.relative_to(R)).replace('\\','/'),'sha256':sha(v2),'AST':True,
    'earlier_draft':'results/T-033/runs/session7-open-001/draft-before-postmap-validation.py',
    'changes_since_earlier_check':['Exact frozen/native column order and post timestamp checks','At most one post_indices match','Raw-source verification covers only explicit executed IDs'],
    'EC2_execution':False,'storage_extension_authorized':False,
    'reference_headers':'results/T-033/runs/session7-open-001/session7-storage-status-002.stdout#/frozen_array_headers'})
log=R/'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'
with log.open('ab') as f:
    f.write(('\n- Tự kiểm nguồn: 825 file cũ, 299 file mới và manifest phiên6 460 file đạt; EC2 source/native/raw89/env pin mới PASS sau một lượt SSH bị môi trường chặn. Timer đầy đủ, không chạy lại detector.\n'
    '- Chặng đọc tay chuẩn bị: kiểm đúng quy tắc đóng băng 64 nhóm, giữ điều kiện ghép thiếu; khóa 210 đường ca trước đọc giá trị, nhận hai file khóa cùng hash. Lượt trích trung gian lỗi vì chiếu mảng fixed hậu proxy sai và guard chưa đo chính xác file sắp ghi; toàn lượt lỗi giữ nguyên, không dùng để kết luận.\n'
    '\n### Kết thúc phiên 7 — '+now+' — checkpoint và dừng vì vượt trần dung lượng\n\n'
    '1. Đã làm: đọc nguồn/chặng/checkpoint Minh chỉ định; tự kiểm hash/EC2 pin; kiểm lựa chọn/coverage 40 nhóm gốc+24 nhóm mới và khóa điểm 210 đường ca. Chỉ trích trung gian đã lưu, không gọi lại detector. Dừng STORAGE_STOP sau 11 ca; kiểm chỉ đọc dung lượng/process/header, nhận hai file khóa. Đã chuẩn bị bản sửa projection/guard/nén không mất dữ liệu cho Minh xem; draft chưa chạy.\n'
    '2. File đổi: chỉ thêm scripts/session7_control.py, session7_extract.py, session7_extract_v2.py (draft), session7_storage_status.py, session7_receive_locks.py, finish_session7.py; runs/session7-open-001/, session7-*-001/002--budget/ theo manifest và session7-storage-checkpoint-001/. LOG chỉ nối; chỉ dòng T-033 STATE. EC2 chỉ thêm snapshot và runs/session7-manual-001/ trong ~/rca/T-033/. Không sửa nguồn cũ/SPEC/DECISIONS/WHY/MRP/LESSONS/AGENTS/review-prompt/T-032/test/locked/heldout; không xóa thêm/cài package/commit/push/bật-tắt EC2.\n'
    '3. Kiểm và lỗi: own integrity PASS 825+299 và 460 manifest; native/raw89/source/env EC2 PASS; audit lựa chọn nhóm PASS, point lock nhận/hash PASS. Extraction exit1 STORAGE_STOP; hậu proxy frozen có721 hàng nhưng mã so T1441, chép cả mảng ở mỗi điểm. Guard64MiB trước ca bỏ lọt file lớn, khiến trần bị vượt trước lượt guard kế tiếp. Mã lỗi/evidence/lượt dở giữ nguyên. Controller lỗi local trước SSH đã lưu, không tính thành xử lý EC2. AST/header bản sửa đạt, chưa pilot/rest/readback EC2 nên không gọi PASS nghiên cứu. Complete diff/file set/scope/hash ở checkpoint.\n'
    '4. OPEN và cần Minh: tổng EC2 '+str(checkpoint['logical_bytes'])+' byte vượt trần '+str(checkpoint['approved_limit_bytes'])+' byte '+str(checkpoint['excess_bytes'])+' byte. Lượt lỗi mới '+str(checkpoint['new_failed_run_bytes'])+' byte. Dừng toàn phần trích/đọc tay/tổng hợp phụ thuộc; xin duyệt đề xuất chính xác ở README checkpoint: trần EC2 5GiB, giữ mọi bản lỗi, dùng draft v2 map post_indices đúng, kiểm byte thực trước ghi, một pilot rồi rest có đo, tiếp nguyên SPEC. Dự toán2–10phút/30–300MiB chưa kiểm, không upper bound. Không thay tham số/tiêu chí/phương pháp hoặc ngân sách thời gian. RQ2/P4/G2/P6 và nguyên nhân vật lý/onset vẫn OPEN; chưa có chuỗi đọc tay được phân xử, không gọi task hoàn tất/chờ Claude.\n\n'
    'Hạch toán: charged mới '+repr(ledger['new_processing_charged_s'])+' giây; còn '+repr(ledger['remaining_approved_s'])+' giây theo ledger.json trong checkpoint mới, gồm lỗi/kiểm/nhận và full SSH bounds. 28800 giây cũ vẫn dự phòng chưa kiểm, actual cũ OPEN; không lấy lịch/subtotal. Không chờ duyệt lại thời gian. Ledger lịch sử giữ nguyên.\n\n'
    'EC2 kiểm cuối metadata tại '+checkpoint['ec2']['observed_utc']+': không worker T-033; disk free '+str(checkpoint['disk_free_bytes'])+' byte. Sau đó chỉ nhận khóa, không ghi thêm EC2 hoặc chạy nghiên cứu. Laptop có thể đóng. Không đổi trạng thái bật/tắt EC2. Minh cần duyệt đề xuất sửa/dung lượng hoặc chọn phương án khác.\n\n'
    'Bước tiếp chính xác: đọc results/T-033/runs/session7-storage-checkpoint-001/README.md, checkpoint.json, ledger.json, scope-verification.json, manifest.json; session7-open-001/points-lock.json, coverage-matching.json và lock-receive-verification.json; v1/v2 và draft-static-check-final.json. Chưa duyệt thì không chạy v2. Sau lời duyệt đúng phạm vi, input mới nối pin hai khóa, chọn pilot explicit, snapshot từ ledger mới cộng mọi timer phát sinh; process/source/hash EC2 có đo trước pilot. Cần tự kiểm schema/scalar/post_indices/NaN/time/flags/byte/hash/readback ở một ca rồi rest loại pilot, giữ mọi lượt. Tiếp đọc tay và tổng hợp đủ nhóm/SPEC/nguồn; log text ở điểm cần phân xử còn cần đọc. Không bịa CLI chưa hoàn thiện. Chưa prompt Claude chính thức vì toàn task chưa xong; không tự mở/gửi review.\n\n'
    'Lệnh EC2 cuối: session7_control.py remote-readonly session7-receive-locks-001 results/T-033/scripts/session7_receive_locks.py; Python pin/SSH trong controller, payload và timer ở session7-open-001. Snapshot ledger pin trong RAM trước lệnh chỉ đọc vì máy đã vượt storage; bản lịch sử lưu trên laptop.\n'
    'Lệnh chốt laptop cuối: C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B -X utf8 results/T-033/scripts/finish_session7.py — chỉ tài liệu/hash/diff, không SSH hay nghiên cứu.\n').encode('utf-8'))

# Read the live STATE immediately before replacing the one authorized task row.
state=R/'docs/STATE.md';before=state.read_bytes();lines=before.decode('utf-8').splitlines(keepends=True)
idx=[i for i,l in enumerate(lines) if l.startswith('| T-033 |')];assert len(idx)==1
i=idx[0];parts=lines[i].split('|');ending='\r\n' if lines[i].endswith('\r\n') else '\n'
parts[6]=' Đang thực hiện (phiên 7, 11/10): source/hash và 64 nhóm/210 đường ca khóa đạt; trích trung gian dừng STORAGE_STOP, EC2 vượt 4GiB 49.489.251 byte, không worker, giữ mọi lượt lỗi. Chờ Minh duyệt đề xuất trần5GiB + draft projection/byte guard, chưa đọc tay/tổng hợp/RQ2/G2. Checkpoint session7-storage-checkpoint-001; ledger cuối ở đó '
lines[i]='|'.join(parts).rstrip('\r\n')+ending
state.write_bytes(''.join(lines).encode('utf-8'))
after=state.read_bytes();oldlines=before.decode('utf-8').splitlines();newlines=after.decode('utf-8').splitlines()
assert len(oldlines)==len(newlines) and [j for j,(a,b) in enumerate(zip(oldlines,newlines)) if a!=b]==[i]
log0=(O/'LOG.md.before').read_bytes();assert log.read_bytes().startswith(log0)
protected={}
for rel,meta in read(O/'baseline.json').items():
    if rel in ('docs/STATE.md','tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'):continue
    assert (R/rel).stat().st_size==meta['bytes'] and sha(R/rel)==meta['sha256'],rel
    protected[rel]=meta
for name in ('checkpoint-handoff-001','session6-compute-checkpoint-001'):
    base=R/'results/T-033/runs'/name;inv=read(base/'artifact-inventory.json');inv=inv.get('files',inv)
    for rel,meta in inv.items():
        p=base/'artifacts'/rel;assert p.stat().st_size==meta['bytes'] and sha(p)==meta['sha256'],rel
diff=[]
for rel,b in [('docs/STATE.md',(O/'STATE.md.before').read_bytes()),('tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md',log0)]:
    diff.extend(difflib.unified_diff(b.decode('utf-8').splitlines(keepends=True),(R/rel).read_text(encoding='utf-8').splitlines(keepends=True),fromfile='before/'+rel,tofile=rel))
(C/'approved-docs.diff').write_text(''.join(diff),encoding='utf-8',newline='\n')
write(C/'scope-verification.json',{'status':'PASS','at':now,'LOG_append_only':True,
    'STATE_only_task_changed':'T-033','STATE_changed_line_1based':i+1,
    'protected_docs_unchanged':protected,'old_inventories_rehashed':1124,
    'no_remote_write_after_storage_stop':True,'no_detector_rerun':True,
    'draft_unexecuted':True,'storage_violation_reported':True,
    'failed_run_preserved':True,'no_commit_push':True})
files={}
for p in (R/'results/T-033/scripts').glob('*session7*.py'):files[str(p.relative_to(R)).replace('\\','/')]={'sha256':sha(p),'bytes':p.stat().st_size}
for p in (R/'results/T-033/runs').glob('session7-*'):
    if p.is_dir():
        for f in p.rglob('*'):
            if f.is_file() and f!=C/'manifest.json':files[str(f.relative_to(R)).replace('\\','/')]={'sha256':sha(f),'bytes':f.stat().st_size}
for p in (log,state):files[str(p.relative_to(R)).replace('\\','/')]={'sha256':sha(p),'bytes':p.stat().st_size}
write(C/'manifest.json',{'status':'PASS','path_basis':'repository root','self_excluded':True,'files':files,
    'NOTE':'Pins this close snapshot. Future authorized LOG/STATE append/change are not old-output corruption.'})
for rel,m in files.items():assert (R/rel).stat().st_size==m['bytes'] and sha(R/rel)==m['sha256']
print('CHECKPOINT PASS',len(files),'files; research stopped, awaiting storage/correction approval')
