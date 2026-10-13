"""Minh's updated cut: finish independent laptop steps, leave EC2 tmux running."""
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/T-029'
RUN=OUT/'runs/checkpoint-laptop-001'
LOG=ROOT/'tasks/T-029-p4-han-che-phat-hien/LOG.md'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def log(s):
    with LOG.open('a',encoding='utf-8') as f:f.write('\n- '+datetime.now().astimezone().isoformat()+' — Checkpoint laptop: '+s+'\n')
def outside(data):
    return b''.join(b'diff --git '+p for p in data.split(b'diff --git ')[1:]
                    if not p.startswith(b'a/docs/STATE.md b/docs/STATE.md') and not p.startswith(b'a/docs/WHY.md b/docs/WHY.md'))

log('Lệnh có ghi: D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -W ignore results/T-029/scripts/checkpoint_laptop.py; kiểm laptop hoàn tất, ghi checkpoint/LOG/dòngSTATE; giữ EC2 chạy.')
assert not RUN.exists()
base=read(OUT/'runs/buoc0-001/manifest.json')
src=sorted((ROOT/'src/p3').rglob('*.py')); total=hashlib.sha256()
for p in src:total.update(p.read_bytes())
per={p.relative_to(ROOT).as_posix():sha(p) for p in src}
checks={'src_aggregate':total.hexdigest()==base['src_p3']['tong'],'src_per_file':per==base['src_p3']['tep']}
checks.update({p:sha(ROOT/p)==h for p,h in base['nguon'].items()})
spec=(ROOT/'tasks/T-029-p4-han-che-phat-hien/SPEC.md').read_text(encoding='utf-8')
block=spec.split('```markdown\n',1)[1].split('\n```',1)[0]
checks['WHY_only_exact_append']=(ROOT/'docs/WHY.md').read_bytes()==(OUT/'runs/buoc0-001/WHY-truoc.md').read_bytes()+('\n\n'+block+'\n').encode()
checks['tracked_diff_outside_STATE_WHY_unchanged']=outside(subprocess.check_output(['git','diff'],cwd=ROOT))==outside((OUT/'runs/buoc0-001/git-diff-truoc.patch').read_bytes())
old=read(OUT/'runs/checkpoint-p1-001/manifest.json')['files']
saved={p:v for p,v in old.items() if any(s in p for s in ('/runs/nsigma-001/','/runs/proxy-001/','/runs/ec2-dung-001/'))}
checks['all_previous_stopped_runs_preserved']=all(sha(ROOT/p)==v['sha256'] for p,v in saved.items())
ns=read(OUT/'runs/nsigma-002/manifest.json')
checks['NS_run_PASS']=ns['status']=='PASS' and ns['V2']['status']=='PASS' and ns['V2']['so_cap']==60
checks['NS_output_hashes']=all(sha(OUT/'runs/nsigma-002'/p)==h for p,h in ns['output_sha256'].items())
bd=read(ROOT/'results/T-025/bao-dong.json')['bo_phat_hien']
v2=[]
for oid,case in ns['cases'].items():
    for det,r in case['bo'].items():
        p=ROOT/r['npz']; assert sha(p)==r['sha256']
        with np.load(p,allow_pickle=False) as z:
            assert z['Z'].dtype==bool and z['Z'].shape==(1441,r['d'])
            assert np.array_equal(z['times']-z['times'][0],np.arange(1441))
            actual=z['times'][np.flatnonzero(z['Z'].any(axis=1))].astype(int).tolist()
            equal=actual==bd[det][oid]['alarms'] and z['columns'].tolist()==bd[det][oid]['detector_columns']
            actual_first=actual[0] if actual else None
            equal=equal and actual_first==bd[det][oid]['luot_rca']['t_hat']
        v2.append({'opaque_id':oid,'detector':det,'match':bool(equal)})
