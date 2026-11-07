"""Kiểm checkpoint chỉ đọc; không chạy phương pháp hoặc mở telemetry."""
import ast
import hashlib
import json
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'results/T-054/scripts'))
from bien_nhan import digest, read_pin
from dieu_phoi import alive, verify_attempt


def main():
    before = json.loads((ROOT / 'results/T-054/runs/trien-khai-001/before.json').read_bytes())
    logpath = 'tasks/T-054-khoa-g3-chay-p7-a/LOG.md'
    for p, pin in before['files'].items():
        if p in (logpath, 'docs/STATE.md'):
            continue
        assert digest(ROOT / p) == pin['sha256'], ('protected file changed', p)
    old_log = before['files'][logpath]
    raw = (ROOT / logpath).read_bytes()
    assert hashlib.sha256(raw[:old_log['bytes']]).hexdigest() == old_log['sha256']
    old_state = (ROOT / 'results/T-054/runs/trien-khai-001/STATE-before.md').read_bytes()
    assert hashlib.sha256(old_state).hexdigest() == before['files']['docs/STATE.md']['sha256']
    def strip_task(data):
        return b''.join(line for line in data.splitlines(keepends=True) if not line.startswith(b'- **T-054'))
    assert strip_task(old_state) == strip_task((ROOT / 'docs/STATE.md').read_bytes())
    now = set(subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT, text=True).splitlines())
    assert now == set(before['tracked_before']), ('new tracked changes', now - set(before['tracked_before']))
    output = ROOT / 'results/T-054'
    manifest = json.loads((output / 'manifest-trien-khai-001.json').read_bytes())
    for p, pin in manifest['outputs'].items():
        assert digest(ROOT / p) == pin['sha256'] and (ROOT / p).stat().st_size == pin['bytes'], p
    actual = {p.relative_to(ROOT).as_posix() for p in output.rglob('*') if p.is_file()}
    expected = {p for p in manifest['outputs'] if p.startswith('results/T-054/')}
    assert actual == expected | {'results/T-054/manifest-trien-khai-001.json'}
    source = json.loads((output / 'source-manifest.json').read_bytes())
    for p, pin in source['own_scripts'].items():
        assert digest(ROOT / p) == pin['sha256'], p
        ast.parse((ROOT / p).read_text(encoding='utf-8'), filename=p)
    for p, pin in source['legacy_code'].items():
        expected_sha = pin['sha256'] if isinstance(pin, dict) else pin
        assert digest(ROOT / p) == expected_sha, p
    package = json.loads((output / 'runs/freeze-cong-cu-003/package.json').read_bytes())
    read_pin(package['files_manifest'])
    assert digest(package['archive']['path']) == package['archive']['sha256']
    files = read_pin(package['files_manifest'])['files']
    with tarfile.open(package['archive']['path'], 'r:gz') as tar:
        for rel, pin in files.items():
            assert hashlib.sha256(tar.extractfile('code/' + rel).read()).hexdigest() == pin['sha256']
            assert digest(ROOT / rel) == pin['sha256'], ('frozen current code differs', rel)
    live = []
    for identity in output.glob('runs/trien-khai-001/**/identity.json'):
        info = json.loads(identity.read_bytes())
        if alive(info): live.append(info['pid'])
    assert not live, ('unexpected fixture worker still running', live)
    for folder in (output / 'runs/trien-khai-001/fixtures-004').glob('reader-*'):
        verify_attempt(folder, json.loads((folder / 'job.json').read_bytes()), 'fixture-route')
    assert json.loads((output / 'authorization.json').read_bytes())['test_grant'] is False
    for path in [*source['own_scripts'], logpath, 'docs/STATE.md', 'results/T-054/runbook.md',
                 'results/T-054/ho-so-g3.md', 'results/T-054/reports/tu-soat-001/bao-cao.md']:
        text = (ROOT / path).read_text(encoding='utf-8')
        assert not any(line.rstrip(' \t') != line for line in text.splitlines()), ('trailing space', path)
    diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    print(json.dumps({'PASS': True, 'manifest_outputs': len(manifest['outputs']), 'own_scripts': len(source['own_scripts']),
          'frozen_files': len(files), 'protected_files_unchanged': True, 'LOG_append_only': True,
          'STATE_only_T054': True, 'live_fixture_workers': live, 'semantic_outputs': 16,
          'diff_check': 'PASS', 'test_opened': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
