"""Kiểm đầu vào đã có; chỉ ghi bằng chứng trong T-047, không đọc nhãn."""
import hashlib
import json
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-047/runs/phien5-tiep-nhan-001'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    before = {}
    paths = ['docs/STATE.md', 'docs/WHY.md', 'docs/DECISIONS.md',
             'tasks/T-047-khoi-k-luot-2/SPEC.md', 'tasks/T-047-khoi-k-luot-2/LOG.md']
    for p in paths:
        target = OUT / 'before' / p
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / p).read_bytes())
        before[p] = sha(target.read_bytes())
    results = []
    for task, rev in [('043', None), ('044', '69ef90b6'), ('045', 'bbef69dd'), ('046', None)]:
        start = time.monotonic()
        p = ROOT / f'results/T-{task}/manifest.json'
        m = json.loads(p.read_text(encoding='utf-8'))
        entries = m.get('outputs', m.get('files', m.get('tep')))
        entries = {x['path']: x for x in entries} if isinstance(entries, list) else entries
        errors, historical = [], []
        for name, entry in entries.items():
            if 'locked' in Path(name).parts:
                raise ValueError('manifest trỏ locked')
            if rev and name.startswith('src/m1/'):
                b = subprocess.check_output(['git', 'show', f'{rev}:{name}'], cwd=ROOT)
                historical.append(name)
                variants = [b, b.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')]
            else:
                variants = [(ROOT / name).read_bytes()] if (ROOT / name).is_file() else []
            if not any(sha(b) == entry['sha256'] for b in variants):
                errors.append(name)
        row = dict(task=task, manifest_sha256=sha(p.read_bytes()), entries=len(entries),
                   historical=historical, errors=errors, seconds=time.monotonic()-start)
        results.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != 'historical'}), flush=True)
    k = json.loads((ROOT / 'results/T-047/kiem-helper.json').read_text(encoding='utf-8'))
    sources = {p: sha((ROOT / p).read_bytes()) == e['sha256'] for p, e in k['sources'].items()}
    suites = []
    for s in k['old_suites']:
        p = ROOT / s['file']
        root = ET.parse(p).getroot()
        tests = list(root.iter('testsuite'))
        suites.append(dict(file=s['file'], hash_ok=sha(p.read_bytes()) == s['sha256'],
                           tests=sum(int(x.get('tests', 0)) for x in tests),
                           failures=sum(int(x.get('failures', 0)) for x in tests),
                           errors=sum(int(x.get('errors', 0)) for x in tests)))
    for s in k['new_regression']['attempts']:
        p = ROOT / s['path'] / 'junit.xml'
        suites.append(dict(file=str(p.relative_to(ROOT)), hash_ok=sha(p.read_bytes()) == s['junit_sha256']))
    src_diff = subprocess.check_output(['git', 'diff', 'c298188e', '--', 'src'], cwd=ROOT)
    status = subprocess.check_output(['git', 'status', '--porcelain=v1', '-uno'], cwd=ROOT)
    (OUT / 'git-status-before.txt').write_bytes(status)
    out = dict(manifests=results, sources=sources, suites=suites, src_diff_empty=not src_diff,
               before=before, PASS=not any(x['errors'] for x in results) and all(sources.values())
               and all(x['hash_ok'] for x in suites) and not src_diff)
    (OUT / 'kiem-tiep-nhan.json').write_text(json.dumps(out, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
    if not out['PASS']:
        raise SystemExit('STOP: hash lệch')


if __name__ == '__main__':
    main()
