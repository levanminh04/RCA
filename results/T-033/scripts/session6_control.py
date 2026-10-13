"""Laptop metadata, transport and timing only; no research calculations."""
import argparse, hashlib, json, pathlib, subprocess, time, datetime, sys

ROOT=pathlib.Path(__file__).resolve().parents[3]
OPEN=ROOT/'results/T-033/runs/session6-open-001'
PYTHON='/home/ubuntu/rca/T-025/envs/main/bin/python'
SSH=['ssh','-i','D:/RCA-ext/keys/keys.pem','-o','UserKnownHostsFile='+str(ROOT/'results/T-033/runs/prepare-001/known_hosts'),'-o','StrictHostKeyChecking=yes','-o','BatchMode=yes','-o','ConnectTimeout=20','ubuntu@3.107.246.249']
def sha(p):
 h=hashlib.sha256()
 with pathlib.Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def write(p,j): p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(): return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
def open_session():
 OPEN.mkdir(exist_ok=False)
 paths=['AGENTS.md','docs/STATE.md','docs/DECISIONS.md','docs/WHY.md','docs/MRP.md','docs/LESSONS.md','docs/review-prompt.md','tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md','tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md']
 baseline={}
 for rel in paths:
  p=ROOT/rel; b=p.read_bytes(); baseline[rel]={'sha256':sha(p),'bytes':len(b)}
  q=OPEN/'before'/rel; q.parent.mkdir(parents=True,exist_ok=True); q.write_bytes(b)
 write(OPEN/'baseline.json',baseline)
 for name in ('nsigma_delay.py','bocpd_delay.py','channel_context.py','bocpd_core.py','lock_groups.py'):
  p=ROOT/'results/T-033/scripts'/name; q=OPEN/'scripts'/name; q.parent.mkdir(exist_ok=True); q.write_bytes(p.read_bytes())
 log=ROOT/'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'
 with log.open('ab') as f:
  f.write(('\n\n## Phiên 6 — '+stamp()+' — Codex — laptop Windows 11 và EC2 T-033 — Người làm\n\n- Intent EXECUTE: tiếp chặng tính theo SPEC và Q-132. Codex làm, Claude phản biện. Chỉ dùng repo; đã đọc AGENTS/STATE/toàn SPEC/LOG phiên 3–5 và bổ sung. Không nghiên cứu mới trước tự kiểm nguồn/process/hash/ledger và điều phối.\n- Phạm vi: results/T-033/, LOG chỉ nối, duy nhất dòng T-033 STATE, EC2 ~/rca/T-033/. Giữ mọi lượt cũ. Không SPEC/WHY/DECISIONS, T-032, test/locked/heldout, cài package, commit/push hoặc bật/tắt EC2.\n- Q-132: hạch toán cũ 28800 giây là dự phòng chưa kiểm, không là thời gian thực tế; tối đa 14400 giây xử lý mới. Ledger lịch sử bất biến. Mọi lệnh EC2 mới gồm lỗi/kiểm được đo toàn thời gian lệnh SSH làm upper bound bảo thủ cho xử lý từ trước import tới sau exit; ngân sách không dựa lịch hoặc subtotal status.\n- Runtime Python tài liệu cũ D:/RCA-ext/envs/T-014-main không còn chạy được; py/python không có trong PATH. Dùng runtime Python bundled chỉ cho metadata/hash/transport/tài liệu laptop; EC2 Python pin giữ nguyên.\n- Một trợ lý chỉ đọc hỗ trợ soát điều phối; không là phản biện chính thức và không thay tự kiểm Codex. Baseline tại session6-open-001/baseline.json.\n').encode())
 print('OPEN',OPEN)
def remote(name,code):
 # Charge the whole SSH call, including connection overhead and process tails.
 assert not any((OPEN/(name+s)).exists() for s in ('.stdout','.stderr','.timer.json')), 'Refuse overwritten command evidence'
 start=stamp(); t=time.perf_counter()
 p=subprocess.run(SSH+["PYTHONDONTWRITEBYTECODE=1 "+PYTHON+" -B -X utf8 -"],input=code.encode(),capture_output=True)
 wall=time.perf_counter()-t
 (OPEN/(name+'.stdout')).write_bytes(p.stdout); (OPEN/(name+'.stderr')).write_bytes(p.stderr)
 write(OPEN/(name+'.timer.json'),{'started':start,'ended':stamp(),'charged_processing_s':wall,'basis':'full SSH elapsed upper bound; includes imports/process exit/network/control overhead','exit_code':p.returncode,'command':SSH+[PYTHON+' -B -X utf8 -'],'payload_sha256':hashlib.sha256(code.encode()).hexdigest()})
 print(name,'exit',p.returncode,'charged_s',wall)
 print(p.stdout.decode(errors='replace')[:3000]);print(p.stderr.decode(errors='replace')[:1000])
 return p
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['open','remote']);parser.add_argument('--name');parser.add_argument('--code');a=parser.parse_args()
 if a.mode=='open':open_session()
 else:sys.exit(remote(a.name,(ROOT/a.code).read_text(encoding='utf-8')).returncode)
