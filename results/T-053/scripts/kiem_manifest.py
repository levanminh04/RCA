"""Đọc và kiểm manifest T-053; không ghi file."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'results/T-053'
path = BASE / 'manifest.json'
manifest = json.loads(path.read_bytes())
for table in ('declared_sources', 'outputs'):
    for name, expected in manifest[table].items():
        file = (ROOT/name).resolve()
        assert file.is_relative_to(ROOT.resolve()) and file.is_file(), name
        assert file.stat().st_size == expected['bytes'], name
        with file.open('rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == expected['sha256'], name
actual = {p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and p != path}
assert actual == set(manifest['outputs']), (actual-set(manifest['outputs']), set(manifest['outputs'])-actual)
assert len(actual) == manifest['output_count']
assert sum(v['bytes'] for v in manifest['outputs'].values()) == manifest['total_logical_bytes']
print(json.dumps(dict(PASS=True, outputs=len(actual), sources=len(manifest['declared_sources']),
                      logical_bytes=manifest['total_logical_bytes'])))
