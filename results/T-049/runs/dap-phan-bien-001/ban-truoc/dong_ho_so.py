"""Đóng manifest T-049 hoặc kiểm lại chỉ đọc, không chạy phương pháp."""
import argparse
import difflib
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-049'
MANIFEST = OUT / 'manifest.json'
LOG = 'tasks/T-049-k-b-va-t6/LOG.md'


def sha(path, length=None):
    with path.open('rb') as stream:
        return (hashlib.sha256(stream.read(length)).hexdigest() if length is not None
                else hashlib.file_digest(stream, 'sha256').hexdigest())


def info(path):
    return {'bytes': path.stat().st_size, 'sha256': sha(path)}


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def verify(name, expected, actual=None, prefix=False):
    path = ROOT / (actual or name)
    assert path.resolve().is_relative_to(ROOT.resolve()) and path.is_file(), name
    expected = expected if isinstance(expected, dict) else {'sha256': expected}
    if 'bytes' in expected:
        assert (path.stat().st_size >= expected['bytes'] if prefix
                else path.stat().st_size == expected['bytes']), ('size', name)
    assert sha(path, expected['bytes'] if prefix else None) == expected['sha256'], ('hash', name, actual)


def inventory():
    return {p.relative_to(ROOT).as_posix(): info(p)
            for p in sorted(OUT.rglob('*')) if p.is_file() and p != MANIFEST}


def prompt_check():
    template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8-sig')

    def block(heading):
        return re.search(r'```text\n(.*?)\n```', template.split(heading + '\n', 1)[1], re.S).group(1)

    actual = re.findall(r'```text\n(.*?)\n```', (ROOT / LOG).read_text(encoding='utf-8-sig'), re.S)[-1]
    suffix = '\n\n' + block('### Soát kết quả') + '\n\n' + block('### G3 — Khóa thiết kế trước khi mở test')
    assert actual.endswith(suffix), 'stage/gate prompt changed'
    source_lines = block('## Prompt chung').splitlines()
    filled_lines = actual[:-len(suffix)].splitlines()
    assert len(source_lines) == len(filled_lines)
    fields = 0
    for source, value in zip(source_lines, filled_lines):
        if source.startswith('- ') and '<' in source:
            assert value.startswith(source.split('<', 1)[0]) and '<' not in value
            fields += 1
        else:
            assert source == value, ('prompt text', source, value)
    assert fields == 8
    return fields


def source_check():
    matrix = read(OUT / 'ma-tran.json')
    for name, expected in matrix['sources'].items():
        verify(name, expected)
    assert sha(ROOT / 'tasks/T-049-k-b-va-t6/SPEC.md') == '8f4cd7ec0684c1f55eb58f6dfadae732a54db5ab6988445dbd96cce0a2b63175'
    init = read(OUT / 'manifest-khoi-tao.json')
    before = read(ROOT / init['before_manifest'])
    snapshots = before['snapshots']
    for name, snapshot in snapshots.items():
        verify(name, before['before'][name], snapshot)
    for name, value in init['mutable_log_prefixes'].items():
        verify(name, value, prefix=True)
    for name, value in before['before'].items():
        if name.endswith('LOG.md') or name in ('docs/DECISIONS.md', 'docs/WHY.md', 'docs/KE-HOACH-SAU-T047.md'):
            verify(name, value, prefix=True)
    counts = {}
    historical_code = {'src/m1/e4.py': 'results/T-049/truoc-tich-hop-001/e4.py'}
    for task, tables in (
        ('T-053', ('declared_sources', 'outputs')),
        ('T-048', ('outputs', 'closed_outputs', 'governing_sources', 'current_tools', 'source_sha256', 'upstream_manifests')),
    ):
        name = f'results/{task}/manifest.json'
        verify(name, before['before'][name])
        manifest = read(ROOT / name)
        for table in tables:
            for source, expected in manifest[table].items():
                mapping = (snapshots if table in ('declared_sources', 'governing_sources')
                           else historical_code if table == 'source_sha256' else {})
                verify(source, expected, mapping.get(source))
            counts[task + '/' + table] = len(manifest[table])
        if task == 'T-053':
            actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'results/T-053').rglob('*')
                      if p.is_file() and p != ROOT / name}
            assert actual == set(manifest['outputs'])
            assert len(actual) == manifest['output_count']
            assert sum(v['bytes'] for v in manifest['outputs'].values()) == manifest['total_logical_bytes']
    for task, names in init['verified_upstream_outputs'].items():
        outputs = read(ROOT / f'results/{task}/manifest.json')['outputs']
        if isinstance(outputs, list):
            outputs = {v['path']: v for v in outputs}
        for name in names:
            verify(name, outputs[name])
        counts[task + '/used_outputs'] = len(names)
    old = (OUT / 'runs/ban-giao-chuan-bi-001/STATE.md').read_text(encoding='utf-8-sig').splitlines()
    new = (ROOT / 'docs/STATE.md').read_text(encoding='utf-8-sig').splitlines()
    delta = list(difflib.ndiff(old, new))
    removed = [s[2:] for s in delta if s.startswith('- ')]
    added = [s[2:] for s in delta if s.startswith('+ ')]
    assert len(removed) == len(added) == 1, ('STATE scope', removed, added)
    assert removed[0].startswith('- **T-049') and added[0].startswith('- **T-049')
    return {'phase1_sources': len(matrix['sources']), 'upstream': counts,
            'unchanged_SPEC': True, 'append_only_initial_LOG': True, 'STATE_changed_lines': 1,
            'neutral_prompt_fields': prompt_check()}


