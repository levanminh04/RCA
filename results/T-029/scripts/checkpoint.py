"""Ghi checkpoint do không kết nối được EC2; chỉ kiểm và kết thúc bước 0."""
import hashlib
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-029'
LOG = ROOT / 'tasks/T-029-p4-han-che-phat-hien/LOG.md'
RUN = OUT / 'runs/buoc0-001'
END = OUT / 'runs/dung-ket-noi-001'

def stamp():
    return datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')

def log(msg):
    with LOG.open('a', encoding='utf-8', newline='') as f:
        f.write(f'\n- {stamp()} — {msg}\n')

def main():
    log('Lệnh có ghi: T-014-main python -B -W ignore results/T-029/scripts/checkpoint.py. Chỉ tạo manifest checkpoint/diff cuối trong results/T-029/runs/dung-ket-noi-001/, cập nhật duy nhất dòng T-029 STATE, thêm mục kết thúc LOG. Không chạy bước nghiên cứu mới hoặc SSH.')
    END.mkdir(parents=True, exist_ok=False)
    before = json.loads((RUN / 'manifest.json').read_text(encoding='utf-8'))
    files = sorted((ROOT / 'src/p3').rglob('*.py'), key=lambda p: p.relative_to(ROOT).as_posix())
    agg = hashlib.sha256()
    hashes = {}
    for p in files:
        b = p.read_bytes()
        agg.update(b)
        hashes[p.relative_to(ROOT).as_posix()] = hashlib.sha256(b).hexdigest()
    checks = {'src_p3_hash_dau_cuoi': agg.hexdigest() == before['src_p3']['tong'],
              'src_p3_tep_dau_cuoi': hashes == before['src_p3']['tep']}
    for rel, expected in before['nguon'].items():
        checks[rel + '_khong_doi'] = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == expected
    spec = (ROOT / 'tasks/T-029-p4-han-che-phat-hien/SPEC.md').read_text(encoding='utf-8')
    block = spec.split('```markdown\n', 1)[1].split('\n```', 1)[0]
    checks['WHY_chi_noi_nguyen_van'] = (ROOT / 'docs/WHY.md').read_bytes() == (RUN / 'WHY-truoc.md').read_bytes() + ('\n\n' + block + '\n').encode('utf-8')
    state = ROOT / 'docs/STATE.md'
    text = state.read_text(encoding='utf-8')
    rows = [line for line in text.splitlines(keepends=True) if line.startswith('| T-029 |')]
    assert len(rows) == 1
    oldrow = rows[0]
    checks['STATE_chi_them_dong_T029'] = text.replace(oldrow + '\n', '', 1) == (RUN / 'STATE-truoc.md').read_text(encoding='utf-8')
    diff_before = (RUN / 'git-diff-truoc.patch').read_bytes()
    diff_final = subprocess.check_output(['git', 'diff'], cwd=ROOT)
    def other_diff(data):
        return b''.join(b'diff --git ' + part for part in data.split(b'diff --git ')[1:]
                        if not part.startswith(b'a/docs/STATE.md b/docs/STATE.md')
                        and not part.startswith(b'a/docs/WHY.md b/docs/WHY.md'))
    checks['diff_tracked_ngoai_STATE_WHY_khong_doi'] = other_diff(diff_before) == other_diff(diff_final)
    assert all(checks.values()), checks
    log('Kiểm cuối đạt: hash tổng và từng tệp src/p3 trùng đầu phiên; SPEC, DECISIONS, allowlist và nguồn T-025/T-031 không đổi; WHY chỉ nối nguyên văn; STATE chỉ thêm dòng T-029; diff tracked ngoài STATE/WHY không đổi so với snapshot trước phiên.')
    newrow = '| T-029 | P4: hạn chế phát hiện chế độ (b) | P4 | Codex | Claude | Dừng sau bước 0 (08/10): V1 đạt; SSH không xác minh được host key EC2; chờ Minh xử lý kết nối. Chưa chạy bước 1–8; checkpoint trong LOG | `tasks/T-029-p4-han-che-phat-hien/` |\n'
    log('Lệnh có ghi: cập nhật duy nhất dòng T-029 STATE thành dừng sau bước 0, chờ Minh xử lý kết nối EC2. Không đổi trạng thái task khác hoặc SPEC.')
    before_state_bytes = state.read_bytes()
    state.write_bytes(before_state_bytes.replace(oldrow.encode('utf-8'), newrow.encode('utf-8'), 1))
    checks['STATE_cap_nhat_dung_mot_dong'] = state.read_text(encoding='utf-8').replace(newrow + '\n', '', 1) == (RUN / 'STATE-truoc.md').read_text(encoding='utf-8')
    assert checks['STATE_cap_nhat_dung_mot_dong']
    manifest = {'task': 'T-029', 'thoi_diem': stamp(), 'status': 'DUNG_KET_NOI_EC2',
                'buoc_da_xong': [0], 'buoc_chua_chay': list(range(1, 9)),
                'ly_do': 'SSH exit 255: No ED25519 host key is known for 3.26.62.217 and you have requested strict checking. Host key verification failed.',
                'EC2': {'host': 'ubuntu@3.26.62.217', 'da_ket_noi': False, 'ghi_remote': False, 'tmux': False},
                'V1': {'allowlist': before['V1'], 'src_p3_cuoi': {'tong': agg.hexdigest(), 'tep': hashes}},
                'kiem_cuoi': checks,
                'log': 'tasks/T-029-p4-han-che-phat-hien/LOG.md',
                'lenh_cuoi_co_ghi': 'T-014-main/Scripts/python.exe -B -W ignore results/T-029/scripts/checkpoint.py'}
    (END / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (END / 'git-diff-cuoi.patch').write_bytes(subprocess.check_output(['git', 'diff'], cwd=ROOT))
    (END / 'git-status-cuoi.txt').write_bytes(subprocess.check_output(['git', 'status', '--short'], cwd=ROOT))
    result_files = sorted(p.relative_to(ROOT).as_posix() for p in OUT.rglob('*') if p.is_file())
    manifest['tep_results_T029'] = result_files
    manifest['hash_dau_ra_ngoai_manifest_nay'] = {
        rel: hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() for rel in result_files
        if rel != (END / 'manifest.json').relative_to(ROOT).as_posix()}
    (END / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    ending = '''
**Kết thúc phiên 1 / checkpoint do điều kiện dừng:**
1. **Đã làm gì:** đọc đầy đủ nguồn được giao; ghi duyệt Q-86 và đổi vai; hoàn tất bước 0; kiểm kết nối EC2 một lần và dừng ngay khi SSH không xác minh được host key. Không chạy bước 1–8. Subagent chỉ khảo sát nguồn, đã ngắt.
2. **File đã thay đổi:** tạo LOG T-029; nối nguyên văn WHY-39 vào docs/WHY.md; thêm/cập nhật duy nhất dòng T-029 trong docs/STATE.md; tạo hai script buoc0.py/checkpoint.py và snapshot/manifest/diff trong results/T-029/runs/buoc0-001/, runs/dung-ket-noi-001/. File set chi tiết và hash nằm trong manifest checkpoint. Giữ mọi thay đổi có trước phiên. Không sửa SPEC/REVIEW/src/data/DECISIONS hoặc kết quả task khác. Không ghi EC2, key hay known_hosts. Không commit.
3. **Kiểm tra đã chạy và kết quả:** V1 SHA allowlist PASS 30 ca/89 tệp; hash tổng và từng tệp src/p3 đầu/cuối trùng; WHY trùng nguyên văn phụ lục và prefix cũ; STATE chỉ đổi dòng T-029; SPEC và nguồn cố định không đổi; diff tracked ngoài STATE/WHY giữ nguyên so với trước phiên. SSH exit 255 vì host key; không xác nhận được kết nối. V2–V8 CHƯA CHẠY, không coi là PASS. Chưa có kết luận C1–C6.
4. **Điều chưa chắc hoặc cần Minh quyết:** cần Minh xác minh host key đúng của EC2 3.26.62.217 và xử lý known_hosts, hoặc cho chỉ dẫn kết nối mới. Không suy IP đã đổi, máy tắt hay key sai từ lỗi host key. Không tự thêm host key hoặc tìm máy khác. Chưa kiểm dữ liệu/env T-025 trên EC2.
5. **Bước tiếp theo chính xác:** chỉ tiếp tục khi Minh giải quyết kết nối và cho làm tiếp. Đọc AGENTS.md, dòng T-029 STATE, toàn SPEC, mục cuối LOG và hai manifest đã lưu; không nối WHY lại hoặc chạy lại buoc0.py. Với kết nối đã được Minh xác nhận, kiểm lại đúng lệnh SSH dưới đây; nếu vẫn lỗi thì dừng ghi LOG. Khi kết nối được, kiểm hash dữ liệu/env T-025 chỉ đọc, chuẩn bị chuỗi 2a→2b→2c→2d trong ~/rca/T-029/ bằng tmux, và các bước laptop đúng phụ thuộc. Chưa có lệnh xem tmux/trang-thai vì chưa tạo phiên EC2.
6. **Lệnh cuối cùng có ghi:** T-014-main/Scripts/python.exe -B -W ignore results/T-029/scripts/checkpoint.py (script này). Kiểm chỉ đọc sau đó: Get-Content LOG -Tail 28; git diff --numstat; git status --short. Các lệnh này chỉ kiểm bàn giao, không thực hiện bước nghiên cứu.

**Lệnh kết nối đã thử, giữ để Minh/phiên sau đối chiếu (không tự chạy lại khi chưa xử lý):**
```powershell
ssh -i D:/RCA-ext/keys/key2.pem -o UserKnownHostsFile=D:/RCA-ext/keys/known_hosts -o StrictHostKeyChecking=yes -o BatchMode=yes -o ConnectTimeout=15 ubuntu@3.26.62.217 uname -n
```

**Trạng thái bàn giao:** dừng có ghi nguyên nhân; chưa xong task, chưa chờ phản biện, chưa được phép báo EC2 có thể tắt vì chưa có kết quả cần chép. Không viết prompt phản biện kết quả khi bước 8 chưa thực hiện.
'''
    with LOG.open('a', encoding='utf-8', newline='') as f:
        f.write('\n' + ending)
    print(json.dumps({'status': manifest['status'], 'kiem_cuoi': checks, 'tep_results_T029': result_files}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
