"""Bước 0 T-029: ghi nguồn, nối WHY đã duyệt, kiểm allowlist; không sửa nguồn."""
import hashlib
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-029'
LOG = ROOT / 'tasks/T-029-p4-han-che-phat-hien/LOG.md'
RUN = OUT / 'runs/buoc0-001'

def stamp():
    return datetime.now(ZoneInfo('Asia/Saigon')).isoformat(timespec='seconds')

def log(msg):
    with LOG.open('a', encoding='utf-8', newline='') as f:
        f.write(f'\n- {stamp()} — {msg}\n')

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def main():
    log('Lệnh có ghi: chạy results/T-029/scripts/buoc0.py bằng T-014-main python -B -W ignore. Tạo runs/buoc0-001/manifest.json và snapshot nguồn trước phiên; nối WHY-39, thêm duy nhất dòng T-029 vào STATE; kiểm SHA allowlist. Script chỉ ghi phạm vi đã duyệt.')
    RUN.mkdir(parents=True, exist_ok=False)
    spec = (ROOT / 'tasks/T-029-p4-han-che-phat-hien/SPEC.md').read_text(encoding='utf-8')
    why_block = spec.split('```markdown\n', 1)[1].split('\n```', 1)[0]
    assert why_block.startswith('## WHY-39.')
    why = ROOT / 'docs/WHY.md'
    state = ROOT / 'docs/STATE.md'
    for p in (why, state):
        (RUN / (p.stem + '-truoc.md')).write_bytes(p.read_bytes())
    (RUN / 'git-status-truoc.txt').write_bytes(subprocess.check_output(['git', 'status', '--short'], cwd=ROOT))
    (RUN / 'git-diff-truoc.patch').write_bytes(subprocess.check_output(['git', 'diff'], cwd=ROOT))
    pys = sorted((ROOT / 'src/p3').rglob('*.py'), key=lambda p: p.relative_to(ROOT).as_posix())
    agg = hashlib.sha256()
    sources = {}
    for p in pys:
        agg.update(p.read_bytes())
        sources[p.relative_to(ROOT).as_posix()] = sha(p)
    m = {'task': 'T-029', 'bat_dau': stamp(), 'src_p3': {'tong': agg.hexdigest(), 'tep': sources},
         'nguon': {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p) for p in (
             ROOT / 'tasks/T-029-p4-han-che-phat-hien/SPEC.md',
             ROOT / 'docs/DECISIONS.md', ROOT / 'results/T-022/allowlist-dev.json',
             ROOT / 'results/T-025/bao-dong.json', ROOT / 'results/T-031/moi-truong.json')},
         'V1': {'status': 'RUNNING', 'tep': []}, 'lenh': 'T-014-main/Scripts/python.exe -B -W ignore results/T-029/scripts/buoc0.py'}
    def save():
        (RUN / 'manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    save()
    with why.open('rb') as f:
        assert b'## WHY-39.' not in f.read(), 'WHY-39 đã có: dừng, không nối trùng'
    log('Bước 0: chuẩn bị nối nguyên văn khối WHY-39 từ Phụ lục SPEC vào cuối docs/WHY.md, không sửa byte cũ.')
    with why.open('ab') as f:
        f.write(('\n\n' + why_block + '\n').encode('utf-8'))
    assert why.read_bytes().startswith((RUN / 'WHY-truoc.md').read_bytes())
    assert why.read_text(encoding='utf-8').endswith(why_block + '\n')
    log('Bước 0: đã nối WHY-39 nguyên văn, kiểm prefix byte cũ và suffix khối SPEC đạt. Không đổi mục cũ.')
    before = state.read_bytes()
    assert b'| T-029 |' not in before
    row = '| T-029 | P4: hạn chế phát hiện chế độ (b) | P4 | Codex | Claude | Đang làm bước 0; SPEC đã duyệt 08/10 (Q-86), khóa; LOG ghi duyệt và đổi vai | `tasks/T-029-p4-han-che-phat-hien/` |\n'
    marker = b'\n## Task '
    pos = before.index(marker)
    log('Bước 0: chuẩn bị thêm dòng T-029 vào bảng STATE; giữ mọi byte khác của STATE.')
    state.write_bytes(before[:pos].rstrip(b'\r\n') + b'\n' + row.encode('utf-8') + b'\n' + before[pos:])
    # So sánh văn bản để xác nhận thay đổi chỉ là thêm dòng đã duyệt.
    assert state.read_text(encoding='utf-8').replace(row + '\n', '', 1) == before.decode('utf-8').replace('\r\n', '\n')
    log('Bước 0: đã thêm duy nhất dòng T-029 trong STATE; kiểm phần còn lại trùng. Hash src/p3 đầu phiên đã lưu manifest; các tệp Nezha có sẵn được tính vào hash và không sửa.')
    from p3.selector import nap_allowlist, chon_ca
    al = nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
    for oid in sorted(al):
        files = chon_ca(al, oid, ROOT, kiem_hash=True)
        for name, path in files.items():
            m['V1']['tep'].append({'opaque_id': oid, 'tep': name, 'sha256': sha(Path(path)), 'bytes': Path(path).stat().st_size})
        save()
        log(f'V1 SHA allowlist: {oid}, {len(files)} tệp khớp guard; chỉ đọc đúng đường dẫn dev trong allowlist.')
    m['V1']['status'] = 'PASS'
    m['V1']['so_ca'] = len(al)
    m['V1']['so_tep'] = len(m['V1']['tep'])
    m['ket_thuc'] = stamp()
    save()
    log(f'Bước 0 xong: V1 allowlist PASS {len(al)} ca/{len(m["V1"]["tep"])} tệp. Manifest runs/buoc0-001/manifest.json. Chưa kiểm hash cuối phiên.')
    print(json.dumps({'V1': 'PASS', 'so_ca': len(al), 'so_tep': len(m['V1']['tep']), 'src_p3_so_tep': len(sources)}, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        log(f'DỪNG bước 0: {type(exc).__name__}: {exc}. Không tự xử lý; giữ nguyên đầu ra đã ghi, báo Minh.')
        raise
