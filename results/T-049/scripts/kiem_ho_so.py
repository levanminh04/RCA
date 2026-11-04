"""Kiểm hồ sơ khởi tạo T-049 và bằng chứng đóng T-048/T-053; chỉ đọc."""
import difflib
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INIT = ROOT / 'results/T-049/manifest-khoi-tao.json'


def digest(path, size=None):
    with path.open('rb') as stream:
        return hashlib.sha256(stream.read(size)).hexdigest() if size is not None else hashlib.file_digest(stream, 'sha256').hexdigest()


def verify(name, expected, snapshots=None):
    path = ROOT / name
    if snapshots and name in snapshots:
        path = ROOT / snapshots[name]
    assert path.resolve().is_relative_to(ROOT.resolve()) and path.is_file(), name
    value = expected if isinstance(expected, dict) else {'sha256': expected}
    if 'bytes' in value:
        assert path.stat().st_size == value['bytes'], ('size', name)
    assert digest(path) == value['sha256'], ('hash', name)


def main():
    init = json.loads(INIT.read_bytes())
    before = json.loads((ROOT / init['before_manifest']).read_bytes())
    snapshots = before['snapshots']
    for name, snapshot in snapshots.items():
        verify(snapshot, before['before'][name])
    append_only = [name for name in before['before'] if name.endswith('LOG.md') or name in ('docs/DECISIONS.md', 'docs/WHY.md', 'docs/KE-HOACH-SAU-T047.md')]
    for name in append_only:
        value = before['before'][name]
        assert digest(ROOT/name, value['bytes']) == value['sha256'], ('old prefix changed', name)
    for name, value in init['current_sources'].items():
        verify(name, value)
    for name, value in init['outputs'].items():
        verify(name, value)
    for name, value in init['mutable_log_prefixes'].items():
        assert digest(ROOT/name, value['bytes']) == value['sha256'], ('LOG prefix', name)
    counts = {}
    for task, tables in (
        ('T-053', ('declared_sources', 'outputs')),
        ('T-048', ('outputs', 'closed_outputs', 'governing_sources', 'current_tools', 'source_sha256', 'upstream_manifests')),
    ):
        manifest_path = f'results/{task}/manifest.json'
        verify(manifest_path, before['before'][manifest_path])
        manifest = json.loads((ROOT/manifest_path).read_bytes())
        for table in tables:
            for name, expected in manifest[table].items():
                verify(name, expected, snapshots if table in ('declared_sources', 'governing_sources') else None)
            counts[task+'/'+table] = len(manifest[table])
        if task == 'T-053':
            excluded = (ROOT/manifest_path).resolve()
            actual = {f.relative_to(ROOT).as_posix() for f in (ROOT/'results/T-053').rglob('*') if f.is_file() and f.resolve() != excluded}
            assert actual == set(manifest['outputs']), 'T-053 inventory'
            assert len(actual) == manifest['output_count']
            assert sum(x['bytes'] for x in manifest['outputs'].values()) == manifest['total_logical_bytes']
    for task, names in init['verified_upstream_outputs'].items():
        manifest = json.loads((ROOT/f'results/{task}/manifest.json').read_bytes())
        outputs = manifest['outputs']
        if isinstance(outputs, list):
            outputs = {row['path']:row for row in outputs}
        for name in names:
            verify(name, outputs[name])
    old = (ROOT/snapshots['docs/STATE.md']).read_text(encoding='utf-8').splitlines()
    new = (ROOT/'docs/STATE.md').read_text(encoding='utf-8').splitlines()
    delta = list(difflib.ndiff(old, new))
    removed = [s[2:] for s in delta if s.startswith('- ')]
    added = [s[2:] for s in delta if s.startswith('+ ')]
    assert len(removed) == 2 and len(added) == 3, ('STATE scope', removed, added)
    assert all(s.startswith(('- **T-053', '- M1:')) for s in removed)
    assert all(s.startswith(('- **T-048', '- **T-049', '- **T-053')) for s in added)
    template = (ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')
    def block(heading):
        part = template.split(heading+'\n', 1)[1]
        return re.search(r'```text\n(.*?)\n```', part, re.S).group(1)
    common = block('## Prompt chung')
    gate = block('### G3 — Khóa thiết kế trước khi mở test')
    for name, stage in (
        ('tasks/T-049-k-b-va-t6/LOG.md', 'Soát SPEC'),
        ('tasks/T-048-thang-diem-tham-so-e4/LOG.md', 'Kiểm lại phản hồi và sửa'),
        ('tasks/T-053-kiem-z-chay-lai-k/LOG.md', 'Kiểm lại phản hồi và sửa'),
    ):
        text = (ROOT/name).read_text(encoding='utf-8')
        actual = re.findall(r'```text\n(.*?)\n```', text, re.S)[-1]
        suffix = '\n\n'+block('### '+stage)+'\n\n'+gate
        assert actual.endswith(suffix), ('prompt blocks', name)
        filled = actual[:-len(suffix)]
        source_lines, filled_lines = common.splitlines(), filled.splitlines()
        assert len(source_lines) == len(filled_lines)
        field_count = 0
        for source, value in zip(source_lines, filled_lines):
            if source.startswith('- ') and '<' in source:
                assert value.startswith(source.split('<', 1)[0]) and '<' not in value
                field_count += 1
            else:
                assert source == value, ('prompt text', name, source, value)
        assert field_count == 8
    decisions = (ROOT/'docs/DECISIONS.md').read_text(encoding='utf-8')
    for q in (236, 237, 238):
        assert len(re.findall(r'^\| Q-'+str(q)+r' \|', decisions, re.M)) == 1
    spec = (ROOT/'tasks/T-049-k-b-va-t6/SPEC.md').read_text(encoding='utf-8')
    assert len(re.findall(r'^\| K-', spec, re.M)) == 4
    assert 'src/m1/e4.py' in spec and 'T6 dùng luat_C' in spec and 'K-b dùng khoi_K' in spec
    print(json.dumps({'PASS':True, 'counts':counts, 'append_only':len(append_only), 'state_removed':len(removed), 'state_added':len(added), 'neutral_prompts':3, 'snapshots':len(snapshots), 'init_outputs':len(init['outputs']), 'no_method_runs':True}, ensure_ascii=False))


if __name__ == '__main__':
    main()
