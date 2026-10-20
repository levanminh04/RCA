from pathlib import Path
import difflib
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


checks = []
def check(label, value, detail=None):
    checks.append({'label': label, 'pass': bool(value), 'detail': detail})


before = read(HERE / 'truoc-sua.json')
targets = {row['path']: row for row in before['targets']}
reports = {'results/T-032/' + n for n in ('nguyen-nhan-xep-hang.md', 'ket-qua-phien-13.md', 'doc-tay.md', 'kiem-tiep.md')}
for rel, row in targets.items():
    check('backup ' + rel, sha(REPO / row['backup']) == row['before_sha256'])
    a = (REPO / row['backup']).read_text(encoding='utf-8').splitlines(keepends=True)
    b = (REPO / rel).read_text(encoding='utf-8').splitlines(keepends=True)
    diff = ''.join(difflib.unified_diff(a, b, fromfile='before/' + rel, tofile='after/' + rel))
    (HERE / (Path(rel).name + '.diff')).write_text(diff, encoding='utf-8')
    result = subprocess.run(['git', '-c', 'core.autocrlf=false', 'diff', '--no-index', '--check', str(REPO / row['backup']), str(REPO / rel)], capture_output=True)
    check('diff whitespace ' + rel, not result.stdout.strip() and not result.stderr.strip(),
          (result.stdout + result.stderr).decode('utf-8', errors='replace'))

combined = ''.join((HERE / (Path(rel).name + '.diff')).read_text(encoding='utf-8') for rel in targets)
(HERE / 'cac-thay-doi.diff').write_text(combined, encoding='utf-8')

for row in before['old_manifest_checks']:
    rel = row['path']
    source = REPO / targets[rel]['backup'] if rel in reports else REPO / rel
    check('old manifest source ' + rel, sha(source) == row['expected'],
          'approved report: use before snapshot' if rel in reports else 'current unchanged output')

for rel in ('tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md', 'docs/DECISIONS.md'):
    check('append-only ' + rel, (REPO / rel).read_bytes().startswith((REPO / targets[rel]['backup']).read_bytes()))

rel = 'docs/STATE.md'
original = (REPO / targets[rel]['backup']).read_text(encoding='utf-8').splitlines()
current = (REPO / rel).read_text(encoding='utf-8').splitlines()
check('STATE only T032 row', [s for s in original if not s.startswith('| T-032 |')] ==
      [s for s in current if not s.startswith('| T-032 |')])

rel = 'tasks/T-032-g2-nguyen-nhan-xep-hang/REVIEW.md'
original = (REPO / targets[rel]['backup']).read_text(encoding='utf-8')
current = (REPO / rel).read_text(encoding='utf-8')
table = '| Điểm | Ý kiến người làm:'
check('REVIEW outside response table unchanged', original.split(table, 1)[0] == current.split(table, 1)[0])
for line in current.split(table, 1)[1].splitlines():
    if re.match(r'^\| [RN]\d+ \|', line):
        check('Minh decision blank ' + line.split('|')[1].strip(), not line.split('|')[-2].strip())

def sections(raw):
    chunks = re.split(br'(?m)(?=^diff --git )', raw)
    result = {}
    for block in chunks:
        if not block.strip():
            continue
        header = block.splitlines()[0]
        name = header.split(b' b/', 1)[1].decode('utf-8').strip('"')
        result[name] = block
    return {k: v for k, v in result.items() if k not in targets}

now = subprocess.run(['git', 'diff', '--binary'], capture_output=True).stdout
check('existing tracked changes outside scope preserved', sections(now) == sections((HERE / 'git-diff-truoc.patch').read_bytes()))

for attempt in (1, 2, 3):
    for row in read(HERE / f'md-partition/attempt-{attempt:03}/manifest.json')['files']:
        check(f'MD manifest {attempt}: ' + row['path'], sha(HERE / 'md-partition' / row['path']) == row['sha256'])
for rel, row in read(HERE / 'md-partition/attempt-003/sources.json').items():
    check('MD source ' + rel, sha(REPO / rel) == row['sha256'])

