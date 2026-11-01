"""T-045: manifest sha256 của mọi tệp trong `results/T-045/` (trừ chính manifest), cùng `src/m1`, `src/m1_danh_gia` (kèm git
blob để kiểm trên checkout CRLF, như T-044) và SPEC T-045. `--kiem`: so lại, báo tệp thiếu, thừa, lệch.
Chạy: $PY -B results/T-045/scripts/tao_manifest.py        (tạo)
      $PY -B results/T-045/scripts/tao_manifest.py --kiem (kiểm)
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = ROOT / 'results/T-045'
MF = R / 'manifest.json'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def git_blob(p):
    return subprocess.run(['git', 'hash-object', str(p)], cwd=str(ROOT), capture_output=True, text=True).stdout.strip()


def tep():
    out = sorted(p for p in R.rglob('*') if p.is_file() and p != MF)
    out += sorted((ROOT / 'src/m1').glob('*.py')) + sorted((ROOT / 'src/m1_danh_gia').glob('*.py'))
    out.append(ROOT / 'tasks/T-045-chay-khoi-k-dev/SPEC.md')
    return out


def rel(p):
    return str(p.relative_to(ROOT)).replace('\\', '/')


def main():
    kiem = '--kiem' in sys.argv
    if not kiem:
        head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=str(ROOT), capture_output=True, text=True).stdout.strip()
        files = {}
        for p in tep():
            x = {'sha256': sha(p), 'bytes': p.stat().st_size}
            if not rel(p).startswith('results/'):
                x['git_blob'] = git_blob(p)
            files[rel(p)] = x
        MF.write_text(json.dumps({'task': 'T-045', 'git_HEAD': head, 'so_file': len(files), 'files': files},
                                 ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(json.dumps({'so_file': len(files), 'git_HEAD': head}))
        return
    m = json.loads(MF.read_text(encoding='utf-8'))
    that = {rel(p): p for p in tep()}
    thieu = sorted(set(m['files']) - set(that))
    thua = sorted(set(that) - set(m['files']))
    lech, khop_blob = [], []
    for k in sorted(set(m['files']) & set(that)):
        if sha(that[k]) != m['files'][k]['sha256']:
            if m['files'][k].get('git_blob') and git_blob(that[k]) == m['files'][k]['git_blob']:
                khop_blob.append(k)
            else:
                lech.append(k)
    print(json.dumps({'so_file_manifest': len(m['files']), 'so_file_that': len(that), 'thieu': thieu[:20], 'thua': thua[:20],
                      'lech': lech[:20], 'khop_git_blob': khop_blob, 'PASS': not (thieu or thua or lech)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
