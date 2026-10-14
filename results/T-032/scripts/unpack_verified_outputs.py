"""Local artifact transport check/extraction only; no research methods."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile

ROOT = Path(__file__).resolve().parents[1] / 'runs/thu-ec2-003'
EXPECTED = {
    'baro-nezha-export-001': ('baro-nezha-verified.tar.gz',
        'fce1ed0baed254e9078f0da662206b00bc916a526b66985bbe8f61bf58ef568a',
        '82f9acf4a7a29bf01b9ffa50439e64d50888a6ccdd28f5775f9cc506d147ec0b'),
    'coverage-export-001': ('coverage-verified.tar.gz',
        '64103ae84c542103e556e4badbddbfbd64d76d4826fb9e94f0f61b0964a2db6e',
        'eb6d13de95ac4840a14f5a9ed28359a869c5f6284e927ac933255da7c697c5e0'),
}


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


out = ROOT / 'verified'
out.mkdir(exist_ok=False)
receipts = []
for stage, (name, archive_sha, inventory_sha) in EXPECTED.items():
    directory = ROOT / stage
    archive, inv = directory / name, directory / 'file-inventory.json'
    if digest(archive) != archive_sha or digest(inv) != inventory_sha:
        raise RuntimeError('Transport hash mismatch: ' + stage)
    rows = json.loads(inv.read_text(encoding='utf-8'))['files']
    expected = {r['path']: r for r in rows}
    if len(expected) != len(rows):
        raise RuntimeError('Inventory duplicate path')
    seen = set()
    with tarfile.open(archive, 'r:gz') as tar:
        for member in tar:
            p = PurePosixPath(member.name)
            if not member.isfile() or p.is_absolute() or '..' in p.parts or ':' in member.name:
                raise RuntimeError('Unsafe archive member')
            if not p.parts or p.parts[0] != 'runs' or member.name not in expected or member.name in seen:
                raise RuntimeError('Unexpected/duplicate archive member')
            row = expected[member.name]
            if member.size != row['bytes']:
                raise RuntimeError('Archive member size mismatch')
            target = (out / member.name).resolve()
            if not target.is_relative_to(out.resolve()):
                raise RuntimeError('Extraction escaped output root')
            stream = tar.extractfile(member)
            blob = stream.read()
            if len(blob) != row['bytes'] or hashlib.sha256(blob).hexdigest() != row['sha256']:
                raise RuntimeError('Archive member byte mismatch')
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as f:
                f.write(blob)
            seen.add(member.name)
    if seen != set(expected):
        raise RuntimeError('Missing archive members')
    for row in rows:
        if digest(out / row['path']) != row['sha256']:
            raise RuntimeError('Extracted byte mismatch')
    receipts.append({'stage': stage, 'status': 'PASS', 'archive_sha256': archive_sha,
                     'inventory_sha256': inventory_sha, 'n_files': len(rows),
                     'all_extracted_file_hashes_pass': True})
    print(json.dumps(receipts[-1]), flush=True)
with (ROOT / 'transport-check.json').open('x', encoding='utf-8') as f:
    json.dump({'status': 'PASS', 'stages': receipts, 'output_root': str(out),
               'methods_executed': False}, f, ensure_ascii=False, indent=2)
    f.write('\n')
