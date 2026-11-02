"""T-046: manifest sha256 của mọi tệp trong `results/T-046/` (trừ chính manifest), cùng `src/m1` (kèm git blob để kiểm
trên checkout CRLF, như T-045) và SPEC T-046. `--kiem`: so lại, báo tệp thiếu, thừa, lệch.
Chạy: $PY -B results/T-046/scripts/tao_manifest.py        (tạo)
      $PY -B results/T-046/scripts/tao_manifest.py --kiem (kiểm)
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = ROOT / 'results/T-046'
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
    out = sorted(p for p in R.rglob('*') if p.is_file() and p != MF and '__pycache__' not in p.parts)
    out += sorted((ROOT / 'src/m1').glob('*.py'))
    out.append(ROOT / 'tasks/T-046-cong-verdict-thang-diem/SPEC.md')
    return out


def rel(p):
    return str(p.relative_to(ROOT)).replace('\\', '/')


def main():
    if '--kiem' in sys.argv:
        mf = json.loads(MF.read_bytes().decode('utf-8'))
        that = {rel(p): p for p in tep()}
        thieu = sorted(set(mf['tep']) - set(that))
        thua = sorted(set(that) - set(mf['tep']))
        lech, khop_blob = [], []
        for k, v in mf['tep'].items():
            if k in that:
                h = sha(that[k])
                if h != v['sha256']:
                    if v.get('git_blob') and git_blob(that[k]) == v['git_blob']:
                        khop_blob.append(k)
                    else:
                        lech.append(k)
        kq = {'so_file_manifest': len(mf['tep']), 'so_file_that': len(that), 'thieu': thieu, 'thua': thua, 'lech': lech,
              'khop_git_blob': khop_blob, 'PASS': not (thieu or thua or lech)}
        print(json.dumps(kq, ensure_ascii=False))
        return
    out = {'tep': {}}
    for p in tep():
        d = {'sha256': sha(p), 'bytes': p.stat().st_size}
        if p.suffix in ('.py', '.md') and 'results' not in p.parts:
            d['git_blob'] = git_blob(p)
        out['tep'][rel(p)] = d
    MF.write_bytes((json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + '\n').encode('utf-8'))
    print('so_file', len(out['tep']))


if __name__ == '__main__':
    main()
