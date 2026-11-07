"""Kiểm checkpoint và bảo toàn phạm vi; không gọi method hoặc đọc telemetry/nhãn."""
import argparse
import ast
import hashlib
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-002'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def check_pin(path, expected):
    raw = path.read_bytes()
    expected_sha = expected if isinstance(expected, str) else expected['sha256']
    assert sha(raw) == expected_sha, ('hash', str(path))
    if isinstance(expected, dict) and 'bytes' in expected:
        assert len(raw) == expected['bytes'], ('bytes', str(path))


def validate():
    before = load(RUN / 'before.json')['files']
    scripts = sorted((OUT / 'scripts').glob('*.py'))
    script_paths = {p.relative_to(ROOT).as_posix() for p in scripts}
    assert len(scripts) == 9
    allowed = script_paths | {'docs/STATE.md', 'tasks/T-054-khoa-g3-chay-p7-a/LOG.md'}
    changed = []
    for relative, expected in before.items():
        path = ROOT / relative
        assert path.is_file(), ('removed', relative)
        if sha(path.read_bytes()) != expected['sha256']:
            changed.append(relative)
            assert relative in allowed, ('out_of_scope', relative)
    old_log = before['tasks/T-054-khoa-g3-chay-p7-a/LOG.md']
    log = (ROOT / 'tasks/T-054-khoa-g3-chay-p7-a/LOG.md').read_bytes()
    assert sha(log[:old_log['bytes']]) == old_log['sha256'], 'LOG prefix changed'
    old_state = (RUN / 'STATE-before.txt').read_bytes()
    check_pin(RUN / 'STATE-before.txt', before['docs/STATE.md'])
    old_lines = old_state.decode('utf-8').splitlines(keepends=True)
    new_lines = (ROOT / 'docs/STATE.md').read_bytes().decode('utf-8').splitlines(keepends=True)
    assert len(old_lines) == len(new_lines)
    changed_lines = [(a, b) for a, b in zip(old_lines, new_lines) if a != b]
    assert len(changed_lines) == 1
    assert all(x.startswith('- **T-054 —') for x in changed_lines[0])

    source = load(RUN / 'source-current.json')
    for key in ('legacy_code', 'own_scripts'):
        for relative, expected in source[key].items():
            check_pin(ROOT / relative, expected)
    assert len(source['legacy_code']) == 93
    assert set(source['own_scripts']) == script_paths
    for path in scripts:
        ast.parse(path.read_bytes(), filename=str(path))

    summaries = {}
    for name in ('queue-fixtures-004', 'regression-transport-002', 'torai-a-fixtures-001',
                 'a4-guard-fixtures-001', 'regression-report-001'):
        item = load(RUN / name / 'summary.json')
        assert item['PASS'] is True, name
        summaries[name] = item
    a = summaries['torai-a-fixtures-001']
    assert a['real_author_source_opened'] is False
    assert a['prep_seed_independent_bytes'] is True
    assert [s['seed'] for s in a['three_seeds']] == [0, 1, 2]
    for item in a['three_seeds']:
        assert item['state'] == 'VERIFIED' and item['status'] == 'OK'
        check_pin(Path(item['method']['path']), item['method'])
    assert summaries['queue-fixtures-004']['count'] == 25
    assert summaries['regression-transport-002']['count'] == 60
    assert summaries['a4-guard-fixtures-001']['label_reads_on_bad_input'] == 0
    assert len(summaries['a4-guard-fixtures-001']['prelabel_counterexamples']) == 8
    assert summaries['regression-report-001']['rows'] == 89

    freeze = OUT / 'runs/freeze-cong-cu-004'
    files = load(freeze / 'files.json')['files']
    assert len(files) == 107
    for relative, expected in files.items():
        check_pin(ROOT / relative, expected)
        check_pin(freeze / 'code' / relative, expected)
    with tarfile.open(freeze / 'code.tar.gz', 'r:gz') as tar:
        assert set(tar.getnames()) == set(files)
        for member in tar.getmembers():
            assert member.isfile()
            assert sha(tar.extractfile(member).read()) == files[member.name]['sha256']
    package = load(freeze / 'package.json')
    assert package['test_allowed'] is False
    for key in ('archive', 'files_manifest'):
        check_pin(ROOT / package[key]['path'], package[key])

    import psutil
    owned = []
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            command = ' '.join(proc.info['cmdline'] or []).replace('\\', '/')
            if ('T-054/scripts/worker.py' in command or
                    ('T-054/scripts/p7.py' in command and '_supervise' in command)):
                owned.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    assert not owned, ('live_workers', owned)
    authority = load(OUT / 'authorization.json')
    assert all(authority[key] is False for key in ('pilot_grant', 'ssh_grant', 'sync_grant',
                                                  'g3', 'test_grant', 'materialize_private', 'commit_push'))
    return {'PASS': True, 'existing_files_checked': len(before), 'changed_existing_files': changed,
            'protected_existing_files_preserved': len(before) - len(changed),
            'LOG_append_only': True, 'STATE_changed_only_T054_row': True,
            'legacy_code_pins': 93, 'own_scripts_AST': 9, 'freeze_files_exact_bytes': 107,
            'archive_verified': True, 'five_summaries_verified': True, 'live_owned_workers': owned,
            'scientific_pilot_run': False, 'test_opened': False,
            'scope': 'code, pinned synthetic artifacts, metadata and process identities only'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest')
    args = parser.parse_args()
    result = validate()
    if args.manifest:
        manifest = load(ROOT / args.manifest)
        for relative, expected in manifest['outputs'].items():
            check_pin(ROOT / relative, expected)
        result['manifest_outputs_verified'] = len(manifest['outputs'])
        print(json.dumps(result, ensure_ascii=False))
    else:
        path = RUN / 'validation.json'
        assert not path.exists(), 'Không ghi đè validation'
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False))
