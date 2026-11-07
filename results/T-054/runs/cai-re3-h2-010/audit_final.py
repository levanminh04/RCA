"""Audit the complete approved patch against checkpoint snapshots."""
from pathlib import Path
import ast
import difflib
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
c = json.loads((RUN/'checkpoint.json').read_text(encoding='utf-8'))
code = c['authorization']['code_files']+c['authorization']['CIRCA_supplement']['files']
docs = c['authorization']['documents']


def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(name, value):
    (RUN/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


for rel, expected in c['before'].items():
    snap = RUN/'before'/rel
    if expected is not None:
        assert pin(snap) == expected, rel
for rel in code:
    ast.parse((ROOT/rel).read_text(encoding='utf-8'))
for rel in ['docs/WHY.md', 'docs/DECISIONS.md', 'tasks/T-054-khoa-g3-chay-p7-a/LOG.md']:
    assert (ROOT/rel).read_bytes().startswith((RUN/'before'/rel).read_bytes()), rel
spec = 'tasks/T-054-khoa-g3-chay-p7-a/SPEC.md'
old = (RUN/'before'/spec).read_text(encoding='utf-8')
new = (ROOT/spec).read_text(encoding='utf-8')
assert all(tag in ('equal', 'insert') for tag, *_ in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes())
for name, files in [('code-diff.patch', code), ('documents-diff.patch', docs)]:
    chunks = []
    for rel in files:
        old_path = RUN/'before'/rel
        a = old_path.read_text(encoding='utf-8').splitlines(keepends=True) if old_path.exists() else []
        b = (ROOT/rel).read_text(encoding='utf-8').splitlines(keepends=True)
        chunks.extend(difflib.unified_diff(a, b, fromfile='before/'+rel, tofile=rel))
    (RUN/name).write_text(''.join(chunks), encoding='utf-8')
previous = json.loads((ROOT/'results/T-054/manifest-cai-ob-source-native-008.json').read_text(encoding='utf-8'))
protected = []
for rel, expected in previous['outputs'].items():
    if rel not in c['before']:
        assert pin(ROOT/rel) == expected, rel
        protected.append(rel)
prior9 = json.loads((ROOT/'results/T-054/manifest-chuan-bi-re3-009.json').read_text(encoding='utf-8'))
for rel, expected in prior9['outputs'].items():
    assert pin(ROOT/rel) == expected, rel
assert pin(RUN/'before/docs/STATE.md') == prior9['mutable_checkpoint']['docs/STATE.md']
for key, expected in prior9['mutable_checkpoint'].items():
    if key.endswith('/LOG.md'):
        assert hashlib.sha256((ROOT/key).read_bytes()[:expected['bytes']]).hexdigest() == expected['sha256']

plan = json.loads((ROOT/'results/T-054/runs/cai-ob-source-native-008/prepared/local-plan.json').read_text(encoding='utf-8'))
pins = next(j['code_pins'] for j in plan['jobs'] if j.get('code_pins'))
current_pins = {}
unchanged, changed = [], []
for rel, expected in pins.items():
    path = Path(rel) if Path(rel).is_absolute() else ROOT/rel
    actual = pin(path)
    current_pins[rel] = actual
    if actual['sha256'] == expected:
        unchanged.append(rel)
    else:
        assert rel in code, rel
        changed.append(rel)
current_pins['src/p3/re3.py'] = pin(ROOT/'src/p3/re3.py')
save('code-binding-candidate.json', {
    'status': 'CANDIDATE_NOT_G3_NOT_EXECUTABLE', 'source': '008 local code pins plus approved010 changes/new reader',
    'files': current_pins, 'code_pins': {k:v['sha256'] for k,v in current_pins.items()},
    'new_cloud_bundle_or_plan_generated': False, 'actual_RE3_profile_or_grant_generated': False})
subprocess.run(['git', 'diff', '--check', '--', *code, *docs], cwd=ROOT, check=True)
save('audit.json', {'code_files': code, 'document_files': docs,
                    'snapshot_pins_verified': True, 'WHY_DECISIONS_LOG_append_only': True,
                    'SPEC_insertions_only': True, 'protected008_outputs_verified': len(protected),
                    'immutable009_outputs_verified': len(prior9['outputs']),
                    'inherited_code_unchanged': len(unchanged), 'inherited_code_approved_changes': changed,
                    'current_code_binding_files': len(current_pins), 'AST': 'PASS', 'diff_check': 'PASS',
                    'new_cloud_or_main_run': False})
print(json.dumps({'PASS': True, 'code_files': len(code), 'protected008': len(protected),
                  'unchanged_inherited_code': len(unchanged), 'current_code_bindings': len(current_pins)}))