checks['V2_independent_60']=len(v2)==60 and all(x['match'] for x in v2)
nf=read(OUT/'features-no-label/nsigma/manifest.json')
checks['NS_features_60']=nf['status']=='PASS' and sum(len(v) for v in nf['cases'].values())==60
checks['NS_feature_hashes']=all(sha(ROOT/v['path'])==v['sha256'] for ds in nf['cases'].values() for v in ds.values())
bf=read(OUT/'runs/bocpd-features-001/manifest.json')
checks['B_features_30']=bf['status']=='PASS' and len(bf['cases'])==30
checks['B_feature_hashes']=all(sha(ROOT/p)==h for p,h in bf['outputs'].items())
pv=read(OUT/'runs/proxy-002/verification.json'); pm=read(OUT/'runs/proxy-002/manifest.json')
checks['P1_30cases']=pm['status']=='PASS' and pm['cases']==30 and pv['status']=='PASS' and pv['cohort_minute_rows']==780
checks['P1_hashes']=all(sha(ROOT/p)==h for p,h in pm['outputs'].items())
proof=read(OUT/'runs/resume-ec2-002/v3/transfer-check.json')
checks['V3']=proof['status']=='PASS' and proof['V3']['status']=='PASS'
state=ROOT/'docs/STATE.md'; text=state.read_text(encoding='utf-8')
oldrow=next(x for x in text.splitlines(keepends=True) if x.startswith('| T-029 |'))
checks['STATE_only_T029']=text.replace(oldrow+'\n','',1)==(OUT/'runs/buoc0-001/STATE-truoc.md').read_text(encoding='utf-8')
assert all(checks.values()),{k:v for k,v in checks.items() if not v}
RUN.mkdir()
(RUN/'remote-status.txt').write_bytes((OUT/'runs/checkpoint-live-002/remote-status.txt').read_bytes())
rawrow=next(x for x in state.read_bytes().splitlines(keepends=True) if x.startswith(b'| T-029 |'))
newrow='| T-029 | P4: hạn chế phát hiện chế độ (b) | P4 | Codex | Claude | Checkpoint laptop 08/10 theo Minh: V2 60/60, bước4/P1 xong; EC2 chuoi-002 còn chạy. Chờ I1/I2/I3 rồi bước5/7/8; đọc cuối LOG | `tasks/T-029-p4-han-che-phat-hien/` |\n'
ending=b'\r\n' if rawrow.endswith(b'\r\n') else b'\n'
state.write_bytes(state.read_bytes().replace(rawrow,newrow.rstrip('\n').encode()+ending,1))
checks['STATE_only_T029_after']=state.read_text(encoding='utf-8').replace(newrow+'\n','',1)==(OUT/'runs/buoc0-001/STATE-truoc.md').read_text(encoding='utf-8')
assert checks['STATE_only_T029_after']
for name,cmd in [('git-diff.patch',['git','diff']),('git-status.txt',['git','status','--short'])]:
    (RUN/name).write_bytes(subprocess.check_output(cmd,cwd=ROOT))
manifest={'task':'T-029','status':'CHECKPOINT_LAPTOP_DONE_EC2_RUNNING','time':datetime.now().astimezone().isoformat(),
          'checks':checks,'V2_independent':v2,'features_no_label_count':90,'src_p3':{'tong':total.hexdigest(),'tep':per},
          'completed_steps':[0,1,'2a',3,4,6],'remaining':['2b/2c/2d (check actual EC2 status)','5','7','8','V4','V5','V7','V8'],
          'EC2':'Running in tmux, not stopped or switched off; see remote-status.txt recorded separately.',
          'next_commands':[
           "ssh -i D:/RCA-ext/keys/key2.pem ubuntu@3.26.62.217 'tail -n 30 ~/rca/T-029/trang-thai.txt'",
           "ssh -i D:/RCA-ext/keys/key2.pem ubuntu@3.26.62.217 'cat ~/rca/T-029/runs/chuoi-002/ket-thuc.json'",
           'After PASS, upload/run scripts/export_completed.py with readonly T025 main python -B, writes only T029/export-complete-002.',
           'Copy artifacts.tar.gz/export-check.json from T029/export-complete-002 to results/T-029/runs/ec2-complete-002; run verify_ec2_transfer.py -B.',
           'Only after transfer PASS, run analyze_step5.py --ec2 results/T-029/runs/ec2-complete-002/artifacts.',
           'Run compare_rca.py --ec2-root results/T-029/runs/ec2-complete-002/artifacts --chain-run chuoi-002 --confirm-i3-pass.'],
          'prepared_not_executed':['analyze_step5.py','verify_flags_independent.py','compare_rca.py','export_completed.py','verify_ec2_transfer.py','checkpoint_after5.py'],
          'P1_duration':'OPEN/norescore','scope':'Only T029 results/LOG and T029 STATE row; SPEC locked.',
          'files':{p.relative_to(ROOT).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(OUT.rglob('*')) if p.is_file()}}
