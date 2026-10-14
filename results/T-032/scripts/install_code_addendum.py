"""Install the explicitly authorized five source code files inside T-032 only."""
import hashlib
import json
from pathlib import Path
import tarfile

BASE = Path('/home/ubuntu/rca/T-032')
FILES = {'src/circa_kien_truc/__init__.py', 'src/circa_kien_truc/builder.py',
         'src/circa_kien_truc/scoring.py', 'src/torai/__init__.py', 'src/torai/torai_sua.py'}
MANIFEST_SHA = 'f241b48cb0fd336aac5e6bf409cc811d945d99d6dee3ffcc1c4136ad8724974e'
ARCHIVE_SHA = '38d78fb15ee7cf922e02b926684af68a14a5adfc2d73149fe6ea80c9210af1ac'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
manifest = BASE / 'inputs/method-code-addendum-001.json'
archive = BASE / 'inputs/method-code-addendum-001.tar.gz'
assert sha(manifest) == MANIFEST_SHA and sha(archive) == ARCHIVE_SHA
meta = json.loads(manifest.read_text(encoding='utf-8-sig'))
rows = {r['path']: r for r in meta['files']}
assert set(rows) == FILES and len(rows) == len(meta['files'])
environment = BASE / 'repo' / meta['source_environment']['path']
assert sha(environment) == meta['source_environment']['sha256']
with tarfile.open(archive) as tar:
    members = tar.getmembers()
    assert len(members) == len(FILES) and {m.name for m in members} == FILES
    contents = {}
    for member in members:
        assert member.isfile() and not member.issym() and not member.islnk()
        payload = tar.extractfile(member).read()
        assert len(payload) == rows[member.name]['bytes']
        assert hashlib.sha256(payload).hexdigest() == rows[member.name]['sha256']
        dest = (BASE / 'repo' / member.name).resolve()
        assert dest.is_relative_to((BASE / 'repo').resolve())
        if dest.exists():
            assert sha(dest) == rows[member.name]['sha256']
        contents[dest] = payload
for dest, payload in contents.items():
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as stream:
            stream.write(payload)
out = BASE / 'runs/method-code-install-001'
out.mkdir(exist_ok=False)
receipt = {'status': 'PASS', 'manifest_sha256': MANIFEST_SHA, 'archive_sha256': ARCHIVE_SHA,
           'files': [{**r, 'remote_sha256': sha(BASE/'repo'/r['path'])} for r in rows.values()]}
(out/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt), flush=True)
