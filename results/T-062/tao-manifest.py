#!/usr/bin/env python3
"""T-062: manifest.json = SHA-256 + kích thước mọi file trong results/T-062 (trừ chính manifest). Dùng: py -3 -B results/T-062/tao-manifest.py"""
import hashlib, json, datetime as dt
from pathlib import Path
G = Path(__file__).resolve().parent
files = {}
for p in sorted(G.rglob('*')):
    if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts:
        h = hashlib.sha256()
        with p.open('rb') as f:
            for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
        files[p.relative_to(G).as_posix()] = {'sha256': h.hexdigest(), 'bytes': p.stat().st_size}
(G / 'manifest.json').write_text(json.dumps({'tao_luc_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'so_file': len(files), 'files': files}, indent=1) + '\n', encoding='utf-8')
print(len(files), 'file')
