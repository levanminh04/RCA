"""T-061: băm hai mẫu đã chuyển đổi (trước mọi bước ghép đáp án). Cách dùng: py -3 bam-mau.py"""
import hashlib, json
from pathlib import Path
mau = Path(__file__).resolve().parent / 'mau'
files = {p.name: {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
         for p in sorted(mau.glob('*.json')) if not p.name.endswith('.phat-lai.json') and p.name != 'manifest-mau.json'}
(mau / 'manifest-mau.json').write_text(json.dumps({'files': files}, indent=1) + '\n', encoding='utf-8')
print(json.dumps(files, indent=1))
