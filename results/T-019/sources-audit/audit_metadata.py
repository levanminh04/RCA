"""Independent SS metadata census and source checksum audit; no telemetry reads."""
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[2]
OLD = REPO / 'results/T-002/public-metadata/run-002'

def dump(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def csvout(name, rows, fields):
    with (BASE/name).open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

manifest=json.loads((OLD/'source-manifest.json').read_text(encoding='utf-8'))
checks=[]
for e in manifest:
    p=OLD/e['artifact']; b=p.read_bytes()
    checks.append(dict(path=p.relative_to(REPO).as_posix(), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), expected_sha256=e['sha256'], ok=len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'], revision=e.get('revision'), url=e['url']))
assert all(e['ok'] for e in checks)
pages=[json.loads((OLD/f'sources/hf-tree-page-{n:03}.json').read_text(encoding='utf-8')) for n in (1,2,3)]
entries=[e for p in pages for e in p]
combined=json.loads((OLD/'hf-tree.json').read_text(encoding='utf-8'))
assert combined==entries
assert len({e['path'] for e in entries})==len(entries)
dump('source-reuse-checks.json', dict(checks=checks, tree_combined_equals_raw_pages=True, page_entry_counts=list(map(len,pages)), n_entries=len(entries), combined_sha256=hashlib.sha256((OLD/'hf-tree.json').read_bytes()).hexdigest(), new_network_bytes=0))

case_re=re.compile(r'^(re[123]ss)_(.+)_([^_]+)_(\d+)$')
case_rows=[]; file_rows=[]; grouped=defaultdict(list)
for e in entries:
    if e['type']=='file' and '/' in e['path']:
        grouped[e['path'].split('/')[0]].append(e)
for e in entries:
    if e['type']!='directory' or '/' in e['path']: continue
    m=case_re.fullmatch(e['path'])
    if not m: continue
    suite,root,fault,repeat=m.groups(); fs=grouped[e['path']]; names={x['path'].split('/')[-1] for x in fs}
    row=dict(case=e['path'], dataset=suite[:3].upper()+'-SS', root=root, fault=fault, repetition=int(repeat), has_metric='metrics.parquet' in names, has_log='logs.parquet' in names, has_trace='traces.parquet' in names, has_inject_time='inject_time.txt' in names, has_root_cause='root_cause.txt' in names, file_count=len(fs), bytes=sum(x['size'] for x in fs))
    case_rows.append(row)
    for x in fs:
        file_rows.append(dict(case=e['path'], path=x['path'], bytes=x['size'], oid=x['oid'], lfs_sha256=x.get('lfs',{}).get('oid',''), modality=Path(x['path']).name))
case_rows.sort(key=lambda x:x['case']); file_rows.sort(key=lambda x:x['path'])
assert len({(r['dataset'],r['root'],r['fault'],r['repetition']) for r in case_rows})==len(case_rows)
cells=defaultdict(list)
for r in case_rows: cells[(r['dataset'],r['root'],r['fault'])].append(r['repetition'])
cell_rows=[dict(dataset=d,root=r,fault=f,n_cases=len(v), repetitions=','.join(map(str,sorted(v))), unique_repetitions=len(set(v))) for (d,r,f),v in sorted(cells.items())]
summary=[]
for d in ['RE1-SS','RE2-SS','RE3-SS']:
    rs=[r for r in case_rows if r['dataset']==d]
    summary.append(dict(dataset=d,n_cases=len(rs),roots=dict(Counter(r['root'] for r in rs)),faults=dict(Counter(r['fault'] for r in rs)),n_cells=sum(c['dataset']==d for c in cell_rows),file_count=sum(r['file_count'] for r in rs),bytes=sum(r['bytes'] for r in rs),modality_counts={k:sum(r[k] for r in rs) for k in ['has_metric','has_log','has_trace','has_inject_time','has_root_cause']},missing_log_cases=[r['case'] for r in rs if not r['has_log']],root_cause_cases=[r['case'] for r in rs if r['has_root_cause']]))
assert sum(r['file_count'] for r in case_rows)==len(file_rows)
assert sum(c['n_cases'] for c in cell_rows)==len(case_rows)
csvout('ss-census.csv',case_rows,list(case_rows[0])); csvout('ss-files.csv',file_rows,list(file_rows[0])); csvout('ss-cells.csv',cell_rows,list(cell_rows[0])); dump('ss-summary.json',summary)
print(json.dumps(summary, ensure_ascii=False, indent=2))
