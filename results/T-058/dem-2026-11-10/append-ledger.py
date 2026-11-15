"""Operator-only append: verify the full hash chain and the existing prefix."""
import hashlib
import json
from pathlib import Path
import sys

source=Path(sys.argv[1]); target=Path(sys.argv[2])
data=source.read_bytes()
if data and not data.endswith(b'\n'): raise SystemExit('Incomplete ledger line')
previous='0'*64; count=0
for line in data.decode('utf8').splitlines():
    row=json.loads(line); digest=row.pop('sha256'); count+=1
    encoded=json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
    if row['sequence']!=count or row['previous_sha256']!=previous or hashlib.sha256(encoded.encode()).hexdigest()!=digest:
        raise SystemExit('Invalid ledger chain')
    previous=digest
old=target.read_bytes() if target.exists() else b''
if not data.startswith(old): raise SystemExit('Refuse to replace or alter previous ledger records')
with target.open('ab') as stream: stream.write(data[len(old):])
print('Verified ledger chain; lines',count,'appended bytes',len(data)-len(old),'last sha256',previous)
