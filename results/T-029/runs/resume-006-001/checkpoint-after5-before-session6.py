"""Run only at Minh's approved cut after step5; preserve enough to resume step7."""
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/T-029'
RUN=OUT/'runs/checkpoint-after5-001'
LOG=ROOT/'tasks/T-029-p4-han-che-phat-hien/LOG.md'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def log(s):
    with LOG.open('a',encoding='utf-8') as f: f.write('\n- '+datetime.now().astimezone().isoformat()+' — Checkpoint sau5: '+s+'\n')

log('Lệnh có ghi: T014main Python -B -W ignore checkpoint_after5.py; chỉ chạy sau bước5 đầy đủ, kiểm phạmvi/V1/giữlượt, ghi manifest/diff/status, đổi dòngT029 STATE và kếtthúcLOG.')
assert not RUN.exists()
transfer=read(OUT/'runs/ec2-complete-002/transfer-check.json'); assert transfer['status']=='PASS'
v5=read(OUT/'runs/step5-001/V5.json'); assert v5['status']=='PASS' and v5['mismatch_count']==0
g=read(OUT/'a-so-b.json'); assert g['status']=='PASS' and g['verification']['mismatches']==0
rows=read(OUT/'theo-ca.json')['rows']; assert len(rows)==90
before=read(OUT/'runs/buoc0-001/manifest.json')
files=sorted((ROOT/'src/p3').rglob('*.py')); agg=hashlib.sha256()
for p in files: agg.update(p.read_bytes())
per={p.relative_to(ROOT).as_posix():sha(p) for p in files}
checks={'src_p3_aggregate':agg.hexdigest()==before['src_p3']['tong'],'src_p3_per_file':per==before['src_p3']['tep']}
checks.update({p:sha(ROOT/p)==h for p,h in before['nguon'].items()})
spec=(ROOT/'tasks/T-029-p4-han-che-phat-hien/SPEC.md').read_text(encoding='utf-8')
block=spec.split('```markdown\n',1)[1].split('\n```',1)[0]
checks['WHY_exact_append']=(ROOT/'docs/WHY.md').read_bytes()==(OUT/'runs/buoc0-001/WHY-truoc.md').read_bytes()+('\n\n'+block+'\n').encode()
def outside(data):
    return b''.join(b'diff --git '+p for p in data.split(b'diff --git ')[1:]
                    if not p.startswith(b'a/docs/STATE.md b/docs/STATE.md') and not p.startswith(b'a/docs/WHY.md b/docs/WHY.md'))
checks['tracked_diff_outside_STATE_WHY_unchanged']=outside(subprocess.check_output(['git','diff'],cwd=ROOT))==outside((OUT/'runs/buoc0-001/git-diff-truoc.patch').read_bytes())
prior=read(OUT/'runs/checkpoint-p1-001/manifest.json')['files']
preserve={p:v for p,v in prior.items() if '/runs/nsigma-001/' in p or '/runs/proxy-001/' in p or '/runs/ec2-dung-001/' in p}
checks['prior_stopped_runs_preserved']=all(sha(ROOT/p)==v['sha256'] for p,v in preserve.items())
state=ROOT/'docs/STATE.md'; text=state.read_text(encoding='utf-8')
oldrows=[x for x in text.splitlines(keepends=True) if x.startswith('| T-029 |')]; assert len(oldrows)==1
oldrow=oldrows[0]
checks['STATE_only_T029']=text.replace(oldrow+'\n','',1)==(OUT/'runs/buoc0-001/STATE-truoc.md').read_text(encoding='utf-8')
assert all(checks.values()),checks
RUN.mkdir()
newrow='| T-029 | P4: hạn chế phát hiện chế độ (b) | P4 | Codex | Claude | Đã xong bước0–6; checkpoint sau bước5 theoMinh. V1–V7 đủ bằngchứng, EC2 đãcopy/hash. Còn bước7–8/V8, chưa chờphảnbiện; đọc cuốiLOG | `tasks/T-029-p4-han-che-phat-hien/` |\n'
state_bytes=state.read_bytes()
rawrow=next(x for x in state_bytes.splitlines(keepends=True) if x.startswith(b'| T-029 |'))
line_end=b'\r\n' if rawrow.endswith(b'\r\n') else b'\n'
state.write_bytes(state_bytes.replace(rawrow,newrow.rstrip('\n').encode()+line_end,1))
checks['STATE_only_T029_after_update']=state.read_text(encoding='utf-8').replace(newrow+'\n','',1)==(OUT/'runs/buoc0-001/STATE-truoc.md').read_text(encoding='utf-8')
assert checks['STATE_only_T029_after_update']
(RUN/'git-diff.patch').write_bytes(subprocess.check_output(['git','diff'],cwd=ROOT))
(RUN/'git-status.txt').write_bytes(subprocess.check_output(['git','status','--short'],cwd=ROOT))
manifest={'task':'T-029','status':'CHECKPOINT_AFTER_STEP5','time':datetime.now().astimezone().isoformat(),
          'checks':checks,'src_p3':{'tong':agg.hexdigest(),'tep':per},'V2':'60/60PASS','V3':'PASS','V4':'PASS','V5':v5['mismatch_count'],
          'V7':'reported in runs/step5-001/V7.json','V8':'NOT_STARTED','step7':'NOT_STARTED','step8':'NOT_STARTED',
          'EC2_transfer':transfer,'decisions':'LOG phiên4: P1 N/A, dependency-only stop; SSH default known_hosts/dataT031/envT025.',
          'next':'Read AGENTS, STATE, whole locked SPEC and last LOG. Do not rerun completed machine/feature/step5 jobs. Step7 select opaque IDs by SPEC before manual reading; then step8 reports/V8/review prompt.',
          'files':{p.relative_to(ROOT).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(OUT.rglob('*')) if p.is_file()}}
