"""Authorized append-only documentary checkpoint and integrity metadata."""
import pathlib,json,hashlib,datetime,shutil,sys
ROOT=pathlib.Path(__file__).resolve().parents[3]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def meta(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
name=sys.argv[1];out=ROOT/'results/T-033/runs'/name;out.mkdir(exist_ok=False)
base=read(ROOT/'results/T-033/runs/session9-open-001/baseline.json')
bad=[r for r,m in base['old_t033_files'].items() if not (ROOT/r).is_file() or meta(ROOT/r)!=m]
protected=[r for r,m in base['protected'].items() if meta(ROOT/r)!=m]
checks=[]
for n in ['session8-extraction-001','session8-evidence-receive-001','session8-stats-receive-001','session9-manual-receive-001']:
 b=ROOT/'results/T-033/runs'/n;entries=read(b/'artifact-inventory.json');entries=entries.get('files',entries)
 if isinstance(entries,list):entries={x.get('path',x.get('relative_path')):x for x in entries}
 mismatches=[r for r,m in entries.items() if meta(b/'artifacts'/r)!={'bytes':m['bytes'],'sha256':m['sha256']}]
 checks.append({'inventory':str((b/'artifact-inventory.json').relative_to(ROOT)),'files':len(entries),'mismatches':mismatches})
 assert not mismatches,mismatches
assert not bad,bad
assert not protected,protected
log=ROOT/'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md';state=ROOT/'docs/STATE.md'
assert log.read_bytes().startswith((ROOT/'results/T-033/runs/session9-open-001/LOG.md.before').read_bytes())
assert state.read_bytes()==(ROOT/'results/T-033/runs/session9-open-001/STATE.md.before').read_bytes()
ledgerpath=ROOT/'results/T-033/runs/session8-compute-evidence-checkpoint-001/ledger.json'
ledger=read(ledgerpath);charges=[]
for p in sorted((ROOT/'results/T-033/runs/session9-open-001').glob('*.timer.json')):
 t=read(p);charges.append({'source':str(p.relative_to(ROOT)),'sha256':sha(p),**{k:t[k] for k in ['charged_processing_s','basis','exit_code']}})
ledger['charges']+=charges;ledger['new_processing_charged_s']+=sum(x['charged_processing_s'] for x in charges)
ledger['remaining_approved_s']=ledger['approved_max_new_processing_s']-ledger['new_processing_charged_s']
ledger['approved_total_processing_s']=ledger['approved_prior_processing_s']+ledger['new_processing_charged_s']
ledger['previous_snapshot']={'path':str(ledgerpath.relative_to(ROOT)),'sha256':sha(ledgerpath)}
stamp=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat();ledger['at']=stamp
write(out/'ledger.json',ledger)
checkpoint={'at':stamp,'task':'T-033','status':'CONTINUE_AFTER_COMPACTION','role':'Codex worker; Claude official reviewer not opened',
 'completed':['All 210 saved unit paths and 968 locked points read in compact scalar displays; not every raw cell read','Native and adapter mechanisms read','Session9 EC2 source verification and manual projections PASS; no detector rerun','Same-column controls, duration projection and all64 frozen group dossiers saved'],
 'remaining':['Read detailed likelihood/theta/factorial/matching and original flag definitions','Finish all SPEC reports and annotated JSON, self-check full scope/diff/source','Measured final EC2 preflight, LOG/STATE completion and neutral handoff'],
 'open':['Physical onset and operational false alarms','Prior-only versus mask effect','Cross-case matching gaps and missing observer theta at some points','Graph benefit and P6 design selection','Historical actual EC2 time remains OPEN'],
 'last_command':'Read session9 controller, timer names and original attached request on laptop',
 'next_command':'Read source intermediates through session9_read.py, including phan-ra-tien-xu-ly, unit-dossiers and group-dossiers; do not rerun PASS jobs',
 'process_status':{'last_measured_preflight':'session9-open-001/session9-preflight-001.stdout','last_job_exit_code':0,'last_job':'session9-manual-001','active_job_started_by_this_session':False,'fresh_check_required_before_next_EC2':True},
 'source_inventory_checks':checks,'scope':{'old_T033_unchanged':True,'protected_unchanged':True,'LOG_append_only':True,'STATE_unchanged':True}}
write(out/'checkpoint.json',checkpoint);write(out/'integrity.json',{'status':'PASS','checks':checks,'old_T033_mismatches':bad,'protected_mismatches':protected})
with log.open('a',encoding='utf-8',newline='\n') as f:
 f.write('\n### Checkpoint sau nén — '+stamp+'\n\n- Lưu `results/T-033/runs/'+name+'/checkpoint.json`, ledger và manifest. Đã đọc scalar của toàn bộ 210 đường/968 điểm khóa; chưa nhận là đọc mọi raw cell hoặc đã hoàn thành phân tích. Bản trích mới, source/hash PASS; không rerun detector. Ba timer phiên9 được cộng một lần vào base phiên8; actual lịch sử vẫn OPEN. Không có job mới đang chờ do phiên này khởi; trạng thái process cuối là lịch sử, trước EC2 tiếp phải kiểm có đo.\n- Còn đọc chi tiết likelihood/theta, factorial, matching, định nghĩa nhóm và hoàn thiện mọi đầu ra/tự kiểm/handoff. Onset vật lý, prior riêng, matching, tác dụng đồ thị còn OPEN. Lệnh cuối và bước tiếp trong checkpoint. Theo chỉ dẫn Minh, sau kiểm hash checkpoint tiếp cùng phiên. Không sửa STATE hoặc nguồn quyết định.\n')
shutil.copyfile(log,out/'LOG.md.after');shutil.copyfile(state,out/'STATE.md.after')
files={str(p.relative_to(ROOT)):meta(p) for p in (ROOT/'results/T-033').rglob('*') if p.is_file() and str(p.relative_to(ROOT)) not in base['old_t033_files'] and p!=out/'manifest.json'}
files[str(log.relative_to(ROOT))]=meta(log);files[str(state.relative_to(ROOT))]=meta(state)
write(out/'manifest.json',{'files':files,'historical_LOG_STATE_snapshots':'LOG.md.after / STATE.md.after'})
for r,m in files.items():assert meta(ROOT/r)==m,r
print(json.dumps({'status':'PASS','checkpoint':str(out.relative_to(ROOT)),'new_processing_charged_s':ledger['new_processing_charged_s'],'remaining_s':ledger['remaining_approved_s'],'files':len(files)},ensure_ascii=False))
