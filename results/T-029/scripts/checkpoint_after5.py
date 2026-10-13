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
from p3.selector import nap_allowlist, chon_ca
allowlist=nap_allowlist(ROOT/'results/T-022/allowlist-dev.json')
data_files=sum(len(chon_ca(allowlist,oid,ROOT,kiem_hash=True)) for oid in allowlist)
checks['V1_final_laptop_30cases_89files']=len(allowlist)==30 and data_files==89
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
newrow='| T-029 | P4: hạn chế phát hiện chế độ (b) | P4 | Codex | Claude | Checkpoint sau bước 5 (09/10): bước 0–6 xong, V1–V7 đã kiểm, EC2 đã chép/hash. Còn bước 7–8/V8; chưa chờ phản biện. Đọc cuối LOG | `tasks/T-029-p4-han-che-phat-hien/` |\n'
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
**Kết thúc phiên 6 / checkpoint sau bước 5 theo chỉ dẫn Minh:**
1. **Đã làm:** phiên 6 kiểm lại checkpoint laptop; xác nhận chuỗi EC2 đã hoàn tất, xuất và chép đủ kết quả, kiểm hash hai phía. Nối nhãn vào 90 dòng đặc trưng đã đóng băng; hoàn thành bảng A/N/B/E/P2, V5/V7 và bảng G. Toàn task đã hoàn thành bước 0–6, gồm N-Sigma 47 cặp mới + 13 cặp cũ và P1 theo quy tắc N/A Minh duyệt. Giữ mọi lượt cũ. Ngữ cảnh đã nén, dừng tại điểm cắt sau bước 5 theo Minh và AGENTS 5a; chưa làm bước 7–8.
2. **File thay đổi:** chỉ results/T-029/, LOG nối thêm và dòng T-029 trong STATE. Danh sách/hash đầy đủ ở results/T-029/runs/checkpoint-after5-001/manifest.json. Phiên 6 không sửa SPEC, REVIEW, src, data, DECISIONS, WHY, kết quả task khác, key hoặc known_hosts. Không commit/push hoặc bật/tắt EC2.
3. **Kiểm:** V1 cuối laptop đủ 30 ca/89 tệp và 20 tệp src khớp; V1 cuối EC2 cũng đạt. V2 đủ 60/60; V3/V4 đạt; V5 kiểm 90 dòng/2.700 giá trị, 0 lệch; V6 tổng hợp có đáp án đã đạt; V7 đủ miền hợp lệ và mẫu số theo từng w, còn phải diễn giải khi báo cáo. G có 240 dòng, 960 đối chiếu số A/B, 0 lệch. Copy EC2 đủ 2.896 tệp, hash/kích thước hai phía khớp; I1/I2 mỗi lượt 30 ca, I3 đủ 60 cặp/360 bản ghi. Đã chép về và kiểm hash xong; EC2 có thể tắt. Minh tự tắt. V8 chưa chạy.
4. **Còn mở:** D (thời lượng lỗi) chưa có nguồn xác nhận; không chấm lại P/R/F1. Cờ liên hệ chưa là nguyên nhân. Cần bước 7 đọc tay, xét giải thích khác và V7 trước khi viết HP-n/C1–C6. Chưa hoàn thành task, chưa chờ phản biện. Lỗi stdout cp1252 khi in tên nhóm đã ghi LOG, chỉ đổi cách in sang JSON ASCII; không có phép kiểm khoa học lệch.
5. **Bước tiếp chính xác:** mở phiên mới bằng câu: "Đọc AGENTS.md, làm tiếp T-029 từ checkpoint sau bước 5; hoàn thành bước 7–8 theo SPEC đã khóa." Đọc AGENTS.md, docs/STATE.md, toàn SPEC, mục cuối LOG và runs/checkpoint-after5-001/manifest.json; kiểm file/hash đã có. Lệnh đọc: `Get-Content results/T-029/theo-ca.json -Raw` và `Get-Content results/T-029/runs/step5-001/V7.json -Raw`. Bước 7 chọn ca theo mã mờ nhỏ nhất, ít nhất 2 ca mỗi cơ chế/tổ hợp nếu có, mọi S/D0/không phân biệt V7; ghi quy tắc và danh sách trước khi đọc tay. Không chạy lại máy/NS/P1/đặc trưng/bước 5/G. Sau bước 7, viết các báo cáo bước 8 và V8 đối chiếu mọi số MD với JSON. Đọc docs/review-prompt.md, chép nguyên văn Prompt chung và khối G2 vào cuối LOG, chỉ điền thông tin trung tính cho Claude. Sau V8 mới cập nhật dòng T-029 thành chờ phản biện.
6. **Lệnh cuối có ghi:** D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -W ignore results/T-029/scripts/checkpoint_after5.py (script này). Sau đó chỉ đọc STATE/LOG/diff để bàn giao. Môi trường theo results/T-031/moi-truong.json→lenh_chay; PYTHONDONTWRITEBYTECODE=1, PYTHONPATH=D:/RCA-ext/src/RCAEval;D:/RCA-ext/src/baro;D:/RCA-ext/work/T-014/CIRCA;D:/RCA-flashticket/src; luôn -B.

Đề xuất nội dung commit khi Minh yêu cầu: "T-029: lưu chuỗi can thiệp và phân tích hạn chế phát hiện bước 0–6". Chưa thực hiện commit; task còn bước 7–8.
'''
with LOG.open('a',encoding='utf-8') as f:f.write('\n'+ending)
print(json.dumps({'status':manifest['status'],'checks':checks,'files':len(manifest['files'])}))
