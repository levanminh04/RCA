"""List this audit branch files, including every created userspace runtime file."""
import csv
import hashlib
from pathlib import Path
import sys

out=Path(__file__).resolve().parent
work=Path('D:/RCA-ext/work/T-014')
subtrees=['downloads','tools/innoextract-1.9','R','R-library','audit-r']
if '--outputs-only' not in sys.argv:
    with (out/'external-files.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['path','bytes','sha256','purpose'])
        for subtree in subtrees:
            root=work/subtree
            for path in sorted(root.rglob('*')):
                if path.is_file():
                    digest=hashlib.sha256(path.read_bytes()).hexdigest()
                    writer.writerow([path.as_posix(),path.stat().st_size,digest,subtree])
with (out/'output-files.csv').open('w',encoding='utf-8-sig',newline='') as stream:
    writer=csv.writer(stream);writer.writerow(['path','bytes','sha256'])
    for path in sorted(out.rglob('*')):
        if path.is_file() and path.name!='output-files.csv':
            writer.writerow([path.as_posix(),path.stat().st_size,hashlib.sha256(path.read_bytes()).hexdigest()])
print('external files:',sum(1 for _ in (out/'external-files.csv').open(encoding='utf-8-sig'))-1)
print('audit output files:',sum(1 for _ in (out/'output-files.csv').open(encoding='utf-8-sig'))-1)
