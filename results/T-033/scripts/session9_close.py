"""Final documentary/source integrity, ledger, append-only handoff and T033 row."""
import pathlib,json,hashlib,datetime,re,shutil,difflib,ast
ROOT=pathlib.Path(__file__).resolve().parents[3];RUN=ROOT/'results/T-033/runs';OUT=RUN/'session9-complete-checkpoint-001';REPORT=RUN/'session9-report-002'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def meta(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def stamp():return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
base=read(RUN/'session9-open-001/baseline.json')
oldbad=[r for r,m in base['old_t033_files'].items() if not (ROOT/r).is_file() or meta(ROOT/r)!=m]
protectedbad=[r for r,m in base['protected'].items() if meta(ROOT/r)!=m]
assert not oldbad,oldbad;assert not protectedbad,protectedbad
checks=[]
for n in ['session8-extraction-001','session8-evidence-receive-001','session8-stats-receive-001','session9-manual-receive-001','session9-final-receive-001']:
 b=RUN/n;inv=read(b/'artifact-inventory.json');inv=inv.get('files',inv)
 if isinstance(inv,list):inv={x.get('path',x.get('relative_path')):x for x in inv}
 bad=[r for r,m in inv.items() if meta(b/'artifacts'/r)!={'bytes':m['bytes'],'sha256':m['sha256']}];assert not bad,(n,bad)
 checks.append({'inventory':str((b/'artifact-inventory.json').relative_to(ROOT)),'files':len(inv),'mismatches':bad})
for n in ['session9-reading-checkpoint-001']:
 b=RUN/n;bad=[]
 for r,m in read(b/'manifest.json')['files'].items():
  p=b/(pathlib.Path(r).name+'.after') if r in ['docs/STATE.md','tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'] else ROOT/r
  if meta(p)!=m:bad.append(r)
 assert not bad,bad
 checks.append({'manifest':str((b/'manifest.json').relative_to(ROOT)),'historical_LOG_STATE_snapshots':True,'mismatches':bad})
for r,m in read(REPORT/'package-manifest.json')['files'].items():assert meta(REPORT/r)==m,r
for r,m in read(REPORT/'additional-source-verification.json')['files'].items():assert meta(pathlib.Path(r) if pathlib.Path(r).is_absolute() else ROOT/r)=={k:m[k] for k in ['bytes','sha256']},r
# Verify publication correction is textual; preserve every numeric/object leaf.
a=read(RUN/'session9-report-001/bao-phu-nhom.json');b=read(REPORT/'bao-phu-nhom.json')
def expected_text(x):
 if isinstance(x,str):return x.replace('window shift/std crossing','window median shift/MAD ratio crossing')
 if isinstance(x,list):return [expected_text(v) for v in x]
 if isinstance(x,dict):return {k:expected_text(v) for k,v in x.items()}
 return x
assert expected_text(a)==b
for name in ['chuoi-bang-chung.json','phan-ra-tien-xu-ly.json','do-tre-sau-moc.json','nsigma-nguong-co-dinh.json','doi-chieu.json','tai-log.json','stats.json','supplemental-stats.json','duration-at-locked-points.json','workload-at-locked-points.json']:
 assert sha(REPORT/name)==sha(RUN/'session9-report-001'/name),name
required=read(RUN/'session9-report-001/package-manifest.json')['required_SPEC_outputs']
assert all((REPORT/n).is_file() for n in required)
for p in (ROOT/'results/T-033/scripts').glob('session9_*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
for r in read(REPORT/'tai-log.json')['log_excerpts']:
 for s in r.get('samples',[]):assert 'message' not in s
last=read(RUN/'session9-open-001/session9-end-preflight-001.stdout');assert last['status']=='PASS' and not last['worker_candidates'] and last['logical_bytes']<5*2**30
log=ROOT/'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md';state=ROOT/'docs/STATE.md';logbefore=log.read_bytes();statebefore=state.read_bytes()
assert logbefore.startswith((RUN/'session9-open-001/LOG.md.before').read_bytes())
OUT.mkdir(exist_ok=False)
shutil.copyfile(log,OUT/'LOG.md.before-end');shutil.copyfile(state,OUT/'STATE.md.before-end')
ledgerpath=RUN/'session8-compute-evidence-checkpoint-001/ledger.json';ledger=read(ledgerpath);charges=[]
for p in sorted((RUN/'session9-open-001').glob('*.timer.json')):
 t=read(p);assert t['exit_code']==0,(p,t)
 charges.append({'source':str(p.relative_to(ROOT)),'sha256':sha(p),**{k:t[k] for k in ['charged_processing_s','basis','exit_code']}})
ledger['charges']+=charges;ledger['new_processing_charged_s']+=sum(x['charged_processing_s'] for x in charges)
ledger['remaining_approved_s']=ledger['approved_max_new_processing_s']-ledger['new_processing_charged_s'];assert ledger['remaining_approved_s']>0
ledger['approved_total_processing_s']=ledger['approved_prior_processing_s']+ledger['new_processing_charged_s'];ledger['previous_snapshot']={'path':str(ledgerpath.relative_to(ROOT)),'sha256':sha(ledgerpath)};ledger['at']=stamp()
write(OUT/'ledger.json',ledger)
template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
def block(header):
 s=template.split(header,1)[1];return s.split('```text\n',1)[1].split('\n```',1)[0]
common=block('## Prompt chung');stage=block('### Soát kết quả');gate=block('### G2 — Baseline và phân tích hạn chế')
fills={
 '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>':'T-033, tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md và LOG.md',
 '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>':'soát kết quả',
 '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>':'P4, G2',
 '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>':'Codex làm; Claude phản biện',
 '<danh sách đường dẫn và git diff từ commit gốc nếu có>':'AGENTS.md; docs/STATE.md; SPEC/LOG của T-033; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; git HEAD 6c93e6dc31f0c991b4ac6d1cfd44fcc0e989c84c; diff phiên tại results/T-033/runs/session9-complete-checkpoint-001/',
 '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>':'không có bản REVIEW trong thư mục task; các mục bàn giao trước nằm trong LOG',
 '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>':'results/T-033/runs/session9-report-002/; package-manifest.json, source-catalog.json, additional-source-verification.json tại đó; results/T-033/runs/session9-complete-checkpoint-001/manifest.json và ledger.json; source native BARO revision e35f4ec ở results/T-033/runs/checkpoint-handoff-001/source-native/; src/p3/adapters/phat_hien.py và src/p3/danh_gia.py; môi trường/lệnh đã lưu trong LOG và results/T-033/scripts/session9_control.py',
 '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>':'chỉ đọc và trả lời trong chat; chưa có quyền ghi bản REVIEW, LOG, STATE hoặc chạy thực nghiệm mới trong lượt phản biện này'
}
for k,v in fills.items():assert k in common,k;common=common.replace(k,v)
assert not re.search(r'<[^\n]+>',common)
prompt=common+'\n\n'+stage+'\n\n'+gate+'\n';(OUT/'handoff-claude.txt').write_text(prompt,encoding='utf-8')
write(OUT/'prompt-template-verification.json',{'status':'PASS','template':{'path':'docs/review-prompt.md',**meta(ROOT/'docs/review-prompt.md')},'blocks':['Prompt chung','Soát kết quả','G2'],'only_neutral_placeholder_fills':fills,'official_reviewer_not_dispatched':True})
write(OUT/'self-check.json',{'status':'PASS','scope_old_T033_unchanged':True,'protected_unchanged':True,'required_SPEC_outputs':required,'current_package':'results/T-033/runs/session9-report-002/package-manifest.json','numeric_origin':'session9-final-receive-001/artifact-inventory.json','checks':checks,'text_amendment_only':True,'all_numeric_outputs_byte_identical_to_author001':True,'scripts_AST':'PASS','source_and_context':'PASS','P4_source_alignment':'Five P4 sections; conditional native chains, matching gaps and K1-K7; no claim RQ2/G2 closed or graph benefit established','open_science':['physical onset/clean negatives','load/sampling/status/unit semantics and matching','prior-only/per-channel theta attribution','causal preprocessing and graph selection/benefit','D duration endpoint'],'historical_actual_time':'OPEN','code_and_data_mutated':False,'detectors_reexecuted':False,'EC2_final':{k:last[k] for k in ['status','worker_candidates','logical_bytes','disk_free_bytes','environment']}})
row='| T-033 | Lần theo cơ chế báo động trước mốc | P4 | Codex | Claude | Chờ phản biện (phiên9, 11/10): đầu ra SPEC và đọc chuỗi/đối chứng đã tổng hợp tại results/T-033/runs/session9-report-002; source/hash/scalar/scope PASS, không rerun detector. RQ2/G2, onset/coverage/prior riêng và chọn P6 còn OPEN; kiểm tiếp K1–K7. Checkpoint cuối session9-complete-checkpoint-001 có ledger/manifest và prompt Claude để Minh chuyển; EC2 cuối không worker, vẫn bật | `tasks/T-033-g2-nguyen-nhan-phat-hien/` |'
text=state.read_text(encoding='utf-8-sig');lines=text.splitlines(keepends=True);found=[i for i,x in enumerate(lines) if x.startswith('| T-033 |')];assert len(found)==1
assert state.read_bytes()==statebefore
i=found[0];lines[i]=row+'\n';state.write_text(''.join(lines),encoding='utf-8',newline='')
assert [x for x in state.read_text(encoding='utf-8').splitlines() if not x.startswith('| T-033 |')]==[x for x in statebefore.decode('utf-8-sig').splitlines() if not x.startswith('| T-033 |')]
with log.open('a',encoding='utf-8',newline='\n') as f:
 f.write('\n### Kết thúc phiên 9 — '+stamp()+'\n\n')
 f.write('1. **Đã làm:** hoàn thiện đầu ra người làm theo toàn SPEC tại `results/T-033/runs/session9-report-002/`. Đọc scalar mọi đường/điểm khóa, đúng cùng cột ở đối chứng, chuỗi density→mass→posterior→MAP/CP, factorial/matching và context; không nhận đã đọc mọi raw cell. Báo cáo đủ năm mục P4, phân biệt tính toán với vật lý và chỉ rõ K1–K7. Cơ chế margin/OR, cạnh tranh MAP và contrast scale/bundle được phân xử có điều kiện. Không chọn detector/graph hoặc đóng RQ2/G2. Hai trợ lý chỉ đọc hỗ trợ, Codex tự đọc nguồn; không phải Claude phản biện.\n')
 f.write('2. **File đổi:** chỉ lượt mới `results/T-033/scripts/session9_*` và `results/T-033/runs/session9-*`, LOG nối, dòng T-033 STATE. File set đầy đủ ở checkpoint `new-files.json`; nguồn cũ, SPEC/WHY/DECISIONS/MRP/AGENTS/T-032 và phần khác STATE giữ nguyên. Bản001 giữ nguyên; bản002 sửa annotation B4 std→MAD và nối notes, số không đổi. Không commit/push.\n')
 f.write('3. **Kiểm:** source/inventory/manifests lịch sử PASS; source/scalar/readback cũ không chạy lại. EC2 publication kiểm common-column arrays toàn file exact, margin/OR, normalizer/MAP→CP và nguồn; receive hai đầu hash PASS. JSON/AST, output list SPEC, numeric copy và text-only correction, protected/old-T033/LOG-prefix/STATE-row PASS; tự soát nguồn MRP/DT18/cô/LESSONS/WHY và code native/chấm. Chi tiết self-check. Local prepare thất bại do alias trang-thai lịch sử, rồi dispatch thiếu input dừng trước SSH; giữ local-errors, sửa namespace, không tính như EC2 command. Mọi EC2 thực tế có timer/pin cumulative.\n')
 f.write('4. **OPEN/cần Minh quyết:** physical onset/false alarms/trễ vận hành; coverage/load/duration/status/log semantics; prior riêng/attribution covariance; causal preprocessing và benefit graph; D. K1–K7 nêu đúng input/owner/phép phân xử/phạm vi/chi phí chưa kiểm/điều kiện thất bại và P6 phụ thuộc. Thiếu trường chưa ghi không được collector mới tái tạo. Không có bất đồng phản biện chính thức mới vì chưa mở review. Chờ Minh chuyển prompt Claude rồi quyết nghiệm thu/bổ sung; task chờ phản biện, không xong. Đề xuất commit sau nghiệm thu: `T-033: lần theo cơ chế phát hiện và tổng hợp bằng chứng P4`; chưa được quyền commit/push.\n')
 f.write('\n- **EC2 cuối:** preflight `session9-open-001/session9-end-preflight-001.stdout` PASS, không worker, '+str(last['logical_bytes'])+' byte logical <5GiB; không archive mới, không cài/xóa/bật/tắt máy. Ledger mới tại checkpoint: charge='+str(ledger['new_processing_charged_s'])+'s, còn='+str(ledger['remaining_approved_s'])+'s trong trần4h xử lý mới. 8h cũ là dự phòng hành chính; actual lịch sử OPEN. Không cộng đôi timer phiên8; base là checkpoint phiên8 và chỉ thêm timer phiên9.\n')
 f.write('- **Lệnh EC2 cuối:** `session9_control.py remote-readonly session9-end-preflight-001 results/T-033/scripts/session6_preflight.py`; SSH/Python/env/payload/timer/ledger pin trong open run. **Lệnh laptop kết thúc:** bundled Python `-B -X utf8 results/T-033/scripts/session9_close.py`.\n')
 f.write('- **Bước tiếp chính xác:** Minh copy `results/T-033/runs/session9-complete-checkpoint-001/handoff-claude.txt` sang Claude. Claude đọc AGENTS/STATE/SPEC/LOG rồi manifest checkpoint và source catalog của report002, kiểm hash trước dùng, soát kết quả theo prompt. Không cần EC2 hoặc rerun PASS để mở review; muốn chạy/ghi REVIEW phải có quyền riêng. Trước EC2 tiếp phải kiểm process/source/hash có đo và pin cumulative mới từ ledger cuối; không khởi trùng.\n\n#### Prompt Claude — Minh chuyển thủ công\n\n```text\n'+prompt+'```\n')
assert log.read_bytes().startswith(logbefore)
shutil.copyfile(log,OUT/'LOG.md.after');shutil.copyfile(state,OUT/'STATE.md.after')
(OUT/'LOG.append.diff').write_text(''.join(difflib.unified_diff(logbefore.decode('utf-8-sig').splitlines(keepends=True),log.read_text(encoding='utf-8').splitlines(keepends=True),fromfile='LOG.before-end',tofile='LOG.after')),encoding='utf-8')
(OUT/'STATE.diff').write_text(''.join(difflib.unified_diff(statebefore.decode('utf-8-sig').splitlines(keepends=True),state.read_text(encoding='utf-8').splitlines(keepends=True),fromfile='STATE.before-end',tofile='STATE.after')),encoding='utf-8')
write(OUT/'checkpoint.json',{'status':'AUTHOR_OUTPUT_COMPLETE_WAITING_REVIEW','at':stamp(),'task':'T-033','report':'results/T-033/runs/session9-report-002/','ledger':'ledger.json','self_check':'self-check.json','official_handoff':'handoff-claude.txt','last_command':'session9_close.py; final EC2 preflight recorded in LOG','next_step':'Minh transfers prompt manually; Claude read-only review unless separately authorized','no_active_job_started_by_session':True,'EC2_still_on':True,'research_decisions_added':False,'historical_actual_processing':'OPEN'})
(OUT/'README.md').write_text('Đầu ra người làm T-033 hoàn thiện, chờ phản biện. Đọc checkpoint/self-check/ledger/manifest; LOG/STATE là snapshot sau phiên, đối chiếu lịch sử bằng LOG.md.after/STATE.md.after. Bản cuối report002; nguồn/run/bản001 giữ nguyên. Prompt chưa gửi, Minh chuyển thủ công. Mọi số và source pin trong gói/manifest.\n',encoding='utf-8')
newfiles={str(p.relative_to(ROOT)).replace('\\','/'):meta(p) for p in (ROOT/'results/T-033').rglob('*') if p.is_file() and str(p.relative_to(ROOT)) not in base['old_t033_files'] and not p.is_relative_to(OUT)}
write(OUT/'new-files.json',{'files':newfiles,'other_mutations':['LOG append','only T033 STATE row'],'preexisting_git_changes_not_attributed_to_session':True})
files=dict(newfiles);files.update({str(p.relative_to(ROOT)).replace('\\','/'):meta(p) for p in OUT.iterdir() if p.is_file()});files[str(log.relative_to(ROOT)).replace('\\','/')]=meta(log);files['docs/STATE.md']=meta(state)
write(OUT/'manifest.json',{'status':'PASS','files':files,'historical_LOG_STATE_snapshots':'LOG.md.after / STATE.md.after'})
for r,m in files.items():assert meta(ROOT/r)==m,r
assert all(meta(ROOT/r)==m for r,m in base['old_t033_files'].items())
print(json.dumps({'status':'PASS','report':str(REPORT.relative_to(ROOT)),'checkpoint':str(OUT.relative_to(ROOT)),'new_processing_charged_s':ledger['new_processing_charged_s'],'remaining_s':ledger['remaining_approved_s'],'new_files':len(newfiles),'manifest_files':len(files),'EC2_workers':last['worker_candidates']},ensure_ascii=False))
