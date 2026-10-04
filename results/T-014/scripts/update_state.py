"""Insert/replace exactly one task line in-place; preserve every other byte."""
from pathlib import Path
import sys,hashlib,json
p=Path('D:/RCA-flashticket/docs/STATE.md')
out=Path('D:/RCA-flashticket/results/T-014/runs')
new=f'| T-014 | Hồ sơ CIRCA PC và kiến trúc | P1 | Codex | Claude | {sys.argv[1]} | `tasks/T-014-ho-so-circa/` |'.encode()
before=p.read_bytes()
lines=before.splitlines(keepends=True)
offset=0
found=False
for line in lines:
    if line.startswith(b'| T-014 |'):
        old=line.rstrip(b'\r\n'); suffix=line[len(old):]; found=True; break
    offset+=len(line)
if not found:
    table=[(sum(map(len,lines[:i+1])),line) for i,line in enumerate(lines) if line.startswith(b'| T-')]
    assert table
    offset,last=table[-1]; old=b''; suffix=b'\r\n' if last.endswith(b'\r\n') else b'\n'
replacement=new+suffix if not found else new
after=before[:offset]+replacement+before[offset+len(old):]
with p.open('r+b') as f:
    current=f.read()
    if current!=before: raise RuntimeError('STATE concurrently changed; reread and retry')
    f.seek(offset); f.write(after[offset:]); f.truncate(); f.flush()
actual=p.read_bytes()
assert actual==after
assert actual[:offset]+old+actual[offset+len(replacement):]==before
out.mkdir(exist_ok=True)
with (out/'state-updates.jsonl').open('a',encoding='utf-8') as f:
    f.write(json.dumps(dict(before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(actual).hexdigest(),old=old.decode(),new=new.decode(),preserved_other_bytes=True),ensure_ascii=False)+'\n')
print('STATE: only T-014 line updated; every other byte preserved')