(RUN/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
log('Kiểm cuối PASS; đã cập nhật đúng dòng T029 STATE và lưu toàn bộ file/hash/diff tại runs/checkpoint-after5-001/manifest.json. Chưa bước7/8/V8, không gọi task xong.')
ending='''
**Kết thúc phiên4 / checkpoint sau bước5 theo chỉ dẫn Minh:**
1. **Đã làm:** kiểm lại raw các lời Claude; ghi quyết định P1 N/A/cách dừng; tiếp tục đúng các lượt mới, giữ001. Hoàn thành bước1–6 gồm chuỗiEC2 V3→I1→I2→V4→I3, NS47mới+13cũ, đặctrưngkhôngnhãn, nối90dòng, V5/V7, P1/P2, bảngG. Dừng tại điểm cắt Minh đã chỉ; chưa đọc tay/báo cáo kết luận.
2. **File thay đổi:** chỉ results/T-029/, LOG nối thêm, dòngT-029 STATE; danh sách/hash đầy đủ ở results/T-029/runs/checkpoint-after5-001/manifest.json. Không sửa SPEC/REVIEW/src/data/DECISIONS/WHY ở phiên4, task khác, key/known_hosts. Không commit/push hoặc bật/tắt EC2.
3. **Kiểm:** V1 nguồn/data khớp; V2 đủ60/60; V3/V4PASS; V5zero mismatch90dòng; V6tổnghợpcóđápánPASS; V7đủmẫusố/miềnhợp lệ, V8chưachạy. Kiểm copy EC2count/SHA/bytes hai phíakhớp, I1/I2 mỗi30ca vàI3 đủ60cặp/360bản ghi. Đã chép về và kiểm hash xong; EC2 có thể tắt. Minh tựtắt. Giữ nguyên mọi lượt dừng/hỏng.
4. **Còn mở:** D thời lượnglỗi chưa có nguồn xác nhận, không chấm lạiP/R/F1. Các cờ liênhệ chưa là nguyênnhân; cần bước7 đọc tay, xét giải thích khác vàV7 trướcviếtHP/C1–C6. Chưa taskxong/chưa chờphảnbiện.
5. **Bước tiếp chính xác:** mở phiên mới, đọc AGENTS/STATE/toànSPEC/cuốiLOG và manifestcheckpoint; kiểm hash đầu ra có sẵn. Đọc theo-ca.json, runs/step5-001/V7.json để chọn ca bước7 theo mãmờ nhỏnhất (>=2 mỗi cơ chế/tổ hợp nếu có), mọiS/D0/khôngphânbiệtV7; ghi quy tắc vàdanhsáchtrướcđọc tay. Không rerun máy. Sau bước7 làm bước8, viết MD+V8soJSON; chép nguyên văn Promptchung vàkhốiG2 của docs/review-prompt.md vào cuốiLOG, điền trung tính choClaude.
6. **Lệnh cuối có ghi:** D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -W ignore results/T-029/scripts/checkpoint_after5.py (script này); sau đó chỉ đọc STATE/LOG/diff để bàn giao. Env/lệnh Python giữ theo results/T-031/moi-truong.json→lenh_chay, luôn -B.
'''
with LOG.open('a',encoding='utf-8') as f:f.write('\n'+ending)
print(json.dumps({'status':manifest['status'],'checks':checks,'files':len(manifest['files'])}))