def seal():
    assert read(MANIFEST)['schema'] == 'T049-chuan-bi-v1', 'Do not overwrite a final manifest'
    assert info(MANIFEST) == info(OUT / 'runs/ban-giao-chuan-bi-001/manifest.json')
    check = source_check()
    assert read(OUT / 'runs/kiem-ho-so-cuoi-001.json')['PASS'] is True
    for phase in ('kb', 't6'):
        base = OUT / f'runs/{phase}-001-cham'
        assert read(base / 'kiem-doc-lap.json')['PASS'] is True
        replay = read(base / 'replay-cap.json')
        assert replay['PASS'] is True
    receipt = OUT / 'runs/kiem-dong-ho-so-001.json'
    assert not receipt.exists()
    receipt.write_text(json.dumps({'PASS': True, **check}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    sources = [
        'AGENTS.md', 'docs/STATE.md', 'docs/MRP.md', 'docs/WHY.md', 'docs/DECISIONS.md',
        'docs/LESSONS.md', 'docs/KE-HOACH-SAU-T047.md', 'docs/review-prompt.md',
        'docs/reference/sources/DT18-de-tai-va-nhiem-vu.md',
        'docs/reference/sources/advisor-2026-09-23.md',
        'tasks/T-049-k-b-va-t6/SPEC.md', 'tasks/T-043-thiet-ke-rca-m1/SPEC.md', 'src/m1/e4.py',
    ]
    upstream = [f'results/{task}/manifest.json' for task in ('T-043', 'T-044', 'T-047', 'T-048', 'T-053')]
    outputs = inventory()
    manifest = {
        'schema': 'T049-ket-qua-v1', 'created_at': datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat(),
        'status': 'CHO_PHAN_BIEN_CLAUDE', 'implementer': 'Codex', 'reviewer': 'Claude',
        'git_HEAD': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'working_tree_revision': 'Phase-1 sources are pinned in ma-tran.json; implementation and run revisions are retained in outputs. HEAD alone is not the execution revision.',
        'runtime': {'python': 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe',
                    'PYTHONPATH': 'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages',
                    'OPENBLAS_NUM_THREADS': '1', 'PYTHONIOENCODING': 'utf-8', 'python_flags': ['-B'],
                    'remote_python': '/home/ubuntu/rca/T-025/envs/main/bin/python'},
        'phase1_main_sealed': True,
        'phase_seals': {p: info(OUT / f'runs/{p}-001-seal.json') for p in ('kb', 't6')},
        'new_method_records': {'K-b': 164, 'T6': 82, 'total': 246},
        'windows_per_phase': {'that': 52, 'ce': 30, 'total': 82},
        'method_worlds': ['P', 'S_lo', 'S_hi'],
        'decision_state': {'K-b': 'GIU_C', 'T6': 'DE_XUAT_BO',
                           'T050_baseline': 'DE_NGHI_MINH_CHOT_SAU_PHAN_BIEN', 'task_accepted': False,
                           'G3_test_opened': False, 'commit_push': False},
        'canonical': {name: f'results/T-049/{name}' for name in (
            'bao-cao.md', 'ma-tran.json', 'tai-su-dung.json', 'k-b.json', 't6.json',
            'co-che.json', 'do-ben.json', 'so-lan-nhin.jsonl', 'nen-de-nghi-T050.json', 'thoi-gian.json')},
        'outputs': outputs, 'output_count': len(outputs),
        'total_logical_bytes': sum(v['bytes'] for v in outputs.values()),
        'inventory_exclusion': 'Only results/T-049/manifest.json itself is excluded. Nested historical manifests are included.',
        'current_sources': {p: info(ROOT / p) for p in sources},
        'upstream_manifests': {p: info(ROOT / p) for p in upstream},
        'mutable_log_prefixes': {LOG: info(ROOT / LOG)},
        'log_policy': 'Verify the exact byte prefix. Later authorized append-only verification receipts or handoffs may follow it.',
        'checks': check,
        'historical_policy': 'Original sources, failed attempts, old preparation manifest and prior edited revisions are retained. Historical governance uses the exact snapshots declared in manifest-khoi-tao.json; old e4 uses truoc-tich-hop-001/e4.py. No historical manifest is relabeled.',
        'limitations': 'Computational chains and dev decisions only. Physical causes, full VC/E5 interaction, independent effectiveness, verdict, mode (b), RE3-OB and FlashTicket remain open as stated in bao-cao.md.',
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def check_final():
    manifest = read(MANIFEST)
    assert manifest['schema'] == 'T049-ket-qua-v1'
    actual = inventory()
    assert actual == manifest['outputs'], 'final output inventory/hash'
    assert len(actual) == manifest['output_count']
    assert sum(v['bytes'] for v in actual.values()) == manifest['total_logical_bytes']
    for table in ('current_sources', 'upstream_manifests'):
        for name, expected in manifest[table].items():
            verify(name, expected)
    for name, expected in manifest['mutable_log_prefixes'].items():
        verify(name, expected, prefix=True)
    assert prompt_check() == 8
    print(json.dumps({'PASS': True, 'outputs': len(actual), 'logical_bytes': manifest['total_logical_bytes'],
                      'sources': len(manifest['current_sources']), 'upstream_manifests': len(manifest['upstream_manifests']),
                      'LOG_prefix': True, 'neutral_prompt': True}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seal', action='store_true', help='One-time final manifest creation')
    args = parser.parse_args()
    if args.seal:
        seal()
    check_final()
