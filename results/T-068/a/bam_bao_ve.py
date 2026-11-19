#!/usr/bin/env python3
"""T-068 A: băm lại các file trong results/T-066/bao-ve.tsv (cột duong_dan_nguon; 'x.tgz!member' đọc bằng tarfile).
In 'sha256  laptop:<đường>' theo thứ tự file; báo LECH ra stderr nếu khác cột sha256_tinh_lai của T-066."""
import csv, hashlib, sys, tarfile
rows = list(csv.DictReader(open('results/T-066/bao-ve.tsv', encoding='utf-8'), delimiter='\t'))
out, lech = [], 0
for r in rows:
    p = r['duong_dan_nguon']
    h = hashlib.sha256()
    if '!' in p:
        tgz, mem = p.split('!', 1)
        with tarfile.open(tgz, 'r:gz') as t:
            f = t.extractfile(mem)
            for b in iter(lambda: f.read(1 << 20), b''):
                h.update(b)
    else:
        with open(p, 'rb') as f:
            for b in iter(lambda: f.read(1 << 20), b''):
                h.update(b)
    out.append(f'{h.hexdigest()}  laptop:{p.replace(chr(92), "/")}')
    if h.hexdigest() != r['sha256_tinh_lai']:
        lech += 1
        print('LECH', p, file=sys.stderr)
sys.stdout.buffer.write(('\n'.join(out) + '\n').encode())
print(f'{len(out)} file, lech {lech}', file=sys.stderr)
