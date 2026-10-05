from pathlib import Path
import json,csv,hashlib,re
from datetime import datetime,timezone
from collections import Counter
import time
started=time.perf_counter()
ROOT=Path('D:/RCA-flashticket');OUT=ROOT/'results/T-020/trung-gian/dataset_evidence'
def js(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def rows(n):return list(csv.DictReader((OUT/n).read_text(encoding='utf-8-sig').splitlines()))
matrix=rows('01-bang-tieu-chi-hop-nhat.csv');checks=rows('checks.csv');sample=rows('seeded-checks.csv');selected=rows('root-selected-checks.csv')
assert len(matrix)==40 and len({x['dataset'] for x in matrix})==40
assert all(x['sources'] and all(x['C'+str(i)] and any(t in x['C'+str(i)] for t in ['FACT','OPEN']) for i in range(1,10)) for x in matrix)
assert all(x['match']=='True' for x in checks)
assert Counter(x['task'] for x in sample)=={x:5 for x in ['T-002','T-003','T-008','T-009','T-010','T-011','T-012','T-019']}
for f in ['independence-axes.csv','schema-provenance.csv','license-revision.csv','task-matrix.csv']:
    assert {x['dataset'] for x in rows(f)}=={x['dataset'] for x in matrix},f
for x in rows('independence-axes.csv'):
    assert all(x[k] for k in ['authors','injector','collector','reuse','c9_state'])
freeze=js('results/T-020/trung-gian/input-freeze.json');frozen={x['path']:x for x in freeze['inputs']}
input_records={}
for name in ['input-hashes-used.json','provenance-input-hashes.json']:
    for x in js('results/T-020/trung-gian/dataset_evidence/'+name):input_records[x['path']]=x
for x in js('results/T-020/trung-gian/dataset_evidence/schema-witnesses.json'):
    p=x['source']; input_records[p]=dict(path=p,sha256=x['sha256'],bytes=(ROOT/p).stat().st_size)
inputaudit=[]
for p,x in sorted(input_records.items()):
    assert not p.startswith('data/') and 'locked' not in p.lower() and p!='results/T-010/runs/schema-samples.json',p
    now=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
    if p in frozen:
        state='MATCH' if now==x['sha256']==frozen[p]['sha256'] else 'MISMATCH'
        assert state=='MATCH',(p,now,x['sha256'],frozen[p]['sha256'])
    else:state='DERIVED_T020_WORKER_OUTPUT' if p.startswith('results/T-020/') else 'OUTSIDE_FREEZE'
    inputaudit.append(dict(path=p,state=state,bytes=x['bytes'],sha256=now,frozen_sha256=frozen.get(p,{}).get('sha256',''),reason='Frozen original input check' if p in frozen else 'Generated during same T020; no claim original frozen input'))
with (OUT/'freeze-recheck.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(inputaudit[0]));w.writeheader();w.writerows(inputaudit)
audit=dict(utc=datetime.now(timezone.utc).isoformat(),head=freeze['head'],freeze_sha256=hashlib.sha256((ROOT/'results/T-020/trung-gian/input-freeze.json').read_bytes()).hexdigest(),datasets=40,criteria=9,criteria_cells=360,blank_source_rows=0,numeric_checks=len(checks),numeric_all_match=True,seeded_important_checks=len(sample),root_selected_checks=len(selected),root_selected_status=Counter(x['status'] for x in selected),data_leakage_rows=len(rows('leakage-data.csv')),mapping_rows=len(rows('root-mapping.csv')),c9_rows=len(rows('independence-axes.csv')),schema_rows=len(rows('schema-provenance.csv')),license_rows=len(rows('license-revision.csv')),runner_rows=len(rows('runner-leakage-method-worker.csv')),frozen_inputs=Counter(x['state'] for x in inputaudit),scope_incident='scope-incident.md/json: saved mixed schema/raw payload seen; current scripts block file. No broad no-raw claim for whole task.',replay_scope='Only existing saved metadata/schema/aggregate/public sources. No raw directory, locked, EC2, method execution, download of measurements, or recommendation',audit_elapsed_seconds=time.perf_counter()-started)
(OUT/'final-validation.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest=[]
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name!='output-manifest.json':
        manifest.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(OUT/'output-manifest.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),scope='Only dataset_evidence artifacts, including failed runs and scope incident',files=manifest),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False))