(RUN/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
log('Kiểm cuối PASS; root kiểm lại V2 60NPZ trùng tuyệt đối,90feature/hash vàP1đạt, src/SPEC/nguồn vàlượt001giữnguyên; STATEchỉdòngT029. Manifestlaptopđãghi. EC2vẫntiếptục, chưacopytoànchuỗi.')
report='''
**Kết thúc phiên 5 / phục hồi phiên 4 sau usage limit và checkpoint laptop theo Minh:**
1. **Đã làm:** tự kiểm các lời Claude từ dữ liệu dev qua SHA. Ghi duyệt P1 N/A và cách dừng theo phụ thuộc. Hoàn thành 47 cặp N-Sigma mới, dùng lại 13 cặp cũ; V2 đủ 60/60. Bước 4 lưu 90 đặc trưng không nhãn. P1 đủ 30 ca, cả hai Nv. EC2 đã đạt V3 và wrapper50, vẫn tiếp tục chuỗi. Mã bước 5/G/V5/copy đã chuẩn bị, chưa chạy. Kết thúc phiên theo yêu cầu của Minh về usage, không ngắt EC2.
2. **File thay đổi:** chỉ results/T-029/, LOG nối thêm và dòng T-029 trong STATE. Danh sách/hash ở results/T-029/runs/checkpoint-laptop-001/manifest.json. Phiên 4–5 không sửa SPEC/REVIEW/src/data/DECISIONS/WHY, kết quả task khác, key/known_hosts hoặc lượt cũ. Không commit, push, bật hoặc tắt EC2.
3. **Kiểm đã chạy:** V1 dữ liệu EC2 đạt 30 ca/89 tệp, 20 file src đầu–cuối trùng. Root đọc lại 60 NPZ: OR, t_hat và cột khớp T-025. V3 replay và số cột 30/30 đạt; wrapper50 đạt. V6 N-Sigma/BOCPD và 29 phép thử giả bước 5 đạt. Hash 90 đặc trưng đạt. P1 kiểm 3.628 phép trên 780 dòng Nv-phút đạt. V4/V5/V7 dev/V8 và bước 5/G/7/8 chưa chạy. Mới chép 4 artifact V3 và kiểm hash 4/4; chưa xuất/chép toàn chuỗi 002. Chưa báo EC2 có thể tắt.
4. **Còn mở:** đợi I1/I2/V4/I3 trên EC2. V1–V4 lệch thì dừng và báo Minh, không tự sửa. D (thời lượng lỗi) vẫn OPEN; không chấm lại P/R/F1. Cờ chỉ là liên hệ; chưa có kết luận HP/C1–C6. Task chưa xong, chưa chờ phản biện.
5. **Bước tiếp chính xác:** đọc AGENTS/STATE/toàn SPEC/cuối LOG và manifest checkpoint; kiểm đầu ra có sẵn. Không chạy lại bước 0/WHY/N-Sigma/P1/đặc trưng hoặc tạo chuỗi EC2 trùng. Xem trang-thai.txt và ket-thuc.json của chuoi-002 bằng hai lệnh trong manifest. Khi chuỗi PASS và tmux T-029 đã thoát, dùng export_completed.py, chép về rồi chạy verify_ec2_transfer.py như đã ghi trong manifest. Mọi ghi EC2 chỉ trong T-029; data T-031 và env T-025 chỉ đọc. Chép và kiểm hash xong mới báo: 'Đã chép về và kiểm hash xong; EC2 có thể tắt.' Sau đó chạy bước 5/G, V5/V7 theo lệnh trong manifest, rồi bước 7/8/V8. Sau bước 8 mới chép nguyên văn Prompt chung và khối G2 của docs/review-prompt.md cho Claude, không gợi ý kết luận.
6. **Lệnh cuối có ghi:** D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B -W ignore results/T-029/scripts/checkpoint_laptop.py. Sau đó chỉ đọc LOG/STATE/diff/process để bàn giao. Môi trường và PYTHONPATH đúng results/T-031/moi-truong.json→lenh_chay, luôn -B. Tiến độ remote đã đọc được lưu ở checkpoint-laptop-001/remote-status.txt; phiên sau phải xem lại trạng thái thực tế vì EC2 tiếp tục chạy.
'''
with LOG.open('a',encoding='utf-8') as f:f.write('\n'+report)
print(json.dumps({'status':manifest['status'],'V2':len(v2),'features':90,'checks':all(checks.values()),'files':len(manifest['files'])}))
