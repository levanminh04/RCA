#!/usr/bin/env python3
"""T-068 A: lập results/T-068/a/nguon-trace.json = {ca: {goi, sha_ngoai, kiem_theo}} cho 28 ca lịch sử trên laptop."""
import json, pathlib
R = pathlib.Path('D:/RCA-flashticket')
idx = json.loads((R / 'results/T-065/may-l11/du-lieu/V082-V066+H8a/chi-muc.json').read_text(encoding='utf-8'))
t062 = json.loads((R / 'results/T-062/manifest.json').read_text(encoding='utf-8'))['files']
def sums(p):
    return {l.split(' *./')[1]: l.split(' ')[0] for l in (R / p).read_text().splitlines() if ' *./' in l}
dev2, dev3 = sums('results/T-063/thu2/SHA256SUMS'), sums('results/T-063/thu3/thu/SHA256SUMS')
arch = {l.split('  ')[1]: l.split('  ')[0] for l in pathlib.Path('D:/RCA-archive/hash-lists/exp-obs-cases.sha256').read_text().splitlines()}
out = {}
for x in idx['su_co']:
    ca, n = x['ma'], x['nguon']
    if ca == 'ebd5ef38':
        out[ca] = {'goi': 'D:/RCA-archive/exp-obs/cases/ebd5ef38', 'sha_ngoai': arch['ebd5ef38/raw-traces.jsonl'],
                   'kiem_theo': 'D:/RCA-archive/hash-lists/exp-obs-cases.sha256 (raw-traces) + manifest.json của gói'}
    elif n == 't062':
        out[ca] = {'goi': f'D:/RCA-flashticket/results/T-062/ca/{ca}/cases/{ca}',
                   'sha_ngoai': t062[f'ca/{ca}/cases/{ca}/raw-traces.jsonl']['sha256'],
                   'kiem_theo': 'results/T-062/manifest.json (raw-traces) + manifest.json của gói'}
    elif n == 'dev2':
        out[ca] = {'goi': f'D:/RCA-flashticket/results/T-063/thu2/ca/{ca}.tgz', 'sha_ngoai': dev2[f'ca/{ca}.tgz'],
                   'kiem_theo': 'results/T-063/manifest-2.json → thu2/SHA256SUMS (tgz) + manifest.json trong gói'}
    else:
        out[ca] = {'goi': f'D:/RCA-flashticket/results/T-063/thu3/thu/ca/{ca}.tgz', 'sha_ngoai': dev3[f'ca/{ca}.tgz'],
                   'kiem_theo': 'results/T-063/manifest-2.json → thu3/thu/SHA256SUMS (tgz) + manifest.json trong gói'}
(R / 'results/T-068/a/nguon-trace.json').write_bytes((json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode())
print(len(out))