numeric = sorted((HERE / 'kiem-so').glob('result-after-*.json'))[-1]
nr = read(numeric)
check('412 numeric assertions', nr['n_claims'] == 412 and nr['n_mismatch'] == 0)
nm = read(numeric.with_name(numeric.name.replace('result-', 'manifest-')))
check('numeric result manifest', sha(numeric) == nm['result_sha256'])
check('numeric script manifest', sha(HERE / 'kiem-so/validate_handwritten.py') == nm['script_sha256'])
for row in nm['source_reports']:
    check('numeric report current ' + row['path'], sha(Path(row['path'])) == row['sha256'])
extra = read(HERE / 'kiem-so/kiem-so-bo-sung.json')
check('17 additional assertions', extra['n_checks'] == 17 and extra['n_mismatch'] == 0)
check('extra numbers current doc', extra['doc_sha256'] == sha(REPO / 'results/T-032/doc-tay.md'))
e = read(HERE / 'self-check-phien13-005.json')
check('E 61 no mismatch', e['n_claims'] == 61 and e['mismatch'] == 0)

template = (REPO / 'docs/review-prompt.md').read_text(encoding='utf-8')
blocks = re.findall(r'```text\n(.*?)\n```', template, re.S)
common = next(x for x in blocks if x.startswith('Bạn thực hiện'))
stage = next(x for x in blocks if x.startswith('Công đoạn: người phản biện kiểm lại'))
gate = next(x for x in blocks if x.startswith('Kiểm chuỗi đầu vào'))
prompt = (HERE / 'prompt-codex-kiem-lai.txt').read_text(encoding='utf-8')
first = prompt.split('\n\n' + stage, 1)[0]
field = lambda s: any(s.startswith(k) for k in (
    '- Task hoặc đề xuất:', '- Công đoạn:', '- Gói/cổng:', '- Người làm và người phản biện chính thức:',
    '- Tài liệu gốc:', '- Phản biện và phản hồi trước:', '- Code và kết quả liên quan:',
    '- Phạm vi ghi được Minh cho phép trong lượt này:'))
check('prompt common verbatim outside fields', [s for s in first.splitlines() if not field(s)] ==
      [s for s in common.splitlines() if not field(s)])
check('prompt stage and G2 verbatim', prompt == first + '\n\n' + stage + '\n\n' + gate + '\n')
check('prompt copied to LOG', prompt in (REPO / 'tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md').read_text(encoding='utf-8'))

parsed = 0
for p in HERE.rglob('*.json'):
    if p.name in ('manifest.json', 'kiem-cuoi.json') and p.parent == HERE:
        continue
    read(p)
    parsed += 1
check('package JSON parses', parsed > 0, parsed)

result = {'status': 'PASS' if all(x['pass'] for x in checks) else 'FAIL', 'checks': checks,
          'n_checks': len(checks), 'mismatches': [x for x in checks if not x['pass']],
          'numeric_final': numeric.relative_to(REPO).as_posix(), 'json_files_parsed': parsed,
          'existing_files_changed': list(targets), 'new_output_scope': HERE.relative_to(REPO).as_posix()}
(HERE / 'kiem-cuoi.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
assert result['status'] == 'PASS', json.dumps(result['mismatches'], ensure_ascii=False)

items = []
for p in sorted(HERE.rglob('*')):
    if p.is_file() and p != HERE / 'manifest.json':
        items.append({'path': p.relative_to(REPO).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size})
for rel in targets:
    p = REPO / rel
    items.append({'path': rel, 'sha256': sha(p), 'bytes': p.stat().st_size})
manifest = {'schema': 'T032-approved-review-corrections-v1', 'files': items,
            'self_excluded': (HERE / 'manifest.json').relative_to(REPO).as_posix(),
            'before_snapshot': 'truoc-sua.json', 'verification': 'kiem-cuoi.json',
            'note': 'Old report manifests apply to the preserved before copies; frozen research outputs remain unchanged.'}
(HERE / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'checks': len(checks), 'json_parsed': parsed,
                  'manifest_files': len(items), 'numeric_final': result['numeric_final']}, ensure_ascii=False))
