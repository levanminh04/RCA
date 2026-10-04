import csv,hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parent
checks={}; total=0
for name in ['network-manifest.json','architecture-manifest.json','diagram-metadata-manifest.json']:
    m=json.loads((BASE/name).read_text(encoding='utf-8'))
    assert m['total_bytes']==sum(e.get('bytes',0) for e in m['entries'])
    total+=m['total_bytes']
    for e in m['entries']:
        b=(BASE/e['artifact']).read_bytes()
        assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
        assert not e.get('error')
    checks[name]=True
d=json.loads((BASE/'diagram-manifest.json').read_text(encoding='utf-8')); b=(BASE/d['artifact']).read_bytes()
assert len(b)==d['expected_bytes'] and hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==d['git_blob_oid']
assert hashlib.sha256(b).hexdigest()==d['sha256']
total+=len(b); assert total==652287 and total<=3000000
checks['diagram_hash_and_byte']=True
rows=list(csv.DictReader((BASE/'ss-census.csv').open(encoding='utf-8',newline='')))
files=list(csv.DictReader((BASE/'ss-files.csv').open(encoding='utf-8',newline='')))
cells=list(csv.DictReader((BASE/'ss-cells.csv').open(encoding='utf-8',newline='')))
assert len(rows)==245 and sum(int(r['file_count']) for r in rows)==len(files)==618
assert sum(int(c['n_cases']) for c in cells)==len(rows) and len(cells)==64
assert all(r['has_trace']=='False' for r in rows)
checks['census_total_cells_files_no_duplicate_keys']=True
label=json.loads((BASE/'label-audit.json').read_text(encoding='utf-8')); assert label['n_files']==8 and label['n_unique_file_hashes']==7
assert all(e['hash_matches_tree'] for e in label['entries'])
assert sum(not e['indicator_time_in_log_window'] for e in label['entries'])==1
checks['eight_label_files_checked_against_tree_and_logs']=True
edges=list(csv.DictReader((BASE/'architecture-edges.csv').open(encoding='utf-8',newline='')))
positions=list(csv.DictReader((BASE/'architecture-root-positions.csv').open(encoding='utf-8',newline='')))
for r in positions:
    neighbors={e['target_normalized'] if e['source_normalized']==r['root'] else e['source_normalized'] for e in edges if r['root'] in [e['source_normalized'],e['target_normalized']]}
    assert len(neighbors)==int(r['undirected_degree_visible_internal_links'])
    assert all(r[k]=='OPEN' for k in ['directed_in_degree','directed_out_degree'])
checks['static_picture_degree_matches_saved_edge_list']=True
out=dict(checks=checks,controlled_source_download_bytes=total,network_cap_bytes=3000000,status='PASS',n_files_before_manifest=len(list(BASE.rglob('*'))))
(BASE/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
art=[]
for p in sorted(BASE.rglob('*')):
    if p.is_file() and p.name!='artifact-manifest.json':
        b=p.read_bytes(); art.append(dict(path=p.relative_to(BASE).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(BASE/'artifact-manifest.json').write_text(json.dumps(dict(artifacts=art,self='artifact-manifest.json lists all other files; self not hashed'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status='PASS',checks=checks,controlled_source_download_bytes=total,artifacts=len(art)),indent=2))
