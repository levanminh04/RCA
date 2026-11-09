"""Manifest T-056: sha256/bytes mọi file trong results/T-056 (trừ chính manifest)."""
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
base = REPO / 'results/T-056'
files = {}
for p in sorted(base.rglob('*')):
    if p.is_file() and p.name != 'manifest-001.json':
        b = p.read_bytes()
        files[p.relative_to(REPO).as_posix()] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
with open(base / 'manifest-001.json', 'x', encoding='utf-8') as f:
    json.dump({'schema': 'T056-MANIFEST-1', 'date': '2026-11-08', 'files': files}, f, ensure_ascii=False, indent=1)
print(len(files))
