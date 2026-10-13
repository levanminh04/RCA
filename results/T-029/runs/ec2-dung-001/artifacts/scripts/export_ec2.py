"""Đóng gói mọi artifact của lượt EC2 đã dừng; không đọc/sửa task khác."""
import hashlib
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path

B = Path.home() / 'rca/T-029'
E = B / 'export-dung-001'
E.mkdir(exist_ok=False)

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

files = sorted([p for name in ('inputs', 'scripts', 'runs') for p in (B / name).rglob('*') if p.is_file()]
               + [B / 'trang-thai.txt', B / 'STOP'])
manifest = {'task': 'T-029', 'status': 'STOPPED_P1_UNDEFINED', 'time': datetime.now(timezone.utc).isoformat(),
            'files': {p.relative_to(B).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in files},
            'file_count': len(files), 'excluded': ['tmp/', 'cache/', 'tmux.sock (socket)', 'export archive itself']}
mp = E / 'transfer-manifest.json'
mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
archive = E / 'artifacts.tar.gz'
with tarfile.open(archive, 'w:gz') as tar:
    for p in files:
        assert not p.is_symlink() and B in p.resolve().parents
        tar.add(p, arcname=p.relative_to(B).as_posix(), recursive=False)
    tar.add(mp, arcname='transfer-manifest.json', recursive=False)
result = {'file_count': len(files), 'archive_members': len(files)+1, 'archive_sha256': sha(archive),
          'manifest_sha256': sha(mp), 'archive_bytes': archive.stat().st_size}
(E / 'export-check.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
