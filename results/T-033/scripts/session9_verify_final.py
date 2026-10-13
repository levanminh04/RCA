"""Metadata-only final readback; normalize diff display, preserve earlier checkpoint."""
import pathlib,json,hashlib,difflib,datetime,shutil
ROOT=pathlib.Path(__file__).resolve().parents[3];RUN=ROOT/'results/T-033/runs';OLD=RUN/'session9-complete-checkpoint-001';OUT=RUN/'session9-complete-checkpoint-002'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def meta(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def write(p,v):
 assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log=ROOT/'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md';state=ROOT/'docs/STATE.md'
for r,m in read(OLD/'manifest.json')['files'].items():
 p=OLD/(pathlib.Path(r).name+'.after') if r in ['docs/STATE.md',str(log.relative_to(ROOT)).replace('\\','/')] else ROOT/r
 assert meta(p)==m,r
before=(OLD/'LOG.md.before-end').read_bytes();after=log.read_bytes();assert after.startswith(before)
OUT.mkdir(exist_ok=False)
def normalized(b):return b.decode('utf-8-sig').replace('\r\n','\n').splitlines(keepends=True)
(OUT/'LOG.append.diff').write_text(''.join(difflib.unified_diff(normalized(before),normalized(after),fromfile='LOG.before-end',tofile='LOG.after-closure')),encoding='utf-8')
shutil.copyfile(OLD/'STATE.diff',OUT/'STATE.diff');shutil.copyfile(OLD/'ledger.json',OUT/'ledger.json');shutil.copyfile(OLD/'self-check.json',OUT/'self-check.json')
prompt=(OLD/'handoff-claude.txt').read_text(encoding='utf-8').replace('session9-complete-checkpoint-001/','session9-complete-checkpoint-002/')
(OUT/'handoff-claude.txt').write_text(prompt,encoding='utf-8')
write(OUT/'diff-display-verification.json',{'status':'PASS','LOG_original_byte_prefix_retained':True,'STATE_only_T033_verified_in_prior_checkpoint':True,'old_LOG_diff_display_issue':'Mixed CRLF/LF comparison showed historical lines as changes; this is display only, byte prefix was preserved','normalized_diff_here':True,'created_before_open_baseline':{'results/T-033/scripts/session9_open.py':meta(ROOT/'results/T-033/scripts/session9_open.py')},'scientific_values_unchanged':True,'all_prior_manifest_entries_verified_with_historical_LOG_STATE_snapshots':True})
stamp=datetime.datetime.now().astimezone().isoformat()
with log.open('a',encoding='utf-8',newline='\n') as f:
 f.write('\n### Kiểm đọc lại cuối — '+stamp+'\n\n- Manifest checkpoint001 và gói report002 đọc lại PASS; LOG/STATE lịch sử đối chiếu snapshot after. Diff LOG đầu tiên hiển thị thay lịch sử do CRLF/LF khác ở bộ so hiển thị; byte prefix không đổi. Diff chuẩn hóa đọc đúng append ở `session9-complete-checkpoint-002/LOG.append.diff`; giữ bản cũ. File `session9_open.py` được tạo trước baseline mở phiên và có pin bổ sung trong diff-display-verification; toàn file set current ở manifest checkpoint002. Không thay dữ liệu/số/code nguồn hay STATE thêm.\n- Checkpoint cuối hiện hành là `session9-complete-checkpoint-002`; ledger giữ nguyên từ001, không có EC2 mới sau end-preflight. Output người làm report002, vẫn chờ phản biện. Lệnh laptop cuối có ghi: bundled Python `-B -X utf8 results/T-033/scripts/session9_verify_final.py`; bước tiếp: Minh copy handoff-claude.txt tại checkpoint002. Bốn mục kết thúc và các OPEN/commit proposal giữ đúng mục trên.\n\n#### Prompt Claude hiện hành — Minh chuyển thủ công\n\n```text\n'+prompt+'```\n')
assert log.read_bytes().startswith(after)
shutil.copyfile(log,OUT/'LOG.md.after');shutil.copyfile(state,OUT/'STATE.md.after')
write(OUT/'checkpoint.json',{'status':'AUTHOR_OUTPUT_COMPLETE_WAITING_REVIEW','task':'T-033','at':stamp,'report':'results/T-033/runs/session9-report-002/','previous_checkpoint':'session9-complete-checkpoint-001','ledger':'ledger.json','official_handoff':'handoff-claude.txt','last_command':'session9_verify_final.py','next_step':'Minh transfers current handoff manually; Claude read-only review unless separately authorized','EC2_still_on':True,'last_process_observation':'session9-open-001/session9-end-preflight-001.stdout; no workers','physical_cause_onset_prior_graph_selection':'OPEN'})
(OUT/'README.md').write_text('Checkpoint cuối T-033 phiên9. Report002 là bộ đầu ra hiện hành; chờ Claude/Minh. Đọc self-check/ledger/manifest/handoff. LOG/STATE trong manifest dùng snapshot LOG.md.after/STATE.md.after để kiểm lịch sử. Giữ checkpoint001; bản diff chuẩn hóa ở đây chỉ sửa hiển thị line ending, không đổi prefix LOG. Không có EC2 mới hoặc ngân sách khác.\n',encoding='utf-8')
base=read(RUN/'session9-open-001/baseline.json');files={str(p.relative_to(ROOT)).replace('\\','/'):meta(p) for p in (ROOT/'results/T-033').rglob('*') if p.is_file() and (str(p.relative_to(ROOT)) not in base['old_t033_files'] or p.name=='session9_open.py') and p!=OUT/'manifest.json'}
files[str(log.relative_to(ROOT)).replace('\\','/')]=meta(log);files['docs/STATE.md']=meta(state)
write(OUT/'manifest.json',{'status':'PASS','files':files,'historical_LOG_STATE_snapshots':'LOG.md.after / STATE.md.after','complete_session_file_set_includes_prebaseline_session9_open_script':True})
for r,m in files.items():assert meta(ROOT/r)==m,r
print(json.dumps({'status':'PASS','checkpoint':'session9-complete-checkpoint-002','manifest_files':len(files),'LOG_append_only':True,'no_EC2_command':True},ensure_ascii=False))
