"""Finish validation after finalize wrote LOG/STATE; no replay of those mutations."""
from pathlib import Path
import json
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
LOG = ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md'
STATE = ROOT/'docs/STATE.md'


def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


previous = json.loads((ROOT/'results/T-054/manifest-cai-ob-source-native-008.json').read_text(encoding='utf-8'))
unchanged = 0
for rel, expected in previous['outputs'].items():
    if rel == 'docs/STATE.md':
        assert pin(RUN/'before-state.md') == expected
    elif rel == 'tasks/T-054-khoa-g3-chay-p7-a/LOG.md':
        assert hashlib.sha256(LOG.read_bytes()[:expected['bytes']]).hexdigest() == expected['sha256']
    else:
        assert pin(ROOT/rel) == expected, rel
        unchanged += 1
oldlines = (RUN/'before-state.md').read_bytes().splitlines(keepends=True)
newlines = STATE.read_bytes().splitlines(keepends=True)
assert len(oldlines) == len(newlines)
delta = [(a, b) for a, b in zip(oldlines, newlines) if a != b]
assert len(delta) == 1 and all(x.startswith(b'- **T-054') for x in delta[0])
sources = json.loads((RUN/'source-pins.json').read_text(encoding='utf-8'))
for rel, expected in sources['files'].items():
    assert pin(ROOT/rel) == expected, rel
c = json.loads((RUN/'checkpoint.json').read_text(encoding='utf-8'))
c['retained_failures'].append({
    'step': 'second finalize009 validation', 'error': 'historical008 STATE full hash after authorized009 change',
    'mutation_before_failure': '009 LOG append/STATE T054 line and outputs already written',
    'resolution': 'do not replay mutations; validate588 unchanged artifacts, old STATE snapshot and appended LOG prefix separately'})
c['final_validation'] = 'PASS'
c['next_command'] = 'Read bao-cao.md exact H2 proposal and await Minh; do not rerun finalize.py or finish_validation.py'
save(RUN/'checkpoint.json', c)
with LOG.open('a', encoding='utf-8', newline='') as f:
    f.write('\n\n### Kiểm cuối009\n\n27 kiểm synthetic PASS;588 output008 bất biến giữ hash, LOG008 giữ prefix, STATE008 khớp snapshot trước009 và chỉ thay đúng dòng T054. 14 source file trong source-pins giữ nguyên. Lượt finalize đầu dừng do key path Windows; lượt hai đã ghi LOG/STATE rồi dừng ở phép kiểm full hash STATE008; không replay mutation, hoàn tất bằng finish_validation.py và ghi nguyên thất bại trong checkpoint. Manifest009 pin đầu ra mới; không mở telemetry/main hoặc cloud. Lệnh cuối: finish_validation.py, sau đó kiểm manifest009 và git diff --check. Bước tiếp giữ nguyên: chờ quyết định exact patch H2; H1 thiếu nguồn exporter/deployment, không coi là chỉ thiếu cloud.\n')
subprocess.run(['git', 'diff', '--check', '--', 'docs/STATE.md', str(LOG.relative_to(ROOT))], cwd=ROOT, check=True)
save(RUN/'validation.json', {
    'previous008_unchanged_artifacts': unchanged, 'previous008_total_checked': len(previous['outputs']),
    'previous008_LOG_prefix': 'PASS', 'previous008_STATE_before009_snapshot': 'PASS',
    'source_files_unchanged': len(sources['files']), 'STATE_only_T054_line_changed': True,
    'synthetic_checks_PASS': 27, 'diff_check': 'PASS', 'RE3_telemetry_opened': False,
    'main_started': False, 'cloud_paused': True, 'source_decisions_added': False,
    'H1_complete': False, 'H2_implemented': False})
outputs = {str(p.relative_to(ROOT)).replace('\\', '/'): pin(p) for p in sorted(RUN.rglob('*')) if p.is_file()}
save(ROOT/'results/T-054/manifest-chuan-bi-re3-009.json', {
    'schema': 'T054-RE3-PREPARATION-009', 'status': c['status'], 'outputs': outputs,
    'previous_manifest': pin(ROOT/'results/T-054/manifest-cai-ob-source-native-008.json'),
    'mutable_checkpoint': {str(LOG.relative_to(ROOT)).replace('\\', '/'): pin(LOG), 'docs/STATE.md': pin(STATE)},
    'RE3_telemetry_opened': False, 'H2_implemented': False, 'main_started': False,
    'approval_question_pending': True, 'worker': 'Codex', 'reviewer': 'Claude'})
print(json.dumps({'manifest009_outputs': len(outputs), 'previous008_unchanged': unchanged,
                  'mutable_two_validated_separately': True, 'synthetic_checks': 27, 'result': 'PASS'}))
